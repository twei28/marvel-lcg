"""Bloc 4 Fear No Evil (Kingpin) : cas du harnais [fne4] + verificateurs fne4_.
Idempotent : remplace le bloc entre ses deux marqueurs, insere juste AVANT le
marqueur du bloc 2. A lancer SOUS VERROU :
  flock /tmp/test_capacites.lock python3 scratchpad/b3/gen_cas_fne_c.py"""
import io, json
p='/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src/tools/test_capacites.py'
s=io.open(p,encoding='utf8').read()
SK='kingpin_fne'; SKE='kingpin_fne_expert'
HERO="Puzzle.ChangeForm('01001b')"; EXH="Puzzle.Exhaust('01001a')"
PLAT=["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', '01186', '01186')"]   # Advance x3 : 0 icone
FEU=["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01193', '01193', '01193')"]    # Under Fire x3 : 3 icones
VIDE=["Puzzle.EmptyEncounterDeck()"]
A2="Puzzle.Flip('60159a')"; B2="Puzzle.Flip('60160a')"
SANS_VAUTOUR="Puzzle.Remove('01167')"
TEMOIN='01101'   # Hydra Mercenary, seme au sommet pour prouver un surge
def cas(nom, pourquoi, scenario, declencher, attendu=None, verifier="etat_attendu", mise=None, **extra):
    d={"nom": nom, "pourquoi": pourquoi, "scenario": scenario, "heros": "spider_man",
       "mise_en_place": mise or [], "declencher": declencher, "verifier": verifier}
    d.update(extra)
    if attendu is not None: d["attendu"]=attendu
    return d
