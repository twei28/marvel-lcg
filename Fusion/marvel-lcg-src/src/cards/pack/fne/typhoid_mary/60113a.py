from . import *

# Establish Trust (side scheme 8[per_hero]) — Permanent, Setup : bases desc.
# [star] In expert mode, this card gains hinder 3[per_hero].
# When Defeated: Place 1 threat token on Disturbed Psyche. Flip this card.
# (Une manigance Permanente ne quitte pas le jeu : elle se RETOURNE en
# attachement Mary Walker, qui s'accroche au vilain.)

def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        env = TrouverDisturbedPsyche(effect)
        if env:
            Faces.PlaceTokensOn([env], 1, 'threat', effect)
        VerifierVictoire(effect)
        if Worlds.IsGameOver(effect):
            return
        this.card.Flip(effect, call_reveal=False)
        mw = this.card.face
        vilain = TrouverMary(effect)
        if vilain is not None and CanAttach.IsType(mw):
            mw.AttachTo2(vilain, effect)

    return [
        AbilityFactory.IfExpertModeThisGainKeyword(hinder="3*"),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
