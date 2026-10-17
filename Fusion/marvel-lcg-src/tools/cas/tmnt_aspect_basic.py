# Cas test_capacites de l'aspect TMNT BASIC (Inkwire, pack `tmnt_aspect_basic`, prefixe `ub`).
# Filtre : `[ub]`. Gabarits : .planning/tmnt/aspects-basic-gabarits.md ; questions :
# .planning/tmnt/aspects-basic-questions.md.
#
# Conventions :
#  - Spider-Man (01001) demarre en ALTER EGO (Peter Parker, GENIUS) ; HEROS le met en forme heros ;
#  - `main_exclusive` vide la main : chaque cas sait avec QUOI il paie
#    (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR) ;
#  - Rhino 01094 (14 PV) est le vilain, 01097b son plan principal, 01101 Hydra Mercenary (3 PV) le sbire ;
#  - RESKIN (IDENTIQUE, `ability_link`) : chaque cas existe DEUX fois, sur la carte TMNT et sur
#    l'officielle (TEMOIN), meme montage, meme chiffre attendu. Le montage est ecrit une fois avec
#    `{X}` a la place du card_id (`_paire`).
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
STRANGE_HEROS = "Puzzle.ChangeForm('09001b')"
LEO_HEROS = "Puzzle.ChangeToFace('tl001b', 'tl001a')"
HULK_HEROS = "Puzzle.ChangeForm('10001b')"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[ub] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


def _sub(valeur, x):
    """Remplace `{X}` par le card_id dans toute la structure du cas."""
    if isinstance(valeur, str):
        return valeur.replace("{X}", x)
    if isinstance(valeur, list):
        return [_sub(v, x) for v in valeur]
    if isinstance(valeur, tuple):
        return tuple(_sub(v, x) for v in valeur)
    if isinstance(valeur, dict):
        return {k: _sub(v, x) for k, v in valeur.items()}
    return valeur


def _paire(reskin, officielle, nom, pourquoi, mise, declencher, attendu, **cle):
    """Le cas sur le reskin TMNT, puis le TEMOIN identique sur l'officielle."""
    return [
        _c(_sub(f"{reskin} {nom}", reskin), pourquoi, _sub(mise, reskin), _sub(declencher, reskin),
           _sub(attendu, reskin), **_sub(dict(cle), reskin)),
        _c(_sub(f"{reskin} TEMOIN {officielle} : {nom}", officielle), "TEMOIN : meme montage sur l'officielle",
           _sub(mise, officielle), _sub(declencher, officielle), _sub(attendu, officielle),
           **_sub(dict(cle), officielle)),
    ]


def _jeu(card_id):
    return "Puzzle.PutIntoPlay('%s', under_control=True)" % card_id


CAS = []

# ============================================================================ RESKINS (IDENTIQUE)
# ub001 April O'Neil <- 01084 Nick Fury
CAS += _paire("ub001", "01084", "({X}) : Reponse forcee a l'entree en jeu, option « 4 degats » -> Rhino 4",
              "« choose one: remove 2 threat, draw 3 cards, or deal 4 damage to an enemy »",
              [HEROS], [], {"degats": [["01094", 4]], "en_jeu": ["{X}"]},
              main_exclusive=["{X}", "01089", "01088"], jouer=["{X}"], preferer_option="Deal_4", cibles=["01094"])
CAS += _paire("ub001", "01084", "({X}) : defausse a la fin du round",
              "« At the end of the round, if April O'Neil is still in play, discard her »",
              [HEROS, _jeu("{X}")], [], {"hors_jeu": ["{X}"]},
              main_exclusive=["01089"], verifier="ub_apres_fin_de_round")
# ub002 Assess the Situation <- 12033
CAS += _paire("ub002", "12033", "({X}) : +1 taille de main jusqu'a la fin de la phase",
              "« You get +1 hand size until the end of the phase »",
              [HEROS], [], {"attributs": {"hand_size": 1}, "defausse": ["{X}"]},
              main_exclusive=["{X}"], jouer=["{X}"])
# ub004 Basic Spell <- 45051
CAS += _paire("ub004", "45051", "({X}) : Doctor Strange (MYSTIC), option « 3 degats a un ennemi »",
              "« Play only if your identity has the MYSTIC trait » + « Deal 3 damage to an enemy »",
              [STRANGE_HEROS], [], {"degats": [["01094", 3]], "defausse": ["{X}"]},
              heros="doctor_strange", main_exclusive=["{X}", "01088"], jouer=["{X}"],
              preferer_option="Deal_3", cibles=["01094"])
CAS += _paire("ub004", "45051", "({X}) : Spider-Man (sans MYSTIC) ne peut pas la jouer",
              "contre-cas de « Play only if your identity has the MYSTIC trait »",
              [HEROS], [], {"en_main": ["{X}"], "degats": [["01094", 0]]},
              main_exclusive=["{X}", "01088"], jouer=["{X}"], cibles=["01094"])
# ub006 Clyde <- 13018 Ironheart
CAS += _paire("ub006", "13018", "({X}) : joue de la main -> pioche 1 carte",
              "« After you play Clyde from your hand, draw 1 card » : main = la carte + 1 Genius, puis 1 pioche",
              [HEROS], [], {"en_jeu": ["{X}"], "taille_main": 1},
              main_exclusive=["{X}", "01089"], jouer=["{X}"])
# ub007 Digging Deep <- 40060, defaussee du dessus du deck par le Rampage 3 de ua015 Demolish
CAS += _paire("ub007", "40060", "({X}) : defaussee du dessus du deck (Rampage de Demolish) -> revient en main",
              "« After this card is discarded from the top of your deck, add it to your hand »",
              [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '{X}', '01089', '01089')"], [],
              {"en_main": ["{X}"], "degats": [["01094", 8]]},
              main_exclusive=["ua015", "01090", "01088"], jouer=["ua015"], cibles=["01094"], accepter_choix=True)
# ub009 Down Time <- 05033
CAS += _paire("ub009", "05033", "({X}) : l'alter ego gagne +2 REC",
              "« Your alter-ego gets +2 REC »",
              [], [], {"attributs": {"recover": 2}, "en_jeu": ["{X}"]},
              main_exclusive=["{X}", "01090"], jouer=["{X}"])
# ub010 Endurance <- 05023
CAS += _paire("ub010", "05023", "({X}) : +3 points de vie (10 -> 13)",
              "« You get +3 hit points »",
              [], [], {"attributs": {"health": 3}, "en_jeu": ["{X}"]},
              main_exclusive=["{X}", "01088"], jouer=["{X}"])
# ub011 Energy / ub016 Genius / ub054 Strength <- 01088 / 01089 / 01090 (aucun module : pures donnees)
for _res, _off, _lettre in (("ub011", "01088", "YY"), ("ub016", "01089", "BB"), ("ub054", "01090", "RR")):
    CAS += _paire(_res, _off, f"({{X}}) : ressource double {_lettre} : paie SEULE Clyde (cout 2)",
                  "ressource de base double : une carte = 2 ressources",
                  [HEROS], [], {"en_jeu": ["ub006"], "defausse": ["{X}"]},
                  main_exclusive=["ub006", "{X}"], jouer=["ub006"])
