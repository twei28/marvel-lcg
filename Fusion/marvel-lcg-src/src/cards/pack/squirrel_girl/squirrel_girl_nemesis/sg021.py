from . import *

# Poisoned Rumors
# When Revealed: Discard up to 2 SQUIRREL allies you control. If fewer than 2
#   SQUIRREL allies were discarded this way, place 2 threat on Discord in the
#   Branches. If that scheme is not in play, place that threat on the main
#   scheme instead.
# Boost: After this activation ends, exhaust 1 SQUIRREL ally you control.
#
# Reformule le 28/08/2026 : l'ancien « Discard 2 ... If you cannot » etait
# ambigu a 1 seul ecureuil (rien ne se passait). Desormais les deux moities
# peuvent s'appliquer : avec 1 ecureuil, on le defausse ET on pose la menace.

def GetAbilities() -> Sequence['Ability']:

    def rumeurs(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        ecureuils = EcureuilsControles(effect, joueur)
        nb = min(2, len(ecureuils))
        if nb > 0:
            choisis = joueur.AskChooseFaces(ecureuils, nb, nb, effect)
            Faces.DiscardAll(list(choisis) if choisis else ecureuils[:nb], effect)
        if nb >= 2:
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
