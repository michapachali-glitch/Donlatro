-- Donlatro tarots and spectrals (assets/{1x,2x}/Consumables.png, one row).
SMODS.Atlas {
    key = 'Consumables',
    path = 'Consumables.png',
    px = 71,
    py = 95,
}

-- Tarot: Classic Donnie - copy 1 selected card into your deck.
SMODS.Consumable {
    key = 'classic_donnie',
    set = 'Tarot',
    atlas = 'Consumables',
    pos = { x = 0, y = 0 },
    config = { max_highlighted = 1 },
    can_use = function(self, card)
        return G.hand and #G.hand.highlighted == 1
    end,
    use = function(self, card, area, copier)
        local orig = G.hand.highlighted[1]
        G.E_MANAGER:add_event(Event({
            func = function()
                G.playing_card = (G.playing_card and G.playing_card + 1) or 1
                local c = copy_card(orig, nil, nil, G.playing_card)
                c:add_to_deck()
                G.deck.config.card_limit = G.deck.config.card_limit + 1
                table.insert(G.playing_cards, c)
                G.hand:emplace(c)
                c:start_materialize()
                SMODS.calculate_context({ playing_card_added = true, cards = { c } })
                return true
            end,
        }))
    end,
}

-- Tarot: Die Therapie - strip debuffs, edition and enhancement from 1 selected card, pay $2.
SMODS.Consumable {
    key = 'therapie',
    set = 'Tarot',
    atlas = 'Consumables',
    pos = { x = 1, y = 0 },
    config = { max_highlighted = 1, extra = { dollars = 2 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { self.config.extra.dollars } }
    end,
    can_use = function(self, card)
        return G.hand and #G.hand.highlighted == 1
    end,
    use = function(self, card, area, copier)
        local target = G.hand.highlighted[1]
        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.2,
            func = function()
                target:flip()
                play_sound('tarot1')
                return true
            end,
        }))
        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.3,
            func = function()
                target:set_ability(G.P_CENTERS.c_base, nil, true)
                target:set_edition(nil, true, true)
                target.ability.debuff_sources = {}
                SMODS.recalc_debuff(target)
                target:flip()
                play_sound('tarot2')
                return true
            end,
        }))
        ease_dollars(-self.config.extra.dollars)
    end,
}

-- Spectral: Die Rückspultaste - restore the deck as it was at the start of this Ante, lose all money.
SMODS.Consumable {
    key = 'rueckspultaste',
    set = 'Spectral',
    atlas = 'Consumables',
    pos = { x = 2, y = 0 },
    can_use = function(self, card)
        -- an empty snapshot would wipe the deck and softlock the run
        return G.GAME.donl_ante_snapshot and G.GAME.donl_ante_snapshot[1]
            and not (G.GAME.blind and G.GAME.blind.in_blind)
    end,
    use = function(self, card, area, copier)
        G.E_MANAGER:add_event(Event({
            func = function()
                local old = {}
                for i, c in ipairs(G.playing_cards) do old[i] = c end
                for _, c in ipairs(old) do
                    c:remove()
                end
                for _, saved in ipairs(G.GAME.donl_ante_snapshot) do
                    -- skip cards whose enhancement no longer exists (e.g. a mod was removed)
                    if saved.save_fields and G.P_CENTERS[saved.save_fields.center] then
                        local c = Card(G.deck.T.x, G.deck.T.y, G.CARD_W, G.CARD_H, G.P_CARDS.empty, G.P_CENTERS.c_base)
                        c:load(copy_table(saved))
                        G.deck:emplace(c)
                        table.insert(G.playing_cards, c)
                    end
                end
                G.deck.config.card_limit = #G.playing_cards
                play_sound('timpani')
                return true
            end,
        }))
        if G.GAME.dollars > 0 then
            ease_dollars(-G.GAME.dollars, true)
        end
    end,
}

-- Spectral: Eingeschissen - a random Joker without edition becomes Negative,
-- and a random card in your deck is destroyed.
local function plain_jokers()
    local t = {}
    for _, j in ipairs(G.jokers and G.jokers.cards or {}) do
        if not j.edition then t[#t + 1] = j end
    end
    return t
end

SMODS.Consumable {
    key = 'eingeschissen',
    set = 'Spectral',
    atlas = 'Consumables',
    pos = { x = 3, y = 0 },
    can_use = function(self, card)
        return #plain_jokers() > 0 and G.playing_cards and #G.playing_cards > 0
    end,
    use = function(self, card, area, copier)
        local joker = pseudorandom_element(plain_jokers(), pseudoseed('donl_eingeschissen_j'))
        local victim = pseudorandom_element(G.playing_cards, pseudoseed('donl_eingeschissen_c'))
        G.E_MANAGER:add_event(Event({
            func = function()
                joker:set_edition('e_negative', true)
                return true
            end,
        }))
        SMODS.destroy_cards(victim)
    end,
}

-- Spectral: Die Unsicherheit - +1 Joker slot, but all current Jokers are debuffed for one
-- full round (lifted in src/tracking.lua).
SMODS.Consumable {
    key = 'unsicherheit',
    set = 'Spectral',
    atlas = 'Consumables',
    pos = { x = 4, y = 0 },
    config = { extra = { slots = 1 } },
    loc_vars = function(self, info_queue, card)
        return { vars = { self.config.extra.slots } }
    end,
    can_use = function(self, card)
        return true
    end,
    use = function(self, card, area, copier)
        G.jokers.config.card_limit = G.jokers.config.card_limit + self.config.extra.slots
        for _, j in ipairs(G.jokers.cards) do
            SMODS.debuff_card(j, true, 'donl_unsicher')
        end
        G.GAME.donl_unsicher_until = G.GAME.round + 1
    end,
}
