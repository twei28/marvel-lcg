# Cas test_capacites du heros DESTINY (Destiny / Irene Adler, Merlin, prefixe `dy`) : noms commencant par le card_id
# (substituer_pack.py filtre dessus : `tools/substituer_pack.py <game_dir> <port> dy0`).
#
# Rappels de montage :
#  - le deck `destiny` demarre en ALTER EGO (dy001b) ; `Puzzle.ChangeToFace('dy001b', 'dy001a')` le passe en HEROS ;
#  - Glimpse of the Future (dy002) est Permanent + Setup : EN JEU des la mise en place ; `Action('dy002')` regarde les 3 cartes du dessus du deck Rencontre ;
#  - Rhino 01094 est le vilain (14 PV), 01097b son complot principal ; 01101 Hydra Mercenary (3 PV, Garde 1) ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ;
#  - icones de boost : 01105 = 0 icone, 01103 Shocker = 2 icones, 01099 Charge = 2 (voir `desc.Boost`).
HEROS = "Puzzle.ChangeToFace('dy001b', 'dy001a')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
ATTAQUE_DE_RHINO = ["Puzzle.Attack('01094')"]


def M(carte):
    return f"Puzzle.PutIntoPlay('{carte}', under_control=True)"


def SOUS(carte):
    """Glisse CARTE sous Glimpse of the Future (dy002), comme apres Precognition."""
    return f"Puzzle.PlaceUnder('{carte}', 'dy002')"


def DECK(*cartes):
    """Deck Rencontre dont la PREMIERE carte citee est le DESSUS (`CreateEncounterDeck` empile : la derniere creee est au-dessus)."""
    return ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(" + ", ".join(f"'{c}'" for c in reversed(cartes)) + ")"]



