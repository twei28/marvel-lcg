# Entrees cards.json des sets MODULAIRES restants du coffret Skrull Menace (sk228-sk262) :
# Shaper of Worlds, les cinq ensembles d'ELITES (Crusader, Jazinda, Skymax, War Skrull, Xavin) et les
# alternatives Standard Skrull / Expert Skrull. Texte = transcriptions/modular-sets.md, RELU SUR LES SCANS
# (15/10/2026). card_id = sk + numero IMPRIME en pied de carte.
#
# Lectures faites en relisant les scans (voir defs/modulaires_questions.md) :
#  - sk229 Cosmic Cube Creation et sk239 Stealing for the Empire : icone ACCELERATION (croix + pointe + barre).
#  - sk234 Spy Training et sk248 Skrull Geneticist : icone HAZARD (carte penchee nue). La transcription disait
#    « box-with-plus » / « acceleration-style ».
#  - sk252 Super-Skrull Training Program : icone AMPLIFY (croix + avion).
#  - sk243 Surprising Alliance et sk249 Cloning Program : AUCUNE icone au milieu de la boite de texte.
#  - Etoile rouge de boost = pas d'icone chiffree (aucune cle Boost) ; « Y » rose = 1 icone de boost.
#  - sk245 War Skrull : badge ATQ « 2* » (etoile en exposant = renvoi au texte, decision utilisateur) -> ATK "2*".
#  - sk262 Tricky Assault : le numero imprime est « 162 » (coquille : Angar the Screamer porte deja sk162) ;
#    card_id sk262, logique d'apres le x/3 du set Expert Skrull.
#  - Les Impostor (sk246, sk254) et le Skrull Commander (sk247) reutilisent le code de sk098 / sk113 par
#    `ability_link` : aucun script propre.
SW = "Shaper of Worlds"
CR = "Skrull Elite - Crusader"
JA = "Skrull Elite - Jazinda"
SK = "Skrull Elite - Skymax"
WS = "Skrull Elite - War Skrull"
XA = "Skrull Elite - Xavin"
ST = "Standard Skrull"
EX = "Expert Skrull"


def c(cid, typ, name, desc, traits, text, set_name, **extra):
    carte = {"card_id": cid, "type": typ, "name": name, "subtitle": "", "desc": desc,
             "traits": traits, "set_name": set_name, "text": text, "custom": "Kajislav"}
    carte.update(extra)
    return carte


IMPOSTOR = ("Treat attached ally as a [[SKRULL]] minion with a blank text box. Attached minion's SCH is equal to its printed "
            "THW and it does not take consequential damage.\n<b>When Revealed</b>: Attach to the non-[[SKRULL]] ally with "
            "the most remaining hit points without Impostor attached. Attached ally engages its controller. Otherwise, "
            "the villain schemes.")
COMMANDER = ("Each other [[SKRULL]] minion gets +1 ATK.\n[star] <b>Boost</b>: If this activation is an attack, this card "
             "gets +2 boost icons ([boost][boost]) for this attack.")
ATTACHER = "Attach to a [[SKRULL]] minion. If you cannot, attach to the villain."
FRAGMENT = ("<i>An artifact to modify reality following the wishes of the user. The Skrulls were the first race to create "
            "a Cosmic Cube.</i>")

