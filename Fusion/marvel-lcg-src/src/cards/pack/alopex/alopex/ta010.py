from . import *

# * Alopex's Other Kama — AMELIORATION signature, x1 (15/16). KAMA. NINJA. WEAPON.
# Cout 1, [mental]. Restricted.
# Each [[KAMA]] upgrade you control gains: "Hero Action (attack/thwart): Exhaust
#   this card -> deal 1 damage to an enemy or remove 1 threat from a scheme."
#
# Cartes de reference :
#  - vrai octroi : voir `ta009` (decision utilisateur, `tl011` / `tm011`) ;
#  - « deal N damage to an enemy OR remove M threat from a scheme » :
#    `32171b` Metro P.D. Support / `cn006` Hyborian Havoc : `ChooseAbilities` a
#    deux `ForChoiceAbility` (`SetTarget(Enemy)` / `SetTarget(Scheme2,
#    has_threat=True)`) ;
#  - « (attack/thwart) » : `cn006`, `SetLabel('attack', 'thwart')`.
#
# Mots-pieges :
#  - « EACH KAMA upgrade GAINS » : chaque Kama controle porte l'Action, chacune
#    s'incline a part (deux Kama = deux Actions par tour) ;
#  - « exhaust THIS card » : la Kama qui porte l'Action donnee ;
#  - « (attack/thwart) » : l'action est une attaque ET un contre (les deux
#    labels), selon l'option choisie ;
#  - « 1 damage to an enemy OR remove 1 threat from a scheme » : UNE des deux
#    options, au choix du joueur ;
#  - Restricted : base automatique (desc).


def GetAbilities() -> Sequence['Ability']:

    def kama_attaque_ou_contre(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        this = effect.this
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def degats(cibles: Sequence['CardFace']) -> None:
            this.DealDamage(cibles, 1, effect)

        def menace(cibles: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(cibles, 1, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to an enemy", degats).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility(
                "Remove 1 threat from a scheme", menace).SetTarget(Scheme2, has_threat=True),
        )

    action_donnee = AbilityFactory.WhenInYourPlayTurn(
        AbilityType.HeroAction,
        kama_attaque_ou_contre,
    ).SetLabel('attack', 'thwart') \
     .SetCostFunc(CostFunc.Exhaust("This"))

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait=TRAIT_KAMA, card_type=Upgrade),
            control_by="You",
            given_abilities=[action_donnee],
        ),
    ]
