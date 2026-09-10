from . import *

# Psionic Web Blast — EVENEMENT, cout 0, RES [mental], x2.
# ATTACK. PSIONIC. SUPERPOWER.
# Hero Action (attack): Remove X psionic web counters from Spider-Woman ->
#   deal X damage to an enemy.
#
# ⚠ LA JUMELLE EXACTE DE `sw006` Psi-Web Trap : voir son en-tete pour la
# lecture commune de « X ». Ici l'ATTAQUE au lieu du contre.


def GetAbilities() -> Sequence['Ability']:

    def rafale_de_toile(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        cibles = [c for c in effect.targets if c is not None]
        if joueur is None or not cibles:
            return
        combien = DemanderCombienDeToiles(joueur, effect)
        retire = RetirerDesToiles(joueur, combien, effect)
        if retire > 0:
            this.DealDamage(cibles, retire, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            rafale_de_toile,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
