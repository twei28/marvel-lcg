from . import *

# * Spider-Girl

def GetAbilities() -> Sequence['Ability']:

    def choisir(effect: 'Effect') -> None:
        # « Response: After Spider-Girl enters play or leaves play, choose:
        #   • Ready your hero.  • Heal 1 damage from your alter-ego. »
        this = effect.this.CastTo(Ally)
        joueur = effect.GetInitiator()

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Ready your hero",
                lambda cibles: Faces.ReadyAll([joueur.GetIdentity()], effect),
            ),
            AbilityFactory.ForChoiceAbility(
                "Heal 1 damage from your alter-ego",
                lambda cibles: this.HealthUnits([joueur.GetIdentity()], 1, effect),
            ),
        )

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            lambda effect, message: choisir(effect)
        ),
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.Response,
            "This",
            lambda effect, message: choisir(effect)
        ),
    ]
