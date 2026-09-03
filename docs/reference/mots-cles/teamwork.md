# Teamwork (TRAIT)

**Texte imprimé / définition** : `Teamwork ([[TRAIT]])`. Après qu'un sbire
portant Teamwork entre en jeu et s'engage avec un joueur, s'il y a **au moins
un AUTRE sbire en jeu qui porte le trait cité**, le sbire qui vient d'arriver
**s'active** contre le joueur avec lequel il est engagé (il attaque ou
manigance immédiatement, comme en phase du vilain).

Le mot-clé transforme donc une arrivée de sbire en attaque immédiate dès que
la bande est constituée. Le trait entre parenthèses n'est pas forcément celui
du sbire lui-même, même si dans les 31 cartes officielles qui le portent,
c'est toujours le cas.

**Mécanisme moteur** : **entièrement natif, aucun script à écrire.** Il se
déclare dans `desc` :

```json
"desc": { "HP": "5", "ATK": "3*", "SCH": "1", "Teamwork": "ASGARD" }
```

`src/game/card/face/attribute/can_teamwork.py` fait le reste :
`RegisterAttribute("Teamwork", "printed_teamwork", str)` lit la valeur, puis
`CanTeamwork.OnAfterCardEnterPlay` cherche un autre sbire du terrain qui
porte le trait (`minion.HasTrait(*self.teamwork)`) et déclenche
`minion.DoActivate(minion.GetEngagedPlayer(), Teamwork(minion))`.

**Carte exemple** : `32159` * Fabian Cortez (set Acolytes) : `"Teamwork":
"ACOLYTE"` dans `desc`, et son `.py` ne contient QUE sa capacité
« When Defeated » — pas une ligne pour Teamwork. Voir aussi `38029` Donald
Pierce et `38030` Skullbuster (set Reavers), même montage.

**Pièges connus** :

- ⚠ **Ne jamais l'écrire en script.** C'est la même famille de pièges que
  `Toughness` et `Restricted` : une base lue directement dans `desc`. Un
  module qui la recoderait ferait s'activer le sbire DEUX fois.
- ⚠ **Le trait cité doit exister dans l'énum `TRAITS`**
  (`src/game/card/face/card_face.py`). `CheckPrintedValue` lève un `assert
  IsTrait(self.printed_teamwork)` : un trait maison non déclaré fait tomber
  la carte à la construction, pas en jeu.
- ⚠ **Le déclencheur est l'ENTRÉE EN JEU, pas l'engagement.** Un sbire déjà
  en jeu quand un second arrive ne se réveille pas de lui-même sous la règle
  actuelle : c'est le NOUVEAU venu qui s'active.
- ⚠ **Deux règles cohabitent dans le moteur**, selon `world.rule.v16_teamwork`
  (`src/game/world/world_rule.py:38`, **`False` par défaut**) :
  - règle par défaut (pré-1.6) : **tous** les sbires dont le `teamwork`
    correspond s'activent, pas seulement celui qui arrive ;
  - `v16_teamwork = True` : **seul** le sbire qui vient d'entrer s'active.
  Un test qui compte les dégâts doit donc savoir sous quelle règle il tourne.
- Le sbire qui arrive s'active contre **son** joueur engagé, pas contre le
  premier joueur.

**Variantes maison** : aucune à ce jour. Le pack `lady_sif` (Rainy, set 150)
est le premier contenu maison à l'imprimer, sur `ls015` Skurge —
`Teamwork (ASGARD)` — et il a exigé l'ajout du trait `TEMPTATION` à l'énum
pour ses deux attachements, mais pas d'`ASGARD`, déjà présent.
