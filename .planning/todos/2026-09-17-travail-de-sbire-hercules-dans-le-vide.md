# Le Travail de sbire d'Hercule se déclenchait dans le vide

**Signalé par BLStark le 17/09/2026** (rapport n° 14, écran plateau) : « Le
travail de sbire d'Hercules trigger dans le vide. »

## Ce que le journal de sa partie montrait

Scénario Sandman (Hapless Pedestrians), campagne Sinistres Motivations, round 5.
Lu dans l'ordre :

```
[(02,59002) Defeat the Hydra] est en cours de révélation
[(02,59002) Defeat the Hydra] révélée
[(02,59002) Defeat the Hydra] s’active
EncounterDeck<24> va être mélangé avec EncounterDiscardPile<11>
[[(02,59002) Defeat the Hydra]] défaussée(s)
```

La carte se révèle, cherche, ne trouve rien, et se défausse. Le joueur perd son
Travail sans avoir pu l'accomplir, et rien ne lui dit pourquoi.

## La cause

`Defeat the Hydra` (59002) dit : « **When Revealed**: Find a non-Elite minion
with at least 6 printed hit points. Reveal it, heal all damage from it, and
attach this card to it. »

Le script cherchait dans **deux zones seulement** : le terrain
(`Worlds.FindCardOnField`) et le deck de rencontre avec sa défausse
(`Search.EncounterCard(include_discard_pile=True)`).

⚠ **Or « Find » fouille TOUTES les zones.** Rules Reference p.19, entrée FIND :
« a player searches each game area where that card could be found (play area,
**set-aside area**, player deck, discard pile, encounter deck, etc.) ».

Et c'est précisément là que vit la cible : **`59037 Lernean Hydra`**, minion,
**6 PV, non-ELITE**, dans le set némésis d'Hercule, mis de côté au setup. La
cible évidente d'une carte qui s'appelle « Defeat the Hydra ».

Vérifié sur la partie de BLStark : aucun sbire éligible ailleurs. Sand Clone et
Common Criminal ont 3 PV, Rhino en a 8 mais il est ELITE. L'Hydre était la
seule cible possible, et elle était dans la seule zone que la carte ne
regardait pas.

⚠ **L'oubli est d'autant plus net que le même pack fait juste** :
`hercules/all_versus_all/__init__.py` appelle la même fonction **avec**
`include_set_aside=True`. Les deux Travaux chercheurs l'avaient perdu en route.

## Le correctif

`include_set_aside=True` sur les deux Travaux qui cherchent :

- `59002` Defeat the Hydra (le défaut signalé) ;
- `59003` Embody Pathos, même oubli, même correctif. Sa cible possible dans le
  set némésis est `59038 Olympic Feud`.

## La preuve

`tools/test_capacites.py`, cas « 59002 Defeat the Hydra — trouve le sbire
nemesis MIS DE COTE ». Scénario `rhino`, choisi parce que son seul sbire est
`01110 Hydra Bomber` (2 PV) : la seule cible éligible est donc celle du set
némésis, et le cas est déterministe.

**Vu rouge, puis vert :**

| | Résultat |
|---|---|
| Sans le correctif | ÉCHEC : « 59037 n'est pas en jeu ; 59002 n'est pas en jeu » |
| Avec le correctif | OK : état conforme, l'Hydre entre en jeu, la carte s'attache |

L'échec reproduit mot pour mot ce que BLStark a vu : la carte disparaît sans
rien faire.

## ⚠ Ce qui n'est PAS prouvé, et pourquoi le cas a été retiré

Un cas avait été écrit pour `59003` Embody Pathos. Il **passait avec ET sans le
correctif** : le scénario d'essai offrait une autre cible que celle du set
némésis, donc il ne prouvait rien. Il a été **supprimé** plutôt que gardé vert :
un cas qui ne peut pas rougir est pire que pas de cas.

Le correctif de `59003` reste en place — il est conforme à la règle FIND et au
reste du pack — mais **rien ne démontre qu'il change quelque chose en jeu**.
C'est écrit tel quel dans `test_capacites.py`. À reprendre avec un scénario
sans aucun complot annexe de rencontre, si un jour le besoin se présente.

Par ailleurs, la partie de BLStark montrait `Embody Pathos` **en zone de
victoire**, donc accompli : cette carte-là trouvait déjà ses cibles.

## Ce qui reste ouvert

- **Le joueur n'est pas prévenu** quand un Travail ne trouve pas de cible : la
  carte se défausse en silence. Même famille que les deux autres silences du
  16/09 (table qui refuse de démarrer, lancement de partie refusé).
- Le journal dit « EncounterDeck<24> va être mélangé avec
  EncounterDiscardPile<11> » après une recherche. Le Rules Reference (p.40,
  SHUFFLE) demande de mélanger **le deck**, pas d'y verser la défausse. Non
  vérifié plus avant : cela vient du moteur d'origine, pas de ce correctif.

## Statut

**Corrigé le 17/09/2026.** Correctif dans le MOTEUR : il ne prend effet qu'à
l'ouverture d'une table NEUVE, chaque table compilant son code au lancement.
