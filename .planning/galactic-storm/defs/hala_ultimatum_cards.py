# Entrees cards.json du scenario 3 HALA ULTIMATUM de Galactic Storm (gs138-gs155), lot GS-6 (20/10/2026).
# Texte = docs/packs/galactic-storm/transcriptions/hala-ultimatum.md, RELU SUR LES SCANS le 20/10/2026.
# card_id = gs + numero IMPRIME en pied de carte, 3 chiffres (+ a/b pour les deux faces du mechant et des
# manigances principales) ; UN card_id par numero, les copies sont des exemplaires du paquet (decision GS-0 Q3).
#
# MECHANT CACHE (HIDDEN) : chaque stade (I/II/III) est UNE carte a deux faces, HIDDEN (Kree Leader, face a)
# et DISCOVERED (Tanalth, face b). `Scenario.AdvanceVillainStage` choisit nativement, au stade suivant, la
# face du MEME NOM que celle qui vient d'etre vaincue (« the next stage enters play on the same side as the
# just-defeated stage ») : d'ou gs138a/gs139a/gs140a nommes tous « Kree Leader » et gs138b/gs139b/gs140b
# tous « Tanalth ». Le retournement HIDDEN -> DISCOVERED (gs142a, Reckoning Begins) utilise `card.Flip`, qui
# garde la MEME carte (attachements/statuts/degats restent).
HALA = "Hala Ultimatum"


def c(cid, typ, name, desc, traits, text, subtitle=""):
    return {"card_id": cid, "type": typ, "name": name, "subtitle": subtitle, "desc": desc,
            "traits": traits, "set_name": HALA, "text": text, "custom": "Kajislav"}


IMMUNITE_ET_INDISCUTABLE = ("The villain cannot be affected by player cards. Attachments attached to the "
                             "villain cannot be discarded.\n[star] <b>Forced Interrupt</b>: When the villain "
                             "would attack you, deal yourself a facedown encounter card instead.")
CITATION_KREE_LEADER = "<i>\"Hidden on Hala, the Kree leader arms to face heroes.\"</i>"
REPONSE_TANALTH_1_2 = ("[star] <b>Forced Response</b>: After Tanalth attacks and defeats a character, give "
                       "her a tough status card. If she already has a tough status card, give her a "
                       "facedown boost card.")
REPONSE_TANALTH_3 = ("[star] <b>Forced Response</b>: After Tanalth attacks and defeats a character, give "
                     "her a tough status card and a facedown boost card.")

