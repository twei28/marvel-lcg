# Reckless (mot-clé maison, aspect Determination)

**Texte imprimé / définition** : « Reckless. *(After this character enters
play, place 1 threat on each scheme.)* » (rappel imprimé sur `dt001`, `dt092`
et `dt100` ; `dt099` porte le mot nu).

Définition MC4DB (règle `fanmade`, `rules?locale=en`, 29/09/2026) : « When
this character enters play, place 1 threat on each scheme in play. » Même
mécanique ; seule la fenêtre diffère en mots (« when » contre « after »),
sans effet observable : le moteur n'offre qu'`AfterCardEnterPlay` pour ce
moment, et rien ne s'intercale entre l'entrée en jeu et la menace posée.

**Mécanisme moteur** : aucun crochet natif. Le mot-clé est une aptitude
écrite UNE fois, `Reckless()` dans
`src/cards/pack/determination/__init__.py`, et posée par chaque carte qui le
porte (`Reckless()` en tête de sa liste d'aptitudes) :

```python
def Reckless() -> 'Ability':
    def reckless(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        this.PlaceThreatOnSchemes("EachScheme", 1, effect)

    return AbilityFactory.AfterCardEnterPlay(
        AbilityType.ForcedResponse,
        "This",
        reckless
    )
```

`"EachScheme"` couvre la manigance principale ET toutes les annexes en jeu,
ce que disent les deux définitions (« each scheme », « each scheme in play »).

**Carte exemple** : `dt001` * Cable : `return [Reckless(), ...]`, puis son
Interrupt d'attaque. Autres porteurs : `dt092` * X-23, `dt099` * Marrow,
`dt100` * Archangel (qui cumule Alias et Retaliate 2).

**Pièges connus** :
- `CastTo(Ally)` : les quatre porteurs sont des alliés. Un futur porteur
  d'un autre type (soutien-personnage, héros) devra passer par
  `CastTo(Unit)` ou équivalent, sinon l'aptitude tombe.
- Le mot-clé n'est PAS lu dans `desc` (aucune clé `Reckless` dans
  `cards.json`) : une carte qui l'imprime sans appeler `Reckless()` est
  inerte. Vérifier le `.py` à chaque nouvelle carte, `verifier_desc_mots_cles`
  ne le voit pas.
- Réponse forcée : le joueur ne choisit ni de l'ignorer ni l'ordre avec une
  autre « after enters play » de la même carte (ex. `dt100` n'en a pas,
  `dt105` Venompool n'est pas Reckless). Aucun cas de conflit aujourd'hui.

**Variantes maison** : aucune. Le mot n'existe pas dans le jeu officiel ;
« Reckless Aggression » (`server_get.py`) est un nom de paquet d'aspect
préfait, sans rapport.
