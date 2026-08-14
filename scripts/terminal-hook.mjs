#!/usr/bin/env node

import { execFileSync } from "node:child_process";
import { createHash, randomUUID } from "node:crypto";
import {
  closeSync,
  existsSync,
  fstatSync,
  lstatSync,
  mkdirSync,
  openSync,
  readdirSync,
  readFileSync,
  readlinkSync,
  readSync,
  renameSync,
  rmSync,
  statSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, relative, resolve } from "node:path";

const SCHEMA_VERSION = 2;
const MAX_ENVELOPE_BYTES = 64 * 1024;
const STATE_TTL_MS = 7 * 24 * 60 * 60 * 1000;
const ENVELOPE_TTL_MS = 24 * 60 * 60 * 1000;
const LOCK_STALE_MS = 5 * 60 * 1000;
const LOCK_WAIT_MS = 60_000;
const GIT_TIMEOUT_MS = 60_000;
const FINGERPRINT_TIMEOUT_MS = 120_000;
const FILE_HASH_BUFFER_BYTES = 1024 * 1024;
const PENDING_TOOL_TTL_MS = 30 * 60 * 1000;
const PENDING_TOOL_LIMIT = 256;
const JOURNAL_LIMIT = 1024;
const OWNER_NAMES = new Set([
  "product-management",
  "software-architecture",
  "backend-engineering",
  "web-engineering",
  "android-engineering",
  "ios-engineering",
  "database-engineering",
  "platform-engineering",
  "security-engineering",
  "quality-engineering",
  "release-engineering",
]);
const FACT_ACTIONS = new Set(["ADD", "UPDATE", "DELETE", "NO_CHANGE"]);
const RESULTS = new Set(["SYNCED", "NO_CHANGE", "DEFERRED", "BLOCKED"]);
const CREDENTIAL_KEY_PATTERN =
  /(?:password|passwd|pwd|secret|token|authorization|api[_-]?key|client[_-]?secret|private[_-]?key|access[_-]?key|account[_-]?key|signing[_-]?key|connection[_-]?string|credential|cookie)/i;

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value)
      .sort()
      .map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`)
      .join(",")}}`;
  }
  return JSON.stringify(value);
}

function toolInputDigest(value) {
  return sha256(canonicalJson(value ?? {}));
}

function parseArguments(argv) {
  const args = { command: "", json: false };
  const rest = [...argv];
  if (rest[0] && !rest[0].startsWith("-")) args.command = rest.shift();
  while (rest.length > 0) {
    const token = rest.shift();
    if (token === "--json") {
      args.json = true;
      continue;
    }
    if (!token?.startsWith("--")) continue;
    const name = token.slice(2).replaceAll("-", "_");
    const value = rest[0] && !rest[0].startsWith("--") ? rest.shift() : true;
    args[name] = value;
  }
  return args;
}

function emit(value) {
  process.stdout.write(`${JSON.stringify(value)}\n`);
}

function safeComponent(value, fallback = "unknown") {
  const normalized = String(value ?? "").trim();
  return /^[A-Za-z0-9._-]{1,160}$/.test(normalized) ? normalized : sha256(normalized || fallback);
}

function normalizePath(path) {
  return resolve(path).replaceAll("\\", "/").toLowerCase();
}

function isSafeProductId(value) {
  return (
    /^[A-Za-z0-9._-]+$/.test(value) &&
    value !== "." &&
    value !== ".."
  );
}

function isOwnerFactBookPath(value) {
  const parts = String(value).replaceAll("\\", "/").split("/");
  if (
    parts.length !== 4 ||
    parts[0] !== "docs" ||
    parts[1] !== "product-studio" ||
    !isSafeProductId(parts[2]) ||
    !parts[3].endsWith(".md")
  ) {
    return false;
  }
  return OWNER_NAMES.has(parts[3].slice(0, -3));
}

function dataRoot(args) {
  const configured =
    args.data_dir ??
    process.env.PLUGIN_DATA ??
    process.env.CLAUDE_PLUGIN_DATA ??
    process.env.PRODUCT_STUDIO_DATA;
  if (!configured) {
    throw new Error("Plugin data directory is required; pass --data-dir.");
  }
  const root = resolve(configured);
  mkdirSync(root, { recursive: true });
  return root;
}

function statePath(root, sessionId) {
  return join(root, "states", `${safeComponent(sessionId)}.json`);
}

function journalPath(root, repositoryRoot) {
  return join(root, "journals", `${sha256(normalizePath(repositoryRoot))}.json`);
}

function envelopePath(root, sessionId, turnKey) {
  return join(
    root,
    "envelopes",
    safeComponent(sessionId),
    `${safeComponent(turnKey)}.json`,
  );
}

function readJson(path, fallback) {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch {
    return fallback;
  }
}

function atomicWriteJson(path, value) {
  mkdirSync(dirname(path), { recursive: true });
  const temporary = `${path}.${process.pid}.${randomUUID()}.tmp`;
  writeFileSync(temporary, `${JSON.stringify(value)}\n`, { mode: 0o600 });
  renameSync(temporary, path);
}

function sleep(milliseconds) {
  const view = new Int32Array(new SharedArrayBuffer(4));
  Atomics.wait(view, 0, 0, milliseconds);
}

function withLock(path, callback) {
  const lock = `${path}.lock`;
  const deadline = Date.now() + LOCK_WAIT_MS;
  mkdirSync(dirname(lock), { recursive: true });
  for (;;) {
    try {
      mkdirSync(lock);
      writeFileSync(
        join(lock, "owner.json"),
        JSON.stringify({ pid: process.pid, createdAt: new Date().toISOString() }),
      );
      break;
    } catch (error) {
      if (error?.code !== "EEXIST") throw error;
      try {
        const owner = readJson(join(lock, "owner.json"), null);
        let alive = false;
        if (Number.isInteger(owner?.pid) && owner.pid > 0) {
          try {
            process.kill(owner.pid, 0);
            alive = true;
          } catch (probeError) {
            alive = probeError?.code === "EPERM";
          }
        }
        const hasOwner = Number.isInteger(owner?.pid) && owner.pid > 0;
        if (
          (!alive && hasOwner) ||
          (!hasOwner && Date.now() - statSync(lock).mtimeMs > LOCK_STALE_MS)
        ) {
          rmSync(lock, { recursive: true, force: true });
          continue;
        }
      } catch {
        continue;
      }
      if (Date.now() >= deadline) throw new Error(`Timed out waiting for state lock: ${lock}`);
      sleep(20);
    }
  }
  try {
    return callback();
  } finally {
    rmSync(lock, { recursive: true, force: true });
  }
}

function git(repositoryRoot, args, options = {}) {
  return execFileSync("git", args, {
    cwd: repositoryRoot,
    encoding: options.encoding ?? "utf8",
    maxBuffer: options.maxBuffer ?? 64 * 1024 * 1024,
    stdio: ["ignore", "pipe", "pipe"],
    timeout: options.timeout ?? GIT_TIMEOUT_MS,
  });
}

function resolveRepositoryRoot(cwd) {
  return git(cwd, ["rev-parse", "--show-toplevel"]).trim();
}

