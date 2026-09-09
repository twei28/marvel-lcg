from . import *

# Brutal Efficiency — EVENEMENT, cout X [physical]. ATTACK. TACTIC.
# Hero Action (attack): Place X threat on the main scheme (to a maximum of 3)
#   -> deal 3X damage to an enemy. This attack gains overkill.
#
# CARTES DE REFERENCE
#  - `14006`, `ho004`, `sm004` : le cout X se lit `effect.GetCostX()`.
#    ⚠⚠ Et il compte les ICONES, pas les cartes (`effect.py:509`) — RECETTES
#    §7bis disait le contraire, corrige le 08/09/2026.
#  - `50134`, `ho015` : `this.PlaceThreatOnSchemes("MainScheme", n, effect)`.
#  - `27078`, `ho016` : `UnitAttackGainKeyword(..., overkill=True)`.
#
# TEXTE CONTRE CODE
#  ⚠ « PLACE X THREAT ON THE MAIN SCHEME -> » : la fleche en fait un COUT, et
#    quel cout : la carte AIDE LE VILAIN pour frapper plus fort. C'est tout le
#    caractere d'Otto Octavius. Ne pas l'oublier ferait une carte gratuite.
#  ⚠ « TO A MAXIMUM OF 3 » : le plafond porte sur X, donc 9 degats au plus.
#  ⚠ « THE MAIN scheme », pas « a scheme » : littéral `"MainScheme"`.
#  ⚠ Le cout X exige la cle `surpayer` dans les cas (RECETTES §7bis).
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def efficacite(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        x = min(int(effect.GetCostX() or 0), 3)
        if x <= 0:
            return

        this.PlaceThreatOnSchemes("MainScheme", x, effect)

        temps = this.effect.RegisterTemp(
            AbilityFactory.UnitAttackGainKeyword("This", overkill=True),
            unregister_after_exec=False,
        )
        this.DealDamage(effect.targets, 3 * x, effect)
        if temps:
            Effects.UnRegister(temps)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            efficacite,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, range=(1, 1)),
    ]
