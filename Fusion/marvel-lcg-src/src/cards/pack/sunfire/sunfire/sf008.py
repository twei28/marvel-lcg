from . import *

# Sunfire's Suit — AMELIORATION, cout 2, [physical]. ARMOR.
# Sunfire gets +1 DEF.
# Hero Response: After Sunfire defends against an attack, exhaust Sunfire's
#   Suit and spend 1 resource of any type -> ready Sunfire.
#
# ⚠ PAS UNIQUE : aucune etoile devant le nom, verifie par DECOUPE D'IMAGE du
# bandeau vertical a cote de `sf006` et `sf007`, qui en ont une. Le zip n'en
# livre pourtant qu'UN exemplaire sur les 15 — c'est la decklist de l'auteur,
# pas une regle d'unicite.
#
# CARTES DE REFERENCE
#  - `04166` / `tg009` : `GiveKeywordToInPlayWhenApplyThis(Hero, defense=1)`.
#  - `AbilityFactory.AfterUnitDefendEnd` : « after X defends against an
#    attack ».
#  - `sf001a` : la defense de base qui pose une brulure — les deux capacites
#    se combinent, et c'est le coeur du kit defensif.
#
# TEXTE CONTRE CODE
#  ⚠ « SUNFIRE gets +1 DEF » -> la face HEROS, donc `Hero` et non `"You"` :
#    c'est l'inverse de `sf007`, qui dit « YOU ». Les deux ecritures cohabitent
#    dans le meme pack, et la difference est imprimee. Contre-cas obligatoire
#    en forme civile (RECETTES §3, defaut `an002`).
#  ⚠ DEUX COUTS derriere le declencheur : incliner l'armure ET depenser 1
#    ressource de n'importe quel type. Le litteral est `Cost("1")` : les
#    lettres R/B/Y/G imposent une COULEUR, les chiffres ne demandent qu'un
#    NOMBRE (element/cost.py:35-41). ⚠ `Cost("*")` n'existe pas, ce serait
#    une API inventee — verifie dans l'enum avant d'ecrire.
#  ⚠ « After Sunfire DEFENDS AGAINST AN ATTACK » -> la defense de base ET la
#    defense d'un evenement : le texte ne restreint pas. La combinaison avec
#    `sf001a` (brulure a la defense de BASE) n'est donc pas la meme fenetre.
#  « ready SUNFIRE » -> par le TYPE, jamais par le nom (`35014` est un allie).


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        heros = HerosDuJoueur(effect)
        if heros is not None:
            Faces.ReadyAll([heros], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            defense=1,
        ),
        AbilityFactory.AfterUnitDefendEnd(
            AbilityType.HeroResponse,
            "YourHero",
            redresser,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCost(Cost("1")),
    ]
