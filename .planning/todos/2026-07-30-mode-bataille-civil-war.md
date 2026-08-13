# TODO / SPEC — Mode Bataille Civil War (PvP / co-op par équipes)

**Statut :** ✅ **TERMINÉ le 13/08/2026 pour le mode COOPÉRATIF** — validé en jeu
par l'utilisateur. Rien n'a eu à être écrit : le contenu, les règles et le
lancement existaient déjà (voir §6). **Le mode COMPÉTITIF reste sans chemin** :
il est désactivé en dur dans le moteur et dépendait du serveur permanent
multijoueur, chantier abandonné le 13/08.
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
