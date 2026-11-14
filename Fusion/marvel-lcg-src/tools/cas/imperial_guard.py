# Cas test_capacites du modulaire IMPERIAL GUARD de Galactic Storm (gs091-gs113), lot GS-4 (20/10/2026).
# Format identique a tools/test_capacites.py ; noms prefixes `[ig]` puis le card_id (filtre : `[ig]`, ou
# `[ig] gs096 ` pour une carte).
#
# Conventions de ce fichier :
#  - le modulaire est monte par le scenario `gs_kree_sentry` (Kree Sentry (I), Spider-Man) : la mise en place REELLE tourne
#    (neuf cartes d'Imperial Guard tirees, un environnement en jeu, Rick Jones et sa Poigne). `ENV` retire les trois
#    environnements du tirage puis pose celui du cas : la mesure ne depend jamais du hasard.
#  - le heros de test (Spider-Man, 01001, DEF 3) demarre en ALTER EGO (01001b) ; `HEROS` le met en heros (01001a).
#  - « Special » d'environnement de reference : Disciplined Training (gs091), « Deal 1 damage to your identity » : un degat
#    sur l'identite prouve que le Special a ete resolu (`SPECIAL_OK`), l'absence de degat qu'il ne l'a pas ete.
#  - `DECK_NEUTRE` : le deck rencontre ne contient que des Advance (01186).
SC = "gs_kree_sentry"
HEROS = "Puzzle.ChangeForm('01001b')"
DECK_NEUTRE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', '01186', '01186', '01186')"]
TOUS_ENV = "Puzzle.Remove('gs091', 'gs092', 'gs093')"


