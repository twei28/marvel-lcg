from cards.pack import *

# Helpers partages du set « Mephisto » (scenario Neptune). Voir mephisto/__init__.py pour le scenario.
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale ;
# tout helper vit donc ICI.


def NombreDeJoueurs(effect: 'Effect') -> int:
    return len(Worlds.GetPlayers(effect))


def PactsDuJoueur(joueur: 'Player') -> List['Attachment']:
    """Les attachements BARGAIN que `joueur` controle : ceux qui pendent a son identite."""
    return [a for a in joueur.GetIdentity().GetAttachedAttachments() if a.HasTrait("BARGAIN")]


def PactsDeLIdentiteSource(source: 'CardFace|None') -> int:
    """Nombre de BARGAIN controles par l'IDENTITE qui est `source` (0 si `source` n'est pas une identite : allie, etc.)."""
    if source is None or not Identity.IsType(source):
        return 0
    joueur = source.GetControlByPlayer()
    return len(PactsDuJoueur(joueur)) if joueur is not None else 0


def PactsEnJeu(effect: 'Effect') -> List['Attachment']:
    """Chaque attachement BARGAIN en jeu (« each BARGAIN attachment in play »)."""
    pacts: List['Attachment'] = []
    for joueur in Worlds.GetPlayers(effect):
        pacts.extend(PactsDuJoueur(joueur))
    return pacts


