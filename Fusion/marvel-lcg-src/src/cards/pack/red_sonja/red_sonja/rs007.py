from . import *

# Red Reckoning — evenement signature, x1 (9/15). THWART. Cout 2, ressource
# [G].
# Hero Action (thwart): Remove 4 threat from a scheme. If you used your
# "She-Devil" ability to reduce the cost of this card, confuse an enemy.
#
# CARTE DE REFERENCE : symetrique de `rs006`, cote menace. « confuse an
# enemy » sans autre precision de cible : n'importe quel ennemi legal (pas
# force lie a la manigance contree) -- cible INDEPENDANTE de celle du
# contre, choisie seulement si la condition est vraie, donc pas un
# `SetTarget` declaratif sur la capacite entiere (fixe a la construction) :
# modele `ar001a` Bring the War, `joueur.ChooseAbilities(effect,
# AbilityFactory.ForChoiceAbility(...).SetTarget(...))` pour un ciblage
# interactif DECIDE PENDANT la resolution.

def GetAbilities() -> Sequence['Ability']:

    def red_reckoning(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 4, effect)
        if AUtiliseSheDevil(this):
            def confondre(cibles: Sequence['CardFace']) -> None:
                Faces.GiveStatus(cibles, "Confused", effect)

            joueur = effect.GetInitiator()
            if isinstance(joueur, Player):
                joueur.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        "Confuse an enemy", confondre,
                    ).SetTarget(Enemy, canbe_confused=True, range=(1, 1)),
                )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            red_reckoning,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
