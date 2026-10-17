from . import *

# Cut-and-Run — EVENEMENT 2 [physical], Ninjutsu (TMNT Shinobi, Inkwire). ATTACK. TACTIC.
# Hero Action (attack): Deal 4 damage to an enemy. If this attack defeats an enemy, cloak your hero.
# « This is getting out of control. You can count me out. » —Ronin
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloak / Cloaked (cloak.md, cloaked.md).
#
# Cartes de reference :
#  - `35018` Precision Strike : « Deal 2 damage to an enemy. If this attack defeats that enemy, heal 2 damage from your
#    hero » = `this.DealDamage(cibles, N, effect)` puis `cibles[0].IsDefeated()` ;
#  - `up023` Lookout : « cloak your hero » (`Faces.GiveStatus`, ici `ShinobiCloak`).
#
# TEXTE CONTRE CODE
#  ⚠ « 4 damage to AN ENEMY » : sbire OU vilain ; « If this attack DEFEATS an enemy » : la cible est vaincue par CES
#    degats (un vilain qui perd sa phase n'est pas « vaincu » : seul le dernier PV compte), pas d'effet sinon.
#  ⚠ « cloak YOUR HERO » : sur le HEROS ; un heros deja camoufle n'en recoit pas une seconde.


def GetAbilities() -> Sequence['Ability']:

    def cut_and_run(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        cible = effect.targets[0]
        this.DealDamage(effect.targets, 4, effect)
        if cible.IsDefeated() and joueur.IsHero():
            ShinobiCloak(effect, joueur.GetHero())

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            cut_and_run,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
