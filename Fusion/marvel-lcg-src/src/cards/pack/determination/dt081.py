from . import *

# Sword Training

def GetAbilities() -> Sequence['Ability']:

    def sword_training(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        Faces.GiveStatus([message.attacked], "Stunned", effect)

    def check_tough_retire(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> bool:
        # Le tough a saute si la cible en portait un avant l'attaque et n'en a
        # plus apres : c'est ce que le moteur laisse voir de « removes a tough ».
        cible = message.attacked
        return Enemy.IsType(cible) and not cible.CastTo(CanStatus).HasStatus("Tough")

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(trait="X-MEN", card_type=Ally)
        ),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.Response,
            "AttachedAlly",
            Enemy,
            sword_training,
            conditions=[check_tough_retire],
        ),
    ]
