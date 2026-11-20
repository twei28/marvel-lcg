# Textes visibles par le joueur qui n'existent que dans une langue (balayage du 26/10/2026)

Demande de l'utilisateur : « certains textes ne sont qu'en français, comme le message “expérimental” au lancement de play.narwhalchampions.com sur téléphone : ça devrait être dans les deux langues. »

## 1. Le message « expérimental » de Play : cause et correctif (FAIT)

**Où.** `navigateur/src/navigateur.html`, écran de lancement de Play sur téléphone (« Sur téléphone, ce mode est expérimental / On a phone, this mode is experimental »).

**Cause.** Le texte anglais existait déjà. La langue était lue dans `localStorage["marvel-langue"]` seulement, et **`play.<domaine>` est une autre origine que le site** : le choix fait sur le site n'y existe pas. Un joueur anglophone, ou qui avait choisi l'anglais sur le site, tombait donc sur le français. Reproduit avant correctif (Chromium, 412×915, navigateur en `en-US`, aucun choix mémorisé : écran en français).

**Correctif.** Une fonction `langueDePlay()` (identique dans `navigateur.html` et dans `shim.js`, qui n'ont aucun module commun) résout la langue dans cet ordre :

1. `?langue=en|fr` dans l'adresse (puis retenu) ;
2. le choix déjà fait ici (`marvel-langue`, même clé que le jeu) ;
3. le **cookie `nc_langue`** posé par le site sur le domaine parent (`site/orchestrateur.py`, route `/langue`, `Domain=.<domaine>`, sans HttpOnly : lisible depuis Play) ;
4. la langue du navigateur (`navigator.language`, comme le site avec `Accept-Language`) ;
5. le français.

Autres textes de Play corrigés dans la même passe :

- accents rétablis dans le français visible (« téléphone », « expérimental », « mémoire », « Continuer quand même », « Préparation du moteur de jeu… », « Le moteur n'a pas pu démarrer », nouvelle version, import/export des parties) ;
- les messages de démarrage envoyés par le Worker (« Demarrage de Python… », « Chargement des bibliotheques… », « Chargement du moteur… ») s'affichent en anglais quand la langue est l'anglais (le Worker n'a pas accès à la langue : table de traduction dans la page) ;
- les erreurs d'import d'une sauvegarde (« fichier trop gros », « ce n'est pas un fichier d'export valide », « ce n'est pas un export de ce jeu ») sont traduites.

**Preuves.** `Fusion/marvel-lcg-src/tools/tests-lanceur/langue-play.test.mjs` : 27 tests (rouges avant : 21 échecs ; verts après), dont l'identité des deux blocs, le cookie, le stockage bloqué, les valeurs inconnues. Captures (Chromium 412×915, mode téléphone, serveur d'essai avec COOP/COEP) : dossier `i18n/` du scratchpad de la session :

| Cas | Avant | Après |
|---|---|---|
| navigateur `en-US`, rien de mémorisé | français | anglais |
| navigateur `fr-FR`, rien de mémorisé | français | français (accentué) |
| navigateur `en-US`, choix mémorisé `fr` | français | français |
| navigateur `fr-FR`, choix mémorisé `en` | (déjà anglais) | anglais |
| navigateur `fr-FR`, cookie du site `nc_langue=en` | français | anglais |
| `?langue=en` | français | anglais |

Rien n'a été publié : `navigateur/dist` est ignoré par git et reconstruit au déploiement.

## 2. Autres textes à une seule langue (BALAYAGE)

Méthode : analyse statique (regex sur les littéraux visibles : `textContent`, `title`, `placeholder`, `aria-label`, `alt`, texte JSX) de `Fusion/marvel-lcg-src/public/**/*.js|html` et de `ui-app/src/**/*.ts|tsx` (tests, dictionnaires, tables de noms exclus), plus lecture de `site/langue.py`. **Le jeu et le site sont déjà bien couverts** : les gates existantes (`ui-app/src/site-langue.test.ts`, `vocabulaire-*.test.ts`, la couverture de `dico-en.ts`) font leur travail ; l'analyse ne trouve aucun libellé français en dur hors `t()` dans `ui-app/src` (1 faux positif) et 14 occurrences dans `public/`, toutes sur des **pages d'outils internes**.

| # | Où | Texte | Langue manquante | Gravité | Décision |
|---|---|---|---|---|---|
| 1 | `public/js/prepare/langue.js` `langueActuelle()` et `ui-app/src/board/langue.ts` | le jeu ne lit NI le cookie `nc_langue` NI `navigator.language` : sans `marvel-langue`, il part en français. `site/langue.py` annonce que le cookie est « posé par le site ET par le jeu » : **le jeu ne le pose pas** (aucun `document.cookie` de langue dans `public/js`) | anglais (pour un joueur qui a choisi l'anglais sur le site ou dont le navigateur est en anglais) | **visible au premier lancement** d'une table `p<N>.<domaine>` (autre origine : la question de langue de la première connexion s'affiche, mais elle part en français) | **NON corrigé** : c'est un changement de comportement du jeu (langue par défaut, clé `marvel-langue-choisie`, accord wizard / plateau) qui demande des tests dans `langue.js` ET `langue.ts` et l'avis du propriétaire. Piste : `basculerLangue()` et la réponse à la question initiale écrivent aussi `nc_langue` (`Domain=.<domaine>`) ; `langueActuelle()` lit stockage > cookie > navigateur > français. |
| 2 | `public/achievements.html:22`, `public/campagne.html:19`, `public/galerie.html:34` | « Chargement… » (français en dur avant que le JS le remplace) | anglais | rare (clignotement avant le JS) | non corrigé |
| 3 | `public/prepare.html:25`, `ui-app/board.html:10`, `ui-app/vitrine.html:9` | « Loading… » (anglais en dur avant le JS) | français | rare (clignotement) | non corrigé |
| 4 | `public/palettes-heros.html`, `releve-images.html`, `sandbox.html` | infobulles et libellés en français (pipette, relevé de couleurs, recherche) | anglais | aucune : **outils internes**, non vus des joueurs | non corrigé |
| 5 | `public/credits.html` (blocs d'origine) | « Developed by Irefrixs », « Tools and Technologies », « Special Thanks »… | français | rare : texte du moteur d'origine, en anglais par nature ; la section « Créateurs de contenu fan-made » ajoutée le 26/10 est bilingue | non corrigé |
| 6 | `public/salon.html` | « Tu es prêt », « En attente du lancement… », « Héros » en dur dans le HTML, traduits par `js/salon/app.js` via `dico-en.js` (« Salon multijoueur ») | — | à vérifier dans un navigateur (non exercé : demande une table multijoueur) | non vérifié |
| 7 | textes des cartes fan-made | `textes-fr-fanmade.ts` : français seulement ; l'anglais est le texte imprimé du scan | — | voulu (le scan est la source anglaise) | rien à faire |

Hors périmètre : la narration du moteur (`data/translate_fr.json`) et les pages du **site** Python (`site/langue.py` : cookie > `Accept-Language` > français, déjà bilingues).

## 3. Ce qu'un humain doit regarder sur téléphone, après la prochaine mise en ligne de Play

- Navigateur en anglais, jamais venu : l'écran « On a phone, this mode is experimental » apparaît en anglais.
- Choisir l'anglais sur `narwhalchampions.com`, puis ouvrir `play.narwhalchampions.com` : le message est en anglais (cookie `nc_langue`).
- Choisir le français dans le jeu de Play puis revenir : le choix de Play l'emporte sur le cookie du site.
- Le jeu lui-même (écran de préparation) peut encore démarrer en français : voir le point 1 du tableau.
