from . import *

# * Queen of Sogaria — manigance JOUEUR signature, x1 (11/15). Cout 7,
# ressource [B]. Menace de depart 5. Victory 0.
# Only Red Sonja can remove threat from this scheme. She may use her basic
# ATK, DEF or THW to do so.
# While Queen of Sogaria is in the victory display, Red Sonja gains:
# "Response: After you exhaust Hyrkanium Blade, draw 1 card. (Limit once
# per round.)"
#
# CARTES DE REFERENCE
#  - `40006` Technovirus Purge (officiel, Cable) : modele de manigance
#    JOUEUR signature -- `AbilityFactory.ThreatCannotBeRemovedFromWhile(
#    "This", by_character=CardFinder(non_name=...))` pour « Only X can
#    remove threat from this scheme » (la seconde phrase, « she may use her
#    basic ATK/DEF/THW », est la regle GENERIQUE des pouvoirs de base contre
#    une manigance -- rien a coder, chaque pouvoir de base sait deja la
#    contrer).
#  - `ls008` Sif's Steed : `Message.AfterCardExhausted` construit a la main
#    (aucune fabrique dediee), filtre `Condition.CheckWhichCard`.
#
# ⚠⚠ « Red Sonja GAINS » une Reponse tant que la carte est dans la vitrine de
# victoire : la capacite ne peut PAS vivre ici, sur rs009 elle-meme -- une
# carte dans la vitrine est `is_out_of_play=True`, donc aucune capacite
# posee dans SON PROPRE `GetAbilities()` n'est jamais enregistree tant
# qu'elle y reste, quelle que soit la condition ecrite a l'interieur (bug
# trouve le 23/09/2026 PAR le cas de test de cette carte, jamais declenche
# une seule fois). Deplacee sur `rs001a.py` (l'identite, toujours en jeu),
# condition `QueenDeSogariaEstEnVitrine` (`__init__.py` de ce dossier) --
# voir ce fichier pour le detail complet du piege et la reference moteur.

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            by_character=CardFinder(non_name="Red Sonja"),
        ),
    ]
