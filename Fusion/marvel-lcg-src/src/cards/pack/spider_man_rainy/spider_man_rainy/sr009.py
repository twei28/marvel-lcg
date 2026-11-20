from . import *

# * J. Jonah Jameson — custom « Rainy »
# Alter-Ego Action: Exhaust J. Jonah Jameson -> draw 1 card. If that card had
#   a picture of Spider-Man on it, draw another card.
#
# « a picture of Spider-Man » n'est PAS une donnee du moteur : c'est du
# DESSIN, pas du texte ni un trait. Une version anterieure devinait a la
# place du joueur (« une carte du set signature Spider-Man (Rainy), J. Jonah
# Jameson excepte ») : approximation fausse (une carte du set peut ne montrer
# que l'objet, ex. Web-Shooters ; une carte HORS set peut tres bien montrer
# Spider-Man) — signalee en jeu le 08/11/2026. On pose donc la question au
# joueur, qui REGARDE la carte qu'il vient de piocher dans sa main (`DrawUp`
# la pose face visible) et juge lui-meme, comme le texte imprime le demande.
#
# Carte de reference : shadowland/deadly_contraptions/sl046 (meme fabrique,
# `AskChooseOneText`, pour un choix nomme pose au joueur apres un effet).

def GetAbilities() -> Sequence['Ability']:

    def jameson(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        piochees = initiator.DrawUp(1, effect)
        if not piochees:
            return
        carte = piochees[0]
        montre_spider_man = initiator.AskChooseOneText(
            [True, False], ["Yes", "No"],
            f"J. Jonah Jameson: does \"{carte.name}\" have a picture of Spider-Man on it?",
        )
        if montre_spider_man:
            initiator.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            jameson
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
