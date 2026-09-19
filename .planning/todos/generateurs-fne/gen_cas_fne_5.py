"""Bloc 5 Fear No Evil : campagne (environnements Completed/Failed, marques, Mary, cartes retirees). Cas [fne5]."""
import io, json
p='/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src/tools/test_capacites.py'
s=io.open(p,encoding='utf8').read()
SA='art_museum_heist_hammerhead'
def cas(nom, pourquoi, carnet, attendu, verifier="etat_attendu", scenario=SA, mise=None, declencher=None, **extra):
    d={"nom": nom, "pourquoi": pourquoi, "scenario": scenario, "heros": "spider_man",
       "mise_en_place": mise or [], "declencher": declencher or [], "verifier": verifier,
       "carnet": carnet, "attendu": attendu, "main_exclusive": ["01088"]}
    d.update(extra)
    return {k: v for k, v in d.items() if v is not None}
CAS=[
 cas("60205a Art Museum Heist (Completed) [fne5] — carnet : affaire completee -> l'environnement entre en jeu, chaque identite est robuste",
     "MettreLesEnvironnements (WhenCampaignSetup) + AfterGameSetup : GiveStatus Tough", {"Completed Scenarios": "art_museum_heist"},
     {"en_jeu": ["60205a"], "statuts": [["01001b","Tough"]]}),
 cas("60205b Art Museum Heist (Failed) [fne5] — carnet : affaire echouee -> face Failed, le joueur choisit etourdi (premiere option)",
     "MettreLesEnvironnements face b + ChooseAbilities", {"Failed Scenarios": "art_museum_heist"},
     {"en_jeu": ["60205b"], "hors_jeu": ["60205a"], "statuts": [["01001b","Stunned"]]}),
 dict(cas("60205b Art Museum Heist (Failed) [fne5] (expert) — etourdi ET desoriente",
     "Worlds.IsExpert -> les deux statuts", {"Failed Scenarios": "art_museum_heist"},
     {"en_jeu": ["60205b"], "statuts": [["01001b","Stunned"],["01001b","Confused"]]}, scenario=SA+"_expert"), ),
 cas("Marques de progression [fne5] — 2 marques sur Art Museum Heist : +2 menaces sur le complot a la mise en place (1 + 2)",
     "MarquesDeLAffaire : 1 menace par marque (2 en expert)", {"Progress: art_museum_heist": "2"},
     {"menace": [["60121b", 3]]}),
 dict(cas("Marques de progression [fne5] (expert) — 2 marques : +4 (1 + 4)",
     "2 menaces par marque en expert", {"Progress: art_museum_heist": "2"},
     {"menace": [["60121b", 5]]}, scenario=SA+"_expert"), ),
 cas("60210a Typhoid Mary (alliee) [fne5] — carnet : Trust Established sans Mary Defeated -> l'alliee entre en jeu sous ton controle",
     "MaryWalker (WhenCampaignSetup) : GenerateCard('60210a,60210b') + PutIntoPlay(under_control)", {"Trust Established?": "1"},
     {"en_jeu": ["60210a"]}),
 cas("60210a Typhoid Mary (alliee) [fne5] — contre-cas : Mary Defeated coche -> pas d'alliee",
     "condition du livret, etape 13", {"Trust Established?": "1", "Mary Defeated?": "1"},
     {"hors_jeu": ["60210a"]}),
 cas("60210a Typhoid Mary (alliee) [fne5] — apres que tu reveles un sbire : soignee et retournee (Bloody Mary)",
     "WhenCardRevealed(Minion) par son controleur + HealHealth('All') + card.Flip", {"Trust Established?": "1"},
     {"en_jeu": ["60210b"], "hors_jeu": ["60210a"], "degats": [["60210b", 0]]},
     mise=["Puzzle.EmptyEncounterDeck()","Puzzle.Damage('60210a', 2)"], declencher=["Puzzle.Reveal('60182')"]),
 cas("Cartes retirees de la campagne [fne5] — carnet : Black Cat retiree -> hors du deck de Spider-Man (retiree du jeu)",
     "RetirerLesCartesRetirees : titre du carnet -> Faces.RemoveAllFromGame", {"Allies removed from the campaign": "Black Cat"},
     {"retirees": ["01002"]}, verifier="fne_retirees"),
 cas("60206a The Getaway (Completed) [fne5] — en jeu ; apres les mulligans, chercher une amelioration (may) : la main compte 7 cartes",
     "ChercherEnMain(Upgrade) : SearchForCard(may) + AddToHand", {"Completed Scenarios": "the_getaway"},
     {"en_jeu": ["60206a"], "taille_main": 7, "en_main": ["01008"]}, main_exclusive=None, cibles=["01008"]),
 cas("60207b Protection Racket (Failed) [fne5] — en jeu ; chaque joueur defausse 1 carte de sa main (6 -> 5)",
     "DefausserDeLaMain(1)", {"Failed Scenarios": "protection_racket"},
     {"en_jeu": ["60207b"], "taille_main": 5}, main_exclusive=None),
 cas("60209b Stop the Presses! (Failed) [fne5] — en jeu ; 1 carte rencontre distribuee face cachee",
     "DealEncounterCards(1)", {"Failed Scenarios": "stop_the_presses"},
     {"distribuees": 1, "en_jeu": ["60209b"]}, verifier="ares_cartes_rencontre_distribuees"),
 cas("60209a Stop the Presses! (Completed) [fne5] — en jeu ; chaque joueur met un soutien DAILY BUGLE en jeu sous son controle",
     "GenerateCard des 4 soutiens moins les retires, choix, PutIntoPlay(under_control)", {"Completed Scenarios": "stop_the_presses"},
     {"en_jeu": ["60209a"], "en_jeu_trait": [["DAILY BUGLE", 1]]}),
 cas("60208b The Raft Breakout (Failed) [fne5] — en jeu ; les six prisonniers du Raft sont meles au deck rencontre",
     "GenerateCard + ShuffleAllTo('EncounterDeck')", {"Failed Scenarios": "the_raft_breakout"},
     {"en_jeu": ["60208b"], "dans_deck_rencontre": ["60144","60149"]}),
 cas("Environnements multiples [fne5] — deux affaires completees et une echouee : trois environnements en jeu sur la bonne face",
     "MettreLesEnvironnements boucle sur le carnet", {"Completed Scenarios": "the_getaway;the_raft_breakout", "Failed Scenarios": "protection_racket"},
     {"en_jeu": ["60206a","60208a","60207b"], "hors_jeu": ["60206b","60208b","60207a","60205a","60209a"]}),
 # --- Les capacites de campagne sur les AUTRES manigances (branchees le 18/09/2026 apres les blocs 3-4) ---
 cas("The Getaway (campagne) [fne5] — carnet : Art Museum Heist completee -> 60205a entre en jeu sur The Getaway aussi",
     "CapacitesDeCampagne('the_getaway') sur 60128a : MettreLesEnvironnements", {"Completed Scenarios": "art_museum_heist"},
     {"en_jeu": ["60205a"], "statuts": [["01001b","Tough"]]}, scenario="the_getaway_hammerhead"),
 cas("The Getaway (campagne) [fne5] — 2 marques : Jackknifed Tanker Truck est revele avec 1 menace de plus (2 + Hinder 1 + 1 marque = 4)",
     "MarquesDeLAffaire('the_getaway') : FindAndReveal + PlaceThreat", {"Progress: the_getaway": "2"},
     {"en_jeu": ["60131"], "menace": [["60131", 4]]}, scenario="the_getaway_hammerhead"),
 cas("The Raft Breakout (campagne) [fne5] — 2 marques : chaque prisonnier revele au Setup est robuste et recoit 1 carte boost",
     "MarquesDeLAffaire('the_raft_breakout') : GiveStatus Tough + GiveFacedownBoostCards", {"Progress: the_raft_breakout": "2"},
     {"trait": "PRISONER", "type": "Minion", "statut": "Tough", "boost": 1}, verifier="fne5_trait", scenario="the_raft_breakout_hammerhead"),
 cas("Stop the Presses! (campagne) [fne5] — 1 marque : le soutien DAILY BUGLE du joueur perd 1 compteur stamina (3 -> 2)",
     "MarquesDeLAffaire('stop_the_presses') : RemoveCountersOn stamina", {"Progress: stop_the_presses": "1"},
     {"trait": "DAILY BUGLE", "type": "Support", "compteur": ["stamina", 2]}, verifier="fne5_trait", scenario="stop_the_presses_hammerhead"),
 cas("Protection Racket (campagne, 2 joueurs) [fne5] — deux complots 1A, mais UN SEUL environnement 60205a entre en jeu",
     "garde _premier_complot sur CapacitesDeCampagne('protection_racket')", {"Completed Scenarios": "art_museum_heist"},
     {"exemplaires": ["60205a", 1]}, verifier="fne5_trait", scenario="protection_racket_hammerhead", heros2="black_panther"),
 cas("Protection Racket (campagne) [fne5] — 1 marque : 1 menace de plus sur le complot du joueur",
     "MarquesDeLAffaire('protection_racket') : PlaceThreatOnSchemes sur chaque complot", {"Progress: protection_racket": "1"},
     {"menace_joueur": 1}, verifier="fne3p_racket", scenario="protection_racket_hammerhead"),
 cas("Kingpin (campagne) [fne5] — 3 affaires completees : les trois environnements en jeu, chaque sbire en jeu robuste",
     "CapacitesDeCampagneKingpin sur 60161a : MettreLesEnvironnements + MarquesKingpin(3)", {"Completed Scenarios": "art_museum_heist;the_getaway;protection_racket"},
     {"en_jeu": ["60205a","60206a","60207a"], "trait": "", "type": "Minion", "statut": "Tough"}, verifier="fne5_trait", scenario="kingpin_fne"),
 cas("Kingpin (campagne) [fne5] — 4 affaires completees : James Wesley est trouve et revele (attache a Kingpin)",
     "MarquesKingpin(4) : Find.FindAndReveal(James Wesley)", {"Completed Scenarios": "art_museum_heist;the_getaway;protection_racket;the_raft_breakout"},
     {"hotes": [["60165", "60159a"]]}, scenario="kingpin_fne"),
 cas("60206b The Getaway (Failed) [fne5] — en jeu ; chaque joueur revele un attachement du deck rencontre a la mise en place (1 oeuvre au Setup + 1 revelee + 1 par l'Art Thief qu'elle appelle = 3 attachements)",
     "Find.FindAndReveal(Attachment) par joueur", {"Failed Scenarios": "the_getaway"},
     {"en_jeu": ["60206b"], "trait": "", "type": "Attachment", "nombre": 3}, verifier="fne5_trait"),
 cas("60207a Protection Racket (Completed) [fne5] — en jeu ; apres les mulligans, chercher un soutien (may) : Aunt May arrive en main",
     "ChercherEnMain(Support)", {"Completed Scenarios": "protection_racket"},
     {"en_jeu": ["60207a"], "taille_main": 7, "en_main": ["01006"]}, main_exclusive=None, cibles=["01006"]),
 cas("60208a The Raft Breakout (Completed) [fne5] — en jeu ; apres les mulligans, chercher un allie (may) : Black Cat arrive en main",
     "ChercherEnMain(Ally)", {"Completed Scenarios": "the_raft_breakout"},
     {"en_jeu": ["60208a"], "taille_main": 7, "en_main": ["01002"]}, main_exclusive=None, cibles=["01002"]),
 cas("Carnet sortant [fne5] — victoire avec Disturbed Psyche a 2 jetons et Black Cat retiree du jeu : Completed + Trust Established? + Allies removed",
     "CollectFNE : Completed Scenarios, Trust Established?, Allies removed from the campaign", {},
     {"collect": "art_museum_heist", "cles": {"Completed Scenarios": "art_museum_heist", "Trust Established?": "1", "Allies removed from the campaign": "Black Cat"}},
     verifier="fne5_collect", scenario="art_museum_heist_typhoid_mary", declencher=["Puzzle.Token('60112', 'threat', 2)", "Puzzle.Remove('01002')"]),
]
DEBUT="    # ------------------------------------------------------------------------\n    # Pack officiel « fne » — bloc 5"
FIN="    # ---- fin du bloc 5 fne ----\n"
bloc = DEBUT + " : campagne (coordinateur, 18/09/2026). Filtre : \"[fne5]\". Genere par scratchpad/b3/gen_cas_fne_5.py.\n    # ------------------------------------------------------------------------\n"
for c in CAS:
    bloc += "    " + json.dumps(c, ensure_ascii=False, indent=4).replace("\n", "\n    ").replace(": true", ": True").replace(": false", ": False") + ",\n"
