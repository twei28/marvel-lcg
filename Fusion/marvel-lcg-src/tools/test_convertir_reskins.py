#!/usr/bin/env python3
"""Teste tools/convertir_reskins_art_seul.py sur une COPIE (jamais sur le depot).

    python3 tools/test_convertir_reskins.py

Verifie : l'essai a blanc n'ecrit rien ; la conversion retire les cartes « art
seul » (et elles seules) de cards.json avec un checksum valide, les declare dans
arts_alternatifs.json, copie leur image sans toucher a l'originale ; les
exclusives et les trois ressources doubles restent ; relancer ne change rien.

Depuis la conversion du 17/10/2026, le depot n'a plus de reskin « art seul » :
le test les RECREE dans la copie (un clone de chaque officielle convertie, lue
dans la colonne `converti_art_alternatif_de` du TSV), puis, en premiere partie,
verifie l'ETAT REEL du depot (`verifier_depot`).
"""
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
sys.path.insert(0, str(ICI))
import classer_reskins_tmnt as classeur  # noqa: E402


def lancer(copie, *args):
    r = subprocess.run([sys.executable, str(ICI / "convertir_reskins_art_seul.py"), "--racine", str(copie), *args],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    return r.stdout


def checksum_ok(chemin):
    d = json.loads(chemin.read_text(encoding="utf-8"))
    sans = {k: v for k, v in d.items() if k != "checksum"}
    return hashlib.sha256(json.dumps(sans, sort_keys=True).encode()).hexdigest() == d["checksum"], d


def verifier_depot():
    """Etat reel : chaque carte convertie a disparu de cards.json, son officielle declare un art `tmnt`
    et possede l'image `<officielle>_tmnt.jpg` ; les exclusives et les ressources doubles restent."""
    converties = {}
    with open(RACINE / "tools" / "tmnt_aspects_numerotation.tsv", encoding="utf-8", newline="") as h:
        for r in csv.DictReader(h, delimiter="\t"):
            if (r.get("converti_art_alternatif_de") or "").strip():
                converties[r["card_id"]] = r["converti_art_alternatif_de"].strip()
    assert len(converties) >= 60, f"colonne converti_art_alternatif_de vide ({len(converties)})"
    ok, d = checksum_ok(RACINE / "data" / "cards.json")
    assert ok, "checksum de cards.json invalide"
    cartes = classeur.charger_cartes()
    arts = json.loads((RACINE / "data" / "arts_alternatifs.json").read_text(encoding="utf-8"))["cartes"]
    pics = RACINE / "assets" / "pics"
    for cid, off in converties.items():
        assert cid not in cartes, f"{cid} devrait avoir ete retiree de cards.json"
        assert off in cartes, f"l'officielle {off} de {cid} manque"
        assert "tmnt" in arts.get(off, []), f"{off} ne declare pas d'art alternatif tmnt (ex-{cid})"
        assert (pics / f"{off}_tmnt.jpg").is_file(), f"image {off}_tmnt.jpg absente (ex-{cid})"
    reste = [c for c, _, o, e in classeur.classer() if not e and o not in {"01088", "01089", "01090"}]
    assert not reste, f"reskins « art seul » encore presents : {reste}"
    print(f"OK depot : {len(converties)} cartes converties, art alternatif tmnt + image presents")
    return converties


def injecter_clones(copie, converties):
    """Recree dans la copie un reskin « art seul » (clone de l'officielle) par carte convertie."""
    chemin = copie / "data" / "cards.json"
    brut = json.loads(chemin.read_text(encoding="utf-8"))
    for cid, off in converties.items():
        for cle, v in brut.items():
            if isinstance(v, list):
                src = next((c for c in v if isinstance(c, dict) and c.get("card_id") == off), None)
                if src:
                    clone = dict(src)
                    clone.update(card_id=cid, ability_link=off, custom="Inkwire", set_name="TMNT test")
                    v.append(clone)
                    break
    brut["checksum"] = hashlib.sha256(json.dumps({k: v for k, v in brut.items() if k != "checksum"},
                                                 sort_keys=True).encode()).hexdigest()
    chemin.write_text(json.dumps(brut, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    converties = verifier_depot()
    with tempfile.TemporaryDirectory() as tmp:
        copie = Path(tmp)
        (copie / "data").mkdir()
        (copie / "tools").mkdir()
        (copie / "assets" / "pics").mkdir(parents=True)
        for f in ("cards.json", "arts_alternatifs.json"):
            shutil.copy(RACINE / "data" / f, copie / "data" / f)
        shutil.copy(RACINE / "tools" / "tmnt_aspects_numerotation.tsv", copie / "tools")

        injecter_clones(copie, converties)
        classement = classeur.classer(classeur.charger_cartes(copie / "data" / "cards.json"),
                                      classeur.lire_origines(copie / "tools" / "tmnt_aspects_numerotation.tsv"))
        ressources = {"01088", "01089", "01090"}
        art_seul = [(c, o) for c, _, o, e in classement if not e and o not in ressources]
        exclusives = [c for c, _, o, e in classement if e]
        res = [c for c, _, o, e in classement if o in ressources]
        assert art_seul and exclusives and res, "classement vide : donnees inattendues"
        for cid, _ in art_seul + [(c, "") for c in res]:
            (copie / "assets" / "pics" / f"{cid}.jpg").write_bytes(b"jpg-" + cid.encode())

        avant = (copie / "data" / "cards.json").read_bytes()
        lancer(copie)  # essai a blanc
        assert (copie / "data" / "cards.json").read_bytes() == avant, "l'essai a blanc a ecrit"

        lancer(copie, "--ecrire")
        ok, d = checksum_ok(copie / "data" / "cards.json")
        assert ok, "checksum de cards.json invalide"
        ids = {c["card_id"] for v in d.values() if isinstance(v, list) for c in v if isinstance(c, dict) and "card_id" in c}
        for cid, off in art_seul:
            assert cid not in ids, f"{cid} aurait du etre retiree"
            assert off in ids, f"officielle {off} disparue"
            assert (copie / "assets" / "pics" / f"{off}_tmnt.jpg").read_bytes() == b"jpg-" + cid.encode()
            assert (copie / "assets" / "pics" / f"{cid}.jpg").exists(), "image d'origine deplacee"
        for cid in exclusives + res:
            assert cid in ids, f"{cid} (exclusive ou ressource) ne devait pas etre retiree"
        arts = json.loads((copie / "data" / "arts_alternatifs.json").read_text(encoding="utf-8"))
        assert set(arts["cartes"]) == {o for _, o in art_seul}
        assert all(v == ["tmnt"] for v in arts["cartes"].values())

        apres = (copie / "data" / "cards.json").read_bytes()
        lancer(copie, "--ecrire")
        assert (copie / "data" / "cards.json").read_bytes() == apres, "relancer a modifie cards.json"
        print(f"OK : {len(art_seul)} retirees, {len(exclusives)} exclusives et {len(res)} ressources conservees")


if __name__ == "__main__":
    main()
