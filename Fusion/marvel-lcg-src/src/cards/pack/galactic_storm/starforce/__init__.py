from cards.pack import *

# ===========================================================================
# Set modulaire STARFORCE (Galactic Storm, Kajislav) — gs209-gs217.
# Insert du scenario 5 : « minions mostly with the victory keyword and three
# boost icons. When these minions enter the victory display, they grant the
# villain a bonus. » OBLIGATOIRE pour Supreme Intelligence, utilisable avec
# n'importe quel mechant.
#
# « While <sbire> is in the victory display, the villain ... » (RECETTES-MOTEUR
# §3bis) :
#  - un bonus de STATISTIQUE ou de MOT-CLE (SCH, ATK, retaliate, steady) passe
#    par `GiveKeywordToInPlayWhenApplyThis(Villain, works_in_the_victory_display
#    =True, ...)` (modele next_evol/40006 Technovirus Purge) ;
#  - « the villain's attacks gain overkill / piercing » n'est pas un mot-cle de
#    carte mais une propriete de l'ATTAQUE : `UnitAttackGainKeyword(Villain, ...)`
#    posee sur le sbire, avec `.NoOutOfPlayLimit()` (la capacite d'une carte
#    HORS JEU n'est pas lue sans ce drapeau) et la condition « ce sbire est dans
#    la pile de victoire ».
# « The villain » = le mechant en jeu (plusieurs : celui que le moteur designe).
# ===========================================================================


def EstEnVitrine(face: 'CardFace') -> bool:
    return bool(face.card.area.flags.is_victory_display)


def BonusDeStatEnVitrine(**bonus: int) -> List['Ability']:
    """« While X is in the victory display, the villain gets +1 SCH / gains retaliate 1 / gains steady. »"""
    return [*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
        Villain,
        works_in_the_victory_display=True,
        **bonus,
    )]


def AttaquesDuMechantEnVitrine(*, overkill: bool = False, piercing: bool = False) -> 'Ability':
    """« While X is in the victory display, the villain's attacks gain overkill / piercing. »"""

    def en_vitrine(effect: 'Effect', message: 'Message.CheckIfAttackMessageHasKeyword') -> bool:
        Unused(message)
        return EstEnVitrine(effect.this)

    return AbilityFactory.UnitAttackGainKeyword(
        Villain,
        overkill=overkill,
        piercing=piercing,
        conditions=[en_vitrine],
    ).NoOutOfPlayLimit()
