# Cas test_capacites du heros SENTRY (Sentry / Robert Reynolds, Neptune, prefixe `rr`) : noms commencant par le card_id
# (substituer_pack.py filtre dessus : `tools/substituer_pack.py <game_dir> <port> rr0`).
#
# Rappels de montage :
#  - le deck `sentry` demarre en ALTER EGO (rr001b) ; `Puzzle.ChangeToFace('rr001b', 'rr001a')` le passe en HEROS (Sentry) ; `Puzzle.ChangeForm('rr001a')` fait l'inverse EN JEU ;
#  - Duality Aspect (rr002) est PERMANENTE : elle est en jeu des la mise en place, sans compteur ; `Puzzle.PlaceCounters('rr002', 'balance', N)` pose N compteurs (avec messages) ;
#  - Rhino 01094 est le vilain (14 PV), 01097b son complot principal ; 01101 Hydra Mercenary (3 PV, Garde 1) ;
#  - `Puzzle.EmptyHand()` AVANT toute mesure (sinon le pilote joue la main de depart) ; `Puzzle.EndPlayerTurn()` = fin de tour du joueur (WhenPlayerTurnEnd puis AfterPlayerTurnEnd).
import os as _os, re as _re
# ⚠ LIMITE DE COMPTEURS DE THE WATCHTOWER : lue dans `src/cards/pack/sentry/sentry/rr005.py` (`WATCHTOWER_MAX_COMPTEURS`), UNE SEULE ligne a changer
# si l'auteur repond « 2 » (question en attente : la carte dit 1, l'insert et la page A4 disent 2).
try:
    WATCHTOWER_MAX = int(_re.search(r"^WATCHTOWER_MAX_COMPTEURS = (\d+)", open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src", "cards", "pack", "sentry", "sentry", "rr005.py"), encoding="utf-8").read(), _re.M).group(1))
except (AttributeError, OSError):
    WATCHTOWER_MAX = 1   # module remplace par un stub (substituer_pack.py) : la constante est absente
HEROS = "Puzzle.ChangeToFace('rr001b', 'rr001a')"
DUALITE = 'rr002'
# ⚠ Le harnais ne rejoue pas « Permanent » a la mise en place : Duality Aspect se met en jeu a la main (un vrai deck la pose seule : cf. verifier_tous_les_decks).
PD = "Puzzle.PutIntoPlay('rr002', under_control=True)"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {'nom': nom, 'pourquoi': pourquoi, 'scenario': cle.pop('scenario', 'rhino'), 'heros': cle.pop('heros', 'sentry'),
           'mise_en_place': list(mise), 'declencher': list(declencher), 'verifier': cle.pop('verifier', 'etat_attendu'), 'attendu': attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ rr001a Balance (fin de tour)
    _c("rr001a Balance — fin de tour en forme HEROS : 1 balance counter sur Duality Aspect",
       "modele `so011` (`AfterPlayerTurnEnd`) ; compteur maison `balance`",
       ["Puzzle.EmptyHand()", HEROS, PD], ["Puzzle.EndPlayerTurn()"],
       {'compteurs': [[DUALITE, 'balance', 1]]}),
    _c("rr001a Balance — TEMOIN : en forme ALTER-EGO la capacite de la face heros n'existe pas (0 compteur)",
       "la capacite est sur la face heros",
       ["Puzzle.EmptyHand()", PD], ["Puzzle.EndPlayerTurn()"],
       {'compteurs': [[DUALITE, 'balance', 0]]}),
    # ============================================================ rr001b Duality (retrait en passant en alter-ego)
    _c("rr001b Duality — en passant en alter-ego avec 3 compteurs : on en retire 2 (reste 1)",
       "modele `wn001a` / `ch001b` (`AfterFlipToThisFace`) ; « up to 2 »",
       ["Puzzle.EmptyHand()", HEROS, PD, f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 3)"], ["Puzzle.ChangeForm('rr001a')"],
       {'compteurs': [[DUALITE, 'balance', 1]]}, accepter_choix=True),
    _c("rr001b Duality — TEMOIN : un seul compteur, on retire ce qu'il y a (« up to 2 » : 0 reste)",
       "« up to 2 » : retirer moins que 2 est permis",
       ["Puzzle.EmptyHand()", HEROS, PD, f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 1)"], ["Puzzle.ChangeForm('rr001a')"],
       {'compteurs': [[DUALITE, 'balance', 0]]}, accepter_choix=True),
    # ============================================================ rr002 Duality Aspect (3+ compteurs : Void)
    _c("rr002 Duality Aspect — le 3e compteur fait reveler Void (il entre en jeu)",
       "modele `ca016` (`Search.EncounterCard` + `Reveal`) ; `AfterCounterPlacedOn(.., at_least=3)`",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('rr016')", f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 2)"],
       [f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 1)"],
       {'en_jeu': ['rr016']}, accepter_choix=True),
    _c("rr002 Duality Aspect — TEMOIN : 2 compteurs seulement, Void ne vient pas",
       "seuil « 3+ »",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('rr016')"],
       [f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 2)"],
       {'hors_jeu': ['rr016']}, accepter_choix=True),
]

CAS += [
    # ============================================================ rr003 C.L.O.C.
    _c("rr003 C.L.O.C. — en entrant en jeu, retire 1 balance counter (2 -> 1)",
       "modele `counter.py::ThisEnterPlayWithCounters` (`AfterCardEnterPlay`)",
       ["Puzzle.EmptyHand()", HEROS, PD, f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 2)"], ["Puzzle.PutIntoPlay('rr003', under_control=True)"],
       {'compteurs': [[DUALITE, 'balance', 1]]}, accepter_choix=True),
    _c("rr003 C.L.O.C. — TEMOIN : sans compteur en jeu, rien a retirer (0 reste)",
       "la Reponse est sans effet",
       ["Puzzle.EmptyHand()", HEROS, PD], ["Puzzle.PutIntoPlay('rr003', under_control=True)"],
       {'compteurs': [[DUALITE, 'balance', 0]]}, accepter_choix=True),
    # ============================================================ rr004 Cornelius Worth
    _c("rr004 Cornelius Worth — Action : epuise la carte et retire 1 compteur de Duality Aspect (2 -> 1)",
       "modele `ca003` (Action + `CostFunc.Exhaust`)",
       ["Puzzle.EmptyHand()", PD, "Puzzle.PutIntoPlay('rr004', under_control=True)", f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 2)"], ["Puzzle.Action('rr004')"],
       {'compteurs': [[DUALITE, 'balance', 1]]}, accepter_choix=True),
    # ============================================================ rr005 The Watchtower
    _c("rr005 The Watchtower — la balance de fin de tour est DETOURNEE ici : 1 compteur sur la tour, 0 sur Duality Aspect",
       "`WhenCardWouldBePlacedCounter` + `SetBeInstead` ; « to a maximum of 1 »",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr005', under_control=True)"], ["Puzzle.EndPlayerTurn()"],
       {'compteurs': [[DUALITE, 'balance', 0], ['rr005', 'balance', 1]]}, accepter_choix=True),
    _c("rr005 The Watchtower — TEMOIN D'EPUISEMENT (plafond = WATCHTOWER_MAX_COMPTEURS) : la tour est PLEINE, le compteur suivant va sur Duality Aspect",
       "« to a maximum of 1 » : decision utilisateur du 03/11 (la carte prime sur l'insert)",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr005', under_control=True)", f"Puzzle.PlaceCounters('rr005', 'balance', {WATCHTOWER_MAX})"], ["Puzzle.EndPlayerTurn()"],
       {'compteurs': [[DUALITE, 'balance', 1], ['rr005', 'balance', WATCHTOWER_MAX]]}, accepter_choix=True),
    _c("rr005 The Watchtower — TEMOIN : tour epuisee, le compteur va sur Duality Aspect",
       "l'Interruption exige d'epuiser la carte",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr005', under_control=True)", "Puzzle.Exhaust('rr005')"], ["Puzzle.EndPlayerTurn()"],
       {'compteurs': [[DUALITE, 'balance', 1], ['rr005', 'balance', 0]]}, accepter_choix=True),
]

CAS += [
    # ============================================================ rr015 Fractured Psyche
    _c("rr015 Fractured Psyche — branche 1 : en alter-ego, Robert Reynolds s'incline et l'obligation est RETIREE de la partie",
       "modele `ca014` / `my015` ; `joueur.IsAlterEgo()` + `Exhaust(\"YourIdentity\")`",
       ["Puzzle.EmptyHand()", PD], ["Puzzle.Reveal('rr015')"],
       {'exhausted': ['rr001b'], 'hors_jeu': ['rr015']}, accepter_choix=True, main_exclusive=['01090']),
    _c("rr015 Fractured Psyche — branche 2 : 3 balance counters sur Duality Aspect, l'obligation est defaussee (pas retiree), Reynolds reste pret",
       "« Place 3 balance counters on Duality Aspect. Discard this obligation » ; le pilote prend la branche demandee (`preferer_option`)",
       ["Puzzle.EmptyHand()", PD], ["Puzzle.Reveal('rr015')"],
       {'compteurs': [[DUALITE, 'balance', 3]], 'pret': ['rr001b']},
       preferer_option='Place 3 balance counters on Duality Aspect. Discard this obligation', main_exclusive=['01090']),
]

CAS += [
    # ============================================================ rr006 Endless Power (Special) + rr002 (remelange) + rr016 Void (active le Special)
    _c("rr006 Endless Power — Special resolu : le Void etourdit et embrouille l'AUTRE ennemi (Hydra Mercenary) ; la carte SPLIT est remelangee dans le deck par Duality Aspect",
       "`WhenResolveSpecialAbility` (RECETTES §27) ; `RemelangerOuGlisser` (rr002, 2e capacite)",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr016')", "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('rr006', under_control=True)"],
       ["Puzzle.ResolveSpecial('rr006')"],
       {'statuts': [['01101', 'Stunned'], ['01101', 'Confused']]}, accepter_choix=True),
    _c("rr006 Endless Power — TEMOIN : sans Void en jeu le Special n'a aucun effet (l'autre ennemi n'est ni etourdi ni embrouille)",
       "« The Void stuns ... » : sans Void, rien",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('rr006', under_control=True)"],
       ["Puzzle.ResolveSpecial('rr006')"],
       {'statuts_absents': [['01101', 'Stunned'], ['01101', 'Confused']]}, accepter_choix=True),
]

CAS += [
    # ============================================================ rr019 Equilibrium Intent + rr016 Void (activation remplacee par le Special)
    _c("rr019 Equilibrium Intent — Void en jeu, 3+ compteurs : il s'active, son Forced Interrupt resout le Special de la carte SPLIT du dessus de la defausse (Endless Power etourdit l'autre ennemi)",
       "`DoActivate` (ca016) ; rr016 `WhenEnemyWouldActivate` + `SetBeInstead` + `ResolveSpecialAbility`",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr016')", "Puzzle.PutIntoPlay('01101')", f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 3)",
        "Puzzle.CreatePlayerDiscardPile('rr006')"], ["Puzzle.Reveal('rr019')"],
       {'statuts': [['01101', 'Stunned']]}, accepter_choix=True),
    _c("rr019 Equilibrium Intent — TEMOIN : seulement 2 compteurs, le Void s'active normalement (le Special de la defausse n'est PAS resolu)",
       "seuil « 3+ balance counters in play »",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr016')", "Puzzle.PutIntoPlay('01101')", f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 2)",
        "Puzzle.CreatePlayerDiscardPile('rr006')"], ["Puzzle.Reveal('rr019')"],
       {'statuts_absents': [['01101', 'Stunned']]}, accepter_choix=True),
    _c("rr019 Equilibrium Intent — Void ABSENT : 1 compteur sur Duality Aspect puis surge (la carte suivante du deck est distribuee)",
       "« If the Void is not in play, place 1 balance counter ..., then this card gains surge »",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"], ["Puzzle.Reveal('rr019')"],
       {'compteurs': [[DUALITE, 'balance', 1]], 'carte_du_surge': '01101'}, accepter_choix=True),
    _c("rr016 Void — plancher de degats : avec 4 compteurs, la 2e attaque de Sentry (2 degats ; la 1re est absorbee par Toughness) inflige AU MOINS 4 : le Void (4 PV pour 1 joueur) est VAINCU",
       "DECISION UTILISATEUR 03/11 : chaque attaque lui inflige au moins X ; `WhenUnitWouldTakeDamage` + `IncreaseDamage`",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr016')", f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 4)"], ["Puzzle.Attack('rr001a')", "Puzzle.Ready('rr001a')", "Puzzle.Attack('rr001a')"],
       {'hors_jeu': ['rr016']}, cibles=['rr016'], accepter_choix=True),
    _c("rr016 Void — TEMOIN : sans compteur (X = 0) la 2e attaque de Sentry (la 1re est absorbee par Toughness) inflige 2, pas davantage",
       "X = 0 : aucun plancher",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr016')"], ["Puzzle.Attack('rr001a')", "Puzzle.Ready('rr001a')", "Puzzle.Attack('rr001a')"],
       {'degats': [['rr016', 2]]}, cibles=['rr016'], accepter_choix=True),
]