def PactsDuDiable(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate', soin_par_joueur: int) -> None:
    """« [star] Devil's Pacts - Forced Interrupt : When Mephisto would activate against you, if you control a BARGAIN attachment, Mephisto
    does not activate and heals N[per_hero] damage instead. If no damage was healed this way, place 1 threat on the main scheme for each
    BARGAIN attachment in play. » (Mephisto I/II/III, N = 1, 2, 3.)"""
    this = effect.this.CastTo(Villain)
    joueur = message.to_player
    if joueur is None or not PactsDuJoueur(joueur):
        return
    message.SetBeInstead(effect)
    avant = this.sustained
    this.HealHealth(soin_par_joueur * NombreDeJoueurs(effect), effect)
    if this.sustained == avant:
        pacts = len(PactsEnJeu(effect))
        if pacts > 0:
            this.PlaceThreatOnSchemes("MainScheme", pacts, effect)


def HellLordsDeCote(effect: 'Effect') -> List['CardFace']:
    return list(Worlds.GetSetAsideAreaCards(effect, CardFinder(name="Hell Lord", card_type=Attachment)))


def AttacherLeHellLord(effect: 'Effect', cible: 'CardFace|None') -> bool:
    """« Find and attach the Hell Lord attachment to Mephisto » : la copie vient de la zone mise de cote (scenario json
    `set_aside`). Faux si elle n'y est pas ou si Mephisto a quitte le jeu."""
    if cible is None or not cible.IsInPlay():
        return False
    copies = HellLordsDeCote(effect)
    if not copies:
        return False
    return bool(copies[0].CastTo(Attachment).AttachTo2(cible, effect))


################################################################################
# La Damnation (zone maison : `player.damnation`, une pile face cachee par joueur ; docs/reference/mots-cles/damnation.md)
def DamnationDe(joueur: 'Player') -> List['CardFace']:
    return list(joueur.damnation.GetAll())


def ToutesLesDamnations(effect: 'Effect') -> List['CardFace']:
    cartes: List['CardFace'] = []
    for joueur in Worlds.GetPlayers(effect):
        cartes.extend(DamnationDe(joueur))
    return cartes


def LimiteDeDamnation(effect: 'Effect') -> int:
    """« If there are 10[per_hero] cards in Damnation, the players lose the game. »"""
    return 10 * NombreDeJoueurs(effect)


def VerifierDamnation(effect: 'Effect', *, en_plus: int = 0) -> None:
    """Defaite des joueurs quand la Damnation atteint 10 cartes par joueur. `en_plus` : cartes sur le point d'y entrer."""
    if effect.world.is_game_over:
        return
    if len(ToutesLesDamnations(effect)) + en_plus >= LimiteDeDamnation(effect):
        Worlds.SetGameOver(False, effect)


def MettreEnDamnation(effect: 'Effect', joueur: 'Player', nombre: int) -> List['CardFace']:
    """« Put N cards from the top of your deck facedown into Damnation. » Moins de cartes si le deck est plus court."""
    cartes = joueur.player_deck.GetTops(nombre) if nombre > 0 else []
    deplacees = Faces.MoveAllTo(cartes, joueur.damnation, effect) if cartes else []
    VerifierDamnation(effect)
    return deplacees


def RedirectionVersLaDamnation() -> 'Ability':
    """« Forced Interrupt : When a card is set aside from a player's deck, put it facedown into Damnation instead. » (Gateway to
    Corruption et Hell.) Pas de ré-entrée : la Damnation n'est pas une zone `is_set_aside`, la carte redirigee ne retombe pas ici."""

    def redirige(effect: 'Effect', message: 'Message.WhenCardWouldMoveToArea') -> None:
        proprietaire = message.from_area.GetOwnerPlayer()
        if proprietaire is None:
            return
        message.ChangeToArea(proprietaire.damnation, effect)
        VerifierDamnation(effect, en_plus=1)

    return AbilityFactory.WhenCardWouldMoveToArea(
        AbilityType.ForcedInterrupt,
        None,
        redirige,
        conditions=[
            lambda effect, message:
                message.into_area.flags.is_set_aside and message.from_area.flags.is_player_deck,
        ],
    )


################################################################################
# Complots : Hidden Clause (docs/reference/mots-cles/hidden-clause.md)
def ClauseCachee(nombre_par_joueur: int) -> List['Ability']:
    """Les deux capacites imprimees sur les faces B des complots 1B/2B/3B.
    « Forced Response : At the end of your turn, resolve the "Hidden Clause" ability for each BARGAIN attachment you control. »
    « Hidden Clause - Special : Put N[per_hero] card(s) from the top of your deck facedown into Damnation. »"""

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        joueur = message.GetToPlayer()
        if joueur is not None:
            MettreEnDamnation(effect, joueur, nombre_par_joueur * NombreDeJoueurs(effect))

    def fin_de_tour(effect: 'Effect', message: 'Message.AfterPlayerTurnEnd') -> None:
        joueur = message.GetToPlayer()
        for _ in PactsDuJoueur(joueur):
            effect.this.ResolveSpecialAbility(joueur, effect)

    return [
        AbilityFactory.WhenResolveSpecialAbility("This", special),
        AbilityFactory.AfterPlayerTurnEnd(AbilityType.ForcedResponse, "AnyPlayer", fin_de_tour),
    ]


def ResoudreLaClauseCachee(effect: 'Effect', joueur: 'Player') -> bool:
    """« resolve the "Hidden Clause" ability on the main scheme » pour `joueur` (cartes de rencontre)."""
    complot = Worlds.FindMainScheme(effect)
    if complot is None:
        return False
    return complot.ResolveSpecialAbility(joueur, effect)


def PactsDeLaDefausseDansLeDeck(effect: 'Effect') -> None:
    """« Shuffle each BARGAIN attachment from the encounter discard pile into the encounter deck. »"""
    pacts = [f for f in Worlds.GetEncounterDiscardPileCards(effect) if f.HasTrait("BARGAIN")]
    if pacts:
        Faces.ShuffleAllTo(pacts, "EncounterDeck", effect)


def PasserelleOuEnfer(effect: 'Effect') -> 'CardFace|None':
    """L'environnement a deux faces : Gateway to Corruption (mp007a) ou, une fois retourne, Hell (mp007b)."""
    for face in Worlds.FindCardsOnField(effect, card_type=Environment):
        if getattr(face.paper, "card_id", None) in ("mp007a", "mp007b"):
            return face
    return None


def JoueursDansLOrdre(effect: 'Effect') -> List['Player']:
    """« in player order » : le premier joueur d'abord, puis dans l'ordre des sieges (meme helper que hellfire_hunt_torn)."""
    joueurs = list(Worlds.GetPlayers(effect))
    premier = Worlds.GetFirstPlayer(effect)
    if premier in joueurs:
        i = joueurs.index(premier)
        joueurs = joueurs[i:] + joueurs[:i]
    return joueurs


################################################################################
# Les sept pactes BARGAIN (mp009 a mp015) : docs/reference/mots-cles/bargain.md
def MephistoActiveContre(effect: 'Effect', joueur: 'Player', carte_boost: 'CardFace|None'=None) -> None:
    """« Mephisto activates against you. » `carte_boost` : « Apply this card's boost icons for this activation as if it were a boost card » ;
    ses icones s'ajoutent a cette seule activation."""
    vilain = Worlds.FindVillainByGameArea(joueur.GetIdentity().card.game_area)
    if vilain is None:
        return
    vilain = vilain.CastTo(Villain)
    if carte_boost is None:
        vilain.DoActivate(joueur, effect)
        return

    def donne_la_carte(message: 'Message.WhenEnemyActivateAgainstYou') -> None:
        vilain.GiveBoostCard(carte_boost, effect, message.would_message)

    vilain.DoActivate(joueur, effect, operation=donne_la_carte)


def AbilitesDuPacte(reponse_propre: 'Callable[[Effect, Message.AfterPlayerTurnBegin], None]|None'=None, *, sans_reponse: bool=False) -> List['Ability']:
    """Les deux capacites imprimees communes aux sept pactes (le passif propre a chaque carte s'ajoute apres).
    « When Revealed : You may attach this card to your identity. If you do not, discard this card and Mephisto activates against you. »
    « Response : After your turn begins, discard this card -> Mephisto activates against you. Apply this card's boost icons for this
    activation as if it were a boost card. » (Peril : natif, `desc`.) `reponse_propre` : Black-Hearted (mp103) a une autre Response (voir blackheart/mp103.py)."""

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()

        def refuse(targets: Any) -> None:
            Faces.DiscardAll([this], effect)
            MephistoActiveContre(effect, joueur)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Attach this card to your identity", lambda targets: this.AttachTo2(joueur.GetIdentity(), effect)),
            AbilityFactory.ForChoiceAbility("Discard this card and Mephisto activates against you", refuse),
        )

    def reponse(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> None:
        if reponse_propre is not None:
            reponse_propre(effect, message)
        else:
            MephistoActiveContre(effect, message.to_player, effect.this)

    if sans_reponse:
        return [AbilityFactory.WhenThisRevealed(None, revele)]
    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterPlayerTurnBegin(AbilityType.Response, "AttachedPlayer", reponse).SetCostFunc(CostFunc.Discard("This")),
    ]


