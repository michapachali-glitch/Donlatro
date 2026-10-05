SMODS.Joker {
    key = 'daunendonnie',
    atlas = 'Jokers',
    pos = { x = 0, y = 0 },
    rarity = 2,
    cost = 6,
    blueprint_compat = true,
    config = { extra = { chips = 0, gain = 2 } },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.e_foil
        return { vars = { card.ability.extra.gain, card.ability.extra.chips } }
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        -- permanently +2 Chips for every played card that doesn't score
        if context.before and not context.blueprint then
            local unscored = 0
            for _, c in ipairs(context.full_hand) do
                if not SMODS.in_scoring(c, context.scoring_hand) then unscored = unscored + 1 end
            end
            if unscored > 0 then
                stg.chips = stg.chips + stg.gain * unscored
                return { message = localize('k_upgrade_ex'), colour = G.C.CHIPS }
            end
        end
        if context.joker_main and stg.chips > 0 then
            return { chips = stg.chips }
        end
        -- Foil only while a Boss Blind is being played
        if context.setting_blind and not context.blueprint and G.GAME.blind.boss then
            stg.boss_foil = true
            card:set_edition('e_foil', true)
        end
        if context.end_of_round and context.main_eval and not context.blueprint and stg.boss_foil then
            stg.boss_foil = nil
            card:set_edition(nil, true)
        end
    end,
}

