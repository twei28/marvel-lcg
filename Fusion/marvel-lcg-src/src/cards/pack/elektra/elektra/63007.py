from . import *

# Killer Blow — EVENEMENT, cout 2, [energy]. ATTACK. x2 (Elektra 4-5/15).
# Hero Action (attack): Deal up to 5 damage to an enemy. If this attack defeats that enemy, shuffle the top card of the
# NINJA deck into the encounter deck.
#
# CARTES DE REFERENCE
#  - « Deal N damage to an enemy ... if this attack defeats that enemy » : `16005` Root Stomp (`this.DealDamage(cibles, n,
#    effect, if_this_attack_defeats=fn)`, `SetPlay().SetLabel('attack').SetTarget(Enemy)`).
#  - « up to N » CHOISI par le joueur, zero compris : `venus/tv003` Arc Nova (`joueur.DeclareNumber(0, N)`).
#
# TEXTE CONTRE CODE
#  ⚠ « UP TO 5 » : le joueur CHOISIT un nombre de 0 a 5 (regle des « up to », decision « regle officielle d'abord »). 0 = rien
#    n'est inflige et rien n'est vaincu : pas de melange.
#  ⚠ « If THIS ATTACK defeats THAT enemy » : le melange ne part que si l'ennemi vise est vaincu par ces degats (`if_this_attack_defeats`).
#  ⚠ « the top card of the NINJA deck » : une seule carte ; paquet Ninja vide = rien.
#  Chiffres : cout 2, 5 degats maximum, 1 carte Ninja.


def GetAbilities() -> Sequence['Ability']:

    def killer_blow(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        degats = joueur.DeclareNumber(0, 5)
        if degats <= 0:
            return

        def si_vaincu(unit: 'Unit2') -> None:
            Unused(unit)
            MelangerDessusNinja(joueur, effect)

        this.DealDamage(effect.targets, degats, effect, if_this_attack_defeats=si_vaincu)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            killer_blow,
        ).SetPlay().SetLabel('attack').SetTarget(Enemy),
    ]
