from cards.pack import *

NOMS_DISTRIBUES = ("DealtTrap0", "DealtTrap1", "DealtTrap2", "DealtTrap3")


def DeckPiege(effect: 'Effect') -> 'SetAsideDeck':
    return Worlds.ScenarioDeck(effect, "TrapDeck")


def DeckDistribue(effect: 'Effect', joueur: 'Player') -> 'SetAsideDeck':
    rang = Worlds.GetPlayers(effect).index(joueur)
    return Worlds.ScenarioDeck(effect, NOMS_DISTRIBUES[rang])


def EstPiege(face: 'CardFace') -> bool:
    return face.HasTrait("TRAP")


def CreerPaquetsPiege(effect: 'Effect') -> None:
    villain = Worlds.FindVillain(effect)
    assert villain
    paquet = DeckPiege(effect)
    paquet.Create(effect, villain, type=DeckType.AdditionalDeck)
    for nom in NOMS_DISTRIBUES:
        Worlds.ScenarioDeck(effect, nom).Create(effect, villain, type=DeckType.AdditionalDeck, has_discard_pile=False)
    faces = [f for f in Worlds.AsideDeck(effect).Get(True) if EstPiege(f)]
    Faces.ShuffleAllTo(faces, paquet.deck, effect)
    Faces.BindDiscardPile(faces, paquet.discard_pile)


def RemelangeDefaussePiege(effect: 'Effect') -> None:
    # Master Trapper (hs226, mode Hunter) : Forced Interrupt avant le remelange.
    if Worlds.FindCardsOnField(effect, name="Master Trapper"):
        Worlds.GetFirstPlayer(effect).DealEncounterCards(1, effect)
    paquet = DeckPiege(effect)
    paquet.deck.ShuffleWithDiscardPile(False, effect)


def DonnerPiege(effect: 'Effect', joueur: 'Player') -> bool:
    """Distribue face cachee le premier piege du paquet Trap ; paquet et defausse vides : rien."""
    paquet = DeckPiege(effect)
    if not paquet.initialize:
        return False
    if paquet.deck.GetSize() == 0 and paquet.discard_pile.GetSize() > 0:
        RemelangeDefaussePiege(effect)
    face = paquet.GetTopCard()
    if face is None:
        return False
    Faces.MoveAllTo([face], DeckDistribue(effect, joueur).deck, effect)
    return True


def PiegesDistribues(effect: 'Effect', joueur: 'Player') -> List['CardFace']:
    return list(DeckDistribue(effect, joueur).deck.Get(True))


def RevelerPiegesDistribues(effect: 'Effect', joueur: 'Player') -> None:
    for face in PiegesDistribues(effect, joueur):
        face.Reveal(joueur, effect)


def LimiteParJoueurEtParRound(effect: 'Effect', joueur: 'Player', cle: str, maximum: int, *, consommer: bool) -> bool:
    """Vrai tant que la limite « par joueur et par round » n'est pas atteinte ; `consommer` compte l'usage."""
    world = effect.world
    registre = getattr(world, "_limites_hs", None)
    if registre is None:
        registre = {}
        setattr(world, "_limites_hs", registre)
    index = (cle, Worlds.GetPlayers(effect).index(joueur), world.round_id)
    n = registre.get(index, 0)
    if n >= maximum:
        return False
    if consommer:
        registre[index] = n + 1
    return True


def PorteurEstAttaquant(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
    cible = effect.this.CastTo(Attachment).bind_face
    return cible is not None and message.attacker is cible


def PeutPayer(joueur: 'Player', couleur: str) -> bool:
    return FacesCounter.GetPrintedResources(joueur.hand_cards.Get()).HasColor(couleur)


def JoueurDuPorteur(effect: 'Effect') -> 'Player|None':
    cible = effect.this.CastTo(Attachment).bind_face
    return None if cible is None else cible.GetControlByPlayer()


def PiegeAttachement() -> 'Ability':
    """When Revealed : epuiser son identite (puis defausser) ou attacher la carte a son identite."""

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()

        def epuiser(cibles: Sequence['CardFace']) -> None:
            Faces.ExhaustAll([identite], effect)
            Faces.DiscardAll([this], effect)

        def attacher(cibles: Sequence['CardFace']) -> None:
            if not this.AttachTo2(identite, effect):
                Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Exhaust your identity", epuiser, condition=identite.IsReady()),
            AbilityFactory.ForChoiceAbility("Attach this card to your identity", attacher),
        )

    return AbilityFactory.WhenThisRevealed(None, revelation)


def ReponseDeMeute() -> 'Ability':
    """Forced Response : apres qu'un personnage du joueur engage attaque Kraven, ce Piege-animal attaque ce joueur."""

    def attaquer(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        animal = effect.this.CastTo(Minion)
        joueur = animal.engaged_player
        if joueur is not None:
            animal.DoAttackYou(joueur, effect)

    def condition(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        animal = effect.this.CastTo(Minion)
        joueur = animal.engaged_player
        if joueur is None or not animal.IsInPlay():
            return False
        vilain = Worlds.FindCardOnField(effect, card_type=Villain)
        if vilain is None or not any(vilain.IsCardId(i) for i in ("hs104", "hs105", "hs106")):
            return False
        return vilain.card in [x.card for x in message.attacked_targets] and message.attacker.GetControlByPlayer() is joueur

    return AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, None, attaquer, conditions=[condition])
