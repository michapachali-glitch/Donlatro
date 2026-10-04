-- Donlatro food jokers. All carry the SMODS 'food' attribute, so they count as food
-- alongside vanilla food jokers (Ice Cream, Popcorn, ...).
--
-- G.GAME.donl_food_run_out counts Donlatro food jokers that ran out (destroyed by their
-- own effect) this run; Döner scales with it. It is saved with the run.

local function end_of_round(context)
    return context.end_of_round and context.main_eval and not context.blueprint and not context.game_over
end

local function food_run_out(card)
    G.GAME.donl_food_run_out = (G.GAME.donl_food_run_out or 0) + 1
    SMODS.destroy_cards(card, nil, nil, true)
end

local function other_food_held(card)
    for _, j in ipairs(G.jokers.cards) do
        if j ~= card and SMODS.has_attribute(j.config.center, 'food') then
            return true
        end
    end
    return false
end

-- 1) So(ß)e: +100 Chips, -5 per round. Destroyed at end of round if another food joker is held.
SMODS.Joker {
    key = 'sosse',
    atlas = 'Jokers',
    pos = { x = 2, y = 0 },
    rarity = 1,
    cost = 4,
    blueprint_compat = true,
    eternal_compat = false,
    attributes = { 'food' },
    config = { extra = { chips = 100, chip_mod = 5 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { card.ability.extra.chips, card.ability.extra.chip_mod } }
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        if context.joker_main then
            return { chips = stg.chips }
        end
        if end_of_round(context) then
            if other_food_held(card) then
                food_run_out(card)
                return { message = localize('k_donl_spilled'), colour = G.C.RED }
            end
            if stg.chips - stg.chip_mod <= 0 then
                food_run_out(card)
                return { message = localize('k_eaten_ex'), colour = G.C.RED }
            end
            stg.chips = stg.chips - stg.chip_mod
            return {
                message = localize { type = 'variable', key = 'a_chips_minus', vars = { stg.chip_mod } },
                colour = G.C.CHIPS,
            }
        end
    end,
}

-- 2) Döner: +10 Mult, +5 more per Donlatro food joker that ran out this run. 0 Mult while So(ß)e is held.
-- The gain is read from the definition (not the card) so Döners already in a run follow balance changes.
local DOENER_GAIN = 5

local function doener_mult(card)
    return card.ability.extra.mult + DOENER_GAIN * (G.GAME and G.GAME.donl_food_run_out or 0)
end

SMODS.Joker {
    key = 'doener',
    atlas = 'Jokers',
    pos = { x = 3, y = 0 },
    rarity = 2,
    cost = 6,
    blueprint_compat = true,
    attributes = { 'food' },
    config = { extra = { mult = 10 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { doener_mult(card), DOENER_GAIN } }
    end,
    calculate = function(self, card, context)
        if context.joker_main then
            if next(SMODS.find_card('j_donl_sosse')) then
                return { message = localize('k_donl_soggy'), colour = G.C.RED }
            end
            return { mult = doener_mult(card) }
        end
    end,
}

-- 3) HolyEnergy: starts at X1, gains X0.2 per round, destroyed once it reaches X2.
SMODS.Joker {
    key = 'holyenergy',
    atlas = 'Jokers',
    pos = { x = 4, y = 0 },
    rarity = 2,
    cost = 6,
    blueprint_compat = true,
    eternal_compat = false,
    attributes = { 'food' },
    config = { extra = { xmult = 1, gain = 0.2, limit = 2 } },
    loc_vars = function(self, info_queue, card)
        local stg = card.ability.extra
        return { vars = { stg.xmult, stg.gain, stg.limit } }
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        if context.joker_main and stg.xmult > 1 then
            return { xmult = stg.xmult }
        end
        if end_of_round(context) then
            -- round to 2 decimals so 1 + 5 * 0.2 lands exactly on 2
            stg.xmult = math.floor((stg.xmult + stg.gain) * 100 + 0.5) / 100
            if stg.xmult >= stg.limit then
                food_run_out(card)
                return { message = localize('k_drank_ex'), colour = G.C.RED }
            end
            return { message = localize { type = 'variable', key = 'a_xmult', vars = { stg.xmult } }, colour = G.C.MULT }
        end
    end,
}

