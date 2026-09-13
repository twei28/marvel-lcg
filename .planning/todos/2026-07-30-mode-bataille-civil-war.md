# TODO / SPEC — Mode Bataille Civil War (PvP / co-op par équipes)

**Statut :** ✅ **TERMINÉ le 13/08/2026.** Coopératif validé en jeu (§6-§7),
mode expert des 4 scénarios livré (§8), et **compétitif complet** : les sept
chantiers du §10 sont fermés (§12). Une partie à deux camps se lance depuis
l'écran de préparation, se joue de bout en bout et **se gagne par un camp**,
avec les trois conditions de victoire, la règle des phases égales et les cinq
départages du livret.
⚠️ Ce qui n'a PAS été fait, et par décision : **personne n'a encore joué une
partie de Bataille dans un navigateur.** Tout ce qui suit est mesuré par le
moteur (`tools/test_competitif.py`, 7 cas), jamais vu à l'écran.
⚠️ Le §2 et le §4 de cette fiche disaient que le compétitif dépendait du serveur
permanent multijoueur : **c'est faux, et mesuré comme tel** (§9.1).
**Pas une campagne** — un mode de jeu distinct.
**Date :** 2026-07-30
**Origine :** exclusion de Civil War du mode Campagne pendant le chantier des campagnes. Mis de côté ici pour un traitement dédié.
**Rapport aux campagnes :** aucun. Civil War n'est PAS une campagne vilain ; ne pas l'ajouter à `CAMPAIGN_CODES`. C'est un système de **bataille par équipes** qui demande son propre flux de préparation.

---

## 1. Ce qu'est Civil War (constaté dans le code + produit officiel)

Extension « bataille » où **deux équipes de héros s'affrontent** (thème Civil War : loi de recensement). Chaque équipe a un **leader** ; l'autre équipe joue contre lui.

- **Scénarios** (`data/sets_info.json`, clé `cw`) = les 4 **leaders adverses** possibles : `iron_man`, `captain_marvel`, `captain_america`, `spider_woman`. Ce ne sont pas des vilains classiques : ce sont des héros jouables retournés en « leader d'équipe adverse ».
- **Deux camps** : `registration` (pro-recensement, camp Iron Man) et `resistance` (anti-recensement, camp Cap).
- **Sets d'équipe** (encounters) : `mighty_avengers`, `new_avengers`, `secret_avengers`, `the_initiative`, etc.
- Héros du set : `tigra`, `hulkling`.

## 2. Deux modes supportés par le moteur

Le code `cw` référence **les deux** :
- **Compétitif** (`IsCompetitiveMode`, 6 occurrences) : deux équipes de joueurs humains s'affrontent.
- **Coopératif** (`IsCooperativeMode`, 1 occurrence) : une équipe de joueurs contre un **leader adverse automatisé**.
- `GetEnemyLeader` (22 occurrences), champ `team`/`Team` (60+ occurrences), `side`.

**Point important :** la logique de bataille est **déjà dans le moteur**, pas seulement dans les cartes cw — voir `src/game/operate/worlds.py` (`IsCompetitiveMode`/`IsCooperativeMode`/`GetEnemyLeader`), `src/game/card/face/card_face.py`, `selector_target*.py`, `ability/factory/do_attack.py`. Donc **le gros du moteur existe** ; le travail est surtout côté préparation + lancement + (peut-être) sièges d'équipe.

Exemple (`cw/registration/56063a.py`) : `assert not Worlds.IsCompetitiveMode(effect)` puis, si `IsCooperativeMode`, révèle un complot secondaire du set du `GetEnemyLeader`. → le même scénario se comporte différemment selon le mode.

## 3. Pourquoi ça ne rentre pas dans l'écran « Préparer une partie » actuel

