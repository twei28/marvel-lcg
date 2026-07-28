# État du projet

## Référence projet

Voir : .planning/PROJECT.md (mis à jour le 2026-07-28)

**Valeur centrale :** Une interface digne du contenu : belle, claire et fluide sur PC, tablette et mobile, sans jamais toucher aux règles du moteur.
**Focus actuel :** Phase 1 — Filet de sécurité et boucle de dev (bloquante)

## Position actuelle

Phase : 1 sur 7 (Filet de sécurité et boucle de dev)
Plan : 01-01 et 01-03 terminés (2 sur 6 dans la phase courante ; 01-02 en cours en parallèle)
Statut : En cours
Dernière activité : 2026-07-28 — 01-03-PLAN.md terminé (34 états de jeu rejouables hors partie, /fixtures.html)

Progression phase 1 : [███░░░░░░░] 33% (2/6 plans)
Progression projet : [█░░░░░░░░░] ~5% (plans des phases 2 à 7 non encore découpés)

## Métriques

**Vélocité :**
- Plans terminés : 2
- Durée moyenne : 13 min
- Temps d'exécution total : 26 min

**Par phase :**

| Phase | Plans | Total | Moy./plan |
|-------|-------|-------|-----------|
| 1 — Filet de sécurité | 2/6 | 26 min | 13 min |

**Tendance récente :** 01-01 en 12 min (3 tâches, 3 déviations), 01-03 en 14 min (3 tâches, 6 déviations auto-corrigées)

*Mis à jour après chaque plan terminé*

## Contexte accumulé

### Décisions

Journal complet dans PROJECT.md (Key Decisions). Décisions structurantes pour le travail en cours :

- [Roadmap] Stack = React 19 + TS 6 + Vite 8, build multi-pages dans `public/app/`, migration page par page (étranglement par nom de fichier HTML, zéro modification backend).
- [Roadmap] Plateau découpé en 3 phases de risque croissant (5 restylage → 6 layout/tactile → 7 interactions), jamais en bloc, jamais en dernier.
- [Roadmap] Galerie de cartes, deck builder et replay différés en v1.x — les écrans actuels restent en service.
- [Roadmap] Le responsive est dans la definition of done de chaque écran ; seul le plateau a une phase de layout dédiée (changement de modèle, pas d'ajustement CSS).
- [Roadmap] Direction visuelle : squelette clair « instrument de jeu », personnalité comic dosée, thème sombre en option par tokens.
- [01-01] Marqueurs de page vérifiés contre le HTML réellement servi, jamais contre la doc : `#mode` (scene.html) est masqué par le wizard, remplacé par `#w-stepper` ; `body` remplacé par de vrais sélecteurs.
- [01-01] Garde-fou anti `clean_cache.html` par le titre de page (`Version Mismatch`), indépendant du marqueur de chaque écran.
- [01-01] `prepare.html` inclus comme 6e écran surveillé (`preparation-nouvelle`).
- [01-01] Les scripts npm des plans 01-02 à 01-05 sont déjà déclarés dans `ui-check/package.json` pour éviter que plusieurs plans se disputent ce fichier.
- [01-03] **Prouvé par mesure** : `game.world.render.descriptor` lu pendant un ask est bit à bit ce que renvoie `/get_world` (36 138 octets comparés). Le principe « le nouveau code est une fonction pure de `get_world` » n'est plus une hypothèse.
- [01-03] Les fixtures sont des modules `.js` (`export default {...}`) et jamais `.json` : `.json` n'est pas dans la liste blanche de routage du serveur (200 + image JPEG).
- [01-03] Le bot d'autoplay tourne sur `marvel-lcg-src/.game` (dossier compilé par `launcher_fast.py`), seul dossier importable et strictement identique au code servi ; `test_autoplay.py` reste intouché, `dump_get_world.py` en est une copie.
- [01-03] `public/fixtures.html` monte aujourd'hui un rendu texte ; en phase 5 le composant React prendra sa place **sans changer le contrat** (import d'une fixture → props).

### Todos en attente

Aucun.

### Blocages / points de vigilance

- ✓ **Intouchabilité étendue actée** dans PROJECT.md (Constraints + Key Decisions) : `public/js/marvel/` jamais lu ni modifié, le nouveau code est une fonction pure de `get_world`.
- **Le serveur doit tourner sous `launcher_fast.py`** pour tous les plans suivants : les fixtures (01-03) et la bascule `?ui=old` (01-04) ajoutent des fichiers dans `public/`, invisibles sous `launcher.py`. Relance = coupure de la partie en cours. Piège connu : le port 2345 reste en TIME_WAIT quelques dizaines de secondes après un arrêt, attendre avant de relancer.
- **Montée de version de Playwright = re-validation des 18 références** (le Chromium embarqué change le rendu). Version épinglée `1.62.0` sans `^`.
- **Référence de l'écran Replays quasi vide** tant qu'aucun replay n'est enregistré : à régénérer le jour où il y en aura.
- **Séquence CSS obligatoire** en Phase 2 : captures de référence → purge des `!important` de `wizard.css` (67 sur 165) → `@layer` → tokens. Inverser aggrave la cascade.
- **Routage serveur par extension** en liste blanche stricte : tout asset de build hors liste échoue silencieusement (200 OK, contenu vide).
- **Recherche approfondie à prévoir** avant planification : Phase 4 (contrat `/new?data=` et campaign logs des 4 formats), Phase 6 (table de zones par palier, géométrie 4 joueurs mobile), Phase 7 (vocabulaire `select_rule` / `ability_type` / `event_name`).
- **Livraison** : chaque étape livrée = re-zip vers `Fusion/` + relance serveur + non-régression (autoplay 0 traceback). Codebase vivant = `~/marvel-work/fusion/marvel-lcg-src`.
- **Les fixtures et `fixtures.html` vivent hors du dépôt** (`~/marvel-work/fusion/marvel-lcg-src/public/`), donc hors sauvegarde git : un re-zip vers `Fusion/` les emporte, mais une reconstruction du codebase les perdrait. Régénération : `~/marvel-work/tools/run_dump.sh <port> <scenario> <heros>` (documenté en tête de `public/js/fixtures/index.js`).
- **Ne jamais éditer une fixture à la main** (l'en-tête de chaque fichier le rappelle) ; `index.js` est tenu à la main et doit suivre toute régénération, sinon `npm run fixtures` devient rouge — comportement voulu.
- **Node est le binaire Windows** (`node.exe` via `~/.local/bin/node`) : il ne lit pas les chemins WSL. Pour importer un fichier du jeu depuis Node, passer par `file://wsl.localhost/Ubuntu/...`.
- **Cas de jeu encore absents des fixtures** : `zone-victoire`, `deck-rencontre-vide`, `stade-3` (les 5 parties se sont soldées par une défaite). Le dumper sait les capturer ; à relancer si le plateau en a besoin.

## Continuité de session

Dernière session : 2026-07-28
Arrêté à : 01-03-PLAN.md terminé (voir .planning/phases/01-filet-de-securite/01-03-SUMMARY.md)
Fichier de reprise : aucun
Prochain plan : 01-04-PLAN.md — bascule `?ui=old` (01-02 exécuté en parallèle)