CAS += [
    # ============================================================ rr014 Unrivaled Might
    _c("rr014 Unrivaled Might — sans compteur : 8 degats au vilain (Rhino)",
       "modele `ca012` (`DealDamage` + label attack) ; cout 3 [physical] paye avec Energy + Strength",
       ["Puzzle.EmptyHand()", HEROS, PD], [],
       {'degats': [['01094', 8]]}, main_exclusive=['rr014', '01088', '01090'], jouer=['rr014'], payer_avec=['01088', '01090'], cibles=['01094']),
    _c("rr014 Unrivaled Might — avec 3 compteurs en jeu : 10 degats « instead »",
       "« 10 damage instead if there are 3+ balance counters in play » ; `RemoveNemesisAside` : sinon le 3e compteur REVELE le Void et Malevolent re-cible la 1re attaque sur lui (comportement voulu)",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.RemoveNemesisAside()", f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 3)"], [],
       {'degats': [['01094', 10]]}, main_exclusive=['rr014', '01088', '01090'], jouer=['rr014'], payer_avec=['01088', '01090'], cibles=['01094'], accepter_choix=True),
    # ============================================================ rr010 Energy Flare
    _c("rr010 Energy Flare — 3 degats a CHAQUE ennemi en jeu (Rhino prend 3, Hydra Mercenary a 3 PV est abattu)",
       "« each enemy in play » ; `DealDamage(ennemis, 3, ..)`",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('01101')"], [],
       {'degats': [['01094', 3]], 'hors_jeu': ['01101']}, main_exclusive=['rr010', '01088', '01090'], jouer=['rr010'], payer_avec=['01088', '01090'], accepter_choix=True),
    # ============================================================ rr011 Global Influence
    _c("rr011 Global Influence — retire 3 menaces du complot principal (5 -> 2) malgre un sbire Patrol engage",
       "modele `ca010` ; « ignoring the patrol keyword »",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.SetThreat('01097b', 5)", "Puzzle.PutIntoPlay('16119')"], [],
       {'menace': [['01097b', 2]]}, main_exclusive=['rr011', '01089'], jouer=['rr011'], payer_avec=['01089'], cibles=['01097b'], accepter_choix=True),
    _c("rr011 Global Influence — avec 3 compteurs : 5 menaces retirees (6 -> 1)",
       "« 5 threat instead if there are 3+ balance counters in play »",
       ["Puzzle.EmptyHand()", HEROS, PD, f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 3)", "Puzzle.SetThreat('01097b', 6)"], [],
       {'menace': [['01097b', 1]]}, main_exclusive=['rr011', '01089'], jouer=['rr011'], payer_avec=['01089'], cibles=['01097b'], accepter_choix=True),
    # ============================================================ rr009 Purposeful Disparity
    _c("rr009 Purposeful Disparity — en forme HEROS, une attaque de 3 (Hydra Mercenary ATK 1... Rhino 2) inflige 1 de moins",
       "`WhenUnitWouldTakeDamage(.., is_from_attack=True)` + `ReduceDamage(1)` ; mesure : Rhino (ATQ 2) attaque Sentry : 1 degat au lieu de 2",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.Exhaust('rr001a')", "Puzzle.PutIntoPlay('rr009', under_control=True)"], ["Puzzle.EnemyAttacks('01094', 'rr001a')"],
       {'degats_identite': 1}, accepter_choix=True),
    _c("rr009 Purposeful Disparity — TEMOIN : sans la carte, la meme attaque inflige 2",
       "base : l'ATQ de Rhino est 2",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.Exhaust('rr001a')"], ["Puzzle.EnemyAttacks('01094', 'rr001a')"],
       {'degats_identite': 2}, accepter_choix=True),
    # ============================================================ rr005 The Watchtower (bonus +2 THW)
    _c("rr005 The Watchtower — « You get +2 THW » : Sentry (THW 1) deja a 3 : un Thwart de base retire 3 menaces (5 -> 2)",
       "`GiveKeywordToInPlayWhenApplyThis(Hero, control_by=\"You\", thwart=2)` ; mesure par l'effet d'un Thwart de base",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr005', under_control=True)", "Puzzle.SetThreat('01097b', 5)"], ["Puzzle.Thwart('rr001a')"],
       {'menace': [['01097b', 2]]}, cibles=['01097b'], accepter_choix=True),
    _c("rr005 The Watchtower — TEMOIN : sans la tour, un Thwart de base retire 1 menace (5 -> 4)",
       "THW de base 1",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.SetThreat('01097b', 5)"], ["Puzzle.Thwart('rr001a')"],
       {'menace': [['01097b', 4]]}, cibles=['01097b'], accepter_choix=True),
]

