from . import *

# Tactical Retreat — EVENEMENT d'aspect PROTECTION, cout 0, RES [mental], x2.
# TACTIC.
# Hero Interrupt: When you would take any amount of damage from an attack,
#   exhaust your hero -> prevent all of that damage. Change to alter-ego form.
#
# ⚠⚠ ELLE FAIT PASSER EN FORME CIVILE, ET C'EST TOUT L'INTERET DU PACK : une
# fois civil, Julia Carpenter recharge 3 compteurs. La carte gratuite qui sauve
# ET recharge.
#
# CARTES DE REFERENCE
#  - `03005` EM Shield : « When you would take any amount of damage from an
#    attack, prevent all of that damage », mot pour mot, par
#    `WhenUnitWouldTakeDamage(Interrupt, "You", op, is_from_attack=True)` +
#    `PreventDamage("All")`.
#  - `01025` Split Personality : `identite.ChangeToOtherIdentityForm(effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « exhaust your hero -> » : COUT. Un heros deja incline ne peut pas jouer
#    la carte, meme s'il va prendre le coup. C'est aussi ce qui rend la carte
#    difficile a mettre en scene : DEFENDRE incline le heros, donc la carte ne
#    se joue que sur une attaque NON defendue. Le cas d'harnais passe par
#    `ip034` Molecule Man, contre qui « Character cannot defend ».
#  ⚠ AUCUN LIBELLE (defense) n'est imprime, contrairement a `01003` Backflip :
#    on n'en pose donc pas. Le modele est `17006` Bad Boy, meme texte au cout
#    pres, qui n'en pose pas non plus.
#  ⚠ « CHANGE to alter-ego form » n'est pas facultatif, et ce n'est pas non
#    plus le changement de forme du TOUR : il ne consomme pas l'action de
#    changement de forme, et il arrive pendant la phase du mechant. D'ou
#    `ChangeToForm(AlterEgo, ...)`, appele directement.
#  ⚠ L'ordre compte : on empeche D'ABORD, on bascule ENSUITE. Basculer avant
#    ferait sortir le heros du jeu et l'empechement porterait dans le vide.


def GetAbilities() -> Sequence['Ability']:

    def repli(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.PreventDamage("All", effect)
        identite = IdentiteDe(effect.GetInitiator())
        if identite is not None:
            identite.ChangeToForm(AlterEgo, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            repli,
            is_from_attack=True,
        ).SetPlay()
        .SetCostFunc(CostFunc.Exhaust("YourHero")),
    ]
