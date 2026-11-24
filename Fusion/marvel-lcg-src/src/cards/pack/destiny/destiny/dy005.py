from . import *

# Clairvoyance : AMELIORATION (SKILL. PSIONIC.), cout 1, [mental]. Classe Hero.
# Hero Action: Spend any number of [mental] resources (to a maximum of 3) and exhaust Clairvoyance -> for each resource spent this way, choose a different scheme and remove X threat from it, where X is the number
# of icons ([star] and [boost]) on the card tucked under Glimpse of the Future.
#
# CARTES DE REFERENCE
#  - `26022` Machine Man / `16093` : « spend up to N » = `.SetCost(Cost("..", up_to=True))`, lu par `effect.GetPaidResources().val`.
#  - `mt` `RetirerUneMenace` / `rc002` : `RemoveThreatFromSchemes(cibles, n, effect)`.
#
# TEXTE CONTRE CODE
#  « any number (to a MAXIMUM of 3) » : 0 a 3 ressources, `Cost("BBB", up_to=True)` ([mental] : la wild compte). « for EACH resource spent, choose a DIFFERENT scheme » : autant de manigances DISTINCTES que de
#    ressources (plafonnees au nombre de manigances en jeu), `ChoisirDistincts`. « remove X threat FROM IT » : X par manigance. X est lu a la resolution (`IconesSousGlimpse`).
#  Chiffres : 3 ressources au plus, X menace par manigance.


def GetAbilities() -> Sequence['Ability']:

    def clairvoyance(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = effect.GetInitiator()
        depensees = effect.GetPaidResources().val
        x = IconesSousGlimpse(joueur)
        if depensees <= 0 or x <= 0:
            return
        schemes = Worlds.FindCardsOnField(effect, card_type=Scheme2)
        choisies = ChoisirDistincts(effect, joueur, schemes, depensees, "Clairvoyance : choose a different scheme for each resource spent")
        if choisies:
            this.RemoveThreatFromSchemes(choisies, x, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            clairvoyance,
        ).SetCost(Cost("BBB", up_to=True))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
