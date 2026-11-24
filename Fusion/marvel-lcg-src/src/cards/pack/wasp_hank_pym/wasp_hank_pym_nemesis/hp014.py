from . import *
# Return of the Prodigal Son — complot annexe (HACKED). Forced Response : apres la fin de la phase JOUEUR, 1 compteur
# seize ici ; a 2 ou plus, retire tous les compteurs seize et glisse FACE CACHEE sous cette carte l'amelioration ou le
# soutien EN JEU au cout le plus eleve. [star] Boost : reveler cette carte.
def GetAbilities() -> Sequence['Ability']:
    def saisie(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(SchemeSide2)
        Faces.PlaceCountersOn([this], 1, 'seize', effect)
        if this.GetCounters('seize') < 2:
            return
        Faces.RemoveCountersOn([this], "All", 'seize', effect)
        candidates = [face for face in Worlds.GetOnFieldCards(effect) if Upgrade.IsType(face) or Support.IsType(face)]
        face = Filter.One(candidates, effect, highest_cost=True)
        if face:
            this.TuckCardUnderHere([face], effect)
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(SchemeSide2)
        this.Reveal(None, effect)
    return [
        AbilityFactory.AfterPhaseEnd(
            AbilityType.ForcedResponse,
            "Player",
            saisie,
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
