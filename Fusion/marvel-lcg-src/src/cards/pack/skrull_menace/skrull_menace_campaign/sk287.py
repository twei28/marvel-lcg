from . import *

# Skrull Shapeshifter — AMELIORATION de campagne (Protection / Campaign, n° 287). Cout 1. NON unique. CONDITION.
# Play under any player's control.
# Your identity gains the SKRULL trait.
# Interrupt: When you would be defeated, set your hit point dial to 1 instead. Then, discard this card.
#
# Cartes de reference :
#  - **`cw/56013`** : « Play under any player's control » = `CanPlayThisUpgradeCard("Players")` ; « You get +3 hit
#    points » = `GiveKeywordToAttached("You", ...)` : ici `trait="SKRULL"` (l'identite = les DEUX faces).
#  - **`cap/03008`** Captain America's Helmet : « When X would be defeated, set his hit point dial to 1 instead.
#    Then, discard this card » = `WhenUnitWouldBeDefeated(Interrupt, ...)` + `message.SetBeInstead(effect)` +
#    `SetHealth(1, effect)` + `Faces.DiscardAll([this], effect)`.
#  - **`wolv/35006`** « I Got Better » : « When YOU would be defeated » = cible `"You"` (l'identite du porteur).
#
# ⚠ Mots-pieges :
#  - « YOUR IDENTITY gains SKRULL » : l'identite, quelle que soit sa forme (heros ET alter ego : le contre-cas
#    dans l'autre forme est exige, RECETTES §3) ;
#  - « When you would be defeated » : l'identite du porteur seulement, pas un allie ; « INSTEAD » : la defaite
#    n'a pas lieu ; « set your hit point dial to 1 » (PV restants = 1, pas un soin de 1) ;
#  - « THEN, discard this card » : defaussee APRES le remplacement.


def GetAbilities() -> Sequence['Ability']:

    def sauvetage(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        identite = this.GetBindFace().CastTo(Unit2)
        message.SetBeInstead(effect)
        identite.SetHealth(1, effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard("Players"),
        *AbilityFactory.GiveKeywordToAttached("You", trait="SKRULL"),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.Interrupt,
            "You",
            sauvetage,
        ),
    ]
