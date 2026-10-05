-- Layered editions: a Joker can carry up to 3 editions in total.
--   * the first one is the normal edition (shader, price, ...)
--   * further ones are "layers", stored in card.ability.donl_layers = { 'e_polychrome', ... }
--     through a sticker (badge + tooltip + small prism icon) and scored like real editions.
-- Only Negative Wheels of Fortune (e.g. from DübelDonnie) add layers.
SMODS.Atlas {
    key = 'Stickers',
    path = 'Stickers.png',
    px = 71,
    py = 95,
}

local MAX_EDITIONS = 3

SMODS.Sticker {
    key = 'layers',
    atlas = 'Stickers',
    pos = { x = 0, y = 0 },
    badge_colour = HEX('8a71e1'),
    rate = 0,
    should_apply = false,
    loc_vars = function(self, info_queue, card)
        local names = {}
        for _, key in ipairs(card.ability[self.key] or {}) do
            names[#names + 1] = localize { type = 'name_text', set = 'Edition', key = key }
        end
        return { vars = { table.concat(names, ', ') } }
    end,
}

local function layers_of(card)
    local l = card.ability and card.ability.donl_layers
    return type(l) == 'table' and l or {}
end

function DONLATRO.edition_count(card)
    return (card.edition and 1 or 0) + #layers_of(card)
end

-- a stand-in card.edition for one layer, so the edition's own calculate() can read its values
local function layer_edition(key)
    local center = G.P_CENTERS[key]
    local e = { key = key, type = center.key:sub(3) }
    e[e.type] = true
    for k, v in pairs(center.config or {}) do e[k] = v end
    return e
end

-- score the extra layers right after the real edition (same timing: Foil/Holo before the
-- Joker, Polychrome after)
local calculate_edition_ref = Card.calculate_edition
function Card:calculate_edition(context)
    local ret = calculate_edition_ref(self, context)
    local layers = layers_of(self)
    if not layers[1] then return ret end
    local effects = { ret }
    local real = self.edition
    for _, key in ipairs(layers) do
        local center = G.P_CENTERS[key]
        if center and type(center.calculate) == 'function' then
            self.edition = layer_edition(key)
            local ok, o = pcall(center.calculate, center, self, context)
            self.edition = real
            if ok and type(o) == 'table' then
                o.card = o.card or self
                effects[#effects + 1] = o
            end
        end
    end
    local list = {}
    for i = 1, #effects do
        if effects[i] then list[#list + 1] = effects[i] end
    end
    if not list[1] then return nil end
    if #list == 1 then return list[1] end
    return SMODS.merge_effects(list)
end

-- Negative Wheel of Fortune --------------------------------------------------------------
local function is_negative_wheel(card)
    return card.config and card.config.center and card.config.center.key == 'c_wheel_of_fortune'
        and card.edition and card.edition.negative
end

local function stackable(joker)
    return joker.ability.set == 'Joker' and DONLATRO.edition_count(joker) < MAX_EDITIONS
        and joker.config.center.key ~= 'j_donl_daunendonnie' -- its edition is locked
end

-- vanilla recomputes the Wheel's targets every frame; a Negative Wheel may also target Jokers
-- that already have an edition (up to 3 in total)
local card_update_ref = Card.update
function Card:update(dt)
    card_update_ref(self, dt)
    if G.jokers and is_negative_wheel(self) then
        self.eligible_strength_jokers = EMPTY(self.eligible_strength_jokers)
        for _, j in ipairs(G.jokers.cards) do
            if stackable(j) then table.insert(self.eligible_strength_jokers, j) end
        end
    end
end

local function edition_key(edition)
    if type(edition) == 'string' then return edition end
    if type(edition) == 'table' then
        for k in pairs(edition) do return 'e_' .. k end
    end
end

local use_consumeable_ref = Card.use_consumeable
function Card:use_consumeable(area, copier)
    if not is_negative_wheel(self) then
        return use_consumeable_ref(self, area, copier)
    end
    stop_use()
    local used = copier or self
    local pool = {}
    for _, j in ipairs(G.jokers.cards) do
        if stackable(j) then pool[#pool + 1] = j end
    end
    local hit = pool[1] and SMODS.pseudorandom_probability(self, 'wheel_of_fortune', 1, self.ability.extra)
    -- what SMODS' own use_consumeable wrapper does after a roll (we bypass it for this card)
    if SMODS.post_prob and next(SMODS.post_prob) then
        local rolls = SMODS.post_prob
        SMODS.post_prob = {}
        for _, v in ipairs(rolls) do
            v.pseudorandom_result = true
            SMODS.calculate_context(v)
        end
    end
    if hit then
        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.4,
            func = function()
                local target = pseudorandom_element(pool, pseudoseed('donl_negative_wheel'))
                local key = edition_key(poll_edition('wheel_of_fortune', nil, true, true)) or 'e_foil'
                if not target.edition then
                    target:set_edition(key, true)
                else
                    local layers = layers_of(target)
                    local new = {}
                    for i, k in ipairs(layers) do new[i] = k end
                    new[#new + 1] = key
                    SMODS.Stickers.donl_layers:apply(target, new)
                    local center = G.P_CENTERS[key]
                    if center and center.sound then
                        play_sound(center.sound.sound, center.sound.per, center.sound.vol)
                    end
                    target:juice_up(1, 0.5)
                end
                check_for_unlock({ type = 'have_edition' })
                used:juice_up(0.3, 0.5)
                return true
            end,
        }))
    else
        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.4,
            func = function()
                attention_text({
                    text = localize('k_nope_ex'),
                    scale = 1.3,
                    hold = 1.4,
                    major = used,
                    backdrop_colour = G.C.SECONDARY_SET.Tarot,
                    align = (G.STATE == G.STATES.TAROT_PACK or G.STATE == G.STATES.SPECTRAL_PACK
                        or G.STATE == G.STATES.SMODS_BOOSTER_OPENED) and 'tm' or 'cm',
                    offset = { x = 0, y = 0 },
                    silent = true,
                })
                play_sound('tarot2', 1, 0.4)
                used:juice_up(0.3, 0.5)
                return true
            end,
        }))
    end
    delay(0.6)
end
