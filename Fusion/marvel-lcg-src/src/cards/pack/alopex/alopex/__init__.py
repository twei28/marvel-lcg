from cards.pack import *

# Helpers partages du set « Alopex » (Inkwire, TMNT Heroes, prefixe `ta`).
# Questions en attente : .planning/tmnt/alopex-questions.md.

ID_PREY = "ta011"
NOM_PREY = "Prey"
TRAIT_KAMA = "KAMA"
HUNTER = 'hunter'


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient (ou que controle) la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception. Pour une carte de RENCONTRE, passer le joueur explicitement.
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def PreyAttachee(face: 'CardFace|None') -> 'CardFace|None':
    """La carte Prey attachee a `face` (ennemi ou manigance), ou None."""
    if face is None:
        return None
    for amelioration in face.GetAttachedUpgrades():
        if amelioration.name == NOM_PREY:
            return amelioration
    return None


def PreyMiseDeCote(joueur: 'Player|None') -> 'CardFace|None':
    """La carte Prey mise de cote par le Setup du joueur, ou None."""
    if joueur is None:
        return None
    for face in joueur.set_aside_deck.Get(True):
        if face.name == NOM_PREY:
            return face
    return None


def PreyEnJeu(joueur: 'Player|None') -> 'CardFace|None':
    """La carte Prey en jeu (attachee quelque part) qui appartient au joueur."""
    if joueur is None:
        return None
    for face in Worlds.FindCardsOnField(joueur.GetIdentity(), name=NOM_PREY):
        return face
    return None


def RessourcesMentalesDepensees(joueur: 'Player', effect: 'Effect', maximum: int) -> int:
    """« You may spend up to N [mental] resources » : combien le joueur a-t-il
    reellement depense (0 s'il refuse ou ne peut pas payer).

    Modele `Cost(..., up_to=True)` de `26022` Machine Man / `47012` Husk, ici
    dans le CORPS de l'effet (`AskSpendResourcesInternal`, comme `dt107`) puisque
    le texte n'a pas de fleche : la depense est facultative et son montant
    pilote l'effet. `Cost("B...")` accepte les ressources [mental] ET wild.
    """
    cout = Cost({1: "B", 2: "BB", 3: "BBB"}[maximum], up_to=True)
    paye = joueur.AskSpendResourcesInternal(cout, effect)
    if paye is None:
        return 0
    return int(paye.val)
