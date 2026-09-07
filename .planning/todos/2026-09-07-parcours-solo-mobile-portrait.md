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
