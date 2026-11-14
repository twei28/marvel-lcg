from . import *

# * Resurrection Altar — SOUTIEN, cout 1, [mental]. HAND. LOCATION. Unique. x1 (Elektra 10/15).
# Interrupt: When you would be defeated, remove this card from the game -> set your hit point dial to 9 instead. Find your
# obligation and reveal it.
#
# CARTES DE REFERENCE
#  - « When you would be defeated ... instead » : `35006` I Got Better (`WhenUnitWouldBeDefeated(Interrupt, "You", op)
#    .SetTarget("YourIdentity")` + `message.SetBeInstead(effect)` + `SetHealth(n)`).
#  - « remove this card from the game » : `Faces.RemoveAllFromGame([this], effect)` (`mf013`, `nt012`).
#
# TEXTE CONTRE CODE
#  ⚠ « When you would be DEFEATED » : TOUTE cause (attaque, degats d'une carte, consequents), pas seulement une attaque d'ennemi
#    (35006 limite a une attaque d'ennemi par ses conditions : ici AUCUNE condition).
#  ⚠ « set your hit point dial to 9 INSTEAD » : la defaite n'a pas lieu (`SetBeInstead`) et les PV restants valent 9 (pas « soigne 9 »).
#    9 = les PV maximum des deux faces d'Elektra, jamais plus.
#  ⚠ « remove this card FROM THE GAME » : hors du jeu pour la partie (pas la defausse).
#  ⚠ « Find your obligation and reveal it » : SANS EFFET pour l'instant. L'obligation 63028 n'a pas de scan officiel publie : decision
#    utilisateur du 14/11/2026, on ne la monte pas (le set nemesis 63029-63033, lui, est monte). A coder le jour ou elle sort.
#  Chiffres : cout 1, PV remis a 9.


def GetAbilities() -> Sequence['Ability']:

    def autel(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        identite = effect.targets[0].CastTo(Unit2)
        Faces.RemoveAllFromGame([effect.this], effect)
        message.SetBeInstead(effect)
        identite.SetHealth(9, effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.Interrupt,
            "You",
            autel,
        ).SetTarget("YourIdentity"),
    ]
