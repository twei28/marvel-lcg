from cards.pack import *

# ===========================================================================
# Pack U.S. AGENT — contenu custom de « DesignHacker », format « SEALED ».
# Prefixe `us` (tools/prefixes_fanmade.json ; `ua` est pris par TMNT Aspect Aggression), set 218.
#
# DEUX sets dans ce pack :
#   - `U.S. Agent`          (us001a-us012, dossier us_agent/us_agent/)
#   - `U.S. Agent Nemesis`  (us013-us016, dossier us_agent/us_agent_nemesis/)
# 17 card_id : 2 faces d'identite, 10 cartes signature (Bouncing Bulwark x3, Deflection x2, Reckless x2, Roundhouse x2
# et six cartes uniques), 1 obligation (Forced Leave, set « U.S. Agent » : son module vit dans us_agent/, lecon nt012),
# 4 cartes nemesis (Seeing Red en 2 exemplaires).
#
# ⚠ `FileManager.CleanName("U.S. Agent")` rend `us_agent` : nom du pack ET du dossier du set.
# ⚠ Des cartes « U.S. Agent » existent deja (04014 trors, 56075 cw, sw014 spider_woman_kajislav) : aucune n'est touchee,
# et les modules du pack cherchent leurs cartes par `card_id` ou par NOM exact (« U.S. Agent's Shield »).
#
# LE PACK EN UNE PHRASE : UN BOUCLIER QU'ON LANCE (Bouncing Bulwark) ET QU'ON REPREND, des armes a compteurs, et un
# alter ego (John Walker) qui joue TOUS les aspects mais ni allies ni cartes Basic (« Master of None », regle de
# deckbuilding declaree dans deck/starter/us_agent.json, metadata.deckbuilding).
# Decklist d'aspect FOURNIE par l'auteur (« US Agent Starter Deck.png ») : 25 cartes officielles.
# ===========================================================================
