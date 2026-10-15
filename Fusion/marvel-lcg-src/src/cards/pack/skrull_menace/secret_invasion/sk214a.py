from . import *

# * Dum Dum Dugan (Sn'Tlo) — ALLIE (paquet IMPOSTOR, face A). CAMOUFLAGED. IMPOSTOR. SKRULL. 4 PV, SCH 2 (1 pastille), ATQ 1 (1 pastille).
# Forced Interrupt: When Dum Dum Dugan would leave play, flip him instead.
# (Regles du paquet, livret p. 16 : un allie CAMOUFLAGED s'utilise comme un allie normal, attaque et defend mais NE PEUT PAS
# contrer ; si l'identite de son controleur est en alter ego pendant la phase du mechant, il manigance apres l'activation du
# mechant, subit un degat consequentiel et ne s'incline pas. Les trois lignes de regle sont COMMUNES aux 20 cartes :
# `AllieImpostor()`, helper du set.)
#
# Cartes de reference :
#  - Interruption forcee « When X would leave play, flip X instead » : **`gambit 37034`** Psionic Shield
#    (`WhenCardWouldLeavePlay(ForcedInterrupt, "This", op)` + `message.SetBeInstead(effect)`).
#  - « cannot thwart » : **`cap 03028`** (`*UnitCannotThwartTarget(who, cannot_thwart=True)`).
#  - Retournement allie -> sbire : **`fne 60113a`** Establish Trust (`card.Flip(effect, call_reveal=False)` hors du
#    chemin de revelation automatique) ; revelation explicite `Reveal(joueur, effect, is_by_flipping=True)`.
#  - Manigance en alter ego apres l'activation du mechant : `AfterEnemyActivationEnd` (**`sk107`** Skrull Scientist).
#
# ⚠ Mots-pieges : « would LEAVE play » (defaite, defausse, retour en main : TOUT depart) ; le garde `en_retournement`
# evite que le retournement lui-meme relance l'interruption ; l'ATQ « 1* » donne 1 degat(s)
# consequentiel(s) apres chaque attaque (une pastille = 1 degat) ; le SCH de l'allie est lu sur la face sbire (meme
# valeur sur les deux faces, la classe Ally n'a pas de stat SCH) ; les PV sont le badge orange (decision NOTES.md).


def GetAbilities() -> Sequence['Ability']:
    return AllieImpostor()
