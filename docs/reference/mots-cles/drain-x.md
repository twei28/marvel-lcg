# Drain X

> ## ✅ LE MOT-CLÉ EST DÉFINI PAR ÉCRIT DEPUIS LE 31/08/2026
>
> L'insert du pack `venompool` (« Venompool Insert.png », CptScorp, Cycle 2)
> le définit noir sur blanc, et c'est **mot pour mot** la lecture retenue à
> l'aveugle le 4/8/2026 pour `agent_anti_venom` :
>
> > « When an ability instructs you to drain X from an enemy, deal X damage
> > to that enemy, then heal X damage from your identity. »
>
> La convention n'est donc plus une supposition arbitrée faute de mieux :
> elle a une source imprimée, et les deux packs la rendent à l'identique.
> La question systématique à l'utilisateur, exigée par la version précédente
> de cette fiche avant tout nouvel appel à `Drain()`, **n'a plus lieu d'être**
> tant qu'une carte reprend le mot-clé sans le modifier.

**Texte imprimé / définition** : mot-clé maison, apparu dans le pack
`agent_anti_venom` — Unlikely Allies (« Drain 2 from an enemy ») et Bear
Arms (« drain 1 from the villain ») — où il n'était **défini nulle part**
(aucun insert dans les trois dossiers Drive du pack, rien trouvé en ligne).
Le pack `venompool` a fourni la définition imprimée (encadré ci-dessus) :
X dégâts à l'ennemi ciblé, puis X soins sur l'identité du joueur qui résout
l'effet, et sur elle seule (pas sur l'allié qui déclenche l'effet s'il est
distinct du héros).

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

**Pièges connus** : chaque pack garde son **propre** helper `Drain()`, au
corps volontairement identique — `venompool` ne réutilise pas celui
d'`agent_anti_venom`. Deux raisons : l'identité soignée n'est pas la même,
et un pack custom ne doit pas dépendre d'un autre pack custom (un joueur
peut très bien avoir installé l'un sans l'autre). Autre piège
local, propre à Bear Arms : le « next attack gains ranged » de sa première
capacité n'a pas de mécanisme « prochaine attaque » dans le moteur ; il est
simulé par une capacité temporaire `UnitAttackGainKeyword` posée sur
l'identité et retirée dès sa première exécution (`unregister_after_exec`),
sans lien direct avec `Drain()`.

**Variantes maison** : le pack `venompool` (CptScorp, set 129) reprend le
mot-clé sans le modifier, sur deux cartes — `vp009` Klyntar Suit (« drain 1
from the attacking enemy », Response après avoir subi des dégâts d'une
attaque) et `vp010` True Form (« Drain 1 from that enemy », Interrupt sur
une attaque de base). Helper local dans
`Fusion/marvel-lcg-src/src/cards/pack/venompool/venompool/__init__.py`.
