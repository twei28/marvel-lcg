# État du projet

## Référence projet

Voir : .planning/PROJECT.md (mis à jour le 2026-07-28)

**Valeur centrale :** Une interface digne du contenu : belle, claire et fluide sur PC, tablette et mobile, sans jamais toucher aux règles du moteur.
**Focus actuel :** Phase 1 — Filet de sécurité et boucle de dev (bloquante)

## Position actuelle

Phase : 1 sur 7 (Filet de sécurité et boucle de dev)
Plan : 01-01 à 01-04 terminés (4 sur 6 dans la phase courante)
Statut : En cours
Dernière activité : 2026-07-28 — 01-04-PLAN.md terminé et validé au checkpoint (bascule vers l'ancienne version, mémorisée, partie jouable depuis l'ancien écran)

Progression phase 1 : [███████░░░] 67% (4/6 plans)
Progression projet : [█░░░░░░░░░] ~10% (plans des phases 2 à 7 non encore découpés)

## Métriques

**Vélocité :**
- Plans terminés : 4
- Durée moyenne : 26 min
- Temps d'exécution total : 104 min

**Par phase :**

| Phase | Plans | Total | Moy./plan |
|-------|-------|-------|-----------|
| 1 — Filet de sécurité | 4/6 | 104 min | 26 min |

**Tendance récente :** 01-01 en 12 min (3 tâches, 3 déviations), 01-03 en 14 min (3 tâches, 6 déviations), 01-02 en 37 min (3 tâches dont 1 checkpoint validé, 6 déviations), 01-04 en 41 min (3 tâches dont 1 checkpoint validé sans réserve, 4 déviations). Les plans à checkpoint coûtent ~10 min d'attente : c'est le prix de la validation sur pièces.

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
- [01-02] **`npm run captures:valider` est le seul chemin autorisé vers `references/`** : aucun plan futur ne doit appeler `--update-snapshots` directement ni ajouter un drapeau de contournement (`--yes`, `--force`). Le contrôle : `grep -rn "update-snapshots" ui-check/` ne doit remonter que `valider.mjs`.
- [01-02] La validation visuelle passe par une page HTML maison (`comparaison/index.html`), pas par le rapport natif de Playwright : celui-ci n'affiche que les échecs, en anglais. La page montre **tous** les écrans, y compris les inchangés.
- [01-02] Mode démonstration `UI_CHECK_DEMO` = inversion de luminosité à teintes conservées, et non un `hue-rotate` : mesuré, un `hue-rotate` ne dépasse pas le seuil de tolérance sur les écrans sombres (4 à 7 écrans détectés sur 18 au lieu de 18).
- [01-02] Entrée fermée sans réponse = refus. Dans le doute, on ne touche pas aux références.
- [01-04] **La bascule vers l'ancienne version est 100 % côté client** (mesuré : le serveur ignore les query strings sur les `.html`). Préférence dans `localStorage` clé `ui` (`'old'`/`'new'`), jamais un cookie (le serveur pose déjà `session_token` et `app_version`) et jamais l'adresse seule : `launcher.js` fait `location.href = "/?hot_seat"` au lancement d'une partie, ce qui efface toute query string.
- [01-04] **Recette de câblage d'une page migrée** : aiguillage inline en TOUT PREMIER dans le `<head>` de la nouvelle page (un script externe se télécharge, la nouvelle UI clignoterait), plus une balise `ui-switch.js` en fin de `<body>` des deux versions. Rien d'autre.
- [01-04] Bandeau et lien de bascule **en tête du flux du document**, jamais en flottant : mesuré dans les 3 gabarits, toute position flottante recouvre un bouton (étapes 5 et 6 de l'assistant en haut, barre de boutons fixe en bas).
- [01-04] Les tests de mécanique (navigation, contrat) tournent sur le **seul gabarit `pc`** (`--project=pc`) ; l'apparence est le métier de `npm run captures`.

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
- **Sans préférence, une page migrée doit rester identique au pixel près.** Toute modification future de `ui-switch.js` se termine par un `npm run captures` vert sur les écrans anciens, sinon on fait bouger des références pour rien.
- **Quand la nouvelle version reprendra le nom de l'ancienne** (`marvel.html`, phase 5) : déposer d'abord une copie VERBATIM de l'ancienne page dans `public/legacy/<page>.html`, ne plus jamais la retoucher, et faire pointer `data-ancienne` dessus. Convention écrite en tête de `ui-switch.js`.
- **`public/scene.html.bak-avant-ui` traîne dans le codebase** (sauvegarde antérieure à la surcouche wizard). Intouché, mais à écarter avant le re-zip du plan 01-06.
- **`node --check` ne lit pas un chemin WSL** (Node est le binaire Windows) : utiliser la forme `//wsl.localhost/Ubuntu/home/arnau/...` pour tout contrôle statique sur un fichier du jeu.
- **`ui-switch.js`, `prepare.html` et `scene.html` vivent hors du dépôt git**, comme les fixtures : le re-zip vers `Fusion/` est leur seule sauvegarde. `ui-switch.js` étant la sortie de secours elle-même, sa perte serait coûteuse.
- **Les fixtures et `fixtures.html` vivent hors du dépôt** (`~/marvel-work/fusion/marvel-lcg-src/public/`), donc hors sauvegarde git : un re-zip vers `Fusion/` les emporte, mais une reconstruction du codebase les perdrait. Régénération : `~/marvel-work/tools/run_dump.sh <port> <scenario> <heros>` (documenté en tête de `public/js/fixtures/index.js`).
- **Ne jamais éditer une fixture à la main** (l'en-tête de chaque fichier le rappelle) ; `index.js` est tenu à la main et doit suivre toute régénération, sinon `npm run fixtures` devient rouge — comportement voulu.
- **Node est le binaire Windows** (`node.exe` via `~/.local/bin/node`) : il ne lit pas les chemins WSL. Pour importer un fichier du jeu depuis Node, passer par `file://wsl.localhost/Ubuntu/...`.
- **npm exécute ses scripts via `cmd.exe`** (conséquence du point précédent : `process.platform === 'win32'`). Donc : `;` et `&&` POSIX ne fonctionnent pas dans `package.json` (tout script npm doit rester **une commande unique**) ; une variable d'environnement passée en préfixe depuis WSL n'atteint pas le processus (il faut `WSLENV=NOM`) ; une entrée redirigée (`printf ... | npm run ...`) n'est pas transmise au script (appeler `node scripts/xxx.mjs` directement dans les tests).
- **Titres d'écrans de `ecrans.ts` sans accents** : ils servent aussi de titres de tests Playwright, donc de noms de dossiers dans `test-results/`. À accentuer en une ligne le jour où `ecrans.ts` sera rouvert (cosmétique, la page de comparaison est accentuée partout ailleurs).
- **Cas de jeu encore absents des fixtures** : `zone-victoire`, `deck-rencontre-vide`, `stade-3` (les 5 parties se sont soldées par une défaite). Le dumper sait les capturer ; à relancer si le plateau en a besoin.

## Continuité de session

Dernière session : 2026-07-28
Arrêté à : 01-04-PLAN.md terminé et validé au checkpoint sans réserve (voir .planning/phases/01-filet-de-securite/01-04-SUMMARY.md) — va-et-vient prouvé, partie jouée depuis l'ancienne version
Fichier de reprise : aucun
Prochain plan : 01-05-PLAN.md — contrat `/new?data=` gelé et arrivée au plateau vérifiée automatiquement (script `lancement` déjà déclaré dans `ui-check/package.json`, reste à écrire `tests/lancement-partie.spec.ts`)
