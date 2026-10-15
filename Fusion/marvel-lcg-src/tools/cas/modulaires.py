# Cas test_capacites du bloc MODULAIRES de Skrull Menace (sk228-sk262) : Shaper of Worlds, les cinq ensembles
# d'ELITES (Crusader, Jazinda, Skymax, War Skrull, Xavin) et les alternatives Standard Skrull / Expert Skrull.
# Format identique a tools/test_capacites.py ; noms prefixes `[modulaires]` (filtre : `[modulaires]`).
#
# Conventions de ce fichier :
#  - SC : scenario d'ESSAI `sk_essai_modulaires` (Rhino + les six modulaires de ce bloc, voir
#    defs/inserer_modulaires.py). Le set entre donc dans le deck rencontre PAR LE CHEMIN REEL (`modular_sets`).
#  - le heros de test (Spider-Man, 01001) demarre en ALTER EGO ; `Puzzle.ChangeForm('01001b')` le met en forme HEROS.
#  - VIDE_DECK vide le deck rencontre (cartes de Rhino et des modulaires) avant de poser une position connue ;
#    `main_exclusive` fixe la main ; `payer_avec` + `payer_tout` imposent QUELLES cartes financent un cout colore
#    (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR).
import os

SC = "sk_essai_modulaires"
SC_STD = "sk_essai_skrull_standard"
SC_EXP = "sk_essai_skrull_expert"
HEROS = "Puzzle.ChangeForm('01001b')"
VIDE_DECK = "Puzzle.EmptyEncounterDeck()"
# Huit « Hard to Keep Down » (01104) : traitrises SANS icone de boost, pour que les cartes de boost retournees par les
# activations n'ajoutent aucun degat ni aucune menace (a placer APRES VIDE_DECK).
ZERO = "Puzzle.CreateEncounterDeck(" + ", ".join(["'01104'"] * 8) + ")"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[modulaires] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "modulaires_etat"), "attendu": attendu}
    cas.update(cle)
    if os.environ.get("MODULAIRES_SONDE"):
        # Mise au point : decrit l'etat au lieu de le verifier (le message d'echec porte la sonde).
        cas["verifier"] = "modulaires_dump"
    return cas


