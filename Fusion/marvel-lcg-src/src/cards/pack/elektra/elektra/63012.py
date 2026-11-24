from . import *

# Elektra's Sai — AMELIORATION, cout 2, [physical]. WEAPON. Restricted. x2 (Elektra 12-13/15).
# Restricted.
# Hero Action: Exhaust Elektra's Sai -> deal 1 damage to an enemy and reduce the cost of the next ACROBATIC or ATTACK event you
# play this phase by 1.
#
# CARTES DE REFERENCE
#  - Hero Action d'amelioration qui s'epuise et inflige 1 degat a un ennemi : le Hero Action d'une arme officielle, ex. `01032`
#    (Mjolnir n'est pas comparable) -> modele de structure : `CostFunc.Exhaust("This")` + `SetTarget(Enemy)` +
#    `this.DealDamage` (Root Stomp 16005 pour DealDamage hors attaque de base).
#  - « reduce the cost of the next <traits> card you play this phase by N » : `bm001b` / `us009`,
#    `Worlds.UpdateNextCardPlayCost(joueur, -N, effect, finder=CardFinder(check_face_fn=...), in_this="Phase")`.
#  - « Restricted » : base automatique (`desc.Restricted`), aucun script.
#
# TEXTE CONTRE CODE
#  ⚠ « the next ACROBATIC OR ATTACK EVENT » : un EVENEMENT portant l'un ou l'autre trait ; une amelioration ATTACK ne compte pas.
#  ⚠ « THIS PHASE » : `in_this="Phase"`, pas Round ni Turn. « by 1 » : -1, jamais sous 0.
#  ⚠ Le « -> » est le COUT : s'epuiser. « 1 damage to an enemy » : un coup d'une capacite, PAS une attaque de base (aucun Villainous).
#  Chiffres : cout 2, 1 degat, reduction de 1.


def GetAbilities() -> Sequence['Ability']:

    def sai(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        this.DealDamage(effect.targets, 1, effect)
        Worlds.UpdateNextCardPlayCost(
            joueur, -1, effect,
            finder=CardFinder(check_face_fn=lambda f: Event.IsType(f) and (f.HasTrait('ACROBATIC') or f.HasTrait('ATTACK'))),
            in_this="Phase",
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            sai,
        ).SetCostFunc(CostFunc.Exhaust("This")).SetTarget(Enemy),
    ]
