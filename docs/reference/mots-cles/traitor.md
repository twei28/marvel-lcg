# Traitor

**Texte imprimé / définition** : mot-clé maison du pack nemesis
`agent_anti_venom` (« Agent Anti-Venom Nemesis »), défini en toutes lettres
sur les deux cartes qui le posent, contrairement à `drain X`. Texte exact
lu dans `cards.json` sur The Made Men (`av014`) et * Infected Scorpion
(`av015`) : « gains traitor *(treat that ally as a minion engaged with its
owner. It has 1 SCH, a blank printed text box, and does not take
consequential damage.)* ».

**Mécanisme moteur** : rendu par `TreatAsMinion`
(`game/ability/factory/treat.py`), une fonction déjà présente dans le
moteur (utilisée nativement par Manipulated Mind 27171 et « Lost » Child
47027) mais que le moteur n'exposait jusque-là que depuis un attachement,
via `AfterCardGainUpgrade`. Ici le déclencheur est une capacité de carte
(Forced Interrupt), pas un attachement posé sur l'allié : le pack appelle
donc directement `TreatAsMinion` hors du chemin standard. Extrait de
`Fusion/marvel-lcg-src/src/cards/pack/agent_anti_venom/agent_anti_venom_nemesis/__init__.py` :

```python
from game.ability.factory.treat import TreatAsMinion

TRAITOR_TEMPLATE = "Traitor Minion"


def _sch_a_un(minion: Any, ally: Any, effect: 'Effect') -> None:
    minion.printed_scheme = 1


def GainTraitor(ally: 'CardFace', effect: 'Effect') -> bool:
    """Transforme un allie en sbire engage avec son proprietaire."""
    player = ally.CastTo(Ally).GetControlByPlayer()
    if player is None:
        return False
    return TreatAsMinion(ally, TRAITOR_TEMPLATE, player, effect, process=_sch_a_un)
```

`GainTraitor` s'appuie sur la carte-gabarit `aav_traitor_minion`
(« Traitor Minion ») pour la conversion, et force le SCH à 1 via le
callback `process=_sch_a_un` (le gabarit ne porte pas nativement ce SCH).
Le commentaire du fichier précise l'import : `TreatAsMinion` est une
fonction de module, pas une méthode d'`AbilityFactory`, donc non
réexportée par le `from game.ability.factory import *` de
`cards/pack/__init__.py` ; il faut l'importer explicitement.

**Carte exemple** : `av015` (* Infected Scorpion), extrait de
`Fusion/marvel-lcg-src/src/cards/pack/agent_anti_venom/agent_anti_venom_nemesis/av015.py` :

```python
def infected_scorpion(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
    this = effect.this.CastTo(Minion)
    Unused(this)

    cible = message.target
    if cible is None or not Ally.IsType(cible):
        return

    def prevenir(effect2: 'Effect', message2: 'Message.WhenUnitWouldTakeDamage') -> None:
        message2.PreventDamage("All", effect2)

    cible.effect.RegisterTemp(
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Temp0,
            "This",
            prevenir,
            is_from_attack=message.would_atk_message,
        ),
        unregister_after_exec=True,
    )

    GainTraitor(cible, effect)
```

`av014` (The Made Men, side scheme nemesis) appelle la même `GainTraitor`
sur l'allié au plus haut ATK imprimé de chaque joueur, après chaque
schéma/attaque de Maniac.

**Pièges connus** : le déclenchement hors attachement est la partie non
standard du montage. Une implémentation naïve qui se contente d'écouter
`AfterCardGainUpgrade` (le seul chemin par lequel `TreatAsMinion` était
exposé jusque-là) rate entièrement le cas `traitor`, puisqu'ici aucun
attachement n'est posé sur l'allié : il faut appeler `TreatAsMinion`
directement depuis la capacité de la carte source (Forced Interrupt ou
Forced Response), comme le fait `GainTraitor`. Piège annexe propre à
Infected Scorpion : la capacité écoute `WhenUnitWouldAttackUnit`, pas
`WhenUnitWouldAttack` (à ce dernier moment l'attaque vise encore le
joueur, le défenseur n'est pas désigné, et `attacked_targets` ne contient
jamais d'allié).

**Variantes maison** : `TreatAsAlly` de Totally Awesome Hulk
(`tah_hellbender_ally`, pack `totally_awesome_hulk`) est le même genre de
montage (« traiter une carte comme si »), à inspecter si un futur pack a
besoin d'un « traiter comme » différent de `traitor`.
