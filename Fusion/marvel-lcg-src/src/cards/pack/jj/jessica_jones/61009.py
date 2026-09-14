from . import *
def GetAbilities() -> Sequence['Ability']:
    def camcorder(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        for target in effect.targets:
            alias = Worlds.FindCardOnField(effect, name='Alias Investigations')
            x = max(0, target.health - 2)
            if alias and alias.GetCounters('evidence') >= x:
                alias.RemoveCountersInternal(x, 'evidence', effect)
                Faces.DiscardAll([target], effect)
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
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, camcorder)
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(CardFinder(card_type=Minion, non_trait="ELITE"), range=(1, 1)),
    ]
