"""45017 Suit Up (pack aoa) : cas du harnais, apres la reecriture du 18/09/2026.

Defaut signale en jeu : la carte proposait UNE question a deux cibles, on
pouvait prendre deux ameliorations, et le couple illegal faisait perdre la
carte. Elle pose desormais deux recherches : un allie, puis une amelioration
attachable A CET ALLIE.
"""
import io, json

p = '/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src/tools/test_capacites.py'
s = io.open(p, encoding='utf8').read()

# ⚠ AUCUN ChangeForm : la partie COMMENCE en alter-ego (RECETTES §7ter), et
# `Puzzle.ChangeForm('01001b')` RETOURNE la face en jeu, donc passerait en
# forme heros, ou l'Alter-Ego Action n'est pas offerte (3 cas rouges, la carte
# restait en main).


def cas(nom, pourquoi, deck, attendu, **extra):
    d = {
        "nom": nom,
        "pourquoi": pourquoi,
        "scenario": "rhino",
        "heros": "spider_man",
        "mise_en_place": [],
        "declencher": ["Puzzle.CreatePlayerDeck(" + ", ".join(f"'{c}'" for c in deck) + ")"],
        # 45017 coute 2 : une seule Energy (01088) rend [[energy]][[energy]].
        "main_exclusive": ["45017", "01088"],
        "jouer": ["45017"],
        "accepter_choix": True,
        "verifier": "etat_attendu",
        "attendu": attendu,
    }
    d.update(extra)
    return d


CAS = [
    cas("45017 Suit Up [aoa] — un allie ET une amelioration attachable a CET allie arrivent en main ; l'amelioration d'identite est ecartee",
        "deux recherches successives (Search.PlayerCard, la seconde avec CardFinder(canbe_attach_to=<allie>)) : "
        "01074 Inspired s'attache a un allie, 01065 Heroic Intuition s'attache a l'identite et ne doit jamais etre proposee",
        ['01067', '01074', '01065'],
        {"en_main": ["01067", "01074"], "taille_main": 2}),

    cas("45017 Suit Up [aoa] — contre-cas : aucune amelioration attachable a un allie, rien n'entre en main",
        "« for an ally AND an upgrade » : les deux ou aucun. Les allies sans amelioration attachable "
        "ne sont meme pas proposes, sinon le joueur choisit un allie et perd sa carte pour rien",
        ['01067', '01065', '01065'],
        {"taille_main": 0}),

    cas("45017 Suit Up [aoa] — Sidekick (45015, « identity-specific ally ») n'est prise qu'avec l'allie signature : Black Cat, pas Maria Hill",
        "le filtre est la VRAIE regle d'attache (Upgrade.CanAttachTo relit le selecteur de la capacite Play) : "
        "45015 ne s'attache qu'a un allie de classe Hero, donc Black Cat (01002) et jamais Maria Hill (01067)",
        ['01002', '01067', '45015'],
        {"en_main": ["01002", "45015"], "taille_main": 2}),
]

DEBUT = "    # ------------------------------------------------------------------------\n    # 45017 Suit Up (pack aoa)"
FIN = "    # ---- fin des cas 45017 ----\n"
bloc = DEBUT + " — reecrite le 18/09/2026. Genere par scratchpad/b3/gen_cas_45017.py.\n    # ------------------------------------------------------------------------\n"
for c in CAS:
    bloc += "    " + json.dumps(c, ensure_ascii=False, indent=4).replace("\n", "\n    ").replace(": true", ": True").replace(": false", ": False") + ",\n"
bloc += FIN

if DEBUT in s:
    i = s.index(DEBUT)
    j = s.index(FIN, i) + len(FIN)
    s = s[:i] + bloc + s[j:]
else:
    ancre = "    # ------------------------------------------------------------------------\n    # Pack officiel « fne » — bloc 2"
    assert ancre in s
    s = s.replace(ancre, bloc + ancre, 1)

io.open(p, 'w', encoding='utf8').write(s)
import ast
ast.parse(s)
print("cas 45017 :", len(CAS), "; syntaxe OK")
