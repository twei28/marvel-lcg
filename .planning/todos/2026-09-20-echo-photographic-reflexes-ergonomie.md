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
