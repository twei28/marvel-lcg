from . import *

# hs051 Stinger Stab

def GetAbilities() -> Sequence['Ability']:
    def trouver(effect: 'Effect') -> 'CardFace|None':
        scorpion, queue = ScorpionEtQueue(effect)
        if scorpion is not None:
            return scorpion
        trouves = Worlds.FindCardsOnField(effect, name="Scorpion")
        return trouves[0] if trouves else None

    def complote(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        scorpion = trouver(effect)
        if scorpion is None:
            return
        etourdi = joueur.GetIdentity().IsStunned()

        bonus = SchemeProperty(additional_value=2 if etourdi else 0)
        scorpion.DoSchemes(joueur, effect, property=bonus)

    def attaque(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        scorpion = trouver(effect)
        if scorpion is None:
            return
        scorpion.DoAttackYou(joueur, effect)
        identite = joueur.GetIdentity()
        if identite.IsStunned():
            Faces.GiveStatus([identite], "Confused", effect)

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", complote),
        AbilityFactory.WhenThisRevealed("Hero", attaque),
    ]
