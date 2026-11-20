# Questions ouvertes du lot « backlog 1, 2, 3 » (20/10/2026)

La question de la réaffichage de la fenêtre « Choix de la phase du méchant » est TRANCHÉE (décision du 20/10/2026 : une seule fois à tous, choix conservés) et implémentée : clé `mc_phase_choix_vu` à `2026-10-20`.

## Fenêtre de choix hors de la table (fiche du 07/10/2026)

État constaté : le cas de la capture de la fiche (toutes les cibles hors table, ex. Constant Training de Cyclops) est déjà réglé depuis le 10/10 par la fenêtre unique du rapport n76 (cartes, puis Annuler et Valider, une seule poignée qui déplace tout). Le cas qui restait en deux pièces (cibles à la fois sur la table et hors table, la table devant rester cliquable) est maintenant collé : le panneau d'action devient le haut du sélecteur, même largeur, une poignée pour l'ensemble.

1. **Position de départ de l'ensemble.** Aujourd'hui : au centre, remis à zéro à chaque nouveau choix (comportement existant, conservé). Alternative : mémoriser la dernière position entre deux choix (le mécanisme `memoire` de `useGlisserPanneau` existe). Recommandation : garder le centre, car un ensemble resté dans un coin d'un choix précédent déroute plus qu'il n'aide.
2. **Place des boutons dans la fenêtre modale (cas « tout hors table »).** La capture de la fiche montrait Annuler et le bouton de validation EN HAUT, avec le titre ; la fenêtre du 10/10 les met EN BAS, sous les cartes. Recommandation : laisser en bas dans la fenêtre modale (lecture naturelle après les cartes), le bandeau du haut ne s'applique qu'au cas mixte. À défaut, déplacer les boutons en haut est un changement de CSS d'une dizaine de lignes.
3. **Petit écran (téléphone, mis de côté).** Le bandeau reste en haut du sélecteur, sans règle propre au téléphone. Question gardée pour la reprise du chantier téléphone.

## Textes à tutoiement hors périmètre du lot

Seuls les textes de la fenêtre de choix de la phase, des réglages de la phase et de l'entrée de nouveautés de la phase ont été revus. Restent tutoyés (non touchés, consigne « pas les autres écrans ») : l'écran d'affichage de la préparation (`app.js` : « Tu pourras changer à tout moment : bouton Affichage… »), les autres entrées de nouveautés du 19/10 (« ton choix », « quand tu assignes un deck », « ton deck »), les textes de l'assistant (« Choisis la cible », « Paie… ») et `FenetreReglages.tsx:706`. Recommandation : un lot de passage unique sur tout le jeu, avec un dictionnaire anglais mis à jour en même temps.
