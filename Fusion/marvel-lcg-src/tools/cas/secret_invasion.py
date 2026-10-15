# Cas test_capacites du scenario SECRET INVASION (sk189-227) : Veranke, complots, environnement, paquet IMPOSTOR.
# Prefixe des cas : [secret_invasion] ; filtre : `secret_invasion`. Le SUJET de chaque cas est le card_id dans son nom.
#
# Conventions de ce fichier :
#  - Spider-Man (01001) demarre en ALTER EGO ; `HEROS` le met en forme heros.
#  - `GARDER(n, ...)` : ne laisse dans le paquet IMPOSTOR que les cartes dont le numero du SET (27..46) est cite, pour que
#    « au hasard » soit deterministe (`Puzzle.Remove` retire les autres de la partie).
#  - `FOND` : un deck rencontre sans surprise (trois Hydra Mercenary 01101, sbires a boost 1).
#  - Les verifications passent par `si_etat` : cles propres (`soupcons`, `mechant`, `paquet`, `calc`...) puis delegation a
#    `etat_attendu`. `calc` = [[expression, valeur attendue]] evaluees dans l'espace de la verification (aides : `j0`, `j1`,
#    `ids(faces)`, `par_id(card_id)`, `W` = Worlds, `soupcons()`, `villain()`, `complot()`, `paquet`).
NORMAL = "sk_secret_invasion"
EXPERT = "sk_secret_invasion_expert"
HEROS = "Puzzle.ChangeForm('01001b')"
FOND = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', '01101', '01101')"]
# Numeros imprimes (set) 27..46 -> card_id sk208..sk227
NUMEROS = list(range(27, 47))


def _id(n, face):
    """card_id de la face `face` ('a' = allie, 'b' = sbire) de la carte n° `n` du set (27..46)."""
    return f"sk{208 + n - 27}{face}"


def GARDER(*numeros):
    retirer = [_id(n, "a") for n in NUMEROS if n not in numeros]
    return ["Puzzle.Remove(" + ", ".join(f"'{c}'" for c in retirer) + ")"] if retirer else []


# nom court de chaque carte Impostor (pour les noms de cas)
NOMS = {27: "Pitt'o Nili", 28: "Khn'nr", 29: "M'lanz", 30: "Zr'x", 31: "Trl'k", 32: "Fry'lu", 33: "Sn'Tlo", 34: "Siri",
        35: "D'lutz", 36: "De'Lila", 37: "Grrix", 38: "Ssrov", 39: "Hs'fld", 40: "H'kurrek", 41: "Korya", 42: "Ch'Gra",
        43: "Hagar", 44: "Dharr", 45: "V'lrym", 46: "Criti Noll"}


def cas(nom, pourquoi, mise, declencher, attendu, verifier="si_etat", scenario=NORMAL, **cle):
    c = {"nom": "[secret_invasion] " + nom, "pourquoi": pourquoi, "scenario": scenario, "heros": cle.pop("heros", "spider_man"),
         "mise_en_place": mise, "declencher": declencher, "verifier": verifier, "attendu": attendu}
    c.update(cle)
    # La main de depart de Spider-Man contient 01061 Great Responsibility, que le pilote joue : elle remplace toute menace
    # posee par des degats (piege paye pendant les tests). Main fixee a une ressource, sauf cas qui la videraient.
    if any("SetThreat" in m for m in mise) and not any("EmptyHand" in m for m in mise):
        c["mise_en_place"] = ["Puzzle.EmptyHand()"] + list(mise)
        mise = c["mise_en_place"]
    if "main_exclusive" not in c and not any("EmptyHand" in m for m in mise):
        c["main_exclusive"] = ["01088"]
    return c


CAS = []

# ======================================================================================================================
# Mise en place
# ======================================================================================================================
CAS += [
    cas("sk189a Setup (1A sk192a, puis 1B sk192b) : Veranke CAMOUFLAGED, environnement en jeu, paquet IMPOSTOR de 20 cartes",
        "Livret p. 16 : Spider-Woman (Veranke) commence CAMOUFLAGED ; Setup de 1A : creer le paquet IMPOSTOR (20 cartes) et mettre "
        "« Who Do You Trust? » en jeu ; 1B : objectif 8, escalade 1, menace de depart 2 (1 joueur)",
        [], [], {"en_jeu": ["sk189a", "sk192b", "sk194"], "hors_jeu": ["sk189b", "sk190a"], "paquet": 20, "defausse_paquet": 0,
                 "mechant": "sk189a", "soupcons": 0, "menace": [["sk192b", 2]], "pv_max": [["sk189a", 14]],
                 "stats": [["sk192b", "escalation_threat", 1], ["sk192b", "printed_target_threat", 8]]}),
    cas("sk192a Setup EXPERT : on commence au stade II (sk190a), meme paquet et meme environnement",
        "Insert p. 16 : mode expert = Spider-Woman (II) puis (III) ; Setup identique",
        [], [], {"en_jeu": ["sk190a", "sk192b", "sk194"], "hors_jeu": ["sk189a"], "paquet": 20, "mechant": "sk190a",
                 "pv_max": [["sk190a", 18]]}, scenario=EXPERT),
    cas("sk192b Valeurs par joueur : 2 joueurs, Veranke I a 28 PV et la menace de depart vaut 4",
        "Valeurs « par joueur » multipliees par le nombre de joueurs (HP 14*, StartingThreat 2*)",
        [], [], {"pv_max": [["sk189a", 28]], "menace": [["sk192b", 4]]}, heros2="hawkeye"),
]

# ======================================================================================================================
# Veranke : les six faces
# ======================================================================================================================
STADES = {
    1: ("sk189a", "sk189b", NORMAL, [], (14, 2, 2), (14, 2, 2)),
    2: ("sk190a", "sk190b", NORMAL, ["Puzzle.AdvanceVillain()"], (18, 3, 2), (18, 2, 3)),
    3: ("sk191a", "sk191b", EXPERT, ["Puzzle.AdvanceVillain()"], (21, 3, 3), (21, 2, 4)),
}
for stade, (a, b, scenario, avancer, (pva, scha, atka), (pvb, schb, atkb)) in STADES.items():
    base = avancer + [HEROS] + FOND
    CAS += [
        cas(f"{a} valeurs imprimees : PV {pva}[per_hero], MNG {scha}, ATQ {atka}",
            f"Stade {stade}, face A (CAMOUFLAGED), lu sur le scan : HP {pva}*, SCH {scha}, ATK {atka}*",
            avancer, [], {"mechant": a, "pv_max": [[a, pva]], "stats": [[a, "scheme", scha], [a, "attack", atka]],
                          "traits_de": [[a, "CAMOUFLAGED"], [a, "SKRULL"]]}, scenario=scenario),
        cas(f"{b} valeurs imprimees : PV {pvb}[per_hero], MNG {schb}, ATQ {atkb}",
            f"Stade {stade}, face B (REVEALED), lu sur le scan : HP {pvb}*, SCH {schb}, ATK {atkb}",
            avancer + ["Puzzle.Flip('" + a + "')"], [], {"mechant": b, "pv_max": [[b, pvb]],
                                                         "stats": [[b, "scheme", schb], [b, "attack", atkb]],
                                                         "traits_de": [[b, "REVEALED"], [b, "SKRULL"]]}, scenario=scenario),
        cas(f"{a} ne peut pas subir de degats ; TEMOIN {b} (face REVEALED) : les degats passent",
            "« Spider-Woman cannot take damage » (face A) ; une fois retournee sur Queen Veranke on peut la blesser",
            base, [f"Puzzle.Damage('{a}', 5)", f"Puzzle.Flip('{a}')", f"Puzzle.Damage('{b}', 5)"],
            {"mechant": b, "degats": [[b, 5]]}, scenario=scenario),
        cas(f"{a} ne subit aucun degat meme a 99 : jamais vaincue sous sa forme CAMOUFLAGED",
            "Degats massifs sur la face A : 0 degat, le stade ne change pas",
            base, [f"Puzzle.Damage('{a}', 99)"], {"mechant": a, "degats": [[a, 0]]}, scenario=scenario),
        cas(f"{a} Reponse forcee : apres qu'elle t'attaque, 1 jeton de soupcon ; TEMOIN {b} : aucun",
            "★ « After Spider-Woman attacks you, place 1 suspicion counter on Who Do You Trust? » ; Queen Veranke n'en pose pas",
            base, [f"Puzzle.Attack('{a}')", f"Puzzle.Flip('{a}')", f"Puzzle.Attack('{b}')"],
            {"mechant": b, "soupcons": 1}, scenario=scenario),
        cas(f"{a} « You are a Skrull! » : incline un heros et depense 1 ressource -> Veranke se retourne sur {b}",
            "Action de heros : inclinez un heros et depensez 1[per_hero] ressources (1 joueur : 1) -> flip. Le heros est incline, "
            "la ressource (01088 Energy) est depensee",
            base, [f"Puzzle.Action('{a}', 'HeroAction', 0)"],
            {"mechant": b, "calc": [["par_id('01001a').IsExhaust()", True], ["'01088' in ids(j0.discard_pile.GetAll())", True]]},
            scenario=scenario, main_exclusive=["01088"]),
        cas(f"{a} « You are a Skrull! » sans ressource : le cout n'est pas paye, Veranke reste {a}",
            "Pas de ressource en main : le cout ne peut pas etre paye",
            base + ["Puzzle.EmptyHand()"], [f"Puzzle.Action('{a}', 'HeroAction', 0)"],
            {"mechant": a, "calc": [["par_id('01001a').IsExhaust()", False]]}, scenario=scenario),
    ]
    if stade == 1:
        CAS += [
            cas(f"{a} « You are a Skrull! » : 2 joueurs, le cout (2 ressources) se paie EN GROUPE avec la main de l'autre joueur",
                "« The players can pay this ability's costs as a group » : le joueur 0 n'a aucune ressource, le joueur 1 tient 01088 "
                "(YY) : le cout 1[per_hero] x 2 joueurs = 2 est paye et Veranke se retourne",
                [HEROS, "Puzzle.EmptyHand()"], [f"Puzzle.Action('{a}', 'HeroAction', 0)"],
                {"mechant": b, "calc": [["par_id('01001a').IsExhaust()", True], ["len(j0.hand_cards.GetAll())", 0]]},
                heros2="hawkeye"),
            cas(f"{a} « You are a Skrull! » : meme montage mais Mistrust and Paranoia (sk201) interdit le paiement en groupe : rien",
                "sk201 « Players cannot pay any card's or ability's costs as a group » : le joueur 0 seul ne peut pas payer, Veranke "
                f"reste {a}",
                [HEROS, "Puzzle.EmptyHand()", "Puzzle.Reveal('sk201')"],
                [f"Puzzle.Action('{a}', 'HeroAction', 0)"],
                {"mechant": a, "calc": [["par_id('01001a').IsExhaust()", False]]}, heros2="hawkeye"),
        ]

