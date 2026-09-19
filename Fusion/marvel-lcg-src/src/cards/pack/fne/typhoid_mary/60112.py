from . import *

# Disturbed Psyche (environment) — Setup (base desc : commence en jeu).
# Setup: Put the villain into play on a random side (and reveal it).
# Forced Interrupt: When the villain phase ends, flip the villain.
# If there are 3 or more tokens here, the players win the game!
#
# Le scenario met deja le vilain en jeu (stade unique 60110a / 60111a) : le
# Setup se contente de le retourner une fois sur deux (Rand), la revelation
# etant celle de la mise en place. ⚠ Hors de portee du harnais (WhenGameWouldBegin
# part une fois, avant lui) : verificateur dedie `fne_setup_psyche`.
# Retournement : card.Flip (modele 45101a),
# a la fin de la phase du mechant (WhenPhaseEnd "Villain"). Victoire :
# Worlds.SetGameOver(True) (32130), verifiee a chaque jeton pose ici.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        vilain = TrouverMary(effect)
        if vilain and Rand.RandomChoice([True, False], effect):
            vilain.card.Flip(effect)

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        vilain = TrouverMary(effect)
        if vilain:
            vilain.card.Flip(effect)

    def jeton(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> None:
        VerifierVictoire(effect)

    return [
        # Une carte Setup (desc) n'a PAS de message WhenCardSetup (envoye pour
        # les complots) : sa capacite Setup vit sur AfterGameSetup (cc001, 58031).
        AbilityFactory.AfterGameSetup(mise_en_place),
        AbilityFactory.WhenPhaseEnd(AbilityType.ForcedInterrupt, "Villain", fin_de_phase),
        AbilityFactory.AfterCardPlacedToken(AbilityType.ForcedResponse, "This", None, jeton),
    ]
