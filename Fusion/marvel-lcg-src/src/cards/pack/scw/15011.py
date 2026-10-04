from . import *

# * Wiccan: William Kaplan

def GetAbilities() -> Sequence['Ability']:

    def wiccan(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        face = Worlds.DiscardEncounterTopCard(effect)
        if face:
            # "For each boost icon ... deal 1 damage to AN enemy" : sans "may",
            # une cible libre par icone, chacune obligatoire. `repeat` fait
            # afficher « (1/3) » au joueur (controller.py, prompt_text).
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 1 damage to an enemy",
                    lambda targets:
                        this.DealDamage(list(targets), 1, effect)
                ).SetTarget(Enemy),
                repeat=FacesCounter.CountTotalBoostIcons([face])
            )

    return [
        AbilityFactory.AfterUnitThwartEnd(
            AbilityType.Response,
            "This",
            wiccan
        ),
    ]

