from . import *

# Cassandra Nova (I). MUMMUDRAI. PSIONIC. « [star] Forced Response : After Cassandra Nova activates against you, place 1 Cassandra Controls counter on
# your identity card. »
# Cartes de reference : AbilityFactory.AfterEnemyActivatesAgainstYou (activate.py ; modele sk255 Skrull : reponse apres l'activation CONTRE un joueur,
# attaque OU complot), hg `PoserInfection` (compteur nomme sur l'identite).
# ⚠ « activates against YOU » : le joueur vise (`message.GetAgainstPlayer()`), pas celui dont c'est le tour.


def GetAbilities() -> Sequence['Ability']:
    return [ReponseControle()]
