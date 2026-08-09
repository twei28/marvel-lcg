from . import *

# * Cypher: Doug Ramsey

def GetAbilities() -> Sequence['Ability']:

    def cypher(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()
        initiator.DrawUp(1, effect)

    return [
        # CORRECTIF : le texte dit « attacks AND DAMAGES a confused enemy ».
        # AfterUnitAttackUnit ne filtre pas les degats : la pioche partait meme
        # quand l'attaque n'en infligeait aucun (cible Tenace, prevention...).
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.Response,
            "This",
            CardFinder(is_confused=True, card_type=Enemy),
            cypher,
        ),
    ]