# face B : retournement en fin de phase du mechant, defaite
CAS += [
    cas("sk189b Reponse forcee : fin de la phase du mechant avec un joueur en ALTER EGO -> Queen Veranke se retourne sur Spider-Woman",
        "« After the villain phase ends, if any player is in alter-ego form, flip Queen Veranke » : le heros de test est en alter ego",
        ["Puzzle.Flip('sk189a')"] + FOND, ["Puzzle.EndVillainPhase()"], {"mechant": "sk189a"}),
    cas("sk189b Reponse forcee : TEMOIN, tous les joueurs en forme HEROS -> Queen Veranke reste REVEALED",
        "Aucun alter ego : pas de retournement",
        ["Puzzle.Flip('sk189a')", HEROS] + FOND, ["Puzzle.EndVillainPhase()"], {"mechant": "sk189b"}),
    cas("sk190b Reponse forcee : stade II, un alter ego -> retourne sur Spider-Woman (sk190a)",
        "Meme texte au stade II",
        ["Puzzle.AdvanceVillain()", "Puzzle.Flip('sk190a')"] + FOND, ["Puzzle.EndVillainPhase()"], {"mechant": "sk190a"}),
    cas("sk190b Reponse forcee : TEMOIN stade II, forme heros -> reste sk190b",
        "Aucun alter ego",
        ["Puzzle.AdvanceVillain()", "Puzzle.Flip('sk190a')", HEROS] + FOND, ["Puzzle.EndVillainPhase()"], {"mechant": "sk190b"}),
    cas("sk191b Reponse forcee : stade III, un alter ego -> retourne sur Spider-Woman, SANS defausser la carte du deck",
        "« if any player is in alter-ego form, flip » : la branche « Otherwise » (defausser) ne part PAS ; deck rencontre intact",
        ["Puzzle.AdvanceVillain()", "Puzzle.Flip('sk191a')"] + FOND, ["Puzzle.EndVillainPhase()"],
        {"mechant": "sk191a", "calc": [["len(Worlds.GetEncounterDeckCards(monde))", 3]]}, scenario=EXPERT),
    cas("sk191b Reponse forcee : stade III, forme heros, la carte defaussee est une TRAITRISE -> Queen Veranke se retourne",
        "« Otherwise, discard the top card of the encounter deck, if it is a treachery, flip Queen Veranke » : 01112 False Alarm "
        "(traitrise) sur le dessus",
        ["Puzzle.AdvanceVillain()", "Puzzle.Flip('sk191a')", HEROS, "Puzzle.EmptyEncounterDeck()",
         "Puzzle.CreateEncounterDeck('01101', '01101', '01112')"], ["Puzzle.EndVillainPhase()"],
        {"mechant": "sk191a", "calc": [["len(Worlds.GetEncounterDeckCards(monde))", 2]]}, scenario=EXPERT),
    cas("sk191b Reponse forcee : TEMOIN stade III, forme heros, la carte defaussee n'est PAS une traitrise -> reste sk191b",
        "Un sbire (01101 Hydra Mercenary) sur le dessus : defausse sans retournement",
        ["Puzzle.AdvanceVillain()", "Puzzle.Flip('sk191a')", HEROS] + FOND, ["Puzzle.EndVillainPhase()"],
        {"mechant": "sk191b", "calc": [["len(Worlds.GetEncounterDeckCards(monde))", 2]]}, scenario=EXPERT),
    cas("sk189b Une fois vaincue : retire TOUS les jetons de soupcon ; le stade II arrive du MEME COTE (Queen Veranke, sk190b)",
        "« When Defeated: Remove all suspicion counters » ; livret p. 16 : le stade suivant arrive du meme cote que le stade vaincu",
        ["Puzzle.Counter('sk194', 'suspicion', 3)", "Puzzle.Flip('sk189a')", HEROS] + FOND, ["Puzzle.Damage('sk189b', 14)"],
        {"mechant": "sk190b", "soupcons": 0, "hors_jeu": ["sk189b"], "en_jeu": ["sk190b"]}),
    cas("sk189b TEMOIN : meme montage SANS vaincre la reine (13 degats sur 14) : les jetons restent",
        "Seule la DEFAITE retire les jetons",
        ["Puzzle.Counter('sk194', 'suspicion', 3)", "Puzzle.Flip('sk189a')", HEROS] + FOND, ["Puzzle.Damage('sk189b', 13)"],
        {"mechant": "sk189b", "soupcons": 3, "degats": [["sk189b", 13]]}),
    cas("sk190b Une fois vaincue : retire les jetons ; stade III du meme cote (sk191b)",
        "Mode expert : sk190 puis sk191 ; « When Defeated » du stade II",
        ["Puzzle.Counter('sk194', 'suspicion', 3)", "Puzzle.Flip('sk190a')", HEROS] + FOND, ["Puzzle.Damage('sk190b', 18)"],
        {"mechant": "sk191b", "soupcons": 0}, scenario=EXPERT),
    cas("sk191b Dernier stade vaincu : pas de « When Defeated », les jetons restent et les joueurs GAGNENT",
        "sk191b n'a pas de « When Defeated » (le texte imprime n'en porte pas) : les jetons restent, partie gagnee",
        ["Puzzle.AdvanceVillain()", "Puzzle.Counter('sk194', 'suspicion', 3)", "Puzzle.Flip('sk191a')", HEROS] + FOND,
        ["Puzzle.Damage('sk191b', 21)"], {"calc": [["monde.is_game_over", True], ["soupcons()", 3]]}, scenario=EXPERT),
    cas("sk189a Avancee de stade depuis la face A : le stade II arrive sur la face A (sk190a)",
        "Livret p. 16 : « the next stage enters play on the same side as the just defeated stage » ; face vaincue = A -> sk190a",
        [], ["Puzzle.AdvanceVillain()"], {"mechant": "sk190a", "hors_jeu": ["sk189a"]}),
    cas("sk189b Avancee de stade depuis la face B (REVEALED) : le stade II arrive sur la face B (sk190b), les degats restent",
        "Livret p. 16 : meme cote (le nouveau stade a ses propres PV)",
        ["Puzzle.Flip('sk189a')", HEROS] + FOND, ["Puzzle.Damage('sk189b', 5)", "Puzzle.AdvanceVillain()"],
        {"mechant": "sk190b", "hors_jeu": ["sk189b"]}),
    cas("sk189b Retournements successifs : les degats RESTENT sur la carte (5 apres deux retournements)",
        "Livret p. 16 : quand le mechant change de forme, attachements, cartes d'etat, boosts et degats restent",
        ["Puzzle.Flip('sk189a')", HEROS] + FOND, ["Puzzle.Damage('sk189b', 5)", "Puzzle.Flip('sk189b')", "Puzzle.Flip('sk189a')"],
        {"mechant": "sk189b", "degats": [["sk189b", 5]]}),
]

# ======================================================================================================================
# Paquet IMPOSTOR : les 20 allies (face A) et la mecanique commune
# ======================================================================================================================
ECHANGE = {n: (f"sk{208 + n - 27}a", f"sk{208 + n - 27}b") for n in NUMEROS}
# (SCH imprime, degats consequentiels d'une ATQ [pastilles ATQ], PV)
STATS_ALLIE = {27: (1, 2, 4), 28: (1, 1, 3), 29: (1, 2, 4), 30: (1, 2, 3), 31: (2, 1, 2), 32: (1, 2, 3), 33: (2, 1, 4), 34: (1, 2, 4),
               35: (1, 2, 4), 36: (2, 1, 3), 37: (2, 1, 3), 38: (1, 2, 4), 39: (1, 2, 3), 40: (1, 1, 2), 41: (1, 2, 3), 42: (1, 1, 2),
               43: (1, 2, 4), 44: (2, 1, 3), 45: (1, 1, 3), 46: (3, 1, 3)}

for n in NUMEROS:
    a, b = ECHANGE[n]
    sch, pastilles, pv = STATS_ALLIE[n]
    CAS += [
        cas(f"{a} Interruption forcee : l'allie {NOMS[n]} devrait QUITTER le jeu (vaincu), il se RETOURNE : sbire {b} engage, PV soignes",
            "« When X would leave play, flip X instead » : 99 degats tuent l'allie ; il ne part pas, il passe sur sa face sbire, "
            "engage son controleur, SANS aucun degat (« Heal all damage ») ; le paquet et sa defausse sont vides (la carte est en jeu)",
            GARDER(n) + [HEROS] + FOND,
            [f"Puzzle.PutIntoPlay('{a}', under_control=True)", f"Puzzle.Damage('{a}', 99)"],
            {"en_jeu": [b], "hors_jeu": [a], "degats": [[b, 0]], "pv_max": [[b, pv]],
             "calc": [[f"ids(j0.engaged_minions.GetAll())", [b]], ["ids(j0.allies.GetAll())", []],
                      ["paquet.deck.GetSize()", 0], ["paquet.discard_pile.GetSize()", 0],
                      [f"par_id('{b}').HasTrait('REVEALED') and par_id('{b}').HasTrait('IMPOSTOR') and par_id('{b}').HasTrait('SKRULL')", True]]}),
        cas(f"{a} valeurs imprimees de l'allie : PV {pv}, ATQ avec {pastilles} degat(s) consequentiel(s), traits CAMOUFLAGED IMPOSTOR SKRULL",
            "Lu sur le scan : badge orange = PV, ATQ a pastilles = degats consequentiels (cle desc « ATK » avec autant d'etoiles)",
            GARDER(n) + FOND, [f"Puzzle.PutIntoPlay('{a}', under_control=True)"],
            {"en_jeu": [a], "pv_max": [[a, pv]],
             "stats": [[a, "printed_attack_consequential_damage", pastilles]],
             "traits_de": [[a, "CAMOUFLAGED"], [a, "IMPOSTOR"], [a, "SKRULL"]],
             "calc": [[f"SchAllie_(par_id('{a}'))", sch]]}),
    ]

