# RoboCop (Alex Murphy / RoboCop) : gabarits PROCESSUS-CARTE, 01/11/2026

Pack `robocop` (prefixe `rc`, set 238, auteur MissSugarPink). Scripts : `src/cards/pack/robocop/{robocop,robocop_nemesis}/` (18 cartes). Cas : `tools/cas/robocop.py` (voir « Verifications ») ; deck `robocop` ; textes FR : `ui-app/src/board/textes-fr-fanmade.ts` ; biographie : `public/js/prepare/heros-info.js` (`rc001a`).

**Aucune carte n'est « terminee »** (PROCESSUS-HEROS : « pas de heros a moitie valide ») : la partie humaine complete n'a pas ete jouee, et toutes les lectures sont tranchees.

## Source

1. **Drive** « Robocop (Released) » : `Hero/AE` (heros + alter-ego), `Hero Cards` (les 15 numeros « n/15 »), `Drip` (variante « full art » de l'alter-ego + Leg Holster), `Nemesis Set` (VIDE pour le connecteur Drive, comme le dossier Buffy).
2. **Images envoyees par l'utilisateur** : le set nemesis (ED-209, Corporate Demonstration, Stairs, Fugitives x2), l'obligation Classified, Leg Holster, Alex Murphy, RoboCop, et cinq cartes de base illustrees par l'auteur (Down Time, Endurance, Genius, Strength, Energy).
3. **Non importees** : Down Time (`05033`), Endurance (`05023`), Genius / Strength / Energy (`01089` / `01090` / `01088`) sont les cartes OFFICIELLES a l'identique (texte, cout, ressource) : art alternatif, pas un contenu de jeu. La variante « full art » d'Alex Murphy (Drip) est un art seul. **Leg Holster** est importee (`rc017`) : texte identique a `20021` Side Holster, mais renommee par l'auteur (« Leg Holster », sous-titre « Side Holster »), donc carte du pack.
4. Scans ramenes a 615 de petit cote (`assets/pics/rc0*.jpg`, dossier ignore par git), RGBA aplati sur noir.

**Numerotation** : rc001a/b identite ; rc002 Authorized Force x3 ; rc003 Dead or Alive x3 ; rc004 No Collateral x2 ; rc005 Auto-9 ; rc006 Internal Reload System ; rc007 Flightpack ; rc008 Terminal Spike ; rc009 Gunarm ; rc010 Squad Car ; rc011 Officer Lewis ; rc012 obligation Classified ; rc013 ED-209 ; rc014 Corporate Demonstration ; rc015 Stairs ; rc016 Fugitives x2 ; rc017 Leg Holster. Deck de heros = les 15 numeros « n/15 » (rc002 x3, rc003 x3, rc004 x2, rc005-rc011), `obligations = [rc012]`, `nemesis_set = [rc013, rc014, rc015, rc016, rc016]`, `player_deck` vide.

**Modification du MOTEUR** : seulement les traits `OFFICER` et `CREEP` (`card_face.py`) et leur traduction (`traits_fr_maison.json`, `traits-fr.ts` et generes). Aucun changement de mecanique.

## Verifications

- **Cas** : `tools/test_capacites.py .game-src <port> <rapport> rc0` : 67/67.
- **Substitution** (`tools/substituer_pack.py ... rc0`, pack sauvegarde avant, identique apres) : **18/18 cartes** avec au moins un cas rouge sans leur module. Les verts restants sont des TEMOINS d'absence (carte sans l'effet), des bases natives (`Patrol`, icone Amplification, `Uses`) ou des temoins d'expiration (la restriction de Fugitives tombe a la fin de l'activation, la limite de `Uses`).
- **Gates** : `test_cards`, `verifier_api_cartes`, `verifier_prefixes`, `verifier_appels_modules robocop`, `verifier_tous_les_decks`, vitest (`textes-fr-fanmade`, `vocabulaire-statuts`, `traduction-public`, `robocop-plateau`) : tous verts le 01/11/2026 : `test_cards` 7862 OK / 0 erreur ; `verifier_api_cartes` 8877 fichiers, 0 en faute ; `verifier_prefixes` OK ; `verifier_appels_modules robocop` OK ; `verifier_tous_les_decks` **178/178** (`robocop` : identite rc001a, main 5, deck 10) ; vitest 37/37 (`textes-fr-fanmade`, `vocabulaire-statuts`, `robocop-plateau`, `buffy-plateau`, `traduction-public`, `zones-corrections`).