CAS += [
    # ============================================================ rr018 Angel of Death
    _c("rr018 Angel of Death — revelee avec le Void en jeu : elle s'attache AU VOID",
       "modele `ca017` (`AttachToFaceWhenPutIntoPlay`)",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr016')"], ["Puzzle.Reveal('rr018')"],
       {'attaches': [['rr016', 'rr018']]}, accepter_choix=True),
    _c("rr018 Angel of Death — Void ABSENT : 2 compteurs sur Duality Aspect PUIS surge (la carte suivante du deck est distribuee)",
       "`if_cannot_operation` + `if_cannot_gain_surge`",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"], ["Puzzle.Reveal('rr018')"],
       {'compteurs': [[DUALITE, 'balance', 2]], 'carte_du_surge': '01101'}, accepter_choix=True),
    # ============================================================ rr008 Pacifying Presence
    _c("rr008 Pacifying Presence — Rhino frappe Sentry (blesse de 3) : les 2 degats sont EMPECHES, la carte est defaussee, puis 2 degats sont soignes (3 -> 1)",
       "`WhenUnitWouldTakeDamage(HeroInterrupt)` + `PreventDamage('All')` + soin autant que de degats",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.Exhaust('rr001a')", "Puzzle.Damage('rr001a', 3)", "Puzzle.PutIntoPlay('rr008', under_control=True)"], ["Puzzle.EnemyAttacks('01094', 'rr001a')"],
       {'degats_identite': 1}, accepter_choix=True),
    _c("rr008 Pacifying Presence — TEMOIN sans la carte : la meme attaque s'ajoute aux 3 degats (5)",
       "base",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.Exhaust('rr001a')", "Puzzle.Damage('rr001a', 3)"], ["Puzzle.EnemyAttacks('01094', 'rr001a')"],
       {'degats_identite': 5}, accepter_choix=True),
    # ============================================================ Specials resolus PAR LE VOID depuis la defausse (rr019 le fait s'activer, 3 compteurs)
    _c("rr012 Nigh-Invulnerability — Special (via Void a 3 compteurs) : le Void ne subit AUCUN degat cette phase (2 attaques de Sentry : la 1re absorbee par Toughness, la 2e normalement 3 par le plancher)",
       "`GiveStatus(.., 'Tough')` + `RegisterTemp(WhenUnitWouldTakeDamage(..), until_phase_end=True)` + `PreventDamage('All')` ; sans le module la 2e attaque inflige au moins 3",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr016')", f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 3)", "Puzzle.CreatePlayerDiscardPile('rr012')"],
       ["Puzzle.Reveal('rr019')", "Puzzle.Attack('rr001a')", "Puzzle.Ready('rr001a')", "Puzzle.Attack('rr001a')", "Puzzle.Ready('rr001a')", "Puzzle.Attack('rr001a')"],
       {'degats': [['rr016', 0]]}, cibles=['rr016'], accepter_choix=True),
    _c("rr011 Global Influence — Special (via Void a 3 compteurs, SCH 3) : 3 menaces sur CHAQUE manigance (complot principal 1 -> 4)",
       "`PlaceThreatOnSchemes(\"EachScheme\", X)` avec X = SCH du Void",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr016')", "Puzzle.SetThreat('01097b', 1)", f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 3)", "Puzzle.CreatePlayerDiscardPile('rr011')"],
       ["Puzzle.Reveal('rr019')"], {'menace': [['01097b', 4]]}, accepter_choix=True),
    _c("rr010 Energy Flare — Special (via Void ATQ 3) : le Void attaque chaque personnage (Sentry subit 3) et chaque AUTRE ennemi (Hydra Mercenary, 3 PV, est abattu)",
       "`AttackCharacter` sur chaque cible ; overkill",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.Exhaust('rr001a')", "Puzzle.PutIntoPlay('rr016')", "Puzzle.PutIntoPlay('01101')", f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 3)",
        "Puzzle.CreatePlayerDiscardPile('rr010')"], ["Puzzle.Reveal('rr019')"],
       {'hors_jeu': ['01101'], 'degats_identite_min': 3}, accepter_choix=True),
    _c("rr014 Unrivaled Might — Special (via Void ATQ 3) : le Void attaque le vilain (Rhino subit 3) ET Sentry (subit 3)",
       "deux attaques, piercing",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.Exhaust('rr001a')", "Puzzle.PutIntoPlay('rr016')", f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 3)", "Puzzle.CreatePlayerDiscardPile('rr014')"],
       ["Puzzle.Reveal('rr019')"], {'degats': [['01094', 3]], 'degats_identite_min': 3}, accepter_choix=True),
]

