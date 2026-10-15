from . import *

# Skrull Imperial Fleet — TRAITRISE (Kree-Skrull War). ★ + 1 icone Y.
# When Revealed: Discard the top card of the encounter deck. Place 1 threat on
#   each scheme in play for each boost icon discarded this way.
# ★ Boost: Place 2 threat on Earth Involvement.
#
# Cartes de reference :
#  - **`sk139`** (meme set, meme premiere phrase) ; **`ho015`** / `sk114` :
#    `PlaceThreatOnSchemes("EachScheme", n, effect)` (principal ET annexes).
#  - **`sk106`** : `CountTotalBoostIcons` sur les cartes defaussees.
#
# ⚠ Mots-pieges : « EACH scheme in play » = complot principal et TOUS les complots
# annexes (pas seulement les annexes) ; « 1 threat ... FOR EACH icon » (N menaces
# sur chacun) ; icones Y imprimees, pas le ★ ; carte defaussee sans icone Y : rien.


def GetAbilities() -> Sequence['Ability']:

    def flotte(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this.CastTo(Treachery)
        defaussees = Worlds.DiscardEncounterCards(1, effect)
        icones = FacesCounter.CountTotalBoostIcons(defaussees)
        if icones > 0:
            this.PlaceThreatOnSchemes("EachScheme", icones, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        PlacerMenaceSurEarthInvolvement(effect, effect.this, 2)

    return [
        AbilityFactory.WhenThisRevealed(None, flotte),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
