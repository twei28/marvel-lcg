from . import *

# * Puppet Master — custom « DesignHacker » (sbire némésis de The Thing)
# Puppet Master cannot be attacked while Hulk is in play.
# Forced Response: After Puppet Master is revealed, search the encounter deck
# for Hulk and reveal him.

def GetAbilities() -> Sequence['Ability']:

    def appeler_hulk(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        player = message.GetToPlayer()
        Find.FindAndReveal(
            effect,
            player,
            name="Hulk",
            card_type=Minion,
        )

    def hulk_en_jeu(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        return Worlds.FindCardOnField(effect, name="Hulk", card_type=Minion) is not None

    return [
        AbilityFactory.UnitCannotBeAttacked(
            "This",
            conditions=[hulk_en_jeu],
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            appeler_hulk
        ),
    ]
