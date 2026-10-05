#!/usr/bin/env python3
"""Calibre les bulles de stats sur les scans reels servis par le jeu.

Le plateau superpose des PNG transparents aux bulles imprimees des scans. Les
ratios par type de carte ne suffisent pas : les scans n'ont pas tous le meme
cadrage. Ce script detecte donc les bulles colorees dans chaque image et genere
un fichier TypeScript importe par ScanCard.
"""

from __future__ import annotations

import argparse
import colorsys
import json
import re
import statistics
from collections import deque
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from PIL import Image

RACINE_APP = Path(__file__).resolve().parents[1]
RACINE_DEPOT = RACINE_APP.parent
CARTES_JSON = RACINE_DEPOT / "Fusion" / "marvel-lcg-src" / "data" / "cards.json"
SORTIE = RACINE_APP / "src" / "components" / "stat-bubbles" / "positions.ts"
CACHE = RACINE_APP / ".cache" / "stat-scans"
PICS = RACINE_DEPOT / "Fusion" / "marvel-lcg-src" / "assets" / "pics"

# Arts alternatifs de heros et d'alter-egos : « 01001a_cb ». Leurs stats
# imprimees ne sont pas aux memes endroits que sur la carte officielle.
ART_ALTERNATIF = re.compile(r"^(\d{5}[ab])_(cb|m3t|rog2?)\.jpg$")

FRAME_H_SUR_W = 176 / 127
LABELS = ("THW", "ATK", "DEF", "REC", "SCH")

TYPE_LABELS: dict[str, tuple[str, ...]] = {
    "Hero": ("THW", "ATK", "DEF"),
    "AlterEgo": ("REC",),
    "Ally": ("THW", "ATK"),
    "Minion": ("SCH", "ATK"),
    "Villain": ("SCH", "ATK"),
}

# Zones larges de recherche, en fractions de l'image source.
RECHERCHE: dict[str, dict[str, tuple[float, float, float, float]]] = {
    "Hero": {
        "THW": (0.0, 0.12, 0.30, 0.30),
        "ATK": (0.0, 0.25, 0.30, 0.43),
        "DEF": (0.0, 0.38, 0.30, 0.56),
    },
    "AlterEgo": {
        "REC": (0.0, 0.12, 0.30, 0.30),
    },
    "Ally": {
        "THW": (0.0, 0.16, 0.32, 0.34),
        "ATK": (0.0, 0.34, 0.32, 0.53),
    },
    "Minion": {
        "SCH": (0.0, 0.10, 0.35, 0.30),
        "ATK": (0.0, 0.24, 0.35, 0.42),
    },
    "Villain": {
        "SCH": (0.0, 0.10, 0.35, 0.30),
        "ATK": (0.0, 0.24, 0.35, 0.42),
    },
}

# Position attendue du haut de la bulle coloree, en fraction de l'image source.
# Sert seulement a choisir entre plusieurs zones colorees candidates.
Y_ATTENDU: dict[str, dict[str, float]] = {
    "Hero": {"THW": 0.156, "ATK": 0.296, "DEF": 0.441},
    "AlterEgo": {"REC": 0.156},
    "Ally": {"THW": 0.195, "ATK": 0.400},
    "Minion": {"SCH": 0.168, "ATK": 0.294},
    "Villain": {"SCH": 0.168, "ATK": 0.294},
}


# Les arts « cb » partagent TOUS le meme gabarit (mesure sur 140 images, dispersion
# nulle) : on pose les boites en pixels d'une image 600x860 au lieu de les
# detecter, car la detection par couleur accroche parfois l'illustration. Les
# rares « cb » d'une autre taille retombent sur la detection, avec ces zones.
TAILLE_GABARIT_CB = (600, 860)
GABARIT_CB: dict[str, tuple[int, int, int, int]] = {
    "THW": (24, 237, 94, 290),
    "ATK": (23, 328, 95, 382),
    "DEF": (23, 420, 95, 474),
    "REC": (26, 235, 100, 290),
}
RECHERCHE["HeroCB"] = {
    "THW": (0.0, 0.22, 0.30, 0.42),
    "ATK": (0.0, 0.36, 0.30, 0.54),
    "DEF": (0.0, 0.48, 0.30, 0.66),
}
Y_ATTENDU["HeroCB"] = {"THW": 0.29, "ATK": 0.41, "DEF": 0.52}
RECHERCHE["AlterEgoCB"] = {"REC": (0.0, 0.22, 0.30, 0.42)}
Y_ATTENDU["AlterEgoCB"] = {"REC": 0.29}


