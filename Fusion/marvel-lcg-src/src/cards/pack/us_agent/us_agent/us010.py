from . import *

# * U.S. Agent's Machine Gun — amelioration unique, cout 2, ressource [physical]. WEAPON.
# Restricted. U.S. Agent gets +1 ATK. Uses (3 ammo counters.)
# Hero Response: After you damage an enemy, remove 1 ammo counter from here → deal 2 damage to each minion engaged
# with you.
#
# Cartes de reference :
#  - `sh016` Jo : `AfterYouDealDamage(HeroResponse, Enemy, op)` + `CostFunc.Counter("This", n, '<compteur>')` ; `Uses`
#    (`desc.Uses = "3,ammo"`, compteur `ammo` deja au moteur) et `Restricted` sont NATIFS.
#  - `43014` Rictor / `dt015` Preparation #2 : « each minion engaged with you » = `.SetTarget("YourEngagedMinions", range="All")`
#    + `this.DealDamage(effect.targets, N, effect)`.
#  - `mf006` : « <Heros> gets +1 ATK » = `*GiveKeywordToAttached(CardFinder(name=..., card_type=Hero), attack=1)`.
#
# ⚠ Mots-pieges :
#  - « After you damage AN ENEMY » : villain OU sbire, y compris le sbire qu'on vient de toucher s'il est ENGAGE avec soi.
#  - « each minion engaged WITH YOU » : les sbires engages avec CE joueur (pas ceux d'un autre joueur, pas le vilain).
#  - « After you damage an enemy » REPREND les degats de la rafale elle-meme (arbitrage du 26/10/2026, RR Response : « once per
#    occurrence of the triggering condition ») : la Reponse est RE-PROPOSEE a chaque degat inflige, facultative, bornee par les 3
#    compteurs. L'ancienne garde `pas_sa_propre_rafale` l'interdisait. Le pilote du harnais accepte tout : il vide les compteurs.
#  - COUT : retirer UN compteur (aucune inclinaison) ; la capacite repart donc a chaque degat tant qu'il reste des
#    compteurs, jusqu'aux 3 compteurs de `Uses`.


def GetAbilities() -> Sequence['Ability']:

    def machine_gun(effect: 'Effect', message: 'Message.AfterFaceDealDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        this.DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name=NOM_HEROS, card_type=Hero),
            attack=1,
        ),
        AbilityFactory.AfterYouDealDamage(
            AbilityType.HeroResponse,
            Enemy,
            machine_gun,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'ammo'))
        .SetTarget("YourEngagedMinions", range="All"),
    ]
