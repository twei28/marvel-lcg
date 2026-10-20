# Iron Fist officiel : questions ouvertes pendant la création (20/10/2026)

Une question par carte, options en multichoix (recommandation en premier), avec ce que chaque option
change EN JEU. Tant qu'une question est ouverte, la carte reste « Carte terminée : NON » dans
`docs/packs/iron_fist_cartes.md`. Le script actuel suit l'option 1 (comportement du moteur) ; rien
d'autre n'a été tranché.

## Q1 — 64008 Channel the Iron Fist : combien de fois sur Fists of Fury (et tout événement à plusieurs « Deal N damage ») ?

Carte : *Hero Interrupt : When you attack, remove 1 chi counter from Iron Fist → increase the amount of
damage that attack deals by 1 (by 2 instead if it is a basic attack).* (scan c3.png)
Situation : Iron Fist joue **Fists of Fury** (64004, « Deal 1 damage to an enemy. Deal 1 damage to an
enemy. Deal 1 damage to an enemy. »), Channel en jeu, 3 chi sur l'identité.

Constat moteur (autoplay du 20/10/2026, partie `iron_fist_rhino_normal_equilibre`, lignes 275-302) : le
moteur traite chaque « Deal 1 damage » comme UNE attaque (message « va attaquer » trois fois). Channel
est donc proposé trois fois : 3 chi dépensés, 2 + 2 + 2 = 6 dégâts. C'est le même modèle que les cartes
officielles déjà en jeu (Cybernetic Arm 54002, Aggressive Energy 32047 : +1 à chaque coup d'un
événement d'attaque à plusieurs coups ; Royal Flush 37007, Tooth and Claw 56008).

1. **(recommandé) Une attaque par coup, comme le moteur aujourd'hui.** Channel peut se déclencher sur
   chaque coup, 1 chi à chaque fois, +1 dégât sur ce coup. En jeu : Fists of Fury + 3 chi = jusqu'à 6
   dégâts ; le joueur choisit coup par coup s'il paie. Aucun changement de code.
2. **Une seule attaque pour tout l'événement, +1 sur UN coup.** Channel ne se déclenche qu'une fois par
   événement (1 chi), le +1 s'ajoute au premier coup seulement. En jeu : Fists of Fury + Channel = 4
   dégâts au mieux. Code : marquer l'événement déjà « canalisé » (limite par effet joué).
3. **Une seule attaque, +1 sur CHACUN des trois coups pour 1 chi.** En jeu : Fists of Fury + 1 chi =
   6 dégâts. Code : payer au premier coup, appliquer aux coups suivants du même événement.
4. Autre (préciser).

Note : la même question vaut pour la Réponse de 64001a ? Non : « After you play a card » compte les
cartes jouées (une seule pour Fists of Fury), elle n'est pas concernée.