# ub012 E.P.F. R.N.D. <- 35022 Weapon X
CAS += _paire("ub012", "35022", "({X}) : Action d'alter ego : 1 degat, defausse jusqu'a une carte d'identite (01005) -> en main",
              "« Exhaust and take 1 damage -> discard cards from your deck until you discard an identity-specific card, "
              "then add that card to your hand »",
              [_jeu("{X}"), SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01005', '01089')"],
              ["Puzzle.Action('{X}', 'AlterEgoAction')"],
              {"degats_identite": 1, "en_main": ["01005"], "exhausted": ["{X}"]},
              main_exclusive=["01090"])
# ub013 Face the Past <- 49022 (montage du cas Hercules existant)
CAS += _paire("ub013", "49022", "({X}) : Hercules : revele Ares (sbire nemesis), pas la Lernean Hydra",
              "« Search ... for your nemesis minion and reveal it -> ready your hero and draw 3 cards »",
              ["Puzzle.ChangeToFace('59001b', '59001a')"], [],
              {"en_jeu": ["59036"], "hors_jeu": ["59037"]},
              heros="hercules", main=["{X}"], jouer=["{X}"])
# ub015 Genghis <- 40057 White Fox, defausse du dessus du deck par Demolish
CAS += _paire("ub015", "40057", "({X}) : defausse du dessus du deck (Rampage de Demolish) -> mis en jeu",
              "« After Genghis is discarded from the top of your deck, put him into play under your control »",
              [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089', '{X}', '01089', '01089')"], [],
              {"en_jeu": ["{X}"], "degats": [["01094", 8]]},
              main_exclusive=["ua015", "01090", "01088"], jouer=["ua015"], cibles=["01094"], accepter_choix=True)
# ub017 Gofu Talisman <- 45050 Bloodgem
CAS += _paire("ub017", "45050", "({X}) : Ressource : s'incliner et subir 2 degats -> paie seule Down Time (cout 1)",
              "« Exhaust and take 2 damage -> generate a [wild] resource »",
              [_jeu("{X}")], [], {"en_jeu": ["ub009"], "degats_identite": 2, "exhausted": ["{X}"]},
              heros="doctor_strange", main_exclusive=["ub009"], jouer=["ub009"])
CAS += _paire("ub017", "45050", "({X}) : jouable par Doctor Strange (MYSTIC)",
              "« Play only if you have the MYSTIC trait » (cout 0)",
              [], [], {"en_jeu": ["{X}"]}, heros="doctor_strange", main_exclusive=["{X}"], jouer=["{X}"])
CAS += _paire("ub017", "45050", "({X}) : NON jouable par Spider-Man (sans MYSTIC)",
              "contre-cas de « Play only if you have the MYSTIC trait »",
              [], [], {"en_main": ["{X}"]}, main_exclusive=["{X}"], jouer=["{X}"])
# ub021 Ingenuity <- 29027
CAS += _paire("ub021", "29027", "({X}) : Ressource : s'incliner -> paie seule Down Time (cout 1)",
              "« Exhaust Ingenuity -> generate a [mental] resource »",
              [HEROS, _jeu("{X}")], [], {"en_jeu": ["ub009"], "exhausted": ["{X}"]},
              main_exclusive=["ub009"], jouer=["ub009"])
CAS += _paire("ub021", "29027", "({X}) : jouable par Peter Parker (GENIUS), pas par Spider-Man (heros, sans GENIUS)",
              "« Play only if your identity has the GENIUS trait » : la forme alter ego de Spider-Man a GENIUS",
              [], [], {"en_jeu": ["{X}"]}, main_exclusive=["{X}", "01089"], jouer=["{X}"])
CAS += _paire("ub021", "29027", "({X}) : NON jouable par Spider-Man en forme heros (AVENGER seulement)",
              "contre-cas de « your identity has the GENIUS trait »",
              [HEROS], [], {"en_main": ["{X}"]}, main_exclusive=["{X}", "01089"], jouer=["{X}"])
# ub026 Limitless Stamina <- 31023
CAS += _paire("ub026", "31023", "({X}) : Hulk (18 PV imprimes) : redresse le heros",
              "« Play only if your identity has at least 14 printed hit points. Hero Action: Ready your hero »",
              [HULK_HEROS, "Puzzle.Exhaust('10001a')"], [], {"pret": ["10001a"], "defausse": ["{X}"]},
              heros="hulk", main_exclusive=["{X}", "01090"], jouer=["{X}"])
CAS += _paire("ub026", "31023", "({X}) : Spider-Man (10 PV) ne peut pas la jouer",
              "contre-cas du seuil de 14 PV imprimes",
              [HEROS, "Puzzle.Exhaust('01001a')"], [], {"en_main": ["{X}"], "exhausted": ["01001a"]},
              main_exclusive=["{X}", "01090"], jouer=["{X}"])
# ub028 Mary <- 01083 Mockingbird
CAS += _paire("ub028", "01083", "({X}) : entree en jeu -> sonne Rhino",
              "« After Mary enters play, stun an enemy »",
              [HEROS], [], {"statuts": [["01094", "Stunned"]], "en_jeu": ["{X}"]},
              main_exclusive=["{X}", "01090", "01088"], jouer=["{X}"], cibles=["01094"])
# ub030 Multitalented <- 47021
CAS += _paire("ub030", "47021", "({X}) : paye en [physical] seulement -> 2 degats, menace intacte",
              "« If you paid for this event using at least 1: [physical] - Deal 2 damage »",
              [HEROS], ["Puzzle.SetThreat('01097b', 5)"], {"degats": [["01094", 2]], "menace": [["01097b", 5]]},
              main_exclusive=["{X}", "01090", "01090"], jouer=["{X}"], cibles=["01094"])
# ub031 Mutagen <- 38019 X-Gene
CAS += _paire("ub031", "38019", "({X}) : Ressource [wild] pour un evenement d'identite (Swinging Web Kick, cout 3)",
              "« generate a [wild] resource for an identity-specific event » : Strength (2) + Mutagen (1) = 3",
              [HEROS, _jeu("{X}")], [], {"degats": [["01094", 8]], "exhausted": ["{X}"]},
              main_exclusive=["01005", "01090"], jouer=["01005"], cibles=["01094"])
CAS += _paire("ub031", "38019", "({X}) : la ressource ne paie PAS un evenement de base (Multitalented reste en main)",
              "contre-cas « for an identity-specific event » : Multitalented (cout 3, basique) reste en main",
              [HEROS, _jeu("{X}")], [], {"en_main": ["ub030"], "degats": [["01094", 0]]},
              main_exclusive=["ub030", "01090"], jouer=["ub030"], cibles=["01094"])
# ub034 Onmyodo Saiko <- 09026 The Sorcerer Supreme
CAS += _paire("ub034", "09026", "({X}) : Doctor Strange en forme heros : +1 taille de main",
              "« You get +1 hand size while in hero form »",
              [STRANGE_HEROS], [], {"attributs": {"hand_size": 1}, "en_jeu": ["{X}"]},
              heros="doctor_strange", main_exclusive=["{X}", "01088"], jouer=["{X}"])
# ub035 Party Time <- 33022 Game Time
CAS += _paire("ub035", "33022", "({X}) : allie avec une amelioration TRAINING : redresse et soigne 1",
              "« Choose an ally with a TRAINING upgrade attached -> ready that ally and heal 1 damage from it »",
              [HEROS, _jeu("01083"), "Puzzle.Attach('32013', '01083')", "Puzzle.Exhaust('01083')",
               "Puzzle.Damage('01083', 1)"], [], {"pret": ["01083"], "degats": [["01083", 0]]},
              main_exclusive=["{X}"], jouer=["{X}"], cibles=["01083"])
# ub039 Practiced Plan <- 50058
CAS += _paire("ub039", "50058", "({X}) : Widow's Bite (PREPARATION) defaussee -> revient en main",
              "« After you discard a PREPARATION card you control, discard Practiced Plan -> return that card to your hand »",
              [HEROS, _jeu("{X}"), _jeu("08010")], ["Puzzle.Reveal('01101')"],
              {"en_main": ["08010"], "hors_jeu": ["{X}", "08010"], "degats": [["01101", 2]]},
              main_exclusive=["01089"], accepter_choix=True, cibles=["01101"])
# ub042 Ready to Rumble <- 21022
CAS += _paire("ub042", "21022", "({X}) : apres le changement de forme, se defausse -> heros redresse",
              "« After you change form, discard this card -> ready your hero »",
              [_jeu("{X}"), "Puzzle.Exhaust('01001b')"], [HEROS], {"pret": ["01001a"], "hors_jeu": ["{X}"]},
              main_exclusive=["01089"], accepter_choix=True)
# ub044 Shell Phone <- 47019 Cell Phone
CAS += _paire("ub044", "47019", "({X}) : attaque de base de Spider-Man a +1 ATQ (3 degats), 1 charge retiree",
              "« that player makes a basic attack or thwart ... gets +1 THW and +1 ATK for this use »",
              [HEROS, _jeu("{X}")], ["Puzzle.Action('{X}')"],
              {"degats": [["01094", 3]], "compteurs": [["{X}", "charge", 2]]},
              main_exclusive=["01089"], preferer_option="ATK", cibles=["01094"])
# ub047 Sky Wagon <- 01092 Helicarrier
CAS += _paire("ub047", "01092", "({X}) : la prochaine carte coute 1 de moins (Clyde paye avec 1 seule ressource)",
              "« Reduce the resource cost of the next card that player plays this phase by 1 »",
              [HEROS, _jeu("{X}")], ["Puzzle.Action('{X}')"], {"en_jeu": ["ub006"], "exhausted": ["{X}"]},
              main_exclusive=["ub006", "ub002"], jouer=["ub006"])
# ub048 Slash <- 62020 Hulk
CAS += _paire("ub048", "62020", "({X}) : le mechant attaque -> 1 compteur rage, +1 ATQ (2 -> 3)",
              "« After the villain attacks you, place 1 rage counter here » + « +1 ATK for each rage counter »",
              [HEROS, _jeu("{X}")], ["Puzzle.Attack('01094', '01001a')"],
              {"compteurs": [["{X}", "rage", 1]], "attributs_carte": [["{X}", "attack", 1]]},
              main_exclusive=["01089"], accepter_choix=True)
# ub051 Spiritual Meditation <- 15019
CAS += _paire("ub051", "15019", "({X}) : pioche 2, defausse 1 (main : 0 -> 1)",
              "« Draw 2 cards. Choose and discard 1 card from your hand »",
              [], [], {"taille_main": 1, "defausse": ["{X}"]},
              heros="doctor_strange", main_exclusive=["{X}"], jouer=["{X}"])
# ub053 Splinter <- 60029 Stick
CAS += _paire("ub053", "60029", "({X}) : Elektra (MARTIAL ARTIST) contre : option +1 en s'inclinant (menace 5 -> 3)",
              "« Exhaust Splinter -> that character gets +1 to that basic power for this use »",
              [HEROS, _jeu("{X}"), _jeu("60007")], ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Thwart('60007')"],
              {"menace": [["01097b", 3]], "exhausted": ["{X}"]},
              main_exclusive=["01089"], cibles=["01097b"], accepter_choix=True)
CAS += _paire("ub053", "60029", "({X}) incline : option -1 et redresser (menace 5 -> 5, carte redressee)",
              "« That character gets -1 to that basic power for this use. Ready Splinter » : Elektra THW 1 - 1 = 0",
              [HEROS, _jeu("{X}"), _jeu("60007"), "Puzzle.Exhaust('{X}')"],
              ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Thwart('60007')"],
              {"menace": [["01097b", 5]], "pret": ["{X}"]},
              main_exclusive=["01089"], cibles=["01097b"], accepter_choix=True, preferer_option="-1")
# ub055 Team-Building Exercise <- 12024
CAS += _paire("ub055", "12024", "({X}) : Leonardo joue son Katana (NINJA, cout 1) pour 0",
              "« play a card from your hand that shares a trait with your hero, reducing its resource cost by 1 »",
              [LEO_HEROS, _jeu("{X}")], ["Puzzle.Action('{X}')"], {"en_jeu": ["tl011"], "exhausted": ["{X}"]},
              heros="leonardo", main_exclusive=["tl011"], cibles=["tl011"])
# ub056 The Market <- 41023 X-Bunker
CAS += _paire("ub056", "41023", "({X}) : Leo (MUTANT), 1 manigance annexe en pile de victoire -> 1 carte du dessus en main",
              "« searches the top X cards of their deck for any card, where X is the number of side schemes in the victory display »",
              [_jeu("{X}"), "Puzzle.MoveTo('01107', 'VictoryDisplay')", SANS_DECK,
               "Puzzle.CreatePlayerDeck('01089', '01089')"], ["Puzzle.Action('{X}')"],
              {"taille_main": 2, "exhausted": ["{X}"]},
              heros="leonardo", main_exclusive=["01090"], accepter_choix=True)
# ub057 Turtle Lair <- 01091 Avengers Mansion
CAS += _paire("ub057", "01091", "({X}) : un joueur pioche 1 carte (main 1 -> 2)",
              "« choose a player. That player draws 1 card »",
              [_jeu("{X}")], ["Puzzle.Action('{X}')"], {"taille_main": 2, "exhausted": ["{X}"]},
              main_exclusive=["01089"])
# ub058 Upstate Farmhouse <- 20029 Crew Quarters
CAS += _paire("ub058", "20029", "({X}) : Action d'alter ego : soigne 1 degat d'un alter ego (2 -> 1)",
              "« Exhaust -> heal 1 damage from an alter-ego »",
              [_jeu("{X}"), "Puzzle.Damage('01001b', 2)"], ["Puzzle.Action('{X}', 'AlterEgoAction')"],
              {"degats_identite": 1, "exhausted": ["{X}"]}, main_exclusive=["01089"])

# ============================================================================ MODIFIEES (script propre)
LEO_CIVIL = "Puzzle.ChangeToFace('tl001a', 'tl001b')"   # Leo (alter ego) : MUTANT
DECK_STARTING = __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)),
                                           "ub_deck_starting.json")
