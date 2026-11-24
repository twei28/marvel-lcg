from . import *

# Busted! — OBLIGATION. CONDITION. Boost 2.
# You cannot attack the villain or trigger abilities on LEAD cards.
# Alter-Ego Action : Exhaust your identity and discard a card from your hand → discard this card.
#
# Cartes de reference : sm/personal_nightmare/27153.py (`PlayersCannotTriggerAbility`, `PlayerActionToDiscardThis` + coût), valk/25028.py et
# `AbilityFactory.UnitCannotAttackTarget` (`Message.CheckIfUnitCanBeAttackBy` + `SetCannotBeAttack`), pu121 (deux `SetCostFunc` enchaines).
# ⚠ Le « you » d'une obligation est le joueur dont elle occupe l'aire (`Joueur`) : `GetControlByOrOwner` y rend le VILAIN. « cannot attack the
# villain » : toute attaque d'un de MES personnages (identite ou allie) contre un vilain ; « trigger abilities on LEAD cards » : les Responses /
# Interruptions / Actions de MES pistes (les capacites forcees ne sont pas des declenchements du joueur).

def GetAbilities() -> Sequence['Ability']:

    def vise_le_vilain(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        joueur = Joueur(effect)
        return joueur is not None and Villain.IsType(message.being_attack) and ControlePar(message.attacker, joueur)

    def une_piste_a_moi(effect: 'Effect', message: 'Message.CheckEffectCondition') -> bool:
        joueur = Joueur(effect)
        verifie = message.check_effect
        return (joueur is not None and verifie.initiator is joueur and not verifie.ability.flags.is_forced
                and verifie.this.HasTrait("LEAD"))

    return [
        Ability(AbilityType.NonKeyword, Message.CheckIfUnitCanBeAttackBy, [vise_le_vilain], lambda effect, message: message.SetCannotBeAttack(effect)),
        Ability(AbilityType.NonKeyword, Message.CheckEffectCondition, [une_piste_a_moi], lambda effect, message: message.SetEffectInvalid(effect)),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.AlterEgoAction)
        .SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCostFunc(CostFunc.Discard("YourHandCards")),
    ]
