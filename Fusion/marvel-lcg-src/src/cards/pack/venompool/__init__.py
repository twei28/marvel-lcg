from cards.pack import *

# ===========================================================================
# Pack VENOMPOOL — contenu custom de « CptScorp » (Marvel Champions Custom
# Project, Cycle 2). Set 129, prefixe `vp`.
#
# Wade Wilson porte le symbiote Klyntar : Deadpool avec un costume vivant.
#
# Deux sets :
#   `Venompool`         (vp001a-vp011, dossier venompool/venompool/)
#   `Venompool Nemesis` (vp012-vp016, dossier venompool/venompool_nemesis/)
#
# ⚠ L'INSERT DU PACK INTERDIT DE JOUER DEADPOOL ET VENOMPOOL ENSEMBLE :
# « don't break the rules by running 2 of me in the same game just because the
# name is technically different ». Ce n'est pas decoratif : l'alter-ego du pack
# s'appelle « Wade Wilson », exactement comme 44001b (Deadpool officiel), et
# `desc.GiveTo` de l'obligation vp011 se resout PAR NOM via
# `Worlds.FindPlayerByName` (game/card/face/card_type/obligation.py). Deux
# « Wade Wilson » a la table et l'obligation part chez le premier trouve.
# ===========================================================================
