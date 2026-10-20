# Cas test_capacites du scenario 1 KREE SENTRY de Galactic Storm (gs076-gs090), lot GS-4 (20/10/2026).
# Format identique a tools/test_capacites.py ; noms prefixes `[ks]` puis le card_id (filtre : `[ks]`, ou
# `[ks] gs083 ` pour une carte).
#
# Conventions de ce fichier :
#  - le heros de test (Spider-Man, 01001, ATQ 2 / CTR 1 / DEF 3) demarre en ALTER EGO ; `HEROS` le met en heros.
#  - la mise en place REELLE du scenario tourne a chaque cas : Rick Jones (gs081) en jeu sous le controle du premier
#    joueur, une Poigne (gs082) sur lui, l'autre mise de cote ; Kree Sentry (I) en jeu.
#  - `DECK_NEUTRE` : le deck rencontre ne contient que des Advance (01186), traitrise SANS icone de boost ni
#    capacite Boost : une activation de Kree Sentry ne recoit alors aucun bonus de boost (mesures exactes).
#  - Imperial Guard n'est PAS monte par ces cas (le scenario d'essai `gs_kree_sentry` le declare en modulaire : le
#    deck rencontre est vide ou remplace par `DECK_NEUTRE`).
SC = "gs_kree_sentry"
SCE = "gs_kree_sentry_expert"
HEROS = "Puzzle.ChangeForm('01001b')"
DECK_NEUTRE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', '01186', '01186', '01186')"]
SANS_DEFENSE = {"passer_sur_option": "Defense"}
# Les deux Poignes ni en jeu ni de cote : « If you cannot » (aucune copie mise de cote) sans rien attacher a Rick Jones.
AUCUNE = ["Puzzle.Discard('gs082')", "Puzzle.Remove('gs082')", "Puzzle.Remove('gs082')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[ks] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "ks_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================== gs079a : mise en place
    _c("gs079a Setup : Rick Jones en jeu sous le controle du premier joueur, UNE Poigne sur lui, l'autre mise de cote",
       "« Put Rick Jones into play under the first player's control. Set 1 copy of Sentry's Grasp aside and attach the "
       "other to Rick Jones » (WhenCardSetup, modele gs117a)",
       [], [], {"en_jeu": ["gs081"], "sous_controle": ["gs081"], "poignes_sur": [["gs081", 1]], "poignes_de_cote": 1,
                "mechant_id": "gs076"}),
    _c("gs079a Setup (expert) : Kree Sentry (II) revele a la mise en place, Rick Jones porte alors LES DEUX Poignes",
       "expert : la face 1A est identique ; le « When Revealed » de gs077 attache la seconde copie",
       [], [], {"en_jeu": ["gs081"], "poignes_sur": [["gs081", 2]], "poignes_de_cote": 0, "mechant_id": "gs077"},
       scenario=SCE),
    # ============================================================== gs079b : 1B
    _c("gs079b valeurs : menace de depart 2[per_hero] (un joueur : 2), aucune menace sur le complot du deck",
       "StartingThreat 2* (lu sur le scan : « 2 » + silhouette)", [], [], {"menace": [["gs079b", 2]]}),
    _c("gs079b Forced Response apres l'etape 1 : Rick Jones porte UNE Poigne -> 1 degat sur lui",
       "« deal 1 damage to each character for each copy of Sentry's Grasp attached to it » (AfterResolveVillainPhaseStep, "
       "modele gs117b) ; le verificateur envoie la fin de l'etape 1",
       DECK_NEUTRE, [], {"degats": [["gs081", 1]]}, verifier="ks_etape_un"),
    _c("gs079b Forced Response : DEUX Poignes sur Rick Jones -> 2 degats (une seule instance)",
       "« for each copy ... attached to IT » : le nombre de Poignes du personnage",
       DECK_NEUTRE, [], {"degats": [["gs081", 2]], "poignes_sur": [["gs081", 2]]}, scenario=SCE,
       verifier="ks_etape_un"),
    _c("gs079b Forced Response : une Poigne sur le HEROS (identite) -> 1 degat sur l'identite ; Rick sans Poigne n'en subit pas",
       "« each character » : l'identite d'un joueur est un personnage ; Rick Jones n'en porte plus -> 0",
       DECK_NEUTRE + [HEROS, "Puzzle.Discard('gs082')", "Puzzle.AttachReel('gs082', '01001a')"], [],
       {"degats_identite": 1, "degats": [["gs081", 0]], "poignes_sur": [["01001a", 1], ["gs081", 0]]},
       verifier="ks_etape_un"),
    _c("gs079b Forced Response : une Poigne sur un SBIRE (Shocker) -> 1 degat sur lui",
       "« each character » : un sbire est un personnage",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('01103')", "Puzzle.AttachReel('gs082', '01103')"], [],
       {"degats": [["01103", 1]]}, verifier="ks_etape_un"),
    _c("gs079b Forced Response, TEMOIN : un allie SANS Poigne (Black Widow) n'est pas blesse",
       "« for each copy attached to it » : 0 copie, 0 degat",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('01075', under_control=True)"], [],
       {"degats": [["01075", 0]], "degats_identite": 0}, verifier="ks_etape_un"),
    # ============================================================== gs080a / gs080b : stade 2
    _c("gs080a When Revealed : Outpost Collapse Protocol EN JEU -> 2[per_hero] menaces et 1 jeton d'acceleration sur elle",
       "« If the Outpost Collapse Protocol side scheme is in play, place 2[per_hero] threat and 1 acceleration token on it »",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs087')"], ["Puzzle.AdvanceMainScheme(1)"],
       {"menace": [["gs087", 5]], "jetons": [["gs087", "acceleration_token", 1]], "principale": "gs080b"}),
    _c("gs080a When Revealed : Outpost Collapse Protocol dans le DECK RENCONTRE -> cherchee et revelee (Hinder 2 : 1 + 2 = 3)",
       "« Otherwise, search the encounter deck and discard pile for the Outpost Collapse Protocol side scheme and reveal it »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', 'gs087', '01186')"],
       ["Puzzle.AdvanceMainScheme(1)"],
       {"en_jeu": ["gs087"], "menace": [["gs087", 3]], "jetons": [["gs087", "acceleration_token", 0]]}),
    _c("gs080a When Revealed : Outpost Collapse Protocol dans la DEFAUSSE rencontre -> cherchee et revelee",
       "« search the encounter deck AND DISCARD PILE »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186')", "Puzzle.CreateEncounterDiscardPile('gs087')"],
       ["Puzzle.AdvanceMainScheme(1)"], {"en_jeu": ["gs087"], "menace": [["gs087", 3]]}),
    _c("gs080b valeurs : menace de depart 1[per_hero] sur le stade 2 (un joueur : 1)",
       "StartingThreat 1* (lu sur le scan)", DECK_NEUTRE, ["Puzzle.AdvanceMainScheme(1)"],
       {"principale": "gs080b", "menace": [["gs080b", 1]]}),
    _c("gs080b Forced Response apres l'etape 1 : une Poigne sur Rick Jones -> 1 degat (stade 2)",
       "meme Reponse forcee que 1B",
       DECK_NEUTRE + ["Puzzle.AdvanceMainScheme(1)"], [], {"degats": [["gs081", 1]], "principale": "gs080b"},
       verifier="ks_etape_un"),
    _c("gs080b : stade 2 accompli (menace 10[per_hero]) -> les joueurs perdent",
       "« If this stage is completed, the players lose the game » : regle du dernier stade, aucun script",
       DECK_NEUTRE + ["Puzzle.AdvanceMainScheme(1)"], ["Puzzle.SetThreat('gs080b', 10)"], {"defaite": True}),
    _c("gs080b : stade 2 non accompli (9 sur 10) -> pas de defaite",
       "temoin : la defaite ne vient qu'a l'objectif",
       DECK_NEUTRE + ["Puzzle.AdvanceMainScheme(1)"], ["Puzzle.SetThreat('gs080b', 9)"], {"defaite": False}),
    # ============================================================== gs076 / gs077 / gs078 : Kree Sentry
    _c("gs076 Forced Response : Kree Sentry attaque un allie (Black Widow) et le blesse -> une Poigne s'attache a lui",
       "« After Kree Sentry attacks and damages a character, attach a set aside copy of Sentry's Grasp to that character » "
       "(modele 01118 Sonic Converter) ; attaque directe d'un allie (brique commune)",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.EnemyAttacks('gs076', '01075')"],
       {"degats": [["01075", 1]], "poignes_sur": [["01075", 1], ["gs081", 1]], "poignes_de_cote": 0,
        "menace": [["gs079b", 2]]}, **SANS_DEFENSE),
    _c("gs076 Forced Response : AUCUNE Poigne de cote -> 1 menace sur la principale (2 -> 3)",
       "« If you cannot, place 1 threat on the main scheme »",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('01075', under_control=True)"] + AUCUNE,
       ["Puzzle.EnemyAttacks('gs076', '01075')"],
       {"menace": [["gs079b", 3]], "poignes_sur": [["01075", 0]], "poignes_de_cote": 0, "poignes_en_jeu": 0},
       **SANS_DEFENSE),
    _c("gs076 Forced Response, TEMOIN : l'attaque ne fait AUCUN degat (allie Tenace) -> rien ne se declenche",
       "« attacks AND DAMAGES » : la carte Tenace absorbe, pas de degat, pas de Poigne, pas de menace",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Tough('01075')"],
       ["Puzzle.EnemyAttacks('gs076', '01075')"],
       {"degats": [["01075", 0]], "poignes_sur": [["01075", 0]], "poignes_de_cote": 1, "menace": [["gs079b", 2]]},
       **SANS_DEFENSE),
    _c("gs076 Forced Response : l'allie est VAINCU par l'attaque -> la Poigne ne peut pas s'y attacher : 1 menace sur la principale",
       "un personnage vaincu a bien ete blesse ; « If you cannot » joue (la copie de cote reste de cote)",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Damage('01075', 1)"],
       ["Puzzle.EnemyAttacks('gs076', '01075')"],
       {"hors_jeu": ["01075"], "menace": [["gs079b", 3]], "poignes_de_cote": 1}, **SANS_DEFENSE),
    _c("gs076 Forced Response : Kree Sentry attaque un SBIRE (Shocker) et le blesse -> Poigne sur le sbire",
       "« a character » : un sbire est un personnage ; « Attached to a minion... » (livret p.9)",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.EnemyAttacks('gs076', '01103')"],
       {"degats": [["01103", 1]], "poignes_sur": [["01103", 1]], "poignes_de_cote": 0}),
    _c("gs077 When Revealed : Kree Sentry (II) arrive -> la Poigne de cote s'attache a Rick Jones (deux sur lui)",
       "« Attach a set aside copy of Sentry's Grasp to Rick Jones »",
       DECK_NEUTRE, ["Puzzle.AdvanceVillain()"],
       {"mechant_id": "gs077", "poignes_sur": [["gs081", 2]], "poignes_de_cote": 0}),
    _c("gs077 Forced Response : AUCUNE Poigne de cote -> 2 menaces sur la principale (2 -> 4)",
       "« If you cannot, place 2 threat on the main scheme »",
       DECK_NEUTRE + ["Puzzle.AdvanceVillain()", "Puzzle.PutIntoPlay('12012', under_control=True)"],
       ["Puzzle.EnemyAttacks('gs077', '12012')"],
       {"menace": [["gs079b", 4]], "poignes_sur": [["12012", 0], ["gs081", 2]], "degats": [["12012", 2]]},
       **SANS_DEFENSE),
    _c("gs077 Forced Response : une Poigne de cote -> s'attache a l'allie blesse (ATQ 2 : 2 degats)",
       "meme Reponse que gs076 avec ATQ 2 ; une copie remise de cote d'abord",
       DECK_NEUTRE + ["Puzzle.AdvanceVillain()", "Puzzle.Discard('gs082')",
                      "Puzzle.PutIntoPlay('12012', under_control=True)"],
       ["Puzzle.EnemyAttacks('gs077', '12012')"],
       {"poignes_sur": [["12012", 1], ["gs081", 1]], "menace": [["gs079b", 2]], "degats": [["12012", 2]],
        "poignes_de_cote": 0}, **SANS_DEFENSE),
    _c("gs078 When Revealed (expert) : Kree Sentry (III) -> CHAQUE Poigne de cote s'attache a Rick Jones (deux copies mises de cote)",
       "« Attach each set aside copy of Sentry's Grasp to Rick Jones »",
       DECK_NEUTRE + ["Puzzle.Discard('gs082')", "Puzzle.Discard('gs082')"], ["Puzzle.AdvanceVillain()"],
       {"mechant_id": "gs078", "poignes_sur": [["gs081", 2]], "poignes_de_cote": 0}, scenario=SCE),
    _c("gs078 Forced Response (expert) : AUCUNE Poigne de cote -> 3 menaces sur la principale (2 -> 5)",
       "« If you cannot, place 3 threat on the main scheme »",
       DECK_NEUTRE + ["Puzzle.AdvanceVillain()", "Puzzle.PutIntoPlay('12012', under_control=True)"],
       ["Puzzle.EnemyAttacks('gs078', '12012')"],
       {"menace": [["gs079b", 5]], "degats": [["12012", 3]], "poignes_sur": [["12012", 0]], "poignes_de_cote": 0},
       scenario=SCE, **SANS_DEFENSE),
    # ============================================================== gs081 : Rick Jones
    _c("gs081 Forced Interrupt : Kree Sentry attaque le HEROS -> il attaque Rick Jones a la place (1 degat sur Rick, 0 sur le heros)",
       "« When Kree Sentry attacks you, it attacks Rick Jones instead » (modele 50089b)",
       DECK_NEUTRE + [HEROS], ["Puzzle.Attack('gs076')"],
       {"degats": [["gs081", 1]], "degats_identite": 0}, **SANS_DEFENSE),
    _c("gs081 Forced Interrupt, TEMOIN : l'attaque contre un AUTRE joueur n'est pas detournee",
       "« attacks YOU » : Rick Jones sert le premier joueur ; le second joueur est attaque normalement",
       DECK_NEUTRE + [HEROS], ["Puzzle.Attack('gs076', against='01001a')"],
       {"degats": [["gs081", 1]]}, heros2="spider_man", **SANS_DEFENSE),
    _c("gs081 Forced Interrupt : le detournement ne compte pas comme une attaque « contre vous » (Experimental Weapons ne part pas)",
       "livret p.4 : « attacks you » ne part pas quand l'attaque vise un allie ; Experimental Weapons (04074) : « After the attached "
       "villain attacks and damages you, discard 1 card from your hand » -> la main reste intacte",
       DECK_NEUTRE + [HEROS, "Puzzle.PutIntoPlay('04074')"], ["Puzzle.Attack('gs076')"],
       {"degats": [["gs081", 1]], "taille_main": 6}, main_exclusive=["01088", "01089", "01090", "01001a", "01005", "01006"][:0] or None,
       **SANS_DEFENSE),
    _c("gs081 Forced Response (Experimental Weapons), TEMOIN : sans detournement, la meme carte fait defausser une carte",
       "contre-cas : le second joueur est blesse directement, sa main perd une carte",
       DECK_NEUTRE + [HEROS, "Puzzle.PutIntoPlay('04074')"], ["Puzzle.Attack('gs076', against='01001a')"],
       {"degats": [["gs081", 1]]}, heros2="spider_man", **SANS_DEFENSE),
    _c("gs081 « If Rick Jones leaves play, the players lose the game » : Rick vaincu -> defaite",
       "AfterCardLeavePlay(\"This\") : tout depart compte",
       DECK_NEUTRE, ["Puzzle.Damage('gs081', 9)"], {"defaite": True}),
    _c("gs081 « If Rick Jones leaves play... » : Rick DEFAUSSE par un effet -> defaite",
       "tout depart, pas seulement la defaite au combat",
       DECK_NEUTRE, ["Puzzle.Discard('gs081')"], {"defaite": True}),
    _c("gs081 « If Rick Jones leaves play... », TEMOIN : un autre allie qui part ne fait pas perdre",
       "seul Rick Jones",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Damage('01075', 9)"],
       {"defaite": False, "hors_jeu": ["01075"], "en_jeu": ["gs081"]}),
    _c("gs081 « does not count against your ally limit » : trois allies + Rick Jones, 3 comptes dans la limite",
       "ThisNotCountAllyLimit (modele 50091)",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.PutIntoPlay('01076', under_control=True)",
                      "Puzzle.PutIntoPlay('01083', under_control=True)"], [],
       {"allies_comptes": 3, "sous_controle": ["gs081", "01075", "01076", "01083"]}),
    _c("gs081 Rick Jones attaque Kree Sentry (seule cible permise par sa Poigne) : ATQ 2 sur Kree Sentry, 2 degats consecutifs sur lui",
       "ATQ 2 avec deux etoiles = 2 degats consecutifs ; la Poigne limite ses attaques a Kree Sentry et a elle-meme",
       DECK_NEUTRE, ["Puzzle.Attack('gs081')"], {"degats": [["gs076", 2], ["gs081", 2]]}, cibles=["gs076"]),
    # ============================================================== gs082 : Sentry's Grasp
    _c("gs082 « cannot thwart » : le heros porteur d'une Poigne ne contre pas (menace du complot inchangee)",
       "UnitCannotThwartTarget(\"AttachedCharacter\", cannot_thwart=True) (modele 03028)",
       DECK_NEUTRE + [HEROS, "Puzzle.Discard('gs082')", "Puzzle.AttachReel('gs082', '01001a')"], ["Puzzle.Thwart('01001a')"],
       {"menace": [["gs079b", 2]]}, cibles=["gs079b"]),
    _c("gs082 « cannot thwart », TEMOIN : sans Poigne sur lui, le meme heros retire 1 menace (2 -> 1)",
       "contre-cas : le montage permet bien le contre", DECK_NEUTRE + [HEROS], ["Puzzle.Thwart('01001a')"],
       {"menace": [["gs079b", 1]]}, cibles=["gs079b"]),
    _c("gs082 « can only attack Kree Sentry or this card » : le heros porteur attaque Kree Sentry (2 degats)",
       "Kree Sentry est une cible permise",
       DECK_NEUTRE + [HEROS, "Puzzle.Discard('gs082')", "Puzzle.AttachReel('gs082', '01001a')", "Puzzle.PutIntoPlay('01103')"],
       ["Puzzle.Attack('01001a')"], {"degats": [["gs076", 2], ["01103", 0]]}, cibles=["gs076"]),
    _c("gs082 « can only attack Kree Sentry or this card » : un SBIRE (Shocker) n'est PAS une cible legale pour le porteur",
       "les cibles proposees a l'attaque de base ne contiennent pas Shocker",
       DECK_NEUTRE + [HEROS, "Puzzle.Discard('gs082')", "Puzzle.AttachReel('gs082', '01001a')", "Puzzle.PutIntoPlay('01103')"],
       ["Puzzle.Attack('01001a')"], {"option": "Attack", "contient": ["gs076"], "exclut": ["01103"]}, verifier="cibles_legales_proposees"),
    _c("gs082 « can only attack Kree Sentry or this card » : le porteur peut attaquer SA Poigne (2 degats sur elle)",
       "« or this card »", DECK_NEUTRE + [HEROS, "Puzzle.Discard('gs082')", "Puzzle.AttachReel('gs082', '01001a')"],
       ["Puzzle.Attack('01001a')"], {"compteurs": [["gs082", "damage", 2]]}, cibles=["gs082"]),
    _c("gs082 « Any player can attack this card as if it were a minion » : un heros SANS Poigne attaque la Poigne de Rick (2 degats)",
       "Encased in Ice (54035) : `consider_as` Minion ; n'importe quel joueur",
       DECK_NEUTRE + [HEROS], ["Puzzle.Attack('01001a')"], {"compteurs": [["gs082", "damage", 2]]}, cibles=["gs082"]),
    _c("gs082 « If there is 3 or more damage here, set Sentry's Grasp aside » : 2 degats -> reste attachee",
       "seuil 3", DECK_NEUTRE, ["Puzzle.PlaceCounters('gs082', 'damage', 2)"],
       {"poignes_sur": [["gs081", 1]], "poignes_de_cote": 1, "compteurs": [["gs082", "damage", 2]]}),
    _c("gs082 « ...3 or more damage here, set aside » : 3 degats -> remise de cote (plus attachee a Rick)",
       "seuil 3 atteint", DECK_NEUTRE, ["Puzzle.PlaceCounters('gs082', 'damage', 3)"],
       {"poignes_sur": [["gs081", 0]], "poignes_de_cote": 2, "poignes_en_jeu": 0}),
    _c("gs082 « Forced Interrupt: When this card would leave play, set it aside instead » : l'hote (Black Widow) est vaincu -> Poigne de cote",
       "WhenCardWouldLeavePlay + SetBeInstead + SetAside",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.AttachReel('gs082', '01075')"],
       ["Puzzle.Damage('01075', 9)"], {"hors_jeu": ["01075"], "poignes_de_cote": 2, "poignes_en_jeu": 0}),
    _c("gs082 « ...set it aside instead » : la Poigne DEFAUSSEE par un effet est mise de cote (jamais en defausse)",
       "meme interruption", DECK_NEUTRE, ["Puzzle.Discard('gs082')"],
       {"poignes_de_cote": 2, "poignes_en_jeu": 0}),
    _c("gs082 degats effaces : une Poigne mise de cote revient SANS degat",
       "elle quitte le jeu : ses compteurs de degats ne la suivent pas",
       DECK_NEUTRE + ["Puzzle.PlaceCounters('gs082', 'damage', 2)", "Puzzle.Discard('gs082')",
                      "Puzzle.AttachReel('gs082', 'gs081')"],
       [], {"compteurs": [["gs082", "damage", 0]], "poignes_sur": [["gs081", 1]]}),
    _c("gs082 sur un SBIRE : Shocker porteur ne peut pas s'activer (ni attaquer ni manigancer) ; le temoin attaque",
       "livret p.9 : « Attached to a minion, that minion cannot activate for a scheme or attack »",
       DECK_NEUTRE + [HEROS, "Puzzle.PutIntoPlay('01103')", "Puzzle.AttachReel('gs082', '01103')"], ["Puzzle.Attack('01103')"],
       {"degats": [["gs081", 0]], "degats_identite": 0}),
    _c("gs082 sur un SBIRE, TEMOIN : sans Poigne, Shocker attaque le heros (2 degats)",
       "contre-cas", DECK_NEUTRE + [HEROS, "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('01103')"],
       {"degats_identite": 2}, **SANS_DEFENSE),
    _c("gs082 « as if it were a minion » = pour les ATTAQUES seulement : la reponse de Valkyrie (« deal 2 damage to a minion ») ne vise pas la Poigne",
       "livret p.9 : « Cards and abilities that target a minion but are not attacks cannot be resolved against the Sentry's Grasp » ; "
       "aucun autre sbire : la Poigne reste a 0 degat",
       DECK_NEUTRE, ["Puzzle.PutIntoPlay('06012', under_control=True)"], {"compteurs": [["gs082", "damage", 0]]}),
    _c("gs082 « as if it were a minion », TEMOIN : la meme reponse de Valkyrie frappe un VRAI sbire (Shocker, 2 degats)",
       "contre-cas : la reponse part bien quand une cible legale existe",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.PutIntoPlay('06012', under_control=True)"],
       {"degats": [["01103", 2]], "compteurs": [["gs082", "damage", 0]]}),
]

