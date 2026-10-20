# Play (mode navigateur) : plantage WebKit, cause trouvée (20/10/2026)

Branche `play-webkit-plantage`. Aucun déploiement, aucun push.

## Verdict en une phrase

Le plantage n'est PAS dans notre code : il vient du moteur WebKit de test de Playwright (build WPE, Linux, `webkit-2336`) sur cette machine. Ce build s'arrête (`abort()`) dès qu'une page affiche 5 images distinctes ou plus, quel que soit le site. Avec `WEBKIT_DISABLE_DMABUF_ATLAS=1`, le parcours complet de Play passe sous WebKit (bureau et mobile émulé, jusqu'au round 2). Cela ne dit rien sur Safari réel.

## Symptôme

Le processus `WPEWebProcess` se termine par `SIGABRT` (« Target crashed ») quelques secondes après l'ouverture de l'assistant solo (liste des héros). Message sur la sortie d'erreur du navigateur, juste avant l'arrêt :

`ERROR: Could not negotiate a suitable buffer format. Aborting ...`

Cette phrase se trouve dans `libWPEWebKit-2.0.so` (route de rendu accéléré par tampons DMA-BUF). La pile du `coredumpctl` ne montre que `abort()` appelé depuis cette bibliothèque (pas de symboles).

## Conditions de l'essai

- Reproduction n° 1 à charge basse : `uptime` 2,7 au départ, mémoire disponible 3,1 Go sur 15,9 Go, swap plein (2 Go). Plantage identique à celui du matin. La charge est montée ensuite à 30-60 à cause d'autres processus de la machine : le processus de rendu WebKit reste à 1 à 2 cœurs et 0,8 à 0,9 Go.
- Les essais suivants ont été lancés charge sous 10 quand c'était possible (attente préalable), sinon en essais courts. Le plantage est déterministe : 100 % des essais avec images, 0 % sans, quelle que soit la charge (2,7 à 60).
- Serveur local `navigateur/serveur-local.py 8791`, `dist` copié du dépôt principal. WebKit Playwright `webkit-2336`, WPE headless, GPU Intel UHD 620 (Mesa iris, `renderD128`).

## Bisection (WebKit, rendu par défaut)

