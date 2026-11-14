from . import *

# Song of Protection
# SONG.
# Max 2 per deck.
# Hero Interrupt (defense): When a friendly character would take any amount of
#   damage, reduce that damage by 1 for each SONG card in your discard pile
#   (to a maximum of 4).
#
# « a FRIENDLY CHARACTER » : tout personnage du cote des joueurs, identites
# et allies de TOUS les joueurs : `Friend` (modeles 40012, 53037). Jusqu'au
# 20/10/2026 le module prenait « YouControlCharacter », qui excluait les
# personnages des autres joueurs (backlog 12, cas a deux joueurs).
#
# `ReduceDamage`, pas `PreventDamage` : le texte reduit d'un montant, il
# n'annule pas.


def GetAbilities() -> Sequence['Ability']:

    def chant_de_protection(effect: 'Effect',
                            message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        valeur = SongsDansLaDefausseBornee(effect)
        if valeur > 0:
            message.ReduceDamage(valeur, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            Friend,
            chant_de_protection,
        ).SetPlay().SetLabel('defense'),
    ]
