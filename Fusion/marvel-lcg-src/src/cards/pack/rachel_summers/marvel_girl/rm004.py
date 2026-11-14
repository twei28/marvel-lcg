from . import *

# Black Hole — EVENEMENT, cout 3 (mental), PSIONIC.
# Hero Action: Stun and confuse a minion and a villain. Deal 1 damage to the villain and each minion engaged with you.
#
# CARTES DE REFERENCE : `04036` Pheromones (`Faces.GiveStatus(.., "Stunned")` + `"Confused"`), `18020` Hit and Run (deux cibles :
# `SetTarget` / `SetTarget2`), `us010` (« each minion engaged with you » : `joueur.engaged_minions`).
#
# MOTS-PIEGES : « a minion AND a villain » = DEUX cibles obligatoires (sans sbire en jeu la carte n'est pas jouable) ; les
# degats vont au vilain et a CHAQUE sbire engage avec VOUS (pas seulement celui qu'on a etourdi) : une liste sans doublon.
def GetAbilities() -> Sequence['Ability']:
    def black_hole(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        initiator = effect.GetInitiator()
        sbires = list(effect.targets)
        vilains = list(effect.targets2)
        cibles = sbires + vilains
        Faces.GiveStatus(cibles, "Stunned", effect)
        Faces.GiveStatus(cibles, "Confused", effect)
        victimes: List['CardFace'] = list(vilains)
        for sbire in initiator.engaged_minions.Get():
            if sbire not in victimes:
                victimes.append(sbire)
        this.DealDamage(victimes, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            black_hole,
        ).SetPlay().SetLabel()
        .SetTarget(Minion)
        .SetTarget2(Villain),
    ]
