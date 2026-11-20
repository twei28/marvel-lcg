from . import *

# Death by a Thousand Cuts — AMELIORATION 2★ [physical], aspect Aggression (Iron Fist 30). SKILL.
# [star] Discount 1 (Martial Artist or Soldier).
# Temporary. Max 1 per player.
# Response (attack): After you play a card (including this one), deal 1 damage to an enemy.
#
# MOTS-CLES : discount.md, temporary.md (fiches lues).
#
# CARTES DE REFERENCE
#  - `60027` Move in Shadow : meme enveloppe (Discount, Temporary, Max 1 per player, « After you play a card (including
#    this one) ») ; seul l'effet change (retirer de la menace -> infliger 1 degat).
#  - `08010` Widow's Bite / `13014` Surprise Attack : un « Response (attack): ... deal N damage to <cible> » =
#    `.SetLabel('attack')` + `this.DealDamage(effect.targets, N, effect)` + `.SetTarget(Enemy)`.
#
# TEXTE CONTRE CODE
#  ⚠ « After you play a card (including this one) » : toute carte, la sienne comprise.
#  ⚠ « an enemy » : sbire OU vilain, un seul coup de 1 degat (jamais « chaque »).
#  ⚠ « Response (attack) » : etiquette d'attaque, pas une attaque du heros (aucun bonus d'ATK).


def GetAbilities() -> Sequence['Ability']:

    def death_by_a_thousand_cuts(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.DealDamage([t for t in effect.targets if t is not None], 1, effect)

    return [
        DiscountAbility(1, ['MARTIAL ARTIST', 'SOLDIER']),
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            'You',
            None,
            death_by_a_thousand_cuts,
        ).SetLabel('attack')
        .SetTarget(Enemy),
    ]
