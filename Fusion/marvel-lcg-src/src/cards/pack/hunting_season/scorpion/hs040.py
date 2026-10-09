from . import *

# hs040 Coiled Up
# ATK/THW/DEF -1 appliqués par le desc (ATK+, THW+, DEF+). Le Forced Interrupt
# « Queue mise de côté » est dans DefausserLesCoiledUp (__init__).

def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        scorpion, queue = ScorpionEtQueue(effect)
        if queue is None:
            ThisCardGainSurge(effect)
            return
        DeplacerDegatsDeLaQueue(effect, scorpion, queue)
        joueur = message.GetToPlayer()
        effect.this.CastTo(Attachment).AttachTo2(joueur.GetIdentity(), effect)
    return [AbilityFactory.WhenThisRevealed(None, revelee)]
