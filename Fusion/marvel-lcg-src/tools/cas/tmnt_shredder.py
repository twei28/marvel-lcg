# Cas test_capacites du scenario SHREDDER (pack `shredder`, prefixe `ts`) : prefixe « [shredder] ».
# Fichier de preuves de .planning/tmnt/shredder-gabarits.md (une section par carte).
#
# Conventions :
#  - heros de test : Spider-Man (01001) en forme HEROS (`HEROS`) ; scenario `shredder` (Shredder I,
#    complot 1A/1B, deck Shredder, Chunin + Foot Goon Squad en modulaires, TMNT Standard) ou
#    `shredder_expert` (Shredder II/III).
#  - la mise en place REVELE un sbire FOOT CLAN au hasard (1A) et pose un Cloaked sur Shredder (1B) :
#    `MENAGE` retire TOUS les sbires du pack, `SANS_CLOAK` retire le Cloaked initial de Shredder I.
#  - `main_exclusive: ["01088"]` : main videe + une Energy, pour qu'aucune carte du heros ne reponde.
#  - le pilote ne defend pas : heros incline (`INCLINE`) quand un ennemi frappe.
MENAGE = "Puzzle.RemoveMinionsInPlay()"
VIDE = "Puzzle.EmptyEncounterDeck()"
SANS_CLOAK = "Puzzle.Cloak('ts001')"          # Shredder I demarre avec 1 Cloaked (1B) : le retire
HEROS = "Puzzle.ChangeForm('01001b')"
INCLINE = "Puzzle.Exhaust('01001a')"
SC = "shredder"
SCE = "shredder_expert"
BASE = [MENAGE, VIDE, "Puzzle.EmptyEncounterDiscardPile()"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[shredder] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "shredder_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ===================================================================== mise en place
    _c("ts004a Setup (solo) : le joueur cherche un sbire FOOT CLAN et le revele, engage avec lui",
       "« Each player searches the encounter deck for a FOOT CLAN minion and reveals it »",
       [], [], {"engages": [[0, 1]], "engage_foot_clan": [0]}),
    _c("ts004a Setup (2 joueurs) : CHAQUE joueur cherche et revele un sbire FOOT CLAN",
       "« Each player » : 2 joueurs = 2 sbires, un engage avec chacun",
       [], [], {"engages": [[0, 1], [1, 1]], "engage_foot_clan": [0, 1]}, heros2="black_widow"),
    _c("ts004b When Revealed : Shredder recoit un Cloaked a la mise en place",
       "« Cloak Shredder » : 1B est revele a la mise en place, Shredder I porte 1 Cloaked",
       [], [], {"cloaked": [["ts001", 1]], "en_jeu": ["ts004b"]}),
    # ===================================================================== ts001-ts003
    _c("ts001 plafond : Shredder I porte AU PLUS 2 cartes Cloaked (la 3e est refusee)",
       "« Shredder can have up to 2 cloaked status cards » : 3 poses, 2 gardees",
       BASE + [SANS_CLOAK], ["Puzzle.AddCloak('ts001', 3)"], {"cloaked": [["ts001", 2]]}),
    _c("ts001 TEMOIN : un personnage ordinaire (le heros) ne porte qu'UNE carte Cloaked",
       "encart du scenario : « Normally characters can only have one Cloaked status card on them at a time »",
       BASE + [HEROS], ["Puzzle.AddCloak('01001a', 3)"], {"cloaked": [["01001a", 1]]}),
    _c("ts001 Forced Response : apres la phase du mechant, Shredder recoit UN Cloaked",
       "« After the villain phase ends, give Shredder a cloaked status card »",
       BASE + [SANS_CLOAK], ["Puzzle.EndVillainPhase()"], {"cloaked": [["ts001", 1]]}),
    _c("ts001 Forced Response au maximum : Shredder I a deja 2 Cloaked, la 3e n'est pas posee",
       "plafond atteint : « give Shredder a cloaked status card » ne depasse pas 2",
       BASE + [SANS_CLOAK, "Puzzle.AddCloak('ts001', 2)"], ["Puzzle.EndVillainPhase()"],
       {"cloaked": [["ts001", 2]]}),
    _c("ts002 plafond : Shredder II porte AU PLUS 3 cartes Cloaked",
       "« Shredder can have up to 3 cloaked status cards »",
       BASE + ["Puzzle.Remove('ts006')"], ["Puzzle.AddCloak('ts002', 5)"], {"cloaked": [["ts002", 3]]},
       scenario=SCE),
    # Encart « Shredder Cloaked Rules » (FAQ chiffree de l'auteur), ajoute le 16/10/2026.
    _c("ts002 encart : Shredder II active avec 3 Cloaked -> TOUS resolvent sur cette activation (base mesuree 3 + 6 = 9)",
       "« All Cloaked status cards will resolve on that single activation. This would mean that he activates with a bonus of +6 »",
       BASE + [HEROS, INCLINE, "Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.AddCloak('ts002', 3)", "Puzzle.Attack('ts002')"],
       {"degats_identite": 9, "cloaked": [["ts002", 0]]}, scenario=SCE, main_exclusive=["01088"]),
    _c("ts002 encart, TEMOIN : meme montage SANS Cloaked -> ligne de base de l'attaque de Shredder II",
       "contre-cas du +6 : sans carte Cloaked l'attaque vaut 3 dans ce montage (ATQ 2 + 1 du boost / expert)",
       BASE + [HEROS, INCLINE, "Puzzle.CreateEncounterDeck('01105')", "Puzzle.Cloak('ts002')"], ["Puzzle.Attack('ts002')"],
       {"degats_identite": 3, "cloaked": [["ts002", 0]]}, scenario=SCE, main_exclusive=["01088"]),
    _c("ts002 encart : 3 Cloaked et UNE attaque de 3 degats -> 2 Cloaked retires, le dernier RESTE, aucun degat",
       "« The 3 damage is a single attack, it removes 2 Cloaked status cards [...] the last Cloaked status card remains »",
       BASE, ["Puzzle.AddCloak('ts002', 3)", "Puzzle.Damage('ts002', 3)"],
       {"degats": [["ts002", 0]], "cloaked": [["ts002", 1]]}, scenario=SCE),
    _c("ts002 encart : 3 Cloaked et TROIS attaques de 1 degat -> chacune retire un Cloaked, tous partis",
       "« Attacks are resolved independently. Each attack will remove one status card, resulting in all Cloaked status cards being removed »",
       BASE, ["Puzzle.AddCloak('ts002', 3)", "Puzzle.Damage('ts002', 1)", "Puzzle.Damage('ts002', 1)", "Puzzle.Damage('ts002', 1)"],
       {"degats": [["ts002", 0]], "cloaked": [["ts002", 0]]}, scenario=SCE),
    _c("ts002 Forced Response : apres la phase du mechant, Shredder II recoit UN Cloaked (pas deux)",
       "« give Shredder a cloaked status card » : une seule carte au stade II",
       BASE + ["Puzzle.Remove('ts006')", "Puzzle.AddCloak('ts002', 5)", "Puzzle.Cloak('ts002')",
               "Puzzle.Cloak('ts002')", "Puzzle.Cloak('ts002')"],
       ["Puzzle.EndVillainPhase()"], {"cloaked": [["ts002", 1]]}, scenario=SCE),
    _c("ts002 When Revealed (mise en place expert) : Bladed Armor est cherchee et s'attache a Shredder II",
       "« Search the encounter deck and discard pile for the Bladed Armor attachment and reveal it »",
       [], [], {"en_jeu": ["ts002", "ts006"], "accroche_a": [["ts006", "ts002"]]}, scenario=SCE),
    _c("ts002 When Revealed (passage au stade II, mode normal) : Bladed Armor vient du deck et s'attache",
       "Shredder I est vaincu : Shredder II est revele, il cherche ts006 dans le deck (ici posee au sommet)",
       BASE + ["Puzzle.CreateEncounterDeck('ts008', 'ts006')"], ["Puzzle.AdvanceVillain()"],
       {"en_jeu": ["ts002", "ts006"], "accroche_a": [["ts006", "ts002"]]}),
    _c("ts002 When Revealed : Bladed Armor est AUSSI cherchee dans la DEFAUSSE de rencontre",
       "« Search the encounter deck and discard pile »",
       BASE + ["Puzzle.CreateEncounterDiscardPile('ts006')"], ["Puzzle.AdvanceVillain()"],
       {"en_jeu": ["ts006"], "accroche_a": [["ts006", "ts002"]]}),
    _c("ts003 plafond : Shredder III porte AU PLUS 4 cartes Cloaked",
       "« Shredder can have up to 4 cloaked status cards »",
       BASE + ["Puzzle.Remove('ts006', 'ts007')"], ["Puzzle.AdvanceVillain()", "Puzzle.AddCloak('ts003', 6)"],
       {"cloaked": [["ts003", 4]]}, scenario=SCE),
    _c("ts003 Forced Response : apres la phase du mechant, Shredder III recoit DEUX Cloaked",
       "« give Shredder 2 cloaked status cards »",
       BASE + ["Puzzle.Remove('ts006', 'ts007')"],
       ["Puzzle.AdvanceVillain()", "Puzzle.Cloak('ts003')", "Puzzle.EndVillainPhase()"],
       {"cloaked": [["ts003", 2]]}, scenario=SCE),
    _c("ts003 Forced Response (un seul emplacement libre) : Shredder III a 3 Cloaked, il n'en recoit qu'UN",
       "« 2 cloaked status cards » mais plafond 4 : la 2e est refusee",
       BASE + ["Puzzle.Remove('ts006', 'ts007')"],
       ["Puzzle.AdvanceVillain()", "Puzzle.AddCloak('ts003', 3)", "Puzzle.EndVillainPhase()"],
       {"cloaked": [["ts003", 4]]}, scenario=SCE),
    _c("ts003 When Revealed : Kuro Kabuto est cherche et s'attache a Shredder III",
       "« Search the encounter deck and discard pile for the Kuro Kabuto attachment and reveal it »",
       BASE + ["Puzzle.Remove('ts006')", "Puzzle.CreateEncounterDeck('ts008', 'ts007')"],
       ["Puzzle.AdvanceVillain()"],
       {"en_jeu": ["ts003", "ts007"], "accroche_a": [["ts007", "ts003"]]}, scenario=SCE),

    # ===================================================================== ts004b : Reponse forcee
    _c("ts004b Forced Response : un sbire FOOT CLAN vaincu -> 1 menace sur 1B",
       "« After a FOOT CLAN minion is defeated, place 1 threat on this scheme »",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts303')", "Puzzle.SetThreat('ts004b', 0)"],
       ["Puzzle.Damage('ts303', 1)"], {"hors_jeu": ["ts303"], "menace": [["ts004b", 1]]}),
    _c("ts004b Forced Response, TEMOIN : un sbire SANS le trait FOOT CLAN vaincu -> aucune menace",
       "Hydra Mercenary (HYDRA) n'est pas FOOT CLAN",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('01101')", "Puzzle.SetThreat('ts004b', 0)"],
       ["Puzzle.Damage('01101', 3)"], {"hors_jeu": ["01101"], "menace": [["ts004b", 0]]}),
    # ===================================================================== ts005a / ts005b
    _c("ts005a When Revealed (solo) : defausse 4 cartes du deck puis revele le sbire FOOT CLAN le plus haut de la defausse",
       "« discards 4 cards from the top of the encounter deck and reveals the topmost FOOT CLAN minion in the encounter discard pile »",
       BASE + ["Puzzle.CreateEncounterDeck('ts305', 'ts305', 'ts305', 'ts305', 'ts305')",
               "Puzzle.CreateEncounterDiscardPile('ts303')"],
       ["Puzzle.AdvanceMainScheme(1)"],
       {"en_jeu": ["ts303"], "defausse_ids": ["ts305", "ts305", "ts305", "ts305"], "engages": [[0, 1]]}),
    _c("ts005a When Revealed (2 joueurs) : CHAQUE joueur defausse 4 puis revele un sbire FOOT CLAN",
       "« In player order, each player » : 8 cartes defaussees, deux sbires reveles (un par joueur)",
       BASE + ["Puzzle.CreateEncounterDeck(" + ", ".join(["'ts305'"] * 9) + ")",
               "Puzzle.CreateEncounterDiscardPile('ts303', 'ts301')"],
       ["Puzzle.AdvanceMainScheme(1)"],
       {"en_jeu": ["ts303", "ts301"], "engages": [[0, 1], [1, 1]],
        "defausse_ids": ["ts305"] * 8}, heros2="black_widow"),
    _c("ts005a When Revealed, TEMOIN : aucun sbire FOOT CLAN dans la defausse -> rien n'est revele",
       "Hydra Mercenary en defausse n'est pas FOOT CLAN",
       BASE + ["Puzzle.CreateEncounterDeck('ts305', 'ts305', 'ts305', 'ts305', 'ts305')",
               "Puzzle.CreateEncounterDiscardPile('01101')"],
       ["Puzzle.AdvanceMainScheme(1)"], {"hors_jeu": ["01101"], "engages": [[0, 0]]}),
    _c("ts005b When Revealed : chaque ennemi (le vilain ET les sbires) recoit une carte Coriace",
       "« Give each enemy a tough status card »",
       BASE + ["Puzzle.PutIntoPlay('ts012')", "Puzzle.PutIntoPlay('ts303')"],
       ["Puzzle.AdvanceMainScheme(1)"],
       {"tough": [["ts001", 1], ["ts012", 1], ["ts303", 1]], "en_jeu": ["ts005b"]}),
    _c("ts005b Forced Response : apres que Shredder manigance -> UN Cloaked sur Shredder",
       "« After Shredder schemes, give Shredder a cloaked status card »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('01105')", "Puzzle.AdvanceMainScheme(1)"],
       ["Puzzle.Scheme('ts001')"], {"cloaked": [["ts001", 1]]}, main_exclusive=["01088"]),
    _c("ts005b Forced Response, TEMOIN : un SBIRE qui manigance ne donne pas de Cloaked a Shredder",
       "« After SHREDDER schemes » : Mongo manigance, Shredder reste sans Cloaked",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('01105')", "Puzzle.AdvanceMainScheme(1)",
               "Puzzle.PutIntoPlay('ts012')"],
       ["Puzzle.Scheme('ts012')"], {"cloaked": [["ts001", 0]]}, main_exclusive=["01088"]),
    # ===================================================================== ts006 Bladed Armor
    _c("ts006 Retaliate 1 : le heros qui attaque Shredder subit 1 degat",
       "« Shredder gains Retaliate 1 »",
       BASE + [SANS_CLOAK, HEROS, "Puzzle.PutIntoPlay('ts006')"], ["Puzzle.Attack('01001a')"],
       {"degats_identite": 1, "degats": [["ts001", 2]]}, cibles=["ts001"], main_exclusive=["01088"]),
    _c("ts006 Retaliate, TEMOIN : sans Bladed Armor, le heros n'encaisse aucune riposte",
       "contre-cas : Shredder I n'a pas Retaliate de lui-meme",
       BASE + [SANS_CLOAK, HEROS], ["Puzzle.Attack('01001a')"],
       {"degats_identite": 0, "degats": [["ts001", 2]]}, cibles=["ts001"], main_exclusive=["01088"]),
    _c("ts006 ATQ +1 : Shredder frappe a 3 (ATQ 2 + 1)",
       "`ATK+ 1` natif d'un attachement a l'ennemi ; heros incline, deck rencontre sans boost",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.CreateEncounterDeck('01105')", "Puzzle.PutIntoPlay('ts006')"],
       ["Puzzle.Attack('ts001')"], {"degats_identite": 3}, main_exclusive=["01088"]),
    _c("ts006 ATQ +1, TEMOIN : sans Bladed Armor Shredder frappe a 2",
       "contre-cas", BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.CreateEncounterDeck('01105')"],
       ["Puzzle.Attack('ts001')"], {"degats_identite": 2}, main_exclusive=["01088"]),
    _c("ts006 Action de heros OFFERTE quand Shredder n'a AUCUN Cloaked",
       "« If there are no cloaked status cards on Shredder »",
       BASE + [SANS_CLOAK, HEROS, "Puzzle.PutIntoPlay('ts006')"], [], {"action_offerte": [["ts006", 1]]},
       main_exclusive=["01088"]),
    _c("ts006 Action de heros NON OFFERTE tant que Shredder porte un Cloaked",
       "meme position, Shredder I a son Cloaked de depart (1B)",
       BASE + [HEROS, "Puzzle.PutIntoPlay('ts006')"], [], {"action_offerte": [["ts006", 0]]},
       main_exclusive=["01088"]),
    _c("ts006 Action de heros : 1 degat a l'identite + 1 ressource -> Bladed Armor est defaussee",
       "couts « take 1 damage » ET « spend 1 resource of any type », effet « discard this card »",
       BASE + [SANS_CLOAK, HEROS, "Puzzle.PutIntoPlay('ts006')"], ["Puzzle.Action('ts006', 'HeroAction', 0)"],
       {"hors_jeu": ["ts006"], "degats_identite": 1, "taille_main": 0},
       main_exclusive=["01088"], payer_avec=["01088"]),
    # ===================================================================== ts007 Kuro Kabuto
    _c("ts007 Steady : Shredder gagne steady",
       "« Shredder gains steady »", BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts007')"], [],
       {"bool_de": [["ts001", "IsSteady", True]]}),
    _c("ts007 Steady, TEMOIN : Shredder I n'est pas steady de lui-meme",
       "contre-cas", BASE + [SANS_CLOAK], [], {"bool_de": [["ts001", "IsSteady", False]]}),
    _c("ts007 Forced Response : apres la phase du mechant, Kuro Kabuto cloake Shredder EN PLUS de la Reponse du vilain",
       "« After the villain phase ends, cloak Shredder » : 1 (vilain) + 1 (Kuro Kabuto) = 2 (plafond du stade I)",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts007')"], ["Puzzle.EndVillainPhase()"],
       {"cloaked": [["ts001", 2]]}),
    _c("ts007 Forced Response, TEMOIN : sans Kuro Kabuto, la phase du mechant ne donne qu'UN Cloaked",
       "contre-cas", BASE + [SANS_CLOAK], ["Puzzle.EndVillainPhase()"], {"cloaked": [["ts001", 1]]}),
    _c("ts007 Action de heros : defausser 2 cartes de la main -> Kuro Kabuto est defaussee",
       "cout « discard 2 cards from your hand », effet « discard this card »",
       BASE + [SANS_CLOAK, HEROS, "Puzzle.PutIntoPlay('ts007')"], ["Puzzle.Action('ts007', 'HeroAction', 0)"],
       {"hors_jeu": ["ts007"], "taille_main": 1}, main_exclusive=["01088", "01089", "01090"]),
    _c("ts007 Boost : apres l'activation, Kuro Kabuto s'attache a Shredder",
       "« [star] Boost: Attach Kuro Kabuto to Shredder »",
       BASE + [SANS_CLOAK], ["Puzzle.Boost('ts007')"],
       {"en_jeu": ["ts007"], "accroche_a": [["ts007", "ts001"]]}, main_exclusive=["01088"]),
    # ===================================================================== ts008 Elite Guard
    _c("ts008 Guard + Patrol (desc) : la garde porte les deux mots-cles",
       "`desc.Guard = 1`, `desc.Patrol = 1`",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts008')"], [],
       {"bool_de": [["ts008", "IsGuard", True], ["ts008", "IsPatrol", True]]}),
    _c("ts008 When Revealed : Shredder recoit un Cloaked",
       "« Cloak Shredder »", BASE + [SANS_CLOAK], ["Puzzle.Reveal('ts008')"],
       {"cloaked": [["ts001", 1]], "en_jeu": ["ts008"]}),
    _c("ts008 Boost : Shredder recoit une carte Coriace",
       "« [star] Boost: Give Shredder a tough status card »",
       BASE + [SANS_CLOAK], ["Puzzle.Boost('ts008')"], {"tough": [["ts001", 1]]}, main_exclusive=["01088"]),
    # ===================================================================== ts010 Foot Ninja
    _c("ts010 When Revealed : Foot Ninja se cloake lui-meme",
       "« Cloak Foot Ninja »", BASE + [SANS_CLOAK], ["Puzzle.Reveal('ts010')"],
       {"cloaked": [["ts010", 1], ["ts001", 0]]}),
    _c("ts010 Forced Interrupt : vaincu, Foot Ninja est melange dans le deck de rencontre",
       "« When Foot Ninja is defeated, shuffle them into the encounter deck »",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts010')"], ["Puzzle.Damage('ts010', 1)"],
       {"hors_jeu": ["ts010"], "dans_deck_rencontre": ["ts010"]}),
    _c("ts010 Forced Interrupt : la defaite COMPTE (1B recoit sa menace : le sbire est bien vaincu)",
       "« is defeated » (et non « would be defeated... instead ») : la Reponse de 1B part",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts010')", "Puzzle.SetThreat('ts004b', 0)"],
       ["Puzzle.Damage('ts010', 1)"], {"menace": [["ts004b", 1]], "dans_deck_rencontre": ["ts010"]}),
    _c("ts010 Boost : apres l'activation, le vilain recoit un Cloaked",
       "« After this activation resolves, cloak the villain »",
       BASE + [SANS_CLOAK], ["Puzzle.Boost('ts010')"], {"cloaked": [["ts001", 1]]}, main_exclusive=["01088"]),
    # ===================================================================== ts012 Mongo
    _c("ts012 Boost (forme heros) : le heros est etourdi",
       "« [star] Boost: Stun your hero »", BASE + [SANS_CLOAK, HEROS, INCLINE], ["Puzzle.Boost('ts012')"],
       {"statuts": [["01001a", "Stunned"]]}, main_exclusive=["01088"]),
    _c("ts012 Boost (forme alter-ego) : pas de heros en jeu, rien n'est etourdi",
       "« your HERO » : en alter-ego le boost ne fait rien (modele 01123)",
       BASE + [SANS_CLOAK], ["Puzzle.Boost('ts012')"], {"statuts_absents": [["01001b", "Stunned"]]},
       main_exclusive=["01088"]),
    _c("ts012 Guard + Retaliate 1 (desc)",
       "`desc.Guard`, `desc.Retaliate`", BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts012')"], [],
       {"bool_de": [["ts012", "IsGuard", True]]}),
    # ===================================================================== ts013 Cloak of Shadows
    _c("ts013 When Revealed : chaque ennemi est cloake (Shredder ET le sbire engage), pas de revelation si engage",
       "« Cloak each enemy. If you are not engaged with a minion, reveal... » : engage avec Hydra -> rien de la defausse",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('01101')", "Puzzle.CreateEncounterDeck('01105')",
               "Puzzle.CreateEncounterDiscardPile('ts303')"],
       ["Puzzle.Reveal('ts013')"],
       {"cloaked": [["ts001", 1], ["01101", 1]], "hors_jeu": ["ts303"]}),
    _c("ts013 When Revealed : non engage -> revele le sbire FOOT CLAN le plus haut de la defausse",
       "« If you are not engaged with a minion, reveal the topmost FOOT CLAN minion in the encounter discard pile »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('01105')", "Puzzle.CreateEncounterDiscardPile('ts303')"],
       ["Puzzle.Reveal('ts013')"],
       {"cloaked": [["ts001", 1]], "en_jeu": ["ts303"], "engages": [[0, 1]]}),
    _c("ts013 Boost : apres l'activation, Shredder recoit un Cloaked",
       "« After this activation resolves, cloak Shredder »",
       BASE + [SANS_CLOAK], ["Puzzle.Boost('ts013')"], {"cloaked": [["ts001", 1]]}, main_exclusive=["01088"]),
    # ===================================================================== ts015 Disarming Assault
    _c("ts015 When Revealed : Shredder attaque SANS boost, et l'arme du joueur est defaussee s'il y a degats",
       "« Do not give Shredder any boost cards » (ts017 reste dans le deck) ; ATQ 2, 2 degats ; « discard a WEAPON you control »",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.CreateEncounterDeck('ts017')",
               "Puzzle.PutIntoPlay('04002', under_control=True)"],
       ["Puzzle.Reveal('ts015')"],
       {"degats_identite": 2, "hors_jeu": ["04002"], "dans_deck_rencontre": ["ts017"]}, main_exclusive=["01088"]),
    _c("ts015 When Revealed, TEMOIN : l'attaque ne fait AUCUN degat (Coriace) -> l'arme est gardee",
       "« If this attack deals damage to you » : Coriace absorbe tout",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.Tough('01001a')", "Puzzle.CreateEncounterDeck('ts017')",
               "Puzzle.PutIntoPlay('04002', under_control=True)"],
       ["Puzzle.Reveal('ts015')"],
       {"degats_identite": 0, "en_jeu": ["04002"]}, main_exclusive=["01088"]),
    _c("ts015 Boost : une arme du joueur est defaussee",
       "« [star] Boost: Discard a WEAPON you control »",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('04002', under_control=True)"], ["Puzzle.Boost('ts015')"],
       {"hors_jeu": ["04002"]}, main_exclusive=["01088"]),
    _c("ts015 Boost, TEMOIN : un allie sans le trait WEAPON n'est PAS defausse",
       "« a WEAPON » : Maria Hill reste en jeu",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('01067', under_control=True)"], ["Puzzle.Boost('ts015')"],
       {"en_jeu": ["01067"]}, main_exclusive=["01088"]),
    # ===================================================================== ts017 Shred
    _c("ts017 When Revealed (alter-ego) : Shredder recoit un Cloaked, sans attaque",
       "« Place a cloaked status card on Shredder »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('ts013')"], ["Puzzle.Reveal('ts017')"],
       {"cloaked": [["ts001", 1]], "degats_identite": 0}),
    _c("ts017 When Revealed (heros) : Shredder attaque SANS boost, aucun Cloaked pose",
       "« Shredder attacks you. Do not give Shredder any boost cards » : 2 degats, le deck est intact",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.CreateEncounterDeck('ts013')"], ["Puzzle.Reveal('ts017')"],
       {"degats_identite": 2, "cloaked": [["ts001", 0]], "dans_deck_rencontre": ["ts013"]}),
    _c("ts017 Boost : apres l'activation, Shredder recoit un Cloaked",
       "« After this activation resolves, cloak Shredder »",
       BASE + [SANS_CLOAK], ["Puzzle.Boost('ts017')"], {"cloaked": [["ts001", 1]]}, main_exclusive=["01088"]),
    # ===================================================================== ts020 Foot Rikugun
    _c("ts020 Forced Response : un sbire FOOT CLAN qui entre en jeu est cloake",
       "« After a FOOT CLAN minion enters play, cloak it » (Mongo n'a pas de When Revealed)",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts020')"], ["Puzzle.PutIntoPlay('ts012')"],
       {"cloaked": [["ts012", 1]], "tough": [["ts012", 0]]}),
    _c("ts020 Forced Response (DEUX Rikugun) : le 2e ne peut pas cloaker, il donne une carte Coriace",
       "« If you cannot, give it a tough status card » : un seul Cloaked par personnage",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay(Puzzle.CreateCard('ts020'))",
               "Puzzle.PutIntoPlay(Puzzle.CreateCard('ts020'))"], ["Puzzle.PutIntoPlay('ts012')"],
       {"cloaked": [["ts012", 1]], "tough": [["ts012", 1]]}),
    _c("ts020 Forced Response, TEMOIN : un sbire SANS le trait FOOT CLAN n'est pas cloake",
       "Hydra Mercenary", BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts020')"], ["Puzzle.PutIntoPlay('01101')"],
       {"cloaked": [["01101", 0]], "tough": [["01101", 0]]}),
    # ===================================================================== ts022 Throne of the Jonin
    _c("ts022 When Revealed : cherche un attachement FOOT CLAN dans le deck et le revele (Bladed Armor)",
       "« Search the encounter deck and discard pile for a FOOT CLAN attachment and reveal it »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('ts006')"], ["Puzzle.Reveal('ts022')"],
       {"en_jeu": ["ts006"], "accroche_a": [["ts006", "ts001"]], "menace": [["ts022", 1]]}),
    _c("ts022 When Revealed : cherche AUSSI dans la defausse",
       "« deck and discard pile »", BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDiscardPile('ts007')"],
       ["Puzzle.Reveal('ts022')"], {"en_jeu": ["ts007"], "menace": [["ts022", 1]]}),
    _c("ts022 If you cannot : aucun attachement FOOT CLAN -> 2[per_hero] menaces en plus (1 + 2 = 3, solo)",
       "un attachement NON FOOT CLAN (Enhanced Ivory Horn) n'est pas pris",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('01100')"], ["Puzzle.Reveal('ts022')"],
       {"menace": [["ts022", 3]], "hors_jeu": ["01100"]}),
    _c("ts022 If you cannot (2 joueurs) : 2 par joueur = 4 en plus de la menace de depart (2) = 6",
       "« 2[per_hero] threat » : 2 x 2 joueurs",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('01100')"], ["Puzzle.Reveal('ts022')"],
       {"menace": [["ts022", 6]]}, heros2="black_widow"),
    # ===================================================================== CHUNIN : ts101 Karai
    _c("ts101 When Revealed : Karai se cloake elle-meme",
       "« Cloak Karai » (pas le vilain)", BASE + [SANS_CLOAK], ["Puzzle.Reveal('ts101')"],
       {"cloaked": [["ts101", 1], ["ts001", 0]]}),
    _c("ts101 When Defeated : le VILAIN recoit un Cloaked",
       "« When Defeated: Cloak the villain »",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts101')"], ["Puzzle.Damage('ts101', 2)"],
       {"hors_jeu": ["ts101"], "cloaked": [["ts001", 1]]}),
    _c("ts101 Boost : Karai est donnee face cachee au PREMIER joueur",
       "« Deal this card to the first player as a facedown encounter card »",
       BASE + [SANS_CLOAK], ["Puzzle.Boost('ts101')"], {"distribuees": [[0, ["ts101"]]]}, main_exclusive=["01088"]),
    _c("ts101 Boost puis revelation : Karai donnee, revelee dans le meme round, entre en jeu cloakee (pas de boucle)",
       "le detournement du boost est a usage UNIQUE (defaut Skulk te006 trouve en autoplay)",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('01105')"],
       ["Puzzle.Boost('ts101')", "Puzzle.RevealDealtCards()"],
       {"en_jeu": ["ts101"], "cloaked": [["ts101", 1]], "distribuees": [[0, []]]}, main_exclusive=["01088"]),
    # ===================================================================== ts102 Ocho
    _c("ts102 Guard (desc) + attaques PERCANTES : Ocho blesse un heros Coriace et lui retire sa carte Coriace",
       "« [star] Ocho's attacks gain piercing » : ATQ 2, Coriace defaussee ET 2 degats",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.Tough('01001a')", "Puzzle.PutIntoPlay('ts102')"],
       ["Puzzle.Attack('ts102')"],
       {"degats_identite": 2, "statuts_absents": [["01001a", "Tough"]], "bool_de": [["ts102", "IsGuard", True]]},
       main_exclusive=["01088"]),
    _c("ts102 TEMOIN : un sbire sans piercing (Hydra, ATQ 1) est absorbe par la carte Coriace",
       "contre-cas : Coriace defaussee, 0 degat",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.Tough('01001a')", "Puzzle.PutIntoPlay('01101')"],
       ["Puzzle.Attack('01101')"], {"degats_identite": 0, "statuts_absents": [["01001a", "Tough"]]},
       main_exclusive=["01088"]),
    _c("ts102 Boost : cherche Karai dans le deck et la revele",
       "« Search the encounter deck and discard pile for Karai and reveal her »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('ts101')"], ["Puzzle.Boost('ts102')"],
       {"en_jeu": ["ts101"]}, main_exclusive=["01088"]),
    _c("ts102 Boost : Karai-NEMESIS de Leonardo (tl015) est AUSSI Karai : trouvee par son card_id",
       "homonyme : `IDS_KARAI` = ts101 + tl015",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('tl015')"], ["Puzzle.Boost('ts102')"],
       {"en_jeu": ["tl015"]}, main_exclusive=["01088"]),
    # ===================================================================== ts103 Kira no Ken
    _c("ts103 Karai en jeu : Kira no Ken s'attache a elle",
       "« Attach to Karai »", BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts101')"], ["Puzzle.PutIntoPlay('ts103')"],
       {"accroche_a": [["ts103", "ts101"]]}),
    _c("ts103 Karai absente : elle est cherchee dans le deck, revelee, puis Kira no Ken s'attache a elle",
       "« If Karai is not in play, search ... and reveal her. Then, attach this card to her »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('ts101')"], ["Puzzle.PutIntoPlay('ts103')"],
       {"en_jeu": ["ts101", "ts103"], "accroche_a": [["ts103", "ts101"]]}),
    _c("ts103 Karai introuvable : Kira no Ken est defaussee",
       "aucune Karai dans le deck ni la defausse : l'attachement n'a nulle part ou aller",
       BASE + [SANS_CLOAK], ["Puzzle.PutIntoPlay('ts103')"], {"hors_jeu": ["ts103"]}),
    _c("ts103 ATQ +1 et attaques PERCANTES : Karai ATQ 1 +1 perce la Coriace du heros (2 degats)",
       "« [star] Attached minion's attacks gain piercing » ; `ATK+ 1`",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.Tough('01001a')", "Puzzle.PutIntoPlay('ts101')",
               "Puzzle.PutIntoPlay('ts103')"], ["Puzzle.Attack('ts101')"],
       {"degats_identite": 2, "statuts_absents": [["01001a", "Tough"]]}, main_exclusive=["01088"]),
    _c("ts103 TEMOIN : Karai SANS Kira no Ken (ATQ 1) est absorbee par la Coriace",
       "contre-cas", BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.Tough('01001a')", "Puzzle.PutIntoPlay('ts101')"],
       ["Puzzle.Attack('ts101')"], {"degats_identite": 0}, main_exclusive=["01088"]),
    # ===================================================================== ts104 Doroppuin
    _c("ts104 When Revealed : revele le sbire le plus haut de la defausse (n'importe quel sbire)",
       "« Reveal the topmost minion in the encounter discard pile »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDiscardPile('01101')"], ["Puzzle.Reveal('ts104')"],
       {"en_jeu": ["01101"]}),
    _c("ts104 Otherwise : defausse sans sbire -> la carte gagne surge (la carte suivante est revelee)",
       "« Otherwise, this gains surge »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"], ["Puzzle.Reveal('ts104')"],
       {"taille_deck_rencontre": 2}),
    _c("ts104 Boost (attaque) : l'attaque gagne PIERCING -> Coriace retiree, degats subis",
       "« If this activation is an attack, it gains piercing » : Shredder ATQ 2 + 1 icone de boost = 3 contre un heros Coriace",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.Tough('01001a')"], ["Puzzle.Boost('ts104')"],
       {"degats_identite": 3, "statuts_absents": [["01001a", "Tough"]]}, main_exclusive=["01088"]),
    _c("ts104 Boost, TEMOIN : sans piercing (boost Elite Guard), la Coriace absorbe tout",
       "contre-cas", BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.Tough('01001a')"], ["Puzzle.Boost('ts008')"],
       {"degats_identite": 0, "statuts_absents": [["01001a", "Tough"]]}, main_exclusive=["01088"]),
    # ===================================================================== FOOT GOON SQUAD
    _c("ts201 Bebop : Toughness (desc) et attaques PERCANTES (Coriace du heros percee)",
       "« Toughness. [star] Bebop's attacks gain piercing »",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.Tough('01001a')", "Puzzle.PutIntoPlay('ts201')"],
       ["Puzzle.Attack('ts201')"],
       {"degats_identite": 2, "statuts_absents": [["01001a", "Tough"]], "tough": [["ts201", 1]]},
       main_exclusive=["01088"]),
    _c("ts201 Boost (attaque) : l'attaque de Shredder gagne piercing",
       "« If this activation is an attack, it gains piercing » (Bebop n'a que l'etoile : ATQ 2)",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.Tough('01001a')"], ["Puzzle.Boost('ts201')"],
       {"degats_identite": 2, "statuts_absents": [["01001a", "Tough"]]}, main_exclusive=["01088"]),
    _c("ts201 Boost (manigance, alter-ego) : Bebop est donne face cachee au premier joueur",
       "« Otherwise, deal this card to the first player as a facedown encounter card »",
       BASE + [SANS_CLOAK], ["Puzzle.Boost('ts201')"], {"distribuees": [[0, ["ts201"]]]}, main_exclusive=["01088"]),
    _c("ts201 Boost (attaque), TEMOIN : en attaque Bebop n'est PAS distribue",
       "branche « attaque » seulement",
       BASE + [SANS_CLOAK, HEROS, INCLINE], ["Puzzle.Boost('ts201')"], {"distribuees": [[0, []]]},
       main_exclusive=["01088"]),
    _c("ts205 Rocksteady : attaque a overkill -> l'excedent frappe le heros (Maria Hill HP 2 - 1 degat, ATQ 2 : 1 en trop)",
       "« [star] Rocksteady's attacks gain overkill » ; Rocksteady entre en jeu en alter-ego (Quickstrike ne joue pas), puis forme heros",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('01067', under_control=True)", "Puzzle.Damage('01067', 1)",
               "Puzzle.PutIntoPlay('ts205')", HEROS, INCLINE],
       ["Puzzle.Attack('ts205', defender='01067')"], {"degats_identite": 1, "hors_jeu": ["01067"]},
       main_exclusive=["01088"]),
    _c("ts205 TEMOIN : Mongo (ATQ 2, sans overkill) tue Maria Hill sans excedent sur le heros",
       "contre-cas", BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('01067', under_control=True)", "Puzzle.Damage('01067', 1)",
                              "Puzzle.PutIntoPlay('ts012')", HEROS, INCLINE],
       ["Puzzle.Attack('ts012', defender='01067')"], {"degats_identite": 0, "hors_jeu": ["01067"]},
       main_exclusive=["01088"]),
    _c("ts205 Boost (attaque) : l'attaque de Shredder gagne overkill (ATQ 2 + 1 icone = 3 contre Maria Hill HP 2)",
       "« If this activation is an attack, it gains overkill » ; boost tire du deck pendant l'attaque",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.PutIntoPlay('01067', under_control=True)",
               "Puzzle.CreateEncounterDeck('ts205')"],
       ["Puzzle.Attack('ts001', defender='01067')"], {"degats_identite": 1, "hors_jeu": ["01067"]},
       main_exclusive=["01088"]),
    _c("ts205 Boost (attaque), TEMOIN : meme position avec un boost sans overkill (Foot Soldiers) : pas d'exces",
       "contre-cas", BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.PutIntoPlay('01067', under_control=True)",
                              "Puzzle.CreateEncounterDeck('ts303')"],
       ["Puzzle.Attack('ts001', defender='01067')"], {"degats_identite": 0, "hors_jeu": ["01067"]},
       main_exclusive=["01088"]),
    _c("ts205 Boost (manigance) : Rocksteady est donne face cachee au premier joueur",
       "« Otherwise, deal this card to the first player »",
       BASE + [SANS_CLOAK], ["Puzzle.Boost('ts205')"], {"distribuees": [[0, ["ts205"]]]}, main_exclusive=["01088"]),
    _c("ts202 Bludgeon : apres avoir attaque ET blesse un personnage, il l'epuise",
       "« After Bludgeon attacks and damages a character, exhaust that character »",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts202')", HEROS], ["Puzzle.Attack('ts202')"],
       {"exhausted": ["01001a"], "degats_identite": 2}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("ts202 Bludgeon, TEMOIN : attaque absorbee par la Coriace -> le heros n'est PAS epuise",
       "« attacks AND damages » : aucun degat, aucune fatigue",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts202')", HEROS, "Puzzle.Tough('01001a')"],
       ["Puzzle.Attack('ts202')"], {"pret": ["01001a"], "degats_identite": 0}, main_exclusive=["01088"],
       passer_sur_option="Defense"),
    _c("ts202 Boost : le heros est epuise",
       "« [star] Boost: Exhaust your hero »", BASE + [SANS_CLOAK, HEROS], ["Puzzle.Boost('ts202')"],
       {"exhausted": ["01001a"]}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("ts203 Hun : apres avoir attaque ET blesse un personnage, il l'etourdit",
       "« After Hun attacks and damages a character, stun that character »",
       BASE + [SANS_CLOAK, HEROS, "Puzzle.PutIntoPlay('ts203')"], ["Puzzle.Attack('ts203')"],
       {"statuts": [["01001a", "Stunned"]], "degats_identite": 2}, main_exclusive=["01088"],
       passer_sur_option="Defense"),
    _c("ts203 Hun, TEMOIN : attaque absorbee par la Coriace -> pas d'etourdissement",
       "aucun degat, aucun Stunned",
       BASE + [SANS_CLOAK, HEROS, "Puzzle.Tough('01001a')", "Puzzle.PutIntoPlay('ts203')"],
       ["Puzzle.Attack('ts203')"], {"statuts_absents": [["01001a", "Stunned"]]}, main_exclusive=["01088"],
       passer_sur_option="Defense"),
    _c("ts203 Boost : si l'activation (attaque) fait des degats, le personnage est etourdi",
       "« If this activation deals damage to a character, stun that character »",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.Boost('ts203')"],
       {"statuts": [["01001a", "Stunned"]], "degats_identite": 3}, main_exclusive=["01088"]),
    _c("ts203 Boost, TEMOIN : l'attaque ne fait aucun degat (Coriace) -> pas d'etourdissement",
       "« IF this activation deals damage »",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.Tough('01001a')"], ["Puzzle.Boost('ts203')"],
       {"statuts_absents": [["01001a", "Stunned"]], "degats_identite": 0}, main_exclusive=["01088"]),
    _c("ts204 Koya : When Revealed, soigne 2 degats du vilain (+ Incite 1 : 1 menace sur le complot principal)",
       "« Heal 2 damage from the villain » ; Incite 1 lu dans `desc`",
       BASE + [SANS_CLOAK, "Puzzle.Damage('ts001', 3)", "Puzzle.SetThreat('ts004b', 0)"],
       ["Puzzle.Reveal('ts204')"], {"degats": [["ts001", 1]], "menace": [["ts004b", 1]]}),
    _c("ts204 Boost : 1 menace sur le complot principal ET 2 degats soignes du vilain",
       "« Place 1 threat on the main scheme and heal 2 damage from the villain » : 1 (Incite 1, icone du boost) + 1 (texte) = 2 menaces",
       BASE + [SANS_CLOAK, "Puzzle.Damage('ts001', 3)", "Puzzle.SetThreat('ts004b', 0)"],
       ["Puzzle.Boost('ts204')"], {"degats": [["ts001", 1]], "menace": [["ts004b", 2]]}, main_exclusive=["01088"]),
    _c("ts206 When Revealed : defausse le deck jusqu'a un sbire BRUTE, qu'elle revele",
       "« Discard cards from the top of the encounter deck until a BRUTE minion is discarded. Reveal that minion »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('ts303', 'ts012', 'ts008')"], ["Puzzle.Reveal('ts206')"],
       {"en_jeu": ["ts012"], "defausse_ids": ["ts008"]}),
    # ===================================================================== SHADOW OF THE FOOT
    _c("ts301 When Revealed : Foot Assassin se cloake elle-meme",
       "« Cloak Foot Assassin »", BASE + [SANS_CLOAK], ["Puzzle.Reveal('ts301')"],
       {"cloaked": [["ts301", 1], ["ts001", 0]]}, main_exclusive=["01088"]),
    _c("ts301 Forced Response : apres avoir attaque, Foot Assassin se cloake",
       "« After Foot Assassin attacks, cloak them » : attaque a la demande, heros incline",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.PutIntoPlay('ts301')"], ["Puzzle.Attack('ts301')"],
       {"cloaked": [["ts301", 1]]}, main_exclusive=["01088"]),
    _c("ts303 When Revealed : Foot Soldiers se cloake lui-meme",
       "« Cloak Foot Soldiers »", BASE + [SANS_CLOAK], ["Puzzle.Reveal('ts303')"],
       {"cloaked": [["ts303", 1], ["ts001", 0]]}),
    _c("ts305 Foothold : menace de depart 3 (fixe) + Hinder 1[per_hero]",
       "`StartingThreat 3`, `Hinder 1*` (solo : 1 menace en plus)",
       BASE + [SANS_CLOAK], ["Puzzle.Reveal('ts305')"], {"menace": [["ts305", 4]]}),
    _c("ts305 Foothold (2 joueurs) : menace 3 + Hinder 1 par joueur (2) = 5",
       "`Hinder 1*` : multiplie par le nombre de joueurs",
       BASE + [SANS_CLOAK], ["Puzzle.Reveal('ts305')"], {"menace": [["ts305", 5]]}, heros2="black_widow"),

    # ===================================================================== encart du scenario : regles des Cloaked MULTIPLES
    _c("encart Q&R : Shredder II active avec 3 Cloaked -> ils jouent TOUS sur l'unique activation (+6 ATQ : 2 + 6 = 8 degats)",
       "« All Cloaked status cards will resolve on that single activation. He activates with a bonus of +6 »",
       BASE + ["Puzzle.Remove('ts006')", "Puzzle.CreateEncounterDeck('01105')", HEROS, INCLINE,
               "Puzzle.Cloak('ts002')", "Puzzle.AddCloak('ts002', 3)"],
       ["Puzzle.Attack('ts002')"], {"degats_identite": 8, "cloaked": [["ts002", 0]]}, scenario=SCE,
       main_exclusive=["01088"]),
    _c("encart Q&R : 3 degats d'UNE attaque contre 3 Cloaked -> 2 cartes retirees, le total est prevenu, la 3e RESTE",
       "« it removes 2 Cloaked status cards. Since that is enough damage reduction to prevent the total damage, the last Cloaked status card remains »",
       BASE + ["Puzzle.Remove('ts006')", "Puzzle.AddCloak('ts002', 3)"], ["Puzzle.Damage('ts002', 3)"],
       {"degats": [["ts002", 0]], "cloaked": [["ts002", 1]]}, scenario=SCE),
    _c("encart Q&R : 3 attaques de 1 degat contre 3 Cloaked -> chaque attaque retire UNE carte (les 3 partent)",
       "« Attacks are resolved independently. Each attack will remove one status card »",
       BASE + ["Puzzle.Remove('ts006')", "Puzzle.AddCloak('ts002', 3)"],
       ["Puzzle.Damage('ts002', 1)", "Puzzle.Damage('ts002', 1)", "Puzzle.Damage('ts002', 1)"],
       {"degats": [["ts002", 0]], "cloaked": [["ts002", 0]]}, scenario=SCE),
    _c("encart Q&R : une carte Tenace absorbe AVANT la carte Cloaked (Cloaked posee d'abord)",
       "« Tough status cards always resolve before cloaked status cards »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('01105')", HEROS, INCLINE, "Puzzle.Cloak('01001a')",
               "Puzzle.Tough('01001a')"],
       ["Puzzle.Attack('ts001')"],
       {"degats_identite": 0, "cloaked": [["01001a", 1]], "statuts_absents": [["01001a", "Tough"]]},
       main_exclusive=["01088"]),
    _c("encart Q&R : une carte Tenace absorbe AVANT la carte Cloaked (Tenace posee d'abord)",
       "meme regle, ordre de pose inverse",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('01105')", HEROS, INCLINE, "Puzzle.Tough('01001a')",
               "Puzzle.Cloak('01001a')"],
       ["Puzzle.Attack('ts001')"],
       {"degats_identite": 0, "cloaked": [["01001a", 1]], "statuts_absents": [["01001a", "Tough"]]},
       main_exclusive=["01088"]),
    _c("encart Q&R : Tenace + Cloaked et attaque PERCANTE -> la Tenace part, le Cloaked previent 2, le reste est subi",
       "« Piercing causes the Tough status card to be removed before the damage is applied. The Cloaked status card will prevent 2 of the damage, and be discarded » : ATQ 3 + 1 icone (Doroppuin) = 4, -2 = 2",
       BASE + ["Puzzle.Remove('ts006', 'ts007')", "Puzzle.CreateEncounterDeck('ts104')", HEROS, INCLINE,
               "Puzzle.Tough('01001a')", "Puzzle.Cloak('01001a')", "Puzzle.Cloak('ts002')"],
       ["Puzzle.AdvanceVillain()", "Puzzle.Attack('ts003')"],
       {"degats_identite": 2, "cloaked": [["01001a", 0]], "statuts_absents": [["01001a", "Tough"]]},
       scenario=SCE, main_exclusive=["01088"]),
    _c("encart Q&R : un heros Etourdi ET Cloaked qui attaque perd son Etourdi, le Cloaked RESTE",
       "« They attempt to attack, and instead remove the stunned status card »",
       BASE + [SANS_CLOAK, HEROS, "Puzzle.Stun('01001a')", "Puzzle.Cloak('01001a')"],
       ["Puzzle.Attack('01001a')"],
       {"statuts_absents": [["01001a", "Stunned"]], "cloaked": [["01001a", 1]], "degats": [["ts001", 0]]},
       cibles=["ts001"], main_exclusive=["01088"]),
    _c("encart Q&R : un personnage STEADY (Rocksteady) ne porte PAS 2 Cloaked",
       "« Can I put 2 Cloaked cards on a steady character? No. Steady only affects how many confused or stunned cards can be placed on them »",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts205')"], ["Puzzle.AddCloak('ts205', 2)"],
       {"cloaked": [["ts205", 1]], "bool_de": [["ts205", "IsSteady", True]]}),
    _c("encart Q&R : un personnage STEADY peut etre cloake (une carte)",
       "« Can I Cloak a steady/stalwart character? Yes »",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts205')"], ["Puzzle.AddCloak('ts205', 1)"],
       {"cloaked": [["ts205", 1]]}),
]

