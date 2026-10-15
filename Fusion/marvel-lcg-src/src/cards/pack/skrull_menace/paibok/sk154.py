from . import *

# * Devos the Devastator — SBIRE (Paibok). ELITE. PV 5, MNG 1, ATQ 4, 4 icones de boost.
# Forced Response: After a status card is placed on a friendly character, Devos the Devastator
#   activates against the player who controls that character.
#
# Cartes de reference :
#  - Reponse apres une carte d'etat : `AbilityFactory.AfterStatusCardPlaceOn(type, who, status, op)`
#    (recette RECETTES-MOTEUR §1 « statut », modele `50144`) ; ici SANS filtre de statut (« a status
#    card ») et sur tout personnage.
#  - « activates against the player » : **`aos 50141`** Gravitational Pull / `Enemy.DoActivate(player,
#    effect)` (enemy.py:208, attaque en heros, manigance en alter ego, regle native).
#
# ⚠ Mots-pieges : « FRIENDLY character » = un personnage qui appartient a un JOUEUR (identite, allie) :
# un ennemi qui recoit un statut (Paibok Robuste, par exemple) ne le declenche PAS ; « the player who
# CONTROLS THAT character » (pas le premier joueur, pas celui qui a pose le statut) ; « activates » =
# attaque OU manigance selon la forme ; tout statut compte : Sonne, Desoriente, Robuste.


def GetAbilities() -> Sequence['Ability']:

    def ami(effect: 'Effect', message: 'Message.AfterStatusCardPlaceOn') -> bool:
        Unused(effect)
        return Player.IsType(message.trigger.GetControlByOrOwner())

    def active(effect: 'Effect', message: 'Message.AfterStatusCardPlaceOn') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.trigger.GetControlByOrOwner()
        if this.IsInPlay() and Player.IsType(joueur):
            this.DoActivate(joueur, effect)

    return [
        AbilityFactory.AfterStatusCardPlaceOn(AbilityType.ForcedResponse, "Character", None, active, conditions=[ami]),
    ]
