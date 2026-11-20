from . import *
# * Home on Chandilar, soutien. Cout 2, [physical]. LOCATION. SHI'AR.
#
# Alter-Ego Action: Exhaust Home on Chandilar → draw 2 cards.
#
# Carte de reference : 01045 The Golden City (texte identique : `AlterEgoAction` + `Exhaust("This")` + `DrawUp(2)`).
def GetAbilities() -> Sequence['Ability']:
    def home_on_chandilar(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        effect.GetInitiator().DrawUp(2, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            home_on_chandilar,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
