from . import *

# Return of the Mask — manigance annexe, menace 3, boost 2. « When Revealed: Find the Black Mask minion. Reveal him and put him into play
# with the first player. Then, each player takes 1 indirect damage. »
# Cartes de reference : `uw014` Directorate X (`Find.FindAndReveal(effect, premier, name=.., card_type=Minion)`, `Worlds.GetFirstPlayer`),
# degats indirects : `Worlds`/joueur `TakeIndirectDamage`. ⚠ Ce n'est PAS « deal a facedown card » : le sbire est REVELE (engage le premier joueur).

NOM_BLACK_MASK = "Black Mask"


def GetAbilities() -> Sequence['Ability']:

    def return_of_the_mask(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        premier = Worlds.GetFirstPlayer(effect)
        Find.FindAndReveal(effect, premier, name=NOM_BLACK_MASK, card_type=Minion)
        for joueur in Worlds.GetPlayers(effect):
            joueur.GetIdentity().TakeIndirectDamage(effect.this, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, return_of_the_mask),
    ]
