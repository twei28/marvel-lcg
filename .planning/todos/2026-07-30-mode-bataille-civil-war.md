# TODO / SPEC — Mode Bataille Civil War (PvP / co-op par équipes)

**Statut :** investigué, non implémenté. **Pas une campagne** — un mode de jeu distinct.
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
