from . import *

def GetAbilities() -> Sequence['Ability']:
    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        if joueur is None:
            return

        def degats_indirects(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            deck = Worlds.GetEncounterDeck(effect)
            faces = deck.DiscardCardsInternal(2, effect, continue_after_shuffle=False) if deck is not None else []
            icones = sum(f.printed_boost for f in faces)
            identite = joueur.GetIdentity()
            if icones > 0 and identite is not None:
                this.DealIndirectDamage(identite, icones, effect)

        def menace(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            faces = joueur.DiscardDeckTopCards(2, effect)
            icones = sum(NombreDIcones(f) for f in faces)
            if icones > 0:
                this.PlaceThreatOnSchemes("MainScheme", icones, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard the top 2 cards of the encounter deck. Take indirect damage equal to the number of boost icons discarded this way",
                degats_indirects),
            AbilityFactory.ForChoiceAbility(
                "Discard the top 2 cards of your deck. Place threat on the main scheme equal to the number of printed resources discarded this way",
                menace),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, reveler),
    ]
