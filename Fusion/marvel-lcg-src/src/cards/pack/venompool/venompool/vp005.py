from . import *

# Thwip! — evenement. SUPERPOWER. THWART. Cout 1. x2
# Hero Action (thwart): Stun the villain. If the villain is already stunned,
#   remove 3 threat from a scheme instead.
#
# Cartes de reference :
#  - 18028 Waylay (pack gam) : `face.IsStunned()` puis
#    `Faces.GiveStatus([face], "Stunned", effect)`.
#  - pt006 Covered Fire / 07011 Chaos In the Prison : le ciblage DYNAMIQUE par
#    `player.ChooseAbilities(effect, ForChoiceAbility(...).SetTarget(...))`,
#    seule facon d'ouvrir un choix de complot SEULEMENT dans la branche qui en
#    a besoin. Un `SetTarget(Scheme2)` fixe forcerait a designer un complot
#    meme quand la carte se contente d'etourdir.
#
# ⚠ mot-piege « instead » (PROCESSUS-CARTE etape 5) : les 3 points de menace
# REMPLACENT l'etourdissement, ils ne s'y ajoutent pas. Les deux branches sont
# donc exclusives, d'ou le `return` dans la premiere.

def GetAbilities() -> Sequence['Ability']:

    def thwip(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        villain = Worlds.FindVillain(effect)
        if villain is None:
            return

        if not villain.IsStunned():
            Faces.GiveStatus([villain], "Stunned", effect)
            return

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 3 threat from a scheme",
                lambda targets:
                    this.RemoveThreatFromSchemes(list(targets), 3, effect),
            ).SetTarget(Scheme2, range=(1, 1)),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            thwip,
        ).SetPlay().SetLabel('thwart'),
    ]
