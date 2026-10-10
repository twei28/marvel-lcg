# Phase du méchant « Sur la table » v3 : décisions du 10/10/2026

Recherche par 50 questions, aucun code écrit. Complète `2026-09-14-phase-mechant-sur-la-table-v2.md`.

## Bulle
- Fixe mais déplaçable, taille moyenne, onglets biseautés sur la bulle.
- Devient transparente automatiquement au survol d'une carte de la table.
- Une carte à la fois, une bulle par héros, bouton Suivant dans la bulle.
- Fil d'Ariane dans la bulle, détail sur 2 colonnes.
- Relecture de l'étape précédente (bouton et flèche gauche), couleur bleue pour les héros.
- Phrases seules, noms en gras ; calcul affiché (les deux formes).
- Termes officiels du jeu (activer, révéler, boost), FR et EN.

## Table
- Halo + atténuation des autres cartes + flèche ; jauge : 3 éléments retenus ; compteur « Sbire 2 / 3 ».
- Vol de carte + trait vers le héros ; zoom + bandeau de type à la révélation.
- Plusieurs jetons visibles ; pastilles « 1 par joueur + 1 accélération = 2 ».
- Alerte : jauge qui pulse en rouge + phrase d'alerte.
- Boost : un retournement par clic ; passage par « OK » ou Suivant.
- Choix héros/allié : clic sur la carte allumée ; clic pour utiliser ; Espace.
- Tout passer : avec confirmation.

## Son, mobile, accessibilité
- Sons : révélation, dégâts et menace ; plus discrets que le reste.
- Téléphone : feuille en bas, glissable (réduite, normale, dépliée).
- Mode sobre : rien de spécial. Réglage du mode : déjà dans les paramètres.
- Clavier : Espace/Entrée = Suivant, flèche gauche = précédent, Tab = cartes allumées.
- Aide : bulle d'accueil unique + bouton ? permanent.

## Multijoueur et fin
- Seul le joueur concerné clique pour sa part (chaque héros), les autres regardent ; on attend avec message « On attend [joueur] », sans minuteur.
- Spectateur : même bulle, sans bouton.
- Défaite : bulle de constat avant l'écran de défaite.
- Journal : une ligne par étape.

## Ordre de réalisation proposé
1. Bulle (forme, déplacement, transparence), 2. jauges et allumage, 3. étapes et relecture, 4. téléphone, 5. multijoueur/spectateur, 6. sons, aide, textes.

## Libellés exacts (relus dans le fil, 10/10/2026 soir)
- Q6 halo doré + reste de la table atténué + trait acteur → cible.
- Q7 jauge qui s'anime + nombre qui s'envole (« -3 ») + ancien niveau en fantôme + jauge agrandie pendant l'étape.
- Q8 gros bouton biseauté jaune avec la touche Espace indiquée + petite flèche « étape précédente ».
- Q10 pastilles [ATQ 2] + [boost 1] − [DÉF 3] pour le calcul, phrase pour le résultat.
- Q12 le boost s'agrandit au retournement et reste lisible jusqu'au clic (OK ou Suivant).
- Q17 défense : les défenseurs possibles s'allument sur la table, on clique la carte, la bulle explique.
- Q26 bilan dans la bulle : menaces posées à gauche, dégâts subis à droite.
- Q27 relecture : liste des coups de l'onglet s'il y en a plusieurs, puis relecture détaillée.
- Q29 « Terminer la phase », puis bandeau de transition « Phase des héros » en bleu.
- Q47 bulle d'accueil unique (3 lignes) + bouton ? permanent.

## Avancement
- [x] Étape 1 : bulle déplaçable, onglets biseautés, fantôme au survol (10/10).
- [x] Étape 2 : halo + table atténuée (feuille de style générée, EffetsSurTable), nombre qui s'envole, ancien niveau en fantôme, jauge agrandie et animée, alerte de menace qui pulse (10/10).
- [x] Étape 3 : bulle détaillée (rang « Sbire 2 / 3 », fil d'Ariane, pastilles de calcul, avant → après, ★, alerte), bouton jaune biseauté + Espace, ← précédent, Échap = tout passer avec confirmation, boosts un par clic (premier à l'arrivée), dernier boost agrandi, bandeau de type sur la carte révélée, bilan en bulle 2 colonnes + « Terminer la phase », défaite en bulle de constat (10/10).
- [x] Étape 4 : téléphone, feuille en bas à trois hauteurs (glisser sur les onglets) (10/10).
- [x] Étape 5 : spectateur sans bouton sur la table ; « On attend [joueur] » existait déjà (10/10).
- [x] Étape 6 : sons à 60 % pendant la phase sur table, aide d'accueil unique + bouton ?, Tab entre les cartes allumées, annonce du tour des héros en bleu (SplashTour), plusieurs jetons de menace, trait du sbire vers son héros à l'engagement (moteur : `engage_avec_id` sur l'effet `entree`) (10/10).
- [x] Q17 : sur la table, la bulle porte la question (et « Ne pas défendre ») à la place du panneau central ; les cartes restent allumées et cliquables (10/10).
- [x] Q24 : déjà en place, une étape (donc une bulle) par joueur à la distribution (`etapesDeroule`, point 3).
- [x] Q45 : en mode « Sur la table », le journal remplace le détail technique de chaque phase du méchant par une ligne par étape (`avecEtapesDuMechant`, journal-compact.ts) ; un round sans étapes connues garde son détail (10/10).

**Tout est codé (10/10/2026), non commité, non déployé en ligne. Moteur à redémarrer pour `engage_avec_id` et la menace d'avant.**
