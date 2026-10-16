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
              [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('{X}', '01089', '01089', '01089')"], [],
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
              [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('{X}', '01089', '01089', '01089')"], [],
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
              [_jeu("{X}")], [], {"en_jeu": ["ub009"], "exhausted": ["{X}"]},
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
              [HEROS, "Puzzle.SetThreat('01097b', 5)"], [], {"degats": [["01094", 2]], "menace": [["01097b", 5]]},
              main_exclusive=["{X}", "01090", "01090"], jouer=["{X}"], cibles=["01094"])
# ub031 Mutagen <- 38019 X-Gene
CAS += _paire("ub031", "38019", "({X}) : Ressource [wild] pour un evenement d'identite (Swinging Web Kick, cout 3)",
              "« generate a [wild] resource for an identity-specific event » : Strength (2) + Mutagen (1) = 3",
              [HEROS, _jeu("{X}")], [], {"degats": [["01094", 8]], "exhausted": ["{X}"]},
              main_exclusive=["01005", "01090"], jouer=["01005"], cibles=["01094"])
CAS += _paire("ub031", "38019", "({X}) : la ressource ne paie PAS un evenement de base (Basic Spell via Strength seul ? non : Multitalented)",
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
              [HEROS, _jeu("{X}"), _jeu("60007"), "Puzzle.SetThreat('01097b', 5)"], ["Puzzle.Thwart('60007')"],
              {"menace": [["01097b", 3]], "exhausted": ["{X}"]},
              main_exclusive=["01089"], cibles=["01097b"])
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


VERIFICATIONS = r'''
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
'''
