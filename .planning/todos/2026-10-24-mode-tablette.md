# Mode tablette (démarré le 24/10/2026)

Demande : tablette en paysage obligatoire, plateau PC, tout au doigt (pas de souris : survol, clic droit, petites zones).
Revoir toute l'UI / UX tactile ; reprendre ce qui marche au téléphone quand c'est utile.
Règles : questions une à une, capture ou maquette avant chaque question ; rien à coder avant les réponses ; pas de déploiement sans demande.

## Constat (1180×820, toucher simulé, commit ea32c637)
- Une tablette (largeur ≥ 768) reçoit le plateau PC (`useModeMobile.ts`, `telephone.ts`).
- Cartes ~75 px de large ; main coupée en bas (VOULU : au survol elle monte, cartes entières) ; « Fin du tour » flottant posé sur la main, en double avec la barre.
- Toucher le héros : petite boîte au centre (Changer de forme / Fin du tour) avec une croix minuscule ; aucun aperçu en grand au doigt.

## Décisions
0. **Paysage obligatoire** (demande de départ) : en portrait, écran « Tourne ta tablette » comme au téléphone.
1. **Base** : on garde la version PC (pas les ronds).
2. **Taille des cartes** : comme le PC (pas agrandies) ; on lit les cartes par l'aperçu en grand.
3. **Aperçu au doigt** : un toucher sur une carte ouvre l'aperçu du PC avec les boutons d'action de la carte ; un toucher à côté le ferme. (Quand le jeu demande une cible, un toucher la choisit directement, comme au téléphone.)
4. **Forme de l'aperçu** : l'aperçu du PC tel quel (même place, sans voile), boutons d'action dessous, carte touchée entourée de jaune.
5. **Main** : reste coupée ; un toucher sur une carte ouvre directement son aperçu avec « Jouer ». Le « Fin du tour » flottant disparaît en tablette (celui de la barre suffit, comme en téléphone couché).
6. **Mode manuel** : toucher une carte ouvre l'aperçu avec TOUS les gestes du clic droit en gros boutons dessous (les « … » ouvrent un sous-choix). Plus de menu flottant au doigt.
   **Glisser au doigt** (demandé par l'utilisateur) : glisser une carte là où elle doit agir : héros sur méchant / sbire = attaquer, héros sur manigance = contrer, carte de la main sur sa cible = la jouer, allié / soutien prêt sur une cible = l'utiliser (comme Q78 du téléphone). Cibles en jaune pendant le glisser. Dès que le doigt bouge, c'est un glisser ; sinon un toucher (aperçu).
7. **Zoom** : non. La table reste entière ; on lit par l'aperçu. Zoom du navigateur bloqué sur le plateau.
8. **Phase du méchant** : en tablette, « Plateau animé » par défaut (la table reste entière) ; « Guidée » reste au choix dans les réglages ; le PC ne change pas.
   Tranché sans question : plus de mentions de touches (« Espace ») sur les boutons en tablette ; quand le jeu demande de choisir des cartes (défausse de fin de tour, cible), un toucher les choisit ; un nom souligné dans un texte (« Peter Parker », « Assaut ») se touche pour ouvrir l'aperçu de la carte.
9. **Languettes AIDE / JOURNAL** : restent au bord droit, élargies à 46 px et plus hautes.
10. **Activation** : automatique (écran tactile sans souris, largeur ≥ 768) + réglage « Jeu au doigt : Auto / Oui / Non ».
   Tranché sans question : en mode tablette, toute cible touchable fait au moins 44 px (réglages, menus, choix de la fenêtre Réglages qui font 24 px aujourd'hui).
11. **Portée** : le plateau d'abord, puis les autres pages : éditeur de deck (toucher = aperçu avec +1 / −1 à la place du clic droit / survol), accueil (choix de la phase : « Plateau animé » présélectionné en tablette), campagnes, réglages ; cibles de 44 px partout.

## Ordre de codage proposé
1. Détection `estTablette` (coarse + ≥ 768, sans souris) + réglage « Jeu au doigt » ; écran « Tourne ta tablette » en portrait ; zoom navigateur bloqué sur le plateau.
2. Toucher = aperçu du PC + boutons d'action dessous (table et main), carte touchée en jaune ; toucher à côté ferme ; cible demandée = choisie directement.
3. Mode manuel : gestes du clic droit en gros boutons sous l'aperçu.
4. Glisser au doigt (attaquer, contrer, jouer, utiliser), cibles jaunes.
5. Retouches : « Fin du tour » flottant retiré, mentions « Espace » retirées, languettes 46 px, cibles 44 px (Réglages…), « Plateau animé » par défaut.
6. Pages : éditeur de deck, accueil, campagnes.
Captures en 1180×820 et 1024×768 (toucher simulé, Playwright `hasTouch`) ; scripts dans le scratchpad de la session 0e46d407.
