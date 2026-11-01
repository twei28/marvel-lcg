from . import *

# * Mutant Extinction Agenda (MANIGANCE ANNEXE). Menace de depart 2[per_hero], Victory 1, Boost 1 + etoile. « Victory 1. Each SENTINEL minion gets +1 ATK
# and +1 SCH. This card cannot be defeated while a SENTINEL minion is in play. When Revealed : Each player search the encounter deck and discard pile
# for a SENTINEL minion in player order. Put it into play engaged with you. [star] Boost : Put this card into play. »
# Cartes de reference : 27142 Life-Size Decoy (boost `PutThisIntoPlay`), `GiveKeywordToInPlayWhenApplyThis(<finder>, attack=1, scheme=1)`
# (environment.py), `SchemeCannotLeavlPlayWhile(while_card_is_in_play=...)` (defeated.py ; modele sl vault), Victory : natif (`desc.Victory`).
# ⚠ « cannot be defeated » : la menace peut tomber a 0 mais la carte reste en jeu tant qu'un SENTINEL est la ; « in player order » : le premier
# joueur d'abord.


def GetAbilities() -> Sequence['Ability']:
    def sentinelle_partie(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        """Le moteur n'a pas de verification d'etat : une manigance a 0 menace dont la defaite a ete REMPLACEE resterait coincee. Des que la
        derniere SENTINEL a quitte le jeu, une manigance restee a 0 menace est vaincue (Victory 1 : pile de victoire)."""
        this = effect.this.CastTo(EncounterSideScheme)
        if this.IsInPlay() and this.threat == 0 and NombreDeSentinelles(effect) == 0:
            this.Defeated(None, effect)

    return [
        AbilityFactory.AfterCardLeavePlay(AbilityType.ForcedResponse, SENTINELLE, sentinelle_partie),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(SENTINELLE, attack=1, scheme=1),
        AbilityFactory.SchemeCannotLeavlPlayWhile("This", while_card_is_in_play=SENTINELLE),
        AbilityFactory.WhenThisRevealed(None, UneSentinelleParJoueur),
        AbilityFactory.WhenCardBecomeBoost("This", PutThisIntoPlay),
    ]
