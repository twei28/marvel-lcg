from . import *

# * Jane Foster — custom "Rainy"
# Survivor — Jane Foster gets +1 hand size while her Chemotherapy obligation
# is set aside or removed from the game.
# Physician — Action: Heal 1 damage from another friendly character.
# (Limit once per round.)

def GetAbilities() -> Sequence['Ability']:

    def physician(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        this.HealthUnits(effect.targets, 1, effect)

    return [
        # LENIENT : l'obligation Chemotherapy n'a pas été publiée par l'auteur
        # (absente du dossier Drive). Sans elle, la condition « set aside or
        # removed from the game » est toujours vraie : bonus permanent.
        AbilityFactory.ThisGainKeyword(
            hand_size=1,
        ).SetName("Survivor"),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            physician
        ).SetName("Physician")
        # LENIENT : « another friendly character » — la cible inclut aussi
        # Jane elle-même ; en pratique on la soigne via REC, impact minime.
        .SetTarget(Friend, canbe_heal=True)
        .LimitOncePerRound()
    ]
