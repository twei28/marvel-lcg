from . import *
def GetAbilities() -> Sequence['Ability']:
    def give_himself_tough(effect: 'Effect', message: 'Message.WhenInYourPlayTurn') -> None:
        this = effect.this.CastTo(Ally)
        this.DealDamage([this], 1, effect)
        Faces.GiveStatus([this], "Tough", effect)
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
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, give_himself_tough)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
