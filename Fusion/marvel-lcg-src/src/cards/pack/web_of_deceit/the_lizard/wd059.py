from . import *

# Reptilian Regeneration

def GetAbilities() -> Sequence['Ability']:

    def cible(effect: 'Effect') -> 'CardFace|None':
        # « Attach to the REPTILIAN enemy with the highest printed hit points
        # without another Reptilian Regeneration attached. »
        candidats = []
        for ennemi in Worlds.FindCardsOnField(effect, trait="REPTILIAN", card_type=Enemy):
            deja = ennemi.GetInventoryDeck().FindCards(name="Reptilian Regeneration")
            if not deja:
                candidats.append(ennemi)
        if not candidats:
            return None
        return sorted(candidats, key=lambda x: x.printed_health)[-1]

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        hote = cible(effect)
        if hote:
            this.PutIntoPlay(message.GetToPlayer(), effect)
            this.AttachTo2(hote, effect)
        else:
            # « If you cannot, this card gains surge. »
            ThisCardGainSurge(effect, message)

    def regeneration(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        # « Forced Interrupt: When the villain phase begins, heal 1[per_hero]
        # damage from attached enemy. »
        this = effect.this.CastTo(Attachment)
        hote = this.attached_face
        if hote:
            this.HealthUnits([hote], "1*", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        AbilityFactory.WhenVillainPhaseBegin(
            AbilityType.ForcedInterrupt,
            regeneration
        ),
    ]
