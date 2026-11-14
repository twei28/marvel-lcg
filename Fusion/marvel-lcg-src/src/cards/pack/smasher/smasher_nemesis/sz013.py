from . import *
# Biosynthetic Sting, traitrise nemesis (x2). Boost : ★ seul (aucune icone imprimee).
#
# When Revealed: Take 1 damage. You are stunned.
# [star] Boost: Reveal this card.
#
# Cartes de reference : 56176 Pheromones (When Revealed qui pose un statut au joueur) ; 04092 / 16140 (« [star] Boost: Reveal this card » =
# `WhenCardBecomeBoost("This", RevealThisCard)`).
def GetAbilities() -> Sequence['Ability']:
    def revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        identite = message.GetToPlayer().GetIdentity()
        this.DealDamage([identite], 1, effect)
        Faces.GiveStatus([identite], "Stunned", effect)
    return [
        AbilityFactory.WhenThisRevealed(None, revealed),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]