CARDS = [
    # ===================================================================== Shaper of Worlds (228-230d)
    c("sk228", "Minion", "* Shaper of Worlds", {"HP": "INF", "SCH": "2", "ATK": "2"}, ["COSMIC ENTITY", "ELITE", "SKRULL"],
      "<b>Forced Response</b>: After a player attacks Shaper of Worlds, shuffle this card into that player's deck.\n"
      "<b>Forced Interrupt</b>: When Shaper of Worlds enters your hand, discard the top 4 cards of the encounter deck. "
      "Put Shaper of Worlds into play engaged with you.", SW),
    c("sk229", "SideScheme", "Cosmic Cube Creation",
      {"StartingThreat": "2", "Hinder": "4*", "Victory": "2", "Acceleration": "1", "Boost": "3"}, [],
      "Hinder 4[per_hero]. Victory 2.\n<b>When Revealed</b>: Put the set-aside Shaper of Worlds into play engaged with you.\n"
      "<b>When Defeated</b>: Each player chooses a copy of the set-aside Cosmic Cube Fragment resource and shuffles it "
      "into their deck.", SW),
    c("sk230a", "Resource", "Cosmic Cube Fragment", {"RES": "YYY"}, [], FRAGMENT, SW),
    c("sk230b", "Resource", "Cosmic Cube Fragment", {"RES": "BBB"}, [], FRAGMENT, SW),
    c("sk230c", "Resource", "Cosmic Cube Fragment", {"RES": "RRR"}, [], FRAGMENT, SW),
    c("sk230d", "Resource", "Cosmic Cube Fragment", {"RES": "RBY"}, [], FRAGMENT, SW),
    # ===================================================================== Crusader (231-235)
    c("sk231", "Minion", "* Crusader", {"HP": "4*", "SCH": "2", "ATK": "2", "Victory": "1"}, ["ELITE", "SKRULL"],
      "Victory 1.\n<b>When Revealed</b>: Deal 1 damage to each character you control. Give the villain 1 facedown boost "
      "card for each character defeated this way.\n[star] <b>Boost</b>: Put Crusader into play engaged with you.", CR),
    c("sk232", "Attachment", "Enemy Adaptation", {"SCH+": "1", "ATK+": "1", "Boost": "2"}, ["CONDITION"],
      ATTACHER + "\nYou cannot defend against attached enemy's attacks.\n<b>Hero Action</b>: Give the villain 1 facedown "
      "boost card → discard Enemy Adaptation.", CR),
    c("sk233", "Attachment", "* Freedom Ring", {"Boost": "3"}, ["ITEM"],
      "Attach to Crusader. If Crusader is not in play, discard cards from the top of the encounter deck until a minion is "
      "discarded. Put that minion into play engaged with you and attach this card to it. If you cannot, give the villain 1 "
      "facedown boost card.\nAttached minion gains villainous.", CR),
    c("sk234", "SideScheme", "Spy Training", {"StartingThreat": "3*", "Hazard": "1", "Boost": "1"}, [],
      "<i>Z'Reg, a Skrull operative who had been scarred by fellow trainee K'rtem, was sent to spy on the Avengers after his "
      "training was complete.</i>\n<b>When Revealed</b>: Defeat an ally you control and give the villain 1 facedown boost "
      "card.", CR),
    c("sk235", "Treachery", "Rivals to the End", {"Boost": "2"}, [],
      "<b>When Revealed</b>: Choose a minion. That minion attacks your hero twice in a row. If no attack was made this way, "
      "give the villain 1 facedown boost card for each character you control.\n<i>\"Your strategy is pathetic, human! You "
      "rush into battle and then you cradle your weak! Ha! Let me show you how Skrulls heed the call!\" —K'rtem</i>", CR),
    # ===================================================================== Jazinda (236-240)
    c("sk236", "Minion", "* Jazinda", {"HP": "5*", "SCH": "3", "ATK": "1", "Victory": "1"}, ["ELITE", "SKRULL"],
      "Victory 1.\nThe villain gets +1 SCH.\n[star] <b>Boost</b>: Put Jazinda into play engaged with you.\n"
      "<i>\"Pretending to be human is amusing. Especially when I do it so much better than you.\"</i>", JA),
    c("sk237", "Attachment", "Skrull Energy Gun", {"ATK+": "1", "Boost": "1"}, ["WEAPON"],
      ATTACHER + "\nWhile attached to a [[SKRULL]] enemy, attached enemy's attacks gain overkill, piercing, and ranged.\n"
      "<b>Hero Action</b>: Spend a [physical] resource → attach this card to another enemy.", JA),
    c("sk238", "Attachment", "* Sy-Torak Gem", {"ATK+": "1", "Boost": "3"}, ["ARTIFACT"],
      "Attach to Jazinda. If you cannot, attach to the villain.\nAttached character gets +3 hit points.\n"
      "<b>Hero Action</b>: Give the villain 1 facedown boost card and spend a [energy] resource → discard Sy-Torak Gem.", JA),
    c("sk239", "SideScheme", "Stealing for the Empire", {"StartingThreat": "3", "Acceleration": "1"}, [],
      "<i>A former agent of the Skrull Empire was sent to recover a sacred artifact of the Skrull stolen by the Kree.</i>\n"
      "<b>When Revealed</b>: Discard cards from the encounter deck until you discard an attachment. Reveal that attachment. "
      "Then, place threat on the main scheme equal to the number of boost icons ([boost]) on that attachment.", JA),
    c("sk240", "Treachery", "Skrull of Royal Blood", {"Surge": "1"}, [],
      "Surge.\n<b>When Revealed</b>: Shuffle all cards with the highest number of boost icons ([boost]) in the encounter "
      "discard pile into the encounter deck.", JA),
    # ===================================================================== Skymax (241-244)
    c("sk241", "Minion", "* Skymax", {"HP": "5*", "SCH": "2", "ATK": "3", "Victory": "1"}, ["ELITE", "SKRULL"],
      "Victory 1.\n<b>When Revealed</b>: Shuffle all minions from the encounter discard pile into the encounter deck.\n"
      "[star] <b>Boost</b>: Put Skymax into play engaged with you.", SK),
    c("sk242", "Attachment", "Changing Appearance", {"SCH+": "2", "Boost": "2"}, ["CONDITION"],
      ATTACHER + "\nAttached enemy cannot be attacked.\n<b>Forced Interrupt</b>: When attached enemy would attack, it "
      "schemes instead. Then, discard this card.\n<i>\"You're not bad, but my people invented shapeshifting!\" —Skymax</i>", SK),
    c("sk243", "SideScheme", "Surprising Alliance", {"StartingThreat": "2*", "Boost": "1"}, [],
      "<i>\"I am my world's last survivor.\" —Skymax</i>\n<b>Forced Response</b>: When a player discards an ally from their "
      "hand, they put that ally into play engaged with them instead. Treat that ally as a minion with a blank text box. "
      "Its SCH is equal to its printed THW and it does not take consequential damage.", SK),
    c("sk244", "Treachery", "Shape Alteration", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Remove each stunned and confused status card from each [[SKRULL]] enemy and give each "
      "[[SKRULL]] enemy a tough status card. If there are no [[SKRULL]] enemies in play, this card gains surge.\n"
      "[star] <b>Boost</b>: Give 1 [[SKRULL]] enemy a tough status card.", SK),
    # ===================================================================== War Skrull (245-249)
    c("sk245", "Minion", "* War Skrull", {"HP": "5*", "SCH": "2", "ATK": "2*", "Victory": "1"}, ["ELITE", "SKRULL"],
      "Victory 1.\n[star] <b>Forced Response</b>: After War Skrull attacks you, discard the top 2 cards of your deck.\n"
      "[star] <b>Boost</b>: Put War Skrull into play engaged with you.", WS),
    c("sk246", "Attachment", "Impostor", {"Boost": "1"}, ["CONDITION"], IMPOSTOR, WS, ability_link="sk098"),
    c("sk247", "Minion", "Skrull Commander", {"HP": "5", "SCH": "2", "ATK": "2", "Boost": "1"}, ["SKRULL", "SOLDIER"],
      COMMANDER + "\n<i>\"If he was a significant threat, we would know who he is\" —Commander Ak'strk</i>", WS,
      ability_link="sk113"),
    c("sk248", "Minion", "Skrull Geneticist", {"HP": "3", "SCH": "3", "ATK": "0", "Hazard": "1", "Boost": "1"},
      ["GENIUS", "SKRULL"],
      "[star] <b>Boost</b>: Deal yourself a facedown encounter card.\n<i>\"These results are fascinating\"</i>", WS),
    c("sk249", "SideScheme", "Cloning Program", {"StartingThreat": "4", "Boost": "1"}, [],
      "<i>The Skrull scientists had cloned samples of Deadpool's blood and use it to upgrade a squadron of Super-Skrulls. "
      "They also place Deadpool in charge of training these new Super-Skrulls.</i>\nEach [[SKRULL]] minion activates 1 "
      "additional time during the step two of the villain phase.\nThreat cannot be removed from this scheme while there is "
      "no [[SKRULL]] minion in play.", WS),
    # ===================================================================== Xavin (250-253)
    c("sk250", "Minion", "* Xavin", {"HP": "5*", "SCH": "2", "ATK": "3", "Victory": "1"}, ["ELITE", "SKRULL"],
      "Victory 1.\n<b>When Revealed</b>: Discard cards from the encounter deck until a treachery is discarded. Reveal that "
      "treachery.\n[star] <b>Boost</b>: Put Xavin into play engaged with you.", XA),
    c("sk251", "Attachment", "Invisible Forcefield", {}, [],
      "Attach to the enemy with the highest printed hit points and without another Invisible Forcefield attached. If you "
      "cannot, this card gains surge.\n<b>Forced Interrupt</b>: When any amount of damage would be dealt to attached "
      "character, place it here instead. Then, if there is at least 5 damage here, discard this card.", XA),
    c("sk252", "SideScheme", "Super-Skrull Training Program", {"StartingThreat": "2*", "Amplify": "1", "Boost": "1"}, [],
      "<i>\"Always remember, when you face a superior opponent, learn their weaknesses. Exploit them. That is the Skrull "
      "way.\" —Commander Chrell</i>\n<b>When Revealed</b>: Give each [[SKRULL]] enemy a tough status card.", XA),
    c("sk253", "Treachery", "Going Nova", {"Boost": "3"}, [],
      "<b>When Revealed</b>: Assign 2[per_hero] indirect damage among players.\n<i>\"Damnation. I keep forgetting how fragile "
      "you people are.\" —Xavin</i>", XA),
    # ===================================================================== Standard Skrull (254-259)
    c("sk254", "Attachment", "Impostor", {"Boost": "1"}, ["CONDITION"], IMPOSTOR, ST, ability_link="sk098"),
    c("sk255", "Treachery", "Cursed by the Past", {"Boost": "2"}, [],
      "<b>When Revealed</b>: If your nemesis minion is in play, it activates against you. Otherwise, find your nemesis "
      "minion and reveal it. If your nemesis side scheme is in play, place threat on it equal to its starting threat value. "
      "Otherwise, find your nemesis side scheme and reveal it. Shuffle your remaining set-aside nemesis set into the "
      "encounter deck.", ST),
    c("sk256", "Treachery", "Experiment Subject", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Discard an upgrade you control. If no card was discarded this way, the villain schemes.\n"
      "<i>\"I am curious to see just what the upper limits of his extension are...\" —Skrull Scientist</i>", ST),
    c("sk257", "Treachery", "Forge Ahead", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Each minion engaged with you schemes. If no scheme was made this way, the villain schemes.\n"
      "<i>\"We are not speaking of conquest. Think of it more as a... strategic protective occupation.\" —Nogor</i>", ST),
    c("sk258", "Treachery", "Mobilization", {"Boost": "1"}, [],
      "<b>When Revealed (Alter-Ego)</b>: Engage each minion in play. The villain schemes.\n"
      "<b>When Revealed (Hero)</b>: The villain and each minion engaged with you attacks you.\n"
      "<i>\"We are by any and all definitions, the superior race!\" —Dorrek VII</i>", ST),
    c("sk259", "Treachery", "Stick to the Plan", {}, [],
      "<b>When Revealed</b>: The villain attacks the hero with the most remaining hit points. If no attack was made this "
      "way, the villain schemes.\n<i>\"Bow down and beg to the Skrulls!\" —Paibok</i>", ST),
    # ===================================================================== Expert Skrull (260-262)
    c("sk260", "Attachment", "Replaced Archenemy", {"SCH+": "1", "Boost": "2"}, ["CONDITION"],
      "Attached minion gains the [[SKRULL]] trait.\n<b>When Revealed</b>: If your nemesis minion is in play, attach this "
      "card to it. Then, it activates against you. Otherwise, find your nemesis minion, attach this card to it and reveal "
      "it.", EX),
    c("sk261", "Treachery", "Focused Attention", {"Surge": "1", "Boost": "3"}, [],
      "Surge.\n<b>When Revealed</b>: Give the villain 1 facedown boost card.\n<i>\"Earth shall pay for what it has done to "
      "my people!\" —Super-Skrull</i>", EX),
    c("sk262", "Treachery", "Tricky Assault", {"Boost": "2"}, [],
      "<b>When Revealed</b>: Flip to hero form. The villain attacks you. If this attack is undefended, the villain "
      "schemes.\n<i>\"We are prepared to accept your surrender.\" —Unknown Skrull</i>", EX),
]

