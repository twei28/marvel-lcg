from . import *
from game.card.face.attribute.can_boost import CanBoost

# * Lady Bullseye (ASSASSIN, HAND) — Villainous : base automatique.
# [star] Forced Interrupt: When resolving boost cards during Lady Bullseye's
#   attack, if that attack is undefended, give her 1 additional boost card
#   for this attack.
# « When resolving boost cards » = WhenBoostCardWouldTurnedFaceUp (envoye par
# ResolveBoostCards, defenseur connu) ; `boost_for_card="This"` borne a SES
# boosts ; une seule fois par attaque (drapeau sur le message d'attaque).

def GetAbilities() -> Sequence['Ability']:

    def sans_defense(effect: 'Effect', message: 'Message.WhenBoostCardWouldTurnedFaceUp') -> bool:
        attaque = message.would_atk_message
        if attaque is None or getattr(attaque, '_lady_bullseye_bonus', False):
            return False
        return getattr(message.being_message, 'defender', None) is None

    def bonus(effect: 'Effect', message: 'Message.WhenBoostCardWouldTurnedFaceUp') -> None:
        attaque = message.would_atk_message
        setattr(attaque, '_lady_bullseye_bonus', True)
        # Pas `GiveAdditionalBoostCardForThisActivation` : sur le message
        # d'attaque il enregistre une capacite Temp pour la PROCHAINE
        # activation (sender_damage.py:276), donc rien pour celle-ci. On pose
        # la carte face cachee tout de suite : la boucle de ResolveBoostCards
        # la retourne dans la foulee (meme primitive que sender_card.py:751).
        effect.this.CastTo(CanBoost).GiveFacedownBoostCardsInternal(1, effect, attaque)

    return [
        AbilityFactory.WhenBoostCardWouldTurnedFaceUp(
            AbilityType.ForcedInterrupt,
            bonus,
            while_attack=True,
            boost_for_card="This",
            conditions=[sans_defense],
        ),
    ]
