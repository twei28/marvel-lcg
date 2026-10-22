from . import *

# Combo Move — EVENEMENT 1 [energy], aspect Aggression (TMNT Reskins, Inkwire). ATTACK.
# Hero Action (attack): Deal 2 damage among enemies in play (3 damage instead if your identity has the
#   MARTIAL ARTIST trait).
#
# CARTES DE REFERENCE
#  - `sk041` (Lyja) « Deal 4 damage among enemies in play » : `SetTarget(Enemy, range=(N, N),
#    repeat_rules="Any")` + 1 degat par selection : TOUT le montant est inflige (pas « jusqu'a »).
#  - `vp003` Talk About Armed Assault / `13006` Wasp Sting : deux capacites mutuellement exclusives, car
#    `range` est fige a la construction (condition lue au jeu).
# TEXTE CONTRE CODE
#  ⚠ « among enemies » : reparti au choix, le meme ennemi peut etre choisi plusieurs fois.
#  ⚠ « your IDENTITY has the MARTIAL ARTIST trait » : identite courante, lue au jeu de la carte.


def IdentiteArtisteMartial(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
    Unused(message)
    joueur = effect.GetInitiator()
    return joueur is not None and joueur.GetIdentity().HasTrait("MARTIAL ARTIST")


def IdentiteSansArtisteMartial(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
    return not IdentiteArtisteMartial(effect, message)


def GetAbilities() -> Sequence['Ability']:

    def combo(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            combo,
            conditions=[IdentiteSansArtisteMartial],
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, range=(2, 2), repeat_rules="Any"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            combo,
            conditions=[IdentiteArtisteMartial],
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, range=(3, 3), repeat_rules="Any"),
    ]
