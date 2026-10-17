from . import *

# Tsujigiri — EVENEMENT ATTACK, classe Bushido (Inkwire, TMNT Shinobi). Cout 2, [physical].
# Hero Action (attack): Deal damage to an enemy equal to your ATK. If this attack defeats that enemy, you may place 1 samurai
#   counter on an OATH upgrade you control.
# « Time to test out my new blades. » —Leonardo
#
# Mots-cles (fiches lues AVANT le code) : samurai counter / OATH (samurai-counter.md).
#
# Cartes de reference :
#  - « Deal damage to an enemy equal to your ATK » : `valk/25018` Quick Strike (`initiator.GetHero().attack`,
#    `WhenInYourPlayTurn(HeroAction).SetPlay().SetLabel('attack').SetTarget(Enemy)`) ;
#  - « If this attack defeats that enemy, <suite> » : `nova/28014` One by One (`this.DealDamage(cibles, n, effect,
#    if_this_attack_defeats=action)`, rappelee PAR unite vaincue) ;
#  - « you may place 1 samurai counter on an OATH upgrade you control » : `PlacerUnCompteurSamurai(..., optionnel=True)` (helper
#    du pack : `MayChooseOneAbility` + cible choisie).
#
# TEXTE CONTRE CODE
#  ⚠ « equal to YOUR ATK » : l'ATQ COURANT du heros (bonus compris, Courage +1 ATQ), lu a la resolution, pas l'ATQ imprime.
#  ⚠ « (attack) » : etiquette `attack` (alimente Sonne / Desoriente) ; le trait ATTACK de la carte est dans `traits`.
#  ⚠ « If THIS ATTACK defeats THAT enemy » : seulement si les degats de CETTE carte vainquent la cible choisie ; un ennemi qui
#    survit ne donne rien.
#  ⚠ « you MAY place » : facultatif ; « 1 » compteur, sur une amelioration OATH SOUS SON CONTROLE (choisie).


def GetAbilities() -> Sequence['Ability']:

    def tsujigiri(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()

        def vaincu(unite: 'Unit2') -> None:
            Unused(unite)
            PlacerUnCompteurSamurai(effect, joueur, optionnel=True)

        degats = joueur.GetHero().attack
        this.DealDamage(effect.targets, degats, effect, if_this_attack_defeats=vaincu)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tsujigiri,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
