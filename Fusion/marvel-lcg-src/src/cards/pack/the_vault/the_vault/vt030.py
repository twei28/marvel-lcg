from . import *

# Rampage in Public — TRAITRISE x4. 2 icones de boost.
# When Revealed: If the number of villains in play is less than the number of players, this card gains surge. Reveal the top
#   card of the villain deck. If you cannot, the villain with the highest activation order value activates against you.
#
# Cartes de reference :
#  - Surge conditionnel : `ThisCardGainSurge` (modele gs189) ; revelation : `RevelerProchainMechant` (helper du set) ;
#    « activates against you » : `villain.DoActivate(joueur, effect)` (modele bw021 Imperius Rex : `namor.DoActivate(joueur, effect)`).
#  - « the villain with the highest activation order value » : `Villains.ParOrdreDActivation(...)[-1]`.
#
# ⚠ Mots-pieges : le nombre de vilains se compte AVANT la revelation ; « If you cannot » = deck de vilains VIDE ; « highest »
# = plus GRAND Activation Order (l'inverse de « the villain ») ; aucun vilain en jeu et deck vide = rien ne s'active.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        joueur = message.GetToPlayer()
        if len(Villains.All(effect)) < NombreDeJoueurs(effect):
            ThisCardGainSurge(effect)
        if Villains.VillainDeckSize(effect) > 0:
            RevelerProchainMechant(effect, joueur)
            return
        mechants = Villains.ParOrdreDActivation(Villains.All(effect))
        if mechants:
            mechants[-1].DoActivate(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
