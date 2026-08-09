from . import *

# Board Meeting

def GetAbilities() -> Sequence['Ability']:

    def board_meeting(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        # « You MAY flip to alter-ego form » : proposee, pas imposee.
        identity = player.GetIdentity()
        # CORRECTIF : IsHero() n'existe que sur Player, jamais sur une face.
        # L'obligation plantait donc a CHAQUE revelation.
        if Hero.IsType(identity):
            player.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Flip to alter-ego form",
                    lambda targets: identity.ChangeToOtherIdentityForm(effect),
                ),
            )

        def epuiser_pepper(targets: Sequence['CardFace']) -> None:
            Faces.ExhaustAll([player.GetIdentity()], effect)
            Faces.RemoveAllFromGame([this], effect)

        def defausser_tech(targets: Sequence['CardFace']) -> None:
            cibles = list(targets)
            if cibles:
                Faces.DiscardAll(cibles, effect)
            else:
                # Aucun upgrade TECH defausse : la carte gagne surge.
                this.GainSurge(1, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Pepper Potts -> remove Board Meeting from the game",
                epuiser_pepper),
            AbilityFactory.ForChoiceAbility(
                "Discard 1 TECH upgrade you control", defausser_tech)
            .SetTarget(CardFinder(card_type=Upgrade, trait="TECH"),
                       range=(0, 1), from_where=["YouControlCards"]),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            board_meeting
        ),
    ]
