# Cas test_capacites du heros 3-D MAN (Delroy Garrett Jr., pack three_d_man, prefixe `dm`) : noms commencant par
# le card_id (substituer_pack.py filtre dessus : `tools/substituer_pack.py <game_dir> <port> dm0`).
#
# Rappels de montage :
#  - le deck `three_d_man` demarre en ALTER EGO (dm001b) ; `Puzzle.ChangeToFace('dm001b', 'dm001a')` le passe en
#    HEROS (3-D Man) ;
#  - Rhino 01094 est le vilain (scenario 'rhino', meme scenario que carnage/sentry/multiple_man), 01097a/01097b
#    ses complots ; 01101 Hydra Mercenary (3 PV) sert de sbire-temoin ;
#  - ressources du deck (dm022 Energy = YY, dm023 Genius = BB, dm024 Strength = RR) ; 01088/01089/01090
#    (officielles, memes couleurs) servent quand un montage a besoin d'une seule icone ;
#  - `Puzzle.EmptyHand()` avant tout montage qui compte sur une main precise.
HEROS = "Puzzle.ChangeToFace('dm001b', 'dm001a')"
VILAIN = '01094'
COMPLOT = '01097b'


def M(carte):
    return f"Puzzle.PutIntoPlay('{carte}', under_control=True)"


