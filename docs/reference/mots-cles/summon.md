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

**Définition** (glossaire fan-made de MC4DB, adoptée le 29/09/2026 ; elle
englobe l'arbitrage du 03/09/2026) :

> « Search the deck, discard pile, or **anywhere in or out of play** for a
> specific card, then shuffle the deck if it was searched in this way. Summon
> predates the official Find keyword, which covers almost the same ground:
> both reach every game area where the named card could be. »

⚠ **Ce qui a changé le 29/09/2026.** L'arbitrage du 03/09/2026 (deck ET
défausse) était un sous-ensemble : les helpers fouillent désormais aussi la
main, la mise de côté et la zone « retiré de la partie » (cas « depuis la zone
RETIREE DE LA PARTIE », rouge avant, côté héros comme côté rencontre). Le
TERRAIN n'est pas fouillé : chaque carte du pack qui convoque une carte
pouvant déjà être en jeu le dit elle-même (« if ... is not in play »), et
`yd004` interdit la duplication en toutes lettres.

**Pourquoi la défausse compte.** Le matériel l'impose : Tahlei
(14/15) et Yaka Arrow (15/15) **sont des cartes du deck de 15**, comptées
comme telles sur la decklist de l'auteur. Restreindre `summon` au seul deck
rendrait une Yaka Arrow défaussée définitivement perdue — or l'obligation
`Banished` la défausse explicitement, et **neuf cartes du pack** ne lisent
qu'elle. Le pack se bloquerait sur son propre texte.

**Mécanisme moteur** : **aucune primitive dédiée, mais rien à inventer** —
c'est `Search.SearchForCards`, qui expose toutes les zones :

```python
faces = Search.SearchForCards(
    effect, joueur,
    include_player_deck=True,
    include_player_discard_pile=True,
    include_player_hand_cards=True,
    include_set_aside=True,
    include_removed_area=True,
    name="Yaka Arrow",
    card_type=Upgrade,
)
if faces and faces[0] not in joueur.hand_cards.Get():
    joueur.GainCard(faces[0], effect)
```

Le « (Shuffle.) » est le comportement PAR DÉFAUT de `Search`, il ne se code
pas. Modèles : `an001b` * Aldrif Odinsdottir, `ok001b` * Okoye, `ls005`
To Arms! (deck + défausse), `mw001b` * Cassandra Webb.

Côté rencontre, `Search.SearchForCards(..., include_encounter_deck=True,
include_encounter_discard_pile=True, include_set_aside=True,
include_removed_area=True)` (`ConvoquerRencontre`, set `yondu_nemesis`) —
modèle `ag013` Hallucination pour le motif « chercher puis attacher ».

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

**Variantes maison** : aucune autre à ce jour. La définition ci-dessus est
celle du glossaire MC4DB ; un futur pack qui imprimerait sa propre parenthèse
l'emporterait sur elle (texte imprimé > MC4DB > fiche).