def valeur_stat(brut: object) -> bool:
    return isinstance(brut, str) and re.match(r"^\d+\*?$", brut) is not None


def cartes_a_calibrer() -> list[tuple[str, str, list[str]]]:
    donnees = json.loads(CARTES_JSON.read_text(encoding="utf-8"))
    cartes: list[tuple[str, str, list[str]]] = []
    for paquet in donnees.values():
        if not isinstance(paquet, list):
            continue
        for carte in paquet:
            if not isinstance(carte, dict):
                continue
            card_id = carte.get("card_id")
            type_carte = carte.get("type")
            desc = carte.get("desc")
            if not isinstance(card_id, str) or type_carte not in TYPE_LABELS or not isinstance(desc, dict):
                continue
            labels = [label for label in TYPE_LABELS[type_carte] if valeur_stat(desc.get(label))]
            if labels:
                cartes.append((card_id, type_carte, labels))
    return cartes


def faces_alternatives(officielles: dict[str, tuple[str, list[str]]]) -> list[tuple[str, str, str, list[str]]]:
    """(pic_id de l'art, style, type de la carte officielle, ses labels)."""
    faces: list[tuple[str, str, str, list[str]]] = []
    for chemin in sorted(PICS.iterdir()):
        trouve = ART_ALTERNATIF.match(chemin.name)
        if not trouve or trouve.group(1) not in officielles:
            continue
        type_carte, labels = officielles[trouve.group(1)]
        if type_carte in ("Hero", "AlterEgo"):
            faces.append((chemin.stem, trouve.group(2), type_carte, labels))
    return faces


def calibrer_alternative(
    image: Image.Image, style: str, type_carte: str, labels: list[str]
) -> dict[str, dict[str, float]]:
    par_label: dict[str, dict[str, float]] = {}
    gabarit_cb = style == "cb" and image.size == TAILLE_GABARIT_CB
    zones = type_carte + "CB" if style == "cb" else type_carte
    for label in labels:
        boite = GABARIT_CB.get(label) if gabarit_cb else detecter_bulle(image, zones, label)
        if boite is not None:
            par_label[label] = convertir_vers_frame(image, boite)
    return par_label


def completer_par_mediane(
    positions: dict[str, dict[str, dict[str, float]]],
    alternatives: list[tuple[str, str, str, list[str]]],
) -> None:
    """Les arts rog et m3t suivent un gabarit unique par type de carte : une
    bulle que la detection ne trouve pas (illustration trop chargee) prend la
    mediane des autres faces du meme style, plutot que de retomber sur la
    position officielle, fausse pour cet art."""
    par_style: dict[tuple[str, str, str], list[dict[str, float]]] = {}
    for pic_id, style, type_carte, labels in alternatives:
        if style == "cb":
            continue
        for label, boite in positions.get(pic_id, {}).items():
            par_style.setdefault((style, type_carte, label), []).append(boite)
    for pic_id, style, type_carte, labels in alternatives:
        if style == "cb":
            continue
        for label in labels:
            if label in positions.get(pic_id, {}):
                continue
            echantillon = par_style.get((style, type_carte, label))
            if not echantillon:
                print(f"  sans repli : {pic_id} {label}")
                continue
            positions.setdefault(pic_id, {})[label] = {
                cle: round(statistics.median(b[cle] for b in echantillon), 5)
                for cle in ("x", "y", "w", "h")
            }
            print(f"  complete par mediane : {pic_id} {label}")


