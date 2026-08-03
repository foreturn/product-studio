# Changelog

## Unreleased

- Restored `release` as the seventh callable skill beside `router`, `design`, `architecture`, `backend`, `frontend`, and `verification`. Release readiness, authorization, execution, health, rollback, incident response, and feedback now have a separate owner again.
- Centralized production deployment, production migration, traffic switching, production configuration changes, rollback, and incident operations in `release`. External changes require explicit authorization bound to the current artifact, target environment, scope, action, and time window, and must use the target project's existing operational tooling.
- Curated seven professional capability references while retaining role responsibilities, core capabilities, and common-misjudgment guidance and removing standalone decision-order and delivery-evidence chapters.
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
