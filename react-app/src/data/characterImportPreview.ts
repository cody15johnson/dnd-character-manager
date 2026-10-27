type JsonRecord = Record<string, unknown>;

export type CharacterImportFormat =
  | "dnd-character v1"
  | "dnd-character-roster v1"
  | "legacy JSON";

export type CharacterImportPreview = {
  ok: true;
  format: CharacterImportFormat;
  recordCount: number;
  validCharacterCount: number;
  invalidRecordCount: number;
  duplicateIdCount: number;
  rulesets: { rules2014: number; rules2024: number; unspecified: number };
  warnings: string[];
};

export type CharacterImportPreviewError = { ok: false; message: string };

const isRecord = (value: unknown): value is JsonRecord =>
  typeof value === "object" && value !== null && !Array.isArray(value);

const hasCharacterShape = (value: unknown): value is JsonRecord =>
  isRecord(value) && isRecord(value.abil);

function unwrapRecords(value: unknown): {
  format: CharacterImportFormat;
  records: unknown[];
} {
  if (isRecord(value) && typeof value.format === "string") {
    if (value.schemaVersion !== 1) {
      throw new Error("Unsupported character file version.");
    }

    if (value.format === "dnd-character") {
      if (!isRecord(value.character)) {
        throw new Error("Character envelope is missing its character data.");
      }
      return { format: "dnd-character v1", records: [value.character] };
    }

    if (value.format === "dnd-character-roster") {
      if (!Array.isArray(value.characters)) {
        throw new Error("Roster envelope is missing its characters list.");
      }
      const records = value.characters.map((entry) => {
        if (isRecord(entry) && entry.format === "dnd-character") {
          if (entry.schemaVersion !== 1 || !isRecord(entry.character)) {
            throw new Error("Invalid character entry in roster.");
          }
          return {
            ...entry.character,
            ruleset:
              entry.ruleset === "2014" || entry.ruleset === "2024"
                ? entry.ruleset
                : entry.character.ruleset,
          };
        }
        return entry;
      });
      return { format: "dnd-character-roster v1", records };
    }

    throw new Error(`Unsupported file format: ${value.format}`);
  }

  return {
    format: "legacy JSON",
    records: Array.isArray(value) ? value : [value],
  };
}

/**
 * Inspect a character export without normalizing, storing, or mutating it.
 * The legacy app considers a record loadable when it has an ability-score map.
 */
export function parseCharacterImportPreview(
  input: string,
): CharacterImportPreview | CharacterImportPreviewError {
  let parsed: unknown;
  try {
    parsed = JSON.parse(input);
  } catch {
    return { ok: false, message: "This text is not valid JSON." };
  }

  try {
    const { format, records } = unwrapRecords(parsed);
    const valid = records.filter(hasCharacterShape);
    const ids = valid
      .map((record) => record.id)
      .filter((id): id is string => typeof id === "string" && id.length > 0);
    const duplicateIdCount = ids.length - new Set(ids).size;
    const invalidRecordCount = records.length - valid.length;
    const rulesets = valid.reduce<{
      rules2014: number;
      rules2024: number;
      unspecified: number;
    }>(
      (counts, character) => {
        const ruleset =
          isRecord(parsed) && parsed.format === "dnd-character" &&
          (parsed.ruleset === "2014" || parsed.ruleset === "2024")
            ? parsed.ruleset
            : character.ruleset;
        if (ruleset === "2014") counts.rules2014 += 1;
        else if (ruleset === "2024") counts.rules2024 += 1;
        else counts.unspecified += 1;
        return counts;
      },
      { rules2014: 0, rules2024: 0, unspecified: 0 },
    );
    const warnings: string[] = [];
    if (invalidRecordCount) {
      warnings.push(
        `${invalidRecordCount} record(s) do not contain the required ability-score map and would be skipped by the legacy loader.`,
      );
    }
    if (duplicateIdCount) {
      warnings.push(
        `${duplicateIdCount} duplicate character ID(s) found; the legacy import path assigns fresh IDs to duplicates.`,
      );
    }

    return {
      ok: true,
      format,
      recordCount: records.length,
      validCharacterCount: valid.length,
      invalidRecordCount,
      duplicateIdCount,
      rulesets,
      warnings,
    };
  } catch (error) {
    return {
      ok: false,
      message: error instanceof Error ? error.message : "Unsupported character file.",
    };
  }
}
