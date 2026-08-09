#!/bin/bash
# Teste un fichier factory requoté isolément : le substitue dans une copie boot,
# mesure les régressions cartes vs baseline. Args: <bootdir> <relpath.py> <port>
BOOTDIR="$1"; REL="$2"; PORT="$3"
SRC="$HOME/marvel-work/fusion/marvel-lcg-src/src/$REL"
PY="$HOME/marvel-work/python/bin/python3.10"
REPORT="/tmp/factory_$(basename $BOOTDIR)_$PORT.json"
# substituer le fichier requoté (les autres restent sur l'état vérifié du boot)
$PY -c "import py_compile, os; py_compile.compile('$SRC', cfile=os.path.join('$HOME/marvel-work/$BOOTDIR', '${REL%.py}.pyc'), doraise=True)" || { echo "COMPILE FAIL $REL"; exit 1; }
STDOUT="/tmp/tof_${BOOTDIR}_${PORT}.log"
RELEASE=1 timeout 400 $PY "$HOME/marvel-work/tools/test_cards.py" "$HOME/marvel-work/$BOOTDIR" "$PORT" "$REPORT" >/dev/null 2>&1
$PY -c "
import json
try:
    r = json.load(open('$REPORT')); base = json.load(open('/tmp/cards_report_original.json'))
    nf = sorted(set(r['failures']) - set(base['failures']))
    print('$REL : %d ok / %d échecs | régressions: %d' % (r['ok'], r['err'], len(nf)))
    for f in nf[:8]: print('   ', f, '->', r['failures'][f][:60])
except Exception as e:
    print('$REL : erreur test ->', e)
    import subprocess
"
# CARDS_STDOUT copie pour debug si init a planté
cp /tmp/cards_stdout.log "$STDOUT" 2>/dev/null || true
