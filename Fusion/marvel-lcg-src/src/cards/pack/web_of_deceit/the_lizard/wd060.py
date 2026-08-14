from . import *

# Super Reptile

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « Attach to The Lizard. Otherwise, Super Reptile gains surge. »
        this = effect.this.CastTo(Attachment)
        lizard = Worlds.FindCardOnField(effect, name="The Lizard", card_type=Villain)
        if lizard:
            this.PutIntoPlay(message.GetToPlayer(), effect)
            this.AttachTo2(lizard, effect)
        else:
            ThisCardGainSurge(effect, message)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: Attach this card to The Lizard. »
        this = effect.this.CastTo(Attachment)
        lizard = Worlds.FindCardOnField(effect, name="The Lizard", card_type=Villain)
        if lizard:
            this.AttachTo2(lizard, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        # « Attached villain gains the BRUTE trait. »
        *AbilityFactory.GiveKeywordToAttached(
            trait=["BRUTE"],
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
