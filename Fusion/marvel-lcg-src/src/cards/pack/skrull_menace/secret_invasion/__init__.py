from cards.pack import *

# ===========================================================================
# Scenario SECRET INVASION (Skrull Menace, Kajislav) — helpers partages.
# Cartes sk189-sk227 (livret p. 16, « Scenario #5 »).
#
# Regles propres :
#  - VERANKE : une seule carte mechant DOUBLE FACE par stade. Face A = Spider-Woman
#    (Veranke), trait CAMOUFLAGED, ne peut PAS subir de degats ; face B = Queen Veranke,
#    trait REVEALED, vulnerable. Elle commence CAMOUFLAGED. « Flip » = `card.Flip` :
#    attachements, cartes d'etat, boosts et degats restent (meme objet carte). Apres la
#    defaite d'un stade, le suivant arrive du MEME COTE : c'est natif (scenario.py,
#    `AdvanceVillainStage` : les faces du stade suivant dont le nom est celui de la face
#    vaincue passent devant).
#  - SOUPCON : l'environnement « Who Do You Trust? » (sk194) porte des jetons de SOUPCON
#    (compteur 'suspicion'), qui evoluent « de concert » avec la menace du complot principal :
#    menace posee -> autant de jetons retires ; menace retiree -> autant de jetons poses.
#  - PAQUET IMPOSTOR : 20 cartes double face (allie CAMOUFLAGED en A, sbire REVEALED en B)
#    melangees a la mise en place dans un paquet de scenario nomme `ImpostorDeck`
#    (worlds.py), avec sa DEFAUSSE IMPOSTOR. « Put a CAMOUFLAGED ally / a REVEALED minion at
#    random from the IMPOSTOR deck » = on prend la carte du dessus du paquet melange, puis on
#    la met du bon cote. Paquet vide : on y remelange la defausse, sans penalite (pas de jeton
#    d'acceleration : le paquet n'est pas le deck rencontre).
#  - ALLIE CAMOUFLAGED : un allie normal (compte dans la limite d'allies, attaque, defend), qui
#    NE PEUT PAS contrer. Si l'identite de son controleur est en alter ego pendant la phase du
#    mechant, il MANIGANCE juste apres l'activation du mechant contre ce joueur, subit des degats
#    consequentiels (une pastille) et ne s'incline pas. S'il devait QUITTER LE JEU, on le
#    RETOURNE a la place (Interruption forcee imprimee sur chaque allie).
#  - RETOURNER un allie CAMOUFLAGED = le REVELER : cartes d'etat, ameliorations et attachements
#    de l'allie sont defausses, la carte passe sur sa face sbire, qui est revelee et ENGAGE LE
#    JOUEUR QUI CONTROLAIT l'allie avant le retournement. Le sbire REVEALED qui quitte le jeu va
#    dans la DEFAUSSE IMPOSTOR (liaison `Faces.BindDiscardPile`, comme les pouvoirs de Super-Skrull).
# ===========================================================================

ID_ENVIRONNEMENT = "sk194"      # « Who Do You Trust? »
NOM_PAQUET = "ImpostorDeck"
COMPTEUR = 'suspicion'


