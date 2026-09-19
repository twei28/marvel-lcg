"""Bloc 3P Fear No Evil : Protection Racket (coordinateur). Cas [fne3p] + verificateur fne3p_racket."""
import io, json
p='/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src/tools/test_capacites.py'
s=io.open(p,encoding='utf8').read()
HERO="Puzzle.ChangeForm('01001b')"
PLAT=["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', '01186', '01186')"]
SPH='protection_racket_hammerhead'
def cas(nom, pourquoi, scenario, declencher, attendu=None, verifier="fne3p_racket", mise=None, **extra):
    d={"nom": nom, "pourquoi": pourquoi, "scenario": scenario, "heros": "spider_man",
       "mise_en_place": mise or [], "declencher": declencher, "verifier": verifier,
       "main_exclusive": ["01088"]}  # jamais Great Responsibility dans la main du pilote (RECETTES §7ter)
    d.update(extra)
    if attendu is not None: d["attendu"]=attendu
    return d
CAS=[
 cas("60134a Protection Racket 1A [fne3p] — mise en place : le joueur choisit son complot (premiere option : Battle in the Bodega), les quatre autres restent de cote",
     "WhenCardSetup('This') : candidats = cette carte + les 4 mises de cote ; AskChooseFace, le pilote prend la premiere ; proprietaire_racket pose sur la carte", SPH,
     [], {"nb": 1, "en_jeu": ["60134b"], "de_cote": 4, "proprietaire": 0}),
 dict(cas("60134a Protection Racket 1A [fne3p] (expert) — mise en place au hasard : un seul complot en jeu, quatre de cote",
     "Rand.RandomChoice en expert", SPH+"_expert", [], {"nb": 1, "de_cote": 4, "proprietaire": 0}), ),
 cas("60134b Protection Racket [fne3p] — le vilain manigance contre le joueur : la menace tombe sur SON complot (0 + 2)",
     "GettingMainScheme -> complot de world.current_player (article FFG : l'ennemi ne pose que sur le complot du joueur vise)", SPH,
     ["Puzzle.Scheme('60086')"], {"menace_joueur": 2}, mise=PLAT),
 cas("60134b Battle in the Bodega [fne3p] — le vilain attaque le heros : 1 degat au vilain et 1 menace ; limite une fois par phase (seconde attaque : rien de plus)",
     "AfterUnitAttackUnit(Enemy, personnage de cette aire) + LimitOncePerPhase hors expert", SPH,
     ["Puzzle.Attack('60086')","Puzzle.Attack('60086')"], {"menace": [["60134b", 1]], "degats": [["60086", 1]]},
     mise=[HERO,"Puzzle.Exhaust('01001a')"]+PLAT),
 cas("60136b Hung Out to Dry [fne3p] — un personnage entre en jeu dans cette aire : 1 degat et 1 menace",
     "Puzzle.Reveal('60136a') met un second complot en jeu pour le joueur (WhenThisRevealed pose le proprietaire) ; AfterCardEnterPlay(Unit2 de cette aire)", SPH,
     ["Puzzle.PutIntoPlay('01020', under_control=True)"], {"en_jeu": ["60136b"], "degats": [["01020", 1]], "menace": [["60136b", 1]]},
     mise=[HERO,"Puzzle.Reveal('60136a')"]+PLAT),
 cas("60135b Bull in a China Shop [fne3p] — degats excedentaires sur un allie de cette aire : autant de menace (5 sur 3 PV = 2)",
     "AfterUnitTookDamage.excess_damage", SPH,
     ["Puzzle.Damage('01020', 5)"], {"en_jeu": ["60135b"], "menace": [["60135b", 2]]},
     mise=[HERO,"Puzzle.Reveal('60135a')","Puzzle.PutIntoPlay('01020', under_control=True)"]+PLAT),
 cas("60137b Pawn Shop Showdown [fne3p] — une amelioration entre en jeu dans cette aire : 1 menace",
     "AfterCardEnterPlay(Upgrade du proprietaire) ; la reduction de cout du premier upgrade du round n'est pas mesuree (jeu depuis la main)", SPH,
     ["Puzzle.PutIntoPlay('01008', under_control=True)"], {"en_jeu": ["60137b"], "menace": [["60137b", 1]]},
     mise=[HERO,"Puzzle.Reveal('60137a')"]+PLAT),
 cas("60138b A Slice of the Pizza Dough [fne3p] — le heros vainc un sbire : il soigne 1 degat et 1 menace ici",
     "AfterUnitDefeatedUnit(tueur de cette aire) + HealAll(1) ; Beetle (5 PV, sans quickstrike) blesse a 4 ; identite : 2 - 1 (soin) = 1", SPH,
     ["Puzzle.PutIntoPlay('60197')","Puzzle.Damage('60197', 4)","Puzzle.Damage('01001a', 2)","Puzzle.Attack('01001a', '60197')"], {"en_jeu": ["60138b"], "hors_jeu": ["60197"], "degats_identite": 1, "menace": [["60138b", 1]]},
     mise=[HERO,"Puzzle.Reveal('60138a')","Puzzle.EmptyEncounterDeck()"]+PLAT),
 cas("60139 Shop Proprietor [fne3p] — revele : entre en jeu sous ton controle et surge ; quand il quitte le jeu : 4 menaces sur ton complot",
     "WhenRevealed PutIntoPlay(under_control) + ThisCardGainSurge ; WhenCardLeavePlay(This) -> ComplotDuJoueur ; 5 = 4 + 1 de Battle in the Bodega (le surge revele Assault : le vilain attaque un personnage de cette aire)", SPH,
     ["Puzzle.Reveal('60139')","Puzzle.Discard('60139')"], {"hors_jeu": ["60139"], "menace_joueur": 5, "carte_du_surge": "01187"},
     mise=[HERO,"Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186', '01186', '01187')"]),
 cas("60140 Man-Bull [fne3p] — attaque defendue par Hellcat (3 PV) : 4 - 3 = 1 menace sur le complot",
     "AfterUnitAttackEnd.excess_damage -> PlaceThreatOnSchemes('MainScheme')", SPH,
     ["Puzzle.Attack('60140', '01020')"], {"hors_jeu": ["01020"], "menace_joueur": 1},
     mise=[HERO,"Puzzle.EmptyEncounterDeck()","Puzzle.PutIntoPlay('60140')","Puzzle.PutIntoPlay('01020', under_control=True)"]+PLAT),
 cas("60141 Change of Venue [fne3p] — le complot du joueur (4 menaces) est echange contre un complot mis de cote au hasard, qui recoit les 4 menaces ; surge",
     "EchangerLeComplot : SetAside de l'ancien, Reveal du nouveau (proprietaire pose), menace reposee", SPH,
     ["Puzzle.SetThreat('60134b', 4)","Puzzle.Reveal('60141')"], {"nb": 1, "hors_jeu": ["60134b"], "menace_joueur": 4, "de_cote": 4, "carte_du_surge": "01187"},
     mise=[HERO,"Puzzle.EmptyEncounterDeck()","Puzzle.CreateEncounterDeck('01186', '01186', '01187')"]),
 cas("60140 Man-Bull [fne3p] (expert) — carte BOOST de l'attaque de Hammerhead II (ATK 2) sur Hellcat a 1 PV : 1 degat en exces = 1 menace sur le complot du joueur (Hung Out to Dry, tire au hasard en expert)",
     "WhenCardBecomeBoost -> RegisterTemp(AfterUnitAttackEnd Temp0, unregister_after_exec=True) ; TypeError avale avant le 18/09/2026 (autoplay)", SPH + "_expert",
     ["Puzzle.Boost('60140')","Puzzle.Damage('01020', 2)","Puzzle.Attack('60087', '01020')"], {"hors_jeu": ["01020"], "menace_joueur": 1},
     mise=[HERO,"Puzzle.EmptyEncounterDeck()","Puzzle.PutIntoPlay('01020', under_control=True)"]+PLAT),
 cas("60135b Bull in a China Shop [fne3p] — contre-cas : le VILAIN vaincu (stade I) n'est dans l'aire de personne : pas de menace, pas de plantage, stade II en jeu",
     "DansCetteAire : Enemy -> False (GetControlByPlayer posait un assert sur le vilain, autoplay 18/09/2026)", SPH,
     ["Puzzle.Damage('60086', 20)"], {"en_jeu": ["60087"], "menace_joueur": 0},
     mise=[HERO,"Puzzle.Reveal('60135a')","Puzzle.EmptyEncounterDeck()"]+PLAT),
]
DEBUT="    # ------------------------------------------------------------------------\n    # Pack officiel « fne » — bloc 3P"
FIN="    # ---- fin du bloc 3P fne ----\n"
bloc = DEBUT + " : Protection Racket (coordinateur, 18/09/2026). Filtre : \"[fne3p]\". Genere par scratchpad/b3/gen_cas_fne_p.py.\n    # ------------------------------------------------------------------------\n"
for c in CAS:
    bloc += "    " + json.dumps(c, ensure_ascii=False, indent=4).replace("\n", "\n    ").replace(": true", ": True").replace(": false", ": False") + ",\n"
