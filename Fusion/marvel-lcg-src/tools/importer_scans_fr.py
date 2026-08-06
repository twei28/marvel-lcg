"""Importe le pack d'images OCTGN FR dans assets/pics-fr.

Le pack est fait de 61 archives .o8c (des ZIP) dont les images portent un GUID
OCTGN pour nom. Le jeu, lui, demande ses images par code de carte. Ce script
fait la traduction, une fois, hors partie.

Trois pieges, tous mesures sur le pack reel :

  1. La correspondance GUID vers code N'EST PAS BIUNIVOQUE. Une carte de
     rencontre reimprimee d'une boite a l'autre garde un seul GUID mais recoit
     un code marvelcdb par boite : l'obligation 01088 en compte 47. A l'inverse
     une carte a deux faces partage son GUID entre 01001a et 01001b, que seul
     le suffixe du nom de fichier separe.
  2. Le filtre sur cards.json est ce qui empeche les reimpressions d'inonder le
     dossier : un code que le jeu ne connait pas n'est pas ecrit.
  3. Le module OCTGN n'est qu'un AUDITEUR. Il ne couvre que 33 sets sur 61 et
     ne rattrape qu'un GUID sur les 80 inconnus de marvelcdb. Il sert a
     signaler les desaccords, dont l'inversion 24031/24032.

Usage :
    python3 tools/importer_scans_fr.py --rapport-seul   # n'ecrit aucune image
    python3 tools/importer_scans_fr.py                  # extraction complete
    python3 tools/importer_scans_fr.py --sans-audit     # sans le module OCTGN
"""

import argparse
import collections
import io
import json
import os
import re
import sys
import tarfile
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

MARVEL = Path(__file__).resolve().parents[1]
RACINE = MARVEL.parents[1]

PACK = MARVEL / "assets" / "pics-fr" / "OCTGN_Image_pack_FR"
SORTIE_IMAGES = MARVEL / "assets" / "pics-fr"
CARTES_JEU = MARVEL / "data" / "cards.json"
SORTIE_TS = RACINE / "ui-app" / "src" / "board"
RAPPORT = RACINE / "RAPPORT-SCANS-FR.md"

URL_CDB = "https://fr.marvelcdb.com/api/public/cards/?encounter=1"
URL_OCTGN = (
    "https://codeload.github.com/twistedsistem/OCTGN-Marvel-Champions/"
    "tar.gz/refs/heads/master"
)

PREFIXE = "fr_"
NOM_IMAGE = re.compile(r"^([0-9a-f-]{36})(\.[bc])?\.jpg$", re.IGNORECASE)
CODE_CARTE = re.compile(r"^\d{5}[a-z]?$")
BALISES_GARDEES = re.compile(r"<(?!/?(b|i|em|strong|br)\b)[^>]*>")


def charger_marvelcdb():
    """GUID vers codes, et code vers texte francais. Une seule requete."""
    with urllib.request.urlopen(URL_CDB, timeout=60) as reponse:
        cartes = json.load(reponse)
    par_guid = collections.defaultdict(set)
    textes = {}
    for carte in cartes:
        guid = carte.get("octgn_id")
        if guid:
            par_guid[guid.lower()].add(carte["code"])
        if carte.get("text"):
            textes[carte["code"]] = BALISES_GARDEES.sub("", carte["text"])
    return par_guid, textes


def charger_octgn():
    """GUID vers codes selon le module OCTGN. Vide si le depot est injoignable."""
    par_guid = collections.defaultdict(set)
    try:
        with urllib.request.urlopen(URL_OCTGN, timeout=180) as reponse:
            donnees = reponse.read()
    except Exception as souci:            # reseau, certificat, depot deplace
        print(f"module OCTGN injoignable ({souci}), audit saute", file=sys.stderr)
        return par_guid, False
    with tarfile.open(fileobj=io.BytesIO(donnees), mode="r:gz") as archive:
        for membre in archive.getmembers():
            if not membre.name.endswith("set.xml"):
                continue
            fichier = archive.extractfile(membre)
            if fichier is None:
                continue
            try:
                racine = ET.parse(fichier).getroot()
            except ET.ParseError:
                continue
            for carte in racine.iter("card"):
                guid = (carte.get("id") or "").lower()
                for prop in carte.findall("property"):
                    if prop.get("name") == "CardNumber" and prop.get("value"):
                        par_guid[guid].add(prop.get("value"))
    return par_guid, True


def pic_ids_du_jeu():
    """Identifiants d'image que le jeu demandera reellement."""
    catalogue = json.loads(CARTES_JEU.read_text(encoding="utf-8"))
    ids = set()
    for cartes in catalogue.values():
        if not isinstance(cartes, list):
            continue                      # la cle « checksum » porte une chaine
        for carte in cartes:
            ids.add(carte.get("pic_id") or carte["card_id"])
    return ids