STATUTS_RETIRABLES = ("Stunned", "Confused", "Tough", "Exposed", "Cloaked", "Dazed", "Intensified")


################################################################################
# Cartes de rencontre (mp016 a mp028)
def RegarderEtRemelanger(effect: 'Effect', joueur: 'Player', nombre: int, *, au_plus: bool=False) -> int:
    """« look at N cards in Damnation and shuffle each back into its owner's deck » : `joueur` choisit, parmi les cartes de TOUTES les piles,
    `nombre` cartes (moins s'il n'y en a pas assez ; `au_plus` : « up to », il peut s'arreter). Chacune retourne dans le deck de SON proprietaire,
    melange. Rend le nombre de cartes remelangees."""
    faites = 0
    for _ in range(nombre):
        restantes = ToutesLesDamnations(effect)
        if not restantes:
            break
        carte = Search.SearchForCard(effect, joueur, faces=restantes, not_move=True, may=au_plus)
        if carte is None:
            break
        proprietaire = carte.card.area.GetOwnerPlayer()
        Faces.ShuffleAllTo([carte], proprietaire.player_deck, effect)
        faites += 1
    return faites


def JoueurDontUneCarteVaEnDamnation(effect: 'Effect', message: 'Message.WhenCardWouldMoveToArea') -> 'Player|None':
    """Le joueur dont une carte DE SON DECK est sur le point d'aller en Damnation, sinon None. Deux chemins y menent : le deplacement direct dans la
    pile (Hidden Clause, `MettreEnDamnation`) et la mise de cote que Gateway to Corruption / Hell redirige (la destination vue par une autre
    interruption est alors encore « mise de cote » : on la lit comme Damnation tant que l'environnement est en jeu)."""
    proprietaire = message.from_area.GetOwnerPlayer()
    if proprietaire is None or not message.from_area.flags.is_player_deck:
        return None
    if message.into_area is proprietaire.damnation:
        return proprietaire
    if message.into_area.flags.is_set_aside and PasserelleOuEnfer(effect) is not None:
        return proprietaire
    return None


