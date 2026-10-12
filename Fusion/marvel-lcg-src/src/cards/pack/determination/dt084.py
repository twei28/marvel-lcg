from . import *

# Off the Cuff

def GetAbilities() -> Sequence['Ability']:

    def off_the_cuff(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        deja = initiator.GetControlCards2(CardFinder(name="Spontaneity"))
        if not deja:
            face = Search.PlayerCard(effect, initiator,
                                     include_player_deck=True,
                                     include_hand=True,
                                     include_discard_pile=True,
                                     may=True,
                                     name="Spontaneity")
            if face:
                face.CastTo(Upgrade).PutIntoPlay(initiator, effect)
                return

        # Deja en jeu : 1 degat a un personnage, puis un statut sur lui.
        def frapper(targets: Sequence['CardFace']) -> None:
            this.DealDamage(targets, 1, effect)
            statut = initiator.AskChooseOneText(["Tough", "Stunned", "Confused"])
            Faces.GiveStatus(targets, statut, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to a character, then place a status card on them",
                frapper
            ).SetTarget(Unit2)
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            off_the_cuff
        ).SetPlay(),
    ]
