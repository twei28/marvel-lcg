# Entrees cards.json du scenario 3 PAIBOK (sk141-160) et du set modulaire NEW REVENGERS (sk161-169).
# Texte = transcriptions/paibok.md et transcriptions/modular-sets.md, RELU SUR LES SCANS (15/10/2026).
# card_id = sk + numero IMPRIME en pied de carte (« MC Custom Content By Kajislav <n> »).
#
# Lectures faites en relisant les scans (voir defs/paibok_questions.md) :
#  - sk146 Captain Paibok porte une icone HAZARD (carte penchee, croix, rien dessous) au milieu de
#    sa boite de texte : la transcription l'appelait « icone de heros ».
#  - sk156 Galactic Ambassador et sk168 The Revenge Time portent l'icone ACCELERATION (decision
#    utilisateur du 15/10/2026 pour sk156 ; meme forme, pointe + barre, sur sk168).
#  - Badge ATK etoile seul d'Ice Control (sk150) : « voir le texte » (decision utilisateur) ; pas de
#    cle ATK+ dans le desc, seul le +1 SCH est chiffre.
#  - Etoile rouge de boost = pas d'icone chiffree (aucune cle Boost) ; « Y » rose = 1 icone de boost.
PA = "Paibok"
NR = "New Revengers"


def c(cid, typ, name, desc, traits, text, set_name):
    return {"card_id": cid, "type": typ, "name": name, "subtitle": "", "desc": desc,
            "traits": traits, "set_name": set_name, "text": text, "custom": "Kajislav"}


REGLE = ("While the number of [[POWER SKRULL]] cards attached to Paibok is equal to or less than the number of "
         "mastery counters on him, [[POWER SKRULL]] cards cannot be discarded.")
FOUILLE = "<b>When Revealed</b>: Search the encounter deck and discard pile for a [[POWER SKRULL]] card and reveal it."
BOOST_PAIBOK = 'Resolve the "<b>Boost</b>" ability on each attachment in play that belongs to the Paibok encounter set'

