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
#  ⚠ « FIND your obligation and reveal it » : 63028 Conditioned by the Hand (montee le 14/11/2026). « Find » lu comme `gs221`
#    Whisper in the Mind (livret Galactic Storm p.4, lecture deja retenue) : deck de rencontre, defausse de rencontre, zone mise de
#    cote ; ni la pile de victoire ni la zone retiree du jeu. Deja en jeu devant Elektra : rien a trouver. « YOUR obligation » :
#    celle du joueur de l'Autel (`obligation_give_to`). Revelee APRES la remise des PV a 9.
#  Chiffres : cout 1, PV remis a 9.


def GetAbilities() -> Sequence['Ability']:

    def autel(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        identite = effect.targets[0].CastTo(Unit2)
        Faces.RemoveAllFromGame([effect.this], effect)
        message.SetBeInstead(effect)
        identite.SetHealth(9, effect)
        joueur = identite.GetControlByPlayer()
        obligation = Search.SearchForCard(
            effect,
            joueur,
            include_encounter_deck=True,
            include_encounter_discard_pile=True,
            include_set_aside=True,
            card_type=Obligation,
            obligation_give_to=joueur,
            check_face_fn=lambda f: not f.card.state.is_revealing,
        )
        if obligation is not None:
            obligation.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.Interrupt,
            "You",
            autel,
        ).SetTarget("YourIdentity"),
    ]
