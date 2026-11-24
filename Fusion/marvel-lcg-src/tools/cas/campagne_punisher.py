# Cas test_capacites de la CAMPAGNE « La ville ne dort jamais », combat 1 (pu140 Big Apple Gang War!, pu141 Seized Tech Crates, et les deux
# ecritures du carnet : stade 2A de pu002a et releve de fin de partie de `punisher_mcdc_2026/campaign.py`). Prefixe `[camp]`.
# Deux montages : (1) la VRAIE mise en place (`scenario: the_big_apple`, `campagne: True`) pour la mise en jeu de pu140 et le carnet SORTANT
# (relu dans `campaign_log_last_file`, comme `fnefin_carnet_sortant`) ; (2) `rhino` pour pu141 (Spider-Man, main reduite a UNE carte).
# ⚠ `Puzzle.SendGameWouldBegin()` : le Setup de pu141 (`AfterGameSetup`) part une fois, AVANT le montage d'un cas : on le renvoie a la main.
SC = "the_big_apple"
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
HEROS_K = FORME_HEROS


def _rec(nom, pourquoi, scenario, pv_restants, attendu, **cle):
    """Regle experte « soigner de sa REC » : le carnet donne les PV restants du joueur 1 (Peter Parker, 10 PV, REC 3), forme alter-ego du depart."""
    carnet = {"Punisher Ally": "1", "Seized Tech Crates": "1", "Punisher's Ordnance Cache": "1", "Underling": "Jigsaw",
              "Player 1 Identity": "Spider-Man", "Player 1 Remaining hit points": str(pv_restants)}
    return _c(nom, pourquoi, [], [], attendu, scenario=scenario, campagne=True, carnet=carnet, **cle)


def _k(nom, pourquoi, mise, declencher, attendu, **cle):
    """Combat 4 : scenario genere Kingsfall (Kingpin + SWAT + Tracksuit Mafia), campagne, carnet du combat 3 (allie Punisher gagne)."""
    cle.setdefault("carnet", {"Punisher Ally": "1", "Player 1 Identity": "Spider-Man"})
    return _c(nom, pourquoi, mise, declencher, attendu, scenario="kingsfall", campagne=True, **cle)

RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
DEUX_PISTES = ["Puzzle.AddToVictoryDisplay('pu041')", "Puzzle.AddToVictoryDisplay('pu042')"]   # pu041 = piste 3 (Upper East Side), pu042 = piste 4 (West Village)
GUNRUNNER = ["Puzzle.AdvanceMainScheme(1)", "Puzzle.AdvanceMainScheme(1)"]                      # 1B -> 2A -> 3A (Gunrunner attache a un CAPO)


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[camp] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC), "heros": "spider_man",
           "mise_en_place": mise, "declencher": declencher, "verifier": cle.pop("verifier", "camp_etat"), "attendu": attendu,
           "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


def _b(nom, pourquoi, mise, declencher, attendu, **cle):
    """Combat 2 : scenario genere The Getaway + Jigsaw, campagne, carnet du combat 1 (Caisses gagnees)."""
    cle.setdefault("carnet", {"Seized Tech Crates": "1", "Player 1 Identity": "Spider-Man"})
    return _c(nom, pourquoi, mise, declencher, attendu, scenario=cle.pop("scenario", "tracking_the_buyer_the_getaway_jigsaw"), campagne=True, **cle)


HEROS = "Puzzle.ChangeForm('01001b')"
RIEN3 = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105')"]


def _t(nom, pourquoi, mise, declencher, attendu, **cle):
    """Combat 3 : scenario genere Punishment contre Hobgoblin (le sous-fifre du combat 2 etait Jigsaw), carnet du combat 2."""
    cle.setdefault("carnet", {"Seized Tech Crates": "1", "Punisher's Ordnance Cache": "1", "Underling": "Jigsaw", "Player 1 Identity": "Spider-Man"})
    return _c(nom, pourquoi, mise, declencher, attendu, scenario=cle.pop("scenario", "punishment_hobgoblin"), campagne=True, **cle)


def _caisses(nom, pourquoi, mise, declencher, attendu, carnet=None, **cle):
    """pu141 : `rhino`, Spider-Man, la carte en jeu SOUS LE CONTROLE du premier joueur (`under_control`)."""
    cle.setdefault("carnet", carnet if carnet is not None else {"Player 1 Identity": "Spider-Man"})
    return _c(nom, pourquoi, [*RIEN, FORME_HEROS, *mise], declencher, attendu, scenario="rhino", campagne=True, **cle)


