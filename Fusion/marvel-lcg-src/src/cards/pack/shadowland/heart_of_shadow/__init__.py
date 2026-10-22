from cards.pack.shadowland import *

# ===========================================================================
# Helpers du set HEART OF SHADOW (sl057 a sl071, scenario 3 du pack Shadowland, vilain Krahllak).
#
# Presque toutes les cartes parlent de « your Creeping Corruption » : l'amelioration sl072a/sl072b (set BLACK FLOWER, codee par un autre agent) que CHAQUE
# joueur met en jeu a la mise en place (sl060a). Le moteur n'a pas de lien « carte -> sa Creeping Corruption » : on la RETROUVE par son identifiant et son
# proprietaire. Le compteur s'appelle `corruption` (declare dans `CardFace.COUNTER`). Le retournement a 5 jetons / la defaite de sl072a/b sont le travail de
# CETTE carte-la : ici on ne fait que poser et retirer des jetons, sans jamais regarder le seuil.
# ===========================================================================

CREEPING_CORRUPTION = ["sl072a", "sl072b"]
KRAHLLAK = "Krahllak"


def CreepingCorruptionDe(joueur: 'Player') -> 'CardFace|None':
    """La Creeping Corruption DU joueur (celle qu'il controle), None s'il n'en a pas en jeu. Les deux faces (a et b) sont UNE carte : on lit la face visible."""
    for carte in joueur.GetControlUpgrade():
        if str(carte.paper.card_id) in CREEPING_CORRUPTION:
            return carte
    # Une Creeping Corruption mise en jeu SANS attache (Setup de sl060a) n'est pas dans l'inventaire d'un personnage : on la cherche sur le terrain par proprietaire.
    for carte in Worlds.GetOnFieldCards(joueur.GetGameArea()):
        if str(carte.paper.card_id) in CREEPING_CORRUPTION and carte.card.GetOwner() == joueur:
            return carte
    return None


def PeutPlacerCorruption(joueur: 'Player') -> bool:
    """« Place N corruption counters on your Creeping Corruption » est faisable : il faut en avoir une en jeu."""
    return CreepingCorruptionDe(joueur) is not None


def PlacerCorruption(effect: 'Effect', joueur: 'Player', n: int=1) -> bool:
    """Pose `n` jetons corruption sur la Creeping Corruption du joueur. Rend False (rien pose) s'il n'en a pas."""
    cc = CreepingCorruptionDe(joueur)
    if cc is None:
        return False
    return bool(Faces.PlaceCountersOn([cc], n, 'corruption', effect))


def RetirerCorruption(effect: 'Effect', joueur: 'Player', n: int=1) -> int:
    """Retire jusqu'a `n` jetons corruption de la Creeping Corruption du joueur (« remove 1 corruption counter ») ; rend le nombre retire (0 s'il n'y en a pas)."""
    cc = CreepingCorruptionDe(joueur)
    if cc is None:
        return 0
    return Faces.RemoveCountersOn([cc], n, 'corruption', effect) or 0


def CorruptionOverpowering(joueur: 'Player') -> bool:
    """« Your Creeping Corruption has the OVERPOWERING trait » : sa face b (sl072b) porte le trait ; faux s'il n'en a pas."""
    cc = CreepingCorruptionDe(joueur)
    return cc is not None and cc.HasTrait('OVERPOWERING')


def CoutPlacerCorruption(n: int) -> 'CostFunc.Custom':
    """Le cout « Place N corruption counters on your Creeping Corruption → ... » : le jeton est pose PAR LE COUT (modele iron_man_model_42 `CoutDuReacteur`), et le
    cout est IMPAYABLE sans Creeping Corruption (sinon la capacite resoudrait a vide et le pilote la rejouerait a l'infini)."""
    def payer(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        joueur = effect.GetInitiator()
        return joueur is not None and PlacerCorruption(effect, joueur, n)
    return CostFunc.Custom(None, payer)


def PeutPayerCorruption(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
    """Condition d'offre d'une action dont le cout pose un jeton : le joueur a une Creeping Corruption."""
    Unused(message)
    joueur = effect.GetInitiator()
    return joueur is not None and PeutPlacerCorruption(joueur)


def InterruptMoinsATQ(attaquant: str='This') -> 'Ability':
    """L'Interruption commune de Krahllak (sl057-sl059) et de Retainer (sl068) : « When <X> attacks you, you may place 1 corruption counter on your Creeping
    Corruption. If you do, <X> gets -3 ATK for this attack. » Le joueur attaque ET c'est lui qui decide (« you may ») : on lui pose la question ; sans Creeping
    Corruption il n'y a rien a proposer."""
    def interruption(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = message.GetAgainstPlayer()
        if joueur is None or not PeutPlacerCorruption(joueur):
            return

        def accepter(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            if PlacerCorruption(effect, joueur):
                if message.IsBasicAttack():
                    message.GainATKForThisAttack(-3, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility("Place 1 corruption counter on your Creeping Corruption: -3 ATK for this attack", accepter),
        )

    return AbilityFactory.WhenUnitWouldAttack(AbilityType.Interrupt, attaquant, interruption, against_player="You")


def CartesControleesDefaussables(joueur: 'Player') -> List['CardFace']:
    """« A card you control » en jeu que l'on PEUT defausser : allies, ameliorations (y compris celles des allies) et soutiens du joueur, SANS la Creeping Corruption, qui est
    Permanent (fiche mots-cles/permanent.md : une carte Permanent ne quitte pas le jeu par un effet d'un AUTRE set) : la proposer ferait « defausser » a vide. Ni l'identite, ni la main."""
    allies = [c for c in joueur.GetControlCharacters() if Ally.IsType(c)]
    cartes = allies + list(joueur.GetControlUpgrade()) + list(joueur.supports.Get())
    return [c for c in cartes if str(c.paper.card_id) not in CREEPING_CORRUPTION and not getattr(c, 'permanent', False)]
