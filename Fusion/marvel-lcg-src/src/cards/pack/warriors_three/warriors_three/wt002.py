from . import *


def GetAbilities() -> Sequence['Ability']:
    def changer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        changer_de_heros(effect)

    def sbire_vaincu(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        # « If a minion was defeated THIS TURN » (wt022) : le tour (RR « Turn »), pas le round. Un seul indicateur pour la table,
        # remis a faux au debut de CHAQUE tour de joueur : un sbire vaincu pendant le tour d'un autre joueur ne compte pas.
        Unused(message)
        effect.world.stat.wt_sbire_vaincu_ce_tour = True

    def tour_commence(effect: 'Effect', message: 'Message.WhenPlayerTurnBegin') -> None:
        Unused(message)
        effect.world.stat.wt_sbire_vaincu_ce_tour = False

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            control_additional_restricted=CardFinder(card_type=Upgrade),
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            changer,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenUnitWouldChangeForm(
            AbilityType.ForcedInterrupt,
            "You",
            noter_le_heros_avant,
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.ForcedResponse,
            "You",
            synchroniser_formes,
        ),
        AbilityFactory.WhenPlayerTurnBegin(AbilityType.ForcedInterrupt, "AnyPlayer", tour_commence),
        AbilityFactory.AfterUnitBeDefeated(AbilityType.ForcedResponse, Minion, sbire_vaincu),
    ]
