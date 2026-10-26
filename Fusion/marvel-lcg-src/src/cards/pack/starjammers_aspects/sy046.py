from . import *
# Ready for Anything (Protection, evenement 3 [mental]). CONDITION. Requirement ([energy][mental][physical]).
# Hero Action: Stun and confuse an enemy. Give your identity a tough status card.
#
# Cartes de reference : 01083 Mockingbird (Sonne) ; dt002 (`GiveStatus` « Confused ») ; 19001a / tg010 (`Faces.GiveStatus([identite], "Tough",
# effect)`). « Stun AND confuse AN enemy » : le MEME ennemi, cible obligatoire (pas de `range=(0, ..)`, RECETTES §6).
def GetAbilities() -> Sequence['Ability']:
    def ready_for_anything(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        Faces.GiveStatus(effect.targets, "Stunned", effect)
        Faces.GiveStatus(effect.targets, "Confused", effect)
        joueur = effect.GetInitiator()
        Faces.GiveStatus([joueur.GetIdentity()], "Tough", effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            ready_for_anything,
        ).SetPlay().SetLabel()
        .SetTarget(Enemy),
    ]
