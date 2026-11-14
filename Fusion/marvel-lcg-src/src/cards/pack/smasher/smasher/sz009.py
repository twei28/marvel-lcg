from . import *
# Exo-Flight, amelioration EXOSPEX AERIAL. Cout 1, [energy]. SUPERPOWER.
#
# Smasher gets +1 THW, +1 DEF and gains the AERIAL trait.
# Hero Response (thwart): After you play Exo-Flight, remove 3 threat from a scheme.
#
# Cartes de reference : 01017 Cosmic Flight (`GiveKeywordToAttached(.., trait="AERIAL")`) ; 47004 Jubilee's Coat (Hero Response (thwart) :
# `.SetLabel('thwart')` + `.SetTarget(Scheme2)`).
def GetAbilities() -> Sequence['Ability']:
    def exo_flight(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        ReponseExoFlight(effect, effect.targets)
    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Smasher"), thwart=1, defense=1, trait=TRAIT_AERIAL),
        AbilityFactory.AfterYouPlayThisFromHand(
            AbilityType.HeroResponse,
            exo_flight,
        ).SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