bloc += FIN
if DEBUT in s:
    i=s.index(DEBUT); j=s.index(FIN, i)+len(FIN); s=s[:i]+bloc+s[j:]
else:
    ancre="    # ------------------------------------------------------------------------\n    # Pack officiel « fne » — bloc 2"
    assert ancre in s; s=s.replace(ancre, bloc+ancre, 1)
VERIFS='''
# ---------------------------------------------------------------- pack fne (bloc 3P)
def fne3p_racket(monde, aides):
    """Protection Racket : `nb` complots Protection Racket en jeu, `de_cote`
    mis de cote, `menace_joueur` sur le complot du joueur 0, `proprietaire`
    du complot en jeu ; le reste passe a etat_attendu."""
    from game.operate.worlds import Worlds
    from game.card.face.card_type import MainScheme
    effet = type("EffetFactice", (), {"world": monde})()
    attendu = dict(aides["cas"].get("attendu") or {})
    soucis = []
    en_jeu = [s for s in Worlds.GetAllMainSchemes(monde) if s.paper.set_name == "Protection Racket"]
    if "nb" in attendu and len(en_jeu) != attendu.pop("nb"):
        soucis.append(f"{len(en_jeu)} complot(s) Protection Racket en jeu : {[s.paper.card_id for s in en_jeu]}")
    if "de_cote" in attendu:
        de_cote = [f for f in Worlds.GetSetAsideAreaCards(effet) if MainScheme.IsType(f) and f.paper.set_name == "Protection Racket"]
        voulu = attendu.pop("de_cote")
        if len(de_cote) != voulu:
            soucis.append(f"{len(de_cote)} complot(s) mis de cote (attendu {voulu}) : {[f.paper.card_id for f in de_cote]}")
    joueur0 = monde.players[0]
    du_joueur = [s for s in en_jeu if getattr(s.card, "proprietaire_racket", None) == joueur0.player_id]
    if "proprietaire" in attendu:
        attendu.pop("proprietaire")
        if not du_joueur:
            soucis.append(f"aucun complot n'appartient au joueur 0 (proprietaires = {[getattr(s.card, 'proprietaire_racket', None) for s in en_jeu]})")
    if "menace_joueur" in attendu:
        voulu = attendu.pop("menace_joueur")
        if not du_joueur:
            soucis.append("menace_joueur : aucun complot du joueur 0")
        elif du_joueur[0].threat != voulu:
            soucis.append(f"menace sur le complot du joueur = {du_joueur[0].threat} (attendu {voulu}) [{du_joueur[0].paper.card_id}]")
    if attendu:
        aides2 = dict(aides); aides2["cas"] = dict(aides["cas"], attendu=attendu)
        if attendu.get("carte_du_surge"):
            ok, msg = surge_carte(monde, aides2) if "surge_carte" in globals() else (True, "")
            if not ok: soucis.append(msg)
            attendu.pop("carte_du_surge"); aides2["cas"] = dict(aides["cas"], attendu=attendu)
        if attendu:
            ok, msg = etat_attendu(monde, aides2)
            if not ok: soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"racket ok : en jeu {[s.paper.card_id for s in en_jeu]}, joueur 0 -> {[s.paper.card_id for s in du_joueur]}"

'''
MARQ="# ---------------------------------------------------------------- pack fne (bloc 3P)"
FINV = "# ---- fin des verificateurs du bloc 3P ----\n"
VERIFS = VERIFS.rstrip("\n") + "\n\n" + FINV
# ⚠ On ne remplace QUE sa propre section (du marqueur au marqueur de fin) :
# « du marqueur a def etat_attendu » effacait les verificateurs des autres
# blocs poses apres (6 verificateurs fne4_ perdus deux fois le 18/09/2026).
if MARQ in s:
    i = s.index(MARQ)
    j = s.index(FINV, i) + len(FINV) if FINV in s[i:] else s.index("def etat_attendu(monde, aides):", i)
    s = s[:i] + VERIFS.lstrip("\n") + "\n" + s[j:]
else:
    j = s.index("def etat_attendu(monde, aides):")
    s = s[:j] + VERIFS.lstrip("\n") + "\n" + s[j:]
io.open(p,'w',encoding='utf8').write(s)
import ast; ast.parse(s)
print("cas [fne3p]:", len(CAS), "; syntaxe OK")
