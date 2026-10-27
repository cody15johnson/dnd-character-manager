# Character Manager React workspace

This Vite + React + TypeScript app is isolated under `react-app/`. The existing standalone app remains at the repository root. This workspace does not change its deployment setup or access browser storage.

Requirements: Node.js 20.19+ or 22.12+ and pnpm 11.25+.

From this directory, run `pnpm install` once, then use `pnpm dev` or `pnpm build`.

The current screen uses fictional typed fixtures. `src/data/characterImportPreview.ts` is a pure preview parser for the existing `dnd-character` and `dnd-character-roster` schema version 1 envelopes and legacy JSON shapes. It accepts JSON text and reports format, shape counts, ruleset counts, duplicates, and warnings; it does not normalize, persist, or mutate records. No file picker or localStorage connection is present.