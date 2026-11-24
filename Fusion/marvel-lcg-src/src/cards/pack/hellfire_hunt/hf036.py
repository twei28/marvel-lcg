from . import *

# Crisis of Faith (POTENTIAL ALLY, Oya). Victory 1.
# Threat cannot be removed from other side scheme in play from thwarting.
# When Defeated : Oya.
#
# Carte de reference : 27104 Taunting Presence (`AbilityFactory.ThreatCannotBeRemovedFromWhile`), `by_thwarting=True`.
# ⚠ « OTHER side scheme » : toute manigance annexe SAUF celle-ci (sinon elle ne pourrait jamais etre defaite) ; « from thwarting » : un
# effet qui retire de la menace sans contrer reste possible.
def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            SchemeSide2,
            by_thwarting=True,
            conditions=[
                lambda effect, message:
                    message.trigger != effect.this,
            ],
        ),
        AbilitePotentialAlly("Oya"),
    ]
