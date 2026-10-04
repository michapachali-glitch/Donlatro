-- Test mode: set to false to play with the normal joker pool again.
-- While on, every new run:
--   * bans all non-Donlatro jokers from spawning (shop, Buffoon packs, Judgement, ...)
--   * doubles the shop's joker rate, so jokers show up twice as often (20 -> 40)
-- Tarot, planet, spectral cards, vouchers etc. are untouched. Jokers already owned stay.
local TEST_MODE = true

if TEST_MODE then
    -- called from DONLATRO.reset_game_globals (src/tracking.lua) when a run starts
    DONLATRO.test_mode_run_start = function()
        for _, center in ipairs(G.P_CENTER_POOLS.Joker) do
            if not (center.mod and center.mod.id == DONLATRO.id) then
                G.GAME.banned_keys[center.key] = true
            end
        end
        G.GAME.joker_rate = G.GAME.joker_rate * 2
    end
end
