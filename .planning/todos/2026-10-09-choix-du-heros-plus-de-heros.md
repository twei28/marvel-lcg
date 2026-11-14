> **MISE À JOUR 23/10/2026 : FAIT, l'en-tête ci-dessous est périmé** (ancien état : « « PAS ENCORE CODÉ » »). Preuve : `public/css/prepare/prepare.css:65` : `--affiche-scene-w:32%` (le défaut du fichier restant 58 % aux lignes 1361 et 1470, remplacé par cette variable) ; nombre exact de colonnes et de rangées non mesuré (tri : `docs/rapports/etat-du-backlog-2026-10-19.md` §3, n°6).

# Étape « Choisis un héros » : plus de héros visibles (décidé le 09/10/2026, PAS ENCORE CODÉ)

Avant : la grille des héros tient dans la moitié droite (5 colonnes, à peine 2,5 rangées visibles, une douzaine de héros) ;
la moitié gauche est la scène du héros (ou le grand titre « CHOISIS UN HÉROS » quand rien n'est survolé) ; « Ton équipe »
prend de la hauteur sous la grille.

Décision de l'utilisateur, après maquettes (`maquette-B2.png` dans le scratchpad de la session du 09/10) :
- **Scène à gauche plus étroite, environ 30 % de la largeur**, MÊME STYLE qu'aujourd'hui : illustration du héros zoomée en
  fond, traits (GUARDIAN · MYSTIC), grand nom Marvel rouge et blanc, pastilles HP / WAVE / VARIANTS, boutons SEE HIS
  CARDS / BIOGRAPHY / FOR NEWCOMERS. Pas une carte entière posée à plat.
- **Grille à droite, environ 70 %** : vignettes actuelles (même taille, mêmes infos : illustration recadrée, nom, traits),
  environ 7 colonnes et 4 rangées à 1920x1080, soit ~28 héros visibles.
- « Ton équipe » plus compacte en bas, Aléatoire / Continuer inchangés.

À faire APRÈS l'en-tête fin (même fichiers : public/js/prepare/app.js, prepare.css).

Étendu le 09/10/2026 (après maquette `maquette-B3.png`, validée) : la MÊME disposition 30 / 70 s'applique aux trois étapes de
l'assistant qui ont une scène à gauche, **Équipe, Decks et Méchant** (Decks : la liste des decks, l'import marvelcdb et
l'art des ressources s'élargissent à droite ; « Ton équipe » compacte en bas).
