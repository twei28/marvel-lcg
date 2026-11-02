# Cas test_capacites de * Magneto (32172b, campagne Mutant Genesis) : ticket #107 du 02/11/2026, « Magneto ne s'est pas soigne
# apres avoir vaincu une sentinelle ». Noms commencant par le card_id (filtre de tools/test_capacites.py).
#
# Montage : Magneto (ATQ 3*, degat consequent 1) attaque une Sentinel Mark III (32102, 3 PV, trait SENTINEL). Le degat consequent
# est pris APRES l'attaque (ally.py, Consequential) : la Reponse « heal 1 damage from Magneto » doit donc le rattraper.
# ⚠ La Sentinelle arrive avec un statut Tough (Toughness 1) : l'attaque ne ferait que l'ecarter. `Puzzle.Tough` (bascule) le retire,
# comme l'attaque de l'identite dans le ticket (premier faux echec de ce cas : la Sentinelle survivait, aucune Reponse).
CAS = [
    {
        "nom": "32172b Magneto — apres avoir vaincu une Sentinelle, il se soigne du degat consequent de son attaque",
        "pourquoi": ("ticket #107 (journal) : Magneto 5/5 vainc la Sentinel Mark III, prend 1 degat consequent, finit a 4 PV sans soin. "
                     "La Reponse partait AVANT le degat, donc sur une cible non blessee (`canbe_heal`) : rien a soigner. "
                     "Attendu : il finit a 0 degat"),
        "scenario": "rhino",
        "heros": "spider_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('32172b', under_control=True)",
                          "Puzzle.PutIntoPlay('32102')",
                          "Puzzle.Tough('32102')"],
        "declencher": ["Puzzle.Attack('32172b', '32102')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["32172b", 0]]},
    },
    {
        "nom": "32172b Magneto — temoin : sans ennemi vaincu (Rhino), il garde son degat consequent",
        "pourquoi": ("temoin d'absence d'effet : Rhino a trop de PV pour mourir, aucune Reponse, Magneto reste a 1 degat. "
                     "Prouve que le cas precedent mesure bien le soin et non une absence de degat consequent"),
        "scenario": "rhino",
        "heros": "spider_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('32172b', under_control=True)"],
        "declencher": ["Puzzle.Attack('32172b', '01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["32172b", 1]]},
    },
]
