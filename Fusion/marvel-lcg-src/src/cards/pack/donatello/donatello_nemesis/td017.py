from . import *

# Flight of Flyborgs — SBIRE nemesis (5/5). AERIAL. FLYBORGS. SWARM.
#   ATQ / MNG / PV = ★, boost 3.
# Enters play with 4 swarm counters on them.
# [star] This minion's SCH, ATK, and hit points are equal to the number of
#   swarm counters here.
# Forced Interrupt: When this minion takes any amount of damage, remove that
#   number of swarm counters from here instead.
#
# JUMEAU de td016 (Plague of M.O.U.S.E.R.s) : 4 compteurs au lieu de 2, boost
# 3 au lieu de 1, traits AERIAL. FLYBORGS. SWARM. Tout le raisonnement
# (carte de reference, mots-pieges, choix technique sur les PV, TODO-QUESTION
# Q-TD-16 sur la representation des PV ★) est dans `td016.py` et vaut mot pour
# mot ici.
#
# TEXTE CONTRE CODE
#  « 4 swarm counters » (td016 : 2). « remove THAT NUMBER of swarm counters »
#  est la meme lecture que « that many » de td016.
#  Le texte imprime differe de td016 par ces seuls mots : « remove that number
#  of » / « on them ». Aucune difference de regle.


def GetAbilities() -> Sequence['Ability']:

    def jauge(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Minion)
        return this.GetCounters(COMPTEUR_ESSAIM)

    def retirer_des_compteurs(effect: 'Effect',
                              message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Minion)
        degats = message.will_take_damage
        message.SetBeInstead(effect)
        if degats <= 0:
            return
        restants = this.GetCounters(COMPTEUR_ESSAIM)
        Faces.RemoveCountersOn([this], min(degats, restants), COMPTEUR_ESSAIM, effect)
        if this.GetCounters(COMPTEUR_ESSAIM) <= 0:
            Faces.DefeatUnits([this], getattr(message, "source", None), effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(4, COMPTEUR_ESSAIM),
        AbilityFactory.ThisGainKeyword(
            jauge,
            attack=1,
            scheme=1,
            change_on_event=OnEvent.Counter("This", COMPTEUR_ESSAIM),
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "This",
            retirer_des_compteurs,
        ),
    ]
