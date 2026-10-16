from . import *

# Intensified (Intensifie), 7e carte d'etat du moteur, TMNT (Inkwire), capture
# Discord du serveur Bebop & Rocksteady (.planning/tmnt/intensified-capture.webp).
#
# Texte imprime : « The next time this character would discard a status card,
# discard this status card instead. This card cannot be given to a character that
# has no status cards. »
#
# Verbe : « intensify X » = donner une carte Intensified a X (te201 Intense
# Combatants). Fiche : docs/reference/mots-cles/intensified.md.
#
# CARTES DE REFERENCE
#  - `tough.py`, `cloaked.py` (meme dossier) : gabarit d'une carte d'etat
#    (`AbilityType.Status`, `effect.this.CastTo(StatusCard).GetBindFace()`).
#  - skrull_menace/paibok/__init__.py : un REMPLACEMENT de defausse, par
#    `WhenCardWouldDiscard` + `message.SetBeInstead(effect)`.
#
# TEXTE CONTRE CODE
#  « would discard a status card » : la fenetre `WhenCardWouldDiscard` d'une
#    AUTRE carte d'etat du MEME porteur. Tous les chemins de defausse d'un etat y
#    passent (`LoseState`, `Faces.DiscardAll([carte])` de cloaked/dazed, perforant,
#    cartes de joueur qui retirent un etat) : un seul crochet, pas un par etat.
#  « discard this status card INSTEAD » : la defausse d'origine est annulee (la
#    carte d'origine RESTE), Intensified part a sa place. L'EFFET de la carte
#    d'origine a deja eu lieu : il est resolu avant sa defausse par son propre
#    module (Sonne : l'attaque est deja annulee ; Coriace : les degats deja
#    prevenus ; Camoufle : le +2 deja applique).
#  « THE NEXT TIME » : une seule fois, puisque la carte part. Une defausse de
#    PLUSIEURS cartes d'un coup (« discard all Exposed ») : chaque Intensified
#    remplace UNE carte (« a status card »), les autres partent.
#  « this card cannot be given to a character that has no status cards » :
#    `CanStatus.CanbeIntensified` (GainStatus rend False, rien n'est pose).
#
# EXCLUSIONS (pas une defausse « par le personnage », documentees dans la fiche) :
#  - une autre Intensified (sinon deux Intensified se remplaceraient en boucle) ;
#  - le VIDAGE de la zone d'etat (`Status.vidage` : le porteur quitte le jeu, se
#    reinitialise, « defaussez chaque carte d'etat ») et les purges de REGLE
#    (plafond de Coriace depasse, gain de Stalwart).


def GetAbilities() -> Sequence['Ability']:

    def remplace(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> bool:
        if message.is_be_instead:
            return False
        this = effect.this.CastTo(StatusCard)
        autre = message.trigger
        if autre is this or not StatusCard.IsType(autre):
            return False
        autre = autre.CastTo(StatusCard)
        if autre.IsStatusName("Intensified"):
            return False
        if this.card.state.is_discarding:
            return False
        porteur = this.bind_face
        if porteur is None or autre.bind_face is not porteur:
            return False
        if porteur.components.status.vidage > 0:
            return False
        return True

    def defausser_a_la_place(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
        from game.operate.faces import Faces
        this = effect.this.CastTo(StatusCard)
        message.SetBeInstead(effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenCardWouldDiscard(
            AbilityType.Status,
            CardFinder(),
            defausser_a_la_place,
            conditions=[remplace],
        ),
    ]
