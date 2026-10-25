# Definitions des cartes PREDATOR (RyCoRan, zip « Predator (5-25 Final) »), 25/10/2026.
# Relues une a une contre les scans. Icones de ressource verifiees contre les trois ressources de base du MEME pack
# (« Predator Resources ») : eclair jaune = energie (Y), noeuds bleus = mental (B, « Genius »), poing = physique (R,
# « Strength »), etoile verte = wild (G). Les deux « Y » rouges du coin des cartes de rencontre sont des icones de
# BOOST ordinaires (cadre de rencontre) ; l'icone « etoile » rouge ronde est l'icone de boost a ETOILE (« [star] Boost »).
# Inseres dans data/cards.json par inserer_predator.py (idempotent).

K = "RyCoRan"
SET = "Predator"
NEM = "Predator Nemesis"
ALT = "Predator Alt Nemesis"


def hero(cid, typ, nom, desc, traits, texte):
    return {"card_id": cid, "type": typ, "name": nom, "subtitle": "", "desc": desc, "traits": traits,
            "set_name": SET, "text": texte, "custom": K}


def carte(cid, typ, nom, desc, traits, texte, sset=SET, subtitle=""):
    return {"card_id": cid, "type": typ, "name": nom, "subtitle": subtitle, "desc": desc, "traits": traits,
            "set_name": sset, "text": texte, "custom": K}


