from . import *

# Psychological Torture — traitrise, boost 2. « When Revealed: Discard cards from the top of your deck until you have discarded 3 cards
# with the same printed resource type. If you run out of cards in your deck this way, the villain schemes. »
# Cartes de reference : `Player.DiscardDeckTopCard` (player_action.py:1651), `Worlds` (complot du vilain : `ProcessVillainScheme`).
# ⚠ « same printed resource type » : on compte par COULEUR imprimee (R, B, Y) ; un wild compte pour chacune (lecture en attente).


def GetAbilities() -> Sequence['Ability']:

    def psychological_torture(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        compte = {"R": 0, "B": 0, "Y": 0}
        while True:
            taille = joueur.player_deck.GetSize()
            if taille <= 0:
                break
            face = joueur.DiscardDeckTopCard(effect)
            if face is not None and ClassCard.IsType(face):
                res = face.printed_resource
                for couleur in compte:
                    if res.GetColor(couleur, convert_green_res=False) > 0 or res.GetColor("G", convert_green_res=False) > 0:
                        compte[couleur] += 1
                        if compte[couleur] >= 3:
                            return
            if taille == 1:
                break  # ce tirage a VIDE le deck (le moteur le remelange apres coup) : « you run out of cards »
        villain = Worlds.FindVillain(effect)
        if villain is not None:
            villain.DoSchemes(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, psychological_torture),
    ]
