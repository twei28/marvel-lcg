> **MISE À JOUR 23/10/2026 : FAIT, l'en-tête ci-dessous est périmé** (ancien état : « « pas encore déployé » »). Preuve : `public/css/affichage-sobre-pages.css` présent ; test `ui-check/tests/affichage-sobre-pages.spec.ts` ; déploiement non établi (section 4) (tri : `docs/rapports/etat-du-backlog-2026-10-19.md` §3, n°7).

# Mode sobre sur les menus (décidé et codé le 09/10/2026, validé sur captures, pas encore déployé)

Aujourd'hui (`public/css/prepare/prepare.css`, bloc AFFICHAGE SOBRE vers la ligne 2690) : le mode sobre des pages ne fait
que mettre le fond en gris uni et couper les animations. Sur le plateau il va bien plus loin (cartouches unis, sans couleurs
du héros, sans trame BD).

Décisions de l'utilisateur :
- En sobre, retirer des menus : **la trame BD et les effets** (points, ombres rouges des titres, biseaux, reflets,
  dégradés → aplats unis) et **les couleurs du héros** (gris neutres, une seule couleur d'accent pour l'action principale).
- **Illustration de la scène : assombrie et désaturée**, sans zoom animé. Les polices BD restent.
- **Toutes les pages** (préparation, campagne, deckbuilder, galerie, stats, salon…), même réglage que le plateau.

À faire APRÈS l'en-tête fin et la mise en page 30 / 70 (mêmes fichiers).

## Fait (09/10/2026)
- `public/css/affichage-sobre-pages.css`, chargé après `teinte-pages.css` sur les 12 pages qui le chargent.
- `public/js/teinte-page.js` pose `data-affichage` sur toutes ces pages et ne pose plus la teinte du fond en sobre
  (aussi quand `prepare/app.js` la redemande).
- Retour de l'utilisateur : « moins flashy, pas noir et blanc, comme le plateau » : l'art de la scène est adouci
  (`saturate(.55) brightness(.7)`), pas en gris. La diagonale de la scène reste (sans elle, la scène couvre « Ton équipe »).
- Test : `ui-check/tests/affichage-sobre-pages.spec.ts` (4 pages, normal puis sobre). Captures : `.planning/captures-sobre/v3-*.png`.
