# Iron Fist prévenait ses 2 dégâts à CHAQUE paquet, pas une fois par attaque

**Signalé par Yarro le 17/09/2026** (rapport n° 15) : « Iron Fist ne fonctionne
pas avec l'homme sable, qui assigne des dommages indirects. [...] il attaque à
deux, Iron Fist défend et active sa capa, un boost de 2 est révélé. Donc
normalement tu assignes 4 dommages et 2 sont tankés par la capa d'Iron Fist.
Sauf que là il tank les 4 au total. »

## Ce que le journal montrait

`62012 * Iron Fist` : « **Interrupt**: When Iron Fist defends against an enemy
attack, prevent damage from that attack equal to Iron Fist's ATK. » Son ATK
vaut 2 : deux dégâts, **pour l'attaque entière**.

L'Homme-Sable (`27061`) : « When Sandman attacks you, that attack deals
**indirect damage** ». Le joueur répartit donc les dégâts, et le moteur envoie
**plusieurs paquets** pour une même attaque. Round 2 de sa partie, dans
l'ordre :

```
Sandman gains Calling in Favors as boost card     (2 icônes)
Iron Fist defense against Sandman
Sandman would deal 2 damage to Iron Fist
  Iron Fist will take 2 damage
  Prevented 2 of this damage (Iron Fist)
Sandman would deal 2 damage to Star-Lord
  Star-Lord will take 2 damage
  Prevented 2 of this damage (Iron Fist)          ← deuxième fois
```

Quatre dégâts, quatre prévenus. Yarro avait raison sur le fait, et sa lecture
« les boosts ne sont pas pris en compte » visait juste à côté : le boost était
bien compté, c'est la prévention qui se rejouait.

## La cause

```python
effect.this.effect.RegisterTemp(..., unregister_after_exec=False, ...)
```

L'interruption restait armée après s'être exécutée. Sur une attaque ordinaire
(un seul paquet) cela ne se voit pas ; sur une attaque indirecte, elle se
déclenche autant de fois qu'il y a de paquets.

## Le correctif

Un budget, décompté : `restant = [this.attack]`, et à chaque paquet on ne
demande que `min(restant, will_take_damage)`. Le plafond compte autant que le
budget : sans lui, un paquet de 1 mangerait les deux points.

`PreventDamage` rend ce qu'il a prévenu, c'est cette valeur qui est décomptée.

## ⚠ Ce qui n'est PAS prouvé

`tools/test_capacites.py` reçoit un cas **nominal** : sur une attaque
ordinaire, Iron Fist prévient bien 2 dégâts. Il protège ce qui marchait.

**Le défaut signalé n'a PAS de cas.** Il demande une attaque à dégâts indirects,
donc plusieurs paquets. Le cas écrit pour cela — scénario `sandman`, Iron Fist
en défense — donnait **le même résultat avec et sans le correctif** : les
boosts sont tirés au hasard, et l'attaque n'a produit qu'un paquet. Il a été
retiré plutôt que gardé vert.

Le diagnostic, lui, ne tient pas à ce cas : il tient au journal du joueur, où
« Prevented 2 » apparaît deux fois pour une attaque, et à
`unregister_after_exec=False` qui l'explique mot pour mot.

À reprendre si le harnais sait un jour forcer un boost et la répartition d'une
attaque indirecte.

## Statut

**Corrigé le 17/09/2026.** Correctif dans le MOTEUR : effet à la prochaine
table ouverte. Non déployé.
