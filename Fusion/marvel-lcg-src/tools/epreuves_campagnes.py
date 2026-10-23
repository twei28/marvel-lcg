"""Les EPREUVES de boucle de campagne, boite par boite.

Lue par `tools/test_campagnes.py`, qui est generique : ce fichier-ci est la
connaissance de chaque boite — ce qu'une victoire laisse au carnet, et ce que
le carnet doit changer a la mise en place SUIVANTE.

Forme d'une epreuve
-------------------
    {
      "nom":       ce qui sera lu au rapport ; commence par le code de la boite
      "scenario":  le scenario de la partie 1 (data/scenarios/<id>.json)
      "heros":     un nom de deck de depart, ou une liste pour le multijoueur
      "carnet":    le carnet ENTRANT de la partie 1 (facultatif)
      "avant":     commandes `Puzzle.*` posant l'etat que la recompense exige
      "fin":       "Win" (defaut) ou "Lose"
      "carnet_attendu": {gagnee, scenario, cles, cles_presentes, cles_absentes}
      "choix":     ce que le JOUEUR coche au panneau, fusionne au carnet sortant
      "suivant":   le scenario de la partie 2 (absent = on s'arrete au carnet)
      "attendu":   l'etat attendu APRES la mise en place de la partie 2
    }

`attendu` connait : en_jeu, main, deck, defausse, retirees, victoire, de_cote
(et leur negation `pas_<zone>`), en_jeu_trait, compteurs, statuts, menace,
taille_main, taille / taille_min / taille_max (par pile, « deck », « deck@2 »),
compteurs_total, perdue (la mise en place perd la partie),
parmi (la carte est dans l'une des piles citees), un_parmi / aucune_parmi
(au moins une, ou aucune, des cartes citees dans une pile), menace_max, et la zone
« rencontres_recues » (cartes rencontre distribuees face cachee),
pv_identite, degats_identite, degats (sur une carte quelconque). Une entree de zone peut etre
`[card_id, joueur]` pour viser un autre siege.
"""

EPREUVES = []


# ============================================================ Fear No Evil (fne)
#
# Carnet : « Completed Scenarios » / « Failed Scenarios » (listes ;),
# « Progress: <affaire> », « Villain: <affaire> », « Trust Established? »,
# « Mary Defeated? », « Allies removed from the campaign », et les PV restants
# par joueur en campagne experte. L'ecran ecrit les marques et les echecs, le
# moteur ecrit le reste (cards/pack/fne/campaign.py).
EPREUVES += [
    {
        "nom": "fne — victoire sur Le casse du musee : l'affaire est cochee, et son environnement Complete entre en jeu au scenario suivant",
        "scenario": "art_museum_heist_hammerhead",
        "heros": "spider_man",
        "carnet_attendu": {
            "gagnee": True,
            "scenario": "art_museum_heist",
            "cles": {"Completed Scenarios": "art_museum_heist"},
            "cles_presentes": ["Player 1 Remaining hit points", "Player 1 Identity"],
        },
        "suivant": "the_getaway_hammerhead",
        "attendu": {"en_jeu": ["60205a"], "pas_en_jeu": ["60205b"], "statuts": [["01001b", "Tough"]]},
    },
    {
        "nom": "fne — DEFAITE sur Le casse du musee : rien n'est coche, et le scenario suivant n'a aucun environnement",
        "scenario": "art_museum_heist_hammerhead",
        "heros": "spider_man",
        "fin": "Lose",
        "carnet_attendu": {
            "gagnee": False,
            "scenario": "art_museum_heist",
            "cles_absentes": ["Completed Scenarios"],
            "cles_presentes": ["Player 1 Remaining hit points"],
        },
        "suivant": "the_getaway_hammerhead",
        "attendu": {"pas_en_jeu": ["60205a", "60205b"]},
    },
    {
        "nom": "fne — affaire ECHOUEE (coche par l'ecran) : l'environnement entre en jeu cote Echoue au scenario suivant",
        "scenario": "art_museum_heist_hammerhead",
        "heros": "spider_man",
        "fin": "Lose",
        "carnet_attendu": {"gagnee": False},
        # Ce que l'ecran de campagne inscrit quand une affaire atteint trois marques.
        "choix": {"Failed Scenarios": "art_museum_heist"},
        "suivant": "the_getaway_hammerhead",
        "attendu": {"en_jeu": ["60205b"], "pas_en_jeu": ["60205a"]},
    },
    {
        "nom": "fne — un allie unique retire du jeu rejoint le carnet, et il a disparu du deck au scenario suivant",
        "scenario": "art_museum_heist_hammerhead",
        "heros": "spider_man",
        "avant": ["Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.Remove('01002')"],
        "carnet_attendu": {"cles": {"Allies removed from the campaign": "Black Cat"}},
        "suivant": "the_getaway_hammerhead",
        "attendu": {"pas_deck": ["01002"], "pas_main": ["01002"]},
    },
    {
        "nom": "fne — marques de progression (ecrites par l'ecran) : deux marques posent deux menaces de plus sur le complot suivant",
        "scenario": "art_museum_heist_hammerhead",
        "heros": "spider_man",
        "carnet_attendu": {"gagnee": True},
        "choix": {"Progress: the_getaway": "2", "Completed Scenarios": None},
        "suivant": "the_getaway_hammerhead",
        # 60131 Jackknifed Tanker Truck est trouve et revele par les marques
        # (2 menaces imprimees + Hinder 1 + 1 par marque au-dela de la premiere).
        "attendu": {"en_jeu": ["60131"]},
    },
    {
        "nom": "fne — Kingpin : trois affaires completees rendent chaque sbire en jeu robuste a la mise en place",
        "scenario": "art_museum_heist_hammerhead",
        "heros": "spider_man",
        "carnet": {"Completed Scenarios": "the_getaway;protection_racket"},
        "carnet_attendu": {"cles": {"Completed Scenarios": "the_getaway;protection_racket;art_museum_heist"}},
        "suivant": "kingpin_fne",
        "attendu": {"en_jeu": ["60206a", "60207a", "60205a"]},
    },
]


# ========================================== L'Avenement de Crane Rouge (trors)
#
# La premiere campagne du jeu, et la plus explicite sur ce qu'on emporte :
# `cards/pack/trors/campaign.py` remet en jeu l'amelioration choisie A CHAQUE
# partie suivante (des le scenario 2), melange les armes experimentales dans le
# deck rencontre, et rend au deck les allies secourus (des le scenario 4).
# Le scenario final (`04128a`) relit trois cles de plus : les pions retard, les
# joueurs engages, et les allies retires de la campagne.
EPREUVES += [
    {
        "nom": "trors — l'amelioration technologique choisie est REMISE EN JEU a chaque partie suivante",
        "scenario": "crossbones",
        "heros": "captain_america",
        # Ce que le joueur coche au panneau : une des quatre ameliorations.
        "choix": {"Player 1 Tech Upgrade": "04155"},
        "suivant": "absorbing_man",
        "attendu": {"en_jeu": ["04155"]},
    },
    {
        "nom": "trors — l'amelioration de base choisie entre aussi en jeu, et sa version SUPERIEURE la remplace au scenario suivant",
        "scenario": "absorbing_man",
        "heros": "captain_america",
        "carnet": {"Player 1 Tech Upgrade": "04155"},
        "choix": {"Player 1 Basic Upgrade": "04159b"},
        "suivant": "taskmaster",
        # L'amelioration technologique tient toujours, et la version superieure
        # a bien pris la place de la version de base.
        "attendu": {"en_jeu": ["04155", "04159b"], "pas_en_jeu": ["04159a"]},
    },
    {
        "nom": "trors — les armes experimentales entrees en jeu sont melangees au deck rencontre de la partie suivante",
        "scenario": "crossbones",
        "heros": "captain_america",
        "choix": {"Experimental Weapons added to encounter deck": "04072;04073"},
        "suivant": "absorbing_man",
        # Elles n'entrent pas en jeu : elles sont DANS le deck rencontre.
        "attendu": {"pas_en_jeu": ["04072", "04073"], "deck_rencontre": ["04072", "04073"]},
    },
    {
        "nom": "trors — les allies secourus rejoignent le deck du joueur au scenario 4",
        "scenario": "taskmaster",
        "heros": "captain_america",
        "choix": {"Player 1 Rescued Allies": "04097;04098"},
        "suivant": "zola",
        "attendu": {"deck": ["04097", "04098"]},
    },
    {
        "nom": "trors — les pions retard du carnet posent autant de menace sur la manigance finale",
        "scenario": "zola",
        "heros": "captain_america",
        "choix": {"Number of delay counters on main scheme": "3"},
        "suivant": "red_skull",
        # 04128b : la manigance du scenario final. Menace de depart + 3.
        "attendu": {"menace_min": [["04128b", 3]]},
    },
    {
        "nom": "trors — un allie retire de la campagne ne revient pas au scenario final",
        "scenario": "zola",
        "heros": "captain_america",
        "choix": {"Allies removed from the campaign": "04097", "Player 1 Rescued Allies": "04097"},
        "suivant": "red_skull",
        # Il est rendu au deck par la recompense, PUIS retire par le scenario.
        "attendu": {"pas_deck": ["04097"], "retirees": ["04097"]},
    },
]


