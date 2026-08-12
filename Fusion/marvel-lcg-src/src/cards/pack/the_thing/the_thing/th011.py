from . import *

# Annual Shedding — custom « DesignHacker » (obligation de The Thing)
# Give to the Ben Grimm player. Flip to alter-ego form. Choose one:
# - Discard a tough status card from Ben Grimm -> discard this obligation.
# - Stun or confuse Ben Grimm -> discard this obligation.

def GetAbilities() -> Sequence['Ability']:

    def annual_shedding(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        identity = player.GetIdentity()
        if player.IsHero():
            identity.ChangeToForm(AlterEgo, effect)
        identity = player.GetIdentity()

        def defausser_tough(targets: Sequence['CardFace']) -> None:
            identity.DiscardTough(effect, rule=1)
            Faces.DiscardAll([this], effect)

        def sonner(targets: Sequence['CardFace']) -> None:
            Faces.GiveStatus([identity], "Stunned", effect)
            Faces.DiscardAll([this], effect)

        def desorienter(targets: Sequence['CardFace']) -> None:
            Faces.GiveStatus([identity], "Confused", effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard a tough status card from Ben Grimm → discard this obligation",
                defausser_tough,
                condition=identity.IsTough(),
            ),
            AbilityFactory.ForChoiceAbility(
                "Stun Ben Grimm → discard this obligation",
                sonner
            ),
            AbilityFactory.ForChoiceAbility(
                "Confuse Ben Grimm → discard this obligation",
                desorienter
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            annual_shedding
        ),
    ]
