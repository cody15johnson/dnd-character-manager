export type DemoCharacter = {
  id: string;
  name: string;
  initial: string;
  level: number;
  ancestry: string;
  className: string;
  ruleset: "2014 rules" | "2024 rules";
  hpCurrent: number;
  hpMaximum: number;
  armorClass: number;
  speed: number;
  tone: "ember" | "moss" | "violet";
};

// Fictional presentation data only. It is not read from character storage.
export const demoCharacters: DemoCharacter[] = [
  { id: "demo-ember", name: "Mira Ashford", initial: "M", level: 5, ancestry: "Tiefling", className: "Bard", ruleset: "2024 rules", hpCurrent: 31, hpMaximum: 38, armorClass: 15, speed: 30, tone: "ember" },
  { id: "demo-moss", name: "Thorin Oakenshield", initial: "T", level: 4, ancestry: "Dwarf", className: "Paladin", ruleset: "2014 rules", hpCurrent: 42, hpMaximum: 42, armorClass: 18, speed: 25, tone: "moss" },
  { id: "demo-violet", name: "Ilyra Moonwhisper", initial: "I", level: 3, ancestry: "Elf", className: "Druid", ruleset: "2024 rules", hpCurrent: 19, hpMaximum: 27, armorClass: 14, speed: 35, tone: "violet" },
];
