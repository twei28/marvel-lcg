from cards.pack import *

# ===========================================================================
# Scenario 2 MAJESTRIX'S VERDICT (Galactic Storm, Kajislav) — helpers partages
# (gs114-gs137). Lot GS-5, 20/10/2026.
#
# Regle propre (insert du scenario et livret 1.2 p.12, « Chandilar Prison ») :
#  - les allies STARJAMMER (Lilandra, Ch'od, Corsair, Hepzibah, Korvus, Raza)
#    commencent la partie GLISSES sous la manigance annexe Imprisoned on
#    Chandilar (Setup de 1A). « Tuck » = face VISIBLE sous l'autre carte, hors
#    jeu (livret p.4) : `PlaceCardHere(faces, True, effect)`, PAS
#    `TuckCardUnderHere` qui pose face cachee (modele officiel Abduct
#    Superhumans 50081).
#  - quand la derniere menace quitte la prison, les joueurs mettent en jeu un
#    allie glisse sous le controle de n'importe quel joueur, puis 6 menaces
#    reviennent (Interruption forcee de gs119, modele 50088b) ;
#  - un STARJAMMER qui quitte le jeu y est glisse a nouveau (Reponse forcee de
#    gs119) ; un allie RETIRE DE LA PARTIE (execution de 2A) ne revient pas :
#    une carte retiree de la partie n'est plus atteignable ;
#  - « If Lilandra is removed from the game, the players lose the game » :
#    `RetirerDeLaPartie` (2A, Lilandra glissee) et la capacite de gs121
#    (Lilandra en jeu).
# ===========================================================================

PRISON = "Imprisoned on Chandilar"
TRONE = "Shi'ar Throne"
LILANDRA = "Lilandra"
DEATHBIRD = "Deathbird"
STARJAMMER = "STARJAMMER"


def EnJeu(effect: 'Effect', nom: str, type_carte: Any) -> 'Any':
    """`FindCardOnField` voit aussi les cartes GLISSEES sous une carte en jeu (zone `PlaceCardArea`, hors jeu) :
    une Lilandra glissee passait pour « en jeu » (mesure du 20/10/2026, Sister's Deception). On exige IsInPlay."""
    for face in Worlds.FindCardsOnField(effect, name=nom, card_type=type_carte):
        if face.IsInPlay():
            return face
    return None


def Prison(effect: 'Effect') -> 'SchemeSide2|None':
    return EnJeu(effect, PRISON, SchemeSide2)


def EstStarjammer(face: 'CardFace') -> bool:
    return Ally.IsType(face) and face.HasTrait(STARJAMMER)


def Glisses(prison: 'CardFace|None') -> List['CardFace']:
    """Les allies STARJAMMER glisses sous la prison (zone `PlaceCardArea`, hors jeu)."""
    if prison is None:
        return []
    return [f for f in prison.GetPlacedCardArea().GetAll() if EstStarjammer(f)]


def GlissesSousLaPrison(effect: 'Effect') -> List['CardFace']:
    return Glisses(Prison(effect))


def Glisser(prison: 'CardFace', faces: Sequence['CardFace'], effect: 'Effect') -> bool:
    """« Tuck » (livret p.4) : la carte glissee est FACE VISIBLE sous l'autre."""
    faces = list(faces)
    if not faces:
        return False
    return prison.PlaceCardHere(faces, True, effect)


def StarjammersEnJeu(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.GetOnFieldAllies(effect) if f.HasTrait(STARJAMMER) and f.IsInPlay()]


def StarjammersDe(joueur: 'Player') -> List['CardFace']:
    return [f for f in joueur.GetControlAllies() if f.HasTrait(STARJAMMER)]


def LilandraEnJeu(effect: 'Effect') -> 'Ally|None':
    return EnJeu(effect, LILANDRA, Ally)


def TroneSoutienEnJeu(effect: 'Effect') -> 'Support|None':
    return EnJeu(effect, TRONE, Support)


def DeathbirdEnJeu(effect: 'Effect') -> 'Villain|None':
    return EnJeu(effect, DEATHBIRD, Villain)


def JoueursControlentLilandraEtTrone(effect: 'Effect') -> bool:
    """« if players do not control Lilandra and the Shi'ar Throne support » : les deux cartes en jeu, chacune
    sous le controle d'UN joueur (pas forcement le meme)."""
    lilandra = LilandraEnJeu(effect)
    trone = TroneSoutienEnJeu(effect)
    if lilandra is None or trone is None:
        return False
    return lilandra.GetControlBy() is not None and trone.GetControlBy() is not None \
        and lilandra.GetControlBy().IsPlayer() and trone.GetControlBy().IsPlayer()


