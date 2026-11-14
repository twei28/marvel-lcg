# Format de puzzle v2 (22/10/2026)

Code : `Fusion/marvel-lcg-src/src/game/puzzle/puzzle_data.py` (champs),
`puzzle_validation.py` (validation stricte). Tests : `python3 outils/test_puzzle_format.py`.

## Compatibilité
Le chargeur ignore les clés inconnues et laisse leur défaut aux clés absentes. Un
fichier v1 (les anciens `puzzle/*.json`) se lit donc sans migration : `format` vaut 1,
tous les champs v2 sont à leur défaut. Un fichier v2 porte `"format": 2`. Le checksum
du fichier reste en mode « Warn ».

## Champs conservés (v1)
`version, author, cover, comment, seed, villain, schemes, encounter_deck,
encounter_discard_pile, set_aside, expert, players[], puzzle_command[]`.
`players[]` : `identities, hand_cards, player_deck, player_discard_pile, set_aside`.
L'ordre des listes de decks est l'ordre réel (dessus du deck en premier).

## Champs ajoutés (v2), tous facultatifs
| Champ | Type | Défaut | Sens |
|---|---|---|---|
| `format` | int | 1 | 1 = ancien, 2 = v2 |
| `title` | texte ≤ 80 | "" | Titre affiché |
| `description` | texte ≤ 2000 | "" | Histoire / énoncé |
| `difficulty` | 0 à 5 | 0 | Étoiles ; 0 = non précisée |
| `hints` | ≤ 10 textes ≤ 500 | [] | Indices, dévoilés un par un |
| `objectives` | ≤ 6 | [] | Voir ci-dessous |
| `objectives_mode` | `all` / `any` | `all` | Tous requis, ou au moins un |
| `start_phase` | `""`, `player`, `villain`, `end_round` | "" | Phase de départ (vide = début de phase joueur, comportement v1) |
| `start_step` | texte | "" | Étape dans la phase (précisée en E2) |
| `first_player` | indice dans `players` | 0 | Premier joueur |
| `solution_visibility` | `after` / `always` / `never` | `after` | Quand la solution de référence est visible |
| `has_solution` | bool | false | Une solution de référence existe (stockée à part) |
| `players[].deck_name` | texte | "" | Deck d'origine, affichage seulement |

Objectif : `{kind, target, text}` avec `kind` parmi `defeat_villain`, `survive`,
`complete_scheme` (`target` obligatoire : le complot visé), `free_text` (`text`
obligatoire, validé à la main par le résolveur).

## Où est l'état du plateau ?
Dans `puzzle_command`, comme en v1 : des appels `Puzzle.<Méthode>(...)` rejoués au
démarrage (dégâts, statuts, mises en jeu…). Le format n'a pas de second langage.
E2 ajoute les commandes manquantes (joueur visé, ressources, stade, phase) ; E4 les
produit depuis le plateau.

## Validation stricte (tout puzzle venant d'un joueur)
`validate_puzzle(puzzle, allowed_methods)` renvoie la liste des erreurs.
- **Commande** : un seul appel `Puzzle.<Méthode>(...)` ; arguments = texte ≤ 200,
  entier |n| ≤ 10⁶, booléen, None, référence `cN`, listes imbriquées (3 niveaux) de ces
  valeurs ; mots-clés permis (`player=1`). Refusés : tout le reste (import,
  affectation, chaînage, lambda, compréhension, f-string, `*args`, flottants…).
- `allowed_methods` : fournir `{n for n in dir(RunPuzzle) if n[:1].isupper()}` côté
  serveur pour refuser un nom de méthode inconnu.
- **Limites** : 1 à 4 joueurs, 200 cartes par zone, 2000 commandes de 400 caractères.
- Identifiants de carte : lettres, chiffres, `_`, `-`, `,` (40 caractères au plus).

## Faille trouvée au cadrage
`PuzzleHelper.Exec` ne refuse que les *appels* hors `Puzzle.<méthode>` ; une commande
sans appel (`import os`, `Puzzle.world.x = 1`) passe le filtre et est exécutée avec
`exec`. Sans danger tant que les commandes viennent de nous, inacceptable pour des
puzzles publiés : **E7 doit appeler `validate_puzzle` à la publication ET à la lecture**,
et E3 doit faire passer `Exec` par `validate_command` pour tout puzzle v2.
