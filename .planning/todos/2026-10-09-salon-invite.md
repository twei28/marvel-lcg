# Salon multijoueur (écran de l'invité) : refonte (décidée le 09/10/2026, PAS ENCORE CODÉE)

Constat (captures réelles, moteur d'essai à deux sièges, scratchpad `salon/`) : `public/salon.html` + `public/js/salon/`
est l'écran de l'INVITÉ (pas une messagerie) : 1) « Tu es le Joueur N » + grille de héros dans une colonne étroite au
centre d'un écran vide, style simple ; 2) choix du deck en longue liste de lignes texte ; 3) bandeau « Tu es prêt, en
attente du lancement par l'hôte », puis bascule directe sur le plateau. Mobile : deux colonnes, correct.

Décisions de l'utilisateur :
- **Même habillage que l'assistant de préparation** : en-tête fin, scène du héros à gauche (~30 %), grille à droite ;
  le choix du deck reprend l'étape Decks de l'assistant.
- **Attente** : dans la scène, « Prêt, en attente de l'hôte », et **l'équipe en train de se former** : les sièges avec le
  héros choisi par chacun (ou « en train de choisir »), le méchant dès que l'hôte l'a choisi.

⚠ Contrainte : `/get_heros_du_siege` est gardée par `tient_le_siege` (un invité ne lit pas le siège du voisin, voulu).
Il faut une route qui publie seulement le héros choisi par siège (+ méchant choisi), sans le deck. Garder la logique de
bascule existante (`bascule.js`, `decisionSalon`, tests `salon-bout-en-bout`, `bascule-salon`).

À faire après le mode sobre et avant / avec la refonte de l'éditeur de deck (mêmes styles).
