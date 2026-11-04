from . import *

# Energy Flare : EVENEMENT (SPLIT. SUPERPOWER.), cout 3, [energy]. Classe Hero.
# Hero Action: Deal 3 damage to each enemy in play (this event gains overkill if there are 3+ balance counters in play).
# Special: The Void attacks each character you control and each enemy in play. This attack gains overkill.
#
# CARTES DE REFERENCE
#  - « Deal N damage to each enemy » : `this.DealDamage(ennemis, 3, effect, property=AttackProperty(overkill=..))` (`ca012`, `.SetPlay()`).
#  - Special : le Void attaque : `void.CastTo(Enemy).AttackCharacter(cible, effect, overkill=True)` (RECETTES §16.1) ; `.NoOutOfPlayLimit()`.
#
# TEXTE CONTRE CODE
#  « each enemy IN PLAY » : le Void compris pour les degats de l'evenement. « gains overkill if 3+ balance counters IN PLAY » : somme sur toutes les cartes. Special : « each character you control AND each
#  enemy » : chaque personnage du joueur (identite, allies) puis chaque AUTRE ennemi (le Void ne s'attaque pas lui-meme), une attaque chacun. Chiffres : cout 3, 3 degats.


def GetAbilities() -> Sequence['Ability']:

    def energy_flare(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        this = effect.this.CastTo(Event)
        ennemis = Worlds.FindCardsOnField(effect, card_type=Enemy)
        this.DealDamage(ennemis, 3, effect, property=AttackProperty(overkill=EquilibreEnJeu(effect) >= 3))

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        void = VoidEnJeu(effect)
        joueur = JoueurDeCetteCarte(effect) or JoueurSentry(effect)
        if void is None or joueur is None:
            return
        for cible in [*PersonnagesDuJoueur(joueur), *AutresEnnemis(effect)]:
            if cible.IsInPlay():
                void.CastTo(Enemy).AttackCharacter(cible, effect, overkill=True)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, energy_flare).SetPlay().SetHasNoTargetEffect(),
        AbilityFactory.WhenResolveSpecialAbility("This", special).NoOutOfPlayLimit(),
    ]
