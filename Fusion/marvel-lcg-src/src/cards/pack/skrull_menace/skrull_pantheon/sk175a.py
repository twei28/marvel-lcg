from . import *

# Skrull Pantheon (175A) — ENVIRONNEMENT double face, face STRONGHOLD (stade 1 accompli).
# Hero Action: Spend 2 resources of the same type → remove 1 faith counter from the villain.
#
# Cartes de reference :
#  - Cout « 2 ressources de meme type » : **`next_evol/40090`** Heavy Armament et **`tt/55035`** Wrapped in
#    Chains (`SetCost(Cost('2', same_type=True))`) ; Action de heros : `WhenInYourPlayTurn(
#    AbilityType.HeroAction, op)` (modele 55035).
#  - Retrait : `Faces.RemoveCountersOn([mechant], 1, 'faith', effect)`.
#
# ⚠ Mots-pieges : « 2 resources of the SAME type » (deux cartes de meme couleur ; un joker compte pour tout
# type, regle du moteur) contre la face Destroyed (« of ANY type ») ; « the villain » (le mechant en jeu,
# Kly'bn ou Sl'gur't) ; le cout est avant la fleche → : l'action n'est offerte que s'il reste un jeton de foi a
# retirer (sinon le cout serait paye pour rien, voir defs/pantheon_questions.md).


def GetAbilities() -> Sequence['Ability']:
    return [ActionRetirerFoi(Cost('2', same_type=True))]
