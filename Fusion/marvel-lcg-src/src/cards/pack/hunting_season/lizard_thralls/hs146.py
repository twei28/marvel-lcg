from . import *

# hs146 Wake Your Inner Lizard

def GetAbilities() -> Sequence['Ability']:

    def menace(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        n = Worlds.ConvertPerPlayerIconToInt("1*", effect)
        effect.this.PlaceThreatOnSchemes([effect.this], n, effect)

    def appeler(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        Find.FindAndPutIntoPlay(
            effect, Worlds.GetFirstPlayer(effect),
            finder=CardFinder(name="Lizard Thrall", card_type=Minion,
                              check_face_fn=lambda f: not f.IsInPlay()),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, menace),
        AbilityFactory.WhenVillainPhaseBegin(AbilityType.ForcedInterrupt, appeler),
    ]
