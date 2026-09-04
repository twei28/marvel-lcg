from cards.pack import *

# ===========================================================================
# Helpers partages du set « Doctor Druid Nemesis » (Nekra).
#
# Le set nemesis ne frappe pas les points de vie, il frappe LA MAIN : dr012 et
# dr013 defaussent des cartes « identity-specific », c'est-a-dire exactement
# la ressource sur laquelle tout le kit du heros est bati (voir le
# `__init__.py` du set « Doctor Druid »).
# ===========================================================================

NOM_NEKRA = "Nekra"
COMPTEUR_HAINE: 'CardFace.COUNTER' = 'hate'
HAINE_MAXIMUM = 5


def ChercherNekra(effect: 'Effect') -> 'CardFace|None':
    """« Search the encounter deck and discard pile for Nekra. »

    ⚠ DEUX ZONES, comme le mot-cle maison `summon` du pack yondu : le deck de
    rencontre ET sa defausse. `Search.SearchForCards` expose les deux, la
    fouiller a moitie rendrait dr012 et dr014 inertes des que Nekra a ete
    vaincue une premiere fois — or c'est precisement le cas que ces deux
    cartes existent pour couvrir (« Resurrection of Nekra »).
    """
    joueur = effect.GetInitiator() if Player.IsType(getattr(effect, "initiator", None)) else None
    if joueur is None:
        joueur = Worlds.GetCurrentPlayer(effect)
    faces = Search.SearchForCards(
        effect, joueur,
        include_encounter_deck=True,
        include_encounter_discard_pile=True,
        name=NOM_NEKRA,
        card_type=Minion,
    )
    return faces[0] if faces else None


def NekraEnJeu(effect: 'Effect') -> 'CardFace|None':
    """Nekra sur le terrain, ou None."""
    return Worlds.FindCardOnField(effect, name=NOM_NEKRA, card_type=Minion)


def PionsDeHaine(face: 'CardFace|None') -> int:
    """Le nombre de pions haine portes par Nekra."""
    if face is None:
        return 0
    return face.GetCounters(COMPTEUR_HAINE)


def AjouterUnPionDeHaine(effect: 'Effect', face: 'CardFace|None') -> None:
    """« place 1 hate counter on her (to a maximum of 5) ».

    ⚠ LE PLAFOND EST DANS LE TEXTE IMPRIME, pas dans le moteur : sans cette
    garde, Nekra monterait indefiniment (+1 ATQ et +1 PV par pion) puisque sa
    Reponse forcee part a CHAQUE attaque ET a CHAQUE fois qu'elle subit des
    degats, donc plusieurs fois par round.
    """
    if face is None:
        return
    if PionsDeHaine(face) >= HAINE_MAXIMUM:
        return
    Faces.PlaceCountersOn([face], 1, COMPTEUR_HAINE, effect)


def EstSpecifiqueIdentite(face: 'CardFace|None') -> bool:
    """« an identity-specific card » — jumeau du helper du set « Doctor Druid ».

    ⚠ DUPLIQUE VOLONTAIREMENT : les deux sets sont deux paquets Python
    distincts, et un module nemesis ne voit que CE fichier-ci. Meme ecriture
    qu'en face, reprise de `beast/beast_nemesis/bt021:46` : le garde de type
    est obligatoire, `IsClass` n'existe que sur `ClassCard`.

    Utilise par dr012 (« identity-specific CARD ») et dr013 (« identity-
    specific EVENT ») : c'est la ressource meme du heros que ce set attaque.
    """
    if face is None or not ClassCard.IsType(face):
        return False
    return face.IsClass("IdentitySpecific")
