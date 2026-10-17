from . import *

# Stiff Jab — EVENEMENT 1 [physical], Taijutsu (TMNT Shinobi, Inkwire). ATTACK.
# Hero Action (attack): Deal 2 damage to an enemy. If you paid for this card with an ATTACK event, you may daze
#   that enemy.
#
# Mots-cles (fiches lues AVANT le code) : Dazed / « daze » (dazed.md) ; Shinobi (shinobi.md).
#
# Cartes de reference :
#  - `jennika/tj004` Decisive Strike : meme montage « deal N damage, then if paid with an ATTACK event, <statut> that
#    enemy » (`PayeAvecUnEvenement(effect, "ATTACK")`, `RECETTES-MOTEUR` §13) ;
#  - `leonardo/tl006` Yo Ko Giri : « you MAY ... » = `ChooseAbilities` a deux branches dont « Decline » ;
#  - « daze X » : `ShinobiDaze(effect, [ennemi])` (`tx016` Wrapped Up).
#
# TEXTE CONTRE CODE
#  ⚠ « paid ... with an ATTACK EVENT » : un AUTRE evenement ATTACK, depense comme ressource (pas une ressource
#    ordinaire, pas un evenement DEFENSE/THWART).
#  ⚠ « you MAY daze » : optionnel (branche « Decline »).
#  ⚠ « Deal 2 damage » PUIS « daze THAT enemy » : le meme ennemi, encore en jeu apres les degats.
#  ⚠ Coquille du scan : « MC Custom Content By: Inkwire » au lieu de « TMNT Shinobi By: Inkwire » (question Q-T1).


def GetAbilities() -> Sequence['Ability']:

    def stiff_jab(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        this.DealDamage(effect.targets, 2, effect)

        if joueur is None or not PayeAvecUnEvenement(effect, "ATTACK"):
            return
        vivants = [e for e in effect.targets if not e.IsDefeated()]
        if not vivants:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Daze that enemy",
                lambda cibles: ShinobiDaze(effect, vivants),
            ),
            AbilityFactory.ForChoiceAbility(
                "Decline",
                lambda cibles: None,
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            stiff_jab,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
