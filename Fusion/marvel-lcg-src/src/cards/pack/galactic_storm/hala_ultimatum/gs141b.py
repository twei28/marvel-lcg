from . import *

# Hidden Might of Hala (1B) — MANIGANCE PRINCIPALE, stade 1. Seuil 9[per_hero], depart 2[per_hero],
#   escalade +1[per_hero].
# Forced Interrupt: When a minion is defeated, remove 1 hideout counter from Hala.
# Forced Response: After the last hideout counter is removed from Hala, advance to stage 2A.
# If this scheme is completed, the players lose the game.
#
# Cartes de reference :
#  - « When a minion is defeated, remove 1 hideout counter from Hala » : `WhenUnitBeDefeated` (modele
#    sk190b Queen Veranke) + `RetirerRepli` (hala_ultimatum/__init__.py).
#  - « After the last hideout counter is removed from Hala, advance to stage 2A » :
#    `AbilityFactory.AfterCardRemovedCounter(..., is_last_counter=True)` sur un `CardFinder` qui vise Hala
#    (PAS « This », la carte qui porte les jetons n'est pas la manigance) + `MainScheme.Advance("2A", effect)`
#    (modele `challenges/2412_wrath_of_the_mad_titan.py`).
#  - « If this scheme is completed, the players lose the game » : natif (desc, texte affiche), aucun module.
#
# ⚠ Mots-pieges : « a minion is defeated » = N'IMPORTE QUEL sbire (pas seulement ceux de ce scenario) ;
# « the LAST hideout counter » (le declencheur ne part qu'au jeton final, pas a chaque retrait) ; « remove
# 1 hideout counter » peut echouer SANS jeton (rien a faire, le texte ne dit pas « if you cannot »).


def GetAbilities() -> Sequence['Ability']:

    def repli_mine(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        RetirerRepli(effect, 1)

    def avancer(effect: 'Effect', message: 'Message.AfterCardRemovedCounter') -> None:
        Unused(message)
        effect.this.CastTo(MainScheme).Advance("2A", effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.ForcedInterrupt, Minion, repli_mine),
        AbilityFactory.AfterCardRemovedCounter(
            AbilityType.ForcedResponse,
            CardFinder(name=NOM_HALA, card_type=Environment),
            'hideout',
            avancer,
            is_last_counter=True,
        ),
    ]
