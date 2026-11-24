from . import *

# Askani's Prophecies — EVENEMENT, cout 2 (wild), TEMPORAL.
# Alter-Ego Action: Ready Rachel Summers. Heal 1 damage from Rachel Summers. Change your form.
#
# CARTES DE REFERENCE : `01025` Split Personality (`ChangeToOtherIdentityForm`), `27032` Double Life (`ChangeToOtherForm`,
# `Faces.ReadyAll([identite])`), `16040` (`this.HealthUnits(cibles, 1, effect)`).
#
# MOTS-PIEGES : trois phrases EN ORDRE : redresser, soigner, puis changer de forme. L'identite se relit AVANT le changement
# (apres, `GetIdentity()` rend l'autre face).
def GetAbilities() -> Sequence['Ability']:
    def askanis_prophecies(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        initiator = effect.GetInitiator()
        identite = initiator.GetIdentity()
        Faces.ReadyAll([identite], effect)
        this.HealthUnits([identite], 1, effect)
        identite.ChangeToOtherForm(effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            askanis_prophecies,
        ).SetPlay().SetLabel(),
    ]
