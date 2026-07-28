# État du projet

## Référence projet

Voir : .planning/PROJECT.md (mis à jour le 2026-07-28)

**Valeur centrale :** Une interface digne du contenu : belle, claire et fluide sur PC, tablette et mobile, sans jamais toucher aux règles du moteur.
**Focus actuel :** Phase 2 en cours (fondations : stack React/TS/Vite servie par le serveur existant + design system tokenisé)

## Position actuelle

Phase : 2 sur 7 (Fondations — stack et design system tokenisé) — **en cours**
Plan : 02-01, 02-02, 02-03 et 02-04 terminés (10 plans dans la phase)
Statut : En cours — la chaîne de build arrive jusqu'au jeu **et la cascade CSS de l'ancienne préparation est saine** : `wizard.css` est passé de 105 `!important` à 2 exceptions documentées, sans qu'un seul style calculé ne bouge
Dernière activité : 2026-07-28 — 02-04-PLAN.md terminé (styles en ligne de `scene.html` extraits vers `css/menu/scene-inline.css` chargé AVANT `wizard.css`, purge des 105 `!important`, 6 régressions mesurées et corrigées par ordre de source puis spécificité ; 27 références vertes, 0 différence de style calculé sur les 4 panneaux et 10 états de survol/sélection)

Progression phase 1 : [██████████] 100% (6/6 plans)
Progression phase 2 : [████░░░░░░] 4/10 plans (02-01, 02-02, 02-03, 02-04)
Progression projet : [██░░░░░░░░] ~20% (1 phase sur 7 terminée ; plans des phases 3 à 7 non encore découpés)

## Métriques

**Vélocité :**
- Plans terminés : 10
- Durée moyenne : 25 min
- Temps d'exécution total : 305 min

**Par phase :**

| Phase | Plans | Total | Moy./plan |
|-------|-------|-------|-----------|
| 1 — Filet de sécurité | 6/6 | 142 min | 24 min |
| 2 — Fondations | 4/10 | 163 min | 41 min |

**Tendance récente :** 01-01 en 12 min (3 tâches, 3 déviations), 01-03 en 14 min (3 tâches, 6 déviations), 01-05 en 14 min (2 tâches, 2 déviations), 01-02 en 37 min (3 tâches dont 1 checkpoint validé, 6 déviations), 01-04 en 41 min (3 tâches dont 1 checkpoint validé sans réserve, 4 déviations). Les plans à checkpoint coûtent ~10 min d'attente : c'est le prix de la validation sur pièces. Les plans sans checkpoint tiennent en 12 à 14 min.

**01-06 en 24 min** (2 tâches dont 1 checkpoint validé, 3 déviations) : 8 min d'exécution, ~14 min d'attente au checkpoint. **Bilan de la phase : 6 plans, 142 min, 24 déviations toutes auto-corrigées, 3 checkpoints tous validés sans réserve.** Les déviations sont massivement des pièges d'environnement (WSL/Node Windows, ports en TIME_WAIT, outils absents), pas des erreurs de conception — c'est le coût d'entrée dans ce codebase, il devrait baisser.