CAS += [
    # ub003 Atilla (Forced Response, 13019 modifie). Heros Leonardo : Atilla porte le bandeau « Spider-Man ».
    _c("ub003 Atilla : Reponse FORCEE apres l'avoir joue de la main : THW choisi -> +2 CTR (1 -> 3)",
       "« Forced Response: After you play Atilla from your hand, choose THW or ATK. Atilla gets +2 »",
       [LEO_HEROS], [], {"attributs_carte": [["ub003", "thwart", 2]], "en_jeu": ["ub003"]},
       heros="leonardo", main_exclusive=["ub003", "01090", "01088"], jouer=["ub003"], preferer_option="THW"),
    _c("ub003 Atilla : option ATK -> +2 ATQ (2 -> 4)",
       "seconde branche du choix", [LEO_HEROS], [], {"attributs_carte": [["ub003", "attack", 2]]},
       heros="leonardo", main_exclusive=["ub003", "01090", "01088"], jouer=["ub003"], preferer_option="ATK"),
    _c("ub003 Atilla : mis en jeu SANS etre joue de la main -> aucun bonus",
       "contre-cas de « After you play Atilla FROM YOUR HAND »", [LEO_HEROS, _jeu("ub003")], [],
       {"attributs_carte": [["ub003", "thwart", 0], ["ub003", "attack", 0]]}, heros="leonardo",
       main_exclusive=["01089"]),
    _c("ub003 Atilla : bandeau « ✦ Spider-Man » (Q-R1) : NON jouable a cote du heros Spider-Man",
       "decision Q-R1 : l'unicite se juge aussi sur le titre du bandeau (`unique_also`)",
       ["Puzzle.ChangeForm('01001b')"], [], {"en_main": ["ub003"]},
       main_exclusive=["ub003", "01090", "01088"], jouer=["ub003"]),
    # ub018 Herold Lilja's Lab (34022 modifie)
    _c("ub018 Herold Lilja's Lab : allie NINJA (ub025) dans les 5 du dessus -> en main",
       "« search the top 5 cards of your deck for a DIMENSION X, NINJA, or MUTANIMAL ally »",
       [LEO_CIVIL, _jeu("ub018"), SANS_DECK,
        "Puzzle.CreatePlayerDeck('01089', '01089', '01089', 'ub025', '01089', '01089')"],
       ["Puzzle.Action('ub018', 'AlterEgoAction')"], {"en_main": ["ub025"], "exhausted": ["ub018"]},
       heros="leonardo", main_exclusive=["01090"], accepter_choix=True),
    _c("ub018 Herold Lilja's Lab : allie sous les 5 du dessus, sans TEMPORAL -> introuvable",
       "« the top 5 cards » : un allie en 7e position n'est pas vu",
       [LEO_CIVIL, _jeu("ub018"), SANS_DECK,
        "Puzzle.CreatePlayerDeck('ub025', '01089', '01089', '01089', '01089', '01089', '01089')"],
       ["Puzzle.Action('ub018', 'AlterEgoAction')"], {"absent_main": ["ub025"], "exhausted": ["ub018"]},
       heros="leonardo", main_exclusive=["01090"], accepter_choix=True),
    _c("ub018 Herold Lilja's Lab : avec un personnage TEMPORAL (Malcolm 45002), tout le deck -> trouve en 7e",
       "« search the whole deck instead if you control a TEMPORAL character »",
       [LEO_CIVIL, _jeu("ub018"), _jeu("45002"), SANS_DECK,
        "Puzzle.CreatePlayerDeck('ub025', '01089', '01089', '01089', '01089', '01089', '01089')"],
       ["Puzzle.Action('ub018', 'AlterEgoAction')"], {"en_main": ["ub025"]},
       heros="leonardo", main_exclusive=["01090"], accepter_choix=True),
    _c("ub018 Herold Lilja's Lab : un allie SANS les traits (01083) n'est pas pris",
       "contre-cas des traits DIMENSION X / NINJA / MUTANIMAL",
       [LEO_CIVIL, _jeu("ub018"), SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01083', '01089')"],
       ["Puzzle.Action('ub018', 'AlterEgoAction')"], {"absent_main": ["01083"]},
       heros="leonardo", main_exclusive=["01090"], accepter_choix=True),
    _c("ub018 Herold Lilja's Lab : NON jouable par Spider-Man (sans MUTANT)",
       "« Play only if your identity has the MUTANT trait »", [], [], {"en_main": ["ub018"]},
       main_exclusive=["ub018", "01089"], jouer=["ub018"]),
    _c("ub018 Herold Lilja's Lab : jouable par Leo (MUTANT)",
       "temoin du precedent", [LEO_CIVIL], [], {"en_jeu": ["ub018"]},
       heros="leonardo", main_exclusive=["ub018", "01089"], jouer=["ub018"]),
    # ub024 The Kennel Klub (33020 modifie)
    _c("ub024 The Kennel Klub : 3 allies NINJA, la limite passe a 4 -> un 4e allie (Leonardo) est jouable",
       "« If each of your allies has the MUTANIMAL or NINJA trait, increase your ally limit by 1 »",
       [HEROS, _jeu("ub024"), _jeu("ub008"), _jeu("ub029"), _jeu("tm002")], [],
       {"allies": 4},
       main_exclusive=["ub025", "01090", "01088"], jouer=["ub025"], verifier="ub_allies"),
    _c("ub024 The Kennel Klub : un allie sans les traits (Mockingbird) -> limite 3, 3 allies au plus",
       "contre-cas « each of your allies »",
       [HEROS, _jeu("ub024"), _jeu("ub008"), _jeu("ub029"), _jeu("01083")], [],
       {"allies": 3},
       main_exclusive=["ub025", "01090", "01088"], jouer=["ub025"], verifier="ub_allies"),
    _c("ub024 The Kennel Klub : un allie NINJA entre en jeu -> s'incliner pour redresser un personnage NINJA (Donatello)",
       "« After a MUTANIMAL or NINJA ally enters play, exhaust The Kennel Klub -> ready a MUTANIMAL or NINJA character »",
       [HEROS, _jeu("ub024"), _jeu("ub008"), "Puzzle.Exhaust('ub008')"], [],
       {"pret": ["ub008"], "exhausted": ["ub024"]},
       main_exclusive=["ub025", "01090", "01088"], jouer=["ub025"], cibles=["ub008"], accepter_choix=True),
    _c("ub024 The Kennel Klub : un allie SANS les traits entre en jeu -> pas de Reponse",
       "contre-cas : Mockingbird (S.H.I.E.L.D) ; le Klub reste pret, Donatello reste incline",
       [HEROS, _jeu("ub024"), _jeu("ub008"), "Puzzle.Exhaust('ub008')"], [],
       {"exhausted": ["ub008"], "pret": ["ub024"]},
       main_exclusive=["01083", "01090", "01088"], jouer=["01083"], cibles=["ub008", "01094"], accepter_choix=True),
    # ub032 Mutanimal Van (41022 modifie)
    _c("ub032 Mutanimal Van : Action de heros : 1 carte rencontre face cachee, le joueur pioche 2",
       "« Exhaust and deal 1 facedown encounter card to a player -> that player draws 2 cards »",
       [HEROS, _jeu("ub032")], ["Puzzle.Action('ub032')"], {"taille_main": 3, "exhausted": ["ub032"]},
       main_exclusive=["01089"]),
    _c("ub032 Mutanimal Van : NON jouable sans le trait MUTANIMAL (Leonardo heros)",
       "« Play only if your identity has the MUTANIMAL trait »", [LEO_HEROS], [], {"en_main": ["ub032"]},
       heros="leonardo", main_exclusive=["ub032", "01089"], jouer=["ub032"]),
    # ub036 Party Wagon (32020 modifie)
    _c("ub036 Party Wagon : Leonardo (NINJA) : le [wild] paie seul son Katana (cout 1)",
       "« generate a [wild] resource for a player whose identity has the NINJA or TURTLE trait »",
       [LEO_HEROS, _jeu("ub036")], [], {"en_jeu": ["tl011"], "exhausted": ["ub036"]},
       heros="leonardo", main_exclusive=["tl011"], jouer=["tl011"]),
    _c("ub036 Party Wagon : Spider-Man heros (ni NINJA ni TURTLE) ne peut pas s'en servir",
       "contre-cas du trait du joueur", [HEROS, _jeu("ub036")], [], {"en_main": ["ub009"], "pret": ["ub036"]},
       main_exclusive=["ub009"], jouer=["ub009"]),
    # ub038 Pizza Time (37021 modifie)
    _c("ub038 Pizza Time : Leo (MUTANT) remelange 2 cartes d'identite de la defausse ; sans Pizzeria, pas de pioche",
       "« Choose up to 2 identity-specific cards in your discard pile and shuffle them into your deck »",
       [LEO_CIVIL, "Puzzle.CreatePlayerDiscardPile('tl003', 'tl004')"], [],
       {"dans_deck_joueur": ["tl003", "tl004"], "taille_main": 0},
       heros="leonardo", main_exclusive=["ub038"], jouer=["ub038"], cibles=["tl003", "tl004"], accepter_choix=True),
    _c("ub038 Pizza Time : Rupert's Pizzeria en jeu -> pioche 1",
       "« If Rupert's Pizzeria is in play, draw 1 card »",
       [LEO_CIVIL, _jeu("ub043"), "Puzzle.CreatePlayerDiscardPile('tl003', 'tl004')"], [],
       {"dans_deck_joueur": ["tl003"], "taille_main": 1},
       heros="leonardo", main_exclusive=["ub038"], jouer=["ub038"], cibles=["tl003", "tl004"], accepter_choix=True),
    _c("ub038 Pizza Time : X-Mansion (32049) n'est PAS Rupert's Pizzeria -> pas de pioche",
       "contre-cas du nom : le texte imprime « Rupert's Pizzeria »",
       [LEO_CIVIL, _jeu("32049"), "Puzzle.CreatePlayerDiscardPile('tl003', 'tl004')"], [],
       {"taille_main": 0}, heros="leonardo", main_exclusive=["ub038"], jouer=["ub038"],
       cibles=["tl003", "tl004"], accepter_choix=True),
    # ub043 Rupert's Pizzeria (32049 modifie)
    _c("ub043 Rupert's Pizzeria : soigne 1 degat de Leo (MUTANT)",
       "« heal 1 damage from a MUTANT, MUTANIMAL or NINJA character »",
       [LEO_CIVIL, _jeu("ub043"), "Puzzle.Damage('tl001b', 2)"], ["Puzzle.Action('ub043', 'AlterEgoAction')"],
       {"degats_identite": 1, "exhausted": ["ub043"]}, heros="leonardo", main_exclusive=["01089"],
       cibles=["tl001b"]),
    _c("ub043 Rupert's Pizzeria : soigne 1 degat d'un allie MUTANIMAL (Slash ub048, 2 -> 1)",
       "le trait MUTANIMAL est nouveau par rapport a X-Mansion",
       [LEO_CIVIL, _jeu("ub043"), _jeu("ub048"), "Puzzle.Damage('ub048', 2)"],
       ["Puzzle.Action('ub043', 'AlterEgoAction')"], {"degats": [["ub048", 1]]}, heros="leonardo",
       main_exclusive=["01089"], cibles=["ub048"]),
    # ub050 "Special Delivery!" (37031 modifie)
    _c("ub050 Special Delivery : remelange l'allie NINJA (ub025), pas Mockingbird",
       "« Choose up to 2 allies in your discard pile with the DIMENSION X, MUTANIMAL, or NINJA trait »",
       [LEO_CIVIL, "Puzzle.CreatePlayerDiscardPile('ub025', '01083')"], [],
       {"dans_deck_joueur": ["ub025"], "defausse": ["01083"]},
       heros="leonardo", main_exclusive=["ub050"], jouer=["ub050"], cibles=["ub025", "01083"], accepter_choix=True),
    _c("ub050 Special Delivery : Rupert's Pizzeria en jeu -> pioche 1",
       "« If Rupert's Pizzeria is in play, draw 1 card »",
       [LEO_CIVIL, _jeu("ub043"), "Puzzle.CreatePlayerDiscardPile('ub014')"], [],
       {"dans_deck_joueur": ["ub014"], "taille_main": 1},
       heros="leonardo", main_exclusive=["ub050"], jouer=["ub050"], cibles=["ub014"], accepter_choix=True),
    # ub052 Splinter Dojo (33021 modifie)
    _c("ub052 Splinter Dojo : un allie NINJA entre en jeu -> amelioration TRAINING du deck attachee",
       "« search your deck and discard pile for a TRAINING upgrade and attach it to that ally »",
       [LEO_CIVIL, _jeu("ub052"), SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '32013', '01089')"], [],
       {"accroche_a": [["32013", "ub008"]], "exhausted": ["ub052"]},
       heros="leonardo", main_exclusive=["ub008", "01090", "01088"], jouer=["ub008"], accepter_choix=True),
    _c("ub052 Splinter Dojo : TRAINING prise dans la DEFAUSSE",
       "« deck AND discard pile »",
       [LEO_CIVIL, _jeu("ub052"), SANS_DECK, "Puzzle.CreatePlayerDeck('01089')",
        "Puzzle.CreatePlayerDiscardPile('32013')"], [],
       {"accroche_a": [["32013", "ub008"]]},
       heros="leonardo", main_exclusive=["ub008", "01090", "01088"], jouer=["ub008"], accepter_choix=True),
    _c("ub052 Splinter Dojo : allie SANS les traits (Mockingbird) -> rien",
       "contre-cas MUTANIMAL / NINJA",
       [LEO_CIVIL, _jeu("ub052"), SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '32013', '01089')"], [],
       {"hors_jeu": ["32013"], "pret": ["ub052"]},
       heros="leonardo", main_exclusive=["01083", "01090", "01088"], jouer=["01083"], cibles=["01094"],
       accepter_choix=True),
    _c("ub052 Splinter Dojo : Reponse d'ALTER EGO : rien en forme heros",
       "« Alter-Ego Response »",
       [LEO_HEROS, _jeu("ub052"), SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '32013', '01089')"], [],
       {"hors_jeu": ["32013"], "pret": ["ub052"]},
       heros="leonardo", main_exclusive=["ub008", "01090", "01088"], jouer=["ub008"], accepter_choix=True),
    # ub059 Weapon Harness (20021 modifie)
    _c("ub059 Weapon Harness : Leonardo (NINJA) controle 4 armes Restricted (2 + 2)",
       "« You may control 2 additional WEAPON upgrades that have the restricted keyword »",
       [LEO_HEROS, _jeu("ub059"), _jeu("tl011"), _jeu("tl012"), _jeu("tc007")], [],
       {"armes_restreintes": 4},
       heros="leonardo", main_exclusive=["tr011", "01090"], jouer=["tr011"], verifier="ub_armes"),
    _c("ub059 Weapon Harness : TEMOIN sans le harnais, une 3e arme Restricted ne reste pas (2 au plus)",
       "ligne de base : limite Restricted = 2",
       [LEO_HEROS, _jeu("tl011"), _jeu("tl012")], [], {"armes_restreintes": 2},
       heros="leonardo", main_exclusive=["tc007", "01090"], jouer=["tc007"], verifier="ub_armes"),
    _c("ub059 Weapon Harness : avec le harnais, une 5e arme Restricted ne reste pas (4 au plus : 2 de plus, pas 3)",
       "la limite mord a 4",
       [LEO_HEROS, _jeu("ub059"), _jeu("tl011"), _jeu("tl012"), _jeu("tc007"), _jeu("tr011")], [],
       {"armes_restreintes": 4},
       heros="leonardo", main_exclusive=["tc010", "01090"], jouer=["tc010"], verifier="ub_armes"),
    _c("ub059 Weapon Harness : NON jouable par Spider-Man (sans NINJA)",
       "« Play only if your identity has the NINJA trait »", [HEROS], [], {"en_main": ["ub059"]},
       main_exclusive=["ub059"], jouer=["ub059"]),
]

# ============================================================================ NOUVELLES
CAS += [
    # ub005 Casey Jones
    _c("ub005 Casey Jones : entree en jeu -> une amelioration WEAPON du deck en main",
       "« search your deck and discard pile for a WEAPON upgrade and add it to your hand »",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', 'tl011', '01089')"], [],
       {"en_main": ["tl011"], "en_jeu": ["ub005"]},
       main_exclusive=["ub005", "01090", "01088"], jouer=["ub005"], accepter_choix=True),
    _c("ub005 Casey Jones : WEAPON prise dans la DEFAUSSE",
       "« deck AND discard pile »",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089')", "Puzzle.CreatePlayerDiscardPile('tl011')"], [],
       {"en_main": ["tl011"]}, main_exclusive=["ub005", "01090", "01088"], jouer=["ub005"], accepter_choix=True),
    _c("ub005 Casey Jones : une amelioration NON WEAPON (Web-Shooter 01008) n'est pas prise",
       "contre-cas du trait WEAPON",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01008', '01089')"], [],
       {"absent_main": ["01008"]}, main_exclusive=["ub005", "01090", "01088"], jouer=["ub005"],
       accepter_choix=True),
    # ub008 Donatello
    _c("ub008 Donatello : entree en jeu -> pioche 2 (main 0 -> 2)",
       "« After Donatello enters play, draw 2 cards »",
       [HEROS], [], {"taille_main": 2, "en_jeu": ["ub008"]},
       main_exclusive=["ub008", "01090", "01088"], jouer=["ub008"], accepter_choix=True),
    # ub014 Fugitoid
    _c("ub014 Fugitoid : attaque, defausse Energy ([energy]) -> 2 degats a un ennemi (Rhino 1 + 2 = 3)",
       "« [energy] - Deal 2 damage to an enemy »",
       [HEROS, _jeu("ub014")], ["Puzzle.Attack('ub014')"], {"degats": [["01094", 3]], "taille_main": 0},
       main_exclusive=["01088"], cibles=["01094"], accepter_choix=True),
    _c("ub014 Fugitoid : contre, defausse Genius ([mental]) -> retire 2 menaces de plus (5 -> 2)",
       "« [mental] - Remove 2 threat from a scheme »",
       [HEROS, _jeu("ub014")], ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Thwart('ub014')"],
       {"menace": [["01097b", 2]]}, main_exclusive=["01089"], cibles=["01097b"], accepter_choix=True),
    _c("ub014 Fugitoid : defausse Strength ([physical]) -> soigne 2 a Spider-Man (3 -> 1)",
       "« [physical] - Heal 2 damage from a friendly character »",
       [HEROS, _jeu("ub014"), "Puzzle.Damage('01001a', 3)"], ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Thwart('ub014')"],
       {"degats_identite": 1}, main_exclusive=["01090"], cibles=["01097b", "01001a"], accepter_choix=True),
    _c("ub014 Fugitoid : defausse Digging Deep ([wild]) -> pioche 1",
       "« [wild] - Draw 1 card »",
       [HEROS, _jeu("ub014")], ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Thwart('ub014')"], {"taille_main": 1, "defausse": ["ub007"]},
       main_exclusive=["ub007"], cibles=["01097b"], accepter_choix=True),
    _c("ub014 Fugitoid : main vide -> rien a defausser, aucun effet (Rhino 1 degat de l'attaque seulement)",
       "« discard 1 card from your hand » : sans carte, aucune icone",
       [HEROS, _jeu("ub014"), "Puzzle.EmptyHand()"], ["Puzzle.Attack('ub014')"], {"degats": [["01094", 1]]},
       cibles=["01094"], accepter_choix=True),
    # ub020 Improvised Club
    _c("ub020 Improvised Club : l'allie porteur attaque et blesse un sbire -> defausse, sbire sonne",
       "« After attached ally attacks and damages a minion, discard Improvised Club -> stun that minion »",
       [HEROS, _jeu("ub025"), "Puzzle.PutIntoPlay('01101')"], [],
       {"statuts": [["01101", "Stunned"]], "hors_jeu": ["ub020"], "degats": [["01101", 2]]},
       main_exclusive=["ub020", "01088"], jouer=["ub020"], declencher_apres=["Puzzle.Attack('ub025')"],
       cibles=["ub025", "01101"], accepter_choix=True),
    _c("ub020 Improvised Club : l'allie attaque le VILAIN -> pas de Reponse (un sbire seulement)",
       "contre-cas « a minion »",
       [HEROS, _jeu("ub025")], [],
       {"statuts_absents": [["01094", "Stunned"]], "en_jeu": ["ub020"], "degats": [["01094", 2]]},
       main_exclusive=["ub020", "01088"], jouer=["ub020"], declencher_apres=["Puzzle.Attack('ub025')"],
       cibles=["ub025", "01094"], accepter_choix=True),
    # ub022 Jennika
    _c("ub022 Jennika : entree en jeu -> une carte Shinobi (Decisive Strike, Taijutsu) de la defausse sur le deck",
       "« put a Shinobi card from your discard pile on top of your deck » : la pioche suivante la rend",
       [HEROS, "Puzzle.CreatePlayerDiscardPile('tj004')"], [],
       {"en_main": ["tj004"], "en_jeu": ["ub022"]},
       main_exclusive=["ub022", "01090", "01088"], jouer=["ub022"], declencher_apres=["Puzzle.Draw(1)"],
       accepter_choix=True),
    _c("ub022 Jennika : une carte NON Shinobi (Composure tj002) reste en defausse",
       "contre-cas : seules les 4 classes Shinobi comptent (fiche shinobi.md)",
       [HEROS, "Puzzle.CreatePlayerDiscardPile('tj002')"], [],
       {"defausse": ["tj002"]},
       main_exclusive=["ub022", "01090", "01088"], jouer=["ub022"], accepter_choix=True),
    # ub023 Katsuichi
    _c("ub023 Katsuichi : entree en jeu -> une carte d'identite du deck en main",
       "« search your deck for an identity-specific card and add it to your hand »",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01005', '01089')"], [],
       {"en_main": ["01005"]}, main_exclusive=["ub023", "01090", "01088"], jouer=["ub023"], accepter_choix=True),
    _c("ub023 Katsuichi : une carte de base (01086) n'est pas prise",
       "contre-cas « identity-specific »",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01086', '01089')"], [],
       {"absent_main": ["01086"]}, main_exclusive=["ub023", "01090", "01088"], jouer=["ub023"],
       accepter_choix=True),
    # ub025 Leonardo
    _c("ub025 Leonardo : apres son attaque, redresse un AUTRE allie NINJA (Donatello)",
       "« After Leonardo uses a basic power, ready another NINJA ally you control »",
       [HEROS, _jeu("ub025"), _jeu("ub008"), "Puzzle.Exhaust('ub008')"], ["Puzzle.Attack('ub025')"],
       {"pret": ["ub008"], "exhausted": ["ub025"], "degats": [["01094", 2]]},
       main_exclusive=["01089"], cibles=["01094", "ub008"], accepter_choix=True),
    _c("ub025 Leonardo : un allie NON NINJA (Mockingbird) reste incline",
       "contre-cas du trait NINJA",
       [HEROS, _jeu("ub025"), _jeu("01083"), "Puzzle.Exhaust('01083')"], ["Puzzle.Attack('ub025')"],
       {"exhausted": ["01083", "ub025"]}, main_exclusive=["01089"], cibles=["01094", "01083"], accepter_choix=True),
    # ub027 Martial Arts Training
    _c("ub027 Martial Arts Training : en forme heros, Spider-Man gagne MARTIAL ARTIST",
       "« Your hero gains the MARTIAL ARTIST trait »",
       [HEROS], [], {"traits": ["MARTIAL ARTIST"], "en_jeu": ["ub027"]},
       main_exclusive=["ub027", "01089"], jouer=["ub027"]),
    _c("ub027 Martial Arts Training : en forme ALTER EGO, pas de trait",
       "« Your HERO » : Peter Parker ne le gagne pas", [], [], {"traits_absents": ["MARTIAL ARTIST"]},
       main_exclusive=["ub027", "01089"], jouer=["ub027"]),
    _c("ub027 Martial Arts Training : le trait accorde fait partir Splinter (ub053) sur le contre de Spider-Man",
       "le trait est REEL pour les autres cartes : +1 au contre (THW 1 -> 2, menace 5 -> 3)",
       [HEROS, _jeu("ub053")], ["Puzzle.SetThreat('01097b', 5)"],
       {"menace": [["01097b", 3]], "exhausted": ["ub053"]},
       main_exclusive=["ub027", "01089"], jouer=["ub027"], declencher_apres=["Puzzle.Thwart('01001a')"],
       cibles=["01097b"], accepter_choix=True),
    _c("ub027 Martial Arts Training : Starting ACCEPTE, la carte est dans la main de depart",
       "mot-cle Starting (fiche starting.md) : deck de test = Spider-Man avec ub027 a la place de 01093",
       [], [], {"en_main": ["ub027"]}, heros=DECK_STARTING,
       options_attendues_mise_en_place=["Add this card to your starting hand"]),
    _c("ub027 Martial Arts Training : Starting REFUSE, la carte n'est pas ajoutee",
       "« You MAY add » : le refus est possible",
       [], [], {"absent_main": ["ub027"]}, heros=DECK_STARTING, refuser_mise_en_place="starting hand",
       options_attendues_mise_en_place=["Add this card to your starting hand"]),
    # ub029 Michelangelo
    _c("ub029 Michelangelo : entree en jeu -> soigne 2 a Spider-Man (3 -> 1)",
       "« heal 2 damage from a friendly character »",
       [HEROS, "Puzzle.Damage('01001a', 3)"], [], {"degats_identite": 1, "en_jeu": ["ub029"]},
       main_exclusive=["ub029", "01090", "01088"], jouer=["ub029"], cibles=["01001a"], accepter_choix=True),
    _c("ub029 Michelangelo : peut soigner un ALLIE (Mockingbird 2 -> 0)",
       "« a friendly CHARACTER » : allie compris",
       [HEROS, _jeu("01083"), "Puzzle.Damage('01083', 2)"], [], {"degats": [["01083", 0]]},
       main_exclusive=["ub029", "01090", "01088"], jouer=["ub029"], cibles=["01083"], accepter_choix=True),
    # ub033 Ninja He-Man
    _c("ub033 Ninja He-Man : Leonardo (NINJA) le joue ; entree en jeu -> camoufle ; Tenacite",
       "« Toughness » + « After Ninja He-Man enters play, cloak him »",
       [LEO_HEROS], [], {"statuts": [["ub033", "Cloaked"], ["ub033", "Tough"]], "en_jeu": ["ub033"]},
       heros="leonardo", main_exclusive=["ub033", "01090", "01088"], jouer=["ub033"], accepter_choix=True),
    _c("ub033 Ninja He-Man : NON jouable par Spider-Man sans carte NINJA ni WARRIOR",
       "« Play only if you control a NINJA or WARRIOR card »",
       [HEROS], [], {"en_main": ["ub033"]}, main_exclusive=["ub033", "01090", "01088"], jouer=["ub033"]),
    _c("ub033 Ninja He-Man : jouable par Spider-Man s'il controle une carte NINJA (Shuriken attache)",
       "« a NINJA or WARRIOR CARD » : toute carte, ici une amelioration",
       [HEROS, "Puzzle.Attach('ub046', '01001a')"], [], {"en_jeu": ["ub033"]},
       main_exclusive=["ub033", "01090", "01088"], jouer=["ub033"], accepter_choix=True),
    # ub037 Pepperoni
    _c("ub037 Pepperoni : Spider-Man vainc un sbire -> s'incline, 1 pep retire, +1 taille de main",
       "« After you defeat an enemy ..., exhaust Pepperoni and remove 1 pep counter -> +1 hand size until the end of the phase »",
       [HEROS, _jeu("ub037"), "Puzzle.Damage(Puzzle.PutIntoPlay('01101'), 2)"], ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["01101"], "attributs": {"hand_size": 1}, "compteurs": [["ub037", "pep", 2]],
        "exhausted": ["ub037"]},
       main_exclusive=["01089"], cibles=["01101"], accepter_choix=True),
    _c("ub037 Pepperoni : Spider-Man retire la DERNIERE menace d'une manigance annexe -> +1 taille de main",
       "« or remove the last threat from a scheme »",
       [HEROS, _jeu("ub037"), "Puzzle.PutIntoPlay('01107')"], ["Puzzle.SetThreat('01107', 1)",
                                                             "Puzzle.Thwart('01001a')"],
       {"hors_jeu": ["01107"], "attributs": {"hand_size": 1}, "compteurs": [["ub037", "pep", 2]]},
       main_exclusive=["01089"], cibles=["01107"], accepter_choix=True),
    _c("ub037 Pepperoni : dernier pep retire -> defaussee (Uses)",
       "Uses : la carte part avec son dernier compteur (fiche uses.md)",
       [HEROS, _jeu("ub037"), "Puzzle.Counter('ub037', 'pep', -2)",
        "Puzzle.Damage(Puzzle.PutIntoPlay('01101'), 2)"], ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["ub037", "01101"], "attributs": {"hand_size": 1}},
       main_exclusive=["01089"], cibles=["01101"], accepter_choix=True),
    _c("ub037 Pepperoni : TEMOIN, un ennemi blesse mais pas vaincu -> rien",
       "contre-cas « defeat »",
       [HEROS, _jeu("ub037"), "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('01001a')"],
       {"en_jeu": ["01101"], "attributs": {"hand_size": 0}, "compteurs": [["ub037", "pep", 3]]},
       main_exclusive=["01089"], cibles=["01101"], accepter_choix=True),
    # ub040 Press and Protect
    _c("ub040 Press and Protect : April (ub001) et Casey (tr002) en jeu : 3 menaces retirees, Tenace sur Spider-Man",
       "Team-Up (April O'Neil and Casey Jones) + « Remove 3 threat from a scheme and give a tough status card »",
       [HEROS, _jeu("ub001"), _jeu("tr002")], ["Puzzle.SetThreat('01097b', 5)"],
       {"menace": [["01097b", 2]], "statuts": [["01001a", "Tough"]], "defausse": ["ub040"]},
       main_exclusive=["ub040", "01089"], jouer=["ub040"], cibles=["01097b", "01001a"]),
    _c("ub040 Press and Protect : sans Casey Jones -> injouable",
       "Team-Up : les DEUX personnages nommes", [HEROS, _jeu("ub001")], [], {"en_main": ["ub040"]},
       main_exclusive=["ub040", "01089"], jouer=["ub040"], cibles=["01097b", "01001a"]),
    # ub041 Raphael
    _c("ub041 Raphael : 1 degat -> +1 ATQ", "« +1 ATK for each damage token here »",
       [HEROS, _jeu("ub041"), "Puzzle.Damage('ub041', 1)"], [], {"attributs_carte": [["ub041", "attack", 1]]},
       main_exclusive=["01089"]),
    _c("ub041 Raphael : 2 degats -> +2 ATQ", "idem, 2 jetons",
       [HEROS, _jeu("ub041"), "Puzzle.Damage('ub041', 2)"], [], {"attributs_carte": [["ub041", "attack", 2]]},
       main_exclusive=["01089"]),
    _c("ub041 Raphael : 4 degats (Reinforced Suit, 5 PV) -> plafond +2 ATQ",
       "« to a maximum of +2 ATK »",
       [HEROS, _jeu("ub041"), "Puzzle.Attach('12018', 'ub041')", "Puzzle.Damage('ub041', 4)"], [],
       {"attributs_carte": [["ub041", "attack", 2]], "en_jeu": ["ub041"]}, main_exclusive=["01089"]),
    _c("ub041 Raphael : intact -> ATQ imprimee", "temoin : 0 degat", [HEROS, _jeu("ub041")], [],
       {"attributs_carte": [["ub041", "attack", 0]]}, main_exclusive=["01089"]),
    # ub046 Shuriken
    _c("ub046 Shuriken : s'incliner et defausser 1 carte -> 1 degat a 2 ennemis (Rhino et le sbire)",
       "« Exhaust this card and discard 1 card from your hand -> deal 1 damage to up to 3 enemies »",
       [HEROS, "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attach('ub046', '01001a')", "Puzzle.Action('ub046')"],
       {"degats": [["01094", 1], ["01101", 1]], "exhausted": ["ub046"], "taille_main": 0},
       main_exclusive=["01089"], cibles=["01094", "01101", "01089"], accepter_choix=True),
    _c("ub046 Shuriken : main vide -> cout impayable, aucun degat",
       "contre-cas « discard 1 card from your hand » (cout)",
       [HEROS, "Puzzle.Attach('ub046', '01001a')", "Puzzle.EmptyHand()"], [],
       {"degats": [["01094", 0]], "pret": ["ub046"]}, cibles=["01094"], accepter_choix=True,
       declencher_tolerant=["Puzzle.Action('ub046')"]),
    # ub045 Shinobi Batman
    _c("ub045 Shinobi Batman : jouable par Leonardo (NINJA) ; vaincu -> une carte NINJA du deck en main",
       "« After Shinobi Batman leaves play, search your deck for a NINJA or VIGILANTE card »",
       [LEO_HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', 'tl011', '01089')"], [],
       {"en_main": ["tl011"], "hors_jeu": ["ub045"]},
       heros="leonardo", main_exclusive=["ub045", "01090", "01088"], jouer=["ub045"],
       declencher_apres=["Puzzle.Damage('ub045', 3)"], accepter_choix=True),
    _c("ub045 Shinobi Batman : NON jouable par Spider-Man (ni NINJA ni VIGILANTE controle)",
       "« Play only if you control a NINJA or VIGILANTE card »",
       [HEROS], [], {"en_main": ["ub045"]}, main_exclusive=["ub045", "01090", "01088"], jouer=["ub045"]),
    # ub049 Snow and Shadow
    _c("ub049 Snow and Shadow : Alopex et Nobody redresses, Nobody camoufle, Rhino hebete",
       "Team-Up (Alopex and Nobody) + « Ready Alopex and Nobody. Cloak a friendly character. Daze an enemy »",
       ["Puzzle.ChangeToFace('ta001b', 'ta001a')", _jeu("ta002"), "Puzzle.Exhaust('ta001a')",
        "Puzzle.Exhaust('ta002')"], [],
       {"pret": ["ta001a", "ta002"], "statuts": [["ta002", "Cloaked"], ["01094", "Dazed"]]},
       heros="alopex", main_exclusive=["ub049", "01089"], jouer=["ub049"], cibles=["ta002", "01094"]),
    _c("ub049 Snow and Shadow : sans Nobody -> injouable",
       "Team-Up : les DEUX personnages nommes",
       ["Puzzle.ChangeToFace('ta001b', 'ta001a')"], [], {"en_main": ["ub049"]},
       heros="alopex", main_exclusive=["ub049", "01089"], jouer=["ub049"], cibles=["ta001a", "01094"]),
]


