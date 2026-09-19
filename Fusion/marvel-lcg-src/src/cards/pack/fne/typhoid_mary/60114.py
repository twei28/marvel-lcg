from . import *

# Telekinesis (PSIONIC, SUPERPOWER) — Attach to the villain. +2 SCH (SCH+).
# Hero Action: Spend [mental] [mental] resources -> discard this card.
# [star] Boost: If Typhoid Mary is activating, take 3 indirect damage. Exhaust
#   each character damaged this way.

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Attachment)
        if not MaryActive(effect, "Typhoid Mary"):
            return
        joueur = message.GetToPlayer()
        touches: List['CardFace'] = []

        def noter(m: 'Message.AfterUnitTookDamage') -> None:
            touches.append(m.trigger)

        joueur.GetIdentity().TakeIndirectDamage(this, 3, effect, operation=noter)
        vivants = [u for u in touches if u.IsInPlay()]
        if vivants:
            Faces.ExhaustAll(vivants, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("BB")),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