# Un allie CAMOUFLAGED s'utilise comme un allie normal : il attaque (degats consequentiels), defend, NE PEUT PAS contrer
for n, pastilles in ((27, 2), (28, 1), (31, 1)):
    a, b = ECHANGE[n]
    CAS.append(cas(f"{a} attaque : subit ses {pastilles} degat(s) consequentiel(s) (les pastilles de l'ATQ) et peut attaquer le mechant",
                   "« It can attack, or defend » : attaque de base de l'allie, puis degats consequentiels = pastilles de l'ATQ",
                   GARDER(n) + [HEROS] + FOND, [f"Puzzle.PutIntoPlay('{a}', under_control=True)", f"Puzzle.Attack('{a}')"],
                   {"degats": [[a, pastilles]]}))
for n in (27, 31, 46):
    a, b = ECHANGE[n]
    CAS += [
        cas(f"{a} ne peut pas CONTRER : son pouvoir THW ne retire aucune menace",
            "Livret p. 16 : « It cannot thwart » ; la menace du complot principal ne bouge pas (temoin juste apres)",
            GARDER(n) + [HEROS] + FOND + ["Puzzle.SetThreat('sk192b', 4)"],
            [f"Puzzle.PutIntoPlay('{a}', under_control=True)", f"Puzzle.Thwart('{a}')"],
            {"menace": [["sk192b", 4]]}),
    ]
CAS += [
    cas("sk208a TEMOIN du contre : un allie ordinaire (01041 Shuri, THW 1) retire bien de la menace",
        "Meme montage, allie normal : la menace baisse de 4 a 3 (le contre fonctionne dans ce harnais)",
        GARDER(27) + [HEROS] + FOND + ["Puzzle.SetThreat('sk192b', 4)"],
        ["Puzzle.PutIntoPlay('01041', under_control=True)", "Puzzle.Thwart('01041')"],
        {"menace": [["sk192b", 3]]}),
    cas("sk208a defend : un allie CAMOUFLAGED peut defendre (il encaisse l'attaque, 1 degat de l'Hydra Mercenary)",
        "Livret p. 16 : « it can attack, or defend » ; ATK 1 de 01101 sur l'allie qui defend",
        GARDER(27) + [HEROS] + FOND, ["Puzzle.PutIntoPlay('sk208a', under_control=True)", "Puzzle.PutIntoPlay('01101')",
                                      "Puzzle.Attack('01101', 'sk208a')"],
        {"degats": [["sk208a", 1]], "degats_identite": 0}),
    cas("sk208a Interruption forcee : une DEFAUSSE ordinaire (pas une defaite) retourne aussi l'allie",
        "« would LEAVE play » : tout depart du jeu ; ici une defausse par effet",
        GARDER(27) + [HEROS] + FOND, ["Puzzle.PutIntoPlay('sk208a', under_control=True)", "Puzzle.Discard('sk208a')"],
        {"en_jeu": ["sk208b"], "hors_jeu": ["sk208a"], "calc": [["ids(j0.engaged_minions.GetAll())", ["sk208b"]],
                                                              ["ids(j0.discard_pile.GetAll()).count('sk208a')", 0]]}),
    cas("sk208a Retourner l'allie : cartes d'etat, ameliorations (01074 Inspired) et jetons partent, le sbire arrive nu",
        "Livret p. 16 : apres le retournement, cartes d'etat, ameliorations et autres elements associes a l'allie sont defausses ; "
        "Revelation (sk207) retourne l'allie CAMOUFLAGED (le seul) : etourdi + desoriente + Inspired -> sbire sans rien",
        GARDER(27) + [HEROS] + FOND + ["Puzzle.PutIntoPlay('sk208a', under_control=True)", "Puzzle.AttachReel('01074', 'sk208a')",
                                       "Puzzle.Stun('sk208a')", "Puzzle.Confuse('sk208a')", "Puzzle.Damage('sk208a', 2)"],
        ["Puzzle.Reveal('sk207')"],
        {"en_jeu": ["sk208b"], "hors_jeu": ["sk208a", "01074"], "degats": [["sk208b", 0]],
         "statuts_absents": [["sk208b", "Stunned"], ["sk208b", "Confused"]],
         "calc": [["ids(j0.engaged_minions.GetAll())", ["sk208b"]], ["'01074' in ids(j0.discard_pile.GetAll())", True]]}),
    cas("sk208a Retourner l'allie d'un AUTRE joueur : le sbire engage le joueur qui CONTROLAIT l'allie (pas celui qui revele)",
        "Livret p. 16 : « The REVEALED minion engages the same player who controlled that card before it was flipped » ; "
        "l'allie est sous le controle du joueur 1, Revelation est revelee par le joueur 0",
        GARDER(27) + [HEROS] + FOND + ["Puzzle.PutIntoPlay('sk208a', under_control=True, player=1)"], ["Puzzle.Reveal('sk207')"],
        {"en_jeu": ["sk208b"], "calc": [["ids(j1.engaged_minions.GetAll())", ["sk208b"]], ["ids(j0.engaged_minions.GetAll())", []]]},
        heros2="hawkeye"),
    cas("sk208a Mise en jeu sous le controle d'un joueur : Arrival of Impostors donne UN allie a CHAQUE joueur (2 joueurs)",
        "sk202 « Each player puts a CAMOUFLAGED ally at random from the IMPOSTOR deck into play under their control » ; deux cartes "
        "restent dans le paquet ; chacun a son allie",
        GARDER(27, 28) + [HEROS] + FOND, ["Puzzle.Reveal('sk202')"],
        {"calc": [["len(j0.allies.GetAll())", 1], ["len(j1.allies.GetAll())", 1],
                  ["sorted(ids(j0.allies.GetAll()) + ids(j1.allies.GetAll()))", ["sk208a", "sk209a"]],
                  ["paquet.deck.GetSize()", 0]]}, heros2="hawkeye"),
    cas("sk208a Paquet vide : on y REMELANGE la defausse IMPOSTOR, sans penalite (aucun jeton d'acceleration)",
        "Livret p. 16 : « If the IMPOSTOR deck is ever empty, shuffle the IMPOSTOR discard pile back into the IMPOSTOR deck. "
        "There is no penalty » : deux sbires tues -> defausse de 2 ; Arrival of Impostors : un allie sort du paquet remelange, "
        "face ALLIE, il reste une carte dans le paquet, la defausse est vide",
        GARDER(27, 28) + [HEROS] + FOND + ["Puzzle.Reveal('sk206')", "Puzzle.Reveal('sk206')"],
        ["Puzzle.Damage('sk208b', 99)", "Puzzle.Damage('sk209b', 99)", "Puzzle.Reveal('sk202')"],
        {"calc": [["paquet.deck.GetSize()", 1], ["paquet.discard_pile.GetSize()", 0], ["len(j0.allies.GetAll())", 1],
                  ["ids(j0.allies.GetAll())[0] in ('sk208a', 'sk209a')", True],
                  ["sum(f.acceleration_token for f in W.GetAllMainSchemes(monde))", 0]]}),
    cas("sk208b Le sbire REVEALED qui quitte le jeu va dans la DEFAUSSE IMPOSTOR (pas dans la defausse rencontre)",
        "Livret p. 16 : « If the REVEALED minion would leave play, place it in the IMPOSTOR discard pile » ; Invasion Fleet (sk206) "
        "met le sbire en jeu, 99 degats le defont",
        GARDER(27) + [HEROS] + FOND, ["Puzzle.Reveal('sk206')", "Puzzle.Damage('sk208b', 99)"],
        {"dans_defausse_paquet": ["sk208b"], "defausse_paquet": 1, "paquet": 0, "hors_jeu": ["sk208b"],
         "calc": [["'sk208b' in ids(W.GetEncounterDiscardPileCards(monde))", False]]}),
    cas("sk208a Une allie en trop : la limite d'allies (3) s'applique a un allie CAMOUFLAGED ; l'excedent se retourne ou part",
        "Livret p. 16 : il compte dans la limite d'allies ; 3 allies deja en jeu + Arrival of Impostors : jamais plus de 3 allies",
        GARDER(27) + [HEROS] + FOND + ["Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.PutIntoPlay('01041', under_control=True)",
                                       "Puzzle.PutIntoPlay('01067', under_control=True)"],
        ["Puzzle.Reveal('sk202')"],
        {"calc": [["len(j0.allies.GetAll()) <= 3", True]]}),
]

# ======================================================================================================================
# Paquet IMPOSTOR : les 20 sbires (face B), un cas par capacite imprimee
# ======================================================================================================================
HEROS2 = "Puzzle.ChangeForm('04001b')"          # Hawkeye (joueur 2) passe en forme heros


EXH = ["Puzzle.Exhaust('01001a')"]     # un heros incline ne defend pas : les degats arrivent
EXH2 = ["Puzzle.Exhaust('04001a')"]


def reveler(n, heros=True, incline=False):
    """Le paquet IMPOSTOR ne garde que la carte n ; Invasion Fleet (sk206) la REVELE : le sbire entre en jeu engage."""
    return GARDER(n) + ([HEROS] if heros else []) + FOND + (EXH if incline else []) + ["Puzzle.Reveal('sk206')"]


for n in NUMEROS:
    a, b = ECHANGE[n]
    sch_s, _, pv = STATS_ALLIE[n]
    CAS.append(cas(f"{b} Une fois revele : soigne tout et s'engage avec le joueur qui le revele (Invasion Fleet, 1 joueur)",
                   "« When Revealed: Heal all damage from X and put it into play engaged with you » : le sbire sort du paquet, "
                   "arrive engage, avec ses PV maximum, sur sa face REVEALED",
                   GARDER(n) + [HEROS] + FOND, ["Puzzle.Reveal('sk206')"],
                   {"en_jeu": [b], "degats": [[b, 0]], "pv_max": [[b, pv]],
                    "traits_de": [[b, "REVEALED"], [b, "IMPOSTOR"], [b, "SKRULL"]],
                    "calc": [["ids(j0.engaged_minions.GetAll())[:1]", [b]], ["paquet.deck.GetSize()", 0],
                             [f"par_id('{b}').scheme", {38: 1, 46: 3}.get(n, sch_s)]]}))

