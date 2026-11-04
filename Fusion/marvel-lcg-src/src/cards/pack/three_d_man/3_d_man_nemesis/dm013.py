from . import *

# * Magnitude — SBIRE nemesis (N 2/5). SKRULL. Toughness.
# [star] Magnitude's attacks gain ranged.
# When Defeated: Shuffle each other SKRULL card from the discard pile into the
#   encounter deck.
#
# CARTES DE REFERENCE
#  - « attacks gain ranged » : **`sk070`** Emperor Dorrek I (meme mot-clef,
#    meme trait SKRULL) : `AbilityFactory.UnitAttackGainKeyword("This",
#    ranged=True)`, sans aucune valeur a ajouter (le [star] renvoie juste au
#    texte imprime).
#  - « Shuffle each OTHER <trait> card from the discard pile into the
#    encounter deck » : **`sl036`** Countless Numbers (`Worlds.
#    GetEncounterDiscardPileCards` + `CardFinder2(trait, CardFace).Checks(..)`
#    + `Faces.ShuffleAllTo(faces, "EncounterDeck", effect)`).
#  - « When Defeated » sur un sbire : **`27091`** Shifting Apparition
#    (`AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This",
#    ..)`).
#  - Toughness : natif (`desc.Toughness`), aucun module.
#
# TEXTE CONTRE CODE
#  « each OTHER SKRULL card » : Magnitude vient d'etre defaussee par sa propre
#  defaite au moment ou cette capacite se resout — elle figure donc dans la
#  defausse de rencontre consultee, et « other » l'exclut explicitement de la
#  recherche (sinon elle se remelangerait elle-meme). Le trait SKRULL couvre
#  minions ET traitrises/manigances portant ce trait, pas seulement les
#  sbires : `CardFinder2("SKRULL", CardFace)`, pas `Minion`.


def GetAbilities() -> Sequence['Ability']:

    def quand_vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        this = effect.this
        faces = [
            f for f in CardFinder2("SKRULL", CardFace).Checks(Worlds.GetEncounterDiscardPileCards(effect))
            if f is not this
        ]
        if faces:
            Faces.ShuffleAllTo(faces, "EncounterDeck", effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", ranged=True),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            quand_vaincu,
        ),
    ]
