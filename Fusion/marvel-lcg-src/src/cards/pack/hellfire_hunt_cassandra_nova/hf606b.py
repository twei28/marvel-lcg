from . import *

# Mutant Extermination (3B), stade 3 (dernier). Menace 13[per_hero], escalade +1[per_hero], menace de depart 3[per_hero].
# « Forced Response : After your turn ends, if there is Cassandra Controls counter on your identity, you must choose to either place 3 threat here
# or discard 1 card from your hand. Hero Action : Discard 7 cards from the top of the encounter deck -> remove a Cassandra Controls counter from
# your identity. (Limit once per round per player.) When this scheme is completed, the players lose the game. »
# Cartes de reference : hf604b.
# ⚠ Le texte imprime dit « When this scheme is completed, the players lose the game » : la lecture native du texte (scheme_main.py :
# « If this stage/scheme is completed ») ne le reconnait PAS, mais elle n'est pas necessaire : c'est le DERNIER stade (deck des manigances
# principales vide), `World.AdvanceMainScheme` termine la partie par la regle (« The Final Stage of the Main Scheme was Completed »).
# Une capacite `IfThisSchemeStageIsCompletedPlayersLoseTheGame` posee a la main ici etait REDONDANTE (nettoyee le 01/11/2026 : le cas
# `hf606b : complot COMPLETE` reste vert sans elle, et la fin de partie ne se produit qu'une fois).


def GetAbilities() -> Sequence['Ability']:
    return [
        ReponseFinDeTour(3, "Discard 1 card from your hand", PenaliteDefausse, possible=MainNonVide),
        ActionRetirerControle(7),
    ]
