from . import *
# Penta-Vision, amelioration EXOSPEX. Cout 1, [mental]. SUPERPOWER.
#
# Smasher gets +1 ATK and +1 THW. Smasher's attacks gain ranged.
# Hero Response (attack): After you play Penta-Vision, deal 3 damage to an enemy.
#
# Cartes de reference : 01017 Cosmic Flight (`GiveKeywordToAttached(CardFinder(name=..))`) ; fiche mots-cles/ranged.md
# (`UnitAttackGainKeyword(.., ranged=True)`, permanent) ; 62009 (`AfterYouPlayThisFromHand`) ; 08010 Widow's Bite (Hero Response (attack) :
# `.SetLabel('attack')` + cible).
def GetAbilities() -> Sequence['Ability']:
    def penta_vision(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        ReponsePentaVision(effect, effect.targets)
    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Smasher"), attack=1, thwart=1),
        AbilityFactory.UnitAttackGainKeyword("You", ranged=True),
        AbilityFactory.AfterYouPlayThisFromHand(
            AbilityType.HeroResponse,
            penta_vision,
        ).SetLabel('attack')
        .SetTarget(Enemy),
    ]
