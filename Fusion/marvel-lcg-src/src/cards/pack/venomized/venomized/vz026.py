from . import *

# Symbiote Infusion — RESSOURCE [wild]. Max 2 per deck.
# Hero Interrupt: When you spend this card to play a SYMBIOTE card, draw 1 card.
#
# CARTE DE REFERENCE
#  - `32018` Defensive Energy (pack mut_gen) : « Max 2 per deck. Hero
#    Interrupt: When you spend this card to play a [[Defense]] event, draw 1
#    card. » Meme carte a un filtre pres.
#
# TEXTE CONTRE CODE
#  ⚠ « a SYMBIOTE CARD » et non « a SYMBIOTE event » : le filtre porte sur le
#    TRAIT SEUL, sans type de carte. `32018` passe `CardFinder2("DEFENSE",
#    Event)` ; ici l'amelioration `vz030` ou l'allie `vz001` comptent aussi.
def GetAbilities() -> Sequence['Ability']:

    def symbiote_infusion(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this, message)

        for target in effect.targets:
            target.GetControlByPlayer().DrawUp(1, effect)

    return [
        AbilityFactory.WhenYouSpendThisCardToPlay(
            AbilityType.HeroInterrupt,
            symbiote_infusion,
            CardFinder(trait=SYMBIOTE),
        ).SetTarget("Initiator"),
    ]
