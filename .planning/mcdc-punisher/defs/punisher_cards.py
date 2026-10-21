# Entrees cards.json (PROJET, NON INSERE) pour le contenu "simple" de la campagne Punisher MC x DC 2026,
# lot PU-0 (cadrage docs/rapports/cadrage-14-15-19-2026-10-20.md section 1.3) : Jigsaw, Hobgoblin, The
# Syndicate, Punisher's Armory, Capo of the Past. AUCUNE LOGIQUE DE CAPACITE : ce fichier ne contient que
# des dictionnaires de donnees brutes (texte, valeurs, traits), sur le modele structurel de
# .planning/galactic-storm/defs/majestrix_cards.py. Rien n'est insere dans data/cards.json, aucun script
# src/cards/pack/... n'est ecrit : preparation pour une session de codage future (PU-2 et PU-3 du
# decoupage).
#
# SOURCE : docs/packs/mcdc-2026-punisher/cartes.md (releve relu en 300 dpi le 19/10/2026, [?] leves le
# 20/10/2026), sections "Jigsaw" (p111-p139), "Hobgoblin" (p141-p169), "Punisher's Armory" (p227-p235),
# "The Syndicate" (p249-p261), "Capo of the Past" (p277). Chaque entree cite sa page p### pour retrouver
# le scan dans paquets-cartes/MC x DC 2026 - campagne Punisher/scans/pNNN.jpg (hors depot git).
#
# ======================================================================================================
# DECISION card_id (point 3 du lot PU-0, PROPOSITION a confirmer au moment du portage) :
#
# Le PDF porte DEUX numerotations par carte : la page du scan (p001-p286, une face = une page) et un
# "ID MC x DC" sequentiel imprime en bas de carte (6001-6140+, voir cartes.md). Aucune des deux ne groupe
# seule les exemplaires identiques : l'ID MC x DC numerote CHAQUE EXEMPLAIRE PHYSIQUE separement (Maggia
# Thug x3 = ID 6060/6061/6062 pour un texte identique), et la page scan fait pareil. Convention retenue,
# alignee sur le pack le plus recent du meme genre (tk, TMNT Bebop & Rocksteady, prefixes_fanmade.json
# "tk" : "les copies identiques (meme scan) partagent un card_id") :
#
#   card_id = "pu" + les 3 derniers chiffres de l'ID MC x DC du PREMIER exemplaire du groupe.
#   - Exemplaires au texte IDENTIQUE (meme nom, meme capacite) : UN SEUL card_id, repete N fois dans la
#     liste ENCOUNTERS du set (comme gs129/gs129 dans majestrix_cards.py). Exemple : Maggia Thug (ID
#     6060/6061/6062, texte identique) -> un seul "pu060", compte 3 fois au deck de rencontre.
#   - Mechant a plusieurs stades, CHAQUE STADE etant une carte PHYSIQUE UNIQUE recto (standard) / verso
#     (expert) : le DOS (expert) recoit le MEME numero d'ID MC x DC que le RECTO (standard) sur ce
#     releve (ex. Jigsaw stade 1 : "I, A" et "II, B" partagent l'ID 6056) -> DEUX card_id distincts,
#     suffixes a (recto, standard) / b (verso, expert), sur le modele deja utilise pour les heros a deux
#     faces (xx001a/xx001b) : "pu056a" (stade 1 standard) / "pu056b" (stade 1 expert), "pu057a" (stade 2
#     standard) / "pu057b" (stade 2 expert).
#   - A CONFIRMER AU PORTAGE : cette convention n'a pas ete relue par un agent fort (contrairement a la
#     recommandation du cadrage pour les briques M1/M2) ; elle est cependant sans risque de collision avec
#     aucun prefixe existant (tools/prefixes_fanmade.json, prefixe "pu" reserve ce jour).
#
# Lectures faites sur les scans (300 dpi, 19-20/10/2026, voir cartes.md pour le detail carte par carte) :
# silhouette apres un nombre (👤) = "par joueur" ; etoile pleine (★) devant une capacite ou en exposant
# d'une stat = renvoi au texte imprime en gras juste en dessous (convention du PDF MC x DC, PAS la meme
# etoile que le "par joueur" des autres packs : ne pas confondre avec le "*" de majestrix_cards.py).
# Desc : les valeurs "par joueur" gardent le glyphe 👤 tel quel (pas converties en "*") pour eviter cette
# confusion tant que la convention finale n'est pas choisie au portage.