-- 4) Maggi: +5 discards, -1 per round (like Drunkard, but running out).
SMODS.Joker {
    key = 'maggi',
    atlas = 'Jokers',
    pos = { x = 5, y = 0 },
    rarity = 2,
    cost = 6,
    blueprint_compat = false,
    eternal_compat = false,
    attributes = { 'food' },
    config = { extra = { discards = 5, discard_mod = 1 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { card.ability.extra.discards, card.ability.extra.discard_mod } }
    end,
    add_to_deck = function(self, card, from_debuff)
        G.GAME.round_resets.discards = G.GAME.round_resets.discards + card.ability.extra.discards
        ease_discard(card.ability.extra.discards)
    end,
    remove_from_deck = function(self, card, from_debuff)
        G.GAME.round_resets.discards = G.GAME.round_resets.discards - card.ability.extra.discards
        ease_discard(-card.ability.extra.discards)
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        if end_of_round(context) then
            if stg.discards - stg.discard_mod <= 0 then
                food_run_out(card)
                return { message = localize('k_eaten_ex'), colour = G.C.RED }
            end
            stg.discards = stg.discards - stg.discard_mod
            G.GAME.round_resets.discards = G.GAME.round_resets.discards - stg.discard_mod
            return {
                message = localize { type = 'variable', key = 'a_donl_discards_minus', vars = { stg.discard_mod } },
                colour = G.C.RED,
            }
        end
    end,
}

-- 5) Maultaschen: +5 hand size, -1 per round (like Turtle Bean).
SMODS.Joker {
    key = 'maultaschen',
    atlas = 'Jokers',
    pos = { x = 6, y = 0 },
    rarity = 2,
    cost = 6,
    blueprint_compat = false,
    eternal_compat = false,
    attributes = { 'food' },
    config = { extra = { h_size = 5, h_mod = 1 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { card.ability.extra.h_size, card.ability.extra.h_mod } }
    end,
    add_to_deck = function(self, card, from_debuff)
        G.hand:change_size(card.ability.extra.h_size)
    end,
    remove_from_deck = function(self, card, from_debuff)
        G.hand:change_size(-card.ability.extra.h_size)
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        if end_of_round(context) then
            if stg.h_size - stg.h_mod <= 0 then
                food_run_out(card)
                return { message = localize('k_eaten_ex'), colour = G.C.RED }
            end
            stg.h_size = stg.h_size - stg.h_mod
            G.hand:change_size(-stg.h_mod)
            return {
                message = localize { type = 'variable', key = 'a_handsize_minus', vars = { stg.h_mod } },
                colour = G.C.FILTER,
            }
        end
    end,
}

-- 6) Sauerteigbrot: doubles its own sell value each round; 1 in 4 chance to be destroyed instead.
SMODS.Joker {
    key = 'sauerteigbrot',
    atlas = 'Jokers',
    pos = { x = 7, y = 0 },
    rarity = 1,
    cost = 5,
    blueprint_compat = false,
    eternal_compat = false,
    attributes = { 'food' },
    config = { extra = { odds = 4 } },
    loc_vars = function(self, info_queue, card)
        local num, den = SMODS.get_probability_vars(card, 1, card.ability.extra.odds, 'donl_sauerteigbrot')
        return { vars = { num, den } }
    end,
    calculate = function(self, card, context)
        if end_of_round(context) then
            if SMODS.pseudorandom_probability(card, 'donl_sauerteigbrot', 1, card.ability.extra.odds) then
                food_run_out(card)
                return { message = localize('k_eaten_ex'), colour = G.C.RED }
            end
            -- double the base sell value (before TrekTrendy's multiplier, so they don't compound)
            local base_sell = math.max(1, math.floor(card.cost / 2)) + (card.ability.extra_value or 0)
            card.ability.extra_value = (card.ability.extra_value or 0) + base_sell
            card:set_cost()
            return { message = localize('k_val_up'), colour = G.C.MONEY }
        end
    end,
}

-- 7) Frustsuppe: +100 Chips, +30 Mult, X2 Mult - but while held, every way of earning money
-- pays $0 (interest, blind rewards, selling, Gold cards, ...). Selling it counts for Döner.
SMODS.Joker {
    key = 'frustsuppe',
    atlas = 'Jokers',
    pos = { x = 1, y = 1 },
    rarity = 3,
    cost = 8,
    blueprint_compat = true,
    eternal_compat = false,
    attributes = { 'food' },
    config = { extra = { chips = 100, mult = 30, xmult = 2 } },
    loc_vars = function(self, info_queue, card)
        local stg = card.ability.extra
        return { vars = { stg.chips, stg.mult, stg.xmult } }
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        if context.joker_main then
            return { chips = stg.chips, mult = stg.mult, xmult = stg.xmult }
        end
        if context.selling_self and not context.blueprint then
            G.GAME.donl_food_run_out = (G.GAME.donl_food_run_out or 0) + 1
        end
    end,
}

local ease_dollars_ref = ease_dollars
function ease_dollars(mod, instant)
    if type(mod) == 'number' and mod > 0 and G.jokers and next(SMODS.find_card('j_donl_frustsuppe')) then
        -- tell SMODS nothing was paid, so its "+$X" text and money_altered context say $0
        if SMODS.ease_dollars_calc then SMODS.dollars_changed = 0 end
        return
    end
    return ease_dollars_ref(mod, instant)
