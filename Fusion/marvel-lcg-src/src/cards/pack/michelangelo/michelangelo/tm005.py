from . import *

# Kaiten — evenement signature, x2 (5/15 et 6/15). ATTACK. Cout 2, [physical].
# Hero Action (attack): Deal 3 damage to an enemy. You may exhaust a NUNCHUCK
#   upgrade you control to confuse or stun that enemy.
#
# Cartes de reference :
#  - attaque d'evenement : `lady_sif/ls003` Impale —
#    `WhenInYourPlayTurn(HeroAction).SetPlay().SetLabel('attack')
#    .SetTarget(Enemy)` + `this.DealDamage(effect.targets, n, effect)` ;
#  - « you MAY exhaust X to ... » : `lady_sif/ls005` (`MayChooseOneAbility`,
#    le « may » impose la branche Cancel) + cout d'epuisement d'une carte
#    controlee : `rainy/thor_jane_foster/ra004` —
#    `CostFunc.Exhaust(trait=, card_type=Upgrade, from_where=["YouControlCards"])` ;
#  - statut : `Faces.GiveStatus(cibles, "Stunned"|"Confused", effect)`.
#
# ⚠ Mots-pieges :
#  - « confuse OR stun » : deux branches EXCLUSIVES, une seule est appliquee,
#    et le cout (epuiser UN Nunchuck) est paye par la branche choisie.
#  - « that enemy » : la MEME cible que les 3 degats (`effect.targets`), meme
#    si elle est vaincue entre-temps (GiveStatus ne fait alors rien).
#  - Le Nunchuck doit etre PRET pour etre epuise : le cout filtre seul.
#  - Le libelle `(attack)` alimente Sonne.

def GetAbilities() -> Sequence['Ability']:

    def kaiten(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        this.DealDamage(effect.targets, 3, effect)

        cible = list(effect.targets)

        def donner(statut: str) -> None:
            Faces.GiveStatus(cible, statut, effect)

        initiator.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust a NUNCHUCK upgrade: stun that enemy",
                lambda cibles: donner("Stunned"),
            ).SetCostFunc(CostFunc.Exhaust(
                trait="NUNCHUCK",
                card_type=Upgrade,
                from_where=["YouControlCards"])),
            AbilityFactory.ForChoiceAbility(
                "Exhaust a NUNCHUCK upgrade: confuse that enemy",
                lambda cibles: donner("Confused"),
            ).SetCostFunc(CostFunc.Exhaust(
                trait="NUNCHUCK",
                card_type=Upgrade,
                from_where=["YouControlCards"])),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            kaiten,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
