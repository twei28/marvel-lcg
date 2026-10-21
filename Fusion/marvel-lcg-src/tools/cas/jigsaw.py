# Cas test_capacites du set JIGSAW (pack MC×DC 2026 « La ville ne dort jamais »), PU-2.
# Prefixe `[jig]` (filtre : `[jig]`, ou `[jig] pu056a ` pour une carte).
#
# Montage : scenario d'essai `protection_racket_jigsaw` (Jigsaw I pu056a, puis pu057a), Spider-Man (01001) en HEROS.
# Le deck rencontre est remplace par des 01105 (« I'm Tough », 0 icone de boost) pour que l'attaque ne recoive aucun
# bonus. Jigsaw attaque directement le heros (`Puzzle.EnemyAttacks`, brique commune) ; aucune defense proposee.
SC = "protection_racket_jigsaw"
SCE = "protection_racket_jigsaw_expert"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DEFENSE = {"passer_sur_option": "Defense"}
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')", HEROS]


def _c(nom, pourquoi, mise, attendu, **cle):
    cas = {"nom": "[jig] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC), "heros": "spider_man",
           "mise_en_place": RIEN + mise, "declencher": ["Puzzle.EnemyAttacks('pu056a', '01001a')"],
           "verifier": "etat_attendu", "attendu": attendu}
    cas.update(cle)
    return cas


# ⚠ La carte Boost de l'attaque est defaussee AVANT la Reponse forcee (« apres que Jigsaw vous a attaque ») : c'est donc
# elle qui est « le dessus de la defausse rencontre ». Le deck rencontre sert ici a choisir ce dessus.
BOOST_SBIRE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01103', '01105')"]


def _d(nom, pourquoi, deck, mise, attendu, attaquant="pu056a", **cle):
    avant = cle.pop("avant_attaque", None)
    cas = _c(nom, pourquoi, mise, attendu, **cle)
    cas["mise_en_place"] = [*RIEN[:1], f"Puzzle.CreateEncounterDeck({', '.join(repr(x) for x in deck)})", HEROS, *mise]
    cas["declencher"] = [*([avant] if avant else []), f"Puzzle.EnemyAttacks('{attaquant}', '01001a')"]
    return cas


CAS = [
    _d("pu056a Forced Response : la carte Boost (defaussee) est un SBIRE -> mis en jeu engage avec le heros, pas de menace",
       "« if the top of the encounter discard pile is a minion, put it into play engaged with you »",
       ["01105", "01103"], [], {"en_jeu": ["01103"], "menace": [["60134b", 0]]}, **SANS_DEFENSE),
    _d("pu056a Forced Response : la carte Boost est une TRAITRISE (sbire plus bas dans la defausse) -> 1 menace, aucun sbire",
       "seul le DESSUS compte ; « Otherwise, place 1 threat on the main scheme »",
       ["01105", "01105"], ["Puzzle.CreateEncounterDiscardPile('01103')"],
       {"hors_jeu": ["01103"], "menace": [["60134b", 1]]}, **SANS_DEFENSE),
    _d("pu057b Forced Response (expert final) : dessus = traitrise -> 2 menaces sur le complot du joueur",
       "« place 2 threat on the main scheme »",
       ["01105", "01105"], [],
       {"menace_joueur": 2}, attaquant="pu057b", scenario=SCE, avant_attaque="Puzzle.AdvanceVillain()",
       verifier="fne3p_racket", main_exclusive=["01088"], **SANS_DEFENSE),
]

# ============================================================== pu058 : Jigsaw's Knife
def _k(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[jig] " + nom, "pourquoi": pourquoi, "scenario": SC, "heros": "spider_man",
           "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')", HEROS, *mise],
           "declencher": declencher, "verifier": "etat_attendu", "attendu": attendu}
    cas.update(cle)
    return cas