def charger_scan(base_url: str, pic_id: str) -> Image.Image | None:
    CACHE.mkdir(parents=True, exist_ok=True)
    chemin = CACHE / f"{pic_id}.img"
    if chemin.exists():
        data = chemin.read_bytes()
    else:
        try:
            requete = Request(f"{base_url.rstrip('/')}/scan/{pic_id}", headers={"Accept-Encoding": "identity"})
            data = urlopen(requete, timeout=10).read()
        except (HTTPError, URLError, TimeoutError):
            return None
        chemin.write_bytes(data)
    try:
        return Image.open(BytesIO(data)).convert("RGB")
    except OSError:
        return None


def couleur_stat(rgb: tuple[int, int, int], label: str) -> bool:
    r, g, b = rgb
    maximum = max(rgb)
    minimum = min(rgb)
    if maximum < 45 or maximum - minimum < 25:
        return False
    teinte, saturation, valeur = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    degres = teinte * 360
    if label in {"THW", "SCH"}:
        return 175 <= degres <= 245 and saturation > 0.25 and valeur > 0.20
    if label == "ATK":
        return (degres <= 25 or degres >= 335) and saturation > 0.25 and valeur > 0.20
    if label == "REC":
        return 35 <= degres <= 75 and saturation > 0.25 and valeur > 0.24
    if label == "DEF":
        return 75 <= degres <= 165 and saturation > 0.20 and valeur > 0.18
    return False


def composants(masque: set[tuple[int, int]]) -> list[tuple[int, tuple[int, int, int, int]]]:
    vus: set[tuple[int, int]] = set()
    resultat: list[tuple[int, tuple[int, int, int, int]]] = []
    voisins = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))
    for depart in list(masque):
        if depart in vus:
            continue
        file: deque[tuple[int, int]] = deque([depart])
        vus.add(depart)
        xs: list[int] = []
        ys: list[int] = []
        while file:
            x, y = file.popleft()
            xs.append(x)
            ys.append(y)
            for dx, dy in voisins:
                suivant = (x + dx, y + dy)
                if suivant in masque and suivant not in vus:
                    vus.add(suivant)
                    file.append(suivant)
        if len(xs) > 15:
            resultat.append((len(xs), (min(xs), min(ys), max(xs) + 1, max(ys) + 1)))
    return sorted(resultat, reverse=True, key=lambda item: item[0])


def detecter_bulle(image: Image.Image, type_carte: str, label: str) -> tuple[int, int, int, int] | None:
    largeur, hauteur = image.size
    rx0, ry0, rx1, ry1 = RECHERCHE[type_carte][label]
    x0, y0, x1, y1 = (
        int(rx0 * largeur),
        int(ry0 * hauteur),
        int(rx1 * largeur),
        int(ry1 * hauteur),
    )
    pixels = image.load()
    masque: set[tuple[int, int]] = set()
    for y in range(max(0, y0), min(hauteur, y1)):
        for x in range(max(0, x0), min(largeur, x1)):
            if couleur_stat(pixels[x, y], label):
                masque.add((x, y))

    candidats = []
    y_attendu = Y_ATTENDU[type_carte][label] * hauteur
    for aire, boite in composants(masque):
        bx0, by0, bx1, by1 = boite
        bw = bx1 - bx0
        bh = by1 - by0
        if not (0.08 * largeur <= bw <= 0.24 * largeur):
            continue
        if not (0.045 * hauteur <= bh <= 0.12 * hauteur):
            continue
        if bx0 > 0.08 * largeur:
            continue
        score = abs(by0 - y_attendu) + bx0 * 0.35 - aire * 0.002
        candidats.append((score, boite))

    if not candidats:
        return None

    _, boite = min(candidats, key=lambda item: item[0])
    return boite


