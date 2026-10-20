from . import *

# Live Concert
# Permanent. Setup.
# Response: After you resolve a SONG event attach it here, placed in a row to
#   the side of this card (to a maximum of 4). Once placed here, it cannot be
#   swapped with a new card. This is the Setlist.
# Hero Action: Flip this card to its Showtime! side and reveal it.
#
# La Setlist est la `PlaceCardArea` de cette amelioration, la meme zone que
# celle d'Armed to the Teeth (44009) ou de Multiverse Shenanigans (dt075).
#
# « After you RESOLVE a SONG event » : la fenetre est `AfterPlayerPlayedCard`,
# qui arrive une fois l'evenement resolu, donc quand il est deja a la defausse.
# On l'en sort avec `PlaceCardHere`, exactement comme 44009 y range la carte
# que `Search.Collection` vient de fabriquer dans cette meme defausse.
#
# « it cannot be swapped with a new card » ne demande aucun code : rien dans ce
# pack ne retire une carte de la Setlist autrement qu'en la defaussant en bloc
# (Showtime!, Karaoke Night, Stealing Sound). La clause interdit un echange qui
# n'existe pas.


def GetAbilities() -> Sequence['Ability']:

    def ranger_dans_la_setlist(effect: 'Effect',
                               message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        chanson = message.played_face
        if chanson is None:
            return
        # FACE VISIBLE : la Setlist s'etale « in a row to the side », et il faut
        # pouvoir lire les « Showtime! » pour les resoudre. C'est Lightbringr
        # (dz014) qui range face cachee, pas Live Concert.
        this.PlaceCardHere([chanson], True, effect)
        # Tribute (dz031) entre dans la Setlist EN TANT QUE COPIE (decision Q4
        # du backlog 12, 20/10/2026) : elle est redevenue Tribute en passant par
        # la defausse (`CheckIfCanDiscard`), on lui rend sa face de copie.
        paper = getattr(chanson.card, "tribute_copie", None)
        if paper is not None:
            chanson.card.tribute_copie = None
            DevenirCopie(chanson.card.face, paper, effect)
            chanson.card.tribute_copie = None

    def lever_le_rideau(effect: 'Effect',
                        message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        joueur = effect.GetInitiator()
        # Modele Psi-Knife/Psi-Katana (41002a/b) : la cible est « This » et
        # `FlipAllTo` retourne la carte sur son autre face.
        Faces.FlipAllTo(effect.targets, None, effect)
        # « ...and REVEAL it ». Le moteur ne revele de lui-meme une carte
        # retournee en jeu que si c'est une carte de rencontre, une manigance
        # principale ou un vilain (game/card/face/model/face_on_event.py:278,
        # `FaceOnEvent.OnAfterFlip`). Une amelioration de joueur n'y entre pas :
        # sans cet appel, le « When Revealed » de Showtime! ne partait jamais.
        for face in effect.targets:
            montree = face.card.face
            if montree is not None and montree.IsInPlay():
                montree.Reveal(joueur, effect, is_by_flipping=True)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(card_type=Event, trait=TRAIT_SONG),
            ranger_dans_la_setlist,
            conditions=[
                lambda effect, message: SetlistALaPlace(effect),
            ],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            lever_le_rideau,
            conditions=[
                # « You cannot [...] use the 'Hero Action' on Live Concert »
                # tant que Performance Anxiety (dz019) est posee chez toi.
                lambda effect, message: not AngoisseEnJeu(effect),
                # Setlist vide : retourner, ne rien resoudre, ne rien defausser,
                # retourner de nouveau ne change RIEN a la partie. Comme
                # Rehearsal (dz001a) et Karaoke Night (dz035), l'action n'est
                # alors pas offerte (piege wd165). Constate a l'autoplay du
                # 20/10/2026 (backlog 12) : 6 parties sur 8 bloquees, le pilote
                # reprenant sans fin cette Hero Action sans effet.
                lambda effect, message: len(Setlist(effect)) > 0,
            ],
        ).SetTarget("This"),
    ]