# ================================== L'Ombre du Titan Fou (mts) — 5 scenarios
#
# La boite la plus riche en recompenses AUTOMATIQUES : le moteur
# (`cards/pack/mts/campaign.py`, `CollectMTS`) regarde l'etat de la table a la
# fin de la partie et en deduit tout seul ce que le joueur emporte. Deux
# familles :
#   — « Campaign Pool: X » : un renfort (Cosmo, Black Swan, Odin, Norn Stone)
#     ou une nuisance (Security Breach, Shawarma, System Shock) verse a la
#     reserve de campagne, relu par `InPool` a la mise en place suivante ;
#   — les deux PUNITIONS (« Avengers Tower Damaged », « The Infinity Stones 1B
#     completed »), relues par `LogSet`, qui frappent des la mise en place.
# Chaque epreuve joue la partie qui PRODUIT la cle, puis monte la partie qui
# la SUBIT : c'est la chaine entiere, pas la moitie.
EPREUVES += [
    {
        "nom": "mts — Cosmo libere au scenario 1 : le carnet le note, et il entre en jeu sous controle au scenario 3",
        "scenario": "ebony_maw",
        "heros": "captain_america",
        # 21180a « Secure the Landing Pad » vaincu se retourne sur 21180b
        # « * Cosmo » : c'est cette face que CollectMTS cherche en jeu.
        "avant": ["Puzzle.Flip('21180a')"],
        "carnet_attendu": {
            "gagnee": True,
            "cles": {"Campaign Pool: Cosmo": "1"},
            "cles_absentes": ["Campaign Pool: Security Breach"],
        },
        "suivant": "thanos",
        "attendu": {"en_jeu": ["21180b"]},
    },
    {
        "nom": "mts — scenario 3 : la manigance de campagne Hack Sanctuary's Computer est recto-verso (elle se retourne, elle ne se couche pas)",
        "scenario": "the_tower_defense",
        "heros": "captain_america",
        "carnet_attendu": {"gagnee": True},
        "suivant": "thanos",
        "attendu": {"en_jeu": ["21184a"], "avec_dos": ["21184a"]},
    },
    {
        "nom": "mts — Cosmo NON libere : rien au carnet, et aucun allie de campagne au scenario 3",
        "scenario": "ebony_maw",
        "heros": "captain_america",
        "carnet_attendu": {"gagnee": True, "cles_absentes": ["Campaign Pool: Cosmo"]},
        "suivant": "thanos",
        "attendu": {"pas_en_jeu": ["21180b"]},
    },
    {
        "nom": "mts — la Pierre de Puissance atteinte au scenario 1 : la breche de securite est melangee au deck rencontre du scenario 2",
        "scenario": "ebony_maw",
        "heros": "captain_america",
        # Deux pas : 21074a se retourne sur 21074b, puis l'etape 2 (21075a
        # « The Power Stone ») prend sa place. C'est l'etape que CollectMTS lit.
        "avant": ["Puzzle.AdvanceMainScheme(2)"],
        "carnet_attendu": {"cles": {"Campaign Pool: Security Breach": "1"}},
        "suivant": "the_tower_defense",
        "attendu": {"pas_en_jeu": ["21181"], "deck_rencontre": ["21181"]},
    },
    {
        "nom": "mts — Shawarma ET Black Swan au scenario 2 : la carte rejoint le deck du joueur et l'alliee entre en jeu au scenario 3",
        "scenario": "the_tower_defense",
        "heros": "captain_america",
        # 21182a « Save the Shawarma Place » retourne sur 21182b « * Black
        # Swan » : la carte existe (Shawarma), et elle n'est pas dans la pile
        # de victoire (Black Swan reste avec vous).
        "avant": ["Puzzle.Flip('21182a')"],
        "carnet_attendu": {
            "cles": {"Campaign Pool: Shawarma": "1", "Campaign Pool: Black Swan": "1"},
        },
        "suivant": "thanos",
        # La mise en place de campagne precede la pioche (annexe II du guide
        # de reference, etapes 13 puis 14) : le shawarma peut deja etre en main.
        "attendu": {"parmi": [["21183", ["deck", "main"]]], "en_jeu": ["21182b"]},
    },
    {
        "nom": "mts — Black Swan mise en pile de victoire : le shawarma reste, mais l'alliee ne revient pas",
        "scenario": "the_tower_defense",
        "heros": "captain_america",
        "avant": [
            "Puzzle.Flip('21182a')",
            "Puzzle.MoveTo('21182b', 'VictoryDisplay')",
        ],
        "carnet_attendu": {
            "cles": {"Campaign Pool: Shawarma": "1"},
            "cles_absentes": ["Campaign Pool: Black Swan"],
        },
        "suivant": "thanos",
        "attendu": {"parmi": [["21183", ["deck", "main"]]], "pas_en_jeu": ["21182b"]},
    },
    {
        "nom": "mts — la Tour des Vengeurs endommagee au scenario 2 : chaque identite subit 3 degats a la mise en place du scenario 3",
        "scenario": "the_tower_defense",
        "heros": "captain_america",
        "avant": ["Puzzle.PutIntoPlay('21100b')"],
        "carnet_attendu": {"cles": {"Avengers Tower Damaged": "1"}},
        "suivant": "thanos",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "mts — les protocoles defensifs NON vaincus au scenario 3 : le court-circuit est melange au deck du joueur au scenario 4",
        "scenario": "thanos",
        "heros": "captain_america",
        # Rien a poser : 21184b « Defensive Protocols » absent de la pile de
        # victoire suffit, et c'est le cas par defaut.
        "carnet_attendu": {"cles": {"Campaign Pool: System Shock": "1"}},
        "suivant": "hela",
        "attendu": {"parmi": [["21185", ["deck", "main"]]]},
    },
    {
        "nom": "mts — les protocoles defensifs VAINCUS : aucun court-circuit au scenario suivant",
        "scenario": "thanos",
        "heros": "captain_america",
        "avant": [
            "Puzzle.Flip('21184a')",
            "Puzzle.MoveTo('21184b', 'VictoryDisplay')",
        ],
        "carnet_attendu": {"cles_absentes": ["Campaign Pool: System Shock"]},
        "suivant": "hela",
        "attendu": {"pas_deck": ["21185"], "pas_main": ["21185"]},
    },
    {
        "nom": "mts — la balance des Pierres atteinte au scenario 3 : le joueur defausse la moitie de son deck a la mise en place du scenario 4",
        "scenario": "thanos",
        "heros": "captain_america",
        # 21115 « Balance the Scales » : l'etape que CollectMTS lit pour
        # « The Infinity Stones 1B completed ».
        "avant": ["Puzzle.AdvanceMainScheme(2)"],
        "carnet_attendu": {"cles": {"The Infinity Stones 1B completed": "1"}},
        "suivant": "hela",
        "attendu": {"taille_min": {"defausse": 10}},
    },
    {
        "nom": "mts — sans la balance des Pierres : le deck du scenario 4 est intact, la defausse vide",
        "scenario": "thanos",
        "heros": "captain_america",
        "carnet_attendu": {"cles_absentes": ["The Infinity Stones 1B completed"]},
        "suivant": "hela",
        "attendu": {"taille": {"defausse": 0}},
    },
    {
        "nom": "mts — la pierre de Norn rapportee au scenario 4 : elle est attachee a l'identite au scenario 5",
        "scenario": "hela",
        "heros": "captain_america",
        # 21186b « Retrieve Odin's Armor » existe (la quete a ete retournee)
        # mais n'est pas en pile de victoire : la pierre, pas l'armure.
        "avant": ["Puzzle.Flip('21186a')"],
        "carnet_attendu": {
            "cles": {"Campaign Pool: Norn Stone": "1"},
            "cles_absentes": ["Campaign Pool: Odin"],
        },
        "suivant": "loki",
        "attendu": {"en_jeu": ["21187a"]},
    },
    {
        "nom": "mts — l'armure d'Odin recuperee au scenario 4 : Odin entre en jeu sous controle au scenario 5",
        "scenario": "hela",
        "heros": "captain_america",
        "avant": [
            "Puzzle.Flip('21186a')",
            "Puzzle.MoveTo('21186b', 'VictoryDisplay')",
        ],
        "carnet_attendu": {
            "cles": {"Campaign Pool: Norn Stone": "1", "Campaign Pool: Odin": "1"},
        },
        "suivant": "loki",
        "attendu": {"en_jeu": ["21139b", "21187a"]},
    },
]


