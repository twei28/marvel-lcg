"""Inviter un joueur connecté à sa table (13/10/2026).

Vérifie, sur une base jetable, le registre des invitations du site :
  1. seuls les comptes valides vus depuis moins de DELAI_PRESENCE sont
     « connectés », l'hôte exclu ;
  2. on n'invite ni soi-même, ni un absent, ni sans table, ni au siège 0 ;
  3. l'invité voit l'invitation SANS le lien ; il ne l'obtient qu'en acceptant ;
  4. l'hôte suit l'état par siège ; refus, absence de réponse, relance ;
  5. un autre compte ne peut pas répondre à la place de l'invité.

Usage : python3 site/test_inviter_un_connecte.py
"""
import os
import sqlite3
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
dossier = tempfile.mkdtemp(prefix="inviter-")
os.environ["BASE"] = os.path.join(dossier, "narwhal.db")
sys.path.insert(0, ICI)

import orchestrateur as o  # noqa: E402

echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom + (" | " + detail if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


o.initialiser_base()
with sqlite3.connect(os.environ["BASE"]) as cx:
    for pseudo, statut in (("hote", "valide"), ("marc", "valide"), ("julie", "valide"),
                           ("absent", "valide"), ("attente", "attente")):
        cx.execute("INSERT INTO comptes (pseudo, email, sel, empreinte, statut, cree)"
                   " VALUES (?, ?, 's', 'e', ?, '2026-10-13')", (pseudo, pseudo + "@x.be", statut))
for pseudo in ("hote", "marc", "julie", "attente"):
    o.toucher_presence(pseudo)
with sqlite3.connect(os.environ["BASE"]) as cx:
    cx.execute("UPDATE comptes SET vu_le='2026-01-01T00:00:00+00:00' WHERE pseudo='absent'")

# 1. Connectés
verifier("connectés : valides et récents, hôte exclu",
         sorted(o.connectes(sauf="hote")) == ["julie", "marc"], str(o.connectes(sauf="hote")))

# 2. Refus
verifier("pas d'invitation sans table", o.inviter_a_la_table("hote", "marc", 1) == "pas de table")


class FausseTable:
    cles_sieges = ["k0", "k1", "k2", "k3"]

    def vivant(self):
        return True

    def base_url(self):
        return "https://p3.exemple.be"


o.PARTIES["hote"] = FausseTable()
verifier("on ne s'invite pas soi-même", o.inviter_a_la_table("hote", "hote", 1) == "invite inconnu")
verifier("on n'invite pas un absent", o.inviter_a_la_table("hote", "absent", 1) == "pas connecte")
verifier("le siège 0 est celui de l'hôte", o.inviter_a_la_table("hote", "marc", 0) == "siege invalide")
verifier("pas de siège au-delà de 3", o.inviter_a_la_table("hote", "marc", 4) == "siege invalide")

# 3. Invitation reçue sans le lien, lien à l'acceptation
inv = o.inviter_a_la_table("hote", "marc", 1)
verifier("invitation créée", isinstance(inv, dict), str(inv))
recues = o.invitations_pour("marc")
verifier("Marc voit l'invitation de l'hôte pour le siège 1",
         len(recues) == 1 and recues[0]["hote"] == "hote" and recues[0]["siege"] == 1, str(recues))
verifier("la liste ne contient jamais le lien", all("lien" not in r for r in recues))
verifier("Julie ne voit rien", o.invitations_pour("julie") == [])
verifier("l'hôte lit « envoyée » au siège 1",
         o.invitations_de("hote").get("1") == {"invite": "marc", "etat": "envoyee"}, str(o.invitations_de("hote")))

# 5. Un autre compte ne répond pas à la place de Marc
verifier("Julie ne peut pas accepter pour Marc", o.repondre_invitation("julie", recues[0]["id"], True) is None)

lien = o.repondre_invitation("marc", recues[0]["id"], True)
verifier("en acceptant, Marc reçoit le lien de SON siège",
         lien == "https://p3.exemple.be/claim_seat?p=1&key=k1&to=salon", str(lien))
verifier("l'hôte lit « acceptée »", o.invitations_de("hote")["1"]["etat"] == "acceptee")
verifier("une invitation acceptée ne se rejoue pas", o.repondre_invitation("marc", recues[0]["id"], True) is None)
verifier("plus rien n'attend Marc", o.invitations_pour("marc") == [])

# 4. Refus, sans réponse, relance
inv2 = o.inviter_a_la_table("hote", "julie", 2)
o.repondre_invitation("julie", inv2["id"], False)
verifier("refus lu par l'hôte", o.invitations_de("hote")["2"]["etat"] == "refusee")

inv3 = o.inviter_a_la_table("hote", "julie", 2)
o.INVITATIONS_TABLE[inv3["id"]]["cree"] -= o.DUREE_INVITATION + 1
verifier("sans réponse après le délai", o.invitations_de("hote")["2"]["etat"] == "sans_reponse")
verifier("une invitation éteinte ne s'affiche plus chez l'invitée", o.invitations_pour("julie") == [])
verifier("ni ne s'accepte", o.repondre_invitation("julie", inv3["id"], True) is None)

inv4 = o.inviter_a_la_table("hote", "julie", 2)
verifier("relancer rouvre l'invitation", o.invitations_de("hote")["2"]["etat"] == "envoyee")
inv5 = o.inviter_a_la_table("hote", "marc", 2)
verifier("une nouvelle invitation au même siège remplace l'ancienne",
         o.invitations_pour("julie") == [] and o.invitations_de("hote")["2"]["invite"] == "marc",
         str(o.invitations_de("hote")))

# 6. Les decks du compte de l'invité (décision 3)
import json  # noqa: E402
jeu = os.path.join(dossier, "jeu")
o.RACINE_JEU = jeu
with sqlite3.connect(os.environ["BASE"]) as cx:
    cx.execute("UPDATE comptes SET emplacement=7 WHERE pseudo='marc'")
    cx.execute("UPDATE comptes SET emplacement=8 WHERE pseudo='julie'")
for place, nom in ((7, "spidey-justice"), (8, "deck-de-julie")):
    d = os.path.join(jeu, ".game", "deck", f"serveur-{place}")
    os.makedirs(d, exist_ok=True)
    json.dump({"name": nom, "hero": ["01001a"]}, open(os.path.join(d, nom + ".json"), "w"))
open(os.path.join(jeu, ".game", "deck", "serveur-7", "casse.json"), "w").write("{pas du json")

verifier("pas de decks sans invitation acceptée au siège",
         o.decks_de_l_invite("hote", 3) == {"invite": "", "decks": []})
lus = o.decks_de_l_invite("hote", 1)
verifier("siège 1 (Marc a accepté) : les decks de Marc, et seulement eux",
         lus["invite"] == "marc" and [d["id"] for d in lus["decks"]] == ["spidey-justice"], str(lus))
verifier("un autre hôte ne lit pas les decks de Marc", o.decks_de_l_invite("julie", 1)["decks"] == [])

print()
print("TOUT PASSE" if not echecs else f"{len(echecs)} ÉCHEC(S)")
sys.exit(1 if echecs else 0)
