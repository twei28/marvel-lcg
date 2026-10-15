from . import *

# The Revenge Time — COMPLOT ANNEXE (New Revengers). Menace 2[per_hero], icone ACCELERATION, 2 boosts.
# The villain gains the REVENGER trait.
# When Revealed: Place 1 additional threat here for each REVENGER enemy in play.
#
# Cartes de reference :
#  - Trait donne a une carte en jeu : **`challenges 2421`** Battle of the Bots / **`next_evol 40006`**
#    (`GiveKeywordToInPlayWhenApplyThis(<finder>, trait="...")`).
#  - Menace sur soi selon un compte : `this.PlaceThreatOnSchemes([this], n, effect)` (modele `sk156`).
#  - Icone Acceleration : natif (`desc.Acceleration`), meme forme que Galactic Ambassador (sk156, lecture
#    validee le 15/10/2026).
#
# ⚠ Mots-pieges : « The VILLAIN gains the trait » : le mechant courant ; « for each REVENGER ENEMY IN PLAY »
# (le mechant, devenu Revenger par la 1re phrase, compte lui aussi) ; « ADDITIONAL » : en plus de la menace
# de depart ; le trait disparait avec la carte (constante, pas permanente) ; Skrull Empire (mechants sans PV) :
# le trait va quand meme au mechant.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this.CastTo(EncounterSideScheme)
        nombre = len(EnnemisRevenger(effect))
        if nombre:
            this.PlaceThreatOnSchemes([this], nombre, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Villain, trait=TRAIT_REVENGER),
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
