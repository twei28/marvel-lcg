from . import *

# * Repulsor Core One — amelioration signature, x1 (n/15 = 12).
# TECH. Cout 2, ressource [energy].
# Hero Action: Exhaust Repulsor Core One -> place 1 reactor counter on Iron Man.
# Hero Action: Remove 1 reactor counter from Iron Man and exhaust Repulsor
#   Core One -> ready Iron Man.
#
# Cartes de reference :
#  - `ho011` * Goblin Glider / `ls008` Sif's Steed pour
#    `WhenInYourPlayTurn(HeroAction)` + `CostFunc.Exhaust("This")` +
#    `Faces.ReadyAll` ;
#  - `im001a` du meme pack pour `Faces.PlaceCountersOn` ;
#  - `ho009` pour le cout arbitraire `CostFunc.Custom(None, fn)`.
#
# ⚠ LA CARTE PIVOT DU PACK : elle CONVERTIT dans les deux sens. La premiere
# action transforme une activation en compteur, la seconde un compteur en
# activation. C'est la seule source de compteur qui ne coute pas de carte, et
# la seule facon de redresser le heros sans im004.
#
# ⚠ LES DEUX ACTIONS PARTAGENT LE MEME COUT D'INCLINAISON : une seule des
# deux part par round. Le joueur choisit s'il stocke ou s'il depense.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - Le cout de la seconde action a **DEUX parties** : retirer un compteur ET
#    incliner la carte. Oublier l'une des deux est le piege `wd005`. Le
#    retrait passe par `CostFunc.Custom`, dont le False bloque le paiement :
#    sans compteur, l'action n'est pas proposee.
#  - « place 1 reactor counter on **Iron Man** » : l'identite, pas
#    l'amelioration. Les compteurs vivent sur la face d'identite, c'est ce que
#    lisent les neuf autres cartes.
#  - « ready **Iron Man** » : la face heros. Les deux capacites sont `Hero
#    Action`, donc la question de la forme ne se pose pas.


def GetAbilities() -> Sequence['Ability']:

    def stocker(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.PlaceCountersOn([identite], 1, 'reactor', effect)

    def cout_du_reacteur(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        joueur = effect.GetInitiator()
        if joueur is None:
            return False
        identite = joueur.GetIdentity()
        if identite is None:
            return False
        return RetirerUnReacteur(identite, effect)

    def redresser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            stocker,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            redresser,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, cout_du_reacteur)),
    ]