# ---------------------------------------------------------------------------------------------------------------------
# Veranke
# ---------------------------------------------------------------------------------------------------------------------
def Veranke(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindVillain(effect)


def VerankeCamouflee(effect: 'Effect') -> bool:
    v = Veranke(effect)
    return v is not None and v.HasTrait("CAMOUFLAGED")


def VerankeRevelee(effect: 'Effect') -> bool:
    v = Veranke(effect)
    return v is not None and v.HasTrait("REVEALED")


def RetournerVeranke(effect: 'Effect') -> bool:
    """« Flip Queen Veranke » / « flip Spider-Woman » : on retourne la carte mechant quelle que soit
    sa face. Les attachements, statuts, boosts et degats restent (meme objet carte)."""
    v = Veranke(effect)
    if v is None or not v.IsInPlay():
        return False
    return v.card.Flip(effect)


# ---------------------------------------------------------------------------------------------------------------------
# Soupcon
# ---------------------------------------------------------------------------------------------------------------------
def Soupcon(effect: 'Effect') -> 'Environment|None':
    """L'environnement « Who Do You Trust? » en jeu (reconnu par son card_id : son nom porte des guillemets)."""
    for f in Worlds.GetOnFieldCards(effect):
        if Environment.IsType(f) and f.paper.card_id == ID_ENVIRONNEMENT and f.IsInPlay():
            return f.CastTo(Environment)
    return None


def NbSoupcons(effect: 'Effect') -> int:
    env = Soupcon(effect)
    return env.GetCounters(COMPTEUR) if env is not None else 0


def SeuilSoupcons(effect: 'Effect') -> int:
    """« 2[per_hero] jetons de soupcon »."""
    return 2 * Worlds.GetPlayerNumIcon(effect)


def PoserSoupcons(effect: 'Effect', nombre: int) -> int:
    env = Soupcon(effect)
    if env is None or nombre <= 0:
        return 0
    return Faces.PlaceCountersOn([env], nombre, COMPTEUR, effect) or 0


def RetirerSoupcons(effect: 'Effect', nombre: 'int|Literal["All"]') -> int:
    env = Soupcon(effect)
    if env is None or nombre == 0:
        return 0
    return Faces.RemoveCountersOn([env], nombre, COMPTEUR, effect) or 0


def MoinsDeSoupcons(effect: 'Effect') -> bool:
    """« if there are less than 2[per_hero] suspicion counters on "Who Do You Trust?" »."""
    return NbSoupcons(effect) < SeuilSoupcons(effect)


# ---------------------------------------------------------------------------------------------------------------------
# Paquet IMPOSTOR
# ---------------------------------------------------------------------------------------------------------------------
def PaquetImpostor(effect: 'Effect') -> 'SetAsideDeck':
    return Worlds.ScenarioDeck(effect, "ImpostorDeck")


def EstImpostor(face: 'CardFace') -> bool:
    return face.HasTrait("IMPOSTOR")


def CreerPaquetImpostor(effect: 'Effect') -> None:
    """Complot 1A, Setup : les 20 cartes IMPOSTOR mises de cote forment le paquet, melange, avec sa
    defausse. Chaque carte repart sur sa face ALLIE (A)."""
    mechant = Veranke(effect)
    assert mechant, "le paquet IMPOSTOR se cree apres la mise en jeu de Veranke"
    paquet = PaquetImpostor(effect)
    paquet.Create(effect, mechant, type=DeckType.AdditionalDeck)
    faces = [f for f in Worlds.AsideDeck(effect).Get(True) if EstImpostor(f)]
    Faces.ShuffleAllTo(faces, paquet.deck, effect)
    Faces.BindDiscardPile(faces, paquet.discard_pile)


def PaquetImpostorPret(effect: 'Effect') -> bool:
    return PaquetImpostor(effect).initialize


def _remelanger_si_vide(effect: 'Effect') -> None:
    """« If the IMPOSTOR deck is ever empty, shuffle the IMPOSTOR discard pile back into the IMPOSTOR deck.
    There is no penalty for doing this. »"""
    paquet = PaquetImpostor(effect)
    if paquet.deck.GetSize() == 0 and paquet.discard_pile.GetSize() > 0:
        Faces.ShuffleAllTo(list(paquet.discard_pile.Get(True)), paquet.deck, effect)


def TirerImpostor(effect: 'Effect', camoufle: bool) -> 'CardFace|None':
    """La carte du DESSUS du paquet melange (= « at random »), posee sur la face voulue : allie CAMOUFLAGED
    (`camoufle`) ou sbire REVEALED. Rend la face (apres retournement eventuel), ou None si le paquet et sa
    defausse sont vides."""
    paquet = PaquetImpostor(effect)
    if not paquet.initialize:
        return None
    _remelanger_si_vide(effect)
    face = paquet.GetTopCard()
    if face is None:
        return None
    if Ally.IsType(face) != camoufle:
        face.card.Flip(effect, call_reveal=False)
    return face.card.face


def MettreAllieCamoufle(effect: 'Effect', joueur: 'Player') -> 'CardFace|None':
    """« Put a CAMOUFLAGED ally at random from the IMPOSTOR deck into play under your control. » Rend la face
    de l'allie mis en jeu, None si rien n'a pu entrer (paquet vide)."""
    face = TirerImpostor(effect, True)
    if face is None:
        return None
    face.PutIntoPlay(joueur, effect, under_control=True)
    return face if face.IsInPlay() else None


def MettreSbireRevele(effect: 'Effect', joueur: 'Player') -> 'CardFace|None':
    """« Put a REVEALED minion at random from the IMPOSTOR deck into play engaged with you. » : la carte est
    REVELEE par `joueur` ; son « When Revealed » (soigne tout, met en jeu engage) fait le reste."""
    face = TirerImpostor(effect, False)
    if face is None:
        return None
    face.Reveal(joueur, effect)
    return face if face.IsInPlay() else None


# ---------------------------------------------------------------------------------------------------------------------
# Allie CAMOUFLAGED
# ---------------------------------------------------------------------------------------------------------------------
def AlliesCamoufles(effect: 'Effect') -> List['CardFace']:
    """Les allies CAMOUFLAGED en jeu (toutes zones d'allies)."""
    return [a for a in Worlds.GetOnFieldAllies(effect) if a.HasTrait("CAMOUFLAGED")]


def SbiresImpostor(effect: 'Effect') -> List['CardFace']:
    return [m for m in Worlds.GetOnFieldMinions(effect) if m.HasTrait("IMPOSTOR")]


def SchAllie(allie: 'CardFace') -> int:
    """Le SCH d'un allie Impostor : la classe Ally n'a pas de stat SCH, mais le SCH imprime est le MEME sur
    les deux faces de la carte (verifie sur les 20 scans) : on le lit sur la face sbire."""
    for face in allie.card.printed_faces:
        if Minion.IsType(face):
            return face.printed_scheme
    return 0


def RetournerAllie(effect: 'Effect', allie: 'CardFace', joueur: 'Player|None'=None) -> 'CardFace|None':
    """« Flip a CAMOUFLAGED ally » = le reveler (livret p. 16). Cartes d'etat, ameliorations et attachements de
    l'allie sont defausses, la carte passe sur sa face sbire, revelee, et engage le joueur qui controlait
    l'allie avant le retournement. Rend la face sbire."""
    if not Ally.IsType(allie) or not allie.IsInPlay():
        return None
    if joueur is None:
        joueur = allie.GetControlByPlayer()
    unite = allie.CastTo(Ally)
    unite.DiscardEachStatus(effect)
    autres = list(allie.GetAttachedUpgrades()) + list(allie.GetAttachedAttachments())
    if autres:
        Faces.DiscardAll(autres, effect)
    allie.card.Flip(effect, call_reveal=False)
    sbire = allie.card.face
    sbire.Reveal(joueur, effect, is_by_flipping=True)
    return sbire


def AllieAvecLePlusDePv(effect: 'Effect', allies: Sequence['CardFace']) -> 'CardFace|None':
    """« the CAMOUFLAGED ally with the most remaining hit points » (le joueur departage les egalites)."""
    if not allies:
        return None
    return Filter.One(list(allies), effect, most_remaining_hp=True)


# ---------------------------------------------------------------------------------------------------------------------
# Capacites communes aux 20 cartes Impostor
# ---------------------------------------------------------------------------------------------------------------------
def AllieImpostor() -> List['Ability']:
    """Face ALLIE (A). Interruption forcee « When X would leave play, flip X instead », « cannot thwart »
    (livret), et la manigance de la phase du mechant quand l'identite du controleur est en alter ego."""

    def retourner_a_la_place(effect: 'Effect', message: 'Message.WhenCardWouldLeavePlay') -> None:
        this = effect.this
        if getattr(this, 'en_retournement', False):
            return
        message.SetBeInstead(effect)
        this.en_retournement = True
        try:
            RetournerAllie(effect, this)
        finally:
            this.en_retournement = False

    def manigance(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this
        Unused(message)
        joueur = message.to_player
        if joueur is None or not this.IsInPlay() or this.GetControlByPlayer() != joueur:
            return
        ManigancerAllie(effect, this)

    def phase_du_mechant(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> bool:
        this = effect.this
        joueur = message.to_player
        if joueur is None or not this.IsInPlay() or this.GetControlByPlayer() != joueur:
            return False
        # « during the villain phase » : l'activation du mechant de l'etape 2 (pas une activation d'une traitrise)
        return effect.world.phase.IsVillainPhaseStep(2) and joueur.IsAlterEgo()

    return [
        *AbilityFactory.UnitCannotThwartTarget("This", cannot_thwart=True),
        AbilityFactory.WhenCardWouldLeavePlay(AbilityType.ForcedInterrupt, "This", retourner_a_la_place),
        AbilityFactory.AfterEnemyActivationEnd(AbilityType.NonKeyword, Villain, manigance, conditions=[phase_du_mechant]),
    ]


def ManigancerAllie(effect: 'Effect', allie: 'CardFace') -> None:
    """Manigance d'un allie CAMOUFLAGED : sa valeur SCH en menace sur le complot principal, puis UN degat
    consequentiel (la pastille du SCH), sans s'incliner."""
    from game.effect.rule import Consequential, SchemeActive
    scheme = Worlds.FindMainScheme(allie)
    if scheme is None:
        return
    valeur = SchAllie(allie)
    scheme.PlaceThreatInternal(valeur, SchemeActive(allie))
    if allie.IsInPlay():
        allie.CastTo(Ally).TakeDamage(allie, 1, Consequential(allie))


def SbireImpostor(*, revele: bool=True) -> List['Ability']:
    """Face SBIRE (B) : « When Revealed: Heal all damage from X and put it into play engaged with you »."""

    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        if this.IsInPlay():
            this.HealthUnits([this], "All", effect)
        if joueur is not None and this.engaged_player != joueur:
            this.PutIntoPlay(joueur, effect)

    return [AbilityFactory.WhenThisRevealed(None, reveler)]


# ---------------------------------------------------------------------------------------------------------------------
# Choix d'un joueur (« under any player's control »)
# ---------------------------------------------------------------------------------------------------------------------
def ChoisirJoueur(effect: 'Effect', chooser: 'Player') -> 'Player':
    """Le joueur `chooser` designe UN joueur de la partie (lui-meme compris). Un seul joueur : pas de question."""
    joueurs = list(Worlds.GetPlayers(effect))
    if len(joueurs) == 1:
        return joueurs[0]
    identites = [j.GetIdentity() for j in joueurs]
    choisi = chooser.AskChooseFaces(identites, (1, 1), effect, prompt="Choose a player")
    if not choisi:
        return chooser
    return choisi[0].GetControlByPlayer()


# ---------------------------------------------------------------------------------------------------------------------
# Veranke : capacites imprimees des six faces
# ---------------------------------------------------------------------------------------------------------------------
def CapacitesSpiderWoman() -> List['Ability']:
    """Face A (CAMOUFLAGED) : ne peut pas subir de degats ; ★ Reponse forcee apres qu'elle vous attaque : 1 jeton de
    soupcon ; « You are a Skrull! » : Action de heros, incliner un heros et depenser 1[per_hero] ressources de
    n'importe quel type, le cout pouvant etre paye en groupe."""

    def soupconner(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        Unused(message)
        PoserSoupcons(effect, 1)

    def retourner(effect: 'Effect', message: 'Message2') -> None:
        Unused(message)
        RetournerVeranke(effect)

    def heros_a_incliner(effect: 'Effect') -> List['CardFace']:
        # En groupe, n'importe quel heros ; sans le groupe (Mistrust and Paranoia), le heros du joueur seulement.
        initiateur = effect.GetInitiator()
        tous = Worlds.GetOnFieldHeroes(effect)
        if PaiementEnGroupeAutorise(effect):
            return list(tous)
        return [h for h in tous if h.GetControlByPlayer() == initiateur]

    action = (AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, retourner)
              .SetName("You are a Skrull!")
              .SetCostFunc(CostFunc.Exhaust(heros_a_incliner))
              .SetCost(lambda effect, cibles: Cost("1") * Worlds.GetPlayerNumIcon(effect)))
    action.cout_en_groupe = True
    return [
        *AbilityFactory.UnitCannotTakeDamage("This"),
        AbilityFactory.AfterUnitAttackYou(AbilityType.ForcedResponse, "This", soupconner),
        action,
    ]


def CapacitesQueen(stade: int) -> List['Ability']:
    """Face B (REVEALED) : Reponse forcee apres la fin de la phase du mechant, si un joueur est en alter ego,
    retourner Queen Veranke (stade III : « Otherwise, discard the top card of the encounter deck, if it is a
    treachery, flip Queen Veranke »). Stades I et II : Une fois vaincue, retirer tous les jetons de soupcon."""
    from cards.pack.skrull_menace.lyja import EstTraitrise

    def fin_de_phase(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        Unused(message)
        if any(j.IsAlterEgo() for j in Worlds.GetPlayers(effect)):
            RetournerVeranke(effect)
        elif stade == 3:
            faces = Worlds.DiscardEncounterCards(1, effect)
            if faces and EstTraitrise(faces[0]):
                RetournerVeranke(effect)

    def vaincue(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        RetirerSoupcons(effect, "All")

    capacites = [AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Villain", fin_de_phase)]
    if stade < 3:
        capacites.append(AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincue))
    return capacites


# ---------------------------------------------------------------------------------------------------------------------
# Paiement en groupe (livret : « The players can pay this ability's costs as a group », interdit par Mistrust and Paranoia)
# ---------------------------------------------------------------------------------------------------------------------
def PaiementEnGroupeAutorise(effect: 'Effect') -> bool:
    """Faux tant qu'une carte portant `interdit_paiement_en_groupe` est en jeu (Mistrust and Paranoia, sk201)."""
    from game.ability.factory.resources import PaiementEnGroupeInterdit
    return not PaiementEnGroupeInterdit(effect.world)


# ---------------------------------------------------------------------------------------------------------------------
# Compteurs de SKRULL / d'IMPOSTOR (complots principaux, Chaos on the Battlefield)
# ---------------------------------------------------------------------------------------------------------------------
def EnnemisSkrull(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.GetOnFieldCards(effect)
            if Enemy.IsType(f) and f.IsInPlay() and f.HasTrait("SKRULL")]


def AlliesImpostor(effect: 'Effect') -> List['CardFace']:
    return [a for a in Worlds.GetOnFieldAllies(effect) if a.HasTrait("IMPOSTOR")]


def ScHTotalImpostors(effect: 'Effect') -> int:
    """« the total SCH of all IMPOSTOR characters in play » : le SCH imprime des allies (lu sur la face sbire)
    + le SCH courant des sbires."""
    total = sum(SchAllie(a) for a in AlliesImpostor(effect))
    total += sum(m.scheme for m in SbiresImpostor(effect))
    return total
