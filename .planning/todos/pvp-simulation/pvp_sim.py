import random, itertools, sys
from collections import Counter

ARCH = {
 # hp, atk, atk_rnd, thw, thw_rnd, def, def_rnd, heal, p_attack, ally_atk, ally_thw
 "Aggression": dict(hp=11, atk=3, ar=3, thw=1, tr=1, df=1, dr=1, heal=4, pa=0.85, aa=0, at=0),
 "Justice":    dict(hp=10, atk=2, ar=2, thw=3, tr=3, df=1, dr=2, heal=4, pa=0.20, aa=0, at=1),
 "Protection": dict(hp=13, atk=2, ar=1, thw=2, tr=1, df=3, dr=3, heal=4, pa=0.35, aa=0, at=0),
 "Leadership": dict(hp=10, atk=1, ar=1, thw=1, tr=1, df=1, dr=1, heal=4, pa=0.50, aa=2, at=1),
}

def play(a, b, first, P):
    names = [a, b]
    S = [dict(ARCH[n]) for n in names]
    hp = [s["hp"] for s in S]
    alter = [False, False]
    obj = [0] * P["nobj"]          # >0 : joueur 0, <0 : joueur 1
    vp = [0, 0]
    turns = [0, 0]
    order = [first, 1 - first]
    for rnd in range(1, P["maxr"] + 1):
        for me in order:
            op = 1 - me
            s = S[me]; turns[me] += 1
            allies = min(turns[me] // 2, 3)
            # decision de forme
            low = hp[me] <= 0.45 * s["hp"]
            alter[me] = low and hp[me] < s["hp"]
            if alter[me]:
                hp[me] = min(s["hp"], hp[me] + s["heal"])
                continue
            can_hit = not alter[op]
            A = s["atk"] + random.randint(0, s["ar"]) + (s["aa"] * allies)
            T = s["thw"] + random.randint(0, s["tr"]) + (s["at"] * allies)
            if alter[op]:
                T += P["alter_bonus"]
            attack = False
            if can_hit:
                if A >= hp[op]:
                    attack = True
                elif vp[op] >= P["vp"] - 3:
                    attack = False
                else:
                    attack = random.random() < s["pa"]
            if attack:
                d = S[op]
                dmg = A
                if not alter[op]:
                    dmg = max(0, A - (d["df"] + random.randint(0, d["dr"])) * P["def_k"])
                hp[op] -= dmg
                if hp[op] <= 0:
                    return me, "KO", rnd
            else:
                # place T de controle sur les objectifs, vers mon signe
                sign = 1 if me == 0 else -1
                rest = T
                while rest > 0:
                    cands = [i for i in range(len(obj)) if obj[i] * sign < P["cap"]]
                    if not cands:
                        break
                    # la plus proche de la capture, sans la deja prise
                    i = max(cands, key=lambda k: obj[k] * sign)
                    put = min(rest, P["cap"] - obj[i] * sign)
                    obj[i] += sign * put
                    rest -= put
        # fin de round : points de domination
        for i in range(len(obj)):
            if obj[i] >= P["cap"]: vp[0] += 1
            elif obj[i] <= -P["cap"]: vp[1] += 1
        if vp[0] >= P["vp"] or vp[1] >= P["vp"]:
            if vp[0] == vp[1]: return first, "VP", rnd
            return (0 if vp[0] > vp[1] else 1), "VP", rnd
    return -1, "NUL", P["maxr"]

def matrix(P, n=3000):
    keys = list(ARCH)
    print(f"{'':12}" + "".join(f"{k[:6]:>8}" for k in keys) + "   (taux de victoire de la ligne, 1er joueur alterné)")
    tot_first = 0; tot = 0; kinds = Counter(); rounds = []
    for a in keys:
        row = []
        for b in keys:
            w = 0; g = 0
            for k in range(n):
                f = k % 2
                win, kind, r = play(a, b, f, P)
                if win == -1: continue
                g += 1
                if (win == 0) == True: w += 1
                kinds[kind] += 1; rounds.append(r)
                tot += 1; tot_first += (win == f)
            row.append(w / max(g, 1))
        print(f"{a:12}" + "".join(f"{x*100:7.0f}%" for x in row))
    print(f"avantage 1er joueur: {tot_first/tot*100:.0f}%  | fins: {dict(kinds)}  | rounds moyens: {sum(rounds)/len(rounds):.1f}")

BASE = dict(nobj=3, cap=6, vp=10, maxr=30, alter_bonus=1, def_k=1)
if __name__ == "__main__":
    random.seed(1)
    print("=== BASE ===")
    matrix(BASE)
    print("\n=== capture 8 au lieu de 6 ===")
    matrix({**BASE, "cap": 8})
    print("\n=== 15 PV de domination ===")
    matrix({**BASE, "vp": 15})
    print("\n=== sans bonus Alter-Ego adverse ===")
    matrix({**BASE, "alter_bonus": 0})
