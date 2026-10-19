#!/usr/bin/env python3
"""Construit catalogue-phases/ (captures/, index.html) depuis manifeste.py."""
import base64, io, json, os, shutil, sys, html
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from manifeste import SECTIONS, ENTREES, ERGO, NON_REALISE

OUT = '/home/oem/Desktop/Marvel LCG/docs/rapports/phase-mechant-sur-la-table/catalogue-phases'
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
shutil.rmtree(OUT + '/captures', ignore_errors=True)
os.makedirs(OUT + '/captures', exist_ok=True)

def jpeg64(path, q=78):
    im = Image.open(path).convert('RGB')
    if im.width > 1280:
        im = im.resize((1280, round(im.height * 1280 / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True, progressive=True)
    return base64.b64encode(b.getvalue()).decode(), im.size

import re
def code(t):
    return re.sub(r'`([^`]+)`', lambda m: '<code>' + html.escape(m.group(1)) + '</code>', t)

def ecran_de(e):
    return e.get('ecran', 'pc')

nums = {}
cartes = {s[0]: [] for s in SECTIONS}
total_bytes = 0
q = 78
for e in ENTREES:
    sec = e['s']
    nums[sec] = nums.get(sec, 0) + 1
    nom = f"{sec}-{e['id']}-{ecran_de(e)}.png"
    src = os.path.join(SRC, e['f'] + '.png')
    if not os.path.exists(src):
        print('MANQUE', src); continue
    Image.open(src).save(os.path.join(OUT, 'captures', nom), 'PNG', optimize=True)
    cartes[sec].append((e, nom))

def build(q):
    parts = []
    size = 0
    for sid, titre, intro in SECTIONS:
        if not cartes.get(sid): continue
        parts.append(f'<section id="s{sid}"><h2>{html.escape(titre)}</h2><p class="intro">{intro}</p><div class="grille">')
        for e, nom in cartes[sid]:
            b64, (w, h) = jpeg64(os.path.join(OUT, 'captures', nom), q)
            size += len(b64)
            ec = ecran_de(e)
            meta = ' · '.join(x for x in [e.get('scenario'), e.get('hero'), f'{w}×{h}' if ec else ''] if x)
            parts.append(f'''<figure class="carte" id="fig-{sid}-{e['id']}" data-ecran="{ec}"><a href="#" class="zoom"><img loading="lazy" width="{w}" height="{h}" alt="{html.escape(e['t'])}" src="data:image/jpeg;base64,{b64}"></a>
<figcaption><span class="badge {ec}">{ {'pc':'PC','tablette':'Tablette','mobile':'Mobile'}.get(ec,ec)}</span><strong>{html.escape(e['t'])}</strong>
<p>{code(e['l'])}</p><p class="decl"><b>Déclencheur :</b> {code(e['d'])}</p><p class="meta">{html.escape(meta)} · <code>captures/{html.escape(nom)}</code></p></figcaption></figure>''')
        parts.append('</div></section>')
    return parts, size

parts, size = build(q)
while size > 11_600_000 and q > 50:
    q -= 4; parts, size = build(q)
print('poids base64', size, 'qualité', q)

idx = {(e['s'], e['id']): e for e, n in [(e, None) for sec in cartes.values() for e, _ in sec]}
def liens(refs):
    out = []
    for sec, i in refs:
        e = idx.get((sec, i))
        if e: out.append(f'<a href="#fig-{sec}-{i}">{html.escape(e["t"])}</a>')
    return ' · '.join(out)
ergo = ''.join(f'<li><strong>{html.escape(t)}</strong> {d}<br><span class="voir">Voir : {liens(r)}</span></li>' for t, d, r in ERGO)
ergo_cartes = ''
for t, d, f in []:
    pass
nonr = ''.join(f'<li><strong>{html.escape(t)}</strong> {d}</li>' for t, d in NON_REALISE)
sommaire = ''.join(f'<li><a href="#s{sid}">{html.escape(titre)}</a> <span class="n">{len(cartes[sid])}</span></li>' for sid, titre, _ in SECTIONS if cartes.get(sid))
tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gabarit.html'), encoding='utf-8').read()
page = tpl.replace('%%SOMMAIRE%%', sommaire).replace('%%SECTIONS%%', '\n'.join(parts)).replace('%%ERGO%%', ergo).replace('%%NONR%%', nonr).replace('%%NB%%', str(sum(len(v) for v in cartes.values())))
open(OUT + '/index.html', 'w', encoding='utf-8').write(page)
print('index.html', os.path.getsize(OUT + '/index.html'), 'octets')
for sid, titre, _ in SECTIONS: print(sid, len(cartes.get(sid, [])))
