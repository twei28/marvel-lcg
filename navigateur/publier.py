#!/usr/bin/env python3
"""Publie navigateur/dist (play.<domaine>). SIMULATION PAR DEFAUT : rien n'est envoye sans --oui.

    python3 navigateur/publier.py              # construit, controle l'equivalence, montre ce qui partirait
    python3 navigateur/publier.py --oui        # envoie vraiment (apres le « deploie » de l'utilisateur)
    options : --sans-construire  --parties N (controle, defaut 20)  --scans <dossier des scans redresses>

Le CONTROLE D'EQUIVALENCE est la porte : N parties jouees par le moteur normal et par celui du navigateur
(essais/equivalence.py). La moindre difference arrete tout, avant tout envoi. Typique d'un changement qui
marche sur le serveur et pas dans le navigateur : du code qui lit des fichiers autrement, appelle Internet
ou lance un fil d'execution.

Cible (variables d'environnement, valeurs par defaut = celles de deploiement/MODE-EMPLOI.md) :
    NARWHAL_HOTE=root@178.105.177.39   NARWHAL_CLE=<deploiement/cle_narwhal>   PLAY_RACINE=/opt/narwhal-play
"""
import os, shutil, subprocess, sys, tempfile
ICI = os.path.dirname(os.path.abspath(__file__)); RACINE = os.path.dirname(ICI)
args = sys.argv[1:]
OUI = "--oui" in args
def option(nom, defaut):
    return args[args.index(nom) + 1] if nom in args and args.index(nom) + 1 < len(args) else defaut
N = option("--parties", "20")
HOTE = os.environ.get("NARWHAL_HOTE", "root@178.105.177.39")
CLE = os.environ.get("NARWHAL_CLE", os.path.join(RACINE, "deploiement", "cle_narwhal"))
DEST = os.environ.get("PLAY_RACINE", "/opt/narwhal-play")

def etape(titre):
    print(f"\n=== {titre}")

def lancer(cmd, **kw):
    print("  $", " ".join(cmd))
    return subprocess.run(cmd, check=True, **kw)

def main():
    print("MODE", "ENVOI REEL" if OUI else "SIMULATION (rien n'est envoye)")
    if "--sans-construire" not in args:
        etape("1. Construction")
        print("  rappel : le plateau n'est pas reconstruit ici (bash ui-app/deployer.sh si ui-app a change)")
        lancer([sys.executable, os.path.join(ICI, "construire.py")])
    etape(f"2. Controle d'equivalence ({N} parties)")
    p = subprocess.run([sys.executable, os.path.join(ICI, "essais", "equivalence.py"), N], capture_output=True, text=True)
    fin = [l for l in p.stdout.splitlines() if "identiques," in l]
    print("  " + (fin[-1] if fin else p.stdout[-300:]))
    if p.returncode != 0 or not fin or " 0 differentes" not in fin[-1]:
        print("  ARRET : le moteur du navigateur ne se comporte pas comme le moteur normal. Rien n'est envoye.")
        sys.exit(1)
    etape("3. Scans redresses")
    print("  un hebergement statique ne peut pas redresser les scans paysage : voir preparer-scans.py")
    scans = option("--scans", "")
    if scans:
        print(f"  envoyes aussi : {scans}")
    etape("4. Envoi" + ("" if OUI else " (simulation : rsync -n)"))
    if not os.path.isfile(CLE):
        sys.exit(f"  cle SSH introuvable : {CLE}")
    tmp = tempfile.mkdtemp(); cle = os.path.join(tmp, "cle"); shutil.copy(CLE, cle); os.chmod(cle, 0o600)
    try:
        ssh = f"ssh -i {cle} -o StrictHostKeyChecking=accept-new"
        cmd = ["rsync", "-az", "--delete", "--itemize-changes", "-e", ssh] + ([] if OUI else ["-n"])
        lancer(cmd + [os.path.join(ICI, "dist") + "/", f"{HOTE}:{DEST}/"])
        if scans:
            lancer(cmd + [scans.rstrip("/") + "/", f"{HOTE}:{DEST}/../narwhal-play-scans/"])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\nTermine." + ("" if OUI else " Rien n'a ete modifie sur le serveur (simulation)."))
    if OUI:
        print("Caddy : voir navigateur/Caddyfile.exemple si le bloc play. n'est pas encore en place.")

if __name__ == "__main__":
    main()