PU = "Jigsaw"
PU_HOB = "Hobgoblin"
PU_ARM = "Punisher's Armory"
PU_SYN = "The Syndicate"
PU_CAPO = "Capo of the Past"


def c(cid, typ, name, desc, traits, text, set_name, subtitle="", page=""):
    return {"card_id": cid, "type": typ, "name": name, "subtitle": subtitle, "desc": desc,
            "traits": traits, "set_name": set_name, "text": text, "custom": "MCxDC 2026", "page": page}


# ======================================================================================================
# Set "Jigsaw" (15 cartes physiques, 13 card_id distincts) -- mechant principal du scenario Punishment.
# ======================================================================================================

JIGSAW_FORCED_1A1B = ("[star] <b>Forced Response</b>: After Jigsaw attacks you, if the top of the encounter discard "
                      "pile is a minion, put it into play engaged with you. Otherwise, place 1 threat on the main "
                      "scheme.")
JIGSAW_FORCED_2A = JIGSAW_FORCED_1A1B  # p113 : "meme texte que 1A, avec 1 menace" (releve cartes.md)
JIGSAW_FORCED_2B = ("[star] <b>Forced Response</b>: After Jigsaw attacks you, if the top of the encounter discard "
                     "pile is a minion, put it into play engaged with you. Otherwise, place 2 threat on the main "
                     "scheme.")

