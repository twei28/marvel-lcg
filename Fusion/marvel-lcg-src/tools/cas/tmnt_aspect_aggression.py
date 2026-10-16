# Cas test_capacites du pack d'aspect TMNT Aggression (Inkwire, prefixe `ua`, pack tmnt_aspect_aggression).
# Filtre : `[ua]`. Les cartes faites par le socle (ua006 Bo-Wing, ua009 Clobber, ua015 Demolish) ont leurs cas
# dans `tools/cas/rampage.py` (filtres `[rampage]`, `[reskin]`).
# Gabarits PROCESSUS-CARTE : `.planning/tmnt/aspects-aggression-gabarits.md`.
#
# RESKINS (scan IDENTIQUE a une officielle, recette RECETTES-MOTEUR §11) : chaque capacite a DEUX cas, le
# reskin et son TEMOIN officiel, meme montage, meme chiffre attendu (`_paire`). Substitution : retirer
# `ability_link` de l'entree du reskin -> le cas du reskin ROUGIT, le temoin reste vert.
#
# Conventions (reprises de rampage.py) :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros (10 PV, ATK 2, THW 1) ;
#  - `main_exclusive` : la main ne contient QUE la carte jouee et de quoi payer
#    (01090 Strength = RR, 01088 Energy = YY, 01089 Genius = BB) ;
#  - Rhino 01094 (14 PV) est la cible de mesure ; 01103 Shocker (3 PV, sans Garde) le sbire ;
#    01105 « I'm Tough » une traitrise de garniture du deck Rencontre.
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[ua] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


def _remplacer(valeur, a, b):
    if isinstance(valeur, str):
        return valeur.replace(a, b)
    if isinstance(valeur, list):
        return [_remplacer(v, a, b) for v in valeur]
    if isinstance(valeur, tuple):
        return tuple(_remplacer(v, a, b) for v in valeur)
    if isinstance(valeur, dict):
        return {k: _remplacer(v, a, b) for k, v in valeur.items()}
    return valeur


def _paire(reskin, officielle, nom, pourquoi, mise, declencher, attendu, **cle):
    """Le cas sur le reskin + le TEMOIN identique sur l'officielle (tout `reskin` remplace par `officielle`)."""
    a = _c(f"{reskin} {nom}", pourquoi, mise, declencher, attendu, **cle)
    b = _remplacer(dict(a), reskin, officielle)
    b["nom"] = f"[ua] {reskin} TEMOIN {officielle} (officielle) : {nom}"
    b["pourquoi"] = "le reskin doit rendre EXACTEMENT le chiffre de l'original ; " + pourquoi
    return [a, b]


CAS = []

# ============================================================ ua001 Aggressive Conditioning (56013)
CAS += _paire("ua001", "56013", "Aggressive Conditioning : +3 PV a l'identite et +1 ATK au heros",
              "« You get +3 hit points and your hero gets +1 ATK »",
              [HEROS], [], {"attributs": {"health": 3, "attack": 1}},
              main_exclusive=["ua001", "01090", "01088"], jouer=["ua001"])

# ============================================================ ua005 Blood Rage (45043)
CAS += _paire("ua005", "45043", "Blood Rage : sbire vaincu par une attaque de base -> 1 degat subi, 1 carte piochee, incline",
              "« After you defeat an enemy with a basic attack, exhaust Blood Rage and take 1 damage → draw 1 card » ; "
              "main videe a 1 carte (01088) : 2 cartes apres la pioche",
              [HEROS, "Puzzle.PutIntoPlay('ua005', under_control=True)", "Puzzle.Damage(Puzzle.PutIntoPlay('01103'), 1)"],
              ["Puzzle.Attack('01001a')"],
              {"hors_jeu": ["01103"], "degats_identite": 1, "taille_main": 2, "exhausted": ["ua005"]},
              main_exclusive=["01088"], cibles=["01103"], accepter_choix=True)

# ============================================================ ua007 "Bring It!" (19030)
CAS += _paire("ua007", "19030", "Bring It! : 2 sbires engages -> 2 cartes piochees",
              "« Draw 1 card for each minion engaged with you » ; main videe : la carte jouee, puis 2 piochees",
              [HEROS, "Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('01102')"], [],
              {"taille_main": 2, "defausse": ["ua007"]},
              main_exclusive=["ua007"], jouer=["ua007"])
CAS += _paire("ua007", "19030", "Bring It! : Max 1 per phase, la 2e copie n'est PAS jouee dans la meme phase (main 3, pas 4)",
              "TEMOIN D'EPUISEMENT de « Max 1 per phase » : deux copies en main ; la 1re pioche 2 (main 1+2=3) ; "
              "sans la limite la 2e piocherait encore 2 (main 4)",
              [HEROS, "Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('01102')"], [],
              {"taille_main": 3, "en_main": ["ua007"]},
              main_exclusive=["ua007", "ua007"], jouer=["ua007"], declencher_tolerant=[],
              jouer_apres=["ua007"])

