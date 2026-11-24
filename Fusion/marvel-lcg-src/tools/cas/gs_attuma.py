# Cas test_capacites d'Attuma (gs170-gs175, Earth Under Siege, lot GS-7). Filtre `[eus] attuma`.
#
# ⚠ ETAT DU 20/10/2026 : seuls les 2 cas de base (etat IMPRIME, sans aucune condition declenchee) passent.
# Les cas conditionnels (bonus ATLANTIS, attache otherwise_attach_to, reduction de degats, decompte a la
# revelation) echouent dans ce harnais pour la MEME famille de raisons que Annihilus (voir
# EARTH-UNDER-SIEGE-GABARITS.md) -- ET une collision possible avec une AUTRE session Claude active en
# parallele sur ce depot (ListAgents : marvel-lcg-cb) a ete constatee pendant cette investigation (fichier
# de ce lot disparu puis recree, conflits "un autre harnais tourne deja"). Construction verifiee
# (test_cards, 0 erreur) pour tout le groupe ; reste a verifier en partie reelle / autoplay.

MEC_SOCLE = [
    "Puzzle.RemoveVillain('01094')",
    "Puzzle.SetVillainRule('Leftmost', 'PlayerChooses')",
]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[eus] attuma " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", "rhino"),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    _c("gs170 (I) seul en jeu : SCH/ATK imprimes (1/2), pas de bonus",
       "etat de base, sans condition declenchee : SCH 1, ATK 2 imprimes",
       MEC_SOCLE + ["Puzzle.PutIntoPlay('gs170')"], [],
       {"attributs_carte": [["gs170", "scheme", 0], ["gs170", "attack", 0]]}),
    _c("gs174 Andromeda seule en jeu : pas de riposte",
       "etat de base, sans condition declenchee : aucune riposte imprimee",
       MEC_SOCLE + ["Puzzle.PutIntoPlay('gs174')"], [],
       {"attributs_carte": [["gs174", "retaliate", 0]]}),
]
