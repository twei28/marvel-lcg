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

# ===========================================================================
# LES CORRECTIONS A LA MAIN (19/09/2026).
#
# Demande de l'utilisateur, 18/09/2026 : « pour chaque personnage, on a une
# couleur en bas a droite de l'ecran, et certaines ne sont pas correctes. Un
# mode disponible que pour moi, ou je peux mettre le hex principal, secondaire
# et tertiaire de chaque personnage. »
#
# ⚠ UN FICHIER A PART, ET C'EST TOUTE L'IDEE. `outils/palettes-heros.py`
# REECRIT `palettes-heros.json` a chaque passe : une correction posee dedans
# serait effacee a la premiere regeneration. Elle vit donc a cote, et se pose
# PAR-DESSUS le releve genere.
#
# ⚠ LE DEPLOIEMENT NE DOIT PAS L'ECRASER, NI L'IGNORER. On corrige aux DEUX
# endroits (editeur local, editeur en ligne) et une correction vaut pour tout le
# monde. `deploiement/deployer-linux.sh` exclut ce fichier de l'archive de code
# et le FUSIONNE a part (`outils/fusionner-palettes.py`, a trois : base = derniere
# synchro) : une carte changee d'un seul cote prend ce cote, changee des deux, le
# poste gagne. Avant le 21/10/2026 il n'allait que dans le sens serveur -> depot,
# et les corrections locales n'arrivaient jamais en ligne.
# ===========================================================================
PALETTES_CORRECTIONS_FILE = ConfigVariables.File(
    'palettes_heros_corrections_file', './data/palettes-heros-corrections.json')


def _lire_palettes(chemin: str, quoi: str) -> Dict[str, List[List[int]]]:
    """Le releve d'un fichier de palettes, ou un releve vide.

    ⚠ FICHIER ABSENT = AUCUNE TEINTE, JAMAIS UNE ERREUR. Vaut pour le releve
    genere comme pour les corrections : le halo est un agrement.
    """
    palettes: Dict[str, List[List[int]]] = {}
    try:
        import json
        with open(chemin, encoding='utf-8') as f:
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
        # Normal sur un serveur qui n'a jamais lance l'outil, et normal tant
        # que personne n'a corrige une palette. Silence.
        pass
    except Exception as erreur:
        Log.Warn("FILE", f"{quoi} illisible ({erreur}), aucune teinte")
    return palettes


class PalettesHeros:
    """Le releve des couleurs, charge une fois par serveur."""

    _palettes: Dict[str, List[List[int]]] | None = None
    _corrections: Dict[str, List[List[int]]] | None = None

    @staticmethod
    def Toutes() -> Dict[str, List[List[int]]]:
        """Le releve genere, corrections a la main POSEES PAR-DESSUS."""
        if PalettesHeros._palettes is not None:
            return PalettesHeros._palettes
        palettes = _lire_palettes(PALETTES_HEROS_FILE.value, 'palettes-heros.json')
        palettes.update(PalettesHeros.Corrections())
        PalettesHeros._palettes = palettes
        return palettes

    @staticmethod
    def Corrections() -> Dict[str, List[List[int]]]:
        """Les seules corrections, sans le releve genere.

        L'editeur en a besoin pour dire ce qui a deja ete corrige, et pour
        proposer de revenir a la couleur mesuree.
        """
        if PalettesHeros._corrections is None:
            PalettesHeros._corrections = _lire_palettes(
                PALETTES_CORRECTIONS_FILE.value, 'palettes-heros-corrections.json')
        return PalettesHeros._corrections

    @staticmethod
    def Generees() -> Dict[str, List[List[int]]]:
        """Le releve genere SEUL, sans les corrections."""
        return _lire_palettes(PALETTES_HEROS_FILE.value, 'palettes-heros.json')

    @staticmethod
    def Recharger() -> None:
        """Oublie ce qui est en cache.

        ⚠ Sans ceci, une couleur corrigee pendant une partie n'arriverait au
        plateau qu'au prochain redemarrage du serveur, et l'auteur croirait a
        un defaut. Meme raison que `ImagesCartes.Recharger()`.
        """
        PalettesHeros._palettes = None
        PalettesHeros._corrections = None
