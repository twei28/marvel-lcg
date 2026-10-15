from . import *

# Sectarian Practices (x3, 188) — TRAITRISE. 1 icone Y.
# When Revealed: Choose a card in play with a "When Revealed" ability and resolve that ability. If you
#   cannot, this card gains surge.
#
# Cartes de reference :
#  - resolution du « When Revealed » d'une autre carte : **`sk046`** Mole / **`27083`** (`Faces.ResolveAbility`),
#    via le helper `ChoisirEtResoudreRevelation` ;
#  - « If you cannot, this card gains surge » : **`skrull_empire/sk103`** (`ThisCardGainSurge(effect)`).
#
# ⚠ Mots-pieges : « a card IN PLAY » (les cartes de la table ; ni la defausse ni cette carte) ; « that ability »
# (l'effet seul) ; « IF YOU CANNOT » = aucune carte en jeu n'a de When Revealed (ou le choix est refuse) ;
# c'est le joueur qui revele la carte qui choisit.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if not ChoisirEtResoudreRevelation(effect, joueur):
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
