from cards.pack import *

# ===========================================================================
# Set nemesis « Donatello Nemesis » (Baxter Stockman, Mousers, Flyborgs).
#
# ⚠ L'OBLIGATION `td013` Broken Shell N'EST PAS ICI : son bandeau imprime dit
# « DONATELLO », pas « DONATELLO NEMESIS ». Son `set_name` est celui du set
# HEROS, son module vit donc dans `donatello/donatello/` (piege bt019 / sf010).
#
# ⚠ TRAITS MOUSERS / FLYBORGS : ecrits au PLURIEL, comme sur les lignes de
# traits imprimees (« MOUSERS. SWARM. », « AERIAL. FLYBORGS. SWARM. ») et sur
# Baxter Stockman (« any MOUSERS or FLYBORGS »). Le texte de td014 dit « a
# MOUSER or FLYBORG minion » au singulier : decision du 15/10/2026, traits pluriels conserves.
# ===========================================================================

TRAITS_ESSAIM = ["MOUSERS", "FLYBORGS"]
COMPTEUR_ESSAIM: 'CardFace.COUNTER' = "swarm"


def CapacitesEssaim(compteurs_a_l_entree: int) -> List['Ability']:
    """Les trois phrases communes de td016 / td017 (Plague of M.O.U.S.E.R.s, Flight
    of Flyborgs), qui ne different que par le nombre de compteurs de depart.

    « This minion's SCH, ATK, AND HIT POINTS are equal to the number of swarm
    counters here » : les TROIS suivent le compteur, par la meme fabrique
    (`ThisGainKeyword(..., attack=1, scheme=1, health=1)`, modele `gorr/gb009` et
    `skrull_pantheon/sk178` pour les PV). `desc.HP` vaut 0 : tout vient des compteurs.

    « Forced Interrupt: when this minion takes any amount of damage, remove that
    many swarm counters from here INSTEAD » : les degats sont REMPLACES
    (`SetBeInstead`) par un retrait de compteurs. Aucune mort donnee a la main :
    quand le dernier compteur part, les PV (= compteurs) tombent a 0 et c'est
    `CanHealth.LimitHealth` du moteur qui VAINC le sbire, exactement comme pour
    une vraie sante epuisee (decision utilisateur du 15/10/2026, phase B).
    """
    def jauge(effect: 'Effect', ui: List['CardFace']) -> int:
        Unused(ui)
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

    return [
        AbilityFactory.ThisEnterPlayWithCounters(compteurs_a_l_entree, COMPTEUR_ESSAIM),
        AbilityFactory.ThisGainKeyword(
            jauge,
            attack=1,
            scheme=1,
            health=1,
            change_on_event=OnEvent.Counter("This", COMPTEUR_ESSAIM),
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "This",
            retirer_des_compteurs,
        ),
    ]
