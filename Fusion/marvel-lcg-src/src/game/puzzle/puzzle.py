from core import *
from game.card.face import *
from game.card import *
from game.effect.rule import DebugRule
from game.world import *
from game.card.face.card_type import Identity
from game.card.face.base import Unit2
from game.card.face.base import Scheme2
from game.operate.worlds import Worlds

CATEGORY_NAME = "PUZZLE"

class RunPuzzle:

    def __init__(self, world: 'World') -> None:
        self.world = world
        self.debug_rule = DebugRule(world.object_manager.card_dict[0].face)

    CardName = str|Card|CardFace

    def FindOrCreateFace(self, card: CardName) -> 'CardFace':
        if isinstance(card, CardFace):
            return card.card.face
        elif isinstance(card, Card):
            return card.face
        elif type(card) is int:
            return self.world.object_manager.card_dict[card].face
        elif type(card) is str:
            found_card: CardFace|None = None

            player = self.world.GetCurrentPlayer()
            if not found_card:
                found_card = player.player_deck.FindCard(name=card)
            if not found_card:
                found_card = player.discard_pile.FindCard(name=card)

            if found_card:
                return found_card

            for face in Worlds.GetEncounterDeckCards(self.world) + Worlds.GetEncounterDiscardPileCards(self.world):
                if face.IsName(card):
                    return face

            # Dernier recours AVANT de creer : chercher parmi les cartes DEJA EN
            # JEU (identite, vilain, complots, ameliorations posees). Sans cela,
            # une commande visant une carte en jeu fabriquait un doublon detache
            # (sans controleur), et toute action dessus echouait. Indispensable
            # au mode bac a sable, qui agit sur une partie en cours ; sans effet
            # sur les puzzles, qui montent un plateau vierge et n'arrivent donc
            # jamais jusqu'ici.
            for objet in self.world.object_manager.card_dict.values():
                face = objet.face
                if face is not None and face.IsInPlay() and face.IsName(card):
                    return face

            if found_card:
                return found_card
        else:
            assert False, f"{card=}"
        return self.CreateCard(card)

    def CreateCard(self, card_name: str) -> 'CardFace':
        from game.card.factory import CardFactory
        from game.card.face.base import ClassCard
        card = CardFactory.GenerateCard(card_name, self.world.aside_deck, self.world)
        if ClassCard.IsType(card.face):
            player = self.world.GetCurrentPlayer()
            card.SetOwner(player)
        return card.face

    def FindCommandCards(self, *cards: CardName) -> List['CardFace']:
        faces = [self.FindOrCreateFace(x) for x in cards]
        return faces

    ################################################################################
    #
    def CreateEncounterDiscardPile(self, *cards: str):
        from game.card.factory import CardFactory
        villain = Worlds.GetAllVillains(self.world)[0]
        for card in cards:
            CardFactory.GenerateCard(card, villain.encounter_discard_pile, self.world)

    def EmptyEncounterDeck(self):
        """Vide le deck Rencontre, pour le reconstruire carte par carte.

        AJOUTEE AU HARNAIS le 09/09/2026, meme motif que `BeginVillainPhase`
        (pack night_thrasher) : sans elle, `CreateEncounterDeck` AJOUTE ses
        cartes a un deck de scenario deja plein, et aucun cas ne peut donc
        nommer « les 3 cartes du dessus » ni « la carte que le surge va
        reveler ». Deux mesures du pack superior_spider_man en dependaient et
        avaient ete declarees hors de portee du harnais le 08/09/2026 : la
        fouille de `su008` et le surge de `su018`.

        Les cartes sont RETIREES DE LA PARTIE, pas defaussees : une defausse
        polluerait justement la zone que ces deux cas mesurent.
        """
        # ⚠ EN BOUCLE : voir la meme remarque sur `EmptyPlayerDeck`.
        from game.operate.faces import Faces
        for _ in range(50):
            faces = [f for f in Worlds.GetEncounterDeckCards(self.world) if f is not None]
            if not faces:
                return
            Faces.RemoveAllFromGame(faces, DebugRule(faces[0]))

    def CreateEncounterDeck(self, *cards: str):
        from game.card.factory import CardFactory
        villain = Worlds.GetAllVillains(self.world)[0]
        for card in cards:
            CardFactory.GenerateCard(card, villain.encounter_deck, self.world)

    def CreateHandCards(self, *cards: str):
        from game.card.factory import CardFactory
        first_player = self.world.GetFirstPlayer()
        for card in cards:
            CardFactory.GenerateCard(card, first_player.hand_cards, self.world)

    def CreatePlayerDiscardPile(self, *cards: str):
        from game.card.factory import CardFactory
        first_player = self.world.GetFirstPlayer()
        for card in cards:
            CardFactory.GenerateCard(card, first_player.discard_pile, self.world)

    def EmptyPlayerDeck(self):
        """Vide le deck du joueur, pour le reconstruire carte par carte.

        AJOUTEE le 09/09/2026, meme motif que `EmptyEncounterDeck` :
        `CreatePlayerDeck` AJOUTE au deck de depart du heros, elle ne le
        remplace pas. Tout cas qui voulait un deck SANS evenement en avait donc
        un plein — et la mesure de `sm010` Hyper-Agility, qui exige une
        Acceleration « without playing an event », lisait l'inverse de ce
        qu'elle croyait lire (journal du 09/09/2026 : l'Acceleration trouvait
        `sm003` et le pilote la jouait).

        Les cartes sont RETIREES DE LA PARTIE : les defausser les rendrait
        pretes a revenir par un remelange.
        """
        # ⚠ EN BOUCLE, et non en un seul passage : un premier appel n'a retire
        # que 8 des 14 cartes (journal du 09/09/2026), `RemoveAllFromGame`
        # travaillant sur la liste que la zone est en train de modifier.
        from game.operate.faces import Faces
        joueur = self.world.GetFirstPlayer()
        for _ in range(50):
            faces = [f for f in joueur.player_deck.GetAll() if f is not None]
            if not faces:
                return
            Faces.RemoveAllFromGame(faces, DebugRule(faces[0]))

    def CreatePlayerDeck(self, *cards: str):
        from game.card.factory import CardFactory
        first_player = self.world.GetFirstPlayer()
        for card in cards:
            CardFactory.GenerateCard(card, first_player.player_deck, self.world)

    def PutOnAdditionalDeckTop(self, *cards: CardName):
        """Remonte des cartes sur le DESSUS du deck annexe du joueur.

        Un deck annexe — les ecureuils de Squirrel Girl, les invocations de
        Strange — est melange au setup. Sans ce levier, on ne peut pas choisir
        QUELLE carte en sortira, et l'action qui l'appelle est souvent limitee
        a une fois par manche : impossible d'appeler jusqu'a tomber sur la
        bonne. C'est ce qui rendait The Lookout (sg004) intestable, alors que
        les cinq autres ecureuils avaient leur cas (constate le 9/8/2026).
        """
        from game.operate.faces import Faces
        player = self.world.GetFirstPlayer()
        # On cherche la carte DEJA PRESENTE dans le deck annexe, on n'en cree
        # pas une neuve : `FindCommandCards` fabriquerait un exemplaire qui n'a
        # pas recu les regles posees au setup, et le cas testerait une copie
        # inerte au lieu de la vraie carte.
        for card_id in cards:
            for face in list(player.additional_deck.Get()):
                if getattr(face.paper, "card_id", None) == card_id:
                    Faces.MoveAllToDeck([face], player.additional_deck, "Top", DebugRule(face))
                    break

    def CreatePlayerAdditionalDeck(self, *cards: str):
        from game.card.factory import CardFactory
        first_player = self.world.GetFirstPlayer()
        for card in cards:
            CardFactory.GenerateCard(card, first_player.additional_discard_pile, self.world)

    ################################################################################
    #
    def Gain(self, *cards: CardName, call_back: Callable[['CardFace'], None]|None=None):
        player = self.world.GetCurrentPlayer()
        for face in self.FindCommandCards(*cards):
            player.GainCard(face, self.debug_rule)
            if call_back:
                call_back(face)

    def Draw(self, num: int):
        player = self.world.GetCurrentPlayer()
        effect = DebugRule(player.GetIdentity())
        player.DrawUp(num, effect)

    ################################################################################
    # Card
    def Ready(self, *cards: CardName):
        from game.operate.faces import Faces
        faces = self.FindCommandCards(*cards)
        Faces.ReadyAll(faces, DebugRule(faces[0]))

    def Exhaust(self, *cards: CardName):
        from game.operate.faces import Faces
        faces = self.FindCommandCards(*cards)
        Faces.ExhaustAll(faces, DebugRule(faces[0]))

    def Discard(self, *cards: CardName):
        from game.operate.faces import Faces
        faces = self.FindCommandCards(*cards)
        Faces.DiscardAll(faces, DebugRule(faces[0]))

    def Remove(self, *cards: CardName):
        from game.operate.faces import Faces
        faces = self.FindCommandCards(*cards)
        Faces.RemoveAllFromGame(faces, DebugRule(faces[0]))

    def Flip(self, *cards: CardName):
        from game.operate.faces import Faces
        faces = self.FindCommandCards(*cards)
        Faces.FlipAllTo(faces, None, DebugRule(faces[0]))

    ################################################################################
    # Unit
    def Heal(self, card: CardName, val: int):
        face = self.FindOrCreateFace(card)
        from game.card.face.attribute.can_health import CanHealth
        if CanHealth.IsType(face):
            face.HealHealth(val, self.debug_rule)

    def Damage(self, card: CardName, val: int, source: CardFace|None=None):
        face = self.FindOrCreateFace(card)
        from game.card.face.attribute.can_health import CanHealth
        if CanHealth.IsType(face):
            if source == None:
                source = face
            face.TakeDamage(source, val, self.debug_rule)

    def PlaceCounters(self, card: CardName, name: str, val: int):
        """AJOUT (01/09/2026, pack custom doctor_doom) : poser des compteurs.

        Sans cela, aucune capacite qui DEPENSE des compteurs n'est testable :
        il faudrait d'abord jouer les cartes qui les posent, ce qui melerait
        deux capacites dans un meme cas. dd001a « Overwhelming Power » exige
        3 compteurs `power` avant de pouvoir s'activer.

        Miroir de `Puzzle.Damage` : on va droit a l'etat voulu, sans passer par
        le jeu normal.
        """
        from game.card.face.attribute.can_place_counter import CanPlaceCounter
        face = self.FindOrCreateFace(card)
        # `CastTo` et non un `if IsType` : une carte qui n'accepte pas de
        # compteurs doit faire ECHOUER le cas, pas le laisser passer au vert.
        face.CastTo(CanPlaceCounter).PlaceCountersInternal(val, name, self.debug_rule)

    def Confuse(self, card: CardName):
        from game.operate.faces import Faces
        unit = self.FindOrCreateFace(card).CastTo(Unit2)
        if unit.IsConfused():
            unit.DiscardConfused(DebugRule(unit), rule=1)
        else:
            Faces.GiveStatus([unit], "Confused", DebugRule(unit))

    def Stun(self, card: CardName):
        from game.operate.faces import Faces
        unit = self.FindOrCreateFace(card).CastTo(Unit2)
        if unit.IsStunned():
            unit.DiscardStunned(DebugRule(unit), rule=1)
        else:
            Faces.GiveStatus([unit], "Stunned", DebugRule(unit))

    def Tough(self, card: CardName):
        from game.operate.faces import Faces
        unit = self.FindOrCreateFace(card).CastTo(Unit2)
        if unit.IsTough():
            unit.DiscardTough(DebugRule(unit), rule=1)
        else:
            Faces.GiveStatus([unit], "Tough", DebugRule(unit))

    def ChangeToFace(self, card: CardName, to: str):
        """Bascule une identite vers une face PRECISE, designee par son card_id.

        `ChangeForm` ne sait aller que vers « l'autre » face : la premiere face
        heros qui differe de l'actuelle, ou la premiere face alter-ego. Cela
        suffit a une identite ordinaire, qui n'en a que deux. Moon Knight en a
        CINQ, deux heros et trois alter-ego : Steven Grant (mk001d) et Jake
        Lockley (mk001e) etaient donc inatteignables, et leurs reducteurs de
        cout intestables (constate le 9/8/2026).

        Comme `ChangeForm`, `card` designe la face ACTUELLEMENT EN JEU, la
        seule que le monde connaisse a cet instant ; `to` designe la
        destination.
        """
        face = self.FindOrCreateFace(card)
        if Identity.IsType(face):
            face.ChangeToForm(CardFinder(card_ids=[to]), self.debug_rule)

    def ChangeForm(self, card: CardName, rule: Literal['', 'Identity', 'Hero']=''):
        face = self.FindOrCreateFace(card)
        if Identity.IsType(face):
            if rule == 'Identity' or rule == '':
                face.ChangeToOtherIdentityForm(self.debug_rule)
            if rule == 'Hero':
                face.ChangeToOtherHeroForm(self.debug_rule)

    ################################################################################
    #
    def PlaceThreat(self, card: CardName, val:int):
        face = self.FindOrCreateFace(card).CastTo(Scheme2)
        if val > 0:
            face.PlaceThreatInternal(val, self.debug_rule)
        elif val < 0:
            val = -1 * val
            face.RemoveThreatFromSchemes([face], val, self.debug_rule)

    def SetThreat(self, card: CardName, val:int):
        face = self.FindOrCreateFace(card).CastTo(Scheme2)
        self.PlaceThreat(face, val - face.threat)

    ################################################################################
    #
    def Counter(self, card: CardName, name: 'CardFace.COUNTER', size: int=3):
        from game.card.face.attribute.can_place_counter import CanPlaceCounter
        from game.operate.faces import Faces

        face = self.FindOrCreateFace(card)
        if isinstance(face, CanPlaceCounter):
            if size > 0:
                Faces.PlaceCountersOn([face], size, name, self.debug_rule)
            else:
                Faces.RemoveCountersOn([face], -1 * size, name, self.debug_rule)

    def Token(self, card: CardName, name: 'CardFace.TOKEN', size: int=3):
        from game.card.face.attribute.can_place_token import CanPlaceToken
        from game.operate.faces import Faces

        face = self.FindOrCreateFace(card)
        if isinstance(face, CanPlaceToken):
            if size > 0:
                Faces.PlaceTokensOn([face], size, name, self.debug_rule)
            else:
                Faces.RemoveTokensOn([face], size, name, self.debug_rule)

    ################################################################################
    #
    def Reveal(self, card: CardName, *, call_back: Callable[['CardFace'], None]|None=None) -> 'CardFace':
        face = self.FindOrCreateFace(card)
        player = self.world.GetCurrentPlayer()
        # La carte doit VENIR du deck Rencontre. `FindOrCreateFace` la fabrique
        # dans la reserve quand elle n'est nulle part ailleurs, et
        # `message.IsFromEncounterDeck()` est alors faux : toutes les
        # interruptions declarees `from_encounter=True` (« quand une traitrise
        # est revelee DEPUIS LE DECK RENCONTRE ») n'etaient jamais proposees, et
        # rien ne le signalait. On depose donc la carte sur le dessus du deck
        # Rencontre avant de la reveler.
        villain = Worlds.FindVillainByGameArea(player.GetIdentity().card.game_area)
        if villain is not None and face.card.area != villain.encounter_deck:
            face.card.MoveToArea(villain.encounter_deck, self.debug_rule)
            face.card.MoveToTop(face.card.area, self.debug_rule)
        face.Reveal(player, self.debug_rule)
        if call_back:
            call_back(face)
        return face

    def PutIntoPlay(self, card: CardName, under_control: bool=False,
                    exhaust: bool=False) -> 'CardFace':
            """Pose une carte en jeu.

            `under_control` la place SOUS LE CONTROLE du joueur courant. Sans
            lui, la carte arrive sans controleur : elle est en jeu, mais toute
            capacite qui demande « une carte que tu controles » l'ignore, et
            surtout ses capacites `Resource` ne sont jamais proposees au
            paiement (`CheckThisCanPayCost` compare le joueur au controleur).
            C'est ce qui rendait intestable la depense d'un allie pose par
            l'API. `exhaust` la pose inclinee, pour les cartes qui arrivent
            ainsi en partie reelle.
            """
            face = self.FindOrCreateFace(card)
            player = self.world.GetCurrentPlayer()
            face.PutIntoPlay(player, self.debug_rule,
                             under_control=under_control, exhaust=exhaust)
            return face

    def Boost(self, card: CardName) -> 'CardFace':
        from game.operate.worlds import Worlds
        face = self.FindOrCreateFace(card)
        card = face.card

        player = self.world.GetCurrentPlayer()
        villain = Worlds.FindVillainByGameArea(player.GetIdentity().card.game_area)

        if villain:
            card.MoveToArea(villain.encounter_deck, self.debug_rule)
            card.MoveToTop(card.area, self.debug_rule)
            villain.DoActivate(player, self.debug_rule)
        return face

    def Deal(self, card: CardName) -> 'CardFace':
        face = self.FindOrCreateFace(card)
        card = face.card

        player = self.world.GetCurrentPlayer()
        effect = DebugRule(player.GetIdentity())
        player.DealEncounterCard(face, effect)
        return face

    ################################################################################
    # Declencher une attaque, ou activer l'action d'une carte deja en jeu.
    #
    # Ces trois commandes existent pour le banc d'essai : sans elles, aucun test
    # ne peut atteindre une capacite du genre « Forced Response: apres que cet
    # ennemi attaque... » ni « Hero Action: ... », qui ne se declenchent que
    # pendant un vrai tour de jeu.
    def FindFaceInPlay(self, card: CardName) -> 'CardFace':
        """Comme `FindOrCreateFace`, mais la copie EN JEU d'abord.

        `FindOrCreateFace` commence par fouiller le deck du joueur. Un deck
        contenant un second exemplaire de la carte, la commande visait alors ce
        double face cachee au lieu de l'exemplaire pose sur la table, et la
        capacite etait rejetee pour « out of play ». Attaquer, manigancer ou
        activer une action ne concerne que ce qui est en jeu.
        """
        if isinstance(card, str):
            for objet in self.world.object_manager.card_dict.values():
                face = objet.face
                if face is None or not face.IsInPlay():
                    continue
                if getattr(face.paper, "card_id", None) == card or face.IsName(card):
                    return face
        return self.FindOrCreateFace(card)

    def Attack(self, card: CardName, defender: CardName|None=None) -> 'CardFace':
        """Fait attaquer une carte : un ennemi frappe le joueur courant, un
        allie ou un heros fait son attaque de base.

        `defender` fait DEFENDRE un personnage contre cette attaque. Sans lui,
        aucune capacite de defense n'est joignable par l'API : le heros encaisse
        sans jamais declarer de defenseur, donc le message
        `WhenUnitWouldDefend` n'est jamais envoye et TOUTES les cartes
        « Hero Interrupt (defense) » (Unbeatable! sg016, Desperate Defense
        09015, Bulletproof vr002...) restent hors de portee des tests.
        """
        from game.card.face.base import Enemy, Friend
        from game.card.face.attribute.can_attack import AttackProperty
        from game.message import Message
        face = self.FindFaceInPlay(card)
        player = self.world.GetCurrentPlayer()

        if defender is not None:
            self._DeclareDefender(defender)

        if Enemy.IsType(face):
            # Une attaque ennemie est une ACTIVATION : sans le message
            # `WhenEnemyWouldActivate`, les interruptions du genre « quand un
            # sbire non-ELITE s'active, annulez son activation » (Spider-Man
            # av002, Jaw Lock lj004) ne sont jamais proposees. On reproduit donc
            # la branche « attaque » de `DoActivate`, sans sa bifurcation vers
            # la manigance : `Puzzle.Attack` doit toujours attaquer.
            enemy = face.CastTo(Enemy)
            would_act = Message.WhenEnemyWouldActivate(enemy, player)
            would_act.Send()
            if not would_act.is_be_instead:
                enemy.DoAttackYou(
                    player, self.debug_rule,
                    property=AttackProperty(against_player=player,
                                            would_act_message=would_act))
        elif Friend.IsType(face):
            # Le pouvoir de base est utilise par le CONTROLEUR de la carte, pas
            # par le joueur courant : sans cela, dans une partie a deux joueurs
            # (identite liee), faire attaquer le heros du second joueur ne
            # produisait rien du tout.
            controleur = face.GetControlByPlayer() or player
            controleur.MakeBasicPowerLikeInTurn([face], self.debug_rule, ["ATK"])
        else:
            assert False, f"{card=} n'est ni un ennemi ni un personnage allie"
        return face

    def _DeclareDefender(self, card: CardName) -> 'CardFace':
        """Arme un defenseur pour la PROCHAINE attaque, puis se retire.

        Meme montage que `CanDefense.BasicDefenseLater` : on ne peut pas
        defendre a froid, la defense n'existe qu'a l'interieur d'une attaque en
        cours. On pose donc une capacite temporaire qui attend le message
        `WhenUnitBeingAttack` et declare alors la defense de base, exactement ce
        que ferait le joueur en repondant « je defends » a la question du
        moteur.

        ⚠ Passer par `message.DeclareDefender` et non par `BasicDefense` seul
        (constate le 01/09/2026, cas al001a « defense de base ») : `BasicDefense`
        enregistre la defense sans lever `has_declare_defender`, le moteur pose
        donc ENCORE sa question « defendre ? », le pilote des tests repond oui
        avec le meme heros, et `can_attack.py` ADDITIONNE les deux
        `defense_messages` : DEF comptee deux fois (Shocker ATK 2 contre DEF 1
        faisait 0 degat). `DeclareDefender` leve le drapeau, `check_defender`
        (friend.py) ecarte alors la question du moteur : une seule defense.
        Le defenseur est incline s'il etait pret, comme le cout de la defense
        de base ; un defenseur deja incline reste tolere (souplesse des tests).
        """
        from game.ability.factory import AbilityFactory
        from game.ability.ability import AbilityType
        from game.card.face.base import Unit2
        from game.message import Message
        from game.operate.faces import Faces

        face = self.FindFaceInPlay(card)

        def declarer(effect: 'Effect', message: 'Message.WhenUnitBeingAttack') -> None:
            if message.has_declare_defender:
                return
            this = effect.this.CastTo(Unit2)
            if this.IsReady():
                Faces.ExhaustAll([this], effect)
            message.DeclareDefender(this, effect)

        face.effect.RegisterTemp(
            AbilityFactory.WhenUnitBeingAttack(
                AbilityType.Temp0,
                None,
                None,
                declarer,
            ),
            unregister_after_exec=True,
        )
        return face

    def Defend(self, card: CardName, attacker: CardName) -> 'CardFace':
        """`attacker` attaque, et `card` declare la defense.

        Raccourci de `Attack(attacker, defender=card)`, dans l'ordre de lecture
        d'un cas de test (« qui defend contre qui »).
        """
        self.Attack(attacker, defender=card)
        return self.FindFaceInPlay(card)

    def Thwart(self, card: CardName) -> 'CardFace':
        """Fait CONTRER un personnage ami : son pouvoir de base THW.

        Miroir de la branche amie de `Puzzle.Attack` (ajoute le 31/08/2026
        pour le portage agatha_harkness) : sans lui, aucun declencheur
        « After <allie> thwarts » (`AfterUnitThwartEnd`, ex. aa019 Wiccan)
        n'etait joignable par le harnais. Meme montage exactement :
        `MakeBasicPowerLikeInTurn` avec le pouvoir "THW", par le CONTROLEUR
        de la carte.
        """
        from game.card.face.base import Friend
        face = self.FindFaceInPlay(card)
        player = self.world.GetCurrentPlayer()

        assert Friend.IsType(face), f"{card=} n'est pas un personnage ami"
        controleur = face.GetControlByPlayer() or player
        controleur.MakeBasicPowerLikeInTurn([face], self.debug_rule, ["THW"])
        return face

    def BeginVillainPhase(self) -> None:
        """Ouvre la PHASE DU MECHANT, sans la jouer.

        AJOUT (03/09/2026, pack custom night_thrasher). Le harnais savait
        faire attaquer, contrer, maniganter et defendre, mais il ne savait pas
        FRANCHIR UNE FRONTIERE DE PHASE : aucune capacite « quand la phase du
        mechant commence » n'etait joignable, et la batterie entiere n'en
        comptait pas un seul cas. `nt011` Prewind Stance en vit.

        On reproduit exactement l'ouverture de phase du moteur
        (`world.py:789`, fonction locale `phase_begin`) : l'etat passe en
        phase du mechant, `WhenPhaseBegin` part — c'est lui que les
        interruptions attendent —, chaque joueur ouvre sa phase, puis
        `AfterPhaseBegin`. On ne joue PAS la suite de la phase : les cas qui
        veulent l'activation du vilain ont deja `Puzzle.Attack` et
        `Puzzle.Scheme` pour ca.
        """
        from game.message import Message
        from game.world.phase import Phase

        world = self.world
        world.phase.SetState(Phase.State.PlaceThreat)
        world.phase_id += 1

        phase_message = Message.WhenPhaseBegin("Villain", world)
        phase_message.Send()

        for player in world.const_players:
            player.phase.BeginPhase()

        Message.AfterPhaseBegin(phase_message).Send()

    def Scheme(self, card: CardName) -> 'CardFace':
        """Fait manigancer un ennemi contre le joueur courant."""
        from game.card.face.base import Enemy
        from game.card.face.attribute.can_scheme import SchemeProperty
        from game.message import Message
        face = self.FindFaceInPlay(card)
        player = self.world.GetCurrentPlayer()

        assert Enemy.IsType(face), f"{card=} n'est pas un ennemi"
        enemy = face.CastTo(Enemy)
        would_act = Message.WhenEnemyWouldActivate(enemy, player)
        would_act.Send()
        if not would_act.is_be_instead:
            enemy.DoSchemes(
                player, self.debug_rule,
                property=SchemeProperty(against_player=player,
                                        would_act_message=would_act))
        return face

    def Action(self, card: CardName, type: str|None=None, index: int=0) -> 'CardFace':
        """Active une action offerte par une carte en jeu.

        `type` restreint au type de capacite (« HeroAction », « AlterEgoAction »,
        « Action »...), `index` choisit parmi les actions restantes.
        """
        from game.ability.ability import AbilityType
        from game.event.manager import EventManager
        from game.message import Message
        from game.effect.rule import GameRule

        face = self.FindFaceInPlay(card)
        player = self.world.GetCurrentPlayer()

        ability_type = getattr(AbilityType, type) if type else None
        candidats = [x for x in face.effect.Find(when=Message.WhenPlayerInTurn,
                                                 type=ability_type)
                     if not x.ability.is_play]
        assert candidats, f"{card=} n'offre aucune action en jeu ({type=})"

        message = Message.WhenPlayerLikeInTurn(player, GameRule(player.GetIdentity()))
        message.Send()
        # Le filtre du gestionnaire d'evenements ecarte les actions dont la
        # condition n'est pas remplie ; il sert ici uniquement a numeroter les
        # actions REELLEMENT disponibles.
        effects = EventManager.FilterAvailableEffects(
            message, candidats, player, self.world, None)
        assert effects, f"{card=} n'offre aucune action disponible ({type=})"
        assert index < len(effects), \
            f"{card=} n'offre que {len(effects)} action(s) disponible(s), {index=} demande"

        # `ChooseEffects` et pas `ResolveEffect` : c'est lui qui fait choisir les
        # cibles et payer le cout.
        #
        # `forced=True` court-circuite la question posee au joueur des qu'il n'y
        # a qu'une option : pratique, mais le paiement en RESSOURCES se fait
        # justement dans cette question. Une action a cout colore echouait donc
        # en silence. On ne force donc que les actions sans cout en ressources.
        effect = effects[index]
        forced = effect.ability.cost_fn is None and effect.ability.play_cost is None
        player.ChooseEffects([effect], message, forced=forced)
        return face

    ################################################################################
    #
    def PutIntoDeck(self, *cards: CardName):
        from game.operate.worlds import Worlds
        from game.operate.faces import Faces
        for face in self.FindCommandCards(*cards):
            player = self.world.GetCurrentPlayer()
            if face.IsInDeck() and not face.card.area.flags.is_discards:
                Faces.MoveAllToDeck([face], face.card.area, "Top", self.debug_rule)
            elif face.GetOwner() == player:
                Faces.MoveAllTo([face], player.player_deck, self.debug_rule)
            else:
                villain = Worlds.FindVillainByGameArea(player.GetIdentity().card.game_area)
                if villain:
                    Faces.MoveAllTo([face], villain.encounter_deck, self.debug_rule)

    ################################################################################
    #
    def End(self, message: str=""):
        from engine import Engine
        game = Engine.game
        from engine.log import Notify
        controller_manager = game.controller_manager
        controller_manager.skip.SetIsSkipping(False)
        if message:
            Notify.Game(message)

