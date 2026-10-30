# « Annuler » par instantané

Depuis le 29/10/2026, le bouton « Annuler » (et Échap / la croix de la question) ne rejoue plus la partie depuis zéro
**pendant le tour d'un joueur** : le moteur restaure un instantané pris à chaque question du tour.

## Pourquoi pas une copie (`deepcopy`)

Le moteur n'a ni historique d'états ni opération inverse : l'état est un graphe d'objets modifiés sur place, et le fil du
jeu attend le joueur au fond d'une pile d'appels. L'ancien « Annuler » rejouait donc les réponses du joueur depuis le début.

`deepcopy` est écarté pour deux raisons : le monde référence des verrous de thread, et surtout les capacités des cartes
sont des lambdas qui **capturent les objets du graphe d'origine** (`deepcopy` ne copie pas les fermetures : les effets
du monde copié agiraient sur l'ancien monde, sans erreur visible). On mémorise donc le **contenu** de chaque objet et on
le lui rend **en place** : mêmes objets, mêmes identités, fermetures valides.

## Où est quoi

| Pièce | Fichier |
|---|---|
| Capture / restauration en place, état hors graphe (hasard, historique, repères d'annulation), pile par tour | `src/game/world/instantane.py` |
| Prise d'un instantané à chaque question du tour, attrape du signal | `src/game/event/manager.py` (`PileDuTour`, `ProcessOptionalEffect`) |
| La demande (fil web) | `src/game/cheat/cheat.py` (`do_undo`) |
| La levée du signal (fil du jeu) | `src/engine/controller/controller.py` (`ChoiceOne`, juste après `GetInput`) |
| Interrupteur | config `annuler_par_instantane` (vrai par défaut) |
| Modale + info-bulle | `ui-app/src/board/ModaleAnnuler.tsx`, `board.tsx` (`demanderAnnulation`), `board.css` (`.bh-undo[data-infobulle]`) |

## Les pièges, dans l'ordre où ils ont mordu

1. **`/undo` s'exécute sur le fil web** (`/debug` → `SetCommand` → `PreDebugExec`), pas sur le fil du jeu. Lever
   `SignalRestaurer` dans `do_undo` l'envoie dans aiohttp. `do_undo` ne fait que DEMANDER (`undo.restauration_demandee` +
   `ExitWait`) ; le fil du jeu lève le signal en sortant de sa question, là où la pile d'appels de l'action existe.
   Un harnais qui déclenche la commande depuis le fil du jeu (comme `tools/test_mode_manuel.py`) **masque ce défaut**.
2. **`SignalRestaurer` est une `BaseException`** : le jeu est plein de `except Exception`.
3. **Pas d'instantané en double.** Quand le joueur clique « Annuler » à la question du tour, la boucle reboucle une fois
   sans action (`is_cheating`) : un second instantané du même état ferait « annuler » revenir là où l'on est déjà
   (`question_reposee`).
4. **La pile meurt avec la boucle du tour** : hors de la question du tour (phase du méchant, début de tour), pas d'instantané,
   on retombe sur l'ancien rejeu.
5. **Corrections à la main** (`scene.manuel_commands`, pause d'une partie ordinaire) : l'instantané les défairait avec le
   reste, le rejeu les garde (`cas_annulation_ordinaire_garde_tout`) → rejeu.
6. **Ni mode manuel, ni puzzle, ni test** (`Test.IsInTesting()`) : ils ont leur propre annulation.
7. Le rendu (`world.render`) est exclu de l'instantané : son compteur de trames ne doit pas reculer.

## Ce qui est restauré, ce qui ne l'est pas

Restauré : tout objet des modules `game`, `cards`, `core` atteignable depuis le monde, le message et les listes locales de
la boucle ; cellules de fermeture ; l'état du hasard (numpy, compteur, pile `Random.states`) ; l'historique des réponses
(`replay.history_inputs`, rangs, CRC) ; `last_step`, `next_step`, `debut_action`, `joueur_action`.

Pas restauré : l'état d'un module appelé `engine` (réseau, contrôleur, verrous), les attributs de **classe** mutables, les
globales de modules de cartes. Un test (voir ci-dessous) compare l'état avant/après ; un oubli se verrait comme une carte
ou un jeton différent après « jouer puis annuler ».

## Coût

~0,1 s par question du tour (≈32 000 entrées ; type classé une fois, ramasse-miettes suspendu pendant la capture), 0,03 s pour restaurer. **Mémoire : ~18 Mo par instantané** (mesuré). Profondeur
limitée à 10 par tour de joueur (`PileInstantanes.PROFONDEUR_MAX`, ≈180 Mo au pire par partie ; 40 en empilaient 720 Mo) ;
au-delà, retour au rejeu. Piste pour descendre : ne pas copier les objets qui ne changent jamais (données de cartes, messages
mis en cache : ~3 400 `WhenCountingResourcesOnCards` par exemple).

## Les tests

- `ui-check/tests/annuler-instantane.spec.ts` : le parcours du joueur (info-bulle, modale, « Garder mon coup », case cochée,
  annulation directe) ET l'état du monde identique avant/après. `ANNULER_INSTANTANE=1`, moteur d'essai sur un autre port que
  le 2345 (le test crée une partie).
- `ui-check/tests/annuler-action.spec.ts` : Échap et la croix (`/undo action`). Ce test pose un geste de console : il passe
  par le rejeu (point 5), ce qui est voulu.
- Le moteur trace `=== Annuler : instantane restaure ===` quand l'instantané sert : c'est la seule preuve que le rejeu n'a
  pas été utilisé.
- `ui-app/src/board/ModaleAnnuler.test.tsx` : la case ne ment pas (cochée + « Garder mon coup » mémorise quand même, et
  n'envoie jamais `/undo`).

⚠ `ouvrirEtMettreEnPlace` (`ui-check/pilote-campagne.ts`) répond à tout tant que la phase est celle de la mise en place : selon
la course avec le moteur, la première question du tour est déjà répondue (« Change Form ») ou non. Ne pas supposer la forme
de Spider-Man au premier tour (cf. `agir` dans `annuler-instantane.spec.ts`).