end

-- 8) Shepherd's Pie: feeds the flock - every scored card permanently gains +1 Mult.
-- 3 portions, one eaten at the end of each round.
SMODS.Joker {
    key = 'shepherds_pie',
    atlas = 'Jokers',
    pos = { x = 2, y = 1 },
    rarity = 1,
    cost = 5,
    blueprint_compat = true,
    eternal_compat = false,
    attributes = { 'food' },
    config = { extra = { perma_mult = 1, portions = 3 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { card.ability.extra.perma_mult, card.ability.extra.portions } }
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        if context.individual and context.cardarea == G.play then
            local c = context.other_card
            c.ability.perma_mult = (c.ability.perma_mult or 0) + stg.perma_mult
            return { message = localize('k_upgrade_ex'), colour = G.C.MULT, message_card = c }
        end
        if end_of_round(context) then
            if stg.portions - 1 <= 0 then
                food_run_out(card)
                return { message = localize('k_eaten_ex'), colour = G.C.RED }
            end
            stg.portions = stg.portions - 1
            return { message = localize { type = 'variable', key = 'a_donl_portions_left', vars = { stg.portions } }, colour = G.C.FILTER }
        end
    end,
}

-- 9) Bierbrunnen: each scored card has a 1 in 5 chance to become a Gold card.
-- Runs dry (destroyed) after converting 5 cards.
SMODS.Joker {
    key = 'bierbrunnen',
    atlas = 'Jokers',
    pos = { x = 3, y = 1 },
    rarity = 2,
    cost = 6,
    blueprint_compat = false,
    eternal_compat = false,
    attributes = { 'food' },
    config = { extra = { odds = 5, converted = 0, limit = 5 } },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_gold
        local stg = card.ability.extra
        local num, den = SMODS.get_probability_vars(card, 1, stg.odds, 'donl_bierbrunnen')
        return { vars = { num, den, stg.limit, stg.limit - stg.converted } }
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        if context.before and not context.blueprint then
            local poured = 0
            for _, c in ipairs(context.scoring_hand) do
                if stg.converted >= stg.limit then break end
                if not SMODS.has_enhancement(c, 'm_gold')
                    and SMODS.pseudorandom_probability(card, 'donl_bierbrunnen', 1, stg.odds) then
                    c:set_ability(G.P_CENTERS.m_gold, nil, true)
                    G.E_MANAGER:add_event(Event({ func = function() c:juice_up(); return true end }))
                    stg.converted = stg.converted + 1
                    poured = poured + 1
                end
            end
            if poured > 0 then
                return { message = localize('k_gold'), colour = G.C.MONEY }
            end
        end
        if context.after and not context.blueprint and stg.converted >= stg.limit then
            food_run_out(card)
            return { message = localize('k_donl_empty'), colour = G.C.RED }
        end
    end,
}

-- 10) Kaffee: +1 discard once, for the next round played after buying it. At end of every
-- round it costs $4; if you can't pay, it's gone.
SMODS.Joker {
    key = 'kaffee',
    atlas = 'Jokers',
    pos = { x = 3, y = 2 },
    rarity = 1,
    cost = 4,
    blueprint_compat = false,
    eternal_compat = false,
    attributes = { 'food' },
    config = { extra = { discards = 1, price = 4, once = true, pending = true } },
    loc_vars = function(self, info_queue, card)
        return { vars = { card.ability.extra.discards, card.ability.extra.price } }
    end,
    add_to_deck = function(self, card, from_debuff)
        -- bought mid-blind: the boost applies to the current round right away
        local stg = card.ability.extra
        if not from_debuff and stg.pending and G.GAME.blind and G.GAME.blind.in_blind then
            stg.pending = false
            ease_discard(stg.discards)
        end
    end,
    remove_from_deck = function(self, card, from_debuff)
        -- Kaffees bought before this change added a permanent +1 discard; take it back
        if not card.ability.extra.once then
            G.GAME.round_resets.discards = G.GAME.round_resets.discards - card.ability.extra.discards
            ease_discard(-card.ability.extra.discards)
        end
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        if context.setting_blind and stg.once and stg.pending and not context.blueprint then
            stg.pending = false
            ease_discard(stg.discards)
            return { message = localize { type = 'variable', key = 'a_donl_discards_plus', vars = { stg.discards } }, colour = G.C.RED }
        end
        if end_of_round(context) then
            if G.GAME.dollars < stg.price then
                food_run_out(card)
                return { message = localize('k_donl_empty'), colour = G.C.RED }
            end
            return { dollars = -stg.price }
        end
    end,
}
