"""L'accusation d'Agents of S.H.I.E.L.D., scenario 5, en mode campagne.

Le pack d'origine avait deja cable toute la chaine (etapes 1B -> 2A -> 2B ->
3A -> 3B, table des 27 combinaisons dans `CalcMole`), mais elle etait INERTE en
campagne : `50167a` renonce a preparer les preuves, donc les deux enveloppes
n'existaient pas et `CalcMole` tombait sur un `assert False`.

En campagne, les enveloppes ne sont plus des paquets de cartes mais deux
lectures du carnet. Ce n'est pas un detail d'implementation : `SetAsideDeck`
inscrit ses piles dans `world.additional_decks`, que `to_descriptor` rend au
navigateur avec le `card_id` REEL de chaque carte, face cachee ou non. Monter
l'enveloppe A.I.M. en pile aurait rendu la taupe lisible depuis la console,
apres deux fuites deja fermees pour la meme raison. D'ou le dernier cas de
chaque serie, qui relit le descripteur.

Le pilote repond toujours la premiere option legale, donc les trois hypotheses
sont fixes : Dossiers medicaux, Argent, Habilitation. Juste ou faux se regle
alors en choisissant l'enveloppe A.I.M. du carnet, ce qui rend les deux
sanctions de la page 19 mesurables separement.

Usage : python3.10 tools/test_accusation_aos.py [racine] [port]
"""
import json
import os
import subprocess
import sys
import tempfile

RACINE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.expanduser(
    "~/marvel-work/fusion/marvel-lcg-src")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 4700
CAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cas_accusation_aos.py")

# Les hypotheses que le pilote finit toujours par choisir.
DOSSIERS, ARGENT, HABILITATION = "50185", "50188", "50191"
# Dossiers + Argent + Habilitation designent le Medecin en chef (50181),
# Scanner + Ideologie + Autorite le Chef tactique (50183). Releve sur le carnet
# imprime, et confirme par la table de `CalcMole` dans le pack.
TAUPE_MEDECIN = f"{DOSSIERS};{ARGENT};{HABILITATION}"
TAUPE_TACTIQUE = "50187;50190;50193"

resultats = []
port = PORT


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), detail))


