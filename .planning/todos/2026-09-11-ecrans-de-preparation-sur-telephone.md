# Les écrans de préparation sur téléphone

**Demandé par l'utilisateur le 11/09/2026**, pendant le chantier du plateau
portrait : « il faudra aussi revoir tout ce qui est écran de sélection etc ».

## Le périmètre

Le chantier en cours ne couvre QUE le plateau
(`docs/superpowers/plans/2026-09-11-plateau-portrait-telephone.md`). Tout ce
qui vient AVANT la partie reste à faire :

- l'accueil et le choix du mode (`public/prepare.html`, écran « Comment veux-tu
  jouer ? ») ;
- la sélection de héros, direction « Affiche » : art plein cadre à gauche,
  mur de portraits à droite (`stepTeam` dans `public/js/prepare/app.js`) ;
- le choix des decks, l'import marvelcdb, l'éditeur de deck ;
- la sélection du méchant et du niveau de menace (`stepScenario`) ;
- l'écran FINAL, le salon multijoueur, la reprise de partie.

## Ce qu'on sait déjà, sans avoir mesuré

- `public/css/prepare/prepare.css` contient **7 media queries**, dont une
  seule sous 560 px. La direction « Affiche » est bâtie sur deux colonnes
  (`--affiche-scene-w: 58%` et `.tb-droite` en absolu) : elle n'a pas de
  version en une colonne.
- Ces écrans ne sont PAS du React : ce sont des modules ES servis tels quels
  (`public/js/prepare/`), hors du build `ui-app`. Ils ne profitent donc
  d'aucune des briques du plateau portrait, et le travail ne se réutilise pas
  d'un côté à l'autre.
- Le plateau, lui, ne se joue plus qu'en portrait depuis le 11/09/2026 : un
  écran de préparation qui ne marcherait qu'en paysage obligerait à tourner le
  téléphone puis à le redresser entre la préparation et la partie.

## Ce qu'il faut faire avant de coder

Mesurer, comme pour le plateau : ouvrir chaque écran à 500x844 dans le
navigateur piloté, capturer, et décider écran par écran. Le relevé de
`play.marvelsimulator.com` a déjà montré ce qui marche sur un téléphone (pile
verticale, vignettes plutôt que cartes, une action principale par écran) ;
leur propre écran de choix de partie est un bon point de comparaison.

## Ordre suggéré

La sélection de héros d'abord : c'est le premier écran et le plus chargé.

## ✅ LIVRÉ LE 11/09/2026 (18:52 et 19:03), dans une autre session

Commits `40400f0f` « les écrans de préparation tiennent dans un téléphone »
et `fee77023` « l'accueil et l'écran final tiennent aussi ». Mesuré à
500x844 : barre du haut 55 px (281 avant), affiche 90 px, les trois méchants
visibles et cliquables sans défiler, grille de héros à 3 colonnes de 145 px,
Reprendre et la langue visibles, Stats / Bug / Documents réduits à leur
icône. Accueil (titre à `--titre-accueil`) et écran final (étoile VS à
120 px) corrigés. Les cinq étapes vérifiées une par une, coop à quatre
héros aussi. Rien ne change au-dessus de 600 px.

**Reste non mesuré** (hors des cinq étapes) : le salon multijoueur,
l'éditeur de deck et l'import marvelcdb, la reprise de partie. À ouvrir
seulement sur retour de terrain.
