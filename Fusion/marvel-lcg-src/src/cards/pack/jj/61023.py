from . import *

# Grapnel Launcher
#
# « Hero Action: Discard this card -> make a basic thwart without exhausting
#   (even if you are exhausted). For this thwart, your hero gets +1 THW and
#   ignores the patrol keyword and any crisis icons in play. »
#
# `BasicThwart` n'epuise pas de lui-meme (l'epuisement est le cout de l'action
# de base, pas du contrer), et l'action n'est pas payee par un epuisement ici :
# le « without exhausting (even if you are exhausted) » est donc acquis.
# Le +1 THW passe par `ThwartProperty(additional_value=1)`, et le patrol/crisis
# ignore par `SetIgnoreKeyword`, le mecanisme dedie du moteur (cf. 42006).

def GetAbilities() -> Sequence['Ability']:

    def grapnel_launcher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        hero = effect.GetInitiator().GetHero()
        if hero is None:
            return
        hero.BasicThwart(effect.targets, effect, property=ThwartProperty(additional_value=1))

    return [
        # Sans cette option, l'amelioration n'entre jamais en jeu ET le moteur
        # evalue quand meme son action de contre : il cherche alors la carte
        # portante d'une amelioration attachee a rien, et leve une assertion
        # (card_face.py `GetBindFace`). « Restricted » l'accroche au heros.
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, grapnel_launcher)
        .SetCostFunc(CostFunc.Discard("This"))
        .SetLabel('thwart')
        .SetTarget(Scheme2, range=(1, 1))
        .SetIgnoreKeyword('Crisis', 'Patrol'),
    ]