CAS = [
    # ---------------------------------------------------------------------------------------------------------- pu140
    _c("pu140 mise en place (campagne) : l'environnement Big Apple Gang War! entre en jeu avec la ville",
       "Battle Setup / Setup : `CampaignSetup()` de pu001a met pu140 en jeu (WhenCampaignSetup)", [], [],
       {"en_jeu": ["pu140", "pu005", "pu006", "pu001b"]}, campagne=True, verifier="camp_etat"),
    _c("pu140, TEMOIN : hors campagne (partie ordinaire de The Big Apple), l'environnement n'entre PAS en jeu", "WhenCampaignSetup ne part qu'en campagne",
       [], [], {"hors_jeu": ["pu140"], "en_jeu": ["pu005"]}),
    # ---------------------------------------------------------------------------------------------------------- pu002a : le lieu
    _c("pu002a (campagne) : 2 pistes en victoire (pu041 puis pu042) -> le carnet note le lieu de la DERNIERE : West Village",
       "« record the location where the final LEAD card was added to the victory display » : la derniere ajoutee, pas la premiere",
       [], [*DEUX_PISTES, "Puzzle.Win()"],
       {"carnet_cles": {"Final LEAD Location": "West Village"}}, campagne=True),
    _c("pu002a (campagne) : l'ordre inverse (pu042 puis pu041) -> Upper East Side (la derniere, quelle que soit la carte)",
       "TEMOIN de l'ordre : le lieu suit la derniere piste ajoutee", [], ["Puzzle.AddToVictoryDisplay('pu042')", "Puzzle.AddToVictoryDisplay('pu041')", "Puzzle.Win()"],
       {"carnet_cles": {"Final LEAD Location": "Upper East Side"}}, campagne=True),
    _c("pu002a, TEMOIN : hors campagne, 2A se revele sans rien ecrire au carnet (le magasin n'a pas la cle)",
       "« In campaign mode » seulement", [], DEUX_PISTES, {"store_sans": ["Final LEAD Location"], "en_jeu": ["pu002b"]}),
    # ---------------------------------------------------------------------------------------------------------- releve
    _c("Releve (campagne, victoire par Gunrunner) : environnement retourne, Caisses gagnees, Trafiquant d'armes = le CAPO porteur",
       "Victory de pu140 : « Flip this card and put Seized Tech Crates into play for battles 2 and 3 » + CAPO Trafiquant d'armes",
       [], [*GUNRUNNER, "Puzzle.DamageAllVillains(100)", "Puzzle.DamageAllVillains(100)"],
       {"partie": "gagnee", "carnet_cles": {"Big Apple Gang War!": "Flipped", "Seized Tech Crates": "1"}, "trafiquant_egal_porteur": True,
        "carnet_gagnee": True}, campagne=True),
    _c("Releve (campagne, victoire forcee AVANT 3A) : environnement retourne et Caisses gagnees, mais PAS de Trafiquant d'armes",
       "Gunrunner n'est pas en jeu : rien a noter pour lui", [], ["Puzzle.Win()"],
       {"carnet_cles": {"Big Apple Gang War!": "Flipped", "Seized Tech Crates": "1"}, "carnet_cles_absentes": ["Gunrunner"], "carnet_gagnee": True}, campagne=True),
    _c("Releve (campagne, DEFAITE) : rien n'est coche (ni environnement, ni Caisses, ni Trafiquant) ; les PV restants restent",
       "« Defaite : on reinitialise le scenario et on reessaie sans penalite »", [], [*GUNRUNNER, "Puzzle.Lose()"],
       {"carnet_cles_absentes": ["Big Apple Gang War!", "Seized Tech Crates", "Gunrunner"], "carnet_cles_presentes": ["Player 1 Remaining hit points"],
        "carnet_gagnee": False}, campagne=True),
    _c("Releve : l'estampille du carnet est l'id du scenario de la campagne (the_big_apple)", "le panneau ignore tout releve dont l'estampille differe",
       [], ["Puzzle.Win()"], {"carnet_scenario": "the_big_apple"}, campagne=True),
    # ---------------------------------------------------------------------------------------------------------- pu141 : Setup
    _caisses("pu141 Setup : le seul joueur etait dans la partie precedente (carnet : Spider-Man) -> 1 compteur",
             "« Place 1 counter here, plus 1 more for each player who did not play the last game together »",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)"], ["Puzzle.SendGameWouldBegin()"], {"compteurs": [["pu141", "counter", 1]]}),
    _caisses("pu141 Setup : un 2e joueur (Iron Man) n'etait PAS dans la partie precedente -> 2 compteurs",
             "« plus 1 more for each player who did not play the last game together » : un heros absent du carnet",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)"], ["Puzzle.SendGameWouldBegin()"], {"compteurs": [["pu141", "counter", 2]]},
             heros2="iron_man"),
    _caisses("pu141 Setup : DEUX joueurs, tous deux dans la partie precedente (carnet : Spider-Man x2) -> 1 compteur (temoin)",
             "personne de nouveau : seulement le compteur de base",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)"], ["Puzzle.SendGameWouldBegin()"], {"compteurs": [["pu141", "counter", 1]]},
             heros2="spider_man", carnet={"Player 1 Identity": "Spider-Man", "Player 2 Identity": "Spider-Man"}),
    _caisses("pu141 Setup : aucun carnet de la partie precedente -> 1 compteur (on ne sait pas qui est nouveau)",
             "decision documentee dans le script : sans carnet, aucun joueur en plus",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)"], ["Puzzle.SendGameWouldBegin()"], {"compteurs": [["pu141", "counter", 1]]}, carnet={"Autre": "1"}),
    # ---------------------------------------------------------------------------------------------------------- pu141 : Action
    _caisses("pu141 Action, 1er choix : la carte suivante coute 1 de moins -> Aunt May (cout 1), seule carte de la main, est jouee sans ressource ; 1 compteur retire",
             "« Remove 1 counter -> reduce the cost of the next card you play this phase by 1 »",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)", "Puzzle.PlaceCounters('pu141', 'counter', 2)"],
             ["Puzzle.Action('pu141', 'Action')"],
             {"compteurs": [["pu141", "counter", 1]], "en_jeu": ["01006"]}, main_exclusive=["01006"], jouer=["01006"],
             choisir_option="Reduce_the_cost_of_the_next_card_you_play_this_phase_by_1"),
    _caisses("pu141 Action, TEMOIN : sans l'Action, Aunt May (cout 1, rien pour le payer) reste en main",
             "preuve par insuffisance : sans reduction la carte est impayable",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)", "Puzzle.PlaceCounters('pu141', 'counter', 2)"], [],
             {"compteurs": [["pu141", "counter", 2]], "en_main": ["01006"]}, main_exclusive=["01006"], jouer=["01006"]),
    _caisses("pu141 Action, 2e choix : chercher un soutien/une amelioration de cout <= 2 -> UNE carte de ce type rejoint la main ; 1 compteur retire",
             "« Find a support or upgrade with a cost of 2 or less and add it to your hand »",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)", "Puzzle.PlaceCounters('pu141', 'counter', 2)"],
             ["Puzzle.Action('pu141', 'Action')"],
             {"compteurs": [["pu141", "counter", 1]], "main_ok": {"taille": 2, "types": ["Support", "Upgrade"], "cout_max": 2}},
             choisir_option="Find_a_support_or_upgrade_with_a_cost_of_2_or_less_and_add_it_to_your_hand"),
    _caisses("pu141 Action, 2e choix, la seule carte eligible est dans la DEFAUSSE du joueur (deck vide) -> elle rejoint la main (find = toutes les zones, decision du 23/10/2026)",
             "« Find a support or upgrade ... » : la Rules Reference du moteur (`find.py`) fouille deck, defausse, zone de jeu, mises de cote",
             ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDiscardPile('01007')", "Puzzle.PutIntoPlay('pu141', under_control=True)", "Puzzle.PlaceCounters('pu141', 'counter', 2)"],
             ["Puzzle.Action('pu141', 'Action')"],
             {"compteurs": [["pu141", "counter", 1]], "main_ok": {"taille": 2, "types": ["Support", "Upgrade"], "cout_max": 2}},
             choisir_option="Find_a_support_or_upgrade_with_a_cost_of_2_or_less_and_add_it_to_your_hand"),
    _caisses("pu141 Action : sans compteur, l'Action n'est pas offerte (rien ne change)",
             "« Remove 1 counter -> » : le retrait est le cout",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)"], [],
             {"compteurs": [["pu141", "counter", 0]]}, declencher_tolerant=["Puzzle.Action('pu141', 'Action')"]),
    _caisses("pu141 Action : limite UNE fois par joueur et par round -> la 2e Action du meme joueur n'est pas offerte (2 compteurs -> 1)",
             "« limit once per player per round »",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)", "Puzzle.PlaceCounters('pu141', 'counter', 2)"],
             ["Puzzle.Action('pu141', 'Action')"],
             {"compteurs": [["pu141", "counter", 1]]}, main_exclusive=["01006"], declencher_tolerant=["Puzzle.Action('pu141', 'Action')"]),
    # ---------------------------------------------------------------------------------------------------------- combat 2 : pu142
    _b("pu142 mise en place (campagne, scenario The Getaway + Jigsaw) : l'environnement est en jeu, Seized Tech Crates aussi (le carnet l'a gagnee) avec 1 compteur",
       "Setup par `encounters` du scenario genere ; « put Seized Tech Crates into play for battles 2 and 3 » (WhenCampaignSetup)", [], [],
       {"en_jeu": ["pu142", "pu141"], "compteurs": [["pu141", "counter", 1]]}),
    _b("pu142, TEMOIN : le carnet n'a PAS gagne les Caisses -> pu141 n'entre pas en jeu", "la recompense depend du carnet", [], [],
       {"en_jeu": ["pu142"], "hors_jeu": ["pu141"]}, carnet={"Player 1 Identity": "Spider-Man"}),
    _b("pu142 releve (victoire, Jigsaw) : environnement retourne, Ordnance Cache gagnee, sous-fifre = Jigsaw, estampille tracking_the_buyer",
       "Victory : « Flip this card and put Punisher's Ordnance Cache into play for battle 3 »", [], ["Puzzle.Win()"],
       {"carnet_cles": {"Tracking the Buyer": "Flipped", "Punisher's Ordnance Cache": "1", "Underling": "Jigsaw"}, "carnet_scenario": "tracking_the_buyer",
        "carnet_gagnee": True}),
    _b("pu142 releve (victoire, Hobgoblin) : sous-fifre = Hobgoblin", "le sous-fifre affronte est note (combat 3 : l'autre)", [], ["Puzzle.Win()"],
       {"carnet_cles": {"Underling": "Hobgoblin"}}, scenario="tracking_the_buyer_the_getaway_hobgoblin"),
    _b("pu142 releve, le releve Fear No Evil de la manigance est CONSERVE (l'ecriture est partagee, pas ecrasee)", "collecteur partage : `Completed Scenarios` = the_getaway ET les cles Punisher",
       [], ["Puzzle.Win()"], {"carnet_cles": {"Completed Scenarios": "the_getaway", "Tracking the Buyer": "Flipped"}}),
    _b("pu142 releve (DEFAITE) : rien de coche", "pas de recompense a la defaite", [], ["Puzzle.Lose()"],
       {"carnet_cles_absentes": ["Tracking the Buyer", "Punisher's Ordnance Cache", "Underling"], "carnet_gagnee": False}),
    # ---------------------------------------------------------------------------------------------------------- le choix du scenario du combat 2
    _c("Combat 2 : le tableau de p265 (9 lieux x 8 CAPO) designe toujours un scenario qui existe, avec la bonne manigance et le bon sous-fifre",
       "« Main scheme based on the final lead » + « Hobgoblin (Nefaria, Ringmaster, Mr. Negative, Nightshade) or Jigsaw (other 4) »",
       [], [], {}, scenario="rhino", verifier="camp_choix"),
    # ---------------------------------------------------------------------------------------------------------- les 20 scenarios du combat 2
    *[_b(f"Combat 2 : le scenario {m}_{u}{ex} se monte en campagne (la scene se cree ; pu142 et pu141 en jeu)",
         "scenario genere (modular_sets Hit List + Syndicate + Capo of the Past, pu142 dans `encounters`)", [], [],
         {"en_jeu": ["pu142", "pu141"]}, scenario=f"tracking_the_buyer_{m}_{u}{ex}")
      for m in ("art_museum_heist", "the_getaway", "the_raft_breakout", "protection_racket", "stop_the_presses")
      for u in ("jigsaw", "hobgoblin") for ex in ("", "_expert")],
    # ---------------------------------------------------------------------------------------------------------- combat 3 : pu144, pu145, pu146
    _t("pu144 mise en place (campagne, Punishment + Hobgoblin) : l'environnement est en jeu, avec Seized Tech Crates et Ordnance Cache (le carnet les a gagnees)",
       "Battle Setup + « Mettez en jeu ... si vous l'avez gagnee »", [], [], {"en_jeu": ["pu144", "pu141", "pu143"], "hors_jeu": ["pu145"]}),
    _t("pu144, TEMOIN : le carnet n'a gagne ni les Caisses ni la Cache -> ni pu141 ni pu143", "la recompense depend du carnet", [], [],
       {"en_jeu": ["pu144"], "hors_jeu": ["pu141", "pu143"]}, carnet={"Underling": "Jigsaw", "Player 1 Identity": "Spider-Man"}),
    _t("pu144 Forced Response : le complot principal avance au stade 2A -> l'environnement est retourne : pu144 part, S.H.I.E.L.D. Support Team entre en jeu avec 1 compteur",
       "« After ... the main scheme advances to stage 2A, flip this card »", [], ["Puzzle.AdvanceMainScheme(1)"],
       {"hors_jeu": ["pu144"], "en_jeu": ["pu145"], "compteurs": [["pu145", "intelligence", 1]]}),
    _t("pu144 Forced Response : le premier stade du Punisher est vaincu -> l'environnement est retourne (1re vague absorbee par Tough, 2e vainc)",
       "« After Punisher's first stage is defeated ... flip this card »", RIEN3, ["Puzzle.Damage('pu086a', 99)", "Puzzle.Damage('pu086a', 99)"],
       {"hors_jeu": ["pu144"], "en_jeu": ["pu145", "pu087a"]}),
    _t("pu144, TEMOIN : sans rien de tout cela, l'environnement reste en jeu et pu145 n'existe pas", "pas de retournement spontane", [], [],
       {"en_jeu": ["pu144"], "hors_jeu": ["pu145"]}),
    _t("pu144 : une seule fois -> stade 1 vaincu PUIS complot en 2A : UNE seule S.H.I.E.L.D. Support Team", "la carte retournee ne se retourne pas deux fois",
       RIEN3, ["Puzzle.Damage('pu086a', 99)", "Puzzle.Damage('pu086a', 99)", "Puzzle.AdvanceMainScheme(1)"], {"copies_en_jeu": [["pu145", 1]]}),
    _t("pu144 releve (victoire) : l'allie Punisher est gagne (Punisher Ally = 1), estampille punishment", "« VICTOIRE : Vous avez gagne l'allie Punisher (6138) »",
       [], ["Puzzle.Win()"], {"carnet_cles": {"Punisher Ally": "1"}, "carnet_scenario": "punishment", "carnet_gagnee": True}),
    _t("pu144 releve (DEFAITE) : pas d'allie", "rien a la defaite", [], ["Puzzle.Lose()"], {"carnet_cles_absentes": ["Punisher Ally"], "carnet_gagnee": False}),
    _t("pu145 entre en jeu : 1 compteur intelligence (le seul joueur etait dans la partie precedente)", "« After this card enters play, place 1 intelligence counter here, plus 1 ... »",
       ["Puzzle.PutIntoPlay('pu145', under_control=True)"], [], {"compteurs": [["pu145", "intelligence", 1]]}),
    _t("pu145 entre en jeu : un 2e joueur (Iron Man) absent de la partie precedente -> 2 compteurs", "idem pu141", ["Puzzle.PutIntoPlay('pu145', under_control=True)"], [],
       {"compteurs": [["pu145", "intelligence", 2]]}, heros2="iron_man"),
    _t("pu145 Response : un joueur vainc un sbire -> 1 compteur retire, chaque joueur pioche 1 carte, 1 carte de rencontre est donnee",
       "« After a player defeats a minion, remove 1 counter -> each player draws 1 card. Deal 1 player an encounter card »",
       [*RIEN3, HEROS, "Puzzle.PutIntoPlay('pu145', under_control=True)", "Puzzle.PutIntoPlay('01110')"], ["Puzzle.Damage('01110', 1)", "Puzzle.Attack('01001a')"],
       {"compteurs": [["pu145", "intelligence", 0]], "taille_main": 2, "hors_jeu": ["01110"], "cartes_donnees": 1}, cibles=["01110"]),
    _t("pu145 Response, TEMOIN : sans compteur, rien (la main reste a 1 carte)", "le retrait est un cout",
       [*RIEN3, HEROS, "Puzzle.PutIntoPlay('pu145', under_control=True)", "Puzzle.PutIntoPlay('01110')", "Puzzle.PlaceCounters('pu145', 'intelligence', -1)"],
       ["Puzzle.Damage('01110', 1)", "Puzzle.Attack('01001a')"], {"compteurs": [["pu145", "intelligence", 0]], "taille_main": 1, "hors_jeu": ["01110"], "cartes_donnees": 0},
       cibles=["01110"]),
    _t("pu146 Punisher : son attaque gagne PERCING -> il vainc un sbire Tough (Hydra Bomber 2 PV) d'une attaque (ATK 2)", "« Punisher's attacks gain piercing and ranged »",
       ["Puzzle.PutIntoPlay('pu146', under_control=True)", "Puzzle.PutIntoPlay('01110')", "Puzzle.Tough('01110')"], ["Puzzle.Attack('pu146')"],
       {"hors_jeu": ["01110"]}, cibles=["01110"]),
    _t("pu146 Response : apres avoir vaincu un sbire (Hydra Bomber), 2 degats a un AUTRE ennemi (Shocker, 3 PV : il en garde 1)", "« After Punisher attacks and defeats a minion, deal 2 damage to an enemy »",
       ["Puzzle.PutIntoPlay('pu146', under_control=True)", "Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('pu146')"],
       {"hors_jeu": ["01110"], "degats": [["01103", 2]]}, cibles=["01110", "01103"]),
    _t("pu146 Response, TEMOIN : le sbire attaque SURVIT (Shocker 3 PV, ATK 2) -> pas de Response, aucun autre ennemi blesse (Hydra Bomber intact)",
       "« defeats a minion » : sans defaite, rien", ["Puzzle.PutIntoPlay('pu146', under_control=True)", "Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')"],
       ["Puzzle.Attack('pu146')"], {"en_jeu": ["01103"], "degats": [["01103", 2], ["01110", 0]]}, cibles=["01103", "01110"]),
    # ---------------------------------------------------------------------------------------------------------- le choix du scenario du combat 3
    _c("Combat 3 : le sous-fifre du combat 2 note au carnet designe le scenario de l'AUTRE (Jigsaw -> Hobgoblin, Hobgoblin -> Jigsaw), standard et expert, et ils existent",
       "« the UNDERLING that you did not use in campaign battle 2 »", [], [], {}, scenario="rhino", verifier="camp_choix3"),
    # ---------------------------------------------------------------------------------------------------------- pu143
    _caisses("pu143 Setup : le seul joueur etait dans la partie precedente -> 1 compteur", "« Place 1 counter here, plus 1 more for each player who did not play the last game together »",
             ["Puzzle.PutIntoPlay('pu143', under_control=True)"], ["Puzzle.SendGameWouldBegin()"], {"compteurs": [["pu143", "counter", 1]]}),
    _caisses("pu143 Setup : un 2e joueur (Iron Man) etait absent -> 2 compteurs", "idem pu141 (decision P6)",
             ["Puzzle.PutIntoPlay('pu143', under_control=True)"], ["Puzzle.SendGameWouldBegin()"], {"compteurs": [["pu143", "counter", 2]]}, heros2="iron_man"),
    _caisses("pu143 Action (collection) : 1 compteur retire, 3 menaces sur le complot principal, UNE arme d'aspect ou basique rejoint la main",
             "« Remove 1 counter and place 3 threat on the main scheme -> search ... and add it to your hand » ; aucune arme dans le deck : la collection",
             ["Puzzle.PutIntoPlay('pu143', under_control=True)", "Puzzle.PlaceCounters('pu143', 'counter', 2)"], ["Puzzle.SetThreat('01097b', 1)", "Puzzle.Action('pu143', 'Action')"],
             {"compteurs": [["pu143", "counter", 1]], "menace": [["01097b", 4]], "main_arme": {"taille": 2}}),
    _caisses("pu143 Action (deck) : une arme est dans le deck -> c'est elle qui rejoint la main (Hand Cannon 16046)",
             "le deck est fouille avant la collection",
             ["Puzzle.PutIntoPlay('pu143', under_control=True)", "Puzzle.PlaceCounters('pu143', 'counter', 2)", "Puzzle.MoveTo('16046', 'PlayerDeck')"],
             ["Puzzle.Action('pu143', 'Action')"], {"compteurs": [["pu143", "counter", 1]], "en_main": ["16046"]}, accepter_choix=True),
    _caisses("pu143 Action (defausse) : une arme est dans la DEFAUSSE -> c'est elle qui rejoint la main : la defausse retombe a sa taille de depart, 6 (UNE recherche sur les 3 zones, 23/10/2026)",
             "« search your deck, discard pile, and collection »",
             ["Puzzle.PutIntoPlay('pu143', under_control=True)", "Puzzle.PlaceCounters('pu143', 'counter', 2)", "Puzzle.CreatePlayerDiscardPile('16046')"],
             ["Puzzle.Action('pu143', 'Action')"], {"compteurs": [["pu143", "counter", 1]], "en_main": ["16046"], "defausse_joueur": 6}),
    _caisses("pu143 Action : sans compteur, l'Action n'est pas offerte (menace intacte)", "le retrait du compteur est un cout",
             ["Puzzle.PutIntoPlay('pu143', under_control=True)"], ["Puzzle.SetThreat('01097b', 1)"],
             {"compteurs": [["pu143", "counter", 0]], "menace": [["01097b", 1]]}, declencher_tolerant=["Puzzle.Action('pu143', 'Action')"]),
    _caisses("pu143 Action : N'IMPORTE QUEL joueur peut la declencher (joueur 2) -> 1 compteur retire, 3 menaces", "« Any player may trigger this ability »",
             ["Puzzle.PutIntoPlay('pu143', under_control=True)", "Puzzle.PlaceCounters('pu143', 'counter', 2)"],
             ["Puzzle.SetThreat('01097b', 1)", "Puzzle.Action('pu143', 'Action', siege=1)"], {"compteurs": [["pu143", "counter", 1]], "menace": [["01097b", 4]]}, heros2="spider_man",
             carnet={"Player 1 Identity": "Spider-Man", "Player 2 Identity": "Spider-Man"}),
    _caisses("pu141 Action : N'IMPORTE QUEL joueur peut la declencher, une fois chacun -> joueur 1 puis joueur 2 : 3 compteurs -> 1",
             "« any player may trigger this ability, limit once per player per round » : la limite est PAR JOUEUR",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)", "Puzzle.PlaceCounters('pu141', 'counter', 3)"],
             ["Puzzle.Action('pu141', 'Action')", "Puzzle.Action('pu141', 'Action', siege=1)"],
             {"compteurs": [["pu141", "counter", 1]]}, heros2="spider_man", carnet={"Player 1 Identity": "Spider-Man", "Player 2 Identity": "Spider-Man"}),
    _caisses("pu141 Action, TEMOIN : le joueur 1 declenche deux fois, le joueur 2 une fois -> seulement 2 retraits (3 compteurs -> 1), pas 3",
             "la limite par joueur bloque la 2e Action du joueur 1 meme quand un autre joueur a joue entre-temps",
             ["Puzzle.PutIntoPlay('pu141', under_control=True)", "Puzzle.PlaceCounters('pu141', 'counter', 3)"],
             ["Puzzle.Action('pu141', 'Action')", "Puzzle.Action('pu141', 'Action', siege=1)"],
             {"compteurs": [["pu141", "counter", 1]]}, heros2="spider_man", carnet={"Player 1 Identity": "Spider-Man", "Player 2 Identity": "Spider-Man"},
             declencher_tolerant=["Puzzle.Action('pu141', 'Action')"]),
    # ---------------------------------------------------------------------------------------------------------- pu139 Capo of the Past
    _b("pu139 When Revealed : un CAPO tire au hasard (face A) entre en jeu comme SBIRE ELITE engage avec le joueur, Steady, Villainous, victory 0, pu139 attachee",
       "« Treat attached character as an ELITE minion. It gains steady, villainous, and victory 0 » + « put it into play engaged with you and attach this card to it »",
       [], ["Puzzle.Reveal('pu139')"], {"capo_du_passe": {"face": "a"}}),
    _b("pu139 When Revealed, EXPERT : la face B du CAPO tire au hasard", "face B en expert", [], ["Puzzle.Reveal('pu139')"],
       {"capo_du_passe": {"face": "b"}}, scenario="tracking_the_buyer_the_getaway_jigsaw_expert"),
    _b("pu139, DEFAITE du CAPO-sbire : il quitte le jeu avec pu139 (aucun CAPO en jeu ensuite)", "le sbire se bat comme un sbire : degats, defaite",
       [], ["Puzzle.Reveal('pu139')", "Puzzle.Damage('minion', 99)"], {"capo_du_passe": {"face": "a", "absent": True}}),
    _b("pu139, DEFAITE du CAPO-sbire : Victory 0 -> il va dans la PILE DE VICTOIRE (pas la defausse)", "« victory 0 » : la carte vaincue est ajoutee a la pile de victoire (decision du 23/10/2026)",
       [], ["Puzzle.Reveal('pu139')", "Puzzle.Damage('minion', 99)"], {"capo_du_passe": {"face": "a", "en_victoire": True}}),
    _b("pu139, TEMOIN de la defaite : 1 seul degat -> le CAPO-sbire est TOUJOURS en jeu (le cas de defaite ne passe donc pas a vide)", "un sbire a PV fixes ne tombe pas au 1er degat",
       [], ["Puzzle.Reveal('pu139')", "Puzzle.Damage('minion', 1)"], {"capo_du_passe": {"face": "a"}}),
    _b("pu139, PHASE DU MECHANT : le CAPO-sbire engage active (attaque ou manigance) sans erreur", "un sbire engage s'active comme un sbire",
       [HEROS_K], ["Puzzle.Reveal('pu139')", "Puzzle.RunVillainPhase()"], {"capo_du_passe": {"face": "a"}}),
    _b("pu139 Boost : la carte est donnee au joueur face cachee (1 carte de rencontre donnee)", "« Deal this to yourself as a facedown encounter card »",
       RIEN, ["Puzzle.Boost('pu139')"], {"cartes_donnees": 1}),
    # ---------------------------------------------------------------------------------------------------------- combat 4 : pu147, pu148, pu149a/b
    _k("pu147 Setup (Kingsfall, l'allie Punisher est gagne) : l'allie pu146 entre en jeu, pu147 est retournee en pu148 Power to the People avec 1 compteur, Long Live (pu149a) est en jeu",
       "« Put the Punisher ally into play under a player's control. Flip this card and place 1 counter on it. »", [], [],
       {"en_jeu": ["pu146", "pu148", "pu149a"], "hors_jeu": ["pu147", "pu149b"], "compteurs": [["pu148", "counter", 1]]}),
    _k("pu147 Setup, TEMOIN : le carnet ne dit pas que l'allie est gagne -> pas de Punisher, mais le retournement (pu148, 1 compteur) a lieu quand meme",
       "« Ne mettez pas en jeu l'allie Punisher si vous n'avez pas gagne le scenario precedent »", [], [],
       {"en_jeu": ["pu148"], "hors_jeu": ["pu146", "pu147"], "compteurs": [["pu148", "counter", 1]]}, carnet={"Player 1 Identity": "Spider-Man"}),
    _k("pu147 releve : Kingpin vaincu (victoire) -> le carnet sortant est estampille `kingsfall` et marque gagne (l'id du combat 4 dans la campagne)",
       "l'ecran de campagne identifie le scenario termine par l'estampille", [], ["Puzzle.Win()"], {"carnet_scenario": "kingsfall", "carnet_gagnee": True}),
    _k("pu147 releve, DEFAITE : meme estampille, non gagne", "la defaite est reportee aussi", [], ["Puzzle.Lose()"], {"carnet_scenario": "kingsfall", "carnet_gagnee": False}),
    _k("pu149a Forced Interrupt : fin de la phase des joueurs -> TOUS les jetons de soutien de Public Support passent sur Long Live (2 -> 0 ici, 2 ici)",
       "« move each support counter from your Public Support to here »", [HEROS_K, "Puzzle.Counter('60163a', 'support', 2)"], ["Puzzle.EndPlayerPhase()"],
       {"compteurs": [["60163a", "support", 0], ["pu149a", "support", 2]], "en_jeu": ["pu149a"]}),
    _k("pu149a Forced Interrupt : le total ici atteint 2 x 1 + 2 = 4 -> Long Live est retournee en Down With (pu149b), qui remet Public Support a 2 x 1 + 3 = 5",
       "« Then, if there are 2[per_hero]+2[per_group] counters here, flip this card » + Down With : « resets ... to 2[per_hero]+3 »",
       [HEROS_K, "Puzzle.Counter('pu149a', 'support', 2)", "Puzzle.Counter('60163a', 'support', 2)"], ["Puzzle.EndPlayerPhase()"],
       {"en_jeu": ["pu149b"], "hors_jeu": ["pu149a"], "compteurs": [["60163a", "support", 5]]}),
    _k("pu149a, TEMOIN : 3 jetons seulement (2 x 1 + 2 = 4 requis) -> pas de retournement", "le seuil est 4, pas 3",
       [HEROS_K, "Puzzle.Counter('pu149a', 'support', 2)", "Puzzle.Counter('60163a', 'support', 1)"], ["Puzzle.EndPlayerPhase()"],
       {"en_jeu": ["pu149a"], "hors_jeu": ["pu149b"], "compteurs": [["pu149a", "support", 3]]}),
    _k("pu149b When Revealed : Public Support a PLUS de jetons (9) -> ramene a 5 (reset TO, pas seulement un plafond inverse)",
       "« resets the number of support counters ... to 2[per_hero]+3 »",
       [HEROS_K, "Puzzle.Counter('pu149a', 'support', 3)", "Puzzle.Counter('60163a', 'support', 9)"], ["Puzzle.EndPlayerPhase()"],
       {"en_jeu": ["pu149b"], "compteurs": [["60163a", "support", 5]]}),
    _k("pu148 Action (retirer 2 menaces) : 1 compteur retire, 2 menaces en moins sur le complot principal", "« Remove 1 counter from here -> ... Remove 2 threat from a scheme »",
       [HEROS_K, "Puzzle.PlaceCounters('pu148', 'counter', 1)"],
       ["Puzzle.SetThreat('60161b', 5)", "Puzzle.Action('pu148', 'Action')"], {"compteurs": [["pu148", "counter", 1]], "menace": [["60161b", 3]]}, choisir_option="Remove_2_threat_from_a_scheme"),
    _k("pu148 Action (jouer une carte) : 1 compteur retire, Black Widow (cout 3) est jouee pour 2 icones (Genius BB) : cout reduit de 1", "« Play a card from your hand, reducing its cost by 1 »",
       [HEROS_K, ], ["Puzzle.Action('pu148', 'Action')"],
       {"compteurs": [["pu148", "counter", 0]], "en_jeu": ["01075"]}, choisir_option="Play_a_card_from_your_hand,_reducing_its_cost_by_1",
       main_exclusive=["01075", "01089"], cibles=["01001a", "01075"], payer_avec=["01089"]),
    _k("pu148 Action, TEMOIN : sans compteur, l'Action n'est pas offerte (menace intacte)", "le retrait du compteur est un cout",
       [HEROS_K, "Puzzle.PlaceCounters('pu148', 'counter', -1)"], ["Puzzle.SetThreat('60161b', 5)"],
       {"compteurs": [["pu148", "counter", 0]], "menace": [["60161b", 5]]}, declencher_tolerant=["Puzzle.Action('pu148', 'Action')"]),
    _k("pu148, TEMOIN : seul le choix \u00ab jouer une carte \u00bb reste (menace deja choisie ce round) et la main n'a aucune carte jouable -> l'Action n'est PAS offerte, le jeton est conserve",
       "decision de l'utilisateur : pas de jeton perdu pour rien", [HEROS_K, "Puzzle.PlaceCounters('pu148', 'counter', 2)"],
       ["Puzzle.SetThreat('60161b', 7)", "Puzzle.Action('pu148', 'Action')"], {"menace": [["60161b", 5]], "compteurs": [["pu148", "counter", 2]]},
       choisir_option="Remove_2_threat_from_a_scheme", declencher_tolerant=["Puzzle.Action('pu148', 'Action')", "Puzzle.Action('pu148', 'Action')"]),
    _k("pu148 : chaque choix UNE fois par round -> 3 Actions avec le meme choix : une seule retire 2 menaces (7 -> 5), les suivantes ne sont pas offertes",
       "« each choice may only be chosen once per group per round » (temoin d'epuisement)",
       [HEROS_K, "Puzzle.PlaceCounters('pu148', 'counter', 2)"],
       ["Puzzle.SetThreat('60161b', 7)", "Puzzle.Action('pu148', 'Action')"], {"menace": [["60161b", 5]]},
       choisir_option="Remove_2_threat_from_a_scheme", declencher_tolerant=["Puzzle.Action('pu148', 'Action')", "Puzzle.Action('pu148', 'Action')"]),
    # ---------------------------------------------------------------------------------------------------------- regle experte : soin par REC (combats 2 a 4)
    _rec("combat 3 EXPERT : PV reportes 5/10, le joueur accepte -> 1 carte de rencontre donnee face cachee, identite soignee de sa REC (Peter Parker 3) : 5 degats -> 2",
         "« Campagne experte uniquement : chaque joueur a le droit de s'attribuer une carte Rencontre face cachee pour soigner son identite d'un nombre de degats egal a sa REC »",
         "punishment_hobgoblin_expert", 5, {"degats_identite": 2, "cartes_donnees": 1}, accepter_choix=True),
    _rec("combat 3 EXPERT, TEMOIN : le joueur REFUSE (« a le droit ») -> rien n'est donne, les 5 degats restent", "le soin est facultatif",
         "punishment_hobgoblin_expert", 5, {"degats_identite": 5, "cartes_donnees": 0}, refuser_mise_en_place="Deal yourself 1 facedown encounter card"),
    _rec("combat 3 STANDARD : pas de regle (campagne experte seulement) -> aucune carte donnee, aucun degat", "« Campagne experte uniquement »",
         "punishment_hobgoblin", 5, {"degats_identite": 0, "cartes_donnees": 0}, accepter_choix=True),
    _rec("combat 3 EXPERT : REC superieure aux degats (9/10 restants = 1 degat) -> soigne jusqu'a 0, pas plus", "on soigne de sa REC, sans depasser les PV",
         "punishment_hobgoblin_expert", 9, {"degats_identite": 0, "cartes_donnees": 1}, accepter_choix=True),
    _rec("combat 2 EXPERT : meme regle (PV 5/10 -> 2 degats, 1 carte donnee)", "instructions de campagne du combat 2",
         "tracking_the_buyer_the_getaway_jigsaw_expert", 5, {"degats_identite": 2, "cartes_donnees": 1}, accepter_choix=True),
    _rec("combat 4 EXPERT : meme regle (PV 5/10 -> 2 degats, 1 carte donnee)", "instructions de campagne du combat 4",
         "kingsfall_expert", 5, {"degats_identite": 2, "cartes_donnees": 1}, accepter_choix=True),
]

