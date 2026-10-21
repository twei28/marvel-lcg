"""Les cas de la batterie « Marvelous » : chaque carte signature empruntable,
jouee par son vrai heros (TEMOIN) puis par Stan Lee (MESURE).

Pur : lit `data/cards.json` + `data/cards_custom.json` + `deck/starter/*.json`,
rend une liste de cas au format de `tools/test_capacites.py`. Aucun moteur.
Deterministe : deux appels rendent la meme liste dans le meme ordre, ce qui
permet au lanceur de regenerer les cas dans chaque processus fils.

    python3 tools/generateurs-marvelous/generer_cas.py            # statistiques
    python3 tools/generateurs-marvelous/generer_cas.py iron_man   # les cas d'un deck

Ce que mesure un cas (verificateur `marvelous_jouee`, voir VERIFICATEURS) :
  1. la carte est en main et le moteur la dit JOUABLE (`Puzzle.AssertJouable`,
     methode ajoutee par le lanceur, qui lit `CardFace.CanPlayBy`) ;
  2. elle se joue par le vrai chemin (`jouer`, donc en payant) sans traceback ;
  3. apres coup : un allie/amelioration/soutien/manigance de joueur est EN
     JEU ; un evenement a quitte la main et le deck (resolu, attache ou retire).
  4. une empreinte de l'etat (cartes du joueur en jeu, taille de main et de
     defausse, PV de l'identite) est ecrite dans le message, pour comparer
     temoin et Stan Lee A POSTERIORI (`analyser.py`), jamais pour rougir.

Ce qu'il NE mesure PAS : que l'EFFET de la carte est le bon (un evenement qui
se resout sans rien faire est vert) ; les cartes dont la mise en place exige
une cible absente (« attach to an ally ») rougissent pour le temoin aussi et
sont classees NON CONCLUANTES par l'analyse, pas « ecart ».
"""
import glob
import json
import os
import re
import sys

RACINE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
if not os.path.exists(os.path.join(RACINE, "data", "cards.json")):
    # Copie gelee hors du depot (batterie complete) : le repertoire courant est
    # la racine du moteur, ou un dossier de jeu (`.game-src-*`, qui porte les
    # liens `data` et `deck`).
    RACINE = os.getcwd()
SCENARIO = "rhino"
STAN_DECK = "stan_lee"
STAN_ALTER = "90101b"          # la partie commence en alter-ego : ChangeForm('90101b') -> heros
TYPES_JOUABLES = ("Ally", "Upgrade", "Support", "Event",
                  "PlayerSideScheme", "Player Side Scheme", "Player_Side_Scheme")
PERMANENTS = ("Ally", "Upgrade", "Support",
              "PlayerSideScheme", "Player Side Scheme", "Player_Side_Scheme")
# Ressources de base a DOUBLE icone : Energy (YY), Genius (BB), Strength (RR).
# On en donne assez de chaque pour couvrir n'importe quelle exigence de type.
CARBURANT = ("01088", "01089", "01090")


def _lire(chemin):
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def charger_cartes():
    """card_id -> entree (avec `_pack`), cards.json ET cards_custom.json."""
    cartes = {}
    for nom in ("cards.json", "cards_custom.json"):
        chemin = os.path.join(RACINE, "data", nom)
        if not os.path.exists(chemin):
            continue
        for pack, liste in _lire(chemin).items():
            for c in liste:
                if isinstance(c, dict) and c.get("card_id"):
                    c = dict(c)
                    c["_pack"] = pack
                    cartes[c["card_id"]] = c
    return cartes


def charger_decks(cartes):
    """nom de deck -> {face_hero, face_alter, set, hero_deck, indisponible}."""
    decks = {}
    for chemin in sorted(glob.glob(os.path.join(RACINE, "deck", "starter", "*.json"))):
        d = _lire(chemin)
        hero = d.get("hero") or []
        if not hero:
            continue
        faces = str(hero[0]).split(",")
        face_hero = faces[0]
        face_alter = faces[1] if len(faces) > 1 else None
        c = cartes.get(face_hero) or {}
        decks[os.path.basename(chemin)[:-5]] = {
            "face_hero": face_hero,
            "face_alter": face_alter,
            "set": c.get("set_name"),
            "hero_deck": [str(x).split(",")[0] for x in (d.get("hero_deck") or [])],
            "indisponible": bool((d.get("metadata") or {}).get("indisponible")),
        }
    return decks


def forme_requise(carte) -> str:
    """'hero' par defaut ; 'alter' si le texte ne parle QUE d'alter-ego."""
    texte = re.sub(r"<[^>]+>", "", str(carte.get("text") or "")).lower()
    alter = re.search(r"alter-ego (action|interrupt|response)|alter-ego form", texte)
    hero = re.search(r"\bhero (action|interrupt|response)\b|hero form", texte)
    return "alter" if (alter and not hero) else "hero"


