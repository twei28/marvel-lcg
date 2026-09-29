"""L'activite Discord : une table par salon vocal.

`role_activite_discord` decide, pour CHAQUE visiteur d'une activite Discord,
s'il est l'hote (doit avoir un compte), un participant (choisit compte ou
invite), ou doit d'abord se connecter. Purement en memoire, testable sans
passer par HTTP.

Usage : python3 site/test_activite_discord.py
"""
import os
import sys
import tempfile

os.environ.setdefault("BASE", os.path.join(tempfile.gettempdir(), "nc-activite-discord.db"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orchestrateur as o  # noqa: E402

echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom
          + (" | " + detail if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


def instance_fraiche():
    """Un identifiant jamais vu, pour ne pas heriter d'un cas precedent."""
    import uuid
    return "instance-" + uuid.uuid4().hex[:12]


# --- Premiere ouverture, personne connecte : il faut se connecter ----------
inst = instance_fraiche()
role, hote = o.role_activite_discord(inst, None)
verifier("premiere ouverture sans compte -> connexion requise",
         role == "connexion_requise", role)
verifier("connexion requise ne nomme personne", hote is None, repr(hote))
verifier("aucune table n'a ete reservee tant que personne ne s'est identifie",
         inst not in o.INSTANCES_DISCORD)

# --- Premiere ouverture, connecte : devient l'hote --------------------------
inst = instance_fraiche()
role, hote = o.role_activite_discord(inst, "chloe")
verifier("premiere ouverture connecte -> hote", role == "hote", role)
verifier("l'hote porte son propre pseudo", hote == "chloe", repr(hote))
verifier("la table est desormais reservee a cette activite",
         o.INSTANCES_DISCORD.get(inst) == "chloe")

# --- Reouverture par le meme hote : reste hote ------------------------------
role, hote = o.role_activite_discord(inst, "chloe")
verifier("reouverture par l'hote -> toujours hote", role == "hote", role)
verifier("meme pseudo", hote == "chloe", repr(hote))

# --- Un autre visiteur, deja connecte sur SON propre compte : participant --
role, hote = o.role_activite_discord(inst, "marc")
verifier("un autre compte sur une activite deja prise -> participant",
         role == "participant", role)
verifier("participant : le pseudo rendu est celui de l'HOTE, pas le sien",
         hote == "chloe", repr(hote))

# --- Un invite (pas de compte) sur une activite deja prise : participant --
role, hote = o.role_activite_discord(inst, None)
verifier("invite sans compte sur une activite deja prise -> participant "
         "(pas connexion_requise : seul le PREMIER doit avoir un compte)",
         role == "participant", role)
verifier("l'invite voit bien le pseudo de l'hote", hote == "chloe", repr(hote))

# --- Deux activites differentes sont deux tables independantes -------------
inst_a = instance_fraiche()
inst_b = instance_fraiche()
_, hote_a = o.role_activite_discord(inst_a, "alice")
_, hote_b = o.role_activite_discord(inst_b, "bob")
verifier("deux salons vocaux distincts -> deux hotes distincts",
         hote_a == "alice" and hote_b == "bob", f"{hote_a} / {hote_b}")

# --- Course : deux ouvertures simultanees ne creent jamais deux hotes ------
# ⚠ Pas de vrai parallelisme ici (le GIL et l'absence de point de bascule
# entre la lecture et l'ecriture sous `VERROU` le rendraient invisible de
# toute facon) : ce cas verifie la PROPRIETE (idempotence), pas la course
# elle-meme.
inst = instance_fraiche()
resultats = [o.role_activite_discord(inst, p)[1] for p in ("premier", "second")]
verifier("deux pseudos qui se disputent la meme activite : un seul gagne",
         resultats[0] == resultats[1] == "premier", repr(resultats))

# --- Les sieges : un par personne, jamais deux fois le meme -----------------
inst = instance_fraiche()
o.role_activite_discord(inst, "hote")
sieges = [{"siege": n, "url": "u%d" % n} for n in (1, 2, 3)]
s1 = o.siege_activite_discord(inst, "marc", sieges)
s2 = o.siege_activite_discord(inst, "invite:abc", sieges)
verifier("le premier participant recoit le siege 1", s1 and s1["siege"] == 1, repr(s1))
verifier("le second recoit le siege 2, pas le meme", s2 and s2["siege"] == 2, repr(s2))
verifier("qui revient retrouve SON siege",
         o.siege_activite_discord(inst, "marc", sieges)["siege"] == 1)
s3 = o.siege_activite_discord(inst, "invite:def", sieges)
verifier("le troisieme recoit le siege 3", s3 and s3["siege"] == 3, repr(s3))
verifier("le quatrieme n'a plus de siege : table complete",
         o.siege_activite_discord(inst, "zoe", sieges) is None)
autre = instance_fraiche()
o.role_activite_discord(autre, "autre_hote")
verifier("un autre salon repart du siege 1",
         o.siege_activite_discord(autre, "marc", sieges)["siege"] == 1)
o.role_activite_discord(inst, "hote")
verifier("l'hote qui rouvre ne remet pas les sieges a zero",
         o.siege_activite_discord(inst, "zoe", sieges) is None)

print()
print("ECHECS : %d" % len(echecs))
for e in echecs:
    print("  - " + e)
sys.exit(1 if echecs else 0)
