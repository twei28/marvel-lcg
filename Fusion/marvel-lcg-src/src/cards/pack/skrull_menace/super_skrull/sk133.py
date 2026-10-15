from . import *

# Hypnotic Gaze — TRAITRISE x3 (Super-Skrull). 1 icone Y.
# When Revealed: Discard the top 2 cards of your deck. For each [physical]
#   resource discarded this way stun a character you control, for each
#   [mental] resource discarded this way confuse a character you control.
#
# Cartes de reference :
#  - **`hood/24017`** Double Trouble : « Stun a character you control. Confuse a
#    character you control » = `CardFinder(canbe_stunned=True).Checks(player.
#    GetControlCharacters())` + `player.AskChooseFace` + `Faces.GiveStatus` (un
#    choix PAR statut, personnage libre).
#  - **`fne/60084`** Energy Overload : ressource IMPRIMEE lue sur des cartes ;
#    `sk114` : `player.DiscardDeckTopCards(2, effect)` rend les cartes defaussees ;
#    `FacesCounter.GetPrintedResourcesCount(cartes, "R")` compte les ICONES.
#
# ⚠ Mots-pieges : « YOUR deck » (le joueur qui revele) ; « FOR EACH resource »
# (une carte a deux icones physiques = deux etourdissements, un choix chacun) ;
# « a character YOU CONTROL » (heros et allies, pas l'ennemi) ; un personnage
# deja etourdi ne peut pas l'etre deux fois (`canbe_stunned`) : le choix suivant
# porte sur un autre ; ressource IMPRIMEE (R physique, B mental ; le wild ne
# compte pas comme physique ni mental, lecture litterale, voir defs/super_skrull_questions.md).


def GetAbilities() -> Sequence['Ability']:

    def regard(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        defaussees = joueur.DiscardDeckTopCards(2, effect)
        physiques = FacesCounter.GetPrintedResourcesCount(defaussees, "R")
        mentales = FacesCounter.GetPrintedResourcesCount(defaussees, "B")
        for _ in range(physiques):
            cibles = CardFinder(canbe_stunned=True).Checks(joueur.GetControlCharacters())
            unite = joueur.AskChooseFace(cibles, effect)
            if unite:
                Faces.GiveStatus([unite], "Stunned", effect)
        for _ in range(mentales):
            cibles = CardFinder(canbe_confused=True).Checks(joueur.GetControlCharacters())
            unite = joueur.AskChooseFace(cibles, effect)
            if unite:
                Faces.GiveStatus([unite], "Confused", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, regard),
    ]
