"""Un siege TENU reste-t-il accorde quand la phase change ?

POURQUOI CE TEST EXISTE
-----------------------
Signale en jeu le 09/09/2026 : « il me sort toujours pas la premiere main pour
pouvoir mulligan », sur une table LOCALE A DEUX HEROS d'un serveur protege. La
mise en place s'arretait avant « Draw Cards ».

La chaine, mesuree ce jour-la avec une sonde dans `get_player_ids` :

    /ws?hot_seat&p=0   -> allowed=[0,1,2,3]  ids=[0,1]
    /get_ask?p=0       -> allowed=[2,3]      ids=[]

Le plateau annonce le hot-seat sur le SOCKET et sur l'accuse de reception, mais
`/get_ask` et `/post` sont per-siege et ne le portent pas. Un siege sans mot de
passe prouve n'etait accorde que tant qu'il etait ORPHELIN : des que le socket
hot-seat le tenait, il cessait de l'etre, la reprise tombait au premier
changement de phase, et plus rien ne le rendait. Le moteur posait sa question au
siege 1, le client ne la voyait jamais.

CE QUE LE TEST VERROUILLE, DANS LES DEUX SENS
--------------------------------------------
  1. un siege orphelin est accorde (la reprise d'origine, inchangee) ;
  2. il le RESTE quand la phase change alors qu'un client le tient ;
  3. il est RENDU quand la phase change ET qu'il est redevenu orphelin ;
  4. sans mot de passe de siege, la protection reste coupee (None).

Usage: python3.10 tools/test_sieges_reprise.py
"""
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))
os.environ.setdefault("RELEASE", "1")


class FausseRequete:
    def __init__(self, cookies=None):
        self.cookies = cookies or {}


class FauxClientManager:
    def __init__(self):
        self.tenus = set()

    def GetClients(self, seat):
        return ["client"] if seat in self.tenus else []


class FauxDeviceManager:
    def __init__(self):
        self.client_manager = FauxClientManager()


def cas(nom, obtenu, attendu, echecs):
    if obtenu == attendu:
        print(f"  ok    {nom}")
        return echecs
    print(f"  ECHEC {nom} : attendu {attendu!r}, obtenu {obtenu!r}")
    return echecs + 1


def main():
    from engine.device.web.server import server_base
    from engine.device.web.server.server_base import GameServerBase

    serveur = object.__new__(GameServerBase)
    serveur.device_manager = FauxDeviceManager()
    # `phase_courante` lit `self.game.world` ; on la remplace par une valeur
    # qu'on pilote, c'est la phase qui est le sujet du test.
    phase = {"valeur": "Round 0 / Scenario Setup"}
    serveur.phase_courante = lambda: phase["valeur"]

    echecs = 0
    server_base.SEAT_PASSWORDS.value = ["a", "b", "c", "d"]

    # 1. Sieges orphelins : tous accordes (reprise d'origine).
    echecs = cas("un plateau qui arrive prend les sieges orphelins",
                 sorted(serveur.allowed_seats(FausseRequete())), [0, 1, 2, 3], echecs)

    # 2. Le client tient maintenant 0 et 1 (socket hot-seat), et la phase change.
    serveur.device_manager.client_manager.tenus = {0, 1}
    phase["valeur"] = "Round 1 / Player"
    echecs = cas("un siege TENU reste accorde quand la phase change",
                 sorted(serveur.allowed_seats(FausseRequete())), [0, 1, 2, 3], echecs)

    # 3. Le client s'en va : au changement de phase suivant, les sieges sont rendus.
    serveur.device_manager.client_manager.tenus = set()
    phase["valeur"] = "Round 2 / Villain"
    accordes = sorted(serveur.allowed_seats(FausseRequete()))
    # Ils redeviennent orphelins, donc re-accordes par la reprise : ce qu'on
    # verifie ici est que la MEMOIRE a bien ete liberee, pas l'inverse.
    echecs = cas("la memoire de reprise se vide quand le siege est lache",
                 serveur.seats_reprises().get(0) == "Round 2 / Villain", True, echecs)
    echecs = cas("et les sieges restent utilisables", accordes, [0, 1, 2, 3], echecs)

    # 4. Aucun mot de passe : protection coupee.
    server_base.SEAT_PASSWORDS.value = []
    echecs = cas("sans mot de passe, aucun filtrage",
                 serveur.allowed_seats(FausseRequete()), None, echecs)

    print(f"ECHECS : {echecs}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
