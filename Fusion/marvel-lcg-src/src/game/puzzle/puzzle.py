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
                # La face CACHEE d'une carte en jeu (« 01001b » alors que Spider-Man
                # est sur 01001a) : sans cela, un doublon detache etait cree, sans
                # controleur, et le rendu suivant plantait (identity.py:42,
                # GetControlByPlayer, 12/10/2026).
                if face is not None and face.IsInPlay() and any(
                        autre is not face and autre.IsName(card)
                        for autre in getattr(objet, 'back_faces', ())):
                    return face

            # ⚠ APRES la recherche « en jeu », pas avant (corrige le
            # 18/09/2026 au soir) : une carte peut exister EN DEUX EXEMPLAIRES,
            # l'un en jeu et l'autre encore mis de cote (60068a
            # Adamantium-Laced Spine). Fouillee d'abord, la mise de cote
            # gagnait, et `Puzzle.Counter('60068a')` posait ses compteurs sur
            # la copie hors jeu, en silence.
            # CORRECTIF (18/09/2026, Protection Racket) : les cartes MISES DE
            # COTE par le scenario (complots de rechange, Out Front, Master
            # Key, soutiens Daily Bugle...) n'etaient pas fouillees : une
            # commande les visant FABRIQUAIT un doublon sur une seule face, et
            # `Puzzle.Reveal('60136a')` tombait sur
            # `assert prev_scheme.card.back_faces` a la progression.
            # (18/09/2026, bloc Kingpin) : la RESERVE NEMESIS aussi, sans quoi
            # quatre `Puzzle.Remove` sur un set nemesis « creaient » quatre
            # cartes au lieu de vider la reserve (journal xc2145).
            de_cote = list(self.world.aside_deck.Get(True)) \
                + [x for p in self.world.const_players for x in p.set_aside_deck.Get(True)] \
                + [x for p in self.world.const_players for x in p.set_aside_nemesis_sets.Get(True)]
            # (09/10/2026, Hunting Season) : les decks supplementaires du scenario
            # (paquet de pieges de Kraven) aussi, sinon `Remove` fabriquait un doublon.
            de_cote += [x for d in self.world.additional_decks + self.world.additional_discard_piles
                        for x in d.Get(True)]
            for face in de_cote:
                if face is not None and face.IsName(card):
                    return face

            # CORRECTIF (09/09/2026, pack iron_patriot) : une carte dont la FACE
            # A ETE ECHANGEE en cours de partie ne repond plus a son propre
            # identifiant. `Faces.TreatAsAlly` remplace la face du sbire par
            # celle d'un gabarit : le sbire `ip032` en jeu s'appelle toujours
            # Penance, mais son `paper.card_id` est devenu `registered_ally`.
            # Sans ce dernier passage, `Puzzle.Damage('ip032', 1)` FABRIQUAIT UN
            # DOUBLON detache et blessait un fantome — en silence, la commande
            # ayant l'air d'avoir marche.
            for objet in self.world.object_manager.card_dict.values():
                face = objet.face
                if face is None or not face.IsInPlay():
                    continue
                imprimees = getattr(objet, "printed_faces", [])
                # ⚠ REPLI RESERVE AUX FACES ECHANGEES, JAMAIS AUX RECTO-VERSO.
                # Une carte qui a simplement ETE RETOURNEE garde ses deux faces
                # dans `printed_faces` : chercher la-dedans la retrouverait sous
                # son ANCIEN identifiant, et tout cas qui affirme « la carte a
                # basculé » (`hors_jeu`) redeviendrait faux. Mesure du
                # 10/09/2026 : 10 cas de flip du depot sont passes au rouge pour
                # cette seule raison (ah012a, iw001a, mk001a, wc019a, gb007a,
                # as002a, nt003a...).
                # Le cas qu'on veut couvrir est l'autre : `Faces.TreatAsAlly`
                # remplace la face active par une face qui N'EST PAS dans
                # `printed_faces`. C'est ce test-la qui separe les deux.
                if face in imprimees:
                    continue
                for imprimee in imprimees:
                    if getattr(imprimee.paper, "card_id", None) == card:
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

    def _JoueurDeMiseEnPlace(self, siege: int|None=None) -> 'Player':
        """Le joueur dont une commande de mise en place remplit ou vide les zones.

        `siege` (22/10/2026, puzzles a 1 a 4 heros) est un rang dans
        `const_seat_order_players`, l'ordre des SIEGES, qui ne bouge jamais.
        Sans lui (`None`), le premier joueur : le comportement d'avant, dont
        dependent tous les cas du depot. Un siege inexistant leve, jamais un
        repli sur un autre joueur.
        """
        if siege is None:
            return self.world.GetFirstPlayer()
        return self.world.const_seat_order_players[siege]

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

    def EmptyEncounterDiscardPile(self):
        """Vide la DEFAUSSE Rencontre (cartes retirees de la partie). La mise en place
        d'un scenario y defausse des cartes au hasard (recherches) : un cas qui parle
        de « la carte la plus haute de la defausse » doit partir d'une defausse vide
        (pack `shredder`)."""
        from game.operate.faces import Faces
        for _ in range(50):
            faces = [f for f in Worlds.GetEncounterDiscardPileCards(self.world) if f is not None]
            if not faces:
                return
            Faces.RemoveAllFromGame(faces, DebugRule(faces[0]))

    def RemoveNemesisAside(self):
        """Retire de la partie les cartes du set nemesis MISES DE COTE du joueur courant
        (`Remove('<id>')` ne les trouve pas : elles ne sont pas en jeu et il en fabrique
        un doublon). Pour mesurer « si votre sbire nemesis n'entre pas en jeu »."""
        from game.operate.faces import Faces
        joueur = self.world.GetCurrentPlayer()
        faces = list(joueur.set_aside_nemesis_sets.GetAll())
        if faces:
            Faces.RemoveAllFromGame(faces, self.debug_rule)

    def CreateEncounterDeck(self, *cards: str):
        from game.card.factory import CardFactory
        villain = Worlds.GetAllVillains(self.world)[0]
        for card in cards:
            CardFactory.GenerateCard(card, villain.encounter_deck, self.world)

    def CreateHandCards(self, *cards: str, siege: int|None=None):
        from game.card.factory import CardFactory
        first_player = self._JoueurDeMiseEnPlace(siege)
        for card in cards:
            CardFactory.GenerateCard(card, first_player.hand_cards, self.world)

    def CreatePlayerDiscardPile(self, *cards: str, siege: int|None=None):
        from game.card.factory import CardFactory
        first_player = self._JoueurDeMiseEnPlace(siege)
        for card in cards:
            CardFactory.GenerateCard(card, first_player.discard_pile, self.world)

    def EmptyPlayerDeck(self, siege: int|None=None):
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
        joueur = self._JoueurDeMiseEnPlace(siege)
        for _ in range(50):
            faces = [f for f in joueur.player_deck.GetAll() if f is not None]
            if not faces:
                return
            Faces.RemoveAllFromGame(faces, DebugRule(faces[0]))

    def EmptyPlayerDiscardPile(self, siege: int|None=None):
        """Vide la defausse du premier joueur (AJOUTEE le 16/10/2026, pack alopex,
        Prowl : « 1 card with a printed [mental] resource from your discard pile »).

        Le harnais defausse la main de depart AVANT `declencher` (`main_exclusive`) :
        la defausse n'est donc jamais vide, et un cas qui veut « aucune carte
        eligible » ou « exactement cette carte » doit la vider lui-meme. Les cartes
        sont RETIREES DE LA PARTIE, comme `EmptyPlayerDeck`.
        """
        from game.operate.faces import Faces
        joueur = self._JoueurDeMiseEnPlace(siege)
        for _ in range(50):
            faces = [f for f in joueur.discard_pile.GetAll() if f is not None]
            if not faces:
                return
            Faces.RemoveAllFromGame(faces, DebugRule(faces[0]))

    def EmptyPlayerAdditionalDeck(self, siege: int|None=None):
        """Vide le DECK ANNEXE du joueur (deck d'Invocation, deck REGISTERED...).

        AJOUTEE le 10/09/2026, meme motif que `EmptyPlayerDeck` et
        `EmptyEncounterDeck` : `CreatePlayerAdditionalDeck` AJOUTE, elle ne
        remplace pas. Sans elle, aucun cas ne peut mesurer ce qu'une carte fait
        quand ce deck est VIDE — et `ip006` Victoria Hand a deux options dont
        la seconde n'est atteignable que dans cette situation exacte.

        Meme boucle que `EmptyPlayerDeck`, pour la meme raison :
        `RemoveAllFromGame` travaille sur la liste que la zone modifie.
        """
        from game.operate.faces import Faces
        joueur = self._JoueurDeMiseEnPlace(siege)
        for _ in range(50):
            faces = [f for f in joueur.additional_deck.GetAll() if f is not None]
            if not faces:
                return
            Faces.RemoveAllFromGame(faces, DebugRule(faces[0]))

    def CreatePlayerDeck(self, *cards: str, siege: int|None=None):
        from game.card.factory import CardFactory
        first_player = self._JoueurDeMiseEnPlace(siege)
        for card in cards:
            CardFactory.GenerateCard(card, first_player.player_deck, self.world)

    def SetFirstPlayer(self, siege: int):
        """Donne le jeton de PREMIER JOUEUR au siege `siege` (puzzles, 22/10/2026).

        L'ordre des joueurs vit dans `world.players`, dont `players[0]` est le
        premier joueur et qui tourne comme `end_round` le fait (`Types.Rotate`) :
        on fait tourner la liste jusqu'a ce que le siege visé soit en tete, ce qui
        garde l'ordre autour de la table. Un siege inexistant leve.
        """
        voulu = self.world.const_seat_order_players[siege]
        assert voulu in self.world.players, f"le siege {siege} est elimine"
        for _ in range(len(self.world.players)):
            if self.world.players[0] is voulu:
                break
            self.world.players = Types.Rotate(self.world.players, 1)
        self.world.UpdatePlayersOrder(self.debug_rule)

    def EmptyHand(self, siege: int|None=None):
        """Defausse toute la main du premier joueur (cas « main vide »). `Discard`
        ne peut pas viser une carte de la main : `FindOrCreateFace` n'y cherche pas."""
        from game.operate.faces import Faces
        player = self._JoueurDeMiseEnPlace(siege)
        faces = list(player.hand_cards.GetAll())
        if faces:
            Faces.DiscardAll(faces, DebugRule(faces[0]))

    def EmptyAdditionalDeck(self, siege: int|None=None):
        """Retire du jeu toutes les cartes du deck annexe du premier joueur (Sens de Daredevil, ecureuils...)."""
        from game.operate.faces import Faces
        player = self._JoueurDeMiseEnPlace(siege)
        faces = list(player.additional_deck.Get())
        if faces:
            Faces.RemoveAllFromGame(faces, DebugRule(faces[0]))

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

    def CreatePlayerAdditionalDeck(self, *cards: str, siege: int|None=None):
        from game.card.factory import CardFactory
        first_player = self._JoueurDeMiseEnPlace(siege)
        for card in cards:
            CardFactory.GenerateCard(card, first_player.additional_discard_pile, self.world)

    ################################################################################
    #
    def _JoueurDeJeu(self, siege: int|None=None) -> 'Player':
        """Le joueur visé par une commande de JEU (piocher, gagner une carte) : celui dont c'est le tour, ou le siege `siege` (rang dans
        `const_seat_order_players`, puzzles a 1 a 4 heros, 23/10/2026). Un siege inexistant ou elimine leve : jamais de repli sur un autre joueur."""
        if siege is None:
            return self.world.GetCurrentPlayer()
        joueur = self.world.const_seat_order_players[siege]
        assert not joueur.is_eliminated, f"le siege {siege} est elimine"
        return joueur

    def Gain(self, *cards: CardName, call_back: Callable[['CardFace'], None]|None=None, siege: int|None=None):
        player = self._JoueurDeJeu(siege)
        for face in self.FindCommandCards(*cards):
            player.GainCard(face, self.debug_rule)
            if call_back:
                call_back(face)

    def Draw(self, num: int, siege: int|None=None):
        player = self._JoueurDeJeu(siege)
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
    def _RefuserEnManuel(self, face: 'CardFace', geste: str) -> None:
        """En mode manuel, une commande sans effet sur cette carte est REFUSEE.

        AJOUT (06/10/2026, lot 6 du mode manuel « comme OCTGN ») : un degat
        sur un soutien ne faisait rien EN SILENCE, et le journal du plateau
        affirmait un geste qui n'avait rien change. L'erreur devient
        `manuel_refus`. Hors manuel (harnais, bac a sable), rien ne change.
        """
        if getattr(self.world, 'manuel_actif', False):
            raise ValueError(f"{geste} : {face.name} n'en accepte pas")

    def Heal(self, card: CardName, val: int):
        face = self.FindOrCreateFace(card)
        from game.card.face.attribute.can_health import CanHealth
        if CanHealth.IsType(face):
            face.HealHealth(val, self.debug_rule)
        else:
            self._RefuserEnManuel(face, "Soin")

    def Damage(self, card: CardName, val: int, source: CardFace|None=None):
        face = self.FindOrCreateFace(card)
        from game.card.face.attribute.can_health import CanHealth
        if CanHealth.IsType(face):
            if source == None:
                source = face
            face.TakeDamage(source, val, self.debug_rule)
        else:
            self._RefuserEnManuel(face, "Degats")

    def SetHealth(self, card: CardName, hp: int):
        """Regle les POINTS DE VIE ACTUELS de la carte a `hp` (23/10/2026, puzzles : « le mechant est a 12 PV »). C'est un reglage ABSOLU, la ou
        `Damage` et `Heal` sont relatifs : on lit les PV courants, puis on inflige ou on soigne la difference (par le chemin normal du moteur,
        donc les capacites « When damaged / healed » partent comme en jeu). `hp` est borne a [0, PV max] ; une carte a PV infinis ne se regle pas."""
        face = self.FindOrCreateFace(card)
        from game.card.face.attribute.can_health import CanHealth
        if not CanHealth.IsType(face):
            self._RefuserEnManuel(face, "PV")
            return
        assert not face.is_infinite_health, "PV infinis : rien a regler"
        voulu = max(0, min(int(hp), face.max_health))
        ecart = face.health - voulu
        if ecart > 0:
            self.Damage(face, ecart)
        elif ecart < 0:
            self.Heal(face, -ecart)

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

    def AddTough(self, card: CardName, n: int = 1):
        """Pose n cartes Coriace, sans la bascule de `Tough` (qui en RETIRE une
        si l'unite est deja Coriace) : pour empiler sur un porteur de
        `ThisCanHaveAdditionalTough`. Le plafond reste celui du moteur."""
        from game.operate.faces import Faces
        unit = self.FindOrCreateFace(card).CastTo(Unit2)
        for _ in range(n):
            Faces.GiveStatus([unit], "Tough", DebugRule(unit))

    def Expose(self, card: CardName):
        """Pose (ou retire) une carte d'etat Exposed, pack `sentinel`.

        ⚠ Contrairement a Coriace, Sonne et Desoriente, Exposed S'EMPILE : le
        bascule ici retire TOUTES les cartes d'un coup, pour rester previsible
        dans un cas de test.
        """
        from game.operate.faces import Faces
        unit = self.FindOrCreateFace(card).CastTo(Unit2)
        if unit.components.status.exposed:
            unit.LoseState("Exposed", DebugRule(unit), rule="All")
        else:
            Faces.GiveStatus([unit], "Exposed", DebugRule(unit))

    def Cloak(self, card: CardName):
        """Pose (ou retire, bascule) une carte d'etat Cloaked, comme `Tough`."""
        from game.operate.faces import Faces
        unit = self.FindOrCreateFace(card).CastTo(Unit2)
        if unit.IsCloaked():
            unit.DiscardCloaked(DebugRule(unit), rule=1)
        else:
            Faces.GiveStatus([unit], "Cloaked", DebugRule(unit))

    def Daze(self, card: CardName):
        """Pose (ou retire, bascule) une carte d'etat Dazed, comme `Cloak`."""
        from game.operate.faces import Faces
        unit = self.FindOrCreateFace(card).CastTo(Unit2)
        if unit.IsDazed():
            unit.DiscardDazed(DebugRule(unit), rule=1)
        else:
            Faces.GiveStatus([unit], "Dazed", DebugRule(unit))

    def RevealDealtCards(self):
        """Revele les cartes distribuees face cachee de CHAQUE joueur (etape 4 de la phase
        du mechant). Pour mesurer ce qu'une carte « donnee au premier joueur » devient
        une fois revelee (pack `shredder` : Skulk bouclait)."""
        for joueur in list(self.world.const_players):
            if joueur.dealt_encounter_cards.GetSize() > 0:
                joueur.RevealEncounterCards()

    def RemoveMinionsInPlay(self):
        """Retire de la partie TOUS les sbires en jeu (engages ou non). Sert aux
        cas de scenario : la mise en place en revele au hasard, et `Remove('<id>')`
        vise l'exemplaire du DECK avant celui du jeu quand l'id existe en
        plusieurs exemplaires (pack `shredder`)."""
        from game.operate.faces import Faces
        from game.card.face.card_type import Minion
        faces = [o.face for o in self.world.object_manager.card_dict.values()
                 if o.face is not None and o.face.IsInPlay() and Minion.IsType(o.face)]
        Faces.RemoveAllFromGame(faces, self.debug_rule)

    def AddCloak(self, card: CardName, n: int = 1):
        """Pose n cartes Cloaked, sans la bascule de `Cloak` (qui en RETIRE une si
        l'unite est deja Cloaked) : pour empiler sur Shredder, dont le maximum est
        2, 3 ou 4 selon son stade (pack `shredder`). Le plafond reste celui du
        moteur (`CanStatus.cloaked_max`)."""
        from game.operate.faces import Faces
        unit = self.FindOrCreateFace(card).CastTo(Unit2)
        for _ in range(n):
            Faces.GiveStatus([unit], "Cloaked", DebugRule(unit))

    def AddStatus(self, card: CardName, name: str, n: int = 1):
        """Pose n cartes d'etat `name` SANS bascule (les plafonds du moteur restent ;
        ajoute pour Intensified : deux Exposed, un Sonne PUIS un second, etc.)."""
        from game.operate.faces import Faces
        unit = self.FindOrCreateFace(card).CastTo(Unit2)
        for _ in range(n):
            Faces.GiveStatus([unit], name, DebugRule(unit))

    def Intensify(self, card: CardName, n: int = 1):
        """Pose n cartes Intensified (7e etat, TMNT). Pas de bascule : la regle de la
        carte (« cannot be given to a character that has no status cards ») s'applique,
        poser d'abord un autre etat."""
        from game.operate.faces import Faces
        unit = self.FindOrCreateFace(card).CastTo(Unit2)
        for _ in range(n):
            Faces.GiveStatus([unit], "Intensified", DebugRule(unit))

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
        else:
            self._RefuserEnManuel(face, "Compteurs")

    def Token(self, card: CardName, name: 'CardFace.TOKEN', size: int=3):
        from game.card.face.attribute.can_place_token import CanPlaceToken
        from game.operate.faces import Faces

        face = self.FindOrCreateFace(card)
        if isinstance(face, CanPlaceToken):
            if size > 0:
                Faces.PlaceTokensOn([face], size, name, self.debug_rule)
            else:
                Faces.RemoveTokensOn([face], -size, name, self.debug_rule)
        else:
            self._RefuserEnManuel(face, "Jetons")

    ################################################################################
    #
    def Reveal(self, card: CardName, *, call_back: Callable[['CardFace'], None]|None=None,
               by: CardName|None=None) -> 'CardFace':
        # `by` (ajoute le 20/10/2026, backlog 12, dz022 « Stealing Sound ») :
        # l'identite du joueur qui REVELE la carte, dans une partie a plusieurs.
        # Sans lui, c'est le joueur courant. Additif.
        face = self.FindOrCreateFace(card)
        player = self.world.GetCurrentPlayer()
        if by is not None:
            player = self.FindFaceInPlay(by).GetControlByPlayer() or player
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
                    exhaust: bool=False, player: int|None=None) -> 'CardFace':
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
            # `player` (29/09/2026) : le siege qui recoit la carte, pour les
            # rulings multijoueur (« la copie de l'AUTRE joueur », 04028).
            joueur = (self.world.GetCurrentPlayer() if player is None
                      else self.world.const_players[player])
            face.PutIntoPlay(joueur, self.debug_rule,
                             under_control=under_control, exhaust=exhaust)
            return face

    def PlaceUnder(self, card: CardName, host: CardName, face_up: bool=False) -> 'CardFace':
        """Glisse CARD face cachee sous HOST (en jeu), sans passer par une
        capacite : sert a monter un plafond « Max N cards tucked here ».

        `face_up=True` (ajoute le 20/10/2026, backlog 12, pack dazzler) : pose
        la carte FACE VISIBLE, comme Live Concert (dz017a) range une chanson
        dans sa Setlist. Additif : sans l'argument, rien ne change."""
        face = self.FindOrCreateFace(card)
        hote = self.FindFaceInPlay(host)
        hote.PlaceCardHere([face], face_up, self.debug_rule)
        return face

    def TurnEncounterTopFaceUp(self) -> 'CardFace|None':
        """Rend VISIBLE la carte du dessus du deck rencontre, sans la reveler
        ni la deplacer (ruling Redwing 53002 : « if the top card is visible »)."""
        player = self.world.GetCurrentPlayer()
        villain = Worlds.FindVillainByGameArea(player.GetIdentity().card.game_area)
        assert villain is not None
        top = villain.encounter_deck.GetTop()
        if top is not None:
            top.card.state.is_face_up = True
        return top

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

    def GiveFacedownBoost(self, target: CardName, card: CardName) -> 'CardFace':
        """Donne a TARGET (en jeu) une carte boost face cachee HORS
        activation : pile persistante (`components.boostable.GetDeck()`),
        comme `fne/kingpin/60165` James Wesley (« give him a facedown boost
        card »), pas la pioche normale du dessus du deck rencontre (`Boost`).

        Sans cette commande, aucun cas ne peut monter une pile de boost non
        vide sur un ennemi en dehors d'une activation reelle (gs226 Lauri-Ell,
        « discard each boost card on that enemy » : preuve par substitution
        bloquee faute de pile a vider, voir CAMPAGNE-ALLIEES-GABARITS.md)."""
        cible = self.FindFaceInPlay(target)
        face = self.FindOrCreateFace(card)
        cible.components.boostable.GiveBoostCard(face, self.debug_rule)
        return face

    def Deal(self, card: CardName, joueur: int|None=None) -> 'CardFace':
        """`joueur` : l'INDICE du joueur servi (0 = le premier). Ajoute le
        19/09/2026 : sans lui, une carte ne pouvait etre distribuee qu'au
        joueur courant, et aucun cas ne pouvait mesurer « apres qu'UN JOUEUR
        recoit une carte » pour un AUTRE joueur (60156 Robbie Robertson)."""
        face = self.FindOrCreateFace(card)
        card = face.card

        if joueur is not None:
            player = self.world.const_players[joueur]
        else:
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

    def Attack(self, card: CardName, defender: CardName|None=None,
               against: CardName|None=None) -> 'CardFace':
        """Fait attaquer une carte : un ennemi frappe le joueur courant, un
        allie ou un heros fait son attaque de base.

        `defender` fait DEFENDRE un personnage contre cette attaque. Sans lui,
        aucune capacite de defense n'est joignable par l'API : le heros encaisse
        sans jamais declarer de defenseur, donc le message
        `WhenUnitWouldDefend` n'est jamais envoye et TOUTES les cartes
        « Hero Interrupt (defense) » (Unbeatable! sg016, Desperate Defense
        09015, Bulletproof vr002...) restent hors de portee des tests.

        `against` (ajoute le 20/10/2026, backlog 12, dz006 « Doll ») : l'identite
        du joueur VISE par l'activation d'un ennemi, dans une partie a plusieurs.
        Sans lui l'ennemi frappe le joueur courant, et un « activate against
        YOU » ne pouvait pas etre distingue d'une activation contre un autre
        joueur. Additif : sans l'argument, rien ne change.
        """
        from game.card.face.base import Enemy, Friend
        from game.card.face.attribute.can_attack import AttackProperty
        from game.message import Message
        face = self.FindFaceInPlay(card)
        player = self.world.GetCurrentPlayer()
        if against is not None:
            player = self.FindFaceInPlay(against).GetControlByPlayer() or player

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

    def EnemyAttacks(self, card: CardName, target: CardName, defender: CardName|None=None,
                     overkill_to: CardName|None=None, joueur: int|None=None,
                     **options: Any) -> 'CardFace':
        """Brique commune du 20/10/2026 : l'ennemi CARD attaque TARGET (allie,
        sbire, mechant), par `Enemy.AttackCharacter`. `defender` arme un
        defenseur comme `Attack` ; `overkill_to` designe la carte qui recoit
        l'exces quand un sbire est abattu ; `options` passe tel quel
        (`players_may_defend`, `overkill`, `additional_attack`, `give_boost`,
        `ally_attack_is_against_player`)."""
        from game.card.face.base import Enemy
        face = self.FindFaceInPlay(card)
        cible = self.FindFaceInPlay(target)
        assert Enemy.IsType(face), f"{card=} n'est pas un ennemi"
        if defender is not None:
            self._DeclareDefender(defender)
        if overkill_to is not None:
            options['overkill_to'] = self.FindFaceInPlay(overkill_to)
        if joueur is not None:
            # L'INDICE du joueur « vous » des Boost (`for_player`), 0 = le premier.
            options['for_player'] = self.world.const_players[joueur]
        face.CastTo(Enemy).AttackCharacter(cible, self.debug_rule, **options)
        return face

    def ProtectFromPlayerCards(self, card: CardName, attached_to: CardName|None=None,
                               trait: str|None=None) -> 'CardFace':
        """Brique commune du 20/10/2026 : rend une carte « insensible aux cartes
        joueur » en passant par la VRAIE fabrique
        `AbilityFactory.CannotBeAffectedByPlayerCards`, comme le ferait le
        script d'une carte de campagne.

        - `attached_to=None` : CARD se protege elle-meme (« This », mechant
          HIDDEN) ; `trait` ajoute la condition « tant qu'elle a ce trait ».
        - `attached_to=X` : CARD (un attachement) est d'abord attachee a X, puis
          protege son porteur (« AttachedCharacter », In the Crosshairs).

        La fabrique ecoute l'entree en jeu de la carte : la commande inscrit la
        capacite puis rejoue la fenetre d'entree en jeu (`ApplyAfterEnterPlay`,
        en retournement pour ne rien relancer d'autre)."""
        from game.ability.factory import AbilityFactory
        from game.card.face.attribute.can_attach import CanAttach
        source = self.FindFaceInPlay(card)
        if attached_to is not None:
            hote = self.FindFaceInPlay(attached_to)
            if not source.IsInPlay():
                source.PutIntoPlay(self.world.GetCurrentPlayer(), self.debug_rule)
            source.CastTo(CanAttach).AttachTo2(hote, self.debug_rule)
            which = "AttachedCharacter"
        else:
            which = "This"
        while_fn = (lambda face: face.HasTrait(trait)) if trait else None
        source.effect.RegisterTemp(
            AbilityFactory.CannotBeAffectedByPlayerCards(which, while_fn).NoOutOfPlayLimit(),
            unregister_after_exec=False,
        )
        area = source.card.area
        source.ApplyAfterEnterPlay(area, area, self.debug_rule, True)
        return source

    # Brique commune du 20/10/2026 : plusieurs mechants (game/operate/villains.py).
    def SetVillainRule(self, the_villain: str="Active", player_cards: str="TheVillain") -> None:
        """Pose `Villains.Rule` sur le scenario (« le mechant » = actif ou le
        plus a gauche ; cartes joueur = le meme, ou au choix du joueur)."""
        from game.operate.villains import Villains
        Villains.SetRule(self.world, Villains.Rule(the_villain=the_villain, player_cards=player_cards))  # type: ignore

    def SetActiveVillain(self, card: CardName) -> 'CardFace':
        """Pose le compteur « active » sur ce mechant (et l'ote aux autres)."""
        from game.operate.villains import Villains
        from game.card.face.base import Villain
        face = self.FindFaceInPlay(card)
        Villains.SetActive(face.CastTo(Villain), self.debug_rule)
        return face

    def RemoveVillain(self, card: CardName) -> None:
        """Retire ce mechant sans rien reporter (`Villains.Remove`)."""
        from game.operate.villains import Villains
        from game.card.face.base import Villain
        Villains.Remove(self.FindFaceInPlay(card).CastTo(Villain), self.debug_rule)

    def PlaceCountersOnVillains(self, name: str, val: int, skip: int=0) -> None:
        """AJOUT (22/10/2026, Punisher MC×DC 2026) : pose des compteurs sur TOUS les vilains en jeu (sauf les `skip` premiers). Les CAPO d'une
        vraie mise en place sont tires au hasard : on ne peut pas les nommer."""
        from game.operate.worlds import Worlds
        for villain in list(Worlds.GetAllVillains(self.world))[skip:]:
            villain.PlaceCountersInternal(val, name, self.debug_rule)

    def DamageAllVillains(self, val: int) -> None:
        """AJOUT (22/10/2026, Punisher MC×DC 2026) : inflige `val` degats a chaque vilain en jeu (ceux d'une vraie mise en place sont tires au hasard)."""
        from game.operate.worlds import Worlds
        for villain in list(Worlds.GetAllVillains(self.world)):
            self.Damage(villain, val)

    def AddToVictoryDisplay(self, *cards: CardName) -> None:
        """AJOUT (22/10/2026, Punisher MC×DC 2026) : ces cartes vont dans la pile de victoire (Gang War : « after a LEAD card is added to
        the victory display »). Envoie le message de deplacement habituel."""
        from game.operate.faces import Faces
        Faces.AddToVictoryDisplay([self.FindOrCreateFace(c) for c in cards], self.debug_rule)

    def CreateLeadsDeck(self, *cards: CardName) -> None:
        """AJOUT (22/10/2026, Punisher MC×DC 2026) : cree le paquet LEADS (pistes) du banc avec ces cartes (le DESSUS est choisi en
        n'en donnant qu'une). Proprietaire du paquet : le premier mechant en jeu."""
        from game.operate.worlds import Worlds
        from game.deck.deck_type import DeckType
        villain = Worlds.GetVillains(self.debug_rule)[0]
        Worlds.ScenarioDeck(self.debug_rule, "LeadsDeck").Create(
            self.debug_rule, villain, list(cards), type=DeckType.AdditionalDeck, has_discard_pile=False)

    def BuildVillainDeck(self, *cards: CardName) -> None:
        """Melange ces mechants dans le deck de mechants (`Villains.BuildVillainDeck`)."""
        from game.operate.villains import Villains
        Villains.BuildVillainDeck([self.FindOrCreateFace(c) for c in cards], self.debug_rule)  # type: ignore

    def RevealNextVillain(self) -> 'CardFace|None':
        """Revele le dessus du deck de mechants, en jeu le plus a droite."""
        from game.operate.villains import Villains
        return Villains.RevealNextVillain(self.world.GetCurrentPlayer(), self.debug_rule)

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

    def EndPlayerTurn(self) -> None:
        """FERME le tour du joueur courant, comme `player_phase.py` (WhenPlayerTurnEnd
        puis AfterPlayerTurnEnd).

        AJOUT (20/10/2026, backlog 12, dz032 « Captivating Performance »). Ni
        `EndPlayerPhase` ni `BeginVillainPhase` n'envoient la fin de TOUR : un
        effet « this turn » (`RegisterTemp(until_turn_end=True)`) restait vivant et
        un cas sur sa duree etait vert avec la mauvaise duree. Additif.
        """
        from game.message import Message
        player = self.world.GetCurrentPlayer()
        turn_end_message = Message.WhenPlayerTurnEnd(player, self.world.round_id)
        turn_end_message.Send()
        Message.AfterPlayerTurnEnd(player, turn_end_message).Send()

    def EndPlayerPhase(self) -> None:
        """FERME la phase des joueurs, comme `phase_end("Player")` du moteur.

        AJOUT (06/10/2026, dz003 « A Little Girl's Dream »). `BeginVillainPhase`
        ouvre la phase du mechant mais ne ferme JAMAIS celle des joueurs : aucun
        `AfterPhaseEnd` ne partait, donc tout effet temporaire « jusqu'a la fin
        de la phase » restait vivant et un cas sur sa DUREE etait vert meme avec
        la mauvaise duree (preuve par substitution rouge impossible). On reprend
        `phase_end` (`world.py`, fonction locale) : etat de fin de phase, tour
        courant vide, `WhenPhaseEnd`, puis `AfterPhaseEnd`.
        """
        from game.message import Message
        from game.world.phase import Phase

        world = self.world
        world.phase.SetState(Phase.State.EndPhase)
        world.current_player = None

        phase_message = Message.WhenPhaseEnd(world.phase_id, "Player", world)
        phase_message.Send()

        world.stat.OnPhaseEnd()

        Message.AfterPhaseEnd(world.phase_id, "Player", phase_message).Send()

    def EndVillainPhase(self) -> None:
        """FERME la phase du mechant, comme `phase_end("Villain")` du moteur (Hunting Season : « quand la phase du mechant se termine »)."""
        from game.message import Message
        from game.world.phase import Phase

        world = self.world
        world.phase.SetState(Phase.State.EndPhase)
        world.current_player = None

        phase_message = Message.WhenPhaseEnd(world.phase_id, "Villain", world)
        phase_message.Send()

        world.stat.OnPhaseEnd()

        Message.AfterPhaseEnd(world.phase_id, "Villain", phase_message).Send()

    def RunVillainPhase(self) -> None:
        """Joue les etapes 1 a 4 de la phase du mechant (`World.VillainPhase`).

        AJOUT (12/10/2026) : un joueur elimine pendant la partie recevait encore
        une carte rencontre a l'etape 3 et la revelait a l'etape 4, et le moteur
        l'attendait (partie bloquee). Aucun cas ne jouait une phase du mechant
        entiere apres une elimination."""
        self.world.VillainPhase()

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

    def Action(self, card: CardName, type: str|None=None, index: int=0, siege: int|None=None) -> 'CardFace':
        """Active une action offerte par une carte en jeu.

        `type` restreint au type de capacite (« HeroAction », « AlterEgoAction »,
        « Action »...), `index` choisit parmi les actions restantes.
        """
        from game.ability.ability import AbilityType
        from game.event.manager import EventManager
        from game.message import Message
        from game.effect.rule import GameRule

        face = self.FindFaceInPlay(card)
        # `siege` (AJOUT 22/10/2026, pu141 « any player may trigger ») : le joueur qui declenche l'action, quand ce n'est pas le courant.
        player = self.world.GetCurrentPlayer() if siege is None else self.world.const_players[siege]

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
    # Les piles atteignables par `MoveTo`, nommees comme les membres de
    # `DeckType` (game/deck/deck_type.py:193). Table EXPLICITE et non
    # reflexive : le moteur n'expose aucun registre des piles, et deviner une
    # pile ferait disparaitre des cartes dans une zone qu'on ne regarde jamais.
    ZONES_JOUEUR = {
        'PlayerDeck':           lambda j: j.player_deck,
        'DiscardPile':          lambda j: j.discard_pile,
        'HandsArea':            lambda j: j.hand_cards,
        'AlliesArea':           lambda j: j.allies,
        'SupportsArea':         lambda j: j.supports,
        'HeroArea':             lambda j: j.area_hero,
        'EngagedEnemiesArea':   lambda j: j.engaged_minions,
        'ResourcesArea':        lambda j: j.area_resources,
        'ReserveArea':          lambda j: j.reserve,
        'RisingTideArea':       lambda j: j.rising_tide, # AJOUT (pack wave)
        # Correctif ronde 1 (18/09/2026) : `j.set_aside_deck` est un faux ami
        # herite du moteur de base (`player.py:100`), il vaut en realite
        # `additional_discard_pile` (`DeckType.AdditionalDiscardPile`), pas
        # `DeckType.AsideDeck`. La vraie pile typee `AsideDeck` est
        # `set_aside_nemesis_sets` (`player.py:61`).
        'AsideDeck':            lambda j: j.set_aside_nemesis_sets,
        'ObligationsArea':      lambda j: j.obligations_area,
        'AdditionalDeck':       lambda j: j.additional_deck,
        # Ronde de correction 1 (tache 5, 19/09/2026) : derniere pile visible
        # sur le plateau et pourtant inatteignable par `MoveTo` - la defausse
        # du deck ANNEXE (Invocation, Reserve...), a ne pas confondre avec le
        # faux ami `j.set_aside_deck` du commentaire ci-dessus (qui POINTE deja
        # sur `additional_discard_pile`, mais sous un nom qui pretend etre
        # autre chose). Ici on nomme l'attribut reel directement.
        'AdditionalDiscardPile': lambda j: j.additional_discard_pile,
        # AJOUT (06/10/2026, lot 2 du mode manuel « comme OCTGN ») : un
        # evenement pose a la main reste a cote de SON heros, en cours de
        # resolution, jusqu'a ce que le joueur le defausse (Suppr). Pile
        # `DeckType.ProcessingArea` propre au joueur (`player.py:90`), distincte
        # de la resolution du scenario (`'ProcessingArea'`, ZONES_MONDE).
        'PlayerProcessingArea': lambda j: j.area_processing,
    }

    ZONES_MONDE = {
        'EncounterDeck':        lambda w: w.GetScenario().encounter_deck,
        'EncounterDiscardPile': lambda w: w.GetScenario().encounter_discard_pile,
        'VillainArea':          lambda w: w.GetScenario().area_villain,
        'MainSchemesArea':      lambda w: w.area_schemes_main,
        'SideSchemesArea':      lambda w: w.area_schemes_side,
        'EnvironmentArea':      lambda w: w.area_environment,
        'ProcessingArea':       lambda w: w.area_processing,
        'RemovedArea':          lambda w: w.area_removed,
        'VictoryDisplay':       lambda w: w.victory_display,
        # La zone de boost, a cote du mechant (07/10/2026) : c'est la que
        # `villainBoost` d'OCTGN pose la carte du dessus du deck Rencontre,
        # FACE CACHEE (actions.py:693, `moveToTable(x, y, True)`).
        'BoostArea':            lambda w: w.area_boosting,
        # Tache 4 bis (19/09/2026) : `'AsideDeck'` (ZONES_JOUEUR) designe deja
        # le set nemesis du heros. Les deux zones ci-dessous sont les mises de
        # cote du SCENARIO, visuellement distinctes sur le plateau mais qui
        # partagent le meme `DeckType.AsideDeck` cote moteur (`world.py`).
        # Ne PAS renommer 'AsideDeck' : on ajoute, on ne deplace pas.
        'AsideScenario':        lambda w: w.aside_deck,
        'AsideModular':         lambda w: w.aside_modular,
        # AJOUT (22/10/2026, scenario Shadow Labyrinth) : le paquet piege (« trap deck ») et sa defausse, crees a la mise en place de sl038a.
        'TrapDeck':             lambda w: w.scenario_decks['TrapDeck'].deck,
        'TrapDiscardPile':      lambda w: w.scenario_decks['TrapDeck'].discard_pile,
    }

    def _JoueurVise(self, player: int, siege: int|None) -> 'Player':
        """Le joueur qu'une commande vise.

        `player` est un rang dans `const_players`, l'ordre du MOMENT : il
        tourne avec le premier joueur, donc un geste ancien rejoue plus tard
        peut viser quelqu'un d'autre. `siege` (06/10/2026, lot 2 du mode
        manuel) est un rang dans `const_seat_order_players`, l'ordre des
        SIEGES, qui ne bouge jamais : avec lui, le geste est deterministe.
        Un siege inexistant leve, jamais un repli sur un autre joueur.
        """
        if siege is not None:
            return self.world.const_seat_order_players[siege]
        return self.world.const_players[player]

    def _ZoneParNom(self, zone: str, player: int, siege: int|None=None) -> 'Deck':
        """Rend la pile designee par son nom.

        ⚠ Un nom inconnu doit ECHOUER bruyamment. Un repli silencieux sur une
        pile par defaut ferait disparaitre la carte.
        """
        if zone in RunPuzzle.ZONES_MONDE:
            return RunPuzzle.ZONES_MONDE[zone](self.world)
        if zone in RunPuzzle.ZONES_JOUEUR:
            return RunPuzzle.ZONES_JOUEUR[zone](self._JoueurVise(player, siege))
        raise KeyError(f"zone inconnue : {zone}")

    def MoveTo(self, card: CardName, zone: str, position: str='Top', player: int=0, siege: int|None=None,
               face_cachee: bool=False):
        """Le deplacement LIBRE : n'importe quelle carte vers n'importe quelle
        pile, sans aucune verification.

        C'est l'echappatoire du mode manuel (spec du 18/09/2026) : sans elle,
        une zone oubliee bloque la partie. Le deplacement reel se fait dans
        `card.MoveToArea`, le message qui suit n'est qu'une notification, donc
        la porte du silence ne casse rien ici.

        Correctif ronde 1 (18/09/2026) sur `position='Bottom'` : si la pile
        visee n'est PAS un deck ordonne (`flags.is_deck`/`is_dealt_encounter`),
        le "dessous" n'a pas de sens, la carte est posee normalement par
        `Faces.MoveAllTo` plutot que de rester immobile en silence.

        Correctif ronde 2 (18/09/2026) : sur une pile ordonnee, on ne leve
        plus sur la VALEUR DE RETOUR de `MoveToBottom` (elle rend `False`
        aussi bien sur un vrai echec que sur une carte deja au fond, ce
        dernier cas n'etant pas un echec). On leve sur le RESULTAT : si,
        apres l'appel, la carte n'est pas dans la pile visee, c'est un vrai
        defaut et on leve bruyamment ; sinon, silence, peu importe ce que la
        methode a rendu.
        """
        from game.operate.faces import Faces
        face = self.FindOrCreateFace(card)
        pile = self._ZoneParNom(zone, player, siege)
        if position == 'Bottom' and (pile.flags.is_deck or pile.flags.is_dealt_encounter):
            face.card.MoveToBottom(pile, self.debug_rule)
            if face.card.area is not pile:
                raise RuntimeError(
                    f"MoveTo({card!r}, {zone!r}, 'Bottom') n'a pas depose la "
                    "carte dans la pile visee")
        else:
            Faces.MoveAllTo([face], pile, self.debug_rule)
        # AJOUT (06/10/2026, lot 6 du mode manuel « comme OCTGN ») : Maj
        # pendant le glisser, ou Ctrl+U sur une pile (`drawUnrevealed`), pose
        # la carte FACE CACHEE en UNE commande (un Ctrl+Z la defait entiere).
        # L'etat est force sans `Flip` : un retournement enverrait ses messages
        # et rejouerait les effets « quand elle est retournee ».
        if face_cachee and face.card.IsFaceUp():
            face.card.state.is_face_up = False

    # La pile ou retourne chaque defausse (`shuffleDiscardIntoDeck` d'OCTGN).
    DECK_DE_LA_DEFAUSSE = {
        'DiscardPile': 'PlayerDeck',
        'EncounterDiscardPile': 'EncounterDeck',
        'AdditionalDiscardPile': 'AdditionalDeck',
    }

    def ShuffleDiscardIntoDeck(self, zone: str, player: int=0, siege: int|None=None):
        """Remet toute une defausse dans son deck, puis melange le deck.

        AJOUT (06/10/2026, lot 6 du mode manuel « comme OCTGN ») : UNE commande,
        donc UN geste, qu'un seul Ctrl+Z defait entier. Le plateau envoyait un
        `MoveTo` par carte puis `Shuffle` : autant de gestes que de cartes. Une
        defausse inconnue leve (`KeyError`), jamais un repli.
        """
        from game.operate.faces import Faces
        defausse = self._ZoneParNom(zone, player, siege)
        deck = self._ZoneParNom(RunPuzzle.DECK_DE_LA_DEFAUSSE[zone], player, siege)
        cartes = list(defausse.GetAll())
        if cartes:
            Faces.MoveAllTo(cartes, deck, self.debug_rule)
        deck.Shuffle(self.debug_rule)

    def DrawUpToHandSize(self, player: int=0, siege: int|None=None):
        """F12 d'OCTGN (`doEndHeroPhase`) : le joueur pioche jusqu'a sa taille
        de main. Un deck vide se reconstitue en remelangeant la defausse
        (`checkDeckRemainingCards`), SANS la carte Rencontre de penalite des
        regles : en manuel, c'est au joueur de la tirer.

        AJOUT (06/10/2026, lot 6 du mode manuel) : UNE commande par heros. Le
        plateau choisissait les cartes du dessus lui-meme, et ne savait pas
        quoi faire d'un deck vide. S'arrete si deck ET defausse sont vides.
        """
        from game.operate.faces import Faces
        joueur = self._JoueurVise(player, siege)
        while len(joueur.hand_cards.GetAll()) < joueur.hand_size:
            if not joueur.player_deck.GetAll():
                defausse = list(joueur.discard_pile.GetAll())
                if not defausse:
                    break
                Faces.MoveAllTo(defausse, joueur.player_deck, self.debug_rule)
                joueur.player_deck.Shuffle(self.debug_rule)
            Faces.MoveAllTo([joueur.player_deck.GetAll()[-1]], joueur.hand_cards, self.debug_rule)

    def EndRound(self):
        """Second F12 d'OCTGN (`advanceGame`, fin de la phase du mechant) : le
        jeton de premier joueur passe (dans chaque camp) et le compteur de
        rounds avance.

        AJOUT (06/10/2026, lot 6 du mode manuel). Aucun message de debut de
        round : en manuel, le moteur se tait.
        """
        camps: list[int] = []
        for joueur in self.world.const_players:
            camp = self.world.GetTeamOfPlayer(joueur)
            if camp not in camps:
                camps.append(camp)
        for camp in camps:
            self.world.PassFirstPlayerToken(camp, self.debug_rule)
        self.world.round_id += 1

    def CreateGameArea(self) -> int:
        """AJOUT (21/10/2026, PU-5, spec-ville-m1-m2 etape 1) : cree une zone de jeu et rend son INDICE dans `world.game_areas`
        (0 = la premiere). Banc des territoires : aucune carte de campagne requise."""
        self.world.CreateGameArea()
        return len(self.world.game_areas) - 1

    def CreateCommonGameArea(self) -> int:
        """AJOUT (21/10/2026, PU-5 etape 2) : cree la zone COMMUNE (`world.game_area_commune`) et rend son indice."""
        self.world.CreateCommonGameArea()
        return len(self.world.game_areas) - 1

    def MoveCardToGameArea(self, card: CardName, zone: int) -> None:
        """AJOUT (21/10/2026, PU-5) : une carte (et ses attachements) change de zone."""
        face = self.FindFaceInPlay(card)
        self.world.game_areas[zone].AddCard(face.card)

    def MovePlayerToGameArea(self, zone: int, player: int=0) -> None:
        """AJOUT (21/10/2026, PU-5) : `GameArea.AddPlayer` (le joueur et tout ce qu'il possede changent de zone)."""
        self.world.MovePlayerToGameArea(self.world.const_players[player], self.world.game_areas[zone])

    def InstallerVille(self, grille: List[List[str]], depart: Tuple[int, int]=(1, 1), en_jeu: bool=False) -> None:
        """AJOUT (21/10/2026, PU-5 etape 3) : pose la ville du banc : une zone COMMUNE, une zone par ligne de la grille, les cartes de
        lieu (`grille[ligne][colonne]` : un identifiant de carte, juste une reference), tous les joueurs sur `depart`."""
        from game.operate.ville import Ville
        self.world.CreateCommonGameArea()
        zones = {ligne: self.world.CreateGameArea() for ligne in range(len(grille))}
        if en_jeu:
            # (22/10/2026, PU-7) lieux REELS : chaque carte est mise en jeu dans la zone de SA rangee (spec G7), les capacites tournent.
            joueur = self.world.GetCurrentPlayer()
            cases = {}
            for l, rang in enumerate(grille):
                for c, cid in enumerate(rang):
                    face = self.CreateCard(cid)
                    face.PutIntoPlay(joueur, self.debug_rule)
                    zones[l].AddCard(face.card)
                    cases[(l, c)] = face
        else:
            cases = {(l, c): self.CreateCard(cid) for l, rang in enumerate(grille) for c, cid in enumerate(rang)}
        Ville.Installer(self.world, cases, zones, tuple(depart))

    def DeplacerDansLaVille(self, case: Tuple[int, int], player: int=0) -> None:
        """AJOUT (21/10/2026, PU-5) : `Ville.Deplacer` (sans le cout : l'Action de The City le paie). Refus silencieux si la case n'est
        pas voisine ; l'etat se lit ensuite avec `case_de`."""
        from game.operate.ville import Ville
        Ville.Deplacer(self.world, self.world.const_players[player], tuple(case))

    def AttacherAuLieu(self, card: CardName, lieu: CardName) -> None:
        """AJOUT (22/10/2026, PU-7 M5) : `Ville.AttacherSbire` (le sbire en jeu est glisse sous le lieu, sans choix ni condition de joueur).
        Refus silencieux (lieu occupe...) : l'etat se lit avec `attache_a`."""
        from game.operate.ville import Ville
        Ville.AttacherSbire(self.debug_rule, self.FindFaceInPlay(card), self.FindFaceInPlay(lieu))

    def PlacerDansLaVille(self, case: Tuple[int, int], player: int=0) -> None:
        """AJOUT (22/10/2026, PU-7 M5) : `Ville.Placer` (deplacement SANS adjacence, avec les interruptions de depart / d'arrivee)."""
        from game.operate.ville import Ville
        Ville.Placer(self.world, self.world.const_players[player], tuple(case))

    def AssembleeAutreTable(self, action: str, *arguments: Any) -> None:
        """AJOUT (22/10/2026, Kingsfall multi-tables) : modifie l'etat COMMUN de l'assemblee COMME UNE AUTRE TABLE le ferait, EN COURS de partie
        (`verser`, n) / (`envoyer`, table) / (`terminer`, table, victoire). Le harnais ne peut pas faire jouer deux tables a la fois : c'est le seul moyen de
        prouver que cette table SE SYNCHRONISE (et ne se contente pas de lire l'etat posee avant la mise en place)."""
        from game.operate.assemblee import Assemblee
        pod = self.world.rule.assemblee
        assert pod is not None, "la partie n'appartient a aucune assemblee"
        code = pod[0]
        if action == 'verser':
            Assemblee.VerserJetons(code, int(arguments[0]))
        elif action == 'envoyer':
            Assemblee.EnvoyerJeton(code, str(arguments[0]))
        elif action == 'terminer':
            Assemblee.Terminer(code, str(arguments[0]), bool(arguments[1]))
        else:
            raise AssertionError(f"action d'assemblee inconnue : {action}")

    def SendRoundEnd(self) -> None:
        """AJOUT (21/10/2026, Punisher MC×DC, Target Lock DISTRACTED « At the end of the round, flip this card ») : envoie
        `WhenRoundEnd`, que `EndRound` (mode manuel) ne partait jamais, pour tester un effet « a la fin de la manche »."""
        from game.message import Message
        Message.WhenRoundEnd(self.world).Send()

    def SendAfterRoundEnd(self) -> None:
        """AJOUT (22/10/2026, PU-7 M5, Overdrive « After the round ends ») : `WhenRoundEnd` PUIS `AfterRoundEnd`, comme `World.RoundLoop`."""
        from game.message import Message
        fin = Message.WhenRoundEnd(self.world)
        fin.Send()
        Message.AfterRoundEnd(fin).Send()

    def SendGameWouldBegin(self) -> None:
        """AJOUT (22/10/2026, Punisher MC×DC, pu141 « Setup : ... ») : envoie `WhenGameWouldBegin`, que `AbilityFactory.AfterGameSetup` ecoute
        et que le harnais manquait toujours (le message part une fois, a la FIN de la mise en place, avant le montage d'un cas)."""
        from game.message import Message
        Message.WhenGameWouldBegin(self.world).Send()

    def SwapWithDeckTop(self, card: CardName, player: int=0, siege: int|None=None):
        """« Switch Card with top Deck Card » d'OCTGN (menu de la main).

        AJOUT (06/10/2026, lot 6 du mode manuel) : la carte part sur le DESSUS
        du deck du joueur, l'ancien dessus vient dans sa main. UNE commande,
        donc un seul Ctrl+Z. Deck vide : la carte part sur le deck, rien ne
        revient.
        """
        from game.operate.faces import Faces
        joueur = self._JoueurVise(player, siege)
        face = self.FindOrCreateFace(card)
        dessus = joueur.player_deck.GetAll()[-1:] if joueur.player_deck.GetAll() else []
        Faces.MoveAllTo([face], joueur.player_deck, self.debug_rule)
        if dessus and dessus[0] is not face:
            Faces.MoveAllTo([dessus[0]], joueur.hand_cards, self.debug_rule)

    def Mulligan(self, *cards: CardName, player: int=0, siege: int|None=None):
        """« Mulligan Hand » d'OCTGN : les cartes choisies vont en defausse,
        puis le joueur en repioche autant depuis le dessus de son deck.

        AJOUT (06/10/2026, lot 6 du mode manuel) : UNE commande, un seul
        Ctrl+Z. La pioche s'arrete si le deck est vide : remelanger la
        defausse reste un geste a part, comme sur OCTGN.
        """
        from game.operate.faces import Faces
        joueur = self._JoueurVise(player, siege)
        faces = [self.FindOrCreateFace(card) for card in cards]
        if faces:
            Faces.MoveAllTo(faces, joueur.discard_pile, self.debug_rule)
        for _ in faces:
            pioche = joueur.player_deck.GetAll()
            if not pioche:
                break
            Faces.MoveAllTo([pioche[-1]], joueur.hand_cards, self.debug_rule)

    def Shuffle(self, zone: str, player: int=0, siege: int|None=None):
        """Melange une pile."""
        self._ZoneParNom(zone, player, siege).Shuffle(self.debug_rule)

    def Attach(self, card: CardName, cible: CardName):
        """Pose une amelioration ou un soutien SUR une carte precise."""
        from game.operate.faces import Faces
        face = self.FindOrCreateFace(card)
        hote = self.FindOrCreateFace(cible)
        Faces.MoveAllTo([face], hote.components.inventory.deck, self.debug_rule)

    def AttachReel(self, card: CardName, cible: CardName):
        """Comme `Attach`, mais par le vrai rattachement (`AttachTo2`) : la carte devient
        « attachee » (`bind_face`) et ses capacites d'amelioration (Interrupt « attached
        enemy ») sont enregistrees. `Attach` ne fait que deplacer la carte."""
        from game.card.face.attribute.can_attach import CanAttach
        face = self.FindOrCreateFace(card)
        hote = self.FindFaceInPlay(cible)
        assert face.CastTo(CanAttach).AttachTo2(hote, self.debug_rule), f"{card} n'a pas pu s'attacher a {cible}"

    def Engage(self, card: CardName, player: int=0, siege: int|None=None):
        """Engage un sbire avec un joueur, ou l'en desengage s'il y est deja."""
        from game.operate.faces import Faces
        face = self.FindOrCreateFace(card)
        joueur = self._JoueurVise(player, siege)
        if face.card.area is joueur.engaged_minions:
            Faces.MoveAllTo([face], self.world.area_processing, self.debug_rule)
        else:
            Faces.MoveAllTo([face], joueur.engaged_minions, self.debug_rule)

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

    def AdvanceMainScheme(self, fois: int=1, to: str|None=None):
        """Fait AVANCER le complot principal, par le chemin du moteur.

        AJOUTE LE 19/09/2026 pour les EPREUVES DE CAMPAGNE : plusieurs
        recompenses ne dependent pas d'une carte posee, mais de l'ETAPE que le
        complot principal a atteinte avant la fin de la partie (« Security
        Breach » et « The Infinity Stones 1B completed » de L'Ombre du Titan
        Fou lisent l'etape active). Sans cette commande, poser cet etat
        demandait de deplacer une carte a la main dans la zone des complots
        principaux, ce qui contourne justement le moteur qu'on veut mesurer.

        Un appel = un pas, exactement comme en partie : depuis une face A, le
        pas retourne la carte sur sa face B ; depuis une face B, il prend
        l'etape suivante dans le deck des complots principaux. Aller de
        l'etape 1A a l'etape 2A demande donc `fois=2`.
        """
        for _ in range(max(1, fois)):
            schemes = self.world.area_schemes_main.Get()
            if not schemes:
                raise RuntimeError("aucun complot principal en jeu : rien a faire avancer")
            schemes[-1].Advance(to, self.debug_rule)

    def AdvanceVillain(self):
        """Fait passer le mechant au stade SUIVANT, par le chemin du moteur.

        Ajoute le 05/10/2026 pour le mode manuel (« vaincre ce stade », comme
        sur OCTGN) : meme pas que `AdvanceMainScheme`, sans passer par la
        defaite du mechant. La carte du stade courant va a la pile de
        victoire, la suivante prend sa place.
        """
        villains = Worlds.GetAllVillains(self.world)
        if not villains:
            raise RuntimeError("aucun mechant en jeu : rien a faire avancer")
        villains[0].Advance(self.debug_rule)

    ################################################################################
    # E4 : remise en etat depuis une capture du plateau (`puzzle_capture.py`).
    #
    # Une capture nomme chaque carte posee par une CLE (« e1 », « e2 »...) : viser
    # une carte par son identifiant serait ambigu des qu'un deck ou une defausse
    # en contient un double (`FindOrCreateFace` fouille les decks d'abord). Le
    # registre vit sur le monde, car `PuzzleHelper.Exec` fabrique un `RunPuzzle`
    # neuf a chaque appel.
    KINDS_RESTAURES = ('ally', 'support', 'minion', 'side_scheme', 'environment', 'upgrade')

    def _Registre(self) -> Dict[str, 'CardFace']:
        registre = getattr(self.world, 'puzzle_restaurees', None)
        if registre is None:
            registre = {}
            self.world.puzzle_restaurees = registre
        return registre

    def _CarteRestauree(self, cible: str) -> 'CardFace':
        face = self._Registre().get(cible)
        if face is not None:
            return face
        return self.FindFaceInPlay(cible)

    def _AppliquerEtat(self, face: 'CardFace', exhausted: bool|None, health: int|None,
                       statuses: List[List[Any]]|None, counters: List[List[Any]]|None,
                       tokens: List[List[Any]]|None, threat: int|None) -> None:
        """Pose l'etat voulu sur `face`. L'ordre compte : les cartes d'etat, compteurs
        et jetons d'abord, puis la menace, l'epuisement, et les PV EN DERNIER (une
        amelioration deja attachee peut changer les PV max)."""
        # Valeurs ABSOLUES : une carte qui arrive en jeu porte deja ses compteurs de
        # depart (Web-Shooter : 3), la capture dit ce qu'elle porte A LA FIN.
        composants = face.card.components
        if statuses is not None:
            voulus = {str(nom): int(n) for nom, n in statuses}
            for nom in ("Confused", "Stunned", "Tough", "Exposed", "Cloaked", "Dazed", "Intensified"):
                ecart = voulus.get(nom, 0) - getattr(composants.status, nom.lower())
                if ecart > 0:
                    self.AddStatus(face, nom, ecart)
                elif ecart < 0:
                    composants.status.DiscardStatusCard(nom, self.debug_rule, -ecart)
        if counters is not None:
            voulus = {str(nom): int(n) for nom, n in counters}
            for nom in set(voulus) | set(composants.counter.counters):
                ecart = voulus.get(nom, 0) - composants.counter.GetCounters(nom)
                if ecart:
                    self.Counter(face, nom, ecart)
        if tokens is not None:
            voulus = {str(nom): int(n) for nom, n in tokens}
            for nom in set(voulus) | set(composants.token.token):
                if nom == 'first_player_token' or (nom == 'threat' and threat is not None):
                    continue
                ecart = voulus.get(nom, 0) - composants.token.GetTokens(nom)
                if ecart:
                    self.Token(face, nom, ecart)
        if threat is not None:
            self.SetThreat(face, int(threat))
        if exhausted is True and face.IsReady():
            self.Exhaust(face)
        elif exhausted is False and not face.IsReady():
            self.Ready(face)
        if health is not None:
            self.SetHealth(face, int(health))

    def RestoreState(self, target: str, key: str|None=None, exhausted: bool|None=None,
                     health: int|None=None, statuses: List[List[Any]]|None=None,
                     counters: List[List[Any]]|None=None, tokens: List[List[Any]]|None=None,
                     threat: int|None=None) -> 'CardFace':
        """Regle l'etat d'une carte DEJA EN JEU (identite, mechant, complot principal,
        ou une carte posee par `RestoreCard`, designee par sa cle). `key` lui donne une
        cle, pour que `RestoreCard` puisse y attacher des ameliorations."""
        face = self._CarteRestauree(target)
        if key:
            self._Registre()[key] = face
        self._AppliquerEtat(face, exhausted, health, statuses, counters, tokens, threat)
        return face

    def RestoreCard(self, key: str, card: str, kind: str, siege: int=0, host: str|None=None,
                    engaged: bool=False, exhausted: bool|None=None, health: int|None=None,
                    statuses: List[List[Any]]|None=None, counters: List[List[Any]]|None=None,
                    tokens: List[List[Any]]|None=None, threat: int|None=None) -> 'CardFace':
        """Cree une carte NEUVE (jamais celle d'un deck, meme si l'identifiant s'y
        trouve) et la pose en jeu avec son etat. `kind` : ally, support, minion,
        side_scheme, environment, ou upgrade (alors `host` est la cle de la carte
        porteuse). `siege` est le joueur qui la controle (ou, pour un sbire, celui qui
        l'engage quand `engaged` est vrai)."""
        from game.card.face.base import ClassCard
        from game.card.face.attribute.can_attach import CanAttach
        assert kind in RunPuzzle.KINDS_RESTAURES, f"kind inconnu : {kind}"
        joueur = self.world.const_seat_order_players[siege]
        face = self.CreateCard(card)
        if ClassCard.IsType(face):
            face.card.SetOwner(joueur)
        if kind == 'upgrade':
            assert host, "une amelioration demande son porteur (host)"
            hote = self._Registre()[host]
            assert face.CastTo(CanAttach).AttachTo2(hote, self.debug_rule), f"{card} n'a pas pu s'attacher a {host}"
        else:
            # Les cartes des joueurs sont sous leur controle ; celles de la rencontre non.
            face.PutIntoPlay(joueur, self.debug_rule, under_control=kind in ('ally', 'support'))
            if kind == 'minion' and engaged and face.card.area is not joueur.engaged_minions:
                self.Engage(face, siege=siege)
        self._Registre()[key] = face
        self._AppliquerEtat(face, exhausted, health, statuses, counters, tokens, threat)
        return face

    ################################################################################
    #
    def ValidateObjective(self, index: int):
        """Valide a la main l'objectif LIBRE `index` (0 = le premier) ; peut finir le puzzle."""
        self.world.puzzle_objectives.ValidateFree(int(index))

    def Win(self):
        """Termine la partie par une VICTOIRE des joueurs.

        AJOUTE LE 19/09/2026, et il manquait vraiment : rien ne permettait de
        finir une partie a la demande. La consequence etait qu'aucun test ne
        pouvait aller jusqu'a la FIN d'un scenario — donc ni le carnet sortant
        d'une campagne (`WhenGameOver`), ni le panneau de recompenses, ni la
        partie SUIVANTE montee avec ce que la precedente a laisse. Tout ce qui
        se passe apres la derniere carte jouee etait hors de portee.

        Passe par `Worlds.SetGameOver`, le meme chemin qu'une vraie victoire
        (`32130` Save the School l'emprunte) : les capacites `WhenGameOver`
        partent, le carnet s'ecrit, la sauvegarde se ferme comme d'habitude.
        """
        from game.operate.worlds import Worlds
        Worlds.SetGameOver(True, self.debug_rule)

    def Lose(self):
        """Termine la partie par une DEFAITE des joueurs (voir `Win`)."""
        from game.operate.worlds import Worlds
        Worlds.SetGameOver(False, self.debug_rule)

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

