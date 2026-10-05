-- Run-wide bookkeeping that has to happen whether or not a particular joker is held.
--   G.GAME.donl_prev_hand        ranks played in the previous hand this round (Classic Donnie)
--   G.GAME.donl_ante_snapshot    the deck at the start of the current Ante (Die Rückspultaste)
--   G.GAME.donl_unsicher_until   round after which Zocker's debuff ends

local function snapshot_deck()
    local saved = {}
    for _, c in ipairs(G.playing_cards or {}) do
        saved[#saved + 1] = copy_table(c:save()) -- deep copy: save() shares the live ability table
    end
    G.GAME.donl_ante_snapshot = saved
end

DONLATRO.reset_game_globals = function(run_start)
    if not run_start then return end
    snapshot_deck()
    if DONLATRO.test_mode_run_start then DONLATRO.test_mode_run_start() end
end

function DONLATRO.previous_hand_ranks()
    local prev = G.GAME.donl_prev_hand
    if prev and prev.round == G.GAME.round then
        return prev.ranks
    end
    return {}
end

DONLATRO.calculate = function(self, context)
    if context.after then
        local ranks = {}
        for _, c in ipairs(context.full_hand) do
            ranks[c:get_id()] = true
        end
        G.GAME.donl_prev_hand = { round = G.GAME.round, ranks = ranks }
    end
    if context.ante_change and context.ante_change > 0 then
        snapshot_deck()
    end
    -- Zocker: lift the joker debuff once its full round is over.
    if context.end_of_round and context.main_eval and not context.game_over
        and G.GAME.donl_unsicher_until and G.GAME.round >= G.GAME.donl_unsicher_until then
        G.GAME.donl_unsicher_until = nil
        for _, j in ipairs(G.jokers.cards) do
            SMODS.debuff_card(j, false, 'donl_unsicher')
        end
    end
    -- Donnie O'Sullivan: lift the "lost the thread" debuff after the round he sat out.
    if context.end_of_round and context.main_eval and not context.game_over then
        for _, j in ipairs(G.jokers.cards) do
            local stg = j.config.center.key == 'j_donl_osullivan' and j.ability.extra
            if stg and stg.off_round and G.GAME.round >= stg.off_round then
                stg.off_round = nil
                SMODS.debuff_card(j, false, 'donl_thread')
            end
        end
    end
end
