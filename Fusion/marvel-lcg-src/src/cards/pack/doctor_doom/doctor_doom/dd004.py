from . import *

# "This World Is Mine!" — evenement signature, x3. ATTACK. SPELL. Cout 3.
# Hero Action (attack): Deal 8 damage to an enemy. If you paid for this card
#   using only [mental] resources, this attack gains overkill and piercing.
#
# Cartes de reference :
#  - 01053 Relentless Assault : « Deal 5 damage to a minion. If you paid for
#    this card using a [physical] resource, this attack gains overkill » —
#    meme forme exacte, `WhenInYourPlayTurn(HeroAction, op).SetPlay()
#    .SetLabel('attack').SetTarget(Enemy)` ;
#  - 20003 Grasping Tendrils pour `OnlyHasColor` ;
#  - 19005 Knife Leap pour `GainOverKill` / `GainPiercing`.
#
# ⚠ « using ONLY [mental] resources » -> `OnlyHasColor("B")`, PAS `HasColor`.
# La distinction est imprimee dans le pack lui-meme : dd001a dit « using a
# [mental] resource » (au moins une), dd004/dd005/dd006 disent « only ».
#
# ⚠ overkill et piercing vivent dans `AttackProperty` (can_attack.py:8 et 10),
# PAS dans `DamageProperty`, qui ne connait que `ignore_tough`,
# `is_from_overkill` et `is_indirect_damage`. Se tromper de classe leve un
# TypeError silencieux a la construction. Et c'est le HEROS qui porte
# l'attaque, pas l'evenement.

def GetAbilities() -> Sequence['Ability']:

    def this_world_is_mine(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero() if initiator else None
        if hero is None:
            return

        seulement_mental = effect.GetPaidResources().OnlyHasColor("B")
        # ⚠ C'est le HEROS qui inflige, pas l'evenement : overkill et piercing
        # sont des proprietes de l'ATTAQUE, et une attaque a un attaquant.
        # Exactement le montage de 01053 Relentless Assault.
        hero.DealDamage(
            effect.targets, 8, effect,
            property=AttackProperty(
                overkill=seulement_mental,
                piercing=seulement_mental,
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            this_world_is_mine,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
