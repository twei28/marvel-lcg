# Questions ouvertes, backlog 7 / 27 / 28 (20/10/2026)

Rien ci-dessous n'a été tranché ni codé : la fiche
`2026-09-28-nice-to-have-yarro.md` ne suffit pas à spécifier ces points.

## Q1. Raccourcis clavier des phases (27c)

**État actuel** (lu dans `board.tsx`, `clavier-cartouche.ts`) : `E` = fin du
tour, `Espace` = étape suivante / fin du tour, `U` = annuler, `B` = rapport de
bug, `Échap` = refus ou annulation, chiffres `1` à `9` = le choix numéroté du
cartouche. Il n'existe aucune aide à l'écran qui les liste.

**La fiche ne dit pas** quelles phases ni quelles touches : « Pas de détail
supplémentaire fourni ».

**Question** : que doit couvrir « passer les différentes phases » au clavier ?

- **Option A (recommandée) : ne rien ajouter aux touches, afficher la liste.**
  Les touches `E` et `Espace` passent déjà du tour du héros à la phase du
  méchant, puis les étapes. On ajoute seulement une ligne « Raccourcis » dans
  l'aide du plateau. En jeu : aucun risque de frappe accidentelle, Yarro
  découvre ce qui existe.
- **Option B : une touche par transition de phase** (par exemple `H` pour la
  phase du héros, `M` pour celle du méchant, `R` pour le ménage de fin de
  tour). En jeu : plus rapide pour un joueur expert, mais le moteur enchaîne
  les phases tout seul après `E` ; une touche « aller à la phase du méchant »
  n'aurait rien à faire de plus que `E`, et une touche « revenir » serait un
  retour arrière que le moteur n'offre pas.
- **Option C : un jeu complet** (passer l'étape, passer l'annonce, ouvrir le
  journal, ouvrir les réglages, etc.). En jeu : le plus utile au clavier seul,
  mais le plus gros, avec des collisions possibles avec les chiffres du
  cartouche et les champs de saisie.

**Ce qu'il faut de l'utilisateur** : A, B ou C, et pour B/C la liste des touches
voulues.

## Q2. « Écarter pour voir dessous » (27a), que reste-t-il à couvrir ?

**État actuel** : la demande « déplacer les fenêtres popup qui s'empilent » est
déjà servie par le chantier du 28/09 (« toutes les fenêtres, tous les
panneaux ») : la fenêtre de décision (`DemandeCentrale`), la confirmation
(`ConfirmationJeu`), le sélecteur hors table (`SelecteurCibles`) et le
cartouche du méchant (`DeroulePhase`) se déplacent à la poignée
(`poignee-glisser`), et le panneau de manigance peut se réduire (« Réduire le
panneau »).

**Écart avec l'énoncé du backlog** : l'énoncé parle d'« écarter des cartes pour
voir dessous » ; la fiche, elle, parle de fenêtres popup (capture de deux
fenêtres « Klaw is about to attack Wolverine » superposées).

**Question** : Yarro veut-il aussi pouvoir écarter des CARTES de la table
(piles de sbires ou d'améliorations qui se chevauchent) ?

- **Option A (recommandée) : non, les fenêtres suffisent.** On vérifie à
  l'usage qu'aucune fenêtre n'a de poignée manquante, et on clôt le point.
  En jeu : rien ne change.
- **Option B : un éventail au survol ou au clic d'une pile** (les cartes d'une
  pile se déploient temporairement). En jeu : on voit les cartes cachées sous
  les premières, mais c'est un nouveau geste sur la table, qui entre en
  concurrence avec le glisser-déposer des cartes.
- **Option C : un bouton « Écarter les fenêtres »** qui replie d'un coup tout
  ce qui recouvre la table. En jeu : un seul clic au lieu de déplacer chaque
  fenêtre ; il faut décider si les questions obligatoires du moteur peuvent
  être masquées (le jeu ne continue pas tant qu'elles n'ont pas de réponse).

**Ce qu'il faut de l'utilisateur** : A, B ou C.

## Q3. Assigner tous les dégâts d'un coup (27b), déjà couvert, à confirmer

**État actuel** : `assignerReste` (`interaction.ts`, `ScanCard`, présent depuis
le 04/10/2026) pose en un clic tout ce qu'une carte peut encore recevoir
dans une répartition. Je n'ai donc rien codé.

**Question** : le bouton existant répond-il à la demande de Yarro (répartition
sur plusieurs sbires et alliés, « actuellement clic par clic ») ?

- **Option A (recommandée) : oui, clore.** En jeu : rien ne change.
- **Option B : ajouter une répartition automatique** (un bouton « Répartir
  équitablement » ou « Tout sur le plus faible »). En jeu : plus rapide, mais
  le choix de la répartition est une décision de jeu ; l'automatiser retire
  une décision au joueur, il faudrait donc la proposer sans jamais l'imposer.

**Ce qu'il faut de l'utilisateur** : A ou B (et la règle de répartition en B).
