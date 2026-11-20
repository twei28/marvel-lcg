from . import *
# * Bio-Synthetic Wings — amelioration. En forme TINY le heros gagne le trait AERIAL (modele 13010 : une
# GiveKeywordToAttached par forme, relancee quand l'identite change). Hero Action (thwart) : incline ->
# retire X menaces REPARTIES ENTRE les manigances (« from among schemes », modele 17029 / 36010 : une designation = 1 menace),
# X = nombre de changements de forme ce tour. CORRECTIF 26/10/2026 : avant, X menaces d'UNE seule manigance.
def GetAbilities() -> Sequence['Ability']:
    def wings(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        this.RemoveThreatFromSchemesTotal(effect.targets, formes_changees_ce_tour(effect), effect)
    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder2("TINY", Hero),
            trait="AERIAL",
            ex_change_on_event=OnEvent.Trait("AttachedIdentity"),
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            wings,
        ).SetLabel('thwart')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Scheme2, range=(lambda e: min(1, formes_changees_ce_tour(e)), formes_changees_ce_tour),
                   repeat_rules="Threat"),
    ]
