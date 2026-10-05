-- Makes Donlatro's own Uncommon and Rare jokers easier to find.
-- The game rolls the rarity first (Common 70% / Uncommon 25% / Rare 5% - unchanged), then picks
-- evenly from that rarity's pool. Listing a joker BOOST times in that pool makes it BOOST times
-- as likely as each other joker of the same rarity. Applies to the shop, Buffoon packs,
-- Judgement, Riff-Raff, ... Donlatro Commons, the reworked vanilla jokers and Legendaries
-- keep their normal weight.
local BOOST = 3

local function boosted(center)
    return center and center.mod == DONLATRO and not center.taken_ownership
        and (center.rarity == 2 or center.rarity == 3)
end

local get_current_pool_ref = get_current_pool
function get_current_pool(_type, ...)
    local pool, pool_key = get_current_pool_ref(_type, ...)
    if _type == 'Joker' and type(pool) == 'table' then
        for i = 1, #pool do
            local key = pool[i]
            if key ~= 'UNAVAILABLE' and boosted(G.P_CENTERS[key]) then
                for _ = 2, BOOST do
                    pool[#pool + 1] = key
                end
            end
        end
    end
    return pool, pool_key
end
