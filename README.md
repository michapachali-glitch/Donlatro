# Donlatro

A [Balatro](https://www.playbalatro.com/) mod by MichaelP: 24 new Jokers, 46 reworked vanilla Jokers,
7 Boss Blinds, 10 Vouchers, 2 Tarots, 3 Spectrals and 2 Decks.

![Donlatro overview](promo/donlatro_overview.png)

## Installation

1. Install [Lovely](https://github.com/ethangreen-dev/lovely-injector) (>= 0.9.0) and
   [Steamodded](https://github.com/Steamodded/smods).
2. Copy this folder into `%AppData%\Balatro\Mods\` (so you get `Mods\Donlatro\main.lua`).
3. Start Balatro - Donlatro shows up in the Mods menu.

## Test mode

`src/testing.lua` has `TEST_MODE = true`: only Donlatro Jokers spawn and Jokers show up twice
as often in the shop. Set it to `false` for the normal Joker pool.

## Layout

| Path | Contents |
|---|---|
| `src/jokers.lua`, `src/food.lua` | new Jokers (food Jokers run out) |
| `src/reskins.lua` | renamed + redrawn vanilla Jokers |
| `src/blinds.lua` | Boss Blinds (incl. the techno final boss) |
| `src/vouchers.lua`, `src/consumables.lua`, `src/decks.lua` | Vouchers, Tarots/Spectrals, Decks |
| `src/tracking.lua` | run-wide bookkeeping (hand history, Ante deck snapshot, ...) |
| `localization/en-us.lua` | all names and descriptions |
| `tools/` | Python scripts that generate the pixel art, the boss music and the poster |
