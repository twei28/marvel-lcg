from . import *

# Dark Teleportation — custom « DesignHacker »
# Hero Action: Ready a friendly character. Then, if Dagger was readied this
#   way, remove 2 threat from a scheme.


def GetAbilities() -> Sequence['Ability']:

    def dark_teleportation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()

        cible = effect.targets[0]
        Faces.ReadyAll([cible], effect)

        if CardFinder(name=NOM_DAGGER, card_type=Hero).Check(cible):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 2 threat from a scheme",
                    lambda targets: this.RemoveThreatFromSchemes(list(targets), 2, effect),
                ).SetTarget(Scheme2),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            dark_teleportation,
        ).SetPlay()
        .SetTarget(Friend, canbe_ready=True),
    ]
