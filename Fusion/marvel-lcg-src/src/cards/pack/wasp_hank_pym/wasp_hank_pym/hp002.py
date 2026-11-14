from . import *
# * Ant-Man (Eric O'Grady) — allie. [star] +1 THW et +1 ATK par compteur pym (max +3/+3).
# Action : incline un Size Manipulation -> deplace 1 compteur pym de lui vers ici.
# Action : defausse cette carte -> change de forme.
def GetAbilities() -> Sequence['Ability']:
    def compteurs(effect: 'Effect', ui: List['CardFace']) -> int:
        return min(3, effect.this.CastTo(Ally).GetCounters('pym'))
    def deplacer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        for source in effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards:
            if Faces.RemoveCountersOn([source], 1, 'pym', effect):
                Faces.PlaceCountersOn([this], 1, 'pym', effect)
    def quitter(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        changer_de_forme(effect)
    return [
        AbilityFactory.ThisGainKeyword(
            compteurs,
            attack=1,
            thwart=1,
            change_on_event=OnEvent.Counter("This", 'pym'),
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            deplacer,
        ).SetCostFunc(CostFunc.Exhaust(name="Size Manipulation", card_type=Upgrade)),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            quitter,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
