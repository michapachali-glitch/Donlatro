-- Vanilla jokers renamed and redrawn for Donlatro (names in localization/en-us.lua; effects
-- stay vanilla). Taking ownership marks them as Donlatro jokers, so they stay in the
-- test-mode pool and start discovered.
--
-- Art: assets/{1x,2x}/Reskins.png, 10 x 5 grid in the order below (drawn by
-- tools/batch7_art.py); cells 45-48 are the soul layers of the four legendaries.
SMODS.Atlas {
    key = 'Reskins',
    path = 'Reskins.png',
    px = 71,
    py = 95,
}

local renamed = {
    'half', 'mystic_summit', 'flower_pot', 'stencil', 'abstract', 'loyalty_card', 'acrobat',
    'smeared', 'pareidolia', 'shortcut',
    'arrowhead', 'bloodstone', 'rough_gem', 'onyx_agate',
    'credit_card', 'delayed_grat', 'business', 'rocket', 'bull', 'bootstraps', 'matador',
    'troubadour', 'burglar', 'stuntman', 'juggler', 'drunkard', 'chaos', 'luchador', 'mr_bones',
    'ceremonial', 'marble', 'hiker', 'swashbuckler', 'misprint', 'baseball', 'idol', 'oops',
    'cartomancer', 'astronomer', 'vagabond', 'burnt',
    'triboulet', 'yorick', 'chicot', 'perkeo',
}
local legendary_soul = { triboulet = 45, yorick = 46, chicot = 47, perkeo = 48 }

local function cell(i)
    return { x = i % 10, y = math.floor(i / 10) }
end

for i, key in ipairs(renamed) do
    local soul = legendary_soul[key]
    SMODS.Joker:take_ownership(key, {
        atlas = 'Reskins',
        pos = cell(i - 1),
        soul_pos = soul and cell(soul) or nil,
    })
end

-- Half Joker ("Der kurze Gedanke"): vanilla shrinks any center *named* "Half Joker" to a
-- half-height card (Card:set_ability, set_sprites, load), which crops the full-size reskin
-- art and pushes the shop's buy button out of view. A different internal name turns that
-- off, so the effect is re-implemented here (same numbers as vanilla).
SMODS.Joker:take_ownership('half', {
    name = 'Donl Half Joker',
    loc_vars = function(self, info_queue, card)
        return { vars = { card.ability.extra.mult, card.ability.extra.size } }
    end,
    calculate = function(self, card, context)
        if context.joker_main and #context.full_hand <= card.ability.extra.size then
            return { mult = card.ability.extra.mult }
        end
    end,
})

-- Space Joker ("Die Rakete") gets the rocket art drawn for Donlatro.
SMODS.Joker:take_ownership('space', {
    atlas = 'Jokers',
    pos = { x = 0, y = 2 },
})
