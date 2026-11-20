"""Les 3 fils du tchat reconstruit (chantier du 06/11/2026) : general (avec
anonymes), prives (inchanges) et table (ephemere, ouvert aux spectateurs).

Sur une base jetable, comme `test_inviter_un_connecte.py`. Appelle les
fonctions d'`orchestrateur.py` directement, sans passer par HTTP : ce qui
nous interesse ici est le comportement du fil, pas le routage (couvert par
`test_routes_chemin.py` et par le test HTTP du moteur, cote Fusion).

Usage : python3 site/test_tchat.py
"""
import os
import sqlite3
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
dossier = tempfile.mkdtemp(prefix="tchat-")
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
    cx.execute("INSERT INTO comptes (pseudo, email, sel, empreinte, statut, cree)"
               " VALUES ('arnaud', 'arnaud@x.be', 's', 'e', 'valide', '2026-11-06')")
    cx.execute("INSERT INTO comptes (pseudo, email, sel, empreinte, statut, cree)"
               " VALUES ('julie', 'julie@x.be', 's', 'e', 'valide', '2026-11-06')")

# --- Fil general : anonymes ------------------------------------------------

verifier("un pseudo anonyme ordinaire est accepte",
         o.pseudo_anonyme_valide("visiteur_42") == "visiteur_42")
verifier("un pseudo anonyme vide est refuse", o.pseudo_anonyme_valide("   ") == "")
verifier("un anonyme ne peut pas usurper un pseudo de compte existant",
         o.pseudo_anonyme_valide("arnaud") == "")
verifier("la casse ne protege pas de l'usurpation",
         o.pseudo_anonyme_valide("ARNAUD") == "")

o.dire("visiteur_42", "coucou tout le monde")
o.dire("arnaud", "salut !")
messages = o.messages_depuis(0)
verifier("le fil general voit le message de l'anonyme et celui du compte",
         [m["pseudo"] for m in messages] == ["visiteur_42", "arnaud"], str(messages))

# Debit anonyme : la limite coupe au-dela du plafond, pas avant.
adresse = "1.2.3.4"
anciens = o.ANONYMES_PAR_HEURE
o.ANONYMES_PAR_HEURE = 3
o._ENVOIS_ANONYMES.clear()
resultats_debit = [o.debit_anonyme_ok(adresse) for _ in range(4)]
verifier("debit anonyme : les 3 premiers passent, le 4e est refuse",
         resultats_debit == [True, True, True, False], str(resultats_debit))
o.ANONYMES_PAR_HEURE = anciens

# --- Messages prives : inchanges, reserves aux comptes ---------------------

o.dire("arnaud", "un secret", "julie")
prives = o.messages_depuis(0, moi="julie", avec="arnaud")
verifier("un prive entre deux comptes se lit normalement",
         len(prives) == 1 and prives[0]["texte"] == "un secret", str(prives))
o.dire("arnaud", "pour un pseudo qui n'existe pas", "personne_inconnue")
verifier("un prive vers un pseudo sans compte est ignore (silencieux)",
         o.messages_depuis(0, moi="personne_inconnue", avec="arnaud") == [])

# --- Fil de table : ephemere, ouvert a tout siege ---------------------------

o.dire_table("table-1", "Hôte", "on commence ?")
o.dire_table("table-1", "Invité 1", "oui !")
o.dire_table("table-2", "Hôte", "autre table, autre fil")

fil1 = o.messages_table_depuis("table-1")
verifier("le fil de la table 1 ne voit que ses propres messages",
         [m["pseudo"] for m in fil1] == ["Hôte", "Invité 1"], str(fil1))
fil2 = o.messages_table_depuis("table-2")
verifier("le fil de la table 2 est independant du fil de la table 1",
         [m["texte"] for m in fil2] == ["autre table, autre fil"], str(fil2))

depuis = fil1[0]["id"]
suite = o.messages_table_depuis("table-1", depuis)
verifier("`depuis` ne renvoie que les messages suivants",
         [m["pseudo"] for m in suite] == ["Invité 1"], str(suite))

o.effacer_messages_table("table-1")
verifier("une table eteinte perd tout son fil",
         o.messages_table_depuis("table-1") == [])
verifier("eteindre la table 1 ne touche pas la table 2",
         len(o.messages_table_depuis("table-2")) == 1)

# Purge par age : un message trop vieux disparait au prochain ecrit, meme
# sur une AUTRE table (filet de securite pour les tables jamais eteintes).
o.dire_table("table-3", "quelqu'un", "message qui va vieillir")
with sqlite3.connect(os.environ["BASE"]) as cx:
    cx.execute("UPDATE messages_table SET quand = '2020-01-01T00:00:00+00:00'"
               " WHERE table_id = 'table-3'")
o.dire_table("table-4", "quelqu'un d'autre", "un message neuf ailleurs")
verifier("un message de table trop vieux est purge par le filet de securite",
         o.messages_table_depuis("table-3") == [])
verifier("la purge par age ne touche pas un message neuf",
         len(o.messages_table_depuis("table-4")) == 1)

# --- Drapeaux de langues (chantier du 06/11/2026) -------------------------

verifier("une langue valide seule passe telle quelle",
         o.langues_tchat_valides("fr") == "fr")
verifier("une langue inconnue est filtree",
         o.langues_tchat_valides("fr,xx,en") == "fr,en")
verifier("les doublons sont retires, l'ordre d'arrivee garde",
         o.langues_tchat_valides("en,fr,en") == "en,fr")
verifier("vide ou n'importe quoi rend une chaine vide",
         o.langues_tchat_valides("") == "" and o.langues_tchat_valides("xx,yy") == "")

o.dire("julie", "bonjour", langues="fr,en")
dernier_general = o.messages_depuis(0)[-1]
verifier("le message general garde les langues de son auteur",
         dernier_general["langues"] == "fr,en", str(dernier_general))

o.dire_table("table-5", "quelqu'un", "hallo", langues="de,xx")
message_table = o.messages_table_depuis("table-5")[-1]
verifier("le fil de table garde aussi les langues, filtrees des codes invalides",
         message_table["langues"] == "de", str(message_table))

verifier("un compte sans langues enregistrees n'en a aucune",
         o.langues_du_compte("arnaud") == "")
verifier("definir_langues_du_compte enregistre, et rend la valeur gardee",
         o.definir_langues_du_compte("arnaud", "es,xx,es") == "es")
verifier("la langue enregistree se relit ensuite au profil",
         o.langues_du_compte("arnaud") == "es")
o.definir_langues_du_compte("personne-ici", "fr")
verifier("un pseudo sans compte ne peut rien enregistrer",
         o.langues_du_compte("personne-ici") == "")

print()
print("TOUT PASSE" if not echecs else f"{len(echecs)} ÉCHEC(S)")
sys.exit(1 if echecs else 0)
