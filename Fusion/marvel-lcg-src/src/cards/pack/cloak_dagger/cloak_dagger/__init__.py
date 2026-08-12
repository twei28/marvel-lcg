from cards.pack import *

# Fabriques partagées du pack custom « Cloak & Dagger » (DesignHacker).
#
# Le pack physique fait piloter DEUX héros par un seul joueur : deux mini-decks,
# deux mains, les deux identités en jeu côte à côte. Depuis le 5/8/2026 le
# moteur sait le faire : le deck déclare une identité LIÉE (`linked_identity`),
# que `SceneLoader.ExpandLinkedIdentity` développe en un second joueur, avec sa
# propre identité, son deck, sa main et sa défausse.
#   cd001a / cd001b   Cloak  / Tyrone Johnson   (joueur 1)
#   cd002a / cd002b   Dagger / Tandy Bowen      (joueur 2, identité liée)
#   cd003             Forces Combined, soutien Setup permanent
# Les synergies imprimées « while X is in play » se lisent donc au pied de la
# lettre : chaque face est une vraie identité en jeu.

NOM_CLOAK = "Cloak"
NOM_DAGGER = "Dagger"
NOM_TYRONE = "Tyrone Johnson"
NOM_TANDY = "Tandy Bowen"


def _face_en_jeu(effect: 'Effect', nom: str, type_de_face: Any) -> 'CardFace|None':
    return Worlds.FindCardOnField(effect, name=nom, card_type=type_de_face)


def CloakEstEnJeu(effect: 'Effect') -> bool:
    """« While Cloak is in play » : l'identité liée est en forme héros Cloak."""
    return _face_en_jeu(effect, NOM_CLOAK, Hero) is not None


def DaggerEstEnJeu(effect: 'Effect') -> bool:
    return _face_en_jeu(effect, NOM_DAGGER, Hero) is not None


def TrouverDagger(effect: 'Effect', player: 'Player|None'=None) -> 'CardFace|None':
    """La face heros Dagger en jeu (celle du joueur precise, le cas echeant).

    Depuis la refonte du 5/8/2026, Dagger est l'identite du joueur LIE, plus
    une alliee : on cherche donc une face `Hero`.
    """
    faces = Worlds.FindCardsOnField(effect, card_type=Hero, name=NOM_DAGGER)
    if player is not None:
        faces = [x for x in faces if x.GetControlByPlayer() == player]
    return faces[0] if faces else None


def CompterFaceEnJeu(nom: str, type_de_face: Any):
    """Fabrique un `check_fn` pour `ThisGainKeyword` : 1 si la face est en jeu.

    Le second argument `ui` sert au moteur à montrer au joueur QUI accorde le
    bonus ; on y range la face trouvée, comme Madame Web mw001a.
    """
    def compter(effect: 'Effect', ui: List['CardFace']) -> int:
        face = _face_en_jeu(effect, nom, type_de_face)
        if face is None:
            return 0
        ui.append(face)
        return 1
    return compter


def DegatsVilainCettePhase(world: 'Any', player: 'Player') -> int:
    """Compteur maison des dégâts infligés au méchant pendant la phase courante.

    Alimenté et remis à zéro par Living Light (cd008). Rangé sur `world` comme
    les bulles de Gwenpool, pour survivre aux allers-retours de l'upgrade.
    """
    suivi = getattr(world, "cd_degats_vilain_phase", None)
    if suivi is None:
        return 0
    return suivi.get(id(player), 0)


def AjouterDegatsVilainCettePhase(world: 'Any', player: 'Player', valeur: int) -> None:
    suivi = getattr(world, "cd_degats_vilain_phase", None)
    if suivi is None:
        suivi = {}
        setattr(world, "cd_degats_vilain_phase", suivi)
    suivi[id(player)] = suivi.get(id(player), 0) + valeur


def RemettreDegatsVilainPhase(world: 'Any') -> None:
    setattr(world, "cd_degats_vilain_phase", {})