# ============================= Les plus recherches de la galaxie (gmw) — 5 scenarios
#
# Deux mecaniques par-dessus les recompenses ordinaires :
#   — le CHASSEUR DE TETES badoon (16183) revient a chaque scenario, et chaque
#     defaite lui ajoute un renfort au scenario SUIVANT, par paliers cumulatifs
#     (livret p.18) : c'est la seule mecanique du jeu ou bien jouer durcit la
#     suite ;
#   — les UNITES, gagnees a chaque victoire et depensees au Marche entre deux
#     scenarios ; les cartes achetees restent dans le deck jusqu'a la fin.
# S'y ajoutent les cartes confisquees par La Collection, les quatre manigances
# « artefact galactique » rapportees du musee, les compteurs d'esquive du
# vaisseau de Nebula et le porteur de la Pierre du Pouvoir.
EPREUVES += [
    {
        "nom": "gmw — le Chasseur de tetes vaincu au scenario 1 : le carnet le coche, et son premier renfort rejoint le deck rencontre du scenario 2",
        "scenario": "brotherhood_of_badoon",
        "heros": "captain_america",
        "avant": [
            "Puzzle.PutIntoPlay('16183')",
            "Puzzle.MoveTo('16183', 'VictoryDisplay')",
        ],
        "carnet_attendu": {
            "gagnee": True,
            # 1 unite de base, +2 pour la valeur de victoire imprimee du
            # Chasseur, +1 sans sbire en jeu, +1 a l'etape 1B.
            "cles": {"Headhunter Defeated: Brotherhood of Badoon": "1",
                     "Player 1 Unspent Units": "5"},
        },
        "suivant": "infiltrate_the_museum",
        # Le Chasseur revient toujours ; « On the Hunt » (16184) est le
        # palier 1.
        "attendu": {"deck_rencontre": ["16183", "16184"]},
    },
    {
        "nom": "gmw — le Chasseur de tetes epargne : il revient seul au scenario 2, sans renfort",
        "scenario": "brotherhood_of_badoon",
        "heros": "captain_america",
        "carnet_attendu": {"cles_absentes": ["Headhunter Defeated: Brotherhood of Badoon"]},
        "suivant": "infiltrate_the_museum",
        "attendu": {"deck_rencontre": ["16183"], "pas_deck_rencontre": ["16184"]},
    },
    {
        "nom": "gmw — trois marques au carnet : les trois premiers renforts sont la, le quatrieme pas encore",
        "scenario": "brotherhood_of_badoon",
        "heros": "captain_america",
        "carnet": {
            "Headhunter Defeated: Infiltrate the Museum": "1",
            "Headhunter Defeated: Escape the Museum": "1",
        },
        # La troisieme marque vient de la partie jouee ici, qui est un
        # scenario DIFFERENT des deux deja coches.
        "avant": [
            "Puzzle.PutIntoPlay('16183')",
            "Puzzle.MoveTo('16183', 'VictoryDisplay')",
        ],
        "suivant": "nebula",
        "attendu": {"deck_rencontre": ["16184", "16185", "16186"],
                    "pas_deck_rencontre": ["16187"]},
    },
    {
        "nom": "gmw — quatre marques : la recuperation de fugitif entre aussi dans le deck rencontre",
        "scenario": "brotherhood_of_badoon",
        "heros": "captain_america",
        "carnet": {
            "Headhunter Defeated: Infiltrate the Museum": "1",
            "Headhunter Defeated: Escape the Museum": "1",
            "Headhunter Defeated: Nebula": "1",
        },
        "avant": [
            "Puzzle.PutIntoPlay('16183')",
            "Puzzle.MoveTo('16183', 'VictoryDisplay')",
        ],
        "suivant": "ronan",
        "attendu": {"deck_rencontre": ["16184", "16185", "16186", "16187"]},
    },
    {
        "nom": "gmw — les unites S'AJOUTENT a celles du carnet : victoire propre au scenario 1, +3 unites",
        "scenario": "brotherhood_of_badoon",
        "heros": "captain_america",
        "carnet": {"Player 1 Unspent Units": "4"},
        # Livret p.8 : 1 unite, +1 s'il n'y a aucun sbire en jeu, +1 si la
        # manigance principale en est encore a l'etape 1B.
        "carnet_attendu": {"cles": {"Player 1 Unspent Units": "7"}},
    },
    {
        "nom": "gmw — un sbire encore en jeu coute une unite",
        "scenario": "brotherhood_of_badoon",
        "heros": "captain_america",
        "carnet": {"Player 1 Unspent Units": "4"},
        "avant": ["Puzzle.PutIntoPlay('16183')"],
        "carnet_attendu": {"cles": {"Player 1 Unspent Units": "6"}},
    },
    # Signalement n°50 (Phocea, 04/10/2026) : les unites des scenarios 2 et 3
    # n'arrivaient JAMAIS au Marche. Le moteur estampillait son carnet sortant
    # avec le set_name de la manigance principale (« collector_1 », « collector_2 »)
    # et le panneau de recompenses n'utilise le releve du moteur que si
    # l'estampille egale l'id du scenario (`preremplissage.ts`) : sinon il retombe
    # sur le carnet ANCIEN, et les gains du scenario sont perdus en silence.
    {
        "nom": "gmw — l'estampille du carnet sortant est l'id du scenario : brotherhood_of_badoon",
        "scenario": "brotherhood_of_badoon",
        "heros": "captain_america",
        "carnet_attendu": {"scenario": "brotherhood_of_badoon"},
    },
    {
        "nom": "gmw — l'estampille du carnet sortant est l'id du scenario : infiltrate_the_museum",
        "scenario": "infiltrate_the_museum",
        "heros": "captain_america",
        "carnet_attendu": {"scenario": "infiltrate_the_museum"},
    },
    {
        "nom": "gmw — l'estampille du carnet sortant est l'id du scenario : escape_the_museum",
        "scenario": "escape_the_museum",
        "heros": "captain_america",
        "carnet_attendu": {"scenario": "escape_the_museum"},
    },
    {
        "nom": "gmw — l'estampille du carnet sortant est l'id du scenario : nebula",
        "scenario": "nebula",
        "heros": "captain_america",
        "carnet_attendu": {"scenario": "nebula"},
    },
    {
        "nom": "gmw — l'estampille du carnet sortant est l'id du scenario : ronan",
        "scenario": "ronan",
        "heros": "captain_america",
        "carnet_attendu": {"scenario": "ronan"},
    },
    {
        "nom": "gmw — scenario 2 : les unites S'AJOUTENT (1 de base + 1 car la Collection n'a retenu qu'une carte au plus)",
        "scenario": "infiltrate_the_museum",
        "heros": "captain_america",
        "carnet": {"Player 1 Unspent Units": "4"},
        # Livret p.10 : 1 unite, +1 si La Collection compte 1 carte ou moins, +1 si
        # les manigances principales n'ont plus de menace (ici elles en portent : 0).
        "carnet_attendu": {"cles": {"Player 1 Unspent Units": "6"}},
    },
    {
        "nom": "gmw — scenario 3 : les unites S'AJOUTENT (1 de base, aucun artefact rapporte)",
        "scenario": "escape_the_museum",
        "heros": "captain_america",
        "carnet": {"Player 1 Unspent Units": "4"},
        "carnet_attendu": {"cles": {"Player 1 Unspent Units": "5"}},
    },
    {
        "nom": "gmw — une carte achetee au Marche reste dans le deck au scenario suivant",
        "scenario": "brotherhood_of_badoon",
        "heros": "captain_america",
        # Ce que l'ecran du Marche inscrit quand le joueur depense ses unites.
        "choix": {"Player 1 Market Cards": "16150"},
        "suivant": "infiltrate_the_museum",
        "attendu": {"parmi": [["16150", ["deck", "main"]]]},
    },
    {
        "nom": "gmw — les cartes du Marche sont MELANGEES au deck, pas posees sur le dessus (07/10/2026)",
        "scenario": "nebula",
        "heros": "captain_america",
        # Signalement de Phocea, 07/10/2026 : ses 3 cartes du Marche etaient
        # TOUJOURS dans sa main de depart (21 mises en place sur 21, mesure).
        # `ShuffleAllTo` ne melangeait pas quand la carte etait deja creee DANS
        # le deck de destination : rien ne bougeait, donc aucun melange. Sur le
        # deck de 40+ cartes, avoir les trois en main de depart vaut ~1 sur 600 :
        # au moins une doit encore etre dans le deck.
        "choix": {"Player 1 Market Cards": "16162;16163;16176"},
        "suivant": "ronan",
        "attendu": {"un_parmi": [["deck", ["16162", "16163", "16176"]]]},
    },
    {
        "nom": "gmw — une carte confisquee par La Collection est RETIREE du jeu au scenario 3, et la main est refaite",
        "scenario": "infiltrate_the_museum",
        "heros": "captain_america",
        "choix": {"Player 1 Collection Cards": "03017"},
        "suivant": "escape_the_museum",
        # 7 cartes et non 6 : la main de depart de Steve Rogers en compte 6, et
        # le bouclier (03009, mot-cle Setup) est tire avec elle, mesure faite
        # juste apres la mise en place, avant qu'il ne parte sur la table. Le
        # temoin juste en dessous donne la meme valeur sans confiscation.
        "attendu": {"retirees": ["03017"], "pas_deck": ["03017"], "pas_main": ["03017"],
                    "taille": {"main": 7}},
    },
    {
        "nom": "gmw — TEMOIN de la confiscation : sans rien au carnet, la main du scenario 3 est celle de tout le monde",
        "scenario": "infiltrate_the_museum",
        "heros": "captain_america",
        "suivant": "escape_the_museum",
        # Le temoin donne la taille de reference : si la main confisquee plus
        # haut vaut la meme chose, la recharge a bien eu lieu.
        "attendu": {"taille": {"main": 7}},
    },
    {
        "nom": "gmw — deux artefacts emportes du musee : le carnet les nomme et la prime d'une unite tombe",
        "scenario": "escape_the_museum",
        "heros": "captain_america",
        "carnet": {"Player 1 Unspent Units": "0"},
        "avant": [
            "Puzzle.PutIntoPlay('16127')",
            "Puzzle.MoveTo('16127', 'VictoryDisplay')",
            "Puzzle.PutIntoPlay('16130')",
            "Puzzle.MoveTo('16130', 'VictoryDisplay')",
        ],
        # Livret p.12 : « For every 2 Galactic Artifacts side schemes in the
        # victory display, record 1 unit for each player. » Donc 1 + 1 = 2.
        "carnet_attendu": {
            "cles": {
                "Galactic Artifacts in Victory Display": "Hujahdarian Monarch Egg;Crystal Ball",
                "Player 1 Unspent Units": "2",
            },
        },
    },
    {
        "nom": "gmw — la boule de cristal rapportee : elle revient au deck rencontre et Nebula commence robuste",
        "scenario": "escape_the_museum",
        "heros": "captain_america",
        "choix": {"Galactic Artifacts in Victory Display": "Crystal Ball"},
        "suivant": "nebula",
        "attendu": {"deck_rencontre": ["16130"], "statuts": [["16088", "Tough"]]},
    },
    {
        "nom": "gmw — l'oeuf du monarque rapporte : il revient au deck rencontre et pose un compteur d'esquive sur le vaisseau de Nebula",
        "scenario": "escape_the_museum",
        "heros": "captain_america",
        "choix": {"Galactic Artifacts in Victory Display": "Hujahdarian Monarch Egg"},
        "suivant": "nebula",
        "attendu": {"deck_rencontre": ["16127"], "compteurs": [["16093", "evasion", 1]]},
    },
    {
        "nom": "gmw — aucun compteur d'esquive au carnet : la Manoeuvre en Tenaille arrive chargee de 3 menaces de plus",
        "scenario": "nebula",
        "heros": "captain_america",
        "choix": {"Evasion Counters": "0"},
        "suivant": "ronan",
        # Menace imprimee 3 + Hinder 2 (solo) = 5, plus 3 - 0 = 3.
        "attendu": {"menace_min": [["16112", 6]]},
    },
    {
        "nom": "gmw — trois compteurs d'esquive : la Manoeuvre en Tenaille n'a aucun supplement",
        "scenario": "nebula",
        "heros": "captain_america",
        "choix": {"Evasion Counters": "3"},
        "suivant": "ronan",
        "attendu": {"menace_max": [["16112", 5]]},
    },
    {
        "nom": "gmw — le porteur de la Pierre du Pouvoir recoit « Vous etes accuse ! » face cachee au scenario 5",
        "scenario": "nebula",
        "heros": "captain_america",
        "choix": {"Power Stone Control": "Captain America"},
        "suivant": "ronan",
        "attendu": {"rencontres_recues": ["16116"]},
    },
]


