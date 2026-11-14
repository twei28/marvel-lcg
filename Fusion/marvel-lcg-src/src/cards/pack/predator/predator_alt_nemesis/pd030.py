from . import *

# Get To The... — TRAITRISE (set « Predator Alt Nemesis »), Boost 2.
# When Revealed: The villain schemes. Place 2 threat on The Chopper side scheme.
#
# Cartes de reference :
#  - `27113` / `27082` (sm) : `villain.DoActivate(player, effect)` ; `enemy.DoSchemes(player, effect)` (enemy.py:46) pour « the
#    villain schemes » ; `PoserDeLaMenaceSurLeChopper` (helper du set).
#
# ⚠ Mots-pieges :
#  - « The villain SCHEMES » : une MANIGANCE du vilain contre le joueur qui revele (pas une activation au choix) ;
#  - « Place 2 threat ON THE CHOPPER side scheme » : le nom propre, 2 menaces, rien si elle n'est pas en jeu.


def GetAbilities() -> Sequence['Ability']:

    def vers_l_helicoptere(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer() or JoueurDeCetteCarte(effect)
        vilain = Worlds.FindVillain(effect)
        if vilain is not None and joueur is not None:
            vilain.DoSchemes(joueur, effect)
        PoserDeLaMenaceSurLeChopper(effect, 2)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            vers_l_helicoptere,
        ),
    ]