VERIFICATIONS = r'''
def camp_etat(monde, aides):
    """Cles propres : `partie`, `store_sans` [cles absentes du magasin], `carnet_*` (le carnet SORTANT ecrit a la fin de la partie, comme
    `fnefin_carnet_sortant`), `trafiquant_egal_porteur`, `main_ok` {taille, types, cout_max} ; le reste va a `etat_attendu`."""
    import json, os
    from engine.config import ConfigVariables
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    propres = ("partie", "store_sans", "carnet_cles", "carnet_cles_absentes", "carnet_cles_presentes", "carnet_gagnee", "carnet_scenario",
               "trafiquant_egal_porteur", "main_ok", "main_arme", "copies_en_jeu", "cartes_donnees", "capo_du_passe")
    soucis = []
    if "partie" in attendu:
        etat = "en_cours" if not monde.is_game_over else ("gagnee" if monde.game_over.players_won else "perdue")
        if etat != attendu["partie"]:
            soucis.append(f"partie {etat} (attendu {attendu['partie']})")
    for cle in attendu.get("store_sans") or []:
        if monde.store.dic.get(cle):
            soucis.append(f"le magasin contient {cle} = {monde.store.dic.get(cle)!r}")
    if any(k.startswith("carnet_") or k == "trafiquant_egal_porteur" for k in attendu):
        chemin = ConfigVariables.File('campaign_log_last_file', './campaign_log_last.json').value
        if not os.path.exists(chemin):
            soucis.append(f"aucun carnet sortant ecrit ({chemin})")
        else:
            carnet = json.load(open(chemin, encoding="utf-8"))
            sug = carnet.get("suggestions") or {}
            if "carnet_gagnee" in attendu and bool(carnet.get("players_won")) != attendu["carnet_gagnee"]:
                soucis.append(f"players_won = {carnet.get('players_won')}")
            if "carnet_scenario" in attendu and carnet.get("scenario") != attendu["carnet_scenario"]:
                soucis.append(f"estampille = {carnet.get('scenario')!r}")
            for cle, valeur in (attendu.get("carnet_cles") or {}).items():
                if sug.get(cle) != valeur:
                    soucis.append(f"{cle} = {sug.get(cle)!r} (attendu {valeur!r})")
            for cle in attendu.get("carnet_cles_presentes") or []:
                if cle not in sug:
                    soucis.append(f"{cle} manque au carnet")
            for cle in attendu.get("carnet_cles_absentes") or []:
                if cle in sug:
                    soucis.append(f"{cle} = {sug[cle]!r} alors qu'il ne devrait pas y etre")
            if attendu.get("trafiquant_egal_porteur"):
                porteur = aides["par_id"](monde, "pu004")
                hote = getattr(porteur, "bind_face", None) if porteur is not None else None
                nom = hote.paper.name.lstrip("* ") if hote is not None else None
                if nom is None:
                    soucis.append("Gunrunner (pu004) n'est attache a aucun CAPO en fin de partie")
                elif sug.get("Gunrunner") != nom:
                    soucis.append(f"Gunrunner = {sug.get('Gunrunner')!r} (CAPO porteur : {nom!r})")
    if "main_ok" in attendu:
        voulu = attendu["main_ok"]
        main = monde.players[0].hand_cards.GetAll()
        if len(main) != voulu["taille"]:
            soucis.append(f"{len(main)} carte(s) en main (attendu {voulu['taille']}) : {[f.paper.card_id for f in main]}")
        nouvelles = [f for f in main if f.paper.card_id != "01088"]
        if len(nouvelles) != voulu["taille"] - 1:
            soucis.append(f"cartes trouvees = {[f.paper.card_id for f in nouvelles]}")
        for f in nouvelles:
            if type(f).__name__ not in voulu["types"]:
                soucis.append(f"{f.paper.card_id} est un {type(f).__name__} (attendu {voulu['types']})")
            cout = f.printed_cost.val
            if cout > voulu["cout_max"]:
                soucis.append(f"{f.paper.card_id} coute {cout} (> {voulu['cout_max']})")
    for card_id, n in attendu.get("copies_en_jeu") or []:
        vues = [o for o in monde.object_manager.card_dict.values()
                if getattr(getattr(getattr(o, "face", None), "paper", None), "card_id", None) == card_id and o.face.IsInPlay()]
        if len(vues) != n:
            soucis.append(f"{len(vues)} exemplaire(s) de {card_id} en jeu (attendu {n})")
    if "cartes_donnees" in attendu:
        donnees = sum(len(j.dealt_encounter_cards.Get()) for j in monde.const_players)
        if donnees != attendu["cartes_donnees"]:
            soucis.append(f"{donnees} carte(s) de rencontre donnee(s) (attendu {attendu['cartes_donnees']})")
    if "capo_du_passe" in attendu:
        from cards.database import CardsDB
        voulu = attendu["capo_du_passe"]
        trouves = [o.face for o in monde.object_manager.card_dict.values()
                   if str(getattr(getattr(o, "face", None), "pic_id", "")).startswith("pu0") and getattr(o.face, "pic_id", "")[-1:] == voulu["face"]
                   and type(o.face).__name__ == "Minion" and o.face.IsInPlay()]
        if voulu.get("en_victoire"):
            # DEFAITE du CAPO-sbire : Victory 0 = il va dans la PILE DE VICTOIRE, pas dans la defausse (decision du 23/10/2026).
            en_pile = [f for f in monde.victory_display.Get() if str(getattr(f, "pic_id", "")).startswith("pu0") and f.pic_id[-1:] == voulu["face"]]
            if trouves:
                soucis.append(f"{len(trouves)} sbire(s) CAPO encore en jeu (attendu 0)")
            if len(en_pile) != 1:
                soucis.append(f"{len(en_pile)} CAPO-sbire(s) dans la pile de victoire (attendu 1)")
        elif voulu.get("absent"):
            if trouves:
                soucis.append(f"{len(trouves)} sbire(s) CAPO encore en jeu (attendu 0)")
        elif len(trouves) != 1:
            soucis.append(f"{len(trouves)} sbire(s) CAPO face {voulu['face']} en jeu (attendu 1)")
        else:
            f = trouves[0]
            papier = CardsDB.FindCardPaper(f.pic_id)
            for trait in ("ELITE", "CAPO"):
                if not f.HasTrait(trait):
                    soucis.append(f"trait {trait} absent")
            if f.GetKeyword("Steady") < 1:
                soucis.append("pas Steady")
            if not f.IsVillainous():
                soucis.append("pas Villainous")
            if f.printed_victory != 0:
                soucis.append(f"victory = {f.printed_victory} (attendu 0)")
            if f.printed_health_numeral != int(papier.desc["HP"]):
                soucis.append(f"PV = {f.printed_health_numeral} (attendu {papier.desc['HP']} : {f.pic_id})")
            if f.printed_name != papier.name:
                soucis.append(f"nom = {f.printed_name!r} (attendu {papier.name!r})")
            if f.GetEngagedPlayer() is not monde.players[0]:
                soucis.append("pas engage avec le joueur 1")
            pu139 = [o.face for o in monde.object_manager.card_dict.values() if getattr(getattr(getattr(o, "face", None), "paper", None), "card_id", None) == "pu139"]
            if not pu139 or pu139[0].attached_face is not f:
                soucis.append(f"pu139 non attachee au CAPO (porteur = {pu139[0].attached_face if pu139 else 'carte absente'})")
    if "main_arme" in attendu:
        main = monde.players[0].hand_cards.GetAll()
        nouvelles = [f for f in main if f.paper.card_id != "01088"]
        if len(main) != attendu["main_arme"]["taille"] or len(nouvelles) != attendu["main_arme"]["taille"] - 1:
            soucis.append(f"main = {[f.paper.card_id for f in main]}")
        for f in nouvelles:
            if "WEAPON" not in f.paper.traits or f.paper.desc.get("Class") not in ("Aggression", "Justice", "Leadership", "Protection", "'Pool", "Determination", "Basic"):
                soucis.append(f"{f.paper.card_id} n'est pas une arme d'aspect/basique ({f.paper.desc.get('Class')})")
    cas["attendu"] = {k: v for k, v in attendu.items() if k not in propres}
    try:
        if cas["attendu"]:
            ok, msg = etat_attendu(monde, aides)
            if not ok:
                soucis.append(msg)
    finally:
        cas["attendu"] = attendu
    return (False, " ; ".join(soucis)) if soucis else (True, "campagne conforme")


def camp_choix(monde, aides):
    """`ScenarioDuCombat2` : chaque (lieu, CAPO) donne un fichier existant ; les valeurs du tableau de p265 sont relues une a une."""
    import os
    from cards.pack.punisher_mcdc_2026.campaign import ScenarioDuCombat2, MANIGANCE_DU_LIEU, SOUS_FIFRE_DU_TRAFIQUANT
    voulu_lieu = {"Theater District": "art_museum_heist", "Financial District": "art_museum_heist", "Hell's Kitchen": "the_getaway",
                  "Lower East Side": "the_getaway", "Upper East Side": "the_raft_breakout", "Midtown": "the_raft_breakout",
                  "Chinatown": "protection_racket", "West Village": "stop_the_presses", "Soho": "stop_the_presses"}
    voulu_capo = {"Count Nefaria": "hobgoblin", "Ringmaster": "hobgoblin", "Mister Negative": "hobgoblin", "Nightshade": "hobgoblin",
                  "Crime-Master": "jigsaw", "Lady Yulan": "jigsaw", "The Rose": "jigsaw", "Diamondback": "jigsaw"}
    soucis = []
    if MANIGANCE_DU_LIEU != voulu_lieu:
        soucis.append("tableau des lieux different de p265")
    if SOUS_FIFRE_DU_TRAFIQUANT != voulu_capo:
        soucis.append("tableau des CAPO different de p265")
    for lieu in voulu_lieu:
        for capo in voulu_capo:
            for expert in (False, True):
                nom = ScenarioDuCombat2(lieu, capo, expert)
                if not nom or not os.path.exists(os.path.join("data", "scenarios", nom + ".json")):
                    soucis.append(f"{lieu} / {capo} / expert={expert} -> {nom!r} introuvable")
    if ScenarioDuCombat2("Atlantis", "Count Nefaria") != "" or ScenarioDuCombat2("Soho", "Inconnu") != "":
        soucis.append("un carnet incomplet doit rendre une chaine vide")
    return (False, " ; ".join(soucis[:6])) if soucis else (True, "144 combinaisons, tous les scenarios existent")


def camp_choix3(monde, aides):
    import os
    from cards.pack.punisher_mcdc_2026.campaign import ScenarioDuCombat3
    voulu = {"Jigsaw": "hobgoblin", "Hobgoblin": "jigsaw", "jigsaw": "hobgoblin"}
    soucis = []
    for nord, autre in voulu.items():
        for expert in (False, True):
            nom = ScenarioDuCombat3(nord, expert)
            attendu = f"punishment_{autre}" + ("_expert" if expert else "")
            if nom != attendu or not os.path.exists(os.path.join("data", "scenarios", nom + ".json")):
                soucis.append(f"{nord}/{expert} -> {nom!r} (attendu {attendu!r}, fichier present : {os.path.exists(os.path.join('data', 'scenarios', attendu + '.json'))})")
    if ScenarioDuCombat3("") != "" or ScenarioDuCombat3("Inconnu") != "":
        soucis.append("un carnet incomplet doit rendre une chaine vide")
    return (False, " ; ".join(soucis)) if soucis else (True, "les 4 scenarios du combat 3 existent")
'''

