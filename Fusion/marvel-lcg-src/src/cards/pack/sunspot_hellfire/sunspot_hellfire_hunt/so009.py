from . import *

# * Da Costa International — SOUTIEN, cout 1, RES [mental]. LOCATION. Unique.
# Alter-Ego Response: After you resolve your "Energy Absorption" ability, place 1 solar counter on your identity.
#
# CARTES DE REFERENCE
#  - `21037` Mystic Senses / `21035` Warlock's Cape : `AfterPlayerResolveAbility(type, "You", CardFinder(name=..), op, ability_name="...")`
#    (« after you resolve your "Battle Mage" ability »).
#
# TEXTE CONTRE CODE
#  ⚠ « your "Energy Absorption" ability » : la capacite NOMMEE de Roberto (so001b), pas n'importe quelle Action.
#  ⚠ Response d'ALTER EGO : `AbilityType.AlterEgoResponse` (sinon elle partirait aussi en forme heros).


def GetAbilities() -> Sequence['Ability']:

    def da_costa_international(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        Unused(message)
        joueur = JoueurQuiControle(effect)
        if joueur is not None:
            PoserSolaires(joueur, 1, effect)

    return [
        AbilityFactory.AfterPlayerResolveAbility(
            AbilityType.AlterEgoResponse,
            "You",
            CardFinder(name="Roberto Da Costa"),
            da_costa_international,
            ability_name="Energy Absorption",
        ),
    ]
