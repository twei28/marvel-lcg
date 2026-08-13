from . import *

# Lightning Rod

def GetAbilities() -> Sequence['Ability']:

    def lightning_rod(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Upgrade)

        sbire = this.GetBindFace()
        if sbire is None:
            return
        avant = sbire.CastTo(CanHealth).health
        this.DealDamage([sbire], 6, effect)
        surplus = 6 - avant
        if surplus <= 0:
            return

        # « le personnage avec le plus de cartes attachees » : le moteur ne le
        # nomme pas, on le calcule.
        personnages = [x for x in Worlds.FindCardsOnField(effect, card_type=Unit2)
                       if not x.IsDefeated() and x is not sbire]
        if not personnages:
            return
        cible = max(personnages, key=lambda f: len(f.GetInventoryDeck().GetAll()))
        this.DealDamage([cible], surplus, effect)

    def check_set_standard(effect: 'Effect', message: 'Message.WhenCardRevealed') -> bool:
        return message.trigger.paper.set_name == "Standard"

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Minion)
        ),
        AbilityFactory.WhenCardRevealed(
            AbilityType.ForcedInterrupt,
            None,
            lightning_rod,
            conditions=[check_set_standard],
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