L'assistant suppose **N héros vs 1 scénario (vilain)**. La bataille suppose :
- choisir un **camp** (Registration / Resistance) ;
- choisir le **leader adverse** (= le « scénario » cw) ;
- choisir **compétitif** (2 équipes de joueurs, sièges antagonistes) **ou coopératif** (vs leader auto) ;
- composer **une ou deux équipes** de héros.

Le descripteur de lancement actuel (`launcher.js` → `campaign_json` + `hero_json[]` + `rules[]`) n'a pas de notion d'équipes/camps/leader. Il faut vérifier comment le moteur active le mode bataille (quelle règle / quel champ du descripteur → `IsCompetitiveMode`/`IsCooperativeMode`, comment `GetEnemyLeader` est renseigné, comment les sièges sont assignés aux 2 camps).

## 4. Plan (esquisse — à préciser après investigation du lancement)

1. **Reverse-engineer le lancement bataille** : trouver comment une partie Civil War était lancée dans le jeu original (chercher un `?` de mode bataille, une règle `mode_competitive`/`mode_battle`, ou un format de `NewGameDescriptor` avec équipes). Regarder `server_new_game.py`, `game_new.py`, `scene/loader.py`, et les specs `ui-check/tests/` si elles couvrent la bataille.
2. **Décider co-op d'abord** (plus simple, aligné sur le hot-seat local) : une équipe de joueurs locale vs un leader adverse automatisé. Le compétitif (2 équipes distantes) dépend du serveur multijoueur (voir [[2026-07-28-serveur-permanent-multijoueur]]) et de l'identité par siège.
3. **Nouveau flux de préparation** (variante ou branche de `prepare.html`) : sélection camp → leader adverse → mode (co-op/compétitif) → composition d'équipe(s). Ne pas polluer le flux campagne/standard existant.
4. **Étendre le descripteur** (`launcher.js` + moteur) : transmettre camp, leader, mode, et la répartition des héros par équipe.
5. **Tester** dans le vrai moteur (pas le serveur statique) — même contrainte que pour AoS : besoin d'une instance moteur testable.

**Ampleur estimée :** moyen-gros. Le cœur de règles est dans le moteur ; le travail est côté UI de préparation + descripteur de lancement + (pour le compétitif) sièges/serveur.

