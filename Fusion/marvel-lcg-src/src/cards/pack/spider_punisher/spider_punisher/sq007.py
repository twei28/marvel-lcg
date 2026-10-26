from . import *


def GetAbilities() -> Sequence['Ability']:
    def concrete_perch(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        joueur = effect.GetInitiator()
        candidates = ArmesOuTechPretes(joueur)
        choisies: List['CardFace'] = []
        for _ in range(min(4, len(candidates))):       # « to a maximum of 4 upgrades »
            face = joueur.MayChooseFace(candidates, effect, not_move=True)
            if face is None:
                break
            candidates.remove(face)
            choisies.append(face)
        if choisies:
            Faces.ExhaustAll(choisies, effect)
        x = len(choisies)
        if x > 0:
            vues = joueur.LookAtDeck("EncounterDeck", x, effect)
            joueur.PlaceOnTopInAnyOrder(vues, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            concrete_perch,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
