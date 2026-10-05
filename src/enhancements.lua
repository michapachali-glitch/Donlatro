-- Rampen-Karte (enhancement): scores 0 Chips on its first trigger and +80 Chips on every
-- retrigger after that. Created by the Tarot 'Rampenfieber'.
SMODS.Atlas {
    key = 'Enhancements',
    path = 'Enhancements.png',
    px = 71,
    py = 95,
}

-- Stoned Card (vanilla Stone Card, renamed in localization): same effect, new art with a
-- cannabis leaf and a bit of smoke (tools/stoned_art.py).
SMODS.Enhancement:take_ownership('stone', {
    atlas = 'Enhancements',
    pos = { x = 1, y = 0 },
})

local RAMPE_CHIPS = 80

SMODS.Enhancement {
    key = 'rampe',
    atlas = 'Enhancements',
    pos = { x = 0, y = 0 },
    loc_vars = function(self, info_queue, card)
        return { vars = { RAMPE_CHIPS } }
    end,
    calculate = function(self, card, context)
        -- card.repetition_trigger is nil on the first trigger and 1, 2, ... on retriggers
        if context.main_scoring and context.cardarea == G.play and card.repetition_trigger then
            return { chips = RAMPE_CHIPS }
        end
    end,
}

-- the card's own rank chips never count ("0 Chips on its first trigger")
local get_chip_bonus_ref = Card.get_chip_bonus
function Card:get_chip_bonus()
    if self.ability and SMODS.has_enhancement(self, 'm_donl_rampe') then
        return 0
    end
    return get_chip_bonus_ref(self)
end

-- Tarot: Rampenfieber - turns up to 2 selected cards into Rampen-Karten.
SMODS.Consumable {
    key = 'rampenfieber',
    set = 'Tarot',
    atlas = 'Consumables',
    pos = { x = 5, y = 0 },
    config = { max_highlighted = 2 },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_donl_rampe
        return { vars = { self.config.max_highlighted } }
    end,
    can_use = function(self, card)
        return G.hand and #G.hand.highlighted >= 1 and #G.hand.highlighted <= self.config.max_highlighted
    end,
    use = function(self, card, area, copier)
        local targets = {}
        for i, c in ipairs(G.hand.highlighted) do targets[i] = c end
        for i, c in ipairs(targets) do
            G.E_MANAGER:add_event(Event({
                trigger = 'after',
                delay = 0.15,
                func = function()
                    c:flip()
                    play_sound('card1', 1.15 - (i - 0.999) / (#targets - 0.998) * 0.3)
                    return true
                end,
            }))
        end
        for _, c in ipairs(targets) do
            G.E_MANAGER:add_event(Event({
                trigger = 'after',
                delay = 0.1,
                func = function()
                    c:set_ability(G.P_CENTERS.m_donl_rampe)
                    return true
                end,
            }))
        end
        for i, c in ipairs(targets) do
            G.E_MANAGER:add_event(Event({
                trigger = 'after',
                delay = 0.15,
                func = function()
                    c:flip()
                    play_sound('tarot2', 0.85 + (i - 0.999) / (#targets - 0.998) * 0.3, 0.6)
                    c:juice_up(0.3, 0.3)
                    return true
                end,
            }))
        end
        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.2,
            func = function()
                G.hand:unhighlight_all()
                return true
            end,
        }))
    end,
}
