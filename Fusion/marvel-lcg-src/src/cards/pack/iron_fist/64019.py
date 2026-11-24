from . import *

# No Time to Bleed — AMELIORATION 2★ [mental], aspect Protection (Iron Fist 19/..). CONDITION.
# [star] Discount 1 (Martial Artist or Soldier).
# Temporary. Max 1 per player.
# Response: After you play a card (including this one), heal 1 damage from your identity.
#
# MOTS-CLES (fiches lues AVANT le code) : discount.md (`DiscountAbility`, desc.Cost garde l'etoile), temporary.md
# (`desc.Temporary`, aucun code). « Max 1 per player » = `desc.MaxPerUnit` (comme 60027).
#
# CARTES DE REFERENCE
#  - `60027` Move in Shadow : MEME ENVELOPPE imprimee (Discount 1, Temporary, Max 1 per player, « Response: After you
#    play a card (including this one) ») = `DiscountAbility` + `CanPlayThisUpgradeCard()` + `AfterPlayerPlayedCard(
#    Response, "You", None, ...)` (filtre None = toute carte jouee, y compris celle-ci).
#  - `43011` Pain Tolerance : « heal 1 damage from your identity » = `this.HealthUnits(effect.targets, 1, effect)` avec
#    `.SetTarget("YourIdentity", canbe_heal=True)`.
#
# TEXTE CONTRE CODE
#  ⚠ « After you play A card (including this one) » : toute carte jouee, la sienne comprise (cas dedie).
#  ⚠ « your IDENTITY » : l'identite, quelle que soit sa forme (pas « your hero »).
#  ⚠ « heal 1 » : un seul point, pas « jusqu'a 1 » ni « 1 par carte »; la Response est facultative (pas Forced).


def GetAbilities() -> Sequence['Ability']:

    def no_time_to_bleed(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.HealthUnits(effect.targets, 1, effect)

    return [
        DiscountAbility(1, ['MARTIAL ARTIST', 'SOLDIER']),
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            'You',
            None,
            no_time_to_bleed,
        ).SetTarget("YourIdentity", canbe_heal=True),
    ]