CARDS = [
    hero("pd001a", "Hero", "* Predator",
         {"HP": "13", "ATK": "3", "THW": "0", "DEF": "2", "HS": "5"}, ["SOLDIER", "YAUTJA"],
         '<b>Response</b>: After a minion enters play, attach Infralocked to it.\n'
         '<i>Camouflaged Hunter</i> — <b>Response</b>: After you defeat a minion, give Predator a cloaked status card.'),
    hero("pd001b", "AlterEgo", "* Yd'Nar",
         {"HP": "13", "REC": "4", "HS": "6"}, ["SOLDIER", "YAUTJA"],
         '<b>Setup</b>: Put Infralocked into play.\n'
         '<i>Future Trophy</i> — <b>Action</b>: Discard cards from the top of your deck until you discard an upgrade, '
         'then add that card to your hand. <i>(Limit once per round.)</i>'),
    hero("pd002", "Upgrade", "* Infralocked",
         {"Cost": "0", "Permanent": "1", "Class": "Hero"}, ["TACTIC"],
         'Permanent.\n<b>Hero Interrupt</b>: When Predator defeats attached minion, remove 2 threat from a scheme '
         '(3 threat instead from a side scheme). Then, return this card to your play area.'),
    dict(hero("pd003", "PlayerMinion", "Xenomorph",
         {"Cost": "0", "RES": "G", "HP": "4", "SCH": "0", "ATK": "2", "Teamwork": "XENOMORPH", "Class": "Hero"},
         ["XENOMORPH"],
         'Teamwork ([[XENOMORPH]]).\n<b>When Defeated</b>: Ready Predator.\n'
         '<b>Interrupt</b>: When Xenomorph is defeated, shuffle it into your deck.'), subtitle="Warrior"),
    hero("pd004", "Event", "Ghost Protocol",
         {"Cost": "1", "RES": "Y", "Class": "Hero"}, ["THWART"],
         '<b>Hero Action</b> <i>(thwart)</i>: Remove 2 threat from a scheme (4 threat instead if you are cloaked).'),
    hero("pd005", "Event", "Spine Rip",
         {"Cost": "3", "RES": "R", "Class": "Hero"}, ["ATTACK"],
         '<b>Hero Action</b> <i>(attack)</i>: Deal 7 damage to an enemy. If that enemy has Infralocked attached, '
         'this attack gains overkill.'),
    hero("pd006", "Event", "Shadow Counter",
         {"Cost": "1", "RES": "B", "Class": "Hero"}, ["DEFENSE"],
         '<b>Hero Interrupt</b> <i>(defense)</i>: When you would take any amount of damage, prevent 3 of that damage. '
         'Then, give Predator a cloaked status card.'),
    hero("pd007", "Event", "Savage Skewer",
         {"Cost": "2", "RES": "R", "Class": "Hero"}, ["ATTACK", "TACTIC"],
         '<b>Hero Action</b> <i>(attack)</i>: Deal 5 damage to an enemy. You may discard a cloaked status card to '
         'either stun and confuse that enemy or discard an attachment on that enemy with the text '
         '"<b>Hero Action</b>" or "<b>Hero Response</b>".'),
    hero("pd008", "Event", "Jungle Stalk",
         {"Cost": "0", "RES": "B", "Class": "Hero"}, ["TACTIC"],
         '<b>Hero Action</b>: Find a minion and put it into play engaged with you → heal damage from your hero for '
         "each icon ([star] and [boost]) in that card's boost area and give Predator a cloaked status card."),
    hero("pd009", "PlayerSideScheme", "* Honor Hunt",
         {"Cost": "0", "RES": "G", "StartingThreat": "5", "Assault": "1", "Victory": "0", "Class": "Hero"}, [],
         'Victory 0. Assault. <i>(Basic thwarts against this scheme use ATK instead of THW.)</i>\n'
         'While Honor Hunt is in the victory display, it gains "<b>Action</b>: Find a minion and put it into play '
         'engaged with you. Any player may trigger this ability. <i>(Limit once per round)</i>."'),
    hero("pd010", "Support", "* Yautja Trophy Room",
         {"Cost": "2", "RES": "B", "Class": "Hero"}, ["LOCATION"],
         '<b>Response</b>: After you defeat a minion, place 1 skull counter here.\n'
         '<b>Resource</b>: Exhaust Yautja Trophy Room and remove X skull counters from it → generate X [wild] resources.'),
    hero("pd011", "Upgrade", "* Self Destruct",
         {"Cost": "2", "RES": "YY", "Class": "Hero"}, ["TECH", "WEAPON"],
         '<b>Hero Action</b>: Exhaust this card → place 2 glyph counters here.\n'
         '<b>Hero Action</b>: Remove this card from the game → deal 1 damage to the villain and each minion engaged '
         'with you (to a maximum of 10) for each glyph counter here.'),
    hero("pd012", "Upgrade", "Yautja Wrist Blades",
         {"Cost": "1", "RES": "R", "Class": "Hero"}, ["TECH", "WEAPON"],
         'Predator gains retaliate 1 and his basic attacks gain piercing.'),
    hero("pd013", "Upgrade", "* Plasmacaster",
         {"Cost": "2", "RES": "Y", "Class": "Hero"}, ["TECH", "WEAPON"],
         '<b>Hero Action</b> <i>(attack)</i>: Exhaust Plasmacaster → deal 2 damage to an enemy (3 damage instead if '
         'that enemy has an upgrade attached). This attack gains ranged.'),
    hero("pd014", "Upgrade", "* Bio-Helmet",
         {"Cost": "2", "RES": "B", "Class": "Hero"}, ["ARMOR", "TECH"],
         '<b>Hero Action</b>: Exhaust Bio-Helmet → look at the top card of the encounter deck. For each icon '
         "([star] and [boost]) in that card's boost area, remove 1 threat from a scheme."),
    hero("pd015", "Obligation", "Exposed Target",
         {"Boost": "2", "GiveTo": "Yd'Nar"}, [],
         "<b><i>Give to the Yd'Nar player.</i></b>\nYou may flip to alter-ego form. Choose:\n"
         "• Exhaust Yd'Nar → remove Exposed Target from the game.\n"
         "• Discard each cloaked status card from your identity and 1 [[TECH]] upgrade you control. "
         "If no cards were discarded this way, this card gains surge. Discard this obligation."),

    # ---- set nemesis Xenomorph (5 cartes) ----
    carte("pd016", "SideScheme", "Xenomorph's Prey",
          {"StartingThreat": "3*", "Boost": "2", "Hazard": "1"}, [],
          "<i>Once the hunter, now the hunted. The Xenomorph's Queen has marked her prey.</i>\n"
          "While this card is in play, Predator cannot gain cloaked status cards.\n"
          "<b>When Revealed</b>: Place 1 additional threat here for each status card in play.", NEM),
    carte("pd017", "Minion", "* Xenomorph Queen",
          {"HP": "9", "SCH": "1", "ATK": "3*", "Boost": "2", "Toughness": "1", "Nemesis": "Predator"},
          ["ELITE", "XENOMORPH"],
          "Toughness.\n[star] Xenomorph Queen's attacks gain piercing and overkill.\n"
          "<i>(Predator's nemesis minion.)</i>", NEM),
    carte("pd018", "Minion", "* Xenomorph Drone",
          {"HP": "3", "SCH": "1", "ATK": "2", "Boost": "1**", "Guard": "1", "Teamwork": "XENOMORPH"},
          ["XENOMORPH"],
          "Guard. Teamwork ([[XENOMORPH]]).\n<b>Forced Response</b>: After Xenomorph Drone engages you, if there are no "
          "other minions engaged with you, deal yourself 1 facedown encounter card.\n"
          "<hr />\n[star] <b>Boost</b>: Put Xenomorph Drone into play engaged with you.", NEM),
    carte("pd019", "Treachery", "Hunted By the Hive",
          {"Boost": "2"}, [],
          "<b>When Revealed</b>: Xenomorph Queen attacks you. If it's not in play, find Xenomorph Queen and put it "
          "into play engaged with you.", NEM),
    carte("pd020", "Attachment", "Acid Blood",
          {"Boost": "1"}, ["CONDITION"],
          "Attached minion gets +1 ATK and gains retaliate 1.\n"
          "<b>When Revealed</b>: Find the Xenomorph Queen and put it into play engaged with you and attach this card to it.", NEM),

    # ---- ressources de base a l'art du heros ----
    carte("pd021", "Resource", "Energy", {"RES": "YY", "MaxPerDeck": "1", "Class": "Basic"}, [], "Max 1 per deck."),
    carte("pd022", "Resource", "Genius", {"RES": "BB", "MaxPerDeck": "1", "Class": "Basic"}, [], "Max 1 per deck."),
    carte("pd023", "Resource", "Strength", {"RES": "RR", "MaxPerDeck": "1", "Class": "Basic"}, [], "Max 1 per deck."),

    # ---- evenements Team-Up de base ----
    carte("pd024", "Event", "Razor Hunt",
          {"Cost": "1", "RES": "R", "MaxPerDeck": "1", "TeamUp": "Wolverine;Predator", "Class": "Basic"}, ["ATTACK"],
          "Team-Up (Wolverine and Predator). Max 1 per deck.\n<b>Hero Action</b> <i>(attack)</i>: Deal 1 damage each to "
          "Wolverine and Predator. Deal 3 damage to an enemy. Deal 3 damage to an enemy."),
    carte("pd025", "Event", "Infrared Web",
          {"Cost": "1", "RES": "Y", "MaxPerDeck": "1", "TeamUp": "Spider-Man;Predator", "Class": "Basic"},
          ["ATTACK", "DEFENSE"],
          "Team-Up (Spider-Man and Predator). Max 1 per deck.\n<b>Hero Interrupt</b> <i>(attack/defense)</i>: When an "
          "enemy attack would deal damage to you, prevent 3 of that damage. Deal 3 damage to an enemy."),

    # ---- set nemesis ALTERNATIF (Dutch et son equipe, 5 cartes) ----
    carte("pd026", "SideScheme", "Chopper",
          {"StartingThreat": "3", "Boost": "2", "Hazard": "1", "Permanent": "1"}, [],
          "Permanent.\nWhile there is no threat here, this scheme loses the [hazard] icon.\n"
          "<b>Forced Response</b>: After threat is placed here, if there is at least 8 threat here, the players lose the game.",
          ALT),
    carte("pd027", "Minion", "* Dutch Schaefer",
          {"HP": "6", "SCH": "2*", "ATK": "2*", "Boost": "2", "Toughness": "1", "Nemesis": "Predator"},
          ["ELITE", "SOLDIER"],
          "Toughness.\n[star] <b>Forced Response</b>: After Dutch Schaefer activates, place 1 threat on each scheme.\n"
          "<i>(Predator's nemesis minion.)</i>\n<i>\"You're one ugly mother—.\"</i>", ALT),
    carte("pd028", "Minion", "* Colonel Dillon",
          {"HP": "4", "SCH": "1", "ATK": "2*", "Boost": "2", "Patrol": "1", "Teamwork": "SOLDIER"},
          ["SOLDIER"],
          "Patrol. Teamwork ([[SOLDIER]]).\n[star] <b>Forced Response</b>: After Colonel Dillon attacks you, place 1 threat on each scheme.\n"
          "<i>\"Cause some damn fool accused you of being the best!\" —Dillon</i>", ALT),
    carte("pd029", "Attachment", "M134 Minigun",
          {"Boost": "1"}, ["WEAPON"],
          "Attached minion gets +1 ATK.\nAttach to Dutch Schaefer. If he is not in play, search the encounter deck and discard pile "
          "for him, reveal him and attach this card to him.\n"
          "[star] <b>Forced Response</b>: After Dutch Schaefer attacks you, place 1 threat on the Chopper side scheme.", ALT),
    carte("pd030", "Treachery", "Get To The...",
          {"Boost": "2"}, [],
          "<b>When Revealed</b>: The villain schemes. Place 2 threat on The Chopper side scheme.\n"
          "<i>\"If it bleeds, we can kill it.\" —Dutch</i>", ALT),
]
