from . import *

# * Kate's Bow — WEAPON, Restricted
# Your basic attacks gain ranged.
# Interrupt: At the end of the player phase, place 1 arrow counter on this
#   card. (Max of 10 arrow counters here.)
#
# « Your basic attacks gain ranged » : modele Hawkeye's Bow (trors/hawkeye/
# 04026.py), meme `WhenUnitWouldAttack(..., "YourHero", lambda e, m:
# m.GainRanged(e), is_basic_attack=...)`, sans la restriction de trait ARROW
# (Kate's Bow le donne a TOUTES les attaques de base, pas seulement aux
# fleches).
#
# Le compteur de fin de phase joueur : `AbilityFactory.WhenPlayerPhaseEnd`
# (turn_phase.py), modele deadpool/44032.py (meme message, en ForcedResponse
# la-bas ; Interrupt ici, texte imprime).


def GetAbilities() -> Sequence['Ability']:

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.PlaceCountersOn([this], 1, 'arrow', effect, maximum=10)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.NonKeyword,
            "YourHero",
            lambda effect, message: message.GainRanged(effect),
            is_basic_attack=True,
        ),
        AbilityFactory.WhenPlayerPhaseEnd(
            AbilityType.Interrupt,
            fin_de_phase,
        ),
    ]
