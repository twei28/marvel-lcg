# Cas du MODE CAMPAGNE de Skrull Menace : prefixe « [campagne_mode] ».
#
# Ce fichier ne definit AUCUN cas pour `tools/test_capacites.py` (`CAS = []` : chaque cas y
# monterait UNE partie, or une campagne se prouve en en jouant plusieurs a la suite). Les
# cas sont des CHAINES, jouees par `tools/test_campagne_chaine.py` :
#
#   RELEASE=1 python3.10 tools/test_campagne_chaine.py "$PWD/.game-src" 31000 /tmp/rapport.json
#
# Voir l'en-tete de ce harnais pour la forme d'une chaine. Les fonctions de verification sont
# de VRAIES fonctions Python (le harnais importe ce fichier dans son fils) ; elles n'importent
# le moteur qu'a l'interieur, pour que `test_capacites.py` puisse charger ce module sans moteur.
#
# CARTES FACTICES : les 26 cartes de campagne sk263-sk288 sont portees EN PARALLELE par un
# autre agent. Ces cas n'en dependent pas : `injecter_factices()` cree, dans CardsDB et seulement
# pour le processus de test, une carte du bon type et du bon nom pour chaque id ABSENT. Quand les
# vraies cartes sont fusionnees, elles prennent le pas (l'injection saute un id deja connu).
CAS = []

CHAINES = []

ELITES = {"Crusader": "sk231", "Jazinda": "sk236", "Skymax": "sk241", "War Skrull": "sk245", "Xavin": "sk250"}
ENSEMBLES = {"Crusader": "sk_skrull_elite_crusader", "Jazinda": "sk_skrull_elite_jazinda",
             "Skymax": "sk_skrull_elite_skymax", "War Skrull": "sk_skrull_elite_war_skrull",
             "Xavin": "sk_skrull_elite_xavin"}
ALLIES = {"Crusader": "sk263", "Jazinda": "sk264", "Skymax": "sk266", "War Skrull": "sk268", "Xavin": "sk269"}
COMPLOTS = {"Crusader": "sk273", "Jazinda": "sk276", "Skymax": "sk272", "War Skrull": "sk271", "Xavin": "sk270"}
FRAGMENTS = ["sk230a", "sk230b", "sk230c", "sk230d"]

# ---------------------------------------------------------------- cartes factices --
_NOMS_FACTICES = {
    "Ally": [(263, "Crusader"), (264, "Jazinda"), (265, "Paibok"), (266, "Skymax"), (267, "Super-Skrull"),
             (268, "War Skrull"), (269, "Xavin")],
    "PlayerSideScheme": [(270, "Buddy Training Program"), (271, "Cloning Faux Pas"), (272, "Fickle Alliance"),
                         (273, "Newbie Training"), (274, "Searching for Powers"), (275, "Skrull Military Training"),
                         (276, "Stealing for Good")],
    "Support": [(277, "Antalya"), (278, "Cadre K"), (279, "Pool-O-Vision"), (280, "Princess Anelle"),
                (281, "Skrull Battleship"), (282, "Skrull Kill Krew")],
    "Upgrade": [(283, "3-D Man's Goggles"), (284, "Inhibitor Mask"), (285, "Ultimate Nullifier"),
                (286, "Reverting Device"), (287, "Skrull Shapeshifter"), (288, "Sy-Torak Gem")],
}
_DESC_FACTICES = {
    "Ally": {"Cost": "2", "HP": "3", "THW": "1", "ATK": "1", "RES": "R", "Class": "Campaign;Basic"},
    "PlayerSideScheme": {"Cost": "0", "RES": "R", "StartingThreat": "2", "Class": "Campaign;Basic", "Victory": "0"},
    "Support": {"Cost": "1", "RES": "R", "Class": "Campaign;Basic"},
    "Upgrade": {"Cost": "1", "RES": "R", "Class": "Campaign;Basic"},
}


def injecter_factices():
    """Cree les cartes de campagne ABSENTES de CardsDB (donnees de test, jamais ecrites au depot)."""
    from cards.database import CardsDB
    from cards.paper import Paper
    for type_, cartes in _NOMS_FACTICES.items():
        for numero, nom in cartes:
            card_id = f"sk{numero}"
            if card_id in CardsDB.papers:
                continue
            CardsDB.papers[card_id] = Paper(card_id, "", type_, True, nom, "", dict(_DESC_FACTICES[type_]),
                                            ["SKRULL"], "skrull_menace", "Skrull Menace Campaign (test)", "")


# ----------------------------------------------------------------- aides --
def _faces(monde):
    for objet in monde.object_manager.card_dict.values():
        face = getattr(objet, "face", None)
        if face is not None:
            yield face


def _id(face):
    return getattr(getattr(face, "paper", None), "card_id", None)


def _existe(monde, card_id):
    return any(_id(f) == card_id for f in _faces(monde))


def _ou(monde, card_id):
    """Ou est la carte, en clair (voir `test_campagnes._ou_est`)."""
    import test_campagnes as tc
    return tc._ou_est(monde, card_id)


def _deck_rencontre(monde):
    from game.operate.worlds import Worlds
    return [_id(f) for f in Worlds.GetEncounterDeckCards(monde)]


def _de_cote(monde):
    faces = list(monde.aside_deck.Get(True))
    for p in monde.const_players:
        faces += list(p.set_aside_deck.Get(True))
    return [_id(f) for f in faces]


def _en_jeu(monde):
    return [_id(f) for f in _faces(monde) if f.IsInPlay()]


def _victoire(monde):
    return [_id(f) for f in monde.victory_display.Get(True)]


def _deck_joueur(monde, i=0):
    return [_id(f) for f in monde.players[i].player_deck.Get(True)]


def _defausse_joueur(monde, i=0):
    return [_id(f) for f in monde.players[i].discard_pile.Get(True)]


def _liste(valeur):
    return [x for x in (valeur or "").split(";") if x]


def _elites_presentes(monde):
    """Les Elites dont le sbire existe dans la partie (donc dont l'ensemble a ete mis en jeu)."""
    return [nom for nom, sbire in ELITES.items() if _existe(monde, sbire)]


def _ensemble_complet(monde, nom):
    """Toutes les cartes de l'ensemble d'une Elite sont dans le deck rencontre."""
    from game.card.factory import CardFactory
    voulues = sorted(CardFactory.LoadEncounterSet(ENSEMBLES[nom]))
    presentes = sorted(i for i in _deck_rencontre(monde) if i in set(voulues))
    return presentes == voulues


def _verif(*controles):
    """Chaque controle est (condition, message d'echec). Rend (ok, messages)."""
    soucis = [message for condition, message in controles if not condition]
    return (not soucis), " ; ".join(soucis)


def _dump(monde):
    sk = sorted(i for i in {_id(f) for f in _faces(monde)} if i and i.startswith("sk"))
    return (f"deck_rencontre(sk)={sorted(set(i for i in _deck_rencontre(monde) if i.startswith('sk')))} "
            f"de_cote={sorted(_de_cote(monde))} en_jeu(sk)={sorted(i for i in _en_jeu(monde) if i.startswith('sk'))} "
            f"victoire={_victoire(monde)} deck_joueur(sk)={sorted(i for i in _deck_joueur(monde) if i.startswith('sk'))} "
            f"tous_sk={sk}")


def sonde(monde):
    """Mise au point seulement : rend toujours faux et dit tout."""
    return False, _dump(monde)


