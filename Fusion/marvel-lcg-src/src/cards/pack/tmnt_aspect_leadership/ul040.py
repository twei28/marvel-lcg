from . import *

# * Weasel In — MANIGANCE ANNEXE DE JOUEUR Leadership (TMNT Aspects, Inkwire), cout 0, [wild].
# Menace de depart 2 par joueur (icone « par joueur » imprimee : `StartingThreat = "2*"`).
# Victory 0.
# When Defeated: Shuffle the set-aside [[WEASEL]] allies into the encounter deck.
#
# MOTS-CLES (fiches lues AVANT le code)
#  - Linked : fiche linked.md. Les trois allies WEASEL (`ul041` Mushroom, `ul042` Zanna, `ul043` Zink)
#    portent `desc.Linked = "ul040"` : le moteur les fabrique MIS DE COTE (`world.aside_deck`) des que
#    Weasel In est fabriquee (`CardFactory.GenerateCard`, `create_linked_faces`). Aucune extension moteur.
#  - Victory : fiche victory.md, `desc.Victory = "0"` lu par le moteur.
#
# CARTES DE REFERENCE
#  - `49020` New Recruits : manigance de joueur a cout 0, `CanPlayThisSchemeCard()`, « When Defeated » sur
#    les allies mis de cote = `WhenSchemeBeDefeated(WhenDefeated, "This", op)`.
#  - `bk013` Morph : une carte ALLIE melangee dans le deck de rencontre = `Faces.ShuffleAllTo(faces,
#    "EncounterDeck", effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « THE set-aside WEASEL allies » : TOUS les allies WEASEL mis de cote (les trois lies), en une fois.
#  ⚠ « into the ENCOUNTER deck » : melanges dedans (pas sur le dessus).
#  ⚠ Pas de restriction de jeu imprimee (contrairement a New Recruits) : jouable par toute identite.


def GetAbilities() -> Sequence['Ability']:

    def weasel_in(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this, message)
        belettes = [f for f in effect.world.aside_deck.Get()
                    if Ally.IsType(f) and f.HasTrait("WEASEL")]
        if belettes:
            Faces.ShuffleAllTo(belettes, "EncounterDeck", effect)

    return [
        AbilityFactory.CanPlayThisSchemeCard().SetPlay(),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            weasel_in,
        ),
    ]
