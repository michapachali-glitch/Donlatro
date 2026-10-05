-- Blind chips: assets/{1x,2x}/Blinds.png, 21 animation frames of 34x34 per row.
--   y=0 Wasserschaden   y=1 Nachbar von oben   y=2 Die Kammer   y=3 ADHS   y=4 Dieb
--   y=5 Hans Flusensieb   y=6 Die falsche Folgennummer
SMODS.Atlas {
    key = 'Blinds',
    path = 'Blinds.png',
    px = 34,
    py = 34,
    atlas_table = 'ANIMATION_ATLAS',
    frames = 21,
}

-- Wasserschaden (boss): every scored card has a 1 in 10 chance to be destroyed.
SMODS.Blind {
    key = 'wasserschaden',
    atlas = 'Blinds',
    pos = { x = 0, y = 0 },
    boss = { min = 1 },
    boss_colour = HEX('3a7fc4'),
    dollars = 5,
    mult = 2,
    config = { extra = { odds = 10 } },
    loc_vars = function(self)
        local num, den = SMODS.get_probability_vars(self, 1, self.config.extra.odds, 'donl_wasserschaden')
        return { vars = { num, den } }
    end,
    collection_loc_vars = function(self)
        return { vars = { 1, self.config.extra.odds } }
    end,
    calculate = function(self, blind, context)
        if blind.disabled then return end
        if context.destroy_card and context.cardarea == G.play
            and SMODS.pseudorandom_probability(blind, 'donl_wasserschaden', 1, self.config.extra.odds) then
            return { remove = true }
        end
    end,
}

-- Nachbar von oben (showdown boss): halves all Chips at the end of scoring and blasts
-- techno at full music volume for the whole blind.
local function nachbar_active()
    local blind = G.GAME and G.GAME.blind
    return blind and blind.in_blind and not blind.disabled
        and blind.config and blind.config.blind and blind.config.blind.key == 'bl_donl_nachbar'
end

SMODS.Blind {
    key = 'nachbar',
    atlas = 'Blinds',
    pos = { x = 0, y = 1 },
    boss = { showdown = true },
    boss_colour = HEX('e028dc'),
    dollars = 8,
    mult = 2,
    calculate = function(self, blind, context)
        if blind.disabled then return end
        if context.final_scoring_step then
            return { xchips = 0.5, message_card = blind.children.animatedSprite }
        end
    end,
}

SMODS.Sound {
    key = 'music_nachbar',
    path = 'music_nachbar.ogg',
    select_music_track = function(self)
        return nachbar_active() and 100 or false
    end,
}

-- "Full volume": while the Nachbar is active, hand the sound thread a copy of the sound
-- settings with music at 100%. The real settings are never changed (or saved).
local modulate_sound_ref = modulate_sound
function modulate_sound(dt)
    if not nachbar_active() then
        return modulate_sound_ref(dt)
    end
    local real = G.SETTINGS.SOUND
    local loud = {}
    for k, v in pairs(real) do loud[k] = v end
    loud.music_volume = 100
    G.SETTINGS.SOUND = loud
    local ok, err = pcall(modulate_sound_ref, dt)
    G.SETTINGS.SOUND = real
    if not ok then error(err, 0) end
end

-- Die Kammer (boss): the first hand of the blind is drawn face down.
SMODS.Blind {
    key = 'kammer',
    atlas = 'Blinds',
    pos = { x = 0, y = 2 },
    boss = { min = 1 },
    boss_colour = HEX('605478'),
    dollars = 5,
    mult = 2,
    stay_flipped = function(self, area, card)
        return area == G.hand
            and G.GAME.current_round.hands_played == 0
            and G.GAME.current_round.discards_used == 0
    end,
}

-- ADHS (boss): played cards are shuffled into a random order before scoring.
SMODS.Blind {
    key = 'adhs',
    atlas = 'Blinds',
    pos = { x = 0, y = 3 },
    boss = { min = 1 },
    boss_colour = HEX('d6c434'),
    dollars = 5,
    mult = 2,
    press_play = function(self)
        G.E_MANAGER:add_event(Event({
            func = function()
                G.play:shuffle('donl_adhs')
                play_sound('cardSlide1')
                return true
            end,
        }))
        return true
    end,
}

-- Dieb (boss): lose $1 for every discarded card.
SMODS.Blind {
    key = 'dieb',
    atlas = 'Blinds',
    pos = { x = 0, y = 4 },
    boss = { min = 1 },
    boss_colour = HEX('548470'),
    dollars = 5,
    mult = 2,
    config = { extra = { dollars = 1 } },
    loc_vars = function(self)
        return { vars = { self.config.extra.dollars } }
    end,
    collection_loc_vars = function(self)
        return { vars = { self.config.extra.dollars } }
    end,
    calculate = function(self, blind, context)
        if blind.disabled then return end
        -- message_card is required: SMODS evaluates discards without a card to attach the
        -- "-$1" text to, and card_eval_status_text crashes on nil.
        if context.discard then
            return { dollars = -self.config.extra.dollars, message_card = context.other_card }
        end
    end,
}

-- Hans Flusensieb (boss): after each hand, a random card in your hand is destroyed.
SMODS.Blind {
    key = 'flusensieb',
    atlas = 'Blinds',
    pos = { x = 0, y = 5 },
    boss = { min = 2 },
    boss_colour = HEX('9696a6'),
    dollars = 5,
    mult = 2,
    calculate = function(self, blind, context)
        if blind.disabled then return end
        if context.after and G.hand then
            local candidates = {}
            for _, c in ipairs(G.hand.cards) do
                if not c.getting_sliced then candidates[#candidates + 1] = c end
            end
            if not candidates[1] then return end
            local victim = pseudorandom_element(candidates, pseudoseed('donl_flusensieb'))
            SMODS.juice_up_blind()
            SMODS.destroy_cards(victim)
        end
    end,
}

-- Die falsche Folgennummer (boss): the hand is scored with the base Chips/Mult of a random
-- other poker hand you have already played this run.
SMODS.Blind {
    key = 'folgennummer',
    atlas = 'Blinds',
    pos = { x = 0, y = 6 },
    boss = { min = 2 },
    boss_colour = HEX('ce6046'),
    dollars = 5,
    mult = 2,
    modify_hand = function(self, cards, poker_hands, text, mult, hand_chips)
        if G.GAME.blind.disabled then return mult, hand_chips, false end
        local options = {}
        for _, name in ipairs(G.handlist) do
            local h = G.GAME.hands[name]
            if name ~= text and h and h.played > 0 then
                options[#options + 1] = name
            end
        end
        if not options[1] then return mult, hand_chips, false end
        local other = pseudorandom_element(options, pseudoseed('donl_folgennummer'))
        local h = G.GAME.hands[other]
        update_hand_text({ delay = 0 }, { handname = localize(other, 'poker_hands'), level = h.level })
        return h.mult, h.chips, true
    end,
}
