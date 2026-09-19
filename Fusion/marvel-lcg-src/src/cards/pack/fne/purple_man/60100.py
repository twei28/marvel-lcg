from . import *

# Converted (CONDITION)
# Treat attached ally as an INFLUENCED minion with a blank text box. Attached
#   minion's SCH is equal to its base THW and it does not take consequential
#   damage.
# When Revealed: Attach to the highest-cost ally you control and engage it.
#   Otherwise, this card gains surge.
# Modele exact : 21178 Beguiled (TreatAttachedCardAsMinion sur le gabarit
# « Influenced Minion », qui porte le trait et un texte vide ; la fabrique
# copie ATK et pose SCH = THW imprime, sans degats consecutifs).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        allies = [a for a in Worlds.GetOnFieldAllies(effect) if a.GetControlByPlayer() is joueur]
        allie = Filter.One(allies, effect, highest_cost=True)
        if allie:
            this.AttachTo2(allie, effect)
        else:
            ThisCardGainSurge(effect)

    def engager(minion: 'Minion', face: 'CardFace', effect: 'Effect') -> None:
        joueur = face.GetControlByPlayer()
        if joueur is not None:
            minion.EngagePlayer(joueur, effect)

    return [
        AbilityFactory.TreatAttachedCardAsMinion(Ally, "Influenced Minion", engager),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
