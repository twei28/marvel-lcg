from cards.pack import *

# Fabriques partagees du pack custom « Squirrel Girl » (75xxx).
#
# Le pack tourne autour d'un DECK ECUREUIL de six allies mis de cote au setup,
# monte comme le deck d'invocation de Doctor Strange (09001b) : les cartes
# vivent dans `additional_deck` / `additional_discard_pile` et n'entrent jamais
# ni dans le deck ni dans la main du joueur.
#
# Deux notions maison, toutes deux resolues ici :
#   - APPELER un ecureuil  : reveler le dessus du deck ecureuil et le mettre en
#     jeu epuise (pret si la carte le precise).
#   - DEPENSER un ecureuil : le defausser pour generer 1 ressource utilisable
#     uniquement sur une carte du set. C'est la traduction moteur de la
#     « reduction de cout de 1 » du materiel d'origine : meme effet a la table,
#     et le moteur sait alors dire « si tu as depense un ecureuil » via le
#     message WhenCardBeSpendAsResource. Ecart documente au §9.

SET_HERO = "Squirrel Girl"
SET_ECUREUILS = "Squirrel Deck"
ID_ECUREUILS = ["sg002", "sg003", "sg004", "sg005", "sg006", "sg007"]

NOM_DISCORDE = "Discord in the Branches"
NOM_CHUCHOTEMENTS = "Ratatoskr's Whispers"


################################################################################
# Etat partage
#
def _Cle(joueur: 'Player', nom: str) -> str:
    return f"SquirrelGirl {nom} P{joueur.player_id}"


def MarquerDepensePour(joueur: 'Player', face_payee: 'CardFace|None', effect: 'Effect') -> None:
    """Retient la carte pour laquelle un ecureuil vient d'etre depense.

    Sert deux regles a la fois : « si tu as depense un ecureuil pour jouer
    cette carte » (les trois evenements du set) et la limite d'UN ecureuil par
    carte jouee, verifiee par `DepenseDejaFaitePour`.
    """
    effect.world.store.SetFace(_Cle(joueur, "DepensePour"), face_payee)

    # La marque ne doit pas survivre a la phase : une amelioration ou un
    # soutien reste en jeu apres avoir ete paye, et sans nettoyage il resterait
    # a jamais impossible de depenser un ecureuil pour cette meme carte.
    def oublier() -> None:
        effect.world.store.SetFace(_Cle(joueur, "DepensePour"), None)

    RunAt.TheEndOfThePhase(effect, oublier)


def DepenseDejaFaitePour(joueur: 'Player', face_payee: 'CardFace|None',
                         effect: 'Effect') -> bool:
    """Un ecureuil a-t-il deja ete depense pour CETTE carte ?

    « Only 1 Squirrel can be spent this way for each card played. » Le moteur
    n'a aucune limite de ce genre : les limites de capacite (`LimitOncePer...`)
    comptent par capacite, or chaque ecureuil porte la sienne, et une limite par
    NOM de carte ne verrait pas non plus six noms differents. La regle est donc
    portee par la marque de depense, comparee a la carte en cours de paiement.
    """
    if face_payee is None:
        return False
    cle = _Cle(joueur, "DepensePour")
    if not effect.world.store.HasKey(cle):
        return False
    return effect.world.store.GetFace(cle) is face_payee


def ADepenseUnEcureuil(effect: 'Effect') -> bool:
    """« If you spent a Squirrel to play this card ». Consomme la marque."""
    joueur = effect.GetInitiator()
    if joueur is None:
        return False
    cle = _Cle(joueur, "DepensePour")
    if not effect.world.store.HasKey(cle):
        return False
    face = effect.world.store.GetFace(cle)
    if face is not effect.this:
        return False
    effect.world.store.SetFace(cle, None)
    return True


def DepensePourCarteSquirrelGirl(effect: 'Effect') -> bool:
    """L'ecureuil qu'on vient de depenser paie-t-il une carte Squirrel Girl ?

    Depuis le 28/08/2026, « Squirrel Aid » paie N'IMPORTE QUELLE carte (patron
    officiel de Reed Richards mf001b : ressource universelle, bonus reserve a
    une famille). Ce sont les BONUS qui portent desormais la restriction :
    Unbeatable Army, The Forager et The Gatherer ne se declenchent que si
    l'ecureuil a servi a payer une carte du set.

    Lecture SEULE, contrairement a `ADepenseUnEcureuil` : la marque doit
    survivre pour les bonus imprimes sur les cartes elles-memes (Squirrel
    Swarm, Recon Team, Unbeatable!), qui la consomment plus tard.
    """
    joueur = effect.GetInitiator()
    if joueur is None:
        return False
    cle = _Cle(joueur, "DepensePour")
    if not effect.world.store.HasKey(cle):
        return False
    return EstCarteSquirrelGirl(effect.world.store.GetFace(cle))


################################################################################
# Le set SQUIRREL GIRL
#
def EstCarteSquirrelGirl(face: 'CardFace|None') -> bool:
    return face is not None and face.paper.set_name in (SET_HERO, SET_ECUREUILS)


