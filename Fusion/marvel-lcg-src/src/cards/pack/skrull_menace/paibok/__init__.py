from cards.pack import *

# ===========================================================================
# Scenario PAIBOK (Skrull Menace, Kajislav) — helpers partages (sk141-160).
#
# Regles propres (insert p.12, « Mastering Powers ») :
#  - Paibok gagne un nouveau pouvoir chaque fois qu'un attachement POWER SKRULL
#    est REVELE depuis le deck rencontre (les quatre attachements : Electricity
#    Projection, Ice Control, Metallic Skin, Shapeshifting).
#  - Des jetons de MAITRISE (compteur maison 'mastery', declare dans
#    card_face.py) sont poses sur Paibok : 1 a la mise en place (1A), +1 a la
#    revelation de 2A, +1 chaque fois que 2B « serait accompli ». Chaque jeton
#    est un pouvoir que Paibok a maitrise : tant que le nombre d'attachements
#    POWER SKRULL est <= au nombre de jetons, on ne peut PAS les defausser (texte
#    imprime sur les trois stades du mechant).
#  - Si 2A/2B (« Mastering Powers ») est en jeu et que Paibok porte les QUATRE
#    attachements POWER SKRULL a la fin de la phase des joueurs, les joueurs
#    perdent (texte en gras imprime sur 2B).
#  - « Resolve the "Boost" ability on each attachment in play that belongs to the
#    Paibok encounter set » (Captain Paibok, General Kalamari, Power
#    Demonstration, Getting Ruthless (alter ego), 2A) : le « Boost » d'un
#    attachement se resout comme effet actif, par le joueur qui resout (`joueur`).
#    Mecanique : `face.ResolveAbility(joueur, AbilityType.Boost, effect)` (modele
#    24017 Double Trouble, qui resout le « When Revealed » de sa propre carte) ;
#    le Boost recoit un message `ExTriggerPlayerMessage` dont `GetToPlayer()`
#    rend ce joueur, exactement ce que lisent tous les Boost de l'ensemble.
# ===========================================================================

NOM_MECHANT = "Paibok"
TRAIT_POUVOIR = "POWER SKRULL"
ENSEMBLE = "Paibok"            # set_name des cartes du scenario (« the Paibok encounter set »)
COMPTEUR_MAITRISE = 'mastery'


def PaibokEnJeu(effect: 'Effect') -> 'Villain|None':
    """Le MECHANT Paibok. ⚠ Le sbire nemesis de Lyja (sk066 « * Paibok », set Lyja
    Nemesis) porte le MEME nom : on filtre sur le type Villain."""
    return Worlds.FindCardOnField(effect, name=NOM_MECHANT, card_type=Villain)


def PouvoirsAttaches(paibok: 'CardFace') -> List['CardFace']:
    return [a for a in paibok.GetAttachedAttachments() if a.HasTrait(TRAIT_POUVOIR)]


def Maitrise(paibok: 'CardFace') -> int:
    return paibok.GetCounters(COMPTEUR_MAITRISE)


def PouvoirsVerrouilles(paibok: 'CardFace') -> bool:
    """« While the number of POWER SKRULL cards attached to Paibok is equal to or less than the
    number of mastery counters on him, POWER SKRULL cards cannot be discarded. »"""
    return len(PouvoirsAttaches(paibok)) <= Maitrise(paibok)


def PoserMaitrise(effect: 'Effect', paibok: 'CardFace|None'=None, nombre: int=1) -> None:
    paibok = paibok or PaibokEnJeu(effect)
    if paibok is not None:
        Faces.PlaceCountersOn([paibok], nombre, COMPTEUR_MAITRISE, effect)


