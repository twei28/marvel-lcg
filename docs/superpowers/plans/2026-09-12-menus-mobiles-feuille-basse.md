# Menus mobiles en feuille basse : plan d'exécution

**Spec :** `docs/superpowers/specs/2026-09-07-parcours-solo-mobile-design.md`, §5 (sous-projet 2 du §9).

**But :** sur le plateau portrait, tout panneau qui s'ouvre par-dessus la table
est une feuille basse (ou haute quand son contenu défile), pleine largeur,
boutons de 48 px, fermeture par Fermer ou Échap. Le rendu PC ne change pas.

**État mesuré le 12/09/2026** (Chrome piloté, 480x1050, tactile) : Options
s'ouvre en popover ancré au bouton, 1 093 px de haut, posé À 1 050 px du haut
(hors écran, on ne voit rien) ; Historique en popover PC de 520 px coupé en bas
à droite ; la question du moteur (`.demande-centrale`) flotte au milieu à
452 px, texte tronqué. Aucune classe `mode-plateau-portrait` sur `body`.

## Contraintes

- TypeScript strict, `t()` pour tout texte, commentaires en français, aucun em dash.
- Aucun composant réécrit : une feuille de style `menus-mobile.css` sous
  `body.mode-plateau-portrait`, et trois changements JS au plus (§5.3).
- Chaque itération est VÉRIFIÉE à l'écran (Playwright, 480x1050, captures)
  avant la suivante.

## Tâches

1. **La classe sur `body`.** `board.tsx` pose `mode-plateau-portrait` quand
   `modePlateau === 'mobile'` (effet, retiré au démontage). Test vitest.
2. **`usePlacement` en mode feuille.** Sous la classe, le hook ne mesure rien
   et rend `VIDE` : la feuille CSS décide. Test vitest.
3. **`menus-mobile.css`** (importée par `PlateauMobile.tsx`) : feuille basse
   pour `.popover-sauvegardes` (Sauvegardes, Options, Plus),
   `.demande-centrale:not(.est-en-scene)`, `.evenement-centrale`,
   `.menu-actions-carte`, `.actions-flottantes` ; feuille haute pour
   `.historique-panneau`, `.salon-panneau`, `.journal-heros`,
   `.plateau-selecteur`, les modales de cartes ; `.fin-partie` en colonne ;
   l'aperçu au survol (`.carte-apercu`) masqué. Gate vitest sur la feuille.
4. **Vérification à l'écran** : `ui-check/tests/menus-mobile.spec.ts` (projet
   `s24`, sur un état enregistré) ouvre Options, Historique, Plus, Journal et
   mesure : feuille dans l'écran, boutons ≥ 44 px, fermeture. La question du
   moteur et la fin de partie se vérifient sur une vraie partie locale
   (captures).
5. **Retour Android** : brancher les panneaux ouverts dans la pile de couches
   (`useCouchesBoard`), si le temps le permet ; sinon consigné.
6. Build local, captures, commit ; déploiement sur validation de l'utilisateur.

## Bilan du 12/09/2026

- Tâches 1 à 4 : **faites**, vérifiées à l'écran (Chrome piloté, 480x1050,
  captures) : Options, Historique, « … », Journal du héros en feuilles
  au-dessus de la barre ; la question du moteur en feuille basse ; la fin de
  partie en carte pleine largeur, bouton de 48 px. Filets : `npm run
  menus-mobile` (3 cas, partie neuve) et `npm run plateau-mobile` porté sur
  le rendu portrait (34 états, aucune carte sous 96 px, aucune cible sous
  44 px, aucun débordement).
- Écart assumé avec la spec : **pas de bouton Fermer dans la feuille**. Les
  composants ne sont pas réécrits ; la feuille s'arrête au-dessus de la barre
  et c'est le bouton qui l'a ouverte qui la referme (Historique et Salon se
  referment aussi d'un tap en dehors).
- Plein écran (spec §3 et §6.3, jamais fait) : le premier tap le demande,
  le retour au menu le quitte (`plein-ecran.ts`, 3 tests).
- Tâche 5 (Retour Android sur les feuilles) : **faite le 12/09 au soir**,
  sans câblage par composant : `retour-android.ts` observe le DOM
  (`FERMABLES`, un sélecteur par feuille), pousse une entrée d'historique
  quand une feuille apparaît et la referme sur `popstate` (bouton connu,
  sinon « Fermer / Annuler », sinon un tap sur le voile). Poussée SYNCHRONE
  dans l'observateur : différée d'un rendu, un Retour rapide quittait la
  page. 5 tests vitest, 1 test Playwright (Options puis carte ouverte : le
  Retour referme, l'URL reste sur `board.html`).
- Assistant (§6) : la modale du héros en feuille basse ; le reste avait été
  livré le 11/09 (barre fixe en bas, grille à 2-3 colonnes, récap sous la
  grille). La « fiche du héros au tap » (spec §6.2) est faite le 12/09 au
  soir : sans survol, le premier tap ouvre une feuille (`ouvrirFicheHeros`,
  art HD, traits, PV et vague, biographie dépliée, « Voir ses cartes » /
  « Choisir ce héros ») ; « Choisir » ou un second tap sur la même tuile
  assigne. Le PC ne change pas. Filet `ui-check/tests/assistant-mobile.spec.ts`
  (2 tests à 480x1050).
- Hors périmètre (spec §2), non touché : deck-builder, salon, rejoindre,
  campagne au téléphone.
