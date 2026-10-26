from . import *

# Solar Soar — AMELIORATION, cout 3, RES [physical]. SUPERPOWER.
# Sunspot gains the AERIAL trait.
# Hero Response: At the end of your turn, place 1 solar counter on Sunspot.
#
# CARTES DE REFERENCE
#  - `01017` Cosmic Flight : `GiveKeywordToAttached(.., trait="AERIAL")`.
#  - `AbilityFactory.AfterPlayerTurnEnd(HeroResponse, "You", op)` : « at the end of your turn » (Binary `bn_fin_de_tour`).
#
# TEXTE CONTRE CODE
#  ⚠ Ce trait AERIAL est CELUI que lisent so003 (stun), so005 (autre manigance), so006 (3 compteurs) : `EstAerien` (helpers du set).


def GetAbilities() -> Sequence['Ability']:

    def solar_soar(effect: 'Effect', message: 'Message.AfterPlayerTurnEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        Unused(message)
        PoserSolaires(effect.GetInitiator(), 1, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Sunspot"),
            trait="AERIAL",
        ),
        AbilityFactory.AfterPlayerTurnEnd(
            AbilityType.HeroResponse,
            "You",
            solar_soar,
        ),
    ]
