from . import *

# * Jazinda — SBIRE (Skrull Elite - Jazinda). ELITE. SKRULL. MNG 3, ATQ 1, PV 5[per_hero], Victory 1,
# une etoile de boost (aucune icone chiffree).
# Victory 1.
# The villain gets +1 SCH.
# [star] Boost: Put Jazinda into play engaged with you.
#
# Cartes de reference :
#  - « The villain gets +1 SCH » : **`sk168`** The Revenge Time / **`hs222`** Hunter Mode
#    (`GiveKeywordToInPlayWhenApplyThis(Villain, scheme=1)`), un bonus qui vit tant que la carte est EN JEU.
#  - Boost qui met la carte en jeu : **`hs007`** Regular Rats (`PutIntoPlay(message.GetToPlayer())`).
#
# ⚠ Mots-pieges : « THE VILLAIN » (le mechant, pas les sbires) ; « +1 SCH » (MNG) pas ATQ ; le bonus vit
# tant que Jazinda est EN JEU (pas depuis la main ni la defausse) ; Victory 1 natif ; « engaged with YOU »
# (le joueur qui retourne la carte de boost).


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        MettreEnJeuEngage(effect, effect.this, message.GetToPlayer())

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Villain, scheme=1),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
