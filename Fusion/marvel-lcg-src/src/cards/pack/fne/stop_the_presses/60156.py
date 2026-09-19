from . import *

# * Robbie Robertson (DAILY BUGLE, PERSONA) — Uses (3 stamina) : base.
# Response: After a player is dealt a facedown encounter card, exhaust Robbie
#   Robertson and remove 1 stamina counter from him -> look at that encounter
#   card. You may discard it and deal that player another facedown encounter
#   card.
# AfterPlayerDealEncounterCard ; la carte = message.would_message.face.

def GetAbilities() -> Sequence['Ability']:

    def relire(effect: 'Effect', message: 'Message.AfterPlayerDealEncounterCard') -> None:
        joueur_vise = message.GetToPlayer()  # TriggerPlayerMessage : pas de `trigger`
        carte = message.would_message.face
        controleur = effect.this.GetControlByPlayer() or joueur_vise
        if carte is None or controleur is None:
            return
        choix = controleur.AskChooseFace([carte], effect, forced=False)  # « You may » = forced=False
        if choix is not None:
            Faces.DiscardAll([carte], effect)
            joueur_vise.DealEncounterCards(1, effect)

    a = AbilityFactory.AfterPlayerDealEncounterCard(AbilityType.Response, relire).SetName("Robbie Robertson: look at that encounter card, you may discard it")
    for c in CoutDeReporter():
        a = a.SetCostFunc(c)
    return [a]