def EstLilandra(face: 'CardFace') -> bool:
    return Ally.IsType(face) and face.name == LILANDRA


def RetirerDeLaPartie(faces: Sequence['CardFace'], effect: 'Effect') -> List['CardFace']:
    """Retire de la partie ; « If Lilandra is removed from the game, the players lose the game »."""
    retirees = Faces.RemoveAllFromGame(list(faces), effect)
    if any(EstLilandra(f) for f in retirees):
        Worlds.SetGameOver(False, effect)
    return retirees


def RevelerLeTrone(face: 'CardFace', effect: 'Effect') -> 'CardFace|None':
    """Shi'ar Throne : « flip this card and reveal it » (face B -> face A, manigance annexe revelee, qui entre en
    jeu avec ses 3[per_hero] menaces). Le soutien encore en jeu (Lilandra vient de partir) quitte d'abord la
    table (mis de cote) : sa face A doit ENTRER en jeu par la revelation, pas rester dans la zone du joueur.
    Rien si le Trone est deja une manigance en jeu."""
    card = face.card
    if Support.IsType(card.face):
        if card.face.IsInPlay():
            Faces.SetAside([card.face], effect)
        if Support.IsType(card.face):
            card.Flip(effect, call_reveal=False)
    manigance = card.face
    if SchemeSide2.IsType(manigance) and not manigance.IsInPlay():
        manigance.Reveal(None, effect)
        return manigance
    return None


def ChoisirEnGroupe(effect: 'Effect', faces: Sequence['CardFace'], nombre: int) -> List['CardFace']:
    """« The players as a group choose » : le premier joueur tranche (convention du moteur, Filter.One)."""
    faces = list(faces)
    if len(faces) <= nombre:
        return faces
    joueur = Worlds.GetFirstPlayer(effect)
    return list(joueur.AskChooseFaces(faces, (nombre, nombre), effect, not_move=True))


def MettreEnJeuSousControle(effect: 'Effect', allie: 'CardFace') -> bool:
    """« put that ally into play under any player's control » : le premier joueur designe l'identite
    (`Worlds.FindPlayer(None, ..)`, modele officiel 50088b Locate Missing Person ; en solo, lui-meme)."""
    joueur = Worlds.FindPlayer(None, effect) or Worlds.GetFirstPlayer(effect)
    # ⚠ Une carte qui ENTRE en jeu depuis une `PlaceCardArea` n'est PAS remise a zero par le moteur
    # (card.py, « Fix 39035 » : on garde l'etat d'une carte rangee sous une autre). Or les STARJAMMER sont
    # glisses directement depuis la reserve du scenario, ou leurs mots-cles n'ont jamais ete calcules :
    # sans ce Reset, l'allie entrait en jeu avec ATQ 0, Riposte 0, sans Toughness (mesure du 20/10/2026,
    # « s'apprete a infliger 0 degat », Raza sans carte Tenace). Reset = ce que fait `Reveal` pour une carte
    # hors jeu (face_on_event.py) ; les degats, eux, sont remis a zero par l'entree en jeu.
    allie.Reset(False)
    return bool(allie.CastTo(Ally).PutIntoPlay(joueur, effect, under_control=True))