VERIFICATIONS = r'''
def shredder_etat(monde, aides):
    """etat_attendu (cles communes) + cles propres au scenario Shredder :
    cloaked [[id, n]] (nombre de Cloaked), tough [[id, n]], engages [[siege, n]]
    (sbires engages), engage_foot_clan [siege...] (un sbire FOOT CLAN engage),
    distribuees [[siege, [ids]]] (cartes distribuees face cachee)."""
    attendu = aides["cas"].get("attendu") or {}
    propres = {"cloaked", "tough", "engages", "engage_foot_clan", "distribuees", "defausse_ids", "bool_de",
               "action_offerte", "taille_deck_rencontre"}
    inconnues = sorted(set(attendu) - set(CLES_ETAT_ATTENDU) - propres)
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de shredder_etat : {inconnues}"
    reste = {k: v for k, v in attendu.items() if k in CLES_ETAT_ATTENDU}
    copie = dict(aides); copie["cas"] = dict(aides["cas"]); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    soucis = [] if ok else [message]
    for card_id, n in attendu.get("cloaked") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (cloaked)")
        elif face.cloaked != n:
            soucis.append(f"{card_id} porte {face.cloaked} Cloaked (attendu {n})")
    for card_id, n in attendu.get("tough") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (tough)")
        elif face.tough != n:
            soucis.append(f"{card_id} porte {face.tough} Coriace (attendu {n})")
    for siege, n in attendu.get("engages") or []:
        reel = monde.players[siege].engaged_minions.GetSize()
        if reel != n:
            soucis.append(f"joueur {siege} : {reel} sbire(s) engage(s) (attendu {n})")
    for siege in attendu.get("engage_foot_clan") or []:
        if not any(m.HasTrait("FOOT CLAN") for m in monde.players[siege].engaged_minions.GetAll()):
            soucis.append(f"joueur {siege} : aucun sbire FOOT CLAN engage")
    for siege, ids in attendu.get("distribuees") or []:
        reel = sorted(getattr(f.paper, "card_id", "?") for f in monde.players[siege].dealt_encounter_cards.GetAll())
        if reel != sorted(ids):
            soucis.append(f"joueur {siege} : cartes distribuees {reel} (attendu {sorted(ids)})")
    for card_id, methode, voulu in attendu.get("bool_de") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu ({methode})")
        elif bool(getattr(face, methode)()) != voulu:
            soucis.append(f"{card_id}.{methode}() = {getattr(face, methode)()} (attendu {voulu})")
    for card_id, n in attendu.get("action_offerte") or []:
        from game.ability.ability import AbilityType
        from game.event.manager import EventManager
        from game.message import Message
        from game.effect.rule import GameRule
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (action_offerte)")
            continue
        joueur = monde.GetCurrentPlayer()
        candidats = [x for x in face.effect.Find(when=Message.WhenPlayerInTurn, type=AbilityType.HeroAction)
                     if not x.ability.is_play]
        msg = Message.WhenPlayerLikeInTurn(joueur, GameRule(joueur.GetIdentity()))
        msg.Send()
        offertes = EventManager.FilterAvailableEffects(msg, candidats, joueur, monde, None)
        if len(offertes) != n:
            soucis.append(f"{card_id} offre {len(offertes)} Action(s) de heros (attendu {n})")
    if "taille_deck_rencontre" in attendu:
        from game.operate.worlds import Worlds
        reel = len(Worlds.GetEncounterDeckCards(monde))
        if reel != attendu["taille_deck_rencontre"]:
            soucis.append(f"deck rencontre = {reel} carte(s) (attendu {attendu['taille_deck_rencontre']})")
    if "defausse_ids" in attendu:
        from game.operate.worlds import Worlds
        reel = sorted(getattr(f.paper, "card_id", "?") for f in Worlds.GetEncounterDiscardPileCards(monde))
        if reel != sorted(attendu["defausse_ids"]):
            soucis.append(f"defausse rencontre {reel} (attendu {sorted(attendu['defausse_ids'])})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''

