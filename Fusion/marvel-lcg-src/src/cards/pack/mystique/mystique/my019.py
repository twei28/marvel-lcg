from . import *

# Mother and Son! (Mere et Fils !) : EVENEMENT BASIQUE (TACTIC.), cout 2, [physical] [mental]. Team-Up (Nightcrawler and Mystique). Max 1 per deck. FR seul (absent de l'EN beta).
# Hero Action: Stun and confuse an enemy.
#
# CARTES DE REFERENCE
#  - `47022` Jubilee / `12020` Swarm Tactics : `desc.TeamUp` + `.SetTarget("TeamUp")` (RECETTES : le chargeur l'exige) puis `.SetTarget2(Enemy, ..)` pour la cible suivante.
#  - `01083` : `Faces.GiveStatus(cibles, "Stunned", effect)` ; meme appel pour "Confused".
#
# TEXTE CONTRE CODE
#  « Team-Up (Nightcrawler and Mystique) » : les DEUX personnages (identite ou allie) en jeu ; `desc.TeamUp = "Nightcrawler;Mystique"`. « STUN AND CONFUSE an enemy » : le MEME ennemi recoit les deux cartes d'etat
#    (sonne ET desoriente). « Max 1 per deck » : `desc.MaxPerDeck` (constructeur de deck).
#  Chiffres : cout 2.


def GetAbilities() -> Sequence['Ability']:

    def mother_and_son(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        ennemis = effect.targets2
        Faces.GiveStatus(ennemis, "Stunned", effect)
        Faces.GiveStatus(ennemis, "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            mother_and_son,
        ).SetPlay().SetLabel()
        .SetTarget("TeamUp")
        .SetTarget2(Enemy),
    ]