# =============================== Sinistres Motivations (sm) — 5 scenarios
#
# Tout tient a la PISTE DE REPUTATION : un compteur unique, cumule de scenario
# en scenario, qui ouvre des recompenses a 1, 5, 9, 13, 17, 21 et 25 noeuds et
# inflige des penalites aux memes paliers (`cards/pack/sm/campaign.py`,
# `FollowSetupInstructionOfReputationTrack`). S'y ajoutent le service a la
# population (une manigance tiree au hasard PARMI CELLES QUI RESTENT), le
# cauchemar de Mysterio et les vilains encore debout a la fin du scenario 4.
# Cette boite n'ecrit pas de carnet sortant : c'est le panneau du plateau qui
# devine les valeurs. Les epreuves mesurent donc ce que le carnet CHANGE.
EPREUVES += [
    {
        "nom": "sm — service a la population : quatre manigances deja accomplies, la cinquieme est celle qui revient",
        "scenario": "sandman",
        "heros": "spider_man",
        "carnet": {"Community Service: Victory for Scenarios #1-4": "27176;27177;27178;27179"},
        "suivant": "venom",
        "attendu": {"deck_rencontre": ["27180"],
                    "pas_deck_rencontre": ["27176", "27177", "27178", "27179"]},
    },
    {
        "nom": "sm — les cinq manigances accomplies : aucune ne revient, et la mise en place ne trebuche pas",
        "scenario": "sandman",
        "heros": "spider_man",
        "carnet": {"Community Service: Victory for Scenarios #1-4": "27176;27177;27178;27179;27180"},
        "suivant": "venom",
        "attendu": {"pas_deck_rencontre": ["27176", "27177", "27178", "27179", "27180"]},
    },
    {
        "nom": "sm — reputation 1 : le materiel S.H.I.E.L.D. choisi entre en jeu au scenario suivant",
        "scenario": "sandman",
        "heros": "spider_man",
        "choix": {"Reputation Track": "1",
                  "Player 1 S.H.I.E.L.D. Tech: Reputation Track Reward": "27182a"},
        "suivant": "venom",
        "attendu": {"en_jeu": ["27182a"]},
    },
    {
        "nom": "sm — reputation 13 : le meme materiel arrive dans sa version AMELIOREE",
        "scenario": "sandman",
        "heros": "spider_man",
        "choix": {"Reputation Track": "13",
                  "Player 1 S.H.I.E.L.D. Tech: Reputation Track Reward": "27182a"},
        "suivant": "venom",
        "attendu": {"en_jeu": ["27182b"], "pas_en_jeu": ["27182a"]},
    },
    {
        "nom": "sm — reputation 9 : les cartes d'aspect choisies sont melangees au deck du joueur",
        "scenario": "sandman",
        "heros": "spider_man",
        "choix": {"Reputation Track": "9",
                  "Player 1 Aspect Advantage: Reputation Track Reward": "01035;01036"},
        "suivant": "venom",
        "attendu": {"parmi": [["01035", ["deck", "main"]], ["01036", ["deck", "main"]]]},
    },
    {
        "nom": "sm — reputation 17 : la carte prevue a l'avance commence EN MAIN",
        "scenario": "sandman",
        "heros": "spider_man",
        "choix": {"Reputation Track": "17",
                  "Player 1 Planning Ahead: Reputation Track Reward": "01007"},
        "suivant": "venom",
        "attendu": {"main": ["01007"]},
    },
    {
        "nom": "sm — reputation 21 : le Helicarrier entre en jeu sous controle du joueur",
        "scenario": "sandman",
        "heros": "spider_man",
        "choix": {"Reputation Track": "21"},
        "suivant": "venom",
        "attendu": {"en_jeu": ["01092"]},
    },
    {
        "nom": "sm — reputation 25 : la tenue symbiotique entre en jeu",
        "scenario": "sandman",
        "heros": "spider_man",
        "choix": {"Reputation Track": "25"},
        "suivant": "venom",
        "attendu": {"en_jeu": ["27191"]},
    },
    {
        "nom": "sm — la technologie Osborn notee au carnet revient dans le deck rencontre",
        "scenario": "sandman",
        "heros": "spider_man",
        "choix": {"Reputation Track": "1",
                  "Osborn Tech: Reputation Track Penalty": "27147;27148"},
        "suivant": "venom",
        "attendu": {"deck_rencontre": ["27147", "27148"]},
    },
    {
        "nom": "sm — reputation 5 : une menace de plus par heros sur la manigance principale",
        "scenario": "sandman",
        "heros": "spider_man",
        "choix": {"Reputation Track": "5"},
        "suivant": "venom",
        # Menace imprimee 2 sur la manigance de Venom, plus 1 par heros.
        "attendu": {"menace_min": [["27076b", 3]]},
    },
    {
        "nom": "sm — TEMOIN de la piste : a 4 noeuds, la manigance principale n'a aucune menace de campagne",
        "scenario": "sandman",
        "heros": "spider_man",
        "choix": {"Reputation Track": "4"},
        "suivant": "venom",
        "attendu": {"menace_max": [["27076b", 2]]},
    },
    {
        "nom": "sm — le cauchemar de Mysterio pose sa menace sur « La lumiere au bout » au scenario 4",
        "scenario": "mysterio",
        "heros": "spider_man",
        "choix": {"Waking Nightmare: Victory for Scenario #3 - Mysterio": "3"},
        "suivant": "sinister_six",
        # Manigance permanente a 10 menaces de depart, plus les 3 du carnet.
        "attendu": {"menace_min": [["27102a", 13]]},
    },
    {
        "nom": "sm — les vilains encore debout au scenario 4 reviennent en renfort au scenario 5",
        "scenario": "sinister_six",
        "heros": "spider_man",
        "choix": {"Last Ones Standing: Victory for Scenario #4 - The Sinister Six": "27094;27095"},
        "suivant": "venom_goblin",
        "attendu": {"deck_rencontre": ["27158", "27159"]},
    },
]


# ================================ Genese des mutants (mut_gen) — 5 scenarios
#
# Trois fils se tirent d'un scenario a l'autre :
#   — le ROLE choisi au scenario 1 (Brawler, Commander, Defender, Peacekeeper)
#     donne une amelioration tiree au hasard dans son set A CHAQUE scenario
#     suivant, mais seulement si la manigance de campagne du scenario
#     precedent a ete accomplie, et jamais deux fois la meme (« Role Upgrades
#     Removed ») ;
#   — les ALLIES CAPTIFS liberes, qui rejoignent le deck d'un joueur au choix
#     (livret p.12, 16 et 19 : « may be shuffled into any player's deck ») ;
#   — le deck FUTUR PASSE, cinq cartes qui migrent entre la reserve, le deck
#     rencontre et la pile de victoire, et ne reviennent jamais une fois
#     vaincues.
# Jubilee, elle, suit ou ne suit pas, selon qu'elle a survecu.
EPREUVES += [
    {
        "nom": "mut_gen — role tenu et manigance accomplie : une amelioration du set choisi entre en jeu au scenario suivant",
        "scenario": "sabretooth",
        "heros": "captain_america",
        "carnet": {"Player 1 Role": "Brawler"},
        "choix": {"Frightened Police Defeated": "1"},
        "suivant": "project_wideawake",
        # Tirage au hasard parmi les cinq ameliorations du role Brawler.
        "attendu": {"un_parmi": [["en_jeu", ["32176", "32177", "32178", "32179", "32180"]]]},
    },
    {
        "nom": "mut_gen — quatre ameliorations de role deja retirees : c'est la cinquieme qui tombe, sans hasard",
        "scenario": "sabretooth",
        "heros": "captain_america",
        "carnet": {"Player 1 Role": "Brawler",
                   "Player 1 Role Upgrades Removed": "32176;32177;32178;32179"},
        "choix": {"Frightened Police Defeated": "1"},
        "suivant": "project_wideawake",
        "attendu": {"en_jeu": ["32180"],
                    "aucune_parmi": [["en_jeu", ["32176", "32177", "32178", "32179"]]]},
    },
    {
        "nom": "mut_gen — manigance de campagne NON accomplie : aucune amelioration de role au scenario suivant",
        "scenario": "sabretooth",
        "heros": "captain_america",
        "carnet": {"Player 1 Role": "Brawler"},
        "suivant": "project_wideawake",
        "attendu": {"aucune_parmi": [["en_jeu", ["32176", "32177", "32178", "32179", "32180"]]]},
    },
    {
        "nom": "mut_gen — la manigance de campagne retournee au scenario 1 est cochee au carnet sortant",
        "scenario": "sabretooth",
        "heros": "captain_america",
        "avant": ["Puzzle.PutIntoPlay('32171b')"],
        "carnet_attendu": {"gagnee": True, "cles": {"Frightened Police Defeated": "1"}},
    },
    {
        "nom": "mut_gen — un allie captif libere rejoint le deck d'un joueur au scenario 3",
        "scenario": "project_wideawake",
        "heros": "captain_america",
        "choix": {"Captive Allies": "32089"},
        "suivant": "master_mold",
        # Le livret laisse choisir le deck ; en solo il n'y en a qu'un.
        "attendu": {"parmi": [["32089", ["deck", "main"]]]},
    },
    {
        "nom": "mut_gen — les allies captifs encore en jeu a la fin du scenario 2 sont releves au carnet",
        "scenario": "project_wideawake",
        "heros": "captain_america",
        "avant": ["Puzzle.PutIntoPlay('32089', under_control=True)"],
        "carnet_attendu": {"cles": {"Captive Allies": "32089"}},
    },
    {
        "nom": "mut_gen — Jubilee ralliee entre en jeu au scenario 3",
        "scenario": "project_wideawake",
        "heros": "captain_america",
        "choix": {"Campaign Pool: Jubilee": "1"},
        "suivant": "master_mold",
        "attendu": {"en_jeu": ["32088b"]},
    },
    {
        "nom": "mut_gen — Jubilee perdue : elle ne revient plus, meme notee a la reserve",
        "scenario": "project_wideawake",
        "heros": "captain_america",
        "choix": {"Campaign Pool: Jubilee": "1", "Jubilee removed": "1"},
        "suivant": "master_mold",
        "attendu": {"pas_en_jeu": ["32088b"]},
    },
    {
        "nom": "mut_gen — Jubilee en jeu a la fin du scenario : le carnet la garde a la reserve",
        "scenario": "master_mold",
        "heros": "captain_america",
        "carnet": {"Campaign Pool: Jubilee": "1"},
        "avant": ["Puzzle.PutIntoPlay('32088b', under_control=True)"],
        "carnet_attendu": {"cles": {"Campaign Pool: Jubilee": "1"},
                           "cles_absentes": ["Jubilee removed"]},
    },
    {
        "nom": "mut_gen — Jubilee disparue en cours de partie : le carnet la retire de la campagne",
        "scenario": "master_mold",
        "heros": "captain_america",
        "carnet": {"Campaign Pool: Jubilee": "1"},
        # Elle entre en jeu a la mise en place puisqu'elle est a la reserve ;
        # c'est sa disparition PENDANT la partie qui doit etre vue.
        "avant": ["Puzzle.Remove('32088b')"],
        "carnet_attendu": {"cles": {"Jubilee removed": "1"},
                           "cles_absentes": ["Campaign Pool: Jubilee"]},
    },
    {
        "nom": "mut_gen — une carte du Futur Passe laissee dans le deck rencontre y revient au scenario suivant",
        "scenario": "sabretooth",
        "heros": "captain_america",
        "carnet": {"Future Past in Encounter Deck": "32166"},
        "suivant": "project_wideawake",
        "attendu": {"deck_rencontre": ["32166"]},
    },
    {
        "nom": "mut_gen — une carte du Futur Passe vaincue ne revient JAMAIS",
        "scenario": "sabretooth",
        "heros": "captain_america",
        "carnet": {"Future Past in Victory Display": "32166"},
        "suivant": "project_wideawake",
        "attendu": {"pas_deck_rencontre": ["32166"], "pas_de_cote": ["32166"],
                    "pas_en_jeu": ["32166"]},
    },
    {
        "nom": "mut_gen — une carte du Futur Passe mise en pile de victoire est inscrite au carnet sortant",
        "scenario": "sabretooth",
        "heros": "captain_america",
        "avant": [
            "Puzzle.PutIntoPlay('32166')",
            "Puzzle.MoveTo('32166', 'VictoryDisplay')",
        ],
        "carnet_attendu": {"cles": {"Future Past in Victory Display": "32166"}},
    },
]


