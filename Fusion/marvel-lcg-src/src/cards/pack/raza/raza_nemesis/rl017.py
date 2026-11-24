from . import *
def GetAbilities() -> Sequence['Ability']:
    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        allies = [f for f in joueur.allies.Get() if f.IsInPlay()]
        if allies:
            # RR First Player (arbitrage du 26/10/2026) : plusieurs allies admissibles pour une carte de rencontre : le PREMIER joueur
            # choisit (en solo, c'est le joueur lui-meme).
            premier = effect.this.card.world.GetFirstPlayer() or joueur
            choisi = allies[0] if len(allies) == 1 else premier.AskChooseFace(
                allies, effect, prompt="Discard an ally you control", forced=True)
            if choisi is not None:
                Faces.DiscardAll([choisi], effect)
                return
        sbire = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if sbire is not None:
            sbire.PutIntoPlay(joueur, effect)
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        attaque = getattr(message, "would_atk_message", None)
        if attaque is not None:
            attaque.GainOverKill(effect)
    return [
        AbilityFactory.WhenThisRevealed(None, reveler),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
