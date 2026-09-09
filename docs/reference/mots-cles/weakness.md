# Weakness (mot-clé maison, ekAugust — aspect Venomized)

**Texte imprimé / définition** : « Weakness. *(Begins the game in your deck and
is discarded into your discard pile.)* »

L'insert du pack **Venomized** la donne en entier :

> **New Keyword: Weakness.** Cards with the "weakness" keyword begin the game
> shuffled into your deck and **do not count toward your deck size**. Cards
> that feature the "weakness" keyword are **encounter cards**, which will have
> a negative effect on your game **when they are drawn into your hand**. They
> can be **discarded like any other card** and they are **discarded into your
> discard pile**.

**Règle de construction de deck** (insert, section « Venomized Weakness Set ») :
après avoir bâti son deck, si l'on y a mis des cartes Venomized *(black)*, on
ajoute au hasard des cartes du set « Venomized Weakness », selon le **coût
total en ressources** de ces cartes Venomized :

| Coût total des cartes Venomized | Cartes Weakness à ajouter |
|---|---|
| 1 à 20 | 1 |
| 21 à 40 | 2 |

Les doublons sont possibles (tirage aléatoire, pas une sélection).

**Mécanisme moteur** : **AUCUN CODE**. C'est le résultat qui compte ici, et il
a été mesuré, pas supposé.

Le mot-clé se ramène à trois faits, dont deux sont natifs :

1. **Une carte de type `Treachery` peut vivre dans le deck du joueur.**
   `PlayerSetup.SelectIdentity` passe la liste `player_deck` telle quelle à
   `CardFactory.GenerateCards` (`player_setup.py:260`) : aucun filtre de type.
2. **Elle se pioche normalement en main**, et son
   `AbilityFactory.AfterCardEnterHand` part. Le déclencheur est celui de
   `bk002` * Sabretooth (pack `blink`), seul autre usage de cette fenêtre au
   dépôt.
3. **Elle se défausse comme n'importe quelle carte en main**, dans la défausse
   **du joueur**, à la fin de la phase du joueur. C'est le comportement natif
   d'une carte du deck joueur : rien à écrire.

> ### ✅ MESURÉ LE 09/09/2026, PAS SUPPOSÉ
>
> Deux cas de `tools/test_capacites.py` montent un deck joueur ne contenant
> que la carte, piochent, et lisent l'état :
>
> - `vz036 Flash Fire — MESURE du mot-cle WEAKNESS` : la carte arrive **en
>   main** et l'identité prend **1 dégât indirect**.
> - `vz037 Sensory Overload` : la carte arrive en main et le complot principal
>   passe de **3 à 4 menaces**.
>
> **Calibrage (§9 de `PROCESSUS-CARTE.md`)** : les deux modules retirés, les
> deux cas tombent — « degats sur 01001b = 0 (attendu 1) » et « menace sur
> 01097b = 3 (attendu 4) ». **2/2 avec, 0/2 sans.**

**Carte exemple** : `vz036` Flash Fire.

```python
def GetAbilities() -> Sequence['Ability']:

    def flash_fire(effect: 'Effect', message: 'Message.AfterCardEnterHand') -> None:
        this = effect.this
        joueur = this.GetControlByOrOwner()
        if not Player.IsType(joueur):
            return
        joueur.GetIdentity().TakeIndirectDamage(this, 1, effect)

    return [
        AbilityFactory.AfterCardEnterHand(
            AbilityType.ForcedResponse,
            "This",
            flash_fire,
        ),
    ]
```

**Pièges connus** :

- ⚠ **`which_card="This"` pose `CanWorkOnlyInHand()` tout seul**
  (`card_move.py`, fin de `AfterCardEnterHand`). L'ajouter à la main branche
  la capacité deux fois.
- ⚠ **« enters your hand » n'est pas « after you draw »** : une carte rendue
  en main par un autre effet déclenche aussi. Leçon déjà écrite dans `bk002`.
- ⚠ **La parenthèse « You may discard this card from your hand at the end of
  the player phase like any other card » ne se code pas.** C'est déjà le
  comportement de toute carte en main. La recoder ajouterait une règle en
  double.
- ⚠ **Ce n'est pas une Obligation.** Une obligation part dans le deck
  **rencontre** et se révèle par la phase du vilain ; une weakness vit dans le
  deck **joueur** et frappe à la pioche. Les deux sont des cartes de rencontre,
  et c'est tout ce qu'elles partagent.
- ✅ **La règle de deck-building EST automatisée** (09/09/2026). Ne plus écrire
  les cartes Weakness à la main dans un `player_deck` : elles y seraient en
  double. C'est le moteur qui les ajoute au montage de la partie.

**Règle de construction, automatisée des deux côtés :**

| Où | Quoi | Verrou |
|---|---|---|
| `PlayerSetup.CartesImposeesParLesAspects` (`src/game/player/element/player_setup.py`) | AJOUTE les cartes au deck, tirage semé, avant le mélange | `tools/test_aspect_determination.py` (bornes 1, 20, 21, 40, au-delà, et le témoin « aucun Venomized ») |
| `cartesImposees` (`public/js/deckbuilder/regles.js`) | ANNONCE le nombre dans l'éditeur | `outils/verifier-regles-deck.mjs` |

⚠ **La table des tranches est écrite DEUX FOIS**, une par côté. Si elle change,
elle change aux deux endroits. C'est précisément pourquoi les deux verrous
existent : la première version JS oubliait de multiplier le coût par le nombre
d'exemplaires, et la seconde tranche n'était jamais atteinte.

⚠ **Le tableau de l'auteur s'arrête à 40.** Au-delà, les deux implémentations
gardent la dernière tranche (2 cartes) plutôt que d'extrapoler « une de plus
par tranche de 20 », qui serait une règle inventée. Un deck de 50 cartes peut
dépasser 40 de coût cumulé : le cas est atteignable, et le choix est figé par
un cas de test pour qu'un changement d'avis soit un geste conscient.

⚠ **Un coût « X » vaut 0** des deux côtés : X se décide en jouant la carte, pas
en construisant le deck, et l'auteur parle du coût imprimé.

⚠ **Le tirage passe par `Random.RandomChoice`**, le générateur semé du moteur,
jamais par `random` : une partie rejouée à la même graine doit tirer les mêmes
faiblesses, sinon les rejeux et le multijoueur divergent. Tirage AVEC remise,
le texte autorisant les doublons.

**Mesure de bout en bout** : deck « Spider-Man (Venomized) », 39 cartes
choisies → `PlayerDeck<41> was created`. Témoin `spider_man`, 40 choisies →
`PlayerDeck<40>`. La règle n'ajoute rien à un deck qui n'emploie pas l'aspect.

**Variantes maison** : aucune à ce jour. Le set « Venomized Weakness » ne
compte que deux cartes, `vz036` Flash Fire et `vz037` Sensory Overload.
