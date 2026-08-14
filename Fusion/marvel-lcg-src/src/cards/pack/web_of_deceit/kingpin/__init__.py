from cards.pack.web_of_deceit import *

# Le scenario tourne autour de deux choses que le moteur ne connaissait pas :
#
#   * les manigances CORROMPUES, faites de cartes du deck des JOUEURS ;
#   * « Pursued by the Past », la carte de Standard III que tout le set nourrit
#     en compteurs `pursuit`.


def PoserUneManiganceCorrompue(joueur: 'Player', effect: 'Effect') -> 'CardFace|None':
    """« Put the top card of your deck into play facedown as a CORRUPT side
    scheme. »

    ⚠ ECART, ecrit. Le jeu physique retourne LA carte du dessus du deck du
    joueur et s'en sert comme d'une manigance : la carte est a la fois le cout
    et l'obstacle. Le moteur ne sait pas faire d'une carte joueur une manigance
    de rencontre — `TreatAsMinion` echange bien une face contre une autre, mais
    il est ecrit pour les allies et les heros, et la manigance qui en sortirait
    ne saurait ni entrer dans la bonne zone ni revenir a son proprietaire.

    On paie donc le cout ET on pose l'obstacle, en deux gestes : la carte du
    dessus du deck part a la defausse, et un exemplaire de `wd106` — le patron
    « Corrupt », mis de cote a la mise en place — entre en jeu a sa place. Le
    joueur perd la meme carte, la table porte la meme manigance ; seule
    l'identite de la carte posee change, et elle etait face cachee de toute
    facon.
    """
    joueur.DiscardDeckTopCards(1, effect)

    patron = Search.SearchForCard(
        effect,
        joueur,
        include_set_aside=True,
        card_ids=["wd106"],
    )
    if patron:
        patron.PutIntoPlay(joueur, effect)
    return patron


def PursuedByThePast(effect: 'Effect') -> 'CardFace|None':
    """La carte de Standard III que tout le set Kingpin nourrit."""
    return Worlds.FindCardOnField(effect, name="Pursued by the Past")


def CompteursDePoursuite(effect: 'Effect', combien: int) -> None:
    cible = PursuedByThePast(effect)
    if cible:
        Faces.PlaceCountersOn([cible], combien, 'pursuit', effect)


def NombreDeCompteursDePoursuite(effect: 'Effect') -> int:
    cible = PursuedByThePast(effect)
    return cible.CastTo(CanPlaceCounter).GetCounters('pursuit') if cible else 0
