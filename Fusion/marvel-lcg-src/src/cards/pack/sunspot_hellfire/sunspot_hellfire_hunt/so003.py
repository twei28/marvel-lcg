from . import *

# Blazing Strike — EVENEMENT, cout 2, RES [physical], x2. ATTACK.
# Hero Action (attack): Remove 1 solar counter from Sunspot -> deal 6 damage to an enemy. If Sunspot has the AERIAL
#   trait, stun that enemy.
#
# CARTES DE REFERENCE
#  - `01021` Gamma Slam : `WhenInYourPlayTurn(HeroAction, ..).SetPlay().SetLabel('attack').SetTarget(Enemy)` + `this.DealDamage`.
#  - `sw001a` / `sw007` : le retrait d'un compteur de l'identite est un COUT (`CostFunc.Counter("YourIdentity", n, COMPTEUR)`) :
#    stock vide, la carte n'est pas jouable.
#  - `05031` Concussive Blow : `Faces.GiveStatus(effect.targets, .., effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « If Sunspot has the AERIAL trait, STUN that enemy » : apres les degats, sur la MEME cible ; le trait vient de so011.


def GetAbilities() -> Sequence['Ability']:

    def blazing_strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        this.DealDamage(effect.targets, 6, effect)
        if EstAerien(joueur):
            Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            blazing_strike,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Counter("YourIdentity", 1, COMPTEUR))
        .SetTarget(Enemy),
    ]
