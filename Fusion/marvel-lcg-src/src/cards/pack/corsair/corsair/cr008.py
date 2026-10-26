from . import *
# Riposte. Evenement ATTACK SKILL, cout 1.
#
# Hero Response (attack): After an enemy attacks you, deal 4 damage to that enemy. If the last card you played was Parry,
#   stun that enemy.
#
# Cartes de reference : 37011 Bishop (`AfterUnitAttackYou(Response, Enemy, op)` : « After an enemy attacks you »),
# 19007 Payback (`AfterUnitAttackUnit(HeroResponse, Villain, "You", ...)` + `SetPlay().SetLabel('attack')`),
# 05015 Tackle pour le statut (`Faces.GiveStatus`).
# « that enemy » = l'attaquant du message (`message.trigger`), pas une cible choisie.
def GetAbilities() -> Sequence['Ability']:
    def riposte(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Event)
        attaquant = message.trigger
        if attaquant is None or not attaquant.IsInPlay():
            return
        this.DealDamage([attaquant], 4, effect)
        if attaquant.IsInPlay() and DerniereEstUne(effect, JoueurDe(effect), PARRY):
            Faces.GiveStatus([attaquant], "Stunned", effect)
    return [
        AbilityFactory.AfterUnitAttackYou(
            AbilityType.HeroResponse,
            Enemy,
            riposte,
        ).SetPlay().SetLabel('attack'),
    ]
