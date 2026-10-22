from . import *

# Into the Labyrinth (1B) — MANIGANCE PRINCIPALE, stade 1. Menace de depart 25 par joueur, escalade +1 par joueur, pas de menace cible (« ∞ » imprime).
# When Revealed : Place 10[per_hero] passage counters on Shifting Corridors (7[per_hero] instead in expert mode).
# Forced Interrupt : When Shifting Corridors would take any amount of damage, remove that much threat from here instead.
# Forced Interrupt : When the last threat is removed from this scheme, advance to stage 2A (the players win by advancing).
#
# Cartes de reference : gmw/collector_2/16082b (`WhenLastThreatRemoveFromThisScheme` + `this.Advance(None, effect)`), skrull_menace/skrull_empire/__init__ (`rediriger` :
# `WhenUnitWouldTakeDamage` + `SetBeInstead` + `message.will_take_damage`), core/rhino/01097b (nombres), web_of_deceit/the_lizard/wd054b (compteurs sur le vilain).
# ⚠ Mots-pieges : « 10[per_hero] » : 10 x nombre de joueurs (7 x en expert) ; « any amount of damage » : TOUT le montant subi (apres Tough, reductions...) devient menace
#  retiree ; « from HERE » : de CE complot (sl038b), pas d'un autre ; « the last threat » : menace tombee a 0 ; pas de menace cible (le « ∞ » imprime = jamais atteinte,
#  desc sans TargetThreat) : le complot ne peut pas etre « accompli », seulement avance.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        corridors = Corridors(effect)
        if corridors is None:
            return
        par_joueur = 7 if Worlds.IsExpert(effect) else 10
        Faces.PlaceCountersOn([corridors], par_joueur * Worlds.GetPlayerNumIcon(effect), 'passage', effect)

    def degats_en_menace(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this
        montant = message.will_take_damage
        message.SetBeInstead(effect)
        if montant > 0:
            this.RemoveThreatFromSchemes([this], montant, effect)

    def derniere_menace(effect: 'Effect', message: 'Message.AfterCardRemovedToken') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(message)
        this.Advance(None, effect)

    def contre_corridors(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return message.trigger.IsCardId(CORRIDORS)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, Villain, degats_en_menace, conditions=[contre_corridors]),
        AbilityFactory.WhenLastThreatRemoveFromThisScheme(AbilityType.ForcedInterrupt, derniere_menace),
    ]
