from . import *

# "In the Darkest Light"
# SONG.
# Hero Action: Deal 2 damage to each enemy.
# Showtime!: Stun a non-ELITE enemy.
#
# « each enemy » : pas de selection, on prend tous les ennemis en jeu.


def GetAbilities() -> Sequence['Ability']:

    def dans_la_lumiere(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        ennemis = Worlds.FindCardsOnField(effect, card_type=Enemy)
        if ennemis:
            this.DealDamage(list(ennemis), 2, effect)

    def showtime(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        # Le joueur CHOISIT la cible : `ResolveAbility` prendrait sinon la
        # premiere cible legale sans rien demander (cf. CiblesShowtime).
        Faces.GiveStatus(CiblesShowtime(effect), "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            dans_la_lumiere,
        ).SetPlay().SetLabel(),
        Showtime(showtime).SetTarget(Enemy, non_trait="ELITE",
                                    canbe_stunned=True, range=(0, 1)),
    ]
