from . import *

# * Zenpool

def GetAbilities() -> Sequence['Ability']:

    def zenpool(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()
        cachees = list(initiator.dealt_encounter_cards.Get())
        if not cachees:
            return
        # « depensez un nombre quelconque de ressources » : on ne peut pas en
        # defausser plus qu'il n'y a de cartes cachees devant soi.
        voulu = initiator.DeclareNumber(0, len(cachees))
        if voulu <= 0:
            return
        res = initiator.AskSpendResourcesInternal(Cost(str(voulu)), effect)
        if res:
            Faces.DiscardAll(cachees[:voulu], effect)

    return [
        *Alias(),
        AbilityFactory.WhenCardEnterPlay(
            AbilityType.Interrupt,
            "This",
            zenpool
        ),
    ]
