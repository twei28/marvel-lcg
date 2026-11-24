from cards.pack import *

# ===========================================================================
# Pack THE WARRIORS THREE (Phenexian et Mysteltainn) : prefixe `wt` (tools/prefixes_fanmade.json). Deck `warriors_three`
# (precon Justice) + variante `warriors_three_aggression`. DEUX sets : `Warriors Three` (wt001a-wt015, dossier
# warriors_three/warriors_three/) et `Warriors Three Nemesis` (wt016-wt021, warriors_three/warriors_three_nemesis/).
# wt022 Revelry in Asgard (Team-Up Basic) et wt023-wt025 (reskins de ressources) : sans module, sauf Revelry.
#
# LE PACK EN UNE PHRASE : UNE identite a QUATRE faces (alter ego « The Warriors Three » + Fandral, Hogun, Volstagg) ; le
# changement de HEROS ACTIF est un changement de FORME (les PV sont ceux de l'identite : partages) ; les deux heros inactifs
# sont des soutiens PERSONA mis en jeu au Setup (wt003-wt005), et chacun garde SON etat prêt/epuise (CORRECTIF a l'echange
# dans `synchroniser_formes`, wt002). Le seul CORRECTIF moteur : player_setup.py (pas de changement LIBRE de heros actif).
# ===========================================================================
