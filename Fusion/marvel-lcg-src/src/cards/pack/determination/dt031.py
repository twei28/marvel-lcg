from . import *

# Act on Impulse

def GetAbilities() -> Sequence['Ability']:

    def act_on_impulse(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        # « a status card » sans plus : les trois statuts du moteur sont offerts,
        # et le joueur choisit aussi le personnage.
        initiator.ChooseAbilities(
            effect,
            *[
                AbilityFactory.ForChoiceAbility(
                    "Give a character a %s status card" % statut.lower(),
                    lambda targets, statut=statut:
                        Faces.GiveStatus(targets, statut, effect)
                ).SetTarget("Character")
                for statut in ("Tough", "Stunned", "Confused")
            ]
        )

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            act_on_impulse,
            to_form=Hero,
        ).SetPlay(),
    ]
