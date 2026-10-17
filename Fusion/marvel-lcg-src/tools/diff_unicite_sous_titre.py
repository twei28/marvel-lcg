# Liste les paires de cartes uniques COTE JOUEUR que la regle « unicite par sous-titre » refuse en plus de l'ancien
# jugement du moteur (titre commun ET meme sous-titre). Replique de `correspondent` (deck-builder) et de
# `CanCoexistWith` (moteur), restreinte aux paires dont une carte au moins est TMNT ; identite contre identite exclue. Voir RECETTES-MOTEUR.md §12. Usage : python3 tools/diff_unicite_sous_titre.py
import json,itertools,re
import os
A=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','arts_alternatifs.json'),encoding='utf-8'))['series']['tmnt']
d=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','cards.json'),encoding='utf-8'))
cards=[]
for k,v in d.items():
    for c in v:
        if isinstance(c,dict) and 'card_id' in c: c['_pack']=k; cards.append(c)
def nm(c): return re.sub(r'^\*\s*','',c.get('name','')).strip()
def uniq(c): return c.get('name','').startswith('*')
ident={}
for c in cards:
    if c.get('type') in('Hero','AlterEgo') and c['card_id'][-1] in 'ab':
        ident.setdefault(c['card_id'][:-1],[]).append(c)
descs=[]
PT={'Ally','Support','Upgrade','Event','Resource'}
for k,fs in ident.items():
    if not any(uniq(f) for f in fs): continue
    heroes={nm(f) for f in fs if f['type']=='Hero'}
    alter=''
    for f in fs:
        if f['type']=='AlterEgo': alter=nm(f)
    sub_old=alter if alter not in heroes else ''
    descs.append(dict(id=k,kind='id',titles=heroes,sub=sub_old,alt=alter,nom=nm(fs[0]),pack=fs[0]['_pack'],set=fs[0].get('set_name')))
for c in cards:
    if c.get('type') in('Hero','AlterEgo'): continue
    if uniq(c) and c['type'] in PT:
        descs.append(dict(id=c['card_id'],kind='card',titles={nm(c)},sub=c.get('subtitle','') or '',alt='',nom=nm(c),type=c['type'],set=c.get('set_name'),pack=c['_pack']))
def tmnt(x):
    return x['pack'] in A['heros_ids'] or x['set'] in A['sets_exclusifs'] or (x['set'] or '').startswith('TMNT')
def old(a,b):
    return bool(a['titles']&b['titles']) and a['sub']==b['sub']
def corr(a,b):
    for ta in a['titles']:
        for tb in b['titles']:
            A=dict(t=ta,s=a['sub'] if a['kind']=='card' else '',alt=a['alt'])
            B=dict(t=tb,s=b['sub'] if b['kind']=='card' else '',alt=b['alt'])
            if A['t']==B['t'] and not A['s'] and not B['s'] and not A['alt'] and not B['alt']: return True
            au=lambda x:[v for v in (x['t'],x['s'],x['alt']) if v]
            if any(v in au(B) for v in (A['s'],A['alt']) if v) or any(v in au(A) for v in (B['s'],B['alt']) if v): return True
    return False
res=[]
for a,b in itertools.combinations(descs,2):
    if a['id']==b['id']: continue
    if a['kind']=='id' and b['kind']=='id': continue
    if not (tmnt(a) or tmnt(b)): continue
    o=old(a,b); c=corr(a,b)
    if c and not o: res.append((a,b))
    elif o and not c: print("OLD-only", a['id'],b['id'],a['nom'],a['sub'],b['sub'])
for a,b in res: print(a['id'],a['nom'],'|',a['sub'] or a['alt'],'<>',b['id'],b['nom'],'|',b['sub'] or b['alt'])
print(len(res),len(descs))
