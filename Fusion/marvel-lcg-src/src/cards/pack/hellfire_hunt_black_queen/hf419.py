from . import *

# Dark Temptation. Traitrise. « When Revealed : Selene attacks you. [star] Boost : If this attack defeats an ally, place 2 threat on the main
# scheme. » Cartes de reference : hf120 (`villain.DoAttackYou`), 32069 Sabretooth Strikes (`would_atk_message.IfThisAttackDefeats(Ally, ...)`).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        selene = Selene(effect)
        if selene is not None:
            selene.DoAttackYou(message.GetToPlayer(), effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        def allie_vaincu(allie: 'CardFace') -> None:
            MenaceSurLeComplotPrincipal(effect, 2)

        message.would_atk_message.IfThisAttackDefeats(Ally, allie_vaincu, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True),
    ]
