from . import *

# The Harlem Hustle (U2) — PISTE Uptown. Response : While in Harlem, after a character you control makes a basic attack, place a hustle counter here and add 3 threat to
#   the main scheme. Then, if there are 3 or more counters here, add this card to the victory display, reveal the top LEAD card, and draw 1 card.
#
# Cartes de reference : pu078 / gs065 (`AfterUnitUseBasicPower`, `powers=["ATK"]`), leads_the_big_apple (`EnLieu`, `ControlePar`, `CompteurPuisFin`),
# `this.PlaceThreatOnSchemes("MainScheme", 3, effect)` (capos/__init__ : TheRose).
# ⚠ Mots-pieges :
#  - « a character YOU CONTROL » : identite OU allie du joueur porteur de la piste (`ControlePar`), pas ceux des autres joueurs ;
#  - « makes a BASIC attack » : le pouvoir de base ATK (heros ou allie), pas une attaque de carte ;
#  - « place a hustle counter AND add 3 threat » : les deux a CHAQUE attaque, AVANT le test du seuil ; « Then, if 3 or more counters » : le 3e compteur ajoute aussi
#    ses 3 menaces, puis la piste se termine ; « add 3 threat to the main scheme » : le complot principal en jeu, un seul.

def GetAbilities() -> Sequence['Ability']:

    def mon_personnage(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> bool:
        joueur = Joueur(effect)
        return joueur is not None and ControlePar(message.trigger, joueur)

    def apres(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this
        # `FindMainScheme` cherche dans la zone de la carte (la piste est dans l'aire du joueur, le complot dans la zone COMMUNE) : on lit tous les complots du monde.
        complots = Worlds.GetAllMainSchemes(effect.world)
        if complots:
            this.PlaceThreatOnSchemes([complots[0]], 3, effect)
        CompteurPuisFin(effect, Joueur(effect), 'hustle', 3)

    return [
        AbilityFactory.AfterUnitUseBasicPower(AbilityType.Response, Friend, apres, powers=["ATK"], conditions=[EnLieu(LIEU_U2), mon_personnage]),
    ]
