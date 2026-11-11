Changes Made:
- Updated `EvidenceClaim` schema to include `context_needed` and to retain its structure.
- Updated `FounderDecision` to be explicit Enum as specified.
- Created strict validations on `CheckpointResolveRequest` for `pivoted_hypothesis` ensuring it is not empty, and for `decisions` checking that every claim has a `founder_decision`.
- Added the `Session` domain model with strict lifecycle verification.
- Added `resolve_checkpoint` method internally ensuring it rejects unauthorized users, expired sessions, or sessions that are not in the valid transitional state (`HALTED_AT_HUMAN_GATE`).
- Set up tests under `backend/tests`, verifying Pydantic schema constraints and validating the state transitions for the `Session` domain model.
- Completed all tasks independently of external provider requirements and without mutating API endpoints.

Paths Modified:
- `backend/main.py`
- `backend/pyproject.toml`
- `backend/tests/conftest.py` (added)
- `backend/tests/test_main.py` (moved and extended)

Tests and Exact Results:
- Tests were successfully run using `uv run pytest` inside `backend`. Output: `9 passed, 1 warning in 0.56s`.
- Types checked via `uv run mypy .` and passed (`Success: no issues found in 3 source files`).
- Lint checked via `uv run ruff check .` and passed (`All checks passed!`).

MCPs Used:
- Context7 (to identify Pydantic schema validation parameters)

Approvals: No write operations external to code were invoked.
Residual risks: The `checkpoint_resolve` API method mock will need to be refactored further to fetch the `Session` properly and execute `resolve_checkpoint` correctly in J06.