JIGSAW_CARDS = [
    # --- Mechant (stade 1 = ID 6056, stade 2 = ID 6057 ; a=standard, b=expert) -------------------------
    c("pu056a", "Villain", "* Jigsaw", {"HP": "14👤", "SCH": "2", "ATK": "1★", "Stage": "1"}, ["CRIMINAL", "MAGGIA", "UNDERLING"],
      JIGSAW_FORCED_1A1B, PU, page="p111",
      subtitle='"How does it feel, Frank? You think I wouldn\'t know you were coming?"'),
    c("pu056b", "Villain", "* Jigsaw", {"HP": "16👤", "SCH": "2", "ATK": "2★", "Stage": "1", "Steady": "1"}, ["CRIMINAL", "MAGGIA", "UNDERLING"],
      "Steady.\n" + JIGSAW_FORCED_1A1B, PU, page="p112"),
    c("pu057a", "Villain", "* Jigsaw", {"HP": "16👤", "SCH": "2", "ATK": "2★", "Stage": "2", "Steady": "1"}, ["CRIMINAL", "MAGGIA", "UNDERLING"],
      "Steady.\n" + JIGSAW_FORCED_2A, PU, page="p113"),
    c("pu057b", "Villain", "* Jigsaw", {"HP": "18👤", "SCH": "3", "ATK": "2★", "Stage": "2", "Steady": "1"}, ["CRIMINAL", "MAGGIA", "UNDERLING"],
      "Steady.\n" + JIGSAW_FORCED_2B, PU, page="p114",
      subtitle='"How does it feel, Frank? You think I wouldn\'t know you were coming?"'),
    # --- Attachement, sbires, manigance annexe, traitrises (ID 6058-6070) ------------------------------
    c("pu058", "Attachment", "Jigsaw's Knife", {"ATK+": "1★", "Boost": "2"}, ["WEAPON"],
      "Weapon. Attach to Jigsaw.\n[star] Jigsaw gains retaliate 1 and his attacks gain piercing.\n"
      "<b>Hero Action</b>: Exhaust a character you control and spend [physical][mental] → discard this card.",
      PU, page="p115",
      subtitle='"Don\'t spoil the surprise! We\'re gonna have some fun... Frankie and Jigsaw, just like old times."'),
    c("pu059", "Minion", "* Bushwhacker", {"SCH": "1", "ATK": "★", "HP": "5", "Boost": "1", "Patrol": "1"}, ["CRIMINAL", "MERCENARY"],
      "Patrol.\n[star] <b>Forced Interrupt</b>: When Bushwhacker would attack, instead take 3 indirect damage. You "
      "may spend [mental] or [wild] to deal that damage to another enemy instead.", PU, page="p117"),
    # ⚠ 3 exemplaires au texte identique : ID 6060 (p119), 6061 (p121), 6062 (p123) -> 1 card_id, x3 au deck.
    c("pu060", "Minion", "Maggia Thug", {"SCH": "1", "ATK": "2", "HP": "3", "Boost": "1", "Guard": "1", "Patrol": "1"}, ["CRIMINAL", "MAGGIA"],
      'Guard. Patrol.\n"Jigsaw uses his standing as a Maggia capo to exert his "influence" on those that resist '
      'him."', PU, page="p119/p121/p123 (x3 exemplaires identiques, ID 6060/6061/6062)"),
    c("pu063", "Minion", "* Man Mountain Marko", {"SCH": "0", "ATK": "3", "HP": "6", "Boost": "2", "Toughness": "1", "Teamwork": "MAGGIA"}, ["CRIMINAL", "FIST", "MAGGIA"],
      "Teamwork (MAGGIA). Toughness.\n<b>When Revealed</b>: Exhaust a character you control.", PU, page="p125",
      subtitle='"This time you ain\'t walking away!"'),
    c("pu064", "Minion", "* Eel", {"SCH": "1", "ATK": "2★", "HP": "4", "Boost": "1", "Quickstrike": "1"}, ["CRIMINAL", "MAGGIA"],
      "Quickstrike.\n[star] <b>Forced Response</b>: After Eel attacks and damages a character, exhaust that "
      "character. Otherwise, stun it.", PU, page="p127",
      subtitle='"I got real power in the underworld now! I got juice! And what do you got?"'),
    c("pu065", "SideScheme", "Putting the Pieces Together", {"StartingThreat": "1👤", "Boost": "2", "Crisis": "1"}, [],
      "<b>When Revealed</b>: Place 2 threat on this scheme for each MAGGIA character in play.\n"
      "<b>When Defeated</b>: In player order, each player finds a MAGGIA minion that is not in play and reveals "
      "it.", PU, page="p129",
      subtitle='"Jigsaw was once known as "Billy the Beaut." Now he uses his terrifying visage to intimidate his '
               'way to power."'),
    # ⚠ 2 exemplaires identiques (ID 6066/6067) -> 1 card_id, x2 au deck.
    c("pu066", "Treachery", "Cut to Pieces", {"Boost": "★"}, [],
      "<b>When Revealed</b>: Jigsaw activates against you. If this activation is an attack, he gets +1 ATK.\n"
      "[star] <b>Boost</b>: Place 1 threat on the main scheme and heal 1 damage from Jigsaw.", PU,
      page="p131/p133 (x2 exemplaires identiques, ID 6066/6067)"),
    # ⚠ 2 exemplaires identiques (ID 6068/6069) -> 1 card_id, x2 au deck.
    c("pu068", "Treachery", "Friends of Ours", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Find a MAGGIA minion that is not in play and reveal it. Each MAGGIA minion activates "
      "against the player it is engaged with.", PU, page="p135/p137 (x2 exemplaires identiques, ID 6068/6069)",
      subtitle='"Get \'em boys!"'),
    c("pu070", "Treachery", "A Made Man", {"Boost": "★+1"}, [],
      "<b>When Revealed (Alter-Ego)</b>: Discard an ally from play. Otherwise, place 1👤 threat on each scheme.\n"
      "<b>When Revealed (Hero)</b>: Give Jigsaw a facedown boost card. If a MAGGIA minion is in play, give him an "
      "additional boost card.\n[star] <b>Boost</b>: After this activation, give Jigsaw a facedown boost card.",
      PU, page="p139"),
]

# Paquet de rencontre du scenario (15 cartes physiques, duplicats repetes selon le nombre d'exemplaires).
JIGSAW_ENCOUNTERS = (["pu058", "pu059"] + ["pu060"] * 3 + ["pu063", "pu064", "pu065"]
                      + ["pu066"] * 2 + ["pu068"] * 2 + ["pu070"])

