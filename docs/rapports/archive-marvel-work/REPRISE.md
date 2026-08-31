> ⚠️ **DOCUMENT HISTORIQUE, ARCHIVÉ LE 31/08/2026.** Il décrit l'époque (juillet-début août 2026)
> où la copie vivante du jeu était `~/marvel-work/fusion/marvel-lcg-src`. Ce n'est plus vrai :
> la copie vivante est `Fusion/marvel-lcg-src` dans ce dépôt (voir GUIDE-CREATION-CONTENU.md §1).
> Aucun chemin cité ici ne fait foi.

# REPRISE — reconstruction Marvel LCG : TERMINÉE (0 fichier restant)

Document à lire après un `/clear` pour reprendre sans rien reperdre.
Tout l'environnement est sous `~/marvel-work/` (persistant, hors `/tmp`).

## État au 27/07/2026 — RECONSTRUCTION COMPLÈTE
Les 28 fichiers défectueux ont tous été reconstruits et vérifiés :
- bytecode 100% identique à l'original pour chacun (compare_bytecode.py → IDENTIQUE)
- 0 régression cartes (3444 ok / 7 échecs préexistants) et création de partie OK
  (PLAYERS: 1), avec TOUTES les réparations substituées ensemble dans boot_sub
- `defectueux.json` est vide, `originals_pyc/` ne contient plus aucun pyc
- livrable re-zippé (4979 fichiers) et copié dans le dossier Windows `Fusion/`

Il ne reste AUCUN fichier à réparer. Le source complet du jeu est reconstruit.
Prochaine étape possible (sur demande) : nettoyage du launcher (la substitution
originals_pyc est devenue inutile), ou ajout de contenu.

## Correctifs de bugs du jeu original (27/07/2026)
Les 7 échecs de cartes préexistants (présents aussi avec le bytecode original)
sont corrigés — le test cartes passe désormais à **3451 ok / 0 échec** :
- `game/ability/factory/environment.py` : import manquant de `Leader`
  (NameError sur la carte 56200b via 'EnemyLeader').
- `game/ability/factory/do_attack.py` / `UnitCannotDefend` : l'assert rejetait
  'AttachedIdentity'/'AttachedAlly' et les types de cartes ('Character', Unit2,
  Ally) → cartes 32150, 32055, 28030, 27152, 55061, 55062. Au passage,
  restauration d'un morceau perdu par la récupération ChatGPT (check_attacker2 +
  append de PlayersCannotTriggerAbility(label='defense'), présent dans le
  bytecode original). Ces 2 fichiers divergent donc désormais VOLONTAIREMENT du
  bytecode original (marqués `corrige_bugs_originaux` dans QUALITE-V2.csv, et
  commentaires `CORRECTIF` dans le code).

## Campagne de refidélisation (27/07/2026) — TERMINÉE ✅
Objectif atteint : **CHAQUE fichier du jeu est bytecode-identique à l'original**
(compare_bytecode.py → IDENTIQUE), à l'exception des 2 correctifs VOLONTAIRES
(`game/ability/factory/environment.py`, `game/ability/factory/do_attack.py`).
`state/survivants.json` est vide (0 restant sur les 297 divergents de départ).
Validation finale : cartes **3451 ok / 0 échec**, création de partie OK
(**PLAYERS: 1**) avec TOUS les fichiers refidélisés substitués dans boot_sub.
Livrable re-zippé (4979 fichiers) et copié dans `Fusion/`.

Vrais bugs de la récupération ChatGPT corrigés pendant la campagne (extraits) :
check_pay ne payait jamais les coûts, Render inexécutable, boucle « Simultaneous
Overkill » ne bouclait pas (can_health), RemoveThreatInternal ne retirait jamais
la menace (scheme.py), ClassCard.Play retournait toujours False sans OnAfterPlay,
AfterEffectResolved/AfterCheck jamais exécutés (effect_invoke), Eliminate tronqué
(player.py), SetGameOver tronqué, les limites (restricted/team/ally/side-scheme)
ne re-bouclaient pas, conditions at_least toujours vraies (counter/token),
find_new_version ne retournait rien, etc.

