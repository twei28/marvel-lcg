from . import *

# * Bushwhacker — SBIRE. CRIMINAL. MERCENARY. SCH 1, ATQ 0★, 5 PV, Patrol 1, Boost 1.
# Patrol.
# ★ Forced Interrupt : When Bushwhacker would attack, instead take 3 indirect damage. You may spend [mental] or
#   [wild] to deal that damage to another enemy instead.
#
# Cartes de reference : skrull_menace/skrull_empire/sk099.py (`WhenUnitWouldAttack(ForcedInterrupt, "This")` +
# `message.SetBeInstead`, vu aussi sk185), sm/community_service/27176.py (`ChooseAbilities` avec
# `ForChoiceAbilityWithCost`), fne/the_getaway/60133.py (`TakeIndirectDamage` sur l'identite).
#
# Reponses de l'utilisateur (21/10) : le joueur visé (= engagé avec Bushwhacker) encaisse les 3 dégâts indirects et
# peut payer. « [mental] or [wild] » = `Cost("B")` (le joker remplace n'importe quelle icone).
# ⚠ « INSTEAD » : l'attaque n'a pas lieu (ni dégâts ni boost) ; « another enemy » : pas Bushwhacker lui-même.

def GetAbilities() -> Sequence['Ability']:

    def au_lieu_d_attaquer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        message.SetBeInstead(effect)
        joueur = this.GetEngagedPlayer() or Worlds.GetFirstPlayer(effect)

        def sur_un_autre_ennemi(targets: Sequence['CardFace'], res: Any) -> None:
            autres = [e for e in Worlds.GetOnFieldEnemies(effect) if e is not this]
            if not autres:
                return
            cible = autres[0] if len(autres) == 1 else joueur.AskChooseFace(autres, effect)
            if cible is not None:
                this.DealDamage([cible], DamageProperty(damage=3, is_indirect_damage=True), effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Take 3 indirect damage",
                lambda targets: joueur.GetIdentity().TakeIndirectDamage(this, 3, effect),
            ),
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("B"),
                "Spend [mental] or [wild]: deal 3 indirect damage to another enemy",
                sur_un_autre_ennemi,
            ),
        )

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", au_lieu_d_attaquer),
    ]
