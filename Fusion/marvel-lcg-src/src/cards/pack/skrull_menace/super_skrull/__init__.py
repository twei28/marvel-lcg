from cards.pack import *

# ===========================================================================
# Scenario SUPER-SKRULL (Skrull Menace, Kajislav) — helpers partages.
# Cartes sk117-sk135 (livret p. 10, « Scenario #2 »).
#
# Regles propres (« Fantastic Four Powers ») :
#  - Un PAQUET SUPERPOWER : les 4 attachements (Flexibility, Invisibility,
#    Pyrokinesis, Rock Mimicry) sont melanges a la mise en place, en un paquet
#    pose a cote du complot principal (complot 1A, Setup). Le moteur n'a pas de
#    « paquet de scenario » libre : on ajoute le nom "SuperpowerDeck" a
#    `Worlds.ASIDE_DECK_NAME` (worlds.py, 15/10/2026), comme "PlanetDeck" du
#    scenario Skrull Empire. Modele : hunting_season/trap (paquet de pieges).
#  - « Reveal the top card of the SUPERPOWER deck » = la carte est REVELEE ; un
#    attachement revele entre en jeu, et son « Attach to Super-Skrull » l'attache
#    (AttachToFaceWhenPutIntoPlay). Paquet vide : rien ne se passe, et les cartes
#    qui disent « If you cannot » (Power Multiplying) le constatent.
#  - Chaque phase du mechant, apres l'etape 2 (Reponse obligatoire du mechant) :
#    tous les attachements SUPERPOWER retournent dans le paquet, qui est
#    melange, puis 1 (stade I) ou 2 (stades II et III) cartes sont revelees.
#
# ⚠ Choix hors texte imprime (voir defs/super_skrull_questions.md, Q1) : la DEFAUSSE
# du paquet SUPERPOWER (un pouvoir defausse par un effet de carte) est rendue au
# paquet au meme moment que les attachements en jeu. Sans cela, un pouvoir
# defausse serait perdu pour la partie. (Entre deux stades du mechant rien ne
# part : le moteur laisse les attachements au mechant qui avance.)
# ===========================================================================

NOM_MECHANT = "Super-Skrull"
NOM_PAQUET = "SuperpowerDeck"
NOM_KLRT = "Lord Kl'rt"


def PaquetSuperpouvoir(effect: 'Effect') -> 'SetAsideDeck':
    return Worlds.ScenarioDeck(effect, "SuperpowerDeck")


def EstSuperpouvoirAttachement(face: 'CardFace') -> bool:
    """Un ATTACHEMENT portant le trait SUPERPOWER (les ameliorations SUPERPOWER
    des heros, comme Lazerfist de Lyja, ne sont pas concernees)."""
    return Attachment.IsType(face) and face.HasTrait("SUPERPOWER")


def MechantSuperSkrull(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindVillain(effect, NOM_MECHANT)


def SuperpouvoirsAttaches(effect: 'Effect') -> List['CardFace']:
    """Les attachements SUPERPOWER attaches au Super-Skrull (Power Multiplying,
    Villain's Versatility)."""
    mechant = MechantSuperSkrull(effect)
    if mechant is None:
        return []
    return [a for a in mechant.GetAttachedAttachments() if EstSuperpouvoirAttachement(a)]


def CreerPaquetSuperpouvoir(effect: 'Effect') -> None:
    """Complot 1A, Setup : les 4 attachements SUPERPOWER mis de cote forment le
    paquet, melange, face cachee, avec sa defausse."""
    mechant = MechantSuperSkrull(effect)
    assert mechant, "le paquet SUPERPOWER se cree apres la mise en jeu du Super-Skrull"
    paquet = PaquetSuperpouvoir(effect)
    paquet.Create(effect, mechant, type=DeckType.AdditionalDeck)
    faces = [f for f in Worlds.AsideDeck(effect).Get(True) if EstSuperpouvoirAttachement(f)]
    Faces.ShuffleAllTo(faces, paquet.deck, effect)
    Faces.BindDiscardPile(faces, paquet.discard_pile)


def PaquetPret(effect: 'Effect') -> bool:
    return PaquetSuperpouvoir(effect).initialize


def PaquetNonVide(effect: 'Effect') -> bool:
    paquet = PaquetSuperpouvoir(effect)
    return paquet.initialize and paquet.deck.GetSize() > 0


def RevelerSuperpouvoir(effect: 'Effect') -> bool:
    """« Reveal the top card of the SUPERPOWER deck. » Rend vrai si une carte a
    ete revelee, faux si le paquet est vide (« If you cannot »)."""
    paquet = PaquetSuperpouvoir(effect)
    if not paquet.initialize:
        return False
    face = paquet.GetTopCard()
    if face is None:
        return False
    face.Reveal(Worlds.GetFirstPlayer(effect), effect)
    return True


def RemelangerSuperpouvoirs(effect: 'Effect') -> None:
    """« Shuffle each SUPERPOWER attachment from play into the SUPERPOWER deck. »
    Les cartes de la defausse du paquet reviennent avec elles (voir en-tete)."""
    paquet = PaquetSuperpouvoir(effect)
    if not paquet.initialize:
        return
    en_jeu = [f for f in Worlds.GetOnFieldCards(effect)
              if EstSuperpouvoirAttachement(f) and f.IsInPlay()]
    defausse = list(paquet.discard_pile.Get(True))
    Faces.ShuffleAllTo(en_jeu + defausse, paquet.deck, effect)
    # Rien n'a peut-etre bouge (paquet complet) : le melange est du quand meme.
    paquet.deck.Shuffle(effect)


def RenouvelerSuperpouvoirs(effect: 'Effect', nombre: int) -> None:
    """Reponse obligatoire du Super-Skrull : remelange, puis revele `nombre` cartes."""
    RemelangerSuperpouvoirs(effect)
    for _ in range(nombre):
        if not RevelerSuperpouvoir(effect):
            break


def ReponseDuMechant(nombre: int) -> 'Ability':
    """Forced Response : After resolving step two of the villain phase, shuffle
    each SUPERPOWER attachment from play into the SUPERPOWER deck and reveal the
    top `nombre` card(s) of the SUPERPOWER deck."""

    def renouveler(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        Unused(message)
        RenouvelerSuperpouvoirs(effect, nombre)

    return AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 2, renouveler)
