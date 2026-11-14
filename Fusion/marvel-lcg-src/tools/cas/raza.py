# Cas test_capacites du heros RAZA LONGKNIFE (Starjammers, prefixe `rl`) :
# noms prefixes « [rl] » puis le card_id (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck `raza` demarre en ALTER EGO (rl001b) ; `Puzzle.ChangeToFace('rl001b', 'rl001a')` la passe en HEROS ;
#  - « sustained 5 or more damage » : `Puzzle.Damage('rl001a', 5)` pose 5 degats SUR L'IDENTITE (seuil de la carte) ;
#  - Rhino 01094 est le vilain (ATQ 2, 14 PV), 01097b son complot principal (menace 0 au depart), 01101 Hydra Mercenary un sbire
#    (3 PV, ATQ 1, boost 1, Guard) ; 01098 Armored Rhino Suit n'a AUCUNE icone de boost ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ; 01083 Mockingbird (cout 3, 3 PV) est un allie ordinaire.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('rl001b', 'rl001a')"
VILAIN = "01094"
COMPLOT = "01097b"
SBIRE = "01101"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def abime(n=5):
    """« has sustained N or more damage » : N degats sur l'identite (forme heros)."""
    return [f"Puzzle.Damage('rl001a', {n})"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    base = [] if cle.pop("sans_deck_neutre", False) else SANS_BOOST
    mise = base + list(mise)
    cas = {"nom": "[rl] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "raza"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "rl_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ rl001a / rl001b : identite
    _c("rl001a Raza Longknife : valeurs imprimees PV 9, ATK 2, THW 2, DEF 2, HS 5, CYBORG STARJAMMER",
       "nombres texte <-> code (scan) : HAND SIZE 5 / HIT POINTS 9, THW 2 ATK 2 DEF 2",
       [HEROS], [], {"pv_max": [["rl001a", 9]], "traits": ["CYBORG", "STARJAMMER"],
                     "rl_stats": {"attack": 2, "thwart": 2, "defense": 2, "hand_size": 5}}),
    _c("rl001b Raza Longknife : valeurs imprimees PV 9, REC 4, HS 6, CYBORG OUTLAW",
       "nombres texte <-> code (scan) : HAND SIZE 6 / HIT POINTS 9 / REC 4",
       [], [], {"pv_max": [["rl001b", 9]], "traits": ["CYBORG", "OUTLAW"], "rl_stats": {"recover": 4, "hand_size": 6}}),
    _c("rl001a Alien Augmentations : une amelioration TECH ET WEAPON (Raza's Blaster) ne vaut qu'UN point de vie (9 -> 10)",
       "« +1 hit point for each TECH or WEAPON upgrade you control » : la meme carte porte les deux traits, comptee une fois",
       [HEROS] + en_jeu("rl010"), [], {"pv_max": [["rl001a", 10]]}, main_exclusive=["01090"]),
    _c("rl001a Alien Augmentations : trois ameliorations (TECH, TECH+WEAPON, WEAPON) -> 9 + 3 = 12 PV",
       "chaque amelioration TECH ou WEAPON compte une fois : rl009 (TECH), rl010 (TECH, WEAPON), rl011 (WEAPON)",
       [HEROS] + en_jeu("rl009", "rl010", "rl011"), [], {"pv_max": [["rl001a", 12]]}, main_exclusive=["01090"]),
    _c("rl001a Alien Augmentations : une amelioration TECH ATTACHEE a un allie (Mockingbird) NE COMPTE PAS : seule celle pres de l'identite vaut 1 PV (9 -> 10)",
       "« UNATTACHED TECH or WEAPON upgrade you control » : RR Upgrade, la plupart des ameliorations entrent pres de l'identite, certaines s'attachent (« attach to ») "
       "a une autre carte ; ces dernieres sont exclues (arbitrage du 26/10/2026)",
       [HEROS] + en_jeu("01083", "rl010", "rl011") + ["Puzzle.AttachReel('rl011', '01083')"], [], {"pv_max": [["rl001a", 10]]}, main_exclusive=["01090"]),
    _c("rl001a Alien Augmentations : CONTRE-CAS, une amelioration CONDITION (Warrior Pride) ne donne rien (9 PV)",
       "ni TECH ni WEAPON : aucun point de vie", [HEROS] + en_jeu("rl007"), [], {"pv_max": [["rl001a", 9]]},
       main_exclusive=["01090"]),
    _c("rl001a Alien Augmentations : l'amelioration QUITTE le jeu, le point de vie repart (10 -> 9)",
       "la valeur se recalcule quand une amelioration est defaussee",
       [HEROS] + en_jeu("rl010"), ["Puzzle.Discard('rl010')"], {"pv_max": [["rl001a", 9]]}, main_exclusive=["01090"]),
    _c("rl001b Alien Augmentations : en ALTER EGO aussi (Raza's Blaster en jeu -> 10 PV)",
       "la meme phrase est imprimee sur l'alter ego", en_jeu("rl010"), [], {"pv_max": [["rl001b", 10]]},
       main_exclusive=["01090"]),

    # ============================================================ rl002 Tolo Hawk
    _c("rl002 Tolo Hawk : valeurs imprimees cout 2, PV 2, ATQ 1*, THW 1*, STARJAMMER",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("rl002"), [],
       {"pv_max": [["rl002", 2]], "traits_de": [["rl002", "STARJAMMER"]],
        "attributs_carte": [["rl002", "attack", 0], ["rl002", "thwart", 0]]}, main_exclusive=["01090"]),
    _c("rl002 Tolo Hawk : defait par des degats CONSEQUENTS -> 1 degat a Raza, tous ses degats retires (il reste en jeu)",
       "« When Tolo Hawk would be defeated by consequential damage, instead deal 1 damage to Raza Longknife and remove all damage from "
       "Tolo Hawk » : il a deja 1 degat (2 PV) et attaque Rhino : tout degat consequent le defait ; il reste en jeu, sans degat, et Raza en a 1",
       [HEROS] + en_jeu("rl002") + ["Puzzle.Damage('rl002', 1)"], ["Puzzle.Attack('rl002')"],
       {"en_jeu": ["rl002"], "degats": [["rl002", 0]], "degats_identite": 1},
       main_exclusive=["01090"], cibles=[VILAIN, VILAIN], accepter_choix=True),
    _c("rl002 Tolo Hawk : CONTRE-CAS, defait par des degats NON consequents -> il est defait normalement",
       "dommage direct de 2 sur 2 PV : l'Interruption ne vaut que pour les degats conséquents",
       [HEROS] + en_jeu("rl002"), ["Puzzle.Damage('rl002', 2)"],
       {"hors_jeu": ["rl002"], "degats_identite": 0}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ rl003 Breach Their Defenses!
    _c("rl003 Breach Their Defenses! : sans arme, 3 degats a Rhino",
       "« Deal 3 damage to an enemy » : aucune carte WEAPON en jeu", [HEROS], [],
       {"degats": [[VILAIN, 3]], "defausse": ["rl003"]},
       main_exclusive=["rl003", "01090"], payer_avec=["01090"], jouer=["rl003"], cibles=[VILAIN], accepter_choix=True),
    _c("rl003 Breach Their Defenses! : deux armes (Blaster, Sabre) -> 3 + 2 = 5 degats",
       "« Deal 1 additional damage for each WEAPON you control »", [HEROS] + en_jeu("rl010", "rl011"), [],
       {"degats": [[VILAIN, 5]], "defausse": ["rl003"]},
       main_exclusive=["rl003", "01090"], payer_avec=["01090"], jouer=["rl003"], cibles=[VILAIN], accepter_choix=True),
    _c("rl003 Breach Their Defenses! : CONTRE-CAS, une amelioration TECH sans WEAPON (Cybernetic Eye) ne compte pas (3 degats)",
       "seules les cartes WEAPON comptent", [HEROS] + en_jeu("rl009"), [],
       {"degats": [[VILAIN, 3]]},
       main_exclusive=["rl003", "01090"], payer_avec=["01090"], jouer=["rl003"], cibles=[VILAIN], accepter_choix=True),
    _c("rl003 Breach Their Defenses! : valeurs imprimees cout 2, trait ATTACK",
       "nombres texte <-> code (scan)", [HEROS], [], {"rl_traits_main": [["rl003", ["ATTACK"]]]}, main_exclusive=["rl003"]),

    # ============================================================ rl004 Boarding Action
    _c("rl004 Boarding Action : sans TECH, 2 menaces retirees (5 -> 3)",
       "« Remove 2 threat from a scheme »", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"menace": [[COMPLOT, 3]], "defausse": ["rl004"]},
       main_exclusive=["rl004", "01088"], payer_avec=["01088"], jouer=["rl004"], cibles=[COMPLOT], accepter_choix=True),
    _c("rl004 Boarding Action : deux cartes TECH (Eye, Blaster) -> 2 + 2 = 4 menaces retirees (6 -> 2)",
       "« Remove 1 additional threat for each TECH you control »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"] + en_jeu("rl009", "rl010"), [],
       {"menace": [[COMPLOT, 2]]},
       main_exclusive=["rl004", "01088"], payer_avec=["01088"], jouer=["rl004"], cibles=[COMPLOT], accepter_choix=True),
    _c("rl004 Boarding Action : CONTRE-CAS, une arme sans TECH (Sabre) ne compte pas (6 -> 4)",
       "seules les cartes TECH comptent", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 6)"] + en_jeu("rl011"), [],
       {"menace": [[COMPLOT, 4]]},
       main_exclusive=["rl004", "01088"], payer_avec=["01088"], jouer=["rl004"], cibles=[COMPLOT], accepter_choix=True),

    # ============================================================ rl005 Warrior Apotheosis
    _c("rl005 Warrior Apotheosis : Rhino attaque SANS carte de boost, puis ATK de Raza (2) en degats a Rhino",
       "« The villain attacks you. Do not deal the villain a boost card for this attack. Then, deal damage equal to Raza's ATK » : "
       "pioche rencontre garnie de 01101 (boost 1) : sans boost l'attaque (ATQ 2) est absorbee par la DEF 2 du heros (0 degat), une carte de boost aurait fait 1 ; le deck rencontre ne diminue pas",
       [HEROS, "Puzzle.EmptyEncounterDeck()",
        "Puzzle.CreateEncounterDeck('01101', '01101', '01101', '01101', '01101', '01101', '01101', '01101')"], [],
       {"degats": [[VILAIN, 2]], "degats_identite": 0, "rl_deck_rencontre": 8},
       sans_deck_neutre=True, main_exclusive=["rl005"], jouer=["rl005"], accepter_choix=True),
    _c("rl005 Warrior Apotheosis : un sbire engage attaque AUSSI et subit l'ATK de Raza (Hydra Mercenary 3 PV : 2 degats)",
       "« Engage any number of minions in play ... each minion engaged with you attacks you ... deal damage equal to Raza's ATK to each enemy that attacked you this way » : le sbire n'est PAS engage au depart",
       [HEROS, "Puzzle.PutIntoPlay('01101', under_control=False)"], [],
       {"degats": [[VILAIN, 2], [SBIRE, 2]], "rl_engage": [[SBIRE, True]]},
       main_exclusive=["rl005"], jouer=["rl005"], accepter_choix=True),
    _c("rl005 Warrior Apotheosis : l'ATK utilisee est CELLE DE RAZA, Sabre compris (2 + 1 = 3 degats a Rhino)",
       "« damage equal to Raza's ATK » : le Sabre donne +1 ATK", [HEROS] + en_jeu("rl011"), [],
       {"degats": [[VILAIN, 3]]},
       main_exclusive=["rl005"], jouer=["rl005"], accepter_choix=True),
    _c("rl005 Warrior Apotheosis : valeurs imprimees cout 0",
       "nombres texte <-> code (scan)", [HEROS], [], {"rl_main": ["rl005"]}, main_exclusive=["rl005"]),

    # ============================================================ rl006 Implanted Tools
    _c("rl006 Implanted Tools : s'incline avec une autre amelioration TECH pour payer un Sabre (cout 1)",
       "« Exhaust Implanted Tools and another TECH upgrade you control -> generate a [wild] resource » : main vide sauf le Sabre",
       [HEROS, "Puzzle.EmptyHand()"] + en_jeu("rl006", "rl009"), [],
       {"en_jeu": ["rl011"], "exhausted": ["rl006", "rl009"]},
       main_exclusive=["rl011"], jouer=["rl011"], accepter_choix=True),
    _c("rl006 Implanted Tools : CONTRE-CAS, sans autre amelioration TECH la ressource n'est pas offerte (le Sabre reste en main)",
       "« and another TECH upgrade you control » : Implanted Tools seule ne suffit pas", [HEROS] + en_jeu("rl006"), [],
       {"pret": ["rl006"], "rl_main": ["rl011"]},
       main_exclusive=["rl011"], jouer=["rl011"], accepter_choix=True),
    _c("rl006 Implanted Tools : CONTRE-CAS, une amelioration NON TECH (Sabre en jeu) ne convient pas",
       "l'autre carte doit etre une amelioration TECH", [HEROS] + en_jeu("rl006", "rl011"), [],
       {"pret": ["rl006", "rl011"], "rl_main": ["rl007"]},
       main_exclusive=["rl007"], jouer=["rl007"], accepter_choix=True),

    # ============================================================ rl007 Warrior Pride
    _c("rl007 Warrior Pride : Rhino attaque -> pioche 1 carte (main 0 -> 1), pas de soin sous 5 degats",
       "« When the villain attacks you, draw 1 card. If you have sustained 5 or more damage, heal 1 » : 1 degat subi avant",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074', '01073')", "Puzzle.Damage('rl001a', 1)"] + en_jeu("rl007"),
       ["Puzzle.Attack('01094')"],
       {"taille_main": 1, "degats_identite": 1}, accepter_choix=True),
    _c("rl007 Warrior Pride : a 5 degats ou plus, elle soigne AUSSI 1 degat avant l'attaque",
       "5 degats subis : pioche 1 ET soigne 1 degat de l'identite (5 -> 4 ; l'attaque de Rhino est absorbee par la DEF 2 du heros)",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074', '01073')"] + abime(5) + en_jeu("rl007"),
       ["Puzzle.Attack('01094')"],
       {"taille_main": 1, "degats_identite": 4}, accepter_choix=True),
    _c("rl007 Warrior Pride : CONTRE-CAS, un SBIRE qui attaque ne la declenche pas (« the villain »)",
       "seul le vilain compte", [HEROS, "Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074', '01073')"] + en_jeu("rl007", SBIRE),
       ["Puzzle.Attack('01101')"],
       {"taille_main": 0}, accepter_choix=True),

    # ============================================================ rl008 Raza's Cybernetic Arm
    _c("rl008 Raza's Cybernetic Arm : permet de controler UNE amelioration RESTRICTED de plus (3e Restricted jouee)",
       "« You can control 1 additional upgrade that has the restricted keyword » : Blaster + Sabre en jeu, le Bouclier de Captain America "
       "(Restricted) peut etre joue avec le Bras",
       [HEROS] + en_jeu("rl008", "rl010", "rl011"), [],
       {"en_jeu": ["03009", "rl010", "rl011"], "rl_en_jeu_parmi": [["rl010", "rl011", "03009"], 3]},
       main_exclusive=["03009", "01090"], payer_avec=["01090"], jouer=["03009"], accepter_choix=True),
    _c("rl008 Raza's Cybernetic Arm : CONTRE-CAS, sans le Bras une 3e Restricted force a en defausser une (2 restent en jeu)",
       "limite imprimee « Max 2 restricted cards per player » : la 3e Restricted en jeu force a en DEFAUSSER une : 2 seulement restent", [HEROS] + en_jeu("rl010", "rl011"), [],
       {"rl_en_jeu_parmi": [["rl010", "rl011", "03009"], 2]},
       main_exclusive=["03009", "01090"], payer_avec=["01090"], jouer=["03009"], accepter_choix=True),
    _c("rl008 Raza's Cybernetic Arm : a 5 degats ou plus, Raza gagne Retaliate 1 (Rhino qui l'attaque subit 1 degat)",
       "« While your identity has sustained 5 or more damage, you gain Retaliate 1 »", [HEROS] + abime(5) + en_jeu("rl008"),
       ["Puzzle.Attack('01094')"], {"degats": [[VILAIN, 1]]}, accepter_choix=True),
    _c("rl008 Raza's Cybernetic Arm : CONTRE-CAS, sous 5 degats (4) aucune riposte",
       "le seuil est de 5", [HEROS] + abime(4) + en_jeu("rl008"),
       ["Puzzle.Attack('01094')"], {"degats": [[VILAIN, 0]]}, accepter_choix=True),
    _c("rl008 Raza's Cybernetic Arm : a 4 degats, une attaque NON DEFENDUE le fait passer a 6 -> Retaliate 1 part (parenthese imprimee)",
       "« (Retaliate will trigger for attacks that cause Raza to gain Retaliate) » : RR 1.8, Retaliate est une Reponse forcee APRES l'attaque ; "
       "Raza (epuise, il ne peut pas defendre) subit les 2 de Rhino : 4 + 2 = 6 >= 5, Rhino subit 1 (arbitrage du 26/10/2026)",
       [HEROS] + abime(4) + en_jeu("rl008") + ["Puzzle.Exhaust('rl001a')"],
       ["Puzzle.Attack('01094')"], {"degats": [[VILAIN, 1]], "degats_identite": 6}, accepter_choix=True),
    _c("rl008 Raza's Cybernetic Arm : TEMOIN, a 2 degats une attaque NON DEFENDUE (2 + 2 = 4, sous le seuil) ne declenche AUCUNE riposte",
       "meme montage, seuil non atteint apres l'attaque",
       [HEROS] + abime(2) + en_jeu("rl008") + ["Puzzle.Exhaust('rl001a')"],
       ["Puzzle.Attack('01094')"], {"degats": [[VILAIN, 0]], "degats_identite": 4}, accepter_choix=True),
    _c("rl008 Raza's Cybernetic Arm : valeurs imprimees cout 1, traits TECH WEAPON",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("rl008"), [],
       {"traits_de": [["rl008", "TECH"], ["rl008", "WEAPON"]]}, main_exclusive=["01090"]),

    # ============================================================ rl009 Raza's Cybernetic Eye
    _c("rl009 Raza's Cybernetic Eye : apres l'attaque du vilain, 1 menace retiree (5 -> 4)",
       "« After the villain attacks you, remove 1 threat from a scheme »", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.Damage('rl001a', 1)"] + en_jeu("rl009"),
       ["Puzzle.Attack('01094')"], {"menace": [[COMPLOT, 4]]}, cibles=[COMPLOT], accepter_choix=True),
    _c("rl009 Raza's Cybernetic Eye : a 5 degats ou plus, 2 menaces retirees (5 -> 3)",
       "« (2 threat if you have sustained 5 or more damage) »", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"] + abime(5) + en_jeu("rl009"),
       ["Puzzle.Attack('01094')"], {"menace": [[COMPLOT, 3]]}, cibles=[COMPLOT], accepter_choix=True),
    _c("rl009 Raza's Cybernetic Eye : CONTRE-CAS, l'attaque d'un SBIRE ne la declenche pas (menace inchangee)",
       "« After the villain attacks you » seulement", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"] + en_jeu("rl009", SBIRE),
       ["Puzzle.Attack('01101')"], {"menace": [[COMPLOT, 5]]}, cibles=[COMPLOT], accepter_choix=True),

    # ============================================================ rl010 Raza's Blaster
    _c("rl010 Raza's Blaster : Hero Action, s'incline -> 1 degat a Rhino",
       "« Exhaust Raza's Blaster -> deal 1 damage to an enemy »", [HEROS] + en_jeu("rl010"), ["Puzzle.Action('rl010', 'HeroAction')"],
       {"degats": [[VILAIN, 1]], "exhausted": ["rl010"]}, main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("rl010 Raza's Blaster : a 5 degats ou plus, 2 degats",
       "« (or 2 damage if you have sustained 5 or more damage) »", [HEROS] + abime(5) + en_jeu("rl010"), ["Puzzle.Action('rl010', 'HeroAction')"],
       {"degats": [[VILAIN, 2]], "exhausted": ["rl010"]}, main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("rl010 Raza's Blaster : valeurs imprimees cout 2, Restricted, TECH WEAPON",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("rl010"), [],
       {"traits_de": [["rl010", "TECH"], ["rl010", "WEAPON"]]}, main_exclusive=["01090"]),

    # ============================================================ rl011 Raza's Sabre
    _c("rl011 Raza's Sabre : +1 ATK au heros sous 5 degats (2 -> 3)",
       "« Raza gets +1 ATK »", [HEROS] + en_jeu("rl011"), [], {"attributs": {"attack": +1}}, main_exclusive=["01090"]),
    _c("rl011 Raza's Sabre : a 5 degats ou plus, +2 ATK (2 -> 4)",
       "« (+2 ATK instead if you have sustained 5 or more damage) » : +2 AU LIEU DE +1, pas +3", [HEROS] + abime(5) + en_jeu("rl011"), [],
       {"attributs": {"attack": +2}}, main_exclusive=["01090"]),
    _c("rl011 Raza's Sabre : le bonus suit les degats (heal 5 -> retour a +1)",
       "la valeur se recalcule quand les degats changent", [HEROS] + abime(5) + en_jeu("rl011") + ["Puzzle.Heal('rl001a', 5)"], [],
       {"attributs": {"attack": +1}}, main_exclusive=["01090"]),

    # ============================================================ rl012 Honour-Bound Warrior
    _c("rl012 Honour-Bound Warrior : le texte des ameliorations est BLANC (le Sabre ne donne plus +1 ATK)",
       "« Treat the textbox on each of your upgrades as blank »", [HEROS] + en_jeu("rl011") + ["Puzzle.Reveal('rl012')"], [],
       {"attributs": {"attack": 0}}, main_exclusive=["01090"], accepter_choix=True),
    _c("rl012 Honour-Bound Warrior : les TRAITS restent (Blaster TECH WEAPON compte toujours pour les PV de Raza : 10)",
       "« (except for TRAITS) » : Alien Augmentations compte les traits, pas le texte des ameliorations",
       [HEROS] + en_jeu("rl010") + ["Puzzle.Reveal('rl012')"], [], {"pv_max": [["rl001a", 10]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("rl012 Honour-Bound Warrior : Alter-Ego Action, incline Raza -> l'obligation quitte la partie",
       "« Exhaust Raza Longknife -> remove this card from the game »", [], ["Puzzle.Reveal('rl012')", "Puzzle.Action('rl012', 'AlterEgoAction')"],
       {"rl_retirees": ["rl012"], "exhausted": ["rl001b"]}, accepter_choix=True),
    _c("rl012 Honour-Bound Warrior : CONTRE-CAS, le texte redevient actif quand l'obligation part (Sabre : +1 ATK)",
       "l'effet « blanc » cesse avec l'obligation", [HEROS] + en_jeu("rl011") + ["Puzzle.Reveal('rl012')", "Puzzle.Remove('rl012')"], [],
       {"attributs": {"attack": +1}}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ rl013 Zzzxx
    _c("rl013 Zzzxx : valeurs imprimees PV 5, ATQ 2, SCH 1, ELITE SYMBIOTE",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("rl013"), [],
       {"pv_max": [["rl013", 5]], "traits_de": [["rl013", "ELITE"], ["rl013", "SYMBIOTE"]],
        "attributs_carte": [["rl013", "attack", 0], ["rl013", "scheme", 0]]}, main_exclusive=["01090"]),
    _c("rl013 Zzzxx : attaque un personnage a 5 degats -> une carte de BOOST est donnee (le deck rencontre diminue)",
       "« When Zzzxx activates against a character who has sustained 5 or more damage, it gains Villainous for that activation » : "
       "Villainous = une carte de boost a l'activation",
       [HEROS] + abime(5) + en_jeu("rl013"), ["Puzzle.Attack('rl013')"],
       {"rl_deck_rencontre": 7}, main_exclusive=["01090"], accepter_choix=True),
    _c("rl013 Zzzxx : CONTRE-CAS, sous 5 degats aucune carte de boost (le deck rencontre reste a 8)",
       "le seuil est de 5", [HEROS] + abime(4) + en_jeu("rl013"), ["Puzzle.Attack('rl013')"],
       {"rl_deck_rencontre": 8}, main_exclusive=["01090"], accepter_choix=True),
    _c("rl013 Zzzxx : Boost, il gagne autant d'icones de boost que le numero de stade du vilain (stade 1 : +1 -> Rhino 3 contre DEF 2 = 1 degat)",
       "« This card gains boost icons equal to the villain's stage number »",
       [HEROS, "Puzzle.GiveFacedownBoost('01094', 'rl013')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 1}, accepter_choix=True),

    # ============================================================ rl014 Symbiote Possession
    _c("rl014 Symbiote Possession : revelee, Zzzxx est mis en jeu ENGAGE avec le joueur",
       "« Find Zzzxx and put him into play engaged with you »", [HEROS, "Puzzle.CreateEncounterDeck('01098', 'rl013', '01098')"], ["Puzzle.Reveal('rl014')"],
       {"en_jeu": ["rl013"], "rl_engage": [["rl013", True]], "menace": [["rl014", 2]]}, sans_deck_neutre=True,
       main_exclusive=["01090"], accepter_choix=True),
    _c("rl014 Symbiote Possession : un joueur engage avec Zzzxx ne peut PAS l'attaquer",
       "« Players engaged with Zzzxx cannot attack Zzzxx »", [HEROS, "Puzzle.CreateEncounterDeck('01098', 'rl013', '01098')"],
       ["Puzzle.Reveal('rl014')", "Puzzle.Attack('rl001a')"],
       {"degats": [["rl013", 0]]}, sans_deck_neutre=True, main_exclusive=["01090"], cibles=["rl013"], accepter_choix=True),
    _c("rl014 Symbiote Possession : ... ni contrer un AUTRE complot (le complot principal garde sa menace)",
       "« or thwart schemes other than this one »", [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 3)", "Puzzle.CreateEncounterDeck('01098', 'rl013', '01098')"],
       ["Puzzle.Reveal('rl014')", "Puzzle.Thwart('rl001a')"],
       {"menace": [[COMPLOT, 3]]}, sans_deck_neutre=True, main_exclusive=["01090"], cibles=[COMPLOT], accepter_choix=True),
    _c("rl014 Symbiote Possession : ... mais PEUT contrer cette manigance annexe (THW 2 : menace 2 -> 0)",
       "« thwart schemes other than THIS one » : celle-ci reste permise", [HEROS, "Puzzle.CreateEncounterDeck('01098', 'rl013', '01098')"],
       ["Puzzle.Reveal('rl014')", "Puzzle.Thwart('rl001a')"],
       {"hors_jeu": ["rl014"]}, sans_deck_neutre=True, main_exclusive=["01090"], cibles=["rl014"], accepter_choix=True),

    # ============================================================ rl015 Shi'ar Host
    _c("rl015 Shi'ar Host : valeurs imprimees PV 3, ATQ 1, SCH 1, SHI'AR",
       "nombres texte <-> code (scan)", [HEROS] + en_jeu("rl015"), [],
       {"pv_max": [["rl015", 3]], "traits_de": [["rl015", "SHI'AR"]], "attributs_carte": [["rl015", "attack", 0], ["rl015", "scheme", 0]]},
       main_exclusive=["01090"]),
    _c("rl015 Shi'ar Host : revele, un attachement de la defausse rencontre s'attache a lui (Genetically Enhanced +3 PV)",
       "« Search the discard pile for an attachment that can be attached to Shi'Ar Host and attach it to them »",
       [HEROS, "Puzzle.EmptyEncounterDiscardPile()", "Puzzle.CreateEncounterDiscardPile('01163')"], ["Puzzle.Reveal('rl015')"],
       {"hotes": [["01163", "rl015"]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("rl015 Shi'ar Host : sans attachement en defausse, il gagne surge (la carte suivante du deck est revelee)",
       "« If no attachment was revealed this way, this card gains surge »",
       [HEROS, "Puzzle.EmptyEncounterDiscardPile()", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
       ["Puzzle.Reveal('rl015')"],
       {"carte_du_surge": SBIRE}, sans_deck_neutre=True, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ rl016 New Host
    _c("rl016 New Host : revelee, defausse le deck jusqu'a un sbire et s'attache a lui (Hydra Mercenary +1 ATQ : 2)",
       "« Discard cards from the top of the encounter deck until you discard a minion. Attach New Host to it »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01101', '01098')"], ["Puzzle.Reveal('rl016')"],
       {"hotes": [["rl016", SBIRE]], "attributs_carte": [[SBIRE, "attack", 1]]}, sans_deck_neutre=True, main_exclusive=["01090"], accepter_choix=True),
    _c("rl016 New Host : le sbire porteur est vaincu -> Zzzxx est mis en jeu engage avec le joueur",
       "« When attached minion is defeated, search the encounter deck and discard pile for Zzzxx and put it into play engaged with you »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01101', 'rl013', '01098')"],
       ["Puzzle.Reveal('rl016')", "Puzzle.Damage('01101', 5)"],
       {"en_jeu": ["rl013"], "rl_engage": [["rl013", True]]}, sans_deck_neutre=True, main_exclusive=["01090"], accepter_choix=True),
    _c("rl016 New Host : CONTRE-CAS, sans sbire dans le deck rencontre elle est defaussee (rien en jeu)",
       "aucun sbire a trouver : la carte n'a pas de porteur", [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01098')"],
       ["Puzzle.Reveal('rl016')"], {"hors_jeu": ["rl016"]}, sans_deck_neutre=True, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ rl017 Devour
    _c("rl017 Devour : revelee, un allie controle est defausse (Mockingbird)",
       "« Discard an ally you control »", [HEROS] + en_jeu("01083"), ["Puzzle.Reveal('rl017')"],
       {"defausse": ["01083"]}, main_exclusive=["01090"], cibles=["01083"], accepter_choix=True),
    _c("rl017 Devour : a DEUX joueurs, revelee par le joueur 2 qui controle deux allies -> c'est le PREMIER joueur (Raza) qui choisit lequel est defausse (RR First Player)",
       "« Discard an ally you control » : plusieurs cibles admissibles pour une carte de rencontre -> le premier joueur choisit (RR First Player, "
       "arbitrage du 26/10/2026) ; avant, le joueur qui revele choisissait",
       ["Puzzle.PutIntoPlay('01020', under_control=True, player=1)", "Puzzle.PutIntoPlay('01083', under_control=True, player=1)"], [],
       {"choisit": 0}, main_exclusive=["01090"], heros2="spider_man", verifier="rl_qui_choisit"),
    _c("rl017 Devour : sans allie, defausse le deck rencontre jusqu'a un sbire et le met en jeu engage (Hydra Mercenary)",
       "« If you cannot, discard cards from the top of the encounter deck until you discard a minion and put it into play engaged with you »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01101', '01098')"], ["Puzzle.Reveal('rl017')"],
       {"en_jeu": [SBIRE], "rl_engage": [[SBIRE, True]]}, sans_deck_neutre=True, main_exclusive=["01090"], accepter_choix=True),
    _c("rl017 Devour : Boost, l'attaque gagne OVERKILL (Rhino 2 + 2 icones = 4 contre Black Cat 2 PV : 2 degats d'exces au heros)",
       "« If this activation is an attack, this attack gains overkill » : l'exces sur l'allie passe a son controleur (Rhino attaque l'allie ; "
       "Black Cat sans effet a l'entree en jeu : Mockingbird sonnait Rhino et annulait l'attaque ; Tolo Hawk, lui, a sa propre Interruption)",
       [HEROS] + en_jeu("01002") + ["Puzzle.GiveFacedownBoost('01094', 'rl017')"], ["Puzzle.EnemyAttacks('01094', '01002')"],
       {"degats_identite": 2, "hors_jeu": ["01002"]}, main_exclusive=["01090"], passer_sur_option="Defense"),
    _c("rl017 Devour : TEMOIN d'overkill, meme montage avec New Host (2 icones, sans overkill) -> l'exces est perdu (0 degat au heros)",
       "meme attaque (2 + 2 = 4 contre 2 PV) sans la carte Devour : aucun exces sur le heros",
       [HEROS] + en_jeu("01002") + ["Puzzle.GiveFacedownBoost('01094', 'rl016')"], ["Puzzle.EnemyAttacks('01094', '01002')"],
       {"degats_identite": 0, "hors_jeu": ["01002"]}, main_exclusive=["01090"], passer_sur_option="Defense"),
    _c("rl017 Devour : valeurs imprimees SYMBIOTE",
       "nombres texte <-> code (scan)", [HEROS], ["Puzzle.Reveal('rl017')"], {"defausse_rencontre": ["rl017"]}, main_exclusive=["01090"], accepter_choix=True),
]


VERIFICATIONS = r'''
def rl_qui_choisit(monde, aides):
    """RR First Player : qui est interroge par `AskChooseFace` quand Devour (revelee par le joueur 2) doit defausser UN de ses allies ?
    Le choix est intercepte (le premier allie est pris) et la revelation est jouee ICI, sous interception. Cle `attendu` : `choisit` =
    indice du joueur interroge."""
    from game.puzzle import RunPuzzle
    attendu = aides["cas"]["attendu"]
    interroges = []
    classe = type(monde.players[0])
    origine = classe.__dict__.get("AskChooseFace")

    def intercepte(self, faces, by_effect, **kwargs):
        interroges.append(self.player_id)
        return faces[0] if faces else None

    classe.AskChooseFace = intercepte
    try:
        RunPuzzle(monde).Reveal('rl017', by='01001b')
    finally:
        if origine is None:
            del classe.AskChooseFace
        else:
            classe.AskChooseFace = origine
    if interroges != [attendu["choisit"]]:
        return False, f"joueur(s) interroge(s) : {interroges}, attendu [{attendu['choisit']}]"
    return True, f"le joueur {interroges[0]} choisit l'allie a defausser"


def rl_etat(monde, aides):
    """Cles propres : `rl_stats` ({attribut: valeur} de l'identite), `rl_engage` ([[card_id, bool]] : le sbire est engage avec le joueur),
    `rl_deck_rencontre` (taille exacte du deck rencontre), `rl_main` (card_id presents en main), `rl_traits_main` ([[card_id, [traits]]]),
    `rl_retirees` (zone retiree du jeu), `rl_soigne` (bool : l'identite a ete soignee, degats < degats poses avant + attaque) ; le reste
    va a etat_attendu."""
    from game.operate.worlds import Worlds
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    joueur = monde.players[0]
    identite = aides["identite"](monde)
    ids = lambda faces: [getattr(f.paper, "card_id", None) for f in faces]
    for nom, valeur in (attendu.get("rl_stats") or {}).items():
        courant = getattr(identite, nom, None)
        if courant != valeur:
            soucis.append(f"{nom} = {courant} (attendu {valeur})")
    for card_id, voulu in attendu.get("rl_engage") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (rl_engage)")
            continue
        engage = False
        try:
            engage = face.GetEngagedPlayer() is joueur
        except Exception:
            engage = False
        if engage != voulu:
            soucis.append(f"{card_id} engage = {engage} (attendu {voulu})")
    if "rl_deck_rencontre" in attendu:
        taille = len(Worlds.GetEncounterDeckCards(monde))
        if taille != attendu["rl_deck_rencontre"]:
            soucis.append(f"deck rencontre = {taille} carte(s) (attendu {attendu['rl_deck_rencontre']})")
    main = ids(joueur.hand_cards.Get())
    for c in attendu.get("rl_main") or []:
        if c not in main:
            soucis.append(f"{c} absente de la main {sorted(main)}")
    cartes_main = {getattr(f.paper, "card_id", None): f for f in joueur.hand_cards.Get()}
    for card_id, traits in attendu.get("rl_traits_main") or []:
        face = cartes_main.get(card_id)
        if face is None:
            soucis.append(f"{card_id} absente de la main (rl_traits_main)")
            continue
        for t in ("ATTACK", "THWART", "SKILL", "TECH", "WEAPON"):
            if face.HasTrait(t) != (t in traits):
                soucis.append(f"{card_id} : trait {t} {'present' if face.HasTrait(t) else 'absent'} (attendu {traits})")
    retirees = ids(monde.area_removed.Get(True))
    for c in attendu.get("rl_retirees") or []:
        if c not in retirees:
            soucis.append(f"{c} pas retiree du jeu (retirees = {retirees})")
    if "rl_soigne" in attendu:
        # Rhino (ATQ 2) non defendu : sans soin 2 degats de plus ; avec soin 1 de moins. Mesure : degats de l'identite apres l'attaque.
        # Cas sous 5 degats : 1 pose + 2 = 3 ; cas a 5 : 5 - 1 + 2 = 6 (et 7 sans le soin).
        degats = identite.sustained
        if attendu["rl_soigne"] and degats == 7:
            soucis.append(f"degats identite = {degats} : pas de soin (attendu 6)")
        if not attendu["rl_soigne"] and degats != 3:
            soucis.append(f"degats identite = {degats} (attendu 3 : 1 pose + 2 de Rhino, aucun soin)")
    if "rl_en_jeu_parmi" in attendu:
        ids_groupe, voulu = attendu["rl_en_jeu_parmi"]
        presentes = [i for i in ids_groupe if aides["par_id"](monde, i) is not None]
        if len(presentes) != voulu:
            soucis.append(f"{len(presentes)} carte(s) en jeu parmi {ids_groupe} (attendu {voulu}) : {presentes}")
    propres = ("rl_stats", "rl_engage", "rl_deck_rencontre", "rl_main", "rl_traits_main", "rl_retirees", "rl_soigne", "rl_en_jeu_parmi")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        try:
            vus = []
            for objet in monde.object_manager.card_dict.values():
                face = getattr(objet, "face", None) or objet
                if getattr(face, "IsInPlay", None) and face.IsInPlay():
                    vus.append(f"{getattr(face.paper, 'card_id', '?')}({getattr(face, 'sustained', '')})")
            soucis.append("[en jeu : " + " ".join(vus) + "]")
        except Exception as e:
            soucis.append(f"[dump impossible : {e}]")
        return False, " ; ".join(soucis)
    return True, message
'''
