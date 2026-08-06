"""Index local des decks MarvelCDB, par heros.

L'API publique de marvelcdb n'a AUCUNE route de recherche : `by_hero`,
`popular`, `hot`, `search` repondent toutes 404 (reverifie le 6/8/2026). La
seule route de liste est `by_date/<AAAA-MM-JJ>.json`, qui rend les decks
publies ce jour-la, CONTENU COMPRIS. D'ou ce script : on aspire l'historique
une fois, on regroupe par heros, et l'ecran de preparation lit des fichiers
locaux. Un deck choisi est alors jouable sans internet.

Aucun import du moteur, bibliotheque standard uniquement.

Usage :
    python3.10 tools/marvelcdb_index.py                 # passage incremental
    python3.10 tools/marvelcdb_index.py --recalculer    # rejoue la jouabilite
    python3.10 tools/marvelcdb_index.py --depuis 2026-01-01 --jusqu-a 2026-01-07
"""
import datetime
import json
import os
import shutil
import sys
import time
import urllib.request

DEBUT_HISTORIQUE = "2019-10-01"   # premiere publication sur marvelcdb


def charger_ids_cartes(racine):
    """Tous les card_id connus du jeu, faces separees.

    cards.json est un dict {nom de pack: [carte, ...]}. Une carte recto-verso
    porte un id compose ("01001a,01001b") : les deux faces comptent, parce
    qu'un deck marvelcdb peut citer l'une ou l'autre.
    """
    ids = set()
    for nom in ("cards.json", "cards_custom.json"):
        chemin = os.path.join(racine, "data", nom)
        if not os.path.exists(chemin):
            continue
        paquets = json.load(open(chemin, encoding="utf-8"))
        for cartes in paquets.values():
            if not isinstance(cartes, list):
                continue
            for carte in cartes:
                brut = str(carte.get("card_id") or "")
                for face in brut.split(","):
                    if face:
                        ids.add(face)
    return ids


def table_deck_starter(racine):
    """« 13001a » -> « wasp », lu dans deck/starter/*.json (champ hero[0])."""
    table = {}
    dossier = os.path.join(racine, "deck", "starter")
    if not os.path.isdir(dossier):
        return table
    for fichier in sorted(os.listdir(dossier)):
        if not fichier.endswith(".json"):
            continue
        try:
            deck = json.load(open(os.path.join(dossier, fichier), encoding="utf-8"))
        except (ValueError, OSError):
            continue
        heros = (deck.get("hero") or [""])[0]
        code = str(heros).split(",")[0]
        if code:
            table[code] = fichier[:-5]
    return table


def _aspect(brut):
    """meta est une CHAINE JSON, pas un objet : '{"aspect":"justice"}'."""
    meta = brut.get("meta")
    if not meta:
        return ""
    try:
        return str(json.loads(meta).get("aspect") or "")
    except ValueError:
        return ""


def _tags(brut):
    """tags est une chaine, separee par des espaces ou des virgules."""
    brut_tags = str(brut.get("tags") or "").replace(",", " ")
    return sorted({t for t in brut_tags.split() if t})


def entree_depuis_deck(brut, ids_connus):
    """Un deck brut de by_date -> une entree d'index."""
    cartes = {str(k): int(v) for k, v in (brut.get("slots") or {}).items()}
    absentes = sorted(c for c in cartes if c not in ids_connus)
    return {
        "id": brut.get("id"),
        "nom": brut.get("name") or "",
        "aspect": _aspect(brut),
        "tags": _tags(brut),
        "date": str(brut.get("date_creation") or "")[:10],
        "auteur": brut.get("user_id"),
        "cartes": cartes,
        "jouable": not absentes,
        "cartes_absentes": absentes,
    }


def regrouper(bruts, ids_connus, table):
    """Regroupe par hero_code. Rend (paquets, nombre de decks ecartes).

    Un deck dont le heros n'existe pas dans le jeu est ecarte : le proposer
    ne menerait qu'a un message d'erreur au lancement.
    """
    paquets = {}
    ecartes = 0
    for brut in bruts:
        code = str(brut.get("hero_code") or "").split(",")[0]
        if not code or code not in table:
            ecartes += 1
            continue
        paquet = paquets.setdefault(code, {
            "hero_code": code,
            "hero_name": brut.get("hero_name") or "",
            "deck_starter": table[code],
            "decks": [],
        })
        paquet["decks"].append(entree_depuis_deck(brut, ids_connus))
    return paquets, ecartes


URL_JOUR = "https://marvelcdb.com/api/public/decklists/by_date/{}.json"
AGENT = "marvel-lcg-local/1.0 (index de decks hors ligne, usage personnel)"
DELAI = 0.2          # seconde entre deux requetes : on ne martele pas le site


