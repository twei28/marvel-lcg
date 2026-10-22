from . import *

# Demoralize — EVENEMENT 0 [mental], aspect Protection (TMNT Aspects, Inkwire). TACTIC.
# Hero Action: Choose an enemy. It attacks you. Confuse that enemy.
#
# NOUVELLE.
#
# CARTES DE REFERENCE
#  - `10015` Toe to Toe : « Choose an enemy. It attacks you » = `.SetTarget(Enemy)` puis
#    `target.DoAttackYou(initiator, effect)` (sbire OU vilain).
#  - `56048` Taunt : evenement TACTIC qui fait attaquer, sans libelle d'attaque (`SetLabel()` vide).
#  - « Confuse that enemy » : `Faces.GiveStatus([cible], "Confused", effect)` (comme `50052` Prism Dust).
#
# TEXTE CONTRE CODE
#  ⚠ « Hero Action » SANS (attack) : pas de libelle d'attaque (le heros n'attaque pas, il est attaque).
#  ⚠ « It attacks YOU » : le joueur qui joue la carte (`GetInitiator`).
#  ⚠ « Confuse THAT enemy » : la meme carte que celle choisie, APRES l'attaque (ordre imprime).
#  ⚠ Aucun « if » : le Desoriente est pose meme si l'attaque n'a pas eu lieu (ennemi Sonne).


def GetAbilities() -> Sequence['Ability']:

    def demoralize(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        initiator = effect.GetInitiator()
        for target in effect.targets:
            ennemi = target.CastTo(Minion | Villain)
            ennemi.DoAttackYou(initiator, effect)
            if ennemi.IsInPlay():
                Faces.GiveStatus([ennemi], "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            demoralize
        ).SetPlay().SetLabel().SetTarget(Enemy)
    ]
