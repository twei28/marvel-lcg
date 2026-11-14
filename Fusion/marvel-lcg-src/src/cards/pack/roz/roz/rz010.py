from . import *

# Negotiator — EVENEMENT, cout 2, [mental] (x2 dans le deck). SKILL.
# Hero Action: Remove 2 threat from a scheme. Resolve the "Special" ability on a [[WAKANDA]] upgrade.
#   Resolve the "Special" ability on a [[WAKANDA]] upgrade.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - Hero Action d'evenement : `01022` Ground Stomp ; menace : `01023` Legal Practice
#    (`this.RemoveThreatFromSchemes(effect.targets, N, effect)` + `SetTarget(Scheme2)`).
#  - deux resolutions de Special : `rz009` (meme helper `ResoudreSpecialSurAmelioration`), `51025`.
#
# MOTS-PIEGES
#  - « Remove 2 threat from A scheme » : une seule manigance. Pas de `(thwart)` imprime : `SetLabel()` sans
#    etiquette (la carte n'est pas un contre de base).
#  - deux resolutions independantes, la meme amelioration peut servir deux fois.
def GetAbilities() -> Sequence['Ability']:

    def negociation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
        ResoudreSpecialSurAmelioration(effect, joueur)
        ResoudreSpecialSurAmelioration(effect, joueur)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            negociation,
        ).SetPlay().SetLabel()
        .SetTarget(Scheme2),
    ]
