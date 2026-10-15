from . import *

# * Donatello's Bō — AMELIORATION, cout 2, [energy]. BO. WEAPON.
# Restricted.
# Hero Action: Exhaust this card -> ready Donatello.
#
# CARTES DE REFERENCE
#  - `ho011` Goblin Glider : `CanPlayThisUpgradeCard()` + `HeroAction` a cout
#    `Exhaust("This")` qui fait `Faces.ReadyAll([hero], effect)`.
#  - `04001a` Hawkeye / `03001a` : « ready Donatello » = redresser la face
#    HEROS. `03009` (Captain America's Shield) pour `desc.Restricted`.
#
# TEXTE CONTRE CODE
#  « Restricted » est lu dans `desc` : AUCUN module (mots-cles/restricted.md).
#  « ready DONATELLO » -> le HEROS (`GetHero`), pas l'identite : `HeroAction`
#    n'est de toute facon jouable qu'en forme heros.
#  Insert : la carte entre EPUISEE quand td001b la va chercher (`exhaust=True`
#    cote td001b), donc l'action n'est pas utilisable le tour meme.


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = effect.GetInitiator()
        heros = joueur.GetHero() if joueur is not None else None
        if heros is not None:
            Faces.ReadyAll([heros], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            redresser,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
