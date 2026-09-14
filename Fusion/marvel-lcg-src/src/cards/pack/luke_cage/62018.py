from . import *
def GetAbilities() -> Sequence['Ability']:
    def defensive_formation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        for target in effect.targets:
            Faces.GiveStatus([target], "Tough", effect)
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
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, defensive_formation)
        .SetCostFunc(CostFunc.Exhaust("This")).SetCostFunc(CostFunc.Counter("This", 1, 'block'))
        .SetTarget(CardFinder(card_type=Ally, trait='DEFENDER'), range=(1, 1)),
    ]
