# Changelog

## 2.2.5 - 2026-09-01

- Required behavior-affecting architecture and implementation work to trace real entry points, state, data interactions, side effects, and recovery through to observable business results before coding.
- Distinguished reusable business capabilities from parameterized examples, helper extraction, and duplicated branches, while converging backend interfaces, messages, tasks, and administrative entry points on shared use cases or domain surfaces.
- Required Web, Android, and iOS entry adapters to reuse established business capabilities and applicable contracts without forcing full-flow design onto unrelated local changes or prebuilding generic frameworks for hypothetical reuse.

## 2.2.4 - 2026-08-31

- Distinguished fully enumerable deterministic rules from context-dependent semantic interpretation across software architecture and backend engineering.
- Required semantic interpretation to cross boundaries through constrained structured results with explicit scope, ambiguity, evidence needs, and next steps, while limiting deterministic execution to validation, authorization, resource, evidence, and side-effect safeguards.
- Added observable evidence-gap feedback and conservative degradation, rejecting keyword, regular-expression, deletion-list, and example heuristics as substitutes for product-owned semantic responsibility.

## 2.2.3 - 2026-08-24

- Required architecture, backend, Web, Android, iOS, and platform implementation to satisfy confirmed functionality and boundaries before choosing the simplest behaviorally complete design.
- Added code-level organization and naming constraints for directories, files, modules, types, classes, components, methods, functions, constants, configuration, pure logic, and side effects.
- Prioritized reuse of existing project capabilities, platform standards, and mature open-source components, while requiring contract, maintenance, security, license, dependency, operational, upgrade, and exit-cost review before adoption or limited custom implementation.

## 2.2.2 - 2026-08-23

- Reframed user-visible content around the user's context, business object, task, decision, outcome, and next step, while limiting AI or system narration and unsupported value claims.
- Required Web, Android, and iOS Skills to implement confirmed product content semantics faithfully and report material semantic gaps instead of inventing product copy from an implementation perspective.
- Aligned client principles, project-memory topics, OpenAI invocation prompts, public ownership documentation, and the current Product Studio product facts with the same content-semantics boundary.

## 2.2.1 - 2026-08-19

- Made project-memory closeout explicit in all eleven Skills: tasks authorized to modify files under the current product root now directly create, update, or remove owner fact books before the final response, while read-only work remains read-only.
- Defined the current product root independently of Git, prioritized explicit product scope and target artifacts, and prohibited resolving fact books from the process directory or Product Studio's source, Skill, installation, or cache directories when the plugin is only the capability provider.
- Clarified root-anchored storage, first-fact directory and file creation, admission of newly verified pre-existing facts, current-fact writing guidance, and cleanup of empty fact books without turning memory into a task log.
- Extended project validation and documentation to enforce the complete root resolution, loading, authority, creation, maintenance, formatting, and cleanup contract, including rejection of empty current-fact books.

## 2.2.0 - 2026-08-17

- Moved project-memory location, authority, admission, synchronization, and exclusion instructions into every `SKILL.md`, leaving each `references/memory.md` focused exclusively on the owner-specific project facts worth remembering.
- Expanded all eleven memory references to nine core topics with three explicit fact prompts each, covering ownership, authority, lifecycle, failure, recovery, compatibility, and evidence boundaries without duplicating source inventories or task history.
- Updated the project validator, README, and current Product Studio fact books to enforce and describe the separate Skill, principles, and memory responsibilities while rejecting the legacy memory usage contract.

## 2.1.1 - 2026-08-16

- Simplified every professional memory reference to five to nine core project-knowledge topics, so future agents read only the durable product-specific context that changes engineering judgment.
- Removed the shared terminal-memory protocol and its action/result vocabulary; each Skill now reads relevant project memory before work and updates or removes stale knowledge only when core understanding changes.

## 2.1.0 - 2026-08-16

- Removed the terminal Hook registration, state machine, receipt fixture, and Hook-specific test suite so terminal fact closure no longer depends on client Hook trust, event delivery, or per-session runtime state.
- Moved terminal memory closure into every professional Skill as an explicit final-answer prompt contract: each Owner now revalidates hit facts, applies `ADD`, `UPDATE`, `DELETE`, or `NO_CHANGE`, writes only with repository authorization, and reports `SYNCED`, `NO_CHANGE`, `DEFERRED`, or `BLOCKED` in human-readable form.
- Replaced Hook asset validation with static checks that all eleven Skills contain owner-specific fact locators, complete action and result semantics, and terminal fact instructions, while explicitly documenting that behavioral compliance still requires fresh-context acceptance evidence.

## 2.0.0 - 2026-08-14

