from . import *

# * Chameleon (CRIMINAL, MAGGIA)
# [star] Chameleon gets +X SCH, where X is the highest THW value among
#   characters in play.
# When Revealed: Chameleon schemes.
#
# Modeles : 27067 Sand Clone (ThisGainKeyword avec fonction de valeur),
# 32117 Master Mold's Children (DoSchemes). Le THW n'existe que sur les
# personnages amis (heros, allies) : un alter-ego ou un ennemi vaut 0. La
# valeur se recalcule a chaque entree/sortie d'un personnage ami en jeu et a
# chaque changement de forme (OnEvent.Form ecoute aussi Enter/LeavePlay).
# ⚠ `OnEvent.Form` refuse une UNION de types (AttributeError 'UnionType' has
# no attribute 'IsType') : on passe la classe mere Friend (identites + allies).

def GetAbilities() -> Sequence['Ability']:

    def plus_haut_thw(effect: 'Effect', ui: List['CardFace']) -> int:
        meilleur = 0
        for unite in Worlds.GetOnFieldFriendlyCharacters(effect):
            if HasThwart.IsType(unite):
                meilleur = max(meilleur, unite.thwart)
        return meilleur

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        this.DoSchemes(message.GetToPlayer(), effect)

    return [
        AbilityFactory.ThisGainKeyword(
            plus_haut_thw,
            scheme=1,
            change_on_event=OnEvent.Form(Friend),
        ),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
