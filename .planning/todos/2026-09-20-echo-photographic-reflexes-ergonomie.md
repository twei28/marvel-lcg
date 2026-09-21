# Echo : Photographic Reflexes ne dit pas comment elle se joue

**Signalement d'un joueur (Yarro), 19/09/2026 16:18, rapport n°17** :

> Photographic Reflexes, normalement tu peux le défausser pour venir chercher
> une carte sous Echo. Là ça ne fonctionne pas : en mode test tu peux le
> défausser mais ça ne fait rien, et en « prod » tu ne peux rien faire.

## ⚠ Ce n'est PAS un défaut du moteur

Vérifié le 20/09/2026 sur le journal de SA partie, joint au rapport.

**La mécanique fonctionne, et il s'en est servi sans le savoir.** Le journal
montre : « Echo would play Strength in Diversity with (mental mental) », la
carte s'active, inflige 1 dégât à Venom et retire 1 menace. Deux ressources
payées, c'est-à-dire le coût réduit de 2 que la carte promet.

Au moment où il a pris son signalement, l'option était **encore offerte** dans
la demande en cours : « Play / portée par c35 / coût 2 », où c35 est la carte
glissée sous Echo.

**Ce qu'il a fait à la place** est aussi dans le journal :
`[triche] Discard — Photographic Reflexes`. Il a défaussé la carte par le menu
du bac à sable. Une intervention de triche ne déclenche évidemment rien.

## Le vrai problème : la carte ne dit pas comment elle se joue

Sa phrase décrit une mécanique qui n'existe pas. La vraie est l'inverse :

- on clique sur l'**événement glissé sous Echo** pour le jouer, coût réduit de 2 ;
- **Photographic Reflexes part toute seule**, comme conséquence, jamais comme
  action du joueur.

Rien à l'écran ne le dit. La carte reste dans la main sans être ni jouable ni
défaussable, ce qui invite exactement à l'erreur qu'il a faite. Un joueur qui
tient une carte qu'il ne peut ni jouer ni défausser conclut à un bug, et il a
de bonnes raisons.

Implémentation, pour qui reprendra le sujet : tout vit sur Echo
(`cards/pack/fne/echo/60037a.py`), la carte elle-même
(`60040a.py`) est volontairement vide. Trois conditions : forme héros, c'est
bien ton Echo, et Photographic Reflexes est dans ta main. Plus
`CanGenerateResources(Resources('GG'))` pour la réduction de coût.

## Pistes, à cadrer

1. Rendre visible que la carte glissée sous Echo est **jouable** : c'est le
   geste que personne ne devine.
2. Dire sur Photographic Reflexes, au survol ou à l'aperçu, qu'elle se consomme
   en jouant une carte glissée, et qu'elle ne se joue pas seule.
3. Et, plus largement : une carte en main qui n'est jamais jouable devrait
   pouvoir expliquer pourquoi. Le moteur sait déjà dire pourquoi une carte est
   refusée (le canal des refus, `refus_json`) ; il n'est pas branché ici.

## Une réserve

Le journal ne couvre que sa partie en bac à sable. Son « en prod tu ne peux
rien faire » porte peut-être sur une partie ordinaire qu'on n'a pas sous les
yeux. Dans celle-ci, tout marchait.

## Statut

**Diagnostiqué le 20/09/2026, non commencé.** Le joueur attend une réponse
depuis le 19/09 au soir : lui expliquer le geste est plus urgent que le
correctif d'ergonomie.


---

## REPRODUIT EN LABORATOIRE le 21/09/2026

Le doute de la section précédente (« son "en prod tu ne peux rien faire" porte
peut-être sur une partie ordinaire qu'on n'a pas sous les yeux ») est levé :
la position a été montée sur le vrai moteur, et le résultat est mesuré.

### La recette, pour qui voudra refaire

Harnais `tools/test_capacites.py`, scénario `rhino`, héros `echo`, sur un
dossier de jeu jetable copié de `.game-src`.

- `Puzzle.ChangeToFace('60037b', '60037a')` pour passer en forme héros.
  ⚠ On désigne la face **actuellement visible**, pas celle qu'on veut obtenir.
  Viser `60037a` fait lever une assertion du moteur : la face héros dort dans
  `world.aside_deck`, dont `GetOwner()` rend le VILAIN, et
  `GetControlByPlayer()` exige un joueur. Ce n'est pas un défaut d'Echo :
  vérifié à l'identique sur Venom (`20001a`, propriétaire Rhino). C'est
  l'idiome qui est piégeux.
