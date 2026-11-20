from cards.pack import *

# Helpers partages du set « Warriors Three Nemesis » (Phenexian et Mysteltainn, prefixe `wt`).
# ⚠ Un helper vit ICI, jamais dans le `__init__.py` du pack (NameError avale, lecon hk005).


def en_jeu(effect: 'Effect', nom: str, type_carte) -> 'CardFace|None':
    for face in Worlds.FindCardsOnField(effect, card_type=type_carte):
        if face.IsInPlay() and face.IsName(nom):
            return face
    return None


def cherche_et_revele(effect: 'Effect', joueur: 'Player', nom: str) -> bool:
    """« search the encounter deck (and discard pile) for <nom> and reveal it »."""
    face = Search.EncounterCard(effect, joueur, include_discard_pile=True, name=nom)
    if face is None:
        return False
    face.Reveal(joueur, effect)
    return True


ID_SOUTIEN = {"Fandral": "wt003", "Hogun": "wt004", "Volstagg": "wt005"}


def soutiens_persona_du_joueur(joueur: 'Player') -> List['CardFace']:
    """Les soutiens PERSONA du joueur qui sont de vrais soutiens (le heros ACTIF est l'identite, son soutien n'en est pas un)."""
    identite = joueur.GetIdentity()
    actif = None
    if identite is not None and Hero.IsType(identite):
        for nom in ID_SOUTIEN:
            if identite.IsName(nom):
                actif = nom
    trouves: List['CardFace'] = []
    for face in joueur.GetControlCards(CardFinder(card_type=Support)):
        if not face.HasTrait("PERSONA"):
            continue
        if actif is not None and face.paper.card_id == ID_SOUTIEN[actif]:
            continue
        trouves.append(face)
    return trouves