# ================================== NeXt Evolution (next_evol) — 5 scenarios
#
# La boite ou la PREPARATION se joue avant la partie : a chaque mise en place,
# le premier joueur pose une manigance annexe de campagne (« Assemble the
# Team », « Gear Up »...). Accomplie, elle se retourne en ENVIRONNEMENT qui
# reste acquis pour toute la campagne ; laissee en jeu, elle est retiree de la
# campagne. Et ces environnements se paient : Juggernaut gagne un pion d'elan
# par environnement, « Teleported Away » et « l'Etreinte de Stryfe » arrivent
# chargees d'autant de menaces.
# S'y ajoutent les Maraudeurs vaincus au scenario 1 (qui ne reviennent pas),
# les Morlocks sauves (autant de cartes cherchees au deck) et l'etat de sante
# de Hope Summers, reporte de partie en partie.
EPREUVES += [
    {
        "nom": "next_evol — un environnement acquis revient en jeu a chaque scenario suivant",
        "scenario": "morlock_siege",
        "heros": "captain_america",
        "choix": {"Campaign Pool: Team Assembled": "1"},
        "suivant": "on_the_run",
        "attendu": {"en_jeu": ["40190b"]},
    },
    {
        "nom": "next_evol — une manigance deja choisie n'est plus proposee, mais sa carte rencontre reste dans le deck",
        "scenario": "morlock_siege",
        "heros": "captain_america",
        "suivant": "on_the_run",
        # La partie 1 a pose « Assemble the Team » (40190a) et melange sa carte
        # rencontre (40199 Malice). A la partie 2, le choix porte donc sur la
        # suivante, « Establish Safehouse » (40191a, carte 40201 Vanisher), et
        # Malice est remelangee par-dessus.
        "attendu": {"en_jeu": ["40191a"], "pas_en_jeu": ["40190a"],
                    "deck_rencontre": ["40199", "40201"]},
    },
    {
        "nom": "next_evol — une manigance de campagne retiree n'est plus jamais proposee",
        "scenario": "morlock_siege",
        "heros": "captain_america",
        "choix": {"Removed: Assemble the Team": "1"},
        "suivant": "on_the_run",
        "attendu": {"en_jeu": ["40191a"], "pas_en_jeu": ["40190a"]},
    },
    {
        "nom": "next_evol — un Maraudeur vaincu au scenario 1 est retire du jeu au scenario 2",
        "scenario": "morlock_siege",
        "heros": "captain_america",
        "choix": {"Marauders Defeated": "40070a"},
        "suivant": "on_the_run",
        "attendu": {"retirees": ["40070a"]},
    },
    {
        "nom": "next_evol — deux Morlocks sauves : deux cartes sont cherchees au deck et la main de depart tient debout",
        "scenario": "morlock_siege",
        "heros": "captain_america",
        "choix": {"Morlocks Saved": "2"},
        "suivant": "on_the_run",
        # Livret p.11 : « choose a player to search their deck for one card,
        # add that card to their hand, and shuffle their deck. » La recompense
        # n'AJOUTE pas de cartes a la main : la mise en place de campagne est
        # l'etape 13 et la pioche l'etape 14 (annexe II du guide de
        # reference), donc on CHOISIT une partie de sa main de depart au lieu
        # de la subir. La main garde sa taille ordinaire.
        "attendu": {"taille_min": {"main": 6}, "taille_max": {"main": 7}},
    },
    {
        "nom": "next_evol — TEMOIN des Morlocks : sans aucun sauve, la main du scenario 2 est la main ordinaire",
        "scenario": "morlock_siege",
        "heros": "captain_america",
        "suivant": "on_the_run",
        "attendu": {"taille": {"main": 7}},
    },
    {
        "nom": "next_evol — les Morlocks encore en jeu a la victoire sont comptes au carnet",
        "scenario": "morlock_siege",
        "heros": "captain_america",
        # Deux EXEMPLAIRES distincts : `Puzzle.PutIntoPlay('40079')` appele
        # deux fois retrouverait la meme carte et n'en poserait qu'une.
        "avant": [
            "Puzzle.PutIntoPlay(Puzzle.CreateCard('40079'), under_control=True)",
            "Puzzle.PutIntoPlay(Puzzle.CreateCard('40079'), under_control=True)",
        ],
        "carnet_attendu": {"gagnee": True, "cles": {"Morlocks Saved": "2"}},
    },
    {
        "nom": "next_evol — l'environnement acquis a la fin de la partie est inscrit au carnet, la manigance laissee en jeu est retiree de la campagne",
        "scenario": "morlock_siege",
        "heros": "captain_america",
        "avant": [
            "Puzzle.PutIntoPlay('40190b')",
            "Puzzle.PutIntoPlay('40191a')",
        ],
        "carnet_attendu": {"cles": {"Campaign Pool: Team Assembled": "1",
                                    "Removed: Establish Safehouse": "1"}},
    },
    {
        "nom": "next_evol — Juggernaut gagne un pion d'elan par environnement acquis",
        "scenario": "on_the_run",
        "heros": "captain_america",
        "choix": {"Campaign Pool: Team Assembled": "1",
                  "Campaign Pool: Geared Up": "1"},
        "suivant": "juggernaut",
        "attendu": {"compteurs": [["40118", "momentum", 3]]},
    },
    {
        "nom": "next_evol — TEMOIN de Juggernaut : sans environnement acquis, il n'a que son elan de depart",
        "scenario": "on_the_run",
        "heros": "captain_america",
        "suivant": "juggernaut",
        "attendu": {"compteurs": [["40118", "momentum", 1]]},
    },
    {
        "nom": "next_evol — quatre environnements : « Teleporte » arrive lourdement chargee au scenario 4",
        "scenario": "juggernaut",
        "heros": "captain_america",
        "choix": {"Campaign Pool: Team Assembled": "1", "Campaign Pool: Geared Up": "1",
                  "Campaign Pool: Safehouse Established": "1", "Campaign Pool: Mission Prepped": "1"},
        "suivant": "mister_sinister",
        "attendu": {"menace_min": [["40146", 8]]},
    },
    {
        "nom": "next_evol — TEMOIN : sans environnement, « Teleporte » n'a que sa menace imprimee",
        "scenario": "juggernaut",
        "heros": "captain_america",
        "suivant": "mister_sinister",
        "attendu": {"menace_max": [["40146", 4]]},
    },
    {
        "nom": "next_evol — quatre environnements : « l'Etreinte de Stryfe » arrive chargee au scenario 5",
        "scenario": "mister_sinister",
        "heros": "captain_america",
        "choix": {"Campaign Pool: Team Assembled": "1", "Campaign Pool: Geared Up": "1",
                  "Campaign Pool: Safehouse Established": "1", "Campaign Pool: Mission Prepped": "1"},
        "suivant": "stryfe",
        "attendu": {"menace_min": [["40168a", 14]]},
    },
    {
        "nom": "next_evol — TEMOIN : sans environnement, « l'Etreinte de Stryfe » n'a que sa menace imprimee",
        "scenario": "mister_sinister",
        "heros": "captain_america",
        "suivant": "stryfe",
        "attendu": {"menace_max": [["40168a", 10]]},
    },
    {
        "nom": "next_evol — les blessures de Hope Summers suivent au scenario suivant",
        "scenario": "juggernaut",
        "heros": "captain_america",
        "choix": {"Hope Summers's Damage Scenario 3": "2"},
        "suivant": "mister_sinister",
        # Le livret laisse le choix entre blesser Hope et charger la manigance ;
        # la premiere option proposee porte sur Hope.
        "attendu": {"degats": [["40130", 2]]},
    },
    {
        "nom": "next_evol — les degats de Hope Summers sont releves au carnet sortant",
        "scenario": "juggernaut",
        "heros": "captain_america",
        "avant": ["Puzzle.Damage('40130', 2)"],
        "carnet_attendu": {"cles": {"Hope Summers's Damage Scenario 3": "2"}},
    },
]


# =================================== L'Ere d'Apocalypse (aoa) — 5 scenarios
#
# Chaque partie se double d'une MISSION tiree parmi celles qui restent a faire,
# gardee par un SURVEILLANT tire parmi ceux qui sont encore debout. Reussir ou
# rater la mission ne change pas la partie en cours : cela change la SUIVANTE,
# en versant (ou non) une nuisance a la reserve de campagne — mesures
# desesperees, refugies paniques, mur de mer nord-americain. Les allies
# rencontres en mission, eux, rejoignent le deck pour le reste de la campagne.
EPREUVES += [
    {
        "nom": "aoa — trois missions deja faites : c'est la quatrieme qui est posee, sans hasard",
        "scenario": "unus",
        "heros": "captain_america",
        # Par `choix` et non par `carnet` : la partie 1 fait elle aussi une
        # mission et la raye a son tour. Ce que le joueur a sous les yeux au
        # panneau, c'est le carnet APRES la partie, et c'est lui qui decide.
        "choix": {"Mission Done: Liberate the Seattle Core": "1",
                  "Mission Done: Evacuate Survivors": "1",
                  "Mission Done: Sabotage the Sea Wall": "1",
                  "Mission Done: Find Lost Mutants": None},
        "suivant": "four_horsemen",
        "attendu": {"en_jeu": ["45169a", "45171a"]},
    },
    {
        "nom": "aoa — quatre surveillants vaincus : c'est le cinquieme qui garde la mission",
        "scenario": "unus",
        "heros": "captain_america",
        "carnet": {"Overseer Defeated: Mister Sinister": "1",
                   "Overseer Defeated: The Shadow King": "1",
                   "Overseer Defeated: Abyss": "1",
                   "Overseer Defeated: Sugar Man": "1"},
        "suivant": "four_horsemen",
        "attendu": {"en_jeu": ["45183a"]},
    },
    {
        "nom": "aoa — la mission « Evacuate Survivors » glisse une obligation dans le deck de chaque joueur",
        "scenario": "unus",
        "heros": "captain_america",
        "choix": {"Mission Done: Liberate the Seattle Core": "1",
                  "Mission Done: Sabotage the Sea Wall": "1",
                  "Mission Done: Find Lost Mutants": "1",
                  "Mission Done: Evacuate Survivors": None},
        "suivant": "four_horsemen",
        "attendu": {"en_jeu": ["45167a"], "parmi": [["45178", ["deck", "main"]]]},
    },
    {
        "nom": "aoa — la mission « Sabotage the Sea Wall » glisse le mur dans le deck rencontre",
        "scenario": "unus",
        "heros": "captain_america",
        "choix": {"Mission Done: Liberate the Seattle Core": "1",
                  "Mission Done: Evacuate Survivors": "1",
                  "Mission Done: Find Lost Mutants": "1",
                  "Mission Done: Sabotage the Sea Wall": None},
        "suivant": "four_horsemen",
        "attendu": {"en_jeu": ["45168a"], "deck_rencontre": ["45177"]},
    },
    {
        "nom": "aoa — les mesures desesperees de la reserve reviennent dans le deck du joueur",
        "scenario": "unus",
        "heros": "captain_america",
        "choix": {"Campaign Pool: Desperate Measures": "1"},
        "suivant": "four_horsemen",
        "attendu": {"parmi": [["45176", ["deck", "main"]]]},
    },
    {
        "nom": "aoa — les refugies paniques de la reserve reviennent dans le deck du joueur",
        "scenario": "unus",
        "heros": "captain_america",
        "choix": {"Campaign Pool: Panicked Refugees": "1"},
        "suivant": "four_horsemen",
        "attendu": {"parmi": [["45178", ["deck", "main"]]]},
    },
    {
        "nom": "aoa — le mur de mer de la reserve revient dans le deck rencontre",
        "scenario": "unus",
        "heros": "captain_america",
        "choix": {"Campaign Pool: North American Sea Wall": "1"},
        "suivant": "four_horsemen",
        "attendu": {"deck_rencontre": ["45177"]},
    },
    {
        "nom": "aoa — l'allie de campagne recrute en mission revient dans le deck a chaque scenario",
        "scenario": "unus",
        "heros": "captain_america",
        "choix": {"Player 1 Campaign Ally": "32089"},
        "suivant": "four_horsemen",
        "attendu": {"parmi": [["32089", ["deck", "main"]]]},
    },
    {
        "nom": "aoa — mission accomplie : elle est rayee de la liste et sa recompense entre a la reserve",
        "scenario": "unus",
        "heros": "captain_america",
        "carnet": {"Mission Done: Evacuate Survivors": "1",
                   "Mission Done: Sabotage the Sea Wall": "1",
                   "Mission Done: Find Lost Mutants": "1",
                   "Mission Result": "accomplished"},
        "carnet_attendu": {
            "gagnee": True,
            "cles": {"Mission Done: Liberate the Seattle Core": "1",
                     "Campaign Pool: Desperate Measures": "1"},
        },
    },
    {
        "nom": "aoa — mission RATEE : les refugies paniques entrent a la reserve, la mission est quand meme rayee",
        "scenario": "unus",
        "heros": "captain_america",
        "carnet": {"Mission Done: Liberate the Seattle Core": "1",
                   "Mission Done: Sabotage the Sea Wall": "1",
                   "Mission Done: Find Lost Mutants": "1",
                   "Mission Result": "failed"},
        "carnet_attendu": {
            "cles": {"Mission Done: Evacuate Survivors": "1",
                     "Campaign Pool: Panicked Refugees": "1"},
        },
    },
    {
        "nom": "aoa — un surveillant mis en pile de victoire est raye de la campagne",
        "scenario": "unus",
        "heros": "captain_america",
        "avant": [
            "Puzzle.PutIntoPlay('45179a')",
            "Puzzle.MoveTo('45179a', 'VictoryDisplay')",
        ],
        "carnet_attendu": {"cles": {"Overseer Defeated: Mister Sinister": "1"}},
    },
]


