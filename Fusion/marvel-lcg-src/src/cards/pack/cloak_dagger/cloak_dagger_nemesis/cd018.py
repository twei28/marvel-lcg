from . import *

# Opposites Attack — custom « DesignHacker » (némésis de Cloak & Dagger)
# When Revealed: Flip each hero to alter-ego form. Then, place 1 threat on the
#   main scheme for each hero flipped this way.


def GetAbilities() -> Sequence['Ability']:

    def opposites_attack(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        heros = Worlds.FindCardsOnField(effect, card_type=Hero)
        bascules = 0
        for face in heros:
            player = face.GetControlByPlayer()
            if player is None or not player.IsHero():
                continue
            player.GetIdentity().ChangeToForm(AlterEgo, effect)
            bascules += 1

        if bascules > 0:
            scheme = Worlds.FindMainScheme(this)
            if scheme:
                this.PlaceThreatOnSchemes([scheme], bascules, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            opposites_attack
        ),
    ]
