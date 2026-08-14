from . import *

# Recharging

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Heal 3 damage from each copy of Electro in play. If
        # 3 or fewer damage was healed this way, this card gains surge. »
        #
        # « each copy » : le vilain ET les sbires, tous nommes Electro — c'est
        # Electricity Clones qui rend cette accumulation possible.
        this = effect.this.CastTo(Treachery)
        electros = Worlds.FindCardsOnField(effect, name="Electro", card_type=Unit2)
        soignes = this.HealthUnits(electros, 3, effect)
        if not soignes or soignes <= 3:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
