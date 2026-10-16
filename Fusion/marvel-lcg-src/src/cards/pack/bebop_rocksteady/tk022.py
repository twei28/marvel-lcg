from . import *

# Lay the Beatdown

def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect)

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()

        def indirects(targets):
            # « Deal 2 indirect damage to your hero » : au HEROS seulement, en degats
            # indirects (TODO-QUESTION Q3, bebop-questions.md).
            identite.TakeDamage(this, DamageProperty(damage=2, is_indirect_damage=True), effect)

        def etourdir(targets):
            Faces.GiveStatus([identite], "Stunned", effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Deal 2 indirect damage to your hero", indirects),
            AbilityFactory.ForChoiceAbility("Stun your hero", etourdir),
        )

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
    ]
