# Cas test_capacites du pack tmnt_shinobi_kuji_kiri (Inkwire, TMNT Shinobi, les 20 cartes KUJI-KIRI, prefixe `sj`), 17/10/2026.
# Filtre : `[sj]`. Gabarits : .planning/tmnt/shinobi-kuji-kiri-gabarits.md. Questions : .planning/tmnt/shinobi-kuji-kiri-questions.md.
#
# Conventions (reprises de tools/cas/tmnt_shinobi_paths.py et tmnt_aspect_*.py) :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros (10 PV, ATQ 2, CTR 1, DEF 3, taille de main 5) ;
#  - Rhino 01094 (14 PV, ATQ 2) ; complot principal 01097b ; 01101 Hydra Mercenary (sbire, 3 PV, boost 1, Guard) ;
#  - ressources : 01090 Strength = RR, 01088 Energy = YY, 01089 Genius = BB ;
#  - `main_exclusive` vide la main (APRES la mise en place) : chaque cas sait avec QUOI il paie ;
#  - `CreatePlayerDeck(a, b, c)` / `CreateEncounterDeck(a, b, c)` : la DERNIERE carte donnee est le DESSUS du deck ;
#  - deck rencontre par defaut bourre de « I'm Tough » (01105, sans icone de boost, When Revealed : Rhino tough) pour que
#    aucune carte rencontre ne vienne brouiller la mesure ; icones de boost connues : 01101 = 1, 01102 Sandman = 2,
#    01103 Shocker = 2, 01106 Stampede = 1, 01111 Explosion = 2, 01112 False Alarm = 1, 01121 Weapons Runner = 0 icone + ETOILE (1).
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
COMPLOT = "01097b"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
DECK6 = "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089', '01089')"
SBIRE = "Puzzle.PutIntoPlay('01101')"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[sj] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


def _dispo(nom, pourquoi, mise, carte, type_, nombre, **cle):
    """Cas « l'action est (ou n'est pas) proposee » : `nombre` actions REELLEMENT disponibles."""
    return _c(nom, pourquoi, mise, cle.pop("declencher", []), {"carte": carte, "type": type_, "nombre": nombre},
              verifier="sj_actions_disponibles", **cle)


def _en_jeu(cid):
    return f"Puzzle.PutIntoPlay('{cid}', under_control=True)"


CAS = []

