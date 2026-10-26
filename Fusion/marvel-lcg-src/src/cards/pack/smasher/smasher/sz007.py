from . import *
# Hyper-Speed, amelioration EXOSPEX. Cout 1, [energy]. SUPERPOWER.
#
# Smasher gets +1 ATK, +1 THW and +1 DEF.
# Hero Response: After you play Hyper-Speed, ready Smasher.
#
# Cartes de reference : 01017 (bonus attache) ; 01082 Indomitable (`.SetTarget("YourHero", canbe_ready=True)` + `ReadyAll`) ; 62009.
def GetAbilities() -> Sequence['Ability']:
    def hyper_speed(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        ReponseHyperSpeed(effect, effect.GetInitiator())
    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Smasher"), attack=1, thwart=1, defense=1),
        AbilityFactory.AfterYouPlayThisFromHand(
            AbilityType.HeroResponse,
            hyper_speed,
        ),
    ]
