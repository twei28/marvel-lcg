from . import *
def GetAbilities() -> Sequence['Ability']:
    # CORRECTIF (16/10/2026, reskin ub048 Slash de l'aspect TMNT Basic) : « Hulk gets +1 ATK for each
    # rage counter here ». L'ancien `WhileValid(OnEvent.CardInPlay(Ally), ...)` ne recalculait l'ATK que
    # quand un ALLIE entrait en jeu : un compteur rage pose par la Reponse ne changeait rien (cas
    # `[ub] ub048 ... TEMOIN 62020` rouge, ATK restee a 2 avec 1 rage). Modele 27067 Sand Clone :
    # `ThisGainKeyword(..., change_on_event=OnEvent.Counter(<carte>, <compteur>))`.
    def rage(effect: 'Effect', ui: List['CardFace']) -> int:
        return effect.this.GetCounters('rage')
    def villain_attacks(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Ally)
        this.PlaceCountersInternal(1, 'rage', effect)
    def check_villain(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> bool:
        return Villain.IsType(message.attacker)
    return [
        AbilityFactory.ThisGainKeyword(rage, attack=1, change_on_event=OnEvent.Counter("This", 'rage')),
        AbilityFactory.AfterUnitAttackUnit(AbilityType.Response, None, "You", villain_attacks, conditions=[check_villain]),
    ]
