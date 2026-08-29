from . import *

# * Dazzler
# Rehearsal — Hero Action: Place 1 sound counter on a SONG in the Setlist
#   without a sound counter on it -> resolve the "Showtime!" effect on that
#   SONG. (Limit once per phase.)
#
# Le compteur `sound` n'est pas decoratif : il est la MEMOIRE de ce qui a deja
# ete repete. La capacite ne vise que les SONG qui n'en portent pas, donc une
# Setlist pleine autorise au plus quatre repetitions, et Sound Collector Suit
# (dz016) est la seule carte qui puisse en effacer une pour rejouer un titre.


def GetAbilities() -> Sequence['Ability']:

    def rehearsal(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        candidats = SongsSansCompteur(effect)
        if not candidats:
            return

        chanson = joueur.AskChooseOneText(candidats) if len(candidats) > 1 \
            else candidats[0]
        if chanson is None:
            return

        MarquerRepete(effect, chanson)
        ResoudreShowtime([chanson], joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            rehearsal,
            conditions=[
                # Sans SONG repetable, l'option ne doit meme pas etre offerte :
                # sinon le pilote la reprend en boucle sans que rien ne change
                # (piege wd165, blocage du scenario Underling).
                lambda effect, message: len(SongsSansCompteur(effect)) > 0,
            ],
        ).SetName("Rehearsal")
        .LimitOncePerPhase(),
    ]