CAS += [
    # ============================================================ rr007 Molecularkinesis (TEXTE du 03/11 : Hero Interrupt, annule une carte rencontre revelee)
    _c("rr007 Molecularkinesis — Equilibrium Intent est revelee (sans Void elle poserait 1 compteur) : ses effets sont ANNULES (les compteurs ne bougent pas), la carte est defaussee, Molecularkinesis aussi, et on pioche 1 carte par compteur de Duality Aspect (2)",
       "modele `bkw/08008` (`WhenPlayerRevealCard` + `CancelAllEffectsAndDiscardIt`) ; `DrawUp(n)`",
       ["Puzzle.EmptyHand()", HEROS, PD, f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 2)", "Puzzle.PutIntoPlay('rr007', under_control=True)"], ["Puzzle.Reveal('rr019')"],
       {'taille_main': 2, 'hors_jeu': ['rr007'], 'compteurs': [[DUALITE, 'balance', 2]]}, accepter_choix=True),
    _c("rr007 Molecularkinesis — TEMOIN : sans compteur sur Duality Aspect, l'annulation a lieu (0 compteur, pas le +1 d'Equilibrium Intent) mais on ne pioche rien",
       "« draw 1 card for each balance counter on Duality Aspect » : 0",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr007', under_control=True)"], ["Puzzle.Reveal('rr019')"],
       {'taille_main': 0, 'hors_jeu': ['rr007'], 'compteurs': [[DUALITE, 'balance', 0]]}, accepter_choix=True),
    # ============================================================ rr013 Obliterate (TEXTE du 03/11)
    _c("rr013 Obliterate — choix « vaincre un sbire non-ELITE » : Hydra Mercenary (Garde 1, 3 PV) est vaincu SANS attaque",
       "`DefeatUnits(.., ignore_when_defeated=True)` ; decision utilisateur : choix direct sans degats",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('01101')"], [],
       {'hors_jeu': ['01101']}, main_exclusive=['rr013', '01088', '01090'], jouer=['rr013'], payer_avec=['01088', '01090'], accepter_choix=True,
       preferer_option='Defeat a non-ELITE minion', cibles=['01101']),
    _c("rr013 Obliterate — Special (via Void a 3 compteurs) : la carte au plus HAUT COUT que Sentry controle (The Watchtower, 3) est defaussee",
       "`printed_cost.val` ; trois defausses (carte, sbire aux PV les plus hauts, complot annexe a la plus haute menace)",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr016')", "Puzzle.PutIntoPlay('rr005', under_control=True)", f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 3)",
        "Puzzle.CreatePlayerDiscardPile('rr013')"], ["Puzzle.Reveal('rr019')"],
       {'hors_jeu': ['rr005']}, accepter_choix=True),
]

