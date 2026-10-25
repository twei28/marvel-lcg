from . import *

# Expanding Hive — MANIGANCE ANNEXE. Alien Queen's Scheme. Depart 2[per_hero]. Permanent. Acceleration.
# While there is no threat here, this scheme loses the [acceleration] icon.
# Forced Interrupt: When a minion with 3 or more printed hit points is defeated, give it to the active villain as a facedown boost card.
#
# Cartes de reference :
#  - « Alien Queen's Scheme » : la Reine y manigance (ap001a, `PlaceThreatOnCardWhenThisScheme`) ; aucun code ici ;
#  - « loses the [acceleration] icon » : `ThisGainKeyword(.., acceleration_icon=-1, change_on_event=OnEvent.Threat("This"))` (pd026) ;
#  - « When a minion ... is defeated » : `WhenUnitBeDefeated(ForcedInterrupt, Minion)` ; « give it to the active villain as a facedown
#    boost card » : `GiveBoostCard` (60075) au mechant actif ;
#  - Permanent : natif (`desc.Permanent`).
#
# ⚠ Mots-pieges :
#  - « 3 or more PRINTED hit points » : `printed_health` (un bonus de PV ne compte pas) ; Alien Scout (2) n'y va jamais ;
#  - n'importe quel sbire (YAUTJA, XENOMORPH, nemesis...) ;
#  - le « When Defeated » du sbire se resout ENSUITE sans reprendre la carte (arbitrage du 25/10/2026 : Drone, Young Blood,
#    Blooded Predator restent en boost).


def GetAbilities() -> Sequence['Ability']:

    def au_mechant(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        DonnerCommeBoost(message.trigger, effect)

    def trois_pv_imprimes(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
        return getattr(message.trigger, "printed_health", 0) >= 3 and MechantActif(effect) is not None

    return [
        ManiganceSansMenacePerdLIcone(),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.ForcedInterrupt, Minion, au_mechant, conditions=[trois_pv_imprimes]),
    ]
