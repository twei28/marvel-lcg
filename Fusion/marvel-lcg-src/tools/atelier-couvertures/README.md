# Atelier de couvertures

Fabrique les couvertures de pack (héros, scénario, modulaire) à partir de `Pack Template.psd`
(dossier « _Templates_ » du Drive des créateurs fan-made).

- **Utiliser** : bouton « 🖌 Atelier de couvertures » dans l'en-tête de l'écran de préparation (compte administrateur), ou ouvrir `public/atelier-couvertures.html` (un seul fichier, double-clic).
  Déposer l'illustration, taper le titre (ou charger une image de titre), régler les couleurs, exporter
  en PNG (938 × 1538) ou en webp (600 px de haut, le format de `assets/textures/sets/`).
- **Regénérer la page** après un changement de `modele.html` ou de `calques/` : `python3 tools/atelier-couvertures/generer.py`.
- **`calques/`** : calques extraits du PSD (boîte, logos, étiquette), moitié de la taille du PSD.
  La page recolore la boîte et l'étiquette en gardant la luminosité et les blancs.

Limite : le titre stylisé de chaque pack est dessiné à la main dans les vraies couvertures ; ici il est
rendu avec une police au choix (ou une image de titre fournie).