CARDS = [
    # --- Mechant : Kree Leader (HIDDEN) / Tanalth (DISCOVERED), 3 stades --------------------------------
    c("gs138a", "Villain", "Kree Leader", {"HP": "15*", "ATK": "0", "SCH": "2", "Stage": "1"}, ["HIDDEN", "KREE"],
      IMMUNITE_ET_INDISCUTABLE + "\n" + CITATION_KREE_LEADER),
    c("gs138b", "Villain", "Tanalth", {"HP": "15*", "ATK": "2", "SCH": "2", "Stage": "1"}, ["DISCOVERED", "KREE"],
      REPONSE_TANALTH_1_2 + "\n<i>\"I have prey, then I hunt it, and kill or capture. For I am Tanalth, "
      "Grand-High Pursuer of the Kree.\"</i>"),
    c("gs139a", "Villain", "Kree Leader", {"HP": "18*", "ATK": "0", "SCH": "2", "Stage": "2"}, ["HIDDEN", "KREE"],
      IMMUNITE_ET_INDISCUTABLE + "\n" + CITATION_KREE_LEADER),
    c("gs139b", "Villain", "Tanalth", {"HP": "18*", "ATK": "3", "SCH": "2", "Stage": "2"}, ["DISCOVERED", "KREE"],
      REPONSE_TANALTH_1_2 + "\n<i>\"In a shocking revelation, the Kree leader Tanalth proved to be none other "
      "than the Skrull Empress R'KIII.\"</i>"),
    c("gs140a", "Villain", "Kree Leader", {"HP": "21*", "ATK": "0", "SCH": "2", "Stage": "3"}, ["HIDDEN", "KREE"],
      IMMUNITE_ET_INDISCUTABLE + "\n" + CITATION_KREE_LEADER),
    c("gs140b", "Villain", "Tanalth", {"HP": "21*", "ATK": "4", "SCH": "2", "Stage": "3", "Steady": "1"},
      ["DISCOVERED", "KREE"],
      "Steady.\n<b>When Revealed</b>: Search the encounter deck and discard pile for Grand-High Pursuer and "
      "attach it to Tanalth.\n" + REPONSE_TANALTH_3),
    # --- Manigances principales ------------------------------------------------------------------------
    c("gs141a", "MainScheme", "Hidden Might of Hala", {"Stage": "1"}, [],
      "<b>Contents</b>: Kree Leader (I) and Kree Leader (II) <i>(Kree Leader (II) and Kree Leader (III) "
      "instead for expert mode)</i>. Hala Ultimatum and Standard encounter sets. One modular encounter set "
      "<i>(Accuser Corps)</i>.\n<b>Setup</b>: Put the Hala environment into play. Each player searches the "
      "encounter deck for a KREE minion and reveals it."),
    c("gs141b", "MainScheme",
      "Hidden Might of Hala", {"Stage": "1", "TargetThreat": "9*", "EscalationThreat": "1*", "StartingThreat": "2*"},
      [],
      "<i>Heroes traveled to the Kree homeworld to stop their conquest and expansion.</i>\n<b>Forced "
      "Interrupt</b>: When a minion is defeated, remove 1 hideout counter from Hala.\n<b>Forced Response</b>: "
      "After the last hideout counter is removed from Hala, advance to stage 2A.\n<b>If this scheme is "
      "completed, the players lose the game.</b>"),
    c("gs142a", "MainScheme", "Reckoning Begins", {"Stage": "2"}, [],
      "<i>From the depths of Hala to the front lines, Tanalth and her elite Kree legions advance, signaling "
      "the Empire's wrath.</i>\n<b>When Revealed</b>: Flip the villain to its DISCOVERED side and set the "
      "Hala environment aside. Each player draws 1 card."),
    c("gs142b", "MainScheme",
      "Reckoning Begins", {"Stage": "2", "TargetThreat": "10*", "EscalationThreat": "1*", "StartingThreat": "1*"},
      [],
      "<i>The air trembles as Tanalth appears, her voice carrying orders that stir the Kree army into "
      "relentless action.</i>\n<b>If this scheme is completed, the players lose the game.</b>"),
    # --- Environnement -----------------------------------------------------------------------------------
    c("gs143", "Environment", "* Hala", {}, ["LOCATION", "PLANET"],
      "Enters play with 2 hideout counters, plus 2[per_hero] additional hideout counters.\n<i>Scour the "
      "Planet</i> — <b>Action</b>: Search the encounter deck and discard pile for a KREE minion and reveal "
      "it → draw 1 card. <i>(Limit once per round per player.)</i>"),
    # --- Attachements du mechant --------------------------------------------------------------------------
    c("gs144", "Attachment", "* Grand-High Pursuer", {"ATK+": "1", "Boost": "2"}, ["TITLE"],
      "Attach to the villain.\nAttached villain gains retaliate 1.\n<b>Hero Action</b>: Spend [energy]"
      "[mental][physical] resources → discard this card.\n<hr />\n[star] <b>Boost</b>: If the "
      "activating enemy has a tough status card, give it an additional boost card."),
    c("gs145", "Attachment", "Kree Plasma Rifle", {"ATK+": "1", "Boost": "2"}, ["WEAPON"],
      "Attach to the villain.\n[star] Attached villain's attacks gain piercing and ranged.\n<b>Hero "
      "Action</b>: Spend [energy][mental][physical] resources → discard this card.\n<i>\"I would have "
      "given you all quick deaths. As painless as possible! Not anymore...\" —Tanalth</i>"),
    c("gs146", "Attachment", "Kree Resilience", {"Boost": "2"}, ["CONDITION"],
      "Attach to the villain.\nAttached villain can have 1 additional tough status card.\n<b>Hero "
      "Action</b>: Spend [physical][physical] resources → discard this card.\n<hr />\n[star] "
      "<b>Boost</b>: Give the activating enemy a tough status card.\n<i>\"To the last Kree!\" "
      "—Tanalth</i>"),
    # --- Sbires ---------------------------------------------------------------------------------------------
    c("gs147", "Minion", "Kree Assassin", {"SCH": "1", "ATK": "3", "HP": "5", "Boost": "1", "Retaliate": "1"},
      ["KREE"],
      "Retaliate 1.\n<hr />\n[star] <b>Boost</b>: If the activating enemy has a tough status card, exhaust "
      "your identity.\n<i>\"All we await now is our target.\" —Sals-Bek</i>"),
    c("gs148", "Minion", "Kree Pursuer",
      {"SCH": "1", "ATK": "2", "HP": "6", "Boost": "2", "Patrol": "1", "Quickstrike": "1"},
      ["KREE", "PURSUER CORPS"],
      "Patrol. Quickstrike.\n<b>When Defeated</b>: If the villain has a tough status card, shuffle Kree "
      "Pursuer into the encounter deck.\n<i>\"Get out of the way!\"</i>"),
    c("gs149", "Minion", "Kree Soldier", {"SCH": "1", "ATK": "2", "HP": "5", "Guard": "1"}, ["KREE", "SOLDIER"],
      "Guard.\n<hr />\n[star] <b>Boost</b>: If the activating enemy has a tough status card, put Kree "
      "Soldier into play engaged with you.\n<i>\"The Kree army protects its own...\"</i>"),
    # --- Manigances annexes -----------------------------------------------------------------------------------
    c("gs150", "SideScheme", "House of Fiyero", {"StartingThreat": "4", "Hinder": "1*", "Boost": "3"}, [],
      "<i>A powerful Kree guild, using its wealth and influence to pursue its ambitions.</i>\nHinder "
      "1[per_hero].\n<b>When Defeated</b>: Remove 1 hideout counter from Hala. If you cannot, the "
      "defeating player may discard an attachment with the text \"Hero Action\" from an enemy."),
    c("gs151", "SideScheme", "Mobilizing the Empire", {"StartingThreat": "4", "Hinder": "1*", "Boost": "2"}, [],
      "<i>The Kree are an extremely militaristic and disciplined race, bred for war, conquest, and absolute "
      "loyalty to their empire.</i>\nHinder 1[per_hero].\n<b>When Defeated</b>: Remove 1 hideout counter "
      "from Hala. If you cannot, the defeating player may draw 1 card."),
    c("gs152", "SideScheme", "Secrets of Detention Core", {"StartingThreat": "4", "Hinder": "1*", "Boost": "1"}, [],
      "<i>Every prisoner of Hala serves the Kree Empire one way or another.</i>\nHinder 1[per_hero].\n<b>When "
      "Defeated</b>: Remove 1 hideout counter from Hala. If you cannot, the defeating player may ready a "
      "character they control."),
    # --- Traitrises ---------------------------------------------------------------------------------------------
    c("gs153", "Treachery", "Advanced Arsenal", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Give the villain a tough status card. If the villain already has a tough "
      "status card, discard cards from the encounter deck until you discard an attachment or a minion and "
      "reveal it."),
    c("gs154", "Treachery", "Battle Cry", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Give the villain a tough status card. If the villain already has a tough "
      "status card, give it a facedown boost card.\n<hr />\n[star] <b>Boost</b>: If the activating enemy "
      "has a tough status card, this card gets +2 boost icons for this activation."),
    c("gs155", "Treachery", "Bloodthirst of Hala", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Give the villain a tough status card. If the villain already has a tough "
      "status card, the villain activates against you.\n<i>\"No quarter! Remember you are Kree!\" "
      "—Ronan</i>"),
]

# Paquet rencontre propre du scenario (22 cartes, numeros 7 a 28 de « HALA ULTIMATUM (n/28) »).
ENCOUNTERS = (
    ["gs144"] + ["gs145"] + ["gs146"] * 2 + ["gs147"] * 2 + ["gs148"] * 2 + ["gs149"] * 4
    + ["gs150"] + ["gs151"] * 2 + ["gs152"] + ["gs153"] * 2 + ["gs154"] * 2 + ["gs155"] * 2
)
# Hala (gs143) est mis de cote, mis en jeu par le Setup de gs141a.
SET_ASIDE = ["gs143"]
