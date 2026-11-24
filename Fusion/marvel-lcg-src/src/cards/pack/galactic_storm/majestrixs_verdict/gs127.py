from . import *

# Royal Cape of the Shi'ar — ATTACHEMENT (Majestrix's Verdict). ARMOR. 2 icones de boost.
# Attach to Deathbird.
# Attached character gets +2 hit points and gains retaliate 1.
# Response: After Lilandra attacks Deathbird, spend a [energy] resource → attach this card to Lilandra.
#
# Cartes de reference :
#  - « Attach to X » : `AttachToFaceWhenPutIntoPlay(CardFinder(name=..))`, modele 07035 Distracting Taunts.
#  - « Attached character gets +2 hit points and gains retaliate 1 » : `GiveKeywordToAttached("Character",
#    health=2, retaliate=1)` (modele 07035 pour health, sk148 pour retaliate) : « Attached CHARACTER » vaut pour
#    Deathbird comme pour Lilandra une fois la Cape passee sur elle.
#  - Response : helper `AttacherALilandra("Y")`, modele 07035 (`AfterUnitAttackUnit(Response)` + `SetCost`).
#  - icone [energy] (eclair) : verifiee par decoupe contre sk008 (RES=Y, meme auteur).
#
# ⚠ Mots-pieges : « Attached CHARACTER » (pas « Deathbird ») ; « After LILANDRA attacks DEATHBIRD » (une autre
# attaque ne declenche rien) ; « spend a [energy] resource » (coût colore, pas 1 ressource quelconque).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=DEATHBIRD, card_type=Villain)),
        *AbilityFactory.GiveKeywordToAttached("Character", health=2, retaliate=1),
        AttacherALilandra("Y"),
    ]