def cout(carte) -> int:
    brut = str((carte.get("desc") or {}).get("Cost", "")).strip()
    if brut.upper().startswith("X"):
        return 2
    chiffres = re.match(r"\d+", brut)
    return int(chiffres.group(0)) if chiffres else 0


# Une ressource de base par couleur : Energy (YY), Genius (BB), Strength (RR).
RESSOURCE_DE_COULEUR = {"Y": "01088", "B": "01089", "R": "01090"}


def carburant(n: int, exigence: str = ""):
    """Les cartes de ressource a donner en main pour payer `n`.

    ⚠ UNE EXIGENCE (`Requirement`, ex. « YYY » de ze006 Wrath of Olympus) EXIGE DES
    COULEURS PRECISES, et le paiement automatique du harnais prend les PREMIERES cartes
    de la main, sans lire l'exigence (`player_action.py`, « Will ignore "Requirement" »).
    Avec les trois couleurs en main, l'ordre decide du paiement : le temoin payait en
    Energy (exigence satisfaite), Stan Lee, dont le deck de 40 cartes contient deja des
    Energy/Genius/Strength remontees dans un autre ordre, payait YY BB RR et la carte
    restait en main (cas ze006 du 21/10/2026 : un artefact du cas, pas du moteur). Pour
    une carte a exigence, on ne donne donc QUE les couleurs exigees.
    """
    par_type = n // 2 + 1
    couleurs = [RESSOURCE_DE_COULEUR[c] for c in dict.fromkeys(exigence) if c in RESSOURCE_DE_COULEUR]
    types = couleurs or CARBURANT
    return [r for r in types for _ in range(par_type)]


def deck_pour(carte, decks):
    """Le deck de depart qui porte cette carte signature, ou None."""
    candidats = [(nom, d) for nom, d in decks.items()
                 if d["set"] == carte.get("set_name") and not d["indisponible"]]
    if not candidats:
        return None
    for nom, d in candidats:
        if carte["card_id"] in d["hero_deck"]:
            return nom
    return candidats[0][0]


def cartes_empruntables(cartes, decks):
    vus = set()
    for cid in sorted(cartes):
        c = cartes[cid]
        if (c.get("desc") or {}).get("Class") != "Hero":
            continue
        if c.get("type") not in TYPES_JOUABLES:
            continue
        if not c.get("set_name") or c["set_name"] == "Stan Lee":
            continue
        if deck_pour(c, decks) is None:
            continue
        if cid in vus:
            continue
        vus.add(cid)
        yield c


def _cas(carte, deck_nom, decks, stan: bool):
    cid = carte["card_id"]
    d = decks[deck_nom]
    forme = forme_requise(carte)
    if stan:
        heros, alter = STAN_DECK, STAN_ALTER
    else:
        heros, alter = deck_nom, d["face_alter"]
    mise = []
    if forme == "hero" and alter:
        mise.append(f"Puzzle.ChangeForm('{alter}')")
    # ⚠ UNE CARTE « (THWART) » N'A DE CIBLE QUE SUR UN COMPLOT QUI PORTE DE LA MENACE
    # (`can_be_thwart_schemes`, `ability.py`). Au premier tour d'une partie d'essai le complot
    # principal est a 0 : le temoin ne passait que si la mise en place de son alter-ego posait
    # un complot (Cable, « Soldier X »), et Stan Lee, qui n'a pas cette mise en place, voyait
    # Mind Scan « injouable » (cas 40003 du 21/10/2026 : un artefact du cas, pas du moteur).
    # En vraie partie le complot a de la menace des la fin du premier tour.
    # ⚠ APRES LE REMPLACEMENT DE LA MAIN (`declencher`, pas `mise_en_place`) : la main de depart
    # de Stan Lee peut contenir une interruption (Great Responsibility) que le harnais joue seule
    # et qui REMPLACE la menace posee ; la main exclusive n'a que la carte et ses ressources.
    avant = []
    if "(thwart)" in str(carte.get("text") or "").lower():
        avant.append("Puzzle.PlaceThreat('01097b', 5)")
    cas = {
        "nom": f"[marvelous] {cid} {carte.get('name')} — {'Stan Lee' if stan else 'temoin ' + deck_nom}",
        "pourquoi": ("Stan Lee (Marvelous) doit pouvoir jouer cette carte signature "
                     "exactement comme " + deck_nom) if stan else
                    "temoin : la carte jouee par son vrai heros, pour separer un ecart Marvelous d'un cas non montable",
        "scenario": SCENARIO,
        "heros": heros,
        "mise_en_place": mise,
        "main_exclusive": [cid] + carburant(cout(carte), str((carte.get("desc") or {}).get("Requirement", ""))),
        "declencher": avant + [f"Puzzle.AssertJouable('{cid}')"],
        "jouer": [cid],
        "verifier": "marvelous_jouee",
        "attendu": {"carte": cid, "type": carte.get("type"), "set": carte.get("set_name"),
                    "deck": deck_nom, "stan": stan},
    }
    if stan:
        # Le deck signature ENTIER du heros emprunte, comme un deck Stan Lee
        # construit sur un seul heros : les cartes qui dependent d'une
        # camarade (pile Tech, compagnons) ont les memes chances que le temoin.
        cas["hero_deck_stan"] = list(d["hero_deck"])
    return cas