# ========================================================================= sj001 Foresight
CAS += [
    _c("sj001 Foresight : regarde le dessus du deck rencontre, le REVELE (Shocker : 1 degat au heros, sbire en jeu) et pioche 3",
       "« Look at the top card of the encounter deck. You may reveal that card to draw 3 cards » : le dessus (la derniere carte creee) est "
       "01103 Shocker (When Revealed : 1 degat a chaque heros, sbire mis en jeu) ; la carte coute 1 (payee par 01090) : main 0 + 3 piochees",
       [HEROS, SANS_DECK, DECK6, "Puzzle.EmptyEncounterDeck()",
        "Puzzle.CreateEncounterDeck('01105', '01105', '01103')"], [],
       {"en_jeu": ["01103"], "degats_identite": 1, "taille_main": 3, "defausse": ["sj001"]},
       main_exclusive=["sj001", "01090"], jouer=["sj001"], accepter_choix=True, avec_boost=True),
    _c("sj001 Foresight : « You MAY reveal » : en declinant, la carte reste au dessus du deck, rien n'est revele, rien n'est pioche",
       "contre-cas : le joueur repond Passer a l'option « Reveal that card to draw 3 cards » ; Shocker reste dans le deck rencontre, "
       "pas de degat, main 0",
       [HEROS, SANS_DECK, DECK6, "Puzzle.EmptyEncounterDeck()",
        "Puzzle.CreateEncounterDeck('01105', '01105', '01103')"], [],
       {"hors_jeu": ["01103"], "degats_identite": 0, "taille_main": 0, "defausse": ["sj001"],
        "dans_deck_rencontre": ["01103"]},
       main_exclusive=["sj001", "01090"], jouer=["sj001"], choisir_option="Cancel", avec_boost=True),
    _c("sj001 Foresight : la carte revelee est bien CELLE DU DESSUS (la suivante reste dans le deck)",
       "deck rencontre [01105, 01112, 01103] : 01103 (dessus) revele, 01112 False Alarm (dessous) intacte : le heros n'est pas Desoriente",
       [HEROS, SANS_DECK, DECK6, "Puzzle.EmptyEncounterDeck()",
        "Puzzle.CreateEncounterDeck('01105', '01112', '01103')"], [],
       {"en_jeu": ["01103"], "statuts_absents": [["01001a", "Confused"]], "dans_deck_rencontre": ["01112"]},
       main_exclusive=["sj001", "01090"], jouer=["sj001"], accepter_choix=True, avec_boost=True),
    _c("sj001 Foresight : Hero Action, injouable en forme alter-ego (carte restee en main)",
       "forme alter-ego : « Hero Action » refusee ; la carte reste en main, rien n'est revele",
       [SANS_DECK, DECK6, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01103')"], [],
       {"carte": "sj001", "jouable": False, "en_jeu": 0}, verifier="max_par_joueur_jouable",
       main_exclusive=["sj001", "01090"], avec_boost=True),
]

# ========================================================================= sj002 Imbued Weapons
ALLIE = "Puzzle.PutIntoPlay('01059', under_control=True)"   # Jessica Jones : HP 3, ATK 2*, THW 1* (+1 THW par complot annexe en jeu)
CAS += [
    _c("sj002 Imbued Weapons : +1 THW et +1 ATK a l'allie qui la porte",
       "« Attached ally gets +1 THW and +1 ATK » : amelioration jouee sur Jessica Jones (01059), THW et ATK +1 par rapport a l'imprime, "
       "et la carte est attachee a l'allie",
       [HEROS, ALLIE], [],
       {"attributs_carte": [["01059", "thwart", 1], ["01059", "attack", 1]], "attaches": [["01059", "sj002"]]},
       main_exclusive=["sj002", "01090"], jouer=["sj002"], cibles=["01059"]),
    _c("sj002 Imbued Weapons : TEMOIN, sans l'amelioration l'allie garde ses valeurs imprimees",
       "contre-cas : meme montage sans jouer la carte, +0 / +0 (sinon le +1 ne prouverait rien)",
       [HEROS, ALLIE], [],
       {"attributs_carte": [["01059", "thwart", 0], ["01059", "attack", 0]]}),
    _c("sj002 Imbued Weapons : le bonus ne touche PAS la defense ni les PV de l'allie (+1 THW / +1 ATK seulement)",
       "« +1 THW and +1 ATK » : pas de PV, pas de DEF",
       [HEROS, ALLIE], [],
       {"attributs_carte": [["01059", "health", 0]], "pv_max": [["01059", 3]]},
       main_exclusive=["sj002", "01090"], jouer=["sj002"], cibles=["01059"]),
    _c("sj002 Imbued Weapons : « Max 1 per ally » : une seconde copie n'est PAS jouable sur l'allie qui en porte deja une",
       "une copie deja attachee a Jessica Jones, une seconde en main : plus aucune cible legale",
       [HEROS, ALLIE, "Puzzle.AttachReel('sj002', '01059')"], ["Puzzle.CreateHandCards('sj002')"],
       {"carte": "sj002", "jouable": False, "en_jeu": 1}, verifier="max_par_joueur_jouable",
       main_exclusive=["01090", "01090"]),
    _c("sj002 Imbued Weapons : TEMOIN de « Max 1 per ally » : sur un allie sans amelioration la copie est jouable",
       "contre-cas : sans copie deja attachee, la carte de la main est jouable",
       [HEROS, ALLIE], ["Puzzle.CreateHandCards('sj002')"],
       {"carte": "sj002", "jouable": True, "en_jeu": 0}, verifier="max_par_joueur_jouable",
       main_exclusive=["01090", "01090"]),
]

# ========================================================================= sj003 Yang
CAS += [
    _c("sj003 Yang : 2 degats a un ennemi PUIS (premier choix) Sonne un ennemi",
       "« Deal 2 damage to an enemy. Choose: Stun an enemy » : Rhino prend 2 degats et est Sonne (premiere option du choix)",
       [HEROS], [],
       {"degats": [["01094", 2]], "statuts": [["01094", "Stunned"]], "statuts_absents": [["01001a", "Tough"]],
        "defausse": ["sj003"]},
       main_exclusive=["sj003", "01090"], jouer=["sj003"], cibles=["01094"]),
    _c("sj003 Yang : 2 degats a un ennemi PUIS (second choix) un statut Coriace a un personnage AMI (le heros)",
       "meme montage, option « Give a friendly character a tough status card » : le heros devient Coriace, Rhino n'est PAS Sonne (une seule option)",
       [HEROS], [],
       {"degats": [["01094", 2]], "statuts": [["01001a", "Tough"]], "statuts_absents": [["01094", "Stunned"]]},
       main_exclusive=["sj003", "01090"], jouer=["sj003"], cibles=["01094"],
       choisir_option="Give_a_friendly_character_a_tough_status_card"),
    _c("sj003 Yang : les 2 degats sont des DEGATS DIRECTS : l'ATQ du heros (2) n'est pas ajoutee",
       "Hydra Mercenary (3 PV) prend exactement 2 degats et survit ; une attaque de base de Spider-Man (ATQ 2) en ajouterait",
       [HEROS, SBIRE], [],
       {"degats": [["01101", 2]], "statuts": [["01101", "Stunned"]]},
       main_exclusive=["sj003", "01090"], jouer=["sj003"], cibles=["01101"]),
    _c("sj003 Yang : « Stun AN enemy » : le Sonne peut viser un AUTRE ennemi que celui qui a pris les degats",
       "Hydra Mercenary est DEJA Sonne et prend les 2 degats : le Sonne ne peut plus le viser, il part sur Rhino (la seule cible legale restante)",
       [HEROS, SBIRE, "Puzzle.Stun('01101')"], [],
       {"degats": [["01101", 2], ["01094", 0]], "statuts": [["01094", "Stunned"]]},
       main_exclusive=["sj003", "01090"], jouer=["sj003"], cibles=["01101"]),
    _c("sj003 Yang : Hero Action, injouable en alter-ego",
       "forme alter-ego : refusee, la carte reste en main",
       [], [], {"carte": "sj003", "jouable": False, "en_jeu": 0}, verifier="max_par_joueur_jouable",
       main_exclusive=["sj003", "01090"]),
]

# ========================================================================= sj004 Yin
CAS += [
    _c("sj004 Yin : soigne 2 du personnage ami choisi PUIS (premier choix) camoufle un personnage ami",
       "heros a 4 degats : 4 -> 2 (soin de 2), puis Cloaked sur le heros",
       [HEROS, "Puzzle.Damage('01001a', 4)"], [],
       {"degats_identite": 2, "statuts": [["01001a", "Cloaked"]], "statuts_absents": [["01094", "Confused"]]},
       main_exclusive=["sj004", "01088"], jouer=["sj004"], cibles=["01001a"]),
    _c("sj004 Yin : soigne 2 PUIS (second choix) desoriente un ennemi, SANS camoufler",
       "meme montage, option « Confuse an enemy » : Rhino Desoriente, le heros n'est pas Cloaked (une seule option)",
       [HEROS, "Puzzle.Damage('01001a', 4)"], [],
       {"degats_identite": 2, "statuts": [["01094", "Confused"]], "statuts_absents": [["01001a", "Cloaked"]]},
       main_exclusive=["sj004", "01088"], jouer=["sj004"], cibles=["01001a", "01094"], choisir_option="Confuse_an_enemy"),
    _c("sj004 Yin : le soin est PLAFONNE a ce qu'il y a a soigner (1 degat -> 0, pas de PV en trop) et le choix reste faisable",
       "heros a 1 degat : soin de 2 ramene a 0 degat ; Cloaked quand meme (le « Choose » ne depend pas du soin)",
       [HEROS, "Puzzle.Damage('01001a', 1)"], [],
       {"degats_identite": 0, "statuts": [["01001a", "Cloaked"]]},
       main_exclusive=["sj004", "01088"], jouer=["sj004"], cibles=["01001a"]),
    _c("sj004 Yin : « Cloak A friendly character » : un allie peut etre camoufle a la place du heros",
       "Jessica Jones (allie) soignee de 2 (3 PV, 2 degats) et camouflee ; le heros ne l'est pas",
       [HEROS, ALLIE, "Puzzle.Damage('01059', 2)"], [],
       {"degats": [["01059", 0]], "statuts": [["01059", "Cloaked"]], "statuts_absents": [["01001a", "Cloaked"]]},
       main_exclusive=["sj004", "01088"], jouer=["sj004"], cibles=["01059"]),
    _c("sj004 Yin : Hero Action, injouable en alter-ego",
       "forme alter-ego : refusee", [], [], {"carte": "sj004", "jouable": False, "en_jeu": 0},
       verifier="max_par_joueur_jouable", main_exclusive=["sj004", "01088"]),
]

# ========================================================================= sj005 Tai Chi
CAS += [
    _c("sj005 Tai Chi : depensee pour une carte SPELL (Foresight, cout 1), pioche 1 carte",
       "« After you spend this card on a SPELL card, draw 1 card » : main de depart = Foresight + Tai Chi ; Foresight payee par Tai Chi (wild) ; "
       "Foresight regarde sans reveler (Cancel) : main = 1 carte piochee grace a Tai Chi",
       [HEROS, SANS_DECK, DECK6], [],
       {"defausse": ["sj001", "sj005"], "taille_main": 1},
       main_exclusive=["sj001", "sj005"], jouer=["sj001"], payer_avec=["sj005"], choisir_option="Cancel"),
    _c("sj005 Tai Chi : depensee pour une carte NON SPELL (Armored Vest, cout 1), ne pioche PAS",
       "contre-cas : 01081 n'a pas le trait SPELL ; main apres paiement : 0",
       [HEROS, SANS_DECK, DECK6], [],
       {"defausse": ["sj005"], "en_jeu": ["01081"], "taille_main": 0},
       main_exclusive=["01081", "sj005"], jouer=["01081"], payer_avec=["sj005"]),
    _c("sj005 Tai Chi : TEMOIN, la meme carte SPELL payee avec une AUTRE ressource (Strength) ne fait rien piocher",
       "Foresight payee par 01090 (RR) ; Tai Chi reste en main : main = Tai Chi seule (1 carte), aucune pioche",
       [HEROS, SANS_DECK, DECK6], [],
       {"en_main": ["sj005"], "taille_main": 1, "defausse": ["sj001", "01090"]},
       main_exclusive=["sj001", "01090", "sj005"], jouer=["sj001"], payer_avec=["01090"], choisir_option="Cancel"),
    _c("sj005 Tai Chi : une carte SPELL qui n'est PAS un evenement (amelioration Imbued Weapons) payee par Tai Chi pioche aussi",
       "« on a SPELL card » : tout type de carte au trait SPELL ; sj002 (amelioration, cout 1) payee par Tai Chi : 1 carte piochee",
       [HEROS, ALLIE, SANS_DECK, DECK6], [],
       {"defausse": ["sj005"], "en_jeu": ["sj002"], "taille_main": 1},
       main_exclusive=["sj002", "sj005"], jouer=["sj002"], payer_avec=["sj005"], cibles=["01059"]),
]

# ========================================================================= sj006 Enthrall
SHOCKER = "Puzzle.PutIntoPlay('01103')"   # Shocker : sbire non ELITE, 3 PV, ATQ 2, SCH 1
CAS += [
    _c("sj006 Enthrall : un sbire non ELITE passe sous le controle du joueur comme allie CONTROLLED (THW = SCH imprime, ATQ, PV, texte vide)",
       "Shocker (3 PV, ATQ 2, SCH 1, When Revealed : 1 degat a chaque heros) devient un allie du joueur : trait CONTROLLED, THW 1, ATQ 2, PV 3, "
       "3 degats consequentiels apres une attaque ou un contre ; il n'est plus un sbire",
       [HEROS, SHOCKER], [],
       {"nom": "Shocker", "thw": 1, "atk": 2, "pv": 3, "conseq_atk": 3, "conseq_thw": 3, "trait": "CONTROLLED", "sbire": False},
       verifier="sj_allie_controle", main_exclusive=["sj006", "01090", "01089"], jouer=["sj006"], cibles=["01103"]),
    _c("sj006 Enthrall : « blank textbox » : le sbire controle n'a plus le texte du Shocker (Surge / When Revealed absents) mais garde ses traits",
       "le gabarit d'allie ne porte aucune capacite propre : aucune des capacites de Shocker n'est enregistree",
       [HEROS, SHOCKER], [],
       {"nom": "Shocker", "sans_capacite_propre": True},
       verifier="sj_allie_controle", main_exclusive=["sj006", "01090", "01089"], jouer=["sj006"], cibles=["01103"]),
    _c("sj006 Enthrall : TEMOIN de « blank textbox » : le sbire Shocker NON controle porte, lui, sa capacite When Revealed",
       "sans Enthrall le sbire garde son texte : la mesure « sans capacite propre » discrimine bien",
       [HEROS, SHOCKER], [],
       {"nom": "Shocker", "temoin_avec_capacite_revelee": True}, verifier="sj_allie_controle"),
    _c("sj006 Enthrall : l'allie controle ATTAQUE : 2 degats au vilain puis 3 degats CONSEQUENTIELS a l'allie (3 PV : vaincu)",
       "Shocker allie attaque Rhino (ATQ 2) ; apres son attaque il subit 3 degats consequentiels : 3 PV -> defaussee ; Rhino a 2 degats",
       [HEROS, SHOCKER], [],
       {"degats": [["01094", 2]], "allie_vaincu": "Shocker"},
       verifier="sj_apres_attaque_de_l_allie", main_exclusive=["sj006", "01090", "01089"], jouer=["sj006"], cibles=["01103"],
       declencher_apres=["Puzzle.Attack('Shocker')"]),
    _c("sj006 Enthrall : l'allie controle CONTRE : 1 menace retiree (THW = SCH imprime 1) puis 3 degats CONSEQUENTIELS (vaincu)",
       "Shocker allie contre le complot principal (5 -> 4) ; « after it thwarts OR attacks » : 3 degats consequentiels apres le contre aussi",
       [HEROS, SHOCKER], ["Puzzle.SetThreat('01097b', 5)"],
       {"menace": [["01097b", 4]], "allie_vaincu": "Shocker"},
       verifier="sj_apres_attaque_de_l_allie", main_exclusive=["sj006", "01090", "01089"], jouer=["sj006"], cibles=["01103"],
       declencher_apres=["Puzzle.Thwart('Shocker')"]),
    _c("sj006 Enthrall : TEMOIN, un sbire ELITE (Sandman) n'est PAS une cible legale",
       "Sandman est ELITE : Enthrall injouable (aucune cible), alors que Shocker (non ELITE) l'est",
       [HEROS, "Puzzle.PutIntoPlay('01102')"], ["Puzzle.CreateHandCards('sj006')"],
       {"carte": "sj006", "jouable": False, "en_jeu": 0}, verifier="max_par_joueur_jouable",
       main_exclusive=["01090", "01089"]),
    _c("sj006 Enthrall : TEMOIN positif, avec un sbire non ELITE en jeu la carte est jouable",
       "Shocker en jeu : Enthrall jouable (cout 3, deux ressources en main)",
       [HEROS, SHOCKER], ["Puzzle.CreateHandCards('sj006')"],
       {"carte": "sj006", "jouable": True, "en_jeu": 0}, verifier="max_par_joueur_jouable",
       main_exclusive=["01090", "01089"]),
    _c("sj006 Enthrall : quand Enthrall quitte le jeu, l'allie redevient le sbire (Shocker, 3 PV)",
       "Enthrall defaussee : l'allie CONTROLLED redevient un sbire Shocker en jeu et n'est plus controle",
       [HEROS, SHOCKER], [],
       {"nom": "Shocker", "sbire": True},
       verifier="sj_allie_controle", main_exclusive=["sj006", "01090", "01089"], jouer=["sj006"], cibles=["01103"],
       declencher_apres=["Puzzle.Discard('sj006')"]),
]

# ========================================================================= sj007 Ring of Protection
# Ring jouee pour de vrai (cout 1, attachee a l'identite), puis une traitrise REVELEE par `Puzzle.Reveal` (deposee sur le dessus
# du deck rencontre puis revelee). Deck joueur : 6 Genius, la taille se lit apres la defausse (6 -> 6 - icones).
def _ring(nom, pourquoi, mise, revelee, attendu, **cle):
    return _c(nom, pourquoi, [HEROS, SANS_DECK, DECK6, "Puzzle.EmptyEncounterDiscardPile()"] + mise, [], attendu,
              declencher_apres=[f"Puzzle.Reveal('{revelee}')"], verifier="sj_etat_rencontre", avec_boost=True,
              main_exclusive=["sj007", "01090"], jouer=["sj007"], **cle)


CAS += [
    _ring("sj007 Ring of Protection : une traitrise a 1 icone de boost (False Alarm) est ANNULEE et defaussee, 1 carte du deck joueur defaussee",
          "« cancel all of the effects of that treachery and discard it. Discard cards from the top of your deck for each icon » : False Alarm "
          "(Desoriente le heros, boost 1) : le heros n'est PAS Desoriente, la traitrise est dans la defausse rencontre, Ring defaussee (cout), deck 6 -> 5",
          [], "01112",
          {"statuts_absents": [["01001a", "Confused"]], "defausse_rencontre": ["01112"], "defausse": ["sj007"],
           "taille_deck_joueur": 5, "hors_jeu": ["sj007"]}),
    _ring("sj007 Ring of Protection : une traitrise a 2 icones (Explosion) fait defausser 2 cartes du deck joueur",
          "Explosion (boost 2) : deck 6 -> 4, traitrise defaussee, Ring defaussee",
          [], "01111",
          {"defausse_rencontre": ["01111"], "defausse": ["sj007"], "taille_deck_joueur": 4, "hors_jeu": ["sj007"]}),
    _ring("sj007 Ring of Protection : l'ETOILE de boost compte comme une icone (Sonic Boom : 0 icone + [star] Boost) : 1 carte defaussee, heros non epuise",
          "« for each icon ([star] and [boost]) » : Sonic Boom a 0 icone [boost] et un effet [star] Boost = 1 icone ; son When Revealed (epuiser chaque personnage) "
          "est annule : le heros reste pret ; deck 6 -> 5",
          [], "01123",
          {"pret": ["01001a"], "defausse_rencontre": ["01123"], "taille_deck_joueur": 5, "hors_jeu": ["sj007"]}),
    _ring("sj007 Ring of Protection : une traitrise SANS icone (I'm Tough) est annulee, mais AUCUNE carte du deck n'est defaussee",
          "« I'm Tough » (0 icone, When Revealed : Rhino gagne Coriace) annulee : Rhino n'est pas Coriace ; deck inchange (6) ; Ring quand meme defaussee",
          [], "01105",
          {"statuts_absents": [["01094", "Tough"]], "defausse_rencontre": ["01105"], "taille_deck_joueur": 6, "hors_jeu": ["sj007"]}),
    _c("sj007 Ring of Protection : TEMOIN, sans Ring la meme traitrise (False Alarm) fait effet : le heros est Desoriente, deck intact",
       "contre-cas des quatre precedents : pas de Ring, False Alarm resolue",
       [HEROS, SANS_DECK, DECK6, "Puzzle.EmptyEncounterDiscardPile()"], ["Puzzle.Reveal('01112')"],
       {"statuts": [["01001a", "Confused"]], "taille_deck_joueur": 6}, verifier="sj_etat_rencontre", avec_boost=True),
    _c("sj007 Ring of Protection : ne reagit QU'A une traitrise : un sbire revele (Hydra Mercenary) n'est pas annule, Ring reste en jeu",
       "« When a TREACHERY is revealed » : 01101 (sbire) entre en jeu engage ; Ring toujours en jeu, deck intact",
       [HEROS, SANS_DECK, DECK6, "Puzzle.EmptyEncounterDiscardPile()"], [],
       {"en_jeu": ["sj007", "01101"], "taille_deck_joueur": 6}, verifier="sj_etat_rencontre", avec_boost=True,
       main_exclusive=["sj007", "01090"], jouer=["sj007"], declencher_apres=["Puzzle.Reveal('01101')"]),
    _c("sj007 Ring of Protection : « Hero Interrupt » : en forme alter-ego Ring reste en jeu et la traitrise fait effet",
       "alter-ego : False Alarm Desoriente l'identite, Ring (en jeu, jouee en alter-ego) n'est pas proposee",
       [SANS_DECK, DECK6, "Puzzle.EmptyEncounterDiscardPile()"], [],
       {"statuts": [["01001b", "Confused"]], "en_jeu": ["sj007"], "taille_deck_joueur": 6}, verifier="sj_etat_rencontre", avec_boost=True,
       main_exclusive=["sj007", "01090"], jouer=["sj007"], declencher_apres=["Puzzle.Reveal('01112')"]),
]

# ========================================================================= sj008 Toshokan Arcana
TOSHOKAN = _en_jeu("sj008")
CAS += [
    _c("sj008 Toshokan Arcana : defausse du dessus du deck JUSQU'A une carte SPELL, la prend en main (cartes sautees restees defaussees)",
       "deck (dessus -> dessous) : Genius, Strength, Imbued Weapons (SPELL), Energy : defausse Genius et Strength, ajoute sj002 a la main ; Energy reste (deck 1) ; "
       "le soutien est incline",
       [HEROS, TOSHOKAN, SANS_DECK, "Puzzle.CreatePlayerDeck('01088', 'sj002', '01090', '01089')", "Puzzle.EmptyPlayerDiscardPile()"],
       ["Puzzle.Action('sj008', 'Action', 0)"],
       {"en_main": ["sj002"], "defausse": ["01089", "01090"], "defausse_joueur": 2, "taille_deck_joueur": 1,
        "exhausted": ["sj008"]}),
    _c("sj008 Toshokan Arcana : s'arrete a la PREMIERE carte SPELL (la seconde SPELL reste dans le deck)",
       "deck (dessus -> dessous) : Strength, Imbued Weapons (SPELL), Yin (SPELL) : seule sj002 est prise, sj004 reste dans le deck",
       [HEROS, TOSHOKAN, SANS_DECK, "Puzzle.CreatePlayerDeck('sj004', 'sj002', '01090')", "Puzzle.EmptyPlayerDiscardPile()"],
       ["Puzzle.Action('sj008', 'Action', 0)"],
       {"en_main": ["sj002"], "absent_main": ["sj004"], "dans_deck_joueur": ["sj004"], "taille_deck_joueur": 1,
        "defausse": ["01090"]}),
    _c("sj008 Toshokan Arcana : une SPELL qui n'est PAS un evenement (amelioration) convient aussi ; un TECH ou une ressource ne conviennent pas",
       "deck (dessus -> dessous) : Energy (ressource), Imbued Weapons (amelioration SPELL), Strength : la ressource est sautee, l'amelioration prise, "
       "Strength reste (le deck ne se vide pas : la regle du deck vide n'intervient pas)",
       [HEROS, TOSHOKAN, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', 'sj002', '01088')", "Puzzle.EmptyPlayerDiscardPile()"],
       ["Puzzle.Action('sj008', 'Action', 0)"],
       {"en_main": ["sj002"], "defausse": ["01088"], "defausse_joueur": 1, "taille_deck_joueur": 1}),
    _c("sj008 Toshokan Arcana : « Action » (sans Hero) : jouable aussi en forme ALTER-EGO",
       "alter-ego : l'action marche, sj002 en main",
       [TOSHOKAN, SANS_DECK, "Puzzle.CreatePlayerDeck('sj002', '01090')", "Puzzle.EmptyPlayerDiscardPile()"],
       ["Puzzle.Action('sj008', 'Action', 0)"],
       {"en_main": ["sj002"], "exhausted": ["sj008"]}),
    _dispo("sj008 Toshokan Arcana : TEMOIN D'EPUISEMENT, apres usage le soutien est incline : plus aucune action ce round",
           "cout = incliner : une fois utilise, 0 action disponible (le soutien reste incline)",
           [HEROS, TOSHOKAN, SANS_DECK, "Puzzle.CreatePlayerDeck('sj002', '01090', 'sj004', '01089')"],
           "sj008", "Action", 0, declencher=["Puzzle.Action('sj008', 'Action', 0)"]),
    _dispo("sj008 Toshokan Arcana : TEMOIN positif, prete, le soutien offre bien 1 action",
           "avant usage : 1 action disponible", [HEROS, TOSHOKAN], "sj008", "Action", 1),
    _c("sj008 Toshokan Arcana : aucune carte SPELL dans le deck : tout le deck est defausse, rien n'est ajoute a la main",
       "deck de 3 cartes sans SPELL : aucune carte SPELL n'arrive en main (la main reste vide), le soutien est incline",
       [HEROS, TOSHOKAN, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01089', '01088')", "Puzzle.EmptyPlayerDiscardPile()", "Puzzle.EmptyHand()"],
       ["Puzzle.Action('sj008', 'Action', 0)"],
       {"taille_main": 0, "exhausted": ["sj008"]}),
]

# ========================================================================= sj010 Flash Ward
# Le heros subit des degats DIRECTS (`Puzzle.Damage`, passe par WhenUnitWouldTakeDamage) avec Flash Ward en main ; deck rencontre
# `[dessous ... dessus]` : les 2 DERNIERES cartes creees sont les 2 du dessus.
def _ward(nom, pourquoi, dessus, degats, attendu, cible="01001a", mise=(), **cle):
    return _c(nom, pourquoi, [HEROS, "Puzzle.EmptyEncounterDiscardPile()", "Puzzle.EmptyEncounterDeck()",
                              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', " + ", ".join(f"'{x}'" for x in dessus) + ")"] + list(mise),
              [f"Puzzle.Damage('{cible}', {degats})"], attendu, verifier="sj_etat_rencontre", avec_boost=True,
              main_exclusive=["sj010", "01090"], **cle)


CAS += [
    _ward("sj010 Flash Ward : 2 cartes du dessus du deck rencontre defaussees (1 + 1 icone) : 2 degats empeches sur 3, le heros en subit 1",
          "dessus : 01101 Hydra Mercenary (boost 1) et 01112 False Alarm (boost 1) : 2 icones -> 2 degats sur 3 empeches ; les deux cartes sont defaussees "
          "(cout), la carte est jouee",
          ["01101", "01112"], 3,
          {"degats_identite": 1, "defausse_rencontre": ["01101", "01112"], "taille_deck_rencontre": 3, "defausse": ["sj010"]}),
    _ward("sj010 Flash Ward : l'ETOILE de boost compte (Weapons Runner : 0 icone + [star] Boost = 1) : 1 degat empeche sur 3",
          "dessus : 01121 Weapons Runner (0 icone [boost], effet [star] Boost) et 01105 : 1 icone au total",
          ["01121", "01105"], 3,
          {"degats_identite": 2, "defausse_rencontre": ["01121", "01105"], "taille_deck_rencontre": 3, "defausse": ["sj010"]}),
    _ward("sj010 Flash Ward : plus d'icones (2 + 2 = 4) que de degats (3) : tout est empeche, pas un point de vie de plus",
          "dessus : Sandman (boost 2) et Shocker (boost 2) : 4 icones pour 3 degats : 0 degat",
          ["01102", "01103"], 3,
          {"degats_identite": 0, "defausse_rencontre": ["01102", "01103"], "defausse": ["sj010"]}),
    _ward("sj010 Flash Ward : aucune icone (deux I'm Tough) : le cout est paye (2 cartes defaussees) mais RIEN n'est empeche",
          "dessus : 01105 et 01105 : 0 icone ; 3 degats subis ; la carte est quand meme jouee",
          ["01105", "01105"], 3,
          {"degats_identite": 3, "taille_deck_rencontre": 3, "defausse": ["sj010"]}),
    _ward("sj010 Flash Ward : protege aussi un ALLIE (« a friendly character ») : Jessica Jones, 2 degats, 2 + 2 icones : aucun degat",
          "allie sous controle du joueur : Flash Ward est proposee et empeche les 2 degats ; le heros est intact",
          ["01102", "01103"], 2,
          {"degats": [["01059", 0]], "degats_identite": 0, "defausse": ["sj010"], "taille_deck_rencontre": 3},
          cible="01059", mise=[ALLIE]),
    _ward("sj010 Flash Ward : TEMOIN, des degats sur un ENNEMI (Rhino) ne declenchent pas Flash Ward : carte en main, deck rencontre intact",
          "« a FRIENDLY character » : Rhino prend 3 degats, aucune interruption ; sj010 reste en main, 8 cartes dans le deck rencontre",
          ["01102", "01103"], 3,
          {"degats": [["01094", 3]], "en_main": ["sj010"], "taille_deck_rencontre": 5}, cible="01094"),
]

# ========================================================================= sj009 Armageddon
FER2 = "Puzzle.ChangeForm('01029b')"    # heros 2 (Iron Man) en forme heros (HS 1 imprime)
CAS += [
    _c("sj009 Armageddon : a l'entree en jeu, CHAQUE joueur recoit 1 carte rencontre face cachee (solo : 1) ; menace de depart 5 par heros",
       "« After Armageddon enters play, deal each player 1 facedown encounter card » : 1 carte distribuee, menace de depart « 5* » = 5 pour 1 heros",
       [HEROS], [],
       {"dealt": [1], "menace": [["sj009", 5]], "en_jeu": ["sj009"], "delta_main": [0]},
       verifier="sj_armageddon", main_exclusive=["sj009"], jouer=["sj009"]),
    _c("sj009 Armageddon : a DEUX joueurs, chacun des deux reçoit 1 carte face cachee ; menace de depart 5 x 2 = 10",
       "« each player » : 2 cartes distribuees au total (une par joueur), menace 10 pour 2 heros",
       [HEROS, FER2], [],
       {"dealt": [1, 1], "menace": [["sj009", 10]], "en_jeu": ["sj009"]},
       verifier="sj_armageddon", main_exclusive=["sj009"], jouer=["sj009"], heros2="iron_man"),
    _c("sj009 Armageddon : TEMOIN, tant qu'Armageddon est EN JEU (pas dans la pile de victoire) les identites n'ont AUCUN bonus de main",
       "« While Armageddon is in the VICTORY DISPLAY » : en jeu, +0 pour les deux heros",
       [HEROS, FER2], [],
       {"delta_main": [0, 0], "en_jeu": ["sj009"]},
       verifier="sj_armageddon", main_exclusive=["sj009"], jouer=["sj009"], heros2="iron_man"),
    _c("sj009 Armageddon : dans la pile de victoire, CHAQUE identite en forme heros gagne +1 taille de main (les deux heros)",
       "Armageddon jouee (menace 10 a deux heros) puis vaincue (10 menaces retirees) : dans la pile de victoire, Spider-Man (5 -> 6) et Iron Man (1 -> 2), "
       "tous deux en forme heros",
       [HEROS, FER2], [],
       {"delta_main": [1, 1], "victoire": True, "hors_jeu": ["sj009"]},
       verifier="sj_armageddon", heros2="iron_man", main_exclusive=["sj009"], jouer=["sj009"],
       declencher_apres=["Puzzle.PlaceThreat('sj009', -10)"]),
    _c("sj009 Armageddon : « IN HERO FORM » : l'identite en forme ALTER-EGO ne gagne rien (Iron Man alter-ego : +0, Spider-Man heros : +1)",
       "pile de victoire (Armageddon vaincue) : seul le heros en forme heros gagne +1",
       [HEROS], [],
       {"delta_main": [1, 0], "victoire": True, "hors_jeu": ["sj009"]},
       verifier="sj_armageddon", heros2="iron_man", main_exclusive=["sj009"], jouer=["sj009"],
       declencher_apres=["Puzzle.PlaceThreat('sj009', -10)"]),
    _c("sj009 Armageddon : TEMOIN, sans Armageddon aucun bonus de main",
       "meme montage sans la carte : +0 pour les deux", [HEROS, FER2], [],
       {"delta_main": [0, 0]}, verifier="sj_armageddon", heros2="iron_man"),
    _c("sj009 Armageddon : toute la menace retiree -> Armageddon est VAINCUE et va dans la pile de victoire (Victory 0), le bonus de main s'applique alors",
       "jouee (5 menace) puis 5 menace retiree : dans la pile de victoire (plus en jeu), Spider-Man heros : taille de main 5 -> 6",
       [HEROS], ["Puzzle.PlaceThreat('sj009', -5)"],
       {"victoire": True, "hors_jeu": ["sj009"], "delta_main": [1]},
       verifier="sj_armageddon", main_exclusive=["sj009"], jouer=["sj009"], declencher_apres=["Puzzle.PlaceThreat('sj009', -5)"]),
]

# ========================================================================= sj011 Unravel
CAS += [
    _c("sj011 Unravel : defausse 3 du deck joueur ET 3 du deck rencontre (cout), puis 3 degats a un ennemi ET 3 menaces retirees d'une manigance",
       "deck joueur 5 -> 2, deck rencontre 6 -> 3 (3 cartes en defausse rencontre), Rhino : 3 degats, complot principal : 5 -> 2",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089')", "Puzzle.EmptyEncounterDiscardPile()",
        "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105')"],
       ["Puzzle.SetThreat('01097b', 5)"],
       {"degats": [["01094", 3]], "menace": [["01097b", 2]], "taille_deck_joueur": 2, "taille_deck_rencontre": 3,
        "taille_defausse_rencontre": 3, "defausse": ["sj011"]},
       verifier="sj_etat_rencontre", avec_boost=True, main_exclusive=["sj011", "01088"], jouer=["sj011"], cibles=["01094", "01097b"]),
    _c("sj011 Unravel : les deux effets sont independants : l'ennemi vise est un SBIRE (Hydra Mercenary vaincu par les 3 degats) et la manigance annexe perd 3 menaces",
       "Hydra Mercenary (3 PV) vaincu, Breakin' & Takin' (01107) 5 -> 2, complot principal intact",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089')", "Puzzle.EmptyEncounterDiscardPile()",
        "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105')", SBIRE,
        "Puzzle.PutIntoPlay('01107')"],
       ["Puzzle.SetThreat('01107', 5)"],
       {"hors_jeu": ["01101"], "menace": [["01107", 2]], "taille_deck_joueur": 1, "taille_deck_rencontre": 1,
        "defausse": ["sj011"]},
       verifier="sj_etat_rencontre", avec_boost=True, main_exclusive=["sj011", "01088"], jouer=["sj011"], cibles=["01101", "01107"]),
    _c("sj011 Unravel : Hero Action, injouable en forme alter-ego (aucune carte defaussee)",
       "alter-ego : refusee, la carte reste en main, deck inchange",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089')"], [],
       {"carte": "sj011", "jouable": False, "en_jeu": 0}, verifier="max_par_joueur_jouable", main_exclusive=["sj011", "01088"]),
]

# ========================================================================= sj012 A Thin Place
THIN = _en_jeu("sj012")
CAS += [
    _c("sj012 A Thin Place : Reponse : apres avoir joue une carte Kuji-Kiri DEPUIS LA MAIN (Foresight), le soutien s'incline et recoit 1 compteur mystic",
       "« After you play a Kuji-Kiri card from your hand, exhaust A Thin Place -> place 1 mystic counter here » : sj001 jouee (Cancel a son option), "
       "1 compteur mystic, soutien incline",
       [HEROS, THIN, SANS_DECK, DECK6], [],
       {"compteurs": [["sj012", "mystic", 1]], "exhausted": ["sj012"], "defausse": ["sj001"]},
       main_exclusive=["sj001", "01090"], jouer=["sj001"], choisir_option="Cancel"),
    _c("sj012 A Thin Place : TEMOIN, une carte NON Kuji-Kiri (Armored Vest) jouee de la main ne donne aucun compteur",
       "01081 n'est pas une carte Kuji-Kiri : 0 compteur, le soutien reste pret",
       [HEROS, THIN, SANS_DECK, DECK6], [],
       {"compteurs": [["sj012", "mystic", 0]], "pret": ["sj012"], "en_jeu": ["01081"]},
       main_exclusive=["01081", "01090"], jouer=["01081"]),
    _c("sj012 A Thin Place : TEMOIN D'EPUISEMENT, une SECONDE carte Kuji-Kiri dans le meme round ne donne pas de second compteur (le soutien est incline)",
       "deux Foresight de la main : la premiere donne le compteur et incline le soutien, la seconde, jouee soutien incline, n'en donne pas : 1 compteur",
       [HEROS, THIN, SANS_DECK, DECK6], [],
       {"compteurs": [["sj012", "mystic", 1]], "exhausted": ["sj012"], "defausse": ["sj001"]},
       main_exclusive=["sj001", "sj001", "01090", "01090"], jouer=["sj001", "sj001"], choisir_option="Cancel"),
    _c("sj012 A Thin Place : la Reponse n'est PAS une Hero Response : jouee en ALTER-EGO (Kirby's Pencil, Kuji-Kiri cout 0), elle donne aussi un compteur",
       "alter-ego : sj013 (amelioration Kuji-Kiri, cout 0) jouee de la main : 1 compteur mystic",
       [THIN, SANS_DECK, DECK6], [],
       {"compteurs": [["sj012", "mystic", 1]], "exhausted": ["sj012"], "en_jeu": ["sj013"]},
       main_exclusive=["sj013"], jouer=["sj013"]),
    _c("sj012 A Thin Place : Alter-Ego Action : 3 compteurs retires et soutien incline -> pioche 2 cartes ET soigne 2 de l'identite",
       "alter-ego, 3 compteurs mystic, identite a 3 degats, main vide : apres l'action 0 compteur, main 2, degats 3 -> 1, soutien incline",
       [THIN, SANS_DECK, DECK6, "Puzzle.Counter('sj012', 'mystic', 3)", "Puzzle.Damage('01001b', 3)", "Puzzle.EmptyHand()"],
       ["Puzzle.Action('sj012', 'AlterEgoAction', 0)"],
       {"compteurs": [["sj012", "mystic", 0]], "taille_main": 2, "degats_identite": 1, "exhausted": ["sj012"]}),
    _dispo("sj012 A Thin Place : seulement 2 compteurs : l'Alter-Ego Action n'est PAS proposee (cout : 3 compteurs)",
           "cout impayable", [THIN, "Puzzle.Counter('sj012', 'mystic', 2)"], "sj012", "AlterEgoAction", 0),
    _dispo("sj012 A Thin Place : 3 compteurs, alter-ego, soutien pret : l'action est proposee (temoin positif)",
           "contre-cas des quatre suivants", [THIN, "Puzzle.Counter('sj012', 'mystic', 3)"], "sj012", "AlterEgoAction", 1),
    _dispo("sj012 A Thin Place : 3 compteurs mais forme HEROS : l'Alter-Ego Action n'est PAS proposee",
           "« Alter-Ego Action » : alter-ego seulement", [HEROS, THIN, "Puzzle.Counter('sj012', 'mystic', 3)"],
           "sj012", "AlterEgoAction", 0),
    _dispo("sj012 A Thin Place : soutien deja INCLINE : l'Alter-Ego Action n'est pas proposee malgre 3 compteurs (cout : incliner)",
           "« Exhaust A Thin Place AND remove 3 counters » : les deux coûts",
           [THIN, "Puzzle.Counter('sj012', 'mystic', 3)", "Puzzle.Exhaust('sj012')"], "sj012", "AlterEgoAction", 0),
]

# ========================================================================= sj013 Kirby's Pencil
# Le Crayon est JOUE (cout 0, attache a l'identite), puis sa Hero Action est declenchee ; la carte a jouer est designee par `cibles`.
def _crayon(nom, pourquoi, mise, jouee, attendu, **cle):
    return _c(nom, pourquoi, [HEROS, "Puzzle.EmptyEncounterDiscardPile()", "Puzzle.EmptyEncounterDeck()",
                              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105')"] + mise, [], attendu,
              verifier="sj_crayon", avec_boost=True, main_exclusive=["sj013", jouee], jouer=["sj013"], cibles=[jouee],
              declencher_apres=["Puzzle.Action('sj013', 'HeroAction', 0)"], **cle)


CAS += [
    _crayon("sj013 Kirby's Pencil : joue une carte de la main SANS payer son cout (Armored Vest, cout 1, aucune ressource en main), defausse 1 carte rencontre, "
            "puis le Crayon est RETIRE DU JEU",
            "« Play a card from your hand, ignoring its resource cost. Discard cards from the top of the encounter deck equal to that card's printed cost. Then, remove "
            "this card from the game » : 01081 en jeu, deck rencontre 6 -> 5, sj013 dans la zone des cartes retirees (pas dans la defausse)",
            [], "01081",
            {"en_jeu": ["01081"], "hors_jeu": ["sj013"], "taille_deck_rencontre": 5, "taille_defausse_rencontre": 1, "taille_main": 0,
             "retiree": True}),
    _crayon("sj013 Kirby's Pencil : cout IMPRIME 3 (Jessica Jones, allie) : joue gratuitement, 3 cartes rencontre defaussees",
            "01059 (cout 3) : allie en jeu sans depenser de ressource ; deck rencontre 6 -> 3",
            [], "01059",
            {"en_jeu": ["01059"], "taille_deck_rencontre": 3, "taille_defausse_rencontre": 3, "retiree": True}),
    _crayon("sj013 Kirby's Pencil : cout imprime 0 (A Thin Place) : aucune carte rencontre defaussee, le Crayon part quand meme",
            "sj012 (cout 0) : soutien en jeu, deck rencontre intact (6), Crayon retire",
            [], "sj012",
            {"en_jeu": ["sj012"], "taille_deck_rencontre": 6, "taille_defausse_rencontre": 0, "retiree": True}),
    _c("sj013 Kirby's Pencil : TEMOIN, sans le Crayon la meme carte (Armored Vest) n'est PAS jouable gratuitement (aucune ressource en main)",
       "main = 01081 seule : le cout 1 ne peut pas etre paye, la carte reste en main et n'entre pas en jeu",
       [HEROS], [], {"en_main": ["01081"], "hors_jeu": ["01081"]}, main_exclusive=["01081"], jouer=["01081"]),
    _c("sj013 Kirby's Pencil : Hero Action NON proposee en alter-ego",
       "alter-ego : le Crayon (en jeu) n'offre aucune Hero Action",
       [], [], {"carte": "sj013", "type": "HeroAction", "nombre": 0}, verifier="sj_actions_disponibles",
       main_exclusive=["sj013", "01081"], jouer=["sj013"]),
    _c("sj013 Kirby's Pencil : TEMOIN D'EPUISEMENT, une fois retire le Crayon n'est plus en jeu : plus aucune action, aucun second usage",
       "apres usage : sj013 introuvable en jeu (retiree), 01081 en jeu",
       [HEROS, "Puzzle.EmptyEncounterDiscardPile()", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"], [],
       {"en_jeu": ["01081"], "hors_jeu": ["sj013"], "retiree": True}, verifier="sj_crayon", avec_boost=True,
       main_exclusive=["sj013", "01081", "01081"], jouer=["sj013"], cibles=["01081"],
       declencher_apres=["Puzzle.Action('sj013', 'HeroAction', 0)"]),
]

# ========================================================================= sj014 Kuji-Kaiju
CHAT = "Puzzle.PutIntoPlay('01002', under_control=True)"    # Black Cat : ATK 1 SANS icone consequentielle, THW 1*, 2 PV
CAS += [
    _c("sj014 Kuji-Kaiju : l'allie qui la porte gagne les traits FERAL et GIANT, +2 PV et +2 ATK (pas de bonus de THW)",
       "Jessica Jones (3 PV, ATQ 2, THW 1) : 5 PV, ATQ 4, THW inchange, FERAL et GIANT",
       [HEROS, ALLIE], [],
       {"pv_max": [["01059", 5]], "attributs_carte": [["01059", "attack", 2], ["01059", "thwart", 0]],
        "traits_de": [["01059", "FERAL"], ["01059", "GIANT"]], "attaches": [["01059", "sj014"]]},
       main_exclusive=["sj014", "01088"], jouer=["sj014"], cibles=["01059"]),
    _c("sj014 Kuji-Kaiju : TEMOIN, sans la carte l'allie n'a ni FERAL ni GIANT et ses valeurs imprimees",
       "contre-cas : 3 PV, ATQ +0, pas de trait",
       [HEROS, ALLIE], [],
       {"pv_max": [["01059", 3]], "attributs_carte": [["01059", "attack", 0]], "carte": "01059",
        "sans_traits": ["FERAL", "GIANT"]}, verifier="sj_sans_traits"),
    _c("sj014 Kuji-Kaiju : « +1 consequential damage after it attacks » : Jessica (1 icone imprimee) attaque a ATQ 4 et subit 1 + 1 = 2 degats consequentiels",
       "Rhino prend 4, Jessica (5 PV) prend 2",
       [HEROS, ALLIE], [],
       {"degats": [["01094", 4], ["01059", 2]]},
       main_exclusive=["sj014", "01088"], jouer=["sj014"], cibles=["01059"], declencher_apres=["Puzzle.Attack('01059')"]),
    _c("sj014 Kuji-Kaiju : TEMOIN, sans la carte Jessica attaque a ATQ 2 et ne subit que 1 degat consequentiel",
       "Rhino prend 2, Jessica prend 1", [HEROS, ALLIE], ["Puzzle.Attack('01059')"],
       {"degats": [["01094", 2], ["01059", 1]]}),
    _c("sj014 Kuji-Kaiju : un allie SANS icone consequentielle imprimee (Black Cat) subit alors 1 degat consequentiel apres son attaque",
       "Black Cat (ATQ 1, 2 PV) + Kuji-Kaiju : ATQ 3, 4 PV ; apres l'attaque : Rhino 3 degats, Black Cat 1 (0 + 1)",
       [HEROS, CHAT], [],
       {"degats": [["01094", 3], ["01002", 1]], "pv_max": [["01002", 4]]},
       main_exclusive=["sj014", "01088"], jouer=["sj014"], cibles=["01002"], declencher_apres=["Puzzle.Attack('01002')"]),
    _c("sj014 Kuji-Kaiju : « after it ATTACKS » seulement : apres un CONTRE de Jessica le degat consequentiel reste 1 (icone imprimee du THW), pas 2",
       "Jessica contre le complot principal (5 -> 4) et subit 1 degat consequentiel (pas 2)",
       [HEROS, ALLIE], ["Puzzle.SetThreat('01097b', 5)"],
       {"menace": [["01097b", 4]], "degats": [["01059", 1]]},
       main_exclusive=["sj014", "01088"], jouer=["sj014"], cibles=["01059"], declencher_apres=["Puzzle.Thwart('01059')"]),
    _c("sj014 Kuji-Kaiju : carte UNIQUE (✦) : une seconde copie n'est pas jouable tant qu'une est en jeu (pas de « Max » imprime : c'est l'unicite)",
       "une copie deja attachee a Jessica Jones, une seconde en main : injouable (unicite)",
       [HEROS, ALLIE, "Puzzle.AttachReel('sj014', '01059')"], ["Puzzle.CreateHandCards('sj014')"],
       {"carte": "sj014", "jouable": False, "en_jeu": 1}, verifier="max_par_joueur_jouable", main_exclusive=["01088"]),
    _c("sj014 Kuji-Kaiju : « an ally YOU CONTROL » : l'allie d'un AUTRE joueur n'est pas une cible legale",
       "deux joueurs : Jessica Jones est sous le controle du joueur 2 : Kuji-Kaiju injouable pour le joueur 1",
       [HEROS, "Puzzle.PutIntoPlay('01059', under_control=True, player=1)"], ["Puzzle.CreateHandCards('sj014')"],
       {"carte": "sj014", "jouable": False, "en_jeu": 0}, verifier="max_par_joueur_jouable", main_exclusive=["01088"], heros2="iron_man"),
    _c("sj014 Kuji-Kaiju : TEMOIN positif, avec un allie sous son controle la carte est jouable",
       "meme montage, allie sous le controle du joueur 1 : jouable",
       [HEROS, ALLIE], ["Puzzle.CreateHandCards('sj014')"],
       {"carte": "sj014", "jouable": True, "en_jeu": 0}, verifier="max_par_joueur_jouable", main_exclusive=["01088"], heros2="iron_man"),
]

# ========================================================================= sj015 Morphic Charm
# Cout 0 : la main = la carte seule. Le remplacement passe par `DeclareStatusCard` : les options se nomment « p_<statut en minuscules> ».
SBIRE_SONNE = "Puzzle.Stun('01101')"
CAS += [
    _c("sj015 Morphic Charm : un sbire Sonne voit sa carte Sonne remplacee par une AUTRE carte d'etat (premier choix : Desoriente), puis 1 carte piochee",
       "Hydra Mercenary Sonne -> Desoriente ; plus de Sonne ; main : la carte jouee part, 1 carte piochee",
       [HEROS, SANS_DECK, DECK6, SBIRE, SBIRE_SONNE], [],
       {"statuts": [["01101", "Confused"]], "statuts_absents": [["01101", "Stunned"]], "taille_main": 1, "defausse": ["sj015"]},
       main_exclusive=["sj015"], jouer=["sj015"], cibles=["01101"]),
    _c("sj015 Morphic Charm : le joueur CHOISIT le nouvel etat (Hebete) ; la carte Sonne est defaussee",
       "Hydra Mercenary Sonne -> Dazed (p_dazed)",
       [HEROS, SANS_DECK, DECK6, SBIRE, SBIRE_SONNE], [],
       {"statuts": [["01101", "Dazed"]], "statuts_absents": [["01101", "Stunned"], ["01101", "Confused"]], "taille_main": 1},
       main_exclusive=["sj015"], jouer=["sj015"], cibles=["01101"], choisir_option="p_dazed"),
    _c("sj015 Morphic Charm : « minion OR ALLY » : un ALLIE camoufle (Jessica Jones) voit son Cloaked remplace par Exposed",
       "Jessica Jones Cloaked -> Exposed (p_exposed) ; plus de Cloaked",
       [HEROS, SANS_DECK, DECK6, ALLIE, "Puzzle.Cloak('01059')"], [],
       {"statuts": [["01059", "Exposed"]], "statuts_absents": [["01059", "Cloaked"]], "taille_main": 1},
       main_exclusive=["sj015"], jouer=["sj015"], cibles=["01059"], choisir_option="p_exposed"),
    _c("sj015 Morphic Charm : « DIFFERENT » : l'etat remplace n'est PAS propose a nouveau (un Exposed ne se remplace pas par un Exposed)",
       "Hydra Mercenary Exposed (qui s'empile, donc sans plafond) : l'option p_exposed n'est jamais posee ; p_stunned l'est",
       [HEROS, SANS_DECK, DECK6, SBIRE, "Puzzle.Expose('01101')"], [],
       {"statuts_absents": [["01101", "Exposed"]], "taille_main": 1},
       main_exclusive=["sj015"], jouer=["sj015"], cibles=["01101"], questions_absentes=["p exposed"], questions_presentes=["p stunned"]),
    _c("sj015 Morphic Charm : « DIFFERENT » vaut aussi pour Coriace : un minion Coriace voit sa carte Coriace remplacee, p_tough n'est PAS offerte",
       "Hydra Mercenary Coriace : l'option p_tough n'est jamais posee ; p_stunned l'est ; plus de Coriace apres",
       [HEROS, SANS_DECK, DECK6, SBIRE, "Puzzle.Tough('01101')"], [],
       {"statuts_absents": [["01101", "Tough"]], "taille_main": 1},
       main_exclusive=["sj015"], jouer=["sj015"], cibles=["01101"], questions_absentes=["p tough"], questions_presentes=["p stunned"]),
    _c("sj015 Morphic Charm : seule la carte jouee compte : un HEROS qui porte un etat n'est pas une cible (aucun sbire ni allie avec un etat : injouable)",
       "le heros est Coriace, aucun sbire ni allie en jeu : Morphic Charm injouable",
       [HEROS, "Puzzle.Tough('01001a')"], [],
       {"carte": "sj015", "jouable": False, "en_jeu": 0}, verifier="max_par_joueur_jouable", main_exclusive=["sj015"]),
    _c("sj015 Morphic Charm : TEMOIN positif, avec un sbire qui porte un etat la carte est jouable",
       "Hydra Mercenary Sonne : jouable", [HEROS, SBIRE, SBIRE_SONNE], [],
       {"carte": "sj015", "jouable": True, "en_jeu": 0}, verifier="max_par_joueur_jouable", main_exclusive=["sj015"]),
    _c("sj015 Morphic Charm : Hero Action, injouable en alter-ego",
       "alter-ego : refusee", [SBIRE, SBIRE_SONNE], [],
       {"carte": "sj015", "jouable": False, "en_jeu": 0}, verifier="max_par_joueur_jouable", main_exclusive=["sj015"]),
]

# ========================================================================= sj016 QNA Restoration
# `Puzzle.Damage` / `CreatePlayerDiscardPile` dans `declencher` (APRES le vidage de la main par main_exclusive).
CAS += [
    _c("sj016 QNA Restoration : soigne 2 de l'identite du joueur choisi (4 -> 2), ce joueur melange 1 carte de SA defausse dans SON deck",
       "heros a 4 degats, defausse = {Strength} : apres la carte : 2 degats, Strength dans le deck, defausse = carte jouee + Genius depense (2)",
       [HEROS, SANS_DECK, DECK6], ["Puzzle.Damage('01001a', 4)", "Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('01073')"],
       {"degats_identite": 2, "dans_deck_joueur": ["01073"], "defausse_joueur": 2, "defausse": ["sj016", "01090"]},
       main_exclusive=["sj016", "01090"], jouer=["sj016"], cibles=["01001a", "01073"], accepter_choix=True),
    _c("sj016 QNA Restoration : « may » : en declinant (Cancel) la carte reste en defausse et rien n'est melange ; le soin a lieu quand meme",
       "meme montage, option declinee : 2 degats, defausse = 3 cartes, 01073 pas dans le deck",
       [HEROS, SANS_DECK, DECK6], ["Puzzle.Damage('01001a', 4)", "Puzzle.EmptyPlayerDiscardPile()", "Puzzle.CreatePlayerDiscardPile('01073')"],
       {"degats_identite": 2, "defausse_joueur": 3, "defausse": ["01073", "sj016"], "taille_deck_joueur": 6},
       main_exclusive=["sj016", "01090"], jouer=["sj016"], cibles=["01001a"], choisir_option="Cancel"),
    _c("sj016 QNA Restoration : le soin est plafonne a ce qu'il y a a soigner (1 degat -> 0, jamais de PV en trop)",
       "heros a 1 degat : apres le soin de 2, 0 degat",
       [HEROS, SANS_DECK, DECK6], ["Puzzle.Damage('01001a', 1)", "Puzzle.EmptyPlayerDiscardPile()"],
       {"degats_identite": 0},
       main_exclusive=["sj016", "01090"], jouer=["sj016"], cibles=["01001a"], accepter_choix=True),
    _c("sj016 QNA Restoration : le joueur CHOISI est l'AUTRE joueur : SON identite est soignee, il melange une carte de SA defausse dans SON deck, le joueur 1 n'a rien",
       "deux joueurs : joueur 2 (Iron Man heros) a 4 degats et 01073 en defausse ; le joueur 1 a 3 degats et 01074 en defausse : seul le joueur 2 est soigne et melange",
       [HEROS, FER2, SANS_DECK, DECK6], ["Puzzle.Damage('01001a', 3)", "Puzzle.Damage('01029a', 4)", "Puzzle.EmptyPlayerDiscardPile()",
                                         "Puzzle.CreatePlayerDiscardPile('01074')", "Puzzle.MoveTo('01073', 'DiscardPile', player=1)"],
       {"degats_j1": 3, "degats_j2": 2, "dans_deck_j2": "01073", "defausse_j1": ["01074"]},
       verifier="sj_qna_deux_joueurs", heros2="iron_man", main_exclusive=["sj016", "01090"], jouer=["sj016"], cibles=["01029a"], accepter_choix=True),
    _c("sj016 QNA Restoration : Hero Action, injouable en alter-ego",
       "alter-ego : refusee", [], [], {"carte": "sj016", "jouable": False, "en_jeu": 0}, verifier="max_par_joueur_jouable",
       main_exclusive=["sj016", "01090"]),
]

# ========================================================================= sj017 Yi
YI = _en_jeu("sj017")   # Yi : allie 3 PV, ATQ 1* et THW 1* (1 degat consequentiel apres chaque)
def _yi(nom, pourquoi, defausse, declencher, attendu, **cle):
    return _c(nom, pourquoi, [HEROS, SANS_DECK, DECK6, YI, "Puzzle.EmptyPlayerDiscardPile()",
                              "Puzzle.CreatePlayerDiscardPile(" + ", ".join(f"'{x}'" for x in defausse) + ")"],
              declencher, attendu, verifier="sj_dessus_du_deck", **cle)


CAS += [
    _yi("sj017 Yi : apres une ATTAQUE de base, une carte SPELL de la defausse est posee sur le DESSUS du deck (et sort de la defausse)",
        "Yi attaque Rhino (1 degat) et subit 1 degat consequentiel ; defausse = {Foresight (SPELL), Strength} : sj001 devient le dessus du deck",
        ["01090", "sj001"], ["Puzzle.Attack('sj017')"],
        {"dessus": "sj001", "pas_en_defausse": ["sj001"], "degats": [["01094", 1], ["sj017", 1]], "taille_deck_joueur": 7}),
    _yi("sj017 Yi : apres un CONTRE de base (pouvoir de base : THW), meme Reponse",
        "Yi contre le complot principal (5 -> 4) : sj001 sur le dessus du deck",
        ["01090", "sj001"], ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Thwart('sj017')"],
        {"dessus": "sj001", "menace": [["01097b", 4]], "taille_deck_joueur": 7}, main_exclusive=["01090"]),
    _yi("sj017 Yi : « SPELL OR TECH » : une carte TECH (Spider-Tracer) convient aussi",
        "defausse = {Spider-Tracer (TECH), Strength} : 01007 sur le dessus du deck",
        ["01090", "01007"], ["Puzzle.Attack('sj017')"],
        {"dessus": "01007", "pas_en_defausse": ["01007"], "taille_deck_joueur": 7}),
    _yi("sj017 Yi : aucune carte SPELL ni TECH en defausse : rien n'est pose sur le deck (le dessus reste Genius)",
        "defausse = {Strength, Energy} : la Reponse n'a aucune cible, le deck est inchange (6)",
        ["01090", "01088"], ["Puzzle.Attack('sj017')"],
        {"dessus": "01089", "taille_deck_joueur": 6}),
    _yi("sj017 Yi : seul YI declenche la Reponse : un AUTRE allie (Jessica Jones) qui attaque ne fait rien (le dessus reste Genius)",
        "Jessica Jones attaque, la defausse contient une SPELL : aucune Reponse de Yi",
        ["01090", "sj001"], ["Puzzle.PutIntoPlay('01059', under_control=True)", "Puzzle.Attack('01059')"],
        {"dessus": "01089", "taille_deck_joueur": 6}),
]

# ========================================================================= sj018 Wu Jen Tessen
# ⚠ Tessen est elle-meme une carte Kuji-Kiri jouee de la main : posee par `jouer`, sa propre Reponse part des son entree en jeu
# (cas dedie ci-dessous). Les autres cas la POSENT PAR `AttachReel` (aucune Reponse a l'entree) pour ne mesurer que la carte suivante.
EPUISE = "Puzzle.Exhaust('01001a')"
TESSEN = "Puzzle.AttachReel('sj018', '01001a')"
CAS += [
    _c("sj018 Wu Jen Tessen : apres avoir joue une carte Kuji-Kiri DEPUIS LA MAIN (Foresight), Tessen s'incline et le HEROS est redresse",
       "Tessen deja en jeu, heros epuise : Foresight jouee de la main -> heros redresse, Tessen inclinee",
       [HEROS, SANS_DECK, DECK6, TESSEN], [EPUISE],
       {"pret": ["01001a"], "exhausted": ["sj018"], "defausse": ["sj001"]},
       main_exclusive=["sj001", "01088"], jouer=["sj001"], choisir_option="Cancel"),
    _c("sj018 Wu Jen Tessen : TEMOIN, une carte NON Kuji-Kiri (Armored Vest) jouee de la main ne redresse rien : heros epuise, Tessen prete",
       "01081 n'est pas Kuji-Kiri : le heros reste epuise, Tessen reste prete",
       [HEROS, SANS_DECK, DECK6, TESSEN], [EPUISE],
       {"exhausted": ["01001a"], "pret": ["sj018"], "en_jeu": ["01081"]},
       main_exclusive=["01081", "01088"], jouer=["01081"]),
    _c("sj018 Wu Jen Tessen : TEMOIN D'EPUISEMENT, une SECONDE carte Kuji-Kiri : Tessen est inclinee, le heros (re-epuise entre-temps) reste EPUISE",
       "1re Foresight : heros redresse, Tessen inclinee ; heros epuise a nouveau ; 2e Foresight : plus de Reponse, heros epuise",
       [HEROS, SANS_DECK, DECK6, TESSEN], [EPUISE],
       {"exhausted": ["01001a", "sj018"]},
       main_exclusive=["sj001", "sj001", "01088", "01088"], jouer=["sj001"],
       declencher_apres=[EPUISE], jouer_apres=["sj001"], choisir_option="Cancel"),
    _c("sj018 Wu Jen Tessen : Tessen est elle-meme une carte Kuji-Kiri jouee de la main : sa propre entree en jeu declenche sa Reponse (heros redresse)",
       "heros epuise, Tessen jouee (cout 2) : heros redresse, Tessen inclinee",
       [HEROS, SANS_DECK, DECK6], [EPUISE],
       {"pret": ["01001a"], "exhausted": ["sj018"], "en_jeu": ["sj018"]},
       main_exclusive=["sj018", "01088"], jouer=["sj018"]),
    _c("sj018 Wu Jen Tessen : « Hero Response » : en forme alter-ego (A Thin Place, Kuji-Kiri cout 0, jouee de la main) Tessen ne repond pas, reste prete",
       "alter-ego : pas de Hero Response",
       [SANS_DECK, DECK6, "Puzzle.AttachReel('sj018', '01001b')"], [],
       {"pret": ["sj018"], "en_jeu": ["sj012"]},
       main_exclusive=["sj012"], jouer=["sj012"]),
]

# ========================================================================= sj019 Static Shock
SHOCKER_SANS_REVELATION = "Puzzle.PutIntoPlay('01103')"   # PutIntoPlay ne revele pas : son When Revealed ne part pas
CAS += [
    _c("sj019 Static Shock : Rampage 1 (1 degat au heros ET 1 carte du dessus du deck defaussee) puis 3 degats a l'ennemi vise et 1 degat a CHAQUE ennemi engage avec vous",
       "Rhino (cible) et Shocker (sbire engage, sans Guard) : Rhino 3, Shocker 1 ; heros 1 degat ; deck 6 -> 5. Le vilain n'est pas « engage » au sens du moteur "
       "(seuls les sbires le sont : meme lecture que `ra005` Lightning Strike, `dt036` Quasar)",
       [HEROS, SANS_DECK, DECK6, SHOCKER_SANS_REVELATION], [],
       {"degats": [["01094", 3], ["01103", 1]], "degats_identite": 1, "taille_deck_joueur": 5, "defausse": ["sj019"]},
       main_exclusive=["sj019", "01088"], jouer=["sj019"], cibles=["01094"]),
    _c("sj019 Static Shock : l'ennemi vise est le SBIRE (3 PV) : vaincu par les 3 degats, il ne reçoit pas un degat de plus ; le vilain n'est pas touche",
       "Shocker vise, vaincu (hors jeu) ; Rhino (non engage) intact",
       [HEROS, SANS_DECK, DECK6, SHOCKER_SANS_REVELATION], [],
       {"hors_jeu": ["01103"], "degats": [["01094", 0]], "degats_identite": 1, "taille_deck_joueur": 5},
       main_exclusive=["sj019", "01088"], jouer=["sj019"], cibles=["01103"]),
    _c("sj019 Static Shock : « engaged WITH YOU » : un sbire engage avec l'AUTRE joueur ne prend pas le degat",
       "deux joueurs : Shocker engage avec le joueur 2 : intact (0 degat) alors que Rhino, vise, prend ses 3 degats",
       [HEROS, SHOCKER_SANS_REVELATION, "Puzzle.Engage('01103', player=1)", SANS_DECK, DECK6], [],
       {"degats": [["01103", 0], ["01094", 3]], "degats_identite": 1},
       heros2="iron_man", main_exclusive=["sj019", "01088"], jouer=["sj019"], cibles=["01094"]),
    _c("sj019 Static Shock : Rampage impayable (le degat est empeche par un statut Coriace) : la carte n'est PAS jouee, aucun degat a l'ennemi, le deck n'est pas touche",
       "heros Coriace : le degat de Rampage est empeche, le cout n'est pas paye : Rhino intact, carte en main, deck 6",
       [HEROS, SANS_DECK, DECK6, "Puzzle.Tough('01001a')"], [],
       {"degats": [["01094", 0]], "en_main": ["sj019"], "taille_deck_joueur": 6},
       main_exclusive=["sj019", "01088"], jouer=["sj019"], cibles=["01094"]),
    _c("sj019 Static Shock : Hero Action, injouable en alter-ego",
       "alter-ego : refusee", [], [], {"carte": "sj019", "jouable": False, "en_jeu": 0}, verifier="max_par_joueur_jouable",
       main_exclusive=["sj019", "01088"]),
]

# ========================================================================= sj020 Aethreal Shift (lecture PROVISOIRE : Hero INTERRUPT, question Q-K1)
# Rhino attaque le heros (ATQ 2, pas de defenseur : le heros prend 2, `Puzzle.Attack('01094')`).
def _shift(nom, pourquoi, mise, declencher, attendu, **cle):
    cle.setdefault("passer_sur_option", "Defense")   # le heros ne defend pas : sinon sa DEF 3 absorbe l'ATQ 2 de Rhino
    return _c(nom, pourquoi, [HEROS] + list(mise), declencher, attendu, main_exclusive=cle.pop("main_exclusive", ["sj020", "01090", "01089"]), **cle)


CAS += [
    _shift("sj020 Aethreal Shift : l'attaque de Rhino (2 degats) est ENTIEREMENT empechee et 2 menaces sont retirees d'une manigance",
           "complot principal a 5 : apres l'attaque : heros intact, complot a 3 ; la carte est jouee",
           [], ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Attack('01094')"],
           {"degats_identite": 0, "menace": [["01097b", 3]], "defausse": ["sj020"]}, cibles=["01097b"]),
    _shift("sj020 Aethreal Shift : TEMOIN, sans la carte la meme attaque inflige 2 degats et la menace reste a 5",
           "contre-cas : main sans Shift", [], ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Attack('01094')"],
           {"degats_identite": 2, "menace": [["01097b", 5]]}, main_exclusive=["01090", "01089"]),
    _shift("sj020 Aethreal Shift : la menace retiree est PLAFONNEE par la menace presente (1 menace pour 2 degats empeches : 0)",
           "complot a 1 : seule 1 menace peut etre retiree",
           [], ["Puzzle.SetThreat('01097b', 1)", "Puzzle.Attack('01094')"],
           {"degats_identite": 0, "menace": [["01097b", 0]]}, cibles=["01097b"]),
    _shift("sj020 Aethreal Shift : « from an ATTACK » : des degats directs (3, pas une attaque) ne la declenchent pas : la carte reste en main",
           "Puzzle.Damage('01001a', 3) : aucune interruption, 3 degats, Shift en main",
           [], ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Damage('01001a', 3)"],
           {"degats_identite": 3, "menace": [["01097b", 5]], "en_main": ["sj020"]}, passer_sur_option=""),
    _shift("sj020 Aethreal Shift : la menace retiree peut viser une manigance ANNEXE (Breakin' & Takin') : 5 -> 3",
           "complot principal a 5 aussi, mais la manigance annexe est choisie : seule elle perd 2 menaces",
           ["Puzzle.PutIntoPlay('01107')"], ["Puzzle.SetThreat('01107', 5)", "Puzzle.SetThreat('01097b', 5)", "Puzzle.Attack('01094')"],
           {"degats_identite": 0, "menace": [["01107", 3], ["01097b", 5]]}, cibles=["01107"]),
]

# @@FIN_DES_CAS@@

VERIFICATIONS = r'''
def sj_actions_disponibles(monde, aides):
    """Nombre d'actions REELLEMENT disponibles sur `carte` (type `type`), comme Puzzle.Action les numerote."""
    from game.event.manager import EventManager
    from game.ability.ability import AbilityType
    from game.message import Message
    from game.effect.rule import GameRule
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} introuvable en jeu"
    joueur = monde.GetCurrentPlayer()
    type_capacite = getattr(AbilityType, attendu["type"]) if attendu.get("type") else None
    candidats = [x for x in face.effect.Find(when=Message.WhenPlayerInTurn, type=type_capacite)
                 if not x.ability.is_play]
    message = Message.WhenPlayerLikeInTurn(joueur, GameRule(joueur.GetIdentity()))
    message.Send()
    dispo = EventManager.FilterAvailableEffects(message, candidats, joueur, monde, None)
    n = len(dispo)
    if n != attendu["nombre"]:
        return False, f"{attendu['carte']} offre {n} action(s) {attendu.get('type')} (attendu {attendu['nombre']})"
    return True, f"{attendu['carte']} : {n} action(s) {attendu.get('type')} disponible(s), comme attendu"


def _sj_faces_nommees(monde, nom):
    out = []
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and face.IsInPlay() and face.IsName(nom):
            out.append(face)
    return out


def sj_allie_controle(monde, aides):
    """Enthrall : `nom` est (ou n'est plus) un allie CONTROLLED sous le controle du joueur.
    attendu : nom, sbire (bool : True = c'est redevenu un sbire), thw, atk, pv, conseq_atk, conseq_thw, trait,
    sans_capacite_propre."""
    from game.card.face.card_type import Ally, Minion
    attendu = aides["cas"]["attendu"]
    nom = attendu["nom"]
    faces = _sj_faces_nommees(monde, nom)
    if attendu.get("temoin_avec_capacite_revelee"):
        # TEMOIN de la mesure « sans capacite propre » : le sbire Shocker NON controle, lui, porte sa capacite.
        sbires = [f for f in faces if Minion.IsType(f)]
        if not sbires:
            return False, f"{nom} n'est pas un sbire en jeu"
        revelees = [str(e) for e in sbires[0].effect.Find() if "Revealed" in str(e)]
        if not revelees:
            return False, "le sbire Shocker non controle ne porte aucune capacite « When Revealed » : la mesure ne discrimine rien"
        return True, f"temoin : le sbire non controle porte {len(revelees)} capacite(s) « When Revealed »"
    controles = [f for f in monde.players[0].GetControlAllies() if f.IsName(nom)]
    if attendu.get("sbire") is True:
        sbires = [f for f in faces if Minion.IsType(f)]
        if controles or not sbires:
            return False, f"{nom} : allies controles={len(controles)}, sbires={len(sbires)} (attendu : plus d'allie, un sbire)"
        return True, f"{nom} est redevenu un sbire en jeu"
    if not controles:
        return False, f"{nom} n'est pas un allie sous le controle du joueur (faces en jeu : {[type(f).__name__ for f in faces]})"
    allie = controles[0]
    soucis = []
    if any(Minion.IsType(f) for f in faces):
        soucis.append("une face Sbire du meme nom est encore en jeu")
    if not Ally.IsType(allie):
        soucis.append(f"la face n'est pas un allie ({type(allie).__name__})")
    if "thw" in attendu and allie.thwart != attendu["thw"]:
        soucis.append(f"THW={allie.thwart} (attendu {attendu['thw']})")
    if "atk" in attendu and allie.attack != attendu["atk"]:
        soucis.append(f"ATQ={allie.attack} (attendu {attendu['atk']})")
    if "pv" in attendu and allie.max_health != attendu["pv"]:
        soucis.append(f"PV max={allie.max_health} (attendu {attendu['pv']})")
    if "conseq_atk" in attendu and allie.printed_attack_consequential_damage != attendu["conseq_atk"]:
        soucis.append(f"degats consequentiels apres attaque={allie.printed_attack_consequential_damage} (attendu {attendu['conseq_atk']})")
    if "conseq_thw" in attendu and allie.printed_thwart_consequential_damage != attendu["conseq_thw"]:
        soucis.append(f"degats consequentiels apres contre={allie.printed_thwart_consequential_damage} (attendu {attendu['conseq_thw']})")
    if "trait" in attendu and not allie.HasTrait(attendu["trait"]):
        soucis.append(f"trait {attendu['trait']} absent")
    if attendu.get("sans_capacite_propre"):
        propres = [str(e) for e in allie.effect.Find()]
        revelees = [x for x in propres if "Revealed" in x]
        if revelees:
            soucis.append(f"capacite « When Revealed » du Shocker encore la : {revelees}")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{nom} : allie CONTROLLED (THW {allie.thwart}, ATQ {allie.attack}, PV {allie.max_health})"


def sj_apres_attaque_de_l_allie(monde, aides):
    """Enthrall : apres l'attaque de l'allie controle, le vilain a pris `degats` et l'allie a subi 3 degats
    consequentiels (vaincu quand ses PV tombent a 0)."""
    attendu = aides["cas"]["attendu"]
    soucis = []
    for card_id, valeur in attendu.get("degats") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable")
        elif face.max_health - face.health != valeur:
            soucis.append(f"degats sur {card_id} = {face.max_health - face.health} (attendu {valeur})")
    for card_id, valeur in attendu.get("menace") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable")
        elif face.threat != valeur:
            soucis.append(f"menace sur {card_id} = {face.threat} (attendu {valeur})")
    nom = attendu["allie_vaincu"]
    restants = [f for f in monde.players[0].GetControlAllies() if f.IsName(nom)]
    if restants:
        soucis.append(f"{nom} est encore en jeu avec {restants[0].health}/{restants[0].max_health} PV (3 degats consequentiels attendus)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{nom} a attaque puis a subi 3 degats consequentiels : vaincu"
def sj_etat_rencontre(monde, aides):
    """Mesure la taille du deck / de la defausse RENCONTRE (cles `taille_deck_rencontre`, `taille_defausse_rencontre`),
    puis delegue le reste a etat_attendu."""
    from game.operate.worlds import Worlds
    attendu = aides["cas"]["attendu"]
    soucis = []
    if "taille_deck_rencontre" in attendu:
        n = len([f for f in Worlds.GetEncounterDeckCards(monde) if f is not None])
        if n != attendu["taille_deck_rencontre"]:
            soucis.append(f"deck rencontre = {n} carte(s) (attendu {attendu['taille_deck_rencontre']})")
    if "taille_defausse_rencontre" in attendu:
        n = len([f for f in Worlds.GetEncounterDiscardPileCards(monde) if f is not None])
        if n != attendu["taille_defausse_rencontre"]:
            soucis.append(f"defausse rencontre = {n} carte(s) (attendu {attendu['taille_defausse_rencontre']})")
    ok, message = etat_attendu(monde, aides)
    if soucis:
        return False, " ; ".join(soucis) + ("" if ok else " ; " + message)
    return ok, message
def sj_armageddon(monde, aides):
    """Armageddon : `dealt` (cartes rencontre distribuees face cachee par joueur), `delta_main` (taille de main de
    l'identite moins son imprime, par joueur), `victoire` (Armageddon dans la pile de victoire) ; le reste -> etat_attendu."""
    attendu = aides["cas"]["attendu"]
    soucis = []
    if "dealt" in attendu:
        obtenu = [len(list(j.dealt_encounter_cards.GetAll())) for j in monde.players]
        if obtenu != attendu["dealt"]:
            soucis.append(f"cartes distribuees face cachee par joueur = {obtenu} (attendu {attendu['dealt']})")
    if "delta_main" in attendu:
        obtenu = [j.hand_size - j.GetIdentity().printed_hand_size for j in monde.players[:len(attendu["delta_main"])]]
        if obtenu != attendu["delta_main"]:
            soucis.append(f"bonus de taille de main par identite = {obtenu} (attendu {attendu['delta_main']})")
    if "victoire" in attendu:
        ids = [getattr(f.paper, "card_id", None) for f in monde.victory_display.GetAll()]
        if ("sj009" in ids) != attendu["victoire"]:
            soucis.append(f"pile de victoire = {ids} (sj009 attendue : {attendu['victoire']})")
    ok, message = etat_attendu(monde, aides)
    if soucis:
        return False, " ; ".join(soucis) + ("" if ok else " ; " + message)
    return ok, message
def sj_sans_traits(monde, aides):
    """`carte` en jeu ne porte AUCUN des traits `sans_traits` ; le reste -> etat_attendu."""
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} introuvable en jeu"
    presents = [t for t in attendu["sans_traits"] if face.HasTrait(t)]
    ok, message = etat_attendu(monde, aides)
    if presents:
        return False, f"traits presents alors qu'ils ne devraient pas l'etre : {presents}" + ("" if ok else " ; " + message)
    return ok, message


def sj_crayon(monde, aides):
    """Kirby's Pencil : `retiree` = sj013 est dans la zone des cartes RETIREES du jeu (jamais dans la defausse du joueur) ;
    le reste (taille du deck rencontre...) -> sj_etat_rencontre."""
    attendu = aides["cas"]["attendu"]
    if attendu.get("retiree"):
        retirees = [getattr(f.paper, "card_id", None) for f in monde.area_removed.GetAll()]
        defausse = [getattr(f.paper, "card_id", None) for f in monde.players[0].discard_pile.Get()]
        if "sj013" not in retirees:
            return False, f"sj013 n'est pas dans la zone des cartes retirees du jeu (retirees = {retirees}, defausse = {defausse})"
        if "sj013" in defausse:
            return False, "sj013 est dans la defausse alors qu'elle devait etre RETIREE DU JEU"
    return sj_etat_rencontre(monde, aides)
def sj_qna_deux_joueurs(monde, aides):
    """QNA Restoration a deux joueurs : degats de l'identite de chaque joueur, carte melangee dans le deck du joueur 2,
    cartes restees dans la defausse du joueur 1."""
    attendu = aides["cas"]["attendu"]
    j1, j2 = monde.players[0], monde.players[1]
    soucis = []
    for cle, joueur in (("degats_j1", j1), ("degats_j2", j2)):
        if cle in attendu:
            ident = joueur.GetIdentity()
            subis = ident.max_health - ident.health
            if subis != attendu[cle]:
                soucis.append(f"{cle} : {subis} degat(s) (attendu {attendu[cle]})")
    if "dans_deck_j2" in attendu:
        ids = [getattr(f.paper, "card_id", None) for f in j2.player_deck.GetAll()]
        if attendu["dans_deck_j2"] not in ids:
            soucis.append(f"{attendu['dans_deck_j2']} n'est pas dans le deck du joueur 2 ({len(ids)} cartes)")
        defausse2 = [getattr(f.paper, "card_id", None) for f in j2.discard_pile.Get()]
        if attendu["dans_deck_j2"] in defausse2:
            soucis.append(f"{attendu['dans_deck_j2']} est encore dans la defausse du joueur 2")
    for card_id in attendu.get("defausse_j1") or []:
        ids = [getattr(f.paper, "card_id", None) for f in j1.discard_pile.Get()]
        if card_id not in ids:
            soucis.append(f"{card_id} n'est plus dans la defausse du joueur 1 (defausse = {ids})")
        ids_deck = [getattr(f.paper, "card_id", None) for f in j1.player_deck.GetAll()]
        if card_id in ids_deck:
            soucis.append(f"{card_id} (defausse du joueur 1) a ete melangee dans le deck du joueur 1")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "identite du joueur 2 soignee, carte de SA defausse melangee dans SON deck, joueur 1 intact"
def sj_dessus_du_deck(monde, aides):
    """Yi : `dessus` = card_id de la carte du DESSUS du deck du joueur (le dernier element de `player_deck.GetAll()`) ;
    `pas_en_defausse` = cartes qui ne doivent plus etre dans la defausse ; le reste -> etat_attendu."""
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    cartes = list(joueur.player_deck.GetAll())
    soucis = []
    if "dessus" in attendu:
        vu = getattr(cartes[-1].paper, "card_id", None) if cartes else None
        if vu != attendu["dessus"]:
            soucis.append(f"dessus du deck = {vu} (attendu {attendu['dessus']})")
    defausse = [getattr(f.paper, "card_id", None) for f in joueur.discard_pile.Get()]
    for card_id in attendu.get("pas_en_defausse") or []:
        if card_id in defausse:
            soucis.append(f"{card_id} est encore dans la defausse")
    ok, message = etat_attendu(monde, aides)
    if soucis:
        return False, " ; ".join(soucis) + ("" if ok else " ; " + message)
    return ok, message
# @@FIN_VERIFICATIONS@@
'''
