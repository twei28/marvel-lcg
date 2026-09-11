"""Les faces d'identite croisees dans les scans HD (engine/lib/faces_hd.py).

    $PY tools/test_faces_hd.py

Aucune partie, aucun reseau : des images de synthese dans un dossier
temporaire. Ce que le test prouve :
- une paire dont le `a` HD est le `b` de reference (et reciproquement) est
  detectee et echangee ;
- une paire conforme n'est pas touchee ;
- une paire dont UN SEUL sens diverge (art alternatif) n'est pas touchee ;
- une paire a laquelle il manque un fichier est ignoree.
"""
import importlib.util
import os
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE = os.path.join(RACINE, "src", "engine", "lib", "faces_hd.py")
spec = importlib.util.spec_from_file_location("faces_hd", MODULE)
faces_hd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(faces_hd)

from PIL import Image, ImageDraw

ECHECS = []


def cas(nom: str, ok: bool) -> None:
    print(("OK    " if ok else "ECHEC ") + nom)
    if not ok:
        ECHECS.append(nom)


def image(chemin: str, fond: int, bande: int) -> None:
    """Une carte de synthese : un fond gris et un bandeau plus ou moins haut,
    pour que deux « faces » aient des empreintes nettement differentes."""
    im = Image.new("L", (120, 160), fond)
    ImageDraw.Draw(im).rectangle([0, 0, 120, bande], fill=255 - fond)
    im.save(chemin, "JPEG")


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ref, hd = os.path.join(tmp, "pics"), os.path.join(tmp, "pics-hd")
        os.makedirs(ref); os.makedirs(hd)
        # Reference : a = heros (sombre, bandeau court), b = alter ego (clair, bandeau long)
        for i in ("11001", "22001", "33001", "44001"):
            image(os.path.join(ref, i + "a.jpg"), 40, 30)
            image(os.path.join(ref, i + "b.jpg"), 200, 110)
        # 11001 : HD croise (a HD = b de reference, b HD = a de reference)
        image(os.path.join(hd, "11001a.jpg"), 200, 110)
        image(os.path.join(hd, "11001b.jpg"), 40, 30)
        # 22001 : HD conforme
        image(os.path.join(hd, "22001a.jpg"), 40, 30)
        image(os.path.join(hd, "22001b.jpg"), 200, 110)
        # 33001 : un seul sens diverge (a HD ressemble a b, mais b HD est bien b)
        image(os.path.join(hd, "33001a.jpg"), 200, 110)
        image(os.path.join(hd, "33001b.jpg"), 200, 110)
        # 44001 : il manque le b HD
        image(os.path.join(hd, "44001a.jpg"), 200, 110)

        heros = ["11001a", "22001a", "33001a", "44001a", "55001a"]
        croisees = faces_hd.paires_croisees(hd, ref, heros)
        cas("seule la paire croisee est detectee", croisees == [("11001a", "11001b")])

        echangees = faces_hd.redresser(hd, ref, heros)
        cas("redresser rend la paire echangee", echangees == [("11001a", "11001b")])
        a_apres = faces_hd.empreinte(os.path.join(hd, "11001a.jpg"))
        ref_a = faces_hd.empreinte(os.path.join(ref, "11001a.jpg"))
        cas("apres echange, le a HD est le heros",
            faces_hd.distance(a_apres, ref_a) < faces_hd.SEUIL_IDENTIQUE)
        cas("le fichier provisoire n'a pas ete laisse derriere",
            not any(n.endswith(".tmp") for n in os.listdir(hd)))
        cas("un second passage ne trouve plus rien a echanger",
            faces_hd.redresser(hd, ref, heros) == [])
        b_conforme = faces_hd.empreinte(os.path.join(hd, "22001b.jpg"))
        cas("la paire conforme est intacte",
            faces_hd.distance(b_conforme, faces_hd.empreinte(os.path.join(ref, "22001b.jpg"))) < faces_hd.SEUIL_IDENTIQUE)

        ids = faces_hd.identifiants_heros_de(os.path.join(RACINE, "data", "cards.json"))
        cas("cards.json donne des faces heros officielles, dont Wolverine",
            "35001a" in ids and all(i.endswith("a") and len(i) == 6 for i in ids))

    print()
    if ECHECS:
        print(f"ECHEC : {len(ECHECS)} cas rouge(s)")
        for nom in ECHECS:
            print("  - " + nom)
        sys.exit(1)
    print("OK : les faces croisees sont detectees et redressees")


if __name__ == "__main__":
    main()