CAS += [
    # ============================================================== gs083 : Optic Blast Cannon
    _c("gs083 Optic Blast Cannon : attache a Kree Sentry, +1 ATQ",
       "badge `desc.ATK+` ; « Attach to Kree Sentry » (modele gs129)", DECK_NEUTRE, ["Puzzle.PutIntoPlay('gs083')"],
       {"accroche_a": [["gs083", "gs076"]], "attributs_carte": [["gs076", "attack", 1]]}),
    _c("gs083 « Kree Sentry's attacks gain piercing and ranged » : l'attaque (detournee sur Rick Tenace) defausse sa carte Tenace et fait 2 degats (1 + 1)",
       "piercing : la carte Tenace est defaussee et les degats passent",
       DECK_NEUTRE + [HEROS, "Puzzle.PutIntoPlay('gs083')", "Puzzle.Tough('gs081')"], ["Puzzle.Attack('gs076')"],
       {"degats": [["gs081", 2]], "statuts_absents": [["gs081", "Tough"]]}, **SANS_DEFENSE),
    _c("gs083 piercing, TEMOIN : sans Optic Blast Cannon, la carte Tenace de Rick absorbe l'attaque (0 degat)",
       "contre-cas", DECK_NEUTRE + [HEROS, "Puzzle.Tough('gs081')"], ["Puzzle.Attack('gs076')"],
       {"degats": [["gs081", 0]], "statuts_absents": [["gs081", "Tough"]]}, **SANS_DEFENSE),
    _c("gs083 ranged : l'attaque de Kree Sentry contre le Jailor (Riposte 1) ne subit pas de riposte",
       "« gain ranged » : ignore Retaliate",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs083')", "Puzzle.PutIntoPlay('gs131')"],
       ["Puzzle.EnemyAttacks('gs076', 'gs131')"], {"degats": [["gs076", 0], ["gs131", 2]]}),
    _c("gs083 ranged, TEMOIN : sans l'arme, le Jailor riposte (1 degat sur Kree Sentry)",
       "contre-cas", DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs131')"], ["Puzzle.EnemyAttacks('gs076', 'gs131')"],
       {"degats": [["gs076", 1], ["gs131", 1]]}),
    _c("gs083 Hero Action : depenser [physical][physical] -> defausser Optic Blast Cannon",
       "PlayerActionToDiscardThis + Cost(\"RR\") (modele 01118) ; icones = poings (physique)",
       DECK_NEUTRE + [HEROS, "Puzzle.PutIntoPlay('gs083')"], ["Puzzle.Action('gs083')"],
       {"hors_jeu": ["gs083"]}, main_exclusive=["01090"]),
    _c("gs083 Hero Action, TEMOIN : sans [physical][physical] (deux [energy]) la carte reste attachee",
       "le cout exige deux ressources PHYSIQUES",
       DECK_NEUTRE + [HEROS, "Puzzle.PutIntoPlay('gs083')"], [],
       {"en_jeu": ["gs083"]}, main_exclusive=["01088"], declencher_tolerant=["Puzzle.Action('gs083')"]),
    _c("gs083 Boost : l'activation recoit Optic Blast Cannon en boost -> l'attaque gagne piercing (Tenace de Rick defaussee), ATQ 1 + 1 icone = 2 degats",
       "« If this activation is an attack, it gains piercing and ranged » (modele 50160)",
       DECK_NEUTRE + [HEROS, "Puzzle.Tough('gs081')"], ["Puzzle.Boost('gs083')"],
       {"degats": [["gs081", 2]], "statuts_absents": [["gs081", "Tough"]]}, **SANS_DEFENSE),
    _c("gs083 Boost : activation de MANIGANCE (alter ego) -> aucun effet de boost (menace 2 + SCH 2 + 1 icone)",
       "« IF this activation is an attack » : rien sur une manigance",
       DECK_NEUTRE, ["Puzzle.Boost('gs083')"], {"menace": [["gs079b", 5]]}),
    # ============================================================== gs084 : Repulsor Blast Unit
    _c("gs084 Repulsor Blast Unit : attache a Kree Sentry, +1 ATQ", "badge `desc.ATK+` ; « Attach to Kree Sentry »",
       DECK_NEUTRE, ["Puzzle.PutIntoPlay('gs084')"],
       {"accroche_a": [["gs084", "gs076"]], "attributs_carte": [["gs076", "attack", 1]]}),
    _c("gs084 « attacks gain overkill » : Kree Sentry (ATQ 2) abat Shocker a 1 PV, l'exces (1) va au mechant lui-meme",
       "overkill : RR 1.8 p.31, l'exces d'un sbire abattu va a « le mechant » = Kree Sentry (livret p.9)",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs084')", "Puzzle.PutIntoPlay('01103')", "Puzzle.Damage('01103', 2)"],
       ["Puzzle.EnemyAttacks('gs076', '01103')"], {"hors_jeu": ["01103"], "degats": [["gs076", 1]]}),
    _c("gs084 overkill, TEMOIN : sans l'unite, aucun exces ne retourne a Kree Sentry (ATQ 1, Shocker a 1 PV)",
       "contre-cas", DECK_NEUTRE + ["Puzzle.PutIntoPlay('01103')", "Puzzle.Damage('01103', 2)"],
       ["Puzzle.EnemyAttacks('gs076', '01103')"], {"hors_jeu": ["01103"], "degats": [["gs076", 0]]}),
    _c("gs084 ranged : l'attaque de Kree Sentry contre le Jailor ne subit pas de riposte",
       "« overkill and ranged »",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs084')", "Puzzle.PutIntoPlay('gs131')"],
       ["Puzzle.EnemyAttacks('gs076', 'gs131')"], {"degats": [["gs076", 0], ["gs131", 2]]}),
    _c("gs084 Forced Interrupt : une Poigne a 5 degats (Death Grip en jeu) va etre mise de cote -> Repulsor Blast Unit defaussee",
       "« When Sentry's Grasp would be set aside, if there is 5 or more damage on it, discard Repulsor Blast Unit »",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs084')", "Puzzle.PutIntoPlay('gs085')"],
       ["Puzzle.PlaceCounters('gs082', 'damage', 5)"], {"hors_jeu": ["gs084"], "poignes_de_cote": 2}),
    _c("gs084 Forced Interrupt, TEMOIN : une Poigne mise de cote a 3 degats seulement -> Repulsor reste attachee",
       "« if there is 5 or more damage on it »",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs084')"], ["Puzzle.PlaceCounters('gs082', 'damage', 3)"],
       {"en_jeu": ["gs084"], "poignes_de_cote": 2}),
    _c("gs084 Forced Interrupt : 5 degats poses d'un coup SANS Death Grip (seuil 3) -> la Poigne part de cote avec 5 degats, Repulsor defaussee",
       "« if there is 5 or more damage on it » : l'etat compte, pas le seuil de la Poigne",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs084')"], ["Puzzle.PlaceCounters('gs082', 'damage', 5)"],
       {"hors_jeu": ["gs084"], "poignes_de_cote": 2}),
    _c("gs084 Forced Interrupt, TEMOIN : 4 degats d'un coup (seuil 3) -> la Poigne part de cote mais Repulsor reste",
       "4 < 5", DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs084')"], ["Puzzle.PlaceCounters('gs082', 'damage', 4)"],
       {"en_jeu": ["gs084"], "poignes_de_cote": 2}),
    _c("gs084 Boost : l'attaque de l'activation gagne overkill (ATQ 1 + 1 icone, Shocker a 1 PV : 1 d'exces)",
       "« If this activation is an attack, it gains overkill » : l'activation attaque le heros, Rick Jones prend",
       DECK_NEUTRE + [HEROS], ["Puzzle.Boost('gs084')"], {"degats": [["gs081", 2]]}, **SANS_DEFENSE),
    # ============================================================== gs085 : Death Grip
    _c("gs085 valeurs : menace de depart 3[per_hero] (un joueur : 3), aucun Hinder",
       "StartingThreat 3*", DECK_NEUTRE, ["Puzzle.PutIntoPlay('gs085')"], {"menace": [["gs085", 3]]}),
    _c("gs085 « set aside when there is 5 or more damage instead of 3 » : 3 degats -> la Poigne RESTE attachee",
       "seuil 5 tant que Death Grip est en jeu", DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs085')"],
       ["Puzzle.PlaceCounters('gs082', 'damage', 3)"], {"poignes_sur": [["gs081", 1]], "compteurs": [["gs082", "damage", 3]]}),
    _c("gs085 : 4 degats -> toujours attachee", "seuil 5", DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs085')"],
       ["Puzzle.PlaceCounters('gs082', 'damage', 4)"], {"poignes_sur": [["gs081", 1]]}),
    _c("gs085 : 5 degats -> mise de cote", "seuil 5 atteint", DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs085')"],
       ["Puzzle.PlaceCounters('gs082', 'damage', 5)"], {"poignes_sur": [["gs081", 0]], "poignes_de_cote": 2}),
    _c("gs085 : Death Grip s'en va avec une Poigne a 4 degats -> « 3 or more damage here » : elle tombe de cote aussitot",
       "retour au seuil 3 : l'etat « 3 degats ou plus » est vrai (lecture, Q4)",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs085')", "Puzzle.PlaceCounters('gs082', 'damage', 4)"],
       ["Puzzle.SetThreat('gs085', 0)"], {"poignes_sur": [["gs081", 0]], "poignes_de_cote": 2, "hors_jeu": ["gs085"]}),
    # ============================================================== gs086 : Locking on Target
    _c("gs086 Hinder 1[per_hero] : revelee, 3 + 1 = 4 menaces (un joueur)",
       "base automatique `desc.Hinder` (fiche hinder.md)", DECK_NEUTRE, ["Puzzle.Reveal('gs086')"], {"menace": [["gs086", 4]]}),
    _c("gs086 Amplify : l'icone « avion + croix » (identique a sk252) est comptee par le moteur",
       "base automatique `desc.Amplify` (fiche amplify.md)", DECK_NEUTRE, ["Puzzle.PutIntoPlay('gs086')"],
       {"icones": [["Amplify", 1]]}),
    _c("gs086 Amplify : l'activation de Kree Sentry (alter ego) qui retourne un boost a 1 icone en recoit une de plus (2 + SCH 2 + 1 + 1 = 6)",
       "Amplify ajoute une icone de boost a la carte retournee (1 icone imprimee + 1)",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs086')"], ["Puzzle.Boost('gs089')"],
       {"menace": [["gs079b", 6]], "principale": "gs079b"}),
    _c("gs086 Amplify, TEMOIN : sans Locking on Target, la meme activation donne 2 + 2 + 1 = 5",
       "contre-cas", DECK_NEUTRE, ["Puzzle.Boost('gs089')"], {"menace": [["gs079b", 5]]}),
    # ============================================================== gs087 : Outpost Collapse Protocol
    _c("gs087 Hinder 2[per_hero] : revelee, 1 + 2 = 3 menaces (un joueur)",
       "base automatique `desc.Hinder`", DECK_NEUTRE, ["Puzzle.Reveal('gs087')"], {"menace": [["gs087", 3]]}),
    _c("gs087 Forced Response apres l'etape 1 : le premier joueur inflige 1 degat a chaque personnage qu'il controle (identite + Rick Jones)",
       "« the first player deals 1 damage to each character they control »",
       DECK_NEUTRE + [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('gs087')", "Puzzle.PutIntoPlay('01075', under_control=True)"], [],
       {"degats_identite": 1, "degats": [["gs081", 2], ["01075", 1]]}, verifier="ks_etape_un"),
    _c("gs087 Forced Response, TEMOIN : un sbire (Shocker) n'est pas un personnage que le joueur controle",
       "« each character THEY CONTROL »",
       DECK_NEUTRE + ["Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('gs087')", "Puzzle.PutIntoPlay('01103')"], [],
       {"degats": [["01103", 0]]}, verifier="ks_etape_un"),
    _c("gs087 Forced Response : seul le PREMIER joueur subit (deux joueurs : le second heros est intact)",
       "« the FIRST player »",
       DECK_NEUTRE + [HEROS, "Puzzle.EmptyHand()", "Puzzle.PutIntoPlay('gs087')"], [],
       {"degats_identite": 1}, heros2="spider_man", verifier="ks_etape_un"),
    # ============================================================== gs088 : "Gotcha!"
    _c("gs088 When Revealed : la Poigne de cote s'attache a Rick Jones (2 sur lui)",
       "« Attach a set aside copy of Sentry's Grasp to Rick Jones »", DECK_NEUTRE, ["Puzzle.Reveal('gs088')"],
       {"poignes_sur": [["gs081", 2]], "poignes_de_cote": 0}),
    _c("gs088 When Revealed : AUCUNE Poigne de cote -> la carte gagne surge (la carte semee au dessus du deck est revelee)",
       "« If you cannot, this card gains surge »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('gs086', '01186')"],
       ["Puzzle.Reveal('gs088')"], {"poignes_sur": [["gs081", 2]], "carte_du_surge": "gs086"}, scenario=SCE),
    _c("gs088 Boost : l'activation retourne « Gotcha! » en boost -> la Poigne de cote s'attache a Rick Jones",
       "« [star] Boost: Attach a set aside copy of Sentry's Grasp to Rick Jones » (aucune icone de boost)",
       DECK_NEUTRE, ["Puzzle.Boost('gs088')"], {"poignes_sur": [["gs081", 2]], "poignes_de_cote": 0}),
    # ============================================================== gs089 : Caught in Its Sights
    _c("gs089 When Revealed : le joueur depense 2 ressources -> Kree Sentry n'attaque pas Rick Jones",
       "« You may spend 2 resources of any type » (modele 28024 War Delivery) ; main de deux cartes ressource",
       DECK_NEUTRE, ["Puzzle.Reveal('gs089')"], {"degats": [["gs081", 0]], "poignes_sur": [["gs081", 1]]},
       main_exclusive=["01088", "01089"]),
    _c("gs089 When Revealed : AUCUNE ressource a depenser -> Kree Sentry attaque Rick Jones (1 degat, une Poigne de plus)",
       "« If you do not, Kree Sentry attacks Rick Jones » ; main vide",
       DECK_NEUTRE + ["Puzzle.EmptyHand()"], ["Puzzle.Reveal('gs089')"],
       {"degats": [["gs081", 1]], "poignes_sur": [["gs081", 2]]}, **SANS_DEFENSE),
    _c("gs089 attaque sur Rick Jones : le heros peut DEFENDRE (DEF 3 contre ATQ 1 : 0 degat, heros incline)",
       "livret p.4 : les joueurs defendent comme d'habitude (decision du 20/10/2026)",
       DECK_NEUTRE + [HEROS, "Puzzle.EmptyHand()"], ["Puzzle.Reveal('gs089')"],
       {"degats": [["gs081", 0]], "exhausted": ["01001a"]}),
    # ============================================================== gs090 : Intruder Elimination
    _c("gs090 When Revealed : cible = un SBIRE (Shocker) -> Kree Sentry l'attaque (1 degat) et la carte gagne surge",
       "« If an enemy was attacked this way, this card gains surge » ; les joueurs peuvent defendre (decision du 20/10/2026)",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('gs086', '01186')", "Puzzle.PutIntoPlay('01103')"],
       ["Puzzle.Reveal('gs090')"], {"degats": [["01103", 1]], "en_jeu": ["gs086"]}, cibles=["01103"], **SANS_DEFENSE),
    _c("gs090 When Revealed : cible = l'identite du PREMIER joueur -> Kree Sentry attaque Rick Jones (FAQ p.22), pas de surge",
       "FAQ du livret : « Kree Sentry attacks Rick Jones (his Forced Interrupt changes the target) »",
       DECK_NEUTRE + [HEROS], ["Puzzle.Reveal('gs090')"],
       {"degats": [["gs081", 1]], "degats_identite": 0}, cibles=["01001a"], **SANS_DEFENSE),
    _c("gs090 When Revealed : cible = un ALLIE (Black Widow) -> Kree Sentry l'attaque, pas de surge",
       "« attacks that character » ; livret p.4 : allie attaque directement",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('12012', under_control=True)"], ["Puzzle.Reveal('gs090')"],
       {"degats": [["12012", 1]], "poignes_sur": [["12012", 1]]}, cibles=["12012"], **SANS_DEFENSE),
    _c("gs090 « non-KREE » : Kree Sentry n'est PAS une cible proposee",
       "les choix ne contiennent ni Kree Sentry ni la Poigne",
       DECK_NEUTRE + [HEROS, "Puzzle.PutIntoPlay('01103')"], ["Puzzle.Reveal('gs090')"],
       {"option": "When Revealed", "porteur": "gs090", "contient": ["01103", "01001a", "gs081"], "exclut": ["gs076", "gs082"]},
       verifier="cibles_legales_proposees", **SANS_DEFENSE),
]