CAS = [
    # ===================================================================== composition des sets (chemin reel)
    _c("sets modulaires : les 6 sets entrent dans le deck rencontre (sauf le sbire et les fragments de Shaper, mis de cote)",
       "`modular_sets` du scenario d'essai : le chargement du set (data/encounter_sets/sk_*.json) cree les cartes ; "
       "Shaper et ses 4 fragments partent de cote a la mise en place, les 30 autres cartes restent dans le deck",
       [], [],
       {"compte_deck": {"sk229": 1, "sk231": 1, "sk232": 1, "sk233": 1, "sk234": 1, "sk235": 2, "sk236": 1, "sk237": 1,
                        "sk238": 1, "sk239": 2, "sk240": 1, "sk241": 1, "sk242": 2, "sk243": 1, "sk244": 2, "sk245": 1,
                        "sk246": 1, "sk247": 1, "sk248": 1, "sk249": 2, "sk250": 1, "sk251": 2, "sk252": 1, "sk253": 2,
                        "sk228": 0, "sk230a": 0, "sk230b": 0, "sk230c": 0, "sk230d": 0}}),
    _c("sk229 mise en place : le sbire Shaper of Worlds et les 4 fragments sont MIS DE COTE (insert du set)",
       "« During setup, set Shaper of Worlds minion and all four Cosmic Cube Fragment resources aside » ; "
       "Cosmic Cube Creation reste dans le deck rencontre",
       [], [], {"mis_de_cote_ids": ["sk228", "sk230a", "sk230b", "sk230c", "sk230d"], "compte_deck": {"sk229": 1}}),
    _c("Standard Skrull REMPLACE Standard : deck = Rhino + les 7 cartes Standard Skrull, aucune carte Standard",
       "scenario d'essai `encounter_sets: [sk_standard_skrull]` (livret : « you may replace them »)",
       [], [],
       {"compte_deck": {"sk254": 1, "sk255": 1, "sk256": 1, "sk257": 1, "sk258": 1, "sk259": 2, "01186": 0, "01187": 0,
                        "01188": 0, "01189": 0, "01190": 0, "sk260": 0}}, scenario=SC_STD),
    _c("Standard Skrull + Expert Skrull REMPLACENT Standard + Expert (mode expert) : 7 + 3 cartes, aucune carte officielle",
       "scenario d'essai expert `encounter_sets: [sk_standard_skrull, sk_expert_skrull]`",
       [], [],
       {"compte_deck": {"sk254": 1, "sk255": 1, "sk256": 1, "sk257": 1, "sk258": 1, "sk259": 2, "sk260": 1, "sk261": 1,
                        "sk262": 1, "01186": 0, "01191": 0, "01192": 0, "01193": 0}}, scenario=SC_EXP),
    # ===================================================================== Shaper of Worlds (sk228-sk230d)
    _c("sk228 Reponse forcee : un joueur attaque Shaper of Worlds -> la carte est melangee dans SON deck",
       "`AfterUnitBeAttacked(ForcedResponse, \"This\")` + `Faces.ShuffleAllTo([this], joueur.player_deck)` ; PV infinis : il ne tombe jamais",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.PutIntoPlay('sk228')"], ["Puzzle.Attack('01001a')"],
       {"hors_jeu": ["sk228"], "deck_joueur_ids": ["sk228"]}, cibles=["sk228"], main_exclusive=["01088"]),
    _c("sk228 Reponse forcee, TEMOIN : attaquer un AUTRE sbire ne melange pas Shaper (il reste en jeu)",
       "ligne de base du precedent : seule une attaque CONTRE Shaper declenche",
       [HEROS, "Puzzle.PutIntoPlay('sk228')", "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Attack('01001a')"],
       {"en_jeu": ["sk228"], "degats": [["01101", 2]]}, cibles=["01101"], main_exclusive=["01088"]),
    _c("sk228 Interruption forcee : Shaper entre en MAIN (pioche) -> 4 cartes du deck rencontre defaussees, Shaper en jeu, main vide",
       "`AfterCardEnterHand(ForcedInterrupt, \"This\")` + `Worlds.DiscardEncounterCards(4)` + `PutIntoPlay(joueur)` ; la carte du dessus est la derniere creee ; Shaper est la seule carte du deck du joueur",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01099', '01100', '01101', '01102', '01103')",
        "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('sk228')"], ["Puzzle.Draw(1)"],
       {"en_jeu": ["sk228"], "defausse_rencontre": ["01103", "01102", "01101", "01100"], "absent_main": ["sk228"],
        "dans_deck_rencontre": ["01099"], "taille_deck_rencontre": 1}),
    _c("sk228 Interruption forcee, TEMOIN : une carte ordinaire piochee ne declenche rien (rien n'est defausse du deck rencontre)",
       "ligne de base du precedent : seule Shaper defausse 4 cartes",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01099', '01100', '01101', '01102', '01103')",
        "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088')"], ["Puzzle.Draw(1)"],
       {"en_main": ["01088"], "taille_deck_rencontre": 5}),
    _c("sk229 Cosmic Cube Creation revelee : le Shaper MIS DE COTE entre en jeu engage ; menace 2 + Hinder 4 ; icone Acceleration",
       "« Put the set-aside Shaper of Worlds into play engaged with you » ; `desc` : StartingThreat 2, Hinder 4*, Acceleration 1",
       [], ["Puzzle.Reveal('sk229')"],
       {"en_jeu": ["sk229", "sk228"], "menace": [["sk229", 6]], "icones": [["Acceleration", 1]],
        "mis_de_cote_ids": ["sk230a", "sk230b", "sk230c", "sk230d"]}),
    _c("sk229 Quand vaincu : le joueur choisit un fragment MIS DE COTE et le melange dans son deck",
       "`WhenSchemeBeDefeated(WhenDefeated)` + `AskChooseFace` sur les fragments de cote + `ShuffleAllTo(joueur.player_deck)`",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.PutIntoPlay('sk229')", "Puzzle.SetThreat('sk229', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"hors_jeu": ["sk229"], "deck_joueur_ids": ["sk230a"], "mis_de_cote_ids": ["sk230b", "sk230c", "sk230d"]},
       cibles=["sk229"], main_exclusive=["01088"]),
    _c("sk229 Quand vaincu a DEUX joueurs : CHAQUE joueur choisit son propre fragment (un fragment pris n'est plus offert au suivant)",
       "`Players.ForEachPlayer` + `AskChooseFace` sur les fragments restants ; le pilote prend la premiere option : a puis b",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.PutIntoPlay('sk229')", "Puzzle.SetThreat('sk229', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"hors_jeu": ["sk229"], "fragments_dans_decks": [1, 1], "fragments_de_cote": 2},
       cibles=["sk229"], main_exclusive=["01088"], heros2="captain_marvel"),
    _c("sk231 Crusader revele a DEUX joueurs : seuls les personnages du joueur a qui il est revele subissent le degat",
       "« each character YOU control » : l'identite de l'autre joueur est intacte (1 degat au total)",
       [], ["Puzzle.Reveal('sk231')"], {"degats_total_identites": 1, "degats_identite": 1}, heros2="captain_marvel"),
    _c("sk230a Cosmic Cube Fragment (YYY) : une ressource qui vaut TROIS energies (paie Crisis Interdiction, cout 2)",
       "ressource sans texte : 3 icones energie du `desc.RES` ; le cas mesure la menace retiree par l'evenement paye avec le fragment",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetThreat('01097b', 4)"], [], {"menace": [["01097b", 2]], "defausse": ["01012"]},
       main_exclusive=["sk230a", "01012"], jouer=["01012"], cibles=["01097b"], payer_avec=["sk230a"], surpayer=True),
    _c("sk230b Cosmic Cube Fragment (BBB) : trois icones MENTALES (paie le cout [mental][mental] de Distracted, qui se defausse)",
       "`desc.RES = BBB` ; Distracted (sk147, Paibok) : « Spend [mental][mental] → discard this card »",
       [HEROS, "Puzzle.PutIntoPlay('sk147')"], ["Puzzle.Action('sk147', 'HeroAction')"], {"hors_jeu": ["sk147"]},
       main_exclusive=["sk230b"], payer_avec=["sk230b"], surpayer=True),
    _c("sk230c Cosmic Cube Fragment (RRR) : trois icones PHYSIQUES (paie le cout [physical] de Skrull Energy Gun, qui change d'ennemi)",
       "`desc.RES = RRR` ; sk237 : « Spend a [physical] resource → attach this card to another enemy »",
       [HEROS, "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk237')", "Puzzle.Attach('sk237', 'sk113')"],
       ["Puzzle.Action('sk237', 'HeroAction')"], {"accroche_a": [["sk237", "01094"]]},
       main_exclusive=["sk230c"], payer_avec=["sk230c"], surpayer=True),
    _c("sk230d Cosmic Cube Fragment (RBY) : trois icones de TROIS couleurs (paie Swinging Web Kick, cout 3 : 8 degats a Rhino)",
       "`desc.RES = RBY` : un seul fragment finance un evenement de cout 3",
       [HEROS], [], {"degats": [["01094", 8]], "defausse": ["01005"]},
       main_exclusive=["sk230d", "01005"], jouer=["01005"], cibles=["01094"], payer_avec=["sk230d"], surpayer=True),
    # ===================================================================== Crusader (sk231-sk235)
    _c("sk231 Crusader revele : 1 degat a CHAQUE personnage qu'on controle (identite et allie), aucune carte de boost si personne ne tombe",
       "`GetControlCharacters()` + `TakeDamage(this, 1)` ; personne n'est vaincu -> 0 carte de boost",
       ["Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Reveal('sk231')"],
       {"degats_identite": 1, "degats": [["01002", 1]], "boosts_mechant": 0}),
    _c("sk231 Crusader revele : un allie VAINCU par ce degat -> 1 carte de boost face cachee au mechant",
       "Black Cat (2 PV) a deja 1 degat : le coup l'abat ; « for each character defeated this way »",
       ["Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.Damage('01002', 1)"], ["Puzzle.Reveal('sk231')"],
       {"hors_jeu": ["01002"], "degats_identite": 1, "boosts_mechant": 1}),
    _c("sk231 Crusader revele : DEUX allies vaincus -> 2 cartes de boost",
       "« 1 facedown boost card FOR EACH character defeated » : Black Cat et Mockingbird (3 PV, 2 degats deja)",
       ["Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.Damage('01002', 1)",
        "Puzzle.PutIntoPlay('01083', under_control=True)", "Puzzle.Damage('01083', 2)"], ["Puzzle.Reveal('sk231')"],
       {"hors_jeu": ["01002", "01083"], "boosts_mechant": 2}),
    _c("sk231 Boost : la carte retournee en boost entre en jeu ENGAGEE avec le joueur",
       "`WhenCardBecomeBoost(\"This\")` + `PutIntoPlay(joueur)` ; le mechant active (alter-ego : complote) et retourne Crusader",
       [], ["Puzzle.Boost('sk231')"], {"en_jeu": ["sk231"]}),
    _c("sk232 Enemy Adaptation revelee avec un sbire SKRULL en jeu : elle s'attache a lui (+1 MNG, +1 ATQ)",
       "`AttacherAUnSbireSkrull` : le sbire SKRULL (Skrull Commander 2/2) devient 3/3 ; le mechant reste intact",
       ["Puzzle.PutIntoPlay('sk113')"], ["Puzzle.Reveal('sk232')"],
       {"accroche_a": [["sk232", "sk113"]], "attributs_carte": [["sk113", "attack", 1], ["sk113", "scheme", 1]]}),
    _c("sk232 Enemy Adaptation : SANS sbire SKRULL (un sbire non-Skrull est en jeu), elle s'attache au MECHANT",
       "« If you cannot, attach to the villain » ; Hydra Mercenary n'est pas SKRULL",
       ["Puzzle.PutIntoPlay('01101')"], ["Puzzle.Reveal('sk232')"],
       {"accroche_a": [["sk232", "01094"]]}),
    _c("sk232 Enemy Adaptation : « You cannot defend against attached enemy's attacks » -> le heros ne peut pas defendre",
       "`UnitCannotDefend(Unit2, \"AttachedEnemy\")` ; Skrull Commander 3 ATQ contre DEF 3 : sans la carte le heros defend (0 degat), avec elle 3",
       [HEROS, VIDE_DECK, "Puzzle.CreateEncounterDeck('01104', '01104')", "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk232')",
        "Puzzle.Attach('sk232', 'sk113')"], ["Puzzle.Attack('sk113')"],
       {"degats_identite": 3}, main_exclusive=["01088"]),
    _c("sk232 Enemy Adaptation, TEMOIN : sans l'attachement le heros DEFEND et ne subit rien (Skrull Commander 2 ATQ contre DEF 3)",
       "ligne de base du precedent",
       [HEROS, VIDE_DECK, "Puzzle.CreateEncounterDeck('01104', '01104')", "Puzzle.PutIntoPlay('sk113')"], ["Puzzle.Attack('sk113')"],
       {"degats_identite": 0}, main_exclusive=["01088"]),
    _c("sk232 Action de heros : donne 1 carte de boost au mechant -> la carte est defaussee",
       "`PlayerActionToDiscardThis(HeroAction)` + cout = `DonnerBoostAuMechant` ; le « → » separe cout et defausse",
       [HEROS, "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk232')", "Puzzle.Attach('sk232', 'sk113')"],
       ["Puzzle.Action('sk232', 'HeroAction')"], {"hors_jeu": ["sk232"], "boosts_mechant": 1}, main_exclusive=["01088"]),
    _c("sk233 Freedom Ring revelee avec Crusader en jeu : elle s'attache a lui, qui devient VILLAINOUS",
       "`AttachToFaceWhenPutIntoPlay(name=Crusader)` + `GiveKeywordToAttached(Minion, villainous=1)`",
       ["Puzzle.PutIntoPlay('sk231')"], ["Puzzle.Reveal('sk233')"],
       {"accroche_a": [["sk233", "sk231"]], "villainous": [["sk231", True]]}),
    _c("sk233 Freedom Ring, Crusader ABSENT : defausse jusqu'a un sbire, le met en jeu engage et s'y attache (Villainous)",
       "deck : Hydra Mercenary sous une traitrise ; la traitrise est defaussee, le sbire entre en jeu",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01099', '01101', '01104')"], ["Puzzle.Reveal('sk233')"],
       {"en_jeu": ["01101"], "accroche_a": [["sk233", "01101"]], "villainous": [["01101", True]],
        "defausse_rencontre": ["01104"]}),
    _c("sk233 Freedom Ring, Crusader absent et AUCUN sbire dans le deck : 1 carte de boost face cachee au mechant",
       "« If you cannot, give the villain 1 facedown boost card »",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01099', '01104')"], ["Puzzle.Reveal('sk233')"],
       {"boosts_mechant": 1}),
    _c("sk234 Spy Training revelee : un allie qu'on controle est VAINCU et le mechant recoit 1 carte de boost ; menace 3, Hazard",
       "`ForChoiceAbility(...).SetTarget(Ally)` + `DefeatUnits` ; `desc` : StartingThreat 3*, Hazard 1",
       ["Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Reveal('sk234')"],
       {"hors_jeu": ["01002"], "boosts_mechant": 1, "menace": [["sk234", 3]], "icones": [["Hazard", 1]]}),
    _c("sk234 Spy Training revelee SANS allie : la carte de boost est donnee quand meme (lecture : effets independants)",
       "defs/modulaires_questions.md, question 1",
       [], ["Puzzle.Reveal('sk234')"], {"boosts_mechant": 1}),
    _c("sk235 Rivals to the End : le sbire choisi attaque le heros DEUX fois de suite (Skrull Commander ATQ 2 x 2 = 4 degats)",
       "`DoAttackYou` deux fois ; chaque attaque retourne une carte de boost (deck de traitrises vides) ; heros sans defense",
       [HEROS, VIDE_DECK, "Puzzle.CreateEncounterDeck('01104', '01104', '01104')", "Puzzle.PutIntoPlay('sk113')"],
       ["Puzzle.Reveal('sk235')"], {"degats_identite": 4}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk235 Rivals to the End en ALTER-EGO : aucune attaque -> 1 carte de boost par personnage qu'on controle (identite + allie = 2)",
       "« If no attack was made this way, give the villain 1 facedown boost card for each character you control »",
       ["Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Reveal('sk235')"],
       {"boosts_mechant": 2, "degats_identite": 0}),
    _c("sk235 Rivals to the End, aucun sbire en jeu (heros) : aucune attaque -> 1 carte de boost (identite seule)",
       "meme repli, sans sbire a choisir",
       [HEROS], ["Puzzle.Reveal('sk235')"], {"boosts_mechant": 1}),
    # ===================================================================== Jazinda (sk236-sk240)
    _c("sk236 Jazinda en jeu : le MECHANT gagne +1 MNG",
       "`GiveKeywordToInPlayWhenApplyThis(Villain, scheme=1)` : Rhino 1 -> 2",
       ["Puzzle.PutIntoPlay('sk236')"], [], {"attributs_carte": [["01094", "scheme", 1]]}),
    _c("sk236 Jazinda, TEMOIN : sans elle le mechant garde son MNG imprime",
       "ligne de base du precedent",
       [], [], {"attributs_carte": [["01094", "scheme", 0]]}),
    _c("sk236 Boost : la carte retournee en boost entre en jeu ENGAGEE avec le joueur",
       "`WhenCardBecomeBoost(\"This\")` + `PutIntoPlay(joueur)`",
       [], ["Puzzle.Boost('sk236')"], {"en_jeu": ["sk236"]}),
    _c("sk237 Skrull Energy Gun revelee avec un sbire SKRULL en jeu : elle s'attache a lui (+1 ATQ)",
       "`AttacherAUnSbireSkrull` ; Skrull Commander 2 -> 3",
       ["Puzzle.PutIntoPlay('sk113')"], ["Puzzle.Reveal('sk237')"],
       {"accroche_a": [["sk237", "sk113"]], "attributs_carte": [["sk113", "attack", 1]]}),
    _c("sk237 Skrull Energy Gun : les attaques de l'hote SKRULL gagnent OVERKILL (Black Cat, 2 PV, defend contre ATQ 3 : l'exces 1 passe au heros)",
       "`UnitAttackGainKeyword(\"AttachedEnemy\", overkill=True)` sous condition SKRULL ; sans la carte aucun exces",
       [HEROS, VIDE_DECK, "Puzzle.CreateEncounterDeck('01104', '01104')", "Puzzle.PutIntoPlay('01002', under_control=True)",
        "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk237')", "Puzzle.Attach('sk237', 'sk113')"],
       ["Puzzle.Attack('sk113', defender='01002')"], {"hors_jeu": ["01002"], "degats_identite": 1}, main_exclusive=["01088"]),
    _c("sk237 Skrull Energy Gun, TEMOIN : sans l'arme, ATQ 2 contre Black Cat (2 PV) : pas d'exces, le heros est intact",
       "ligne de base du precedent",
       [HEROS, VIDE_DECK, "Puzzle.CreateEncounterDeck('01104', '01104')", "Puzzle.PutIntoPlay('01002', under_control=True)",
        "Puzzle.PutIntoPlay('sk113')"],
       ["Puzzle.Attack('sk113', defender='01002')"], {"hors_jeu": ["01002"], "degats_identite": 0}, main_exclusive=["01088"]),
    _c("sk237 Skrull Energy Gun : PIERCING -> l'attaque ignore la carte Robuste de Volstagg et lui inflige ses 3 degats",
       "`piercing=True` ; Volstagg (Toughness : entre robuste) defend, ATQ 2 + 1",
       [HEROS, VIDE_DECK, "Puzzle.CreateEncounterDeck('01104', '01104')", "Puzzle.PutIntoPlay('21193', under_control=True)",
        "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk237')", "Puzzle.Attach('sk237', 'sk113')"],
       ["Puzzle.Attack('sk113', defender='21193')"], {"degats": [["21193", 3]], "statuts_absents": [["21193", "Tough"]]},
       main_exclusive=["01088"]),
    _c("sk237 Skrull Energy Gun, TEMOIN : sans l'arme, la carte Robuste de Volstagg absorbe l'attaque (0 degat)",
       "ligne de base du precedent",
       [HEROS, VIDE_DECK, "Puzzle.CreateEncounterDeck('01104', '01104')", "Puzzle.PutIntoPlay('21193', under_control=True)",
        "Puzzle.PutIntoPlay('sk113')"],
       ["Puzzle.Attack('sk113', defender='21193')"], {"degats": [["21193", 0]]}, main_exclusive=["01088"]),
    _c("sk237 Skrull Energy Gun : RANGED -> la Riposte de Volstagg est ignoree (le sbire ne perd aucun PV)",
       "`ranged=True` : Volstagg (Retaliate 1) defend ; sans l'arme Skrull Commander subirait 1 degat",
       [HEROS, VIDE_DECK, "Puzzle.CreateEncounterDeck('01104', '01104')", "Puzzle.PutIntoPlay('21193', under_control=True)",
        "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk237')", "Puzzle.Attach('sk237', 'sk113')"],
       ["Puzzle.Attack('sk113', defender='21193')"], {"degats": [["sk113", 0]]}, main_exclusive=["01088"]),
    _c("sk237 Skrull Energy Gun, TEMOIN : sans l'arme, la Riposte de Volstagg blesse Skrull Commander (1 degat)",
       "ligne de base du precedent",
       [HEROS, VIDE_DECK, "Puzzle.CreateEncounterDeck('01104', '01104')", "Puzzle.PutIntoPlay('21193', under_control=True)",
        "Puzzle.PutIntoPlay('sk113')"],
       ["Puzzle.Attack('sk113', defender='21193')"], {"degats": [["sk113", 1]]}, main_exclusive=["01088"]),
    _c("sk237 Skrull Energy Gun sur un ennemi NON SKRULL (le mechant Rhino) : ni overkill ni piercing ni ranged, seulement +1 ATQ",
       "« While attached to a SKRULL enemy » : Rhino 2 + 1 = 3 contre Black Cat (2 PV) : aucun exces, heros intact",
       [HEROS, VIDE_DECK, "Puzzle.CreateEncounterDeck('01104', '01104')", "Puzzle.PutIntoPlay('01002', under_control=True)",
        "Puzzle.PutIntoPlay('sk237')", "Puzzle.Attach('sk237', '01094')"],
       ["Puzzle.Attack('01094', defender='01002')"], {"hors_jeu": ["01002"], "degats_identite": 0, "attributs_carte": [["01094", "attack", 1]]},
       main_exclusive=["01088"]),
    _c("sk237 Action de heros : depenser une ressource [physical] -> la carte passe a un AUTRE ennemi (le mechant)",
       "`WhenInYourPlayTurn(HeroAction).SetCost(Cost(\"R\")).SetTarget(Enemy, hors hote)` + `AttachTo2` ; Strength (RR) paie",
       [HEROS, "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk237')", "Puzzle.Attach('sk237', 'sk113')"],
       ["Puzzle.Action('sk237', 'HeroAction')"], {"accroche_a": [["sk237", "01094"]]},
       main_exclusive=["01090"], payer_avec=["01090"], surpayer=True, cibles=["01094"]),
    _c("sk237 Action de heros SANS choisir la cible (le pilote prend la premiere) : l'hote n'est JAMAIS une cible offerte",
       "le filtre « another enemy » exclut l'hote ; deux ennemis seulement (Skrull Commander porteur, Rhino) : la seule cible est Rhino",
       [HEROS, "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk237')", "Puzzle.Attach('sk237', 'sk113')"],
       ["Puzzle.Action('sk237', 'HeroAction')"], {"accroche_a": [["sk237", "01094"]]},
       main_exclusive=["01090"], payer_avec=["01090"], surpayer=True),
    _c("sk237 Action de heros, aucun AUTRE ennemi (la carte est sur le mechant, seul ennemi) : l'action n'est PAS offerte",
       "condition `un_autre_ennemi_existe` : pas de coup a vide",
       [HEROS, "Puzzle.PutIntoPlay('sk237')", "Puzzle.Attach('sk237', '01094')"], [],
       {"action_offerte": [["sk237", 0]]}, main_exclusive=["01090"]),
    _c("sk238 Sy-Torak Gem revelee avec Jazinda en jeu : elle s'attache a elle (+1 ATQ, +3 PV)",
       "`AttachToFaceWhenPutIntoPlay(name=Jazinda)` + `GiveKeywordToAttached(Unit2, health=3)` : Jazinda 5 -> 8 PV",
       ["Puzzle.PutIntoPlay('sk236')"], ["Puzzle.Reveal('sk238')"],
       {"accroche_a": [["sk238", "sk236"]], "attributs_carte": [["sk236", "health", 3], ["sk236", "attack", 1]]}),
    _c("sk238 Sy-Torak Gem, Jazinda ABSENTE : elle s'attache au MECHANT (Rhino 14 -> 17 PV)",
       "« If you cannot, attach to the villain » ; « attached CHARACTER gets +3 hit points » vaut aussi pour le mechant",
       [], ["Puzzle.Reveal('sk238')"],
       {"accroche_a": [["sk238", "01094"]], "attributs_carte": [["01094", "health", 3]]}),
    _c("sk238 Action de heros : carte de boost au mechant ET une ressource [energy] -> la carte est defaussee",
       "`SetCost(Cost(\"Y\"))` + `SetCostFunc(Custom)` : les DEUX parties du cout ; Energy (YY) paie",
       [HEROS, "Puzzle.PutIntoPlay('sk236')", "Puzzle.PutIntoPlay('sk238')", "Puzzle.Attach('sk238', 'sk236')"],
       ["Puzzle.Action('sk238', 'HeroAction')"], {"hors_jeu": ["sk238"], "boosts_mechant": 1},
       main_exclusive=["01088"], payer_avec=["01088"], surpayer=True),
    _c("sk239 Stealing for the Empire revelee : defausse jusqu'a un attachement, le revele, menace sur le complot PRINCIPAL = ses icones (Sy-Torak Gem : 3)",
       "`DiscardEncounterCardsUntil(card_type=Attachment)` + `Reveal` + `CountTotalBoostIcons` ; une traitrise est defaussee au passage ; Acceleration 1",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01106', 'sk238', '01104')"], ["Puzzle.Reveal('sk239')"],
       {"menace": [["01097b", 3], ["sk239", 3]], "en_jeu": ["sk238"], "defausse_rencontre": ["01104"], "icones": [["Acceleration", 1]]}),
    _c("sk239 Stealing for the Empire : attachement a 2 icones (Charge) -> 2 menaces sur le complot principal",
       "meme chaine, nombre d'icones different (preuve que le chiffre est lu et non code en dur)",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01106', '01099')"], ["Puzzle.Reveal('sk239')"],
       {"menace": [["01097b", 2]], "en_jeu": ["01099"]}),
    _c("sk239 Stealing for the Empire, aucun attachement dans le deck : pas de menace sur le complot principal",
       "tout le deck est defausse sans trouver d'attachement ; rien n'est place",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01106', '01104')"], ["Puzzle.Reveal('sk239')"],
       {"menace": [["01097b", 0]]}),
    _c("sk240 Skrull of Royal Blood : les cartes de la defausse rencontre au MAXIMUM d'icones de boost (2 : Charge et Ivory Horn) retournent dans le deck",
       "`GetEncounterDiscardPileCards` + `CountTotalBoostIcons` + `ShuffleAllTo` ; Hydra Mercenary (1) et la traitrise (0) restent",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01106', '01105', '01107', '01108')",
        "Puzzle.CreateEncounterDiscardPile('01099', '01100', '01101', '01104')"], ["Puzzle.Reveal('sk240')"],
       {"defausse_rencontre": ["01101", "01104"], "dans_deck_rencontre": ["01099", "01100"]}),
    _c("sk240 Skrull of Royal Blood : surge natif -> la carte du dessus du deck est revelee aussi",
       "`desc.Surge = 1` ; Hydra Mercenary au-dessus du deck entre en jeu",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01106', '01101')"], ["Puzzle.Reveal('sk240')"],
       {"carte_du_surge": "01101", "en_jeu": ["01101"]}),
    # ===================================================================== Skymax (sk241-sk244)
    _c("sk241 Skymax revele : TOUS les sbires de la defausse rencontre retournent dans le deck (la traitrise reste)",
       "`GetEncounterDiscardPileCards` filtre `Minion` + `ShuffleAllTo`",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01106', '01105')", "Puzzle.CreateEncounterDiscardPile('01101', '01103', '01104')"],
       ["Puzzle.Reveal('sk241')"],
       {"defausse_rencontre": ["01104"], "dans_deck_rencontre": ["01101", "01103"]}),
    _c("sk241 Skymax revele, TEMOIN : une defausse sans sbire ne bouge pas",
       "ligne de base : rien n'est melange",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01106', '01105')", "Puzzle.CreateEncounterDiscardPile('01104')"],
       ["Puzzle.Reveal('sk241')"], {"defausse_rencontre": ["01104"], "taille_deck_rencontre": 2}),
    _c("sk241 Boost : la carte retournee en boost entre en jeu ENGAGEE avec le joueur",
       "`WhenCardBecomeBoost(\"This\")` + `PutIntoPlay(joueur)`",
       [], ["Puzzle.Boost('sk241')"], {"en_jeu": ["sk241"]}),
    _c("sk242 Changing Appearance revelee avec un sbire SKRULL : elle s'attache a lui (+2 MNG)",
       "`AttacherAUnSbireSkrull` ; Skrull Commander MNG 2 -> 4",
       ["Puzzle.PutIntoPlay('sk113')"], ["Puzzle.Reveal('sk242')"],
       {"accroche_a": [["sk242", "sk113"]], "attributs_carte": [["sk113", "scheme", 2]]}),
    _c("sk242 Changing Appearance : l'ennemi attache NE PEUT PAS ETRE ATTAQUE (le heros frappe Rhino a la place, Skrull Commander est intact)",
       "`UnitCannotBeAttacked(\"AttachedEnemy\")`",
       [HEROS, VIDE_DECK, "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk242')", "Puzzle.Attach('sk242', 'sk113')"],
       ["Puzzle.Attack('01001a')"], {"degats": [["sk113", 0]]}, cibles=["sk113"], main_exclusive=["01088"]),
    _c("sk242 Changing Appearance, TEMOIN : sans l'attachement le heros attaque Skrull Commander (2 degats)",
       "ligne de base du precedent",
       [HEROS, "Puzzle.PutIntoPlay('sk113')"], ["Puzzle.Attack('01001a')"], {"degats": [["sk113", 2]]},
       cibles=["sk113"], main_exclusive=["01088"]),
    _c("sk242 Interruption forcee : l'ennemi attache qui allait attaquer COMPLOTE a la place (MNG 2 + 2 = 4 menaces), puis la carte est defaussee",
       "`WhenUnitWouldAttack(ForcedInterrupt, \"AttachedEnemy\")` + `DoSchemeInstead` + `DiscardAll([this])` ; le heros ne subit rien",
       [HEROS, VIDE_DECK, ZERO, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('sk113')",
        "Puzzle.PutIntoPlay('sk242')", "Puzzle.Attach('sk242', 'sk113')"],
       ["Puzzle.Attack('sk113')"], {"degats_identite": 0, "menace": [["01097b", 4]], "hors_jeu": ["sk242"]}),
    _c("sk242 Interruption forcee, TEMOIN : sans l'attachement le meme sbire ATTAQUE (2 degats au heros, aucune menace)",
       "ligne de base du precedent (heros sans defense)",
       [HEROS, VIDE_DECK, "Puzzle.CreateEncounterDeck('01104', '01104')", "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('sk113')"],
       ["Puzzle.Attack('sk113')"], {"degats_identite": 2, "menace": [["01097b", 0]]}, passer_sur_option="Defense"),
    _c("sk243 Surprising Alliance : un allie DEFAUSSE de la main entre en jeu engage comme SBIRE (SCH = THW imprime 1), il ne va pas a la defausse",
       "`WhenCardWouldDiscard` + `SetBeInstead` + `TreatAsMinion` (gabarit « Minion », SCH = THW)",
       [HEROS, "Puzzle.PutIntoPlay('sk243')"], ["Puzzle.EmptyHand()"],
       {"en_jeu": ["01002"], "type_en_jeu": [["01002", "Minion"]], "attributs_carte": [["01002", "scheme", 0]]}, main_exclusive=["01002"]),
    _c("sk243 Surprising Alliance, TEMOIN : sans le complot l'allie defausse va a la defausse du joueur",
       "ligne de base du precedent (`Puzzle.EmptyHand` defausse toute la main)",
       [HEROS], ["Puzzle.EmptyHand()"], {"hors_jeu": ["01002"], "defausse": ["01002"]}, main_exclusive=["01002"]),
    _c("sk243 Surprising Alliance, TEMOIN : un evenement defausse de la main (Backflip) va a la defausse normalement",
       "« discards an ALLY from their hand » : seule une carte Allie est detournee",
       [HEROS, "Puzzle.PutIntoPlay('sk243')"], ["Puzzle.EmptyHand()"], {"defausse": ["01003"]}, main_exclusive=["01003"]),
    _c("sk244 Shape Alteration : retire Sonne et Desoriente des ennemis SKRULL et leur donne Robuste ; un ennemi non-Skrull est intact",
       "`DiscardStunned/Confused(rule=\"All\")` + `GiveStatus(\"Tough\")` ; Hydra Mercenary (non Skrull) garde son statut Sonne",
       [VIDE_DECK, "Puzzle.PutIntoPlay('sk113')", "Puzzle.Stun('sk113')", "Puzzle.Confuse('sk113')", "Puzzle.PutIntoPlay('01101')", "Puzzle.Stun('01101')"],
       ["Puzzle.Reveal('sk244')"],
       {"statuts": [["sk113", "Tough"], ["01101", "Stunned"]], "statuts_absents": [["sk113", "Stunned"], ["sk113", "Confused"], ["01101", "Tough"]]}),
    _c("sk244 Shape Alteration : aucun ennemi SKRULL en jeu -> SURGE (la carte du dessus est revelee)",
       "`ThisCardGainSurge` ; Hydra Mercenary au-dessus du deck entre en jeu",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01106', '01101')"], ["Puzzle.Reveal('sk244')"],
       {"carte_du_surge": "01101", "en_jeu": ["01101"]}),
    _c("sk244 Shape Alteration, TEMOIN : avec un ennemi SKRULL en jeu, PAS de surge (le deck n'est pas touche)",
       "ligne de base du precedent",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01106', '01101')", "Puzzle.PutIntoPlay('sk113')"], ["Puzzle.Reveal('sk244')"],
       {"dans_deck_rencontre": ["01101", "01106"], "taille_deck_rencontre": 2}),
    _c("sk244 Boost : un ennemi SKRULL (au choix du joueur) recoit une carte Robuste",
       "`WhenCardBecomeBoost` + `ChooseAbilities(...SetTarget(Enemy, trait=SKRULL, canbe_tough=True))`",
       ["Puzzle.PutIntoPlay('sk113')"], ["Puzzle.Boost('sk244')"], {"statuts": [["sk113", "Tough"]]}),
    # ===================================================================== War Skrull (sk245-sk249)
    _c("sk245 Reponse forcee : War Skrull attaque le joueur -> les 2 cartes du dessus de SON deck sont defaussees (3 -> 1)",
       "`AfterUnitAttackYou(ForcedResponse, \"This\")` + `DiscardDeckTopCards(2)` ; attaque sans defense",
       [HEROS, VIDE_DECK, ZERO, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', '01090', '01091')", "Puzzle.PutIntoPlay('sk245')"],
       ["Puzzle.Attack('sk245')"], {"taille_deck_joueur": 1, "degats_identite": 2}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk245 Reponse forcee, TEMOIN : l'attaque d'un AUTRE sbire ne defausse rien (le deck garde ses 3 cartes)",
       "ligne de base du precedent",
       [HEROS, VIDE_DECK, ZERO, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01089', '01090', '01091')", "Puzzle.PutIntoPlay('sk113')"],
       ["Puzzle.Attack('sk113')"], {"taille_deck_joueur": 3}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk245 Boost : la carte retournee en boost entre en jeu ENGAGEE avec le joueur",
       "`WhenCardBecomeBoost(\"This\")` + `PutIntoPlay(joueur)`",
       [], ["Puzzle.Boost('sk245')"], {"en_jeu": ["sk245"]}),
    _c("sk246 Impostor (War Skrull) revele : un allie devient un sbire SKRULL engage (meme code que sk098, `ability_link`)",
       "`ability_link: sk098` : le texte est identique ; Black Cat est la seule candidate",
       ["Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Reveal('sk246')"],
       {"accroche_a": [["sk246", "skrull_minion"]], "type_en_jeu": [["skrull_minion", "Minion"]], "traits_de": [["skrull_minion", "SKRULL"]]}),
    _c("sk246 Impostor (War Skrull) revele SANS allie : le mechant complote (menace sur le complot principal)",
       "« Otherwise, the villain schemes » ; alter-ego : Rhino MNG 1",
       [VIDE_DECK, ZERO], ["Puzzle.Reveal('sk246')"], {"menace": [["01097b", 1]]}),
    _c("sk247 Skrull Commander (War Skrull) : les AUTRES sbires SKRULL gagnent +1 ATQ (meme code que sk113, `ability_link`)",
       "`ability_link: sk113` ; Skrull Soldier 2 -> 3, le Commander lui-meme reste a 2",
       ["Puzzle.PutIntoPlay('sk247')", "Puzzle.PutIntoPlay('sk114')"], [],
       {"attributs_carte": [["sk114", "attack", 1], ["sk247", "attack", 0]]}),
    _c("sk247 Skrull Commander (War Skrull) Boost : si l'activation est une attaque, +2 icones (1 + 2 = 3 icones : Rhino ATQ 2 + 3 = 5 degats)",
       "`WhenCardBecomeBoost(\"This\", during_attack=True)` + `GainBoostIcon(2)` via le lien ; heros sans defense",
       [HEROS, "Puzzle.EmptyHand()"], ["Puzzle.Boost('sk247')"], {"degats_identite": 5}, passer_sur_option="Defense"),
    _c("sk248 Skrull Geneticist Boost : le joueur se distribue 1 carte rencontre face cachee",
       "`player.DealEncounterCards(1)`",
       [], ["Puzzle.Boost('sk248')"], {"cartes_distribuees": 1}),
    _c("sk248 Skrull Geneticist en jeu : icone HAZARD (1 carte rencontre de plus a la phase du mechant)",
       "icone Hazard dans `desc`, lue nativement (fiche mots-cles/hazard.md)",
       ["Puzzle.PutIntoPlay('sk248')"], [], {"icones": [["Hazard", 1]]}),
    _c("sk249 Cloning Program : chaque sbire SKRULL active UNE FOIS DE PLUS a l'etape 2 de la phase du mechant (Rhino 2 + Commander 2 + 2 = 6)",
       "`AfterEnemyActivationEnd` filtre sur l'etape 2 ; phase du mechant complete, heros sans defense, boosts a 0 icone",
       [HEROS, VIDE_DECK, ZERO, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk249')"], ["Puzzle.RunVillainPhase()"],
       {"degats_identite": 6}, passer_sur_option="Defense"),
    _c("sk249 Cloning Program, TEMOIN : sans le complot la meme phase fait 4 degats (Rhino 2 + Commander 2)",
       "ligne de base du precedent",
       [HEROS, ZERO, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('sk113')"], ["Puzzle.RunVillainPhase()"],
       {"degats_identite": 4}, passer_sur_option="Defense"),
    _c("sk249 Cloning Program, DEUX exemplaires : deux activations de plus (2 + 2 + 2 + 2 = 8)",
       "chaque exemplaire ajoute une activation (cumul)",
       [HEROS, ZERO, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk249')", "Puzzle.PutIntoPlay('sk249')"],
       ["Puzzle.RunVillainPhase()"], {"degats_identite": 8}, passer_sur_option="Defense"),
    _c("sk249 Cloning Program : une attaque HORS de l'etape 2 (Puzzle.Attack) n'est pas doublee (2 degats)",
       "« during the step two of the villain phase »",
       [HEROS, VIDE_DECK, ZERO, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk249')"], ["Puzzle.Attack('sk113')"],
       {"degats_identite": 2}, passer_sur_option="Defense"),
    _c("sk249 Cloning Program : la menace ne peut PAS etre retiree tant qu'AUCUN sbire SKRULL n'est en jeu (4 menaces restent)",
       "`ThreatCannotBeRemovedFromWhile` + condition inverse (modele sk033) ; Spider-Man contre (THW 1)",
       [HEROS, VIDE_DECK, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('sk249')"], ["Puzzle.Thwart('01001a')"],
       {"menace": [["sk249", 4]]}, cibles=["sk249"], main_exclusive=["01088"]),
    _c("sk249 Cloning Program, TEMOIN : avec un sbire SKRULL en jeu la meme contre retire 1 menace (4 -> 3)",
       "ligne de base du precedent",
       [HEROS, VIDE_DECK, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('sk249')", "Puzzle.PutIntoPlay('sk113')"], ["Puzzle.Thwart('01001a')"],
       {"menace": [["sk249", 3]]}, cibles=["sk249"], main_exclusive=["01088"]),
    # ===================================================================== Xavin (sk250-sk253)
    _c("sk250 Xavin revele : defausse jusqu'a une TRAITRISE (un sbire est defausse au passage) et la revele (Advance : le mechant complote)",
       "`DiscardEncounterCardsUntil(check_face_fn=EstTraitrise)` + `Reveal` ; deck (dessus d'abord) : Hydra Mercenary, Advance, boosts a 0 icone",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01104', '01104', '01104', '01186', '01101')"], ["Puzzle.Reveal('sk250')"],
       {"defausse_rencontre": ["01101"], "menace": [["01097b", 1]]}),
    _c("sk250 Xavin revele : AUCUNE traitrise dans le deck -> tout le deck est defausse, rien n'est revele (pas de menace)",
       "meme chaine sans cible",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01099', '01100', '01101')"], ["Puzzle.Reveal('sk250')"],
       {"menace": [["01097b", 0]]}),
    _c("sk250 Boost : la carte retournee en boost entre en jeu ENGAGEE avec le joueur",
       "`WhenCardBecomeBoost(\"This\")` + `PutIntoPlay(joueur)`",
       [], ["Puzzle.Boost('sk250')"], {"en_jeu": ["sk250"]}),
    _c("sk251 Invisible Forcefield revele : elle s'attache a l'ennemi aux PV imprimes les plus eleves (Rhino 14 > Skrull Commander 5)",
       "`AttachToFaceWhenPutIntoPlay(highest_printed_hp=True, not_with_attach=...)`",
       ["Puzzle.PutIntoPlay('sk113')"], ["Puzzle.Reveal('sk251')"], {"accroche_a": [["sk251", "01094"]]}),
    _c("sk251 Invisible Forcefield : un SECOND exemplaire ne s'attache pas au meme ennemi, il va au suivant (Skrull Commander)",
       "« without another Invisible Forcefield attached »",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('sk251', 'sk251')", "Puzzle.PutIntoPlay('sk113')", "Puzzle.Reveal('sk251')"],
       ["Puzzle.Reveal('sk251')"], {"attaches_n": [["01094", "Invisible Forcefield", 1], ["sk113", "Invisible Forcefield", 1]]}),
    _c("sk251 Invisible Forcefield : aucun ennemi eligible (le mechant en porte deja une, aucun sbire) -> SURGE",
       "« If you cannot, this card gains surge » ; la carte du dessus est revelee",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01106', '01101', 'sk251', 'sk251')", "Puzzle.Reveal('sk251')"],
       ["Puzzle.Reveal('sk251')"], {"carte_du_surge": "01101", "en_jeu": ["01101"]}),
    _c("sk251 Interruption forcee : les degats infliges a l'ennemi attache vont SUR la carte (Rhino intact, 2 jetons de degat)",
       "`WhenUnitWouldTakeDamage(ForcedInterrupt, \"AttachedCharacter\")` + `SetBeInstead` + compteur 'damage' ; le heros frappe Rhino (ATQ 2)",
       [HEROS, VIDE_DECK, "Puzzle.PutIntoPlay('sk251')", "Puzzle.Attach('sk251', '01094')"], ["Puzzle.Attack('01001a')"],
       {"degats": [["01094", 0]], "compteurs": [["sk251", "damage", 2]]}, cibles=["01094"], main_exclusive=["01088"]),
    _c("sk251 Interruption forcee, TEMOIN : sans la carte l'attaque blesse Rhino (2 degats)",
       "ligne de base du precedent",
       [HEROS], ["Puzzle.Attack('01001a')"], {"degats": [["01094", 2]]}, cibles=["01094"], main_exclusive=["01088"]),
    _c("sk251 Seuil : 3 degats deja poses + 2 = 5 -> la carte est DEFAUSSEE, Rhino toujours intact",
       "« if there is at least 5 damage here, discard this card »",
       [HEROS, VIDE_DECK, "Puzzle.PutIntoPlay('sk251')", "Puzzle.Attach('sk251', '01094')", "Puzzle.Counter('sk251', 'damage', 3)"],
       ["Puzzle.Attack('01001a')"], {"hors_jeu": ["sk251"], "degats": [["01094", 0]]}, cibles=["01094"], main_exclusive=["01088"]),
    _c("sk251 Seuil, TEMOIN : 2 degats deja poses + 2 = 4 -> la carte RESTE en jeu avec 4 jetons",
       "ligne de base du precedent (4 < 5)",
       [HEROS, VIDE_DECK, "Puzzle.PutIntoPlay('sk251')", "Puzzle.Attach('sk251', '01094')", "Puzzle.Counter('sk251', 'damage', 2)"],
       ["Puzzle.Attack('01001a')"], {"en_jeu": ["sk251"], "compteurs": [["sk251", "damage", 4]], "degats": [["01094", 0]]},
       cibles=["01094"], main_exclusive=["01088"]),
    _c("sk252 Super-Skrull Training Program revele : chaque ennemi SKRULL recoit une carte Robuste (le mechant non-Skrull non) ; icone Amplify",
       "`EnnemisSkrull` + `GiveStatus(\"Tough\")` ; `desc.Amplify = 1`",
       ["Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk114')"], ["Puzzle.Reveal('sk252')"],
       {"statuts": [["sk113", "Tough"], ["sk114", "Tough"]], "statuts_absents": [["01094", "Tough"]], "menace": [["sk252", 2]],
        "icones": [["Amplify", 1]]}),
    _c("sk253 Going Nova revelee : 2 degats indirects (1 joueur) -> l'identite les subit",
       "`premier.AssignDamage(unites, this, 2[per_hero])` ; une seule cible possible",
       [], ["Puzzle.Reveal('sk253')"], {"degats_identite": 2}),
    _c("sk253 Going Nova revelee a DEUX joueurs : 4 degats indirects repartis entre tous les personnages (4 sur les deux identites)",
       "2[per_hero] = 4 a deux joueurs ; la somme des degats des identites vaut 4",
       ["Puzzle.ChangeForm('01001b')", "Puzzle.ChangeForm('01010b')"], ["Puzzle.Reveal('sk253')"],
       {"degats_total_identites": 4}, heros2="captain_marvel"),
    # ===================================================================== Standard Skrull (sk254-sk259)
    _c("sk254 Impostor (Standard Skrull) revele : un allie devient un sbire SKRULL engage (meme code que sk098, `ability_link`)",
       "`ability_link: sk098`",
       ["Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Reveal('sk254')"],
       {"accroche_a": [["sk254", "skrull_minion"]], "type_en_jeu": [["skrull_minion", "Minion"]], "traits_de": [["skrull_minion", "SKRULL"]]}),
    _c("sk254 Impostor (Standard Skrull) SANS allie : le mechant complote",
       "« Otherwise, the villain schemes »",
       [VIDE_DECK, ZERO], ["Puzzle.Reveal('sk254')"], {"menace": [["01097b", 1]]}),
    _c("sk255 Cursed by the Past (rien en jeu) : le Vautour (sbire nemesis) et Highway Robbery (complot nemesis) sont reveles, le RESTE du set va dans le deck rencontre",
       "`Find.FindAndReveal(finder=is_nemesis)` x2 + `ShuffleAllTo(set_aside_nemesis_sets)` ; alter-ego : le Vautour n'attaque pas",
       [VIDE_DECK, ZERO], ["Puzzle.Reveal('sk255')"],
       {"en_jeu": ["01167", "01166"], "compte_deck": {"01168": 2, "01169": 1}}),
    _c("sk255 Cursed by the Past (Vautour et complot DEJA en jeu) : le Vautour active contre soi, le complot recoit sa menace de depart (3 + 3 = 6)",
       "« it activates against you » (alter-ego : il complote : +1 menace sur le complot principal) ; « place threat equal to its starting threat value »",
       [VIDE_DECK, ZERO, "Puzzle.PutIntoPlay('01167')", "Puzzle.PutIntoPlay('01166')"], ["Puzzle.Reveal('sk255')"],
       {"menace": [["01166", 6], ["01097b", 1]], "compte_deck": {"01168": 2, "01169": 1}}),
    _c("sk256 Experiment Subject : une amelioration qu'on controle est defaussee, le mechant ne complote pas",
       "`DiscardControlCards(upgrade=True)` ; Arc Reactor est la seule amelioration",
       [VIDE_DECK, ZERO, "Puzzle.PutIntoPlay('01035', under_control=True)"], ["Puzzle.Reveal('sk256')"],
       {"hors_jeu": ["01035"], "menace": [["01097b", 0]]}),
    _c("sk256 Experiment Subject SANS amelioration : le mechant complote (menace 1)",
       "« If no card was discarded this way, the villain schemes »",
       [VIDE_DECK, ZERO], ["Puzzle.Reveal('sk256')"], {"menace": [["01097b", 1]]}),
    _c("sk257 Forge Ahead : chaque sbire engage avec soi complote (Skrull Commander MNG 2) et le mechant NE complote PAS",
       "`Worlds.Enemies.EngagedMinionSchemes` -> `activated_cnt` 1 : pas de repli",
       [VIDE_DECK, ZERO, "Puzzle.PutIntoPlay('sk113')"], ["Puzzle.Reveal('sk257')"], {"menace": [["01097b", 2]]}),
    _c("sk257 Forge Ahead SANS sbire engage : le mechant complote (menace 1)",
       "« If no scheme was made this way, the villain schemes »",
       [VIDE_DECK, ZERO], ["Puzzle.Reveal('sk257')"], {"menace": [["01097b", 1]]}),
    _c("sk258 Mobilization (alter-ego) : chaque sbire en jeu s'engage avec LE JOUEUR, puis le mechant complote",
       "`EngagePlayer` pour tous les sbires (meme engage avec l'autre joueur) + `DoSchemes` ; 2 joueurs",
       [VIDE_DECK, ZERO, "Puzzle.PutIntoPlay('sk113', player=1)"], ["Puzzle.Reveal('sk258')"],
       {"engage_avec": [["sk113", 0]], "menace": [["01097b", 1]]}, heros2="captain_marvel"),
    _c("sk258 Mobilization (heros) : le mechant ET chaque sbire engage attaquent (Rhino 2 + Skrull Commander 2 = 4 degats)",
       "`VillainAndEngagedMinionsAttackYou` ; heros sans defense",
       [HEROS, VIDE_DECK, ZERO, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('sk113')"], ["Puzzle.Reveal('sk258')"],
       {"degats_identite": 4, "menace": [["01097b", 0]]}, passer_sur_option="Defense"),
    _c("sk259 Stick to the Plan : le mechant attaque le heros qui a le plus de PV RESTANTS (Captain Marvel 12 contre Spider-Man 10)",
       "`Filter.One(identites en forme heros, most_remaining_hp=True)` + `DoAttackYou` ; 2 joueurs, sans defense",
       [VIDE_DECK, ZERO, "Puzzle.ChangeForm('01001b')", "Puzzle.ChangeForm('01010b')"], ["Puzzle.Reveal('sk259')"],
       {"degats": [["01010a", 2]], "degats_identite": 0}, heros2="captain_marvel", main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk259 Stick to the Plan : PV RESTANTS (pas PV max) : Captain Marvel a 3 degats (9 restants) -> Spider-Man (10) est attaque",
       "preuve que le choix lit les PV restants",
       [VIDE_DECK, ZERO, "Puzzle.ChangeForm('01001b')", "Puzzle.ChangeForm('01010b')", "Puzzle.Damage('01010a', 3)"], ["Puzzle.Reveal('sk259')"],
       {"degats": [["01010a", 3]], "degats_identite": 2}, heros2="captain_marvel", main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk259 Stick to the Plan, joueur en ALTER-EGO : aucun heros -> aucune attaque, le mechant complote",
       "« If no attack was made this way, the villain schemes »",
       [VIDE_DECK, ZERO], ["Puzzle.Reveal('sk259')"], {"menace": [["01097b", 1]], "degats_identite": 0}),
    # ===================================================================== Expert Skrull (sk260-sk262)
    _c("sk260 Replaced Archenemy (nemesis hors jeu) : le Vautour est trouve, la carte s'y attache, il est revele ; il gagne SKRULL et +1 MNG",
       "`Find.Find` + `AttachTo2` + `Reveal` ; `GiveKeywordToAttached(Minion, trait=SKRULL)` ; alter-ego : le Vautour n'attaque pas",
       [VIDE_DECK, ZERO], ["Puzzle.Reveal('sk260')"],
       {"en_jeu": ["01167", "sk260"], "accroche_a": [["sk260", "01167"]], "traits_de": [["01167", "SKRULL"]],
        "attributs_carte": [["01167", "scheme", 1]]}),
    _c("sk260 Replaced Archenemy (Vautour DEJA en jeu) : elle s'y attache puis il active contre soi (alter-ego : il complote, MNG 1 + 1 = 2)",
       "« attach this card to it. Then, it activates against you »",
       [VIDE_DECK, ZERO, "Puzzle.PutIntoPlay('01167')"], ["Puzzle.Reveal('sk260')"],
       {"accroche_a": [["sk260", "01167"]], "menace": [["01097b", 2]], "traits_de": [["01167", "SKRULL"]]}),
    _c("sk260 Replaced Archenemy : aucun sbire nemesis trouvable (retire de la partie) -> la carte est defaussee",
       "pas de cible : l'attachement ne reste pas en jeu",
       [VIDE_DECK, ZERO, "Puzzle.Remove('01167')"], ["Puzzle.Reveal('sk260')"], {"hors_jeu": ["sk260"]}),
    _c("sk261 Focused Attention : le mechant recoit 1 carte de boost face cachee ; surge natif (la carte du dessus est revelee)",
       "`desc.Surge = 1` + `DonnerBoostAuMechant` ; Hydra Mercenary au-dessus du deck",
       [VIDE_DECK, "Puzzle.CreateEncounterDeck('01106', '01101', '01102')"], ["Puzzle.Reveal('sk261')"],
       {"boosts_mechant": 1, "carte_du_surge": "01101", "en_jeu": ["01101"]}),
    _c("sk262 Tricky Assault : le joueur passe en forme HEROS, le mechant l'attaque ; attaque NON defendue -> le mechant complote en plus",
       "`ChangeToForm(Hero)` + `DoAttackYou(if_undefended=...)` ; Rhino ATQ 2 : 2 degats, 1 menace ; sans defense",
       [VIDE_DECK, ZERO, "Puzzle.EmptyHand()"], ["Puzzle.Reveal('sk262')"],
       {"forme": "Hero", "degats_identite": 2, "menace": [["01097b", 1]]}, passer_sur_option="Defense"),
    _c("sk262 Tricky Assault, attaque DEFENDUE (Spider-Man DEF 3) : aucun degat et le mechant ne complote pas",
       "« If this attack is undefended » : la defense annule le complot",
       [VIDE_DECK, ZERO, "Puzzle.EmptyHand()"], ["Puzzle.Reveal('sk262')"],
       {"forme": "Hero", "degats_identite": 0, "menace": [["01097b", 0]]}),
]

VERIFICATIONS = r'''
def modulaires_dump(monde, aides):
    """SONDE de mise au point (jamais dans la batterie finale) : decrit l'etat, rend toujours False."""
    from game.operate.worlds import Worlds
    lignes = []
    identite = aides["identite"](monde)
    lignes.append(f"identite={identite.paper.card_id} forme={'Hero' if monde.players[0].IsHero() else 'AlterEgo'} "
                  f"main={[getattr(f.paper, 'card_id', '?') for f in monde.players[0].hand_cards.Get()]}")
    lignes.append("deck_joueur=" + str([getattr(f.paper, 'card_id', '?') for f in monde.players[0].player_deck.Get()][:12]))
    lignes.append("attaches identite=" + str([a.paper.card_id for a in identite.GetAttachedAttachments()]))
    for objet in monde.object_manager.card_dict.values():
        f = objet.face
        if f is not None and f.IsInPlay() and (getattr(f.paper, "card_id", "").startswith("sk") or getattr(f.paper, "card_id", "").startswith("010")):
            lignes.append(f"EN JEU {f.paper.card_id} menace={getattr(f, 'threat', None)} hote={getattr(getattr(f, 'bind_face', None), 'paper', None) and f.bind_face.paper.card_id}")
    lignes.append("defausse_rencontre=" + str([getattr(f.paper, 'card_id', '?') for f in Worlds.GetEncounterDiscardPileCards(monde)]))
    lignes.append("deck_rencontre_dessus=" + str([getattr(f.paper, 'card_id', '?') for f in Worlds.GetEncounterDeckCards(monde)][-6:]))
    lignes.append("de_cote=" + str(sorted(getattr(x.paper, 'card_id', '?') for x in _de_cote(monde))))
    return False, " | ".join(lignes)


def _de_cote(monde):
    faces = list(monde.aside_deck.Get(True))
    for j in monde.const_players:
        faces += list(j.set_aside_deck.Get(True))
    return faces


def _mechant(monde):
    from game.operate.worlds import Worlds
    vilains = Worlds.GetAllVillains(monde)
    return vilains[0] if vilains else None


def modulaires_etat(monde, aides):
    """etat_attendu (cles communes) + les cles propres au bloc :
    compte_deck {card_id: n} (copies dans le deck rencontre), mis_de_cote_ids [ids], boosts_mechant n,
    deck_joueur_ids [ids] (presents dans le deck du joueur 1), hote [[card_id, hote_id]]."""
    attendu = aides["cas"].get("attendu") or {}
    connues = set(CLES_ETAT_ATTENDU) | {"compte_deck", "mis_de_cote_ids", "boosts_mechant", "deck_joueur_ids", "hote",
                                        "sans_hote", "boosts_mechant_min", "taille_deck_rencontre", "villainous", "type_en_jeu", "cartes_distribuees",
                                        "degats_total_identites", "engage_avec", "attaches_n", "action_offerte",
                                        "deck_joueur2_ids", "fragments_dans_decks", "fragments_de_cote"}
    inconnues = sorted(set(attendu) - connues)
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de modulaires_etat : {inconnues}"
    ok, message = etat_attendu(monde, aides)
    soucis = [] if ok else [message]
    from game.operate.worlds import Worlds
    if "compte_deck" in attendu:
        ids = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde)]
        for card_id, n in attendu["compte_deck"].items():
            if ids.count(card_id) != n:
                soucis.append(f"{card_id} : {ids.count(card_id)} copie(s) dans le deck rencontre (attendu {n})")
    if "taille_deck_rencontre" in attendu:
        n = len(Worlds.GetEncounterDeckCards(monde))
        if n != attendu["taille_deck_rencontre"]:
            soucis.append(f"deck rencontre = {n} carte(s) (attendu {attendu['taille_deck_rencontre']})")
    if "mis_de_cote_ids" in attendu:
        ids = [getattr(f.paper, "card_id", None) for f in _de_cote(monde)]
        for card_id in attendu["mis_de_cote_ids"]:
            if card_id not in ids:
                soucis.append(f"{card_id} n'est pas mis de cote (de cote = {sorted(ids)})")
    if "fragments_dans_decks" in attendu:
        for indice, voulu in enumerate(attendu["fragments_dans_decks"]):
            n = sum(1 for f in monde.players[indice].player_deck.Get() if getattr(f.paper, "card_id", "").startswith("sk230"))
            if n != voulu:
                soucis.append(f"{n} fragment(s) dans le deck du joueur {indice + 1} (attendu {voulu})")
    if "fragments_de_cote" in attendu:
        n = sum(1 for f in _de_cote(monde) if getattr(f.paper, "card_id", "").startswith("sk230"))
        if n != attendu["fragments_de_cote"]:
            soucis.append(f"{n} fragment(s) encore mis de cote (attendu {attendu['fragments_de_cote']})")
    if "deck_joueur2_ids" in attendu:
        ids = [getattr(f.paper, "card_id", None) for f in monde.players[1].player_deck.Get()]
        for card_id in attendu["deck_joueur2_ids"]:
            if card_id not in ids:
                soucis.append(f"{card_id} n'est pas dans le deck du joueur 2")
    if "deck_joueur_ids" in attendu:
        ids = [getattr(f.paper, "card_id", None) for f in monde.players[0].player_deck.Get()]
        for card_id in attendu["deck_joueur_ids"]:
            if card_id not in ids:
                soucis.append(f"{card_id} n'est pas dans le deck du joueur")
    for carte_id, hote_id in attendu.get("hote") or []:
        carte = aides["par_id"](monde, carte_id)
        if carte is None:
            soucis.append(f"{carte_id} n'est pas en jeu (hote)")
            continue
        hote = getattr(carte, "bind_face", None)
        reel = getattr(getattr(hote, "paper", None), "card_id", None)
        if reel != hote_id:
            soucis.append(f"{carte_id} est attachee a {reel}, attendu {hote_id}")
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
    if "cartes_distribuees" in attendu:
        n = sum(len(list(j.dealt_encounter_cards.GetAll())) for j in monde.players)
        if n != attendu["cartes_distribuees"]:
            soucis.append(f"cartes rencontre distribuees face cachee = {n} (attendu {attendu['cartes_distribuees']})")
    if "degats_total_identites" in attendu:
        total = sum(j.GetIdentity().max_health - j.GetIdentity().health for j in monde.players)
        if total != attendu["degats_total_identites"]:
            soucis.append(f"degats cumules des identites = {total} (attendu {attendu['degats_total_identites']})")
    for carte_id, indice in attendu.get("engage_avec") or []:
        carte = aides["par_id"](monde, carte_id)
        if carte is None:
            soucis.append(f"{carte_id} n'est pas en jeu (engage_avec)")
        elif carte.engaged_player is not monde.players[indice]:
            soucis.append(f"{carte_id} n'est pas engage avec le joueur {indice}")
    for hote_id, nom, voulu in attendu.get("attaches_n") or []:
        hote = aides["par_id"](monde, hote_id)
        if hote is None:
            soucis.append(f"{hote_id} n'est pas en jeu (attaches_n)")
            continue
        n = sum(1 for a in hote.GetAttachedAttachments() if a.IsName(nom))
        if n != voulu:
            soucis.append(f"{hote_id} porte {n} « {nom} » (attendu {voulu})")
    for carte_id, type_voulu in attendu.get("type_en_jeu") or []:
        carte = aides["par_id"](monde, carte_id)
        if carte is None:
            soucis.append(f"{carte_id} n'est pas en jeu (type_en_jeu)")
        elif type(carte).__name__ != type_voulu:
            soucis.append(f"{carte_id} est de type {type(carte).__name__} (attendu {type_voulu})")
    for carte_id, voulu in attendu.get("villainous") or []:
        carte = aides["par_id"](monde, carte_id)
        if carte is None:
            soucis.append(f"{carte_id} n'est pas en jeu (villainous)")
        elif bool(carte.IsVillainous()) != voulu:
            soucis.append(f"{carte_id}.IsVillainous() = {carte.IsVillainous()} (attendu {voulu})")
    if "boosts_mechant" in attendu or "boosts_mechant_min" in attendu:
        v = _mechant(monde)
        n = v.components.boostable.GetDeck().GetSize() if v is not None else -1
        if "boosts_mechant" in attendu and n != attendu["boosts_mechant"]:
            soucis.append(f"cartes de boost face cachee du mechant = {n} (attendu {attendu['boosts_mechant']})")
        if "boosts_mechant_min" in attendu and n < attendu["boosts_mechant_min"]:
            soucis.append(f"cartes de boost face cachee du mechant = {n} (attendu au moins {attendu['boosts_mechant_min']})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat modulaires conforme"
'''
