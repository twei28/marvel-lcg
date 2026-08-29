from . import *

# * Longshot
# X-MEN.
# Longshot enters play with 2 knife counters on him.
# Interrupt: When Longshot attacks an enemy, remove 1 knife counter from him ->
#   choose one: deal 2 damage to an enemy or stun a minion.
#
# Modele Hawkeye (01066) : les compteurs d'entree se posent par
# `ThisEnterPlayWithCounters`, ils ne passent PAS par une cle `desc`, et le
# retrait d'un compteur est un COUT (`CostFunc.Counter`).
#
# Le compteur `knife` a ete ajoute a COUNTER_LIST (card_face.py) : sans lui,
# `IsCounter` refuse le nom et la carte tombe des la creation de la partie.


def GetAbilities() -> Sequence['Ability']:

    def longshot(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def degats(targets: Sequence['CardFace']) -> None:
            this.DealDamage(targets, 2, effect)

        def etourdir(targets: Sequence['CardFace']) -> None:
            Faces.GiveStatus(targets, "Stunned", effect)

        # « choose one » : les deux options ne visent pas la meme chose, un
        # ennemi quelconque d'un cote, un SBIRE de l'autre.
        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility("Deal 2 damage", degats)
            .SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility("Stun a minion", etourdir)
            .SetTarget(Minion, canbe_stunned=True),
        )

    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, 'knife'),
        # `WhenUnitMakeAttack` prend TROIS arguments (type, attaquant,
        # operation) ; le quatrieme, celui de `WhenUnitMakeThwart`, n'existe
        # pas ici.
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.Interrupt,
            "This",
            longshot,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'knife')),
    ]
