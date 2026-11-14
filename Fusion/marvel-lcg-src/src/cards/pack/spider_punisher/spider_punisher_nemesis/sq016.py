from . import *


def GetAbilities() -> Sequence['Ability']:
    def reorganized_crime(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        candidats = list(Worlds.GetEncounterDiscardPileCards(effect, CardFinder(card_type=Minion, non_trait="ELITE")))
        if candidats:
            sbire = candidats[0] if len(candidats) == 1 else joueur.AskChooseFace(candidats, effect, prompt="Put a minion into play")
            if sbire.PutIntoPlay(joueur, effect):
                Faces.GiveStatus([sbire], "Tough", effect)
                return
        this.GainSurge(1, effect)                    # « If you cannot, this card gains surge »

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        this.Reveal(message.GetToPlayer(), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, reorganized_crime),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