# --- capacites imprimees, carte par carte
a, b = ECHANGE[27]
CAS += [
    cas(f"{b} Guard : mot-cle natif lu dans desc, le sbire garde le mechant",
        "Guard. (« While this minion is engaged with you, you cannot attack the villain ») : `IsGuard()` vrai en jeu",
        reveler(27), [], {"calc": [[f"par_id('{b}').IsGuard()", True]]}),
]
a, b = ECHANGE[28]
CAS += [
    cas(f"{b} Une fois vaincu : retire TOUS les jetons de soupcon de Who Do You Trust?",
        "« When Defeated: Remove all suspicion counters from Who Do You Trust? » : 3 jetons poses, 99 degats",
        reveler(28) + ["Puzzle.Counter('sk194', 'suspicion', 3)"], [f"Puzzle.Damage('{b}', 99)"], {"soupcons": 0}),
    cas(f"{b} TEMOIN : sans la defaite, les 3 jetons restent",
        "Le sbire vivant ne retire rien",
        reveler(28) + ["Puzzle.Counter('sk194', 'suspicion', 3)"], [f"Puzzle.Damage('{b}', 1)"], {"soupcons": 3}),
]
a, b = ECHANGE[29]
CAS += [
    cas(f"{b} ★ Interruption forcee : quand M'lanz t'attaque, son attaque est AUSSI resolue contre chaque autre heros (2 joueurs en forme heros)",
        "Whirlwind (01130) en modele : un seul sbire, deux attaques ; le heros 2 subit des degats",
        GARDER(29) + [HEROS, HEROS2] + FOND + EXH + EXH2 + ["Puzzle.Reveal('sk206')"], [f"Puzzle.Attack('{b}')"],
        {"degats_identite_min": 1, "calc": [["j1.GetIdentity().max_health - j1.GetIdentity().health >= 1", True]]}, heros2="hawkeye"),
    cas(f"{b} TEMOIN : un sbire ordinaire (01101) n'attaque que SON joueur, le heros 2 est indemne",
        "Meme montage avec Hydra Mercenary : seul le joueur 0 est touche",
        GARDER(29) + [HEROS, HEROS2] + FOND + EXH + EXH2, ["Puzzle.PutIntoPlay('01101')", "Puzzle.Attack('01101')"],
        {"degats_identite_min": 1, "calc": [["j1.GetIdentity().max_health - j1.GetIdentity().health", 0]]}, heros2="hawkeye"),
]
a, b = ECHANGE[30]
CAS += [
    cas(f"{b} Toughness : le sbire entre en jeu avec une carte Robuste",
        "« Toughness. (This character enters play with a tough status card.) » : mot-cle natif lu dans desc",
        reveler(30), [], {"statuts": [[b, "Tough"]]}),
]
a, b = ECHANGE[31]
CAS += [
    cas(f"{b} ne peut pas subir de degats tant que le joueur engage est engage avec un AUTRE sbire SKRULL (Skrull Warrior sk110)",
        "« While the engaged player is engaged with another SKRULL minion Trl'k cannot take damage » : 3 degats, 0 subi",
        reveler(31) + ["Puzzle.PutIntoPlay('sk110')"], [f"Puzzle.Damage('{b}', 3)"],
        {"degats": [[b, 0]], "en_jeu": ["sk110"]}),
    cas(f"{b} TEMOIN : seul engage, Trl'k subit les 3 degats",
        "Meme montage sans l'autre sbire SKRULL",
        reveler(31), [f"Puzzle.Damage('{b}', 1)"], {"degats": [[b, 1]]}),
]
a, b = ECHANGE[32]
CAS += [
    cas(f"{b} Une fois vaincu : le joueur qui l'a vaincu recoit une carte rencontre FACE CACHEE",
        "« When Defeated: Deal the player who defeated X a facedown encounter card » : Spider-Man (hero) l'acheve par une attaque",
        reveler(32) + [f"Puzzle.Damage('{b}', 2)"], [f"Puzzle.Attack('01001a')"],
        {"hors_jeu": [b], "calc": [["len(j0.dealt_encounter_cards.Get(True))", 1]]}, cibles=[b]),
]
a, b = ECHANGE[33]
CAS += [
    cas(f"{b} Reduit de 1 les degats de chaque attaque : l'ATQ 2 de Spider-Man n'en inflige que 1",
        "« Reduce the amount of damage X takes from each attack by 1 »",
        reveler(33), [f"Puzzle.Attack('01001a')"], {"degats": [[b, 1]]}, cibles=[b]),
    cas(f"{b} TEMOIN : un sbire ordinaire subit les 2 degats de la meme attaque",
        "Hydra Mercenary (3 PV) en face du meme attaquant",
        GARDER(33) + [HEROS] + FOND, ["Puzzle.PutIntoPlay('01101')", "Puzzle.Attack('01001a')"],
        {"degats": [["01101", 2]]}, cibles=["01101"]),
]
a, b = ECHANGE[34]
CAS += [
    cas(f"{b} Patrol : mot-cle natif, le joueur engage ne peut pas contrer le complot principal",
        "« Patrol. (While this minion is engaged with you, you cannot thwart the main scheme.) » : la menace ne baisse pas",
        reveler(34) + ["Puzzle.SetThreat('sk192b', 4)"], ["Puzzle.Thwart('01001a')"],
        {"menace": [["sk192b", 4]], "calc": [[f"par_id('{b}').IsPatrol()", True]]}),
]
a, b = ECHANGE[35]
CAS += [
    cas(f"{b} Retaliate 1 : le heros qui l'attaque subit 1 degat",
        "« Retaliate 1 » : mot-cle natif lu dans desc ; Spider-Man attaque D'lutz (4 PV) et prend 1 degat de riposte",
        reveler(35), ["Puzzle.Attack('01001a')"], {"degats_identite": 1, "degats": [[b, 2]]}, cibles=[b]),
]
a, b = ECHANGE[36]
CAS += [
    cas(f"{b} Cout additionnel : pour l'attaquer il faut depenser 1 ressource (la carte 01088 de la main est depensee)",
        "« As an additional cost to attack De'Lila, you must spend 1 resource of any type » : l'attaque a lieu ET la ressource est depensee",
        reveler(36), ["Puzzle.Attack('01001a')"],
        {"degats": [[b, 2]], "calc": [["'01088' in ids(j0.discard_pile.GetAll())", True]]}, cibles=[b], main_exclusive=["01088"]),
    cas(f"{b} Cout additionnel : sans ressource a depenser, l'attaque n'a pas lieu (aucun degat)",
        "Main vide : le cout n'est pas paye, l'attaque est annulee",
        reveler(36) + ["Puzzle.EmptyHand()"], ["Puzzle.Attack('01001a')"], {"degats": [[b, 0]]}, cibles=[b]),
]
a, b = ECHANGE[37]
CAS += [
    cas(f"{b} Une fois vaincu : le mechant attaque le joueur qui l'a vaincu, MEME SI ce joueur est en alter ego",
        "« The villain attacks the player who defeated Grrix (even if that player is in alter-ego form) » : l'allie 01067 Maria Hill "
        "(joueur en ALTER EGO) acheve Grrix ; Spider-Woman (Veranke) attaque Peter Parker : il subit au moins 1 degat",
        reveler(37, heros=False) + [f"Puzzle.Damage('{b}', 2)", "Puzzle.PutIntoPlay('01067', under_control=True)"],
        ["Puzzle.Attack('01067')"],
        {"hors_jeu": [b], "degats_identite_min": 1, "calc": [["j0.IsAlterEgo()", True]]}, cibles=[b]),
    cas(f"{b} TEMOIN : tant que Grrix vit, le mechant n'attaque pas",
        "Meme montage, aucune defaite : l'identite est indemne",
        reveler(37, heros=False) + ["Puzzle.PutIntoPlay('01067', under_control=True)"], [], {"degats_identite": 0}),
]
a, b = ECHANGE[38]
CAS += [
    cas(f"{b} ★ Tant que le mechant est CAMOUFLAGED : SCH et ATQ imprimes (1 / 2)",
        "« While the villain has the REVEALED trait, Ssrov gets +1 SCH and +1 ATK » : Veranke commence CAMOUFLAGED",
        reveler(38), [], {"stats": [[b, "scheme", 1], [b, "attack", 2]]}),
    cas(f"{b} ★ Tant que le mechant est REVEALED (Queen Veranke) : +1 SCH et +1 ATQ (2 / 3), puis retour a 1 / 2 quand elle se camoufle",
        "Meme carte apres `flip` du mechant (sk189b) puis un second retournement",
        reveler(38), ["Puzzle.Flip('sk189a')"], {"mechant": "sk189b", "stats": [[b, "scheme", 2], [b, "attack", 3]]}),
    cas(f"{b} ★ +1 SCH +1 ATQ : le bonus RETOMBE quand le mechant repasse CAMOUFLAGED",
        "Deux retournements : sk189a -> sk189b -> sk189a",
        reveler(38), ["Puzzle.Flip('sk189a')", "Puzzle.Flip('sk189b')"], {"mechant": "sk189a", "stats": [[b, "scheme", 1], [b, "attack", 2]]}),
]
a, b = ECHANGE[39]
CAS += [
    cas(f"{b} Une fois vaincu : le joueur qui l'a vaincu met un allie CAMOUFLAGED du paquet en jeu sous son controle",
        "Deux cartes dans le paquet (Hs'fld et H'kurrek) ; Hs'fld est revele et tue par Spider-Man : l'autre carte (sk221a) arrive en jeu "
        "sous son controle, sur sa face ALLIE",
        GARDER(39, 40) + [HEROS] + FOND + ["Puzzle.Flip('sk220a')", "Puzzle.Reveal('sk220b')", f"Puzzle.Damage('{b}', 1)"],
        ["Puzzle.Attack('01001a')"],
        {"hors_jeu": [b], "calc": [["ids(j0.allies.GetAll())", ["sk221a"]], ["paquet.deck.GetSize()", 0]]}, cibles=[b]),
]
a, b = ECHANGE[40]
CAS += [
    cas(f"{b} ★ Ses attaques gagnent OVERKILL : un allie qui defend a 1 PV restant, l'exces d'un degat passe au heros",
        "« H'kurrek's attacks gain overkill, piercing, and ranged » : Maria Hill (2 PV, 1 degat deja) defend contre ATQ 2 : "
        "1 degat tue l'allie, l'exces de 1 est inflige au heros",
        reveler(40, heros=True, incline=True) + ["Puzzle.PutIntoPlay('01067', under_control=True)", "Puzzle.Damage('01067', 1)"],
        [f"Puzzle.Attack('{b}', '01067')"], {"degats_identite_min": 1}),
    cas(f"{b} TEMOIN overkill : Hydra Mercenary (ATQ 1) contre le meme defenseur : pas d'exces, le heros est indemne",
        "Meme montage, attaquant ordinaire",
        GARDER(40) + [HEROS] + FOND + EXH + ["Puzzle.PutIntoPlay('01067', under_control=True)", "Puzzle.Damage('01067', 1)",
                                       "Puzzle.PutIntoPlay('01101')"],
        ["Puzzle.Attack('01101', '01067')"], {"degats_identite": 0}),
    cas(f"{b} ★ Ses attaques gagnent PIERCING : le heros Robuste subit quand meme les 2 degats",
        "Piercing ignore Robuste ; Spider-Man porte une carte Robuste, H'kurrek l'attaque",
        reveler(40, incline=True) + ["Puzzle.Tough('01001a')"], [f"Puzzle.Attack('{b}')"], {"degats_identite_min": 2}),
    cas(f"{b} TEMOIN piercing : Hydra Mercenary contre le heros Robuste : la carte Robuste absorbe, aucun degat",
        "Meme montage, attaquant ordinaire",
        GARDER(40) + [HEROS] + FOND + EXH + ["Puzzle.Tough('01001a')", "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('01101')"],
        {"degats_identite": 0}),
    cas(f"{b} ★ Ses attaques gagnent RANGED : le defenseur 04014 U.S. Agent (Riposte) ne riposte pas",
        "Ranged ignore la riposte ; sk122 en modele",
        reveler(40) + ["Puzzle.PutIntoPlay('04014', under_control=True)"], [f"Puzzle.Attack('{b}', '04014')"],
        {"degats": [[b, 0]]}),
    cas(f"{b} TEMOIN ranged : Hydra Mercenary contre U.S. Agent (Riposte 1) : il subit 1 degat",
        "Meme montage, attaquant ordinaire",
        GARDER(40) + [HEROS] + FOND + ["Puzzle.PutIntoPlay('04014', under_control=True)", "Puzzle.PutIntoPlay('01101')"],
        ["Puzzle.Attack('01101', '04014')"], {"degats": [["01101", 1]]}),
]
a, b = ECHANGE[41]
CAS += [
    cas(f"{b} ★ Reponse forcee : apres qu'elle t'attaque, la carte du dessus de TON deck est defaussee (deck de 3 cartes : le temoin suivant en perd 1 par la pioche, Korya en perd 2)",
        "« After Korya attacks you, discard the top card of each player's deck » (1 joueur)",
        reveler(41) + ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', '01088', '01088')"], [f"Puzzle.Attack('{b}')"],
        {"calc": [["len(j0.player_deck.GetAll())", 1]]}),
    cas(f"{b} TEMOIN : un sbire ordinaire (01101) qui attaque ne defausse rien du deck",
        "Meme montage, Hydra Mercenary (perte de 1 carte seulement, la pioche du tour)",
        GARDER(41) + [HEROS] + FOND + ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', '01088', '01088')", "Puzzle.PutIntoPlay('01101')"],
        ["Puzzle.Attack('01101')"], {"calc": [["len(j0.player_deck.GetAll())", 2]]}),
]
a, b = ECHANGE[42]
CAS += [
    cas(f"{b} Une fois vaincu : retourne Queen Veranke (sk189b -> Spider-Woman sk189a)",
        "« When Defeated: Flip Queen Veranke » : Veranke est sur sa face B quand Ch'Gra tombe",
        reveler(42) + ["Puzzle.Flip('sk189a')"], [f"Puzzle.Damage('{b}', 99)"], {"mechant": "sk189a", "hors_jeu": [b]}),
]
a, b = ECHANGE[43]
CAS += [
    cas(f"{b} ★ Ses attaques infligent des degats INDIRECTS : le defenseur n'encaisse rien",
        "« Hagar's attacks deal indirect damage » : Maria Hill defend, mais des degats indirects ne se defendent pas ; "
        "la defenseuse ne subit pas l'attaque",
        reveler(43) + ["Puzzle.PutIntoPlay('01067', under_control=True)"], [f"Puzzle.Attack('{b}', '01067')"],
        {"degats": [["01067", 0]]}),
]
a, b = ECHANGE[44]
CAS += [
    cas(f"{b} Villainous : mot-cle natif, une carte de boost a chaque activation",
        "« Villainous. (When this minion activates, give it a boost card.) » : `villainous` = 1",
        reveler(44), [], {"calc": [[f"par_id('{b}').IsVillainous()", True]]}),
]
a, b = ECHANGE[45]
CAS += [
    cas(f"{b} Quickstrike : en arrivant engage avec un heros, il attaque immediatement (au moins 2 degats)",
        "« Quickstrike. » : mot-cle natif ; Spider-Man (forme heros) subit l'attaque a l'engagement",
        reveler(45, incline=True), [], {"degats_identite_min": 2}),
]
a, b = ECHANGE[46]
CAS += [
    cas(f"{b} Incite 3 : a la revelation, 3 menaces sur le complot principal",
        "« Incite 3. (When this card is revealed, place 3 threat on the main scheme.) » : menace 0 -> 3",
        GARDER(46) + [HEROS] + FOND + ["Puzzle.SetThreat('sk192b', 0)", "Puzzle.Reveal('sk206')"], [],
        {"menace": [["sk192b", 3]], "en_jeu": [b]}),
]

