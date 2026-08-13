from . import *

# Switching Sides

def GetAbilities() -> Sequence['Ability']:

    def switching_sides_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()

        player.AskDiscardFaces(player.GetControlAllies(), (1, 1), effect)
        if Worlds.IsCompetitiveMode(effect):
            # ECART ASSUME, ecrit plutot que silencieux. Le texte complet est :
            # « any player on the enemy team may spend resources equal to that
            # ally's cost to put it into play under their control. If no ally
            # left play this way, this card gains surge. »
            #
            # Racheter l'allie defausse demande une fenetre de paiement offerte
            # a un joueur d'une AUTRE table, ce que le moteur ne sait pas poser.
            # La carte se resout donc comme si personne n'avait paye, ce qui est
            # la seconde moitie de son propre texte : elle gagne deferlement.
            this.GainSurge(+1, effect)


    return [
        AbilityFactory.WhenThisRevealed(
            None,
            switching_sides_revealed
        ),
    ]

