from . import *

# The Bronx (U3) — LIEU Uptown (environnement LOCATION).
# Each attack in The Bronx gains overkill.
#
# Cartes de reference : `AbilityFactory.UnitAttackGainKeyword` (game/ability/factory/do_attack.py : `Message.CheckIfAttackMessageHasKeyword` +
# `message.GainOverKill(effect)`), pu035 Lower East Side (« chaque personnage dans ce lieu » : `JoueurDuPersonnage` + `Ville.Occupe`), the_big_apple/pu020.
# ⚠ Mots-pieges :
#  - « EACH attack IN The Bronx » : toute attaque dont l'attaquant OU la cible fait partie d'un joueur present a The Bronx : un heros ou un allie qui attaque,
#    un sbire engage avec ce joueur, le CAPO de la rangee quand il l'attaque (la cible est un personnage de ce joueur) ; pas les attaques d'autres lieux ;
#  - c'est un mot-cle donne a l'attaque (overkill), pas un effet : lu par le moteur via `CheckIfAttackMessageHasKeyword` ;
#  - continu : aucune limite, aucun cout.

def GetAbilities() -> Sequence['Ability']:

    def dans_le_bronx(effect: 'Effect', message: 'Message.CheckIfAttackMessageHasKeyword') -> bool:
        faces = [message.attacker, *list(message.targets or [])]
        for face in faces:
            joueur = JoueurDuPersonnage(face)
            if joueur is not None and Ville.Occupe(effect, joueur, effect.this):
                return True
        return False

    return [
        Ability(AbilityType.NonKeyword, Message.CheckIfAttackMessageHasKeyword, [dans_le_bronx],
                lambda effect, message: message.GainOverKill(effect)),
    ]