def jouer(etape, carnet, campagne=True):
    global port
    port += 1
    rapport = os.path.join(tempfile.gettempdir(), f"accusation_aos_{os.getpid()}_{port}.json")
    env = dict(os.environ,
               RAPPORT=rapport,
               ETAPE=etape,
               CAMPAIGN_LOG=json.dumps(carnet),
               RULES=json.dumps(["mode_campaign"] if campagne else []))
    subprocess.run([sys.executable, CAS, RACINE, str(port)],
                   env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(rapport, encoding="utf-8") as f:
        sortie = json.load(f)
    os.remove(rapport)
    return sortie


def secrets(releve, base):
    """Les compteurs secrets d'un membre, quelle que soit sa face."""
    return sum(v for k, v in (releve.get("membres") or {}).items() if k.startswith(base))


def face_retournee(releve, base):
    return any(k == base + "b" for k in (releve.get("membres") or {}))


# --------------------------------------------------- puiser dans l'enveloppe --
# Quatre preuves deja gagnees, trois chez la taupe : il en reste deux.
d = jouer("puiser", {"A.I.M. Envelope": TAUPE_MEDECIN,
                     "Evidence Gained": "50186;50187;50189;50190"})
verifier("puiser : la partie tourne sans erreur", not d.get("erreurs"), d.get("erreurs"))
tirages = d.get("tirages") or []
verifier("l'enveloppe rend exactement les deux preuves restantes",
         len(tirages) == 3 and tirages[-1]["enveloppe_non_vide"] is False, tirages)
carnet = d.get("carnet_preuves") or ""
verifier("le carnet est cumulatif et compte six preuves",
         len(carnet.split(";")) == 6, carnet)
verifier("aucune preuve de l'enveloppe A.I.M. n'a ete puisee",
         not [x for x in carnet.split(";") if x in TAUPE_MEDECIN.split(";")], carnet)
verifier("les preuves puisees sont posees dans l'aire des preuves",
         sorted(d.get("aire_des_preuves") or []) == sorted(carnet.split(";")),
         (d.get("aire_des_preuves"), carnet))
verifier("puiser : rien de l'enveloppe ne part au navigateur",
         not d.get("preuves_dans_le_descripteur") and not d.get("descripteur_contient_le_secret"),
         (d.get("preuves_dans_le_descripteur"), d.get("descripteur_contient_le_secret")))

# ------------------------------------------- accusation : tout tombe juste --
# L'enveloppe EST Dossiers/Argent/Habilitation, exactement les hypotheses du
# pilote. Comme l'accuse DECOULE de la combinaison (livret p.19), viser juste
# sur les trois, c'est viser juste sur le membre : aucune sanction.
d = jouer("accuser", {"A.I.M. Envelope": TAUPE_MEDECIN})
verifier("accusation : la chaine 2A-2B-3A-3B se deroule sans erreur",
         not d.get("erreurs"), d.get("erreurs"))
verifier("la chaine s'arrete bien sur la derniere etape",
         d.get("manigances") == ["50169b"], d.get("manigances"))
verifier("Baron Zemo est demasque", d.get("villains") == ["50165b"], d.get("villains"))
verifier("accusation entierement juste : aucune sanction",
         sum(secrets(d, b) for b in ("50181", "50182", "50183")) == 0, d.get("membres"))
verifier("la taupe designee par le carnet est le Medecin en chef, retournee",
         face_retournee(d, "50181"), d.get("membres"))
verifier("accusation : rien de l'enveloppe ne part au navigateur",
         not d.get("preuves_dans_le_descripteur") and not d.get("descripteur_contient_le_secret"),
         (d.get("preuves_dans_le_descripteur"), d.get("descripteur_contient_le_secret")))

# ------------------------------- accusation : bon membre, une hypothese ratee --
# Dossiers/Argent/VOYAGES designe aussi le Medecin en chef. Le pilote propose
# Habilitation : une seule erreur, sur l'occasion, mais le membre reste bon.
# Livret p.19 : « place a secret counter on each board member for each guess
# they got wrong » — donc un secret sur chacun des trois, et rien de plus.
d = jouer("accuser", {"A.I.M. Envelope": "50185;50188;50192"})
verifier("une hypothese ratee : la chaine se deroule sans erreur",
         not d.get("erreurs"), d.get("erreurs"))
for base, nom in (("50181", "Medecin en chef"), ("50182", "Surveillance"), ("50183", "Tactique")):
    verifier(f"une hypothese ratee : un secret sur {nom}",
             secrets(d, base) == 1, d.get("membres"))

# --------------------------------- accusation : tout faux, membre compris --
# L'enveloppe est Scanner/Ideologie/Autorite, qui designe le Chef tactique. Les
# trois hypotheses du pilote sont fausses ET elles designent le Medecin en chef,
# donc le mauvais membre : trois secrets sur chacun, plus trois sur l'accuse.
d = jouer("accuser", {"A.I.M. Envelope": TAUPE_TACTIQUE})
verifier("tout faux : la chaine se deroule sans erreur", not d.get("erreurs"), d.get("erreurs"))
verifier("trois hypotheses fausses : trois secrets sur la Surveillance",
         secrets(d, "50182") == 3, d.get("membres"))
verifier("trois hypotheses fausses : trois secrets sur le Chef tactique",
         secrets(d, "50183") == 3, d.get("membres"))
verifier("mauvais membre accuse : trois secrets DE PLUS sur lui",
         secrets(d, "50181") == 6, d.get("membres"))
verifier("la taupe designee est le Chef tactique, retournee",
         face_retournee(d, "50183"), d.get("membres"))

# ------------------------- accusation : la taupe est deja passee attachement --
# En campagne les secrets se reportent, donc un membre a quatre secrets arrive
# DEJA retourne et le reste jusqu'a la fin (livret p.6). Il doit rester
# accusable : l'accuse decoule de la combinaison, pas d'un choix parmi les
# environnements encore sur la table. Avant correction, il etait impossible
# d'accuser la taupe dans ce cas, et l'accusation etait fausse d'office.
d = jouer("accuser", {"A.I.M. Envelope": TAUPE_MEDECIN,
                      "Secret Counters: Chief Medical Officer": "4"})
verifier("taupe deja retournee : la chaine se deroule sans erreur",
         not d.get("erreurs"), d.get("erreurs"))
verifier("taupe deja retournee : elle est bien accusable, donc aucune sanction",
         secrets(d, "50182") == 0 and secrets(d, "50183") == 0, d.get("membres"))
verifier("taupe deja retournee : elle garde ses quatre secrets",
         secrets(d, "50181") == 4, d.get("membres"))

# ----------------------------------------------------------- hors campagne --
# Le pack d'origine monte de vraies enveloppes. Rien ne doit changer pour lui.
d = jouer("puiser", {}, campagne=False)
verifier("hors campagne : puiser tourne sans erreur", not d.get("erreurs"), d.get("erreurs"))
tirages = d.get("tirages") or []
verifier("hors campagne : l'enveloppe S.H.I.E.L.D. rend ses six preuves",
         len(tirages) == 7 and tirages[-1]["enveloppe_non_vide"] is False, len(tirages))
verifier("hors campagne : le carnet n'est pas touche",
         d.get("carnet_preuves") is None, d.get("carnet_preuves"))

d = jouer("accuser", {}, campagne=False)
verifier("hors campagne : l'accusation se deroule sans erreur",
         not d.get("erreurs"), d.get("erreurs"))
verifier("hors campagne : la chaine s'arrete sur la derniere etape",
         d.get("manigances") == ["50169b"], d.get("manigances"))

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
