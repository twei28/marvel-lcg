from . import *

# Stealth Proficiency — EVENEMENT 0 [mental], Ninjutsu (TMNT Shinobi, Inkwire). Aucun trait.
# Hero Action: Discard a cloaked status card from your hero -> ready your hero.
# Hero Response: After you use one of your basic powers, cloak your hero.
# « There is far more potential in chaos... » —Ronin
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloak / Cloaked (cloak.md, cloaked.md).
#
# Cartes de reference :
#  - `sk049` The Thing / `CoutDefausserCloaked` : cout « discard a <statut> status card from <personnage> » ;
#  - `09015` Desperate Defense : « ready your hero » = `Faces.ReadyAll([initiator.GetHero()], effect)` ;
#  - `su009` Mechanical Arms : « After you use a basic power » = `AfterUnitUseBasicPower(HeroResponse, "You", fn)` ;
#  - `up023` Lookout : « cloak your hero ».
#
# TEXTE CONTRE CODE
#  ⚠ DEUX capacites distinctes, une seule carte jouee : l'evenement se joue SOIT en Action, SOIT en Reponse.
#  ⚠ « Discard a cloaked status card FROM YOUR HERO » est le COUT (devant la fleche) : sans Cloaked sur le heros, l'action
#    n'est pas proposee ; « ready YOUR HERO » : le heros, qui est incline ou non (rien ne se passe s'il est pret).
#  ⚠ « After you use ONE OF YOUR BASIC POWERS » : ATQ, CTR, DEF ou REC du joueur (pas un pouvoir d'allie, pas une carte) ;
#    « cloak your hero » : sur le heros (un heros deja camoufle n'en recoit pas une seconde).
#  ⚠ Hero Action / Hero Response : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def preparer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None or not joueur.IsHero():
            return
        Faces.ReadyAll([joueur.GetHero()], effect)

    def camoufler(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None or not joueur.IsHero():
            return
        ShinobiCloak(effect, joueur.GetHero())

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            preparer,
        ).SetPlay().SetLabel()
        .SetCostFunc(CoutDefausserCloaked("hero")),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "You",
            camoufler,
        ).SetPlay().SetLabel(),
    ]
