from . import *

# Recon

def GetAbilities() -> Sequence['Ability']:

    # APPROXIMATION, ECRITE PLUTOT QUE SILENCIEUSE.
    #
    # « look at up to 3 facedown encounter cards » n'a aucun crochet dans le
    # moteur, et le releve des 142 cartes le signalait deja. Les seules cartes
    # de rencontre face cachee qu'il sait montrer sont celles du DESSUS DE LA
    # PILE (`LookAtDeck`) : les cartes deja distribuees face cachee devant les
    # joueurs ne sont pas un ensemble consultable. C'est donc la pile qui est
    # lue — la lecture la plus proche, et la seule jouable.
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
        faces = initiator.LookAtDeck("EncounterDeck", 3, effect)

        minions = Filter.ByType(faces, Minion)
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
