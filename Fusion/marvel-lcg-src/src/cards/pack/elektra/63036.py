from . import *

# Misdirect — TRAITRISE, aspect Justice (Elektra Natchios 36). Linked (Double-Cross).
# When Revealed: Heal 4 damage from an identity. This card gains surge.
# [star] Boost: Stun an enemy.
#
# CARTES DE REFERENCE
#  - `sk039` : `joueur.ChooseAbilities(effect, ForChoiceAbility(...).SetTarget(Enemy, canbe_stunned=True))` + `Faces.GiveStatus(.., "Stunned")`.
#  - `mf004` : `.SetTarget(Identity, canbe_heal=True)` pour soigner une identite.
#
# TEXTE CONTRE CODE
#  ⚠ « from AN IDENTITY » : n'importe quelle identite (celle d'un autre joueur aussi), 4 points, pas « votre ».
#  ⚠ « Stun AN ENEMY » : vilain ou sbire, au choix du joueur a qui la carte est revelee.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Heal 4 damage from an identity",
                lambda cibles: this.HealthUnits(cibles, 4, effect),
            ).SetTarget(Identity, canbe_heal=True),
        )
        this.GainSurge(1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Stun an enemy",
                lambda cibles: Faces.GiveStatus(cibles, "Stunned", effect),
            ).SetTarget(Enemy, canbe_stunned=True),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
