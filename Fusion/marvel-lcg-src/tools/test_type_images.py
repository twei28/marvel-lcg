"""Le type d'une image se lit dans ses OCTETS, jamais dans son nom.

    python3 tools/test_type_images.py

⚠ POURQUOI. Jusqu'au 16/09/2026, `server_files.py` annoncait `image/jpeg` pour
TOUTE image : les scans, les vignettes, les textures, le narval de l'en-tete.
Les navigateurs devinent souvent et affichent quand meme, mais pas toujours :
un PNG annonce en JPEG a fait echouer un controle qui verifie que l'image est
bien DECODEE, et non seulement recue.

C'est le meme raisonnement que `_ecrire_capture` cote site, qui refuse de faire
confiance a l'etiquette d'un envoi : seuls les premiers octets font foi.
"""
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))

echecs = []


def verifier(nom, obtenu, attendu):
    if obtenu == attendu:
        print(f"  ok   {nom}")
    else:
        print(f"  ECHEC {nom} : obtenu {obtenu!r}, attendu {attendu!r}")
        echecs.append(nom)


# On importe la fonction seule, sans demarrer le moteur : elle est statique et
# ne depend de rien.
import importlib.util  # noqa: E402

chemin = os.path.join(RACINE, "src", "engine", "device", "web", "server", "server_files.py")
source = open(chemin, encoding="utf-8").read()
debut = source.index("    def TypeImage(")
fin = source.index("    def handle_sets_image(")
corps = "class Faux:\n" + source[debut:fin].replace("    @staticmethod\n", "    @staticmethod\n", 1)
espace = {}
exec(compile("from typing import Any\n" + corps, chemin, "exec"), espace)  # noqa: S102
TypeImage = espace["Faux"].TypeImage

PNG = bytes.fromhex("89504e470d0a1a0a") + b"reste"
WEBP = b"RIFF" + b"\x00\x00\x00\x00" + b"WEBPVP8 "
GIF = b"GIF89a" + b"reste"
JPEG = bytes((0xFF, 0xD8, 0xFF, 0xE0)) + b"reste"

print("Le type d'une image, lu dans ses octets")
verifier("un PNG s'annonce en PNG", TypeImage(PNG), "image/png")
verifier("un WebP s'annonce en WebP", TypeImage(WEBP), "image/webp")
verifier("un GIF s'annonce en GIF", TypeImage(GIF), "image/gif")
verifier("un JPEG s'annonce en JPEG", TypeImage(JPEG), "image/jpeg")
# ⚠ LE REPLI COMPTE AUTANT QUE LE RESTE. La quasi-totalite des scans sont des
# JPEG ; un octet inconnu ne doit pas casser l'affichage d'une carte.
verifier("un format inconnu retombe sur le JPEG", TypeImage(b"\x00\x01\x02\x03"), "image/jpeg")
verifier("des octets vides ne levent pas", TypeImage(b""), "image/jpeg")

print()
print("ECHECS : %d" % len(echecs))
sys.exit(1 if echecs else 0)
