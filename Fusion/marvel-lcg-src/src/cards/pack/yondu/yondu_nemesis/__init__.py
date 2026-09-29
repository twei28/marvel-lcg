from cards.pack import *

# Helpers partages du set « Yondu Nemesis ».


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """A QUI cette carte est-elle accrochee ? `None` si elle ne l'est pas.

    ⚠ NE JAMAIS appeler `GetBindFace()` en direct : il fait `assert face`
    (card_face.py:1063) et leve donc une AssertionError des que la carte n'est
    PAS attachee. Le moteur AVALE l'exception, la capacite ne fait rien, et
    aucun cas de test ne le voit — c'est l'AUTOPLAY qui l'a sorti le
    04/09/2026, 2 fois sur 128 parties, depuis la condition de yd015 : elle
    lisait l'hote de TOUTE amelioration passant par la, y compris une
    amelioration encore libre. Jumeau de `Hote` du set « Yondu ».
    """
    return getattr(face, "bind_face", None) if face is not None else None


def ConvoquerRencontre(effect: 'Effect', nom: str, card_type: Any=None) -> 'CardFace|None':
    """MOT-CLE MAISON `summon`, cote RENCONTRE.

    ⚠ Meme mot, meme definition que cote heros (fiche
    `docs/reference/mots-cles/summon.md`, glossaire MC4DB, aligne le
    29/09/2026) : deck de rencontre, sa defausse, la mise de cote et la zone
    « retire de la partie ». Jusqu'au 29/09, seules les deux premieres.

    Trois cartes du set nemesis en vivent : `yd015` Sav'rkk convoque son
    Sword-Gun-Arm, `yd017` Hard to Kill et `yd018` Savage Destruction
    convoquent Sav'rkk lui-meme.
    """
    joueur = effect.GetInitiator() if Player.IsType(getattr(effect, "initiator", None)) else None
    if joueur is None:
        joueur = Worlds.GetCurrentPlayer(effect)
    faces = Search.SearchForCards(
        effect, joueur,
        include_encounter_deck=True,
        include_encounter_discard_pile=True,
        include_set_aside=True,
        include_removed_area=True,
        name=nom,
        card_type=card_type,
    )
    if not faces:
        return None
    return faces[0]