| Essai | Résultat |
|---|---|
| Accueil seul, 60 s au repos (moteur Pyodide prêt) | survit |
| Assistant solo, images bloquées (toutes les requêtes de type image) | survit, capture correcte |
| Assistant solo, CSS lourd coupé (filtres, masques, clip-path, ombres, animations, transformations), images chargées | plante |
| Pages « Options » et « Mises à jour » (texte, peu d'images) | survivent |
| Éditeur de deck, bac à sable (nombreuses images de cartes) | plantent |
| Pages statiques `prepare.html`, `main.html`, `cards.html` sans moteur (pas d'images) | survivent |
| Pages de synthèse : `transform`, animation, `backdrop-filter`, `will-change`, canvas 2D, WebGL, iframe, filtre, image de 8000 px | toutes survivent |
| Page de synthèse avec seulement des `<img>` 100×142 : 1 à 4 images | survit |
| Idem, 5 images ou plus (5, 7, 64) | plante (même message) |
| Mêmes images converties : JPEG réel RGB, PNG RGB, WebP RGBA, WebP RGB, PNG servi en `image/png` | plantent toutes (donc ni le format, ni l'alpha, ni le type MIME) |
| `LIBGL_ALWAYS_SOFTWARE=1`, `WEBKIT_SKIA_GPU_PAINTING_THREADS=0` | plantent encore |
| `WEBKIT_DISABLE_COMPOSITING_MODE=1` | plante encore |
| `WEBKIT_SKIA_ENABLE_CPU_RENDERING=1` (Skia sans GPU) | survit, fiche héros correcte |
| `WEBKIT_DISABLE_DMABUF_ATLAS=1` (variable présente dans la bibliothèque) | survit (synthèse à 7 images, puis parcours complet) |

Écarté : la mémoire (la page de l'assistant solo ne compte que 498 éléments ; 64 cartes de 300×426 pèsent environ 33 Mo décodées ; le processus reste à 0,8 Go), la taille du WASM ou du `moteur.zip` (l'accueil avec moteur prêt survit 60 s), l'iframe d'isolation (le plantage se reproduit sans iframe, sans moteur, sans CSS), COOP/COEP et `SharedArrayBuffer`, le CSS lourd, le format des images.

Note : les scans du jeu sont en réalité des PNG RGBA 300×426 nommés `.jpg` (environ 250 Ko chacun) ; le serveur les annonce `image/jpeg`. Sans lien avec le plantage, mais à savoir.

## Cause

Défaut du rendu accéléré du build WPE de test : la route Skia GPU alloue un atlas d'images en tampon DMA-BUF. À partir de quelques images, l'allocation d'un nouveau tampon échoue pour tous les formats proposés (le build n'arrive pas à en « négocier » un avec ce Mesa/Intel en mode headless) et WebKit appelle `abort()`. Couper cet atlas suffit. C'est un défaut de l'environnement de test, pas de la page : n'importe quelle page de cinq images le déclenche ici.

Ce n'est pas une preuve que Safari est sain : c'est une preuve que le plantage observé ne vient pas de notre code, et que le banc WebKit Linux n'est pas représentatif de Safari (Safari sur macOS et iOS n'utilise pas cette route DMA-BUF de WPE).

## Correctif

Aucune correction côté page : il n'existe pas de repli applicable (le seuil est de 5 images simples).

Correctif du banc : `navigateur/essais/navigateurs.mjs` lance maintenant WebKit avec `WEBKIT_DISABLE_DMABUF_ATLAS=1` par défaut (`WEBKIT_DISABLE_DMABUF_ATLAS=0` pour reproduire le plantage).

## Vérification après correctif

- WebKit bureau (1440×900), parcours complet : moteur prêt en 15,6 s, assistant, plateau, tour du héros, fin de tour, phase du méchant, round 2 atteint, aucun plantage. Capture de la fiche héros correcte.
- WebKit mobile émulé (390×844) : idem, round 2 atteint, aucune erreur.
- Chromium bureau : moteur prêt en 15,0 s. Firefox bureau : moteur prêt en 61 s (charge de la machine, même ordre que Q2 du backlog). Pas de régression : le banc ne change rien hors WebKit.

## Constat annexe

Le plateau demande `/sets/<nom du set>` (par exemple `/sets/1. Core Set`) et le serveur local répond 404 (aussi sur le serveur du dépôt principal). Sans conséquence sur le parcours, mais à regarder : icônes de set manquantes dans Play ?

## Ce qui reste à vérifier sur un vrai Safari ou iPhone

1. Un Mac (Safari récent) et un iPhone : ouvrir `navigateur.html`, passer l'avertissement, lancer le moteur, l'assistant solo (plus de 60 cartes à l'écran), une partie jusqu'au round 2.
2. Mémoire réelle sur iPhone : le moteur demande environ 300 Mo (WASM Pyodide) plus les images ; surveiller une fermeture de l'onglet par le système.
3. Isolation `crossOriginIsolated` et `SharedArrayBuffer` : disponibles sous Safari 15.2 et plus avec COOP/COEP `require-corp` ; à confirmer sur appareil.
4. Exceptions WebAssembly de Pyodide 0.27 (Firefox émet un avertissement de dépréciation ; Safari non testé).

## Journaux et outils

- `coredumpctl info <pid>` (pile : `abort` dans `libWPEWebKit`), sortie d'erreur du navigateur avec `DEBUG=pw:browser`.
- Reproduction minimale : une page de 5 balises `<img>` (images distinctes de quelques centaines de pixels) ouverte avec le WebKit de Playwright sans la variable.
