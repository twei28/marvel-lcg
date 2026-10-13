# Phase 8 : Fondations tactiles et filet de tests - Contexte

**Recueilli le :** 2026-10-13
**Statut :** prêt pour la planification

<domain>
## Périmètre de la phase

Le jeu distingue doigt et souris d'après le dernier geste, sait quel plateau afficher
(écrans limites compris), expose deux réglages partagés plateau + menus, joint des mesures
d'écran aux signalements, et un filet Playwright tactile existe AVANT le premier changement
visible. Exigences : SAISIE-01 à 04, TEST-01, TEST-03. Rien des phases 9 à 14 (aperçu
refermable, cibles 44 px, barre du bas, paysage téléphone) n'entre ici.

</domain>

<decisions>
## Décisions d'implémentation

### Les deux réglages (« Écran tactile » et « Plateau »)
- Réglables à deux endroits, valeur unique partagée : la fenêtre Réglages du plateau ET les
  pages de menus.
- Côté plateau : onglet **Apparence** de `FenetreReglages.tsx` (à côté de « Couleur de la
  table » et « Placement des zones »).
- Côté menus : un bouton à côté de FR/EN et du bouton Affichage (même emplacement que
  `boutonAffichage`, en-tête et rangée flottante de l'accueil), qui ouvre les deux mêmes choix.
- Valeurs : « Écran tactile : Automatique / Toujours / Jamais » et « Plateau : Automatique /
  Téléphone / Tablette ».
- Mémoire **par appareil** uniquement (navigateur), jamais sur le compte : à la différence
  d'Affichage, pas d'envoi à `/save_preferences`.
- Effet **immédiat** : changer « Plateau » en pleine partie change la forme du plateau tout de
  suite, sans rechargement ni perte de partie (comme une rotation).

### Question posée sur écran limite
- Écran limite = appareil tactile dont la fenêtre fait entre ~500 et 767 px de large côté
  court en tablette : iPad mini debout (744x1133), iPad en écran partagé. Jamais un vrai
  téléphone (iPhone 390x844 : téléphone d'office), jamais un iPad standard (820x1180 :
  tablette d'office), jamais un PC. La borne basse exacte est à fixer par mesures.
- Posée **à l'accueil**, à la première arrivée, sur le modèle de la question de langue.
- Exception : un joueur qui arrive directement sur le plateau par un lien de partie sans
  être passé par l'accueil reçoit la question **à l'entrée du plateau**.
- Forme : fenêtre avec **deux vignettes dessinées** (plateau téléphone en bandes, plateau
  tablette complet), une ligne d'explication sous chacune, et « Tu pourras changer dans les
  Réglages ».
- **Pas de fermeture sans choix** : ni croix ni toucher à côté ; il faut toucher une vignette.
  Le choix est mémorisé, la question n'est plus jamais reposée sur cet appareil ; il se
  change ensuite dans les réglages.

### Bascule doigt / souris
- **Silencieuse** : aucun message ni indicateur à la bascule. Le mode courant se lit dans les
  mesures du signalement.
- Au chargement, en Automatique : départ **selon l'appareil** (doigt si l'écran principal est
  tactile : iPad, téléphone ; souris sinon), corrigé dès le premier geste.
- Anti-saut : le mode change **après le geste** (doigt levé), jamais pendant l'appui. Le geste
  qui provoque la bascule est traité normalement.
- **PC à écran tactile : reste souris** en Automatique, les touchers ponctuels ne basculent
  pas. Le joueur qui veut le mode doigt règle « Toujours ». ⚠ L'iPad qui se déclare Mac doit,
  lui, basculer (critère de succès 1) : la détection « PC » doit l'exclure explicitement.
- La disposition par largeur (`ui-app/src/board/mobile/useModeMobile.ts`,
  `REQUETE_MOBILE = '(max-width: 767px)'`) reste un axe séparé de la saisie.

### Signalement et filet de tests
- Mesures (taille d'écran, zones sûres, mode de saisie, plateau choisi) **jointes d'office et
  invisibles** : le formulaire de signalement ne change pas.
- Jointes **partout où l'on peut signaler**, pas seulement depuis la partie.
- Filet tactile de la phase 8 : **plateau sur fixture** (toucher une carte, ouvrir Réglages)
  + **accueil** (question écran limite). État de toutes les suites relevé AVANT tout
  changement (tout vert au 13/10, `boutons-bd.test.ts` compris : mesuré par la recherche).
- **Réglages testés sur une vraie partie** lancée sur un moteur d'essai séparé (port dédié,
  cache séparé) : le plateau sur fixture n'a ni Réglages ni signalement, et on ne l'en dote
  pas pour le test. La fixture reste utilisée pour « toucher une carte ». (Décidé après
  recherche, 13/10.)

### Décisions prises après la recherche (13/10)
- **Ligne « Plateau » masquée sur PC** : on garde la protection actuelle contre
  l'enfermement dans un plateau téléphone étiré sur grand écran (test existant).
- **« Table complète comme sur PC » est remplacée** par « Plateau » (validé par
  l'utilisateur le 13/10) : la ligne disparaît, la valeur `pc` migre vers « Tablette ».
- **« Plateau » ne change que le plateau en phase 8** : la valeur est partagée et réglable
  depuis les menus, mais son effet sur la mise en page des menus vient avec la phase 11.
- Gabarits : tablette tactile Chromium + WebKit **iPad (820x1180)** + WebKit **iPad mini
  debout (744x1133)**, avec `hasTouch` et vrais touchers.

### Latitude de Claude
- Libellés exacts et texte d'aide sous chaque réglage.
- Dessin des deux vignettes.
- Méthode de détection « appareil tactile » / « PC » / « iPad se déclarant Mac ».
- Bornes chiffrées exactes de l'écran limite (dans l'esprit ci-dessus).
- Comportement quand un iPad passe d'écran partagé à plein écran (non discuté : rester
  cohérent avec « choix mémorisé, jamais redemandé »).

</decisions>

<specifics>
## Idées précises

- Modèle à suivre côté menus : `public/js/prepare/affichage.js` (attribut sur `<html>`, CSS
  qui bascule sans rechargement, bouton dans l'en-tête et la rangée flottante), SANS la partie
  synchronisation compte.
- Modèle à suivre pour « une seule fois à l'arrivée » : la question de langue de l'accueil
  (`app.js`, vers la ligne 1046) et `doitProposerLeChoix` d'`affichage-choix.js`.

</specifics>

<deferred>
## Idées reportées

Aucune : la discussion est restée dans le périmètre.

</deferred>

---

*Phase : 08-fondations-tactiles-et-filet-de-tests*
*Contexte recueilli : 2026-10-13*