# ==================================================================== fonctions pures ==
def purs_tableau():
    """Le tableau « Cooperation Progress » et ses outils, SANS partie (p.24 du livret)."""
    from cards.pack.skrull_menace import campaign as C
    soucis = []

    def verifie(condition, message):
        if not condition:
            soucis.append(message)

    def carte(nom, type_="Minion", traits=(), unique=False, nemesis=False, joueur=False):
        return C.CarteDuTableau(nom, type_, list(traits), unique, nemesis, joueur)

    spy = carte("Skrull Spy", traits=["SKRULL", "SPY"])
    scientist = carte("Skrull Scientist", traits=["GENIUS", "SKRULL"])
    telepath = carte("Skrull Telepath", traits=["PSIONIC", "SKRULL"])
    warrior = carte("Skrull Warrior", traits=["SKRULL"])
    soldat = carte("Skrull Soldier", traits=["SKRULL", "SOLDIER"])
    commandant = carte("Skrull Commander", traits=["SKRULL", "SOLDIER"])
    jazinda = carte("Jazinda", traits=["ELITE", "SKRULL"], unique=True)
    shaper = carte("Shaper of Worlds", traits=["COSMIC ENTITY", "ELITE", "SKRULL"], unique=True)
    paibok_nemesis = carte("Paibok", traits=["ELITE", "SKRULL"], unique=True, nemesis=True)
    humain = carte("Hydra Soldier", traits=["HYDRA"])
    monde_ss = carte("Seeking a Suitable World", "SideScheme")
    hijacked = carte("Hijacked", "SideScheme")
    cloning = carte("Cloning Program", "SideScheme")
    trone = carte("Emperor's Throne", "SideScheme")
    revanche = carte("Plotting Revenge", "SideScheme")
    empire = carte("Stealing for the Empire", "SideScheme")
    cube = carte("Cosmic Cube Creation", "SideScheme")
    ss_joueur = carte("Newbie Training", "SideScheme", joueur=True)
    ss_nemesis = carte("Punish the Defector", "SideScheme", nemesis=True)
    ss_simple = carte("Overthrow", "SideScheme")

    # --- chaque exigence imprimee, un cas qui la remplit et un qui ne la remplit pas
    R = C.ExigenceRemplie
    attendu = {
        "Nemesis minion": ([paibok_nemesis], [warrior, ss_nemesis]),
        "Nemesis side scheme": ([ss_nemesis], [ss_simple, paibok_nemesis]),
        "Non-ELITE minion": ([warrior, humain], [jazinda, ss_simple]),
        "ELITE minion": ([jazinda, shaper], [warrior, cube]),
        "GENIUS minion": ([scientist], [warrior, spy]),
        "SOLDIER minion": ([soldat, commandant], [warrior]),
        "SKRULL minion": ([warrior, jazinda], [humain, hijacked]),
        "Non-SKRULL minion": ([humain], [warrior, jazinda]),
        "ELITE non-SKRULL minion": ([carte("Elite humain", traits=["ELITE"])], [jazinda, warrior]),
        "ELITE SKRULL minion": ([jazinda, shaper], [warrior, humain]),
        "Non-ELITE SKRULL minion": ([warrior, spy], [jazinda, humain]),
        "Non-ELITE non-SKRULL minion": ([humain], [warrior, jazinda]),
        "Unique minion": ([jazinda], [warrior]),
        "Non-unique minion": ([warrior], [jazinda]),
        "Player side scheme": ([ss_joueur], [ss_simple, hijacked, warrior]),
        "Seeking a Suitable World": ([monde_ss], [hijacked, warrior]),
        "Hijacked": ([hijacked], [monde_ss]),
        "Cloning Program": ([cloning], [hijacked]),
        "Emperor's Throne": ([trone], [hijacked]),
        "Plotting Revenge": ([revanche], [hijacked]),
        "Stealing for the Empire": ([empire], [hijacked]),
        "Cosmic Cube Creation": ([cube], [hijacked]),
        "Skrull Spy": ([spy], [warrior, scientist]),
        "Skrull Warrior": ([warrior], [spy]),
        "Skrull Soldier": ([soldat], [commandant]),
        "Skrull Commander": ([commandant], [soldat]),
        "Skrull Scientist": ([scientist], [spy]),
        "Skrull Telepath": ([telepath], [spy]),
        "Jazinda": ([jazinda], [shaper, warrior]),
    }
    toutes = {e for _, _, exigences, _ in C.PROGRESSION for e in exigences}
    verifie(toutes == set(attendu), f"exigences du tableau sans cas : {sorted(toutes - set(attendu))} / en trop : {sorted(set(attendu) - toutes)}")
    for exigence, (oui, non) in attendu.items():
        for c in oui:
            verifie(R(exigence, c), f"« {exigence} » devrait etre remplie par {c['nom']}")
        for c in non:
            verifie(not R(exigence, c), f"« {exigence} » ne devrait PAS etre remplie par {c['nom']}")
    verifie(len(C.PROGRESSION) == 13 and sum(len(e) for _, _, e, _ in C.PROGRESSION) == 34,
            f"le tableau compte {len(C.PROGRESSION)} lignes / {sum(len(e) for _, _, e, _ in C.PROGRESSION)} cases (attendu 13 / 34, p.24)")

    # --- l'assignation : une carte, UNE case
    def progres(cartes, cochees=()):
        nouvelles, completes = C.AssignerLaProgression(cartes, set(cochees))
        return nouvelles, completes

    n, c = progres([])
    verifie(not n and not c, f"pile vide : rien a cocher ({n}, {c})")

    n, c = progres([spy])
    verifie(len(n) == 1 and not c, f"UNE carte coche UNE case ({n}, {c})")
    verifie(next(iter(n)) in {("Skrull Kill Crew", "Skrull Spy"), ("Reverting Device", "Skrull Spy")},
            f"la case choisie est la plus rare (le titre, pas « Non-ELITE minion ») : {n}")

    n, c = progres([hijacked])
    verifie(n == {("Cadre K", "Hijacked")} and not c, f"un seul Hijacked coche une seule case, dans l'ordre du tableau : {n}")
    n, c = progres([hijacked, hijacked])
    verifie(n == {("Cadre K", "Hijacked"), ("Skrull Battleship", "Hijacked")}, f"deux Hijacked cochent les deux lignes : {n}")

    n, c = progres([spy, scientist, telepath, warrior])
    verifie(c == ["Reverting Device"], f"Spy + Scientist + Telepath + Warrior completent Reverting Device : {c}")
    verifie(n == {("Reverting Device", e) for e in ["Skrull Spy", "Skrull Scientist", "Skrull Warrior", "Skrull Telepath"]},
            f"et ses quatre cases : {n}")

    n, c = progres([spy, warrior, soldat, commandant])
    verifie(c == ["Skrull Kill Crew"], f"Spy + Warrior + Soldier + Commander completent Skrull Kill Crew : {c}")

    # un seul Spy et un seul Warrior : une des deux lignes seulement, jamais les deux
    n, c = progres([spy, warrior, soldat, commandant, scientist, telepath])
    verifie(len(c) == 1, f"un seul Spy et un seul Warrior : UNE ligne complete, pas deux ({c})")
    # deux de chaque : les deux
    n, c = progres([spy, spy, warrior, warrior, soldat, commandant, scientist, telepath])
    verifie(sorted(c) == ["Reverting Device", "Skrull Kill Crew"], f"deux Spy et deux Warrior : les deux lignes ({c})")

    # le progres reste : les cases deja cochees comptent, un seul sbire manquant suffit
    deja = [("Reverting Device", e) for e in ["Skrull Spy", "Skrull Scientist", "Skrull Warrior"]]
    n, c = progres([telepath], deja)
    verifie(c == ["Reverting Device"] and ("Reverting Device", "Skrull Telepath") in n,
            f"trois cases deja cochees, le Telepath arrive : la ligne se complete ({n}, {c})")

    # une ligne deja pleine au carnet (corrigee a la main) est versee a la zone
    pleines = [("Antalya", "Nemesis minion"), ("Antalya", "Seeking a Suitable World")]
    n, c = progres([], pleines)
    verifie(c == ["Antalya"], f"ligne pleine corrigee a la main : ajoutee ({c})")

    # Antalya : un sbire nemesis + Seeking a Suitable World ; le meme sbire ne coche pas deux cases
    n, c = progres([paibok_nemesis, monde_ss])
    verifie("Antalya" in c, f"Nemesis minion + Seeking a Suitable World completent Antalya ({c})")
    n, c = progres([paibok_nemesis])
    verifie(len(n) == 1 and not c, f"un sbire nemesis seul ne coche qu'une case ({n}, {c})")

    # le cube : une carte, la ligne des fragments
    n, c = progres([cube])
    verifie(c == ["Cosmic Cube Fragment"], f"Cosmic Cube Creation en pile : la ligne des fragments ({c})")
    verifie(C.CartesAjouteesParLigne(c) == FRAGMENTS, f"et ses QUATRE exemplaires (FAQ p.21) : {C.CartesAjouteesParLigne(c)}")

    # tout le reste : la meilleure combinaison, pas la premiere venue
    n, c = progres([warrior, hijacked, scientist, soldat, monde_ss, spy, revanche, humain])
    verifie("Cadre K" in c, f"Non-ELITE minion + Hijacked + GENIUS minion : Cadre K ({c})")

    # --- le carnet : un aller-retour sans perte, dans l'ordre imprime
    texte = C.FormatProgres({("Skrull Kill Crew", "Skrull Spy"), ("Antalya", "Nemesis minion"), ("Cadre K", "Hijacked")})
    verifie(texte == "Antalya: Nemesis minion;Cadre K: Hijacked;Skrull Kill Crew: Skrull Spy", f"format du tableau : {texte!r}")
    verifie(C.ParseProgres(texte.split(";")) == {("Skrull Kill Crew", "Skrull Spy"), ("Antalya", "Nemesis minion"), ("Cadre K", "Hijacked")},
            "relecture du tableau")

    # --- la zone : ordre imprime, sans doublon
    verifie(C.OrdonnerLaZone(["sk286", "sk263", "sk230a", "sk263", "zz"]) == ["sk263", "sk286", "sk230a", "zz"],
            f"ordre de la zone : {C.OrdonnerLaZone(['sk286', 'sk263', 'sk230a', 'sk263', 'zz'])}")
    # --- les types de la zone (livret p.22 : cinq colonnes)
    verifie([C.TypeDeLaCarte(i) for i in ["sk263", "sk269", "sk270", "sk276", "sk277", "sk282", "sk283", "sk288", "sk230c"]]
            == ["Ally", "Ally", "PlayerSideScheme", "PlayerSideScheme", "Support", "Support", "Upgrade", "Upgrade", "Resource"],
            "types des cartes de la zone")
    verifie(C.TypeDeLaCarte("01001a") != "" and C.TypeDeLaCarte("n'existe pas") == "", "repli sur la fiche de la carte, puis sur rien")
    # --- les ensembles d'Elite et la table des ajouts
    verifie([e["nom"] for e in C.ELITES] == list(ELITES), "les cinq Elites, dans l'ordre du livret")
    verifie(all(C.TypeDeLaCarte(e["allie"]) == "Ally" and C.TypeDeLaCarte(e["complot"]) == "PlayerSideScheme" for e in C.ELITES),
            "chaque Elite ajoute un allie et un complot annexe de joueur")
    verifie(C.AJOUTS_DE_SCENARIO == {2: ["sk267", "sk274"], 3: ["sk265", "sk275"]}, "victoires des scenarios 2 et 3 (p.11, p.13)")
    return (not soucis), (" ; ".join(soucis) if soucis else "tableau Cooperation Progress : toutes les exigences, l'assignation, le carnet")


