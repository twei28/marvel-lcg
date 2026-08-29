from . import *

# Ion Amplifiers (1/2)
# Uses (X ion counters, where X is equal to the number of TECH cards you
#   control.)
# Hero Resource: Exhaust Ion Amplifiers and remove 1 ion counter from it →
#   generate a [wild] resource.
#
# Compte DYNAMIQUE, pas fixe : desc.Uses (has_uses.py) n'accepte qu'un
# nombre fixe ou "N*" par joueur, donc pas de cle desc.Uses ici. Les
# compteurs sont poses a la main a l'entree en jeu (modele du couple
# AfterCardEnterPlay + Faces.PlaceCountersOn : with_counters,
# game/ability/factory/counter.py) via `CartesTechControlees` (__init__.py).
# Tranche par l'utilisateur le 29/08/2026 : PAS de defausse automatique a 0
# jeton (le texte imprime de cette carte ne porte pas la clause « discard
# this card », contrairement a Web-Shooter officiel).

def GetAbilities() -> Sequence['Ability']:

    def ion_amplifiers_enter(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        Faces.PlaceCountersOn([this], len(CartesTechControlees(player)), 'ion', effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.NonKeyword,
            "This",
            ion_amplifiers_enter,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, "ion")),
    ]