CAS += [
    # ============================================================ modulaire Merged Sentry (rr020-rr023)
    _c("rr021 External Darkness — revelee : Merged Sentry est CHERCHE dans le deck rencontre et entre en jeu engage, avec autant de compteurs overwhelm que le stade du complot principal (1)",
       "`Search.EncounterCard` + `PutIntoPlay` (ca016/ca022) ; X = `printed_stage` du complot principal",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('rr020')"], ["Puzzle.Reveal('rr021')"],
       {'en_jeu': ['rr020'], 'compteurs': [['rr020', 'overwhelm', 1]]}, accepter_choix=True),
    _c("rr023 Scourge Blast — Merged Sentry en jeu : +1 compteur overwhelm (1 -> 2) puis 2 degats indirects a Sentry",
       "« place 1 counter ... take 1 indirect damage for each overwhelm counter »",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr020')", "Puzzle.PlaceCounters('rr020', 'overwhelm', 1)"], ["Puzzle.Reveal('rr023')"],
       {'compteurs': [['rr020', 'overwhelm', 2]], 'degats_identite': 2}, accepter_choix=True),
    _c("rr023 Scourge Blast — TEMOIN : sans Merged Sentry, surge (la carte suivante est distribuee) et aucun degat",
       "« Otherwise, this card gains surge »",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"], ["Puzzle.Reveal('rr023')"],
       {'carte_du_surge': '01101', 'degats_identite': 0}, accepter_choix=True),
    _c("rr022 Newfound Nature — revelee avec Merged Sentry en jeu : elle s'attache A MERGED SENTRY et pose X compteurs (stade du vilain 1)",
       "`AttachToFaceWhenPutIntoPlay` ; X = `printed_stage` du vilain",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.EmptyEncounterDeck()", "Puzzle.PutIntoPlay('rr020')"], ["Puzzle.Reveal('rr022')"],
       {'attaches': [['rr020', 'rr022']], 'compteurs': [['rr020', 'overwhelm', 1]]}, accepter_choix=True),
    _c("rr020 Merged Sentry — plancher et +X ATQ : avec 2 compteurs overwhelm, une attaque de 2 (apres la 1re absorbee par Toughness) lui inflige au moins 2 et il est a 2 degats",
       "plancher par attaque (meme lecture que Void)",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr020')", "Puzzle.PlaceCounters('rr020', 'overwhelm', 2)"],
       ["Puzzle.Attack('rr001a')", "Puzzle.Ready('rr001a')", "Puzzle.Attack('rr001a')"],
       {'degats': [['rr020', 2]]}, cibles=['rr020'], accepter_choix=True),
]

