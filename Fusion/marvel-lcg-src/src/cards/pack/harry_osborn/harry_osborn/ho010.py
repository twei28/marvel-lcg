from . import *

# Powered Gauntlets — amelioration signature. TECH. Cout 2. x2
# Hero Action (attack): Exhaust Powered Gauntlets -> deal 1 damage to an
#   enemy. If you have the AERIAL trait, you may spend a resource of any
#   type to confuse that enemy.
#
# Cartes de reference :
#  - squelette : 01038 Powered Gauntlets OFFICIEL (signature Iron Man), meme
#    nom, meme premiere moitie (« Exhaust -> deal 1 damage to an enemy » +
#    test `hero.HasTrait("AERIAL")`) — mais l'officiel fait +1 degat quand
#    la version fan-made propose une confusion payante, textes distincts ;
#  - « you may spend a resource of any type » : 50134 Innocent Bystanders,
#    `ForChoiceAbilityWithCost(Cost("1"), ...)` dans un `ChooseAbilities`
#    avec `Otherwise` pour refuser.
#
# ⚠ « confuse THAT enemy » : la confusion vise l'ennemi DEJA blesse par les
# gants, pas un autre (piege « that <nom> », etape 5). Et le « you may » rend
# la depense strictement optionnelle, meme en AERIAL.

def GetAbilities() -> Sequence['Ability']:

    def powered_gauntlets(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        cibles = [t for t in effect.targets if t is not None]
        this.DealDamage(cibles, 1, effect)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()
        if hero is None or not hero.HasTrait("AERIAL"):
            return

        vivantes = [t for t in cibles if t.IsInPlay()]
        if not vivantes:
            return

        def confuse(targets: Sequence['CardFace'], res: 'Resources') -> None:
            Unused(targets, res)
            Faces.GiveStatus(vivantes, "Confused", effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("1"),
                "Spend a resource to confuse that enemy",
                confuse,
            ),
            AbilityFactory.Otherwise(lambda targets: None),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            powered_gauntlets
        ).SetLabel('attack')
        .SetTarget(Enemy)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