function emptyJournal(repositoryRoot) {
  return {
    schemaVersion: SCHEMA_VERSION,
    repositoryRoot,
    revision: 0,
    nextSequence: 1,
    floorSequence: 1,
    pending: {},
    events: [],
  };
}

function readJournal(root, repositoryRoot) {
  const path = journalPath(root, repositoryRoot);
  if (!existsSync(path)) return emptyJournal(repositoryRoot);
  let journal;
  try {
    journal = JSON.parse(readFileSync(path, "utf8"));
  } catch {
    throw new Error("Repository event journal is corrupt; refusing to rebaseline.");
  }
  if (journal?.schemaVersion !== SCHEMA_VERSION) {
    throw new Error("Repository event journal schema is unsupported; refusing to rebaseline.");
  }
  if (
    !Number.isInteger(journal.revision) ||
    !Number.isInteger(journal.nextSequence) ||
    !Number.isInteger(journal.floorSequence) ||
    !journal.pending ||
    typeof journal.pending !== "object" ||
    !Array.isArray(journal.events)
  ) {
    throw new Error("Repository event journal is invalid; refusing to rebaseline.");
  }
  return journal;
}

function writeJournal(root, repositoryRoot, journal) {
  journal.revision += 1;
  atomicWriteJson(journalPath(root, repositoryRoot), journal);
}

function pendingToolKey(sessionId, turnKey, toolUseId) {
  return sha256(canonicalJson([sessionId, turnKey, toolUseId]));
}

function pruneJournal(journal) {
  const now = Date.now();
  for (const [key, pending] of Object.entries(journal.pending)) {
    if (now - Date.parse(pending.startedAt) <= PENDING_TOOL_TTL_MS) continue;
    delete journal.pending[key];
    journal.lastGapSequence = journal.nextSequence;
    journal.nextSequence += 1;
  }
  const pendingEntries = Object.entries(journal.pending).sort(
    (left, right) => Date.parse(left[1].startedAt) - Date.parse(right[1].startedAt),
  );
  for (const [key] of pendingEntries.slice(0, -PENDING_TOOL_LIMIT)) {
    delete journal.pending[key];
    journal.lastGapSequence = journal.nextSequence;
    journal.nextSequence += 1;
  }
  if (journal.events.length > JOURNAL_LIMIT) {
    const removed = journal.events.splice(0, journal.events.length - JOURNAL_LIMIT);
    journal.floorSequence = removed.at(-1).sequence + 1;
  } else if (journal.events.length > 0) {
    journal.floorSequence = Math.min(
      journal.floorSequence,
      journal.events[0].sequence,
    );
  }
}

function withJournal(root, repositoryRoot, callback) {
  const path = journalPath(root, repositoryRoot);
  return withLock(path, () => {
    const journal = readJournal(root, repositoryRoot);
    pruneJournal(journal);
    const result = callback(journal);
    pruneJournal(journal);
    writeJournal(root, repositoryRoot, journal);
    return result;
  });
}

function factBookChanges(before, after) {
  const changes = [];
  for (const path of new Set([...Object.keys(before), ...Object.keys(after)])) {
    const beforeHash = before[path] ?? null;
    const afterHash = after[path] ?? null;
    if (beforeHash !== afterHash) changes.push({ path, beforeHash, afterHash });
  }
  return changes.sort((left, right) => left.path.localeCompare(right.path));
}

function readState(root, sessionId) {
  const state = readJson(statePath(root, sessionId), null);
  return state?.schemaVersion === SCHEMA_VERSION ? state : null;
}

function writeState(root, state) {
  state.updatedAt = new Date().toISOString();
  atomicWriteJson(statePath(root, state.sessionId), state);
}

