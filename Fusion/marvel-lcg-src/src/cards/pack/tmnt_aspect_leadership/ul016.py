from . import *

# Naginata — AMELIORATION Leadership (TMNT Aspects, Inkwire), cout 1, [mental]. NINJA. WEAPON.
# Attach to an ally. Max 1 per ally.
# Interrupt: When attached character uses a basic power, exhaust Naginata -> they get +2 to that power for
#   this use.
#
# CARTES DE REFERENCE
#  - `01074` Inspired : « Attach to an ally. Max 1 per ally. » = `CanPlayThisUpgradeCard(Ally)` +
#    `desc.MaxPerUnit = "1"` (regle generique du moteur).
#  - `al012` Gator Aid : meme phrase (« When attached character uses a basic power, exhaust X -> that
#    character gets +1 to that power for this use »), cout `CostFunc.Exhaust("This")`.
#  - `status/cloaked.py` : « uses a basic power » sur le porteur = `WhenUnitUseBasicPower(...,
#    "AttachedCharacter", ...)` + `message.GainValue(n, effect)`, qui route vers ATQ / CTR / DEF.
#
# TEXTE CONTRE CODE
#  ⚠ « Interrupt » (pas Hero Interrupt) : facultative, jouable dans les deux formes.
#  ⚠ « exhaust Naginata » est le COUT : Naginata deja inclinee ne se declenche pas.
#  ⚠ « +2 to THAT power » : le pouvoir de base utilise (ATQ, CTR ou DEF), pour CET usage seulement.
#  ⚠ « they » = le personnage attache (un allie).
#  Aucune limite imprimee (l'inclinaison fait office de limite naturelle).


def GetAbilities() -> Sequence['Ability']:

    def naginata(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.GainValue(2, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Ally),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "AttachedCharacter",
            naginata,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
