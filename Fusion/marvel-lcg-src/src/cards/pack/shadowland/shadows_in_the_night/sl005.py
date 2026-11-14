from . import *

# * Black Tarantula — SBIRE. BRUTE. HAND. Guard. ATQ 2 / MNG 2 / PV 5, Boost 3.
# Guard.
# When Revealed : Change the villain's position if it has not changed this phase. If the villain's position is Atop the Tenshu, Black Tarantula attacks you;
#   otherwise, give the villain and Black Tarantula each a tough status card.
#
# Cartes de reference : fne/.../48036 Executioner (attaque a sa propre revelation), rhino/01106 Stampede (`DoAttackYou(player, effect)`),
# core/masters_of_evil/01131 (`Faces.GiveStatus([...], "Tough", effect)`), sl003a/b (position).
# ⚠ Mots-pieges : « if it has not changed THIS PHASE » (une seule fois par phase, tous les changements comptent) ; « attacks YOU » = le joueur a qui elle est
#  revelee ; « the villain AND Black Tarantula each » : DEUX cartes Tough, pas une ; la position est lue APRES le changement eventuel.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        ChangerSiPasChange(effect)
        if AuTenshu(effect):
            this.DoAttackYou(joueur, effect)
        else:
            vilain = Worlds.FindVillain(effect)
            Faces.GiveStatus([f for f in (vilain, this) if f is not None], "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
