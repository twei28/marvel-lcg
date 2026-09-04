from . import *

# Lose Footing — EVENEMENT, cout 2, [energy]. ATTACK. SUPERPOWER.
# Hero Action (attack): Deal 4 damage to an enemy. Deal 2 additional damage to
#   that enemy for each [[PORTAL]] upgrade attached to it.
#
# TEXTE CONTRE CODE
#  « to THAT enemy for each PORTAL attached TO IT » -> les portails de LA
#    CIBLE, pas ceux du terrain. Mot-piege « that <nom> » du PROCESSUS-CARTE.
#  Un seul jet de degats (4 + 2N) et non deux : le Deferlement et la Riposte
#  ne se declencheraient pas de la meme facon sur deux jets separes.


def GetAbilities() -> Sequence['Ability']:

    def perdre_pied(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        cibles = list(effect.targets)
        if not cibles:
            return
        montant = 4 + 2 * len(PortailsSur(effect, cibles[0]))
        this.DealDamage(cibles, montant, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            perdre_pied,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