def convertir_vers_frame(image: Image.Image, boite: tuple[int, int, int, int]) -> dict[str, float]:
    largeur, hauteur = image.size
    scale = max(1 / largeur, FRAME_H_SUR_W / hauteur)
    largeur_affichee = largeur * scale
    hauteur_affichee = hauteur * scale
    offset_x = (1 - largeur_affichee) / 2
    offset_y = (FRAME_H_SUR_W - hauteur_affichee) / 2

    x0, y0, x1, y1 = boite
    # La detection vise la zone coloree. On agrandit legerement pour que le PNG
    # transparent recouvre aussi le vieux contour blanc, sans manger le label noir.
    pad_x = max(1, round(largeur * 0.006))
    pad_y = max(1, round(hauteur * 0.004))
    x0 = max(0, x0 - pad_x)
    x1 = min(largeur, x1 + pad_x)
    y0 = max(0, y0 - pad_y)
    y1 = min(hauteur, y1 + pad_y)

    return {
        "x": (x0 * scale + offset_x),
        "y": (y0 * scale + offset_y) / FRAME_H_SUR_W,
        "w": ((x1 - x0) * scale),
        "h": ((y1 - y0) * scale) / FRAME_H_SUR_W,
    }


def formater_nombre(valeur: float) -> str:
    return f"{valeur:.5f}".rstrip("0").rstrip(".")


def ecrire_positions(positions: dict[str, dict[str, dict[str, float]]]) -> None:
    lignes = [
        "// Genere par outils/calibrer-stat-bubbles.py. Ne pas editer a la main.",
        "",
        "export type StatBubbleLabel = 'THW' | 'ATK' | 'DEF' | 'REC' | 'SCH'",
        "export type StatBubbleBox = { x: number; y: number; w: number; h: number }",
        "export type StatBubblePositions = Partial<Record<StatBubbleLabel, StatBubbleBox>>",
        "",
        "export const STAT_BUBBLE_POSITIONS: Record<string, StatBubblePositions> = {",
    ]
    for pic_id in sorted(positions):
        morceaux = []
        for label in LABELS:
            if label not in positions[pic_id]:
                continue
            boite = positions[pic_id][label]
            morceaux.append(
                f"{label}: {{ x: {formater_nombre(boite['x'])}, y: {formater_nombre(boite['y'])}, "
                f"w: {formater_nombre(boite['w'])}, h: {formater_nombre(boite['h'])} }}"
            )
        lignes.append(f"  {pic_id!r}: {{ {', '.join(morceaux)} }},")
    lignes.append("}")
    lignes.append("")
    SORTIE.write_text("\n".join(lignes), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:2345")
    args = parser.parse_args()

    positions: dict[str, dict[str, dict[str, float]]] = {}
    cartes = cartes_a_calibrer()
    erreurs = 0
    for index, (pic_id, type_carte, labels) in enumerate(cartes, start=1):
        image = charger_scan(args.base_url, pic_id)
        if image is None:
            erreurs += 1
            continue
        par_label: dict[str, dict[str, float]] = {}
        for label in labels:
            boite = detecter_bulle(image, type_carte, label)
            if boite is None:
                continue
            par_label[label] = convertir_vers_frame(image, boite)
        if par_label:
            positions[pic_id] = par_label
        if index % 100 == 0:
            print(f"{index}/{len(cartes)} cartes analysees...")

    officielles = {pic_id: (type_carte, labels) for pic_id, type_carte, labels in cartes}
    alternatives = faces_alternatives(officielles)
    for pic_id, style, type_carte, labels in alternatives:
        image = Image.open(PICS / f"{pic_id}.jpg").convert("RGB")
        par_label = calibrer_alternative(image, style, type_carte, labels)
        if len(par_label) < len(labels):
            print(f"  incomplet : {pic_id} ({len(par_label)}/{len(labels)})")
        if par_label:
            positions[pic_id] = par_label
    completer_par_mediane(positions, alternatives)
    print(f"{len(alternatives)} arts alternatifs de heros et d'alter-egos traites.")

    ecrire_positions(positions)
    print(f"{len(positions)} cartes calibrees sur {len(cartes)} candidates. {erreurs} scans illisibles.")
    print(f"Ecrit : {SORTIE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
