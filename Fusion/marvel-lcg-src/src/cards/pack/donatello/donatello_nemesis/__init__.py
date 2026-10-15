from cards.pack import *

# ===========================================================================
# Set nemesis « Donatello Nemesis » (Baxter Stockman, Mousers, Flyborgs).
#
# ⚠ L'OBLIGATION `td013` Broken Shell N'EST PAS ICI : son bandeau imprime dit
# « DONATELLO », pas « DONATELLO NEMESIS ». Son `set_name` est celui du set
# HEROS, son module vit donc dans `donatello/donatello/` (piege bt019 / sf010).
#
# ⚠ TRAITS MOUSERS / FLYBORGS : ecrits au PLURIEL, comme sur les lignes de
# traits imprimees (« MOUSERS. SWARM. », « AERIAL. FLYBORGS. SWARM. ») et sur
# Baxter Stockman (« any MOUSERS or FLYBORGS »). Le texte de td014 dit « a
# MOUSER or FLYBORG minion » au singulier : voir TODO-QUESTION dans td014.
# ===========================================================================

TRAITS_ESSAIM = ["MOUSERS", "FLYBORGS"]
COMPTEUR_ESSAIM: 'CardFace.COUNTER' = "swarm"