# ============================================================ ua010 Combat Training (01057)
CAS += _paire("ua010", "01057", "Combat Training : +1 ATK au heros",
              "« Your hero gets +1 ATK »", [HEROS], [], {"attributs": {"attack": 1}},
              main_exclusive=["ua010", "01090"], jouer=["ua010"])

# ============================================================ ua016 Drop Kick (10014)
CAS += _paire("ua016", "10014", "Drop Kick : paye uniquement en [physical] -> 4 degats, Rhino sonne, 1 carte piochee",
              "« If you paid for this card using only [physical] resources, stun that enemy and draw 1 card » : "
              "main = la carte + 01090 (RR) + ua009 (R) ; tout est depense, la main finit a 1 (la pioche)",
              [HEROS], [],
              {"degats": [["01094", 4]], "statuts": [["01094", "Stunned"]], "taille_main": 1},
              main_exclusive=["ua016", "01090", "ua009"], jouer=["ua016"], cibles=["01094"])
CAS += _paire("ua016", "10014", "Drop Kick : paye avec de l'energie -> 4 degats, ni sonne ni pioche (contre-cas)",
              "branche « only [physical] » FAUSSE : 01088 (YY) + ua009 (R)",
              [HEROS], [],
              {"degats": [["01094", 4]], "statuts_absents": [["01094", "Stunned"]], "taille_main": 0},
              main_exclusive=["ua016", "01088", "ua009"], jouer=["ua016"], cibles=["01094"])

