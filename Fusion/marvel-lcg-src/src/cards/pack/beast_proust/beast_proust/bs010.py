from . import *

# Beastly Charge : EVENEMENT (ATTACK), cout 3, [physical]. x2.
# Hero Action (attack): Deal 6 damage to an enemy. You may exhaust Beast's Lab and discard 1 card tucked under it. If you do, this attack gains overkill and deals X additional damage,
# where X is the printed cost of the discarded card.
#
# CARTES DE REFERENCE
#  - `01053` Relentless Assault : `hero.DealDamage(effect.targets, n, effect, property=AttackProperty(overkill=..))` + `.SetPlay().SetLabel('attack')`. Fiche `overkill.md`.
#  - `ra011` / `night_thrasher/nt014` : `joueur.MayChooseOneAbility(effect, ForChoiceAbility(..).SetCostFunc(..))` pour un « you may » a cout.
#  - `bs001a` (meme set) : `CoutImprime` = `printed_cost.val` de la carte defaussee.
#
# TEXTE CONTRE CODE
#  « Deal 6 damage to AN enemy » : cible Enemy (villain ou sbire). « YOU MAY exhaust Beast's Lab AND discard 1 card tucked under it » : option a DEUX couts, refusable ; sans Lab pret ou sans carte glissee elle n'est
#    pas offerte. « If you do, THIS ATTACK gains overkill AND deals X additional damage » : les deux, X = cout IMPRIME de la carte defaussee ; total 6 + X d'un seul tenant, avec overkill. Refusee : 6 degats, sans overkill.
#  Chiffres : cout 3, 6 degats, X additionnels.


def GetAbilities() -> Sequence['Ability']:

    def charge(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        glissees = GlisseesSousLab(joueur)
        effect.bs_x = None
        if glissees and LabPret(joueur):
            def defausser(cibles: Sequence['CardFace']) -> None:
                Unused(cibles)
                carte = joueur.AskChooseFace(glissees, effect, prompt="Discard 1 card tucked under Beast's Lab", peek=True, not_move=True)
                if carte is not None:
                    effect.bs_x = CoutImprime(carte)
                    Faces.DiscardAll([carte], effect)

            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Exhaust Beast's Lab and discard 1 card tucked under it: overkill and extra damage",
                    defausser,
                ).SetHasNoTargetEffect()
                .SetCostFunc(CostFunc.Exhaust("YouControlCards", name=NOM_LAB)),
            )
        fait = effect.bs_x is not None
        x = effect.bs_x or 0
        joueur.GetHero().DealDamage(effect.targets, 6 + x, effect, property=AttackProperty(overkill=fait))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            charge,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
