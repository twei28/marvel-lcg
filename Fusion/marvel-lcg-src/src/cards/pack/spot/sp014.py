from . import *

# Warp Hole

def GetAbilities() -> Sequence['Ability']:

    def au_moins_trois_menaces(effect: 'Effect', ui: List['CardFace']) -> int:
        return 1 if effect.this.CastTo(CanPlaceToken).GetTokens('threat') >= 3 else 0

    def apres_gros_degats(effect: 'Effect', message: 'Message.AfterFaceDealDamage') -> None:
        this = effect.this.CastTo(Environment)

        # « After an attack deals 3 or more damage to The Spot, remove 2 threat
        # from here. If the last threat is removed from here this way, discard
        # Warp Hole. »
        #
        # Le deroutement du complot principal ne s'applique PAS ici : il ne vise
        # que le complot lui-meme et les manigances annexes du Spot, et Warp
        # Hole est un environnement. La menace part donc vraiment.
        avant = this.GetTokens('threat')
        if avant <= 0:
            return
        Faces.RemoveTokensOn([this], 2, 'threat', effect)
        if this.GetTokens('threat') == 0:
            Faces.DiscardAll([this], effect)

    return [
        # « While there is 3 or more threat here, this card gains
        # [acceleration] [hazard]. »
        AbilityFactory.ThisGainKeyword(
            au_moins_trois_menaces,
            acceleration_icon=1,
            hazard=1,
            change_on_event=OnEvent.Token("This", 'threat')
        ),
        *AbilityFactory.AfterUnitDealsDamageWithSingleAttack(
            AbilityType.HeroResponse,
            None,
            CardFinder(name="The Spot"),
            apres_gros_degats,
            dealt_more_than_damage=3
        ),
    ]