-- Daunendonnie's edition is locked: Foil during Boss Blinds, none otherwise
-- (shop rolls, Aura, Ectoplasm, Wheel of Fortune can't give it another edition).
local set_edition_ref = Card.set_edition
function Card:set_edition(edition, ...)
    if self.config and self.config.center and self.config.center.key == 'j_donl_daunendonnie' then
        local stg = self.ability and self.ability.extra
        edition = (type(stg) == 'table' and stg.boss_foil) and 'e_foil' or nil
    end
    return set_edition_ref(self, edition, ...)
end

-- TrekTrendy: while held, doubles the sell value of every card (including itself).
-- Multiple copies stack (x2 each). The doubling lives in Card:set_sell_value, so it
-- also applies to anything that recalculates its value later (Egg, Gift Card, ...).
local function trektrendy_count()
    if not G.jokers then return 0 end
    local n = 0
    for _, c in ipairs(G.jokers.cards) do
        if c.config.center.key == 'j_donl_trektrendy' and not c.debuff and not c.donl_inactive then
            n = n + 1
        end
    end
    return n
end

local set_sell_value_ref = Card.set_sell_value
function Card:set_sell_value()
    set_sell_value_ref(self)
    local n = trektrendy_count()
    if n > 0 then
        self.sell_cost = self.sell_cost * 2 ^ n
    end
end

-- Recalculate owned cards once TrekTrendy has actually entered/left the joker area.
local function refresh_sell_values()
    G.E_MANAGER:add_event(Event({
        func = function()
            for _, area in ipairs({ G.jokers, G.consumeables }) do
                for _, c in ipairs(area and area.cards or {}) do
                    c:set_cost()
                end
            end
            return true
        end,
    }))
end

SMODS.Joker {
    key = 'trektrendy',
    atlas = 'Jokers',
    pos = { x = 1, y = 0 },
    rarity = 2,
    cost = 6,
    blueprint_compat = false,
    add_to_deck = function(self, card, from_debuff)
        card.donl_inactive = nil
        refresh_sell_values()
    end,
    remove_from_deck = function(self, card, from_debuff)
        card.donl_inactive = true
        refresh_sell_values()
    end,
}

-- Bähnle (Tübinger Bähnle): +2 Mult each time a Gold card pays out while held in hand
-- at end of round. Mime retriggers count as extra payouts.
SMODS.Joker {
    key = 'baehnle',
    atlas = 'Jokers',
    pos = { x = 8, y = 0 },
    rarity = 1,
    cost = 5,
    blueprint_compat = true,
    perishable_compat = false,
    config = { extra = { mult = 0, gain = 2 } },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_gold
        return { vars = { card.ability.extra.gain, card.ability.extra.mult } }
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        if context.joker_main and stg.mult > 0 then
            return { mult = stg.mult }
        end
        if context.individual and context.end_of_round and context.cardarea == G.hand
            and not context.blueprint and not context.other_card.debuff
            and SMODS.has_enhancement(context.other_card, 'm_gold') then
            stg.mult = stg.mult + stg.gain
            return { message = localize('k_upgrade_ex'), colour = G.C.MULT, message_card = card }
        end
    end,
}

-- Erdie Feuermann: when sold, removes every sticker (Eternal, Perishable, Rental, ...) from
-- all other held jokers. Perishable-expired jokers get un-debuffed, rentals get normal prices.
SMODS.Joker {
    key = 'erdie',
    atlas = 'Jokers',
    pos = { x = 9, y = 0 },
    rarity = 2,
    cost = 6,
    blueprint_compat = false,
    eternal_compat = false,
    calculate = function(self, card, context)
        if context.selling_self and not context.blueprint then
            for _, j in ipairs(G.jokers.cards) do
                if j ~= card then
                    for key in pairs(SMODS.Stickers) do
                        if key ~= 'donl_layers' then -- layered editions aren't a real sticker
                            j:remove_sticker(key)
                        end
                    end
                    SMODS.recalc_debuff(j)
                    j:set_cost()
                end
            end
            return { message = localize('k_donl_extinguished'), colour = G.C.FILTER }
        end
    end,
}

-- Nolan: a Straight played in descending order (e.g. 6-5-4-3-2) raises his sell value by $5.
-- Once it reaches $20 (from $5): -1 Ante, then Nolan is destroyed.
local function is_descending_run(cards)
    if #cards < 2 then return false end
    for i = 2, #cards do
        local prev, cur = cards[i - 1]:get_id(), cards[i]:get_id()
        local ace_low = cur == 14 and i == #cards and prev == 2 -- 5-4-3-2-A
        if not (cur < prev or ace_low) then return false end
    end
    return true
end

SMODS.Joker {
    key = 'nolan',
    atlas = 'Jokers',
    pos = { x = 0, y = 1 },
    rarity = 2,
    cost = 10, -- sells for $5
    blueprint_compat = false,
    eternal_compat = false,
    config = { extra = { value = 5, gain = 5, limit = 20, ante = 1 } },
    loc_vars = function(self, info_queue, card)
        local stg = card.ability.extra
        return { vars = { stg.gain, stg.limit, stg.ante, stg.value } }
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        if context.before and not context.blueprint and next(context.poker_hands['Straight'])
            and is_descending_run(context.scoring_hand) then
            stg.value = stg.value + stg.gain
            card.ability.extra_value = (card.ability.extra_value or 0) + stg.gain
            card:set_cost()
            if stg.value >= stg.limit then
                ease_ante(-stg.ante)
                G.GAME.round_resets.blind_ante = (G.GAME.round_resets.blind_ante or G.GAME.round_resets.ante) - stg.ante
                SMODS.destroy_cards(card)
                return { message = localize { type = 'variable', key = 'a_donl_ante_minus', vars = { stg.ante } }, colour = G.C.FILTER }
            end
            return { message = localize('k_val_up'), colour = G.C.MONEY }
        end
    end,
}

-- Jochen (Steuerberater): adds a "Jochen" row to the cash-out screen with a random amount
-- between -$5 and +$15. Like Golden Joker, the money only moves when you press Cash Out.
SMODS.Joker {
    key = 'jochen',
    atlas = 'Jokers',
    pos = { x = 4, y = 1 },
    rarity = 1,
    cost = 6,
    blueprint_compat = false,
    config = { extra = { min = -5, max = 15 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { -card.ability.extra.min, card.ability.extra.max } }
    end,
    calc_dollar_bonus = function(self, card)
        local amount = pseudorandom('donl_jochen', card.ability.extra.min, card.ability.extra.max)
        if amount ~= 0 then -- 0 would still draw an empty row (0 is truthy in Lua)
            return amount
        end
    end,
}

-- UDK Abschlussarbeit: if every scored card is an Ace, X1 Mult per scored Ace.
SMODS.Joker {
    key = 'udk',
    atlas = 'Jokers',
    pos = { x = 5, y = 1 },
    rarity = 2,
    cost = 7,
    blueprint_compat = true,
    calculate = function(self, card, context)
        if context.joker_main then
            local aces = 0
            for _, c in ipairs(context.scoring_hand) do
                if c:get_id() ~= 14 then return end
                aces = aces + 1
            end
            if aces > 1 then
                return { xmult = aces }
            end
        end
    end,
}

-- Die Rampe: X0.25 Mult per discard used this round (uses the round's own discard
-- counter, so it resets by itself when the next round starts).
SMODS.Joker {
    key = 'rampe',
    atlas = 'Jokers',
    pos = { x = 6, y = 1 },
    rarity = 3,
    cost = 8,
    blueprint_compat = true,
    config = { extra = { gain = 0.25 } },
    loc_vars = function(self, info_queue, card)
        local used = G.GAME and G.GAME.current_round and G.GAME.current_round.discards_used or 0
        return { vars = { card.ability.extra.gain, 1 + card.ability.extra.gain * used } }
    end,
    calculate = function(self, card, context)
        if context.joker_main then
            local xmult = 1 + card.ability.extra.gain * G.GAME.current_round.discards_used
            if xmult > 1 then
                return { xmult = xmult }
            end
        end
    end,
}

-- Classic Donnie: retriggers played cards whose rank was also played in the previous hand
-- this round (the hand history is tracked in src/tracking.lua).
SMODS.Joker {
    key = 'classic_donnie',
    atlas = 'Jokers',
    pos = { x = 7, y = 1 },
    rarity = 3,
    cost = 8,
    blueprint_compat = true,
    calculate = function(self, card, context)
        if context.repetition and context.cardarea == G.play then
            if DONLATRO.previous_hand_ranks()[context.other_card:get_id()] then
                return { repetitions = 1 }
            end
        end
    end,
}

-- Ihr checkt schon, was ich meine: 4-card Flushes count, and so do Straights that are
-- exactly one card short (4 of the 5 ranks present, e.g. 4-5-6-7 or 4-5-7-8).
SMODS.Joker {
    key = 'ihr_checkt',
    atlas = 'Jokers',
    pos = { x = 8, y = 1 },
    rarity = 3,
    cost = 8,
    blueprint_compat = false,
}

local function checkt_held()
    return G.jokers and next(SMODS.find_card('j_donl_ihr_checkt'))
end

local four_fingers_ref = SMODS.four_fingers
function SMODS.four_fingers(hand_type)
    local n = four_fingers_ref(hand_type)
    if hand_type == 'flush' and checkt_held() then
        return math.min(n, 4)
    end
    return n
end

local function one_short_straight(hand)
    local best
    for low = 1, 10 do -- windows A-5 (ace low) up to 10-A
        local present, cards = {}, {}
        for _, c in ipairs(hand) do
            local id = c:get_id()
            local r = (id == 14 and low == 1) and 1 or id
            if r >= low and r <= low + 4 then
                present[r] = true
                cards[#cards + 1] = c
            end
        end
        local count = 0
        for _ in pairs(present) do count = count + 1 end
        if count >= 4 and (not best or count > best.count) then
            best = { count = count, cards = cards }
        end
    end
    return best and { best.cards } or {}
end

local straight_part = SMODS.PokerHandParts['_straight']
local straight_func_ref = straight_part.func
straight_part.func = function(hand)
    local res = straight_func_ref(hand)
    if next(res) or not checkt_held() then
        return res
    end
    return one_short_straight(hand)
end

-- DübelDonnie: permanently gains +1 Mult every time a High Card is played.
-- Also: every scored Stoned Card (vanilla Stone Card, renamed) has a 1 in 4 chance to create
-- a Negative Wheel of Fortune, which can stack up to 3 editions on one Joker.
-- Keeps the old 'anyway' key so jokers in existing saves still load. The gain is read from
-- here (not the card) so copies bought before the rework follow the new balance.
local DUEBEL_GAIN = 1
local DUEBEL_WHEEL_ODDS = 4

-- Negative, so it never needs a free consumable slot. A Negative Wheel can stack editions
-- (see src/layered_editions.lua).
local function create_wheel_of_fortune()
    G.E_MANAGER:add_event(Event({
        func = function()
            SMODS.add_card({ key = 'c_wheel_of_fortune', edition = 'e_negative' })
            return true
        end,
    }))
    return true
end

SMODS.Joker {
    key = 'anyway',
    atlas = 'Jokers',
    pos = { x = 9, y = 1 },
    rarity = 2,
    cost = 6,
    blueprint_compat = true,
    perishable_compat = false,
    config = { extra = { mult = 0 } },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_stone
        info_queue[#info_queue + 1] = G.P_CENTERS.c_wheel_of_fortune
        info_queue[#info_queue + 1] = { set = 'Other', key = 'donl_negative_wheel' }
        local num, den = SMODS.get_probability_vars(card, 1, DUEBEL_WHEEL_ODDS, 'donl_duebel_wheel')
        return { vars = { DUEBEL_GAIN, card.ability.extra.mult, num, den } }
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        if context.individual and context.cardarea == G.play and not context.blueprint
            and SMODS.has_enhancement(context.other_card, 'm_stone')
            and SMODS.pseudorandom_probability(card, 'donl_duebel_wheel', 1, DUEBEL_WHEEL_ODDS)
            and create_wheel_of_fortune() then
            return { message = localize('k_plus_tarot'), colour = G.C.PURPLE, message_card = card }
        end
        if context.before and not context.blueprint and context.scoring_name == 'High Card' then
            stg.mult = stg.mult + DUEBEL_GAIN
            return { message = localize('k_upgrade_ex'), colour = G.C.MULT }
        end
        if context.joker_main and stg.mult > 0 then
            return { mult = stg.mult }
        end
    end,
}

-- Der Akkuschrauber: a recharging battery. Charges +6 Mult and +15 Chips at the end of
-- every round. Beating a Boss Blind discharges it: earn $1 per 2 stored Mult, then the charge
-- resets to 0 and it keeps going. Never destroyed. Gains are read from here (not the card)
-- so copies already in a run follow balance changes.
local AKKU_MULT, AKKU_CHIPS = 6, 15

SMODS.Joker {
    key = 'akkuschrauber',
    atlas = 'Jokers',
    pos = { x = 1, y = 2 },
    rarity = 1,
    cost = 4,
    blueprint_compat = true,
    perishable_compat = false,
    config = { extra = { mult = 0, chips = 0 } },
    loc_vars = function(self, info_queue, card)
        local stg = card.ability.extra
        return { vars = { AKKU_MULT, AKKU_CHIPS, stg.mult or 0, stg.chips or 0 } }
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        stg.mult, stg.chips = stg.mult or 0, stg.chips or 0 -- copies from before the rework
        if context.joker_main and (stg.mult > 0 or stg.chips > 0) then
            return { mult = stg.mult > 0 and stg.mult or nil, chips = stg.chips > 0 and stg.chips or nil }
        end
        if context.end_of_round and context.main_eval and not context.blueprint and not context.game_over then
            stg.mult = stg.mult + AKKU_MULT
            stg.chips = stg.chips + AKKU_CHIPS
            if context.beat_boss then
                local payout = math.floor(stg.mult / 2)
                stg.mult, stg.chips = 0, 0
                return { dollars = payout, message = localize('k_donl_battery_empty'), colour = G.C.MONEY }
            end
            return { message = localize('k_donl_charging'), colour = G.C.FILTER }
        end
    end,
}

-- Buttplugs bei Butlers: played cards are retriggered once for every hand already
-- played this round (2nd hand: +1, 3rd hand: +2, ...).
SMODS.Joker {
    key = 'butlers',
    atlas = 'Jokers',
    pos = { x = 2, y = 2 },
    rarity = 2,
    cost = 6,
    blueprint_compat = true,
    loc_vars = function(self, info_queue, card)
        local played = G.GAME and G.GAME.current_round and G.GAME.current_round.hands_played or 0
        return { vars = { played } }
    end,
    calculate = function(self, card, context)
        if context.repetition and context.cardarea == G.play then
            local n = G.GAME.current_round.hands_played
            if n > 0 then
                return { repetitions = n }
            end
        end
    end,
}

-- Donnie O'Sullivan (Legendary, The Soul only): X6.9 Mult. At end of round, 1 in 4 chance
-- he loses the thread and is debuffed for the following round (lifted in src/tracking.lua).
SMODS.Joker {
    key = 'osullivan',
    atlas = 'Jokers',
    pos = { x = 4, y = 2 },
    soul_pos = { x = 5, y = 2 },
    rarity = 4,
    cost = 20,
    blueprint_compat = true,
    config = { extra = { xmult = 6.9, odds = 4 } },
    loc_vars = function(self, info_queue, card)
        local num, den = SMODS.get_probability_vars(card, 1, card.ability.extra.odds, 'donl_osullivan')
        return { vars = { card.ability.extra.xmult, num, den } }
    end,
    calculate = function(self, card, context)
        local stg = card.ability.extra
        if context.joker_main then
            return { xmult = stg.xmult }
        end
        if context.end_of_round and context.main_eval and not context.blueprint and not context.game_over
            and SMODS.pseudorandom_probability(card, 'donl_osullivan', 1, stg.odds) then
            stg.off_round = G.GAME.round + 1
            SMODS.debuff_card(card, true, 'donl_thread')
            return { message = localize('k_donl_lost_thread'), colour = G.C.RED }
        end
    end,
}
