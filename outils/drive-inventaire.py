#!/usr/bin/env python3
"""drive-inventaire.py : releve ce qu'il y a dans les Drives fan-made, SANS compte Google ni cle API.

Pourquoi : le connecteur Drive du chat cache des fichiers (Mantis : 1 carte vue dans « Encounter Cards » au lieu de 6).
La vue publique `embeddedfolderview` d'un dossier partage « a toute personne ayant le lien » liste TOUT (titre, id,
date de derniere modification au jour pres), sans pagination cachee.

Usage :
  python3 outils/drive-inventaire.py                 # releve tous les dossiers de sources-drive.json
  python3 outils/drive-inventaire.py mantis destiny  # seulement ceux dont le nom contient ces mots
Sortie : docs/reference/drive-snapshots/AAAA-MM-JJ.json (+ comparaison avec le releve precedent).
Limites : dates au jour pres (pas de somme de controle) ; un dossier prive n'est pas lisible ; profondeur max 4.
"""
import json, os, re, sys, time, html, datetime, urllib.request
from concurrent.futures import ThreadPoolExecutor

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(RACINE, 'docs', 'reference', 'sources-drive.json')
SNAP = os.path.join(RACINE, 'docs', 'reference', 'drive-snapshots')
PROFONDEUR = 4
ENTREE = re.compile(r'<div class="flip-entry" id="entry-([^"]+)".*?href="([^"]+)".*?<div class="flip-entry-title">(.*?)</div>.*?<div class="flip-entry-last-modified"><div>(.*?)</div>', re.S)

def lire(dossier_id):
    url = f'https://drive.google.com/embeddedfolderview?id={dossier_id}'
    for essai in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode('utf8', 'replace')
        except Exception as e:
            time.sleep(2 + essai * 3)
            err = e
    raise RuntimeError(f'{dossier_id}: {err}')

def explorer(dossier_id, niveau=0):
    page = lire(dossier_id)
    sortie = []
    for ident, lien, titre, date in ENTREE.findall(page):
        est_dossier = '/folders/' in lien
        e = {'id': ident, 'nom': html.unescape(titre).strip(), 'type': 'dossier' if est_dossier else 'fichier', 'date': date.strip()}
        if est_dossier and niveau < PROFONDEUR:
            time.sleep(0.1)
            try:
                e['contenu'] = explorer(ident, niveau + 1)
            except Exception as ex:
                e['erreur'] = str(ex)
        sortie.append(e)
    return sortie

def aplatir(arbre, chemin=''):
    for e in arbre:
        p = f"{chemin}/{e['nom']}"
        yield p, e
        yield from aplatir(e.get('contenu', []), p)

def compter(arbre):
    fichiers = sum(1 for _, e in aplatir(arbre) if e['type'] == 'fichier')
    dossiers = sum(1 for _, e in aplatir(arbre) if e['type'] == 'dossier')
    return fichiers, dossiers

def main():
    filtres = [a.lower() for a in sys.argv[1:]]
    sources = json.load(open(SOURCES, encoding='utf8'))
    os.makedirs(SNAP, exist_ok=True)
    releve = {}
    choisies = [s for s in sources if not filtres or any(f in s['nom'].lower() for f in filtres)]

    def un(s):
        t = time.time()
        try:
            arbre = explorer(s['id'])
        except Exception as ex:
            print(f"ECHEC {s['nom']}: {ex}", flush=True)
            return s['nom'], {'id': s['id'], 'erreur': str(ex)}
        f, d = compter(arbre)
        print(f"{s['nom']}: {f} fichiers, {d} dossiers ({time.time()-t:.0f}s)", flush=True)
        return s['nom'], {'id': s['id'], 'fichiers': f, 'dossiers': d, 'arbre': arbre}

    with ThreadPoolExecutor(max_workers=6) as pool:
        for nom, val in pool.map(un, choisies):
            releve[nom] = val
    jour = datetime.date.today().isoformat()
    sortie = os.path.join(SNAP, f'{jour}.json')
    if filtres and os.path.exists(sortie):  # un releve partiel complete celui du jour au lieu de l'ecraser
        deja = json.load(open(sortie, encoding='utf8'))
        deja.update(releve)
        releve = deja
    json.dump(releve, open(sortie, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('ecrit', os.path.relpath(sortie, RACINE))
    precedents = sorted(x for x in os.listdir(SNAP) if x.endswith('.json') and x != f'{jour}.json')
    if precedents:
        ancien = json.load(open(os.path.join(SNAP, precedents[-1]), encoding='utf8'))
        for nom, cur in releve.items():
            old = ancien.get(nom)
            if not old or 'arbre' not in old or 'arbre' not in cur:
                continue
            a = {p: e['date'] for p, e in aplatir(old['arbre'])}
            b = {p: e['date'] for p, e in aplatir(cur['arbre'])}
            nouveaux = [p for p in b if p not in a]
            changes = [p for p in b if p in a and a[p] != b[p]]
            disparus = [p for p in a if p not in b]
            if nouveaux or changes or disparus:
                print(f'== {nom} : +{len(nouveaux)} nouveaux, ~{len(changes)} modifies, -{len(disparus)} disparus (vs {precedents[-1]})')

if __name__ == '__main__':
    main()
