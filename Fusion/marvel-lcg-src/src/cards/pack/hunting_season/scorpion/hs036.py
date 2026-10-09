from . import *

# hs036 * Scorpion’s Tail

def GetAbilities() -> Sequence['Ability']:

    def punir(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        for cible in list(message.damaged_targets):
            if cible.IsStunned():
                cible.TakeDamage(effect.this, 1, effect)
            else:
                Faces.GiveStatus([cible], "Stunned", effect)

    def absorber(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        if ETAT["deplacement"]:
            return
        queue = effect.this
        scorpion = message.trigger
        joueur = Worlds.GetFirstPlayer(effect)
        degats = message.will_take_damage

        def ici(cibles) -> None:
            message.PreventDamage("All", effect)
            PlacerDegatsSurLaQueue(effect, scorpion, queue, degats)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Place the damage on Scorpion’s Tail", ici),
            AbilityFactory.ForChoiceAbility("Scorpion takes the damage", lambda cibles: None),
        )

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse, "AttachedVillain", punir,
            conditions=[lambda effect, message: len(message.damaged_targets) > 0],
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt, "AttachedVillain", absorber,
        ),
    ]
