from ..commun import *

# Set The Syndicate (pack MC×DC 2026) : six sbires lies par la meme aptitude « When Defeated ».
#
# « When Defeated : Choose a CRIMINAL minion. That minion activates against the player it is engaged with. »
# Cartes de reference : sk167 (`WhenUnitBeDefeated(WhenDefeated, "This", ...)`), jigsaw/pu068 (activation des sbires
# engages : `DoActivate(joueur, effect)`), sm/sinister_six (choix par le premier joueur).
#
# ⚠ « Choose a CRIMINAL minion » : n'importe quel sbire CRIMINAL en jeu ENGAGE avec un joueur, SAUF celui qui vient
# d'etre vaincu ; le texte ne dit pas qui choisit : le PREMIER JOUEUR (regle generale de la RR). Aucun candidat = rien.

def DefaiteSyndicate() -> 'Ability':

    def apres_defaite(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this
        candidats = [m for m in Worlds.GetOnFieldMinions(effect)
                     if m is not this and m.HasTrait("CRIMINAL") and m.GetEngagedPlayer() is not None]
        if not candidats:
            return
        premier = Worlds.GetFirstPlayer(effect)
        choisi = candidats[0] if len(candidats) == 1 else premier.AskChooseFace(candidats, effect)
        if choisi is not None:
            choisi.CastTo(Minion).DoActivate(choisi.GetEngagedPlayer(), effect)

    return AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", apres_defaite)