# ======================================================================================================================
# Un allie CAMOUFLAGED maniganche en phase du mechant quand le joueur est en ALTER EGO
# ======================================================================================================================
SANS_JEU = ["Puzzle.SetThreat('sk192b', 0)"]
for n, sch in ((27, 1), (31, 2), (46, 3)):
    a, b = ECHANGE[n]
    CAS += [
        cas(f"{a} Phase du mechant, joueur en ALTER EGO : l'allie maniganche (SCH {sch}), subit 1 degat consequentiel et ne s'incline pas",
            "Livret p. 16 : « if the player's identity is in alter-ego form during the villain phase, the CAMOUFLAGED ally schemes at the "
            f"same time as minions after the villain's activation. It takes consequential damage after it schemes but does not exhaust » : "
            f"SCH {sch}, une pastille",
            GARDER(n) + FOND + SANS_JEU + [f"Puzzle.PutIntoPlay('{a}', under_control=True)"], ["Puzzle.RunVillainPhase()"],
            {"degats": [[a, 1]], "pret": [a], "calc": [["j0.IsAlterEgo()", True]]}),
    ]
a, b = ECHANGE[27]
CAS += [
    cas(f"{a} TEMOIN : joueur en forme HEROS, l'allie ne maniganche pas (aucun degat consequentiel)",
        "« if the player's identity is in alter-ego form » : en forme heros il reste tranquille",
        GARDER(27) + [HEROS] + FOND + SANS_JEU + [f"Puzzle.PutIntoPlay('{a}', under_control=True)"], ["Puzzle.RunVillainPhase()"],
        {"degats": [[a, 0]]}),
    cas(f"{a} Menace posee par la manigance de l'allie : SCH 1 de plus que sans lui (temoin : meme montage sans allie)",
        "Mesure : avec l'allie (menace = x) ; le temoin suivant mesure sans allie. escalade 1 + 1 (Veranke SKRULL) + 1 (allie IMPOSTOR) "
        "+ manigance du mechant + SCH de l'allie",
        GARDER(27) + FOND + SANS_JEU + [f"Puzzle.PutIntoPlay('{a}', under_control=True)"], ["Puzzle.RunVillainPhase()"],
        {"menace_min": [["sk192b", 7]]}),
    cas("sk192b TEMOIN de la manigance de l'allie : sans allie, la menace est inferieure de 2 (1 d'escalade supplementaire + 1 de SCH)",
        "Meme montage sans l'allie : le total s'arrete a 5",
        GARDER(27) + FOND + SANS_JEU, ["Puzzle.RunVillainPhase()"], {"menace": [["sk192b", 5]]}),
]

