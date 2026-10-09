# Écran de campagne : livre ouvert au lieu des pages empilées (décidé le 09/10/2026, PAS ENCORE CODÉ)

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
