from . import *

# hs060 Reptilian Rage

LIZARD = CardFinder(card_type=Villain, check_face_fn=EstLizard)

def GetAbilities() -> Sequence['Ability']:

    def bonus_atk(effect: 'Effect', face: 'CardFace') -> int:
        return min(Honte(effect), MAX_HONTE)

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        RetirerHonte(effect, {1: 2, 2: 1, 3: 0}.get(EtapeDuVilain(effect), 0))

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            LIZARD,
            get_new_value=bonus_atk,
            attack=1,
            change_on_event=OnEvent.Counter("This", 'shame'),
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.NonKeyword, LIZARD,
            lambda effect, message: message.GainOverKill(effect),
            conditions=[lambda effect, message: Honte(effect) >= 1],
        ),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse, LIZARD,
            apres_attaque,
        ),
    ]
