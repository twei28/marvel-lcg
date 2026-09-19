from . import *

# Power Struggle (side scheme, Acceleration : base automatique)
# When Revealed: Defeat the minion with the fewest remaining hit points in
#   play. Discard cards from the encounter deck until you discard a minion.
#   Reveal that minion.
#
# Modeles : 24023 Out for Blood (Filter.One fewest_remaining_hp), 01116b
# Underground Distribution (DiscardEncounterCardsUntil), 01095 Rhino (Reveal).
# Sans sbire en jeu, la premiere phrase ne fait rien et la suite se resout.

def GetAbilities() -> Sequence['Ability']:

    def lutte(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        joueur = message.GetToPlayer()
        sbire = Filter.One(Worlds.GetOnFieldMinions(effect), effect, fewest_remaining_hp=True)
        if sbire:
            Faces.DefeatUnits([sbire], this, effect)
        face = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if face:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            lutte,
        ),
    ]