# ======================================================================================================
# Set "Hobgoblin" (15 cartes physiques, 14 card_id distincts) -- mechant a 3 stades, sous-fifre alternatif.
# ======================================================================================================

HOB_PUMPKIN_X1 = '[star] "Pumpkin Bomb" -- Forced Response: After Hobgoblin attacks you, resolve the "Pumpkin Bomb" ability.'
HOB_PUMPKIN_X2 = ('[star] "Pumpkin Bomb" -- Forced Response: After Hobgoblin attacks you, resolve the "Pumpkin Bomb" '
                   'ability twice.')

HOBGOBLIN_CARDS = [
    # --- Mechant (stade 1 = ID 6071, stade 2 = ID 6072 ; a=standard, b=expert) -------------------------
    c("pu071a", "Villain", "* Hobgoblin", {"HP": "15👤", "SCH": "1", "ATK": "1★", "Stage": "1"}, ["SINISTER_SIX", "UNDERLING"],
      "[star] Hobgoblin's attacks gain ranged.\n" + HOB_PUMPKIN_X1, PU_HOB, page="p141",
      subtitle='"You\'re right on time! For your funeral!"'),
    c("pu071b", "Villain", "* Hobgoblin", {"HP": "17👤", "SCH": "2", "ATK": "1★", "Stage": "1", "Steady": "1"}, ["SINISTER_SIX", "UNDERLING"],
      "Steady.\n[star] Hobgoblin's attacks gain ranged.\n" + HOB_PUMPKIN_X2, PU_HOB, page="p142",
      subtitle='"Sorry, but there\'s no profit to be made in my own annihilation!"'),
    c("pu072a", "Villain", "* Hobgoblin", {"HP": "17👤", "SCH": "2", "ATK": "1★", "Stage": "2", "Steady": "1"}, ["SINISTER_SIX", "UNDERLING"],
      "Steady.\n[star] Hobgoblin's attacks gain ranged.\n" + HOB_PUMPKIN_X2, PU_HOB, page="p143"),
    c("pu072b", "Villain", "* Hobgoblin", {"HP": "19👤", "SCH": "2", "ATK": "2★", "Stage": "2", "Steady": "1"}, ["SINISTER_SIX", "UNDERLING"],
      "Steady.\n[star] Hobgoblin's attacks gain ranged.\n" + HOB_PUMPKIN_X2, PU_HOB, page="p144",
      subtitle='"This place is ruined. Worse for wear, but the important thing is... it\'s mine now! HAHAHAHA!"'),
    # --- Glider (porte le texte de l'aptitude "Pumpkin Bomb" invoquee par tout le set), arme, sbires --
    c("pu073", "Attachment", "Hobgoblin's Glider", {"Setup": "1", "Permanent": "1"}, [],
      'Setup. Permanent. Attach to Hobgoblin.\n"Pumpkin Bomb" -- <b>Special</b>: Discard a card from the encounter '
      'deck. If that card is a:\n- Treachery: Place 1 threat on the main scheme.\n- Minion or side scheme: Take 1 '
      'indirect damage.\n- Other: Discard 3 cards from the encounter deck.', PU_HOB, page="p145"),
    c("pu074", "Attachment", "Flaming Sword", {"ATK+": "1★", "Boost": "2"}, ["WEAPON"],
      'Weapon. Attach to Hobgoblin.\n[star] Hobgoblin\'s attacks gain piercing.\n<b>Hero Action</b>: Exhaust your '
      'hero and resolve the "Pumpkin Bomb" ability twice → discard this card.', PU_HOB, page="p147",
      subtitle='"Now don\'t go dying on me too fast!"'),
    c("pu075", "Minion", "* Prowler", {"SCH": "2", "ATK": "2", "HP": "4", "Boost": "1", "Quickstrike": "1"}, ["CRIMINAL", "THIEF"],
      "Quickstrike.\n<b>Forced Response</b>: After Prowler damages your hero, discard 2 cards from the encounter "
      "deck. If a treachery was discarded this way, discard an upgrade or support you control.", PU_HOB, page="p149",
      subtitle='"It\'s nothing personal, just business."'),
    c("pu076", "Minion", "* Rabble", {"SCH": "2", "ATK": "2", "HP": "3", "Boost": "1", "Vulnerable": "1"}, ["AERIAL", "CRIMINAL"],
      "Vulnerable.\nRabble enters play with 2 drone counters on her.\n<b>Forced Interrupt</b>: When Rabble would "
      "take damage → remove 1 drone counter → prevent that damage and discard 2 cards from the encounter deck "
      "instead.", PU_HOB, page="p151"),
    c("pu077", "Minion", "* The Enforcers", {"SCH": "1★", "ATK": "3★", "HP": "6", "Boost": "2"}, ["CRIMINAL", "MERCENARY"],
      "[star] <b>Forced Response</b>: After The Enforcers activate against you, discard 3 cards from the encounter "
      "deck. Take 1 indirect damage for each treachery discarded this way.", PU_HOB, page="p153",
      subtitle="Montana, Ox, and Fancy Dan will employ each of their special skills for the highest bidder."),
    c("pu078", "Obligation", "Torn to Pieces", {}, [],
      '<b>Forced Response</b>: After your hero uses a basic power, resolve the "Pumpkin Bomb" ability.\n'
      "<b>Alter-Ego Action</b>: Exhaust your identity and discard 3 cards from the encounter deck → discard this "
      "card.", PU_HOB, page="p155",
      subtitle='"You will pay! So says the Hobgoblin!"'),
    c("pu079", "SideScheme", "Designs on Crimes", {"StartingThreat": "3👤", "Boost": "1", "Hazard": "1"}, [],
      "<b>When Revealed</b>: Discard 3👤 cards from the encounter deck.\n"
      '<b>When Defeated</b>: In player order, each player resolves the "Pumpkin Bomb" ability.', PU_HOB, page="p157",
      subtitle="Hobgoblin lurks in the shadows, waiting for an opportunity to take over New York's criminal "
               "underworld."),
    # ⚠ 2 exemplaires identiques (ID 6080/6081) -> 1 card_id, x2 au deck.
    c("pu080", "Treachery", "Guise to Terrorize", {"Boost": "2"}, [],
      '<b>When Revealed</b>: Discard a card from the encounter deck. If the discarded card is a treachery, resolve '
      'the "Pumpkin Bomb" ability. Otherwise, reveal that card.', PU_HOB,
      page="p159/p161 (x2 exemplaires identiques, ID 6080/6081)",
      subtitle='"Dig a hole, Fisk, wide enough for your final resting place."'),
    # ⚠ 2 exemplaires identiques (ID 6082/6083) -> 1 card_id, x2 au deck.
    c("pu082", "Treachery", "Smashing Pumpkins", {"Boost": "★"}, [],
      '<b>When Revealed</b>: Resolve the "Pumpkin Bomb" ability three times.\n'
      '[star] <b>Boost</b>: Resolve the "Pumpkin Bomb" ability.', PU_HOB,
      page="p163/p165 (x2 exemplaires identiques, ID 6082/6083)", subtitle='"Trick or Treat!"'),
    # ⚠ 2 exemplaires identiques (ID 6084/6085) -> 1 card_id, x2 au deck.
    c("pu084", "Treachery", "Wrath of the Hobgoblin", {"Boost": "★+1"}, [],
      "<b>When Revealed</b>: Hobgoblin activates against you with +1 SCH and +1 ATK for each acceleration token on "
      "the main scheme.\n[star] <b>Boost</b>: Discard 2 cards from the encounter deck.", PU_HOB,
      page="p167/p169 (x2 exemplaires identiques, ID 6084/6085)"),
]

