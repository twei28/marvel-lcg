from . import *

# Pit Trap

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « Attach to your identity and take 1 damage. »
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        this.DealDamage([joueur.GetIdentity()], 1, effect)

    def au_lieu_de_redresser(effect: 'Effect', message: 'Message.WhenCardWouldReady') -> None:
        # « Forced Interrupt: When attached character would ready, discard this
        # card instead. » Le piege coute un redressement, une seule fois.
        this = effect.this.CastTo(Attachment)
        message.SetBeInstead(effect)
        Faces.DiscardAll([this], effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: Attach this card to your identity. »
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        this.PutIntoPlay(joueur, effect)
        this.AttachTo2(joueur.GetIdentity(), effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity"
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        AbilityFactory.WhenCardWouldReady(
            AbilityType.ForcedInterrupt,
            "AttachedCharacter",
            au_lieu_de_redresser
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
