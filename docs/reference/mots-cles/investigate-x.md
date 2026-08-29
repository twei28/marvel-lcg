# Investigate X

**Texte imprimé / définition** : mot-clé maison du pack `jessica_jones`
(héroïne custom **Jessica Jones**, par « ekAugust »), porté par quatre des
cinq manigances secondaires du set de rencontre « On the Job ». Texte exact
lu dans `cards.json` sur * Chase Down a Lead (`jj013`) : « Investigate 2.
*(When revealed, move 2 threat from the main scheme to here.)* ». Le
gabarit `X[per_hero]` existe aussi : sur * Hang Back and Watch (`jj014`),
« Investigate 2[per_hero]. *(When revealed, move 2[per_hero] threat from
the main scheme to here.)* ».

**Mécanisme moteur** : composé dans `Investigate(value, *, per_hero=False)`
(`Fusion/marvel-lcg-src/src/cards/pack/jessica_jones/on_the_job/__init__.py`,
lignes 16-36), commune aux cartes du set qui portent le mot-clé :

```python
def Investigate(value: int, *, per_hero: bool=False) -> 'Ability':

    def investigate(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        amount = value
        if per_hero:
            amount *= Worlds.GetPlayerNumIcon(effect)

        main = Worlds.FindMainScheme(this)
        if main is None:
            return

        moved = this.RemoveThreatFromSchemes([main], amount, effect)
        if moved:
            this.PlaceThreatOnSchemes([this], moved, effect)

    return AbilityFactory.WhenThisRevealed(
        None,
        investigate,
    )
```

Aucune fabrique moteur ne porte ce mot-clé nativement : c'est un script
carte par carte, posé en tête de `GetAbilities()` de chaque carte
concernée. `AbilityFactory.WhenThisRevealed(None, investigate)`
(`game/ability/factory/reveal.py`, ligne 118) est la fabrique générique
« When Revealed » du moteur, sans condition ici (`None`). Le calcul en
deux temps suit le texte imprimé au mot près : `RemoveThreatFromSchemes`
retire d'abord `amount` de menace sur la manigance principale trouvée par
`Worlds.FindMainScheme` (`game/operate/worlds.py`, ligne 101), et renvoie
`moved`, la quantité réellement retirée ; seule cette quantité (jamais la
valeur demandée telle quelle) est ensuite posée sur la carte elle-même via
`this.PlaceThreatOnSchemes([this], moved, effect)`. `RemoveThreatFromSchemes`
et `PlaceThreatOnSchemes` sont deux méthodes génériques de `CardFace`
(`game/card/face/card_face.py`, lignes 641 et 567), pas des fabriques
propres au mot-clé : une manigance principale à 0 menace (ou déjà vidée par
un `RemoveThreatFromSchemes` précédent dans la même résolution) ne donne
donc rien, conformément au commentaire du fichier source (« une manigance
principale à 0 de menace ne doit rien donner »).

Le multiplicateur `per_hero` (`jj014`, `jj015`) multiplie `value` par
`Worlds.GetPlayerNumIcon(effect)` avant le retrait ; il ne change rien au
reste du mécanisme.

**Carte exemple** : `jj013` (* Chase Down a Lead), extrait de
`Fusion/marvel-lcg-src/src/cards/pack/jessica_jones/on_the_job/jj013.py` :

```python
return [
    Investigate(2),

    AbilityFactory.WhenSchemeBeDefeated(
        AbilityType.WhenDefeated,
        "This",
        when_defeated,
    ),
]
```

Trois autres manigances du set portent aussi `Investigate(...)` en tête de
leurs capacités, confirmé par grep sur le dossier
`Fusion/marvel-lcg-src/src/cards/pack/jessica_jones/on_the_job/` : `jj014`
(* Hang Back and Watch, `Investigate(2, per_hero=True)`), `jj015` (* Pore
Over the Evidence, `Investigate(1, per_hero=True)`) et `jj016` (* Sneak
Into the Crime Scene, `Investigate(2)`). La cinquième carte du set, `jj012`
(* Always a Bigger Conspiracy), ne porte pas le mot-clé : son texte imprimé
n'a pas de clause « When revealed », confirmé par lecture de son fichier
source et de son `text` dans `cards.json`, qui ne mentionnent aucun
« Investigate ».

**Pièges connus** : aucune fabrique moteur ne porte ce mot-clé nativement,
ne pas chercher du côté d'`AbilityFactory` standard. Le set de rencontre
« On the Job » lui-même (`data/encounter_sets/on_the_job.json`, cartes
`jj012` à `jj016`) est ajouté au deck Rencontre via
`message.encounter_set_names` dans `Message.WhenGameBeginSetup`,
enregistré en `RegisterTemp` depuis `WhenPlayerSelectHero` : ce point
d'accroche est nécessaire car `World.Begin` a déjà créé puis mélangé le
deck Rencontre à l'étape suivante, un `ShuffleAllTo` plus tardif arriverait
trop tard. Ce mécanisme d'ajout du set n'est pas propre au mot-clé
Investigate, mais conditionne l'apparition en jeu des cartes qui le
portent.

**Variantes maison** : aucune connue au 29/08/2026.
