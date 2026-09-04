from . import *

# Multiple 'Porting — EVENEMENT, cout 2, [energy]. SUPERPOWER. THWART.
# Hero Action (thwart): Remove 3 threat from a scheme. Remove 2 additional
#   threat from that scheme for each [[PORTAL]] upgrade attached to it.
#
# Jumelle de bk005 cote menace. ⚠ `RemoveThreatFromSchemes` et NON
# `RemoveThreat`, qui n'existe pas — leçon du pack doctor_druid, ou l'appel
# fautif levait une exception AVALEE par le moteur et sortie seulement par
# l'autoplay.


def GetAbilities() -> Sequence['Ability']:

    def portage_multiple(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        cibles = list(effect.targets)
        if not cibles:
            return
        montant = 3 + 2 * len(PortailsSur(effect, cibles[0]))
        this.RemoveThreatFromSchemes(cibles, montant, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            portage_multiple,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
