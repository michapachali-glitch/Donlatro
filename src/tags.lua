-- Skip tags. Art: assets/{1x,2x}/Tags.png, 34x34 cells (drawn by tools/tag_art.py).
--   x=0 Der Umzug
SMODS.Atlas {
    key = 'Tags',
    path = 'Tags.png',
    px = 34,
    py = 34,
}

-- Der Umzug: in the next shop, every reroll also rerolls the booster packs (everything moves).
-- The tag sets G.GAME.donl_umzug when the shop opens; src/tracking.lua clears it when the
-- shop is left. Saved with the run, so it survives reloading mid-shop.
SMODS.Tag {
    key = 'umzug',
    atlas = 'Tags',
    pos = { x = 0, y = 0 },
    apply = function(self, tag, context)
        if context.type == 'shop_start' and not G.GAME.donl_umzug then
            G.GAME.donl_umzug = true
            tag:yep('+', G.C.BOOSTER, function()
                return true
            end)
            tag.triggered = true
            return true
        end
    end,
}

local reroll_shop_ref = G.FUNCS.reroll_shop
G.FUNCS.reroll_shop = function(e)
    reroll_shop_ref(e)
    if not (G.GAME.donl_umzug and G.shop_booster) then return end
    G.E_MANAGER:add_event(Event({
        func = function()
            for i = #G.shop_booster.cards, 1, -1 do
                local c = G.shop_booster:remove_card(G.shop_booster.cards[i])
                c:remove()
            end
            for _ = 1, G.GAME.starting_params.boosters_in_shop + (G.GAME.modifiers.extra_boosters or 0) do
                SMODS.add_booster_to_shop():juice_up()
            end
            return true
        end,
    }))
end
