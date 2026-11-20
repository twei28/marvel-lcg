from cards.pack import *

# ===========================================================================
# Pack HELLFIRE HUNT - SCENARIO 5 « CASSANDRA NOVA » (campagne Hellfire Hunt, « MC Custom Content By: Dipsome »), 01/11/2026.
# Prefixe `hf` (tools/prefixes_fanmade.json), set 245. Module PLAT : `cards.pack.hellfire_hunt_cassandra_nova.<card_id>`
# (modele : pack hellfire_hunt_white_queen). Tout helper appele par une carte vit ICI (NameError avale par le moteur sinon, lecon hk005).
#
# card_id : hf601-hf621 = scenario (600 + numero du scan ; 4A/4B = hf604a/hf604b...), hf371-hf376 = module Mind Control, hf381-hf388 = module
# Mutant Extinction Agenda. Le module Immensity (hf351-hf358) appartient a l'agent de Torn (set 244) : le scenario n'y fait que renvoyer.
#
# LE SCENARIO EN UNE PHRASE : Cassandra Nova pose des compteurs « Cassandra Controls » sur l'IDENTITE de chaque joueur (a chacune de ses
# activations contre lui, et par ses cartes) ; a 3 compteurs, l'environnement Cassandra Domination les retire et impose un choix a trois
# branches ; les trois complots principaux (face B) font choisir, a chaque fin de tour d'un joueur controle, entre de la menace et une
# penalite, et offrent une Action de heros pour retirer un compteur en defaussant 5 / 6 / 7 cartes du deck de rencontre.
# ===========================================================================

NOM_CN = "Cassandra Nova"
ENSEMBLE_CN = "Cassandra Nova"            # `set_name` des cartes hf601-hf621 (« a Cassandra Nova card »)
CTR = 'cassandra_controls'                # compteur « Cassandra Controls » (card_face.py, COUNTER)
SENTINEL = "SENTINEL"
NOM_DOMINATION = "Cassandra Domination"
ID_DOMINATION = "hf607"

LIB_MENACE = "Place 2 threat on each scheme"
LIB_STATUTS = "Stun and confuse your identity"
LIB_DEGATS = "Deal 3 indirect damage to another friendly character"


# ---------------------------------------------------------------------------------------------------- les compteurs sur l'identite
def VilainCN(effect: 'Effect') -> 'Villain|None':
    """Le VILAIN Cassandra Nova en jeu (jamais le sbire homonyme du module Immensity)."""
    for v in Worlds.GetVillains(effect):
        if v.IsName(NOM_CN):
            return v
    return None


def Controles(joueur: 'Player') -> int:
    """Le nombre de compteurs « Cassandra Controls » sur l'identite du joueur."""
    return joueur.GetIdentity().GetCounters(CTR)


def PoserControle(effect: 'Effect', joueur: 'Player', n: int = 1) -> None:
    """« place N Cassandra Controls counter on your identity (card) »."""
    if n > 0:
        Faces.PlaceCountersOn([joueur.GetIdentity()], n, CTR, effect)


def RetirerControle(effect: 'Effect', joueur: 'Player', n: int = 1) -> int:
    return Faces.RemoveCountersOn([joueur.GetIdentity()], n, CTR, effect) or 0


def TotalControlesEnJeu(effect: 'Effect') -> int:
    """« For each Cassandra Controls counter in play » : toutes les identites."""
    return sum(Controles(j) for j in Worlds.GetPlayers(effect))


def EstUneIdentite(face: 'CardFace') -> bool:
    return Identity.IsType(face)


# ---------------------------------------------------------------------------------------------------- Cassandra Domination (hf607)
def AutresPersonnagesAmis(effect: 'Effect', joueur: 'Player') -> 'List[CardFace]':
    """« another friendly character » : les alliés et les AUTRES identités en jeu (FAQ p.22 : « you cannot damage yourself »)."""
    identite = joueur.GetIdentity()
    return [f for f in Worlds.GetOnFieldFriendlyCharacters(effect) if f is not identite and f.IsInPlay()]


def Domination(effect: 'Effect', joueur: 'Player') -> None:
    """« remove 3 Cassandra Controls counter from it -> you choose one : place 2 threat on each scheme, stun and confuse your identity,
    or deal 3 indirect damage to another friendly character. » FAQ du livret p.22 : les options impossibles DISPARAISSENT (pas assez de PV chez
    les AUTRES personnages amis pour absorber 3 degats ; identite deja etourdie OU desorientee) ; il ne reste alors que les autres, la menace
    en dernier recours."""
    this = effect.this
    identite = joueur.GetIdentity()
    Faces.RemoveCountersOn([identite], 3, CTR, effect)
    autres = AutresPersonnagesAmis(effect, joueur)
    peut_degats = sum(max(0, f.health) for f in autres) >= 3
    peut_statuts = not (identite.HasStatus("Stunned") or identite.HasStatus("Confused"))

    def menace(cibles: Sequence['CardFace']) -> None:
        this.PlaceThreatOnSchemes("EachScheme", 2, effect)

    def statuts(cibles: Sequence['CardFace']) -> None:
        Faces.GiveStatus([identite], "Stunned", effect)
        Faces.GiveStatus([identite], "Confused", effect)

    def degats(cibles: Sequence['CardFace']) -> None:
        joueur.AssignDamage(autres, this, 3, effect)

    joueur.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(LIB_MENACE, menace),
        AbilityFactory.ForChoiceAbility(LIB_STATUTS, statuts, condition=peut_statuts),
        AbilityFactory.ForChoiceAbility(LIB_DEGATS, degats, condition=peut_degats),
        forced=True,
    )


