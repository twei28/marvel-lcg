# Un mode MANUEL : le joueur fait tout, le moteur ne conduit plus

**Idée de l'utilisateur, 14/09/2026** : « une version pas automatisée du jeu :
on clique vraiment sur la pile pour prendre sa main, on amène la carte vers la
défausse pour la défausser, on clique sur la carte du méchant pour dire qu'on
lui fait autant de dégâts, pareil pour la manigance ».

Autrement dit : le plateau devient une **table**, et c'est le joueur qui
applique les règles. Le modèle est celui de Tabletop Simulator ou d'OCTGN.

## ⚠ Mon avis : c'est beaucoup plus proche qu'il n'y paraît

**Presque tous les gestes existent déjà**, dans `ui-app/src/board/triche.ts`,
qui parle au moteur par l'API `Puzzle` :

| Geste voulu | Ce qui existe déjà |
|---|---|
| Défausser une carte | `Puzzle.Discard` |
| Piocher | `Puzzle.Draw`, `Puzzle.Gain` |
| Mettre une carte en jeu | `Puzzle.PutIntoPlay` |
| Révéler une carte rencontre | `Puzzle.Reveal` |
| Infliger des dégâts | `Puzzle.Damage` |
| Poser de la menace | `Puzzle.PlaceThreat`, `Puzzle.SetThreat` |
| Incliner, redresser, retourner | `Puzzle.Exhaust`, `Ready`, `Flip` |
| Remettre dans le deck | `Puzzle.PutIntoDeck` |
| Statuts | `Puzzle.Tough`, `Stun`, `Confuse`, `Expose` |

Le moteur porte en plus une file de commandes libres
(`sandbox_commands` / `sandbox_executor`, `engine/device/manager/base.py`), et
le plateau sait déjà glisser des cartes (`ui-check/tests/glisser-plateau.spec.ts`).

**Ce n'est donc pas un second jeu à écrire.** C'est une autre façon de présenter
des commandes qui tournent déjà.

## ⚠ Le vrai coût n'est pas là où on le croit

Ce n'est pas « cliquer sur une pile ». C'est :

1. **Empêcher le moteur de conduire.** Aujourd'hui il pose les questions,
   enchaîne les phases, applique les règles. En manuel il doit se taire et se
   contenter de tenir l'état. C'est LE chantier, et il touche au cœur.
2. **Tout doit devenir manipulable.** En automatique, seules les actions légales
   sont offertes ; en manuel, n'importe quelle carte doit pouvoir aller
   n'importe où, y compris là où les règles l'interdisent. Une zone oubliée rend
   le mode inutilisable dès qu'on tombe dessus.
3. **Deux façons de jouer à maintenir.** Chaque carte maison, chaque correction
   devra être pensée dans les deux modes, ou assumée comme ne valant que pour
   l'un.

## Ce que ça apporterait vraiment

- Jouer les cartes **non implémentées**, et les extensions non portées : c'est
  le gain le plus concret, il débloque tout le catalogue.
- **Corriger une erreur du moteur** en pleine partie sans annuler dix coups.
- **Rejouer une situation** pour l'étudier.

## Ce que j'en pense, franchement

À faire, mais **pas avant d'avoir fini les chantiers ouverts**. Et à commencer
par le plus petit bout utile : un mode où le moteur se tait et où le menu de
triche existant devient un menu NORMAL, accessible sans drapeau de triche. On
saurait très vite si l'idée tient, pour quelques jours de travail plutôt que
quelques semaines.

⚠ Ne pas commencer par le glisser-déposer : c'est la partie visible, mais c'est
la moins risquée et la moins utile tant que le moteur continue de conduire.

## Statut

Notée le 14/09/2026, **non commencée**. À cadrer avec l'utilisateur quand les
chantiers en cours seront finis.

---

## Correction et cadrage du 18/09/2026

**Une promesse de cette fiche est fausse.** « Jouer les extensions non
portées » ne dépend PAS du mode manuel. Leurs cartes ne sont ni dans
`data/cards.json` (140 sets, tous portés) ni dans `assets/`. Sans import de
données, le mode manuel n'aurait rien à afficher. C'est un chantier
distinct, encore à cadrer.

**Le conseil « ne pas commencer par le glisser-déposer » est levé**, sur
décision de l'utilisateur : le mode visé est un calque de Tabletop
Simulator, et la manipulation directe en est le cœur, pas la décoration.

**Le coût est plus faible qu'annoncé, et les trois risques sont mesurés :**

1. Exécuter les commandes hors de `DoGetInput` marche déjà :
   `PuzzleHelper.Exec` est appelé dans `GameSetup`
   (`game/game_run/game_session.py:133`), sur le fil du jeu.
2. Les identifiants d'objets sont un simple compteur de création
   (`game/object/manager.py:59`), sans lien avec le tirage. Tout le corpus
   de cas Puzzle vise déjà les cartes par `c1`, `c2` d'une exécution à
   l'autre. Reste à prouver par un test aller-retour.
3. Faire taire les capacités tient en une porte, dans
   `EventManager.BroadcastMessage` (`game/event/manager.py:650`). Le récit
   à l'écran n'y passe pas (les messages appellent `Present` dans leur
   constructeur), donc l'affichage et le journal survivent. En revanche les
   modificateurs de caractéristiques disparaissent aussi : le plateau
   montrera les valeurs imprimées.

**Statut** : cadrée avec l'utilisateur le 18/09/2026. Spec à écrire.

**06/10/2026 : fiche close.** Spec écrite
(`docs/superpowers/specs/2026-09-18-mode-manuel-design.md`), livrée le 22/09,
complétée par `docs/superpowers/specs/2026-10-06-mode-manuel-comme-octgn-design.md`.
Suivi : `.planning/todos/2026-10-06-mode-manuel-comme-octgn.md`.
