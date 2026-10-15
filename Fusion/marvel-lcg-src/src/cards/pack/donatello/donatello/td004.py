from . import *

# Chūdan-Ura-Uke — EVENEMENT, cout 1, [mental]. ATTACK. DEFENSE. x2.
# Hero Interrupt (attack/defense): When you would take damage from an attack,
#   prevent 3 of that damage and deal 3 damage to the attacking enemy.
#
# CARTES DE REFERENCE
#  - `br004` Hammer Twirl : meme fenetre (`WhenUnitWouldTakeDamage`,
#    `is_from_attack=True`), et « deal damage to your attacker » = lire
#    `message.attacker` puis `this.DealDamage([attaquant], n, effect)`.
#  - `si012` / `td003` : `PreventDamage(n)` + `SetLabel(...)` a deux libelles
#    (`HeroInterrupt` accepte attack/defense/thwart, ability.py:195).
#
# TEXTE CONTRE CODE
#  « prevent 3 OF THAT damage » -> au plus 3. « and deal 3 damage to THE
#  ATTACKING ENEMY » -> l'attaquant lu sur le message, vivant (`IsInPlay`).
#  Libelles (attack/defense) : `SetLabel('attack', 'defense')`.
#  Deux exemplaires identiques (scans 4 et 5) : un seul card_id.


def GetAbilities() -> Sequence['Ability']:

    def chudan_ura_uke(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        message.PreventDamage(3, effect)
        attaquant = getattr(message, "attacker", None)
        if attaquant is not None and attaquant.IsInPlay():
            this.DealDamage([attaquant], 3, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            chudan_ura_uke,
            is_from_attack=True,
        ).SetPlay().SetLabel('attack', 'defense'),
    ]