HOBGOBLIN_ENCOUNTERS = (["pu073", "pu074", "pu075", "pu076", "pu077", "pu078", "pu079"]
                         + ["pu080"] * 2 + ["pu082"] * 2 + ["pu084"] * 2)

# ======================================================================================================
# Set "Punisher's Armory" (5 cartes, 5 card_id) -- extension modulaire, armes a munitions (ID 6114-6118).
# ======================================================================================================

ARMORY_CARDS = [
    c("pu114", "SideScheme", "Punisher's Armory", {"StartingThreat": "4👤", "Boost": "★"}, [],
      "<b>Forced Response</b>: After the villain phase begins, if there is no WEAPON attachment on the villain, "
      "discard from the encounter deck until a WEAPON is discarded. Reveal that card.\n"
      "<b>When Defeated</b>: Shuffle each WEAPON in the encounter discard pile into the encounter deck.\n"
      "[star] <b>Boost</b>: Reveal this card.", PU_ARM, page="p227"),
    c("pu115", "Attachment", "Punisher's Shotgun", {"ATK+": "1★", "Boost": "1", "Uses": "2👤,ammo"}, ["ARMAMENT", "WEAPON"],
      "Armament. Weapon. Attach to Punisher. Otherwise, attach to the villain. Uses (2👤 ammo counters).\n"
      "<b>When Revealed</b>: Discard each other ARMAMENT card in play.\n"
      "[star] <b>Forced Response</b>: After attached character attacks, remove 1 ammo counter from here and stun "
      "the attack's target.", PU_ARM, page="p229"),
    c("pu116", "Attachment", "Punisher's Sniper Rifle", {"ATK+": "2★", "Boost": "2", "Uses": "1+1👤,ammo"}, ["ARMAMENT", "WEAPON"],
      "Armament. Weapon. Attach to Punisher. Otherwise, attach to the villain. Uses (1+1👤 ammo counters).\n"
      "<b>When Revealed</b>: Discard each other ARMAMENT card in play.\n"
      "[star] Attached character's attacks gain piercing and ranged.\n"
      "[star] <b>Forced Response</b>: After attached character attacks, remove 1 counter from here.", PU_ARM,
      page="p231"),
    c("pu117", "Attachment", "Punisher's SMG", {"ATK": "★", "Boost": "2", "Uses": "1+1👤,ammo"}, ["ARMAMENT", "WEAPON"],
      "Armament. Weapon. Attach to Punisher. Otherwise, attach to the villain. Uses (1+1👤 ammo counters).\n"
      "<b>When Revealed</b>: Discard each other ARMAMENT card in play.\n"
      "[star] <b>Forced Response</b>: After attached character attacks, each player deals 1 damage to a character "
      "they control. Remove 1 ammo counter from here.", PU_ARM, page="p233"),
    c("pu118", "Treachery", "Frag Grenade", {"Boost": "1"}, ["WEAPON"],
      "Weapon.\n<b>When Revealed</b>: Take 3 indirect damage. You may discard a card you control to prevent X of "
      "this damage, where X is equal to that card's cost.", PU_ARM, page="p235",
      subtitle='"Just... just you and me, though, right? Just you and me. And a bomb."'),
]