## 5. Rappels techniques
- Source moteur = **WSL** `~/marvel-work/fusion/marvel-lcg-src/src/` (copie Windows périmée — voir [[engine-source-of-truth]]).
- Contrainte de test : pas de 2e instance du vrai moteur (assert port 2345, occupé par l'online). Le port 2346 = serveur **statique**, pas le moteur.
- Ne PAS mettre `cw` dans `CAMPAIGN_CODES` (`public/js/prepare/app.js`) : ce n'est pas une campagne.


## 6. INVESTIGATION DU 13/08/2026 : le coopératif MARCHE DÉJÀ

La fiche estimait l'ampleur « moyen-gros » et supposait qu'il fallait un nouveau
flux de préparation, un descripteur étendu et du reverse-engineering. **La mesure
dit autre chose.**

### 6.1 Ce qui a été mesuré, pas supposé

* **Le moteur force le coopératif** : `Worlds.IsCompetitiveMode` retourne
  `False` **en dur** (`-> Literal[False]`), `IsCooperativeMode` retourne `True`.
  Il n'y a donc rien à « activer » : le mode coopératif EST le mode.
* **Un scénario Civil War a la structure d'un scénario ordinaire**
  (`data/scenarios/iron_man.json` : villain, schemes, encounters, modular_sets).
  Rien de particulier à lancer.
* **Les 4 leaders se jouent de bout en bout.** `tools/autoplay.py` a mené une
  partie complète contre chacun — Iron Man (9 rounds), Captain America (4),
  Captain Marvel (3), Spider-Woman (3). **Aucun plantage, aucune réponse
  illégale.**
* **Les 2 héros de la boîte se jouent** : Tigra et Hulkling, une partie chacun.
* **La boîte est DÉJÀ proposée dans l'écran de préparation.** Vérifié dans un
  vrai navigateur : `catalog.extensions()` rend « 56. Civil War » avec ses quatre
  scénarios et ses deux héros — parce que `sets_info.json` les déclare et que le
  catalogue lit ce fichier.

### 6.2 Ce qui reste vraiment

**Le coopératif est jouable aujourd'hui.** Ce qui manque :

1. **Une partie menée par un humain**, du wizard à la fin — le seul juge, comme
   toujours. Le bot ne dit pas si l'expérience tient debout (le camp est-il
   lisible ? les sets d'équipe arrivent-ils ?).
2. **Le mode COMPÉTITIF** (deux équipes de joueurs) : désactivé en dur dans le
   moteur. Il dépendait du serveur permanent multijoueur, **chantier abandonné le
   13/08**. Sans lui, le compétitif n'a pas de chemin.
3. **Le choix explicite du camp** (Registration / Resistance) à la préparation :
   à évaluer en jouant. En coopératif, le camp est implicitement l'opposé du
   leader choisi, et les sets d'équipe sont déjà dans les modulaires du scénario.

### 6.3 Conséquence sur l'ampleur

**Ce n'est plus un chantier « moyen-gros ».** Le contenu (227 cartes, 184
modules), les règles (dans le moteur) et le lancement (par l'écran ordinaire)
existent. Il reste à JOUER pour voir ce qui manque — et, si le compétitif est
voulu un jour, à rouvrir la question du serveur.


---

## 7. Validé en jeu (13/08/2026)

**L'utilisateur a joué Civil War et confirme que ça fonctionne.** Le mode
coopératif est donc clos : une équipe de héros contre un leader adverse
automatisé, lancé depuis l'écran de préparation ordinaire.

Ce qui reste ouvert, et seulement si le besoin s'en fait sentir :

* **le mode compétitif** (deux équipes de joueurs humains) — il faudrait d'abord
  rouvrir le serveur permanent multijoueur, et lever le `return False` en dur de
  `Worlds.IsCompetitiveMode` ;
* **le choix explicite du camp** (Registration / Resistance) à la préparation —
  non nécessaire en coopératif, où le camp est l'opposé du leader choisi.


---

## 8. LE MODE EXPERT MANQUAIT — livré le 13/08/2026 (`3ab6266`)

Point 1 de la reprise (« le camp est-il lisible ? ») : **le camp n'est pas le
problème, le livret le dit**. En coopératif le joueur n'a PAS de camp — « choisir
un camp » est l'étape 1 de la *création de scénario*, et l'obligation de camps
opposés est explicitement réservée au compétitif (mc56 p.4). Le camp est une
propriété du leader adverse et de ses sets, et les 4 scénarios livrés
reproduisent exactement les listes du livret (p.7-8).

**Vérifié aussi, contre l'apparence** : 9 faces de complot et 8 stades de leader
n'ont pas de module, mais aucun n'est inerte — ils passent par
`ability_link`/`full_link` (`56141a → 56063a`). Cartes cw à texte, sans module
et sans lien : **0**.

**Ce qui manquait vraiment** : aucun fichier `*_expert.json` pour les 4 leaders.
C'étaient, avec les 4 de Synthezoid, les 8 seuls scénarios du jeu dans ce cas,
alors que les stades III/IV sont dans les données et déjà branchés. 8 fichiers
écrits, générateur contrôlé en reconstruisant `rhino_expert.json` à l'octet près,
8 parties complètes par autoplay, et la preuve par substitution via les PV de
départ (Iron Man 12 en normal → 16 en expert = stade III).

---

## 9. LE COMPÉTITIF : CE QUI A ÉTÉ MESURÉ, PUIS CONSTRUIT (13/08/2026)

Trois commits : `8857de3` (le drapeau et le descripteur), `de3f14d` (les deux
tables et la famille équipe), `f14150e` (le round enfilé et les six cartes).

### 9.1 Deux prémisses de cette fiche étaient fausses

* **Le serveur n'était pas le verrou.** Le jeu multi-sièges existe déjà :
  `launch.online.json` porte `seat_passwords` à 4 places, avec `JOUER-EN-MULTI.bat`
  et `tools/test_serveur_multi.py`. Le chantier abandonné était celui d'un serveur
  PERMANENT hébergé, pas du jeu à plusieurs.
* **Le socle « deux tables » n'était pas à bâtir.** `World.game_areas` est une
  LISTE avec `CreateGameArea()`, et ce n'est pas du code mort : **Kang s'en sert
  en vrai** (`toafk/kang/__init__.py:107`). `GetMainSchemes`, `GetSideSchemes`,
  `FindVillainByGameArea` et `GetEncounterDeck` filtrent DÉJÀ par zone, et un
  vilain peut porter son propre deck rencontre (`Villain.SetEncounterDeck`).

### 9.2 Le vrai verrou, trouvé par la sonde et non déduit

La première mesure montrait les DEUX complots dans la première zone et aucun
leader dans la seconde, **alors que le code visait explicitement la bonne zone**.
La trace a nommé le coupable : `Deck.Insert` recalcule la zone d'une carte à
CHAQUE insertion, depuis son propriétaire. Or les decks du scénario appartiennent
au scénario, et `Scenario.GetGameArea()` rend la PREMIÈRE zone tant que la partie
n'a pas commencé. Toute carte de la seconde table était ramenée à la première au
moment même où on l'y posait.

**Leçon à garder** : viser une zone ne suffit pas, c'est le deck d'arrivée qui
tranche.

### 9.3 Ce qui marche aujourd'hui, mesuré

`tools/sonde_competitif.py` monte une partie à deux camps et la mène :

* deux zones, un complot principal chacune, deux leaders différents, **deux decks
  rencontre distincts** ;
* chaque table révèle **sa propre copie de Choosing Sides** ;
* le round suit l'ordre du livret : héros camp 0, héros camp 1, vilain camp 0,
  vilain camp 1 ;
* **partie complète en 5 rounds, zéro erreur fatale.**

Le vocabulaire d'équipe veut enfin dire quelque chose, lu depuis la table de la
carte : « the enemy leader » est celui posé sur VOTRE table, « your leader » est
le vôtre et il est en face (les équipes échangent leurs scénarios, p.14 étape 4),
« the enemy team » sont les joueurs d'en face. **En coopératif, les quatre
fonctions rendent exactement ce qu'elles rendaient** — c'est ce que le livret p.6
demande.

Non-régression sur les trois lots : `test_cards` 4331 ok / 0 erreur (inchangé),
une partie ordinaire rend le même résultat qu'avant, et Kang mène 3 parties.

---

## 10. CE QUI RESTAIT AU COMPÉTITIF — LES SEPT POINTS SONT FERMÉS

La liste était rangée par ordre de ce qui bloquait le plus un joueur. Le détail
de chaque correctif est au §12.

1. ~~Aucun chemin de lancement.~~ **FAIT le 13/08** (`802f457`), voir §11.
1 bis. ⏳ **Regarder ce qu'une partie de Bataille DONNE À VOIR.** Toujours
   ouvert, et c'est le seul : le plateau React ne connaît pas les zones de jeu
   (`grep -rn "game_area" ui-app/src` rend 0). Une partie jouée dans un
   navigateur tranchera. Le reste a été fait sans attendre, à la demande de
   l'utilisateur (« finis Civil War complètement »).
2. ~~Les conditions de victoire sont globales.~~ **FAIT** (§12.1) : trois
   conditions par camp, la règle des phases égales, et les cinq départages.
3. ~~Les PV du leader comptent tous les joueurs.~~ **FAIT** (§12.2) : Iron Man
   démarre à 12 PV face à un joueur, 24 face à deux.
4. ~~Un seul jeton de premier joueur.~~ **FAIT** (§12.3) : un par camp, qui
   tourne à la fin de la phase vilain de SON camp.
5. ~~L'étape 3 de la mise en place manque.~~ **FAIT** (§12.4) : les 4 cartes
   joueur du leader de chaque camp sont mises de côté, et 56128b les donne.
6. ~~56158 Switching Sides ne sait pas offrir une fenêtre de paiement à un
   joueur d'une autre table.~~ **FAIT** (§12.5).
7. ~~L'isolement entre tables n'a pas été audité.~~ **FAIT** (§12.6), et
   l'audit a trouvé une vraie fuite.

---

## 11. LE CHEMIN DE LANCEMENT (13/08/2026, `802f457`)

`NewGameDescriptor` gagne trois champs **à défaut** : `campaign_json_2`,
`encounter_set_names_2`, `teams`. Un descripteur qui ne les porte pas se charge
exactement comme avant. L'écran de préparation a une tuile **Bataille**, un
sélecteur pour le leader d'en face, et **déduit le camp du siège** (le livret ne
connaît que le 1v1 et le 2v2, donc première moitié contre seconde moitié).

