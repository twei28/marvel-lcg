# Cas test_capacites du pack tmnt_shinobi_paths (Inkwire, TMNT Shinobi, les 11 PATHS, prefixe `se`), 17/10/2026.
# Filtre : `[se]`. Gabarits : .planning/tmnt/shinobi-paths-gabarits.md. Questions : .planning/tmnt/shinobi-socle-questions.md.
#
# Conventions :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros ;
#  - le Path est mis en jeu par `Puzzle.PutIntoPlay('seNNN', under_control=True)` (aire de soutien, type Path) ;
#    le chemin REEL « Path du deck -> mis de cote -> en jeu au Setup » a ses propres cas (`deck_ajoute`) ;
#  - Rhino 01094 (vilain du scenario `rhino`) est la cible des attaques, 01101 Hydra Mercenary le sbire ;
#  - `main_exclusive` vide la main (APRES la mise en place) : chaque cas sait avec QUOI il paie
#    (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR) ;
#  - deck rencontre bourre de « I'm Tough » (01105, sans icone de boost) : aucune carte rencontre ne vient
#    brouiller la mesure.
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
COMPLOT = "01097b"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]


def _voie(cid):
    return f"Puzzle.PutIntoPlay('{cid}', under_control=True)"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[se] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ===================================================================== se001 Kagemusha
    _c("se001 Kagemusha Shadow Stride : Hero Action, la Voie s'incline et le HEROS est camoufle (Cloaked)",
       "« Hero Action: Exhaust this card -> cloak your hero » : carte d'etat Cloaked sur le heros, Voie inclinee",
       [HEROS, _voie("se001")], ["Puzzle.Action('se001', 'HeroAction', 0)"],
       {"statuts": [["01001a", "Cloaked"]], "exhausted": ["se001"]}),
]
VERIFICATIONS = r'''
'''
