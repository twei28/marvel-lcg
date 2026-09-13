"""Ce que le releve des illustrations promet, et ce qu'il ne promet pas.

    python3 outils/test_releve_images.py

⚠ LE CAS QUI COMPTE LE PLUS est `cle_absente_n_est_pas_liste_vide`. Tout le
dispositif repose dessus : une carte qu'on n'a pas encore regardee garde
l'approximation du jeu, une carte regardee sans personne dessus repond non. Les
confondre transformerait 5746 cartes non relevees en 5746 cartes « sans
personne », et Muse ne se declencherait plus jamais.
"""

import json
import os
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RACINE, 'Fusion', 'marvel-lcg-src', 'src')
DATA = os.path.join(RACINE, 'Fusion', 'marvel-lcg-src', 'data')
sys.path.insert(0, SRC)

echecs = []


def verifier(nom, obtenu, attendu):
    if obtenu == attendu:
        print(f"  ok   {nom}")
    else:
        print(f"  ECHEC {nom} : obtenu {obtenu!r}, attendu {attendu!r}")
        echecs.append(nom)


class FauxPaper:
    """Ce que le moteur passe : un `Paper`, dont seuls deux champs comptent."""

    def __init__(self, card_id, pic_id=''):
        self.card_id = card_id
        self.pic_id = pic_id


def main():
    from cards.images_cartes import ImagesCartes, Identites, IMAGES_CARTES_FILE, IDENTITES_FILE

    print("Releve : ce qui est dedans, ce qui n'y est pas")
    dossier = tempfile.mkdtemp(prefix='releve-')
    chemin = os.path.join(dossier, 'images_cartes.json')
    with open(chemin, 'w', encoding='utf-8') as f:
        json.dump({'version': 1, 'cartes': {
            '01002': ['spider-man-peter-parker'],
            '01005': [],
            '01007': ['spider-man-peter-parker', 'rhino'],
        }}, f)
    # On ecrit `value` directement : `SetDefault` refuse une variable deja
    # servie, et ici on veut justement la detourner vers un fichier temporaire.
    IMAGES_CARTES_FILE.value = chemin
    ImagesCartes.Recharger()

    verifier("carte relevee avec quelqu'un dessus",
             ImagesCartes.IdentitesSur(FauxPaper('01002')), ['spider-man-peter-parker'])
    verifier("carte relevee SANS personne : relevee, mais vide",
             (ImagesCartes.EstRelevee(FauxPaper('01005')),
              ImagesCartes.IdentitesSur(FauxPaper('01005'))), (True, []))
    verifier("cle_absente_n_est_pas_liste_vide",
             (ImagesCartes.EstRelevee(FauxPaper('01006')),
              ImagesCartes.IdentitesSur(FauxPaper('01006'))), (False, []))
    verifier("plusieurs personnes sur une meme image",
             ImagesCartes.IdentitesSur(FauxPaper('01007')),
             ['spider-man-peter-parker', 'rhino'])

    print("\nL'unite est l'IMAGE, pas la carte")
    verifier("pic_id l'emporte sur card_id",
             ImagesCartes.IdImage(FauxPaper('55999', pic_id='01002')), '01002')
    verifier("une carte qui emprunte un scan herite du releve",
             ImagesCartes.IdentitesSur(FauxPaper('55999', pic_id='01002')),
             ['spider-man-peter-parker'])
    verifier("sans pic_id, l'image est la carte elle-meme",
             ImagesCartes.IdImage(FauxPaper('01002')), '01002')

    print("\nFichier illisible : le jeu continue, il ne plante pas")
    abime = os.path.join(dossier, 'abime.json')
    with open(abime, 'w', encoding='utf-8') as f:
        f.write('{ ceci n est pas du json')
    IMAGES_CARTES_FILE.value = abime
    ImagesCartes.Recharger()
    verifier("json casse : releve vide, aucune exception",
             (ImagesCartes.NombreReleve(), ImagesCartes.EstRelevee(FauxPaper('01002'))), (0, False))

    IMAGES_CARTES_FILE.value = os.path.join(dossier, 'absent.json')
    ImagesCartes.Recharger()
    verifier("fichier absent : releve vide, aucune exception",
             ImagesCartes.NombreReleve(), 0)

    print("\nAnnuaire : une personne, pas une carte")
    IDENTITES_FILE.value = os.path.join(DATA, 'identites.json')
    Identites.Recharger()
    verifier("les deux faces d'un heros donnent la meme personne",
             (Identites.DeLaFace(FauxPaper('01001a')), Identites.DeLaFace(FauxPaper('01001b'))),
             ('spider-man-peter-parker', 'spider-man-peter-parker'))
    verifier("les trois etapes d'un vilain donnent la meme personne",
             {Identites.DeLaFace(FauxPaper(x)) for x in ('01094', '01095', '01096')},
             {'rhino'})
    verifier("deux Spider-Man differents restent deux personnes",
             Identites.DeLaFace(FauxPaper('27030a')) != Identites.DeLaFace(FauxPaper('01001a')),
             True)
    verifier("SP//dr : la combinaison et sa pilote sont une seule personne",
             (Identites.DeLaFace(FauxPaper('31001a')), Identites.DeLaFace(FauxPaper('31002a'))),
             ('sp-dr-suit-peni-parker', 'sp-dr-suit-peni-parker'))
    verifier("une carte qui n'est l'identite de personne",
             Identites.DeLaFace(FauxPaper('01003')), '')

    print()
    if echecs:
        print(f"{len(echecs)} ECHEC(S) : " + ', '.join(echecs))
        return 1
    print("tout est vert")
    return 0


if __name__ == '__main__':
    sys.exit(main())