CHAINES += [
    {
        "nom": "[campagne_mode] pur — tableau Cooperation Progress : 34 cases, une carte = une case, ligne complete, carnet",
        "campagne": "skrull_menace",
        "purs": purs_tableau,
        "etapes": [],
    },
]


# ============================================================ mises en place (une partie) ==
def _chaine(nom, carnet, etapes, heros=("lyja",), **extra):
    """Une chaine de campagne Skrull Menace : cartes factices, filtre des cles du fichier de campagne."""
    return {"nom": f"[campagne_mode] {nom}", "campagne": "skrull_menace", "heros": list(heros),
            "carnet": carnet, "preparation": injecter_factices, "etapes": etapes, **extra}


def _fragments_de_cote(monde):
    return [i for i in _de_cote(monde) if i in FRAGMENTS]


def v_scenario1_solo(monde):
    """p.9 : Cosmic Cube Creation melange au deck rencontre ; le Shaper et UN fragment par joueur mis de cote ;
    UN ensemble Skrull Elite au hasard, tout entier dans le deck rencontre."""
    deck = _deck_rencontre(monde)
    elites = _elites_presentes(monde)
    return _verif(
        (deck.count("sk229") == 1, f"Cosmic Cube Creation dans le deck rencontre : {deck.count('sk229')} exemplaire(s)"),
        ("cartes de cote" in _ou(monde, "sk228"), f"le Shaper est mis de cote : {_ou(monde, 'sk228')}"),
        (len(_fragments_de_cote(monde)) == 1, f"un fragment par joueur de cote : {_fragments_de_cote(monde)}"),
        ("sk228" not in deck and not any(f in deck for f in FRAGMENTS), "ni le Shaper ni un fragment dans le deck rencontre"),
        (len(elites) == 1, f"UNE Elite tiree : {elites}"),
        (bool(elites) and _ensemble_complet(monde, elites[0]), f"l'ensemble complet de {elites} est dans le deck rencontre"),
    )


def v_scenario1_duo(monde):
    deck = _deck_rencontre(monde)
    fragments = _fragments_de_cote(monde)
    return _verif(
        (len(fragments) == 2 and len(set(fragments)) == 2, f"DEUX fragments distincts de cote a deux joueurs : {fragments}"),
        (deck.count("sk229") == 1, "un seul Cosmic Cube Creation"),
        (len(_elites_presentes(monde)) == 1, f"UNE seule Elite meme a deux joueurs : {_elites_presentes(monde)}"),
    )


def v_alt_standard(monde):
    from game.card.factory import CardFactory
    deck = _deck_rencontre(monde)
    anciens = set(CardFactory.LoadEncounterSet("standard"))
    nouveaux = sorted(CardFactory.LoadEncounterSet("standard_skrull"))
    presents = sorted(i for i in deck if i in set(nouveaux))
    return _verif(
        (presents == nouveaux, f"Standard Skrull complet dans le deck : {presents} (attendu {nouveaux})"),
        (not [i for i in deck if i in anciens], f"plus aucune carte de Standard : {[i for i in deck if i in anciens]}"),
    )


def v_alt_expert(monde):
    from game.card.factory import CardFactory
    deck = _deck_rencontre(monde)
    expert = set(CardFactory.LoadEncounterSet("expert"))
    skrull = sorted(CardFactory.LoadEncounterSet("expert_skrull"))
    standard = sorted(CardFactory.LoadEncounterSet("standard_skrull"))
    return _verif(
        (sorted(i for i in deck if i in set(skrull)) == skrull, "Expert Skrull complet"),
        (sorted(i for i in deck if i in set(standard)) == standard, "Standard Skrull complet"),
        (not [i for i in deck if i in expert], f"plus aucune carte d'Expert : {[i for i in deck if i in expert]}"),
    )


def v_sans_alternatifs(monde):
    from game.card.factory import CardFactory
    deck = _deck_rencontre(monde)
    standard = set(CardFactory.LoadEncounterSet("standard"))
    skrull = set(CardFactory.LoadEncounterSet("standard_skrull"))
    return _verif(
        (len([i for i in deck if i in standard]) == len(CardFactory.LoadEncounterSet("standard")), "Standard intact par defaut"),
        (not [i for i in deck if i in skrull], "aucune carte de Standard Skrull par defaut"),
    )


