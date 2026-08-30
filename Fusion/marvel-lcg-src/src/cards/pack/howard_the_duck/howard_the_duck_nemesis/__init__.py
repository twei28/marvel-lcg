from cards.pack import *

# ===========================================================================
# Set nemesis de HOWARD THE DUCK — contenu custom de RyCoRan.
#
# Composition du `nemesis_set` standard (data/nemesis/howard_the_duck_
# nemesis.json) : hd022 Duck and Cover!, hd023 Collector, hd025 Duck, Duck,
# Doom!, hd026 A Fowl Plot, hd027 Duck Hunt — CINQ cartes, comme tout set
# nemesis officiel.
#
# hd024 HELLCOW est la SIXIEME carte du set physique et n'est PAS dans le
# `nemesis_set` : c'est un sbire nemesis ALTERNATIF, a utiliser A LA PLACE du
# Collector (hd023) quand on affronte le scenario du Collector — le Collector
# est un vilain OFFICIEL du pack `gmw` (cartes 16070-16081), il ne peut pas
# etre des deux cotes de la table a la fois. Hellcow existe donc bien dans le
# jeu, est scriptee et testee, mais n'est jamais tiree par le set standard.
# Arbitrage de l'utilisateur du 30/08/2026.
#
# ICONES : deux icones distinctes, verifiees par decoupe d'image cote a cote
# avec `ag011` comme temoin (arbitrage utilisateur du 30/08/2026, encadre
# ajoute a `docs/reference/mots-cles/hazard.md` et `acceleration.md`) —
# hd022 porte HAZARD (carte penchee nue), hd026 porte ACCELERATION (pointe +
# barre de soulignement). Les deux sont des mots-cles AUTOMATIQUES, lus par
# le moteur dans `desc.Hazard` / `desc.Acceleration` : aucun code.
# Idem `Villainous` sur hd023 et `Quickstrike` sur hd024.
# ===========================================================================
