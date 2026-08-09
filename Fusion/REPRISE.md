# REPRISE — reconstruction Marvel LCG, étape 4 (10 fichiers restants)

Document à lire après un `/clear` pour reprendre sans rien reperdre.
Tout l'environnement est sous `~/marvel-work/` (persistant, hors `/tmp`).

## État au 26/07/2026
18 fichiers moteur reconstruits et vérifiés (0 régression). Il reste **10
fichiers défectueux** (reconstructions lourdes), listés dans
`~/marvel-work/fusion/marvel-lcg-src/defectueux.json` :

```
game/ability/factory/ability_factory.py   (45l — corps de classe ~50 méthodes perdues)
game/ability/factory/environment.py       (84l — GiveKeywordToInPlayWhenApplyThis à 3 branches d'appel)
game/card/card_finder/checker.py          (35l — fonctions Check/Checks énormes, décorées @Tracker.count_calls)
game/card/card_finder/finder.py           (198l — corps de classe 479 vs 153 instr.; __and__/__or__/__repr__ déjà corrigés, reste le corps)
game/selector/factory.py                  (254l — 7 UNKNOWN)
game/ability/cost_func.py                  (690l — 3 UNKNOWN, le plus gros)
engine/lib/json.py                         (176l — ConvertDictToDataclass: if/elif à démêler + try/except + 2 with)
engine/log/log.py                          (245l — 13 marqueurs)
engine/network/web_server.py               (261l — 28 marqueurs)
cards/database.py                          (265l — 18 marqueurs)
```

## Environnement (déjà en place, ne pas recréer)
- `~/marvel-work/python/bin/python3.10` — Python 3.10.13 (OBLIGATOIRE)
- `~/marvel-work/boot/` — jeu bootable, bytecode d'ORIGINE = référence, NE PAS MODIFIER
- `~/marvel-work/boot_sub/` — banc d'essai (18 réparés déjà substitués + 10 défectueux sur pyc original)
- `~/marvel-work/fusion/marvel-lcg-src/` — le dépôt fusionné livrable (src/ = sources corrigées, defectueux.json, launcher.py)
- `~/marvel-work/tools/` — scripts de test et de réparation
- `~/marvel-work/state/` — références sauvegardées : `cards_report_original.json` (baseline 3444 ok/7 échecs), `repares.json` (liste des 18 réparés)

## Boucle de travail par fichier (méthode éprouvée, NON négociable)
1. Lire les marqueurs : `grep -n "UNKNOWN\|RECOVER_TODO" src/<fichier>.py`
2. Désassembler le pyc d'origine pour la vérité du flux :
   ```python
   ~/marvel-work/python/bin/python3.10 -c "
   import dis,marshal,os
   def find(c,n):
    for k in c.co_consts:
     if hasattr(k,'co_name'):
      if k.co_name==n: return k
      r=find(k,n)
      if r: return r
   m=marshal.loads(open(os.path.expanduser('~/marvel-work/boot/<fichier>.pyc'),'rb').read()[16:])
   dis.dis(find(m,'<methode>'))"
   ```
   Comparer méthode par méthode orig vs version ChatGPT (comparer le nombre
   d'instructions pour repérer les divergences).
3. Corriger dans `~/marvel-work/fusion/marvel-lcg-src/src/<fichier>.py`.
   Reposer les guillemets d'annotations : `python3.10 ~/marvel-work/tools/quote_forward_refs.py src/<fichier>.py`
4. `ast.parse` puis substituer dans boot_sub et VÉRIFIER PAR EXÉCUTION :
   - cartes : `bash ~/marvel-work/tools/test_one_factory.sh boot_sub <chemin>.py <port>`
     (compile la version src, la substitue, lance test_cards, compte les régressions vs baseline)
   - partie : port rotatif dans boot_sub/launch.json puis
     `RELEASE=1 python3.10 ~/marvel-work/tools/test_newgame.py ~/marvel-work/boot_sub`
     (chercher "PLAYERS: 1" = OK)
   Les DEUX à 0 régression, sinon le fichier n'est pas réparé.
5. Quand OK : retirer de defectueux.json, supprimer son pyc de originals_pyc/,
   régénérer QUALITE-V2.csv, re-zipper (voir plus bas), recopier dans le
   dossier projet Windows `Fusion/`.

## Pièges déjà payés (ne pas refaire)
- « vérifié cartes » ≠ « vérifié gameplay » : random/scene/file-manager passaient
  les cartes mais cassaient la création de partie. Toujours les DEUX tests.
- Corriger le seul marqueur ne suffit pas : finder avait 3 bugs voisins non
  marqués. Comparer TOUTES les méthodes au désassemblage.
- Port 2345 en TIME_WAIT ~60 s entre deux boots → utiliser un port rotatif
  (les scripts le gèrent via server_addresses dans launch.json).
- Le crash handler du jeu masque l'exception primaire (lire au-dessus de
  « During handling of the above exception »).
- Ne jamais toucher `~/marvel-work/boot/` (référence de comparaison).

## Re-zip du livrable
```bash
cd ~/marvel-work/fusion && ~/marvel-work/python/bin/python3.10 -c "
import zipfile,os
root='marvel-lcg-src'; skip={'.game','__pycache__'}
z=zipfile.ZipFile('../marvel-lcg-src-fusion.zip','w',zipfile.ZIP_DEFLATED)
for dp,dirs,files in os.walk(root):
 dirs[:]=[d for d in dirs if d not in skip]
 for f in files:
  if f.endswith('.pyc') and '__pycache__' in dp: continue
  p=os.path.join(dp,f); z.write(p,os.path.relpath(p,root))
z.close(); print('ok')"
cp ~/marvel-work/marvel-lcg-src-fusion.zip "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Fusion/"
```

## Ordre de reconstruction suggéré (du plus sûr au plus risqué)
1. `checker.py` puis `finder.py` (cœur du filtrage de cartes ; se valident bien via test_cards)
2. `environment.py`, `selector/factory.py`, `ability_factory.py` (factory ; test_cards + test_newgame)
3. `json.py`, `log.py`, `web_server.py`, `cards/database.py`, `cost_func.py`
   (périphériques/gros ; certains touchent du gameplay non couvert par mes tests
   → prudence maximale sur les and/or inversés et les branches perdues)
