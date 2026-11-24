from . import *


def GetAbilities() -> Sequence['Ability']:
    def enhanced_combat_sense(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        message.CancelAllEffectsAndDiscardIt(effect)
        # « For each upgrade you exhausted to pay for this card » : posees par la ressource de sq001a.
        for _ in range(getattr(effect, "sq_ameliorations_epuisees", 0)):
            DegatOuMenace(effect, this, joueur)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            EncounterCard,
            "All",
            enhanced_combat_sense,
            from_encounter=True,
        ).SetPlay().SetLabel(),
    ]
