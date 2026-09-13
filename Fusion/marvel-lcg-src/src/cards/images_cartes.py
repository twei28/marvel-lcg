from core import *

from engine.config import ConfigVariables
from engine.log import Log

# ===========================================================================
# QUI EST DESSINE SUR CHAQUE CARTE.
#
# AJOUT du 13/09/2026, aucun equivalent dans le moteur officiel.
#
# Pourquoi ce fichier existe : quatre cartes du set modulaire Muse parlent
# d'« une carte qui porte l'image de ton identite ». Le moteur lit du texte et
# des mots-cles, il ne voit AUCUNE illustration. Personne ne peut deduire d'un
# `card_id` que Spider-Man est dessine dessus. On releve donc a la main, depuis
# la page `/releve-images.html` reservee a l'administrateur, et on range le
# resultat dans `data/images_cartes.json`.
#
# ⚠ LA CLE EST L'IMAGE, PAS LA CARTE. Une reimpression (`full_link`) et une
# carte qui emprunte le scan d'une autre (`pic_id`) montrent LA MEME
# ILLUSTRATION : les relever deux fois serait du travail en double, et surtout
# deux verites possibles pour une seule image. 6153 cartes, 5746 images.
#
# ⚠ RELEVE VIDE ET CARTE NON RELEVEE NE SONT PAS LA MEME CHOSE :
#   - cle presente, liste vide  -> « regarde, il n'y a aucune identite dessus »
#                                  (un lieu, un objet, un civil sans nom) ;
#   - cle absente               -> « pas encore regarde », et l'appelant
#                                  retombe alors sur son approximation.
# Confondre les deux transformerait 5746 cartes non relevees en 5746 cartes
# « sans personne dessus », et Muse ne se declencherait plus jamais. D'ou
# `EstRelevee()`, separee de `IdentitesSur()`.
# ===========================================================================

IMAGES_CARTES_FILE = ConfigVariables.File('images_cartes_file', './data/images_cartes.json')
IDENTITES_FILE     = ConfigVariables.File('identites_file', './data/identites.json')


class ImagesCartes:
    """Le releve, charge une fois, consulte a chaque carte jouee."""

    _releve: Dict[str, List[str]] | None = None

    @staticmethod
    def _charger() -> Dict[str, List[str]]:
        if ImagesCartes._releve is not None:
            return ImagesCartes._releve
        releve: Dict[str, List[str]] = {}
        chemin = IMAGES_CARTES_FILE.value
        try:
            import json
            with open(chemin, encoding='utf-8') as f:
                donnees = json.load(f)
            brut = donnees.get('cartes') if isinstance(donnees, dict) else None
            if isinstance(brut, dict):
                for cle, valeur in brut.items():
                    if isinstance(valeur, list):
                        releve[str(cle)] = [str(x) for x in valeur]
        except FileNotFoundError:
            # Normal : un serveur qui n'a jamais rien releve. Silence.
            pass
        except Exception as erreur:
            # ⚠ ON NE PLANTE PAS. Un fichier abime ne doit pas empecher de
            # jouer : le jeu entier n'en depend pas, seules quatre cartes
            # perdent leur precision et reprennent leur approximation.
            Log.Warn("FILE", f"images_cartes.json illisible ({erreur}), releve ignore")
        ImagesCartes._releve = releve
        return releve

    @staticmethod
    def Recharger() -> None:
        """Oublie le cache. Appele apres une ecriture depuis la page de releve,
        pour que la partie en cours tienne compte du travail qui vient d'etre
        fait sans redemarrer le serveur."""
        ImagesCartes._releve = None

    @staticmethod
    def IdImage(paper: 'Any') -> str:
        """L'ILLUSTRATION que porte cette carte, pas la carte.

        Meme resolution que `Cache.SetLinkPic` dans `cards/database.py` :
        `pic_id` d'abord (la carte emprunte explicitement un scan), la carte
        d'origine ensuite si c'est une reimpression, son propre id sinon.
        """
        if paper is None:
            return ""
        pic_id = getattr(paper, 'pic_id', '') or ''
        if pic_id:
            return str(pic_id)
        card_id = str(getattr(paper, 'card_id', '') or '')
        from cards.database import CardsDB
        return str(CardsDB.full_link_cards.get(card_id, card_id))

    @staticmethod
    def EstRelevee(paper: 'Any') -> bool:
        """A-t-on deja REGARDE cette illustration ? Distinct de « quelqu'un est
        dessus » : voir l'avertissement en tete de fichier."""
        return ImagesCartes.IdImage(paper) in ImagesCartes._charger()

    @staticmethod
    def IdentitesSur(paper: 'Any') -> List[str]:
        """Les identites dessinees sur cette carte. Vide si aucune, vide aussi
        si la carte n'a pas encore ete relevee : n'appelez ceci qu'apres
        `EstRelevee()`, ou acceptez de traiter les deux cas pareil."""
        return list(ImagesCartes._charger().get(ImagesCartes.IdImage(paper), []))

    @staticmethod
    def NombreReleve() -> int:
        return len(ImagesCartes._charger())


class Identites:
    """L'annuaire des personnes : `data/identites.json`.

    GENERE par `outils/annuaire-identites.py`, jamais ecrit a la main. Il
    repond a une seule question : cette carte de heros, d'alter ego, de vilain
    ou de sbire unique, c'est QUI ?

    ⚠ UNE PERSONNE N'EST PAS UNE CARTE. Spider-Man est douze faces (l'officiel,
    les fan-made, les deux cotes de chacun), Rhino est quatre cartes (ses trois
    etapes plus une reprise), Ironheart en est six. Le releve des illustrations
    designe la PERSONNE ; sans quoi relever « Rhino » sur une image obligerait a
    choisir laquelle de ses trois etapes est dessinee, question qui n'a pas de
    reponse.
    """

    _par_face: Dict[str, str] | None = None
    _noms: Dict[str, str] | None = None

    @staticmethod
    def _charger() -> None:
        if Identites._par_face is not None:
            return
        par_face: Dict[str, str] = {}
        noms: Dict[str, str] = {}
        try:
            import json
            with open(IDENTITES_FILE.value, encoding='utf-8') as f:
                donnees = json.load(f)
            for entree in donnees.get('identites', []):
                id_personne = str(entree.get('id') or '')
                if not id_personne:
                    continue
                noms[id_personne] = str(entree.get('nom') or id_personne)
                for face in entree.get('faces', []):
                    par_face[str(face)] = id_personne
        except FileNotFoundError:
            Log.Warn("FILE", "identites.json absent : lancez outils/annuaire-identites.py --ecrire")
        except Exception as erreur:
            Log.Warn("FILE", f"identites.json illisible ({erreur})")
        Identites._par_face = par_face
        Identites._noms = noms

    @staticmethod
    def Recharger() -> None:
        Identites._par_face = None
        Identites._noms = None

    @staticmethod
    def DeLaFace(paper: 'Any') -> str:
        """Qui est cette carte d'identite ? Chaine vide si ce n'en est pas une,
        ou si l'annuaire ne la connait pas encore."""
        Identites._charger()
        assert Identites._par_face is not None
        card_id = str(getattr(paper, 'card_id', '') or '')
        return Identites._par_face.get(card_id, '')

    @staticmethod
    def Nom(id_personne: str) -> str:
        Identites._charger()
        assert Identites._noms is not None
        return Identites._noms.get(id_personne, id_personne)
