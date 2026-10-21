from . import *

# * Punisher — SBIRE ELITE. ELITE. VIGILANTE. SCH 0, ATQ 1, 7 PV, Boost 3. Steady. Toughness. Villainous.
# « Punishment » — Special : voir __init__.py (`Punishment`).
#
# Cartes de reference : sm/sinister_six/27100b.py (`WhenResolveSpecialAbility(...).SetName(...)`).
# Steady, Toughness, Villainous : natifs (`desc`). Les cartes du set appellent `Punishment()` (fonction) : meme effet,
# sans dependre de la presence de cette carte ; l'aptitude nommee la rend aussi disponible par `ResolveSpecialAbility`.

def GetAbilities() -> Sequence['Ability']:

    def punishment(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Punishment(effect, effect.this.CastTo(Enemy))

    return [
        AbilityFactory.WhenResolveSpecialAbility("This", punishment).SetName("Punishment"),
    ]
