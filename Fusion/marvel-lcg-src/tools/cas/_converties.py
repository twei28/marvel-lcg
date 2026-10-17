# Cartes TMNT « image seule » converties en ARTS ALTERNATIFS le 17/10/2026 (plus de carte dans cards.json).
# Source unique : la colonne `converti_art_alternatif_de` de tools/tmnt_aspects_numerotation.tsv
# ({card_id retire: card_id de l'officielle}). Les modules de cas la chargent par chemin (ce fichier, prefixe
# `_`, n'est pas lu comme un bloc de cas par test_capacites.py).
import csv
import os


def lire():
    chemin = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tmnt_aspects_numerotation.tsv")
    with open(chemin, encoding="utf-8", newline="") as h:
        return {r["card_id"]: r["converti_art_alternatif_de"].strip()
                for r in csv.DictReader(h, delimiter="\t") if (r.get("converti_art_alternatif_de") or "").strip()}


CONVERTIES = lire()