CAS=[
 # ================================================================ Kingpin A1 / The King's Gambit (mise en place)
 cas("60161a The King's Gambit 1A [fne4] — Setup : le sbire nemesis (Vulture) est revele ; 1B et Public Support LOW sont en jeu",
     "WhenCardSetup('This') : chaque joueur revele son nemesis mis de cote (01167) ; 1B When Revealed -> SetupCards.PutIntoPlay(Public Support) face LOW ; Kingpin A1", SK,
     [], {"en_jeu": ["60159a", "60161b", "60163a", "01167"], "hors_jeu": ["60163b", "60159b"]}),
 dict(cas("60161a The King's Gambit 1A [fne4] — Setup avec Echo : son nemesis Kingpin partage un titre avec le vilain, il est retire du jeu et un UNDERLING revele a la place",
     "« shares a title with a character in play » : le sbire 60061 Kingpin (nemesis de Maya Lopez) -> RemoveAllFromGame + TrouverEtRevelerUnderling", SK,
     [], verifier="fne4_sbires_en_jeu", attendu={"retirees": ["60061"], "underlings_min": 1, "hors_jeu": ["60061"]}), heros="echo"),
 cas("60159a Kingpin A1 [fne4] — ne peut pas subir de degats : 10 degats -> 0",
     "*UnitCannotTakeDamage(CardFinder(name=Kingpin, Villain)) (sd022) : PreventDamage('All')", SK,
     ["Puzzle.Damage('60159a', 10)"], {"degats": [["60159a", 0]], "en_jeu": ["60159a"]}),
 cas("60159a Kingpin A1 [fne4] — Webbed Up ne peut pas s'attacher a lui : aucune cible legale, la carte reste en main",
     "*UnitCannotHaveUpgradeAttached (46003) : CheckIfFaceCanAttachTo, envoye par Asset2.CanAttachTo depuis le 18/09/2026 (D1) : Kingpin n'est plus offert comme cible", SK,
     [], {"en_main": ["01009"], "hors_jeu": ["01009"]}, mise=[HERO, SANS_VAUTOUR], main_exclusive=["01009","01088","01088","01089"], jouer=["01009"], cibles=["60159a"]),
 cas("60159b Kingpin A2 [fne4] — contre-cas : Webbed Up s'attache a la face 2",
     "la face 2 n'a pas l'interdiction : hotes [01009 -> 60159b]", SK,
     [], {"hotes": [["01009", "60159b"]]}, mise=[A2, HERO, SANS_VAUTOUR], main_exclusive=["01009","01088","01088","01089"], jouer=["01009"], cibles=["60159b"]),
 cas("60159a Kingpin A1 [fne4] — quand il attaquerait, il manigance a la place (0 degat, 2 menaces)",
     "WhenUnitWouldAttack ForcedInterrupt + message.DoSchemeInstead (51019) ; SCH 2 + Advance (0 icone)", SK,
     ["Puzzle.SetThreat('60161b', 0)", "Puzzle.Attack('60159a')"], {"degats_identite": 0, "menace": [["60161b", 2]]}, mise=[HERO, EXH]+PLAT, main_exclusive=["01088"]),
 # ================================================================ Kingpin A2
 cas("60159b Kingpin A2 [fne4] — attaque sans sbire engage : 1 carte boost de plus (2 + 3 + 3 = 8)",
     "CapacitesDeKingpin2 : WhenUnitWouldAttack + GiveAdditionalBoostCardForThisActivation, condition engaged_minions vide ; deck = Under Fire x3", SK,
     ["Puzzle.Attack('60159b')"], {"degats_identite": 8}, mise=[A2, SANS_VAUTOUR, HERO, EXH]+FEU),
 cas("60159b Kingpin A2 [fne4] — contre-cas : Vulture engage, une seule carte boost (2 + 3 = 5)",
     "la condition « not engaged with a minion » echoue", SK,
     ["Puzzle.Attack('60159b')"], {"degats_identite": 5}, mise=[A2, HERO, EXH]+FEU),
 cas("60159b Kingpin A2 [fne4] — manigance sans sbire engage : 1 carte boost de plus (2 + 3 + 3 = 8 menaces)",
     "WhenUnitWouldScheme, meme condition ; partie en alter-ego", SK,
     ["Puzzle.SetThreat('60161b', 0)", "Puzzle.Scheme('60159b')"], {"menace": [["60161b", 8]]}, mise=[A2, SANS_VAUTOUR]+FEU, main_exclusive=["01088"]),
 cas("60159b Kingpin A2 [fne4] — Steady (base desc) : une seule carte stun ne l'empeche pas d'attaquer (2 degats)",
     "Steady = deux cartes de statut necessaires ; temoin du desc", SK,
     ["Puzzle.Attack('60159b')"], {"degats_identite": 2}, mise=[A2, HERO, EXH, "Puzzle.Stun('60159b')"]+PLAT),
 # ================================================================ Kingpin B1 / B2 (expert)
 cas("60160a Kingpin B1 [fne4] (expert) — pas de degats, et il manigance au lieu d'attaquer (SCH 3)",
     "CapacitesDeKingpin1 sur la face expert", SKE,
     ["Puzzle.SetThreat('60161b', 0)", "Puzzle.Damage('60160a', 10)", "Puzzle.Attack('60160a')"], {"degats": [["60160a", 0]], "degats_identite": 0, "menace": [["60161b", 3]]}, mise=[HERO, EXH]+PLAT, main_exclusive=["01088"]),
 cas("60160b Kingpin B2 [fne4] (expert) — attaque sans sbire : carte de plus ET overkill (3 + 3 + 3 = 9 sur Spider-Woman 2 PV : 7 passent)",
     "CapacitesDeKingpin2(overkill=True) : GainOverKill sur le message d'attaque ; Spider-Woman 01011 defend", SKE,
     ["Puzzle.Attack('60160b', '01011')"], {"degats_identite": 7, "hors_jeu": ["01011"]}, mise=[B2, SANS_VAUTOUR, HERO, "Puzzle.PutIntoPlay('01011', under_control=True)"]+FEU),
 cas("60159b Kingpin A2 [fne4] — contre-cas overkill : en standard, l'exces sur Spider-Woman est perdu (0 sur l'identite)",
     "CapacitesDeKingpin2(overkill=False)", SK,
     ["Puzzle.Attack('60159b', '01011')"], {"degats_identite": 0, "hors_jeu": ["01011"]}, mise=[A2, SANS_VAUTOUR, HERO, "Puzzle.PutIntoPlay('01011', under_control=True)"]+FEU),
 # ================================================================ The King's Gambit 1B
 cas("60161b The King's Gambit 1B [fne4] — Hero Action : 5 menaces retirees, la defausse remelangee, un sbire defausse et revele",
     "CostFunc.Custom(RemoveThreatFromSchemes 5) + ShuffleAllTo(EncounterDeck) + DiscardEncounterCardsUntil(Minion) + Reveal ; defausse = Hydra Mercenary, deck = Advance x2", SK,
     ["Puzzle.SetThreat('60161b', 6)", "Puzzle.Action('60161b', 'HeroAction', 0)"], {"menace": [["60161b", 1]], "en_jeu": [TEMOIN]},
     mise=[HERO, SANS_VAUTOUR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', '01186')", f"Puzzle.CreateEncounterDiscardPile('{TEMOIN}')"], main_exclusive=["01088"]),
 cas("60161b The King's Gambit 1B [fne4] — contre-cas : 4 menaces seulement, l'action n'est pas offerte",
     "condition assez_de_menace (5 en standard) ; declencher_tolerant", SK,
     ["Puzzle.SetThreat('60161b', 4)"], {"menace": [["60161b", 4]], "hors_jeu": [TEMOIN]},
     mise=[HERO, SANS_VAUTOUR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', '01186')", f"Puzzle.CreateEncounterDiscardPile('{TEMOIN}')"],
     declencher_tolerant=["Puzzle.Action('60161b', 'HeroAction', 0)"], main_exclusive=["01088"]),
 cas("60161b The King's Gambit 1B [fne4] (expert) — 4 menaces suffisent (4 -> 0)",
     "seuil 4 en expert (Worlds.IsExpert)", SKE,
     ["Puzzle.SetThreat('60161b', 4)", "Puzzle.Action('60161b', 'HeroAction', 0)"], {"menace": [["60161b", 0]], "en_jeu": [TEMOIN]},
     mise=[HERO, SANS_VAUTOUR, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', '01186')", f"Puzzle.CreateEncounterDiscardPile('{TEMOIN}')"], main_exclusive=["01088"]),
 # ================================================================ Public Support LOW / Endgame
 cas("60163a Public Support LOW [fne4] — apres la defaite d'un sbire : 1 compteur support",
     "AfterUnitBeDefeated(ForcedResponse, Minion) + PlaceCountersOn 'support' ; Diamondback 6 PV", SK,
     ["Puzzle.Damage('60170', 6)"], {"compteurs": [["60163a", "support", 1]], "hors_jeu": ["60170"]}, mise=VIDE+["Puzzle.PutIntoPlay('60170')"]),
 cas("60163a Public Support LOW [fne4] — 4 compteurs (2x1+2) au debut de la phase du mechant : Kingpin retourne (A2), complot au stade 2 (Endgame 2B), carte retournee (HIGH)",
     "WhenVillainPhaseBegin ForcedInterrupt + card.Flip(Kingpin) + MainScheme.Advance('2A') + card.Flip(this) ; Puzzle.BeginVillainPhase envoie WhenPhaseBegin", SK,
     ["Puzzle.BeginVillainPhase()"], {"en_jeu": ["60159b", "60162b", "60163b"], "hors_jeu": ["60159a", "60161b", "60163a"], "compteurs": [["60163b", "support", 4]]},
     mise=["Puzzle.Counter('60163a', 'support', 4)"]),
 cas("60163a Public Support LOW [fne4] — contre-cas : 3 compteurs, rien ne bouge",
     "la condition du seuil (2[per_hero]+2)", SK,
     ["Puzzle.BeginVillainPhase()"], {"en_jeu": ["60159a", "60161b", "60163a"], "hors_jeu": ["60159b", "60162b", "60163b"]},
     mise=["Puzzle.Counter('60163a', 'support', 3)"]),
 cas("60162a Endgame 2A [fne4] — When Revealed : Vulture deja en jeu n'entre pas en jeu « this way », un UNDERLING est trouve et revele",
     "Find.FindAndReveal(nemesis, if_no_entered_play) -> TrouverEtRevelerUnderling ; Vulture reste en jeu", SK,
     ["Puzzle.BeginVillainPhase()"], verifier="fne4_sbires_en_jeu", attendu={"en_jeu": ["01167", "60162b"], "underlings_min": 1},
     mise=["Puzzle.Counter('60163a', 'support', 4)"]),
 cas("60162a Endgame 2A [fne4] — When Revealed : Vulture en defausse est trouve et revele (aucun UNDERLING)",
     "Find fouille la defausse rencontre ; le nemesis entre en jeu, pas d'UNDERLING", SK,
     ["Puzzle.BeginVillainPhase()"], verifier="fne4_sbires_en_jeu", attendu={"en_jeu": ["01167", "60162b"], "underlings": 0},
     mise=["Puzzle.Discard('01167')", "Puzzle.Counter('60163a', 'support', 4)"]),
 cas("60162a Endgame 2A [fne4] — When Revealed : Vulture retire du jeu, un UNDERLING est revele a la place",
     "Find exclut la zone retiree -> TrouverEtRevelerUnderling", SK,
     ["Puzzle.BeginVillainPhase()"], verifier="fne4_sbires_en_jeu", attendu={"en_jeu": ["60162b"], "hors_jeu": ["01167"], "underlings_min": 1},
     mise=[SANS_VAUTOUR, "Puzzle.Counter('60163a', 'support', 4)"]),
 cas("60162a Endgame 2A [fne4] (expert) — le premier joueur trouve et revele Organized Crime",
     "Worlds.IsExpert -> Find.FindAndReveal(name=Organized Crime)", SKE,
     ["Puzzle.BeginVillainPhase()"], {"en_jeu": ["60174", "60162b", "60160b"], "hors_jeu": ["60160a"]},
     mise=["Puzzle.Counter('60163a', 'support', 4)"]),
 cas("60162b Endgame 2B [fne4] — chaque sbire gagne guard (Vulture)",
     "GiveKeywordToInPlayWhenApplyThis(Minion, guard=1)", SK,
     ["Puzzle.BeginVillainPhase()"], verifier="fne_mots_cles", attendu={"carte": "01167", "guard": True},
     mise=["Puzzle.Counter('60163a', 'support', 4)"]),
 cas("60162b Endgame 2B [fne4] — contre-cas : au stade 1, Vulture n'a pas guard",
     "le complot 2B n'est pas en jeu", SK,
     [], verifier="fne_mots_cles", attendu={"carte": "01167", "guard": False}),
 # ================================================================ Public Support HIGH
 cas("60163b Public Support HIGH [fne4] — Interrupt : 1 compteur retire a la place de la carte boost de Kingpin (2 + 0 = 2)",
     "WhenEnemyWouldBeGivenBoostCards(Interrupt) : SetNum(num - 1) + RemoveCountersOn ; deck = Under Fire x3 (sans l'interruption : 5)", SK,
     ["Puzzle.Attack('60159b')"], {"degats_identite": 2, "compteurs": [["60163b", "support", 0]]},
     mise=["Puzzle.Flip('60163a')", "Puzzle.Counter('60163b', 'support', 1)", A2, HERO, EXH]+FEU),
 cas("60163b Public Support HIGH [fne4] — contre-cas sans compteur : la carte boost est donnee (2 + 3 = 5)",
     "condition remplacable : au moins 1[per_hero] compteur", SK,
     ["Puzzle.Attack('60159b')"], {"degats_identite": 5, "compteurs": [["60163b", "support", 0]]},
     mise=["Puzzle.Flip('60163a')", A2, HERO, EXH]+FEU),
 cas("60163b Public Support HIGH [fne4] — Interrupt sur la carte boost donnee par James Wesley (hors activation) : compteur retire, pile de boost vide",
     "la fenetre WhenEnemyWouldBeGivenBoostCards vaut pour toutes les sources (D2) ; Wesley revele -> aucune carte dans la pile de Kingpin, 1 -> 0 support", SK,
     ["Puzzle.Reveal('60165')"], verifier="fne4_pile_boost_vide", attendu={"vilain": "60159a", "compteurs": [["60163b", "support", 0]], "hotes": [["60165", "60159a"]]},
     mise=["Puzzle.Flip('60163a')", "Puzzle.Counter('60163b', 'support', 1)"]+PLAT),
 cas("60163b Public Support HIGH [fne4] — Forced Response : sbire vaincu, +1 compteur",
     "ReponseForceeSoutien sur la face HIGH", SK,
     ["Puzzle.Damage('60170', 6)"], {"compteurs": [["60163b", "support", 1]]}, mise=["Puzzle.Flip('60163a')"]+VIDE+["Puzzle.PutIntoPlay('60170')"]),
 # ================================================================ Bear Hug
 cas("60164 Bear Hug [fne4] — Kingpin A1 (pas MARTIAL ARTIST) : surge, la carte ne s'attache pas",
     "selecteur YourHero + check_effect_fn KingpinArtMartial ; if_cannot_operation -> ThisCardGainSurge ; temoin = sbire du dessus", SK,
     ["Puzzle.Reveal('60164')"], {"en_jeu": [TEMOIN], "hors_jeu": ["60164"]}, mise=[HERO]+VIDE+[f"Puzzle.CreateEncounterDeck('{TEMOIN}')"]),
 cas("60164 Bear Hug [fne4] — Kingpin A2 : attachee au heros avec 3 grip ; une attaque du heros retire 1 grip a la place (Vulture indemne)",
     "AttachToFaceWhenPutIntoPlayInternal(YourHero) ; Uses (3 grip) = base desc ; WhenUnitWouldAttack('You') SetBeInstead + RemoveCountersOn", SK,
     ["Puzzle.Attack('01001a')"], {"hotes": [["60164", "01001a"]], "compteurs": [["60164", "grip", 2]], "degats": [["01167", 0]]},
     mise=[A2, HERO, "Puzzle.Reveal('60164')"], cibles=["01167"], main_exclusive=["01088"]),
 cas("60164 Bear Hug [fne4] — un contre du heros retire 1 grip a la place (menace intacte)",
     "WhenUnitWouldThwart('You') SetBeInstead + RemoveCountersOn", SK,
     ["Puzzle.SetThreat('60161b', 5)", "Puzzle.Thwart('01001a')"], {"compteurs": [["60164", "grip", 2]], "menace": [["60161b", 5]]},
     mise=[A2, HERO, SANS_VAUTOUR, "Puzzle.Reveal('60164')"], cibles=["60161b"], main_exclusive=["01088"]),
 cas("60164 Bear Hug [fne4] — le dernier grip retire : la carte quitte le jeu (Uses)",
     "3 attaques/contres : 3 -> 0, sortie native (has_uses.py)", SK,
     ["Puzzle.Attack('01001a')", "Puzzle.Ready('01001a')", "Puzzle.Attack('01001a')", "Puzzle.Ready('01001a')", "Puzzle.Attack('01001a')"],
     {"hors_jeu": ["60164"], "degats": [["01167", 0]]},
     mise=[A2, HERO, "Puzzle.Reveal('60164')", "Puzzle.EmptyPlayerDeck()"], cibles=["01167"], main_exclusive=["01088"]),
 cas("60164 Bear Hug [fne4] — impossible de passer en alter-ego",
     "PlayersCannotChangeForms(You, to_form=AlterEgo) ; declencher_tolerant", SK,
     [], {"forme": "Hero", "hotes": [["60164", "01001a"]]},
     mise=[A2, HERO, "Puzzle.Reveal('60164')"], declencher_tolerant=["Puzzle.ChangeForm('01001a')"], main_exclusive=["01088"]),
 # ================================================================ James Wesley
 cas("60165 James Wesley [fne4] — revele : attache a Kingpin (+1 SCH) et une carte boost face cachee lui est donnee",
     "AttacheAKingpin + WhenThisRevealed -> GiveFacedownBoostCardsInternal(1) ; deck = Advance", SK,
     ["Puzzle.Reveal('60165')"], verifier="fne4_wesley_revele", attendu={"boost_du_vilain": "01186", "vilain": "60159a", "hotes": [["60165", "60159a"]], "attributs_carte": [["60159a", "scheme", 1]]},
     mise=PLAT),
 cas("60165 James Wesley [fne4] — Hero Action : Emergency (THWART) defaussee -> Wesley defausse, Kingpin manigance (2 menaces)",
     "CostFunc.Discard('YourHandCards', trait=THWART, Event) + DoSchemes ; SCH 2 sans le +1, Advance 0 icone", SK,
     ["Puzzle.SetThreat('60161b', 0)", "Puzzle.Action('60165', 'HeroAction', 0)"], {"hors_jeu": ["60165"], "defausse": ["01085"], "menace": [["60161b", 2]]},
     mise=[HERO]+PLAT+["Puzzle.Reveal('60165')"], main_exclusive=["01085", "01088"]),
 cas("60165 James Wesley [fne4] — contre-cas : sans evenement THWART en main, l'action n'est pas offerte",
     "le cout n'a pas de cible ; declencher_tolerant", SK,
     ["Puzzle.SetThreat('60161b', 0)"], {"en_jeu": ["60165"], "menace": [["60161b", 0]]},
     mise=[HERO]+PLAT+["Puzzle.Reveal('60165')"], declencher_tolerant=["Puzzle.Action('60165', 'HeroAction', 0)"], main_exclusive=["01088"]),
 cas("60165 James Wesley [fne4] — Boost : apres l'activation, attache a Kingpin",
     "WhenThisBoostAttachTo(CardFinder(name=Kingpin, Villain)) (21170)", SK,
     ["Puzzle.Boost('60165')"], {"hotes": [["60165", "60159a"]]}, mise=[HERO, EXH]+PLAT),
 # ================================================================ Kingpin's Cane
 cas("60166 Kingpin's Cane [fne4] — revele : attache a Kingpin (+1 ATK), tu es etourdi",
     "AttacheAKingpin + WhenThisRevealed GiveStatus Stunned", SK,
     ["Puzzle.Reveal('60166')"], {"hotes": [["60166", "60159a"]], "attributs_carte": [["60159a", "attack", 1]], "statuts": [["01001a", "Stunned"]]}, mise=[HERO]),
 cas("60166 Kingpin's Cane [fne4] — Kingpin A2 attaque et blesse le heros (2 + 1 = 3) : heros etourdi, canne defaussee",
     "AfterUnitAttackAndDamageUnit(Kingpin, Hero) + GiveStatus > 0 -> DiscardAll ; Puzzle.Stun retire le stun de la revelation", SK,
     ["Puzzle.Attack('60159b')"], {"degats_identite": 3, "statuts": [["01001a", "Stunned"]], "hors_jeu": ["60166"]},
     mise=[A2, HERO, "Puzzle.Reveal('60166')", "Puzzle.Stun('01001a')", EXH]+PLAT),
 cas("60166 Kingpin's Cane [fne4] — contre-cas : heros robuste, 0 degat, pas d'etourdissement, la canne reste",
     "« attacks AND damages » : Tough absorbe, la reponse ne part pas", SK,
     ["Puzzle.Attack('60159b')"], {"degats_identite": 0, "statuts_absents": [["01001a", "Stunned"]], "en_jeu": ["60166"]},
     mise=[A2, HERO, "Puzzle.Reveal('60166')", "Puzzle.Stun('01001a')", "Puzzle.Tough('01001a')", EXH]+PLAT),
 cas("60166 Kingpin's Cane [fne4] — Boost : tu es etourdi (2 + 1 icone = 3 degats)",
     "WhenCardBecomeBoost : GiveStatus Stunned, pas deja etourdi -> pas de degat en plus", SK,
     ["Puzzle.Boost('60166')"], {"statuts": [["01001a", "Stunned"]], "degats_identite": 3}, mise=[A2, HERO, EXH]+VIDE+["Puzzle.CreateEncounterDeck('01186')"]),
 cas("60166 Kingpin's Cane [fne4] — Boost, deja etourdi : 1 degat de plus (3 + 1 = 4)",
     "« If you were already stunned » lu avant GiveStatus", SK,
     ["Puzzle.Boost('60166')"], {"degats_identite": 4}, mise=[A2, HERO, EXH, "Puzzle.Stun('01001a')"]+VIDE+["Puzzle.CreateEncounterDeck('01186')"]),
 # ================================================================ Mountain of Muscle
 cas("60167 Mountain of Muscle [fne4] — Kingpin A1 : surge, pas d'attache",
     "AttachToFaceWhenPutIntoPlay(CardFinder(Kingpin, trait MARTIAL ARTIST), if_cannot_gain_surge)", SK,
     ["Puzzle.Reveal('60167')"], {"en_jeu": [TEMOIN], "hors_jeu": ["60167"]}, mise=VIDE+[f"Puzzle.CreateEncounterDeck('{TEMOIN}')"]),
 cas("60167 Mountain of Muscle [fne4] — Kingpin A2 : attachee, 3 degats poses dessus a la place, retaliate 1 sur l'attaque du heros",
     "WhenUnitWouldTakeDamage(Villain, porteur) PreventDamage('All') + compteurs 'damage' ; GiveKeywordToAttached(retaliate=1) ; attaque ATK 2 -> 3 + 2 = 5 compteurs, 1 degat de riposte", SK,
     ["Puzzle.Damage('60159b', 3)", "Puzzle.Attack('01001a')"], {"hotes": [["60167", "60159b"]], "degats": [["60159b", 0]], "compteurs": [["60167", "damage", 5]], "degats_identite": 1},
     mise=[A2, HERO, SANS_VAUTOUR, "Puzzle.Reveal('60167')"], cibles=["60159b"], main_exclusive=["01088"]),
 cas("60167 Mountain of Muscle [fne4] — 8 degats accumules : defaussee, Kingpin indemne",
     "seuil 8 (5 + 3)", SK,
     ["Puzzle.Damage('60159b', 5)", "Puzzle.Damage('60159b', 3)"], {"hors_jeu": ["60167"], "degats": [["60159b", 0]]}, mise=[A2, "Puzzle.Reveal('60167')"]),
 # ================================================================ Vanessa Fisk
 cas("60168 Vanessa Fisk [fne4] — revele : attache a Kingpin (+1 SCH), tu es desoriente",
     "CapacitesDUnePersona + GiveStatus Confused", SK,
     ["Puzzle.Reveal('60168')"], {"hotes": [["60168", "60159a"]], "attributs_carte": [["60159a", "scheme", 1]], "statuts": [["01001a", "Confused"]]}, mise=[HERO]),
 cas("60168 Vanessa Fisk [fne4] — Hero Action : Swinging Web Kick (ATTACK) defausse -> Vanessa defaussee, Kingpin A2 attaque (2 degats)",
     "CostFunc.Discard('YourHandCards', trait=ATTACK, Event) + DoAttackYou ; heros incline, Advance 0 icone", SK,
     ["Puzzle.Action('60168', 'HeroAction', 0)"], {"hors_jeu": ["60168"], "defausse": ["01005"], "degats_identite": 2},
     mise=[A2, HERO, "Puzzle.Reveal('60168')", "Puzzle.Confuse('01001a')", EXH]+PLAT, main_exclusive=["01005", "01088"]),
 cas("60168 Vanessa Fisk [fne4] — Boost : tu es desoriente (pas de menace en plus)",
     "WhenCardBecomeBoost : GiveStatus Confused ; menace du complot inchangee (attaque)", SK,
     ["Puzzle.SetThreat('60161b', 0)", "Puzzle.Boost('60168')"], {"statuts": [["01001a", "Confused"]], "menace": [["60161b", 0]]}, mise=[A2, HERO, EXH]+VIDE+["Puzzle.CreateEncounterDeck('01186')"], main_exclusive=["01088"]),
 cas("60168 Vanessa Fisk [fne4] — Boost, deja desoriente : 1 menace sur le complot principal",
     "« If you were already confused » -> PlaceThreatOnSchemes('MainScheme', 1)", SK,
     ["Puzzle.SetThreat('60161b', 0)", "Puzzle.Boost('60168')"], {"menace": [["60161b", 1]]}, mise=[A2, HERO, EXH, "Puzzle.Confuse('01001a')"]+VIDE+["Puzzle.CreateEncounterDeck('01186')"], main_exclusive=["01088"]),
 # ================================================================ Black Cat
 cas("60169 Black Cat [fne4] — Hero Action [mental] : 4e menace, elle passe sous ton controle comme alliee (1/1, 2 degats consecutifs)",
     "PlaceTokensOn 'threat' puis Faces.TreatAsAlly(karma_controlled_ally) ; Genius (BB) paye", SK,
     ["Puzzle.Action('60169', 'HeroAction', 0)"], verifier="fne4_black_cat_alliee", attendu={"joueur": 0, "atk": 1, "thw": 1, "consecutifs": 2},
     mise=[HERO]+VIDE+["Puzzle.PutIntoPlay('60169')", "Puzzle.Token('60169', 'threat', 3)"], main_exclusive=["01089"], payer_avec=["01089"]),
 cas("60169 Black Cat [fne4] — alliee, elle garde Villainous : son attaque recoit 1 carte boost (1 + 3 = 4 sur Diamondback)",
     "gabarit fne_black_cat_ally (Villainous 1), Ally herite de HasVillainous (D3) ; deck = Under Fire x3 ; Puzzle.Attack trouve la face echangee par son ancien id", SK,
     ["Puzzle.Action('60169', 'HeroAction', 0)", "Puzzle.Attack('60169')"], {"degats": [["60170", 4]], "degats_identite": 0},
     mise=[HERO]+FEU+["Puzzle.PutIntoPlay('60169')", "Puzzle.PutIntoPlay('60170')", "Puzzle.Token('60169', 'threat', 3)"], main_exclusive=["01089"], payer_avec=["01089"], cibles=["60170"]),
 cas("60169 Black Cat [fne4] — contre-cas : 3e menace seulement, elle reste un sbire",
     "seuil 4", SK,
     ["Puzzle.Action('60169', 'HeroAction', 0)"], {"jetons": [["60169", "threat", 3]], "en_jeu": ["60169"]},
     mise=[HERO]+VIDE+["Puzzle.PutIntoPlay('60169')", "Puzzle.Token('60169', 'threat', 2)"], main_exclusive=["01089"], payer_avec=["01089"]),
 # ================================================================ Diamondback
 cas("60170 Diamondback [fne4] — quand il t'attaque : 1 degat, puis l'attaque (1 + 1 + 0 = 2)",
     "WhenUnitWouldAttack('This') ForcedInterrupt + identity.TakeDamage(1) ; Villainous (base) : Advance 0 icone", SK,
     ["Puzzle.Attack('60170')"], {"degats_identite": 2}, mise=VIDE+["Puzzle.PutIntoPlay('60170')", HERO, EXH]+PLAT),
 cas("60170 Diamondback [fne4] — Boost : 1 degat (2 + 2 icones + 1 = 5)",
     "WhenCardBecomeBoost : GetToPlayer().GetIdentity().TakeDamage(1)", SK,
     ["Puzzle.Boost('60170')"], {"degats_identite": 5}, mise=[A2, HERO, EXH]+VIDE+["Puzzle.CreateEncounterDeck('01186')"]),
 # ================================================================ Spot
 cas("60171 Spot [fne4] — entre avec 1 spot ; attaque du heros : le pion est retire et les 2 degats renvoyes a l'attaquant",
     "ThisEnterPlayWithCounters(1) ; WhenUnitWouldTakeDamage('This', is_from_attack) PreventDamage('All') + DealDamage(attacker)", SK,
     ["Puzzle.Attack('01001a')"], {"degats": [["60171", 0]], "degats_identite": 2, "compteurs": [["60171", "spot", 0]]},
     mise=VIDE+["Puzzle.PutIntoPlay('60171')", HERO], cibles=["60171"], main_exclusive=["01088"]),
 cas("60171 Spot [fne4] — sans pion : il subit les 2 degats et gagne 1 spot",
     "branche Otherwise : PlaceCountersOn 1", SK,
     ["Puzzle.Attack('01001a')"], {"degats": [["60171", 2]], "degats_identite": 0, "compteurs": [["60171", "spot", 1]]},
     mise=VIDE+["Puzzle.PutIntoPlay('60171')", "Puzzle.Counter('60171', 'spot', -1)", HERO], cibles=["60171"], main_exclusive=["01088"]),
 cas("60171 Spot [fne4] — contre-cas : des degats hors attaque ne sont pas renvoyes",
     "is_from_attack=True : Puzzle.Damage passe", SK,
     ["Puzzle.Damage('60171', 2)"], {"degats": [["60171", 2]], "degats_identite": 0, "compteurs": [["60171", "spot", 1]]},
     mise=VIDE+["Puzzle.PutIntoPlay('60171')", HERO]),
 # ================================================================ Stilt-Man
 cas("60172 Stilt-Man [fne4] — entre avec 2 stilt : +2 SCH et +2 ATK",
     "ThisEnterPlayWithCounters(2) + ThisGainKeyword(pions, attack=1, scheme=1, OnEvent.Counter)", SK,
     ["Puzzle.PutIntoPlay('60172')"], {"compteurs": [["60172", "stilt", 2]], "attributs_carte": [["60172", "attack", 2], ["60172", "scheme", 2]]}, mise=VIDE),
 cas("60172 Stilt-Man [fne4] — 3 degats : 1 stilt retire a la place, +1/+1 seulement",
     "WhenUnitWouldTakeDamage('This') PreventDamage('All') + RemoveCountersOn 1 ; rafraichi par OnEvent.Counter", SK,
     ["Puzzle.Damage('60172', 3)"], {"degats": [["60172", 0]], "compteurs": [["60172", "stilt", 1]], "attributs_carte": [["60172", "attack", 1], ["60172", "scheme", 1]]}, mise=VIDE+["Puzzle.PutIntoPlay('60172')"]),
 cas("60172 Stilt-Man [fne4] — sans stilt : les 3 degats passent",
     "condition a_un_pion", SK,
     ["Puzzle.Damage('60172', 3)"], {"degats": [["60172", 3]], "attributs_carte": [["60172", "attack", 0]]}, mise=VIDE+["Puzzle.PutIntoPlay('60172')", "Puzzle.Counter('60172', 'stilt', -2)"]),
 # ================================================================ Kingpin's Influence
 cas("60173 Kingpin's Influence [fne4] — vaincue : Highway Robbery (nemesis) hors jeu -> trouvee et revelee (3 menaces)",
     "WhenSchemeBeDefeated + GetDefeatingPlayer + Find.FindAndReveal(CardFinder(SideScheme, is_nemesis)) ; Hazard = base desc", SK,
     ["Puzzle.SetThreat('60173', 1)", "Puzzle.Thwart('01001a')"], {"en_jeu": ["01166"], "menace": [["01166", 3]], "hors_jeu": ["60173"], "icones": [["Hazard", 0]]},
     mise=[HERO, SANS_VAUTOUR]+VIDE+["Puzzle.PutIntoPlay('60173')"], cibles=["60173"], main_exclusive=["01088"]),
 cas("60173 Kingpin's Influence [fne4] — vaincue, Highway Robbery deja en jeu : 3 menaces de plus (3 -> 6)",
     "PlaceThreatOnSchemes([nemesis], 3)", SK,
     ["Puzzle.SetThreat('01166', 3)", "Puzzle.SetThreat('60173', 1)", "Puzzle.Thwart('01001a')"], {"menace": [["01166", 6]], "hors_jeu": ["60173"]},
     mise=[HERO, SANS_VAUTOUR]+VIDE+["Puzzle.Reveal('01166')", "Puzzle.PutIntoPlay('60173')"], cibles=["60173"], main_exclusive=["01088"]),
 cas("60173 Kingpin's Influence [fne4] — en jeu : 2[per_hero] menaces et 1 icone Hazard",
     "StartingThreat 2* et Hazard 1 (base desc)", SK,
     ["Puzzle.Reveal('60173')"], {"menace": [["60173", 2]], "icones": [["Hazard", 1]]}, mise=VIDE),
 # ================================================================ Organized Crime
 cas("60174 Organized Crime [fne4] — chaque sbire a +2 PV (Diamondback 8, Vulture 6)",
     "GiveKeywordToInPlayWhenApplyThis(Minion, health=2)", SK,
     ["Puzzle.PutIntoPlay('60170')"], {"pv_max": [["60170", 8], ["01167", 6]], "menace": [["60174", 3]]}, mise=VIDE+["Puzzle.PutIntoPlay('60174')"]),
 # ================================================================ Bag of Tricks
 cas("60175 Bag of Tricks [fne4] — revelee : une carte au hasard du set nemesis mis de cote est revelee (4 -> 3, Sweeping Swoop en defausse)",
     "CartesNemesisMisesDeCote + Rand.RandomChoice + Reveal ; apres la mise en place il reste 01166, 01168 x2, 01169 ; sous graine 42 c'est 01168 (elle porte Surge elle-meme : pas de temoin de non-surge possible)", SK,
     ["Puzzle.Reveal('60175')"], verifier="fne4_reserve_nemesis", attendu={"taille": 3, "defausse_rencontre": ["01168"]},
     mise=[HERO]+PLAT),
 cas("60175 Bag of Tricks [fne4] — set nemesis vide : surge",
     "ThisCardGainSurge ; les 4 cartes de la reserve retirees par Puzzle.Remove (fouille set_aside_nemesis_sets depuis le 18/09/2026, D4) ; temoin = sbire du dessus", SK,
     ["Puzzle.Reveal('60175')"], verifier="fne4_reserve_nemesis", attendu={"taille": 0, "en_jeu": [TEMOIN]},
     mise=[HERO, "Puzzle.Remove('01166')", "Puzzle.Remove('01168')", "Puzzle.Remove('01168')", "Puzzle.Remove('01169')"]+VIDE+[f"Puzzle.CreateEncounterDeck('{TEMOIN}')"]),
 cas("60175 Bag of Tricks [fne4] — Boost : une carte du set nemesis donnee en boost supplementaire (4 -> 3, au moins 2 degats)",
     "CanBoost.GiveBoostCard(carte) pendant ResolveBoostCards ; Bag 0 icone, la carte tiree en ajoute 0 a 3", SK,
     ["Puzzle.Boost('60175')"], verifier="fne4_reserve_nemesis", attendu={"taille": 3, "degats_identite_min": 2},
     mise=[A2, HERO, EXH]+VIDE+["Puzzle.CreateEncounterDeck('01186')"]),
 # ================================================================ Unrelenting Hate
 cas("60176 Unrelenting Hate [fne4] — revelee : Vulture (en jeu) s'active contre toi (3 degats)",
     "SbireNemesisEnJeu + DoActivate ; heros incline", SK,
     ["Puzzle.Reveal('60176')"], {"degats_identite": 3}, mise=[HERO, EXH]+PLAT),
 cas("60176 Unrelenting Hate [fne4] — Vulture en defausse : trouve et revele",
     "Find.FindAndReveal(CardFinder(Minion, is_nemesis))", SK,
     ["Puzzle.Reveal('60176')"], verifier="fne4_sbires_en_jeu", attendu={"en_jeu": ["01167"], "underlings": 0}, mise=["Puzzle.MoveTo('01167', 'EncounterDiscardPile')"]),
 cas("60176 Unrelenting Hate [fne4] — Vulture retire du jeu : un UNDERLING est trouve et revele",
     "Find exclut la zone retiree -> TrouverEtRevelerUnderling", SK,
     ["Puzzle.Reveal('60176')"], verifier="fne4_sbires_en_jeu", attendu={"hors_jeu": ["01167"], "underlings_min": 1}, mise=[SANS_VAUTOUR]),
 cas("60176 Unrelenting Hate [fne4] — Boost : l'attaque gagne overkill (2 + 1 = 3 sur Spider-Woman 2 PV : 1 passe)",
     "would_atk_message.GainOverKill ; Unrelenting Hate semee au sommet du deck = la carte boost de l'attaque ; Spider-Woman defend (Puzzle.Attack(defender))", SK,
     ["Puzzle.Attack('60159b', '01011')"], {"degats_identite": 1, "hors_jeu": ["01011"]},
     mise=[A2, HERO, "Puzzle.PutIntoPlay('01011', under_control=True)"]+VIDE+["Puzzle.CreateEncounterDeck('60176')"]),
]
DEBUT="    # ------------------------------------------------------------------------\n    # Pack officiel « fne » — bloc 4"
FIN="    # ---- fin du bloc 4 fne ----\n"
bloc = DEBUT + " : Kingpin (scenario final)\n    # (18/09/2026). Filtre : \"[fne4]\". Genere par scratchpad/b3/gen_cas_fne_c.py.\n    # ------------------------------------------------------------------------\n"
for c in CAS:
    bloc += "    " + json.dumps(c, ensure_ascii=False, indent=4).replace("\n", "\n    ").replace(": true", ": True").replace(": false", ": False") + ",\n"
bloc += FIN
if DEBUT in s:
    i=s.index(DEBUT); j=s.index(FIN, i)+len(FIN); s=s[:i]+bloc+s[j:]
else:
    ancre="    # ------------------------------------------------------------------------\n    # Pack officiel « fne » — bloc 2"
    assert ancre in s, "ancre bloc 2"
    s=s.replace(ancre, bloc+ancre, 1)

VERIFS='''
# ---------------------------------------------------------------- pack fne (bloc 4)
def _fne4_delegue(monde, aides, cles_propres):
    """Delegue a etat_attendu les cles generiques, en cachant les cles propres
    (le garde-fou des cles inconnues ne joue que si le cas appelle etat_attendu
    directement ; on ne laisse passer ici QUE des cles qu'il lit vraiment)."""
    attendu = aides["cas"].get("attendu") or {}
    reste = {k: v for k, v in attendu.items() if k not in cles_propres}
    inconnues = sorted(set(reste) - CLES_ETAT_ATTENDU)
    if inconnues:
        return False, f"cle(s) inconnue(s) : {inconnues}"
    if not reste:
        return True, ""
    sauve = aides["cas"]["attendu"]
    aides["cas"]["attendu"] = reste
    try:
        return etat_attendu(monde, aides)
    finally:
        aides["cas"]["attendu"] = sauve

def _fne4_sbires(monde):
    from game.card.face.card_type import Minion
    out = []
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and face.IsInPlay() and Minion.IsType(face):
            out.append(face)
    return out

def fne4_sbires_en_jeu(monde, aides):
    """`underlings` (exact) / `underlings_min` : sbires UNDERLING en jeu ;
    `retirees` : card_id dans la zone retiree ; le reste va a etat_attendu."""
    attendu = aides["cas"].get("attendu") or {}
    sbires = _fne4_sbires(monde)
    n = sum(1 for f in sbires if f.HasTrait("UNDERLING"))
    ids = [getattr(f.paper, "card_id", "?") for f in sbires]
    if "underlings" in attendu and n != attendu["underlings"]:
        return False, f"{n} UNDERLING en jeu (attendu {attendu['underlings']}) ; sbires = {ids}"
    if "underlings_min" in attendu and n < attendu["underlings_min"]:
        return False, f"{n} UNDERLING en jeu (attendu au moins {attendu['underlings_min']}) ; sbires = {ids}"
    retirees = [getattr(f.paper, "card_id", None) for f in monde.area_removed.Get(True)]
    manquent = [c for c in attendu.get("retirees") or [] if c not in retirees]
    if manquent:
        return False, f"{manquent} pas retiree(s) du jeu (retirees = {retirees})"
    ok, msg = _fne4_delegue(monde, aides, {"underlings", "underlings_min", "retirees"})
    return ok, f"sbires = {ids}, UNDERLING = {n} ; {msg}"

def fne4_reserve_nemesis(monde, aides):
    """`taille` : nombre de cartes restant dans la reserve nemesis du joueur 0."""
    attendu = aides["cas"].get("attendu") or {}
    joueur = monde.players[0]
    cartes = [getattr(f.paper, "card_id", "?") for f in joueur.set_aside_nemesis_sets.Get()]
    if len(cartes) != attendu["taille"]:
        return False, f"reserve nemesis = {cartes} ({len(cartes)}, attendu {attendu['taille']})"
    ok, msg = _fne4_delegue(monde, aides, {"taille"})
    return ok, f"reserve nemesis = {cartes} ; {msg}"

def fne4_bag_sans_reserve(monde, aides):
    """Vide la reserve nemesis du joueur 0 (RemoveAllFromGame, le harnais ne
    fouille pas set_aside_nemesis_sets) PUIS revele Bag of Tricks ; `taille`
    et le temoin de surge vont aux verifications habituelles."""
    from game.puzzle.puzzle import PuzzleHelper
    from game.operate.faces import Faces
    from game.effect.rule import DebugRule
    joueur = monde.players[0]
    reserve = list(joueur.set_aside_nemesis_sets.Get())
    if reserve:
        Faces.RemoveAllFromGame(reserve, DebugRule(joueur.GetIdentity()))
    PuzzleHelper.Exec(["Puzzle.Reveal('60175')"], monde)
    return fne4_reserve_nemesis(monde, aides)

def fne4_pile_boost_vide(monde, aides):
    """`vilain` : sa pile de boost est VIDE (la carte a ete remplacee) ; le
    reste (compteurs, hotes) va a etat_attendu."""
    attendu = aides["cas"].get("attendu") or {}
    vilain = aides["par_id"](monde, attendu["vilain"])
    if vilain is None:
        return False, f"{attendu['vilain']} introuvable en jeu"
    pile = [getattr(f.paper, "card_id", "?") for f in vilain.components.boostable.GetDeck().Get(True)]
    if pile:
        return False, f"pile de boost non vide : {pile}"
    ok, msg = _fne4_delegue(monde, aides, {"vilain"})
    return ok, f"pile de boost vide ; {msg}"

def fne4_black_cat_alliee(monde, aides):
    """Black Cat convertie : un ALLIE a son image (pic_id 60169) controle par le
    joueur, ATK/THW recopies, 2 degats consecutifs, et plus aucun sbire 60169."""
    from game.card.face.card_type import Ally
    attendu = aides["cas"].get("attendu") or {}
    joueur = monde.players[attendu.get("joueur", 0)]
    trouve = None
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and face.IsInPlay() and Ally.IsType(face) and getattr(face, "pic_id", None) == "60169":
            trouve = face
    if trouve is None:
        return False, "aucun allie a l'image de Black Cat en jeu"
    soucis = []
    if trouve.GetControlBy() is not joueur:
        soucis.append("pas sous le controle du joueur")
    if trouve.attack != attendu["atk"]:
        soucis.append(f"ATK = {trouve.attack} (attendu {attendu['atk']})")
    if trouve.thwart != attendu["thw"]:
        soucis.append(f"THW = {trouve.thwart} (attendu {attendu['thw']})")
    ca = getattr(trouve, "attack_consequential_damage", None)
    ct = getattr(trouve, "thwart_consequential_damage", None)
    if ca != attendu["consecutifs"] or ct != attendu["consecutifs"]:
        soucis.append(f"degats consecutifs ATK/THW = {ca}/{ct} (attendu {attendu['consecutifs']})")
    if trouve.card.face is not trouve:
        soucis.append("la face active de la carte n'est pas l'alliee")
    from game.card.face.card_type import Minion
    if Minion.IsType(trouve.card.face):
        soucis.append("la face active est encore un sbire")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"Black Cat alliee : {trouve.name} ATK {trouve.attack} THW {trouve.thwart}, consecutifs {ca}/{ct}"

def fne4_wesley_revele(monde, aides):
    """James Wesley revele : la pile de boost de Kingpin contient la carte
    (fne_boost_du_vilain), et le reste (hotes, attributs_carte) va a etat_attendu."""
    ok, msg = fne_boost_du_vilain(monde, aides)
    if not ok:
        return ok, msg
    ok2, msg2 = _fne4_delegue(monde, aides, {"boost_du_vilain", "vilain"})
    return ok2, f"{msg} ; {msg2}"

'''
MARQ="# ---------------------------------------------------------------- pack fne (bloc 4)"
FINV = "# ---- fin des verificateurs du bloc 4 ----\n"
VERIFS = VERIFS.rstrip("\n") + "\n\n" + FINV
# ⚠ On ne remplace QUE sa propre section (du marqueur au marqueur de fin) :
# « du marqueur a def etat_attendu » effacait les verificateurs des autres
# blocs poses apres (6 verificateurs fne4_ perdus deux fois le 18/09/2026).
if MARQ in s:
    i = s.index(MARQ)
    j = s.index(FINV, i) + len(FINV) if FINV in s[i:] else s.index("def etat_attendu(monde, aides):", i)
    s = s[:i] + VERIFS.lstrip("\n") + "\n" + s[j:]
else:
    j = s.index("def etat_attendu(monde, aides):")
    s = s[:j] + VERIFS.lstrip("\n") + "\n" + s[j:]
io.open(p,'w',encoding='utf8').write(s)
import ast; ast.parse(s)
print("cas [fne4]:", len(CAS), "; syntaxe OK")
