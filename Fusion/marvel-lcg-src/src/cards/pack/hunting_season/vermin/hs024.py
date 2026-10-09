from . import *

# hs024 Rabid Assault
# When Revealed (Alter-Ego): Vermin schemes. When Revealed (Hero): Vermin attacks you.
# If there are no RAT minions engaged with you, this card gains surge.

def GetAbilities() -> Sequence['Ability']:

    def surge_si_aucun_rat(effect: 'Effect', joueur: 'Player') -> None:
        if not RatsEngages(joueur):
            ThisCardGainSurge(effect)

    def complote(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilain = Worlds.FindCardOnField(effect, card_type=Villain)
        if vilain is not None:
            vilain.DoSchemes(joueur, effect)
        surge_si_aucun_rat(effect, joueur)

    def attaque(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilain = Worlds.FindCardOnField(effect, card_type=Villain)
        if vilain is not None:
            vilain.DoAttackYou(joueur, effect)
        surge_si_aucun_rat(effect, joueur)

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", complote),
        AbilityFactory.WhenThisRevealed("Hero", attaque),
    ]
