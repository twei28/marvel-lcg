# Cas test_capacites du scenario THE VAULT, 4e fichier : LES CARTES DE RENCONTRE (vt020 Craven Escape, vt022 Corrupted Guardsman, vt026 Burglary,
# vt028 Contingency Measures, vt029 Scheming from Within, vt030 Rampage in Public, vt034 Riot in the Vault). Memes conventions et aides que
# `the_vault.py` ; prefixe de nom « [vt] ».
#
# Rappels : `01121` (Weapons Runner) sert de TEMOIN DE SURGE : pose au sommet du deck de rencontre, il en sort si et seulement si un surge a
# joue (`carte_du_surge`) ; `main_exclusive: ["01090"]` ecarte « Great Responsibility » (01061) de la main du pilote (il interrompt les menaces).
# Inspection of the Vault en jeu = `Puzzle.PutIntoPlay('vt019', under_control=True)`.
import importlib.util as _imp
import os as _os

_spec = _imp.spec_from_file_location("cas_vt_aides", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "the_vault.py"))
_h = _imp.module_from_spec(_spec)
_spec.loader.exec_module(_h)
_c, mechants_en_jeu, sous_le_vault = _h._c, _h.mechants_en_jeu, _h.sous_le_vault
HEROS = _h.HEROS
SURGE = "Puzzle.CreateEncounterDeck('01121')"      # le dernier cree est le DESSUS du deck
INSPECTION = "Puzzle.PutIntoPlay('vt019', under_control=True)"
MX = {"main_exclusive": ["01090"]}
H = "01001a"

