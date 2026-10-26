from . import *


def GetAbilities() -> Sequence['Ability']:
    def point_blank(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        cible = list(effect.targets)
        this.DealDamage(cible, 3, effect)
        armes = [f for f in AmeliorationsDe(joueur) if f.HasTrait("WEAPON") and f.IsReady()]
        for _ in range(2):                 # « up to 2 WEAPON upgrades »
            if not armes or not cible or cible[0].IsDefeated() or not cible[0].IsInPlay():
                break
            face = joueur.MayChooseFace(armes, effect, not_move=True)
            if face is None:
                break
            armes.remove(face)
            if Faces.ExhaustAll([face], effect):
                this.DealDamage(cible, 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            point_blank,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
