"""Bloc 3A Fear No Evil (The Getaway, The Raft Breakout, Stop the Presses!) :
cas du harnais [fne3a] + verificateurs fne3a_*. Idempotent : remplace le bloc
entre ses deux marqueurs (place juste AVANT le bloc 2, qui est lui-meme avant
le bloc 1). A lancer SOUS VERROU :
    flock /tmp/test_capacites.lock python3 scratchpad/b3/gen_cas_fne_a.py
Copie adaptee de scratchpad/b2/gen_cas_fne_b2.py."""
import io, json
p='/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src/tools/test_capacites.py'
s=io.open(p,encoding='utf8').read()
HERO="Puzzle.ChangeForm('01001b')"; HERO_BP="Puzzle.ChangeForm('01040b')"
PLAT=["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', '01186', '01186')"]
TEMOIN='01101'
SG='the_getaway_hammerhead'; SR='the_raft_breakout_hammerhead'; SP='stop_the_presses_hammerhead'
def cas(nom, pourquoi, scenario, declencher, attendu=None, verifier="etat_attendu", mise=None, **extra):
    d={"nom": nom, "pourquoi": pourquoi, "scenario": scenario, "heros": "spider_man",
       "mise_en_place": mise or [], "declencher": declencher, "verifier": verifier}
    # Main controlee PAR DEFAUT : Great Responsibility (01061), jouee par le
    # pilote, encaissait en degats la menace posee par Proxima, Stop the Presses
    # 1B et meme Puzzle.SetThreat (RECETTES §7ter). `main_exclusive: []` n'est
    # pas applique : une ressource injouable.
    d.setdefault("main_exclusive", ["01088"])
    d.update(extra)
    if attendu is not None: d["attendu"]=attendu
    return d