def DECK(*cartes):
    """Deck Rencontre dont la PREMIERE carte citee est le DESSUS (`CreateEncounterDeck` empile : la derniere creee est au-dessus)."""
    return ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(" + ", ".join(f"'{c}'" for c in reversed(cartes)) + ")"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {'nom': nom, 'pourquoi': pourquoi, 'scenario': cle.pop('scenario', 'rhino'), 'heros': cle.pop('heros', 'three_d_man'),
           'mise_en_place': list(mise), 'declencher': list(declencher), 'verifier': cle.pop('verifier', 'etat_attendu'), 'attendu': attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ dm001a 3-D Man (face heros)
    _c("dm001a Action — reduit de 1 le cout de la prochaine carte jouee ce tour : Tri-Force Vision (cout 1, main sans aucune ressource) se joue quand meme",
       "modele us009 (`Worlds.UpdateNextCardPlayCost`), meme fabrique que bg012/dm007 de cette session",
       ["Puzzle.EmptyHand()", HEROS], ["Puzzle.Action('dm001a')"],
       {'absent_main': ['dm002']}, main_exclusive=['dm002'], jouer=['dm002']),
    _c("dm001a Strength & Spirit of Three Men — Interrupt : en defaussant Energy, le pouvoir de base (ATK 1) est porte a 3 pour cette attaque (1 -> 3 sur Rhino)",
       "ARBITRAGE UTILISATEUR (04/11/2026) : ecart calcule contre `this.printed_attack` (1), bonus +2 -> 3 au total",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", HEROS, "Puzzle.CreateHandCards('dm022')"], ["Puzzle.Attack('dm001a')"],
       {'degats': [[VILAIN, 3]]}, accepter_choix=True),
    _c("dm001a Strength & Spirit of Three Men — TEMOIN : aucune carte a defausser (main vide) : le cout est impayable, le pouvoir de base reste a 1",
       "le cout (`CostFunc.Discard`) est optionnel : sans carte, l'Interruption ne part pas",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", HEROS], ["Puzzle.Attack('dm001a')"],
       {'degats': [[VILAIN, 1]]}),

    # ============================================================ dm002 Tri-Force Vision
    _c("dm002 Tri-Force Vision — Hero Action : regarde les 3 dessus du deck de rencontre, les remet dans le MEME ordre -> remelange jusqu'a 3 cartes de la defausse joueur dans le deck",
       "modele uj016 (`LookAtDeck` + `PlaceOnTopInAnyOrder`) + rm008 (`AskChooseFaces` + `ShuffleAllTo`)",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', '01102', '01107')",
        "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDiscardPile('dm023', 'dm024')", HEROS, "Puzzle.Action('dm001a')"],
       [],
       {'taille_deck_joueur': 2, 'defausse_joueur': 1}, main_exclusive=['dm002'], jouer=['dm002'], accepter_choix=True),

    # ============================================================ dm003 Triple the Beatdown
    _c("dm003 Triple the Beatdown — Hero Action (attack) : 3 degats sur le vilain ET 3 sur un sbire distinct (deux cibles simultanees)",
       "modele 27182b (`.SetTarget(Enemy, range=(1,2))` + un seul `DealDamage` sur la liste)",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", HEROS, "Puzzle.PutIntoPlay('01101')"], [],
       {'degats': [[VILAIN, 3]], 'hors_jeu': ['01101']}, main_exclusive=['dm003', 'dm024', 'dm023'], jouer=['dm003'], cibles=[VILAIN, '01101'], accepter_choix=True),
    _c("dm003 Triple the Beatdown — cout REDUIT (Action de dm001a avant) : 3-D Man (epuise avant) est redresse",
       "« If you reduced this card's cost, ready 3-D Man » : `CoutReduit` compare le paye au cout IMPRIME (3)",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", HEROS, "Puzzle.Exhaust('dm001a')", "Puzzle.Action('dm001a')"], [],
       {'pret': ['dm001a']}, main_exclusive=['dm003', 'dm024'], jouer=['dm003'], cibles=[VILAIN], accepter_choix=True),
    _c("dm003 Triple the Beatdown — TEMOIN : cout PLEIN (pas d'Action dm001a) : 3-D Man (epuise avant) reste epuise",
       "sans reduction, `CoutReduit` rend faux",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", HEROS, "Puzzle.Exhaust('dm001a')"], [],
       {'exhausted': ['dm001a']}, main_exclusive=['dm003', 'dm024', 'dm023'], jouer=['dm003'], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ dm004 Triple the Heroics
    _c("dm004 Triple the Heroics — Hero Action (thwart) : 3 menaces retirees du complot principal ET 3 d'un complot annexe distinct",
       "meme patron que dm003, cote manigance (`RemoveThreatFromSchemes` sur deux cibles)",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 4)"], [],
       {'menace': [[COMPLOT, 2], ['01107', 1]]}, main_exclusive=['dm004', 'dm023', 'dm022'], jouer=['dm004'], cibles=['01107', COMPLOT], accepter_choix=True),

    # ============================================================ dm005 Triple the Effectiveness
    _c("dm005 Triple the Effectiveness — Hero Interrupt (defense) : l'attaque de Shocker (ATK 2, DEF 3-D Man 1 -> 1 degat net AVANT dm005) est reduite a 0, 3 menaces retirees du complot, 3 degats sur le vilain",
       "modele sm010 (`message.ReduceDamage`) + sj011 (deux cibles de types differents) + bw005/03005 (joue en defense) ; Hydra Mercenary (ATK 1) donnait un degat net NUL (1-1=0) AVANT meme dm005 -- `WhenUnitWouldTakeDamage` ne se declenche jamais s'il n'y a rien a prevenir, d'ou Shocker (ATK 2) pour un degat net reellement positif a reduire ; `ne_pas_depenser=['dm005']` + une 3e carte en main (dm024) + `cibles=['dm024', ...]` : SANS eux, l'Interruption 'Strength & Spirit of Three Men' de dm001a (declenchee par le pouvoir de base DEF) defausse dm005 LUI-MEME pour payer son propre cout",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.PutIntoPlay('01103')"],
       ["Puzzle.EnemyAttacks('01103', 'dm001a')"],
       {'degats_identite': 0, 'menace': [[COMPLOT, 2]], 'degats': [[VILAIN, 3]]},
       main_exclusive=['dm005', 'dm022', 'dm023', 'dm024'], ne_pas_depenser=['dm005'], cibles=['dm024', VILAIN, COMPLOT], accepter_choix=True,
       preferer_option='Triple the Effectiveness', passer_sur_option='Strength'),

    # ============================================================ dm006 3-D Men Combined
    _c("dm006 3-D Men Combined — Hero Action : redresse jusqu'a 3 cartes controlees (ici dm007, incline) ; cout PLEIN -> aucun degat (pas de bonus)",
       "modele lj029/ar003 (`CardFinder()` + `from_where=['YouControlCards']`, `canbe_ready=True`)",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", HEROS, "Puzzle.PutIntoPlay('dm007', under_control=True, exhaust=True)"], [],
       {'pret': ['dm007'], 'degats': [[VILAIN, 0]]}, main_exclusive=['dm006', 'dm023', 'dm024'], jouer=['dm006'], cibles=['dm007'], accepter_choix=True),
    _c("dm006 3-D Men Combined — cout REDUIT (Action dm001a avant) : 1 degat par carte redressee (ici 1) sur le vilain",
       "« for each card readied this way, deal 3 damage » : 1 carte redressee -> 3 degats",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", HEROS, "Puzzle.Action('dm001a')", "Puzzle.PutIntoPlay('dm007', under_control=True, exhaust=True)"], [],
       {'degats': [[VILAIN, 3]]}, main_exclusive=['dm006', 'dm024'], jouer=['dm006'], cibles=['dm007'], accepter_choix=True),

    # ============================================================ dm007 3-D Man's Suit
    _c("dm007 3-D Man's Suit — Interrupt : entree en jeu depuis la main -> soigne 1 degat de l'identite",
       "modele il002/hp011 (`WhenCardEnterPlay` + `HealthUnits`)",
       ["Puzzle.EmptyHand()", HEROS, "Puzzle.Damage('dm001a', 4)"], [],
       {'degats_identite': 3}, main_exclusive=['dm007', 'dm024'], jouer=['dm007']),
    _c("dm007 3-D Man's Suit — Hero Action : defausse la carte -> le prochain evenement joue ce tour (dm002, cout 1) se joue sans aucune ressource en main",
       "ARBITRAGE UTILISATEUR (04/11/2026) : `AbilityType.HeroAction` qui ARME la reduction (meme blocage moteur que bg012)",
       ["Puzzle.EmptyHand()", HEROS, M('dm007')], ["Puzzle.Action('dm007')"],
       {'hors_jeu': ['dm007'], 'absent_main': ['dm002']}, main_exclusive=['dm002'], jouer=['dm002']),

    # ============================================================ dm008 True Sight
    _c("dm008 True Sight — Interrupt : entree en jeu depuis la main -> retire 2 menaces d'un complot",
       "modele 03002 (`RemoveThreatFromSchemes`)",
       ["Puzzle.EmptyHand()", HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {'menace': [[COMPLOT, 3]]}, main_exclusive=['dm008', 'dm024'], jouer=['dm008'], cibles=[COMPLOT], accepter_choix=True),
    _c("dm008 True Sight — Hero Action : defausse la carte, choix 2 -> retire un statut (Confused) d'Hydra Mercenary",
       "modele 16155 (`ChooseAbilities` + `Faces.RemoveAllFromGame(StatusCard)`)",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", HEROS, M('dm008'), "Puzzle.PutIntoPlay('01101')", "Puzzle.Confuse('01101')"], ["Puzzle.Action('dm008')"],
       {'hors_jeu': ['dm008'], 'statuts_absents': [['01101', 'Confused']]}, preferer_option='Remove a status card from any character', cibles=['01101'], accepter_choix=True),

    # ============================================================ dm009 The Triune Understanding
    _c("dm009 The Triune Understanding — Alter-Ego Action : ajoute 1 menace au complot principal, s'incline -> le prochain evenement signature (dm002, cout 1) se joue sans ressource",
       "`PlaceThreatOnSchemes('MainScheme', 1)` + `Worlds.UpdateNextCardPlayCost` (modele bg012/dm007)",
       ["Puzzle.EmptyHand()", f"Puzzle.SetThreat('{COMPLOT}', 2)", M('dm009')], ["Puzzle.Action('dm009')", HEROS],
       {'menace': [[COMPLOT, 3]], 'exhausted': ['dm009'], 'absent_main': ['dm002']}, main_exclusive=['dm002'], jouer=['dm002']),

    # ============================================================ dm010 Tri-Power
    _c("dm010 Tri-Power — Hero Response : apres avoir depense la ressource, 3-D Man (epuise avant) est redresse",
       "modele 56132 (`AfterYouSpendThisCard`) + sk019 (`Faces.ReadyAll`)",
       ["Puzzle.EmptyHand()", HEROS, "Puzzle.Exhaust('dm001a')"], [],
       {'pret': ['dm001a']}, main_exclusive=['dm002', 'dm010'], jouer=['dm002'], payer_avec=['dm010']),

    # ============================================================ dm011 Arrival of the Triple-Evil!
    _c("dm011 Arrival of the Triple-Evil! — When Revealed : trouve The Triune Understanding, la met en jeu et pose 1 compteur acceleration",
       "modele bs001b (`Search.PlayerCard` + `PutIntoPlay(under_control=True)`) + rr002 (`PlaceCountersOn`)",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('dm009')", HEROS], ["Puzzle.Reveal('dm011')"],
       {'en_jeu': ['dm009'], 'compteurs': [['dm009', 'acceleration', 1]]}),
    _c("dm011 Arrival of the Triple-Evil! — Response : apres l'Action alter-ego de The Triune Understanding, pose 1 compteur apostasy ; au 3e, elle est defaussee et l'obligation retiree du jeu",
       "modele rc011 (`AfterPlayerResolveAbility(.., which_abilities='AlterEgoAction')`) + dm012 (seuil 3)",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('dm009')", "Puzzle.Reveal('dm011')",
        "Puzzle.PlaceCounters('dm009', 'apostasy', 2)"],
       ["Puzzle.Action('dm009')"],
       {'hors_jeu': ['dm009', 'dm011']}),
    # NOTE : pas de cas distinct pour "The Triune Understanding gagne Permanent" -- `Puzzle.Discard`
    # (regle de debogage) ne porte pas de `paper.set_name` comparable de facon fiable dans ce harnais
    # (`OnWhenCardLeavePlay` compare des sets), et le mecanisme lui-meme (`GiveKeywordToInPlayWhenApplyThis`)
    # est deja un patron prouve ailleurs (modele sd018). A verifier en partie reelle si besoin.

    # ============================================================ dm012 Secret Initiative
    _c("dm012 Secret Initiative — Response : quand des cartes du deck de rencontre sont regardees (Tri-Force Vision), chaque sbire trouve entre en jeu engage avec le joueur ; 1 compteur skrull par sbire",
       "primitive `AfterPlayerLookedAtEncounterDeck` (ajoutee 04/11/2026 pour cette carte) + ar014 (`PutIntoPlay` + `EngagePlayer`)",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', '01107', '01107')", HEROS,
        M('dm012')],
       [],
       {'en_jeu': ['01101'], 'compteurs': [['dm012', 'skrull', 1]]}, main_exclusive=['dm002', 'dm022'], jouer=['dm002'], accepter_choix=True),
    _c("dm012 Secret Initiative — TEMOIN D'EPUISEMENT : avec 2 compteurs skrull deja poses, un 3e (meme mecanisme) fait defausser la carte",
       "« When there are 3+ counters here, discard this scheme » (`AfterCounterPlacedOn(.., at_least=3)`)",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', '01107', '01107')", HEROS,
        M('dm012'), "Puzzle.PlaceCounters('dm012', 'skrull', 2)"],
       [],
       {'hors_jeu': ['dm012']}, main_exclusive=['dm002', 'dm022'], jouer=['dm002'], accepter_choix=True),

    # ============================================================ dm013 Magnitude
    _c("dm013 Magnitude — When Defeated : remelange chaque AUTRE carte SKRULL de la defausse de rencontre dans le deck (Skrull Invaders)",
       "modele sl036 (`CardFinder2('SKRULL', CardFace)` + `ShuffleAllTo`) ; `other` l'exclut elle-meme (deja defaussee par sa propre defaite)",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.EmptyEncounterDiscardPile()", "Puzzle.CreateEncounterDiscardPile('dm014')", M('dm013')],
       ["Puzzle.Damage('dm013', 1)", "Puzzle.Damage('dm013', 4)"],
       {'dans_deck_rencontre': ['dm014']}, accepter_choix=True),
    _c("dm013 Magnitude — TEMOIN : aucune autre carte SKRULL en defausse : rien ne remonte dans le deck",
       "« each OTHER SKRULL card » : sans copie disponible, rien a remelanger",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.EmptyEncounterDiscardPile()", M('dm013')],
       ["Puzzle.Damage('dm013', 4)"],
       {'dans_deck_rencontre': []}, accepter_choix=True),

    # ============================================================ dm014 Skrull Invaders
    _c("dm014 Skrull Invaders — [star] Boost : trouve Skrull Infiltrator (en defausse de rencontre) et le revele",
       "modele ca021 (`Search.EncounterCard(.., include_discard_pile=True, name=..)` + `Reveal`)",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.EmptyEncounterDiscardPile()", "Puzzle.CreateEncounterDiscardPile('dm015')",
        "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('dm022', 'dm023', 'dm016')", M('dm014')],
       ["Puzzle.Boost('dm014')"],
       {'defausse_rencontre': []}, accepter_choix=True),

    # ============================================================ dm015 Skrull Infiltrator
    _c("dm015 Skrull Infiltrator — When Revealed : revele le deck du premier joueur jusqu'a un allie (She-Hulk) et s'y attache ; l'allie gagne +2 PV",
       "`Deck.DiscardUntil(card_type=Ally)` (generalisation de `Worlds.DiscardEncounterCardsUntil`) + bl017 (`GainHealthAndMaxHealth`)",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('dm022', 'dm023', 'dm016')"], ["Puzzle.Reveal('dm015')"],
       {'attaches': [['dm016', 'dm015']], 'pv_max': [['dm016', 5]]}, accepter_choix=True),

    # ============================================================ dm016 She-Hulk
    _c("dm016 She-Hulk — Response : apres avoir joue un evenement a 3 couts (dm003), 1 degat sur le vilain",
       "play.py (`AfterPlayerPlayedCard(.., CardFinder(card_type=Event))`) + condition `printed_cost==3`",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", "Puzzle.AddTraitToPaper('dm001a', 'AVENGER')", HEROS, M('dm016')],
       [],
       {'degats': [[VILAIN, 4]]}, main_exclusive=['dm003', 'dm024', 'dm023'], jouer=['dm003'], cibles=[VILAIN], accepter_choix=True),
    _c("dm016 She-Hulk — TEMOIN : un evenement a 1 cout (dm002, Tri-Force Vision) ne declenche rien",
       "« a 3-COST event » : filtre sur le cout imprime, pas seulement le type",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", "Puzzle.AddTraitToPaper('dm001a', 'AVENGER')", HEROS, M('dm016')],
       [],
       {'degats': [[VILAIN, 0]]}, main_exclusive=['dm002', 'dm022'], jouer=['dm002'], accepter_choix=True),

    # ============================================================ dm017 Number Cruncher
    _c("dm017 Number Cruncher — Interrupt : en defaussant dm003 (evenement a 3 couts) pour payer dm006 (evenement [wild]), s'incline et triple ses ressources",
       "modele yd007 (`AfterGenerateResources` + reversement de `message.res` deux fois supplementaires = 3x au total) ; main = dm006 + dm003(1) + dm023(2) = 3 pile, pour que le pre-controle d'affordabilite (qui ne connait pas la triplication a l'avance) n'echoue pas tout seul",
       ["Puzzle.EmptyHand()", HEROS, M('dm017')], [],
       {'absent_main': ['dm006'], 'exhausted': ['dm017']}, main_exclusive=['dm006', 'dm003', 'dm023'], jouer=['dm006']),

    # ============================================================ dm018 Getting it Done
    _c("dm018 Getting it Done — Hero Interrupt : +3 ATK sur l'attaque de base (1 -> 4), partagee en 1+3 entre Hydra Mercenary et le vilain",
       "modele ah011 (`GainATKForThisAttack`) + 16155 (`SetTarget(Enemy, range=(1,4), repeat_rules='Health')`) ; ARBITRAGE UTILISATEUR : partage REEL, `SetBeInstead` annule l'attaque normale",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", HEROS, "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('dm001a')"],
       {'degats': [['01101', 1], [VILAIN, 3]]}, main_exclusive=['dm018', 'dm024', 'dm023'], accepter_choix=True, preferer_option='Split this damage between enemies',
       cibles=['01101', VILAIN, VILAIN, VILAIN]),
    _c("dm018 Getting it Done — cout REDUIT (Action dm001a avant) : 3-D Man (epuise avant l'attaque) est redresse",
       "« If you reduced this card's cost, ready your hero » : `CoutReduit` (helper du pack)",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", HEROS, "Puzzle.Action('dm001a')"], ["Puzzle.Attack('dm001a')"],
       {'pret': ['dm001a']}, main_exclusive=['dm018', 'dm024'], accepter_choix=True, preferer_option="Don't split this damage"),

    # ============================================================ dm019 Brick Session
    _c("dm019 Brick Session — Hero Interrupt : +3 THW sur le contre de base (1 -> 4), partage en 1+3 entre deux complots",
       "miroir THW de dm018 ; `RemoveThreatFromSchemes(.., repeat_rules='Threat')`",
       ["Puzzle.EmptyHand()", f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 5)", HEROS], ["Puzzle.Thwart('dm001a')"],
       {'menace': [[COMPLOT, 4], ['01107', 2]]}, main_exclusive=['dm019', 'dm022', 'dm023'], accepter_choix=True, preferer_option='Split this threat removal between schemes',
       cibles=['01107', '01107', '01107', COMPLOT]),

    # ============================================================ dm020 Prevent Disaster
    # TROUVE (03/11/2026) : ni `Puzzle.EnemyAttacks` ni `Puzzle.Boost` ne font traverser l'icone de boost
    # jusqu'au calcul de l'attaque (voir `tools/cas/destiny.py` pour le modele qui marche). `Puzzle.Attack`
    # (brique dy001a/sw001a/08006), lui, rejoue la VRAIE chaine `WhenEnemyWouldActivate -> DoAttackYou ->
    # ResolveBoostCards`, qui envoie `WhenBoostCardTurnedFaceUp` avec les icones reellement comptees sur la
    # carte retournee. `01156` Usurp The Throne (SideScheme, Boost 3, texte vide -> aucun effet "When
    # Revealed" ni "Boost" [star] ne vient brouiller le resultat) sert de carte de boost a 3 icones.
    _c("dm020 Prevent Disaster — Hero Interrupt (defense) : boost a 3 icones retourne sur l'attaque de Rhino -> l'activation est annulee, aucun degat, +1 carte",
       "`WhenBoostCardTurnedFaceUp(HeroInterrupt, None, while_attack=True, activate_target='You', boost_icons>=3)` ; `PreventDamage('All')` sur `would_message` + `CancelBoostAbility` + `DrawUp(1)` ; "
       "`passer_sur_option='Strength'` -- SANS lui, l'Interruption 'Strength & Spirit of Three Men' de dm001a (declenchee par le pouvoir de base DEF, AVANT que le boost ne se retourne) defausse dm020 LUI-MEME pour payer son propre cout, avant que la fenetre de dm020 n'existe meme (lecon dm005, ou `ne_pas_depenser` seul ne protege PAS ce choix de defausse) ; "
       "main = 4 (dm020, dm022, dm023, dm024) ; le pilote paie le cout en ressources de dm020 depuis la main (observe : dm022+dm023) puis joue dm020 (- 3), `DrawUp(1)` en rajoute une (main finale observee = 3)",
       ["Puzzle.EmptyHand()"] + DECK('01156') + [HEROS], [f"Puzzle.Attack('{VILAIN}', defender='dm001a')"],
       {'degats_identite': 0, 'taille_main': 3, 'defausse_rencontre': ['01156']},
       main_exclusive=['dm020', 'dm022', 'dm023', 'dm024'], jouer=['dm020'], accepter_choix=True, passer_sur_option='Strength'),
    _c("dm020 Prevent Disaster — TEMOIN : boost a 2 icones (Shocker 01103, insuffisant) : aucune Interruption offerte, degat net = 1 (ATK 2+2 - DEF boostee a 3 par Strength & Spirit)",
       "seuil `boost_icons >= 3` non atteint ; `01103` Shocker sert de boost (2 icones) ; main = 4 - 1 (cout DEF) = 3",
       ["Puzzle.EmptyHand()"] + DECK('01103') + [HEROS], [f"Puzzle.Attack('{VILAIN}', defender='dm001a')"],
       {'degats_identite': 1, 'taille_main': 3},
       main_exclusive=['dm020', 'dm022', 'dm023', 'dm024'], accepter_choix=True),



    # ============================================================ dm021 Team Coordination
    _c("dm021 Team Coordination — Hero Action : redresse un allie incline (dm016) ; cout PLEIN -> aucun bonus",
       "modele bk012 (`GainUntilRoundEnd`) ; ARBITRAGE UTILISATEUR : le redressement est inconditionnel, le bonus +1/+1 non",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", "Puzzle.AddTraitToPaper('dm001a', 'AVENGER')", HEROS, M('dm016'), "Puzzle.Exhaust('dm016')"], [],
       {'pret': ['dm016'], 'attributs_carte': [['dm016', 'attack', 0]]}, main_exclusive=['dm021', 'dm023', 'dm024'], jouer=['dm021'], cibles=['dm016'], accepter_choix=True),
    _c("dm021 Team Coordination — cout REDUIT (Action dm001a avant) : l'allie redresse gagne +1 ATK et +1 THW jusqu'a la fin du round",
       "« those allies get +1 ATK and +1 THW for that action »",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyEncounterDeck()", "Puzzle.AddTraitToPaper('dm001a', 'AVENGER')", HEROS, "Puzzle.Action('dm001a')", M('dm016'), "Puzzle.Exhaust('dm016')"], [],
       {'attributs_carte': [['dm016', 'attack', 1], ['dm016', 'thwart', 1]]}, main_exclusive=['dm021', 'dm023'], jouer=['dm021'], cibles=['dm016'], accepter_choix=True),
]
