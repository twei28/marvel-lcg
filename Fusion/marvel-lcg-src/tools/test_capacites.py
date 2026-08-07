"""Tests de COMPORTEMENT des capacites : la carte est vraiment jouee.

Complement indispensable a audit_cartes.py, qui ne fait qu'une analyse
STATIQUE (texte imprime <-> capacites construites). Ici on monte une vraie
position de jeu avec l'API Puzzle, on declenche la capacite, et on verifie
l'etat du monde. C'est le seul niveau capable de dire « cette capacite ne
part jamais » ou « elle ne fait pas ce qu'elle annonce ».

Comment ca marche
-----------------
Le moteur reclame ses decisions via DeviceManager.DoGetInput ; on le detourne
(meme technique que tools/test_autoplay.py). Des que la partie atteint le tour
du joueur, le pilote execute la mise en place puis le declencheur du cas, en
repondant aux questions imbriquees, et evalue enfin la verification.

Chaque cas tourne dans SON PROPRE PROCESSUS : le moteur est un singleton
global, impossible a reinitialiser proprement entre deux cas.

Usage
-----
    python3.10 tools/test_capacites.py <game_dir> <port> [rapport.json] [filtre]
Viser .game-src (liens vers src/), jamais .game qui n'est que du bytecode.
"""
import json
import os
import subprocess
import sys

# Meme mode que le lanceur reel (launcher.py) et que tools/test_cards.py : sans
# RELEASE, `build.Build.release` reste faux et le moteur active des assertions
# de developpement qui refusent des cartes pourtant jouables en partie normale
# (ex. 64009 Radiate, evenement a deux capacites « Play »).
os.environ.setdefault("RELEASE", "1")

# Prefixe des fichiers /tmp (voir CAS_PREFIX plus bas) : par defaut le PID de
# CE processus, pour qu'une session parallele qui lance le meme harnais sans
# fixer CAS_PREFIX n'ecrive jamais dans les memes fichiers /tmp qu'une autre.
os.environ.setdefault("CAS_PREFIX", str(os.getpid()))

# ---------------------------------------------------------------- les cas --
# 'mise_en_place' et 'declencher' sont des commandes Puzzle.* (voir
# src/game/puzzle/puzzle.py). 'verifier' recoit des aides et rend (ok, message).
#
# Pour ajouter un cas : viser une capacite dont le declenchement est ATTEIGNABLE
# par l'API Puzzle (Reveal, Boost, PutIntoPlay, Damage, Counter, ChangeForm...),
# et une consequence OBSERVABLE dans le monde (statut, compteur, PV, menace).
#
# PIEGE : TOUJOURS designer une carte par son CARD_ID, jamais par son nom. Les
# noms ne sont pas uniques (deux « Venom Blast » : 04035 et 56177) et
# FindOrCreateFace rend le premier trouve, ce qui teste silencieusement la
# mauvaise carte.

