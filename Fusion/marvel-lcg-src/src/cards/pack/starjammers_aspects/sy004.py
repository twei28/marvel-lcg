from . import *
# * Sikorsky (Basic, allie 2 [mental], 1*/1*, PV 2). AERIAL. PSIONIC. STARJAMMER.
# Response: After Sikorsky enters play, heal 1 damage from a character.
#
# Carte de reference : 45048 Triage (`AfterCardEnterPlay(Response, "This")` + `HealthUnits(targets, N)` + `canbe_heal=True`).
# Difference : « a CHARACTER » sans trait ni « friendly » : tout personnage soignable (allie, identite, mais aussi un ennemi).
def GetAbilities() -> Sequence['Ability']:
    def sikorsky(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        this.HealthUnits(effect.targets, 1, effect)
    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            sikorsky,
        ).SetTarget(Unit2, canbe_heal=True),
    ]
