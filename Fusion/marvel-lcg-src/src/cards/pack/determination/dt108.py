from . import *

# Defy the Future

def GetAbilities() -> Sequence['Ability']:

    def defy_the_future(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        faces = list(initiator.LookAtDeck("EncounterDeck", 1, effect))
        cachees = list(initiator.dealt_encounter_cards.Get())
        Faces.LookAt(cachees, initiator, effect)
        faces += cachees
        if not faces:
            return

        combien = initiator.DeclareNumber(0, len(faces))
        if combien <= 0:
            return
        Faces.DiscardAll(faces[:combien], effect)
        initiator.DealEncounterCards(combien, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            defy_the_future
        ).SetPlay(),
    ]