# ===================================================================== retouches du 17/10/2026
# ub002 / ub047 : traits confirmes par l'utilisateur ; ub019 Honorable Blades (Team-Up, NOUVELLE)
CAS.append(_c("ub002 Assess the Situation : porte le trait TACTIC (oubli de l'auteur confirme le 17/10/2026)",
              "Paper.Load lit `traits` sur l'entree du reskin ; comme 12033",
              [HEROS, "Puzzle.Gain('ub002')"], [],
              {"carte": "ub002", "presents": ["TACTIC"], "nom": "Assess the Situation"},
              verifier="tmnt_donnees_carte"))
CAS.append(_c("ub047 Sky Wagon : traits du scan NYC et VEHICLE, PAS LOCATION (confirme le 17/10/2026)",
              "Paper.Load lit `traits` sur l'entree du reskin ; Helicarrier (01092) est LOCATION, Sky Wagon non",
              [HEROS, _jeu("ub047")], [],
              {"carte": "ub047", "presents": ["NYC", "VEHICLE"], "absents": ["LOCATION", "S.H.I.E.L.D"],
               "nom": "Sky Wagon"}, verifier="reskin_identite"))

USAGI = [_jeu("up041"), "Puzzle.Tough('up041')"]      # Usagi entre en jeu Tenace (Toughness) : on retire l'etat
CAS += [
    _c("ub019 Honorable Blades : Leonardo ET Usagi en jeu -> les deux redresses, Leonardo camoufle, Usagi Tenace",
       "Team-Up (Leonardo and Usagi Yojimbo) ; « Ready Leonardo and Usagi. Cloak Leonardo. Place a tough status "
       "card on Usagi » : les deux inclines au depart, Usagi sans Tenace",
       [LEO_HEROS, *USAGI, "Puzzle.Exhaust('tl001a')", "Puzzle.Exhaust('up041')"], [],
       {"pret": ["tl001a", "up041"], "statuts": [["tl001a", "Cloaked"], ["up041", "Tough"]],
        "statuts_absents": [["up041", "Cloaked"], ["tl001a", "Tough"]], "defausse": ["ub019"]},
       heros="leonardo", main_exclusive=["ub019", "01088"], jouer=["ub019"]),
    _c("ub019 Honorable Blades : Leonardo ET Usagi en jeu -> jouable (contre-cas des deux suivants)",
       "les deux personnages nommes sont en jeu : la condition Team-Up est remplie",
       [LEO_HEROS, *USAGI, "Puzzle.Gain('ub019')"], [], {"carte": "ub019", "jouable": True, "en_jeu": 0},
       heros="leonardo", main=["01088"], verifier="max_par_joueur_jouable"),
    _c("ub019 Honorable Blades : Leonardo SANS Usagi -> PAS jouable",
       "Team-Up : « les DEUX personnages (identite ou allie) en jeu »",
       [LEO_HEROS, "Puzzle.Gain('ub019')"], [], {"carte": "ub019", "jouable": False, "en_jeu": 0},
       heros="leonardo", main=["01088"], verifier="max_par_joueur_jouable"),
    _c("ub019 Honorable Blades : Usagi SANS Leonardo (Spider-Man) -> PAS jouable",
       "Team-Up : l'identite n'est pas Leonardo",
       [HEROS, *USAGI, "Puzzle.Gain('ub019')"], [], {"carte": "ub019", "jouable": False, "en_jeu": 0},
       main=["01088"], verifier="max_par_joueur_jouable"),
]


