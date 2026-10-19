# D&D 5e Character Manager

A lightweight, browser-based character sheet for players who want a convenient place to build, organize, and play their Dungeons & Dragons 5e characters—without needing a complicated setup.

This is an independent project built for my own games and friends. It is actively evolving, so treat it as a work in progress and double-check rules interactions with your table's chosen rules.

## What it is

The Character Manager brings the everyday details of a player character into one place: core stats, combat tracking, equipment, spells, features, resources, and the personal notes that make a character feel like more than a list of numbers. It is designed to be usable at the table on both desktop and mobile-sized screens.

## Current features

- **Character roster and character creation** — create and switch between multiple characters.
- **Character overview** — keep key information such as hit points, armor class, speed, initiative, conditions, and concentration status close at hand.
- **Stats and skills** — manage ability scores, saving throws, skill proficiencies, and related character details.
- **Equipment and attacks** — record gear, equip supported items, and use available attack and dice-rolling tools.
- **Spells and resources** — organize spells, track spell slots and limited-use abilities, and manage rest-related resources.
- **Level and character details** — record class levels, features, feats, appearance, background, and other character information.
- **Notes and personal organization** — keep character notes and campaign-related thoughts together, with tags and linked notes.
- **Printable character sheet** — create a themed print-friendly sheet for a physical or digital tabletop.
- **Themes and presentation** — choose from several visual themes and character-sheet frame styles.
- **Import, export, and backups** — export characters or rosters as JSON and import them later, so your data can be moved or backed up.
- **2014 / 2024 ruleset selection** — identify which rules generation a character uses. This is a useful organizing aid, not a guarantee that every rule or edge case is automated.

## What makes it different?

There are already excellent character tools, and this project is not trying to claim that it has more content or more complete automation than established platforms. Its focus is a smaller, approachable tool that I can shape around the needs of my own table.

### Compared with D&D Beyond

D&D Beyond is the official D&D digital toolset, with a character builder and sheet, cross-device account syncing, and a wider connected ecosystem. This project takes a more lightweight approach: it is a standalone web app, keeps character data in the browser, and supports JSON export/import rather than requiring an account-based cloud workflow. That can be useful for a small group that wants a simple tool they can experiment with and customize.

### Compared with Reroll

Reroll is known for its distinctive customizable pixel-art characters and visual character-sheet experience. The Character Manager takes a more practical, information-first approach: its emphasis is on character details, play-time tracking, notes, printable sheets, and data portability rather than pixel-art avatar creation.

### The intended sweet spot

- **Simple to open:** the app is a self-contained HTML page; no build step is required to run it locally.
- **Personal and adaptable:** the project can evolve in response to feedback from the people using it.
- **Data you can take with you:** character and roster JSON export/import make it easier to keep your own backups.
- **Useful between turns:** core stats, gear, spells, resources, and notes live together instead of being spread across separate documents.

These are differences in project focus, not a claim that one product is universally better than another.

## Important limitations

- **Browser-local data:** characters are saved in the browser's local storage. They do not automatically sync between friends, browsers, or devices. Export backups regularly, especially before clearing browser data or switching devices.
- **No accounts or multiplayer backend:** this is currently a personal character manager, not a hosted multi-user campaign service.
- **Rules coverage is incomplete:** the ruleset selector and centralized calculations are still a work in progress. Verify edition-specific mechanics, class features, spells, feats, multiclassing, and unusual combinations against the rules used by your DM.
- **Content availability:** this project is not a replacement for official rulebooks or a complete licensed digital compendium.
- **Work in progress:** bugs and rough edges are possible. Feedback and reproducible bug reports are welcome.

## Try it

### Run locally

1. Download or clone this repository.
2. Open `index.html` in a modern browser.
3. Create a character and use the export option to make a backup.

No package installation or build step is needed for the current standalone app.

## Feedback

This is currently aimed at a small group of friends and other players who are interested in trying it. If something is confusing, a calculation looks wrong, or you have an idea that would make it more useful at the table, please open a GitHub issue with steps to reproduce the problem where possible.

## Project boundaries

This repository contains the **Character Manager** only. The separate Dungeon Master Manager lives in its own repository.

## Disclaimer

This is an unofficial, fan-made project and is not affiliated with, endorsed by, or sponsored by Wizards of the Coast. Dungeons & Dragons and D&D are trademarks of Wizards of the Coast. Use the rules and content you are authorized to use, and follow the applicable licenses for any third-party material included in this repository.
