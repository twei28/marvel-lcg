import random, json, itertools
from collections import Counter, defaultdict
import pvp_sim as p

HEROES = {  # stats imprimees reelles (data/cards.json, set core)
 "SpiderMan": dict(hp=10, atk=2, thw=1, df=3),
 "CapMarvel": dict(hp=12, atk=2, thw=2, df=1),
 "SheHulk":   dict(hp=15, atk=3, thw=1, df=2),
 "IronMan":   dict(hp=9,  atk=1, thw=2, df=1),
 "BlackPanth":dict(hp=11, atk=2, thw=2, df=2),
}
# bonus moyen de cartes par tour : (atk_rnd, thw_rnd, def_rnd, allies atk, allies thw, p_attack)
ASPECT = {
 "Aggression": dict(ar=3, tr=0, dr=0, aa=0, at=0, pa=0.85),
 "Justice":    dict(ar=1, tr=3, dr=1, aa=0, at=1, pa=0.20),
 "Protection": dict(ar=1, tr=1, dr=2, aa=0, at=0, pa=0.35),
 "Leadership": dict(ar=1, tr=1, dr=1, aa=2, at=1, pa=0.50),
}
def build():
    out = {}
    for h, s in HEROES.items():
        for a, b in ASPECT.items():
            out[f"{h}/{a[:4]}"] = dict(hp=s["hp"], atk=s["atk"], ar=b["ar"], thw=s["thw"], tr=b["tr"],
                                       df=s["df"], dr=b["dr"], heal=3, pa=b["pa"], aa=b["aa"], at=b["at"])
    return out

def run(P, n=400):
    p.ARCH.clear(); p.ARCH.update(build())
    keys = list(p.ARCH)
    wins = Counter(); games = Counter(); kinds = Counter(); rounds = []; firstw = 0; tot = 0
    for a, b in itertools.combinations(keys, 2):
        for k in range(n):
            f = k % 2
            win, kind, r = p.play(a, b, f, P)
            if win == -1: continue
            who = (a, b)[win]; wins[who] += 1; games[a] += 1; games[b] += 1
            kinds[kind] += 1; rounds.append(r); tot += 1; firstw += (win == f)
    return keys, wins, games, kinds, rounds, firstw / tot

def report(title, P):
    keys, wins, games, kinds, rounds, fw = run(P)
    print(f"=== {title} | fins {dict(kinds)} | rounds {sum(rounds)/len(rounds):.1f} | 1er joueur {fw*100:.0f}% ===")
    byasp = defaultdict(list); byhero = defaultdict(list)
    for k in keys:
        r = wins[k] / games[k]
        h, a = k.split("/"); byasp[a].append(r); byhero[h].append(r)
    print("  par aspect :", {a: f"{sum(v)/len(v)*100:.0f}%" for a, v in byasp.items()})
    print("  par héros  :", {h: f"{sum(v)/len(v)*100:.0f}%" for h, v in byhero.items()})
    rs = sorted(keys, key=lambda k: -wins[k] / games[k])
    print("  top 3 :", [(k, f"{wins[k]/games[k]*100:.0f}%") for k in rs[:3]], " bas 3 :", [(k, f"{wins[k]/games[k]*100:.0f}%") for k in rs[-3:]])

if __name__ == "__main__":
    random.seed(3)
    report("BASE (cap 6, 10 VP)", p.BASE)
    report("cap 8, 15 VP", {**p.BASE, "cap": 8, "vp": 15})
    report("2 objectifs", {**p.BASE, "nobj": 2})
