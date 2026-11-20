#!/usr/bin/env python3
"""La REGLE D'OR appliquee au verificateur de livraison : un controle qui repond « OK » ne prouve rien tant qu'on ne
l'a pas vu ECHOUER (20/10/2026).

    python3 outils/test_verifier_livraison.py

Pour trois campagnes deja integrees (Mad Titan's Shadow, Web of Deceit, Hunting Season), on reconstitue leur
livraison (`livraison-depuis-le-depot.py`), puis on CASSE une chose a la fois dans une copie et on verifie que
`verifier-livraison-campagne.py` signale PRECISEMENT cette casse (et que la livraison intacte ne la signale pas).
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
MOTEUR = os.path.join(os.path.dirname(ICI), "Fusion", "marvel-lcg-src")
VERIF = os.path.join(ICI, "verifier-livraison-campagne.py")
LIVRAISON = os.path.join(ICI, "livraison-depuis-le-depot.py")


def sh(*cmd):
    return subprocess.run([sys.executable, *cmd], capture_output=True, text=True)


def lire(p):
    with io.open(p, encoding="utf-8", newline="") as f:
        return f.read()


def ecrire(p, t):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)


def verifier(dossier, ref, officiel):
    args = [VERIF, dossier, "--reference", ref] + (["--officiel"] if officiel else [])
    return sh(*args).stdout


def cas():
    """(nom, base, mutation(dossier_integration) -> None, motif attendu dans la sortie)."""
    def remplacer(chemin, ancien, nouveau):
        def f(d):
            p = os.path.join(d, "integration", chemin)
            t = lire(p)
            assert ancien in t, "mutation impossible : %r absent de %s" % (ancien, chemin)
            ecrire(p, t.replace(ancien, nouveau, 1))
        return f

    def supprimer(chemin):
        def f(d):
            os.remove(os.path.join(d, "integration", chemin))
        return f

    def deplacer(src, dst):
        def f(d):
            os.makedirs(os.path.dirname(os.path.join(d, "integration", dst)), exist_ok=True)
            shutil.move(os.path.join(d, "integration", src), os.path.join(d, "integration", dst))
        return f

    def json_modifier(chemin, fonction):
        def f(d):
            import json
            p = os.path.join(d, "integration", chemin)
            j = json.loads(lire(p))
            fonction(j)
            ecrire(p, json.dumps(j, ensure_ascii=False, indent=4) + "\n")
        return f

    def champ(j, cle):
        for s in j["scenarios"]:
            for c in s.get("victoire", []):
                if c["cle"] == cle:
                    return c
        raise AssertionError(cle)

    def carte(j, cid):
        for pack, liste in j.items():
            for c in liste:
                if c.get("card_id") == cid:
                    return c
        raise AssertionError(cid)

    mts = "mts"
    wd = "web_of_deceit"
    hs = "hunting_season"
    return [
        ("dossier de set sans __init__.py", wd, supprimer("src/cards/pack/web_of_deceit/shocker/__init__.py"),
         "dossier de set SANS `__init__.py`"),
        ("niveau CampaignSetup faux sur la face 1A", mts,
         remplacer("src/cards/pack/mts/the_tower_defense/21098a.py", "*CampaignSetup(2)", "*CampaignSetup(3)"),
         "CampaignSetup(3) mais le numero du scenario est 2"),
        ("face 1A qui n'appelle plus la campagne", mts,
         remplacer("src/cards/pack/mts/ebony_maw/21074a.py", "return [*CampaignSetup(1)]", "return []"),
         "n'appelle aucune fonction de campagne"),
        ("cle de carnet mal orthographiee dans la description", mts,
         json_modifier("data/campagnes/mts.json", lambda j: champ(j, "Campaign Pool: Cosmo").update({"cle": "Campaign Pool: Cosmos"})),
         "n'est ECRITE NI LUE"),
        ("valeur de desc numerique au lieu d'une chaine", wd,
         json_modifier("data/cards.web_of_deceit.fragment.json", lambda j: carte(j, "wd006")["desc"].update({"HP": 5})),
         "doit etre une CHAINE"),
        ("appel de fonction inventee", wd,
         remplacer("src/cards/pack/web_of_deceit/shocker/wd006.py", "def GetAbilities", "def Inutile():\n    return InventerUnEffetMagique()\n\n\ndef GetAbilities"),
         "appel `InventerUnEffetMagique(...)`"),
        ("set de rencontre inexistant dans un scenario", wd,
         remplacer("data/scenarios/wd_shocker.json", '"shocker"', '"shocker_fantome"'),
         "le set 'shocker_fantome' n'existe ni"),
        ("script range dans le mauvais dossier", wd,
         deplacer("src/cards/pack/web_of_deceit/shocker/wd005.py", "src/cards/pack/web_of_deceit/bodyguard/wd005.py"),
         "script rangé dans 'bodyguard'"),
        ("cle `custom` retiree d'une carte fan-made", wd,
         json_modifier("data/cards.web_of_deceit.fragment.json", lambda j: carte(j, "wd006").pop("custom")),
         "la cle `custom`"),
        ("detection inexistante", mts,
         json_modifier("data/campagnes/mts.json", lambda j: champ(j, "Campaign Pool: Cosmo").update({"detection": "inventee"})),
         "detection 'inventee' n'existe pas"),
        ("vocabulaire francais interdit", hs,
         lambda d: ecrire(os.path.join(d, "integration", "textes-fr", "hunting_season.fragment.txt"),
                          re.sub(r"(^  'hs[^']*': \")", r"\1étourdi ",
                                 lire(os.path.join(d, "integration", "textes-fr", "hunting_season.fragment.txt")),
                                 count=1, flags=re.M)),
         "vocabulaire interdit"),
        ("carte avec capacite imprimee et script vide", wd,
         remplacer("src/cards/pack/web_of_deceit/shocker/wd009.py", "return [", "return []\n    _ = ["),
         "liste VIDE"),
        ("CardFinder avec l'etoile d'unicite", wd,
         remplacer("src/cards/pack/web_of_deceit/shocker/wd006.py", "def GetAbilities", "X = CardFinder(name=\"* Sandman\")\n\n\ndef GetAbilities"),
         "ne trouve jamais rien"),
        ("scenario qui cite une carte absente", wd,
         json_modifier("data/scenarios/wd_shocker.json", lambda j: j["encounters"].append("wd999")),
         "carte inconnue 'wd999'"),
        ("numero de scenario avec un trou", mts,
         json_modifier("data/campagnes/mts.json", lambda j: j["scenarios"][2].update({"numero": 7})),
         "`numero` doit valoir 1, 2, 3"),
        ("deck requis sans parJoueur", mts,
         json_modifier("data/campagnes/mts.json", lambda j: champ(j, "Campaign Pool: Cosmo").update({"deck": "requis"})),
         "deck: requis exige parJoueur"),
    ]


def main():
    tmp = tempfile.mkdtemp(prefix="test-livraison-")
    ref = os.path.join(tmp, "reference")
    r = sh(VERIF, "--generer-reference", MOTEUR, ref)
    assert r.returncode == 0, r.stderr
    bases = {}
    for pack in ("mts", "web_of_deceit", "hunting_season"):
        d = os.path.join(tmp, "base-" + pack)
        r = sh(LIVRAISON, pack, pack, d, *(["--officiel"] if pack == "mts" else []))
        assert r.returncode == 0, r.stderr
        bases[pack] = d
    echecs = 0
    for nom, base, mutation, motif in cas():
        officiel = base == "mts"
        intact = verifier(bases[base], ref, officiel)
        copie = os.path.join(tmp, "copie")
        if os.path.exists(copie):
            shutil.rmtree(copie)
        shutil.copytree(bases[base], copie)
        try:
            mutation(copie)
        except AssertionError as e:
            print("CAS INVALIDE  %s : %s" % (nom, e))
            echecs += 1
            continue
        casse = verifier(copie, ref, officiel)
        vu_avant = motif in intact
        vu_apres = motif in casse
        if vu_apres and not vu_avant:
            print("ok            %s" % nom)
        else:
            echecs += 1
            print("ECHEC         %s : motif %r %s" % (nom, motif, "deja present sur la livraison intacte" if vu_avant else "NON detecte"))
    shutil.rmtree(tmp, ignore_errors=True)
    print("\n%d echec(s) sur %d cas" % (echecs, len(cas())))
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
