from core import *

from engine.config import ConfigVariables
from engine.log import Log

# ===========================================================================
# LES COULEURS DE CHAQUE HEROS.
#
# AJOUT du 14/09/2026, aucun equivalent dans le moteur officiel.
#
# Pourquoi ce fichier existe : le plateau teinte son coin bas droit aux
# couleurs du heros qu'on regarde. Ces couleurs ne sont ecrites nulle part
# dans les donnees de carte ; elles sont sur le CONTOUR des illustrations,
# deux ou trois traits par carte, les memes sur tout un deck.
#
# ⚠ RIEN NE SE CALCULE ICI. `outils/palettes-heros.py` echantillonne les
# contours une fois pour toutes et ecrit `data/palettes-heros.json`. Les
# images ne changent pas : analyser en pleine partie serait payer a chaque
# tour ce qui se mesure une seule fois.
#
# ⚠ LA CLE EST LA CARTE D'IDENTITE (`card_id`), ET LES DEUX FACES PORTENT LA
# MEME PALETTE. On se transforme en cours de partie ; la couleur du fond ne
# doit pas sauter quand Peter Parker enfile son costume.
#
# ⚠ FICHIER ABSENT = AUCUNE TEINTE, JAMAIS UNE ERREUR. Le halo est un
# agrement : un serveur sans ce fichier joue exactement pareil, sur fond uni.
# ===========================================================================

PALETTES_HEROS_FILE = ConfigVariables.File('palettes_heros_file', './data/palettes-heros.json')


class PalettesHeros:
    """Le releve des couleurs, charge une fois par serveur."""

    _palettes: Dict[str, List[List[int]]] | None = None

    @staticmethod
    def Toutes() -> Dict[str, List[List[int]]]:
        if PalettesHeros._palettes is not None:
            return PalettesHeros._palettes
        palettes: Dict[str, List[List[int]]] = {}
        try:
            import json
            with open(PALETTES_HEROS_FILE.value, encoding='utf-8') as f:
                donnees = json.load(f)
            brut = donnees.get('palettes') if isinstance(donnees, dict) else None
            if isinstance(brut, dict):
                for cle, valeur in brut.items():
                    if not isinstance(valeur, list):
                        continue
                    couleurs = [
                        [int(c) for c in couleur]
                        for couleur in valeur
                        if isinstance(couleur, list) and len(couleur) == 3
                    ]
                    if couleurs:
                        palettes[str(cle)] = couleurs
        except FileNotFoundError:
            # Normal sur un serveur qui n'a jamais lance l'outil. Silence.
            pass
        except Exception as erreur:
            Log.Warn("FILE", f"palettes-heros.json illisible ({erreur}), aucune teinte")
        PalettesHeros._palettes = palettes
        return palettes
