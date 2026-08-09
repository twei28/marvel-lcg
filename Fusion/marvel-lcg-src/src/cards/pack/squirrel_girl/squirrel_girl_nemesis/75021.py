from . import *

# Poisoned Rumors
# When Revealed: Discard 2 SQUIRREL allies you control. If you cannot, place
#   2 threat on Discord in the Branches. If that scheme is not in play, place
#   that threat on the main scheme instead.
# Boost: After this activation ends, exhaust 1 SQUIRREL ally you control.

def GetAbilities() -> Sequence['Ability']:

    def rumeurs(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        ecureuils = EcureuilsControles(effect, joueur)
        if len(ecureuils) >= 2:
            choisis = joueur.AskChooseFaces(ecureuils, 2, 2, effect)
            Faces.DiscardAll(list(choisis) if choisis else ecureuils[:2], effect)
            return

        discorde = Worlds.FindCardOnField(effect, name=NOM_DISCORDE)
        if discorde is not None:
            this.PlaceThreatOnSchemes([discorde], 2, effect)
        else:
            this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    def boost(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        joueur = message.GetToPlayer()
        ecureuils = [face for face in EcureuilsControles(effect, joueur)
                     if face.card.state.is_ready]
        if not ecureuils:
            return
        choisi = joueur.AskChooseFace(ecureuils, effect)
        Faces.ExhaustAll([choisi] if choisi else ecureuils[:1], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            rumeurs,
        ),
        # « After this activation ends » : l'epuisement est resolu des le
        # retournement de la carte boost. Un ecureuil n'agit que pendant le
        # tour du joueur, jamais pendant l'activation d'un ennemi : le moment
        # exact ne change rien a la table.
        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.Boost,
            None,
            boost,
        ),
    ]
