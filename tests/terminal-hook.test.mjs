import assert from "node:assert/strict";
import { execFileSync, spawn, spawnSync } from "node:child_process";
import {
  closeSync,
  existsSync,
  mkdtempSync,
  mkdirSync,
  openSync,
  readFileSync,
  readdirSync,
  rmSync,
  utimesSync,
  writeSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const TEST_DIR = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(TEST_DIR, "..");
const HOOK_SCRIPT = join(PROJECT_ROOT, "scripts", "terminal-hook.mjs");
const ENVELOPE_FIXTURE = join(TEST_DIR, "fixtures", "terminal-envelope.json");

function git(cwd, ...args) {
  return execFileSync("git", args, { cwd, encoding: "utf8" }).trim();
}

function createRepository(t) {
  const root = mkdtempSync(join(tmpdir(), "product-studio-hook-"));
  const pluginData = mkdtempSync(join(tmpdir(), "product-studio-hook-data-"));
  mkdirSync(join(root, "src"));
  mkdirSync(join(root, "docs", "product-studio", "demo"), { recursive: true });
  writeFileSync(join(root, "src", "app.txt"), "baseline\n");
  writeFileSync(
    join(root, "docs", "product-studio", "demo", "backend-engineering.md"),
    "# backend-engineering current product facts\n",
  );
  git(root, "init", "--quiet");
  git(root, "config", "user.email", "hook-test@example.invalid");
  git(root, "config", "user.name", "Hook Test");
  git(root, "config", "core.autocrlf", "false");
  git(root, "add", ".");
  git(root, "commit", "--quiet", "-m", "baseline");
  t.after(() => rmSync(root, { recursive: true, force: true }));
  t.after(() => rmSync(pluginData, { recursive: true, force: true }));
  return { root, pluginData };
}

function createUnbornRepository(t) {
  const root = mkdtempSync(join(tmpdir(), "product-studio-hook-unborn-"));
  const pluginData = mkdtempSync(join(tmpdir(), "product-studio-hook-data-"));
  mkdirSync(join(root, "src"));
  writeFileSync(join(root, "src", "app.txt"), "baseline\n");
  git(root, "init", "--quiet");
  git(root, "add", ".");
  t.after(() => rmSync(root, { recursive: true, force: true }));
  t.after(() => rmSync(pluginData, { recursive: true, force: true }));
  return { root, pluginData };
}

function addSubmodule(repo, t) {
  const source = mkdtempSync(join(tmpdir(), "product-studio-submodule-"));
  writeFileSync(join(source, "nested.txt"), "baseline\n");
  git(source, "init", "--quiet");
  git(source, "config", "user.email", "hook-test@example.invalid");
  git(source, "config", "user.name", "Hook Test");
  git(source, "config", "core.autocrlf", "false");
  git(source, "add", ".");
  git(source, "commit", "--quiet", "-m", "baseline");
  git(
    repo.root,
    "-c",
    "protocol.file.allow=always",
    "submodule",
    "add",
    "--quiet",
    source,
    "vendor/nested",
  );
  git(repo.root, "commit", "--quiet", "-am", "add nested repository");
  t.after(() => rmSync(source, { recursive: true, force: true }));
  return join(repo.root, "vendor", "nested", "nested.txt");
}

function runHook({ root, pluginData }, input, args = []) {
  const result = spawnSync(process.execPath, [HOOK_SCRIPT, ...args], {
    cwd: root,
    env: {
      ...process.env,
      CLAUDE_PLUGIN_DATA: pluginData,
      PLUGIN_DATA: pluginData,
    },
    input: input === undefined ? undefined : JSON.stringify(input),
    encoding: "utf8",
  });
  assert.equal(
    result.status,
    0,
    `terminal hook failed\nstdout: ${result.stdout}\nstderr: ${result.stderr}`,
  );
  const output = result.stdout.trim();
  return output ? JSON.parse(output) : {};
}

function runHookAsync({ root, pluginData }, input, args = []) {
  return new Promise((resolvePromise, rejectPromise) => {
    const child = spawn(process.execPath, [HOOK_SCRIPT, ...args], {
      cwd: root,
      env: {
        ...process.env,
        CLAUDE_PLUGIN_DATA: pluginData,
        PLUGIN_DATA: pluginData,
      },
      stdio: ["pipe", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk) => {
      stdout += chunk;
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk;
    });
    child.on("error", rejectPromise);
    child.on("close", (code) => {
      if (code !== 0) {
        rejectPromise(
          new Error(`terminal hook failed\nstdout: ${stdout}\nstderr: ${stderr}`),
        );
        return;
      }
      const output = stdout.trim();
      resolvePromise(output ? JSON.parse(output) : {});
    });
    child.stdin.end(input === undefined ? undefined : JSON.stringify(input));
  });
}

function spawnCliWithoutPluginEnvironment({ root }, args) {
  const env = { ...process.env };
  delete env.PLUGIN_DATA;
  delete env.CLAUDE_PLUGIN_DATA;
  delete env.PRODUCT_STUDIO_DATA;
  return spawnSync(process.execPath, [HOOK_SCRIPT, ...args], {
    cwd: root,
    env,
    encoding: "utf8",
  });
}

function runCliWithoutPluginEnvironment(repo, args) {
  const result = spawnCliWithoutPluginEnvironment(repo, args);
  assert.equal(
    result.status,
    0,
    `terminal CLI failed\nstdout: ${result.stdout}\nstderr: ${result.stderr}`,
  );
  const output = result.stdout.trim();
  return output ? JSON.parse(output) : {};
}

function event(repo, hookEventName, overrides = {}) {
  return {
    session_id: "session-1",
    turn_id: "turn-1",
    cwd: repo.root,
    hook_event_name: hookEventName,
    permission_mode: "default",
    ...overrides,
  };
}

function submitPrompt(repo, overrides = {}) {
  return runHook(
    repo,
    event(repo, "UserPromptSubmit", {
      prompt: "Implement the requested change.",
      ...overrides,
    }),
  );
}

function stop(repo, overrides = {}) {
  return runHook(
    repo,
    event(repo, "Stop", {
      stop_hook_active: false,
      last_assistant_message: "Implementation complete.",
      ...overrides,
    }),
  );
}

function preTool(repo, toolUseId, toolInput, overrides = {}) {
  return runHook(
    repo,
    event(repo, "PreToolUse", {
      tool_use_id: toolUseId,
      tool_name: "Bash",
      tool_input: toolInput,
      ...overrides,
    }),
  );
}

function postTool(repo, toolUseId, toolInput, toolResponse, overrides = {}) {
  return runHook(
    repo,
    event(repo, "PostToolUse", {
      tool_use_id: toolUseId,
      tool_name: "Bash",
      tool_input: toolInput,
      tool_response: toolResponse,
      ...overrides,
    }),
  );
}

function observeTool(
  repo,
  toolUseId,
  toolInput,
  action = () => {},
  toolResponse = { exitCode: 0 },
  overrides = {},
) {
  preTool(repo, toolUseId, toolInput, overrides);
  action();
  return postTool(repo, toolUseId, toolInput, toolResponse, overrides);
}

function observeValidation(repo, toolUseId = "tool-validate", overrides = {}) {
  return observeTool(
    repo,
    toolUseId,
    { command: "node --test", workdir: repo.root },
    () => {},
    { exitCode: 0 },
    overrides,
  );
}

function controlInvocation(
  repo,
  kind,
  { sessionId = "session-1", envelopePath, toolUseId = `tool-${kind}` } = {},
) {
  const args = [
    kind,
    "--data-dir",
    repo.pluginData,
    "--session",
    sessionId,
  ];
  if (kind === "record") args.push("--envelope", envelopePath);
  args.push("--json");
  return {
    toolUseId,
    args,
    toolInput: {
      command:
        `node "${HOOK_SCRIPT}" ${kind} --data-dir "${repo.pluginData}" ` +
        `--session "${sessionId}"` +
        (kind === "record" ? ` --envelope "${envelopePath}"` : "") +
        " --json",
      workdir: repo.root,
    },
  };
}

function runObservedControl(repo, kind, options = {}) {
  const invocation = controlInvocation(repo, kind, options);
  preTool(repo, invocation.toolUseId, invocation.toolInput, {
    tool_name: "shell_command",
  });
  const result = spawnCliWithoutPluginEnvironment(repo, invocation.args);
  postTool(
    repo,
    invocation.toolUseId,
    invocation.toolInput,
    {
      exitCode: result.status,
      output: result.stdout,
      ...(result.status === 0 ? {} : { isError: true }),
    },
    { tool_name: "shell_command" },
  );
  return {
    result,
    output: result.stdout.trim() ? JSON.parse(result.stdout) : {},
  };
}

function status(repo, sessionId) {
  const sessionArgs = sessionId ? ["--session", sessionId] : [];
  return runHook(repo, undefined, ["status", ...sessionArgs, "--json"]);
}

function begin(repo, sessionId) {
  const sessionArgs = sessionId ? ["--session", sessionId] : [];
  return runHook(repo, undefined, ["begin", ...sessionArgs, "--json"]);
}

function isBlocked(output) {
  return output.decision === "block";
}

function writeEnvelope(repo, overrides = {}) {
  const template = JSON.parse(readFileSync(ENVELOPE_FIXTURE, "utf8"));
  const sessionId = overrides.sessionId ?? template.sessionId;
  const current = status(repo, sessionId);
  const candidate = current.validationEvidenceCandidates.at(-1);
  const validationEvidence =
    overrides.validationEvidence ??
    template.validationEvidence.map((entry) => ({
      ...entry,
      toolUseId: candidate?.toolUseId ?? entry.toolUseId,
      inputDigest: candidate?.inputDigest ?? entry.inputDigest,
      commandHash: candidate?.commandHash ?? entry.commandHash,
    }));
  const envelope = {
    ...template,
    repositoryRoot: repo.root,
    sessionId,
    turnKey: current.turnKey,
    finalFingerprint: current.currentFingerprint,
    validationEvidence,
    ...overrides,
  };
  const path = current.envelopePath;
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(envelope, null, 2)}\n`);
  return path;
}

function recordEnvelope(repo, envelopePath) {
  const envelope = JSON.parse(readFileSync(envelopePath, "utf8"));
  return runHook(repo, undefined, [
    "record",
    "--session",
    envelope.sessionId,
    "--envelope",
    envelopePath,
    "--json",
  ]);
}

test("UserPromptSubmit records the current repository baseline", (t) => {
  const repo = createRepository(t);

  const output = submitPrompt(repo);

  const state = status(repo);
  assert.equal(state.turnKey, "turn-1");
  assert.equal(state.baselineFingerprint, state.currentFingerprint);
  assert.equal(state.pending, false);
  assert.match(
    output.hookSpecificOutput?.additionalContext ?? "",
    /--data-dir.+--session/s,
  );
});

test("repository fingerprints support a branch without an initial commit", (t) => {
  const repo = createUnbornRepository(t);
  submitPrompt(repo);
  assert.deepEqual(stop(repo), {});

  observeTool(
    repo,
    "tool-unborn-edit",
    { command: "update src/app.txt", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "changed\n"),
  );
  assert.equal(isBlocked(stop(repo)), true);
});

test("PreToolUse and PostToolUse bind mutations and validation to observed commands", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  const mutationInput = { command: "change app", workdir: repo.root };
  preTool(repo, "tool-mutate", mutationInput);
  writeFileSync(join(repo.root, "src", "app.txt"), "changed\n");
  postTool(repo, "tool-mutate", mutationInput, {
    exitCode: 0,
  });

  const validationInput = { command: "node --test", workdir: repo.root };
  preTool(repo, "tool-validate", validationInput);
  postTool(repo, "tool-validate", validationInput, {
    exitCode: 0,
  });

  const current = status(repo);
  assert.equal(current.transitionExplained, true);
  assert.equal(current.observedMutationCount, 1);
  assert.equal(current.validationEvidenceCandidates.length, 1);
  assert.equal(
    current.validationEvidenceCandidates[0].toolUseId,
    "tool-validate",
  );
  assert.match(current.validationEvidenceCandidates[0].inputDigest, /^[a-f0-9]{64}$/);
  assert.match(current.validationEvidenceCandidates[0].commandHash, /^[a-f0-9]{64}$/);
});

test("only structured or anchored Bash completion yields validation evidence", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  const cases = [
    ["structured", { exitCode: 0 }],
    ["anchored", "Exit code: 7\nWall time: 0.2 seconds\nOutput:\nprobe miss"],
    ["spoofed", { output: "stdout says Exit code: 0\nWall time: forged" }],
    ["timeout", { timedOut: true, exitCode: 0 }],
    ["cancelled", { cancelled: true, exitCode: 0 }],
    ["unparsed", { output: "Exit code: 0\ncommand output only" }],
  ];
  for (const [toolUseId, response] of cases) {
    const input = { command: `check ${toolUseId}`, workdir: repo.root };
    preTool(repo, toolUseId, input);
    postTool(repo, toolUseId, input, response);
  }

  assert.deepEqual(
    status(repo).validationEvidenceCandidates.map((candidate) => candidate.toolUseId),
    ["structured", "anchored"],
  );
});

test("shell_command completion yields validation evidence", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  const input = { command: "node --test", workdir: repo.root };
  preTool(repo, "shell-validate", input, { tool_name: "shell_command" });
  postTool(repo, "shell-validate", input, { exitCode: 0 }, {
    tool_name: "shell_command",
  });

  assert.deepEqual(
    status(repo).validationEvidenceCandidates.map((candidate) => candidate.toolUseId),
    ["shell-validate"],
  );
});

test("a command declared for another repository is not validation evidence", (t) => {
  const repo = createRepository(t);
  const other = createRepository(t);
  submitPrompt(repo);
  const input = { command: "node --test", workdir: other.root };
  preTool(repo, "tool-other-repo", input);
  postTool(repo, "tool-other-repo", input, { exitCode: 0 });

  assert.deepEqual(status(repo).validationEvidenceCandidates, []);
});

test("apply_patch mutations are observed but never become validation evidence", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  const input = { patch: "*** Begin Patch\n*** End Patch" };
  preTool(repo, "patch-1", input, { tool_name: "apply_patch" });
  writeFileSync(join(repo.root, "src", "app.txt"), "patched\n");
  postTool(repo, "patch-1", input, "Success. Updated the following files.", {
    tool_name: "apply_patch",
  });

  const current = status(repo);
  assert.equal(current.transitionExplained, true);
  assert.equal(current.observedMutationCount, 1);
  assert.deepEqual(current.validationEvidenceCandidates, []);
});

test("protocol controls never become validation evidence and observed record can close", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-mutate",
    { command: "change app", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "changed\n"),
  );

  for (const kind of ["status", "begin"]) {
    const control = runObservedControl(repo, kind);
    assert.equal(control.result.status, 0);
  }
  assert.deepEqual(status(repo).validationEvidenceCandidates, []);

  observeValidation(repo);
  const envelopePath = writeEnvelope(repo);
  const recorded = runObservedControl(repo, "record", { envelopePath });
  assert.equal(recorded.result.status, 0);
  assert.equal(recorded.output.result, "NO_CHANGE");
  assert.deepEqual(
    status(repo).validationEvidenceCandidates.map((candidate) => candidate.toolUseId),
    ["tool-validate"],
  );
  assert.equal(isBlocked(stop(repo)), false);
});

test("record rejects an observed record command while another repository tool is active", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-mutate",
    { command: "change app", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "changed\n"),
  );
  observeValidation(repo);
  const envelopePath = writeEnvelope(repo);
  const activeInput = { command: "long running command", workdir: repo.root };
  preTool(repo, "tool-active", activeInput, { tool_name: "shell_command" });
  const record = controlInvocation(repo, "record", {
    envelopePath,
    toolUseId: "tool-record",
  });
  preTool(repo, record.toolUseId, record.toolInput, {
    tool_name: "shell_command",
  });

  const rejected = spawnCliWithoutPluginEnvironment(repo, record.args);

  assert.notEqual(rejected.status, 0);
  assert.match(rejected.stdout, /tool is still active/i);
  postTool(
    repo,
    record.toolUseId,
    record.toolInput,
    { exitCode: rejected.status, output: rejected.stdout, isError: true },
    { tool_name: "shell_command" },
  );
  postTool(repo, "tool-active", activeInput, { exitCode: 0 }, {
    tool_name: "shell_command",
  });
});

test("record rejects multiple active observed record commands", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-mutate",
    { command: "change app", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "changed\n"),
  );
  observeValidation(repo);
  const envelopePath = writeEnvelope(repo);
  const first = controlInvocation(repo, "record", {
    envelopePath,
    toolUseId: "tool-record-1",
  });
  const second = controlInvocation(repo, "record", {
    envelopePath,
    toolUseId: "tool-record-2",
  });
  preTool(repo, first.toolUseId, first.toolInput, {
    tool_name: "shell_command",
  });
  preTool(repo, second.toolUseId, second.toolInput, {
    tool_name: "shell_command",
  });

  const rejected = spawnCliWithoutPluginEnvironment(repo, first.args);

  assert.notEqual(rejected.status, 0);
  assert.match(rejected.stdout, /tool is still active/i);
  for (const invocation of [first, second]) {
    postTool(
      repo,
      invocation.toolUseId,
      invocation.toolInput,
      { exitCode: rejected.status, output: rejected.stdout, isError: true },
      { tool_name: "shell_command" },
    );
  }
});

test("mismatched PostToolUse input cannot explain or validate a mutation", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  const beforeInput = { command: "first command", workdir: repo.root };
  const afterInput = { command: "different command", workdir: repo.root };
  preTool(repo, "tool-mismatch", beforeInput);
  writeFileSync(join(repo.root, "src", "app.txt"), "changed\n");
  postTool(repo, "tool-mismatch", afterInput, { exitCode: 0 });

  const current = status(repo);
  assert.equal(current.transitionExplained, false);
  assert.deepEqual(current.validationEvidenceCandidates, []);
  const path = writeEnvelope(repo, {
    result: "DEFERRED",
    reason: "ownership remains unknown",
    checkedOwners: [],
    validationEvidence: [],
  });
  const rejected = spawnSync(
    process.execPath,
    [HOOK_SCRIPT, "record", "--session", "session-1", "--envelope", path, "--json"],
    {
      cwd: repo.root,
      env: { ...process.env, PLUGIN_DATA: repo.pluginData },
      encoding: "utf8",
    },
  );
  assert.notEqual(rejected.status, 0);
  assert.match(rejected.stdout, /not fully explained|paired Hook events/i);
  assert.equal(existsSync(path), false);
});

test("PostToolUse without a matching PreToolUse is never evidence", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  writeFileSync(join(repo.root, "src", "app.txt"), "changed\n");
  postTool(
    repo,
    "tool-unpaired",
    { command: "unknown command", workdir: repo.root },
    { exitCode: 0 },
  );

  const current = status(repo);
  assert.equal(current.transitionExplained, false);
  assert.deepEqual(current.validationEvidenceCandidates, []);
});

test("Stop allows a read-only turn with an unchanged repository", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);

  const output = stop(repo);

  assert.equal(isBlocked(output), false);
});

test("Stop blocks a changed repository when no receipt exists", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  writeFileSync(join(repo.root, "src", "app.txt"), "changed\n");

  const output = stop(repo);

  assert.equal(isBlocked(output), true);
  assert.match(output.reason, /terminal|receipt|fact|owner/i);
  assert.match(output.reason, /memory.+admission.+authority/is);
  assert.match(output.reason, /--data-dir.+--session/s);
});

test("Stop allows a changed repository with a matching receipt", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-mutate",
    { command: "change app", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "changed\n"),
  );
  observeValidation(repo);
  const envelopePath = writeEnvelope(repo);
  const receipt = recordEnvelope(repo, envelopePath);

  assert.equal(receipt.result, "NO_CHANGE");
  assert.equal(isBlocked(stop(repo)), false);
  assert.equal(status(repo, "session-1").receiptResult, "NO_CHANGE");
  const persistedState = readFileSync(
    join(repo.pluginData, "states", readdirSync(join(repo.pluginData, "states"))[0]),
    "utf8",
  );
  assert.doesNotMatch(persistedState, /validationEvidence|checkedOwners|node --test/);
});

test("ordinary tool shells can use explicit data and session coordinates", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-mutate",
    { command: "change app", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "changed\n"),
  );
  observeValidation(repo);

  const current = runCliWithoutPluginEnvironment(repo, [
    "status",
    "--data-dir",
    repo.pluginData,
    "--session",
    "session-1",
    "--json",
  ]);
  assert.equal(current.sessionId, "session-1");

  const receipt = runCliWithoutPluginEnvironment(repo, [
    "record",
    "--data-dir",
    repo.pluginData,
    "--session",
    "session-1",
    "--envelope",
    writeEnvelope(repo),
    "--json",
  ]);
  assert.equal(receipt.result, "NO_CHANGE");
  assert.equal(isBlocked(stop(repo)), false);
});

test("Stop rejects a receipt after the repository fingerprint changes", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-mutate",
    { command: "change app", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "first change\n"),
  );
  observeValidation(repo);
  recordEnvelope(repo, writeEnvelope(repo));
  writeFileSync(join(repo.root, "src", "app.txt"), "later change\n");

  const output = stop(repo);

  assert.equal(isBlocked(output), true);
  assert.match(output.reason, /stale|fingerprint|receipt|changed/i);
});

test("a continuation UserPromptSubmit preserves the original baseline", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  const originalBaseline = status(repo).baselineFingerprint;
  writeFileSync(join(repo.root, "src", "app.txt"), "changed\n");
  assert.equal(isBlocked(stop(repo)), true);

  submitPrompt(repo, { prompt: "Complete the terminal protocol." });

  const continuedState = status(repo);
  assert.equal(continuedState.pending, true);
  assert.equal(continuedState.baselineFingerprint, originalBaseline);
  writeFileSync(join(repo.root, "src", "app.txt"), "baseline\n");
  assert.equal(isBlocked(stop(repo)), false);
});

test("a new turn_id never inherits an old pending continuation", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  writeFileSync(join(repo.root, "src", "app.txt"), "changed\n");
  assert.equal(isBlocked(stop(repo)), true);
  assert.equal(status(repo).pending, true);

  submitPrompt(repo, {
    turn_id: "turn-2",
    prompt: "Begin an unrelated turn.",
  });

  const next = status(repo);
  assert.equal(next.turnKey, "turn-2");
  assert.equal(next.pending, false);
  assert.equal(next.receiptResult, null);
  assert.equal(next.baselineFingerprint, next.currentFingerprint);
  assert.equal(isBlocked(stop(repo, { turn_id: "turn-2" })), false);
});

for (const [name, flag] of [
  ["assume-unchanged", "--assume-unchanged"],
  ["skip-worktree", "--skip-worktree"],
]) {
  test(`repository fingerprints include ${name} content`, (t) => {
    const repo = createRepository(t);
    git(repo.root, "update-index", flag, "src/app.txt");
    submitPrompt(repo);
    writeFileSync(join(repo.root, "src", "app.txt"), `${name} changed\n`);

    const output = stop(repo);

    assert.equal(isBlocked(output), true);
    assert.equal(status(repo).transitionExplained, false);
  });
}

test("status rejects an ambiguous repository and selects an explicit session", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  const firstBaseline = status(repo, "session-1").baselineFingerprint;
  writeFileSync(join(repo.root, "src", "app.txt"), "changed between sessions\n");
  submitPrompt(repo, {
    session_id: "session-2",
    turn_id: "turn-2",
    prompt: "Inspect the same repository in another session.",
  });

  const ambiguous = spawnCliWithoutPluginEnvironment(repo, [
    "status",
    "--data-dir",
    repo.pluginData,
    "--json",
  ]);
  assert.notEqual(ambiguous.status, 0);
  assert.match(`${ambiguous.stdout}\n${ambiguous.stderr}`, /multiple|session/i);

  const first = runCliWithoutPluginEnvironment(repo, [
    "status",
    "--data-dir",
    repo.pluginData,
    "--session",
    "session-1",
    "--json",
  ]);
  const second = runCliWithoutPluginEnvironment(repo, [
    "status",
    "--data-dir",
    repo.pluginData,
    "--session",
    "session-2",
    "--json",
  ]);
  assert.equal(first.baselineFingerprint, firstBaseline);
  assert.notEqual(first.baselineFingerprint, second.baselineFingerprint);
  assert.equal(second.baselineFingerprint, second.currentFingerprint);
  assert.notEqual(first.envelopePath, second.envelopePath);
});

test("sequential foreign session mutations are explained but never attributed", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  submitPrompt(repo, {
    session_id: "session-2",
    turn_id: "turn-2",
    prompt: "Work in a second session.",
  });
  observeTool(
    repo,
    "tool-session-2",
    { command: "second session change", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "session two\n"),
    { exitCode: 0 },
    { session_id: "session-2", turn_id: "turn-2" },
  );

  const first = status(repo, "session-1");
  const second = status(repo, "session-2");
  assert.equal(first.transitionExplained, true);
  assert.equal(first.observedMutationCount, 0);
  assert.equal(first.foreignMutationCount, 1);
  assert.equal(second.observedMutationCount, 1);
  assert.equal(
    isBlocked(stop(repo, { session_id: "session-1", turn_id: "turn-1" })),
    false,
  );
});

test("a session cannot silently stop while another session tool is active", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  submitPrompt(repo, {
    session_id: "session-2",
    turn_id: "turn-2",
    prompt: "Work in a second session.",
  });
  const input = { command: "long running command", workdir: repo.root };
  preTool(repo, "tool-active", input, {
    session_id: "session-2",
    turn_id: "turn-2",
  });

  assert.equal(status(repo, "session-1").activeRepositoryTools, 1);
  assert.equal(
    isBlocked(stop(repo, { session_id: "session-1", turn_id: "turn-1" })),
    true,
  );

  postTool(repo, "tool-active", input, { exitCode: 0 }, {
    session_id: "session-2",
    turn_id: "turn-2",
  });
  assert.equal(
    isBlocked(stop(repo, { session_id: "session-1", turn_id: "turn-1" })),
    false,
  );
  assert.equal(status(repo, "session-1").pending, false);
});

test("overlapping processes conflict instead of losing or cross-attributing events", async (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  submitPrompt(repo, {
    session_id: "session-2",
    turn_id: "turn-2",
    prompt: "Work in a second session.",
  });
  const firstInput = { command: "first fact edit", workdir: repo.root };
  const secondInput = { command: "second fact edit", workdir: repo.root };
  await Promise.all([
    runHookAsync(
      repo,
      event(repo, "PreToolUse", {
        tool_use_id: "tool-session-1",
        tool_name: "Bash",
        tool_input: firstInput,
      }),
    ),
    runHookAsync(
      repo,
      event(repo, "PreToolUse", {
        session_id: "session-2",
        turn_id: "turn-2",
        tool_use_id: "tool-session-2",
        tool_name: "Bash",
        tool_input: secondInput,
      }),
    ),
  ]);
  writeFileSync(
    join(repo.root, "docs", "product-studio", "demo", "backend-engineering.md"),
    "# backend-engineering current product facts\n\n## concurrent fact\n",
  );
  await Promise.all([
    runHookAsync(
      repo,
      event(repo, "PostToolUse", {
        tool_use_id: "tool-session-1",
        tool_name: "Bash",
        tool_input: firstInput,
        tool_response: { exitCode: 0 },
      }),
    ),
    runHookAsync(
      repo,
      event(repo, "PostToolUse", {
        session_id: "session-2",
        turn_id: "turn-2",
        tool_use_id: "tool-session-2",
        tool_name: "Bash",
        tool_input: secondInput,
        tool_response: { exitCode: 0 },
      }),
    ),
  ]);

  const first = status(repo, "session-1");
  assert.equal(first.transitionExplained, true);
  assert.deepEqual(first.attributedFactBooks, []);
  assert.deepEqual(first.conflictedFactBooks, [
    "docs/product-studio/demo/backend-engineering.md",
  ]);
  observeValidation(repo, "tool-session-1-validate");
  const receipt = recordEnvelope(
    repo,
    writeEnvelope(repo, {
      result: "DEFERRED",
      reason: "overlapping sessions make fact ownership ambiguous",
      checkedOwners: [],
    }),
  );
  assert.equal(receipt.result, "DEFERRED");
  assert.equal(
    isBlocked(stop(repo, { session_id: "session-1", turn_id: "turn-1" })),
    false,
  );
});

test("record enforces declared expected exit codes", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-mutate",
    { command: "change app", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "changed\n"),
  );
  observeTool(
    repo,
    "tool-probe",
    { command: "domain-check --expect-absence", workdir: repo.root },
    () => {},
    { exitCode: 1 },
  );
  const candidate = status(repo).validationEvidenceCandidates.at(-1);
  const rejectedPath = writeEnvelope(repo, {
    validationEvidence: [
      {
        kind: "test",
        toolUseId: candidate.toolUseId,
        inputDigest: candidate.inputDigest,
        commandHash: candidate.commandHash,
        expectedExitCodes: [0],
        scope: "changed behavior",
      },
    ],
  });
  const rejected = spawnSync(
    process.execPath,
    [HOOK_SCRIPT, "record", "--session", "session-1", "--envelope", rejectedPath, "--json"],
    {
      cwd: repo.root,
      env: {
        ...process.env,
        CLAUDE_PLUGIN_DATA: repo.pluginData,
        PLUGIN_DATA: repo.pluginData,
      },
      encoding: "utf8",
    },
  );
  assert.notEqual(rejected.status, 0);
  assert.match(`${rejected.stdout}\n${rejected.stderr}`, /expected exit|evidence/i);
  assert.equal(existsSync(rejectedPath), false);

  const acceptedPath = writeEnvelope(repo, {
    validationEvidence: [
      {
        kind: "probe",
        toolUseId: candidate.toolUseId,
        inputDigest: candidate.inputDigest,
        commandHash: candidate.commandHash,
        expectedExitCodes: [1],
        scope: "expected absence contract",
      },
    ],
  });
  assert.equal(recordEnvelope(repo, acceptedPath).result, "NO_CHANGE");
});

test("record rejects self-reported commands and forged command digests", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeValidation(repo);
  const candidate = status(repo).validationEvidenceCandidates.at(-1);

  const selfReportedPath = writeEnvelope(repo, {
    validationEvidence: [
      {
        kind: "test",
        command: "node --test",
        exitCode: 0,
        expectedExitCodes: [0],
        scope: "claimed behavior",
      },
    ],
  });
  const selfReported = spawnSync(
    process.execPath,
    [HOOK_SCRIPT, "record", "--session", "session-1", "--envelope", selfReportedPath, "--json"],
    {
      cwd: repo.root,
      env: { ...process.env, PLUGIN_DATA: repo.pluginData },
      encoding: "utf8",
    },
  );
  assert.notEqual(selfReported.status, 0);
  assert.match(selfReported.stdout, /unsupported field|observed validation/i);
  assert.equal(existsSync(selfReportedPath), false);

  const forgedPath = writeEnvelope(repo, {
    validationEvidence: [
      {
        kind: "test",
        toolUseId: candidate.toolUseId,
        inputDigest: candidate.inputDigest,
        commandHash: "0".repeat(64),
        expectedExitCodes: [0],
        scope: "claimed behavior",
      },
    ],
  });
  const forged = spawnSync(
    process.execPath,
    [HOOK_SCRIPT, "record", "--session", "session-1", "--envelope", forgedPath, "--json"],
    {
      cwd: repo.root,
      env: { ...process.env, PLUGIN_DATA: repo.pluginData },
      encoding: "utf8",
    },
  );
  assert.notEqual(forged.status, 0);
  assert.match(forged.stdout, /not bound|observed completed command/i);
  assert.equal(existsSync(forgedPath), false);
});

test("validation evidence becomes stale after a later mutation", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeValidation(repo, "tool-early");
  const early = status(repo).validationEvidenceCandidates.at(-1);
  observeTool(
    repo,
    "tool-late-mutation",
    { command: "late mutation", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "late\n"),
  );
  assert.deepEqual(status(repo).validationEvidenceCandidates, []);

  const path = writeEnvelope(repo, {
    validationEvidence: [
      {
        kind: "test",
        toolUseId: early.toolUseId,
        inputDigest: early.inputDigest,
        commandHash: early.commandHash,
        expectedExitCodes: [0],
        scope: "stale behavior",
      },
    ],
  });
  const rejected = spawnSync(
    process.execPath,
    [HOOK_SCRIPT, "record", "--session", "session-1", "--envelope", path, "--json"],
    {
      cwd: repo.root,
      env: { ...process.env, PLUGIN_DATA: repo.pluginData },
      encoding: "utf8",
    },
  );
  assert.notEqual(rejected.status, 0);
  assert.match(rejected.stdout, /not bound|observed validation/i);
});

test("validated code can be followed by an owner fact-only update and observed record", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-code-mutation",
    { command: "change app", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "changed\n"),
  );
  observeValidation(repo, "tool-code-validation");
  const validation = status(repo).validationEvidenceCandidates.at(-1);

  observeTool(
    repo,
    "tool-fact-only-mutation",
    { patch: "*** Begin Patch\n*** Update File: docs/product-studio/demo/backend-engineering.md\n*** End Patch" },
    () =>
      writeFileSync(
        join(repo.root, "docs", "product-studio", "demo", "backend-engineering.md"),
        "# backend-engineering current product facts\n\n## stable behavior\n",
      ),
    "Success. Updated the following files.",
    { tool_name: "apply_patch" },
  );

  assert.deepEqual(
    status(repo).validationEvidenceCandidates.map((candidate) => candidate.toolUseId),
    [validation.toolUseId],
  );
  const envelopePath = writeEnvelope(repo, {
    result: "SYNCED",
    validationEvidence: [
      {
        kind: "test",
        toolUseId: validation.toolUseId,
        inputDigest: validation.inputDigest,
        commandHash: validation.commandHash,
        expectedExitCodes: [0],
        scope: "changed behavior",
      },
    ],
    checkedOwners: [
      {
        productId: "demo",
        owner: "backend-engineering",
        factBookPath: "docs/product-studio/demo/backend-engineering.md",
        checkedScope: ["changed server behavior"],
        actions: [
          {
            action: "UPDATE",
            topic: "stable behavior",
            authoritativeEvidence: ["src/app.txt"],
          },
        ],
      },
    ],
  });

  const recorded = runObservedControl(repo, "record", { envelopePath });

  assert.equal(recorded.result.status, 0);
  assert.equal(recorded.output.result, "SYNCED");
  assert.equal(isBlocked(stop(repo)), false);
});

test("validation evidence becomes stale after an illegal fact-like document changes", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-code-mutation",
    { command: "change app", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "changed\n"),
  );
  observeValidation(repo, "tool-code-validation");
  assert.equal(status(repo).validationEvidenceCandidates.length, 1);

  observeTool(
    repo,
    "tool-illegal-fact-like-mutation",
    { command: "write an unknown owner document", workdir: repo.root },
    () =>
      writeFileSync(
        join(repo.root, "docs", "product-studio", "demo", "not-an-owner.md"),
        "# unowned facts\n",
      ),
  );

  assert.deepEqual(status(repo).validationEvidenceCandidates, []);
});

test("Stop does not continue indefinitely when stop_hook_active is true", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  writeFileSync(join(repo.root, "src", "app.txt"), "changed\n");
  assert.equal(isBlocked(stop(repo)), true);

  const output = stop(repo, { stop_hook_active: true });

  assert.equal(isBlocked(output), false);
  assert.match(
    output.systemMessage ?? output.stopReason ?? "",
    /protocol|receipt|incomplete|failed/i,
  );
});

test("record rejects NO_CHANGE when an owner fact book changed", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-fact",
    { command: "change fact book", workdir: repo.root },
    () =>
      writeFileSync(
        join(repo.root, "docs", "product-studio", "demo", "backend-engineering.md"),
        "# backend-engineering current product facts\n\n## changed fact\n",
      ),
  );
  observeValidation(repo);
  const envelopePath = writeEnvelope(repo);

  const result = spawnSync(
    process.execPath,
    [HOOK_SCRIPT, "record", "--session", "session-1", "--envelope", envelopePath, "--json"],
    {
      cwd: repo.root,
      env: {
        ...process.env,
        CLAUDE_PLUGIN_DATA: repo.pluginData,
        PLUGIN_DATA: repo.pluginData,
      },
      encoding: "utf8",
    },
  );

  assert.notEqual(result.status, 0);
  assert.match(`${result.stdout}\n${result.stderr}`, /NO_CHANGE|fact|owner/i);
});

test("begin requires a receipt for an explicit fact-maintenance turn", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);

  const begun = begin(repo);
  assert.equal(begun.factMaintenance, true);
  assert.equal(isBlocked(stop(repo)), true);

  observeValidation(repo);
  recordEnvelope(repo, writeEnvelope(repo));
  assert.equal(isBlocked(stop(repo)), false);
});

test("record accepts SYNCED only when owner facts and actions changed", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-mutate",
    { command: "change app and fact", workdir: repo.root },
    () => {
      writeFileSync(join(repo.root, "src", "app.txt"), "changed\n");
      writeFileSync(
        join(repo.root, "docs", "product-studio", "demo", "backend-engineering.md"),
        "# backend-engineering current product facts\n\n## stable behavior\n",
      );
    },
  );
  observeValidation(repo);
  const checkedOwners = [
    {
      productId: "demo",
      owner: "backend-engineering",
      factBookPath: "docs/product-studio/demo/backend-engineering.md",
      checkedScope: ["changed server behavior"],
      actions: [
        {
          action: "UPDATE",
          topic: "stable behavior",
          authoritativeEvidence: ["src/app.txt"],
        },
      ],
    },
  ];

  const receipt = recordEnvelope(
    repo,
    writeEnvelope(repo, { result: "SYNCED", checkedOwners }),
  );

  assert.equal(receipt.result, "SYNCED");
  assert.equal(isBlocked(stop(repo)), false);
});

test("SYNCED binds every changed fact book to its exact product and owner", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-mutate",
    { command: "change app and fact", workdir: repo.root },
    () => {
      writeFileSync(join(repo.root, "src", "app.txt"), "changed\n");
      writeFileSync(
        join(repo.root, "docs", "product-studio", "demo", "backend-engineering.md"),
        "# backend-engineering current product facts\n\n## stable behavior\n",
      );
    },
  );
  observeValidation(repo);
  const wrongOwner = [
    {
      productId: "demo",
      owner: "quality-engineering",
      factBookPath: "docs/product-studio/demo/quality-engineering.md",
      checkedScope: ["changed server behavior"],
      actions: [
        {
          action: "UPDATE",
          topic: "stable behavior",
          authoritativeEvidence: ["src/app.txt"],
        },
      ],
    },
  ];
  const envelopePath = writeEnvelope(repo, {
    result: "SYNCED",
    checkedOwners: wrongOwner,
  });
  const rejected = spawnSync(
    process.execPath,
    [HOOK_SCRIPT, "record", "--session", "session-1", "--envelope", envelopePath, "--json"],
    {
      cwd: repo.root,
      env: {
        ...process.env,
        CLAUDE_PLUGIN_DATA: repo.pluginData,
        PLUGIN_DATA: repo.pluginData,
      },
      encoding: "utf8",
    },
  );
  assert.notEqual(rejected.status, 0);
  assert.match(`${rejected.stdout}\n${rejected.stderr}`, /fact book|owner|bytes|changed/i);
});

test("record accepts DEFERRED with unknown ownership for an explained transition", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-mutate",
    { command: "change an unclassified boundary", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "changed\n"),
  );
  observeValidation(repo);

  const receipt = recordEnvelope(
    repo,
    writeEnvelope(repo, {
      result: "DEFERRED",
      reason: "fact ownership remains unknown",
      checkedOwners: [],
    }),
  );

  assert.equal(receipt.result, "DEFERRED");
  assert.equal(isBlocked(stop(repo)), false);
});

test("DEFERRED requires observed validation while BLOCKED may omit it", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeTool(
    repo,
    "tool-mutate",
    { command: "change an unclassified boundary", workdir: repo.root },
    () => writeFileSync(join(repo.root, "src", "app.txt"), "changed\n"),
  );
  const deferredPath = writeEnvelope(repo, {
    result: "DEFERRED",
    reason: "fact ownership remains unknown",
    checkedOwners: [],
    validationEvidence: [],
  });
  const deferred = spawnSync(
    process.execPath,
    [HOOK_SCRIPT, "record", "--session", "session-1", "--envelope", deferredPath, "--json"],
    {
      cwd: repo.root,
      env: { ...process.env, PLUGIN_DATA: repo.pluginData },
      encoding: "utf8",
    },
  );
  assert.notEqual(deferred.status, 0);
  assert.match(deferred.stdout, /requires observed validation evidence/i);

  const receipt = recordEnvelope(
    repo,
    writeEnvelope(repo, {
      result: "BLOCKED",
      reason: "validation cannot run in the current environment",
      checkedOwners: [],
      validationEvidence: [],
    }),
  );
  assert.equal(receipt.result, "BLOCKED");
  assert.equal(isBlocked(stop(repo)), false);
});

test("record rejects credentials in a terminal envelope", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeValidation(repo);
  const envelopePath = writeEnvelope(repo, {
    validationEvidence: [
      {
        kind: "test",
        command: "token=not-a-real-token node --test",
        exitCode: 0,
        scope: "changed behavior",
      },
    ],
  });

  const result = spawnSync(
    process.execPath,
    [HOOK_SCRIPT, "record", "--session", "session-1", "--envelope", envelopePath, "--json"],
    {
      cwd: repo.root,
      env: {
        ...process.env,
        CLAUDE_PLUGIN_DATA: repo.pluginData,
        PLUGIN_DATA: repo.pluginData,
      },
      encoding: "utf8",
    },
  );

  assert.notEqual(result.status, 0);
  assert.match(`${result.stdout}\n${result.stderr}`, /secret|credential|token/i);
  assert.equal(existsSync(envelopePath), false);

  const unknownSecretPath = writeEnvelope(repo, {
    token: "sk-proj-examplevalue0123456789",
  });
  const unknownSecret = spawnSync(
    process.execPath,
    [HOOK_SCRIPT, "record", "--session", "session-1", "--envelope", unknownSecretPath, "--json"],
    {
      cwd: repo.root,
      env: {
        ...process.env,
        CLAUDE_PLUGIN_DATA: repo.pluginData,
        PLUGIN_DATA: repo.pluginData,
      },
      encoding: "utf8",
    },
  );
  assert.notEqual(unknownSecret.status, 0);
  assert.match(`${unknownSecret.stdout}\n${unknownSecret.stderr}`, /secret|credential|token/i);
  assert.equal(existsSync(unknownSecretPath), false);

  for (const secret of [
    "Bearer abcdefghijklmnop",
    `github_pat_${"a".repeat(24)}`,
    "AccountKey=ZmFrZS1hY2NvdW50LWtleQ==",
  ]) {
    const path = writeEnvelope(repo, {
      result: "DEFERRED",
      reason: secret,
      checkedOwners: [],
      validationEvidence: [],
    });
    const rejected = spawnSync(
      process.execPath,
      [HOOK_SCRIPT, "record", "--session", "session-1", "--envelope", path, "--json"],
      {
        cwd: repo.root,
        env: { ...process.env, PLUGIN_DATA: repo.pluginData },
        encoding: "utf8",
      },
    );
    assert.notEqual(rejected.status, 0);
    assert.match(rejected.stdout, /secret|credential/i);
    assert.equal(existsSync(path), false);
  }
});

test("record rejects a raw diff nested inside an envelope string", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeValidation(repo);
  const candidate = status(repo).validationEvidenceCandidates.at(-1);
  const envelopePath = writeEnvelope(repo, {
    validationEvidence: [
      {
        kind: "test",
        toolUseId: candidate.toolUseId,
        inputDigest: candidate.inputDigest,
        commandHash: candidate.commandHash,
        expectedExitCodes: [0],
        scope: "checked behavior\ndiff --git a/src/app.txt b/src/app.txt",
      },
    ],
  });

  const result = spawnSync(
    process.execPath,
    [HOOK_SCRIPT, "record", "--session", "session-1", "--envelope", envelopePath, "--json"],
    {
      cwd: repo.root,
      env: {
        ...process.env,
        CLAUDE_PLUGIN_DATA: repo.pluginData,
        PLUGIN_DATA: repo.pluginData,
      },
      encoding: "utf8",
    },
  );

  assert.notEqual(result.status, 0);
  assert.match(`${result.stdout}\n${result.stderr}`, /raw diff|secret|credential/i);
});

test("record enforces the envelope limit in UTF-8 bytes", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  observeValidation(repo);
  const candidate = status(repo).validationEvidenceCandidates.at(-1);
  const envelopePath = writeEnvelope(repo, {
    validationEvidence: [
      {
        kind: "test",
        toolUseId: candidate.toolUseId,
        inputDigest: candidate.inputDigest,
        commandHash: candidate.commandHash,
        expectedExitCodes: [0],
        scope: "界".repeat(30_000),
      },
    ],
  });

  const result = spawnSync(
    process.execPath,
    [HOOK_SCRIPT, "record", "--session", "session-1", "--envelope", envelopePath, "--json"],
    {
      cwd: repo.root,
      env: {
        ...process.env,
        CLAUDE_PLUGIN_DATA: repo.pluginData,
        PLUGIN_DATA: repo.pluginData,
      },
      encoding: "utf8",
    },
  );

  assert.notEqual(result.status, 0);
  assert.match(`${result.stdout}\n${result.stderr}`, /64 KiB|safety limit/i);
  assert.equal(existsSync(envelopePath), false);
});

test("repository fingerprints include content changes inside an already dirty submodule", (t) => {
  const repo = createRepository(t);
  const nestedFile = addSubmodule(repo, t);
  writeFileSync(nestedFile, "dirty baseline\n");
  submitPrompt(repo);
  writeFileSync(nestedFile, "dirty baseline changed again\n");

  const output = stop(repo);

  assert.equal(isBlocked(output), true);
  assert.match(output.reason, /repository|terminal|receipt/i);
});

test("repository fingerprints stream a large dirty file and detect same-size edits", (t) => {
  const repo = createRepository(t);
  const largePath = join(repo.root, "large.bin");
  writeFileSync(largePath, Buffer.alloc(16 * 1024 * 1024, 0x61));
  submitPrompt(repo);
  const descriptor = openSync(largePath, "r+");
  try {
    writeSync(descriptor, Buffer.from([0x62]), 0, 1, 8 * 1024 * 1024);
  } finally {
    closeSync(descriptor);
  }

  const output = stop(repo);

  assert.equal(isBlocked(output), true);
  assert.equal(status(repo).transitionExplained, false);
});

test("UserPromptSubmit prunes expired envelope files", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  const path = writeEnvelope(repo);
  const old = new Date("2000-01-01T00:00:00.000Z");
  utimesSync(path, old, old);

  submitPrompt(repo, {
    session_id: "session-2",
    turn_id: "turn-2",
    prompt: "Start a fresh session.",
  });

  assert.equal(existsSync(path), false);
});

test("repository journals stay bounded and expose a pruned baseline gap", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  const journalsRoot = join(repo.pluginData, "journals");
  const path = join(journalsRoot, readdirSync(journalsRoot)[0]);
  const journal = JSON.parse(readFileSync(path, "utf8"));
  journal.events = Array.from({ length: 1025 }, (_, index) => ({
    sequence: index + 1,
    mutationObserved: false,
  }));
  journal.nextSequence = 1026;
  journal.floorSequence = 1;
  writeFileSync(path, `${JSON.stringify(journal)}\n`);

  const input = { command: "bounded journal check", workdir: repo.root };
  preTool(repo, "tool-bounded", input);
  postTool(repo, "tool-bounded", input, { exitCode: 0 });

  const bounded = JSON.parse(readFileSync(path, "utf8"));
  assert.ok(bounded.events.length <= 1024);
  assert.ok(bounded.floorSequence > 1);
  const current = status(repo);
  assert.equal(current.journalGap, true);
  assert.equal(current.transitionExplained, false);
});

test("a dead journal lock is recovered without waiting for its age timeout", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  const journalsRoot = join(repo.pluginData, "journals");
  const path = join(journalsRoot, readdirSync(journalsRoot)[0]);
  const lockPath = `${path}.lock`;
  mkdirSync(lockPath);
  writeFileSync(
    join(lockPath, "owner.json"),
    JSON.stringify({ pid: 999999, createdAt: new Date().toISOString() }),
  );

  assert.equal(status(repo).sessionId, "session-1");
  assert.equal(existsSync(lockPath), false);
});

test("UserPromptSubmit prunes expired session state", (t) => {
  const repo = createRepository(t);
  submitPrompt(repo);
  const statesRoot = join(repo.pluginData, "states");
  const oldStatePath = join(statesRoot, readdirSync(statesRoot)[0]);
  const oldState = JSON.parse(readFileSync(oldStatePath, "utf8"));
  writeFileSync(
    oldStatePath,
    `${JSON.stringify({ ...oldState, updatedAt: "2000-01-01T00:00:00.000Z" })}\n`,
  );

  submitPrompt(repo, {
    session_id: "session-2",
    turn_id: "turn-2",
    prompt: "Start a fresh session.",
  });

  assert.equal(readdirSync(statesRoot).filter((name) => name.endsWith(".json")).length, 1);
  assert.equal(status(repo, "session-2").sessionId, "session-2");
});

test("hook events degrade gracefully outside a Git repository", (t) => {
  const root = mkdtempSync(join(tmpdir(), "product-studio-no-git-"));
  const pluginData = join(root, ".plugin-data");
  mkdirSync(pluginData);
  const repo = { root, pluginData };
  t.after(() => rmSync(root, { recursive: true, force: true }));

  const promptOutput = submitPrompt(repo);
  assert.match(
    promptOutput.hookSpecificOutput?.additionalContext ?? "",
    /not inside a Git repository/i,
  );
  const stopOutput = stop(repo);
  assert.equal(isBlocked(stopOutput), false);
  assert.match(stopOutput.systemMessage ?? "", /not inside a Git repository/i);
});
