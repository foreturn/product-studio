# Changelog

## Unreleased

## 1.0.1 - 2026-08-03

- Reorganized backend engineering into nine concrete capabilities, separating data modeling and queries from migration and data evolution. Assigned API idempotency semantics, transaction enforcement, asynchronous delivery, and performance evidence to a single capability each, and simplified the Skill workflow so it no longer repeats detailed capability rules.
- Reorganized system architecture into nine non-overlapping capabilities, separating architecture-context gating, boundary responsibilities, data ownership and invariants, cross-boundary interactions, quality decisions, failure recovery, security, operability, and evolution/delivery slicing. Simplified the Skill workflow so it no longer repeats the detailed capability rules.
- Reorganized product design into eight concrete capabilities: current-state problem definition, user-role-task modeling, business rules and closure, task journey and information actions, state and recovery, scope, success and acceptance, and assumption/decision management. Removed the standalone product-contract section, assigned risk handling, permission semantics, prioritization, and unknowns to a single capability each, and simplified the Skill workflow so it no longer repeats detailed capability rules.
- Removed duplicated capability-selection maps from the six professional `SKILL.md` files. Each Skill now keeps only the progressive-loading entry to its `principles.md`; router routing rules remain unchanged.
- Expanded `release` with repository release governance: exact diff ranges, authoritative version sources, project-defined version and Tag conventions, traceable release notes, dirty-worktree gates, immutable published Tags, and separate authorization for commit, Tag, push, remote Release, and Tag-triggered deployment actions.
- Restored `release` as the seventh callable skill beside `router`, `design`, `architecture`, `backend`, `frontend`, and `verification`. Release readiness, authorization, execution, health, rollback, incident response, and feedback now have a separate owner again.
- Centralized production deployment, production migration, traffic switching, production configuration changes, rollback, and incident operations in `release`. External changes require explicit authorization bound to the current artifact, target environment, scope, action, and time window, and must use the target project's existing operational tooling.
- Curated seven professional capability references around concrete core capabilities and common misjudgments, removing generic role-responsibility sections already owned by each `SKILL.md`.
- Normalized every skill-owned capability filename to the single word `principles.md`; each Skill loads only its own curated reference.
- Replaced process/history memory with six current-fact stores owned by `design`, `architecture`, `backend`, `frontend`, `verification`, and `release`. Each professional Skill owns its sole `references/memory.md`; release memory retains only reusable, currently evidenced operational facts and never persists authorization, command streams, incident timelines, or secrets. `router` owns no memory.
- Removed the repository-specific Python validator and exact capability-reference hashes. Platform validators now cover plugin shape, while routing, ownership boundaries, and task behavior require direct evidence from fresh-context trials.
- Removed router-owned terminal closure and centralized memory synchronization. The router now stops orchestration when promised artifacts are ready or a hard dependency prevents continuation; `verification` owns the final verdict, while each invoked specialist owns its own fact synchronization.

## 0.3.0 - 2026-07-16

- Added evidence-based expansion for sparse vibe-coding prompts with explicit fact, inference, and decision boundaries.
- Defined role inputs, responsibilities, outputs, handoff gates, and return paths across the complete product lifecycle.
- Added requirement-to-evidence traceability and stricter delivery completion rules.
- Added release operations for deployment authorization, migrations, rollback, post-release validation, and feedback loops.
- Expanded every lifecycle role with explicit professional capabilities and implementation-level decision heuristics, including comprehensive frontend UX and visual quality guidance.
- Expanded shared templates, Codex UI metadata, dual-platform descriptions, and deterministic project validation targets.

## 0.2.1 - 2026-07-16

- Translated skill instructions, UI prompts, plugin metadata, templates, and usage documentation into Chinese.
- Removed routing eval cases that were not connected to an evaluation runner.

## 0.2.0 - 2026-07-16

- Extracted product, frontend, backend, architecture, and verification guidance from global instructions into focused skills.
- Added end-to-end product delivery orchestration and durable artifact paths.
- Added architecture and acceptance templates, routing eval cases, and deterministic project validation.

## 0.1.0 - 2026-07-16

- Initialized shared product development skills and templates.
- Added Codex and Claude Code plugin manifests.
