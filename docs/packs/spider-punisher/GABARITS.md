# Spider-Punisher (T-Wrecks) : gabarits PROCESSUS-CARTE, 18 card_id

Pack `spider_punisher`, préfixe `sq`, set 221. Source : zip « Spider-Punisher » déposé le 25/10/2026 (27 fichiers : 18 cartes distinctes, 15 du deck signature numérotées X/15, 5 du set némésis, 2 obligations ; images seules, **aucun texte fourni**, tout est lu sur les scans ; auteur T-Wrecks, Terre-71928). Extras non utilisés : `Cover.jpg`, `Playmat.jpg`, art alternatif `Peter Parker (1).png` / `Spider-Punisher.jpg`.

## Arbitrages du 26/10/2026 (RR 1.8 + scans)
Questions en attente tranchées par le Rules Reference et les scans (`VERDICTS-REGLES-2026-10-26.md`, `docs/rapports/2026-10-26-arbitrages-heros-fanmade.md`). Changent : **sq005 / sq012** (vrai trait AERIAL), **sq013** (« from play » : tous les joueurs), **sq014** (le premier joueur choisit l'allié). Le reste est « A confirmé ».

## NOTES DE REPRISE (état au 26/10/2026)

- Fait : cartes (`data/cards.json`, pack `spider_punisher`), `sets_info.json` (« 221. Custom (Spider-Punisher) »), préfixe `sq`, deck `deck/starter/spider_punisher.json` (`player_deck` VIDE), scripts `src/cards/pack/spider_punisher/{spider_punisher,spider_punisher_nemesis}/`, images `assets/pics/sq*.jpg` (18, `sq015` en paysage), textes FR (`ui-app/src/board/textes-fr-fanmade.ts`), biographie (`public/js/prepare/heros-info.js`, `sq001a`), cas `tools/cas/spider_punisher.py` (filtre `[sq] `).
- Dossier de jeu à moi : `Fusion/marvel-lcg-src/.game-src-sq` (copie des liens de `.game-src-rz`) ; commande : `flock /tmp/nc-lourd.lock ../../.venv-linux/bin/python3.10 tools/test_capacites.py .game-src-sq 36200 /tmp/rapport-sq.json "[sq] "`.
- Restait à la dernière mise à jour de cette note : voir la section « Reste à faire » en bas.

## Modifications du MOTEUR (toutes `# CORRECTIF`)

1. `src/game/card/face/card_face.py` : traits `EARTH-71928`, `WEB-SHOOTER` ajoutés à la liste (sans eux la partie ne se monte pas).
2. `src/game/world/world_stat.py` : compteurs par joueur et par round (`AddRoundCounter` / `GetRoundCounter`, remis à zéro en fin de round) pour « Limit 3 times per round » de Web-Sling.
3. `src/game/puzzle/puzzle.py` : `Puzzle.ReadyAtEndOfPlayerPhase()` (banc de test seulement) rejoue l'étape « redresser toutes ses cartes » de la fin de phase joueur avec le vrai effet `EndPhase`.

## Écart connu (à dire clairement)

Le trait **AERIAL** de Neighborhood Watch (« You gain the AERIAL trait when 2 or more upgrades you control are exhausted ») n'est PAS posé sur l'identité : le moteur n'a pas de trait conditionnel à l'état d'inclinaison. `EstAerien(joueur)` (`spider_punisher/__init__.py`) applique la règle imprimée pour les deux cartes qui la lisent (sq005, sq012). Une carte d'un AUTRE pack qui testerait AERIAL sur l'identité ne le verrait pas.


## Résultats

- **Cas** `[sq]` : 64/64 verts (63 puis le contre-cas sq006 corrigé) ; `Fusion/marvel-lcg-src/tools/cas/spider_punisher.py`.
- **Substitution** (`tools/substituer_pack.py .game-src-sq 36300 sq0`, pack sauvegardé puis diffé sans écart) : **18/18 cartes avec au moins un cas rouge sans leur module** ; les cas restés verts sont des contre-cas d'absence, des valeurs imprimées ou des témoins.
- **Autoplay** : 8 parties `spider_punisher` (rhino, normal, équilibré, graines 1 à 8) : 0 victoire, 4 défaites/fins de partie, **4 « bloquée »** ; témoin `she_hulk` : 8 parties, 1 « bloquée ». Grep tracebacks (NameError|AttributeError|TypeError|KeyError|AssertionError) : **0 partout** (16 journaux). Les 4 blocages = le pilote répète un Hero Action de Incendiary Rounds (`sq011`) offert mais dont le paiement échoue (« WhenPlayerInTurn failed »), pilote qui répète une action offerte mais impayable (RECETTES §27, `us008`) ; cause NON prouvée par trace de paiement à confirmer en partie réelle.
- **verifier_tous_les_decks** (`DECK_NOM=spider_punisher`) : OK, « identite sq001a, main 6, deck 9 » (`/tmp/deck_spider_punisher.json`).
- **Vocabulaire FR** : `textes-fr-fanmade.test.ts`, `vocabulaire-statuts/moteur/evenements.test.ts` verts (43 tests).
- **Partie humaine** : NON FAITE (toutes les cartes restent « NON (provisoire) »).


## Résultats

- **Cas** `[sq]` : 69/69 verts ; `Fusion/marvel-lcg-src/tools/cas/spider_punisher.py`.
- **Substitution** (`tools/substituer_pack.py .game-src-sq 36300 sq0`, pack sauvegardé puis diffé sans écart) : **18/18 cartes avec au moins un cas rouge sans leur module** ; les cas restés verts sont des contre-cas d'absence, des valeurs imprimées ou des témoins.
- **Autoplay** : **avant correctif** : 8 parties `spider_punisher` (rhino, normal, équilibré, graines 1 à 8) = 0 victoire, 4 fins de partie, **4 « bloquée »** (témoin `she_hulk` : 1 sur 8) ; cause PROUVÉE : le moteur OFFRE une Hero Action à coût de ressource même quand la main ne peut rien payer (reproduit sans mes générateurs : `actions_disponibles` = 1 main vide, sq008 et sq011), le paiement échoue (« WhenPlayerInTurn failed », journal ligne 114 de la graine 2 : sq011 offerte après que la main a été dépensée) et le pilote répète la même action sans effet. **Correctif** : `ActionPayable(coût)` (`spider_punisher/__init__.py`) en `conditions` des Hero Actions de sq008, sq009, sq010, sq011 et de l'obligation sq017 : offerte seulement si les icônes imprimées de la main et de la réserve couvrent le coût (`PeutCouvrirLeCout`), ou si With Great Firepower est prête. **après correctif** : 8 parties, 0 victoire, 8 fins de partie, **0 bloquée** (4 éliminés, 4 complot principal), 0 traceback ; le témoin reste à 1 sur 8. Cas ajoutés (4) : action NON offerte main vide (sq011, sq008), NON offerte avec [energy] seul (sq008), offerte avec une ressource (sq011) et avec With Great Firepower prête. Le journal des 8 parties reste témoin de régression.
- **verifier_tous_les_decks** (`DECK_NOM=spider_punisher`) : OK, « identite sq001a, main 6, deck 9 » (`/tmp/deck_spider_punisher.json`).
- **Vocabulaire FR** : `textes-fr-fanmade.test.ts`, `vocabulaire-statuts/moteur/evenements.test.ts` verts (43 tests).
- **Partie humaine** : NON FAITE (toutes les cartes restent « NON (provisoire) »).


## Résultats

- **Cas** `[sq]` : 69/69 verts ; `Fusion/marvel-lcg-src/tools/cas/spider_punisher.py`.
- **Substitution** (`tools/substituer_pack.py .game-src-sq 36300 sq0`, pack sauvegardé puis diffé sans écart) : **18/18 cartes avec au moins un cas rouge sans leur module** ; **refaite après les `conditions` `ActionPayable` pour sq008 (3/5), sq009 (3/3), sq010 (3/3), sq011 (6/7), sq017 (2/2)**, empreinte du pack identique avant et après (`e0f486f0...`, `diff -rq` vide) ; les cas restés verts sont des contre-cas d'absence, des valeurs imprimées ou des témoins.
- **Autoplay** : **avant correctif** : 8 parties `spider_punisher` (rhino, normal, équilibré, graines 1 à 8) = 0 victoire, 4 fins de partie, **4 « bloquée »** (témoin `she_hulk` : 1 sur 8) ; cause PROUVÉE : le moteur OFFRE une Hero Action à coût de ressource même quand la main ne peut rien payer (reproduit sans mes générateurs : `actions_disponibles` = 1 main vide, sq008 et sq011), le paiement échoue (« WhenPlayerInTurn failed », journal ligne 114 de la graine 2 : sq011 offerte après que la main a été dépensée) et le pilote répète la même action sans effet. **Correctif** : `ActionPayable(coût)` (`spider_punisher/__init__.py`) en `conditions` des Hero Actions de sq008, sq009, sq010, sq011 et de l'obligation sq017 : offerte seulement si les icônes imprimées de la main et de la réserve couvrent le coût (`PeutCouvrirLeCout`), ou si With Great Firepower est prête. **après correctif** : 8 parties, 0 victoire, 8 fins de partie, **0 bloquée** (4 éliminés, 4 complot principal), 0 traceback ; le témoin reste à 1 sur 8. Cas ajoutés (4) : action NON offerte main vide (sq011, sq008), NON offerte avec [energy] seul (sq008), offerte avec une ressource (sq011) et avec With Great Firepower prête. Le journal des 8 parties reste témoin de régression.
- **verifier_tous_les_decks** (`DECK_NOM=spider_punisher`) : OK, « identite sq001a, main 6, deck 9 » (`/tmp/deck_spider_punisher.json`).
- **Vocabulaire FR** : `textes-fr-fanmade.test.ts`, `vocabulaire-statuts/moteur/evenements.test.ts` verts (43 tests).
- **Partie humaine** : NON FAITE (toutes les cartes restent « NON (provisoire) »).

## Cartes

### sq001a : Spider-Punisher — Hero, traits EARTH-71928, WEB-WARRIOR

[star] Spider-Punisher's attacks from [[Web-Shooter]] upgrades gain ranged. / <i>Web-Sling</i> — <b>Response</b>: After you ready your cards at the end of the player phase, for each 2 upgrades you readied this way, deal 1 damage to an enemy or remove 1 threat from a scheme. (Limit 3 times per round.)

- [x] Étape 2 : carte(s) de référence : `iw005` Flying Disk / `nt009` (UnitAttackGainKeyword conditionnel) ; `14009` / `dt131` (AfterCardReady) ; compteur par round : CORRECTIF `world_stat.py`.
- [x] Étape 5 : mots-pièges : « ★ ... attacks FROM Web-Shooter upgrades » (la carte porteuse, pas l'identité) ; « for each 2 upgrades you READIED THIS WAY » (fin de phase seulement) ; « Limit 3 TIMES per round » ; « or » (dégât OU menace) ; Response facultative. Conforme au code.
- [x] Étape 6 : nombres texte <-> code : PV 11, ATK 2, THW 2, DEF 2, main 5 (cas valeurs imprimées).
- [x] Étape 7 : cas (10) : valeurs imprimees PV 11, THW 2, ATK 2, DEF 2, main 5, EARTH-71928 WEB- | 2 ameliorations redressees en fin de phase -> 1 degat a Rhino | 4 ameliorations redressees -> 2 degats (une fois par paire) | CONTRE-CAS une seule amelioration redressee -> aucun degat | branche « remove 1 threat from a scheme » (3 -> 2) | TEMOIN D'EPUISEMENT, 8 ameliorations redressees (4 paires) -> 3 fois s | CONTRE-CAS en ALTER EGO, rien ne part | CONTRE-CAS une redressement HORS fin de phase (Swing and Reload) ne co | attaque de High Explosive Rounds contre un ennemi RETALIATE -> aucune  | TEMOIN, attaque de BASE contre le meme ennemi RETALIATE -> 1 degat de . Substitution : rouges 5/10.
- [x] Étape 7 bis : limite imprimée ? OUI : 3 fois par round, témoin d'épuisement (8 améliorations, 4 paires -> 3 dégâts).
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite ; question en attente : Web-Sling est une Réponse FORCÉE à choix facultatif posée par PAIRE (une proposition par paire redressée), non une unique Réponse répétée N fois. Option A (codé) / B une seule Réponse avec N répétitions..

### sq001b : Peter Parker — AlterEgo, traits GENIUS

<i>Vengeance</i> — <b>Action</b>: Search your deck and discard pile for a [[Web-Shooter]] upgrade and add it to your hand. (Limit once per phase.)

- [x] Étape 2 : carte(s) de référence : `ho007` Otto, `an001b` (Search.PlayerCard + GainCard).
- [x] Étape 5 : mots-pièges : « deck AND discard pile » ; « Limit once per phase » ; trait WEB-SHOOTER (pas WEAPON). Conforme au code.
- [x] Étape 6 : nombres texte <-> code : PV 11, REC 3, main 6.
- [x] Étape 7 : cas (6) : valeurs imprimees PV 11, REC 3, main 6, GENIUS | cherche Armor-Piercing Rounds (WEB-SHOOTER) dans le deck -> en main | cherche aussi dans la DEFAUSSE (EMP Rounds) | CONTRE-CAS une amelioration qui n'est PAS WEB-SHOOTER (Neighborhood Wa | TEMOIN D'EPUISEMENT, apres UNE Action la capacite n'est plus offerte ( | TEMOIN, avant toute Action la capacite est offerte (nombre = 1). Substitution : rouges 5/6.
- [x] Étape 7 bis : limite imprimée ? OUI : une Action par phase, témoin : après la première, « 0 action disponible ».
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite.

### sq002 : Enhanced Combat Sense — Event, traits aucun

[star] You can exhaust any number of [[Weapon]] or [[Tech]] upgrades you control to generate that many [wild] resources while paying for this card. / <b>Hero Interrupt</b>: When an encounter card is revealed from the encounter deck, discard it. For each upgrade you exhausted to pay for this card, deal 1 damage to an enemy or remove 1 threat from a scheme.

- [x] Étape 2 : carte(s) de référence : `44005` / `15006` (WhenPlayerRevealCard, annuler et défausser) ; `tc001a` (CanGenerateResources, ex_operation marque la carte payée).
- [x] Étape 5 : mots-pièges : « any number » (une capacité par amélioration) ; « for each upgrade you exhausted to pay » ; « discard it » ; coût 3★. Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Coût 3 (3*) ; 3 améliorations = 3 ressources.
- [x] Étape 7 : cas (2) : revelation d'une carte rencontre -> elle est defaussee (payee avec 3 r | [star] 3 ameliorations inclinees pour la payer -> 3 resources, puis 3 . Substitution : rouges 2/2.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite ; question en attente : « discard it » = annuler tous les effets de la carte révélée et la défausser (A, codé) ou la défausser seulement (B) ; le coût « 3★ » est lu comme 3..

### sq003 : Point Blank — Event, traits ATTACK

<b>Hero Action</b> <i>(attack)</i>: Deal 3 damage to an enemy. You may exhaust up to 2 [[Weapon]] upgrades you control. For each exhausted this way, deal 3 damage to that enemy.

- [x] Étape 2 : carte(s) de référence : `01021` Gamma Slam (attaque), `01022` (plusieurs dégâts).
- [x] Étape 5 : mots-pièges : « You MAY exhaust UP TO 2 WEAPON upgrades » ; « for each exhausted this way, deal 3 damage TO THAT ENEMY ». Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Coût 3 ; 3 + 3 + 3 = 9 au plus.
- [x] Étape 7 : cas (4) : sans arme -> 3 degats a Rhino | 2 armes inclinees -> 3 + 3 + 3 = 9 degats | 3 armes -> au plus 2 inclinees (9 degats, une arme reste prete) | valeurs imprimees cout 3, trait ATTACK. Substitution : rouges 3/4.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite ; question en attente : Les 3 dégâts supplémentaires par arme sont des dégâts distincts (A, codé) ou s'ajoutent à l'attaque (B)..

### sq004 : Web Snatch — Event, traits TACTIC

<b>Hero Action</b>: Stun an enemy → search your deck and discard pile for an upgrade and add it to your hand. You may choose to discard an attachment from the villain's play area instead.

- [x] Étape 2 : carte(s) de référence : `05015` Tackle (étourdir), `ho007` (recherche).
- [x] Étape 5 : mots-pièges : « Stun an enemy -> search ... » (l'étourdissement est un coût : cible étourdissable exigée) ; « an attachment from the VILLAIN'S play area ». Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Coût 1.
- [x] Étape 7 : cas (2) : etourdit Rhino, cherche Neighborhood Watch dans le deck -> en main | variante « discard an attachment from the villain's play area instead . Substitution : rouges 2/2.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite ; question en attente : « attachment from the villain's play area » = attachements attachés au méchant seulement (A, codé) ou aussi ceux d'un sbire (B)..

### sq005 : Neighborhood Watch — Upgrade, traits CONDITION

You gain the [[Aerial]] trait when 2 or more upgrades you control are exhausted. / <b>Hero Action</b>: If you have the [[Aerial]] trait, exhaust this card → ready Spider-Punisher.

- [x] Étape 2 : carte(s) de référence : `09009` Cloak of Levitation (aérien + redresser), `iw005`.
- [x] Étape 5 : mots-pièges : « 2 or more upgrades you control are EXHAUSTED » ; « If you have the AERIAL trait » ; « ready Spider-Punisher » (pas l'allié). **ARBITRAGE DU 26/10/2026** : AERIAL est un VRAI trait de l'identite (`GiveKeywordToAttached("You", trait="AERIAL", get_new_value=deux_ameliorations_inclinees, ex_change_on_event=SurInclinaisonOuRedressement)`), recalcule a chaque inclinaison / redressement ; plus de raccourci.
- [x] Étape 6 : nombres texte <-> code : Coût 1.
- [x] Étape 7 : cas (3) : 2 ameliorations inclinees -> AERIAL -> redresse Spider-Punisher | CONTRE-CAS une seule amelioration inclinee (hors Watch) -> pas AERIAL, | valeurs imprimees cout 1, trait CONDITION. NOUVEAU : AERIAL est un vrai trait de l'identite (2 inclinees : present, vu ROUGE avant) ; temoin 1 seule inclinee : absent ; une amelioration redressee : le trait se PERD (cas vert, assertion d'absence : reste vert sans module, assume). Substitution : rouges 2/6.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite. Question TRANCHÉE le 26/10/2026 : le vrai trait AERIAL est posé sur l'identité. À vérifier en partie : l'affichage du trait AERIAL sur l'identité et qu'une carte d'un autre pack qui teste AERIAL le voit.

### sq006 : With Great Firepower — Upgrade, traits aucun

<b>Hero Resource</b>: Exhaust this card → generate a [wild] resource for an upgrade ability. / <b>Alter-Ego Action</b>: Exhaust this card → play a [[Weapon]] or [[Tech]] upgrade from your hand, reducing its cost by 2.

- [x] Étape 2 : carte(s) de référence : `26036` Meditation (PlayCardsLikeInTurn -3), `33003` (CanGenerateResources `for_ability`).
- [x] Étape 5 : mots-pièges : « for an upgrade ABILITY » (pas pour jouer) ; « WEAPON OR TECH » (traits, OU) ; « reducing its cost by 2 ». Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Coût 2 ; réduction de 2.
- [x] Étape 7 : cas (3) : Alter-Ego Action, joue Armor-Piercing Rounds (cout 2) pour 0 | CONTRE-CAS seule une amelioration ni WEAPON ni TECH (Neighborhood Watc | valeurs imprimees cout 2. Substitution : rouges 1/3.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite.

### sq007 : Concrete Perch — Support, traits LOCATION

<b>Hero Action</b>: Exhaust Concrete Perch and X [[Weapon]] or [[Tech]] upgrades you control (to a maximum of 4 upgrades) → look at the top X cards of the encounter deck, and return them to the top of the encounter deck in any order.

- [x] Étape 2 : carte(s) de référence : `40004` Precognition (LookAtDeck + PlaceOnTopInAnyOrder).
- [x] Étape 5 : mots-pièges : « X upgrades (to a maximum of 4) » ; « look at the top X » ; « in any order ». Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Coût 1 ; X <= 4.
- [x] Étape 7 : cas (2) : 2 ameliorations inclinees -> regarde les 2 premieres cartes rencontre  | valeurs imprimees cout 1, trait LOCATION. Substitution : rouges 1/2.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite ; question en attente : X est choisi pendant l'effet (inclinaison des améliorations avant de regarder) plutôt qu'en coût préalable ; X = 0 ne regarde rien..

### sq008 : Armor-Piercing Rounds — Upgrade, traits TECH, WEAPON, WEB-SHOOTER

<b>Hero Action</b> <i>(attack)</i>: Spend a [mental] resource and exhaust this card → deal 2 damage to an enemy. If that enemy has a tough status card, deal 5 damage instead. This attack gains piercing.

- [x] Étape 2 : carte(s) de référence : `nt009` (piercing/overkill conditionnel à la carte), `01105` (IsTough).
- [x] Étape 5 : mots-pièges : « If that enemy has a tough status card, deal 5 damage INSTEAD » ; « this attack gains piercing » ; « Spend a [mental] resource AND exhaust ». Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Coût 2 ; dégâts 2 / 5 ; ressource [mental].
- [x] Étape 7 : cas (5) : 2 degats a Rhino, l'amelioration s'incline | ennemi ROBUSTE (Shocker 3 PV) -> 5 degats : il est vaincu malgre Robus | CONTRE-CAS sans Robuste -> 2 degats seulement (Shocker 3 PV survit ave | SANS RESSOURCE [mental] EN MAIN la Hero Action n'est PAS offerte (nomb | main avec seulement [energy] (01088) -> la Hero Action [mental] n'est . Substitution : rouges 3/5.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite.

### sq009 : EMP Rounds — Upgrade, traits TECH, WEAPON, WEB-SHOOTER

<b>Hero Action</b>: Spend a [energy] resource and exhaust this card → stun or confuse a minion. You may shuffle this card into your deck to stun or confuse the villain instead.

- [x] Étape 2 : carte(s) de référence : `nt009` (ShuffleAllTo), `05015` (statuts).
- [x] Étape 5 : mots-pièges : « stun OR confuse a MINION » ; « You MAY shuffle this card into your deck to stun or confuse the VILLAIN INSTEAD ». Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Coût 1 ; ressource [energy].
- [x] Étape 7 : cas (3) : etourdit un sbire (Hydra Bomber) | desoriente un sbire | « shuffle this card into your deck » -> etourdit le MECHANT, la carte . Substitution : rouges 3/3.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite.

### sq010 : High Explosive Rounds — Upgrade, traits TECH, WEAPON, WEB-SHOOTER

<b>Hero Action</b> <i>(attack)</i>: Spend a [physical] resource and exhaust this card → deal 3 damage to an enemy. This attack gains overkill. If this attack defeats an enemy, draw 1 card. / <i>"The hunt ends loud." - Spider-Punisher</i>

- [x] Étape 2 : carte(s) de référence : `nt009` (overkill), `ag006`/`th009` (`if_this_attack_defeats`).
- [x] Étape 5 : mots-pièges : « this attack gains overkill » ; « If this attack defeats AN enemy, draw 1 card ». Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Coût 2 ; 3 dégâts ; ressource [physical].
- [x] Étape 7 : cas (3) : 3 degats a Rhino | vainc un sbire (Hydra Bomber 2 PV) -> overkill sur le mechant + pioche | CONTRE-CAS ne vainc pas -> pas de pioche. Substitution : rouges 3/3.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite.

### sq011 : Incendiary Rounds — Upgrade, traits TECH, WEAPON, WEB-SHOOTER

<b>Hero Action</b> <i>(attack)</i>: Spend 1 resource of any type and exhaust this card → deal 3 damage to an enemy. Reduce this damage by 1 for each other enemy in play, to a maximum of 2. Then deal 1 damage to that many other enemies.

- [x] Étape 2 : carte(s) de référence : `01022` Ground Stomp (plusieurs cibles), `ap030` (AskChooseFace).
- [x] Étape 5 : mots-pièges : « Reduce this damage by 1 for each OTHER enemy in play, to a maximum of 2 » ; « deal 1 damage to THAT MANY other enemies ». Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Coût 2 ; 3 - k dégâts, k <= 2.
- [x] Étape 7 : cas (7) : seul ennemi en jeu -> 3 degats | 1 autre ennemi -> 2 a Rhino, puis 1 a l'autre | 2 autres ennemis -> 1 a Rhino, puis 1 a chacun | 3 autres ennemis -> 1 a Rhino, 1 a DEUX des trois seulement (plafond 2 | SANS RESSOURCE EN MAIN la Hero Action n'est PAS offerte (nombre = 0) | TEMOIN, AVEC une ressource en main la Hero Action est offerte (nombre  | main VIDE mais With Great Firepower PRETE -> la Hero Action est offert. Substitution : rouges 6/7.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite ; question en attente : Avec plus de 2 autres ennemis, le joueur choisit lesquels sont touchés (A, codé)..

### sq012 : Swing and Reload — Upgrade, traits SKILL

<b>Hero Action</b>: If you have the [[Aerial]] trait, exhaust this card → ready another upgrade you control. / <b>Hero Interrupt</b>: When you would take any amount of damage, discard this card → prevent that damage.

- [x] Étape 2 : carte(s) de référence : `mf011` (WhenUnitWouldTakeDamage + PreventDamage), `09009` (ready).
- [x] Étape 5 : mots-pièges : « ANOTHER upgrade » ; « If you have the AERIAL trait » ; « discard this card -> prevent THAT damage » (tous les dégâts). Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Coût 1.
- [x] Étape 7 : cas (3) : AERIAL (2 ameliorations inclinees avec Watch) -> redresse une autre am | Interruption, 1 degat qui menace -> prevenu, la carte est defaussee | valeurs imprimees cout 1, trait SKILL. Substitution : rouges 2/3.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite. Question TRANCHÉE le 26/10/2026 : `EstAerien` lit désormais le VRAI trait de l'identité (voir sq005).

### sq013 : Punisher No More — Obligation, traits aucun

<b><i>Give to the Peter Parker player.</i></b> / You may flip to alter-ego form. Choose: / • Discard 2 [[Web-Shooter]] upgrades from play. Remove Punisher No More from the game. / • Exhaust Peter Parker → discard this obligation.

- [x] Étape 2 : carte(s) de référence : `kb014` Family = Trouble (obligation, choix à deux branches).
- [x] Étape 5 : mots-pièges : « You MAY flip » ; « 2 WEB-SHOOTER upgrades FROM PLAY » (**26/10/2026 : pas de « you control » et pas un coût : toute amélioration WEB-SHOOTER en jeu, tous joueurs ; le joueur de l'obligation choisit**) ; « Exhaust Peter Parker » (forme alter ego). Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Boost 2 ; donnée à Peter Parker.
- [x] Étape 7 : cas (2) : branche « exhaust Peter Parker -> discard this obligation » | branche « discard 2 Web-Shooter upgrades -> remove from the game ». NOUVEAU : à deux joueurs, un WEB-SHOOTER chez chacun → les deux sont défaussés (vu ROUGE avec l'ancien code). Substitution : rouges 3/3.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite. Question TRANCHÉE le 26/10/2026 (« from play » = tous les joueurs ; « Exhaust Peter Parker » exige l'alter ego, A confirmé).

### sq014 : Green Goblin — Minion, traits ELITE, GOBLIN

Toughness. / <b>Forced Interrupt</b>: When Green Goblin attacks you, he attacks an ally you control instead (if able). / <i>(Spider-Punisher's nemesis minion.)</i>

- [x] Étape 2 : carte(s) de référence : `ap030` / RECETTES §16.1 (AttackCharacter), `60182` Cop (SetBeInstead).
- [x] Étape 5 : mots-pièges : « attacks YOU » ; « an ally you control INSTEAD (if able) » ; Toughness native ; ELITE. Conforme au code. **26/10/2026 (RR First Player)** : plusieurs alliés admissibles pour une carte de rencontre → le PREMIER joueur choisit (`world.GetFirstPlayer()`), pas le joueur attaqué ; en solo c'est le même joueur.
- [x] Étape 6 : nombres texte <-> code : PV 6, ATK 2, SCH 2, boost 3, Toughness 1.
- [x] Étape 7 : cas (3) : attaque un allie du joueur au lieu du joueur (Hellcat 01020) | CONTRE-CAS sans allie, il attaque le joueur (2 degats) | valeurs imprimees PV 6, ATK 2, SCH 2, ELITE GOBLIN, Toughness. NOUVEAU : à deux joueurs, joueur 2 attaqué avec deux alliés → le joueur 0 (premier joueur) est interrogé (vu ROUGE : joueur 1 avant). Substitution : rouges 2/4.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite. Question TRANCHÉE le 26/10/2026 (le premier joueur choisit) ; la garde anti-boucle est correcte.

### sq015 : The Goblin's Ultimatum — SideScheme, traits aucun

<i>Goblin forces Peter to choose between his own life and Stacy's.</i> / Threat cannot be removed from this scheme except from its own abilities. / <b>Hero Action</b>: Exhaust your hero, discard 1 upgrade you control, or take 2 damage → remove 1 threat from this scheme. / <b>Forced Interrupt</b>: At the end of the next player phase, if this card is still in play, find the Spider-Punisher obligation and reveal it. Discard this card.

- [x] Étape 2 : carte(s) de référence : `01139b` (ThreatCannotBeRemovedFromWhile), `uw014` (Find.FindAndReveal), `pu114`.
- [x] Étape 5 : mots-pièges : « EXCEPT from its own abilities » ; trois coûts alternatifs (« or ») ; « at the end of the NEXT player phase, if STILL in play ». Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Menace de départ 2 (fixe) ; boost 2.
- [x] Étape 7 : cas (6) : entre en jeu avec 2 de menace | un heros ne peut PAS retirer sa menace en thwart | Hero Action « take 2 damage -> remove 1 threat from this scheme » | Hero Action « exhaust your hero » | Hero Action « discard 1 upgrade you control » | fin de la phase joueur -> devoile l'obligation Punisher No More et se . Substitution : rouges 5/6.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite ; question en attente : « next player phase » = la première fin de phase joueur après l'entrée en jeu ; l'obligation est cherchée par le premier joueur..

### sq016 : Reorganized Crime — Treachery, traits aucun

<b>When Revealed</b>: Search the encounter discard pile for a non-[[Elite]] minion and put it into play engaged with you. Give that minion a tough status card. If you cannot, this card gains surge. / <hr /> / [star] <b>Boost</b>: Reveal this card.

- [x] Étape 2 : carte(s) de référence : `53033` (GetEncounterDiscardPileCards), `01105` (donner Tenace, surge), `27124` (Boost : révéler).
- [x] Étape 5 : mots-pièges : « NON-ELITE minion » ; « engaged with YOU » ; « Give THAT minion a tough status card. If you cannot, ... surge » ; [star] Boost : révéler. Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Boost ★ + 1 (desc Boost 1).
- [x] Étape 7 : cas (3) : sbire non ELITE (Hydra Bomber) dans la defausse rencontre -> en jeu, R | CONTRE-CAS un sbire ELITE (Green Goblin) n'est pas cherche | aucune cible -> la carte gagne Renfort. Substitution : rouges 1/3.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite ; question en attente : « If you cannot » couvre l'absence de sbire (A, codé) ; le sbire est engagé avec le joueur qui révèle..

### sq017 : Revealed Identity — Obligation, traits aucun

<b>Forced Interrupt</b>: When the villain would scheme against you, it attacks you instead. Place 2 threat on the main scheme after that attack. / <b>Hero Action</b>: Spend 2 resources of any type → discard this card.

- [x] Étape 2 : carte(s) de référence : `60182` Cop / `uw015` (SetBeInstead sur manigance), `ap030` (DoAttackYou).
- [x] Étape 5 : mots-pièges : « it attacks you INSTEAD » (attaque normale avec boost) ; « Place 2 threat ... AFTER that attack » ; « 2 resources of ANY type ». Conforme au code.
- [x] Étape 6 : nombres texte <-> code : Boost 2 ; coût de défausse 2.
- [x] Étape 7 : cas (2) : le mechant manigance contre le joueur -> il l'ATTAQUE (2 degats), puis | Hero Action « spend 2 resources -> discard this card ». Substitution : rouges 2/2.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Résultats » (0 traceback).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement glissé, compteur, statut ou zone nouvelle ; pas de cas plateau).
Carte terminée : NON (provisoire) : partie humaine non faite ; question en attente : Obligation de set némésis sans « Give to » ; le joueur est celui visé par la manigance..

## Reste à faire / à vérifier en partie réelle

- Une partie complète jouée avec Spider-Punisher ; Web-Sling en fin de phase réelle ; Enhanced Combat Sense payée avec plusieurs améliorations ; Goblin's Ultimatum jusqu'à l'obligation ; le blocage du pilote sur Incendiary Rounds ; survol de la biographie dans l'assistant.