CAS += [
    # ============================================================ rr016 Void : MALEVOLENT (page de regles A4 du 03/11)
    _c("rr016 Malevolent — la 1re attaque de Sentry du round vise Rhino mais est RE-CIBLEE sur le Void : Rhino ne subit rien",
       "`WhenUnitWouldAttackUnit` + `ChangeTarget` (modele `ca019`) ; marqueur par attaquant et par round",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr016')"], ["Puzzle.Attack('rr001a')"],
       {'degats': [['01094', 0]]}, cibles=['01094'], accepter_choix=True),
    _c("rr016 Malevolent — la 2e attaque du MEME round n'est plus contrainte : elle touche Rhino (2)",
       "« first attack each round » : seule la premiere est re-ciblee",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr016')"], ["Puzzle.Attack('rr001a')", "Puzzle.Ready('rr001a')", "Puzzle.Attack('rr001a')"],
       {'degats': [['01094', 2]]}, cibles=['01094'], accepter_choix=True),
    _c("rr016 Malevolent — TEMOIN : sans le Void en jeu, la 1re attaque de Sentry touche Rhino (2)",
       "la capacite vit sur le Void",
       ["Puzzle.EmptyHand()", HEROS, PD], ["Puzzle.Attack('rr001a')"],
       {'degats': [['01094', 2]]}, cibles=['01094'], accepter_choix=True),
    _c("rr016 Malevolent — Rhino allait attaquer Sentry alors que le Void est engage avec le joueur : il attaque le VOID a la place (Sentry, epuise, ne subit rien)",
       "« If an enemy would attack you while the Void is engaged with you, that enemy attacks the Void instead »",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.Exhaust('rr001a')", "Puzzle.PutIntoPlay('rr016')"], ["Puzzle.EnemyAttacks('01094', 'rr001a')"],
       {'degats_identite': 0}, accepter_choix=True),
]

