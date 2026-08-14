from . import *

# * Princess Python

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Search the encounter deck and discard pile for a copy
        # of Experimental Injection and attach it to Princess Python. »
        this = effect.this.CastTo(Minion)
        seringue = Search.SearchForCard(
            effect,
            message.GetToPlayer(),
            include_encounter_deck=True,
            include_encounter_discard_pile=True,
            name="Experimental Injection",
        )
        if seringue:
            seringue.PutIntoPlay(message.GetToPlayer(), effect)
            seringue.AttachTo2(this, effect)

    def morsure(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        # « Forced Response: After Princess Python attacks you, take 2 indirect
        # damage. »
        this = effect.this.CastTo(Minion)
        joueur = message.attacked.GetControlByPlayer()
        joueur.GetIdentity().TakeIndirectDamage(this, 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "This",
            "YourIdentity",
            morsure
        ),
    ]