def AbilitesDeDarkCompulsions() -> List['Ability']:
    """mp021 et mp022 (deux exemplaires identiques).
    « When Revealed : Each player resolves the "Hidden Clause" ability on the main scheme if they control a BARGAIN attachment. If no player
    controls a BARGAIN attachment, you may look at 1[per_hero] card in Damnation and shuffle it back into its owner's deck. »
    « [star] Boost : This card gains boost icons equal to the number of BARGAIN attachments in play. »"""

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        avec_pacte = [j for j in JoueursDansLOrdre(effect) if PactsDuJoueur(j)]
        if avec_pacte:
            for j in avec_pacte:
                ResoudreLaClauseCachee(effect, j)
        else:
            RegarderEtRemelanger(effect, joueur, NombreDeJoueurs(effect), au_plus=True)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        effect.this.CastTo(Treachery).GainBoostIcons(len(PactsEnJeu(effect)), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]


def ChercherEtAttacherUnPacte(effect: 'Effect', joueur: 'Player') -> bool:
    """« Search the encounter deck and discard pile for a BARGAIN attachment. Attach it to your identity. » Pas de When Revealed : la carte est
    attachee directement (comme mp020). Faux s'il n'y en a aucun."""
    pacte = Search.EncounterCard(effect, joueur, include_discard_pile=True, trait="BARGAIN", card_type=Attachment)
    if pacte is None:
        return False
    return bool(pacte.CastTo(Attachment).AttachTo2(joueur.GetIdentity(), effect))


def AbilitesDInfernalTemper() -> List['Ability']:
    """mp024 et mp025 (deux exemplaires identiques).
    « When Revealed (Alter-Ego) : Mephisto schemes with +X SCH, where X is equal to the number of BARGAIN attachments in play. »
    « When Revealed (Hero) : Mephisto attacks you with +X ATK, where X is equal to the number of BARGAIN attachments in play. »"""

    def manigance(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilain = Worlds.FindVillainByGameArea(joueur.GetIdentity().card.game_area)
        if vilain is None:
            return
        x = len(PactsEnJeu(effect))
        vilain.CastTo(Villain).DoSchemes(joueur, effect, property=SchemeProperty(against_player=joueur),
                                         operation=lambda would: would.GainSCHForThisScheme(x, effect))

    def attaque(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilain = Worlds.FindVillainByGameArea(joueur.GetIdentity().card.game_area)
        if vilain is None:
            return
        x = len(PactsEnJeu(effect))
        vilain.CastTo(Villain).DoAttackYou(joueur, effect, property=AttackProperty(against_player=joueur),
                                           operation=lambda would: would.GainATKForThisAttack(x, effect))

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", manigance),
        AbilityFactory.WhenThisRevealed("Hero", attaque),
    ]


def AbilitesDeMeagerRequest() -> List['Ability']:
    """mp026 et mp027 (deux exemplaires identiques).
    « When Revealed : You may ready your identity, draw 1 card, and heal 4 damage from your identity. If you do, resolve the "Hidden Clause" ability on
    the main scheme. Otherwise, this card gains surge. »
    « [star] Boost : After this activation, discard cards from the top of the encounter deck until a BARGAIN attachment is discarded. Reveal that card. »"""

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()

        def accepte(targets: Any) -> None:
            Faces.ReadyAll([identite], effect)
            joueur.DrawUp(1, effect)
            identite.HealHealth(4, effect)
            ResoudreLaClauseCachee(effect, joueur)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Ready your identity, draw 1 card, heal 4 damage and resolve the Hidden Clause", accepte),
            AbilityFactory.ForChoiceAbility("This card gains surge", lambda targets: ThisCardGainSurge(effect)),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetAgainstPlayer()

        def apres() -> None:
            # Copie des cartes du deck (dessus d'abord) : le moteur remelange la defausse a deck vide (voir mp020).
            for carte in list(Worlds.GetEncounterDeck(effect).GetAll()):
                Faces.DiscardAll([carte], effect)
                if carte.HasTrait("BARGAIN"):
                    carte.Reveal(joueur, effect)
                    return

        message.AfterThisActivation(effect, apres)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]


