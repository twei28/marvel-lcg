from . import *

# Risky Business — obligation. Boost 2. GiveTo: Harry Osborn.
# Give to the Harry Osborn player.
# You are stunned.
# Alter-Ego Action: Exhaust Harry Osborn -> discard this card. Return the
#   topmost TECH upgrade in your discard pile to your hand.
#
# Cartes de reference :
#  - squelette obligation : an010 Banished from Asgard,
#    `WhenThisObligationGiveToYou` ; « You are stunned » a la remise, comme
#    la puce 2 de an010 (`Faces.GiveStatus([identite], "Stunned", ...)`) ;
#  - l'action de sortie : wd005 Vibro-Shock Gauntlets,
#    `PlayerActionToDiscardThis(...)` — ici en AlterEgoAction avec
#    `CostFunc.Exhaust("YourIdentity")` ;
#  - « the topmost [[TECH]] upgrade in your discard pile » : 01034 * Stark
#    Tower, `discard_pile.FindTopmost(CardFinder2("TECH", Upgrade))` +
#    `Faces.ReturnToHand`.
#
# ⚠ HOMONYME : « Risky Business » est AUSSI le nom du SET vilain officiel de
# Norman Osborn (02001a-02003a) ET de l'obligation du pack officiel `gob`.
# Pure coincidence d'auteur, aucune carte ne resout ce nom : rien a coder,
# mais le signaler (meme piege documente dans le plan des portages).
#
# ⚠ « Return ... to your hand » est une PHRASE SEPARE apres « discard this
# card » : la remontee de la carte TECH n'est pas conditionnee a trouver
# quelque chose — s'il n'y a aucune amelioration TECH dans la defausse,
# l'action se resout quand meme (l'obligation part, rien ne remonte).

def GetAbilities() -> Sequence['Ability']:

    def remise(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)

        player = message.GetGaveToPlayer()
        if player is None:
            return
        identite = player.GetIdentity()
        if identite is not None:
            Faces.GiveStatus([identite], "Stunned", effect)

    def remonter_tech(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        initiator = effect.GetInitiator()
        if initiator is None:
            return
        face = initiator.discard_pile.FindTopmost(CardFinder2("TECH", Upgrade))
        if face:
            Faces.ReturnToHand([face], initiator, effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            remise
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
            ex_operation=remonter_tech,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