CHAINES += [
    _chaine("mise en place 1 — scenario 1 sans carnet : Cube melange, Shaper et un fragment de cote, UNE Elite tiree",
            {}, [{"scenario": "sk_skrull_empire", "verifier": v_scenario1_solo, "fin": "aucune"}]),
    _chaine("mise en place 1 — a DEUX joueurs : deux fragments de cote, toujours une seule Elite",
            {}, [{"scenario": "sk_skrull_empire", "verifier": v_scenario1_duo, "fin": "aucune"}],
            heros=("lyja", "spider_man")),
    _chaine("sets alternatifs — Standard Skrull remplace Standard (reglage de campagne)",
            {"Alternative Standard Set": "1"},
            [{"scenario": "sk_skrull_empire", "verifier": v_alt_standard, "fin": "aucune"}]),
    _chaine("sets alternatifs — Standard Skrull ET Expert Skrull en campagne experte",
            {"Alternative Standard Set": "1", "Alternative Expert Set": "1"},
            [{"scenario": "sk_skrull_empire_expert", "verifier": v_alt_expert, "fin": "aucune"}]),
    _chaine("sets alternatifs — TEMOIN : reglage a 0, Standard reste en place",
            {"Alternative Standard Set": "0"},
            [{"scenario": "sk_skrull_empire", "verifier": v_sans_alternatifs, "fin": "aucune"}]),
]


# ---------------------------------------------------- Shaper of Worlds et Cosmic Cube Creation ==
EN_JEU, MIS_DE_COTE, AUTRE_ZONE, PILE_VICTOIRE, RETIRE = (
    "In play", "Set aside, out of play", "In another game area", "In the victory display", "Removed from campaign")
CLE_SHAPER, CLE_CUBE = "Shaper of Worlds Game Area", "Cosmic Cube Creation Game Area"


def v_en_jeu(monde):
    engages = [_id(f) for f in monde.players[0].engaged_minions.Get(True)]
    deck = _deck_rencontre(monde)
    return _verif(
        ("sk228" in engages, f"« In play » : le Shaper entre en jeu ENGAGE avec le premier joueur : {engages}"),
        ("sk229" in _en_jeu(monde), "« In play » : Cosmic Cube Creation entre en jeu"),
        ("sk229" not in deck and "sk228" not in deck, "ni l'un ni l'autre dans le deck rencontre"),
        (len(_fragments_de_cote(monde)) == 1, f"et un fragment par joueur de cote : {_fragments_de_cote(monde)}"),
    )


def v_ailleurs(monde):
    deck = _deck_rencontre(monde)
    return _verif(
        ("sk228" in deck, "« In another game area » : le Shaper est remelange au deck rencontre"),
        (deck.count("sk229") == 1, "Cosmic Cube Creation aussi"),
        (len(_fragments_de_cote(monde)) == 1, f"un fragment par joueur de cote : {_fragments_de_cote(monde)}"),
        ("sk228" not in _en_jeu(monde), "le Shaper n'est pas en jeu"),
    )


def v_cote_et_victoire(monde):
    return _verif(
        ("cartes de cote" in _ou(monde, "sk228"), f"« Set aside » : le Shaper est mis de cote : {_ou(monde, 'sk228')}"),
        (not _existe(monde, "sk229"), "« In the victory display » : Cosmic Cube Creation est RETIREE de la campagne (aucune carte creee)"),
        (not _fragments_de_cote(monde), f"et aucun fragment n'est mis de cote : {_fragments_de_cote(monde)}"),
    )


def v_cube_retire(monde):
    return _verif(
        (not _existe(monde, "sk229"), "Cosmic Cube Creation retiree : jamais recreee"),
        (not _fragments_de_cote(monde), "aucun fragment de cote"),
    )


CHAINES += [
    _chaine("Shaper « In play » + Cube « In play » (scenario 2) : tous deux en jeu, Shaper engage, un fragment de cote",
            {CLE_SHAPER: EN_JEU, CLE_CUBE: EN_JEU},
            [{"scenario": "sk_super_skrull", "verifier": v_en_jeu, "fin": "aucune"}]),
    _chaine("Shaper « In another game area » + Cube « In another game area » (scenario 3) : remelanges au deck rencontre",
            {CLE_SHAPER: AUTRE_ZONE, CLE_CUBE: AUTRE_ZONE},
            [{"scenario": "sk_paibok", "verifier": v_ailleurs, "fin": "aucune"}]),
    _chaine("Shaper « Set aside » + Cube « In the victory display » (scenario 2) : Cube retire, fragments : zone de cooperation",
            {CLE_SHAPER: MIS_DE_COTE, CLE_CUBE: PILE_VICTOIRE},
            [{"scenario": "sk_super_skrull", "verifier": v_cote_et_victoire, "fin": "Win",
              "carnet_attendu": {"gagnee": True, "scenario": "sk_super_skrull",
                                 "cles": {CLE_CUBE: RETIRE, CLE_SHAPER: MIS_DE_COTE, "Cooperation Area": "sk267;sk274"}}}]),
    _chaine("Cube « Removed from campaign » (scenario 4) : jamais recree",
            {CLE_SHAPER: MIS_DE_COTE, CLE_CUBE: RETIRE},
            [{"scenario": "sk_skrull_pantheon", "verifier": v_cube_retire, "fin": "aucune"}]),
]


# ================================================================== les Elites (p.10-17) ==
def _cle_elite(nom):
    return f"Skrull Elite: {nom}"


def v_elites_scenario3(monde):
    """Crusader (pile de victoire) quitte la campagne ; Jazinda (ailleurs) revient avec son ensemble ; une AUTRE
    Elite, jamais tiree, s'ajoute."""
    presentes = _elites_presentes(monde)
    autres = [n for n in presentes if n not in ("Jazinda", "Crusader")]
    return _verif(
        (not _existe(monde, "sk231"), "Crusader (pile de victoire) est retiree de la campagne : ni sbire ni ensemble"),
        ("Jazinda" in presentes and _ensemble_complet(monde, "Jazinda"), f"Jazinda (ailleurs) revient avec TOUT son ensemble : {presentes}"),
        (len(presentes) == 2 and len(autres) == 1, f"plus UNE nouvelle Elite jamais tiree : {presentes}"),
        (bool(autres) and _ensemble_complet(monde, autres[0]), "dont l'ensemble est complet"),
    )


def avant_elite_nouvelle_en_pile(monde):
    nouvelle = [n for n in _elites_presentes(monde) if n != "Jazinda"][0]
    MEMO["nouvelle"] = nouvelle
    return [f"Puzzle.MoveTo('{ELITES[nouvelle]}', 'VictoryDisplay')"]


MEMO = {}


def cv_elite_nouvelle_en_pile(suggestions, carnet):
    n = MEMO["nouvelle"]
    zone = _liste(suggestions.get("Cooperation Area"))
    return _verif(
        (suggestions.get(_cle_elite(n)) == PILE_VICTOIRE, f"{n} : {suggestions.get(_cle_elite(n))!r}"),
        (suggestions.get(_cle_elite("Jazinda")) == AUTRE_ZONE, f"Jazinda : {suggestions.get(_cle_elite('Jazinda'))!r}"),
        (suggestions.get(_cle_elite("Crusader")) == RETIRE, f"Crusader : {suggestions.get(_cle_elite('Crusader'))!r}"),
        (ALLIES[n] in zone and COMPLOTS[n] in zone, f"allie {ALLIES[n]} et complot {COMPLOTS[n]} de {n} dans la zone : {zone}"),
        ("sk265" in zone and "sk275" in zone, f"et Paibok + Skrull Military Training (scenario 3) : {zone}"),
        (ALLIES["Jazinda"] not in zone, "Jazinda n'est pas en pile de victoire : pas son allie"),
    )


