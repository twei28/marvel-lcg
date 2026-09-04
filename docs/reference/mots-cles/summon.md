# Summon — MOT-CLÉ MAISON

**Texte imprimé / définition** : « **Summon** the Tahlei upgrade and add it to
your hand. », « **Summon** the Yaka Arrow upgrade and add it to your hand. »,
« **Summon** the Sword-Gun-Arm attachment and attach it to Sav'rkk. »,
« Otherwise, **summon** Sav'rkk and reveal him. »

**L'auteur ne le définit JAMAIS.** Le mot apparaît six fois dans le pack
`yondu` (set 154, BLUEHG + DESIGNHACKER) et **nulle part ailleurs dans le
jeu** : aucune carte officielle ne l'imprime, et les deux seules occurrences
du dépôt (`bw019` Rising Tide, `gb010` Necro-Raven) sont du texte
d'ambiance, pas une mécanique.

**Définition arbitrée par l'utilisateur le 03/09/2026** :

> « Summon X » = **fouiller votre deck ET votre défausse** pour la carte
> nommée X, la prendre, puis remélanger le deck. Côté rencontre, le même
> geste dans le deck de rencontre et sa défausse.

**Pourquoi cette lecture et pas une autre.** Le matériel l'impose : Tahlei
(14/15) et Yaka Arrow (15/15) **sont des cartes du deck de 15**, comptées
comme telles sur la decklist de l'auteur. Restreindre `summon` au seul deck
rendrait une Yaka Arrow défaussée définitivement perdue — or l'obligation
`Banished` la défausse explicitement, et **neuf cartes du pack** ne lisent
qu'elle. Le pack se bloquerait sur son propre texte.

**Mécanisme moteur** : **aucune primitive dédiée, mais rien à inventer** —
c'est exactement `Search.PlayerCard` :

```python
face = Search.PlayerCard(
    effect, initiator,
    include_player_deck=True,
    include_discard_pile=True,
    name="Yaka Arrow",
    card_type=Upgrade,
)
if face:
    initiator.GainCard(face, effect)
```

Le « (Shuffle.) » est le comportement PAR DÉFAUT de `Search`, il ne se code
pas. Modèles : `an001b` * Aldrif Odinsdottir, `ok001b` * Okoye, `ls005`
To Arms! (deck + défausse), `mw001b` * Cassandra Webb.

Côté rencontre, `Worlds.DiscardEncounterCardsUntil` ou
`CostFunc.SearchForCard(..., include_encounter_deck=True,
include_encounter_discard_pile=True)` selon la carte — modèle `ag013`
Hallucination.

**Carte exemple** : `yd001b` * Yondu Udonta — voir le `.py` correspondant, qui
porte le commentaire complet.

**Pièges connus** :

- ⚠ **« Summon … **and add it to your hand** » n'est PAS « put it into play ».**
  La carte va en MAIN et devra être jouée, coût compris. Trois cartes du pack
  l'écrivent ainsi ; `yd015` Sav'rkk et `yd016` Sword-Gun-Arm, elles, disent
  « and reveal him » / « and attach it », donc directement en jeu. Lire le
  verbe qui suit, jamais le seul mot `summon`.
- ⚠ **Ne pas oublier la défausse.** C'est la moitié de la définition, et
  celle sans laquelle le pack se bloque. Un cas de test qui ne monte que le
  deck passera au vert dans les deux montages : le contre-cas obligatoire
  place la carte cherchée **dans la défausse**.
- ⚠ **Si la carte est déjà en jeu, `summon` ne doit rien faire.** `yd004`
  Whistle While You Work l'écrit noir sur blanc (« If the Yaka Arrow upgrade
  is **not in play**, summon it … **instead** »), et les autres cartes le
  supposent. Chercher une carte déjà sur le terrain la dupliquerait.

**Variantes maison** : aucune autre à ce jour. À relire si un futur pack
imprime « summon » — la définition ci-dessus est un ARBITRAGE, pas une règle
officielle, et un autre auteur pourrait l'entendre autrement.
