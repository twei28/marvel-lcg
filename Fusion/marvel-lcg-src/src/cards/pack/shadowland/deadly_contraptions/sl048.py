from . import *

# Hall of Punishment — COMPLOT ANNEXE. Menace de depart 2 par joueur, Crisis 1, boost ★ seul.
# Forced Interrupt : When you choose the "Trip" effect on a TRAP! card, discard the top 3 cards of your deck.
# ★ Boost : Place 1 threat on the main scheme for each character you control.
#
# Cartes de reference : `QuandOnChoisitUnEffetDePiege` (ce module), player_action.py `DiscardDeckTopCards`, shadows_in_the_night/sl010 (boost de rencontre),
# mut_gen/sabretooth/32069 (`PlaceThreatOnSchemes("MainScheme", n, effect)`), crisis.md (natif).
# ⚠ Mots-pieges : « YOU choose » : le joueur qui choisit Trip (pas tous les joueurs) ; « the top 3 cards of YOUR deck » : son deck ; « each character YOU control » : identite
#  + allies du joueur contre qui l'activation a lieu (le joueur du boost), pas les sbires ; Trip seulement.


def GetAbilities() -> Sequence['Ability']:

    def trip(effect: 'Effect', message: 'QuandOnChoisitUnEffetDePiege') -> bool:
        return message.effet == PIEGE_TRIP

    def defausser(effect: 'Effect', message: 'QuandOnChoisitUnEffetDePiege') -> None:
        message.GetToPlayer().DiscardDeckTopCards(3, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        effect.this.PlaceThreatOnSchemes("MainScheme", len(joueur.GetControlCharacters()), effect)

    return [
        Ability(AbilityType.ForcedInterrupt, QuandOnChoisitUnEffetDePiege, [trip], defausser),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
