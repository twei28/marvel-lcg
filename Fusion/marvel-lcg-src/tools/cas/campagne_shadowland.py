# Cas test_capacites de la CAMPAGNE « Shadowland » (livret FR, docs/packs/shadowland/livret-fr.md) : mise en place des trois scenarios en mode campagne
# (`src/cards/pack/shadowland/campaign.py`), exclusion des Sombres Proteges retires, carnet SORTANT. Prefixe `[slcamp]`.
# Les trois scenarios REELS (`shadows_in_the_night`, `shadow_labyrinth`, `heart_of_shadow`), `campagne: True`, carnet entrant dans `carnet`. Spider-Man, 1 joueur.
# Le pilote du harnais accepte toujours la PREMIERE option : un « peut choisir » (carte inscrite, soin expert) est donc pris quand il est offert.
S1, S2, S3 = "shadows_in_the_night", "shadow_labyrinth", "heart_of_shadow"
BLACK_FLOWER = ["sl073", "sl074", "sl075", "sl076", "sl077", "sl078"]
FORME_HEROS = "Puzzle.ChangeForm('01001b')"


def _c(nom, pourquoi, scenario, attendu, carnet=None, mise=(), declencher=(), verifier="slcamp_etat", **cle):
    cas = {"nom": "[slcamp] " + nom, "pourquoi": pourquoi, "scenario": scenario, "heros": cle.pop("heros", "spider_man"), "campagne": True,
           "carnet": carnet or {}, "mise_en_place": ["Puzzle.EmptyHand()", *mise], "declencher": list(declencher), "verifier": verifier, "attendu": attendu,
           "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


CAS = [
    # ---------------------------------------------------------------- scenario 1 : Des Ombres dans la Nuit
    _c("S1 mise en place : la Corruption Insidieuse (face A) du joueur est EN JEU", "livret p. 9 : « chaque joueur met en jeu sous son controle une Corruption Insidieuse (72A) »",
       S1, {"en_jeu": ["sl072a"]}),
    _c("S1 mise en place : les cartes du set Black Flower sont melangees au deck de rencontre", "livret p. 9 : « melangez dans le deck Rencontre chaque autre carte de ce set modulaire »",
       S1, {"black_flower_dans_le_deck": True}),
    _c("S1 mise en place : 1 menace supplementaire par joueur sur la maniganc principale (3 pour 1 joueur)", "livret p. 9 : « placez 1 menace supplementaire par joueur »",
       S1, {"menace": [["sl001b", 3]]}),
    _c("S1 mise en place a 2 joueurs : 2 menaces supplementaires (6 en tout)", "PAR joueur", S1, {"menace": [["sl001b", 6]]}, heros2="spider_man"),
    _c("S1 mise en place, 2 joueurs : une Corruption Insidieuse CHACUN", "une par joueur, jamais une partagee", S1, {"corruptions": [[0, 0], [1, 0]]}, heros2="spider_man"),
    _c("S1 HORS campagne, TEMOIN : aucune Corruption, aucune carte Black Flower, menace imprimee (2)", "la mise en place de campagne ne part qu'en mode campagne",
       S1, {"hors_jeu": ["sl072a"], "menace": [["sl001b", 2]], "black_flower_dans_le_deck": False}, campagne=False),
    _c("S1 : les cartes liees a un vilain retire n'entrent pas dans le deck de rencontre", "seul le vilain tire a ses cartes liees melangees",
       S1, {"vilain_parmi": ["sl012", "sl013", "sl016", "sl017"]}, carnet={"Dark Protege Removed": "sl014a;sl015a"}),
    _c("S1 hors campagne avec Daredevil, TEMOIN : le tirage est libre (Daredevil peut sortir)", "hors campagne, aucun retrait",
       S1, {"vilain_parmi": ["sl012", "sl013", "sl014", "sl015", "sl016", "sl017"]}, heros="daredevil", campagne=False),
    # ---------------------------------------------------------------- scenario 2 : Le Labyrinthe des Ombres
    _c("S2 mise en place : Corruption Insidieuse en jeu, 0 jeton (carnet vierge), 3 menaces par joueur en plus (28)", "livret p. 14 : « placez 3 menaces supplementaires par joueur »",
       S2, {"en_jeu": ["sl072a"], "corruptions": [[0, 0]], "menace": [["sl038b", 28]]}),
    _c("S2 : Corruption INSOUTENABLE au scenario 1 -> 1 jeton Corruption", "livret p. 14 : « chaque joueur dont la Corruption avait le trait INSOUTENABLE place 1 jeton »",
       S2, {"corruptions": [[0, 1]]}, carnet={"Player 1 Overpowering Scenario 1": "1"}),
    _c("S2 : la carte inscrite (01006 Aunt May, dans le deck) entre en jeu SOUS CONTROLE et coute 1 jeton Corruption", "livret p. 14 : « choisir son exemplaire de la carte inscrite, la mettre en jeu, 1 jeton »",
       S2, {"en_jeu": ["01006"], "corruptions": [[0, 1]]}, carnet={"Player 1 Recorded Card 1": "01006"}),
    _c("S2 : carte inscrite ET Corruption insoutenable : 2 jetons", "les deux effets s'ajoutent", S2, {"en_jeu": ["01006"], "corruptions": [[0, 2]]},
       carnet={"Player 1 Overpowering Scenario 1": "1", "Player 1 Recorded Card 1": "01006"}),
    _c("S2 : une carte inscrite qui n'est PAS dans le deck (01033 Pepper Potts) : rien a mettre en jeu, aucun jeton", "pas d'exemplaire, pas de choix", S2, {"hors_jeu": ["01033"], "corruptions": [[0, 0]]},
       carnet={"Player 1 Recorded Card 1": "01033"}),
    # ---------------------------------------------------------------- scenario 3 : Coeur d'Ombre
    _c("S3 : jetons Corruption = nombre de scenarios ou elle etait insoutenable (S1 et S2 -> 2)", "livret p. 17 : « 1 jeton pour chaque fois que la Corruption a eu le trait INSOUTENABLE »",
       S3, {"corruptions": [[0, 2]]}, carnet={"Player 1 Overpowering Scenario 1": "1", "Player 1 Overpowering Scenario 2": "1"}),
    _c("S3 : les deux cartes inscrites entrent en jeu, 1 jeton chacune (+ 1 insoutenable = 3)", "livret p. 17 : « chaque carte ainsi mise en jeu : 1 jeton »",
       S3, {"en_jeu": ["01006", "01008"], "corruptions": [[0, 3]]},
       carnet={"Player 1 Overpowering Scenario 2": "1", "Player 1 Recorded Card 1": "01006", "Player 1 Recorded Card 2": "01008"}),
    _c("S3 : un des quatre sbires Sombres Proteges est attribue au joueur FACE CACHEE, les trois autres sont melanges au deck de rencontre", "livret p. 17",
       S3, {"sbires_sombres_proteges": True}),
    _c("S3 a 2 joueurs : un sbire face cachee chacun, deux dans le deck de rencontre", "un sbire PAR joueur", S3, {"sbires_sombres_proteges": True}, heros2="spider_man"),
    _c("S3 HORS campagne, TEMOIN : aucun sbire Sombres Proteges", "pas de mise en place de campagne", S3, {"aucun_sbire_sombres_proteges": True}, campagne=False),
    # ---------------------------------------------------------------- campagne experte
    _c("S2 expert : les PV restants du carnet (4) sont reportes ; le joueur se soigne en s'attribuant une carte Rencontre face cachee (le pilote accepte)", "livret p. 14 : PV restants puis soin possible",
       "shadow_labyrinth_expert", {"expert_pv_reportes_ou_soignes": 4}, carnet={"Player 1 Remaining hit points": "4"}),
    # ---------------------------------------------------------------- carnet SORTANT
    _c("S1 victoire : le vilain tire est inscrit « retire de la campagne » au carnet sortant", "livret p. 9 : « cochez le nom du mechant utilise »",
       S1, {"gagnee": True, "scenario": "shadows_in_the_night", "cles_presentes": ["Dark Protege Removed"]}, declencher=["Puzzle.Win()"], verifier="fnefin_carnet_sortant"),
    _c("S1 victoire avec une Corruption INSOUTENABLE (retournee) : « Player 1 Overpowering Scenario 1 » = 1", "livret p. 9 : « chaque joueur precise si sa Corruption a le trait INSOUTENABLE »",
       S1, {"gagnee": True, "cles": {"Player 1 Overpowering Scenario 1": "1"}}, mise=["Puzzle.Counter('sl072a', 'corruption', 5)"], declencher=["Puzzle.Win()"], verifier="fnefin_carnet_sortant"),
    _c("S1 victoire, Corruption ordinaire (face A) : AUCUNE cle « Overpowering » au carnet", "case non cochee = cle absente (jamais « 0 »)",
       S1, {"gagnee": True, "cles_absentes": ["Player 1 Overpowering Scenario 1"]}, declencher=["Puzzle.Win()"], verifier="fnefin_carnet_sortant"),
    _c("S1 DEFAITE : rien n'est coche (ni vilain retire, ni insoutenable) : on rejoue sans penalite", "livret p. 5 : « les joueurs peuvent reinitialiser le scenario et reessayer sans penalite »",
       S1, {"gagnee": False, "cles_absentes": ["Dark Protege Removed", "Player 1 Overpowering Scenario 1"]}, mise=["Puzzle.Counter('sl072a', 'corruption', 5)"],
       declencher=["Puzzle.Lose()"], verifier="fnefin_carnet_sortant"),
    _c("S2 victoire : les vilains deja retires restent au carnet, le nouveau s'y ajoute", "le carnet CUMULE", S2,
       {"gagnee": True, "scenario": "shadow_labyrinth", "cles_presentes": ["Dark Protege Removed"]}, carnet={"Dark Protege Removed": "sl013a"}, declencher=["Puzzle.Win()"], verifier="fnefin_carnet_sortant"),
    _c("S3 victoire : « Campaign Completed » = 1", "livret p. 17 : « les joueurs remportent la campagne ! »", S3,
       {"gagnee": True, "scenario": "heart_of_shadow", "cles": {"Campaign Completed": "1"}}, declencher=["Puzzle.Win()"], verifier="fnefin_carnet_sortant"),
    _c("S3 DEFAITE : pas de « Campaign Completed »", "on rejoue", S3, {"gagnee": False, "cles_absentes": ["Campaign Completed"]}, declencher=["Puzzle.Lose()"], verifier="fnefin_carnet_sortant"),
]


# Le tirage au hasard change avec la graine : l'exclusion doit tenir sur 12 graines, pas sur une seule.
for _g in range(1, 13):
    CAS += [
        _c(f"S1 graine {_g} : Elektra et Gorgon retires (carnet) ne sont jamais tires", "livret p. 5 : un mechant coche est retire de la campagne",
           S1, {"vilain_parmi": ["sl012", "sl013", "sl016", "sl017"]}, carnet={"Dark Protege Removed": "sl014a;sl015a"}, graine=_g),
        _c(f"S1 graine {_g} avec le heros Daredevil : le vilain Daredevil n'est jamais tire", "livret p. 9 : le mechant qui partage le nom d'un heros est retire",
           S1, {"vilain_parmi": ["sl012", "sl014", "sl015", "sl016", "sl017"]}, heros="daredevil", graine=_g),
        _c(f"S2 graine {_g} : Elektra retiree (carnet) n'est jamais le vilain tire", "meme exclusion au scenario 2",
           S2, {"vilain_choisi_parmi": ["sl012", "sl013", "sl015", "sl016", "sl017"]}, carnet={"Dark Protege Removed": "sl014a"}, graine=_g),
    ]


VERIFICATIONS = r'''
def slcamp_etat(monde, aides):
    """etat_attendu + cles de la campagne Shadowland :
    `corruptions` : [[rang du joueur, nombre de jetons Corruption]] (la Creeping Corruption du joueur est en jeu, sl072a ou sl072b) ;
    `black_flower_dans_le_deck` : vrai = les 6 cartes du set sont dans le deck de rencontre, faux = aucune ;
    `vilain_parmi` : le vilain Sombre Protege EN JEU (S1) est l'un de ces ids de base ; `vilain_choisi_parmi` : idem pour le vilain tire et mis de cote (S2, `sl_vilain_choisi`) ;
    `sbires_sombres_proteges` : chaque joueur a un sbire sl020-sl023 face cachee, les autres sont dans le deck de rencontre ; `aucun_sbire_sombres_proteges` ;
    `expert_pv_reportes_ou_soignes` : PV restants posés par le carnet ; l'identite a ces PV OU est soignee a fond (le pilote accepte le soin)."""
    import json as _json, os as _os, re as _re
    from game.operate.worlds import Worlds as _W
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []

    def ids(faces):
        return [str(getattr(f.paper, "card_id", "?")) for f in faces]

    joueurs = list(monde.const_seat_order_players)
    for rang, n in attendu.get("corruptions") or []:
        cc = None
        for f in joueurs[rang].GetControlUpgrade():
            if str(f.paper.card_id) in ("sl072a", "sl072b"):
                cc = f
        if cc is None:
            soucis.append(f"joueur {rang} : aucune Creeping Corruption en jeu")
        else:
            reel = cc.GetCounters("corruption")
            if reel != n:
                soucis.append(f"joueur {rang} : {reel} jeton(s) Corruption (attendu {n})")
    if "black_flower_dans_le_deck" in attendu:
        deck = ids(_W.GetEncounterDeckCards(monde))
        presentes = [c for c in ("sl073", "sl074", "sl075", "sl076", "sl077", "sl078") if c in deck]
        if attendu["black_flower_dans_le_deck"] and len(presentes) != 6:
            soucis.append(f"Black Flower dans le deck de rencontre : {presentes} (attendu les 6)")
        if not attendu["black_flower_dans_le_deck"] and presentes:
            soucis.append(f"Black Flower dans le deck de rencontre alors que la campagne n'est pas jouee : {presentes}")
        if attendu["black_flower_dans_le_deck"]:
            with open(_os.path.join("data", "encounter_sets", "black_flower.json"), encoding="utf-8") as f:
                voulu = sorted(_json.load(f)["encounters"])
            reel = sorted(c for c in deck if c.startswith("sl07") and c != "sl072a")
            if reel != voulu:
                soucis.append(f"cartes Black Flower du deck {reel} differentes du set {voulu}")
    if "vilain_parmi" in attendu:
        vus = sorted({_re.match(r"(sl\d{3})", c).group(1) for c in ids(_W.GetAllVillains(monde)) if c.startswith("sl01")})
        if not vus or any(v not in attendu["vilain_parmi"] for v in vus):
            soucis.append(f"vilain Sombre Protege en jeu {vus} (attendu parmi {attendu['vilain_parmi']})")
    if "vilain_choisi_parmi" in attendu:
        choisi = getattr(monde, "sl_vilain_choisi", None)
        if choisi not in attendu["vilain_choisi_parmi"]:
            soucis.append(f"vilain tire {choisi} (attendu parmi {attendu['vilain_choisi_parmi']})")
    SBIRES = ("sl020", "sl021", "sl022", "sl023")
    if attendu.get("sbires_sombres_proteges"):
        distribues = [ids(j.dealt_encounter_cards.GetAll()) for j in joueurs]
        for rang, cartes in enumerate(distribues):
            if len(cartes) != 1 or cartes[0] not in SBIRES:
                soucis.append(f"joueur {rang} : cartes Rencontre face cachee {cartes} (attendu 1 sbire parmi {SBIRES})")
        dans_deck = [c for c in ids(_W.GetEncounterDeckCards(monde)) if c in SBIRES]
        attendu_deck = 4 - len(joueurs)
        if len(dans_deck) != attendu_deck:
            soucis.append(f"{len(dans_deck)} sbire(s) Sombres Proteges dans le deck de rencontre (attendu {attendu_deck})")
        tous = [c for d in distribues for c in d] + dans_deck
        if len(set(tous)) != len(tous):
            soucis.append(f"un meme sbire en double : {tous}")
    if attendu.get("aucun_sbire_sombres_proteges"):
        trouves = [c for c in ids(_W.GetEncounterDeckCards(monde)) if c in SBIRES] + [c for j in joueurs for c in ids(j.dealt_encounter_cards.GetAll())]
        if trouves:
            soucis.append(f"sbires Sombres Proteges presents hors campagne : {trouves}")
    if "expert_pv_reportes_ou_soignes" in attendu:
        identite = joueurs[0].GetIdentity()
        pv = identite.health
        if pv not in (attendu["expert_pv_reportes_ou_soignes"], identite.max_health):
            soucis.append(f"PV de l'identite {pv} (attendu {attendu['expert_pv_reportes_ou_soignes']} ou {identite.max_health} apres le soin)")
    reste = {k: v for k, v in attendu.items() if k not in ("corruptions", "black_flower_dans_le_deck", "vilain_parmi", "vilain_choisi_parmi",
                                                           "sbires_sombres_proteges", "aucun_sbire_sombres_proteges", "expert_pv_reportes_ou_soignes")}
    cas["attendu"] = reste
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = attendu
    if not ok:
        soucis.append(msg)
    return (False, " ; ".join(soucis)) if soucis else (True, "etat conforme")
'''
