from . import *

# He's Got This : EVENEMENT, cout 1, [mental]. DEFENSE. DUPLICATE. (mm010 et mm011 : deux exemplaires)
# Hero Interrupt (defense): When you take damage from an attack, discard 1 Dupe ally from play → prevent all damage from that attack. Search your deck, hand, and discard pile for a different Dupe
# ally and put it into play exhausted.
#
# CARTES DE REFERENCE : `nt007` / `05005` (`WhenUnitWouldTakeDamage(HeroInterrupt, "You", op, ..)` + `message.PreventDamage(..)` + `.SetPlay().SetLabel('defense')`), `49018` (Noble Sacrifice :
#  `CostFunc.Discard("YourAlly")`).
# TEXTE CONTRE CODE : « from an ATTACK » -> `is_from_attack=True`. « discard 1 Dupe ally FROM PLAY → » : COUT (on ne peut pas jouer la carte sans Dupe). « prevent ALL damage » : `PreventDamage("All")`.
#  « a DIFFERENT Dupe ally » : une autre carte que celle qui vient d'etre defaussee (les 4 Dupe sont 4 cartes distinctes). « exhausted » : `exhaust=True`. Recherche : RRG « Search » (deck melange).
#  Chiffres : cout 1.


def GetAbilities() -> Sequence['Ability']:

    def hes(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = JoueurDeCetteCarte(effect)
        message.PreventDamage("All", effect)
        if joueur is None:
            return
        # le Dupe defausse EN COUT (modele `47028` : `effect.cost_func.Get(CostFunc.X)` rend le cout paye)
        defausses = effect.cost_func.Get(CostFunc.Discard).return_discarded_cards
        ChercherEtMettreUnDupe(effect, joueur, different_de=defausses[0] if defausses else None, epuise=True)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            hes,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense')
        .SetCostFunc(CostFunc.Discard("YourAlly", name=NOM_DUPE)),
    ]
