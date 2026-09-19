from . import *

# Shop Proprietor (allie de rencontre, CIVILIAN, cout 0, THW 1, ATK 1, 3 PV)
# When Revealed: Put Shop Proprietor into play under your control. This card
#   gains surge.
# Forced Interrupt: When this ally leaves play, place 4 threat on the main
#   scheme in your play area.
# « your play area » = le complot du controleur de l'allie (ComplotDuJoueur).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Ally)
        joueur = message.GetToPlayer()
        this.PutIntoPlay(joueur, effect, under_control=True)
        ThisCardGainSurge(effect)

    def part(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> None:
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()
        if joueur is None:
            return
        scheme = ComplotDuJoueur(effect, joueur) or Worlds.FindMainScheme(effect)
        if scheme is not None:
            this.PlaceThreatOnSchemes([scheme], 4, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardLeavePlay(AbilityType.ForcedInterrupt, "This", part),
    ]
