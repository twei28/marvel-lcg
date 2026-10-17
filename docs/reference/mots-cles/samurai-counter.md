# Jeton « samurai counter » et trait OATH (TMNT Shinobi, Inkwire)

**Texte imprimé / définition** : les améliorations **OATH** du type Bushido s'impriment « *Uses (3 samurai counters).* »
(livret p.5 : Rectitude, Self-Control, Devotion). Le Path du Samurai agit sur eux : « *Way of the Warrior* —
Hero Action : Exhaust this card and remove a total of 2 samurai counters from among OATH upgrades you control → ready your
hero and draw 1 card. » Un « samurai counter » est un compteur nommé, sans règle propre (comme `doubt`, `charge`...).

**Mécanisme moteur** : le compteur `'samurai'` est dans `CardFace.COUNTER` (`card_face.py`, ajouté pour `tj006` de Jennika,
16/10/2026) ; le trait `OATH` (et `SENPAI`) est déclaré dans `CardFace.TRAITS` (17/10/2026). `Uses` est NATIF
(`desc.Uses = "3,samurai"`, fiche `uses.md`) : le moteur pose les compteurs à l'entrée en jeu et fait sortir la carte au
dernier compteur retiré. Le plateau affiche le compteur (« samouraï », `compteurs-fr.ts`, déjà en place).

Retirer des compteurs :
- sur la carte elle-même : `CostFunc.Counter("This", n, 'samurai')` (modèle `tj006`) ;
- **réparti entre plusieurs cartes** (« a total of 2 ... from among OATH upgrades you control », `se003`) :
  `CostFunc.Custom(Select.From("This", finder=CardFinder(check_effect_fn=assez)), retirer)` où `assez` somme les compteurs des
  `joueur.GetControlUpgrade(CardFinder(trait="OATH"))` et `retirer` en retire UN à la fois, au choix du joueur
  (`Faces.RemoveCountersOn([carte], 1, 'samurai', effect)`).

**Carte exemple** : `se003` Samurai (coût réparti), `tj006` Fearless Resolve (coût sur la carte).

**Pièges connus** :
- compter seulement les améliorations OATH SOUS SON CONTRÔLE ; des compteurs samurai sur une carte sans le trait OATH ne
  paient rien (cas `[se] se003`) ;
- 1 compteur au total ne suffit pas pour un « total of 2 » (l'action n'est pas proposée) ;
- une amélioration OATH qui perd son dernier compteur est défaussée (`Uses`), donc retirer 2 compteurs d'une amélioration à
  2 compteurs la défausse ;
- le livret dit « once per turn » pour Way of the Warrior : la carte s'incline, ce qui réalise la limite.

**Variantes maison** : tout est maison.
