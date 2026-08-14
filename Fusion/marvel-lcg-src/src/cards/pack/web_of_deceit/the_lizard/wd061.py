from . import *

# Experimental Injection

def GetAbilities() -> Sequence['Ability']:

    def cible(effect: 'Effect') -> 'CardFace|None':
        # « Attach to a minion without the REPTILIAN trait. Otherwise, attach to
        # the minion with the least remaining hit points. »
        sbires = Worlds.FindCardsOnField(effect, card_type=Minion)
        sans_trait = [x for x in sbires if not x.HasTrait("REPTILIAN")]
        if sans_trait:
            return sans_trait[0]
        if sbires:
            return sorted(sbires, key=lambda x: x.health)[0]
        return None

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        hote = cible(effect)
        if hote:
            this.PutIntoPlay(message.GetToPlayer(), effect)
            this.AttachTo2(hote, effect)
        else:
            ThisCardGainSurge(effect, message)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        # « Attached minion gains the REPTILIAN trait and gets +4 hit points. »
        *AbilityFactory.GiveKeywordToAttached(
            trait=["REPTILIAN"],
            health=4,
        ),
    ]