⚠️ **Le sélecteur ne tient pas une liste de boîtes en dur** : un scénario de
bataille se reconnaît dans les DONNÉES, son adversaire étant de type `Leader`.
C'est la leçon de l'aspect Determination. Mesuré : 8 scénarios trouvés.

**Vérifié, et le test mis en défaut exprès** : `bataille-descripteur.spec.ts`
exige les trois clés et le drapeau en Bataille, et leur ABSENCE en partie
ordinaire. Un descripteur de bataille envoyé à `/new` rend « New game created ».

### Deux pièges payés, pour la prochaine fois

* **`UI_CHECK_BASE` ne traverse pas vers le node Windows sans `WSLENV`.** Sans
  lui, Playwright visait le serveur du JOUEUR sur 2345 et le test passait en
  mesurant le mauvais fichier. Commande juste :
  `UI_CHECK_BASE=http://127.0.0.1:2346 WSLENV=UI_CHECK_BASE npx playwright test ...`
* **`/new` refuse une URL de plus de 8190 octets.** Un descripteur de bataille
  porte deux scénarios ; il tient (**4696 octets en 1v1**) parce que le
  navigateur envoie du JSON COMPACT. Le reconstruire à la main avec le texte
  indenté des fichiers de scénario le fait exploser.

### ⚠️ CE QUI N'A PAS ÉTÉ MESURÉ, et qui compte

