from . import *

# The Gatherer
# Response: After you spend The Gatherer, heal 1 damage from Squirrel Girl.
#
# La depense est portee par l'identite (« Squirrel Aid ») pour tenir la limite
# d'un ecureuil par carte : la reponse se lit donc sur le DEPART du jeu de cet
# ecureuil, quand la marque de depense le designe.

def GetAbilities() -> Sequence['Ability']:

    def soigner(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        identite = joueur.GetIdentity()
        if identite is not None:
            effect.this.HealthUnits([identite], 1, effect)

    return [
        *Ecureuil(),
        ReponseALaDepense(soigner),
    ]