class PuzzleHelper:

    ################################################################################
    #
    # @staticmethod
    # def Exec(commands: List[str]):
    #     for c in ObjectManager.card_dict:
    #         exec(f'c{c} = ObjectManager.card_dict[{c}].face')
    #     for command in commands:
    #         exec(command)

    @staticmethod
    def Exec(commands: List[str], world: 'World'):
        # from engine.lib import Log
        import ast

        Puzzle = RunPuzzle(world)
        Unused(Puzzle)

        class PuzzleCallVisitor(ast.NodeVisitor):
            def visit_Call(self, node: ast.Call):
                # Check if the function call is to a static method of Puzzle
                if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                    if node.func.value.id != 'Puzzle':
                        raise ValueError(f"Function call to '{node.func.attr}' is not allowed. Only calls to 'Puzzle' methods are permitted.")
                else:
                    raise ValueError("Function call to a non-attribute is not allowed.")

                # Continue visiting child nodes
                self.generic_visit(node)

        for command in commands:
            # Parse the command into an AST
            parsed_code = ast.parse(command)

            # Create an instance of the visitor and visit the parsed code
            visitor = PuzzleCallVisitor()

            visitor.visit(parsed_code)

            for c in world.object_manager.card_dict:
                exec(f'c{c} = world.object_manager.card_dict[{c}].face')

            exec(command)  # Only execute if the command is valid
            # try:
            #     pass
            # except ValueError as e:
            #     Log.Assert(CATEGORY_NAME, f"Error executing command '{command}': {e}")
            # except Exception as e:
            #     Log.Assert(CATEGORY_NAME, f"An error occurred while executing command '{command}': {e}")

