from . import *
def GetAbilities() -> Sequence['Ability']:
    # « After you PLAY Squirrel Girl FROM YOUR HAND » : le declencheur doit etre
    # la mise en jeu depuis la main, pas l'entree en jeu par un autre moyen
    # (Calling in Favors la met en jeu depuis le deck, sans poser de jetons).
    def place_squirrel(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        player = effect.GetInitiator()
        this.PlaceCountersInternal(len(player.hand_cards.Get()), 'squirrel', effect, maximum=4)
    def remove_threat(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect)
    return [
        AbilityFactory.AfterYouPlayThisFromHand(AbilityType.Response, place_squirrel),
        # Action d'un allie DEJA en jeu : pas de `SetPlay`, qui designerait une
        # mise en jeu depuis la main (cf. Cloak 60020 du pack Fear No Evil).
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, remove_threat)
        .SetCostFunc(CostFunc.Counter("This", 1, 'squirrel')).SetTarget(Scheme2, range=(1, 1)),
    ]
