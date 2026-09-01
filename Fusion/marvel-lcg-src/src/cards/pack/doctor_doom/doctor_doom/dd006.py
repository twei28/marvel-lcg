from . import *

# "Pain Is For Lesser Men!" — evenement signature, x2. DEFENSE. SPELL. Cout 2.
# Hero Interrupt (defense): When you would take any amount of damage from an
#   attack, prevent all of that damage. If you paid for this card using only
#   [mental] resources, stun and confuse the enemy.
#
# Cartes de reference :
#  - 01003 Backflip et 03005 Shield Block : « Interrupt (defense): When you
#    would take any amount of damage from an attack, prevent all of that
#    damage », soit `WhenUnitWouldTakeDamage(type, "You", op).SetPlay()
#    .SetLabel('defense')` + `message.PreventDamage("All", effect)` ;
#  - 05015 Tackle / 20003 Grasping Tendrils pour `Faces.GiveStatus`.
#
# ⚠ « stun AND confuse » : les DEUX statuts, pas un choix. Chacun exige que la
# cible puisse le recevoir (`canbe_stunned` / `canbe_confused`) : un ennemi
# Stalwart n'en prend aucun, et c'est le comportement attendu.
#
# ⚠ « the enemy » = l'attaquant de CETTE attaque (`message.attacker`), pas un
# ennemi au choix.

def GetAbilities() -> Sequence['Ability']:

    def pain_is_for_lesser_men(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.PreventDamage("All", effect)

        if not effect.GetPaidResources().OnlyHasColor("B"):
            return
        attaquant = getattr(message, "attacker", None)
        if attaquant is not None:
            Faces.GiveStatus([attaquant], "Stunned", effect)
            Faces.GiveStatus([attaquant], "Confused", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            pain_is_for_lesser_men,
        ).SetPlay().SetLabel('defense'),
    ]
