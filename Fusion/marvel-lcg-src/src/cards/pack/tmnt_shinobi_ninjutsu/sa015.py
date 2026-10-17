from . import *

# * Kusari-Kagi — AMELIORATION unique 1 [physical], Ninjutsu (TMNT Shinobi, Inkwire). NINJA. WEAPON.
# Restricted.
# Hero Action: Exhaust this card and discard a cloaked status card from your hero -> deal 1 damage to an enemy and
# draw 1 card.
# « Get over here! » —Ronin
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Restricted (restricted.md), Cloak / Cloaked (cloak.md, cloaked.md).
#
# Cartes de reference :
#  - `03009` / `restricted.md` : « Restricted » est LU dans `desc.Restricted` (aucun module) ;
#  - `17007` Element Gun : amelioration Restricted a Hero Action (`CostFunc.Exhaust("This")`, `this.DealDamage(...)`) ;
#  - `sk049` The Thing / `CoutDefausserCloaked("hero")` : cout « discard a <statut> status card from your hero ».
#
# TEXTE CONTRE CODE
#  ⚠ « Restricted » : base automatique (`desc.Restricted = 1`) ; sans module.
#  ⚠ « Exhaust this card AND discard a cloaked status card from YOUR HERO » : DEUX couts, tous deux obligatoires ; sans Cloaked
#    sur le HEROS l'action n'est pas proposee.
#  ⚠ « deal 1 damage to AN ENEMY AND draw 1 card » : les DEUX effets ; un ennemi (sbire ou vilain), 1 degat (pas une
#    attaque) ; la pioche a lieu meme si l'ennemi est vaincu.
#  ⚠ Unique (✦) ; Hero Action : forme heros.


def GetAbilities() -> Sequence['Ability']:

    def kusari_kagi(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        this.DealDamage(effect.targets, 1, effect)
        joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            kusari_kagi,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CoutDefausserCloaked("hero"))
        .SetTarget(Enemy),
    ]
