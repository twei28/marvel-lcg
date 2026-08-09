from . import *

# Doreen Green
# Setup : monte le deck ecureuil (six allies mis de cote, melanges).
# Squirrel Speech — Alter-Ego Action: Exhaust Doreen Green → call 1 Squirrel.

def GetAbilities() -> Sequence['Ability']:

    def avec_le_deck_ecureuil(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        ecureuils = [face for face in initiator.additional_discard_pile.Get()
                     if face.HasTrait('SQUIRREL')]

        for face in ecureuils:
            PreparerEcureuil(face, initiator)

        Faces.FlipAllTo(ecureuils, False, effect)
        Faces.ShuffleAllTo(ecureuils, initiator.additional_deck, effect)

    def squirrel_speech(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        AppelerEcureuil(effect.GetInitiator(), effect)

    return [
        # « Squirrel Aid » : meme source de paiement que la face heros. Les
        # cartes du set se jouent aussi en alter-ego, la capacite doit donc
        # exister des deux cotes.
        CapaciteDepenseIdentite(),
        AbilityFactory.BeginGameWithSetAside(ID_ECUREUILS, avec_le_deck_ecureuil),
        (AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, squirrel_speech)
            .SetName("Squirrel Speech")
            .SetCostFunc(CostFunc.Exhaust("This"))
            .LimitOncePerRound()),
    ]
