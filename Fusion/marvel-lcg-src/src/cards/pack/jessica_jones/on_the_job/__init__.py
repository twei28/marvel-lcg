from cards.pack import *

################################################################################
# Set de rencontre « On the Job » — custom « ekAugust ».
#
# Nouveau mot-cle du pack, INVESTIGATE X : « When revealed, move X threat from
# the main scheme to here. » Le moteur ne connait pas ce mot-cle ; il est donc
# scripte carte par carte via cette fabrique commune.
#
# « Move » = retirer de la manigance principale puis poser ici, en se limitant
# a ce qui a reellement ete retire (une manigance principale a 0 de menace ne
# doit rien donner).
################################################################################


def Investigate(value: int, *, per_hero: bool=False) -> 'Ability':

    def investigate(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        amount = value
        if per_hero:
            amount *= Worlds.GetPlayerNumIcon(effect)

        main = Worlds.FindMainScheme(this)
        if main is None:
            return

        moved = this.RemoveThreatFromSchemes([main], amount, effect)
        if moved:
            this.PlaceThreatOnSchemes([this], moved, effect)

    return AbilityFactory.WhenThisRevealed(
        None,
        investigate,
    )