def v_elites_scenario5(monde):
    presentes = sorted(_elites_presentes(monde))
    return _verif(
        (presentes == ["Jazinda", "Skymax", "Xavin"], f"Jazinda et Skymax (ailleurs) + Xavin (la restante) : {presentes}"),
        (not _existe(monde, "sk245") and not _existe(monde, "sk231"), "War Skrull et Crusader (pile de victoire) retirees"),
        (all(_ensemble_complet(monde, n) for n in presentes), "chaque ensemble complet"),
    )


def cv_elites_scenario5(suggestions, carnet):
    return _verif(
        (suggestions.get(_cle_elite("War Skrull")) == RETIRE, f"War Skrull retiree : {suggestions.get(_cle_elite('War Skrull'))!r}"),
        (suggestions.get(_cle_elite("Crusader")) == RETIRE, f"Crusader retiree : {suggestions.get(_cle_elite('Crusader'))!r}"),
    )


def v_elite_unique_par_scenario(monde):
    """Deux scenarios a la suite sans rien de nouveau a noter : une seule Elite tiree meme si 4 sont encore possibles."""
    return _verif((len(_elites_presentes(monde)) == 1, f"{_elites_presentes(monde)}"))


CHAINES += [
    _chaine("Elites — scenario 3 : l'Elite en pile de victoire quitte la campagne, celle laissee ailleurs revient, une nouvelle s'ajoute",
            {_cle_elite("Crusader"): PILE_VICTOIRE, _cle_elite("Jazinda"): AUTRE_ZONE,
             CLE_SHAPER: MIS_DE_COTE, CLE_CUBE: AUTRE_ZONE},
            [{"scenario": "sk_paibok", "verifier": v_elites_scenario3, "avant": avant_elite_nouvelle_en_pile,
              "carnet_verifier": cv_elite_nouvelle_en_pile, "fin": "Win"}]),
    _chaine("Elites — scenario 5 : « the remaining » Elite + celles laissees ailleurs ; celles en pile de victoire retirees",
            {_cle_elite("Crusader"): PILE_VICTOIRE, _cle_elite("Jazinda"): AUTRE_ZONE, _cle_elite("Skymax"): AUTRE_ZONE,
             _cle_elite("War Skrull"): PILE_VICTOIRE, CLE_SHAPER: MIS_DE_COTE, CLE_CUBE: RETIRE},
            [{"scenario": "sk_secret_invasion", "verifier": v_elites_scenario5, "carnet_verifier": cv_elites_scenario5,
              "fin": "Win"}]),
    _chaine("Elites — scenario 4 avec trois Elites deja tirees : une seule nouvelle, parmi les deux jamais tirees",
            {_cle_elite("Crusader"): RETIRE, _cle_elite("Jazinda"): RETIRE, _cle_elite("Skymax"): RETIRE,
             CLE_SHAPER: MIS_DE_COTE, CLE_CUBE: RETIRE},
            [{"scenario": "sk_skrull_pantheon",
              "verifier": lambda monde: _verif((sorted(_elites_presentes(monde)) in (["War Skrull"], ["Xavin"]),
                                                f"une des deux Elites jamais tirees : {_elites_presentes(monde)}")),
              "fin": "aucune"}]),
]


# ============================================================= la zone de cooperation ==
ZONE_TEST = "sk263;sk264;sk270;sk271;sk277;sk283;sk284;sk230a;sk230b"


def _dans_les_mains(monde, i=0):
    return [_id(f) for f in monde.players[i].hand_cards.Get(True)]


def _possede(monde, i=0):
    """Deck + main + defausse du joueur : ou qu'une carte de la zone ait atterri au tirage de depart."""
    return set(_deck_joueur(monde, i)) | set(_dans_les_mains(monde, i)) | set(_defausse_joueur(monde, i))


def v_zone_premieres(monde):
    p = _possede(monde)
    voulues = {"sk263", "sk270", "sk230a", "sk277", "sk283"}
    refusees = {"sk264", "sk271", "sk230b", "sk284"}
    return _verif(
        (voulues <= p, f"une carte de CHAQUE type melangee au deck : manque {sorted(voulues - p)}"),
        (not (refusees & p), f"pas les autres : {sorted(refusees & p)}"),
    )


def v_zone_choisies(monde):
    p = _possede(monde)
    return _verif(
        ({"sk264", "sk271"} <= p, f"le pilote a choisi Jazinda et Cloning Faux Pas : {sorted(p & {'sk263','sk264','sk270','sk271'})}"),
        (not ({"sk263", "sk270"} & p), "et pas les premieres"),
    )


def v_zone_refus(monde):
    zone = set(ZONE_TEST.split(";"))
    return _verif((not (zone & _possede(monde)), f"« Cancel » partout : aucune carte de la zone dans le deck : {sorted(zone & _possede(monde))}"))


def v_zone_deux_joueurs(monde):
    a, b = _possede(monde, 0), _possede(monde, 1)
    return _verif(
        ({"sk263", "sk277"} <= a, f"le premier joueur prend les deux : {sorted(a & {'sk263', 'sk277'})}"),
        (not ({"sk263", "sk277"} & b), "une carte unique ne va que dans UN deck : le second joueur ne les voit plus"),
    )


def cv_zone_rendue(suggestions, carnet):
    zone = _liste(suggestions.get("Cooperation Area"))
    attendus = set(ZONE_TEST.split(";")) | {"sk267", "sk274"}
    return _verif((set(zone) == attendus, f"la zone est RENDUE intacte apres la partie, plus les ajouts du scenario 2 : {zone}"))


CHAINES += [
    _chaine("zone de cooperation — scenario 2 : chaque joueur melange UNE carte de chaque type (le pilote prend la premiere)",
            {"Cooperation Area": ZONE_TEST, CLE_SHAPER: MIS_DE_COTE, CLE_CUBE: RETIRE},
            [{"scenario": "sk_super_skrull", "verifier": v_zone_premieres,
              "questions_attendues": ["Crusader", "Jazinda", "Buddy Training Program", "Cosmic Cube Fragment", "Antalya", "3-D Man's Goggles"],
              "carnet_verifier": cv_zone_rendue, "fin": "Win"}]),
    _chaine("zone de cooperation — le joueur CHOISIT (Jazinda, Cloning Faux Pas)",
            {"Cooperation Area": ZONE_TEST, CLE_SHAPER: MIS_DE_COTE, CLE_CUBE: RETIRE},
            [{"scenario": "sk_paibok", "verifier": v_zone_choisies, "preferer": ["Jazinda", "Cloning Faux Pas"], "fin": "aucune"}]),
    _chaine("zone de cooperation — « Cancel » partout : rien n'entre dans le deck",
            {"Cooperation Area": ZONE_TEST, CLE_SHAPER: MIS_DE_COTE, CLE_CUBE: RETIRE},
            [{"scenario": "sk_skrull_pantheon", "verifier": v_zone_refus, "preferer": ["Cancel"], "fin": "aucune"}]),
    _chaine("zone de cooperation — a DEUX joueurs, une carte unique ne va que dans le deck du premier",
            {"Cooperation Area": "sk263;sk277", CLE_SHAPER: MIS_DE_COTE, CLE_CUBE: RETIRE},
            [{"scenario": "sk_super_skrull", "verifier": v_zone_deux_joueurs, "fin": "aucune"}],
            heros=("lyja", "spider_man")),
    _chaine("zone de cooperation — scenario 1 : AUCUNE carte de la zone n'est proposee (elle n'existe pas encore)",
            {"Cooperation Area": ZONE_TEST},
            [{"scenario": "sk_skrull_empire", "verifier": v_zone_refus, "questions_absentes": ["Crusader", "Antalya"], "fin": "aucune"}]),
]