Motifs de reconstruction documentés (répertoire complet pour référence future) :
try/except/finally et with perdus (RECOVER_TODO), or/and-dup pycdc (bloc dupliqué
après ifs imbriqués → `if A or B:`), ternaires ↔ if/else (1 vs 2 STOREs),
listcomps imbriquées aplaties, chaînes de comparaison `a <= b < c` (DUP_TOP/
ROT_THREE), swaps `a, b = b, a`, `assert False, msg` vs raise AssertionError,
booléens multi-lignes (JIFOP préservé si lignes différentes : peephole 3.10
n'optimise JIFOP→PJIF que si même ligne — reproduire le layout multi-lignes,
p.ex. `((\n` double-paren pour les lambdas), returns explicites par branche
(duplication d'exits sans lineno), while True + if not X: break, while perdu
(test dupliqué par rotation, backward conditional jump), références mortes pour
closures (`if False: def dead(): return this, effect` ; annotation locale
`deck: Deck = ...`), imports fusionnés/séparés, `f(*tuple([a,*b]))` → `f(a,*b)`,
gros appels >30 kwargs → CALL_FUNCTION_EX, `elif True:` pour else mort.

Outils créés dans `~/marvel-work/tools/` :
- `fix_annotations.py` / `mass_fix_annotations.py` : restaure les annotations
  perdues depuis le pyc original (3441 fichiers réparés automatiquement).
- `fix_structural.py` : candidats AST validés par compile+compare (assert,
  augassign, dépaquetage, ternaires, kwargs `**{'k':v,**kw}`→`k=v,**kw`,
  suppression de doublons, éclatement de listes mono-ligne). +139 fichiers.
- `show_divergences.py` : diff + dis original par objet, pour le travail manuel.

Acquis de méthode pour les 315 restants (travail manuel) :
- Fusion de constantes : si tout est sur UNE ligne source, les lambdas
  identiques fusionnent en une seule constante → reformater en multi-lignes
  suffit souvent (cas game/rule/statistics.py, devenu identique ainsi).
- pycdc DUPLIQUE des blocs de branches (cas BroadcastMessage dans
  game/event/manager.py : 914 instr. au lieu de 660, reconstruit à la main).
- Les gros restants sont dans game/ : operate/filter.py,
  ability/factory/for_choice.py, message/sender/sender_card.py,
  player/action/player_action.py, card/card.py, card/face/card_face.py...

## Environnement (déjà en place, ne pas recréer)
- `~/marvel-work/python/bin/python3.10` — Python 3.10.13 (OBLIGATOIRE)
- `~/marvel-work/boot/` — jeu bootable, bytecode d'ORIGINE = référence, NE PAS MODIFIER
- `~/marvel-work/boot_sub/` — banc d'essai (18 réparés déjà substitués + 10 défectueux sur pyc original)
- `~/marvel-work/fusion/marvel-lcg-src/` — le dépôt fusionné livrable (src/ = sources corrigées, defectueux.json, launcher.py)
- `~/marvel-work/tools/` — scripts de test et de réparation
- `~/marvel-work/state/` — références sauvegardées : `cards_report_original.json` (baseline 3444 ok/7 échecs), `repares.json` (liste des 18 réparés)

## Vérification bytecode (méthode qui a validé checker.py et finder.py)
Après réécriture du source, compiler avec python3.10 et comparer TOUS les
objets code (module + fonctions + comprehensions imbriquées) contre le pyc
d'origine, instruction par instruction (ignorer EXTENDED_ARG et les cibles de
saut, comparer opnames + argval). Objectif : « IDENTIQUE » avant même de
lancer les tests. Pièges de fidélité rencontrés : `assert not x` vs `raise`,
`assert False` (LOAD_ASSERTION_ERROR) vs `raise AssertionError` (LOAD_GLOBAL),
`!= None` vs `is not None`, annotations chaîne vs réelles (ex. `'str|None'`
vs `str | None`, `Type[TF]` réel vs `'TF'` chaîne), `if A or B` aplati par
ChatGPT en ifs imbriqués faux, `else: return []` perdu dans une boucle,
kwargs `CALL_FUNCTION_KW`, `break` = POP_TOP+JUMP dans le désassemblage.

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
   Vérifier le bytecode : `python3.10 ~/marvel-work/tools/compare_bytecode.py src/<fichier>.py ~/marvel-work/boot/<fichier>.pyc` (viser IDENTIQUE)
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
3. `json.py`, `log.py`, `web_server.py`, `   (périphériques/gros ; certains touchent du gameplay non couvert par mes tests
   → prudence maximale sur les and/or inversés et les branches perdues)