CAS += [
    _k("pu058 Jigsaw's Knife : attache a Jigsaw, Jigsaw gagne Riposte 1",
       "« Attach to Jigsaw » ; « Jigsaw gains retaliate 1 » (modele sk148)",
       ["Puzzle.PutIntoPlay('pu058')"], [], {"accroche_a": [["pu058", "pu056a"]], "attributs_carte": [["pu056a", "retaliate", 1]]},
       main_exclusive=["01088"]),
    _k("pu058 TEMOIN : sans le couteau, Jigsaw n'a pas de Riposte",
       "contre-cas", [], [], {"attributs_carte": [["pu056a", "retaliate", 0]]}, main_exclusive=["01088"]),
    _k("pu058 « his attacks gain piercing » : l'attaque sur un allie Tenace defausse la carte Tenace et blesse",
       "piercing : sans Tenace l'allie meurt (2 PV), avec le couteau la Tenace saute et il meurt quand meme ; TEMOIN ci-dessous = 0 degat", ["Puzzle.PutIntoPlay('pu058')", "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Tough('01075')"],
       ["Puzzle.EnemyAttacks('pu056a', '01075')"], {"hors_jeu": ["01075"]},
       main_exclusive=["01088"], **SANS_DEFENSE),
    _k("pu058 piercing, TEMOIN : sans le couteau la carte Tenace absorbe l'attaque",
       "contre-cas", ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Tough('01075')"],
       ["Puzzle.EnemyAttacks('pu056a', '01075')"], {"statuts_absents": [["01075", "Tough"]], "degats": [["01075", 0]]},
       main_exclusive=["01088"], **SANS_DEFENSE),
    _k("pu058 Hero Action : epuiser un personnage et depenser [mental][physical] -> couteau defausse, le heros est epuise",
       "cout `BR` + « exhaust a character you control » (seul le heros est pret)",
       ["Puzzle.PutIntoPlay('pu058')"], ["Puzzle.Action('pu058', 'HeroAction')"],
       {"hors_jeu": ["pu058"], "exhausted": ["01001a"]},
       main_exclusive=["01089", "01090"], payer_avec=["01089", "01090"], payer_tout=True),
]

# ============================================================== pu059 : Bushwhacker
CAS += [
    _k("pu059 Forced Interrupt : Bushwhacker veut attaquer -> a la place le joueur prend 3 degats indirects (aucun degat d'attaque)",
       "« instead take 3 indirect damage » ; ATQ 0* donc aucun autre degat ; le joueur choisit l'option par defaut",
       ["Puzzle.PutIntoPlay('pu059')"], ["Puzzle.Attack('pu059')"], {"degats_identite": 3},
       main_exclusive=["01088"], choisir_option="Take_3_indirect_damage"),
    _k("pu059 « may spend [mental] » : le joueur paie [mental] -> les 3 degats vont a Jigsaw, le heros n'en prend aucun",
       "« deal that damage to another enemy instead » (Jigsaw = le seul autre ennemi)",
       ["Puzzle.PutIntoPlay('pu059')"], ["Puzzle.Attack('pu059')"], {"degats": [["pu056a", 3]], "degats_identite": 0},
       main_exclusive=["01089"], payer_avec=["01089"], payer_tout=True,
       preferer_option="to another enemy"),
]

# ============================================================== pu063 : Man Mountain Marko
CAS += [
    _k("pu063 When Revealed : un personnage qu'on controle est epuise (le heros, seul pret)",
       "« Exhaust a character you control » (modele 60133)",
       [], ["Puzzle.Reveal('pu063')"], {"exhausted": ["01001a"]}, main_exclusive=["01088"]),
    _k("pu063 When Revealed, TEMOIN : sans le script le heros reste pret (cas de reference : un autre sbire, Shocker 01103)",
       "contre-cas", [], ["Puzzle.Reveal('01103')"], {"pret": ["01001a"]}, main_exclusive=["01088"]),
    _k("pu063 Teamwork (MAGGIA) : un autre MAGGIA en jeu (Maggia Thug pu060) -> Marko s'active contre le joueur a son arrivee (ATQ 3 : 3 degats sur l'identite, ou la defense)",
       "Teamwork natif lu dans desc ; l'activation contre le joueur : attaque (SCH 0)",
       ["Puzzle.PutIntoPlay('pu060')"], ["Puzzle.Reveal('pu063')"], {"degats_identite": 3}, main_exclusive=["01088"], **SANS_DEFENSE),
    _k("pu063 Teamwork, TEMOIN : aucun autre MAGGIA en jeu -> pas d'activation (aucun degat sur l'identite)",
       "contre-cas", [], ["Puzzle.Reveal('pu063')"], {"degats_identite": 0}, main_exclusive=["01088"]),
]