# ---------------------------------------------------------------------------------------------------- les complots principaux (faces B)
def ReponseFinDeTour(menace: int, libelle: str, autre: 'Callable[[Effect, Player], None]',
                     possible: 'Callable[[Player], bool]|None' = None) -> 'Ability':
    """Les trois faces B : « Forced Response : After your turn ends, if there is Cassandra Controls counter on your identity, you must choose
    to either place N threat here or <penalite>. » `possible` : l'option « penalite » disparait si elle est impossible (main vide...)."""
    def a_un_compteur(effect: 'Effect', message: 'Message.AfterPlayerTurnEnd') -> bool:
        joueur = message.GetToPlayer()
        return joueur is not None and not joueur.is_eliminated and Controles(joueur) > 0

    def fin_de_tour(effect: 'Effect', message: 'Message.AfterPlayerTurnEnd') -> None:
        this = effect.this.CastTo(MainScheme)
        joueur = message.GetToPlayer()

        def poser(cibles: Sequence['CardFace']) -> None:
            Faces.PlaceTokensOn([this], menace, 'threat', effect)

        def penalite(cibles: Sequence['CardFace']) -> None:
            autre(effect, joueur)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Place %d threat here" % menace, poser),
            AbilityFactory.ForChoiceAbility(libelle, penalite, condition=(possible(joueur) if possible else True)),
            forced=True,
        )

    return AbilityFactory.AfterPlayerTurnEnd(AbilityType.ForcedResponse, "AnyPlayer", fin_de_tour, conditions=[a_un_compteur])


def ActionRetirerControle(cartes: int) -> 'Ability':
    """Les trois faces B : « Hero Action : Discard N cards from the top of the encounter deck -> remove a Cassandra Controls counter from your
    identity. (Limit once per round per player.) » Le cout est la defausse (modele gb006b : `CostFunc.DiscardDeckTopCards`) ; sans compteur sur
    l'identite l'action n'est pas proposee (elle ne changerait rien)."""
    def retirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        RetirerControle(effect, message.GetToPlayer(), 1)

    def a_un_compteur(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        joueur = message.GetToPlayer()
        return joueur is not None and Controles(joueur) > 0

    return (AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, retirer, conditions=[a_un_compteur])
            .SetCostFunc(CostFunc.DiscardDeckTopCards("EncounterDeck", cartes))
            .LimitOncePerRoundPerPlayer())


def PenaliteDegats(effect: 'Effect', joueur: 'Player') -> None:
    joueur.GetIdentity().TakeDamage(effect.this, 2, effect)


def PenaliteCarteRencontre(effect: 'Effect', joueur: 'Player') -> None:
    joueur.DealEncounterCards(1, effect)


def PenaliteDefausse(effect: 'Effect', joueur: 'Player') -> None:
    joueur.DiscardHandCards((1, 1), effect)


def MainNonVide(joueur: 'Player') -> bool:
    return joueur.hand_cards.GetSize() > 0


def PersonnagesControles(joueur: 'Player') -> int:
    """« each character they control » (hf606a) : l'identite et les allies."""
    return 1 + len(joueur.allies.Get())


