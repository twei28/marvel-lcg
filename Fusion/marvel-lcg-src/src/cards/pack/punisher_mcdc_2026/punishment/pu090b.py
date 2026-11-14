from . import *

# Justice or Punishment? (5B) — ENVIRONNEMENT. Permanent.
# • Punisher is the active villain. Encounter cards referring to or affecting "the villain" refer only to Punisher.
# • Players may defend any attack, even ones targeting enemies.
# If Punisher's final stage is defeated, the players win the game.
#
# Cartes de reference : regle 1 = `Villains.SetRule(the_villain="Active")` + Punisher actif, posee par pu090a a la mise en place ;
# regle 2 = `PunisherAttaque(players_may_defend=True)` (__init__.py) ; regle 3 : `WhenUnitBeDefeated(WhenDefeated, ...)` +
# `Worlds.SetGameOver(True, effect)`.
# ⚠ « Punisher's FINAL stage » : le dernier stade de la liste du scenario (pu087a en standard, pu087b en expert) ; le moteur ne
# gagne pas tout seul ici : deux vilains sont en jeu, le sous-fifre (cible, intouchable) reste vivant, la regle native « le dernier
# stade du vilain vaincu » ne se declenche donc pas pour Punisher.

STADES_FINAUX = ("pu087a", "pu087b")

def GetAbilities() -> Sequence['Ability']:

    def victoire(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        if message.trigger.paper.card_id in STADES_FINAUX:
            Worlds.SetGameOver(True, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, CardFinder(name="Punisher"), victoire),
    ]
