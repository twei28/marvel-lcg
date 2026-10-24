from . import *

# Stark Nunchaku — AMELIORATION, cout 3, [energy]. WEAPON. (card_id shc015, 13/15)
# Restricted. Enters play with 3 charge counters on it.
# Hero Action: Exhaust Stark Nunchaku and remove 2 charge counters from it → stun an enemy.
#
# Cartes de reference :
#  - `dz002` : `AbilityFactory.ThisEnterPlayWithCounters(N, 'nom')` (« enters play with N counters »).
#  - `sh010` Martial Skill / `ua033` Pete : cout double `SetCostFunc(CostFunc.Exhaust("This"))` + `SetCostFunc(CostFunc.Counter("This", N, 'nom'))`.
#  - `01083` / `05015` : `Faces.GiveStatus(cibles, "Stunned", effect)` avec `SetTarget(Enemy, canbe_stunned=True)`.
#
# ⚠ Mots-pieges :
#  - « Restricted » : base automatique (`desc.Restricted`), aucun code.
#  - « remove 2 charge counters » : DEUX, pas un ; `CostFunc.Counter` seul est offert meme impayable (RECETTES §5) : une condition
#    verifie les 2 compteurs. 3 compteurs au depart = UN seul usage complet (3 - 2 = 1 < 2).
#  - « Hero Action » : en forme heros seulement ; « stun AN enemy » : cible obligatoire (un STALWART n'est pas ciblable).
#  - Pas de limite imprimee (le cout le borne).


def GetAbilities() -> Sequence['Ability']:

    def deux_compteurs(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return effect.this.GetCounters('charge') >= 2

    def nunchaku(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        Faces.GiveStatus([t for t in effect.targets if t is not None], "Stunned", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.ThisEnterPlayWithCounters(3, 'charge'),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            nunchaku,
            conditions=[deux_compteurs],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 2, 'charge'))
        .SetTarget(Enemy, canbe_stunned=True),
    ]
