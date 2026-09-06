from cards.pack import *

# ===========================================================================
# Pack THROG — set nemesis « Throg Nemesis » (tg012-tg016).
#
# Alligator Loki n'attaque pas Throg : il l'ENCOMBRE. Les cinq cartes visent
# toutes le meme point faible d'un heros qui n'a que 12 PV et 2 ATQ :
#   - tg012 Adorable Distraction le rend INTOUCHABLE tant que le complot est
#     la, pendant que « Hinder 1[per_hero] » ralentit le contre ;
#   - tg013 le sbire lui-meme repand sa menace sur TOUTES les manigances
#     annexes, et transforme donc le complot precedent en machine a menace ;
#   - tg014 Causing a Commotion vide le deck du joueur ;
#   - tg015 « Lost » Property lui CONFISQUE Frogjolnir, la carte autour de
#     laquelle tourne tout le pack ;
#   - tg016 Chomped lui interdit le prochain pouvoir de base.
#
# ⚠ HOMONYME MAJEUR : « * Alligator Loki » (tg013) est un SBIRE nemesis. Le
# HEROS `al001a` du pack `alligator_loki` (set 140) porte le meme nom et n'a
# rien de commun avec lui — ni statistiques, ni texte, ni code. Le plan de
# portage s'etait deja trompe une fois en croyant l'inverse (§6 du todo du
# 29/08/2026) : ne jamais citer une reutilisation sans avoir lu les deux
# cartes.
# ===========================================================================

NOM_SBIRE = "Alligator Loki"
NOM_MORSURE = "Chomped"
