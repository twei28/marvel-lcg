from . import *

# Darkhold (module Darkhold). Attachement MAGICAL BOOK, +1 ATK (desc `ATK+`), Uses (2 darkspell counters) (desc, natif). « Attach to the villain.
# [star] Forced Interrupt : When the villain attacks, remove 1 Darkspell counter from here -> give the attached character 1 additional boost card
# for this activation. »
# Carte de reference : gs183 Induced Mutation (`AttachToFaceWhenPutIntoPlay(Villain)` + `GiveAdditionalBoostCardForThisActivation` + retrait de
# compteur ; `WhenUnitWouldAttack` comme 02020 Hysteria). Le dernier compteur retire fait quitter la carte (mot-cle Uses : fiche mots-cles/uses.md).
# ⚠ « the villain » = l'hote ; la capacite ne vaut que pour une ATTAQUE (pas un complot).


def GetAbilities() -> Sequence['Ability']:
    def sur_lhote(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return message.attacker is effect.this.GetBindFace()

    def boost_en_plus(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this
        Faces.RemoveCountersOn([this], 1, COMPTEUR_SORT, effect)
        message.GiveAdditionalBoostCardForThisActivation(1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, Villain, boost_en_plus, conditions=[sur_lhote]),
    ]
