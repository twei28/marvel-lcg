from . import *

# * Dutch Schaefer — SBIRE nemesis de Predator (set « Predator Alt Nemesis »). ELITE. SOLDIER. PV 6, MNG 2★, ATQ 2★, Boost 2.
# Toughness.
# ★ Forced Response: After Dutch Schaefer activates, place 1 threat on each scheme.
# (Predator's nemesis minion.)
#
# Cartes de reference :
#  - `nt013` : `AfterEnemyActivationEnd(ForcedResponse, "This", op)` pour « after X activates » (toute activation, pas seulement
#    contre toi) ; `27094` / `27158` : `this.PlaceThreatOnSchemes("EachScheme", 1, effect)` ;
#  - `Toughness` et `Nemesis` : bases automatiques (`desc`).
#
# ⚠ Mots-pieges :
#  - « After Dutch Schaefer ACTIVATES » : attaque OU manigance, contre n'importe quel joueur (pas « activates against you ») ;
#  - « on EACH scheme » : le complot principal ET chaque manigance annexe, 1 menace chacune ;
#  - « ★ » = etoile imprimee devant la phrase, capacite constante (convention RECETTES §3).


def GetAbilities() -> Sequence['Ability']:

    def menace_partout(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        this.PlaceThreatOnSchemes("EachScheme", 1, effect)

    return [
        AbilityFactory.AfterEnemyActivationEnd(
            AbilityType.ForcedResponse,
            "This",
            menace_partout,
        ),
    ]
