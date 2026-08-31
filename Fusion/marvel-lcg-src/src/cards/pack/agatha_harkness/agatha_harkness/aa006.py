from . import *

# Soul Harvest — evenement. ATTACK. SPELL. Cout 3. x2
# Hero Action (attack): Deal 5 damage to an enemy. Heal 2 damage from Agatha
#   Harkness. Discard the top card of your deck. If that card's printed
#   resources has:
#   [wild] or [physical] - Stun that enemy.
#   [mental] or [energy] - Confuse that enemy.
#
# Cartes de reference (RECETTES) : 09004 Magic Blast (degats + defausse du
# dessus + branche par couleur), 01050 * Hulk pour la lecture
# (`DiscardDeckTopCard` + `GetPrintedResources`).
#
# ⚠ « THAT enemy » partout : le statut vise l'ennemi frappe. S'il est mort
# des 5 degats, plus personne a statuer — la branche s'eteint (meme logique
# que les vivantes de aa005). Une carte double icone (« GB » d'aa007) peut
# remplir LES DEUX conditions : l'ordre imprime resout stun puis confuse.

def GetAbilities() -> Sequence['Ability']:

    def soul_harvest(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        cibles = [t for t in effect.targets if t is not None]
        this.DealDamage(cibles, 5, effect)

        hero = initiator.GetHero()
        if hero is not None:
            this.HealthUnits([hero], 2, effect)

        face = initiator.DiscardDeckTopCard(effect)
        if face is None:
            return
        res = FacesCounter.GetPrintedResources([face])
        vivantes = [t for t in cibles if t.IsInPlay()]
        if not vivantes:
            return
        if res.g > 0 or res.r > 0:
            Faces.GiveStatus(vivantes, "Stunned", effect)
        if res.b > 0 or res.y > 0:
            Faces.GiveStatus(vivantes, "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            soul_harvest
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
