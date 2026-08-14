from . import *

# Experimental Sewer Lair

def GetAbilities() -> Sequence['Ability']:

    def boost_attaque(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: If this activation is a:
        #   • Attack, that attack gains ranged and overkill. »
        message.would_atk_message.GainRanged(effect)
        message.would_atk_message.GainOverKill(effect)

    def boost_complot(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # «   • Scheme, put Experimental Sewer Lair into play. Then, place
        #     1 acceleration token on Experimental Sewer Lair. »
        this = effect.this.CastTo(EncounterSideScheme)
        this.PutIntoPlay(message.GetToPlayer(), effect)
        this.PlaceAccelerationToken(1, effect)

    return [
        # « Each enemy gains retaliate 1. »
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Enemy),
            retaliate=1,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost_attaque,
            during_attack=True,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost_complot,
            during_scheme=True,
        ),
    ]
