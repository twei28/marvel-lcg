from . import *

# Corrupt — le patron des manigances CORROMPUES
#
# ⚠ CETTE CARTE N'EXISTE PAS DANS LE JEU PHYSIQUE. Voir `PoserUneManiganceCorrompue`
# dans le `__init__.py` du set : le jeu de table retourne LA carte du dessus du
# deck du joueur et s'en sert comme manigance. Le moteur ne sait pas faire d'une
# carte joueur une manigance de rencontre, alors on paie le cout (la carte part
# a la defausse) et on pose l'obstacle (un exemplaire de celle-ci). Le joueur
# perd la meme carte, la table porte la meme manigance, et sa menace de depart
# vient de Fisk Tower comme le veut le texte.

def GetAbilities() -> Sequence['Ability']:

    return []
