from . import *

# Shi'ar Javelin — ATTACHEMENT (Majestrix's Verdict). WEAPON. Badge +1[star] ATK. 1 icone de boost.
# Attach to Deathbird.
# [star] Attached character's attacks gain piercing and overkill.
# Response: After Lilandra attacks Deathbird, spend a [physical] resource → attach this card to Lilandra.
# [star] Boost: If this activation is an attack, it gains piercing and overkill.
#
# Cartes de reference :
#  - badge « +1 ATK » : BASE AUTOMATIQUE `desc.ATK+` (l'etoile renvoie au texte, convention Skrull Menace).
#  - « Attached character's attacks gain piercing and overkill » : `UnitAttackGainKeyword("AttachedCharacter",
#    piercing=True, overkill=True)`, modele OFFICIEL 27147 Arm Cannon (« AttachedVillain »).
#  - Response : helper `AttacherALilandra("R")`, modele 07035.
#  - Boost : `message.would_atk_message.GainPiercing / GainOverKill`, modele OFFICIEL 50160 Supersonic, sous
#    `getattr(.., None)` (RECETTES §1 : pas d'attaque en cours = activation de manigance, rien).
#  - icone [physical] (poing) : verifiee par decoupe contre sk004 (RES=R, meme auteur).
#
# ⚠ Mots-pieges : « IF this activation is an attack » (rien sur une manigance) ; « attached CHARACTER » vaut
# aussi pour Lilandra.


def GetAbilities() -> Sequence['Ability']:

    def percer(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        attaque = getattr(message, "would_atk_message", None)
        if attaque is not None:
            attaque.GainPiercing(effect)
            attaque.GainOverKill(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=DEATHBIRD, card_type=Villain)),
        AbilityFactory.UnitAttackGainKeyword("AttachedCharacter", piercing=True, overkill=True),
        AttacherALilandra("R"),
        AbilityFactory.WhenCardBecomeBoost("This", percer),
    ]