# ======================================================================================================================
# Complots principaux
# ======================================================================================================================
CAS += [
    cas("sk192b ★ Escalade : +1 par ennemi SKRULL et par allie IMPOSTOR : Veranke seule -> 1 (imprime) + 1 = 2",
        "Phase du mechant, joueur en forme heros (le mechant attaque) : menace 0 -> escalade 1[per_hero] + 1 (Veranke est SKRULL)",
        [HEROS] + FOND + SANS_JEU, ["Puzzle.RunVillainPhase()"], {"menace": [["sk192b", 2]]}),
    cas("sk192b ★ Escalade : avec UN allie IMPOSTOR en plus : 3",
        "+1 pour l'allie CAMOUFLAGED (trait IMPOSTOR)",
        GARDER(27) + [HEROS] + FOND + SANS_JEU + ["Puzzle.PutIntoPlay('sk208a', under_control=True)"], ["Puzzle.RunVillainPhase()"],
        {"menace": [["sk192b", 3]]}),
    cas("sk192b ★ Escalade : un SBIRE SKRULL compte (+1) mais pas comme « allie IMPOSTOR » ; Veranke + Skrull Warrior + allie = 4",
        "1 (imprime) + 3 : Veranke (SKRULL enemy), sk110 (SKRULL enemy), l'allie IMPOSTOR",
        GARDER(27) + [HEROS] + FOND + SANS_JEU + ["Puzzle.PutIntoPlay('sk208a', under_control=True)", "Puzzle.PutIntoPlay('sk110')"],
        ["Puzzle.RunVillainPhase()"], {"menace": [["sk192b", 4]]}),
    cas("sk192b Reponse forcee : fin du tour, moins de 2[per_hero] jetons de soupcon -> un allie CAMOUFLAGED au hasard sous le controle du joueur",
        "0 jeton < 2 (1 joueur) : l'allie du paquet (sk208a, seul) arrive en jeu sous le controle du joueur",
        GARDER(27) + [HEROS] + FOND, [], {"calc": [["ids(j0.allies.GetAll())", ["sk208a"]]]}, verifier="si_fin_de_tour"),
    cas("sk192b Reponse forcee : 1 jeton de soupcon (< 2) : l'allie arrive encore",
        "Strictement moins de 2[per_hero]",
        GARDER(27) + [HEROS] + FOND + ["Puzzle.Counter('sk194', 'suspicion', 1)"], [],
        {"calc": [["ids(j0.allies.GetAll())", ["sk208a"]]]}, verifier="si_fin_de_tour"),
    cas("sk192b Reponse forcee : TEMOIN, 2 jetons de soupcon (= 2[per_hero]) : aucun allie n'arrive",
        "« if there are LESS THAN 2[per_hero] »",
        GARDER(27) + [HEROS] + FOND + ["Puzzle.Counter('sk194', 'suspicion', 2)"], [],
        {"calc": [["ids(j0.allies.GetAll())", []], ["paquet.deck.GetSize()", 1]]}, verifier="si_fin_de_tour"),
    cas("sk192b Reponse forcee : 2 joueurs, seuil 2[per_hero] = 4 : 3 jetons laissent encore arriver un allie, sous le controle du joueur dont le tour finit",
        "Le joueur 1 termine son tour : l'allie va a LUI (pas au premier joueur)",
        GARDER(27) + [HEROS] + FOND + ["Puzzle.Counter('sk194', 'suspicion', 3)"], [],
        {"calc": [["ids(j1.allies.GetAll())", ["sk208a"]], ["ids(j0.allies.GetAll())", []]]}, verifier="si_fin_de_tour_j1", heros2="hawkeye"),
    cas("sk193a Une fois revele (Mistrust and Paranoia DEJA en jeu) : retire 2[per_hero] jetons de soupcon et ne cherche rien",
        "Complot 2A : si Mistrust est en jeu, retirer 2[per_hero] jetons (1 joueur : 2) ; 5 jetons -> 3 ; Mistrust reste en jeu",
        [HEROS] + FOND + ["Puzzle.Reveal('sk201')", "Puzzle.Counter('sk194', 'suspicion', 5)"], ["Puzzle.AdvanceMainScheme()"],
        {"soupcons": 3, "en_jeu": ["sk193b", "sk201"]}),
    cas("sk193a Une fois revele (Mistrust absent) : cherche Mistrust and Paranoia dans le deck rencontre et le REVELE, sans retirer de jeton",
        "Otherwise, find Mistrust and Paranoia and reveal it : le complot annexe est mis en jeu ; les 5 jetons restent",
        [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', 'sk201', '01101')",
         "Puzzle.Counter('sk194', 'suspicion', 5)"], ["Puzzle.AdvanceMainScheme()"],
        {"soupcons": 5, "en_jeu": ["sk193b", "sk201"]}),
    cas("sk193a Une fois revele : Mistrust cherche aussi dans la DEFAUSSE rencontre",
        "« find » = deck ET defausse",
        [HEROS] + FOND + ["Puzzle.CreateEncounterDiscardPile('sk201')"], ["Puzzle.AdvanceMainScheme()"],
        {"en_jeu": ["sk193b", "sk201"]}),
    cas("sk193b ★ Escalade X : 2 par ennemi SKRULL : Veranke + Skrull Warrior = 4",
        "Complot 2B : +X ou X = 2 x SKRULL enemies ; phase du mechant en forme heros, menace 0 -> 4",
        [HEROS] + FOND + ["Puzzle.AdvanceMainScheme()", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101', '01101', '01101')",
                          "Puzzle.PutIntoPlay('sk110')", "Puzzle.SetThreat('sk193b', 0)"],
        ["Puzzle.RunVillainPhase()"], {"menace": [["sk193b", 4]]}),
    cas("sk193b ★ Escalade X : Veranke seule : 2",
        "X = 2 x 1",
        [HEROS] + FOND + ["Puzzle.AdvanceMainScheme()", "Puzzle.SetThreat('sk193b', 0)"], ["Puzzle.RunVillainPhase()"],
        {"menace": [["sk193b", 2]]}),
    cas("sk193b Valeurs imprimees : objectif 14[per_hero], escalade 0 (X), menace de depart 1[per_hero]",
        "Lu sur le scan",
        [HEROS] + FOND + ["Puzzle.AdvanceMainScheme()"], [],
        {"menace": [["sk193b", 1 + 0]], "stats": [["sk193b", "printed_target_threat", 14]]}),
    cas("sk193b Reponse forcee : fin du tour, moins de 2[per_hero] jetons -> un SBIRE REVEALED du paquet, ENGAGE avec le joueur",
        "0 jeton : le sbire sk208b arrive engage avec le joueur dont le tour finit",
        GARDER(27) + [HEROS] + FOND + ["Puzzle.AdvanceMainScheme()"], [],
        {"calc": [["ids(j0.engaged_minions.GetAll())", ["sk208b"]]]}, verifier="si_fin_de_tour"),
    cas("sk193b Reponse forcee : TEMOIN 2 jetons de soupcon : aucun sbire",
        "Le seuil",
        GARDER(27) + [HEROS] + FOND + ["Puzzle.AdvanceMainScheme()", "Puzzle.Counter('sk194', 'suspicion', 2)"], [],
        {"calc": [["ids(j0.engaged_minions.GetAll())", []]]}, verifier="si_fin_de_tour"),
    cas("sk193b Dernier stade : un complot accompli = les joueurs PERDENT",
        "« If this stage is completed, the players lose the game » : regle native du dernier complot ; menace 14 atteinte",
        [HEROS] + FOND + ["Puzzle.AdvanceMainScheme()"], ["Puzzle.PlaceThreat('sk193b', 14)", "Puzzle.EndVillainPhase()"],
        {"calc": [["monde.is_game_over", True]]}),
]

# ======================================================================================================================
# L'environnement « Who Do You Trust? » : jetons de soupcon de concert avec la menace du complot principal
# ======================================================================================================================
CAS += [
    cas("sk194 Menace POSEE sur le complot principal (manigance du mechant) : autant de jetons de soupcon sont RETIRES",
        "Forced Interrupt : When any amount of threat is placed on the main scheme, remove an equal amount of suspicion counters ; "
        "Spider-Woman (alter ego du joueur) maniganche : 2 + 1 boost = 3 menaces, 5 jetons -> 2 ; menace 2 + 3 = 5",
        FOND + ["Puzzle.Counter('sk194', 'suspicion', 5)"], ["Puzzle.Scheme('sk189a')"],
        {"soupcons": 2, "menace": [["sk192b", 5]]}),
    cas("sk194 Menace posee : les jetons ne descendent pas sous 0",
        "1 jeton, 3 menaces : le jeton part, rien de plus",
        FOND + ["Puzzle.Counter('sk194', 'suspicion', 1)"], ["Puzzle.Scheme('sk189a')"],
        {"soupcons": 0, "menace": [["sk192b", 5]]}),
    cas("sk194 Menace RETIREE du complot principal (contre du heros) : autant de jetons de soupcon sont POSES",
        "Forced Interrupt : When any amount of threat is removed from the main scheme, place an equal amount of suspicion counters here : "
        "Spider-Man contre 1 (THW 1) : menace 2 -> 1, +1 jeton",
        [HEROS] + FOND, ["Puzzle.Thwart('01001a')"],
        {"soupcons": 1, "menace": [["sk192b", 1]]}),
    cas("sk194 Menace retiree : seule la menace REELLEMENT retiree compte (1 menace presente, retrait de 3 : 1 jeton de plus)",
        "Le complot n'a plus que 1 menace (SetThreat 1 retire 1 : 1 jeton) ; un retrait de 3 n'en retire que 1 : 2 jetons au total",
        [HEROS] + FOND + ["Puzzle.SetThreat('sk192b', 1)"], ["Puzzle.PlaceThreat('sk192b', -3)"],
        {"soupcons": 2, "menace": [["sk192b", 0]]}),
    cas("sk194 Menace posee sur un complot ANNEXE : aucun jeton retire (seul le complot PRINCIPAL compte)",
        "Hydra... Fulfill the Prophecy (sk200) revelee : sa propre menace n'enleve rien",
        [HEROS] + FOND + ["Puzzle.Counter('sk194', 'suspicion', 3)"], ["Puzzle.Reveal('sk200')"], {"soupcons": 3}),
]

# ======================================================================================================================
# Cartes de rencontre du set SECRET INVASION
# ======================================================================================================================
CAS += [
    # ---- sk195 Impostor (attachement, meme carte que sk098)
    cas("sk195 Impostor : un allie NON SKRULL (01002 Black Cat) devient un sbire SKRULL engage",
        "Meme texte que sk098 (Skrull Empire) : `TreatAttachedCardAsMinion` ; ennemis SKRULL : Veranke + l'allie traite en sbire",
        [HEROS] + FOND + ["Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Reveal('sk195')"],
        {"en_jeu": ["sk195"], "en_jeu_trait": [["SKRULL", 2]]}),
    cas("sk195 Impostor : les allies Impostor CAMOUFLAGED sont deja SKRULL, ils ne sont pas cibles : le mechant maniganche",
        "« non-SKRULL ally » ; seul allie = sk208a (SKRULL) : « Otherwise, the villain schemes » (Veranke CAMOUFLAGED, SCH 2 + boost)",
        GARDER(27) + FOND + SANS_JEU + ["Puzzle.PutIntoPlay('sk208a', under_control=True)"], ["Puzzle.Reveal('sk195')"],
        {"hors_jeu": ["sk195"], "menace_min": [["sk192b", 2]]}),
    cas("sk195 Impostor : sans allie, le mechant maniganche",
        "« Otherwise, the villain schemes » : menace posee par Veranke",
        FOND + SANS_JEU, ["Puzzle.Reveal('sk195')"], {"hors_jeu": ["sk195"], "menace_min": [["sk192b", 2]]}),
]
MINIONS = ["Puzzle.PutIntoPlay('sk110')", "Puzzle.PutIntoPlay('sk113')"]    # Skrull Warrior (4 PV), Skrull Commander (5 PV)
for cid, plus, effet in (("sk196", 2, {"pv_max": [["sk113", 7]]}), ("sk197", 3, {"stats": [["sk113", "attack", 5]]}),
                         ("sk198", 2, {"stats": [["sk113", "retaliate", 1]]})):
    base_atk = {"sk196": 4, "sk197": 5, "sk198": 4}[cid]
    CAS += [
        cas(f"{cid} Super-Skrull Enhancement : s'attache au sbire SKRULL qui a le plus de PV restants (Skrull Commander, 5 PV)",
            f"« Attach to the SKRULL minion with the most remaining hit points without another Super-Skrull Enhancement » ; "
            f"+{plus} ATQ (cle desc ATK+)" + (" et +2 PV" if cid == "sk196" else " et Riposte 1" if cid == "sk198" else ""),
            [HEROS] + FOND + MINIONS, [f"Puzzle.Reveal('{cid}')"],
            dict({"accroche_a": [[cid, "sk113"]], "stats": [["sk113", "attack", 2 + plus]]}, **(effet if cid != "sk197" else {}))),
        cas(f"{cid} Super-Skrull Enhancement : « without another » : une SECONDE amelioration va sur l'AUTRE sbire (Skrull Warrior)",
            "sk196 deja sur le Commander ; la carte revelee ensuite s'attache au Warrior",
            [HEROS] + FOND + MINIONS + (["Puzzle.Reveal('sk196')"] if cid != "sk196" else ["Puzzle.Reveal('sk198')"]),
            [f"Puzzle.Reveal('{cid}')"], {"accroche_a": [[cid, "sk110"]]}),
        cas(f"{cid} Super-Skrull Enhancement : sans sbire SKRULL, l'allie CAMOUFLAGED est RETOURNE puis la carte s'attache au sbire revele",
            "« If you cannot, choose a CAMOUFLAGED ally, flip that ally and attach this card to it »",
            GARDER(27) + [HEROS] + FOND + ["Puzzle.PutIntoPlay('sk208a', under_control=True)"], [f"Puzzle.Reveal('{cid}')"],
            {"accroche_a": [[cid, "sk208b"]], "hors_jeu": ["sk208a"], "calc": [["ids(j0.engaged_minions.GetAll())", ["sk208b"]]]}),
        cas(f"{cid} Super-Skrull Enhancement : ni sbire SKRULL ni allie CAMOUFLAGED : la carte gagne SURGE (revele la suivante)",
            "« Otherwise, this card gains surge » : Hydra Mercenary sur le dessus du deck est revelee",
            [HEROS] + FOND, [f"Puzzle.Reveal('{cid}')"],
            {"hors_jeu": [cid], "en_jeu": ["01101"], "calc": [["len(W.GetEncounterDeckCards(monde))", 2]]}),
        cas(f"{cid} Super-Skrull Enhancement ★ Boost : revelee APRES l'activation, elle s'attache au Skrull Commander",
            "« Reveal this card, after this activation ends » : Veranke attaque, la carte est retournee comme boost, puis revelee",
            [HEROS] + FOND + MINIONS, [f"Puzzle.Boost('{cid}')"], {"accroche_a": [[cid, "sk113"]]}),
    ]

