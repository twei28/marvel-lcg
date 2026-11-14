from . import *

# Soho (7) — LIEU (environnement LOCATION).
# Increase the cost of each event you play by 1.
# Action: Draw 2 cards, then discard 2 cards. (Limit once per round.)
#
# Cartes de reference : ar010 (`IncreaseResourceCostToPlay(<filtre>, 1, ...)`, cout +1 mesure par une carte jouable a 2 icones, pas a 3),
# 28020 (`player.DrawUp(2, effect)` puis `DiscardHandCards`), pu031 (Action de lieu + `LimitOncePerRound` globale + `Ville.AuLieu`).
# ⚠ « each event YOU play » : seuls les joueurs QUI OCCUPENT Soho paient +1 : `"AnyPlayer"` + `conditions=[Ville.AuLieu]` (le joueur est
# lu sur `message.GetToPlayer()`) ; `"You"` ne vaudrait rien sur un environnement sans controleur.
# ⚠ « Draw 2 cards, THEN discard 2 cards » : pioche d'abord, defausse ensuite, au choix du joueur, dans sa main (2 cartes exactement).

def GetAbilities() -> Sequence['Ability']:

    def piocher_puis_defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        joueur.DrawUp(2, effect)
        joueur.DiscardHandCards(2, effect)

    return [
        AbilityFactory.IncreaseResourceCostToPlay(Event, 1, "AnyPlayer", conditions=[Ville.AuLieu]),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, piocher_puis_defausser, conditions=[Ville.AuLieu])
        .LimitOncePerRound(),
    ]
