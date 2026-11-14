from . import *

# * Convincer — amelioration unique, cout 2, ressource [energy]. TECH. WEAPON.
# Restricted. U.S. Agent gets +1 ATK. Uses (3 charge counters.)
# Hero Response: After you damage a minion with base hit points of 5 or less, exhaust Convincer and remove 1 charge
# counter from here → stun that minion.
#
# Cartes de reference :
#  - `mf006` Unstable Uniform : « <Heros> gets +1 DEF » = `*AbilityFactory.GiveKeywordToAttached(CardFinder(name=..., card_type=Hero),
#    ...)` (liste a deballer avec `*`).
#  - `sh016` Jo : `AfterYouDealDamage(HeroResponse, Enemy, op)` + `CostFunc.Counter("This", n, '<compteur>')`, cibles dans
#    `message.who_took_damage` ; `Uses` et `Restricted` sont NATIFS (`desc.Uses = "3,charge"`, `desc.Restricted`).
#  - `ch015` Stark Nunchaku (meme auteur) : `Exhaust("This")` + `Counter(...)` en cout.
#
# ⚠ Mots-pieges :
#  - « a minion with BASE hit points of 5 or less » : les PV IMPRIMES du sbire (`printed_health`), pas les PV restants ni
#    les bonus (Genetically Enhanced +3 ne change rien).
#  - « After you damage A MINION » : un sbire, pas le vilain ; « that minion » : celui qui a pris les degats (le premier
#    qui remplit la condition s'il y en a plusieurs).
#  - COUT : incliner ET retirer UN compteur ; sans compteur la capacite n'est pas offerte.


def GetAbilities() -> Sequence['Ability']:

    def sbires_etourdissables(message: 'Message.AfterFaceDealDamage') -> List['CardFace']:
        return [x for x in (message.who_took_damage or [])
                if Minion.IsType(x) and x.IsInPlay() and x.printed_health <= 5]

    def un_sbire_assez_petit(effect: 'Effect', message: 'Message.AfterFaceDealDamage') -> bool:
        Unused(effect)
        return len(sbires_etourdissables(message)) > 0

    def convincer(effect: 'Effect', message: 'Message.AfterFaceDealDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        Faces.GiveStatus(sbires_etourdissables(message)[:1], "Stunned", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name=NOM_HEROS, card_type=Hero),
            attack=1,
        ),
        AbilityFactory.AfterYouDealDamage(
            AbilityType.HeroResponse,
            Minion,
            convincer,
            conditions=[un_sbire_assez_petit],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'charge')),
    ]
