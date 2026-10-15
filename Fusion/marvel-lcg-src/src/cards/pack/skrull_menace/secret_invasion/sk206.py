from . import *

# Invasion Fleet — TRAITRISE (Secret Invasion). ★ + 2 boosts.
# When Revealed: Each player puts a REVEALED minion at random from the IMPOSTOR deck into play engaged with them.
# ★ Boost: Put a REVEALED minion at random from the IMPOSTOR deck into play engaged with you.
#
# Cartes de reference : **`sk202`** (meme squelette allie -> sbire) ; `Players.ForEachPlayer` (**`fne 60113b`**) ;
# helper `MettreSbireRevele` (le sbire est REVELE par le joueur : son « When Revealed » le met en jeu engage).
#
# ⚠ Mots-pieges : « EACH player ... engaged with THEM » : un sbire par joueur, engage avec lui ; « REVEALED minion » (pas un allie) ;
# Boost : « engaged with YOU » = le joueur a qui la carte est retournee.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        Players.ForEachPlayer(effect, lambda joueur: MettreSbireRevele(effect, joueur))

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        MettreSbireRevele(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