- Main forcée : un événement d'aspect ou basique bon marché (`12033` Assess
  the Situation, coût 0), `60040a` Photographic Reflexes, et deux ressources.
- Jouer l'événement : « Watch and Learn » le glisse sous Echo.

### Ce que le moteur répond

**Forme HÉROS**, une carte glissée, Photographic Reflexes en main :

```
glissées sous Echo = ['12033']   12033 jouable = True
main = ['60040a', ...]           60040a jouable = False
```

**Forme CIVILE**, même position : `60040a jouable = False` également.

### Conclusion, et elle confirme le diagnostic du 20/09

**Photographic Reflexes n'est jouable dans aucune des deux formes, et ne se
défausse pas.** C'est le comportement voulu : la carte n'est pas une action du
joueur, elle se consomme toute seule quand on joue la carte glissée sous Echo,
laquelle est bien offerte (`jouable = True`).

Yarro décrivait donc l'inverse de la mécanique réelle, et **son expérience est
exacte** : il tenait une carte qu'il ne pouvait ni jouer ni défausser. Le
défaut est d'ergonomie, pas de moteur, et il est réel.

### L'observation est CONCLUE le 21/09/2026 : c'était un VRAI DÉFAUT

L'observation disait : « en forme **CIVILE**, la carte glissée est rapportée
`jouable = True` ». Les deux lectures proposées étaient toutes les deux
justes, et la mesure a tranché les deux.

#### 1. La mesure du 20/09 était fausse — et il faut savoir pourquoi

`face.CanPlayBy(joueur)` **ne peut pas** répondre à cette question.
`HasCost.CanPlayBy` (`src/game/card/face/attribute/has_cost.py`) pose
`self.card.can_state.is_like_in_hand = True` **avant** de filtrer les effets,
puis le remet à `None`. Il court-circuite donc exactement l'endroit où vit la
condition de forme : `check_tucked_playable`, branché sur le message
`CheckIfFaceIsLikeInHand`.

Mesuré, sur la position montée : `CanPlayBy` rend `True` dans les **trois**
états (forme héros, forme civile, retour en forme héros). Il aurait rendu
`True` même sur une carte qu'aucune règle n'autorise. **Ne jamais mesurer une
jouabilité avec `CanPlayBy`.** Le vrai chemin est `face.IsLikeInHand()`, qui
envoie le message, puis `EventManager.FilterAvailableEffects`.

#### 2. Mais le moteur laissait bel et bien jouer la carte en forme civile

Mesure par le vrai chemin, une carte glissée, Photographic Reflexes en main :

| état | `IsLikeInHand()` | effets de jeu offerts | attendu |
| --- | --- | --- | --- |
| forme HÉROS | `True` | 1 | ✅ |
| bascule en forme CIVILE | `True` | **1** | ❌ devrait être 0 |
| retour en forme HÉROS | `False` | **0** | ❌ devrait être 1 |

En vidant le cache à la main avant chaque lecture, on obtenait
`True / False / True`, c'est-à-dire la bonne réponse.

**Cause.** `card.can_state.is_like_in_hand` est un cache qui n'est remis à
zéro qu'au **déplacement** d'une carte (`card.py`, `MoveToArea`). Or la
réponse de `check_tucked_playable` dépend de deux choses qui bougent sans que
la carte glissée ne bouge : la **forme** du joueur et la présence de
**Photographic Reflexes** dans sa main. La toute première réponse restait donc
figée pour toute la vie de la carte sous Echo.

C'est un piège connu du moteur : Magik (`aoa/magik/45030a.py`) le contourne
déjà à la main, et le correctif « pack brawn » en tête de `Card.IsLikeInHand`
porte sur la même famille. Echo, elle, ne le contournait pas.

**Et c'est bien ce que le joueur a vécu.** La seconde moitié du tableau
(`retour en forme HÉROS → 0 effet`) dit mot pour mot son « en prod tu ne peux
rien faire » : un aller-retour en forme civile suffisait à éteindre
définitivement toutes les cartes glissées. Sa réserve du 20/09 est donc levée
dans l'autre sens : il n'y avait pas qu'un défaut d'ergonomie.

**Corrigé** le 21/09/2026 : `rafraichir_les_glissees` dans `60037a.py`, avec
ses trois témoins (`forme CIVILE`, `retour en forme HÉROS`, et le positif) dans
`tools/test_capacites.py`. Rapport complet :
`.planning/rapports/2026-09-21-echo-conclusion.md`.
