from . import *

# Spear Thrust (1/2)
# Hero Action (attack): Deal 4 damage to an enemy. You may exhaust up to
#   3 DORA MILAJE characters you control to deal a total of X damage divided
#   among enemies as you choose, where X is the number of allies exhausted
#   as part of this effect.
#
# Le texte imprime melange « characters » (premiere phrase) et « allies »
# (clause X) : lecture retenue -- uniforme sur les allies Dora Milaje, cout
# ET decompte, la plus coherente (exhaustif Okoye elle-meme ne rapporterait
# alors aucun degat, ce qui n'aurait aucun sens a payer). Exemplaire physique
# 1 de 2 (ok008, ok009).
#
# Modele exact : winter/54014.py (Firepower), meme structure --
# `CostFunc.Exhaust("YouControlCards", trait=..., card_type=Ally, range=(0,3))`
# en cout OPTIONNEL (Firepower l'a en range=(1,3), obligatoire, car c'est son
# SEUL effet ; ici il s'ajoute a un degat de base garanti, donc range
# commence a 0), puis une resolution "choisir un ennemi, degat" repetee une
# fois par carte exhaustee (`len(effect.cost_func.Get(CostFunc.Exhaust)
# .return_exhausted_cards)`), en plus du degat de base fixe.


def GetAbilities() -> Sequence['Ability']:

    def spear_thrust(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        this.DealDamage(effect.targets, 4, effect)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def degat_supplementaire(targets: Sequence['CardFace']) -> None:
            this.DealDamage(targets, 1, effect)

        nombre_exhauste = len(effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards)
        for _ in range(nombre_exhauste):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "",
                    degat_supplementaire,
                ).SetLabel('attack').SetTarget(Enemy),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            spear_thrust,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("YouControlCards", trait="DORA MILAJE", card_type=Ally, range=(0, 3)))
        .SetTarget(Enemy),
    ]
