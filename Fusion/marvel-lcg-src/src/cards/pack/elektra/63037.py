from . import *

# Sabotage — TRAITRISE, aspect Justice (Elektra Natchios 37). Linked (Double-Cross).
# When Revealed: Remove 3 threat from the main scheme. This card gains surge.
# [star] Boost: Confuse an enemy.
#
# CARTES DE REFERENCE
#  - `sk025`/`sk009` : `this.RemoveThreatFromSchemes("MainScheme", N, effect)`.
#  - `sk039` : choix d'un ennemi + `Faces.GiveStatus(.., "Confused")`.
#
# TEXTE CONTRE CODE
#  ⚠ « from the MAIN scheme » : le complot principal, pas une annexe ; 3 points (pas moins que la menace presente).
#  ⚠ « Confuse AN ENEMY » : vilain ou sbire, au choix du joueur a qui la carte est revelee.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(message)
        this.RemoveThreatFromSchemes("MainScheme", 3, effect)
        this.GainSurge(1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Confuse an enemy",
                lambda cibles: Faces.GiveStatus(cibles, "Confused", effect),
            ).SetTarget(Enemy, canbe_confused=True),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