CAS=[
 # ================================================================ The Getaway
 cas("60128a The Getaway 1A [fne3a] — Setup : 1 compteur speed sur le complot, Out Front attachee au vilain",
     "WhenCardSetup du complot 1A (60121a) + Find.FindAndAttachTo depuis la mise de cote du scenario (60066)", SG, [],
     {"compteurs": [["60128b","speed",1]], "hotes": [["60129a","60086"]], "en_jeu": ["60129a"], "menace": [["60128b", 2]]}),
 dict(cas("60128a The Getaway 1A [fne3a] (expert) — Setup : 2 compteurs speed",
     "Worlds.IsExpert -> 2 compteurs ; le vilain expert est Hammerhead II (60087)", SG+"_expert", [],
     {"compteurs": [["60128b","speed",2]], "hotes": [["60129a","60087"]]}), ),
 cas("60128b The Getaway 1B [fne3a] — fin de round avec de la menace, Out Front en jeu : +1 speed puis +1 de plus (1 -> 3)",
     "WhenRoundEnd ForcedInterrupt ; le verificateur envoie WhenRoundEnd (brawn_hulk_out_fin_de_round) ; Alongside absente -> 2e compteur", SG,
     [], verifier="fne3a_fin_de_round", attendu={"compteurs": [["60128b","speed",3]], "en_jeu": ["60129a"]}),
 cas("60128b The Getaway 1B [fne3a] — fin de round, Alongside en jeu : +1 speed et Alongside se retourne en Out Front (1 -> 2)",
     "2 degats au vilain -> Out Front retire 2 menaces (2 -> 0) et se retourne en Alongside ; menace remise a 3 ; RetournerLAttachement au round end", SG,
     [], verifier="fne3a_fin_de_round", attendu={"compteurs": [["60128b","speed",2]], "en_jeu": ["60129a"], "hors_jeu": ["60129b"], "hotes": [["60129a","60086"]]},
     mise=["Puzzle.Damage('60086', 2)","Puzzle.SetThreat('60128b', 3)"]),
 cas("60128b The Getaway 1B [fne3a] — contre-cas : sans menace sur le complot, rien ne se passe (speed reste 1)",
     "« if there is threat here » lu avant toute action ; SetThreat 0 retourne Out Front en Alongside au passage", SG,
     [], verifier="fne3a_fin_de_round", attendu={"compteurs": [["60128b","speed",1]], "en_jeu": ["60129b"]},
     mise=["Puzzle.SetThreat('60128b', 0)"]),
 dict(cas("60129a Out Front [fne3a] — attachee au vilain : ses attaques gagnent ranged, la riposte de Black Panther ne le touche pas",
     "UnitAttackGainKeyword('AttachedEnemy', ranged) ; sans module la riposte (1) toucherait Hammerhead", SG,
     ["Puzzle.Attack('60086')"], {"degats": [["60086", 0]], "menace": [["60128b", 2]], "hotes": [["60129a","60086"]]},
     mise=[HERO_BP,"Puzzle.Exhaust('01040a')"]+PLAT), heros="black_panther"),
 cas("60129a Out Front [fne3a] — Forced Interrupt : 3 degats au vilain deviennent 3 menaces retirees du complot (5 -> 2), le vilain n'a rien",
     "WhenUnitWouldTakeDamage(Villain) + PreventDamage('All') + RemoveThreatFromSchemes('MainScheme', total)", SG,
     ["Puzzle.Damage('60086', 3)"], {"degats": [["60086", 0]], "menace": [["60128b", 2]]},
     mise=["Puzzle.SetThreat('60128b', 5)"]),
 cas("60129a Out Front [fne3a] — le retrait ignore la crise (Crowd Control 01108 en jeu) : 5 -> 2",
     "ignore_crisis=True (si007) ; Crowd Control porte l'icone crise", SG,
     ["Puzzle.Damage('60086', 3)"], {"degats": [["60086", 0]], "menace": [["60128b", 2]], "icones": [["Crisis", 1]]},
     mise=["Puzzle.SetThreat('60128b', 5)","Puzzle.PutIntoPlay('01108')"]),
 cas("60129a Out Front [fne3a] — plus de menace sur le complot : la carte se retourne (Alongside) et reste attachee au vilain",
     "AfterSchemeRemoveThreat('MainScheme') + RetournerLAttachement (card.Flip nu detache, RECETTES §7quater) ; 2 degats -> 2 menaces -> 0", SG,
     ["Puzzle.Damage('60086', 2)"], {"en_jeu": ["60129b"], "hors_jeu": ["60129a"], "hotes": [["60129b","60086"]], "menace": [["60128b", 0]]}),
 cas("60129a Out Front [fne3a] — un contre du heros ramene la menace a 0 : la carte se retourne aussi",
     "meme message AfterSchemeRemoveThreat, par un contre cette fois (1 menace, THW 1)", SG,
     ["Puzzle.Thwart('01001a')"], {"en_jeu": ["60129b"], "hors_jeu": ["60129a"], "hotes": [["60129b","60086"]], "menace": [["60128b", 0]]},
     mise=[HERO,"Puzzle.SetThreat('60128b', 1)"], cibles=["60128b"], main_exclusive=["01088"]),
 cas("60129b Alongside [fne3a] — When Revealed au retournement : chaque joueur prend 1 degat indirect, le vilain 2[per_hero] degats",
     "RetournerLAttachement(call_reveal=True) -> WhenThisRevealed ; Out Front n'est plus la pour convertir les 2 degats", SG,
     ["Puzzle.Damage('60086', 2)"], {"degats_identite": 1, "degats": [["60086", 2]], "en_jeu": ["60129b"]}),
 cas("60130 Escort Vehicle [fne3a] — guard, patrol (bases) ; 1 compteur speed : ni toughness, ni quickstrike, ni surge",
     "ThisGainKeyword(seuil, change_on_event=OnEvent.Counter(MainScheme, speed)) ; le Setup a pose 1 compteur", SG,
     ["Puzzle.PutIntoPlay('60130')"], verifier="fne3a_mots_cles",
     attendu={"carte": "60130", "guard": True, "patrol": True, "toughness": False, "quickstrike": False, "surge": False, "statuts_absents": [["60130","Tough"]]},
     mise=["Puzzle.EmptyEncounterDeck()"]),
 cas("60130 Escort Vehicle [fne3a] — 3 compteurs speed : gagne toughness et entre en jeu robuste",
     "seuil(3) ; Toughness pose le statut a l'entree en jeu (has_toughness.py)", SG,
     ["Puzzle.PutIntoPlay('60130')"], verifier="fne3a_mots_cles",
     attendu={"carte": "60130", "toughness": True, "quickstrike": False, "surge": False, "statuts": [["60130","Tough"]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.Counter('60128b', 'speed', 2)"]),
 cas("60130 Escort Vehicle [fne3a] — 6 compteurs speed : aussi quickstrike, il attaque en entrant (2 degats)",
     "seuil(6) ; Minion.OnEngagePlayer -> ResolveQuickstrike (heros incline : pas de defense)", SG,
     ["Puzzle.PutIntoPlay('60130')"], verifier="fne3a_mots_cles",
     attendu={"carte": "60130", "toughness": True, "quickstrike": True, "surge": False, "degats_identite": 2},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.Counter('60128b', 'speed', 5)",HERO,"Puzzle.Exhaust('01001a')"]),
 cas("60130 Escort Vehicle [fne3a] — 9 compteurs speed : aussi surge, le temoin du dessus du deck est revele",
     "seuil(9) ; en alter-ego, quickstrike n'attaque pas ; temoin Hydra Mercenary", SG,
     ["Puzzle.Reveal('60130')"], verifier="fne3a_mots_cles",
     attendu={"carte": "60130", "toughness": True, "quickstrike": True, "surge": True, "en_jeu": [TEMOIN]},
     mise=["Puzzle.EmptyEncounterDeck()",f"Puzzle.CreateEncounterDeck('{TEMOIN}')","Puzzle.Counter('60128b', 'speed', 8)"]),
 cas("60130 Escort Vehicle [fne3a] — contre-cas : deja en jeu quand le 3e compteur arrive, il gagne toughness SANS carte de statut (regle : a l'entree en jeu seulement)",
     "GainToughness ne touche que le compteur de mot-cle ; le statut Tough n'est pose que par OnWhenCardEnterPlay (has_toughness.py)", SG,
     ["Puzzle.Counter('60128b', 'speed', 2)"], verifier="fne3a_mots_cles",
     attendu={"carte": "60130", "toughness": True, "statuts_absents": [["60130","Tough"]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.PutIntoPlay('60130')"]),
 cas("60131 Jackknifed Tanker Truck [fne3a] — Hinder 1[per_hero] : 3 menaces, crise ; le vilain ne peut pas subir de degats (Out Front retiree)",
     "UnitCannotTakeDamage(Villain) ; Hinder/Crisis = bases desc ; Out Front retiree pour que rien ne convertisse les degats", SG,
     ["Puzzle.PutIntoPlay('60131')","Puzzle.Damage('60086', 3)"], {"menace": [["60131", 3]], "icones": [["Crisis", 1]], "degats": [["60086", 0]]},
     mise=["Puzzle.Remove('60129a')"]),
 cas("60131 Jackknifed Tanker Truck [fne3a] — avec Out Front en jeu : aucun degat ET aucune menace retiree (« cannot » prime sur « would »)",
     "les degats ne sont pas infliges, donc l'interruption d'Out Front n'a rien a convertir", SG,
     ["Puzzle.PutIntoPlay('60131')","Puzzle.Damage('60086', 3)"], {"degats": [["60086", 0]], "menace": [["60128b", 5]]},
     mise=["Puzzle.SetThreat('60128b', 5)"]),
 cas("60132 Burning Rubber [fne3a] — 1 compteur : premiere branche, 1 ressource depensee (Energy), pas de menace",
     "ForChoiceAbilityWithCost(Cost('1'), conditions=[PeutCouvrirLeCout]) ; main = Energy (YY)", SG,
     ["Puzzle.Reveal('60132')"], {"taille_main": 0, "menace": [["60128b", 2]]},
     mise=[HERO], main_exclusive=["01088"], payer_avec=["01088"]),
 cas("60132 Burning Rubber [fne3a] — 3 compteurs, une seule carte en main : 1 paiement, puis la branche payante n'est plus offerte : 2 menaces (2 -> 4)",
     "PourChaqueCompteurDeVitesse : un ChooseAbilities par compteur ; sans carte la condition cache la branche payante", SG,
     ["Puzzle.Reveal('60132')"], {"taille_main": 0, "menace": [["60128b", 4]]},
     mise=[HERO,"Puzzle.Counter('60128b', 'speed', 2)"], main_exclusive=["01088"], payer_avec=["01088"]),
 cas("60132 Burning Rubber [fne3a] — 2 compteurs, seconde branche choisie : 2 menaces (2 -> 4), la main est intacte",
     "preferer_option sur le libelle de la seconde branche", SG,
     ["Puzzle.Reveal('60132')"], {"taille_main": 1, "menace": [["60128b", 4]]},
     mise=[HERO,"Puzzle.Counter('60128b', 'speed', 1)"], main_exclusive=["01088"], preferer_option="Place 1 threat"),
 cas("60133 Pedestrians [fne3a] — 1 compteur : premiere branche, le heros est incline, 0 degat",
     "ForChoiceAbility(incliner, conditions=[un_pret_existe]) ; un seul personnage pret -> pas de question", SG,
     ["Puzzle.Reveal('60133')"], {"exhausted": ["01001a"], "degats_identite": 0},
     mise=[HERO], main_exclusive=["01088"]),
 cas("60133 Pedestrians [fne3a] — 2 compteurs, un seul personnage : incline au premier, plus rien de pret au second -> 1 degat indirect",
     "la branche « incliner » n'est plus offerte quand aucun personnage n'est pret", SG,
     ["Puzzle.Reveal('60133')"], {"exhausted": ["01001a"], "degats_identite": 1},
     mise=[HERO,"Puzzle.Counter('60128b', 'speed', 1)"], main_exclusive=["01088"]),
 cas("60133 Pedestrians [fne3a] — 2 compteurs, seconde branche choisie : 2 degats indirects, le heros reste pret",
     "preferer_option 'Take 1 indirect damage'", SG,
     ["Puzzle.Reveal('60133')"], {"pret": ["01001a"], "degats_identite": 2},
     mise=[HERO,"Puzzle.Counter('60128b', 'speed', 1)"], main_exclusive=["01088"], preferer_option="Take 1 indirect damage"),
 # ================================================================ The Raft Breakout
 cas("60142a The Raft Breakout 1A [fne3a] — Setup : Master Key attachee au vilain, un sbire PRISONER defausse depuis le deck et revele",
     "WhenCardSetup + Find.FindAndAttachTo (mise de cote) + DiscardEncounterCardsUntil(trait=PRISONER) + Reveal", SR, [],
     {"hotes": [["60143","60086"]], "en_jeu_trait": [["PRISONER", 1]]}),
 cas("60142b The Raft Breakout 1B [fne3a] — un sbire non-ELITE vaincu retire 1 menace du complot (5 -> 4)",
     "GiveAbilityToInPlayWhenApplyThis(Minion, abilities=[WhenUnitBeDefeated]) ; Hydra Mercenary 3 PV", SR,
     ["Puzzle.PutIntoPlay('01101')","Puzzle.Damage('01101', 3)"], {"menace": [["60142b", 4]], "hors_jeu": ["01101"]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.SetThreat('60142b', 5)"]),
 cas("60142b The Raft Breakout 1B [fne3a] — un sbire ELITE vaincu retire 2 menaces (5 -> 3)",
     "HasTrait('ELITE') -> 2 ; Drang 6 PV", SR,
     ["Puzzle.PutIntoPlay('60146')","Puzzle.Damage('60146', 6)"], {"menace": [["60142b", 3]], "hors_jeu": ["60146"]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.SetThreat('60142b', 5)"]),
 cas("60143 Master Key [fne3a] — le vilain manigance avec un sbire en boost : ce sbire est distribue au joueur face cachee apres l'activation",
     "WhenCardBecomeBoost(vilain_seulement, attaque=False) + AfterThisActivation + DealEncounterCard ; deck : Hydra Mercenary au dessus", SR,
     ["Puzzle.Scheme('60086')"], verifier="fne_carte_distribuee", attendu={"carte": TEMOIN, "joueur": 0},
     mise=["Puzzle.EmptyEncounterDeck()",f"Puzzle.CreateEncounterDeck('01186', '{TEMOIN}')"]),
 cas("60143 Master Key [fne3a] — contre-cas : le vilain ATTAQUE avec un sbire en boost, rien n'est distribue",
     "attaque=False : seule la manigance compte", SR,
     ["Puzzle.Attack('60086')"], verifier="fne_carte_distribuee", attendu={"carte": TEMOIN, "joueur": 0, "absente": True},
     mise=["Puzzle.EmptyEncounterDeck()",f"Puzzle.CreateEncounterDeck('01186', '{TEMOIN}')"]),
 cas("60143 Master Key [fne3a] — contre-cas : manigance avec une traitrise en boost, rien n'est distribue",
     "type_carte=Minion : Advance (traitrise) reste en defausse", SR,
     ["Puzzle.Scheme('60086')"], verifier="fne_carte_distribuee", attendu={"carte": "01186", "joueur": 0, "absente": True},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186', '01186')"]),
 cas("60144 Absorbing Man [fne3a] — attaque : la carte du dessus de mon deck (Energy) est glissee sous lui, +1 ATK (1 + 1 = 2)",
     "WhenUnitAttackYou ForcedInterrupt + TuckCardUnderHere + GetPrintedResourcesTypes + GainATKForThisAttack ; Villainous : Advance (0 icone)", SR,
     ["Puzzle.Attack('60144')"], {"degats_identite": 2, "pose_sous": [["60144","01088"]], "taille_pose_sous": [["60144", 1]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186', '01186', '01186')","Puzzle.PutIntoPlay('60144')",HERO,"Puzzle.Exhaust('01001a')","Puzzle.CreatePlayerDeck('01088')"]),
 cas("60144 Absorbing Man [fne3a] — deux attaques, Energy puis Genius : 2 types differents, +1 puis +2 (2 + 3 = 5)",
     "chaque type de ressource DIFFERENT compte une fois ; deck joueur : Genius sous Energy", SR,
     ["Puzzle.Attack('60144')","Puzzle.Attack('60144')"], {"degats_identite": 5, "taille_pose_sous": [["60144", 2]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186', '01186', '01186', '01186')","Puzzle.PutIntoPlay('60144')",HERO,"Puzzle.Exhaust('01001a')","Puzzle.CreatePlayerDeck('01089', '01088')"]),
 cas("60144 Absorbing Man [fne3a] — contre-cas : deux Energy glissees = un seul type, +1 puis +1 (2 + 2 = 4)",
     "« each different resource type » : deux [energy] ne valent qu'un", SR,
     ["Puzzle.Attack('60144')","Puzzle.Attack('60144')"], {"degats_identite": 4, "taille_pose_sous": [["60144", 2]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186', '01186', '01186', '01186')","Puzzle.PutIntoPlay('60144')",HERO,"Puzzle.Exhaust('01001a')","Puzzle.CreatePlayerDeck('01088', '01088')"]),
 cas("60145 Baron Zemo [fne3a] — When Revealed : 1 menace sur Hellcat, qui devient un sbire DECEIVED engage, SCH = son THW (2), texte vide",
     "Faces.PlaceTokensOn(threat) -> AfterCardPlacedToken(Ally, threat) -> ConvertirEnDeceived (gabarit deceived_minion, SwapCardFace) ; PV de l'allie conserves (3)", SR,
     ["Puzzle.Reveal('60145')"], verifier="fne3a_converti", attendu={"pic": "01020", "sch": 2, "joueur": 0, "trait": "DECEIVED", "jetons_menace": 1, "pv": 3},
     mise=["Puzzle.EmptyEncounterDeck()",HERO,"Puzzle.PutIntoPlay('01020', under_control=True)"]),
 cas("60145 Baron Zemo [fne3a] — Zemo quitte le jeu : Hellcat redevient un allie sous mon controle, la menace reste sur elle (FAQ)",
     "WhenCardLeavePlay('This') -> RendreLAllie (SwapBackToPrintedCard + PutIntoPlay under_control) ; les jetons restent", SR,
     ["Puzzle.Reveal('60145')","Puzzle.Damage('60145', 6)"], verifier="fne3a_converti", attendu={"pic": "01020", "absente": True, "allie": "01020", "joueur": 0, "jetons_menace": 1, "hors_jeu": ["60145"]},
     mise=["Puzzle.EmptyEncounterDeck()",HERO,"Puzzle.PutIntoPlay('01020', under_control=True)"]),
 cas("60145 Baron Zemo [fne3a] — la menace retiree de l'allie converti : il redevient un allie (Zemo toujours en jeu)",
     "AfterCardRemovedToken(DECEIVED, threat, 0 restant) -> RendreLAllie ; le verificateur retire le jeton du SBIRE converti (Puzzle.Token('01020') ne le trouve pas)", SR,
     ["Puzzle.Reveal('60145')"], verifier="fne3a_zemo_retrait", attendu={"pic": "01020", "absente": True, "allie": "01020", "joueur": 0, "jetons_menace": 0, "en_jeu": ["60145"]},
     mise=["Puzzle.EmptyEncounterDeck()",HERO,"Puzzle.PutIntoPlay('01020', under_control=True)"]),
 cas("60145 Baron Zemo [fne3a] — le sbire DECEIVED est vaincu : la carte redevient Hellcat et va dans MA defausse, plus aucun sbire converti",
     "Card.CheckIfCanDiscard remet la face imprimee avant la defausse (natif) ; le verificateur inflige 3 degats au sbire converti", SR,
     ["Puzzle.Reveal('60145')"], verifier="fne3a_zemo_vaincu", attendu={"pic": "01020", "absente": True, "defausse": ["01020"], "en_jeu": ["60145"]},
     mise=["Puzzle.EmptyEncounterDeck()",HERO,"Puzzle.PutIntoPlay('01020', under_control=True)"]),
 cas("60145 Baron Zemo [fne3a] — contre-cas : aucun allie en jeu, la revelation ne fait rien et ne plante pas",
     "liste vide -> return", SR,
     ["Puzzle.Reveal('60145')"], {"en_jeu": ["60145"], "menace": [["60142b", 2]]},
     mise=["Puzzle.EmptyEncounterDeck()",HERO]),
 cas("60146 Drang [fne3a] — apres son attaque : 1 compteur barrage, puis 1 degat indirect par compteur (1 + 0 + 1 = 2)",
     "AfterUnitAttackEnd ForcedResponse + PlaceCountersOn(barrage) + TakeIndirectDamage(n) ; Villainous : Advance (0 icone)", SR,
     ["Puzzle.Attack('60146')"], {"degats_identite": 2, "compteurs": [["60146","barrage",1]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186', '01186', '01186')","Puzzle.PutIntoPlay('60146')",HERO,"Puzzle.Exhaust('01001a')"]),
 cas("60146 Drang [fne3a] — deuxieme attaque : 2 compteurs, 2 indirects ((1 + 1) + (1 + 2) = 5)",
     "le barrage s'accumule", SR,
     ["Puzzle.Attack('60146')","Puzzle.Attack('60146')"], {"degats_identite": 5, "compteurs": [["60146","barrage",2]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186', '01186', '01186', '01186')","Puzzle.PutIntoPlay('60146')",HERO,"Puzzle.Exhaust('01001a')"]),
 cas("60147 Mysterio [fne3a] — apres son attaque, la traitrise en boost est distribuee au joueur face cachee",
     "WhenCardBecomeBoost(attaque=True, ennemi = this) + AfterThisActivation + DealEncounterCard ; boost = Advance", SR,
     ["Puzzle.Attack('60147')"], verifier="fne_carte_distribuee", attendu={"carte": "01186", "joueur": 0},
     mise=["Puzzle.EmptyEncounterDeck()",f"Puzzle.CreateEncounterDeck('{TEMOIN}', '01186')","Puzzle.PutIntoPlay('60147')",HERO,"Puzzle.Exhaust('01001a')"]),
 cas("60147 Mysterio [fne3a] — contre-cas : un sbire en boost n'est pas distribue",
     "type_carte=Treachery", SR,
     ["Puzzle.Attack('60147')"], verifier="fne_carte_distribuee", attendu={"carte": TEMOIN, "joueur": 0, "absente": True},
     mise=["Puzzle.EmptyEncounterDeck()",f"Puzzle.CreateEncounterDeck('01186', '{TEMOIN}')","Puzzle.PutIntoPlay('60147')",HERO,"Puzzle.Exhaust('01001a')"]),
 cas("60147 Mysterio [fne3a] — contre-cas : il MANIGANCE avec une traitrise en boost, rien n'est distribue",
     "attaque=True : seule l'attaque compte", SR,
     ["Puzzle.Scheme('60147')"], verifier="fne_carte_distribuee", attendu={"carte": "01186", "joueur": 0, "absente": True},
     mise=["Puzzle.EmptyEncounterDeck()",f"Puzzle.CreateEncounterDeck('{TEMOIN}', '01186')","Puzzle.PutIntoPlay('60147')"]),
 cas("60148 Proxima Midnight [fne3a] — attaque, premiere branche : 1 menace sur le complot principal (2 -> 3), ATK 2",
     "WhenUnitAttackYou ForcedInterrupt + ChooseAbilities ; le pilote prend la premiere branche", SR,
     ["Puzzle.Attack('60148')"], {"degats_identite": 2, "menace": [["60142b", 3]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186', '01186', '01186')","Puzzle.PutIntoPlay('60148')",HERO,"Puzzle.Exhaust('01001a')"]),
 cas("60148 Proxima Midnight [fne3a] — seconde branche : +2 ATK pour cette attaque (2 + 2 = 4), pas de menace",
     "preferer_option '+2 ATK' + GainATKForThisAttack(2)", SR,
     ["Puzzle.Attack('60148')"], {"degats_identite": 4, "menace": [["60142b", 2]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186', '01186', '01186')","Puzzle.PutIntoPlay('60148')",HERO,"Puzzle.Exhaust('01001a')"], preferer_option="+2 ATK"),
 cas("60149 Rhino [fne3a] — robuste a l'entree (Toughness) ; ses attaques gagnent overkill : Spider-Woman (2 PV) defend, 1 degat passe",
     "UnitAttackGainKeyword('This', overkill) ; Toughness = base desc", SR,
     ["Puzzle.Attack('60149', '01011')"], {"degats_identite": 1, "hors_jeu": ["01011"], "statuts": [["60149","Tough"]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186', '01186', '01186')","Puzzle.PutIntoPlay('60149')",HERO,"Puzzle.PutIntoPlay('01011', under_control=True)"]),
 cas("60149 Rhino [fne3a] — Boost : l'ennemi qui s'active (Hammerhead) devient robuste",
     "WhenCardBecomeBoost + GiveStatus(activating_enemy, Tough)", SR,
     ["Puzzle.Boost('60149')"], {"statuts": [["60086","Tough"]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186')",HERO,"Puzzle.Exhaust('01001a')"]),
 cas("60150 Imprisoned [fne3a] — obligation revelee : je ne peux pas attaquer (0 degat au vilain)",
     "PlayersCannotAttackWhile('You') ; l'obligation de rencontre va au joueur qui la revele (obligation.py)", SR,
     ["Puzzle.Attack('01001a')"], {"degats": [["60086", 0]], "en_jeu": ["60150"]},
     mise=["Puzzle.EmptyEncounterDeck()",HERO,"Puzzle.Reveal('60150')"], cibles=["60086"], main_exclusive=["01088"]),
 cas("60150 Imprisoned [fne3a] — je ne peux pas contrer (la menace reste a 5)",
     "PlayersCannotThwartWhile('You')", SR,
     ["Puzzle.SetThreat('60142b', 5)","Puzzle.Thwart('01001a')"], {"menace": [["60142b", 5]], "en_jeu": ["60150"]},
     mise=["Puzzle.EmptyEncounterDeck()",HERO,"Puzzle.Reveal('60150')"], cibles=["60142b"], main_exclusive=["01088"]),
 cas("60150 Imprisoned [fne3a] — je ne peux pas passer en alter-ego",
     "PlayersCannotChangeForms(to_form=AlterEgo)", SR,
     ["Puzzle.ChangeForm('01001a')"], {"forme": "Hero", "en_jeu": ["60150"]},
     mise=["Puzzle.EmptyEncounterDeck()",HERO,"Puzzle.Reveal('60150')"], main_exclusive=["01088"]),
 cas("60150 Imprisoned [fne3a] — Hero Action : 3 ressources quelconques (Energy YY + Genius BB) -> defaussee",
     "WhenInYourPlayTurn(HeroAction).SetCost(Cost('3'))", SR,
     ["Puzzle.Action('60150', 'HeroAction', 0)"], {"hors_jeu": ["60150"], "taille_main": 0},
     mise=["Puzzle.EmptyEncounterDeck()",HERO,"Puzzle.Reveal('60150')"], main_exclusive=["01088","01089"], payer_avec=["01088","01089"]),
 cas("60150 Imprisoned [fne3a] — Hero Action : incliner le heros (THW 1) et Hellcat (THW 2) = 3 -> defaussee",
     "seconde capacite, CostFunc.Custom(incliner_pour_trois_thw)", SR,
     ["Puzzle.Action('60150', 'HeroAction', 1)"], {"hors_jeu": ["60150"], "exhausted": ["01001a","01020"]},
     mise=["Puzzle.EmptyEncounterDeck()",HERO,"Puzzle.PutIntoPlay('01020', under_control=True)","Puzzle.Reveal('60150')"], main_exclusive=["01088"]),
 cas("60150 Imprisoned [fne3a] — contre-cas : THW total 1 (heros seul), la seconde capacite ne part pas, l'obligation reste",
     "Custom rend False, aucun personnage incline", SR,
     ["Puzzle.Action('60150', 'HeroAction', 1)"], {"en_jeu": ["60150"], "pret": ["01001a"]},
     mise=["Puzzle.EmptyEncounterDeck()",HERO,"Puzzle.Reveal('60150')"], main_exclusive=["01088"]),
 cas("60150 Imprisoned [fne3a] — Boost : la carte est revelee (elle entre en jeu chez le joueur)",
     "WhenCardBecomeBoost + Reveal(GetToPlayer)", SR,
     ["Puzzle.Boost('60150')"], {"en_jeu": ["60150"]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186')"]),
 # ================================================================ Stop the Presses!
 cas("60151a Stop the Presses! 1A [fne3a] — Setup : Daily Bugle en jeu, UN soutien DAILY BUGLE au hasard sous mon controle (3 stamina), les 3 autres retires du jeu",
     "WhenCardSetup + GetSetAsideAreaCards + Rand.RandomChoice + PutIntoPlay(under_control) + RemoveAllFromGame ; Uses (3 stamina) = base", SP, [],
     verifier="fne3a_bugle", attendu={"en_jeu": ["60152"], "n_soutiens": 1, "soutien": {"stamina": 3, "exhausted": False, "joueur": 0}, "n_retires": 3}),
 cas("60151b Stop the Presses! 1B [fne3a] — attaque non defendue du vilain, premiere branche : 2 menaces ici (1 -> 3)",
     "AfterUnitAttackUnit(Enemy, Identity, is_undefended_attack=True) ForcedResponse + ChooseAbilities (60121b)", SP,
     ["Puzzle.Attack('60086')"], {"menace": [["60151b", 3]]},
     mise=[HERO,"Puzzle.Exhaust('01001a')"]+PLAT),
 dict(cas("60151b Stop the Presses! 1B [fne3a] (expert) — 3 menaces au lieu de 2 (1 -> 4)",
     "Worlds.IsExpert -> 3 ; vilain expert = Hammerhead II", SP+"_expert",
     ["Puzzle.Attack('60087')"], {"menace": [["60151b", 4]]},
     mise=[HERO,"Puzzle.Exhaust('01001a')"]+PLAT), ),
 cas("60151b Stop the Presses! 1B [fne3a] — seconde branche : 1 stamina retiree du soutien DAILY BUGLE que je controle (3 -> 2), pas de menace",
     "preferer_option 'Remove 1 stamina' + RetirerUneEndurance", SP,
     ["Puzzle.Attack('60086')"], verifier="fne3a_bugle", attendu={"soutien": {"stamina": 2}, "menace": [["60151b", 1]]},
     mise=[HERO,"Puzzle.Exhaust('01001a')"]+PLAT, preferer_option="Remove 1 stamina"),
 cas("60151b Stop the Presses! 1B [fne3a] — contre-cas : attaque DEFENDUE par le heros, rien (menace 1)",
     "is_undefended_attack=True exclut l'attaque defendue", SP,
     ["Puzzle.Attack('60086', '01001a')"], {"menace": [["60151b", 1]]},
     mise=[HERO]+PLAT),
 cas("60151b Stop the Presses! 1B [fne3a] — un soutien DAILY BUGLE quitte le jeu (dernier stamina retire) : les joueurs perdent",
     "WhenCardLeavePlay(DAILY BUGLE Support) ForcedInterrupt + SetGameOver(False) ; le verificateur retire les 3 pions (Uses fait sortir la carte)", SP,
     [], verifier="fne3a_bugle_perte", attendu={}),
 cas("60152 Daily Bugle [fne3a] — Alter-Ego Action : incliner mon soutien DAILY BUGLE -> +1 stamina dessus (3 -> 4)",
     "WhenInYourPlayTurn(AlterEgoAction) + CostFunc.Exhaust(finder) + return_exhausted_cards", SP,
     ["Puzzle.Action('60152', 'AlterEgoAction', 0)"], verifier="fne3a_bugle", attendu={"soutien": {"stamina": 4, "exhausted": True}},
     main_exclusive=["01088"]),
 cas("60153 Ben Urich [fne3a] — Action : incliner + 1 stamina -> regarde les 2 cartes du dessus du deck rencontre, en defausse 1",
     "LookAtDeck('EncounterDeck', 2) + AskChooseFace(may=True) + DiscardAll ; deck : Hydra Mercenary, Advance, Under Fire", SP,
     ["Puzzle.Action('60153', 'Action', 0)"], {"compteurs": [["60153","stamina",2]], "exhausted": ["60153"], "defausse_rencontre": [TEMOIN]},
     mise=["Puzzle.EmptyEncounterDeck()",f"Puzzle.CreateEncounterDeck('01193', '01186', '{TEMOIN}')","Puzzle.PutIntoPlay('60153', under_control=True)",HERO], main_exclusive=["01088"]),
 cas("60154 Betty Brant [fne3a] — Interrupt : la carte boost retournee (Under Fire, 3 icones) est annulee, une autre (Advance, 0) la remplace : 1 + 0 = 1",
     "WhenBoostCardWouldTurnedFaceUp + SetBeInstead + DiscardAll + GiveFacedownBoostCardsInternal(1) ; sans module : 1 + 3 = 4", SP,
     ["Puzzle.Attack('60086')"], {"degats_identite": 1, "compteurs": [["60154","stamina",2]], "exhausted": ["60154"], "defausse_rencontre": ["01193"]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01193', '01186', '01193')","Puzzle.PutIntoPlay('60154', under_control=True)",HERO,"Puzzle.Exhaust('01001a')"], main_exclusive=["01088"]),
 cas("60154 Betty Brant [fne3a] — contre-cas : Betty deja inclinee, l'interruption n'est pas offerte (1 + 3 = 4)",
     "le cout Exhaust('This') n'est pas payable", SP,
     ["Puzzle.Attack('60086')"], {"degats_identite": 4, "compteurs": [["60154","stamina",3]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01193', '01186', '01193')","Puzzle.PutIntoPlay('60154', under_control=True)","Puzzle.Exhaust('60154')",HERO,"Puzzle.Exhaust('01001a')"], main_exclusive=["01088"]),
 cas("60155 J. Jonah Jameson [fne3a] — Action : incliner + 1 stamina + 1 carte rencontre face cachee -> pioche 2 (main 1 -> 3)",
     "trois couts dont CostFunc.DealPlayerEncounterCard(1, 'Initiator') ; DrawUp(2)", SP,
     ["Puzzle.Action('60155', 'Action', 0)"], verifier="fne3a_bugle", attendu={"distribuees_min": 1, "taille_main": 3, "compteurs": [["60155","stamina",2]], "exhausted": ["60155"]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186', '01186')","Puzzle.PutIntoPlay('60155', under_control=True)",HERO], main_exclusive=["01088"]),
 cas("60156 Robbie Robertson [fne3a] — Response : la carte distribuee (Hydra Mercenary) est regardee, defaussee, et une autre (Advance) est distribuee a la place",
     "AfterPlayerDealEncounterCard + AskChooseFace(forced=False) + DiscardAll + DealEncounterCards(1) ; Puzzle.Deal distribue la carte du dessus ; Under Fire au fond pour que le deck ne remelange pas sa defausse", SP,
     [f"Puzzle.Deal('{TEMOIN}')"], verifier="fne3a_bugle", attendu={"distribuees": ["01186"], "defausse_rencontre": [TEMOIN], "compteurs": [["60156","stamina",2]], "exhausted": ["60156"]},
     mise=["Puzzle.EmptyEncounterDeck()",f"Puzzle.CreateEncounterDeck('01193', '01186', '{TEMOIN}')","Puzzle.PutIntoPlay('60156', under_control=True)",HERO], main_exclusive=["01088"]),
 cas("60157 Exclusive Interview [fne3a] — When Revealed : chaque soutien DAILY BUGLE est incline ; 6 menaces",
     "Faces.ExhaustAll(SoutiensDailyBugle) ; Ben Urich ajoute au soutien du Setup", SP,
     ["Puzzle.Reveal('60157')"], verifier="fne3a_bugle", attendu={"soutiens_tous_inclines": True, "exhausted": ["60153"], "menace": [["60157", 6]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.PutIntoPlay('60153', under_control=True)",HERO]),
 cas("60157 Exclusive Interview [fne3a] — les soutiens DAILY BUGLE ne peuvent pas se redresser",
     "CardCannotReady(finder) ; Puzzle.Ready sur Ben Urich incline", SP,
     ["Puzzle.Ready('60153')"], {"exhausted": ["60153"], "en_jeu": ["60157"]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.EmptyPlayerDeck()","Puzzle.PutIntoPlay('60153', under_control=True)",HERO,"Puzzle.Reveal('60157')"]),
 cas("60157 Exclusive Interview [fne3a] — contre-cas : sans elle, Ben Urich se redresse",
     "temoin du harnais : Puzzle.Ready redresse bien un soutien", SP,
     ["Puzzle.Ready('60153')"], {"pret": ["60153"]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.EmptyPlayerDeck()","Puzzle.PutIntoPlay('60153', under_control=True)",HERO,"Puzzle.Exhaust('60153')"]),
 cas("60158 Breaking News [fne3a] — When Revealed, premiere branche : mon soutien DAILY BUGLE est incline et perd 1 stamina (3 -> 2)",
     "ChooseAbilities + ExhaustAll + RetirerUneEndurance ; un seul soutien : pas de question", SP,
     ["Puzzle.Reveal('60158')"], verifier="fne3a_bugle", attendu={"soutien": {"stamina": 2, "exhausted": True}, "menace": [["60151b", 1]]},
     mise=[HERO]),
 cas("60158 Breaking News [fne3a] — seconde branche : 2 menaces sur le complot principal (1 -> 3), le soutien intact",
     "preferer_option 'Place 2 threat'", SP,
     ["Puzzle.Reveal('60158')"], verifier="fne3a_bugle", attendu={"soutien": {"stamina": 3, "exhausted": False}, "menace": [["60151b", 3]]},
     mise=[HERO], preferer_option="Place 2 threat"),
 cas("60158 Breaking News [fne3a] — Boost : mon soutien DAILY BUGLE est incline (stamina intacte)",
     "WhenCardBecomeBoost + ExhaustAll", SP,
     ["Puzzle.Boost('60158')"], verifier="fne3a_bugle", attendu={"soutien": {"stamina": 3, "exhausted": True}},
     mise=[HERO,"Puzzle.Exhaust('01001a')"]+PLAT),
]
DEBUT="    # ------------------------------------------------------------------------\n    # Pack officiel « fne » — bloc 3A"
FIN="    # ---- fin du bloc 3A fne ----\n"
bloc = DEBUT + " : The Getaway, The Raft Breakout, Stop the Presses!\n    # (18/09/2026). Filtre : \"[fne3a]\". Genere par scratchpad/b3/gen_cas_fne_a.py.\n    # ------------------------------------------------------------------------\n"
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
# ---------------------------------------------------------------- pack fne (bloc 3A)
def fne3a_fin_de_round(monde, aides):
    """Envoie WhenRoundEnd (modele brawn_hulk_out_fin_de_round) puis delegue
    a etat_attendu : The Getaway 1B (60128b)."""
    from game.message import Message
    Message.WhenRoundEnd(monde).Send()
    return etat_attendu(monde, aides)

def fne3a_mots_cles(monde, aides):
    """`attendu.carte` porte (ou non) guard / patrol / toughness / quickstrike /
    surge / villainous, puis le reste des cles est delegue a etat_attendu."""
    attendu = aides["cas"].get("attendu") or {}
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} introuvable en jeu"
    soucis = []
    for mot, fn in (("guard", "IsGuard"), ("patrol", "IsPatrol"), ("villainous", "IsVillainous"),
                    ("toughness", "IsToughness"), ("quickstrike", "IsQuickstrike")):
        if mot in attendu and bool(getattr(face, fn)()) != attendu[mot]:
            soucis.append(f"{attendu['carte']}.{mot} = {getattr(face, fn)()} (attendu {attendu[mot]})")
    if "surge" in attendu and bool(getattr(face, "surge", 0)) != attendu["surge"]:
        soucis.append(f"{attendu['carte']}.surge = {getattr(face, 'surge', None)} (attendu {attendu['surge']})")
    reste = {k: v for k, v in attendu.items() if k in CLES_ETAT_ATTENDU}
    if reste:
        copie = dict(aides); copie["cas"] = dict(aides["cas"]); copie["cas"]["attendu"] = reste
        ok, msg = etat_attendu(monde, copie)
        if not ok:
            soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, "mots-cles conformes"

def fne3a_converti(monde, aides):
    """Baron Zemo : la face de sbire (pic = l'allie) est en jeu (ou `absente`),
    engagee avec `joueur`, SCH attendu, trait attendu ; `allie` : l'allie
    imprime est de retour en jeu sous le controle de `joueur` ; `jetons_menace` :
    menace portee par la carte (sbire ou allie) ; le reste -> etat_attendu."""
    from game.card.face.card_type import Minion, Ally
    attendu = aides["cas"].get("attendu") or {}
    trouve = None
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is None or not face.IsInPlay() or not Minion.IsType(face):
            continue
        if getattr(face, "pic_id", None) == attendu["pic"]:
            trouve = face
    soucis = []
    joueur = monde.players[attendu.get("joueur", 0)]
    porteur = None
    if attendu.get("absente"):
        if trouve is not None:
            soucis.append(f"un sbire converti a l'image de {attendu['pic']} est encore en jeu")
    else:
        if trouve is None:
            return False, f"aucun sbire converti a l'image de {attendu['pic']} en jeu"
        porteur = trouve
        if trouve.engaged_player is not joueur:
            soucis.append("pas engage avec le joueur attendu")
        if "sch" in attendu and trouve.scheme != attendu["sch"]:
            soucis.append(f"SCH = {trouve.scheme} (attendu {attendu['sch']})")
        if attendu.get("trait") and not trouve.HasTrait(attendu["trait"]):
            soucis.append(f"trait {attendu['trait']} absent")
    if attendu.get("allie"):
        allie = aides["par_id"](monde, attendu["allie"])
        if allie is None or not Ally.IsType(allie):
            soucis.append(f"{attendu['allie']} n'est pas de retour en jeu comme allie")
        else:
            porteur = allie
            if allie.GetControlByPlayer() is not joueur:
                soucis.append(f"{attendu['allie']} n'est pas sous le controle du joueur attendu")
    if "pv" in attendu and porteur is not None and getattr(porteur, "max_health", None) != attendu["pv"]:
        soucis.append(f"PV max de {attendu['pic']} = {getattr(porteur, 'max_health', None)} (attendu {attendu['pv']})")
    if "jetons_menace" in attendu and porteur is not None:
        n = porteur.GetTokens('threat')
        if n != attendu["jetons_menace"]:
            soucis.append(f"menace sur {attendu['pic']} = {n} (attendu {attendu['jetons_menace']})")
    reste = {k: v for k, v in attendu.items() if k in CLES_ETAT_ATTENDU}
    if reste:
        copie = dict(aides); copie["cas"] = dict(aides["cas"]); copie["cas"]["attendu"] = reste
        ok, msg = etat_attendu(monde, copie)
        if not ok:
            soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, "conversion conforme"

def fne3a_zemo_retrait(monde, aides):
    """Retire 1 jeton threat du sbire converti (pic = attendu.pic), comme un
    contre le ferait, puis delegue a fne3a_converti."""
    from game.card.face.card_type import Minion
    from game.operate.faces import Faces
    from game.effect.rule import DebugRule
    attendu = aides["cas"].get("attendu") or {}
    sbire = None
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and face.IsInPlay() and Minion.IsType(face) and getattr(face, "pic_id", None) == attendu["pic"]:
            sbire = face
    if sbire is None:
        return False, f"aucun sbire converti a l'image de {attendu['pic']} avant le retrait du jeton"
    Faces.RemoveTokensOn([sbire], 1, 'threat', DebugRule(sbire))
    return fne3a_converti(monde, aides)

def fne3a_zemo_vaincu(monde, aides):
    """Inflige 3 degats au sbire converti (pic = attendu.pic) depuis Zemo, puis
    delegue a fne3a_converti (absente + defausse du joueur)."""
    from game.card.face.card_type import Minion
    from game.effect.rule import DebugRule
    attendu = aides["cas"].get("attendu") or {}
    sbire = None
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and face.IsInPlay() and Minion.IsType(face) and getattr(face, "pic_id", None) == attendu["pic"]:
            sbire = face
    if sbire is None:
        return False, f"aucun sbire converti a l'image de {attendu['pic']} avant les degats"
    # Meme chemin que Puzzle.Damage : TakeDamage(source, n, DebugRule) ;
    # `DealDamage` exige un vrai Effect (`.ability`), pas une DebugRule.
    sbire.TakeDamage(sbire, 3, DebugRule(sbire))
    return fne3a_converti(monde, aides)

def _fne3a_soutiens_bugle(monde):
    from game.card.face.card_type import Support
    from game.operate.worlds import Worlds
    return [f for f in Worlds.GetOnFieldCards(monde.players[0].GetIdentity().card.game_area)
            if Support.IsType(f) and f.HasTrait("DAILY BUGLE")]

def fne3a_bugle(monde, aides):
    """Stop the Presses! (independant de la graine) : `n_soutiens` = nombre de
    soutiens DAILY BUGLE en jeu ; `soutien` = {stamina, exhausted, joueur} lu
    sur l'UNIQUE soutien en jeu ; `soutiens_tous_inclines` ; `n_retires` =
    soutiens DAILY BUGLE retires du jeu ; `distribuees` / `distribuees_min` =
    cartes rencontre face cachee du joueur 0 ; le reste -> etat_attendu."""
    from game.card.face.card_type import Support
    attendu = aides["cas"].get("attendu") or {}
    soutiens = _fne3a_soutiens_bugle(monde)
    ids = [getattr(f.paper, "card_id", "?") for f in soutiens]
    soucis = []
    if "n_soutiens" in attendu and len(soutiens) != attendu["n_soutiens"]:
        soucis.append(f"soutiens DAILY BUGLE en jeu = {ids} (attendu {attendu['n_soutiens']})")
    if attendu.get("soutien"):
        if len(soutiens) != 1:
            soucis.append(f"il faut exactement UN soutien DAILY BUGLE en jeu pour lire `soutien` (en jeu : {ids})")
        else:
            s0 = soutiens[0]; v = attendu["soutien"]
            if "stamina" in v and s0.GetCounters('stamina') != v["stamina"]:
                soucis.append(f"{ids[0]} stamina = {s0.GetCounters('stamina')} (attendu {v['stamina']})")
            if "exhausted" in v and bool(s0.IsExhaust()) != v["exhausted"]:
                soucis.append(f"{ids[0]} exhausted = {s0.IsExhaust()} (attendu {v['exhausted']})")
            if "joueur" in v and s0.GetControlByPlayer() is not monde.players[v["joueur"]]:
                soucis.append(f"{ids[0]} n'est pas controle par le joueur {v['joueur']}")
    if attendu.get("soutiens_tous_inclines") and any(not f.IsExhaust() for f in soutiens):
        soucis.append(f"un soutien DAILY BUGLE est encore pret ({ids})")
    if "n_retires" in attendu:
        retires = [f for f in monde.area_removed.Get(True) if Support.IsType(f) and f.HasTrait("DAILY BUGLE")]
        if len(retires) != attendu["n_retires"]:
            soucis.append(f"soutiens DAILY BUGLE retires du jeu = {len(retires)} (attendu {attendu['n_retires']})")
    distribuees = [getattr(f.paper, "card_id", None) for f in monde.players[0].dealt_encounter_cards.Get(True)]
    if "distribuees" in attendu and sorted(distribuees) != sorted(attendu["distribuees"]):
        soucis.append(f"cartes distribuees = {distribuees} (attendu {attendu['distribuees']})")
    if "distribuees_min" in attendu and len(distribuees) < attendu["distribuees_min"]:
        soucis.append(f"cartes distribuees = {distribuees} (au moins {attendu['distribuees_min']} attendue)")
    reste = {k: v for k, v in attendu.items() if k in CLES_ETAT_ATTENDU}
    if reste:
        copie = dict(aides); copie["cas"] = dict(aides["cas"]); copie["cas"]["attendu"] = reste
        ok, msg = etat_attendu(monde, copie)
        if not ok:
            soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"soutiens = {ids}, distribuees = {distribuees}"

def fne3a_bugle_perte(monde, aides):
    """Retire les 3 stamina de l'unique soutien DAILY BUGLE (Uses le fait
    sortir du jeu), puis verifie que la partie est finie ET perdue."""
    from game.operate.faces import Faces
    from game.effect.rule import DebugRule
    soutiens = _fne3a_soutiens_bugle(monde)
    if len(soutiens) != 1:
        return False, f"il faut exactement UN soutien DAILY BUGLE en jeu ({len(soutiens)})"
    s0 = soutiens[0]
    Faces.RemoveCountersOn([s0], 3, 'stamina', DebugRule(s0))
    if s0.IsInPlay():
        return False, "le soutien est encore en jeu apres le retrait des 3 pions (Uses)"
    if not getattr(monde, "is_game_over", False):
        return False, "le soutien a quitte le jeu mais la partie continue"
    gagnee = getattr(monde, "is_players_win", None)
    if gagnee is None:
        gagnee = getattr(monde, "players_win", None)
    if gagnee:
        return False, "partie terminee mais GAGNEE"
    return True, "le soutien a quitte le jeu, partie perdue"

# ---- fin des verificateurs bloc 3A ----
'''
MARQ="# ---------------------------------------------------------------- pack fne (bloc 3A)"
FINV="# ---- fin des verificateurs bloc 3A ----\n"
if MARQ in s:
    i=s.index(MARQ); j=s.index(FINV, i)+len(FINV); s=s[:i]+VERIFS.lstrip("\n")+s[j:]
else:
    # Juste AVANT le marqueur du bloc 2 : le generateur du bloc 2 REMPLACE tout
    # ce qui va de son marqueur a `def etat_attendu`, un bloc pose entre les
    # deux y serait efface a sa prochaine regeneration.
    ancre="# ---------------------------------------------------------------- pack fne (bloc 2)"
    assert ancre in s, "ancre verifs bloc 2"
    s=s.replace(ancre, VERIFS.lstrip("\n")+"\n"+ancre, 1)
io.open(p,'w',encoding='utf8').write(s)
import ast; ast.parse(s)
print("cas [fne3a]:", len(CAS), "; syntaxe OK")