# ===================================== la regle de cooperation : vaincre = pile de victoire (p.6) ==
BASE = {}
TUEUR = "Puzzle.FindFaceInPlay('sk037b')"     # l'identite de Lyja (alter ego) : un joueur qui vainc


def _avant(commandes, vider_deck=False):
    """Releve la taille du deck et de la defausse AVANT le coup, puis rend les commandes."""
    def f(monde):
        BASE["deck"] = len(monde.players[0].player_deck.Get(True))
        BASE["defausse"] = len(monde.players[0].discard_pile.Get(True))
        return (["Puzzle.EmptyPlayerDeck()"] if vider_deck else []) + list(commandes)
    return f


def _defausse_rencontre(monde):
    from game.operate.worlds import Worlds
    return [_id(f) for f in Worlds.GetEncounterDiscardPileCards(monde)]


def vf_cooperation_acceptee(monde):
    taille = len(monde.players[0].player_deck.Get(True))
    return _verif(
        ("sk110" in _victoire(monde), f"le sbire vaincu est dans la pile de victoire : {_victoire(monde)}"),
        ("sk110" not in _defausse_rencontre(monde), "et pas dans la defausse rencontre"),
        (taille == BASE["deck"] - 1, f"le dessus du deck a ete defausse : {taille} carte(s) (avant : {BASE['deck']})"),
        (len(monde.players[0].discard_pile.Get(True)) == BASE["defausse"] + 1, "la carte defaussee est dans la defausse du joueur"),
    )


def vf_cooperation_refusee(monde):
    taille = len(monde.players[0].player_deck.Get(True))
    return _verif(
        ("sk110" not in _victoire(monde), "refus : pas dans la pile de victoire"),
        ("sk110" in _defausse_rencontre(monde), f"refus : defausse rencontre habituelle : {_defausse_rencontre(monde)[:8]}"),
        (taille == BASE["deck"], f"refus : le deck n'a pas bouge : {taille} (avant : {BASE['deck']})"),
    )


def vf_sans_joueur(monde):
    taille = len(monde.players[0].player_deck.Get(True))
    return _verif(
        ("sk110" not in _victoire(monde), "vaincu par personne (degats sans source) : aucune cooperation proposee"),
        (taille == BASE["deck"], f"et le deck n'a pas bouge : {taille} (avant : {BASE['deck']})"),
    )


def vf_victory_x(monde):
    taille = len(monde.players[0].player_deck.Get(True))
    return _verif(
        ("sk231" in _victoire(monde), "Crusader (Victory 1) va dans la pile de victoire de toute facon"),
        (taille == BASE["deck"], f"sans rien defausser : {taille} (avant : {BASE['deck']})"),
    )


def vf_complot(monde):
    taille = len(monde.players[0].player_deck.Get(True))
    return _verif(
        ("sk101" in _victoire(monde), f"un complot annexe vaincu : lui aussi peut aller en pile de victoire : {_victoire(monde)}"),
        (taille == BASE["deck"] - 1, f"pour le dessus du deck : {taille} (avant : {BASE['deck']})"),
    )


def vf_deck_vide(monde):
    return _verif(
        ("sk110" not in _victoire(monde), "deck VIDE : on ne peut rien defausser, rien n'est propose"),
        ("sk110" in _defausse_rencontre(monde), "le sbire part a la defausse"),
    )


def vf_revealed(monde):
    taille = len(monde.players[0].player_deck.Get(True))
    return _verif(
        ("sk208b" not in _victoire(monde), "FAQ p.21 : un sbire REVEALED ne va jamais en pile de victoire"),
        (taille == BASE["deck"], f"et rien n'a ete propose ni defausse : {taille} (avant : {BASE['deck']})"),
    )


TUER_SBIRE = ["Puzzle.PutIntoPlay('sk110')", f"Puzzle.Damage(Puzzle.FindFaceInPlay('sk110'), 50, {TUEUR})"]

CHAINES += [
    _chaine("cooperation — un joueur vainc un sbire : il defausse le dessus de son deck, le sbire va en pile de victoire",
            {}, [{"scenario": "sk_skrull_empire", "avant": _avant(TUER_SBIRE), "verifier_fin": vf_cooperation_acceptee}]),
    _chaine("cooperation — le joueur REFUSE (Cancel) : defausse rencontre habituelle, deck intact",
            {}, [{"scenario": "sk_skrull_empire", "avant": _avant(TUER_SBIRE), "preferer": ["Cancel"],
                  "verifier_fin": vf_cooperation_refusee}]),
    _chaine("cooperation — sbire vaincu par personne (degats sans source) : rien n'est propose",
            {}, [{"scenario": "sk_skrull_empire",
                  "avant": _avant(["Puzzle.PutIntoPlay('sk110')", "Puzzle.Damage(Puzzle.FindFaceInPlay('sk110'), 50)"]),
                  "verifier_fin": vf_sans_joueur}]),
    _chaine("cooperation — Victory X : le sbire y va de lui-meme, sans rien defausser",
            {}, [{"scenario": "sk_skrull_empire",
                  "avant": _avant(["Puzzle.PutIntoPlay('sk231')", f"Puzzle.Damage(Puzzle.FindFaceInPlay('sk231'), 50, {TUEUR})"]),
                  "verifier_fin": vf_victory_x}]),
    _chaine("cooperation — complot annexe contre par un joueur : pile de victoire pour le dessus du deck",
            {}, [{"scenario": "sk_skrull_empire",
                  "avant": _avant(["Puzzle.ChangeToFace('sk037b', 'sk037a')", "Puzzle.PutIntoPlay('sk101')",
                                   "Puzzle.SetThreat(Puzzle.FindFaceInPlay('sk101'), 1)", "Puzzle.Thwart('sk037a')"]),
                  "cibles": ["sk101"], "verifier_fin": vf_complot}]),
    _chaine("cooperation — deck VIDE : rien a defausser, rien n'est propose",
            {}, [{"scenario": "sk_skrull_empire", "avant": _avant(TUER_SBIRE, vider_deck=True),
                  "verifier_fin": vf_deck_vide}]),
    _chaine("cooperation — scenario 5 : un sbire REVEALED vaincu ne va PAS en pile de victoire (FAQ p.21)",
            {}, [{"scenario": "sk_secret_invasion",
                  "avant": _avant(["Puzzle.PutIntoPlay('sk208b')", f"Puzzle.Damage(Puzzle.FindFaceInPlay('sk208b'), 50, {TUEUR})"]),
                  "verifier_fin": vf_revealed}]),
]


# ============================================================ la campagne EXPERTE (p.6) ==
CLE_PV = "Player 1 Remaining hit points"


def _identite(monde, i=0):
    return monde.const_seat_order_players[i].GetIdentity()


def _tokens_acceleration(monde):
    from game.operate.worlds import Worlds
    return sum(s.GetTokens("acceleration_token") for s in Worlds.GetAllMainSchemes(monde))


def v_pv_gueris(monde):
    ident = _identite(monde)
    return _verif(
        (ident.health == ident.max_health, f"soin accepte : PV au complet ({ident.health}/{ident.max_health})"),
        (_tokens_acceleration(monde) == 1, f"un pion Acceleration sur la manigance principale : {_tokens_acceleration(monde)}"),
    )


def v_pv_restants(monde):
    ident = _identite(monde)
    return _verif(
        (ident.health == ident.max_health - 4, f"PV de depart = PV restants (6) : {ident.health}/{ident.max_health}"),
        (_tokens_acceleration(monde) == 0, f"soin refuse : aucun pion : {_tokens_acceleration(monde)}"),
    )


def v_pv_standard(monde):
    ident = _identite(monde)
    return _verif(
        (ident.health == ident.max_health, f"campagne STANDARD : les PV restants ne comptent pas : {ident.health}/{ident.max_health}"),
        (_tokens_acceleration(monde) == 0, "et aucun soin n'est propose"),
    )


