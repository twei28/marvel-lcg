from . import *

# Art Museum Heist (1B)  — 1[per_hero] de depart, 9[per_hero] cible.
# [star] X is 1 more than the number of ART attachments on the villain.
#   (escalade +X[per_hero] : EscalationThreat "0" + WhenCalcThisSchemeEscalation,
#   modele 16091b The Art of Evasion, avec Worlds.GetPlayerNumIcon.)
# Forced Response: After an enemy makes an undefended attack against an
#   identity, attach 1 ART attachment on that identity to the villain.
#   (AfterUnitAttackUnit is_undefended_attack=True, modele Dense Forest 04080.)
# If this stage is completed, the players lose the game.

def GetAbilities() -> Sequence['Ability']:

    def escalade(effect: 'Effect') -> int:
        vilain = Worlds.FindVillain(effect)
        nb = len(OeuvresSur(vilain)) if vilain else 0
        return Worlds.GetPlayerNumIcon(effect) * (1 + nb)

    def vol_apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        identite = message.attacked
        vilain = Worlds.FindVillain(effect)
        oeuvres = OeuvresSur(identite)
        if vilain is None or not oeuvres:
            return
        joueur = identite.GetControlByPlayer()
        oeuvre = joueur.AskChooseFace(oeuvres, effect, prompt="Choose an Art attachment to give to the villain") if len(oeuvres) > 1 else oeuvres[0]
        if oeuvre is not None:
            oeuvre.AttachTo2(vilain, effect)

    return [
        AbilityFactory.WhenCalcThisSchemeEscalation(escalade),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            Enemy,
            Identity,
            vol_apres_attaque,
            is_undefended_attack=True,
        ),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
