-- Donlatro decks (assets/{1x,2x}/Backs.png).
SMODS.Atlas {
    key = 'Backs',
    path = 'Backs.png',
    px = 71,
    py = 95,
}

-- Das ADHS-Deck: +2 hand size, +1 discard, but your Jokers reshuffle at the start of every round.
SMODS.Back {
    key = 'adhs',
    atlas = 'Backs',
    pos = { x = 0, y = 0 },
    config = { hand_size = 2, discards = 1 },
    loc_vars = function(self, info_queue, back)
        return { vars = { self.config.hand_size, self.config.discards } }
    end,
    calculate = function(self, back, context)
        if context.setting_blind and G.jokers and #G.jokers.cards > 1 then
            G.E_MANAGER:add_event(Event({
                func = function()
                    DONLATRO.allow_joker_shuffle = true
                    G.jokers:shuffle('donl_adhs_deck')
                    DONLATRO.allow_joker_shuffle = nil
                    play_sound('cardSlide1')
                    return true
                end,
            }))
        end
    end,
}

-- Das Frustsuppen-Deck: start with $0, no interest, +2 hands per round.
SMODS.Back {
    key = 'frustsuppe',
    atlas = 'Backs',
    pos = { x = 1, y = 0 },
    config = { hands = 2, dollars = -4 },
    loc_vars = function(self, info_queue, back)
        return { vars = { self.config.hands } }
    end,
    apply = function(self, back)
        G.GAME.modifiers.no_interest = true
    end,
}
