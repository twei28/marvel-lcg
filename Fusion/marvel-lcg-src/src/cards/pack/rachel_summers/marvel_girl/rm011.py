from . import *

# Telekinetic Axe — AMELIORATION, cout 3 (physique), Restricted. PSIONIC. WEAPON.
# Marvel Girl gets +1 ATK.
# Hero Interrupt: When Marvel Girl makes a basic attack, exhaust this card -> that attack gains overkill and stun the attacked
# enemy.
#
# CARTES DE REFERENCE : `10003` Hulk Smash (`WhenUnitMakeAttack(HeroInterrupt, "You", .., is_basic_attack=True)` +
# `message.GainOverKill`), `27187a` (`SetTarget("Attacked")` + `Faces.GiveStatus`), `01028` (+ATQ attache).
#
# MOTS-PIEGES : « that attack gains overkill » ET « stun the attacked enemy » : deux effets de la meme Interruption ; pas de
# filtre `canbe_stunned` (sinon l'Interruption disparait d'un ennemi deja etourdi et le overkill est perdu).
def GetAbilities() -> Sequence['Ability']:
    def telekinetic_axe(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.GainOverKill(effect)
        Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Marvel Girl"),
            attack=1,
        ),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            "You",
            telekinetic_axe,
            is_basic_attack=True,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("Attacked"),
    ]
