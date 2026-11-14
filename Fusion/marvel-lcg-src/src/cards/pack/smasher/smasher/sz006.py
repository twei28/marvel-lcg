from . import *
# Hyper-Strength, amelioration EXOSPEX. Cout 1, [physical]. SUPERPOWER.
#
# Smasher gets +2 ATK. Smasher's attacks gain overkill.
# Hero Response: After you play Hyper-Strength, stun an enemy.
#
# Cartes de reference : 01017 (bonus attache) ; fiche mots-cles/overkill.md (`UnitAttackGainKeyword(.., overkill=True)`) ; 62009 (Response a la jouee).
def GetAbilities() -> Sequence['Ability']:
    def hyper_strength(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        ReponseHyperStrength(effect, effect.targets)
    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Smasher"), attack=2),
        AbilityFactory.UnitAttackGainKeyword("You", overkill=True),
        AbilityFactory.AfterYouPlayThisFromHand(
            AbilityType.HeroResponse,
            hyper_strength,
        ).SetTarget(Enemy),
    ]
