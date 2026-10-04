-- Donlatro entry point.
-- Steamodded runs this file once at load. Content goes in src/ and is loaded below.
-- Every key we register gets the 'donl' prefix automatically (e.g. j_donl_example).

DONLATRO = SMODS.current_mod

-- Load every .lua file in src/ (add jokers, consumables, etc. there).
local files = NFS.getDirectoryItems(DONLATRO.path .. 'src')
table.sort(files)
for _, file in ipairs(files) do
    if file:match('%.lua$') then
        assert(SMODS.load_file('src/' .. file))()
    end
end

-- Everything from Donlatro is unlocked and discovered from the start (no collection "?").
for _, objects in ipairs({ SMODS.Centers, SMODS.Blinds }) do
    for _, obj in pairs(objects) do
        if obj.mod == DONLATRO then
            obj.unlocked = true
            obj.discovered = true
        end
    end
end