**Le plateau React ne connaît pas les zones de jeu** : `grep -rn "game_area"
ui-app/src` rend **0**. Une partie de Bataille se lance, mais personne n'a
encore regardé ce qu'elle DONNE À VOIR. Deux possibilités, et seule une partie
jouée dans un navigateur tranchera : soit le rendu du moteur est déjà filtré par
zone et le plateau montre la bonne table sans le savoir, soit les deux tables
s'affichent mêlées. **C'est le prochain point à mesurer, avant d'ajouter quoi
que ce soit d'autre.**

---

## 12. LE COMPÉTITIF EST COMPLET (13/08/2026, soir)

Sept chantiers, six correctifs et une fuite trouvée en auditant. Tout est
mesuré par `tools/test_competitif.py` (7 cas, un processus chacun — le moteur
ne sait monter qu'une partie par processus).

### 12.1 La fin de partie se gagne PAR UN CAMP

Nouveau `src/game/world/competitive.py`. Le principe tient en une phrase du
livret : « The game does not end until both sides have played an equal number
of phases » (p.17). Une condition atteinte n'arrête donc plus la partie, elle
est **enregistrée** ; la partie s'arrête à la fin de la phase du camp
resistance, qui joue en second dans le round enfilé.

Les quatre portes du moteur ont été détournées, chacune en gardant son
comportement d'avant hors mode compétitif :

* `AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame` et
  `World.AdvanceMainScheme` → `World.RecordCompetitiveDefeat` ;
* `World.CheckIsAllPlayersEliminated` → compte **par camp**, sur
  `const_seat_order_players` (un joueur éliminé sort de `const_players`) ;
* `Scenario.AdvanceVillainStage` → `IsCompetitiveLeaderDefeated`, qui compte les
  leaders **de la zone** : le test global « il ne reste que celui-ci » n'est
  jamais vrai avec deux leaders sur la table ;
* `Worlds.PopEncounterCards` (deck rencontre vide) → c'est le camp de CETTE
  table qui perd, pas la partie entière.

⚠️ **Le sens se lit depuis la table.** Un complot accompli ou des héros vaincus
donnent le point au camp d'EN FACE (c'est SON leader qui a réussi) ; un leader
vaincu donne le point au camp de sa table. C'est ce renversement qui a fait
rendre le mauvais vainqueur au premier jet, et la sonde l'a montré tout de
suite.

