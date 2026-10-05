return {
    descriptions = {
        Mod = {
            Donlatro = {
                name = 'Donlatro',
                text = { 'A Balatro mod.' },
            },
        },
        Joker = {
            j_donl_daunendonnie = {
                name = 'Daunendonnie',
                text = {
                    'Permanently gains {C:chips}+#1#{} Chips',
                    'for each played card',
                    'that does {C:attention}not{} score',
                    'Becomes {C:dark_edition}Foil{} during {C:attention}Boss Blinds{}',
                    '{C:inactive}(Currently {C:chips}+#2#{C:inactive} Chips)',
                },
            },
            j_donl_trektrendy = {
                name = 'TrekTrendy',
                text = {
                    '{C:attention}Doubles{} the {C:money}sell value{}',
                    'of all your cards,',
                    'including this one',
                },
            },
            j_donl_sosse = {
                name = 'So(ß)e',
                text = {
                    '{C:chips}+#1#{} Chips',
                    '{C:chips}-#2#{} Chips at end of round',
                    '{C:red}Destroyed{} at end of round if',
                    'another {C:attention}food{} Joker is held',
                },
            },
            j_donl_doener = {
                name = 'Döner',
                text = {
                    '{C:mult}+#1#{} Mult for each different',
                    '{C:attention}suit{} in the scored hand',
                    '{X:mult,C:white} X#2# {} Mult while {C:attention}So(ß)e{} is held',
                },
            },
            j_donl_don_appetito = {
                name = 'Don Appetito',
                text = {
                    '{C:mult}+#1#{} Mult',
                    'Gains {C:mult}+#2#{} Mult for every',
                    '{C:attention}Donlatro food{} Joker',
                    'that ran out this run',
                    '{C:inactive}No Mult while {C:attention}So(ß)e{C:inactive} is held',
                },
            },
            j_donl_holyenergy = {
                name = 'HolyEnergy',
                text = {
                    '{X:mult,C:white} X#1# {} Mult',
                    'Gains {X:mult,C:white} X#2# {} Mult',
                    'at end of round',
                    '{C:red}Destroyed{} when it reaches {X:mult,C:white} X#3# {}',
                },
            },
            j_donl_maggi = {
                name = 'Maggi',
                text = {
                    '{C:red}+#1#{} discards',
                    'each round, reduces by',
                    '{C:red}#2#{} every round',
                },
            },
            j_donl_maultaschen = {
                name = 'Maultaschen',
                text = {
                    '{C:attention}+#1#{} hand size,',
                    'reduces by',
                    '{C:red}#2#{} every round',
                },
            },
            j_donl_sauerteigbrot = {
                name = 'Sauerteigbrot',
                text = {
                    'Doubles its {C:money}sell value{}',
                    'at end of round',
                    '{C:green}#1# in #2#{} chance to be',
                    '{C:red}destroyed{} instead',
                },
            },
            j_donl_baehnle = {
                name = 'Bähnle',
                text = {
                    'Gains {C:mult}+#1#{} Mult each time a',
                    '{C:attention}Gold{} card held in hand',
                    'pays out at end of round',
                    '{C:inactive}(Currently {C:mult}+#2#{C:inactive} Mult)',
                },
            },
            j_donl_erdie = {
                name = 'Erdie Feuermann',
                text = {
                    'When {C:attention}sold{}, removes all',
                    '{C:attention}stickers{} from your',
                    'other Jokers',
                },
            },
            j_donl_nolan = {
                name = 'Nolan',
                text = {
                    'Playing a {C:attention}Straight{} in',
                    '{C:attention}descending{} order (e.g. 6-5-4-3-2)',
                    'adds {C:money}$#1#{} sell value',
                    'At {C:money}$#2#{}: {C:attention}-#3#{} Ante, then destroyed',
                    '{C:inactive}(Currently {C:money}$#4#{C:inactive})',
                },
            },
            j_donl_frustsuppe = {
                name = 'Frustsuppe',
                text = {
                    '{C:chips}+#1#{} Chips, {C:mult}+#2#{} Mult',
                    '{X:mult,C:white} X#3# {} Mult',
                    'You earn {C:money}$0{} from',
                    'everything while held',
                },
            },
            j_donl_shepherds_pie = {
                name = "Shepherd's Pie",
                text = {
                    'Every {C:attention}scored{} card permanently',
                    'gains {C:mult}+#1#{} Mult',
                    '{C:attention}#2#{} portions left,',
                    'one eaten each round',
                },
            },
            j_donl_bierbrunnen = {
                name = 'Bierbrunnen',
                text = {
                    '{C:green}#1# in #2#{} chance for each',
                    'scored card to become',
                    'a {C:money}Gold{} card',
                    'Runs dry after {C:attention}#3#{} conversions',
                    '{C:inactive}(#4# left)',
                },
            },
            j_donl_jochen = {
                name = 'Jochen',
                text = {
                    'Earn between {C:red}-$#1#{} and {C:money}$#2#{}',
                    'at {C:attention}Cash Out{}',
                    '{C:inactive}(your Steuerberater decides)',
                },
            },
            j_donl_udk = {
                name = 'UDK Abschlussarbeit',
                text = {
                    'If all scored cards are {C:attention}Aces{},',
                    '{X:mult,C:white} X1 {} Mult per scored {C:attention}Ace{}',
                },
            },
            j_donl_rampe = {
                name = 'Die Rampe',
                text = {
                    'Gains {X:mult,C:white} X#1# {} Mult for each',
                    '{C:attention}discard{} used this round',
                    '{C:inactive}(Currently {X:mult,C:white} X#2# {C:inactive} Mult)',
                },
            },
            j_donl_classic_donnie = {
                name = 'Classic Donnie',
                text = {
                    '{C:attention}Retrigger{} played cards whose',
                    'rank was also played in your',
                    '{C:attention}previous hand{} this round',
                },
            },
            j_donl_ihr_checkt = {
                name = 'Ihr checkt schon, was ich meine',
                text = {
                    '{C:attention}Flushes{} can be made with {C:attention}4{} cards',
                    '{C:attention}Straights{} can be made with',
                    '{C:attention}4{} of the {C:attention}5{} ranks (one card short)',
                },
            },
            j_donl_anyway = {
                name = 'DübelDonnie',
                text = {
                    'Permanently gains {C:mult}+#1#{} Mult',
                    'every time a {C:attention}High Card{} is played',
                    'Scored {C:attention}Stoned Cards{} have a {C:green}#3# in #4#{}',
                    'chance to create a {C:dark_edition}Negative{}',
                    '{C:tarot}Wheel of Fortune{}',
                    '{C:inactive}(Currently {C:mult}+#2#{C:inactive} Mult)',
                },
            },
            j_donl_akkuschrauber = {
                name = 'Der Akkuschrauber',
                text = {
                    'Charges {C:mult}+#1#{} Mult and {C:chips}+#2#{} Chips',
                    'at end of round',
                    'Beating a {C:attention}Boss Blind{} empties it:',
                    'earn {C:money}$1{} per {C:mult}2{} Mult, then recharge',
                    '{C:inactive}(Currently {C:mult}+#3#{C:inactive} Mult, {C:chips}+#4#{C:inactive} Chips)',
                },
            },
            j_donl_butlers = {
                name = 'Buttplugs bei Butlers',
                text = {
                    'Every scored card is {C:attention}retriggered{}',
                    'once for each hand already',
                    'played this round',
                    '{C:inactive}(e.g. 3rd hand: every card scores 3 times)',
                    '{C:inactive}(Next hand: {C:attention}+#1#{C:inactive} retriggers)',
                },
            },
            j_donl_kaffee = {
                name = 'Kaffee',
                text = {
                    '{C:red}+#1#{} discard for the',
                    'next round only',
                    'Costs {C:money}$#2#{} at end of round,',
                    '{C:red}destroyed{} if you can\'t pay',
                },
            },
            j_donl_osullivan = {
                name = "Donnie O'Sullivan",
                text = {
                    '{X:mult,C:white} X#1# {} Mult',
                    '{C:green}#2# in #3#{} chance at end of round',
                    'to {C:red}lose the thread{}: debuffed',
                    'for the following round',
                },
            },
            -- renamed vanilla jokers (src/reskins.lua): only the name changes, text stays vanilla
            j_half = { name = 'Der kurze Gedanke' },
            j_mystic_summit = { name = 'Ohne Rampe, ohne mich' },
            j_flower_pot = { name = 'Die Monstera' },
            j_stencil = { name = 'Das Solo-Format' },
            j_abstract = { name = 'Die Gästeliste' },
            j_loyalty_card = { name = 'Die Mittwochsfolge' },
            j_acrobat = { name = 'Auf einer positiven Note' },
            j_smeared = { name = 'Die Mayo-Chronik' },
            j_pareidolia = { name = 'Parasozial' },
            j_shortcut = { name = 'Der Themensprung' },
            j_arrowhead = { name = 'Berlin' },
            j_bloodstone = { name = 'Tübingen' },
            j_rough_gem = { name = 'Hamburg' },
            j_onyx_agate = { name = 'Irland' },
            j_credit_card = { name = 'Erste Steuernachzahlung' },
            j_delayed_grat = { name = '„Ich komme gleich dazu"' },
            j_business = { name = 'Die Werbeanfrage' },
            j_rocket = { name = 'Die Reichweite' },
            j_bull = { name = 'Das neue Studio' },
            j_bootstraps = { name = 'Der Selbstständige' },
            j_matador = { name = 'Der Gegenwind' },
            j_troubadour = { name = 'Der Deep Talk' },
            j_burglar = { name = 'Dieb Talk' },
            j_stuntman = { name = 'Disziplin-Donnie' },
            j_juggler = { name = 'Die Überleitung' },
            j_drunkard = { name = 'Das Bierchen' },
            j_chaos = { name = 'Noch ein Take' },
            j_luchador = { name = 'Der Werbepartner' },
            j_mr_bones = { name = '„Lass ihn mal drin"' },
            j_ceremonial = { name = 'Rausgeschnitten' },
            j_marble = { name = 'Löcher spachteln', text = { 'Adds one {C:attention}Stoned{} card', 'to deck when', '{C:attention}Blind{} is selected' } },
            j_stone = { text = { 'Gives {C:chips}+#1#{} Chips for', 'each {C:attention}Stoned Card', 'in your {C:attention}full deck', '{C:inactive}(Currently {C:chips}+#2#{C:inactive} Chips)' } },
            j_hiker = { name = 'Der Spaziergang' },
            j_swashbuckler = { name = 'Das Merch' },
            j_misprint = { name = 'Der Zahlendreher' },
            j_baseball = { name = 'Die Nebenfiguren' },
            j_idol = { name = 'Der Algorithmus' },
            j_oops = { name = 'Die Hoffnung' },
            j_cartomancer = { name = 'Die Astrologie' },
            j_astronomer = { name = 'Nolan Schmolan' },
            j_vagabond = { name = 'Die Pfandflaschen' },
            j_burnt = { name = 'Die Pause-Taste' },
            j_space = { name = 'Die Rakete' },
            j_triboulet = { name = 'Costa und Jochen' },
            j_yorick = { name = '„Wo war ich?"' },
            j_chicot = { name = 'Der Spotify-Deal' },
            j_perkeo = { name = 'Das Transkript' },
        },
        Enhanced = {
            m_stone = { name = 'Stoned Card' },
            m_donl_rampe = {
                name = 'Rampen-Karte',
                text = {
                    'Scores {C:chips}0{} Chips on its',
                    'first trigger, {C:chips}+#1#{} Chips',
                    'on every {C:attention}retrigger{}',
                },
            },
        },
        Other = {
            p_donl_donnie = {
                name = 'Donnie Pack',
                text = {
                    'Choose {C:attention}#1#{} of up to',
                    '{C:attention}#2#{} Donlatro Jokers:',
                    '{C:green}Uncommon{}, {C:red}Rare{} or {C:legendary,E:1}Legendary{}',
                    '{C:inactive}(no Commons, no food)',
                },
            },
            donl_layers = {
                name = 'Layered Editions',
                text = {
                    'Also has: {C:dark_edition}#1#{}',
                },
            },
            donl_negative_wheel = {
                name = 'Negative Wheel',
                text = {
                    'A {C:dark_edition}Negative{} {C:tarot}Wheel of Fortune{}',
                    'can add an edition to a Joker',
                    'that already has one',
                    '{C:inactive}(up to {C:attention}3{C:inactive} editions per Joker)',
                },
            },
        },
        Blind = {
            bl_donl_wasserschaden = {
                name = 'Wasserschaden',
                text = {
                    '#1# in #2# chance for each',
                    'scored card to be destroyed',
                },
            },
            bl_donl_nachbar = {
                name = 'Nachbar von oben',
                text = {
                    'All Chips are halved',
                    'and the techno is LOUD',
                    '{C:inactive}(always the final boss on White Stake)',
                },
            },
            bl_donl_kammer = {
                name = 'Die Kammer',
                text = {
                    'First hand is',
                    'drawn face down',
                },
            },
            bl_donl_adhs = {
                name = 'ADHS',
                text = {
                    'Played cards are',
                    'shuffled before scoring',
                },
            },
            bl_donl_dieb = {
                name = 'Dieb',
                text = {
                    'Lose {C:money}$#1#{} for every',
                    'discarded card',
                },
            },
            bl_donl_flusensieb = {
                name = 'Hans Flusensieb',
                text = {
                    'After each hand, destroy',
                    'a random card in hand',
                },
            },
            bl_donl_folgennummer = {
                name = 'Die falsche Folgennummer',
                text = {
                    'Hands are scored as a random',
                    'other hand type you have',
                    'played this run',
                },
            },
        },
        Voucher = {
            v_donl_patreon = {
                name = 'Patreon',
                text = {
                    'Earn {C:money}$#1#{} at end of round',
                    'per {C:attention}Joker{} owned',
                },
            },
            v_donl_patreon_exklusiv = {
                name = 'Patreon Exklusiv',
                text = {
                    'Earn {C:money}$#1#{} per {C:attention}Joker{}',
                    'at end of round',
                    'One shop item per Ante',
                    'is {C:attention}free{}',
                },
            },
            v_donl_therapieplatz = {
                name = 'Therapieplatz',
                text = {
                    'Reroll the {C:attention}Boss Blind{}',
                    'for {C:money}free{} once per Ante',
                },
            },
            v_donl_kassenzulassung = {
                name = 'Kassenzulassung',
                text = {
                    'Reroll the {C:attention}Boss Blind{}',
                    'for {C:money}free{}, unlimited times',
                },
            },
            v_donl_medikinet = {
                name = 'Medikinet',
                text = {
                    '{C:attention}+#1#{} hand size',
                },
            },
            v_donl_elvanse = {
                name = 'Elvanse',
                text = {
                    '{C:attention}+#1#{} hand size',
                    'Blinds can no longer {C:attention}debuff{}',
                    'or {C:attention}shuffle{} your Jokers',
                },
            },
            v_donl_arcaden = {
                name = 'Schönhauser Allee Arcaden',
                text = {
                    '{C:attention}+1{} card slot',
                    'available in shop',
                },
            },
            v_donl_erdgeschoss = {
                name = 'Das ganze Erdgeschoss',
                text = {
                    '{C:attention}+1{} card slot and',
                    '{C:attention}+1{} Voucher slot',
                    'available in shop',
                },
            },
            v_donl_superrampe = {
                name = 'Superrampe',
                text = {
                    '{C:red}+#1#{} discard',
                    'each round',
                },
            },
            v_donl_mini_superrampe = {
                name = 'Mini-Superrampe in der Superrampe',
                text = {
                    '{C:red}+#1#{} discard each round',
                    'Each discarded card adds',
                    '{C:chips}+#2#{} Chips to your next hand',
                    '{C:inactive}(Next hand: {C:chips}+#3#{C:inactive})',
                },
            },
        },
        Tarot = {
            c_donl_rampenfieber = {
                name = 'Rampenfieber',
                text = {
                    'Enhances up to {C:attention}#1#{}',
                    'selected cards into',
                    '{C:attention}Rampen-Karten{}',
                },
            },
            c_donl_classic_donnie = {
                name = 'Classic Donnie',
                text = {
                    'Creates a copy of',
                    '{C:attention}1{} selected card',
                    'and adds it to your deck',
                },
            },
            c_donl_therapie = {
                name = 'Die Therapie',
                text = {
                    'Removes {C:attention}debuffs{}, {C:attention}edition{}',
                    'and {C:attention}enhancement{} from',
                    '{C:attention}1{} selected card',
                    '{C:red}-$#1#{}',
                },
            },
        },
        Spectral = {
            c_donl_rueckspultaste = {
                name = 'Die Rückspultaste',
                text = {
                    'Restores your deck to its',
                    'state at the {C:attention}start of this Ante{}',
                    'Lose {C:money}all money{}',
                },
            },
            c_donl_eingeschissen = {
                name = 'Eingeschissen',
                text = {
                    'Adds {C:dark_edition}Negative{} to a',
                    'random {C:attention}Joker{}',
                    'Destroys a random card',
                    'in your deck',
                    '{C:inactive,s:0.8}A word with no meaning that',
                    '{C:inactive,s:0.8}changes everything. 11 uses in #231.',
                },
            },
            c_donl_unsicherheit = {
                name = 'Zocker',
                text = {
                    '{C:attention}+#1#{} Joker slot',
                    'All current Jokers are',
                    '{C:red}debuffed{} for one full round',
                },
            },
        },
        Back = {
            b_donl_adhs = {
                name = 'Das ADHS-Deck',
                text = {
                    '{C:attention}+#1#{} hand size',
                    '{C:red}+#2#{} discard',
                    'Jokers {C:attention}reshuffle{} every round',
                },
            },
            b_donl_frustsuppe = {
                name = 'Das Frustsuppen-Deck',
                text = {
                    'Start with {C:money}$0{}',
                    'Earn {C:attention}no interest{}',
                    '{C:blue}+#1#{} hands every round',
                },
            },
        },
    },
    misc = {
        labels = {
            donl_layers = 'Layered',
        },
        dictionary = {
            k_donl_spilled = 'Spilled!',
            k_donl_soggy = 'Soggy!',
            k_donl_extinguished = 'Extinguished!',
            k_donl_empty = 'Empty!',
            k_donl_donnie_pack = 'Donnie Pack',
            k_donl_lost_thread = 'Lost the thread!',
            k_donl_charging = 'Charging!',
            k_donl_battery_empty = 'Akku leer!',
            k_plus_stone = '+1 Stoned',
            ph_deck_preview_stones = 'Stoned',
        },
        v_dictionary = {
            a_donl_discards_minus = '-#1# Discards',
            a_donl_discards_plus = '+#1# Discards',
            a_donl_ante_minus = '-#1# Ante!',
            a_donl_portions_left = '#1# left',
        },
    },
}
