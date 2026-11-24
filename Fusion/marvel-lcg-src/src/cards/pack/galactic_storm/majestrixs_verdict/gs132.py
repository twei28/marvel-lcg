from . import *

# Private Audience — MANIGANCE ANNEXE (Majestrix's Verdict), menace de depart 3[per_hero]. Acceleration.
# Allies cannot attack the villain or thwart the main scheme.
#
# Cartes de reference :
#  - Acceleration : BASE AUTOMATIQUE (`desc.Acceleration`) ; icone comparee par decoupe a sk100 Emperor's Throne
#    (croix + pointe + barre).
#  - « Allies cannot attack X » : `UnitCannotAttackTarget(Ally, cannot_attack=Villain)`, modele OFFICIEL 49039
#    Selene ; « cannot thwart X » : `UnitCannotThwartTarget(Ally, cannot_thwart=MainScheme)`, modele OFFICIEL
#    55061 Puppet Master.
#
# ⚠ Mots-pieges : « ALLIES » (les heros, eux, le peuvent) ; « the VILLAIN » (un sbire reste attaquable) ;
# « the MAIN scheme » (les annexes restent contrables par les allies).


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.UnitCannotAttackTarget(Ally, cannot_attack=Villain),
        *AbilityFactory.UnitCannotThwartTarget(Ally, cannot_thwart=MainScheme),
    ]
