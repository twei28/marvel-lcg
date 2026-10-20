# Cas test_capacites de gs165 Threat on the Horizon (Earth Under Siege, lot GS-7). Filtre `[eus] gs165`.
#
# Utilise la VRAIE mise en place du scenario ("scenario": SC) : "rhino" porte deja sa propre manigance
# principale (The Break-In!), et Worlds.FindMainScheme y trouverait le mauvais complot (constate le
# 20/10/2026, cas en echec silencieux : les compteurs de securite etaient poses sur gs161b mais retires
# du mauvais complot). Earthfall doit etre LA manigance principale reelle de la partie.

SC = "gs_earth_under_siege"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[eus] gs165 " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    _c("choix : depenser 2 ressources (le pilote accepte la premiere option proposee) -> securite inchangee",
       "« Choose to either spend 2 resources of any type or remove 1 safety counter » : ChooseAbilities, "
       "option « Spend 2 resources » prioritaire par le pilote",
       [], ["Puzzle.Reveal('gs165')"],
       {"compteurs": [["gs161b", "safety", 6]]}),
    _c("aucune ressource disponible : seule l'option securite reste -> 1 compteur de securite retire",
       "sans ressource couvrable, seule l'option securite est proposee (ChooseAbilities avec 1 seul choix)",
       ["Puzzle.EmptyHand()"], ["Puzzle.Reveal('gs165')"],
       {"compteurs": [["gs161b", "safety", 5]]}),
]
