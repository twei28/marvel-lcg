from . import *

# Reinforced Plating — Amelioration 1 [physical], classe Hero.
# [star] As an additional cost to play this upgrade, exhaust Torso (Intact).
# Hero Action: Discard Reinforced Plating → flip 1 [[COMPONENT]]
#   ([[DESTROYED]] side up) upgrade to its [[INTACT]] side. Gain a tough
#   status card.
#
# Cartes de reference :
#  - `56007` Hunted pour le cout additionnel sur la capacite de jeu.
#  - `an006` / `42030` : « discard this card → » est un COUT,
#    `CostFunc.Discard("This")`, jamais un effet.
#  - `49009` Metal Shards : `Faces.GiveStatus([identite], "Tough", effect)`.
#  - `dz017a` : `Faces.FlipAllTo(cibles, None, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Discard Reinforced Plating → » : la fleche fait de la defausse un COUT.
#    Consequence concrete : si aucun Component detruit n'est en jeu, la
#    capacite n'a pas de cible et la carte NE DOIT PAS partir. D'ou le
#    selecteur de cible, qui bloque l'action avant tout paiement.
#  - « flip **1** COMPONENT (DESTROYED side up) » : un seul, au choix, et
#    seulement une piece detruite.
#  - « Gain a tough status card » : c'est le JOUEUR (son identite) qui gagne
#    Coriace, pas le Component.
#  - Deux exemplaires dans le deck, et rien ne les limite a un par joueur.


def GetAbilities() -> Sequence['Ability']:

    def reinforced_plating(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        Faces.FlipAllTo(effect.targets, None, effect)
        Faces.GiveStatus([effect.GetInitiator().GetIdentity()], "Tough", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard()
        .SetCostFunc(CostFunc.Exhaust(SelecteurComposantIntact(nom=NOM_TORSO))),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            reinforced_plating,
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget(
            Upgrade,
            trait=TRAIT_DESTROYED,
            from_where=["YouControlCards"],
        ),
    ]
