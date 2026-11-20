from . import *

# Kree Plasma Rifle — ATTACHEMENT (Hala Ultimatum). WEAPON. Badge +1[star] ATK. 2 icones de boost.
# Attach to the villain.
# [star] Attached villain's attacks gain piercing and ranged.
# Hero Action: Spend [energy][mental][physical] resources → discard this card.
#
# Cartes de reference :
#  - « Attach to the villain » : `AttachToFaceWhenPutIntoPlay(Villain)`, modele 01153 Concussion Blasters.
#  - « Attached villain's attacks gain piercing and ranged » : `UnitAttackGainKeyword("AttachedCharacter",
#    piercing=True, ranged=True)`, modele OFFICIEL 27147 Arm Cannon, repris par gs083 Optic Blast Cannon
#    (meme pack).
#  - « Hero Action: Spend [...] resources -> discard this card » : `PlayerActionToDiscardThis(HeroAction)`
#    + `SetCost(Cost("YBR"))`, modele 01118 Sonic Converter.
#
# ⚠ Mots-pieges : aucune ligne « Boost » n'est imprimee sur cette carte (contrairement a gs144) : l'etoile
# devant « Attached villain's attacks... » renvoie seulement aux icones de boost imprimes (convention Skrull
# Menace), aucun module de Boost a ecrire.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.UnitAttackGainKeyword("AttachedCharacter", piercing=True, ranged=True),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("YBR")),
    ]
