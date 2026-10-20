from . import *

################################################################################
# BRIQUE COMMUNE (20/10/2026) : PLUSIEURS MECHANTS EN JEU, UN SEUL « LE
# MECHANT » (campagnes Punisher MC×DC et Galactic Storm). Recette :
# docs/reference/RECETTES-MOTEUR.md §15.3.
#
# Vocabulaire des cartes, et l'appel qui le rend :
#   « the villain »                 Villains.TheVillain(effect)
#                                   (= Worlds.FindVillain, que 246 scripts
#                                   appellent deja : ils suivent la regle)
#   « a villain », « each villain »  Villains.All(effect), ou SetTarget(Villain)
#   « the active villain »          Villains.Active(effect) / SetActive(...)
#   « the leftmost villain »        Villains.Leftmost(effect)
#
# Sans regle posee (toutes les parties ordinaires, Sinister Six, Wrecking
# Crew...), RIEN ne change : `Scenario.GetVillain` garde son ordre (crochet
# `GettingVillain` du scenario, puis compteur « active », puis le premier en
# jeu). Un scenario a plusieurs mechants pose sa regle a la mise en place :
#
#   Villains.SetRule(effect, Villains.Rule(the_villain="Leftmost",
#                                          player_cards="PlayerChooses"))
#
# - `the_villain="Active"` (Punisher p180 « Punisher is the active villain.
#   Encounter cards referring to or affecting "the villain" refer only to
#   Punisher ») : le mechant qui porte le compteur « active » ; a defaut, le
#   plus a gauche.
# - `the_villain="Leftmost"` (Galactic Storm p.16 « Encounter cards that refer
#   to "the villain" only refer to the leftmost villain ») : le premier de la
#   zone des mechants, qui garde l'ordre d'arrivee (un mechant revele va a
#   DROITE, `Villains.RevealNextVillain`).
# - `player_cards="PlayerChooses"` (Galactic Storm p.16 « Player cards that
#   refer to "the villain" only refer to the villain chosen by the player who
#   controls that player card ») : une question par effet, memorisee sur
#   l'effet ; les mechants insensibles aux cartes joueur (brique 2) ne sont
#   pas proposes tant qu'il en reste un autre. Vaut aussi pour l'exces d'un
#   coup overkill du joueur sur un sbire (« the attacking player must choose
#   which villain that excess damage is dealt to »).
# - Une carte (rencontre OU joueur) ATTACHEE a un mechant designe ce mechant
#   (« Encounter and player cards attached to a villain that refer to "the
#   villain" only refer to the attached villain »).
#
class Villains:

    class Rule:
        def __init__(self, *,
                     the_villain: Literal["Active", "Leftmost"]="Active",
                     player_cards: Literal["TheVillain", "PlayerChooses"]="TheVillain") -> None:
            assert the_villain in ("Active", "Leftmost"), f"{the_villain=}"
            assert player_cards in ("TheVillain", "PlayerChooses"), f"{player_cards=}"
            self.the_villain = the_villain
            self.player_cards = player_cards

        def __repr__(self) -> str:
            return f"Villains.Rule(the_villain={self.the_villain!r}, player_cards={self.player_cards!r})"

    ############################################################################
    # La regle
    @staticmethod
    def SetRule(effect_or_world: 'Effect|World', rule: 'Villains.Rule|None') -> None:
        from game.operate.worlds import Worlds
        Worlds.CastWorld(effect_or_world).GetScenario().regle_mechants = rule

    @staticmethod
    def GetRule(effect_or_world: 'Effect|World') -> 'Villains.Rule|None':
        from game.operate.worlds import Worlds
        return getattr(Worlds.CastWorld(effect_or_world).GetScenario(), 'regle_mechants', None)

    ############################################################################
    # Lire
    @staticmethod
    def TheVillain(effect: 'Effect') -> 'Villain|None':
        from game.operate.worlds import Worlds
        return Worlds.FindVillain(effect)

    @staticmethod
    def All(effect: 'Effect') -> List['Villain']:
        """« a villain » / « each villain » : tous les mechants de la zone de
        jeu de l'effet, de gauche a droite."""
        from game.operate.worlds import Worlds
        return Worlds.GetVillains(effect)

    @staticmethod
    def Leftmost(effect: 'Effect') -> 'Villain|None':
        mechants = Villains.All(effect)
        return mechants[0] if mechants else None

    @staticmethod
    def Rightmost(effect: 'Effect') -> 'Villain|None':
        mechants = Villains.All(effect)
        return mechants[-1] if mechants else None

    @staticmethod
    def Active(effect: 'Effect') -> 'Villain|None':
        for mechant in Villains.All(effect):
            if mechant.IsActive():
                return mechant
        return None

    ############################################################################
    # Agir
    @staticmethod
    def SetActive(villain: 'Villain', effect: 'Effect') -> None:
        """Pose le compteur « active » sur ce mechant (et l'ote aux autres)."""
        villain.SetActive(effect)

    @staticmethod
    def Remove(villain: 'Villain', effect: 'Effect') -> None:
        """Retire ce mechant de la partie SANS RIEN REPORTER (Galactic Storm
        p.16 « all tokens, status cards, and attachments on the just-defeated
        villain are discarded instead of carrying over to the next villain ») :
        attachements et ameliorations a la defausse, cartes d'etat defaussees,
        puis la carte quitte la partie (ses compteurs et jetons avec elle).
        Le compteur « active » qu'il portait disparait avec lui : avec
        `the_villain="Active"`, « le mechant » retombe alors sur le plus a
        gauche jusqu'a ce qu'un autre soit designe."""
        from game.operate.faces import Faces
        from game.card.face.attribute.can_status import CanStatus
        attaches = list(villain.GetInventoryDeck().GetAll())
        if attaches:
            Faces.DiscardAll(attaches, effect)
        if CanStatus.IsType(villain):
            statut = villain.components.status
            with statut.SansRemplacement():
                villain.DiscardEachStatus(effect)
        Faces.RemoveAllFromGame([villain], effect)

    @staticmethod
    def BuildVillainDeck(villains: Sequence['Villain'], effect: 'Effect') -> 'Deck':
        """Le DECK DE MECHANTS (Galactic Storm p.16, Earth Under Siege) : les
        cartes donnees, melangees, face cachee, hors jeu. Distinct de
        `Scenario.villain_deck`, qui porte les STADES du mechant ordinaire."""
        from game.operate.faces import Faces
        deck = Villains._VillainDeck(effect)
        if villains:
            Faces.ShuffleAllTo(list(villains), deck, effect)
        return deck

    @staticmethod
    def RevealNextVillain(player: 'Player', effect: 'Effect') -> 'Villain|None':
        """Revele le dessus du deck de mechants et le met en jeu le plus a
        DROITE (« place the newly revealed villain as the rightmost villain,
        so that the villain that has been in play the longest is always the
        leftmost villain »). Rend le mechant, ou None si le deck est vide."""
        deck = Villains._VillainDeck(effect)
        haut = deck.GetTop()
        if haut is None:
            return None
        haut.PutIntoPlay(player, effect)
        return haut.card.face

    @staticmethod
    def VillainDeckSize(effect: 'Effect') -> int:
        deck = getattr(Villains._Scenario(effect), 'deck_de_mechants', None)
        return deck.GetSize() if deck is not None else 0

    ############################################################################
    # Interne
    @staticmethod
    def _Scenario(effect: 'Effect|World') -> 'Scenario':
        from game.operate.worlds import Worlds
        return Worlds.CastWorld(effect).GetScenario()

    @staticmethod
    def _VillainDeck(effect: 'Effect') -> 'Deck':
        # Cree A LA DEMANDE : un deck de plus a la creation de chaque scenario
        # decalerait la numerotation des objets de toutes les parties.
        from game.deck import Deck2, DeckType
        from game.card.face.base import Villain
        scenario = Villains._Scenario(effect)
        deck = getattr(scenario, 'deck_de_mechants', None)
        if deck is None:
            deck = Deck2(scenario, DeckType.VillainDeck, Villain)
            scenario.deck_de_mechants = deck
        return deck

    @staticmethod
    def Resolve(villains: List['Villain'], rule: 'Villains.Rule', by_effect: 'Effect|None') -> 'Villain|None':
        """« Le mechant » selon la regle, parmi `villains` (deja filtres par
        zone de jeu, de gauche a droite). Appele par `Scenario.GetVillain`."""
        from game.operate.immunity import PlayerCardImmunity
        from game.card.face.attribute.can_attach import CanAttach
        from game.card.face.base import Villain
        if not villains:
            return None

        this = getattr(by_effect, 'this', None) if by_effect is not None else None
        if this is not None and CanAttach.IsType(this):
            porteur = getattr(this, 'bind_face', None)
            if porteur is not None and Villain.IsType(porteur) and porteur in villains:
                return porteur

        if rule.player_cards == "PlayerChooses" and len(villains) > 1 and \
                PlayerCardImmunity.IsPlayerCardEffect(by_effect):
            deja = getattr(by_effect, '_mechant_choisi', None)
            if deja is not None and deja in villains:
                return deja
            candidats = [v for v in villains if not PlayerCardImmunity.IsProtected(v)] or villains
            if len(candidats) == 1:
                choisi = candidats[0]
            else:
                from game.player import Player
                joueur = this.GetControlByOrOwner() if this is not None else None
                if not Player.IsType(joueur):
                    from game.operate.worlds import Worlds
                    joueur = Worlds.GetFirstPlayer(by_effect)
                choisi = joueur.AskChooseFace(candidats, by_effect, prompt="Choose the villain") or candidats[0]
            by_effect._mechant_choisi = choisi
            return choisi

        if rule.the_villain == "Active":
            for mechant in villains:
                if mechant.IsActive():
                    return mechant
        return villains[0]