bloc += FIN
if DEBUT in s:
    i=s.index(DEBUT); j=s.index(FIN, i)+len(FIN); s=s[:i]+bloc+s[j:]
else:
    ancre="    # ------------------------------------------------------------------------\n    # Pack officiel « fne » — bloc 2"
    assert ancre in s; s=s.replace(ancre, bloc+ancre, 1)

VERIFS='''
# ---------------------------------------------------------------- pack fne (bloc 5)
def fne5_trait(monde, aides):
    """Campagne : toutes les cartes EN JEU d'un `trait` (ou toutes, trait vide)
    et d'un `type` portent le `statut`, ont `boost` carte(s) boost, ont le
    `compteur` [nom, n] ; `exemplaires` [id, n] compte les copies en jeu."""
    attendu = dict(aides["cas"].get("attendu") or {})
    soucis = []
    if "exemplaires" in attendu:
        cid, n = attendu.pop("exemplaires")
        copies = [c for c in monde.object_manager.card_dict.values()
                  if c.face is not None and c.face.IsInPlay() and c.face.paper.card_id == cid]
        if len(copies) != n:
            soucis.append(f"{len(copies)} exemplaire(s) de {cid} en jeu (attendu {n})")
    if "trait" in attendu:
        trait = attendu.pop("trait"); typ = attendu.pop("type")
        cibles = [c.face for c in monde.object_manager.card_dict.values()
                  if c.face is not None and c.face.IsInPlay() and type(c.face).__name__ == typ
                  and (not trait or c.face.HasTrait(trait))]
        if not cibles:
            soucis.append(f"aucune carte {typ} {trait!r} en jeu")
        if "nombre" in attendu and len(cibles) != attendu["nombre"]:
            soucis.append(f"{len(cibles)} carte(s) {typ} {trait!r} en jeu (attendu {attendu['nombre']}) : {[f.paper.card_id for f in cibles]}")
        attendu.pop("nombre", None)
        for f in cibles:
            if "statut" in attendu and not f.HasStatus(attendu["statut"]):
                soucis.append(f"{f.paper.card_id} sans statut {attendu['statut']}")
            if "boost" in attendu:
                nb = f.card.components.boostable.GetDeck().GetSize() if getattr(f.card.components, "boostable", None) else 0
                if nb != attendu["boost"]:
                    soucis.append(f"{f.paper.card_id} : {nb} carte(s) boost (attendu {attendu['boost']})")
            if "compteur" in attendu:
                nom, n = attendu["compteur"]
                if f.GetCounters(nom) != n:
                    soucis.append(f"{f.paper.card_id} : {nom}={f.GetCounters(nom)} (attendu {n})")
        for k in ("statut", "boost", "compteur"):
            attendu.pop(k, None)
    if attendu:
        aides2 = dict(aides); aides2["cas"] = dict(aides["cas"], attendu=attendu)
        ok, msg = etat_attendu(monde, aides2)
        if not ok: soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, "campagne ok"


def fne5_collect(monde, aides):
    """Le carnet SORTANT (CollectFNE) sur une partie gagnee : on simule la fin
    de partie gagnee (world.game_over) et on lit les cles rendues."""
    import types
    from cards.pack.fne.campaign import CollectFNE
    from game.effect.rule import DebugRule
    attendu = dict(aides["cas"].get("attendu") or {})
    manigance = attendu.pop("collect")
    voulu = attendu.pop("cles")
    monde.game_over = types.SimpleNamespace(is_players_won=True)
    effet = DebugRule(monde.object_manager.card_dict[0].face)
    rendu = CollectFNE(manigance, effet)
    soucis = [f"{k} = {rendu.get(k)!r} (attendu {v!r})" for k, v in voulu.items() if rendu.get(k) != v]
    if soucis:
        retirees = [(f.paper.card_id, f.paper.name, type(f).__name__, type(f.GetOwner()).__name__) for f in monde.area_removed.Get(True)]
        return False, " ; ".join(soucis) + f" ; rendu = {rendu} ; area_removed = {retirees}"
    return True, f"carnet sortant ok : {rendu}"

'''
MARQ="# ---------------------------------------------------------------- pack fne (bloc 5)"
FINV = "# ---- fin des verificateurs du bloc 5 ----\n"
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
print("cas [fne5]:", len(CAS), "; syntaxe OK")