# ============================================================== pu064 : Eel
# ⚠ Quickstrike : l'entree en jeu d'Eel (engage avec le heros) declenche deja une attaque.
CAS += [
    _k("pu064 Forced Response : l'attaque Quickstrike d'Eel blesse le heros -> il est epuise, pas etourdi",
       "« attacks and damages a character, exhaust that character »",
       ["Puzzle.PutIntoPlay('pu064')"], [], {"exhausted": ["01001a"], "statuts_absents": [["01001a", "Stunned"]]},
       main_exclusive=["01088"], **SANS_DEFENSE),
    _k("pu064 Forced Response : l'allie Tenace defend, ne subit aucun degat -> il est etourdi (Otherwise, stun it)",
       "« Otherwise, stun it » : le defenseur est la cible ; la Tenace absorbe",
       ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Tough('01075')"],
       ["Puzzle.PutIntoPlay('pu064')", "Puzzle.EnemyAttacks('pu064', '01001a', defender='01075')"],
       {"statuts": [["01075", "Stunned"]]}, main_exclusive=["01088"]),
]

# pu064, branche « Otherwise » SANS defenseur : le heros Tenace absorbe l'attaque d'Eel -> il est etourdi
CAS += [
    _k("pu064 Forced Response, sans defenseur : le heros (Tenace) ne subit aucun degat -> il est etourdi",
       "« Otherwise, stun it » : la cible de l'attaque est le heros lui-meme",
       ["Puzzle.Tough('01001a')"], ["Puzzle.PutIntoPlay('pu064')"], {"statuts": [["01001a", "Stunned"]]},
       main_exclusive=["01088"], **SANS_DEFENSE),
]

# ============================================================== pu065 / pu068
CAS += [
    _k("pu065 When Revealed : Jigsaw seul MAGGIA en jeu -> 2 menaces + menace de depart 1 = 3 sur le complot annexe",
       "« 2 threat for each MAGGIA character in play » : le vilain compte",
       [], ["Puzzle.Reveal('pu065')"], {"menace": [["pu065", 3]]}, main_exclusive=["01088"]),
    _k("pu065 When Revealed : Jigsaw + Maggia Thug (pu060) = 2 MAGGIA -> 4 menaces + 1 = 5",
       "« for each » : un par personnage MAGGIA",
       ["Puzzle.PutIntoPlay('pu060')"], ["Puzzle.Reveal('pu065')"], {"menace": [["pu065", 5]]}, main_exclusive=["01088"]),
    _k("pu065 When Defeated : une fois vaincu, le joueur trouve un sbire MAGGIA hors jeu et le revele (Maggia Thug du deck rencontre)",
       "« finds a MAGGIA minion that is not in play and reveals it »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('pu060')", "Puzzle.PutIntoPlay('pu065')"],
       ["Puzzle.SetThreat('pu065', 1)", "Puzzle.Thwart('01001a')"], {"en_jeu": ["pu060"]}, main_exclusive=["01088"]),
    _k("pu068 When Revealed : un MAGGIA hors jeu (pu060 dans le deck) est trouve et revele, puis tous les MAGGIA engages s'activent -> Thug (ATQ 2) attaque : 2 degats sur l'identite",
       "ordre : trouver/reveler d'abord, activer ensuite (le nouveau compris)",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('pu060')"], ["Puzzle.Reveal('pu068')"],
       {"en_jeu": ["pu060"], "degats_identite": 2}, main_exclusive=["01088"], **SANS_DEFENSE),
    _k("pu068 When Revealed, TEMOIN : aucun MAGGIA a trouver -> rien n'entre en jeu, aucun degat",
       "contre-cas", ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.Reveal('pu068')"],
       {"hors_jeu": ["pu060"], "degats_identite": 0}, main_exclusive=["01088"]),
]

# ============================================================== pu066 : Cut to Pieces
CAS += [
    _k("pu066 When Revealed (heros) : Jigsaw attaque, ATQ 1* + 1 -> 2 degats sur l'identite (aucune carte de boost)",
       "« If this activation is an attack, he gets +1 ATK » (ATQ de base 1 : 1 + 1)",
       [], ["Puzzle.Reveal('pu066')"], {"degats_identite": 2}, main_exclusive=["01088"], **SANS_DEFENSE),
    _k("pu066 Boost : 1 menace sur la principale ET 1 degat soigne sur Jigsaw (4 degats - 1 = 3, + 1 degat que Puzzle.Boost inflige a Jigsaw avec n'importe quelle carte : sonde du 21/10 = 4)",
       "« Place 1 threat on the main scheme and heal 1 damage from Jigsaw » ; sans soin le cas mesurerait 5",
       ["Puzzle.Damage('pu056a', 4)"], ["Puzzle.Boost('pu066')"], {"menace": [["60134b", 3]], "degats": [["pu056a", 4]]},
       main_exclusive=["01088"], **SANS_DEFENSE),
]


