# Mode téléphone : refonte (décidée le 09/10/2026, 50 questions, EN COURS)

Remplace `2026-09-11-ecrans-de-preparation-sur-telephone.md` (écrans de préparation). Le plateau portrait de
`2026-09-07-parcours-solo-mobile-portrait.md` (clos, validé le 13/09) reste la base : on le retouche, on ne le refait pas.

## Cadre
- Périmètre : plateau ET pages de menus, à égalité. Portrait pour tout.
- Appareils variés : tenir de 320 à 430 px. Dès 768 px, disposition PC. Paysage toléré avec le plateau PC réduit, plus un
  verrou portrait en option.
- Zones tactiles : 44 px minimum partout.
- Mode sobre : le même réglage que sur PC.
- Hors périmètre : activité Discord, tchat sur téléphone.
- Ordre : assistant de préparation, puis les autres pages, puis le plateau. Validation à la fin (captures réelles à la fin,
  pas par zone). Déploiement seulement sur « déploie ».
- Tests : Playwright en 320, 360, 390 et 430 px, avec contrôle du débordement et des zones tactiles sous 44 px.

## Assistant de préparation (Héros, Équipe, Decks, Méchant)
- En-tête fin avec logo et menu burger (liens, langue en un toucher, compte).
- Barre d'étapes cliquable sous l'en-tête. Retour Android = étape précédente, partout dans les menus.
- Scène du héros en bandeau en haut (~25 % de la hauteur), fixe mais qui rétrécit en une ligne (nom + traits) au défilement.
- Grille dessous, 3 colonnes. Pas de survol : un toucher = aperçu dans le bandeau, bouton « Choisir » = valide.
- Barre fixe en bas : pastilles de l'équipe, Aléatoire, Continuer.
- « Options de ce héros » (arts alternatifs) supprimée de l'enchaînement : Choisir mène direct aux Decks, un bouton « Art »
  dans le bandeau ouvre la sélection.
- Decks : une carte empilée par deck (nom, aspects, validité, Choisir). Import marvelcdb dans une feuille basse.
- Méchant : même schéma que les héros.
- Modales (fiche du héros, biographie, nouveaux joueurs) en feuilles basses fermables en glissant.

## Autres pages
- Accueil : gros bouton « Jouer » puis vignettes (Campagne, Galerie, Deckbuilder...).
- Campagne : le livre page par page, glissement latéral.
- Galerie : barre de recherche + feuille de filtres à pastilles, 3 colonnes de cartes.
- Deckbuilder : décision du 09/10 gardée (grille plein écran, barre du bas « Filtres · Deck (40) », panneaux glissants).
- Salon invité : intégré à la refonte, même schéma que l'assistant (bandeau + grille 3 colonnes + barre du bas).
- Connexion / inscription : bandeau fin + formulaire dessous, clavier qui ne cache pas le bouton.
- Stats, profil, administration : cartes empilées à la place des tableaux.

## Plateau
- Garder : 4 bandes, 3 cartes par rangée, toucher long pour lire une carte, menu « … » en feuille basse. Le héros « coupé en
  bas » sur la capture est le défilement normal, pas un défaut.
- Languettes Piles et Main (déjà déplaçables en hauteur, place retenue par côté) : plus fines et semi-transparentes au repos.
- Jouer une carte : toucher puis bouton Jouer.
- Bandeau « Annuler » 5 s après chaque action.
- Texte : réglage « taille du texte » à 3 niveaux.
- Écran maintenu allumé pendant une partie (plateau seulement).
- Vibrations sur quelques moments clés (ton tour, attaque subie, validation), interrupteur dans les réglages.
- Animations courtes et sobres, coupées en sobre ou si le système demande moins d'animations.
- Images adaptées à l'écran, chargement paresseux.
- Installation en application (plein écran) proposée par un bouton discret.

## Constats des captures du 09/10 (avant refonte)
- Préparation portrait : scène réduite à une miniature tronquée ; Decks et Méchant laissent une grande zone vide ; Méchant
  n'affiche que trois méchants.
- Préparation paysage : en-tête = un quart de la hauteur, Solo / Coop sous la ligne de flottaison, « Options de ce héros »
  avec carte minuscule qui chevauche Valider.
- Galerie : filtres en style navigateur, 2 cartes par rangée en portrait.
- Plateau paysage : une seule bande à la fois, la main ouverte couvre presque tout.

## Journal
- 09/10/2026 : décisions prises, fiche écrite. Codage de l'assistant à lancer.
- 10/10/2026 : zone 2 (autres pages) codée, commits b8ce6864 (pages du jeu), 75430bd7 (site), 31ee97ff (nouveautés).
  Accueil : gros bouton « Jouer » qui ouvre les modes en feuille basse, puis 4 vignettes (Campagne, Galerie, Éditeur,
  Mises à jour). Stats (reprise.js) en feuille basse, tableaux en cartes. Galerie, campagne, éditeur : en-tête fin à
  burger (js/tel-pages.js, css/tel-pages.css). Site : barre fine à burger, connexion/inscription, admin en cartes.
  Filet : ui-check/tests/pages-telephone.spec.ts (320 à 430 px, débordement, 44 px, Retour, sobre). PC comparé
  avant/après au pixel (768 à 1920) : identique. Non déployé. Salon invité non touché (en pause).
