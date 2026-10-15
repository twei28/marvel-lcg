from . import *

# Experiment Subject — TRAITRISE (Standard Skrull). 1 icone de boost.
# When Revealed: Discard an upgrade you control. If no card was discarded this way, the villain schemes.
#
# Cartes de reference :
#  - **`01188`** Caught Off Guard : `player.DiscardControlCards(effect, upgrade=True)` rend la carte defaussee
#    (ou None), meme repli « sinon ... » ; ici le repli est un complot, pas un surge.
#  - « the villain schemes » : **`sk098`** Impostor (`mechant.DoSchemes(joueur, effect)`).
#
# ⚠ Mots-pieges : « an UPGRADE you control » (amelioration seulement : pas un soutien, pas un allie ; le joueur
# choisit laquelle) ; « YOU control » (celles du joueur qui revele) ; « no card was discarded THIS WAY » : aucune
# amelioration, ou defausse empechee ; « the villain schemes » CONTRE ce joueur (en alter-ego comme en heros).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = joueur.DiscardControlCards(effect, upgrade=True)
        if face is None:
            mechant = LeMechant(effect)
            if mechant is not None:
                mechant.DoSchemes(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
