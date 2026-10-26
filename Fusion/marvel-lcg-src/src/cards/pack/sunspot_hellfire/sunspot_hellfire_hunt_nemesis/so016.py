from . import *

# Political Persecution — TRAITRISE de l'ennemi juré (TACTIC), boost 1.
# When Revealed: If the Superhuman Mutants Murdering scheme is in play, place 2 threats to that scheme. If it is not in
#   play, place 2 threats to the main scheme.
#
# CARTES DE REFERENCE
#  - `ch020` / `01107` : `this.PlaceThreatOnSchemes([manigance], n, effect)`.
#  - `Worlds.FindMainScheme(effect)` : la manigance principale ; `Worlds.FindCardOnField(effect, name=..)` : une carte nommee en jeu.
#
# TEXTE CONTRE CODE
#  ⚠ « If it is NOT in play » : SINON la manigance principale (jamais les deux).


def GetAbilities() -> Sequence['Ability']:

    def political_persecution(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(message)
        annexe = Worlds.FindCardOnField(effect, name="Superhuman Mutants Murdering", card_type=Scheme2)
        cible = annexe if annexe else Worlds.FindMainScheme(effect)
        if cible:
            this.PlaceThreatOnSchemes([cible], 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            political_persecution,
        ),
    ]
