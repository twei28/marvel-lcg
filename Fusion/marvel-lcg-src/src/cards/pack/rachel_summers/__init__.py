from cards.pack import *

# ===========================================================================
# Pack RACHEL SUMMERS / MARVEL GIRL (campagne Hellfire Hunt) — contenu custom de Dipsome. Prefixe `rm`
# (tools/prefixes_fanmade.json), deck `rachel_summers`.
#
# DEUX sets : `Marvel Girl` (rm001a-rm013, dossier marvel_girl/) et `Marvel Girl Nemesis` (rm014-rm016,
# marvel_girl_nemesis/).
#
# LE PACK EN UNE PHRASE : Marvel Girl rejoue son tour (Chronoskimming = elle remelange sa main au debut de CHAQUE tour,
# et Temporal Reversal lui donne un TOUR SUPPLEMENTAIRE) ; Temporal Retrieval garde des cartes face cachee pour les
# reprendre apres un effet TEMPORAL. Deux ajouts MOTEUR (marques `# CORRECTIF`) : le tour supplementaire
# (`World.PlayerPhase`, `PlayerPhase.FinDeTourSupplementaire`) et « end this turn » (`EventManager`, drapeau
# `RM_FIN_DE_TOUR`). Voir docs/packs/rachel_summers/GABARITS.md et RECETTES-MOTEUR.md.
# ===========================================================================
