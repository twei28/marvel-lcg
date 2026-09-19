# La boucle de campagne, mesurée sur les dix boîtes

**Demandé le 19/09/2026** : « si nécessaire, tu crées tout un nouveau truc
parce que comme ça on peut tester toutes les campagnes. Autant faire une fois
un travail qui permettra de tout tester, de simuler automatiquement une
victoire, de voir les différentes choses qu'on peut sélectionner, toutes les
tester et voir si ça se met bien en place lors de la seconde partie. » Portée
choisie : **outil + les 10 boîtes à fond**.

## Ce qui manquait

Rien ne pouvait terminer une partie à la demande. Le harnais des capacités
monte une position, déclenche, mesure, s'arrête : tout ce qui se passe APRÈS la
dernière carte jouée était hors de portée — le carnet sortant, le panneau de
récompenses, et la partie suivante montée avec ce que la précédente a laissé.

## Ce qui a été ajouté

| Pièce | Fichier |
|---|---|
| Fin de partie forcée | `Puzzle.Win()` / `Puzzle.Lose()`, plus les triches console `Gagner()` / `Perdre()` |
| Avancement du complot principal | `Puzzle.AdvanceMainScheme(fois)` |
| Lanceur générique | `tools/test_campagnes.py` |
| Épreuves, boîte par boîte | `tools/epreuves_campagnes.py` |

    RELEASE=1 PARALLELES=4 CAS_PREFIX=cz \
      ~/marvel-work/python/bin/python3.10 tools/test_campagnes.py \
      "$PWD/.game-src-a" 48000 /tmp/rapport-campagnes.json ["filtre"]

**115 épreuves, 115 vertes, 327 s** : fne 6, trors 6, mts 12, gmw 15, sm 13,
mut_gen 13, next_evol 16, aoa 11, aos 19, web_of_deceit 4.

## Les huit défauts trouvés

1. **Toutes les boîtes** — les collecteurs lisaient `world.game_over` pendant
   `WhenGameOver`, qui n'est posé qu'après le message. Une victoire Fear No
   Evil ne cochait jamais l'affaire. Le collecteur reçoit désormais le message.
2. **gmw** — les artefacts galactiques étaient cherchés par un trait
   inexistant. Le carnet restait vide.
3. **gmw** — les manigances d'artefact n'étaient pas remélangées au deck
   rencontre, alors que c'est la punition principale du scénario 4.
4. **gmw** — « Power Stone Control » cherchait 16110 (Fanaticism) parmi les
   améliorations, au lieu de 16149 parmi les attachements.
5. **gmw** — le porteur était noté sous sa face active (« Steve Rogers ») et
   relu à une mise en place où tout le monde est en alter-ego.
6. **gmw** — les unités additionnaient `face.victory`, un booléen : on comptait
   les cartes au lieu des points de victoire.
7. **sm** — le matériel S.H.I.E.L.D. était fabriqué sans face arrière, donc la
   récompense du palier 13 (version améliorée) n'existait pas.
8. **next_evol** — les Maraudeurs vaincus étaient cherchés dans le deck vilain
   alors qu'ils attendent dans la réserve de côté.
9. **aos** — les serrures de campagne étaient posées sur la carte suivante du
   paquet de la cellule, alors que le livret dit « the top card of this deck is
   in play ».

Chaque correctif porte sa date et la citation du livret qui tranche. Les
questions de règles ont été tranchées sur les PDF officiels (annexe II du guide
de référence pour l'ordre de mise en place, livrets mc16, mc40 et mc50), jamais
à l'estime.

## Couvertures de livret (même jour)

Demande : « j'aimerais utiliser la couverture de chaque livret dans l'écran de
sélection des boîtes et des campagnes ». La page 1 des neuf livrets officiels a
été rendue à 975 px dans `public/stories/<code>/00-couverture.jpg` ; La Toile
du Mensonge, maison, reprend l'art de sa boîte recadré en carré.
`tools/pages_livret.py` rend désormais la couverture avec les autres planches,
et porte la liste des URL officielles. L'écran des campagnes l'affiche en
première couche, l'illustration d'extension restant dessous en repli.

## Ce que l'outil ne mesure pas

Le pilote joue le minimum et force la fin dès le tour du joueur : une épreuve
mesure une MISE EN PLACE, pas une partie complète. trors, sm et web_of_deceit
n'écrivent pas de carnet sortant ; leurs épreuves ne mesurent que ce que le
carnet CHANGE.