def AbilitesDeSinfulAmbitions() -> List['Ability']:
    """mp104 et mp105 (deux exemplaires identiques), Incite 2 natif.
    « When Revealed : If Blackheart is in play, you may shuffle a BARGAIN attachment you control into the encounter deck. If you do, give Blackheart a
    tough status. Otherwise, this card gains surge. » (« Otherwise » : sans Blackheart en jeu, sans pacte, ou si le joueur refuse.)"""

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        blackheart = Worlds.FindCardOnField(effect, name="Blackheart", card_type=Minion)

        def paie(targets: Any) -> None:
            pacte = Search.SearchForCard(effect, joueur, faces=PactsDuJoueur(joueur), not_move=True)
            if pacte is None:
                ThisCardGainSurge(effect)
                return
            Faces.ShuffleAllTo([pacte], "EncounterDeck", effect)
            Faces.GiveStatus([blackheart], "Tough", effect)

        if blackheart is not None and PactsDuJoueur(joueur):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Shuffle a BARGAIN attachment into the encounter deck and give Blackheart a tough status", paie),
                AbilityFactory.ForChoiceAbility("This card gains surge", lambda targets: ThisCardGainSurge(effect)),
            )
        else:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]


################################################################################
# Corruptive Offers (mp111 a mp116) : compteurs `corrupt` (docs/reference/mots-cles/compteurs-corrupt-scorned.md)
def CompteursCorrupt(pacte: 'CardFace') -> int:
    return pacte.CastTo(Attachment).GetCounters('corrupt')


def MettreDeCoteLeDessus(effect: 'Effect', joueur: 'Player', nombre: int) -> List['CardFace']:
    """« set-aside N cards from the top of your deck facedown » : par `Faces.SetAside`, donc redirigees en Damnation par Gateway to Corruption / Hell."""
    cartes = joueur.player_deck.GetTops(nombre) if nombre > 0 else []
    return Faces.SetAside(cartes, effect) if cartes else []


def AbilitesDePacteCorrompu() -> List['Ability']:
    """Communs aux quatre pactes de Corruptive Offers (mp111 a mp114) : le When Revealed des pactes et
    « Response : Discard this card -> set-aside X[per_hero] cards from the top of your deck facedown, where X is equal to the number of corrupt counters here. »
    Aucun declencheur n'est imprime sur cette Response : lue comme une action LIBRE pendant son tour (decision de l'utilisateur, 09/11/2026)."""

    def met_de_cote(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        # Le cout (defausse) est deja paye : les compteurs sont lus sur la carte defaussee (ils lui restent attaches).
        MettreDeCoteLeDessus(effect, joueur, CompteursCorrupt(this) * NombreDeJoueurs(effect))

    return [
        *AbilitesDuPacte(sans_reponse=True),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, met_de_cote).SetCostFunc(CostFunc.Discard("This")),
    ]


def AbilitesDeSoulGambling() -> List['Ability']:
    """mp115 et mp116 (deux exemplaires identiques).
    « When Revealed : Each player sets aside the top X[per_hero] cards of their deck, where X is equal to the number of corrupt counters on each BARGAIN attachment
    they have under their control. Otherwise, this card gains surge. »
    « [star] Boost : Place 1 corrupt counter on each BARGAIN attachment you control. If no counters were placed this way, shuffle this card into the encounter deck. »"""

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        total = 0
        for joueur in JoueursDansLOrdre(effect):
            x = sum(CompteursCorrupt(p) for p in PactsDuJoueur(joueur))
            total += len(MettreDeCoteLeDessus(effect, joueur, x * NombreDeJoueurs(effect)))
        if total == 0:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetAgainstPlayer()
        pacts = PactsDuJoueur(joueur) if joueur is not None else []
        posees = Faces.PlaceCountersOn(pacts, 1, 'corrupt', effect) if pacts else None
        if not pacts or not posees:
            ShuffleThisCardIntoEncounter(effect, message)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]


