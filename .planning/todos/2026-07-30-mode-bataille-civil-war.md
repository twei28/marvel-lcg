# TODO / SPEC — Mode Bataille Civil War (PvP / co-op par équipes)

**Statut :** ✅ **COOPÉRATIF TERMINÉ** le 13/08/2026, validé en jeu (voir §6-§7),
**plus le mode expert des 4 scénarios, livré le 13/08** (§8).
🚧 **COMPÉTITIF EN COURS** depuis le 13/08 : une partie à deux camps **se lance
depuis l'écran de préparation** et se joue de bout en bout dans le moteur
(§9, §11). Ce qui reste est nommé au §10.
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

## 10. CE QUI RESTE AU COMPÉTITIF, nommé et non deviné

Rien de tout cela n'est commencé. C'est la liste, par ordre de ce qui bloque le
plus un joueur.

1. ~~Aucun chemin de lancement.~~ **FAIT le 13/08** (`802f457`), voir §11.
2. **Les conditions de victoire sont encore globales.** Le premier complot
   principal complété termine TOUTE la partie. Le livret p.17 veut trois
   conditions par équipe, la règle « la partie ne s'arrête pas avant que les deux
   camps aient joué autant de phases », et cinq départages.
3. **Les PV du leader comptent tous les joueurs.** Mesuré : Iron Man démarre à 24
   PV pour 1 joueur en face, parce que `GetYourTeamSize` lit le nombre TOTAL de
   joueurs. Il doit lire la taille du camp qui l'affronte.
4. **Un seul jeton de premier joueur.** En 2v2 chaque camp a le sien (p.16).
5. **L'étape 3 de la mise en place manque** : les 4 cartes joueur du leader mises
   de côté, que Choosing Sides fait gagner (p.16). C'est ce qui bloque 56128b.
6. **56158 Switching Sides** ne sait pas offrir une fenêtre de paiement à un
   joueur d'une autre table.
7. **L'isolement entre tables n'a pas été audité** (p.16 : « card abilities on
   your side of the table completely ignore cards on the other side unless they
   specifically refer to them »).


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
