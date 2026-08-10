"""Remplace les cartes en PROXY par leur vrai scan, quand il existe en ligne.

Une carte « proxy » est une image FABRIQUEE par le moteur faute de scan : un
rectangle beige ou le texte est simplement ecrit, avec la mention « PROXY
<card_id> » en bas. Le jeu en compte 42, dont 27 pour la seule boite 060 Fear
No Evil (Daredevil et Echo). Elles se reconnaissent a leur taille, 450x630,
qu'aucun vrai scan n'a.

Le moteur sait deja telecharger une image absente depuis `image_servers`
(cache.py). Il ne le fait jamais ici : un fichier EXISTE, donc il s'arrete la.
D'ou cet outil, qui va chercher le vrai scan et remplace le proxy.

    ~/marvel-work/python/bin/python3.10 tools/remplacer_proxies.py [--pour-de-vrai]

Sans `--pour-de-vrai`, rien n'est ecrit : l'outil dit seulement ce qu'il
trouverait. Les proxies remplaces sont deplaces dans `assets/pics-proxy/`, ils
ne sont pas effaces : `assets/pics/` n'est pas suivi par git (869 Mo), donc
rien ne les rendrait.
"""
import argparse
import json
import os
import shutil
import sys
import urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PICS = os.path.join(RACINE, "assets", "pics")
REBUT = os.path.join(RACINE, "assets", "pics-proxy")
TAILLE_PROXY = (450, 630)


def serveurs():
    """Les fournisseurs d'images declares dans la configuration du jeu."""
    for nom in ("launch.json", "launch.online.json"):
        chemin = os.path.join(RACINE, nom)
        if not os.path.exists(chemin):
            continue
        liste = json.load(open(chemin, encoding="utf-8")).get("image_servers")
        if liste:
            return liste
    return []


def telecharger(gabarit, card_id):
    url = gabarit.replace("{card_id:U}", card_id.upper()).replace("{card_id}", card_id)
    try:
        with urllib.request.urlopen(url, timeout=20) as reponse:
            if reponse.status != 200:
                return None
            return reponse.read()
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pour-de-vrai", action="store_true",
                    help="ecrit vraiment ; sans lui, l'outil ne fait que dire")
    options = ap.parse_args()

    from PIL import Image
    import io as _io

    gabarits = serveurs()
    if not gabarits:
        print("Aucun image_servers dans la configuration.", file=sys.stderr)
        return 1

    proxies = []
    for fichier in sorted(os.listdir(PICS)):
        chemin = os.path.join(PICS, fichier)
        try:
            if Image.open(chemin).size == TAILLE_PROXY:
                proxies.append((os.path.splitext(fichier)[0], chemin))
        except Exception:
            continue

    print("  %d carte(s) en proxy" % len(proxies))
    remplaces, introuvables = 0, []
    for card_id, chemin in proxies:
        donnees = None
        for gabarit in gabarits:
            donnees = telecharger(gabarit, card_id)
            if donnees:
                break
        if not donnees:
            introuvables.append(card_id)
            continue
        # Un serveur qui rend une page d'erreur en 200, ou un scan qui serait
        # lui-meme un proxy, ne doit rien remplacer.
        try:
            taille = Image.open(_io.BytesIO(donnees)).size
        except Exception:
            introuvables.append(card_id)
            continue
        if taille == TAILLE_PROXY or taille[0] < 400:
            introuvables.append(card_id)
            continue

        print("    %-8s proxy -> vrai scan %dx%d (%d Ko)"
              % (card_id, taille[0], taille[1], len(donnees) // 1024))
        if options.pour_de_vrai:
            os.makedirs(REBUT, exist_ok=True)
            shutil.move(chemin, os.path.join(REBUT, os.path.basename(chemin)))
            with open(os.path.join(PICS, card_id + ".jpg"), "wb") as sortie:
                sortie.write(donnees)
        remplaces += 1

    print()
    if options.pour_de_vrai:
        print("  %d remplacee(s), proxies deplaces dans assets/pics-proxy/" % remplaces)
    else:
        print("  %d remplacable(s). Relancer avec --pour-de-vrai pour ecrire." % remplaces)
    if introuvables:
        print("  %d sans scan en ligne, le proxy reste : %s"
              % (len(introuvables), ", ".join(introuvables)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