ARMORY_ENCOUNTERS = ["pu114", "pu115", "pu116", "pu117", "pu118"]

# ======================================================================================================
# Set "The Syndicate" (7 cartes, 7 card_id) -- extension modulaire, sbires lies par "When Defeated" (ID 6125-6131).
# ======================================================================================================

SYNDICATE_DEFEATED = ("<b>When Defeated</b>: Choose a CRIMINAL minion. That minion activates against the player it "
                       "is engaged with.")

SYNDICATE_CARDS = [
    c("pu125", "Minion", "* Beetle", {"SCH": "2", "ATK": "2", "HP": "5", "Boost": "3"}, ["AERIAL", "CRIMINAL", "SYNDICATE"],
      "Reduce the amount of damage Beetle takes from non-AERIAL attacks by 1.\n" + SYNDICATE_DEFEATED, PU_SYN,
      page="p249", subtitle='"You colossal idiot -- are you seriously trying to mansplain heists to us right now?"'),
    c("pu126", "Minion", "* White Rabbit", {"SCH": "2", "ATK": "2★", "HP": "3", "Boost": "2"}, ["CRIMINAL", "SYNDICATE"],
      "[star] <b>Forced Response</b>: After White Rabbit attacks and damages you, discard a card you control from "
      "play.\n" + SYNDICATE_DEFEATED, PU_SYN, page="p251", subtitle='"So give up... because of feminism and stuff?"'),
    c("pu127", "Minion", "* Electro", {"SCH": "1", "ATK": "1", "HP": "5", "Boost": "3", "Villainous": "1"}, ["CRIMINAL", "SYNDICATE"],
      "Villainous. Electro's attacks deal indirect damage.\n" + SYNDICATE_DEFEATED, PU_SYN, page="p253",
      subtitle='"Let\'s go get us a revenge kill and send the criminal patriarchy a message!"'),
    c("pu128", "Minion", "* Lady Octopus", {"SCH": "2", "ATK": "1★", "HP": "4", "Boost": "1", "Incite": "2", "Toughness": "1"}, ["CRIMINAL", "GENIUS", "SYNDICATE"],
      "Incite 2. Toughness.\n[star] <b>Forced Response</b>: After Lady Octopus attacks, place 2 threat on the main "
      "scheme.\n" + SYNDICATE_DEFEATED, PU_SYN, page="p255"),
    c("pu129", "Minion", "* Scorpia", {"SCH": "1", "ATK": "3★", "HP": "6", "Boost": "2", "Guard": "1", "Patrol": "1"}, ["CRIMINAL", "SYNDICATE"],
      "Guard. Patrol.\n[star] Scorpia's attacks gain piercing.\n" + SYNDICATE_DEFEATED, PU_SYN, page="p257",
      subtitle='"I thought this was the part where we team up cause we risked our lives for each other and stuff."'),
    c("pu130", "Minion", "* Trapstr", {"SCH": "1", "ATK": "2★", "HP": "3", "Boost": "1", "Quickstrike": "1"}, ["CRIMINAL", "SYNDICATE"],
      "Quickstrike.\n[star] <b>Forced Interrupt</b>: When Trapstr attacks you, stun a character you control.\n"
      + SYNDICATE_DEFEATED, PU_SYN, page="p259"),
    c("pu131", "SideScheme", "The Syndicate", {"StartingThreat": "3", "Boost": "★+1"}, [],
      "<b>When Revealed</b>: In player order, each player finds and reveals a SYNDICATE minion that is not in "
      "play.\n[star] <b>Boost</b>: Deal this card to yourself as a facedown encounter card.", PU_SYN, page="p261",
      subtitle="Beetle's Syndicate takes a collaborative approach to plotting and scheming."),
]

