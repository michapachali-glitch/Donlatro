-- Donlatro vouchers (assets/{1x,2x}/Vouchers.png: tier 1 on row 0, tier 2 on row 1).
SMODS.Atlas {
    key = 'Vouchers',
    path = 'Vouchers.png',
    px = 71,
    py = 95,
}

local function redeemed(key)
    return G.GAME and G.GAME.used_vouchers and G.GAME.used_vouchers[key]
end

-- Patreon / Patreon Exklusiv ------------------------------------------------------------
SMODS.Voucher {
    key = 'patreon',
    atlas = 'Vouchers',
    pos = { x = 0, y = 0 },
    config = { extra = { dollars = 2 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { self.config.extra.dollars } }
    end,
    calc_dollar_bonus = function(self, card)
        if redeemed('v_donl_patreon_exklusiv') or #G.jokers.cards == 0 then return end
        return self.config.extra.dollars * #G.jokers.cards
    end,
}

-- one shop item per Ante is free: mark a random shop card as couponed until it is bought
local function ensure_freebie()
    if not G.shop_jokers or G.GAME.donl_free_ante == G.GAME.round_resets.ante then return end
    for _, c in ipairs(G.shop_jokers.cards) do
        if c.ability.donl_freebie then return end
    end
    if not G.shop_jokers.cards[1] then return end
    local c = pseudorandom_element(G.shop_jokers.cards, pseudoseed('donl_patreon'))
    c.ability.couponed = true
    c.ability.donl_freebie = true
    c:set_cost()
    c:juice_up()
end

SMODS.Voucher {
    key = 'patreon_exklusiv',
    atlas = 'Vouchers',
    pos = { x = 0, y = 1 },
    requires = { 'v_donl_patreon' },
    config = { extra = { dollars = 4 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { self.config.extra.dollars } }
    end,
    redeem = function(self, card)
        G.E_MANAGER:add_event(Event({ func = function() ensure_freebie(); return true end }))
    end,
    calc_dollar_bonus = function(self, card)
        if #G.jokers.cards == 0 then return end
        return self.config.extra.dollars * #G.jokers.cards
    end,
    calculate = function(self, card, context)
        if context.starting_shop or context.reroll_shop then
            G.E_MANAGER:add_event(Event({ func = function() ensure_freebie(); return true end }))
        end
        if context.buying_card and context.card and context.card.ability.donl_freebie then
            G.GAME.donl_free_ante = G.GAME.round_resets.ante
        end
    end,
}

-- Therapieplatz / Kassenzulassung: free Boss rerolls (button patched in via lovely.toml) --
SMODS.Voucher {
    key = 'therapieplatz',
    atlas = 'Vouchers',
    pos = { x = 1, y = 0 },
}

SMODS.Voucher {
    key = 'kassenzulassung',
    atlas = 'Vouchers',
    pos = { x = 1, y = 1 },
    requires = { 'v_donl_therapieplatz' },
}

local function free_boss_reroll()
    if redeemed('v_donl_kassenzulassung') then return true end
    return redeemed('v_donl_therapieplatz') and not G.GAME.round_resets.boss_rerolled
end

local reroll_boss_button_ref = G.FUNCS.reroll_boss_button
G.FUNCS.reroll_boss_button = function(e)
    if not free_boss_reroll() then
        return reroll_boss_button_ref(e)
    end
    e.config.colour = G.C.RED
    e.config.button = 'reroll_boss'
    e.children[1].children[1].config.shadow = true
    if e.children[2] then e.children[2].children[1].config.shadow = true end
end

local reroll_boss_ref = G.FUNCS.reroll_boss
G.FUNCS.reroll_boss = function(e)
    if free_boss_reroll() then
        G.from_boss_tag = true -- vanilla's "this reroll is free" flag (Boss Tag)
    end
    return reroll_boss_ref(e)
end

-- Medikinet / Elvanse ------------------------------------------------------------------
SMODS.Voucher {
    key = 'medikinet',
    atlas = 'Vouchers',
    pos = { x = 2, y = 0 },
    config = { extra = { h_size = 1 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { self.config.extra.h_size } }
    end,
    redeem = function(self, card)
        G.hand:change_size(self.config.extra.h_size)
    end,
}

local function own_debuff(card)
    for _, v in pairs(card.ability.debuff_sources or {}) do
        if v then return true end
    end
    return card.ability.perishable and (card.ability.perish_tally or 1) <= 0
end

SMODS.Voucher {
    key = 'elvanse',
    atlas = 'Vouchers',
    pos = { x = 2, y = 1 },
    requires = { 'v_donl_medikinet' },
    config = { extra = { h_size = 1 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { self.config.extra.h_size } }
    end,
    redeem = function(self, card)
        G.hand:change_size(self.config.extra.h_size)
        for _, j in ipairs(G.jokers.cards) do SMODS.recalc_debuff(j) end
    end,
    calculate = function(self, card, context)
        -- Blinds can't debuff Jokers (Perishable, Unsicherheit, O'Sullivan still can)
        local c = context.debuff_card
        if c and c.ability and c.ability.set == 'Joker' and not own_debuff(c) then
            return { prevent_debuff = true }
        end
    end,
}

-- ...and Blinds can't shuffle them (Amber Acorn). Donlatro's own shuffles set allow_joker_shuffle.
local shuffle_ref = CardArea.shuffle
function CardArea:shuffle(seed)
    if self == G.jokers and redeemed('v_donl_elvanse') and not DONLATRO.allow_joker_shuffle then
        return
    end
    return shuffle_ref(self, seed)
end

-- Schönhauser Allee Arcaden / Das ganze Erdgeschoss ------------------------------------
SMODS.Voucher {
    key = 'arcaden',
    atlas = 'Vouchers',
    pos = { x = 3, y = 0 },
    redeem = function(self, card)
        G.E_MANAGER:add_event(Event({ func = function() change_shop_size(1); return true end }))
    end,
}

SMODS.Voucher {
    key = 'erdgeschoss',
    atlas = 'Vouchers',
    pos = { x = 3, y = 1 },
    requires = { 'v_donl_arcaden' },
    redeem = function(self, card)
        G.E_MANAGER:add_event(Event({ func = function() change_shop_size(1); return true end }))
        SMODS.change_voucher_limit(1)
    end,
}

-- Superrampe / Mini-Superrampe in der Superrampe ---------------------------------------
SMODS.Voucher {
    key = 'superrampe',
    atlas = 'Vouchers',
    pos = { x = 4, y = 0 },
    config = { extra = { discards = 1 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { self.config.extra.discards } }
    end,
    redeem = function(self, card)
        G.GAME.round_resets.discards = G.GAME.round_resets.discards + self.config.extra.discards
        ease_discard(self.config.extra.discards)
    end,
}

SMODS.Voucher {
    key = 'mini_superrampe',
    atlas = 'Vouchers',
    pos = { x = 4, y = 1 },
    requires = { 'v_donl_superrampe' },
    config = { extra = { discards = 1, chips = 5 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { self.config.extra.discards, self.config.extra.chips, G.GAME and G.GAME.donl_rampe_chips or 0 } }
    end,
    redeem = function(self, card)
        G.GAME.round_resets.discards = G.GAME.round_resets.discards + self.config.extra.discards
        ease_discard(self.config.extra.discards)
    end,
    calculate = function(self, card, context)
        if context.discard then
            G.GAME.donl_rampe_chips = (G.GAME.donl_rampe_chips or 0) + self.config.extra.chips
        end
        if context.joker_main and (G.GAME.donl_rampe_chips or 0) > 0 then
            local chips = G.GAME.donl_rampe_chips
            G.GAME.donl_rampe_chips = 0
            return { chips = chips }
        end
    end,
}
