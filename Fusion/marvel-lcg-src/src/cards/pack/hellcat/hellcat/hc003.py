from . import *
# * Cat Suit — AMELIORATION, cout 2, [energy]. ARMOR. INFERNAL.
# You get +3 hit points.
# Hero Interrupt: When you make a basic thwart, exhaust Cat Suit and spend a
#   [mental] resource → you get +2 THW and ignore the patrol keyword for this
#   thwart.
#
# Modeles : 05023 Endurance (`GiveKeywordToAttached("You", health=3)`), tg006
# Thunderous Charge (`WhenUnitMakeThwart(..., is_basic_thwart=True)`), 21191
# Fandral (`UnitIgnoreKeywordIcons(..., patrol=True, while_use_basic_thw=True)`).
#
# ⚠ LIMITE ASSUMEE : Patrouille verrouille la CIBLE (`MainScheme.CanBeThwartBy`,
#   scheme_main.py), AVANT que cette interruption ne soit proposee. Le
#   complot principal n'est donc pas offert sous Patrouille, et l'ignorance
#   accordee ici n'a d'effet que si la cible etait deja legale. Meme famille
#   de cas limite que 15012 Crisis Averted (mots-cles/crisis.md). A verifier
#   en partie reelle : un joueur qui compte sur Cat Suit contre un sbire
#   Patrouille ne verra pas le complot principal.

def GetAbilities() -> Sequence['Ability']:

    def cat_suit(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Upgrade)
        message.GainTHWForThisThwart(2, effect)
        this.effect.RegisterTemp(
            AbilityFactory.UnitIgnoreKeywordIcons(
                message.trigger,
                patrol=True,
                while_use_basic_thw=True,
            ),
            unregister_after_exec=False,
            until_event_end=message,
        )

    return [
        *AbilityFactory.GiveKeywordToAttached("You", health=3),
        AbilityFactory.WhenUnitMakeThwart(
            AbilityType.HeroInterrupt,
            "You",
            Scheme2,
            cat_suit,
            is_basic_thwart=True,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Spend(Cost("B"))),
    ]
