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

> ## ⚠ DEUX DÉFINITIONS COEXISTENT DEPUIS LE 29/09/2026
>
> Le glossaire fan-made de MC4DB dit :
>
> > « When this keyword is triggered by a character, deal X damage to that
> > character's target. Then, **if the target took that damage**, heal X
> > damage from the character who triggered drain. »
>
> Règle de priorité fixée par l'utilisateur : texte imprimé > MC4DB > fiche.
> - `venompool` **imprime** sa définition (insert ci-dessus, soin
>   inconditionnel sur l'identité) : il la garde. Divergence assumée avec
>   MC4DB, notée ici, pas dans le script.
> - `agent_anti_venom` n'imprime rien : son helper suit MC4DB, le soin n'a
>   lieu que si l'ennemi a **subi** les dégâts (un Tough les absorbe : pas de
>   soin). Cas « av009 ... vilain TOUGH », rouge avec l'ancien helper.
> - « the character who triggered drain » : sur les quatre cartes du dépôt,
>   c'est toujours l'identité (aucun allié ne déclenche un drain). Sans
>   effet aujourd'hui, à relire si un allié imprime le mot.
> - « a subi » se lit sur les **points de vie** (ou la défaite) de la cible,
>   pas sur le retour de `DealDamage`, qui compte les dégâts INFLIGÉS avant
>   prévention et rendait 1 face à un Tough.

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
    if not targets:
        return
    avant = {cible: cible.health for cible in targets if hasattr(cible, "health")}
    source.DealDamage(targets, value, effect)
    subis = any(cible.health < sante or cible.IsDefeated() or not cible.IsInPlay()
                for cible, sante in avant.items())
    if not subis:
        return
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

**Pièges connus** : chaque pack garde son **propre** helper `Drain()`, et
depuis le 29/09/2026 les deux corps DIFFÈRENT (soin conditionnel côté
`agent_anti_venom`, inconditionnel côté `venompool`, voir l'encadré). Deux
raisons de ne pas les fusionner : l'identité soignée n'est pas la même, et un
pack custom ne doit pas dépendre d'un autre pack custom (un joueur peut très
bien avoir installé l'un sans l'autre). Autre piège
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
