from . import *

# * Black Bolt (Blackagar Boltagon) — custom « Nugget »
# [star] Forced Interrupt: When Black Bolt attacks, discard X cards from each
#   player's deck and the encounter deck. X is equal to Black Bolt's ATK.


def GetAbilities() -> Sequence['Ability']:

    def cri(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        valeur = this.attack
        if valeur <= 0:
            return

        for joueur in Worlds.GetPlayers(effect):
            joueur.DiscardDeckTopCards(valeur, effect)

        Worlds.DiscardEncounterCards(valeur, effect)

    return [
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.ForcedInterrupt,
            "This",
            cri,
        ),
    ]
