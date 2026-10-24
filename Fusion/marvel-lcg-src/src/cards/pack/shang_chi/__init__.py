from cards.pack import *

# ===========================================================================
# Pack SHANG-CHI — contenu custom de « DesignHacker », format « SEALED ».
# Prefixe `shc` (tools/prefixes_fanmade.json), set 212.
#
# DEUX sets dans ce pack :
#   - `Shang-Chi`          (shc001a-shc018, dossier shang_chi/shang_chi/)
#   - `Shang-Chi Nemesis`  (shc019-shc021, dossier shang_chi/shang_chi_nemesis/)
# 22 card_id : 2 faces d'identite, State of Flow, 12 evenements ATTACK (6 titres x 2 IMPRESSIONS),
# 3 ameliorations, 1 obligation, 3 cartes nemesis (Downtown Attack en 3 exemplaires).
#
# ⚠ `FileManager.CleanName` rend `shang_chi` et `shang_chi_nemesis` : les noms des deux dossiers de
# modules. L'OBLIGATION `shc018` Family Ties porte `set_name = "Shang-Chi"` : son module vit dans
# `shang_chi/`, PAS dans `shang_chi_nemesis/` (lecon nt012).
#
# ⚠ PREFIXE : `sc` appartient a tmnt_shinobi_dual et 63015 est l'allie Shang-Chi d'Iron Fist
# (autre carte, autre pack). Homonymes de NOM au depot : « Special Delivery » (16148) et
# « The Life Stealer » (sv014, Silver Surfer) : aucun module du pack ne cherche par nom ces deux cartes.
#
# LE PACK EN UNE PHRASE : UNE PILE D'ATTAQUES DEJA JOUEES QUI AMPLIFIENT LA SUIVANTE.
# Mot-cle maison `Flow` (fiche mots-cles/flow.md) : chaque evenement ATTACK imprime une ressource ;
# la carte du dessus de State of Flow (shc002, la derniere attaque jouee) active le Flow de la
# suivante si une de ses ressources IMPRIMEES est celle que ce Flow exige.
# Aucune decklist d'aspect fournie par l'auteur : `player_deck` reste vide (PROCESSUS-HEROS, etape 3).
# ===========================================================================
