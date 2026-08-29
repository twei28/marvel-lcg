from . import *

# Regenerative Longevity
# Action: Heal a total of 4 damage from your identity and Honey Badger.
#
# Copie de Regenerative Longevity (43006). Le modele bornait deja l'identite
# au controleur ; on fait pareil pour Honey Badger, qui n'a pas un nom unique
# a la table.


def GetAbilities() -> Sequence['Ability']:

    def regenerative_longevity(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        this.HealthUnits(effect.targets, 1, effect)

    def find(effect: 'Effect', face: 'CardFace') -> bool:
        if face.GetControlByPlayer() != effect.GetInitiator():
            return False
        if Identity.IsType(face):
            return True
        if face.IsName(NOM_SOEUR):
            return True
        return False

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            regenerative_longevity
        ).SetPlay().SetLabel()
        .SetTarget("YouControlUnit", check_fn=find, repeat_rules="Sustained", range=(1, 4)),
    ]