CAS = [
    # ============================================================ vt020 Craven Escape
    _c("vt020 Craven Escape : s'attache au vilain qui a le MOINS de PV restants (Batroc 7-4 = 3 contre Hydro-Man 7)",
       "« Attach to the villain with the fewest remaining hit points »",
       mechants_en_jeu("vt001", "vt007") + sous_le_vault("vt003") + ["Puzzle.Damage('vt001', 4)"], ["Puzzle.Reveal('vt020')"],
       {"attaches": [["vt001", "vt020"]]}, **MX),
    _c("vt020 Craven Escape : « WITHOUT another Craven Escape attached » : la 2e copie va sur l'AUTRE vilain (Batroc a deja la 1re)",
       "« ... and without another Craven Escape attached »",
       mechants_en_jeu("vt001", "vt007") + sous_le_vault("vt003") + ["Puzzle.Damage('vt001', 4)"], ["Puzzle.Reveal('vt020')", "Puzzle.CreateEncounterDeck('vt020')", "Puzzle.Reveal('vt020')"],
       {"attaches": [["vt001", "vt020"], ["vt007", "vt020"]]}, **MX),
    _c("vt020 Craven Escape : aucun vilain sans Craven Escape -> la carte gagne SURGE (le temoin est revele)",
       "« If you cannot, this card gains surge »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003") + [SURGE], ["Puzzle.Reveal('vt020')", "Puzzle.CreateEncounterDeck('vt020')", "Puzzle.Reveal('vt020')"],
       {"carte_du_surge": "01121"}, verifier="etat_attendu", **MX),
    _c("vt020 Craven Escape : apres la phase JOUEUR, le vilain attache est MELANGE dans le deck de vilains (degats effaces, l'autre vilain reste)",
       "« Forced Response: After the player phase ends, shuffle attached villain into the villain deck »",
       mechants_en_jeu("vt001", "vt007") + sous_le_vault("vt003") + ["Puzzle.Damage('vt001', 4)"],
       ["Puzzle.Reveal('vt020')", "Puzzle.EndPlayerPhase()"],
       {"tous": 1, "deck_de_mechants": 1, "en_jeu": ["vt007"], "hors_jeu": ["vt001", "vt020"]}, **MX),
    _c("vt020 Craven Escape : le DERNIER vilain en jeu est melange puis aussitot revele (deck de vilains), a PV pleins",
       "livret p.1 : « After the last villain leaves play, reveal the top card of the villain deck »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003") + ["Puzzle.Damage('vt001', 4)"],
       ["Puzzle.Reveal('vt020')", "Puzzle.EndPlayerPhase()"],
       {"tous": 1, "deck_de_mechants": 0, "en_jeu": ["vt001"], "degats": [["vt001", 0]], "hors_jeu": ["vt020"]}, **MX),

    # ============================================================ vt022 Corrupted Guardsman
    _c("vt022 Corrupted Guardsman : Inspection en jeu et un sbire sous le Vault -> il est REVELE (en jeu), pas de surge",
       "« If Inspection of the Vault is in play, reveal 1 random minion beneath The Vault »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003", "01103") + [INSPECTION, SURGE], ["Puzzle.Reveal('vt022')"],
       {"en_jeu": ["01103", "vt022"], "sous_vault_sbires": 0, "dans_deck_rencontre": ["01121"]}, **MX),
    _c("vt022 Corrupted Guardsman : Inspection NON en jeu -> il gagne SURGE (arbitrage du 25/10/2026), le sbire reste sous le Vault",
       "« If you cannot, this card gains surge » couvre aussi l'absence d'Inspection",
       mechants_en_jeu("vt001") + sous_le_vault("vt003", "01103") + [SURGE], ["Puzzle.Reveal('vt022')"],
       {"carte_du_surge": "01121", "sous_vault_sbires": 1}, **MX),
    _c("vt022 Corrupted Guardsman : Inspection en jeu mais AUCUN sbire sous le Vault -> SURGE",
       "« If you cannot, this card gains surge »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003") + [INSPECTION, SURGE], ["Puzzle.Reveal('vt022')"],
       {"carte_du_surge": "01121"}, **MX),
    _c("vt022 Corrupted Guardsman : Boost -> un sbire de sous le Vault est MELANGE dans le deck de rencontre",
       "« [star] Boost: Shuffle 1 minion beneath The Vault into the encounter deck »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003", "01103") + [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.CreateEncounterDeck('vt022')"],
       ["Puzzle.Attack('vt001')"],
       {"sous_vault_sbires": 0, "dans_deck_rencontre": ["01103"]}, avec_boost=True, **MX),

    # ============================================================ vt026 Burglary
    _c("vt026 Burglary : sans Inspection, menace de depart seule (2 pour 1 joueur)",
       "« StartingThreat 2[per_hero] » ; la menace additionnelle exige l'Inspection",
       mechants_en_jeu("vt001") + sous_le_vault("vt003"), ["Puzzle.Reveal('vt026')"], {"menace": [["vt026", 2]]}, **MX),
    _c("vt026 Burglary : Inspection en jeu -> 1[per_hero] menace EN PLUS (2 + 1 = 3)",
       "« When Revealed: If Inspection of the Vault is in play, place 1[per_hero] additional threat here »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003") + [INSPECTION], ["Puzzle.Reveal('vt026')"], {"menace": [["vt026", 3]]}, **MX),
    _c("vt026 Burglary : vaincue -> le dessus du deck de vilains est REVELE",
       "« When Defeated: Reveal the top card of the villain deck »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003") + ["Puzzle.BuildVillainDeck('vt005')", "Puzzle.Reveal('vt026')"],
       ["Puzzle.PlaceThreat('vt026', -2)"],
       {"tous": 2, "deck_de_mechants": 0, "en_jeu": ["vt005"]}, **MX),

    # ============================================================ vt028 Contingency Measures
    _c("vt028 Contingency Measures : un vilain qui serait vaincu est MELANGE dans le deck de vilains (pas vaincu), l'autre reste",
       "« Forced Interrupt: When a villain would be defeated, shuffle it into the villain deck instead »",
       mechants_en_jeu("vt001", "vt007") + sous_le_vault("vt003") + ["Puzzle.Reveal('vt028')"], ["Puzzle.Damage('vt001', 99)"],
       {"tous": 1, "deck_de_mechants": 1, "en_jeu": ["vt007"], "hors_jeu": ["vt001"], "fin": None}, **MX),
    _c("vt028 Contingency Measures : tant que l'Inspection est en jeu, la carte gagne une icone HAZARD",
       "« While Inspection of the Vault is in play, this card gains a hazard icon »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003") + [INSPECTION, "Puzzle.Reveal('vt028')"], [], {"hazard_de": [["vt028", 1]]}, **MX),
    _c("vt028 Contingency Measures : TEMOIN sans Inspection -> aucune icone Hazard",
       "contre-cas du precedent",
       mechants_en_jeu("vt001") + sous_le_vault("vt003") + ["Puzzle.Reveal('vt028')"], [], {"hazard_de": [["vt028", 0]]}, **MX),

    # ============================================================ vt029 Scheming from Within
    _c("vt029 Scheming from Within : 1 menace EN PLUS par vilain sous le Vault (2 + 2 = 4)",
       "« When Revealed: Place 1 additional threat here for each villain beneath The Vault »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003", "vt005", "01103"), ["Puzzle.Reveal('vt029')"], {"menace": [["vt029", 4]]}, **MX),
    _c("vt029 Scheming from Within : Boost avec Inspection -> +1 icone de boost par vilain sous le Vault (1 + 2 = 3)",
       "« [star] Boost: If Inspection of the Vault is in play, this card gets +1 boost icon for each villain beneath The Vault »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003", "vt005") + [INSPECTION, "Puzzle.PutIntoPlay('vt029')"], [], {"icones_boost": [["vt029", 3]]}, **MX),
    _c("vt029 Scheming from Within : TEMOIN sans Inspection -> 1 seule icone de boost",
       "contre-cas du precedent",
       mechants_en_jeu("vt001") + sous_le_vault("vt003", "vt005") + ["Puzzle.PutIntoPlay('vt029')"], [], {"icones_boost": [["vt029", 1]]}, **MX),

    # ============================================================ vt030 Rampage in Public
    _c("vt030 Rampage in Public : 1 vilain pour 1 joueur (pas moins) -> PAS de surge, le dessus du deck de vilains est revele",
       "« If the number of villains in play is less than the number of players, this card gains surge. Reveal the top card of the villain deck »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003") + ["Puzzle.BuildVillainDeck('vt005')", SURGE], ["Puzzle.Reveal('vt030')"],
       {"tous": 2, "deck_de_mechants": 0, "en_jeu": ["vt005"], "dans_deck_rencontre": ["01121"]}, **MX),
    _c("vt030 Rampage in Public : AUCUN vilain en jeu (0 < 1 joueur) -> SURGE, et le dessus du deck de vilains est revele",
       "meme texte : moins de vilains que de joueurs",
       mechants_en_jeu("vt001") + sous_le_vault("vt003") + [SURGE, "Puzzle.BuildVillainDeck('vt005')", "Puzzle.RemoveVillain('vt001')"],
       ["Puzzle.Reveal('vt030')"],
       {"tous": 1, "deck_de_mechants": 0, "carte_du_surge": "01121"}, **MX),
    _c("vt030 Rampage in Public : deck de vilains VIDE -> le vilain de plus GRAND Activation Order (Hydro-Man 4, ATK 2) active contre vous, pas Mentallo (2, ATK 1)",
       "« If you cannot, the villain with the highest activation order value activates against you »",
       mechants_en_jeu("vt003", "vt007") + sous_le_vault("vt005") + [HEROS, "Puzzle.Exhaust('01001a')"], ["Puzzle.Reveal('vt030')"],
       {"degats_joueurs": [2]}, **MX),

    # ============================================================ vt034 Riot in the Vault
    _c("vt034 Riot in the Vault : Inspection NON en jeu -> elle est REVELEE (donnee au 1er joueur), aucune menace",
       "« If Inspection of the Vault is not in play, reveal it »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003", "vt005") + ["Puzzle.CreateCard('vt019')"], ["Puzzle.Reveal('vt034')"],
       {"inspection_en_jeu": True, "menace": [["vt017b", 0]]}, **MX),
    _c("vt034 Riot in the Vault : Inspection DEJA en jeu -> 1 menace sur le complot par vilain sous le Vault (2)",
       "« Otherwise, place 1 threat on the main scheme for each Villain beneath The Vault »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003", "vt005") + [INSPECTION], ["Puzzle.Reveal('vt034')"],
       {"menace": [["vt017b", 2]]}, **MX),
    _c("vt034 Riot in the Vault : Surge (natif) -> le temoin du deck de rencontre est revele",
       "« Surge. »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003") + [SURGE], ["Puzzle.Reveal('vt034')"],
       {"carte_du_surge": "01121"}, **MX),
]