def avant_degats_4(monde):
    return ["Puzzle.Damage(Puzzle.FindFaceInPlay('sk037b'), 4)"]


def v_pv_apres_degats(monde):
    ident = _identite(monde)
    return _verif((ident.health == ident.max_health - 4, f"fin du scenario 1 avec 4 degats : {ident.health}/{ident.max_health}"))


CHAINES += [
    _chaine("expert — 2 scenarios : PV restants reportes (10 - 4 = 6), le joueur les soigne d'un pion Acceleration",
            {},
            [{"scenario": "sk_skrull_empire_expert", "avant": avant_degats_4, "verifier_fin": v_pv_apres_degats,
              "carnet_reporte_attendu": {CLE_PV: "6"}},
             {"scenario": "sk_super_skrull_expert", "questions_attendues": ["Place 1 acceleration token"],
              "verifier": v_pv_gueris, "fin": "aucune"}]),
    _chaine("expert — le joueur REFUSE le soin : il commence le scenario avec ses PV restants",
            {CLE_PV: "6", CLE_SHAPER: MIS_DE_COTE, CLE_CUBE: RETIRE},
            [{"scenario": "sk_super_skrull_expert", "preferer": ["Cancel"], "verifier": v_pv_restants, "fin": "aucune"}]),
    _chaine("expert — TEMOIN campagne standard : les PV restants du carnet ne s'appliquent pas",
            {CLE_PV: "6", CLE_SHAPER: MIS_DE_COTE, CLE_CUBE: RETIRE},
            [{"scenario": "sk_super_skrull", "verifier": v_pv_standard, "questions_absentes": ["Place 1 acceleration token"],
              "fin": "aucune"}]),
]


def avant_elimine(monde):
    """Le joueur 2 est vaincu pendant la partie, ses coequipiers gagnent."""
    ident = _identite(monde, 1)
    return [f"Puzzle.Damage(Puzzle.FindFaceInPlay('{ident.paper.card_id}'), 99)"]


def v_elimine_revient(monde):
    p2 = monde.const_seat_order_players[1]
    return _verif(
        (not p2.is_eliminated, "le joueur elimine REVIENT en payant un pion Acceleration"),
        (p2.GetIdentity().health == p2.GetIdentity().max_health, f"a pleins PV : {p2.GetIdentity().health}/{p2.GetIdentity().max_health}"),
        (_tokens_acceleration(monde) == 1, f"un pion sur la manigance principale : {_tokens_acceleration(monde)}"),
    )


def v_elimine_reste(monde):
    return _verif((monde.const_seat_order_players[1].is_eliminated, "il refuse le pion : il ne joue pas ce scenario"),
                  (not monde.const_seat_order_players[0].is_eliminated, "et son coequipier joue"))


def vf_elimine_note(monde):
    return _verif((monde.const_seat_order_players[1].is_eliminated, "le joueur 2 a bien ete elimine pendant la partie"))


CHAINES += [
    _chaine("expert — un joueur ELIMINE au scenario 1 revient au scenario 2 (pion Acceleration)",
            {},
            [{"scenario": "sk_skrull_empire_expert", "avant": avant_elimine, "verifier_fin": vf_elimine_note,
              "carnet_reporte_attendu": {"Eliminated Players": "2"}},
             {"scenario": "sk_super_skrull_expert", "questions_attendues": ["rejoin the team"],
              "verifier": v_elimine_revient, "fin": "aucune"}],
            heros=("lyja", "spider_man")),
    _chaine("expert — un joueur elimine qui REFUSE le pion ne joue pas le scenario suivant",
            {"Eliminated Players": "2", CLE_SHAPER: MIS_DE_COTE, CLE_CUBE: RETIRE},
            [{"scenario": "sk_super_skrull_expert", "preferer": ["Cancel"], "verifier": v_elimine_reste, "fin": "aucune"}],
            heros=("lyja", "spider_man")),
]


# ============================== LA CAMPAGNE ENTIERE : 5 scenarios a la suite, l'etat reporte ==
def _zone_du_carnet(suggestions):
    return set(_liste(suggestions.get("Cooperation Area")))


def _progres_du_carnet(suggestions):
    return set(_liste(suggestions.get("Cooperation Progress")))


def _victoire_de(*ids):
    return lambda monde: [f"Puzzle.MoveTo('{i}', 'VictoryDisplay')" for i in ids]


# --- scenario 1 : Skrull Empire
def v_c1(monde):
    elites = _elites_presentes(monde)
    MEMO["e1"] = elites[0] if elites else None
    return _verif((len(elites) == 1, f"scenario 1 : UNE Elite tiree : {elites}"))


def avant_c1(monde):
    return [f"Puzzle.MoveTo('{i}', 'VictoryDisplay')" for i in ("sk107", "sk108", "sk109", "sk110", ELITES[MEMO["e1"]])]


def cv_c1(s, carnet):
    e1 = MEMO["e1"]
    zone, progres = _zone_du_carnet(s), _progres_du_carnet(s)
    reverting = {f"Reverting Device: {x}" for x in ("Skrull Spy", "Skrull Scientist", "Skrull Warrior", "Skrull Telepath")}
    return _verif(
        (reverting <= progres, f"Spy + Scientist + Warrior + Telepath en pile de victoire : Reverting Device complet : {sorted(progres)}"),
        ({"sk286", ALLIES[e1], COMPLOTS[e1]} <= zone, f"zone : Reverting Device + allie et complot de {e1} : {sorted(zone)}"),
        (s.get(_cle_elite(e1)) == PILE_VICTOIRE, f"{e1} en pile de victoire : {s.get(_cle_elite(e1))!r}"),
        (s.get(CLE_SHAPER) == MIS_DE_COTE, f"Shaper mis de cote : {s.get(CLE_SHAPER)!r}"),
        (s.get(CLE_CUBE) == AUTRE_ZONE, f"Cube ailleurs (deck rencontre) : {s.get(CLE_CUBE)!r}"),
        (not (zone & {"sk267", "sk274", "sk265", "sk275"}), "le scenario 1 n'ajoute ni Super-Skrull ni Paibok"),
    )


# --- scenario 2 : Super-Skrull
def v_c2(monde):
    e1 = MEMO["e1"]
    elites = _elites_presentes(monde)
    nouvelle = [n for n in elites if n != e1]
    MEMO["e2"] = nouvelle[0] if nouvelle else None
    p = _possede(monde)
    deck = _deck_rencontre(monde)
    return _verif(
        (e1 not in elites, f"{e1} (pile de victoire) a quitte la campagne : {elites}"),
        (len(elites) == 1 and len(nouvelle) == 1, f"UNE nouvelle Elite : {elites}"),
        ({"sk286", ALLIES[e1], COMPLOTS[e1]} <= p, f"les cartes de la zone sont au deck : manque {sorted({'sk286', ALLIES[e1], COMPLOTS[e1]} - p)}"),
        ("sk229" in deck, "le Cube (« In another game area ») est remelange au deck rencontre"),
        (len(_fragments_de_cote(monde)) == 1, "un fragment par joueur de cote"),
    )


def avant_c2(monde):
    e2 = MEMO["e2"]
    return [f"Puzzle.MoveTo('{i}', 'VictoryDisplay')"
            for i in ("sk229", "sk108", "sk110", "sk114", "sk113", ELITES[e2])]


