# Une carte jouée se pose derrière le méchant avant d'aller à la défausse

**Constat de l'utilisateur, 15/09/2026**, signalé en passant, à traiter plus
tard : « pourquoi les cartes que je joue, on dirait qu'elles se placent derrière
le méchant quand je les joue, avant d'aller à la défausse ».

## Ce qui est noté, et rien de plus

Aucune investigation faite : la remarque est arrivée pendant un autre chantier
et l'utilisateur a demandé de la garder pour un prochain point. **Ne rien
supposer de la cause avant d'avoir regardé.**

## Où regarder quand on l'ouvrira

- `ui-app/src/board/CoucheAnimations.tsx` : le vol d'une carte qui QUITTE la
  main (`GROUPE_JEU`) va de sa position en main à sa position d'arrivée mesurée
  dans le DOM. Si la carte n'a pas encore de place à elle au moment de la
  mesure, le point d'arrivée peut tomber n'importe où, y compris sur la zone du
  méchant. C'est la même famille de défaut que la défausse vide qui envoyait les
  cartes voler vers la pioche (corrigé le 14/09/2026, voir
  `2026-09-14-animations-molles.md` point 6).
- `ui-app/src/board/zones.ts` : l'ordre des unités dessinées, et l'endroit où
  une carte en cours de résolution est posée.
- Le moteur fait transiter une carte jouée par une zone de résolution
  (`area_revealing` / zone de traitement) avant la défausse : si le plateau
  dessine cette zone au même endroit que le méchant, ce n'est pas une animation
  qui se trompe, c'est un placement.

## Statut

Noté le 15/09/2026, **non ouvert**. À faire décrire précisément (quelles cartes,
quel mode de phase) avant de toucher quoi que ce soit.
