from . import *

# * Negasonic Teenage Warhead (sbire ELITE HELLFIRE, PV 4, ATQ 2*, MNG 1, Steady, Toughness, Boost 1 + [star]).
# « Steady. Toughness. [star] When Negasonic Teenage Warhead attacks you, you must exhaust a support or upgrade you control, if able. [star] Boost : Exhaust a
# support or upgrade you control. » Steady et Toughness : natifs (`desc`, fiches steady.md / toughness.md).
# Cartes de reference : 40105a (`WhenUnitAttackYou(ForcedInterrupt, ..., op)` + `message.GetAgainstPlayer()`), 40160 Manufactured Drama (soutiens du joueur),
# robocop rc012 (`joueur.GetControlUpgrade(...)`), hf321 (`WhenCardBecomeBoost("This", op)` + `message.GetToPlayer()`).
# ⚠ « When ... attacks you » = AVANT l'attaque (Interruption forcee, pas Reponse) ; « if able » : aucun soutien/amelioration pret -> rien ; le joueur choisit lequel.


def GetAbilities() -> Sequence['Ability']:
    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        EpuiserUnSoutienOuUneAmelioration(effect, message.GetAgainstPlayer())

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        EpuiserUnSoutienOuUneAmelioration(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, "This", attaque),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