def ENV(env):
    return [TOUS_ENV, f"Puzzle.PutIntoPlay('{env}')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[ig] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "ig_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


E1 = ENV("gs091")      # Special : 1 degat sur l'identite
SPECIAL_OK = {"degats_identite": 1}
SPECIAL_ABSENT = {"degats_identite": 0}

CAS = [
    # ============================================================== composition du set (random_pick)
    _c("gs_imperial_guard composition : 1 environnement en jeu, 6 sbires + 2 traitrises dans le deck rencontre (9 cartes sur 23)",
       "livret p.8 : « one random environment, six random minions, and both treacheries » ; `random_pick` du set (CardFactory.RandomPick)",
       [], [], {"composition": {"environnements_en_jeu": 1, "sbires_dans_le_deck": 6, "traitrises_dans_le_deck": 2,
                                "environnements_dans_le_deck": 0, "total_ig": 9}}, verifier="ig_composition"),
    # ============================================================== gs091 Disciplined Training
    _c("gs091 « Each IMPERIAL GUARD minion gains toughness » : Astra entre en jeu avec une carte Tenace",
       "GiveKeywordToInPlayWhenApplyThis(toughness=1) (modeles ar011, 40189)",
       DECK_NEUTRE + E1, ["Puzzle.PutIntoPlay('gs094')"], {"statuts": [["gs094", "Tough"]]}),
    _c("gs091 toughness, TEMOIN : un sbire d'un AUTRE set (Shocker) n'a pas de carte Tenace",
       "« Each IMPERIAL GUARD minion »", DECK_NEUTRE + E1, ["Puzzle.PutIntoPlay('01103')"],
       {"statuts_absents": [["01103", "Tough"]]}),
    _c("gs091 Special : « Deal 1 damage to your identity » (resolu par le verificateur)",
       "WhenResolveSpecialAbility (modele ab007)", DECK_NEUTRE + E1, [], SPECIAL_OK, verifier="ig_special"),
    _c("gs091 When Revealed : revelee, elle defausse l'AUTRE environnement SETTING en jeu (Noble Bearing)",
       "« Discard each other SETTING environment in play » (Worlds.DiscardEachOther)",
       DECK_NEUTRE + ENV("gs093"), ["Puzzle.Reveal('gs091')"], {"en_jeu": ["gs091"], "hors_jeu": ["gs093"]}),
    _c("gs091 Setup : en jeu des la mise en place (aucun script) ; son « When Revealed » n'a PAS joue",
       "base automatique `desc.Setup` : le tirage garde UN environnement, qui est deja en jeu (le tirage de cette graine)",
       [], [], {"environnement_unique": True}, verifier="ig_composition"),
    # ============================================================== gs092 Loyal Devotion
    _c("gs092 « teamwork (IMPERIAL GUARD) » : Titan entre en jeu alors qu'Astra y est deja -> il s'active (attaque le heros : 2 degats)",
       "GiveKeywordToInPlayWhenApplyThis(teamwork=\"IMPERIAL GUARD\") (modele bl012 ; fiche teamwork.md)",
       DECK_NEUTRE + ENV("gs092") + [HEROS, "Puzzle.PutIntoPlay('gs094')"], ["Puzzle.PutIntoPlay('gs110')"],
       {"degats_identite": 2}, passer_sur_option="Defense", regles=["v16_all"]),
    _c("gs092 teamwork, TEMOIN : sans autre sbire IMPERIAL GUARD en jeu, Titan n'active rien",
       "« if there is at least one OTHER minion ... that shares the trait »",
       DECK_NEUTRE + ENV("gs092") + [HEROS], ["Puzzle.PutIntoPlay('gs110')"], {"degats_identite": 0}),
    _c("gs092 Special : « Place 1 threat on the main scheme » (1B : 2 -> 3)",
       "PlaceThreatOnSchemes(\"MainScheme\", 1)", DECK_NEUTRE + ENV("gs092"), [], {"menace": [["gs079b", 3]]},
       verifier="ig_special"),
    _c("gs092 When Revealed : revelee, elle defausse l'AUTRE environnement SETTING en jeu (Disciplined Training)",
       "« Discard each other SETTING environment in play »",
       DECK_NEUTRE + E1, ["Puzzle.Reveal('gs092')"], {"en_jeu": ["gs092"], "hors_jeu": ["gs091"]}),
    # ============================================================== gs093 Noble Bearing
    _c("gs093 « gains guard and the ELITE trait » : Astra entre en jeu avec le trait ELITE",
       "GiveKeywordToInPlayWhenApplyThis(guard=1, trait=\"ELITE\") (modeles sk091, bl012)",
       DECK_NEUTRE + ENV("gs093"), ["Puzzle.PutIntoPlay('gs094')"], {"traits_de": [["gs094", "ELITE"]]}),
    _c("gs093 guard : Astra porte le mot-cle Guard (1)",
       "meme capacite, mot-cle", DECK_NEUTRE + ENV("gs093"), ["Puzzle.PutIntoPlay('gs094')"],
       {"carte": "gs094", "guard": 1}, verifier="ig_mots_cles"),
    _c("gs093 guard et ELITE, TEMOIN : un sbire d'un autre set (Shocker) n'en a ni l'un ni l'autre",
       "« Each IMPERIAL GUARD minion »", DECK_NEUTRE + ENV("gs093"), ["Puzzle.PutIntoPlay('01103')"],
       {"carte": "01103", "guard": 0, "elite": False}, verifier="ig_mots_cles"),
    _c("gs093 Special : « Discard the top 3 cards of the encounter deck » (3 Advance en defausse)",
       "Worlds.DiscardEncounterCards(3)", DECK_NEUTRE + ENV("gs093"), [], {"defausse_rencontre_n": [["01186", 3]]},
       verifier="ig_special"),
    _c("gs093 When Revealed : revelee, elle defausse l'AUTRE environnement SETTING en jeu",
       "« Discard each other SETTING environment in play »",
       DECK_NEUTRE + E1, ["Puzzle.Reveal('gs093')"], {"en_jeu": ["gs093"], "hors_jeu": ["gs091"]}),
    # ============================================================== gs094 Astra
    _c("gs094 « Discard an identity-specific card you control » : Aunt May (soutien propre a Spider-Man) est defaussee, pas de Special",
       "IsClass(\"IdentitySpecific\") (modele bt021)", DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('01006', under_control=True)"],
       ["Puzzle.Reveal('gs094')"], dict(SPECIAL_ABSENT, hors_jeu=["01006"], en_jeu=["gs094"])),
    _c("gs094 « If you cannot » : seul un allie BASIC en jeu (Mockingbird) -> rien a defausser, Special",
       "un allie Basic n'est pas propre a l'identite", DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('01083', under_control=True)"],
       ["Puzzle.Reveal('gs094')"], dict(SPECIAL_OK, en_jeu=["01083"])),
    _c("gs094 « you control » : une carte propre a l'identite qui n'est que dans la MAIN n'est pas defaussee (Special)",
       "« you CONTROL » = en jeu", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs094')"], SPECIAL_OK, main_exclusive=["01006"]),
    # ============================================================== gs095 Earthquake
    _c("gs095 « Exhaust your identity » : l'identite est inclinee, pas de Special",
       "Faces.ExhaustAll", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs095')"], dict(SPECIAL_ABSENT, exhausted=["01001b"])),
    _c("gs095 « If you were already exhausted » : identite deja inclinee -> Special",
       "l'etat est lu avant", DECK_NEUTRE + E1 + ["Puzzle.Exhaust('01001b')"], ["Puzzle.Reveal('gs095')"],
       dict(SPECIAL_OK, exhausted=["01001b"])),
    # ============================================================== gs096 Electron
    _c("gs096 « Discard a [energy] resource from your hand » : Energy (YY) defaussee, pas de Special",
       "FacesCounter.GetPrintedResourcesCount (modele gs240) ; icone eclair = [energy]",
       DECK_NEUTRE + E1, ["Puzzle.Reveal('gs096')"], dict(SPECIAL_ABSENT, dans_defausse_joueur=["01088"]),
       main_exclusive=["01088"]),
    _c("gs096 « If you cannot » : main sans [energy] (Genius, mentale) -> Special",
       "aucune icone [energy] en main", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs096')"], SPECIAL_OK, main_exclusive=["01089"]),
    _c("gs096 « [energy] resource » : une carte WILD (Spider-Woman) n'est pas une ressource [energy] imprimee -> Special",
       "convert_green_res=False (moteur officiel)", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs096')"], SPECIAL_OK,
       main_exclusive=["01011"]),
    # ============================================================== gs097 Fang
    _c("gs097 « Discard a card you control with a printed [wild] resource » : Spider-Woman (RES G) en jeu est defaussee",
       "GetControlCards(CardFinder(has_printed_res=\"G\")) ; icone etoile = wild",
       DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('01011', under_control=True)"], ["Puzzle.Reveal('gs097')"],
       dict(SPECIAL_ABSENT, hors_jeu=["01011"])),
    _c("gs097 « If you cannot » : seul un allie a ressource [physical] en jeu (Mockingbird) -> Special",
       "pas d'icone wild imprimee", DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('01083', under_control=True)"],
       ["Puzzle.Reveal('gs097')"], dict(SPECIAL_OK, en_jeu=["01083"])),
    # ============================================================== gs098 Gladiator
    _c("gs098 « Defeat a non-scenario specific ally you control » : Mockingbird est vaincue, pas de Special",
       "Defeated(None, effect) ; Victory 0 ; ELITE", DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('01083', under_control=True)"],
       ["Puzzle.Reveal('gs098')"], dict(SPECIAL_ABSENT, hors_jeu=["01083"], en_jeu=["gs081"])),
    _c("gs098 « non-scenario specific » : Rick Jones (allie du scenario) ne peut PAS etre choisi -> Special, Rick toujours en jeu",
       "classe Encounter exclue", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs098')"], dict(SPECIAL_OK, en_jeu=["gs081"], defaite=False)),
    _c("gs098 Victory 0 : Gladiator vaincu va dans la pile de victoire",
       "base automatique `desc.Victory = \"0\"` (fiche victory.md) ; environnement sans Tenace (Noble Bearing)", DECK_NEUTRE + ENV("gs093") + ["Puzzle.PutIntoPlay('gs098')"],
       ["Puzzle.Damage('gs098', 99)"], {"pile_de_victoire": ["gs098"]}, verifier="ig_victoire"),
    _c("gs098 trait ELITE imprime", "traits : ELITE. IMPERIAL GUARD", DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('gs098')"], [],
       {"traits_de": [["gs098", "ELITE"], ["gs098", "IMPERIAL GUARD"]]}),
    # ============================================================== gs099 Hobgoblin
    _c("gs099 « Resolve a When Revealed ability of another IMPERIAL GUARD minion in play » : copie celui de Titan (defausse une carte Ressource)",
       "Faces.ResolveAbility(.., WhenRevealed, ..) (modeles sm 27083, sk046)",
       DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('gs110')"], ["Puzzle.Reveal('gs099')"],
       dict(SPECIAL_ABSENT, dans_defausse_joueur=["01088"]), main_exclusive=["01088"]),
    _c("gs099 « If no ability was resolved this way » : aucun autre sbire IMPERIAL GUARD en jeu -> Special",
       "« another » : pas lui-meme", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs099')"], SPECIAL_OK),
    _c("gs099 « another » : un sbire d'un AUTRE set (Shocker) en jeu ne compte pas -> Special",
       "« another IMPERIAL GUARD minion »", DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Reveal('gs099')"],
       SPECIAL_OK),
    # ============================================================== gs100 Hussar
    _c("gs100 « Discard an upgrade you control » : Combat Training (amelioration) est defaussee",
       "GetControlUpgrade()", DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('01057', under_control=True)"],
       ["Puzzle.Reveal('gs100')"], dict(SPECIAL_ABSENT, hors_jeu=["01057"])),
    _c("gs100 « If you cannot » : aucune amelioration (un soutien seulement) -> Special",
       "un soutien n'est pas une amelioration", DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('01006', under_control=True)"],
       ["Puzzle.Reveal('gs100')"], dict(SPECIAL_OK, en_jeu=["01006"])),
    # ============================================================== gs101 Magique
    _c("gs101 « Give the villain a tough status card » : Kree Sentry recoit une carte Tenace",
       "Faces.GiveStatus([mechant], \"Tough\")", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs101')"],
       dict(SPECIAL_ABSENT, statuts=[["gs076", "Tough"]])),
    _c("gs101 « If you cannot » : le mechant a deja une carte Tenace -> Special",
       "une seule carte Tenace", DECK_NEUTRE + E1 + ["Puzzle.Tough('gs076')"], ["Puzzle.Reveal('gs101')"],
       dict(SPECIAL_OK, statuts=[["gs076", "Tough"]])),
    # ============================================================== gs102 Manta
    _c("gs102 « You are stunned » : l'identite est etourdie, pas de Special",
       "Faces.GiveStatus([identite], \"Stunned\")", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs102')"],
       dict(SPECIAL_ABSENT, statuts=[["01001b", "Stunned"]])),
    _c("gs102 « If you were already stunned » : deja etourdie -> Special",
       "etat deja pose", DECK_NEUTRE + E1 + ["Puzzle.Stun('01001b')"], ["Puzzle.Reveal('gs102')"],
       dict(SPECIAL_OK, statuts=[["01001b", "Stunned"]])),
    # ============================================================== gs103 Mentor
    _c("gs103 « Discard a player side scheme from play » : Build Support (manigance annexe JOUEUR) est defaussee",
       "Worlds.GetAllSideSchemes filtre PlayerSideScheme", DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('40027', under_control=True)"],
       ["Puzzle.Reveal('gs103')"], dict(SPECIAL_ABSENT, hors_jeu=["40027"])),
    _c("gs103 « If you cannot » : une manigance annexe de RENCONTRE (Locking on Target) n'est pas une manigance JOUEUR -> Special",
       "« PLAYER side scheme »", DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('gs086')"], ["Puzzle.Reveal('gs103')"],
       dict(SPECIAL_OK, en_jeu=["gs086"])),
    # ============================================================== gs104 Neutron
    _c("gs104 « Discard a support you control » : Aunt May est defaussee",
       "GetControlCardsByType(support=True)", DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('01006', under_control=True)"],
       ["Puzzle.Reveal('gs104')"], dict(SPECIAL_ABSENT, hors_jeu=["01006"])),
    _c("gs104 « If you cannot » : aucun soutien (un allie seulement) -> Special",
       "un allie n'est pas un soutien", DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('01083', under_control=True)"],
       ["Puzzle.Reveal('gs104')"], dict(SPECIAL_OK, en_jeu=["01083"])),
    # ============================================================== gs105 Nightside
    _c("gs105 « Discard a [mental] resource from your hand » : Genius (BB) defausse, pas de Special",
       "icone noeuds relies = [mental]", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs105')"],
       dict(SPECIAL_ABSENT, dans_defausse_joueur=["01089"]), main_exclusive=["01089"]),
    _c("gs105 « If you cannot » : main sans [mental] (Energy) -> Special", "aucune icone [mental]",
       DECK_NEUTRE + E1, ["Puzzle.Reveal('gs105')"], SPECIAL_OK, main_exclusive=["01088"]),
    # ============================================================== gs106 Oracle
    _c("gs106 « You are confused » : l'identite est desorientee, pas de Special",
       "Faces.GiveStatus([identite], \"Confused\")", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs106')"],
       dict(SPECIAL_ABSENT, statuts=[["01001b", "Confused"]])),
    _c("gs106 « If you were already confused » : deja desorientee -> Special",
       "etat deja pose", DECK_NEUTRE + E1 + ["Puzzle.Confuse('01001b')"], ["Puzzle.Reveal('gs106')"],
       dict(SPECIAL_OK, statuts=[["01001b", "Confused"]])),
    # ============================================================== gs107 Pulsar
    _c("gs107 « Discard a [physical] resource from your hand » : Strength (RR) defaussee, pas de Special",
       "icone poing = [physical]", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs107')"],
       dict(SPECIAL_ABSENT, dans_defausse_joueur=["01090"]), main_exclusive=["01090"]),
    _c("gs107 « If you cannot » : main sans [physical] -> Special", "aucune icone [physical]",
       DECK_NEUTRE + E1, ["Puzzle.Reveal('gs107')"], SPECIAL_OK, main_exclusive=["01089"]),
    # ============================================================== gs108 Smasher
    _c("gs108 « Discard an event from your hand » : l'evenement (01005) est defausse, pas de Special",
       "CardFinder Event sur la main", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs108')"],
       dict(SPECIAL_ABSENT, dans_defausse_joueur=["01005"]), main_exclusive=["01005", "01088"]),
    _c("gs108 « If you cannot » : main sans evenement -> Special", "aucun evenement",
       DECK_NEUTRE + E1, ["Puzzle.Reveal('gs108')"], SPECIAL_OK, main_exclusive=["01088"]),
    # ============================================================== gs109 Starbolt
    _c("gs109 « Remove 1 all-purpose counter from a card you control » : Web-Shooter (3 jetons web) en perd un",
       "Faces.RemoveCountersOn([carte], 1, 'all-purpose') (fiche all-purpose-counter.md)",
       DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('01008', under_control=True)"], ["Puzzle.Reveal('gs109')"],
       dict(SPECIAL_ABSENT, compteurs=[["01008", "web", 2]])),
    _c("gs109 « If you cannot » : aucune carte controlee avec un compteur -> Special", "aucun compteur polyvalent",
       DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('01083', under_control=True)"], ["Puzzle.Reveal('gs109')"],
       dict(SPECIAL_OK, en_jeu=["01083"])),
    # ============================================================== gs110 Titan
    _c("gs110 « Discard a resource card from your hand » : la carte Ressource (Energy) est defaussee, pas de Special",
       "type Ressource", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs110')"], dict(SPECIAL_ABSENT, dans_defausse_joueur=["01088"]),
       main_exclusive=["01088", "01005"]),
    _c("gs110 « resource card » : un evenement portant une icone de ressource n'est PAS une carte Ressource -> Special",
       "type Ressource et non icone", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs110')"], SPECIAL_OK, main_exclusive=["01005"]),
    # ============================================================== gs111 Warstar
    _c("gs111 « Discard the top card of the encounter deck. If that card is an IMPERIAL GUARD minion, reveal it » : Titan est revele",
       "Worlds.DiscardEncounterCards(1) + Reveal (modele tx009)",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', 'gs110')"] + E1, ["Puzzle.Reveal('gs111')"],
       dict(SPECIAL_ABSENT, en_jeu=["gs110"]), main_exclusive=["01088"]),
    _c("gs111 « Otherwise » : la carte du dessus n'est pas un sbire IMPERIAL GUARD (Advance) -> Special",
       "carte defaussee, Special", DECK_NEUTRE + E1, ["Puzzle.Reveal('gs111')"], dict(SPECIAL_OK, hors_jeu=["gs110"])),
    _c("gs111 « IMPERIAL GUARD MINION » : une traitrise IMPERIAL GUARD du dessus (Guard Assembles) -> Special, elle n'est pas revelee",
       "le type compte", ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', 'gs112')"] + E1,
       ["Puzzle.Reveal('gs111')"], dict(SPECIAL_OK, defausse_rencontre_n=[["gs112", 1]])),
    # ============================================================== gs112 Guard Assembles
    _c("gs112 « Discard cards ... until you discard an IMPERIAL GUARD minion and reveal it » : deux Advance defaussees puis Titan revele",
       "defausse une a une (modele baxter_stockman) puis Reveal",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', 'gs110', '01186', '01186')"] + E1,
       ["Puzzle.Reveal('gs112')"], {"en_jeu": ["gs110"], "defausse_rencontre_n": [["01186", 2]]}),
    _c("gs112 « IMPERIAL GUARD minion » : un sbire d'un AUTRE set (Shocker) ne l'arrete pas ; Titan, derriere, est revele",
       "le trait compte", ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', 'gs110', '01103')"] + E1,
       ["Puzzle.Reveal('gs112')"], {"en_jeu": ["gs110"], "hors_jeu": ["01103"], "defausse_rencontre_n": [["01103", 1]]}),
    # ============================================================== gs113 Imperial Formation
    _c("gs113 « Resolve the When Revealed ability of each IMPERIAL GUARD minion in play » : Titan ET Smasher resolvent le leur",
       "Faces.ResolveAbility (modeles sm 27083, sk046) : Titan defausse la Ressource, Smasher l'evenement",
       DECK_NEUTRE + E1 + ["Puzzle.PutIntoPlay('gs110')", "Puzzle.PutIntoPlay('gs108')"], ["Puzzle.Reveal('gs113')"],
       dict(SPECIAL_ABSENT, dans_defausse_joueur=["01088", "01005"]), main_exclusive=["01088", "01005"]),
    _c("gs113 « If you cannot » : aucun sbire IMPERIAL GUARD en jeu -> cherche dans le deck rencontre et revele Titan",
       "Search.EncounterCard (modele 60185)", ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', 'gs110')"] + E1,
       ["Puzzle.Reveal('gs113')"], {"en_jeu": ["gs110"]}),
    _c("gs113 recherche : dans la DEFAUSSE rencontre aussi",
       "« the encounter deck AND DISCARD PILE »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186')", "Puzzle.CreateEncounterDiscardPile('gs110')"] + E1,
       ["Puzzle.Reveal('gs113')"], {"en_jeu": ["gs110"]}),
]

VERIFICATIONS = r'''
def _ig_env_en_jeu(monde):
    from game.operate.worlds import Worlds
    zone = monde.players[0].GetGameArea()
    return [f for f in Worlds.GetOnFieldEnvironment(zone) if f.IsInPlay()]


def ig_etat(monde, aides):
    """etat_attendu (cles communes) + `dans_defausse_joueur` : card_id presents dans la defausse du premier joueur
    (la pile contient d'autres cartes : mise en place, mulligan)."""
    from game.operate.worlds import Worlds
    attendu = dict(aides["cas"].get("attendu") or {})
    voulus = attendu.pop("dans_defausse_joueur", [])
    rencontre = attendu.pop("defausse_rencontre_n", [])
    aides["cas"]["attendu"] = attendu
    ok, message = etat_attendu(monde, aides)
    soucis = [] if ok else [message]
    pile = [getattr(f.paper, "card_id", None) for f in monde.players[0].discard_pile.GetAll()]
    manquants = [c for c in voulus if c not in pile]
    if manquants:
        soucis.append(f"defausse du joueur = {pile} ; manquants {manquants}")
    for card_id, n in rencontre:
        reel = sum(1 for f in Worlds.GetEncounterDiscardPileCards(monde) if getattr(f.paper, "card_id", None) == card_id)
        if reel != n:
            soucis.append(f"{card_id} dans la defausse rencontre = {reel} (attendu {n})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "ok"


def ig_special(monde, aides):
    """Resout le Special de l'environnement SETTING en jeu pour le premier joueur, comme le ferait un sbire
    (`ResolveSpecialAbility`), puis mesure par etat_attendu."""
    from game.effect.rule import GameRule
    joueur = monde.players[0]
    for face in _ig_env_en_jeu(monde):
        if face.HasTrait("SETTING"):
            face.ResolveSpecialAbility(joueur, GameRule(face))
            break
    else:
        return False, "aucun environnement SETTING en jeu"
    return ig_etat(monde, aides)


def ig_composition(monde, aides):
    """`attendu.composition` : environnements_en_jeu, sbires_dans_le_deck, traitrises_dans_le_deck,
    environnements_dans_le_deck, total_ig ; `attendu.environnement_unique` : exactement un environnement IG en jeu."""
    from game.operate.worlds import Worlds
    attendu = aides["cas"].get("attendu") or {}
    ids = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde)]
    ig = [i for i in ids if i and i[:3] == "gs0" and 91 <= int(i[2:5]) <= 113 or (i and i[:3] == "gs1" and i[2:5] in ("100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113"))]
    envs_jeu = [getattr(f.paper, "card_id", None) for f in _ig_env_en_jeu(monde)
                if getattr(f.paper, "card_id", None) in ("gs091", "gs092", "gs093")]
    sbires = [i for i in ig if i not in ("gs091", "gs092", "gs093", "gs112", "gs113")]
    trait = [i for i in ig if i in ("gs112", "gs113")]
    envs_deck = [i for i in ig if i in ("gs091", "gs092", "gs093")]
    soucis = []
    if attendu.get("environnement_unique") and len(envs_jeu) != 1:
        soucis.append(f"environnements IG en jeu = {envs_jeu} (attendu 1)")
    comp = attendu.get("composition") or {}
    reel = {"environnements_en_jeu": len(envs_jeu), "sbires_dans_le_deck": len(sbires), "traitrises_dans_le_deck": len(trait),
            "environnements_dans_le_deck": len(envs_deck), "total_ig": len(envs_jeu) + len(ig)}
    for cle, voulu in comp.items():
        if reel[cle] != voulu:
            soucis.append(f"{cle} = {reel[cle]} (attendu {voulu}) ; deck IG = {sorted(ig)}, env en jeu = {envs_jeu}")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"ok {reel}"


def ig_mots_cles(monde, aides):
    """`attendu.carte` porte `guard` (valeur attendue) et `elite` (trait, facultatif)."""
    attendu = aides["cas"].get("attendu") or {}
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} introuvable en jeu"
    soucis = []
    if "guard" in attendu and getattr(face, "guard", 0) != attendu["guard"]:
        soucis.append(f"guard = {getattr(face, 'guard', 0)} (attendu {attendu['guard']})")
    if "elite" in attendu and face.HasTrait("ELITE") != attendu["elite"]:
        soucis.append(f"ELITE = {face.HasTrait('ELITE')} (attendu {attendu['elite']})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "ok"


def ig_victoire(monde, aides):
    """`attendu.pile_de_victoire` : card_id presents dans la pile de victoire."""
    attendu = aides["cas"].get("attendu") or {}
    pile = [getattr(f.paper, "card_id", None) for f in monde.victory_display.GetAll()] \
        if hasattr(monde, "victory_display") else []
    if not pile:
        for objet in monde.object_manager.card_dict.values():
            f = objet.face
            if f is not None and f.card.area.flags.is_victory_display:
                pile.append(getattr(f.paper, "card_id", None))
    manquants = [c for c in attendu.get("pile_de_victoire", []) if c not in pile]
    if manquants:
        return False, f"pile de victoire = {pile} ; manquants {manquants}"
    return True, f"pile de victoire = {pile}"
'''
