# Cas test_capacites du scenario BAXTER STOCKMAN v3 (TMNT Villains / Modulars, Inkwire, prefixe `tx`)
# et de la carte d'etat DAZED (6e etat du moteur). Noms : « [dazed] ... » et « [baxter] txNNN ... »
# (filtres : `[dazed]`, `[baxter]`). Gabarits PROCESSUS-CARTE : .planning/tmnt/baxter-gabarits-processus-carte.md.
#
# Montage Dazed : Spider-Man (01001a ATQ 2 / CTR 1 / DEF 3) en forme heros contre Rhino 01094 (ATQ 2 / MNG 1,
# PV 14), comme tools/cas/cloaked.py. Le deck rencontre ne garde que 01105 « I'm Tough » (0 icone de boost).

FORME_HEROS = "Puzzle.ChangeForm('01001b')"
RIEN_A_BOOSTER = "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"

CAS = []


def _d(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[dazed] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", "rhino"),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "bx_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


# ========================================================================= Dazed : -2 aux pouvoirs, +2 aux degats
CAS += [
    _d("pose : Puzzle.Daze pose une vraie carte d'etat reconnue par HasStatus",
       "la carte d'etat existe (card_id dazed), HasStatus('Dazed') la compte, une seule carte",
       [FORME_HEROS, "Puzzle.Daze('01001a')"], [], {"statuts": [["01001a", "Dazed"]], "nb_dazed": [["01001a", 1]]}),
    _d("attaque de base du heros : -2 ATQ (2 -> 0 degat), carte defaussee",
       "« uses a basic power ... decrease that value by 2 » : ATQ 2 - 2 = 0 degat sur Rhino ; la carte part",
       [FORME_HEROS, "Puzzle.Daze('01001a')"], ["Puzzle.Attack('01001a')"],
       {"degats": [["01094", 0]], "statuts_absents": [["01001a", "Dazed"]]},
       main_exclusive=["01088"], cibles=["01094"]),
    _d("TEMOIN : attaque de base sans Dazed = ATQ imprimee seule (2 degats)",
       "contre-cas : prouve que le 0 du cas precedent vient de la carte",
       [FORME_HEROS], ["Puzzle.Attack('01001a')"], {"degats": [["01094", 2]]},
       main_exclusive=["01088"], cibles=["01094"]),
    _d("contre de base du heros : -2 CTR (minimum 0), carte defaussee",
       "« a basic power » couvre le contre : CTR 1 - 2 = 0 (jamais negatif) : 5 menaces restent 5 ; la carte part",
       [FORME_HEROS, "Puzzle.Daze('01001a')"], ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Thwart('01001a')"],
       {"menace": [["01097b", 5]], "statuts_absents": [["01001a", "Dazed"]]}, main_exclusive=["01088"]),
    _d("TEMOIN : contre de base sans Dazed = 1 menace retiree (5 -> 4)",
       "contre-cas du precedent",
       [FORME_HEROS], ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Thwart('01001a')"],
       {"menace": [["01097b", 4]]}, main_exclusive=["01088"]),
    _d("activation d'ennemi (attaque) : -2 ATQ, carte defaussee",
       "Rhino hebete frappe : ATQ 2 - 2 = 0 degat a l'identite (sans boost) ; Dazed part",
       [FORME_HEROS, "Puzzle.Exhaust('01001a')", RIEN_A_BOOSTER, "Puzzle.Daze('01094')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0, "statuts_absents": [["01094", "Dazed"]]}, main_exclusive=["01088"]),
    _d("TEMOIN : activation d'ennemi sans Dazed = ATQ imprimee seule (2 degats)",
       "contre-cas du precedent",
       [FORME_HEROS, "Puzzle.Exhaust('01001a')", RIEN_A_BOOSTER], ["Puzzle.Attack('01094')"],
       {"degats_identite": 2}, main_exclusive=["01088"]),
    _d("activation d'ennemi (manigance) : -2 MNG (minimum 0), carte defaussee",
       "« or activates » vaut aussi pour la manigance : MNG 1 - 2 = 0 menace ; Dazed part",
       [FORME_HEROS, RIEN_A_BOOSTER, "Puzzle.Daze('01094')"], ["Puzzle.Scheme('01094')"],
       {"menace": [["01097b", 0]], "statuts_absents": [["01094", "Dazed"]]}, main_exclusive=["01088"]),
    _d("TEMOIN : manigance d'ennemi sans Dazed = MNG imprimee seule (1 menace)",
       "contre-cas du precedent",
       [FORME_HEROS, RIEN_A_BOOSTER], ["Puzzle.Scheme('01094')"],
       {"menace": [["01097b", 1]]}, main_exclusive=["01088"]),
    _d("degats subis : +2, carte defaussee",
       "« would take any amount of damage, increase that value by 2 » : 1 degat direct = 3 subis ; Dazed part",
       [FORME_HEROS, "Puzzle.Daze('01001a')"], ["Puzzle.Damage('01001a', 1)"],
       {"degats_identite": 3, "statuts_absents": [["01001a", "Dazed"]]}),
    _d("TEMOIN : 1 degat sans Dazed = 1 subi",
       "contre-cas du precedent",
       [FORME_HEROS], ["Puzzle.Damage('01001a', 1)"], {"degats_identite": 1}),
    _d("degats subis : zero degat n'est pas « une quantite » : Dazed reste",
       "« any amount of damage » : 0 degat ne declenche pas la carte (comme Cloaked) ; elle n'est pas defaussee",
       [FORME_HEROS, "Puzzle.Daze('01001a')"], ["Puzzle.Damage('01001a', 0)"],
       {"degats_identite": 0, "statuts": [["01001a", "Dazed"]]}),
    # ------------------------------------------------------------ UN SEUL effet, le premier qui arrive
    _d("un seul effet : le pouvoir de base arrive d'abord (-2), les degats suivants ne sont PAS augmentes",
       "attaque de base (0 degat, carte consommee) puis 1 degat au heros : 1 subi, pas 3",
       [FORME_HEROS, "Puzzle.Daze('01001a')"], ["Puzzle.Attack('01001a')", "Puzzle.Damage('01001a', 1)"],
       {"degats": [["01094", 0]], "degats_identite": 1, "statuts_absents": [["01001a", "Dazed"]]},
       main_exclusive=["01088"], cibles=["01094"]),
    _d("un seul effet : les degats arrivent d'abord (+2), l'attaque suivante n'a PAS -2",
       "1 degat (3 subis, carte consommee) puis attaque de base : 2 degats, pas 0",
       [FORME_HEROS, "Puzzle.Daze('01001a')"], ["Puzzle.Damage('01001a', 1)", "Puzzle.Attack('01001a')"],
       {"degats": [["01094", 2]], "degats_identite": 3, "statuts_absents": [["01001a", "Dazed"]]},
       main_exclusive=["01088"], cibles=["01094"]),
    # ------------------------------------------------------------ un seul Dazed par personnage
    _d("un seul Dazed par personnage : le second n'est pas pose",
       "« a character can only have one Dazed status card on them » : deux Puzzle.Daze consecutifs (le second RETIRE, "
       "c'est la bascule du harnais) ne prouvent rien : on pose par GiveStatus deux fois (cas de verification dedie)",
       [FORME_HEROS], [], {"deux_dazed": "01001a"}, verifier="bx_deux_dazed"),
    # ------------------------------------------------------------ Tough d'abord
    _d("Tough resout AVANT Dazed : Tough absorbe, Dazed reste en place",
       "heros avec Tough ET Dazed, 1 degat : Tough part, 0 degat, Dazed intact (« Tough status cards always resolve before ... »)",
       [FORME_HEROS, "Puzzle.Tough('01001a')", "Puzzle.Daze('01001a')"], ["Puzzle.Damage('01001a', 1)"],
       {"degats_identite": 0, "statuts": [["01001a", "Dazed"]], "statuts_absents": [["01001a", "Tough"]]}),
    _d("Tough resout AVANT Dazed meme quand Dazed a ete pose en PREMIER",
       "ordre de pose inverse (Dazed puis Tough) : l'ordre d'enregistrement des cartes d'etat ne doit pas decider ; Tough absorbe, "
       "0 degat, Dazed intact",
       [FORME_HEROS, "Puzzle.Daze('01001a')", "Puzzle.Tough('01001a')"], ["Puzzle.Damage('01001a', 1)"],
       {"degats_identite": 0, "statuts": [["01001a", "Dazed"]], "statuts_absents": [["01001a", "Tough"]]}),
    _d("zero degat REEL (attaque de Baxter I, ATQ 0) : « any amount of damage » n'est pas atteint, Dazed reste",
       "Baxter Stockman I (ATQ 0, aucun boost) attaque une identite hebetee : 0 degat, la carte Dazed n'est pas consommee "
       "(contre-cas : sans la condition « au moins 1 degat » elle ajouterait ses 2 degats)",
       [FORME_HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.Daze('01001a')", "Puzzle.CreateEncounterDeck('01105')"],
       ["Puzzle.Attack('tx001')"],
       {"degats_identite": 0, "statuts": [["01001a", "Dazed"]]}, scenario="baxter_stockman", main_exclusive=["01088"]),
    # ------------------------------------------------------------ Cloaked et Dazed : SIMULTANES
    _d("Cloaked + Dazed, degats : simultanes (1 - 2 + 2 = 1), les DEUX cartes defaussees",
       "« Cloaked and Dazed status cards always resolve simultaneously » : 1 degat = 1 subi (en sequence on obtiendrait 0 ou 3), "
       "les deux cartes partent",
       [FORME_HEROS, "Puzzle.Cloak('01001a')", "Puzzle.Daze('01001a')"], ["Puzzle.Damage('01001a', 1)"],
       {"degats_identite": 1, "statuts_absents": [["01001a", "Dazed"], ["01001a", "Cloaked"]]}),
    _d("Cloaked + Dazed, attaque de base : simultanes (2 + 2 - 2 = 2), les DEUX cartes defaussees",
       "ATQ 2 reste 2 : ni 4 (Cloaked seul) ni 0 (Dazed seul)",
       [FORME_HEROS, "Puzzle.Cloak('01001a')", "Puzzle.Daze('01001a')"], ["Puzzle.Attack('01001a')"],
       {"degats": [["01094", 2]], "statuts_absents": [["01001a", "Dazed"], ["01001a", "Cloaked"]]},
       main_exclusive=["01088"], cibles=["01094"]),
    _d("Cloaked seul reste inchange : degats -2 (non-regression du correctif de cloaked.py)",
       "3 degats avec Cloaked seul = 1 subi",
       [FORME_HEROS, "Puzzle.Cloak('01001a')"], ["Puzzle.Damage('01001a', 3)"],
       {"degats_identite": 1, "statuts_absents": [["01001a", "Cloaked"]]}),
    # ------------------------------------------------------------ DEF : -2 DEF, puis la carte part AVANT l'exces
    _d("defense du heros : -2 DEF (3 -> 1), carte defaussee AVANT les degats : l'exces n'est PAS augmente",
       "Shocker (ATQ 2) frappe, Spider-Man hebete DEFEND : DEF 3 - 2 = 1, 2 - 1 = 1 degat (pas 3) ; Dazed part. Peter "
       "forme heros, main videe : le pilote declare la defense",
       [FORME_HEROS, "Puzzle.Daze('01001a')", "Puzzle.PutIntoPlay('01103')", RIEN_A_BOOSTER],
       ["Puzzle.Attack('01103')"],
       {"degats_identite": 1, "statuts_absents": [["01001a", "Dazed"]]}, main_exclusive=["01088"]),
    _d("TEMOIN : meme attaque sans Dazed, DEF 3 bloque tout (0 degat)",
       "contre-cas du precedent",
       [FORME_HEROS, "Puzzle.PutIntoPlay('01103')", RIEN_A_BOOSTER],
       ["Puzzle.Attack('01103')"],
       {"degats_identite": 0}, main_exclusive=["01088"]),
]

VERIFICATIONS = r'''
CLES_BX = {"nb_dazed", "dazed_total", "distribuees", "engages_ids", "compteurs_de_tous", "menace_cible",
           "traits_absents_de", "valeurs", "compte_en_jeu", "taille_deck_rencontre", "defaite"}


def _bx_en_jeu(monde, card_id):
    return [o.face for o in monde.object_manager.card_dict.values()
            if o.face is not None and o.face.IsInPlay() and getattr(o.face.paper, "card_id", None) == card_id]


def bx_etat(monde, aides):
    """etat_attendu (cles communes) + les cles du bloc Baxter :
    nb_dazed [[card_id, n]] (cartes Dazed posees sur la carte), dazed_total (cartes Dazed sur TOUS les personnages amis),
    distribuees [n_joueur1, ...] (cartes rencontre distribuees face cachee, pas encore revelees),
    engages_ids [[ids engages avec le joueur 1], ...], compteurs_de_tous [[card_id, compteur, [valeurs triees]]]
    (TOUS les exemplaires en jeu), menace_cible [[card_id, n]], traits_absents_de [[card_id, trait]],
    valeurs [[card_id, attribut, n]] (getattr direct), compte_en_jeu {card_id: n}, taille_deck_rencontre n."""
    from game.operate.worlds import Worlds
    attendu = aides["cas"].get("attendu") or {}
    inconnues = sorted(set(attendu) - set(CLES_ETAT_ATTENDU) - CLES_BX)
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de bx_etat : {inconnues}"
    ok, message = etat_attendu(monde, aides)
    soucis = [] if ok else [message]
    for card_id, n in attendu.get("nb_dazed") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (nb_dazed)")
        elif face.dazed != n:
            soucis.append(f"{card_id} porte {face.dazed} carte(s) Dazed (attendu {n})")
    if "dazed_total" in attendu:
        total = 0
        for joueur in monde.const_players:
            for ami in [joueur.GetIdentity()] + list(joueur.allies.Get()):
                total += ami.dazed
        if total != attendu["dazed_total"]:
            soucis.append(f"{total} carte(s) Dazed sur les personnages amis (attendu {attendu['dazed_total']})")
    if "distribuees" in attendu:
        vues = [len(j.dealt_encounter_cards.Get()) for j in monde.const_players]
        if vues != attendu["distribuees"]:
            soucis.append(f"cartes distribuees face cachee par joueur = {vues} (attendu {attendu['distribuees']})")
    if "engages_ids" in attendu:
        vus = [sorted(getattr(c.paper, "card_id", "?") for c in j.engaged_minions.Get()) for j in monde.const_players]
        voulu = [sorted(x) for x in attendu["engages_ids"]]
        if vus != voulu:
            soucis.append(f"sbires engages par joueur = {vus} (attendu {voulu})")
    for card_id, compteur, valeurs in attendu.get("compteurs_de_tous") or []:
        vus = sorted(f.GetCounters(compteur) for f in _bx_en_jeu(monde, card_id))
        if vus != sorted(valeurs):
            soucis.append(f"compteurs {compteur} des {card_id} en jeu = {vus} (attendu {sorted(valeurs)})")
    for card_id, n in attendu.get("menace_cible") or []:
        face = aides["par_id"](monde, card_id)
        vu = getattr(face, "target_threat", None) if face is not None else None
        if face is None or vu != n:
            soucis.append(f"menace cible de {card_id} = {vu} (attendu {n})")
    for card_id, trait in attendu.get("traits_absents_de") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (traits_absents_de)")
        elif face.HasTrait(trait):
            soucis.append(f"{card_id} a le trait {trait} (attendu : absent)")
    for card_id, nom, n in attendu.get("valeurs") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (valeurs)")
        elif getattr(face, nom) != n:
            soucis.append(f"{card_id}.{nom} = {getattr(face, nom)} (attendu {n})")
    for card_id, n in (attendu.get("compte_en_jeu") or {}).items():
        vu = len(_bx_en_jeu(monde, card_id))
        if vu != n:
            soucis.append(f"{vu} exemplaire(s) de {card_id} en jeu (attendu {n})")
    if "taille_deck_rencontre" in attendu:
        n = len(Worlds.GetEncounterDeckCards(monde))
        if n != attendu["taille_deck_rencontre"]:
            soucis.append(f"deck rencontre = {n} carte(s) (attendu {attendu['taille_deck_rencontre']})")
    if "defaite" in attendu:
        perdu = bool(monde.is_game_over) and not monde.game_over.players_won
        if perdu != attendu["defaite"]:
            soucis.append(f"defaite = {perdu} (attendu {attendu['defaite']}, partie terminee = {monde.is_game_over})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"


def bx_defaite(monde, aides):
    return bx_etat(monde, aides)


def bx_actions(monde, aides):
    """attendu.action_offerte [[card_id, n]] : nombre d'actions de heros / d'actions offertes par la carte
    (HeroAction pour tx005, Action pour tx018) dans la forme courante du joueur."""
    from game.ability.ability import AbilityType
    from game.event.manager import EventManager
    from game.message import Message
    from game.effect.rule import GameRule
    attendu = aides["cas"]["attendu"]
    soucis = []
    for card_id, n in attendu["action_offerte"]:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu")
            continue
        type_ = AbilityType.Action if card_id == "tx018" else AbilityType.HeroAction
        joueur = monde.GetCurrentPlayer()
        candidats = [x for x in face.effect.Find(when=Message.WhenPlayerInTurn, type=type_) if not x.ability.is_play]
        msg = Message.WhenPlayerLikeInTurn(joueur, GameRule(joueur.GetIdentity()))
        msg.Send()
        offertes = EventManager.FilterAvailableEffects(msg, candidats, joueur, monde, None)
        if len(offertes) != n:
            soucis.append(f"{card_id} offre {len(offertes)} action(s) (attendu {n})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "actions conformes"


def bx_essaim(monde, aides):
    """Etat d'un sbire a compteur du scenario. attendu : carte, en_jeu (defaut True), compteur (defaut swarm),
    compteurs_carte, pv, pv_max, atq, mng, defausse_rencontre, traits_de, valeurs."""
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if not attendu.get("en_jeu", True):
        if face is not None:
            return False, f"{attendu['carte']} est encore en jeu (PV {face.health}/{face.max_health})"
        if attendu.get("defausse_rencontre"):
            from game.operate.worlds import Worlds
            ids = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDiscardPileCards(monde)]
            if attendu["carte"] not in ids:
                return False, f"{attendu['carte']} n'est pas dans la defausse de rencontre ({ids})"
        return True, f"{attendu['carte']} n'est plus en jeu"
    if face is None:
        return False, f"{attendu['carte']} n'est pas en jeu"
    compteur = attendu.get("compteur", "swarm")
    mesure = {"compteurs_carte": face.GetCounters(compteur), "pv": face.health, "pv_max": face.max_health,
              "atq": face.attack, "mng": getattr(face, "scheme", None)}
    ecarts = [f"{k}={mesure[k]} (attendu {v})" for k, v in attendu.items() if k in mesure and mesure[k] != v]
    for card_id, trait in attendu.get("traits_de") or []:
        f2 = aides["par_id"](monde, card_id)
        if f2 is None or not f2.HasTrait(trait):
            ecarts.append(f"{card_id} n'a pas le trait {trait}")
    for card_id, nom, n in attendu.get("valeurs") or []:
        f2 = aides["par_id"](monde, card_id)
        if f2 is None or getattr(f2, nom) != n:
            ecarts.append(f"{card_id}.{nom} = {getattr(f2, nom, None)} (attendu {n})")
    if ecarts:
        return False, " ; ".join(ecarts) + f" [mesure {mesure}]"
    return True, f"etat conforme {mesure}"


def bx_deux_dazed(monde, aides):
    """Pose Dazed DEUX FOIS par le vrai chemin (Faces.GiveStatus) : la 2e doit etre refusee (retour 0)."""
    from game.operate.faces import Faces
    from game.effect.rule import GameRule
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["deux_dazed"])
    regle = GameRule(face)
    premier = Faces.GiveStatus([face], "Dazed", regle)
    second = Faces.GiveStatus([face], "Dazed", regle)
    if (premier, second) != (1, 0):
        return False, f"GiveStatus rend ({premier}, {second}) (attendu (1, 0))"
    if face.dazed != 1:
        return False, f"{face.dazed} carte(s) Dazed posee(s) (attendu 1)"
    return True, "un seul Dazed par personnage"
'''



# ========================================================================= SCENARIO BAXTER STOCKMAN
# Montage : Spider-Man (01001b alter-ego, 01001a heros) contre Baxter Stockman I (tx001) ; la mise en place
# reelle pose la manigance 1B (tx004b), le vilain et UNE Plague of M.O.U.S.E.R.S. (tx007, 2 compteurs swarm)
# engagee avec chaque joueur. EXPERT : Baxter II (tx002) en jeu avec le Baxter Blaster (tx005) attache des la mise
# en place. Deux joueurs : Spider-Man + Black Widow (`heros2`).
SC = "baxter_stockman"
SCE = "baxter_stockman_expert"
DUO = {"heros2": "black_widow"}
SANS_PLAGUE = "Puzzle.Remove('tx007')"
FORME_ET_INCLINE = [FORME_HEROS, "Puzzle.Exhaust('01001a')"]


# ⚠ LE DECK RENCONTRE REEL CONTIENT DES EXEMPLAIRES DE CHAQUE CARTE DU SET (4 Plague, 3 Flyborgs...).
# `FindOrCreateFace` cherche le deck rencontre AVANT les cartes en jeu : sans ce vidage, `Puzzle.Damage('tx007')`,
# `Puzzle.Remove('tx007')`, `Puzzle.Discard(...)` visaient la copie du DECK et non celle en jeu (mesure du 16/10/2026 :
# 20 rouges sur 93, tous de ce motif). On le vide donc au debut de CHAQUE cas (la mise en place reelle est deja faite,
# l'etat en jeu est intact) et on le remplace par trois cartes inoffensives, sauf si le cas bati le sien.
FOND = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]


def _b(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = FOND + list(mise)
    cas = {"nom": "[baxter] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "bx_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS += [
    # ===================================================================== tx004a / tx004b : mise en place
    _b("tx004a Setup (solo) : UNE Plague (tx007) engagee avec le joueur, 2 compteurs swarm ; Baxter I et le complot 1B en jeu",
       "« Put a Plague of M.O.U.S.E.R.S. minion into play engaged with each player » ; le passage 1A -> 1B est fait par le moteur",
       [], [], {"en_jeu": ["tx001", "tx004b", "tx007"], "hors_jeu": ["tx004a", "tx002"], "engages_ids": [["tx007"]],
                "compteurs": [["tx007", "swarm", 2]], "compte_en_jeu": {"tx007": 1}}),
    _b("tx004a Setup (2 joueurs) : UNE Plague PAR joueur, chacune engagee avec SON joueur",
       "« engaged with EACH player » : deux Plague, une engagee avec chaque joueur (pas les deux avec le premier)",
       [], [], {"engages_ids": [["tx007"], ["tx007"]], "compte_en_jeu": {"tx007": 2},
                "compteurs_de_tous": [["tx007", "swarm", [2, 2]]]}, **DUO),
    _b("tx004b menace : depart 1 par joueur, cible 11 par joueur (solo : 1 / 11)",
       "StartingThreat 1*, TargetThreat 11*",
       [], [], {"menace": [["tx004b", 1]], "menace_cible": [["tx004b", 11]]}),
    _b("tx004b menace : depart 1 par joueur, cible 11 par joueur (2 joueurs : 2 / 22)",
       "les valeurs `N*` se multiplient par le nombre de joueurs",
       [], [], {"menace": [["tx004b", 2]], "menace_cible": [["tx004b", 22]]}, **DUO),
    _b("tx004b « If this scheme is completed, the players lose the game » : menace a la cible -> defaite",
       "11 menaces sur le complot 1B (cible 11, solo) : la partie est perdue, regle de base du dernier stade",
       [], ["Puzzle.SetThreat('tx004b', 11)"], {"defaite": True}, verifier="bx_defaite"),
    _b("tx004b TEMOIN : 10 menaces sur 11 : pas de defaite",
       "contre-cas du precedent",
       [], ["Puzzle.SetThreat('tx004b', 10)"], {"defaite": False}, verifier="bx_defaite"),
    # ===================================================================== tx001 : Toughness, Forced Interrupt
    _b("tx001 Baxter Stockman I : PV 13 par joueur (solo 13), Toughness (carte Tough a l'entree en jeu)",
       "PV 13[per_hero] ; « Toughness. » est une base automatique : le vilain entre avec une carte d'etat Tough",
       [], [], {"pv_max": [["tx001", 13]], "statuts": [["tx001", "Tough"]]}),
    _b("tx001 Baxter Stockman I : PV 13 par joueur (2 joueurs : 26)",
       "le `13*` se multiplie par le nombre de joueurs",
       [], [], {"pv_max": [["tx001", 26]]}, **DUO),
    _b("tx001 Forced Interrupt : au debut de la phase du mechant, le joueur resout le Special : +1 compteur sur sa Plague, aucune carte distribuee",
       "« each player resolves the Special on the Baxter's Laboratory scheme » : un SWARM engage avec le joueur -> 1 compteur (2 -> 3) ; rien a distribuer",
       [], ["Puzzle.BeginVillainPhase()"], {"compteurs": [["tx007", "swarm", 3]], "distribuees": [0]}),
    _b("tx001 TEMOIN : sans debut de phase du mechant, la Plague garde ses 2 compteurs",
       "contre-cas du precedent : le +1 vient de l'interruption forcee",
       [], [], {"compteurs": [["tx007", "swarm", 2]]}),
    _b("tx001 Forced Interrupt, aucun SWARM engage : le joueur recoit UNE carte rencontre face cachee",
       "Plague retiree : « If there are no SWARM minions engaged with you, deal yourself a facedown encounter card »",
       [SANS_PLAGUE], ["Puzzle.BeginVillainPhase()"], {"distribuees": [1], "hors_jeu": ["tx007"]}),
    _b("tx001 Forced Interrupt, un sbire NON-SWARM engage ne compte pas : une carte face cachee est distribuee",
       "Plague retiree, Shocker (01103, pas SWARM) engage : « no SWARM minions engaged with you » -> carte distribuee, aucun compteur",
       [SANS_PLAGUE, "Puzzle.PutIntoPlay('01103')"], ["Puzzle.BeginVillainPhase()"],
       {"distribuees": [1], "engages_ids": [["01103"]]}),
    _b("tx001 Forced Interrupt (2 joueurs) : CHAQUE joueur resout, sur SA Plague : 3 et 3 (pas 4 sur la meme)",
       "« each player resolves » + « engaged with YOU » : la Plague du joueur 1 gagne 1, celle du joueur 2 gagne 1",
       [], ["Puzzle.BeginVillainPhase()"],
       {"compteurs_de_tous": [["tx007", "swarm", [3, 3]]], "distribuees": [0, 0]}, **DUO),
    _b("tx001 Forced Interrupt (2 joueurs) : le joueur 2 n'a aucun SWARM : il recoit une carte, le joueur 1 un compteur",
       "la Plague du joueur 2 est retiree puis remplacee par un sbire non-SWARM : joueur 1 -> compteur, joueur 2 -> carte face cachee",
       [SANS_PLAGUE, SANS_PLAGUE, "Puzzle.PutIntoPlay('tx007')", "Puzzle.PutIntoPlay('01103', player=1)"],
       ["Puzzle.BeginVillainPhase()"],
       {"compteurs_de_tous": [["tx007", "swarm", [3]]], "distribuees": [0, 1]}, **DUO),
    # ===================================================================== tx002 : When Revealed, Forced Interrupt
    _b("tx002 When Revealed : cherche le Baxter Blaster (tx005) dans le deck rencontre et le revele : il s'attache a Baxter II",
       "passage au stade II : « Search the encounter deck and discard pile for the Baxter Blaster attachment and reveal it » ; "
       "le tx005 quitte le deck",
       ["Puzzle.CreateEncounterDeck('tx005')"], ["Puzzle.AdvanceVillain()"],
       {"en_jeu": ["tx002", "tx005"], "accroche_a": [["tx005", "tx002"]], "hors_jeu": ["tx001"], "taille_deck_rencontre": 3}),
    _b("tx002 When Revealed : le Blaster n'est que dans la DEFAUSSE rencontre : il est trouve aussi",
       "« the encounter deck AND DISCARD PILE » : deck vide, tx005 en defausse",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDiscardPile('tx005')"], ["Puzzle.AdvanceVillain()"],
       {"accroche_a": [["tx005", "tx002"]]}),
    _b("tx002 When Revealed : aucun Blaster nulle part : rien ne plante, rien n'est revele",
       "deck et defausse vides de tx005",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.AdvanceVillain()"],
       {"en_jeu": ["tx002"], "hors_jeu": ["tx005"]}),
    _b("tx002 EXPERT : Baxter II en jeu des la mise en place, Blaster deja attache",
       "mode expert : « Baxter Stockman (II) and Baxter (III) » ; le When Revealed du stade II part a la mise en place",
       [], [], {"en_jeu": ["tx002", "tx005", "tx004b"], "hors_jeu": ["tx001"], "accroche_a": [["tx005", "tx002"]],
                "pv_max": [["tx002", 16]], "statuts": [["tx002", "Tough"]]}, scenario=SCE),
    _b("tx002 Forced Interrupt : au debut de la phase du mechant (stade II), +1 compteur sur la Plague",
       "meme texte que le stade I",
       [], ["Puzzle.BeginVillainPhase()"], {"compteurs": [["tx007", "swarm", 3]]}, scenario=SCE),
    # ===================================================================== tx003 : guard, When Revealed, Forced Interrupt
    _b("tx003 : « Each SWARM minion gains guard » : la Plague (SWARM) a guard 1, un sbire non-SWARM n'en gagne pas",
       "expert : Baxter II -> III (AdvanceVillain). Plague : guard 0 -> 1 ; Shocker (01103) : guard 0",
       ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.AdvanceVillain()"],
       {"en_jeu": ["tx003"], "valeurs": [["tx007", "guard", 1], ["01103", "guard", 0]]}, scenario=SCE),
    _b("tx003 TEMOIN : au stade II (avant tx003), la Plague n'a pas guard",
       "contre-cas du precedent",
       [], [], {"valeurs": [["tx007", "guard", 0]]}, scenario=SCE),
    _b("tx003 When Revealed : UNE carte rencontre face cachee par joueur (solo : 1)",
       "« Deal each player 1 facedown encounter card »",
       [], ["Puzzle.AdvanceVillain()"], {"distribuees": [1]}, scenario=SCE),
    _b("tx003 When Revealed (2 joueurs) : une carte face cachee a CHAQUE joueur",
       "deux joueurs : une carte chacun",
       [], ["Puzzle.AdvanceVillain()"], {"distribuees": [1, 1]}, scenario=SCE, **DUO),
    _b("tx003 TEMOIN : le stade II (When Revealed du Blaster seulement) ne distribue aucune carte",
       "contre-cas : la distribution vient bien du stade III",
       [], [], {"distribuees": [0]}, scenario=SCE),
    _b("tx003 Forced Interrupt : au debut de la phase du mechant (stade III), +1 compteur sur la Plague",
       "meme texte que les stades I et II",
       ["Puzzle.AdvanceVillain()"], ["Puzzle.BeginVillainPhase()"], {"compteurs": [["tx007", "swarm", 3]]}, scenario=SCE),
]

# ========================================================================= tx005 : Baxter Blaster
CAS += [
    _b("tx005 Attach to Baxter Stockman : s'attache au VILAIN (tx001), pas au sbire homonyme de Donatello (td015)",
       "td015 (« * Baxter Stockman », SBIRE) en jeu AVANT : le Blaster va sur le vilain tx001",
       ["Puzzle.PutIntoPlay('td015')"], ["Puzzle.PutIntoPlay('tx005')"],
       {"accroche_a": [["tx005", "tx001"]]}),
    _b("tx005 Forced Response : apres que Baxter attaque ET blesse un personnage ami, ce personnage est hebete",
       "expert (Baxter II ATQ 1, Blaster attache) : 1 degat a l'identite (sans boost) -> Dazed sur l'identite",
       FORME_ET_INCLINE + ["Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.Attack('tx002')"],
       {"degats_identite": 1, "statuts": [["01001a", "Dazed"]]}, scenario=SCE, main_exclusive=["01088"]),
    _b("tx005 TEMOIN : sans Blaster, la meme attaque ne hebete personne",
       "contre-cas : le Dazed vient bien de la carte (Blaster retire de la partie)",
       FORME_ET_INCLINE + ["Puzzle.Remove('tx005')", "Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.Attack('tx002')"],
       {"degats_identite": 1, "statuts_absents": [["01001a", "Dazed"]]}, scenario=SCE, main_exclusive=["01088"]),
    _b("tx005 « attacks AND damages » : un coup entierement prevenu (Tough) n'hebete pas",
       "identite Tough : le degat est absorbe, 0 degat subi, pas de Dazed (Tough part)",
       FORME_ET_INCLINE + ["Puzzle.Tough('01001a')", "Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.Attack('tx002')"],
       {"degats_identite": 0, "statuts_absents": [["01001a", "Dazed"], ["01001a", "Tough"]]}, scenario=SCE, main_exclusive=["01088"]),
    _b("tx005 ATQ « ★ » : AUCUN bonus d'ATQ (decision utilisateur Q1) : Baxter II garde son ATQ imprimee 1",
       "lecture provisoire : l'etoile de la case ATQ ne definit aucune valeur ; ATQ de Baxter II = 1 avec ou sans Blaster",
       [], [], {"attributs_carte": [["tx002", "attack", 0]]}, scenario=SCE),
    _b("tx005 Hero Action « Exhaust your hero » : le Blaster est defausse et le heros s'incline",
       "forme heros, Blaster attache (expert) ; action 0 = incliner le heros",
       [FORME_HEROS], ["Puzzle.Action('tx005', 'HeroAction', 0)"],
       {"hors_jeu": ["tx005"], "exhausted": ["01001a"]}, scenario=SCE, main_exclusive=["01088"]),
    _b("tx005 Hero Action « spend 2 resources of any type » : Energy (YY) paie, le Blaster est defausse, le heros reste pret",
       "action 1 = payer 2 ressources de n'importe quel type",
       [FORME_HEROS], ["Puzzle.Action('tx005', 'HeroAction', 1)"],
       {"hors_jeu": ["tx005"], "pret": ["01001a"], "defausse": ["01088"], "taille_main": 0}, scenario=SCE,
       main_exclusive=["01088"], payer_avec=["01088"], payer_tout=True),
    _b("tx005 Hero Action : DEUX actions offertes en forme heros (incliner / 2 ressources), AUCUNE en alter-ego",
       "« Hero Action » : reservee a la forme heros ; deux couts alternatifs = deux capacites",
       [], [], {"action_offerte": [["tx005", 0]]}, scenario=SCE, main_exclusive=["01088"], verifier="bx_actions"),
    _b("tx005 Hero Action : deux actions offertes en forme heros",
       "meme position en forme heros",
       [FORME_HEROS], [], {"action_offerte": [["tx005", 2]]}, scenario=SCE, main_exclusive=["01088"], verifier="bx_actions"),
    _b("tx005 Boost : retourne comme carte de boost, le Blaster s'attache a Baxter Stockman",
       "« [star] Boost: Attach Baxter Blaster to Baxter Stockman » : stade I, Blaster pas encore en jeu",
       [], ["Puzzle.Boost('tx005')"], {"accroche_a": [["tx005", "tx001"]]}),
]

# ========================================================================= tx006 : Swarm Superiority
CAS += [
    _b("tx006 Attach to a SWARM minion : s'attache a la Plague, qui gagne AERIAL et guard 1, et recoit 2 compteurs",
       "When Revealed : 2 compteurs all-purpose sur le sbire porteur = 2 swarm (2 -> 4)",
       [], ["Puzzle.Reveal('tx006')"],
       {"accroche_a": [["tx006", "tx007"]], "traits_de": [["tx007", "AERIAL"]], "valeurs": [["tx007", "guard", 1]],
        "compteurs": [["tx007", "swarm", 4]]}),
    _b("tx006 TEMOIN : sans la carte, la Plague n'a ni AERIAL ni guard",
       "contre-cas du precedent",
       [], [], {"traits_absents_de": [["tx007", "AERIAL"]], "valeurs": [["tx007", "guard", 0]]}),
    _b("tx006 : la defausse de la carte retire AERIAL et guard (ils ne tiennent qu'a l'attachement)",
       "carte attachee puis defaussee : trait et mot-cle disparaissent, les 2 compteurs restent",
       [], ["Puzzle.Reveal('tx006')", "Puzzle.Discard('tx006')"],
       {"traits_absents_de": [["tx007", "AERIAL"]], "valeurs": [["tx007", "guard", 0]], "compteurs": [["tx007", "swarm", 4]]}),
    _b("tx006 « If you cannot, this card gains surge » : aucun SWARM en jeu -> surge",
       "Plague retiree ; la carte seme au sommet est revelee par le Surge",
       [SANS_PLAGUE, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"],
       ["Puzzle.Reveal('tx006')"], {"carte_du_surge": "01105", "hors_jeu": ["tx006"]}),
    _b("tx006 : un sbire NON-SWARM en jeu ne suffit pas -> surge",
       "Plague retiree, Shocker (01103) en jeu : « a SWARM minion » est un trait",
       [SANS_PLAGUE, "Puzzle.PutIntoPlay('01103')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"],
       ["Puzzle.Reveal('tx006')"], {"carte_du_surge": "01105", "hors_jeu": ["tx006"], "valeurs": [["01103", "guard", 0]]}),
]

# ========================================================================= tx007 / tx012 : essaims
CAS += [
    _b("tx007 Plague of M.O.U.S.E.R.S. : entre avec 2 compteurs swarm : ATQ, MNG et PV valent 2",
       "« Enters play with 2 swarm counters. [star] SCH, ATK and hit points are equal to the number of swarm counters »",
       [], [], {"carte": "tx007", "compteurs_carte": 2, "pv": 2, "pv_max": 2, "atq": 2, "mng": 2}, verifier="bx_essaim"),
    _b("tx007 : 1 degat retire 1 compteur INSTEAD ; PV et ATQ suivent, aucun degat inscrit",
       "« remove that many swarm counters from here instead »",
       [], ["Puzzle.Damage('tx007', 1)"], {"carte": "tx007", "compteurs_carte": 1, "pv": 1, "pv_max": 1, "atq": 1, "mng": 1},
       verifier="bx_essaim"),
    _b("tx007 : 3 degats sur 2 compteurs : vaincu par le moteur (PV 0), pas a la main",
       "aucun exces ne passe ; la Plague part a la defausse rencontre",
       [], ["Puzzle.Damage('tx007', 3)"], {"carte": "tx007", "en_jeu": False, "defausse_rencontre": True},
       verifier="bx_essaim"),
    _b("tx007 : la Plague grossit avec le Special : 3 compteurs -> ATQ, MNG et PV valent 3",
       "le Special ajoute un compteur swarm, les trois valeurs suivent (fusion de la mecanique swarm et de Replicate)",
       [], ["Puzzle.BeginVillainPhase()"], {"carte": "tx007", "compteurs_carte": 3, "pv": 3, "pv_max": 3, "atq": 3, "mng": 3},
       verifier="bx_essaim"),
    _b("tx012 Flight of Flyborgs : entre avec 4 compteurs swarm : ATQ, MNG et PV valent 4 ; traits AERIAL, FLYBORG (singulier), SWARM",
       "meme montage que la Plague avec 4 compteurs ; le trait imprime est FLYBORG, pas FLYBORGS",
       ["Puzzle.PutIntoPlay('tx012')"], [],
       {"carte": "tx012", "compteurs_carte": 4, "pv": 4, "pv_max": 4, "atq": 4, "mng": 4,
        "traits_de": [["tx012", "AERIAL"], ["tx012", "FLYBORG"], ["tx012", "SWARM"]]}, verifier="bx_essaim"),
    _b("tx012 : 3 degats : 1 compteur reste, PV 1, toujours en jeu",
       "« that many » : 3 compteurs retires sur 4",
       ["Puzzle.PutIntoPlay('tx012')"], ["Puzzle.Damage('tx012', 3)"],
       {"carte": "tx012", "compteurs_carte": 1, "pv": 1, "pv_max": 1, "atq": 1, "mng": 1}, verifier="bx_essaim"),
    _b("tx012 : 9 degats sur 4 compteurs : vaincu par le moteur",
       "meme logique que la Plague",
       ["Puzzle.PutIntoPlay('tx012')"], ["Puzzle.Damage('tx012', 9)"],
       {"carte": "tx012", "en_jeu": False, "defausse_rencontre": True}, verifier="bx_essaim"),
]

# ========================================================================= tx013 : Superfly
CAS += [
    _b("tx013 Superfly : entre avec 2 compteurs Ooze : ATQ et MNG valent 2, PV imprimes 5",
       "« Enters play with 2 Ooze counters. [star] SCH and ATK are equal to the number of Ooze counters » ; PV non dynamiques",
       ["Puzzle.PutIntoPlay('tx013')"], [],
       {"carte": "tx013", "compteurs_carte": 2, "pv": 5, "pv_max": 5, "atq": 2, "mng": 2, "compteur": "ooze"}, verifier="bx_essaim"),
    _b("tx013 : le Special (+1 Ooze) -> ATQ et MNG valent 3, PV toujours 5",
       "Replicate pose un compteur « all-purpose » = Ooze sur Superfly",
       [SANS_PLAGUE, "Puzzle.PutIntoPlay('tx013')"], ["Puzzle.BeginVillainPhase()"],
       {"carte": "tx013", "compteurs_carte": 3, "pv": 5, "pv_max": 5, "atq": 3, "mng": 3, "compteur": "ooze"}, verifier="bx_essaim"),
    _b("tx013 : 2 degats sont de VRAIS degats (pas un retrait de compteurs) : PV 3, Ooze inchange",
       "Superfly n'a pas la clause « remove counters instead » des essaims",
       ["Puzzle.PutIntoPlay('tx013')"], ["Puzzle.Damage('tx013', 2)"],
       {"carte": "tx013", "compteurs_carte": 2, "pv": 3, "pv_max": 5, "atq": 2, "mng": 2, "compteur": "ooze"}, verifier="bx_essaim"),
    _b("tx013 : 5 degats vainquent Superfly (PV 5)",
       "vaincu normalement, defausse rencontre",
       ["Puzzle.PutIntoPlay('tx013')"], ["Puzzle.Damage('tx013', 5)"],
       {"carte": "tx013", "en_jeu": False, "defausse_rencontre": True}, verifier="bx_essaim"),
]

# ========================================================================= tx015 : Roadkill Rodneys
CAS += [
    _b("tx015 Roadkill Rodneys : entre avec 1 compteur cable : ATQ 1 + 1 = 2 ; PV 3, MNG 1",
       "« Enters play with 1 cable counter. [star] +1 ATK for each cable counter »",
       ["Puzzle.PutIntoPlay('tx015')"], [],
       {"carte": "tx015", "compteurs_carte": 1, "pv": 3, "pv_max": 3, "atq": 2, "mng": 1, "compteur": "cable"}, verifier="bx_essaim"),
    _b("tx015 : le Special (+1 cable) -> ATQ 3",
       "Replicate pose un compteur cable ; « +1 ATK for EACH cable counter » suit",
       [SANS_PLAGUE, "Puzzle.PutIntoPlay('tx015')"], ["Puzzle.BeginVillainPhase()"],
       {"carte": "tx015", "compteurs_carte": 2, "pv": 3, "pv_max": 3, "atq": 3, "mng": 1, "compteur": "cable"}, verifier="bx_essaim"),
    _b("tx015 Forced Response : apres avoir attaque ET blesse un personnage, il l'hebete et retire TOUS ses cables",
       "alter-ego (pas de Coup Rapide a l'entree en jeu) : 2 cables -> ATQ 3 : 3 degats a l'identite (sans boost) ; Dazed sur l'identite ; "
       "cable 0 ; ATQ retombee a 1",
       ["Puzzle.PutIntoPlay('tx015')", "Puzzle.CreateEncounterDeck('01105')", "Puzzle.Counter('tx015', 'cable', 1)"],
       ["Puzzle.Attack('tx015')"],
       {"degats_identite": 3, "statuts": [["01001b", "Dazed"]], "compteurs": [["tx015", "cable", 0]],
        "attributs_carte": [["tx015", "attack", 0]]}, main_exclusive=["01088"]),
    _b("tx015 TEMOIN : « attacks AND damages » : coup entierement prevenu (Tough) -> pas de Dazed, les cables restent",
       "identite Tough : 0 degat subi, aucun effet de la Reponse forcee",
       ["Puzzle.Tough('01001b')", "Puzzle.PutIntoPlay('tx015')", "Puzzle.CreateEncounterDeck('01105')"],
       ["Puzzle.Attack('tx015')"],
       {"degats_identite": 0, "statuts_absents": [["01001b", "Dazed"], ["01001b", "Tough"]], "compteurs": [["tx015", "cable", 1]]},
       main_exclusive=["01088"]),
]

# ========================================================================= tx017 : Auto Defense Bots
CAS += [
    _b("tx017 Auto Defense Bots : entre avec 1 compteur shield ; guard 1, patrol 1 ; PV 1, ATQ 1, MNG 0",
       "« Guard. Patrol. Enters play with 1 shield counter on them. »",
       ["Puzzle.PutIntoPlay('tx017')"], [],
       {"carte": "tx017", "compteurs_carte": 1, "pv": 1, "pv_max": 1, "atq": 1, "mng": 0, "compteur": "shield",
        "valeurs": [["tx017", "guard", 1], ["tx017", "patrol", 1]]}, verifier="bx_essaim"),
    _b("tx017 Forced Interrupt : « would be defeated » : soigne tout et retire 1 shield : il survit (shield 0, 0 degat)",
       "1 degat sur PV 1 : il devrait mourir ; il est soigne et perd son bouclier",
       ["Puzzle.PutIntoPlay('tx017')"], ["Puzzle.Damage('tx017', 1)"],
       {"carte": "tx017", "compteurs_carte": 0, "pv": 1, "pv_max": 1, "atq": 1, "mng": 0, "compteur": "shield"}, verifier="bx_essaim"),
    _b("tx017 : sans bouclier, le coup suivant le vainc (le texte n'a plus rien a retirer ; decision utilisateur Q3)",
       "2 coups : le 1er consomme le shield, le 2nd vainc le sbire (lecture provisoire)",
       ["Puzzle.PutIntoPlay('tx017')"], ["Puzzle.Damage('tx017', 1)", "Puzzle.Damage('tx017', 1)"],
       {"carte": "tx017", "en_jeu": False, "defausse_rencontre": True}, verifier="bx_essaim"),
    _b("tx017 : le Special (+1 shield) -> 2 boucliers : il survit a DEUX coups mortels",
       "Replicate pose un shield ; deux coups, deux boucliers retires, le sbire reste",
       [SANS_PLAGUE, "Puzzle.PutIntoPlay('tx017')"], ["Puzzle.BeginVillainPhase()", "Puzzle.Damage('tx017', 1)", "Puzzle.Damage('tx017', 1)"],
       {"carte": "tx017", "compteurs_carte": 0, "pv": 1, "pv_max": 1, "atq": 1, "mng": 0, "compteur": "shield"}, verifier="bx_essaim"),
]

# ========================================================================= tx004b : le Special « Replicate », pose par type de sbire
CAS += [
    _b("tx004b Replicate : Flight of Flyborgs (tx012) et Plague (tx007) engages avec le joueur gagnent CHACUN 1 compteur",
       "« each SWARM minion engaged with you » : tx007 2 -> 3, tx012 4 -> 5",
       ["Puzzle.PutIntoPlay('tx012')"], ["Puzzle.BeginVillainPhase()"],
       {"compteurs": [["tx007", "swarm", 3], ["tx012", "swarm", 5]], "distribuees": [0]}),
    _b("tx004b Replicate : le compteur « all-purpose » de Superfly est un compteur OOZE (la carte porteuse en definit le type)",
       "FAQ officielle MC4DB : le type du compteur est celui de la carte qui le porte ; Ooze 2 -> 3",
       [SANS_PLAGUE, "Puzzle.PutIntoPlay('tx013')"], ["Puzzle.BeginVillainPhase()"],
       {"compteurs": [["tx013", "ooze", 3], ["tx013", "swarm", 0]]}),
    _b("tx004b Replicate : le compteur de Roadkill Rodneys est un CABLE (cable 1 -> 2)",
       "meme regle : ni swarm ni un compteur generique",
       [SANS_PLAGUE, "Puzzle.PutIntoPlay('tx015')"], ["Puzzle.BeginVillainPhase()"],
       {"compteurs": [["tx015", "cable", 2], ["tx015", "swarm", 0]]}),
    _b("tx004b Replicate : le compteur d'Auto Defense Bots est un SHIELD (shield 1 -> 2)",
       "meme regle",
       [SANS_PLAGUE, "Puzzle.PutIntoPlay('tx017')"], ["Puzzle.BeginVillainPhase()"],
       {"compteurs": [["tx017", "shield", 2], ["tx017", "swarm", 0]]}),
    _b("tx004b Replicate : un Roadkill Rodneys SANS cable (apres sa Reponse forcee) regagne un CABLE, pas un compteur generique",
       "tous les cables retires : « all-purpose » ne doit pas devenir un compteur `counter` sans effet (COMPTEUR_DU_SBIRE)",
       [SANS_PLAGUE, "Puzzle.PutIntoPlay('tx015')", "Puzzle.Counter('tx015', 'cable', -1)"], ["Puzzle.BeginVillainPhase()"],
       {"compteurs": [["tx015", "cable", 1]], "attributs_carte": [["tx015", "attack", 1]]}),
    _b("tx004b Replicate : seuls les SWARM ENGAGES AVEC LE JOUEUR gagnent un compteur (Plague du joueur 2 ignoree par le joueur 1)",
       "2 joueurs, Plague du joueur 2 seule : le joueur 1 recoit une carte (aucun SWARM engage avec lui), la Plague du joueur 2 gagne 1 compteur de SON Special",
       [SANS_PLAGUE, "Puzzle.PutIntoPlay('tx007', player=1)"], ["Puzzle.BeginVillainPhase()"],
       {"compteurs_de_tous": [["tx007", "swarm", [3]]], "distribuees": [1, 0]}, **DUO),
]

# ========================================================================= tx008 / tx009 / tx014 : traitrises
CAS += [
    _b("tx008 Radical Ingenuity, option 1 : resout le Special (Plague 2 -> 3), aucune menace posee",
       "« Choose: Resolve the Special ability on Baxter's Laboratory »",
       [], ["Puzzle.Reveal('tx008')"], {"compteurs": [["tx007", "swarm", 3]], "menace": [["tx004b", 1]]},
       preferer_option="Resolve the"),
    _b("tx008 Radical Ingenuity, option 2 : 2 menaces sur le complot principal (1 -> 3), pas de Special",
       "« Choose: Place 2 threat on the main scheme »",
       [], ["Puzzle.Reveal('tx008')"], {"compteurs": [["tx007", "swarm", 2]], "menace": [["tx004b", 3]]},
       preferer_option="Place 2 threat"),
    _b("tx008 Radical Ingenuity, option 1 sans SWARM engage : le joueur recoit UNE carte face cachee",
       "le Special est resolu par le joueur a qui la carte est revelee",
       [SANS_PLAGUE], ["Puzzle.Reveal('tx008')"], {"distribuees": [1]}, preferer_option="Resolve the"),
    _b("tx009 Rapid Replication : defausse jusqu'a un sbire, le revele, PUIS resout le Special (revele et Plague +1)",
       "deck : 01105, 01105, tx015 (sbire SWARM), 01105 : deux defaussees, tx015 defausse puis revele (cable 1, +1 du Special = 2) ; "
       "Plague 2 -> 3",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', 'tx015', '01105', '01105')"], ["Puzzle.Reveal('tx009')"],
       {"en_jeu": ["tx015"], "compteurs": [["tx015", "cable", 2], ["tx007", "swarm", 3]], "taille_deck_rencontre": 1}, verifier="bx_etat"),
    _b("tx009 : le sbire est la DERNIERE carte du deck (bord du deck) : il est quand meme revele",
       "deck : tx015 tout en bas, deux 01105 au-dessus ; le deck est vide apres la defausse du sbire",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('tx015', '01105', '01105')"], ["Puzzle.Reveal('tx009')"],
       {"en_jeu": ["tx015"], "compteurs": [["tx007", "swarm", 3]]}),
    _b("tx009 : aucun sbire dans le deck, un sbire en DEFAUSSE : la defausse est melangee dans le deck, le sbire est revele",
       "deck : 01105 x2 ; defausse : tx017. Le deck s'epuise sans sbire, la defausse est remelangee, on continue",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')", "Puzzle.CreateEncounterDiscardPile('tx017')"],
       ["Puzzle.Reveal('tx009')"], {"en_jeu": ["tx017"]}),
    _b("tx009 : aucun sbire nulle part : rien de revele, le Special est resolu quand meme (Plague 2 -> 3)",
       "« Then, resolve the Special » ne depend pas du sbire",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"], ["Puzzle.Reveal('tx009')"],
       {"compteurs": [["tx007", "swarm", 3]], "hors_jeu": ["tx015", "tx017"]}),
    _b("tx014 Buzz Off, option 1 : 3 menaces sur le complot principal (1 -> 4), aucun degat",
       "« Choose: Place 3 threat on the main scheme »",
       [], ["Puzzle.Reveal('tx014')"], {"menace": [["tx004b", 4]], "degats_identite": 0}, preferer_option="Place 3 threat"),
    _b("tx014 Buzz Off, option 2 : 2 degats a l'identite, menace inchangee",
       "« Choose: Take 2 damage »",
       [], ["Puzzle.Reveal('tx014')"], {"menace": [["tx004b", 1]], "degats_identite": 2}, preferer_option="Take 2 damage"),
]

# ========================================================================= tx010 / tx011 : manigances annexes
CAS += [
    _b("tx010 Robotics Facility : 4 menaces de depart FIXES + Hinder 1 par joueur (solo : 5)",
       "StartingThreat 4 (sans icone de joueur) ; Hinder 1[per_hero] ajoute 1 menace a l'entree en jeu",
       [], ["Puzzle.PutIntoPlay('tx010')"], {"menace": [["tx010", 5]]}),
    _b("tx010 Robotics Facility (2 joueurs) : 4 fixes + Hinder 2 = 6",
       "le Hinder 1[per_hero] double avec deux joueurs, les 4 de depart non",
       [], ["Puzzle.PutIntoPlay('tx010')"], {"menace": [["tx010", 6]]}, **DUO),
    _b("tx010 icones : Acceleration et Crisis portees (desc), lues en jeu",
       "bases automatiques, aucun script : l'icone doit etre REELLEMENT portee",
       [], ["Puzzle.PutIntoPlay('tx010')"], {"icones": [["Acceleration", 1], ["Crisis", 1]]}),
    _b("tx010 Crisis : le complot principal ne peut plus etre contre (menace 5 reste 5)",
       "contre de base du heros avec Crisis en jeu : aucune menace retiree du complot",
       [FORME_HEROS, "Puzzle.PutIntoPlay('tx010')"], ["Puzzle.SetThreat('tx004b', 5)", "Puzzle.Thwart('01001a')"],
       {"menace": [["tx004b", 5]]}, main_exclusive=["01088"]),
    _b("tx010 TEMOIN : sans Robotics Facility, le meme contre retire 1 menace (5 -> 4)",
       "contre-cas du precedent",
       [FORME_HEROS], ["Puzzle.SetThreat('tx004b', 5)", "Puzzle.Thwart('01001a')"],
       {"menace": [["tx004b", 4]]}, main_exclusive=["01088"]),
    _b("tx011 Mad Lab : 2 menaces par joueur (solo 2, 2 joueurs 4)",
       "StartingThreat 2*",
       [], ["Puzzle.PutIntoPlay('tx011')"], {"menace": [["tx011", 2]]}),
    _b("tx011 Mad Lab (2 joueurs) : 4 menaces",
       "le `2*` double",
       [], ["Puzzle.PutIntoPlay('tx011')"], {"menace": [["tx011", 4]]}, **DUO),
    _b("tx011 Forced Interrupt : le PREMIER joueur resout un Special DE PLUS (sa Plague : 2 -> 4 avec celui du vilain), pas le second",
       "2 joueurs, Mad Lab en jeu : joueur 1 : +1 (Baxter) +1 (Mad Lab) = 4 ; joueur 2 : +1 (Baxter) = 3",
       ["Puzzle.PutIntoPlay('tx011')"], ["Puzzle.BeginVillainPhase()"],
       {"compteurs_de_tous": [["tx007", "swarm", [3, 4]]]}, **DUO),
    _b("tx011 TEMOIN : sans Mad Lab, les deux Plague gagnent 1 (3 et 3)",
       "contre-cas du precedent",
       [], ["Puzzle.BeginVillainPhase()"], {"compteurs_de_tous": [["tx007", "swarm", [3, 3]]]}, **DUO),
]

# ========================================================================= tx016 : Wrapped Up
CAS += [
    _b("tx016 Wrapped Up : hebete UN personnage ami (solo : l'identite)",
       "« Daze a friendly character » : Spider-Man seul -> son identite est hebetee",
       [FORME_HEROS], ["Puzzle.Reveal('tx016')"], {"statuts": [["01001a", "Dazed"]], "dazed_total": 1}),
    _b("tx016 : avec un allie en jeu, UN SEUL personnage est hebete (le joueur choisit)",
       "identite + Daredevil (01058) : « a friendly character » = exactement un",
       [FORME_HEROS, "Puzzle.PutIntoPlay('01058', under_control=True)"], ["Puzzle.Reveal('tx016')"], {"dazed_total": 1}),
    _b("tx016 « If you cannot, this card gains surge » : l'identite est DEJA hebetee, aucun allie -> surge",
       "personne ne peut etre hebete : la carte du sommet est revelee par le Surge",
       [FORME_HEROS, "Puzzle.Daze('01001a')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"],
       ["Puzzle.Reveal('tx016')"], {"carte_du_surge": "01105", "nb_dazed": [["01001a", 1]]}),
    _b("tx016 TEMOIN : quelqu'un peut etre hebete -> PAS de surge (la carte du sommet reste dans le deck)",
       "contre-cas du surge : identite non hebetee",
       [FORME_HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105')"],
       ["Puzzle.Reveal('tx016')"], {"statuts": [["01001a", "Dazed"]], "taille_deck_rencontre": 2}),
]

# ========================================================================= tx018 : Intruder Alert!
CAS += [
    _b("tx018 Attach to your identity : s'attache a l'identite du joueur",
       "revelee : accrochee a Peter Parker (alter-ego)",
       [], ["Puzzle.Reveal('tx018')"], {"accroche_a": [["tx018", "01001b"]]}),
    _b("tx018 Crisis : le complot principal ne peut plus etre contre tant que l'attachement est en jeu",
       "contre du heros (forme heros) avec Intruder Alert sur son identite : menace 5 reste 5",
       [FORME_HEROS, "Puzzle.PutIntoPlay('tx018')"], ["Puzzle.SetThreat('tx004b', 5)", "Puzzle.Thwart('01001a')"],
       {"menace": [["tx004b", 5]], "icones": [["Crisis", 1]]}, main_exclusive=["01088"]),
    _b("tx018 Action « Take 2 damage » : l'identite subit 2 degats, la carte est defaussee",
       "action 0 : cout = 2 degats a l'identite (alter-ego : « Action » nu vaut dans les DEUX formes)",
       [], ["Puzzle.PutIntoPlay('tx018')", "Puzzle.Action('tx018', 'Action', 0)"],
       {"degats_identite": 2, "hors_jeu": ["tx018"]}, main_exclusive=["01088"]),
    _b("tx018 Action « exhaust your identity » : l'identite s'incline, la carte est defaussee",
       "action 1 : cout = incliner l'identite (alter-ego)",
       [], ["Puzzle.PutIntoPlay('tx018')", "Puzzle.Action('tx018', 'Action', 1)"],
       {"exhausted": ["01001b"], "degats_identite": 0, "hors_jeu": ["tx018"]}, main_exclusive=["01088"]),
    _b("tx018 Action en FORME HEROS : « exhaust your identity » incline le heros",
       "« your IDENTITY » (pas « your hero ») : meme action dans les deux formes ; ici la forme heros",
       [FORME_HEROS], ["Puzzle.PutIntoPlay('tx018')", "Puzzle.Action('tx018', 'Action', 1)"],
       {"exhausted": ["01001a"], "hors_jeu": ["tx018"]}, main_exclusive=["01088"]),
    _b("tx018 Boost : « [star] Boost: Reveal this card » : retournee comme carte de boost, elle est REVELEE (attachee a l'identite)",
       "stade I, deck rencontre contenant tx018 : le Boost la revele",
       [], ["Puzzle.Boost('tx018')"], {"accroche_a": [["tx018", "01001b"]]}),
]

# ========================================================================= etape 6 : les nombres imprimes
# Table recopiee A LA MAIN depuis les scans (`.planning/tmnt/pics-baxter/`), INDEPENDAMMENT de `cards.json` : le cas
# relit `cards.json` et compare. Une valeur absente de la table n'est pas verifiee ; une valeur de la table absente de
# `desc` fait echouer.
IMPRIME = {
    "tx001": ("Villain", {"HP": "13*", "ATK": "0", "SCH": "1", "Stage": "I", "Toughness": "1"}, ["AERIAL", "FLY", "GENIUS"]),
    "tx002": ("Villain", {"HP": "16*", "ATK": "1", "SCH": "2", "Stage": "II", "Toughness": "1"}, ["AERIAL", "FLY", "GENIUS"]),
    "tx003": ("Villain", {"HP": "19*", "ATK": "2", "SCH": "2", "Stage": "III", "Toughness": "1"}, ["AERIAL", "FLY", "GENIUS"]),
    "tx004a": ("MainScheme", {"Stage": "1A"}, []),
    "tx004b": ("MainScheme", {"StartingThreat": "1*", "TargetThreat": "11*", "EscalationThreat": "1*", "Stage": "1B"}, []),
    "tx005": ("Attachment", {"Boost": "0"}, ["TECH", "WEAPON"]),
    "tx006": ("Attachment", {"Boost": "1"}, ["CONDITION"]),
    # PV, ATQ et MNG sont des ETOILES imprimees (valeur dynamique, `desc` = "0", lue sur les compteurs)
    "tx007": ("Minion", {"HP": "0", "ATK": "0", "SCH": "0", "Boost": "1"}, ["MOUSERS", "SWARM"]),
    "tx008": ("Treachery", {"Boost": "2"}, []),
    "tx009": ("Treachery", {"Boost": "2"}, []),
    "tx010": ("SideScheme", {"StartingThreat": "4", "Hinder": "1*", "Boost": "1", "Acceleration": "1", "Crisis": "1"}, []),
    "tx011": ("SideScheme", {"StartingThreat": "2*", "Boost": "1"}, []),
    "tx012": ("Minion", {"HP": "0", "ATK": "0", "SCH": "0", "Boost": "2"}, ["AERIAL", "FLYBORG", "SWARM"]),
    # ATQ et MNG : etoiles (suivent les compteurs Ooze) ; PV imprimes 5
    "tx013": ("Minion", {"HP": "5", "ATK": "0", "SCH": "0", "Boost": "3"}, ["AERIAL", "FLYBORG", "SWARM"]),
    "tx014": ("Treachery", {"Boost": "1"}, []),
    "tx015": ("Minion", {"HP": "3", "ATK": "1", "SCH": "1", "Boost": "2", "Quickstrike": "1"}, ["ROBOT", "SWARM"]),
    "tx016": ("Treachery", {"Boost": "1"}, []),
    "tx017": ("Minion", {"HP": "1", "ATK": "1", "SCH": "0", "Boost": "1", "Guard": "1", "Patrol": "1"}, ["ROBOT", "SWARM"]),
    "tx018": ("Attachment", {"Boost": "1", "Crisis": "1"}, []),
}
for _id, (_type, _desc, _traits) in IMPRIME.items():
    CAS.append({
        "nom": f"[baxter] {_id} nombres imprimes (etape 6) : {_type} {_desc}",
        "pourquoi": "texte <-> code : chaque valeur lue sur le scan est dans `desc` de cards.json (type, PV, ATQ, MNG, menaces, "
                    "icones de boost, mots-cles chiffres, traits)",
        "scenario": SC, "heros": "spider_man", "mise_en_place": [], "declencher": [],
        "verifier": "bx_imprime", "attendu": {"carte": _id, "type": _type, "desc": _desc, "traits": _traits},
    })

VERIFICATIONS += r'''
def bx_imprime(monde, aides):
    """Compare cards.json (relu depuis le disque) a la table des valeurs lues sur le scan."""
    import json, os
    attendu = aides["cas"]["attendu"]
    donnees = json.load(open(os.path.join(os.getcwd(), "data", "cards.json"), encoding="utf-8"))
    carte = None
    for pack, cartes in donnees.items():
        if isinstance(cartes, list):
            for c in cartes:
                if isinstance(c, dict) and c.get("card_id") == attendu["carte"]:
                    carte = c
    if carte is None:
        return False, f"{attendu['carte']} absente de cards.json"
    soucis = []
    if carte["type"] != attendu["type"]:
        soucis.append(f"type {carte['type']} (attendu {attendu['type']})")
    for cle, valeur in attendu["desc"].items():
        if carte["desc"].get(cle) != valeur:
            soucis.append(f"desc.{cle} = {carte['desc'].get(cle)!r} (attendu {valeur!r})")
    for cle in carte["desc"]:
        if cle not in attendu["desc"]:
            soucis.append(f"desc.{cle} = {carte['desc'][cle]!r} NON lu sur le scan (a verifier)")
    if sorted(carte["traits"]) != sorted(attendu["traits"]):
        soucis.append(f"traits {carte['traits']} (attendu {attendu['traits']})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "nombres imprimes conformes"
'''
