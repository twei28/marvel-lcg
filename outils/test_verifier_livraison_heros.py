#!/usr/bin/env python3
"""La REGLE D'OR appliquee au verificateur de livraison de HEROS : un controle qui repond « OK » ne prouve rien
tant qu'on ne l'a pas vu ECHOUER (20/10/2026).

    python3 outils/test_verifier_livraison_heros.py

Pour deux heros deja integres (Lockjaw, maison ; Ant-Man, officiel), on reconstitue leur livraison
(`livraison-heros-depuis-le-depot.py`), puis on CASSE une chose a la fois dans une copie et on verifie que
`verifier-livraison-heros.py` signale PRECISEMENT cette casse (et que la livraison intacte ne la signale pas).
"""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
MOTEUR = os.path.join(os.path.dirname(ICI), "Fusion", "marvel-lcg-src")
VERIF = os.path.join(ICI, "verifier-livraison-heros.py")
LIVRAISON = os.path.join(ICI, "livraison-heros-depuis-le-depot.py")


def sh(*cmd):
    return subprocess.run([sys.executable, *cmd], capture_output=True, text=True)


def lire(p):
    with io.open(p, encoding="utf-8", newline="") as f:
        return f.read()


def ecrire(p, t):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)


def verifier(dossier, ref, officiel):
    return sh(VERIF, dossier, "--reference", ref, *(["--officiel"] if officiel else [])).stdout


