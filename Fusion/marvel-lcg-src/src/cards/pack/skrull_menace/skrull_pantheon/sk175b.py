from . import *

# Skrull Pantheon (175B) — ENVIRONNEMENT double face, face DESTROYED (stade 1 termine par « last threat removed »).
# Hero Action: Spend 2 resources of any type → remove 1 faith counter from the villain.
#
# Cartes de reference : voir `sk175a` (meme action, cout different : `Cost('2')`, 2 ressources de n'importe quel type ;
# modele `skrull_empire` Incite Rebellion pour `Cost("2")` dans un choix, et `sk148`... pour un cout simple).
#
# ⚠ Mots-pieges : « of ANY type » (aucune contrainte de couleur) ; meme garde que la face A (action offerte
# seulement s'il y a un jeton de foi a retirer).


def GetAbilities() -> Sequence['Ability']:
    return [ActionRetirerFoi(Cost('2'))]
