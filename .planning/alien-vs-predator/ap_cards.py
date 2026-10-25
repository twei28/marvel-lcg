# Definitions des cartes ALIEN VS PREDATOR (RyCoRan, « Custom Content By: RyCoRan », 06-26), 25/10/2026.
# Relues une a une contre les scans (zip « Alien vs Predator (06-26) », 60 images). Transcriptions : docs/packs/alien-vs-predator/TRANSCRIPTIONS.md.
# Icones identifiees par COMPARAISON AVEC LES GLYPHES de public/fonts/ChampionsIcons.ttf (mots-cles/hazard.md) : Expanding Hive, Skulls for the
# Taking = Acceleration (A) ; 3B, 4B = Hazard (H) ; Swarm Breaker = Acceleration + Hazard.
# Doublons du zip (verifies au pixel pres hors pied) : Thermal Target 13-14, Facehugger 16-17, Xenomorph Drone 18-19. Les deux « Advance » sont
# deux cartes (Advance / Advance Again). Alien Scout : 4 versions, 4 exemplaires chacune (deck Xenomorph de 16 cartes).
# Numerotation : ap + numero imprime (faces a/b pour les mechants et complots) ; ap101-ap104 Alien Scout ; ap201-ap207 Apex Standard ;
# ap301-ap306 Clan Yautja. Inseres par inserer_avp.py (idempotent).

K = "RyCoRan"
SET = "Alien vs. Predator"
XENO = "Xenomorph Deck"
STD = "Apex Standard"
CLAN = "Clan Yautja"

PLACE = "[star] When {nom} schemes, place that threat on {pos} side scheme instead of the main scheme, if able."
QUEEN = (PLACE.format(nom="Alien Queen", pos="her") + "\n[star] <b>Forced Response</b>: After Alien Queen attacks and damages a character you control, "
         "shuffle a Xenomorph card into your deck.\n<b>When Defeated</b>: Flip this card.")
WARLORD = (PLACE.format(nom="Predator Warlord", pos="his") + "\n[star] <b>Forced Interrupt</b>: When Predator Warlord attacks, either place 2 threat "
           "on the main scheme or he gets +1 ATK for this attack.\n<b>When Defeated</b>: Flip this card.")


def defaite(soigne, autre, pronom, stade):
    return (f"<b>When Revealed</b>: Heal {soigne}[per_hero] damage from {autre} and give {pronom} a tough status card. Advance to stage {stade}. "
            "Remove each permanent side scheme and this card from the game.")


def vilain(cid, nom, trait, sch, atk, hp, texte, mode, soigne, autre, pronom, stade):
    return [
        {"card_id": cid + "a", "type": "Villain", "name": f"* {nom}", "subtitle": "",
         "desc": {"HP": f"{hp}*", "ATK": str(atk), "SCH": str(sch), "Stage": mode}, "traits": [trait], "set_name": SET, "text": texte, "custom": K},
        {"card_id": cid + "b", "type": "Villain", "name": f"* {nom}", "subtitle": "",
         "desc": {"HP": f"{hp}*", "ATK": "0", "SCH": "0", "Stage": mode}, "traits": ["DEFEATED", trait], "set_name": SET,
         "text": defaite(soigne, autre, pronom, stade), "custom": K},
    ]


def scout(cid, sch, atk, mots, desc_extra, pioche):
    interrupt = ("<b>Forced Interrupt</b>: When you would draw or discard this card from your deck, "
                 + ("draw 1 card. Deal this card to yourself as a facedown encounter card." if pioche
                    else "deal this card to yourself as a facedown encounter card."))
    d = {"HP": "2", "ATK": str(atk), "SCH": str(sch)}
    d.update(desc_extra)
    return {"card_id": cid, "type": "Minion", "name": "Alien Scout", "subtitle": "", "desc": d, "traits": ["XENOMORPH"], "set_name": XENO,
            "text": (mots + "\n" if mots else "") + interrupt + "\n<b>When Defeated</b>: Place Alien Scout in your discard pile.", "custom": K}


