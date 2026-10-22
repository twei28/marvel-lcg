# Cas test_capacites du scenario 3 de Shadowland, « Heart of Shadow » (sl057-sl071, Krahllak), agent c. Prefixe de nom `[slc]`.
# Les cas tournent sur le scenario REEL `heart_of_shadow` (standard) ou `heart_of_shadow_expert` : la mise en place (sl060a) met une Creeping Corruption en jeu pour chaque joueur.
# ⚠ MONTAGE DE TEST MINIMAL : la Creeping Corruption sl072a/b appartient au set BLACK FLOWER (agent d, autre branche) ; elle n'a ICI aucun script (pas de retournement a 5 jetons, pas d'action).
#   Elle n'est qu'une carte portant des jetons `corruption`, mise en jeu par le Setup de sl060a. Le retournement / la defaite a 5 jetons ne sont PAS testes ici.
# Seed 42 : voir `Worlds.FindVillain` -> Krahllak (I) sl057 en standard, Krahllak (II) sl058 en expert.
HEROS = "spider_man"
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
# Deck de rencontre sans boost (3 x 01105) : les degats mesures sont ceux de l'ATQ imprimee, sans icone de boost ; l'identite est INCLINEE pour ne pas defendre.
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
INCLINEE = "Puzzle.Exhaust('01001a')"


def _h(nom, pourquoi, mise, declencher, attendu, forme_heros=True, scenario="heart_of_shadow", **cle):
    cas = {"nom": "[slc] " + nom, "pourquoi": pourquoi, "scenario": scenario, "heros": HEROS,
           "mise_en_place": [*([FORME_HEROS] if forme_heros else []), *mise], "declencher": declencher, "verifier": "slc_etat", "attendu": attendu,
           "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


CAS = [
    _h("sl057 attaque le joueur, il accepte : 1 jeton pose, ATQ 3 - 3 = 0 degat", "« you may place 1 corruption counter ... If you do, Krahllak gets -3 ATK for this attack »",
       [*RIEN, INCLINEE], ["Puzzle.EnemyAttacks('sl057', '01001a')"], {"corruption": [1], "degats_identite": 0}),
    _h("sl057 attaque le joueur, il REFUSE : aucun jeton, 3 degats", "« you MAY » : facultatif",
       [*RIEN, INCLINEE], ["Puzzle.EnemyAttacks('sl057', '01001a')"], {"corruption": [0], "degats_identite": 3}, choisir_option="Cancel"),
    _h("sl060a Setup : chaque joueur a SA Creeping Corruption en jeu (solo : 1)", "« Each player puts a Creeping Corruption upgrade into play »",
       [], [], {"corruption": [0]}, forme_heros=False),
    _h("sl060a Setup a DEUX joueurs : chacun a sa Creeping Corruption (2 cartes distinctes), les deux autres exemplaires restent de cote", "UNE par joueur, pas deux pour le premier",
       [], [], {"corruption": [0, 0], "cc_en_jeu": 2, "cc_de_cote": 2}, forme_heros=False, heros2="spider_man", main_exclusive=["01088", "01089"]),
]


VERIFICATIONS = r'''
def slc_etat(monde, aides):
    """etat_attendu + cles propres au scenario Heart of Shadow :
    `corruption` : [n par joueur] = jetons `corruption` sur la Creeping Corruption de chaque joueur (dans l'ordre des joueurs) ;
    `cc_en_jeu` / `cc_de_cote` : nombre de Creeping Corruption en jeu / mises de cote."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    ids_cc = ("sl072a", "sl072b")
    en_jeu = []
    for objet in monde.object_manager.card_dict.values():
        face = getattr(objet, "face", None)
        if face is not None and face.IsInPlay() and str(getattr(face.paper, "card_id", "")) in ids_cc:
            en_jeu.append(face)
    if "cc_en_jeu" in attendu and len(en_jeu) != attendu["cc_en_jeu"]:
        soucis.append(f"{len(en_jeu)} Creeping Corruption en jeu (attendu {attendu['cc_en_jeu']})")
    if "cc_de_cote" in attendu:
        cote = [f for f in monde.aside_deck.Get(True) if str(f.paper.card_id) in ids_cc]
        if len(cote) != attendu["cc_de_cote"]:
            soucis.append(f"{len(cote)} Creeping Corruption de cote (attendu {attendu['cc_de_cote']})")
    if "corruption" in attendu:
        vus = []
        for joueur in monde.const_players:
            cc = [f for f in en_jeu if f.card.GetOwner() == joueur]
            vus.append(cc[0].GetCounters("corruption") if len(cc) == 1 else f"{len(cc)} cartes")
        if vus != attendu["corruption"]:
            soucis.append(f"jetons corruption par joueur {vus} (attendu {attendu['corruption']})")
    reste = {k: v for k, v in attendu.items() if k not in ("corruption", "cc_en_jeu", "cc_de_cote")}
    cas["attendu"] = reste
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = attendu
    if not ok:
        soucis.append(msg)
    return (False, " ; ".join(soucis)) if soucis else (True, "etat conforme")
'''
