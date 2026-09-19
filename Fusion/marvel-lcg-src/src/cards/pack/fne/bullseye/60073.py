from . import *

# Deranged Bloodlust (side scheme, 4, aléa : base)
# When Revealed: Place additional threat here equal to Bullseye's stage number.
# [star] Boost: After this activation, reveal this card.
# Modeles : 01109 Bomb Scare (menace additionnelle), 07009 Escaped Convict
# (message.AfterThisActivation).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        bullseye = TrouverBullseye(effect)
        if bullseye:
            this.PlaceThreatOnSchemes([this], bullseye.printed_stage, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        joueur = message.GetToPlayer()
        message.AfterThisActivation(effect, lambda: this.Reveal(joueur, effect))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