Deux camps perdus = les deux perdent. Deux leaders vaincus = égalité, et les
**cinq départages** de la p.17 tranchent, dans l'ordre : stade 1B non dépassé,
sbires et manigances en zone, menace sur le complot, PV restants, attachements
sur le leader.

Un leader vaincu **reste en jeu** (p.17 : « it remains on the table [...] so it
can still be targeted »). Un garde-fou empêche le moteur de le vaincre deux
fois.

Le client reçoit `winning_team` et `teams` (le camp de chaque siège) :
`players_won` seul ne suffit pas, le MÊME descripteur sert aux deux tables.
`ui-app` lit ça dans `board/fin-partie.ts` (4 tests), et l'écran de fin dit
« Votre camp l'emporte » ou « Le camp adverse l'emporte » au lieu de parler des
héros. Les quatre raisons de fin sont traduites.

### 12.2 Les PV du leader se comptent sur SA table

`WorldAction.GetPlayerNumIcon` rend la moitié des sièges en mode compétitif.
Le livret ne connaît que le 1v1 et le 2v2 (p.14) et l'écran de préparation
coupe les sièges en deux : les deux camps ont donc toujours la même taille.
Un seul point de correction, et il porte tout ce qui se compte « par joueur » :
PV du leader, menace de départ du complot, `GetYourTeamSize`.

Mesuré : Iron Man 12 PV en 1v1 (24 avant), 24 en 2v2 ; Captain America 14 et 28.

### 12.3 Un jeton de premier joueur par camp

`World.PassFirstPlayerToken` tourne **les places tenues par un camp** dans
`self.players`, l'autre camp gardant les siennes. Appelé à la fin de la phase
vilain de chaque camp (p.16) ; la rotation globale de fin de round est coupée en
compétitif, sinon le jeton changerait de camp. `Identity.SetActive` ne retire le
jeton qu'aux joueurs du même camp — sans quoi les deux jetons ne pourraient pas
coexister. La mise en place en pose un par camp.

### 12.4 Les 4 cartes joueur du leader (étape 3, p.14)

`Competitive.CartesDuLeader` les trouve **dans les données** : ce sont les
cartes de type joueur du set du leader. Piège payé : le set d'un leader porte le
nom du personnage, et ce nom est DÉJÀ celui d'un set de héros (« Iron Man »
désigne aussi la boîte de base) — sans filtre par pack, on mettait 13 cartes de
côté au lieu de 4.

