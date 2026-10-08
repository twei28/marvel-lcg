# Mode normal : glisser un événement sur la table pour le jouer (08/10/2026)

**Statut : FAIT le 08/10/2026 (fd54189e), vérifié en vrai sans défaut (5 cas, ui-check/tests/zz-glisser-evenements.spec.ts), NON DÉPLOYÉ.** Demande : « en mode normal, on ne peut pas glisser les événements. J'aimerais qu'on puisse les glisser vers la zone de jeu pour les jouer, parce qu'il y a plein de cartes où il faut cliquer dessus et cliquer Jouer, alors qu'elles n'ont pas de lieu où être posées. »

## Décidé (questions une à une)

- Lâché n'importe où sur la table, il se joue ; lâché sur une cible possible, il la vise directement.
- Lâché sur une carte qui n'est PAS une cible possible : il se joue quand même, la cible se choisit ensuite comme aujourd'hui.
- Pendant le glisser, les cibles possibles s'allument, et viser une cible affiche ce qui va se passer (« Coup de pied tournoyant → Rhino »).
- Le paiement suit exactement le chemin du bouton « Jouer » (le glisser remplace seulement clic + Jouer).
- Toute carte de la main qui a une action « Jouer » se glisse (événements, ressources spéciales, manigances annexes du joueur…).
- Injouable maintenant : bulle rouge avec la raison (la même que celle de la carte injouable), la carte revient en main.