# ---------------------------------------------------------------------------------------------------- les trois stades du vilain (hf601-hf603)
def ReponseControle() -> 'Ability':
    """« [star] Forced Response : After Cassandra Nova activates against you, place 1 Cassandra Controls counter on your identity card. »"""
    def apres_activation(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        joueur = message.GetAgainstPlayer()
        if joueur is not None:
            PoserControle(effect, joueur, 1)

    return AbilityFactory.AfterEnemyActivatesAgainstYou(AbilityType.ForcedResponse, "This", apres_activation)


def controle_sur_chaque_identite(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
    """« When Revealed : Place 1 Cassandra Controls counter on each identity. » (dans l'ordre des joueurs)"""
    for joueur in Worlds.GetPlayers(effect):
        PoserControle(effect, joueur, 1)


def controle_et_acceleration(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
    """Stade III : « ... and place 1[per_hero] acceleration tokens on the main scheme. »"""
    controle_sur_chaque_identite(effect, message)
    complot = Worlds.FindMainScheme(effect)
    if complot is not None:
        complot.CastTo(MainScheme).PlaceAccelerationToken(len(Worlds.GetPlayers(effect)), effect)


# ---------------------------------------------------------------------------------------------------- Exploding Their Head (hf608, hf609)
def CartesControlees(joueur: 'Player') -> 'List[CardFace]':
    """« cards you control » : allies, ameliorations et soutiens du joueur, avec un cout imprime."""
    return [f for f in joueur.GetControlCardsByType(ally=True, upgrade=True, support=True) if getattr(f, "has_printed_cost", False)]


def ObligationExploding() -> 'List[Ability]':
    def fin_de_tour(effect: 'Effect', message: 'Message.AfterPlayerTurnEnd') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetToPlayer()
        disponibles = CartesControlees(joueur)
        if sum(f.printed_cost.val for f in disponibles) >= 2:
            choisies: List['CardFace'] = []
            cout = 0
            while cout < 2 and disponibles:
                face = joueur.AskChooseFace(disponibles, effect, prompt="Discard (total resource cost at least 2)")
                if face is None:
                    break
                disponibles.remove(face)
                choisies.append(face)
                cout += face.printed_cost.val
            Faces.DiscardAll(choisies, effect)
            joueur.GetIdentity().TakeDamage(this, len(choisies), effect)
            Faces.DiscardAll([this], effect)
        else:
            joueur.DealEncounterCards(1, effect)

    def peril(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        face = message.trigger
        if EncounterNonVillainCard.IsType(face):
            face.GainPeril(1, effect)

    return [
        # « Each encounter card you revealed gains peril » : posee AVANT la resolution de la carte, au moment ou elle est revelee PAR le porteur de
        # l'obligation (`GiveKeywordToInPlayWhenApplyThis(control_by="You")` ne lit pas le joueur qui revele : mesure du 01/11/2026).
        AbilityFactory.WhenPlayerRevealCard(AbilityType.ForcedInterrupt, "AttachedPlayer", EncounterNonVillainCard, None, peril),
        AbilityFactory.AfterPlayerTurnEnd(AbilityType.ForcedResponse, "AttachedPlayer", fin_de_tour),
    ]


# ---------------------------------------------------------------------------------------------------- module Mind Control
def JoueurQuiRetire(message: 'Message.WhenSchemeWouldRemoveThreat') -> 'Player|None':
    """« that player » (hf372) : le joueur qui retire la menace : celui qui controle le personnage qui poursuit, sinon l'initiateur de l'effet."""
    poursuit = message.would_thw_message
    if poursuit is not None:
        joueur = poursuit.trigger.GetControlByOrOwner()
    else:
        joueur = message.by_effect.initiator
    return joueur if Player.IsType(joueur) else None


# ---------------------------------------------------------------------------------------------------- module Mutant Extinction Agenda
SENTINELLE = CardFinder(traits=[SENTINEL], card_type=Minion)


def MettreUneSentinelle(effect: 'Effect', joueur: 'Player') -> 'Minion|None':
    """« search the encounter deck and discard pile for a SENTINEL minion ... Put it into play engaged with you » (hf381, hf386, hf388)."""
    sbire = Search.EncounterCard(effect, joueur, include_discard_pile=True, trait=SENTINEL, card_type=Minion)
    if sbire is not None:
        sbire.PutIntoPlay(joueur, effect)
    return sbire


def UneSentinelleParJoueur(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
    """« Each player search ... for a SENTINEL minion in player order. Put it into play engaged with you. » (hf381, hf388)."""
    for joueur in Worlds.GetPlayers(effect):
        MettreUneSentinelle(effect, joueur)


def NombreDeSentinelles(effect: 'Effect') -> int:
    return len(Worlds.FindCardsOnField(effect, card_type=Minion, trait=SENTINEL))


def SentinelleSauvage() -> 'List[Ability]':
    """Wild Sentinel (hf382-hf385)."""
    def vaincue(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this
        joueur = message.defeating_player
        if joueur is None:
            return

        def degats(cibles: Sequence['CardFace']) -> None:
            joueur.GetIdentity().TakeDamage(this, 2, effect)

        def dessous(cibles: Sequence['CardFace']) -> None:
            this.bas_du_deck = True

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Take 2 damage", degats),
            AbilityFactory.ForChoiceAbility("Place this card on the bottom of the encounter deck instead of the discard pile", dessous),
            forced=True,
        )

    def a_defausser(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
        this = effect.this
        this.bas_du_deck = False
        message.SetBeInstead(effect)
        this.card.MoveToBottom(Worlds.GetEncounterDeck(effect), effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
        AbilityFactory.WhenCardWouldDiscard(AbilityType.ForcedInterrupt, "This", a_defausser,
                                            conditions=[lambda effect, message: getattr(effect.this, "bas_du_deck", False)]),
    ]