def RegleDesPouvoirs() -> List['Ability']:
    """Le texte imprime sur les trois stades de Paibok : « POWER SKRULL cards cannot be discarded »
    tant que (attachements <= jetons de maitrise). Fenetre : `WhenCardWouldDiscard` (porte
    `CanBeInstead`, modele ih002/wd077b). ⚠ Seule une carte EN JEU et ATTACHEE a ce Paibok est
    protegee : « discard cards until a POWER SKRULL card is discarded » (2B, 1B) defausse des
    cartes du DECK, qui doivent pouvoir l'etre."""

    def verrouille(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> bool:
        face = message.trigger
        paibok = effect.this
        if not face.IsInPlay() or getattr(face, 'bind_face', None) != paibok:
            return False
        return PouvoirsVerrouilles(paibok)

    def interdire(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
        message.SetBeInstead(effect)

    return [
        AbilityFactory.WhenCardWouldDiscard(
            AbilityType.NonKeyword,
            CardFinder(trait=TRAIT_POUVOIR),
            interdire,
            conditions=[verrouille],
        ),
    ]


def RevelerPouvoirDuDeck(effect: 'Effect', joueur: 'Player|None') -> 'CardFace|None':
    """« Discard cards from the encounter deck until a POWER SKRULL card is discarded. Reveal that
    card. » (1B, 2B). Rien a trouver (les quatre sont deja sur Paibok) : on ne boucle pas."""
    if not _pouvoir_disponible(effect):
        return None
    face = Worlds.DiscardEncounterCardsUntil(effect, trait=TRAIT_POUVOIR, card_type=Attachment)
    if face is not None:
        face.Reveal(joueur or Worlds.GetFirstPlayer(effect), effect)
    return face


def ChercherEtReveler(effect: 'Effect', joueur: 'Player|None', **filtre: Any) -> 'CardFace|None':
    """« Search the encounter deck and discard pile for X and reveal it. » (Paibok II/III, The Maker.)
    La fouille melange le deck rencontre (comportement natif)."""
    face = Search.EncounterCard(effect, include_discard_pile=True, **filtre)
    if face is not None:
        face.Reveal(joueur or Worlds.GetFirstPlayer(effect), effect)
    return face


def _pouvoir_disponible(effect: 'Effect') -> bool:
    faces = list(Worlds.GetEncounterDeckCards(effect)) + list(Worlds.GetEncounterDiscardPileCards(effect))
    return any(f.HasTrait(TRAIT_POUVOIR) and not f.IsInPlay() for f in faces)


def AttachementsDeLEnsemble(effect: 'Effect') -> List['CardFace']:
    """Les attachements EN JEU du set Paibok : sur Paibok (Captain Paibok, POWER SKRULL) comme sur
    les identites des joueurs (Distracted, Hypnotized, Trapped in Ice)."""
    return [f for f in Worlds.GetOnFieldCards(effect)
            if Attachment.IsType(f) and f.IsInPlay() and f.paper.set_name == ENSEMBLE]


def ResoudreLesBoosts(effect: 'Effect', joueur: 'Player') -> None:
    """« Resolve the "Boost" ability on each attachment in play that belongs to the Paibok encounter
    set. » Ordre au choix du joueur qui resout (plusieurs effets resolus d'affilee)."""
    faces = AttachementsDeLEnsemble(effect)
    if not faces:
        return
    for face in joueur.ChooseOrder(faces):
        if face.IsInPlay():
            face.ResolveAbility(joueur, AbilityType.Boost, effect)


def AttacherAPaibok() -> 'Ability':
    """« Attach to Paibok. » (Captain Paibok et les quatre POWER SKRULL.) Modele 01100."""
    return AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=NOM_MECHANT, card_type=Villain))


def ActionDefausserPouvoir(cout: 'Cost') -> 'Ability':
    """« Hero Action: Spend ... resources → discard this card. » d'un attachement POWER SKRULL.
    Modele 01100 Enhanced Ivory Horn (`PlayerActionToDiscardThis` + `SetCost`). L'action n'est
    OFFERTE que si la carte PEUT etre defaussee (attachements > jetons de maitrise) : sinon le
    cout serait paye pour rien, la defausse etant interdite par `RegleDesPouvoirs`."""

    def defaussable(effect: 'Effect', message: 'Message2') -> bool:
        hote = getattr(effect.this, 'bind_face', None)
        return hote is not None and not PouvoirsVerrouilles(hote)

    return AbilityFactory.PlayerActionToDiscardThis(
        AbilityType.HeroAction,
        conditions=[defaussable],
    ).SetCost(cout)


def AuChoixDuJoueur(effect: 'Effect', joueur: 'Player', operation: Callable[[Sequence['CardFace']], Any], **filtre: Any) -> None:
    """« <verbe> a character you control » : le JOUEUR choisit parmi SES personnages (identite et
    allies). `filtre` : canbe_stunned / canbe_confused / canbe_exhaust (un personnage Stalwart n'est
    pas ciblable pour etourdir ou desorienter). Modeles 32073 Avalanche, 04136 Bitter Rival."""
    joueur.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility("", lambda cibles: operation(cibles)).SetTarget("YouControlUnit", **filtre),
    )