**02-04 en 2h20** (2 tâches + 1 checkpoint, 5 déviations) : ~57 min d'exécution, ~80 min d'attente au checkpoint. Le plan le plus long jusqu'ici, pour deux raisons dont aucune n'est le CSS lui-même : le port 2345 était occupé par une partie multi servie depuis un codebase périmé (déblocage complet à construire), et la purge exigeait une preuve que les captures ne savent pas donner (mesure des styles calculés). Le coût d'entrée n'a donc pas encore baissé : il s'est déplacé du harnais vers l'environnement d'exécution.

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
- [01-05] **Le contrat `/new?data=` est gelé dans `ui-check/contrat-nouvelle-partie.json`** : 8 clés typées (`campaign_json`, `campaign_log`, `challenges`, `encounter_set_names`, `hero_json`, `rules`, `seed`, `timeout`), jamais les valeurs. C'est la seule documentation écrite de ce contrat.
- [01-05] Le test de lancement pilote **`prepare.html` (la nouvelle préparation)**, pas `scene.html` : les deux envoient le même descripteur, mais seul le nouvel écran sera refait en phase 4 — un test sur l'ancien resterait vert pendant que la refonte casse le lancement.
- [01-05] **Prouvé par mesure** : `NewGame` remet le monde à zéro (`render_id = 0`) et le moteur répond **après**. Sonder `/get_world` sans attendre la réponse de `/new` lit donc l'état de la partie précédente — piège corrigé, à ne pas réintroduire.
- [01-05] Parcours de test figé sur la boîte de base (Solo / Spider-Man / Rhino / Standard) et sélecteurs par **rôle et libellé** : ce contenu ne disparaîtra jamais, et les libellés survivront mieux que le DOM à la refonte de la phase 4.
- [02-02] **`ui-app/` est le projet de la nouvelle UI** : React 19.2.8 + TypeScript 6.0.3 + Vite 8.1.5, dans le dépôt Desktop à côté de `ui-check/` (chemin Windows natif obligatoire, Node est le binaire Windows). Il n'entre jamais dans le livrable ; `dist/` et `node_modules/` sont ignorés par git.
- [02-02] **TypeScript reste en 6.0.3, jamais 7.x** : la 7 est `latest` sur npm mais expédiée sans API compilateur publique. Ne pas « mettre à jour » sans vérifier que l'API est revenue.
- [02-02] **`build.rolldownOptions` et non `rollupOptions`** (renommé en Vite 8) : vérifié, aucun avertissement de dépréciation au build. Tout exemple multi-pages antérieur à mars 2026 est à corriger.
- [02-02] **`assetsInlineLimit: () => true`** : tout asset importé est inliné, donc le build ne peut produire que du `.html`, du `.js` et du `.css`. C'est la traduction en configuration de la liste blanche du serveur.
- [02-02] **`node outils/verifier-sortie.mjs` est le garde-fou d'extensions** : liste blanche `.html`/`.js`/`.css`, `exit 1` sur intrus, sur dossier absent et sur dossier vide. Testé par un vrai négatif (un `.png` déposé dans `dist/`). À lancer après chaque build, avant toute recopie vers le jeu.
- [02-02] **`vite-plugin-checker` fait réellement échouer le build sur erreur de type** (vérifié en injectant une erreur volontaire, exit 2 + `TS2322`). Le repli prévu (script `typecheck` enchaîné dans `deployer.sh`) n'est pas nécessaire.
- [02-02] **`ui-app/styles/tokens.css` est la source unique des tokens**, avec la déclaration `@layer socle, legacy, base, composants, utilitaires;` en tête. Deux destinations : le bundle Vite et une copie vers `public/css/tokens.css`. Ne jamais éditer la copie.
- [02-02] **Pas d'aiguillage `ui-switch.js` sur `vitrine.html`** : cette page n'a pas d'ancienne version, il n'y a rien vers quoi revenir. La recette de bascule redevient obligatoire en phase 3.
- [02-01] **Un panneau masqué du wizard s'ouvre par `window.wizardShow(i)`, jamais par un clic sur `.w-step`** : le gestionnaire de clic de `scene.html` est gardé par `canPass[cur]()` et ne fait rien tant que l'étape courante n'est pas valide.
- [02-01] **Un écran de `ecrans.ts` peut décrire une interaction** (`etape`, `depliages`) et plus seulement une URL. Il doit alors déclarer des `preuves` : sans elles, une photo d'en-tête vide passerait pour une référence valide.
- [02-01] **Ce que la page replie par défaut échappe à la surveillance.** Mesuré : `#modular-sets` porte `hide-not-click` au chargement, la première photo de l'étape 2 ne montrait aucun set modulaire alors que l'essentiel des `!important` de ce panneau les vise. Tout contenu replié doit être déplié avant la photo.
- [02-01] **Un bouton se vise par son `onclick`, pas par son libellé** (`button[onclick*="hide-not-click"]`) : le libellé peut être traduit, le comportement non.
- [02-01] **Une nouvelle référence se contrôle sur son CONTENU** (lecture de l'image), jamais sur sa seule existence. Une image montrant le mauvais panneau serait figée sans bruit.
- [02-03] **`bash ui-app/deployer.sh` est le seul chemin vers le jeu** : build → garde-fou d'extensions → `rsync -a --delete` vers `public/app/` → copie de `tokens.css` → recalcul des empreintes. Jamais de recopie de `dist/` à la main, jamais d'édition de `public/css/tokens.css` (c'est une copie).
- [02-03] **Cache-busting par empreinte de contenu** (8 premiers caractères du `sha256`), recalculée à chaque déploiement. Les 5 `?v=N` tenus à la main sont morts ; critère 5 de la phase démontré en 4 temps (modification → empreinte changée → retour → empreinte revenue).
- [02-03] **Ordre de réécriture du plus profond vers le plus superficiel** : les imports de `app.js` avant l'empreinte de `app.js` dans `prepare.html`, sinon deux déploiements sont nécessaires pour converger.
- [02-03] **Aucun fichier du jeu n'est réécrit si son contenu ne change pas** (garde `grep` + comparaison, écriture par redirection et jamais par `mv` : inode, droits et bit d'exécution conservés). Ces fichiers vivent hors du dépôt git, les remuer pour rien est un risque gratuit.
- [02-03] **Le franchissement Windows → WSL se fait par `rsync` en bash, jamais par Node** (Node est le binaire Windows). Corollaire mesuré : `node /mnt/c/...` échoue même pour son propre script d'entrée, il faut un chemin relatif.
- [02-03] **Le serveur n'a pas besoin d'être relancé pour un déploiement** : `public/` est vu par `.game/public` via un lien symbolique, les fichiers déposés sont servis à chaud. C'est ce qui permet de déployer sans couper une partie.
- [02-04] **Un `!important` se remplace par l'ordre de source d'abord, par la spécificité ensuite, jamais par un autre `!important`.** Les 105 de `wizard.css` visaient presque tous des règles écrites plus bas dans le document (les blocs `<style>` de `scene.html`) ou plus haut dans son propre fichier. Déplacer, ou calquer le sélecteur concurrent d'un cran plus spécifique, suffit.
- [02-04] **Seule exception légitime : un style posé en ligne par JavaScript.** Les 2 `!important` restants visent les vignettes de la galerie de héros, à qui le script de `scene.html` pose un attribut `style` (`border-radius:5px`, puis `borderColor='#c00'` au survol). Aucune feuille ne bat un style en ligne. Les deux sont commentés dans le fichier, avec la condition de leur disparition.
- [02-04] **`deployer.sh` compte les `!important` de `wizard.css` hors commentaires** et refuse le déploiement si le nombre diffère de `IMPORTANTS_ATTENDUS` (2 aujourd'hui). Éprouvé par un vrai négatif. Le modifier est un geste conscient, dans le même commit.
- [02-04] **Les captures ne prouvent pas que la cascade est intacte.** Elles ne montrent que le chargement. 3 des 6 régressions de la purge (contour rouge des cartes sélectionnées, ombre blanche au survol, grisage des paquets indisponibles) n'apparaissaient dans aucune des 27 références. La preuve se fait sur les **styles calculés** : `node ui-check/scripts/releve-styles.mjs relever|comparer`.
- [02-04] **`UI_CHECK_BASE` déplace l'adresse du jeu pour le harnais**, défaut inchangé `http://127.0.0.1:2345`. Depuis WSL : `export UI_CHECK_BASE=... WSLENV=UI_CHECK_BASE`.
- [02-04] **Tout correctif sur un fichier du jeu doit être rejouable par script tant que des mesures avant/après sont en cours** : la restauration de l'état « avant » écrase les éditions manuelles, et ces fichiers vivent hors du dépôt git.

**Les quatre acquis de structure de la phase 1**, à connaître avant toute phase suivante :

- **`ui-check/` est le harnais**, il vit dans le dépôt Desktop et n'entre jamais dans le livrable (contrôlé au re-zip : 0 entrée `ui-check` dans le zip).
- **`launcher_fast.py` est le serveur de développement** (port 2345) : lui seul sert à chaud les fichiers ajoutés dans `public/`. Toute relance coupe la partie en cours et exige d'attendre la libération effective du port.
- **Les fixtures vivent dans `public/js/fixtures/`** (34 états + `index.js`), au format module `.js`, et sont rejouées par `public/fixtures.html` sans qu'aucune partie ne tourne.
- **La bascule vers l'ancienne version est mémorisée dans `localStorage` (clé `ui`)**, jamais dans l'adresse ni dans un cookie : c'est ce qui la fait survivre au lancement d'une partie.
- [01-06] **Le zip de `Fusion/` n'a pas de préfixe de dossier** : ses entrées sont à la racine de l'archive (`src/`, `public/`, `launcher.py`…). Exclusions du livrable : `.game/`, `__pycache__/`, `originals_pyc/`. Tout re-zip doit calquer cette structure, sinon le livrable change de forme sans prévenir.
- [01-06] **Un livrable se contrôle comme un test** : diff des listes ancien/nouveau zip, puis assertions nommées (les ajouts attendus présents, le harnais et les caches absents). Le zip précédent est sauvegardé en `.bak-avant-<étape>` avant remplacement.

### Todos en attente

Aucun.

### Blocages / points de vigilance

- ✓ **Intouchabilité étendue actée** dans PROJECT.md (Constraints + Key Decisions) : `public/js/marvel/` jamais lu ni modifié, le nouveau code est une fonction pure de `get_world`.
- **Le serveur doit tourner sous `launcher_fast.py`** pour tous les plans suivants : les fixtures (01-03) et la bascule `?ui=old` (01-04) ajoutent des fichiers dans `public/`, invisibles sous `launcher.py`. Relance = coupure de la partie en cours. Piège connu : le port 2345 reste en TIME_WAIT quelques dizaines de secondes après un arrêt, attendre avant de relancer.
- **Montée de version de Playwright = re-validation des 18 références** (le Chromium embarqué change le rendu). Version épinglée `1.62.0` sans `^`.
- **Référence de l'écran Replays quasi vide** tant qu'aucun replay n'est enregistré : à régénérer le jour où il y en aura.
- **Séquence CSS obligatoire** en Phase 2 : captures de référence → purge des `!important` de `wizard.css` → `@layer` → tokens. Inverser aggrave la cascade. ✓ **Étape zéro faite (02-01)** ; ✓ **purge faite (02-04)** : 105 → 2 exceptions documentées. `@layer` (02-05) peut être posé sans être renversé.
- ⚠️ **`Fusion/marvel-lcg-src` est un codebase de DISTRIBUTION périmé**, et c'est lui que sert `JOUER-EN-MULTI.bat` sur le port 2345, avec mot de passe (`launch.online.json`) et tunnel Cloudflare public. Le codebase de TRAVAIL, seul alimenté par `deployer.sh`, est `~/marvel-work/fusion/marvel-lcg-src`. Ne jamais couper ce serveur ni écrire dans `Fusion/` : une partie peut être en cours avec d'autres joueurs.
- ⚠️ **Un `200 OK` sur `/main.html` ne prouve pas que le jeu est servi** : la page d'authentification et la page d'avertissement de cache répondent toutes deux 200. Contrôler le CONTENU (titre contenant `Marvel`), comme le fait `global-setup.ts`.
- **Serveur de développement local sur le port 2346**, à laisser allumé pour les plans 02-05 à 02-09 (il ne survit pas à un redémarrage du poste) :
  `~/marvel-work/python/bin/python3.10 "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/ui-check/scripts/serveur-dev.py" --port 2346`
  Puis, pour le harnais : `export UI_CHECK_BASE=http://127.0.0.1:2346 WSLENV=UI_CHECK_BASE`.
- **`RELEASE=1` doit être posé avant tout import du moteur** dans un lanceur maison : sans elle, le moteur démarre en mode debug (`0.5.9.200d`) et importe `editor.editor`, absent de la distribution. Les références ont été prises en mode release (`0.5.9.200r`).
- **`ui-check/test-results/` est vidé à chaque exécution de Playwright** : n'y déposer que du jetable. Les outils vivent dans `ui-check/scripts/`.
- **`scene-inline.css` est un fichier de transition**, sans intention de design : c'est l'ancien CSS en ligne de `scene.html`, rangé. Il partira avec `scene.html` en phase 5, en même temps que les 3 écrans `preparation-rencontre|heros|lancement` du harnais.
- ⚠ **DETTE : la validation visuelle humaine du 02-04 n'a pas eu lieu et reste DUE.** Le checkpoint `gate="blocking"` du plan a été franchi sans réponse de l'utilisateur, sur les seules mesures automatiques. À faire sur `http://127.0.0.1:2346/scene.html` (4 étapes du wizard + lancement d'une partie) **avant de clore 02-05**, qui pose `@layer` par-dessus. État de départ conservé dans `~/marvel-work/scratch/02-04/`.
- **Le filet dépend maintenant de deux détails internes de `scene.html`** : `window.wizardShow` doit rester exposé, et le bouton de dépliage des sets modulaires doit garder un `onclick` contenant `hide-not-click`. Les deux ont un message d'erreur en français qui le dit. Quand `scene.html` sera remplacé (phase 5), les 3 écrans `preparation-rencontre|heros|lancement` seront à revoir ou à retirer.
- **Autres contenus repliés de `scene.html` non couverts** : les `<details>` `#rules` et `#challenge` de l'étape 4 sont fermés par défaut. Si la purge touche leurs styles internes, les ajouter aux `depliages`. Les sets modulaires sont dans un conteneur à défilement (`max-height:44vh`) : la photo n'en montre que la première partie.
- **Routage serveur par extension** en liste blanche stricte : tout asset de build hors liste échoue silencieusement (200 OK, contenu vide).
- **Recherche approfondie à prévoir** avant planification : Phase 4 (contrat `/new?data=` et campaign logs des 4 formats), Phase 6 (table de zones par palier, géométrie 4 joueurs mobile), Phase 7 (vocabulaire `select_rule` / `ability_type` / `event_name`).
- **Livraison** : chaque étape livrée = re-zip vers `Fusion/` + relance serveur + non-régression (autoplay 0 traceback). Codebase vivant = `~/marvel-work/fusion/marvel-lcg-src`. Rituel exécuté le 2026-07-28 pour la phase 1 ; sauvegarde du zip précédent en `marvel-lcg-src-fusion.zip.bak-avant-phase1`.
- **`zip` et `unzip` ne sont pas installés** dans cet environnement : le re-zip et son inspection passent par le module `zipfile` de Python 3.10 (`~/marvel-work/python/bin/python3.10`). Ne pas partir du principe que les commandes du plan existent.
- **`test_autoplay.py` a besoin d'un `winsound`** que le dossier compilé `.game` n'embarque pas (le lanceur l'injecte en mémoire). Le fournir par `PYTHONPATH` vers un dossier contenant une copie de `~/marvel-work/boot/winsound.py`, jamais en écrivant dans le dossier du jeu. Le dossier de jeu à passer au bot est `.game`, pas `marvel-lcg-src`.
- **Sans préférence, une page migrée doit rester identique au pixel près.** Toute modification future de `ui-switch.js` se termine par un `npm run captures` vert sur les écrans anciens, sinon on fait bouger des références pour rien.
- **Quand la nouvelle version reprendra le nom de l'ancienne** (`marvel.html`, phase 5) : déposer d'abord une copie VERBATIM de l'ancienne page dans `public/legacy/<page>.html`, ne plus jamais la retoucher, et faire pointer `data-ancienne` dessus. Convention écrite en tête de `ui-switch.js`.
- ✓ **`public/scene.html.bak-avant-ui` écarté** (01-06) : déplacé dans `~/marvel-work/scratch/ecartes-01-06/`, absent du nouveau zip, et toujours présent dans `marvel-lcg-src-fusion.zip.bak-avant-phase1` si besoin.
- **`node --check` ne lit pas un chemin WSL** (Node est le binaire Windows) : utiliser la forme `//wsl.localhost/Ubuntu/home/arnau/...` pour tout contrôle statique sur un fichier du jeu.
- **`ui-switch.js`, `prepare.html` et `scene.html` vivent hors du dépôt git**, comme les fixtures : le re-zip vers `Fusion/` est leur seule sauvegarde. `ui-switch.js` étant la sortie de secours elle-même, sa perte serait coûteuse.
- **Les fixtures et `fixtures.html` vivent hors du dépôt** (`~/marvel-work/fusion/marvel-lcg-src/public/`), donc hors sauvegarde git : un re-zip vers `Fusion/` les emporte, mais une reconstruction du codebase les perdrait. Régénération : `~/marvel-work/tools/run_dump.sh <port> <scenario> <heros>` (documenté en tête de `public/js/fixtures/index.js`).
- **Ne jamais éditer une fixture à la main** (l'en-tête de chaque fichier le rappelle) ; `index.js` est tenu à la main et doit suivre toute régénération, sinon `npm run fixtures` devient rouge — comportement voulu.
- **Node est le binaire Windows** (`node.exe` via `~/.local/bin/node`) : il ne lit pas les chemins WSL. Pour importer un fichier du jeu depuis Node, passer par `file://wsl.localhost/Ubuntu/...`.
- **npm exécute ses scripts via `cmd.exe`** (conséquence du point précédent : `process.platform === 'win32'`). Donc : `;` et `&&` POSIX ne fonctionnent pas dans `package.json` (tout script npm doit rester **une commande unique**) ; une variable d'environnement passée en préfixe depuis WSL n'atteint pas le processus (il faut `WSLENV=NOM`) ; une entrée redirigée (`printf ... | npm run ...`) n'est pas transmise au script (appeler `node scripts/xxx.mjs` directement dans les tests).
- **Titres d'écrans de `ecrans.ts` sans accents** : ils servent aussi de titres de tests Playwright, donc de noms de dossiers dans `test-results/`. À accentuer en une ligne le jour où `ecrans.ts` sera rouvert (cosmétique, la page de comparaison est accentuée partout ailleurs).
- **Cas de jeu encore absents des fixtures** : `zone-victoire`, `deck-rencontre-vide`, `stade-3` (les 5 parties se sont soldées par une défaite). Le dumper sait les capturer ; à relancer si le plateau en a besoin.
- **Signal UX relevé au checkpoint 01-06** : `fixtures.html` a été pris pour un écran de jeu (« ça sert à lancer une partie ? »). La page ne dit pas ce qu'elle est. Quand elle accueillera le composant React du plateau (phase 5), lui donner un titre et une phrase explicites : visionneuse d'états enregistrés, aucune partie en cours.
- **`npm run lancement` détruit la partie en cours** (il appelle `/new`). Il reste une commande à part, jamais enchaînée à `npm run captures` qui est en lecture seule. L'avertissement s'affiche en français au démarrage du test.
- **Le contrat gelé ne se modifie jamais pour faire passer un test rouge.** Un rouge = la préparation a changé ce qu'elle envoie au moteur : soit accident à corriger, soit changement voulu et mesuré, et alors le golden se met à jour **dans le même commit**. La règle est écrite en tête du fichier.
- **`npm run lancement` est le critère d'acceptation de la phase 4.** Il pilote `prepare.html` par libellés (« Continuer », « Lancer la partie », « Rhino », « Spider-Man ») : si la refonte change ces libellés, les mettre à jour dans le test est un geste conscient, pas une régression.
- **Le contrat couvre les clés et les types, pas la sémantique** (`campaign_log` de campagne, `challenges` non vide). La recherche approfondie prévue pour la phase 4 (contrat `/new?data=` et campaign logs des 4 formats) reste nécessaire.
- **`ui-app/dist/` est ignoré par git** : la sortie de build n'est jamais versionnée. Tout déploiement enchaîne build → garde-fou → recopie, jamais une recopie d'un `dist/` supposé présent.
- **Le garde-fou affiche des chemins au séparateur Windows** (`dist\assets\faux.png`) puisque Node est le binaire Windows. Ne pas les confondre avec des chemins WSL dans un message d'erreur.
- **`vitrine.html` n'est pas encore dans `ui-check/ecrans.ts`** : à ajouter avec le marqueur `#vitrine` quand la page sera servie, pour bénéficier du garde-fou anti `clean_cache.html` et des captures.
- **La vitrine est un squelette** (titre, une phrase, la version de React) : palette, typo, pastilles d'aspect et bascule de thème sont le périmètre du plan 02-09, pas un manque du 02-02.
- **Toute nouvelle référence `?v=` doit être déclarée dans `deployer.sh`**, sinon elle reste tenue à la main et se désynchronise — exactement le bug fermé par le 02-03. Une ligne `remplacer` par couple (page, fichier référencé), en respectant l'ordre du plus profond vers le plus superficiel.
- **`public/app/` est nouveau dans l'arborescence du jeu** : le prochain re-zip vers `Fusion/` doit l'emporter (c'est du livrable), au contraire de `ui-app/` et `ui-check/` qui restent dehors. À vérifier au rituel de livraison du 02-10.
- **`public/css/tokens.css` est déjà servie en 200 `text/css`** et les lignes qui recalculeront son empreinte sont déjà dans `deployer.sh` : le plan 02-05 n'a plus qu'à ajouter la balise `<link>`.

## Continuité de session

Dernière session : 2026-07-28
Arrêté à : **02-01 à 02-04 terminés** — la chaîne de build arrive jusqu'au jeu et la cascade de l'ancienne préparation est assainie. `wizard.css` est passé de 105 `!important` à 2 exceptions commentées (styles posés en ligne par le JavaScript de `scene.html`) ; les 361 lignes de CSS jadis en ligne vivent dans `css/menu/scene-inline.css`, chargé avant `wizard.css`. 27 références vertes, 0 différence de style calculé sur les 4 panneaux et sur 10 états de survol et de sélection.
Fichier de reprise : aucun
Prochaine étape : plan 02-05 (pose des `@layer`). **Avant de commencer** : vérifier que le serveur de dev tourne sur 2346 (commande dans les points de vigilance) et exporter `UI_CHECK_BASE` + `WSLENV`. Méthode de preuve désormais disponible et attendue : `node ui-check/scripts/releve-styles.mjs relever` avant, puis après, puis `comparer` — la sortie doit dire « Aucun style calculé n'a changé ». Rappels : séquence CSS obligatoire (✓ captures, ✓ purge, → `@layer`, → tokens), routage serveur en liste blanche stricte par extension, tout passage vers le jeu par `deployer.sh`.
