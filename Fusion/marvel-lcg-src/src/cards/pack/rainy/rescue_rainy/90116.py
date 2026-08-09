from . import *

# Magnetic Restraints

def GetAbilities() -> Sequence['Ability']:

    def restraints(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()

        def etourdir(targets: Sequence['CardFace']) -> None:
            Faces.GiveStatus(list(targets), "Stunned", effect)

        def defausser_attachement(targets: Sequence['CardFace']) -> None:
            # Meme aide que « Phase Disruption » (26011) : elle sait trouver les
            # attachements portant « Hero Action » / « Hero Response ».
            Players.DiscardHeroActionAttachment(initiator, list(targets), effect, may=False)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Stun an enemy", etourdir)
            .SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility(
                'Discard an attachment with "Hero Action" or "Hero Response"',
                defausser_attachement
            ).SetTarget(Enemy, check_fn=
                lambda effect, face:
                    Enemy.IsType(face) and
                    face.GetInventoryDeck().FindCard(
                        with_texts=["Hero Action", "Hero Response"]) != None
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            restraints
        ).SetPlay().SetLabel(),
    ]
