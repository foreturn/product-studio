# Changelog

## Unreleased

- Replaced seven role shells with five callable skills: `router`, `design`, `backend`, `frontend`, and `verification`. `design` owns product design, while `backend` owns system architecture and server implementation; the former release role and standalone deployment capability were removed.
- Scoped the plugin to product design, system architecture, frontend and backend implementation, and test verification. Actual production deployment, production migration, traffic switching, production configuration changes, and rollback remain outside the plugin and must use the target project's existing operational tooling and ownership.
- Curated five professional capability references from commit `9efef58ddb3f3a4bebcf856f6c2eef7ca7a53194`, retaining role responsibilities, core capabilities, and common-misjudgment guidance while removing the standalone decision-order and delivery-evidence chapters.
- Mapped delivery orchestration to `router`, product design to `design`, and system architecture to `backend`; product design uses the compact downstream contract in `design/SKILL.md`, while backend conditionally loads the architecture and implementation references.
- Replaced process/history memory with four final-code-fact stores owned by `design`, `backend`, `frontend`, and `verification`. Each professional Skill owns its sole `references/memory.md`; human-readable semantic topics retain only the current fact, code locations, impact scope, and reusable validation entrypoint. Refactors, migrations, renames, temporary compatibility stages, and change history only trigger reconciliation and never become memory content; `router` owns no memory.
- Added static gates for the exact five-skill topology, five curated-reference hashes and structure, product-versus-architecture ownership, four skill-owned memory references and inline formats, human-readable fact topics, code-task routing boundaries, and the absence of legacy role invocations or root-level memory resources.

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
