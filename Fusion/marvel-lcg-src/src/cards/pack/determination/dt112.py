from . import *

# * Spiral

def GetAbilities() -> Sequence['Ability']:

    def bonus_cartes_cachees(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Ally)
        player = this.GetControlByPlayer()
        if player is None:
            return 0
        # « elle ne peut pas depasser 6 ATK » : ATK imprimee 1, donc +5 au plus.
        return min(5, len(player.dealt_encounter_cards.Get()))

    def spiral(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        effect.GetInitiator().DealEncounterCards(2, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            bonus_cartes_cachees,
            attack=1,
            change_on_event=OnEvent.GameArea(),
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            spiral
        ),
    ]