## Navigateur (01/11/2026, Chromium via ui-check, moteur local ; extension Chrome non connectee)

- **Biographie PROUVEE** dans le wizard (Solo > Fan-made > RoboCop) : texte, identite civile, base, equipes, ennemis, premiere apparition.
- **Voile francais vu a l'ecran** sur la face heros / alter-ego, Authorized Force, Auto-9 (avec glossaire RESTREINT et A DISTANCE) ; les 17 cartes ont ete survolees (captures), lecture detaillee faite sur 4 d'entre elles seulement. Le menu de l'identite propose bien Auto-9 comme action ; le parcours complet « cible + paiement » n'a pas ete rejoue a la souris (les cas du harnais le font).
- **Parcours souris d'Auto-9 PROUVE (01/11/2026, `ui-check/tests/robocop-auto9.spec.ts`, moteur local 2351)** : Alex Murphy > Changer de forme > clic sur l'amelioration Auto-9 (carte agrandie en FR, glossaire RESTREINT / A DISTANCE) > bouton AUTO-9 > cible unique Rhino prise d'office > panneau « Payer 1 pour Auto-9 / Il manque 1 ressource » > clic sur Squad Car en main : Rhino 14 -> 12, Squad Car defaussee, Auto-9 inclinee. Captures `captures/robocop-auto9/`. **Main VIDE (second test du spec)** : Auto-9 est bien proposee, le panneau « Payer 1 pour Auto-9 / Il manque 1 ressource » s'ouvre avec le bouton de confirmation grise, ANNULER ferme le panneau (« Action annulee : Auto-9 »), Auto-9 reste prete, Rhino intact, le tour continue : le joueur n'est pas coince (captures `7-main-vide.png`, `8-main-vide-annule.png`). Particularite : le pilote commun `ouvrirEtMettreEnPlace` repond « Action » a la 1re question du tour (recherche d'Alex Murphy restee ouverte) : le spec fait sa propre mise en place.
- Non fait : une partie complete jouee.

## Decisions de montage (a lire avant de toucher aux cartes)