def _date(txt):
    return datetime.date(int(txt[0:4]), int(txt[5:7]), int(txt[8:10]))


def _lendemain(txt):
    return (_date(txt) + datetime.timedelta(days=1)).isoformat()


def _veille(txt):
    return (_date(txt) - datetime.timedelta(days=1)).isoformat()


def jours_a_traiter(derniere_date, aujourdhui, jusqu_a=None):
    """Jours restant a aspirer, bornes incluses.

    Le jour courant est volontairement exclu : sa journee n'est pas finie, et
    l'aspirer figerait un total partiel qu'aucun passage suivant ne reprendrait.
    """
    debut = DEBUT_HISTORIQUE if not derniere_date else _lendemain(derniere_date)
    fin = _veille(aujourdhui)
    if jusqu_a and jusqu_a < fin:
        fin = jusqu_a
    jours, jour = [], debut
    while jour <= fin:
        jours.append(jour)
        jour = _lendemain(jour)
    return jours


def recuperer_jour(date):
    """Une journee de by_date. Leve en cas d'echec, l'appelant decide."""
    requete = urllib.request.Request(URL_JOUR.format(date), headers={"User-Agent": AGENT})
    with urllib.request.urlopen(requete, timeout=30) as reponse:
        return json.loads(reponse.read().decode("utf-8"))


def aspirer(dates, recuperer, ids_connus, table):
    """Aspire chaque jour et regroupe. `recuperer` est injecte (testable).

    Un jour en erreur est reessaye UNE fois, puis journalise et saute : une
    coupure reseau au 900e jour ne doit pas perdre les 899 precedents.
    """
    paquets, en_erreur, ecartes = {}, [], 0
    for i, date in enumerate(dates):
        bruts = None
        for essai in (1, 2):
            try:
                bruts = recuperer(date)
                break
            except Exception as exc:           # reseau, JSON, 404 : meme traitement
                if essai == 2:
                    en_erreur.append(date)
                    print(f"  ! {date} saute apres 2 essais : {exc}")
        if bruts is None:
            continue
        du_jour, ecartes_jour = regrouper(bruts, ids_connus, table)
        ecartes += ecartes_jour
        for code, paquet in du_jour.items():
            cible = paquets.setdefault(code, {**paquet, "decks": []})
            cible["decks"].extend(paquet["decks"])
        if i % 100 == 0:
            print(f"  {date} ({i + 1}/{len(dates)})")
    return paquets, en_erreur, ecartes


def fusionner(anciennes, nouvelles):
    """Dedoublonne par id, la version la plus recente gagne, tri date decroissante."""
    par_id = {d["id"]: d for d in anciennes}
    par_id.update({d["id"]: d for d in nouvelles})
    return sorted(par_id.values(), key=lambda d: (d.get("date", ""), d["id"]), reverse=True)


def ecrire_index(racine, paquets):
    """Un fichier par heros, FUSIONNE avec l'existant. Rend le nombre ecrit."""
    dossier = os.path.join(racine, "data", "marvelcdb")
    os.makedirs(dossier, exist_ok=True)
    for code, paquet in paquets.items():
        chemin = os.path.join(dossier, code + ".json")
        anciennes = []
        if os.path.exists(chemin):
            try:
                anciennes = json.load(open(chemin, encoding="utf-8")).get("decks", [])
            except ValueError:
                anciennes = []          # fichier tronque par une interruption : on repart
        json.dump({
            "hero_code": code,
            "hero_name": paquet["hero_name"],
            "deck_starter": paquet["deck_starter"],
            "genere_le": datetime.date.today().isoformat(),
            "decks": fusionner(anciennes, paquet["decks"]),
        }, open(chemin, "w", encoding="utf-8"), ensure_ascii=False)
    return len(paquets)


def publier_vers_game(racine):
    """Rend data/marvelcdb visible depuis .game/, d'ou le moteur lit.

    Le moteur tourne avec .game pour repertoire courant : `/read_file?data/x`
    resout .game/data/x. Selon le lanceur utilise, .game/data est un lien
    symbolique vers data/ (launcher_fast.py, et l'installation miroir) ou une
    COPIE figee (installation WSL, heritee de launcher.py). Dans le second cas
    l'index n'apparaitrait jamais : on y pose un lien vers le vrai dossier, ou
    une copie si les liens sont impossibles.
    """
    data_game = os.path.join(racine, ".game", "data")
    if not os.path.isdir(data_game):
        return "rien a faire"                 # pas de .game : rien a publier
    if os.path.islink(data_game):
        return "rien a faire"                 # deja un lien vers data/
    source = os.path.join(racine, "data", "marvelcdb")
    cible = os.path.join(data_game, "marvelcdb")
    if os.path.islink(cible):
        return "lien"
    if os.path.isdir(cible):
        shutil.rmtree(cible)
    try:
        os.symlink(source, cible, target_is_directory=True)
        return "lien"
    except OSError:
        shutil.copytree(source, cible)
        return "copie"


