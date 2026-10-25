from . import *

# Skulls for the Taking — MANIGANCE ANNEXE. Predator Warlord's Scheme. Depart 2[per_hero]. Permanent. Acceleration.
# While there is no threat here, this scheme loses the [acceleration] icon.
# Forced Response: After an ally is defeated by an enemy attack, tuck it under here.
# Insert : Trophy Taken a priorite (l'allie qu'il vainc est retire de la partie) ; quand cette manigance quitte le jeu, les allies glisses
#   dessous vont a la defausse de leur proprietaire.
#
# Cartes de reference :
#  - « loses the [acceleration] icon » : `ThisGainKeyword(acceleration_icon=-1)` (pd026) ;
#  - « After an ally is defeated by an enemy attack » : `AfterUnitDefeatedUnit(ForcedResponse, Enemy, Ally, is_from_attack=True)` ;
#    « tuck it under here » : `TuckCardUnderHere` (fiche tuck.md) ;
#  - « leaves play » (insert : allies glisses -> defausse de leur proprietaire) : NATIF, les cartes glissees sous une carte qui quitte le
#    jeu partent a la defausse de leur proprietaire (mesure du 25/10/2026 : le cas « Skulls quitte le jeu » reste vert sans aucun code ;
#    une capacite `WhenCardWouldLeavePlay` ecrite d'abord a ete retiree, elle faisait double emploi).
#
# ⚠ Mots-pieges :
#  - « by an ENEMY attack » : pas une traitrise ni un degat indirect ; l'allie doit etre arrive a la defausse (Trophy Taken l'a retire
#    du jeu avant : il n'est plus la, rien a glisser) ;
#  - les allies glisses ne reviennent qu'a la sortie de la manigance.


def GetAbilities() -> Sequence['Ability']:

    def glisser(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        allie = message.target.card.face
        if allie.IsInPlay() or allie.card.area.flags.is_removed:
            return
        this.TuckCardUnderHere([allie], effect)

    return [
        ManiganceSansMenacePerdLIcone(),
        AbilityFactory.AfterUnitDefeatedUnit(AbilityType.ForcedResponse, Enemy, Ally, glisser, is_from_attack=True),
    ]
