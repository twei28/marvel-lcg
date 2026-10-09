from . import *

# hs107b Acquiring Targets
# Forced Interrupt : quand un joueur passe en forme heros, 2 menaces ici.
# Forced Response : apres qu'un joueur passe en alter-ego, retire 1 menace ici.

def GetAbilities() -> Sequence['Ability']:

    def vers_heros(effect: 'Effect', message: 'Message.WhenUnitWouldChangeForm') -> None:
        effect.this.PlaceThreatOnSchemes([effect.this], 2, effect)

    def vers_alter_ego(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        effect.this.RemoveThreatFromSchemes([effect.this], 1, effect)

    return [
        AbilityFactory.WhenUnitWouldChangeForm(AbilityType.ForcedInterrupt, None, vers_heros, to_form=Hero),
        AbilityFactory.AfterUnitChangeForm(AbilityType.ForcedResponse, None, vers_alter_ego, to_form=AlterEgo),
    ]
