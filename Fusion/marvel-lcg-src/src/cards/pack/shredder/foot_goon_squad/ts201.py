from . import *

# * Bebop — SBIRE UNIQUE (Foot Goon Squad). BRUTE. FOOT CLAN. WARTHOG. MNG 0 / ATQ 2* / PV 4.
# Toughness.
# [star] Bebop's attacks gain piercing.
# [star] Boost: If this activation is an attack, it gains piercing. Otherwise,
#   deal this card to the first player as a facedown encounter card.
#
# Cartes de reference : `wd110` Tiger (`UnitAttackGainKeyword("This", piercing=
# True)` + boost piercing) ; `tl015` (detournement du rangement du boost vers les
# cartes distribuees : `FaceCacheeAuPremierJoueur`) ; Toughness lu dans `desc`.
#
# ⚠ HOMONYME : ce `ts201` est le SBIRE Bebop du set Foot Goon Squad ; le VILAIN
# « Bebop » du pack `tk` est une autre carte. Rien ici n'est cherche par le nom.
# Mots-pieges : « Otherwise » = l'activation n'est PAS une attaque (une
# manigance) ; « to the FIRST player » ; `Toughness` : carte robuste a l'entree.


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if EstUneAttaque(message):
            message.would_atk_message.GainPiercing(effect)
        else:
            FaceCacheeAuPremierJoueur(effect, effect.this)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
