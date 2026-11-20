# Cas test_capacites du heros custom SHANG-CHI (DesignHacker, SEALED, prefixe `ch`) :
# noms prefixes « [ch] » puis le card_id (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - Shang-Chi demarre en ALTER EGO (ch001b) ; `Puzzle.ChangeToFace('ch001b', 'ch001a')` la passe en forme HEROS ;
#  - State of Flow (ch002, Permanent. Setup.) est mis de cote et entre en jeu au Setup (ch001b) ; on le pose sinon par
#    `Puzzle.PutIntoPlay('ch002', under_control=True)` ;
#  - la pile se garnit par `Puzzle.PlaceUnder('<attaque>', 'ch002', face_up=True)` (la DERNIERE posee est le dessus) ;
#  - `player_deck` est VIDE dans le deck de depart : le harnais le complete avec des ressources inertes,
#    `main_exclusive` fixe la main ;
#  - Rhino 01094 est le vilain, 01097b son complot principal, 01101 Hydra Mercenary un sbire ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ;
#  - icones imprimees : ch003 R+B, ch004 B, ch005 Y, ch006 R+Y, ch007 G, ch008 B, ch009 G, ch010 Y, ch011 G,
#    ch012 R, ch013 Y+B, ch014 R.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('ch001b', 'ch001a')"
CIVIL = "Puzzle.ChangeToFace('ch001a', 'ch001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
VIDER_DEFAUSSE = "Puzzle.EmptyPlayerDiscardPile()"
COMPLOT = "01097b"
VILAIN = "01094"
PILE = "ch002"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def empiler(*ids):
    """Pose ces attaques sur State of Flow, la derniere = le dessus."""
    return [f"Puzzle.PlaceUnder('{i}', '{PILE}', face_up=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[ch] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "shang_chi"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


DECK5 = [SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089')"]
MERC = "01103"      # Shocker, 3 PV, sans Guard (Hydra Mercenary a GUARD : il rend le vilain intouchable)
SANDMAN = "01182"   # Hydra Soldier, 4 PV, GUARD (cible d'un « minion » qui ne doit pas attaquer ; Sandman entre en jeu avec Tough, Vulture attaque a l'engagement)
RUNNER = "01121"    # Weapons Runner, 2 PV, sans Guard
WHIP = "01184"      # M.O.D.O.K., 8 PV, riposte 2

CAS = [
    # ============================================================ ch001a Shang-Chi : Chi Mastery
    _c("ch001a Chi Mastery : apres un Flow resolu, Shang-Chi se redresse (Roundhouse Kick, dessus = Chi Jabs physique)",
       "« Response: After you resolve a Flow ability, ready Shang-Chi »",
       [HEROS, "Puzzle.Exhaust('ch001a')", *en_jeu(PILE), *empiler("ch012")], [],
       {"pret": ["ch001a"], "degats": [[VILAIN, 3]]},
       main_exclusive=["ch005"], jouer=["ch005"], cibles=[VILAIN, VILAIN]),
    _c("ch001a Chi Mastery : AUCUN Flow resolu (pile vide) -> Shang-Chi reste incline",
       "contre-cas : sans Flow, la Response ne part pas",
       [HEROS, "Puzzle.Exhaust('ch001a')", *en_jeu(PILE)], [],
       {"exhausted": ["ch001a"], "degats": [[VILAIN, 1]]},
       main_exclusive=["ch005"], jouer=["ch005"], cibles=[VILAIN]),
    _c("ch001a Chi Mastery : le Flow est REFUSE (le joueur ne veut pas le resoudre) -> Shang-Chi reste incline, pas de 2 degats",
       "« you MAY also resolve its effects » : refuser = pas de resolution, donc pas de Response",
       [HEROS, "Puzzle.Exhaust('ch001a')", *en_jeu(PILE), *empiler("ch012")], [],
       {"exhausted": ["ch001a"], "degats": [[VILAIN, 1]]},
       main_exclusive=["ch005"], jouer=["ch005"], cibles=[VILAIN, VILAIN], choisir_option="Cancel"),
    _c("ch001a Shang-Chi : valeurs imprimees PV 9, THW/ATK/DEF 1, AVENGER MARTIAL ARTIST",
       "nombres texte <-> code (scan HERO) : HAND SIZE 5 / HIT POINTS 9",
       [HEROS], [], {"pv_max": [["ch001a", 9]], "traits": ["AVENGER", "MARTIAL ARTIST"]}, main_exclusive=["01090"]),
    # ============================================================ ch001b Shang-Chi : Meditate, Setup
    _c("ch001b Meditate : apres le changement de forme vers l'alter-ego, une carte AU CHOIX de la pile retourne dans le deck",
       "« Response: After you change to this form, shuffle a card from State of Flow into your deck » (decision du 24/10 : au choix)",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089')", *en_jeu(PILE), *empiler("ch011", "ch005")],
       ["Puzzle.ChangeToFace('ch001a', 'ch001b')"],
       {"taille_deck_joueur": 3, "forme": "AlterEgo"}, main_exclusive=["01090"], cibles=["ch011"]),
    _c("ch001b Meditate : la pile perd la carte choisie et garde l'autre",
       "une seule carte quitte la pile, pas toute la pile ; la carte choisie (Chi Jabs) est dans le deck",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089')", *en_jeu(PILE), *empiler("ch011", "ch005")],
       ["Puzzle.ChangeToFace('ch001a', 'ch001b')"],
       {"pose_sous": [[PILE, "ch005"]], "dans_deck_joueur": ["ch011"]}, main_exclusive=["01090"], cibles=["ch011"]),
    _c("ch001b Meditate : pile vide -> rien ne se passe, le deck ne grossit pas",
       "contre-cas : « shuffle a card from State of Flow » sans carte",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089')", *en_jeu(PILE)],
       ["Puzzle.ChangeToFace('ch001a', 'ch001b')"],
       {"taille_deck_joueur": 2, "forme": "AlterEgo"}, main_exclusive=["01090"]),
    _c("ch001b Meditate : absente quand on passe a la forme HEROS (la Response est imprimee sur l'alter-ego)",
       "« After you change to THIS form » : seul le retour en alter-ego la declenche",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089')", *en_jeu(PILE), *empiler("ch011")],
       ["Puzzle.ChangeToFace('ch001b', 'ch001a')"],
       {"taille_deck_joueur": 2, "pose_sous": [[PILE, "ch011"]], "forme": "Hero"}, main_exclusive=["01090"]),
    _c("ch001b Shang-Chi : valeurs imprimees PV 9, MARTIAL ARTIST",
       "nombres texte <-> code (scan ALTER-EGO) : HAND SIZE 6 / HIT POINTS 9 / REC 4",
       [], [], {"pv_max": [["ch001b", 9]], "traits": ["MARTIAL ARTIST"]}, main_exclusive=["01090"]),
    # ============================================================ ch002 State of Flow
    _c("ch002 State of Flow : une attaque jouee (Chi Jabs) se pose face visible sur la pile et quitte la defausse",
       "« Forced Response: After you play an ATTACK event, place it faceup on top here »",
       [HEROS, *en_jeu(PILE)], [],
       {"pose_sous": [[PILE, "ch012"]], "degats": [[VILAIN, 1]]},
       main_exclusive=["ch012", "01090"], jouer=["ch012"], payer_avec=["01090"], cibles=[VILAIN]),
    _c("ch002 State of Flow : deux attaques de suite, la DERNIERE est le dessus (le Flow de la 3e lit celle-la)",
       "« place it faceup on TOP here » : ordre de la pile",
       [HEROS, *en_jeu(PILE)], [],
       {"pose_sous": [[PILE, "ch005"], [PILE, "ch003"]], "dessus_pile": "ch003"},
       main_exclusive=["ch005", "ch003"], jouer=["ch005", "ch003"], cibles=[VILAIN, VILAIN],
       verifier="pile_flow"),
    _c("ch002 State of Flow : un evenement qui n'est PAS une attaque (For Justice!) reste a la defausse",
       "« After you play an ATTACK event » : trait ATTACK exige",
       [HEROS, *en_jeu(PILE), f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"pile_vide": True, "defausse": ["01060"], "menace": [[COMPLOT, 2]]},
       main_exclusive=["01060", "01090"], jouer=["01060"], payer_avec=["01090"], cibles=[COMPLOT], verifier="pile_flow"),
    _c("ch002 State of Flow : deck vide apres une pioche -> toute la pile retourne dans le deck du joueur",
       "« After the player deck runs out, shuffle each card placed here back into the player deck »",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089')", *en_jeu(PILE), *empiler("ch005", "ch011")],
       [VIDER_DEFAUSSE, "Puzzle.Draw(1)"],
       {"pile_vide": True, "taille_deck_joueur": 2, "dans_deck_joueur": ["ch005", "ch011"]}, main_exclusive=["01090"], verifier="pile_flow"),
]


VERIFICATIONS = r'''
def pile_flow(monde, aides):
    """Cles propres : `dessus_pile` (card_id de la carte du dessus de State of Flow), `pile` (liste des card_id, dessus en
    DERNIER), `pile_vide` (bool), `attaque` ([[card_id, ATK courante]]), `etape_un` (n : envoie n fois la fin de l'ETAPE 1 de
    la phase du mechant avant de mesurer, comme `process_villain_phase_step`) ; le reste va a `etat_attendu`."""
    from game.message import Message
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    for _ in range(int(attendu.get("etape_un") or 0)):
        debut = Message.WhenVillainPhaseStepStart(1, monde)
        debut.Send()
        Message.AfterResolveVillainPhaseStep(1, debut).Send()
    if any(k in attendu for k in ("dessus_pile", "pile", "pile_vide")):
        face = aides["par_id"](monde, "ch002")
        if face is None:
            soucis.append("State of Flow introuvable en jeu")
            contenu = []
        else:
            contenu = [getattr(f.paper, "card_id", None) for f in face.GetPlacedCardArea().Get()]
        if "dessus_pile" in attendu and (not contenu or contenu[-1] != attendu["dessus_pile"]):
            soucis.append(f"dessus de la pile = {contenu[-1] if contenu else None} (attendu {attendu['dessus_pile']}) ; pile = {contenu}")
        if "pile" in attendu and contenu != attendu["pile"]:
            soucis.append(f"pile = {contenu} (attendu {attendu['pile']})")
        if attendu.get("pile_vide") and contenu:
            soucis.append(f"la pile devait etre vide, elle contient {contenu}")
    for card_id, valeur in attendu.get("attaque") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (attaque)")
        elif face.attack != valeur:
            soucis.append(f"ATK de {card_id} = {face.attack} (attendu {valeur})")
    propres = ("dessus_pile", "pile", "pile_vide", "attaque", "etape_un")
    cas["attendu"] = {k: v for k, v in attendu.items() if k not in propres}
    try:
        if cas["attendu"]:
            ok, msg = etat_attendu(monde, aides)
            if not ok:
                soucis.append(msg)
    finally:
        cas["attendu"] = attendu
    return (False, " ; ".join(soucis)) if soucis else (True, "Shang-Chi conforme")
'''
