from . import *

# Song of Aggression
# ATTACK. SONG.
# Max 2 per deck.
# Hero Action (attack): Deal 1 damage to an enemy for each SONG card in your
#   discard pile (to a maximum of 4).
#
# Carte D'ASPECT : elle porte le trait [[SONG]], donc Live Concert la rattrape
# et elle compte pour les autres, mais elle n'a PAS de « Showtime! ». La fiche
# de regles le dit : on ne resout le Showtime! que « on each card THAT HAS ONE ».
#
# Elle se compte elle-meme : quand son effet se resout, elle n'est pas encore a
# la defausse. C'est le texte, on ne l'aide pas.


def GetAbilities() -> Sequence['Ability']:

    def chant_de_guerre(effect: 'Effect',
                        message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        valeur = SongsDansLaDefausseBornee(effect)
        if valeur > 0:
            this.DealDamage(effect.targets, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chant_de_guerre,
        ).SetPlay().SetLabel("attack")
        .SetTarget(Enemy),
    ]