CARDS = (
    vilain("ap001", "Alien Queen", "XENOMORPH", 2, 1, 18, QUEEN, "A", 4, "Predator Warlord", "him", "3A")
    + vilain("ap002", "Predator Warlord", "YAUTJA", 1, 2, 16, WARLORD, "A", 4, "Alien Queen", "her", "4A")
    + vilain("ap003", "Alien Queen", "XENOMORPH", 2, 2, 18, QUEEN, "B", 6, "Predator Warlord", "him", "3A")
    + vilain("ap004", "Predator Warlord", "YAUTJA", 1, 3, 16, WARLORD, "B", 6, "Alien Queen", "her", "4A")
    + [
    {"card_id": "ap005a", "type": "MainScheme", "name": "The Ultimate Hunt", "subtitle": "", "desc": {"Stage": "1"}, "traits": [], "set_name": SET,
     "text": "<b>Contents</b>: Alien Queen (A) and Predator Warlord (A) <i>(B instead in expert mode)</i>. Alien vs. Predator, Xenomorph deck, Apex Standard "
             "and one modular encounter set <i>(Clan Yautja)</i>.\n<b>Setup</b>: Put Skulls for the Taking and Expanding Hive into play. Place the Xenomorph "
             "deck next to Alien Queen and place the active counter on her.", "custom": K},
    {"card_id": "ap005b", "type": "MainScheme", "name": "The Ultimate Hunt", "subtitle": "",
     "desc": {"StartingThreat": "0", "TargetThreat": "8*", "EscalationThreat": "1*", "Stage": "1"}, "traits": [], "set_name": SET,
     "text": "<i>Two apex species collide. A Predator hunt. An Alien Hive. Earth becomes their battleground.</i>\n"
             "[star] <b>Forced Response</b>: After resolving step one of the villain phase, if there is no threat on each villain's side scheme, deal 2 damage "
             "to each villain.\n<b>Forced Response</b>: After a villain activates, move the active counter to the next villain.", "custom": K},
    {"card_id": "ap006a", "type": "MainScheme", "name": "Battleground Earth", "subtitle": "", "desc": {"Stage": "2"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: Each player searches the encounter deck and discard pile for a [[YAUTJA]] minion and a [[XENOMORPH]] minion and puts them "
             "into play engaged with them. Shuffle the encounter deck.", "custom": K},
    {"card_id": "ap006b", "type": "MainScheme", "name": "Battleground Earth", "subtitle": "",
     "desc": {"StartingThreat": "2*", "EscalationThreat": "1*", "Stage": "2"}, "traits": [], "set_name": SET,
     "text": "<b>Forced Response</b>: After a villain attacks, give them a facedown boost card, then move the active counter to the next villain.\n"
             "<b>Forced Response</b>: After threat is placed here, if there is at least 4[per_hero] threat here, deal each player a facedown encounter card. "
             "Then, remove 2[per_hero] threat from this scheme.", "custom": K},
    {"card_id": "ap007a", "type": "MainScheme", "name": "Predator's Pursuit", "subtitle": "", "desc": {"Stage": "3"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: Discard cards from the top of the encounter deck until a [[WEAPON]] attachment is discarded. Reveal it.", "custom": K},
    {"card_id": "ap007b", "type": "MainScheme", "name": "Predator's Pursuit", "subtitle": "",
     "desc": {"StartingThreat": "1*", "TargetThreat": "8*", "EscalationThreat": "1*", "Stage": "3", "Hazard": "1"}, "traits": [], "set_name": SET,
     "text": "Predator Warlord is the active villain.\n<b>When Revealed</b>: Each player searches the encounter deck and discard pile for a [[YAUTJA]] minion "
             "and reveals it.\n<b>If this stage is completed, the players lose the game.</b>", "custom": K},
    {"card_id": "ap008a", "type": "MainScheme", "name": "Queen's Dominion", "subtitle": "", "desc": {"Stage": "4"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: Discard cards from the top of the encounter deck until a [[XENOMORPH]] attachment is discarded. Reveal it.", "custom": K},
    {"card_id": "ap008b", "type": "MainScheme", "name": "Queen's Dominion", "subtitle": "",
     "desc": {"StartingThreat": "1*", "TargetThreat": "8*", "EscalationThreat": "1*", "Stage": "4", "Hazard": "1"}, "traits": [], "set_name": SET,
     "text": "Alien Queen is the active villain.\n<b>When Revealed</b>: Each player searches the encounter deck and discard pile for a [[XENOMORPH]] minion "
             "and reveals it.\n<b>If this stage is completed, the players lose the game.</b>", "custom": K},
    {"card_id": "ap009", "type": "SideScheme", "name": "Expanding Hive", "subtitle": "",
     "desc": {"StartingThreat": "2*", "Acceleration": "1", "Permanent": "1"}, "traits": [], "set_name": SET,
     "text": "Alien Queen's Scheme. Permanent.\nWhile there is no threat here, this scheme loses the [acceleration] icon.\n"
             "<b>Forced Interrupt</b>: When a minion with 3 or more printed hit points is defeated, give it to the active villain as a facedown boost card.", "custom": K},
    {"card_id": "ap010", "type": "SideScheme", "name": "Skulls for the Taking", "subtitle": "",
     "desc": {"StartingThreat": "2*", "Acceleration": "1", "Permanent": "1"}, "traits": [], "set_name": SET,
     "text": "Predator Warlord's Scheme. Permanent.\nWhile there is no threat here, this scheme loses the [acceleration] icon.\n"
             "<b>Forced Response</b>: After an ally is defeated by an enemy attack, tuck it under here.", "custom": K},
    {"card_id": "ap011", "type": "Attachment", "name": "Plasmacaster", "subtitle": "", "desc": {"Boost": "2", "Uses": "3,plasma"}, "traits": ["WEAPON"], "set_name": SET,
     "text": "Attach to Predator Warlord. Otherwise, this card gains surge.\nUses (3 plasma counters).\n[star] <b>Forced Interrupt</b>: When Predator Warlord "
             "attacks you, remove 1 plasma counter from here and discard the top card of your deck → take indirect damage equal to that card's printed cost.", "custom": K},
    {"card_id": "ap012", "type": "Attachment", "name": "* Yautja Wrist Blades", "subtitle": "", "desc": {"Boost": "2", "ATK+": "2"}, "traits": ["WEAPON"], "set_name": SET,
     "text": "Attach to Predator Warlord. If you cannot, attach to a [[YAUTJA]] minion. Otherwise, this card gains surge.\n[star] Attached enemy's attacks gain "
             "piercing.\n<b>Hero Action</b>: Spend [energy][physical] resources → discard this card.", "custom": K},
    {"card_id": "ap013", "type": "Attachment", "name": "Thermal Target", "subtitle": "", "desc": {"Boost": "1**"}, "traits": ["CONDITION", "YAUTJA"], "set_name": SET,
     "text": "Attach to your identity.\n<b>Forced Response</b>: After your turn ends, take 2 damage and place 2 threat on the main scheme.\n"
             "<b>Alter-Ego Action</b>: Find a [[YAUTJA]] minion and reveal it → discard this card.\n[star] <b>Boost</b>: Reveal this card.", "custom": K},
    {"card_id": "ap015", "type": "Attachment", "name": "* Piercing Pharynx", "subtitle": "", "desc": {"Boost": "1**", "ATK+": "1"}, "traits": ["CONDITION", "XENOMORPH"],
     "set_name": SET,
     "text": "Attach to Alien Queen and give her a tough status card. Otherwise, this card gains surge.\nAlien Queen gains retaliate 1.\n<b>Hero Action</b>: If "
             "Predator Warlord is in play, spend [energy][mental] resources → discard this card.\n[star] <b>Boost</b>: Reveal this card.", "custom": K},
    {"card_id": "ap016", "type": "Attachment", "name": "Facehugger", "subtitle": "", "desc": {"Boost": "1"}, "traits": ["CONDITION", "XENOMORPH"], "set_name": SET,
     "text": "Attach to your identity.\n<b>Forced Response</b>: After your turn ends, take 2 damage and place 2 threat on the main scheme.\n"
             "<b>Alter-Ego Action</b>: Search the encounter deck and discard pile for a [[XENOMORPH]] minion and reveal it → discard this card.", "custom": K},
    {"card_id": "ap018", "type": "Minion", "name": "Xenomorph Drone", "subtitle": "", "desc": {"HP": "3", "ATK": "2", "SCH": "0", "Boost": "2", "Guard": "1", "Incite": "2"},
     "traits": ["XENOMORPH"], "set_name": SET,
     "text": "Guard. Incite 2 (3 instead if Alien Queen is the active villain).\n<b>When Defeated</b>: Remove 2 threat from Expanding Hive. If you cannot, shuffle "
             "Xenomorph Drone into the encounter deck.", "custom": K},
    {"card_id": "ap020", "type": "Minion", "name": "Xenomorph Warrior", "subtitle": "", "desc": {"HP": "6", "ATK": "2", "SCH": "1", "Boost": "1", "Quickstrike": "1"},
     "traits": ["XENOMORPH"], "set_name": SET,
     "text": "Quickstrike.\n<b>When Defeated</b>: Discard the top card of the encounter deck and deal 1 damage to a [[YAUTJA]] enemy for each icon ([star] and "
             "[boost]) in that card's boost area.", "custom": K},
    {"card_id": "ap021", "type": "Minion", "name": "* Alien Praetorian", "subtitle": "", "desc": {"HP": "8", "ATK": "2", "SCH": "2", "Boost": "3", "Villainous": "1"},
     "traits": ["ELITE", "XENOMORPH"], "set_name": SET,
     "text": "Villainous.\n<b>Forced Response</b>: After the villain phase begins, Alien Praetorian engages the first player.", "custom": K},
    {"card_id": "ap022", "type": "Attachment", "name": "Chestburster", "subtitle": "", "desc": {"Boost": "2", "ATK+": "2"}, "traits": ["CONDITION"], "set_name": SET,
     "text": "Attach to a [[XENOMORPH]] minion. Otherwise attach to the active villain.\n[star] <b>Forced Interrupt</b>: When attached enemy attacks, this attack "
             "gains piercing. At the end of this attack, stun your identity and discard this card.", "custom": K},
    {"card_id": "ap023", "type": "Treachery", "name": "Hive Incursion", "subtitle": "", "desc": {"Boost": "0**"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: Discard your hand. Draw up to your hand size.\n[star] <b>Boost</b>: Resolve the \"<b>When Revealed</b>\" ability on this card.", "custom": K},
    {"card_id": "ap024", "type": "Treachery", "name": "Predator's Prize", "subtitle": "", "desc": {"Boost": "3"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: Choose to either give this card to the active villain as a facedown boost card, or find your identity-specific ally and "
             "remove it from the game.", "custom": K},
    {"card_id": "ap025", "type": "SideScheme", "name": "Brood Breakout", "subtitle": "", "desc": {"StartingThreat": "4", "Boost": "3"}, "traits": [], "set_name": SET,
     "text": "<b>Forced Response</b>: After a [[XENOMORPH]] minion enters play, give it a tough status card.\n<b>When Revealed</b>: Discard cards from the top of "
             "the encounter deck until a [[XENOMORPH]] minion is discarded. Reveal it.", "custom": K},
    {"card_id": "ap026", "type": "Treachery", "name": "Alien Assault", "subtitle": "", "desc": {"Boost": "1**"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: If Predator Warlord is the active villain, stun your identity. If Alien Queen is the active villain, confuse your identity.\n"
             "[star] <b>Boost</b>: After this activation ends, do not move the active counter to the next villain.", "custom": K},
    {"card_id": "ap027", "type": "Treachery", "name": "Killing Ground", "subtitle": "", "desc": {"Boost": "2"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: Move all threat from the villain's side scheme with the most threat to the main scheme. If no threat was moved this way, "
             "exhaust your identity. If you cannot, stun or confuse your identity.", "custom": K},
    {"card_id": "ap028", "type": "Treachery", "name": "Predator's Prey", "subtitle": "", "desc": {"Boost": "1"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: Discard cards from the top of your deck until you discard an ally, then put that ally into play under your control. The active "
             "villain attacks that ally. This attack gains overkill.", "custom": K},
    {"card_id": "ap029", "type": "Treachery", "name": "Predation", "subtitle": "", "desc": {"Boost": "2**"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: Heal 3 damage from the active villain and give them a tough status card. Deal 3 damage to an enemy whose trait does not match "
             "the active villain.\n[star] <b>Boost</b>: Place 2 threat on each scheme.", "custom": K},
    {"card_id": "ap030", "type": "Treachery", "name": "Trophy Taken", "subtitle": "", "desc": {"Boost": "2"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: The active villain attacks the friendly character with the fewest remaining hit points. If this attack defeats an ally, remove "
             "that ally from the game.", "custom": K},
    {"card_id": "ap031", "type": "Treachery", "name": "Lethal Ambush", "subtitle": "", "desc": {"Boost": "2"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: Discard the top 7 cards of the encounter deck. Put the first minion discarded this way into play engaged with you. Then, the "
             "villain and each minion engaged with you attacks you.", "custom": K},
    {"card_id": "ap032", "type": "SideScheme", "name": "Swarm Breaker", "subtitle": "",
     "desc": {"StartingThreat": "4", "Boost": "2", "Acceleration": "1", "Hazard": "1", "Hinder": "1*", "Victory": "0"}, "traits": [], "set_name": SET,
     "text": "<i>Dark shapes swarm across the battlefield, relentless and numerous. A whirlwind of thunder and steel splits the sky. Their attack falters, if only "
             "for a moment...</i>\nHinder 1[per_hero]. Victory 0.\n<b>When Defeated</b>: Deal 2[per_hero] damage to each enemy.", "custom": K},
    {"card_id": "ap033", "type": "SideScheme", "name": "Alien Onslaught", "subtitle": "", "desc": {"StartingThreat": "4", "Boost": "2", "Hinder": "2*"}, "traits": [],
     "set_name": SET,
     "text": "Hinder 2[per_hero].\n<b>When Revealed</b>: Each player discards the top 2[per_hero] of their deck. Place 1 acceleration token here for each "
             "[[XENOMORPH]] minion discarded this way.\n<b>Forced Response</b>: After you thwart this scheme, discard the top 2[per_hero] cards of your deck.", "custom": K},
    # ---------------------------------------------------------------- deck Xenomorph (16 cartes)
    scout("ap101", 1, 1, "Surge.", {"Surge": "1"}, True),
    scout("ap102", 1, 1, "Guard.", {"Guard": "1"}, False),
    scout("ap103", 1, 1, "Incite 1. Surge.", {"Incite": "1", "Surge": "1"}, True),
    scout("ap104", 1, 2, "Teamwork ([[XENOMORPH]]).", {"Teamwork": "XENOMORPH"}, True),
    # ---------------------------------------------------------------- Apex Standard (7 cartes)
    {"card_id": "ap201", "type": "Treachery", "name": "Advance", "subtitle": "", "desc": {"Boost": "1"}, "traits": [], "set_name": STD,
     "text": "<b>When Revealed</b>: The villain schemes. Place this threat on the main scheme.", "custom": K},
    {"card_id": "ap202", "type": "Treachery", "name": "Advance Again", "subtitle": "", "desc": {"Boost": "1"}, "traits": [], "set_name": STD,
     "text": "<b>When Revealed</b>: The villain schemes. Do not move the active villain counter.", "custom": K},
    {"card_id": "ap203", "type": "Treachery", "name": "Assault", "subtitle": "", "desc": {"Boost": "1"}, "traits": [], "set_name": STD,
     "text": "<b>When Revealed (Alter-Ego)</b>: This card gains surge.\n<b>When Revealed (Hero)</b>: The villain attacks you. Do not move the active villain counter.", "custom": K},
    {"card_id": "ap204", "type": "Treachery", "name": "Cruel Intentions", "subtitle": "", "desc": {"Boost": "1**", "Incite": "1"}, "traits": [], "set_name": STD,
     "text": "Incite 1.\n<b>When Revealed</b>: Deal each player 1 facedown encounter card. Give the villain 1 facedown boost card.\n[star] <b>Boost</b>: Deal yourself 1 "
             "facedown encounter card.", "custom": K},
    {"card_id": "ap205", "type": "Treachery", "name": "Overwhelming Force", "subtitle": "", "desc": {"Boost": "2**"}, "traits": [], "set_name": STD,
     "text": "<b>When Revealed</b>: Discard the highest cost upgrade or support you control. If no card was discarded this way, this card gains surge.\n[star] "
             "<b>Boost</b>: Give the villain 1 additional boost card for this activation.", "custom": K},
    {"card_id": "ap206", "type": "Treachery", "name": "Masterplan", "subtitle": "", "desc": {"Boost": "2"}, "traits": [], "set_name": STD,
     "text": "<b>When Revealed</b>: Place 4 threat on each side scheme. If there are no side schemes in play, discard cards from the top of the encounter deck "
             "until a side scheme is discarded. Reveal that side scheme.", "custom": K},
    {"card_id": "ap207", "type": "Treachery", "name": "Shadow of the Past", "subtitle": "", "desc": {"Boost": "2"}, "traits": [], "set_name": STD,
     "text": "<b>When Revealed</b>: Reveal your set-aside nemesis minion and put it into play engaged with you. Reveal your set-aside nemesis side scheme and put "
             "it into play. Shuffle the rest of your set-aside nemesis encounter set into the encounter deck. If your nemesis minion does not enter the game this "
             "way, this card gains surge.", "custom": K, "ability_link": "01190"},
    # ---------------------------------------------------------------- Clan Yautja (6 cartes)
    {"card_id": "ap301", "type": "Minion", "name": "* Yautja Young Blood", "subtitle": "", "desc": {"HP": "4", "ATK": "1", "SCH": "1", "Boost": "1", "Patrol": "1", "Incite": "2"},
     "traits": ["YAUTJA"], "set_name": CLAN,
     "text": "Patrol. Incite 2 (3 instead if Predator Warlord is the active villain).\n<b>When Defeated</b>: Place 2 threat on The Ultimate Hunt, if you cannot "
             "shuffle Yautja Young Blood into the encounter deck.", "custom": K},
    {"card_id": "ap302", "type": "Minion", "name": "* Blooded Predator", "subtitle": "", "desc": {"HP": "4", "ATK": "2", "SCH": "2", "Boost": "3"}, "traits": ["YAUTJA"],
     "set_name": CLAN,
     "text": "<b>When Revealed</b>: Stun your identity. If you are already stunned, take 3 damage.\n<b>When Defeated</b>: Give Predator Warlord a tough status card. "
             "If you cannot, give this card to the active villain as a facedown boost card.", "custom": K},
    {"card_id": "ap303", "type": "Minion", "name": "* Predator Elite", "subtitle": "", "desc": {"HP": "6", "ATK": "2", "SCH": "2", "Boost": "2"}, "traits": ["ELITE", "YAUTJA"],
     "set_name": CLAN,
     "text": "<b>When Revealed</b>: Discard an upgrade or support you control.\n<b>When Defeated</b>: Discard the top card of your deck and deal damage to a "
             "[[XENOMORPH]] enemy equal to that cards printed cost.", "custom": K},
    {"card_id": "ap304", "type": "Minion", "name": "* Apex Predator", "subtitle": "", "desc": {"HP": "7", "ATK": "3", "SCH": "1", "Boost": "2", "Toughness": "1"},
     "traits": ["ELITE", "YAUTJA"], "set_name": CLAN,
     "text": "Toughness.\n[star] Apex Predator's attacks gain piercing.\n<b>Forced Response</b>: After a character attacks Apex Predator, discard the top card of "
             "the encounter deck. If that card is a treachery, stun the attacker.", "custom": K},
    {"card_id": "ap305", "type": "SideScheme", "name": "The Hunt Begins", "subtitle": "", "desc": {"StartingThreat": "5", "Boost": "2"}, "traits": [], "set_name": CLAN,
     "text": "Allies cannot defend against enemy attacks.\n<b>Forced Response</b>: After a [[YAUTJA]] enemy attacks, give it a tough status card.\n"
             "<b>When Defeated</b>: Stun or confuse an enemy.", "custom": K},
    {"card_id": "ap306", "type": "Attachment", "name": "Cloaking Device", "subtitle": "", "desc": {"Boost": "1"}, "traits": ["WEAPON"], "set_name": CLAN,
     "text": "Attach to Predator Warlord. If you cannot, attach to a [[YAUTJA]] minion. Otherwise, this card gains surge.\nReduce the amount of damage attached enemy "
             "takes from each attack by 2.\n<b>Hero Action</b>: After a hero makes a basic attack against this enemy, spend [energy][physical] resources → "
             "discard this card.", "custom": K},
])