CAS += [
    # ---- sk199 Chaos on the Battlefield
    cas("sk199 Chaos on the Battlefield : X = SCH total des IMPOSTOR en jeu (allie sk208a SCH 1 + sbire sk212b SCH 2 = 3) : 1 + 3 = 4 menaces",
        "« Place X additional threat here, where X is equal to the total SCH of all IMPOSTOR characters in play » ; menace de depart 1",
        GARDER(27, 31) + [HEROS] + FOND + ["Puzzle.Flip('sk212a')", "Puzzle.Reveal('sk212b')", "Puzzle.PutIntoPlay('sk208a', under_control=True)"],
        ["Puzzle.Reveal('sk199')"], {"menace": [["sk199", 4]]}),
    cas("sk199 Chaos on the Battlefield : sans IMPOSTOR, X = 0 : seulement la menace de depart (1)",
        "Aucun personnage IMPOSTOR",
        [HEROS] + FOND, ["Puzzle.Reveal('sk199')"], {"menace": [["sk199", 1]]}),
    cas("sk199 Chaos on the Battlefield : Incite 2 (+2 sur le complot principal) et icone Acceleration",
        "Incite 2 natif ; Acceleration : desc",
        [HEROS] + FOND + SANS_JEU, ["Puzzle.Reveal('sk199')"], {"menace": [["sk192b", 2]], "stats": [["sk199", "printed_acceleration_icon", 1]]}),
    # ---- sk200 Fulfill the Prophecy
    cas("sk200 Fulfill the Prophecy : chaque sbire SKRULL gagne Guard ET Patrol (Skrull Warrior, qui a deja Guard)",
        "« Each SKRULL minion gains guard and patrol » : sk113 Skrull Commander n'a ni l'un ni l'autre",
        [HEROS] + FOND + MINIONS, ["Puzzle.Reveal('sk200')"],
        {"calc": [["par_id('sk113').IsGuard()", True], ["par_id('sk113').IsPatrol()", True]]}),
    cas("sk200 Fulfill the Prophecy : TEMOIN sans la carte, le Commander n'a ni Guard ni Patrol",
        "Meme montage sans revelation",
        [HEROS] + FOND + MINIONS, [], {"calc": [["par_id('sk113').IsGuard()", False], ["par_id('sk113').IsPatrol()", False]]}),
    cas("sk200 Fulfill the Prophecy : Hinder 1[per_hero] et menace 3",
        "Hinder 1[per_hero] : mot-cle natif (la revelation ajoute 1 menace par joueur a la menace de depart 3)",
        [HEROS] + FOND, ["Puzzle.Reveal('sk200')"],
        {"menace": [["sk200", 4]], "stats": [["sk200", "printed_hinder", 1]]}),
    # ---- sk201 Mistrust and Paranoia
    cas("sk201 Mistrust and Paranoia : menace de depart 2 + 1 par personnage ami en jeu (2 joueurs : 2 identites -> 4)",
        "« Place 1 additional threat here for each friendly character in play »",
        [HEROS] + FOND, ["Puzzle.Reveal('sk201')"], {"menace": [["sk201", 4]]}, heros2="hawkeye"),
    cas("sk201 Mistrust and Paranoia : compte aussi les allies (1 joueur, identite + Black Cat = 2) : 2 + 2 = 4",
        "Les allies sont des personnages amis",
        [HEROS] + FOND + ["Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Reveal('sk201')"], {"menace": [["sk201", 4]]}),
    cas("sk201 Mistrust and Paranoia : un joueur ne peut PAS attaquer un sbire engage avec un AUTRE joueur",
        "Hydra Mercenary engage avec le joueur 1 ; Spider-Man (joueur 0) l'attaque : aucun degat",
        [HEROS] + FOND + ["Puzzle.Reveal('sk201')", "Puzzle.PutIntoPlay('01101', player=1)"], ["Puzzle.Attack('01001a')"],
        {"degats": [["01101", 0]]}, heros2="hawkeye", cibles=["01101"]),
    cas("sk201 Mistrust and Paranoia : TEMOIN, le meme sbire engage avec le joueur 0 est attaque normalement (2 degats)",
        "Montage identique, sbire du joueur 0",
        [HEROS] + FOND + ["Puzzle.Reveal('sk201')", "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('01001a')"],
        {"degats": [["01101", 2]]}, heros2="hawkeye", cibles=["01101"]),
    cas("sk201 Mistrust and Paranoia : un allie du joueur 1 ne peut PAS defendre contre un sbire engage avec le joueur 0",
        "Hydra Mercenary (engage avec J0) attaque J0, l'allie 01041 de J1 est declare defenseur : refuse, c'est le heros qui encaisse",
        [HEROS] + FOND + ["Puzzle.Exhaust('01001a')", "Puzzle.Reveal('sk201')", "Puzzle.PutIntoPlay('01101')",
                          "Puzzle.PutIntoPlay('01041', under_control=True, player=1)"],
        ["Puzzle.Attack('01101', '01041')"], {"degats_identite": 2}, heros2="hawkeye"),
    cas("sk201 TEMOIN : sans Mistrust, l'allie du joueur 1 defend bien contre le sbire du joueur 0",
        "Meme montage sans la carte : l'allie encaisse 1 degat, le heros 0",
        [HEROS] + FOND + ["Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01041', under_control=True, player=1)"],
        ["Puzzle.Attack('01101', '01041')"], {"degats_identite": 0}, heros2="hawkeye"),
    # ---- sk202 Arrival of Impostors
    cas("sk202 Arrival of Impostors ★ Boost : un allie CAMOUFLAGED arrive sous le controle du joueur attaque",
        "Veranke attaque le heros, la carte est retournee comme boost : « Put a CAMOUFLAGED ally ... under your control »",
        GARDER(27) + [HEROS] + FOND, ["Puzzle.Boost('sk202')"], {"calc": [["ids(j0.allies.GetAll())", ["sk208a"]]]}),
    # ---- sk203 Camouflage
    cas("sk203 Camouflage Une fois revelee (Queen Veranke) : la retourne SUR Spider-Woman et retire 3 jetons de soupcon",
        "« When Revealed (Queen Veranke): Flip Queen Veranke. Remove 3 suspicion counter(s) » : 5 jetons -> 2",
        ["Puzzle.Flip('sk189a')", HEROS] + FOND + ["Puzzle.Counter('sk194', 'suspicion', 5)"], ["Puzzle.Reveal('sk203')"],
        {"mechant": "sk189a", "soupcons": 2}),
    cas("sk203 Camouflage Une fois revelee (Spider-Woman) : Spider-Woman MANIGANCE, ne se retourne pas, ne touche pas aux jetons",
        "« When Revealed (Spider-Woman): Spider-Woman schemes » : SCH 2 + 1 boost",
        FOND + SANS_JEU + ["Puzzle.Counter('sk194', 'suspicion', 5)"], ["Puzzle.Reveal('sk203')"],
        {"mechant": "sk189a", "menace_min": [["sk192b", 2]]}),
    cas("sk203 Camouflage ★ Boost : Queen Veranke se retourne sur Spider-Woman APRES l'activation",
        "Queen Veranke attaque, la carte retournee en boost : « Flip Queen Veranke, after this activation ends »",
        ["Puzzle.Flip('sk189a')", HEROS] + FOND, ["Puzzle.Boost('sk203')"], {"mechant": "sk189a"}),
    cas("sk203 Camouflage ★ Boost : TEMOIN, Spider-Woman (deja camouflee) n'est pas retournee",
        "« Flip Queen Veranke » : seulement si c'est la face visible",
        [HEROS] + FOND, ["Puzzle.Boost('sk203')"], {"mechant": "sk189a"}),
    # ---- sk204 Glory to the Skrull Empire
    cas("sk204 Glory to the Skrull Empire : le mechant ET chaque sbire SKRULL engage avec toi recoivent une carte Robuste",
        "« Give the villain and each SKRULL minion engaged with you a tough status card » : sk110 est engage",
        [HEROS] + FOND + ["Puzzle.PutIntoPlay('sk110')"], ["Puzzle.Reveal('sk204')"],
        {"statuts": [["sk189a", "Tough"], ["sk110", "Tough"]]}),
    cas("sk204 Glory to the Skrull Empire : un sbire SKRULL engage avec un AUTRE joueur ne recoit rien",
        "« engaged with you »",
        [HEROS] + FOND + ["Puzzle.PutIntoPlay('sk110', player=1)"], ["Puzzle.Reveal('sk204')"],
        {"statuts": [["sk189a", "Tough"]], "statuts_absents": [["sk110", "Tough"]]}, heros2="hawkeye"),
    cas("sk204 Glory to the Skrull Empire : le mechant avait DEJA une carte Robuste : la carte gagne SURGE",
        "« If the villain already has a tough status card, this card gains surge » : Hydra Mercenary du dessus est revelee",
        [HEROS] + FOND + ["Puzzle.Tough('sk189a')"], ["Puzzle.Reveal('sk204')"],
        {"en_jeu": ["01101"], "calc": [["len(W.GetEncounterDeckCards(monde))", 2]]}),
    cas("sk204 Glory to the Skrull Empire : TEMOIN sans carte Robuste prealable, pas de surge",
        "La carte du dessus reste dans le deck",
        [HEROS] + FOND, ["Puzzle.Reveal('sk204')"], {"calc": [["len(W.GetEncounterDeckCards(monde))", 3]]}),
    cas("sk204 Glory to the Skrull Empire ★ Boost : le mechant recoit une carte Robuste",
        "Boost : « Give the villain a tough status card »",
        [HEROS] + FOND, ["Puzzle.Boost('sk204')"], {"statuts": [["sk189a", "Tough"]]}),
    # ---- sk205 Infiltration Ritual
    cas("sk205 Infiltration Ritual : un allie CAMOUFLAGED du paquet entre en jeu sous le controle d'UN joueur (1 joueur : lui)",
        "« Put a CAMOUFLAGED ally at random ... under any player's control »",
        GARDER(27) + [HEROS] + FOND, ["Puzzle.Reveal('sk205')"], {"calc": [["ids(j0.allies.GetAll())", ["sk208a"]]]}),
    cas("sk205 Infiltration Ritual : 2 joueurs, le joueur qui revele DESIGNE le joueur : l'allie arrive sous le controle de l'un des deux",
        "« under ANY player's control » : un seul allie, chez j0 ou j1",
        GARDER(27) + [HEROS] + FOND, ["Puzzle.Reveal('sk205')"],
        {"calc": [["len(j0.allies.GetAll()) + len(j1.allies.GetAll())", 1]]}, heros2="hawkeye"),
    cas("sk205 Infiltration Ritual : paquet et defausse vides -> la carte gagne SURGE",
        "« If you cannot, this card gains surge »",
        GARDER() + [HEROS] + FOND, ["Puzzle.Reveal('sk205')"],
        {"en_jeu": ["01101"], "calc": [["ids(j0.allies.GetAll())", []], ["len(W.GetEncounterDeckCards(monde))", 2]]}),
    cas("sk205 Infiltration Ritual ★ Boost : retire 3 jetons de soupcon",
        "5 jetons ; Veranke attaque le heros (+1 jeton par sa Reponse forcee), le Boost en retire 3 : 3",
        [HEROS] + FOND + ["Puzzle.Counter('sk194', 'suspicion', 5)"], ["Puzzle.Boost('sk205')"], {"soupcons": 3}),
    # ---- sk206 Invasion Fleet
    cas("sk206 Invasion Fleet : CHAQUE joueur recoit un sbire REVEALED du paquet, engage avec LUI (2 joueurs)",
        "« Each player puts a REVEALED minion at random from the IMPOSTOR deck into play engaged with them » ; deux cartes dans le paquet",
        GARDER(27, 28) + [HEROS] + FOND, ["Puzzle.Reveal('sk206')"],
        {"calc": [["len(j0.engaged_minions.GetAll())", 1], ["len(j1.engaged_minions.GetAll())", 1],
                  ["sorted(ids(j0.engaged_minions.GetAll()) + ids(j1.engaged_minions.GetAll()))", ["sk208b", "sk209b"]]]}, heros2="hawkeye"),
    cas("sk206 Invasion Fleet ★ Boost : un sbire REVEALED du paquet, engage avec le joueur attaque",
        "Veranke attaque le heros, la carte est retournee comme boost",
        GARDER(27) + [HEROS] + FOND, ["Puzzle.Boost('sk206')"], {"calc": [["ids(j0.engaged_minions.GetAll())", ["sk208b"]]]}),
    # ---- sk207 Revelation
    cas("sk207 Revelation : retourne l'allie CAMOUFLAGED qui a le PLUS de PV RESTANTS (l'autre, blesse, reste allie)",
        "sk208a (4 PV pleins) et sk209a (3 PV, 2 degats -> 1 restant) : c'est le premier qui est retourne",
        GARDER(27, 28) + [HEROS] + FOND + ["Puzzle.PutIntoPlay('sk208a', under_control=True)", "Puzzle.PutIntoPlay('sk209a', under_control=True)",
                                           "Puzzle.Damage('sk209a', 2)"],
        ["Puzzle.Reveal('sk207')"],
        {"calc": [["ids(j0.engaged_minions.GetAll())", ["sk208b"]], ["ids(j0.allies.GetAll())", ["sk209a"]]]}),
    cas("sk207 Revelation : sans allie CAMOUFLAGED, un sbire REVEALED du paquet vient engager le joueur",
        "« If you cannot, put a REVEALED minion at random ... engaged with you »",
        GARDER(27) + [HEROS] + FOND, ["Puzzle.Reveal('sk207')"], {"calc": [["ids(j0.engaged_minions.GetAll())", ["sk208b"]]]}),
    cas("sk207 Revelation ★ Boost : retourne UN allie CAMOUFLAGED que tu controles, APRES l'activation",
        "Veranke attaque, la carte est retournee comme boost ; ensuite l'allie sk208a passe sur sa face sbire",
        GARDER(27) + [HEROS] + FOND + ["Puzzle.PutIntoPlay('sk208a', under_control=True)"], ["Puzzle.Boost('sk207')"],
        {"calc": [["ids(j0.engaged_minions.GetAll())", ["sk208b"]], ["ids(j0.allies.GetAll())", []]]}),
]

