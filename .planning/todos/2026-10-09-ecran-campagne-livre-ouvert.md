> **MISE À JOUR 23/10/2026 : FAIT, l'en-tête ci-dessous est périmé** (ancien état : « « pas encore déployé » »). Preuve : `public/js/campagne/livre-pages.js` (commit `fce9ef4f`, 09/10) ; déploiement non établi (tri : `docs/rapports/etat-du-backlog-2026-10-19.md` §3, n°8).

# Écran de campagne : livre ouvert au lieu des pages empilées (décidé et codé le 09/10/2026, validé par l'utilisateur, pas encore déployé)

Problème : `public/js/campagne/app.js` empile les planches (colonne récit) et les pages de règles du scénario puis de la
campagne (colonne mission) ; le bouton « Lancer le scénario » est sous toutes ces pages, il faut défiler.

Décisions de l'utilisateur (questions une à une) :
- **Livre ouvert, deux pages côte à côte**, flèches pour tourner la double page (clavier aussi).
- **Contenu selon l'étape** :
  - début de campagne : couverture, intro et règles de la campagne, puis le scénario 1 ;
  - entre deux scénarios : épilogue du précédent, puis intro et règles du suivant ;
  - fin : épilogue final ;
  - un onglet « Règles de campagne » toujours disponible.
- **Bandeau sous le livre** : enjeux, mise en place, options côte à côte, bouton Lancer toujours visible sans défiler.
- **Écran étroit** (téléphone, tablette portrait) : une page à la fois, balayage du doigt ; toucher agrandit (loupe actuelle).
- **Animation** : page qui se tourne (~0,3 s), coupée si `prefers-reduced-motion`.

À garder : la loupe au clic, la variante française des pages (`fr/`, repli anglais), les écrans Marché, Enquête,
conclusion, et la vue « affaires » (pages_intro + affaire montrée, autour de la ligne 1010 d'app.js).

## Fait (09/10/2026)
- `public/js/campagne/livre-pages.js` (pur) choisit les pages par étape ; `tools/tests-lanceur/livre-pages.test.mjs` (8 tests) vérifie aussi que
  chaque page déclarée des 11 campagnes apparaît à une étape.
- `livreOuvert()` dans `app.js` : vue linéaire, conclusion, ordre libre (Fear No Evil). Page absente (couverture d'une boîte sans livret) : retirée du livre.
- Mesuré : bouton Lancer en bas à 670 px sur 768 et 982 sur 1080, la page ne défile pas.
- `ui-check/tests/campagne-livre-ouvert.spec.ts` (5), `campagne-livret-fr`, `campagne-aoa`, `campagne-ordre-libre` adaptés et verts sur moteur d'essai.
- Échecs de la suite `campagne-*` NON liés (plateau en partie, non vérifiés contre l'ancienne version) : cartes-imposees, decks (`.campagne-bandeau`),
  ordre-libre-boucle (panneau de récompenses), ordre-libre-lancement (nom de manigance), pilote, professor-x ; et `site-en-anglais` sur `/salon.html`.
