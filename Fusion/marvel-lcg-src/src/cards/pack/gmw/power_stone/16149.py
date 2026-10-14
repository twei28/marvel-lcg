from . import *

# * Power Stone

def GetAbilities() -> Sequence['Ability']:

    def power_stone(effect: 'Effect', message: 'Message.AfterFaceDealDamage|Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)

        this.AttachTo2(message.trigger, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Villain
        ),
        *AbilityFactory.AfterUnitDealsDamageWithSingleAttack(
            AbilityType.ForcedResponse,
            CardFinder(card_type=Hero|Villain),
            "AttachedCharacter",
            power_stone,
            dealt_more_than_damage=3,
        ),
        # RR 1.8 FAQ : identite vaincue -> la pierre resout son « attach to » et s'attache au vilain.
        # Gere par l'etape 3 de l'elimination (`Player.EliminerAttachementsPermanentsEtrangers`).
    ]

