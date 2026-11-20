# Definitions des cartes SILVER SURFER (DesignHacker, « MC4 SEALED », 2020), 24/10/2026.
# Relues une a une contre les scans (zip « SILVER SURFER (MC4 SEALED) », notice « Silver Surfer Insert »).
# Icones de ressource : eclair jaune = energie (Y), poing = physique (R), noeuds bleus = mental (B),
# etoile verte = wild (G), identiques aux ressources officielles et du MEME pack (verifie sur les scans :
# Surfboard = etoile verte, Energy Manipulation/Cosmic Speed/Cosmic Strength/Cosmic Energy/Silver Up/Power Cosmic
# = eclair jaune, Rage of Retribution = poing, Dawn Greenwood = noeuds).
# Inseres dans data/cards.json par inserer_silver_surfer.py (idempotent).

K = "DesignHacker"
SET = "Silver Surfer"
NEM = "Silver Surfer Nemesis"

CARDS = [
    {"card_id": "sv001a", "type": "Hero", "name": "* Silver Surfer", "subtitle": "",
     "desc": {"HP": "14", "ATK": "3", "THW": "1", "DEF": "2", "HS": "5"},
     "traits": ["AERIAL", "COSMIC", "ADVENTURER"], "set_name": SET,
     "text": "<i>Compunction</i> — <b>Forced Response</b>: After Silver Surfer makes a basic attack, change your form.\n"
             "<i>\"You mistake restraint for weakness.\"</i>",
     "custom": K},
    {"card_id": "sv001b", "type": "AlterEgo", "name": "* Norrin Radd", "subtitle": "",
     "desc": {"HP": "14", "REC": "4", "HS": "6"},
     "traits": ["COSMIC", "ADVENTURER"], "set_name": SET,
     "text": "<i>Toomie!</i> — <b>Action</b>: Exhaust Norrin Radd → search your deck and discard pile for The Silver Surfboard upgrade and add it to your hand. Shuffle your deck.\n"
             "<i>\"To me, my board!\"</i>",
     "custom": K},
    {"card_id": "sv002", "type": "Ally", "name": "* Dawn Greenwood", "subtitle": "",
     "desc": {"Cost": "0", "HP": "1", "ATK": "1*", "THW": "1*", "RES": "B", "Class": "Hero"},
     "traits": ["ADVENTURER"], "set_name": SET,
     "text": "<b>Interrupt</b>: When Dawn Greenwood is defeated, deal 2 damage to your identity → return Dawn Greenwood to your hand.\n"
             "<i>\"You can't have her! I won't let you!\" —Silver Surfer</i>",
     "custom": K},
    {"card_id": "sv003", "type": "Upgrade", "name": "* The Silver Surfboard", "subtitle": "",
     "desc": {"Cost": "0", "RES": "G", "Class": "Hero"},
     "traits": ["AERIAL", "COSMIC", "VEHICLE"], "set_name": SET,
     "text": "<b>Hero Action</b>: Exhaust The Silver Surfboard → ready Silver Surfer.\n"
             "<b>Interrupt</b>: When you discard The Silver Surfboard, deal 1 damage to Silver Surfer → draw a card.",
     "custom": K},
    {"card_id": "sv004", "type": "Upgrade", "name": "Energy Manipulation", "subtitle": "",
     "desc": {"Cost": "0", "RES": "Y", "Class": "Hero"},
     "traits": ["COSMIC", "SUPERPOWER"], "set_name": SET,
     "text": "<b>Action</b>: Spend X [energy] resources → put X energy counters here.\n"
             "<b>Hero Action</b>: Discard Energy Manipulation → draw 1 card (to a maximum of 5) for each energy counter here.",
     "custom": K},
    {"card_id": "sv005", "type": "Upgrade", "name": "Rage of Retribution", "subtitle": "",
     "desc": {"Cost": "2", "RES": "R", "Class": "Hero"},
     "traits": ["CONDITION"], "set_name": SET,
     "text": "Silver Surfer gains retaliate 1.\n"
             "<b>Interrupt</b>: When Silver Surfer would change form, discard Rage of Retribution → ready Silver Surfer instead.\n"
             "<i>\"Face my full unbridled fury!\"</i>",
     "custom": K},
    {"card_id": "sv006", "type": "Event", "name": "Cosmic Speed", "subtitle": "",
     "desc": {"Cost": "3", "RES": "Y", "Class": "Hero"},
     "traits": ["COSMIC", "THWART"], "set_name": SET,
     "text": "<b>Hero Action</b> <i>(thwart)</i>: Choose one:\n"
             "• Remove 4 threat from a scheme.\n"
             "• Discard The Silver Surfboard → remove up to 3 threat from each scheme in play.\n"
             "<i>\"Board, listen! Go that way, I'll go the other.\"</i>",
     "custom": K},
    {"card_id": "sv007", "type": "Event", "name": "Cosmic Strength", "subtitle": "",
     "desc": {"Cost": "3", "RES": "Y", "Class": "Hero"},
     "traits": ["COSMIC", "SUPERPOWER"], "set_name": SET,
     "text": "<b>Hero Interrupt</b>: When you make a basic attack, choose one:\n"
             "• You get +7 ATK for that attack.\n"
             "• Discard The Silver Surfboard → You get +9 ATK for that attack and it gains overkill.",
     "custom": K},
    {"card_id": "sv008", "type": "Event", "name": "Cosmic Energy", "subtitle": "",
     "desc": {"Cost": "X", "RES": "Y", "Class": "Hero"},
     "traits": ["ATTACK", "COSMIC", "THWART"], "set_name": SET,
     "text": "<b>Hero Action</b> <i>(attack)</i>: Remove X threat divided among schemes as you choose and deal X damage to an enemy, where X is the number of [energy] resources you paid for Cosmic Energy's cost.\n"
             "<i>\"That's the power cosmic.\"</i>",
     "custom": K},
    {"card_id": "sv009", "type": "Event", "name": "Silver Up", "subtitle": "",
     "desc": {"Cost": "2", "RES": "Y", "Class": "Hero"},
     "traits": ["COSMIC", "SUPERPOWER"], "set_name": SET,
     "text": "When you play this card, you may discard The Silver Surfboard, then choose two instead.\n"
             "<b>Alter-Ego Action</b>: Flip to Silver Surfer, then choose one: draw 2 cards, deal 4 damage to an enemy, or ready Silver Surfer.",
     "custom": K},
    {"card_id": "sv010", "type": "Resource", "name": "The Power Cosmic", "subtitle": "",
     "desc": {"RES": "YY", "Class": "Hero"},
     "traits": [], "set_name": SET,
     "text": "<b>Response</b>: After you spend this card to play a [[COSMIC]] event, deal 2 damage to an enemy.\n"
             "<i>\"That's very...convenient.\" —Dawn Greenwood</i>",
     "custom": K},
    {"card_id": "sv011", "type": "Obligation", "name": "Silver Down", "subtitle": "",
     "desc": {"Boost": "1", "GiveTo": "Norrin Radd"},
     "traits": [], "set_name": SET,
     "text": "<b><i>Give to the Norrin Radd player.</i></b>\nYou may flip to alter-ego form. Choose:\n"
             "• Exhaust Norrin Radd → remove Silver Down from the game.\n"
             "• Summon Dawn Greenwood and remove her from the game → remove Silver Down from the game.",
     "custom": K},
    {"card_id": "sv012", "type": "Minion", "name": "* Galactus", "subtitle": "",
     "desc": {"HP": "3", "SCH": "2", "ATK": "2", "Villainous": "1", "Nemesis": "Silver Surfer"},
     "traits": ["COSMIC", "ELITE"], "set_name": NEM,
     "text": "Villainous.\n<b>When Revealed</b>: Reveal The World Eater and put it into play engaged with you.\n"
             "<b>When Defeated</b>: Remove Galactus from the game.\n<i>(Silver Surfer's nemesis minion.)</i>",
     "custom": K},
    {"card_id": "sv013", "type": "Minion", "name": "* The World Eater", "subtitle": "",
     "desc": {"HP": "5", "SCH": "0", "ATK": "0"},
     "traits": ["COSMIC", "ELITE"], "set_name": NEM,
     "text": "Galactus cannot take damage and his attacks gain overkill.\n"
             "<b>When Defeated</b>: Remove The World Eater from the game.\n"
             "<i>\"You will claim no victory here today, Norrin Radd. True, you may delay me for a time, but you cannot possibly stop me.\"</i>",
     "custom": K},
    {"card_id": "sv014", "type": "SideScheme", "name": "The Life Stealer", "subtitle": "",
     "desc": {"StartingThreat": "2", "Boost": "2"},
     "traits": [], "set_name": NEM,
     "text": "All friendly characters get -1 ATK.\n<b>When Revealed</b>: Place 1 additional threat here for each friendly character in play.\n"
             "<i>Galactus is using The Power Cosmic to steal the heroes' life force!</i>",
     "custom": K},
    {"card_id": "sv015", "type": "Attachment", "name": "Cosmic Power", "subtitle": "",
     "desc": {"Boost": "1", "ATK+": "0*"},
     "traits": [], "set_name": NEM,
     "text": "Attach to Galactus. If you cannot, attach to the villain.\n[star] Attached enemy's attacks gain overkill.\n"
             "<b>Hero Action</b>: Take 3 damage → remove Cosmic Power from the game.\n"
             "<i>\"The only power you possess, is the power I bestowed upon you.\"</i>",
     "custom": K},
]
