from cards.pack import *

# ===========================================================================
# MUSE (Rainy, set 174, prefixe `mu`) — helpers partages du SET MODULAIRE.
#
# Ce n'est ni un heros ni un vilain : c'est un set modulaire, celui qu'on
# ajoute a n'importe quel scenario (modele `necroverse`, `intergalactic_hazards`).
# Six cartes distinctes, sept exemplaires (Obsession en double).
#
# ⚠ L'ARBITRAGE QUI TIENT TOUT LE SET, decision utilisateur du 13/09/2026.
#
# QUATRE cartes sur six parlent d'« une carte avec l'image de votre identite
# dessus » (mu001, mu003, mu004, mu006). Le moteur lit du texte et des
# mots-cles ; il ne voit AUCUNE illustration.
#
# ⚠ C'EST BIEN L'IMAGE QUI FAIT FOI, PAS LA CLASSE DE LA CARTE. Arbitrage
# tranche par l'utilisateur apres un premier choix inverse, le meme jour : « les
# cartes signature » (`card_class="IdentitySpecific"`) etait commode mais faux.
# Une amelioration d'aspect qui dessine le heros compte ; une carte signature
# qui ne montre que son equipement ne compte pas.
#
# On ne peut pas le deviner : on le RELEVE. `data/images_cartes.json` dit qui
# est dessine sur chaque illustration, rempli a la main depuis la page
# `/releve-images.html` reservee a l'administrateur. Voir `cards/images_cartes.py`
# et `.planning/todos/2026-09-13-releve-des-images-de-cartes.md`.
#
# ⚠ LE RELEVE EST LONG (5746 illustrations) ET NE BLOQUE RIEN. Une carte pas
# encore regardee garde l'ancienne approximation, les cartes signature. Muse
# reste donc jouable des le premier jour, et gagne en justesse a mesure que le
# releve avance. Les deux cas sont distincts et le restent : voir
# l'avertissement en tete de `cards/images_cartes.py`.

NOM_MUSE = "Muse"


def EstUneCarteSignature(face: 'CardFace|None') -> bool:
    """L'APPROXIMATION, utilisee seulement tant que l'image n'est pas relevee.

    ⚠ Ne l'appelez pas directement pour juger une carte : passez par
    `PorteLImageDe`, qui consulte d'abord le releve. Cette fonction ne repond
    pas a la question du texte, elle bouche le trou en attendant.

    Le vocabulaire vient de l'auteur lui-meme, qui ecrit « an identity-specific
    card » sur `mu005` Grim Inspiration : c'est donc le repli le plus proche de
    son intention.
    """
    if face is None:
        return False
    classe = face.CastTo(ClassCard)
    if classe is None:
        return False
    return classe.IsClass("IdentitySpecific")


def PorteLImageDe(face: 'CardFace|None', joueur: 'Player|None') -> bool:
    """« Une carte qui porte l'image de SON identite » : celle de ce joueur-la.

    ⚠ « THEIR identity », pas « la votre ». En multijoueur chaque joueur a sa
    propre identite : une carte qui montre Spider-Man ne reveille Muse que pour
    celui qui JOUE Spider-Man. C'est pour cela que le joueur est un argument et
    non une constante du set.

    ⚠ LES DEUX FACES COMPTENT. Peter Parker est l'identite de Spider-Man autant
    que Spider-Man : l'annuaire range les deux faces sous la meme personne, donc
    une image de Peter compte meme en forme heros, et l'inverse aussi.

    ⚠ REPLI ASSUME quand l'image n'a pas encore ete relevee : on retombe sur
    `EstUneCarteSignature`. Ce repli est volontairement DISCRET, c'est-a-dire
    qu'il ne s'applique QUE aux images jamais regardees. Une image relevee sans
    personne dessus repond non, meme si c'est une carte signature, sinon relever
    une carte n'aurait aucun effet.
    """
    if face is None or joueur is None:
        return False

    from cards.images_cartes import ImagesCartes, Identites

    paper = getattr(face, 'paper', None)
    if paper is None:
        return False

    if not ImagesCartes.EstRelevee(paper):
        return EstUneCarteSignature(face)

    identites_dessus = ImagesCartes.IdentitesSur(paper)
    if not identites_dessus:
        return False

    identite = joueur.GetIdentity()
    if identite is None:
        return False
    # Les deux faces de la carte d'identite, pas seulement celle en cours :
    # un joueur en forme alter ego reste la meme personne.
    qui_je_suis = set()
    carte = getattr(identite, 'card', None)
    # `printed_faces` = recto + verso imprimes (game/card/card.py:143).
    faces = list(getattr(carte, 'printed_faces', []) or []) if carte is not None else []
    for f in faces + [identite]:
        id_personne = Identites.DeLaFace(getattr(f, 'paper', None))
        if id_personne:
            qui_je_suis.add(id_personne)

    return any(x in qui_je_suis for x in identites_dessus)


def CartesSignatureDe(faces: Sequence['CardFace']) -> List['CardFace']:
    """Les cartes signature au sens strict. ⚠ RESERVE A `mu005` Grim
    Inspiration, la seule carte du set dont le texte imprime dit vraiment « an
    identity-specific card ». Les quatre autres parlent d'IMAGE : elles passent
    par `CartesAvecLImageDe`."""
    return [f for f in faces if EstUneCarteSignature(f)]


def CartesAvecLImageDe(faces: Sequence['CardFace'], joueur: 'Player|None') -> List['CardFace']:
    """Celles qui portent l'image de l'identite de ce joueur. Voir
    `PorteLImageDe` pour l'arbitrage et le repli."""
    return [f for f in faces if PorteLImageDe(f, joueur)]


def TrouverMuse(effect: 'Effect') -> 'CardFace|None':
    """Muse EN JEU, s'il y est. Rien d'autre : les cartes qui veulent le faire
    venir cherchent ensuite dans le deck de rencontre."""
    return Worlds.FindCardOnField(effect, name=NOM_MUSE, card_type=Minion)
