from . import *

# Hardwire Access — Evenement 1 [mental], classe Hero. THWART.
# [star] As an additional cost to play this event, exhaust Head (Intact) or
#   destroy it.
# Hero Action (thwart): Remove 3 threat from among schemes in play, plus X,
#   where X is the number of Exposed status cards in play.
#
# Cartes de reference :
#  - `03011` Falcon: Sam Wilson : le retrait de menace REPARTI entre plusieurs
#    complots, `range=("Zero", N), repeat_rules="Threat"` puis
#    `RemoveThreatFromSchemes(targets, 1, effect)`. C'est le seul montage qui
#    laisse le joueur ventiler la menace.
#  - `36010` Torrential Rain pour la meme phrase avec un total fixe.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « from **among** schemes in play » : la menace se REPARTIT, elle ne tombe
#    pas sur un seul complot. `SetTarget(Scheme2)` seul serait faux.
#  - « Exposed status cards **in play** » : tout le plateau, allies compris,
#    pas seulement les ennemis ni la cible (helper `ExposedEnJeu`).
#  - X se lit AU MOMENT DE LA SELECTION : le maximum du selecteur est une
#    fonction, pas un nombre fige a la construction de la capacite.
#  - Aucune mention de Crise : pas d'`ignore_crisis`.


def GetAbilities() -> Sequence['Ability']:

    def hardwire_access(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            hardwire_access,
        ).SetPlay().SetLabel('thwart')
        .SetCostFunc(CostFunc.Custom(
            SelecteurComposantIntact(nom=NOM_HEAD),
            InclinerOuDetruire,
        ))
        .SetTarget(
            Scheme2,
            range=("Zero", lambda effect: 3 + ExposedEnJeu(effect)),
            repeat_rules="Threat",
        ),
    ]
