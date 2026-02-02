<!--
 Sync Impact Report
 - Version change: N/A -> 0.1.0
 - Modified principles: N/A (initial)
 - Added sections: Core Principles, Application & Data Standards, Development Workflow & Quality Gates, Governance
 - Removed sections: N/A
 - Templates requiring updates: ⚠ pending review (.specify/templates/*.md)
 - Follow-up TODOs: TODO(RATIFICATION_DATE) set ratification date once agreed
 -->
 
 # GeoEmerge Mosquito Risk Mapping Constitution
 
## Core Principles

 ### 1) Clean Architecture Boundaries
 Domain/business logic MUST not depend on frameworks, web layers, or infrastructure.
 Dependencies MUST point inward. Prefer composition over inheritance.

 ### 2) Reproducible EDA Over Intuition
 EDA work MUST be reproducible (seeded, scripted/notebooked, and rerunnable).
 Surface schema, missingness, outliers, distributions, correlations, and leakage risk
 before modeling.

 ### 3) Tests for Non-Trivial Logic
 Any non-trivial domain logic MUST have tests (prefer `pytest`).
 Tests MUST be deterministic and avoid unnecessary mocking.

 ### 4) Contract-Driven API
 API request/response schemas MUST be explicit and versioned.
 Breaking changes require a migration plan and a version bump.

 ### 5) Observability, Safety, and Simplicity
 Do not swallow exceptions. Log meaningful events (without secrets/PII). Validate all
 external inputs at boundaries. Avoid over-engineering; keep changes minimal.

 ## Application & Data Standards
 
 - Python target MUST be 3.10+.
 - Type hints SHOULD be used for production code paths.
 - Notebooks MUST have outputs cleared before commit (`jupyter nbconvert --clear-output`).
 - Raw datasets MUST be preserved; preprocessing steps MUST be explainable.

 ## Development Workflow & Quality Gates
 
 - Changes MUST be small and aligned to existing architecture (no unrelated refactors).
 - PRs MUST include:
   - What changed and why
   - Risks and rollout/validation plan (if applicable)
   - Evidence: tests run and/or EDA artifacts updated

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

 This constitution is the top-level standard for this repository.
 
 - Amendments MUST update this file and increment semantic versioning:
   - MAJOR: breaking governance changes or principle removals
   - MINOR: new/expanded principle or section
   - PATCH: clarifications/wording
 - All significant changes MUST be reviewed for compliance.

 **Version**: 0.1.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2026-02-02