def _meta(racine):
    chemin = os.path.join(racine, "data", "marvelcdb", "_meta.json")
    if os.path.exists(chemin):
        try:
            return json.load(open(chemin, encoding="utf-8"))
        except ValueError:
            pass
    return {}


def compter_index(racine):
    """Total REEL de decks dans l'index, relu sur les fichiers ecrits.

    Ne jamais additionner le total du passage precedent : les passages se
    recouvrent (une plage rejouee, un jour en erreur rattrape) et le compteur
    derivait a chaque fois.
    """
    dossier = os.path.join(racine, "data", "marvelcdb")
    if not os.path.isdir(dossier):
        return 0
    total = 0
    for fichier in sorted(os.listdir(dossier)):
        if not fichier.endswith(".json") or fichier.startswith("_"):
            continue
        try:
            paquet = json.load(open(os.path.join(dossier, fichier), encoding="utf-8"))
            total += len(paquet.get("decks", []))
        except (ValueError, OSError):
            continue
    return total


def _recalculer(racine, ids_connus):
    """Rejoue la jouabilite sur l'index existant, sans reseau.

    A lancer apres l'ajout d'un pack : des decks jusque-la incomplets
    redeviennent jouables sans qu'il faille reaspirer quoi que ce soit.
    """
    dossier = os.path.join(racine, "data", "marvelcdb")
    if not os.path.isdir(dossier):
        print("Aucun index a recalculer : lance d'abord un passage d'aspiration.")
        return 0
    change = 0
    for fichier in sorted(os.listdir(dossier)):
        if not fichier.endswith(".json") or fichier.startswith("_"):
            continue
        chemin = os.path.join(dossier, fichier)
        paquet = json.load(open(chemin, encoding="utf-8"))
        for deck in paquet.get("decks", []):
            absentes = sorted(c for c in deck.get("cartes", {}) if c not in ids_connus)
            if absentes != deck.get("cartes_absentes"):
                change += 1
            deck["cartes_absentes"] = absentes
            deck["jouable"] = not absentes
        json.dump(paquet, open(chemin, "w", encoding="utf-8"), ensure_ascii=False)
    return change


if __name__ == "__main__":
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    args = sys.argv[1:]

    def option(nom):
        return args[args.index(nom) + 1] if nom in args else None

    ids_connus = charger_ids_cartes(racine)
    print(f"{len(ids_connus)} cartes connues du jeu.")

    if "--recalculer" in args:
        change = _recalculer(racine, ids_connus)
        print(f"Jouabilite recalculee, {change} deck(s) ont change d'etat.")
        print("Publication :", publier_vers_game(racine))
        raise SystemExit(0)

    meta = _meta(racine)
    depuis = meta.get("derniere_date")
    if option("--depuis"):
        depuis = _veille(option("--depuis"))       # --depuis est INCLUSIF
    dates = jours_a_traiter(depuis, datetime.date.today().isoformat(), option("--jusqu-a"))
    a_reessayer = [j for j in meta.get("jours_en_erreur", []) if j not in dates]
    dates = sorted(set(dates) | set(a_reessayer))
    if not dates:
        print("Deja a jour, rien a aspirer.")
        raise SystemExit(0)

    print(f"{len(dates)} jour(s) a aspirer, du {dates[0]} au {dates[-1]}.")

    def recuperer_ralenti(date):
        time.sleep(DELAI)
        return recuperer_jour(date)

    table = table_deck_starter(racine)
    paquets, en_erreur, ecartes = aspirer(dates, recuperer_ralenti, ids_connus, table)
    total = sum(len(p["decks"]) for p in paquets.values())
    ecrire_index(racine, paquets)

    json.dump({
        "derniere_date": max(dates[-1], _meta(racine).get("derniere_date", "")),
        "genere_le": datetime.date.today().isoformat(),
        "total_decks": compter_index(racine),
        "jours_en_erreur": en_erreur,
    }, open(os.path.join(racine, "data", "marvelcdb", "_meta.json"), "w",
            encoding="utf-8"), ensure_ascii=False)

    print(f"{total} deck(s) indexes sur {len(paquets)} heros, "
          f"{ecartes} ecarte(s) (heros absent du jeu), "
          f"{len(en_erreur)} jour(s) en erreur.")
    print("Publication :", publier_vers_game(racine))
