from . import *

# Plague of M.O.U.S.E.R.s — SBIRE nemesis (3/5 et 4/5, UN card_id, 2 copies).
#   MOUSERS. SWARM. SCH / ATK / PV = ★, boost 1.
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
#  - `16036` Particle Cannon : `ThisEnterPlayWithCounters(n, 'nom')`.
#  - `27067` Sand Clone / `bw016` : ATK/SCH = nombre de compteurs, par
#    `ThisGainKeyword(fn, attack=1, change_on_event=OnEvent.Counter(...))`.
#  - `gorr/gb009` Black Berserker et `skrull_pantheon/sk178` Nogor : PV calcules
#    par `ThisGainKeyword(fn, health=1, ...)`.
#  - `status/tough.py` : « when X takes damage, Y instead » =
#    `WhenUnitWouldTakeDamage(ForcedInterrupt)` + `SetBeInstead`.
#
# TEXTE CONTRE CODE (decision du 15/10/2026 : PV suivis DYNAMIQUEMENT)
#  « SCH, ATK, AND hit points » -> les trois suivent le compteur ; `desc.HP`
#    vaut 0, les PV viennent des compteurs. AUCUNE mort donnee a la main : quand
#    le dernier compteur part, PV = 0 et le moteur (`CanHealth.LimitHealth`)
#    vainc le sbire comme pour une vraie sante epuisee.
#  « remove THAT MANY swarm counters » -> autant que de degats SUBIS (apres
#    prevention), plafonne au nombre de compteurs. « INSTEAD » -> `SetBeInstead` :
#    les degats n'ont pas lieu (jamais d'inscription sur la carte).
#  « any amount of damage » -> au moins 1 (defaut de la fabrique).
#  Tout le montage est dans `CapacitesEssaim` (`__init__.py`), partage avec td017.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesEssaim(2)
