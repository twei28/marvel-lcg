from . import *

# Plague of M.O.U.S.E.R.s — SBIRE nemesis (3/5 et 4/5, UN card_id, 2 copies).
#   MOUSERS. SWARM. ATQ / MNG / PV = ★, boost 1.
# Enters play with 2 swarm counters on them.
# [star] This minion's SCH, ATK, and hit points are equal to the number of
#   swarm counters here.
# Forced Interrupt: When this minion takes any amount of damage, remove that
#   many swarm counters from here instead.
#
# LECTURE DU SCAN (verifiee contre 01167 Vulture) : le disque orange « ★ » est
# les PV, la marque rouge du coin est le BOOST (1). Pas de boost etoile.
#
# CARTES DE REFERENCE
#  - `16036` Particle Cannon : `ThisEnterPlayWithCounters(n, 'nom')` pour
#    « enters play with N counters ».
#  - `27067` Sand Clone : « ATK/SCH equal to the number of X counters » =
#    `ThisGainKeyword(fn, attack=1, change_on_event=OnEvent.Counter(...))`
#    (+ `bw016` pour `OnEvent.Counter("This", "rage")`).
#  - `status/tough.py` (via mots-cles/toughness.md) : « when X takes damage,
#    Y instead » = `WhenUnitWouldTakeDamage(...)` + `message.SetBeInstead(
#    effect)`.
#  - `faces.py` : `Faces.RemoveCountersOn`, `Faces.DefeatUnits`.
#
# TEXTE CONTRE CODE
#  « SCH, ATK, AND hit points » -> SCH et ATQ suivent le compteur par
#    `ThisGainKeyword(attack=1, scheme=1)` (base imprimee 0).
#  ⚠ CHOIX TECHNIQUE (sans effet sur les regles, a verifier) : les PV ne sont
#    PAS suivis dynamiquement. `desc.HP = "1"` et la mort est donnee A LA MAIN
#    quand le dernier compteur part. Raison : un gain de PV dynamique sur une
#    base 0 risque une mort immediate a l'entree en jeu, et les degats ne
#    s'inscrivent jamais sur la carte (ils retirent des compteurs), donc les PV
#    ne servent a rien d'autre que l'affichage. Voir le rapport (a tester :
#    surplus de degats / Deferlement).
#  « remove THAT MANY swarm counters » -> autant que de degats SUBIS (apres
#    prevention), plafonne au nombre de compteurs. « INSTEAD » -> `SetBeInstead`
#    : les degats n'ont pas lieu.
#  « any amount of damage » -> au moins 1 (defaut de la fabrique).
#  Plus aucun compteur -> le sbire est VAINCU (PV = 0) : `DefeatUnits`, avec la
#    source des degats comme vainqueur pour les « after you defeat ».
#
# TODO-QUESTION Q-TD-16 : representation des PV « ★ » (voir ci-dessus) — a
# confirmer en phase C (surplus de degats, Deferlement).


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
        AbilityFactory.ThisEnterPlayWithCounters(2, COMPTEUR_ESSAIM),
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
