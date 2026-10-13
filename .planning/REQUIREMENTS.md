# REQUIREMENTS : v1.1 Tablette et téléphone

Scopé le 2026-10-13 avec l'utilisateur, à partir de `.planning/research/v1.1/`.
Exigences v1.0 archivées dans `.planning/milestones/v1.0-REQUIREMENTS.md`.

## Décisions de cadrage (13/10/2026)

- Téléphone couché : les bandes du portrait réparties sur deux colonnes (rencontre à gauche, mon héros à droite), plus le plateau PC réduit.
- Menus du téléphone : barre de navigation en bas ; le burger ne garde que le secondaire.
- Réglages impossibles sur iPhone (vibrations, verrou portrait, plein écran) : masqués sur iPhone, inchangés ailleurs.
- Écrans limites (iPad mini portrait, écran partagé) : question posée une fois à l'arrivée + réglage permanent « Plateau : automatique / téléphone / tablette ».
- Aucune dépendance ajoutée (recherche STACK).

## v1.1 Requirements

### Fondations tactiles (SAISIE)

- [ ] **SAISIE-01**: Le jeu sait si le joueur utilise le doigt ou une souris/trackpad d'après son dernier geste, et bascule seul (iPad qui se déclare Mac compris)
- [ ] **SAISIE-02**: Le joueur règle « Écran tactile : automatique / toujours / jamais », réglage partagé par le plateau et les pages
- [ ] **SAISIE-03**: Le joueur règle « Plateau : automatique / téléphone / tablette » ; en automatique, le seuil de largeur s'applique
- [ ] **SAISIE-04**: Sur un écran limite (entre téléphone et tablette), le joueur choisit une fois à l'arrivée entre plateau téléphone et plateau tablette ; le choix est mémorisé
- [ ] **SAISIE-05**: Les zones sûres (encoche, coins) sont respectées sur iPhone et iPad (`viewport-fit=cover` sur le plateau)

### Tablette (TAB)

- [ ] **TAB-01**: Sur tablette au doigt, toucher une carte ouvre aperçu + menu, et l'aperçu se ferme en touchant ailleurs ou par une croix, sans déclencher la carte du dessous
- [ ] **TAB-02**: L'appui long n'ouvre ni la loupe ni le menu d'iOS, et le double toucher ne zoome pas la page
- [ ] **TAB-03**: Les boutons de la barre du haut, les compteurs et la croix font au moins 44 px à l'écran, réduction du plateau comprise
- [ ] **TAB-04**: Un appui long sur une icône affiche son libellé ; un toucher l'active
- [ ] **TAB-05**: Toucher une carte injouable affiche la raison
- [ ] **TAB-06**: Carte de la main agrandie : glisser à gauche ou à droite montre les autres cartes de la main
- [ ] **TAB-07**: L'agrandissement de l'identité propose « voir l'autre face » sans changer de forme
- [ ] **TAB-08**: Mode manuel au doigt : le joueur choisit un outil dans une barre (ex. « jeton +1 »), puis touche les cartes visées
- [ ] **TAB-09**: Avec « Écran tactile : jamais », le plateau PC est identique au pixel à avant le jalon

### Plateau du téléphone (TELP)

- [ ] **TELP-01**: Téléphone couché : les bandes s'affichent en deux colonnes (rencontre à gauche, mon héros à droite), la main en languette, au lieu du plateau PC réduit
- [ ] **TELP-02**: Après n'importe quel nombre de rotations, aucun bouton ne recouvre la main et une carte agrandie s'affiche en entier
- [ ] **TELP-03**: Quand le moteur demande une cible ou une réponse hors de l'écran, une pastille l'indique sur la bande ou l'onglet concerné
- [ ] **TELP-04**: La carte agrandie explique ses mots-clés (Retaliate, Guard…) sous le scan
- [ ] **TELP-05**: Les options existantes (bandeau Annuler, taille du texte, écran allumé, vibrations, installation) fonctionnent en portrait et en paysage
- [ ] **TELP-06**: Sur iPhone, les réglages vibrations, verrou portrait et plein écran sont masqués

### Menus du téléphone (TELM)

- [ ] **TELM-01**: Une barre de navigation en bas donne accès aux 4-5 destinations principales depuis toutes les pages ; le burger ne garde que le secondaire (langue, compte, mises à jour)
- [ ] **TELM-02**: L'assistant de préparation (Héros, Équipe, Decks, Méchant) est revu à la lumière de la recherche et cohabite avec la barre du bas
- [ ] **TELM-03**: Accueil, galerie, éditeur, campagne et connexion sont alignés sur la barre du bas ; le livre de campagne se feuillette par glissement
- [ ] **TELM-04**: Le jeu installé sur l'écran d'accueil s'ouvre sur l'accueil, jamais sur une ancienne partie

### Tests et diagnostic (TEST)

- [ ] **TEST-01**: Des gabarits Playwright touchent vraiment : tablette tactile (Chromium) et WebKit iPad
- [ ] **TEST-02**: Un test enchaîne 6 rotations et vérifie que la main et chaque bouton restent touchables
- [ ] **TEST-03**: Chaque signalement joint les mesures réelles de l'écran (taille, zones sûres, mode de saisie, plateau choisi)

## Future Requirements

- Vue d'ensemble des héros en coop sur téléphone (proposée par la recherche, non retenue pour ce jalon)
- Compteur anonyme des parties jouées couchées ou debout
- Vérification sur un vrai iPad et un vrai iPhone par un joueur (hors backlog automatique)

## Out of Scope

- Salon invité sur téléphone : reste en pause depuis le 10/10/2026
- Troisième mise en page dédiée à la tablette : la tablette est le plateau PC + l'axe de saisie
- Bibliothèques de gestes ou de feuilles basses (`vaul`, `@use-gesture`) : non maintenues, le maison existe déjà
- Verrou d'orientation imposé par défaut : impossible sur iPhone, et le paysage est désormais pensé
- Activité Discord et tchat sur téléphone : hors périmètre depuis le 09/10
- Toute modification des règles du moteur

## Traceability

| Requirement | Phase | Statut |
|-------------|-------|--------|
| SAISIE-01 | Phase 8 | En attente |
| SAISIE-02 | Phase 8 | En attente |
| SAISIE-03 | Phase 8 | En attente |
| SAISIE-04 | Phase 8 | En attente |
| SAISIE-05 | Phase 12 | En attente |
| TAB-01 | Phase 9 | En attente |
| TAB-02 | Phase 9 | En attente |
| TAB-03 | Phase 10 | En attente |
| TAB-04 | Phase 10 | En attente |
| TAB-05 | Phase 10 | En attente |
| TAB-06 | Phase 10 | En attente |
| TAB-07 | Phase 10 | En attente |
| TAB-08 | Phase 14 | En attente |
| TAB-09 | Phase 9 (DoD des phases 10 et 14) | En attente |
| TELP-01 | Phase 12 | En attente |
| TELP-02 | Phase 12 | En attente |
| TELP-03 | Phase 13 | En attente |
| TELP-04 | Phase 13 | En attente |
| TELP-05 | Phase 13 | En attente |
| TELP-06 | Phase 13 | En attente |
| TELM-01 | Phase 11 | En attente |
| TELM-02 | Phase 11 | En attente |
| TELM-03 | Phase 11 | En attente |
| TELM-04 | Phase 11 | En attente |
| TEST-01 | Phase 8 | En attente |
| TEST-02 | Phase 12 | En attente |
| TEST-03 | Phase 8 | En attente |

**Couverture : 27/27 exigences v1.1 rattachées, aucune orpheline.**