# ============================================================== pu070 : A Made Man
ALTER_EGO = "Puzzle.ChangeForm('01001a')"
CAS += [
    _k("pu070 When Revealed (heros) : Jigsaw recoit 1 carte de boost face cachee (aucun sbire MAGGIA)",
       "« Give Jigsaw a facedown boost card »", [], ["Puzzle.Reveal('pu070')"], {"boosts_jigsaw": 1},
       main_exclusive=["01088"], verifier="jigsaw_etat"),
    _k("pu070 When Revealed (heros) : un sbire MAGGIA en jeu (pu060) -> 1 + 1 supplementaire = 2 cartes de boost",
       "« If a MAGGIA minion is in play, give him an additional boost card »",
       ["Puzzle.PutIntoPlay('pu060')"], ["Puzzle.Reveal('pu070')"], {"boosts_jigsaw": 2},
       main_exclusive=["01088"], verifier="jigsaw_etat"),
    _k("pu070 When Revealed (alter ego) : un allie en jeu (Spider-Woman 01011) est defausse, aucune menace posee",
       "« Discard an ally from play. Otherwise ... »",
       [ALTER_EGO, "Puzzle.PutIntoPlay('01011', under_control=True)"], ["Puzzle.Reveal('pu070')"],
       {"hors_jeu": ["01011"], "menace": [["60134b", 0]]}, main_exclusive=["01088"]),
    _k("pu070 When Revealed (alter ego) : AUCUN allie -> 1 menace par joueur sur chaque complot (0 + 1 = 1)",
       "« Otherwise, place 1[per hero] threat on each scheme »",
       [ALTER_EGO], ["Puzzle.Reveal('pu070')"], {"menace": [["60134b", 1]]}, main_exclusive=["01088"]),
    _k("pu070 Boost : apres l'activation (Jigsaw attaque le heros), Jigsaw recoit 1 carte de boost face cachee",
       "« After this activation, give Jigsaw a facedown boost card » (modele sk196 : RunAt.AfterEnemyActivationEnd)",
       [], ["Puzzle.Boost('pu070')"], {"boosts_jigsaw": 1}, main_exclusive=["01088"], verifier="jigsaw_etat", **SANS_DEFENSE),
    _k("pu070 Boost, TEMOIN : avec une carte de boost quelconque (01105), Jigsaw n'a aucune carte face cachee apres",
       "contre-cas", [], ["Puzzle.Boost('01105')"], {"boosts_jigsaw": 0}, main_exclusive=["01088"], verifier="jigsaw_etat", **SANS_DEFENSE),
]


VERIFICATIONS = r'''
def jigsaw_etat(monde, aides):
    """etat_attendu + `boosts_jigsaw` (cartes de boost face cachee de Jigsaw), `menace_complots` ([[card_id, n]])."""
    attendu = aides["cas"].get("attendu") or {}
    propres = {"boosts_jigsaw"}
    inconnues = sorted(set(attendu) - set(CLES_ETAT_ATTENDU) - propres)
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de jigsaw_etat : {inconnues}"
    ok, message = etat_attendu(monde, aides)
    soucis = [] if ok else [message]
    if "boosts_jigsaw" in attendu:
        v = aides["par_id"](monde, "pu056a")
        n = v.components.boostable.GetDeck().GetSize()
        if n != attendu["boosts_jigsaw"]:
            soucis.append(f"cartes de boost face cachee de Jigsaw = {n} (attendu {attendu['boosts_jigsaw']})")
    return (False, " ; ".join(soucis)) if soucis else (True, "etat Jigsaw conforme")
'''

CAS += [
    _k("pu060 Maggia Thug : Guard 1 (Patrol natif non mesurable ici) (natifs, lus dans desc), ATQ 2, PV 3, SCH 1",
       "aucun script : mots-cles `desc` (fiches guard.md, patrol.md)",
       ["Puzzle.PutIntoPlay('pu060')"], [],
       {"attributs_carte": [["pu060", "guard", 0], ["pu060", "attack", 0], ["pu060", "scheme", 0]],
        "pv_max": [["pu060", 3]]}, main_exclusive=["01088"]),
]
