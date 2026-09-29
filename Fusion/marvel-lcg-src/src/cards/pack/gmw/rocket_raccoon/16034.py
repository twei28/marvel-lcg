from . import *

# Battery Pack

def GetAbilities() -> Sequence['Ability']:

    def battery_pack(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        upgrade = effect.targets[0].CastTo(Upgrade)
        # FAQ (MC4DB, 29/09/2026) : « the card that an all-purpose counter is
        # on defines the type of that counter » -- sur Bambino (Uses ammo) le
        # compteur deplace devient un ammo, pas un charge orphelin.
        Faces.PlaceCountersOn([upgrade], 1, 'all-purpose', effect)


    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, "charge"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            battery_pack
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Upgrade, trait="TECH", another=True, from_where=["YouControlCards"])
        .SetCostFunc(CostFunc.Counter("This", 1, "charge")),
    ]