def cas(carte_etrangere):
    """(nom, base, mutation(dossier) -> None, motif attendu dans la sortie)."""
    def chemin(d, rel):
        return os.path.join(d, "integration", rel)

    def remplacer(rel, ancien, nouveau):
        def f(d):
            t = lire(chemin(d, rel))
            assert ancien in t, "mutation impossible : %r absent de %s" % (ancien, rel)
            ecrire(chemin(d, rel), t.replace(ancien, nouveau, 1))
        return f

    def supprimer(rel):
        def f(d):
            os.remove(chemin(d, rel))
        return f

    def deplacer(src, dst):
        def f(d):
            os.makedirs(os.path.dirname(chemin(d, dst)), exist_ok=True)
            shutil.move(chemin(d, src), chemin(d, dst))
        return f

    def json_modifier(rel, fonction):
        def f(d):
            j = json.loads(lire(chemin(d, rel)))
            fonction(j)
            ecrire(chemin(d, rel), json.dumps(j, ensure_ascii=False, indent=4) + "\n")
        return f

    def carte(j, cid):
        for c in j["lockjaw"]:
            if c.get("card_id") == cid:
                return c
        raise AssertionError(cid)

    CARTES = "data/cards.lockjaw.fragment.json"
    DECK = "deck/starter/lockjaw.json"
    INFO = "data/sets_info.lockjaw.fragment.json"
    FR = "textes-fr/lockjaw.fragment.txt"

    def retirer_carte(cid):
        def fonction(j):
            j["lockjaw"] = [c for c in j["lockjaw"] if c.get("card_id") != cid]
        return json_modifier(CARTES, fonction)

    def retirer_desc(cid, cle):
        return json_modifier(CARTES, lambda j: carte(j, cid)["desc"].pop(cle))

    def sur_deck(fonction):
        return json_modifier(DECK, fonction)

    def meta(cle, valeur):
        def fonction(j):
            j["metadata"][cle] = valeur
        return sur_deck(fonction)

    return [
        ("face alter ego absente", "lockjaw", retirer_carte("lj001b"), "il manque la face ALTER EGO `lj001b`"),
        ("stat THW absente de la face heros", "lockjaw", retirer_desc("lj001a", "THW"), "desc.THW absente"),
        ("REC absente de l'alter ego", "lockjaw", retirer_desc("lj001b", "REC"), "desc.REC absente"),
        ("nom de l'identite sans etoile", "lockjaw", json_modifier(CARTES, lambda j: carte(j, "lj001a").update(name="Lockjaw")),
         "commence par `* `"),
        ("set_name different sur la face b", "lockjaw", json_modifier(CARTES, lambda j: carte(j, "lj001b").update(set_name="Autre")),
         "pas le meme set_name"),
        ("valeur de desc en nombre", "lockjaw", json_modifier(CARTES, lambda j: carte(j, "lj001a")["desc"].update(HP=14)),
         "doit etre une CHAINE"),
        ("custom absent", "lockjaw", json_modifier(CARTES, lambda j: carte(j, "lj002").pop("custom")), "`custom`"),
        ("prefixe deja pris", "lockjaw", remplacer("tools/prefixes.lockjaw.fragment.json", '"lj"', '"sm"'), "DEJA pris"),
        ("deck de depart supprime", "lockjaw", supprimer(DECK), "aucun deck de depart"),
        ("cle hero_deck absente", "lockjaw", sur_deck(lambda j: j.pop("hero_deck")), "cle absente : hero_deck"),
        ("faces de l'identite dans le mauvais ordre", "lockjaw", sur_deck(lambda j: j.update(hero=["lj001b,lj001a"])),
         "doit etre de type Hero"),
        ("identite inconnue", "lockjaw", sur_deck(lambda j: j.update(hero=["lj099a,lj099b"])), "`hero` cite une carte inconnue"),
        ("carte inconnue dans hero_deck", "lockjaw", sur_deck(lambda j: j["hero_deck"].__setitem__(0, "zz999")),
         "hero_deck : carte inconnue 'zz999'"),
        ("carte signature d'un autre heros dans hero_deck", "lockjaw", sur_deck(lambda j: j["hero_deck"].__setitem__(0, carte_etrangere)),
         "SIGNATURE D'UN AUTRE HEROS"),
        ("hero_deck de 14 cartes", "lockjaw", sur_deck(lambda j: j["hero_deck"].pop()), "`hero_deck` compte 14 cartes"),
        ("quatre exemplaires d'une signature", "lockjaw",
         sur_deck(lambda j: j["hero_deck"].__setitem__(1, j["hero_deck"][0]) or j["hero_deck"].__setitem__(2, j["hero_deck"][0])
                  or j["hero_deck"].__setitem__(3, j["hero_deck"][0])), "exemplaires (limite"),
        ("obligation qui n'en est pas une", "lockjaw", sur_deck(lambda j: j.update(obligations=["lj002"])), "attendu Obligation"),
        ("obligation sans GiveTo", "lockjaw", retirer_desc("lj013", "GiveTo"), "sans desc.GiveTo"),
        ("obligation absente", "lockjaw", sur_deck(lambda j: j.update(obligations=[])), "aucune obligation"),
        ("carte joueur dans le set nemesis", "lockjaw", sur_deck(lambda j: j["nemesis_set"].__setitem__(0, "lj002")), "carte JOUEUR"),
        ("set nemesis de 4 cartes", "lockjaw", sur_deck(lambda j: j["nemesis_set"].pop()), "set nemesis de 4 cartes"),
        ("fichier nemesis incoherent", "lockjaw", json_modifier("data/nemesis/lockjaw_nemesis.json", lambda j: j["encounters"].pop()),
         "differe de `nemesis_set`"),
        ("player_deck invente pour un heros maison", "lockjaw", meta("note", "deck compose pour le portage"),
         "NON VIDE pour un heros maison"),
        ("signature etrangere dans player_deck", "lockjaw", sur_deck(lambda j: j["player_deck"].append(carte_etrangere)),
         "carte SIGNATURE D'UN AUTRE HEROS"),
        ("player_deck de 10 cartes", "lockjaw", sur_deck(lambda j: j.update(player_deck=j["player_deck"][:10])), "player_deck de 10 cartes"),
        ("deckbuilding : cle inconnue", "lockjaw", meta("deckbuilding", {"inconnue": 1}), "deckbuilding : cle inconnue"),
        ("variante dont la base n'existe pas", "lockjaw", sur_deck(lambda j: j["metadata"].update(variante_de="nope", variante_nom="V")),
         "le deck de base 'nope' n'existe pas"),
        ("deck qui prend l'identifiant d'un autre heros", "lockjaw", deplacer(DECK, "deck/starter/spider_man.json"),
         "EXISTE deja dans le jeu pour un autre heros"),
        ("heroes de sets_info cite un deck absent", "lockjaw",
         json_modifier(INFO, lambda j: next(iter(j.values())).update(heroes=["fantome"])), "n'a pas de deck de depart"),
        ("heroes de sets_info vide", "lockjaw", json_modifier(INFO, lambda j: next(iter(j.values())).update(heroes=[])), "`heroes` vide"),
        ("scenarios non vide dans sets_info", "lockjaw", json_modifier(INFO, lambda j: next(iter(j.values())).update(scenarios=["x"])),
         "`scenarios` doit etre []"),
        ("un scenario dans une livraison de heros", "lockjaw",
         lambda d: (os.makedirs(chemin(d, "data/scenarios")), ecrire(chemin(d, "data/scenarios/x.json"), "{}")),
         "ne contient ni scenario"),
        ("script d'identite supprime", "lockjaw", supprimer("src/cards/pack/lockjaw/lockjaw/lj001a.py"), "n'a AUCUN script"),
        ("script range dans le mauvais dossier", "lockjaw",
         deplacer("src/cards/pack/lockjaw/lockjaw/lj002.py", "src/cards/pack/lockjaw/mauvais/lj002.py"), "le script est MUET"),
        ("fonction inventee dans un script", "lockjaw",
         remplacer("src/cards/pack/lockjaw/lockjaw/lj004.py", "def GetAbilities", "x = AbilityFactory.AppelImaginaire()\n\n\ndef GetAbilities"),
         "AppelImaginaire"),
        ("texte francais manquant", "lockjaw", lambda d: ecrire(chemin(d, FR), "\n".join(
            l for l in lire(chemin(d, FR)).split("\n") if not l.lstrip().startswith("'lj003'"))), "pas de texte francais pour lj003"),
        ("vocabulaire francais interdit", "lockjaw", remplacer(FR, "Mise en place", "Robustesse"), "vocabulaire interdit"),
        ("biographie absente", "lockjaw", supprimer("public/js/prepare/heros-info.fragment.js"), "pas de biographie"),
        ("biographie indexee par le nom", "lockjaw", remplacer("public/js/prepare/heros-info.fragment.js", '"lj001a"', '"lockjaw"'),
         "FACE HEROS, jamais par le nom"),
        ("biographie sans version anglaise", "lockjaw", remplacer("public/js/prepare/heros-info.fragment.js", "bioEn:", "autre:"),
         "`bioEn` absent"),
        ("replique indexee par un id qui n'est pas un deck", "lockjaw",
         remplacer("public/js/prepare/repliques-heros.fragment.js", "lockjaw:", "lockjaw_x:"), "n'est pas l'identifiant d'un deck livre"),
        ("MANIFESTE absent", "lockjaw", lambda d: os.remove(os.path.join(d, "MANIFESTE.md")), "fichier de suivi absent de la livraison"),
        # --- un heros officiel a trois formes
        ("Ant-Man : forme geante sans stats", "ant", json_modifier("data/cards.ant.fragment.json",
         lambda j: [c["desc"].pop("DEF") for c in j["ant"] if c.get("card_id") == "12001c"]), "desc.DEF absente"),
        ("Ant-Man : obligation vers un autre alter ego", "ant", json_modifier("data/cards.ant.fragment.json",
         lambda j: [c["desc"].update(GiveTo="Autre") for c in j["ant"] if c.get("type") == "Obligation"]), "GiveTo='Autre'"),
        ("Ant-Man : forme de plus inconnue dans hero", "ant", json_modifier("deck/starter/ant_man.json",
         lambda j: j.update(hero=["12001a,12001b,12001z"])), "`hero` cite une carte inconnue : 12001z"),
    ]


