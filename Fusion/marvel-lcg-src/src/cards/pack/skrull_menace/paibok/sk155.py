from . import *

# * General Kalamari — SBIRE (Paibok). ELITE. SKRULL. SOLDIER. PV 4, MNG 2, ATQ 2, 2 icones de boost.
# When Defeated: The player who defeated General Kalamari resolves the "Boost" ability on each
#   attachment in play, that belongs to the Paibok encounter set.
#
# Cartes de reference :
#  - Fenetre « When Defeated » d'un sbire : `AbilityFactory.WhenUnitBeDefeated(WhenDefeated, "This", ...)`
#    (guide §3.1, modele `32072` pour `GetDefeatingPlayer`).
#  - Resolution des Boost : helper `ResoudreLesBoosts` (paibok/__init__.py), modele `24017` Double Trouble
#    (`Faces.ResolveAbility(...)`).
#
# ⚠ Mots-pieges : « The player WHO DEFEATED » le general = `message.GetDefeatingPlayer()` (le joueur qui
# controle l'attaquant) ; defait par un EFFET sans joueur (Retaliate d'un autre ennemi...) : repli sur le
# premier joueur (a signaler si le cas se presente) ; « each attachment IN PLAY, that belongs to the Paibok
# SET » : attachements de rencontre du set seulement (pas les ameliorations, pas d'autres sets).


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        joueur = message.GetDefeatingPlayer() or Worlds.GetFirstPlayer(effect)
        ResoudreLesBoosts(effect, joueur)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
