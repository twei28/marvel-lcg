from . import *

# Black Belt
# Play only if any player controls a [[Martial Artist]] card.
# Attach to a friendly character. Max 1 per character.
# Attached character gets +1 hit point and gains the [[Martial Artist]] trait.
#
# `SetCondition` n'offre que des conditions portant sur VOTRE zone
# (`only_if_you_control_*`). Ici le texte dit « ANY player », donc on ecrit la
# condition a la main et on la passe a l'option de mise en jeu.

def GetAbilities() -> Sequence['Ability']:

    def un_joueur_controle_un_martial_artist(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        for player in Worlds.GetPlayers(effect):
            for face in player.GetControlCardsByType(ally=True, upgrade=True, support=True, identity=True):
                if face.HasTrait('MARTIAL ARTIST'):
                    return True
        return False

    return [
        # CORRECTIF (10/10/2026) : « Attach to a FRIENDLY character ».
        # `"Character"` laissait poser la ceinture sur un ennemi (Rhino gagnait
        # 1 PV). Modele : 34007 / 31029, `CanPlayThisUpgradeCard(Friend)`.
        AbilityFactory.CanPlayThisUpgradeCard(
            Friend,
            conditions=[un_joueur_controle_un_martial_artist],
        ),
        *AbilityFactory.GiveKeywordToAttached("Character", health=1, trait="MARTIAL ARTIST"),
    ]