CAS += [
    # ============================================================ cas manquants
    _c("rr020 Merged Sentry — When Defeated : abattu (1 PV restant, 2 attaques dont la 1re absorbee par Toughness), il N'EST PAS defait : il reste en jeu comme ALLIE, PV remis a 4 (0 degat)",
       "modele `warriors_three/wt020` (`SetBeInstead` + `HealHealth` + `TreatAsAlly`) ; sans la capacite il serait hors jeu",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.PutIntoPlay('rr020')", "Puzzle.SetHealth('rr020', 1)"],
       ["Puzzle.Attack('rr001a')", "Puzzle.Ready('rr001a')", "Puzzle.Attack('rr001a')"],
       {'en_jeu': ['rr020'], 'degats': [['rr020', 0]]}, cibles=['rr020'], accepter_choix=True),
    _c("rr022 Newfound Nature — ★ : Merged Sentry (avec la carte attachee) attaque un allie (Hulk, 5 PV : il survit aux 3 degats) et le blesse : l'allie est ETOURDI",
       "`AfterUnitAttackAndDamageUnit(.., \"AttachedEnemy\", Ally, op)` + `GiveStatus(.., 'Stunned')`",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.EmptyPlayerDeck()", "Puzzle.Exhaust('rr001a')", "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('rr020')",
        "Puzzle.PutIntoPlay('rr022')", "Puzzle.Attach('rr022', 'rr020')"], ["Puzzle.EnemyAttacks('rr020', '01050')"],
       {'statuts': [['01050', 'Stunned']]}, accepter_choix=True),
    _c("rr022 Newfound Nature — TEMOIN : sans la carte attachee, l'allie blesse n'est PAS etourdi",
       "★ porte par la carte",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.EmptyPlayerDeck()", "Puzzle.Exhaust('rr001a')", "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('rr020')"],
       ["Puzzle.EnemyAttacks('rr020', '01050')"], {'statuts_absents': [['01050', 'Stunned']]}, accepter_choix=True),
    _c("rr008 Pacifying Presence — Special (via Void a 3 compteurs) : le Void (3 degats : le 1er `Damage` est absorbe par Toughness, le 2e s'applique) est SOIGNE de 2 par joueur (2) -> il lui reste 1 degat",
       "`HealthUnits([void], 2 * nb_joueurs)` ; `NoOutOfPlayLimit`",
       ["Puzzle.EmptyHand()", HEROS, PD, "Puzzle.EmptyEncounterDeck()", "Puzzle.RemoveNemesisAside()", "Puzzle.PutIntoPlay('rr016')", f"Puzzle.PlaceCounters('{DUALITE}', 'balance', 3)", "Puzzle.Damage('rr016', 1)", "Puzzle.Damage('rr016', 3)",
        "Puzzle.CreatePlayerDiscardPile('rr008')"], ["Puzzle.Reveal('rr019')"],
       {'degats': [['rr016', 1]]}, accepter_choix=True),
]
