from . import *

# Hacked Power Gloves : AMELIORATION (ITEM. TECH.), cout 3, [energy].
# Reduce the cost of this card by 1 if you control an upgrade with the TECH trait.
# Hero Interrupt: When Beast uses a basic power, choose: • deal 1 damage to an enemy • remove 1 threat from a scheme.
#
# CARTES DE REFERENCE
#  - `nt005` Kickflip : `ReduceCostToPlayThis(1, conditions=[..])` (reduction conditionnelle). `bs005` a la meme.
#  - `14001a` / `20010` : `WhenUnitUseBasicPower(type, "You", op, powers=["ATK", "THW", "DEF"])` ; l'Interruption part AVANT la resolution du pouvoir.
#  - `mantis/__init__.py` `RetirerUneMenace` : `ChooseAbilities(.., ForChoiceAbility(..).SetTarget(Scheme2))`. `hz006` : `this.DealDamage(cibles, n, effect)` depuis l'effet de la carte.
#
# TEXTE CONTRE CODE
#  « if you CONTROL an upgrade with the TECH trait » : `AmeliorationsTech` (la carte n'est pas encore en jeu : elle ne se compte pas elle-meme). « BASIC power » : ATQ, CTR ou DEF (pas la recuperation). « BEAST uses » :
#    l'identite (`"You"`, la forme heros est la seule a utiliser un pouvoir de base). « CHOOSE » : une seule des deux branches, chacune offerte seulement si une cible existe.
#  Chiffres : cout 3, reduction 1, 1 degat, 1 menace.


def GetAbilities() -> Sequence['Ability']:

    def controle_une_amelioration_tech(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        return joueur is not None and bool(AmeliorationsTech(joueur))

    def gants(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = effect.GetInitiator()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to an enemy",
                lambda cibles:
                    this.DealDamage(cibles, 1, effect),
            ).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility(
                "Remove 1 threat from a scheme",
                lambda cibles:
                    this.RemoveThreatFromSchemes(cibles, 1, effect),
            ).SetTarget(Scheme2),
        )

    return [
        AbilityFactory.ReduceCostToPlayThis(1, conditions=[controle_une_amelioration_tech]),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            "You",
            gants,
            powers=["ATK", "THW", "DEF"],
        ),
    ]
