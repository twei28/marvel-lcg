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
URL_CDB_EN = "https://marvelcdb.com/api/public/cards/?encounter=1"
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


def charger_marvelcdb_anglais():
    """Code vers texte anglais, sur le modele de charger_marvelcdb().

    fr.marvelcdb.com renvoie le texte anglais tel quel pour les cartes qu'il
    n'a pas traduites : mesure, 60 des 73 entrees candidates au dictionnaire
    sont identiques caractere pour caractere a leur texte anglais, dont toute
    la gamme Daredevil 60xxx. Sans ce catalogue de comparaison, ces entrees
    s'affichaient en jeu sous un bloc titre « francais » alors qu'elles ne le
    sont pas : un mensonge a l'ecran.
    """
    with urllib.request.urlopen(URL_CDB_EN, timeout=60) as reponse:
        cartes = json.load(reponse)
    return {
        carte["code"]: BALISES_GARDEES.sub("", carte["text"])
        for carte in cartes
        if carte.get("text")
    }


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


def est_fan_made(code):
    """Les codes fan-made de ce projet vont de 61xxx a 75xxx.

    Au-dela, le prefixe redevient officiel : le set Ronan (90001-90005),
    notamment, a des scans francais et n'a rien de fan-made. Une comparaison
    ">= 61" seule les comptait a tort.
    """
    prefixe = int(code[:2])
    return 61 <= prefixe <= 75


def ecrire_rapport(mesures, inconnus, ecarts, manquants, audite):
    officielles = [c for c in manquants if not est_fan_made(c)]
    fan = [c for c in manquants if est_fan_made(c)]
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


def extraire(attributions):
    """Ecrit une image par code couvert. Ne relit pas une archive deux fois."""
    SORTIE_IMAGES.mkdir(parents=True, exist_ok=True)
    par_archive = collections.defaultdict(list)
    for code, (nom_archive, entree, _) in attributions.items():
        par_archive[nom_archive].append((code, entree))
    ecrites = 0
    for nom_archive in sorted(par_archive):
        with zipfile.ZipFile(PACK / nom_archive) as archive:
            for code, entree in par_archive[nom_archive]:
                cible = SORTIE_IMAGES / f"{PREFIXE}{code}.jpg"
                cible.write_bytes(archive.read(entree))
                ecrites += 1
    return ecrites


def ecrire_modules(attributions, textes, textes_en, ids_jeu):
    """Les deux modules TypeScript consommes par le plateau.

    Le dictionnaire est restreint aux cartes SANS scan francais ET presentes
    dans le catalogue du jeu (ids_jeu) : c'est le seul endroit ou il sert.
    marvelcdb renvoie du texte pour des cartes hors catalogue (autres boites,
    non implementees ici) ; sans le filtre sur ids_jeu ces cartes inutiles
    s'ajoutaient au dictionnaire. Complet il pesait 914 Ko, restreint il en
    pese 13.

    Deuxieme filtre : une entree est ecartee quand son texte francais est
    identique, caractere pour caractere, au texte anglais (textes_en). C'est
    le cas quand fr.marvelcdb.com n'a pas traduit la carte et renvoie
    l'anglais tel quel ; l'afficher sous un bloc titre « francais » serait
    un mensonge a l'ecran. Mesure : 60 des 73 entrees candidates tombent
    dans ce cas.
    """
    codes = sorted(attributions)
    liste = SORTIE_TS / "scans-fr-liste.ts"
    liste.write_text(
        "// Genere par tools/importer_scans_fr.py — NE PAS EDITER A LA MAIN.\n"
        "//\n"
        "// Codes de carte qui disposent d'un scan francais dans assets/pics-fr.\n"
        "// Liste vide = pack FR non importe : le plateau reste integralement en anglais.\n"
        "export const CODES_SCAN_FR: ReadonlySet<string> = new Set([\n"
        + "".join(f"  '{code}',\n" for code in codes)
        + "])\n",
        encoding="utf-8",
    )

    sans_scan = {
        code: texte
        for code, texte in sorted(textes.items())
        if code not in attributions
        and code in ids_jeu
        and texte != textes_en.get(code)
    }
    corps = "".join(
        f"  '{code}': {json.dumps(texte, ensure_ascii=False)},\n"
        for code, texte in sans_scan.items()
    )
    (SORTIE_TS / "textes-fr.ts").write_text(
        "// Genere par tools/importer_scans_fr.py — NE PAS EDITER A LA MAIN.\n"
        "//\n"
        "// Texte francais des cartes qui n'ont PAS de scan francais : c'est le seul\n"
        "// cas ou le plateau l'affiche, sous l'apercu. Les cartes fan-made n'y sont\n"
        "// pas, marvelcdb ne les connait pas.\n"
        "//\n"
        "// Le type dit « string | undefined » parce que la plupart des codes sont\n"
        "// ABSENTS : sans cela le plateau croirait tenir un texte pour chaque carte.\n"
        "export const TEXTES_FR: Readonly<Record<string, string | undefined>> = {\n"
        + corps
        + "}\n",
        encoding="utf-8",
    )
    return len(codes), len(sans_scan)


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

    if options.rapport_seul:
        print("mode rapport : aucune image ni module ecrit")
        return 0

    ecrites = extraire(attributions)
    textes_en = charger_marvelcdb_anglais()
    nb_codes, nb_textes = ecrire_modules(attributions, textes, textes_en, ids_jeu)
    print(f"{'Images ecrites':34} {ecrites}")
    print(f"{'Codes dans scans-fr-liste.ts':34} {nb_codes}")
    print(f"{'Entrees dans textes-fr.ts':34} {nb_textes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
