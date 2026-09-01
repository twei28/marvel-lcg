from . import *

# Automated Life-Support — amelioration Discovery (4/5). ARMOR. Cout 2.
# Attach to an ally. Max 1 per ally.
# Forced Interrupt: When the ally would be defeated, heal 1 damage and give
#   the ally a tough status card.
#
# Cartes de reference :
#  - 01185 Biomechanical Upgrades : meme charpente exacte — amelioration
#    attachee a un personnage, `WhenUnitWouldBeDefeated(ForcedInterrupt,
#    "Attached...", op)`, `message.SetBeInstead(effect)` pour empecher la
#    defaite, puis soin. Elle vise un sbire et soigne tout ; nous visons un
#    allie et ne soignons que 1.
#  - le statut robuste : 05015 Tackle / 01083 Mockingbird,
#    `Faces.GiveStatus(cibles, "Tough", effect)` (recette moteur §2).
#
# ⚠ « Max 1 per ally » est lu NATIVEMENT dans `desc.MaxPerUnit` (base
# automatique, recette §3) : aucun module a ecrire pour cette phrase.
#
# ⚠ `SetBeInstead` est indispensable : sans lui, l'allie meurt malgre le soin,
# puisque l'interruption ne fait que s'intercaler. C'est la lecon de 01185.
#
# ⚠ « heal 1 damage » ne suffit PAS toujours a sauver l'allie : s'il encaisse
# 3 degats d'un coup avec 1 PV restant, il reste a -1 apres le soin de 1. Le
# statut Robuste, lui, absorbe l'attaque SUIVANTE. C'est le texte imprime ;
# on ne « repare » pas la carte en soignant plus.
#
# ⚠ Le porteur peut aussi ne PAS etre soignable (deja a plein). Le soin est
# alors sans effet, mais le statut Robuste et l'annulation de la defaite, eux,
# s'appliquent quand meme.

def GetAbilities() -> Sequence['Ability']:

    def automated_life_support(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)

        message.SetBeInstead(effect)

        allie = message.trigger
        if allie is None:
            return
        this.HealthUnits([allie], 1, effect)
        Faces.GiveStatus([allie], "Tough", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Ally),
        ),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "AttachedAlly",
            automated_life_support,
        ),
    ]
