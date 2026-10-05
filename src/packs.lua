-- Donnie Pack: a booster with only Donlatro's own Uncommon, Rare and Legendary Jokers
-- (no Commons, no food Jokers, no vanilla / reworked Jokers). Art: assets/{1x,2x}/Packs.png.
SMODS.Atlas {
    key = 'Packs',
    path = 'Packs.png',
    px = 71,
    py = 95,
}

local RARITY_ROLL = { { 0.97, 4 }, { 0.75, 3 }, { 0, 2 } } -- 3% Legendary, 22% Rare, 75% Uncommon

local function donnie_pool(rarity, taken, allow_owned)
    local pool = {}
    for key, c in pairs(G.P_CENTERS) do
        if c.set == 'Joker' and c.mod == DONLATRO and not c.taken_ownership and c.rarity == rarity
            and not SMODS.has_attribute(c, 'food') and not G.GAME.banned_keys[key] and not taken[key]
            and not (type(c.in_pool) == 'function' and not c:in_pool({ source = 'donl_pack' }))
            and (allow_owned or not (G.GAME.used_jokers[key] and not SMODS.showman(key))) then
            pool[#pool + 1] = key
        end
    end
    table.sort(pool) -- deterministic order for seeded runs
    return pool
end

SMODS.Booster {
    key = 'donnie',
    kind = 'Donnie',
    group_key = 'k_donl_donnie_pack',
    atlas = 'Packs',
    pos = { x = 0, y = 0 },
    config = { extra = 3, choose = 1 },
    cost = 8,
    weight = 0.5,
    draw_hand = false,
    ease_background_colour = function(self)
        ease_background_colour_blind(G.STATES.BUFFOON_PACK)
    end,
    create_card = function(self, card, i)
        -- no duplicates inside one pack
        local taken = {}
        for _, c in ipairs(G.pack_cards and G.pack_cards.cards or {}) do
            taken[c.config.center.key] = true
        end
        local roll = pseudorandom('donl_donnie_pack' .. G.GAME.round_resets.ante)
        local rarity = 2
        for _, r in ipairs(RARITY_ROLL) do
            if roll > r[1] then rarity = r[2] break end
        end
        local pool = donnie_pool(rarity, taken)
        for _, fallback in ipairs({ 3, 2, 4 }) do -- e.g. the Legendary is already owned
            if pool[1] then break end
            pool = donnie_pool(fallback, taken)
        end
        -- you already own every eligible Joker: offer duplicates (as with Showman) rather than
        -- falling back to anything outside the pack's pool
        for _, r in ipairs({ rarity, 3, 2, 4 }) do
            if pool[1] then break end
            pool = donnie_pool(r, taken, true)
        end
        if not pool[1] then
            for _, r in ipairs({ rarity, 3, 2, 4 }) do -- last resort: duplicates inside this pack
                if pool[1] then break end
                pool = donnie_pool(r, {}, true)
            end
        end
        local key = pseudorandom_element(pool, pseudoseed('donl_donnie_pick' .. G.GAME.round_resets.ante))
        return { set = 'Joker', key = key, area = G.pack_cards, skip_materialize = true, key_append = 'donl_pack' }
    end,
}
