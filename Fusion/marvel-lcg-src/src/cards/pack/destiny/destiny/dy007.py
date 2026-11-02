from . import *

# Be Careful : AMELIORATION (SKILL. PSIONIC.), cout 0, [energy]. Classe Hero.
# Hero Interrupt: When you would take any amount of damage, spend 1 [mental] resource and exhaust Be Careful -> prevent X of that damage, where X is the number of icons ([star] and [boost]) on the card tucked under
# Glimpse of the Future.
#
# CARTES DE REFERENCE
#  - `mw004` Clairvoyance (Madame Web) : `WhenUnitWouldTakeDamage(HeroInterrupt, "You", op).SetCostFunc(CostFunc.Exhaust("This"))` + `message.PreventDamage(n, effect)`.
#  - `dy005` : lecture de X par `IconesSousGlimpse`.
#
# TEXTE CONTRE CODE
#  « When YOU would take any amount of damage » : degats subis par l'identite du joueur (toute source). « spend 1 [MENTAL] resource » : `Cost("B")`. « prevent X OF THAT damage » : au plus X ; la capacite n'est offerte
#    que si X >= 1 (sinon elle ne previendrait rien).
#  Chiffres : cout 0, 1 ressource, X.


def GetAbilities() -> Sequence['Ability']:

    def x_positif(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        joueur = effect.GetInitiator()
        return joueur is not None and IconesSousGlimpse(joueur) > 0

    def be_careful(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        joueur = effect.GetInitiator()
        message.PreventDamage(IconesSousGlimpse(joueur), effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            be_careful,
            conditions=[x_positif],
        ).SetCost(Cost("B"))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
