from . import *

# Xenomorph (Warrior) — SBIRE DE JOUEUR, cout 0, [wild]. PV 4, MNG 0 / ATQ 2. XENOMORPH. Hero.
# Teamwork (XENOMORPH).
# When Defeated: Ready Predator.
# Interrupt: When Xenomorph is defeated, shuffle it into your deck.
#
# Cartes de reference :
#  - `al002` * Throg (pack alligator_loki) : le SEUL autre sbire de joueur (type `PlayerMinion`, entete de
#    `game/card/face/card_type/minion_player.py`) : joue depuis la main contre son cout, s'engage avec son proprietaire ;
#    « When Defeated » par `WhenUnitBeDefeated(WhenDefeated, "This", op)` ; remelange dans le deck du PROPRIETAIRE par
#    `Faces.ShuffleAllTo(.., joueur.player_deck, effect)`.
#  - `32159` Fabian Cortez / `38029` Donald Pierce : `desc.Teamwork` natif (fiche mots-cles/teamwork.md), AUCUN script.
#  - `Faces.ReadyAll([heros], effect)` (an001a, 31009) pour « ready Predator ».
#
# ⚠ Mots-pieges :
#  - « Teamwork (XENOMORPH) » : natif, relu dans `desc` ; la Reine et les Drones du set nemesis portent le meme trait.
#  - « When Defeated: Ready PREDATOR » : le HEROS Predator, sans condition « you defeated » (n'importe quel joueur ou carte
#    peut vaincre le sbire).
#  - « Interrupt: When Xenomorph is defeated, shuffle it into YOUR deck » : une Interruption (avant la defaite), au deck du
#    joueur proprietaire ; une carte rangee au deck ne declenche plus son propre « When Defeated ».


def GetAbilities() -> Sequence['Ability']:

    def pret(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        heros = HerosDuJoueur(JoueurDeCetteCarte(effect) or effect.this.card.GetOwner())
        if heros is not None:
            Faces.ReadyAll([heros], effect)

    def remelanger(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        proprietaire = this.card.GetOwner() or JoueurDeCetteCarte(effect)
        if proprietaire is not None:
            Faces.ShuffleAllTo([this], proprietaire.player_deck, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            pret,
        ),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.Interrupt,
            "This",
            remelanger,
        ),
    ]
