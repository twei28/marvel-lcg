from . import *

# Protectors of the Kree Empire (1B) — COMPLOT PRINCIPAL (Supreme Intelligence). Objectif 6 (★, SANS
# silhouette), escalade +2 (SANS silhouette), depart 0.
# The target threat value of this scheme cannot be changed.
# ★ Forced Interrupt: When this scheme would be completed, remove all threat from here instead and put a
#   random set aside STARFORCE minion into play engaged with the first player. Then, if there are 5 or less
#   set aside STARFORCE minions, advance to stage 2A.
#
# Cartes de reference :
#  - **`aos/50104b`** Upgrading Adaptoids : `WhenMainSchemeStageWouldBeCompleted(ForcedInterrupt, "This",
#    op)` + `message.SetBeInstead(effect)`, un objet mis de cote AU HASARD mis en jeu, puis une condition sur
#    ce qui reste mis de cote ; **`skrull_menace/paibok/sk145b`** pour « remove all threat from here instead ».
#  - « advance to stage 2A » : **`gmw/16082b`** / `mut_gen/32125b` (`this.Advance(None, effect)`).
#  - « The target threat value ... cannot be changed » : AUCUN modele dans le depot. AJOUT moteur
#    (scheme_main.py `GainTargetThreatValue`) : un complot dont le texte porte cette phrase ignore toute
#    modification de son objectif (voir .planning/galactic-storm/defs/supreme_intelligence_moteur.md).
#
# ⚠ Mots-pieges : « INSTEAD » (le complot n'est PAS complete : la partie continue) ; « remove ALL threat from
# HERE » (de ce complot ; c'est un effet du scenario, pas des joueurs : la Crise ne le bloque pas,
# `ignore_crisis=True`) ; « a RANDOM set aside STARFORCE minion » (aucun : rien n'entre) ; « THEN, if there
# are 5 OR LESS set aside » (compte APRES la mise en jeu ; <= 5) ; « advance to stage 2A ».


def GetAbilities() -> Sequence['Ability']:

    def serait_complete(effect: 'Effect', message: 'Message.WhenMainSchemeStageWouldBeCompleted') -> None:
        this = effect.this.CastTo(MainScheme)
        message.SetBeInstead(effect)
        this.RemoveThreatFromSchemes([this], "All", effect, ignore_crisis=True)
        MettreEnJeuUnStarforceAuHasard(effect)
        if len(SbiresStarforceMisDeCote(effect)) <= 5:
            this.Advance(None, effect)

    return [
        AbilityFactory.WhenMainSchemeStageWouldBeCompleted(
            AbilityType.ForcedInterrupt,
            "This",
            serait_complete,
        ),
    ]
