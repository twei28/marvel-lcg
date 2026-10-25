from . import *

# Xenomorph's Prey — MANIGANCE ANNEXE (set « Predator Nemesis »), menace 3 par joueur, Boost 2. Hazard.
# Once the hunter, now the hunted. The Xenomorph's Queen has marked her prey.
# While this card is in play, Predator cannot gain cloaked status cards.
# When Revealed: Place 1 additional threat here for each status card in play.
#
# Cartes de reference :
#  - `mf015` Hubris (mister_fantastic_nemesis) : `WhenThisRevealed(None, op)` + `this.PlaceThreatOnSchemes([this], n, effect)` ;
#  - `ah006` Gamma Barrier (totally_awesome_hulk) : `WhenUnitWouldBeStatus(type, unite, [statuts], op)` puis
#    `message.SetBeInstead(effect)` pour REFUSER la pose d'une carte d'etat ;
#  - `Hazard` et `StartingThreat "3*"` : bases automatiques (`desc`, fiches mots-cles/hazard.md).
#
# ⚠ Mots-pieges :
#  - « Predator CANNOT gain cloaked status cards » : NOM PROPRE, la face HEROS ; tant que la manigance est en jeu ; une carte Cloaked
#    deja posee RESTE (« cannot gain », pas « loses »). Regle continue (`AbilityType.NonKeyword` : une `Rule` resterait active apres le retrait de la carte).
#  - « for EACH status card IN PLAY » : toutes les cartes d'etat en jeu, de n'importe quel personnage (Sonne, Desoriente, Coriace,
#    Camoufle...), ennemis compris ; comptees a la revelation.
#  - « 1 ADDITIONAL threat » en plus de la menace imprimee (3 par joueur).


def GetAbilities() -> Sequence['Ability']:

    def pas_de_camouflage(effect: 'Effect', message: 'Message.WhenStatusWouldCardPlaceOn') -> None:
        Unused(effect)
        message.SetBeInstead(effect)

    def proie(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)
        etats = NombreDeCartesDEtat(effect)
        if etats:
            this.PlaceThreatOnSchemes([this], etats, effect)

    return [
        AbilityFactory.WhenUnitWouldBeStatus(
            AbilityType.NonKeyword,
            CardFinder(name=NOM_HEROS, card_type=Hero),
            ["Cloaked"],
            pas_de_camouflage,
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            proie,
        ),
    ]
