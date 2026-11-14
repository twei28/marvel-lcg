from . import *

# Wakandan Jumpsuit — AMELIORATION, cout 3, [energy]. ARMOR. TECH. WAKANDA.
# You get +3 hit points.
# Special (thwart): Remove 2 threat from a scheme.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - « You get +N hit points » : `01039` Rocket Boots / `bw013` : `*GiveKeywordToAttached("You", health=N)`.
#  - Special (thwart) : `51010` Kimoyo Beads (`SetLabel('thwart')` + `SetTarget(Scheme2)` +
#    `this.RemoveThreatFromSchemes(effect.targets, N, effect)`).
#
# MOTS-PIEGES
#  - « YOU get +3 hit points » : l'IDENTITE (hero ou alter ego), pas seulement la face heros : `"You"`.
#  - « a scheme » : n'importe quelle manigance (principale ou annexe) : `Scheme2`.
def GetAbilities() -> Sequence['Ability']:

    def combinaison(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=3,
        ),
        AbilityFactory.WhenResolveSpecialAbility(
            "This",
            combinaison,
        ).SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
