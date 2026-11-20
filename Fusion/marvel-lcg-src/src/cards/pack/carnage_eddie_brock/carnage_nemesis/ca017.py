from . import *

# * Death Spiral : ATTACHEMENT (CONDITION.), boost 2. Set « Carnage Nemesis ».
# Attach to Torment. Otherwise, this card gains surge.
# [star] Forced Interrupt: When Torment attacks a friendly character, if there is an ally or PERSONA support with the same classification as that character under your control or in your hand (identity-specific, aspect, or basic), cancel this attack and discard that card instead.
# Hero Action: Spend [mental][physical] resources -> discard this card.
#
# CARTES DE REFERENCE
#  - « Attach to X. Otherwise, gains surge » : `AttachToFaceWhenPutIntoPlay(CardFinder(..), if_cannot_gain_surge=True)` (attachment.py:47) ; modele de forme `sk242` (attache a un sbire d'un trait).
#  - « When the attached enemy attacks → cancel » : `sk242` : `WhenUnitWouldAttack(ForcedInterrupt, "AttachedEnemy", op)` + `message.CancelThisAttack(effect)` (`hf120`).
#  - « Hero Action: Spend [mental][physical] → discard this card » : `sk147` (Distracted) : `PlayerActionToDiscardThis(HeroAction).SetCost(Cost("BB"))` ; ici `Cost("BR")` ([mental]=B, [physical]=R, verifie contre une carte du pack : ca003 RES B, ca004 RES R).
#
# TEXTE CONTRE CODE
#  « Attach to TORMENT. Otherwise → surge » : seul Torment (le sbire du set) convient ; absent, la carte gagne surge. « [star] » : capacite propre a la carte (`NonKeywordStar` dans la fiche special.md : le moteur n'en fait rien de plus ; l'Interruption forcee est
#    bien portee par la carte). « When TORMENT attacks a FRIENDLY character » : l'attache (`"AttachedEnemy"`) attaque une identite ou un allie du joueur. « an ALLY OR PERSONA SUPPORT with the SAME CLASSIFICATION as THAT CHARACTER, under your control OR IN YOUR HAND » :
#    helper `CartesSacrifiables` (classe imprimee ; identite = `Hero`) ; « cancel this attack AND discard THAT CARD INSTEAD » : l'attaque est annulee et la carte choisie par le joueur est defaussee. Sans carte sacrifiable, l'attaque a lieu.
#    Meme texte que Torment : si les deux sont en jeu, la premiere annule l'attaque et la seconde n'a plus rien a annuler (une seule carte defaussee). « Hero Action » : forme heros seulement ; cout [mental][physical] (B + R).
#  Chiffres : boost 2.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Minion, name=NOM_TORMENT),
            if_cannot_gain_surge=True,
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "AttachedEnemy",
            EchangerContreUnSacrifice,
            conditions=[CibleAmie],
        ),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("BR")),
    ]
