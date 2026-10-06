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

-- Credit Card ("Nachträgliche Vorauszahlung"): +$20 when bought, but after 5 rounds it is
-- destroyed and takes $30 with it; selling it early also costs $30. Vanilla's debt effect
-- is tied to the name "Credit Card", so a different internal name turns that off.
-- Credit Cards saved before the rework store `extra` as a plain number (vanilla's 20).
local function credit_extra(card)
    if type(card.ability.extra) ~= 'table' then
        card.ability.extra = { money = 20, rounds = 5, penalty = 30 }
    end
    return card.ability.extra
end

SMODS.Joker:take_ownership('credit_card', {
    name = 'Donl Credit Card',
    blueprint_compat = false,
    eternal_compat = false,
    config = { extra = { money = 20, rounds = 5, penalty = 30 } },
    loc_vars = function(self, info_queue, card)
        local ex = credit_extra(card)
        return { vars = { ex.money, ex.rounds, ex.penalty } }
    end,
    add_to_deck = function(self, card, from_debuff)
        if not from_debuff then
            ease_dollars(credit_extra(card).money)
        end
    end,
    calculate = function(self, card, context)
        if context.end_of_round and context.main_eval and not context.blueprint and not context.game_over then
            local ex = credit_extra(card)
            ex.rounds = ex.rounds - 1
            if ex.rounds <= 0 then
                ease_dollars(-ex.penalty)
                SMODS.destroy_cards(card, nil, nil, true)
                return { message = '-$' .. ex.penalty, colour = G.C.RED }
            end
            return { message = ex.rounds .. '', colour = G.C.FILTER }
        end
    end,
})

-- Its sell value is a fixed -$30 (outermost wrapper, so TrekTrendy doesn't double it).
local set_sell_value_ref = Card.set_sell_value
function Card:set_sell_value()
    set_sell_value_ref(self)
    if self.config.center.key == 'j_credit_card' then
        self.sell_cost = -credit_extra(self).penalty
    end
end

-- "Die Monstera" (Flower Pot) and "Die Werbeanfrage" (Business Card): removed from the game -
-- never spawn and hidden from the collection. They stay registered (and in the art grid
-- above, which is index-based) so saves load.
for _, key in ipairs({ 'flower_pot', 'business' }) do
    SMODS.Joker:take_ownership(key, {
        no_collection = true,
        in_pool = function(self, args)
            return false
        end,
    })
end

-- Burnt Joker ("One-Take Donnie"): beat a Small or Big Blind with a single hand and no
-- discards and you also get that blind's skip tag. Nothing for Boss Blinds (they have no
-- skip tag). Vanilla's level-up on the first discard is tied to the name "Burnt Joker",
-- so a different internal name turns that off.
SMODS.Joker:take_ownership('burnt', {
    name = 'Donl Burnt Joker',
    rarity = 2,
    cost = 6,
    blueprint_compat = true,
    calculate = function(self, card, context)
        if context.end_of_round and context.main_eval and not context.game_over
            and G.GAME.current_round.discards_used == 0 and G.GAME.current_round.hands_played == 1 then
            local blind_type = G.GAME.blind:get_type()
            local tag_key = blind_type ~= 'Boss' and G.GAME.round_resets.blind_tags[blind_type]
            if tag_key then
                G.E_MANAGER:add_event(Event({
                    func = function()
                        add_tag(Tag(tag_key, nil, blind_type))
                        play_sound('generic1', 0.9 + math.random() * 0.1, 0.8)
                        play_sound('holo1', 1.2 + math.random() * 0.1, 0.4)
                        return true
                    end,
                }))
                return { message = localize('k_donl_one_take'), colour = G.C.FILTER }
            end
        end
    end,
})

-- Mystic Summit ("Ohne Rampe, ohne mich"): effect unchanged, but a bit rarer. Each time a
-- joker pool is built it sits out 1 time in 4, so it shows up ~75% as often as another Common.
SMODS.Joker:take_ownership('mystic_summit', {
    in_pool = function(self, args)
        return pseudorandom('donl_mystic_summit') >= 0.25
    end,
})