# ============================ Les Agents du S.H.I.E.L.D. (aos) — 5 scenarios
#
# La boite-enquete. Trois membres du CONSEIL EXECUTIF restent sur la table d'un
# scenario a l'autre avec leurs compteurs secret ; vider un membre rapporte une
# PREUVE, et les preuves accumulees eliminent des combinaisons jusqu'a designer
# la taupe. Le reste du carnet est une longue liste de dettes : ce qu'on a
# laisse debout au scenario 1 charge le niveau d'alerte du 2, les captifs
# liberes au 2 ouvrent les serrures du 3, les Adaptoides laisses en jeu au 3 et
# les Thunderbolts encore debout au 4 reviennent tous au scenario final.
EPREUVES += [
    {
        "nom": "aos — les compteurs secret du Conseil se reportent au scenario suivant",
        "scenario": "black_widow",
        "heros": "captain_america",
        "choix": {"Secret Counters: Chief Medical Officer": "3",
                  "Secret Counters: Chief Surveillance Officer": "1",
                  "Secret Counters: Chief Tactical Officer": "0"},
        "suivant": "batroc",
        "attendu": {"compteurs": [["50181a", "secret", 3],
                                  ["50182a", "secret", 1],
                                  ["50183a", "secret", 0]]},
    },
    {
        "nom": "aos — TEMOIN du Conseil : au premier scenario, chaque membre commence avec deux secrets",
        "scenario": "black_widow",
        "heros": "captain_america",
        "suivant": "black_widow",
        "attendu": {"compteurs": [["50181a", "secret", 2],
                                  ["50182a", "secret", 2],
                                  ["50183a", "secret", 2]]},
    },
    {
        "nom": "aos — un Conseil entierement retourne des la mise en place fait perdre la partie",
        "scenario": "black_widow",
        "heros": "captain_america",
        "choix": {"Secret Counters: Chief Medical Officer": "4",
                  "Secret Counters: Chief Surveillance Officer": "4",
                  "Secret Counters: Chief Tactical Officer": "4"},
        "suivant": "batroc",
        "attendu": {"en_jeu": ["50181b", "50182b", "50183b"], "perdue": True},
    },
    {
        "nom": "aos — ce qu'on a laisse debout au scenario 1 charge le niveau d'alerte du scenario 2",
        "scenario": "black_widow",
        "heros": "captain_america",
        "choix": {"Minions and Side Schemes": "3"},
        "suivant": "batroc",
        # Des JETONS de menace, pas des compteurs : c'est ainsi que la carte
        # elle-meme les pose et les retire (aos/batroc/50090a.py).
        "attendu": {"jetons": [["50090a", "threat", 3]]},
    },
    {
        "nom": "aos — TEMOIN du niveau d'alerte : sans rien au carnet, il commence vide",
        "scenario": "black_widow",
        "heros": "captain_america",
        "choix": {"Minions and Side Schemes": "0"},
        "suivant": "batroc",
        "attendu": {"jetons": [["50090a", "threat", 0]]},
    },
    {
        "nom": "aos — chaque captif libere au scenario 2 ouvre une serrure de la cellule au scenario 3",
        "scenario": "batroc",
        "heros": "captain_america",
        "choix": {"Rescued Captives": "2"},
        "suivant": "modok",
        # La carte en jeu porte deja 2 serrures posees par son propre texte ;
        # la campagne en ajoute 3, puis en retire une par captif libere.
        "attendu": {"compteurs_total": [["lock", 3]]},
    },
    {
        "nom": "aos — TEMOIN de la cellule : sans captif libere, les trois serrures sont posees",
        "scenario": "batroc",
        "heros": "captain_america",
        "choix": {"Rescued Captives": "0"},
        "suivant": "modok",
        "attendu": {"compteurs_total": [["lock", 5]]},
    },
    {
        "nom": "aos — les Adaptoides laisses en jeu au scenario 3 reviennent au scenario final",
        "scenario": "modok",
        "heros": "captain_america",
        "choix": {"Adaptoid Environments": "50109;50110"},
        "suivant": "baron_zemo",
        "attendu": {"en_jeu": ["50109", "50110"], "deck_rencontre": ["50113"]},
    },
    {
        "nom": "aos — un Thunderbolt encore debout au scenario 4 revient AVEC son set au scenario final",
        "scenario": "thunderbolts",
        "heros": "captain_america",
        "choix": {"Surviving Thunderbolts": "Moonstone"},
        "suivant": "baron_zemo",
        "attendu": {"deck_rencontre": ["50139"]},
    },
    {
        "nom": "aos — Jolt survivante revient SEULE, sans set (« except for Jolt's »)",
        "scenario": "thunderbolts",
        "heros": "captain_america",
        "choix": {"Surviving Thunderbolts": "Jolt"},
        "suivant": "baron_zemo",
        "attendu": {"deck_rencontre": ["50133"]},
    },
    {
        "nom": "aos — une preuve gagnee entre en jeu au scenario suivant et y resout sa mise en place",
        "scenario": "black_widow",
        "heros": "captain_america",
        "choix": {"Evidence Gained": "50185"},
        "suivant": "batroc",
        "attendu": {"en_jeu": ["50185"]},
    },
    {
        "nom": "aos — les sbires et manigances annexes encore en jeu a la victoire sont comptes au carnet",
        "scenario": "black_widow",
        "heros": "captain_america",
        "avant": ["Puzzle.PutIntoPlay('50113')"],
        # Le scenario laisse deja une manigance annexe sur la table : le sbire
        # ajoute ici fait donc 2. Le temoin juste en dessous donne le 1 de
        # reference.
        "carnet_attendu": {"gagnee": True, "cles": {"Minions and Side Schemes": "2"}},
    },
    {
        "nom": "aos — TEMOIN du comptage : sans sbire ajoute, le scenario 1 n'en compte qu'un",
        "scenario": "black_widow",
        "heros": "captain_america",
        "carnet_attendu": {"cles": {"Minions and Side Schemes": "1"}},
    },
    {
        "nom": "aos — les captifs liberes encore en jeu au scenario 2 sont comptes au carnet",
        "scenario": "batroc",
        "heros": "captain_america",
        "avant": ["Puzzle.PutIntoPlay('50091', under_control=True)"],
        "carnet_attendu": {"cles": {"Rescued Captives": "1"}},
    },
    {
        "nom": "aos — les Adaptoides encore en jeu au scenario 3 sont releves au carnet",
        "scenario": "modok",
        "heros": "captain_america",
        "avant": ["Puzzle.PutIntoPlay('50109')"],
        "carnet_attendu": {"cles": {"Adaptoid Environments": "50109"}},
    },
    {
        "nom": "aos — les Thunderbolts encore en jeu au scenario 4 sont nommes au carnet",
        "scenario": "thunderbolts",
        "heros": "captain_america",
        "avant": ["Puzzle.PutIntoPlay('50139')"],
        # Le scenario 4 met deja deux Thunderbolts sur la table ; Moonstone
        # s'ajoute a la liste, triee par nom.
        "carnet_attendu": {"cles": {"Surviving Thunderbolts": "Black Widow;MACH-IV;Moonstone"}},
    },
    {
        "nom": "aos — TEMOIN des Thunderbolts : ceux que le scenario pose sont deja comptes",
        "scenario": "thunderbolts",
        "heros": "captain_america",
        "carnet_attendu": {"cles": {"Surviving Thunderbolts": "Black Widow;MACH-IV"}},
    },
    {
        "nom": "aos — un membre du Conseil vide rapporte une preuve et compte un scenario de plus",
        "scenario": "black_widow",
        "heros": "captain_america",
        # L'enveloppe A.I.M. est tiree par le serveur ; sans elle le moteur
        # refuse de donner une preuve, faute de savoir laquelle est a la taupe.
        "carnet": {"A.I.M. Envelope": "50185;50188;50191"},
        # `Counter(..., 0)` ne ferait rien : c'est un RETRAIT de deux secrets
        # qu'il faut pour vider le membre.
        "avant": ["Puzzle.Counter('50181a', 'secret', -2)"],
        "carnet_attendu": {
            "cles": {"Scenarios With A Cleared Board Member": "1"},
            "cles_presentes": ["Evidence Gained"],
        },
    },
    {
        "nom": "aos — aucun membre vide : aucune preuve, et le compte ne bouge pas",
        "scenario": "black_widow",
        "heros": "captain_america",
        "carnet": {"A.I.M. Envelope": "50185;50188;50191"},
        "carnet_attendu": {
            "cles_absentes": ["Evidence Gained", "Scenarios With A Cleared Board Member"],
        },
    },
]


