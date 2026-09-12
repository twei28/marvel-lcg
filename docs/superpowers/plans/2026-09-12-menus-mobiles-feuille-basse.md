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