################################################################################
# Damned (mp121 a mp132)
def SbiresMystiquesEnJeu(effect: 'Effect', *, sauf: 'CardFace|None'=None) -> List['CardFace']:
    return [m for m in Worlds.GetOnFieldMinions(effect) if m.HasTrait("MYSTIC") and m is not sauf]


################################################################################
# Mother of Demons (mp141 a mp145) : sbires MYSTIC FACE CACHEE (carte technique `hellspawn_minion`, modele `ultron_facedown_drone`)
NOM_SBIRE_FACE_CACHEE = "Hellspawn Minion"


def DessusDeLaDefausse(joueur: 'Player', nombre: int) -> List['CardFace']:
    """Les `nombre` cartes du dessus de la defausse du joueur (la plus recente d'abord)."""
    return list(joueur.discard_pile.Get(True))[:nombre]


def MettreEnSbireFaceCachee(effect: 'Effect', joueur: 'Player', carte: 'CardFace') -> bool:
    """« put [a card] into play facedown and engaged with you as a MYSTIC minion » : la carte prend la face du sbire technique (HP 1, ATK 1, SCH 1, MYSTIC) et
    entre en jeu engagee avec `joueur` (meme montage que `Enemies.PutYouDeckTopCardAsFacedownMinion`)."""
    from game.card.factory import CardFactory
    paper = CardFactory.FindCardPapers(NOM_SBIRE_FACE_CACHEE)[0]
    gabarit = CardFactory.CreateFace(paper, effect.world)
    carte.card.SetAsCard(gabarit)
    return bool(carte.card.face.CastTo(Minion).PutIntoPlay(joueur, effect))


def SbiresFaceCachee(effect: 'Effect') -> List['CardFace']:
    return [m for m in Worlds.GetOnFieldMinions(effect) if getattr(m.paper, "card_id", None) == "hellspawn_minion"]


def AppelDeLaDemoniaque(effect: 'Effect') -> 'CardFace|None':
    """Call of the Demoness (mp142), si elle est en jeu."""
    return Worlds.FindCardOnField(effect, name="Call of the Demoness")


def AbilitesDeSpawnMagic() -> List['Ability']:
    """mp144 et mp145 (deux exemplaires identiques).
    « When Revealed : If Call of the Demoness is in play, put the top 2 cards of your discard pile into play each facedown and engaged with you as a MYSTIC minion. Otherwise,
    find Call of the Demoness and reveal it. » « [star] Boost : Resolve this card's "When Revealed" ability. »"""

    def resout(effect: 'Effect', joueur: 'Player') -> None:
        if AppelDeLaDemoniaque(effect) is not None:
            for carte in DessusDeLaDefausse(joueur, 2):
                MettreEnSbireFaceCachee(effect, joueur, carte)
            return
        trouve = Search.EncounterCard(effect, joueur, include_discard_pile=True, include_set_aside=True, name="Call of the Demoness", card_type=EncounterSideScheme)
        if trouve is not None:
            trouve.Reveal(joueur, effect)

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        resout(effect, message.GetToPlayer())

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        resout(effect, message.GetAgainstPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]


def TrouverRevelerEtActiver(effect: 'Effect', joueur: 'Player', nom: str) -> None:
    """« find <nom> and reveal [him/her]. (If [he/she] is already in play, [he/she] engages you.) <nom> activates against you. » (Black-Hearted mp103 pour Blackheart, Lilin Remaking mp143 pour Lilith.)"""
    sbire = Worlds.FindCardOnField(effect, name=nom, card_type=Minion)
    if sbire is None:
        trouve = Search.EncounterCard(effect, joueur, include_discard_pile=True, include_set_aside=True, name=nom, card_type=Minion)
        if trouve is not None:
            trouve.Reveal(joueur, effect)
        sbire = Worlds.FindCardOnField(effect, name=nom, card_type=Minion)
    else:
        sbire.CastTo(Minion).EngagePlayer(joueur, effect)
    if sbire is not None:
        sbire.CastTo(Minion).DoActivate(joueur, effect)
