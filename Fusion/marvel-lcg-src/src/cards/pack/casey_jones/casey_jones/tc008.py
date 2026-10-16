from . import *

# * Casey's Mask — AMELIORATION, cout 3, [mental]. ARMOR. UNIQUE.
# Hero Action: Exhaust Casey's Mask → ready Casey Jones.
#
# CARTES DE REFERENCE
#  - `ho010` : amelioration a Hero Action = `CanPlayThisUpgradeCard()` +
#    `WhenInYourPlayTurn(HeroAction, op).SetCostFunc(Exhaust("This"))`.
#  - `Faces.ReadyAll([identite], effect)` : recette §2 (an001a, 31009).
#  - `raphael/tr008` Shell Cycle : « ready your hero » = la face heros du joueur.
#
# TEXTE CONTRE CODE
#  ⚠ « ready CASEY JONES » = l'IDENTITE du joueur (jamais une recherche par nom :
#    l'allie homonyme tr002 existe). Hero Action : forme heros seulement.
#  ⚠ « Exhaust Casey's Mask » est devant la fleche : un COUT ; le Masque
#    incline ne se propose plus.
#  Aucune limite imprimee ; le Masque est UNIQUE (regle moteur, `desc` : « * »).


def GetAbilities() -> Sequence['Ability']:

    def casey_s_mask(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            casey_s_mask,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