# Contenu des ensembles (card_id repetes = copies), dans l'ordre imprime.
ENCOUNTERS = {
    "sk_shaper_of_worlds": ("Shaper of Worlds", ["sk228", "sk229", "sk230a", "sk230b", "sk230c", "sk230d"]),
    "sk_skrull_elite_crusader": ("Skrull Elite - Crusader", ["sk231", "sk232", "sk233", "sk234", "sk235", "sk235"]),
    "sk_skrull_elite_jazinda": ("Skrull Elite - Jazinda", ["sk236", "sk237", "sk238", "sk239", "sk239", "sk240"]),
    "sk_skrull_elite_skymax": ("Skrull Elite - Skymax", ["sk241", "sk242", "sk242", "sk243", "sk244", "sk244"]),
    "sk_skrull_elite_war_skrull": ("Skrull Elite - War Skrull", ["sk245", "sk246", "sk247", "sk248", "sk249", "sk249"]),
    "sk_skrull_elite_xavin": ("Skrull Elite - Xavin", ["sk250", "sk251", "sk251", "sk252", "sk253", "sk253"]),
    # ⚠ Noms SANS le prefixe `sk_` : le moteur et l'interface classent les sets de la famille Standard / Expert par
    # leur NOM (`startswith("standard")` / `startswith("expert")` : SetModularSetsAside ne les compte pas comme
    # modulaires, catalog.js ne les propose pas comme modulaires, niveau-standard.js les echange).
    "standard_skrull": ("Standard Skrull", ["sk254", "sk255", "sk256", "sk257", "sk258", "sk259", "sk259"]),
    "expert_skrull": ("Expert Skrull", ["sk260", "sk261", "sk262"]),
}
ANCIENS_NOMS = ["sk_standard_skrull", "sk_expert_skrull"]  # premiere version du bloc, a retirer du depot