# ============================ La Toile du Mensonge (web_of_deceit) — maison
#
# Campagne maison, une seule mecanique de report : les ARBRES DE TALENTS. A
# chaque rencontre gagnee, chaque joueur prend une carte du palier suivant de
# son arbre ; ces cartes restent dans son deck jusqu'a la fin de la campagne et
# doivent y figurer (livret maison p.2). Le carnet retient un choix par palier
# et par joueur, et la mise en place les remet toutes dans le deck.
EPREUVES += [
    {
        "nom": "web_of_deceit — le talent de palier 0 choisi est dans le deck des la rencontre suivante",
        "scenario": "wd_shocker",
        "heros": "spider_man",
        "choix": {"Player 1 Talent Tier 0": "wd112"},
        "suivant": "wd_electro",
        "attendu": {"parmi": [["wd112", ["deck", "main"]]]},
    },
    {
        "nom": "web_of_deceit — les paliers S'ACCUMULENT : trois talents gagnes, trois cartes dans le deck",
        "scenario": "wd_the_lizard",
        "heros": "spider_man",
        "choix": {"Player 1 Talent Tier 0": "wd112",
                  "Player 1 Talent Tier 1": "wd113",
                  "Player 1 Talent Tier 2": "wd115"},
        "suivant": "wd_vulture",
        "attendu": {"parmi": [["wd112", ["deck", "main"]],
                              ["wd113", ["deck", "main"]],
                              ["wd115", ["deck", "main"]]]},
    },
    {
        "nom": "web_of_deceit — TEMOIN : sans talent au carnet, aucune carte de campagne ne s'invite dans le deck",
        "scenario": "wd_shocker",
        "heros": "spider_man",
        "suivant": "wd_electro",
        "attendu": {"aucune_parmi": [["deck", ["wd112", "wd113", "wd115"]],
                                     ["main", ["wd112", "wd113", "wd115"]]]},
    },
    {
        "nom": "web_of_deceit — les talents suivent jusqu'a la derniere rencontre",
        "scenario": "wd_vulture",
        "heros": "spider_man",
        "choix": {"Player 1 Talent Tier 0": "wd112",
                  "Player 1 Talent Tier 4": "wd121"},
        "suivant": "wd_kingpin",
        "attendu": {"parmi": [["wd112", ["deck", "main"]], ["wd121", ["deck", "main"]]]},
    },
]


# ================================================ Hunting Season (hunting_season)
#
# Carnet (cards/pack/hunting_season/campaign.py) : « Player N Experience »
# (solde), « Player N Cards added to deck », « Player N Hero-specific cards
# removed / to remove », drapeaux « Vermin escaped », « Scorpion joined you »,
# « Lizard escaped », « Vulture joined you », « Gibbon unlocked », et les
# reglages « Hunter Mode » / « Master Hunter » ecrits par l'ecran. Une defaite
# aux scenarios 1 a 4 fait CONTINUER la campagne (decision du 09/10/2026).
EPREUVES += [
    {
        "nom": "hunting_season — victoire contre Vermin au stade 1 : 4 XP, l'allie Vermin va au Master Hunter et revient au deck au scenario 2",
        "scenario": "hs_vermin",
        "heros": "spider_man",
        "carnet_attendu": {
            "gagnee": True,
            "scenario": "hs_vermin",
            # 3 (victoire) + 1 (complot au stade Rats and More Rats) ; un rat
            # regulier est engage avec le joueur : pas de point « sans rat ».
            "cles": {"Player 1 Experience": "4", "Player 1 Cards added to deck": "hs200"},
            "cles_absentes": ["Vermin escaped"],
            "cles_presentes": ["Player 1 Remaining hit points", "Player 1 Identity"],
        },
        "suivant": "hs_scorpion",
        "attendu": {"parmi": [["hs200", ["deck", "main"]]]},
    },
    {
        "nom": "hunting_season — DEFAITE contre Vermin : 2 XP, Vermin s'echappe, aucun allie gagne",
        "scenario": "hs_vermin",
        "heros": "spider_man",
        "fin": "Lose",
        "carnet_attendu": {
            "gagnee": False,
            "scenario": "hs_vermin",
            "cles": {"Player 1 Experience": "2", "Vermin escaped": "1"},
            "cles_absentes": ["Player 1 Cards added to deck"],
        },
    },
    {
        "nom": "hunting_season — DEFAITE contre Scorpion : la penalite « 1 carte de heros » est notee puis appliquee a la mise en place suivante",
        "scenario": "hs_scorpion",
        "heros": "spider_man",
        "fin": "Lose",
        "carnet_attendu": {"gagnee": False, "cles": {"Player 1 Hero-specific cards to remove": "1"}},
        "suivant": "hs_the_lizard",
        "attendu": {"un_parmi": [["retirees", ["01002", "01003", "01004", "01005", "01006", "01007", "01008", "01009", "01010"]]]},
    },
    {
        "nom": "hunting_season — victoire contre Vulture : Vulture rejoint, Gibbon est debloque, l'allie Vulture est au deck",
        "scenario": "hs_vulture",
        "heros": "spider_man",
        "carnet_attendu": {
            "gagnee": True,
            "scenario": "hs_vulture",
            "cles": {"Vulture joined you": "1", "Gibbon unlocked": "1", "Player 1 Cards added to deck": "hs203"},
        },
    },
    {
        "nom": "hunting_season — Kraven : les deux fuyards rejoignent le deck rencontre, les deux ralliés en sortent",
        "scenario": "hs_vulture",
        "heros": "spider_man",
        "carnet": {"Vermin escaped": "1", "Scorpion joined you": "1", "Lizard escaped": "1"},
        "carnet_attendu": {"gagnee": True, "cles": {"Vulture joined you": "1"}},
        "suivant": "hs_kraven_the_hunter",
        "attendu": {"deck_rencontre": ["hs204", "hs205"], "pas_deck_rencontre": ["hs160", "hs158"]},
    },
    {
        "nom": "hunting_season — temoin Kraven : sans drapeau, ni fuyard ajoute ni rallie retire",
        "scenario": "hs_vulture",
        "heros": "spider_man",
        "fin": "Lose",
        "carnet_attendu": {"gagnee": False, "cles_absentes": ["Vulture joined you"]},
        "suivant": "hs_kraven_the_hunter",
        "attendu": {"deck_rencontre": ["hs160", "hs158"], "pas_deck_rencontre": ["hs204", "hs205"]},
    },
    {
        "nom": "hunting_season — les cartes du Lodge achetees (carnet) sont remises au deck a chaque scenario",
        "scenario": "hs_vermin",
        "heros": "spider_man",
        "carnet_attendu": {"gagnee": True},
        # Ce que l'ecran du Lodge inscrit apres l'achat.
        "choix": {"Player 1 Cards added to deck": "hs200;hs185;hs191"},
        "suivant": "hs_scorpion",
        "attendu": {"parmi": [["hs185", ["deck", "main"]], ["hs191", ["deck", "main"]], ["hs200", ["deck", "main"]]]},
    },
    {
        "nom": "hunting_season — mode Hunter en campagne experte : l'environnement du scenario entre en jeu",
        "scenario": "hs_vermin_expert",
        "heros": "spider_man",
        "carnet": {"Hunter Mode": "1"},
        "carnet_attendu": {"gagnee": True},
        "suivant": "hs_scorpion_expert",
        "attendu": {"en_jeu": ["hs223"]},
    },
    {
        "nom": "hunting_season — temoin : mode Hunter coche en campagne STANDARD, aucun environnement",
        "scenario": "hs_vermin",
        "heros": "spider_man",
        "carnet": {"Hunter Mode": "1"},
        "carnet_attendu": {"gagnee": True},
        "suivant": "hs_scorpion",
        "attendu": {"pas_en_jeu": ["hs223"]},
    },
    {
        "nom": "hunting_season — campagne experte : les PV restants (plafonnes) sont notes ; blesse et sans XP, le heros prend une carte de son set expert pour revenir au maximum",
        "scenario": "hs_vermin_expert",
        "heros": "spider_man",
        "avant": ["Puzzle.Damage('01001b', 4)"],
        "carnet_attendu": {"gagnee": True, "cles": {"Player 1 Remaining hit points": "6"}},
        "choix": {"Player 1 Experience": "0"},
        "suivant": "hs_scorpion_expert",
        # Graine 42 : le tirage donne hs209 Poisoned!, pioche a la main de depart,
        # revelee aussitot (« Take 2 damage », faute d'energie) apres le soin complet.
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "hunting_season — temoin : PV notes au maximum et sans XP, aucune carte du set expert, aucun degat",
        "scenario": "hs_vermin_expert",
        "heros": "spider_man",
        "carnet_attendu": {"gagnee": True, "cles": {"Player 1 Remaining hit points": "10"}},
        "choix": {"Player 1 Experience": "0"},
        "suivant": "hs_scorpion_expert",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "hunting_season — campagne experte : un heros vaincu (0 PV) doit prendre une carte de son set expert, meme avec de l'XP",
        "scenario": "hs_vermin_expert",
        "heros": "spider_man",
        "carnet_attendu": {"gagnee": True},
        "choix": {"Player 1 Remaining hit points": "0", "Player 1 Experience": "0"},
        "suivant": "hs_scorpion_expert",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "hunting_season — 2 XP depenses a la mise en place : une carte de plus a la main de depart",
        "scenario": "hs_vermin",
        "heros": "spider_man",
        "carnet_attendu": {"gagnee": True},
        "choix": {"Player 1 Experience": "2", "Player 1 Cards added to deck": None},
        "suivant": "hs_scorpion",
        "attendu": {"taille_main": 7},
    },
    {
        "nom": "hunting_season — temoin : 1 XP ne suffit pas, main de depart normale",
        "scenario": "hs_vermin",
        "heros": "spider_man",
        "carnet_attendu": {"gagnee": True},
        "choix": {"Player 1 Experience": "1", "Player 1 Cards added to deck": None},
        "suivant": "hs_scorpion",
        "attendu": {"taille_main": 6},
    },
]


