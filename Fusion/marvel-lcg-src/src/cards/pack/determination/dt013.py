from . import *

# Recon

def GetAbilities() -> Sequence['Ability']:

    # « look at up to 3 facedown encounter cards » : ce sont bien les cartes
    # distribuees FACE CACHEE devant les joueurs, et le moteur les tient —
    # `player.dealt_encounter_cards` (50051, Intelligence). L'approximation
    # « le dessus de la pile » du premier jet est donc levee.
    def cout(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        return initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Spend a resource of any type",
                lambda targets:
                    initiator.AskSpendResourcesInternal(Cost("1"), effect)
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Exhaust a friendly character you control",
                lambda targets:
                    Faces.ExhaustAll(targets, effect)
            ).SetTarget("YouControlUnit", canbe_exhaust=True),
        ) != []

    def recon(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        cachees = [f for joueur in Worlds.GetPlayers(effect)
                   for f in joueur.dealt_encounter_cards.Get()][:3]
        if not cachees:
            return
        Faces.LookAt(cachees, initiator, effect)

        minions = Filter.ByType(cachees, Minion)
        for minion in minions:
            minion.CastTo(Minion).PutIntoPlay(initiator, effect)
            initiator.DrawUp(2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            recon
        ).LimitOncePerRound()
        .SetCostFunc(CostFunc.Custom(None, cout)),
    ]