Une réserve par CAMP (`World.GetTeamSetAside`), pas par joueur : les 4 cartes
sont celles de l'équipe, qui se les partage à deux en 2v2. `56128b Now It's
Personal` en donne 2 à chaque joueur du camp, avec `SetOwner` — sans quoi la
carte repartirait à la défausse du scénario. L'écart assumé du 13/08 est levé.

### 12.5 56158 Switching Sides

La fenêtre de paiement à un joueur d'une autre table n'était pas un manque du
moteur : `player.AskSpendResources` s'adresse à n'importe quel joueur. L'allié
défaussé est proposé à chaque joueur du camp d'en face, dans l'ordre des sièges,
et entre en jeu sur SA table sous SON contrôle.

⚠️ **Le déferlement change de sens, et c'est délibéré.** « If no ally left play
this way » est l'idiome habituel du jeu (« If you cannot, this card gains
surge », mw020) : la carte déferle quand AUCUN allié n'a été défaussé, pas quand
personne n'a racheté. Avant ce lot elle déferlait à chaque révélation en
compétitif, et jamais en coopératif.

### 12.6 L'isolement des tables, et la fuite trouvée en l'auditant

L'audit (`mesurer_isolement`, joué à la mise en place ET après une partie
entière) compare la zone de CHAQUE carte de chaque joueur à celle de son
identité. Il a trouvé du premier coup : **toute la main, le deck et la défausse
du second camp naissaient sur la table du premier.**

Cause : `Player.GetGameArea` rendait la PREMIÈRE zone tant que la partie n'avait
pas commencé, et `Deck.Insert` demande sa zone au propriétaire du deck
d'arrivée. Chaque carte piochée pendant la mise en place atterrissait donc chez
l'adversaire. La table d'un joueur est maintenant celle de son identité dès
qu'elle existe.

C'est la même leçon qu'au lot précédent, sous un autre angle : **viser une zone
ne suffit pas, c'est le deck d'arrivée qui tranche.**

Deux autres isolements réparés au passage, tous deux en mode compétitif :
l'élimination d'un joueur passait ses sbires et son jeton au joueur SUIVANT,
qui est à l'autre table en 1v1 ; et le nettoyage « Fix Kang » (retirer les
complots d'une zone vidée) effaçait la table du camp perdant, que les départages
doivent encore mesurer.

### Un défaut du PILOTE trouvé en route, et il ne vient pas d'ici

La partie 2v2 ne se terminait jamais : un seul tour de Tigra mangeait le
plafond de questions. Mesuré : le moteur reposait indéfiniment la MÊME question
(une capacité « Ask » visant une autre identité), et un pilote qui répond
toujours la première option la rechoisit sans fin.

⚠️ **Ce n'est pas le mode compétitif** : une partie ORDINAIRE à 4 joueurs, même
descripteur sans camps, se bloque exactement pareil. Le pilote de
`test_competitif.py` répond donc la n-ième option à la n-ième répétition d'une
question dans une même phase, puis DÉCLINE au bout de trois. La partie ordinaire
à 4 joueurs va alors jusqu'à sa fin en 226 questions. `tools/autoplay.py`, qui a
son propre garde-fou anti-boucle, ne joue que des parties en solo : personne
n'avait encore mené une partie à 4 par le bot.

### Ce que la mesure dit

`tools/test_competitif.py` : **7 cas, tous verts** (préparation 1v1 et 2v2,
verdicts, cartes du leader, switching sides, parties 1v1 et 2v2 complètes).
La partie 1v1 finit sur « The Registration Team Won », la 2v2 sur « Both Teams
Lost » — les deux camps ayant perdu dans la même fenêtre, ce qui exerce en vraie
partie la branche que le livret décrit.
Non-régression : `test_cards` 4352 ok / 0 erreur, `autoplay` mène des parties
ordinaires sans incident, `ui-app` 461 tests + `tsc` propres.

**Ce qui n'est PAS mesuré** : l'écran. Aucune partie de Bataille n'a été jouée
dans un navigateur, et le plateau ne connaît toujours pas les zones de jeu —
c'est le point 1 bis du §10, et il demande un humain.

## Clos le 13/09/2026

Décision de l'utilisateur : le mode sort du backlog tel quel, mesuré par le
moteur et jamais joué dans un navigateur. « S'il y a un souci, on verra ça. »
