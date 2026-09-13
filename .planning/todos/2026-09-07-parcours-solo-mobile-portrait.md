# TODO : finir le parcours solo au téléphone (portrait)

Mis en attente le 07/09/2026 au soir, à la demande de l'utilisateur, pour
créer un nouveau personnage.

## Où on en est

- Spec **version 2** validée et commitée (`47aa7824`) :
  `docs/superpowers/specs/2026-09-07-parcours-solo-mobile-design.md`.
  Portrait obligatoire, quatre rangées de vraies cartes de 110 px, menus en
  feuille basse, assistant sans bulle, livraison publique par
  `deploiement/deployer.ps1 -Code` à chaque sous-projet.
- Le plateau **paysage** (version 1, 22 commits `b60ba9fe..a3c84357`) est
  déployé en local ET sur narwhalchampions.com. Il est à retirer au
  sous-projet 1 ; 70 % de son code est réutilisé (CartePosee, PilesEpinglees,
  RangeeCartes, hors-champ, plein-ecran, etats).
- Rien du sous-projet 1 (plateau portrait) n'est commencé : pas de plan.

## Reprise

1. Relire la spec v2, §4 et §9.
2. `superpowers:writing-plans` sur le sous-projet 1 (plateau portrait), puis
   `subagent-driven-development`.
3. Ensuite les sous-projets 2 (menus), 3 (assistant), 4 (terrain).

## Pièges déjà payés (dans `.twei/SESSION.md`, section du 07/09)

- `bash ui-app/deployer.sh` ne touche que l'installation locale ; le serveur
  public ne reçoit le code que par `deployer.ps1`, qui redémarre le service.
- La clé `deploiement/cle_narwhal` est en 0444 sur /mnt/c : ssh depuis WSL
  exige une copie temporaire en 0600.
- `medaillon.css` pose sa grille sur `.plateau-mobile.est-paysage` : toute
  feuille du plateau mobile doit la neutraliser ou la découper.
- Ne jamais dimensionner une carte par une estimation en `dvh` : mesurer la
  boîte réelle (unités de conteneur) ou partir de la largeur.

## Point du 12/09/2026 : les sous-projets

1. Plateau portrait : livré le 11/09 (26 commits), filet Playwright porté
   dessus le 12/09 (34 états verts).
2. Menus en feuille basse : livré le 12/09
   (`docs/superpowers/plans/2026-09-12-menus-mobiles-feuille-basse.md`),
   avec le plein écran de la spec §3 et, le soir même, le Retour Android
   sur les feuilles (`retour-android.ts`).
3. Assistant au doigt : livré le 11/09 (écrans téléphone) et complété le
   12/09 (modale du héros en feuille, puis fiche du héros au tap le soir).
   Deck-builder et campagne mesurés OK à 480 px (boutons visibles, pas de
   défilement horizontal) ; le salon « Joueurs & tchat » n'est pas
   mesurable en local, à vérifier sur le terrain.
4. Terrain : premier test du 12/09 au soir, « je vois plein de problèmes »
   → refonte en BANDES, décidée en dix-neuf questions
   (`docs/superpowers/specs/2026-09-12-plateau-portrait-en-bandes-design.md`,
   plan `2026-09-12-plateau-portrait-en-bandes.md`) : quatre bandes qui
   défilent du doigt (méchant, manigances, engagés, mon héros), la main
   derrière une encoche à droite, les piles derrière une encoche à gauche,
   le bandeau qui porte le menu « … » et Fin du tour, plus de barre en bas,
   même plateau en paysage. L'ancien modèle `?medaillons` est retiré du
   dépôt. Livré le 12/09 au soir.

## ✅ CLOS LE 13/09/2026

**Le plateau téléphone est validé par l'utilisateur**, sur son téléphone :
« le plateau du téléphone c'est bon ». Les quatre sous-projets sont livrés et
éprouvés à la main. Ce qui reste du parcours mobile n'appartient plus à cette
fiche : le salon « Joueurs & tchat » n'a jamais été mesuré à 480 px, faute de
pouvoir le monter en local.
