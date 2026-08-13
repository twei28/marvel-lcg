from . import *

# Phase Shift

def GetAbilities() -> Sequence['Ability']:

    # APPROXIMATION ECRITE. La carte agit sur un personnage « dans n'importe
    # quelle zone, y compris la zone de mission, le deck ou la main » : le
    # moteur ne sait donner un mot-cle qu'a une carte EN JEU. La carte agit donc
    # sur un personnage ami en jeu, ce qui couvre le cas courant ; la version
    # « dans le deck ou la main » n'a pas de crochet.
    def phase_shift(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        for cible in effect.targets:
            cible.effect.Register(
                AbilityFactory.ThisGainKeyword(
                    lambda effect2, ui: 1,
                    treat_as_blank=True,
                    have_res_icon="G",
                )
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            phase_shift
        ).SetPlay()
        .SetTarget(Friend),
    ]
