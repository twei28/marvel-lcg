from cards.pack import *

# Helpers partages du set « Shang-Chi » (mot-cle maison Flow : fiche mots-cles/flow.md).
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un
# NameError avale par le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.

NOM_PILE = "State of Flow"
ID_PILE = "ch002"
RESSOURCES_ASPECT = ["Aggression", "Justice", "Leadership", "Protection"]


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (jamais `GetInitiator()` en premier :
    il leve un assert quand l'initiateur n'est pas un joueur, et le moteur l'avale)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def LaPile(joueur: 'Player|None') -> 'CardFace|None':
    """State of Flow EN JEU chez ce joueur (carte permanente, un seul exemplaire), ou None."""
    if joueur is None:
        return None
    for face in joueur.supports.Get():
        if face.paper.card_id == ID_PILE:
            return face
    return None


def CartesDeLaPile(joueur: 'Player|None') -> List['CardFace']:
    """Les cartes de la pile, la plus RECENTE en dernier."""
    pile = LaPile(joueur)
    if pile is None:
        return []
    return list(pile.GetPlacedCardArea().Get())


def DessusDeLaPile(joueur: 'Player|None') -> 'CardFace|None':
    """« Look at the top card here » : la derniere attaque jouee, ou None si la pile est vide."""
    cartes = CartesDeLaPile(joueur)
    return cartes[-1] if cartes else None


def FlowActif(joueur: 'Player|None', ressource: str) -> bool:
    """Le Flow exigeant `ressource` ('R' physique, 'B' mental, 'Y' energie, 'G' wild) peut-il se resoudre ?

    DECISION UTILISATEUR (24/10/2026) : correspondance STRICTE. « a printed resource on that card
    matches » : une icone IMPRIMEE sur la carte du dessus (une carte peut en porter deux) ; un wild
    ne vaut que wild, un poing que poing. `HasColorPrinted` ne convertit pas le wild."""
    dessus = DessusDeLaPile(joueur)
    if dessus is None:
        return False
    return dessus.printed_resource_internal.HasColorPrinted(ressource)


def AccepterFlow(effect: 'Effect', joueur: 'Player|None', ressource: str) -> bool:
    """Regarde la pile ; si la ressource correspond, propose « you MAY also resolve its effects ».
    Rend True si le joueur accepte. L'appelant resout ensuite les effets du Flow puis appelle
    `FlowResolu` (qui declenche Chi Mastery)."""
    if joueur is None or not FlowActif(joueur, ressource):
        return False
    choix = [False]

    def accepter(cibles: Sequence['CardFace']) -> None:
        Unused(cibles)
        choix[0] = True

    # `MayChooseOneAbility` ajoute l'option « Cancel » : « you MAY also resolve its effects ».
    joueur.MayChooseOneAbility(
        effect,
        AbilityFactory.ForChoiceAbility("Resolve the Flow ability", accepter),
    )
    return choix[0]


def FlowResolu(joueur: 'Player|None', carte: 'CardFace') -> None:
    """« After you resolve a Flow ability » : previent Chi Mastery (ch001a)."""
    if joueur is not None:
        Message.AfterPlayerResolveFlow(joueur, carte).Send()