CAS += []

VERIFICATIONS = r'''
def _ks_poignes_sur(monde, host_id):
    for objet in monde.object_manager.card_dict.values():
        f = objet.face
        if f is not None and f.IsInPlay() and getattr(f.paper, "card_id", None) == host_id:
            return [a for a in f.GetAttachedAttachments() if getattr(a.paper, "card_id", None) == "gs082"]
    return None


def _ks_toutes_poignes(monde):
    return [objet.face for objet in monde.object_manager.card_dict.values()
            if objet.face is not None and getattr(objet.face.paper, "card_id", None) == "gs082"]


def ks_etat(monde, aides):
    """etat_attendu (cles communes) + cles propres au scenario Kree Sentry : poignes_sur [[hote, n]],
    poignes_de_cote n, poignes_en_jeu n, defaite, victoire, mechant_id, principale, dans_deck_rencontre_n
    [[card_id, n]], defausse_rencontre_n [[card_id, n]]."""
    attendu = aides["cas"].get("attendu") or {}
    connues = set(CLES_ETAT_ATTENDU) | {"poignes_sur", "poignes_de_cote", "poignes_en_jeu", "defaite", "victoire",
                                        "mechant_id", "principale", "dans_deck_rencontre_n", "defausse_rencontre_n",
                                        "sous_controle", "allies_comptes"}
    inconnues = sorted(set(attendu) - connues)
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de ks_etat : {inconnues}"
    ok, message = etat_attendu(monde, aides)
    soucis = [] if ok else [message]
    for hote, n in attendu.get("poignes_sur") or []:
        poignes = _ks_poignes_sur(monde, hote)
        if poignes is None:
            soucis.append(f"{hote} introuvable en jeu (poignes_sur)")
        elif len(poignes) != n:
            soucis.append(f"poignes sur {hote} = {len(poignes)} (attendu {n})")
    toutes = _ks_toutes_poignes(monde)
    de_cote = [f for f in toutes if str(f.card.area.deck_type).endswith('AsideDeck')]
    en_jeu = [f for f in toutes if f.IsInPlay()]
    if "poignes_de_cote" in attendu and len(de_cote) != attendu["poignes_de_cote"]:
        soucis.append(f"poignes mises de cote = {len(de_cote)} (attendu {attendu['poignes_de_cote']}) ; en jeu {len(en_jeu)}")
    if "poignes_en_jeu" in attendu and len(en_jeu) != attendu["poignes_en_jeu"]:
        soucis.append(f"poignes en jeu = {len(en_jeu)} (attendu {attendu['poignes_en_jeu']})")
    if "defaite" in attendu:
        perdu = bool(monde.is_game_over) and not monde.game_over.players_won
        if perdu != attendu["defaite"]:
            soucis.append(f"defaite = {perdu} (attendu {attendu['defaite']}, partie terminee = {monde.is_game_over})")
    if "victoire" in attendu:
        gagne = bool(monde.is_game_over) and bool(monde.game_over.players_won)
        if gagne != attendu["victoire"]:
            soucis.append(f"victoire = {gagne} (attendu {attendu['victoire']}, partie terminee = {monde.is_game_over})")
    if "mechant_id" in attendu:
        from game.operate.worlds import Worlds
        vilains = [getattr(v.paper, "card_id", None) for v in Worlds.GetAllVillains(monde)]
        if attendu["mechant_id"] not in vilains:
            soucis.append(f"mechant en jeu = {vilains} (attendu {attendu['mechant_id']})")
    if "principale" in attendu:
        from game.operate.worlds import Worlds
        mains = [getattr(m.paper, "card_id", None) for m in Worlds.GetAllMainSchemes(monde)]
        if attendu["principale"] not in mains:
            soucis.append(f"manigance principale = {mains} (attendu {attendu['principale']})")
    for card_id in attendu.get("sous_controle") or []:
        face = aides["par_id"](monde, card_id)
        controle = face.GetControlBy() if face is not None else None
        if face is None or controle is None or not controle.IsPlayer():
            soucis.append(f"{card_id} n'est pas en jeu sous le controle d'un joueur")
    if "allies_comptes" in attendu:
        from game.message import Message
        joueur = monde.players[0]
        n = 0
        for allie in joueur.GetControlAllies():
            m = Message.CheckIfAllyCountLimit(allie)
            m.Send()
            if not m.not_count:
                n += 1
        if n != attendu["allies_comptes"]:
            soucis.append(f"allies comptes dans la limite = {n} (attendu {attendu['allies_comptes']})")
    for card_id, n in attendu.get("dans_deck_rencontre_n") or []:
        from game.operate.worlds import Worlds
        reel = sum(1 for f in Worlds.GetEncounterDeckCards(monde) if getattr(f.paper, "card_id", None) == card_id)
        if reel != n:
            soucis.append(f"{card_id} dans le deck rencontre = {reel} (attendu {n})")
    for card_id, n in attendu.get("defausse_rencontre_n") or []:
        from game.operate.worlds import Worlds
        reel = sum(1 for f in Worlds.GetEncounterDiscardPileCards(monde) if getattr(f.paper, "card_id", None) == card_id)
        if reel != n:
            soucis.append(f"{card_id} dans la defausse rencontre = {reel} (attendu {n})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "ok"


def ks_etape_un(monde, aides):
    """Envoie la fin de l'ETAPE 1 de la phase du mechant (`AfterResolveVillainPhaseStep(1)`), exactement comme
    `process_villain_phase_step`, puis mesure par ks_etat."""
    from game.message import Message
    debut = Message.WhenVillainPhaseStepStart(1, monde)
    debut.Send()
    Message.AfterResolveVillainPhaseStep(1, debut).Send()
    return ks_etat(monde, aides)


def ks_sonde_etape(monde, aides):
    from game.message import Message
    debut = Message.WhenVillainPhaseStepStart(1, monde)
    debut.Send()
    Message.AfterResolveVillainPhaseStep(1, debut).Send()
    return ks_sonde(monde, aides)


def ks_sonde(monde, aides):
    """SONDE de mise au point (jamais dans la batterie finale) : decrit l'etat, rend toujours False."""
    lignes = []
    for objet in monde.object_manager.card_dict.values():
        f = objet.face
        if f is None:
            continue
        cid = getattr(f.paper, "card_id", "")
        if not cid.startswith("gs") and not (cid.startswith("010") and f.IsInPlay()):
            continue
        extra = ""
        try:
            extra = ":dmg=" + str(f.GetCounters('damage'))
        except Exception:
            pass
        lignes.append(f"{cid}:{type(f).__name__}:{getattr(f.card.area, 'deck_type', '?')}"
                      f":jeu={f.IsInPlay()}:menace={getattr(f, 'threat', None)}"
                      f":pv={getattr(f, 'health', None)}:att={getattr(getattr(f, 'bind_face', None), 'paper', None) and f.bind_face.paper.card_id}{extra}")
    lignes.append(f"fin={monde.is_game_over}")
    lignes.append("prompts=" + str((aides.get("etat") or {}).get("prompts", []))[:600])
    lignes.append("prompts_options=" + str((aides.get("etat") or {}).get("options_vues", []))[:300])
    lignes.append("prompts_cibles=" + str((aides.get("etat") or {}).get("cibles_legales", []))[:600])
    return False, " | ".join(sorted(lignes))
'''
