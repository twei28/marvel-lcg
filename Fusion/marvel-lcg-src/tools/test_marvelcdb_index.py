"""Teste le noyau de l'indexeur MarvelCDB, SANS RESEAU.

Toutes les fonctions visees sont pures : on leur passe des journees figees,
ecrites ici, et un catalogue de cartes reduit. Aucun appel a marvelcdb.com.

Usage: python3.10 tools/test_marvelcdb_index.py
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import marvelcdb_index as idx

resultats = []


def verifier(nom, obtenu, attendu):
    ok = obtenu == attendu
    resultats.append((nom, ok, f"obtenu {obtenu!r}, attendu {attendu!r}"))


# --- Journees figees, au format exact de by_date (verifie le 6/8/2026) -------
DECK_NOVA = {
    "id": 64331, "name": "Nova Justice", "hero_code": "28001a", "hero_name": "Nova",
    "date_creation": "2026-08-01T00:33:02+00:00", "user_id": 77086,
    "meta": '{"aspect":"justice"}', "tags": "solo", "version": "1.0",
    "slots": {"01062": 2, "28002": 1, "99999": 1},
}
DECK_WASP = {
    "id": 64332, "name": "Hives", "hero_code": "13001a", "hero_name": "Wasp",
    "date_creation": "2026-08-01T09:00:00+00:00", "user_id": 42,
    "meta": '{"aspect":"protection","aspect2":"basic"}', "tags": "multiplayer solo",
    "slots": {"01062": 2, "13002": 1},
}
IDS_CONNUS = {"01062", "28002", "13002"}
TABLE = {"28001a": "nova", "13001a": "wasp"}

# --- Aspect, tags -----------------------------------------------------------
e = idx.entree_depuis_deck(DECK_NOVA, IDS_CONNUS)
verifier("aspect lu dans meta", e["aspect"], "justice")
verifier("tags decoupes", idx.entree_depuis_deck(DECK_WASP, IDS_CONNUS)["tags"],
         ["multiplayer", "solo"])
verifier("meta vide ne casse rien",
         idx.entree_depuis_deck({**DECK_NOVA, "meta": ""}, IDS_CONNUS)["aspect"], "")
verifier("tags vides donnent une liste vide",
         idx.entree_depuis_deck({**DECK_NOVA, "tags": ""}, IDS_CONNUS)["tags"], [])

# --- Jouabilite -------------------------------------------------------------
verifier("carte inconnue -> non jouable", e["jouable"], False)
verifier("carte inconnue listee", e["cartes_absentes"], ["99999"])
verifier("toutes cartes connues -> jouable",
         idx.entree_depuis_deck(DECK_WASP, IDS_CONNUS)["jouable"], True)

# --- Champs conserves -------------------------------------------------------
verifier("date reduite au jour", e["date"], "2026-08-01")
verifier("cartes conservees", e["cartes"], {"01062": 2, "28002": 1, "99999": 1})
verifier("id conserve", e["id"], 64331)

# --- Regroupement -----------------------------------------------------------
paquets, ecartes = idx.regrouper([DECK_NOVA, DECK_WASP], IDS_CONNUS, TABLE)
verifier("un paquet par heros", sorted(paquets), ["13001a", "28001a"])
verifier("nom du heros conserve", paquets["28001a"]["hero_name"], "Nova")
verifier("deck starter resolu", paquets["28001a"]["deck_starter"], "nova")
verifier("aucun ecarte", ecartes, 0)

inconnu = {**DECK_NOVA, "id": 1, "hero_code": "77777a"}
paquets2, ecartes2 = idx.regrouper([inconnu], IDS_CONNUS, TABLE)
verifier("heros inconnu du jeu : ecarte", (sorted(paquets2), ecartes2), ([], 1))

# --- Catalogue et table, lus sur de vrais fichiers ---------------------------
with tempfile.TemporaryDirectory() as tmp:
    os.makedirs(os.path.join(tmp, "data"))
    os.makedirs(os.path.join(tmp, "deck", "starter"))
    json.dump({"pack": [{"card_id": "01001a,01001b"}, {"card_id": "01062"}]},
              open(os.path.join(tmp, "data", "cards.json"), "w", encoding="utf-8"))
    json.dump({"hero": ["13001a,13001b,13001c"]},
              open(os.path.join(tmp, "deck", "starter", "wasp.json"), "w", encoding="utf-8"))
    verifier("ids de cartes, faces separees",
             idx.charger_ids_cartes(tmp), {"01001a", "01001b", "01062"})
    verifier("table deck starter", idx.table_deck_starter(tmp), {"13001a": "wasp"})

# --- Calendrier -------------------------------------------------------------
verifier("premier passage : depuis le debut de l'historique",
         idx.jours_a_traiter(None, "2019-10-04", None),
         ["2019-10-01", "2019-10-02", "2019-10-03"])
verifier("passage incremental : reprend au lendemain",
         idx.jours_a_traiter("2026-08-01", "2026-08-04", None),
         ["2026-08-02", "2026-08-03"])
verifier("le jour courant n'est jamais aspire (journee incomplete)",
         idx.jours_a_traiter("2026-08-02", "2026-08-03", None), [])
verifier("deja a jour", idx.jours_a_traiter("2026-08-05", "2026-08-03", None), [])
verifier("--jusqu-a borne la plage",
         idx.jours_a_traiter("2026-08-01", "2026-08-10", "2026-08-03"),
         ["2026-08-02", "2026-08-03"])

# --- Fusion -----------------------------------------------------------------
a = {"id": 1, "date": "2026-01-01"}
b = {"id": 2, "date": "2026-02-01"}
b2 = {"id": 2, "date": "2026-02-01", "nom": "renomme"}
verifier("tri par date decroissante", [d["id"] for d in idx.fusionner([a], [b])], [2, 1])
verifier("dedoublonnage par id, la nouvelle version gagne",
         idx.fusionner([b], [b2]), [b2])

# --- Aspiration, avec une fonction de recuperation INJECTEE -----------------
appels = []


def faux_recuperer(date):
    appels.append(date)
    if date == "2026-08-02":
        raise OSError("marvelcdb injoignable")
    return [DECK_NOVA] if date == "2026-08-01" else [DECK_WASP]


paquets3, en_erreur, ecartes3, _vides = idx.aspirer(
    ["2026-08-01", "2026-08-02", "2026-08-03"], faux_recuperer, IDS_CONNUS, TABLE)
verifier("un jour en erreur n'interrompt rien", sorted(paquets3), ["13001a", "28001a"])
verifier("le jour en erreur est journalise", en_erreur, ["2026-08-02"])
verifier("le jour en erreur est reessaye une fois", appels.count("2026-08-02"), 2)

# --- Ecriture ---------------------------------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    os.makedirs(os.path.join(tmp, "data"))
    n = idx.ecrire_index(tmp, paquets3)
    verifier("un fichier par heros", n, 2)
    ecrit = json.load(open(os.path.join(tmp, "data", "marvelcdb", "28001a.json"),
                           encoding="utf-8"))
    verifier("format du fichier heros",
             (ecrit["hero_code"], ecrit["deck_starter"], len(ecrit["decks"])),
             ("28001a", "nova", 1))

    # Second passage : le fichier existant est FUSIONNE, pas ecrase.
    autre = {"28001a": {"hero_code": "28001a", "hero_name": "Nova", "deck_starter": "nova",
                        "decks": [idx.entree_depuis_deck({**DECK_NOVA, "id": 99}, IDS_CONNUS)]}}
    idx.ecrire_index(tmp, autre)
    relu = json.load(open(os.path.join(tmp, "data", "marvelcdb", "28001a.json"),
                          encoding="utf-8"))
    verifier("second passage : fusion, pas ecrasement",
             sorted(d["id"] for d in relu["decks"]), [99, 64331])

    # Le total se COMPTE sur les fichiers : l'additionner derivait des qu'une
    # plage de jours etait rejouee.
    verifier("total compte sur les fichiers", idx.compter_index(tmp), 3)
    json.dump({"total_decks": 999},
              open(os.path.join(tmp, "data", "marvelcdb", "_meta.json"), "w",
                   encoding="utf-8"))
    verifier("_meta.json n'est pas compte comme un heros",
             idx.compter_index(tmp), 3)

# --- Jour creux : marvelcdb repond 500, pas une liste vide ------------------
# Mesure le 6/8/2026 : by_date/2019-10-01 rend HTTP 500 (aucun deck publie ce
# jour-la) tandis que le 2019-10-02 rend 200 avec un deck. Traiter ce 500
# comme une panne remplirait jours_en_erreur de centaines de jours creux, tous
# reessayes a chaque passage, pour toujours.
import urllib.error
faux_500 = urllib.error.HTTPError("u", 500, "Internal Server Error", {}, None)
faux_503 = urllib.error.HTTPError("u", 503, "Service Unavailable", {}, None)
verifier("500 = jour sans deck", idx.est_jour_creux(faux_500), True)
verifier("503 = vraie panne", idx.est_jour_creux(faux_503), False)
verifier("erreur reseau = vraie panne", idx.est_jour_creux(OSError("timeout")), False)

# Un jour creux compte comme creux, pas comme erreur, et n'interrompt rien.
def recuperer_avec_creux(date):
    if date == "2026-08-02":
        return []
    return [DECK_NOVA] if date == "2026-08-01" else [DECK_WASP]


p4, err4, ec4, vides4 = idx.aspirer(
    ["2026-08-01", "2026-08-02", "2026-08-03"], recuperer_avec_creux, IDS_CONNUS, TABLE)
verifier("jour creux compte a part", (vides4, err4), (1, []))
verifier("les autres jours sont bien indexes", sorted(p4), ["13001a", "28001a"])

# --- Tranches : l'ecriture doit etre PERIODIQUE, pas finale -----------------
# Une aspiration de 2500 jours ecrite en un seul bloc final perd tout si on
# l'interrompt, alors que la spec promet une reprise au jour suivant le
# dernier ecrit. On decoupe donc en tranches.
verifier("decoupage exact", idx.tranches(["a", "b", "c", "d"], 2), [["a", "b"], ["c", "d"]])
verifier("derniere tranche incomplete",
         idx.tranches(["a", "b", "c"], 2), [["a", "b"], ["c"]])
verifier("liste plus courte qu'une tranche", idx.tranches(["a"], 100), [["a"]])
verifier("liste vide", idx.tranches([], 100), [])

with tempfile.TemporaryDirectory() as tmp:
    os.makedirs(os.path.join(tmp, "data", "marvelcdb"))
    idx.ecrire_meta(tmp, "2020-01-08", ["2019-12-25"])
    meta = json.load(open(os.path.join(tmp, "data", "marvelcdb", "_meta.json"),
                          encoding="utf-8"))
    verifier("meta ecrite apres chaque tranche : la reprise est possible",
             (meta["derniere_date"], meta["jours_en_erreur"], meta["total_decks"]),
             ("2020-01-08", ["2019-12-25"], 0))

# --- Publication vers .game -------------------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    os.makedirs(os.path.join(tmp, "data", "marvelcdb"))
    os.makedirs(os.path.join(tmp, ".game", "data"))      # copie reelle, cas WSL
    verifier("copie reelle : marvelcdb devient visible",
             idx.publier_vers_game(tmp), "lien")
    verifier("visible depuis .game",
             os.path.isdir(os.path.join(tmp, ".game", "data", "marvelcdb")), True)

with tempfile.TemporaryDirectory() as tmp:
    os.makedirs(os.path.join(tmp, "data", "marvelcdb"))
    os.makedirs(os.path.join(tmp, ".game"))
    os.symlink(os.path.join(tmp, "data"), os.path.join(tmp, ".game", "data"))
    verifier("lien symbolique deja en place : rien a faire",
             idx.publier_vers_game(tmp), "rien a faire")

for nom, ok, detail in resultats:
    print(("OK    " if ok else "ECHEC ") + nom + ("" if ok else f"   [{detail}]"))
rates = [n for n, ok, _ in resultats if not ok]
print("\nTOUT PASSE" if not rates else f"\n{len(rates)} ECHEC(S)")
sys.exit(0 if not rates else 1)
