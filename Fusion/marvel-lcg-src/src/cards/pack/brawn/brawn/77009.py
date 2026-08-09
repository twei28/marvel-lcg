from . import *

# Heavy Lifting (2e exemplaire) — custom « Rainy »
# Hero Action (thwart): For each [physical] resource you used to pay for this
#   card, your hero gets +1 ATK until the end of the round. Remove threat from
#   a scheme equal to your ATK.
#
# L'ordre imprime compte : le bonus d'ATK est pose AVANT le retrait de menace,
# et c'est l'ATK ainsi augmentee qui fixe la quantite retiree. Une carte payee
# avec deux [physical] retire donc ATK+2 menaces, pas ATK.

def GetAbilities() -> Sequence['Ability']:

    def heavy_lifting(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        joueur = effect.GetInitiator()
        heros = joueur.GetHero()
        if heros is None:
            return

        bonus = effect.GetPaidResources().GetColor("R")
        if bonus > 0:
            heros.GainUntilRoundEnd(effect, attack=bonus)

        cibles = effect.targets
        if cibles:
            this.RemoveThreatFromSchemes(cibles, heros.attack, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            heavy_lifting,
        ).SetPlay(hero_form_only=True)
        .SetLabel('thwart')
        .SetTarget(Scheme2, range=(1, 1)),
    ]
