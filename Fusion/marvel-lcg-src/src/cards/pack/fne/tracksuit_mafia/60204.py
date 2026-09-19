from . import *

# Tracksuit Mafia (side scheme, 3[per_hero])
# When Revealed: Discard cards from the top of the encounter deck until a
#   TRACKSUIT minion is discarded and tuck that minion here.
# Forced Response: After a player reveals a TRACKSUIT minion from the
#   encounter deck, that player reveals 1 minion tucked here.
# ⚠ Le sbire sorti d'ici est lui-meme « revele » : le drapeau `en_cours`
# empeche la reponse de se rappeler elle-meme (le texte dit « from the
# encounter deck », pas « from here »).

def GetAbilities() -> Sequence['Ability']:
    etat = {"en_cours": False}

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        face = Worlds.DiscardEncounterCardsUntil(effect, trait="TRACKSUIT", card_type=Minion)
        if face is not None:
            this.TuckCardUnderHere(face, effect)

    def sortie(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        if etat["en_cours"]:
            return
        joueur = message.GetToPlayer()
        caches = [f for f in this.GetPlacedCardArea().Get() if Minion.IsType(f)]
        if not caches or joueur is None:
            return
        choisi = caches[0] if len(caches) == 1 else joueur.AskChooseFace(caches, effect)
        if choisi is None:
            return
        etat["en_cours"] = True
        try:
            choisi.Reveal(joueur, effect)
        finally:
            etat["en_cours"] = False

    def un_tracksuit_du_deck(effect: 'Effect', message: 'Message.WhenCardRevealed') -> bool:
        return not etat["en_cours"] and message.trigger is not effect.this

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardRevealed(AbilityType.ForcedResponse, CardFinder(trait="TRACKSUIT", card_type=Minion), sortie, conditions=[un_tracksuit_du_deck]),
    ]