def cv_c2(s, carnet):
    e1, e2 = MEMO["e1"], MEMO["e2"]
    zone, progres = _zone_du_carnet(s), _progres_du_carnet(s)
    kill_crew = {f"Skrull Kill Crew: {x}" for x in ("Skrull Spy", "Skrull Warrior", "Skrull Soldier", "Skrull Commander")}
    return _verif(
        (kill_crew <= progres, f"Spy + Warrior + Soldier + Commander : Skrull Kill Crew complet : {sorted(progres)}"),
        ("Cosmic Cube Fragment: Cosmic Cube Creation" in progres, "Cosmic Cube Creation en pile : case de la ligne des fragments cochee"),
        (set(FRAGMENTS) <= zone, f"et les QUATRE fragments dans la zone (FAQ p.21) : {sorted(zone)}"),
        ({"sk282", "sk267", "sk274", ALLIES[e2], COMPLOTS[e2], "sk286", ALLIES[e1], COMPLOTS[e1]} <= zone,
         f"Skrull Kill Krew, Super-Skrull + Searching for Powers (scenario 2), allie et complot de {e2} : {sorted(zone)}"),
        (s.get(CLE_CUBE) == PILE_VICTOIRE, f"Cube en pile de victoire : {s.get(CLE_CUBE)!r}"),
        (s.get(_cle_elite(e2)) == PILE_VICTOIRE, f"{e2} en pile de victoire : {s.get(_cle_elite(e2))!r}"),
    )


# --- scenario 3 : Paibok
def v_c3(monde):
    e1, e2 = MEMO["e1"], MEMO["e2"]
    elites = _elites_presentes(monde)
    nouvelle = [n for n in elites if n not in (e1, e2)]
    MEMO["e3"] = nouvelle[0] if nouvelle else None
    p = _possede(monde)
    return _verif(
        (e1 not in elites and e2 not in elites, f"{e1} et {e2} ont quitte la campagne : {elites}"),
        (len(elites) == 1 and len(nouvelle) == 1, f"UNE nouvelle Elite : {elites}"),
        (not _existe(monde, "sk229"), "Cosmic Cube Creation (pile de victoire au scenario 2) a quitte la campagne"),
        (not _fragments_de_cote(monde), "donc aucun fragment de cote"),
        ({"sk230a", "sk282", "sk286"} <= p, f"ressource, soutien et amelioration de la zone au deck : manque {sorted({'sk230a','sk282','sk286'} - p)}"),
        (len(p & {ALLIES[e1], ALLIES[e2], "sk267"}) == 1, f"UN allie de la zone : {sorted(p & {ALLIES[e1], ALLIES[e2], 'sk267'})}"),
        (len(p & {COMPLOTS[e1], COMPLOTS[e2], "sk274"}) == 1, f"UN complot annexe de joueur de la zone : {sorted(p & {COMPLOTS[e1], COMPLOTS[e2], 'sk274'})}"),
    )


def cv_c3(s, carnet):
    e3 = MEMO["e3"]
    zone = _zone_du_carnet(s)
    return _verif(
        (s.get(_cle_elite(e3)) == AUTRE_ZONE, f"{e3} pas vaincue : {s.get(_cle_elite(e3))!r}"),
        ({"sk265", "sk275"} <= zone, f"Paibok + Skrull Military Training (scenario 3) : {sorted(zone)}"),
        (ALLIES[e3] not in zone, f"{e3} pas en pile de victoire : son allie n'est pas ajoute"),
        (s.get(CLE_CUBE) == RETIRE, f"Cube retire de la campagne : {s.get(CLE_CUBE)!r}"),
        (s.get(_cle_elite(MEMO['e1'])) == RETIRE and s.get(_cle_elite(MEMO['e2'])) == RETIRE, "les deux premieres Elites retirees"),
    )


# --- scenario 4 : Skrull Pantheon
def v_c4(monde):
    e1, e2, e3 = MEMO["e1"], MEMO["e2"], MEMO["e3"]
    elites = _elites_presentes(monde)
    nouvelle = [n for n in elites if n not in (e1, e2, e3)]
    MEMO["e4"] = nouvelle[0] if nouvelle else None
    return _verif(
        (e3 in elites and _ensemble_complet(monde, e3), f"{e3} (laissee ailleurs au scenario 3) REVIENT avec son ensemble : {elites}"),
        (len(elites) == 2 and len(nouvelle) == 1, f"plus UNE nouvelle : {elites}"),
        (e1 not in elites and e2 not in elites, "les deux premieres restent retirees"),
    )


def avant_c4(monde):
    return [f"Puzzle.MoveTo('{ELITES[MEMO['e4']]}', 'VictoryDisplay')"]


def cv_c4(s, carnet):
    e3, e4 = MEMO["e3"], MEMO["e4"]
    zone = _zone_du_carnet(s)
    return _verif(
        (s.get(_cle_elite(e4)) == PILE_VICTOIRE and s.get(_cle_elite(e3)) == AUTRE_ZONE, f"{e4} vaincue, {e3} toujours debout"),
        ({ALLIES[e4], COMPLOTS[e4]} <= zone and ALLIES[e3] not in zone, f"allie et complot de {e4} seulement : {sorted(zone)}"),
        ("sk265" in zone and "sk275" in zone and "sk267" in zone, "la zone garde ce que les scenarios precedents y ont mis"),
    )


# --- scenario 5 : Secret Invasion
def v_c5(monde):
    e1, e2, e3, e4 = MEMO["e1"], MEMO["e2"], MEMO["e3"], MEMO["e4"]
    elites = _elites_presentes(monde)
    restante = [n for n in ELITES if n not in (e1, e2, e3, e4)]
    return _verif(
        (len(restante) == 1, f"quatre Elites distinctes tirees en quatre scenarios : {[e1, e2, e3, e4]}"),
        (sorted(elites) == sorted([e3] + restante), f"{e3} (ailleurs) + « the remaining » {restante} : {elites}"),
        (e4 not in elites, f"{e4} (pile de victoire au scenario 4) a quitte la campagne"),
    )


CHAINES += [
    _chaine("CAMPAGNE ENTIERE (standard, solo) — 5 scenarios a la suite : zone, tableau, Elites, Cube, fragments",
            {},
            [{"scenario": "sk_skrull_empire", "verifier": v_c1, "avant": avant_c1, "carnet_verifier": cv_c1,
              "carnet_attendu": {"gagnee": True, "scenario": "sk_skrull_empire"}},
             {"scenario": "sk_super_skrull", "verifier": v_c2, "avant": avant_c2, "carnet_verifier": cv_c2,
              "carnet_attendu": {"gagnee": True, "scenario": "sk_super_skrull"}},
             {"scenario": "sk_paibok", "verifier": v_c3, "avant": _victoire_de("sk111", "sk115"), "carnet_verifier": cv_c3,
              "carnet_attendu": {"gagnee": True, "scenario": "sk_paibok"}},
             {"scenario": "sk_skrull_pantheon", "verifier": v_c4, "avant": avant_c4, "carnet_verifier": cv_c4,
              "carnet_attendu": {"gagnee": True, "scenario": "sk_skrull_pantheon"}},
             {"scenario": "sk_secret_invasion", "verifier": v_c5,
              "carnet_attendu": {"gagnee": True, "scenario": "sk_secret_invasion"}}]),
]


def avant_pv_au_dessus_de_la_base(monde):
    """Simule « +3 hit points » (Sy-Torak Gem) : PV max et PV courants a 13 pour une base de 10."""
    ident = _identite(monde)
    ident.components.health.SetMaxHealth(ident.printed_health + 3)
    ident.components.health.SetHealth(ident.printed_health + 3)
    BASE["pv_base"] = ident.printed_health
    return []


def vf_pv_depasses(monde):
    ident = _identite(monde)
    return _verif((ident.health == BASE["pv_base"] + 3, f"la partie finit bien AU-DESSUS de la base : {ident.health} (base {BASE['pv_base']})"))


CHAINES += [
    _chaine("expert — PV restants PLAFONNES aux PV de base (13 sur une base de 10 : on note 10)",
            {},
            [{"scenario": "sk_skrull_empire_expert", "avant": avant_pv_au_dessus_de_la_base, "verifier_fin": vf_pv_depasses,
              "carnet_reporte_attendu": {CLE_PV: "10"}}]),
]
