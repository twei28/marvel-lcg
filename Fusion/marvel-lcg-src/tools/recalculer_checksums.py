"""Recalcule les checksums de data/*.json AVEC LE MOTEUR.

Le moteur refuse en silence un fichier dont le checksum ne correspond plus
(`CardsDB.checksum_ok`). Le calcul est celui de `Types.DictChecksum`, sur le
dictionnaire PRIVE de sa cle `checksum` — c'est exactement ce que fait
`Json.LoadInternal` a la lecture. Le recalculer a la main, hors moteur, serait
un appel plausible : on appelle donc la vraie fonction.

Usage : python3.10 tools/recalculer_checksums.py <game_dir absolu> <fichier...>
"""
import io, json, os, sys

os.environ.setdefault("RELEASE", "1")
game_dir = os.path.abspath(sys.argv[1])
fichiers = sys.argv[2:]
os.chdir(game_dir); sys.path.insert(0, game_dir)
sys.argv = [sys.argv[0], "-config_files", "launch.json", "-device", "key"]

from core.utility.types import Types

for nom in fichiers:
    t = io.open(nom, encoding="utf-8", newline="").read()
    obj = json.loads(t)
    ancien = obj.pop("checksum", None)
    nouveau = Types.DictChecksum(obj)
    if ancien == nouveau:
        print(f"{nom} : inchange")
        continue
    assert ancien and f'"{ancien}"' in t, f"checksum introuvable dans {nom}"
    io.open(nom, "w", encoding="utf-8", newline="").write(t.replace(f'"{ancien}"', f'"{nouveau}"', 1))
    print(f"{nom} : {ancien[:12]}... -> {nouveau[:12]}...")
