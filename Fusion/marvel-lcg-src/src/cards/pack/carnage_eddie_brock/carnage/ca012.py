from . import *

# * Chomp : EVENEMENT (ATTACK. SUPERPOWER.), cout 3, [wild]. Classe Hero.
# Hero Action (attack): Deal 8 damage to an enemy. This attack gains piercing. If this attack defeats that enemy, ready Carnage.
#
# CARTES DE REFERENCE
#  - Evenement d'attaque a libelle, degats fixes + mot-cle d'attaque : `uw004` (Deranged Burst) : `this.DealDamage(effect.targets, N, effect, property=AttackProperty(piercing=True))` + `.SetPlay().SetLabel('attack').SetTarget(Enemy)`.
#  - « If this attack defeats that enemy → » : `th009` (Sock 'Em) / `sn002` : `if_this_attack_defeats=fn`, appelee PAR UNITE VAINCUE par CETTE attaque ; redressement : `Faces.ReadyAll` (`an001a`).
#
# TEXTE CONTRE CODE
#  « Hero Action (attack) » : `HeroAction` + `SetLabel('attack')`. « Deal 8 damage to AN enemy » : une cible, vilain ou sbire (`Enemy`). « This attack GAINS PIERCING » : `AttackProperty(piercing=True)` (fiche mots-cles/piercing.md : defausse un statut tough au lieu d'etre absorbe).
#  « IF THIS ATTACK defeats THAT enemy » : defaite par CETTE attaque seulement (`if_this_attack_defeats`). « ready CARNAGE » : l'identite du joueur (face heros, seule forme ou l'evenement se joue). Chiffres : cout 3, 8 degats.


def GetAbilities() -> Sequence['Ability']:

    def chomp(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)

        def si_l_ennemi_tombe(unit: 'Unit2') -> None:
            Unused(unit)
            if joueur is not None:
                Faces.ReadyAll([joueur.GetIdentity()], effect)

        this.DealDamage(
            effect.targets,
            8,
            effect,
            property=AttackProperty(piercing=True),
            if_this_attack_defeats=si_l_ennemi_tombe,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chomp,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
