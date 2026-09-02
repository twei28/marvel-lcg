from . import *

# Hologram Projection — evenement signature, x1 (n/15 = 1). SUPERPOWER.
# Cout 2, ressource [mental], Requirement ([energy][mental]).
# Hero Interrupt: When an enemy would activate, cancel that activation and
#   confuse that enemy.
#
# Cartes de reference :
#  - 27006 Web Binding (Ghost-Spider), src/cards/pack/sm/ghost_spider/27006.py :
#    meme phrase « When an enemy would activate », meme montage
#    `WhenEnemyWouldActivate(HeroInterrupt, None, ...).SetPlay().SetLabel()`
#    et meme annulation par `message.SetBeInstead(effect)`. Web Binding porte
#    d'ailleurs elle aussi un `Requirement`, ce qui en fait le modele exact ;
#  - 01083 Mockingbird / 05015 Tackle pour la pose de statut par
#    `Faces.GiveStatus(cibles, "Confused", effect)`.
#
# ⚠ AUCUN script pour le `Requirement` : `desc.Requirement` = "YB" est lu
# nativement par `HasCost.RegisterAttribute("Requirement", parse2)`
# (has_cost.py:23). C'est une « base automatique » du guide, au meme titre que
# Toughness. Voir docs/reference/mots-cles/requirement.md.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « an ENEMY would activate » : ennemi, donc le vilain COMME les sbires.
#    `WhenEnemyWouldActivate(..., None, ...)` ne filtre sur aucun type, c'est
#    voulu. Web Binding, elle, teste `Minion.IsType` avant ses degats — pas
#    nous, la desorientation vise les deux.
#  - « cancel THAT activation » : l'activation en cours uniquement, rendue par
#    `SetBeInstead`, pas une interdiction durable.
#  - « confuse THAT enemy » : le MEME ennemi que celui dont on annule
#    l'activation, donc `message.trigger`, jamais un choix du joueur.
#  - Un ennemi `stalwart` ne peut pas etre desoriente : `Faces.GiveStatus`
#    passe par `GainStatus`, qui le refuse proprement et rend 0. L'annulation
#    a deja eu lieu, elle, et c'est le bon ordre : les deux effets sont
#    independants sur le texte imprime.


def GetAbilities() -> Sequence['Ability']:

    def hologram_projection(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.SetBeInstead(effect)

        ennemi = message.trigger
        if ennemi is not None:
            Faces.GiveStatus([ennemi], "Confused", effect)

    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.HeroInterrupt,
            None,
            hologram_projection,
        ).SetPlay().SetLabel(),
    ]
