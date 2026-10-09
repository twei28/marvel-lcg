from . import *

# hs093 Forcefully Elevated
# Vous gagnez AERIAL et ne pouvez pas passer en alter-ego.
# Forced Response : apres avoir attaque Vulture, 2 degats ou une ressource physique, puis defaussez ceci.

def GetAbilities() -> Sequence['Ability']:

    def attaque_vulture(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        return any(any(t.IsCardId(i) for i in ID_VULTURE)
                   for t in message.attacked_targets)

    def payer(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this
        joueur = message.would_atk_messages[0].attacker.GetControlByPlayer()
        identite = joueur.GetIdentity()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Subir 2 degats",
                lambda cibles: this.DealDamage([identite], 2, effect)),
            AbilityFactory.ForChoiceAbilityWithCost(Cost.FromText("R"), "Depenser une ressource physique"),
        )
        Faces.DiscardAll([this], effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", trait="AERIAL"),
        AbilityFactory.PlayersCannotChangeForms(AbilityType.NonKeyword, "You", to_form=AlterEgo),
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, "YourIdentity", payer, conditions=[attaque_vulture]),
    ]
