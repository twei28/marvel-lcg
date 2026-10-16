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


# ======================================================================================================
# CARTES NOUVELLES / MODIFIEE (scripts propres, src/cards/pack/tmnt_aspect_aggression/uaNNN.py)
# Daredevil (60001, MARTIAL ARTIST, 10 PV, ATK 2) sert d'identite MARTIAL ARTIST.
DD = "daredevil"
DD_HEROS = "Puzzle.ChangeForm('60001b')"
DECK6 = "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089', '01089')"

CAS += [
    # ---------------------------------------------------------------- ua002 Apex Predator
    _c("ua002 Apex Predator : Rampage 2 paye (2 degats, 2 cartes du deck) puis branche « Deal 4 damage »",
       "« take 2 damage and discard 2 cards from the top of your deck » + « Choose: Deal 4 damage to an enemy »",
       [HEROS, SANS_DECK, DECK6], [],
       {"degats_identite": 2, "taille_deck_joueur": 4, "degats": [["01094", 4]], "defausse": ["ua002", "01089"]},
       main_exclusive=["ua002", "01088"], payer_avec=["01088"], jouer=["ua002"], cibles=["01094"],
       preferer_option="Deal 4 damage"),
    _c("ua002 Apex Predator : branche « Stun an enemy » -> Rhino sonne, aucun degat",
       "seconde branche du « Choose » ; le cout Rampage est paye de meme",
       [HEROS, SANS_DECK, DECK6], [],
       {"degats_identite": 2, "taille_deck_joueur": 4, "degats": [["01094", 0]], "statuts": [["01094", "Stunned"]]},
       main_exclusive=["ua002", "01088"], payer_avec=["01088"], jouer=["ua002"], cibles=["01094"],
       preferer_option="Stun an enemy"),
    _c("ua002 Apex Predator : identite Tenace -> Rampage impaye, ni defausse ni effet",
       "« If taking damage is a cost, that cost is not considered paid unless all of that damage was taken »",
       [HEROS, SANS_DECK, DECK6, "Puzzle.Tough('01001a')"], [],
       {"degats_identite": 0, "taille_deck_joueur": 6, "degats": [["01094", 0]], "statuts_absents": [["01094", "Stunned"]]},
       main_exclusive=["ua002", "01088"], payer_avec=["01088"], jouer=["ua002"], cibles=["01094"]),

    # ---------------------------------------------------------------- ua003 Assassin
    _c("ua003 Assassin : attaque le VILAIN -> 1 seul degat consecutif (2 - 1)",
       "« takes -1 consequential damage after he attacks the villain »",
       [HEROS, "Puzzle.PutIntoPlay('ua003', under_control=True)"], ["Puzzle.Attack('ua003')"],
       {"degats": [["ua003", 1], ["01094", 3]]}, main_exclusive=["01088"], cibles=["01094"]),
    _c("ua003 Assassin : attaque un sbire ELITE (Sandman) -> 1 seul degat consecutif",
       "« ... or an ELITE minion » (Sandman 01102 est ELITE)",
       [HEROS, "Puzzle.PutIntoPlay('ua003', under_control=True)", "Puzzle.PutIntoPlay('01102')"],
       ["Puzzle.Attack('ua003')"],
       {"degats": [["ua003", 1]]}, main_exclusive=["01088"], cibles=["01102"]),
    _c("ua003 Assassin : CONTRE-CAS, attaque un sbire NON ELITE (Shocker) -> 2 degats consecutifs",
       "la reduction ne vise que le vilain et les ELITE",
       [HEROS, "Puzzle.PutIntoPlay('ua003', under_control=True)", "Puzzle.PutIntoPlay('01103')"],
       ["Puzzle.Attack('ua003')"],
       {"degats": [["ua003", 2]], "hors_jeu": ["01103"]}, main_exclusive=["01088"], cibles=["01103"]),

    # ---------------------------------------------------------------- ua004 Attack Training (MODIFIEE)
    _c("ua004 Attack Training : sur un allie NINJA (Assassin) -> +1 ATK, +2 PV",
       "« Attach to a NINJA or MUTANIMAL ally » ; « +1 ATK and +2 hit points »",
       [HEROS, "Puzzle.PutIntoPlay('ua003', under_control=True)"], [],
       {"attributs_carte": [["ua003", "attack", 1], ["ua003", "health", 2]]},
       main_exclusive=["ua004", "01090"], jouer=["ua004"], cibles=["ua003"]),
    _c("ua004 Attack Training : sur un allie MUTANIMAL (Leatherhead) -> +1 ATK, +2 PV",
       "second trait du « or »",
       [HEROS, "Puzzle.PutIntoPlay('ua026', under_control=True)"], [],
       {"attributs_carte": [["ua026", "attack", 1], ["ua026", "health", 2]]},
       main_exclusive=["ua004", "01090"], jouer=["ua004"], cibles=["ua026"]),
    _c("ua004 Attack Training : seul allie = Mockingbird (ni NINJA ni MUTANIMAL) -> injouable, reste en main",
       "contre-cas du trait ; c'est ce qui distingue la carte de 32043 (X-MEN)",
       [HEROS, "Puzzle.PutIntoPlay('01083', under_control=True)"], [],
       {"en_main": ["ua004"], "attributs_carte": [["01083", "attack", 0]]},
       main_exclusive=["ua004", "01090"], jouer=["ua004"], cibles=["01083"]),

    # ---------------------------------------------------------------- ua008 Chain Reaction
    _c("ua008 Chain Reaction : Shocker vaincu -> 2 a Hydra Bomber, vaincu -> 3 a Rhino",
       "les trois maillons : 2, 2 puis 3 degats, chaque cible choisie apres la defaite de la precedente",
       [HEROS, "Puzzle.Damage(Puzzle.PutIntoPlay('01103'), 1)", "Puzzle.PutIntoPlay('01110')"], [],
       {"hors_jeu": ["01103", "01110"], "degats": [["01094", 3]]},
       main_exclusive=["ua008", "01090"], jouer=["ua008"], cibles=["01103", "01110", "01094"]),
    _c("ua008 Chain Reaction : CONTRE-CAS, la 1re cible (Rhino) survit -> la chaine s'arrete",
       "« If that enemy is defeated » faux : Shocker n'est pas touche",
       [HEROS, "Puzzle.PutIntoPlay('01103')"], [],
       {"degats": [["01094", 2], ["01103", 0]]},
       main_exclusive=["ua008", "01090"], jouer=["ua008"], cibles=["01094", "01103"]),

    # ---------------------------------------------------------------- ua011 Combo Move
    _c("ua011 Combo Move : identite SANS MARTIAL ARTIST -> 2 degats repartis (1 Rhino, 1 Shocker)",
       "« Deal 2 damage among enemies in play »",
       [HEROS, "Puzzle.PutIntoPlay('01103')"], [],
       {"degats": [["01094", 1], ["01103", 1]]},
       main_exclusive=["ua011", "01088"], jouer=["ua011"], cibles=["01094", "01103"]),
    _c("ua011 Combo Move : identite SANS MARTIAL ARTIST -> 2 degats sur Rhino seul",
       "le meme ennemi peut recevoir tout le montant",
       [HEROS], [],
       {"degats": [["01094", 2]]},
       main_exclusive=["ua011", "01088"], jouer=["ua011"], cibles=["01094", "01094", "01094"]),
    _c("ua011 Combo Move : identite MARTIAL ARTIST (Daredevil) -> 3 degats",
       "« 3 damage instead if your identity has the MARTIAL ARTIST trait »",
       [DD_HEROS], [],
       {"degats": [["01094", 3]]}, heros=DD,
       main_exclusive=["ua011", "01088"], jouer=["ua011"], cibles=["01094", "01094", "01094"]),

    # ---------------------------------------------------------------- ua012 Commando
    _c("ua012 Commando : entre en jeu, defausse un evenement de la main -> Rhino sonne",
       "« After Commando enters play, discard an event from your hand → stun an enemy »",
       [HEROS], [],
       {"en_jeu": ["ua012"], "statuts": [["01094", "Stunned"]], "defausse": ["35018"]},
       main_exclusive=["ua012", "01088", "35018"], payer_avec=["01088"], jouer=["ua012"], cibles=["01094"],
       accepter_choix=True),
    _c("ua012 Commando : CONTRE-CAS, aucun evenement en main -> pas de Reponse, Rhino pas sonne",
       "la defausse est le COUT : impayable sans evenement",
       [HEROS], [],
       {"en_jeu": ["ua012"], "statuts_absents": [["01094", "Stunned"]]},
       main_exclusive=["ua012", "01088", "01090"], payer_avec=["01088"], jouer=["ua012"], cibles=["01094"],
       accepter_choix=True),

    # ---------------------------------------------------------------- ua013 Critical Wound
    _c("ua013 Critical Wound : Shocker attaque par le heros -> attachee, gagne vulnerable : sonne = defausse",
       "« Attach to a minion that your hero attacked this turn » + « non-ELITE -> vulnerable » (sonne = defausse)",
       [HEROS, "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["01103"], "defausse_rencontre": ["01103"]},
       main_exclusive=["ua013", "01088"], jouer=["ua013"], cibles=["01103"],
       declencher_apres=["Puzzle.Stun('01103')"]),
    _c("ua013 Critical Wound : sbire ELITE (Radioactive Man) : pas vulnerable, mais +1 degat par attaque (2 puis 3)",
       "« If attached to a non-ELITE minion » faux : le Stun ne le defausse pas ; « Increase ... from each attack by 1 »",
       [HEROS, "Puzzle.PutIntoPlay('01129')"], ["Puzzle.Attack('01001a')"],
       {"en_jeu": ["01129"], "degats": [["01129", 5]]},
       main_exclusive=["ua013", "01088"], jouer=["ua013"], cibles=["01129"],
       declencher_apres=["Puzzle.Stun('01129')", "Puzzle.Ready('01001a')", "Puzzle.Attack('01001a')"]),
    _c("ua013 Critical Wound : CONTRE-CAS, Shocker PAS attaque ce tour -> injouable, reste en main",
       "la cible doit avoir ete attaquee par votre heros ce tour",
       [HEROS, "Puzzle.PutIntoPlay('01103')"], [],
       {"en_main": ["ua013"], "en_jeu": ["01103"]},
       main_exclusive=["ua013", "01088"], jouer=["ua013"], cibles=["01103"]),

    # ---------------------------------------------------------------- ua014 Daito
    _c("ua014 Daito : sur le heros, attaque de base contre Rhino Tenace -> +1 et percant (Tenace defausse, 3 degats)",
       "« exhaust Daito → this attack deals 1 additional damage and gains piercing »",
       [HEROS, "Puzzle.Tough('01094')"], [],
       {"degats": [["01094", 3]], "exhausted": ["ua014"], "statuts_absents": [["01094", "Tough"]]},
       main_exclusive=["ua014", "01090"], jouer=["ua014"], cibles=["01001a", "01094"], accepter_choix=True,
       declencher_apres=["Puzzle.Attack('01001a')"]),
    _c("ua014 Daito : sur un ALLIE (Leatherhead, ATK 3) -> 4 degats a Rhino",
       "« Attach to a friendly character » : un allie convient ; « attached character attacks »",
       [HEROS, "Puzzle.PutIntoPlay('ua026', under_control=True)"], [],
       {"degats": [["01094", 4]], "exhausted": ["ua014"]},
       main_exclusive=["ua014", "01090"], jouer=["ua014"], cibles=["ua026", "01094"], accepter_choix=True,
       declencher_apres=["Puzzle.Attack('ua026')"]),

    # ---------------------------------------------------------------- ua019 Flow of Battle
    _c("ua019 Flow of Battle : Daredevil attaque et vainc EXACTEMENT Shocker (2 PV restants) -> defaussee, pioche 3",
       "« After you attack and exactly defeat an enemy, discard this card → draw 3 cards »",
       [DD_HEROS, "Puzzle.Damage(Puzzle.PutIntoPlay('01103'), 1)"], [],
       {"hors_jeu": ["01103", "ua019"], "defausse": ["ua019"], "taille_main": 3}, heros=DD,
       main_exclusive=["ua019", "01089"], jouer=["ua019"], cibles=["01103"], accepter_choix=True,
       declencher_apres=["Puzzle.Attack('60001a')"]),
    _c("ua019 Flow of Battle : CONTRE-CAS degats en exces (Shocker a 1 PV) -> rien",
       "« exactly » : un degat de trop et la Reponse ne part pas",
       [DD_HEROS, "Puzzle.Damage(Puzzle.PutIntoPlay('01103'), 2)"], [],
       {"hors_jeu": ["01103"], "en_jeu": ["ua019"], "taille_main": 0}, heros=DD,
       main_exclusive=["ua019", "01089"], jouer=["ua019"], cibles=["01103"], accepter_choix=True,
       declencher_apres=["Puzzle.Attack('60001a')"]),
    _c("ua019 Flow of Battle : Prerequisite (MARTIAL ARTIST) : Spider-Man ne peut pas la jouer (lecture codee Q-UA1)",
       "lecture en attente de reponse : « Prerequisite » = jouable seulement si votre identite a le trait",
       [HEROS], [],
       {"en_main": ["ua019"]},
       main_exclusive=["ua019", "01089"], jouer=["ua019"]),

    # ---------------------------------------------------------------- ua021 Guerilla Trap
    _c("ua021 Guerilla Trap : un sbire engage -> defaussee, sbire hebete, heros camoufle",
       "« After a minion engages you, discard Guerilla Trap → daze that minion and cloak your hero »",
       [HEROS, "Puzzle.PutIntoPlay('ua021', under_control=True)"], ["Puzzle.PutIntoPlay('01103')"],
       {"statuts": [["01103", "Dazed"], ["01001a", "Cloaked"]], "defausse": ["ua021"]},
       main_exclusive=["01088"], accepter_choix=True),
    _c("ua021 Guerilla Trap : soutien NYC controle -> cout 1 (payee avec une seule ressource)",
       "« Reduce the cost to play this card by 1 if you control a NYC support » : tr008 Shell Cycle",
       [HEROS, "Puzzle.PutIntoPlay('tr008', under_control=True)"], [],
       {"en_jeu": ["ua021"]},
       main_exclusive=["ua021", "ua009"], jouer=["ua021"]),
    _c("ua021 Guerilla Trap : CONTRE-CAS sans soutien NYC -> cout 2, une ressource ne suffit pas",
       "la reduction n'existe qu'avec un soutien NYC",
       [HEROS], [],
       {"en_main": ["ua021"]},
       main_exclusive=["ua021", "ua009"], jouer=["ua021"]),

    # ---------------------------------------------------------------- ua025 Kitsune
    _c("ua025 Kitsune : jouee depuis la main, branche « Cloak Kitsune »",
       "« After you play Kitsune from your hand, choose: Cloak Kitsune »",
       [HEROS], [],
       {"statuts": [["ua025", "Cloaked"]]},
       main_exclusive=["ua025", "01088", "01090"], jouer=["ua025"], accepter_choix=True,
       preferer_option="Cloak Kitsune"),
    _c("ua025 Kitsune : branche « Daze an enemy » -> Rhino hebete",
       "seconde branche",
       [HEROS], [],
       {"statuts": [["01094", "Dazed"]], "statuts_absents": [["ua025", "Cloaked"]]},
       main_exclusive=["ua025", "01088", "01090"], jouer=["ua025"], accepter_choix=True, cibles=["01094"],
       preferer_option="Daze an enemy"),
    _c("ua025 Kitsune : CONTRE-CAS mise en jeu par un autre effet (pas « play from your hand ») -> rien",
       "la Reponse exige d'etre JOUEE depuis la main",
       [HEROS, "Puzzle.PutIntoPlay('ua025', under_control=True)"], [],
       {"statuts_absents": [["ua025", "Cloaked"], ["01094", "Dazed"]]},
       main_exclusive=["01088"], accepter_choix=True),

    # ---------------------------------------------------------------- ua026 Leatherhead
    _c("ua026 Leatherhead : 2 degats prealables, attaque et vainc Shocker -> soigne 2, puis 2 consecutifs (2 au total)",
       "« After Leatherhead attacks and defeats a minion, heal 2 damage from him » ; ordre moteur : consecutifs EN "
       "DERNIER (TimingPriority, comme Tigra 01051) : sans la Reponse il finirait a 4",
       [HEROS, "Puzzle.PutIntoPlay('ua026', under_control=True)", "Puzzle.Damage('ua026', 2)",
        "Puzzle.PutIntoPlay('01103')"],
       ["Puzzle.Attack('ua026')"],
       {"hors_jeu": ["01103"], "degats": [["ua026", 2]]}, main_exclusive=["01088"], cibles=["01103"],
       accepter_choix=True),
    _c("ua026 Leatherhead : CONTRE-CAS attaque Rhino (pas vaincu) -> 2 prealables + 2 consecutifs = 4",
       "« defeats a MINION » faux",
       [HEROS, "Puzzle.PutIntoPlay('ua026', under_control=True)", "Puzzle.Damage('ua026', 2)"],
       ["Puzzle.Attack('ua026')"],
       {"hors_jeu": ["ua026"]}, main_exclusive=["01088"], cibles=["01094"],
       accepter_choix=True),

    # ---------------------------------------------------------------- ua030 Nerve Strike
    _c("ua030 Nerve Strike : 2 degats a Rhino puis sonne (branche Stun)",
       "« Deal 2 damage to an enemy. Stun or confuse that enemy »",
       [HEROS], [],
       {"degats": [["01094", 2]], "statuts": [["01094", "Stunned"]], "statuts_absents": [["01094", "Confused"]]},
       main_exclusive=["ua030", "01088", "01090"], jouer=["ua030"], cibles=["01094"], preferer_option="Stun"),
    _c("ua030 Nerve Strike : branche Confuse",
       "seconde branche du « or »",
       [HEROS], [],
       {"degats": [["01094", 2]], "statuts": [["01094", "Confused"]], "statuts_absents": [["01094", "Stunned"]]},
       main_exclusive=["ua030", "01088", "01090"], jouer=["ua030"], cibles=["01094"], preferer_option="Confuse"),
    _c("ua030 Nerve Strike : Discount 1 (MARTIAL ARTIST) : Daredevil la paie 2 (une Energy = YY)",
       "« [star] Discount 1 (MARTIAL ARTIST) » : cout 3 - 1",
       [DD_HEROS], [],
       {"degats": [["01094", 2]]}, heros=DD,
       main_exclusive=["ua030", "01088"], jouer=["ua030"], cibles=["01094"]),
    _c("ua030 Nerve Strike : CONTRE-CAS Spider-Man (pas MARTIAL ARTIST) : 2 ressources ne suffisent pas",
       "sans le trait, le cout reste 3",
       [HEROS], [],
       {"en_main": ["ua030"], "degats": [["01094", 0]]},
       main_exclusive=["ua030", "01088"], jouer=["ua030"], cibles=["01094"]),

    # ---------------------------------------------------------------- ua033 Pete
    _c("ua033 Pete : le heros inflige des degats a Rhino -> Pete incline, 1 pistolet retire, +1 degat",
       "« After you deal damage to an enemy, exhaust Pete and remove 1 pistol counter → deal 1 damage to that enemy »",
       [HEROS, "Puzzle.PutIntoPlay('ua033', under_control=True)"], ["Puzzle.Attack('01001a')"],
       {"degats": [["01094", 3]], "exhausted": ["ua033"], "compteurs": [["ua033", "pistol", 2]]},
       main_exclusive=["01088"], cibles=["01094"], accepter_choix=True),
    _c("ua033 Pete : incline apres usage -> 2e attaque du heros dans le round sans degat en plus",
       "le cout « exhaust Pete » borne l'usage : 2 attaques (heros redresse) -> 3 puis 2 = 5, pistolets 2",
       [HEROS, "Puzzle.PutIntoPlay('ua033', under_control=True)"],
       ["Puzzle.Attack('01001a')", "Puzzle.Ready('01001a')", "Puzzle.Attack('01001a')"],
       {"degats": [["01094", 5]], "compteurs": [["ua033", "pistol", 2]]},
       main_exclusive=["01088"], cibles=["01094"], accepter_choix=True),
    _c("ua033 Pete : evenement d'attaque (Precision Strike) -> PAS de declenchement (lecture codee Q-UA3)",
       "lecture codee : « you » = votre identite (precedent 16032) ; un evenement ne declenche pas Pete",
       [HEROS, "Puzzle.PutIntoPlay('ua033', under_control=True)"], [],
       {"degats": [["01094", 2]], "compteurs": [["ua033", "pistol", 3]]},
       main_exclusive=["35018", "01089"], jouer=["35018"], cibles=["01094"], accepter_choix=True),

    # ---------------------------------------------------------------- ua036 Ray Fillet
    _c("ua036 Ray Fillet : entre en jeu avec 2 munitions ; attaque -> 1 munition retiree, 2 degats en plus",
       "« enters play with 2 ammo counters » + « When Ray Fillet uses a basic power, remove 1 ammo → deal 2 damage »",
       [HEROS, "Puzzle.PutIntoPlay('ua036', under_control=True)"], ["Puzzle.Attack('ua036')"],
       {"degats": [["01094", 4]], "compteurs": [["ua036", "ammo", 1]]},
       main_exclusive=["01088"], cibles=["01094", "01094"], accepter_choix=True),
    _c("ua036 Ray Fillet : CONTRE (basic power THW) -> 2 degats a Rhino, 1 munition retiree",
       "« a basic power » couvre aussi le contre",
       [HEROS, "Puzzle.PutIntoPlay('ua036', under_control=True)"],
       ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Thwart('ua036')"],
       {"degats": [["01094", 2]], "compteurs": [["ua036", "ammo", 1]], "menace": [["01097b", 4]]},
       main_exclusive=["01088"], cibles=["01097b", "01094"], accepter_choix=True),
    _c("ua036 Ray Fillet : 2 munitions seulement : 3e pouvoir de base sans degat en plus",
       "temoin d'epuisement des munitions : 3 attaques (redresse et soigne entre deux) -> 2+2, 2+2, puis 2 seuls",
       [HEROS, "Puzzle.PutIntoPlay('ua036', under_control=True)"],
       ["Puzzle.Attack('ua036')", "Puzzle.Ready('ua036')", "Puzzle.Heal('ua036', 5)", "Puzzle.Attack('ua036')",
        "Puzzle.Ready('ua036')", "Puzzle.Heal('ua036', 5)", "Puzzle.Attack('ua036')"],
       {"degats": [["01094", 10]], "compteurs": [["ua036", "ammo", 0]]},
       main_exclusive=["01088"], cibles=["01094", "01094"], accepter_choix=True),

    # ---------------------------------------------------------------- ua037 Slash
    _c("ua037 Slash : Reponse forcee a l'entree en jeu -> l'identite subit 3 degats (lecture codee Q-UA2)",
       "« After Slash enters play, take 3 damage » : « take » = vous (convention des cartes joueur)",
       [HEROS], [],
       {"en_jeu": ["ua037"], "degats_identite": 3, "degats": [["ua037", 0]]},
       main_exclusive=["ua037", "01088"], jouer=["ua037"]),

    # ---------------------------------------------------------------- ua040 Ujigami
    _c("ua040 Ujigami : 10 dagues ; Action -> 1 dague retiree, 1 degat a Rhino",
       "« enters play with 10 dagger counters » + « Remove 1 dagger counter → deal 1 damage to an enemy »",
       [HEROS, "Puzzle.PutIntoPlay('ua040', under_control=True)"], ["Puzzle.Action('ua040', 'Action')"],
       {"degats": [["01094", 1]], "compteurs": [["ua040", "dagger", 9]]},
       main_exclusive=["01088"], cibles=["01094"]),
    _c("ua040 Ujigami : Limit twice per round : la 3e Action du round est refusee (2 degats, 8 dagues)",
       "TEMOIN D'EPUISEMENT : trois tentatives dans le meme round, la troisieme ne part pas",
       [HEROS, "Puzzle.PutIntoPlay('ua040', under_control=True)"],
       ["Puzzle.Action('ua040', 'Action')", "Puzzle.Action('ua040', 'Action')"],
       {"degats": [["01094", 2]], "compteurs": [["ua040", "dagger", 8]]},
       main_exclusive=["01088"], cibles=["01094"],
       declencher_tolerant=["Puzzle.Action('ua040', 'Action')"]),

    # ---------------------------------------------------------------- ua041 Yagi & Gorogoro
    _c("ua041 Yagi & Gorogoro : attaque percante (Tenace de Rhino defausse, 4 degats) puis defausse 2 cartes",
       "« attacks gain piercing » + « choose to either discard 2 cards from your hand, or remove ... »",
       [HEROS, "Puzzle.PutIntoPlay('ua041', under_control=True)", "Puzzle.Tough('01094')"],
       ["Puzzle.Attack('ua041')"],
       {"degats": [["01094", 4]], "statuts_absents": [["01094", "Tough"]], "taille_main": 0, "en_jeu": ["ua041"]},
       main_exclusive=["01088", "01090"], cibles=["01094", "01088", "01090"],
       preferer_option="Discard 2 cards"),
    _c("ua041 Yagi & Gorogoro : une seule carte en main -> retire de la partie (pas defausse)",
       "branche « discard 2 » impossible : il ne reste que « remove from the game »",
       [HEROS, "Puzzle.PutIntoPlay('ua041', under_control=True)"], ["Puzzle.Attack('ua041')"],
       {"hors_jeu": ["ua041"], "taille_main": 1, "degats": [["01094", 4]]},
       main_exclusive=["01088"], cibles=["01094"]),
]


# ============================================================ bandeaux « ✦ <titre d'origine> » (Q-R1, unique_also)
# Decision de l'utilisateur (16/10/2026) : l'unicite se juge sur les DEUX titres. Exeen ✦ Angela, He-Dude ✦ Two-Gun
# Kid, Rave ✦ Bug. Cout de l'allie paye par la main 01088/01089/01088 (6 ressources).
for _r, _o, _nom in (("ua017", "18011", "Exeen / Angela"), ("ua022", "56010", "He-Dude / Two-Gun Kid"),
                     ("ua035", "16040", "Rave / Bug")):
    CAS += [
        _c(f"{_r} {_nom} : bandeau ✦ : l'officielle {_o} en jeu -> {_r} PAS jouable",
           "Q-R1 : `unique_also` du reskin = titre du bandeau, compare au titre de l'officielle",
           [HEROS, f"Puzzle.Gain('{_r}')", f"Puzzle.PutIntoPlay('{_o}', under_control=True)"], [],
           {"carte": _r, "jouable": False, "en_jeu": 0},
           main=["01088", "01089", "01088"], verifier="max_par_joueur_jouable"),
        _c(f"{_r} {_nom} : bandeau ✦ : sens inverse, {_r} en jeu -> l'officielle {_o} PAS jouable",
           "le titre secondaire bloque dans les deux sens",
           [HEROS, f"Puzzle.Gain('{_o}')", f"Puzzle.PutIntoPlay('{_r}', under_control=True)"], [],
           {"carte": _o, "jouable": False, "en_jeu": 0},
           main=["01088", "01089", "01088"], verifier="max_par_joueur_jouable"),
        _c(f"{_r} {_nom} : TEMOIN, rien en jeu -> {_r} en main est jouable",
           "contre-cas : c'est bien l'officielle en jeu qui bloque",
           [HEROS, f"Puzzle.Gain('{_r}')"], [],
           {"carte": _r, "jouable": True, "en_jeu": 0},
           main=["01088", "01089", "01088"], verifier="max_par_joueur_jouable"),
    ]


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
