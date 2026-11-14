from . import *
# Super-Resistance, amelioration EXOSPEX. Cout 1, [physical]. SUPERPOWER.
#
# Smasher gets +2 DEF and gains Stalwart.
# Hero Response: After you play Super-Resistance, give Smasher a tough status card.
#
# Cartes de reference : 01017 ; fiche mots-cles/stalwart.md (`GiveKeywordToAttached(.., stalwart=1)`) ; 01105 « I'm Tough »
# (`Faces.GiveStatus([..], "Tough", effect)`).
def GetAbilities() -> Sequence['Ability']:
    def super_resistance(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        ReponseSuperResistance(effect, effect.GetInitiator())
    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Smasher"), defense=2, stalwart=1),
        AbilityFactory.AfterYouPlayThisFromHand(
            AbilityType.HeroResponse,
            super_resistance,
        ),
    ]
