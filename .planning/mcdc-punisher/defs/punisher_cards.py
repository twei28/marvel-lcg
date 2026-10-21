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
    c("pu117", "Attachment", "Punisher's SMG", {"ATK+": "★", "Boost": "2", "Uses": "1+1👤,ammo"}, ["ARMAMENT", "WEAPON"],
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
# Set "Punisher's Hit List" (8 cartes physiques, 7 card_id) -- modulaire ; Punisher y est un sbire elite (ID 6106-6113).
# Releve cartes.md relu sur les scans p211-p219 le 21/10/2026 (conforme).
# ======================================================================================================
PU_HIT = "Punisher's Hit List"
PU_SWAT = "SWAT Team"

HITLIST_CARDS = [
    c("pu106a", "Environment", "Punisher's Hit List", {"Setup": "1", "Permanent": "1"}, [],
      'Setup. Permanent.\n<b>Forced Response</b>: After Punisher defeats a character, add 1 counter here. Then, if '
      'there are at least 2+1👤 counters here, remove all counters and flip this card.\n<b>Forced Response</b>: After '
      'the player phase ends, resolve Punisher\'s "Punishment" ability, if able.', PU_HIT, page="p211"),
    c("pu106b", "Environment", "Satchel Charge", {}, [],
      "This card's effects cannot be canceled.\n<b>When Revealed</b>: Deal 2👤 damage to the villain. The players as a "
      "group take 3👤 indirect damage. Shuffle Punisher and each ARMAMENT card in play and in the encounter discard "
      "pile into the encounter deck. Flip this card.", PU_HIT, page="p212",
      subtitle='"I don\'t have to come find you. You\'re next on my list."'),
    c("pu107", "Minion", "* Punisher", {"SCH": "0", "ATK": "1", "HP": "7", "Boost": "3", "Steady": "1", "Toughness": "1", "Villainous": "1"},
      ["ELITE", "VIGILANTE"],
      'Steady. Toughness. Villainous.\n"Punishment" -- <b>Special</b>: Punisher attacks the minion with the fewest '
      'remaining hit points with +2 ATK. Ignore "Boost" abilities for this attack. If the attack defeats that minion, '
      'repeat this ability.', PU_HIT, page="p213", subtitle='"All the scum. All in one place. It\'s perfect."'),
    c("pu108", "Minion", "* Rachel Cole-Alves", {"SCH": "1", "ATK": "2", "HP": "5", "Boost": "2"}, ["MARINE", "VIGILANTE"],
      'Punisher cannot attack this minion.\n<b>When Revealed</b>: Resolve Punisher\'s "Punishment" ability. Otherwise, '
      'Rachel Cole-Alves attacks you. If you are in hero form, give her a boost card for this attack.', PU_HIT, page="p215",
      subtitle='"Every last one of them will be punished for what they\'ve done. Every. Last. One."'),
    c("pu109", "Attachment", "Punisher's Katana", {"ATK+": "1★", "Boost": "★+1"}, ["ARMAMENT", "WEAPON"],
      "Armament. Weapon.\n[star] Punisher's attacks gain piercing.\n<b>When Revealed</b>: Find Punisher, reveal him, "
      'and attach this to him. Resolve his "Punishment" ability.\n[star] <b>Boost</b>: If this attack defeats an ally, '
      "add a counter to Punisher's Hit List.", PU_HIT, page="p217"),
    c("pu110", "Attachment", "Punisher's M1911", {"ATK+": "1★", "Boost": "★+1"}, ["ARMAMENT", "WEAPON"],
      "Armament. Weapon.\n[star] Punisher's attacks gain ranged.\n<b>When Revealed</b>: Find Punisher, reveal him, "
      'and attach this to him. He attacks you. Do not give him a boost card for this attack. Resolve his "Punishment" '
      "ability.\n[star] <b>Boost</b>: If this attack defeats an ally, add a counter to Punisher's Hit List.", PU_HIT, page="p219"),
    # 2 exemplaires identiques (ID 6111/6112) -> 1 card_id, x2 au deck.
    c("pu111", "Treachery", "Dramatic Entrance", {"Boost": "★+2"}, [],
      '<b>When Revealed</b>: Find Punisher and reveal him. He attacks the villain and then attacks you. Resolve his '
      '"Punishment" ability.\n[star] <b>Boost</b>: If this attack defeats an ally, add a counter to Punisher\'s Hit List.',
      PU_HIT, page="p221/p223 (x2, ID 6111/6112)"),
    c("pu113", "SideScheme", "Punisher's Arsenal", {"StartingThreat": "2👤", "Boost": "1"}, [],
      "<b>When Revealed</b>: Find an ARMAMENT attachment that is not in play and reveal it.\n<b>When Defeated</b>: Find "
      'Punisher and reveal him. Resolve his "Punishment" ability.', PU_HIT, page="p225",
      subtitle="Punisher stockpiles weapons and supplies in safehouses scattered throughout New York."),
]
HITLIST_ENCOUNTERS = ["pu106a,pu106b", "pu107", "pu108", "pu109", "pu110", "pu111", "pu111", "pu113"]

# ======================================================================================================
# Set "SWAT Team" (6 cartes physiques, 4 card_id) -- modulaire, la police (ID 6119-6124). Releve p237-p247.
# ======================================================================================================
SWAT_CARDS = [
    c("pu119", "SideScheme", "SWAT", {"StartingThreat": "1", "Boost": "1", "Setup": "1", "Permanent": "1"}, [],
      "Setup. Permanent. Players cannot thwart this scheme.\n<b>Forced Response</b>: After an enemy is defeated, place 1 "
      "threat here (3 threat instead if it had the POLICE trait). Then, if there is 4+ threat here, remove all threat "
      "and place 1 wanted counter here.\nIf there are 5 or more wanted counters here, the players lose the game.",
      PU_SWAT, page="p237"),
    c("pu120", "Minion", "* Cole North", {"SCH": "2★", "ATK": "2★", "HP": "4", "Boost": "3", "Patrol": "1"}, ["DETECTIVE", "POLICE"],
      "Patrol.\n[star] When Cole North schemes, place that threat on SWAT, if able.\n[star] <b>Forced Interrupt</b>: When "
      "Cole North would attack, if there are fewer than 3 wanted counters on SWAT, remove 2 threat from the main scheme "
      "instead.", PU_SWAT, page="p239"),
    # 2 exemplaires identiques (ID 6121/6122)
    c("pu121", "Minion", "Riot Police", {"SCH": "1★", "ATK": "0", "HP": "6", "Boost": "1", "Guard": "1", "Retaliate": "2", "Toughness": "1"}, ["POLICE"],
      "Guard. Retaliate 2. Toughness.\n[star] When Riot Police schemes, place that threat on SWAT, if able.\n<b>Hero "
      "Action</b>: Spend 1 resource of any type and discard an ally you control → discard Riot Police and remove 2 "
      'threat from SWAT.', PU_SWAT, page="p241/p243 (x2, ID 6121/6122)", subtitle='"DISPERSE AND CLEAR THE AREA!"'),
    # 2 exemplaires identiques (ID 6123/6124)
    c("pu123", "Minion", "Tactical Sniper", {"SCH": "1★", "ATK": "3★", "HP": "4", "Boost": "2", "Vulnerable": "1"}, ["POLICE"],
      "Vulnerable.\n[star] When Tactical Sniper schemes, place that threat on SWAT, if able.\n[star] <b>Forced "
      "Interrupt</b>: When Tactical Sniper would attack, if there are fewer than 3 wanted counters on SWAT, it attacks "
      "the enemy with the fewest remaining hit points without the POLICE trait instead.", PU_SWAT, page="p245/p247 (x2, ID 6123/6124)"),
]
SWAT_ENCOUNTERS = ["pu119", "pu120", "pu121", "pu121", "pu123", "pu123"]

# ======================================================================================================
# Set "Punishment" (20 cartes physiques, 18 card_id) -- le Punisher, vilain final (ID 6086-6105). Releve p171-p209 relu le 21/10/2026.
# Vilain a 3 stades (I, II, II, III) : 6086 = I (1A, a) / II (1B, b) ; 6087 = II (2A, a) / III (2B, b) ; standard = pu086a -> pu087a,
# expert = pu086b -> pu087b (meme schema que Jigsaw et Hobgoblin).
# ======================================================================================================
PU_PUN = "Punishment"
PUN_HERO_RESP_ANY = ('<b>Hero Response</b>: After you attack Punisher, spend 2 resources of any type → flip Target Lock '
                     'to its DISTRACTED side and discard one non-permanent attachment from Punisher.')
PUN_HERO_RESP_SAME = ('<b>Hero Response</b>: After you attack Punisher, spend 2 resources of the same type → flip Target '
                      'Lock to its DISTRACTED side and discard one non-permanent attachment from Punisher.')

PUNISHMENT_CARDS = [
    c("pu086a", "Villain", "* Punisher", {"HP": "16👤", "SCH": "0", "ATK": "1", "Stage": "1", "Toughness": "1"}, ["SOLDIER", "VIGILANTE"],
      "Toughness.\n" + PUN_HERO_RESP_ANY, PU_PUN, page="p171",
      subtitle='"My actions aren\'t vengeance. No, not vengeance. Punishment!"'),
    c("pu086b", "Villain", "* Punisher", {"HP": "18👤", "SCH": "0", "ATK": "2", "Stage": "2", "Steady": "1", "Toughness": "1"}, ["SOLDIER", "VIGILANTE"],
      "Steady. Toughness.\n" + PUN_HERO_RESP_SAME, PU_PUN, page="p172",
      subtitle='"You need a role model? His name is Captain America, and he\'d be happy to have you."'),
    c("pu087a", "Villain", "* Punisher", {"HP": "18👤", "SCH": "0", "ATK": "2", "Stage": "2", "Steady": "1", "Toughness": "1"}, ["SOLDIER", "VIGILANTE"],
      "Steady. Toughness.\n" + PUN_HERO_RESP_SAME, PU_PUN, page="p173",
      subtitle='"My actions aren\'t vengeance. No, not vengeance. Punishment!"'),
    c("pu087b", "Villain", "* Punisher", {"HP": "20👤", "SCH": "0", "ATK": "3", "Stage": "3", "Steady": "1", "Toughness": "1"}, ["SOLDIER", "VIGILANTE"],
      "Steady. Toughness.\n" + PUN_HERO_RESP_SAME + " Give Punisher a facedown boost card.", PU_PUN, page="p174"),
    c("pu088a", "MainScheme", "One Last Kill", {"Stage": "1A"}, [],
      "<b>Contents</b>: Punisher I and II (II and III for expert mode) and one UNDERLING villain. Punishment, UNDERLING "
      "villain's set, and Standard sets. One modular set (Punisher's Armory).\n<b>Setup</b>: Find Target Lock and attach "
      "to Punisher, FOCUSED side up. Find Justice or Punishment? and reveal its setup side.", PU_PUN, page="p175",
      subtitle="You've chased down the villain and move in to apprehend them when suddenly a shot rings out!"),
    c("pu088b", "MainScheme", "One Last Kill", {"StartingThreat": "1👤", "TargetThreat": "8👤", "EscalationThreat": "1👤", "Stage": "1B"}, [],
      "<b>When Revealed</b>: Find and reveal Punisher's M1911s.\n<b>Forced Response</b>: After resolving step one of the "
      "villain phase, the TARGETED villain activates against the first player.", PU_PUN, page="p176",
      subtitle="Punisher sets his sights on the villain as they try to escape. But you need them alive to get answers about the escalating gang war."),
    c("pu089a", "MainScheme", "Escaping Punishment", {"Stage": "2A"}, [],
      "<b>When Revealed</b>: Find and reveal Punisher's Assault Rifle. Flip Target Lock to its DISTRACTED side.", PU_PUN, page="p177",
      subtitle="Punisher's target nears escape. Angered by your interference, he sets his sights on you!"),
    c("pu089b", "MainScheme", "Escaping Punishment", {"StartingThreat": "1👤", "TargetThreat": "9👤", "EscalationThreat": "1👤", "Stage": "2B"}, [],
      "<b>Forced Response</b>: After resolving step one of the villain phase, the TARGETED villain activates against the first "
      "player.\nIf this scheme is completed, the TARGETED villain escapes and the players lose the game.", PU_PUN, page="p178",
      subtitle="The villain frantically searches for an exit. SWAT surrounds the building. Punisher is out for blood. Can you stop him and capture the villain alive?"),
    c("pu090a", "Environment", "Justice or Punishment?", {"Setup": "1"}, [],
      "<b>Setup</b>: Reveal the UNDERLING villain (I for standard, II for expert mode). Set their hit points to the numeral "
      "(ignoring 👤) in their printed hit point value.\nAttach In the Crosshairs to them.\nShuffle their encounter cards "
      "into the encounter deck, following any <b>Setup</b> and <b>When Revealed</b> instructions.\nFlip this card.", PU_PUN, page="p179"),
    c("pu090b", "Environment", "Justice or Punishment?", {"Permanent": "1"}, [],
      "Permanent.\n• Punisher is the active villain. Encounter cards referring to or affecting \"the villain\" refer only to "
      "Punisher.\n• Players may defend any attack, even ones targeting enemies.\nIf Punisher's final stage is defeated, the "
      "players win the game.", PU_PUN, page="p180"),
    c("pu091a", "Attachment", "Target Lock", {"SCH+": "★", "ATK+": "★", "Setup": "1", "Permanent": "1"}, [],
      "Focused. Setup. Permanent.\n[star] <b>Forced Interrupt</b>: When Punisher would activate, he attacks the enemy with "
      "the fewest remaining hit points instead. If this attack damages an enemy or ally, place threat on the main scheme "
      "equal to the number of boost icons on the top card of the encounter discard pile.", PU_PUN, page="p181"),
    c("pu091b", "Attachment", "Target Lock", {"SCH+": "★", "ATK+": "1", "Permanent": "1"}, [],
      "Distracted. Permanent. Attach to Punisher.\n[star] <b>Forced Interrupt</b>: When Punisher would scheme, flip this "
      "card instead.\n<b>Forced Interrupt</b>: At the end of the round, flip this card.", PU_PUN, page="p182"),
    c("pu092", "Attachment", "In the Crosshairs", {"Setup": "1", "Permanent": "1"}, [],
      "Targeted. Setup. Permanent.\nAttached character gets +5👤 hit points, gains the TARGETED trait, and cannot be affected "
      "by player cards.\nIf attached character's current stage is defeated, the players lose the game.", PU_PUN, page="p183",
      subtitle="With every hit from Punisher, his target grows increasingly desperate to escape."),
    c("pu093", "Attachment", "Punisher's Assault Rifle", {"ATK+": "1★", "Boost": "1", "Uses": "2👤,ammo"}, ["ARMAMENT", "WEAPON"],
      "Armament. Weapon. Attach to Punisher. Uses (2👤 ammo counters).\n<b>When Revealed</b>: Discard each other ARMAMENT "
      "card in play.\n[star] Punisher's attacks gain overkill. His overkill damage on minions is dealt to the TARGETED "
      "villain.\n[star] <b>Forced Response</b>: After Punisher attacks, remove 1 ammo counter from here.", PU_PUN, page="p185"),
    c("pu094", "Attachment", "Punisher's RPG", {"ATK+": "2★", "Boost": "2", "Uses": "1+1👤,ammo"}, ["ARMAMENT", "WEAPON"],
      "Armament. Weapon. Attach to Punisher. Uses (1+1👤 ammo counters).\n<b>When Revealed</b>: Discard each other ARMAMENT "
      "card in play.\n[star] Punisher's attacks deal indirect damage. Exhaust any character damaged by his attack.\n[star] "
      "<b>Forced Response</b>: After Punisher attacks, remove 1 ammo counter from here.", PU_PUN, page="p187"),
    c("pu095", "Attachment", "Punisher's M1911s", {"ATK+": "1★", "Boost": "2", "Uses": "2👤,ammo"}, ["ARMAMENT", "WEAPON"],
      "Armament. Weapon. Attach to Punisher. Uses (2👤 ammo counters).\n<b>When Revealed</b>: Discard each other ARMAMENT "
      "card in play.\n[star] Punisher's attacks gain ranged.\n[star] <b>Forced Response</b>: After Punisher attacks, remove "
      "1 ammo counter from here.", PU_PUN, page="p189"),
    c("pu096", "Attachment", "Mexican Standoff", {"Boost": "1"}, ["CONFRONTATION"],
      "Confrontation. Attach to Punisher.\n<b>Forced Response</b>: After you attack Punisher, he activates. Then, the "
      "TARGETED villain activates against you. Do not give either character a boost card for these activations. Discard "
      "this card.", PU_PUN, page="p191", subtitle='"So, which one of us is going to make the first move?"'),
    c("pu097", "Minion", "* Microchip", {"SCH": "★", "ATK": "★", "HP": "3", "Boost": "1"}, ["GENIUS", "VIGILANTE"],
      "Punisher cannot attack this minion.\n[star] <b>Forced Interrupt</b>: When Microchip would activate, give Punisher a "
      "facedown boost card instead.\n<b>When Defeated</b>: Reveal the top WEAPON attachment in the encounter discard pile.",
      PU_PUN, page="p193"),
    c("pu098", "Minion", "* Rachel Cole-Alves", {"SCH": "★", "ATK": "2", "HP": "5", "Boost": "1"}, ["MARINE", "VIGILANTE"],
      "Punisher cannot attack this minion.\n[star] <b>Forced Interrupt</b>: When Rachel Cole-Alves would scheme, she "
      "attacks the TARGETED villain instead.", PU_PUN, page="p195",
      subtitle='"Nobody could ever be as driven as us. Nobody else knows pain like we do, Frank."'),
    c("pu099", "SideScheme", "Judge, Jury... Execution!", {"StartingThreat": "3👤", "Boost": "2", "Amplify": "1"}, [],
      "<b>When Defeated</b>: Discard the minion with the fewest remaining hit points and deal damage to the TARGETED villain "
      "equal to that minion's remaining hit points. Otherwise, give Punisher a facedown boost card.", PU_PUN, page="p197",
      subtitle="In a broken system, Punisher views himself as the only true source of justice for the worst of the worst."),
    # 2 exemplaires identiques (ID 6100/6101)
    c("pu100", "Treachery", "Back Against the Wall", {"Boost": "★+1"}, [],
      "<b>When Revealed (Alter-Ego)</b>: Deal damage to Punisher equal to the TARGETED villain's ATK.\n<b>When Revealed "
      "(Hero)</b>: Flip Target Lock to its DISTRACTED side. Punisher activates.\n[star] <b>Boost</b>: Give Punisher a "
      "facedown boost card (if he is activating, resolve it).", PU_PUN, page="p199/p201 (x2, ID 6100/6101)"),
    # 2 exemplaires identiques (ID 6102/6103)
    c("pu102", "Treachery", "Bullet Spray", {"Boost": "★"}, [],
      "<b>When Revealed</b>: Deal 1 damage to each character you control. Deal 1 damage to the TARGETED villain and each "
      "minion engaged with you.\n[star] <b>Boost</b>: Deal 1 damage to the TARGETED villain.", PU_PUN,
      page="p203/p205 (x2, ID 6102/6103)", subtitle='"I\'m fine. They\'re not."'),
    c("pu104", "Treachery", "Flash-Bang", {"Boost": "★"}, ["WEAPON"],
      "<b>When Revealed</b>: Stun each character you control. Stun the TARGETED villain and each minion engaged with you.\n"
      "[star] <b>Boost</b>: Stun a character you control.", PU_PUN, page="p207", subtitle="FWOOOSH!!"),
    c("pu105", "Treachery", "Say Good Night", {"Boost": "1"}, [],
      "<b>When Revealed (Alter-Ego)</b>: Deal damage to the TARGETED villain equal to Punisher's ATK.\n<b>When Revealed "
      "(Hero)</b>: Take damage equal to Punisher's ATK. You may exhaust your hero or discard an ally you control to prevent "
      "this damage.", PU_PUN, page="p209",
      subtitle='"We\'re nothing alike, me and the enemy. We both deal in death, but they sell theirs. I give it away."'),
]
# Paquet de rencontre du scenario (Punishment 20 cartes physiques, sans les cartes de mise en place).
PUNISHMENT_ENCOUNTERS = ["pu093", "pu094", "pu095", "pu096", "pu097", "pu098", "pu099",
                         "pu100", "pu100", "pu102", "pu102", "pu104", "pu105"]
# Cartes mises de cote par le scenario (« Find Target Lock », « Find Justice or Punishment? », In the Crosshairs).
PUNISHMENT_SET_ASIDE = ["pu091a,pu091b", "pu090a,pu090b", "pu092"]

# ======================================================================================================
# Scenario 1 « The Big Apple » (PU-5 fin / PU-7) : les 2 environnements de la ville et les 9 LIEUX (ID 6030-6038).
# Un lieu = carte Environnement a trait LOCATION (spec ville M1) ; le chiffre imprime dans le coin est le numero de case
# de la grille 3x3, PAS une valeur de jeu. Les 9 lieux sont mis de cote par le scenario et poses par `Ville.Installer`.
# ======================================================================================================
PU_BIG = "The Big Apple"
PU_LOC = "Locations - The Big Apple"
LOC_LIMIT = " <i>(Limit once per round.)</i>"

BIGAPPLE_CARDS = [
    c("pu005", "Environment", "The City", {"Setup": "1", "Permanent": "1"}, [],
      "Setup. Permanent.\n\u2022 Players mark their location in the city with a token, starting in Midtown.\n\u2022 Players can only interact with "
      "locations (abilities & cards attached) they occupy.\n<b>Action</b>: Exhaust a character you control or spend 1 resource of any type "
      "\u2192 move to an adjacent (\u2194 or \u2195) location.", PU_BIG, page="p009"),
    c("pu006", "Environment", "Never Sleeps", {"Setup": "1", "Permanent": "1"}, [],
      "Setup. Permanent.\n\u2022 Each row of locations is the \"turf\" of the villain in that row. Villains only activate against players in "
      "their turf.\n\u2022 Players can only interact with villains or other players (including their play areas) if they are in the same "
      "turf.\n\u2022 Players can interact with all schemes.", PU_BIG, page="p011"),
]

# Jeu de rencontre du scenario 1 : PARTIEL (environnements seulement), complete au fil de PU-7.
BIGAPPLE_ENCOUNTERS = []

LOCATION_CARDS = [
    c("pu030", "Environment", "Hell's Kitchen", {}, ["LOCATION"],
      "Allies and minions in Hell's Kitchen cannot thwart or scheme and gain toughness.\n<b>Action</b>: Confuse and give a tough status card to "
      "your identity \u2192 search the encounter deck for a minion and reveal it.", PU_LOC, page="p059"),
    c("pu031", "Environment", "Theater District", {}, ["LOCATION"],
      "<b>Action</b>: Exhaust a character you control \u2192 heal 2 damage from that character." + LOC_LIMIT, PU_LOC, page="p061"),
    c("pu032", "Environment", "Upper East Side", {}, ["LOCATION"],
      "<b>Action</b>: Discard cards from the encounter deck until a side scheme is discarded. Reveal that scheme." + LOC_LIMIT, PU_LOC, page="p063"),
    c("pu033", "Environment", "West Village", {}, ["LOCATION"],
      "Each player in West Village gets +1 hand size.\n<b>Forced Interrupt</b>: During step 3 of the villain phase, deal yourself an additional "
      "encounter card.", PU_LOC, page="p065"),
    c("pu034", "Environment", "Midtown", {}, ["LOCATION"],
      "<b>Action</b>: Choose a player in this turf. They play an AVENGER, S.H.I.E.L.D., or TECH card from their hand, reducing its cost by 1."
      + LOC_LIMIT, PU_LOC, page="p067"),
    c("pu035", "Environment", "Lower East Side", {}, ["LOCATION"],
      "Each character <i>(including the villain for players here)</i> in Lower East Side gains retaliate 1.", PU_LOC, page="p069"),
    c("pu036", "Environment", "Soho", {}, ["LOCATION"],
      "Increase the cost of each event you play by 1.\n<b>Action</b>: Draw 2 cards, then discard 2 cards." + LOC_LIMIT, PU_LOC, page="p071"),
    c("pu037", "Environment", "Financial District", {}, ["LOCATION"],
      "<b>Hero Action</b>: The villain attacks you. If you take less than 2 damage from this attack, draw 1 card for each printed \u2605 and "
      "[boost] on the attack's boost card(s)." + LOC_LIMIT, PU_LOC, page="p073"),
    c("pu038", "Environment", "Chinatown", {}, ["LOCATION"],
      "<b>Interrupt</b>: When you would be dealt an encounter card, instead discard from the encounter deck until a minion is discarded. "
      "Reveal that minion." + LOC_LIMIT, PU_LOC, page="p075"),
]
# Mis de cote par le scenario (poses dans la grille par Ville.Installer).
LOCATIONS_SET_ASIDE = ["pu030", "pu031", "pu032", "pu033", "pu034", "pu035", "pu036", "pu037", "pu038"]

# ======================================================================================================
# Recapitulatif : 13 + 14 + 5 + 7 + 1 = 40 card_id distincts, pour 15 + 15 + 5 + 7 + 1 = 43 cartes
# physiques (releve "contenu simple" du cadrage section 1.2 : "aucune brique neuve au-dela de M6-M9").
# ======================================================================================================
ALL_CARDS = JIGSAW_CARDS + HOBGOBLIN_CARDS + ARMORY_CARDS + SYNDICATE_CARDS + CAPO_OF_THE_PAST_CARDS + HITLIST_CARDS + SWAT_CARDS + PUNISHMENT_CARDS + BIGAPPLE_CARDS + LOCATION_CARDS
assert len({card["card_id"] for card in ALL_CARDS}) == len(ALL_CARDS), "card_id en double dans ce fichier"