def generer(decks_voulus=None, cartes=None, decks=None):
    """Tous les cas, temoin puis Stan Lee, carte par carte, tries par card_id.
    `decks_voulus` : noms de decks de depart (ou de sets), pour un pilote."""
    cartes = cartes or charger_cartes()
    decks = decks or charger_decks(cartes)
    voulus = set(decks_voulus or [])
    cas = []
    for carte in cartes_empruntables(cartes, decks):
        deck_nom = deck_pour(carte, decks)
        if voulus and deck_nom not in voulus and carte.get("set_name") not in voulus:
            continue
        cas.append(_cas(carte, deck_nom, decks, stan=False))
        cas.append(_cas(carte, deck_nom, decks, stan=True))
    return cas


# Ajoute a `test_capacites.VERIFICATIONS` par le lanceur : meme espace, memes
# aides (`par_id`, `identite`, `cas`).
VERIFICATEURS = r'''

def marvelous_jouee(monde, aides):
    import json
    cas = aides["cas"]
    att = cas.get("attendu") or {}
    cid, typ = att["carte"], att.get("type")
    joueur = monde.players[0]

    def dans(collection):
        try:
            faces = collection.GetAll()
        except Exception:
            return False
        return any(getattr(f.paper, "card_id", None) == cid for f in faces)

    en_main = dans(joueur.hand_cards)
    en_jeu = aides["par_id"](monde, cid) is not None
    en_defausse = dans(joueur.discard_pile)
    en_deck = dans(joueur.player_deck)

    # Empreinte : ecrite dans le message pour la comparaison temoin/Stan Lee
    # faite par analyser.py. Ne fait jamais rougir.
    empreinte = {}
    try:
        identite = aides["identite"](monde)
        en_jeu_joueur = 0
        for objet in monde.object_manager.card_dict.values():
            face = objet.face
            if face is None or not face.IsInPlay():
                continue
            proprietaire = getattr(face, "controller", None) or getattr(face.card, "controller", None)
            if proprietaire is joueur or proprietaire is None and getattr(face.paper, "card_id", None) == cid:
                en_jeu_joueur += 1
        empreinte = {
            "jeu": en_jeu_joueur,
            "main": len(list(joueur.hand_cards.GetAll())),
            "defausse": len(list(joueur.discard_pile.GetAll())),
            "pv": getattr(identite, "health", None),
        }
    except Exception as exc:
        empreinte = {"erreur": f"{type(exc).__name__}: {exc}"}

    zones = f"main={en_main} jeu={en_jeu} defausse={en_defausse} deck={en_deck}"
    if typ in ("Ally", "Upgrade", "Support", "PlayerSideScheme", "Player Side Scheme", "Player_Side_Scheme"):
        ok = en_jeu
        raison = "" if ok else f"{cid} ({typ}) n'est pas en jeu apres avoir ete jouee"
    else:
        # Un evenement joue quitte la main (defausse, attache, retire...). Ne pas
        # regarder le deck : le deck signature en porte d'autres exemplaires.
        # Une carte injouable serait defaussee sans jouer, mais AssertJouable
        # l'a ecartee AVANT ; une resolution qui echoue leve une exception.
        ok = not en_main
        raison = "" if ok else f"{cid} ({typ}) est encore en main : pas jouee"
    return ok, (raison + " | " if raison else "") + zones + " | empreinte=" + json.dumps(empreinte)
'''


if __name__ == "__main__":
    voulus = sys.argv[1:] or None
    cartes = charger_cartes()
    decks = charger_decks(cartes)
    cas = generer(voulus, cartes, decks)
    if voulus:
        for c in cas:
            print(json.dumps(c, ensure_ascii=False))
    par_set = {}
    for c in cas[::2]:
        par_set[c["attendu"]["set"]] = par_set.get(c["attendu"]["set"], 0) + 1
    print(f"{len(cas)} cas ({len(cas) // 2} cartes signature, {len(par_set)} sets), "
          f"{sum(1 for d in decks.values() if d['indisponible'])} deck(s) masque(s)", file=sys.stderr)
    for s, n in sorted(par_set.items(), key=lambda x: -x[1])[:8]:
        print(f"  {n:3d}  {s}", file=sys.stderr)
