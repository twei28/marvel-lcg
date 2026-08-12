from . import *

# * Mjolnir — custom « DesignHacker » (Age of Khonshu)
# Linked (Thor) : mis en jeu par le When Defeated de Thor (mk020).
# Your hero gets +1 ATK and gains the AERIAL trait.
# Forced Response: After you engage a minion, exhaust Mjolnir and remove 1
#   attack counter from it → draw 2 cards.


def GetAbilities() -> Sequence['Ability']:

    def apres_engagement(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> None:
        this = effect.this.CastTo(Upgrade)
        controleur = this.GetControlByPlayer()
        if controleur is not None:
            controleur.DrawUp(2, effect)

    def concerne_son_controleur(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> bool:
        return message.GetToPlayer() == effect.this.GetControlByPlayer()

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            attack=1,
            trait="AERIAL",
        ),
        Ability(
            AbilityType.ForcedResponse,
            Message.AfterMinionEngagePlayer,
            [concerne_son_controleur],
            apres_engagement,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'attack')),
    ]