def main():
    tmp = tempfile.mkdtemp(prefix="test-livraison-heros-")
    ref = os.path.join(tmp, "reference")
    os.makedirs(ref)
    r = sh(VERIF, "--generer-reference", MOTEUR, ref)
    assert r.returncode == 0, r.stderr
    signature = json.loads(lire(os.path.join(ref, "cartes-signature.json")))
    etrangere = next(cid for cid, st in sorted(signature.items()) if st == "Spider-Man")
    bases = {}
    for pack, deck, officiel in (("lockjaw", "lockjaw", False), ("ant", "ant_man", True)):
        d = os.path.join(tmp, "base-" + pack)
        r = sh(LIVRAISON, pack, deck, d, *(["--officiel"] if officiel else []))
        assert r.returncode == 0, r.stderr
        bases[pack] = d
    echecs, liste = 0, cas(etrangere)
    for nom, base, mutation, motif in liste:
        officiel = base == "ant"
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
        vu_avant, vu_apres = motif in intact, motif in casse
        if vu_apres and not vu_avant:
            print("ok            %s" % nom)
        else:
            echecs += 1
            print("ECHEC         %s : motif %r %s" % (nom, motif, "deja present sur la livraison intacte" if vu_avant else "NON detecte"))
    shutil.rmtree(tmp, ignore_errors=True)
    print("\n%d echec(s) sur %d cas" % (echecs, len(liste)))
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