def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {'nom': nom, 'pourquoi': pourquoi, 'scenario': cle.pop('scenario', 'rhino'), 'heros': cle.pop('heros', 'destiny'),
           'mise_en_place': list(mise), 'declencher': list(declencher), 'verifier': cle.pop('verifier', 'etat_attendu'), 'attendu': attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ dy002 Glimpse of the Future
    _c("dy002 Setup — Glimpse of the Future est en jeu des la mise en place (Permanent + Setup)",
       "mot-cle Setup natif (`desc.Setup`) : la carte entre en jeu sans etre jouee",
       [], ["Puzzle.Draw(0)"],
       {'en_jeu': ['dy002']}),
    _c("dy002 Glimpse of the Future — Precognition : une des 3 cartes du dessus est glissee sous la carte, les deux autres restent dans le deck Rencontre, Glimpse est inclinee",
       "modeles 40004 (`LookAtDeck`) + sn014 (`TuckCardUnderHere`) + `Faces.ShuffleAllTo(.., \"EncounterDeck\")`",
       DECK('dy014', '01101', '01102', '01107', '01108'), ["Puzzle.Action('dy002')"],
       {'pose_sous': [['dy002', 'dy014']], 'taille_pose_sous': [['dy002', 1]], 'dans_deck_rencontre': ['01101', '01102', '01107', '01108'], 'exhausted': ['dy002']},
       cibles=['dy014'], accepter_choix=True, main_exclusive=['01090']),
    _c("dy002 Glimpse of the Future — « top 3 » : la 4e carte du deck n'est pas regardee, elle reste dans le deck (la carte glissee est l'une des 3 premieres)",
       "la 4e et la 5e carte ne peuvent pas etre choisies",
       DECK('01101', '01102', 'dy014', '01107', '01108'), ["Puzzle.Action('dy002')"],
       {'pose_sous': [['dy002', 'dy014']], 'dans_deck_rencontre': ['01101', '01102', '01107', '01108']},
       cibles=['dy014'], accepter_choix=True, main_exclusive=['01090']),
    _c("dy002 Glimpse of the Future — la carte glissee est defaussee (defausse RENCONTRE) a la fin du round",
       "FR 1.2 : « Defaussez-la a la fin du round » ; `WhenRoundEnd(ForcedInterrupt)`",
       DECK('dy014', '01101', '01102', '01107', '01108'), ["Puzzle.Action('dy002')", "Puzzle.SendRoundEnd()"],
       {'taille_pose_sous': [['dy002', 0]], 'defausse_rencontre': ['dy014']},
       cibles=['dy014'], accepter_choix=True, main_exclusive=['01090']),
    _c("dy002 Glimpse of the Future — TEMOIN : tant que le round n'est pas fini, la carte reste glissee",
       "meme position sans fin de round",
       DECK('dy014', '01101', '01102', '01107', '01108'), ["Puzzle.Action('dy002')"],
       {'taille_pose_sous': [['dy002', 1]]},
       cibles=['dy014'], accepter_choix=True, main_exclusive=['01090']),
    # ============================================================ dy001a Destiny : X et Interruption
    _c("dy001a X — Mister Sinister (2 icones de boost) sous Glimpse : ATQ, CTR et DEF valent 2",
       "modele mw001a (`ThisGainKeyword(fn, attack=1, thwart=1, defense=1, change_on_event=..)`, `desc` a 0)",
       [HEROS, SOUS('dy014')], ["Puzzle.Draw(0)"],
       {'attributs_carte': [['dy001a', 'attack', 2], ['dy001a', 'thwart', 2], ['dy001a', 'defense', 2]]}),
    _c("dy001a X — Destiny's Warning (UNE etoile Boost, 0 icone) sous Glimpse : X vaut 1 (l'etoile compte)",
       "`CountTotalBoostStarAndBoost` et non `CountTotalBoostIcons` (lecon sn014)",
       [HEROS, SOUS('dy015')], ["Puzzle.Draw(0)"],
       {'attributs_carte': [['dy001a', 'attack', 1], ['dy001a', 'thwart', 1], ['dy001a', 'defense', 1]]}),
    _c("dy001a X — TEMOIN : rien sous Glimpse, ATQ, CTR et DEF valent 0",
       "X = 0 sans carte glissee",
       [HEROS], ["Puzzle.Draw(0)"],
       {'attributs_carte': [['dy001a', 'attack', 0], ['dy001a', 'thwart', 0], ['dy001a', 'defense', 0]]}),
    _c("dy001a Interruption — on defausse la carte RETOURNEE : ses icones sont annulees, la nouvelle (2 icones) joue : Rhino frappe pour 2 + 2 = 4",
       "modeles sw001a / 08006 (`WhenBoostCardTurnedFaceUp`) + `GiveBoostCardForThisActivation` ; Hydra Mercenary (1 icone) puis Shocker (2 icones)",
       [HEROS] + DECK('01101', '01103', '01105'), ATTAQUE_DE_RHINO,
       {'degats_identite': 4, 'defausse_rencontre': ['01101', '01103']},
       accepter_choix=True, main_exclusive=['01090'], preferer_option='Discard the boost card that was turned faceup'),
    _c("dy001a Interruption — on defausse la NOUVELLE carte (encore face cachee) : la carte retournee joue seule : Rhino frappe pour 2 + 1 = 3",
       "la seconde moitie du choix « discard one of them »",
       [HEROS] + DECK('01101', '01103', '01105'), ATTAQUE_DE_RHINO,
       {'degats_identite': 3, 'defausse_rencontre': ['01101', '01103']},
       accepter_choix=True, main_exclusive=['01090'], preferer_option='Discard the other boost card (still facedown)'),
    _c("dy001a Interruption — TEMOIN : en ALTER-EGO la capacite de la face heros n'existe pas : une seule carte de boost, Rhino frappe pour 2 + 1 = 3 et le deck garde Shocker",
       "la capacite est portee par la face heros",
       DECK('01101', '01103', '01105'), ATTAQUE_DE_RHINO,
       {'degats_identite': 3, 'dans_deck_rencontre': ['01103']},
       accepter_choix=True, main_exclusive=['01090']),
    _c("dy001a Interruption — LIMITE une fois par phase : au 2e Rhino de la phase, rien n'est offert (carte de boost 2 icones : 2 + 2 ; total 4 + 4 = 8, et non 7)",
       "TEMOIN D'EPUISEMENT : sans limite le 2e boost donnerait une carte de plus (Hydra, 1 icone) et defausserait la retournee : 4 + 3 = 7",
       [HEROS] + DECK('01101', '01103', '01102', '01101', '01105'), ATTAQUE_DE_RHINO + ATTAQUE_DE_RHINO,
       {'degats_identite': 8},
       accepter_choix=True, main_exclusive=['01090'], preferer_option='Discard the boost card that was turned faceup'),
    # ============================================================ dy001b Irene Adler
    _c("dy001b Setup — une amelioration PSIONIC du deck est ajoutee a la main de depart",
       "modele 01040b (`WhenCardSetup` + `Search.PlayerCard`)",
       [], ["Puzzle.Draw(0)"],
       {'taille_main': 7}),
    _c("dy001b Response — apres le retour en alter-ego, une carte PSIONIC de la defausse est melangee dans le deck",
       "modele 27030b (`AfterUnitChangeForm(.., to_this_form=True)`)",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDiscardPile('dy004')"], ["Puzzle.ChangeToFace('dy001a', 'dy001b')"],
       {'dans_deck_joueur': ['dy004']}, cibles=['dy004'], accepter_choix=True),
    _c("dy001b Response — TEMOIN : une carte NON PSIONIC de la defausse (Energy) n'est pas offerte, elle y reste",
       "« a PSIONIC card »",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDiscardPile('01088')"], ["Puzzle.ChangeToFace('dy001a', 'dy001b')"],
       {'taille_deck_joueur': 0}, accepter_choix=True),
    # ============================================================ dy003 Mystique
    _c("dy003 Mystique — Action : une ressource depensee, l'identite gagne 1 PV et est REDRESSEE, Mystique inclinee",
       "FR 1.2 : « redressez votre identite » ; modele 48001a (cout `Cost(\"1\")` + `LimitOncePerPhase`)",
       [M('dy003'), "Puzzle.Damage('dy001b', 3)", "Puzzle.Exhaust('dy001b')"], ["Puzzle.Action('dy003')"],
       {'degats_identite': 2, 'pret': ['dy001b'], 'exhausted': ['dy003']}, main_exclusive=['01090'], accepter_choix=True),
    _c("dy003 Mystique — LIMITE une fois par phase : Mystique redressee, la 2e Action est refusee (1 seul soin : 3 - 1 = 2 degats, et non 1)",
       "TEMOIN D'EPUISEMENT, chiffre mesure au second emploi",
       [M('dy003'), "Puzzle.Damage('dy001b', 3)", "Puzzle.Exhaust('dy001b')"], ["Puzzle.Action('dy003')", "Puzzle.Ready('dy003')"],
       {'degats_identite': 2}, main_exclusive=['01090', '01090'], accepter_choix=True, declencher_tolerant=["Puzzle.Action('dy003')"]),
    # ============================================================ dy004 Mental Awareness
    _c("dy004 Mental Awareness — genere [wild] pour une carte PSIONIC : elle paie Unmask (cout 1, PSIONIC), Mental Awareness s'incline",
       "modeles 08007 / 46004 (`CanGenerateResources(.., for_card=CardFinder2(\"TRAIT\"))`)",
       [HEROS, M('dy004')], [],
       {'en_jeu': ['dy006'], 'exhausted': ['dy004']}, main_exclusive=['dy006'], jouer=['dy006'], payer_avec=['dy004'], accepter_choix=True),
    _c("dy004 Mental Awareness — TEMOIN : elle NE paie PAS une carte non PSIONIC (Unconditional Love reste en main, Mental Awareness reste prete)",
       "« for a PSIONIC card »",
       [HEROS, M('dy004')], [],
       {'en_main': ['dy011'], 'pret': ['dy004']}, main_exclusive=['dy011'], jouer=['dy011'], payer_avec=['dy004'], accepter_choix=True),
    # ============================================================ dy005 Clairvoyance
    _c("dy005 Clairvoyance — 2 ressources mentales, X = 2 : DEUX manigances DIFFERENTES perdent 2 menaces chacune ; Clairvoyance inclinee",
       "modele 26022 (`Cost(.., up_to=True)`) + 01060 (`RemoveThreatFromSchemes`) ; cibles distinctes",
       [HEROS, M('dy005'), SOUS('dy014'), "Puzzle.SetThreat('01097b', 5)", "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 4)"], ["Puzzle.Action('dy005', 'HeroAction')"],
       {'menace': [['01097b', 3], ['01107', 2]], 'exhausted': ['dy005']}, main_exclusive=['01089'], payer_jusqu_a=2, cibles=['01097b', '01107'], accepter_choix=True),
    _c("dy005 Clairvoyance — UNE seule ressource depensee : UNE seule manigance est visee (l'autre garde sa menace)",
       "« for each resource spent »",
       [HEROS, M('dy005'), SOUS('dy014'), "Puzzle.SetThreat('01097b', 5)", "Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 4)"], ["Puzzle.Action('dy005', 'HeroAction')"],
       {'menace': [['01097b', 3], ['01107', 4]]}, main_exclusive=['dy009'], payer_jusqu_a=1, cibles=['01097b'], accepter_choix=True),
    _c("dy005 Clairvoyance — TEMOIN : rien sous Glimpse (X = 0), aucune menace retiree",
       "X = 0",
       [HEROS, M('dy005'), "Puzzle.SetThreat('01097b', 5)"], ["Puzzle.Action('dy005', 'HeroAction')"],
       {'menace': [['01097b', 5]]}, main_exclusive=['01089'], payer_jusqu_a=2, cibles=['01097b'], accepter_choix=True),
    # ============================================================ dy006 Unmask
    _c("dy006 Unmask — 2 ressources mentales, X = 2 : DEUX ennemis DIFFERENTS (Rhino, Hydra Mercenary) recoivent 2 degats chacun ; Unmask inclinee",
       "modele 26022 + 01054 (`DealDamage`) ; cibles distinctes",
       [HEROS, M('dy006'), SOUS('dy014'), "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Action('dy006', 'HeroAction')"],
       {'degats': [['01094', 2], ['01101', 2]], 'exhausted': ['dy006']}, main_exclusive=['01089'], payer_jusqu_a=2, cibles=['01094', '01101'], accepter_choix=True),
    _c("dy006 Unmask — UNE seule ressource depensee : UN seul ennemi est vise",
       "« for each resource spent »",
       [HEROS, M('dy006'), SOUS('dy014'), "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Action('dy006', 'HeroAction')"],
       {'degats': [['01094', 2], ['01101', 0]]}, main_exclusive=['dy009'], payer_jusqu_a=1, cibles=['01094'], accepter_choix=True),
    _c("dy006 Unmask — TEMOIN : rien sous Glimpse (X = 0), aucun degat",
       "X = 0",
       [HEROS, M('dy006')], ["Puzzle.Action('dy006', 'HeroAction')"],
       {'degats': [['01094', 0]]}, main_exclusive=['01089'], payer_jusqu_a=2, cibles=['01094'], accepter_choix=True),
    # ============================================================ dy007 Be Careful
    # ⚠ Le heros DEFEND l'attaque (DEF = X) : l'ATQ 3 de Sandman est d'abord reduite de X par la defense, puis Be Careful previent X de ce qui reste.
    _c("dy007 Be Careful — X = 2 : Sandman (ATQ 3) frappe, la DEF 2 laisse 1 degat, Be Careful (X = 2) le previent : 0 degat et Be Careful s'incline",
       "modele mw004 (`WhenUnitWouldTakeDamage(HeroInterrupt, \"You\")` + `PreventDamage`)",
       [HEROS, M('dy007'), SOUS('dy014'), "Puzzle.PutIntoPlay('01102')"] + SANS_BOOST, ["Puzzle.Attack('01102')"],
       {'degats_identite': 0, 'exhausted': ['dy007']}, main_exclusive=['dy009'], payer_avec=['dy009'], accepter_choix=True),
    _c("dy007 Be Careful — X = 1 (une etoile) : DEF 1 laisse 2 degats, Be Careful en previent 1 : l'identite subit 1",
       "« prevent X OF that damage »",
       [HEROS, M('dy007'), SOUS('dy015'), "Puzzle.PutIntoPlay('01102')"] + SANS_BOOST, ["Puzzle.Attack('01102')"],
       {'degats_identite': 1, 'exhausted': ['dy007']}, main_exclusive=['dy009'], payer_avec=['dy009'], accepter_choix=True),
    _c("dy007 Be Careful — TEMOIN : rien sous Glimpse (X = 0), la capacite n'est pas offerte : 3 degats, Be Careful reste prete",
       "X = 0",
       [HEROS, M('dy007'), "Puzzle.PutIntoPlay('01102')"] + SANS_BOOST, ["Puzzle.Attack('01102')"],
       {'degats_identite': 3, 'pret': ['dy007']}, main_exclusive=['dy009'], payer_avec=['dy009'], accepter_choix=True),
    # ============================================================ dy008 Prescience
    _c("dy008 Prescience — a la revelation d'une traitrise, ses effets Une fois revelee sont annules (Rhino ne recoit pas de carte Tenace), elle est defaussee, puis Prescience aussi",
       "modele 21036 Cosmic Ward (`WhenPlayerRevealCard(ForcedInterrupt, .., Treachery, \"WhenRevealed\")`)",
       [HEROS, M('dy008')], ["Puzzle.Reveal('01105')"],
       {'statuts_absents': [['01094', 'Tough']], 'defausse_rencontre': ['01105'], 'hors_jeu': ['dy008']}, accepter_choix=True, main_exclusive=['01090']),
    _c("dy008 Prescience — TEMOIN : sans Prescience la traitrise s'applique (Rhino devient Tenace)",
       "meme revelation sans la carte",
       [HEROS], ["Puzzle.Reveal('01105')"],
       {'statuts': [['01094', 'Tough']]}, accepter_choix=True, main_exclusive=['01090']),
    # ============================================================ dy009 Astral Projection
    _c("dy009 Astral Projection — X = 2 : 3 + 2 = 5 menaces retirees du complot principal (6 -> 1)",
       "modele 01060 For Justice! (`RemoveThreatFromSchemes(effect.targets, n, effect)`)",
       [HEROS, SOUS('dy014'), "Puzzle.SetThreat('01097b', 6)"], [],
       {'menace': [['01097b', 1]]}, main_exclusive=['dy009', '01089'], jouer=['dy009'], payer_avec=['01089'], cibles=['01097b'], accepter_choix=True),
    _c("dy009 Astral Projection — TEMOIN : rien sous Glimpse : 3 menaces seulement (6 -> 3)",
       "X = 0",
       [HEROS, "Puzzle.SetThreat('01097b', 6)"], [],
       {'menace': [['01097b', 3]]}, main_exclusive=['dy009', '01089'], jouer=['dy009'], payer_avec=['01089'], cibles=['01097b'], accepter_choix=True),
    # ============================================================ dy010 Path of Violence
    _c("dy010 Path of Violence — X = 2 : 4 + 2 = 6 degats a Rhino",
       "modele 01054 Uppercut (`DealDamage(effect.targets, n, effect)`)",
       [HEROS, SOUS('dy014')], [],
       {'degats': [['01094', 6]]}, main_exclusive=['dy010', '01090'], jouer=['dy010'], payer_avec=['01090'], cibles=['01094'], accepter_choix=True),
    _c("dy010 Path of Violence — TEMOIN : rien sous Glimpse : 4 degats seulement",
       "X = 0",
       [HEROS], [],
       {'degats': [['01094', 4]]}, main_exclusive=['dy010', '01090'], jouer=['dy010'], payer_avec=['01090'], cibles=['01094'], accepter_choix=True),
    # ============================================================ dy011 Unconditional Love
    _c("dy011 Unconditional Love — Mystique en jeu : Mystique ET l'identite de Destiny sont redressees",
       "« ready Mystique/Raven Darkholme and Destiny/Irene Adler »",
       [HEROS, M('dy003'), "Puzzle.Exhaust('dy003')", "Puzzle.Exhaust('dy001a')"], [],
       {'pret': ['dy003', 'dy001a']}, main_exclusive=['dy011', '01090'], jouer=['dy011'], payer_avec=['01090'], accepter_choix=True),
    _c("dy011 Unconditional Love — Mystique absente, dans le DECK : elle est ajoutee a la main",
       "« Otherwise, search your deck ... »",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('dy003', '01088')"], [],
       {'en_main': ['dy003']}, main_exclusive=['dy011', '01090'], jouer=['dy011'], payer_avec=['01090'], accepter_choix=True),
    _c("dy011 Unconditional Love — Mystique absente, dans la DEFAUSSE : elle est ajoutee a la main",
       "« ... and discard pile »",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088')", "Puzzle.CreatePlayerDiscardPile('dy003')"], [],
       {'en_main': ['dy003']}, main_exclusive=['dy011', '01090'], jouer=['dy011'], payer_avec=['01090'], accepter_choix=True),
    # ============================================================ dy012 Fragment Studies
    # ⚠ Deck vide et defausse montes dans `declencher` (APRES `main_exclusive`) : `EmptyPlayerDeck` RETIRE DE LA PARTIE les cartes du deck, et `Puzzle.Gain` en reprend
    # alors des copies retirees ; et Astral Projection n'est jouable que s'il y a de la menace a retirer (SetThreat).
    _c("dy012 Fragment Studies — apres depense, une carte propre a l'identite (Mental Awareness) de la defausse est melangee dans le deck",
       "modele mt006 (`AfterYouSpendThisCard`) + 27030b (`card_class=\"IdentitySpecific\"`)",
       [HEROS, "Puzzle.SetThreat('01097b', 6)"], ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDiscardPile('dy004')"],
       {'dans_deck_joueur': ['dy004']}, main_exclusive=['dy009', 'dy012'], jouer=['dy009'], payer_avec=['dy012'], cibles=['01097b', 'dy004'], accepter_choix=True),
    _c("dy012 Fragment Studies — TEMOIN : une carte de BASE (Energy) de la defausse n'est pas offerte, elle y reste (deck vide)",
       "« identity-specific »",
       [HEROS, "Puzzle.SetThreat('01097b', 6)"], ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDiscardPile('01088')"],
       {'taille_deck_joueur': 0}, main_exclusive=['dy009', 'dy012'], jouer=['dy009'], payer_avec=['dy012'], cibles=['01097b'], accepter_choix=True),
    # ============================================================ dy013 Seizure
    _c("dy013 Seizure — branche 1 : en alter-ego, Irene Adler s'incline et l'obligation est retiree de la partie",
       "modele mt011 : `Exhaust(\"YourIdentity\")` + `Faces.RemoveAllFromGame`",
       [], ["Puzzle.Reveal('dy013')"],
       {'exhausted': ['dy001b'], 'hors_jeu': ['dy013']}, accepter_choix=True, main_exclusive=['01090']),
    _c("dy013 Seizure — branche 2 : une amelioration SKILL (Unmask) est defaussee, puis l'obligation est defaussee",
       "« Discard 1 SKILL upgrade you control »",
       [HEROS, M('dy006')], ["Puzzle.Reveal('dy013')"],
       {'hors_jeu': ['dy006', 'dy013']}, accepter_choix=True, preferer_option='Discard 1 SKILL upgrade you control. Discard this obligation', main_exclusive=['01090']),
    _c("dy013 Seizure — branche 2 SANS amelioration SKILL : rien n'est defausse et la carte gagne SURGE (la carte rencontre suivante, Hydra Mercenary, est distribuee)",
       "« If no upgrade was discarded this way, this card gains surge »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"], ["Puzzle.Reveal('dy013')"],
       {'carte_du_surge': '01101'}, accepter_choix=True, preferer_option='Discard 1 SKILL upgrade you control. Discard this obligation', main_exclusive=['01090']),
    # ============================================================ dy014 Mister Sinister
    _c("dy014 Mister Sinister — tant que Destiny's Warning est en jeu, il ne s'active PAS (0 degat)",
       "modeles 49007 / 60113b (`EnemyCannotActivate(NonKeyword, \"This\", conditions=[..])`)",
       [HEROS, "Puzzle.PutIntoPlay('dy015')", "Puzzle.PutIntoPlay('dy014')"] + SANS_BOOST, ["Puzzle.Activate('dy014')"],
       {'degats_identite': 0}, accepter_choix=True, main_exclusive=['01090']),
    _c("dy014 Mister Sinister — TEMOIN : sans Destiny's Warning il s'active (ATQ 3 : 3 degats)",
       "meme position sans la manigance annexe",
       [HEROS, "Puzzle.PutIntoPlay('dy014')"] + SANS_BOOST, ["Puzzle.Activate('dy014')"],
       {'degats_identite': 3}, accepter_choix=True, main_exclusive=['01090']),
    _c("dy014 Mister Sinister — Une fois revele, DEJA en jeu : la 2e copie est defaussee et le sbire en jeu s'active MEME avec Destiny's Warning (3 degats)",
       "branche decouverte au pack Mystique : le moteur defaussait la 2e copie (UNIQUE) avant son When Revealed ; `UniqueRuleNotApplyTo(name=..)` ; la 2e copie est creee SUR le deck (`FindOrCreateFace` cherche le deck avant le jeu)",
       [HEROS, "Puzzle.Exhaust('dy001a')", "Puzzle.PutIntoPlay('dy015')", "Puzzle.PutIntoPlay('dy014')"] + SANS_BOOST, ["Puzzle.CreateEncounterDeck('dy014')", "Puzzle.Reveal('dy014')"],
       {'degats_identite': 3}, accepter_choix=True, main_exclusive=['01090']),
    # ============================================================ dy015 Destiny's Warning
    _c("dy015 Destiny's Warning — a la revelation : Incite 2 pose 2 menaces PUIS Une fois revelee en retire 1 par joueur (1 + 2 - 1 = 2)",
       "`desc.Incite = 2` natif + `RemoveThreatFromSchemes(\"MainScheme\", \"1*\", effect)` (menace de depart basse : au-dela de 7 le complot serait accompli)",
       [HEROS, "Puzzle.SetThreat('01097b', 1)"], ["Puzzle.Reveal('dy015')"],
       {'menace': [['01097b', 2]], 'en_jeu': ['dy015']}, accepter_choix=True, main_exclusive=['01090']),
    _c("dy015 Destiny's Warning — ★ Boost : retournee comme carte de boost d'une manigance de Rhino, elle entre en jeu",
       "modele 02027 Goblin Nation (`WhenCardBecomeBoost(\"This\", PutThisIntoPlay)`) ; en ALTER-EGO (en forme heros, l'Interruption de dy001a peut annuler l'effet ★)",
       DECK('dy015', '01105'), ["Puzzle.Scheme('01094')"],
       {'en_jeu': ['dy015']}, accepter_choix=True, main_exclusive=['01090']),
    # ============================================================ dy016 So, What's the Plan?
    _c("dy016 So, What's the Plan? — Destiny's Warning en jeu : 1 menace par joueur retiree de la manigance annexe (4 -> 3)",
       "premiere branche",
       [HEROS, "Puzzle.PutIntoPlay('dy015')", "Puzzle.SetThreat('dy015', 4)"], ["Puzzle.Reveal('dy016')"],
       {'menace': [['dy015', 3]]}, accepter_choix=True, main_exclusive=['01090']),
    _c("dy016 So, What's the Plan? — pas de Warning, Mister Sinister en jeu : il s'active contre vous (ATQ 3 : 3 degats)",
       "seconde branche (« If you cannot, Mister Sinister activates against you »)",
       [HEROS, "Puzzle.PutIntoPlay('dy014')"] + SANS_BOOST, ["Puzzle.Reveal('dy016')"],
       {'degats_identite': 3}, accepter_choix=True, main_exclusive=['01090']),
    _c("dy016 So, What's the Plan? — ni Warning ni Sinister : la carte gagne SURGE (la carte suivante, Hydra Mercenary, est distribuee)",
       "troisieme branche",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"], ["Puzzle.Reveal('dy016')"],
       {'carte_du_surge': '01101'}, accepter_choix=True, main_exclusive=['01090']),
]
