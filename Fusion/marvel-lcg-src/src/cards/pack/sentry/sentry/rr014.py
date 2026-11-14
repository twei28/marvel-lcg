from . import *

# Unrivaled Might : EVENEMENT (ATTACK. SPLIT. SUPERPOWER.), cout 3, [physical]. Classe Hero. (x2)
# Hero Action (attack): Deal 8 damage to an enemy (10 damage instead if there are 3+ balance counters in play). This attack gains piercing.
# Special: The Void attacks the villain and you. You cannot defend against this attack. This attack gains piercing.
#
# CARTES DE REFERENCE
#  - `ca012` (Chomp) : `this.DealDamage(effect.targets, N, effect, property=AttackProperty(piercing=True))` + `.SetPlay().SetLabel('attack').SetTarget(Enemy)`.
#  - Special : `void.AttackCharacter(villain, effect, property=AttackProperty(piercing=True))` puis `void.DoAttackYou(joueur, effect, property=AttackProperty(piercing=True, other_characters_cannot_defend=True))` ; `.NoOutOfPlayLimit()`.
#
# TEXTE CONTRE CODE
#  « 10 damage INSTEAD » : 10 a 3+ compteurs en jeu (somme), sinon 8. « The Void attacks the villain AND you » : DEUX attaques (le vilain, puis le joueur). « You CANNOT DEFEND » : aucun autre personnage ne peut defendre
#  l'attaque contre le joueur (`other_characters_cannot_defend`) ; l'identite subit l'attaque. « piercing » : sur les deux. Chiffres : cout 3, 8 ou 10.


def GetAbilities() -> Sequence['Ability']:

    def unrivaled_might(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        this = effect.this.CastTo(Event)
        degats = 10 if EquilibreEnJeu(effect) >= 3 else 8
        this.DealDamage(effect.targets, degats, effect, property=AttackProperty(piercing=True))

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        void = VoidEnJeu(effect)
        joueur = JoueurDeCetteCarte(effect) or JoueurSentry(effect)
        if void is None or joueur is None:
            return
        vilain = Worlds.FindCardOnField(effect, card_type=Villain)
        if vilain is not None:
            void.CastTo(Enemy).AttackCharacter(vilain, effect, property=AttackProperty(piercing=True))
        void.CastTo(Enemy).DoAttackYou(joueur, effect, property=AttackProperty(piercing=True, other_characters_cannot_defend=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, unrivaled_might).SetPlay().SetLabel('attack').SetTarget(Enemy),
        AbilityFactory.WhenResolveSpecialAbility("This", special).NoOutOfPlayLimit(),
    ]