# ============================================================ Galactic Storm (galactic_storm)
#
# Carnet : « Recruited Allies » / « Campaign Pool: <nom> » (listes/drapeaux cumulatifs), « Imperial
# Guard Removed » (liste, informationnel — voir le mot en tete de cards/pack/galactic_storm/
# campaign.py), « Time Pressure » (entier, ne baisse jamais), « Odd Guesses Correct » (entier,
# saisi par le joueur), « Campaign Completed ». Le moteur ecrit tout (campaign.py), le panneau
# n'a rien a detecter seul (victoire majoritairement "auto" sans "detection").
EPREUVES += [
    {
        "nom": "galactic_storm — victoire Kree Sentry, Gladiator vaincu : Rick Jones ET Gladiator rejoignent la reserve, l'Imperial Guard utilisee est notee",
        "scenario": "gs_kree_sentry",
        "heros": "spider_man",
        "avant": [
            "Puzzle.PutIntoPlay('gs098')", "Puzzle.Damage('gs098', 8)",
            "Puzzle.PutIntoPlay('gs094')",
        ],
        "carnet_attendu": {
            "gagnee": True,
            "cles": {
                "Recruited Allies": "Rick Jones;Gladiator",
                "Campaign Pool: Rick Jones": "1",
                "Campaign Pool: Gladiator": "1",
                "Imperial Guard Removed": "gs092;gs094;gs098",
            },
        },
    },
    {
        # gs092 (un des 3 environnements Loyal Devotion/Disciplined Training/Noble Bearing) entre
        # TOUJOURS en jeu de base des que le modulaire Imperial Guard est actif (un seul SETTING en
        # jeu, choisi au hasard a la mise en place du scenario) : sa presence dans « Imperial Guard
        # Removed » ne depend donc PAS d'un allie explicitement pose par l'epreuve.
        "nom": "galactic_storm — victoire Kree Sentry SANS Gladiator vaincu : seul Rick Jones rejoint la reserve, l'environnement Imperial Guard de base est quand meme note",
        "scenario": "gs_kree_sentry",
        "heros": "spider_man",
        "carnet_attendu": {
            "gagnee": True,
            "cles": {"Recruited Allies": "Rick Jones", "Campaign Pool: Rick Jones": "1",
                      "Imperial Guard Removed": "gs092"},
            "cles_absentes": ["Campaign Pool: Gladiator"],
        },
    },
    {
        "nom": "galactic_storm — Time Pressure cumulee (venue du carnet) fixe la menace de depart de la Nega-Bombe au scenario 5",
        "scenario": "gs_kree_sentry",
        "heros": "spider_man",
        "carnet": {"Time Pressure": "20"},
        "carnet_attendu": {"gagnee": True, "cles": {"Time Pressure": "20"}},
        "suivant": "gs_supreme_intelligence",
        "attendu": {"menace": [["gs222a", 20]], "deck_rencontre": ["gs223"]},
    },
    {
        # Graine 42 : sans correction, le tirage aleatoire de l'environnement Imperial Guard au
        # scenario 2 tombe sur gs092 (meme tirage que celui constate au scenario 1 plus haut,
        # DETERMINISTE par graine) — exactement la carte que ce carnet entrant dit deja retiree de
        # la campagne. `CorrigerImperialGuardExclue` doit la remplacer par une AUTRE carte du meme
        # groupe (gs091 ou gs093), jamais par gs092 lui-meme.
        "nom": "galactic_storm — une carte Imperial Guard deja retiree de la campagne n'est pas repiochee au scenario suivant",
        "scenario": "gs_kree_sentry",
        "heros": "spider_man",
        "carnet": {"Imperial Guard Removed": "gs092"},
        "carnet_attendu": {"gagnee": True},
        "suivant": "gs_majestrix_verdict",
        "attendu": {"pas_en_jeu": ["gs092"], "un_parmi": [["en_jeu", ["gs091", "gs093"]]]},
    },
    {
        # Quasar porte gs302 Epoch (allie IDENTITY-SPECIFIC, desc.Class "Hero") dans son hero_deck.
        # Le pilote de test accepte toujours la PREMIERE option offerte : avec gs227 (Binary)
        # disponible en reserve, « chaque_joueur_peut_remplacer_un_allie » doit retirer Epoch et
        # poser Binary a la place.
        "nom": "galactic_storm — remplacement cible d'un allie d'identite par un allie de campagne au scenario 5",
        "scenario": "gs_kree_sentry",
        "heros": "quasar",
        "carnet": {"Campaign Pool: gs227": "1"},
        "carnet_attendu": {"gagnee": True},
        "suivant": "gs_supreme_intelligence",
        "heros_suivant": "quasar",
        "attendu": {"pas_deck": ["gs302"], "deck": ["gs227"]},
    },
]


# ============================================ La ville ne dort jamais (punisher_mcdc_2026)
#
# Carnet : « Final LEAD Location », « Gunrunner », « Seized Tech Crates » (combat 1) ; « Underling », « Punisher's Ordnance Cache » (combat 2) ;
# « Punisher Ally » (combat 3). Le moteur ecrit tout (cards/pack/punisher_mcdc_2026/campaign.py) ; l'ecran choisit le scenario des combats 2 et 3
# d'apres le carnet (public/js/campagne/catalogue-carnet.js, teste par tools/test_catalogue_carnet.mjs).
EPREUVES += [
    {
        "nom": "punisher — victoire au combat 2 (Jigsaw) : le sous-fifre et la Cache sont notes, et le combat 3 met en jeu les Caisses, la Cache et Punishment",
        "scenario": "tracking_the_buyer_the_getaway_jigsaw",
        "heros": "spider_man",
        "carnet": {"Seized Tech Crates": "1", "Player 1 Identity": "Spider-Man"},
        "carnet_attendu": {
            "gagnee": True,
            "scenario": "tracking_the_buyer",
            "cles": {"Underling": "Jigsaw", "Punisher's Ordnance Cache": "1"},
        },
        "suivant": "punishment_hobgoblin",
        "attendu": {"en_jeu": ["pu144", "pu141", "pu143"], "pas_en_jeu": ["pu145"]},
    },
    {
        "nom": "punisher — victoire au combat 3 : l'allie Punisher est gagne, et le combat 4 le met en jeu avec Power to the People",
        "scenario": "punishment_hobgoblin",
        "heros": "spider_man",
        "carnet": {"Seized Tech Crates": "1", "Punisher's Ordnance Cache": "1", "Underling": "Jigsaw", "Player 1 Identity": "Spider-Man"},
        "carnet_attendu": {"gagnee": True, "scenario": "punishment", "cles": {"Punisher Ally": "1"}},
        "suivant": "kingsfall",
        "attendu": {"en_jeu": ["pu146", "pu148", "pu149a"], "pas_en_jeu": ["pu147"], "compteurs": [["pu148", "counter", 1]]},
    },
    {
        "nom": "punisher — DEFAITE au combat 3 : pas d'allie, et le combat 4 n'a pas le Punisher (mais Power to the People y est)",
        "scenario": "punishment_hobgoblin",
        "heros": "spider_man",
        "fin": "Lose",
        "carnet": {"Seized Tech Crates": "1", "Punisher's Ordnance Cache": "1", "Underling": "Jigsaw", "Player 1 Identity": "Spider-Man"},
        "carnet_attendu": {"gagnee": False, "scenario": "punishment", "cles_absentes": ["Punisher Ally"]},
        "suivant": "kingsfall",
        "attendu": {"en_jeu": ["pu148", "pu149a"], "pas_en_jeu": ["pu146"]},
    },
    {
        "nom": "punisher — victoire au combat 4 (Kingsfall) : estampille `kingsfall`, campagne gagnee",
        "scenario": "kingsfall",
        "heros": "spider_man",
        "carnet": {"Punisher Ally": "1", "Player 1 Identity": "Spider-Man"},
        "carnet_attendu": {"gagnee": True, "scenario": "kingsfall"},
    },
]


# ============================================================ Shadowland (shadowland), livret FR
#
# Carnet : « Dark Protege Removed » (liste, ecrit par le moteur), « Player N Overpowering Scenario 1|2 » (ecrit par le moteur : la Corruption est
# retournee en face B), « Player N Recorded Card 1|2 » (SAISI par le joueur : `choix`), « Campaign Completed ». Voir docs/packs/shadowland/CAMPAGNE.md.
EPREUVES += [
    {
        "nom": "shadowland — victoire au scenario 1 avec une Corruption INSOUTENABLE : le scenario 2 la recoit avec 1 jeton Corruption",
        "scenario": "shadows_in_the_night",
        "heros": "spider_man",
        "avant": ["Puzzle.Counter('sl072a', 'corruption', 5)"],
        "carnet_attendu": {"gagnee": True, "scenario": "shadows_in_the_night",
                           "cles": {"Player 1 Overpowering Scenario 1": "1"}, "cles_presentes": ["Dark Protege Removed"]},
        "suivant": "shadow_labyrinth",
        "attendu": {"en_jeu": ["sl072a"], "compteurs": [["sl072a", "corruption", 1]]},
    },
    {
        "nom": "shadowland — victoire au scenario 1 avec une Corruption ordinaire : le scenario 2 la recoit SANS jeton",
        "scenario": "shadows_in_the_night",
        "heros": "spider_man",
        "carnet_attendu": {"gagnee": True, "cles_absentes": ["Player 1 Overpowering Scenario 1"]},
        "suivant": "shadow_labyrinth",
        "attendu": {"en_jeu": ["sl072a"], "compteurs": [["sl072a", "corruption", 0]]},
    },
    {
        "nom": "shadowland — la carte inscrite par le joueur apres le scenario 1 (Aunt May) entre en jeu au scenario 2, contre 1 jeton Corruption",
        "scenario": "shadows_in_the_night",
        "heros": "spider_man",
        "choix": {"Player 1 Recorded Card 1": "01006"},
        "carnet_attendu": {"gagnee": True},
        "suivant": "shadow_labyrinth",
        "attendu": {"en_jeu": ["01006", "sl072a"], "compteurs": [["sl072a", "corruption", 1]]},
    },
    {
        "nom": "shadowland — scenario 2 gagne avec une Corruption insoutenable, deux cartes inscrites : le scenario 3 pose 1 + 2 jetons Corruption et met les deux cartes en jeu",
        "scenario": "shadow_labyrinth",
        "heros": "spider_man",
        "carnet": {"Player 1 Overpowering Scenario 1": "1", "Player 1 Recorded Card 1": "01006"},
        "avant": ["Puzzle.Counter('sl072a', 'corruption', 5)"],
        "choix": {"Player 1 Recorded Card 2": "01008"},
        "carnet_attendu": {"gagnee": True, "scenario": "shadow_labyrinth",
                           "cles": {"Player 1 Overpowering Scenario 1": "1", "Player 1 Overpowering Scenario 2": "1", "Player 1 Recorded Card 1": "01006"}},
        "suivant": "heart_of_shadow",
        "attendu": {"en_jeu": ["01006", "01008"], "compteurs": [["sl072a", "corruption", 4]]},
    },
    {
        "nom": "shadowland — victoire au scenario 3 : la campagne est gagnee",
        "scenario": "heart_of_shadow",
        "heros": "spider_man",
        "carnet_attendu": {"gagnee": True, "scenario": "heart_of_shadow", "cles": {"Campaign Completed": "1"}},
    },
]
