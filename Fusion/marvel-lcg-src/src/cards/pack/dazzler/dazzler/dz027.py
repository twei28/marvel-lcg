from . import *

# Song of Protection
# SONG.
# Max 2 per deck.
# Hero Interrupt (defense): When a friendly character would take any amount of
#   damage, reduce that damage by 1 for each SONG card in your discard pile
#   (to a maximum of 4).
#
# « a FRIENDLY CHARACTER », pas seulement toi : la carte couvre aussi les
# allies, d'ou « YouControlCharacter » et non « You ».
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
            "YouControlCharacter",
            chant_de_protection,
        ).SetPlay().SetLabel('defense'),
    ]