def attribuer(par_guid, ids_jeu):
    """Parcourt les archives et attribue chaque image a des codes du jeu.

    Rend (attributions, guid_inconnus, nb_images). Une attribution est
    code -> (archive, entree, taille) ; a taille egale la premiere gagne, sinon
    la plus lourde, ce qui privilegie la meilleure definition sans dependre de
    l'ordre de lecture.
    """
    attributions = {}
    inconnus = set()
    nb_images = 0
    for nom in sorted(os.listdir(PACK)):
        if not nom.endswith(".o8c"):
            continue
        with zipfile.ZipFile(PACK / nom) as archive:
            for entree in archive.infolist():
                trouve = NOM_IMAGE.match(os.path.basename(entree.filename))
                if not trouve:
                    continue              # Thumbs.db et autres residus
                nb_images += 1
                guid = trouve.group(1).lower()
                face_fichier = (trouve.group(2) or "")[1:]
                codes = par_guid.get(guid)
                if not codes:
                    inconnus.add(guid)
                    continue
                for code in codes:
                    face_code = code[5:] if len(code) > 5 else ""
                    meme_face = face_code == face_fichier or (
                        face_fichier == "" and face_code in ("", "a")
                    )
                    if not meme_face or code not in ids_jeu:
                        continue
                    ancien = attributions.get(code)
                    if ancien is None or entree.file_size > ancien[2]:
                        attributions[code] = (nom, entree.filename, entree.file_size)
    return attributions, inconnus, nb_images


def desaccords(par_guid_cdb, par_guid_octgn, guids_du_pack):
    """GUID que les deux sources rattachent a des codes entierement differents."""
    trouves = []
    for guid in sorted(guids_du_pack):
        cotes_cdb = par_guid_cdb.get(guid)
        cotes_octgn = par_guid_octgn.get(guid)
        if cotes_cdb and cotes_octgn and not (cotes_cdb & cotes_octgn):
            trouves.append((guid, sorted(cotes_cdb), sorted(cotes_octgn)))
    return trouves


def ecrire_rapport(mesures, inconnus, ecarts, manquants, audite):
    officielles = [c for c in manquants if int(c[:2]) < 61]
    fan = [c for c in manquants if int(c[:2]) >= 61]
    lignes = ["# Rapport d'import des scans FR", ""]
    if not audite:
        lignes += [
            "> Module OCTGN injoignable : cette extraction n'a PAS ete auditee.",
            "",
        ]
    lignes += ["| Mesure | Valeur |", "|---|---|"]
    for nom, valeur in mesures.items():
        lignes.append(f"| {nom} | {valeur} |")
    lignes += ["", f"## GUID inconnus de marvelcdb ({len(inconnus)})", ""]
    lignes += [f"- `{g}`" for g in sorted(inconnus)]
    lignes += ["", f"## Desaccords avec le module OCTGN ({len(ecarts)})", ""]
    lignes += ["marvelcdb l'emporte. A verifier a l'oeil dans le jeu.", ""]
    for guid, cdb, octgn in ecarts:
        lignes.append(f"- `{guid}` : marvelcdb {cdb}, module OCTGN {octgn}")
    lignes += ["", f"## Cartes officielles sans scan FR ({len(officielles)})", ""]
    lignes += [f"- `{c}`" for c in officielles]
    lignes += ["", f"## Cartes fan-made sans scan FR ({len(fan)})", ""]
    lignes += ["Attendu : ces cartes n'existent ni dans le pack, ni sur marvelcdb.", ""]
    lignes += [f"- `{c}`" for c in fan]
    RAPPORT.write_text("\n".join(lignes) + "\n", encoding="utf-8")


def main():
    analyse = argparse.ArgumentParser(description=__doc__)
    analyse.add_argument("--rapport-seul", action="store_true",
                         help="n'ecrit ni image ni module TypeScript")
    analyse.add_argument("--sans-audit", action="store_true",
                         help="ne telecharge pas le module OCTGN")
    options = analyse.parse_args()

    par_guid_cdb, textes = charger_marvelcdb()
    par_guid_octgn, audite = ({}, False) if options.sans_audit else charger_octgn()
    ids_jeu = pic_ids_du_jeu()
    attributions, inconnus, nb_images = attribuer(par_guid_cdb, ids_jeu)

    guids_du_pack = set()
    for nom in sorted(os.listdir(PACK)):
        if nom.endswith(".o8c"):
            with zipfile.ZipFile(PACK / nom) as archive:
                for entree in archive.namelist():
                    trouve = NOM_IMAGE.match(os.path.basename(entree))
                    if trouve:
                        guids_du_pack.add(trouve.group(1).lower())

    ecarts = desaccords(par_guid_cdb, par_guid_octgn, guids_du_pack)
    manquants = sorted(c for c in ids_jeu
                       if c not in attributions and CODE_CARTE.match(c))
    poids = sum(t for _, _, t in attributions.values())

    mesures = {
        "Images dans le pack": nb_images,
        "GUID distincts": len(guids_du_pack),
        "GUID inconnus de marvelcdb": len(inconnus),
        "Cartes couvertes en francais": len(attributions),
        "Cartes du jeu sans scan FR": len(manquants),
        "Desaccords avec le module OCTGN": len(ecarts),
        "Poids des images": f"{poids / 1e6:.0f} Mo",
    }
    ecrire_rapport(mesures, inconnus, ecarts, manquants, audite)
    for nom, valeur in mesures.items():
        print(f"{nom:34} {valeur}")
    print(f"rapport ecrit dans {RAPPORT}")

    # L'extraction est branchee a la tache suivante. Tant qu'elle ne l'est pas,
    # le script s'arrete ici quelle que soit l'option.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
