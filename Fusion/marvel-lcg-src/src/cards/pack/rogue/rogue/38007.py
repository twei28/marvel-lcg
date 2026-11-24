from . import *

# Energy Transfer
#
# ERRATA RRG 1.7 / 1.8 (Annexe V, Rogue Hero Pack #7) : « Find Touched and attach it to a character other than Rogue and deal 2 damage to that character → heal 2 damage from Rogue and ready her. »
#   (« Attach Touched ... » devient « Find Touched and attach it ... »). Le script suivait DEJA ce texte : le cout personnalise (`attach_touched`) retrouve Touched (`FindTouched`),
#   l'attache a un personnage autre que Rogue et lui inflige 2 degats, l'effet soigne et redresse Rogue. Relu le 03/11/2026 : rien a changer.

def GetAbilities() -> Sequence['Ability']:

    def energy_transfer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        this.HealthUnits(effect.targets, 2, effect)
        Faces.ReadyAll(effect.targets, effect)

        touched = FindTouched(effect)

        if touched:
            target = touched.bind_face
            if target:
                identity = initiator.GetIdentity()
                identity.GainUntilRoundEnd(
                    effect,
                    trait=target.traits
                )

    def attach_touched(faces: Sequence['CardFace'], effect: 'Effect') -> bool:
        this = effect.this.CastTo(Event)

        if not faces:
            return False

        touched = FindTouched(effect)
        if not touched:
            return False

        target = faces[0]
        if touched.AttachTo2(target, effect):
            this.DealDamage([target], 2, effect)
            return True
        return False

    # def get_touched(effect: 'Effect') -> Sequence['CardFace']:
    #     touched = GetTouched(effect)
    #     if touched:
    #         return [touched.GetBindFace()]
    #     return []

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            energy_transfer
        ).SetPlay().SetLabel()
        .SetCostFunc(CostFunc.Custom(CardFinder(card_type=Unit2, non_name="Rogue"), attach_touched))
        # .SetCostFunc(CostFunc.DealDamage(2, selector=Select.From(get_targets_fn=get_touched)))
        .SetTarget(name="Rogue"),
    ]

