from . import *

# Dupes Gone Bad : SBIRE (set nemesis, n/5 : mm020, mm021, mm022). DUPLICATE. SCH 1 / ATQ 2 / PV 3, boost ★ + 1.
# When Revealed: Add 1 threat to each side scheme in play.
# ★ Boost: Add 1 threat to each side scheme in play.
#
# CARTES DE REFERENCE : `ca020` (`WhenCardBecomeBoost("This", op)` pour un Boost ★), `ca016` / `60095` (`WhenThisRevealed(None, op)`), `card_face.py::PlaceThreatOnSchemes("EachSideScheme", n, effect)`.
# TEXTE CONTRE CODE : « each SIDE scheme in play » : les complots annexes (le principal n'en recoit pas) ; aucun complot annexe : sans effet. « Add 1 threat » = placer 1 menace. Le Boost se resout quand la
#  carte est retournee comme carte de renfort d'une activation ; le ★ du Boost est lu dans le texte (`Boost` du desc = 1 icone). Chiffres : SCH 1, ATQ 2, PV 3, boost 1 + ★.


def GetAbilities() -> Sequence['Ability']:

    def une_menace_partout(effect: 'Effect', message: 'Message2') -> None:
        Unused(message)
        effect.this.PlaceThreatOnSchemes("EachSideScheme", 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            une_menace_partout,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            une_menace_partout,
        ),
    ]