CARDS = [
    # --- Mechants -------------------------------------------------------------------------
    c("sk141", "Villain", "* Paibok", {"HP": "13*", "ATK": "2", "SCH": "1", "Toughness": "1", "Stage": "1"},
      ["SKRULL"], "Toughness.\n" + REGLE, PA),
    c("sk142", "Villain", "* Paibok", {"HP": "16*", "ATK": "2", "SCH": "2", "Toughness": "1", "Stage": "2"},
      ["SKRULL"], "Toughness.\n" + REGLE + "\n" + FOUILLE, PA),
    c("sk143", "Villain", "* Paibok", {"HP": "20*", "ATK": "3", "SCH": "3", "Toughness": "1", "Stage": "3"},
      ["SKRULL"], "Toughness.\n" + REGLE + "\n" + FOUILLE, PA),
    # --- Complots principaux ------------------------------------------------------------------
    c("sk144a", "MainScheme", "Power Skrull Engineering", {"Stage": "1"}, [],
      "<b>Contents</b>: Paibok I and Paibok II <i>(Paibok II and Paibok III for expert mode)</i>. Paibok and Standard "
      "encounter sets. One modular encounter set <i>(New Revengers)</i>.\n<b>Setup</b>: Place 1 mastery counter on Paibok.", PA),
    c("sk144b", "MainScheme", "Power Skrull Engineering",
      {"Stage": "1", "TargetThreat": "5*", "EscalationThreat": "1*", "StartingThreat": "1*"}, [],
      "<b>When Revealed</b>: Discard cards from the encounter deck until a [[POWER SKRULL]] card is discarded. Reveal that card. "
      "Shuffle the encounter discard pile into the encounter deck.", PA),
    c("sk145a", "MainScheme", "Mastering Superpowers", {"Stage": "2"}, [],
      "<b>When Revealed</b>: Place 1 mastery counter on Paibok. Then, if Captain Paibok is in play, resolve its \"<b>Boost</b>\" "
      "ability. Otherwise, search the encounter deck and discard pile for Captain Paibok and attach it to Paibok. "
      "Shuffle the encounter deck.", PA),
    c("sk145b", "MainScheme", "Mastering Superpowers",
      {"Stage": "2", "TargetThreat": "5*", "EscalationThreat": "1*", "StartingThreat": "0"}, [],
      "[star] <b>Forced Interrupt</b>: When this scheme would be completed, place 1 mastery counter on Paibok and remove all "
      "threat from here instead. Then, discard cards from the encounter deck until a [[POWER SKRULL]] card is discarded. "
      "Reveal that card.\n<b>When the player phase ends, if all 4 [[POWER SKRULL]] cards are attached to Paibok, the players "
      "lose the game.</b>", PA),
    # --- Attachements ----------------------------------------------------------------------
    c("sk146", "Attachment", "Captain Paibok", {"Boost": "2", "Hazard": "1"}, ["TITLE"],
      "Attach to Paibok.\n<b>Hero Action</b>: " + BOOST_PAIBOK + " → discard this card.\n<hr />\n"
      "[star] <b>Boost</b>: Heal 2 damage from Paibok.", PA),
    c("sk147", "Attachment", "Distracted", {}, ["CONDITION"],
      "Attach to your identity.\n<b>Forced Interrupt</b>: When you thwart, reduce the amount of threat that thwart removes by 1.\n"
      "<b>Hero Action</b>: Spend [mental][mental] resources → discard this card.\n<hr />\n"
      "[star] <b>Boost</b>: Place 1 threat on the main scheme.", PA),
    c("sk148", "Attachment", "Electricity Projection", {"Boost": "1", "ATK+": "1"}, ["POWER SKRULL"],
      "Attach to Paibok.\nPaibok gains retaliate 1.\n<b>Hero Action</b>: Spend [mental][physical] resources → discard this card.\n<hr />\n"
      "[star] <b>Boost</b>: Stun a character you control.", PA),
    c("sk149", "Attachment", "Hypnotized", {}, ["CONDITION"],
      "Attach to your identity.\nAs an additional cost to change form, you must spend 1 resource of any type.\n"
      "<b>Hero Action</b>: Spend [energy][energy] resources → discard this card.\n<hr />\n"
      "[star] <b>Boost</b>: Discard 1 card from your hand.", PA),
    c("sk150", "Attachment", "Ice Control", {"Boost": "1", "SCH+": "1"}, ["POWER SKRULL"],
      "Attach to Paibok.\n[star] <b>Forced Response</b>: After Paibok attacks you, exhaust a character you control.\n"
      "<b>Hero Action</b>: Spend 3 resources of any type → discard this card.\n<hr />\n"
      "[star] <b>Boost</b>: Exhaust a character you control.", PA),
    c("sk151", "Attachment", "Metallic Skin", {"Boost": "1", "ATK+": "1"}, ["POWER SKRULL"],
      "Attach to Paibok.\n<b>Forced Response</b>: After Paibok takes damage, give him a tough status card.\n"
      "<b>Hero Action</b>: Spend [energy][mental] resources → discard this card.\n<hr />\n"
      "[star] <b>Boost</b>: Give Paibok a tough status card.", PA),
    c("sk152", "Attachment", "Shapeshifting", {"Boost": "1", "SCH+": "1"}, ["POWER SKRULL"],
      "Attach to Paibok.\nPaibok gains stalwart and the [[AERIAL]] trait.\n"
      "<b>Hero Action</b>: Spend [energy][physical] resources → discard this card.\n<hr />\n"
      "[star] <b>Boost</b>: Confuse a character you control.", PA),
    c("sk153", "Attachment", "Trapped in Ice", {}, ["CONDITION"],
      "Attach to your identity.\n<b>Forced Interrupt</b>: When you attack, reduce the amount of damage that attacks deals by 1.\n"
      "<b>Hero Action</b>: Spend [physical][physical] resources → discard this card.\n<hr />\n"
      "[star] <b>Boost</b>: Take 1 damage.", PA),
    # --- Sbires ----------------------------------------------------------------------------
    c("sk154", "Minion", "* Devos the Devastator", {"HP": "5", "SCH": "1", "ATK": "4", "Boost": "4"}, ["ELITE"],
      "<b>Forced Response</b>: After a status card is placed on a friendly character, Devos the Devastator activates against "
      "the player who controls that character.", PA),
    c("sk155", "Minion", "* General Kalamari", {"HP": "4", "SCH": "2", "ATK": "2", "Boost": "2"}, ["ELITE", "SKRULL", "SOLDIER"],
      "<b>When Defeated</b>: The player who defeated General Kalamari resolves the \"<b>Boost</b>\" ability on each attachment "
      "in play, that belongs to the Paibok encounter set.", PA),
    # --- Complots annexes ----------------------------------------------------------------------
    c("sk156", "SideScheme", "Galactic Ambassador", {"StartingThreat": "2*", "Acceleration": "1", "Boost": "1"}, [],
      "<b>When Revealed</b>: Place 2 additional threat here for each friendly character with a status card.", PA),
    c("sk157", "SideScheme", "Settling Scores", {"StartingThreat": "2", "Hinder": "2*", "Boost": "2"}, [],
      "Hinder 2[per_hero].\nResolve the \"<b>Boost</b>\" ability on each boost card 1 additional time.\n"
      "<b>When Revealed</b>: Shuffle each [[POWER SKRULL]] card from the encounter discard pile into the encounter deck.", PA),
    # --- Traitrises ------------------------------------------------------------------------
    c("sk158", "Treachery", "Council Manipulation", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Paibok schemes. If you are stunned or confused, this card gains surge.", PA),
    c("sk159", "Treachery", "Getting Ruthless", {"Boost": "2"}, [],
      "<b>When Revealed (Alter-Ego)</b>: " + BOOST_PAIBOK + ".\n"
      "<b>When Revealed (Hero)</b>: Paibok attacks you. Give him 1 additional boost card if you are stunned or confused.", PA),
    c("sk160", "Treachery", "Power Demonstration", {"Boost": "2"}, [],
      "<b>When Revealed</b>: " + BOOST_PAIBOK + ".", PA),
    # --- NEW REVENGERS ------------------------------------------------------------------------
    c("sk161", "Environment", "O.M.N.I.T.R.O.N.I.C.U.S.", {"Boost": "1"}, ["COMPUTER", "REVENGER"],
      "Each [[REVENGER]] minion gains villainous.\n<b>Hero Action</b>: If there is no [[REVENGER]] enemy in play, spend "
      "[energy][energy] resources → discard this card.", NR),
    c("sk162", "Minion", "* Angar the Screamer", {"HP": "4", "SCH": "1", "ATK": "2*", "Boost": "1"}, ["REVENGER"],
      "[star] Angar the Screamer's attacks gain ranged.\n<b>Forced Interrupt</b>: When Angar the Screamer attacks you, also "
      "resolve his attack against each other hero.", NR),
    c("sk163", "Minion", "* Asti the All-Seeing", {"HP": "4", "SCH": "2", "ATK": "1", "Boost": "1"}, ["REVENGER"],
      "<b>Forced Interrupt</b>: When Asti the All-Seeing takes any amount of damage, place 1 absorption counter on it.\n"
      "<b>When Defeated</b>: Assign 2 indirect damage among players for each absorption counter on Asti the All-Seeing.", NR),
    c("sk164", "Minion", "* Skar", {"HP": "4", "SCH": "1", "ATK": "3*", "Boost": "2"}, ["REVENGER"],
      "[star] Skar's attacks gain overkill.\n<b>When Revealed</b>: Exhaust a character you control.", NR),
    c("sk165", "Minion", "* The Maker", {"HP": "3", "SCH": "3", "ATK": "1", "Boost": "3"}, ["ELITE", "REVENGER"],
      "The Maker cannot take damage while another [[REVENGER]] enemy is in play.\n<b>When Revealed</b>: Search the encounter "
      "deck and discard pile for The Revenge Time side scheme and reveal it.", NR),
    c("sk166", "Minion", "* Vermin", {"HP": "5", "SCH": "1", "ATK": "2*", "Boost": "1"}, ["REVENGER"],
      "[star] Vermin's attacks deal indirect damage.\n<hr />\n"
      "[star] <b>Boost</b>: If this activation is an attack, it deals indirect damage.", NR),
    c("sk167", "Minion", "* White Tiger", {"HP": "3", "SCH": "2", "ATK": "2", "Boost": "2", "Quickstrike": "1"}, ["REVENGER"],
      "Quickstrike. <i>(After this minion engages your hero, it attacks you.)</i>\n"
      "<b>When Defeated</b>: Give the villain 1 facedown boost card.", NR),
    c("sk168", "SideScheme", "The Revenge Time", {"StartingThreat": "2*", "Acceleration": "1", "Boost": "2"}, [],
      "The villain gains the [[REVENGER]] trait.\n<b>When Revealed</b>: Place 1 additional threat here for each [[REVENGER]] "
      "enemy in play.", NR),
    c("sk169", "Treachery", "Forming the Revengers", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Discard cards from the top of the encounter deck until a card with the [[REVENGER]] trait is "
      "discarded. Reveal that card.", NR),
]

# Composition des decks / scenarios (copies incluses). Une seule entree cards.json par card_id.
ENCOUNTERS_PAIBOK = (["sk146", "sk147", "sk147", "sk148", "sk149", "sk149", "sk150", "sk151", "sk152", "sk153", "sk153",
                      "sk154", "sk155", "sk156", "sk157", "sk157", "sk158", "sk159", "sk159"] + ["sk160"] * 4)
ENCOUNTERS_REVENGERS = ["sk161", "sk162", "sk163", "sk164", "sk165", "sk166", "sk167", "sk168", "sk169", "sk169"]