# ============================================================ ua017 Exeen (18011, reskin d'Angela)
CAS += _paire("ua017", "18011", "Exeen : en jeu, cherche un sbire dans le deck Rencontre et le met en jeu engage",
              "« search the top 10 cards of the encounter deck for a minion and put it into play engaged with you »",
              [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01103', '01105')"], [],
              {"en_jeu": ["ua017", "01103"]},
              main_exclusive=["ua017"], jouer=["ua017"], accepter_choix=True)
CAS += _paire("ua017", "18011", "Exeen : aucun sbire dans le deck Rencontre -> Exeen est defausse",
              "« If a minion was not put into play this way, discard Exeen »",
              [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01104', '01105')"], [],
              {"hors_jeu": ["ua017"], "defausse": ["ua017"]},
              main_exclusive=["ua017"], jouer=["ua017"], accepter_choix=True)

# ============================================================ ua018 Firepower (54014)
CAS += _paire("ua018", "54014", "Firepower : 2 armes inclinees -> 2 x 3 degats (6 sur Rhino)",
              "« Exhaust up to 3 WEAPON upgrades you control → for each upgrade exhausted this way, choose an enemy and "
              "deal 3 damage to it » : 16046 Hand Cannon et 20022 Plasma Pistol",
              [HEROS, "Puzzle.PutIntoPlay('16046', under_control=True)", "Puzzle.PutIntoPlay('20022', under_control=True)"],
              [], {"degats": [["01094", 6]], "exhausted": ["16046", "20022"]},
              main_exclusive=["ua018", "01090"], jouer=["ua018"], cibles=["01094", "01094"], accepter_choix=True)

# ============================================================ ua020 Fusillade (20026)
CAS += _paire("ua020", "20026", "Fusillade : une arme inclinee -> 5 degats",
              "« Exhaust a WEAPON upgrade you control → deal 5 damage to an enemy »",
              [HEROS, "Puzzle.PutIntoPlay('16046', under_control=True)"], [],
              {"degats": [["01094", 5]], "exhausted": ["16046"]},
              main_exclusive=["ua020", "01089"], jouer=["ua020"], cibles=["01094"])

# ============================================================ ua022 He-Dude (56010, reskin de Two-Gun Kid)
CAS += _paire("ua022", "56010", "He-Dude : attaque de base contre 2 ennemis (2 degats a Rhino ET a Shocker)",
              "« choose 2 enemies instead of 1 and resolve this attack against each of them »",
              [HEROS, "Puzzle.PutIntoPlay('ua022', under_control=True)", "Puzzle.PutIntoPlay('01103')"],
              ["Puzzle.Attack('ua022')"],
              {"degats": [["01094", 2], ["01103", 2]]},
              main_exclusive=["01088"], cibles=["01094", "01103"], accepter_choix=True)

CAS += _paire("ua022", "56010", "He-Dude : Rhino SEUL ennemi -> 2 degats, jamais 4 (pas de 2e cible = la meme)",
              "« choose 2 enemies » = deux ennemis DIFFERENTS : sans 2e ennemi, l'attaque ne vise que Rhino, une fois "
              "(correctif 56010 `exclude=\"Targets\"` : avant, Rhino etait choisi deux fois et prenait 4)",
              [HEROS, "Puzzle.PutIntoPlay('ua022', under_control=True)"],
              ["Puzzle.Attack('ua022')"],
              {"degats": [["01094", 2]]},
              main_exclusive=["01088"], cibles=["01094"], accepter_choix=True)

# ============================================================ ua023 Honed Technique (28017)
CAS += _paire("ua023", "28017", "Honed Technique : evenement ATTACK Aggression paye en [mental] -> + cout imprime (2+1=3)",
              "« increase the amount of damage that event deals by its printed cost » : 35018 Precision Strike "
              "(cout 1, 2 degats) payee par 01089 (BB)",
              [HEROS, "Puzzle.PutIntoPlay('ua023', under_control=True)"], [],
              {"degats": [["01094", 3]]},
              main_exclusive=["35018", "01089"], jouer=["35018"], cibles=["01094"], accepter_choix=True)

# ============================================================ ua024 Innate Aggression (61034)
CAS += _paire("ua024", "61034", "Innate Aggression : +1 ATK au heros",
              "« Your hero gets +1 ATK »", [HEROS], [], {"attributs": {"attack": 1}},
              main_exclusive=["ua024", "01090"], jouer=["ua024"])
CAS += _paire("ua024", "61034", "Innate Aggression : porte la capacite Starting (WhenGameBeginSetup) de l'original",
              "« Starting » : capacite de MISE EN PLACE, hors de portee du harnais sans deck qui contient la carte ; "
              "on verifie qu'elle est construite sur la carte (le module de 61034 ne lit ni nom ni card_id)",
              [HEROS, "Puzzle.Gain('ua024')"], [],
              {"carte": "ua024", "fabrique": "WhenGameBeginSetup"},
              verifier="ua_porte_fabrique")

# ============================================================ ua027 Looking for Trouble (16043)
CAS += _paire("ua027", "16043", "Looking for Trouble : defausse jusqu'a un sbire, le met en jeu, retire 3 menaces",
              "« Discard cards ... until you discard a minion. Put that minion into play engaged with you → remove 3 "
              "threat from the main scheme »",
              [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01103', '01105')"],
              ["Puzzle.SetThreat('01097b', 5)"],
              {"en_jeu": ["01103"], "menace": [["01097b", 2]]},
              main_exclusive=["ua027"], jouer=["ua027"])

# ============================================================ ua028 Magic Attack (21043)
CAS += _paire("ua028", "21043", "Magic Attack : identite MYSTIC, 3 cartes defaussees (sur 5 au deck) -> 3 degats",
              "« discard up to 5 cards from the top of your deck → deal 1 damage to that enemy for each card discarded "
              "this way » : deck de 5 cartes, le joueur en declare 3 ; 2 restent",
              ["Puzzle.ChangeForm('09001b')", SANS_DECK,
               "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089')"], [],
              {"degats": [["01094", 3]], "taille_deck_joueur": 2},
              heros="doctor_strange", main_exclusive=["ua028", "01090"], jouer=["ua028"], cibles=["01094"],
              choisir_option=["3"])
CAS += _paire("ua028", "21043", "Magic Attack : identite SANS MYSTIC (Spider-Man) -> injouable, rien ne se passe",
              "« Play only if your identity has the MYSTIC trait »",
              [HEROS], [], {"degats": [["01094", 0]], "en_main": ["ua028"]},
              main_exclusive=["ua028", "01090"], jouer=["ua028"], cibles=["01094"])

# ============================================================ ua029 Martial Prowess (10018)
CAS += _paire("ua029", "10018", "Martial Prowess : genere le [physical] qui paie un evenement ATTACK (main sans ressource)",
              "« Exhaust Martial Prowess → generate a [physical] resource for an ATTACK event » : la main ne contient "
              "que 35018 (cout 1) : seule la Ressource de la carte peut la payer",
              [HEROS, "Puzzle.PutIntoPlay('ua029', under_control=True)"], [],
              {"degats": [["01094", 2]], "exhausted": ["ua029"]},
              main_exclusive=["35018"], jouer=["35018"], cibles=["01094"])

# ============================================================ ua031 No Quarter (28013)
CAS += _paire("ua031", "28013", "No Quarter : 1 point d'exces -> 1 carte du deck defaussee, Aggression -> en main",
              "« For each point of excess damage ..., discard the top card of your deck and add each Aggression (red) "
              "card discarded this way to your hand » : Shocker 3 PV, 4 degats -> 1 exces ; deck de trois 18012 "
              "(Aggression) : 2 restent, 1 en main",
              [HEROS, "Puzzle.PutIntoPlay('01103')", SANS_DECK, "Puzzle.CreatePlayerDeck('18012', '18012', '18012')"], [],
              {"hors_jeu": ["01103"], "en_main": ["18012"], "taille_deck_joueur": 2},
              main_exclusive=["ua031", "01090"], jouer=["ua031"], cibles=["01103"])

# ============================================================ ua032 "Now I'm Mad" (43019)
CAS += _paire("ua032", "43019", "Now I'm Mad : 4 PV restants sur 10 (< moitie) -> +1 ATK et -1 THW",
              "« While your hero's remaining hit points are less than half ... +1 ATK and -1 THW »",
              [HEROS, "Puzzle.PutIntoPlay('ua032', under_control=True)", "Puzzle.Damage('01001a', 6)"], [],
              {"attributs": {"attack": 1, "thwart": -1}})
CAS += _paire("ua032", "43019", "Now I'm Mad : 5 PV restants sur 10 (PAS moins de la moitie) -> aucun bonus",
              "contre-cas du seuil : « less than half » est strict",
              [HEROS, "Puzzle.PutIntoPlay('ua032', under_control=True)", "Puzzle.Damage('01001a', 5)"], [],
              {"attributs": {"attack": 0, "thwart": 0}})

# ============================================================ ua034 Precision Strike (35018)
CAS += _paire("ua034", "35018", "Precision Strike : 2 degats tuent Shocker -> le heros soigne 2",
              "« If this attack defeats that enemy, heal 2 damage from your hero » : identite a 3 degats -> 1",
              [HEROS, "Puzzle.Damage(Puzzle.PutIntoPlay('01103'), 1)", "Puzzle.Damage('01001a', 3)"], [],
              {"hors_jeu": ["01103"], "degats_identite": 1},
              main_exclusive=["ua034", "01089"], jouer=["ua034"], cibles=["01103"])

# ============================================================ ua035 Rave (16040, reskin de Bug)
CAS += _paire("ua035", "16040", "Rave : apres une attaque de base du heros, soigne 1 degat de Rave",
              "« After your hero makes a basic attack, heal 1 damage from Rave »",
              [HEROS, "Puzzle.PutIntoPlay('ua035', under_control=True)", "Puzzle.Damage('ua035', 1)"],
              ["Puzzle.Attack('01001a')"],
              {"degats": [["ua035", 0], ["01094", 2]]},
              main_exclusive=["01088"], cibles=["01094"], accepter_choix=True)

# ============================================================ ua038 Spoiling for a Fight (54016)
CAS += _paire("ua038", "54016", "Spoiling for a Fight : un sbire mis en jeu engage -> le heros est redresse",
              "« Put that minion into play engaged with you → ready your hero »",
              [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01103', '01105')"], [],
              {"en_jeu": ["01103"], "pret": ["01001a"]},
              main_exclusive=["ua038"], jouer=["ua038"])

# ============================================================ ua039 Suppressing Fire (46014)
CAS += _paire("ua039", "46014", "Suppressing Fire : attachee a Shocker, le heros l'attaque et le tue -> soigne 2",
              "« When you attack and defeat attached minion, heal 2 damage from your hero »",
              [HEROS, "Puzzle.PutIntoPlay('01103')", "Puzzle.Damage('01001a', 3)"], [],
              {"hors_jeu": ["01103"], "degats_identite": 1},
              main_exclusive=["ua039"], jouer=["ua039"], cibles=["01103"], accepter_choix=True,
              declencher_apres=["Puzzle.Damage('01103', 1)", "Puzzle.Attack('01001a')"])


VERIFICATIONS = r'''
def ua_porte_fabrique(monde, aides):
    """La carte (en main ou en jeu) porte une capacite construite par la fabrique nommee."""
    attendu = aides["cas"]["attendu"]
    cible = attendu["carte"]
    face = None
    for objet in monde.object_manager.card_dict.values():
        f = getattr(objet, "face", None)
        if f is not None and getattr(getattr(f, "paper", None), "card_id", None) == cible:
            face = f
            break
    if face is None:
        return False, f"{cible} introuvable"
    from cards.database import CardsDB
    capacites = CardsDB.FindAbilities(cible, getattr(face.paper, "pack", ""), getattr(face.paper, "set_name", ""))
    noms = []
    for c in capacites or []:
        noms += list(getattr(c, "func_names", []) or [])
        noms.append(getattr(getattr(c, "when", None), "__name__", ""))
    if any(attendu["fabrique"] in (n or "") for n in noms):
        return True, f"{cible} porte {attendu['fabrique']}"
    return False, f"{cible} : fabriques vues {noms}"
'''
