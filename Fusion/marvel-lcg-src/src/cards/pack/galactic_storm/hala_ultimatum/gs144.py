from . import *

# * Grand-High Pursuer — ATTACHEMENT (Hala Ultimatum), unique. TITLE. Badge +1 ATK. 1 etoile + 2 icones de boost.
# Attach to the villain.
# Attached villain gains retaliate 1.
# Hero Action: Spend [energy][mental][physical] resources → discard this card.
# [star] Boost: If the activating enemy has a tough status card, give it an additional boost card.
#
# Cartes de reference :
#  - « Attach to the villain » : `AttachToFaceWhenPutIntoPlay(Villain)`, modele 01153 Concussion Blasters.
#  - « Attached villain gains retaliate 1 » : `AbilityFactory.GiveKeywordToAttached(Villain, retaliate=1)`,
#    modele 01153 / gs127 Royal Cape of the Shi'ar (meme pack).
#  - « Hero Action: Spend [...] resources -> discard this card » : `PlayerActionToDiscardThis(HeroAction)`
#    + `SetCost(Cost("YBR"))`, modele 01118 Sonic Converter / gs145 (meme pack, memes trois icones).
#  - « If the activating enemy has a tough status card, give it an additional boost card » :
#    `AbilityFactory.WhenCardBecomeBoost("This", ...)` + `message.activating_enemy` + `Faces.HasStatus` +
#    `Faces.GiveFacedownBoostCards`, modele gs083 Optic Blast Cannon pour le declencheur de boost.
#
# ⚠ Mots-pieges : « Attached VILLAIN » (pas « Character » : seul le mechant recoit retaliate) ; « the
# ACTIVATING enemy » peut etre un sbire different du mechant (le boost se lit sur l'activation en cours,
# pas forcement sur le porteur de la carte) ; « an ADDITIONAL boost card » (en plus de celle qui vient
# d'etre retournee, pas a la place).


def GetAbilities() -> Sequence['Ability']:

    def booster(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        ennemi = message.activating_enemy
        if Faces.HasStatus([ennemi], "Tough") > 0:
            Faces.GiveFacedownBoostCards([ennemi], 1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        *AbilityFactory.GiveKeywordToAttached(Villain, retaliate=1),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("YBR")),
        AbilityFactory.WhenCardBecomeBoost("This", booster),
    ]
