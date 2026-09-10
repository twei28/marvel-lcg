from . import *

# * Arachnne Costume — AMELIORATION, cout 1, RES [wild]. ITEM.
# Hero Action: Exhaust this card, remove up to 2 psionic web counters from
#   Spider-Woman and choose a basic power -> Spider-Woman gets +1 to that power
#   for each psionic web counter removed this way until the end of the round.
#
# ⚠ « ARACHNNE » EST LA COQUILLE IMPRIMEE de l'auteur (deux n), pour
# « Arachne ». Le nom de la carte la garde : c'est ce qui est imprime.
#
# CARTE DE REFERENCE
#  - `bl006` Vampiric Reflexes : `identite.GainUntilRoundEnd(effect, ...)`, qui
#    accepte `attack`, `thwart`, `defense` et `recover`.
#  - `sw006` Psi-Web Trap : la saisie du nombre, `DemanderCombienDeToiles`,
#    ici bornee a 2.
#
# TEXTE CONTRE CODE
#  ⚠ « UP TO 2 » : de 0 a 2, et jamais plus que le stock.
#  ⚠ « +1 for each counter REMOVED THIS WAY » : le bonus suit ce qui est
#    VRAIMENT parti. Un stock vide donne +0, et la carte s'incline pour rien —
#    ce que le texte autorise.
#  ⚠ « a BASIC POWER » : ATQ, CTR, DEF ou RECUPERATION. Le quatrieme est facile
#    a oublier ; il ne sert qu'en forme civile, mais il est imprime.
#  ⚠ « until the END OF THE ROUND », pas de la phase.


def GetAbilities() -> Sequence['Ability']:

    POUVOIRS = {"ATK": "attack", "THW": "thwart", "DEF": "defense", "REC": "recover"}

    def costume(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        identite = IdentiteDe(joueur)
        if joueur is None or identite is None:
            return
        combien = min(2, ToilesDe(joueur))
        if combien > 0:
            combien = joueur.AskChooseOneText(list(range(combien, -1, -1)))
        retire = RetirerDesToiles(joueur, combien, effect)
        if retire <= 0:
            return
        pouvoir = joueur.AskChooseOneText(list(POUVOIRS))
        identite.GainUntilRoundEnd(effect, **{POUVOIRS[pouvoir]: retire})

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            costume,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
