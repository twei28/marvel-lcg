from . import *

# Citizens in Danger! — ATTACHEMENT. Boost 1.
# When Revealed : Exhaust your identity. Attach this card to your current location; if you cannot, surge.
# Forced Interrupt : When a player leaves this location, deal them a facedown encounter card and discard this card.
#
# Cartes de reference : pu009 (`WhenThisRevealed` + `AttachTo2`), 90126 (`Faces.ExhaustAll([identite])`), nt015 (surge), `Message.WhenPlayerWouldLeaveLocation`
# (nouveau, `Ville.Placer`), `Player.DealEncounterCards` (modele : carte distribuee face cachee).
# ⚠ « Exhaust your identity » : PREMIER, meme si la carte ne peut pas s'attacher ; « your current location » : le lieu occupe par le joueur qui
# revele ; impossible (plus de ville) : surge et la carte est defaussee ; « When a player leaves THIS location » : tout joueur qui quitte CE lieu
# (pas seulement celui qui a revele), « deal THEM » : ce joueur-la.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        Faces.ExhaustAll([joueur.GetIdentity()], effect)
        lieu = Ville.Lieu(effect, joueur)
        if lieu is None or not this.AttachTo2(lieu, effect):
            ThisCardGainSurge(effect)
            Faces.DiscardAll([this], effect)

    def quitte(effect: 'Effect', message: 'Message.WhenPlayerWouldLeaveLocation') -> None:
        message.GetToPlayer().DealEncounterCards(1, effect)
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        Ability(AbilityType.ForcedInterrupt, Message.WhenPlayerWouldLeaveLocation, [AuLieuDeLAttachement(lambda m: m.lieu)], quitte),
    ]