SYNDICATE_ENCOUNTERS = ["pu125", "pu126", "pu127", "pu128", "pu129", "pu130", "pu131"]

# ======================================================================================================
# Set "Capo of the Past" (1 carte, 1 card_id) -- attachement qui met en jeu un CAPO deja vaincu (ID 6139).
# ======================================================================================================

CAPO_OF_THE_PAST_CARDS = [
    c("pu139", "Attachment", "Capo of the Past", {"Boost": "2+★", "Permanent": "1", "Victory": "0"}, [],
      "Permanent. Victory 0.\nTreat attached character as an ELITE minion. It gains steady, villainous, and "
      "victory 0.\n<b>When Revealed</b>: Search your collection for a random CAPO villain. Put it into play "
      "engaged with you and attach this card to it.\n[star] <b>Boost</b>: Deal this to yourself as a facedown "
      "encounter card.", PU_CAPO, page="p277 (type Attachement sur cartes.md ; porte un When Revealed : type exact "
      "Treachery/Attachment a confirmer au portage, voir le piege 'carte de rencontre qui s'attache elle-meme' "
      "d'autres packs)"),
]

CAPO_OF_THE_PAST_ENCOUNTERS = ["pu139"]

# ======================================================================================================
# Recapitulatif : 13 + 14 + 5 + 7 + 1 = 40 card_id distincts, pour 15 + 15 + 5 + 7 + 1 = 43 cartes
# physiques (releve "contenu simple" du cadrage section 1.2 : "aucune brique neuve au-dela de M6-M9").
# ======================================================================================================
ALL_CARDS = JIGSAW_CARDS + HOBGOBLIN_CARDS + ARMORY_CARDS + SYNDICATE_CARDS + CAPO_OF_THE_PAST_CARDS
assert len({card["card_id"] for card in ALL_CARDS}) == len(ALL_CARDS), "card_id en double dans ce fichier"
