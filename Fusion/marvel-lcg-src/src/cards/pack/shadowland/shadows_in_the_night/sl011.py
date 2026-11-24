from . import *

# Moonlit Silhouette — TRAITRISE.
# When Revealed (Alter-Ego) : Change the villain's position if it has not changed this phase. You are confused.
# When Revealed (Hero) : If the villain's position is Atop the Tenshu, the villain schemes; otherwise, the villain attacks you.
#
# Cartes de reference : core/rhino/01106 Stampede (`WhenThisRevealed("Hero", ...)` / `("Alter-Ego", ...)`), skrull_menace/standard_skrull/sk259 (`DoSchemes(joueur, effect)`).
# ⚠ Le changement de position n'est imprime que sur la branche ALTER-EGO : en forme HEROS la position n'est PAS changee, on la lit telle quelle ; « the villain schemes »
#  = une manigance du vilain contre CE joueur (avec son boost) ; « you are confused » = l'identite devient confuse.


def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        ChangerSiPasChange(effect)
        Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Confused", effect)

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilain = Worlds.FindVillain(effect)
        if vilain is None:
            return
        if AuTenshu(effect):
            vilain.DoSchemes(joueur, effect)
        else:
            vilain.DoAttackYou(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
    ]
