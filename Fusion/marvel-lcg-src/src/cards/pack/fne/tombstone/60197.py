from . import *

# * Beetle (AERIAL, CRIMINAL) — Villainous : base desc.
# When Revealed: Search the encounter deck and discard pile for an attachment
#   that can attach to a minion and attach it to Beetle.
# « can attach to a minion » : PeutSAccrocherAUnSbire (tombstone/__init__.py),
# qui relit la phrase imprimee « Attach to ... » : la regle moteur
# `Asset2.CanAttachTo` ne connait que MaxPerUnit et acceptait Gatling Gun
# (« Attach to the villain ») sur Beetle. La fouille passe par
# Search.SearchForCard sur cette liste filtree (faces=...).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        candidates = [f for f in Worlds.GetEncounterDeckCards(effect.world) + Worlds.GetEncounterDiscardPileCards(effect.world)
                      if PeutSAccrocherAUnSbire(f, this)]
        if not candidates:
            return
        face = Search.SearchForCard(effect, joueur, faces=candidates, card_type=Attachment)
        if face:
            face.CastTo(Attachment).AttachTo2(this, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