VERIFICATIONS = r'''
def _si_ids(faces):
    return [getattr(f.paper, "card_id", None) for f in faces]

def _si_paquet(monde):
    return monde.scenario_decks.get("ImpostorDeck")

_SI_PROPRES = {"paquet", "defausse_paquet", "dans_defausse_paquet", "soupcons", "mechant", "calc", "stats"}

def _si_espace(monde, aides):
    from game.operate.worlds import Worlds
    def par_id(card_id):
        return aides["par_id"](monde, card_id)
    def soupcons():
        env = par_id("sk194")
        return env.GetCounters('suspicion') if env is not None else None
    def villain():
        return Worlds.GetAllVillains(monde)[0]
    def complot():
        return Worlds.GetAllMainSchemes(monde)[0]
    from cards.pack.skrull_menace.secret_invasion import SchAllie
    return {
        "SchAllie_": SchAllie, "monde": monde, "Worlds": Worlds, "j0": monde.players[0],
        "j1": monde.players[1] if len(monde.players) > 1 else None,
        "ids": _si_ids, "par_id": par_id, "W": Worlds, "soupcons": soupcons, "villain": villain, "complot": complot,
        "paquet": _si_paquet(monde),
    }

def si_etat(monde, aides):
    """Etat de Secret Invasion : paquet IMPOSTOR, jetons de soupcon, Veranke, expressions libres (`calc`) ; delegue le reste
    (en_jeu, hors_jeu, degats, menace, accroche_a, statuts, pv_max...) a etat_attendu."""
    from game.operate.worlds import Worlds
    attendu = aides["cas"].get("attendu") or {}
    soucis = []
    paquet = _si_paquet(monde)
    if any(k in attendu for k in ("paquet", "defausse_paquet", "dans_defausse_paquet")):
        if paquet is None or not paquet.initialize:
            soucis.append("le paquet IMPOSTOR n'existe pas")
        else:
            if "paquet" in attendu and paquet.deck.GetSize() != attendu["paquet"]:
                soucis.append(f"paquet = {paquet.deck.GetSize()} carte(s) (attendu {attendu['paquet']})")
            if "defausse_paquet" in attendu and paquet.discard_pile.GetSize() != attendu["defausse_paquet"]:
                soucis.append(f"defausse du paquet = {paquet.discard_pile.GetSize()} {_si_ids(paquet.discard_pile.GetAll())} "
                              f"(attendu {attendu['defausse_paquet']})")
            for i in attendu.get("dans_defausse_paquet") or []:
                if i not in _si_ids(paquet.discard_pile.GetAll()):
                    soucis.append(f"{i} absent de la defausse du paquet {_si_ids(paquet.discard_pile.GetAll())}")
    if "mechant" in attendu:
        v = Worlds.GetAllVillains(monde)[0]
        reel = getattr(v.paper, "card_id", None)
        if reel != attendu["mechant"]:
            soucis.append(f"mechant visible = {reel} (attendu {attendu['mechant']})")
    if "soupcons" in attendu:
        env = aides["par_id"](monde, "sk194")
        n = env.GetCounters('suspicion') if env is not None else None
        if n != attendu["soupcons"]:
            soucis.append(f"jetons de soupcon = {n} (attendu {attendu['soupcons']})")
    for card_id, attr, valeur in attendu.get("stats") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (stat {attr})")
            continue
        reel = getattr(face, attr, None)
        if reel != valeur:
            soucis.append(f"{card_id}.{attr} = {reel} (attendu {valeur})")
    espace = _si_espace(monde, aides)
    for expression, valeur in attendu.get("calc") or []:
        try:
            reel = eval(expression, espace)
        except Exception as exc:
            soucis.append(f"calc « {expression} » : {type(exc).__name__}: {exc}")
            continue
        if reel != valeur:
            soucis.append(f"« {expression} » = {reel!r} (attendu {valeur!r})")
    reste = {k: v for k, v in attendu.items() if k not in _SI_PROPRES}
    if reste:
        inconnues = sorted(set(reste) - CLES_ETAT_ATTENDU)
        if inconnues:
            return False, f"cle(s) inconnue(s) : {inconnues}"
        sauve = aides["cas"]["attendu"]
        aides["cas"]["attendu"] = reste
        try:
            ok, msg = etat_attendu(monde, aides)
        finally:
            aides["cas"]["attendu"] = sauve
        if not ok:
            soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"

def _si_fin_de_tour_de(monde, aides, rang):
    """Envoie la fin du tour du joueur `rang` (comme gorr_berserker_fin_de_tour) puis mesure l'etat."""
    from game.message import Message
    joueur = monde.players[rang]
    fin = Message.WhenPlayerTurnEnd(joueur, 1)
    Message.AfterPlayerTurnEnd(joueur, fin).Send()
    return si_etat(monde, aides)

def si_fin_de_tour(monde, aides):
    return _si_fin_de_tour_de(monde, aides, 0)

def si_fin_de_tour_j1(monde, aides):
    return _si_fin_de_tour_de(monde, aides, 1)
'''