def FinderCarteSquirrelGirl() -> 'CardFinder':
    return CardFinder(set_name=SET_HERO)


################################################################################
# Discord in the Branches (sg020) : capacites imprimees traitees comme blanches
#
# Le moteur ne sait rendre blanche qu'une face designee, pas une famille entiere
# avec exception. La condition est donc portee par chaque capacite d'ecureuil.
# Si un septieme ecureuil est ajoute un jour, ne pas oublier de la recopier.
#
def DiscordeEnJeu(effect: 'Effect') -> bool:
    return Worlds.FindCardOnField(effect, name=NOM_DISCORDE) is not None


def PasDeDiscorde(effect: 'Effect', message: 'Message2') -> bool:
    return not DiscordeEnJeu(effect)


################################################################################
# Les ecureuils en jeu
#
def EcureuilsControles(effect: 'Effect', joueur: 'Player') -> List['CardFace']:
    return [face for face in Worlds.FindCardsOnField(effect, trait='SQUIRREL')
            if face.GetControlByPlayer() == joueur]


def _EstSourceEtrangere(effect: 'Effect') -> bool:
    """Vrai si l'effet vient d'une carte JOUEUR exterieure au set.

    Les cartes rencontre et les regles du moteur passent : la nemesis doit
    pouvoir defausser un ecureuil, et un ecureuil doit pouvoir etre attaque.
    """
    from game.card.face.base import PlayerCard
    source = effect.this
    if source is None:
        return False
    if EstCarteSquirrelGirl(source):
        return False
    return PlayerCard.IsType(source)


def PreparerEcureuil(face: 'CardFace', joueur: 'Player') -> None:
    """Regles permanentes d'un ecureuil, posees au setup sur les six cartes."""

    def vers_le_deck_ecureuil(effect: 'Effect', message: 'Message.WhenCardWouldMoveToArea') -> None:
        if joueur.discard_pile == message.into_area:
            message.ChangeToArea(joueur.additional_discard_pile, effect)
        if joueur.player_deck == message.into_area:
            message.ChangeToArea(joueur.additional_deck, effect)

    face.effect.Registers(
        AbilityFactory.WhenCardWouldMoveToArea(
            AbilityType.Temp0,
            "This",
            vers_le_deck_ecureuil,
            conditions=[
                lambda effect, message:
                    joueur.discard_pile == message.into_area or
                    joueur.player_deck == message.into_area
            ],
        ),
    )

    # Points d'accroche du moteur (CORRECTIF §9) : hors du set, on ne peut ni
    # choisir un ecureuil, ni lui donner de bonus.
    face.refuse_target_fn = _EstSourceEtrangere
    face.refuse_gain_fn = _EstSourceEtrangere


################################################################################
# Appeler un ecureuil
#
def _NetworkOfTrees(effect: 'Effect', joueur: 'Player') -> 'CardFace|None':
    """Le soutien sg012, en jeu et pret, sinon None."""
    face = Worlds.FindCardOnField(effect, name="Network of Trees")
    if face is None:
        return None
    if face.GetControlByPlayer() != joueur or not face.card.state.is_ready:
        return None
    return face


def AppelerEcureuil(joueur: 'Player', effect: 'Effect', *, pret: bool = False) -> 'CardFace|None':
    """Revele le dessus du deck ecureuil et le met en jeu sous ton controle."""
    if joueur.additional_deck.GetSize() == 0:
        joueur.additional_deck.ShuffleWithDiscardPile(False, effect)

    face = joueur.additional_deck.GetTop()
    if face is None:
        return None

    # Network of Trees (sg012) s'interpose ici : le moteur n'ayant pas de
    # message « quand tu appellerais un ecureuil », l'interruption est resolue
    # dans l'appel lui-meme, seul point de passage de tous les appels.
    reseau = _NetworkOfTrees(effect, joueur)
    if reseau is not None and joueur.additional_deck.GetSize() >= 2:
        deux = list(joueur.additional_deck.Get())[-2:]
        # MayChooseFace et pas un selecteur de cible : les cartes d'un deck ne
        # sont pas en jeu, un selecteur ne les restreint pas (voir le correctif
        # de Tippy-Toe sg002).
        choisi = joueur.MayChooseFace(deux, effect, not_move=True)
        if choisi is not None:
            Faces.ExhaustAll([reseau], effect)
            Faces.MoveAllToDeck([f for f in deux if f is not choisi],
                                joueur.additional_deck, "Bottom", effect)
            face = choisi

    Faces.FlipAllTo([face], True, effect)
    face.CastTo(Ally).PutIntoPlay(joueur, effect, under_control=True, exhaust=not pret)
    return face


def AppelerEcureuils(joueur: 'Player', effect: 'Effect', nombre: int, *, pret: bool = False) -> None:
    for _ in range(nombre):
        AppelerEcureuil(joueur, effect, pret=pret)