def AttaqueDetourneeVersStarjammer(bonus_atq: int = 0, boost_sup: int = 0) -> 'Ability':
    """Deathbird I/II/III : « Forced interrupt: When Deathbird initiates an attack against you, if you control a
    STARJAMMER ally, she attacks that ally instead [with +1 ATK | give her 1 additional boost card] ».
    Modele officiel 50089b Extract Captives (`message.ReplaceTarget(allie)` sur `WhenUnitWouldAttack`).
    « against YOU » : l'attaque vise l'identite d'un joueur (pas une attaque deja dirigee vers un allie) ;
    « that ally » : un STARJAMMER que CE joueur controle, choisi par lui s'il en a plusieurs."""

    def joueur_vise(message: 'Message.WhenUnitWouldAttack') -> 'Player|None':
        joueur = message.against_player
        if joueur is None:
            return None
        identite = joueur.GetIdentity()
        if identite not in message.attacked_targets:
            return None
        return joueur

    def possible(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        joueur = joueur_vise(message)
        return joueur is not None and bool(StarjammersDe(joueur))

    def detourner(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = joueur_vise(message)
        if joueur is None:
            return
        allies = StarjammersDe(joueur)
        if not allies:
            return
        allie = allies[0] if len(allies) == 1 else joueur.AskChooseFace(allies, effect)
        if allie is None:
            return
        message.ReplaceTarget(allie)
        if bonus_atq:
            if message.IsBasicAttack():
                message.GainATKForThisAttack(bonus_atq, effect)
            else:
                message.DealAdditionalDamage(bonus_atq, effect)
        if boost_sup:
            message.GiveAdditionalBoostCardForThisActivation(boost_sup, effect)

    return AbilityFactory.WhenUnitWouldAttack(
        AbilityType.ForcedInterrupt,
        "This",
        detourner,
        conditions=[possible],
    )


def DeathbirdInvaincue() -> List['Ability']:
    """Deathbird II/III : « Deathbird cannot be defeated, if players do not control Lilandra and the Shi'ar
    Throne support. » Modele 50129a Citizen V (`UnitCannotBeDefeatedWhile`) ; `change_on_event` relance la
    defaite des que la condition tombe (Lilandra ou le Trone passe sous controle, Deathbird a 0 PV).
    ⚠ `change_on_event` de la fabrique ne relance la defaite que TANT QUE `condition` est vraie (defeated.py,
    `new_condition` : « if not condition(effect): return False »), c'est-a-dire jamais au moment ou elle tombe
    (mesure du 20/10/2026 : Deathbird restait a 0 PV apres l'arrivee du Trone). On ecrit donc la relance a part,
    sur le meme evenement, avec la condition INVERSE."""

    def relancer(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Unit2)
        if this.IsInPlay() and this.health <= 0:
            this.Defeated(None, effect)

    return [
        *AbilityFactory.UnitCannotBeDefeatedWhile(
            AbilityType.NonKeyword,
            "This",
            condition=lambda effect: not JoueursControlentLilandraEtTrone(effect),
        ),
        *Condition.GetEventAbilities(
            OnEvent.PlayAreaCard(CardFinder(name=LILANDRA) | CardFinder(name=TRONE)),
            AbilityType.NonKeyword,
            lambda effect, message: JoueursControlentLilandraEtTrone(effect),
            relancer,
        ),
    ]


def AttacherALilandra(ressource: str) -> 'Ability':
    """Royal Cape / Shi'ar Crest / Shi'ar Javelin : « Response: After Lilandra attacks Deathbird, spend a [x]
    resource → attach this card to Lilandra. » Modele 07035 Distracting Taunts (`AfterUnitAttackUnit` +
    `SetCost`) ; n'importe quel joueur peut payer (carte de rencontre, modele 32173b `AnyPlayerCanDoThis`)."""

    def attacher(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Attachment)
        lilandra = LilandraEnJeu(effect)
        if lilandra is not None:
            this.AttachTo2(lilandra, effect)

    def pas_deja_sur_lilandra(effect: 'Effect', message: 'Message2') -> bool:
        hote = effect.this.GetBindFace()
        return hote is None or not EstLilandra(hote)

    return AbilityFactory.AfterUnitAttackUnit(
        AbilityType.Response,
        CardFinder(name=LILANDRA, card_type=Ally),
        CardFinder(name=DEATHBIRD, card_type=Villain),
        attacher,
        conditions=[pas_deja_sur_lilandra],
    ).SetCost(Cost(ressource)).AnyPlayerCanDoThis()


def ApresEtapeUn() -> 'Ability':
    """1B et 2B : « Forced Response: After resolving step one of the villain phase, place 2 threat on Imprisoned
    on Chandilar for each player in alter-ego form. » Modele 04096b (`AfterResolveVillainPhaseStep(.., 1, ..)`)."""

    def poser(effect: 'Effect', message: 'Message2') -> None:
        prison = Prison(effect)
        if prison is None:
            return
        n = sum(1 for j in Worlds.GetPlayers(effect) if j.IsAlterEgo())
        if n:
            effect.this.PlaceThreatOnSchemes([prison], 2 * n, effect)

    return AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, poser)


def MenaceSurLaPrisonParJoueur() -> 'Ability':
    """1B et 2B : « When Revealed: Place 1[per_hero] threat on Imprisoned on Chandilar. »"""

    def poser(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        prison = Prison(effect)
        if prison is not None:
            effect.this.PlaceThreatOnSchemes([prison], "1*", effect)

    return AbilityFactory.WhenThisRevealed(None, poser)
