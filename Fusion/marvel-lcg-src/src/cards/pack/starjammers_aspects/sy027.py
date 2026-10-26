from . import *
# Freedom Fighters (Justice, evenement 1 [physical]). THWART. Alliance.
# Response (thwart): When the villain activates against a player, exhaust a STARJAMMER character and an X-MEN character → cancel that
# activation. Remove X threat from a scheme, where X is the combined THW of the two exhausted characters.
#
# Cartes de reference : 27006 Web Binding (`WhenEnemyWouldActivate(.., op).SetPlay().SetLabel()` + `message.SetBeInstead(effect)` = « cancel
# that activation ») ; 48032 Gunboat Diplomacy (`desc.Alliance`, `CostFunc.Exhaust(Select.Alliance([T1, T2]))`, X relu sur
# `effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards`) ; gam/18020 (`SetTarget(Scheme2)`).
# ⚠ TEXTE CONTRADICTOIRE (question en attente, QUESTIONS.md) : « Response » + « When the villain activates » : une Reponse part APRES, or
# « cancel that activation » exige une INTERRUPTION. Code en Interruption (« Interrupt », ni Hero ni Alter-Ego) : l'effet imprime est
# inatteignable en Reponse. « against A PLAYER » : n'importe quel joueur (pas seulement vous).
def GetAbilities() -> Sequence['Ability']:
    def freedom_fighters(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Event)
        x = 0
        for face in effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards:
            if HasThwart.IsType(face):
                x += face.thwart
        message.SetBeInstead(effect)
        if x > 0:
            this.RemoveThreatFromSchemes(effect.targets, x, effect)
    def contre_le_vilain(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> bool:
        return Villain.IsType(message.trigger) and getattr(message, "to_player", None) is not None
    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.Interrupt,
            None,
            freedom_fighters,
            conditions=[contre_le_vilain],
        ).SetPlay().SetLabel('thwart')
        .SetCostFunc(CostFunc.Exhaust(Select.Alliance(["STARJAMMER", "X-MEN"])))
        .SetTarget(Scheme2),
    ]
