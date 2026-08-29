from . import *

# The Gatherer
# Interrupt: When you spend The Gatherer to pay for a Squirrel Girl card,
#   heal 1 damage from your identity.
#
# 28/08/2026 : meme garde que The Forager (sg006) — la ressource est
# universelle, le soin ne l'est pas.
#
# La depense est portee par l'identite (« Squirrel Aid ») pour tenir la limite
# d'un ecureuil par carte : l'effet se lit donc sur le DEPART du jeu de cet
# ecureuil, quand la marque de depense le designe.
#
# ECART DE TEXTE ASSUME (28/08/2026) : meme cas que The Forager (sg006) — la
# carte dit « Interrupt / When », le moteur ecoute AfterCardLeavePlay, faute
# de crochet « quand tu depenserais ». Sans consequence observable.
# « your identity » et non « Squirrel Girl » : le code soigne bien
# GetIdentity(), donc la face en jeu quelle que soit la forme.

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
