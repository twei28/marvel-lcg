from . import *

# White Queen, forme A (PSIONIC), stade 102. « [star] Forced Response : After White Queen attacks you, discard the top card of the
# encounter deck. If that card has the ILLUSION trait, reveal it. Flip White Queen (whether that card had the ILLUSION trait or not). »
# Cartes de reference : 55039 Malekith (`AfterUnitAttackYou` + `Worlds.DiscardEncounterTopCard`, joueur = `GetAgainstPlayer`),
# 45144 Warstar (`face.Reveal`), tk001a/tk002a Bebop (`villain.card.Flip`, un retournement n'est pas une defaite).
# ⚠ « you » = le joueur attaque ; le retournement a lieu MEME si la carte n'a pas le trait (parenthese imprimee).


def GetAbilities() -> Sequence['Ability']:
    return [ReponseForceeFormeA()]
