from . import *

# Malediction — TRAITRISE. Boost 1.
# When Revealed (Alter-Ego) : You may place 2 corruption counters on your Creeping Corruption. If you do not, the villain schemes with +2 SCH.
# When Revealed (Hero) : If your Creeping Corruption has the OVERPOWERING trait, the villain schemes with +1 SCH; otherwise, the villain attacks you.
#
# Cartes de reference : gmw/ship_command/16148 Special Delivery (meme montage : `WhenThisRevealed("Alter-Ego")` + `MayChooseOneAbility`, sinon `DoSchemes(... SchemeProperty(additional_value))` ;
#  `WhenThisRevealed("Hero")` + `DoAttackYou`), hood/standard_ii/24050 (`SchemeProperty(additional_value)`).
# ⚠ Mots-pieges : « you MAY » = facultatif ; « if you do not » = refus OU impossibilite (pas de Creeping Corruption) : le vilain manigance +2 SCH ; deux compteurs d'un coup (4 -> 6) retournent la
#  carte ; la branche Hero lit le trait sur la face COURANTE de LA Creeping Corruption du joueur (sl072b = OVERPOWERING, sl072a non) ; sans Creeping Corruption : « otherwise » (le vilain attaque).


def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        accepte = joueur.MayChooseOneAbility(effect, BrancheCorruption(effect, joueur, 2))
        if accepte is None:
            vilain = Worlds.FindVillain(effect)
            if vilain is not None:
                vilain.DoSchemes(joueur, effect, property=SchemeProperty(additional_value=2))

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilain = Worlds.FindVillain(effect)
        if vilain is None:
            return
        if CorruptionOverpowering(joueur):
            vilain.DoSchemes(joueur, effect, property=SchemeProperty(additional_value=1))
        else:
            vilain.DoAttackYou(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
    ]
