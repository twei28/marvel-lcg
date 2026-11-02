from . import *

# Unmask : AMELIORATION (SKILL. PSIONIC.), cout 1, [physical]. Classe Hero.
# Hero Action: Spend any number of [mental] resources (to a maximum of 3) and exhaust Unmask -> for each resource spent this way, choose a different enemy and deal X damage to them, where X is the number of icons
# ([star] and [boost]) on the card tucked under Glimpse of the Future.
#
# CARTES DE REFERENCE
#  - `dy005` Clairvoyance : meme montage (depense variable + cibles distinctes), ici sur les ennemis.
#  - `26022` / `16093` : `Cost(.., up_to=True)` + `GetPaidResources().val` ; `01054` Uppercut : `this.DealDamage(cibles, n, effect)` (degats d'une carte, pas une attaque).
#
# TEXTE CONTRE CODE
#  « [mental] » et non [physical] : la ressource imprimee dans le coin de la carte (poing rouge) est autre chose que la depense de la capacite (noeuds bleus). « different enemy » : vilain ET sbires, tous distincts.
#    « deal X damage » : degats directs, pas une attaque (ni Perforant ni Robuste de l'attaque).
#  Chiffres : 3 ressources au plus, X degats par ennemi.


def GetAbilities() -> Sequence['Ability']:

    def unmask(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = effect.GetInitiator()
        depensees = effect.GetPaidResources().val
        x = IconesSousGlimpse(joueur)
        if depensees <= 0 or x <= 0:
            return
        ennemis = Worlds.FindCardsOnField(effect, card_type=Enemy)
        choisis = ChoisirDistincts(effect, joueur, ennemis, depensees, "Unmask : choose a different enemy for each resource spent")
        if choisis:
            this.DealDamage(choisis, x, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            unmask,
        ).SetCost(Cost("BBB", up_to=True))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
