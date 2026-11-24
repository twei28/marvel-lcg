from . import *

# * Ghost Maker — SBIRE. HAND. NINJA. ATQ 2 / MNG 1 / PV 4, Boost ★.
# When Defeated : Change the villain's position if it has not changed this phase. If the villain's position is Atop the Tenshu, discard 1 card you control;
#   otherwise, take 2 indirect damage.
# [star] Boost : If an ally is defending against this attack, reveal this minion.
#
# Cartes de reference : core/legions_of_hydra/01182 (`WhenUnitBeDefeated(WhenDefeated, "This")`), punisher_mcdc_2026/punishers_armory/pu118 (`TakeIndirectDamage`),
# sm/whispers_of_paranoia/27170 (boost : `message.would_atk_message.GetDefender()`), pack `RevealThisCard`.
# ⚠ Mots-pieges : « you » du When Defeated = le joueur qui a VAINCU Ghost Maker (a defaut, celui avec qui il etait engage) ; « discard 1 card you control » = une carte EN JEU
#  (allie, amelioration, soutien : pas la main, pas l'identite), au choix du joueur, obligatoire s'il en a ; « indirect damage » : sur l'identite ; boost : l'ALLIE
#  qui defend CETTE attaque (une defense d'un heros ne compte pas), « reveal this minion » = la carte de boost est revelee (ses When Revealed partent).


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        joueur = getattr(message, 'defeating_player', None) or this.GetEngagedPlayer()
        if joueur is None:
            return
        ChangerSiPasChange(effect)
        if AuTenshu(effect):
            candidates = CartesControlees(joueur)
            if candidates:
                choisies = joueur.AskChooseFaces(candidates, (1, 1), effect, not_move=True)
                Faces.DiscardAll(list(choisies), effect)
        else:
            joueur.GetIdentity().TakeIndirectDamage(this, 2, effect)

    def un_allie_defend(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> bool:
        Unused(effect)
        attaque = getattr(message, 'would_atk_message', None)
        defenseur = attaque.GetDefender() if attaque is not None else None
        return defenseur is not None and Ally.IsType(defenseur)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard, during_attack=True, conditions=[un_allie_defend]),
    ]
