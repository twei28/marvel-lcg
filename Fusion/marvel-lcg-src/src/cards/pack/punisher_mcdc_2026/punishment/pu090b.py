from . import *

# Justice or Punishment? (5B) — ENVIRONNEMENT. Permanent.
# Punisher is the active villain. Encounter cards referring to or affecting "the villain" refer only to Punisher.
# Players may defend any attack, even ones targeting enemies.
# If Punisher's final stage is defeated, the players win the game.
#
# Regles posees par la face 5A a la mise en place (`Villains.SetRule(the_villain="Active")` + Punisher actif) ; « players may
# defend any attack » : applique par `PunisherAttaque(players_may_defend=True)` (__init__.py) ; la victoire sur le dernier stade de
# Punisher est la regle native du dernier stade du vilain. Aucun script propre (a verifier par le cas [pun] de fin de partie).

def GetAbilities() -> Sequence['Ability']:
    return []
