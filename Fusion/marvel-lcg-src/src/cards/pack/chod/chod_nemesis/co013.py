from . import *

def GetAbilities() -> Sequence['Ability']:
    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(SchemeSide2)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        main = list(joueur.hand_cards.Get())
        if not main:
            return
        choisie = main[0] if len(main) == 1 else joueur.AskChooseFace(
            main, effect, prompt="Tuck a card from your hand under Duel of Wits", forced=True)
        if choisie is not None:
            this.TuckCardUnderHere(choisie, effect)

    def meme_ressource(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        """« by cards with a printed resource that matches the printed resource on the card tucked under here »."""
        this = effect.this
        dessous = list(this.GetPlacedCardArea().Get(True))
        par = getattr(message, "by_effect", None)
        source = getattr(par, "this", None)
        if not dessous or source is None:
            return False
        return bool(Types(source) & Types(dessous[0]))

    return [
        AbilityFactory.WhenThisRevealed(None, reveler),
        AbilityFactory.PlayersCannotRemoveThreatFrom(
            "AnyPlayer",
            "This",
            conditions=[meme_ressource],
        ),
    ]
