# Working on Worlds 2026 Calendar

- Keep the product minimal, bilingual (PL/EN), mobile-friendly and clearly unofficial.
- Never invent production matches. Test fixtures belong in tests only. Preserve the last successful schedule on source or validation failure.
- Keep stable event UIDs and increment SEQUENCE only for changed event data. Never infer cancellation from omission in a rolling API page.
- Use Python 3.12 and the standard library for the sync job. Run `python -m unittest discover -s tests -v` after backend changes. Exercise real API generation when access permits, using `--state .local/events.json --site .local/site` to avoid changing the published snapshot.
- For interface changes, check PL/EN, mobile widths, local times, subscription links and clipboard behavior in a real browser. Browser tooling is optional development tooling, not a runtime dependency.
- Record significant verified work, test results and blockers in `docs/BUILD_LOG.md`; update `docs/PROJECT_STATUS.md` and record important technical choices in `docs/DECISIONS.md`.
- Documentation is public: do not include secrets, personal reflections or claims of unverified deployment. Distinguish local checks, pushed code, Actions runs, Pages publication and calendar-client checks.
- Finish major sessions with CHATGPT_HANDOFF: date/project, delivered work, solved problems, decisions, test/deployment evidence, commit/PR links, next step and a factual potential entrepreneurial milestone. Do not invent the owner's feelings or decisions.
- Use the existing isolated checkout; do not create a worktree unless requested. Preserve existing user work and never force-push or reset unrelated changes.