- **rc001a RoboCop : « resolve an Action ability from a WEAPON upgrade you control »** : le chemin `Message.WhenPlayerLikeInTurn` + `player.ChooseEffects` (celui de `MakeBasicPowerLikeInTurn`) joue l'Action comme en tour : cout PAYE, cibles CHOISIES. `CardFace.ResolveAbility` (« resolve the Special ability ») saute le cout (`skip_cost=True`) et prend la premiere cible : il ne convient pas. Cas : `rc001a ... TEMOIN DU COUT`.
- **« Action » entre guillemets couvre Hero Action** (`flags.is_action`) : Auto-9 et Gunarm sont des Hero Actions ; sinon l'Interruption ne ferait rien.
- **rc009 Gunarm : `Uses` fait tout** (3 jetons a l'entree, defausse au dernier). Une premiere version ajoutait `ThisEnterPlayWithCounters(3, 'ammo')` : 6 jetons (mesure). Lire `mots-cles/uses.md` AVANT le script.
- **rc006 Internal Reload System** : modele `33003` (`for_ability="Auto-9"`, regle temporaire `GainPiercing` sur l'attaque payee). L'Action d'Auto-9 porte `SetName("Auto-9")`.
- **rc016 Fugitives** : `PlayersCannotTriggerAbility` enregistree par `RegisterTemp(.., until_event_end=<WhenUnitWouldAttack|WouldScheme>)` : elle tombe a la fin de l'activation (cas d'expiration). Posee des le debut de l'attaque car le moteur ouvre la fenetre des Interruptions AVANT `WhenEnemyActivateAgainstYou` (premiere version, posee sur ce dernier : No Collateral passait encore ; cas rouge puis vert).
- **rc013 / rc014 / rc015** : Stairs est TROUVEE (deck rencontre, defausse, mise de cote nemesis) puis revelee ; si elle atterrit ailleurs que sur ED-209 (sbire a PV plus hauts), `AttachTo2(ED-209)` la ramene (cas avec Mister Hyde, 10 PV).
- **Icones de manigance** : rc014 porte l'AMPLIFICATION (avion + croix), comparee aux scans officiels `16054` / `01109` / `01108` / `01107` ; elle a aussi fait trouver le meme defaut sur Buffy (4 manigances sans leur icone, corrige).
- **Pieges de mesure rencontres** : une carte presente en DEUX exemplaires dans le deck (Hydra Mercenary) ne se blesse pas par `Puzzle.Damage('<id>')` (le degat part sur l'autre copie) ; `Puzzle.Engage` provoque une activation ; vider le deck (`EmptyPlayerDeck`) fait remelanger la defausse ; `main_exclusive` verse le reste de la main dans la defausse ; la Tenace de Sandman absorbe le premier degat.
- **Aucun cas pour** : l'effet « Any player may trigger » de Officer Lewis (multijoueur ; Classified a un cas a deux joueurs, `siege=1`, ajoute le 01/11), les regles de construction de deck (« up to 6 Justice cards » : texte seulement, comme les autres « you may include » du depot).

## Question tranchee par l'utilisateur (01/11/2026)

1. **rc016 Fugitives** : decision finale « Oui, les evenements en main aussi » : les Interruptions des cartes du joueur EN JEU ET de ses evenements EN MAIN (No Collateral) sont bloquees pendant l'activation. Cas `rc016 ... l'EVENEMENT a Interruption en main` ; rc0 = 64/64.

## Questions tranchees (01/11/2026, suite)

2. **rc010 Squad Car** (tranche) : « 1 RoboCop card » = carte du set RoboCop (classe Hero, propre a l'identite). Code inchange.
3. **rc012 Classified** (tranche) : « You cannot attack the villain » = le JOUEUR entier, allies compris. Le `"You"` du moteur n'exclut que l'identite ; code passe a `"AnyPlayer"` + condition sur le joueur (modele `hs015`). Cas allie + temoin ajoutes ; rc0 = 67/67.

4. **« resolve an Action ability »** (rc001a) (tranche) : cout paye, cibles choisies. Code inchange.

**Plus aucune question en attente.**

## Manques (a dire noir sur blanc)

1. **Aucune partie reelle humaine complete.** Autoplay (rhino, normal, equilibre, 8 parties) : 0 exception (grep sur les 8 journaux), 0 victoire, 3,5 rounds ; **3 parties sur 8 « bloquees »** : le pilote reste coince devant l'Action d'Auto-9, offerte par le moteur alors que la main est VIDE (le cout « 1 ressource de n'importe quel type » est impayable : l'option reste proposee, puis echoue). C'est le meme comportement du moteur que celui note dans `tools/autoplay.py` pour Tenacity (01093) : une option offerte puis refusee. A confirmer en vraie partie : le joueur verrait Auto-9 proposee sans pouvoir la payer.
2. **Multijoueur** : « Any player may trigger » (Officer Lewis ; Classified couvert par un cas), RoboCop avec un autre joueur, ED-209 revele par un autre joueur (un cas a deux joueurs existe pour l'engagement).
3. Images non versionnees (`assets/pics/` ignore par git) : a recopier sur une autre machine.
4. Cinq cartes de base illustrees et la variante full art non importees (art seul).
