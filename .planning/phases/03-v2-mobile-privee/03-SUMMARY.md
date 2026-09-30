# Phase 03 — V2 mobile privée

## Résultat

Une V2 mobile complète est disponible uniquement pour l'hôte dont le code de compte normalisé est `arnaud`. La version actuelle reste le comportement par défaut pour tous les autres comptes et pour les invités.

## Livré

- Porte d'entrée privée `prepare-v2`, protégée par la clé du siège hôte.
- Cookie de préférence `ui_version=v2`, jamais posé par une mauvaise clé ni par un invité.
- Préparation mobile : parcours en une colonne, commandes tactiles, navigation stable et zones sûres.
- Galerie, deck builder et replay : grilles et formulaires mobiles, actions de deck fixes, replay vertical.
- Plateau : onglets joueur à 44 px, prise en charge des encoches, focus visible et réduction des animations.
- Isolation stricte : sans le cookie V2, aucun marqueur V2 et aucune feuille V2 ne s'appliquent.

## Vérifications

- Authentification protégée : tous les cas passent, y compris les refus V2 invité et mauvaise clé.
- Mode local ouvert : tous les cas passent.
- Playwright : 17/17 scénarios V1/V2 à 360, 390 et 480 px.
- React : 17/17 tests ciblés du plateau.
- TypeScript : `tsc --noEmit` passe.
- Vite : build passe et la sortie contient uniquement les extensions autorisées.

## Livraison

Les sources sont prêtes et commitées. Le déploiement et le push restent volontairement séparés : le répertoire contient d'autres modifications utilisateur qui ne font pas partie de cette phase.
