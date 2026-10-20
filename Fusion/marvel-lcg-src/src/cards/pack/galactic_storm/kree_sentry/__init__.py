from cards.pack import *

# ===========================================================================
# Scenario 1 KREE SENTRY (Galactic Storm, Kajislav) — gs076-gs090. Lot GS-4, 20/10/2026.
# Livret 1.2 p.9-10 et insert du scenario. Paquet de rencontre : Kree Sentry, Imperial Guard (modulaire par defaut),
# Standard (+ Expert).
#
# Regles propres :
#  - Rick Jones (gs081, allie de scenario) est mis en jeu sous le controle du PREMIER joueur par 1A (Setup) ; il porte
#    l'une des deux copies de Sentry's Grasp (gs082), l'autre est mise de cote. S'il quitte le jeu, les joueurs perdent.
#  - Sentry's Grasp (« la Poigne ») : condition attachee a un personnage ; le porteur ne peut ni contrer ni
#    manigancer et ne peut attaquer que Kree Sentry ou cette carte ; n'importe quel joueur peut ATTAQUER la Poigne comme
#    un sbire (modele officiel 54035 Encased in Ice : `consider_as` Minion) ; a 3 degats (5 avec Death Grip) elle est
#    remise de cote, et quand elle devrait quitter le jeu elle est mise de cote a la place. Livret p.9 : une Poigne
#    attachee a un sbire l'empeche d'activer pour manigancer ou attaquer ; les cartes et capacites qui visent un
#    sbire SANS etre des attaques ne peuvent pas viser la Poigne.
#  - Kree Sentry attaque un SBIRE ou un ALLIE (livret p.9 et p.4) : briques moteur communes `Enemy.AttackCharacter`
#    (decisions de l'utilisateur du 20/10/2026 : les joueurs PEUVENT defendre une attaque visant un sbire ;
#    `ally_attack_is_against_player=False` pour un allie, c'est le livret qui s'applique).
# ===========================================================================

SENTRY = "Kree Sentry"
RICK = "Rick Jones"
GRASP = "Sentry's Grasp"
REPULSOR = "Repulsor Blast Unit"
DEATH_GRIP = "Death Grip"
OUTPOST = "Outpost Collapse Protocol"


def EnJeu(effect: 'Effect', nom: str, type_carte: Any) -> 'CardFace|None':
    """`FindCardOnField` voit aussi les cartes glissees ou mises de cote sur le terrain : on exige IsInPlay."""
    for face in Worlds.FindCardsOnField(effect, name=nom, card_type=type_carte):
        if face.IsInPlay():
            return face
    return None


def KreeSentry(effect: 'Effect') -> 'Villain|None':
    return EnJeu(effect, SENTRY, Villain)


def RickJones(effect: 'Effect') -> 'Ally|None':
    return EnJeu(effect, RICK, Ally)


def PoignesDeCote(effect: 'Effect') -> List['CardFace']:
    """Les copies de Sentry's Grasp de la zone « mise de cote » (deck du scenario)."""
    return list(Worlds.GetSetAsideAreaCards(effect, CardFinder(name=GRASP, card_type=Attachment)))


def PoignesSur(cible: 'CardFace|None') -> List['CardFace']:
    """Les copies de Sentry's Grasp attachees a ce personnage."""
    if cible is None:
        return []
    return [f for f in cible.GetAttachedAttachments() if f is not None and f.IsName(GRASP)]


def PoignesEnJeu(effect: 'Effect') -> List['CardFace']:
    """Toutes les copies de Sentry's Grasp EN JEU (attachees)."""
    return [f for f in Worlds.FindCardsOnField(effect, name=GRASP, card_type=Attachment) if f.IsInPlay()]


def AttacherUnePoigne(effect: 'Effect', cible: 'CardFace|None') -> bool:
    """« attach a set aside copy of Sentry's Grasp to <cible> ». Faux si la cible n'est plus en jeu ou s'il ne
    reste aucune copie mise de cote (le texte enchaine alors « If you cannot, ... »)."""
    if cible is None or not cible.IsInPlay():
        return False
    copies = PoignesDeCote(effect)
    if not copies:
        return False
    return bool(copies[0].CastTo(Attachment).AttachTo2(cible, effect))


def SeuilDeLaPoigne(effect: 'Effect') -> int:
    """« If there is 3 or more damage here, set Sentry's Grasp aside » ; Death Grip : « 5 or more damage on it
    instead of 3 »."""
    for face in Worlds.FindCardsOnField(effect, name=DEATH_GRIP, card_type=SchemeSide2):
        if face.IsInPlay() and getattr(face, "gs_seuil_poigne", 3) == 5:
            return 5
    return 3


def PersonnagesDeLaTable(effect: 'Effect') -> List['CardFace']:
    """Les personnages en jeu : identites, allies, sbires, mechant (la Poigne n'en est pas un, livret p.9)."""
    return [f for f in Worlds.GetOnFieldCharacters(effect) if not f.IsName(GRASP)]


def PeutDepenserDeuxRessources(joueur: 'Player') -> bool:
    """« You may spend 2 resources of any type » : la depense n'est OFFERTE que si les deux ressources sont couvrables. Le
    moteur propose sinon « Do as much as you can: spend 1 resource » (regle des cartes rencontre a option impayable, RR 1.8) :
    le joueur brulerait une ressource pour rien, et `AskSpendResources` rendrait VRAI pour un paiement partiel. On lit les
    icones IMPRIMEES de la main et de la reserve (meme limite assumee que fne `PeutCouvrirLeCout` : les generateurs en jeu,
    dont la ressource de l'alter ego, ne sont pas comptes)."""
    faces = list(joueur.hand_cards.Get()) + list(joueur.reserve.Get())
    return FacesCounter.GetPrintedResources(faces).val >= 2


def DegatsDesPoignes(effect: 'Effect') -> None:
    """1B et 2B : « deal 1 damage to each character for each copy of Sentry's Grasp attached to it »."""
    for personnage in PersonnagesDeLaTable(effect):
        n = len(PoignesSur(personnage))
        if n and personnage.IsInPlay():
            effect.this.DealDamage([personnage], n, effect)
