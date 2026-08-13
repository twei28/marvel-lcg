from . import *

# Heroes for Hire

def GetAbilities() -> Sequence['Ability']:

    # La capacite n'est gagnee QUE si chacun de vos allies porte le trait, et
    # cela peut changer a tout moment : la condition se relit au declenchement.
    def check_tous_hero_for_hire(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> bool:
        this = effect.this.CastTo(Support)
        player = this.GetControlByPlayer()
        if player is None:
            return False
        allies = player.GetAllies()
        return bool(allies) and all(a.HasTrait("HERO FOR HIRE") for a in allies)

    def heroes_for_hire(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        player = this.GetControlByPlayer()
        if player:
            player.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(
            under_any_players_control=True
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "YourAlly",
            Enemy,
            heroes_for_hire,
            conditions=[check_tous_hero_for_hire],
        ),
    ]
