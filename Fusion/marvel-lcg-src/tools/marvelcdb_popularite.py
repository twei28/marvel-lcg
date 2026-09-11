"""Le classement de POPULARITE des decks marvelcdb, par rang.

    python3.10 tools/marvelcdb_popularite.py [--pages 50]

POURQUOI CE SCRIPT EXISTE, ET POURQUOI IL LIT DU HTML
-----------------------------------------------------
Demande de l'utilisateur (11/09/2026) : « proposer pour chaque personnage les
decks les plus populaires de marvelcdb ».

⚠ L'API PUBLIQUE NE PORTE AUCUNE POPULARITE. Verifie ce jour-la sur ses DEUX
routes, champs listes un par un :

    /api/public/decklists/by_date/<date>.json  -> date_creation, date_update,
        description_md, hero_code, hero_name, id, ignoreDeckLimitSlots, meta,
        name, slots, tags, user_id, version
    /api/public/decklist/<id>.json             -> les memes champs, exactement

`nb_votes`, `nb_favorites`, `nb_comments` sont absents des deux. Et les routes
`popular`, `hot`, `search` de l'API repondent 404, comme le note deja
`marvelcdb_index.py` depuis le 6/8/2026.

La popularite n'existe donc QUE dans les pages du site. `/decklists/popular`
et ses pages suivantes rendent le classement, douze decks par page, du plus
populaire au moins populaire.

CE QU'ON RECUPERE, ET CE QU'ON NE RECUPERE PAS
----------------------------------------------
On ne prend QUE L'ORDRE : l'identifiant du deck et son rang. Le contenu, lui,
est deja en local, aspire par `marvelcdb_index.py`. On ne retelecharge rien.

⚠ On ne recupere pas un NOMBRE de votes, seulement un RANG. La page ne montre
pas le compte, et rien ne permet de dire si le premier devance le deuxieme
d'une voix ou de cent. Un rang suffit a trier, il ne suffit pas a afficher un
score : ne pas ecrire « 245 votes » a partir de ces donnees.

COMBIEN DE PAGES
----------------
Mesure du 11/09/2026 : **15 pages, soit 180 decks, couvrent deja 62 heros sur
les 68 indexes**. Le classement melange tous les heros, donc la profondeur
necessaire depend de combien de decks on veut PAR heros : le cinquieme deck
d'un heros moyennement joue se trouve vers le rang 100. Cinquante pages (600
decks) donnent un bon top pour la plupart. Le site en compte 4488 : on n'en
veut surtout pas la totalite.

⚠ ON EST POLI. Une seconde entre deux pages, un `User-Agent` qui se nomme. Ce
script tourne a la main, pas en boucle.
"""
import argparse
import json
import os
import re
import sys
import time
import http.client

HOTE = "marvelcdb.com"
PAGES_PAR_DEFAUT = 50
ATTENTE = 1.0
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "data", "marvelcdb", "_popularite.json")

# Un bloc de deck dans la page : le lien vers la fiche, puis, un peu plus loin,
# le code du heros porte par la vignette. La distance est bornee pour ne pas
# rattacher un deck au heros du bloc SUIVANT.
BLOC = re.compile(r'/decklist/view/(\d+)[^"]*"[\s\S]{0,900}?data-code="([0-9a-z]+)"')


def lire_page(numero: int) -> str:
    route = "/decklists/popular" + ("" if numero == 1 else f"/{numero}")
    connexion = http.client.HTTPSConnection(HOTE, timeout=30)
    try:
        connexion.request("GET", route, headers={
            "User-Agent": "NarwhalChampions/1.0 (index local de decks)"})
        reponse = connexion.getresponse()
        if reponse.status != 200:
            raise RuntimeError(f"page {numero} : statut {reponse.status}")
        return reponse.read().decode("utf-8", "replace")
    finally:
        connexion.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=PAGES_PAR_DEFAUT)
    args = ap.parse_args()

    rangs = {}
    heros = {}
    rang = 0
    for numero in range(1, args.pages + 1):
        try:
            corps = lire_page(numero)
        except Exception as exc:
            print(f"  page {numero} abandonnee : {exc}")
            break
        trouves = 0
        for trouve in BLOC.finditer(corps):
            deck_id, code_heros = trouve.group(1), trouve.group(2)
            if deck_id in rangs:
                continue  # le classement bouge entre deux pages : on garde le premier rang vu
            rang += 1
            rangs[deck_id] = rang
            heros.setdefault(code_heros, []).append(deck_id)
            trouves += 1
        print(f"  page {numero:3d} : {trouves} decks (total {len(rangs)}, "
              f"{len(heros)} heros)")
        if trouves == 0:
            print("  plus rien a lire, on s'arrete la.")
            break
        time.sleep(ATTENTE)

    if not rangs:
        print("ECHEC : aucun deck lu. La page a-t-elle change de forme ?")
        sys.exit(1)

    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    with open(SORTIE, "w", encoding="utf-8") as f:
        json.dump({
            "releve_le": time.strftime("%Y-%m-%d"),
            "pages_lues": numero,
            "rangs": rangs,
        }, f, ensure_ascii=False, indent=1)

    print()
    print(f"{len(rangs)} decks classes, {len(heros)} heros representes")
    print(f"ecrit dans {SORTIE}")


if __name__ == "__main__":
    main()
