# Cas test_capacites du pack SHADOWLAND (MC65, prefixe `sl`). Prefixe de nom `[sl]`. Rien n'est teste sur un scenario Shadowland
# tant que celui-ci n'existe pas : on monte la position a la main sur `rhino` (Spider-Man, Whirlwind 01130 en mise en place).
HEROS = "spider_man"
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
FORME_HEROS = "Puzzle.ChangeForm('01001b')"


def _s(nom, pourquoi, mise, declencher, attendu, **cle):
    avant = cle.pop("avant_forme", [])   # ⚠ PIEGE : `ChangeForm` remet la menace du complot a 0 -> poser la menace AVANT
    cas = {"nom": "[sl] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": HEROS, "mise_en_place": [*RIEN, *avant, FORME_HEROS, *mise],
           "declencher": declencher, "verifier": "sl_etat", "attendu": attendu, "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


def _pos(v, h):
    # une carte recto-verso se cree par PAIRE « visible,verso » (comme les complots « 56141a,56141b ») : sans le verso, Flip() ne fait rien
    autre = {"a": "b", "b": "a"}
    return [f"Puzzle.PutIntoPlay('sl003{v},sl003{autre[v]}')", f"Puzzle.PutIntoPlay('sl004{h},sl004{autre[h]}')"]


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
    # ------------------------------------------------------------------------------------------------------ sl004 : position du heros (First Player Action)
    _s("sl004a, branche 1 : 3 menaces sur le complot et identite etourdie, puis la carte se retourne (sl004b)", "« Resolve one of the effects below, then flip this card »",
       [*_pos("a", "a")], ["Puzzle.Action('sl004a', 'FirstPlayerAction')"], {"menace": [["01097b", 5]], "statuts": [["01001a", "Stunned"]], "face_visible": [["sl004", "sl004b"]]},
       choisir_option="Place_3_threat_on_the_main_scheme_and_stun_your_identity", avant_forme=["Puzzle.SetThreat('01097b', 2)"]),
    _s("sl004b, branche 1 : 3 degats a l'identite, puis la carte se retourne (sl004a)", "face b : « Deal 3 damage to your identity »",
       [*_pos("a", "b")], ["Puzzle.Action('sl004b', 'FirstPlayerAction')"], {"degats_identite": 3, "face_visible": [["sl004", "sl004a"]]},
       choisir_option="Deal_3_damage_to_your_identity"),
    _s("sl004a, branche 2 : depenser [physical][physical] (Strength) puis la carte se retourne", "« Spend [physical][physical] resources »",
       [*_pos("a", "a")], ["Puzzle.Action('sl004a', 'FirstPlayerAction')"], {"face_visible": [["sl004", "sl004b"]], "defausse": ["01090"], "menace": [["01097b", 2]]},
       preferer_option="Spend", payer_avec=["01090"], main_exclusive=["01090"], avant_forme=["Puzzle.SetThreat('01097b', 2)"]),
    _s("sl004a, branche 3 : 1 ressource et epuiser un AERIAL (Falcon) puis la carte se retourne", "« Spend 1 resource of any type and exhaust an AERIAL character you control »",
       [*_pos("a", "a"), "Puzzle.PutIntoPlay('03011', under_control=True)"], ["Puzzle.Action('sl004a', 'FirstPlayerAction')"],
       {"face_visible": [["sl004", "sl004b"]], "exhausted": ["03011"], "statuts_absents": [["01001a", "Stunned"]]}, preferer_option="AERIAL", payer_avec=["01088"], main_exclusive=["01088"], avant_forme=["Puzzle.SetThreat('01097b', 2)"]),
    _s("sl004b, branche 2 : depenser [energy][energy] (Energy) puis la carte se retourne", "« Spend [energy][energy] resources »",
       [*_pos("a", "b")], ["Puzzle.Action('sl004b', 'FirstPlayerAction')"], {"face_visible": [["sl004", "sl004a"]], "defausse": ["01088"], "degats_identite": 0},
       preferer_option="Spend", payer_avec=["01088"], main_exclusive=["01088"]),
    _s("sl004b, branche 3 : defausser un allie que vous controlez puis la carte se retourne", "« Discard an ally or upgrade you control »",
       [*_pos("a", "b"), "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Action('sl004b', 'FirstPlayerAction')"],
       {"face_visible": [["sl004", "sl004a"]], "defausse": ["01075"], "degats_identite": 0}, preferer_option="Discard"),
    _s("sl004a, branche 2, TEMOIN : [physical][physical] impayable (Genius = BB) -> la branche n'est PAS offerte, le pilote retombe sur la branche 1 (menace +3)", "le moteur reduit un choix payant impayable au plus gros morceau payable : on ne l'offre donc que si payable",
       [*_pos("a", "a")], ["Puzzle.Action('sl004a', 'FirstPlayerAction')"], {"face_visible": [["sl004", "sl004b"]], "en_main": ["01089"], "menace": [["01097b", 5]]},
       preferer_option="Spend", main_exclusive=["01089"], avant_forme=["Puzzle.SetThreat('01097b', 2)"]),
]


VERIFICATIONS = r'''
def sl_etat(monde, aides):
    """etat_attendu + `face_visible` : [[prefixe, card_id attendu]] = la face MONTREE de la carte (les deux faces d'une carte partagent un prefixe)."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    for prefixe, voulu in attendu.get("face_visible") or []:
        vues = []
        for objet in monde.object_manager.card_dict.values():
            face = getattr(objet, "face", None)
            cid = str(getattr(getattr(face, "paper", None), "card_id", ""))
            if cid.startswith(prefixe) and cid not in vues:
                vues.append(cid)
        if vues != [voulu]:
            soucis.append(f"faces montrees pour {prefixe} : {vues} (attendu {voulu})")
    reste = {k: v for k, v in attendu.items() if k != "face_visible"}
    cas["attendu"] = reste
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = attendu
    if not ok:
        soucis.append(msg)
    return (False, " ; ".join(soucis)) if soucis else (True, "etat conforme")
'''
