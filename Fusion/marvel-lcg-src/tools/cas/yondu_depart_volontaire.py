# Cas du CORRECTIF du 23/11/2026 (rapport de bug n°164, Yondu / Sifflez en Travaillant) : noms prefixes « [yd164] ».
# La fleche Yaka (yd012) est attachee a un sbire a 1 PV. Quand le JOUEUR la deplace (yd004 -> sur Yondu), le degat de
# depart de yd001a achevait le sbire ALORS QUE la fleche lui etait encore attachee : l'interruption forcee de yd012
# (« quand l'ennemi auquel elle est attachee devrait etre vaincu ») ouvrait un choix inutile (ennemi / identite / main).
# Le pilote du harnais prend la PREMIERE branche (« Attach ... to an enemy ») : sans le correctif la fleche partait sur
# l'autre sbire (01101) au lieu d'arriver sur Yondu. Avec : aucun choix, fleche sur yd001a, sbire mort.
# Rouge sans le drapeau `depart_volontaire` (yondu/__init__.py + yd012.py), vert avec.
# Temoin : sans le correctif, la fleche fait un DETOUR par Rhino (choix pris par le pilote) puis finit quand meme sur Yondu :
# seuls les 2 degats infliges a Rhino (arrivee + depart) revelent le bug, d ou `degats` Rhino = 0.
# ⚠ Le sbire est 01110 (Hydra Bomber, 2 PV) : 01101 a plus de PV et ne meurt pas du seul degat de depart.
CAS = [
    {
        "nom": "[yd164] yd004 Sifflez en Travaillant : la fleche quitte un sbire a 1 PV -> arrive sur Yondu, sans choix",
        "pourquoi": ("le depart est VOULU par le joueur : la fleche n'est plus attachee a l'ennemi qui tombe, "
                     "l'interruption forcee de yd012 ne doit pas se declencher. Temoin : un SECOND sbire (01101) "
                     "en jeu, cible de la premiere branche du choix qui s'ouvrait a tort"),
        "scenario": "rhino",
        "heros": "yondu",
        "mise_en_place": ["Puzzle.ChangeToFace('yd001b', 'yd001a')",
                          "Puzzle.PutIntoPlay('01110')",
                          "Puzzle.PutIntoPlay('01101')",
                          "Puzzle.AttachReel('yd012', '01110')",
                          "Puzzle.SetHealth('01110', 1)"],
        "main_exclusive": ["yd004", "01088"],
        "declencher": [],
        "jouer": ["yd004"],
        "verifier": "yd_attachements",
        "attendu": {"fleche_sur": "yd001a", "en_jeu": ["01101"], "defausse_rencontre": ["01110"],
                    "degats": [["01094", 0]]},
    },
]
