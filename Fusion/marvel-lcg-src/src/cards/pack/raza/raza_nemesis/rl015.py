from . import *
import re
def GetAbilities() -> Sequence['Ability']:
    def peut_s_attacher_a_un_sbire(face: 'CardFace') -> bool:
        """« an attachment that can be attached to Shi'Ar Host » : « Attach to a minion », « ... the minion with ... », « a character »."""
        texte = (getattr(face.paper, "text", "") or "")
        return bool(re.match(r"\s*Attach to (a|an|the|any)\b[^.\n]*\b(minion|character|enemy)", texte, re.I))
    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        candidats = [f for f in Worlds.GetEncounterDiscardPileCards(effect)
                     if Attachment.IsType(f) and peut_s_attacher_a_un_sbire(f)]
        if not candidats:
            ThisCardGainSurge(effect, message)
            return
        choisie = candidats[0] if len(candidats) == 1 or joueur is None else joueur.AskChooseFace(
            candidats, effect, prompt="Attach to Shi'Ar Host", forced=True)
        if choisie is None:
            ThisCardGainSurge(effect, message)
            return
        choisie.CastTo(Attachment).AttachTo2(this, effect)
    return [
        AbilityFactory.WhenThisRevealed(None, reveler),
    ]