VERIFICATIONS = r'''
def ub_allies(monde, aides):
    """`allies` : nombre d'allies en jeu controles par le joueur 1 (limite d'allies : le surplus est defausse)."""
    attendu = aides["cas"]["attendu"]
    n = len(list(monde.players[0].GetControlAllies()))
    if n != attendu["allies"]:
        return False, f"{n} allies en jeu (attendu {attendu['allies']})"
    return True, f"{n} allies en jeu"

def ub_armes(monde, aides):
    """`armes_restreintes` : nombre d'ameliorations WEAPON Restricted en jeu chez le joueur 1."""
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    n = 0
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is None or not face.IsInPlay() or not face.HasTrait("WEAPON"):
            continue
        if not getattr(face, "restricted", 0):
            continue
        if face.GetControlByPlayer() == joueur:
            n += 1
    if n != attendu["armes_restreintes"]:
        return False, f"{n} armes Restricted en jeu (attendu {attendu['armes_restreintes']})"
    return True, f"{n} armes Restricted en jeu"

def ub_apres_fin_de_round(monde, aides):
    """Envoie une vraie fin de round (WhenRoundEnd, temporaires, AfterRoundEnd) puis `etat_attendu`."""
    from game.message import Message
    from game.effect.rule import GameRule
    m = Message.WhenRoundEnd(monde)
    m.Send()
    monde.buff_manager.OnRoundEnd()
    monde.ProcessTemporary(GameRule(monde.const_players[0].GetIdentity()))
    Message.AfterRoundEnd(m).Send()
    return etat_attendu(monde, aides)

def tmnt_donnees_carte(monde, aides):
    """Traits et nom d'une carte QUELLE QUE SOIT SA ZONE (main, deck, jeu) : un evenement n'est jamais « en jeu ».
    `attendu` = {carte, presents, absents, nom}."""
    attendu = aides["cas"]["attendu"]
    face = None
    for objet in monde.object_manager.card_dict.values():
        f = objet.face
        if f is not None and getattr(f.paper, "card_id", None) == attendu["carte"]:
            face = f
            break
    if face is None:
        return False, f"{attendu['carte']} introuvable"
    soucis = []
    for t in attendu.get("presents", []):
        if not face.HasTrait(t):
            soucis.append(f"trait {t} absent")
    for t in attendu.get("absents", []):
        if face.HasTrait(t):
            soucis.append(f"trait {t} PRESENT")
    if "nom" in attendu and face.name != attendu["nom"]:
        soucis.append(f"nom {face.name!r} (attendu {attendu['nom']!r})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{attendu['carte']} : {face.name}, traits conformes"
'''
