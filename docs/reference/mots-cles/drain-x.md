# Drain X

**Texte imprimé / définition** : mot-clé maison du pack `agent_anti_venom`,
utilisé tel quel sur Unlikely Allies (« Drain 2 from an enemy ») et Bear
Arms (« drain 1 from the villain »), mais **jamais défini sur les cartes
fournies** (aucun insert dans les trois dossiers Drive du pack, rien trouvé
en ligne). Lecture arrêtée avec l'utilisateur le 4/8/2026, faute de mieux :
X dégâts à l'ennemi ciblé, puis X soins sur Agent Anti-Venom, et sur lui
seul (pas sur l'allié qui déclenche l'effet s'il est distinct du héros).

**Mécanisme moteur** : centralisé dans `Drain()` du `__init__.py` du set
`agent_anti_venom` (`Fusion/marvel-lcg-src/src/cards/pack/agent_anti_venom/agent_anti_venom/__init__.py`) :

```python
def Drain(source: 'CardFace', targets: Sequence['CardFace'], value: int, effect: 'Effect') -> None:
    """X degats a l'ennemi, puis X soins sur Agent Anti-Venom."""
    if not targets:
        return
    source.DealDamage(targets, value, effect)
    identity = GetAgentAntiVenom(effect)
    if identity is not None:
        source.HealthUnits([identity], value, effect)
```

`GetAgentAntiVenom(effect)` remonte l'identité du joueur qui résout l'effet
via `effect.GetInitiator().GetIdentity()`, quelle que soit sa face (Hero ou
Alter-Ego) : c'est ce qui garantit que les soins vont bien sur Agent
Anti-Venom lui-même, jamais sur la carte source de l'effet (Bear Arms,
Unlikely Allies). Chaque carte appelle `Drain(source, targets, X, effect)`
avec son propre `X` : pas de champ `desc` dédié, la valeur est en dur dans
le script de chaque carte.

**Carte exemple** : `av009` (Bear Arms), extrait de
`Fusion/marvel-lcg-src/src/cards/pack/agent_anti_venom/agent_anti_venom/av009.py` :

```python
def bear_arms_drain(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
    this = effect.this.CastTo(Upgrade)
    Drain(this, effect.targets, 1, effect)
```

`av007` (Unlikely Allies) appelle la même fonction avec `value=2`, dans une
des quatre branches ouvertes selon l'icône de ressource imprimée de la
carte défaussée (« [physical] - Drain 2 from an enemy. ») :

```python
def _drain(initiator: 'Player', source: 'CardFace', effect: 'Effect') -> 'Ability':
    return AbilityFactory.ForChoiceAbility(
        "Drain 2 from an enemy",
        lambda targets:
            Drain(source, targets, 2, effect)
    ).SetTarget(Enemy)
```

**Pièges connus** : mot-clé maison non défini sur les cartes fournies par
l'auteur : sa lecture (dégâts puis soin de X sur l'identité) est une
convention retenue avec l'utilisateur, pas une règle imprimée à faire
confiance aveuglément. Toute nouvelle carte qui reprend « drain X » doit
déclencher systématiquement une question à l'utilisateur pour confirmer
que la même lecture s'applique (voir `PROCESSUS-CARTE.md`, tableau « en
cas de doute »), avant d'appeler `Drain()` sans vérifier. Autre piège
local, propre à Bear Arms : le « next attack gains ranged » de sa première
capacité n'a pas de mécanisme « prochaine attaque » dans le moteur ; il est
simulé par une capacité temporaire `UnitAttackGainKeyword` posée sur
l'identité et retirée dès sa première exécution (`unregister_after_exec`),
sans lien direct avec `Drain()`.

**Variantes maison** : aucune connue au 29/08/2026.
