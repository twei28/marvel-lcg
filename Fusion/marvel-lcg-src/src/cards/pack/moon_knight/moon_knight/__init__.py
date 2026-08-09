from cards.pack import *

# Fabriques partagées du pack custom « Moon Knight » (DesignHacker, MC4 Sealed).
#
# L'identité a CINQ faces (« pile d'identités » de l'insert) :
#   76001a  Moon Knight   (héros,     réduit le coût des cartes Aggression)
#   76001b  Marc Spector  (alter-ego, face de départ, main de 7)
#   76001c  Mr. Knight    (héros,     réduit le coût des cartes Protection)
#   76001d  Steven Grant  (alter-ego, réduit le coût des cartes Leadership)
#   76001e  Jake Lockley  (alter-ego, réduit le coût des cartes Justice)
#
# La restriction de l'insert (interdiction de REVENIR à une identité quittée
# avant la fin de la phase des joueurs) n'est PAS câblée : bloquer un choix du
# menu de changement de forme coûterait l'action au joueur (leçon « Losing
# Control » du pack TAH). Écart documenté au §9 du guide.

NOMS_FACES_HEROS = ["Moon Knight", "Mr. Knight"]
NOMS_FACES_ALTER = ["Marc Spector", "Steven Grant", "Jake Lockley"]


def TrouverFaceIdentite(player: 'Player', nom: str) -> 'CardFace|None':
    identity = player.GetIdentity()
    if identity is not None and identity.IsName(nom):
        return None  # déjà sur cette face
    for face in player.GetAllIdentityFace(exclude=identity):
        if face.IsName(nom):
            return face
    return None


def ChangerVersFaceNommee(player: 'Player', effect: 'Effect', nom: str) -> None:
    """« Change form to X » : bascule directe vers la face nommée."""
    face = TrouverFaceIdentite(player, nom)
    if face is not None:
        player.GetIdentity().ChangeToFace(face, effect)


def ChoisirEtChangerDeForme(player: 'Player', effect: 'Effect',
                            vers_heros: bool|None=None) -> None:
    """« Change your form » : menu parmi les autres faces de la pile.

    vers_heros=True limite aux faces héros, False aux alter-egos,
    None laisse tout ouvert.
    """
    identity = player.GetIdentity()
    faces = list(player.GetAllIdentityFace(exclude=identity))
    if vers_heros is True:
        faces = [x for x in faces if Hero.IsType(x)]
    elif vers_heros is False:
        faces = [x for x in faces if AlterEgo.IsType(x)]
    if not faces:
        return

    def bascule(face: 'CardFace'):
        def operation(targets: Sequence['CardFace']) -> None:
            player.GetIdentity().ChangeToFace(face, effect)
        return operation

    player.ChooseAbilities(
        effect,
        *[AbilityFactory.ForChoiceAbility(f"Change form to {face.name}", bascule(face))
          for face in faces],
    )