- Rebuilt the plugin as eleven independently discoverable professional skills spanning product management, architecture, backend, Web, Android, iOS, database, platform, security, quality, and release engineering; the coding agent chooses and orders applicable skills from the request, repository evidence, and risk.
- Standardized every `SKILL.md` as an execution contract with hit-only fact loading and authority revalidation, every `principles.md` as broad professional categories containing framework-neutral invariants and trade-off constraints, and every `memory.md` as five to nine owner-specific semantic terminal fact types with explicit admission, merging, wording, authority, revalidation, change, and exclusion rules.
- Removed applicability, non-applicability, and required-input sections from every Skill so the coding agent retains discovery and input-selection autonomy; frontmatter descriptions are now concise Chinese professional summaries.
- Tightened fact admission to require current terminal truth, stability, non-obviousness, decision relevance, rediscovery cost, unique ownership, revalidatability, and safe retention; source summaries, plans, migration progress, runtime snapshots, generated inventories, and one-run results remain turn evidence rather than project memory.
- Consolidated product intent and product experience under one product-management owner, while giving Web, Android, iOS, and platform engineering independent platform-specific boundaries.
- Replaced callable terminal synchronization with `UserPromptSubmit`, paired `PreToolUse`/`PostToolUse`, and `Stop` hooks that journal observed repository changes and validation commands, stream content fingerprints across unborn repositories, hidden index flags and nested worktrees, isolate concurrent sessions, bind exact fact-book paths, accept `SYNCED`, `NO_CHANGE`, `DEFERRED`, or `BLOCKED` receipts, delete accepted or rejected envelopes, and bound continuation to one retry.
- Bound validation evidence from observed `Bash`, `exec_command`, and `shell_command` completions while treating edit tools solely as mutation evidence.
- Split full-repository and implementation fingerprints so verified implementation evidence survives a later owner fact-book update, excluded protocol-control commands from validation evidence, and allowed only the sole observed `record` control to close its own ToolUse envelope.
- Made fact-book expression semantic rather than template-driven: topics retain stable merge keys, current truth, authority, scope, and revalidation meaning without requiring fixed Markdown headings, four labeled fields, order, or sentence counts.
- Adopted owner-named fact locators under `docs/product-studio/<product-id>/`, with no compatibility aliases or duplicate fact stores.

## 1.0.3 - 2026-08-11

- Scoped each specialist fact store to `docs/product-studio/<product-id>/<owner>.md` using a repository-unique, directory-safe product ID that may span multiple project roots; multi-product work now resolves and synchronizes every affected product separately without duplicating authoritative facts.

## 1.0.2 - 2026-08-06

- Redefined the six specialist fact stores as cumulative, project-wide views of each Owner's currently verified facts. A task now synchronizes only its actually inspected scope without treating the task, final diff, or most recent code change as the fact boundary, and read-only work reports candidate memory changes unless fact-store writes are authorized.
- Standardized every fact-store template and the fourteen existing Product Studio facts on four fields: current fact, authoritative evidence, impact boundary, and revalidation entry. Fact stores now use current-project titles without frontmatter, Owner metadata, status, timestamps, or format versions; volatile release facts still bind environment, artifact, verification time, and invalidation conditions.
- Clarified that Router owns no fact store, architecture memory retains only implemented evolution, migration, and compatibility constraints rather than temporary delivery slices, and each specialist remains the sole Owner of its fact text.
- Added durable verification and release facts for the distinct Codex and Claude Code distribution surfaces, their evidence limits, and the production-operation authorization boundary.

## 1.0.1 - 2026-08-03

- Reorganized frontend engineering into nine concrete capabilities, merging duplicated task and information-architecture rules, assigning interaction state, interface integration, accessibility, security, performance, and real-browser evidence to a single capability each, and simplifying the Skill workflow and completion gates so they no longer repeat detailed capability rules.
- Reorganized backend engineering into nine concrete capabilities, separating data modeling and queries from migration and data evolution. Assigned API idempotency semantics, transaction enforcement, asynchronous delivery, and performance evidence to a single capability each, and simplified the Skill workflow so it no longer repeats detailed capability rules.
- Reorganized system architecture into nine non-overlapping capabilities, separating architecture-context gating, boundary responsibilities, data ownership and invariants, cross-boundary interactions, quality decisions, failure recovery, security, operability, and evolution/delivery slicing. Simplified the Skill workflow so it no longer repeats the detailed capability rules.
- Reorganized product design into eight concrete capabilities: current-state problem definition, user-role-task modeling, business rules and closure, task journey and information actions, state and recovery, scope, success and acceptance, and assumption/decision management. Removed the standalone product-contract section, assigned risk handling, permission semantics, prioritization, and unknowns to a single capability each, and simplified the Skill workflow so it no longer repeats detailed capability rules.
- Reorganized router orchestration into eight non-overlapping capabilities covering trigger decisions, minimal skill chains, vertical slices, contract dependencies, parallel write isolation, risk probes, gate stopping, and change handoffs. Router remains the sole owner of explicit skill selection while specialist Skills keep only their progressive-loading principles entry, and the orchestration workflow no longer repeats detailed capability rules.
- Reorganized release and operations into nine non-overlapping capabilities covering release scope, version and Tag governance, release notes, artifact provenance, environment readiness, compatibility and migration, execution gates, health, and recovery feedback. Reduced duplicated workflow and incident rules while preserving exact authorization for repository and environment changes.
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
