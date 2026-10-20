# Definitions des cartes BINARY (Galactic Storm, Kajislav), lot GS-1 (20/10/2026).
# Relues une a une contre les scans (sources z1..z3, Hero Packs/Binary). Icones de
# ressource verifiees par decoupe contre les reskins du MEME pack dont la ressource
# est connue (Energy 01088 YY = eclair jaune, Genius 01089 BB = noeuds bleus,
# Strength 01090 RR = poing rouge, Specialists 43034-43037 G = etoile verte).
# Inseres dans data/cards.json par inserer_binary.py (idempotent).

K = "Kajislav"
SET = "Binary"
NEM = "Binary Nemesis"

CARDS = [
    {"card_id": "gs001a", "type": "Hero", "name": "* Binary", "subtitle": "",
     "desc": {"HP": "12", "ATK": "0", "THW": "2", "DEF": "2", "HS": "5"},
     "traits": ["AERIAL", "STARJAMMER"], "set_name": SET,
     "text": "X is the number of [energy] resources in your hand (to a maximum of 5).\n"
             "<i>Burnout</i> — <b>Forced Response</b>: After your turn ends, discard each [energy] resource from your hand.\n"
             "<i>\"My fires blaze as hot as the world's heart...\"</i>",
     "custom": K},
    {"card_id": "gs001b", "type": "AlterEgo", "name": "* Carol Danvers", "subtitle": "",
     "desc": {"HP": "12", "REC": "4", "HS": "5"},
     "traits": ["ASTRONAUT"], "set_name": SET,
     "text": "You must include an equal number of cards with a printed [energy], [mental], and [physical] resource in your deck.\n"
             "<i>Exploring Space</i> — <b>Action</b>: Draw 1 card. <i>(Limit once per round.)</i>",
     "custom": K},
    {"card_id": "gs002", "type": "Event", "name": "Cosmic Influx", "subtitle": "",
     "desc": {"Cost": "1", "RES": "R", "Class": "Hero"},
     "traits": ["SUPERPOWER"], "set_name": SET,
     "text": "Max 1 per round.\n<b>Hero Action</b>: Draw 3 cards. Take 1 damage for each non-[energy] resource drawn this way.\n"
             "<i>\"Somehow, when I use my power, I tap into a white hole...\" —Binary</i>",
     "custom": K},
    {"card_id": "gs003", "type": "Event", "name": "Fuel the Fire", "subtitle": "",
     "desc": {"Cost": "0", "RES": "B", "Class": "Hero"},
     "traits": ["DEFENSE", "SUPERPOWER"], "set_name": SET,
     "text": "<b>Hero Interrupt</b> <i>(defense)</i>: When you would take any amount of damage from an attack, for each [energy] resource in your hand prevent 1 of that damage and heal 1 damage from Binary.\n"
             "<i>\"You hit me with fire, you overgrown fish?! I was born on fire!\" —Binary</i>",
     "custom": K},
    {"card_id": "gs004", "type": "Event", "name": "Pursued by the Flame", "subtitle": "",
     "desc": {"Cost": "1", "RES": "Y", "Class": "Hero"},
     "traits": ["SUPERPOWER", "THWART"], "set_name": SET,
     "text": "<b>Hero Action</b> <i>(thwart)</i>: Remove 2 threat from a scheme. If you have at least [energy][energy] resources in your hand, ready Binary.\n"
             "<i>\"That's right, monster...I'm coming after you!\" —Binary</i>",
     "custom": K},
    {"card_id": "gs005", "type": "Event", "name": "Solar Flare", "subtitle": "",
     "desc": {"Cost": "2", "RES": "Y", "Class": "Hero"},
     "traits": ["ATTACK", "SUPERPOWER"], "set_name": SET,
     "text": "<b>Hero Action</b> <i>(attack)</i>: Deal 4 damage to an enemy. If you have at least [energy][energy] resources in your hand, deal 2 additional damage to that enemy.\n"
             "<i>\"You like bombs so much? I will bring you a bomb you will never forget!\" —Binary</i>",
     "custom": K},
    {"card_id": "gs006", "type": "Resource", "name": "Energy Torrent", "subtitle": "",
     "desc": {"RES": "YY", "Class": "Hero"},
     "traits": [], "set_name": SET,
     "text": "<b>Response</b>: After you spend this card, shuffle it into your deck.\n<i>\"Here come the reserves!\" —Binary</i>",
     "custom": K},
    {"card_id": "gs007", "type": "Support", "name": "* Prophet-Singer", "subtitle": "",
     "desc": {"Cost": "0", "RES": "R", "Class": "Hero"},
     "traits": ["AERIAL", "CREATURE"], "set_name": SET,
     "text": "<b>Action</b>: Exhaust Prophet-Singer → look at the top card of your deck and swap it with a card in your hand.\n"
             "<i>The Prophet-Singer is the leader of the Acanti, giant spacefaring beings that travel the stars, guided by song and spirit.</i>",
     "custom": K},
    {"card_id": "gs008", "type": "Support", "name": "White Hole", "subtitle": "",
     "desc": {"Cost": "2", "RES": "R", "Class": "Hero"},
     "traits": ["LOCATION"], "set_name": SET,
     "text": "<b>Hero Action</b>: Exhaust White Hole → discard cards from the top of your deck until you discard a card with a printed [energy] resource. Add that card to your hand.\n"
             "<i>A white hole is the endless source of cosmic energy Binary can harness.</i>",
     "custom": K},
    {"card_id": "gs009", "type": "Upgrade", "name": "Body in Flames", "subtitle": "",
     "desc": {"Cost": "2", "RES": "R", "Class": "Hero"},
     "traits": ["CONDITION", "SUPERPOWER"], "set_name": SET,
     "text": "While the number of [energy] resources in your hand is equal to:\n• 1 or 2 - Binary gains retaliate 1.\n"
             "• 3 or 4 - Binary gains retaliate 2.\n• 5 or more - Binary gains retaliate 3.",
     "custom": K},
    {"card_id": "gs010", "type": "Upgrade", "name": "Energy Conversion", "subtitle": "",
     "desc": {"Cost": "0", "RES": "B", "Class": "Hero", "Temporary": "1"},
     "traits": ["SUPERPOWER"], "set_name": SET,
     "text": "Temporary.\nTreat the printed resources of each card in your hand as if they were [energy] resources.\n"
             "<i>\"No time to dawdle, sprout-sprats. Getting a mite unhealthy out here.\" —Binary</i>",
     "custom": K},
    {"card_id": "gs011", "type": "Upgrade", "name": "Light, Radiation, Heat", "subtitle": "",
     "desc": {"Cost": "1", "RES": "B", "Class": "Hero"},
     "traits": ["SUPERPOWER"], "set_name": SET,
     "text": "While the number of [energy] resources in your hand is at least:\n• 1 - Your basic attacks gain ranged.\n"
             "• 2 - Your basic attacks also gain piercing.\n• 3 - Your basic attacks also gain overkill.",
     "custom": K},
    {"card_id": "gs031", "type": "Obligation", "name": "Forgotten Life", "subtitle": "",
     "desc": {"Boost": "2", "GiveTo": "Carol Danvers"},
     "traits": [], "set_name": SET,
     "text": "<b><i>Give to the Carol Danvers player.</i></b>\nWhile in hero form, your hand size is reduced by 1.\n"
             "<b>Alter-Ego Action</b>: Exhaust Carol Danvers and discard an identity-specific card from your hand → remove Forgotten Life from the game.",
     "custom": K},
    {"card_id": "gs032", "type": "Minion", "name": "* Rogue", "subtitle": "",
     "desc": {"HP": "5", "SCH": "2", "ATK": "2", "Boost": "2", "Nemesis": "Binary"},
     "traits": ["BROTHERHOOD OF MUTANTS", "ELITE"], "set_name": NEM,
     "text": "<b>Forced Response</b>: After the player phase begins, find Touched and attach it to a character other than Rogue. If it is a friendly character, exhaust that character.\n"
             "<b>When Defeated</b>: Discard Touched.\n<i>(Binary's nemesis minion.)</i>",
     "custom": K},
    {"card_id": "gs237", "type": "Attachment", "name": "Touched", "subtitle": "",
     "desc": {},
     "traits": ["CONDITION"], "set_name": NEM,
     "text": "If Rogue is in play, attach to a character other than Rogue. Otherwise, this card gains surge.\n"
             "While Touched is attached to a:\n• Minion, Rogue gains retaliate 2.\n• Villain, reduce the damage Rogue takes from each attack by 2.\n"
             "• Ally, Rogue gets +2 ATK.\n• Identity, Rogue gains villainous.",
     "custom": K},
    {"card_id": "gs239", "type": "SideScheme", "name": "Goin' Rogue", "subtitle": "",
     "desc": {"StartingThreat": "2*", "Hazard": "1", "Boost": "2"},
     "traits": [], "set_name": NEM,
     "text": "<i>\"Any chance you can give me a top-off?\" —Rogue</i>\n"
             "While Touched is attached to a friendly character, Rogue gets +1 SCH.\n"
             "While Touched is attached to an enemy character, Rogue gets +1 ATK.",
     "custom": K},
    {"card_id": "gs240", "type": "Treachery", "name": "Energy Transfer", "subtitle": "",
     "desc": {"Boost": "1"},
     "traits": [], "set_name": NEM,
     "text": "<b>When Revealed</b>: Discard each [energy] resource from your hand. If no card was discarded this way, take 3 damage.\n"
             "<i>\"Been itchin' to finish what I started all those years ago — and this time, I'm not leavin' enough of you for anyone to save.\" —Rogue</i>",
     "custom": K},
]
