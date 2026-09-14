from . import *
def GetAbilities() -> Sequence['Ability']:
    def calling_in_favors(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        player = effect.GetInitiator()
        faces = Search.SearchForCards(effect, player, include_player_deck=True, card_type=Ally)
        def action(targets: Sequence['CardFace']):
            player.PlayCardsLikeInTurn(list(targets), effect, update_resources_cost=-2)
            player.player_deck.Shuffle(effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Choose an ally to play, reducing its cost by 2', action).SetTarget(faces, range=(0, 1)))
    return [
        # ⚠ PAS DE `.SetPlay()` ICI, ET C'EST LE POINT DE LA CARTE.
        # `SetPlay()` baptise la capacite « Play » : le moteur la presente alors
        # comme la MISE EN JEU de la carte, evaluee pendant qu'elle est encore
        # EN MAIN. Or son cout est « incliner cette carte », impossible depuis
        # la main : le moteur repondait « rien a depenser pour payer le cout »
        # et la carte etait INJOUABLE, pour toujours.
        # Signale en partie le 14/09/2026 sur `62008` Burstein Process ; quatre
        # autres cartes avaient la meme faute. Une gate l'interdit desormais
        # (game/ability/ability.py, `_refuser_play_avec_cout_sur_soi`).
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, calling_in_favors)
        .SetCostFunc(CostFunc.Counter(CardFinder(name='Alias Investigations'), 2, 'evidence'))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
