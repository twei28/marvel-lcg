"""Fin d'une partie competitive : qui gagne, et quand (livret mc56 p.17).

En partie ordinaire, la premiere condition atteinte termine la partie. Le
livret competitif dit le contraire : « The game does not end until both sides
have played an equal number of phases. » Une condition atteinte est donc
ENREGISTREE, pas appliquee ; la partie s'arrete a la fin de la phase du camp
resistance, qui est le second a jouer dans le round enfile (p.16).

Trois facons de gagner (p.17), lues depuis la table ou la chose arrive :

  * vaincre le leader qu'on affronte      -> point pour le camp de CETTE table ;
  * son complot principal accompli        -> point pour le camp d'EN FACE
    (« whichever team's leader completes its main scheme 2B first wins », et
    votre leader est sur la table d'en face) ;
  * tous ses heros vaincus                -> point pour le camp d'EN FACE.

Quand les deux camps marquent dans la meme fenetre, le livret tranche : deux
leaders vaincus = egalite, deux camps perdus = les deux perdent. Une egalite
passe alors par les cinq departages de la p.17.
"""
from typing import Final
from core import *


class Competitive:

    # Ce qu'un camp a fait, du point de vue de ce camp.
    VICTOIRE: Final = "victoire"
    DEFAITE: Final = "defaite"

    # Le camp qui joue en premier dans le round enfile (p.16). La partie ne
    # peut donc se terminer qu'a la fin d'une phase de l'AUTRE camp : c'est la
    # seule facon d'avoir joue autant de phases de part et d'autre.
    CAMP_PREMIER: Final = 0
    CAMP_DERNIER: Final = 1

    NOMS: Final = {0: "Registration", 1: "Resistance"}

    def __init__(self, world: 'World') -> None:
        self.world: Final = world
        # camp -> {VICTOIRE|DEFAITE: raison lisible}. Un camp peut porter les
        # deux : vaincre son leader et voir son complot s'accomplir dans la
        # meme fenetre est possible, et le livret n'en dit rien — on le traite
        # comme une egalite plutot que d'inventer une preseance.
        self.faits: Dict[int, Dict[str, str]] = {0: {}, 1: {}}
        self.by_effect: 'Effect|None' = None
        # Le camp gagnant une fois la partie finie, -1 s'il n'y en a pas.
        self.camp_gagnant: int = -1

    ################################################################################
    # Etape 3 de la mise en place : les 4 cartes joueur du leader (p.14)
    @staticmethod
    def CartesDuLeader(card_id: str) -> List[str]:
        """Les cartes JOUEUR du set d'un leader.

        « Each team finds their chosen leader's basic player cards and sets
        them aside » : ces cartes ne sont pas listees a part dans les donnees,
        elles vivent dans le set du leader a cote de ses stades, de ses
        attachements et de ses traitrises. Ce qui les distingue est leur TYPE,
        et c'est la seule chose sur laquelle s'appuyer : les huit leaders du
        jeu (4 de Civil War, 4 de Synthezoid) en ont exactement 4 chacun.
        """
        from cards.database import CardsDB
        from game.card.face.card_type import Ally, Event, Resource, Support, Upgrade

        paper = CardsDB.papers.get(card_id)
        if paper is None:
            return []
        types_joueur = (Ally, Event, Resource, Support, Upgrade)
        sortie: List[str] = []
        for autre_id in CardsDB.sets_cards.get(paper.set_name, []):
            autre = CardsDB.papers.get(autre_id)
            if autre is None or autre_id in sortie:
                continue
            # Le set d'un leader porte le nom du personnage, et ce nom est
            # DEJA celui d'un set de heros ailleurs : « Iron Man » designe
            # aussi les cartes du heros de la boite de base. Le pack tranche.
            if autre.pack != paper.pack:
                continue
            if issubclass(autre.GetType(), types_joueur):
                sortie.append(autre_id)
        return sortie

    ################################################################################
    # Enregistrement
    @property
    def en_attente(self) -> bool:
        return any(self.faits.values())

    def ADejaMarque(self, camp: int, quoi: str) -> bool:
        return quoi in self.faits.get(camp, {})

    def Enregistrer(self, camp: int, quoi: str, raison: str, by_effect: 'Effect|None') -> bool:
        """Note ce qu'un camp vient de faire. Rend toujours True, pour que
        l'appelant puisse ecrire `if world.competitive.Enregistrer(...): return`
        et laisser la partie continuer."""
        from game.message import Message

        if quoi not in self.faits[camp]:
            self.faits[camp][quoi] = raison
            if self.by_effect is None:
                self.by_effect = by_effect
            Message.TextRender(
                f"\n--- {self.NOMS[camp]} : {raison} "
                f"(la partie continue jusqu'a ce que les deux camps aient joue autant de phases) ---",
                self.world)
        return True

    def EnregistrerVictoire(self, camp: int, raison: str, by_effect: 'Effect|None') -> bool:
        return self.Enregistrer(camp, self.VICTOIRE, raison, by_effect)

    def EnregistrerDefaite(self, camp: int, raison: str, by_effect: 'Effect|None') -> bool:
        return self.Enregistrer(camp, self.DEFAITE, raison, by_effect)

    def LeaderEstVaincu(self, camp: int) -> bool:
        """Le leader pose sur la table de ce camp a deja ete vaincu.

        Il reste EN JEU jusqu'a la fin de la partie (p.17 : « it remains on the
        table [...] so it can still be targeted »), donc le moteur peut
        repasser par sa defaite : c'est ce garde-fou qui l'en empeche."""
        return self.ADejaMarque(camp, self.VICTOIRE)

    ################################################################################
    # Resolution
    def AFinDePhase(self, camp: 'int|None') -> None:
        """Appelee a la fin de chaque phase du round enfile.

        Le camp qui joue en dernier ferme la fenetre : a ce moment precis, les
        deux camps ont joue le meme nombre de phases."""
        if camp != self.CAMP_DERNIER or not self.en_attente:
            return
        self.Terminer()

    def Terminer(self) -> None:
        from game.message import Message
        from game.effect.rule import GameRule
        from game.operate.worlds import Worlds

        gagnant, raison = self.Verdict()
        self.camp_gagnant = gagnant if gagnant is not None else -1

        by_effect = self.by_effect
        if by_effect is None:
            schemes = Worlds.GetAllMainSchemes(self.world)
            by_effect = GameRule(schemes[0]) if schemes else None
        assert by_effect is not None

        for camp in (0, 1):
            for quoi, texte in self.faits[camp].items():
                Message.TextRender(f"> {self.NOMS[camp]} : {texte} ({quoi})", self.world)

        self.world.game_over.SetGameOver(raison, by_effect)

    def Verdict(self) -> 'Tuple[int|None, str]':
        """Le camp gagnant et la raison de fin exposee au client."""
        marques = self.Marques()
        marqueurs = [camp for camp in (0, 1) if marques[camp]]

        if len(marqueurs) == 1:
            return marqueurs[0], self.RaisonVictoire(marqueurs[0])

        if all(self.DEFAITE in self.faits[camp] for camp in (0, 1)) and \
                not any(self.VICTOIRE in self.faits[camp] for camp in (0, 1)):
            # « If the resistance team also lose the game [...] both teams lose
            # the game. » Pas de departage : personne ne gagne.
            return None, "Both Teams Lost"

        # Deux leaders vaincus dans la meme fenetre, ou un camp qui a fait les
        # deux : « the game is a tie » (p.17), et les cinq departages tranchent.
        camp = self.Departage()
        if camp is None:
            return None, "The Game is a Tie"
        return camp, self.RaisonVictoire(camp)

    def Marques(self) -> 'Dict[int, List[str]]':
        """Ce que chaque camp a marque EN SA FAVEUR.

        Une victoire compte pour le camp qui l'a obtenue ; une defaite compte
        pour le camp d'en face, parce que c'est SON leader qui a accompli son
        complot ou vaincu les heros (p.17)."""
        marques: Dict[int, List[str]] = {0: [], 1: []}
        for camp in (0, 1):
            for quoi, raison in self.faits[camp].items():
                gagnant = camp if quoi == self.VICTOIRE else self.world.GetOtherTeam(camp)
                marques[gagnant].append(raison)
        return marques

    def RaisonVictoire(self, camp: int) -> str:
        return "The Registration Team Won" if camp == 0 else "The Resistance Team Won"

    ################################################################################
    # Les cinq departages (p.17), dans l'ordre du livret
    def Departage(self) -> 'int|None':
        from game.message import Message

        for nom, mesure, le_moins_gagne in self.DEPARTAGES:
            valeurs = {camp: mesure(self, camp) for camp in (0, 1)}
            if valeurs[0] == valeurs[1]:
                continue
            if le_moins_gagne:
                camp = 0 if valeurs[0] < valeurs[1] else 1
            else:
                camp = 0 if valeurs[0] > valeurs[1] else 1
            Message.TextRender(
                f"> Departage : {nom} ({valeurs[0]} contre {valeurs[1]}) "
                f"-> {self.NOMS[camp]}", self.world)
            return camp
        return None

    def _Zone(self, camp: int) -> 'GameArea':
        return self.world.GetTeamGameArea(camp)

    def _ComplotPrincipal(self, camp: int) -> 'MainScheme|None':
        from game.operate.worlds import Worlds
        schemes = Worlds.GetMainSchemes(self._Zone(camp))
        return schemes[0] if schemes else None

    def _StadeDepasse(self, camp: int) -> int:
        """1 si le complot principal affronte par ce camp a depasse le stade 1B.

        « The team whose enemy main scheme deck did not advance past stage 1B
        wins » : c'est le complot de SA table, celui qu'il affronte."""
        scheme = self._ComplotPrincipal(camp)
        if scheme is None:
            return 0
        return 1 if getattr(scheme, "printed_stage", 1) > 1 else 0

    def _SbiresEtManigances(self, camp: int) -> int:
        from game.card.face.card_type import Minion
        from game.operate.worlds import Worlds
        zone = self._Zone(camp)
        sbires = [x for x in Worlds.GetOnFieldCards(zone) if Minion.IsType(x)]
        return len(sbires) + len(Worlds.GetSideSchemes(zone))

    def _MenaceSurLeComplot(self, camp: int) -> int:
        scheme = self._ComplotPrincipal(camp)
        if scheme is None:
            return 0
        return scheme.GetCounters('threat')

    def _PointsDeVieDesHeros(self, camp: int) -> int:
        total = 0
        for player in self.world.const_seat_order_players:
            if self.world.GetTeamOfPlayer(player) != camp or player.is_eliminated:
                continue
            identity = player.GetIdentity()
            total += max(0, getattr(identity, "health", 0))
        return total

    def _AttachementsSurLeLeader(self, camp: int) -> int:
        from game.operate.worlds import Worlds
        leader = Worlds.FindVillainByGameArea(self._Zone(camp))
        if leader is None:
            return 0
        return len(leader.GetAttachedAttachments())

    # (nom, mesure, le moins gagne)
    DEPARTAGES: Final = [
        ("complot principal reste au stade 1B", _StadeDepasse, True),
        ("sbires et manigances en zone", _SbiresEtManigances, True),
        ("menace sur le complot principal", _MenaceSurLeComplot, True),
        ("points de vie restants des identites", _PointsDeVieDesHeros, False),
        ("attachements sur le leader", _AttachementsSurLeLeader, True),
    ]
