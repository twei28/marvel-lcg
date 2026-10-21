from . import *

# "It's a Trap!" — ATTACHEMENT. Boost 1.
# When Revealed : Attach to your current location; if you cannot, surge.
# Forced Interrupt : When a player enters or leaves this location, they find a minion not in play and reveal it. Each minion engaged with that
#   player activates. Then, discard this card.
#
# Cartes de reference : pu008 (attache au lieu actuel, surge), pu009 (`Find.FindAndReveal`), `Worlds.Enemies.EngagedMinionActivateAgainstYou`
# (game/operate/enemies.py), `Message.WhenPlayerWouldEnterLocation / LeaveLocation` (nouveaux).
# ⚠ « enters OR leaves » : deux messages, meme effet ; « THEY find a minion not in play » : le joueur qui entre / sort cherche (deck de rencontre et
# defausse), aucun : rien a reveler mais les sbires engages s'activent quand meme ; « Each minion engaged with THAT player » : y compris celui
# qui vient d'etre revele ; « Then, discard this card » : toujours.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        lieu = Ville.Lieu(effect, message.GetToPlayer())
        if lieu is None or not this.AttachTo2(lieu, effect):
            ThisCardGainSurge(effect)
            Faces.DiscardAll([this], effect)

    def piege(effect: 'Effect', message: 'Message.WhenPlayerWouldEnterLocation|Message.WhenPlayerWouldLeaveLocation') -> None:
        joueur = message.GetToPlayer()
        Find.FindAndReveal(effect, joueur, finder=CardFinder(card_type=Minion))
        Worlds.Enemies.EngagedMinionActivateAgainstYou(effect, joueur)
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        Ability(AbilityType.ForcedInterrupt, Message.WhenPlayerWouldEnterLocation, [AuLieuDeLAttachement(lambda m: m.lieu)], piege).NoGameAreaLimit(),
        Ability(AbilityType.ForcedInterrupt, Message.WhenPlayerWouldLeaveLocation, [AuLieuDeLAttachement(lambda m: m.lieu)], piege),
    ]
