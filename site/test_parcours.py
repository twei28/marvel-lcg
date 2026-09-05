"""Le parcours du site : se connecter, puis tomber dans le jeu.

Le site n'est qu'une PORTE. Ces cas verifient qu'il ne s'interpose nulle part :
qui est connecte part vers son moteur, qui ne l'est pas voit le formulaire, et
la seule page intermediaire est l'attente du demarrage.

Usage : python3 site/test_parcours.py
"""
import os
import re
import sys
import tempfile

os.environ.setdefault("BASE", os.path.join(tempfile.gettempdir(), "nc-parcours.db"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orchestrateur as o  # noqa: E402

echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom
          + (" | " + detail if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


class FauxProcessus:
    def poll(self):
        return None


def allumer(pseudo="chloe", emplacement=2):
    partie = o.Partie(emplacement, pseudo, "Jeu de " + pseudo)
    partie.processus = FauxProcessus()
    partie.mot_de_passe = "MOTDEPASSE"
    partie.cles_sieges = ["cle0", "cle1", "cle2", "cle3"]
    o.PARTIES[pseudo] = partie
    return partie


# --- Le lien qui depose l'hote dans son jeu --------------------------------
partie = allumer()
lien = partie.lien_hote()
verifier("le lien de l'hote vise SON moteur", "127.0.0.1:2352" in lien, lien)
verifier("le lien reclame le siege 0", "p=0" in lien, lien)
verifier("le lien porte la cle du siege 0", "key=cle0" in lien, lien)
verifier("le lien mene a l'ecran des heros", "to=prepare" in lien, lien)

# Sans cle, `claim_seat` ne poserait aucun cookie et le moteur refuserait les
# liens d'invitation a l'hote lui-meme : le cas merite son garde-fou.
partie.cles_sieges = []
verifier("sans cle, le lien ne pretend pas en avoir une",
         "key=" in partie.lien_hote() and "key=cle" not in partie.lien_hote(),
         partie.lien_hote())
partie.cles_sieges = ["cle0", "cle1", "cle2", "cle3"]

# --- Les pages du site -----------------------------------------------------
attente = o.page_attente("chloe").decode("utf-8")
verifier("l'attente se rafraichit toute seule",
         'http-equiv="refresh"' in attente and "/entrer" in attente)
verifier("l'attente dit ce qu'on attend", "Ton jeu demarre" in attente)

o.ERREURS_DEMARRAGE["chloe"] = "Le moteur n'a pas repondu a temps."
casse = o.page_attente("chloe").decode("utf-8")
verifier("en cas d'echec, la page ne boucle PAS", 'http-equiv="refresh"' not in casse)
# `html.escape` transforme l'apostrophe en &#x27; : on cherche donc un
# morceau qui n'en contient pas, sans quoi le cas passerait a cote.
verifier("en cas d'echec, la raison est dite",
         "pas repondu a temps" in casse, casse[-400:])
verifier("en cas d'echec, on peut reessayer", "Reessayer" in casse)
o.ERREURS_DEMARRAGE.pop("chloe", None)

arret = o.page_arret("chloe").decode("utf-8")
verifier("l'arret rassure sur les donnees", "Rien n'est perdu" in arret)
verifier("l'arret propose de rallumer", "/entrer" in arret)

# --- Le bouton Administration n'est pose QUE pour l'administrateur ---------
# ⚠ On appelle VRAIMENT `_config_partie`. Se contenter de poser la cle
# soi-meme puis de la relire ne prouverait rien : le cas passerait au vert
# meme si la fonction ne faisait rien du tout.
reel = os.path.join(o.RACINE_JEU, "launch.json")
if os.path.isfile(reel):
    import json
    import shutil
    bac = tempfile.mkdtemp(prefix="nc-config-")
    shutil.copy(reel, os.path.join(bac, "launch.json"))
    racine_reelle = o.RACINE_JEU
    o.RACINE_JEU = bac                    # tout ce qui s'ecrit part au bac
    try:
        for pseudo, attendu in ((o.ADMIN, True), ("quelqu-un-dautre", False)):
            p2 = o.Partie(19, pseudo, "Jeu de " + pseudo)
            p2.mot_de_passe = "x"
            p2.cles_sieges = ["a", "b", "c", "d"]
            cfg = json.load(open(o._config_partie(19, p2), encoding="utf-8"))
            verifier("l'admin recoit le bouton Administration" if attendu
                     else "les autres comptes ne l'ont pas",
                     ("site_admin_url" in cfg) is attendu, json.dumps(cfg)[:150])
            verifier("les cles de siege sont transmises au moteur (%s)" % pseudo,
                     cfg.get("seat_passwords") == ["a", "b", "c", "d"],
                     str(cfg.get("seat_passwords")))
    finally:
        o.RACINE_JEU = racine_reelle
        shutil.rmtree(bac, ignore_errors=True)
else:
    print("  (launch.json absent : verification du bouton admin sautee)")

o.PARTIES.clear()
print()
print("ECHECS : %d" % len(echecs))
for e in echecs:
    print("  - " + e)
sys.exit(1 if echecs else 0)