function removeIfExists(path) {
  try {
    unlinkSync(path);
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
}

function readJsonLimited(path) {
  const descriptor = openSync(path, "r");
  try {
    const info = fstatSync(descriptor);
    if (!info.isFile()) throw new Error("Terminal envelope must be a regular file.");
    if (info.size > MAX_ENVELOPE_BYTES) {
      throw new Error("Terminal envelope exceeds the 64 KiB safety limit.");
    }
    const buffer = Buffer.allocUnsafe(MAX_ENVELOPE_BYTES + 1);
    let total = 0;
    for (;;) {
      const length = readSync(
        descriptor,
        buffer,
        total,
        buffer.length - total,
        null,
      );
      if (length === 0) break;
      total += length;
      if (total > MAX_ENVELOPE_BYTES) {
        throw new Error("Terminal envelope exceeds the 64 KiB safety limit.");
      }
    }
    return JSON.parse(buffer.subarray(0, total).toString("utf8"));
  } finally {
    closeSync(descriptor);
  }
}

function assertExactKeys(value, allowed, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${label} must be an object.`);
  }
  const unexpected = Object.keys(value).filter((key) => !allowed.has(key));
  if (unexpected.length > 0) {
    throw new Error(`${label} contains unsupported field ${unexpected[0]}.`);
  }
}

function assertSafeEnvelope(value, path = "$") {
  if (Array.isArray(value)) {
    value.forEach((entry, index) => assertSafeEnvelope(entry, `${path}[${index}]`));
    return;
  }
  if (value && typeof value === "object") {
    for (const [key, entry] of Object.entries(value)) {
      if (CREDENTIAL_KEY_PATTERN.test(key)) {
        throw new Error(`Terminal envelope contains a credential-like field at ${path}.${key}.`);
      }
      assertSafeEnvelope(entry, `${path}.${key}`);
    }
    return;
  }
  if (typeof value !== "string") return;
  const credentialPatterns = [
    /-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----/,
    /\bBearer\s+[A-Za-z0-9._~+/-]{8,}/i,
    /\bBasic\s+[A-Za-z0-9+/]{12,}={0,2}/i,
    /\b(?:password|passwd|pwd|secret|token|authorization|api[_-]?key|client[_-]?secret|private[_-]?key|access[_-]?key|account[_-]?key|signing[_-]?key|connection[_-]?string|credential|cookie)\s*[:=]\s*\S+/i,
    /\b(?:AKIA|ASIA)[A-Z0-9]{16}\b/,
    /\bgh[pousr]_[A-Za-z0-9]{20,}\b/,
    /\bgithub_pat_[A-Za-z0-9_]{20,}\b/,
    /\bglpat-[A-Za-z0-9_-]{20,}\b/,
    /\bnpm_[A-Za-z0-9]{20,}\b/,
    /\bpypi-[A-Za-z0-9_-]{20,}\b/,
    /\bsk-(?:proj-)?[A-Za-z0-9_-]{16,}\b/,
    /\bsk_(?:live|test)_[A-Za-z0-9]{16,}\b/,
    /\bxox[baprs]-[A-Za-z0-9-]{10,}\b/,
    /\bAIza[0-9A-Za-z_-]{30,}\b/,
    /\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b/,
    /https?:\/\/[^/\s:@]+:[^/\s@]+@/i,
  ];
  if (credentialPatterns.some((pattern) => pattern.test(value))) {
    throw new Error(`Terminal envelope contains a secret or credential at ${path}.`);
  }
  if (/(?:^|\r?\n)diff --git a\/.+ b\/.+/.test(value)) {
    throw new Error(`Terminal envelope contains a raw diff at ${path}.`);
  }
}

function listStates(root) {
  const directory = join(root, "states");
  if (!existsSync(directory)) return [];
  return readdirSync(directory)
    .filter((name) => name.endsWith(".json"))
    .map((name) => readJson(join(directory, name), null))
    .filter((state) => state?.schemaVersion === SCHEMA_VERSION);
}

function pruneStorage(root) {
  const now = Date.now();
  const statesDirectory = join(root, "states");
  if (existsSync(statesDirectory)) {
    for (const name of readdirSync(statesDirectory)) {
      if (!name.endsWith(".json")) continue;
      const path = join(statesDirectory, name);
      const state = readJson(path, null);
      const updated = Date.parse(state?.updatedAt ?? "");
      if (!Number.isFinite(updated) || now - updated > STATE_TTL_MS) removeIfExists(path);
    }
  }
  const envelopesDirectory = join(root, "envelopes");
  if (!existsSync(envelopesDirectory)) return;
  for (const sessionDirectory of readdirSync(envelopesDirectory, { withFileTypes: true })) {
    if (!sessionDirectory.isDirectory()) continue;
    const directory = join(envelopesDirectory, sessionDirectory.name);
    for (const name of readdirSync(directory)) {
      const path = join(directory, name);
      try {
        if (now - statSync(path).mtimeMs > ENVELOPE_TTL_MS) removeIfExists(path);
      } catch {
        // A concurrent cleanup may already have removed the envelope.
      }
    }
    try {
      if (readdirSync(directory).length === 0) rmSync(directory, { recursive: false });
    } catch {
      // A concurrent writer may have populated the directory.
    }
  }
}

function selectState(root, sessionId, cwd = process.cwd()) {
  if (sessionId) {
    const state = readState(root, sessionId);
    if (!state) throw new Error(`No active terminal state for session ${sessionId}.`);
    return state;
  }
  let repositoryRoot = null;
  try {
    repositoryRoot = resolveRepositoryRoot(cwd);
  } catch {
    // Status can still select the sole state outside the repository.
  }
  const states = listStates(root).filter(
    (state) =>
      !repositoryRoot ||
      normalizePath(state.repositoryRoot) === normalizePath(repositoryRoot),
  );
  if (states.length === 0) throw new Error("No active terminal state was found.");
  if (states.length > 1) {
    throw new Error("Multiple terminal sessions are active; pass --session explicitly.");
  }
  return states[0];
}

function readStdinJson() {
  const raw = readFileSync(0, "utf8").trim();
  return raw ? JSON.parse(raw) : {};
}

function makeState({
  sessionId,
  turnKey,
  repositoryRoot,
  baselineFingerprint,
  baselineImplementationFingerprint,
  baselineFactBooks,
  baselineSequence,
}) {
  return {
    schemaVersion: SCHEMA_VERSION,
    sessionId,
    turnKey,
    repositoryRoot,
    baselineFingerprint,
    baselineImplementationFingerprint,
    baselineFactBooks,
    baselineSequence,
    receipt: null,
    pendingContinuation: false,
    protocolFailed: false,
    forceReceipt: false,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
}

function assertBeforeDeadline(deadline) {
  if (Date.now() > deadline) {
    throw new Error("Repository fingerprint exceeded the 120 second safety timeout.");
  }
}

function fingerprintGit(repositoryRoot, args, deadline, options = {}) {
  assertBeforeDeadline(deadline);
  return git(repositoryRoot, args, {
    ...options,
    timeout: Math.max(
      1,
      Math.min(GIT_TIMEOUT_MS, deadline - Date.now()),
    ),
  });
}

function hashFileInto(hash, path, deadline) {
  const descriptor = openSync(path, "r");
  const buffer = Buffer.allocUnsafe(FILE_HASH_BUFFER_BYTES);
  try {
    const before = fstatSync(descriptor);
    hash.update(`file\0${before.mode}\0${before.size}\0`);
    for (;;) {
      assertBeforeDeadline(deadline);
      const length = readSync(descriptor, buffer, 0, buffer.length, null);
      if (length === 0) break;
      hash.update(buffer.subarray(0, length));
    }
    const after = fstatSync(descriptor);
    if (before.size !== after.size || before.mtimeMs !== after.mtimeMs) {
      throw new Error(`Repository file changed while fingerprinting: ${path}`);
    }
  } finally {
    closeSync(descriptor);
  }
}

function hashWorkingPath(hash, repositoryRoot, relativePath, deadline, visitedRepositories) {
  const absolutePath = resolve(repositoryRoot, relativePath);
  const relativeToRoot = relative(repositoryRoot, absolutePath).replaceAll("\\", "/");
  if (
    relativeToRoot === ".." ||
    relativeToRoot.startsWith("../") ||
    resolve(absolutePath) === resolve(repositoryRoot)
  ) {
    throw new Error(`Unsafe repository path while fingerprinting: ${relativePath}`);
  }
  hash.update(`path\0${relativeToRoot}\0`);
  let info;
  try {
    info = lstatSync(absolutePath);
  } catch (error) {
    if (error?.code === "ENOENT") {
      hash.update("missing\0");
      return;
    }
    throw error;
  }
  if (info.isSymbolicLink()) {
    hash.update(`symlink\0${readlinkSync(absolutePath)}\0`);
    return;
  }
  if (info.isFile()) {
    hashFileInto(hash, absolutePath, deadline);
    return;
  }
  if (!info.isDirectory()) {
    hash.update(`special\0${info.mode}\0${info.size}\0`);
    return;
  }

  try {
    const nestedRoot = fingerprintGit(
      absolutePath,
      ["rev-parse", "--show-toplevel"],
      deadline,
    ).trim();
    if (normalizePath(nestedRoot) === normalizePath(absolutePath)) {
      hash.update("repository\0");
      hash.update(repositorySnapshot(absolutePath, { deadline, visitedRepositories }).fingerprint);
      return;
    }
  } catch {
    // An ordinary untracked directory is hashed below.
  }

  hash.update("directory\0");
  for (const entry of readdirSync(absolutePath, { withFileTypes: true })
    .filter((candidate) => candidate.name !== ".git")
    .sort((left, right) => left.name.localeCompare(right.name))) {
    hashWorkingPath(
      hash,
      repositoryRoot,
      join(relativePath, entry.name),
      deadline,
      visitedRepositories,
    );
  }
}

function statusPaths(statusBuffer) {
  const tokens = statusBuffer.toString("utf8").split("\0");
  const paths = new Set();
  for (let index = 0; index < tokens.length; index += 1) {
    const token = tokens[index];
    if (!token) continue;
    const code = token.slice(0, 2);
    const path = token.slice(3);
    if (path) paths.add(path);
    if (/[RC]/.test(code) && tokens[index + 1]) paths.add(tokens[++index]);
  }
  return paths;
}

function specialIndexPaths(indexBuffer) {
  const paths = new Set();
  for (const token of indexBuffer.toString("utf8").split("\0")) {
    if (!token) continue;
    const tag = token[0];
    if (tag === "S" || (tag >= "a" && tag <= "z")) {
      paths.add(token.slice(2));
    }
  }
  return paths;
}

function factBookFingerprints(repositoryRoot, deadline) {
  const factsRoot = join(repositoryRoot, "docs", "product-studio");
  const result = {};
  if (!existsSync(factsRoot)) return result;
  for (const product of readdirSync(factsRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .sort((left, right) => left.name.localeCompare(right.name))) {
    if (!isSafeProductId(product.name)) continue;
    for (const owner of OWNER_NAMES) {
      const path = join(factsRoot, product.name, `${owner}.md`);
      if (!existsSync(path) || !lstatSync(path).isFile()) continue;
      const hash = createHash("sha256");
      hashFileInto(hash, path, deadline);
      result[`docs/product-studio/${product.name}/${owner}.md`] = hash.digest("hex");
    }
  }
  return result;
}

function trackedFactBookPaths(repositoryRoot, deadline) {
  const paths = fingerprintGit(
    repositoryRoot,
    ["ls-files", "-z", "--", "docs/product-studio"],
    deadline,
    { encoding: "buffer" },
  )
    .toString("utf8")
    .split("\0")
    .filter(isOwnerFactBookPath);
  return new Set(paths);
}

function repositoryStateFingerprint(
  repositoryRoot,
  head,
  deadline,
  visitedRepositories,
  excludedPaths = [],
) {
  const exclusions = [...excludedPaths]
    .sort()
    .map((path) => `:(top,exclude,literal)${path}`);
  const scopedPathspec = exclusions.length > 0 ? ["--", ".", ...exclusions] : [];
  const status = fingerprintGit(
    repositoryRoot,
    [
      "status",
      "--porcelain=v1",
      "-z",
      "--untracked-files=all",
      "--ignore-submodules=none",
      ...scopedPathspec,
    ],
    deadline,
    { encoding: "buffer" },
  );
  const rawDiff =
    head === "UNBORN"
      ? Buffer.alloc(0)
      : fingerprintGit(
          repositoryRoot,
          [
            "diff",
            "--raw",
            "-z",
            "--no-ext-diff",
            "HEAD",
            "--",
            ...(exclusions.length > 0 ? [".", ...exclusions] : []),
          ],
          deadline,
          { encoding: "buffer" },
        );
  const indexEntries = fingerprintGit(
    repositoryRoot,
    ["ls-files", "-s", "-z", ...scopedPathspec],
    deadline,
    { encoding: "buffer" },
  );
  const indexFlags = fingerprintGit(
    repositoryRoot,
    ["ls-files", "-v", "-z", ...scopedPathspec],
    deadline,
    { encoding: "buffer" },
  );
  const paths = statusPaths(status);
  for (const path of specialIndexPaths(indexFlags)) paths.add(path);

  const hash = createHash("sha256");
  hash.update(`head\0${head}\0status\0`);
  hash.update(status);
  hash.update("diff\0");
  hash.update(rawDiff);
  hash.update("index-entries\0");
  hash.update(indexEntries);
  hash.update("index-flags\0");
  hash.update(indexFlags);
  for (const path of [...paths].sort()) {
    assertBeforeDeadline(deadline);
    hashWorkingPath(hash, repositoryRoot, path, deadline, visitedRepositories);
  }
  return hash.digest("hex");
}

function repositorySnapshot(repositoryRoot, options = {}) {
  const deadline = options.deadline ?? Date.now() + FINGERPRINT_TIMEOUT_MS;
  const visitedRepositories = options.visitedRepositories ?? new Set();
  const repositoryKey = normalizePath(repositoryRoot);
  if (visitedRepositories.has(repositoryKey)) {
    const fingerprint = sha256(`repository-cycle\0${repositoryKey}`);
    return { fingerprint, implementationFingerprint: fingerprint, factBooks: {} };
  }
  visitedRepositories.add(repositoryKey);
  try {
    assertBeforeDeadline(deadline);
    let head = "UNBORN";
    try {
      head = fingerprintGit(
        repositoryRoot,
        ["rev-parse", "--verify", "HEAD"],
        deadline,
      ).trim();
    } catch {
      // A newly initialized repository has an index and worktree but no HEAD yet.
    }
    const factBooks = factBookFingerprints(repositoryRoot, deadline);
    const excludedFactBooks = trackedFactBookPaths(repositoryRoot, deadline);
    for (const path of Object.keys(factBooks)) excludedFactBooks.add(path);
    const fingerprint = repositoryStateFingerprint(
      repositoryRoot,
      head,
      deadline,
      visitedRepositories,
    );
    const implementationFingerprint = repositoryStateFingerprint(
      repositoryRoot,
      head,
      deadline,
      visitedRepositories,
      excludedFactBooks,
    );
    return {
      fingerprint,
      implementationFingerprint,
      factBooks,
    };
  } finally {
    visitedRepositories.delete(repositoryKey);
  }
}

function parseObservedExitCode(response) {
  if (response && typeof response === "object") {
    if (
      response.cancelled === true ||
      response.canceled === true ||
      response.timedOut === true ||
      response.timed_out === true ||
      response.timeout === true ||
      response.success === false ||
      response.isError === true ||
      response.error != null ||
      /^(?:cancelled|canceled|timeout|timed_out|failed)$/i.test(
        String(response.status ?? ""),
      )
    ) {
      return null;
    }
    for (const key of ["exitCode", "exit_code"]) {
      if (Number.isInteger(response[key])) return response[key];
    }
  }
  const wrappers = [];
  if (typeof response === "string") wrappers.push(response);
  if (response && typeof response === "object") {
    for (const key of ["output", "content", "text"]) {
      if (typeof response[key] === "string") wrappers.push(response[key]);
    }
  }
  for (const wrapper of wrappers) {
    const match = wrapper.match(/^Exit code:\s*(-?\d+)\r?\nWall time:\s*[^\r\n]+(?:\r?\n|$)/);
    if (match) return Number.parseInt(match[1], 10);
  }
  return null;
}

function commandHash(toolInput) {
  return typeof toolInput?.command === "string" && toolInput.command.length > 0
    ? sha256(toolInput.command)
    : null;
}

function protocolControlKind(toolInput) {
  if (typeof toolInput?.command !== "string") return null;
  const command = toolInput.command.replaceAll("\\", "/").toLowerCase();
  const script = normalizePath(process.argv[1]);
  let offset = 0;
  for (;;) {
    const index = command.indexOf(script, offset);
    if (index < 0) return null;
    const tail = command.slice(index + script.length);
    const match = tail.match(/^["']?\s+(status|begin|record)(?=\s|$)/);
    if (match) return match[1];
    offset = index + script.length;
  }
}

function isValidationTool(toolName) {
  return ["Bash", "exec_command", "shell_command"].includes(toolName);
}

function activeStateForTool(root, input) {
  const state = readState(root, String(input.session_id ?? ""));
  if (!state || state.turnKey !== String(input.turn_id ?? "")) return null;
  const hookCwd = resolve(String(input.cwd ?? state.repositoryRoot));
  const declaredCwd =
    input.tool_input?.workdir ?? input.tool_input?.cwd ?? hookCwd;
  let toolRepositoryRoot;
  try {
    toolRepositoryRoot = resolveRepositoryRoot(
      resolve(hookCwd, String(declaredCwd)),
    );
  } catch {
    return null;
  }
  if (
    normalizePath(toolRepositoryRoot) !== normalizePath(state.repositoryRoot)
  ) {
    return null;
  }
  return state;
}

function recordToolPre(root, input, state) {
  const sessionId = state.sessionId;
  const turnKey = state.turnKey;
  const toolUseId = String(input.tool_use_id ?? "");
  const toolName = String(input.tool_name ?? "");
  if (!toolUseId || !toolName) return {};
  const inputDigest = toolInputDigest(input.tool_input);
  const key = pendingToolKey(sessionId, turnKey, toolUseId);
  withJournal(root, state.repositoryRoot, (journal) => {
    const completed = journal.events.find((event) => event.key === key);
    if (completed) {
      if (
        completed.inputDigest !== inputDigest ||
        completed.toolName !== toolName
      ) {
        completed.conflict = true;
      }
      return;
    }
    const existing = journal.pending[key];
    if (existing) {
      if (existing.inputDigest !== inputDigest || existing.toolName !== toolName) {
        existing.conflict = true;
      }
      return;
    }
    const before = repositorySnapshot(state.repositoryRoot);
    const otherPending = Object.values(journal.pending);
    for (const pending of otherPending) pending.concurrent = true;
    journal.pending[key] = {
      key,
      sessionId,
      turnKey,
      toolUseId,
      toolName,
      protocolControl: protocolControlKind(input.tool_input),
      inputDigest,
      commandHash: commandHash(input.tool_input),
      beforeFingerprint: before.fingerprint,
      beforeImplementationFingerprint: before.implementationFingerprint,
      beforeFactBooks: before.factBooks,
      concurrent: otherPending.length > 0,
      conflict: false,
      startedAt: new Date().toISOString(),
    };
  });
  return {};
}

function recordToolPost(root, input, state) {
  const sessionId = state.sessionId;
  const turnKey = state.turnKey;
  const toolUseId = String(input.tool_use_id ?? "");
  const toolName = String(input.tool_name ?? "");
  if (!toolUseId || !toolName) return {};
  const inputDigest = toolInputDigest(input.tool_input);
  const postCommandHash = commandHash(input.tool_input);
  const responseDigest = sha256(canonicalJson(input.tool_response) ?? "undefined");
  const key = pendingToolKey(sessionId, turnKey, toolUseId);
  withJournal(root, state.repositoryRoot, (journal) => {
    const completed = journal.events.find((event) => event.key === key);
    if (completed) {
      if (
        completed.inputDigest !== inputDigest ||
        completed.toolName !== toolName ||
        completed.responseDigest !== responseDigest
      ) {
        completed.conflict = true;
      }
      return;
    }
    const after = repositorySnapshot(state.repositoryRoot);
    const pending = journal.pending[key] ?? null;
    const otherPending = Object.values(journal.pending).filter(
      (candidate) => candidate.key !== key,
    );
    for (const candidate of otherPending) candidate.concurrent = true;
    const inputMatched =
      pending !== null &&
      pending.inputDigest === inputDigest &&
      pending.commandHash === postCommandHash &&
      pending.toolName === toolName;
    const event = {
      key,
      sequence: journal.nextSequence,
      sessionId,
      turnKey,
      toolUseId,
      toolName,
      protocolControl: pending?.protocolControl ?? protocolControlKind(input.tool_input),
      inputDigest,
      commandHash: postCommandHash,
      responseDigest,
      paired: pending !== null,
      inputMatched,
      observedExitCode: isValidationTool(toolName)
        ? parseObservedExitCode(input.tool_response)
        : null,
      beforeFingerprint: pending?.beforeFingerprint ?? null,
      afterFingerprint: after.fingerprint,
      beforeImplementationFingerprint:
        pending?.beforeImplementationFingerprint ?? null,
      afterImplementationFingerprint: after.implementationFingerprint,
      factBookChanges: pending
        ? factBookChanges(pending.beforeFactBooks, after.factBooks)
        : [],
      mutationObserved:
        pending !== null && pending.beforeFingerprint !== after.fingerprint,
      implementationMutationObserved:
        pending !== null &&
        pending.beforeImplementationFingerprint !== after.implementationFingerprint,
      concurrent:
        Boolean(pending?.concurrent) ||
        otherPending.length > 0,
      conflict: Boolean(pending?.conflict) || !inputMatched,
      completedAt: new Date().toISOString(),
    };
    journal.nextSequence += 1;
    journal.events.push(event);
    if (pending) delete journal.pending[key];
    else journal.lastGapSequence = event.sequence;
  });
  return {};
}

function handleToolEvent(root, input, phase) {
  const state = activeStateForTool(root, input);
  if (!state) return {};
  return phase === "pre"
    ? recordToolPre(root, input, state)
    : recordToolPost(root, input, state);
}

function analyzeTransition(state, current, journal) {
  const events = journal.events
    .filter((event) => event.sequence > state.baselineSequence)
    .sort((left, right) => left.sequence - right.sequence);
  const journalGap =
    state.baselineSequence < journal.floorSequence - 1 ||
    (journal.lastGapSequence ?? 0) > state.baselineSequence;
  let transitionExplained = !journalGap;
  let chain = state.baselineFingerprint;
  const seenFingerprints = new Set([chain]);
  let lastImplementationMutationSequence = state.baselineSequence;
  const mutationEvents = [];
  for (const event of events) {
    if (!event.mutationObserved) continue;
    mutationEvents.push(event);
    if (event.implementationMutationObserved ?? event.mutationObserved) {
      lastImplementationMutationSequence = Math.max(
        lastImplementationMutationSequence,
        event.sequence,
      );
    }
    if (!event.paired || !event.inputMatched || event.conflict) {
      transitionExplained = false;
      continue;
    }
    if (event.beforeFingerprint !== chain) {
      if (
        !event.concurrent ||
        !seenFingerprints.has(event.beforeFingerprint)
      ) {
        transitionExplained = false;
        continue;
      }
    }
    chain = event.afterFingerprint;
    seenFingerprints.add(chain);
  }
  if (chain !== current.fingerprint) transitionExplained = false;

  const currentFactChanges = factBookChanges(
    state.baselineFactBooks ?? {},
    current.factBooks,
  );
  const factSessions = new Map();
  const concurrentFacts = new Set();
  for (const event of mutationEvents) {
    for (const change of event.factBookChanges ?? []) {
      const sessions = factSessions.get(change.path) ?? new Set();
      sessions.add(`${event.sessionId}\0${event.turnKey}`);
      factSessions.set(change.path, sessions);
      if (event.concurrent) concurrentFacts.add(change.path);
    }
  }
  const ownKey = `${state.sessionId}\0${state.turnKey}`;
  const attributedFactBooks = [];
  const foreignFactBooks = [];
  const conflictedFactBooks = [];
  for (const change of currentFactChanges) {
    const sessions = factSessions.get(change.path) ?? new Set();
    if (sessions.size === 1 && sessions.has(ownKey) && !concurrentFacts.has(change.path)) {
      attributedFactBooks.push(change.path);
    } else if (sessions.size === 1 && !sessions.has(ownKey) && !concurrentFacts.has(change.path)) {
      foreignFactBooks.push(change.path);
    } else {
      conflictedFactBooks.push(change.path);
    }
  }
  const ownMutations = mutationEvents.filter(
    (event) => event.sessionId === state.sessionId && event.turnKey === state.turnKey,
  );
  const foreignMutations = mutationEvents.filter(
    (event) => event.sessionId !== state.sessionId || event.turnKey !== state.turnKey,
  );
  const hasConcurrency = mutationEvents.some((event) => event.concurrent);
  const validationEvidenceCandidates = events
    .filter(
      (event) =>
        event.sessionId === state.sessionId &&
        event.turnKey === state.turnKey &&
        isValidationTool(event.toolName) &&
        event.protocolControl == null &&
        event.paired &&
        event.inputMatched &&
        !event.concurrent &&
        !event.conflict &&
        Number.isInteger(event.observedExitCode) &&
        typeof event.commandHash === "string" &&
        event.sequence > lastImplementationMutationSequence &&
        (event.beforeImplementationFingerprint ?? event.beforeFingerprint) ===
          current.implementationFingerprint &&
        (event.afterImplementationFingerprint ?? event.afterFingerprint) ===
          current.implementationFingerprint,
    )
    .map((event) => ({
      toolUseId: event.toolUseId,
      inputDigest: event.inputDigest,
      commandHash: event.commandHash,
      observedExitCode: event.observedExitCode,
      sequence: event.sequence,
    }));
  const activeTools = Object.values(journal.pending).filter(
    (pending) =>
      pending.sessionId === state.sessionId &&
      pending.turnKey === state.turnKey,
  ).length;
  const activeRepositoryToolEntries = Object.values(journal.pending).map(
    (pending) => ({
      sessionId: pending.sessionId,
      turnKey: pending.turnKey,
      toolUseId: pending.toolUseId,
      toolName: pending.toolName,
      protocolControl: pending.protocolControl ?? null,
      concurrent: Boolean(pending.concurrent),
      conflict: Boolean(pending.conflict),
    }),
  );
  const activeRepositoryTools = activeRepositoryToolEntries.length;
  return {
    current,
    journalRevision: journal.revision,
    journalFloorSequence: journal.floorSequence,
    journalGap,
    transitionExplained,
    mutationEvents,
    ownMutations,
    foreignMutations,
    attributedFactBooks,
    foreignFactBooks,
    conflictedFactBooks,
    hasConcurrency,
    validationEvidenceCandidates,
    activeTools,
    activeRepositoryTools,
    activeRepositoryToolEntries,
  };
}

function captureAnalysis(root, state) {
  const path = journalPath(root, state.repositoryRoot);
  return withLock(path, () => {
    const journal = readJournal(root, state.repositoryRoot);
    return analyzeTransition(state, repositorySnapshot(state.repositoryRoot), journal);
  });
}

function activeSessionCount(root, repositoryRoot) {
  const cutoff = Date.now() - STATE_TTL_MS;
  return listStates(root).filter(
    (state) =>
      normalizePath(state.repositoryRoot) === normalizePath(repositoryRoot) &&
      Date.parse(state.updatedAt) >= cutoff,
  ).length;
}

function statusPayload(root, state) {
  const analysis = captureAnalysis(root, state);
  const receiptRequired =
    state.forceReceipt ||
    analysis.ownMutations.length > 0 ||
    !analysis.transitionExplained ||
    analysis.activeRepositoryTools > 0;
  return {
    schemaVersion: SCHEMA_VERSION,
    sessionId: state.sessionId,
    turnKey: state.turnKey,
    repositoryRoot: state.repositoryRoot,
    baselineFingerprint: state.baselineFingerprint,
    currentFingerprint: analysis.current.fingerprint,
    pending: state.pendingContinuation,
    factMaintenance: state.forceReceipt,
    receiptRequired,
    receiptResult: state.receipt?.result ?? null,
    envelopePath: envelopePath(root, state.sessionId, state.turnKey),
    transitionExplained: analysis.transitionExplained,
    journalGap: analysis.journalGap,
    activeTools: analysis.activeTools,
    activeRepositoryTools: analysis.activeRepositoryTools,
    activeSessionCount: activeSessionCount(root, state.repositoryRoot),
    observedMutationCount: analysis.ownMutations.length,
    foreignMutationCount: analysis.foreignMutations.length,
    attributedFactBooks: analysis.attributedFactBooks,
    foreignFactBooks: analysis.foreignFactBooks,
    conflictedFactBooks: analysis.conflictedFactBooks,
    validationEvidenceCandidates: analysis.validationEvidenceCandidates,
  };
}

function handlePrompt(root, input) {
  pruneStorage(root);
  const sessionId = String(input.session_id ?? "");
  const turnKey = String(input.turn_id ?? "");
  if (!sessionId || !turnKey) {
    return {
      hookSpecificOutput: {
        hookEventName: "UserPromptSubmit",
        additionalContext:
          "Terminal-state protocol is unavailable because session_id or turn_id is missing.",
      },
    };
  }
  let repositoryRoot;
  try {
    repositoryRoot = resolveRepositoryRoot(input.cwd ?? process.cwd());
  } catch {
    return {
      hookSpecificOutput: {
        hookEventName: "UserPromptSubmit",
        additionalContext:
          "Terminal-state protocol is inactive because the current directory is not inside a Git repository.",
      },
    };
  }
  const previous = readState(root, sessionId);
  const continuation =
    previous &&
    previous.turnKey === turnKey &&
    normalizePath(previous.repositoryRoot) === normalizePath(repositoryRoot);
  let state = previous;
  if (!continuation) {
    const baseline = withJournal(root, repositoryRoot, (journal) => ({
      snapshot: repositorySnapshot(repositoryRoot),
      sequence: journal.nextSequence - 1,
    }));
    if (previous) removeIfExists(envelopePath(root, previous.sessionId, previous.turnKey));
    state = makeState({
      sessionId,
      turnKey,
      repositoryRoot,
      baselineFingerprint: baseline.snapshot.fingerprint,
      baselineImplementationFingerprint:
        baseline.snapshot.implementationFingerprint,
      baselineFactBooks: baseline.snapshot.factBooks,
      baselineSequence: baseline.sequence,
    });
  }
  writeState(root, state);
  const script = resolve(process.argv[1]);
  const statusCommand =
    `node "${script}" status --data-dir "${root}" --session "${sessionId}" --json`;
  const recordCommand =
    `node "${script}" record --data-dir "${root}" --session "${sessionId}" ` +
    `--envelope "${envelopePath(root, sessionId, turnKey)}" --json`;
  return {
    hookSpecificOutput: {
      hookEventName: "UserPromptSubmit",
      additionalContext:
        `Terminal-state protocol: inspect ${statusCommand}. ` +
        "After final observed validation, review every actually affected Owner: read the " +
        "memory ownership, index, common gates, actions, and safety rules; expand only hit " +
        "types and topics; revalidate authority; then update facts or declare NO_CHANGE. " +
        `Record with ${recordCommand}.`,
    },
  };
}

function handleStatus(root, args) {
  const state = selectState(root, String(args.session ?? ""));
  return statusPayload(root, state);
}

function handleBegin(root, args) {
  const state = selectState(root, String(args.session ?? ""));
  state.forceReceipt = true;
  state.protocolFailed = false;
  writeState(root, state);
  return statusPayload(root, state);
}

function requireNonEmptyString(value, label) {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new Error(`${label} must be a non-empty string.`);
  }
}

function validateEvidence(evidence, candidates, required) {
  if (!Array.isArray(evidence)) {
    throw new Error("validationEvidence must be an array.");
  }
  if (required && evidence.length === 0) {
    throw new Error("A successful terminal result requires observed validation evidence.");
  }
  const candidateById = new Map(
    candidates.map((candidate) => [candidate.toolUseId, candidate]),
  );
  const used = new Set();
  let finalSequence = 0;
  for (const [index, entry] of evidence.entries()) {
    const label = `validationEvidence[${index}]`;
    assertExactKeys(
      entry,
      new Set([
        "kind",
        "toolUseId",
        "inputDigest",
        "commandHash",
        "expectedExitCodes",
        "scope",
      ]),
      label,
    );
    requireNonEmptyString(entry.kind, `${label}.kind`);
    requireNonEmptyString(entry.toolUseId, `${label}.toolUseId`);
    requireNonEmptyString(entry.scope, `${label}.scope`);
    if (!/^[a-f0-9]{64}$/.test(entry.inputDigest ?? "")) {
      throw new Error(`${label}.inputDigest must be a SHA-256 digest.`);
    }
    if (!/^[a-f0-9]{64}$/.test(entry.commandHash ?? "")) {
      throw new Error(`${label}.commandHash must be a SHA-256 digest.`);
    }
    if (
      !Array.isArray(entry.expectedExitCodes) ||
      entry.expectedExitCodes.length === 0 ||
      entry.expectedExitCodes.some((code) => !Number.isInteger(code))
    ) {
      throw new Error(`${label}.expectedExitCodes must contain integers.`);
    }
    if (used.has(entry.toolUseId)) {
      throw new Error(`${label} reuses a toolUseId.`);
    }
    used.add(entry.toolUseId);
    const candidate = candidateById.get(entry.toolUseId);
    if (
      !candidate ||
      candidate.inputDigest !== entry.inputDigest ||
      candidate.commandHash !== entry.commandHash
    ) {
      throw new Error(`${label} is not bound to an observed completed command.`);
    }
    if (!entry.expectedExitCodes.includes(candidate.observedExitCode)) {
      throw new Error(`${label} observed exit code is not expected.`);
    }
    if (
      entry.kind !== "probe" &&
      (candidate.observedExitCode !== 0 ||
        entry.expectedExitCodes.length !== 1 ||
        entry.expectedExitCodes[0] !== 0)
    ) {
      throw new Error(`${label} requires exit code 0; nonzero semantics belong to probe evidence.`);
    }
    finalSequence = Math.max(finalSequence, candidate.sequence);
  }
  return finalSequence;
}

function validateOwners(checkedOwners) {
  if (!Array.isArray(checkedOwners)) {
    throw new Error("checkedOwners must be an array.");
  }
  const paths = new Set();
  const actions = [];
  for (const [ownerIndex, checked] of checkedOwners.entries()) {
    const label = `checkedOwners[${ownerIndex}]`;
    assertExactKeys(
      checked,
      new Set([
        "productId",
        "owner",
        "factBookPath",
        "checkedScope",
        "actions",
      ]),
      label,
    );
    if (!/^[A-Za-z0-9._-]+$/.test(checked.productId ?? "")) {
      throw new Error(`${label}.productId must be a safe single directory name.`);
    }
    if (!OWNER_NAMES.has(checked.owner)) {
      throw new Error(`${label}.owner is not a Product Studio owner.`);
    }
    const expectedPath =
      `docs/product-studio/${checked.productId}/${checked.owner}.md`;
    if (checked.factBookPath !== expectedPath) {
      throw new Error(`${label}.factBookPath does not match productId and owner.`);
    }
    if (paths.has(expectedPath)) {
      throw new Error(`${label}.factBookPath is duplicated.`);
    }
    paths.add(expectedPath);
    if (
      !Array.isArray(checked.checkedScope) ||
      checked.checkedScope.length === 0 ||
      checked.checkedScope.some(
        (scope) => typeof scope !== "string" || scope.trim().length === 0,
      )
    ) {
      throw new Error(`${label}.checkedScope must contain non-empty scopes.`);
    }
    if (!Array.isArray(checked.actions)) {
      throw new Error(`${label}.actions must be an array.`);
    }
    for (const [actionIndex, action] of checked.actions.entries()) {
      const actionLabel = `${label}.actions[${actionIndex}]`;
      assertExactKeys(
        action,
        new Set(["action", "topic", "authoritativeEvidence"]),
        actionLabel,
      );
      if (!FACT_ACTIONS.has(action.action)) {
        throw new Error(`${actionLabel}.action is invalid.`);
      }
      requireNonEmptyString(action.topic, `${actionLabel}.topic`);
      if (
        !Array.isArray(action.authoritativeEvidence) ||
        action.authoritativeEvidence.length === 0 ||
        action.authoritativeEvidence.some(
          (item) => typeof item !== "string" || item.trim().length === 0,
        )
      ) {
        throw new Error(`${actionLabel}.authoritativeEvidence must not be empty.`);
      }
      actions.push({ ...action, factBookPath: expectedPath });
    }
  }
  return { paths, actions };
}

function sameStringSets(left, right) {
  return (
    left.size === right.size &&
    [...left].every((value) => right.has(value))
  );
}

function hasOnlyCurrentRecordTool(analysis, state) {
  if (analysis.activeRepositoryToolEntries.length !== 1) return false;
  const [active] = analysis.activeRepositoryToolEntries;
  return (
    active.sessionId === state.sessionId &&
    active.turnKey === state.turnKey &&
    active.protocolControl === "record" &&
    !active.concurrent &&
    !active.conflict
  );
}

function validateEnvelope(envelope, state, analysis) {
  assertSafeEnvelope(envelope);
  assertExactKeys(
    envelope,
    new Set([
      "schemaVersion",
      "repositoryRoot",
      "sessionId",
      "turnKey",
      "finalFingerprint",
      "validationEvidence",
      "checkedOwners",
      "result",
      "reason",
    ]),
    "terminal envelope",
  );
  if (envelope.schemaVersion !== SCHEMA_VERSION) {
    throw new Error(`Terminal envelope schemaVersion must be ${SCHEMA_VERSION}.`);
  }
  requireNonEmptyString(envelope.repositoryRoot, "repositoryRoot");
  requireNonEmptyString(envelope.sessionId, "sessionId");
  requireNonEmptyString(envelope.turnKey, "turnKey");
  if (!/^[a-f0-9]{64}$/.test(envelope.finalFingerprint ?? "")) {
    throw new Error("finalFingerprint must be a SHA-256 digest.");
  }
  if (
    normalizePath(envelope.repositoryRoot ?? "") !==
    normalizePath(state.repositoryRoot)
  ) {
    throw new Error("Terminal envelope repositoryRoot does not match the active state.");
  }
  if (envelope.sessionId !== state.sessionId || envelope.turnKey !== state.turnKey) {
    throw new Error("Terminal envelope session or turn does not match the active state.");
  }
  if (envelope.finalFingerprint !== analysis.current.fingerprint) {
    throw new Error("Terminal envelope finalFingerprint is stale.");
  }
  if (!RESULTS.has(envelope.result)) {
    throw new Error("Terminal envelope result is invalid.");
  }
  if (!analysis.transitionExplained) {
    throw new Error("Repository changes are not fully explained by paired Hook events.");
  }
  if (
    analysis.activeRepositoryTools > 0 &&
    !hasOnlyCurrentRecordTool(analysis, state)
  ) {
    throw new Error("A tool is still active in this repository.");
  }
  if (
    (analysis.hasConcurrency ||
      analysis.conflictedFactBooks.length > 0 ||
      analysis.foreignFactBooks.length > 0) &&
    !["DEFERRED", "BLOCKED"].includes(envelope.result)
  ) {
    throw new Error("Cross-session fact ownership is not current-session evidence; use DEFERRED or BLOCKED.");
  }
  if (["DEFERRED", "BLOCKED"].includes(envelope.result)) {
    requireNonEmptyString(envelope.reason, "reason");
  } else if ("reason" in envelope && String(envelope.reason).trim().length > 0) {
    throw new Error(`${envelope.result} must not include a reason.`);
  }

  const evidenceSequence = validateEvidence(
    envelope.validationEvidence,
    analysis.validationEvidenceCandidates,
    envelope.result !== "BLOCKED",
  );
  const owners = validateOwners(envelope.checkedOwners);
  const mutatingActions = owners.actions.filter((action) => action.action !== "NO_CHANGE");
  const noChangeActions = owners.actions.filter((action) => action.action === "NO_CHANGE");
  const attributed = new Set(analysis.attributedFactBooks);
  const claimedMutations = new Set(
    mutatingActions.map((action) => action.factBookPath),
  );

  if (envelope.result === "SYNCED") {
    if (mutatingActions.length === 0 || !sameStringSets(attributed, claimedMutations)) {
      throw new Error("SYNCED must bind every attributed changed fact book to a mutating action.");
    }
  } else if (envelope.result === "NO_CHANGE") {
    if (noChangeActions.length === 0 || mutatingActions.length > 0 || attributed.size > 0) {
      throw new Error("NO_CHANGE requires explicit NO_CHANGE actions and unchanged attributed facts.");
    }
  } else if (mutatingActions.length > 0 || attributed.size > 0) {
    throw new Error(`${envelope.result} cannot retain an attributed fact-book mutation.`);
  }

  return { evidenceSequence };
}

function handleRecord(root, args) {
  const state = selectState(root, String(args.session ?? ""));
  const expectedPath = envelopePath(root, state.sessionId, state.turnKey);
  const suppliedPath = resolve(String(args.envelope ?? ""));
  if (normalizePath(suppliedPath) !== normalizePath(expectedPath)) {
    throw new Error("Envelope path must equal status.envelopePath.");
  }
  try {
    const envelope = readJsonLimited(expectedPath);
    const analysis = captureAnalysis(root, state);
    const validated = validateEnvelope(envelope, state, analysis);
    state.receipt = {
      result: envelope.result,
      turnKey: state.turnKey,
      finalFingerprint: analysis.current.fingerprint,
      journalRevision: analysis.journalRevision,
      evidenceSequence: validated.evidenceSequence,
      mutationSequence: Math.max(
        state.baselineSequence,
        ...analysis.mutationEvents.map((event) => event.sequence),
      ),
      recordedAt: new Date().toISOString(),
    };
    state.pendingContinuation = false;
    state.protocolFailed = false;
    writeState(root, state);
    return {
      result: envelope.result,
      finalFingerprint: analysis.current.fingerprint,
    };
  } finally {
    removeIfExists(expectedPath);
  }
}

function handleStop(root, input) {
  const state = readState(root, String(input.session_id ?? ""));
  if (!state || state.turnKey !== String(input.turn_id ?? "")) {
    return {
      systemMessage:
        "Terminal-state protocol had no matching state for this session and turn; the current directory is not inside a Git repository or no prompt baseline was recorded.",
    };
  }
  const analysis = captureAnalysis(root, state);
  const mutationAfterReceipt =
    state.receipt &&
    analysis.mutationEvents.some(
      (event) => event.sequence > (state.receipt.mutationSequence ?? 0),
    );
  const validReceipt =
    state.receipt &&
    state.receipt.turnKey === state.turnKey &&
    state.receipt.finalFingerprint === analysis.current.fingerprint &&
    analysis.transitionExplained &&
    analysis.activeRepositoryTools === 0 &&
    !mutationAfterReceipt;
  if (validReceipt) return {};

  if (state.receipt) {
    state.receipt = null;
    writeState(root, state);
  }
  const receiptRequired =
    state.forceReceipt ||
    analysis.ownMutations.length > 0 ||
    !analysis.transitionExplained ||
    analysis.activeRepositoryTools > 0;
  if (!receiptRequired) {
    if (state.pendingContinuation || state.protocolFailed) {
      state.pendingContinuation = false;
      state.protocolFailed = false;
      writeState(root, state);
    }
    return {};
  }
  if (state.protocolFailed) {
    return {
      systemMessage:
        "Terminal-state protocol previously failed for this turn; no success receipt was recorded.",
    };
  }
  if (state.pendingContinuation || input.stop_hook_active === true) {
    state.pendingContinuation = false;
    state.protocolFailed = true;
    writeState(root, state);
    return {
      systemMessage:
        "Terminal-state protocol failed: the observed transition and terminal receipt remain incomplete.",
    };
  }
  state.pendingContinuation = true;
  writeState(root, state);
  const script = resolve(process.argv[1]);
  const statusCommand =
    `node "${script}" status --data-dir "${root}" --session "${state.sessionId}" --json`;
  const recordCommand =
    `node "${script}" record --data-dir "${root}" --session "${state.sessionId}" ` +
    `--envelope "${envelopePath(root, state.sessionId, state.turnKey)}" --json`;
  return {
    decision: "block",
    reason:
      "Terminal-state receipt is required. Review every actually affected Owner using its " +
      "memory index and admission gates, revalidate hit facts from authority, and update the " +
      "owner fact book or declare NO_CHANGE. Review observed evidence with " +
      `${statusCommand}, then record the final envelope with ${recordCommand}.`,
  };
}

function main() {
  const args = parseArguments(process.argv.slice(2));
  const root = dataRoot(args);
  let output;
  if (args.command === "status") output = handleStatus(root, args);
  else if (args.command === "begin") output = handleBegin(root, args);
  else if (args.command === "record") output = handleRecord(root, args);
  else {
    const input = readStdinJson();
    if (input.hook_event_name === "UserPromptSubmit") output = handlePrompt(root, input);
    else if (input.hook_event_name === "PreToolUse") output = handleToolEvent(root, input, "pre");
    else if (input.hook_event_name === "PostToolUse") output = handleToolEvent(root, input, "post");
    else if (input.hook_event_name === "Stop") output = handleStop(root, input);
    else output = {};
  }
  emit(output);
}

try {
  main();
} catch (error) {
  emit({ error: error instanceof Error ? error.message : String(error) });
  process.exitCode = 1;
}
