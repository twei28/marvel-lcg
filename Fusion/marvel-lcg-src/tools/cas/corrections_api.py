# Cas ajoutes le 26/10/2026 avec la passe « verifier_api_cartes » (cartes hors de nos packs de heros) : noms prefixes « [api] » puis le card_id.
#
# su018 Goblin Glider : « Attach to the enemy with the HIGHEST PRINTED hit points ». `choisir_le_plus_gros` etait defini mais jamais
# passe a la fabrique : le joueur pouvait l'attacher a N'IMPORTE QUEL ennemi sans carte a PV imprimes plus hauts. Le cas historique (Rhino
# 14 PV imprimes contre Hobgoblin 6) passait quand meme, parce que le pilote prend d'abord Rhino, qui est AUSSI le plus gros : il faut un
# montage ou le plus gros est un SBIRE (Moonstone 50139, 16 PV imprimes) et ou le vilain (Rhino, 14) n'est pas le plus gros.
SC = "rhino"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[api] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "superior_spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": "etat_attendu", "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    _c("su018 Goblin Glider : le plus gros n'est PAS le vilain (Moonstone 16 PV imprimes > Rhino 14) -> il s'attache au sbire",
       "« Attach to the enemy with the highest printed hit points » : le choix n'est pas libre, c'est l'ennemi aux PV imprimes les plus hauts",
       ["Puzzle.ChangeToFace('su001b', 'su001a')", "Puzzle.PutIntoPlay('50139')", "Puzzle.CreateEncounterDeck('01107')"],
       ["Puzzle.Reveal('su018')"], {"hotes": [["su018", "50139"]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("su018 Goblin Glider : TEMOIN, le vilain est le plus gros (Rhino 14 > Hobgoblin 6) -> il s'attache a Rhino",
       "meme texte, montage de l'ancien cas : Rhino reste la cible quand il a les PV imprimes les plus hauts",
       ["Puzzle.ChangeToFace('su001b', 'su001a')", "Puzzle.PutIntoPlay('su016')", "Puzzle.CreateEncounterDeck('01107')"],
       ["Puzzle.Reveal('su018')"], {"hotes": [["su018", "01094"]]}, main_exclusive=["01090"], accepter_choix=True),
    # pu090a Justice or Punishment? : « Set their hit points to the numeral (ignoring the per-player icon) in their printed hit point value ».
    # Jigsaw I (pu056a) imprime « 14* » : `printed_health` vaut 14 x joueurs (28 a deux), `printed_health_numeral` vaut 14. Le code lisait
    # `printed_health` : a deux heros Jigsaw avait 28 + 5 x 2 = 38 PV au lieu de 14 + 10 = 24. Un seul heros ne distingue pas les deux (14).
    _c("pu090a Justice or Punishment? : A DEUX heros, les PV de Jigsaw = le NOMBRE imprime (14) + 5 par heros = 24 (pas 28 + 10 = 38)",
       "« Set their hit points to the numeral (ignoring the per-player icon) » puis In the Crosshairs « +5[per hero] hit points »",
       ["Puzzle.ChangeForm('01001b')"], [], {"pv_max": [["pu056a", 24]]},
       scenario="one_last_kill_jigsaw", heros="spider_man", heros2="spider_man", main_exclusive=["01088"]),

    # ---- Wild IMPRIME (arbitrage du 26/10/2026, fiche mots-cles/wild-resource.md) : une ressource wild imprimee sur une carte n'est QUE
    # « wild » : ni [physical] ni [mental]. bw010 / bw011 Shockwave et bw025 Brains and Brawn comptaient `icones.r + icones.g` et
    # `icones.b + icones.g` : chaque wild frappait ET retirait de la menace. 01020 Hellcat porte une ressource wild (RES G), 01090 Strength RR.
    _c("bw010 Shockwave : un deck de cartes WILD seulement -> ni degats aux ennemis ni menace retiree (un wild imprime n'est ni [physical] ni [mental])",
       "« For each [physical] resource discarded this way... For each [mental] resource discarded this way » : le wild imprime n'a que « wild »",
       ["Puzzle.ChangeForm('bw001b')", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01020', '01020', '01020', '01020', '01020')",
        "Puzzle.SetThreat('01097b', 5)"],
       [], {"wild_defaussees_min": 1, "degats_de": [["01094", 0]], "menace_de": [["01097b", 5]]},
       heros="brawn", verifier="api_wild_imprime", main_exclusive=["bw010", "01090"], jouer=["bw010"], surpayer=True),
    _c("bw011 Shockwave (2e exemplaire) : un deck de cartes WILD seulement -> ni degats ni menace retiree",
       "meme texte que bw010 : le script est le meme, le 2e exemplaire est mesure aussi",
       ["Puzzle.ChangeForm('bw001b')", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01020', '01020', '01020', '01020', '01020')",
        "Puzzle.SetThreat('01097b', 5)"],
       [], {"wild_defaussees_min": 1, "degats_de": [["01094", 0]], "menace_de": [["01097b", 5]]},
       heros="brawn", verifier="api_wild_imprime", main_exclusive=["bw011", "01090"], jouer=["bw011"], surpayer=True),
    _c("bw025 Brains and Brawn : main [bw025, Strength RR, Hellcat WILD] -> AUCUNE menace retiree (le wild n'est pas [mental] : 5 -> 5)",
       "« For each printed resource in your hand and reserve, if it is a [physical] - Deal 1 damage to an enemy. [mental] - Remove 1 threat from a scheme » : "
       "1 menace retiree avec l'ancien code (5 -> 4, le wild comptait comme [mental]). Les DEGATS ne sont pas mesures : la selection de la cible "
       "(AskChooseFace repetee) n'est pas deterministe dans le banc (0, 1 ou 3 selon le montage)",
       ["Puzzle.ChangeForm('bw001b')", "Puzzle.PutIntoPlay('bw003', under_control=True)", "Puzzle.SetThreat('01097b', 5)"],
       [], {"wild_defaussees_min": 0, "menace_de": [["01097b", 5]]},
       heros="brawn", verifier="api_wild_imprime", main_exclusive=["bw025", "01090", "01020"], jouer=["bw025"], accepter_choix=True),
]


VERIFICATIONS = r'''
def api_wild_imprime(monde, aides):
    """Cles de `attendu` : `wild_defaussees_min` (combien de Hellcat 01020 au moins en defausse : prouve que Shockwave a bien defausse),
    `degats_de` ([[card_id, n]] : degats subis), `menace_de` ([[card_id, n]] : menace posee)."""
    attendu = aides["cas"]["attendu"]
    soucis = []
    joueur = monde.players[0]
    ids = [getattr(f.paper, "card_id", None) for f in joueur.discard_pile.Get()]
    voulu = attendu.get("wild_defaussees_min", 0)
    if ids.count("01020") < voulu:
        soucis.append(f"{ids.count('01020')} Hellcat en defausse (attendu >= {voulu}) : rien n'a ete defausse, le cas ne prouve rien (defausse = {ids})")
    for card_id, n in attendu.get("degats_de") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable")
        elif face.max_health - face.health != n:
            soucis.append(f"{card_id} a subi {face.max_health - face.health} degat(s) (attendu {n})")
    for card_id, n in attendu.get("menace_de") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable")
        elif face.threat != n:
            soucis.append(f"{card_id} a {face.threat} menace(s) (attendu {n})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''
