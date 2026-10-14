# Mode tablette simple : le plateau PC au doigt (12/10/2026)

Retour joueur : « ça marche sur iPad mais clairement le tactile c'est pas terrible ». Un iPad (≥ 768 px) reçoit
le plateau PC (`ui-app/src/board/mobile/useModeMobile.ts`), pensé pour la souris. Choix de l'utilisateur : la
version simple (plateau PC rendu tactile, gestes du téléphone réutilisés), pas une troisième mise en page.
Inventaire complet : scratchpad de la session (`inventaire-tactile.md`), points bloquants : aperçu au survol
(`Board.tsx:1133`, un toucher ouvre aperçu + menu et l'aperçu ne se ferme plus), barre du haut à 30 px.

## Décisions

| # | Question | Réponse |
|---|---|---|
| 1 | Toucher une carte | **Aperçu + menu ensemble** (comme aujourd'hui) |
| 2 | Fermer l'aperçu | **Les deux** : toucher ailleurs OU une croix sur l'aperçu |
| 3 | Barre du haut | **Boutons de 44 px**, la barre grandit sur tablette |
| 4 | iPad avec trackpad / souris | **Selon le dernier geste** : doigt → tactile, trackpad → souris, bascule automatique |
| 5 | Réglage manuel | **Oui** : « Écran tactile : automatique / toujours / jamais » |
| 6 | Mode manuel au doigt | **Plus tard** |
| 7 | Infobulles des icônes | **Appui long** affiche le libellé, un toucher active |

## Retours de Raven (téléphone, iPhone Safari vertical, 12/10/2026 21:30), à faire dans ce chantier

1. La fenêtre du Mulligan du début gêne : l'agrandissement d'une carte (appui long) passe sous son message →
   masquer ou déplacer la fenêtre pendant l'agrandissement.
2. Carte de la main agrandie : glisser à gauche / à droite pour voir les autres cartes de la main en grand.
3. Voir l'autre face de son identité (héros / alter ego) pour lire un passif, SANS changer de forme (aujourd'hui :
   changer, valider, annuler) → bouton « voir l'autre face » dans l'agrandissement de l'identité.
Suite (12/10/2026, 22:08 et 22:20) :
4. Vertical : les cartes en jeu se superposent, impossible de jouer une action sans toucher une autre carte →
   une ligne par famille : héros + alliés, soutiens, améliorations.
5. Vertical : le réglage « améliorations à gauche » n'a aucun effet (il marche en horizontal).
6. Horizontal : après plusieurs rotations, « Fin de tour » se retrouve sur les cartes de la main, impossible
   de les toucher.
7. Horizontal : une carte affichée en grand ne montre que sa moitié haute.
« C'est excellent pour le moment sur téléphone. » Ces trois points visent le PLATEAU TÉLÉPHONE (PlateauMobile,
MainPortrait, agrandissement à l'appui long), pas le plateau PC : ils sont faits dans le mode téléphone, au même
moment que le mode tablette. Les points 2 et 3 pourront ensuite être repris sur tablette.

## Lots

- T1 : détection (dernier geste, iPad qui se déclare Mac via maxTouchPoints, réglage auto/toujours/jamais) +
  fermeture de l'aperçu (toucher ailleurs + croix) + `touch-action: manipulation`, `-webkit-touch-callout: none`.
- T2 : cibles de 44 px (barre du haut, compteurs, croix), infobulles à l'appui long, raison « injouable » au toucher.
- T3 (plus tard) : mode manuel au doigt, vérification sur un vrai iPad.

**Avancement (13/10/2026)** : retours de Raven 1 à 7 faits et commités (959f1402, non déployé). Prochaine
étape : T1. À noter : `boutons-bd.test.ts` est déjà rouge avant ce commit (vient de l'autre session).

À lancer après la passe de finition de la refonte de la phase du méchant (mêmes fichiers du plateau).