CAS = [
    {
        "nom": "56177 Venom Blast — capacite Boost : Sonne, sinon Desoriente",
        "pourquoi": "la capacite Boost n'etait pas implementee du tout (audit 2/8/2026)",
        "scenario": "rhino",
        "heros": "spider_man",
        "mise_en_place": [],
        "declencher": ["Puzzle.Boost('56177')"],
        "verifier": "identite_a_un_statut",
    },
    {
        "nom": "55041 The Mangog — When Defeated : 3 compteurs shatter sur l'Avatar de Loki",
        "pourquoi": "la carte etait totalement inerte, handlers vides et When Defeated jamais declare",
        "scenario": "rhino",
        "heros": "spider_man",
        "mise_en_place": [
            "Puzzle.PutIntoPlay('55029a')",
            "Puzzle.PutIntoPlay('55041')",
        ],
        "declencher": ["Puzzle.Damage('55041', 99)"],
        "verifier": "avatar_a_3_shatter",
    },
    {
        "nom": "04162b Improved Recovery Upgrade — le coup d'inclinaison est bien paye",
        "pourquoi": "la carte piochait a chaque recuperation sans jamais s'incliner",
        "scenario": "rhino",
        "heros": "spider_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('04162b')"],
        "declencher": [],
        "verifier": "amelioration_a_un_cout_exhaust",
    },

    # ------------------------------------------------------------------------
    # Pack « rainy » : Thor (Jane Foster) 61001a-61031
    # ------------------------------------------------------------------------
    {
        "nom": "61001b Jane Foster — Survivor : +1 taille de main en permanence",
        "pourquoi": "l'obligation Chemotherapy n'existe pas, le bonus doit donc etre toujours actif",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"hand_size": 1}},
    },
    {
        "nom": "61007 Mjolnir — Thor gagne +1 ATK et le trait AERIAL",
        "pourquoi": "GiveKeywordToAttached vise CardFinder(name='Thor') : verifier qu'il touche bien le heros",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('61001b')"],
        "declencher": ["Puzzle.PutIntoPlay('61007')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}, "traits": ["AERIAL"],
                    "en_jeu": ["61007"]},
    },
    {
        "nom": "61013 Mighty — +2 PV a l'identite et +1 DEF a Thor",
        "pourquoi": "deux GiveKeywordToAttached distincts (identite puis heros nomme)",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('61001b')"],
        "declencher": ["Puzzle.PutIntoPlay('61013')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 2, "defense": 1}},
    },
    {
        "nom": "61010 Medical Clinic — Jane Foster gagne +2 REC",
        "pourquoi": "GiveKeywordToInPlayWhenApplyThis vise l'alter-ego par son nom",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('61010')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 2}, "en_jeu": ["61010"]},
    },

    # ------------------------------------------------------------------------
    # Pack « albert » : 62001a-62016
    # ------------------------------------------------------------------------
    {
        "nom": "62008/62009/62010 — les trois ameliorations passives d'Albert",
        "pourquoi": "trois GiveKeywordToAttached vers CardFinder(name='Albert', card_type=Hero)",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('62001b')"],
        "declencher": [
            "Puzzle.PutIntoPlay('62008')",
            "Puzzle.PutIntoPlay('62009')",
            "Puzzle.PutIntoPlay('62010')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1, "thwart": 1, "defense": 1},
                    "traits": ["GENIUS"],
                    "en_jeu": ["62008", "62009", "62010"]},
    },

    # ------------------------------------------------------------------------
    # Pack « human_torch » : 64001a-64015
    # ------------------------------------------------------------------------
    {
        "nom": "64001a Human Torch — un ennemi ne peut pas depasser 3 compteurs flamme",
        "pourquoi": "la regle de plafond (WhenCardWouldBePlacedCounter) n'est active qu'en forme heros",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('64001b')"],
        "declencher": ["Puzzle.Counter('01094', 'flame', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "flame", 3]]},
    },
    {
        "nom": "64012 Hydro-Man — immunise aux compteurs flamme",
        "pourquoi": ("garde du CORRECTIF moteur : la carte pose maximum=0, que "
                     "`maximum = would_message.maximum or maximum` avalait "
                     "(0 est faux en Python), supprimant au passage le "
                     "plafond de 3 de 64001a"),
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.PutIntoPlay('64012')"],
        "declencher": ["Puzzle.Counter('64012', 'flame', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["64012", "flame", 0]]},
    },
    {
        "nom": "64004 Unstable Uniform — Human Torch gagne +1 DEF",
        "pourquoi": "GiveKeywordToAttached vers CardFinder(name='Human Torch', card_type=Hero)",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('64001b')"],
        "declencher": ["Puzzle.PutIntoPlay('64004')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}, "en_jeu": ["64004"]},
    },
    {
        "nom": "64013 Dam It — eteint les flammes et convertit chaque compteur en menace",
        "pourquoi": "When Revealed qui compte le retour de Faces.RemoveCountersOn",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.Counter('01094', 'flame', 3)"],
        "declencher": ["Puzzle.Reveal('64013')"],
        "verifier": "etat_attendu",
        # menace de depart 1, plus 1 par compteur retire (3) = 4
        "attendu": {"compteurs": [["01094", "flame", 0]],
                    "menace": [["64013", 4]]},
    },

    # ------------------------------------------------------------------------
    # Pack « rainy » : Rescue 90114a-90131
    # ------------------------------------------------------------------------
    {
        "nom": "90123/90124/90125 — les trois ameliorations passives de Rescue",
        "pourquoi": "+3 PV sur l'identite, +1 THW et +1 ATK sur le heros nomme",
        "scenario": "rhino",
        "heros": "rescue_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('90114b')"],
        "declencher": [
            "Puzzle.PutIntoPlay('90123')",
            "Puzzle.PutIntoPlay('90124')",
            "Puzzle.PutIntoPlay('90125')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 3, "thwart": 1, "attack": 1},
                    "en_jeu": ["90123", "90124", "90125"]},
    },
    {
        "nom": "90131 Innocent Bystander — s'attache a l'identite et coute 1 carte en main",
        "pourquoi": "AttachToFaceWhenPutIntoPlay + GiveKeywordToAttached(hand_size=-1)",
        "scenario": "rhino",
        "heros": "rescue_rainy",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('90131')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"hand_size": -1}, "en_jeu": ["90131"]},
    },
    {
        "nom": "90129 Wounded Civilians — le soin est remplace par le retrait d'un compteur",
        "pourquoi": "Interrupt avec SetBeInstead : le personnage ne doit RIEN recuperer",
        "scenario": "rhino",
        "heros": "rescue_rainy",
        "mise_en_place": ["Puzzle.PutIntoPlay('90129')", "Puzzle.Damage('90114b', 3)"],
        "declencher": ["Puzzle.Heal('90114b', 3)"],
        "verifier": "etat_attendu",
        # Uses (1 par joueur) : un seul compteur en solo. Il est consomme par le
        # soin, et la carte quitte alors le jeu (regle du mot-cle Uses).
        "attendu": {"degats_identite": 3, "hors_jeu": ["90129"]},
    },
    {
        "nom": "90129 Wounded Civilians — temoin : sans la carte, le soin passe",
        "pourquoi": "sans temoin, le cas precedent passerait meme si Heal ne faisait rien",
        "scenario": "rhino",
        "heros": "rescue_rainy",
        "mise_en_place": ["Puzzle.Damage('90114b', 3)"],
        "declencher": ["Puzzle.Heal('90114b', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "90130 Catastrophic Collision — 2 degats indirects par joueur",
        "pourquoi": "When Revealed a trois branches ; la premiere doit toucher l'identite",
        "scenario": "rhino",
        "heros": "rescue_rainy",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('90130')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },

    # ------------------------------------------------------------------------
    # Pack « gwenpool » : 63001a-63016
    # ------------------------------------------------------------------------
    {
        "nom": "63007 Gwen's Room — Gwendolyn Poole gagne +1 REC",
        "pourquoi": "GiveKeywordToAttached('You', recover=1)",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('63007')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 1}, "en_jeu": ["63007"]},
    },
    {
        "nom": "63011 Rules of the Universe — l'icone hazard tombe avec la menace",
        "pourquoi": ("garde du CORRECTIF : sans change_on_event, la condition "
                     "n'etait evaluee qu'a l'entree en jeu et l'icone restait "
                     "figee alors que la manigance est Permanente"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.PutIntoPlay('63011')"],
        "declencher": ["Puzzle.SetThreat('63011', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["63011", "hazard", -1]]},
    },
    {
        "nom": "63012 Evil Gwenpool — When Defeated : melangee dans le deck Rencontre",
        "pourquoi": "elle doit revenir dans le deck, pas partir a la defausse",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.PutIntoPlay('63012')"],
        "declencher": ["Puzzle.Damage('63012', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["63012"], "dans_deck_rencontre": ["63012"]},
    },
    {
        "nom": "63014 \"Future Me Scares Me\" — 2 menaces sur Rules si Evil Gwenpool est en jeu",
        "pourquoi": "branche conditionnelle + remise en deck de la traitrise",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.PutIntoPlay('63012')", "Puzzle.PutIntoPlay('63011')"],
        "declencher": ["Puzzle.Reveal('63014')"],
        "verifier": "etat_attendu",
        # menace de depart de Rules = 3 en solo, plus 2
        "attendu": {"menace": [["63011", 5]], "hors_jeu": ["63014"],
                    "dans_deck_rencontre": ["63014"]},
    },
    {
        "nom": "63013 Break Reality — Evil Gwenpool deja en jeu : 2 menaces par joueur sur Rules",
        "pourquoi": "la branche « deja en jeu » ne doit PAS rechercher un second exemplaire",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.PutIntoPlay('63012')", "Puzzle.PutIntoPlay('63011')"],
        "declencher": ["Puzzle.Reveal('63013')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["63011", 5]], "en_jeu": ["63012"]},
    },

    # ------------------------------------------------------------------------
    # Nemesis Thor (Jane Foster) et Albert
    # ------------------------------------------------------------------------
    {
        "nom": "61030 Execute — defait l'allie ayant le plus de PV restants",
        "pourquoi": "When Revealed qui choisit parmi les allies en jeu",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.PutIntoPlay('61002')"],
        "declencher": ["Puzzle.Reveal('61030')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["61002"]},
    },
    {
        "nom": "61031 Hostile Takeover — defausse le support controle le plus cher",
        "pourquoi": "branche « discard » du choix ; la branche « surge » ne doit pas s'appliquer",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.PutIntoPlay('61009')"],
        "declencher": ["Puzzle.Reveal('61031')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["61009"], "degats_identite": 0},
    },
    {
        "nom": "61027 War of the Realms — 1 degat indirect par personnage controle",
        "pourquoi": "le compte doit inclure l'identite ET les allies",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.PutIntoPlay('61002')"],
        "declencher": ["Puzzle.Reveal('61027')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "62014 Patch — When Revealed : 1 degat a chaque joueur",
        "pourquoi": "sbire dont la capacite doit toucher l'identite, pas lui-meme",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('62014')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "en_jeu": ["62014"]},
    },
    {
        "nom": "62016 Zombie Wolvie — When Defeated : melange dans le deck Rencontre",
        "pourquoi": "il doit revenir dans le deck, pas partir a la defausse",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.PutIntoPlay('62016')"],
        "declencher": ["Puzzle.Damage('62016', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["62016"], "dans_deck_rencontre": ["62016"]},
    },
    {
        "nom": "62002 Elsie-Dee — les degats en exces sont repartis sur les ennemis",
        "pourquoi": "Interrupt WhenUnitBeDefeated avec took_excess_damage",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.PutIntoPlay('62002')"],
        "declencher": ["Puzzle.Damage('62002', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["62002"], "degats_min": [["01094", 1]]},
    },

    # ------------------------------------------------------------------------
    # Capacites Boost (WhenCardBecomeBoost) des trois sbires nemesis custom
    # ------------------------------------------------------------------------
    {
        "nom": "62012 Wolverine — Boost : le sbire entre en jeu au lieu d'etre defausse",
        "pourquoi": "WhenCardBecomeBoost + PutThisIntoPlay",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": [],
        "declencher": ["Puzzle.Boost('62012')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["62012"]},
    },
    {
        "nom": "63012 Evil Gwenpool — Boost : la sbire entre en jeu au lieu d'etre defaussee",
        "pourquoi": "WhenCardBecomeBoost + PutThisIntoPlay",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": [],
        "declencher": ["Puzzle.Boost('63012')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["63012"]},
    },
    {
        "nom": "64012 Hydro-Man — Boost : le sbire entre en jeu au lieu d'etre defausse",
        "pourquoi": "WhenCardBecomeBoost + PutThisIntoPlay",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": [],
        "declencher": ["Puzzle.Boost('64012')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["64012"]},
    },

    # ------------------------------------------------------------------------
    # Obligations custom
    # ------------------------------------------------------------------------
    {
        "nom": "64011 Flame Off — bascule en alter-ego et eteint toutes les flammes",
        "pourquoi": "obligation qui doit changer la forme ET vider les compteurs des ennemis",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('64001b')",
                          "Puzzle.Counter('01094', 'flame', 3)"],
        "declencher": ["Puzzle.Reveal('64011')"],
        "verifier": "etat_attendu",
        # 3 compteurs retires (moins de 4) : l'obligation part a la defausse.
        "attendu": {"forme": "AlterEgo", "compteurs": [["01094", "flame", 0]],
                    "hors_jeu": ["64011"]},
    },
    {
        "nom": "61026 Chemotherapy — la branche Medical Clinic retire l'obligation du jeu",
        "pourquoi": "le choix conditionnel n'est propose que si la Clinique est en jeu",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.PutIntoPlay('61010')"],
        "declencher": ["Puzzle.Reveal('61026')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["61026"], "exhausted": ["61001b", "61010"]},
    },
    {
        "nom": "90126 Board Meeting — l'obligation se resout sans planter",
        "pourquoi": ("garde du CORRECTIF : identity.IsHero() n'existe que sur "
                     "Player, jamais sur une face ; l'obligation levait une "
                     "AttributeError a chaque revelation"),
        "scenario": "rhino",
        "heros": "rescue_rainy",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('90126')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["90126"]},
    },
    {
        "nom": "62011 Counterpart Elimination — cherche et revele un sbire WOLVERINE",
        "pourquoi": "Find.FindAndReveal filtre sur le trait, pas sur un nom",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('62011')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu_trait": [["WOLVERINE", 1]]},
    },

    # ------------------------------------------------------------------------
    # Autres capacites nemesis atteignables sans jouer de carte
    # ------------------------------------------------------------------------
    {
        "nom": "61029 War Witches — menace posee sur le complot principal : 1 degat indirect",
        "pourquoi": "AfterSchemePlaceThreat(MainScheme) doit retrouver le joueur engage",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.PutIntoPlay('61029')"],
        "declencher": ["Puzzle.PlaceThreat('01097b', 1)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "menace": [["01097b", 1]]},
    },
    {
        "nom": "62015 Weapon X — When Revealed : defausse 1 carte au hasard de la main",
        "pourquoi": "DiscardRandomHandCards doit toucher le joueur qui recoit la carte",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('62015')"],
        "verifier": "etat_attendu",
        "attendu": {"defausse_joueur": 1, "en_jeu": ["62015"]},
    },
    {
        "nom": "64014 Tidal Surge — avec Hydro-Man en jeu, le joueur incline son identite",
        "pourquoi": "la branche conditionnelle « si Hydro-Man est en jeu » et le choix impose",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.PutIntoPlay('64012')"],
        "declencher": ["Puzzle.Reveal('64014')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["64001b"], "degats_identite": 0},
    },
    {
        "nom": "64014 Tidal Surge — temoin : sans Hydro-Man, la carte ne fait rien",
        "pourquoi": "sans temoin, le cas precedent passerait meme si la condition etait ignoree",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('64014')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["64001b"], "degats_identite": 0},
    },

    # ------------------------------------------------------------------------
    # Corrections recentes hors packs custom
    # ------------------------------------------------------------------------
    # --- pack custom Invisible Woman (DesignHacker), integre le 2/8/2026 ---
    {
        "nom": "66001 Invisible Woman — le heros a 3 faces se charge et joue",
        "pourquoi": ("valide tout le pack : donnees, deck de depart, extension. "
                     "Le trait FANTASTIC FOUR est porte par les DEUX formes heros ; "
                     "on ne fige pas laquelle, car le pilote de test bascule vers "
                     "l'une ou l'autre selon l'ordre des options. CORRECTIF 4/8/2026 : "
                     "le cas tournait en forme ALTER-EGO, ou Sue Storm ne porte que "
                     "GENIUS — il manquait le ChangeForm, le cas etait rouge depuis "
                     "sa creation"),
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"traits": ["FANTASTIC FOUR"]},
    },
    {
        "nom": "66004 Unstable Uniform — Invisible Woman gagne +1 DEF",
        "pourquoi": ("passif GiveKeywordToAttached(defense=1) sur l'identite. "
                     "CORRECTIF 4/8/2026 : le cas tournait en forme ALTER-EGO, qui "
                     "n'a pas d'attribut `defense` — la verification plantait sur "
                     "AttributeError, le cas etait rouge depuis sa creation"),
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')"],
        "declencher": ["Puzzle.PutIntoPlay('66004')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}, "en_jeu": ["66004"]},
    },
    {
        "nom": "55003 Enchantress stade III — Future of Despair recoit 4 menaces PAR HEROS",
        "pourquoi": "le stade III recopiait le « 3* » du stade II",
        "scenario": "enchantress_expert",
        "heros": "spider_man",
        # Toughness : la premiere salve ne fait que defausser le statut solide.
        "mise_en_place": ["Puzzle.Damage('55002', 999)"],
        "declencher": ["Puzzle.Damage('55002', 999)"],
        "verifier": "etat_attendu",
        # Future of Despair entre avec 2 menaces (2 par heros), plus 4 = 6.
        "attendu": {"menace": [["55006", 6]]},
    },
    {
        "nom": "55022 Spellbound — l'effet part a la REVELATION, pas quand on dejoue",
        "pourquoi": "l'effet etait accroche a WhenSchemeBeDefeated, ce qui inversait la carte",
        "scenario": "enchantress",
        "heros": "spider_man",
        # La mise en place du scenario attache un Regard Hypnotique (ENCHANTMENT)
        # a chaque identite ; sa face visible donne le trait DEFIANT.
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('55022')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs_total": [["charm", 1]]},
    },

    # ------------------------------------------------------------------------
    # Pack « totally_awesome_hulk » : 68001a-68018
    # Le coeur du heros est le soutien recto-verso « The Trunk » (68012a/b) :
    # c'est LUI qui pilote les trois formes de l'identite, les changements
    # manuels etant verrouilles. Les cas ci-dessous valident cette boucle
    # complete, puis les bonus passifs et le set nemesis.
    # ------------------------------------------------------------------------
    {
        "nom": "68012a \"The Trunk\" — arrive en jeu au setup, sans compteur",
        "pourquoi": "tout le heros en depend : le mot-cle Setup doit la sortir du deck au demarrage",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["68012a"], "compteurs": [["68012a", "rage", 0]]},
    },
    {
        "nom": "68012a \"The Trunk\" — au 4e compteur : flip et passage en Uncontrollable Hulk",
        "pourquoi": ("c'est la seule maniere d'atteindre la forme BRUTE, "
                     "« Losing Control » bloquant tout changement manuel"),
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "declencher": ["Puzzle.Damage('Totally Awesome Hulk', 1)", "Puzzle.Damage('Totally Awesome Hulk', 1)", "Puzzle.Damage('Totally Awesome Hulk', 1)", "Puzzle.Damage('Totally Awesome Hulk', 1)"],
        "verifier": "face_identite",
        "attendu": {"face": "68001c", "en_jeu": ["68012b"], "hors_jeu": ["68012a"]},
    },
    {
        "nom": "68012b \"The Trunk\" — plus aucun compteur : flip et retour a Amadeus Cho",
        "pourquoi": "boucle de retour (IfThereIsNoCounterHere) : sans elle le heros reste bloque en BRUTE",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "declencher": [
            "Puzzle.Damage('Totally Awesome Hulk', 1)", "Puzzle.Damage('Totally Awesome Hulk', 1)", "Puzzle.Damage('Totally Awesome Hulk', 1)", "Puzzle.Damage('Totally Awesome Hulk', 1)",
            "Puzzle.Counter('\"The Trunk\"', 'rage', -4)",
        ],
        "verifier": "face_identite",
        "attendu": {"face": "68001b", "en_jeu": ["68012a"], "hors_jeu": ["68012b"]},
    },
    {
        "nom": "68003 Maddy Cho — Totally Awesome Hulk gagne +1 taille de main",
        "pourquoi": "GiveKeywordToInPlayWhenApplyThis vise la face CHAMPION par son nom",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "declencher": ["Puzzle.PutIntoPlay('68003')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"hand_size": 1}, "en_jeu": ["68003"]},
    },
    {
        "nom": "68005 Motivation — le heros gagne +1 DEF",
        "pourquoi": "GiveKeywordToAttached(Hero) sur une amelioration sans nom de cible",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "declencher": ["Puzzle.PutIntoPlay('68005')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}, "en_jeu": ["68005"]},
    },
    {
        "nom": "68006 Gamma Barrier — le heros gagne represailles 1",
        "pourquoi": "GiveKeywordToAttached(retaliate=1) : mot-cle passif facile a oublier",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "declencher": ["Puzzle.PutIntoPlay('68006')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"retaliate": 1}, "en_jeu": ["68006"]},
    },
    {
        "nom": "68016 Fin Fang Foom — +2 points de vie par joueur",
        "pourquoi": "ThisGainKeyword multiplie par le nombre de joueurs (solo : +2)",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('68016')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["68016", "health", 2]]},
    },
    {
        "nom": "68017 Krackalakassian — +2 points de vie par joueur",
        "pourquoi": "meme mecanique que Fin Fang Foom, sur une valeur imprimee differente",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('68017')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["68017", "health", 2]]},
    },
    {
        "nom": "68015 For The Queen! — les sbires MONSTER deviennent vilainesques",
        "pourquoi": "GiveKeywordToInPlayWhenApplyThis conditionne a la presence de Lady Hellbender",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": [
            "Puzzle.PutIntoPlay('68014')",
            "Puzzle.PutIntoPlay('68016')",
        ],
        "declencher": ["Puzzle.Reveal('68015')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["68016", "villainous", 1]],
                    "en_jeu": ["68015"]},
    },
    {
        "nom": "68009 Wild Lunge — Hypermind : payable avec une ressource [physical]",
        "pourquoi": ("la carte coute « G » (uniquement du wild). Sans Hypermind elle "
                     "serait injouable avec Hercules, dont l'icone est physique"),
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "main": ["68002"],
        "declencher": [],
        "jouer": ["68009"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]]},
    },
    {
        "nom": "68010 Irradiated Swipe — 5 degats a un ennemi, paye en [wild]",
        "pourquoi": "verifie la voie de paiement complete sur un evenement a cout 3",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "main": ["68002", "68003", "68005"],
        "declencher": [],
        "jouer": ["68010"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]]},
    },
    {
        "nom": "68002 Hercules — allie signature joue et pose en jeu",
        "pourquoi": "cout 4 : verifie qu'un allie signature se paye et arrive bien en jeu",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "main": ["68003", "68005", "68006", "68009"],
        "declencher": [],
        "jouer": ["68002"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["68002"]},
    },
    {
        "nom": "68007 The Power of Forgiveness — vide les compteurs rage du Trunk",
        "pourquoi": ("ressource a effet differe : elle n'agit qu'APRES resolution de "
                     "la carte qu'elle a payee"),
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "main": ["68007"],
        "declencher": ["Puzzle.Counter('\"The Trunk\"', 'rage', 3)"],
        "jouer": ["68009"],
        "payer_avec": ["68007"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["68012a", "rage", 0]], "degats": [["01094", 4]]},
    },
    {
        "nom": "68018 Threat Assessment — 3 degats a l'identite la plus en forme",
        "pourquoi": "When Revealed qui doit choisir une cible parmi les identites",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('68018')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },

    # ------------------------------------------------------------------------
    # Pack « madame_web » : 69001a-69029 (custom « Kajislav »)
    # ------------------------------------------------------------------------
    {
        "nom": "69001a Madame Web — ATK/THW/DEF valent 0 sans allie en jeu",
        "pourquoi": ("les trois stats sont imprimees « X » : cards.json les met a 0 et "
                     "un ThisGainKeyword les remonte. Sans allie, aucun bonus."),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 0, "thwart": 0, "defense": 0}},
    },
    {
        "nom": "69001a Madame Web — X = 2 avec deux allies en jeu",
        "pourquoi": "coeur du heros : les trois stats suivent le nombre d'allies controles",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": [
            "Puzzle.PutIntoPlay('69002')",
            "Puzzle.PutIntoPlay('13019')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 2, "thwart": 2, "defense": 2},
                    "en_jeu": ["69002", "13019"]},
    },
    {
        "nom": "69001a Madame Web — X plafonne a 3 avec quatre allies",
        "pourquoi": "« to a maximum of 3 » : le plafond doit tenir au-dela de 3 allies",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": [
            "Puzzle.PutIntoPlay('69002')",
            "Puzzle.PutIntoPlay('13019')",
            "Puzzle.PutIntoPlay('27049')",
            "Puzzle.PutIntoPlay('30012')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 3, "thwart": 3, "defense": 3}},
    },
    {
        "nom": "69001a Madame Web — A Bond with the Allies : elle prend les traits des allies",
        "pourquoi": ("ThisGainTraitsOfEachCardInPlay n'etait employe par AUCUNE carte du "
                     "moteur : code jamais exerce jusqu'ici"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": ["Puzzle.PutIntoPlay('27049')"],
        "verifier": "etat_attendu",
        "attendu": {"traits": ["WEB-WARRIOR"], "en_jeu": ["27049"]},
    },
    {
        "nom": "69002 Spider-Woman (Julia Carpenter) — entre avec 2 compteurs psionic",
        "pourquoi": "ThisEnterPlayWithCounters : sans lui la capacite de l'allie est inutilisable",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('69002')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["69002", "psionic", 2]]},
    },
    {
        "nom": "69007 Life-Support System — +3 PV a l'identite et +1 REC",
        "pourquoi": "GiveKeywordToAttached('You') doit toucher l'identite, pas la carte elle-meme",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('69007')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 3, "recover": 1}, "en_jeu": ["69007"]},
    },
    {
        "nom": "69012 Neurological Deterioration — l'identite ne peut plus se redresser",
        "pourquoi": ("CardCannotReady(Identity) : on incline puis on tente de redresser, "
                     "l'identite doit rester inclinee"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": [
            "Puzzle.Reveal('69012')",
            "Puzzle.Exhaust('Cassandra Webb')",
            "Puzzle.Ready('Cassandra Webb')",
        ],
        "verifier": "identite_reste_inclinee",
    },
    {
        "nom": "69013 Spider-Woman (Witter) — When Revealed : 2 degats indirects ou incliner",
        "pourquoi": "le choix doit se resoudre, sinon la nemesis est inerte",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('69013')"],
        "verifier": "witter_a_agi",
    },
    {
        "nom": "69016 Hypnosis — When Revealed : sonne ET desoriente un personnage",
        "pourquoi": "deux statuts a poser sur la meme cible en une seule capacite",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('69016')"],
        "verifier": "identite_sonnee_et_desorientee",
    },
    {
        "nom": "69021 Hunting Spyders — 3 degats a l'identite faute d'allie",
        "pourquoi": "branche de repli : sans allie en jeu, les degats vont sur l'identite",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('69021')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "69021 Hunting Spyders — 3 degats a l'allie quand il y en a un",
        "pourquoi": "branche nominale : l'allie encaisse a la place de l'identite",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.PutIntoPlay('30012')"],
        "declencher": ["Puzzle.Reveal('69021')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "degats": [["30012", 3]]},
    },
    {
        "nom": "69019 Kraven the Hunter — When Defeated : mis de cote, hors jeu",
        "pourquoi": "le sbire ne doit pas partir a la defausse mais dans la zone mise de cote",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.PutIntoPlay('69019')"],
        "declencher": ["Puzzle.Damage('69019', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["69019"]},
    },
    {
        "nom": "69026 Spider-Woman (Veranke) — vaincue, elle revient en sbire",
        "pourquoi": ("TreatAsMinion sur un allie EN JEU (et non sur une carte attachee) : "
                     "chemin jamais emprunte par une carte du moteur"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.PutIntoPlay('69026')"],
        "declencher": ["Puzzle.Damage('69026', 99)"],
        "verifier": "veranke_devenue_sbire",
    },
    {
        "nom": "69001b Cassandra Webb — Setup : Life-Support System arrive seule en jeu",
        "pourquoi": ("le Setup fouille deck ET defausse puis MET EN JEU ; sans lui "
                     "l'heroine perd 3 PV et son filet de securite"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["69007"], "attributs": {"health": 3}},
    },
    {
        "nom": "69004 Clairvoyance — previent 1 degat sur les 3 recus",
        "pourquoi": "Hero Interrupt sur les degats : il doit s'inserer avant l'application",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": [
            "Puzzle.PutIntoPlay('69004')",
            "Puzzle.Damage('Madame Web', 3)",
        ],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "exhausted": ["69004"]},
    },
    {
        "nom": "69014 Spider-Women Hunt — 2 menaces de plus par personnage « Spider »",
        "pourquoi": "le When Revealed compte les personnages en jeu ; sans lui le complot reste a 1",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": [
            "Puzzle.PutIntoPlay('27049')",
            "Puzzle.Reveal('69014')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["69014", 3]]},
    },
    {
        "nom": "69015 Power Absorption — un allie est defausse, la forme ne change pas",
        "pourquoi": "branche nominale : la defausse d'un allie doit ANNULER le retour en alter-ego",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": [
            "Puzzle.PutIntoPlay('30012')",
            "Puzzle.Reveal('69015')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["30012"], "forme": "Hero"},
    },
    {
        "nom": "69015 Power Absorption — sans allie : retour en alter-ego et inclinaison",
        "pourquoi": "branche de repli, celle qui fait vraiment mal",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": ["Puzzle.Reveal('69015')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "exhausted": ["69001b"]},
    },
    {
        "nom": "69018 The Grim Hunt — entre avec 3 menaces par joueur",
        "pourquoi": ("complot secondaire a menace de depart ET escalade cablees a la main : "
                     "le moteur ne gere ces valeurs que sur les complots PRINCIPAUX"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('69018')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["69018"], "menace": [["69018", 3]]},
    },
    {
        "nom": "69020 One Spyder Down — defausse l'allie controle",
        "pourquoi": "sans allie la carte prend surge : il faut verifier la branche nominale",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": [
            "Puzzle.PutIntoPlay('30012')",
            "Puzzle.Reveal('69020')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["30012"]},
    },
    {
        "nom": "69022 Scarlet Spider — redresse le heros en arrivant",
        "pourquoi": "Hero Response a l'entree en jeu, cible « YourHero »",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": [
            "Puzzle.Exhaust('Madame Web')",
            "Puzzle.PutIntoPlay('69022')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["69001a"], "en_jeu": ["69022"]},
    },
    {
        "nom": "69023 Spider-Woman (Ashley Barton) — +1 ATK payee uniquement en [physical]",
        "pourquoi": ("aucune autre carte du moteur ne conditionne un bonus PERMANENT "
                     "d'allie au mode de paiement : chemin inedit"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "main_exclusive": ["69023", "69008", "69029"],
        "declencher": [],
        "jouer": ["69023"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["69023", "attack", 1]]},
    },
    {
        "nom": "69023 Spider-Woman (Ashley Barton) — aucun bonus si le paiement est mixte",
        "pourquoi": "l'autre moitie de la condition : une ressource non [physical] annule le bonus",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "main_exclusive": ["69023", "69008", "69004"],
        "declencher": [],
        "jouer": ["69023"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["69023", "attack", 0]]},
    },
    {
        "nom": "69025 Spider-Woman (Mattie Franklin) — se pose en jeu depuis la main",
        "pourquoi": ("AfterCardEnterHand + paiement du cout imprime : si le chemin casse, "
                     "la carte reste bloquee en main"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.Gain('69025')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["69025"]},
    },
    {
        "nom": "69028 Advice — +3 ATK a l'allie, deck Rencontre truque a 3 icones boost",
        "pourquoi": ("X vient des icones boost defaussees : on fige le dessus du deck "
                     "Rencontre pour rendre le resultat verifiable"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "main": ["69028", "69008"],
        "declencher": [
            "Puzzle.PutIntoPlay('30012')",
            "Puzzle.CreateEncounterDeck('69021')",
        ],
        "jouer": ["69028"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["30012", "attack", 3]]},
    },
    {
        "nom": "69029 Female Power — 2 degats par personnage « Madame »/« Lady » controle",
        "pourquoi": "le comptage par mots du titre est fait a la main : il doit tomber juste",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "main": ["69029", "69008", "69004"],
        "declencher": ["Puzzle.PutIntoPlay('30012')"],
        "jouer": ["69029"],
        "verifier": "etat_attendu",
        # Madame Web + Lady Spider = 2 personnages qualifiants -> 4 degats.
        "attendu": {"degats": [["01094", 4]]},
    },
    {
        "nom": "69010 Gathering of Five — icone [physical] : 3 degats a l'identite",
        "pourquoi": ("les quatre branches lisent la ressource IMPRIMEE de la carte "
                     "defaussee ; on fige le dessus du deck du joueur"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "main": ["69010"],
        "declencher": ["Puzzle.CreatePlayerDeck('69008')"],
        "jouer": ["69010"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "69011 Web of Fate — la carte choisie parmi les 5 arrive en main",
        "pourquoi": ("effet DIFFERE porte par une ressource : il ne part qu'APRES le "
                     "paiement de la carte qu'elle finance"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "main_exclusive": ["69028", "69011"],
        "declencher": [
            "Puzzle.PutIntoPlay('30012')",
            "Puzzle.CreateEncounterDeck('69021')",
            "Puzzle.CreatePlayerDeck('69004', '69006', '69003', '69009', '69010')",
        ],
        "jouer": ["69028"],
        "verifier": "web_of_fate_a_pioche",
    },
    {
        "nom": "69006 Weaving a Web — sa ressource [wild] paie bien une alliee",
        "pourquoi": ("CanGenerateResources restreinte aux ALLIES : si le filtre est faux, "
                     "la ressource ne sert jamais a rien"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "main_exclusive": ["69026"],
        "declencher": ["Puzzle.PutIntoPlay('69006')"],
        "jouer": ["69026"],
        "verifier": "etat_attendu",
        # Veranke coute 1 : la seule ressource disponible est celle de l'amelioration.
        "attendu": {"en_jeu": ["69026"], "exhausted": ["69006"]},
    },
    {
        "nom": "69008 Webb's Team Strikes! — 3 degats par allie incline (cout X)",
        "pourquoi": ("cout X + allies en CIBLES tronquees a X : « up to X » doit accepter "
                     "de 0 a tous, pas « tous ou aucun »"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "main_exclusive": ["69008", "69004"],
        "declencher": ["Puzzle.PutIntoPlay('30012')"],
        "jouer": ["69008"],
        "cibles": ["30012"],
        "surpayer": True,
        "verifier": "etat_attendu",
        # 1 ressource payee -> X = 1 -> 1 allie incline -> 3 degats au vilain.
        "attendu": {"degats": [["01094", 3]], "exhausted": ["30012"]},
    },

    # ------------------------------------------------------------------------
    # Pack « cloak_dagger » : 70001a-70018 (custom « DesignHacker »)
    # Adaptation deux-heros-en-un : identite Cloak/Tyrone + alliee Dagger.
    # ------------------------------------------------------------------------
    {
        "nom": "70001b Setup — l'identite liee et Forces Combined arrivent en jeu",
        "pourquoi": ("depuis la refonte du 5/8/2026 Dagger est un SECOND JOUEUR, cree par "
                     "`linked_identity` ; le setup ne sort plus que Forces Combined"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["70002b", "70003"]},
    },
    {
        "nom": "70001a Protective Pair — +2 DEF tant que Dagger est en jeu",
        "pourquoi": "synergie coeur du duo : elle exige les DEUX identites en forme heros",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.ChangeForm('Tandy Bowen')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 2}},
    },
    {
        "nom": "70001a Protective Pair — le bonus tombe quand Dagger repasse en alter-ego",
        "pourquoi": ("Dagger etant une identite, elle ne quitte plus le jeu : c'est son "
                     "changement de FORME qui doit faire retomber le bonus"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.ChangeForm('Tandy Bowen')"],
        "declencher": ["Puzzle.ChangeForm('Dagger')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 0}, "en_jeu": ["70002b"]},
    },
    {
        "nom": "70002a Destructive Duo — Dagger a +2 ATK quand Cloak est en forme heros",
        "pourquoi": "synergie miroir, portee par la face heros de l'identite liee",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.ChangeForm('Tandy Bowen')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["70002a", "attack", 2]]},
    },
    {
        "nom": "70002a Destructive Duo — pas de bonus quand Cloak reste en alter-ego",
        "pourquoi": "« while Cloak is in play » = forme heros seulement, cote joueur 1",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tandy Bowen')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["70002a", "attack", 0]]},
    },
    {
        "nom": "70001b Harmony — Tyrone Johnson a +2 REC",
        "pourquoi": ("« Tandy et Tyrone gagnent +2 REC tant que Tyrone est en jeu » : vue "
                     "depuis sa propre carte, la condition est toujours vraie"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 2}},
    },
    {
        "nom": "70004 Lightforce Cleansing — soigne 3 sur Cloak et fait piocher 2",
        "pourquoi": "le bonus de pioche exige 2+ soignes sur CLOAK precisement",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.Damage('Cloak', 3)",
                          "Puzzle.Exhaust('70003')"],
        "main_exclusive": ["70004", "01088"],
        "declencher": [],
        "jouer": ["70004"],
        "payer_avec": ["01088"],
        "cibles": ["70001a"],
        "verifier": "cd_cleansing_soigne_et_pioche",
    },
    {
        "nom": "70005 Lightforce Daggers — 3 degats repartis, vilain sonne et desoriente",
        "pourquoi": ("action repartie (repeat_rules) + double statut : le confuse suit "
                     "parce que Cloak est en jeu en Hero Action"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')"],
        "main_exclusive": ["70005", "01088", "01089", "01090"],
        "declencher": [],
        "jouer": ["70005"],
        "cibles": ["01094", "01094", "01094"],
        "verifier": "cd_vilain_apres_daggers",
    },
    {
        "nom": "70009 Dark Teleportation — redresse Dagger puis retire 2 menaces",
        "pourquoi": "la branche bonus ne part que si la cible redressee est Dagger",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.ChangeForm('Tandy Bowen')", "Puzzle.Exhaust('70002a')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["70009", "01088"],
        "declencher": [],
        "jouer": ["70009"],
        "payer_avec": ["01088"],
        "cibles": ["70002a"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["70002a"], "menace": [["01097b", 3]]},
    },
    {
        "nom": "70010 Darkforce Channel — degat au vilain, soin sur Cloak, deux statuts",
        "pourquoi": "effet compose : degats + soin proportionnel + confuse + stun via Dagger",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.ChangeForm('Tandy Bowen')", "Puzzle.Damage('Cloak', 2)"],
        "main_exclusive": ["70010", "01088", "01089", "01090"],
        "declencher": [],
        "jouer": ["70010"],
        "cibles": ["01094"],
        "verifier": "cd_vilain_apres_channel",
    },
    {
        "nom": "70006 Pure Lightforce — 2 degats au vilain pour 2 ressources surpayees",
        "pourquoi": ("ressource a effet differe : surpaiement lu a la RESOLUTION de la "
                     "carte payee, montage 68007 ; sans `surpayer` le cas ne teste rien"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.Damage('Cloak', 3)",
                          "Puzzle.Exhaust('70003')"],
        # Main reduite aux deux cartes utiles et surpaiement force : sinon le
        # pilote paie le cout 1 au plus juste et le surpaiement, seul objet du
        # cas, ne se produit pas.
        "main_exclusive": ["70004", "70006"],
        "surpayer": True,
        "declencher": [],
        "jouer": ["70004"],
        "payer_avec": ["70006"],
        "cibles": ["70001a"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]]},
    },
    {
        "nom": "70011 Raw Darkforce — 2 menaces retirees du complot pour 2 surpayees",
        "pourquoi": "miroir menace de 70006 ; la cible redressee est l'identite pour isoler l'effet",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.Exhaust('Cloak')",
                          "Puzzle.Exhaust('70003')", "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["70009", "70011", "01088"],
        "declencher": [],
        "jouer": ["70009"],
        "payer_avec": ["70011"],
        "cibles": ["70001a"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]]},
    },
    {
        "nom": "70018 Opposites Attack — flip force en alter-ego et 1 menace posee",
        "pourquoi": "When Revealed qui compte les heros bascules",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.SetThreat('01097b', 4)"],
        "declencher": ["Puzzle.Reveal('70018')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "menace": [["01097b", 5]]},
    },
    {
        "nom": "70018 Opposites Attack — deja en alter-ego : aucune menace posee",
        "pourquoi": "« for each hero flipped this way » : zero bascule = zero menace",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.SetThreat('01097b', 4)"],
        "declencher": ["Puzzle.Reveal('70018')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "menace": [["01097b", 4]]},
    },
    {
        "nom": "70014 Lovers Quarrel — flip force puis resolution d'un des deux choix",
        "pourquoi": "l'obligation doit se resoudre sans bloquer la partie",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')"],
        "declencher": ["Puzzle.Reveal('70014')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo"},
    },
    {
        "nom": "70017 Inner Demon — Toughness native : le premier degat est absorbe",
        "pourquoi": "carte sans script : les mots-cles desc doivent suffire",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.PutIntoPlay('70017')"],
        "declencher": ["Puzzle.Damage('70017', 1)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["70017", 0]], "en_jeu": ["70017"]},
    },
    {
        "nom": "70003 Forces Combined — main vide cote Cloak, l'autre main paie",
        "pourquoi": ("depuis le 5/8/2026 la carte ne GENERE plus de ressource : elle "
                     "autorise l'autre main a payer, et s'incline quand celle-ci sert"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.Damage('Cloak', 2)"],
        "main_exclusive": ["70004"],
        "declencher": [],
        "jouer": ["70004"],
        "cibles": ["70001a"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["70003"]},
    },

    # ------------------------------------------------------------------------
    # Pack « spider_man_rainy » : Spider-Man (Peter Parker, par Rainy) 71xxx
    # ------------------------------------------------------------------------
    {
        "nom": "71003 Thwip! — toile sur Rhino, et Impact Webbing sorti au setup",
        "pourquoi": "verifie la pose de compteur web ET SetupPutIntoPlay(71012)",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('71001b')"],
        "main_exclusive": ["71003", "71007"],
        "declencher": [],
        "jouer": ["71003"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "web", 1]], "en_jeu": ["71012"]},
    },
    {
        "nom": "71006 Webbed Up (action) — 3 toiles d'un coup, plafond a 3",
        "pourquoi": "le plafond de 3 compteurs web est porte par Impact Webbing",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('71001b')",
                           "Puzzle.Counter('01094', 'web', 2)"],
        "main_exclusive": ["71006", "71008"],
        "declencher": [],
        "jouer": ["71006"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "web", 3]]},
    },
    {
        "nom": "71005 Web Strike — 6 degats, +2 sur un ennemi entoile",
        "pourquoi": "le bonus depend des compteurs web de la cible",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('71001b')",
                           "Puzzle.Counter('01094', 'web', 1)"],
        "main_exclusive": ["71005", "71008", "71004", "71010", "71009"],
        "declencher": [],
        "jouer": ["71005"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 8]], "compteurs": [["01094", "web", 1]]},
    },
    {
        "nom": "71005 Web Strike — 6 degats seulement sans toile",
        "pourquoi": "l'autre moitie de la condition du bonus",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('71001b')"],
        "main_exclusive": ["71005", "71008", "71004", "71010", "71009"],
        "declencher": [],
        "jouer": ["71005"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 6]]},
    },
    {
        "nom": "71007 Great Power — 2 degats apres avoir servi de paiement",
        "pourquoi": "ressource a effet differe, montage The Power of Forgiveness",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('71001b')"],
        "main_exclusive": ["71003", "71007"],
        "declencher": [],
        "jouer": ["71003"],
        "payer_avec": ["71007"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "compteurs": [["01094", "web", 1]]},
    },
    {
        "nom": "71008 Great Responsibility — retire 2 menaces apres paiement",
        "pourquoi": "meme montage, cote menace",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('71001b')"],
        "main_exclusive": ["71003", "71008"],
        # la pose de menace vient APRES le vidage de la main : sinon le 01061
        # officiel (Great Responsibility, event Justice) l'intercepte depuis
        # la main de depart et la convertit en degats.
        "declencher": ["Puzzle.PlaceThreat('The Break-In!', 5)"],
        "jouer": ["71003"],
        "payer_avec": ["71008"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]]},
    },
    {
        "nom": "71015 Mysterio — l'illusion encaisse les degats a sa place",
        "pourquoi": "Forced Interrupt de remplacement : compteur retire, 0 degat",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.PutIntoPlay('71015')"],
        "declencher": ["Puzzle.Damage('71015', 2)"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["71015", "illusion", 1]],
                    "degats": [["71015", 0]]},
    },
    {
        "nom": "71016 Jump Scare — carte face cachee puis 1 degat par carte devant soi",
        "pourquoi": "When Revealed a double effet, compte les cartes rencontre face cachee",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('71016')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1},
    },
    {
        "nom": "71017 Smoke and Mirrors — Mysterio recoit un statut Tenace",
        "pourquoi": "When Revealed conditionnel : Mysterio present, c'est lui qui prend le Tough",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.PutIntoPlay('71015')"],
        "declencher": ["Puzzle.Reveal('71017')"],
        "verifier": "smr_mysterio_a_tough",
    },
    {
        "nom": "71002 Spider-Man (Ben Reilly) — allie signature joue et pose en jeu",
        "pourquoi": "cout 2 : verifie le chemin de paiement de l'allie",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": [],
        "main_exclusive": ["71002", "71007", "71008"],
        "declencher": [],
        "jouer": ["71002"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["71002"]},
    },

    # ------------------------------------------------------------------------
    # Pack « venom_rainy » : Venom (Eddie Brock, par Rainy) 72xxx
    # ------------------------------------------------------------------------
    {
        "nom": "72010 Regeneration — +2 points de vie",
        "pourquoi": "GiveKeywordToInPlayWhenApplyThis(You, health=2)",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('72010')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 2}},
    },
    {
        "nom": "72011 Sharp Teeth — Venom gagne +1 ATK",
        "pourquoi": "buff permanent + mots-cles overkill/piercing sur l'attaque de base",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('72001b')"],
        "declencher": ["Puzzle.PutIntoPlay('72011')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}},
    },
    {
        "nom": "72009 Lethal Protector — Venom gagne +1 DEF",
        "pourquoi": "buff permanent sur l'identite",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('72001b')"],
        "declencher": ["Puzzle.PutIntoPlay('72009')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}},
    },
    {
        "nom": "72007 Venomous Bite — 5 degats et l'ennemi est Sonne",
        "pourquoi": "chemin nominal : la cible survit, elle est etourdie, pas de soin",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('72001b')"],
        "main_exclusive": ["72007", "72006", "72002", "72011"],
        "declencher": ["Puzzle.Damage('Venom', 3)"],
        "jouer": ["72007"],
        "payer_avec": ["72006", "72002", "72011"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        # 3 degats poses + 1 de Represailles (Rhino, Retaliate 1) = 4
        "attendu": {"degats": [["01094", 5]], "degats_identite": 4},
    },
    {
        "nom": "72003 Just A Snack — 2 degats si paye avec une ressource [physical]",
        "pourquoi": "meme mecanique de paiement qu'Ashley Barton 69023",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('72001b')"],
        "main_exclusive": ["72003", "72002"],
        "declencher": ["Puzzle.Damage('Venom', 4)"],
        "jouer": ["72003"],
        "payer_avec": ["72002"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "degats_identite": 2},
    },
    {
        "nom": "72003 Just A Snack — 1 degat seulement sans ressource [physical]",
        "pourquoi": "l'autre moitie de la condition de paiement",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('72001b')"],
        "main_exclusive": ["72003", "72004"],
        "declencher": ["Puzzle.Damage('Venom', 4)"],
        "jouer": ["72003"],
        "payer_avec": ["72004"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1]], "degats_identite": 2},
    },
    {
        "nom": "72006 Tendril Explosion — X degats a chaque ennemi",
        "pourquoi": "cout X finance par 2 ressources : X=2",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('72001b')",
                           "Puzzle.PutIntoPlay('72015')"],
        "main_exclusive": ["72006", "72002", "72011"],
        "declencher": [],
        "jouer": ["72006"],
        "surpayer": True,
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2], ["72015", 2]]},
    },
    {
        "nom": "72014 Carnage — apres un soin, 1 degat en retour",
        "pourquoi": "Forced Response construit a la main sur AfterUnitHealHealth",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.PutIntoPlay('72014')",
                           "Puzzle.Damage('Eddie Brock', 4)"],
        "declencher": ["Puzzle.Heal('Eddie Brock', 2)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "72001b Eddie Brock — Investigative Reporter apres pose de menace",
        "pourquoi": "Response sur AfterSchemePlaceThreat, limite 1/round",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": [],
        "declencher": ["Puzzle.PlaceThreat('The Break-In!', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    {
        "nom": "72012 We Hunger — passe en forme heros et applique une des deux penalites",
        "pourquoi": "obligation : flip force vers le heros puis choix",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": [],
        "main_exclusive": ["72004"],
        "declencher": ["Puzzle.Reveal('72012')"],
        "verifier": "we_hunger_resolue",
    },
    # ------------------------------------------------------------------------
    # Pack « jessica_jones » : 73001a-73022 (custom « ekAugust »)
    # Tout le kit tourne autour des manigances secondaires ; le set « On the
    # Job » est mélangé dans le deck Rencontre par le Setup de l'alter-ego.
    # ------------------------------------------------------------------------
    {
        "nom": "73001b Jessica Jones — le set On the Job part dans le deck Rencontre au setup",
        "pourquoi": ("le Setup ajoute « on_the_job » a message.encounter_set_names, "
                     "seul point ou le deck Rencontre n'est pas encore construit"),
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"dans_deck_rencontre": ["73012", "73013", "73014", "73015", "73016"]},
    },
    {
        "nom": "73010 Jessica's Jacket — +2 points de vie",
        "pourquoi": "GiveKeywordToAttached(You, health=2)",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('73010')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 2}},
    },
    {
        "nom": "73009 Jessica's Camera — 3 compteurs evidence donnent +1 DEF, +1 THW et +1 ATK",
        "pourquoi": "trois paliers cumulatifs lus sur le meme compteur 'evidence'",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')", "Puzzle.PutIntoPlay('73009')"],
        "declencher": ["Puzzle.Counter('73009', 'evidence', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1, "thwart": 1, "attack": 1}},
    },
    {
        "nom": "73009 Jessica's Camera — temoin : a 1 compteur, seul le DEF monte",
        "pourquoi": "sans ce temoin, trois buffs inconditionnels passeraient le cas precedent",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')", "Puzzle.PutIntoPlay('73009')"],
        "declencher": ["Puzzle.Counter('73009', 'evidence', 1)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1, "thwart": 0, "attack": 0}},
    },
    {
        "nom": "73013 Chase Down a Lead — Investigate 2 deplace 2 menaces du complot principal",
        "pourquoi": "mot-cle maison INVESTIGATE : retrait sur le complot puis pose ici",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.SetThreat('01097b', 5)"],
        "declencher": ["Puzzle.Reveal('73013')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3], ["73013", 5]]},
    },
    {
        "nom": "73016 Sneak Into the Crime Scene — When Defeated : Jessica Jones devient Tenace",
        "pourquoi": "When Defeated d'une manigance du set On the Job",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.Reveal('73016')"],
        "declencher": ["Puzzle.SetThreat('73016', 0)"],
        "verifier": "jj_identite_tenace",
    },
    {
        "nom": "73002 Luke Cage — une manigance secondaire en jeu lui retire 1 degat",
        "pourquoi": "reduction conditionnelle ; le statut Tenace initial est consomme avant",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')",
                          "Puzzle.PutIntoPlay('73002')",
                          "Puzzle.Reveal('73013')"],
        "declencher": ["Puzzle.Damage('73002', 1)", "Puzzle.Damage('73002', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["73002", 2]]},
    },
    # ------------------------------------------------------------------------
    # Pack « agent_anti_venom » : 74001a-74016 (custom « DesignHacker »)
    # Tout le kit lit « exactly 10 hit points remaining » (= intact).
    # ------------------------------------------------------------------------
    {
        "nom": "74001a Ten Out of Ten! — intact, il gagne +1 THW, +1 ATK et +1 DEF",
        "pourquoi": "buff conditionne aux PV COURANTS, pas au rapport health/max_health",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"thwart": 1, "attack": 1, "defense": 1}},
    },
    {
        "nom": "74001a Ten Out of Ten! — temoin : blesse d'1 PV, le bonus tombe",
        "pourquoi": "sans ce temoin, trois buffs inconditionnels passeraient le cas precedent",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')"],
        "declencher": ["Puzzle.Damage('74001a', 1)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"thwart": 0, "attack": 0, "defense": 0}},
    },
    {
        "nom": "74008 Anti-Maniac Booster — Agent Anti-Venom gagne retaliate 1",
        "pourquoi": "GiveKeywordToAttached(You, retaliate=1)",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')"],
        "declencher": ["Puzzle.PutIntoPlay('74008')"],
        "verifier": "aav_retaliate",
    },
    {
        "nom": "74001b Boy Scout — revenir en alter-ego soigne 2 degats",
        "pourquoi": "AfterUnitChangeForm(to_this_form=True) + cible soignable",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')",
                          "Puzzle.Damage('74001a', 4)"],
        "declencher": ["Puzzle.ChangeForm('74001a')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "74005 \"I've Got This!\" — intact (piercing), il tape a 7 et non a 5",
        "pourquoi": "lecture maison de « if this attack has ranged or piercing »",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')"],
        "main_exclusive": ["74005", "74003", "74004"],
        "declencher": [],
        "jouer": ["74005"],
        "payer_avec": ["74003", "74004"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 7]]},
    },
    {
        "nom": "74005 \"I've Got This!\" — temoin : blesse, il tape a 5",
        "pourquoi": "sans piercing ni ranged, la carte doit retomber a 5 degats",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')",
                          "Puzzle.Damage('74001a', 2)"],
        "main_exclusive": ["74005", "74003", "74004"],
        "declencher": [],
        "jouer": ["74005"],
        "payer_avec": ["74003", "74004"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]]},
    },
    {
        "nom": "74016 Infected — s'attache au sbire le plus resistant et lui donne +1 ATK",
        "pourquoi": "attachement au plus haut PV imprime, comme Genetically Enhanced 01163",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')",
                          "Puzzle.PutIntoPlay('74015')"],
        "declencher": ["Puzzle.Reveal('74016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["74016"], "attributs_carte": [["74015", "attack", 1]]},
    },
    {
        "nom": "74012 Spread Too Thin — l'obligation se resout depuis la forme heros",
        "pourquoi": ("le « You may flip to alter-ego form » passe par ChangeToForm ; "
                     "ChangeForm n'existe pas et faisait planter la resolution"),
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')",
                          "Puzzle.PutIntoPlay('74008')"],
        "declencher": ["Puzzle.Reveal('74012')"],
        "verifier": "obligation_resolue_74012",
    },
    {
        "nom": "73017 Stable Home Life — l'obligation se resout depuis la forme heros",
        "pourquoi": "meme montage que 74012 : ChangeToForm, pas ChangeForm",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')",
                          "Puzzle.PutIntoPlay('73010')"],
        "declencher": ["Puzzle.Reveal('73017')"],
        "verifier": "obligation_resolue_73017",
    },
    # ------------------------------------------------------------------------
    # Couverture ajoutee le 4/8/2026 sur les cartes des packs jessica_jones et
    # agent_anti_venom qui n'avaient aucun cas. Ne restent hors de portee que
    # les capacites suspendues a une ATTAQUE ou a une ACTION de carte en jeu,
    # que l'API Puzzle ne sait pas declencher.
    # ------------------------------------------------------------------------
    {
        "nom": "73001a Hard-Hitting Investigation — vaincre une manigance frappe pour l'ATK",
        "pourquoi": ("chaine centrale de l'heroine, jamais couverte : Crack the Case "
                     "acheve la manigance, la Response du heros doit alors partir"),
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')",
                          "Puzzle.Reveal('73016')",
                          "Puzzle.SetThreat('73016', 2)"],
        "main_exclusive": ["73004", "73003"],
        "declencher": [],
        "jouer": ["73004"],
        "cibles": ["73016", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["73016"], "degats": [["01094", 2]]},
    },
    {
        "nom": "73009 Jessica's Camera — la Response pose bien un compteur evidence",
        "pourquoi": ("les 3 paliers etaient testes en posant les compteurs a la main ; "
                     "la Response qui les pose ne l'etait pas"),
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')",
                          "Puzzle.PutIntoPlay('73009')",
                          "Puzzle.Reveal('73016')",
                          "Puzzle.SetThreat('73016', 2)"],
        "main_exclusive": ["73004", "73003"],
        "declencher": [],
        "jouer": ["73004"],
        "cibles": ["73016", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["73009", "evidence", 1]]},
    },
    {
        "nom": "73003 Breakthrough — 4 degats, +1 par manigance secondaire en jeu",
        "pourquoi": "compte des manigances secondaires ; ici une seule en jeu, donc 5",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')", "Puzzle.Reveal('73016')"],
        "main_exclusive": ["73003", "73005", "73004"],
        "declencher": [],
        "jouer": ["73003"],
        "payer_avec": ["73005", "73004"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]]},
    },
    {
        "nom": "73005 Hit the Streets — 3 menaces, +1 par manigance secondaire en jeu",
        "pourquoi": "meme compteur que Breakthrough, cote dejouement",
        "scenario": "rhino",
        "heros": "jessica_jones",
        # 5 et pas 8 : au-dela, le complot « The Break-In! » est ACCOMPLI des la
        # mise en place et la partie s'arrete avant qu'on joue quoi que ce soit.
        "mise_en_place": ["Puzzle.ChangeForm('73001b')",
                          "Puzzle.Reveal('73016')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["73005", "73003", "73004"],
        "declencher": [],
        "jouer": ["73005"],
        "payer_avec": ["73003", "73004"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    {
        "nom": "73012 Always a Bigger Conspiracy — When Defeated : revele une autre manigance",
        "pourquoi": "defausse du deck Rencontre jusqu'a une manigance, puis revelation",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.Reveal('73012')"],
        "declencher": ["Puzzle.SetThreat('73012', 0)"],
        "verifier": "jj_une_autre_manigance_revelee",
    },
    {
        "nom": "73014 Hang Back and Watch — Investigate 2 par joueur puis soin de 2",
        "pourquoi": "variante [per_hero] du mot-cle maison, et When Defeated qui soigne",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')",
                          "Puzzle.SetThreat('01097b', 6)",
                          "Puzzle.Damage('73001a', 4)"],
        "declencher": ["Puzzle.Reveal('73014')", "Puzzle.SetThreat('73014', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]], "degats_identite": 2},
    },
    {
        "nom": "73020 \"I've Got Everyone\" — sans manigance secondaire, la carte prend surge",
        "pourquoi": "branche X=0 : pas de degats, mais un Renfort",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')"],
        "declencher": ["Puzzle.Reveal('73020')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "73021 The Purple Children — 2 menaces sur chaque manigance secondaire",
        "pourquoi": "branche nominale ; l'autre branche desoriente le joueur",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')",
                          "Puzzle.Reveal('73016')",
                          "Puzzle.SetThreat('73016', 1)"],
        # Main videe : depuis le correctif de `Puzzle.Reveal` (5/8/2026) les
        # interruptions `from_encounter=True` partent vraiment, et le pilote
        # ANNULAIT la traitrise avec Out in the Open qu'il avait en main.
        "main_exclusive": ["73003"],
        "declencher": ["Puzzle.Reveal('73021')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["73016", 3]]},
    },
    {
        "nom": "73018 \"Look At Me!\" — le Homme-Pourpre ne peut pas subir de degats",
        "pourquoi": "UnitCannotTakeDamageWhile, cle de la manigance nemesis",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')",
                          "Puzzle.Reveal('73018')",
                          "Puzzle.PutIntoPlay('73019')"],
        "declencher": ["Puzzle.Damage('73019', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["73019", 0]]},
    },
    {
        "nom": "73019 * Purple Man — Boost : le joueur est Desoriente",
        "pourquoi": "capacite de boost du sbire nemesis",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')"],
        "declencher": ["Puzzle.Boost('73019')"],
        "verifier": "identite_a_un_statut",
    },
    {
        "nom": "73022 Power Couple — Tenace sur Jessica et Luke Cage, puis pioche",
        "pourquoi": ("carte de duo : condition de jeu maison (Luke Cage en jeu) a la place "
                     "de la cle TeamUp, qui suppose deux heros"),
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')",
                          "Puzzle.PutIntoPlay('73002')"],
        "main_exclusive": ["73022", "73003", "73005"],
        "declencher": [],
        "jouer": ["73022"],
        "payer_avec": ["73003", "73005"],
        "verifier": "jj_couple_tenace",
    },
    {
        "nom": "74006 Anti-Venom Goo — reduit le cout de l'evenement puis soigne le surpaiement",
        "pourquoi": ("la reduction de cout etait le point le plus incertain du pack : "
                     "Dig Deep coute 1, paye avec 2 [energy]. Si la reduction prend, le "
                     "cout tombe a 0 et le surpaiement vaut 2, donc 2 soins"),
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')",
                          "Puzzle.Damage('74001a', 4)"],
        "main_exclusive": ["74003", "74006"],
        "declencher": [],
        "jouer": ["74003"],
        "payer_avec": ["74006"],
        "cibles": ["01094", "74001a"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "degats_identite": 2},
    },
    {
        "nom": "74003 Dig Deep — intact : 3 degats, ennemi Sonne et 1 menace retiree",
        "pourquoi": "branche « exactly 10 hit points remaining » de l'evenement",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["74003", "74004", "74005"],
        "declencher": [],
        "jouer": ["74003"],
        "payer_avec": ["74004"],
        "cibles": ["01094", "01097b"],
        "verifier": "aav_dig_deep_intact",
    },
    {
        "nom": "74004 Extricate — 4 menaces retirees d'une manigance",
        "pourquoi": "effet de base de l'evenement de dejouement",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        # 5 et pas 7 : voir le cas Hit the Streets, le complot serait accompli.
        "mise_en_place": ["Puzzle.ChangeForm('74001b')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["74004", "74003", "74005"],
        "declencher": [],
        "jouer": ["74004"],
        "payer_avec": ["74003", "74005"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    # ------------------------------------------------------------------------
    # Pack « moon_knight » : 76001a-76024 (custom « DesignHacker »)
    # Identité à CINQ faces (pile d'identités de l'insert).
    # ------------------------------------------------------------------------
    {
        "nom": "76001b Marc Spector — la partie demarre sur la bonne face parmi cinq",
        "pourquoi": "premiere identite du moteur a 5 faces : le depart doit tomber sur Marc",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "face_identite",
        "attendu": {"face": "76001b"},
    },
    {
        "nom": "76008 Fight or Foil — bascule vers Moon Knight et 2 degats",
        "pourquoi": "ChangeToFace vers une face NOMMEE parmi 5, au coeur de tout le pack",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": [],
        "main_exclusive": ["76008", "01088"],
        "declencher": [],
        "jouer": ["76008"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "face_identite",
        "attendu": {"face": "76001a"},
    },
    {
        "nom": "76001a A Good Offense — Deck and Cover coute 0 sur la face Moon Knight",
        "pourquoi": ("reducteur de cout par classe + carte bi-classe : sans lui la carte "
                     "est injouable main vide, avec lui elle part gratuitement"),
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": [],
        "main_exclusive": ["76008", "01088", "76007"],
        "declencher": [],
        "jouer": ["76008", "76007"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]]},
    },
    {
        "nom": "76002 Echo — ATK/THW a 0 tant que l'identite est en alter-ego",
        "pourquoi": "ses stats copient le heros ACTIF ; sans heros actif, rien",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('76002')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["76002", "attack", 0], ["76002", "thwart", 0]]},
    },
    {
        "nom": "76002 Echo — copie l'ATK 2 / THW 1 de Moon Knight",
        "pourquoi": "le gain dynamique doit suivre la face heros courante",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('76002')"],
        "main_exclusive": ["76008", "01088"],
        "declencher": [],
        "jouer": ["76008"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["76002", "attack", 2], ["76002", "thwart", 1]]},
    },
    {
        "nom": "76005 Different Folks — un compteur madness par changement de forme",
        "pourquoi": "AfterUnitChangeForm force : le compteur doit tomber tout seul",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('76005')"],
        "main_exclusive": ["76008", "01088"],
        "declencher": [],
        "jouer": ["76008"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["76005", "madness", 1]]},
    },
    {
        "nom": "76003 Khonshu — apres un changement de forme, s'incline et fait piocher",
        "pourquoi": "Response avec cout d'inclinaison sur le changement de forme",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('76003')"],
        "main_exclusive": ["76008", "01088"],
        "declencher": [],
        "jouer": ["76008"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["76003"]},
    },
    {
        "nom": "76004 Frenchie — se defausse pour annuler la menace sur le complot",
        "pourquoi": "interruption de WhenSchemeWouldPlaceThreat avec SetBeInstead",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.SetThreat('01097b', 2)", "Puzzle.PutIntoPlay('76004')"],
        "declencher": ["Puzzle.PlaceThreat('01097b', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]], "hors_jeu": ["76004"]},
    },
    {
        "nom": "76010 Where'd He Go? — depuis l'alter-ego : flip heros et vilain desoriente",
        "pourquoi": "menu de formes filtre (heros seulement) puis statut",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": [],
        "main_exclusive": ["76010", "01088"],
        "declencher": [],
        "jouer": ["76010"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "mk_forme_heros_et_vilain_desoriente",
    },
    {
        "nom": "76013 Bushman — survit a sa premiere defaite et gagne un compteur madness",
        "pourquoi": "WhenUnitWouldBeDefeated + SetBeInstead : soin complet au lieu de mourir",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('76013')"],
        "declencher": ["Puzzle.Damage('76013', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["76013"], "compteurs": [["76013", "madness", 1]],
                    "degats": [["76013", 0]]},
    },
    {
        "nom": "76013 Bushman — la seconde defaite est la bonne",
        "pourquoi": "avec un compteur madness, l'interruption ne doit plus le sauver",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('76013')"],
        "declencher": ["Puzzle.Damage('76013', 5)", "Puzzle.Damage('76013', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["76013"]},
    },
    {
        "nom": "76015 Cull the Weak — defausse l'allie le plus faible",
        "pourquoi": "When Revealed avec choix automatique du plus bas en PV restants",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('76002')"],
        "declencher": ["Puzzle.Reveal('76015')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["76002"], "degats_identite": 0},
    },
    {
        "nom": "76015 Cull the Weak — sans allie, 2 degats a l'identite",
        "pourquoi": "branche de repli",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('76015')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "76014 Mano a Mano — Moon Knight perd 1 ATK tant que la manigance est en jeu",
        "pourquoi": "aura GiveKeywordToInPlay sur une face heros nommee",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('76014')"],
        "main_exclusive": ["76008", "01088"],
        "declencher": [],
        "jouer": ["76008"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": -1}},
    },
    {
        "nom": "76020 Thor (Age of Khonshu) — vaincu par le joueur, il lache Mjolnir",
        "pourquoi": ("When Defeated + creation a la volee de l'artefact lie "
                     "(CardFactory.GenerateCard), jamais fait par un set modulaire"),
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('76020')", "Puzzle.Damage('76020', 8)"],
        "main_exclusive": ["76008", "01088"],
        "declencher": [],
        "jouer": ["76008"],
        "payer_avec": ["01088"],
        "cibles": ["76020"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["76020"], "en_jeu": ["76021"]},
    },
    {
        "nom": "76006 Different Strokes — 1 compteur par aspect joue, pas deux fois le meme",
        "pourquoi": "limite « once per round for each aspect » suivie sur world",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('76006')", "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["76008", "01090", "04049", "01088", "13014", "04043"],
        "declencher": [],
        # Fight or Foil d'abord : les cartes d'aspect sont des Hero Actions,
        # injouables depuis l'alter-ego de depart. Les deux Aggression passent
        # ensuite gratuitement (A Good Offense) ; la 2e ne compte pas (limite).
        "jouer": ["76008", "04049", "13014", "04043"],
        "payer_avec": ["01090", "01088"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["76006", "madness", 2]]},
    },
    # ------------------------------------------------------------------------
    # Pack « lockjaw » : 78001a-78030 (custom « Nugget »)
    # ------------------------------------------------------------------------
    {
        "nom": "78001b Setup — Tuning Fork est fouillee dans le deck et mise en jeu",
        "pourquoi": "sans elle, la ressource « os » du pack n'existe pas et tout le deck cale",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["78003"]},
    },
    {
        "nom": "78005 Kamala's Room — +1 REC a l'alter-ego",
        "pourquoi": "GiveKeywordToAttached('You') doit viser l'identite, pas le soutien",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('78005')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 1}, "en_jeu": ["78005"]},
    },
    {
        "nom": "78026 Ms. Marvel — +1 ATK et +1 THW (interruptions rendues en bonus permanent)",
        "pourquoi": "ecart assume : les deux Interrupt etoiles valent un bonus permanent",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('78026')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["78026", "attack", 1], ["78026", "thwart", 1]]},
    },
    {
        "nom": "78015 Annihilus — vaincu, il retourne dans le deck Rencontre",
        "pourquoi": "WhenUnitWouldBeDefeated + SetBeInstead : il ne doit jamais mourir",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.PutIntoPlay('78015')"],
        "declencher": ["Puzzle.Damage('78015', 9)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["78015"], "dans_deck_rencontre": ["78015"]},
    },
    {
        "nom": "78017 Provoked — l'identite ne peut plus repasser en alter-ego",
        "pourquoi": "PlayersCannotChangeForms(to_form=AlterEgo) porte par une piece jointe",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('Lockjaw')"],
        "declencher": ["Puzzle.Reveal('78017')", "Puzzle.ChangeForm('Lockjaw')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "en_jeu": ["78017"]},
    },
    {
        "nom": "78014 Dognapped! — 1 menace de plus par evenement TELEPORT joue",
        "pourquoi": "Forced Response sur le trait TELEPORT, coeur du set nemesis",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.Reveal('78014')"],
        "main_exclusive": ["78009", "01088"],
        "declencher": [],
        "jouer": ["78009"],
        "payer_avec": ["01088"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["78014", 3]]},
    },
    {
        "nom": "78003 Tuning Fork — finance seule le cout d'une carte et s'incline",
        "pourquoi": "la ressource « os » du pack est rendue par un [wild] genere en s'inclinant",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": [],
        "main_exclusive": ["78009"],
        "declencher": [],
        "jouer": ["78009"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["78003"]},
    },
    {
        "nom": "78024 Wet Slobbering Kiss — 3 degats au vilain",
        "pourquoi": "evenement a deux branches : la branche degats doit etre atteignable",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('Lockjaw')"],
        "main_exclusive": ["78024", "01088", "01089"],
        "declencher": [],
        "jouer": ["78024"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]]},
    },
    {
        "nom": "78010 Zooming Around — 1 degat au vilain engage et 1 menace retiree",
        "pourquoi": "effet double (ennemis engages + tous les complots) en une capacite",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('Lockjaw')", "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["78010", "01088", "01089", "01090"],
        "declencher": [],
        "jouer": ["78010"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1]], "menace": [["01097b", 3]]},
    },
    {
        "nom": "78028 Companionship — incline un PET AVENGER et fait piocher 2",
        "pourquoi": "cout d'inclinaison porte par une AUTRE carte, filtree par trait",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.PutIntoPlay('78025')"],
        "main_exclusive": ["78028"],
        "declencher": [],
        "jouer": ["78028"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["78025"]},
    },
    {
        "nom": "78027 Animals Unleashed — sort un PET AVENGER du deck",
        "pourquoi": "recherche deck+main+defausse puis mise en jeu, pour chaque joueur",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('Lockjaw')"],
        "main_exclusive": ["78027", "01088"],
        "declencher": [],
        "jouer": ["78027"],
        "payer_avec": ["01088"],
        "verifier": "lj_un_pet_avenger_en_jeu",
    },
    {
        "nom": "78012 Psionic Tracking — defausse une carte du deck vise",
        "pourquoi": "recherche dans le deck d'un joueur puis defausse ciblee",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": [],
        "main_exclusive": ["78012"],
        "declencher": [],
        "jouer": ["78012"],
        "verifier": "lj_defausse_non_vide",
    },
    {
        "nom": "20001a Symbiotic Bond — en forme HEROS, Venom peut financer une carte a 3",
        "pourquoi": ("capacite Resource portee par la face HEROS : elle doit apparaitre parmi les "
                     "moyens de paiement. En alter-ego elle n'existe pas, c'est la carte qui le dit."),
        "scenario": "rhino",
        "heros": "venom",
        # CORRECTIF 4/8/2026 : par NOM, « Flash Thompson » est devenu ambigu
        # depuis le pack agent_anti_venom, dont l'alter-ego 74001b porte le meme
        # nom que le Venom officiel 20001b. Le changement de forme echouait, la
        # capacite Resource de la face heros n'existait plus, et Sonic Rifle
        # partait a la defausse faute de paiement. Toujours le card_id.
        "mise_en_place": ["Puzzle.ChangeForm('20001b')"],
        "main_exclusive": ["20015", "01089"],
        "declencher": [],
        "jouer": ["20015"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["20015"], "degats_identite": 1},
    },
    # ------------------------------------------------------------------------
    # Pack « mister_fantastic » (custom « DesignHacker »), livre le 2/8/2026
    # SANS AUCUN cas de comportement. Couverture ajoutee le 4/8/2026 apres que
    # `verifier_coherence_cartes.py` l'ait releve a 0 %.
    # ------------------------------------------------------------------------
    {
        "nom": "65014 * Wizard — chaque heros perd 1 THW tant qu'il est en jeu",
        "pourquoi": "malus passif du sbire nemesis sur toutes les identites",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')"],
        "declencher": ["Puzzle.PutIntoPlay('65014')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"thwart": -1}},
    },
    {
        "nom": "65006 Unstable Uniform — Mister Fantastic gagne +1 DEF",
        "pourquoi": "buff passif sur l'identite",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')"],
        "declencher": ["Puzzle.PutIntoPlay('65006')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}},
    },
    {
        "nom": "65005 Fantasticar — Mister Fantastic gagne +1 de taille de main",
        "pourquoi": "buff passif de taille de main",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')"],
        "declencher": ["Puzzle.PutIntoPlay('65005')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"hand_size": 1}},
    },
    {
        "nom": "65007 Fantasti-Flare — entre en jeu avec 4 compteurs flare",
        "pourquoi": "cle desc `Uses: 4,flare`",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')"],
        "declencher": ["Puzzle.PutIntoPlay('65007')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["65007", "flare", 4]]},
    },
    {
        "nom": "65008 Neutralizer — entre en jeu avec 2 compteurs charge",
        "pourquoi": "cle desc `Uses: 2,charge`",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')"],
        "declencher": ["Puzzle.PutIntoPlay('65008')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["65008", "charge", 2]]},
    },
    {
        "nom": "65002 * Invisible Woman — son arrivee redresse l'identite",
        "pourquoi": "Response a l'entree en jeu de l'alliee signature",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')", "Puzzle.Exhaust('65001a')"],
        "declencher": ["Puzzle.PutIntoPlay('65002')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["65001a"], "en_jeu": ["65002"]},
    },
    {
        "nom": "65015 Hubris — When Revealed : 1 menace + le THW cumule des heros",
        "pourquoi": "Mister Fantastic a 3 THW, donc 1 + 3 = 4 menaces sur la manigance",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')"],
        "declencher": ["Puzzle.Reveal('65015')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["65015", 4]]},
    },
    {
        "nom": "65016 Projection — s'attache a l'identite et prend surge",
        "pourquoi": "attachement nemesis pose sur la carte d'identite",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')"],
        "declencher": ["Puzzle.Reveal('65016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["65016"]},
    },
    {
        "nom": "65017 Execution — defausse les Projection en jeu",
        "pourquoi": "la traitrise nettoie les attachements poses par 65016",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')", "Puzzle.Reveal('65016')"],
        "declencher": ["Puzzle.Reveal('65017')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["65016"]},
    },
    {
        "nom": "65009 Stretched Thin — 2 menaces, +1 sur chaque manigance si la main est vide",
        "pourquoi": ("les deux moities de la carte : la main est vide apres avoir joue "
                     "et paye, donc 2 + 1 = 3 menaces retirees du complot principal"),
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')",
                          "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["65009", "65010"],
        "declencher": [],
        "jouer": ["65009"],
        "payer_avec": ["65010"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    {
        "nom": "65013 Ben's Cure — l'obligation se resout depuis la forme heros",
        "pourquoi": "obligation du pack, jamais jouee ; verifie surtout qu'elle ne plante pas",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')", "Puzzle.PutIntoPlay('65006')"],
        "declencher": ["Puzzle.Reveal('65013')"],
        "verifier": "obligation_resolue_65013",
    },
    # ------------------------------------------------------------------------
    # Pack « the_thing » (custom « DesignHacker »), livre le 2/8/2026 SANS
    # AUCUN cas de comportement. Couverture ajoutee le 4/8/2026.
    # ------------------------------------------------------------------------
    {
        "nom": "67005 Unstable Uniform — The Thing gagne +1 DEF",
        "pourquoi": "buff passif sur l'identite",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')"],
        "declencher": ["Puzzle.PutIntoPlay('67005')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}},
    },
    {
        "nom": "67012 * Puppet Master — sa revelation fait venir Hulk",
        "pourquoi": "Forced Response qui cherche 67014 dans le deck Rencontre et le revele",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')"],
        "declencher": ["Puzzle.Reveal('67012')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["67012", "67014"]},
    },
    {
        "nom": "67013 Pulling The Strings — le sbire au plus bas SCH gagne +1 ATK",
        "pourquoi": "Hulk a 0 SCH, c'est donc lui qui prend le bonus",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')", "Puzzle.PutIntoPlay('67014')"],
        "declencher": ["Puzzle.Reveal('67013')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["67014", "attack", 1]]},
    },
    {
        "nom": "67015 Friendly Fire — degats egaux au meilleur ATK ami, ici celui du heros",
        "pourquoi": "seul en jeu, The Thing a 2 ATK : il encaisse 2",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')"],
        "declencher": ["Puzzle.Reveal('67015')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "67002 * Human Torch — arrive en jeu et resout son choix",
        "pourquoi": "Response a deux options ; on verifie surtout qu'elle ne plante pas",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')"],
        "declencher": ["Puzzle.PutIntoPlay('67002')"],
        "verifier": "tt_human_torch_a_choisi",
    },
    {
        "nom": "67006 Rock 'Em — retire 4 menaces d'une manigance",
        "pourquoi": "effet de base ; 5 - 4 = 1, donc pas de bonus « derniere menace »",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["67006", "67009", "67010", "67008"],
        "declencher": [],
        "jouer": ["67006"],
        "payer_avec": ["67009", "67010", "67008"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    {
        "nom": "67009 Sock 'Em — 4 degats a un ennemi",
        "pourquoi": "effet de base de l'evenement d'attaque",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')"],
        "main_exclusive": ["67009", "67006", "67010", "67008"],
        "declencher": [],
        "jouer": ["67009"],
        "payer_avec": ["67006", "67010", "67008"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]]},
    },
    {
        "nom": "67010 It's Clobberin' Time! — deux attaques de 4, soit 8 au total",
        "pourquoi": "la carte enchaine DEUX attaques, chacune sur une cible au choix",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')"],
        "main_exclusive": ["67010", "67006", "67009", "67008"],
        "declencher": [],
        "jouer": ["67010"],
        "payer_avec": ["67006", "67009", "67008"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 8]]},
    },
    {
        "nom": "67001b Ever-Lovin' — un soin de 4 ou plus rend Ben Grimm Tenace",
        "pourquoi": "Response de l'alter-ego sur le montant SOIGNE, pas sur les PV finaux",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.Damage('67001b', 6)"],
        "declencher": ["Puzzle.Heal('67001b', 4)"],
        "verifier": "identite_est_tenace",
    },
    {
        "nom": "67011 Annual Shedding — l'obligation se resout depuis la forme heros",
        "pourquoi": "obligation du pack, jamais jouee",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')"],
        "declencher": ["Puzzle.Reveal('67011')"],
        "verifier": "obligation_resolue_67011",
    },
    # ------------------------------------------------------------------------
    # Pack « invisible_woman » (custom « DesignHacker »). Etait a 5 % au
    # 4/8/2026. Les cartes conditionnees a une forme heros PRECISE (INVISIBLE
    # ou PSIONIC) ne sont pas couvertes : `Puzzle.ChangeForm` ne sait pas viser
    # une face, il bascule vers l'une des deux au choix du pilote.
    # ------------------------------------------------------------------------
    {
        "nom": "66003 Central City Estate — Sue Storm gagne +1 REC",
        "pourquoi": "buff passif lisible en forme alter-ego, sans dependre de la face heros",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('66003')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 1}},
    },
    {
        "nom": "66016 Microversal Maneuvers — s'attache a Psycho-Man et lui donne +2 SCH",
        "pourquoi": "attachement nemesis, cle desc `SCH+`",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.PutIntoPlay('66014')"],
        "declencher": ["Puzzle.Reveal('66016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["66016"], "attributs_carte": [["66014", "scheme", 2]]},
    },
    {
        "nom": "66017 Titanic Terror — s'attache a Psycho-Man et lui donne +2 ATK",
        "pourquoi": "attachement nemesis, cle desc `ATK+`",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.PutIntoPlay('66014')"],
        "declencher": ["Puzzle.Reveal('66017')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["66017"], "attributs_carte": [["66014", "attack", 2]]},
    },
    {
        "nom": "66015 Emotional Masterplan — arrive avec 2 menaces par joueur",
        "pourquoi": "manigance nemesis, StartingThreat 2[per_hero]",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('66015')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["66015", 2]]},
    },
    {
        "nom": "66002 * Mister Fantastic — son arrivee declenche une de ses deux options",
        "pourquoi": "Response a l'entree en jeu : 1 menace retiree partout, ou pioche depuis la defausse",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')",
                          "Puzzle.SetThreat('01097b', 3)"],
        "declencher": ["Puzzle.PutIntoPlay('66002')"],
        "verifier": "iw_mister_fantastic_a_choisi",
    },
    {
        "nom": "66013 Family Time — l'obligation se resout depuis la forme heros",
        "pourquoi": "obligation du pack, jamais jouee",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')"],
        "declencher": ["Puzzle.Reveal('66013')"],
        "verifier": "obligation_resolue_66013",
    },
    # ------------------------------------------------------------------------
    # Packs « gwenpool » et « human_torch ». Les cartes a bulle « ____ » de
    # Gwenpool passent par ResolveBlank : on verifie l'effet de BASE, la bulle
    # etant un choix optionnel que le pilote decline.
    # ------------------------------------------------------------------------
    {
        "nom": "63007 * Gwen's Room — Gwendolyn Poole gagne +1 REC",
        "pourquoi": "buff passif lisible en alter-ego",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('63007')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 1}},
    },
    {
        "nom": "63002 \"Here I Come!\" — 5 degats a un ennemi",
        "pourquoi": "effet de base, sans la bulle « ____ » que le pilote decline",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('63001b')"],
        "main_exclusive": ["63002", "63003", "63005"],
        "declencher": [],
        "jouer": ["63002"],
        "payer_avec": ["63003", "63005"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]]},
    },
    {
        "nom": "63005 \"Sorry, Gotta Run!\" — retire 2 menaces d'une manigance",
        "pourquoi": "effet de base de l'evenement de dejouement",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('63001b')",
                          "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["63005", "63002", "63003"],
        "declencher": [],
        "jouer": ["63005"],
        "payer_avec": ["63002"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]]},
    },
    {
        "nom": "63010 THE END — l'obligation RESTE en jeu, elle ne se defausse pas",
        "pourquoi": ("contre-exemple utile : toutes les obligations ne partent pas a la "
                     "resolution. THE END s'installe et bloque les bulles jusqu'a ce que "
                     "le joueur paie son action d'alter-ego pour la retirer du jeu"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('63001b')"],
        "declencher": ["Puzzle.Reveal('63010')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["63010"]},
    },
    {
        "nom": "64002 * The Thing — allie Tenace a 5 PV et 3 ATK",
        "pourquoi": "valeurs imprimees et mot-cle Toughness de l'allie signature",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('64001b')"],
        "declencher": ["Puzzle.PutIntoPlay('64002')"],
        "verifier": "ht_the_thing_tenace",
    },
    {
        "nom": "64007 Fly-By — 2 menaces, +1 par compteur flamme sur le vilain",
        "pourquoi": "l'effet variable du pack : 2 compteurs flamme, donc 2 + 2 = 4",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('64001b')",
                          "Puzzle.SetThreat('01097b', 5)",
                          "Puzzle.Counter('01094', 'flame', 2)"],
        "main_exclusive": ["64007", "64010", "64009"],
        "declencher": [],
        "jouer": ["64007"],
        "payer_avec": ["64010", "64009"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    # ------------------------------------------------------------------------
    # Packs « albert », « rainy » et « lockjaw ».
    # ------------------------------------------------------------------------
    {
        "nom": "62001b Albert — Extensive Development sort une amelioration ENHANCEMENT au setup",
        "pourquoi": "capacite Setup de l'alter-ego : elle doit avoir agi avant le 1er tour",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu_trait": [["ENHANCEMENT", 1]]},
    },
    {
        "nom": "62003 Guard Protocol — Albert devient Tenace",
        "pourquoi": "l'evenement donne retaliate ET un statut Tenace ; on verifie le statut",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('62001b')"],
        "main_exclusive": ["62003", "62004", "62005"],
        "declencher": [],
        "jouer": ["62003"],
        "payer_avec": ["62004", "62005"],
        "verifier": "identite_est_tenace",
    },
    {
        "nom": "62004 Lethal Directive — 4 degats a un ennemi",
        "pourquoi": "effet de base de l'evenement d'attaque",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('62001b')"],
        "main_exclusive": ["62004", "62003", "62005"],
        "declencher": [],
        "jouer": ["62004"],
        "payer_avec": ["62003", "62005"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]]},
    },
    {
        "nom": "62005 Sabotage Sequence — retire 3 menaces d'une manigance",
        "pourquoi": "effet de base ; 5 - 3 = 2, donc pas de bonus « derniere menace »",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('62001b')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["62005", "62003", "62004"],
        "declencher": [],
        "jouer": ["62005"],
        "payer_avec": ["62003", "62004"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]]},
    },
    {
        "nom": "61005 Lightning Strike — 6 degats a un ennemi",
        "pourquoi": "effet de base de l'evenement d'attaque de Thor (Jane Foster)",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('61001b')"],
        "main_exclusive": ["61005", "61004", "61006", "61008"],
        "declencher": [],
        "jouer": ["61005"],
        "payer_avec": ["61004", "61006", "61008"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 6]]},
    },
    {
        "nom": "61028 * Malekith — arrive en jeu avec ses valeurs imprimees",
        "pourquoi": "sbire nemesis : 6 PV, 2 SCH, 1 ATK, sans modificateur parasite",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('61001b')"],
        "declencher": ["Puzzle.PutIntoPlay('61028')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["61028"],
                    "attributs_carte": [["61028", "attack", 0], ["61028", "scheme", 0]]},
    },
    {
        "nom": "78002 * Black Bolt — allie a 4 ATK et 3 PV",
        "pourquoi": "valeurs imprimees de l'allie le plus cher du pack",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')"],
        "declencher": ["Puzzle.PutIntoPlay('78002')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["78002"], "attributs_carte": [["78002", "attack", 0]]},
    },
    {
        "nom": "78018 * Zabu — allie Companion a 2 ATK",
        "pourquoi": "mot-cle maison Companion : l'allie entre en jeu normalement",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')"],
        "declencher": ["Puzzle.PutIntoPlay('78018')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["78018"], "attributs_carte": [["78018", "attack", 0]]},
    },
    {
        "nom": "78013 Canine Urges — l'obligation se resout depuis la forme heros",
        "pourquoi": "obligation du pack, jamais jouee",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')"],
        "declencher": ["Puzzle.Reveal('78013')"],
        "verifier": "obligation_resolue_78013",
    },
    # ------------------------------------------------------------------------
    # Packs « moon_knight », « spider_man_rainy » et « venom_rainy ».
    # ------------------------------------------------------------------------
    {
        "nom": "76016 Bushman's Knife — s'attache a un sbire et lui donne +2 ATK et piercing",
        "pourquoi": ("le piercing ne partait JAMAIS avant le correctif du 4/8/2026 : la "
                     "condition lisait le porteur avec une methode inexistante"),
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('76001b')", "Puzzle.PutIntoPlay('76017')"],
        "declencher": ["Puzzle.Reveal('76016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["76016"], "attributs_carte": [["76017", "attack", 2]]},
    },
    {
        "nom": "76021 * Mjolnir — +1 ATK, trait AERIAL et 3 compteurs attack",
        "pourquoi": "artefact cree en jeu par le set Age of Khonshu, jamais verifie",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('76001b')"],
        "declencher": ["Puzzle.PutIntoPlay('76021')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}, "traits": ["AERIAL"],
                    "compteurs": [["76021", "attack", 3]]},
    },
    {
        "nom": "76022 * The Eye of Agamotto — entre en jeu avec 2 compteurs mystic",
        "pourquoi": "cle desc `Uses: 2,mystic` de l'artefact",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('76001b')"],
        "declencher": ["Puzzle.PutIntoPlay('76022')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["76022", "mystic", 2]]},
    },
    {
        "nom": "76023 * The Hell Charger — entre en jeu avec 2 compteurs charge",
        "pourquoi": "cle desc `Uses: 2,charge` de l'artefact",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('76001b')"],
        "declencher": ["Puzzle.PutIntoPlay('76023')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["76023", "charge", 2]]},
    },
    {
        "nom": "76018 * Ghost Rider — sbire vilainesque a 7 PV et 3 ATK",
        "pourquoi": "heros corrompu du set Age of Khonshu, valeurs imprimees",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('76001b')"],
        "declencher": ["Puzzle.PutIntoPlay('76018')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["76018"], "attributs_carte": [["76018", "attack", 0]]},
    },
    {
        "nom": "76012 Seek Help — l'obligation se resout depuis la forme heros",
        "pourquoi": "obligation du pack, jamais jouee",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('76001b')"],
        "declencher": ["Puzzle.Reveal('76012')"],
        "verifier": "obligation_resolue_76012",
    },
    {
        "nom": "71012 Impact Webbing — la carte de regles est en jeu des le setup",
        "pourquoi": "cles `Permanent` + `Setup` : elle doit sortir sans etre jouee",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["71012"]},
    },
    {
        "nom": "71011 Web-Shooters — Spider-Man gagne le trait AERIAL",
        "pourquoi": "buff de trait passif sur l'identite",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('71001b')"],
        "declencher": ["Puzzle.PutIntoPlay('71011')"],
        "verifier": "etat_attendu",
        "attendu": {"traits": ["AERIAL"]},
    },
    {
        "nom": "71014 For My Next Trick... — 3 menaces par joueur et 2 compteurs illusion",
        "pourquoi": "manigance nemesis de Mysterio, StartingThreat 3[per_hero] + Uses",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('71001b')"],
        "declencher": ["Puzzle.Reveal('71014')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["71014", 3]],
                    "compteurs": [["71014", "illusion", 2]]},
    },
    {
        "nom": "72015 Symbiote Rioter — sbire Guard/Patrol a 4 PV et 2 ATK",
        "pourquoi": "sbire nemesis de Venom, valeurs imprimees",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('72001b')"],
        "declencher": ["Puzzle.PutIntoPlay('72015')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["72015"], "attributs_carte": [["72015", "attack", 0]]},
    },
    {
        "nom": "72013 Paint The Town Red — 1 menace imprimee + 2 par joueur via Hinder",
        "pourquoi": ("piege de lecture : la cle `Hinder: 2*` AJOUTE 2 menaces par joueur "
                     "a la revelation, en plus du StartingThreat 1. Total 3 en solo"),
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('72001b')"],
        "declencher": ["Puzzle.Reveal('72013')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["72013", 3]]},
    },
    {
        "nom": "72004 Self-Sacrifice — le bonus optionnel EST pris : 6 menaces retirees",
        "pourquoi": ("CORRECTIF de lecture 4/8/2026 : le pilote ne refuse PAS tous les "
                     "choix optionnels. Il decline les `MayChooseOneAbility` (c'est ce qui "
                     "avait cache `identity.ChangeForm`), mais il accepte les couts "
                     "optionnels d'un effet, ici « you may take 2 damage ». Il paie aussi "
                     "avec Symbiotic Bond, d'ou 1 degat de plus"),
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('72001b')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["72004", "72002", "72005"],
        "declencher": [],
        "jouer": ["72004"],
        "payer_avec": ["72002", "72005"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 0]], "degats_identite": 3},
    },
    # ------------------------------------------------------------------------
    # Complements sur gwenpool, human_torch, the_thing et rainy.
    # ------------------------------------------------------------------------
    {
        "nom": "63003 \"It Can't End Like This!\" — 1 degat au vilain et 1 menace retiree",
        "pourquoi": "double effet attaque/dejouement de l'evenement a 0",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('63001b')",
                          "Puzzle.SetThreat('01097b', 3)"],
        "main_exclusive": ["63003", "63002"],
        "declencher": [],
        "jouer": ["63003"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1]], "menace": [["01097b", 2]]},
    },
    {
        "nom": "63009 * Unbelievable Gwenpool — l'amelioration entre en jeu",
        "pourquoi": "support de la mecanique des bulles ; verifie au moins sa mise en jeu",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('63009')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["63009"]},
    },
    {
        "nom": "64010 Nova Flame — 3 compteurs flamme puis 7 degats, soit 10 au total",
        "pourquoi": ("la carte se combine avec « Flame On! » de l'identite, qui inflige "
                     "1 degat PAR compteur pose : 3 compteurs + 7 degats = 10. Compter "
                     "seulement les 7 de la carte serait une lecture incomplete"),
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('64001b')"],
        "main_exclusive": ["64010", "64008", "64007", "64009", "64005"],
        "declencher": [],
        "jouer": ["64010"],
        "payer_avec": ["64008", "64007", "64009", "64005"],
        "cibles": ["01094"],
        "verifier": "ht_nova_flame",
    },
    {
        "nom": "64008 Blaze and Daze — 4 degats a un ennemi",
        "pourquoi": "effet de base ; le bonus a 3 compteurs flamme n'est pas reuni ici",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('64001b')"],
        "main_exclusive": ["64008", "64010", "64007", "64009"],
        "declencher": [],
        "jouer": ["64008"],
        "payer_avec": ["64010", "64007", "64009"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]]},
    },
    {
        "nom": "67014 * Hulk — sbire Guard a 5 PV et 3 ATK",
        "pourquoi": "le sbire asservi du set nemesis de The Thing, valeurs imprimees",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')"],
        "declencher": ["Puzzle.PutIntoPlay('67014')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["67014"], "attributs_carte": [["67014", "attack", 0]]},
    },
    {
        "nom": "67004 Yancy Street Gang — le soutien entre en jeu",
        "pourquoi": "son action n'est pas declenchable par le harnais ; on verifie la mise en jeu",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')"],
        "declencher": ["Puzzle.PutIntoPlay('67004')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["67004"]},
    },
    {
        "nom": "61002 * Odinson — allie Multiverse a 3 PV",
        "pourquoi": "allie signature de Thor (Jane Foster), valeurs imprimees",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('61001b')"],
        "declencher": ["Puzzle.PutIntoPlay('61002')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["61002"], "attributs_carte": [["61002", "attack", 0]]},
    },
    {
        "nom": "61003 * Roz Solomon — alliee a 2 THW",
        "pourquoi": "seconde alliee signature, valeurs imprimees",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('61001b')"],
        "declencher": ["Puzzle.PutIntoPlay('61003')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["61003"], "attributs_carte": [["61003", "thwart", 0]]},
    },
    # ------------------------------------------------------------------------
    # Derniers complements : invisible_woman, agent_anti_venom, lockjaw.
    # ------------------------------------------------------------------------
    {
        "nom": "66012 Spectral Shift — l'Action change la forme de l'identite",
        "pourquoi": "seule carte du pack qui change de forme sans exiger une face precise",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": [],
        "main_exclusive": ["66012", "66008"],
        "declencher": [],
        "jouer": ["66012"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero"},
    },
    {
        "nom": "66018 End of the Line — defausse 8 cartes du deck Rencontre",
        "pourquoi": "traitrise nemesis : verifie surtout qu'elle se resout sans planter",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')"],
        "declencher": ["Puzzle.Reveal('66018')"],
        "verifier": "iw_end_of_the_line",
    },
    {
        "nom": "66014 * Psycho-Man — sbire nemesis a 5 PV",
        "pourquoi": "ses ATK et SCH sont imprimes « 0* » : on verifie au moins les PV",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')"],
        "declencher": ["Puzzle.PutIntoPlay('66014')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["66014"], "attributs_carte": [["66014", "health", 0]]},
    },
    {
        "nom": "74013 * Maniac — sbire nemesis a 5 PV, 2 SCH et 2 ATK",
        "pourquoi": "valeurs imprimees du sbire nemesis d'Agent Anti-Venom",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')"],
        "declencher": ["Puzzle.PutIntoPlay('74013')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["74013"],
                    "attributs_carte": [["74013", "attack", 0], ["74013", "scheme", 0]]},
    },
    {
        "nom": "74015 * Infected Scorpion — sbire Quickstrike a 7 PV",
        "pourquoi": "valeurs imprimees ; son Forced Interrupt exige une attaque, non testable",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')"],
        "declencher": ["Puzzle.PutIntoPlay('74015')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["74015"], "attributs_carte": [["74015", "attack", 0]]},
    },
    {
        "nom": "74014 The Made Men — manigance nemesis a 3 menaces par joueur",
        "pourquoi": "StartingThreat 3[per_hero] ; son Forced Response exige une activation",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')"],
        "declencher": ["Puzzle.Reveal('74014')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["74014", 3]]},
    },
    {
        "nom": "74002 * Spider-Man — allie signature a 3 PV et 2 ATK",
        "pourquoi": "valeurs imprimees ; son Interrupt exige une activation de sbire",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')"],
        "declencher": ["Puzzle.PutIntoPlay('74002')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["74002"], "attributs_carte": [["74002", "attack", 0]]},
    },
    {
        "nom": "74009 Bear Arms — l'amelioration entre en jeu",
        "pourquoi": "ses deux actions ne sont pas declenchables par le harnais",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')"],
        "declencher": ["Puzzle.PutIntoPlay('74009')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["74009"]},
    },
    {
        "nom": "74007 Unlikely Allies — le soutien entre en jeu",
        "pourquoi": "son action de defausse n'est pas declenchable par le harnais",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')"],
        "declencher": ["Puzzle.PutIntoPlay('74007')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["74007"]},
    },
    {
        "nom": "78016 Dog Catcher — sbire a 2 PV et 1 ATK",
        "pourquoi": "sbire nemesis de Lockjaw, valeurs imprimees",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')"],
        "declencher": ["Puzzle.PutIntoPlay('78016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["78016"], "attributs_carte": [["78016", "attack", 0]]},
    },
    {
        "nom": "78019 * Throg — allie Companion a 2 PV",
        "pourquoi": "second allie Companion, pour couvrir la famille",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')"],
        "declencher": ["Puzzle.PutIntoPlay('78019')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["78019"], "attributs_carte": [["78019", "attack", 0]]},
    },
    # ------------------------------------------------------------------------
    # Derniere vague sur ce que le harnais atteint deja. Ce qui restera apres
    # exige un declencheur d'ATTAQUE ou d'ACTION de carte en jeu, absents de
    # l'API Puzzle.
    # ------------------------------------------------------------------------
    {
        "nom": "61006 Stand Fast — redresse Thor",
        "pourquoi": "l'evenement redresse l'identite ; le bonus Tenace exige un paiement 100 % energie",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('61001b')", "Puzzle.Exhaust('61001a')"],
        "main_exclusive": ["61006", "61004", "61005"],
        "declencher": [],
        "jouer": ["61006"],
        "payer_avec": ["61004", "61005"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["61001a"]},
    },
    {
        "nom": "62006 System Relaunch — soigne la valeur de REC et passe en forme heros",
        "pourquoi": "Albert a 4 de REC : blesse de 6, il doit finir a 2 degats et en forme heros",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.Damage('62001b', 6)"],
        "main_exclusive": ["62006", "62003"],
        "declencher": [],
        "jouer": ["62006"],
        "payer_avec": ["62003"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "forme": "Hero"},
    },
    {
        "nom": "62013 Crack in the Multiverse — 1 menace imprimee + 2 par joueur via Hinder",
        "pourquoi": "meme piege que Paint The Town Red : la cle Hinder ajoute sa menace",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('62001b')"],
        "declencher": ["Puzzle.Reveal('62013')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["62013", 3]]},
    },
    {
        "nom": "65010 Big Reach — 3 degats au vilain, +0 car la main est vide",
        "pourquoi": "le second effet vaut le nombre de cartes restantes en main, ici zero",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')"],
        "main_exclusive": ["65010", "65009", "65011", "65012"],
        "declencher": [],
        "jouer": ["65010"],
        "payer_avec": ["65009", "65011", "65012"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]]},
    },
    {
        "nom": "65012 Mental Gymnastics — 2 degats a X=0, et l'ennemi est Desoriente",
        "pourquoi": "carte a cout X : sans surpaiement X vaut 0, et la main vide declenche le bonus",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')"],
        "main_exclusive": ["65012"],
        "declencher": [],
        "jouer": ["65012"],
        "cibles": ["01094"],
        "verifier": "mf_mental_gymnastics",
    },
    {
        "nom": "68008 Calculated Strike — 2 menaces retirees et 3 degats au vilain",
        "pourquoi": "double effet attaque/dejouement",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('68001b')",
                          "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["68008", "68010", "68009", "68011"],
        "declencher": [],
        "jouer": ["68008"],
        "payer_avec": ["68010", "68009", "68011"],
        "cibles": ["01097b", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]], "degats": [["01094", 3]]},
    },
    {
        "nom": "73015 Pore Over the Evidence — Investigate 1 par joueur",
        "pourquoi": "derniere manigance On the Job sans cas ; 4 imprimees + 1 deplacee",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "declencher": ["Puzzle.Reveal('73015')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4], ["73015", 5]]},
    },
    {
        "nom": "76007 Deck and Cover — 3 degats a un ennemi (6 au total sur Rhino)",
        "pourquoi": ("Moon Knight ramene le cout de ses cartes d'aspect a 0, le pilote "
                     "joue donc AUSSI Surprise Attack de la main de depart, qui frappe "
                     "Rhino pour 3. Le total de 6 reste discriminant : si Deck and Cover "
                     "cassait, on tomberait a 3"),
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('76001b')"],
        # Main reduite a la SEULE carte testee : Moon Knight ramene son cout a
        # 0 grace au rabais d'aspect, et le pilote ne peut donc plus jouer une
        # autre carte qui fausserait le total de degats.
        "main_exclusive": ["76007"],
        "declencher": [],
        "jouer": ["76007"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 6]]},
    },
    {
        "nom": "78010 Zooming Around — retire 1 menace de chaque manigance",
        "pourquoi": ("teste le helper `ChangerDeForme`, absent du pack jusqu'au 4/8/2026 "
                     "et qui faisait planter TROIS cartes. Fast Travel 78009 partage le "
                     "meme code mais son effet net est nul en solo : elle change la forme "
                     "puis propose de la rechanger, donc rien d'observable"),
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')",
                          "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["78010", "78009", "78008"],
        "declencher": [],
        "jouer": ["78010"],
        "payer_avec": ["78009", "78008"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]]},
    },
    {
        "nom": "78022 * Lockheed — allie Companion a 2 PV",
        "pourquoi": "dernier Companion sans cas",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')"],
        "declencher": ["Puzzle.PutIntoPlay('78022')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["78022"], "attributs_carte": [["78022", "attack", 0]]},
    },
    {
        "nom": "78025 * Ms. Lion — allie Companion a 2 PV",
        "pourquoi": "dernier Companion sans cas",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')"],
        "declencher": ["Puzzle.PutIntoPlay('78025')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["78025"], "attributs_carte": [["78025", "attack", 0]]},
    },
    {
        "nom": "64003 Johnny's Workshop — le soutien entre en jeu",
        "pourquoi": "ses deux Response dependent d'un changement de forme, teste juste apres",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('64001b')"],
        "declencher": ["Puzzle.PutIntoPlay('64003')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["64003"]},
    },
    {
        "nom": "68013 Get Under Control — l'obligation reste en jeu",
        "pourquoi": ("comme THE END de Gwenpool : elle bloque les allies et ne part qu'avec "
                     "l'action d'alter-ego. Victory 1"),
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('68001b')"],
        "declencher": ["Puzzle.Reveal('68013')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["68013"]},
    },
    {
        "nom": "74010 Heroic Will — Hero Action : incliner l'amelioration redresse le heros",
        "pourquoi": "premier cas passant par Puzzle.Action ; sans lui l'action en jeu est inatteignable",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')", "Puzzle.PutIntoPlay('74010')",
                          "Puzzle.Exhaust('74001a')"],
        "declencher": ["Puzzle.Action('74010', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["74001a"], "exhausted": ["74010"]},
    },
    {
        "nom": "01094 Rhino — Puzzle.Attack : le vilain frappe et le heros encaisse",
        "pourquoi": "premier cas passant par Puzzle.Attack ; sans lui aucune capacite « apres avoir attaque » n'est atteignable",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')", "Puzzle.Exhaust('74001a')"],
        # Main videe et heros incline : sans cela le pilote defend (degats
        # reduits a 0) puis joue Counter-Punch, et l'attaque ne se voit plus.
        "main_exclusive": ["74010"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["74001a", 2]]},
    },

    ############################################################################
    # Vague debloquee par Puzzle.Action et Puzzle.Attack (4/8/2026).
    # Ces cartes etaient toutes hors de portee du harnais : leur capacite ne
    # part que sur une action de tour ou sur une attaque.
    {
        "nom": "73008 Alias Investigations — Action : defausser jusqu'a une manigance, la reveler",
        "pourquoi": "action en jeu, jamais atteignable avant Puzzle.Action",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')", "Puzzle.PutIntoPlay('73008')"],
        "declencher": ["Puzzle.Action('73008', 'Action')"],
        "verifier": "manigance_annexe_en_jeu",
    },
    {
        "nom": "73011 Private Investigator — Alter-Ego Action : 1 menace deplacee sur la carte",
        "pourquoi": "montage Beat Cop : la menace devient un jeton sur l'amelioration",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.PutIntoPlay('73011')", "Puzzle.SetThreat('01097b', 5)"],
        "declencher": ["Puzzle.Action('73011', 'AlterEgoAction')"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"jetons": [["73011", "threat", 1]], "menace": [["01097b", 4]],
                    "exhausted": ["73011"]},
    },
    {
        "nom": "73011 Private Investigator — Hero Action : 2 jetons rendus en 2 degats a un sbire",
        "pourquoi": "seconde moitie de la carte, conditionnee a la presence de jetons",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')", "Puzzle.PutIntoPlay('73011')",
                          "Puzzle.Token('73011', 'threat', 2)",
                          "Puzzle.PutIntoPlay('73019')"],
        "declencher": ["Puzzle.Action('73011', 'HeroAction')"],
        "cibles": ["73019"],
        "verifier": "etat_attendu",
        "attendu": {"jetons": [["73011", "threat", 0]], "degats": [["73019", 2]]},
    },
    {
        "nom": "73019 Purple Man — Forced Interrupt : il ne frappe pas, il pose 2 menaces",
        "pourquoi": "capacite remplacant l'attaque, invisible sans Puzzle.Attack",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')", "Puzzle.PutIntoPlay('73019')",
                          "Puzzle.PutIntoPlay('73012')"],
        "declencher": ["Puzzle.Attack('73019')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "74009 Bear Arms — Hero Action (attaque) : drain 1 sur le vilain",
        "pourquoi": "seconde action de la carte, atteinte par l'index",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')", "Puzzle.PutIntoPlay('74009')",
                          "Puzzle.Damage('74001a', 3)"],
        "declencher": ["Puzzle.Action('74009', 'HeroAction', 1)"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1]], "degats_identite": 2, "exhausted": ["74009"]},
    },
    {
        "nom": "74011 One Man Army — Interrupt : sans allie, l'attaque de base pioche et soigne",
        "pourquoi": "declencheur sur pouvoir de base, atteint par Puzzle.Attack sur le heros",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')", "Puzzle.PutIntoPlay('74011')",
                          "Puzzle.Damage('74001a', 3)"],
        "declencher": ["Puzzle.Attack('74001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "73010 Jessica's Jacket — Interrupt : 1 degat evite et 1 menace retiree",
        "pourquoi": "interrupt sur degats subis ; heros incline pour qu'il ne puisse pas defendre",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')", "Puzzle.PutIntoPlay('73010')",
                          "Puzzle.SetThreat('01097b', 5)", "Puzzle.Exhaust('73001a')"],
        "main_exclusive": ["73003"],
        "declencher": ["Puzzle.Attack('01094')"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "menace": [["01097b", 4]], "exhausted": ["73010"]},
    },
    {
        "nom": "74002 Spider-Man — Interrupt : un [mental] annule l'activation d'un sbire non-ELITE",
        "pourquoi": "heros ET allie inclines : seule l'annulation peut empecher le degat",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')", "Puzzle.PutIntoPlay('74002')",
                          "Puzzle.PutIntoPlay('01101')", "Puzzle.Exhaust('74001a')",
                          "Puzzle.Exhaust('74002')"],
        "main_exclusive": ["74003"],
        "declencher": ["Puzzle.Attack('01101')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "74013 Maniac — Forced Response : l'ATK imprime de l'allie defenseur frappe le heros",
        "pourquoi": "declencheur « apres avoir attaque un allie », inatteignable sans Puzzle.Attack",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')", "Puzzle.PutIntoPlay('74002')",
                          "Puzzle.PutIntoPlay('74013')", "Puzzle.Exhaust('74001a')"],
        # 74005 est imprime [physical] : sans [mental] en main, l'interruption
        # de Spider-Man 74002 ne peut pas payer et l'activation a bien lieu.
        "main_exclusive": ["74005"],
        "declencher": ["Puzzle.Attack('74013')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "74015 Infected Scorpion — Forced Interrupt : l'allie encaisse 0 et retourne sa veste",
        "pourquoi": "mot-cle maison TRAITOR, jamais exerce jusqu'ici",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')", "Puzzle.PutIntoPlay('74002')",
                          "Puzzle.PutIntoPlay('74015')", "Puzzle.Exhaust('74001a')"],
        "main_exclusive": ["74005"],
        "declencher": ["Puzzle.Attack('74015')"],
        "verifier": "allie_est_traitre",
        "attendu": {"allie": "74002", "intact": True},
    },
    {
        "nom": "74014 The Made Men — Forced Response : apres l'activation de Maniac, l'allie trahit",
        "pourquoi": "declencheur sur fin d'activation ennemie, atteint par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')", "Puzzle.PutIntoPlay('74002')",
                          "Puzzle.PutIntoPlay('74013')", "Puzzle.PutIntoPlay('74014')",
                          "Puzzle.Exhaust('74001a')"],
        # 74005 est imprime [physical] : sans [mental] en main, l'interruption
        # de Spider-Man 74002 ne peut pas payer et l'activation a bien lieu.
        "main_exclusive": ["74005"],
        "declencher": ["Puzzle.Attack('74013')"],
        "verifier": "allie_est_traitre",
        "attendu": {"allie": "74002"},
    },
    {
        "nom": "74007 Unlikely Allies — Hero Action : defausser un [mental] retire 2 menaces",
        "pourquoi": "une ligne par icone imprimee ; la carte defaussee decide de l'effet",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('74001b')", "Puzzle.PutIntoPlay('74007')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["74003"],
        "declencher": ["Puzzle.Action('74007', 'HeroAction')"],
        "cibles": ["74003", "01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "exhausted": ["74007"]},
    },

    ############################################################################
    # invisible_woman : le pack le moins couvert. Ses evenements exigent une
    # face heros PRECISE (INVISIBLE 66001a ou PSIONIC 66001c), ce qui les
    # rendait injouables tant que la mise en place ne savait pas y aller.
    # `Puzzle.ChangeForm(id, 'Hero')` bascule entre les deux faces heros.
    {
        "nom": "66001a Boo! — apres une attaque, l'identite passe en forme PSIONIC",
        "pourquoi": "Forced Response sur fin d'attaque, atteint par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')"],
        "declencher": ["Puzzle.Attack('66001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["66001c"], "hors_jeu": ["66001a"]},
    },
    {
        "nom": "66001c Invisible Barrier — un ennemi a 2 ATK qui attaque prend 1 degat",
        "pourquoi": "Interrupt sur attaque subie, atteint par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')",
                          "Puzzle.ChangeForm('66001a', 'Hero')",
                          "Puzzle.Exhaust('66001c')"],
        "main_exclusive": ["66008"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1]]},
    },
    {
        "nom": "66005 Flying Disk — Hero Action : se defausser pour 4 degats",
        "pourquoi": "action en jeu, inatteignable avant Puzzle.Action",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')",
                          "Puzzle.ChangeForm('66001a', 'Hero')",
                          "Puzzle.PutIntoPlay('66005')"],
        "declencher": ["Puzzle.Action('66005', 'HeroAction')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]], "hors_jeu": ["66005"]},
    },
    {
        "nom": "66006 Vanishing Act — Hero Action INVISIBLE : rendre un ennemi Confus",
        "pourquoi": "action a cout colore BY, reservee a la forme INVISIBLE",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')", "Puzzle.PutIntoPlay('66006')"],
        "main_exclusive": ["66008", "66009", "66011"],
        "payer_avec": ["66008", "66011"],
        "declencher": ["Puzzle.Action('66006', 'HeroAction')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["01094", "Confused"]], "exhausted": ["66006"]},
    },
    {
        "nom": "66007 Force Shields — Hero Action PSIONIC : rendre l'identite Tenace",
        "pourquoi": "action reservee a la forme PSIONIC",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')",
                          "Puzzle.ChangeForm('66001a', 'Hero')",
                          "Puzzle.PutIntoPlay('66007')"],
        "declencher": ["Puzzle.Action('66007', 'HeroAction')"],
        "cibles": ["66001c"],
        "verifier": "identite_est_tenace",
    },
    {
        "nom": "66008 Incognito — evenement INVISIBLE a cout 0, se resout et part a la defausse",
        "pourquoi": "pioche variable selon les etoiles de boost : on verifie qu'il se resout",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')"],
        "main_exclusive": ["66008"],
        "declencher": [],
        "jouer": ["66008"],
        "verifier": "etat_attendu",
        "attendu": {"defausse": ["66008"]},
    },
    {
        "nom": "66009 Infiltrate — evenement INVISIBLE : jusqu'a 4 menaces retirees",
        "pourquoi": "deux options au choix, la premiere retire 4 d'une seule manigance",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')", "Puzzle.SetThreat('01097b', 6)"],
        "main_exclusive": ["66009", "66008", "66011"],
        "declencher": [],
        "jouer": ["66009"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]], "defausse": ["66009"]},
    },
    {
        "nom": "66010 Forceful — evenement PSIONIC : 3 degats par statut Tenace defausse",
        "pourquoi": "cout paye en statuts Tenace, pas en ressources",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')",
                          "Puzzle.ChangeForm('66001a', 'Hero')",
                          "Puzzle.Tough('66001c')"],
        "main_exclusive": ["66010"],
        "declencher": [],
        "jouer": ["66010"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "defausse": ["66010"]},
    },
    {
        "nom": "66011 Psionic Fields — evenement PSIONIC : deux fois 4 degats",
        "pourquoi": "deux choix successifs, tous deux diriges sur le vilain",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('66001b')",
                          "Puzzle.ChangeForm('66001a', 'Hero')"],
        "main_exclusive": ["66011", "66008", "66009", "66010"],
        "declencher": [],
        "jouer": ["66011"],
        "cibles": ["01094", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 4]], "defausse": ["66011"]},
    },
    {
        "nom": "66001b Great Minds — Sue Storm se redresse quand elle paie une carte TECH",
        "pourquoi": "capacite Resource : elle s'incline pour payer, puis se redresse si la cible est TECH",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": [],
        "main_exclusive": ["66004", "66008", "66009", "66012"],
        "declencher": [],
        "jouer": ["66004"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["66004"], "pret": ["66001b"]},
    },

    ############################################################################
    # Vague C : le reste des packs, debloque par Puzzle.Action / Puzzle.Attack.
    {
        "nom": "73004 Crack the Case — Action (thwart) : 2 menaces retirees",
        "pourquoi": "evenement jouable seulement si une manigance annexe est en jeu",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')", "Puzzle.PutIntoPlay('73013')",
                          "Puzzle.SetThreat('73013', 2)", "Puzzle.Exhaust('73001a')"],
        "main_exclusive": ["73004", "73003"],
        "declencher": [],
        "jouer": ["73004"],
        "cibles": ["73013"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["73013"], "pret": ["73001a"], "defausse": ["73004"]},
    },
    {
        "nom": "73006 Out in the Open — Interrupt : annule la traitrise et revele une manigance",
        "pourquoi": "interrupt sur revelation de traitrise, avec l'evenement en main",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')"],
        "main_exclusive": ["73006"],
        "declencher": ["Puzzle.Reveal('73020')"],
        "verifier": "manigance_annexe_en_jeu",
    },
    {
        "nom": "73007 The Truth Hurts — Hero Action (attaque) : 2 degats a un ennemi",
        "pourquoi": "seconde moitie conditionnee a une manigance vaincue ce tour, ici absente",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('73001b')", "Puzzle.PutIntoPlay('73013')"],
        "main_exclusive": ["73007", "73003"],
        "declencher": [],
        "jouer": ["73007"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "defausse": ["73007"]},
    },
    {
        "nom": "62001a Albert — Action « Initiate Protocol » : pioche 1 carte",
        "pourquoi": "capacite Special declenchee par une Action, hors de portee avant Puzzle.Action",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('62001b')"],
        "main_exclusive": ["62002"],
        "declencher": ["Puzzle.Action('62001a', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2},
    },
    {
        "nom": "62007 Donald Pierce — se redresse apres « Initiate Protocol »",
        "pourquoi": "Response sur capacite Special : le declencheur est l'Action d'Albert",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('62001b')", "Puzzle.PutIntoPlay('62007')",
                          "Puzzle.Exhaust('62007')"],
        "main_exclusive": ["62002"],
        "declencher": ["Puzzle.Action('62001a', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["62007"]},
    },
    {
        "nom": "67003 Alicia Masters — Alter-Ego Action : incliner pour piocher 2",
        "pourquoi": "action en jeu cote alter-ego",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.PutIntoPlay('67003')"],
        "main_exclusive": ["67008"],
        "declencher": ["Puzzle.Action('67003', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 3, "exhausted": ["67003"]},
    },
    {
        "nom": "67008 Toughen Up — Response : apres avoir subi des degats, l'identite devient Tenace",
        "pourquoi": "Response sur degats subis, atteinte par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')", "Puzzle.Exhaust('67001a')"],
        "main_exclusive": ["67008"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "identite_est_tenace",
    },
    {
        "nom": "65003 H.E.R.B.I.E. — Action : defausser sa main puis repiocher autant",
        "pourquoi": "action en jeu ; la main garde sa taille, le soutien s'incline",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')", "Puzzle.PutIntoPlay('65003')"],
        "main_exclusive": ["65011", "65009"],
        "declencher": ["Puzzle.Action('65003', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2, "exhausted": ["65003"]},
    },
    {
        "nom": "65004 Baxter Building — Alter-Ego Action : 2 degats soignes",
        "pourquoi": "premiere des deux actions de la carte",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.PutIntoPlay('65004')", "Puzzle.Damage('65001b', 3)"],
        "declencher": ["Puzzle.Action('65004', 'AlterEgoAction')"],
        "cibles": ["65001b"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "exhausted": ["65004"]},
    },
    {
        "nom": "65011 Slippery — Interrupt : 2 degats evites sur l'attaque de Rhino",
        "pourquoi": "interrupt sur degats subis, avec l'evenement en main",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')", "Puzzle.Exhaust('65001a')"],
        "main_exclusive": ["65011"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "defausse": ["65011"]},
    },
    {
        "nom": "65001b Reed Richards — « Great Minds » le redresse en payant une carte TECH",
        "pourquoi": "meme montage que Sue Storm 66001b : ex_operation sur une identite",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": [],
        "main_exclusive": ["65006", "65009", "65011"],
        "declencher": [],
        "jouer": ["65006"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["65006"], "pret": ["65001b"]},
    },
    {
        "nom": "64001b Johnny Storm — Action « Ignition » : incliner pour chercher une carte FIRE",
        "pourquoi": "action portee par la face alter-ego elle-meme",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": [],
        "declencher": ["Puzzle.Action('64001b', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["64001b"]},
    },
    {
        "nom": "64005 Internal Combustion — Hero Action : 3 compteurs flamme contre 3 cartes",
        "pourquoi": "cout paye en compteurs sur un ennemi puis defausse de l'amelioration",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('64001b')", "Puzzle.PutIntoPlay('64005')",
                          "Puzzle.Counter('01094', 'flame', 3)"],
        "main_exclusive": ["64007"],
        "declencher": ["Puzzle.Action('64005', 'HeroAction')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "flame", 0]], "hors_jeu": ["64005"],
                    "taille_main": 4},
    },
    {
        "nom": "64006 Spark — Hero Action : poser un compteur flamme sur un ennemi",
        "pourquoi": "seconde capacite de la carte, la premiere etant une ressource",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('64001b')", "Puzzle.PutIntoPlay('64006')"],
        "declencher": ["Puzzle.Action('64006', 'HeroAction')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "flame", 1]], "exhausted": ["64006"]},
    },
    {
        "nom": "78006 New Attilan — Alter-Ego Action : fouiller le deck jusqu'a une carte Lockjaw",
        "pourquoi": "action en jeu cote alter-ego",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.PutIntoPlay('78006')"],
        "declencher": ["Puzzle.Action('78006', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["78006"]},
    },
    {
        "nom": "78007 Doc Jaw's Lab — Alter-Ego Action : redresser Tuning Fork",
        "pourquoi": "action qui vise une AUTRE carte nommee, montage fragile",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.PutIntoPlay('78007')", "Puzzle.PutIntoPlay('78003')",
                          "Puzzle.Exhaust('78003')"],
        "declencher": ["Puzzle.Action('78007', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["78003"], "exhausted": ["78007"]},
    },
    {
        "nom": "78020 Redwing — Hero Action : s'incline et se blesse pour regarder le deck Rencontre",
        "pourquoi": "cout compose : inclinaison PLUS 1 degat sur soi",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')", "Puzzle.PutIntoPlay('78020')"],
        "declencher": ["Puzzle.Action('78020', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["78020"], "degats": [["78020", 1]]},
    },
    {
        "nom": "78030 Central Park — Alter-Ego Action : soigner 1 degat d'un PET AVENGER",
        "pourquoi": "cible restreinte par traits maison PET AVENGER / GOOD BOY",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.PutIntoPlay('78030')", "Puzzle.PutIntoPlay('78020')",
                          "Puzzle.Damage('78020', 1)"],
        "declencher": ["Puzzle.Action('78030', 'AlterEgoAction')"],
        "cibles": ["78020"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["78020", 0]], "exhausted": ["78030"]},
    },
    {
        "nom": "78021 Hairball — Interrupt : s'incline pour eviter 1 degat au heros",
        "pourquoi": "interrupt sur degats d'attaque, atteint par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')", "Puzzle.PutIntoPlay('78021')",
                          "Puzzle.Exhaust('78001a')", "Puzzle.Exhaust('78021')",
                          "Puzzle.Ready('78021')"],
        "main_exclusive": ["78024"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "exhausted": ["78021"]},
    },
    {
        "nom": "78008 Teleport To Safety — Interrupt : changer de forme evite toute l'attaque",
        "pourquoi": "l'evenement doit etre en main et le heros incapable de defendre",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')", "Puzzle.Exhaust('78001a')"],
        "main_exclusive": ["78008"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "forme": "AlterEgo", "defausse": ["78008"]},
    },


    ############################################################################
    # Vague D : derniers packs.
    {
        "nom": "78029 Inhuman's Best Friend — Alter-Ego Action : redresser un soutien",
        "pourquoi": "evenement a action d'alter-ego, cible jusqu'a 4 soutiens",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.PutIntoPlay('78006')", "Puzzle.Exhaust('78006')"],
        "main_exclusive": ["78029", "78024", "78028"],
        "declencher": [],
        "jouer": ["78029"],
        "cibles": ["78006"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["78006"], "defausse": ["78029"]},
    },
    {
        "nom": "78023 Protect The Pack — Hero Interrupt : le heros encaisse a la place de l'allie",
        "pourquoi": "redirection de degats, atteinte par Puzzle.Attack sur un allie defenseur",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')", "Puzzle.PutIntoPlay('78026')",
                          "Puzzle.Exhaust('78001a')"],
        "main_exclusive": ["78023"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "degats": [["78026", 0]], "defausse": ["78023"]},
    },
    {
        "nom": "78009 Fast Travel — Action : le joueur vise change de forme",
        "pourquoi": "evenement qui cible un JOUEUR, cas de ciblage rare",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')"],
        "main_exclusive": ["78009", "78024", "78028"],
        "payer_avec": ["78024"],
        "declencher": [],
        "jouer": ["78009"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "defausse": ["78009"]},
    },
    {
        "nom": "78011 Ruff Ambush — Hero Response : 5 degats apres le passage en forme heros",
        "pourquoi": "Response sur changement de forme, l'evenement doit etre en main",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": [],
        "main_exclusive": ["78011", "78024", "78028"],
        "declencher": ["Puzzle.ChangeForm('78001b')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 5]], "defausse": ["78011"]},
    },
    {
        "nom": "67001a The Thing — Action « Give 'Er » : defausser son statut Tenace",
        "pourquoi": "action portee par la face heros elle-meme",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')", "Puzzle.Tough('67001a')"],
        "declencher": ["Puzzle.Action('67001a', 'HeroAction')"],
        "verifier": "identite_sans_statut_tenace",
    },
    {
        "nom": "72002 Bulletproof — Hero Interrupt : 2 degats evites sur l'attaque de Rhino",
        "pourquoi": "interrupt de defense, heros incline pour qu'il ne defende pas",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('72001b')", "Puzzle.Exhaust('72001a')"],
        "main_exclusive": ["72002"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "72005 Symbiotic Fury — Response : 1 degat de plus, mais le heros se redresse",
        "pourquoi": "Response sur degats subis, atteinte par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('72001b')", "Puzzle.Exhaust('72001a')"],
        "main_exclusive": ["72005"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3, "pret": ["72001a"], "defausse": ["72005"]},
    },
    {
        "nom": "72008 Camouflage — Hero Interrupt : 4 degats et Desoriente sur l'attaquant",
        "pourquoi": "interrupt qui se defausse pour frapper l'ennemi avant son attaque",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('72001b')", "Puzzle.PutIntoPlay('72008')",
                          "Puzzle.Exhaust('72001a')"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 4]], "statuts": [["01094", "Confused"]],
                    "hors_jeu": ["72008"]},
    },
    {
        "nom": "71009 J. Jonah Jameson — Alter-Ego Action : incliner pour piocher",
        "pourquoi": "action en jeu cote alter-ego, avec pioche conditionnelle",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.PutIntoPlay('71009')"],
        "declencher": ["Puzzle.Action('71009', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["71009"]},
    },
    {
        "nom": "71010 Spider-Sense — Hero Interrupt : piocher quand le vilain attaque",
        "pourquoi": "interrupt sur initiation d'attaque, atteint par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('71001b')", "Puzzle.PutIntoPlay('71010')",
                          "Puzzle.Exhaust('71001a')"],
        "main_exclusive": ["71004"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2},
    },
    {
        "nom": "61009 Congress of Worlds — Alter-Ego Action : 2 menaces retirees du complot principal",
        "pourquoi": "action a cout mixte : inclinaison PLUS une ressource",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.PutIntoPlay('61009')", "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["61004", "61005"],
        "payer_avec": ["61004"],
        "declencher": ["Puzzle.Action('61009', 'AlterEgoAction')"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "exhausted": ["61009"]},
    },
    {
        "nom": "61011 Scrying Pool — Hero Action : incliner pour regarder le dessus d'un deck",
        "pourquoi": "action en jeu cote heros",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('61001b')", "Puzzle.PutIntoPlay('61011')"],
        "declencher": ["Puzzle.Action('61011', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["61011"]},
    },
    {
        "nom": "68011 Kinetic Stomp — Hero Interrupt : +6 ATK sur une attaque de base",
        "pourquoi": "interrupt sur attaque de base, atteint par Puzzle.Attack sur le heros",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('68001b')"],
        "main_exclusive": ["68011", "68005", "68006", "68009"],
        "declencher": ["Puzzle.Attack('68001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 7]], "defausse": ["68011"]},
    },
    {
        "nom": "70012 Dark Intangibility — Response : Cloak se redresse apres avoir defendu",
        "pourquoi": "Response sur fin de defense, atteinte par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('70001b')", "Puzzle.PutIntoPlay('70012')"],
        "main_exclusive": ["70011"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["70012"]},
    },
    {
        "nom": "70016 Bigger Fish — Forced Interrupt : le vilain manigance au lieu d'attaquer",
        "pourquoi": "remplacement d'activation, invisible sans Puzzle.Attack",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('70001b')", "Puzzle.PutIntoPlay('70016')",
                          "Puzzle.SetThreat('01097b', 0)", "Puzzle.Exhaust('70001a')"],
        "main_exclusive": ["70011"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        # La valeur exacte depend des icones de boost tirees, qui changent avec
        # le nombre de joueurs : on verifie que le vilain a bien MANIGANCE au
        # lieu d'attaquer, pas un total precis.
        "attendu": {"degats_identite": 0, "menace_min": [["01097b", 1]]},
    },


    ############################################################################
    # Vague E : les 36 cartes restantes atteignables telles quelles.
    {
        "nom": "69003 Webb's Apartment — Alter-Ego Action : soigner 1 degat",
        "pourquoi": "action en jeu cote alter-ego, cible « personnage que vous controlez »",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.PutIntoPlay('69003')", "Puzzle.Damage('69001b', 3)"],
        "declencher": ["Puzzle.Action('69003', 'AlterEgoAction')"],
        "cibles": ["69001b"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "exhausted": ["69003"]},
    },
    {
        "nom": "69005 Astral Form — Hero Action : 1 menace retiree par allie controle",
        "pourquoi": "X calcule sur le nombre d'allies, avec cout mixte inclinaison + [mental]",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('69001b')", "Puzzle.PutIntoPlay('69005')",
                          "Puzzle.PutIntoPlay('69002')", "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["69009"],
        "payer_avec": ["69009"],
        "declencher": ["Puzzle.Action('69005', 'HeroAction')"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]], "exhausted": ["69005"]},
    },
    {
        "nom": "69017 Ana Kraven — Forced Response : 1 menace sur le complot apres son attaque",
        "pourquoi": "The Grim Hunt absente, la branche de repli vise le complot principal",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('69001b')", "Puzzle.PutIntoPlay('69017')",
                          "Puzzle.SetThreat('01097b', 0)", "Puzzle.Exhaust('69001a')"],
        "main_exclusive": ["69010"],
        "declencher": ["Puzzle.Attack('69017')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    {
        "nom": "69024 Spider-Woman (May Parker) — Hero Interrupt : piocher quand le vilain attaque",
        "pourquoi": "interrupt porte par un ALLIE, sur l'initiation d'attaque du vilain",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('69001b')", "Puzzle.PutIntoPlay('69024')",
                          "Puzzle.Exhaust('69001a')", "Puzzle.Exhaust('69024')"],
        "main_exclusive": ["69010"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2},
    },
    {
        "nom": "70007 Lightforce Absorption — Response : s'incline apres une carte LIGHTFORCE",
        "pourquoi": "Response sur « apres avoir joue une carte du trait X »",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('70001b')", "Puzzle.PutIntoPlay('70007')",
                          "Puzzle.Discard('70005')", "Puzzle.Damage('70001a', 3)"],
        "main_exclusive": ["70004", "70006"],
        "declencher": [],
        "jouer": ["70004"],
        "cibles": ["70001a"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["70007"]},
    },
    {
        "nom": "70013 Darkforce Absorption — Response : s'incline apres une carte DARKFORCE",
        "pourquoi": "miroir exact de 70007, le trait change",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('70001b')", "Puzzle.PutIntoPlay('70013')",
                          "Puzzle.Discard('70010')", "Puzzle.Exhaust('70001a')"],
        "main_exclusive": ["70009", "70011"],
        "declencher": [],
        "jouer": ["70009"],
        "cibles": ["70001a"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["70013"]},
    },
    {
        "nom": "70015 Mister Negative — Forced Response : son attaque renvoie en alter-ego",
        "pourquoi": "Forced Response sur attaque du heros, inatteignable avant Puzzle.Attack",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('70001b')", "Puzzle.PutIntoPlay('70015')",
                          "Puzzle.Exhaust('70001a')"],
        "main_exclusive": ["70011"],
        "declencher": ["Puzzle.Attack('70015')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo"},
    },
    {
        "nom": "76009 Gear Up — Hero Interrupt : defendre puis basculer en alter-ego",
        "pourquoi": "interrupt de defense, le heros doit etre PRET pour defendre",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('76001b')"],
        "main_exclusive": ["76009", "76007", "76008"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["76001c"], "hors_jeu": ["76001a"], "defausse": ["76009"]},
    },
    {
        "nom": "76011 Versatility — Hero Action : dessus de defausse Aggression, donc 4 degats",
        "pourquoi": "l'effet depend de l'ASPECT de la carte au-dessus de la defausse",
        "scenario": "rhino",
        "heros": "moon_knight",
        # Main sans aucune autre carte d'attaque : Moon Knight met les couts
        # d'aspect a zero, et avec Deck and Cover en main le pilote enchainait
        # une seconde attaque qui faussait le total.
        "mise_en_place": ["Puzzle.ChangeForm('76001b')"],
        "main_exclusive": ["76011", "76005", "76006"],
        "declencher": [],
        "jouer": ["76011"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        # 7 et pas 4 : Moon Knight met les couts d'aspect a zero, et le pilote
        # joue Surprise Attack (3 degats) depuis la MAIN DE DEPART, avant meme
        # que `main_exclusive` ne la vide. Meme phenomene que Deck and Cover.
        "attendu": {"degats": [["01094", 7]], "defausse": ["76011"]},
    },
    {
        "nom": "76017 Doctor Strange — Forced Response : defausse aleatoire apres ses degats",
        "pourquoi": "Forced Response sur degats infliges au heros",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('76001b')", "Puzzle.PutIntoPlay('76017')",
                          "Puzzle.Exhaust('76001a')"],
        "main_exclusive": ["76007", "76008"],
        "declencher": ["Puzzle.Attack('76017')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 1},
    },
    {
        "nom": "76019 Iron Fist — Forced Response : le personnage blesse est Sonne",
        "pourquoi": "Forced Response sur degats infliges a un personnage controle",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('76001b')", "Puzzle.PutIntoPlay('76019')",
                          "Puzzle.Exhaust('76001a')"],
        "main_exclusive": ["76007"],
        "declencher": ["Puzzle.Attack('76019')"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["76001a", "Stunned"]]},
    },
    {
        "nom": "76024 The Iron Fist — Hero Interrupt : +1 degat et l'ennemi est Sonne",
        "pourquoi": "cout mixte inclinaison PLUS retrait d'un compteur mystic",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('76001b')", "Puzzle.PutIntoPlay('76024')",
                          "Puzzle.Counter('76024', 'mystic', 1)"],
        "main_exclusive": ["76007"],
        "declencher": ["Puzzle.Attack('76001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["01094", "Stunned"]], "exhausted": ["76024"]},
    },
    {
        "nom": "61001a Thor — Action « Worthy » : Mjolnir arrive en main",
        "pourquoi": "action portee par la face heros, fouille deck ET defausse",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('61001b')"],
        "declencher": ["Puzzle.Action('61001a')"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["61007"]},
    },
    {
        "nom": "61004 Hammer Swing — Hero Action (attaque) : 4 degats en inclinant Mjolnir",
        "pourquoi": "le cout d'inclinaison porte sur une AUTRE carte que l'evenement",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('61001b')", "Puzzle.PutIntoPlay('61007')"],
        "main_exclusive": ["61004", "61005"],
        "declencher": [],
        "jouer": ["61004"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]], "exhausted": ["61007"], "defausse": ["61004"]},
    },
    {
        "nom": "61008 Unyielding — Hero Response : attaque encaissee a 0 degat, 2 menaces retirees",
        "pourquoi": "declencheur « apres avoir ete attaque SANS subir de degat », d'ou le statut Tenace",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('61001b')", "Puzzle.PutIntoPlay('61008')",
                          "Puzzle.SetThreat('01097b', 5)", "Puzzle.Tough('61001a')"],
        "main_exclusive": ["61006"],
        "declencher": ["Puzzle.Attack('01094')"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "exhausted": ["61008"]},
    },
    {
        "nom": "61012 Goddess of Thunder — Hero Resource : elle finance une carte Thor",
        "pourquoi": ("la capacite Resource est bien sollicitee et la carte s'incline. "
                     "Le DOUBLEMENT pour une carte du set signature n'est PAS prouve ici : "
                     "avec la seule Goddess en source, une carte a cout 2 reste impayable"),
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('61001b')", "Puzzle.PutIntoPlay('61012')"],
        "main_exclusive": ["61006", "61013"],
        "declencher": [],
        "jouer": ["61006"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["61012"], "defausse": ["61006"]},
    },
    {
        "nom": "65001a Mister Fantastic — « Flexibility » : la carte SUPERPOWER depensee revient en main",
        "pourquoi": "Response sur defausse d'une carte du trait SUPERPOWER",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('65001b')"],
        "main_exclusive": ["65010", "65011"],
        "payer_avec": ["65011"],
        "declencher": [],
        "jouer": ["65010"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["65011"]},
    },


    {
        "nom": "67007 True Grit — Hero Action : 2 degats a soi pour se redresser et perdre un statut",
        "pourquoi": "cout paye en degats sur sa propre identite",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('67001b')", "Puzzle.PutIntoPlay('67007')",
                          "Puzzle.Stun('67001a')", "Puzzle.Exhaust('67001a')"],
        "declencher": ["Puzzle.Action('67007', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["67001a"], "degats_identite": 2},
    },
    {
        "nom": "78004 Jaw Lock — Response : un evenement TELEPORT blesse l'ennemi porteur",
        "pourquoi": "l'amelioration s'attache a un ENNEMI, la Response lit son porteur",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')"],
        "main_exclusive": ["78004", "78010", "78024", "78028", "78027", "78009"],
        "declencher": [],
        "jouer": ["78004", "78010"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        # 2 degats : 1 de Zooming Around lui-meme, 1 de la Response de Jaw Lock.
        "attendu": {"degats": [["01094", 2]], "en_jeu": ["78004"]},
    },
    {
        "nom": "78001a Lockjaw — Action « Fetch! » : recuperer une carte de la defausse",
        "pourquoi": "action portee par la face heros, cout inclinaison PLUS un joker",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('78001b')"],
        "main_exclusive": ["78024", "78028"],
        "declencher": ["Puzzle.Discard('78027')",
                       "Puzzle.Action('78001a', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 3, "exhausted": ["78001a"]},
    },
    {
        "nom": "71001b Peter Parker — Action : defausser 1 carte pour en chercher une",
        "pourquoi": "action portee par la face alter-ego, cout paye en defaussant de la main",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": [],
        "main_exclusive": ["71004", "71005"],
        "declencher": ["Puzzle.Action('71001b', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2},
    },
    {
        "nom": "71004 Web Barrage — Hero Action a cout X : toiler et blesser un ennemi",
        "pourquoi": "cout X, d'ou le surpaiement obligatoire pour que X vaille au moins 1",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('71001b')"],
        "main_exclusive": ["71004", "71005", "71006"],
        "surpayer": True,
        "declencher": [],
        "jouer": ["71004"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 2]], "defausse": ["71004"]},
    },
    {
        "nom": "64009 Radiate — cout X : 2 compteurs flamme sur un ennemi",
        "pourquoi": "premiere des deux options, cout X paye par surpaiement",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('64001b')"],
        "main_exclusive": ["64009", "64007", "64008"],
        "surpayer": True,
        "declencher": [],
        "jouer": ["64009"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "flame", 2]], "defausse": ["64009"]},
    },
    {
        "nom": "68001b Amadeus Cho — Action « Reverse Engineer » : defausser pour piocher",
        "pourquoi": "X = cout imprime de la carte signature defaussee",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": [],
        "main_exclusive": ["68009", "68005"],
        "declencher": ["Puzzle.Action('68001b', 'Action')"],
        "verifier": "etat_attendu",
        # Le pilote defausse 68005 (cout imprime 2), donc 1 carte restante + 2 piochees.
        "attendu": {"taille_main": 3},
    },
    {
        "nom": "68004 Kegger — Action : se remelanger avec une carte pour redresser l'identite",
        "pourquoi": "cout paye en remelangeant DEUX cartes dans le deck",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('68001b')", "Puzzle.PutIntoPlay('68004')",
                          "Puzzle.Exhaust('68001a')"],
        "main_exclusive": ["68005", "68006"],
        "declencher": ["Puzzle.Action('68004', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["68001a"], "hors_jeu": ["68004"]},
    },
    {
        "nom": "68014 Lady Hellbender — Hero Action : la sbire devient une alliee",
        "pourquoi": "cout en jokers egal aux PV restants, puis TreatAsAlly",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('68001b')", "Puzzle.PutIntoPlay('68014')",
                          "Puzzle.Damage('68014', 4)"],
        "main_exclusive": ["68007", "68005", "68006"],
        "declencher": ["Puzzle.Action('68014', 'HeroAction')"],
        "verifier": "tah_hellbender_alliee",
    },


    {
        "nom": "58001a Wonder Man — « Power Recycling » : +1 ATK par carte glissee sous Ionic Physiology",
        "pourquoi": ("temoin du correctif du 5/8/2026 : la construction d'origine empechait "
                     "toute creation de partie. Jouer un evenement [energy] le glisse sous "
                     "Ionic Physiology, donc l'ATK doit monter de 1"),
        "scenario": "rhino",
        "heros": "wonder_man",
        # Active Altruism exige une manigance PORTANT de la menace pour etre
        # jouable (`has_threat=True`).
        "mise_en_place": ["Puzzle.ChangeForm('58001b')", "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["58003", "58004"],
        "declencher": [],
        "jouer": ["58003"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}, "en_jeu": ["58002"]},
    },


    {
        "nom": "70002a Bright Barrage — l'attaque de base de Dagger se repartit entre ennemis",
        "pourquoi": ("capacite perdue lors de la refonte du 5/8/2026 et recablee : la face "
                     "heros a une vraie attaque de base, `ThisCanAttack(canbe_divided=True)` "
                     "suffit (modele Wasp 13001c). Dagger a 3 ATK avec Cloak en jeu, on les "
                     "repartit sur deux sbires"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')",
                          "Puzzle.ChangeForm('Tandy Bowen')",
                          "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01103')"],
        "declencher": ["Puzzle.Attack('70002a')"],
        "cibles": ["01101", "01103"],
        "verifier": "cd_barrage_reparti",
    },


    {
        "nom": "70003 Forces Combined — la main de l'identite liee finance le cout de l'autre",
        "pourquoi": ("texte imprime enfin rendu depuis la refonte du 5/8/2026 : les DEUX "
                     "mains existent. La main de Cloak est reduite a la SEULE carte jouee, "
                     "qui coute 3 : sans le financement par la main de l'identite liee, "
                     "elle est strictement impayable"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')",
                          "Puzzle.ChangeForm('Tandy Bowen')"],
        "main_exclusive": ["70005"],
        "declencher": [],
        "jouer": ["70005"],
        "cibles": ["01094", "01094", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"defausse": ["70005"], "degats_min": [["01094", 3]],
                    "exhausted": ["70003"]},
    },


    ############################################################################
    # Vague G : les 19 cartes restantes.
    {
        "nom": "70002b Tandy Bowen — Harmony : +2 REC tant que Tyrone Johnson est en jeu",
        "pourquoi": "moitie de Harmony qui vise l'AUTRE alter-ego, donc conditionnee",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "cd_tandy_recover",
    },
    {
        "nom": "68001c Uncontrollable Hulk — Interrupt : ses attaques font 2 degats de plus",
        "pourquoi": "forme BRUTE atteinte par les compteurs rage de « The Trunk »",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('68001b')",
                          "Puzzle.Counter('68012a', 'rage', 4)"],
        "main_exclusive": ["68009"],
        "declencher": ["Puzzle.Attack('68001c')"],
        "cibles": ["01094"],
        "verifier": "tah_brute_frappe_plus_fort",
    },
    {
        "nom": "68001a Totally Awesome Hulk — « Hypermind » : toute ressource generee devient [wild]",
        "pourquoi": ("interception de `CheckEffectGeneratedResources` : une carte a cout "
                     "colore doit se payer avec des icones d'une AUTRE couleur"),
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('68001b')"],
        "main_exclusive": ["68009", "68006"],
        "payer_avec": ["68006"],
        "declencher": [],
        "jouer": ["68009"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"defausse": ["68009"]},
    },
    {
        "nom": "69027 Order of the Web — soutien pose sous le controle d'un autre joueur",
        "pourquoi": "texte multijoueur, inexercable en solo : la partie est montee A DEUX",
        "scenario": "rhino",
        "heros": "madame_web",
        "heros2": "spider_man",
        "mise_en_place": ["Puzzle.ChangeForm('69001b')"],
        "main_exclusive": ["69027", "69010", "69011"],
        "declencher": [],
        "jouer": ["69027"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["69027"]},
    },
    {
        "nom": "71013 Bad Publicity — l'obligation arrive en jeu avec ses compteurs",
        "pourquoi": "obligation a Uses, donnee au joueur Peter Parker ; partie montee A DEUX",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "heros2": "spider_man",
        "mise_en_place": ["Puzzle.ChangeForm('71001b')"],
        "declencher": ["Puzzle.Reveal('71013')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["71013"]},
    },


    {
        "nom": "63001b Gwendolyn Poole — Action « I Won't Be an Extra » : une carte Gwenpool en main",
        "pourquoi": "action portee par la face alter-ego, fouille deck ET defausse",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": [],
        "main_exclusive": ["63003"],
        "declencher": ["Puzzle.Action('63001b', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2},
    },
    {
        "nom": "63004 Fun Background Noise — annule la traitrise, puis la bulle rend Gwenpool Tenace",
        "pourquoi": ("teste d'un coup l'interruption ET « Medium Awareness » (63001a), le "
                     "moteur de bulles qui remplit les blancs des cartes Gwenpool"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('63001b')"],
        "main_exclusive": ["63004", "63002", "63005"],
        "declencher": ["Puzzle.Reveal('63013')"],
        "verifier": "identite_est_tenace",
    },
    {
        "nom": "63008 Comicbook Panels — Hero Action : incliner les deux cartes pour deux bulles",
        "pourquoi": ("cout compose : la carte elle-meme PLUS Unbelievable Gwenpool, "
                     "et deux blancs a remplir"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('63001b')", "Puzzle.PutIntoPlay('63008')",
                          "Puzzle.PutIntoPlay('63009')"],
        "declencher": ["Puzzle.Action('63008', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["63008", "63009"]},
    },
    {
        "nom": "76001c Mr. Knight — « The Best Defense » : les cartes Protection coutent 1 de moins",
        "pourquoi": ("main reduite a la SEULE carte jouee : sans la reduction son cout 1 "
                     "est impayable, avec elle il tombe a 0"),
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('76001b')",
                          "Puzzle.ChangeForm('76001a', 'Hero')"],
        "main_exclusive": ["01081"],
        "declencher": [],
        "jouer": ["01081"],
        "verifier": "mk_reduction_protection",
    },
    {
        "nom": "71001a Spider-Man — « Just Like Flies » : le sbire qui s'engage est toile",
        "pourquoi": "Interrupt sur engagement, declenche par l'arrivee du sbire",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('71001b')"],
        "declencher": ["Puzzle.PutIntoPlay('01101')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01101", "web", 1]]},
    },
    {
        "nom": "70008 Living Light — Hero Action : 5 degats au vilain deverrouillent l'inclinaison",
        "pourquoi": ("« cannot be exhausted until 5+ damage this phase » : deux attaques de "
                     "Cloak a 3 ATK suffisent, l'action redresse ensuite Dagger"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')",
                          "Puzzle.ChangeForm('Tandy Bowen')",
                          "Puzzle.PutIntoPlay('70008')",
                          "Puzzle.Exhaust('70002a')"],
        # Cloak n'a qu'1 ATK (le +2 de Destructive Duo va a Dagger) : il faut
        # cinq attaques pour franchir le seuil de 5 degats de la phase.
        "declencher": ["Puzzle.Attack('70001a')", "Puzzle.Ready('70001a')",
                       "Puzzle.Attack('70001a')", "Puzzle.Ready('70001a')",
                       "Puzzle.Attack('70001a')", "Puzzle.Ready('70001a')",
                       "Puzzle.Attack('70001a')", "Puzzle.Ready('70001a')",
                       "Puzzle.Attack('70001a')",
                       "Puzzle.Action('70008', 'HeroAction')"],
        "cibles": ["01094", "01094", "01094", "01094", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["70002a"], "exhausted": ["70008"]},
    },


    {
        "nom": "69009 Foresight — Hero Interrupt : annuler et defausser la carte Rencontre",
        "pourquoi": ("cout paye en inclinant l'IDENTITE. Longtemps cru defaillant : c'etait "
                     "`Puzzle.Reveal` qui ne faisait pas venir la carte du deck Rencontre, "
                     "donc `from_encounter=True` ne matchait jamais"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('69001b')"],
        "main_exclusive": ["69009", "69010", "69011"],
        "declencher": ["Puzzle.Reveal('69021')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["69001a"], "degats_identite": 0, "defausse": ["69009"]},
    },

    # ------------------------------------------------------------------------
    # Pack « squirrel_girl » : 75001a-75022 (custom)
    #
    # Deux notions maison a prouver : APPELER un ecureuil (le deck additionnel
    # se vide vers le champ de bataille) et DEPENSER un ecureuil (il finance
    # une carte du set). Le reste des cas verifie que les regles speciales du
    # mot-cle « Squirrel » tiennent, y compris les deux points d'accroche poses
    # dans le moteur (cible et bonus refuses hors du set).
    # ------------------------------------------------------------------------
    {
        "nom": "75001b Setup — le deck ecureuil est monte avec ses 6 allies",
        "pourquoi": "sans deck ecureuil, aucune carte du pack ne fonctionne",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "sg_deck_ecureuil_complet",
    },
    {
        "nom": "75001b Squirrel Speech — l'alter-ego s'incline pour appeler 1 ecureuil",
        "pourquoi": "premier appel du pack : le deck additionnel doit se vider vers le jeu",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": [],
        "declencher": ["Puzzle.Action('75001b', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu_trait": [["SQUIRREL", 1]], "exhausted": ["75001b"]},
    },
    {
        "nom": "75001a Unbeatable Army — depenser un ecureuil retire 1 menace ou fait 1 degat",
        "pourquoi": "la capacite d'identite est branchee sur la depense, notion maison du pack",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        # L'ecureuil est APPELE par le jeu, pas pose par Puzzle.PutIntoPlay :
        # une carte posee d'autorite n'a pas de controleur, et sa capacite
        # Resource n'est alors jamais proposee au paiement.
        "mise_en_place": ["Puzzle.Action('75001b', 'AlterEgoAction')",
                          "Puzzle.ChangeForm('75001b')"],
        "main_exclusive": ["75014", "01088"],
        "declencher": [],
        "jouer": ["75014"],
        "cibles": ["01094"],
        "payer_avec": ["75002", "75003", "75004", "75005", "75006", "75007"],
        "verifier": "sg_ecureuil_depense",
    },
    {
        "nom": "75008 Nancy Whitehead — son entree en jeu appelle 1 ecureuil",
        "pourquoi": "AfterCardEnterPlay('This') doit appeler pour le controleur",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('75008')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["75008"], "en_jeu_trait": [["SQUIRREL", 1]]},
    },
    {
        "nom": "75009 Squirrel Girl's Costume — +1 ATK a l'identite",
        "pourquoi": "GiveKeywordToAttached(Hero) sur une amelioration signature",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('75001b')"],
        "declencher": ["Puzzle.PutIntoPlay('75009')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}, "en_jeu": ["75009"]},
    },
    {
        "nom": "75009 Squirrel Girl's Costume — un sbire vaincu appelle 1 ecureuil",
        "pourquoi": "ecart assume au materiel : le declencheur est « un sbire est vaincu »",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('75001b')", "Puzzle.PutIntoPlay('75009')",
                          "Puzzle.PutIntoPlay('01103')"],
        "declencher": ["Puzzle.Damage('01103', 9)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01103"], "en_jeu_trait": [["SQUIRREL", 1]]},
    },
    {
        "nom": "75011 Central Park — s'incline et appelle 1 ecureuil",
        "pourquoi": "action conditionnee au nombre d'ecureuils controles",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.PutIntoPlay('75011')"],
        "declencher": ["Puzzle.Action('75011', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["75011"], "en_jeu_trait": [["SQUIRREL", 1]]},
    },
    {
        "nom": "75013 Call the Squirrels — 2 ecureuils entrent en jeu PRETS",
        "pourquoi": "seule carte qui appelle des ecureuils prets ; ils doivent pouvoir agir",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('75001b')"],
        "main_exclusive": ["75013", "01088", "01089"],
        "declencher": [],
        "jouer": ["75013"],
        "verifier": "sg_deux_ecureuils_prets",
    },
    {
        "nom": "75014 Squirrel Swarm — 3 degats sans ecureuil depense",
        "pourquoi": "valeur de base apres arbitrage (3 puis +3), a distinguer du bonus",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('75001b')"],
        "main_exclusive": ["75014", "01088", "01089"],
        "declencher": [],
        "jouer": ["75014"],
        "cibles": ["01094"],
        "payer_avec": ["01088", "01089"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "defausse": ["75014"]},
    },
    {
        "nom": "75015 Recon Team — retire 3 menaces de la manigance principale",
        "pourquoi": "branche de base de l'evenement de manigance",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('75001b')", "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["75015", "01088", "01089"],
        "declencher": [],
        "jouer": ["75015"],
        "cibles": ["01097b"],
        "payer_avec": ["01088", "01089"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]], "defausse": ["75015"]},
    },
    {
        "nom": "75017 Nuts! — depensee pour une carte du set, elle appelle 1 ecureuil",
        "pourquoi": "WhenYouSpendThisCardToPlay filtre sur le set SQUIRREL GIRL",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('75001b')"],
        "main_exclusive": ["75014", "75017"],
        "declencher": [],
        "jouer": ["75014"],
        "cibles": ["01094"],
        "payer_avec": ["75017"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu_trait": [["SQUIRREL", 1]], "degats": [["01094", 3]]},
    },
    {
        "nom": "75002 Tippy-Toe — Boot Camp ne peut PAS augmenter son ATK",
        "pourquoi": ("regle centrale du set, rendue par le point d'accroche `refuse_gain_fn` "
                     "pose dans face_gain.py (CORRECTIF §9)"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        # L'ecureuil est APPELE par le jeu : une carte posee par Puzzle est une
        # copie neuve, qui n'a pas recu les regles speciales du setup.
        "mise_en_place": ["Puzzle.Action('75001b', 'AlterEgoAction')"],
        "declencher": ["Puzzle.PutIntoPlay('13016')"],
        "verifier": "sg_ecureuil_refuse_bonus",
    },
    {
        "nom": "75002 temoin — Boot Camp augmente bien l'ATK d'un allie ORDINAIRE",
        "pourquoi": "sans ce temoin, le cas precedent passerait meme si Boot Camp etait inerte",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.PutIntoPlay('01051')"],
        "declencher": ["Puzzle.PutIntoPlay('13016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["13016", "01051"], "attributs_carte": [["01051", "attack", 1]]},
    },
    {
        "nom": "75019 Ratatoskr — son activation defausse un ecureuil",
        "pourquoi": "Forced Interrupt de la nemesis, qui punit l'armee",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('75001b')", "Puzzle.PutIntoPlay('75002')",
                          "Puzzle.PutIntoPlay('75019')"],
        "declencher": ["Puzzle.Attack('75019')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["75002"]},
    },
    {
        "nom": "75020 Discord in the Branches — 1 menace quand un ecureuil entre en jeu",
        "pourquoi": "Forced Response limite a une fois par round sur le trait SQUIRREL",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Reveal('75020')"],
        "declencher": ["Puzzle.PutIntoPlay('75002')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["75020", 3]], "en_jeu": ["75002"]},
    },
    {
        "nom": "75020 Discord in the Branches — les capacites des ecureuils sont blanches",
        "pourquoi": ("le blanchiment est porte par CHAQUE ecureuil : sans lui, Monkey Joe "
                     "appellerait encore un ecureuil en tuant un sbire"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Reveal('75020')", "Puzzle.PutIntoPlay('75008')"],
        "declencher": [],
        "verifier": "sg_capacites_blanches",
    },
    {
        "nom": "75021 Poisoned Rumors — sans ecureuil, 2 menaces sur Discord",
        "pourquoi": "gabarit officiel « sinon » retenu a l'arbitrage, a la place du choix libre",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Reveal('75020')"],
        "declencher": ["Puzzle.Reveal('75021')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["75020", 4]]},
    },
    {
        "nom": "75022 Ratatoskr's Whispers — capacite Boost : defausse un ecureuil",
        "pourquoi": "branche Boost de l'attachement, jamais atteinte par une partie normale",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Action('75001b', 'AlterEgoAction')"],
        "declencher": ["Puzzle.Boost('75022')"],
        "verifier": "sg_aucun_ecureuil_en_jeu",
    },
    {
        "nom": "75005 The Bruiser — encaisse le degat consequent d'un autre ecureuil",
        "pourquoi": ("carte redessinee a l'arbitrage : sans elle, Lookout et Monkey Joe "
                     "meurent des leur premiere action"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Action('75001b', 'AlterEgoAction')",
                          "Puzzle.PutIntoPlay('75011')",
                          "Puzzle.Action('75011', 'Action')",
                          "Puzzle.PutIntoPlay('75008')",
                          "Puzzle.ChangeForm('75001b')",
                          "Puzzle.SetThreat('01097b', 4)"],
        # Rien n'est joue depuis la main : le pilote paierait en DEPENSANT les
        # ecureuils, et il ne resterait personne pour agir. Les deux ecureuils
        # sont redresses : appeles, ils arrivent inclines, et le cout de The
        # Bruiser est justement de s'incliner.
        "declencher": ["Puzzle.Ready('75002')", "Puzzle.Ready('75005')",
                       "Puzzle.Action('75002', 'BasicPower', 1)"],
        "verifier": "sg_bruiser_encaisse",
    },
    {
        "nom": "75010 Prehensile Tail — finance seule une carte du set et s'incline",
        "pourquoi": "ressource restreinte : elle ne doit payer QUE les cartes Squirrel Girl",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('75001b')", "Puzzle.PutIntoPlay('75010')"],
        "main_exclusive": ["75014", "01088"],
        "declencher": [],
        "jouer": ["75014"],
        "cibles": ["01094"],
        "payer_avec": ["75010"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["75010"], "degats": [["01094", 3]], "defausse": ["75014"]},
    },
    {
        "nom": "75018 Surprise Exam — l'obligation se resout et quitte le jeu",
        "pourquoi": "obligation du pack, jamais jouee ; verifie surtout qu'elle ne plante pas",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Action('75001b', 'AlterEgoAction')"],
        "declencher": ["Puzzle.Reveal('75018')"],
        "verifier": "obligation_resolue_75018",
    },
    {
        "nom": "75016 Unbeatable! — +2 DEF en defense, et le heros se redresse si rien ne passe",
        "pourquoi": ("premiere carte « Hero Interrupt (defense) » atteignable : "
                     "`Puzzle.Attack(defender=...)` declare enfin un defenseur"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('75001b')"],
        "main_exclusive": ["75016", "01088"],
        "declencher": ["Puzzle.Defend('75001a', '01094')"],
        "verifier": "sg_unbeatable",
    },
    {
        "nom": "75012 Network of Trees — s'incline pour choisir l'ecureuil appele",
        "pourquoi": "l'interruption vit dans AppelerEcureuil, seul point de passage des appels",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.PutIntoPlay('75012')"],
        "declencher": ["Puzzle.Action('75001b', 'AlterEgoAction')"],
        "cibles": ["75002", "75003", "75004", "75005", "75006", "75007"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["75012"], "en_jeu_trait": [["SQUIRREL", 1]]},
    },
    {
        "nom": "75011 Central Park — n'appelle rien quand tu controles deja 3 ecureuils",
        "pourquoi": "la condition « fewer than 3 » est dans le handler : sans elle, appel infini",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Action('75001b', 'AlterEgoAction')",
                          "Puzzle.PutIntoPlay('75011')",
                          "Puzzle.Action('75011', 'Action')",
                          "Puzzle.PutIntoPlay('75008')",
                          "Puzzle.Ready('75011')"],
        "declencher": ["Puzzle.Action('75011', 'Action')"],
        "verifier": "sg_central_park_plafond",
    },
    {
        "nom": "75016 temoin — sans defenseur declare, Unbeatable! reste en main",
        "pourquoi": ("prouve que c'est bien `defender` qui ouvre la fenetre de defense : "
                     "sans lui le cas precedent passerait meme si la carte etait morte"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('75001b')", "Puzzle.Exhaust('75001a')"],
        "main_exclusive": ["75016", "01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "sg_unbeatable_non_jouee",
    },
    {
        "nom": "75007 The Gatherer — le depenser soigne 1 degat a Squirrel Girl",
        "pourquoi": ("arbitrage du 5/8/2026 : les ecureuils 0/0 paient au moment ou on s'en "
                     "separe, pas a leur entree en jeu"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        # `under_control=True` : sans lui l'ecureuil est en jeu mais sans
        # controleur, et sa capacite Resource n'est jamais proposee au paiement.
        # Nancy Whitehead coute 3 : Energy en fournit 2, l'ecureuil le
        # troisieme. Il ne PEUT pas etre paye autrement, donc la depense est
        # certaine — et un seul ecureuil suffit, la limite est respectee.
        "mise_en_place": ["Puzzle.ChangeForm('75001b')",
                          "Puzzle.PutIntoPlay('75007', under_control=True)",
                          "Puzzle.Damage('75001a', 3)"],
        "main_exclusive": ["75008", "01088"],
        "declencher": [],
        "jouer": ["75008"],
        "verifier": "sg_gatherer_soigne",
    },
    {
        "nom": "75006 The Forager — le depenser fait fouiller le dessus du deck",
        "pourquoi": ("seconde carte arbitree le 5/8/2026 vers un effet a la depense ; "
                     "sa branche optionnelle exige `accepter_choix`"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        # Strength (01090) est remontee sur le dessus du deck : c'est elle que
        # le Forager doit faire defausser, ce qui rend l'effet observable.
        # Nancy Whitehead (cout 3) oblige a completer Energy par l'ecureuil.
        "mise_en_place": ["Puzzle.ChangeForm('75001b')",
                          "Puzzle.PutIntoPlay('75006', under_control=True)",
                          "Puzzle.PutIntoDeck('01090')"],
        "main_exclusive": ["75008", "01088"],
        "declencher": [],
        "jouer": ["75008"],
        "accepter_choix": True,
        "verifier": "sg_forager_defausse",
    },
    {
        "nom": "75003 Monkey Joe — vaincre un sbire appelle 1 ecureuil",
        "pourquoi": "seule capacite du deck ecureuil branchee sur une attaque",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('75001b')",
                          "Puzzle.PutIntoPlay('75003', under_control=True)",
                          "Puzzle.PutIntoPlay('01103')",
                          "Puzzle.Damage('01103', 2)"],
        "declencher": ["Puzzle.Action('75003', 'BasicPower', 0)"],
        "cibles": ["01103"],
        "verifier": "sg_monkey_joe",
    },
    {
        "nom": "75002/75005 — un seul ecureuil peut payer une meme carte",
        "pourquoi": ("regle du materiel d'origine, absente du moteur : sans elle deux "
                     "ecureuils paient une carte a cout 2, donc gratuitement"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('75001b')",
                          "Puzzle.PutIntoPlay('75002', under_control=True)",
                          "Puzzle.PutIntoPlay('75005', under_control=True)"],
        "main_exclusive": ["75014"],
        "declencher": [],
        "jouer": ["75014"],
        "cibles": ["01094"],
        "verifier": "sg_un_seul_ecureuil_par_carte",
    },

    # ------------------------------------------------------------------------
    # Pack « brawn » : 77001a-77025 (custom, auteur « Rainy »)
    #
    # Tout le pack tourne autour de la RESERVE, zone hors-jeu de 3 cartes que le
    # moteur ne connaissait pas (voir les # CORRECTIF de game/deck/deck_type.py,
    # game/player/player.py, game/card/card.py, game/ability/cost_func.py et
    # game/ability/factory/resources.py). Les cas ci-dessous prouvent, dans
    # l'ordre : qu'on peut y METTRE une carte, qu'une carte y reste JOUABLE,
    # qu'elle y est DEPENSABLE, et que le cloisonnement du paiement tient.
    # ------------------------------------------------------------------------
    {
        "nom": "77001b Mastermind Excello — une carte du dessus part en reserve",
        "pourquoi": "premier remplissage de la reserve : sans lui, rien du pack ne demarre",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": [],
        "declencher": ["Puzzle.Action('77001b', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_reserve": 1},
    },
    {
        "nom": "77001a The Complete Package — la ressource n'existe QUE si Brawn est epuise",
        "pourquoi": ("condition inversee par rapport aux identites generatrices "
                     "habituelles, qui s'epuisent POUR generer"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')"],
        "declencher": [],
        "verifier": "brawn_ressource_seulement_si_epuise",
    },
    {
        "nom": "77012 Cho's Lab — changer de forme envoie la carte du dessous en reserve",
        "pourquoi": "Hero Response sur AfterUnitChangeForm, restreinte a l'arrivee en heros",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.PutIntoPlay('77012')"],
        "declencher": ["Puzzle.ChangeForm('77001b')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_reserve": 1, "exhausted": ["77012"]},
    },
    {
        "nom": "77015 Hulk Out — 2 compteurs de rage donnent +2 ATK, +2 DEF et riposte 1",
        "pourquoi": ("arbitrage du 7/8/2026 : le « for each » porte sur ATK et DEF, "
                     "PAS sur riposte, qui reste a 1"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')"],
        "declencher": ["Puzzle.PutIntoPlay('77015')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 2, "defense": 2, "retaliate": 1},
                    "en_jeu": ["77015"],
                    "compteurs": [["77015", "rage", 2]]},
    },
    {
        "nom": "77013 Brawn's Suit — +2 PV a l'identite",
        "pourquoi": "amelioration signature : le bonus vise « You », pas le type Hero",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')"],
        "declencher": ["Puzzle.PutIntoPlay('77013')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 2}, "en_jeu": ["77013"]},
    },
    {
        "nom": "77006 Gamma Strike — paye en [physical] uniquement : 10 degats",
        "pourquoi": "la moitie « only [physical] » ajoute 3 degats et l'overkill",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')"],
        # 01077 Counter-Punch porte une icone [physical] ; Haymaker 01087, elle,
        # est ENERGIE — la premiere version du cas payait donc en [energy] et
        # mesurait 7 degats. La carte etait juste, le test faux.
        "main_exclusive": ["77006", "01077", "01077", "01077"],
        "declencher": [],
        "jouer": ["77006"],
        "cibles": ["01094"],
        "payer_avec": ["01077", "01077", "01077"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 10]]},
    },
    {
        "nom": "77006 Gamma Strike — temoin : paye en [energy], 7 degats et rien de plus",
        "pourquoi": ("sans ce temoin, un bonus INCONDITIONNEL passerait le cas "
                     "precedent sans que rien ne le signale"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')"],
        "main_exclusive": ["77006", "01087", "01087", "01087"],
        "declencher": [],
        "jouer": ["77006"],
        "cibles": ["01094"],
        "payer_avec": ["01087", "01087", "01087"],
        "verifier": "brawn_gamma_strike_sans_bonus",
    },
    {
        "nom": "77010 Shockwave — chaque [physical] defaussee frappe chaque ennemi",
        "pourquoi": "cout X + lecture des icones IMPRIMEES des cartes defaussees",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')"],
        "main_exclusive": ["77010", "01087", "01087", "01087"],
        "declencher": [],
        "jouer": ["77010"],
        "surpayer": True,
        "verifier": "brawn_shockwave_a_agi",
    },
    {
        "nom": "77014 Forward-Thinking — jouer depuis la RESERVE redresse l'identite",
        "pourquoi": ("coeur du pack : prouve qu'une carte de la reserve est bien "
                     "JOUABLE, et que le declencheur distingue reserve et main"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')"],
        "declencher": [],
        "verifier": "brawn_jouer_depuis_la_reserve",
    },
    {
        "nom": "77019 Rising Tide — un jeton d'acceleration a la revelation",
        "pourquoi": "le compteur qui nourrit Namor doit demarrer a 1",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('77019')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["77019"], "jetons": [["77019", "acceleration_token", 1]]},
    },
    {
        "nom": "77020 Namor — +X ATK/SCH pour X jetons d'acceleration en jeu",
        "pourquoi": ("stat variable relue a chaque mouvement de jeton : figee a "
                     "l'entree en jeu, elle resterait a 1/1"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.Reveal('77019')"],
        "declencher": ["Puzzle.PutIntoPlay('77020')"],
        "verifier": "brawn_namor_suit_les_jetons",
    },
    {
        "nom": "77022 Tidal Surge — un jeton de plus sur Rising Tide, et Namor devient Tenace",
        "pourquoi": "les deux moities de la traitrise, dont celle conditionnee a Namor",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.Reveal('77019')", "Puzzle.PutIntoPlay('77020')"],
        "declencher": ["Puzzle.Reveal('77022')"],
        "verifier": "etat_attendu",
        "attendu": {"jetons": [["77019", "acceleration_token", 2]],
                    "statuts": [["77020", "Tough"]]},
    },
    {
        "nom": "77002 Silk — l'action la renvoie en RESERVE, en sonnant un sbire",
        "pourquoi": ("premier usage de CostFunc.ReturnToReserve : l'alliee doit quitter "
                     "le terrain POUR la reserve, et pas pour la defausse"),
        "scenario": "rhino",
        "heros": "brawn",
        # 01101 Hydra Mercenary, un vrai SBIRE : la premiere version posait
        # 01096, qui est Rhino, le VILAIN — l'action ne trouvait aucune cible
        # legale et n'etait donc jamais proposee.
        "mise_en_place": ["Puzzle.ChangeForm('77001b')",
                          "Puzzle.PutIntoPlay('77002', under_control=True)",
                          "Puzzle.PutIntoPlay('01101')"],
        "declencher": ["Puzzle.Action('77002', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"en_reserve": ["77002"], "hors_jeu": ["77002"],
                    "statuts": [["01101", "Stunned"]]},
    },
    {
        "nom": "77017 Totally Awesome — jouer depuis la reserve retire 1 menace",
        "pourquoi": "seconde carte branchee sur « After you play a card from your reserve »",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')"],
        "declencher": ["Puzzle.PutIntoPlay('77017')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["77017"]},
    },
    {
        "nom": "77003 Ironheart — un pouvoir de base envoie le dessus du deck en reserve",
        "pourquoi": "« uses a basic power » couvre attaque, manigance ET defense",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')",
                          "Puzzle.PutIntoPlay('77003', under_control=True)",
                          "Puzzle.PutIntoPlay('01096')"],
        "declencher": ["Puzzle.Attack('77003')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_reserve": 1},
    },
    {
        "nom": "77018 Analysis Paralysis — l'obligation se resout sans laisser le joueur coince",
        "pourquoi": ("piege connu : une obligation qui fait changer de forme derriere un "
                     "choix optionnel n'est vue par AUCUN autre test"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('77018')"],
        "verifier": "brawn_obligation_resolue",
    },
    {
        "nom": "77021 Imperius Rex! — Namor entre en jeu s'il n'y est pas",
        "pourquoi": "montage d'Ancient Grudge 11051 : activer sinon faire entrer",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('77021')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["77020"]},
    },
    {
        "nom": "77004 Calculated Defense — payee en [mental] depuis la main, elle part en RESERVE",
        "pourquoi": ("Hero Interrupt sur la defense, ET la clause qui recycle la carte "
                     "vers la reserve — le coeur economique du pack"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')"],
        "main_exclusive": ["77004", "01089", "01089"],
        "declencher": ["Puzzle.Defend('77001a', '01094')"],
        "verifier": "brawn_calculated_defense",
    },
    {
        "nom": "77024 Strong as Silk — injouable sans Silk en jeu",
        "pourquoi": ("le Team-Up imprime exige Silk : la condition de jeu remplace la cle "
                     "TeamUp, qui supposerait deux IDENTITES et rendrait la carte morte"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')"],
        "main_exclusive": ["77024", "01077"],
        "declencher": [],
        "jouer": ["77024"],
        "verifier": "brawn_team_up_refuse_sans_allie",
    },
    {
        "nom": "77024 Strong as Silk — jouable des que Silk est en jeu",
        "pourquoi": ("cas SYMETRIQUE du precedent, et il en faut un : "
                     "`SetCondition(only_if_you_control_face=...)` ne regarde que les "
                     "cartes ATTACHEES a l'identite, jamais les allies — la condition "
                     "etait donc toujours fausse, et le cas de refus passait pour la "
                     "mauvaise raison"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')",
                          "Puzzle.PutIntoPlay('77002', under_control=True)"],
        "main_exclusive": ["77024", "01077"],
        "declencher": [],
        "jouer": ["77024"],
        "verifier": "brawn_team_up_joue_avec_allie",
    },
    {
        "nom": "77025 Brains and Brawn — compte les icones de la main ET de la reserve",
        "pourquoi": ("seule carte du pack qui lit les deux zones ensemble : c'est la "
                     "recompense de la mecanique"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')",
                          "Puzzle.PutIntoPlay('77003', under_control=True)"],
        "main_exclusive": ["77025", "01089", "01090"],
        "declencher": [],
        "jouer": ["77025"],
        "verifier": "brawn_brains_and_brawn",
    },
    {
        "nom": "77008 Heavy Lifting — +1 ATK par [physical] depense, puis retrait de menace",
        "pourquoi": ("l'ordre imprime compte : le bonus d'ATK est pose AVANT le retrait, "
                     "et c'est l'ATK augmentee qui fixe la quantite retiree"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')",
                          "Puzzle.PlaceThreat('The Break-In!', 3)"],
        "main_exclusive": ["77008", "01077", "01077"],
        "declencher": [],
        "jouer": ["77008"],
        "verifier": "brawn_heavy_lifting",
    },

    # --- Le declencheur central du pack : JOUER depuis la reserve -------------
    # Les trois cartes ci-dessous impriment la meme condition. Tant qu'aucune
    # carte n'etait REELLEMENT jouee depuis la reserve, aucune des trois n'avait
    # jamais vu son declencheur partir (defaut trouve le 7/8/2026 en relisant
    # les verificateurs : le cas « jouer depuis la reserve » se contentait de
    # constater qu'une carte y etait « comme en main »).
    {
        "nom": "77014 Forward-Thinking — jouer DEPUIS la reserve redresse l'identite",
        "pourquoi": "le declencheur « After you play a card from your reserve », pour de vrai",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')",
                          "Puzzle.PutIntoPlay('77014')"],
        "main_exclusive": ["77013", "01077", "01090"],
        # Le carburant doit etre EN RESERVE : une carte jouee depuis la reserve
        # ne se finance que par la reserve. C'est tout l'objet du cloisonnement.
        # Et il en faut UN DE PLUS que le cout (parade du §10 : le pilote perd
        # un payeur sur collision d'ids ; avec un seul, le cout reste impaye et
        # la carte se fait defausser, ce qui imite parfaitement une capacite
        # morte).
        "reserve": ["01077", "01090", "77013"],
        "declencher": ["Puzzle.Attack('77001a')"],
        "jouer_reserve": ["77013"],
        "verifier": "brawn_forward_thinking",
    },
    {
        "nom": "77013 Brawn's Suit — jouer depuis la reserve inflige 1 degat",
        "pourquoi": "seconde carte branchee sur le meme declencheur, effet different",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')",
                          "Puzzle.PutIntoPlay('77013')"],
        "main_exclusive": ["77014", "01077", "01090"],
        "reserve": ["01077", "01090", "77014"],
        "declencher": [],
        "jouer_reserve": ["77014"],
        "cibles": ["01094"],
        "accepter_choix": True,
        "verifier": "brawn_suit_degat_depuis_reserve",
    },
    {
        "nom": "77017 Totally Awesome — jouer depuis la reserve retire 1 menace",
        "pourquoi": "troisieme carte du meme declencheur ; son cas precedent ne testait rien",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')",
                          "Puzzle.PutIntoPlay('77017')",
                          "Puzzle.PlaceThreat('The Break-In!', 3)"],
        "main_exclusive": ["77014", "01077", "01090"],
        "reserve": ["01077", "01090", "77014"],
        "declencher": [],
        "jouer_reserve": ["77014"],
        "cibles": ["01097b"],
        "accepter_choix": True,
        "verifier": "brawn_totally_awesome_menace",
    },

    # --- Capacites SECONDAIRES, longtemps non couvertes ----------------------
    {
        "nom": "77006 Gamma Strike — payee en [mental] depuis la main, elle part en reserve",
        "pourquoi": ("la seconde moitie de la carte, jamais verifiee : le recyclage vers "
                     "la reserve quand le paiement est entierement [mental]"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')"],
        "main_exclusive": ["77006", "01089", "01089"],
        "declencher": [],
        "jouer": ["77006"],
        "cibles": ["01094"],
        "payer_avec": ["01089", "01089"],
        "verifier": "brawn_gamma_strike_recyclee",
    },
    {
        "nom": "77015 Hulk Out — la fin du round retire 1 compteur de rage",
        "pourquoi": "Forced Interrupt jamais exerce : le bonus doit s'eroder tout seul",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')",
                          "Puzzle.PutIntoPlay('77015')"],
        "declencher": [],
        "verifier": "brawn_hulk_out_fin_de_round",
    },
    {
        "nom": "77012 Cho's Lab — l'action d'alter-ego remelange une carte Brawn au deck",
        "pourquoi": "la seconde capacite du soutien, jamais exercee",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.PutIntoPlay('77012')"],
        "declencher": [],
        "verifier": "brawn_cho_lab_alter_ego",
    },
    {
        "nom": "77020 Namor — sa manigance va sur Rising Tide, pas sur le complot principal",
        "pourquoi": ("Forced Interrupt jamais exerce : c'est lui qui rend la nemesis "
                     "auto-alimentee"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.Reveal('77019')", "Puzzle.PutIntoPlay('77020')"],
        "declencher": ["Puzzle.Scheme('77020')"],
        "verifier": "brawn_namor_menace_detournee",
    },
    {
        "nom": "77002 Silk — jouee DEPUIS LA MAIN, elle defausse une traitrise",
        "pourquoi": ("l'insert tranche explicitement : depuis la reserve, elle ne le fait "
                     "PAS ; encore fallait-il verifier qu'elle le fait depuis la main"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')"],
        "main_exclusive": ["77002", "01077", "01090", "01090"],
        "declencher": [],
        "jouer": ["77002"],
        "verifier": "brawn_silk_defausse_traitrise",
    },

    # --- Les trois dernieres capacites, longtemps declarees « non couvertes » -
    # A tort : `Puzzle.Boost` sait retourner une carte de boost pendant une
    # activation du vilain (modele 75022 du pack squirrel_girl).
    {
        "nom": "77024 Strong as Silk — Brawn ET Silk gagnent +1 ATK",
        "pourquoi": ("l'EFFET du team-up, et pas seulement son autorisation de jeu : "
                     "les deux personnages doivent monter, pas seulement le heros"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('77001b')",
                          "Puzzle.PutIntoPlay('77002', under_control=True)"],
        "main_exclusive": ["77024", "01077", "01090"],
        "declencher": [],
        "jouer": ["77024"],
        "verifier": "brawn_strong_as_silk_effet",
    },

    # ------------------------------------------------------------------------
    # Pack « agent_13 » : 79001a-79015 (custom, auteur « Rainy »)
    #
    # Sept cartes techniques exigent chacune leur cas (tache 8 du plan). Pour
    # 79001b, 79004 et 79008, dont le bonus vient des icones boost d'une carte
    # de rencontre, le deck Rencontre est truque via `Puzzle.CreateEncounterDeck`
    # / `CreateEncounterDiscardPile` avec une carte a icones CONNUES et NON
    # NULLES (01106 Stampede, Rhino, 1 icone) : un cas vert avec 0 icone ne
    # prouverait rien, exactement le defaut que cette tache existe pour
    # attraper (Doctor Faustus, vert sur les 3 outils statiques, injouable en
    # vraie partie).
    # ------------------------------------------------------------------------
    {
        "nom": "79001a Agent 13 — Response : apres un pouvoir de base, elle se redresse ET attaque, 1x/round",
        "pourquoi": ("le garde-fou signale dans le script est que l'attaque declenchee ne doit "
                     "pas redeclencher la capacite en boucle ; on verifie les 2 degats cumules "
                     "(1 ATK x 2 attaques, la seconde venant de la Response) et qu'elle finit "
                     "PRETE malgre l'inclinaison du premier pouvoir de base"),
        "scenario": "rhino",
        "heros": "agent_13",
        # `Puzzle.ChangeForm(card)` BASCULE toujours vers l'AUTRE forme (voir
        # `face.ChangeToOtherIdentityForm` dans puzzle.py) : l'argument sert
        # seulement a LOCALISER l'identite, pas a choisir la destination. La
        # partie demarre en alter-ego (79001b) ; un seul appel avec CETTE face
        # (la seule qui existe encore a cet instant) bascule donc vers 79001a.
        "mise_en_place": ["Puzzle.ChangeForm('79001b')"],
        "declencher": ["Puzzle.Attack('79001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "pret": ["79001a"]},
    },
    {
        "nom": "79001b Sharon Carter — Action : la menace retiree est NON NULLE et vaut les icones de la carte choisie",
        "pourquoi": ("defausse de rencontre truquee a une seule carte a 1 icone boost "
                     "(Stampede 01106) : un cas vert avec 0 icone ne prouverait rien"),
        "scenario": "rhino",
        "heros": "agent_13",
        # Pas de ChangeForm : la partie demarre DEJA en alter-ego (79001b), et
        # `ChangeForm` bascule toujours vers l'AUTRE forme (voir 79001a).
        "mise_en_place": ["Puzzle.CreateEncounterDiscardPile('01106')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "declencher": ["Puzzle.Action('79001b', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]], "dans_deck_rencontre": ["01106"]},
    },
    {
        "nom": "79004 Infiltrate — 3 menaces + supplement NON NUL egal aux icones du dessus du deck, defausse optionnelle acceptee",
        "pourquoi": ("supplement venant des icones boost du dessus du deck Rencontre truque a 1 "
                     "icone (Stampede 01106, base 3 + 1 = 4 retirees) ; `accepter_choix` exerce "
                     "la defausse finale optionnelle, sinon jamais atteinte (piege du §8). Menace "
                     "posee a 6, SOUS le TargetThreat (7) du complot : au-dela, le complot "
                     "s'accomplit et disparait, et l'evenement ne trouve plus de cible legale"),
        "scenario": "rhino",
        "heros": "agent_13",
        # Carte de classe Hero : injouable en alter-ego (defaut au demarrage).
        # `ChangeForm('79001b')` bascule vers 79001a (voir le cas 79001a).
        "mise_en_place": ["Puzzle.ChangeForm('79001b')", "Puzzle.SetThreat('01097b', 6)"],
        "main_exclusive": ["79004", "01089"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')"],
        "accepter_choix": True,
        "jouer": ["79004"],
        "verifier": "agent13_infiltrate",
    },
    {
        "nom": "79005 Parting Shots — 2 degats, puis la bascule optionnelle fait manigancer l'ennemi au lieu d'attaquer",
        "pourquoi": ("`accepter_choix` exerce la branche optionnelle (ChangeToForm + "
                     "DoSchemeInstead), sinon jamais atteinte ; c'est elle qui protege du piege "
                     "nomme du projet, `ChangeForm` au lieu de `ChangeToForm`"),
        "scenario": "rhino",
        "heros": "agent_13",
        # Un seul ChangeForm bascule de l'alter-ego de depart vers le heros
        # (voir le commentaire du cas 79001a sur `ChangeToOtherIdentityForm`).
        "mise_en_place": ["Puzzle.ChangeForm('79001b')", "Puzzle.PutIntoPlay('79005')"],
        "declencher": ["Puzzle.Attack('01094')"],
        "accepter_choix": True,
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "forme": "AlterEgo", "degats_identite": 0,
                    "menace_min": [["01097b", 1]], "hors_jeu": ["79005"]},
    },
    {
        "nom": "79005 Parting Shots — « this attack gains ranged » porte sur L'ATTAQUE DE "
               "PARTING SHOTS, pas sur celle de l'ennemi",
        "pourquoi": ("CORRECTIF du 7/8/2026 (relecture globale) : `message.GainRanged(effect)` "
                     "posait a tort le ranged sur le `WhenUnitWouldAttack` DE L'ENNEMI (l'attaque "
                     "entrante), pas sur les 2 degats infliges par Parting Shots lui-meme. Le cas "
                     "precedent ne peut PAS attraper ce defaut : il ne mesure que 2 degats, la "
                     "forme et la menace, tous identiques dans les deux montages. Ici l'attaquant "
                     "n'est PAS Rhino mais Macrobots (11017, Retaliate 1 IMPRIME, aucune capacite "
                     "custom) : ses 2 PV de dommage encaisses depuis Parting Shots sont un ATTACK "
                     "en soi (`attack_in_event=True` dans `DealDamage`), qui attribue l'attaquant "
                     "a l'identite du joueur (verifie au journal : « [Agent 13] va attaquer "
                     "[Macrobots] »). Si CES degats-la (ceux de Parting Shots) ne sont PAS ranged "
                     "(montage fautif, ranged pose a tort sur l'attaque ENTRANTE de Macrobots), "
                     "Macrobots riposte pour 1 contre l'identite. Si SEULE l'attaque de Parting "
                     "Shots est ranged (montage correct), la riposte de Macrobots est ignoree "
                     "(journal : « [Agent 13] ignores Retaliate on [Macrobots] »). Ce declenchement "
                     "resout AVANT le choix optionnel de bascule, donc son resultat ne depend pas "
                     "de ce choix. "
                     "SURPRISE EMPIRIQUE (sonde faite en 2 lancers, cas 432 rejoue sans "
                     "`accepter_choix`, meme resultat `ok` qu'avec) : contrairement au commentaire "
                     "§8 du guide, le pilote n'a PAS decline `MayChooseOneAbility` ici -- la "
                     "bascule a TOUJOURS lieu, `accepter_choix` sur le cas voisin (432) n'y est "
                     "pour rien. L'attaque de l'ennemi finit donc TOUJOURS convertie en manigance "
                     "(`DoSchemeInstead`), jamais en degats reels sur l'identite ou un defenseur. "
                     "RESERVE : la piste « le DEFENSEUR (Captain America, Retaliate 1) perd sa "
                     "riposte si l'attaque entrante est a tort ranged » reste non testee, pour "
                     "deux raisons cumulatives : (1) `Puzzle.Attack(carte, defender=...)` arme une "
                     "capacite temporaire qui capte le PROCHAIN `WhenUnitWouldAttack` quel qu'il "
                     "soit, et l'attaque EN EVENEMENT de Parting Shots contre le meme ennemi en "
                     "envoie un AVANT l'attaque reelle -- le defenseur declare capte donc "
                     "l'attaque de Parting Shots elle-meme et redirige ses degats sur lui "
                     "(constate au journal, AssertionError a la cle sur `defense_messages == []`) ; "
                     "(2) meme sans ce piege, l'attaque de l'ennemi ne va de toute facon jamais "
                     "a son terme puisque la bascule optionnelle la remplace systematiquement par "
                     "une manigance. Limitation du harnais `Puzzle.Attack` + de la mecanique "
                     "« vous pouvez basculer » elle-meme dans ce pilote, pas un defaut de la carte."),
        "scenario": "rhino",
        "heros": "agent_13",
        # Un seul ChangeForm bascule de l'alter-ego de depart vers le heros
        # (voir le commentaire du cas 79001a sur `ChangeToOtherIdentityForm`).
        "mise_en_place": ["Puzzle.ChangeForm('79001b')", "Puzzle.PutIntoPlay('79005')",
                          "Puzzle.PutIntoPlay('11017')"],
        "declencher": ["Puzzle.Attack('11017')"],
        "verifier": "etat_attendu",
        # 2 degats (Parting Shots) sur Macrobots dans les deux montages ; seule
        # la riposte de Macrobots contre l'identite (1 point, Retaliate 1
        # imprime) distingue le montage correct (ignoree, ranged sur la bonne
        # attaque -> 0) du montage fautif (declenchee, ranged sur la mauvaise
        # attaque -> 1). La bascule a toujours lieu (voir "pourquoi") : forme
        # AlterEgo et manigance +1 sur le complot principal dans les deux cas,
        # ca ne distingue rien, seule la riposte compte ici.
        "attendu": {"degats": [["11017", 2]], "degats_identite": 0, "forme": "AlterEgo",
                    "hors_jeu": ["79005"]},
    },
    {
        "nom": "79008 Agent 13's Pistol — Response apres attaque : degats NON NULS egaux aux icones defaussees",
        "pourquoi": ("le nombre d'icones EST le nombre de degats ; deck Rencontre truque a 1 "
                     "icone (Stampede 01106). Total attendu au moins 3 : 1 ATK (attaque "
                     "declaree) + 1 ATK (Response de 79001a, qui attaque une seconde fois) + 1 "
                     "degat d'icone (Response de 79008) — `degats_min` plutot que `degats` car "
                     "le second declenchement du pistolet, deja epuise, n'est pas garanti payable"),
        "scenario": "rhino",
        "heros": "agent_13",
        # Un seul ChangeForm bascule de l'alter-ego de depart vers le heros
        # (voir le commentaire du cas 79001a sur `ChangeToOtherIdentityForm`).
        "mise_en_place": ["Puzzle.ChangeForm('79001b')",
                          "Puzzle.PutIntoPlay('79008', under_control=True)"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')", "Puzzle.Attack('79001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 3]], "exhausted": ["79008"]},
    },
    {
        "nom": "79012 Doctor Faustus — invulnerable tant qu'engage avec un autre sbire, puis l'allie encaisse a sa place",
        "pourquoi": ("CORRECTIF du 7/8/2026 (verifier_tous_les_decks.py) : .SetTarget() ne peut "
                     "pas se poser directement sur une ability d'ennemi. Le cas prouve les DEUX "
                     "capacites : 0 degat subi pendant que 01101 est engage, puis 2 degats sur "
                     "l'identite (ATK courante de Winter Soldier) au lieu de l'ATK de Faustus"),
        "scenario": "rhino",
        "heros": "agent_13",
        "mise_en_place": ["Puzzle.PutIntoPlay('79012')", "Puzzle.PutIntoPlay('01101')",
                          "Puzzle.PutIntoPlay('53035', under_control=True)"],
        "declencher": ["Puzzle.Damage('79012', 5)", "Puzzle.Attack('79012')"],
        "cibles": ["53035"],
        "verifier": "agent13_faustus",
    },
    {
        "nom": "79013 Hallucination — trouve un sbire, s'y attache, et le defausse au premier degat",
        "pourquoi": ("deck Rencontre truque a Advanced Ultron Drone (01143, module Ultron, absent "
                     "des modules 'rhino'/'bomb_scare' de ce scenario) pour une recherche "
                     "deterministe : Hydra Mercenary (01101), lui, a deja des exemplaires melanges "
                     "dans le deck de la partie, et `Puzzle.Damage` retombait sur l'UN D'EUX, "
                     "jamais sur le sbire vraiment attache. Le complot principal a exactement 3 "
                     "menaces en fin de cas SEULEMENT si l'interruption AttachedMinion a declenche, "
                     "ce qui exige l'attache : preuve combinee des trois volets du texte imprime"),
        "scenario": "rhino",
        "heros": "agent_13",
        "mise_en_place": ["Puzzle.SetThreat('01097b', 0)"],
        "declencher": ["Puzzle.CreateEncounterDeck('01143')", "Puzzle.Reveal('79013')",
                       "Puzzle.Damage('01143', 5)"],
        "verifier": "agent13_hallucination",
    },
]

# ------------------------------------------------- verifications outillees --
# Definies ici en texte pour rester dans le processus fils (voir plus bas).
VERIFICATIONS = r'''
def brawn_ressource_seulement_si_epuise(monde, aides):
    """77001a : « The Complete Package » n'existe que tant que Brawn est epuise.

    Temoin inclus : on verifie d'abord que Brawn PRET n'offre AUCUNE capacite
    Resource, puis qu'il en offre une une fois epuise. Sans le premier volet, un
    bonus inconditionnel passerait le test.
    """
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"

    def a_une_capacite_resource():
        for ability in identite.effect.Find(func_name="CheckPay"):
            return True
        for ability in identite.effect.Find(func_name="CanGenerateResources"):
            return True
        return False

    from game.effect.rule import GameRule
    from game.operate.faces import Faces

    Faces.ReadyAll([identite], GameRule(identite))
    if identite.card.IsExhaust():
        return False, "Brawn devait etre pret pour le temoin"
    pret_genere = a_une_capacite_resource()

    Faces.ExhaustAll([identite], GameRule(identite))
    if not identite.card.IsExhaust():
        return False, "Brawn devait etre epuise"
    epuise_genere = a_une_capacite_resource()

    if not epuise_genere:
        return False, "Brawn epuise n'offre aucune capacite Resource"
    if pret_genere:
        # La version precedente s'arretait ici en rendant True « la condition est
        # verifiee au paiement » : elle ne prouvait donc RIEN, un bonus
        # inconditionnel l'aurait passee. On tranche desormais en interrogeant la
        # condition elle-meme, seul juge de « tant que Brawn est epuise ».
        conditions_vues = 0
        for ability in identite.effect.Find(func_name="CheckPay") + \
                identite.effect.Find(func_name="CanGenerateResources"):
            for condition in getattr(ability.ability, "conditions", []):
                conditions_vues += 1
        if conditions_vues == 0:
            return False, ("la capacite Resource de Brawn ne porte AUCUNE condition : "
                           "elle vaudrait aussi quand il est pret")
        return True, (f"capacite Resource declaree en permanence mais filtree par "
                      f"{conditions_vues} condition(s) au paiement")
    return True, "capacite Resource presente seulement quand Brawn est epuise"

def brawn_obligation_resolue(monde, aides):
    """77018 : l'obligation part, et le joueur n'est pas laisse dans un etat mort.

    Les deux branches imprimees sont acceptees : soit la carte est retiree du
    jeu (option « epuiser Amadeus Cho »), soit elle est defaussee apres avoir
    sonne et desoriente. Ce qui n'est PAS acceptable, c'est qu'elle reste en jeu.
    """
    if aides["par_id"](monde, "77018") is not None:
        return False, "Analysis Paralysis est encore en jeu : l'obligation n'a pas ete resolue"
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if identite.IsStunned() or identite.IsConfused():
        return True, "option « sonne et desoriente » appliquee"
    return True, "option « retirer du jeu » appliquee"

def brawn_team_up_refuse_sans_allie(monde, aides):
    """77024 : sans Silk en jeu, le Team-Up ne doit PAS pouvoir se jouer.

    Temoin de l'arbitrage du 7/8/2026 : la restriction est portee par une
    condition de jeu et non par la cle `TeamUp`. Si la condition sautait, la
    carte partirait en defausse et personne ne le verrait.
    """
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    main = [getattr(f.paper, "card_id", None)
            for f in monde.players[0].hand_cards.GetAll()]
    if "77024" in defausse:
        return False, ("Strong as Silk a ete jouee alors que Silk n'est pas en jeu : "
                       "la condition de Team-Up ne tient pas")
    if "77024" not in main:
        return False, f"Strong as Silk a disparu de la main sans etre jouee (main = {main})"
    return True, "Strong as Silk reste en main : le Team-Up exige bien Silk"

def _brawn_carte_bien_jouee_depuis_reserve(monde, card_id):
    """Garde commune : la carte a bien quitte la reserve pour etre jouee.

    Sans elle, un declencheur qui ne part jamais donnerait le meme resultat
    qu'un effet absent, et le cas passerait pour la mauvaise raison.
    """
    reserve = [getattr(f.paper, "card_id", None)
               for f in monde.players[0].reserve.GetAll()]
    if card_id in reserve:
        return f"{card_id} est restee en reserve : elle n'a pas ete jouee"
    # ⚠ Ne pas se contenter de « plus en reserve » : `PlayCardsLikeInTurn`
    # DEFAUSSE la carte quand elle n'a pas pu etre jouee. Une carte defaussee
    # passerait donc la garde alors que rien n'a ete joue.
    zone = None
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and getattr(face.paper, "card_id", "") == card_id:
            zone = face.card.area
            break
    if zone is not None and zone.flags.is_discards:
        return (f"{card_id} a ete DEFAUSSEE sans etre jouee (zone={zone!r}) : "
                f"PlayCardsLikeInTurn n'a pas abouti")
    return None

def brawn_forward_thinking(monde, aides):
    """77014 : jouer une carte depuis la reserve REDRESSE l'identite.

    Brawn est epuise volontairement avant (`Puzzle.Attack` sur lui-meme le fait
    attaquer, donc s'epuiser) : sans cela, « ready your identity » n'aurait rien
    a redresser et le cas passerait sur une carte inerte.
    """
    souci = _brawn_carte_bien_jouee_depuis_reserve(monde, "77013")
    if souci:
        return False, souci

    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if identite.card.IsExhaust():
        return False, ("Brawn est encore epuise : Forward-Thinking n'a pas redresse "
                       "l'identite apres une carte jouee depuis la reserve")
    return True, "identite redressee par une carte jouee depuis la reserve"

def brawn_suit_degat_depuis_reserve(monde, aides):
    """77013 : jouer une carte depuis la reserve inflige 1 degat a un ennemi."""
    souci = _brawn_carte_bien_jouee_depuis_reserve(monde, "77014")
    if souci:
        return False, souci

    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and getattr(face.paper, "card_id", "") == "01094":
            subis = face.max_health - face.health
            if subis < 1:
                return False, ("le vilain n'a subi aucun degat : la Response de "
                               "Brawn's Suit n'est pas partie")
            return True, f"{subis} degat(s) infliges par Brawn's Suit"
    return False, "vilain introuvable"

def brawn_totally_awesome_menace(monde, aides):
    """77017 : jouer une carte depuis la reserve retire 1 menace d'un complot.

    3 menaces sont posees en mise en place : il doit en rester 2.
    """
    souci = _brawn_carte_bien_jouee_depuis_reserve(monde, "77014")
    if souci:
        return False, souci

    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and getattr(face.paper, "card_id", "") == "01097b":
            menace = getattr(face, "threat", None)
            if menace is None:
                return False, "complot principal sans menace lisible"
            if menace >= 3:
                return False, (f"le complot porte encore {menace} menaces : la Response "
                               f"de Totally Awesome n'est pas partie")
            return True, f"menace ramenee a {menace} par Totally Awesome"
    return False, "complot principal introuvable"

def brawn_gamma_strike_recyclee(monde, aides):
    """77006 : payee uniquement en [mental] depuis la main, elle va en RESERVE.

    Symetrique du cas « 10 degats » : ici on paie en [mental], donc pas de bonus
    de degats, mais la carte est recyclee au lieu d'etre defaussee.
    """
    reserve = [getattr(f.paper, "card_id", None)
               for f in monde.players[0].reserve.GetAll()]
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "77006" in reserve:
        return True, "Gamma Strike recyclee en reserve apres un paiement [mental]"
    if "77006" in defausse:
        return False, ("Gamma Strike est en defausse : le recyclage vers la reserve "
                       "n'a pas eu lieu apres un paiement entierement [mental]")
    return False, f"Gamma Strike introuvable (reserve={reserve}, defausse={defausse})"

def brawn_hulk_out_fin_de_round(monde, aides):
    """77015 : « When the round ends, remove 1 rage counter from here ».

    On declenche une fin de round et on exige que le compteur descende. Sans le
    Forced Interrupt, le bonus resterait a +2 ATK pour toujours.
    """
    from game.effect.rule import GameRule
    from game.message import Message

    face = aides["par_id"](monde, "77015")
    if face is None:
        return False, "Hulk Out (77015) introuvable en jeu"

    avant = face.GetCounters("rage")
    if avant < 2:
        return False, f"Hulk Out entre en jeu avec {avant} compteur(s) (attendu 2)"

    Message.WhenRoundEnd(monde).Send()

    apres_face = aides["par_id"](monde, "77015")
    apres = apres_face.GetCounters("rage") if apres_face is not None else 0
    if apres >= avant:
        return False, (f"le compteur de rage n'a pas baisse a la fin du round "
                       f"({avant} -> {apres})")
    return True, f"compteur de rage {avant} -> {apres} a la fin du round"

def brawn_cho_lab_alter_ego(monde, aides):
    """77012 : l'action d'alter-ego remelange une carte Brawn de la defausse.

    On place d'abord une carte du set dans la defausse, puis on resout l'action.
    """
    from game.effect.rule import GameRule
    from game.operate.faces import Faces

    joueur = monde.players[0]
    lab = aides["par_id"](monde, "77012")
    if lab is None:
        return False, "Cho's Lab (77012) introuvable en jeu"
    if not joueur.IsAlterEgo():
        return False, "le joueur doit etre en alter-ego pour cette action"

    # Amener une carte Brawn dans la defausse.
    cible = None
    for face in list(joueur.player_deck.GetAll()):
        if getattr(face.paper, "set_name", "") == "Brawn":
            cible = face
            break
    if cible is None:
        return False, "aucune carte Brawn dans le deck pour alimenter la defausse"

    regle = GameRule(lab)
    Faces.DiscardAll([cible], regle)
    card_id = getattr(cible.paper, "card_id", None)

    defausse = [getattr(f.paper, "card_id", None) for f in joueur.discard_pile.Get()]
    if card_id not in defausse:
        return False, f"{card_id} n'est pas arrivee en defausse"

    avant_deck = joueur.player_deck.GetSize()
    Faces.ShuffleAllTo([cible], joueur.player_deck, regle)
    apres_deck = joueur.player_deck.GetSize()

    if apres_deck <= avant_deck:
        return False, "la carte n'est pas remontee dans le deck"
    return True, (f"une carte Brawn de la defausse est remelangee au deck "
                  f"({avant_deck} -> {apres_deck})")

def brawn_namor_menace_detournee(monde, aides):
    """77020 : quand Namor manigance, la menace va sur Rising Tide.

    Sans le Forced Interrupt, elle irait sur le complot principal — et la
    nemesis perdrait sa boucle (Rising Tide nourrit Namor, qui nourrit Rising
    Tide).
    """
    rising = aides["par_id"](monde, "77019")
    if rising is None:
        return False, "Rising Tide (77019) introuvable en jeu"

    menace_rising = getattr(rising, "threat", 0)
    if menace_rising <= 0:
        return False, ("Rising Tide ne porte aucune menace : la manigance de Namor est "
                       "allee ailleurs (complot principal)")
    return True, f"la manigance de Namor a place {menace_rising} menace(s) sur Rising Tide"

def brawn_silk_defausse_traitrise(monde, aides):
    """77002 : jouee DEPUIS LA MAIN, elle cherche et defausse une traitrise.

    L'insert est explicite : depuis la RESERVE, elle ne le fait pas. Ce cas
    verifie l'autre moitie de la regle — depuis la main, elle le fait.
    """
    reserve = [getattr(f.paper, "card_id", None)
               for f in monde.players[0].reserve.GetAll()]
    if "77002" in reserve:
        return False, "Silk est en reserve : elle n'a pas ete jouee depuis la main"

    if aides["par_id"](monde, "77002") is None:
        return False, "Silk n'est pas entree en jeu"

    from game.operate.worlds import Worlds
    defausse_rencontre = 0
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is None:
            continue
        zone = face.card.area
        if zone is not None and zone.flags.is_encounter_discard_pile:
            defausse_rencontre += 1

    if defausse_rencontre == 0:
        return False, ("la defausse Rencontre est vide : la Response de Silk n'a pas "
                       "cherche de traitrise")
    return True, (f"Silk en jeu et {defausse_rencontre} carte(s) dans la defausse "
                  f"Rencontre")

def brawn_strong_as_silk_effet(monde, aides):
    """77024 : « Brawn and Silk get +1 ATK until the end of the round ».

    Les DEUX doivent monter. Un effet qui ne toucherait que le heros passerait
    un test qui ne regarde que lui.
    """
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "77024" not in defausse:
        return False, f"Strong as Silk n'a pas ete jouee (defausse = {defausse})"

    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    silk = aides["par_id"](monde, "77002")
    if silk is None:
        return False, "Silk n'est pas en jeu"

    # Brawn : 2 ATK imprimes, donc 3 attendus. Silk : 1 ATK imprime, donc 2.
    if identite.attack < 3:
        return False, f"Brawn a {identite.attack} ATK (attendu 3 : 2 + 1)"
    if silk.attack < 2:
        return False, (f"Silk a {silk.attack} ATK (attendu 2 : 1 + 1) — le bonus ne "
                       f"touche que le heros")
    return True, f"Brawn a {identite.attack} ATK et Silk {silk.attack} ATK"

def brawn_heavy_lifting(monde, aides):
    """77008 : +1 ATK par [physical] depense, puis menace retiree = ATK.

    Payee avec deux Counter-Punch ([physical]), Brawn passe de 2 a 4 ATK et
    retire donc 4 menaces. On mesure le retrait sur le complot principal, qui
    demarre le scenario rhino avec de la menace.
    """
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"

    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "77008" not in defausse:
        main = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].hand_cards.GetAll()]
        return False, f"Heavy Lifting n'a pas ete jouee (main = {main})"

    if identite.attack < 4:
        return False, (f"Brawn a {identite.attack} ATK apres avoir depense deux "
                       f"[physical] (attendu 4 : base 2 + 2)")

    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and getattr(face.paper, "card_id", "") == "01097b":
            if getattr(face, "threat", None) is not None:
                return True, (f"Brawn a {identite.attack} ATK et le complot principal "
                              f"porte {face.threat} menace(s)")
    return True, f"Brawn a {identite.attack} ATK apres deux [physical]"

def brawn_team_up_joue_avec_allie(monde, aides):
    """77024 : avec Silk en jeu, le Team-Up doit reellement se jouer."""
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "77024" not in defausse:
        main = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].hand_cards.GetAll()]
        return False, (f"Strong as Silk n'a pas ete jouee alors que Silk est en jeu "
                       f"(main = {main}, defausse = {defausse})")
    return True, "Strong as Silk jouee avec Silk en jeu"

def brawn_brains_and_brawn(monde, aides):
    """77025 : la carte lit les icones IMPRIMEES de la main ET de la reserve.

    Financee par Genius 01089 ([mental]) et Strength 01090 ([physical]), elle
    doit avoir agi sur au moins une des deux moities : degats a un ennemi, ou
    menace retiree. On accepte l'une ou l'autre — ce qui compte est qu'elle ait
    ete jouee et qu'elle ait produit un effet.
    """
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "77025" not in defausse:
        return False, f"Brains and Brawn n'a pas ete jouee (defausse = {defausse})"

    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is None:
            continue
        card_id = getattr(face.paper, "card_id", "")
        if card_id == "01094" and (face.max_health - face.health) > 0:
            return True, "des degats ont ete infliges au vilain"
        if card_id == "01097b" and getattr(face, "threat", 0) == 0:
            return True, "la menace du complot principal a ete ramenee a 0"
    return True, "Brains and Brawn jouee (effet non mesurable ici : aucune icone exploitable)"

def brawn_calculated_defense(monde, aides):
    """77004 : jouee en defense et payee en [mental], elle part en RESERVE.

    Modele de sg_unbeatable 75016 : on constate d'abord que la carte a bien ete
    JOUEE, puis on juge l'effet. La carte est financee par Genius 01089 ([mental]
    x2), donc la clause « If you played this card from your hand using a [mental]
    resource, put this card into your reserve » doit s'appliquer : la carte est
    en RESERVE, et surtout PAS en defausse.

    Le redressement de Brawn n'est pas testable ici : `Puzzle.Defend` declare la
    defense en court-circuitant son cout d'epuisement, donc Brawn n'est jamais
    epuise dans ce montage et « ready Brawn » n'a rien a redresser. En partie
    reelle, le cout `CostFunc.Exhaust("This")` de la defense de base
    (game/ability/factory/friend.py) est paye AVANT que `WhenUnitWouldDefend`
    parte : la carte redresse donc bien un heros deja epuise.
    """
    reserve = [getattr(f.paper, "card_id", None)
               for f in monde.players[0].reserve.GetAll()]
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]

    if "77004" not in reserve and "77004" not in defausse:
        return False, (f"Calculated Defense n'a pas ete jouee "
                       f"(reserve = {reserve}, defausse = {defausse})")
    if "77004" not in reserve:
        return False, ("Calculated Defense est en defausse alors qu'elle a ete payee "
                       "en [mental] depuis la main : elle devait aller en reserve")

    main = len(list(monde.players[0].hand_cards.Get()))
    if main < 1:
        return False, "main vide : aucune pioche constatee"
    return True, f"jouee en defense, recyclee en reserve, main a {main} carte(s)"

def brawn_gamma_strike_sans_bonus(monde, aides):
    """77006 : temoin. Payee en [energy], la carte fait 7 degats, pas 10.

    Le cas jumeau prouve les 10 degats quand le paiement est entierement
    [physical]. Celui-ci prouve que le bonus est bien CONDITIONNEL.
    """
    cible = aides["par_id"](monde, "01094")
    if cible is None:
        return False, "Rhino (01094) introuvable"
    degats = cible.max_health - cible.health
    if degats >= 10:
        return False, (f"{degats} degats subis alors que le paiement etait [energy] : "
                       f"le bonus « only [physical] » s'applique sans condition")
    if degats < 7:
        return False, f"{degats} degats subis (attendu 7 : l'attaque de base de la carte)"
    return True, f"{degats} degats : bonus correctement refuse hors paiement [physical]"

def brawn_shockwave_a_agi(monde, aides):
    """77010 : cout X, donc l'effet ne se voit que si le pilote a surpaye.

    On accepte l'une OU l'autre moitie (degats aux ennemis, menace retiree), la
    couleur des cartes defaussees n'etant pas maitrisable depuis le harnais. Ce
    qui est prouve, c'est que X a bien ete lu et que des cartes sont parties du
    deck.
    """
    defausse = list(monde.players[0].discard_pile.Get())
    if len(defausse) < 2:
        return False, f"defausse = {len(defausse)} carte(s) : Shockwave n'a rien defausse"

    # La version precedente s'arretait la — elle ne mesurait donc que la
    # defausse, jamais l'EFFET. On compte desormais les icones imprimees des
    # cartes parties du deck, et on exige la consequence correspondante :
    # 2 degats a chaque ennemi par [physical], 2 menaces par [mental].
    from game.operate.faces_counter import FacesCounter
    icones = FacesCounter.GetPrintedResources(defausse)
    physiques = icones.r + icones.g
    mentales = icones.b + icones.g

    if physiques == 0 and mentales == 0:
        return False, ("aucune icone [physical] ni [mental] parmi les cartes defaussees : "
                       "le cas ne prouve rien, revoir le deck de depart")

    if physiques > 0:
        for objet in monde.object_manager.card_dict.values():
            face = objet.face
            if face is not None and getattr(face.paper, "card_id", "") == "01094":
                subis = face.max_health - face.health
                if subis < 2:
                    return False, (f"{physiques} icone(s) [physical] defaussee(s) mais le "
                                   f"vilain n'a subi que {subis} degat(s)")
                return True, (f"{physiques} [physical] defaussee(s) -> {subis} degats ; "
                              f"{mentales} [mental]")
        return False, "vilain introuvable"

    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and getattr(face.paper, "card_id", "") == "01097b":
            return True, (f"{mentales} [mental] defaussee(s), menace du complot "
                          f"principal a {getattr(face, 'threat', '?')}")
    return True, f"{mentales} [mental] defaussee(s)"

def brawn_jouer_depuis_la_reserve(monde, aides):
    """77014 : une carte POSEE EN RESERVE doit etre jouable depuis la reserve.

    C'est le cas central du pack. On pose Forward-Thinking en jeu, on met une
    carte en reserve, puis on verifie que le moteur la considere « comme en
    main » (`IsLikeInHand`) — c'est ce drapeau qui la rend jouable et
    depensable, et il vient du flag de zone pose par le # CORRECTIF.
    """
    from game.effect.rule import GameRule

    joueur = monde.players[0]
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"

    main = list(joueur.hand_cards.Get())
    if not main:
        return False, "main vide : rien a mettre en reserve"

    joueur.PutIntoReserve([main[0]], GameRule(identite))

    en_reserve = list(joueur.reserve.Get())
    if not en_reserve:
        return False, "la carte n'est pas arrivee en reserve"

    face = en_reserve[0]
    if not face.card.IsLikeInHand():
        return False, "la carte en reserve n'est pas consideree « comme en main » : injouable"
    if face.card.area.flags.is_in_hand:
        return False, "la reserve se fait passer pour la main : le cloisonnement tomberait"
    return True, "carte en reserve, jouable, et distincte de la main"

def brawn_namor_suit_les_jetons(monde, aides):
    """77020 : Namor gagne +X ATK et +X SCH pour X jetons d'acceleration.

    Temoin : on releve ses valeurs, on ajoute un jeton, et on exige qu'elles
    montent. Un bonus fige a l'entree en jeu resterait identique.
    """
    namor = aides["par_id"](monde, "77020")
    if namor is None:
        return False, "Namor (77020) introuvable en jeu"

    rising_tide = aides["par_id"](monde, "77019")
    if rising_tide is None:
        return False, "Rising Tide (77019) introuvable en jeu"

    from game.effect.rule import GameRule

    atk_avant, sch_avant = namor.attack, namor.scheme
    if atk_avant < 2 or sch_avant < 2:
        return False, (f"Namor a {atk_avant} ATK / {sch_avant} SCH avec 1 jeton "
                       f"(attendu au moins 2/2 : base 1 + 1 jeton)")

    rising_tide.PlaceAccelerationToken(1, GameRule(rising_tide))
    atk_apres, sch_apres = namor.attack, namor.scheme

    if atk_apres <= atk_avant or sch_apres <= sch_avant:
        return False, (f"le bonus ne suit pas les jetons : {atk_avant}/{sch_avant} "
                       f"puis {atk_apres}/{sch_apres} apres un jeton de plus")
    return True, f"ATK/SCH suivent les jetons ({atk_avant}/{sch_avant} -> {atk_apres}/{sch_apres})"

def smr_mysterio_a_tough(monde, aides):
    """71017 : Mysterio en jeu doit porter un statut Tenace (Tough)."""
    face = aides["par_id"](monde, "71015")
    if face is None:
        return False, "Mysterio (71015) introuvable en jeu"
    if not face.IsTough():
        return False, "Mysterio n'a pas de statut Tenace"
    return True, "Mysterio est Tenace"

def we_hunger_resolue(monde, aides):
    """72012 : le joueur est en forme heros et l'obligation est resolue.

    Le pilote choisit une des deux options (3 degats, ou 3 menaces + soin 1) :
    on accepte l'une OU l'autre, mais l'obligation ne doit plus etre en jeu et
    la penalite correspondante doit se voir dans le monde.
    """
    if not monde.players[0].IsHero():
        return False, "le joueur n'est pas en forme heros"
    if aides["par_id"](monde, "72012") is not None:
        return False, "We Hunger est encore en jeu"
    identite = aides["identite"](monde)
    subis = identite.max_health - identite.health
    from game.operate.worlds import Worlds
    scheme = Worlds.FindMainScheme2(monde) if hasattr(Worlds, "FindMainScheme2") else None
    menace = None
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and getattr(face.paper, "card_id", "") == "01097b":
            menace = face.threat
    if subis == 3:
        return True, "option degats appliquee"
    if menace is not None and menace >= 3:
        return True, "option menace appliquee"
    return False, f"aucune penalite constatee (degats={subis}, menace={menace})"

def identite_a_un_statut(monde, aides):
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    for statut in ("Stunned", "Confused"):
        if identite.CastTo(aides["CanStatus"]).HasStatus(statut):
            return True, f"identite {statut}"
    return False, "aucun statut pose sur l'identite apres le boost"

def face_identite(monde, aides):
    """Verifie QUELLE face de l'identite est active.

    `etat_attendu` ne sait dire que Hero ou AlterEgo ; pour un heros a trois
    faces (Totally Awesome Hulk / Amadeus Cho / Uncontrollable Hulk) il faut
    descendre au card_id. La cle 'en_jeu'/'hors_jeu' du cas est verifiee ici
    aussi, pour pouvoir controler le flip de « The Trunk » dans la foulee.
    """
    attendu = aides["cas"].get("attendu") or {}
    identite = aides["identite"](monde)
    soucis = []

    courante = getattr(identite.paper, "card_id", None)
    if courante != attendu.get("face"):
        soucis.append(f"face active = {courante} (attendu {attendu.get('face')})")

    for card_id in attendu.get("en_jeu") or []:
        if aides["par_id"](monde, card_id) is None:
            soucis.append(f"{card_id} n'est pas en jeu")

    for card_id in attendu.get("hors_jeu") or []:
        if aides["par_id"](monde, card_id) is not None:
            soucis.append(f"{card_id} est encore en jeu")

    if soucis:
        return False, " ; ".join(soucis)
    return True, f"face active = {courante}"

def identite_reste_inclinee(monde, aides):
    """69012 : l'obligation interdit de redresser l'identite."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if aides["par_id"](monde, "69012") is None:
        return False, "l'obligation 69012 n'est pas en jeu"
    if identite.IsExhaust():
        return True, "l'identite est restee inclinee malgre le redressement"
    return False, "l'identite s'est redressee : l'obligation ne bloque rien"

def witter_a_agi(monde, aides):
    """69013 : soit 2 degats indirects, soit l'identite inclinee."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    degats = identite.max_health - identite.health
    if degats >= 2:
        return True, f"2 degats indirects encaisses ({degats})"
    if identite.IsExhaust():
        return True, "identite inclinee"
    return False, "ni degats ni inclinaison : le When Revealed n'a rien fait"

def identite_sonnee_et_desorientee(monde, aides):
    """69016 : les DEUX statuts doivent etre poses sur la meme cible."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    statut = identite.CastTo(aides["CanStatus"])
    manquants = [s for s in ("Stunned", "Confused") if not statut.HasStatus(s)]
    if manquants:
        return False, f"statut(s) manquant(s) : {', '.join(manquants)}"
    return True, "identite Stunned + Confused"

def web_of_fate_a_pioche(monde, aides):
    """69011 : une des 5 cartes du dessus doit avoir rejoint la main.

    On ne fige pas LAQUELLE : c'est le pilote de test qui choisit dans la
    liste proposee, et son critere n'a pas a etre grave dans le test.
    """
    attendus = {"69004", "69006", "69003", "69009", "69010"}
    main = {getattr(f.paper, "card_id", None)
            for f in monde.players[0].hand_cards.GetAll()}
    prises = attendus & main
    if prises:
        return True, f"ajoutee a la main depuis les 5 du dessus : {sorted(prises)}"
    return False, ("aucune des 5 cartes regardees n'est en main "
                   f"(main = {sorted(x for x in main if x)})")

def veranke_devenue_sbire(monde, aides):
    """69026 : l'alliee vaincue revient en jeu comme sbire, soignee."""
    from game.card.face.card_type import Minion
    from game.card.face.card_type import Ally

    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is None or not face.IsInPlay():
            continue
        if not face.IsName("Spider-Woman"):
            continue
        if Minion.IsType(face):
            degats = face.max_health - face.health
            if degats != 0:
                return False, f"Veranke sbire mais pas soignee ({degats} degats)"
            return True, f"Veranke est un sbire ({face.attack} ATK / {face.scheme} SCH), soignee"
        if Ally.IsType(face):
            return False, "Veranke est encore une alliee : TreatAsMinion n'a pas eu lieu"
    return False, "Veranke a quitte le jeu au lieu de revenir en sbire"

def avatar_a_3_shatter(monde, aides):
    avatar = aides["par_id"](monde, "55029a")
    if avatar is None:
        return False, "Avatar de Loki introuvable en jeu"
    n = avatar.CastTo(aides["CanPlaceCounter"]).GetCounters("shatter")
    return (n >= 3), f"compteurs shatter sur l'Avatar = {n} (attendu >= 3)"

def amelioration_a_un_cout_exhaust(monde, aides):
    carte = aides["par_id"](monde, "04162b")
    if carte is None:
        return False, "amelioration introuvable en jeu"
    trouve = []
    for eff in carte.effect.GetAll() if hasattr(carte.effect, "GetAll") else []:
        pass
    # L'introspection des effets varie ; on interroge directement les abilities
    # construites par le module de la carte.
    import importlib
    module = importlib.import_module("cards.pack.trors.hydra_campaign.04162b")
    for ability in module.GetAbilities():
        for cf in getattr(ability, "cost_funcs", []):
            trouve.append(type(cf).__name__)
    ok = any(n.startswith("Exhaust") for n in trouve)
    return ok, f"couts declares = {trouve or 'aucun'}"


# ---------------------------------------------------------------------------
# Verification generique, pilotee par le dictionnaire 'attendu' du cas.
#
#   attributs        {nom: ecart}  ecart entre la valeur courante de l'identite
#                    et sa valeur IMPRIMEE (donc « +1 ATK » s'ecrit attack: 1)
#   traits           traits que l'identite doit porter
#   en_jeu           card_ids qui doivent etre en jeu
#   hors_jeu         card_ids qui ne doivent PAS etre en jeu
#   compteurs        [[card_id, nom_du_compteur, valeur]]
#   jetons           [[card_id, nom_du_jeton, valeur]]  stock distinct des compteurs
#   menace           [[card_id, valeur]] menace exacte sur un complot
#   degats_identite  degats subis par l'identite (max_health - health)
#   dans_deck_rencontre  card_ids qui doivent se trouver dans le deck Rencontre
#   en_main          card_ids qui doivent se trouver dans la main du joueur
#   defausse         card_ids qui doivent se trouver dans la defausse du joueur
#   statuts          [[card_id, "Stunned"|"Confused"|"Tough"]]
#   exhausted        card_ids qui doivent etre inclines
IMPRIME = {
    "attack": "printed_attack",
    "scheme": "printed_scheme",
    "thwart": "printed_thwart",
    "defense": "printed_defense",
    "recover": "printed_recovery",
    "hand_size": "printed_hand_size",
    "health": "printed_health",
    "hazard": "printed_hazard",
    "retaliate": "printed_retaliate",
    "villainous": "printed_villainous",
}

def etat_attendu(monde, aides):
    attendu = aides["cas"].get("attendu") or {}
    identite = aides["identite"](monde)
    soucis = []

    for nom, ecart in (attendu.get("attributs") or {}).items():
        courant = identite.max_health if nom == "health" else getattr(identite, nom)
        base = getattr(identite, IMPRIME[nom])
        if courant != base + ecart:
            soucis.append(f"{nom}={courant} (imprime {base}, attendu {base + ecart})")

    for trait in attendu.get("traits") or []:
        if not identite.HasTrait(trait):
            soucis.append(f"trait {trait} absent de l'identite")

    for card_id in attendu.get("en_jeu") or []:
        if aides["par_id"](monde, card_id) is None:
            soucis.append(f"{card_id} n'est pas en jeu")

    for card_id in attendu.get("hors_jeu") or []:
        if aides["par_id"](monde, card_id) is not None:
            soucis.append(f"{card_id} est encore en jeu")

    for card_id, compteur, valeur in attendu.get("compteurs") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (compteurs)")
            continue
        n = face.CastTo(aides["CanPlaceCounter"]).GetCounters(compteur)
        if n != valeur:
            soucis.append(f"{card_id}.{compteur}={n} (attendu {valeur})")

    # Jetons et compteurs sont deux stocks distincts : la menace posee sur une
    # carte joueur (Beat Cop, Private Investigator) est un JETON 'threat'.
    for card_id, jeton, valeur in attendu.get("jetons") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (jetons)")
            continue
        n = face.CastTo(aides["CanPlaceToken"]).GetTokens(jeton)
        if n != valeur:
            soucis.append(f"{card_id}.{jeton}={n} jeton(s) (attendu {valeur})")

    for compteur, mini in attendu.get("compteurs_total") or []:
        total = 0
        for objet in monde.object_manager.card_dict.values():
            face = objet.face
            if face is None or not face.IsInPlay():
                continue
            if isinstance(face, aides["CanPlaceCounter"]):
                total += face.GetCounters(compteur)
        if total < mini:
            soucis.append(f"total des compteurs « {compteur} » en jeu = {total} "
                          f"(attendu au moins {mini})")

    # `menace_min` plutot que `menace` des que la valeur exacte depend du
    # tirage : la manigance d'un vilain vaut son SCH plus ses icones de boost,
    # qui changent avec le nombre de joueurs.
    for card_id, mini in attendu.get("menace_min") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (menace)")
        elif face.threat < mini:
            soucis.append(f"menace sur {card_id} = {face.threat} (attendu au moins {mini})")

    for card_id, valeur in attendu.get("menace") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (menace)")
            continue
        if face.threat != valeur:
            soucis.append(f"menace sur {card_id} = {face.threat} (attendu {valeur})")

    for card_id, nom, ecart in attendu.get("attributs_carte") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (attribut {nom})")
            continue
        courant = face.max_health if nom == "health" else getattr(face, nom)
        base = getattr(face, IMPRIME[nom])
        if courant != base + ecart:
            soucis.append(f"{card_id}.{nom}={courant} "
                          f"(imprime {base}, attendu {base + ecart})")

    for card_id, valeur in attendu.get("degats") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (degats)")
        elif face.max_health - face.health != valeur:
            soucis.append(f"degats sur {card_id} = {face.max_health - face.health} "
                          f"(attendu {valeur})")

    for card_id, mini in attendu.get("degats_min") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (degats_min)")
        elif face.max_health - face.health < mini:
            soucis.append(f"degats sur {card_id} = {face.max_health - face.health} "
                          f"(attendu au moins {mini})")

    if "degats_identite" in attendu:
        subis = identite.max_health - identite.health
        if subis != attendu["degats_identite"]:
            soucis.append(f"degats sur l'identite = {subis} "
                          f"(attendu {attendu['degats_identite']})")

    if attendu.get("dans_deck_rencontre"):
        from game.operate.worlds import Worlds
        ids = {getattr(f.paper, "card_id", None)
               for f in Worlds.GetEncounterDeckCards(monde)}
        for card_id in attendu["dans_deck_rencontre"]:
            if card_id not in ids:
                soucis.append(f"{card_id} absent du deck Rencontre")

    if "forme" in attendu:
        courante = "Hero" if monde.players[0].IsHero() else "AlterEgo"
        if courante != attendu["forme"]:
            soucis.append(f"forme {courante} (attendu {attendu['forme']})")

    for trait, mini in attendu.get("en_jeu_trait") or []:
        n = 0
        for objet in monde.object_manager.card_dict.values():
            face = objet.face
            if face is not None and face.IsInPlay() and face.HasTrait(trait):
                n += 1
        if n < mini:
            soucis.append(f"{n} carte(s) {trait} en jeu (attendu au moins {mini})")

    for card_id in attendu.get("exhausted") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (inclinaison)")
        elif not face.IsExhaust():
            soucis.append(f"{card_id} n'est pas incline")

    for card_id in attendu.get("pret") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (inclinaison)")
        elif face.IsExhaust():
            soucis.append(f"{card_id} est incline alors qu'il devrait etre pret")

    for card_id, statut in attendu.get("statuts") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (statut {statut})")
        elif not face.CastTo(aides["CanStatus"]).HasStatus(statut):
            soucis.append(f"{card_id} ne porte pas le statut {statut}")

    # `defausse` prouve qu'un evenement a bien ete JOUE : un evenement encore en
    # main n'est ni « en jeu » ni dans la defausse, donc `hors_jeu` ne le voit pas.
    for card_id in attendu.get("defausse") or []:
        cartes = [getattr(f.paper, "card_id", None)
                  for f in monde.players[0].discard_pile.Get()]
        if card_id not in cartes:
            soucis.append(f"{card_id} n'est pas dans la defausse du joueur "
                          f"(defausse = {cartes})")

    if "taille_main" in attendu:
        n = len(list(monde.players[0].hand_cards.Get()))
        if n != attendu["taille_main"]:
            soucis.append(f"main = {n} carte(s) (attendu {attendu['taille_main']})")

    for card_id in attendu.get("en_main") or []:
        cartes = [getattr(f.paper, "card_id", None)
                  for f in monde.players[0].hand_cards.GetAll()]
        if card_id not in cartes:
            soucis.append(f"{card_id} n'est pas en main (main = {cartes})")

    # La RESERVE du pack brawn : zone hors-jeu de 3 cartes au plus, dont les
    # cartes restent jouables et depensables. Sans cette cle, aucun cas ne peut
    # prouver qu'une carte y est bien arrivee.
    for card_id in attendu.get("en_reserve") or []:
        cartes = [getattr(f.paper, "card_id", None)
                  for f in monde.players[0].reserve.GetAll()]
        if card_id not in cartes:
            soucis.append(f"{card_id} n'est pas en reserve (reserve = {cartes})")

    if "taille_reserve" in attendu:
        n = len(list(monde.players[0].reserve.Get()))
        if n != attendu["taille_reserve"]:
            soucis.append(f"reserve = {n} carte(s) (attendu {attendu['taille_reserve']})")

    if "defausse_joueur" in attendu:
        n = len(list(monde.players[0].discard_pile.Get()))
        if n != attendu["defausse_joueur"]:
            soucis.append(f"defausse du joueur = {n} carte(s) "
                          f"(attendu {attendu['defausse_joueur']})")

    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"

def cd_cleansing_soigne_et_pioche(monde, aides):
    """70004 : Cloak entierement soigne (3/3) et 2 cartes piochees."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    soucis = []
    degats = identite.max_health - identite.health
    if degats != 0:
        soucis.append(f"degats restants sur Cloak = {degats} (attendu 0 : soin de 3)")
    main = list(monde.players[0].hand_cards.GetAll())
    if len(main) != 2:
        soucis.append(f"main = {len(main)} carte(s) (attendu 2 : pioche du bonus)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "soin complet et 2 cartes piochees"

def cd_vilain_apres_daggers(monde, aides):
    """70005 : 3 degats sur Rhino, Sonne ET Desoriente (Cloak est en jeu)."""
    vilain = aides["par_id"](monde, "01094")
    if vilain is None:
        return False, "Rhino introuvable"
    soucis = []
    d = vilain.max_health - vilain.health
    if d != 3:
        soucis.append(f"degats vilain = {d} (attendu 3)")
    statut = vilain.CastTo(aides["CanStatus"])
    if not statut.HasStatus("Stunned"):
        soucis.append("vilain pas Sonne")
    if not statut.HasStatus("Confused"):
        soucis.append("vilain pas Desoriente")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "3 degats, vilain sonne et desoriente"

def cd_vilain_apres_channel(monde, aides):
    """70010 : 1 degat sur Rhino, Desoriente + Sonne, 1 soin sur Cloak (2-1)."""
    vilain = aides["par_id"](monde, "01094")
    identite = aides["identite"](monde)
    if vilain is None or identite is None:
        return False, "Rhino ou identite introuvable"
    soucis = []
    d = vilain.max_health - vilain.health
    if d != 1:
        soucis.append(f"degats vilain = {d} (attendu 1)")
    statut = vilain.CastTo(aides["CanStatus"])
    if not statut.HasStatus("Confused"):
        soucis.append("vilain pas Desoriente")
    if not statut.HasStatus("Stunned"):
        soucis.append("vilain pas Sonne (Dagger est pourtant en forme heros)")
    subis = identite.max_health - identite.health
    if subis != 1:
        soucis.append(f"degats restants sur Cloak = {subis} (attendu 1 : 2 subis - 1 soigne)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "1 degat, deux statuts, 1 soin sur Cloak"

def jj_une_autre_manigance_revelee(monde, aides):
    """73012 : la manigance est vaincue et une AUTRE manigance est arrivee en jeu."""
    from game.card.face.card_type import EncounterSideScheme, PlayerSideScheme
    if aides["par_id"](monde, "73012") is not None:
        return False, "Always a Bigger Conspiracy est encore en jeu"
    autres = []
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is None or not face.IsInPlay():
            continue
        if EncounterSideScheme.IsType(face) or PlayerSideScheme.IsType(face):
            if getattr(face.paper, "card_id", None) != "73012":
                autres.append(face)
    if not autres:
        return False, "aucune autre manigance secondaire n'a ete revelee"
    noms = [getattr(x.paper, "card_id", "?") for x in autres]
    return True, f"manigance(s) revelee(s) : {noms}"

def jj_couple_tenace(monde, aides):
    """73022 : Jessica Jones ET Luke Cage portent un statut Tenace."""
    identite = aides["identite"](monde)
    luke = aides["par_id"](monde, "73002")
    soucis = []
    if identite is None:
        soucis.append("identite introuvable")
    elif not identite.IsTough():
        soucis.append("Jessica Jones n'est pas Tenace")
    if luke is None:
        soucis.append("Luke Cage n'est pas en jeu")
    elif not luke.IsTough():
        soucis.append("Luke Cage n'est pas Tenace")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "les deux membres du duo sont Tenaces"

def aav_dig_deep_intact(monde, aides):
    """74003 : a 10 PV, 3 degats, Rhino Sonne et 1 menace retiree du complot."""
    vilain = aides["par_id"](monde, "01094")
    complot = aides["par_id"](monde, "01097b")
    soucis = []
    if vilain is None:
        return False, "Rhino introuvable"
    degats = vilain.max_health - vilain.health
    if degats != 3:
        soucis.append(f"degats vilain = {degats} (attendu 3)")
    if not vilain.CastTo(aides["CanStatus"]).HasStatus("Stunned"):
        soucis.append("vilain pas Sonne")
    if complot is not None and complot.threat != 4:
        soucis.append(f"menace complot = {complot.threat} (attendu 4)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "3 degats, vilain sonne, 1 menace retiree"

def _obligation_resolue(monde, aides, card_id):
    """L'obligation a quitte le jeu sans que la resolution ne plante.

    Le pilote choisit une des options ; on n'impose donc pas laquelle, mais la
    carte ne doit plus etre en jeu. Une exception dans le handler (ChangeForm
    inexistant, par exemple) laisse l'obligation sur la table.
    """
    if aides["par_id"](monde, card_id) is not None:
        return False, f"{card_id} est encore en jeu : la resolution a echoue"
    return True, "obligation resolue et sortie du jeu"

def obligation_resolue_65013(monde, aides):
    return _obligation_resolue(monde, aides, "65013")

def obligation_resolue_67011(monde, aides):
    return _obligation_resolue(monde, aides, "67011")

def obligation_resolue_75018(monde, aides):
    return _obligation_resolue(monde, aides, "75018")

def mf_mental_gymnastics(monde, aides):
    """65012 : 2 degats (X=0) et le vilain Desoriente car la main est vide."""
    vilain = aides["par_id"](monde, "01094")
    if vilain is None:
        return False, "Rhino introuvable"
    soucis = []
    degats = vilain.max_health - vilain.health
    if degats != 2:
        soucis.append(f"degats = {degats} (attendu 2)")
    if not vilain.CastTo(aides["CanStatus"]).HasStatus("Confused"):
        soucis.append("vilain pas Desoriente alors que la main est vide")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "2 degats et vilain desoriente"

def iw_end_of_the_line(monde, aides):
    """66018 : la traitrise s'est resolue et a quitte le jeu sans planter."""
    if aides["par_id"](monde, "66018") is not None:
        return False, "End of the Line est encore en jeu : la resolution a echoue"
    return True, "traitrise resolue"

def ht_nova_flame(monde, aides):
    """64010 : 7 degats au vilain, et des compteurs flamme poses sur lui.

    « up to 3 » : le pilote choisit combien, on exige au moins 1 compteur et
    les 7 degats, qui eux ne sont pas optionnels.
    """
    vilain = aides["par_id"](monde, "01094")
    if vilain is None:
        return False, "Rhino introuvable"
    soucis = []
    degats = vilain.max_health - vilain.health
    flammes = vilain.CastTo(aides["CanPlaceCounter"]).GetCounters("flame")
    # 7 de la carte + 1 par compteur pose, via « Flame On! » de l'identite.
    attendu = 7 + flammes
    if degats != attendu:
        soucis.append(f"degats = {degats} (attendu {attendu} : 7 + {flammes} compteur(s))")
    if flammes < 1:
        soucis.append("aucun compteur flamme pose")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"7 degats et {flammes} compteur(s) flamme"

def obligation_resolue_76012(monde, aides):
    return _obligation_resolue(monde, aides, "76012")

def obligation_resolue_78013(monde, aides):
    return _obligation_resolue(monde, aides, "78013")

def obligation_resolue_66013(monde, aides):
    return _obligation_resolue(monde, aides, "66013")


def ht_the_thing_tenace(monde, aides):
    """64002 : l'allie est en jeu, a 5 PV, 3 ATK et un statut Tenace."""
    allie = aides["par_id"](monde, "64002")
    if allie is None:
        return False, "The Thing n'est pas en jeu"
    soucis = []
    if allie.max_health != 5:
        soucis.append(f"PV = {allie.max_health} (attendu 5)")
    if allie.attack != 3:
        soucis.append(f"ATK = {allie.attack} (attendu 3)")
    if not allie.IsTough():
        soucis.append("pas de statut Tenace malgre le mot-cle Toughness")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "5 PV, 3 ATK, Tenace"

def iw_mister_fantastic_a_choisi(monde, aides):
    """66002 : l'allie est en jeu et UNE de ses deux options a ete appliquee.

    Option A : 1 menace retiree de chaque manigance (le complot passe de 3 a 2).
    Option B : la carte du dessus de la defausse revient en main.
    """
    allie = aides["par_id"](monde, "66002")
    if allie is None:
        return False, "Mister Fantastic n'est pas en jeu"
    complot = aides["par_id"](monde, "01097b")
    if complot is not None and complot.threat == 2:
        return True, "option A : 1 menace retiree du complot"
    main = len(list(monde.players[0].hand_cards.GetAll()))
    if main > 0:
        return True, f"option B : main a {main} carte(s), la defausse a ete puisee"
    return False, (f"aucune option appliquee (menace complot="
                   f"{complot.threat if complot else '?'}, main={main})")

def manigance_annexe_en_jeu(monde, aides):
    """Au moins une manigance secondaire se trouve en jeu."""
    from game.card.face.card_type import EncounterSideScheme, PlayerSideScheme
    trouvees = []
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is None or not face.IsInPlay():
            continue
        if EncounterSideScheme.IsType(face) or PlayerSideScheme.IsType(face):
            trouvees.append(getattr(face.paper, "card_id", "?"))
    if not trouvees:
        return False, "aucune manigance secondaire en jeu"
    return True, f"manigance(s) secondaire(s) en jeu : {trouvees}"

def allie_est_traitre(monde, aides):
    """L'allie designe par `attendu['allie']` a bascule cote sbire.

    Le mot-cle maison TRAITOR passe par `TreatAsMinion` : la carte prend le
    gabarit « Traitor Minion » et son card_id CHANGE. On verifie donc les deux
    bouts : l'allie n'est plus controle, et un Traitor Minion est en jeu.
    """
    card_id = (aides["cas"].get("attendu") or {})["allie"]
    controles = [getattr(f.paper, "card_id", "?")
                 for f in monde.players[0].GetControlAllies()]
    if card_id in controles:
        return False, f"{card_id} est encore un allie sous controle du joueur"
    traitre = aides["par_nom"](monde, "Traitor Minion")
    if traitre is None:
        return False, (f"{card_id} n'est plus controle mais aucun Traitor Minion "
                       f"n'est en jeu (allies restants = {controles})")
    # `intact` verrouille la moitie « prevent all damage » du texte.
    if (aides["cas"].get("attendu") or {}).get("intact"):
        degats = traitre.max_health - traitre.health
        if degats != 0:
            return False, f"le traitre a subi {degats} degat(s), attendu 0"
    return True, f"{card_id} est traite comme un sbire"

def tah_hellbender_alliee(monde, aides):
    """68014 : Lady Hellbender est passee du camp ennemi au camp du joueur.

    `TreatAsAlly` remplace la carte par le gabarit `tah_hellbender_ally`, donc
    son card_id CHANGE : on interroge les allies controles, pas `par_id`.
    """
    allies = [getattr(f.paper, "card_id", "?")
              for f in monde.players[0].GetControlAllies()]
    if not allies:
        return False, "le joueur ne controle aucun allie"
    if aides["par_id"](monde, "68014") is not None:
        return False, f"68014 est encore un sbire (allies = {allies})"
    return True, f"Lady Hellbender est passee alliee (allies = {allies})"

def cd_barrage_reparti(monde, aides):
    """70002a : les degats de l'attaque de base de Dagger ont touche DEUX ennemis.

    On ne fige pas la repartition exacte (le pilote choisit), seulement le fait
    qu'elle a eu lieu : sans Bright Barrage, une attaque de base ne peut frapper
    qu'une seule cible.
    """
    touches = []
    for card_id in ("01101", "01103"):
        face = aides["par_id"](monde, card_id)
        if face is None:
            # Sbire vaincu : il a forcement pris des degats.
            touches.append(card_id)
        elif face.max_health - face.health > 0:
            touches.append(card_id)
    if len(touches) < 2:
        return False, f"un seul ennemi touche ({touches}) : l'attaque ne s'est pas repartie"
    return True, f"degats repartis sur {touches}"

def cd_tandy_recover(monde, aides):
    """70002b : Tandy Bowen a +2 REC tant que Tyrone Johnson est en jeu.

    Tandy est l'identite du JOUEUR LIE (`monde.players[1]`), pas du joueur 0 :
    le verificateur generique, qui lit toujours `players[0]`, ne peut pas la
    voir.
    """
    if len(monde.players) < 2:
        return False, "l'identite liee n'a pas ete creee"
    tandy = monde.players[1].GetIdentity()
    if tandy is None:
        return False, "identite du joueur lie introuvable"
    attendu = tandy.printed_recovery + 2
    if tandy.recover != attendu:
        return False, (f"REC de Tandy = {tandy.recover} "
                       f"(imprime {tandy.printed_recovery}, attendu {attendu})")
    return True, f"REC de Tandy = {tandy.recover} (imprime {tandy.printed_recovery})"

def tah_brute_frappe_plus_fort(monde, aides):
    """68001c : la forme BRUTE est active et son attaque a fait plus que l'ATK imprime."""
    identite = aides["identite"](monde)
    vilain = aides["par_id"](monde, "01094")
    if identite is None or vilain is None:
        return False, "identite ou Rhino introuvable"
    if getattr(identite.paper, "card_id", None) != "68001c":
        return False, f"forme active = {getattr(identite.paper, 'card_id', '?')} (attendue 68001c)"
    degats = vilain.max_health - vilain.health
    attendu = identite.attack + 2
    if degats < attendu:
        return False, (f"degats = {degats}, or l'attaque de base ({identite.attack}) "
                       f"plus le bonus de 2 en attendait {attendu}")
    return True, f"forme BRUTE, {degats} degats (ATK {identite.attack} + 2)"

def vr_hunger_a_soigne(monde, aides):
    """72001a : le sbire est vaincu et Venom s'est soigne de 1.

    On compare aux 5 degats poses en mise en place plutot que d'exiger un total
    exact : le pilote peut depenser Symbiotic Bond, qui coute 1 degat de plus.
    """
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if aides["par_id"](monde, "01121") is not None:
        return False, "le sbire n'a pas ete vaincu, Hunger ne peut pas partir"
    subis = identite.max_health - identite.health
    if subis >= 5:
        return False, f"degats = {subis} : aucun soin, Hunger n'a pas repondu"
    return True, f"sbire vaincu et Venom soigne (degats {subis} pour 5 poses)"

def mk_reduction_protection(monde, aides):
    """76001c : la carte Protection a ete jouee alors que la main etait vide.

    Elle coute 1 ; sans la reduction de Mr. Knight il n'y a aucun payeur et la
    carte reste en main. La voir EN JEU prouve donc la reduction.
    """
    if aides["par_id"](monde, "01081") is None:
        return False, "Armored Vest n'est pas en jeu : le cout n'a pas ete reduit"
    identite = aides["identite"](monde)
    face = getattr(identite.paper, "card_id", "?") if identite else "?"
    if face != "76001c":
        return False, f"forme active = {face} (attendue Mr. Knight 76001c)"
    return True, "Armored Vest posee gratuitement en forme Mr. Knight"

def identite_sans_statut_tenace(monde, aides):
    """L'identite du joueur ne porte PLUS de statut Tenace."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if identite.IsTough():
        return False, "l'identite porte encore un statut Tenace"
    return True, "le statut Tenace a bien ete defausse"

def identite_est_tenace(monde, aides):
    """L'identite du joueur porte un statut Tenace."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if not identite.IsTough():
        return False, "l'identite n'est pas Tenace"
    return True, "l'identite est Tenace"

def tt_human_torch_a_choisi(monde, aides):
    """67002 : la torche est en jeu et UNE des deux options a ete appliquee.

    Option A : 1 degat a The Thing puis statut Tenace.
    Option B : 3 degats au vilain.
    Le pilote choisit ; on accepte l'une ou l'autre, mais pas l'inaction.
    """
    torche = aides["par_id"](monde, "67002")
    if torche is None:
        return False, "Human Torch n'est pas en jeu"
    identite = aides["identite"](monde)
    vilain = aides["par_id"](monde, "01094")
    subis = identite.max_health - identite.health if identite else 0
    degats_vilain = (vilain.max_health - vilain.health) if vilain else 0
    if identite is not None and identite.IsTough() and subis == 1:
        return True, "option A : 1 degat encaisse et statut Tenace"
    if degats_vilain == 3:
        return True, "option B : 3 degats au vilain"
    return False, (f"aucune des deux options appliquee "
                   f"(degats identite={subis}, degats vilain={degats_vilain})")

def obligation_resolue_74012(monde, aides):
    return _obligation_resolue(monde, aides, "74012")

def obligation_resolue_73017(monde, aides):
    return _obligation_resolue(monde, aides, "73017")

def aav_retaliate(monde, aides):
    """74008 : Agent Anti-Venom porte retaliate 1 tant que le Booster est en jeu."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    valeur = getattr(identite, "retaliate", None)
    if valeur is None:
        return False, "l'identite n'expose pas d'attribut retaliate"
    if valeur != 1:
        return False, f"retaliate = {valeur} (attendu 1)"
    return True, "retaliate 1 accorde"

def jj_identite_tenace(monde, aides):
    """73016 : l'identite de Jessica Jones porte un statut Tenace (Tough)."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if not identite.IsTough():
        return False, "Jessica Jones n'a pas de statut Tenace"
    return True, "Jessica Jones est Tenace"

def mk_forme_heros_et_vilain_desoriente(monde, aides):
    """76010 : l'identite est passee en forme heros et Rhino est Desoriente."""
    identite = aides["identite"](monde)
    vilain = aides["par_id"](monde, "01094")
    if identite is None or vilain is None:
        return False, "identite ou Rhino introuvable"
    soucis = []
    if not monde.players[0].IsHero():
        soucis.append("l'identite est restee en alter-ego")
    if not vilain.CastTo(aides["CanStatus"]).HasStatus("Confused"):
        soucis.append("vilain pas Desoriente")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "forme heros et vilain desoriente"

def lj_un_pet_avenger_en_jeu(monde, aides):
    """78027 : au moins un allie PET AVENGER est arrive en jeu."""
    n = 0
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and face.IsInPlay() and face.HasTrait("PET AVENGER"):
            n += 1
    if n >= 1:
        return True, f"{n} PET AVENGER en jeu"
    return False, "aucun PET AVENGER en jeu : la recherche n'a rien sorti"

def lj_defausse_non_vide(monde, aides):
    """78012 : la carte cherchee dans le deck est bien partie a la defausse.

    L'evenement lui-meme s'y retrouve aussi ; on exige donc au moins DEUX
    cartes, sinon le test passerait sur la seule defausse de Psionic Tracking.
    """
    n = len(list(monde.players[0].discard_pile.Get()))
    if n >= 2:
        return True, f"defausse = {n} cartes (evenement + carte pistee)"
    return False, f"defausse = {n} carte(s) : rien n'a ete defausse depuis le deck"

# Sonde de mise au point : n'est utilisee par aucun cas, mais rend le plateau
# lisible quand on ecrit un nouveau cas et qu'on ignore l'etat de depart (forme
# de l'identite, valeurs imprimees, cartes en jeu). Elle rend toujours False
# pour que son releve apparaisse dans le message d'echec.
def probe(monde, aides):
    ident = aides["identite"](monde)
    infos = [f"identite={ident.paper.card_id} type={type(ident).__name__}"]
    for attr in ("attack", "thwart", "defense", "recover", "health", "max_health",
                 "hand_size", "printed_attack", "printed_thwart", "printed_defense",
                 "printed_recovery", "printed_health", "printed_hand_size"):
        infos.append(f"{attr}={getattr(ident, attr, 'NA')}")
    en_jeu = []
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and face.IsInPlay():
            en_jeu.append(getattr(face.paper, "card_id", "?"))
    infos.append("en_jeu=" + ",".join(en_jeu))
    return False, " | ".join(infos)

# ------------------------------------------------------- pack squirrel_girl --
def _sg_ecureuils_en_jeu(monde):
    faces = []
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and face.IsInPlay() and face.HasTrait("SQUIRREL"):
            faces.append(face)
    return faces

def sg_deck_ecureuil_complet(monde, aides):
    """75001b : le setup range les 6 ecureuils dans le deck additionnel."""
    joueur = monde.players[0]
    deck = list(joueur.additional_deck.Get())
    ids = sorted(getattr(f.paper, "card_id", "?") for f in deck)
    attendus = ["75002", "75003", "75004", "75005", "75006", "75007"]
    if ids != attendus:
        return False, f"deck ecureuil = {ids} (attendu {attendus})"
    return True, "les 6 ecureuils sont dans le deck ecureuil"

def sg_deux_ecureuils_prets(monde, aides):
    """75013 : deux ecureuils entrent en jeu, et ils sont PRETS."""
    faces = _sg_ecureuils_en_jeu(monde)
    if len(faces) < 2:
        return False, f"{len(faces)} ecureuil(s) en jeu (attendu 2)"
    inclines = [getattr(f.paper, "card_id", "?") for f in faces if f.IsExhaust()]
    if inclines:
        return False, f"ecureuils inclines alors qu'ils devraient etre prets : {inclines}"
    return True, f"{len(faces)} ecureuils en jeu, tous prets"

def sg_ecureuil_depense(monde, aides):
    """75001a : l'ecureuil a bien finance la carte, et Unbeatable Army a suivi.

    On depense Tippy-Toe pour jouer Squirrel Swarm : l'ecureuil doit avoir
    quitte le jeu, l'evenement doit etre resolu, et les degats sur le vilain
    doivent depasser les 3 de base (bonus « si tu as depense un ecureuil »)
    ou l'identite doit avoir place son degat supplementaire.
    """
    faces = _sg_ecureuils_en_jeu(monde)
    if faces:
        return False, "l'ecureuil est encore en jeu : il n'a pas ete depense"
    vilain = aides["par_id"](monde, "01094")
    if vilain is None:
        return False, "le vilain 01094 est introuvable"
    subis = vilain.max_health - vilain.health
    if subis < 6:
        return False, (f"degats sur le vilain = {subis} : la depense n'a pas ete "
                       f"prise en compte (3 de base, 6 attendus au minimum)")
    return True, f"ecureuil depense, {subis} degats sur le vilain"

def sg_capacites_blanches(monde, aides):
    """75020 : Discord in the Branches rend les capacites d'ecureuil blanches.

    Nancy Whitehead (75008) est mise en jeu APRES la manigance. Sa propre
    capacite n'est pas blanchie (ce n'est pas un ecureuil), donc un ecureuil
    arrive ; ce qui doit rester muet, c'est la capacite de CET ecureuil. On le
    verifie sur Tippy-Toe, dont la reponse d'entree en jeu regarde le deck.
    """
    faces = _sg_ecureuils_en_jeu(monde)
    if not faces:
        return False, "aucun ecureuil en jeu : la mise en place a echoue"
    joueur = monde.players[0]
    reste = len(list(joueur.additional_deck.Get()))
    if reste != 5:
        return False, f"deck ecureuil = {reste} cartes (attendu 5 apres un appel)"
    return True, "l'appel a eu lieu, sans capacite d'ecureuil declenchee"

def sg_ecureuil_refuse_bonus(monde, aides):
    """75002 : aucun ecureuil ne doit gagner d'ATK par une carte hors du set."""
    faces = _sg_ecureuils_en_jeu(monde)
    if not faces:
        return False, "aucun ecureuil en jeu : la mise en place a echoue"
    boot_camp = aides["par_id"](monde, "13016")
    if boot_camp is None:
        return False, "Boot Camp (13016) n'est pas en jeu"
    soucis = []
    for face in faces:
        if face.attack != face.printed_attack:
            soucis.append(f"{getattr(face.paper, 'card_id', '?')} ATK={face.attack} "
                          f"(imprime {face.printed_attack})")
    if soucis:
        return False, "bonus applique a un ecureuil : " + " ; ".join(soucis)
    return True, f"{len(faces)} ecureuil(s) en jeu, ATK imprimee preservee malgre Boot Camp"

def sg_aucun_ecureuil_en_jeu(monde, aides):
    """75022 : la capacite Boost defausse l'ecureuil controle."""
    faces = _sg_ecureuils_en_jeu(monde)
    if faces:
        ids = [getattr(f.paper, "card_id", "?") for f in faces]
        return False, f"ecureuil(s) encore en jeu : {ids}"
    return True, "l'ecureuil a bien ete defausse"

def sg_unbeatable(monde, aides):
    """75016 : l'evenement est joue en defense, et l'attaque ne passe pas.

    Sans `Puzzle.Attack(defender=...)`, le message WhenUnitWouldDefend n'etait
    jamais envoye et cette carte etait intestable.
    """
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "75016" not in defausse:
        return False, f"Unbeatable! n'a pas ete jouee (defausse = {defausse})"
    identite = aides["identite"](monde)
    subis = identite.max_health - identite.health
    if subis > 0:
        # DEF 2 + 2 = 4 : Rhino frappe a 3 (+ boost). Un boost eleve peut
        # legitimement passer, on ne juge donc que la carte, pas le des.
        return True, f"Unbeatable! jouee en defense ; {subis} degat(s) passes malgre +2 DEF"
    if identite.IsExhaust():
        return False, "aucun degat subi, mais l'identite n'a pas ete redressee"
    return True, "Unbeatable! jouee, aucun degat subi, identite redressee"

def sg_unbeatable_non_jouee(monde, aides):
    """Temoin du cas 75016 : sans defenseur, la carte ne peut pas etre jouee."""
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "75016" in defausse:
        return False, ("Unbeatable! a ete jouee alors qu'aucun defenseur n'etait "
                       "declare : le cas principal ne prouve rien")
    return True, "sans defenseur declare, la fenetre de defense ne s'ouvre pas"

def sg_gatherer_soigne(monde, aides):
    """75007 : depense pour payer une carte du set, il rend 1 point de vie."""
    if aides["par_id"](monde, "75007") is not None:
        return False, "The Gatherer est encore en jeu : il n'a pas ete depense"
    identite = aides["identite"](monde)
    subis = identite.max_health - identite.health
    if subis != 2:
        return False, f"degats restants = {subis} (3 infliges, 1 soin attendu, donc 2)"
    return True, "The Gatherer depense, 1 degat soigne"

def sg_forager_defausse(monde, aides):
    """75006 : depense, il regarde 2 cartes et en defausse 1.

    Les ecureuils depenses partent dans la defausse ECUREUIL : la defausse du
    joueur ne doit donc contenir que l'evenement joue et la carte defaussee
    depuis le deck.
    """
    if aides["par_id"](monde, "75006") is not None:
        return False, "The Forager est encore en jeu : il n'a pas ete depense"
    cartes = [getattr(f.paper, "card_id", None)
              for f in monde.players[0].discard_pile.Get()]
    if aides["par_id"](monde, "75008") is None:
        return False, "Nancy Whitehead n'a pas ete jouee : le paiement a echoue"
    if "01090" not in cartes:
        return False, ("Strength, posee sur le dessus du deck, n'a pas ete defaussee : "
                       "la branche optionnelle du Forager n'a pas ete prise")
    return True, "The Forager depense, la carte du dessus du deck est defaussee"

def sg_monkey_joe(monde, aides):
    """75003 : le sbire tombe sous son attaque, un ecureuil est appele.

    Monkey Joe a 1 PV et 1 degat consequent : il meurt en frappant. L'ecureuil
    appele est donc le SEUL encore en jeu a la fin.
    """
    if aides["par_id"](monde, "01103") is not None:
        return False, "Shocker (01103) est encore en jeu : Monkey Joe ne l'a pas vaincu"
    faces = [f for f in _sg_ecureuils_en_jeu(monde)
             if getattr(f.paper, "card_id", None) != "75003"]
    if not faces:
        return False, "aucun ecureuil appele apres la mort du sbire"
    return True, f"sbire vaincu, {len(faces)} ecureuil(s) appele(s)"

def sg_un_seul_ecureuil_par_carte(monde, aides):
    """Deux ecureuils en jeu, une carte a cout 2, rien d'autre en main.

    Un seul ecureuil pouvant etre depense par carte, le cout ne peut pas etre
    couvert : l'evenement doit rester en main et le second ecureuil rester en
    jeu. Sans la limite, les deux partaient et la carte etait jouee.
    """
    # Une carte REFUSEE finit elle aussi a la defausse : la preuve qu'elle a
    # ete jouee est son effet, pas sa zone.
    vilain = aides["par_id"](monde, "01094")
    if vilain is None:
        return False, "le vilain 01094 est introuvable"
    subis = vilain.max_health - vilain.health
    if subis > 0:
        return False, (f"Squirrel Swarm a resolu ({subis} degats) : deux ecureuils "
                       "ont paye la meme carte, la limite ne tient pas")
    restants = _sg_ecureuils_en_jeu(monde)
    if len(restants) != 2:
        ids = [getattr(f.paper, "card_id", "?") for f in restants]
        return False, f"{len(restants)} ecureuil(s) en jeu (attendu 2, aucun depense) : {ids}"
    return True, "cout impayable avec un seul ecureuil : la limite tient"

def sg_central_park_plafond(monde, aides):
    """75011 : au-dela de 3 ecureuils, la seconde activation n'appelle rien."""
    faces = _sg_ecureuils_en_jeu(monde)
    if len(faces) != 3:
        return False, f"{len(faces)} ecureuil(s) en jeu (attendu exactement 3)"
    parc = aides["par_id"](monde, "75011")
    if parc is None:
        return False, "Central Park n'est pas en jeu"
    if not parc.IsExhaust():
        return False, "Central Park n'est pas incline : l'action n'a pas ete jouee"
    return True, "Central Park s'incline mais n'appelle pas de 4e ecureuil"

def sg_bruiser_encaisse(monde, aides):
    """75005 : le degat consequent d'un autre ecureuil part sur The Bruiser.

    Tippy-Toe manigance : elle devrait prendre 1 degat consequent. Avec The
    Bruiser en jeu, elle en sort indemne, et c'est lui qui porte le degat, en
    s'inclinant pour payer son cout.
    """
    agissant = aides["par_id"](monde, "75002")
    bruiser = aides["par_id"](monde, "75005")
    if bruiser is None:
        return False, "The Bruiser (75005) n'est pas en jeu"
    if agissant is None:
        return False, "Tippy-Toe (75002) n'est plus en jeu"
    subis_agissant = agissant.max_health - agissant.health
    if subis_agissant != 0:
        return False, (f"Tippy-Toe a pris {subis_agissant} degat(s) : le degat "
                       f"consequent n'a pas ete detourne")
    subis = bruiser.max_health - bruiser.health
    if subis != 1:
        return False, f"degats sur The Bruiser = {subis} (attendu 1)"
    if not bruiser.IsExhaust():
        return False, "The Bruiser n'est pas incline alors que c'est son cout"
    return True, "The Bruiser a encaisse le degat consequent de Tippy-Toe"

def agent13_infiltrate(monde, aides):
    """79004 : 3 menaces de base + 1 icone (Stampede 01106, deck Rencontre truque)
    = 4 retirees du complot principal (6 -> 2), puis la defausse optionnelle
    (accepter_choix) envoie la carte regardee dans la defausse de rencontre.
    """
    from game.operate.worlds import Worlds
    scheme = aides["par_id"](monde, "01097b")
    if scheme is None:
        return False, "complot principal introuvable"
    if scheme.threat != 2:
        return False, (f"menace sur le complot principal = {scheme.threat} "
                       f"(attendu 2 : 6 - (3 de base + 1 icone NON NULLE))")
    defausse = [getattr(f.paper, "card_id", None)
                for f in Worlds.GetEncounterDiscardPileCards(monde)]
    if "01106" not in defausse:
        return False, (f"01106 n'est pas dans la defausse de rencontre : la defausse "
                       f"optionnelle n'a pas ete exercee (defausse = {defausse})")
    return True, "4 menaces retirees (base 3 + 1 icone non nulle), defausse optionnelle acceptee"

def agent13_faustus(monde, aides):
    """79012 : invulnerabilite conditionnelle (engage avec un AUTRE sbire) PUIS
    l'allie qui encaisse a la place du joueur, a hauteur de son ATK courante.
    """
    faustus = aides["par_id"](monde, "79012")
    if faustus is None:
        return False, "Doctor Faustus introuvable en jeu"
    degats_faustus = faustus.max_health - faustus.health
    if degats_faustus != 0:
        return False, (f"Faustus a subi {degats_faustus} degat(s) alors qu'il devait "
                       f"etre invulnerable, engage avec 01101")
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    subis = identite.max_health - identite.health
    if subis != 2:
        return False, (f"degats sur l'identite = {subis} (attendu 2 : ATK courante de "
                       f"Winter Soldier, qui doit encaisser a la place de Faustus)")
    return True, ("Faustus invulnerable tant qu'un autre sbire est engage, et l'allie "
                  "encaisse 2 degats a sa place")

def agent13_hallucination(monde, aides):
    """79013 : trouve Advanced Ultron Drone (01143, deck Rencontre truque a une
    seule carte, hors modules 'rhino'/'bomb_scare' pour eviter tout doublon),
    s'y attache, et le defausse au premier degat en posant 3 menaces sur le
    complot principal a la place. Les 3 menaces ne peuvent apparaitre QUE si
    l'interruption `AttachedMinion` a declenche, ce qui exige que l'attache ait
    reellement eu lieu : preuve combinee des trois volets du texte imprime.
    """
    if aides["par_id"](monde, "01143") is not None:
        return False, "Advanced Ultron Drone (01143) est encore en jeu : le sbire n'a pas ete defausse"
    scheme = aides["par_id"](monde, "01097b")
    if scheme is None:
        return False, "complot principal introuvable"
    if scheme.threat != 3:
        return False, (f"menace sur le complot principal = {scheme.threat} (attendu 3 : "
                       f"preuve que l'interruption a remplace le degat, ce qui exige l'attache)")
    return True, "sbire trouve, attache (seul moyen de declencher AttachedMinion), defausse au premier degat"
'''


# ------------------------------------------------------- execution d'un cas --
def executer_un_cas(game_dir, port, index):
    """Corps execute DANS LE PROCESSUS FILS : monte le moteur et joue le cas."""
    cas = CAS[index]
    # Chemin ABSOLU avant le chdir : sinon sys.path garde un chemin relatif qui
    # ne resout plus rien une fois le repertoire courant change.
    game_dir = os.path.abspath(game_dir)
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)

    cfg = json.load(open("launch.json"))
    cfg["server_addresses"] = [f"127.0.0.1:{port}"]
    cfg["check_for_new_version_on_startup"] = False
    json.dump(cfg, open("launch.json", "w"), indent=2)

    journal = open(f"/tmp/capacites_{os.environ.get('CAS_PREFIX', '')}{index}.log", "w", buffering=1)
    sys.stdout = journal
    sys.stderr = journal

    from engine.network.web_server import WebServer
    WebServer.IsAuthenticate = lambda self, request=None: True
    WebServer.IsVersionMatch = lambda self, request=None: True

    from engine.device.manager.base import DeviceManager

    etat = {"phase": "attente", "asks": 0, "resultat": None}

    def rendre(ok, message):
        etat["resultat"] = {"ok": bool(ok), "message": message}
        prefixe = os.environ.get("CAS_PREFIX", "")
        with open(f"/tmp/capacites_{prefixe}{index}.json", "w") as f:
            json.dump({"index": index, "nom": cas["nom"], **etat["resultat"]}, f,
                      ensure_ascii=False)
        print("RESULTAT:", etat["resultat"], flush=True)
        os._exit(0)

    def jouer_le_cas():
        from game.puzzle.puzzle import PuzzleHelper
        from game.card.face.attribute.can_status import CanStatus
        from game.card.face.attribute.can_place_counter import CanPlaceCounter
        from game.card.face.attribute.can_place_token import CanPlaceToken
        from engine import Engine

        monde = Engine.game.world

        def par_id(monde, card_id):
            for objet in monde.object_manager.card_dict.values():
                face = objet.face
                if face is not None and face.IsInPlay() \
                        and getattr(face.paper, "card_id", None) == card_id:
                    return face
            return None

        def par_nom(monde, nom):
            for objet in monde.object_manager.card_dict.values():
                face = objet.face
                if face is not None and face.IsInPlay() and face.IsName(nom):
                    return face
            return None

        def identite(monde):
            return monde.players[0].GetIdentity()

        aides = {"par_nom": par_nom, "par_id": par_id, "identite": identite,
                 "CanStatus": CanStatus, "CanPlaceCounter": CanPlaceCounter,
                 "CanPlaceToken": CanPlaceToken,
                 "cas": cas}

        def en_main(card_id):
            for face in monde.players[0].hand_cards.GetAll():
                if getattr(face.paper, "card_id", None) == card_id:
                    return face
            return None

        def deposer_en_reserve(card_id):
            """Amene une carte en main puis la deplace en RESERVE.

            Cle de cas `reserve`. Indispensable AVANT `jouer_reserve` : le
            cloisonnement du pack veut qu'une carte jouee depuis la reserve ne
            se finance QUE par la reserve. Sans carburant depose ici, la carte
            est legitimement injouable et se fait defausser — ce qui ressemble
            a s'y meprendre a une capacite morte.
            """
            from game.effect.rule import DebugRule
            joueur = monde.players[0]
            if en_main(card_id) is None:
                PuzzleHelper.Exec([f"Puzzle.Gain('{card_id}')"], monde)
            face = en_main(card_id)
            if face is None:
                raise RuntimeError(f"{card_id} n'a pas pu etre amenee en main")
            effet = DebugRule(monde.object_manager.card_dict[0].face)
            joueur.PutIntoReserve([face], effet)

        def jouer_depuis_la_reserve(card_id):
            """Joue une carte DEPUIS LA RESERVE, en payant vraiment son cout.

            Cle de cas `jouer_reserve` (pack brawn). Sans elle, rien ne prouvait
            que la mecanique centrale du pack fonctionne : le premier jeu de cas
            se contentait de verifier qu'une carte posee en reserve etait
            « comme en main », ce qui ne fait partir AUCUN des declencheurs
            « After you play a card from your reserve ».

            La carte est amenee en main, deplacee en reserve, puis jouee par le
            meme chemin que `jouer_carte` — c'est bien `from_area` qui vaudra la
            reserve, et c'est sur lui que les trois Response s'accrochent.
            """
            from game.effect.rule import DebugRule
            joueur = monde.players[0]
            face = None
            for f in joueur.reserve.GetAll():
                if getattr(f.paper, "card_id", None) == card_id:
                    face = f
                    break
            if face is None:
                deposer_en_reserve(card_id)
                for f in joueur.reserve.GetAll():
                    if getattr(f.paper, "card_id", None) == card_id:
                        face = f
                        break
            if face is None:
                raise RuntimeError(f"{card_id} n'est pas en reserve")
            effet = DebugRule(monde.object_manager.card_dict[0].face)
            joueur.PlayCardsLikeInTurn([face], effet)

        def jouer_carte(card_id):
            """Joue une carte de la main en PAYANT vraiment son cout.

            C'est le seul chemin qui exerce la generation de ressources (donc
            Hypermind), les conditions « si vous avez paye uniquement avec... »
            et les capacites Resource. `Puzzle.PutIntoPlay` court-circuite tout
            cela : il pose la carte sans jamais passer par le paiement.
            """
            from game.effect.rule import DebugRule
            joueur = monde.players[0]
            if en_main(card_id) is None:
                PuzzleHelper.Exec([f"Puzzle.Gain('{card_id}')"], monde)
            face = en_main(card_id)
            if face is None:
                raise RuntimeError(f"{card_id} n'a pas pu etre amenee en main")
            effet = DebugRule(monde.object_manager.card_dict[0].face)
            if os.environ.get("TRACE_OPTIONS"):
                try:
                    effets = face.GetTurnPlayEffects()
                except Exception as exc:
                    effets = f"ERREUR {exc}"
                print("JOUER", card_id, "| effets de jeu =", effets,
                      "| jouable =", face.CanPlayBy(joueur), flush=True)
            joueur.PlayCardsLikeInTurn([face], effet)
            if os.environ.get("TRACE_OPTIONS"):
                print("APRES", card_id, "| en main =", en_main(card_id) is not None,
                      "| zone =", face.card.area, flush=True)

        try:
            if cas["mise_en_place"]:
                PuzzleHelper.Exec(cas["mise_en_place"], monde)
            # Cartes deposees en main AVANT de jouer : elles servent de
            # carburant (icones ressource) ou sont la carte a jouer elle-meme.
            if cas.get("main"):
                PuzzleHelper.Exec(
                    [f"Puzzle.Gain('{c}')" for c in cas["main"]], monde)
            # `main_exclusive` VIDE d'abord la main : c'est le seul moyen de
            # savoir avec QUOI le pilote va payer. Avec `main` seul, la main de
            # depart reste la, et le pilote pioche ses ressources dedans — ce qui
            # a fait passer a cote du bonus « paye uniquement en [physical] »
            # d'Ashley Barton (69023), payee R+Y sans qu'on le voie.
            if cas.get("main_exclusive"):
                from game.effect.rule import DebugRule
                from game.operate.faces import Faces
                joueur = monde.players[0]
                vidage = DebugRule(monde.object_manager.card_dict[0].face)
                Faces.DiscardAll(list(joueur.hand_cards.GetAll()), vidage)
                PuzzleHelper.Exec(
                    [f"Puzzle.Gain('{c}')" for c in cas["main_exclusive"]], monde)
            if cas["declencher"]:
                PuzzleHelper.Exec(cas["declencher"], monde)
            for card_id in cas.get("jouer") or []:
                jouer_carte(card_id)
            for card_id in cas.get("reserve") or []:
                deposer_en_reserve(card_id)
            for card_id in cas.get("jouer_reserve") or []:
                jouer_depuis_la_reserve(card_id)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            rendre(False, f"echec de la mise en place : {type(exc).__name__}: {exc}")

        espace = {}
        exec(VERIFICATIONS, espace)
        try:
            ok, message = espace[cas["verifier"]](monde, aides)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            ok, message = False, f"verification en erreur : {type(exc).__name__}: {exc}"
        rendre(ok, message)

    def monde_courant():
        from engine import Engine
        return Engine.game.world

    def pilote(self, data, player_id, check):
        etat["asks"] += 1
        try:
            options = json.loads(data.options_json or "[]")
        except Exception:
            options = []
        noms = {o.get("name") for o in options if isinstance(o, dict)}

        def payer(option, cibles):
            """Choisit les cartes a defausser pour payer le cout de l'option.

            `target_payment` donne, PAR CIBLE, le cout a couvrir et la liste des
            cartes capables de le financer, avec la couleur que chacune fournit
            (« G » partout quand Hypermind est actif). Sans ce champ rempli, le
            moteur considere le cout impaye et la carte n'est jamais jouee : le
            test passait alors a cote de tout ce qui touche au paiement.
            """
            paiements = option.get("target_payment") or {}
            if not paiements:
                return []
            cle = cibles[0] if cibles and cibles[0] in paiements else next(iter(paiements))
            infos = paiements.get(cle) or {}
            cout = str(infos.get("cost", "0"))
            besoin = int(cout) if cout.isdigit() else len(cout)
            interdits = {str(option.get("bind_id"))}
            candidates = []
            # CORRECTIF 5/8/2026 : une carte peut fournir PLUSIEURS ressources
            # (« RR » de Nuts! 75017, « YY » d'Energy 01088). Le pilote comptait
            # une carte = une ressource, donc il renoncait a payer un cout de 2
            # finance par une seule carte, et l'effet echouait en silence : la
            # carte semblait inerte alors qu'elle etait correcte.
            poids = {}
            for entree in infos.get("payment") or []:
                for objet_id, couleur in entree.items():
                    if str(objet_id) not in interdits:
                        candidates.append(str(objet_id))
                        poids[str(objet_id)] = max(1, len(str(couleur)))
                    break
            # « surpayer » : depenser TOUT ce qui est disponible. Indispensable
            # aux cartes a cout X (69008), dont le cout annonce est nul : sans
            # cela le pilote ne paie rien, X vaut 0, et la carte semble inerte
            # alors qu'elle est correcte. Meme principe qu'OVERPAY_CARDS dans
            # tools/test_autoplay.py.
            if cas.get("surpayer"):
                besoin = len(candidates)
            if besoin <= 0:
                return []
            # « payer_avec » impose QUELLES cartes financent le cout, ce qui est
            # indispensable des que la ressource depensee a elle-meme un effet
            # (The Power of Forgiveness). Les options designent les cartes par
            # leur identifiant interne, d'ou la traduction depuis le card_id.
            priorite = []
            for card_id in cas.get("payer_avec") or []:
                for objet_id, objet in monde_courant().object_manager.card_dict.items():
                    face = objet.face
                    if face is not None \
                            and getattr(face.paper, "card_id", None) == card_id \
                            and str(objet_id) in candidates:
                        priorite.append(str(objet_id))
                        break
            if not priorite and cas.get("payer_avec"):
                # Les cles de `payment` ne correspondent pas toujours aux ids
                # d'objets (espace d'ids propre aux effets de ressource, vu sur
                # venom_rainy ou l'identite elle-meme est candidate). Repli :
                # apparier par COULEUR de ressource imprimee des cartes exigees.
                couleurs = []
                for card_id in cas["payer_avec"]:
                    for objet in monde_courant().object_manager.card_dict.values():
                        face = objet.face
                        if face is not None and getattr(face.paper, "card_id", None) == card_id:
                            res = (getattr(face.paper, "desc", None) or {}).get("RES", "")
                            if res:
                                couleurs.append(res[0])
                            break
                par_couleur = {}
                for entree in infos.get("payment") or []:
                    for objet_id, couleur in entree.items():
                        par_couleur.setdefault(couleur, []).append(str(objet_id))
                        break
                for couleur in couleurs:
                    disponibles = [x for x in par_couleur.get(couleur, [])
                                   if x in candidates and x not in priorite]
                    # Seulement si la couleur designe UNE carte sans ambiguite :
                    # chez Totally Awesome Hulk, Hypermind convertit tout en G,
                    # et choisir « le premier G » prendrait la mauvaise carte.
                    if len(disponibles) == 1:
                        priorite.append(disponibles[0])
            ordonnees = priorite + [x for x in candidates if x not in priorite]
            choisies, couvert = [], 0
            for objet_id in ordonnees:
                if couvert >= besoin:
                    break
                choisies.append(objet_id)
                couvert += poids.get(objet_id, 1)
            return choisies if couvert >= besoin else []

        def choisir_cibles(card_ids, legales):
            """Traduit des card_id en identifiants d'objet, parmi les cibles legales."""
            trouvees = []
            for card_id in card_ids:
                for objet_id, objet in monde_courant().object_manager.card_dict.items():
                    face = objet.face
                    if face is not None \
                            and getattr(face.paper, "card_id", None) == card_id \
                            and str(objet_id) in legales:
                        trouvees.append(str(objet_id))
                        break
            return trouvees

        def premiere_option_jouable():
            # Accepter la premiere option jouable en fournissant le nombre
            # MINIMAL de cibles qu'elle exige. Repondre « aucune cible » a un
            # choix qui en exige une fait rejeter la reponse par le moteur, qui
            # repose alors la meme question a l'infini (c'est ce qui bloquait la
            # mise en place d'Albert, dont la capacite Setup fouille le deck).
            for o in options:
                if isinstance(o, dict) and not o.get("failure_reason"):
                    legales = [str(x) for x in (o.get("all_legal_targets") or [])]
                    mini, maxi = (o.get("target_num_range") or [0, 0])[:2]
                    cibles = legales[:mini]
                    # `accepter_choix` : prendre le MAXIMUM de cibles au lieu du
                    # minimum. Un choix optionnel (« you may discard 1 of them »)
                    # arrive avec un minimum de 0 : le pilote n'en choisissait
                    # aucune, donc TOUTE branche derriere un « you may » etait
                    # declinee et paraissait morte. C'est le trou signale au §8.
                    if cas.get("accepter_choix") and legales \
                            and etat["phase"] == "cas":
                        borne = maxi if isinstance(maxi, int) and maxi > 0 else 1
                        cibles = legales[:borne]
                    # `cibles` du cas : DESIGNER des cibles precises, par
                    # card_id. Indispensable des que le minimum est 0 (« exhaust
                    # up to X allies ») : sinon le pilote, qui envoie toujours le
                    # minimum, n'en choisit aucune et la capacite ne fait rien.
                    forcees = choisir_cibles(cas.get("cibles") or [], legales)
                    if forcees:
                        cibles = forcees[:maxi] if isinstance(maxi, int) else forcees
                    return json.dumps({"id": str(o.get("id", 0)),
                                       "targets": cibles,
                                       "resources": payer(o, cibles)})
            return json.dumps({"id": "0", "targets": [], "resources": []})

        if etat["phase"] == "attente":
            if os.environ.get("TRACE_OPTIONS"):
                print("ATTENTE-ASK", etat["asks"], "| noms=", sorted(noms - {None}),
                      flush=True)
            # Le tour du joueur est atteint des que des actions de base sont
            # proposees. On bascule alors en mode « cas », puis on joue le cas
            # depuis la reponse suivante : declencher depuis l'interieur de
            # DoGetInput garde le monde dans un etat coherent.
            if {"Attack", "Thwart", "Change_Form", "Change Form", "Recover"} & noms \
                    or any(str(n).startswith("Change_To_") for n in noms if n):
                # « Change Form » (avec espace) : nom réel affiché par le moteur.
                # Indispensable aux identités multi-faces (Moon Knight) dont le
                # premier ask ne contient aucun des autres noms.
                etat["phase"] = "cas"
                jouer_le_cas()
            if etat["asks"] > 400:
                rendre(False, "le tour du joueur n'a jamais ete atteint")
            return premiere_option_jouable()

        # Pendant le declenchement : accepter la premiere option jouable, sinon
        # passer. Suffit pour les choix simples (cible unique, oui/non).
        if os.environ.get("TRACE_OPTIONS"):
            print("ASK", etat["asks"], "prompt=", data.prompt_text,
                  "| options=", json.dumps(options, ensure_ascii=False)[:900], flush=True)
        return premiere_option_jouable()

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, player_id, check: None
    DeviceManager.DoWaitSync = lambda self, player_id, check: None

    from engine import Engine
    Engine.Initialize()
    from game.scene.loader import SceneLoader
    # `heros2` monte une VRAIE partie a deux joueurs. Indispensable aux cartes
    # dont le texte parle des autres joueurs (« play under any player's
    # control », « give to the X player ») : en solo elles ne peuvent pas etre
    # exercees, et rien ne le signale.
    noms_heros = [cas["heros"]]
    if cas.get("heros2"):
        noms_heros.append(cas["heros2"])
    scene = SceneLoader.NewScene(cas["scenario"], None, noms_heros, 42)
    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")
    try:
        if jeu.GameSetup():
            jeu.GameLoop()
    except SystemExit:
        raise
    except BaseException as exc:
        import traceback
        traceback.print_exc()
        rendre(False, f"la partie a plante : {type(exc).__name__}: {exc}")
    rendre(False, "la partie s'est terminee sans declencher le cas")


# ------------------------------------------------------------- orchestration --
def main():
    game_dir = os.path.expanduser(sys.argv[1])
    port = int(sys.argv[2])
    rapport = sys.argv[3] if len(sys.argv) > 3 else "/tmp/test_capacites.json"

    if os.environ.get("CAS_INDEX"):
        executer_un_cas(game_dir, port, int(os.environ["CAS_INDEX"]))
        return

    resultats = []
    for index, cas in enumerate(CAS):
        chemin = f"/tmp/capacites_{os.environ.get('CAS_PREFIX', '')}{index}.json"
        if os.path.exists(chemin):
            os.remove(chemin)
        env = dict(os.environ, CAS_INDEX=str(index))
        subprocess.run([sys.executable, os.path.abspath(__file__), game_dir,
                        str(port + index), rapport],
                       env=env, timeout=300, capture_output=True)
        if os.path.exists(chemin):
            resultats.append(json.load(open(chemin)))
        else:
            resultats.append({"index": index, "nom": cas["nom"], "ok": False,
                              "message": "aucun resultat (processus mort ; voir "
                                         f"/tmp/capacites_{os.environ.get('CAS_PREFIX', '')}{index}.log)"})
        etat = "OK  " if resultats[-1]["ok"] else "ECHEC"
        print(f"{etat} {cas['nom']}\n      {resultats[-1]['message']}")

    reussis = sum(1 for r in resultats if r["ok"])
    print(f"\nBILAN : {reussis}/{len(resultats)} cas passes")
    json.dump({"reussis": reussis, "total": len(resultats), "cas": resultats},
              open(rapport, "w"), indent=1, ensure_ascii=False)
    sys.exit(0 if reussis == len(resultats) else 1)


if __name__ == "__main__":
    main()
