from game.card.face import *
from game.player import *

class EncounterCard(CanSurge, CanAccelerationToken, CardFace):
    pass

class EncounterNonVillainCard(HasBoostIcon, CanIncite, HasVictory, HasPeril, EncounterCard):

    def IsNemesis(self, player: 'Player') -> bool:
        # CORRECTIF (02/09/2026) : la carte est-elle DANS le set nemesis de CE
        # joueur ? C'est la seule question qui compte, et le deck de depart y
        # repond deja par sa cle `nemesis_set`. Le marqueur est pose a la mise
        # en place (`player_setup.py`, etape 5) et suit la carte partout.
        #
        # Le test par NOM DE SET conserve juste en dessous ne marchait que pour
        # un heros dont le set nemesis porte son propre nom. Des qu'un deck
        # EMPRUNTE le set d'un autre — cas courant des packs fan-made, dont les
        # auteurs ne livrent pas toujours de nemesis — il rendait False, et
        # `01190` Shadow of the Past (set STANDARD, donc a chaque partie) ne
        # mettait jamais le sbire en jeu. Detail et preuve : commentaire de
        # `player_setup.py`.
        #
        # AJOUT PUR : ce chemin ne peut que transformer un False en True, et
        # seulement pour une carte reellement declaree dans le `nemesis_set` du
        # joueur. Aucun heros officiel ne change de comportement, son set
        # portant deja son nom.
        if getattr(self, "nemesis_of_player", None) is player:
            # CORRECTIF (04/10/2026). Le marqueur dit « cette carte est dans
            # le set nemesis du joueur », PAS « c'est son sbire nemesis ». Un
            # set peut tenir deux sbires : Ares et la Lernean Hydra (Hercules),
            # Taskmaster et Hydra Mercenary (Black Widow), 37 heros officiels
            # en tout. Rendre True pour tous mettait le second en jeu avec le
            # premier (Face the Past, Shadow of the Past). Regle choisie par
            # l'utilisateur : si le set contient un sbire MARQUE « Nemesis »,
            # lui seul compte ; sinon (Zzzax emprunte par Viv Vision, sbire de
            # module sans mention), le sbire du set compte.
            from game.card.face.card_type import Minion
            if (Minion.IsType(self) and not self.nemesis
                    and getattr(player, "set_nemesis_a_un_sbire_marque", False)):
                return False
            return True

        if not self.paper.set_name.endswith(" Nemesis"):
            return False
        identity = player.GetIdentity()
        from game.card.face.card_type import Minion
        if Minion.IsType(self):
            if not self.nemesis:
                return False
        # We cannot use this, see "01167" and "27058"
        #     return player.IsName(self.nemesis)
        if identity.paper.set_name == "Spider-Man - Miles Morales":
            return self.paper.set_name[:-8] == "Spider-Man - Morales"
        return identity.paper.set_name == self.paper.set_name[:-8]


