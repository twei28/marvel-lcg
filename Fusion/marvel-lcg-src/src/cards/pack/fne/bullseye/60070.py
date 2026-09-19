from . import *

# Deadly Sai (WEAPON) — Attach to Bullseye. +2 ATK (cle desc ATK+).
# [star] Bullseye's attacks lose ranged and gain piercing.
#   (piercing : UnitAttackGainKeyword ; « lose ranged » : lu par la capacite
#   etoilee de Bullseye, DeadlySaiAttache.)
# Hero Response: After your hero defends against an attack from Bullseye,
#   spend 2 different resources -> discard this card.
#   (AfterUnitDefendAgainstAttack("You", attacker=Bullseye) + Cost("2",
#   different_type=True), modele 05002 Red Dagger.)

def GetAbilities() -> Sequence['Ability']:

    def defausser(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Bullseye")),
        AbilityFactory.UnitAttackGainKeyword(CardFinder(name="Bullseye"), piercing=True),
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.HeroResponse,
            "You",
            defausser,
            attacker=CardFinder(name="Bullseye"),
        ).SetCost(Cost("2", different_type=True)),
    ]
