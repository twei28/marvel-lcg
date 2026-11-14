# Cas test_capacites des CARTES SENSE du deck Daredevil (fne/daredevil, prefixe 60002 a 60006), noms « [fne_sense] ».
# Un cas par capacite ; le card_id est dans le nom. Scripts : src/cards/pack/fne/sense_deck/6000[2-6].py
# (PAS fne/daredevil : un 6000[2-6].py pose la n'est jamais charge).
#
# Montage : vilain Rhino 01094 (14 PV, ATQ 2) ; Daredevil (60001a/60001b, forme heros via DD_HEROS).
# `main_exclusive` dit avec QUOI on paie (01090 = Strength RR).
SC = "rhino"
DD_HEROS = "Puzzle.ChangeToFace('60001b', '60001a')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[fne_sense] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "daredevil"), "mise_en_place": SANS_BOOST + list(mise),
           "declencher": declencher, "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ===================================================================== 60005 Radar Sense
    _c("60005 Radar Sense : Daredevil attaque Rhino (ATQ 2) ; la carte attachee ajoute 3 degats",
       "« After you attack attached enemy, discard this card -> deal 3 damage to that enemy » : 2 + 3 = 5 degats, carte defaussee",
       [DD_HEROS, "Puzzle.AttachReel('60005', '01094')"], ["Puzzle.Attack('60001a')"], {"degats": [["01094", 5]], "hors_jeu": ["60005"]}),
    # ===================================================================== 60004 Heightened Hearing
    _c("60004 Heightened Hearing : Rhino attaque Daredevil ; la carte fait -3 ATQ (Rhino 2 -> 0) et Daredevil devient le defenseur",
       "« Hero Interrupt (defense): that enemy gets -3 ATK for that attack. You become the target »",
       [DD_HEROS, "Puzzle.AttachReel('60004', '01094')"], ["Puzzle.Attack('01094')"], {"hors_jeu": ["60004"], "degats_identite": 0},
       accepter_choix=True),
    # ===================================================================== 60002 Acute Tactility (ramener le heros)
    _c("60002 Acute Tactility : la dernière menace du complot attache est retiree -> interruption : Daredevil redevient pret",
       "« Interrupt: When you remove the last threat from attached scheme, discard -> ready your identity »",
       [DD_HEROS, "Puzzle.SetThreat('01097b', 2)", "Puzzle.AttachReel('60002', '01097b')"], ["Puzzle.Thwart('60001a')"],
       {"hors_jeu": ["60002"], "pret": ["60001a"]}, accepter_choix=True),
    _c("60002 Acute Tactility : il reste de la menace sur le complot attache -> rien ne se declenche",
       "« remove the LAST threat » : 5 - 2 = 3 menaces restantes, la carte reste attachee",
       [DD_HEROS, "Puzzle.SetThreat('01097b', 5)", "Puzzle.AttachReel('60002', '01097b')"], ["Puzzle.Thwart('60001a')"],
       {"en_jeu": ["60002"], "menace": [["01097b", 3]]}, accepter_choix=True),
    _c("60002 Acute Tactility : manigance ANNEXE attachee vaincue par Daredevil -> Daredevil redevient pret",
       "non-regression de la voie d'origine (`WhenSchemeBeDefeated`) : une annexe a 0 menace est vaincue",
       [DD_HEROS, "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 2)", "Puzzle.AttachReel('60002', '01107')"],
       ["Puzzle.Thwart('60001a')"], {"hors_jeu": ["60002", "01107"], "pret": ["60001a"]}, cibles=["01107"], accepter_choix=True),
    # ===================================================================== 60003 Enhanced Olfaction
    _c("60003 Enhanced Olfaction : la dernière menace du complot PRINCIPAL attache est retiree -> la carte se defausse",
       "meme declencheur que 60002 (complot principal jamais vaincu) ; la reduction de cout elle-meme n'est pas mesuree ici",
       [DD_HEROS, "Puzzle.SetThreat('01097b', 2)", "Puzzle.AttachReel('60003', '01097b')"], ["Puzzle.Thwart('60001a')"],
       {"hors_jeu": ["60003"]}, accepter_choix=True),
    # ===================================================================== 60006 Superior Taste
    _c("60006 Superior Taste : Daredevil dejoue le complot attache -> reponse : 2 menaces de plus retirees",
       "« Response (thwart): After you thwart attached scheme, discard -> remove 2 threat from that scheme » : 6 - 2 (contre) - 2 (reponse) = 2",
       [DD_HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.AttachReel('60006', '01097b')"], ["Puzzle.Thwart('60001a')"],
       {"menace": [["01097b", 2]], "hors_jeu": ["60006"]}, accepter_choix=True),
]
