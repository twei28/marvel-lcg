from . import *

# Outer Space Ambush

def GetAbilities() -> Sequence['Ability']:

    # « Alliance » n'a AUCUN crochet ni rappel entre parentheses sur la carte :
    # le mot-cle ne fait rien par lui-meme, il nomme ce que le texte demande
    # deja (un AVENGER et un GUARDIAN). Rien n'est donc invente pour lui.
    def outer_space_ambush(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        cout = effect.cost_func.Get(CostFunc.Exhaust)
        exhausted = list(cout.return_exhausted_cards) if cout else []

        this.DealDamage(exhausted, 1, effect)

        ennemis = [x for x in Worlds.FindCardsOnField(effect, card_type=Enemy)
                   if not x.IsDefeated()]
        if ennemis:
            initiator.AssignDamage(ennemis, this, 6, effect)

        debout = [f for f in exhausted if not f.CastTo(Unit2).IsDefeated()]
        if len(debout) == len(exhausted):
            Faces.ReadyAll(exhausted, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            outer_space_ambush
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("YouControlUnit", trait="AVENGER"))
        .SetCostFunc(CostFunc.Exhaust("YouControlUnit", trait="GUARDIAN")),
    ]
