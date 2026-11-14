# Nice to have relevés par Yarro (28/09/2026, sur Discord)

Trois idées, aucune urgente, aucun bug. Partagées par Yarro en même temps que
les signalements 25-28, notées à part pour ne pas les perdre.

- **Déplacer les fenêtres popup qui s'empilent.** Capture à l'appui : deux
  fenêtres de décision superposées (« Klaw is about to attack Wolverine »)
  sans moyen de les écarter pour voir ce qu'il y a dessous.
- **Assigner tous les dégâts d'un coup plutôt qu'un par un.** Capture à
  l'appui : répartition de dégâts sur plusieurs sbires/alliés, actuellement
  clic par clic.
- **Raccourcis clavier pour passer les différentes phases.** Pas de détail
  supplémentaire fourni (quelles touches, quelles phases précisément).

Pour mémoire, deux autres points de son message du même jour ont été traités
ailleurs, pas ici :
- « Le reveal qui speed trop vite pour suivre » (Surge enchaîné) → couvert
  par le correctif du signalement n°27 (bannière « Renfort : ... »).
- Le glisser-déposer pour permuter les cartes à ordonner (vu sur Felt Table,
  Flesh and Blood) → décision utilisateur du 28/09 : à développer EN PLUS des
  badges numérotés déjà posés pour le signalement n°28, pas à leur place.

## Statut au 20/10/2026 (décisions de l'utilisateur)

- (a) Écarter pour voir dessous : CLOS. Les fenêtres se déplacent à la poignée depuis le 28/09 (et le panneau de manigance se réduit) ; rien à coder.
- (b) Assigner tous les dégâts d'un coup : CLOS. Couvert par `assignerReste` (`interaction.ts`, `ScanCard`), présent depuis le 04/10.
- (c) Raccourcis clavier des phases : FAIT, option A. Aucune nouvelle touche ; l'aide du plateau (`VoletAideAuto.tsx`) liste maintenant toutes les touches existantes (E, Espace, U, B, 1 à 9, Échap), FR et dico-en, avec un cas dans `VoletAideAuto.test.tsx`.
- (d) Glisser-déposer pour permuter les cartes à ordonner : FAIT (`ordre-glisser.ts`, spec `ordre-glisser-selection.spec.ts`).
