# Cross-App Regression Test Report

Apps: Character Manager v1.5.0 and DM Manager Phase 3.2 (3.2.0).

Environment: Playwright + system Chromium; HTML loaded via page.set_content with localStorage shim. Native file pickers/downloads and real browser-profile persistence are not covered.

Result: 11/11 checks passed.

- PASS: Character Manager imports 2014/2024 roster
- PASS: Character note links persist bidirectionally — 2 notes; suggestion detected=True
- PASS: Character note links survive JSON export
- PASS: Character export contains the note records and links — dnd-character
- PASS: DM Manager validates Character Manager export before changes — Validated 1 character(s) from dnd-character. Nothing has been changed yet.
Ruleset warning: 1 imported character(s) are labeled differently from this campaign (2024 rules). No conv
- PASS: DM Manager imports character snapshot
- PASS: DM snapshot preserves linked character notes — 2 note records imported
- PASS: Edition mismatch is warned without conversion
- PASS: Combat HP changes are saved to encounter state — HP 12 → 9
- PASS: Combat HP changes do not overwrite imported character snapshot — encounter HP is DM-owned state
- PASS: No uncaught browser JavaScript errors