################################################################################
# Depenser un ecureuil
#
def PeutDepenser(effect: 'Effect') -> bool:
    """Ratatoskr's Whispers (sg022) interdit toute depense."""
    joueur = effect.GetInitiator() or effect.this.GetControlByPlayer()
    if joueur is None:
        return True
    chuchotements = Worlds.FindCardOnField(effect, name=NOM_CHUCHOTEMENTS)
    if chuchotements is None:
        return True
    return chuchotements.GetControlByPlayer() != joueur


def EcureuilDepense(effect: 'Effect') -> 'CardFace|None':
    """L'ecureuil que la depense en cours est en train de consommer."""
    joueur = effect.GetInitiator()
    if joueur is None:
        return None
    cle = _Cle(joueur, "EcureuilDepense")
    if not effect.world.store.HasKey(cle):
        return None
    return effect.world.store.GetFace(cle)


def CapaciteDepenseIdentite() -> 'Ability':
    """« Resource: Discard a SQUIRREL ally you control → 1 [wild]. »

    La capacite est portee par l'IDENTITE, pas par chaque ecureuil, et c'est ce
    qui donne gratuitement la limite du materiel d'origine : « un seul ecureuil
    par carte jouee ». Le moteur recense les sources de paiement UNE fois, avant
    toute depense, et chaque capacite ne compte que pour une source : avec la
    capacite posee sur les six ecureuils, six sources etaient offertes et rien
    ne pouvait plus les limiter ensuite. Une source qu'on refuserait apres coup
    fait echouer une assertion du moteur (`ProcessPayingEffect`), la limite
    n'est donc PAS exprimable a ce niveau. Ici, une seule source existe, et le
    joueur choisit quel ecureuil elle consomme via le cout.
    """

    def cible_ecureuil(effect: 'Effect', face: 'CardFace') -> bool:
        joueur = effect.GetInitiator()
        return joueur is not None and face.GetControlByPlayer() == joueur

    def depenser(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        faces = list(targets)
        if not faces:
            return False
        joueur = effect.GetInitiator()
        if joueur is not None:
            # Retenu AVANT la defausse : les reponses « apres avoir depense cet
            # ecureuil » (The Gatherer, The Forager) se declenchent sur son
            # depart et ont besoin de savoir que c'est bien une depense.
            effect.world.store.SetFace(_Cle(joueur, "EcureuilDepense"), faces[0])
        Faces.DiscardAll(faces, effect)
        return True

    def marquer(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        MarquerDepensePour(message.GetToPlayer(), message.paying_card, effect)

    # 28/08/2026 : plus de `for_card=FinderCarteSquirrelGirl()`. La ressource
    # paie desormais N'IMPORTE QUELLE carte ; ce sont les bonus (Unbeatable
    # Army, Forager, Gatherer) qui sont reserves aux cartes du set, via
    # `DepensePourCarteSquirrelGirl`. Patron officiel : Reed Richards (mf001b).
    # Motif : une ressource limitee a 15 cartes sur 40 restait le plus souvent
    # inutilisable en main, ce qui rendait les ecureuils frustrants a jouer.
    return (AbilityFactory.CanGenerateResources(
                AbilityType.Resource,
                Resources('G'),
                conditions=[lambda effect, message: PeutDepenser(effect)],
                ex_operation=marquer,
            )
            .SetName("Squirrel Aid")
            .SetCostFunc(CostFunc.Custom(
                CardFinder(card_type=Ally, traits=['SQUIRREL'],
                           check_effect_fn=cible_ecureuil),
                depenser)))


def Ecureuil() -> List['Ability']:
    """Mot-cle maison « Squirrel », commun aux six cartes du deck ecureuil.

    Hors limite d'alliés, ne peut pas defendre, ne peut pas recevoir
    d'amelioration, et peut etre depense. Les deux regles « pas ciblable » et
    « pas renforcable » hors du set ne sont pas des capacites : elles passent
    par les points d'accroche poses dans PreparerEcureuil.
    """
    return [
        *AbilityFactory.ThisNotCountAllyLimit(),
        *AbilityFactory.UnitCannotDefend(
            "This",
            None,
            cannot_trigger_defense_ability=True,
        ),
        *AbilityFactory.UnitCannotHaveUpgradeAttached("This"),
    ]


def ReponseALaDepense(operation) -> 'Ability':
    """« Interrupt: When you spend this Squirrel to pay for a Squirrel Girl
    card, ... »

    La depense n'est plus une capacite de l'ecureuil (voir
    `CapaciteDepenseIdentite`) : elle se lit sur son DEPART du jeu, quand la
    marque de depense le designe.

    28/08/2026 : la ressource etant devenue universelle, l'effet est desormais
    reserve aux cartes du set (choix de l'utilisateur : payer une carte
    d'aspect ne donne QUE la ressource, aucun bonus).
    """

    def c_est_bien_une_depense(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> bool:
        if DiscordeEnJeu(effect):
            return False
        if EcureuilDepense(effect) is not effect.this:
            return False
        return DepensePourCarteSquirrelGirl(effect)

    return AbilityFactory.AfterCardLeavePlay(
        AbilityType.Response,
        "This",
        operation,
        conditions=[c_est_bien_une_depense],
    )
