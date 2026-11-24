from . import *

# Nimble — EVENEMENT, cout 1, [energy] (x2 dans le deck). DEFENSE. SKILL.
# Hero Interrupt (defense): When you would take any amount of damage, prevent 3 of that damage. Resolve the
#   "Special" ability of a [[WAKANDA]] card you control.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - `05005` Wiggle Room / `14015` Side Step : `WhenUnitWouldTakeDamage(HeroInterrupt, "You", op).SetPlay()
#    .SetLabel('defense')` + `message.PreventDamage(3, effect)`.
#  - Special : `51025` (`ChooseAbilities` + `ForChoiceAbility` + `ResolveSpecialAbility`).
#
# MOTS-PIEGES
#  - « prevent 3 of THAT damage » : au plus 3, jamais plus que ce qui allait etre subi (le moteur borne).
#  - « Special of a WAKANDA card YOU CONTROL » : n'importe quel type de carte a Special (heros, amelioration,
#    soutien, allie), pas seulement une amelioration (contraste avec rz009/rz010).
#  - l'Interruption se joue AVANT les degats ; le Special est resolu ensuite, dans le meme effet.
def GetAbilities() -> Sequence['Ability']:

    def esquive(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = JoueurDeCetteCarte(effect)
        message.PreventDamage(3, effect)
        if joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            CarteWakandaSousControle(
                AbilityFactory.ForChoiceAbility(
                    "Resolve the \"Special\" ability of a WAKANDA card you control",
                    lambda targets: joueur.ResolveSpecialAbility(targets, effect),
                ),
            ),
        )

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            esquive,
        ).SetPlay().SetLabel('defense'),
    ]
