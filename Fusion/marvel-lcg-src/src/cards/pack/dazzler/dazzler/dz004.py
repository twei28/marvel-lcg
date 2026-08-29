from . import *

# "Beautiful Dreamer"
# SONG. THWART.
# Hero Action (thwart): Remove 3 threat from a scheme. If this removes the last
#   threat from that scheme, you may remove 2 threat from another scheme.
# Showtime!: Remove 2 threat from a scheme.
#
# « If this removes the LAST threat » : on ne peut pas le savoir a l'avance,
# une machination peut avoir moins de 3 menaces comme en avoir dix. On lit donc
# la menace APRES le retrait, et le bonus ne part que si elle est tombee a
# zero — et seulement pour une AUTRE machination (`exclude`).


def GetAbilities() -> Sequence['Ability']:

    def belle_reveuse(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        cibles = list(effect.targets)
        if not cibles:
            return
        premiere = cibles[0]

        this.RemoveThreatFromSchemes([premiere], 3, effect)

        if premiere.threat > 0:
            return

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        autres = [s for s in Worlds.FindCardsOnField(effect, card_type=Scheme2)
                  if s is not premiere and s.threat > 0]
        if not autres:
            return

        def retirer(targets: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(targets, 2, effect)

        # « YOU MAY » : le choix doit rester offert, pas force.
        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility("Remove 2 threat", retirer)
            .SetTarget(Scheme2, exclude=[premiere]),
        )

    def showtime(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Event)
        # Le joueur CHOISIT la cible : `ResolveAbility` prendrait sinon la
        # premiere cible legale sans rien demander (cf. CiblesShowtime).
        this.RemoveThreatFromSchemes(CiblesShowtime(effect), 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            belle_reveuse,
        ).SetPlay().SetLabel("thwart")
        .SetTarget(Scheme2),
        Showtime(showtime).SetTarget(Scheme2, range=(0, 1)),
    ]
