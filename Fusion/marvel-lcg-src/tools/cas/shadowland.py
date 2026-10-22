# Cas test_capacites du pack SHADOWLAND (MC65, prefixe `sl`). Prefixe de nom `[sl]`. Rien n'est teste sur un scenario Shadowland
# tant que celui-ci n'existe pas : on monte la position a la main sur `rhino` (Spider-Man, Whirlwind 01130 en mise en place).
HEROS = "spider_man"
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
FORME_HEROS = "Puzzle.ChangeForm('01001b')"


def _s(nom, pourquoi, mise, declencher, attendu, **cle):
    avant = cle.pop("avant_forme", [])   # ⚠ PIEGE : `ChangeForm` remet la menace du complot a 0 -> poser la menace AVANT
    cas = {"nom": "[sl] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": HEROS, "mise_en_place": [*RIEN, *avant, FORME_HEROS, *mise],
           "declencher": declencher, "verifier": "etat_attendu", "attendu": attendu, "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


def _pos(v, h):
    return [f"Puzzle.PutIntoPlay('sl003{v}')", f"Puzzle.PutIntoPlay('sl004{h}')"]


CAS = [
    # ------------------------------------------------------------------------------------------------------ sl003 : positions du vilain / du heros
    _s("sl003a/sl004a : positions identiques (Streets/Streets) -> chaque personnage a +1 ATK : l'attaque de base inflige 3", "« If both positions are the same: each character gets +1 ATK » (ATK 2 + 1)",
       [*_pos("a", "a"), "Puzzle.PutIntoPlay('01130')"], ["Puzzle.Attack('01001a')"], {"degats": [["01130", 3]]}, cibles=["01130"]),
    _s("sl003b/sl004b : positions identiques (Tenshu/Tenshu) -> +1 ATK aussi (meme texte sur la face b)", "les deux faces de sl003 portent le meme effet",
       [*_pos("b", "b"), "Puzzle.PutIntoPlay('01130')"], ["Puzzle.Attack('01001a')"], {"degats": [["01130", 3]]}, cibles=["01130"]),
    _s("sl003, TEMOIN : sans carte de position, l'attaque de base inflige 2", "la regle seule ajoute le degat",
       ["Puzzle.PutIntoPlay('01130')"], ["Puzzle.Attack('01001a')"], {"degats": [["01130", 2]]}, cibles=["01130"]),
    _s("sl003a/sl004b : positions differentes -> chaque personnage subit 1 degat de moins par attaque : 2 - 1 = 1", "« Reduce the amount of damage each character takes from each attack by 1 »",
       [*_pos("a", "b"), "Puzzle.PutIntoPlay('01130')"], ["Puzzle.Attack('01001a')"], {"degats": [["01130", 1]]}, cibles=["01130"]),
    _s("sl003b/sl004a : positions differentes (l'autre sens) -> 1 degat de moins aussi", "la regle ne depend pas de la face exacte",
       [*_pos("b", "a"), "Puzzle.PutIntoPlay('01130')"], ["Puzzle.Attack('01001a')"], {"degats": [["01130", 1]]}, cibles=["01130"]),
    _s("sl003a/sl004b : positions differentes -> la menace ne peut pas etre retiree du complot principal", "« Threat cannot be removed from the main scheme »",
       [*_pos("a", "b"), "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01075')"], {"menace": [["01097b", 5]]}, avant_forme=["Puzzle.SetThreat('01097b', 5)"]),
    _s("sl003a/sl004a : positions identiques -> la menace se retire normalement (temoin)", "le blocage ne vaut que si les positions different",
       [*_pos("a", "a"), "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01075')"], {"menace": [["01097b", 3]]}, avant_forme=["Puzzle.SetThreat('01097b', 5)"]),
]
