"""Le fil de TABLE du tchat (chantier du 06/11/2026), cote moteur.

⚠ CE N'EST PAS `test_salon.py`. Ce dernier teste le SALON du wizard (choix
de heros/deck par siege, `salon.html`) : un nom qui designe deja autre chose
dans ce code, piege a ne pas reproduire ici. Ce fichier teste l'ACCES au fil
de tchat de la table (`get_salon_joueurs`/`post_salon_message`,
`salon=table`), cote `server_get.py` : qui a le droit de lire/ecrire, pas le
contenu des messages (couvert cote site par `site/test_tchat.py`).

Teste `_acces_salon_table`/`_pseudo_table` directement, sans demarrer de
vrai serveur HTTP ni le moteur de jeu : ce sont des fonctions pures de
`request.cookies` et de `SEAT_PASSWORDS`, inutile de payer le cout d'un
`Engine.Initialize()` pour les verifier.

Usage: python3 tools/test_salon_table.py <game_dir>
Viser .game-src-base (ou tout .game-src*), jamais .game.
"""
import os
import sys

GAME_DIR = os.path.expanduser(sys.argv[1])
os.chdir(GAME_DIR)
sys.path.insert(0, GAME_DIR)
os.environ.setdefault("RELEASE", "1")

resultats = []


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), detail))


from engine.device.web.server.server_get import GameServerGet  # noqa: E402
from engine.device.web.server.server_base import SEAT_PASSWORDS  # noqa: E402


class FauxRequest:
    def __init__(self, cookies=None):
        self.cookies = cookies or {}


class FauxServeur(GameServerGet):
    """Ne construit JAMAIS un vrai serveur : seules les methodes pures sur
    `request.cookies`/`SEAT_PASSWORDS` nous interessent ici."""
    def __init__(self):
        pass


serveur = FauxServeur()

# --- Sans aucune protection de siege (table locale) -------------------------
SEAT_PASSWORDS.value = []
verifier("sans protection : acces libre au fil de table",
         serveur._acces_salon_table(FauxRequest()) is True)

# --- Avec sieges proteges ----------------------------------------------------
SEAT_PASSWORDS.value = ["h0", "j1", "j2", "j3"]
import hashlib  # noqa: E402


def jeton(mot_de_passe):
    return hashlib.md5(mot_de_passe.encode()).hexdigest()


verifier("sans cookie du tout : refuse",
         serveur._acces_salon_table(FauxRequest()) is False)

cookie_siege1 = {"seat_token_1": jeton("j1")}
verifier("un siege occupe (invite) a acces au fil de table",
         serveur._acces_salon_table(FauxRequest(cookie_siege1)) is True)

cookie_faux = {"seat_token_1": jeton("faux")}
verifier("un mauvais jeton de siege n'a pas acces",
         serveur._acces_salon_table(FauxRequest(cookie_faux)) is False)

cookie_spectateur = {"spectateur": "1"}
verifier("un spectateur (cookie pose par le serveur) a acces au fil de table",
         serveur._acces_salon_table(FauxRequest(cookie_spectateur)) is True)

# ⚠ LE COOKIE SPECTATEUR NE SE FABRIQUE PAS SOI-MEME COTE NAVIGATEUR : c'est
# `est_spectateur` qui en depend entierement, et elle est deja testee
# ailleurs (server_base). Ici on verifie seulement qu'un spectateur passe,
# pas qu'il puisse se faire passer pour un spectateur sans l'etre — ce
# serait un test de `est_spectateur`, pas de `_acces_salon_table`.

# --- Le nom affiche dans le fil ---------------------------------------------
verifier("un spectateur s'affiche comme 'Spectateur'",
         serveur._pseudo_table(FauxRequest(cookie_spectateur), 0) == "Spectateur")
verifier("le siege 0 s'affiche comme 'Hôte'",
         serveur._pseudo_table(FauxRequest(cookie_siege1), 0) == "Hôte")
verifier("un siege invite s'affiche comme 'Invité <n>'",
         serveur._pseudo_table(FauxRequest(cookie_siege1), 1) == "Invité 1")

for nom, ok, detail in resultats:
    print(("OK    " if ok else "ECHEC ") + nom + ("" if ok else f"   [{detail}]"))
rates = [nom for nom, ok, _ in resultats if not ok]
print(("\nTOUT PASSE" if not rates else f"\n{len(rates)} ECHEC(S)"))
sys.exit(0 if not rates else 1)
