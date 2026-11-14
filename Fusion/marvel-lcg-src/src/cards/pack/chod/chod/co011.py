from . import *

def GetAbilities() -> Sequence['Ability']:
    def capturee(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            finder=CardFinder(name=NOM_CRREEE),
        )
        if face:
            this.TuckCardUnderHere(face, effect)
        Faces.PlaceCountersOn([this], 2, 'search', effect)

    def chercher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        this.RemoveCountersInternal(1, 'search', effect)
        if this.GetAllCounters() <= 0:
            Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(capturee),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            chercher,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
