from . import *

# * Mary Walker (PERSONA) — Attach to the villain. Permanent.
# [star] Attached villain cannot activate.
# Forced Response: After the villain takes damage or the round ends, deal each
#   player 1 facedown encounter card and flip this card.
# (Le retour vers Establish Trust : FlipMaryWalkerVersEstablishTrust.)

def GetAbilities() -> Sequence['Ability']:

    def rechute(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Attachment)
        premier = Worlds.GetFirstPlayer(effect)

        def action(joueur: 'Player') -> None:
            joueur.DealEncounterCards(1, effect)

        Players.ForEachPlayer(effect, action)
        FlipMaryWalkerVersEstablishTrust(effect, premier)

    def le_vilain(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> bool:
        this = effect.this.CastTo(Attachment)
        return message.trigger is this.GetBindFace()

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.EnemyCannotActivate(AbilityType.NonKeywordStar, "AttachedEnemy"),
        AbilityFactory.AfterUnitTookDamage(AbilityType.ForcedResponse, Villain, rechute, conditions=[le_vilain]),
        AbilityFactory.WhenRoundEnd(AbilityType.ForcedResponse, None, rechute),
    ]
