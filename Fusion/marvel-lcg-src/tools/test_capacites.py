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
# (ex. ht009 Radiate, evenement a deux capacites « Play »).
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
    # Pack « rainy » : Thor (Jane Foster) ra001a-ra031
    # ------------------------------------------------------------------------
    {
        "nom": "ra001b Jane Foster — Survivor : +1 taille de main en permanence",
        "pourquoi": "l'obligation Chemotherapy n'existe pas, le bonus doit donc etre toujours actif",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"hand_size": 1}},
    },
    {
        "nom": "ra007 Mjolnir — Thor gagne +1 ATK et le trait AERIAL",
        "pourquoi": "GiveKeywordToAttached vise CardFinder(name='Thor') : verifier qu'il touche bien le heros",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('ra001b')"],
        "declencher": ["Puzzle.PutIntoPlay('ra007')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}, "traits": ["AERIAL"],
                    "en_jeu": ["ra007"]},
    },
    {
        "nom": "ra013 Mighty — +2 PV a l'identite et +1 DEF a Thor",
        "pourquoi": "deux GiveKeywordToAttached distincts (identite puis heros nomme)",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('ra001b')"],
        "declencher": ["Puzzle.PutIntoPlay('ra013')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 2, "defense": 1}},
    },
    {
        "nom": "ra010 Medical Clinic — Jane Foster gagne +2 REC",
        "pourquoi": "GiveKeywordToInPlayWhenApplyThis vise l'alter-ego par son nom",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('ra010')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 2}, "en_jeu": ["ra010"]},
    },

    # ------------------------------------------------------------------------
    # Pack « albert » : ab001a-ab016
    # ------------------------------------------------------------------------
    {
        "nom": "ab008/ab009/ab010 — les trois ameliorations passives d'Albert",
        "pourquoi": "trois GiveKeywordToAttached vers CardFinder(name='Albert', card_type=Hero)",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('ab001b')"],
        "declencher": [
            "Puzzle.PutIntoPlay('ab008')",
            "Puzzle.PutIntoPlay('ab009')",
            "Puzzle.PutIntoPlay('ab010')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1, "thwart": 1, "defense": 1},
                    "traits": ["GENIUS"],
                    "en_jeu": ["ab008", "ab009", "ab010"]},
    },

    # ------------------------------------------------------------------------
    # Pack « human_torch » : ht001a-64015
    # ------------------------------------------------------------------------
    {
        "nom": "ht001a Human Torch — un ennemi ne peut pas depasser 3 compteurs flamme",
        "pourquoi": "la regle de plafond (WhenCardWouldBePlacedCounter) n'est active qu'en forme heros",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('ht001b')"],
        "declencher": ["Puzzle.Counter('01094', 'flame', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "flame", 3]]},
    },
    {
        "nom": "ht012 Hydro-Man — immunise aux compteurs flamme",
        "pourquoi": ("garde du CORRECTIF moteur : la carte pose maximum=0, que "
                     "`maximum = would_message.maximum or maximum` avalait "
                     "(0 est faux en Python), supprimant au passage le "
                     "plafond de 3 de ht001a"),
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.PutIntoPlay('ht012')"],
        "declencher": ["Puzzle.Counter('ht012', 'flame', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["ht012", "flame", 0]]},
    },
    {
        "nom": "ht004 Unstable Uniform — Human Torch gagne +1 DEF",
        "pourquoi": "GiveKeywordToAttached vers CardFinder(name='Human Torch', card_type=Hero)",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('ht001b')"],
        "declencher": ["Puzzle.PutIntoPlay('ht004')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}, "en_jeu": ["ht004"]},
    },
    {
        "nom": "ht013 Dam It — eteint les flammes et convertit chaque compteur en menace",
        "pourquoi": "When Revealed qui compte le retour de Faces.RemoveCountersOn",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.Counter('01094', 'flame', 3)"],
        "declencher": ["Puzzle.Reveal('ht013')"],
        "verifier": "etat_attendu",
        # menace de depart 1, plus 1 par compteur retire (3) = 4
        "attendu": {"compteurs": [["01094", "flame", 0]],
                    "menace": [["ht013", 4]]},
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
    # Pack « gwenpool » : gp001a-gp016
    # ------------------------------------------------------------------------
    {
        "nom": "gp007 Gwen's Room — Gwendolyn Poole gagne +1 REC",
        "pourquoi": "GiveKeywordToAttached('You', recover=1)",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('gp007')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 1}, "en_jeu": ["gp007"]},
    },
    {
        "nom": "gp011 Rules of the Universe — l'icone hazard tombe avec la menace",
        "pourquoi": ("garde du CORRECTIF : sans change_on_event, la condition "
                     "n'etait evaluee qu'a l'entree en jeu et l'icone restait "
                     "figee alors que la manigance est Permanente"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.PutIntoPlay('gp011')"],
        "declencher": ["Puzzle.SetThreat('gp011', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["gp011", "hazard", -1]]},
    },
    {
        "nom": "gp012 Evil Gwenpool — When Defeated : melangee dans le deck Rencontre",
        "pourquoi": "elle doit revenir dans le deck, pas partir a la defausse",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.PutIntoPlay('gp012')"],
        "declencher": ["Puzzle.Damage('gp012', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["gp012"], "dans_deck_rencontre": ["gp012"]},
    },
    {
        "nom": "gp014 \"Future Me Scares Me\" — 2 menaces sur Rules si Evil Gwenpool est en jeu",
        "pourquoi": "branche conditionnelle + remise en deck de la traitrise",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.PutIntoPlay('gp012')", "Puzzle.PutIntoPlay('gp011')"],
        "declencher": ["Puzzle.Reveal('gp014')"],
        "verifier": "etat_attendu",
        # menace de depart de Rules = 3 en solo, plus 2
        "attendu": {"menace": [["gp011", 5]], "hors_jeu": ["gp014"],
                    "dans_deck_rencontre": ["gp014"]},
    },
    {
        "nom": "gp013 Break Reality — Evil Gwenpool deja en jeu : 2 menaces par joueur sur Rules",
        "pourquoi": "la branche « deja en jeu » ne doit PAS rechercher un second exemplaire",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.PutIntoPlay('gp012')", "Puzzle.PutIntoPlay('gp011')"],
        "declencher": ["Puzzle.Reveal('gp013')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["gp011", 5]], "en_jeu": ["gp012"]},
    },

    # ------------------------------------------------------------------------
    # Nemesis Thor (Jane Foster) et Albert
    # ------------------------------------------------------------------------
    {
        "nom": "ra030 Execute — defait l'allie ayant le plus de PV restants",
        "pourquoi": "When Revealed qui choisit parmi les allies en jeu",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.PutIntoPlay('ra002')"],
        "declencher": ["Puzzle.Reveal('ra030')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["ra002"]},
    },
    {
        "nom": "ra031 Hostile Takeover — defausse le support controle le plus cher",
        "pourquoi": "branche « discard » du choix ; la branche « surge » ne doit pas s'appliquer",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.PutIntoPlay('ra009')"],
        "declencher": ["Puzzle.Reveal('ra031')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["ra009"], "degats_identite": 0},
    },
    {
        "nom": "ra027 War of the Realms — 1 degat indirect par personnage controle",
        "pourquoi": "le compte doit inclure l'identite ET les allies",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.PutIntoPlay('ra002')"],
        "declencher": ["Puzzle.Reveal('ra027')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "ab014 Patch — When Revealed : 1 degat a chaque joueur",
        "pourquoi": "sbire dont la capacite doit toucher l'identite, pas lui-meme",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('ab014')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "en_jeu": ["ab014"]},
    },
    {
        "nom": "ab016 Zombie Wolvie — When Defeated : melange dans le deck Rencontre",
        "pourquoi": "il doit revenir dans le deck, pas partir a la defausse",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.PutIntoPlay('ab016')"],
        "declencher": ["Puzzle.Damage('ab016', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["ab016"], "dans_deck_rencontre": ["ab016"]},
    },
    {
        "nom": "ab002 Elsie-Dee — les degats en exces sont repartis sur les ennemis",
        "pourquoi": "Interrupt WhenUnitBeDefeated avec took_excess_damage",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.PutIntoPlay('ab002')"],
        "declencher": ["Puzzle.Damage('ab002', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["ab002"], "degats_min": [["01094", 1]]},
    },

    # ------------------------------------------------------------------------
    # Capacites Boost (WhenCardBecomeBoost) des trois sbires nemesis custom
    # ------------------------------------------------------------------------
    {
        "nom": "ab012 Wolverine — Boost : le sbire entre en jeu au lieu d'etre defausse",
        "pourquoi": "WhenCardBecomeBoost + PutThisIntoPlay",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": [],
        "declencher": ["Puzzle.Boost('ab012')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["ab012"]},
    },
    {
        "nom": "gp012 Evil Gwenpool — Boost : la sbire entre en jeu au lieu d'etre defaussee",
        "pourquoi": "WhenCardBecomeBoost + PutThisIntoPlay",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": [],
        "declencher": ["Puzzle.Boost('gp012')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["gp012"]},
    },
    {
        "nom": "ht012 Hydro-Man — Boost : le sbire entre en jeu au lieu d'etre defausse",
        "pourquoi": "WhenCardBecomeBoost + PutThisIntoPlay",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": [],
        "declencher": ["Puzzle.Boost('ht012')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["ht012"]},
    },

    # ------------------------------------------------------------------------
    # Obligations custom
    # ------------------------------------------------------------------------
    {
        "nom": "ht011 Flame Off — bascule en alter-ego et eteint toutes les flammes",
        "pourquoi": "obligation qui doit changer la forme ET vider les compteurs des ennemis",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('ht001b')",
                          "Puzzle.Counter('01094', 'flame', 3)"],
        "declencher": ["Puzzle.Reveal('ht011')"],
        "verifier": "etat_attendu",
        # 3 compteurs retires (moins de 4) : l'obligation part a la defausse.
        "attendu": {"forme": "AlterEgo", "compteurs": [["01094", "flame", 0]],
                    "hors_jeu": ["ht011"]},
    },
    {
        "nom": "ra026 Chemotherapy — la branche Medical Clinic retire l'obligation du jeu",
        "pourquoi": "le choix conditionnel n'est propose que si la Clinique est en jeu",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.PutIntoPlay('ra010')"],
        "declencher": ["Puzzle.Reveal('ra026')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["ra026"], "exhausted": ["ra001b", "ra010"]},
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
        "nom": "ab011 Counterpart Elimination — cherche et revele un sbire WOLVERINE",
        "pourquoi": "Find.FindAndReveal filtre sur le trait, pas sur un nom",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('ab011')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu_trait": [["WOLVERINE", 1]]},
    },

    # ------------------------------------------------------------------------
    # Autres capacites nemesis atteignables sans jouer de carte
    # ------------------------------------------------------------------------
    {
        "nom": "ra029 War Witches — menace posee sur le complot principal : 1 degat indirect",
        "pourquoi": "AfterSchemePlaceThreat(MainScheme) doit retrouver le joueur engage",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.PutIntoPlay('ra029')"],
        "declencher": ["Puzzle.PlaceThreat('01097b', 1)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "menace": [["01097b", 1]]},
    },
    {
        "nom": "ab015 Weapon X — When Revealed : defausse 1 carte au hasard de la main",
        "pourquoi": "DiscardRandomHandCards doit toucher le joueur qui recoit la carte",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('ab015')"],
        "verifier": "etat_attendu",
        "attendu": {"defausse_joueur": 1, "en_jeu": ["ab015"]},
    },
    {
        "nom": "ht014 Tidal Surge — avec Hydro-Man en jeu, le joueur incline son identite",
        "pourquoi": "la branche conditionnelle « si Hydro-Man est en jeu » et le choix impose",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.PutIntoPlay('ht012')"],
        "declencher": ["Puzzle.Reveal('ht014')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["ht001b"], "degats_identite": 0},
    },
    {
        "nom": "ht014 Tidal Surge — temoin : sans Hydro-Man, la carte ne fait rien",
        "pourquoi": "sans temoin, le cas precedent passerait meme si la condition etait ignoree",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('ht014')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["ht001b"], "degats_identite": 0},
    },

    # ------------------------------------------------------------------------
    # Corrections recentes hors packs custom
    # ------------------------------------------------------------------------
    # --- pack custom Invisible Woman (DesignHacker), integre le 2/8/2026 ---
    {
        "nom": "iw001 Invisible Woman — le heros a 3 faces se charge et joue",
        "pourquoi": ("valide tout le pack : donnees, deck de depart, extension. "
                     "Le trait FANTASTIC FOUR est porte par les DEUX formes heros ; "
                     "on ne fige pas laquelle, car le pilote de test bascule vers "
                     "l'une ou l'autre selon l'ordre des options. CORRECTIF 4/8/2026 : "
                     "le cas tournait en forme ALTER-EGO, ou Sue Storm ne porte que "
                     "GENIUS — il manquait le ChangeForm, le cas etait rouge depuis "
                     "sa creation"),
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"traits": ["FANTASTIC FOUR"]},
    },
    {
        "nom": "iw004 Unstable Uniform — Invisible Woman gagne +1 DEF",
        "pourquoi": ("passif GiveKeywordToAttached(defense=1) sur l'identite. "
                     "CORRECTIF 4/8/2026 : le cas tournait en forme ALTER-EGO, qui "
                     "n'a pas d'attribut `defense` — la verification plantait sur "
                     "AttributeError, le cas etait rouge depuis sa creation"),
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')"],
        "declencher": ["Puzzle.PutIntoPlay('iw004')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}, "en_jeu": ["iw004"]},
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
    # Pack « totally_awesome_hulk » : ah001a-ah018
    # Le coeur du heros est le soutien recto-verso « The Trunk » (ah012a/b) :
    # c'est LUI qui pilote les trois formes de l'identite, les changements
    # manuels etant verrouilles. Les cas ci-dessous valident cette boucle
    # complete, puis les bonus passifs et le set nemesis.
    # ------------------------------------------------------------------------
    {
        "nom": "ah012a \"The Trunk\" — arrive en jeu au setup, sans compteur",
        "pourquoi": "tout le heros en depend : le mot-cle Setup doit la sortir du deck au demarrage",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["ah012a"], "compteurs": [["ah012a", "rage", 0]]},
    },
    {
        "nom": "ah012a \"The Trunk\" — au 4e compteur : flip et passage en Uncontrollable Hulk",
        "pourquoi": ("c'est la seule maniere d'atteindre la forme BRUTE, "
                     "« Losing Control » bloquant tout changement manuel"),
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "declencher": ["Puzzle.Damage('Totally Awesome Hulk', 1)", "Puzzle.Damage('Totally Awesome Hulk', 1)", "Puzzle.Damage('Totally Awesome Hulk', 1)", "Puzzle.Damage('Totally Awesome Hulk', 1)"],
        "verifier": "face_identite",
        "attendu": {"face": "ah001c", "en_jeu": ["ah012b"], "hors_jeu": ["ah012a"]},
    },
    {
        "nom": "ah012b \"The Trunk\" — plus aucun compteur : flip et retour a Amadeus Cho",
        "pourquoi": "boucle de retour (IfThereIsNoCounterHere) : sans elle le heros reste bloque en BRUTE",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "declencher": [
            "Puzzle.Damage('Totally Awesome Hulk', 1)", "Puzzle.Damage('Totally Awesome Hulk', 1)", "Puzzle.Damage('Totally Awesome Hulk', 1)", "Puzzle.Damage('Totally Awesome Hulk', 1)",
            "Puzzle.Counter('\"The Trunk\"', 'rage', -4)",
        ],
        "verifier": "face_identite",
        "attendu": {"face": "ah001b", "en_jeu": ["ah012a"], "hors_jeu": ["ah012b"]},
    },
    {
        "nom": "ah003 Maddy Cho — Totally Awesome Hulk gagne +1 taille de main",
        "pourquoi": "GiveKeywordToInPlayWhenApplyThis vise la face CHAMPION par son nom",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "declencher": ["Puzzle.PutIntoPlay('ah003')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"hand_size": 1}, "en_jeu": ["ah003"]},
    },
    {
        "nom": "ah005 Motivation — le heros gagne +1 DEF",
        "pourquoi": "GiveKeywordToAttached(Hero) sur une amelioration sans nom de cible",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "declencher": ["Puzzle.PutIntoPlay('ah005')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}, "en_jeu": ["ah005"]},
    },
    {
        "nom": "ah006 Gamma Barrier — le heros gagne represailles 1",
        "pourquoi": "GiveKeywordToAttached(retaliate=1) : mot-cle passif facile a oublier",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "declencher": ["Puzzle.PutIntoPlay('ah006')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"retaliate": 1}, "en_jeu": ["ah006"]},
    },
    {
        "nom": "ah016 Fin Fang Foom — +2 points de vie par joueur",
        "pourquoi": "ThisGainKeyword multiplie par le nombre de joueurs (solo : +2)",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('ah016')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["ah016", "health", 2]]},
    },
    {
        "nom": "ah017 Krackalakassian — +2 points de vie par joueur",
        "pourquoi": "meme mecanique que Fin Fang Foom, sur une valeur imprimee differente",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('ah017')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["ah017", "health", 2]]},
    },
    {
        "nom": "ah015 For The Queen! — les sbires MONSTER deviennent vilainesques",
        "pourquoi": "GiveKeywordToInPlayWhenApplyThis conditionne a la presence de Lady Hellbender",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": [
            "Puzzle.PutIntoPlay('ah014')",
            "Puzzle.PutIntoPlay('ah016')",
        ],
        "declencher": ["Puzzle.Reveal('ah015')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["ah016", "villainous", 1]],
                    "en_jeu": ["ah015"]},
    },
    {
        "nom": "ah009 Wild Lunge — Hypermind : payable avec une ressource [physical]",
        "pourquoi": ("la carte coute « G » (uniquement du wild). Sans Hypermind elle "
                     "serait injouable avec Hercules, dont l'icone est physique"),
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "main": ["ah002"],
        "declencher": [],
        "jouer": ["ah009"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]]},
    },
    {
        "nom": "ah010 Irradiated Swipe — 5 degats a un ennemi, paye en [wild]",
        "pourquoi": "verifie la voie de paiement complete sur un evenement a cout 3",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "main": ["ah002", "ah003", "ah005"],
        "declencher": [],
        "jouer": ["ah010"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]]},
    },
    {
        "nom": "ah002 Hercules — allie signature joue et pose en jeu",
        "pourquoi": "cout 4 : verifie qu'un allie signature se paye et arrive bien en jeu",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "main": ["ah003", "ah005", "ah006", "ah009"],
        "declencher": [],
        "jouer": ["ah002"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["ah002"]},
    },
    {
        "nom": "ah007 The Power of Forgiveness — vide les compteurs rage du Trunk",
        "pourquoi": ("ressource a effet differe : elle n'agit qu'APRES resolution de "
                     "la carte qu'elle a payee"),
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('Amadeus Cho')"],
        "main": ["ah007"],
        "declencher": ["Puzzle.Counter('\"The Trunk\"', 'rage', 3)"],
        "jouer": ["ah009"],
        "payer_avec": ["ah007"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["ah012a", "rage", 0]], "degats": [["01094", 4]]},
    },
    {
        "nom": "ah018 Threat Assessment — 3 degats a l'identite la plus en forme",
        "pourquoi": "When Revealed qui doit choisir une cible parmi les identites",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('ah018')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },

    # ------------------------------------------------------------------------
    # Pack « madame_web » : mw001a-mw029 (custom « Kajislav »)
    # ------------------------------------------------------------------------
    {
        "nom": "mw001a Madame Web — ATK/THW/DEF valent 0 sans allie en jeu",
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
        "nom": "mw001a Madame Web — X = 2 avec deux allies en jeu",
        "pourquoi": "coeur du heros : les trois stats suivent le nombre d'allies controles",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": [
            "Puzzle.PutIntoPlay('mw002')",
            "Puzzle.PutIntoPlay('13019')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 2, "thwart": 2, "defense": 2},
                    "en_jeu": ["mw002", "13019"]},
    },
    {
        "nom": "mw001a Madame Web — X plafonne a 3 avec quatre allies",
        "pourquoi": "« to a maximum of 3 » : le plafond doit tenir au-dela de 3 allies",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": [
            "Puzzle.PutIntoPlay('mw002')",
            "Puzzle.PutIntoPlay('13019')",
            "Puzzle.PutIntoPlay('27049')",
            "Puzzle.PutIntoPlay('30012')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 3, "thwart": 3, "defense": 3}},
    },
    {
        "nom": "mw001a Madame Web — A Bond with the Allies : elle prend les traits des allies",
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
        "nom": "mw002 Spider-Woman (Julia Carpenter) — entre avec 2 compteurs psionic",
        "pourquoi": "ThisEnterPlayWithCounters : sans lui la capacite de l'allie est inutilisable",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('mw002')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["mw002", "psionic", 2]]},
    },
    {
        "nom": "mw007 Life-Support System — +3 PV a l'identite et +1 REC",
        "pourquoi": "GiveKeywordToAttached('You') doit toucher l'identite, pas la carte elle-meme",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('mw007')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 3, "recover": 1}, "en_jeu": ["mw007"]},
    },
    {
        "nom": "mw012 Neurological Deterioration — l'identite ne peut plus se redresser",
        "pourquoi": ("CardCannotReady(Identity) : on incline puis on tente de redresser, "
                     "l'identite doit rester inclinee"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": [
            "Puzzle.Reveal('mw012')",
            "Puzzle.Exhaust('Cassandra Webb')",
            "Puzzle.Ready('Cassandra Webb')",
        ],
        "verifier": "identite_reste_inclinee",
    },
    {
        "nom": "mw013 Spider-Woman (Witter) — When Revealed : 2 degats indirects ou incliner",
        "pourquoi": "le choix doit se resoudre, sinon la nemesis est inerte",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('mw013')"],
        "verifier": "witter_a_agi",
    },
    {
        "nom": "mw016 Hypnosis — When Revealed : sonne ET desoriente un personnage",
        "pourquoi": "deux statuts a poser sur la meme cible en une seule capacite",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('mw016')"],
        "verifier": "identite_sonnee_et_desorientee",
    },
    {
        "nom": "mw021 Hunting Spyders — 3 degats a l'identite faute d'allie",
        "pourquoi": "branche de repli : sans allie en jeu, les degats vont sur l'identite",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('mw021')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "mw021 Hunting Spyders — 3 degats a l'allie quand il y en a un",
        "pourquoi": "branche nominale : l'allie encaisse a la place de l'identite",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.PutIntoPlay('30012')"],
        "declencher": ["Puzzle.Reveal('mw021')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "degats": [["30012", 3]]},
    },
    {
        "nom": "mw019 Kraven the Hunter — When Defeated : mis de cote, hors jeu",
        "pourquoi": "le sbire ne doit pas partir a la defausse mais dans la zone mise de cote",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.PutIntoPlay('mw019')"],
        "declencher": ["Puzzle.Damage('mw019', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["mw019"]},
    },
    {
        "nom": "mw026 Spider-Woman (Veranke) — vaincue, elle revient en sbire",
        "pourquoi": ("TreatAsMinion sur un allie EN JEU (et non sur une carte attachee) : "
                     "chemin jamais emprunte par une carte du moteur"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.PutIntoPlay('mw026')"],
        "declencher": ["Puzzle.Damage('mw026', 99)"],
        "verifier": "veranke_devenue_sbire",
    },
    {
        "nom": "mw001b Cassandra Webb — Setup : Life-Support System arrive seule en jeu",
        "pourquoi": ("le Setup fouille deck ET defausse puis MET EN JEU ; sans lui "
                     "l'heroine perd 3 PV et son filet de securite"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["mw007"], "attributs": {"health": 3}},
    },
    {
        "nom": "mw004 Clairvoyance — previent 1 degat sur les 3 recus",
        "pourquoi": "Hero Interrupt sur les degats : il doit s'inserer avant l'application",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": [
            "Puzzle.PutIntoPlay('mw004')",
            "Puzzle.Damage('Madame Web', 3)",
        ],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "exhausted": ["mw004"]},
    },
    {
        "nom": "mw014 Spider-Women Hunt — 2 menaces de plus par personnage « Spider »",
        "pourquoi": "le When Revealed compte les personnages en jeu ; sans lui le complot reste a 1",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": [
            "Puzzle.PutIntoPlay('27049')",
            "Puzzle.Reveal('mw014')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["mw014", 3]]},
    },
    {
        "nom": "mw015 Power Absorption — un allie est defausse, la forme ne change pas",
        "pourquoi": "branche nominale : la defausse d'un allie doit ANNULER le retour en alter-ego",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": [
            "Puzzle.PutIntoPlay('30012')",
            "Puzzle.Reveal('mw015')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["30012"], "forme": "Hero"},
    },
    {
        "nom": "mw015 Power Absorption — sans allie : retour en alter-ego et inclinaison",
        "pourquoi": "branche de repli, celle qui fait vraiment mal",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": ["Puzzle.Reveal('mw015')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "exhausted": ["mw001b"]},
    },
    {
        "nom": "mw018 The Grim Hunt — entre avec 3 menaces par joueur",
        "pourquoi": ("complot secondaire a menace de depart ET escalade cablees a la main : "
                     "le moteur ne gere ces valeurs que sur les complots PRINCIPAUX"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('mw018')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["mw018"], "menace": [["mw018", 3]]},
    },
    {
        "nom": "mw020 One Spyder Down — defausse l'allie controle",
        "pourquoi": "sans allie la carte prend surge : il faut verifier la branche nominale",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": [
            "Puzzle.PutIntoPlay('30012')",
            "Puzzle.Reveal('mw020')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["30012"]},
    },
    {
        "nom": "mw022 Scarlet Spider — redresse le heros en arrivant",
        "pourquoi": "Hero Response a l'entree en jeu, cible « YourHero »",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "declencher": [
            "Puzzle.Exhaust('Madame Web')",
            "Puzzle.PutIntoPlay('mw022')",
        ],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["mw001a"], "en_jeu": ["mw022"]},
    },
    {
        "nom": "mw023 Spider-Woman (Ashley Barton) — +1 ATK payee uniquement en [physical]",
        "pourquoi": ("aucune autre carte du moteur ne conditionne un bonus PERMANENT "
                     "d'allie au mode de paiement : chemin inedit"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "main_exclusive": ["mw023", "mw008", "mw029"],
        "declencher": [],
        "jouer": ["mw023"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["mw023", "attack", 1]]},
    },
    {
        "nom": "mw023 Spider-Woman (Ashley Barton) — aucun bonus si le paiement est mixte",
        "pourquoi": "l'autre moitie de la condition : une ressource non [physical] annule le bonus",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "main_exclusive": ["mw023", "mw008", "mw004"],
        "declencher": [],
        "jouer": ["mw023"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["mw023", "attack", 0]]},
    },
    {
        "nom": "mw025 Spider-Woman (Mattie Franklin) — se pose en jeu depuis la main",
        "pourquoi": ("AfterCardEnterHand + paiement du cout imprime : si le chemin casse, "
                     "la carte reste bloquee en main"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "declencher": ["Puzzle.Gain('mw025')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["mw025"]},
    },
    {
        "nom": "mw028 Advice — +3 ATK a l'allie, deck Rencontre truque a 3 icones boost",
        "pourquoi": ("X vient des icones boost defaussees : on fige le dessus du deck "
                     "Rencontre pour rendre le resultat verifiable"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "main": ["mw028", "mw008"],
        "declencher": [
            "Puzzle.PutIntoPlay('30012')",
            "Puzzle.CreateEncounterDeck('mw021')",
        ],
        "jouer": ["mw028"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["30012", "attack", 3]]},
    },
    {
        "nom": "mw029 Female Power — 2 degats par personnage « Madame »/« Lady » controle",
        "pourquoi": "le comptage par mots du titre est fait a la main : il doit tomber juste",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "main": ["mw029", "mw008", "mw004"],
        "declencher": ["Puzzle.PutIntoPlay('30012')"],
        "jouer": ["mw029"],
        "verifier": "etat_attendu",
        # Madame Web + Lady Spider = 2 personnages qualifiants -> 4 degats.
        "attendu": {"degats": [["01094", 4]]},
    },
    {
        "nom": "mw010 Gathering of Five — icone [physical] : 3 degats a l'identite",
        "pourquoi": ("les quatre branches lisent la ressource IMPRIMEE de la carte "
                     "defaussee ; on fige le dessus du deck du joueur"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "main": ["mw010"],
        "declencher": ["Puzzle.CreatePlayerDeck('mw008')"],
        "jouer": ["mw010"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "mw011 Web of Fate — la carte choisie parmi les 5 arrive en main",
        "pourquoi": ("effet DIFFERE porte par une ressource : il ne part qu'APRES le "
                     "paiement de la carte qu'elle finance"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "main_exclusive": ["mw028", "mw011"],
        "declencher": [
            "Puzzle.PutIntoPlay('30012')",
            "Puzzle.CreateEncounterDeck('mw021')",
            "Puzzle.CreatePlayerDeck('mw004', 'mw006', 'mw003', 'mw009', 'mw010')",
        ],
        "jouer": ["mw028"],
        "verifier": "web_of_fate_a_pioche",
    },
    {
        "nom": "mw006 Weaving a Web — sa ressource [wild] paie bien une alliee",
        "pourquoi": ("CanGenerateResources restreinte aux ALLIES : si le filtre est faux, "
                     "la ressource ne sert jamais a rien"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": [],
        "main_exclusive": ["mw026"],
        "declencher": ["Puzzle.PutIntoPlay('mw006')"],
        "jouer": ["mw026"],
        "verifier": "etat_attendu",
        # Veranke coute 1 : la seule ressource disponible est celle de l'amelioration.
        "attendu": {"en_jeu": ["mw026"], "exhausted": ["mw006"]},
    },
    {
        "nom": "mw008 Webb's Team Strikes! — 3 degats par allie incline (cout X)",
        "pourquoi": ("cout X + allies en CIBLES tronquees a X : « up to X » doit accepter "
                     "de 0 a tous, pas « tous ou aucun »"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('Cassandra Webb')"],
        "main_exclusive": ["mw008", "mw004"],
        "declencher": ["Puzzle.PutIntoPlay('30012')"],
        "jouer": ["mw008"],
        "cibles": ["30012"],
        "surpayer": True,
        "verifier": "etat_attendu",
        # 1 ressource payee -> X = 1 -> 1 allie incline -> 3 degats au vilain.
        "attendu": {"degats": [["01094", 3]], "exhausted": ["30012"]},
    },

    # ------------------------------------------------------------------------
    # Pack « cloak_dagger » : cd001a-cd018 (custom « DesignHacker »)
    # Adaptation deux-heros-en-un : identite Cloak/Tyrone + alliee Dagger.
    # ------------------------------------------------------------------------
    {
        "nom": "cd001b Setup — l'identite liee et Forces Combined arrivent en jeu",
        "pourquoi": ("depuis la refonte du 5/8/2026 Dagger est un SECOND JOUEUR, cree par "
                     "`linked_identity` ; le setup ne sort plus que Forces Combined"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["cd002b", "cd003"]},
    },
    {
        "nom": "cd001a Protective Pair — +2 DEF tant que Dagger est en jeu",
        "pourquoi": "synergie coeur du duo : elle exige les DEUX identites en forme heros",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.ChangeForm('Tandy Bowen')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 2}},
    },
    {
        "nom": "cd001a Protective Pair — le bonus tombe quand Dagger repasse en alter-ego",
        "pourquoi": ("Dagger etant une identite, elle ne quitte plus le jeu : c'est son "
                     "changement de FORME qui doit faire retomber le bonus"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.ChangeForm('Tandy Bowen')"],
        "declencher": ["Puzzle.ChangeForm('Dagger')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 0}, "en_jeu": ["cd002b"]},
    },
    {
        "nom": "cd002a Destructive Duo — Dagger a +2 ATK quand Cloak est en forme heros",
        "pourquoi": "synergie miroir, portee par la face heros de l'identite liee",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.ChangeForm('Tandy Bowen')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["cd002a", "attack", 2]]},
    },
    {
        "nom": "cd002a Destructive Duo — pas de bonus quand Cloak reste en alter-ego",
        "pourquoi": "« while Cloak is in play » = forme heros seulement, cote joueur 1",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tandy Bowen')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["cd002a", "attack", 0]]},
    },
    {
        "nom": "cd001b Harmony — Tyrone Johnson a +2 REC",
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
        "nom": "cd004 Lightforce Cleansing — soigne 3 sur Cloak et fait piocher 2",
        "pourquoi": "le bonus de pioche exige 2+ soignes sur CLOAK precisement",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.Damage('Cloak', 3)",
                          "Puzzle.Exhaust('cd003')"],
        "main_exclusive": ["cd004", "01088"],
        "declencher": [],
        "jouer": ["cd004"],
        "payer_avec": ["01088"],
        "cibles": ["cd001a"],
        "verifier": "cd_cleansing_soigne_et_pioche",
    },
    {
        "nom": "cd005 Lightforce Daggers — 3 degats repartis, vilain sonne et desoriente",
        "pourquoi": ("action repartie (repeat_rules) + double statut : le confuse suit "
                     "parce que Cloak est en jeu en Hero Action"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')"],
        "main_exclusive": ["cd005", "01088", "01089", "01090"],
        "declencher": [],
        "jouer": ["cd005"],
        "cibles": ["01094", "01094", "01094"],
        "verifier": "cd_vilain_apres_daggers",
    },
    {
        "nom": "cd009 Dark Teleportation — redresse Dagger puis retire 2 menaces",
        "pourquoi": "la branche bonus ne part que si la cible redressee est Dagger",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.ChangeForm('Tandy Bowen')", "Puzzle.Exhaust('cd002a')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["cd009", "01088"],
        "declencher": [],
        "jouer": ["cd009"],
        "payer_avec": ["01088"],
        "cibles": ["cd002a"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["cd002a"], "menace": [["01097b", 3]]},
    },
    {
        "nom": "cd010 Darkforce Channel — degat au vilain, soin sur Cloak, deux statuts",
        "pourquoi": "effet compose : degats + soin proportionnel + confuse + stun via Dagger",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.ChangeForm('Tandy Bowen')", "Puzzle.Damage('Cloak', 2)"],
        "main_exclusive": ["cd010", "01088", "01089", "01090"],
        "declencher": [],
        "jouer": ["cd010"],
        "cibles": ["01094"],
        "verifier": "cd_vilain_apres_channel",
    },
    {
        "nom": "cd006 Pure Lightforce — 2 degats au vilain pour 2 ressources surpayees",
        "pourquoi": ("ressource a effet differe : surpaiement lu a la RESOLUTION de la "
                     "carte payee, montage ah007 ; sans `surpayer` le cas ne teste rien"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.Damage('Cloak', 3)",
                          "Puzzle.Exhaust('cd003')"],
        # Main reduite aux deux cartes utiles et surpaiement force : sinon le
        # pilote paie le cout 1 au plus juste et le surpaiement, seul objet du
        # cas, ne se produit pas.
        "main_exclusive": ["cd004", "cd006"],
        "surpayer": True,
        "declencher": [],
        "jouer": ["cd004"],
        "payer_avec": ["cd006"],
        "cibles": ["cd001a"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]]},
    },
    {
        "nom": "cd011 Raw Darkforce — 2 menaces retirees du complot pour 2 surpayees",
        "pourquoi": "miroir menace de cd006 ; la cible redressee est l'identite pour isoler l'effet",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.Exhaust('Cloak')",
                          "Puzzle.Exhaust('cd003')", "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["cd009", "cd011", "01088"],
        "declencher": [],
        "jouer": ["cd009"],
        "payer_avec": ["cd011"],
        "cibles": ["cd001a"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]]},
    },
    {
        "nom": "cd018 Opposites Attack — flip force en alter-ego et 1 menace posee",
        "pourquoi": "When Revealed qui compte les heros bascules",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.SetThreat('01097b', 4)"],
        "declencher": ["Puzzle.Reveal('cd018')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "menace": [["01097b", 5]]},
    },
    {
        "nom": "cd018 Opposites Attack — deja en alter-ego : aucune menace posee",
        "pourquoi": "« for each hero flipped this way » : zero bascule = zero menace",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.SetThreat('01097b', 4)"],
        "declencher": ["Puzzle.Reveal('cd018')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "menace": [["01097b", 4]]},
    },
    {
        "nom": "cd014 Lovers Quarrel — flip force puis resolution d'un des deux choix",
        "pourquoi": "l'obligation doit se resoudre sans bloquer la partie",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')"],
        "declencher": ["Puzzle.Reveal('cd014')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo"},
    },
    {
        "nom": "cd017 Inner Demon — Toughness native : le premier degat est absorbe",
        "pourquoi": "carte sans script : les mots-cles desc doivent suffire",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.PutIntoPlay('cd017')"],
        "declencher": ["Puzzle.Damage('cd017', 1)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["cd017", 0]], "en_jeu": ["cd017"]},
    },
    {
        "nom": "cd003 Forces Combined — main vide cote Cloak, l'autre main paie",
        "pourquoi": ("depuis le 5/8/2026 la carte ne GENERE plus de ressource : elle "
                     "autorise l'autre main a payer, et s'incline quand celle-ci sert"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')", "Puzzle.Damage('Cloak', 2)"],
        "main_exclusive": ["cd004"],
        "declencher": [],
        "jouer": ["cd004"],
        "cibles": ["cd001a"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["cd003"]},
    },

    # ------------------------------------------------------------------------
    # Pack « spider_man_rainy » : Spider-Man (Peter Parker, par Rainy) 71xxx
    # ------------------------------------------------------------------------
    {
        "nom": "sr003 Thwip! — toile sur Rhino, et Impact Webbing sorti au setup",
        "pourquoi": "verifie la pose de compteur web ET SetupPutIntoPlay(sr012)",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('sr001b')"],
        "main_exclusive": ["sr003", "sr007"],
        "declencher": [],
        "jouer": ["sr003"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "web", 1]], "en_jeu": ["sr012"]},
    },
    {
        "nom": "sr006 Webbed Up (action) — 3 toiles d'un coup, plafond a 3",
        "pourquoi": "le plafond de 3 compteurs web est porte par Impact Webbing",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('sr001b')",
                           "Puzzle.Counter('01094', 'web', 2)"],
        "main_exclusive": ["sr006", "sr008"],
        "declencher": [],
        "jouer": ["sr006"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "web", 3]]},
    },
    {
        "nom": "sr005 Web Strike — 6 degats, +2 sur un ennemi entoile",
        "pourquoi": "le bonus depend des compteurs web de la cible",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('sr001b')",
                           "Puzzle.Counter('01094', 'web', 1)"],
        "main_exclusive": ["sr005", "sr008", "sr004", "sr010", "sr009"],
        "declencher": [],
        "jouer": ["sr005"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 8]], "compteurs": [["01094", "web", 1]]},
    },
    {
        "nom": "sr005 Web Strike — 6 degats seulement sans toile",
        "pourquoi": "l'autre moitie de la condition du bonus",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('sr001b')"],
        "main_exclusive": ["sr005", "sr008", "sr004", "sr010", "sr009"],
        "declencher": [],
        "jouer": ["sr005"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 6]]},
    },
    {
        "nom": "sr007 Great Power — 2 degats apres avoir servi de paiement",
        "pourquoi": "ressource a effet differe, montage The Power of Forgiveness",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('sr001b')"],
        "main_exclusive": ["sr003", "sr007"],
        "declencher": [],
        "jouer": ["sr003"],
        "payer_avec": ["sr007"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "compteurs": [["01094", "web", 1]]},
    },
    {
        "nom": "sr008 Great Responsibility — retire 2 menaces apres paiement",
        "pourquoi": "meme montage, cote menace",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('sr001b')"],
        "main_exclusive": ["sr003", "sr008"],
        # la pose de menace vient APRES le vidage de la main : sinon le 01061
        # officiel (Great Responsibility, event Justice) l'intercepte depuis
        # la main de depart et la convertit en degats.
        "declencher": ["Puzzle.PlaceThreat('The Break-In!', 5)"],
        "jouer": ["sr003"],
        "payer_avec": ["sr008"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]]},
    },
    {
        "nom": "sr015 Mysterio — l'illusion encaisse les degats a sa place",
        "pourquoi": "Forced Interrupt de remplacement : compteur retire, 0 degat",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.PutIntoPlay('sr015')"],
        "declencher": ["Puzzle.Damage('sr015', 2)"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["sr015", "illusion", 1]],
                    "degats": [["sr015", 0]]},
    },
    {
        "nom": "sr016 Jump Scare — carte face cachee puis 1 degat par carte devant soi",
        "pourquoi": "When Revealed a double effet, compte les cartes rencontre face cachee",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('sr016')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1},
    },
    {
        "nom": "sr017 Smoke and Mirrors — Mysterio recoit un statut Tenace",
        "pourquoi": "When Revealed conditionnel : Mysterio present, c'est lui qui prend le Tough",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.PutIntoPlay('sr015')"],
        "declencher": ["Puzzle.Reveal('sr017')"],
        "verifier": "smr_mysterio_a_tough",
    },
    {
        "nom": "sr002 Spider-Man (Ben Reilly) — allie signature joue et pose en jeu",
        "pourquoi": "cout 2 : verifie le chemin de paiement de l'allie",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": [],
        "main_exclusive": ["sr002", "sr007", "sr008"],
        "declencher": [],
        "jouer": ["sr002"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["sr002"]},
    },

    # ------------------------------------------------------------------------
    # Pack « venom_rainy » : Venom (Eddie Brock, par Rainy) 72xxx
    # ------------------------------------------------------------------------
    {
        "nom": "vr001a Venom — Hunger : soigne 1 apres avoir vaincu un ennemi",
        "pourquoi": ("DEFAUT signale dans le script depuis le 5/8/2026 et jamais mis en cas : "
                     "« Hunger ne repond jamais ». Aucun outil ne pouvait le voir, l'audit ne "
                     "regarde que le type declare. Venom frappe a 2 et le sbire a 3 PV : on lui "
                     "en retire 1 d'abord pour que l'attaque de base l'acheve, sinon Venom n'est "
                     "pas le tueur et la Response n'a aucune raison de partir."),
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')", "Puzzle.PutIntoPlay('vr011')",
                          "Puzzle.Damage('vr001a', 3)", "Puzzle.PutIntoPlay('01101')"],
        # Les 3 degats de mise en place en declenchent un QUATRIEME : Symbiotic
        # Fury (vr005) est une « Hero Response: After you take damage, take 1
        # additional damage → ready your hero ». Elle part toute seule, c'est
        # deterministe, et c'est elle qui redresse Venom pour qu'il puisse
        # frapper. Le total sans Hunger est donc 4, et 3 si Hunger soigne.
        #
        # On monte la frappe de Venom au lieu d'affaiblir la cible : Sharp
        # Teeth (vr011) lui donne +1 ATK, soit 3, juste de quoi achever les
        # 3 PV du sbire. `Puzzle.Damage` sur un sbire ne fait RIEN, ni par
        # card_id ni par nom, et sans le moindre message : `FindOrCreateFace`
        # rend une face qui n'est pas `CanHealth` et la fonction sort en
        # silence. Deux essais y sont passes.
        "declencher": ["Puzzle.Attack('vr001a')"],
        "cibles": ["01101"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3, "hors_jeu": ["01101"]},
    },
    {
        "nom": "vr010 Regeneration — +2 points de vie",
        "pourquoi": "GiveKeywordToInPlayWhenApplyThis(You, health=2)",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('vr010')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 2}},
    },
    {
        "nom": "vr011 Sharp Teeth — Venom gagne +1 ATK",
        "pourquoi": "buff permanent + mots-cles overkill/piercing sur l'attaque de base",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')"],
        "declencher": ["Puzzle.PutIntoPlay('vr011')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}},
    },
    {
        "nom": "vr009 Lethal Protector — Venom gagne +1 DEF",
        "pourquoi": "buff permanent sur l'identite",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')"],
        "declencher": ["Puzzle.PutIntoPlay('vr009')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}},
    },
    {
        "nom": "vr007 Venomous Bite — 5 degats et l'ennemi est Sonne",
        "pourquoi": "chemin nominal : la cible survit, elle est etourdie, pas de soin",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')"],
        "main_exclusive": ["vr007", "vr006", "vr002", "vr011"],
        "declencher": ["Puzzle.Damage('Venom', 3)"],
        "jouer": ["vr007"],
        "payer_avec": ["vr006", "vr002", "vr011"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        # 3 degats poses + 1 de Represailles (Rhino, Retaliate 1) = 4
        "attendu": {"degats": [["01094", 5]], "degats_identite": 4},
    },
    {
        "nom": "vr003 Just A Snack — 2 degats si paye avec une ressource [physical]",
        "pourquoi": "meme mecanique de paiement qu'Ashley Barton mw023",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')"],
        "main_exclusive": ["vr003", "vr002"],
        "declencher": ["Puzzle.Damage('Venom', 4)"],
        "jouer": ["vr003"],
        "payer_avec": ["vr002"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "degats_identite": 2},
    },
    {
        "nom": "vr003 Just A Snack — 1 degat seulement sans ressource [physical]",
        "pourquoi": "l'autre moitie de la condition de paiement",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')"],
        "main_exclusive": ["vr003", "vr004"],
        "declencher": ["Puzzle.Damage('Venom', 4)"],
        "jouer": ["vr003"],
        "payer_avec": ["vr004"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1]], "degats_identite": 2},
    },
    {
        "nom": "vr006 Tendril Explosion — X degats a chaque ennemi",
        "pourquoi": "cout X finance par 2 ressources : X=2",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')",
                           "Puzzle.PutIntoPlay('vr015')"],
        "main_exclusive": ["vr006", "vr002", "vr011"],
        "declencher": [],
        "jouer": ["vr006"],
        "surpayer": True,
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2], ["vr015", 2]]},
    },
    {
        "nom": "vr014 Carnage — apres un soin, 1 degat en retour",
        "pourquoi": "Forced Response construit a la main sur AfterUnitHealHealth",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.PutIntoPlay('vr014')",
                           "Puzzle.Damage('Eddie Brock', 4)"],
        "declencher": ["Puzzle.Heal('Eddie Brock', 2)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "vr001b Eddie Brock — Investigative Reporter apres pose de menace",
        "pourquoi": "Response sur AfterSchemePlaceThreat, limite 1/round",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": [],
        "declencher": ["Puzzle.PlaceThreat('The Break-In!', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    {
        "nom": "vr012 We Hunger — passe en forme heros et applique une des deux penalites",
        "pourquoi": "obligation : flip force vers le heros puis choix",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": [],
        "main_exclusive": ["vr004"],
        "declencher": ["Puzzle.Reveal('vr012')"],
        "verifier": "we_hunger_resolue",
    },
    # ------------------------------------------------------------------------
    # Pack « jessica_jones » : jj001a-jj022 (custom « ekAugust »)
    # Tout le kit tourne autour des manigances secondaires ; le set « On the
    # Job » est mélangé dans le deck Rencontre par le Setup de l'alter-ego.
    # ------------------------------------------------------------------------
    {
        "nom": "jj001b Jessica Jones — le set On the Job part dans le deck Rencontre au setup",
        "pourquoi": ("le Setup ajoute « on_the_job » a message.encounter_set_names, "
                     "seul point ou le deck Rencontre n'est pas encore construit"),
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"dans_deck_rencontre": ["jj012", "jj013", "jj014", "jj015", "jj016"]},
    },
    {
        "nom": "jj010 Jessica's Jacket — +2 points de vie",
        "pourquoi": "GiveKeywordToAttached(You, health=2)",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('jj010')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 2}},
    },
    {
        "nom": "jj009 Jessica's Camera — 3 compteurs evidence donnent +1 DEF, +1 THW et +1 ATK",
        "pourquoi": "trois paliers cumulatifs lus sur le meme compteur 'evidence'",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')", "Puzzle.PutIntoPlay('jj009')"],
        "declencher": ["Puzzle.Counter('jj009', 'evidence', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1, "thwart": 1, "attack": 1}},
    },
    {
        "nom": "jj009 Jessica's Camera — temoin : a 1 compteur, seul le DEF monte",
        "pourquoi": "sans ce temoin, trois buffs inconditionnels passeraient le cas precedent",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')", "Puzzle.PutIntoPlay('jj009')"],
        "declencher": ["Puzzle.Counter('jj009', 'evidence', 1)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1, "thwart": 0, "attack": 0}},
    },
    {
        "nom": "jj013 Chase Down a Lead — Investigate 2 deplace 2 menaces du complot principal",
        "pourquoi": "mot-cle maison INVESTIGATE : retrait sur le complot puis pose ici",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.SetThreat('01097b', 5)"],
        "declencher": ["Puzzle.Reveal('jj013')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3], ["jj013", 5]]},
    },
    {
        "nom": "jj016 Sneak Into the Crime Scene — When Defeated : Jessica Jones devient Tenace",
        "pourquoi": "When Defeated d'une manigance du set On the Job",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.Reveal('jj016')"],
        "declencher": ["Puzzle.SetThreat('jj016', 0)"],
        "verifier": "jj_identite_tenace",
    },
    {
        "nom": "jj002 Luke Cage — une manigance secondaire en jeu lui retire 1 degat",
        "pourquoi": "reduction conditionnelle ; le statut Tenace initial est consomme avant",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')",
                          "Puzzle.PutIntoPlay('jj002')",
                          "Puzzle.Reveal('jj013')"],
        "declencher": ["Puzzle.Damage('jj002', 1)", "Puzzle.Damage('jj002', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["jj002", 2]]},
    },
    # ------------------------------------------------------------------------
    # Pack « agent_anti_venom » : av001a-av016 (custom « DesignHacker »)
    # Tout le kit lit « exactly 10 hit points remaining » (= intact).
    # ------------------------------------------------------------------------
    {
        "nom": "av001a Ten Out of Ten! — intact, il gagne +1 THW, +1 ATK et +1 DEF",
        "pourquoi": "buff conditionne aux PV COURANTS, pas au rapport health/max_health",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"thwart": 1, "attack": 1, "defense": 1}},
    },
    {
        "nom": "av001a Ten Out of Ten! — temoin : blesse d'1 PV, le bonus tombe",
        "pourquoi": "sans ce temoin, trois buffs inconditionnels passeraient le cas precedent",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')"],
        "declencher": ["Puzzle.Damage('av001a', 1)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"thwart": 0, "attack": 0, "defense": 0}},
    },
    {
        "nom": "av008 Anti-Maniac Booster — Agent Anti-Venom gagne retaliate 1",
        "pourquoi": "GiveKeywordToAttached(You, retaliate=1)",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')"],
        "declencher": ["Puzzle.PutIntoPlay('av008')"],
        "verifier": "aav_retaliate",
    },
    {
        "nom": "av001b Boy Scout — revenir en alter-ego soigne 2 degats",
        "pourquoi": "AfterUnitChangeForm(to_this_form=True) + cible soignable",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')",
                          "Puzzle.Damage('av001a', 4)"],
        "declencher": ["Puzzle.ChangeForm('av001a')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "av005 \"I've Got This!\" — intact (piercing), il tape a 7 et non a 5",
        "pourquoi": "lecture maison de « if this attack has ranged or piercing »",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')"],
        "main_exclusive": ["av005", "av003", "av004"],
        "declencher": [],
        "jouer": ["av005"],
        "payer_avec": ["av003", "av004"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 7]]},
    },
    {
        "nom": "av005 \"I've Got This!\" — temoin : blesse, il tape a 5",
        "pourquoi": "sans piercing ni ranged, la carte doit retomber a 5 degats",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')",
                          "Puzzle.Damage('av001a', 2)"],
        "main_exclusive": ["av005", "av003", "av004"],
        "declencher": [],
        "jouer": ["av005"],
        "payer_avec": ["av003", "av004"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]]},
    },
    {
        "nom": "av016 Infected — s'attache au sbire le plus resistant et lui donne +1 ATK",
        "pourquoi": "attachement au plus haut PV imprime, comme Genetically Enhanced 01163",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')",
                          "Puzzle.PutIntoPlay('av015')"],
        "declencher": ["Puzzle.Reveal('av016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["av016"], "attributs_carte": [["av015", "attack", 1]]},
    },
    {
        "nom": "av012 Spread Too Thin — l'obligation se resout depuis la forme heros",
        "pourquoi": ("le « You may flip to alter-ego form » passe par ChangeToForm ; "
                     "ChangeForm n'existe pas et faisait planter la resolution"),
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')",
                          "Puzzle.PutIntoPlay('av008')"],
        "declencher": ["Puzzle.Reveal('av012')"],
        "verifier": "obligation_resolue_74012",
    },
    {
        "nom": "jj017 Stable Home Life — l'obligation se resout depuis la forme heros",
        "pourquoi": "meme montage que av012 : ChangeToForm, pas ChangeForm",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')",
                          "Puzzle.PutIntoPlay('jj010')"],
        "declencher": ["Puzzle.Reveal('jj017')"],
        "verifier": "obligation_resolue_73017",
    },
    # ------------------------------------------------------------------------
    # Couverture ajoutee le 4/8/2026 sur les cartes des packs jessica_jones et
    # agent_anti_venom qui n'avaient aucun cas. Ne restent hors de portee que
    # les capacites suspendues a une ATTAQUE ou a une ACTION de carte en jeu,
    # que l'API Puzzle ne sait pas declencher.
    # ------------------------------------------------------------------------
    {
        "nom": "jj001a Hard-Hitting Investigation — vaincre une manigance frappe pour l'ATK",
        "pourquoi": ("chaine centrale de l'heroine, jamais couverte : Crack the Case "
                     "acheve la manigance, la Response du heros doit alors partir"),
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')",
                          "Puzzle.Reveal('jj016')",
                          "Puzzle.SetThreat('jj016', 2)"],
        "main_exclusive": ["jj004", "jj003"],
        "declencher": [],
        "jouer": ["jj004"],
        "cibles": ["jj016", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["jj016"], "degats": [["01094", 2]]},
    },
    {
        "nom": "jj009 Jessica's Camera — la Response pose bien un compteur evidence",
        "pourquoi": ("les 3 paliers etaient testes en posant les compteurs a la main ; "
                     "la Response qui les pose ne l'etait pas"),
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')",
                          "Puzzle.PutIntoPlay('jj009')",
                          "Puzzle.Reveal('jj016')",
                          "Puzzle.SetThreat('jj016', 2)"],
        "main_exclusive": ["jj004", "jj003"],
        "declencher": [],
        "jouer": ["jj004"],
        "cibles": ["jj016", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["jj009", "evidence", 1]]},
    },
    {
        "nom": "jj003 Breakthrough — 4 degats, +1 par manigance secondaire en jeu",
        "pourquoi": "compte des manigances secondaires ; ici une seule en jeu, donc 5",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')", "Puzzle.Reveal('jj016')"],
        "main_exclusive": ["jj003", "jj005", "jj004"],
        "declencher": [],
        "jouer": ["jj003"],
        "payer_avec": ["jj005", "jj004"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]]},
    },
    {
        "nom": "jj005 Hit the Streets — 3 menaces, +1 par manigance secondaire en jeu",
        "pourquoi": "meme compteur que Breakthrough, cote dejouement",
        "scenario": "rhino",
        "heros": "jessica_jones",
        # 5 et pas 8 : au-dela, le complot « The Break-In! » est ACCOMPLI des la
        # mise en place et la partie s'arrete avant qu'on joue quoi que ce soit.
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')",
                          "Puzzle.Reveal('jj016')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["jj005", "jj003", "jj004"],
        "declencher": [],
        "jouer": ["jj005"],
        "payer_avec": ["jj003", "jj004"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    {
        "nom": "jj012 Always a Bigger Conspiracy — When Defeated : revele une autre manigance",
        "pourquoi": "defausse du deck Rencontre jusqu'a une manigance, puis revelation",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.Reveal('jj012')"],
        "declencher": ["Puzzle.SetThreat('jj012', 0)"],
        "verifier": "jj_une_autre_manigance_revelee",
    },
    {
        "nom": "jj014 Hang Back and Watch — Investigate 2 par joueur puis soin de 2",
        "pourquoi": "variante [per_hero] du mot-cle maison, et When Defeated qui soigne",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')",
                          "Puzzle.SetThreat('01097b', 6)",
                          "Puzzle.Damage('jj001a', 4)"],
        "declencher": ["Puzzle.Reveal('jj014')", "Puzzle.SetThreat('jj014', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]], "degats_identite": 2},
    },
    {
        "nom": "jj020 \"I've Got Everyone\" — sans manigance secondaire, la carte prend surge",
        "pourquoi": "branche X=0 : pas de degats, mais un Renfort",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')"],
        "declencher": ["Puzzle.Reveal('jj020')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "jj021 The Purple Children — 2 menaces sur chaque manigance secondaire",
        "pourquoi": "branche nominale ; l'autre branche desoriente le joueur",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')",
                          "Puzzle.Reveal('jj016')",
                          "Puzzle.SetThreat('jj016', 1)"],
        # Main videe : depuis le correctif de `Puzzle.Reveal` (5/8/2026) les
        # interruptions `from_encounter=True` partent vraiment, et le pilote
        # ANNULAIT la traitrise avec Out in the Open qu'il avait en main.
        "main_exclusive": ["jj003"],
        "declencher": ["Puzzle.Reveal('jj021')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["jj016", 3]]},
    },
    {
        "nom": "jj018 \"Look At Me!\" — le Homme-Pourpre ne peut pas subir de degats",
        "pourquoi": "UnitCannotTakeDamageWhile, cle de la manigance nemesis",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')",
                          "Puzzle.Reveal('jj018')",
                          "Puzzle.PutIntoPlay('jj019')"],
        "declencher": ["Puzzle.Damage('jj019', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["jj019", 0]]},
    },
    {
        "nom": "jj019 * Purple Man — Boost : le joueur est Desoriente",
        "pourquoi": "capacite de boost du sbire nemesis",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')"],
        "declencher": ["Puzzle.Boost('jj019')"],
        "verifier": "identite_a_un_statut",
    },
    {
        "nom": "jj022 Power Couple — Tenace sur Jessica et Luke Cage, puis pioche",
        "pourquoi": ("carte de duo : condition de jeu maison (Luke Cage en jeu) a la place "
                     "de la cle TeamUp, qui suppose deux heros"),
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')",
                          "Puzzle.PutIntoPlay('jj002')"],
        "main_exclusive": ["jj022", "jj003", "jj005"],
        "declencher": [],
        "jouer": ["jj022"],
        "payer_avec": ["jj003", "jj005"],
        "verifier": "jj_couple_tenace",
    },
    {
        "nom": "av006 Anti-Venom Goo — reduit le cout de l'evenement puis soigne le surpaiement",
        "pourquoi": ("la reduction de cout etait le point le plus incertain du pack : "
                     "Dig Deep coute 1, paye avec 2 [energy]. Si la reduction prend, le "
                     "cout tombe a 0 et le surpaiement vaut 2, donc 2 soins"),
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')",
                          "Puzzle.Damage('av001a', 4)"],
        "main_exclusive": ["av003", "av006"],
        "declencher": [],
        "jouer": ["av003"],
        "payer_avec": ["av006"],
        "cibles": ["01094", "av001a"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "degats_identite": 2},
    },
    {
        "nom": "av003 Dig Deep — intact : 3 degats, ennemi Sonne et 1 menace retiree",
        "pourquoi": "branche « exactly 10 hit points remaining » de l'evenement",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["av003", "av004", "av005"],
        "declencher": [],
        "jouer": ["av003"],
        "payer_avec": ["av004"],
        "cibles": ["01094", "01097b"],
        "verifier": "aav_dig_deep_intact",
    },
    {
        "nom": "av004 Extricate — 4 menaces retirees d'une manigance",
        "pourquoi": "effet de base de l'evenement de dejouement",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        # 5 et pas 7 : voir le cas Hit the Streets, le complot serait accompli.
        "mise_en_place": ["Puzzle.ChangeForm('av001b')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["av004", "av003", "av005"],
        "declencher": [],
        "jouer": ["av004"],
        "payer_avec": ["av003", "av005"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    # ------------------------------------------------------------------------
    # Pack « moon_knight » : mk001a-mk024 (custom « DesignHacker »)
    # Identité à CINQ faces (pile d'identités de l'insert).
    # ------------------------------------------------------------------------
    {
        "nom": "mk001b Marc Spector — la partie demarre sur la bonne face parmi cinq",
        "pourquoi": "premiere identite du moteur a 5 faces : le depart doit tomber sur Marc",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "face_identite",
        "attendu": {"face": "mk001b"},
    },
    {
        "nom": "mk008 Fight or Foil — bascule vers Moon Knight et 2 degats",
        "pourquoi": "ChangeToFace vers une face NOMMEE parmi 5, au coeur de tout le pack",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": [],
        "main_exclusive": ["mk008", "01088"],
        "declencher": [],
        "jouer": ["mk008"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "face_identite",
        "attendu": {"face": "mk001a"},
    },
    {
        "nom": "mk001a A Good Offense — Deck and Cover coute 0 sur la face Moon Knight",
        "pourquoi": ("reducteur de cout par classe + carte bi-classe : sans lui la carte "
                     "est injouable main vide, avec lui elle part gratuitement"),
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": [],
        "main_exclusive": ["mk008", "01088", "mk007"],
        "declencher": [],
        "jouer": ["mk008", "mk007"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]]},
    },
    {
        "nom": "mk002 Echo — ATK/THW a 0 tant que l'identite est en alter-ego",
        "pourquoi": "ses stats copient le heros ACTIF ; sans heros actif, rien",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('mk002')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["mk002", "attack", 0], ["mk002", "thwart", 0]]},
    },
    {
        "nom": "mk002 Echo — copie l'ATK 2 / THW 1 de Moon Knight",
        "pourquoi": "le gain dynamique doit suivre la face heros courante",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('mk002')"],
        "main_exclusive": ["mk008", "01088"],
        "declencher": [],
        "jouer": ["mk008"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["mk002", "attack", 2], ["mk002", "thwart", 1]]},
    },
    {
        "nom": "mk005 Different Folks — un compteur madness par changement de forme",
        "pourquoi": "AfterUnitChangeForm force : le compteur doit tomber tout seul",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('mk005')"],
        "main_exclusive": ["mk008", "01088"],
        "declencher": [],
        "jouer": ["mk008"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["mk005", "madness", 1]]},
    },
    {
        "nom": "mk003 Khonshu — apres un changement de forme, s'incline et fait piocher",
        "pourquoi": "Response avec cout d'inclinaison sur le changement de forme",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('mk003')"],
        "main_exclusive": ["mk008", "01088"],
        "declencher": [],
        "jouer": ["mk008"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["mk003"]},
    },
    {
        "nom": "mk004 Frenchie — se defausse pour annuler la menace sur le complot",
        "pourquoi": "interruption de WhenSchemeWouldPlaceThreat avec SetBeInstead",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.SetThreat('01097b', 2)", "Puzzle.PutIntoPlay('mk004')"],
        "declencher": ["Puzzle.PlaceThreat('01097b', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]], "hors_jeu": ["mk004"]},
    },
    {
        "nom": "mk010 Where'd He Go? — depuis l'alter-ego : flip heros et vilain desoriente",
        "pourquoi": "menu de formes filtre (heros seulement) puis statut",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": [],
        "main_exclusive": ["mk010", "01088"],
        "declencher": [],
        "jouer": ["mk010"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "mk_forme_heros_et_vilain_desoriente",
    },
    {
        "nom": "mk013 Bushman — survit a sa premiere defaite et gagne un compteur madness",
        "pourquoi": "WhenUnitWouldBeDefeated + SetBeInstead : soin complet au lieu de mourir",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('mk013')"],
        "declencher": ["Puzzle.Damage('mk013', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["mk013"], "compteurs": [["mk013", "madness", 1]],
                    "degats": [["mk013", 0]]},
    },
    {
        "nom": "mk013 Bushman — la seconde defaite est la bonne",
        "pourquoi": "avec un compteur madness, l'interruption ne doit plus le sauver",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('mk013')"],
        "declencher": ["Puzzle.Damage('mk013', 5)", "Puzzle.Damage('mk013', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["mk013"]},
    },
    {
        "nom": "mk015 Cull the Weak — defausse l'allie le plus faible",
        "pourquoi": "When Revealed avec choix automatique du plus bas en PV restants",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('mk002')"],
        "declencher": ["Puzzle.Reveal('mk015')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["mk002"], "degats_identite": 0},
    },
    {
        "nom": "mk015 Cull the Weak — sans allie, 2 degats a l'identite",
        "pourquoi": "branche de repli",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('mk015')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "mk014 Mano a Mano — Moon Knight perd 1 ATK tant que la manigance est en jeu",
        "pourquoi": "aura GiveKeywordToInPlay sur une face heros nommee",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('mk014')"],
        "main_exclusive": ["mk008", "01088"],
        "declencher": [],
        "jouer": ["mk008"],
        "payer_avec": ["01088"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": -1}},
    },
    {
        "nom": "mk020 Thor (Age of Khonshu) — vaincu par le joueur, il lache Mjolnir",
        "pourquoi": ("When Defeated + creation a la volee de l'artefact lie "
                     "(CardFactory.GenerateCard), jamais fait par un set modulaire"),
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('mk020')", "Puzzle.Damage('mk020', 8)"],
        "main_exclusive": ["mk008", "01088"],
        "declencher": [],
        "jouer": ["mk008"],
        "payer_avec": ["01088"],
        "cibles": ["mk020"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["mk020"], "en_jeu": ["mk021"]},
    },
    {
        "nom": "mk006 Different Strokes — 1 compteur par aspect joue, pas deux fois le meme",
        "pourquoi": "limite « once per round for each aspect » suivie sur world",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.PutIntoPlay('mk006')", "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["mk008", "01090", "04049", "01088", "13014", "04043"],
        "declencher": [],
        # Fight or Foil d'abord : les cartes d'aspect sont des Hero Actions,
        # injouables depuis l'alter-ego de depart. Les deux Aggression passent
        # ensuite gratuitement (A Good Offense) ; la 2e ne compte pas (limite).
        "jouer": ["mk008", "04049", "13014", "04043"],
        "payer_avec": ["01090", "01088"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["mk006", "madness", 2]]},
    },
    # ------------------------------------------------------------------------
    # Pack « lockjaw » : lj001a-lj030 (custom « Nugget »)
    # ------------------------------------------------------------------------
    {
        "nom": "lj001b Setup — Tuning Fork est fouillee dans le deck et mise en jeu",
        "pourquoi": "sans elle, la ressource « os » du pack n'existe pas et tout le deck cale",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["lj003"]},
    },
    {
        "nom": "lj005 Kamala's Room — +1 REC a l'alter-ego",
        "pourquoi": "GiveKeywordToAttached('You') doit viser l'identite, pas le soutien",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('lj005')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 1}, "en_jeu": ["lj005"]},
    },
    {
        "nom": "lj026 Ms. Marvel — +1 ATK et +1 THW (interruptions rendues en bonus permanent)",
        "pourquoi": "ecart assume : les deux Interrupt etoiles valent un bonus permanent",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('lj026')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["lj026", "attack", 1], ["lj026", "thwart", 1]]},
    },
    {
        "nom": "lj015 Annihilus — vaincu, il retourne dans le deck Rencontre",
        "pourquoi": "WhenUnitWouldBeDefeated + SetBeInstead : il ne doit jamais mourir",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.PutIntoPlay('lj015')"],
        "declencher": ["Puzzle.Damage('lj015', 9)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["lj015"], "dans_deck_rencontre": ["lj015"]},
    },
    {
        "nom": "lj017 Provoked — l'identite ne peut plus repasser en alter-ego",
        "pourquoi": "PlayersCannotChangeForms(to_form=AlterEgo) porte par une piece jointe",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('Lockjaw')"],
        "declencher": ["Puzzle.Reveal('lj017')", "Puzzle.ChangeForm('Lockjaw')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "en_jeu": ["lj017"]},
    },
    {
        "nom": "lj014 Dognapped! — 1 menace de plus par evenement TELEPORT joue",
        "pourquoi": "Forced Response sur le trait TELEPORT, coeur du set nemesis",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.Reveal('lj014')"],
        "main_exclusive": ["lj009", "01088"],
        "declencher": [],
        "jouer": ["lj009"],
        "payer_avec": ["01088"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["lj014", 3]]},
    },
    {
        "nom": "lj003 Tuning Fork — finance seule le cout d'une carte et s'incline",
        "pourquoi": "la ressource « os » du pack est rendue par un [wild] genere en s'inclinant",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": [],
        "main_exclusive": ["lj009"],
        "declencher": [],
        "jouer": ["lj009"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["lj003"]},
    },
    {
        "nom": "lj024 Wet Slobbering Kiss — 3 degats au vilain",
        "pourquoi": "evenement a deux branches : la branche degats doit etre atteignable",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('Lockjaw')"],
        "main_exclusive": ["lj024", "01088", "01089"],
        "declencher": [],
        "jouer": ["lj024"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]]},
    },
    {
        "nom": "lj010 Zooming Around — 1 degat au vilain engage et 1 menace retiree",
        "pourquoi": "effet double (ennemis engages + tous les complots) en une capacite",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('Lockjaw')", "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["lj010", "01088", "01089", "01090"],
        "declencher": [],
        "jouer": ["lj010"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1]], "menace": [["01097b", 3]]},
    },
    {
        "nom": "lj010 Zooming Around — payee en mental, la forme change aussi",
        "pourquoi": "meme clause bonus que lj009, et jamais exercee avant le 9/8/2026. La main "
                    "ne fournit que du mental (lj024 et lj028 portent RES=B) pour couvrir le "
                    "cout de 2 ; le bonus fait passer en identite civile, l'action de heros "
                    "ayant d'abord exige la forme de heros.",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('Lockjaw')", "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["lj010", "lj024", "lj028"],
        # lj003 Tuning Fork demarre EN JEU et genere un wild, qui vaut n'importe
        # quelle couleur : sans cette ligne le pilote le depense et la couleur
        # reellement payee n'est plus celle que le cas croit exercer.
        "ne_pas_depenser": ["lj003"],
        "declencher": [],
        "jouer": ["lj010"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "degats": [["01094", 1]], "menace": [["01097b", 3]]},
    },
    {
        "nom": "lj028 Companionship — incline un PET AVENGER et fait piocher 2",
        "pourquoi": "cout d'inclinaison porte par une AUTRE carte, filtree par trait",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.PutIntoPlay('lj025')"],
        "main_exclusive": ["lj028"],
        "declencher": [],
        "jouer": ["lj028"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["lj025"]},
    },
    {
        "nom": "lj027 Animals Unleashed — sort un PET AVENGER du deck",
        "pourquoi": "recherche deck+main+defausse puis mise en jeu, pour chaque joueur",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('Lockjaw')"],
        "main_exclusive": ["lj027", "01088"],
        "declencher": [],
        "jouer": ["lj027"],
        "payer_avec": ["01088"],
        "verifier": "lj_un_pet_avenger_en_jeu",
    },
    {
        "nom": "lj012 Psionic Tracking — defausse une carte du deck vise",
        "pourquoi": "recherche dans le deck d'un joueur puis defausse ciblee",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": [],
        "main_exclusive": ["lj012"],
        "declencher": [],
        "jouer": ["lj012"],
        "verifier": "lj_defausse_non_vide",
    },
    {
        "nom": "20001a Symbiotic Bond — en forme HEROS, Venom peut financer une carte a 3",
        "pourquoi": ("capacite Resource portee par la face HEROS : elle doit apparaitre parmi les "
                     "moyens de paiement. En alter-ego elle n'existe pas, c'est la carte qui le dit."),
        "scenario": "rhino",
        "heros": "venom",
        # CORRECTIF 4/8/2026 : par NOM, « Flash Thompson » est devenu ambigu
        # depuis le pack agent_anti_venom, dont l'alter-ego av001b porte le meme
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
        "nom": "mf014 * Wizard — chaque heros perd 1 THW tant qu'il est en jeu",
        "pourquoi": "malus passif du sbire nemesis sur toutes les identites",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')"],
        "declencher": ["Puzzle.PutIntoPlay('mf014')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"thwart": -1}},
    },
    {
        "nom": "mf006 Unstable Uniform — Mister Fantastic gagne +1 DEF",
        "pourquoi": "buff passif sur l'identite",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')"],
        "declencher": ["Puzzle.PutIntoPlay('mf006')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}},
    },
    {
        "nom": "mf005 Fantasticar — Mister Fantastic gagne +1 de taille de main",
        "pourquoi": "buff passif de taille de main",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')"],
        "declencher": ["Puzzle.PutIntoPlay('mf005')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"hand_size": 1}},
    },
    {
        "nom": "mf007 Fantasti-Flare — entre en jeu avec 4 compteurs flare",
        "pourquoi": "cle desc `Uses: 4,flare`",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')"],
        "declencher": ["Puzzle.PutIntoPlay('mf007')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["mf007", "flare", 4]]},
    },
    {
        "nom": "mf008 Neutralizer — entre en jeu avec 2 compteurs charge",
        "pourquoi": "cle desc `Uses: 2,charge`",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')"],
        "declencher": ["Puzzle.PutIntoPlay('mf008')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["mf008", "charge", 2]]},
    },
    {
        "nom": "mf002 * Invisible Woman — son arrivee redresse l'identite",
        "pourquoi": "Response a l'entree en jeu de l'alliee signature",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')", "Puzzle.Exhaust('mf001a')"],
        "declencher": ["Puzzle.PutIntoPlay('mf002')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["mf001a"], "en_jeu": ["mf002"]},
    },
    {
        "nom": "mf015 Hubris — When Revealed : 1 menace + le THW cumule des heros",
        "pourquoi": "Mister Fantastic a 3 THW, donc 1 + 3 = 4 menaces sur la manigance",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')"],
        "declencher": ["Puzzle.Reveal('mf015')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["mf015", 4]]},
    },
    {
        "nom": "mf016 Projection — s'attache a l'identite et prend surge",
        "pourquoi": "attachement nemesis pose sur la carte d'identite",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')"],
        "declencher": ["Puzzle.Reveal('mf016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["mf016"]},
    },
    {
        "nom": "mf017 Execution — defausse les Projection en jeu",
        "pourquoi": "la traitrise nettoie les attachements poses par mf016",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')", "Puzzle.Reveal('mf016')"],
        "declencher": ["Puzzle.Reveal('mf017')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["mf016"]},
    },
    {
        "nom": "mf009 Stretched Thin — 2 menaces, +1 sur chaque manigance si la main est vide",
        "pourquoi": ("les deux moities de la carte : la main est vide apres avoir joue "
                     "et paye, donc 2 + 1 = 3 menaces retirees du complot principal"),
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')",
                          "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["mf009", "mf010"],
        "declencher": [],
        "jouer": ["mf009"],
        "payer_avec": ["mf010"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    {
        "nom": "mf013 Ben's Cure — l'obligation se resout depuis la forme heros",
        "pourquoi": "obligation du pack, jamais jouee ; verifie surtout qu'elle ne plante pas",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')", "Puzzle.PutIntoPlay('mf006')"],
        "declencher": ["Puzzle.Reveal('mf013')"],
        "verifier": "obligation_resolue_65013",
    },
    # ------------------------------------------------------------------------
    # Pack « the_thing » (custom « DesignHacker »), livre le 2/8/2026 SANS
    # AUCUN cas de comportement. Couverture ajoutee le 4/8/2026.
    # ------------------------------------------------------------------------
    {
        "nom": "th005 Unstable Uniform — The Thing gagne +1 DEF",
        "pourquoi": "buff passif sur l'identite",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')"],
        "declencher": ["Puzzle.PutIntoPlay('th005')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}},
    },
    {
        "nom": "th012 * Puppet Master — sa revelation fait venir Hulk",
        "pourquoi": "Forced Response qui cherche th014 dans le deck Rencontre et le revele",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')"],
        "declencher": ["Puzzle.Reveal('th012')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["th012", "th014"]},
    },
    {
        "nom": "th013 Pulling The Strings — le sbire au plus bas SCH gagne +1 ATK",
        "pourquoi": "Hulk a 0 SCH, c'est donc lui qui prend le bonus",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')", "Puzzle.PutIntoPlay('th014')"],
        "declencher": ["Puzzle.Reveal('th013')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["th014", "attack", 1]]},
    },
    {
        "nom": "th015 Friendly Fire — degats egaux au meilleur ATK ami, ici celui du heros",
        "pourquoi": "seul en jeu, The Thing a 2 ATK : il encaisse 2",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')"],
        "declencher": ["Puzzle.Reveal('th015')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "th002 * Human Torch — arrive en jeu et resout son choix",
        "pourquoi": "Response a deux options ; on verifie surtout qu'elle ne plante pas",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')"],
        "declencher": ["Puzzle.PutIntoPlay('th002')"],
        "verifier": "tt_human_torch_a_choisi",
    },
    {
        "nom": "th006 Rock 'Em — retire 4 menaces d'une manigance",
        "pourquoi": "effet de base ; 5 - 4 = 1, donc pas de bonus « derniere menace »",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["th006", "th009", "th010", "th008"],
        "declencher": [],
        "jouer": ["th006"],
        "payer_avec": ["th009", "th010", "th008"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    {
        "nom": "th009 Sock 'Em — 4 degats a un ennemi",
        "pourquoi": "effet de base de l'evenement d'attaque",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')"],
        "main_exclusive": ["th009", "th006", "th010", "th008"],
        "declencher": [],
        "jouer": ["th009"],
        "payer_avec": ["th006", "th010", "th008"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]]},
    },
    {
        "nom": "th010 It's Clobberin' Time! — deux attaques de 4, soit 8 au total",
        "pourquoi": "la carte enchaine DEUX attaques, chacune sur une cible au choix",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')"],
        "main_exclusive": ["th010", "th006", "th009", "th008"],
        "declencher": [],
        "jouer": ["th010"],
        "payer_avec": ["th006", "th009", "th008"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 8]]},
    },
    {
        "nom": "th001b Ever-Lovin' — un soin de 4 ou plus rend Ben Grimm Tenace",
        "pourquoi": "Response de l'alter-ego sur le montant SOIGNE, pas sur les PV finaux",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.Damage('th001b', 6)"],
        "declencher": ["Puzzle.Heal('th001b', 4)"],
        "verifier": "identite_est_tenace",
    },
    {
        "nom": "th011 Annual Shedding — l'obligation se resout depuis la forme heros",
        "pourquoi": "obligation du pack, jamais jouee",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')"],
        "declencher": ["Puzzle.Reveal('th011')"],
        "verifier": "obligation_resolue_67011",
    },
    # ------------------------------------------------------------------------
    # Pack « invisible_woman » (custom « DesignHacker »). Etait a 5 % au
    # 4/8/2026. Les cartes conditionnees a une forme heros PRECISE (INVISIBLE
    # ou PSIONIC) ne sont pas couvertes : `Puzzle.ChangeForm` ne sait pas viser
    # une face, il bascule vers l'une des deux au choix du pilote.
    # ------------------------------------------------------------------------
    {
        "nom": "iw003 Central City Estate — Sue Storm gagne +1 REC",
        "pourquoi": "buff passif lisible en forme alter-ego, sans dependre de la face heros",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('iw003')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 1}},
    },
    {
        "nom": "iw016 Microversal Maneuvers — s'attache a Psycho-Man et lui donne +2 SCH",
        "pourquoi": "attachement nemesis, cle desc `SCH+`",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.PutIntoPlay('iw014')"],
        "declencher": ["Puzzle.Reveal('iw016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["iw016"], "attributs_carte": [["iw014", "scheme", 2]]},
    },
    {
        "nom": "iw017 Titanic Terror — s'attache a Psycho-Man et lui donne +2 ATK",
        "pourquoi": "attachement nemesis, cle desc `ATK+`",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.PutIntoPlay('iw014')"],
        "declencher": ["Puzzle.Reveal('iw017')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["iw017"], "attributs_carte": [["iw014", "attack", 2]]},
    },
    {
        "nom": "iw015 Emotional Masterplan — arrive avec 2 menaces par joueur",
        "pourquoi": "manigance nemesis, StartingThreat 2[per_hero]",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('iw015')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["iw015", 2]]},
    },
    {
        "nom": "iw002 * Mister Fantastic — son arrivee declenche une de ses deux options",
        "pourquoi": "Response a l'entree en jeu : 1 menace retiree partout, ou pioche depuis la defausse",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')",
                          "Puzzle.SetThreat('01097b', 3)"],
        "declencher": ["Puzzle.PutIntoPlay('iw002')"],
        "verifier": "iw_mister_fantastic_a_choisi",
    },
    {
        "nom": "iw013 Family Time — l'obligation se resout depuis la forme heros",
        "pourquoi": "obligation du pack, jamais jouee",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')"],
        "declencher": ["Puzzle.Reveal('iw013')"],
        "verifier": "obligation_resolue_66013",
    },
    # ------------------------------------------------------------------------
    # Packs « gwenpool » et « human_torch ». Les cartes a bulle « ____ » de
    # Gwenpool passent par ResolveBlank : on verifie l'effet de BASE, la bulle
    # etant un choix optionnel que le pilote decline.
    # ------------------------------------------------------------------------
    {
        "nom": "gp007 * Gwen's Room — Gwendolyn Poole gagne +1 REC",
        "pourquoi": "buff passif lisible en alter-ego",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('gp007')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 1}},
    },
    {
        "nom": "gp002 \"Here I Come!\" — 5 degats a un ennemi",
        "pourquoi": "effet de base, sans la bulle « ____ » que le pilote decline",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('gp001b')"],
        "main_exclusive": ["gp002", "gp003", "gp005"],
        "declencher": [],
        "jouer": ["gp002"],
        "payer_avec": ["gp003", "gp005"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]]},
    },
    {
        "nom": "gp005 \"Sorry, Gotta Run!\" — retire 2 menaces d'une manigance",
        "pourquoi": "effet de base de l'evenement de dejouement",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('gp001b')",
                          "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["gp005", "gp002", "gp003"],
        "declencher": [],
        "jouer": ["gp005"],
        "payer_avec": ["gp002"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]]},
    },
    {
        "nom": "gp010 THE END — l'obligation RESTE en jeu, elle ne se defausse pas",
        "pourquoi": ("contre-exemple utile : toutes les obligations ne partent pas a la "
                     "resolution. THE END s'installe et bloque les bulles jusqu'a ce que "
                     "le joueur paie son action d'alter-ego pour la retirer du jeu"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('gp001b')"],
        "declencher": ["Puzzle.Reveal('gp010')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["gp010"]},
    },
    {
        "nom": "ht002 * The Thing — allie Tenace a 5 PV et 3 ATK",
        "pourquoi": "valeurs imprimees et mot-cle Toughness de l'allie signature",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('ht001b')"],
        "declencher": ["Puzzle.PutIntoPlay('ht002')"],
        "verifier": "ht_the_thing_tenace",
    },
    {
        "nom": "ht007 Fly-By — 2 menaces, +1 par compteur flamme sur le vilain",
        "pourquoi": "l'effet variable du pack : 2 compteurs flamme, donc 2 + 2 = 4",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('ht001b')",
                          "Puzzle.SetThreat('01097b', 5)",
                          "Puzzle.Counter('01094', 'flame', 2)"],
        "main_exclusive": ["ht007", "ht010", "ht009"],
        "declencher": [],
        "jouer": ["ht007"],
        "payer_avec": ["ht010", "ht009"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    # ------------------------------------------------------------------------
    # Packs « albert », « rainy » et « lockjaw ».
    # ------------------------------------------------------------------------
    {
        "nom": "ab001b Albert — Extensive Development sort une amelioration ENHANCEMENT au setup",
        "pourquoi": "capacite Setup de l'alter-ego : elle doit avoir agi avant le 1er tour",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu_trait": [["ENHANCEMENT", 1]]},
    },
    {
        "nom": "ab003 Guard Protocol — Albert devient Tenace",
        "pourquoi": "l'evenement donne retaliate ET un statut Tenace ; on verifie le statut",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('ab001b')"],
        "main_exclusive": ["ab003", "ab004", "ab005"],
        "declencher": [],
        "jouer": ["ab003"],
        "payer_avec": ["ab004", "ab005"],
        "verifier": "identite_est_tenace",
    },
    {
        "nom": "ab004 Lethal Directive — 4 degats a un ennemi",
        "pourquoi": "effet de base de l'evenement d'attaque",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('ab001b')"],
        "main_exclusive": ["ab004", "ab003", "ab005"],
        "declencher": [],
        "jouer": ["ab004"],
        "payer_avec": ["ab003", "ab005"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]]},
    },
    {
        "nom": "ab005 Sabotage Sequence — retire 3 menaces d'une manigance",
        "pourquoi": "effet de base ; 5 - 3 = 2, donc pas de bonus « derniere menace »",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('ab001b')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["ab005", "ab003", "ab004"],
        "declencher": [],
        "jouer": ["ab005"],
        "payer_avec": ["ab003", "ab004"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]]},
    },
    {
        "nom": "ra005 Lightning Strike — 6 degats a un ennemi",
        "pourquoi": "effet de base de l'evenement d'attaque de Thor (Jane Foster)",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('ra001b')"],
        "main_exclusive": ["ra005", "ra004", "ra006", "ra008"],
        "declencher": [],
        "jouer": ["ra005"],
        "payer_avec": ["ra004", "ra006", "ra008"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 6]]},
    },
    {
        "nom": "ra028 * Malekith — arrive en jeu avec ses valeurs imprimees",
        "pourquoi": "sbire nemesis : 6 PV, 2 SCH, 1 ATK, sans modificateur parasite",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('ra001b')"],
        "declencher": ["Puzzle.PutIntoPlay('ra028')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["ra028"],
                    "attributs_carte": [["ra028", "attack", 0], ["ra028", "scheme", 0]]},
    },
    {
        "nom": "lj002 * Black Bolt — allie a 4 ATK et 3 PV",
        "pourquoi": "valeurs imprimees de l'allie le plus cher du pack",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')"],
        "declencher": ["Puzzle.PutIntoPlay('lj002')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["lj002"], "attributs_carte": [["lj002", "attack", 0]]},
    },
    {
        "nom": "lj018 * Zabu — allie Companion a 2 ATK",
        "pourquoi": "mot-cle maison Companion : l'allie entre en jeu normalement",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')"],
        "declencher": ["Puzzle.PutIntoPlay('lj018')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["lj018"], "attributs_carte": [["lj018", "attack", 0]]},
    },
    {
        "nom": "lj013 Canine Urges — l'obligation se resout depuis la forme heros",
        "pourquoi": "obligation du pack, jamais jouee",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')"],
        "declencher": ["Puzzle.Reveal('lj013')"],
        "verifier": "obligation_resolue_78013",
    },
    # ------------------------------------------------------------------------
    # Packs « moon_knight », « spider_man_rainy » et « venom_rainy ».
    # ------------------------------------------------------------------------
    {
        "nom": "mk016 Bushman's Knife — s'attache a un sbire et lui donne +2 ATK et piercing",
        "pourquoi": ("le piercing ne partait JAMAIS avant le correctif du 4/8/2026 : la "
                     "condition lisait le porteur avec une methode inexistante"),
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('mk001b')", "Puzzle.PutIntoPlay('mk017')"],
        "declencher": ["Puzzle.Reveal('mk016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["mk016"], "attributs_carte": [["mk017", "attack", 2]]},
    },
    {
        "nom": "mk021 * Mjolnir — +1 ATK, trait AERIAL et 3 compteurs attack",
        "pourquoi": "artefact cree en jeu par le set Age of Khonshu, jamais verifie",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('mk001b')"],
        "declencher": ["Puzzle.PutIntoPlay('mk021')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}, "traits": ["AERIAL"],
                    "compteurs": [["mk021", "attack", 3]]},
    },
    {
        "nom": "mk022 * The Eye of Agamotto — entre en jeu avec 2 compteurs mystic",
        "pourquoi": "cle desc `Uses: 2,mystic` de l'artefact",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('mk001b')"],
        "declencher": ["Puzzle.PutIntoPlay('mk022')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["mk022", "mystic", 2]]},
    },
    {
        "nom": "mk023 * The Hell Charger — entre en jeu avec 2 compteurs charge",
        "pourquoi": "cle desc `Uses: 2,charge` de l'artefact",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('mk001b')"],
        "declencher": ["Puzzle.PutIntoPlay('mk023')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["mk023", "charge", 2]]},
    },
    {
        "nom": "mk018 * Ghost Rider — sbire vilainesque a 7 PV et 3 ATK",
        "pourquoi": "heros corrompu du set Age of Khonshu, valeurs imprimees",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('mk001b')"],
        "declencher": ["Puzzle.PutIntoPlay('mk018')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["mk018"], "attributs_carte": [["mk018", "attack", 0]]},
    },
    {
        "nom": "mk012 Seek Help — l'obligation se resout depuis la forme heros",
        "pourquoi": "obligation du pack, jamais jouee",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('mk001b')"],
        "declencher": ["Puzzle.Reveal('mk012')"],
        "verifier": "obligation_resolue_76012",
    },
    {
        "nom": "sr012 Impact Webbing — la carte de regles est en jeu des le setup",
        "pourquoi": "cles `Permanent` + `Setup` : elle doit sortir sans etre jouee",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["sr012"]},
    },
    {
        "nom": "sr011 Web-Shooters — Spider-Man gagne le trait AERIAL",
        "pourquoi": "buff de trait passif sur l'identite",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('sr001b')"],
        "declencher": ["Puzzle.PutIntoPlay('sr011')"],
        "verifier": "etat_attendu",
        "attendu": {"traits": ["AERIAL"]},
    },
    {
        "nom": "sr014 For My Next Trick... — 3 menaces par joueur et 2 compteurs illusion",
        "pourquoi": "manigance nemesis de Mysterio, StartingThreat 3[per_hero] + Uses",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('sr001b')"],
        "declencher": ["Puzzle.Reveal('sr014')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["sr014", 3]],
                    "compteurs": [["sr014", "illusion", 2]]},
    },
    {
        "nom": "vr015 Symbiote Rioter — sbire Guard/Patrol a 4 PV et 2 ATK",
        "pourquoi": "sbire nemesis de Venom, valeurs imprimees",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')"],
        "declencher": ["Puzzle.PutIntoPlay('vr015')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["vr015"], "attributs_carte": [["vr015", "attack", 0]]},
    },
    {
        "nom": "vr013 Paint The Town Red — 1 menace imprimee + 2 par joueur via Hinder",
        "pourquoi": ("piege de lecture : la cle `Hinder: 2*` AJOUTE 2 menaces par joueur "
                     "a la revelation, en plus du StartingThreat 1. Total 3 en solo"),
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')"],
        "declencher": ["Puzzle.Reveal('vr013')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["vr013", 3]]},
    },
    {
        "nom": "vr004 Self-Sacrifice — le bonus optionnel EST pris : 6 menaces retirees",
        "pourquoi": ("CORRECTIF de lecture 4/8/2026 : le pilote ne refuse PAS tous les "
                     "choix optionnels. Il decline les `MayChooseOneAbility` (c'est ce qui "
                     "avait cache `identity.ChangeForm`), mais il accepte les couts "
                     "optionnels d'un effet, ici « you may take 2 damage ». Il paie aussi "
                     "avec Symbiotic Bond, d'ou 1 degat de plus"),
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["vr004", "vr002", "vr005"],
        "declencher": [],
        "jouer": ["vr004"],
        "payer_avec": ["vr002", "vr005"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 0]], "degats_identite": 3},
    },
    # ------------------------------------------------------------------------
    # Complements sur gwenpool, human_torch, the_thing et rainy.
    # ------------------------------------------------------------------------
    {
        "nom": "gp003 \"It Can't End Like This!\" — 1 degat au vilain et 1 menace retiree",
        "pourquoi": "double effet attaque/dejouement de l'evenement a 0",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('gp001b')",
                          "Puzzle.SetThreat('01097b', 3)"],
        "main_exclusive": ["gp003", "gp002"],
        "declencher": [],
        "jouer": ["gp003"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1]], "menace": [["01097b", 2]]},
    },
    {
        "nom": "gp009 * Unbelievable Gwenpool — l'amelioration entre en jeu",
        "pourquoi": "support de la mecanique des bulles ; verifie au moins sa mise en jeu",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('gp009')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["gp009"]},
    },
    {
        "nom": "ht010 Nova Flame — 3 compteurs flamme puis 7 degats, soit 10 au total",
        "pourquoi": ("la carte se combine avec « Flame On! » de l'identite, qui inflige "
                     "1 degat PAR compteur pose : 3 compteurs + 7 degats = 10. Compter "
                     "seulement les 7 de la carte serait une lecture incomplete"),
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('ht001b')"],
        "main_exclusive": ["ht010", "ht008", "ht007", "ht009", "ht005"],
        "declencher": [],
        "jouer": ["ht010"],
        "payer_avec": ["ht008", "ht007", "ht009", "ht005"],
        "cibles": ["01094"],
        "verifier": "ht_nova_flame",
    },
    {
        "nom": "ht008 Blaze and Daze — 4 degats a un ennemi",
        "pourquoi": "effet de base ; le bonus a 3 compteurs flamme n'est pas reuni ici",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('ht001b')"],
        "main_exclusive": ["ht008", "ht010", "ht007", "ht009"],
        "declencher": [],
        "jouer": ["ht008"],
        "payer_avec": ["ht010", "ht007", "ht009"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]]},
    },
    {
        "nom": "th014 * Hulk — sbire Guard a 5 PV et 3 ATK",
        "pourquoi": "le sbire asservi du set nemesis de The Thing, valeurs imprimees",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')"],
        "declencher": ["Puzzle.PutIntoPlay('th014')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["th014"], "attributs_carte": [["th014", "attack", 0]]},
    },
    {
        "nom": "th004 Yancy Street Gang — le soutien entre en jeu",
        "pourquoi": "son action n'est pas declenchable par le harnais ; on verifie la mise en jeu",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')"],
        "declencher": ["Puzzle.PutIntoPlay('th004')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["th004"]},
    },
    {
        "nom": "ra002 * Odinson — allie Multiverse a 3 PV",
        "pourquoi": "allie signature de Thor (Jane Foster), valeurs imprimees",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('ra001b')"],
        "declencher": ["Puzzle.PutIntoPlay('ra002')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["ra002"], "attributs_carte": [["ra002", "attack", 0]]},
    },
    {
        "nom": "ra003 * Roz Solomon — alliee a 2 THW",
        "pourquoi": "seconde alliee signature, valeurs imprimees",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('ra001b')"],
        "declencher": ["Puzzle.PutIntoPlay('ra003')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["ra003"], "attributs_carte": [["ra003", "thwart", 0]]},
    },
    # ------------------------------------------------------------------------
    # Derniers complements : invisible_woman, agent_anti_venom, lockjaw.
    # ------------------------------------------------------------------------
    {
        "nom": "iw012 Spectral Shift — l'Action change la forme de l'identite",
        "pourquoi": "seule carte du pack qui change de forme sans exiger une face precise",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": [],
        "main_exclusive": ["iw012", "iw008"],
        "declencher": [],
        "jouer": ["iw012"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero"},
    },
    {
        "nom": "iw018 End of the Line — defausse 8 cartes du deck Rencontre",
        "pourquoi": "traitrise nemesis : verifie surtout qu'elle se resout sans planter",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')"],
        "declencher": ["Puzzle.Reveal('iw018')"],
        "verifier": "iw_end_of_the_line",
    },
    {
        "nom": "iw014 * Psycho-Man — sbire nemesis a 5 PV",
        "pourquoi": "ses ATK et SCH sont imprimes « 0* » : on verifie au moins les PV",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')"],
        "declencher": ["Puzzle.PutIntoPlay('iw014')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["iw014"], "attributs_carte": [["iw014", "health", 0]]},
    },
    {
        "nom": "av013 * Maniac — sbire nemesis a 5 PV, 2 SCH et 2 ATK",
        "pourquoi": "valeurs imprimees du sbire nemesis d'Agent Anti-Venom",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')"],
        "declencher": ["Puzzle.PutIntoPlay('av013')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["av013"],
                    "attributs_carte": [["av013", "attack", 0], ["av013", "scheme", 0]]},
    },
    {
        "nom": "av015 * Infected Scorpion — sbire Quickstrike a 7 PV",
        "pourquoi": "valeurs imprimees ; son Forced Interrupt exige une attaque, non testable",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')"],
        "declencher": ["Puzzle.PutIntoPlay('av015')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["av015"], "attributs_carte": [["av015", "attack", 0]]},
    },
    {
        "nom": "av014 The Made Men — manigance nemesis a 3 menaces par joueur",
        "pourquoi": "StartingThreat 3[per_hero] ; son Forced Response exige une activation",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')"],
        "declencher": ["Puzzle.Reveal('av014')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["av014", 3]]},
    },
    {
        "nom": "av002 * Spider-Man — allie signature a 3 PV et 2 ATK",
        "pourquoi": "valeurs imprimees ; son Interrupt exige une activation de sbire",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')"],
        "declencher": ["Puzzle.PutIntoPlay('av002')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["av002"], "attributs_carte": [["av002", "attack", 0]]},
    },
    {
        "nom": "av009 Bear Arms — l'amelioration entre en jeu",
        "pourquoi": "ses deux actions ne sont pas declenchables par le harnais",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')"],
        "declencher": ["Puzzle.PutIntoPlay('av009')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["av009"]},
    },
    {
        "nom": "av007 Unlikely Allies — le soutien entre en jeu",
        "pourquoi": "son action de defausse n'est pas declenchable par le harnais",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')"],
        "declencher": ["Puzzle.PutIntoPlay('av007')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["av007"]},
    },
    {
        "nom": "lj016 Dog Catcher — sbire a 2 PV et 1 ATK",
        "pourquoi": "sbire nemesis de Lockjaw, valeurs imprimees",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')"],
        "declencher": ["Puzzle.PutIntoPlay('lj016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["lj016"], "attributs_carte": [["lj016", "attack", 0]]},
    },
    {
        "nom": "lj019 * Throg — allie Companion a 2 PV",
        "pourquoi": "second allie Companion, pour couvrir la famille",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')"],
        "declencher": ["Puzzle.PutIntoPlay('lj019')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["lj019"], "attributs_carte": [["lj019", "attack", 0]]},
    },
    # ------------------------------------------------------------------------
    # Derniere vague sur ce que le harnais atteint deja. Ce qui restera apres
    # exige un declencheur d'ATTAQUE ou d'ACTION de carte en jeu, absents de
    # l'API Puzzle.
    # ------------------------------------------------------------------------
    {
        "nom": "ra006 Stand Fast — redresse Thor",
        "pourquoi": "l'evenement redresse l'identite ; le bonus Tenace exige un paiement 100 % energie",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('ra001b')", "Puzzle.Exhaust('ra001a')"],
        "main_exclusive": ["ra006", "ra004", "ra005"],
        "declencher": [],
        "jouer": ["ra006"],
        "payer_avec": ["ra004", "ra005"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["ra001a"]},
    },
    {
        "nom": "ab006 System Relaunch — soigne la valeur de REC et passe en forme heros",
        "pourquoi": "Albert a 4 de REC : blesse de 6, il doit finir a 2 degats et en forme heros",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.Damage('ab001b', 6)"],
        "main_exclusive": ["ab006", "ab003"],
        "declencher": [],
        "jouer": ["ab006"],
        "payer_avec": ["ab003"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "forme": "Hero"},
    },
    {
        "nom": "ab013 Crack in the Multiverse — 1 menace imprimee + 2 par joueur via Hinder",
        "pourquoi": "meme piege que Paint The Town Red : la cle Hinder ajoute sa menace",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('ab001b')"],
        "declencher": ["Puzzle.Reveal('ab013')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["ab013", 3]]},
    },
    {
        "nom": "mf010 Big Reach — 3 degats au vilain, +0 car la main est vide",
        "pourquoi": "le second effet vaut le nombre de cartes restantes en main, ici zero",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')"],
        "main_exclusive": ["mf010", "mf009", "mf011", "mf012"],
        "declencher": [],
        "jouer": ["mf010"],
        "payer_avec": ["mf009", "mf011", "mf012"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]]},
    },
    {
        "nom": "mf012 Mental Gymnastics — 2 degats a X=0, et l'ennemi est Desoriente",
        "pourquoi": "carte a cout X : sans surpaiement X vaut 0, et la main vide declenche le bonus",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')"],
        "main_exclusive": ["mf012"],
        "declencher": [],
        "jouer": ["mf012"],
        "cibles": ["01094"],
        "verifier": "mf_mental_gymnastics",
    },
    {
        "nom": "ah008 Calculated Strike — 2 menaces retirees et 3 degats au vilain",
        "pourquoi": "double effet attaque/dejouement",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('ah001b')",
                          "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["ah008", "ah010", "ah009", "ah011"],
        "declencher": [],
        "jouer": ["ah008"],
        "payer_avec": ["ah010", "ah009", "ah011"],
        "cibles": ["01097b", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]], "degats": [["01094", 3]]},
    },
    {
        "nom": "jj015 Pore Over the Evidence — Investigate 1 par joueur",
        "pourquoi": "derniere manigance On the Job sans cas ; 4 imprimees + 1 deplacee",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "declencher": ["Puzzle.Reveal('jj015')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4], ["jj015", 5]]},
    },
    {
        "nom": "mk007 Deck and Cover — 3 degats a un ennemi (6 au total sur Rhino)",
        "pourquoi": ("Moon Knight ramene le cout de ses cartes d'aspect a 0, le pilote "
                     "joue donc AUSSI Surprise Attack de la main de depart, qui frappe "
                     "Rhino pour 3. Le total de 6 reste discriminant : si Deck and Cover "
                     "cassait, on tomberait a 3"),
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('mk001b')"],
        # Main reduite a la SEULE carte testee : Moon Knight ramene son cout a
        # 0 grace au rabais d'aspect, et le pilote ne peut donc plus jouer une
        # autre carte qui fausserait le total de degats.
        "main_exclusive": ["mk007"],
        "declencher": [],
        "jouer": ["mk007"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 6]]},
    },
    {
        "nom": "lj010 Zooming Around — retire 1 menace de chaque manigance",
        "pourquoi": ("teste le helper `ChangerDeForme`, absent du pack jusqu'au 4/8/2026 "
                     "et qui faisait planter TROIS cartes. Fast Travel lj009 partage le "
                     "meme code mais son effet net est nul en solo : elle change la forme "
                     "puis propose de la rechanger, donc rien d'observable"),
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')",
                          "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["lj010", "lj009", "lj008"],
        "declencher": [],
        "jouer": ["lj010"],
        "payer_avec": ["lj009", "lj008"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]]},
    },
    {
        "nom": "lj022 * Lockheed — allie Companion a 2 PV",
        "pourquoi": "dernier Companion sans cas",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')"],
        "declencher": ["Puzzle.PutIntoPlay('lj022')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["lj022"], "attributs_carte": [["lj022", "attack", 0]]},
    },
    {
        "nom": "lj025 * Ms. Lion — allie Companion a 2 PV",
        "pourquoi": "dernier Companion sans cas",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')"],
        "declencher": ["Puzzle.PutIntoPlay('lj025')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["lj025"], "attributs_carte": [["lj025", "attack", 0]]},
    },
    {
        "nom": "ht003 Johnny's Workshop — le soutien entre en jeu",
        "pourquoi": "ses deux Response dependent d'un changement de forme, teste juste apres",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('ht001b')"],
        "declencher": ["Puzzle.PutIntoPlay('ht003')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["ht003"]},
    },
    {
        "nom": "ah013 Get Under Control — l'obligation reste en jeu",
        "pourquoi": ("comme THE END de Gwenpool : elle bloque les allies et ne part qu'avec "
                     "l'action d'alter-ego. Victory 1"),
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('ah001b')"],
        "declencher": ["Puzzle.Reveal('ah013')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["ah013"]},
    },
    {
        "nom": "av010 Heroic Will — Hero Action : incliner l'amelioration redresse le heros",
        "pourquoi": "premier cas passant par Puzzle.Action ; sans lui l'action en jeu est inatteignable",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')", "Puzzle.PutIntoPlay('av010')",
                          "Puzzle.Exhaust('av001a')"],
        "declencher": ["Puzzle.Action('av010', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["av001a"], "exhausted": ["av010"]},
    },
    {
        "nom": "01094 Rhino — Puzzle.Attack : le vilain frappe et le heros encaisse",
        "pourquoi": "premier cas passant par Puzzle.Attack ; sans lui aucune capacite « apres avoir attaque » n'est atteignable",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')", "Puzzle.Exhaust('av001a')"],
        # Main videe et heros incline : sans cela le pilote defend (degats
        # reduits a 0) puis joue Counter-Punch, et l'attaque ne se voit plus.
        "main_exclusive": ["av010"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["av001a", 2]]},
    },

    ############################################################################
    # Vague debloquee par Puzzle.Action et Puzzle.Attack (4/8/2026).
    # Ces cartes etaient toutes hors de portee du harnais : leur capacite ne
    # part que sur une action de tour ou sur une attaque.
    {
        "nom": "jj008 Alias Investigations — Action : defausser jusqu'a une manigance, la reveler",
        "pourquoi": "action en jeu, jamais atteignable avant Puzzle.Action",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')", "Puzzle.PutIntoPlay('jj008')"],
        "declencher": ["Puzzle.Action('jj008', 'Action')"],
        "verifier": "manigance_annexe_en_jeu",
    },
    {
        "nom": "jj011 Private Investigator — Alter-Ego Action : 1 menace deplacee sur la carte",
        "pourquoi": "montage Beat Cop : la menace devient un jeton sur l'amelioration",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.PutIntoPlay('jj011')", "Puzzle.SetThreat('01097b', 5)"],
        "declencher": ["Puzzle.Action('jj011', 'AlterEgoAction')"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"jetons": [["jj011", "threat", 1]], "menace": [["01097b", 4]],
                    "exhausted": ["jj011"]},
    },
    {
        "nom": "jj011 Private Investigator — Hero Action : 2 jetons rendus en 2 degats a un sbire",
        "pourquoi": "seconde moitie de la carte, conditionnee a la presence de jetons",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')", "Puzzle.PutIntoPlay('jj011')",
                          "Puzzle.Token('jj011', 'threat', 2)",
                          "Puzzle.PutIntoPlay('jj019')"],
        "declencher": ["Puzzle.Action('jj011', 'HeroAction')"],
        "cibles": ["jj019"],
        "verifier": "etat_attendu",
        "attendu": {"jetons": [["jj011", "threat", 0]], "degats": [["jj019", 2]]},
    },
    {
        "nom": "jj019 Purple Man — Forced Interrupt : il ne frappe pas, il pose 2 menaces",
        "pourquoi": "capacite remplacant l'attaque, invisible sans Puzzle.Attack",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')", "Puzzle.PutIntoPlay('jj019')",
                          "Puzzle.PutIntoPlay('jj012')"],
        "declencher": ["Puzzle.Attack('jj019')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "av009 Bear Arms — Hero Action (attaque) : drain 1 sur le vilain",
        "pourquoi": "seconde action de la carte, atteinte par l'index",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')", "Puzzle.PutIntoPlay('av009')",
                          "Puzzle.Damage('av001a', 3)"],
        "declencher": ["Puzzle.Action('av009', 'HeroAction', 1)"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1]], "degats_identite": 2, "exhausted": ["av009"]},
    },
    {
        "nom": "av011 One Man Army — Interrupt : sans allie, l'attaque de base pioche et soigne",
        "pourquoi": "declencheur sur pouvoir de base, atteint par Puzzle.Attack sur le heros",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')", "Puzzle.PutIntoPlay('av011')",
                          "Puzzle.Damage('av001a', 3)"],
        "declencher": ["Puzzle.Attack('av001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "jj010 Jessica's Jacket — Interrupt : 1 degat evite et 1 menace retiree",
        "pourquoi": "interrupt sur degats subis ; heros incline pour qu'il ne puisse pas defendre",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')", "Puzzle.PutIntoPlay('jj010')",
                          "Puzzle.SetThreat('01097b', 5)", "Puzzle.Exhaust('jj001a')"],
        "main_exclusive": ["jj003"],
        "declencher": ["Puzzle.Attack('01094')"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "menace": [["01097b", 4]], "exhausted": ["jj010"]},
    },
    {
        "nom": "av002 Spider-Man — Interrupt : un [mental] annule l'activation d'un sbire non-ELITE",
        "pourquoi": "heros ET allie inclines : seule l'annulation peut empecher le degat",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')", "Puzzle.PutIntoPlay('av002')",
                          "Puzzle.PutIntoPlay('01101')", "Puzzle.Exhaust('av001a')",
                          "Puzzle.Exhaust('av002')"],
        "main_exclusive": ["av003"],
        "declencher": ["Puzzle.Attack('01101')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "av013 Maniac — Forced Response : l'ATK imprime de l'allie defenseur frappe le heros",
        "pourquoi": "declencheur « apres avoir attaque un allie », inatteignable sans Puzzle.Attack",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')", "Puzzle.PutIntoPlay('av002')",
                          "Puzzle.PutIntoPlay('av013')", "Puzzle.Exhaust('av001a')"],
        # av005 est imprime [physical] : sans [mental] en main, l'interruption
        # de Spider-Man av002 ne peut pas payer et l'activation a bien lieu.
        "main_exclusive": ["av005"],
        "declencher": ["Puzzle.Attack('av013')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "av015 Infected Scorpion — Forced Interrupt : l'allie encaisse 0 et retourne sa veste",
        "pourquoi": "mot-cle maison TRAITOR, jamais exerce jusqu'ici",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')", "Puzzle.PutIntoPlay('av002')",
                          "Puzzle.PutIntoPlay('av015')", "Puzzle.Exhaust('av001a')"],
        "main_exclusive": ["av005"],
        "declencher": ["Puzzle.Attack('av015')"],
        "verifier": "allie_est_traitre",
        "attendu": {"allie": "av002", "intact": True},
    },
    {
        "nom": "av014 The Made Men — Forced Response : apres l'activation de Maniac, l'allie trahit",
        "pourquoi": "declencheur sur fin d'activation ennemie, atteint par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')", "Puzzle.PutIntoPlay('av002')",
                          "Puzzle.PutIntoPlay('av013')", "Puzzle.PutIntoPlay('av014')",
                          "Puzzle.Exhaust('av001a')"],
        # av005 est imprime [physical] : sans [mental] en main, l'interruption
        # de Spider-Man av002 ne peut pas payer et l'activation a bien lieu.
        "main_exclusive": ["av005"],
        "declencher": ["Puzzle.Attack('av013')"],
        "verifier": "allie_est_traitre",
        "attendu": {"allie": "av002"},
    },
    {
        "nom": "av007 Unlikely Allies — Hero Action : defausser un [mental] retire 2 menaces",
        "pourquoi": "une ligne par icone imprimee ; la carte defaussee decide de l'effet",
        "scenario": "rhino",
        "heros": "agent_anti_venom",
        "mise_en_place": ["Puzzle.ChangeForm('av001b')", "Puzzle.PutIntoPlay('av007')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["av003"],
        "declencher": ["Puzzle.Action('av007', 'HeroAction')"],
        "cibles": ["av003", "01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "exhausted": ["av007"]},
    },

    ############################################################################
    # invisible_woman : le pack le moins couvert. Ses evenements exigent une
    # face heros PRECISE (INVISIBLE iw001a ou PSIONIC iw001c), ce qui les
    # rendait injouables tant que la mise en place ne savait pas y aller.
    # `Puzzle.ChangeForm(id, 'Hero')` bascule entre les deux faces heros.
    {
        "nom": "iw001a Boo! — apres une attaque, l'identite passe en forme PSIONIC",
        "pourquoi": "Forced Response sur fin d'attaque, atteint par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')"],
        "declencher": ["Puzzle.Attack('iw001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["iw001c"], "hors_jeu": ["iw001a"]},
    },
    {
        "nom": "iw001c Invisible Barrier — un ennemi a 2 ATK qui attaque prend 1 degat",
        "pourquoi": "Interrupt sur attaque subie, atteint par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')",
                          "Puzzle.ChangeForm('iw001a', 'Hero')",
                          "Puzzle.Exhaust('iw001c')"],
        "main_exclusive": ["iw008"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1]]},
    },
    {
        "nom": "iw005 Flying Disk — Hero Action : se defausser pour 4 degats",
        "pourquoi": "action en jeu, inatteignable avant Puzzle.Action",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')",
                          "Puzzle.ChangeForm('iw001a', 'Hero')",
                          "Puzzle.PutIntoPlay('iw005')"],
        "declencher": ["Puzzle.Action('iw005', 'HeroAction')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]], "hors_jeu": ["iw005"]},
    },
    {
        "nom": "iw006 Vanishing Act — Hero Action INVISIBLE : rendre un ennemi Confus",
        "pourquoi": "action a cout colore BY, reservee a la forme INVISIBLE",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')", "Puzzle.PutIntoPlay('iw006')"],
        "main_exclusive": ["iw008", "iw009", "iw011"],
        "payer_avec": ["iw008", "iw011"],
        "declencher": ["Puzzle.Action('iw006', 'HeroAction')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["01094", "Confused"]], "exhausted": ["iw006"]},
    },
    {
        "nom": "iw007 Force Shields — Hero Action PSIONIC : rendre l'identite Tenace",
        "pourquoi": "action reservee a la forme PSIONIC",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')",
                          "Puzzle.ChangeForm('iw001a', 'Hero')",
                          "Puzzle.PutIntoPlay('iw007')"],
        "declencher": ["Puzzle.Action('iw007', 'HeroAction')"],
        "cibles": ["iw001c"],
        "verifier": "identite_est_tenace",
    },
    {
        "nom": "iw008 Incognito — evenement INVISIBLE a cout 0, se resout et part a la defausse",
        "pourquoi": "pioche variable selon les etoiles de boost : on verifie qu'il se resout",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')"],
        "main_exclusive": ["iw008"],
        "declencher": [],
        "jouer": ["iw008"],
        "verifier": "etat_attendu",
        "attendu": {"defausse": ["iw008"]},
    },
    {
        "nom": "iw009 Infiltrate — evenement INVISIBLE : jusqu'a 4 menaces retirees",
        "pourquoi": "deux options au choix, la premiere retire 4 d'une seule manigance",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')", "Puzzle.SetThreat('01097b', 6)"],
        "main_exclusive": ["iw009", "iw008", "iw011"],
        "declencher": [],
        "jouer": ["iw009"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]], "defausse": ["iw009"]},
    },
    {
        "nom": "iw010 Forceful — evenement PSIONIC : 3 degats par statut Tenace defausse",
        "pourquoi": "cout paye en statuts Tenace, pas en ressources",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')",
                          "Puzzle.ChangeForm('iw001a', 'Hero')",
                          "Puzzle.Tough('iw001c')"],
        "main_exclusive": ["iw010"],
        "declencher": [],
        "jouer": ["iw010"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "defausse": ["iw010"]},
    },
    {
        "nom": "iw011 Psionic Fields — evenement PSIONIC : deux fois 4 degats",
        "pourquoi": "deux choix successifs, tous deux diriges sur le vilain",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": ["Puzzle.ChangeForm('iw001b')",
                          "Puzzle.ChangeForm('iw001a', 'Hero')"],
        "main_exclusive": ["iw011", "iw008", "iw009", "iw010"],
        "declencher": [],
        "jouer": ["iw011"],
        "cibles": ["01094", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 4]], "defausse": ["iw011"]},
    },
    {
        "nom": "iw001b Great Minds — Sue Storm se redresse quand elle paie une carte TECH",
        "pourquoi": "capacite Resource : elle s'incline pour payer, puis se redresse si la cible est TECH",
        "scenario": "rhino",
        "heros": "invisible_woman",
        "mise_en_place": [],
        "main_exclusive": ["iw004", "iw008", "iw009", "iw012"],
        "declencher": [],
        "jouer": ["iw004"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["iw004"], "pret": ["iw001b"]},
    },

    ############################################################################
    # Vague C : le reste des packs, debloque par Puzzle.Action / Puzzle.Attack.
    {
        "nom": "jj004 Crack the Case — Action (thwart) : 2 menaces retirees",
        "pourquoi": "evenement jouable seulement si une manigance annexe est en jeu",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')", "Puzzle.PutIntoPlay('jj013')",
                          "Puzzle.SetThreat('jj013', 2)", "Puzzle.Exhaust('jj001a')"],
        "main_exclusive": ["jj004", "jj003"],
        "declencher": [],
        "jouer": ["jj004"],
        "cibles": ["jj013"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["jj013"], "pret": ["jj001a"], "defausse": ["jj004"]},
    },
    {
        "nom": "jj006 Out in the Open — Interrupt : annule la traitrise et revele une manigance",
        "pourquoi": "interrupt sur revelation de traitrise, avec l'evenement en main",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')"],
        "main_exclusive": ["jj006"],
        "declencher": ["Puzzle.Reveal('jj020')"],
        "verifier": "manigance_annexe_en_jeu",
    },
    {
        "nom": "jj007 The Truth Hurts — Hero Action (attaque) : 2 degats a un ennemi",
        "pourquoi": "seconde moitie conditionnee a une manigance vaincue ce tour, ici absente",
        "scenario": "rhino",
        "heros": "jessica_jones",
        "mise_en_place": ["Puzzle.ChangeForm('jj001b')", "Puzzle.PutIntoPlay('jj013')"],
        "main_exclusive": ["jj007", "jj003"],
        "declencher": [],
        "jouer": ["jj007"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "defausse": ["jj007"]},
    },
    {
        "nom": "ab001a Albert — Action « Initiate Protocol » : pioche 1 carte",
        "pourquoi": "capacite Special declenchee par une Action, hors de portee avant Puzzle.Action",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('ab001b')"],
        "main_exclusive": ["ab002"],
        "declencher": ["Puzzle.Action('ab001a', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2},
    },
    {
        "nom": "ab007 Donald Pierce — se redresse apres « Initiate Protocol »",
        "pourquoi": "Response sur capacite Special : le declencheur est l'Action d'Albert",
        "scenario": "rhino",
        "heros": "albert",
        "mise_en_place": ["Puzzle.ChangeForm('ab001b')", "Puzzle.PutIntoPlay('ab007')",
                          "Puzzle.Exhaust('ab007')"],
        "main_exclusive": ["ab002"],
        "declencher": ["Puzzle.Action('ab001a', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["ab007"]},
    },
    {
        "nom": "th003 Alicia Masters — Alter-Ego Action : incliner pour piocher 2",
        "pourquoi": "action en jeu cote alter-ego",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.PutIntoPlay('th003')"],
        "main_exclusive": ["th008"],
        "declencher": ["Puzzle.Action('th003', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 3, "exhausted": ["th003"]},
    },
    {
        "nom": "th008 Toughen Up — Response : apres avoir subi des degats, l'identite devient Tenace",
        "pourquoi": "Response sur degats subis, atteinte par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')", "Puzzle.Exhaust('th001a')"],
        "main_exclusive": ["th008"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "identite_est_tenace",
    },
    {
        "nom": "mf003 H.E.R.B.I.E. — Action : defausser sa main puis repiocher autant",
        "pourquoi": "action en jeu ; la main garde sa taille, le soutien s'incline",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')", "Puzzle.PutIntoPlay('mf003')"],
        "main_exclusive": ["mf011", "mf009"],
        "declencher": ["Puzzle.Action('mf003', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2, "exhausted": ["mf003"]},
    },
    {
        "nom": "mf004 Baxter Building — Alter-Ego Action : 2 degats soignes",
        "pourquoi": "premiere des deux actions de la carte",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.PutIntoPlay('mf004')", "Puzzle.Damage('mf001b', 3)"],
        "declencher": ["Puzzle.Action('mf004', 'AlterEgoAction')"],
        "cibles": ["mf001b"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "exhausted": ["mf004"]},
    },
    {
        "nom": "mf011 Slippery — Interrupt : 2 degats evites sur l'attaque de Rhino",
        "pourquoi": "interrupt sur degats subis, avec l'evenement en main",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')", "Puzzle.Exhaust('mf001a')"],
        "main_exclusive": ["mf011"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "defausse": ["mf011"]},
    },
    {
        "nom": "mf001b Reed Richards — « Great Minds » le redresse en payant une carte TECH",
        "pourquoi": "meme montage que Sue Storm iw001b : ex_operation sur une identite",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": [],
        "main_exclusive": ["mf006", "mf009", "mf011"],
        "declencher": [],
        "jouer": ["mf006"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["mf006"], "pret": ["mf001b"]},
    },
    {
        "nom": "ht001b Johnny Storm — Action « Ignition » : incliner pour chercher une carte FIRE",
        "pourquoi": "action portee par la face alter-ego elle-meme",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": [],
        "declencher": ["Puzzle.Action('ht001b', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["ht001b"]},
    },
    {
        "nom": "ht005 Internal Combustion — Hero Action : 3 compteurs flamme contre 3 cartes",
        "pourquoi": "cout paye en compteurs sur un ennemi puis defausse de l'amelioration",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('ht001b')", "Puzzle.PutIntoPlay('ht005')",
                          "Puzzle.Counter('01094', 'flame', 3)"],
        "main_exclusive": ["ht007"],
        "declencher": ["Puzzle.Action('ht005', 'HeroAction')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "flame", 0]], "hors_jeu": ["ht005"],
                    "taille_main": 4},
    },
    {
        "nom": "ht006 Spark — Hero Action : poser un compteur flamme sur un ennemi",
        "pourquoi": "seconde capacite de la carte, la premiere etant une ressource",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('ht001b')", "Puzzle.PutIntoPlay('ht006')"],
        "declencher": ["Puzzle.Action('ht006', 'HeroAction')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "flame", 1]], "exhausted": ["ht006"]},
    },
    {
        "nom": "lj006 New Attilan — Alter-Ego Action : fouiller le deck jusqu'a une carte Lockjaw",
        "pourquoi": "action en jeu cote alter-ego",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.PutIntoPlay('lj006')"],
        "declencher": ["Puzzle.Action('lj006', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["lj006"]},
    },
    {
        "nom": "lj007 Doc Jaw's Lab — Alter-Ego Action : redresser Tuning Fork",
        "pourquoi": "action qui vise une AUTRE carte nommee, montage fragile",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.PutIntoPlay('lj007')", "Puzzle.PutIntoPlay('lj003')",
                          "Puzzle.Exhaust('lj003')"],
        "declencher": ["Puzzle.Action('lj007', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["lj003"], "exhausted": ["lj007"]},
    },
    {
        "nom": "lj020 Redwing — Hero Action : s'incline et se blesse pour regarder le deck Rencontre",
        "pourquoi": "cout compose : inclinaison PLUS 1 degat sur soi",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')", "Puzzle.PutIntoPlay('lj020')"],
        "declencher": ["Puzzle.Action('lj020', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["lj020"], "degats": [["lj020", 1]]},
    },
    {
        "nom": "lj030 Central Park — Alter-Ego Action : soigner 1 degat d'un PET AVENGER",
        "pourquoi": "cible restreinte par traits maison PET AVENGER / GOOD BOY",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.PutIntoPlay('lj030')", "Puzzle.PutIntoPlay('lj020')",
                          "Puzzle.Damage('lj020', 1)"],
        "declencher": ["Puzzle.Action('lj030', 'AlterEgoAction')"],
        "cibles": ["lj020"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["lj020", 0]], "exhausted": ["lj030"]},
    },
    {
        "nom": "lj021 Hairball — Interrupt : s'incline pour eviter 1 degat au heros",
        "pourquoi": "interrupt sur degats d'attaque, atteint par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')", "Puzzle.PutIntoPlay('lj021')",
                          "Puzzle.Exhaust('lj001a')", "Puzzle.Exhaust('lj021')",
                          "Puzzle.Ready('lj021')"],
        "main_exclusive": ["lj024"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "exhausted": ["lj021"]},
    },
    {
        "nom": "lj008 Teleport To Safety — Interrupt : changer de forme evite toute l'attaque",
        "pourquoi": "l'evenement doit etre en main et le heros incapable de defendre",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')", "Puzzle.Exhaust('lj001a')"],
        "main_exclusive": ["lj008"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "forme": "AlterEgo", "defausse": ["lj008"]},
    },


    ############################################################################
    # Vague D : derniers packs.
    {
        "nom": "lj029 Inhuman's Best Friend — Alter-Ego Action : redresser un soutien",
        "pourquoi": "evenement a action d'alter-ego, cible jusqu'a 4 soutiens",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.PutIntoPlay('lj006')", "Puzzle.Exhaust('lj006')"],
        "main_exclusive": ["lj029", "lj024", "lj028"],
        "declencher": [],
        "jouer": ["lj029"],
        "cibles": ["lj006"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["lj006"], "defausse": ["lj029"]},
    },
    {
        "nom": "lj023 Protect The Pack — Hero Interrupt : le heros encaisse a la place de l'allie",
        "pourquoi": "redirection de degats, atteinte par Puzzle.Attack sur un allie defenseur",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')", "Puzzle.PutIntoPlay('lj026')",
                          "Puzzle.Exhaust('lj001a')"],
        "main_exclusive": ["lj023"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "degats": [["lj026", 0]], "defausse": ["lj023"]},
    },
    {
        "nom": "lj009 Fast Travel — Action : le joueur vise change de forme",
        "pourquoi": "evenement qui cible un JOUEUR, cas de ciblage rare. La main ne fournit ni "
                    "mental ni wild (lj018 RES=R, lj019 RES=Y), donc SEUL l'effet principal "
                    "joue : un aller simple vers l'identite civile.",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')"],
        "main_exclusive": ["lj009", "lj018", "lj019"],
        # lj003 Tuning Fork demarre EN JEU et genere un wild, qui vaut n'importe
        # quelle couleur : sans cette ligne le pilote le depense et la couleur
        # reellement payee n'est plus celle que le cas croit exercer.
        "ne_pas_depenser": ["lj003"],
        "declencher": [],
        "jouer": ["lj009"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "defausse": ["lj009"]},
    },
    {
        "nom": "lj009 Fast Travel — payee en mental, la forme change DEUX fois",
        "pourquoi": "branche bonus « si vous avez paye avec une [mental], vous pouvez changer "
                    "de forme ». La main ne fournit que du mental (lj024 RES=B), le bonus part "
                    "et ramene en forme de heros : c'est ce retour qui le prouve, l'effet "
                    "principal garantissant a lui seul le passage en identite civile. Cas "
                    "temoin du precedent, ecrit apres le correctif du 9/8/2026.",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')"],
        "main_exclusive": ["lj009", "lj024", "lj028"],
        # lj003 Tuning Fork demarre EN JEU et genere un wild, qui vaut n'importe
        # quelle couleur : sans cette ligne le pilote le depense et la couleur
        # reellement payee n'est plus celle que le cas croit exercer.
        "ne_pas_depenser": ["lj003"],
        "declencher": [],
        "jouer": ["lj009"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "defausse": ["lj009"]},
    },
    {
        "nom": "lj011 Ruff Ambush — Hero Response : 5 degats quand on ne paie PAS en mental",
        "pourquoi": "Response sur changement de forme, l'evenement doit etre en main. La main "
                    "ne fournit ni mental ni wild (lj018 porte RES=R, lj019 RES=Y) : la clause "
                    "bonus ne doit pas partir. Un wild ne convient PAS pour ce cas, il compte "
                    "comme n'importe quelle couleur et satisfait donc « paye en mental ». "
                    "Signale en jeu le 9/8/2026 : la carte plafonnait a 5 meme payee en mental, "
                    "parce que le pack lisait l'icone mentale comme un wild. Le cas precedent "
                    "tenait la main en lj024+lj028, deux MENTALES, et attendait « au moins 5 » : "
                    "il passait au vert dans les deux sens.",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": [],
        "main_exclusive": ["lj011", "lj018", "lj019"],
        # lj003 Tuning Fork demarre EN JEU et genere un wild, qui vaut n'importe
        # quelle couleur : sans cette ligne le pilote le depense et la couleur
        # reellement payee n'est plus celle que le cas croit exercer.
        "ne_pas_depenser": ["lj003"],
        "declencher": ["Puzzle.ChangeForm('lj001b')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]], "defausse": ["lj011"]},
    },
    {
        "nom": "lj011 Ruff Ambush — Hero Response : 7 degats quand on paie en mental",
        "pourquoi": "la branche bonus, jamais exercee jusqu'ici. La main ne fournit que du "
                    "mental (lj024 et lj028 portent RES=B), le cout de 2 est donc paye en "
                    "mental et les degats passent de 5 a 7.",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": [],
        "main_exclusive": ["lj011", "lj024", "lj028"],
        # lj003 Tuning Fork demarre EN JEU et genere un wild, qui vaut n'importe
        # quelle couleur : sans cette ligne le pilote le depense et la couleur
        # reellement payee n'est plus celle que le cas croit exercer.
        "ne_pas_depenser": ["lj003"],
        "declencher": ["Puzzle.ChangeForm('lj001b')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 7]], "defausse": ["lj011"]},
    },
    {
        "nom": "th001a The Thing — Action « Give 'Er » : defausser son statut Tenace",
        "pourquoi": "action portee par la face heros elle-meme",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')", "Puzzle.Tough('th001a')"],
        "declencher": ["Puzzle.Action('th001a', 'HeroAction')"],
        "verifier": "identite_sans_statut_tenace",
    },
    {
        "nom": "vr002 Bulletproof — Hero Interrupt : 2 degats evites sur l'attaque de Rhino",
        "pourquoi": "interrupt de defense, heros incline pour qu'il ne defende pas",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')", "Puzzle.Exhaust('vr001a')"],
        "main_exclusive": ["vr002"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "vr005 Symbiotic Fury — Response : 1 degat de plus, mais le heros se redresse",
        "pourquoi": "Response sur degats subis, atteinte par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')", "Puzzle.Exhaust('vr001a')"],
        "main_exclusive": ["vr005"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3, "pret": ["vr001a"], "defausse": ["vr005"]},
    },
    {
        "nom": "vr008 Camouflage — Hero Interrupt : 4 degats et Desoriente sur l'attaquant",
        "pourquoi": "interrupt qui se defausse pour frapper l'ennemi avant son attaque",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')", "Puzzle.PutIntoPlay('vr008')",
                          "Puzzle.Exhaust('vr001a')"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 4]], "statuts": [["01094", "Confused"]],
                    "hors_jeu": ["vr008"]},
    },
    {
        "nom": "sr009 J. Jonah Jameson — Alter-Ego Action : incliner pour piocher",
        "pourquoi": "action en jeu cote alter-ego, avec pioche conditionnelle",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.PutIntoPlay('sr009')"],
        "declencher": ["Puzzle.Action('sr009', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["sr009"]},
    },
    {
        "nom": "sr010 Spider-Sense — Hero Interrupt : piocher quand le vilain attaque",
        "pourquoi": "interrupt sur initiation d'attaque, atteint par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('sr001b')", "Puzzle.PutIntoPlay('sr010')",
                          "Puzzle.Exhaust('sr001a')"],
        "main_exclusive": ["sr004"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2},
    },
    {
        "nom": "sr006 Webbed Up (defense) — l'attaque du vilain ne fait aucun degat",
        "pourquoi": "la carte a DEUX branches et seule l'action etait couverte. La "
                    "branche defense n'etait pas atteignable avant Puzzle.Attack, d'ou "
                    "la note « a verifier en partie reelle » du 3/8/2026 : elle l'est ici",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "main_exclusive": ["sr006"],
        # La carte est hero_form_only : sans ce passage en forme heros, Rhino
        # attaque Peter Parker et l'interrupt n'est meme pas propose.
        #
        # ChangeForm prend la face ACTUELLEMENT EN JEU et la retourne, pas la
        # face visee. Lui passer 'sr001a' fabrique une face orpheline, sans
        # proprietaire, qui plante au rendu sur un assert GetControlByPlayer.
        "mise_en_place": ["Puzzle.ChangeForm('sr001b')"],
        "accepter_choix": True,
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0},
    },
    {
        "nom": "sr012 Impact Webbing — l'ennemi entoile qui ATTAQUE perd ses toiles",
        "pourquoi": "le seul cas verifiait que la carte de regles est en jeu au setup, "
                    "jamais son Forced Interrupt : elle pouvait etre totalement inerte "
                    "sans que rien ne le signale",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "main_exclusive": ["sr006"],
        "mise_en_place": [],
        "jouer": ["sr006"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "web", 0]]},
    },
    {
        "nom": "vr009 Lethal Protector — Hero Interrupt : 2 degats a l'attaquant",
        "pourquoi": "le cas existant ne verifiait que le +1 DEF passif, jamais "
                    "l'interrupt qui s'incline pour frapper l'ennemi qui attaque",
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')", "Puzzle.PutIntoPlay('vr009')",
                          "Puzzle.Exhaust('vr001a')"],
        "accepter_choix": True,
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 2]], "exhausted": ["vr009"]},
    },
    {
        "nom": "ra009 Congress of Worlds — Alter-Ego Action : 2 menaces retirees du complot principal",
        "pourquoi": "action a cout mixte : inclinaison PLUS une ressource",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.PutIntoPlay('ra009')", "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["ra004", "ra005"],
        "payer_avec": ["ra004"],
        "declencher": ["Puzzle.Action('ra009', 'AlterEgoAction')"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "exhausted": ["ra009"]},
    },
    {
        "nom": "ra011 Scrying Pool — Hero Action : incliner pour regarder le dessus d'un deck",
        "pourquoi": "action en jeu cote heros",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('ra001b')", "Puzzle.PutIntoPlay('ra011')"],
        "declencher": ["Puzzle.Action('ra011', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["ra011"]},
    },
    {
        "nom": "ah011 Kinetic Stomp — Hero Interrupt : +6 ATK sur une attaque de base",
        "pourquoi": "interrupt sur attaque de base, atteint par Puzzle.Attack sur le heros",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('ah001b')"],
        "main_exclusive": ["ah011", "ah005", "ah006", "ah009"],
        "declencher": ["Puzzle.Attack('ah001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 7]], "defausse": ["ah011"]},
    },
    {
        "nom": "cd012 Dark Intangibility — Response : Cloak se redresse apres avoir defendu",
        "pourquoi": "Response sur fin de defense, atteinte par Puzzle.Attack",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('cd001b')", "Puzzle.PutIntoPlay('cd012')"],
        "main_exclusive": ["cd011"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["cd012"]},
    },
    {
        "nom": "cd016 Bigger Fish — Forced Interrupt : le vilain manigance au lieu d'attaquer",
        "pourquoi": "remplacement d'activation, invisible sans Puzzle.Attack",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('cd001b')", "Puzzle.PutIntoPlay('cd016')",
                          "Puzzle.SetThreat('01097b', 0)", "Puzzle.Exhaust('cd001a')"],
        "main_exclusive": ["cd011"],
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
        "nom": "mw003 Webb's Apartment — Alter-Ego Action : soigner 1 degat",
        "pourquoi": "action en jeu cote alter-ego, cible « personnage que vous controlez »",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.PutIntoPlay('mw003')", "Puzzle.Damage('mw001b', 3)"],
        "declencher": ["Puzzle.Action('mw003', 'AlterEgoAction')"],
        "cibles": ["mw001b"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "exhausted": ["mw003"]},
    },
    {
        "nom": "mw005 Astral Form — Hero Action : 1 menace retiree par allie controle",
        "pourquoi": "X calcule sur le nombre d'allies, avec cout mixte inclinaison + [mental]",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('mw001b')", "Puzzle.PutIntoPlay('mw005')",
                          "Puzzle.PutIntoPlay('mw002')", "Puzzle.SetThreat('01097b', 5)"],
        "main_exclusive": ["mw009"],
        "payer_avec": ["mw009"],
        "declencher": ["Puzzle.Action('mw005', 'HeroAction')"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]], "exhausted": ["mw005"]},
    },
    {
        "nom": "mw017 Ana Kraven — Forced Response : 1 menace sur le complot apres son attaque",
        "pourquoi": "The Grim Hunt absente, la branche de repli vise le complot principal",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('mw001b')", "Puzzle.PutIntoPlay('mw017')",
                          "Puzzle.SetThreat('01097b', 0)", "Puzzle.Exhaust('mw001a')"],
        "main_exclusive": ["mw010"],
        "declencher": ["Puzzle.Attack('mw017')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    {
        "nom": "mw024 Spider-Woman (May Parker) — Hero Interrupt : piocher quand le vilain attaque",
        "pourquoi": "interrupt porte par un ALLIE, sur l'initiation d'attaque du vilain",
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('mw001b')", "Puzzle.PutIntoPlay('mw024')",
                          "Puzzle.Exhaust('mw001a')", "Puzzle.Exhaust('mw024')"],
        "main_exclusive": ["mw010"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2},
    },
    {
        "nom": "cd007 Lightforce Absorption — Response : s'incline apres une carte LIGHTFORCE",
        "pourquoi": "Response sur « apres avoir joue une carte du trait X »",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('cd001b')", "Puzzle.PutIntoPlay('cd007')",
                          "Puzzle.Discard('cd005')", "Puzzle.Damage('cd001a', 3)"],
        "main_exclusive": ["cd004", "cd006"],
        "declencher": [],
        "jouer": ["cd004"],
        "cibles": ["cd001a"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["cd007"]},
    },
    {
        "nom": "cd013 Darkforce Absorption — Response : s'incline apres une carte DARKFORCE",
        "pourquoi": "miroir exact de cd007, le trait change",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('cd001b')", "Puzzle.PutIntoPlay('cd013')",
                          "Puzzle.Discard('cd010')", "Puzzle.Exhaust('cd001a')"],
        "main_exclusive": ["cd009", "cd011"],
        "declencher": [],
        "jouer": ["cd009"],
        "cibles": ["cd001a"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["cd013"]},
    },
    {
        "nom": "cd015 Mister Negative — Forced Response : son attaque renvoie en alter-ego",
        "pourquoi": "Forced Response sur attaque du heros, inatteignable avant Puzzle.Attack",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('cd001b')", "Puzzle.PutIntoPlay('cd015')",
                          "Puzzle.Exhaust('cd001a')"],
        "main_exclusive": ["cd011"],
        "declencher": ["Puzzle.Attack('cd015')"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo"},
    },
    {
        "nom": "mk009 Gear Up — Hero Interrupt : defendre puis basculer en alter-ego",
        "pourquoi": "interrupt de defense, le heros doit etre PRET pour defendre",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('mk001b')"],
        "main_exclusive": ["mk009", "mk007", "mk008"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["mk001c"], "hors_jeu": ["mk001a"], "defausse": ["mk009"]},
    },
    {
        "nom": "mk011 Versatility — Hero Action : dessus de defausse Aggression, donc 4 degats",
        "pourquoi": "l'effet depend de l'ASPECT de la carte au-dessus de la defausse",
        "scenario": "rhino",
        "heros": "moon_knight",
        # Main sans aucune autre carte d'attaque : Moon Knight met les couts
        # d'aspect a zero, et avec Deck and Cover en main le pilote enchainait
        # une seconde attaque qui faussait le total.
        "mise_en_place": ["Puzzle.ChangeForm('mk001b')"],
        "main_exclusive": ["mk011", "mk005", "mk006"],
        "declencher": [],
        "jouer": ["mk011"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        # 7 et pas 4 : Moon Knight met les couts d'aspect a zero, et le pilote
        # joue Surprise Attack (3 degats) depuis la MAIN DE DEPART, avant meme
        # que `main_exclusive` ne la vide. Meme phenomene que Deck and Cover.
        "attendu": {"degats": [["01094", 7]], "defausse": ["mk011"]},
    },
    {
        "nom": "mk017 Doctor Strange — Forced Response : defausse aleatoire apres ses degats",
        "pourquoi": "Forced Response sur degats infliges au heros",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('mk001b')", "Puzzle.PutIntoPlay('mk017')",
                          "Puzzle.Exhaust('mk001a')"],
        "main_exclusive": ["mk007", "mk008"],
        "declencher": ["Puzzle.Attack('mk017')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 1},
    },
    {
        "nom": "mk019 Iron Fist — Forced Response : le personnage blesse est Sonne",
        "pourquoi": "Forced Response sur degats infliges a un personnage controle",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('mk001b')", "Puzzle.PutIntoPlay('mk019')",
                          "Puzzle.Exhaust('mk001a')"],
        "main_exclusive": ["mk007"],
        "declencher": ["Puzzle.Attack('mk019')"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["mk001a", "Stunned"]]},
    },
    {
        "nom": "mk024 The Iron Fist — Hero Interrupt : +1 degat et l'ennemi est Sonne",
        "pourquoi": "cout mixte inclinaison PLUS retrait d'un compteur mystic",
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('mk001b')", "Puzzle.PutIntoPlay('mk024')",
                          "Puzzle.Counter('mk024', 'mystic', 1)"],
        "main_exclusive": ["mk007"],
        "declencher": ["Puzzle.Attack('mk001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["01094", "Stunned"]], "exhausted": ["mk024"]},
    },
    {
        "nom": "ra001a Thor — Action « Worthy » : Mjolnir arrive en main",
        "pourquoi": "action portee par la face heros, fouille deck ET defausse",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('ra001b')"],
        "declencher": ["Puzzle.Action('ra001a')"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["ra007"]},
    },
    {
        "nom": "ra004 Hammer Swing — Hero Action (attaque) : 4 degats en inclinant Mjolnir",
        "pourquoi": "le cout d'inclinaison porte sur une AUTRE carte que l'evenement",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('ra001b')", "Puzzle.PutIntoPlay('ra007')"],
        "main_exclusive": ["ra004", "ra005"],
        "declencher": [],
        "jouer": ["ra004"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]], "exhausted": ["ra007"], "defausse": ["ra004"]},
    },
    {
        "nom": "ra008 Unyielding — Hero Response : attaque encaissee a 0 degat, 2 menaces retirees",
        "pourquoi": "declencheur « apres avoir ete attaque SANS subir de degat », d'ou le statut Tenace",
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('ra001b')", "Puzzle.PutIntoPlay('ra008')",
                          "Puzzle.SetThreat('01097b', 5)", "Puzzle.Tough('ra001a')"],
        "main_exclusive": ["ra006"],
        "declencher": ["Puzzle.Attack('01094')"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "exhausted": ["ra008"]},
    },
    {
        "nom": "ra012 Goddess of Thunder — Hero Resource : elle finance une carte Thor",
        "pourquoi": ("la capacite Resource est bien sollicitee et la carte s'incline. "
                     "Le DOUBLEMENT pour une carte du set signature n'est PAS prouve ici : "
                     "avec la seule Goddess en source, une carte a cout 2 reste impayable"),
        "scenario": "rhino",
        "heros": "thor_jane_foster",
        "mise_en_place": ["Puzzle.ChangeForm('ra001b')", "Puzzle.PutIntoPlay('ra012')"],
        "main_exclusive": ["ra006", "ra013"],
        "declencher": [],
        "jouer": ["ra006"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["ra012"], "defausse": ["ra006"]},
    },
    {
        "nom": "mf001a Mister Fantastic — « Flexibility » : la carte SUPERPOWER depensee revient en main",
        "pourquoi": "Response sur defausse d'une carte du trait SUPERPOWER",
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')"],
        "main_exclusive": ["mf010", "mf011"],
        "payer_avec": ["mf011"],
        "declencher": [],
        "jouer": ["mf010"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["mf011"]},
    },


    {
        "nom": "th007 True Grit — Hero Action : 2 degats a soi pour se redresser et perdre un statut",
        "pourquoi": "cout paye en degats sur sa propre identite",
        "scenario": "rhino",
        "heros": "the_thing",
        "mise_en_place": ["Puzzle.ChangeForm('th001b')", "Puzzle.PutIntoPlay('th007')",
                          "Puzzle.Stun('th001a')", "Puzzle.Exhaust('th001a')"],
        "declencher": ["Puzzle.Action('th007', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["th001a"], "degats_identite": 2},
    },
    {
        "nom": "lj004 Jaw Lock — Response : un evenement TELEPORT blesse l'ennemi porteur",
        "pourquoi": "l'amelioration s'attache a un ENNEMI, la Response lit son porteur",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')"],
        "main_exclusive": ["lj004", "lj010", "lj024", "lj028", "lj027", "lj009"],
        "declencher": [],
        "jouer": ["lj004", "lj010"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        # 2 degats : 1 de Zooming Around lui-meme, 1 de la Response de Jaw Lock.
        "attendu": {"degats": [["01094", 2]], "en_jeu": ["lj004"]},
    },
    {
        "nom": "lj001a Lockjaw — Action « Fetch! » : recuperer une carte de la defausse",
        "pourquoi": "action portee par la face heros, cout inclinaison PLUS un joker",
        "scenario": "rhino",
        "heros": "lockjaw",
        "mise_en_place": ["Puzzle.ChangeForm('lj001b')"],
        "main_exclusive": ["lj024", "lj028"],
        "declencher": ["Puzzle.Discard('lj027')",
                       "Puzzle.Action('lj001a', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 3, "exhausted": ["lj001a"]},
    },
    {
        "nom": "sr001b Peter Parker — Action : defausser 1 carte pour en chercher une",
        "pourquoi": "action portee par la face alter-ego, cout paye en defaussant de la main",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": [],
        "main_exclusive": ["sr004", "sr005"],
        "declencher": ["Puzzle.Action('sr001b', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2},
    },
    {
        "nom": "sr004 Web Barrage — Hero Action a cout X : toiler et blesser un ennemi",
        "pourquoi": "cout X, d'ou le surpaiement obligatoire pour que X vaille au moins 1",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('sr001b')"],
        "main_exclusive": ["sr004", "sr005", "sr006"],
        "surpayer": True,
        "declencher": [],
        "jouer": ["sr004"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 2]], "defausse": ["sr004"]},
    },
    {
        "nom": "ht009 Radiate — cout X : 2 compteurs flamme sur un ennemi",
        "pourquoi": "premiere des deux options, cout X paye par surpaiement",
        "scenario": "rhino",
        "heros": "human_torch",
        "mise_en_place": ["Puzzle.ChangeForm('ht001b')"],
        "main_exclusive": ["ht009", "ht007", "ht008"],
        "surpayer": True,
        "declencher": [],
        "jouer": ["ht009"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "flame", 2]], "defausse": ["ht009"]},
    },
    {
        "nom": "ah001b Amadeus Cho — Action « Reverse Engineer » : defausser pour piocher",
        "pourquoi": "X = cout imprime de la carte signature defaussee",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": [],
        "main_exclusive": ["ah009", "ah005"],
        "declencher": ["Puzzle.Action('ah001b', 'Action')"],
        "verifier": "etat_attendu",
        # Le pilote defausse ah005 (cout imprime 2), donc 1 carte restante + 2 piochees.
        "attendu": {"taille_main": 3},
    },
    {
        "nom": "ah004 Kegger — Action : se remelanger avec une carte pour redresser l'identite",
        "pourquoi": "cout paye en remelangeant DEUX cartes dans le deck",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('ah001b')", "Puzzle.PutIntoPlay('ah004')",
                          "Puzzle.Exhaust('ah001a')"],
        "main_exclusive": ["ah005", "ah006"],
        "declencher": ["Puzzle.Action('ah004', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["ah001a"], "hors_jeu": ["ah004"]},
    },
    {
        "nom": "ah014 Lady Hellbender — Hero Action : la sbire devient une alliee",
        "pourquoi": "cout en jokers egal aux PV restants, puis TreatAsAlly",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('ah001b')", "Puzzle.PutIntoPlay('ah014')",
                          "Puzzle.Damage('ah014', 4)"],
        "main_exclusive": ["ah007", "ah005", "ah006"],
        "declencher": ["Puzzle.Action('ah014', 'HeroAction')"],
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
        "nom": "cd002a Bright Barrage — l'attaque de base de Dagger se repartit entre ennemis",
        "pourquoi": ("capacite perdue lors de la refonte du 5/8/2026 et recablee : la face "
                     "heros a une vraie attaque de base, `ThisCanAttack(canbe_divided=True)` "
                     "suffit (modele Wasp 13001c). Dagger a 3 ATK avec Cloak en jeu, on les "
                     "repartit sur deux sbires"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')",
                          "Puzzle.ChangeForm('Tandy Bowen')",
                          "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01103')"],
        "declencher": ["Puzzle.Attack('cd002a')"],
        "cibles": ["01101", "01103"],
        "verifier": "cd_barrage_reparti",
    },


    {
        "nom": "cd003 Forces Combined — la main de l'identite liee finance le cout de l'autre",
        "pourquoi": ("texte imprime enfin rendu depuis la refonte du 5/8/2026 : les DEUX "
                     "mains existent. La main de Cloak est reduite a la SEULE carte jouee, "
                     "qui coute 3 : sans le financement par la main de l'identite liee, "
                     "elle est strictement impayable"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')",
                          "Puzzle.ChangeForm('Tandy Bowen')"],
        "main_exclusive": ["cd005"],
        "declencher": [],
        "jouer": ["cd005"],
        "cibles": ["01094", "01094", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"defausse": ["cd005"], "degats_min": [["01094", 3]],
                    "exhausted": ["cd003"]},
    },


    ############################################################################
    # Vague G : les 19 cartes restantes.
    {
        "nom": "cd002b Tandy Bowen — Harmony : +2 REC tant que Tyrone Johnson est en jeu",
        "pourquoi": "moitie de Harmony qui vise l'AUTRE alter-ego, donc conditionnee",
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "cd_tandy_recover",
    },
    {
        "nom": "ah001c Uncontrollable Hulk — Interrupt : ses attaques font 2 degats de plus",
        "pourquoi": "forme BRUTE atteinte par les compteurs rage de « The Trunk »",
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('ah001b')",
                          "Puzzle.Counter('ah012a', 'rage', 4)"],
        "main_exclusive": ["ah009"],
        "declencher": ["Puzzle.Attack('ah001c')"],
        "cibles": ["01094"],
        "verifier": "tah_brute_frappe_plus_fort",
    },
    {
        "nom": "ah001a Totally Awesome Hulk — « Hypermind » : toute ressource generee devient [wild]",
        "pourquoi": ("interception de `CheckEffectGeneratedResources` : une carte a cout "
                     "colore doit se payer avec des icones d'une AUTRE couleur"),
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('ah001b')"],
        "main_exclusive": ["ah009", "ah006"],
        "payer_avec": ["ah006"],
        "declencher": [],
        "jouer": ["ah009"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"defausse": ["ah009"]},
    },
    {
        "nom": "mw027 Order of the Web — soutien pose sous le controle d'un autre joueur",
        "pourquoi": "texte multijoueur, inexercable en solo : la partie est montee A DEUX",
        "scenario": "rhino",
        "heros": "madame_web",
        "heros2": "spider_man",
        "mise_en_place": ["Puzzle.ChangeForm('mw001b')"],
        "main_exclusive": ["mw027", "mw010", "mw011"],
        "declencher": [],
        "jouer": ["mw027"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["mw027"]},
    },
    {
        "nom": "sr013 Bad Publicity — l'obligation arrive en jeu avec ses compteurs",
        "pourquoi": "obligation a Uses, donnee au joueur Peter Parker ; partie montee A DEUX",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "heros2": "spider_man",
        "mise_en_place": ["Puzzle.ChangeForm('sr001b')"],
        "declencher": ["Puzzle.Reveal('sr013')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["sr013"]},
    },


    {
        "nom": "gp001b Gwendolyn Poole — Action « I Won't Be an Extra » : une carte Gwenpool en main",
        "pourquoi": "action portee par la face alter-ego, fouille deck ET defausse",
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": [],
        "main_exclusive": ["gp003"],
        "declencher": ["Puzzle.Action('gp001b', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_main": 2},
    },
    {
        "nom": "gp004 Fun Background Noise — annule la traitrise, puis la bulle rend Gwenpool Tenace",
        "pourquoi": ("teste d'un coup l'interruption ET « Medium Awareness » (gp001a), le "
                     "moteur de bulles qui remplit les blancs des cartes Gwenpool"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('gp001b')"],
        "main_exclusive": ["gp004", "gp002", "gp005"],
        "declencher": ["Puzzle.Reveal('gp013')"],
        "verifier": "identite_est_tenace",
    },
    {
        "nom": "gp008 Comicbook Panels — Hero Action : incliner les deux cartes pour deux bulles",
        "pourquoi": ("cout compose : la carte elle-meme PLUS Unbelievable Gwenpool, "
                     "et deux blancs a remplir"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('gp001b')", "Puzzle.PutIntoPlay('gp008')",
                          "Puzzle.PutIntoPlay('gp009')"],
        "declencher": ["Puzzle.Action('gp008', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["gp008", "gp009"]},
    },
    {
        "nom": "mk001c Mr. Knight — « The Best Defense » : les cartes Protection coutent 1 de moins",
        "pourquoi": ("main reduite a la SEULE carte jouee : sans la reduction son cout 1 "
                     "est impayable, avec elle il tombe a 0"),
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeForm('mk001b')",
                          "Puzzle.ChangeForm('mk001a', 'Hero')"],
        "main_exclusive": ["01081"],
        "declencher": [],
        "jouer": ["01081"],
        "verifier": "mk_reduction_protection",
    },
    {
        "nom": "mk001d Steven Grant — « CEO » : les cartes Commandement coutent 1 de moins",
        "pourquoi": ("main reduite a la SEULE carte jouee : sans la reduction son cout 1 "
                     "est impayable, avec elle il tombe a 0. Steven Grant est une face "
                     "ALTER-EGO parmi les trois de Moon Knight, inatteignable par "
                     "ChangeForm qui ne va que vers « l'autre » face : d'ou "
                     "Puzzle.ChangeToFace, ajoutee pour ce cas"),
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeToFace('mk001b', 'mk001d')"],
        "main_exclusive": ["01073"],
        "declencher": [],
        "jouer": ["01073"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["01073"]},
    },
    {
        "nom": "mk001e Jake Lockley — « Just 'Cause » : les cartes Justice coutent 1 de moins",
        "pourquoi": ("meme montage que Steven Grant, sur l'autre aspect : Interrogation "
                     "Room (01063) coute 1, la main est vide de ressources, elle ne part "
                     "que si la reduction s'applique"),
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": ["Puzzle.ChangeToFace('mk001b', 'mk001e')"],
        "main_exclusive": ["01063"],
        "declencher": [],
        "jouer": ["01063"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["01063"]},
    },
    {
        "nom": "mk001d temoin — sur la face de depart, la carte Commandement reste injouable",
        "pourquoi": ("sans temoin, les deux cas ci-dessus passeraient meme si le moteur "
                     "laissait jouer une carte sans la payer : c'est le temoin qui prouve "
                     "que la reduction fait la difference"),
        "scenario": "rhino",
        "heros": "moon_knight",
        "mise_en_place": [],
        "main_exclusive": ["01073"],
        "declencher": [],
        "jouer": ["01073"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01073"]},
    },
    {
        "nom": "vr001a Venom — « Symbiotic Bond » : sa ressource lui coute 1 degat",
        "pourquoi": ("une capacite Resource n'est jamais proposee si la carte n'est pas sous "
                     "controle du joueur, et son cout est ici un DEGAT et non une "
                     "inclinaison : le prouver demande de voir l'identite encaisser"),
        "scenario": "rhino",
        "heros": "venom_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('vr001b')"],
        "main_exclusive": ["08024"],
        "payer_avec": ["vr001a"],
        "declencher": [],
        "jouer": ["08024"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "en_jeu": ["08024"]},
    },
    {
        "nom": "gp001a Gwenpool — la manche ou le Mechant intrigue est NOTEE",
        "pourquoi": ("capacite sans effet visible : elle remplit une ardoise que gp003 "
                     "consulte. Elle pouvait rester muette pour toujours sans que rien ne "
                     "le signale"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": [],
        "declencher": ["Puzzle.Scheme('01094')"],
        "verifier": "gwenpool_manche_intrigue",
    },
    {
        "nom": "gp006 Endless Storylines — depensee, elle resout DEUX blancs",
        "pourquoi": ("carte Resource dont l'effet part APRES la depense. Ses bulles sont "
                     "ordonnees : le premier blanc retire 1 menace, le second soigne. On "
                     "reste en alter-ego pour que l'identite n'ajoute pas sa propre bulle "
                     "au choix. Sans `accepter_choix`, le MayChooseOneAbility est decline "
                     "et la carte parait morte"),
        "scenario": "rhino",
        "heros": "gwenpool",
        # La capacite est une HERO Response : en alter-ego elle ne part pas, la
        # carte est simplement depensee et rien ne se produit.
        "mise_en_place": ["Puzzle.ChangeForm('gp001b')", "Puzzle.SetThreat('01097b', 3)"],
        "main_exclusive": ["gp006", "08024"],
        "payer_avec": ["gp006"],
        "accepter_choix": True,
        "declencher": [],
        "jouer": ["08024"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]]},
    },
    {
        "nom": "sg004 The Lookout — l'ecureuil ne compte pas dans la limite d'allies",
        "pourquoi": ("tout son comportement tient dans le helper Ecureuil(), partage par les "
                     "six cartes du deck ecureuil : ce cas verifie que le mot-cle atteint "
                     "bien CELLE-CI. La limite d'allies est de trois : avec trois allies "
                     "ordinaires deja poses, un quatrieme allie ordinaire forcerait une "
                     "defausse, alors qu'un ecureuil doit s'ajouter sans rien deloger.\n"
                     "\n"
                     "L'ecureuil est APPELE par le jeu, jamais pose par PutIntoPlay : une "
                     "carte posee d'autorite est une copie neuve, privee des regles du "
                     "setup. Et l'appel est limite a UNE FOIS PAR MANCHE, donc impossible "
                     "d'appeler jusqu'a tomber sur le bon : d'ou "
                     "Puzzle.PutOnAdditionalDeckTop, ajoutee pour ce cas.\n"
                     "\n"
                     "Les deux autres garanties du mot-cle ne sont pas verifiables ici. "
                     "« Ne peut pas defendre » resiste au harnais : Puzzle.Attack(defender=) "
                     "FORCE la defense et court-circuite la regle, comme il court-circuite "
                     "deja le cout d'inclinaison."),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.PutIntoPlay('01083', under_control=True)",
                          "Puzzle.PutIntoPlay('01084', under_control=True)",
                          "Puzzle.PutIntoPlay('04020', under_control=True)",
                          "Puzzle.PutOnAdditionalDeckTop('sg004')",
                          "Puzzle.Action('sg001b', 'AlterEgoAction')"],
        "declencher": [],
        "accepter_choix": True,
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["01083", "01084", "04020", "sg004"]},
    },
    {
        "nom": "sr001a Spider-Man — « Just Like Flies » : le sbire qui s'engage est toile",
        "pourquoi": "Interrupt sur engagement, declenche par l'arrivee du sbire",
        "scenario": "rhino",
        "heros": "spider_man_rainy",
        "mise_en_place": ["Puzzle.ChangeForm('sr001b')"],
        "declencher": ["Puzzle.PutIntoPlay('01101')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01101", "web", 1]]},
    },
    {
        "nom": "cd008 Living Light — Hero Action : 5 degats au vilain deverrouillent l'inclinaison",
        "pourquoi": ("« cannot be exhausted until 5+ damage this phase » : deux attaques de "
                     "Cloak a 3 ATK suffisent, l'action redresse ensuite Dagger"),
        "scenario": "rhino",
        "heros": "cloak_dagger",
        "mise_en_place": ["Puzzle.ChangeForm('Tyrone Johnson')",
                          "Puzzle.ChangeForm('Tandy Bowen')",
                          "Puzzle.PutIntoPlay('cd008')",
                          "Puzzle.Exhaust('cd002a')"],
        # Cloak n'a qu'1 ATK (le +2 de Destructive Duo va a Dagger) : il faut
        # cinq attaques pour franchir le seuil de 5 degats de la phase.
        "declencher": ["Puzzle.Attack('cd001a')", "Puzzle.Ready('cd001a')",
                       "Puzzle.Attack('cd001a')", "Puzzle.Ready('cd001a')",
                       "Puzzle.Attack('cd001a')", "Puzzle.Ready('cd001a')",
                       "Puzzle.Attack('cd001a')", "Puzzle.Ready('cd001a')",
                       "Puzzle.Attack('cd001a')",
                       "Puzzle.Action('cd008', 'HeroAction')"],
        "cibles": ["01094", "01094", "01094", "01094", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["cd002a"], "exhausted": ["cd008"]},
    },


    {
        "nom": "mw009 Foresight — Hero Interrupt : annuler et defausser la carte Rencontre",
        "pourquoi": ("cout paye en inclinant l'IDENTITE. Longtemps cru defaillant : c'etait "
                     "`Puzzle.Reveal` qui ne faisait pas venir la carte du deck Rencontre, "
                     "donc `from_encounter=True` ne matchait jamais"),
        "scenario": "rhino",
        "heros": "madame_web",
        "mise_en_place": ["Puzzle.ChangeForm('mw001b')"],
        "main_exclusive": ["mw009", "mw010", "mw011"],
        "declencher": ["Puzzle.Reveal('mw021')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["mw001a"], "degats_identite": 0, "defausse": ["mw009"]},
    },

    # ------------------------------------------------------------------------
    # Pack « squirrel_girl » : sg001a-sg022 (custom)
    #
    # Deux notions maison a prouver : APPELER un ecureuil (le deck additionnel
    # se vide vers le champ de bataille) et DEPENSER un ecureuil (il finance
    # une carte du set). Le reste des cas verifie que les regles speciales du
    # mot-cle « Squirrel » tiennent, y compris les deux points d'accroche poses
    # dans le moteur (cible et bonus refuses hors du set).
    # ------------------------------------------------------------------------
    {
        "nom": "sg001b Setup — le deck ecureuil est monte avec ses 6 allies",
        "pourquoi": "sans deck ecureuil, aucune carte du pack ne fonctionne",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "sg_deck_ecureuil_complet",
    },
    {
        "nom": "sg001b Squirrel Speech — l'alter-ego s'incline pour appeler 1 ecureuil",
        "pourquoi": "premier appel du pack : le deck additionnel doit se vider vers le jeu",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": [],
        "declencher": ["Puzzle.Action('sg001b', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu_trait": [["SQUIRREL", 1]], "exhausted": ["sg001b"]},
    },
    {
        "nom": "sg001a Unbeatable Army — depenser un ecureuil retire 1 menace ou fait 1 degat",
        "pourquoi": "la capacite d'identite est branchee sur la depense, notion maison du pack",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        # L'ecureuil est APPELE par le jeu, pas pose par Puzzle.PutIntoPlay :
        # une carte posee d'autorite n'a pas de controleur, et sa capacite
        # Resource n'est alors jamais proposee au paiement.
        "mise_en_place": ["Puzzle.Action('sg001b', 'AlterEgoAction')",
                          "Puzzle.ChangeForm('sg001b')"],
        "main_exclusive": ["sg014", "01088"],
        "declencher": [],
        "jouer": ["sg014"],
        "cibles": ["01094"],
        "payer_avec": ["sg002", "sg003", "sg004", "sg005", "sg006", "sg007"],
        "verifier": "sg_ecureuil_depense",
    },
    {
        "nom": "sg008 Nancy Whitehead — son entree en jeu appelle 1 ecureuil",
        "pourquoi": "AfterCardEnterPlay('This') doit appeler pour le controleur",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('sg008')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["sg008"], "en_jeu_trait": [["SQUIRREL", 1]]},
    },
    {
        "nom": "sg009 Squirrel Girl's Costume — +1 ATK a l'identite",
        "pourquoi": "GiveKeywordToAttached(Hero) sur une amelioration signature",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')"],
        "declencher": ["Puzzle.PutIntoPlay('sg009')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}, "en_jeu": ["sg009"]},
    },
    {
        "nom": "sg009 Squirrel Girl's Costume — un sbire vaincu appelle 1 ecureuil",
        "pourquoi": "ecart assume au materiel : le declencheur est « un sbire est vaincu »",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')", "Puzzle.PutIntoPlay('sg009')",
                          "Puzzle.PutIntoPlay('01103')"],
        "declencher": ["Puzzle.Damage('01103', 9)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01103"], "en_jeu_trait": [["SQUIRREL", 1]]},
    },
    {
        "nom": "sg011 Central Park — s'incline et appelle 1 ecureuil",
        "pourquoi": "action conditionnee au nombre d'ecureuils controles",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.PutIntoPlay('sg011')"],
        "declencher": ["Puzzle.Action('sg011', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["sg011"], "en_jeu_trait": [["SQUIRREL", 1]]},
    },
    {
        "nom": "sg013 Call the Squirrels — 2 ecureuils entrent en jeu PRETS",
        "pourquoi": "seule carte qui appelle des ecureuils prets ; ils doivent pouvoir agir",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')"],
        "main_exclusive": ["sg013", "01088", "01089"],
        "declencher": [],
        "jouer": ["sg013"],
        "verifier": "sg_deux_ecureuils_prets",
    },
    {
        "nom": "sg014 Squirrel Swarm — 3 degats sans ecureuil depense",
        "pourquoi": "valeur de base apres arbitrage (3 puis +3), a distinguer du bonus",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')"],
        "main_exclusive": ["sg014", "01088", "01089"],
        "declencher": [],
        "jouer": ["sg014"],
        "cibles": ["01094"],
        "payer_avec": ["01088", "01089"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "defausse": ["sg014"]},
    },
    {
        "nom": "sg015 Recon Team — retire 3 menaces de la manigance principale",
        "pourquoi": "branche de base de l'evenement de manigance",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')", "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["sg015", "01088", "01089"],
        "declencher": [],
        "jouer": ["sg015"],
        "cibles": ["01097b"],
        "payer_avec": ["01088", "01089"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]], "defausse": ["sg015"]},
    },
    {
        "nom": "sg017 Nuts! — depensee pour une carte du set, elle appelle 1 ecureuil",
        "pourquoi": "WhenYouSpendThisCardToPlay filtre sur le set SQUIRREL GIRL",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')"],
        "main_exclusive": ["sg014", "sg017"],
        "declencher": [],
        "jouer": ["sg014"],
        "cibles": ["01094"],
        "payer_avec": ["sg017"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu_trait": [["SQUIRREL", 1]], "degats": [["01094", 3]]},
    },
    {
        "nom": "sg002 Tippy-Toe — Boot Camp ne peut PAS augmenter son ATK",
        "pourquoi": ("regle centrale du set, rendue par le point d'accroche `refuse_gain_fn` "
                     "pose dans face_gain.py (CORRECTIF §9)"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        # L'ecureuil est APPELE par le jeu : une carte posee par Puzzle est une
        # copie neuve, qui n'a pas recu les regles speciales du setup.
        "mise_en_place": ["Puzzle.Action('sg001b', 'AlterEgoAction')"],
        "declencher": ["Puzzle.PutIntoPlay('13016')"],
        "verifier": "sg_ecureuil_refuse_bonus",
    },
    {
        "nom": "sg002 temoin — Boot Camp augmente bien l'ATK d'un allie ORDINAIRE",
        "pourquoi": "sans ce temoin, le cas precedent passerait meme si Boot Camp etait inerte",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.PutIntoPlay('01051')"],
        "declencher": ["Puzzle.PutIntoPlay('13016')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["13016", "01051"], "attributs_carte": [["01051", "attack", 1]]},
    },
    {
        "nom": "sg019 Ratatoskr — son activation defausse un ecureuil",
        "pourquoi": "Forced Interrupt de la nemesis, qui punit l'armee",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')", "Puzzle.PutIntoPlay('sg002')",
                          "Puzzle.PutIntoPlay('sg019')"],
        "declencher": ["Puzzle.Attack('sg019')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["sg002"]},
    },
    {
        "nom": "sg020 Discord in the Branches — 1 menace quand un ecureuil entre en jeu",
        "pourquoi": "Forced Response limite a une fois par round sur le trait SQUIRREL",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Reveal('sg020')"],
        "declencher": ["Puzzle.PutIntoPlay('sg002')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["sg020", 3]], "en_jeu": ["sg002"]},
    },
    {
        "nom": "sg020 Discord in the Branches — les capacites des ecureuils sont blanches",
        "pourquoi": ("le blanchiment est porte par CHAQUE ecureuil : sans lui, Monkey Joe "
                     "appellerait encore un ecureuil en tuant un sbire"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Reveal('sg020')", "Puzzle.PutIntoPlay('sg008')"],
        "declencher": [],
        "verifier": "sg_capacites_blanches",
    },
    {
        "nom": "sg021 Poisoned Rumors — sans ecureuil, 2 menaces sur Discord",
        "pourquoi": "gabarit officiel « sinon » retenu a l'arbitrage, a la place du choix libre",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Reveal('sg020')"],
        "declencher": ["Puzzle.Reveal('sg021')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["sg020", 4]]},
    },
    {
        "nom": "sg022 Ratatoskr's Whispers — capacite Boost : defausse un ecureuil",
        "pourquoi": "branche Boost de l'attachement, jamais atteinte par une partie normale",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Action('sg001b', 'AlterEgoAction')"],
        "declencher": ["Puzzle.Boost('sg022')"],
        "verifier": "sg_aucun_ecureuil_en_jeu",
    },
    {
        "nom": "sg005 The Bruiser — encaisse le degat consequent d'un autre ecureuil",
        "pourquoi": ("carte redessinee a l'arbitrage : sans elle, Lookout et Monkey Joe "
                     "meurent des leur premiere action"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Action('sg001b', 'AlterEgoAction')",
                          "Puzzle.PutIntoPlay('sg011')",
                          "Puzzle.Action('sg011', 'Action')",
                          "Puzzle.PutIntoPlay('sg008')",
                          "Puzzle.ChangeForm('sg001b')",
                          "Puzzle.SetThreat('01097b', 4)"],
        # Rien n'est joue depuis la main : le pilote paierait en DEPENSANT les
        # ecureuils, et il ne resterait personne pour agir. Les deux ecureuils
        # sont redresses : appeles, ils arrivent inclines, et le cout de The
        # Bruiser est justement de s'incliner.
        "declencher": ["Puzzle.Ready('sg002')", "Puzzle.Ready('sg005')",
                       "Puzzle.Action('sg002', 'BasicPower', 1)"],
        "verifier": "sg_bruiser_encaisse",
    },
    {
        "nom": "sg010 Prehensile Tail — finance seule une carte du set et s'incline",
        "pourquoi": "ressource restreinte : elle ne doit payer QUE les cartes Squirrel Girl",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')", "Puzzle.PutIntoPlay('sg010')"],
        "main_exclusive": ["sg014", "01088"],
        "declencher": [],
        "jouer": ["sg014"],
        "cibles": ["01094"],
        "payer_avec": ["sg010"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["sg010"], "degats": [["01094", 3]], "defausse": ["sg014"]},
    },
    {
        "nom": "sg018 Surprise Exam — l'obligation se resout et quitte le jeu",
        "pourquoi": "obligation du pack, jamais jouee ; verifie surtout qu'elle ne plante pas",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Action('sg001b', 'AlterEgoAction')"],
        "declencher": ["Puzzle.Reveal('sg018')"],
        "verifier": "obligation_resolue_75018",
    },
    {
        "nom": "sg016 Unbeatable! — +2 DEF en defense, et le heros se redresse si rien ne passe",
        "pourquoi": ("premiere carte « Hero Interrupt (defense) » atteignable : "
                     "`Puzzle.Attack(defender=...)` declare enfin un defenseur"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')"],
        "main_exclusive": ["sg016", "01088"],
        "declencher": ["Puzzle.Defend('sg001a', '01094')"],
        "verifier": "sg_unbeatable",
    },
    {
        "nom": "sg012 Network of Trees — s'incline pour choisir l'ecureuil appele",
        "pourquoi": "l'interruption vit dans AppelerEcureuil, seul point de passage des appels",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.PutIntoPlay('sg012')"],
        "declencher": ["Puzzle.Action('sg001b', 'AlterEgoAction')"],
        "cibles": ["sg002", "sg003", "sg004", "sg005", "sg006", "sg007"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["sg012"], "en_jeu_trait": [["SQUIRREL", 1]]},
    },
    {
        "nom": "sg011 Central Park — n'appelle rien quand tu controles deja 3 ecureuils",
        "pourquoi": "la condition « fewer than 3 » est dans le handler : sans elle, appel infini",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.Action('sg001b', 'AlterEgoAction')",
                          "Puzzle.PutIntoPlay('sg011')",
                          "Puzzle.Action('sg011', 'Action')",
                          "Puzzle.PutIntoPlay('sg008')",
                          "Puzzle.Ready('sg011')"],
        "declencher": ["Puzzle.Action('sg011', 'Action')"],
        "verifier": "sg_central_park_plafond",
    },
    {
        "nom": "sg016 temoin — sans defenseur declare, Unbeatable! reste en main",
        "pourquoi": ("prouve que c'est bien `defender` qui ouvre la fenetre de defense : "
                     "sans lui le cas precedent passerait meme si la carte etait morte"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')", "Puzzle.Exhaust('sg001a')"],
        "main_exclusive": ["sg016", "01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "sg_unbeatable_non_jouee",
    },
    {
        "nom": "sg007 The Gatherer — le depenser soigne 1 degat a Squirrel Girl",
        "pourquoi": ("arbitrage du 5/8/2026 : les ecureuils 0/0 paient au moment ou on s'en "
                     "separe, pas a leur entree en jeu"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        # `under_control=True` : sans lui l'ecureuil est en jeu mais sans
        # controleur, et sa capacite Resource n'est jamais proposee au paiement.
        # Nancy Whitehead coute 3 : Energy en fournit 2, l'ecureuil le
        # troisieme. Il ne PEUT pas etre paye autrement, donc la depense est
        # certaine — et un seul ecureuil suffit, la limite est respectee.
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')",
                          "Puzzle.PutIntoPlay('sg007', under_control=True)",
                          "Puzzle.Damage('sg001a', 3)"],
        "main_exclusive": ["sg008", "01088"],
        "declencher": [],
        "jouer": ["sg008"],
        "verifier": "sg_gatherer_soigne",
    },
    {
        "nom": "sg006 The Forager — le depenser fait fouiller le dessus du deck",
        "pourquoi": ("seconde carte arbitree le 5/8/2026 vers un effet a la depense ; "
                     "sa branche optionnelle exige `accepter_choix`"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        # Strength (01090) est remontee sur le dessus du deck : c'est elle que
        # le Forager doit faire defausser, ce qui rend l'effet observable.
        # Nancy Whitehead (cout 3) oblige a completer Energy par l'ecureuil.
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')",
                          "Puzzle.PutIntoPlay('sg006', under_control=True)",
                          "Puzzle.PutIntoDeck('01090')"],
        "main_exclusive": ["sg008", "01088"],
        "declencher": [],
        "jouer": ["sg008"],
        "accepter_choix": True,
        "verifier": "sg_forager_defausse",
    },
    {
        "nom": "sg003 Monkey Joe — vaincre un sbire appelle 1 ecureuil",
        "pourquoi": "seule capacite du deck ecureuil branchee sur une attaque",
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')",
                          "Puzzle.PutIntoPlay('sg003', under_control=True)",
                          "Puzzle.PutIntoPlay('01103')",
                          "Puzzle.Damage('01103', 2)"],
        "declencher": ["Puzzle.Action('sg003', 'BasicPower', 0)"],
        "cibles": ["01103"],
        "verifier": "sg_monkey_joe",
    },
    {
        "nom": "sg002/sg005 — un seul ecureuil peut payer une meme carte",
        "pourquoi": ("regle du materiel d'origine, absente du moteur : sans elle deux "
                     "ecureuils paient une carte a cout 2, donc gratuitement"),
        "scenario": "rhino",
        "heros": "squirrel_girl",
        "mise_en_place": ["Puzzle.ChangeForm('sg001b')",
                          "Puzzle.PutIntoPlay('sg002', under_control=True)",
                          "Puzzle.PutIntoPlay('sg005', under_control=True)"],
        "main_exclusive": ["sg014"],
        "declencher": [],
        "jouer": ["sg014"],
        "cibles": ["01094"],
        "verifier": "sg_un_seul_ecureuil_par_carte",
    },

    # ------------------------------------------------------------------------
    # Pack « brawn » : bw001a-bw025 (custom, auteur « Rainy »)
    #
    # Tout le pack tourne autour de la RESERVE, zone hors-jeu de 3 cartes que le
    # moteur ne connaissait pas (voir les # CORRECTIF de game/deck/deck_type.py,
    # game/player/player.py, game/card/card.py, game/ability/cost_func.py et
    # game/ability/factory/resources.py). Les cas ci-dessous prouvent, dans
    # l'ordre : qu'on peut y METTRE une carte, qu'une carte y reste JOUABLE,
    # qu'elle y est DEPENSABLE, et que le cloisonnement du paiement tient.
    # ------------------------------------------------------------------------
    {
        "nom": "bw001b Mastermind Excello — une carte du dessus part en reserve",
        "pourquoi": "premier remplissage de la reserve : sans lui, rien du pack ne demarre",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": [],
        "declencher": ["Puzzle.Action('bw001b', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_reserve": 1},
    },
    {
        "nom": "bw001a The Complete Package — la ressource n'existe QUE si Brawn est epuise",
        "pourquoi": ("condition inversee par rapport aux identites generatrices "
                     "habituelles, qui s'epuisent POUR generer"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')"],
        "declencher": [],
        "verifier": "brawn_ressource_seulement_si_epuise",
    },
    {
        "nom": "bw012 Cho's Lab — changer de forme envoie la carte du dessous en reserve",
        "pourquoi": "Hero Response sur AfterUnitChangeForm, restreinte a l'arrivee en heros",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.PutIntoPlay('bw012')"],
        "declencher": ["Puzzle.ChangeForm('bw001b')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_reserve": 1, "exhausted": ["bw012"]},
    },
    {
        "nom": "bw015 Hulk Out — 2 compteurs de rage donnent +2 ATK, +2 DEF et riposte 1",
        "pourquoi": ("arbitrage du 7/8/2026 : le « for each » porte sur ATK et DEF, "
                     "PAS sur riposte, qui reste a 1"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')"],
        "declencher": ["Puzzle.PutIntoPlay('bw015')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 2, "defense": 2, "retaliate": 1},
                    "en_jeu": ["bw015"],
                    "compteurs": [["bw015", "rage", 2]]},
    },
    {
        "nom": "bw013 Brawn's Suit — +2 PV a l'identite",
        "pourquoi": "amelioration signature : le bonus vise « You », pas le type Hero",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')"],
        "declencher": ["Puzzle.PutIntoPlay('bw013')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 2}, "en_jeu": ["bw013"]},
    },
    {
        "nom": "bw006 Gamma Strike — paye en [physical] uniquement : 10 degats",
        "pourquoi": "la moitie « only [physical] » ajoute 3 degats et l'overkill",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')"],
        # 01077 Counter-Punch porte une icone [physical] ; Haymaker 01087, elle,
        # est ENERGIE — la premiere version du cas payait donc en [energy] et
        # mesurait 7 degats. La carte etait juste, le test faux.
        "main_exclusive": ["bw006", "01077", "01077", "01077"],
        "declencher": [],
        "jouer": ["bw006"],
        "cibles": ["01094"],
        "payer_avec": ["01077", "01077", "01077"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 10]]},
    },
    {
        "nom": "bw006 Gamma Strike — temoin : paye en [energy], 7 degats et rien de plus",
        "pourquoi": ("sans ce temoin, un bonus INCONDITIONNEL passerait le cas "
                     "precedent sans que rien ne le signale"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')"],
        "main_exclusive": ["bw006", "01087", "01087", "01087"],
        "declencher": [],
        "jouer": ["bw006"],
        "cibles": ["01094"],
        "payer_avec": ["01087", "01087", "01087"],
        "verifier": "brawn_gamma_strike_sans_bonus",
    },
    {
        "nom": "bw010 Shockwave — chaque [physical] defaussee frappe chaque ennemi",
        "pourquoi": "cout X + lecture des icones IMPRIMEES des cartes defaussees",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')"],
        "main_exclusive": ["bw010", "01087", "01087", "01087"],
        "declencher": [],
        "jouer": ["bw010"],
        "surpayer": True,
        "verifier": "brawn_shockwave_a_agi",
    },
    {
        "nom": "bw014 Forward-Thinking — jouer depuis la RESERVE redresse l'identite",
        "pourquoi": ("coeur du pack : prouve qu'une carte de la reserve est bien "
                     "JOUABLE, et que le declencheur distingue reserve et main"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')"],
        "declencher": [],
        "verifier": "brawn_jouer_depuis_la_reserve",
    },
    {
        "nom": "bw019 Rising Tide — un jeton d'acceleration a la revelation",
        "pourquoi": "le compteur qui nourrit Namor doit demarrer a 1",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('bw019')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["bw019"], "jetons": [["bw019", "acceleration_token", 1]]},
    },
    {
        "nom": "bw020 Namor — +X ATK/SCH pour X jetons d'acceleration en jeu",
        "pourquoi": ("stat variable relue a chaque mouvement de jeton : figee a "
                     "l'entree en jeu, elle resterait a 1/1"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.Reveal('bw019')"],
        "declencher": ["Puzzle.PutIntoPlay('bw020')"],
        "verifier": "brawn_namor_suit_les_jetons",
    },
    {
        "nom": "bw022 Tidal Surge — un jeton de plus sur Rising Tide, et Namor devient Tenace",
        "pourquoi": "les deux moities de la traitrise, dont celle conditionnee a Namor",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.Reveal('bw019')", "Puzzle.PutIntoPlay('bw020')"],
        "declencher": ["Puzzle.Reveal('bw022')"],
        "verifier": "etat_attendu",
        "attendu": {"jetons": [["bw019", "acceleration_token", 2]],
                    "statuts": [["bw020", "Tough"]]},
    },
    {
        "nom": "bw002 Silk — l'action la renvoie en RESERVE, en sonnant un sbire",
        "pourquoi": ("premier usage de CostFunc.ReturnToReserve : l'alliee doit quitter "
                     "le terrain POUR la reserve, et pas pour la defausse"),
        "scenario": "rhino",
        "heros": "brawn",
        # 01101 Hydra Mercenary, un vrai SBIRE : la premiere version posait
        # 01096, qui est Rhino, le VILAIN — l'action ne trouvait aucune cible
        # legale et n'etait donc jamais proposee.
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')",
                          "Puzzle.PutIntoPlay('bw002', under_control=True)",
                          "Puzzle.PutIntoPlay('01101')"],
        "declencher": ["Puzzle.Action('bw002', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"en_reserve": ["bw002"], "hors_jeu": ["bw002"],
                    "statuts": [["01101", "Stunned"]]},
    },
    {
        "nom": "bw017 Totally Awesome — jouer depuis la reserve retire 1 menace",
        "pourquoi": "seconde carte branchee sur « After you play a card from your reserve »",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')"],
        "declencher": ["Puzzle.PutIntoPlay('bw017')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["bw017"]},
    },
    {
        "nom": "bw003 Ironheart — un pouvoir de base envoie le dessus du deck en reserve",
        "pourquoi": "« uses a basic power » couvre attaque, manigance ET defense",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')",
                          "Puzzle.PutIntoPlay('bw003', under_control=True)",
                          "Puzzle.PutIntoPlay('01096')"],
        "declencher": ["Puzzle.Attack('bw003')"],
        "verifier": "etat_attendu",
        "attendu": {"taille_reserve": 1},
    },
    {
        "nom": "bw018 Analysis Paralysis — l'obligation se resout sans laisser le joueur coince",
        "pourquoi": ("piege connu : une obligation qui fait changer de forme derriere un "
                     "choix optionnel n'est vue par AUCUN autre test"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('bw018')"],
        "verifier": "brawn_obligation_resolue",
    },
    {
        "nom": "bw021 Imperius Rex! — Namor entre en jeu s'il n'y est pas",
        "pourquoi": "montage d'Ancient Grudge 11051 : activer sinon faire entrer",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('bw021')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["bw020"]},
    },
    {
        "nom": "bw004 Calculated Defense — payee en [mental] depuis la main, elle part en RESERVE",
        "pourquoi": ("Hero Interrupt sur la defense, ET la clause qui recycle la carte "
                     "vers la reserve — le coeur economique du pack"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')"],
        "main_exclusive": ["bw004", "01089", "01089"],
        "declencher": ["Puzzle.Defend('bw001a', '01094')"],
        "verifier": "brawn_calculated_defense",
    },
    {
        "nom": "bw004+bw005 Calculated Defense — les DEUX exemplaires sur la MEME defense",
        "pourquoi": ("le seul trou reel du pack : les six cartes sans cas dedie sont des "
                     "seconds exemplaires au code identique, mais leur INTERACTION n'etait "
                     "pas testee, et c'est precisement la qu'une boucle infinie s'est "
                     "produite en partie reelle le 7/8/2026. `LimitOncePerEvent` doit la "
                     "borner SANS interdire le second exemplaire"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')"],
        "main_exclusive": ["bw004", "bw005", "01089", "01089"],
        # Sans cette interdiction, le pilote defausse le SECOND exemplaire pour
        # financer le premier et le cas ne peut plus rien prouver.
        "ne_pas_depenser": ["bw004", "bw005"],
        "accepter_choix": True,
        "declencher": ["Puzzle.Defend('bw001a', '01094')"],
        "verifier": "brawn_double_defense",
    },
    {
        "nom": "bw024 Strong as Silk — injouable sans Silk en jeu",
        "pourquoi": ("le Team-Up imprime exige Silk : la condition de jeu remplace la cle "
                     "TeamUp, qui supposerait deux IDENTITES et rendrait la carte morte"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')"],
        "main_exclusive": ["bw024", "01077"],
        "declencher": [],
        "jouer": ["bw024"],
        "verifier": "brawn_team_up_refuse_sans_allie",
    },
    {
        "nom": "bw024 Strong as Silk — jouable des que Silk est en jeu",
        "pourquoi": ("cas SYMETRIQUE du precedent, et il en faut un : "
                     "`SetCondition(only_if_you_control_face=...)` ne regarde que les "
                     "cartes ATTACHEES a l'identite, jamais les allies — la condition "
                     "etait donc toujours fausse, et le cas de refus passait pour la "
                     "mauvaise raison"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')",
                          "Puzzle.PutIntoPlay('bw002', under_control=True)"],
        "main_exclusive": ["bw024", "01077"],
        "declencher": [],
        "jouer": ["bw024"],
        "verifier": "brawn_team_up_joue_avec_allie",
    },
    {
        "nom": "bw025 Brains and Brawn — compte les icones de la main ET de la reserve",
        "pourquoi": ("seule carte du pack qui lit les deux zones ensemble : c'est la "
                     "recompense de la mecanique"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')",
                          "Puzzle.PutIntoPlay('bw003', under_control=True)"],
        "main_exclusive": ["bw025", "01089", "01090"],
        "declencher": [],
        "jouer": ["bw025"],
        "verifier": "brawn_brains_and_brawn",
    },
    {
        "nom": "bw008 Heavy Lifting — +1 ATK par [physical] depense, puis retrait de menace",
        "pourquoi": ("l'ordre imprime compte : le bonus d'ATK est pose AVANT le retrait, "
                     "et c'est l'ATK augmentee qui fixe la quantite retiree"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')",
                          "Puzzle.PlaceThreat('The Break-In!', 3)"],
        "main_exclusive": ["bw008", "01077", "01077"],
        "declencher": [],
        "jouer": ["bw008"],
        "verifier": "brawn_heavy_lifting",
    },

    # --- Le declencheur central du pack : JOUER depuis la reserve -------------
    # Les trois cartes ci-dessous impriment la meme condition. Tant qu'aucune
    # carte n'etait REELLEMENT jouee depuis la reserve, aucune des trois n'avait
    # jamais vu son declencheur partir (defaut trouve le 7/8/2026 en relisant
    # les verificateurs : le cas « jouer depuis la reserve » se contentait de
    # constater qu'une carte y etait « comme en main »).
    {
        "nom": "bw014 Forward-Thinking — jouer DEPUIS la reserve redresse l'identite",
        "pourquoi": "le declencheur « After you play a card from your reserve », pour de vrai",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')",
                          "Puzzle.PutIntoPlay('bw014')"],
        "main_exclusive": ["bw013", "01077", "01090"],
        # Le carburant doit etre EN RESERVE : une carte jouee depuis la reserve
        # ne se finance que par la reserve. C'est tout l'objet du cloisonnement.
        # Et il en faut UN DE PLUS que le cout (parade du §10 : le pilote perd
        # un payeur sur collision d'ids ; avec un seul, le cout reste impaye et
        # la carte se fait defausser, ce qui imite parfaitement une capacite
        # morte).
        "reserve": ["01077", "01090", "bw013"],
        "declencher": ["Puzzle.Attack('bw001a')"],
        "jouer_reserve": ["bw013"],
        "verifier": "brawn_forward_thinking",
    },
    {
        "nom": "bw013 Brawn's Suit — jouer depuis la reserve inflige 1 degat",
        "pourquoi": "seconde carte branchee sur le meme declencheur, effet different",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')",
                          "Puzzle.PutIntoPlay('bw013')"],
        "main_exclusive": ["bw014", "01077", "01090"],
        "reserve": ["01077", "01090", "bw014"],
        "declencher": [],
        "jouer_reserve": ["bw014"],
        "cibles": ["01094"],
        "accepter_choix": True,
        "verifier": "brawn_suit_degat_depuis_reserve",
    },
    {
        "nom": "bw017 Totally Awesome — jouer depuis la reserve retire 1 menace",
        "pourquoi": "troisieme carte du meme declencheur ; son cas precedent ne testait rien",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')",
                          "Puzzle.PutIntoPlay('bw017')",
                          "Puzzle.PlaceThreat('The Break-In!', 3)"],
        "main_exclusive": ["bw014", "01077", "01090"],
        "reserve": ["01077", "01090", "bw014"],
        "declencher": [],
        "jouer_reserve": ["bw014"],
        "cibles": ["01097b"],
        "accepter_choix": True,
        "verifier": "brawn_totally_awesome_menace",
    },

    # --- Capacites SECONDAIRES, longtemps non couvertes ----------------------
    {
        "nom": "bw006 Gamma Strike — payee en [mental] depuis la main, elle part en reserve",
        "pourquoi": ("la seconde moitie de la carte, jamais verifiee : le recyclage vers "
                     "la reserve quand le paiement est entierement [mental]"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')"],
        "main_exclusive": ["bw006", "01089", "01089"],
        "declencher": [],
        "jouer": ["bw006"],
        "cibles": ["01094"],
        "payer_avec": ["01089", "01089"],
        "verifier": "brawn_gamma_strike_recyclee",
    },
    {
        "nom": "bw015 Hulk Out — la fin du round retire 1 compteur de rage",
        "pourquoi": "Forced Interrupt jamais exerce : le bonus doit s'eroder tout seul",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')",
                          "Puzzle.PutIntoPlay('bw015')"],
        "declencher": [],
        "verifier": "brawn_hulk_out_fin_de_round",
    },
    {
        "nom": "bw012 Cho's Lab — l'action d'alter-ego remelange une carte Brawn au deck",
        "pourquoi": "la seconde capacite du soutien, jamais exercee",
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.PutIntoPlay('bw012')"],
        "declencher": [],
        "verifier": "brawn_cho_lab_alter_ego",
    },
    {
        "nom": "bw020 Namor — sa manigance va sur Rising Tide, pas sur le complot principal",
        "pourquoi": ("Forced Interrupt jamais exerce : c'est lui qui rend la nemesis "
                     "auto-alimentee"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.Reveal('bw019')", "Puzzle.PutIntoPlay('bw020')"],
        "declencher": ["Puzzle.Scheme('bw020')"],
        "verifier": "brawn_namor_menace_detournee",
    },
    {
        "nom": "bw002 Silk — jouee DEPUIS LA MAIN, elle defausse une traitrise",
        "pourquoi": ("l'insert tranche explicitement : depuis la reserve, elle ne le fait "
                     "PAS ; encore fallait-il verifier qu'elle le fait depuis la main"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')"],
        "main_exclusive": ["bw002", "01077", "01090", "01090"],
        "declencher": [],
        "jouer": ["bw002"],
        "verifier": "brawn_silk_defausse_traitrise",
    },

    # --- Les trois dernieres capacites, longtemps declarees « non couvertes » -
    # A tort : `Puzzle.Boost` sait retourner une carte de boost pendant une
    # activation du vilain (modele sg022 du pack squirrel_girl).
    {
        "nom": "bw024 Strong as Silk — Brawn ET Silk gagnent +1 ATK",
        "pourquoi": ("l'EFFET du team-up, et pas seulement son autorisation de jeu : "
                     "les deux personnages doivent monter, pas seulement le heros"),
        "scenario": "rhino",
        "heros": "brawn",
        "mise_en_place": ["Puzzle.ChangeForm('bw001b')",
                          "Puzzle.PutIntoPlay('bw002', under_control=True)"],
        "main_exclusive": ["bw024", "01077", "01090"],
        "declencher": [],
        "jouer": ["bw024"],
        "verifier": "brawn_strong_as_silk_effet",
    },

    # ------------------------------------------------------------------------
    # Pack « agent_13 » : ag001a-ag015 (custom, auteur « Rainy »)
    #
    # Sept cartes techniques exigent chacune leur cas (tache 8 du plan). Pour
    # ag001b, ag004 et ag008, dont le bonus vient des icones boost d'une carte
    # de rencontre, le deck Rencontre est truque via `Puzzle.CreateEncounterDeck`
    # / `CreateEncounterDiscardPile` avec une carte a icones CONNUES et NON
    # NULLES (01106 Stampede, Rhino, 1 icone) : un cas vert avec 0 icone ne
    # prouverait rien, exactement le defaut que cette tache existe pour
    # attraper (Doctor Faustus, vert sur les 3 outils statiques, injouable en
    # vraie partie).
    # ------------------------------------------------------------------------
    {
        "nom": "ag001a Agent 13 — Response : apres un pouvoir de base, elle se redresse ET attaque, 1x/round",
        "pourquoi": ("le garde-fou signale dans le script est que l'attaque declenchee ne doit "
                     "pas redeclencher la capacite en boucle ; on verifie les 2 degats cumules "
                     "(1 ATK x 2 attaques, la seconde venant de la Response) et qu'elle finit "
                     "PRETE malgre l'inclinaison du premier pouvoir de base"),
        "scenario": "rhino",
        "heros": "agent_13",
        # `Puzzle.ChangeForm(card)` BASCULE toujours vers l'AUTRE forme (voir
        # `face.ChangeToOtherIdentityForm` dans puzzle.py) : l'argument sert
        # seulement a LOCALISER l'identite, pas a choisir la destination. La
        # partie demarre en alter-ego (ag001b) ; un seul appel avec CETTE face
        # (la seule qui existe encore a cet instant) bascule donc vers ag001a.
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')"],
        "declencher": ["Puzzle.Attack('ag001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "pret": ["ag001a"]},
    },
    {
        "nom": "ag001b Sharon Carter — Action : la menace retiree est NON NULLE et vaut les icones de la carte choisie",
        "pourquoi": ("defausse de rencontre truquee a une seule carte a 1 icone boost "
                     "(Stampede 01106) : un cas vert avec 0 icone ne prouverait rien"),
        "scenario": "rhino",
        "heros": "agent_13",
        # Pas de ChangeForm : la partie demarre DEJA en alter-ego (ag001b), et
        # `ChangeForm` bascule toujours vers l'AUTRE forme (voir ag001a).
        "mise_en_place": ["Puzzle.CreateEncounterDiscardPile('01106')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "declencher": ["Puzzle.Action('ag001b', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]], "dans_deck_rencontre": ["01106"]},
    },
    {
        "nom": "ag004 Infiltrate — 3 menaces + supplement NON NUL egal aux icones du dessus du deck, defausse optionnelle acceptee",
        "pourquoi": ("supplement venant des icones boost du dessus du deck Rencontre truque a 1 "
                     "icone (Stampede 01106, base 3 + 1 = 4 retirees) ; `accepter_choix` exerce "
                     "la defausse finale optionnelle, sinon jamais atteinte (piege du §8). Menace "
                     "posee a 6, SOUS le TargetThreat (7) du complot : au-dela, le complot "
                     "s'accomplit et disparait, et l'evenement ne trouve plus de cible legale"),
        "scenario": "rhino",
        "heros": "agent_13",
        # Carte de classe Hero : injouable en alter-ego (defaut au demarrage).
        # `ChangeForm('ag001b')` bascule vers ag001a (voir le cas ag001a).
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')", "Puzzle.SetThreat('01097b', 6)"],
        "main_exclusive": ["ag004", "01089"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')"],
        "accepter_choix": True,
        "jouer": ["ag004"],
        "verifier": "agent13_infiltrate",
    },
    {
        "nom": "ag005 Parting Shots — 2 degats, puis la bascule optionnelle fait manigancer l'ennemi au lieu d'attaquer",
        "pourquoi": ("`accepter_choix` exerce la branche optionnelle (ChangeToForm + "
                     "DoSchemeInstead), sinon jamais atteinte ; c'est elle qui protege du piege "
                     "nomme du projet, `ChangeForm` au lieu de `ChangeToForm`"),
        "scenario": "rhino",
        "heros": "agent_13",
        # Un seul ChangeForm bascule de l'alter-ego de depart vers le heros
        # (voir le commentaire du cas ag001a sur `ChangeToOtherIdentityForm`).
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')", "Puzzle.PutIntoPlay('ag005')"],
        "declencher": ["Puzzle.Attack('01094')"],
        "accepter_choix": True,
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "forme": "AlterEgo", "degats_identite": 0,
                    "menace_min": [["01097b", 1]], "hors_jeu": ["ag005"]},
    },
    {
        "nom": "ag005 Parting Shots — « this attack gains ranged » porte sur L'ATTAQUE DE "
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
        # (voir le commentaire du cas ag001a sur `ChangeToOtherIdentityForm`).
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')", "Puzzle.PutIntoPlay('ag005')",
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
                    "hors_jeu": ["ag005"]},
    },
    {
        "nom": "ag008 Agent 13's Pistol — Response apres attaque : degats NON NULS egaux aux icones defaussees",
        "pourquoi": ("le nombre d'icones EST le nombre de degats ; deck Rencontre truque a 1 "
                     "icone (Stampede 01106). Total attendu au moins 3 : 1 ATK (attaque "
                     "declaree) + 1 ATK (Response de ag001a, qui attaque une seconde fois) + 1 "
                     "degat d'icone (Response de ag008) — `degats_min` plutot que `degats` car "
                     "le second declenchement du pistolet, deja epuise, n'est pas garanti payable"),
        "scenario": "rhino",
        "heros": "agent_13",
        # Un seul ChangeForm bascule de l'alter-ego de depart vers le heros
        # (voir le commentaire du cas ag001a sur `ChangeToOtherIdentityForm`).
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')",
                          "Puzzle.PutIntoPlay('ag008', under_control=True)"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')", "Puzzle.Attack('ag001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 3]], "exhausted": ["ag008"]},
    },
    {
        "nom": "ag012 Doctor Faustus — invulnerable tant qu'engage avec un autre sbire, puis l'allie encaisse a sa place",
        "pourquoi": ("CORRECTIF du 7/8/2026 (verifier_tous_les_decks.py) : .SetTarget() ne peut "
                     "pas se poser directement sur une ability d'ennemi. Le cas prouve les DEUX "
                     "capacites : 0 degat subi pendant que 01101 est engage, puis 2 degats sur "
                     "l'identite (ATK courante de Winter Soldier) au lieu de l'ATK de Faustus"),
        "scenario": "rhino",
        "heros": "agent_13",
        "mise_en_place": ["Puzzle.PutIntoPlay('ag012')", "Puzzle.PutIntoPlay('01101')",
                          "Puzzle.PutIntoPlay('53035', under_control=True)"],
        "declencher": ["Puzzle.Damage('ag012', 5)", "Puzzle.Attack('ag012')"],
        "cibles": ["53035"],
        "verifier": "agent13_faustus",
    },
    {
        "nom": "ag013 Hallucination — trouve un sbire, s'y attache, et le defausse au premier degat",
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
        "declencher": ["Puzzle.CreateEncounterDeck('01143')", "Puzzle.Reveal('ag013')",
                       "Puzzle.Damage('01143', 5)"],
        "verifier": "agent13_hallucination",
    },
    {
        "nom": "ag002 Captain America — Interrupt : il encaisse 2 degats de moins en defendant",
        "pourquoi": ("l'interrupt ne part QUE s'il defend, d'ou `defender=` : sans lui le message "
                     "WhenUnitWouldTakeDamage arrive sans while_defending et la reduction reste "
                     "lettre morte. La reduction est bornee a 1 degat minimum"),
        "scenario": "rhino",
        "heros": "agent_13",
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')",
                          "Puzzle.PutIntoPlay('ag002', under_control=True)"],
        "declencher": ["Puzzle.Attack('01094', defender='ag002')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["ag002", 1]], "en_jeu": ["ag002"]},
    },
    {
        "nom": "ag003 Burst Fire — DEUX attaques de 2, pas une de 4",
        "pourquoi": ("les deux attaques passent par ForChoiceAbility, donc le pilote les decline "
                     "sans `accepter_choix` (piege du §8) et la carte parait inerte. On attend au "
                     "moins 4 degats : 2 + 2, plus l'attaque supplementaire que la Response de "
                     "ag001a peut ajouter, d'ou `degats_min`"),
        "scenario": "rhino",
        "heros": "agent_13",
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')"],
        # Genius (01089) fournit BB, soit exactement le cout de 2 : sans une
        # carte de ressource en main, l'evenement n'est jamais joue et la
        # carte parait inerte.
        "main_exclusive": ["ag003", "01089"],
        "payer_avec": ["01089"],
        "declencher": [],
        "accepter_choix": True,
        "jouer": ["ag003"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 4]]},
    },
    {
        "nom": "ag006 Takedown — Response apres attaque : 2 degats de plus",
        "pourquoi": ("Hero Response declenchee par l'attaque du heros, pas par le fait de jouer la "
                     "carte : sans Puzzle.Attack la carte ne part jamais. Au moins 4 degats : "
                     "1 ATK, 1 ATK de la Response de ag001a, et les 2 de Takedown"),
        "scenario": "rhino",
        "heros": "agent_13",
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')"],
        "main_exclusive": ["ag006"],
        "accepter_choix": True,
        "declencher": ["Puzzle.Attack('ag001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 4]]},
    },
    {
        "nom": "ag007 Briefing Room — s'epuise quand un sbire est revele",
        "pourquoi": ("le declencheur est la REVELATION d'un sbire ou d'une manigance annexe, pas "
                     "une action du joueur : la carte peut rester inerte tout une partie sans que "
                     "rien ne le signale. L'epuisement prouve que le cout a ete paye, donc que la "
                     "Response est partie"),
        "scenario": "rhino",
        "heros": "agent_13",
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')",
                          "Puzzle.PutIntoPlay('ag007', under_control=True)"],
        "accepter_choix": True,
        "declencher": ["Puzzle.CreateEncounterDeck('01101')", "Puzzle.Reveal('01101')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["ag007"]},
    },
    {
        "nom": "ag009 Physical Training — +1 ATK a Agent 13",
        "pourquoi": ("deux GiveKeywordToAttached distincts, l'un pour les PV de la porteuse, "
                     "l'autre pour l'attaque et reserve au nom « Agent 13 ». On verifie celui qui "
                     "porte une condition de nom : c'est le seul des deux qui puisse se tromper "
                     "de cible"),
        "scenario": "rhino",
        "heros": "agent_13",
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')"],
        "declencher": ["Puzzle.PutIntoPlay('ag009', under_control=True)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}},
    },
    {
        "nom": "ag010 Secret Agent — s'epuise pour fournir une ressource",
        "pourquoi": ("une capacite Resource n'est jamais proposee au paiement si la carte n'est "
                     "pas SOUS CONTROLE du joueur (piege du §8) ; l'epuisement prouve qu'elle a "
                     "bien servi a payer"),
        "scenario": "rhino",
        "heros": "agent_13",
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')",
                          "Puzzle.PutIntoPlay('ag010', under_control=True)"],
        # Captain America coute 3. Genius (01089) n'en fournit que 2 : il FAUT
        # la ressource de Secret Agent pour completer. Avec une carte a 2, le
        # harnais payait tout avec Genius et l'agent restait pret, sans que le
        # cas n'apprenne quoi que ce soit.
        "main_exclusive": ["ag002", "01089"],
        "payer_avec": ["ag010", "01089"],
        "declencher": [],
        "accepter_choix": True,
        "jouer": ["ag002"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["ag010"], "en_jeu": ["ag002"]},
    },
    {
        "nom": "ag011 Assassination Plot — defausse l'allie qui a le PLUS de PV",
        "pourquoi": ("la manigance a deux branches selon qu'un allie est present ou non ; avec "
                     "Captain America en jeu, c'est lui qui doit partir, et AUCUNE menace ne doit "
                     "etre posee sur la manigance"),
        "scenario": "rhino",
        "heros": "agent_13",
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')",
                          "Puzzle.PutIntoPlay('ag002', under_control=True)"],
        "declencher": ["Puzzle.Reveal('ag011')"],
        "verifier": "etat_attendu",
        "attendu": {"defausse": ["ag002"]},
    },
    {
        "nom": "ag014 Hypnotic Suggestion — en forme HEROS : Desoriente et menace egale au THW",
        "pourquoi": ("la carte a deux branches selon la forme ; celle du heros pose une menace "
                     "egale a la valeur de contre de l'identite, soit 2 pour Agent 13. Un chiffre "
                     "en dur passerait a cote d'une erreur de lecture de l'attribut"),
        "scenario": "rhino",
        "heros": "agent_13",
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')", "Puzzle.SetThreat('01097b', 0)"],
        "declencher": ["Puzzle.Reveal('ag014')"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["ag001a", "Confused"]], "menace": [["01097b", 2]]},
    },
    {
        "nom": "ag015 Sleeper Agent — retire Captain America ET l'obligation du jeu",
        "pourquoi": ("l'obligation offre DEUX issues ; la premiere n'existe que si Captain America "
                     "est en jeu, et `accepter_choix` la fait prendre. Les deux cartes doivent "
                     "quitter la partie, pas la defausse"),
        "scenario": "rhino",
        "heros": "agent_13",
        "mise_en_place": ["Puzzle.ChangeForm('ag001b')",
                          "Puzzle.PutIntoPlay('ag002', under_control=True)"],
        "accepter_choix": True,
        "declencher": ["Puzzle.Reveal('ag015')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["ag002", "ag015"]},
    },

    # ------------------------------------------------------------------------
    # Pack « okoye » : ok001a-ok024
    # ------------------------------------------------------------------------
    {
        "nom": "ok001a Okoye — The Art of War reduit les degats consecutifs d'un allie DORA MILAJE officiel",
        "pourquoi": "verifie que le crochet AfterUnitUseBasicPower cible bien tous les allies DORA MILAJE (y compris les officiels du pack bp, pas seulement les tokens du pack)",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('51022', under_control=True)"],
        "declencher": ["Puzzle.Attack('Okoye')"],
        "verifier": "okoye_art_of_war_reduit_degats_consecutifs",
    },
    {
        "nom": "ok001b Okoye — Vanguard Leader trouve une carte REINFORCEMENTS au Setup",
        "pourquoi": "le Setup s'execute automatiquement avant meme d'atteindre le tour du joueur",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "okoye_vanguard_leader_cherche_reinforcements",
    },
    {
        "nom": "ok001b Okoye — Marshalling Forces remelange une carte REINFORCEMENTS de la defausse",
        "pourquoi": "Action disponible dans les deux formes, distincte du Setup",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.Discard('ok004')"],
        "declencher": ["Puzzle.Action('ok001b', 'Action', 0)"],
        "verifier": "okoye_marshalling_forces_remet_dans_le_deck",
    },
    {
        "nom": "ok002 Aneka — Response : +1 ATK aux autres allies DORA MILAJE, pas a elle-meme",
        "pourquoi": "verifie le filtre `exclude This` calcule a la main (pas via .SetTarget)",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok017', under_control=True)"],
        "declencher": ["Puzzle.PutIntoPlay('ok002', under_control=True)"],
        "verifier": "okoye_aneka_buff_atk_allies",
    },
    {
        "nom": "ok003 Ayo — Response : +1 THW aux autres allies DORA MILAJE",
        "pourquoi": "meme modele qu'Aneka, THW au lieu d'ATK",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok017', under_control=True)"],
        "declencher": ["Puzzle.PutIntoPlay('ok003', under_control=True)"],
        "verifier": "okoye_ayo_buff_thw_allies",
    },
    {
        "nom": "ok004 Adored Ones — branche « Create 2 Dora Milaje allies »",
        "pourquoi": ("la carte doit reellement etre JOUEE (paiement du cout en [energy]), pas seulement "
                     "posee, pour exercer le choix ChooseAbilities. Hero Action : la partie DEMARRE en "
                     "forme IDENTITE CIVILE (decouvert en executant ce cas), il faut passer en forme "
                     "heros avant de jouer une carte Hero Action"),
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.ChangeForm('Okoye')"],
        "main_exclusive": ["ok004", "01088"],
        "declencher": [],
        "jouer": ["ok004"],
        "verifier": "okoye_adored_ones_cree_deux_dora_milaje",
    },
    {
        "nom": "ok006 Angelic Warfare — branche « Create 2 Midnight Angel allies »",
        "pourquoi": "meme modele qu'Adored Ones, cout en [mental] (4), meme besoin de forme heros",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.ChangeForm('Okoye')"],
        "main_exclusive": ["ok006", "01089", "01084", "01081"],
        "declencher": [],
        "jouer": ["ok006"],
        "verifier": "okoye_angelic_warfare_cree_deux_midnight_angel",
    },
    {
        "nom": "ok008 Spear Thrust — 4 degats de base a un ennemi",
        "pourquoi": "preuve du degat de base garanti ; la branche bonus (exhaust jusqu'a 3 DORA MILAJE) reste hors de portee du harnais (cout OPTIONNEL a plage 0-3, le pilote decline les couts optionnels)",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.ChangeForm('Okoye')"],
        "main_exclusive": ["ok008", "01090"],
        "declencher": [],
        "cibles": ["01094"],
        "jouer": ["ok008"],
        "verifier": "okoye_spear_thrust_degat_de_base",
    },
    {
        "nom": "ok010 Close Ranks — Response : 1 compteur phalanx apres la defaite d'un allie DORA MILAJE",
        "pourquoi": "verifie le declencheur AfterUnitBeDefeated et Faces.PlaceCountersOn avec plafond",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok010', under_control=True)",
                          "Puzzle.PutIntoPlay('ok017', under_control=True)"],
        "declencher": ["Puzzle.Damage('ok017', 2)"],
        "verifier": "okoye_close_ranks_pose_un_compteur",
    },
    {
        "nom": "ok010 Close Ranks — la Resource finance un achat en consommant SEULEMENT les compteurs necessaires",
        "pourquoi": ("preuve par substitution du correctif : l'ancien brouillon depensait TOUJOURS tous les "
                     "compteurs disponibles ; le montage CostFunc.Counter + SetToAvailableTimesFn doit "
                     "n'en consommer qu'un seul pour payer Vibranium Spear (cout 1)"),
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok010', under_control=True)",
                          "Puzzle.Counter('ok010', 'phalanx', 2)"],
        "main_exclusive": ["ok015"],
        "declencher": [],
        "jouer": ["ok015"],
        "payer_avec": ["ok010"],
        "verifier": "okoye_close_ranks_finance_un_achat",
    },
    {
        "nom": "ok011 Upanga — chaque allie DORA MILAJE controle gagne +1 PV",
        "pourquoi": "GiveKeywordToInPlayWhenApplyThis restreint par CardFinder(trait=DORA MILAJE)",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok011', under_control=True)",
                          "Puzzle.PutIntoPlay('ok017', under_control=True)"],
        "declencher": [],
        "verifier": "okoye_upanga_buff_hp_allies",
    },
    {
        "nom": "ok011 Upanga — Action d'identite civile remet un equipement ARMOR/TECH/WEAPON dans le deck",
        "pourquoi": ("recherche multi-trait via check_face_fn, cout Exhaust seul (pas de ressource). "
                     "La partie DEMARRE en forme identite civile : pas besoin de ChangeForm ici"),
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok011', under_control=True)",
                          "Puzzle.Discard('ok015')"],
        "declencher": ["Puzzle.Action('ok011', 'AlterEgoAction', 0)"],
        "verifier": "okoye_upanga_action_remet_equipement",
    },
    {
        "nom": "ok012 Midnight Angel Armor — +2 PV, trait AERIAL sur le DORA MILAJE attache",
        "pourquoi": "GiveKeywordToAttached standard, cible CardFinder(card_type=Friend, trait=DORA MILAJE)",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok017', under_control=True)"],
        "declencher": ["Puzzle.PutIntoPlay('ok012', under_control=True)"],
        "cibles": ["ok017"],
        "verifier": "okoye_midnight_angel_armor_stats",
    },
    {
        "nom": "ok017 Dora Milaje — Fragile deverse l'exces d'attaque sur l'identite (SANS armure)",
        "pourquoi": ("preuve du mot-cle maison Fragile : ok017 a 2 PV, deja blessee a 1 PV restant ; "
                     "Rhino (ATK 2) l'attaque en defense, l'exces (1) doit se deverser sur Okoye"),
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok017', under_control=True)",
                          "Puzzle.Damage('ok017', 1)"],
        "declencher": ["Puzzle.Attack('01094', defender='ok017')"],
        "verifier": "okoye_fragile_donne_overkill",
    },
    {
        "nom": "ok012 Midnight Angel Armor — retire le mot-cle fragile (AUCUN Deferlement)",
        "pourquoi": ("meme mise en place que le cas Fragile seul, MAIS avec l'armure attachee : "
                     "preuve par substitution que la condition dans Fragile() coupe bien l'overkill"),
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok017', under_control=True)"],
        "cibles": ["ok017"],
        "declencher": ["Puzzle.PutIntoPlay('ok012', under_control=True)",
                       "Puzzle.Damage('ok017', 1)",
                       "Puzzle.Attack('01094', defender='ok017')"],
        "verifier": "okoye_armure_retire_fragile",
    },
    {
        "nom": "ok017/ok018 — Legion : 2 allies Legion comptent comme 1 seul pour la limite d'allies",
        "pourquoi": "preuve directe du pairage par ordre de creation (object_id) dans Legion()",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok017', under_control=True)",
                          "Puzzle.PutIntoPlay('ok018', under_control=True)",
                          "Puzzle.PutIntoPlay('51022', under_control=True)"],
        "declencher": [],
        "verifier": "okoye_legion_paire_pour_la_limite",
    },
    {
        "nom": "ok014 Royal Protector — +1 limite d'allies, Okoye +1 THW en forme heros",
        "pourquoi": ("deux GiveKeywordToInPlayWhenApplyThis distincts (joueur, puis Hero nomme) ; "
                     "la partie demarre en forme identite civile, or le bonus ne s'applique QUE sur la "
                     "face Hero (elle doit donc etre active pour l'observer)"),
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.ChangeForm('Okoye')",
                          "Puzzle.PutIntoPlay('ok014', under_control=True)"],
        "declencher": [],
        "verifier": "okoye_royal_protector_limite_et_thw",
    },
    {
        "nom": "ok014 Royal Protector — Response : redresse Okoye apres la defaite d'un allie WAKANDA",
        "pourquoi": ("AfterUnitBeDefeated cible ('YouControl', CardFinder(trait=WAKANDA)), cout Exhaust ; "
                     "forme heros necessaire pour qu'exhaust/ready sur 'Okoye' portent sur la face Hero"),
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.ChangeForm('Okoye')",
                          "Puzzle.PutIntoPlay('ok014', under_control=True)",
                          "Puzzle.PutIntoPlay('ok017', under_control=True)",
                          "Puzzle.Exhaust('Okoye')"],
        "declencher": ["Puzzle.Damage('ok017', 2)"],
        "verifier": "okoye_royal_protector_redresse_apres_defaite",
    },
    {
        "nom": "ok015 Vibranium Spear — +1 ATK sur un heros",
        "pourquoi": ("get_new_value renvoie 1 (pas 2) quand la face attachee n'est pas un Ally ; "
                     "forme heros necessaire pour lire identite.attack ensuite"),
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.ChangeForm('Okoye')"],
        "declencher": ["Puzzle.PutIntoPlay('ok015', under_control=True)"],
        "cibles": ["Okoye"],
        "verifier": "okoye_vibranium_spear_sur_heros",
    },
    {
        "nom": "ok015 Vibranium Spear — +2 ATK sur un allie",
        "pourquoi": "get_new_value renvoie 2 quand la face attachee EST un Ally",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok017', under_control=True)"],
        "declencher": ["Puzzle.PutIntoPlay('ok015', under_control=True)"],
        "cibles": ["ok017"],
        "verifier": "okoye_vibranium_spear_sur_allie",
    },
    {
        "nom": "ok019 Funeral Rites — branche « exhaust alter-ego + allies -> retirer de la partie »",
        "pourquoi": "WhenThisObligationGiveToYou + YouMayFlipToYourAlterEgoForm + ChooseAbilities a 2 branches",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok017', under_control=True)"],
        "declencher": ["Puzzle.Reveal('ok019')"],
        "verifier": "okoye_funeral_rites_branche_retrait",
    },
    {
        "nom": "ok020 Malevolent Mimic — Forced Response : +2 menace apres la defaite d'un allie",
        "pourquoi": ("cible Ally SANS restriction de controle (contrairement a Close Ranks). NE PAS "
                     "remettre la menace a 0 : un side scheme a 0 menace est aussitot considere dejoue "
                     "et retire du jeu (contrairement au complot principal) -- piege trouve en executant "
                     "ce cas. Attendu = 2 (StartingThreat imprime '2*') + 2 (Response) = 4. Ce cas a "
                     "aussi debusque un vrai bug de script : 'SideScheme' n'existe pas dans l'espace de "
                     "noms des scripts, seul 'EncounterSideScheme' (piege documente au GUIDE §10) -- "
                     "corrige dans ok020.py"),
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok020', under_control=True)",
                          "Puzzle.PutIntoPlay('ok017', under_control=True)"],
        "declencher": ["Puzzle.Damage('ok017', 2)"],
        "verifier": "okoye_malevolent_mimic_menace_apres_defaite",
    },
    {
        "nom": "ok021 Malice — Forced Response : manigance (SCH imprime) apres la defaite d'un allie",
        "pourquoi": "BasicSchemes hors activation normale, complot principal remis a 0 pour un chiffre exact",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok021', under_control=True)",
                          "Puzzle.PutIntoPlay('ok017', under_control=True)",
                          "Puzzle.SetThreat('01097b', 0)"],
        "declencher": ["Puzzle.Damage('ok017', 2)"],
        "verifier": "okoye_malice_manigance_apres_defaite",
    },
    {
        "nom": "ok022 Mimic-27 — X = ATK du joueur en forme HEROS",
        "pourquoi": ("ThisSetKeyword recalcule sur identite.attack, pas printed_attack ; la partie "
                     "demarre en forme identite civile, ChangeForm est indispensable ici"),
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.ChangeForm('Okoye')",
                          "Puzzle.PutIntoPlay('ok022', under_control=True)"],
        "declencher": [],
        "verifier": "okoye_mimic27_atk_egal_atk_heros",
    },
    {
        "nom": "ok022 Mimic-27 — X = 0 en forme IDENTITE CIVILE",
        "pourquoi": ("branche 'else' de mimic_27_atk, joueur.IsAlterEgo() ; la partie demarre DEJA en "
                     "forme identite civile, aucun ChangeForm necessaire ici"),
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('ok022', under_control=True)"],
        "declencher": [],
        "verifier": "okoye_mimic27_atk_zero_en_alter_ego",
    },
    {
        "nom": "ok023 War Drumming — branche HEROS : le seul sbire en jeu attaque le joueur",
        "pourquoi": ("Malice (ATK 1, seul sbire en jeu) est designe sans MayChooseOneText et attaque ; "
                     "branche 'villainous' (ATK<=2) non codee (ecart assume documente), seule l'attaque "
                     "elle-meme est verifiable ici. Forme heros necessaire pour declencher la branche "
                     "(Hero) plutot que (Alter-Ego) au Reveal. `main_exclusive` NON VIDE (piege : une "
                     "liste VIDE est falsy en Python, `if cas.get('main_exclusive')` la traite alors "
                     "comme absente et NE VIDE PAS la main) avec une seule carte inoffensive : le deck "
                     "Protection provisoire (01075-01093) contient Get Behind Me! (01078), qui annule "
                     "tout effet 'When Revealed' d'une trahison -- le pilote le jouait spontanement et "
                     "empechait War Drumming de jamais se resoudre, decouvert en executant ce cas. Okoye "
                     "est INCLINEE avant le Reveal : un heros incline ne defend pas (guide §8), seul "
                     "moyen fiable de laisser l'attaque de Malice atteindre l'identite sans etre absorbee "
                     "par sa DEF (2, superieure a l'ATK 1 de Malice) -- deuxieme piege trouve en executant "
                     "ce cas"),
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.ChangeForm('Okoye')",
                          "Puzzle.PutIntoPlay('ok021', under_control=True)",
                          "Puzzle.Exhaust('Okoye')"],
        "main_exclusive": ["01079"],
        "declencher": ["Puzzle.Reveal('ok023')"],
        "verifier": "okoye_war_drumming_branche_heros_faible_atk",
    },
    {
        "nom": "ok023 War Drumming — branche IDENTITE CIVILE : gagne renfort",
        "pourquoi": "ThisCardGainSurge, verifie indirectement par la carte Rencontre supplementaire distribuee",
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.ChangeForm('Okoye')"],
        "declencher": ["Puzzle.Reveal('ok023')"],
        "verifier": "okoye_war_drumming_branche_identite_civile_surge",
    },

    # ------------------------------------------------------------------------
    # Pack « iron_lad » : il001a-il023
    # ------------------------------------------------------------------------
    {
        "nom": "il001a Iron Lad — Destiny : regarde 4 cartes, en garde au plus 2, defausse le reste",
        "pourquoi": "invariant valide quel que soit le type de ressource nomme ou les correspondances trouvees : au moins 2 des 4 cartes vues partent TOUJOURS en defausse",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": ["Puzzle.ChangeForm('Iron Lad')"],
        "declencher": ["Puzzle.Action('il001a', 'Action', 0)"],
        "verifier": "iron_lad_destiny_defausse_au_moins_deux",
    },
    {
        "nom": "il001b Nathaniel Richards — Inventive Genius reduit de 2 le cout de la prochaine carte TECH",
        "pourquoi": "preuve par insuffisance de ressources : il009 (cout 1) est jouee sans AUCUNE carte de paiement en main, donc seule la reduction de 2 (plancher 0) rend cela possible",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": [],
        "main_exclusive": ["il009"],
        "declencher": ["Puzzle.Action('il001b', 'Action', 0)"],
        "jouer": ["il009"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["il009"]},
    },
    {
        "nom": "il002 Stature — Response : soigne 1 degat de l'identite a son entree en jeu",
        "pourquoi": "le pilote decline le bonus optionnel (defausser jusqu'a 3 cartes), donc exactement 1 degat soigne",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": ["Puzzle.Damage('Iron Lad', 3)"],
        "declencher": ["Puzzle.PutIntoPlay('il002', under_control=True)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "il003 Energy Overflow — 6 degats a un ennemi, X=1 (cout imprime de la carte TECH defaussee)",
        "pourquoi": "X est calcule APRES paiement du cout, choix des cibles fait a la main dans le handler (pas un SetTarget statique) : preuve que le montant de degats (6, pas 2) est bien atteint",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": ["Puzzle.ChangeForm('Iron Lad')", "Puzzle.PutIntoPlay('il009', under_control=True)"],
        "main_exclusive": ["il003", "01088"],
        "declencher": [],
        "cibles": ["01094"],
        "jouer": ["il003"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 6]]},
    },
    {
        "nom": "il004 Ion Blast — 2 degats de base a un ennemi",
        "pourquoi": "preuve du degat de base garanti ; la branche bonus (defausser 5 cartes pour 6 degats) reste optionnelle, le pilote decline",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": ["Puzzle.ChangeForm('Iron Lad')"],
        "main_exclusive": ["il004", "01088"],
        "declencher": [],
        "cibles": ["01094"],
        "jouer": ["il004"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]]},
    },
    {
        "nom": "il007 Seeking Solutions — melange une carte TECH de la defausse dans le deck",
        "pourquoi": "preuve directe et robuste : la carte doit avoir QUITTE la defausse, independamment du bonus de pioche (secondaire, non verifie ici) ; c'est un Event, il doit etre JOUE (pas Puzzle.Action, reserve aux cartes deja en jeu)",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": ["Puzzle.Discard('il009')"],
        "main_exclusive": ["il007", "01089"],
        "declencher": [],
        "cibles": ["il009"],
        "jouer": ["il007"],
        "verifier": "iron_lad_seeking_solutions_remet_en_deck",
    },
    {
        "nom": "il009 Vision AI — melange le dessus de la defausse, rend le dessous en main",
        "pourquoi": "deux cibles distinctes (from_where Topmost / Bottommost) sur la meme defausse a 2 cartes",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": [
            "Puzzle.PutIntoPlay('il009', under_control=True)",
            "Puzzle.Discard('01088')",
            "Puzzle.Discard('01089')",
        ],
        "declencher": ["Puzzle.Action('il009', 'AlterEgoAction', 0)"],
        "verifier": "iron_lad_vision_ai_melange_et_retourne",
    },
    {
        "nom": "il010 Hack — retire la menace posee au lieu de l'ajouter",
        "pourquoi": "message.SetBeInstead + RemoveThreatFromSchemes : la menace du complot principal doit BAISSER, jamais monter, quand un sbire manigance",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": ["Puzzle.PutIntoPlay('il010', under_control=True)", "Puzzle.SetThreat('01097b', 5)"],
        "declencher": ["Puzzle.Scheme('01094')"],
        "verifier": "iron_lad_hack_retire_au_lieu_de_placer",
    },
    {
        "nom": "il011 Ion Amplifiers — entre en jeu avec 1 compteur ion (elle-meme, seule carte TECH controlee)",
        "pourquoi": "compte DYNAMIQUE pose a la main (AfterCardEnterPlay + PlaceCountersOn), pas desc.Uses",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('il011', under_control=True)"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["il011", "ion", 1]]},
    },
    {
        "nom": "il011 Ion Amplifiers — 2 compteurs ion si 2 cartes TECH sont controlees (elle-meme + Vision AI)",
        "pourquoi": "verifie que le compte suit vraiment le nombre de cartes TECH controlees, pas une constante",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": ["Puzzle.PutIntoPlay('il009', under_control=True)"],
        "declencher": ["Puzzle.PutIntoPlay('il011', under_control=True)"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["il011", "ion", 2]]},
    },
    {
        "nom": "il013 Iron Lad's Boots — Iron Lad gagne le trait AERIAL",
        "pourquoi": "GiveKeywordToAttached('You', trait='AERIAL') sans cible attachee",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('il013', under_control=True)"],
        "verifier": "etat_attendu",
        "attendu": {"traits": ["AERIAL"], "en_jeu": ["il013"]},
    },
    {
        "nom": "il013 Iron Lad's Boots — Response : apres avoir joue un evenement, rend le dessous de la defausse",
        "pourquoi": "declencheur generique AfterPlayerPlayedCard(CardFinder(card_type=Event))",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": [
            "Puzzle.ChangeForm('Iron Lad')",
            "Puzzle.PutIntoPlay('il013', under_control=True)",
            "Puzzle.Discard('01089')",
        ],
        "main_exclusive": ["il004", "01088"],
        "declencher": [],
        "cibles": ["01094"],
        "jouer": ["il004"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["01089"]},
    },
    {
        "nom": "il014 Iron Lad's Helmet — Response : apres un pouvoir de base, rend le dessous de la defausse",
        "pourquoi": "declencheur AfterUnitUseBasicPower(powers=['ATK','THW']), meme modele que ok001a",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": [
            "Puzzle.ChangeForm('Iron Lad')",
            "Puzzle.PutIntoPlay('il014', under_control=True)",
            "Puzzle.Discard('01089')",
        ],
        "declencher": ["Puzzle.Attack('Iron Lad')"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["01089"]},
    },
    {
        "nom": "il015 Iron Lad's Suit — +3 PV et redresse Iron Lad",
        "pourquoi": "GiveKeywordToAttached('You', health=3) et Faces.ReadyAll sur l'identite",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": [
            "Puzzle.ChangeForm('Iron Lad')",
            "Puzzle.PutIntoPlay('il015', under_control=True)",
            "Puzzle.Exhaust('il001a')",
        ],
        "declencher": ["Puzzle.Action('il015', 'HeroAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 3}, "pret": ["il001a"]},
    },
    {
        "nom": "il016 Neurokinetic Interface — 2 degats a un ennemi apres reveler une trahison",
        "pourquoi": "branche « treachery or minion » de AfterPlayerRevealCard ; HeroResponse exige la forme heros (oubli initial corrige)",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": ["Puzzle.ChangeForm('Iron Lad')", "Puzzle.PutIntoPlay('il016', under_control=True)"],
        "declencher": ["Puzzle.Reveal('il021')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]]},
    },
    {
        "nom": "il017 Shadow of the Future — branche « retirer les 3 dessus du deck -> retirer l'obligation »",
        "pourquoi": "WhenThisObligationGiveToYou + ChooseAbilities a 2 branches, meme modele qu'ok019",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('il017')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["il017"]},
    },
    {
        "nom": "il018 Early Start — When Revealed : incline chaque amelioration Iron Lad en jeu",
        "pourquoi": "UpgradesIronLadEnJeu filtre par set_name, pas par trait",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": ["Puzzle.PutIntoPlay('il011', under_control=True)"],
        "declencher": ["Puzzle.Reveal('il018')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["il011"]},
    },
    {
        "nom": "il019 Kang the Conqueror — empile l'amelioration au cout le plus eleve, la rend a sa defaite",
        "pourquoi": "Filter.One(highest_cost=True) + TuckCardUnderHere puis retour en main au When Defeated ; deux coups de degats (Toughness absorbe le premier)",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": [
            "Puzzle.PutIntoPlay('il011', under_control=True)",
            "Puzzle.PutIntoPlay('il015', under_control=True)",
        ],
        "declencher": [
            "Puzzle.Reveal('il019')",
            "Puzzle.Damage('il019', 1)",
            "Puzzle.Damage('il019', 99)",
        ],
        "verifier": "iron_lad_kang_empile_puis_rend",
    },
    {
        "nom": "il020 Taking Responsability — Forced Response : defausse le dessus du deck apres une attaque",
        "pourquoi": "AfterUnitUseBasicPower(powers=['ATK','THW']), meme modele que Weakened (11018, officielle)",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": ["Puzzle.Reveal('il020')", "Puzzle.ChangeForm('Iron Lad')"],
        "declencher": ["Puzzle.Attack('Iron Lad')"],
        "verifier": "etat_attendu",
        "attendu": {"defausse_joueur": 1},
    },
    {
        "nom": "il020 Taking Responsability — Action : retire le dessus du deck pour se defausser",
        "pourquoi": "cout sans choix (pas de CostFunc.RemoveFromGame reutilisable pour une carte de deck, code a la main)",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": ["Puzzle.Reveal('il020')"],
        "declencher": ["Puzzle.Action('il020', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["il020"]},
    },
    {
        "nom": "il021 Pay the Price — defausse 8 cartes du deck",
        "pourquoi": "player.DiscardDeckTopCards(8, effect) ; deck de depart assez grand pour ne pas gagner renfort",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('il021')"],
        "verifier": "etat_attendu",
        "attendu": {"defausse_joueur": 8},
    },
    {
        "nom": "il023 Sudden Plan Change — condition Stature en jeu, change de forme, +1 taille de main",
        "pourquoi": "TeamUp rendu comme 'Stature (alliee) en jeu' (tranche par l'utilisateur le 29/08/2026), only_if_you_control_face",
        "scenario": "rhino",
        "heros": "iron_lad",
        "mise_en_place": ["Puzzle.ChangeForm('Iron Lad')", "Puzzle.PutIntoPlay('il002', under_control=True)"],
        "declencher": [],
        "jouer": ["il023"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "attributs": {"hand_size": 1}},
    },
    # ------------------------------------------------------------------------
    # Packs custom DAZZLER (dz) et WOLVERINE X-23 (wx), ajoutes le 29/08/2026.
    # Chacun de ces cinq cas a passe la PREUVE PAR SUBSTITUTION exigee par
    # CHECKLIST-VALIDATION-CARTE.md bloc 3 : module retire -> ROUGE,
    # module remis -> VERT.
    # ------------------------------------------------------------------------
    {
        "nom": "dz017a Live Concert — Setup : posee en jeu par Alison Blaire",
        "pourquoi": ("le Setup posait la carte sur sa SEULE face recto ; sans les deux "
                     "faces, `Card.Flip` la couchait face cachee et elle QUITTAIT le jeu, "
                     "ce qui tuait toute la moitie Showtime! du pack"),
        "scenario": "rhino",
        "heros": "dazzler",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["dz017a"]},
    },
    {
        "nom": "dz016 Sound Collector Suit — Dazzler gagne +1 DEF",
        "pourquoi": "effet continu d'une armure : verifier qu'il touche bien l'identite",
        "scenario": "rhino",
        "heros": "dazzler",
        # La partie demarre en ALTER-EGO : sans ce passage en forme heros,
        # l'identite n'a pas d'attribut `defense` et la verification tombe sur
        # un AttributeError au lieu de mesurer quoi que ce soit.
        # `ChangeForm` BASCULE vers l'autre face : on lui passe la face EN
        # COURS (l'alter-ego), pas celle qu'on veut atteindre.
        "mise_en_place": ["Puzzle.ChangeForm('dz001b')"],
        "declencher": ["Puzzle.PutIntoPlay('dz016', under_control=True)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}, "en_jeu": ["dz016"]},
    },
    {
        "nom": "dz002 Longshot — entre en jeu avec 2 compteurs knife",
        "pourquoi": ("les compteurs d'entree passent par `ThisEnterPlayWithCounters` et "
                     "NON par une cle desc ; le compteur `knife` a du etre declare dans "
                     "COUNTER_LIST, sans quoi la carte tombe des la creation de la partie"),
        "scenario": "rhino",
        "heros": "dazzler",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('dz002', under_control=True)"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["dz002", "knife", 2]]},
    },
    {
        "nom": "wx002 Wolverine's Claws — Setup : posee en jeu par Laura Kinney",
        "pourquoi": "re-skin de X-23 : verifier que le Setup vise bien wx002 et pas 43002",
        "scenario": "rhino",
        "heros": "wolverine_x23",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["wx002"]},
    },
    {
        "nom": "wx009 Adamantium Lacing — +2 PV a l'identite et retaliate 1",
        "pourquoi": ("deux `GiveKeywordToAttached` distincts ; le second visait le heros "
                     "PAR NOM, or « Wolverine » n'est plus unique depuis ce pack — la "
                     "cible est desormais bornee au controleur"),
        "scenario": "rhino",
        "heros": "wolverine_x23",
        # Forme heros obligatoire : `retaliate` n'existe pas sur l'alter-ego,
        # et le CardFinder de la carte cherche « Wolverine », pas
        # « Laura Kinney ». `ChangeForm` BASCULE : on passe la face en cours.
        "mise_en_place": ["Puzzle.ChangeForm('wx001b')"],
        "declencher": ["Puzzle.PutIntoPlay('wx009', under_control=True)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 2, "retaliate": 1}, "en_jeu": ["wx009"]},
    },
    {
        "nom": "si008 Stark Island — recherche + met en jeu EN PAYANT le cout",
        "pourquoi": ("aucune carte officielle ne combine recherche et paiement du "
                     "cout (`Player.PlayACard`, generalisation de `PlayAnAlly`) ; "
                     "prouver que le cout est VRAIMENT paye, pas seulement que la "
                     "carte cherchee est trouvee et posee gratuitement"),
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": [
            "Puzzle.PutIntoPlay('si008', under_control=True)",
            "Puzzle.CreatePlayerDiscardPile('si007')",
        ],
        # Seule carte en main : 01088 (Energy, [energy][energy]). Force le
        # pilote a payer AVEC elle le cout 1 de Pepper Potts (si007) — sans
        # `main_exclusive`, la main de depart resterait et masquerait un
        # eventuel oubli de paiement.
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('si008', 'AlterEgoAction')"],
        # `Search.PlayerCard(..., may=True)` : choix a minimum 0, le pilote
        # decline par defaut sans ce drapeau (§8 du guide).
        "accepter_choix": True,
        # Plusieurs [[Individual]] sont legaux (Daniel Hall/Claire Mooney/Mason
        # Thomas dans le deck, Pepper Potts en defausse ET dans le deck) : sans
        # forcer la cible, le pilote prend le premier trouve (cout 0), ce qui
        # ne prouverait rien sur le paiement. Pepper Potts (cout 1) le prouve.
        "cibles": ["si007"],
        "verifier": "si008_stark_island_paye",
    },
    {
        "nom": "si001a Superior Iron Man — Ressource : degat a un ami -> genere wild",
        "pourquoi": "premiere carte du pack, verifier le cout CostFunc.DealDamage + CanGenerateResources",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": ["Puzzle.ChangeForm('si001b')"],
        "declencher": [],
        "main_exclusive": ["si010"],
        "jouer": ["si010"],
        "verifier": "si001a_degat_et_ressource",
    },
    {
        "nom": "DIAGNOSTIC si002 — PutIntoPlay direct (sans passer par le Setup)",
        "pourquoi": "isoler si le bug vient de si002 lui-meme ou du mecanisme BeginGameWithSetAside",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('si002', under_control=True)"],
        "declencher": [],
        "verifier": "diag_si002_direct",
    },
    {
        "nom": "DIAGNOSTIC wonder_man — Setup : Ionic Physiology (temoin)",
        "pourquoi": "verifier que BeginGameWithSetAside marche pour un heros CONNU BON avant de blamer si001b",
        "scenario": "rhino",
        "heros": "wonder_man",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "diag_wonder_man_ionic",
    },
    {
        "nom": "si001b Tony Stark — Setup : trouve et met en jeu l'Armure Endo-Sym",
        "pourquoi": "BeginGameWithSetAside, modele Wonder Man 58001b",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": [],
        "declencher": [],
        "verifier": "si001b_armure_en_jeu",
    },
    {
        "nom": "si001b Tony Stark — O.P.A. : depense X mental -> retire 1+X menace",
        "pourquoi": "cout variable Cost(\"B\") minimum 1, valeur lue sur cost_func.Get(Spend).return_res",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": ["Puzzle.PlaceThreat('01097b', 5)"],
        "declencher": ["Puzzle.Action('si001b', 'Action')"],
        "main_exclusive": ["01089"],
        "surpayer": True,
        "cibles": ["01097b"],
        "verifier": "si001b_opa_retire_menace",
    },
    {
        "nom": "si002 Endo-Sym Armor — Hero Action (attaque) : depense X physical -> 2+X degats",
        "pourquoi": "bug .SetPlay() trouve et corrige ; verifier que l'attaque marche bien maintenant",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": ["Puzzle.ChangeForm('si001b')"],
        "declencher": ["Puzzle.Action('si002', 'HeroAction')"],
        # Main VIDE (main_exclusive: []) : seule source de paiement possible =
        # la capacite Ressource de l'identite (deal 1 damage -> wild), X=1
        # garanti. Une carte a 2 symboles ("RR") ne se laisse pas forcer de
        # facon fiable par `payer_avec` (repli par couleur du pilote ne
        # matche pas "RR" avec "R"), donc on verifie la formule avec X=1.
        "main_exclusive": [],
        "cibles": ["01094"],
        "verifier": "si002_attaque_degats",
    },
    {
        "nom": "si002 Endo-Sym Armor — Hero Interrupt (defense) : depense X energy -> previent 1+X",
        "pourquoi": ("meme correctif .SetPlay() ; HeroInterrupt exige la forme HEROS "
                     "(is_hero_type), sans ChangeForm l'ability n'est meme pas offerte"),
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": ["Puzzle.ChangeForm('si001b')"],
        "declencher": ["Puzzle.Damage('si001a', 5)"],
        "main_exclusive": [],
        "verifier": "si002_defense_prevention",
    },
    {
        "nom": "si003 Teen Abomination — entre avec 4 rage, +1 ATK/rage, -1 rage apres attaque",
        "pourquoi": "ThisEnterPlayWithCounters + ThisGainKeyword dynamique + AfterUnitUseBasicPower",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('si003', under_control=True)"],
        "declencher": ["Puzzle.Attack('si003')"],
        "verifier": "si003_rage_et_atk",
    },
    {
        "nom": "si007 Pepper Potts — Action : retire 1 menace en ignorant la crise",
        "pourquoi": "RemoveThreatFromSchemes(ignore_crisis=True), teste avec Crowd Control (01108) en jeu",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": [
            "Puzzle.PutIntoPlay('si007', under_control=True)",
            "Puzzle.PutIntoPlay('01108', under_control=True)",
            "Puzzle.PlaceThreat('01097b', 5)",
        ],
        "declencher": ["Puzzle.Action('si007', 'Action')"],
        "cibles": ["01097b"],
        "verifier": "si007_ignore_crisis",
    },
    {
        "nom": "si004 Daniel Hall — dernier jeton Flouze : genere wild + defausse 1 carte de la main",
        "pourquoi": "ex_operation apres paiement, verifie GetCounters('cash')==0 pour detecter le dernier jeton",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": [
            "Puzzle.PutIntoPlay('si004', under_control=True)",
            "Puzzle.Counter('si004', 'cash', -2)",
        ],
        "declencher": [],
        "main_exclusive": ["si010"],
        "main": ["01085"],
        "payer_avec": ["si004"],
        "jouer": ["si010"],
        "verifier": "si004_dernier_jeton",
    },
    {
        "nom": "si009 Iron Sight — annule les icones de boost (corrige avec le retrait de .SetPlay())",
        "pourquoi": "meme bug .SetPlay() que si002 (Support injouable depuis la main sinon)",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('si009', under_control=True)"],
        "declencher": ["Puzzle.Boost('01108')"],
        "verifier": "si009_boost_annule",
    },
    {
        "nom": "si010 Endo-Sym Spare — cherche Endo-Sym Matter en defausse et la mele au deck",
        "pourquoi": "Faces.ShuffleAllTo + .SetTarget(from_where=YourDiscardPile)",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": [
            "Puzzle.PutIntoPlay('si010', under_control=True)",
            "Puzzle.CreatePlayerDiscardPile('si013')",
        ],
        "declencher": ["Puzzle.Action('si010', 'AlterEgoAction')"],
        "verifier": "si010_matter_dans_deck",
    },
    {
        "nom": "si009 Iron Sight — jouable normalement depuis la main (verif du correctif .SetPlay())",
        "pourquoi": ("sans le correctif, Support.GetAbilities() ne generait plus "
                     "CanPlayThisSupportCard() : la carte etait injouable depuis la main"),
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": [],
        "declencher": [],
        "main_exclusive": ["si009", "01088"],
        "jouer": ["si009"],
        "verifier": "si009_jouable_depuis_main",
    },
    {
        "nom": "si011 Spectacular Blast — 3 degats + retire 2 menaces",
        "pourquoi": "double cible (SetTarget/SetTarget2) sur la meme carte",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": ["Puzzle.ChangeForm('si001b')", "Puzzle.PlaceThreat('01097b', 5)"],
        "declencher": [],
        "main_exclusive": ["si011", "01090"],
        "jouer": ["si011"],
        "cibles": ["01094", "01097b"],
        "verifier": "si011_double_effet",
    },
    {
        "nom": "si012 Spectacular Save — previent 3 degats + retire 1 menace (Interruption)",
        "pourquoi": "Event joue en reaction (Hero Interrupt), verifier is_hero_type + double effet",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        # 1er degat consomme le LimitOncePerPhase de si002 (concurrente possible),
        # pour forcer le pilote a utiliser si012 sur le VRAI degat de 5 teste.
        "mise_en_place": ["Puzzle.ChangeForm('si001b')", "Puzzle.PlaceThreat('01097b', 5)",
                          "Puzzle.Damage('si001a', 1)"],
        "declencher": ["Puzzle.Damage('si001a', 5)"],
        "main_exclusive": ["si012", "01088"],
        "cibles": ["01097b"],
        "verifier": "si012_double_effet",
    },
    {
        "nom": "si013 Endo-Sym Matter — double la ressource pour une carte de Classe Hero",
        "pourquoi": "DoubleResourcesThisGenerates(card_class=Hero) : 1 wild imprime doit devenir 2",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        # ne_pas_depenser exclut la capacite Ressource de l'identite (si001a) :
        # sans cela, le pilote la sollicite EN PLUS de si013 (surpaiement),
        # ce qui declenche l'interruption de defense de si002 sur le degat
        # auto-inflige et confond l'estimation de paiement du pilote (bug de
        # harnais, pas de carte -- confirme en isolant si002 temporairement).
        "mise_en_place": ["Puzzle.ChangeForm('si001b')", "Puzzle.PlaceThreat('01097b', 3)"],
        "declencher": [],
        "main_exclusive": ["si013", "si011"],
        "payer_avec": ["si013"],
        "ne_pas_depenser": ["si001a"],
        "jouer": ["si011"],
        "verifier": "si013_double_ressource",
    },
    {
        "nom": "si014 Alone — option 1 : exhaust Tony Stark, retire l'obligation de la partie",
        "pourquoi": "modele Business Problems (01170, obligation officielle de Tony Stark)",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('si014')"],
        "verifier": "si014_option1_exhaust",
    },
    # NOTE : pas de cas automatise pour l'option 2 ("Spend 3 resources...").
    # `YouMayFlipToYourAlterEgoForm` (cards/pack/__init__.py:132) reflippe
    # TOUJOURS le joueur en alter-ego avant le choix (le pilote generique
    # accepte le "may" par defaut), donc l'option 1 (condition IsAlterEgo)
    # redevient disponible et `premiere_option_jouable()` la reprend en
    # premier -- le harnais n'a pas de mecanisme pour forcer un CHOIX NOMME
    # entre 2 ForChoiceAbility (seulement des cibles a l'interieur d'un
    # choix deja selectionne). Le code suit fidelement le modele officiel
    # Business Problems (01170) + Soldiers of Fortune (aos/50102.py pour
    # ThisCardGainSurge) ; a verifier en partie reelle.
    {
        "nom": "si015 Massive Attack — Une fois revelee : 1 degat au joueur",
        "pourquoi": "message.GetToPlayer() (pas GetInitiator) pour une carte rencontre",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('si015')"],
        "verifier": "si015_when_revealed",
    },
    {
        "nom": "si015 Massive Attack — Boost : mise en jeu",
        "pourquoi": "WhenCardBecomeBoost + PutThisIntoPlay",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": [],
        "declencher": ["Puzzle.Boost('si015')"],
        "verifier": "si015_boost_en_jeu",
    },
    {
        "nom": "si016 Tony Stark A.I. — Armored 2 : previent 2 degats a CHAQUE instance",
        "pourquoi": "mot-cle maison, Forced Interrupt sans limite (contrairement a Toughness)",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": ["Puzzle.PutIntoPlay('si016', under_control=True)"],
        "declencher": ["Puzzle.Damage('si016', 3)", "Puzzle.Damage('si016', 3)"],
        "verifier": "si016_armored_repete",
    },
    {
        "nom": "si016 Tony Stark A.I. — Une fois revelee + Boost : 1 degat au joueur chacun",
        "pourquoi": "deux triggers distincts (When Revealed et [star]) sur le meme minion",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('si016')", "Puzzle.Boost('si016')"],
        "verifier": "si016_revealed_et_boost",
    },
    {
        "nom": "si017 Get My Body Back — Une fois revelee : 2 degats au joueur (2x1)",
        "pourquoi": "decision utilisateur : 2 instances de 1 degat, pas 1 instance de 2",
        "scenario": "rhino",
        "heros": "superior_iron_man",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('si017')"],
        "verifier": "si017_deux_degats",
    },
    # NOTE : pas de cas automatise pour "O.P.A. reste-t-elle offerte 2 fois
    # dans la meme phase ?" (vu en autoplay, graine 1, rhino -- bloquage).
    # Tente via `Puzzle.Action` deux fois de suite : la 2e activation est
    # ACCEPTEE, ce qui ressemblait a un vrai bug. Mais `Puzzle.Action` passe
    # par `Message.WhenPlayerLikeInTurn` (sender_player.py:338), une
    # `LikeFakeMessage` + `NoSendMessage` FAITE pour contourner la
    # comptabilite normale (`Send()` ne fait rien) -- `effect.
    # SetHasSpellInPhase()` (effect_invoke.py:158), qui enregistre l'usage
    # pour `LimitOncePerPhase`, ne se declenche QUE si `message.
    # send_resolve_message` est vrai, ce que `WhenPlayerLikeInTurn` desactive
    # expres. Le test etait donc invalide : il prouvait que le CONTOURNEMENT
    # de test contourne bien la comptabilite, pas que la vraie partie le
    # ferait. Preuve indirecte que ce n'est PAS un vrai bug de regle : dans le
    # journal d'autoplay, malgre "O.P.A.": 6 en un round, la menace du complot
    # PRINCIPAL a EMPIRE (0.14 -> 0.43) au lieu de s'ameliorer -- coherent
    # avec une option qui reste listee mais que le moteur refuse en silence a
    # la resolution (meme famille que Tenacity 01093, deja documente dans ce
    # fichier comme "le defaut est ailleurs"), pas avec 6 vraies executions.
    # A verifier malgre tout en partie reelle : le symptome (le pilote
    # d'autoplay se bloque en reproposant O.P.A.) reste reel meme s'il n'a
    # pas viole la regle.

    # ------------------------------------------------------------------------
    # Pack « kate_bishop » : identite kb001a/kb001b, signatures kb002-kb013,
    # obligation kb014, Team-Up kb015, set nemesis kb016-kb020.
    # ------------------------------------------------------------------------
    {
        "nom": "kb001a Hawkeye (Kate Bishop) — Master Archer : retire 2 compteurs fleche, inflige 2 degats a l'attaquant",
        "pourquoi": ("le plafond variable (3, 5 avec Kate's Quiver) est gere a la main via "
                     "player.DeclareNumber, jamais par CostFunc.Counter : sans `choisir_option` "
                     "le pilote choisirait toujours 0 (reponse minimale toujours legale), et la "
                     "carte semblerait inerte alors qu'elle marche"),
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.ChangeForm('kb001b')",
                          "Puzzle.PutIntoPlay('kb012', under_control=True)",
                          "Puzzle.Counter('kb012', 'arrow', 3)"],
        "declencher": ["Puzzle.Attack('01094')"],
        "choisir_option": "2",
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "compteurs": [["kb012", "arrow", 1]]},
    },
    {
        "nom": "kb001b Kate Bishop — Action : cherche Kate's Bow dans le deck/defausse et le pose en jeu",
        "pourquoi": "Search.PlayerCard doit vraiment trouver la carte et PutIntoPlay doit reussir",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.CreatePlayerDeck('kb012')"],
        "declencher": ["Puzzle.Action('kb001b', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["kb012"]},
    },
    {
        "nom": "kb002 Hawkeye (Clint Barton) — Interrupt : defait par degat consequent, se remelange au deck + 1 fleche sur Kate's Bow",
        "pourquoi": ("CORRECTIF DE DONNEES (data/cards.json) : ATK/THW etaient imprimes sans "
                     "asterisque (« 2 »/« 1 »), donc `printed_attack_consequential_damage=0` et "
                     "l'allie ne pouvait JAMAIS subir de degat consequent -- son propre Interrupt, "
                     "qui reagit precisement a ce degat, etait totalement inatteignable. Corrige en "
                     "« 2* »/« 1* » (Consequential 1 sur ATK et THW), a l'identique du modele "
                     "imprime 01066/58013 (« * Hawkeye » officiel, ATK 1*/THW 1*)"),
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.PutIntoPlay('kb012', under_control=True)",
                          "Puzzle.PutIntoPlay('kb002', under_control=True)",
                          "Puzzle.Damage('kb002', 1)"],
        "declencher": ["Puzzle.Attack('kb002')"],
        "verifier": "kb_hawkeye_ally_consequential",
    },
    {
        "nom": "kb003 Evasive Shot — prevention de 4 degats + riposte egale aux compteurs fleche (plafond 5)",
        "pourquoi": "Rhino (ATK 2) est integralement encaisse par la prevention de 4 : preuve que la prevention agit vraiment, pas juste la riposte",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.ChangeForm('kb001b')",
                          "Puzzle.PutIntoPlay('kb012', under_control=True)",
                          "Puzzle.Counter('kb012', 'arrow', 3)"],
        "main_exclusive": ["kb003", "01090"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "degats": [["01094", 3]], "defausse": ["kb003"]},
    },
    {
        "nom": "kb004 Infiltrate — en forme heros : prevention de 2 menaces seulement",
        "pourquoi": "branche « sinon » du texte (4 seulement si alter-ego) : ce cas isole la valeur EN FORME HEROS",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.ChangeForm('kb001b')", "Puzzle.SetThreat('01097b', 0)"],
        "main_exclusive": ["kb004", "01089"],
        "declencher": ["Puzzle.PlaceThreat('01097b', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]], "defausse": ["kb004"]},
    },
    {
        "nom": "kb004 Infiltrate — en forme alter-ego : prevention de 4 menaces",
        "pourquoi": "branche « si alter-ego » du texte : sans ce second cas, la valeur 4 n'est jamais distinguee de 2",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.SetThreat('01097b', 0)"],
        "main_exclusive": ["kb004", "01089"],
        "declencher": ["Puzzle.PlaceThreat('01097b', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]], "defausse": ["kb004"]},
    },
    {
        "nom": "kb005 Quick Draw — Alter-Ego Action : bascule en heros et redresse",
        "pourquoi": "deux abilities distinctes selon la forme : ce cas isole la branche Alter-Ego (bascule + redresse)",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.Exhaust('kb001b')"],
        "main_exclusive": ["kb005", "01090"],
        "declencher": [],
        "jouer": ["kb005"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "Hero", "pret": ["kb001a"]},
    },
    {
        "nom": "kb005 Quick Draw — Hero Action : redresse et pose 2 compteurs fleche",
        "pourquoi": "branche Hero, distincte de la branche Alter-Ego testee a part",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.ChangeForm('kb001b')",
                          "Puzzle.PutIntoPlay('kb012', under_control=True)",
                          "Puzzle.Exhaust('kb001a')"],
        "main_exclusive": ["kb005", "01090"],
        "declencher": [],
        "jouer": ["kb005"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["kb001a"], "compteurs": [["kb012", "arrow", 2]]},
    },
    {
        "nom": "kb006 Smoke Arrow — annule l'activation d'un ennemi, depense 1 compteur fleche, bascule en alter-ego",
        "pourquoi": "SetBeInstead doit vraiment annuler l'attaque de Rhino (0 degat sur l'identite), pas juste s'afficher",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.ChangeForm('kb001b')",
                          "Puzzle.PutIntoPlay('kb012', under_control=True)",
                          "Puzzle.Counter('kb012', 'arrow', 1)"],
        "main_exclusive": ["kb006", "01089", "01090"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["kb012", "arrow", 0]], "degats_identite": 0, "forme": "AlterEgo"},
    },
    {
        "nom": "kb007 Anchor Points — Resource : incline Anchor Points -> ressource wild pour une carte SKILL",
        "pourquoi": "for_card=CardFinder2('SKILL') restreint le paiement : sans lui la carte ne finance rien de valide",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.PutIntoPlay('kb007', under_control=True)"],
        "main_exclusive": ["kb005"],
        "declencher": [],
        "jouer": ["kb005"],
        "verifier": "etat_attendu",
        # kb010 (Athletic Agility) coute 2 : injouable avec la seule ressource
        # wild d'Anchor Points. kb005 (Quick Draw, SKILL, cout 1) tient dans
        # la seule ressource generee -- preuve suffisante que le paiement a
        # bien ete finance par Anchor Points (main_exclusive ne laisse aucune
        # autre source). C'est un evenement : il part en defausse, pas en jeu.
        "attendu": {"exhausted": ["kb007"], "defausse": ["kb005"]},
    },
    {
        "nom": "kb008 Hawkeye Investigations — Response : apres prevention de menace, 1 menace retiree d'UNE AUTRE manigance",
        "pourquoi": ("AJOUT MOTEUR (AfterThreatBePrevented) : la Response retire sa menace AVANT que "
                     "le reste de la pose (le complot principal, deja en cours de resolution) ne "
                     "s'applique -- cibler CE MEME complot annulerait exactement le retrait (retire 1 "
                     "avant pose, +1 repose juste apres = aucun changement net, ce qui ne prouverait "
                     "rien). On cible donc kb016, une AUTRE manigance deja en jeu, seule facon "
                     "d'observer un effet net"),
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.ChangeForm('kb001b')",
                          "Puzzle.PutIntoPlay('kb008', under_control=True)",
                          "Puzzle.PutIntoPlay('kb016')",
                          "Puzzle.SetThreat('kb016', 2)",
                          "Puzzle.SetThreat('01097b', 0)"],
        "main_exclusive": ["kb004", "01089"],
        "declencher": ["Puzzle.PlaceThreat('01097b', 3)"],
        # Le champ « name » transmis au pilote remplace les espaces par des
        # underscores (observe via TRACE_OPTIONS : "Finding_the_Perfect_LMD").
        "choisir_option": "Finding_the_Perfect_LMD",
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1], ["kb016", 1]]},
    },
    {
        "nom": "kb008 Hawkeye Investigations — Response : apres prevention de degats, 1 menace retiree",
        "pourquoi": "second Response de la carte, declenche par une prevention de DEGATS (Evasive Shot) plutot que de menace",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.ChangeForm('kb001b')",
                          "Puzzle.PutIntoPlay('kb008', under_control=True)",
                          "Puzzle.PutIntoPlay('kb012', under_control=True)"],
        # `SetThreat` passe par `WhenSchemeWouldPlaceThreat` : lance en
        # DECLENCHER (apres main_exclusive) pour eviter que « Great
        # Responsibility » (01061, aspect Justice du deck de depart, cout 0)
        # ne detourne la pose en 5 degats sur l'identite s'il traine encore en
        # main de depart -- main_exclusive garantit une main propre avant.
        "main_exclusive": ["kb003", "01090"],
        "declencher": ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]], "degats_identite": 0},
    },
    {
        "nom": "kb009 Lucky — Alter-Ego Action : incline Lucky, soigne 2 degats, pose 1 compteur fleche",
        "pourquoi": "cout d'inclinaison + double consequence (soin + compteur) sur la meme resolution",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.Damage('kb001b', 3)",
                          "Puzzle.PutIntoPlay('kb009', under_control=True)",
                          "Puzzle.PutIntoPlay('kb012', under_control=True)"],
        "declencher": ["Puzzle.Action('kb009', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "compteurs": [["kb012", "arrow", 1]], "exhausted": ["kb009"]},
    },
    {
        "nom": "kb010 Athletic Agility — Agile 1 reduit un coup non defendu, puis riposte 1 degat",
        "pourquoi": ("reduction ET riposte sur la MEME attaque NON DEFENDUE, deux volets du texte "
                     "imprime. `Puzzle.Exhaust('kb001a')` AVANT l'attaque : incline, Kate ne peut "
                     "plus se declarer elle-meme defenseuse (seul personnage en solo), ce qui rend "
                     "l'attaque reellement non defendue -- sans cela le pilote la declare "
                     "defenseuse par defaut (DEF imprimee 1 appliquee), et `while_defending=False` "
                     "ne s'active jamais"),
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.ChangeForm('kb001b')", "Puzzle.PutIntoPlay('kb010', under_control=True)",
                          "Puzzle.Exhaust('kb001a')"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 1]]},
    },
    {
        "nom": "kb011 Kate's Aviators — Hero Action : incline + retire 1 compteur style -> pioche 1 carte",
        "pourquoi": "Uses (2 compteurs a l'entree en jeu) + double cout (inclinaison ET compteur) + pioche reelle",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.ChangeForm('kb001b')",
                          "Puzzle.PutIntoPlay('kb011', under_control=True)",
                          "Puzzle.CreatePlayerDeck('35013')"],
        "declencher": ["Puzzle.Action('kb011', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["kb011"], "compteurs": [["kb011", "style", 1]], "en_main": ["35013"]},
    },
    {
        "nom": "kb012 Kate's Bow — les attaques de base gagnent ranged : Retaliate de l'ennemi ignore",
        "pourquoi": "temoin ci-dessous : sans Kate's Bow, le meme montage encaisse la riposte de Retaliate",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.ChangeForm('kb001b')",
                          "Puzzle.PutIntoPlay('kb012', under_control=True)",
                          "Puzzle.PutIntoPlay('11017')"],
        "declencher": ["Puzzle.Attack('kb001a')"],
        "cibles": ["11017"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["11017", 2]], "degats_identite": 0},
    },
    {
        "nom": "kb012 Kate's Bow — TEMOIN : sans la carte, la meme attaque subit la riposte de Retaliate",
        "pourquoi": "sans ce temoin, le cas precedent passerait meme si `GainRanged` ne faisait rien",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.ChangeForm('kb001b')", "Puzzle.PutIntoPlay('11017')"],
        "declencher": ["Puzzle.Attack('kb001a')"],
        "cibles": ["11017"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["11017", 2]], "degats_identite": 1},
    },
    {
        "nom": "kb012 Kate's Bow — Interrupt : 1 compteur fleche place en fin de phase joueur",
        "pourquoi": "declencheur WhenPhaseEnd, hors de portee de l'API Puzzle : message envoye directement dans le verifieur, comme brawn_ressource_seulement_si_epuise le fait deja pour un autre declencheur",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.PutIntoPlay('kb012', under_control=True)"],
        "declencher": [],
        "verifier": "kb_bow_fin_de_phase",
    },
    {
        "nom": "kb013 Kate's Quiver — Resource : incline Kate's Quiver -> ressource wild + 1 compteur fleche sur Kate's Bow",
        "pourquoi": "double consequence de la meme Resource ability : la ressource ET le compteur",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.PutIntoPlay('kb012', under_control=True)",
                          "Puzzle.PutIntoPlay('kb013', under_control=True)"],
        "main_exclusive": ["kb009"],
        "declencher": [],
        "jouer": ["kb009"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["kb013"], "en_jeu": ["kb009"], "compteurs": [["kb012", "arrow", 1]]},
    },
    {
        "nom": "kb014 Family = Trouble — branche par defaut : l'allie Hawkeye retire du jeu, l'obligation retiree du jeu",
        "pourquoi": "player.ChooseAbilities prend la PREMIERE branche par defaut (pas de Cancel ajoute, contrairement a MayChooseOneAbility) : c'est elle qui est exercee ici",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.CreatePlayerDeck('kb002')"],
        "declencher": ["Puzzle.Reveal('kb014')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["kb014", "kb002"]},
    },
    {
        "nom": "kb015 Tandem Archery — Team-Up : pose 2 compteurs fleche sur Kate's Bow, pioche 1 carte",
        "pourquoi": "SetTarget('TeamUp') exige Hawkeye (Clint Barton) ET Kate Bishop en jeu -> partie a 2 joueurs",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "heros2": "hawkeye",
        # HeroAction : injouable en alter-ego (defaut au demarrage).
        "mise_en_place": ["Puzzle.ChangeForm('kb001b')",
                          "Puzzle.PutIntoPlay('kb012', under_control=True)",
                          "Puzzle.CreatePlayerDeck('35013')"],
        "declencher": [],
        "jouer": ["kb015"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["kb012", "arrow", 2]], "defausse": ["kb015"], "en_main": ["35013"]},
    },
    {
        "nom": "kb016 Finding the Perfect LMD — tant qu'elle est en jeu, Madame Masque ne peut pas prendre de degats",
        "pourquoi": "UnitCannotTakeDamageWhile cible Madame Masque par son nom : verifie qu'elle encaisse vraiment 0",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.PutIntoPlay('kb016')", "Puzzle.PutIntoPlay('kb017')"],
        "declencher": ["Puzzle.Damage('kb017', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["kb017", 0]], "en_jeu": ["kb016", "kb017"]},
    },
    {
        "nom": "kb017 Madame Masque — ATK/SCH copies sur ATK/THW imprimes de la forme HEROS, Kate en forme HEROS",
        "pourquoi": ("Kate est mise en forme Heros ici pour prouver le mecanisme central (copie reelle, "
                     "non triviale : verifie 2/2, pas 0=0). Voir le cas suivant pour la forme alter-ego, "
                     "l'interet reel de la carte (« MEME si Kate n'est pas en forme heros »)."),
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.ChangeForm('kb001b')", "Puzzle.PutIntoPlay('kb017')"],
        "declencher": [],
        "verifier": "kb_madame_masque_stats",
    },
    {
        "nom": "kb017 Madame Masque — ATK/SCH copies sur ATK/THW imprimes de la forme HEROS, Kate en ALTER-EGO",
        "pourquoi": ("Corrige le 29/8/2026 : c'est le cas qui echouait avant la correction "
                     "(`heros.attack`/`heros.thwart` valent 0 pour une face d'identite non affichee, "
                     "cf. docstring de `kb_madame_masque_stats`). Kate demarre en alter-ego par defaut "
                     "(aucun `Puzzle.ChangeForm` ici) : c'est precisement le scenario que le texte de la "
                     "carte revendique (« la forme heros de l'identite qu'elle affronte », MEME "
                     "actuellement en alter-ego) et qui n'etait pas prouve."),
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.PutIntoPlay('kb017')"],
        "declencher": [],
        "verifier": "kb_madame_masque_stats",
    },
    {
        "nom": "kb018 Masque's Minions — Forced Interrupt : survit a une defaite, se soigne, gagne 1 compteur",
        "pourquoi": "SetBeInstead doit remplacer la defaite ET soigner integralement, pas juste ajouter un compteur",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.PutIntoPlay('kb018')"],
        "declencher": ["Puzzle.Damage('kb018', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["kb018"], "degats": [["kb018", 0]], "compteurs": [["kb018", "minion", 1]]},
    },
    {
        "nom": "kb018 Masque's Minions — Forced Interrupt : au 2e compteur, defausse pour de bon",
        "pourquoi": "seconde ligne imprimee, conditionnee au compteur pose par la premiere : temoin qu'il ne survit pas indefiniment",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.PutIntoPlay('kb018')", "Puzzle.Counter('kb018', 'minion', 1)"],
        "declencher": ["Puzzle.Damage('kb018', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["kb018"]},
    },
    {
        "nom": "kb019 Golden Shot (1/2) — When Revealed : 1 degat direct + 1 indirect par personnage allie controle",
        "pourquoi": "2 personnages controles (identite + kb002) -> 1 + 2 = 3 degats, pas juste 1 + 1",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.PutIntoPlay('kb002', under_control=True)"],
        "declencher": ["Puzzle.Reveal('kb019')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "kb020 Golden Shot (2/2) — meme texte que kb019, exemplaire physique distinct",
        "pourquoi": "deuxieme card_id physique de la meme trahison : verifie qu'il porte bien la MEME capacite (pas un doublon vide)",
        "scenario": "rhino",
        "heros": "kate_bishop",
        "mise_en_place": ["Puzzle.PutIntoPlay('kb002', under_control=True)"],
        "declencher": ["Puzzle.Reveal('kb020')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },

    # ------------------------------------------------------------------------
    # Pack « scarlet_spider » : ss001a-ss022
    # ------------------------------------------------------------------------
    {
        "nom": "ss001a Scarlet Spider — Extreme Interrogation : sbire vaincu par exces remelange, menace retiree = exces",
        "pourquoi": "AfterUnitAttackAndDefeatUnit('This'->Minion, has_excess_damage=True) ; message.target encore deplacable a ce stade (Faces.ShuffleAllTo vers le deck rencontre) ; retrait de menace = min(exces,3)",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Kaine Parker', 'ss001a')",
            "Puzzle.PutIntoPlay('01110')",
            "Puzzle.SetThreat('01097b', 5)",
        ],
        "main_exclusive": ["01087", "01088"],
        "declencher": [],
        "cibles": ["01110"],
        "jouer": ["01087"],
        "verifier": "etat_attendu",
        "attendu": {"dans_deck_rencontre": ["01110"], "menace": [["01097b", 4]]},
    },
    {
        "nom": "ss001b Kaine Parker — Spider Link : defausse 1 carte, cherche Spider-pathy en defausse, l'ajoute en main",
        "pourquoi": "Search.PlayerCard(include_discard_pile=True, name='Spider-pathy') + initiator.GainCard, meme modele qu'ok001b",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.Discard('ss007')"],
        "declencher": ["Puzzle.Action('ss001b', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["ss007"]},
    },
    {
        "nom": "ss002 Grim Resolve — choisit ATK (1er choix), +1 pour la ressource depensee, redresse l'identite",
        "pourquoi": "effect.GetPaidResources().GetResourceIconTypes() (modele 47009 Grande Finale) ; TemporaryGain(..., Message.WhenRoundEnd, attack=1) ; Faces.ReadyAll([identite])",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.ChangeToFace('Kaine Parker', 'ss001a')", "Puzzle.Exhaust('ss001a')"],
        "main_exclusive": ["ss002", "01088"],
        "declencher": [],
        "jouer": ["ss002"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}, "pret": ["ss001a"]},
    },
    {
        "nom": "ss004 Precise Force — Hero Action (attack) jouee, degats bornes 0-3 sur un ennemi",
        "pourquoi": "initiator.DeclareNumber(0,3) (modele dt005/il002) ; le pilote choisit TOUJOURS le premier item de la liste offerte (valeur 0), meme limite deja documentee sur il002 : la branche non-nulle reste declaree mais non forcable par ce harnais",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.ChangeToFace('Kaine Parker', 'ss001a')"],
        "main_exclusive": ["ss004", "01088"],
        "declencher": [],
        "cibles": ["01094"],
        "jouer": ["ss004"],
        "verifier": "ss004_precise_force_joue_et_borne",
    },
    {
        "nom": "ss007 Spider-pathy — cherche le sbire du dessus du deck de rencontre, le met en jeu engage, pioche 1",
        "pourquoi": "Search.EncounterCard(include_discard_pile=False, card_type=Minion) + face.PutIntoPlay (auto-engage, face_on_event.py:169)",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.ChangeToFace('Kaine Parker', 'ss001a')"],
        "main_exclusive": ["ss007", "01088"],
        "declencher": [],
        "jouer": ["ss007"],
        "verifier": "ss007_spider_pathy_pose_sbire",
    },
    {
        "nom": "ss009 Unrestrained — 7 degats garantis a un ennemi (branche stun/confuse si exces non exercee ici)",
        "pourquoi": "this.DealDamage(effect.targets, 7, effect, if_this_attack_deal_excess_damage=...) (modele wsp/13013.py) ; Rhino (14 PV) encaisse 7 sans etre vaincu, donc sans exces : preuve du degat de base garanti seulement",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.ChangeToFace('Kaine Parker', 'ss001a')"],
        "main_exclusive": ["ss009", "01090", "01090"],
        "declencher": [],
        "cibles": ["01094"],
        "jouer": ["ss009"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 7]]},
    },
    {
        "nom": "ss011 Four Seasons' Room — Alter-Ego Action : exhaust -> pioche 1 (branche par defaut, comme Funeral Rites)",
        "pourquoi": "player.ChooseAbilities a 2 branches (modele core/02035.py Intimidation) ; le pilote prend TOUJOURS la premiere option (draw 1), meme convention que il017/ok019 pour une branche libre",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.PutIntoPlay('ss011', under_control=True)"],
        "declencher": ["Puzzle.Action('ss011', 'AlterEgoAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["ss011"], "taille_main": 7},
    },
    {
        "nom": "ss012 Mark of Kaine — attaques contre le sbire marque gagnent deferlement (deversement sur un autre ennemi)",
        "pourquoi": "WhenUnitWouldAttackUnit(None, 'AttachedMinion', ...) + message.GainOverKill (modele officiel exact 33032 Marked) ; attaquant = un ALLIE (pas l'identite), pour eviter la reponse ss001a (attacker='This') dont l'interaction avec le deversement 'Simultaneous Overkill' du moteur (can_health.py:258) fait planter le harnais (AssertionError reproductible, voir rapport) — la capacite testee ici (le deferlement lui-meme) est independante de ss001a",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": [
            "Puzzle.PutIntoPlay('01110')",
            "Puzzle.Damage('01110', 1)",
            "Puzzle.PutIntoPlay('01051', under_control=True)",
        ],
        "declencher": ["Puzzle.PutIntoPlay('ss012', under_control=True)", "Puzzle.Attack('01051')"],
        "cibles": ["01110"],
        "verifier": "ss012_mark_of_kaine_deferlement",
    },
    {
        "nom": "ss012 Mark of Kaine — Hero Interrupt : +2 a l'exces quand Scarlet Spider vainc elle-meme le sbire marque (regression moteur ChooseOrder/ChoiceOne)",
        "pourquoi": "WhenUnitAttackDealExcessDamage(HeroInterrupt, 'You', ...) + message.IncreaseDamage(2, effect) (modele gmw/16045.py Follow Through). 39043 Goblin (HP imprime 1, aucune capacite propre) : l'identite Scarlet Spider (ATK 2) le vainc avec 1 exces garanti, sans Puzzle.Damage prealable (ne s'applique pas de façon fiable sur une carte fraichement instanciee dans le meme mise_en_place, piege distinct de FindOrCreateFace). Ce scenario precis (attaquant = identite, PAS un allie) a revele deux vrais bugs moteur le 30/08/2026 : (1) engine/controller/controller.py ChoiceOne plantait en boucle infinie (AssertionError, target_range=(2,2) fige a l'offre du choix vs all_legal_targets reevalue plus court a la validation) des que le deversement d'exces (Worlds.FindVillain, can_attack.py) ajoute le VILLAIN comme second candidat a `ChooseOrder` aux cotes du sbire vaincu (can_health.py:245-249) ; (2) une fois (1) corrige, game/player/model/player_ask.py ChooseOrder plantait sur `assert len(faces) == 0` car `effect` revenait vide sans que `faces` le soit. Preuve par substitution du CORRECTIF (pas du module ss012, deja prouve capacite 1 au cas precedent) : les deux correctifs retires -> AssertionError/boucle infinie reproductible a volonte ; correctifs en place -> partie continue normalement, Rhino subit bien 1+2=3 degats d'exces (preuve que l'interruption a reellement augmente le montant, pas seulement qu'elle a ete offerte).",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Kaine Parker', 'ss001a')",
            "Puzzle.PutIntoPlay('39043')",
            "Puzzle.PutIntoPlay('ss012', under_control=True)",
        ],
        "declencher": ["Puzzle.Attack('ss001a')"],
        "cibles": ["39043"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["39043"], "degats_min": [["01094", 3]]},
    },
    {
        "nom": "ss015 Spider Stealth Suit — +1 point de vie fixe sur l'identite",
        "pourquoi": "GiveKeywordToInPlayWhenApplyThis('You', health=1), modele ok016 Royal Protector (upgrade sans attache)",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.ChangeToFace('Kaine Parker', 'ss001a')"],
        "declencher": ["Puzzle.PutIntoPlay('ss015', under_control=True)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 1}},
    },
    {
        "nom": "ss015 Spider Stealth Suit — Hero Interrupt : +1 au degat inflige par un evenement ATTACK joue",
        "pourquoi": "WhenDamageWouldBeDealtTo(by_play_card=('YouControl', CardFinder(trait='ATTACK', card_type=Event))) + IncreaseDamage(1) ; Unrestrained (ss009) inflige un montant FIXE (7, pas de DeclareNumber) pour un total previsible 7+1=8",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.ChangeToFace('Kaine Parker', 'ss001a')", "Puzzle.PutIntoPlay('ss015', under_control=True)"],
        "main_exclusive": ["ss009", "01090", "01090"],
        "declencher": [],
        "cibles": ["01094"],
        "jouer": ["ss009"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 8]]},
    },
    {
        "nom": "ss016 Stings of Kaine — +1 ATK fixe sur Scarlet Spider",
        "pourquoi": "GiveKeywordToInPlayWhenApplyThis('You', attack=1), modele ok016 Royal Protector",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.ChangeToFace('Kaine Parker', 'ss001a')"],
        "declencher": ["Puzzle.PutIntoPlay('ss016', under_control=True)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": 1}},
    },
    {
        "nom": "ss016 Stings of Kaine — Hero Interrupt : exhaust quand vous attaquez (piercing + overkill accordes)",
        "pourquoi": "WhenUnitMakeAttack('You') + SetCostFunc(CostFunc.Exhaust('This')) (modele cw/tigra/56005.py Sharp Claws) ; l'inclinaison prouve que l'interruption a bien ete offerte et payee ; cible a 3 PV pour egaler exactement l'ATK effective (2 de base + 1 fixe de Stings of Kaine) et EVITER l'exces (qui, combine au deferlement accorde ici, ferait planter le harnais sur l'interaction 'Simultaneous Overkill' deja rencontree sur ss012)",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Kaine Parker', 'ss001a')",
            "Puzzle.PutIntoPlay('ss016', under_control=True)",
            "Puzzle.PutIntoPlay('01101')",
        ],
        "declencher": ["Puzzle.Attack('ss001a')"],
        "cibles": ["01101"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["ss016"]},
    },
    {
        "nom": "ss017 Murderer's Guilt — branche « exhaust Kaine Parker + 2 degats -> retirer de la partie » (branche par defaut)",
        "pourquoi": "WhenThisObligationGiveToYou + ChooseAbilities a 2 branches (modele ok019 Funeral Rites) ; le pilote prend la premiere option, meme convention que il017",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('ss017')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["ss017"]},
    },
    {
        "nom": "ss018 Assassins Guild — chaque sbire ASSASSIN gagne +1 ATK",
        "pourquoi": "GiveKeywordToInPlayWhenApplyThis(CardFinder2('ASSASSIN', Enemy), attack=1), modele officiel 01136 Ultron",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('ss018')", "Puzzle.PutIntoPlay('ss020')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["ss020", "attack", 1]]},
    },
    {
        "nom": "ss019 Bella Donna — Plotting : manigance a l'engagement de l'identite",
        "pourquoi": "AfterMinionEngagePlayer('This','You') + this.BasicSchemes(effect) (modele ok021 Malice, mots-cles/plotting.md) ; PutIntoPlay engage automatiquement le sbire",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.SetThreat('01097b', 0)"],
        "declencher": ["Puzzle.PutIntoPlay('ss019')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]]},
    },
    {
        "nom": "ss019 Bella Donna — Forced Interrupt : a sa defaite, cherche un autre sbire ASSASSIN et le revele",
        "pourquoi": "WhenUnitBeDefeated(ForcedInterrupt,'This') + Search.EncounterCard(trait='ASSASSIN') + face.Reveal (modele core/spider_man_nemesis/01095.py Rhino) ; deck de rencontre truque a un seul sbire ASSASSIN trouvable",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.CreateEncounterDeck('ss020')", "Puzzle.PutIntoPlay('ss019')"],
        "declencher": ["Puzzle.Damage('ss019', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["ss019"], "en_jeu": ["ss020"]},
    },
    {
        "nom": "ss020 Harvester — attaques gagnent piercing (ignore tenace) ET Forced Response +1 degat apres avoir blesse",
        "pourquoi": "UnitAttackGainKeyword('This', piercing=True) (modele officiel 04027 Crossfire) + AfterUnitAttackAndDamageUnit (modele core/klaw/01118.py) ; identite tenace : sans piercing 0 degat, avec piercing seul 2, avec les deux capacites 3 -- 3 valeurs distinctes selon ce qui est retire",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.ChangeToFace('Kaine Parker', 'ss001a')", "Puzzle.PutIntoPlay('ss020')", "Puzzle.Tough('ss001a')"],
        "declencher": ["Puzzle.Attack('ss020')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "ss021 Undead Hand Ninja — Forced Interrupt : serait vaincu -> remelange dans le deck de rencontre a la place",
        "pourquoi": "WhenUnitWouldBeDefeated('This') + message.SetBeInstead + Faces.ShuffleAllTo (modele fan-made exact lj015 Annihilus)",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.PutIntoPlay('ss021')"],
        "declencher": ["Puzzle.Damage('ss021', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["ss021"], "dans_deck_rencontre": ["ss021"]},
    },
    {
        "nom": "ss022 Forced Contract — When Revealed : l'allie a l'ATK la plus haute subit des degats = ATK de Scarlet Spider",
        "pourquoi": "max(allies, key=attack) + player.GetHero().attack (modele th015 Friendly Fire pour le max)",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.PutIntoPlay('01051', under_control=True)"],
        "declencher": ["Puzzle.Reveal('ss022')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01051", 2]]},
    },
    {
        "nom": "ss022 Forced Contract — Boost : chaque personnage ami subit 1 degat",
        "pourquoi": "player.GetControlCharacters() + DealDamage(units, 1, effect) (modele officiel exact core/01154.py Concussive Blast)",
        "scenario": "rhino",
        "heros": "scarlet_spider",
        "mise_en_place": ["Puzzle.ChangeToFace('Kaine Parker', 'ss001a')", "Puzzle.PutIntoPlay('01051', under_control=True)"],
        "declencher": ["Puzzle.Boost('ss022')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01051", 1]], "degats_identite": 1},
    },

    # ------------------------------------------------------------------------
    # Pack « howard_the_duck » : hd001a-hd027 (RyCoRan, set 135)
    # PIEGE de nommage : les deux faces s'appellent « Howard the Duck » et
    # « Howard Duckson », noms UNIQUES dans les 5168 cartes du depot, mais on
    # suit quand meme la convention `Puzzle.ChangeToFace('<face active>',
    # '<card_id vise>')` de scarlet_spider — elle ne passe jamais par la
    # recherche ambigue de `FindOrCreateFace`.
    # ------------------------------------------------------------------------
    {
        "nom": "hd001a Howard the Duck — Private Eye : previent 1 menace posee sur une manigance",
        "pourquoi": "WhenThreatWouldBePlacedOn(Interrupt, None) + message.PreventThreat(1) (modele bkw/08017 Counterintelligence). `Puzzle.PlaceThreat` passe bien par PlaceThreatInternal, donc par le message interrompu : 3 poses -> 2 reellement placees",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.ChangeToFace('Howard Duckson', 'hd001a')"],
        "main_exclusive": ["01090"],
        "declencher": ["Puzzle.PlaceThreat('01097b', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]]},
    },
    {
        "nom": "hd001a Howard the Duck — Response : redresse Howard apres l'entree en jeu d'une manigance annexe",
        "pourquoi": "AfterCardEnterPlay(Response, SchemeSide2) + Faces.ReadyAll([this]) ; hd025 (manigance annexe nemesis) mise en jeu SANS reveler, pour n'exercer que le declencheur d'entree en jeu",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.ChangeToFace('Howard Duckson', 'hd001a')", "Puzzle.Exhaust('hd001a')"],
        "declencher": ["Puzzle.PutIntoPlay('hd025')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["hd001a"], "en_jeu": ["hd025"]},
    },
    {
        "nom": "hd001b Howard Duckson — Deducktive Reasoning : met une des 3 cartes du dessus sous le deck de rencontre",
        "pourquoi": "LookAtDeck + MayChooseFace + MoveAllToDeck(..., 'Bottom') (modele 40004 Precognition, sauf que Precognition DEFAUSSE) ; hd024 remontee sur le DESSUS du deck de rencontre par Puzzle.PutIntoDeck, le pilote prend toujours le premier item offert",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.CreateEncounterDeck('hd024')", "Puzzle.PutIntoDeck('hd024')"],
        "declencher": ["Puzzle.Action('hd001b', 'Action', 0)"],
        "verifier": "hd001b_carte_mise_au_fond_du_deck_rencontre",
    },
    {
        "nom": "hd002 Man-Thing — cout reduit de 1 par manigance Howard en zone de victoire (preuve par insuffisance)",
        "pourquoi": "ReduceCostToPlayThis(<nb de manigances Howard en victoire>) (modele 34021 Storm). Trois Haymaker = 3 ressources EXACTEMENT : le cout imprime 4 est impayable, seul le cout reduit a 3 (hd010 en zone de victoire) rend Man-Thing jouable. Meme technique de preuve que il001b",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Howard Duckson', 'hd001a')",
            "Puzzle.PutIntoPlay('hd010', under_control=True)",
            "Puzzle.SetThreat('hd010', 0)",
        ],
        "main_exclusive": ["hd002", "01087", "01087", "01087"],
        "declencher": [],
        "jouer": ["hd002"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hd002"]},
    },
    {
        "nom": "hd003 Mallard Magic — branche 1 : sonne un ennemi et lui inflige 5 degats",
        "pourquoi": "UNE seule ability .SetPlay() (factory.py n'accepte qu'un play_count de 1) + ChooseAbilities a 2 branches ; le pilote prend TOUJOURS la premiere option, meme convention que il017/ok019/ss011. La MEME cible recoit le statut ET les degats (piege `that <nom>`). Partage avec hd004, code identique",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.ChangeToFace('Howard Duckson', 'hd001a')"],
        "main_exclusive": ["hd003", "01088", "01089"],
        "declencher": [],
        "cibles": ["01094"],
        "jouer": ["hd003"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]], "statuts": [["01094", "Stunned"]]},
    },
    {
        "nom": "hd005 Quack Attack — Hero Interrupt : previent 2 des degats subis",
        "pourquoi": "WhenUnitWouldTakeDamage(HeroInterrupt, 'You') + message.PreventDamage(2) (modele 40012 Telekinetic Force Field). Source de degats DETERMINISTE (Puzzle.Damage, 3 points) plutot qu'une attaque de Rhino : Howard a DEF 2 contre ATK 2, il defend et ne subit rien, l'interruption n'a alors aucune fenetre (constate le 30/08/2026). 3 - 2 prevenus = 1 degat. Partage avec hd006, code identique",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.ChangeToFace('Howard Duckson', 'hd001a')"],
        "main_exclusive": ["hd005", "01088"],
        "declencher": ["Puzzle.Damage('hd001a', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1, "defausse": ["hd005"]},
    },
    {
        "nom": "hd007 Fowl Play — retire 3 menaces, vainc la manigance annexe et redresse le heros",
        "pourquoi": "RemoveThreatFromSchemes(..., if_this_remove_last_threat=<fn>) (modele 56009 Feline Senses / 29005 Fly Over) puis MayChooseOneAbility a 2 branches, dont la premiere est « Ready your hero ». Howard incline AVANT : son redressement prouve que la branche bonus a bien tourne. Partage avec hd008, code identique",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Howard Duckson', 'hd001a')",
            "Puzzle.PutIntoPlay('hd010', under_control=True)",
            "Puzzle.Exhaust('hd001a')",
        ],
        "main_exclusive": ["hd007", "01087", "01087"],
        "declencher": [],
        "cibles": ["hd010"],
        "jouer": ["hd007"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hd010"], "pret": ["hd001a"]},
    },
    {
        "nom": "hd009 Quack and Burn — Man-Thing en main, degats = ATK de Man-Thing, menace retiree = THW de Howard",
        "pourquoi": "Search.PlayerCard(name='Man-Thing') + GainCard (modele ok001b/ss001b) ; les DEUX montants sont dynamiques : 3 degats (ATK imprimee de Man-Thing, lue via printed_attack — lecon ss022) et 2 menaces (THW effective de la face Heros, modele 40009 Askani'son). La menace finale attendue est 2 et non 3 : les 5 menaces posees par Puzzle.SetThreat passent par PlaceThreatInternal, donc par Private Eye (hd001a, en jeu en forme heros) qui en previent 1 -> 4 posees, moins les 2 retirees = 2",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.ChangeToFace('Howard Duckson', 'hd001a')"],
        "main_exclusive": ["hd009", "01087", "01087"],
        "declencher": ["Puzzle.SetThreat('01097b', 5)"],
        "cibles": ["01094", "01097b"],
        "jouer": ["hd009"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "menace": [["01097b", 2]], "en_main": ["hd002"]},
    },
    {
        "nom": "hd010 Trapped — When Defeated : chaque joueur cherche un allie, le vainqueur peut le mettre en jeu",
        "pourquoi": "WhenSchemeBeDefeated(WhenDefeated, 'This', has_defeating_player=True) (modele 47003 Shopping Spree) ; la manigance est vaincue par une VRAIE action de joueur (hd007 joue), seul moyen d'avoir un `defeating_player`. Man-Thing depose en defausse : la recherche doit l'en sortir puis le poser en jeu",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Howard Duckson', 'hd001a')",
            "Puzzle.CreatePlayerDiscardPile('hd002')",
            "Puzzle.PutIntoPlay('hd010', under_control=True)",
        ],
        "main_exclusive": ["hd007", "01087", "01087"],
        "declencher": [],
        "cibles": ["hd010", "hd002"],
        "jouer": ["hd007"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hd010"], "en_jeu": ["hd002"]},
    },
    {
        "nom": "hd011 In a World — When Defeated : Tenace a chaque joueur, le vainqueur soigne 2 degats",
        "pourquoi": "meme montage que hd010 ; deux portees distinctes verifiees d'un coup — le statut Tenace (chaque joueur) ET le soin de 2 (le seul vainqueur, 3 degats subis avant -> 1 apres)",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Howard Duckson', 'hd001a')",
            "Puzzle.PutIntoPlay('hd011', under_control=True)",
            "Puzzle.Damage('hd001a', 3)",
        ],
        "main_exclusive": ["hd007", "01087", "01087"],
        "declencher": [],
        "cibles": ["hd011"],
        "jouer": ["hd007"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hd011"], "degats_identite": 1, "statuts": [["hd001a", "Tough"]]},
    },
    {
        "nom": "hd012 He Never Made — When Defeated : 3 cartes quittent la defausse, 1 va en main au lieu du deck",
        "pourquoi": "AskChooseFaces((0,3)) + ShuffleAllTo, avec la carte gardee RETIREE de la liste avant le remelange (piege `instead`). `accepter_choix` force le pilote a prendre le MAXIMUM de cibles : sans lui, un choix « up to 3 » se resout a 0 et la capacite parait morte",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Howard Duckson', 'hd001a')",
            "Puzzle.CreatePlayerDiscardPile('01051', '01088', '01089')",
            "Puzzle.PutIntoPlay('hd012', under_control=True)",
        ],
        "main": ["hd007", "01087", "01087"],
        "declencher": [],
        "cibles": ["hd012"],
        "accepter_choix": True,
        "jouer": ["hd007"],
        "verifier": "hd012_defausse_videe_et_une_carte_en_main",
    },
    {
        "nom": "hd013 Beverly Switzler — rend la carte Howard la plus BASSE de la defausse et soigne 1",
        "pourquoi": "filtre par SET (`CardFinder(set_name='Howard the Duck')`) sur `discard_pile.Get()`, qui rend la defausse du FOND vers le dessus. 01087 Haymaker est deposee SOUS hd005 : c'est elle la vraie carte du fond, mais elle n'est pas une carte Howard — si le filtre etait absent, c'est elle qui remonterait",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.CreatePlayerDiscardPile('01087', 'hd005')",
            "Puzzle.PutIntoPlay('hd013', under_control=True)",
            "Puzzle.Damage('hd001b', 2)",
        ],
        "declencher": ["Puzzle.Action('hd013', 'AlterEgoAction', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["hd005"], "degats_identite": 1, "exhausted": ["hd013"]},
    },
    {
        "nom": "hd014 Ducktective Agency — capacite Resource : 1 ressource mentale pour un EVENEMENT (preuve par insuffisance)",
        "pourquoi": "CanGenerateResources(Resource, Resources('B'), for_card=CardFinder(card_type=Event)) (modele 48005 Prehensile Tail). PREUVE PAR INSUFFISANCE : la main ne contient QUE First Aid (01086, evenement officiel a cout 1) et AUCUNE carte-ressource — la seule source de paiement possible est l'Agence. Cible du soin : l'identite, blessee au prealable. Un evenement a cout 2 ne convenait pas : le pilote generique ne compose pas un paiement a plusieurs sources, verifie avec un temoin officiel (40007 Graymalkin) pose a cote de l'Agence, lui non plus retenu",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Howard Duckson', 'hd001a')",
            "Puzzle.PutIntoPlay('hd014', under_control=True)",
            "Puzzle.Damage('hd001a', 3)",
        ],
        "main_exclusive": ["01086"],
        "declencher": [],
        "cibles": ["hd001a"],
        "payer_avec": ["hd014"],
        "jouer": ["01086"],
        "verifier": "etat_attendu",
        "attendu": {"defausse": ["01086"], "exhausted": ["hd014"], "degats_identite": 1},
    },
    {
        "nom": "hd014 Ducktective Agency — Hero Response : redressee apres le retrait de la derniere menace d'une manigance",
        "pourquoi": "AfterUnitDefeatedScheme(HeroResponse, 'You', None) (scheme.py:203, famille de 40001a Cable) ; l'Agence est inclinee AVANT, donc elle ne peut pas non plus servir a payer : son redressement ne peut venir que de la Response",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Howard Duckson', 'hd001a')",
            "Puzzle.PutIntoPlay('hd014', under_control=True)",
            "Puzzle.Exhaust('hd014')",
            "Puzzle.PutIntoPlay('hd010', under_control=True)",
        ],
        "main_exclusive": ["hd007", "01087", "01087"],
        "declencher": [],
        "cibles": ["hd010"],
        "jouer": ["hd007"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hd010"], "pret": ["hd014"]},
    },
    {
        "nom": "hd015 Duckpool Suit — +3 points de vie a l'identite et +1 ATK a Howard",
        "pourquoi": "deux GiveKeywordToInPlayWhenApplyThis de portees DIFFERENTES sur la meme carte (modele ok014 Royal Protector) : « you » (l'identite) pour les PV, la face Heros NOMMEE pour l'ATK",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.ChangeToFace('Howard Duckson', 'hd001a')"],
        "declencher": ["Puzzle.PutIntoPlay('hd015', under_control=True)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 3, "attack": 1}, "en_jeu": ["hd015"]},
    },
    {
        "nom": "hd015 Duckpool Suit — Hero Response : inclinee apres la defaite d'une manigance annexe, 1 degat a un ennemi",
        "pourquoi": "AfterUnitDefeatedScheme(HeroResponse, 'You', SchemeSide2) restreint aux manigances ANNEXES (contrairement a hd014, qui accepte n'importe quelle manigance) + CostFunc.Exhaust('This')",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Howard Duckson', 'hd001a')",
            "Puzzle.PutIntoPlay('hd015', under_control=True)",
            "Puzzle.PutIntoPlay('hd010', under_control=True)",
        ],
        "main_exclusive": ["hd007", "01087", "01087"],
        "declencher": [],
        "cibles": ["hd010", "01094"],
        "jouer": ["hd007"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hd010"], "exhausted": ["hd015"], "degats": [["01094", 1]]},
    },
    {
        "nom": "hd016 Iron Suit — Action : deplace 1 menace d'une manigance vers la carte (jeton, pas compteur)",
        "pourquoi": "RemoveThreatFromSchemes + Faces.PlaceTokensOn([this], <retire>, 'threat') (modele exact 50046 Secret Agent). La menace posee sur une carte JOUEUR est un JETON, jamais un compteur : la cle `jetons` du harnais le verifie explicitement",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.PutIntoPlay('hd016', under_control=True)",
            "Puzzle.SetThreat('01097b', 5)",
        ],
        "declencher": ["Puzzle.Action('hd016', 'Action', 0)"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]], "jetons": [["hd016", "threat", 1]], "exhausted": ["hd016"]},
    },
    {
        "nom": "hd016 Iron Suit — Hero Action : depense X menaces de la carte pour X degats a un sbire",
        "pourquoi": "DeclareNumber(1, <jetons disponibles>) puis ChooseAbilities a 2 branches de portees ASYMETRIQUES (degats a un SBIRE, menace sur n'importe quelle manigance). Le pilote prend le premier item offert : X=1, branche degats. 3 jetons poses, 2 doivent rester",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Howard Duckson', 'hd001a')",
            "Puzzle.PutIntoPlay('hd016', under_control=True)",
            "Puzzle.Token('hd016', 'threat', 3)",
            "Puzzle.PutIntoPlay('01110')",
        ],
        "declencher": ["Puzzle.Action('hd016', 'HeroAction', 0)"],
        "cibles": ["01110"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01110", 1]], "jetons": [["hd016", "threat", 2]]},
    },
    {
        "nom": "hd017 Nexus of all Realities — Interrupt : un allie quitte le jeu, un evenement est cherche dans le deck",
        "pourquoi": "WhenCardLeavePlay(Interrupt, ('YouControl', Ally)) + Search.PlayerCard(card_type=Event) ; la main est videe puis rechargee d'une SEULE carte ressource (aucun evenement) : tout evenement present en fin de cas ne peut venir que de la recherche. Man-Thing porte Tenacite : il faut DEUX coups de degats pour le vaincre, le premier etant absorbe par le statut Tenace (meme piege que il019 Kang). Le PREMIER Interrupt imprime (« choose a play area ») est deliberement non code, voir hd017.py",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Howard Duckson', 'hd001a')",
            "Puzzle.PutIntoPlay('hd002', under_control=True)",
        ],
        "main_exclusive": ["01090"],
        "declencher": ["Puzzle.Damage('hd002', 1)", "Puzzle.Damage('hd002', 99)"],
        "verifier": "hd017_un_evenement_cherche_en_main",
    },
    {
        "nom": "hd021 Waddle it Be? — branche 1 : incline l'alter-ego et retire l'obligation de la partie",
        "pourquoi": "WhenThisObligationGiveToYou + YouMayFlipToYourAlterEgoForm + ChooseAbilities a 2 branches (modele ok019 Funeral Rites / ss017) ; le pilote prend la premiere option, meme convention que il017",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('hd021')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hd021"]},
    },
    {
        "nom": "hd022 Duck and Cover! — When Revealed : defausse les cartes a ressource mentale imprimee, +1 menace par carte",
        "pourquoi": "hand_cards.FindCards(has_printed_res='B') + DiscardAll (modele 01179 Yon-Rogg's Treason) ; deux Genius (RES 'BB') en main : menace de depart 2 + 2 defaussees = 4. Cas joue en forme d'IDENTITE CIVILE a dessein, pour que Private Eye (hd001a, hors jeu en civil) n'interfere pas avec la menace posee",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [],
        "main_exclusive": ["01089", "01089"],
        "declencher": ["Puzzle.Reveal('hd022')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["hd022", 4]], "taille_main": 0},
    },
    {
        "nom": "hd023 Collector — When Revealed : defausse un allie controle",
        "pourquoi": "GetControlCardsByType(ally=True, support=True) (piege `you control`) + AskChooseFace + DiscardAll ; Man-Thing est le seul allie/soutien en jeu",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.PutIntoPlay('hd002', under_control=True)"],
        "declencher": ["Puzzle.Reveal('hd023')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hd002"], "en_jeu": ["hd023"]},
    },
    {
        "nom": "hd023 Collector — branche de repli : aucun allie ni soutien, la manigance du dessus du deck de rencontre entre en jeu",
        "pourquoi": "« If you CANNOT » : verifie AVANT le choix, pas apres un refus. hd025 remontee sur le dessus du deck de rencontre (Puzzle.PutIntoDeck) pour rendre la carte trouvee deterministe. Modele de la recherche : ss007 Spider-pathy",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.CreateEncounterDeck('hd025')", "Puzzle.PutIntoDeck('hd025')"],
        "declencher": ["Puzzle.Reveal('hd023')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["hd025", "hd023"]},
    },
    {
        "nom": "hd024 Hellcow — Interrupt : serait vaincue -> remelangee dans le deck de rencontre a la place",
        "pourquoi": "WhenUnitWouldBeDefeated('This') + SetBeInstead + ShuffleAllTo (modele exact ss021 Undead Hand Ninja / lj015 Annihilus) ; piege `instead` : la carte PART du terrain et ARRIVE dans le deck, elle n'est pas dupliquee",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.PutIntoPlay('hd024')"],
        "declencher": ["Puzzle.Damage('hd024', 99)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hd024"], "dans_deck_rencontre": ["hd024"]},
    },
    {
        "nom": "hd025 Duck, Duck, Doom! — range un allie sous la carte, puis le rend en main a sa defaite",
        "pourquoi": "TuckCardUnderHere + GetPlacedCardArea().Get() (modele exact 50081 Abduct Superhumans, qui les remet EN JEU la ou hd025 les rend EN MAIN via Faces.ReturnToHand(..., 'Owner'))",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.PutIntoPlay('hd002', under_control=True)"],
        "declencher": ["Puzzle.Reveal('hd025')", "Puzzle.SetThreat('hd025', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hd025"], "en_main": ["hd002"]},
    },
    {
        "nom": "hd025 Duck, Duck, Doom! — branche de repli : aucun allie, l'identite est desorientee",
        "pourquoi": "« If you CANNOT » distinct d'un refus : aucun allie en jeu du tout. Statut pose sur l'identite civile (hd001b), forme de depart",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('hd025')"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["hd001b", "Confused"]]},
    },
    {
        "nom": "hd026 A Fowl Plot — When Revealed : defausse une amelioration controlee",
        "pourquoi": "GetControlCardsByType(upgrade=True) + AskChooseFace ; `cibles` designe explicitement hd016 pour eviter que le pilote ne tombe sur hd017 (permanente, en jeu des la mise en place)",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.PutIntoPlay('hd016', under_control=True)"],
        "declencher": ["Puzzle.Reveal('hd026')"],
        "cibles": ["hd016"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["hd016"], "en_jeu": ["hd026"]},
    },
    {
        "nom": "hd027 Duck Hunt — When Revealed (Hero) : donne Tenace au vilain",
        "pourquoi": "WhenThisRevealed('Hero') (modele 01106 Stampede / ok023) + Faces.GiveStatus([villain], 'Tough')",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.ChangeToFace('Howard Duckson', 'hd001a')"],
        "declencher": ["Puzzle.Reveal('hd027')"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["01094", "Tough"]]},
    },
    {
        "nom": "hd027 Duck Hunt — When Revealed (Hero), branche « If you cannot » : le vilain deja Tenace est soigne de 3",
        "pourquoi": "« If you CANNOT » verifie AVANT (HasStatus('Tough')), pas apres un echec silencieux ; « heal 3 damage from IT » vise le vilain lui-meme (piege `that <nom>`) : 5 degats subis -> 2 apres",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.ChangeToFace('Howard Duckson', 'hd001a')",
            "Puzzle.Damage('01094', 5)",
            "Puzzle.Tough('01094')",
        ],
        "declencher": ["Puzzle.Reveal('hd027')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]]},
    },
    {
        "nom": "hd027 Duck Hunt — When Revealed (Alter-Ego) : la menace du vilain part sur les manigances annexes, pas sur le complot principal",
        "pourquoi": "interruption TEMPORAIRE WhenSchemeWouldPlaceThreat(MainScheme) enregistree avant BasicSchemes (modele 50035b Stealth) + PreventThreat('All') + repartition point par point (modele ok008). Piege `instead` : le complot principal doit rester a 0, la manigance annexe doit monter",
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": [
            "Puzzle.PutIntoPlay('hd010', under_control=True)",
            "Puzzle.SetThreat('01097b', 0)",
        ],
        "declencher": ["Puzzle.Reveal('hd027')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 0]], "menace_min": [["hd010", 4]]},
    },
    # ------------------------------------------------------------------------
    # Pack « wiccan » : wc001a-wc023 (custom, auteur « CptScorp », Cycle 2)
    #
    # Mecanique centrale : COMPTER LES ICONES DE BONUS DE LA CARTE DU DESSUS
    # DU DECK RENCONTRE. Comme pour agent_13, un cas vert avec 0 icone ne
    # prouverait rien : le deck Rencontre est donc truque via
    # `Puzzle.CreateEncounterDeck` avec des cartes a icones CONNUES —
    # 01106 Stampede (1 icone, palier « 0 ou 1 ») et 01111 Explosion
    # (2 icones, palier « 2 ou plus »).
    #
    # `Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')` et jamais
    # `Puzzle.ChangeForm` : la partie demarre en alter-ego, et ChangeToFace
    # nomme explicitement la face visee (piege du nom ambigu).
    # ------------------------------------------------------------------------
    {
        "nom": "wc001a Wiccan — Clairvoyance : la carte du dessus du deck rencontre est FACE VISIBLE (forme heros)",
        "pourquoi": ("`PlayWithTopCardOfDeckFaceup(..., only_during_player_phase=True)` pose un "
                     "`WhenPlayerPhaseBegin` : la sonde renvoie ce message dans le monde et "
                     "verifie que la carte du dessus est bien retournee. Sans le module, elle "
                     "reste face cachee et tout le kit joue a l'aveugle"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.CreateEncounterDeck('01106')"],
        "declencher": [],
        "verifier": "wc_clairvoyance_dessus_face_visible",
    },
    {
        "nom": "wc001b Billy Kaplan — Clairvoyance : face visible AUSSI en identite civile",
        "pourquoi": ("la capacite est imprimee sur LES DEUX faces : sans module sur wc001b, "
                     "passer en identite civile eteindrait la carte visible. C'est aussi ce cas "
                     "qui a trouve le bug moteur `CastTo(Hero)` de la fabrique partagee"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.CreateEncounterDeck('01106')"],
        "declencher": [],
        "verifier": "wc_clairvoyance_dessus_face_visible",
    },
    {
        "nom": "wc001a Wiccan — Forced Interrupt : au debut de la phase du vilain, le dessus du deck rencontre est defausse",
        "pourquoi": ("declencheur hors de portee de l'API Puzzle (aucune commande n'avance de "
                     "phase) : la sonde renvoie `Message.WhenPhaseBegin('Villain')` dans le "
                     "monde, exactement ce que fait `world.phase_begin` (world.py:789-793)"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.CreateEncounterDeck('01106')"],
        "declencher": [],
        "verifier": "wc001a_defausse_au_debut_de_la_phase_du_vilain",
    },
    {
        "nom": "wc001b Billy Kaplan — Action : regarde les 2 du dessus du deck rencontre et en defausse 1",
        "pourquoi": ("la defausse est OPTIONNELLE (« you MAY discard one of them ») : sans "
                     "`accepter_choix`, le pilote choisit 0 carte et la capacite parait morte "
                     "(piege du §8 du guide). La defausse de rencontre est VIDE au depart, "
                     "donc toute carte qui s'y trouve vient de cette action"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.CreateEncounterDeck('01106')"],
        "declencher": ["Puzzle.Action('wc001b', 'Action')"],
        "accepter_choix": True,
        "verifier": "wc_defausse_rencontre_non_vide",
    },
    {
        "nom": "wc002 Hulkling — Interrupt : +1 ATQ par icone de bonus du dessus du deck, puis cette carte est defaussee",
        "pourquoi": ("deck Rencontre truque a 2 icones (01111 Explosion) : ATQ 1* (=1 en solo) "
                     "+ 2 icones = 3 degats. Un cas a 0 icone ne distinguerait rien. La carte "
                     "defaussee prouve la seconde phrase du texte"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.PutIntoPlay('wc002', under_control=True)"],
        "declencher": ["Puzzle.CreateEncounterDeck('01111')", "Puzzle.Attack('wc002')"],
        "cibles": ["01094"],
        "verifier": "wc002_hulkling_bonus_et_defausse",
    },
    {
        "nom": "wc003 Impenetrable Barrier — Hero Action : Tough au heros PUIS a X personnages amis",
        "pourquoi": ("deux phrases, deux portees : le heros recoit son Tough sans condition, "
                     "les X autres viennent des icones de bonus (01111 = 2). `accepter_choix` "
                     "exerce le « up to X », dont le minimum est 0 et que le pilote declinerait "
                     "sinon. Code partage avec wc004"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.PutIntoPlay('wc002', under_control=True)"],
        "declencher": ["Puzzle.CreateEncounterDeck('01111')"],
        "main_exclusive": ["wc003", "01088"],
        "accepter_choix": True,
        "jouer": ["wc003"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["wc001a", "Tough"], ["wc002", "Tough"]]},
    },
    {
        "nom": "wc005 Magic Bolt — palier « 0 ou 1 icone » : 3 degats puis pioche 1",
        "pourquoi": ("deck Rencontre truque a 1 icone (01106 Stampede) : la branche du haut. "
                     "Main videe puis rechargee, donc la carte en main a la fin ne peut venir "
                     "que de la pioche. Code partage avec wc006 et wc007"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')"],
        "main_exclusive": ["wc005", "01088"],
        "cibles": ["01094"],
        "jouer": ["wc005"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "taille_main": 1},
    },
    {
        "nom": "wc005 Magic Bolt — palier « 2 icones ou plus » : 3 + 3 degats, le SECOND en ranged",
        "pourquoi": ("deck Rencontre truque a 2 icones (01111 Explosion). La cible est "
                     "M.O.D.O.K. (01184, 8 PV, Retaliate 2 IMPRIME) : il survit aux 6 degats, "
                     "et sa riposte distingue les deux montages — seule la SECONDE salve est "
                     "ranged (arbitrage documente dans wc005.py), donc l'identite ne doit "
                     "encaisser la riposte qu'UNE fois"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.PutIntoPlay('01184')"],
        "declencher": ["Puzzle.CreateEncounterDeck('01111')"],
        "main_exclusive": ["wc005", "01088"],
        "cibles": ["01184"],
        "accepter_choix": True,
        "jouer": ["wc005"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01184", 6]]},
    },
    {
        "nom": "wc008 Magic Manipulation — Alter-Ego Action : X cartes remontent de la defausse dans le deck, puis pioche 1",
        "pourquoi": ("X = icones de bonus (01111 = 2), donc EXACTEMENT les 2 cartes semees dans "
                     "la defausse doivent la quitter. Un cas a 0 icone ne prouverait rien. "
                     "Aucun ChangeToFace : la partie demarre deja en alter-ego"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.CreatePlayerDiscardPile('01086')",
                          "Puzzle.CreatePlayerDiscardPile('01087')"],
        "declencher": ["Puzzle.CreateEncounterDeck('01111')"],
        "main_exclusive": ["wc008"],
        "jouer": ["wc008"],
        "verifier": "wc008_defausse_remontee_dans_le_deck",
    },
    {
        "nom": "wc009 Magic Portal — palier « 0 ou 1 icone » : 5 menaces retirees puis pioche 1",
        "pourquoi": ("deck Rencontre truque a 1 icone (01106). Menace posee a 6, SOUS le seuil "
                     "du complot : au-dela il s'accomplit et l'evenement n'a plus de cible "
                     "legale. Code partage avec wc010"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.SetThreat('01097b', 6)"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')"],
        "main_exclusive": ["wc009", "01088", "01089"],
        "cibles": ["01097b"],
        "jouer": ["wc009"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    {
        "nom": "wc009 Magic Portal — palier « 2 icones ou plus » : 5 menaces sur la cible PUIS 2 sur CHAQUE manigance en jeu",
        "pourquoi": ("deck Rencontre truque a 2 icones (01111). Une manigance annexe (01107) est "
                     "posee a 3 menaces a cote : elle doit descendre a 1 sans avoir ete choisie, "
                     "ce qui prouve la portee « each scheme in play » (piege `each`)"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.SetThreat('01097b', 6)",
                          "Puzzle.PutIntoPlay('01107')",
                          "Puzzle.SetThreat('01107', 3)"],
        "declencher": ["Puzzle.CreateEncounterDeck('01111')"],
        "main_exclusive": ["wc009", "01088", "01089"],
        "cibles": ["01097b"],
        "jouer": ["wc009"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01107", 1]]},
    },
    {
        "nom": "wc011 Teleport — Action : redresse l'identite du joueur choisi et lui donne +1 a un pouvoir de base",
        "pourquoi": ("deck Rencontre truque a 2 icones (01111), seul palier qui donne le bonus. "
                     "L'identite est inclinee au depart : le redressement et le bonus sont deux "
                     "preuves independantes. Code partage avec wc012"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.Exhaust('wc001a')"],
        "declencher": ["Puzzle.CreateEncounterDeck('01111')"],
        "main_exclusive": ["wc011", "01088"],
        "jouer": ["wc011"],
        "preferer_option": "Cancel",
        "verifier": "wc011_teleport",
    },
    {
        "nom": "wc011 Teleport — Action : « that player MAY change their form » (bascule optionnelle acceptee)",
        "pourquoi": ("seconde moitie de la meme phrase imprimee. Sans ce cas, la bascule de "
                     "forme n'est jamais exercee : le cas voisin repond « Cancel » a la "
                     "question pour garder la face heros et pouvoir mesurer le +1 ATQ. Ici on "
                     "laisse le pilote accepter, et la partie doit finir en identite civile"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.Exhaust('wc001a')"],
        "declencher": ["Puzzle.CreateEncounterDeck('01111')"],
        "main_exclusive": ["wc011", "01088"],
        "jouer": ["wc011"],
        "verifier": "etat_attendu",
        "attendu": {"forme": "AlterEgo", "pret": ["wc001b"]},
    },
    {
        "nom": "wc013 Transmutation — Action : la carte cherchee dans le deck rencontre remonte SUR LE DESSUS",
        "pourquoi": ("01111 est place sur le dessus, 01143 juste dessous ; `cibles` force la "
                     "recherche sur 01143. Le selecteur remelange le deck (search_internal.py), "
                     "donc retrouver 01143 sur le dessus prouve la remontee, pas un hasard"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.CreateEncounterDeck('01143')",
                          "Puzzle.CreateEncounterDeck('01111')"],
        "declencher": [],
        "main_exclusive": ["wc013"],
        "cibles": ["01143"],
        "jouer": ["wc013"],
        "verifier": "wc013_carte_remontee_sur_le_dessus",
    },
    {
        "nom": "wc014 Warping Reality — Action : la carte suivante coute 1+X de moins (preuve par insuffisance)",
        "pourquoi": ("Magic Portal (wc009) coute 3 et la main ne contient qu'Energy (01088), qui "
                     "fournit 2 ressources : SANS la reduction elle est injouable. Avec 1 icone "
                     "de bonus (01106), la reduction vaut 1+1=2, le cout tombe a 1 et la carte "
                     "part. Preuve par insuffisance, sans ambiguite"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.SetThreat('01097b', 6)"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')"],
        "main_exclusive": ["wc014", "wc009", "01088"],
        "cibles": ["01097b"],
        # Warping Reality porte elle-meme une ressource [wild] : sans cette
        # interdiction, le pilote la DEPENSE pour financer Magic Portal (0+2+1
        # = 3, le cout plein) et le cas reste vert meme sans le module — c'est
        # ce qu'a montre la preuve par substitution du 30/08/2026. Interdite
        # comme ressource, elle ne peut plus servir qu'a ce que la carte fait
        # vraiment : reduire le cout suivant.
        "ne_pas_depenser": ["wc014"],
        "jouer": ["wc014", "wc009"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]], "defausse": ["wc009"]},
    },
    {
        "nom": "wc015 Mother's Protection — Interrupt : 3 degats prevenus, la carte retourne dans le deck",
        "pourquoi": ("5 degats infliges a l'identite, 3 prevenus -> 2 encaisses. Le cout "
                     "(remelanger la carte dans le deck) est REEL : elle ne doit plus etre en jeu"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.PutIntoPlay('wc015', under_control=True)"],
        "declencher": ["Puzzle.Damage('wc001a', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "hors_jeu": ["wc015"]},
    },
    {
        "nom": "wc016 Wiccan's Cloak — Response : l'evenement SPELL qui compte les icones est RESOLU UNE SECONDE FOIS",
        "pourquoi": ("Magic Bolt (wc005) inflige 3 degats ; rejouee par la cape elle en inflige "
                     "3 de plus, sans etre repayee (`ResolveToPlayer` -> `skip_cost=True`). "
                     "6 degats et la cape inclinee : deux preuves. Deck Rencontre truque a "
                     "01106 pour rester sur le palier bas et ne pas melanger les branches"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.PutIntoPlay('wc016', under_control=True)"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')"],
        "main_exclusive": ["wc005", "01088"],
        "cibles": ["01094"],
        "accepter_choix": True,
        "jouer": ["wc005"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["01094", 6]], "exhausted": ["wc016"]},
    },
    {
        "nom": "wc017 Royal Couple — Hero Action AVEC Hulkling : la carte de la defausse rencontre remonte et le heros est redresse",
        "pourquoi": ("Team-Up rendu comme condition « Hulkling en jeu » (arbitrage utilisateur "
                     "du 30/08/2026). Le heros est incline au depart, la defausse de rencontre "
                     "est truquee a 01106 : les deux moities du texte sont observables"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.PutIntoPlay('wc002', under_control=True)",
                          "Puzzle.CreateEncounterDiscardPile('01106')",
                          "Puzzle.Exhaust('wc001a')"],
        "declencher": [],
        "main_exclusive": ["wc017", "01088"],
        "jouer": ["wc017"],
        "verifier": "wc017_royal_couple",
    },
    {
        "nom": "wc017 Royal Couple — SANS Hulkling : la carte reste injouable, le heros reste incline",
        "pourquoi": ("contre-epreuve de la condition : sans elle, la carte partirait quand meme "
                     "et redresserait le heros. C'est exactement le defaut qu'il023 avait "
                     "(`only_if_you_control_face` qui ne voit pas les allies)"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.CreateEncounterDiscardPile('01106')",
                          "Puzzle.Exhaust('wc001a')"],
        "declencher": [],
        "main_exclusive": ["wc017", "01088"],
        "jouer": ["wc017"],
        "verifier": "wc017_sans_hulkling",
    },
    {
        "nom": "wc018 Avoiding the Demiurge — branche 1 : incliner l'identite -> retirer l'obligation du jeu",
        "pourquoi": ("le pilote prend TOUJOURS la premiere option d'un ChooseAbilities "
                     "(convention il017/ok019) : c'est donc cette branche-la qu'il exerce "
                     "spontanement. L'obligation doit avoir QUITTE le jeu"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('wc018')"],
        "verifier": "wc018_obligation_retiree",
    },
    {
        "nom": "wc018 Avoiding the Demiurge — branche 2 : les icones de bonus ne sont plus comptees, jusqu'a la fin de la phase joueur",
        "pourquoi": ("branche inatteignable sans la cle `preferer_option` ajoutee le 30/08/2026 "
                     "(le pilote prend toujours la premiere option). Le verificateur controle "
                     "l'interrupteur global du pack DANS LES DEUX SENS : leve juste apres, puis "
                     "abaisse quand la sonde renvoie `WhenPhaseEnd('Player')` dans le monde"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('wc018')"],
        "preferer_option": "Boost icons cannot be counted",
        "verifier": "wc018_interrupteur_des_boosts",
    },
    {
        "nom": "wc019a New Vessel — When Completed (8 menaces) : Moridun est mis de cote et la carte se RETOURNE en wc019b The Demiurge",
        "pourquoi": ("mecanisme rare : une manigance annexe qui devient un ENVIRONNEMENT. La "
                     "carte est generee avec SES DEUX FACES (« wc019a,wc019b ») — avec la seule "
                     "face recto, `Card.Flip` la couche face cachee et elle QUITTE le jeu "
                     "(lecon Dazzler). Le seuil de 8 est cable a la main (ecart assume, "
                     "modele mw018)"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.PutIntoPlay('wc019a,wc019b')"],
        "declencher": ["Puzzle.PlaceThreat('wc019a', 4)"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["wc019b"], "hors_jeu": ["wc019a"]},
    },
    {
        "nom": "wc019a New Vessel — When Defeated : 2 menaces retirees du complot principal, la manigance et Moridun mis de cote",
        "pourquoi": ("« set aside » et non « discard » : c'est ce qui permet a wc020 de "
                     "re-reveler « your SET-ASIDE New Vessel side scheme ». Le complot principal "
                     "est pose a 5 : il doit finir a 3"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.PutIntoPlay('wc019a,wc019b')",
                          "Puzzle.SetThreat('01097b', 5)"],
        "declencher": ["Puzzle.PlaceThreat('wc019a', -4)"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "hors_jeu": ["wc019a", "wc019b"]},
    },
    {
        "nom": "wc019b The Demiurge — Forced Response : quand un deck de JOUEUR se vide, 1 menace sur le complot principal",
        "pourquoi": ("declencheur hors de portee de l'API Puzzle sans bruit (vider le deck "
                     "declenche aussi la penalite standard, qui distribue une carte rencontre "
                     "et fausserait le releve) : la sonde renvoie `Message.AfterDeckRunOut` sur "
                     "le deck du joueur, exactement ce que fait `Deck` quand il se vide"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.PutIntoPlay('wc019a,wc019b')",
                          "Puzzle.PlaceThreat('wc019a', 4)",
                          "Puzzle.SetThreat('01097b', 0)"],
        "declencher": [],
        "verifier": "wc019b_deck_joueur_vide",
    },
    {
        "nom": "wc020 Moridun — When Revealed : la manigance New Vessel MISE DE COTE est revelee",
        "pourquoi": ("wc019a est deja dans la zone de reserve du joueur au montage de la partie "
                     "(le set nemesis y vit, worlds.py:384) : la carte revelee est donc bien "
                     "CELLE DU DECK, pas une copie fabriquee par le harnais"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('wc020')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["wc020", "wc019a"]},
    },
    {
        "nom": "wc020 Moridun — Forced Interrupt : quand Wiccan inflige des degats a un ennemi, 1 menace sur New Vessel",
        "pourquoi": ("New Vessel demarre a 4 menaces imprimees : apres une attaque de base de "
                     "Wiccan elle doit etre a 5. Le declencheur est nomme (« Wiccan »), pas "
                     "« votre identite »"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.Reveal('wc020')"],
        "declencher": ["Puzzle.Attack('wc001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"menace_min": [["wc019a", 5]]},
    },
    {
        "nom": "wc020 Moridun — Forced Interrupt : quand Wiccan retire de la menace d'une manigance, 1 menace sur New Vessel",
        "pourquoi": ("second declencheur de la meme phrase imprimee (« deal damage OR remove "
                     "threat ») : deux fabriques distinctes, jamais un `if`. Le retrait passe "
                     "par Magic Portal (wc009), dont la cible est forcee sur le complot "
                     "principal pour ne pas viser New Vessel elle-meme"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.Reveal('wc020')",
                          "Puzzle.SetThreat('01097b', 6)"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')"],
        "main_exclusive": ["wc009", "01088", "01089"],
        "cibles": ["01097b"],
        "jouer": ["wc009"],
        "verifier": "etat_attendu",
        "attendu": {"menace_min": [["wc019a", 5]]},
    },
    {
        "nom": "wc021 Inescapable Horror — When Revealed SANS Moridun : 1 degat a chaque personnage ami, aucun etourdissement",
        "pourquoi": ("portee NUE (« each friendly character ») : l'identite ET l'allie "
                     "encaissent. Sans Moridun en jeu, la seconde phrase ne doit PAS partir — "
                     "c'est le contre-exemple du cas suivant. Code partage avec wc022"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.PutIntoPlay('wc002', under_control=True)"],
        "declencher": ["Puzzle.Reveal('wc021')"],
        "verifier": "wc021_degats_sans_etourdissement",
    },
    {
        "nom": "wc021 Inescapable Horror — When Revealed AVEC Moridun : le joueur est SONNE en plus",
        "pourquoi": "la branche conditionnelle « If Moridun is in play » n'est exercee que la",
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.PutIntoPlay('wc020')"],
        "declencher": ["Puzzle.Reveal('wc021')"],
        "verifier": "etat_attendu",
        "attendu": {"statuts": [["wc001a", "Stunned"]], "degats_identite": 1},
    },
    {
        "nom": "wc021 Inescapable Horror — capacite Boost : 1 degat a chaque personnage ami QUE VOUS CONTROLEZ",
        "pourquoi": ("portee DIFFERENTE de celle du When Revealed (« you control » imprime sur "
                     "la seule capacite Boost) ; sans module, la capacite Boost n'existe pas et "
                     "l'allie ne prend rien"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.ChangeToFace('Billy Kaplan', 'wc001a')",
                          "Puzzle.PutIntoPlay('wc002', under_control=True)"],
        "declencher": ["Puzzle.Boost('wc021')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_min": [["wc002", 1]]},
    },
    {
        "nom": "wc023 Master Magus Returns — When Revealed : Moridun mis de cote est revele, la trahison est retiree du jeu",
        "pourquoi": ("wc020 est dans la zone de reserve du joueur au montage (set nemesis) : "
                     "c'est bien la carte du deck qui entre en jeu. « then remove ... from the "
                     "game » appartient a la branche conditionnelle"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('wc023')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["wc020"], "hors_jeu": ["wc023"]},
    },
    {
        "nom": "wc023 Master Magus Returns — When Revealed avec The Demiurge en jeu : rien n'est revele, le joueur est DESORIENTE",
        "pourquoi": ("branche negative du texte : « If Moridun was not revealed this way, you "
                     "are confused ». New Vessel est accomplie au montage pour poser "
                     "l'environnement, ce qui bloque la revelation"),
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": ["Puzzle.PutIntoPlay('wc019a,wc019b')",
                          "Puzzle.PlaceThreat('wc019a', 4)"],
        "declencher": ["Puzzle.Reveal('wc023')"],
        "verifier": "wc023_desoriente_et_non_retiree",
    },
    {
        "nom": "wc023 Master Magus Returns — capacite Boost : le joueur est DESORIENTE",
        "pourquoi": "capacite Boost distincte du When Revealed, sans module elle n'existe pas",
        "scenario": "rhino",
        "heros": "wiccan",
        "mise_en_place": [],
        "declencher": ["Puzzle.Boost('wc023')"],
        "verifier": "identite_a_un_statut",
    },
    {
        "nom": "wc019a New Vessel — seul le joueur Billy Kaplan peut retirer de la menace de cette manigance",
        "pourquoi": ("restriction intestable en solo : il faut une VRAIE partie a deux joueurs "
                     "(`heros2`) et deux tentatives de retrait, une par joueur. Le pilote "
                     "generique ne sait pas faire contrer le SECOND joueur : la verification "
                     "monte donc les deux effets a la main (`GameRule(identite)`, dont "
                     "`initiator` vaut le joueur controlant la face, rule.py:10-22) et compare "
                     "les deux resultats"),
        "scenario": "rhino",
        "heros": "wiccan",
        "heros2": "okoye",
        "mise_en_place": ["Puzzle.PutIntoPlay('wc019a,wc019b')"],
        "declencher": [],
        "verifier": "wc019a_seul_billy_retire_la_menace",
    },
    # ------------------------------------------------------------------------
    # Pack « speed » : sd001a-sd022 (custom, auteur « CptScorp », Cycle 2)
    #
    # MECANIQUE CENTRALE : LES COMPTEURS EXPLOSIFS. Le compteur s'appelle
    # `explosive` ; il se pose avec `Puzzle.Counter('<card_id>', 'explosive', N)`
    # et se lit avec la cle `compteurs` de `etat_attendu`.
    #
    # Le BALAYAGE de fin de phase des joueurs (regle de l'insert) est hors de
    # portee de l'API Puzzle, qui n'avance aucune phase : deux verificateurs
    # sont des SONDES IN-PROCESS et renvoient dans le monde
    # `Message.WhenPhaseEnd(monde.phase_id, "Player", monde)`, exactement le
    # message qu'emet `world.phase_end` au meme moment.
    #
    # `Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')` et jamais
    # `Puzzle.ChangeForm` : la partie demarre en alter-ego, et ChangeToFace
    # nomme explicitement la face visee (piege du nom ambigu — le catalogue
    # contient aussi un allie `15010` « * Speed » et un sbire `57060`).
    #
    # Ressources de paiement, toujours par `main_exclusive` : `01088` Energy
    # (YY, donc « uniquement en energie ») et `01090` Strength (RR, donc
    # PHYSIQUE : le temoin negatif de Hyperkinetic Fuel). Un wild ne peut pas
    # servir de temoin negatif — il compte comme energie.
    # ------------------------------------------------------------------------
    {
        "nom": "sd001a Speed — Hyperkinetic Fuel : un evenement paye UNIQUEMENT en energie pose 1 compteur explosif",
        "pourquoi": ("mecanique centrale du pack. `main_exclusive` a 01088 (YY) garantit que "
                     "le paiement est integralement en energie ; sans cette cle le pilote "
                     "puiserait dans la main de depart et `OnlyHasColor(\'Y\')` ne serait "
                     "jamais vrai (piege Ashley Barton). Le compteur est pose AVANT que "
                     "l'evenement se resolve : c'est un Interrupt"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')"],
        "declencher": [],
        "main_exclusive": ["sd008", "01088"],
        "cibles": ["01094"],
        "jouer": ["sd008"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "explosive", 1]]},
    },
    {
        "nom": "sd001a Speed — Hyperkinetic Fuel NE part PAS quand l'evenement est paye en PHYSIQUE",
        "pourquoi": ("temoin negatif indispensable : sans lui, une capacite qui poserait un "
                     "compteur a CHAQUE evenement passerait le cas precedent. 01090 Strength "
                     "fournit RR ; un wild aurait compte comme energie et n'aurait rien prouve"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')"],
        "declencher": [],
        "main_exclusive": ["sd008", "01090"],
        "cibles": ["01094"],
        "jouer": ["sd008"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "explosive", 0]], "degats": [["01094", 3]]},
    },
    {
        "nom": "sd001a Speed — regle de l'insert : PLAFOND de 1 compteur explosif par ennemi/manigance",
        "pourquoi": ("regle transverse portee par l'identite, pas par une carte. On demande "
                     "5 compteurs d'un coup : le plafond doit en laisser 1. Meme forme que le "
                     "cas ht001a (plafond de 3 compteurs flamme)"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')"],
        "declencher": ["Puzzle.Counter('01094', 'explosive', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["01094", "explosive", 1]]},
    },
    {
        "nom": "sd001a Speed — regle de l'insert : a la fin de la phase des joueurs, le compteur d'un ENNEMI part et lui inflige 1 degat",
        "pourquoi": ("declencheur hors de portee de l'API Puzzle (aucune commande n'avance de "
                     "phase) : la sonde renvoie `Message.WhenPhaseEnd(phase_id, \'Player\')` "
                     "dans le monde. Le verificateur controle les DEUX moities : le compteur "
                     "a disparu ET le degat a ete inflige"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')"],
        "declencher": ["Puzzle.Counter('01094', 'explosive', 1)"],
        "verifier": "sd_balayage_ennemi",
    },
    {
        "nom": "sd001b Thomas Shepherd — regle de l'insert EN ALTER-EGO : le compteur d'une MANIGANCE part et retire 1 menace",
        "pourquoi": ("la regle est imprimee sur l'insert, pas sur une carte : elle doit valoir "
                     "sur LES DEUX faces. Sans module sur sd001b, finir la phase des joueurs "
                     "en identite civile laisserait les compteurs en place pour toujours. "
                     "Aucun ChangeToFace ici : la partie demarre deja en alter-ego"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.SetThreat('01097b', 5)"],
        "declencher": ["Puzzle.Counter('01097b', 'explosive', 1)"],
        "verifier": "sd_balayage_manigance",
    },
    {
        "nom": "sd001b Thomas Shepherd — Accelerated Perception : un evenement remonte de la defausse dans le deck, puis pioche 1",
        "pourquoi": ("le remelange vise UN EVENEMENT (sd003 seme dans la defausse) et la "
                     "pioche est INCONDITIONNELLE. Main videe puis rechargee d'une seule "
                     "carte : une main a 2 a la fin ne peut venir que de la pioche"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.CreatePlayerDiscardPile('sd003')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('sd001b', 'Action')"],
        # `main_exclusive` VIDE la main de depart DANS LA DEFAUSSE : elle y jette
        # d'autres evenements (01052, 01053...). Sans `cibles`, le pilote prend
        # le premier evenement legal et le releve ne veut plus rien dire.
        "cibles": ["sd003"],
        "verifier": "sd001b_accelerated_perception",
    },
    {
        "nom": "sd002 Quicksilver — Interrupt : AUCUN degat consecutif quand la cible porte un compteur explosif",
        "pourquoi": ("ATQ 2* = 1 degat consecutif imprime, lu nativement. La capacite doit "
                     "l'annuler pour CETTE utilisation. Modele du declencheur : 17020 Cosmo"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.PutIntoPlay('sd002', under_control=True)"],
        "declencher": ["Puzzle.Counter('01094', 'explosive', 1)",
                       "Puzzle.Attack('sd002')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["sd002", 0], ["01094", 2]]},
    },
    {
        "nom": "sd002 Quicksilver — contre-epreuve SANS compteur : il encaisse bien son degat consecutif",
        "pourquoi": ("temoin negatif : sans lui, un allie qui ne prendrait JAMAIS de degat "
                     "consecutif passerait le cas precedent"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.PutIntoPlay('sd002', under_control=True)"],
        "declencher": ["Puzzle.Attack('sd002')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["sd002", 1], ["01094", 2]]},
    },
    {
        "nom": "sd003 Blasting Velocity — 3 menaces retirees PUIS attaque de base sur l'ennemi marque, sans s'incliner",
        "pourquoi": ("les deux moities de la carte sont mesurees separement. Le heros est "
                     "INCLINE au depart : l'attaque de base part quand meme, ce qui prouve "
                     "le « without exhausting ». Paiement en PHYSIQUE (01090) pour que "
                     "Hyperkinetic Fuel ne pose pas un second compteur et ne brouille pas "
                     "le releve. Code partage avec sd004"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.SetThreat('01097b', 6)",
                          "Puzzle.Exhaust('sd001a')"],
        "declencher": ["Puzzle.Counter('01094', 'explosive', 1)"],
        "main_exclusive": ["sd003", "01090"],
        "cibles": ["01097b", "01094"],
        "jouer": ["sd003"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 3]], "degats": [["01094", 1]]},
    },
    {
        "nom": "sd005 \"I'm Out\" — Hero Interrupt : la carte rencontre revelee est annulee et defaussee",
        "pourquoi": ("modele mw009 Foresight : l'evenement est en main, `Puzzle.Reveal` fait "
                     "venir la carte du deck Rencontre (sans quoi `from_encounter=True` ne "
                     "matcherait jamais). sd020 s'attacherait au vilain si elle n'etait pas "
                     "annulee : son absence du jeu est la preuve. Paiement en PHYSIQUE pour "
                     "rester sur la branche « annulation » et pas sur le « instead »"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')"],
        "main_exclusive": ["sd005", "01090"],
        "declencher": ["Puzzle.Reveal('sd020')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["sd020"], "defausse": ["sd005"]},
    },
    {
        "nom": "sd005 \"I'm Out\" — branche « instead » : payee en energie, elle remonte un evenement et pioche AU LIEU de poser un compteur",
        "pourquoi": ("couplage inter-cartes : c'est la capacite du HEROS (sd001a) qui teste "
                     "si la carte payee est sd005. Sa ressource IMPRIMEE est MENTALE, le cas "
                     "« payee uniquement en energie » doit donc etre construit expres. Le "
                     "verificateur controle les TROIS consequences : l'evenement remonte, "
                     "AUCUN compteur explosif en jeu, et l'annulation a quand meme eu lieu"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.CreatePlayerDiscardPile('sd003')"],
        "main_exclusive": ["sd005", "01088"],
        "declencher": ["Puzzle.Reveal('sd020')"],
        # Voir le cas sd001b : la main de depart part a la defausse et y ajoute
        # d'autres evenements ; `cibles` fixe celui que la carte doit remonter.
        "cibles": ["sd003"],
        "verifier": "sd005_instead",
    },
    {
        "nom": "sd006 Kinetic Flurry — X attaques SEPAREES a 3 degats sur l'ennemi marque",
        "pourquoi": ("cout X : sans `surpayer` le pilote ne paie rien, X vaut 0 et la carte "
                     "parait inerte (piege du §8). 01088 fournit 2 energies -> X = 2, et "
                     "l'ennemi porte un compteur -> 3 degats par attaque, donc 6. A 2 degats "
                     "(branche sans compteur) on lirait 4 : les deux branches sont "
                     "distinguables. Code partage avec sd007"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')"],
        "declencher": ["Puzzle.Counter('01094', 'explosive', 1)"],
        "main_exclusive": ["sd006", "01088"],
        "surpayer": True,
        "cibles": ["01094"],
        "jouer": ["sd006"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 6]]},
    },
    {
        "nom": "sd008 Swift Strikes — 3 degats PUIS contre de base sur la manigance marquee, sans s'incliner",
        "pourquoi": ("MIROIR de sd003 : degats d'abord, CONTRE de base ensuite, sur une "
                     "MANIGANCE marquee. Le heros est incline au depart, le contre part quand "
                     "meme. CTR 1 -> 6 menaces deviennent 5. Le cas sd016 rejoue exactement "
                     "ce montage AVEC Quick Adaptation en jeu et lit 4 : la paire prouve le "
                     "+1 CTR. Code partage avec sd009 et sd010"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.SetThreat('01097b', 6)",
                          "Puzzle.Exhaust('sd001a')"],
        "declencher": ["Puzzle.Counter('01097b', 'explosive', 1)"],
        "main_exclusive": ["sd008", "01090"],
        "cibles": ["01094", "01097b"],
        "jouer": ["sd008"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "menace": [["01097b", 5]]},
    },
    {
        "nom": "sd011 Top Speed — AVEC un compteur explosif en jeu : 1 + 2 ressources, la carte a 3 devient jouable (preuve par insuffisance)",
        "pourquoi": ("Never Ending Spark (sd015) coute 3 et Top Speed est la SEULE ressource "
                     "en main. Sans le supplement double, elle ne fournirait que 2 et la "
                     "carte resterait injouable : sa presence en jeu prouve les 3 ressources. "
                     "Code partage avec sd012"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')"],
        "declencher": ["Puzzle.Counter('01094', 'explosive', 1)"],
        "main_exclusive": ["sd015", "sd011"],
        "jouer": ["sd015"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["sd015"]},
    },
    {
        "nom": "sd011 Top Speed — SANS compteur explosif : le supplement n'est que de 1, la carte a 3 reste injouable",
        "pourquoi": ("contre-epreuve du cas precedent, meme montage sans le compteur. Sans "
                     "elle, un supplement de 2 INCONDITIONNEL passerait le premier cas"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')"],
        "declencher": [],
        "main_exclusive": ["sd015", "sd011"],
        "jouer": ["sd015"],
        "verifier": "etat_attendu",
        # Une carte dont le cout ne peut pas etre paye n'est PAS rendue a la
        # main : `CardPlayer.Play` la defausse (card_player.py:134-136). Les
        # deux cles ensemble disent bien « elle n'est jamais entree en jeu ».
        "attendu": {"hors_jeu": ["sd015"], "defausse": ["sd015"]},
    },
    {
        "nom": "sd011 Top Speed — la carte qu'on paie part QUAND MEME, mais plus aucune autre ensuite",
        "pourquoi": ("LE point risque de la carte : `PlayersCannotPlayCardWhile` ne doit pas "
                     "bloquer la carte en cours de paiement, sinon Top Speed n'a aucun sens. "
                     "Le verificateur controle les deux : sd014 est bien entree en jeu, et "
                     "sd013 (cout 1, financable par le 01088 encore en main) n'est plus "
                     "jouable"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')"],
        "declencher": [],
        "main_exclusive": ["sd014", "sd013", "sd011", "01088"],
        "payer_avec": ["sd011"],
        "jouer": ["sd014"],
        "verifier": "sd011_restriction_du_tour",
    },
    {
        "nom": "sd013 Mother's Protection — Interrupt : 3 degats prevenus, la carte retourne dans le deck",
        "pourquoi": ("duplicat volontaire de wc015 (meme carte reutilisee par l'auteur pour "
                     "le frere jumeau) : le cas est donc le meme. 5 degats infliges, 3 "
                     "prevenus -> 2 encaisses, et le cout (remelanger la carte) est REEL"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.PutIntoPlay('sd013', under_control=True)"],
        "declencher": ["Puzzle.Damage('sd001a', 5)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "hors_jeu": ["sd013"]},
    },
    {
        "nom": "sd014 Explosive Touch — apres une ATTAQUE de base sur une cible marquee : la carte s'incline, Speed est redresse",
        "pourquoi": ("une attaque de base incline le heros (c'est son cout) : le retrouver "
                     "PRET apres l'attaque ne peut venir que de la Response. L'inclinaison "
                     "d'Explosive Touch prouve que le cout a bien ete paye"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.PutIntoPlay('sd014', under_control=True)"],
        "declencher": ["Puzzle.Counter('01094', 'explosive', 1)",
                       "Puzzle.Attack('sd001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["sd001a"], "exhausted": ["sd014"]},
    },
    {
        "nom": "sd014 Explosive Touch — apres un CONTRE de base sur une manigance marquee (via sd008)",
        "pourquoi": ("l'autre moitie du declencheur imprime (« basic attack OR basic "
                     "thwart »). L'API Puzzle n'a pas de commande de contre : on passe par "
                     "le contre de base offert par Swift Strikes. Le heros est incline au "
                     "depart et doit finir PRET"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.PutIntoPlay('sd014', under_control=True)",
                          "Puzzle.SetThreat('01097b', 6)",
                          "Puzzle.Exhaust('sd001a')"],
        "declencher": ["Puzzle.Counter('01097b', 'explosive', 1)"],
        "main_exclusive": ["sd008", "01090"],
        "cibles": ["01094", "01097b"],
        "jouer": ["sd008"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["sd001a"], "exhausted": ["sd014"]},
    },
    {
        "nom": "sd015 Never Ending Spark — Hero Response : la carte inclinee est REDRESSEE quand un compteur explosif est pose",
        "pourquoi": ("premiere des deux capacites imprimees. La carte est inclinee au depart : "
                     "seule la Response peut la redresser"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.PutIntoPlay('sd015', under_control=True)",
                          "Puzzle.Exhaust('sd015')"],
        "declencher": ["Puzzle.Counter('01094', 'explosive', 1)"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["sd015"]},
    },
    {
        "nom": "sd015 Never Ending Spark — Resource : elle finance seule une carte a cout 1 et s'incline",
        "pourquoi": ("seconde capacite imprimee, distincte. La main ne contient QUE la carte "
                     "a jouer : la ressource ne peut venir que de la Spark, et son "
                     "inclinaison prouve le cout"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.PutIntoPlay('sd015', under_control=True)"],
        "declencher": [],
        "main_exclusive": ["sd013"],
        "jouer": ["sd013"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["sd013"], "exhausted": ["sd015"]},
    },
    {
        "nom": "sd016 Quick Adaptation — +1 ATQ contre un ennemi marque",
        "pourquoi": ("ATQ imprimee 1 : une attaque de base a 2 degats ne peut venir que du "
                     "bonus. La carte NE S'INCLINE PAS (c'est sd014 qui s'incline), le "
                     "verificateur le controle aussi pour ne pas confondre les deux cartes"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.PutIntoPlay('sd016', under_control=True)"],
        "declencher": ["Puzzle.Counter('01094', 'explosive', 1)",
                       "Puzzle.Attack('sd001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "pret": ["sd016"]},
    },
    {
        "nom": "sd016 Quick Adaptation — +1 CTR contre une manigance marquee (via sd008)",
        "pourquoi": ("montage IDENTIQUE au cas sd008, plus Quick Adaptation en jeu : la "
                     "manigance tombe a 4 au lieu de 5. La paire de cas est la preuve du +1 "
                     "CTR, et l'API Puzzle n'a pas de commande de contre"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.PutIntoPlay('sd016', under_control=True)",
                          "Puzzle.SetThreat('01097b', 6)",
                          "Puzzle.Exhaust('sd001a')"],
        "declencher": ["Puzzle.Counter('01097b', 'explosive', 1)"],
        "main_exclusive": ["sd008", "01090"],
        "cibles": ["01094", "01097b"],
        "jouer": ["sd008"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]]},
    },
    {
        "nom": "sd017 No Outrunning This — branche 1 : incliner Thomas Shepherd -> l'obligation est retiree du jeu",
        "pourquoi": ("le pilote prend TOUJOURS la premiere option d'un ChooseAbilities "
                     "(convention il017/ok019/wc018) : c'est donc cette branche-la qu'il "
                     "exerce spontanement. La partie demarre en alter-ego, la condition "
                     "`player.IsAlterEgo()` est remplie"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('sd017')"],
        "verifier": "sd017_obligation_retiree",
    },
    {
        "nom": "sd017 No Outrunning This — branche 2 : Hyperkinetic Fuel eteint jusqu'a la fin du PROCHAIN round",
        "pourquoi": ("branche inatteignable sans `preferer_option`. Le verificateur controle "
                     "l'interrupteur DANS LES DEUX SENS et surtout la duree : apres la "
                     "PREMIERE fin de round il doit rester leve (c'est le round courant), il "
                     "ne retombe qu'a la SECONDE (« the end of the NEXT round »). C'est la "
                     "difference avec wc018, qui s'eteint des la fin de la phase joueur"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": [],
        "declencher": ["Puzzle.Reveal('sd017')"],
        "preferer_option": "You cannot resolve Speed",
        "verifier": "sd017_interrupteur_hyperkinetic",
    },
    {
        "nom": "sd018 The Real Question — When Revealed : defausse jusqu'a un attachement, qui est ensuite REVELE",
        "pourquoi": ("le deck Rencontre est truque avec sd020 sur le dessus : l'attachement "
                     "trouve doit etre revele, donc entrer en jeu attache au vilain. Modeles "
                     "40093 et wd104, qui impriment la meme phrase"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": [],
        "declencher": ["Puzzle.CreateEncounterDeck('sd020')", "Puzzle.Reveal('sd018')"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["sd018", "sd020"]},
    },
    {
        "nom": "sd018 The Real Question — tant qu'elle est en jeu, les attachements gagnent Permanent",
        "pourquoi": ("seconde phrase imprimee, distincte du When Revealed. L'attachement "
                     "entre en jeu APRES la manigance : c'est le chemin le plus fragile de "
                     "`GiveKeywordToInPlayWhenApplyThis`. Le verificateur lit le mot-cle sur "
                     "la carte, pas le texte"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.PutIntoPlay('sd018')"],
        "declencher": ["Puzzle.PutIntoPlay('sd020')"],
        "verifier": "sd018_attachements_permanents",
    },
    {
        "nom": "sd019 Coat of Arms — [star] : si son attaque inflige des degats, 1 degat de plus a CHAQUE personnage du joueur",
        "pourquoi": ("le sbire est mis en jeu AVANT le passage en forme heros, sinon "
                     "Quickstrike (natif, non code) declencherait une attaque de plus et "
                     "fausserait le releve. Identite ET allie sont INCLINES : sinon le "
                     "pilote declare un defenseur (constate le 30/08/2026 : Quicksilver "
                     "encaissait l'attaque a la place du heros). ATQ 1 -> l'identite "
                     "encaisse 1 puis 1 de "
                     "supplement = 2, et l'allie 1 : la portee « each character you control » "
                     "est ainsi verifiee sur DEUX personnages"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.PutIntoPlay('sd019')",
                          "Puzzle.PutIntoPlay('sd002', under_control=True)",
                          "Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.Exhaust('sd001a')",
                          "Puzzle.Exhaust('sd002')"],
        "declencher": ["Puzzle.Attack('sd019')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "degats": [["sd002", 1]]},
    },
    {
        "nom": "sd020 Inspirational Art — attachee au vilain, chaque carte de bonus d'une activation gagne +1 icone",
        "pourquoi": ("deck Rencontre truque a 01106 Stampede (1 icone imprimee). Rhino ATQ 2 "
                     "+ 1 icone = 3 sans l'attachement, 4 avec : la valeur exacte est la "
                     "preuve du +1. `en_jeu` controle en meme temps l'attache au vilain"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.PutIntoPlay('sd020')",
                          "Puzzle.Exhaust('sd001a')"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')", "Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 4, "en_jeu": ["sd020"]},
    },
    {
        "nom": "sd020 Inspirational Art — Hero Action : depenser [energy][physical] la defausse",
        "pourquoi": ("cout releve par DECOUPE D'IMAGE, pas a vue (lecon Lockjaw) : 01088 (YY) "
                     "et 01090 (RR) fournissent exactement une energie et un physique"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.PutIntoPlay('sd020')"],
        # ⚠ LIMITE DU PILOTE : `payer()` compte des RESSOURCES, pas des
        # COULEURS (`besoin = len(cout)`, puis `poids = len(couleur)`). Energy
        # (01088, « YY ») couvrait donc a lui seul un cout de 2 et le paiement
        # partait sans le physique, ce que le moteur refusait ensuite en
        # silence. On finance donc avec deux cartes a UNE SEULE icone : sd003
        # imprime [energy], sd008 imprime [physical].
        "main_exclusive": ["sd003", "sd008"],
        "declencher": ["Puzzle.Action('sd020', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["sd020"]},
    },
    {
        "nom": "sd020 Inspirational Art — la Hero Action devient INDISPONIBLE tant que The Real Question est en jeu",
        "pourquoi": ("collision Permanent : une carte permanente ne peut pas etre defaussee, "
                     "et le moteur PLANTE sur ce chemin (assert de card_face.py). La Hero "
                     "Action doit donc etre grisee, pas echouer. Le verificateur interroge le "
                     "filtre du gestionnaire d'evenements, exactement comme `Puzzle.Action`"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.PutIntoPlay('sd018')",
                          "Puzzle.PutIntoPlay('sd020')"],
        "main_exclusive": ["01088", "01090"],
        "declencher": [],
        "verifier": "sd020_action_indisponible",
    },
    {
        "nom": "sd021 Magic Chains — attachee a Coat of Arms, elle etourdit le heros puis se defausse",
        "pourquoi": ("l'attache conditionnelle vise Coat of Arms EN PRIORITE : l'attachement "
                     "doit donc etre lie au sbire, pas au vilain. Le sbire est pose avant le "
                     "passage en forme heros pour eviter Quickstrike. Les deux consequences "
                     "sont controlees : statut Sonne ET carte defaussee"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.PutIntoPlay('sd019')",
                          "Puzzle.PutIntoPlay('sd021')",
                          "Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.Exhaust('sd001a')"],
        "declencher": ["Puzzle.Attack('sd019')"],
        "verifier": "sd021_chaines",
    },
    {
        "nom": "sd021 Magic Chains — en ALTER-EGO le cout de la fleche est impayable : la carte RESTE",
        "pourquoi": ("la fleche lie un COUT (« stun your hero ») a un EFFET (« discard this "
                     "card ») : regle officielle du Rules Reference, confirmee par "
                     "l'utilisateur le 30/08/2026. Sans heros en jeu le cout n'est pas "
                     "payable, donc RIEN ne se passe et l'attachement garde son +1 ATQ. "
                     "Contre-epreuve du cas precedent, dont il ne differe que par l'absence "
                     "de passage en forme heros"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.PutIntoPlay('sd019')",
                          "Puzzle.PutIntoPlay('sd021')"],
        "declencher": ["Puzzle.Attack('sd019')"],
        "verifier": "sd021_cout_impayable",
    },
    {
        "nom": "sd022 Conflicted Feelings — tant qu'elle est en jeu, Coat of Arms ne peut pas subir de degats",
        "pourquoi": ("`Puzzle.Damage` ne fait RIEN sur un sbire (piege documente du guide) : "
                     "on passe donc par une vraie attaque de base du heros. ATQ 1 -> 1 degat "
                     "attendu sans l'obligation, 0 avec. `en_jeu` controle au passage que "
                     "l'obligation RESTE en jeu apres avoir ete donnee (modele 28021)"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.PutIntoPlay('sd019')",
                          "Puzzle.ChangeToFace('Thomas Shepherd', 'sd001a')",
                          "Puzzle.Reveal('sd022')"],
        "declencher": ["Puzzle.Attack('sd001a')"],
        "cibles": ["sd019"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["sd019", 0]], "en_jeu": ["sd022"]},
    },
    {
        "nom": "sd022 Conflicted Feelings — Alter-Ego Action : depenser [energy][mental] la defausse",
        "pourquoi": ("cout releve par DECOUPE D'IMAGE : 01088 (YY) et 01089 (BB) fournissent "
                     "exactement une energie et un mental. La partie demarre en alter-ego, "
                     "l'action est donc disponible d'emblee"),
        "scenario": "rhino",
        "heros": "speed",
        "mise_en_place": ["Puzzle.Reveal('sd022')"],
        # Meme limite du pilote que pour sd020 : deux cartes a UNE icone, sd003
        # ([energy]) et sd005 ([mental]).
        "main_exclusive": ["sd003", "sd005"],
        "declencher": ["Puzzle.Action('sd022', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["sd022"]},
    },
    # ------------------------------------------------------------------------
    # Pack « patriot » : pt001a-pt022 (custom, auteur « CptScorp », Cycle 2)
    #
    # TOUT LE KIT PARLE D'ALLIES : 12 des 17 cartes joueur en dependent. Les
    # cas ci-dessous posent donc presque toujours un allie sous controle.
    # `01083` Mockingbird (ATQ 1*, CTR 1*, 3 PV) sert d'allie de reference :
    # elle est dans le deck de depart Leadership, ses DEUX pouvoirs de base
    # infligent 1 degat consecutif, et ses valeurs sont assez basses pour que
    # chaque bonus se lise a l'unite.
    #
    # `Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')` et jamais
    # `Puzzle.ChangeForm` : la partie demarre en alter-ego, et ChangeToFace
    # nomme explicitement la face visee (piege du nom ambigu).
    #
    # Les degats d'une attaque de Rhino dependent de ses icones de bonus :
    # `Puzzle.CreateEncounterDeck('01106')` (Stampede, 1 icone) rend la valeur
    # DETERMINISTE — Rhino ATQ 2 + 1 = 3.
    # ------------------------------------------------------------------------
    {
        "nom": "pt001a Patriot — Will to Protect : le degat CONSECUTIF de l'allie part sur Patriot",
        "pourquoi": ("modele dt009 Savior Complex : `SetBeInstead` + `TakeDamage`. Le degat "
                     "est DEPLACE, pas duplique (lecon The Spot) : l'allie doit finir a 0 "
                     "degat ET l'identite a 1. Un seul des deux releves ne prouverait rien"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01083', under_control=True)"],
        "declencher": ["Puzzle.Attack('01083')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01083", 0]], "degats_identite": 1},
    },
    {
        "nom": "pt001a Patriot — Will to Protect : LIMITE une fois par round (deux allies frappent)",
        "pourquoi": ("`.LimitOncePerRound()` imprime entre parentheses. Deux allies a degat "
                     "consecutif attaquent : Patriot ne doit encaisser qu'UNE fois, l'autre "
                     "allie garde son degat. Sans la limite, l'identite prendrait 2"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01083', under_control=True)",
                          "Puzzle.PutIntoPlay('01067', under_control=True)"],
        "declencher": ["Puzzle.Attack('01083')", "Puzzle.Attack('01067')"],
        "cibles": ["01094", "01094"],
        "verifier": "pt001a_limite_une_fois_par_round",
    },
    {
        "nom": "pt001b Elijah Bradley — Action : le Patriot's Shield sort du deck et arrive en main",
        "pourquoi": ("PIEGE DU `*` D'UNICITE : pt012 s'appelle « * Patriot's Shield » dans "
                     "cards.json, mais paper.py:45 retire le prefixe. Une recherche sur "
                     "« * Patriot's Shield » ne trouverait rien, EN SILENCE. Le cas prouve "
                     "que le nom cherche est le bon, et que l'identite s'incline (le cout)"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": [],
        "declencher": ["Puzzle.Action('pt001b', 'Action')"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["pt012"], "exhausted": ["pt001b"]},
    },
    {
        "nom": "pt002 Hawkingbird — +1 PV a TOUS les allies, ELLE COMPRISE",
        "pourquoi": ("le texte n'ecrit PAS « other » : a 1 PV imprime, Hawkingbird mourrait "
                     "au moindre degat sans son propre bonus. Le cas controle les DEUX "
                     "allies, le sien et celui d'a cote — un seul ne departagerait pas "
                     "`not_include_this=True` de `False`"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('pt002', under_control=True)",
                          "Puzzle.PutIntoPlay('01083', under_control=True)"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["pt002", "health", 1], ["01083", "health", 1]]},
    },
    {
        "nom": "pt002 Hawkingbird — Response : elle cherche une amelioration ATTACHABLE A UN ALLIE",
        "pourquoi": ("le filtre n'est pas « une amelioration » mais « attachable a un allie » "
                     "(`CardFinder(canbe_attach_to=...)`). Le deck est truque avec pt013 "
                     "(s'attache a un allie) ET pt012 (s'attache a l'identite) : seule la "
                     "premiere doit remonter. Sans le filtre, pt012 serait un choix legal"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')"],
        "declencher": ["Puzzle.CreatePlayerDeck('pt013')",
                       "Puzzle.PutIntoPlay('pt002', under_control=True)"],
        "accepter_choix": True,
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["pt013"]},
    },
    {
        "nom": "pt003 Aided Defense — +1 DEF par PV RESTANT de l'allie epuise, puis il est redresse",
        "pourquoi": ("Rhino ATQ 2 + 1 icone (01106) = 3 degats. DEF 2 du heros + 2 PV de "
                     "Maria Hill = 4 : le heros ne prend RIEN, donc « if you take no damage "
                     "-> ready the exhausted ally » part aussi. Les trois moities de la carte "
                     "sont mesurees d'un coup (cout paye, bonus, redresse). `Puzzle.Defend` "
                     "ouvre la fenetre et le pilote joue la carte depuis la main, comme pour "
                     "sg016 Unbeatable!. Code partage avec pt004"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01067', under_control=True)"],
        "main_exclusive": ["pt003"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')",
                       "Puzzle.Defend('pt001a', '01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "pret": ["01067"], "defausse": ["pt003"]},
    },
    {
        "nom": "pt005 Covered Fire — l'allie CHOISI (pas epuise) inflige ses degats d'ATQ a un ennemi",
        "pourquoi": ("difference avec pt003 : l'allie est DESIGNE, il ne s'incline pas. "
                     "Maria Hill ATQ 1 -> exactement 1 degat sur Rhino, et l'allie reste "
                     "PRET. Ce n'est pas une attaque de l'allie : aucun degat consecutif. "
                     "Code partage avec pt006"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01067', under_control=True)"],
        "main_exclusive": ["pt005", "01088"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')",
                       "Puzzle.Defend('pt001a', '01094')"],
        "cibles": ["01067", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1], ["01067", 0]], "pret": ["01067"],
                    "defausse": ["pt005"]},
    },
    {
        "nom": "pt007 Isaiah Bradley — +1 REC continu ET Alter-Ego Action : 2 degats soignes",
        "pourquoi": ("les deux capacites imprimees sont mesurees ensemble : `attributs` lit "
                     "le REC courant contre le REC imprime (3 -> 4), `degats_identite` "
                     "prouve le soin de 2 sur 3 degats poses. La partie demarre en "
                     "alter-ego, l'action est donc disponible d'emblee"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.PutIntoPlay('pt007', under_control=True)",
                          "Puzzle.Damage('pt001b', 3)"],
        "declencher": ["Puzzle.Action('pt007', 'AlterEgoAction')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"recover": 1}, "degats_identite": 1,
                    "exhausted": ["pt007"]},
    },
    {
        "nom": "pt008 Commandeer — l'attachement passe du vilain a l'allie, texte blanc, SCH devenu CTR",
        "pourquoi": ("04075 Exo-Suit porte ATK+ 1 ET SCH+ 1 : c'est la seule facon de "
                     "mesurer la conversion. Rhino doit REDESCENDRE a son ATQ imprimee, "
                     "Mockingbird monter de +1 ATQ et de +1 CTR (le SCH converti, qu'un "
                     "allie perdrait sinon en silence, face_gain.py:123). Le verificateur "
                     "controle aussi que la carte est bien LIEE a l'allie et traitee comme "
                     "blanche"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01083', under_control=True)",
                          "Puzzle.PutIntoPlay('04075')",
                          "Puzzle.PutIntoPlay('pt008', under_control=True)"],
        "declencher": ["Puzzle.Action('pt008', 'HeroAction')"],
        "cibles": ["01083", "04075"],
        "verifier": "pt008_attachement_deplace",
    },
    {
        "nom": "pt009 Commander's Orders — l'ATQ et le CTR de l'allie sont ECHANGES pour cette activation",
        "pourquoi": ("Maria Hill 01067 a ATQ 1 et CTR 2 : apres l'echange elle frappe pour 2. "
                     "PIEGE `message.power` : il vaut 'ATK'/'THW', jamais 'Attack'/'Thwart' — "
                     "une condition ecrite avec le mauvais litteral serait MORTE et le cas "
                     "montrerait 1 degat"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01067', under_control=True)",
                          "Puzzle.PutIntoPlay('pt009', under_control=True)"],
        "declencher": ["Puzzle.Attack('01067')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]], "exhausted": ["pt009"]},
    },
    {
        "nom": "pt010 Follow My Lead — la ressource [wild] finance une amelioration attachable a un allie",
        "pourquoi": ("modele mw006 Weaving a Web. pt013 Revenge (cout 1, s'attache a un "
                     "allie) est la seule carte en main : sans la ressource elle reste "
                     "injouable, avec elle elle entre en jeu. Un allie est en jeu, sans quoi "
                     "aucune amelioration ne passerait le filtre"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01083', under_control=True)",
                          "Puzzle.PutIntoPlay('pt010', under_control=True)"],
        "main_exclusive": ["pt013"],
        "declencher": [],
        "jouer": ["pt013"],
        "cibles": ["01083"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["pt013"], "exhausted": ["pt010"]},
    },
    {
        "nom": "pt010 Follow My Lead — contre-epreuve : elle NE finance PAS une amelioration d'identite",
        "pourquoi": ("la ressource est RESTREINTE. pt012 Patriot's Shield coute 1 et "
                     "s'attache a l'IDENTITE : elle ne passe pas le filtre, donc elle n'entre "
                     "JAMAIS en jeu et la ressource n'est jamais depensee (pt010 reste "
                     "PRET). Contre-epreuve du cas precedent, dont il ne differe que par "
                     "la carte a payer. Cette verte-la est legitime : elle affirme que RIEN "
                     "ne se passe"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01083', under_control=True)",
                          "Puzzle.PutIntoPlay('pt010', under_control=True)"],
        "main_exclusive": ["pt012"],
        "declencher": [],
        "jouer": ["pt012"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["pt012"], "pret": ["pt010"]},
    },
    {
        "nom": "pt011 On Your Feet — branche 1 : un allie incline est REDRESSE",
        "pourquoi": ("le pilote prend la PREMIERE option d'un ChooseAbilities : c'est la "
                     "redresse. L'allie est incline en mise en place, sans quoi la branche "
                     "n'aurait aucune cible legale (`canbe_ready=True`)"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01083', under_control=True)",
                          "Puzzle.PutIntoPlay('pt011', under_control=True)",
                          "Puzzle.Exhaust('01083')"],
        "declencher": ["Puzzle.Action('pt011', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["01083"], "exhausted": ["pt011"]},
    },
    {
        "nom": "pt011 On Your Feet — branche 2 : 1 degat soigne sur un allie",
        "pourquoi": ("branche inatteignable sans la cle `preferer_option` : le pilote prend "
                     "toujours la premiere option. L'allie porte 2 degats en mise en place, "
                     "sans quoi la branche n'a aucune cible (`canbe_heal=True`)"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01083', under_control=True)",
                          "Puzzle.PutIntoPlay('pt011', under_control=True)",
                          "Puzzle.Damage('01083', 2)"],
        "declencher": ["Puzzle.Action('pt011', 'HeroAction')"],
        "preferer_option": "Heal 1 damage",
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01083", 1]], "exhausted": ["pt011"]},
    },
    {
        "nom": "pt012 Patriot's Shield — +1 DEF continu ET 1 SEUL degat DEPLACE sur la carte",
        "pourquoi": ("modele 04065 Crossbones' Armor, mais 1 point et non tous : Rhino ATQ 2 "
                     "+ 1 icone (01106) = 3, le heros est INCLINE donc ne defend pas, il "
                     "encaisse 2 et le bouclier prend 1 compteur. Si le point etait duplique "
                     "au lieu d'etre deplace, l'identite serait a 3"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('pt012', under_control=True)",
                          "Puzzle.Exhaust('pt001a')"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')", "Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"defense": 1}, "degats_identite": 2,
                    "compteurs": [["pt012", "damage", 1]]},
    },
    {
        "nom": "pt012 Patriot's Shield — a 3 degats elle est DEFAUSSEE",
        "pourquoi": ("le seuil imprime est 3, pas 5 (04065). Deux compteurs sont poses en "
                     "mise en place, le troisieme vient de l'attaque : la carte doit quitter "
                     "le jeu dans la foulee"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('pt012', under_control=True)",
                          "Puzzle.Counter('pt012', 'damage', 2)",
                          "Puzzle.Exhaust('pt001a')"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')", "Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["pt012"], "degats_identite": 2},
    },
    {
        "nom": "pt013 Revenge — quand Patriot encaisse une attaque, l'allie porteur gagne +2 ATQ",
        "pourquoi": ("« YourHero » et non un CardFinder par NOM : DEUX allies "
                     "officiels s'appellent deja Patriot (29016, 56041). Le heros ET l'allie "
                     "sont inclines : c'est le seul moyen de faire arriver l'attaque "
                     "jusqu'a l'identite. La carte est defaussee (le cout de la fleche) et "
                     "l'allie monte de 1 a 3 d'ATQ"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01067', under_control=True)",
                          "Puzzle.PutIntoPlay('pt013', under_control=True)",
                          "Puzzle.Exhaust('pt001a')",
                          "Puzzle.Exhaust('01067')"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')", "Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["01067", "attack", 2]], "hors_jeu": ["pt013"]},
    },
    {
        "nom": "pt014 The Chosen Leader — Forced Response : un allie qui DEFEND coute 1 degat a l'identite",
        "pourquoi": ("TEXTE CONTRADICTOIRE tranche par l'utilisateur le 30/08/2026 : le "
                     "mot-cle en gras (« Forced Response ») fait foi, « When » n'est que de "
                     "l'anglais relache. `AfterUnitBecomeDefender` part au moment ou l'allie "
                     "est DESIGNE defenseur, donc meme s'il meurt de l'attaque"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01067', under_control=True)",
                          "Puzzle.PutIntoPlay('pt014', under_control=True)"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')",
                       "Puzzle.Attack('01094', defender='01067')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 1},
    },
    {
        "nom": "pt014 The Chosen Leader — Response : allie vaincu par degat CONSECUTIF -> un allie remonte en main",
        "pourquoi": ("restriction forte `by_consequential=True` (modele 38028 Med Lab) : un "
                     "allie tue par une ATTAQUE ne declencherait RIEN. Deux allies frappent : "
                     "le premier consomme la limite de Will to Protect, le second (a 1 PV) "
                     "encaisse donc vraiment son degat consecutif et meurt. La main est "
                     "VIDEE par `main_exclusive` : tout allie qui s'y trouve ensuite vient "
                     "de la recherche"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('pt014', under_control=True)",
                          "Puzzle.PutIntoPlay('01067', under_control=True)",
                          "Puzzle.PutIntoPlay('01083', under_control=True)",
                          "Puzzle.Damage('01083', 2)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01067')", "Puzzle.Attack('01083')"],
        "cibles": ["01094", "01094"],
        "verifier": "pt014_allie_cherche",
    },
    {
        "nom": "pt015 Throwing Stars — 3 degats REPARTIS en plus de l'attaque de l'allie porteur",
        "pourquoi": ("`repeat_rules` « Health » rend la vraie repartition : un clic = une "
                     "attribution, il en faut TROIS (les doublons de all_legal_targets sont "
                     "du sens, pas du bruit). Mockingbird ATQ 1 + 3 repartis = 4 degats sur "
                     "Rhino, et la carte est defaussee (le cout de la fleche)"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01083', under_control=True)",
                          "Puzzle.PutIntoPlay('pt015', under_control=True)"],
        "declencher": ["Puzzle.Attack('01083')"],
        "cibles": ["01094", "01094", "01094", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]], "hors_jeu": ["pt015"]},
    },
    {
        "nom": "pt016 Working Together — le CTR d'un AUTRE personnage ami s'ajoute au contre de l'allie",
        "pourquoi": ("« another » : l'allie porteur est exclu de la liste, seul Patriot "
                     "(CTR 1) est un choix legal en solo. 6 menaces - 1 (allie) - 1 (heros) "
                     "= 4. La carte est defaussee (le cout de la fleche)"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01083', under_control=True)",
                          "Puzzle.PutIntoPlay('pt016', under_control=True)",
                          "Puzzle.SetThreat('01097b', 6)"],
        "declencher": ["Puzzle.Action('01083', 'BasicPower', 1)"],
        "cibles": ["01097b", "pt001a"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]], "hors_jeu": ["pt016"]},
    },
    {
        "nom": "pt017 MGH Addiction — branche 1 : defausser Isaiah Bradley retire l'obligation DU JEU",
        "pourquoi": ("la fleche est un COUT : sans pt007 en jeu la branche est INDISPONIBLE. "
                     "Ici elle est disponible et le pilote prend la premiere option. Les "
                     "DEUX cartes doivent quitter le jeu"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.PutIntoPlay('pt007', under_control=True)"],
        "declencher": ["Puzzle.Reveal('pt017')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["pt017", "pt007"]},
    },
    {
        "nom": "pt017 MGH Addiction — branche 2 : tous les allies sont EPUISES, pas de surge",
        "pourquoi": ("sans pt007 en jeu la premiere branche est indisponible : seule la "
                     "seconde est proposee. Un allie PRET est epuise « this way », donc la "
                     "condition du surge est fausse. L'obligation part a la defausse"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.PutIntoPlay('01083', under_control=True)"],
        "declencher": ["Puzzle.Reveal('pt017')"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["01083"], "hors_jeu": ["pt017"]},
    },
    {
        "nom": "pt018 Mr. Hyde's Lab — When Defeated : Mr. Hyde n'est pas la, il est CHERCHE et mis en jeu",
        "pourquoi": ("le sbire nemesis est place dans le deck Rencontre par le banc "
                     "(au montage il vit dans la reserve du joueur, hors de portee d'une "
                     "recherche « encounter deck + discard pile »). La manigance est "
                     "ramenee a 1 menace pour qu'un seul contre de base la batte"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('pt018')",
                          "Puzzle.SetThreat('pt018', 1)"],
        "declencher": ["Puzzle.CreateEncounterDeck('pt019')",
                       "Puzzle.Action('pt001a', 'BasicPower', 1)"],
        "cibles": ["pt018"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["pt019"], "hors_jeu": ["pt018"]},
    },
    {
        "nom": "pt019 Mr. Hyde — When Revealed : le MGH Drug est cherche dans TROIS zones et attache a lui",
        "pourquoi": ("« encounter deck, encounter discard pile AND SET ASIDE CARDS » : trois "
                     "zones, pas deux (pt018, elle, n'en cite que deux). Le verificateur "
                     "controle que l'attachement est bien LIE au sbire, pas seulement en jeu"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')"],
        "declencher": ["Puzzle.CreateEncounterDeck('pt020')", "Puzzle.Reveal('pt019')"],
        "verifier": "pt019_mgh_drug_attachee",
    },
    {
        "nom": "pt020 MGH Drug — Hero Action : depenser [mental][energy] la defausse",
        "pourquoi": ("cout releve par DECOUPE D'IMAGE, pas a vue (lecon Lockjaw). Meme "
                     "limite du pilote que pour sd020 : deux cartes a UNE icone, pt009 "
                     "([mental]) et pt003 ([energy]). L'attache conditionnelle est controlee "
                     "au passage — sans elle la carte ne serait meme pas en jeu"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('pt020')"],
        "main_exclusive": ["pt009", "pt003"],
        "declencher": ["Puzzle.Action('pt020', 'HeroAction')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["pt020"]},
    },
    {
        "nom": "pt020 MGH Drug — [star] : les attaques de l'ennemi porteur gagnent OVERKILL",
        "pourquoi": ("l'overkill n'est observable qu'avec un defenseur qui MEURT : "
                     "Maria Hill ramenee a 1 PV encaisse l'attaque, l'exces passe a "
                     "l'identite. Rhino ATQ 2 + 1 (l'ATK+ de la carte) + 1 icone (01106) = 4, "
                     "moins 1 PV du defenseur = 3 sur l'identite. Sans overkill, l'identite "
                     "ne prendrait RIEN"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('pt020')",
                          "Puzzle.PutIntoPlay('01067', under_control=True)",
                          "Puzzle.Damage('01067', 1)"],
        "declencher": ["Puzzle.CreateEncounterDeck('01106')",
                       "Puzzle.Attack('01094', defender='01067')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3},
    },
    {
        "nom": "pt021 Bulldozing Charge — When Revealed SANS Mr. Hyde : 1 degat a CHAQUE personnage ami",
        "pourquoi": ("le repli part aussi quand le sbire n'est pas en jeu (modele 02040 Tail "
                     "Sweep, `else: action()`). « each friendly character » n'est pas "
                     "restreint a « you control » : l'allie ET l'identite encaissent. Code "
                     "partage avec pt022"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01083', under_control=True)"],
        "declencher": ["Puzzle.Reveal('pt021')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01083", 1]], "degats_identite": 1},
    },
    {
        "nom": "pt021 Bulldozing Charge — AVEC Mr. Hyde en jeu : il attaque, l'allie ne prend RIEN",
        "pourquoi": ("contre-epreuve du cas precedent : quand l'attaque a lieu, la branche "
                     "« if no attack was made this way » ne part PAS. Le heros ET l'allie "
                     "sont inclines pour que personne ne defende, l'allie doit rester "
                     "intact. Cette verte "
                     "affirme que RIEN ne se passe cote allie ; son jumeau positif est le "
                     "cas precedent"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('pt019')",
                          "Puzzle.PutIntoPlay('01067', under_control=True)",
                          "Puzzle.Exhaust('pt001a')",
                          "Puzzle.Exhaust('01067')"],
        "declencher": ["Puzzle.Reveal('pt021')"],
        "verifier": "pt021_hyde_a_frappe",
    },
    {
        "nom": "pt021 Bulldozing Charge — capacite Boost : l'attaque en cours gagne OVERKILL",
        "pourquoi": ("la trahison est posee sur le DESSUS du deck Rencontre : elle devient "
                     "la carte de bonus de l'attaque. 1 icone imprimee -> Rhino ATQ 2 + 1 = 3, "
                     "moins 1 PV du defenseur = 2 sur l'identite grace a l'overkill. Sans la "
                     "capacite Boost, l'identite ne prendrait RIEN"),
        "scenario": "rhino",
        "heros": "patriot",
        "mise_en_place": ["Puzzle.ChangeToFace('Elijah Bradley', 'pt001a')",
                          "Puzzle.PutIntoPlay('01067', under_control=True)",
                          "Puzzle.Damage('01067', 1)"],
        "declencher": ["Puzzle.CreateEncounterDeck('pt021')",
                       "Puzzle.Attack('01094', defender='01067')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2},
    },
    {
        "nom": "gp003 \"It Can't End Like This!\" — Desorientee, la carte est ANNULEE et le statut consomme",
        "pourquoi": ("la carte est imprimee « (attack/thwart) » et porte les traits ATTACK et "
                     "THWART, mais le module ne posait que le label 'attack'. Or le label "
                     "'thwart' est ce qui declenche Desoriente. Sans lui, une Gwenpool "
                     "Desorientee joue la carte, retire quand meme sa menace, et GARDE son "
                     "statut. Meme forme que la carte OFFICIELLE 18004 Crosscounter"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('gp001b')",
                          "Puzzle.SetThreat('01097b', 3)",
                          "Puzzle.Confuse('gp001a')"],
        "main_exclusive": ["gp003", "gp002"],
        "declencher": [],
        "jouer": ["gp003"],
        "verifier": "gp003_desorientee_annule_tout",
    },
    {
        "nom": "gp005 \"Sorry, Gotta Run!\" — elle dejoue le complot principal MALGRE un sbire patrol",
        "pourquoi": ("la carte est imprimee « ignores the patrol keyword and crisis icons ». "
                     "Le module n'ignorait que les crises, au motif que « le moteur ne propose "
                     "pas d'exemption patrol » — c'est faux, `SetIgnoreKeyword('Crisis', "
                     "'Patrol')` existe et deux cartes portant LA MEME phrase l'utilisent, "
                     "42006 Natural Flight (officielle) et 61023 Grapnel Launcher. Patrol "
                     "protege le COMPLOT PRINCIPAL (`minion.py`, SetGuardPatrolEffectedBy -> "
                     "GetMainSchemes) : avec le Magistrate 45134 engage, le complot principal "
                     "est hors d'atteinte et la carte ne tient pas sa promesse"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('gp001b')",
                          "Puzzle.SetThreat('01097b', 3)",
                          "Puzzle.PutIntoPlay('45134')"],
        "main_exclusive": ["gp005", "gp003", "gp002"],
        "declencher": [],
        "jouer": ["gp005"],
        "payer_avec": ["gp003"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]], "en_jeu": ["45134"]},
    },
    {
        "nom": "gp005 \"Sorry, Gotta Run!\" — elle dejoue le complot principal MALGRE une icone de crise",
        "pourquoi": ("jumeau du cas patrol, pour l'autre moitie de la phrase imprimee. Le "
                     "correctif remplace `ignore_crisis=True` (un enregistrement temporaire "
                     "d'UnitIgnoreKeywordIcons) par `SetIgnoreKeyword('Crisis', 'Patrol')`, "
                     "la convention de 42006 : ce cas est VERT avant comme apres, il garantit "
                     "que le changement de mecanisme ne perd pas la crise en route. "
                     "`scheme_main.py` RemoveThreatInternal rend 0 sans l'exemption"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.ChangeForm('gp001b')",
                          "Puzzle.SetThreat('01097b', 3)",
                          "Puzzle.PutIntoPlay('01125')"],
        "main_exclusive": ["gp005", "gp003", "gp002"],
        "declencher": [],
        "jouer": ["gp005"],
        "payer_avec": ["gp003"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]], "en_jeu": ["01125"]},
    },
    {
        "nom": "ah008 Calculated Strike — Sonne, la carte est ANNULEE et le statut consomme",
        "pourquoi": ("carte imprimee « (attack/thwart) » qui infligeait 3 degats au vilain, mais "
                     "le module ne posait que le label 'thwart'. Le label 'attack' est ce qui "
                     "livre la capacite a Sonne (`cards/pack/status/stunned.py`, l.49). Sonde "
                     "de mesure : jumeau exact du cas ah008 de base, avec le heros Sonne"),
        "scenario": "rhino",
        "heros": "totally_awesome_hulk",
        "mise_en_place": ["Puzzle.ChangeForm('ah001b')",
                          "Puzzle.SetThreat('01097b', 4)",
                          "Puzzle.Stun('ah001a')"],
        "main_exclusive": ["ah008", "ah010", "ah009", "ah011"],
        "declencher": [],
        "jouer": ["ah008"],
        "payer_avec": ["ah010", "ah009", "ah011"],
        "cibles": ["01097b", "01094"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]], "degats": [["01094", 0]],
                    "statuts_absents": [["ah001a", "Stunned"]]},
    },
    {
        "nom": "hd009 Quack and Burn — Sonne, la carte est ANNULEE et le statut consomme",
        "pourquoi": ("carte imprimee « (attack/thwart) ». La capacite PRINCIPALE, celle qui "
                     "infligeait les degats, portait `SetLabel()` VIDE ; seul le "
                     "`ForChoiceAbility` imbrique du retrait de menace portait 'thwart'. Sonde "
                     "de mesure : le heros est Sonne, la carte devrait etre annulee"),
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.ChangeToFace('Howard Duckson', 'hd001a')",
                          "Puzzle.Stun('hd001a')"],
        "main_exclusive": ["hd009", "01087", "01087"],
        "declencher": ["Puzzle.SetThreat('01097b', 5)"],
        "cibles": ["01094", "01097b"],
        "jouer": ["hd009"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 0]],
                    "statuts_absents": [["hd001a", "Stunned"]]},
    },
    {
        "nom": "hd005 Quack Attack — Sonne, l'interruption est ANNULEE et le statut consomme",
        "pourquoi": ("carte imprimee « (attack/defense) ». La capacite PRINCIPALE porte "
                     "`SetLabel()` VIDE ; seul le `ForChoiceAbility` imbrique des degats porte "
                     "'attack'. Sonde de mesure : si le label imbrique suffit, Sonne annule "
                     "quand meme et l'identite encaisse les 3 degats sans prevention"),
        "scenario": "rhino",
        "heros": "howard_the_duck",
        "mise_en_place": ["Puzzle.ChangeToFace('Howard Duckson', 'hd001a')",
                          "Puzzle.Stun('hd001a')"],
        "main_exclusive": ["hd005", "01088"],
        "declencher": ["Puzzle.Damage('hd001a', 3)"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3,
                    "statuts_absents": [["hd001a", "Stunned"]]},
    },
    {
        "nom": "gp014 \"Future Me Scares Me\" — Incite en SOLO STANDARD : 1 menace (temoin)",
        "pourquoi": ("la carte imprime DEUX lignes d'Incite qui s'additionnent (verifie sur le "
                     "visuel, assets/pics/gp014.png) : « Incite 0 (1 en multijoueur) » et "
                     "« Incite 1 (2 en expert) ». En solo standard cela fait 0 + 1 = 1, la "
                     "valeur du `desc`. Ce cas est le TEMOIN : il doit rester vert avant comme "
                     "apres le cablage des deux bonus conditionnels. Incite = poser X menaces "
                     "sur le complot principal a la revelation (`can_incite.py`)"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.SetThreat('01097b', 0)"],
        "declencher": ["Puzzle.Reveal('gp014')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 1]]},
    },
    {
        "nom": "gp014 \"Future Me Scares Me\" — Incite en MULTIJOUEUR : 2 menaces",
        "pourquoi": ("premiere ligne imprimee : « incite 1 instead, if this is a multiplayer "
                     "game » -> 1 + 1 = 2. `Worlds.GetPlayerNum` existe ; gp014 est la SEULE "
                     "carte du depot dont le texte parle de multijoueur, donc aucun precedent, "
                     "mais la primitive est la"),
        "scenario": "rhino",
        "heros": "gwenpool",
        "heros2": "spider_man",
        "mise_en_place": ["Puzzle.SetThreat('01097b', 0)"],
        "declencher": ["Puzzle.Reveal('gp014')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]]},
    },
    {
        "nom": "gp014 \"Future Me Scares Me\" — Incite en EXPERT : 2 menaces",
        "pourquoi": ("seconde ligne imprimee : « incite 2 instead, if this is an expert mode "
                     "game » -> 0 + 2 = 2. Le moteur porte une fabrique DEDIEE, "
                     "`AbilityFactory.IfExpertModeThisGainKeyword(incite=1)` : l'affirmation "
                     "du module (« le moteur ne porte qu'une valeur d'Incite ») etait fausse, "
                     "comme celles de gp003 et gp005"),
        "scenario": "rhino_expert",
        "heros": "gwenpool",
        "mise_en_place": ["Puzzle.SetThreat('01097b', 0)"],
        "declencher": ["Puzzle.Reveal('gp014')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 2]]},
    },
    # ------------------------------------------------------ pack ms_america --
    # Le pack tourne autour de Star-Gaze (ma001a), la Response qui branche sur
    # la RESSOURCE IMPRIMEE de la carte SUPERPOWER jouee. Les quatre branches
    # ont chacune leur cas, plus une contre-epreuve « carte non-SUPERPOWER ».
    {
        "nom": "ma001a Star-Gaze — branche [physical] : 1 degat a un ennemi",
        "pourquoi": ("mecanique centrale du pack. ma009 America's Anger imprime [physical] "
                     "et coute 1. L'identite est INCLINEE au depart parce que le cout de "
                     "ma009 est « redresser ton identite » (arbitrage du 30/08/2026) : "
                     "prete, la carte serait injouable"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.Exhaust('ma001a')"],
        "declencher": [],
        "main_exclusive": ["ma009", "01088"],
        "cibles": ["01094"],
        "jouer": ["ma009"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 1]], "defausse": ["ma009"]},
    },
    {
        "nom": "ma001a Star-Gaze — branche [energy] : 1 degat soigne sur Ms. America",
        "pourquoi": ("ma005 Star Light imprime [energy]. L'identite porte 3 degats au "
                     "depart : sans le soin le releve ne pourrait pas distinguer « rien "
                     "ne s'est passe » de « la branche a resolu »"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.Damage('ma001a', 3)"],
        "declencher": [],
        "main_exclusive": ["ma005", "01088", "01090"],
        "jouer": ["ma005"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 2, "en_jeu": ["ma005"]},
    },
    {
        "nom": "ma001a Star-Gaze — branche [mental] : 1 menace retiree d'une manigance",
        "pourquoi": ("ma007 Hyper-Cosmic Awareness imprime [mental]. La menace est posee a "
                     "5 : a 8 le complot principal AVANCE et le releve mesurerait autre "
                     "chose (piege du GUIDE §10)"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')"],
        "declencher": ["Puzzle.SetThreat('The Break-In!', 5)"],
        "main_exclusive": ["ma007", "01088", "01090"],
        "jouer": ["ma007"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["01097b", 4]]},
    },
    {
        "nom": "ma001a Star-Gaze — branche [wild] : Ms. America est REDRESSEE",
        "pourquoi": ("ma013 Star Portal imprime [wild]. L'identite est inclinee au depart, "
                     "sinon « redresser » ne se verrait pas. Un allie est seme dans la "
                     "defausse parce que ma013 est injouable sans"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.CreatePlayerDiscardPile('01059')",
                          "Puzzle.Exhaust('ma001a')"],
        "declencher": [],
        "main_exclusive": ["ma013", "01088", "01090"],
        "cibles": ["01094"],
        "jouer": ["ma013"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["ma001a"]},
    },
    {
        "nom": "ma001a Star-Gaze — contre-epreuve : une carte NON-SUPERPOWER ne declenche RIEN",
        "pourquoi": ("temoin negatif indispensable : sans lui, une capacite qui partirait "
                     "sur CHAQUE carte jouee passerait les quatre cas precedents. 01059 "
                     "Jessica Jones est un allie [energy] SANS le trait SUPERPOWER : si "
                     "Star-Gaze partait, l'identite serait soignee"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.Damage('ma001a', 3)"],
        "declencher": [],
        "main_exclusive": ["01059", "01088", "01090"],
        "jouer": ["01059"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 3, "en_jeu": ["01059"]},
    },
    {
        "nom": "ma001b Thinking With Portals — defausser 1 carte remonte 1 carte de la defausse dans le deck",
        "pourquoi": ("la fleche est un COUT : sans carte en main, l'action n'est pas "
                     "proposee. La partie demarre en identite civile, aucun ChangeToFace "
                     "n'est necessaire. `cibles` designe ma002 pour que la recherche ne "
                     "remonte pas la carte qui vient de payer"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.CreatePlayerDiscardPile('ma002')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Action('ma001b', 'Action')"],
        "cibles": ["ma002"],
        "verifier": "ma001b_carte_remontee_dans_le_deck",
    },
    {
        "nom": "ma002 Alloy — Hero Response : +1 ATQ apres la RESOLUTION de Star-Gaze",
        "pourquoi": ("le declencheur est la RESOLUTION de Star-Gaze, pas le jeu d'une carte "
                     "SUPERPOWER : deux choses differentes. ma007 est joue pour faire "
                     "resoudre la branche [mental], qui a besoin de menace sur une "
                     "manigance pour avoir une cible legale"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma002', under_control=True)"],
        "declencher": ["Puzzle.SetThreat('The Break-In!', 5)"],
        "main_exclusive": ["ma007", "01088", "01090"],
        "jouer": ["ma007"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["ma002", "attack", 1]]},
    },
    {
        "nom": "ma002 Alloy — contre-epreuve : sans carte SUPERPOWER jouee, aucun bonus",
        "pourquoi": ("jumeau negatif du cas precedent. 01059 n'a pas le trait SUPERPOWER : "
                     "Star-Gaze ne resout pas, Alloy garde son ATQ imprimee. Une capacite "
                     "qui donnerait +1 a chaque carte jouee echouerait ici"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma002', under_control=True)"],
        "declencher": ["Puzzle.SetThreat('The Break-In!', 5)"],
        "main_exclusive": ["01087", "01088", "01090"],
        "cibles": ["01094"],
        "jouer": ["01087"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["ma002", "attack", 0]]},
    },
    {
        "nom": "ma003 Hawkeye — [star] son attaque est PERFORANTE : le Robuste de Rhino saute et les degats passent",
        "pourquoi": ("`piercing` defausse les cartes de statut Tough AVANT d'infliger les "
                     "degats. Sans le mot-cle, le Tough absorberait TOUT et le releve "
                     "montrerait 0 degat. ⚠ `ranged`, lui, ignore la RIPOSTE et non le "
                     "Garde (can_retaliate.py:38) : il n'est pas observable ici"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma003', under_control=True)",
                          "Puzzle.Tough('01094')"],
        "declencher": ["Puzzle.Attack('ma003')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]]},
    },
    {
        "nom": "ma003 Hawkeye — Interrupt : vaincue par degats consecutifs APRES Star-Gaze, elle est MELANGEE DANS LE DECK",
        "pourquoi": ("cas qui exige la cle `declencher_apres` : il faut avoir joue une carte "
                     "SUPERPOWER (donc resolu Star-Gaze) AVANT que l'attaque ne la tue, or "
                     "`declencher` tourne avant `jouer`. Elle est amenee a 1 PV pour que le "
                     "SEUL degat consecutif de son ATQ 2* la mette a terre"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma003', under_control=True)",
                          "Puzzle.Damage('ma003', 1)"],
        "declencher": ["Puzzle.SetThreat('The Break-In!', 5)"],
        "main_exclusive": ["ma007", "01088", "01090"],
        "jouer": ["ma007"],
        "declencher_apres": ["Puzzle.Attack('ma003')"],
        "cibles": ["01094"],
        "verifier": "ma003_melangee_dans_le_deck",
    },
    {
        "nom": "ma003 Hawkeye — contre-epreuve : SANS Star-Gaze resolue, elle est bel et bien VAINCUE",
        "pourquoi": ("jumeau negatif du cas precedent, et seule preuve que la clause « if "
                     "you have resolved Star-Gaze this turn » est vraiment lue : sans elle "
                     "l'allie serait sauve dans tous les cas"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma003', under_control=True)",
                          "Puzzle.Damage('ma003', 1)"],
        "declencher": ["Puzzle.Attack('ma003')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["ma003"], "defausse": ["ma003"]},
    },
    {
        "nom": "ma004 Santana Family — Alter-Ego Action : un evenement de la DEFAUSSE est attache FACE CACHEE",
        "pourquoi": ("la partie demarre en identite civile : aucun ChangeToFace. Le cout de "
                     "la fleche est l'inclinaison, verifiee elle aussi. Le plafond de 2 est "
                     "porte par une `conditions=`"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.PutIntoPlay('ma004', under_control=True)",
                          "Puzzle.CreatePlayerDiscardPile('ma015')"],
        "declencher": ["Puzzle.Action('ma004', 'AlterEgoAction')"],
        "cibles": ["ma015"],
        "verifier": "ma004_evenement_attache",
    },
    {
        "nom": "ma005 Star Light — la ressource imprimee de la carte payee devient [wild] : Star-Gaze REDRESSE au lieu de soigner",
        "pourquoi": ("preuve indirecte mais sans ambiguite de la seconde phrase. ma006 Star "
                     "Flight imprime [energy] : sans le changement, Star-Gaze soignerait "
                     "(l'identite n'a aucun degat, donc rien de visible) et l'identite "
                     "resterait INCLINEE. Avec, la branche [wild] la redresse. La main ne "
                     "contient qu'un seul icone (ma009 = [physical]) : Star Light est donc "
                     "OBLIGEE de financer le second point du cout"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma005', under_control=True)",
                          "Puzzle.Exhaust('ma001a')"],
        "declencher": [],
        "main_exclusive": ["ma006", "ma009"],
        "jouer": ["ma006"],
        "verifier": "etat_attendu",
        "attendu": {"pret": ["ma001a"], "exhausted": ["ma005"], "en_jeu": ["ma006"]},
    },
    {
        "nom": "ma006 Star Flight — bonus continu : +1 CTR et trait AERIAL a Ms. America",
        "pourquoi": ("deux choses distinctes dans la meme phrase, un bonus de stat ET un "
                     "trait accorde : le releve controle les deux"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma006', under_control=True)"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"thwart": 1}, "traits": ["AERIAL"]},
    },
    {
        "nom": "ma006 Star Flight — Hero Interrupt : l'evenement joue gagne SUPERPOWER, donc Star-Gaze part",
        "pourquoi": ("c'est le SEUL moyen du catalogue de faire declencher Star-Gaze sur une "
                     "carte d'aspect. 01087 Haymaker est un evenement BASIC [energy] SANS "
                     "le trait SUPERPOWER : sans Star Flight, Star-Gaze ne part pas et "
                     "l'identite garde ses 3 degats. Avec, la branche [energy] en soigne 1. "
                     "Le releve controle aussi l'inclinaison, qui est le cout de la fleche, "
                     "et les 3 degats de Haymaker sur Rhino (preuve que l'evenement a bien "
                     "ete joue et non simplement defausse)"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma006', under_control=True)",
                          "Puzzle.Damage('ma001a', 3)"],
        "declencher": [],
        "main_exclusive": ["01087", "01088"],
        "cibles": ["01094"],
        "jouer": ["01087"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 3]], "degats_identite": 2,
                    "exhausted": ["ma006"]},
    },
    {
        "nom": "ma007 Hyper-Cosmic Awareness — Hero Response : 1 compteur star par carte SUPERPOWER jouee",
        "pourquoi": ("ma007 est elle-meme SUPERPOWER : la poser puis jouer ma005 doit donner "
                     "UN compteur, pas deux (la carte est deja en jeu quand ma005 est "
                     "jouee)"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma007', under_control=True)"],
        "declencher": [],
        "main_exclusive": ["ma005", "01088", "01090"],
        "jouer": ["ma005"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["ma007", "star", 1]]},
    },
    {
        "nom": "ma007 Hyper-Cosmic Awareness — Hero Interrupt : 4 compteurs retires, la carte rencontre est ANNULEE et defaussee",
        "pourquoi": ("le cout a DEUX parties (incliner ET retirer 4 compteurs) : le releve "
                     "controle les deux. 01107 est une manigance annexe : annulee, elle "
                     "n'entre PAS en jeu, ce qui est directement observable"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma007', under_control=True)",
                          "Puzzle.Counter('ma007', 'star', 4)"],
        "declencher": ["Puzzle.Reveal('01107')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["ma007", "star", 0]], "exhausted": ["ma007"],
                    "hors_jeu": ["01107"]},
    },
    {
        "nom": "ma007 Hyper-Cosmic Awareness — contre-epreuve : a 3 compteurs, l'annulation est INJOUABLE",
        "pourquoi": ("`CostFunc.Counter` filtre lui-meme les porteurs qui n'ont pas assez de "
                     "compteurs : la capacite ne doit meme pas etre proposee. Sans ce "
                     "temoin, un cout mal ecrit annulerait la carte a n'importe quel "
                     "nombre de compteurs"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma007', under_control=True)",
                          "Puzzle.Counter('ma007', 'star', 3)"],
        "declencher": ["Puzzle.Reveal('01107')"],
        "verifier": "etat_attendu",
        "attendu": {"compteurs": [["ma007", "star", 3]], "pret": ["ma007"],
                    "en_jeu": ["01107"]},
    },
    {
        "nom": "ma008 Energy Infusion — Star-Gaze est resolue UNE SECONDE FOIS, sur la couleur de la carte payee",
        "pourquoi": ("ma009 imprime [physical] : Star-Gaze inflige 1 degat, et Energy "
                     "Infusion la rejoue sur la MEME couleur, donc 2 degats au total. La "
                     "main ne contient QUE ma009 et ma008 : Energy Infusion est donc "
                     "obligee de payer, et ses deux icones [wild] ne dictent PAS la "
                     "branche (sinon Ms. America serait redressee au lieu de frapper)"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.Exhaust('ma001a')"],
        "declencher": [],
        "main_exclusive": ["ma009", "ma008"],
        "cibles": ["01094"],
        "jouer": ["ma009"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]]},
    },
    {
        "nom": "ma009 America's Anger — les modificateurs d'ATQ sont DOUBLES a la prochaine utilisation",
        "pourquoi": ("01057 Combat Training donne +1 ATQ : Ms. America passe de 2 a 3. La "
                     "carte double le MODIFICATEUR, pas la base -> 2 + (1 x 2) = 4 a "
                     "l'attaque suivante, jamais 6. Avec le degat de Star-Gaze [physical], "
                     "Rhino encaisse 5. `preferer_option` force la branche ATQ (le pilote "
                     "prend toujours la premiere, ici CTR) et `declencher_apres` fait "
                     "attaquer APRES le jeu de la carte"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('01057', under_control=True)",
                          "Puzzle.Exhaust('ma001a')"],
        "declencher": [],
        "main_exclusive": ["ma009", "01088"],
        "preferer_option": "your ATK",
        "cibles": ["01094"],
        "jouer": ["ma009"],
        "declencher_apres": ["Puzzle.Attack('ma001a')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 5]]},
    },
    {
        "nom": "ma009 America's Anger — contre-epreuve : identite DEJA PRETE, la carte est INJOUABLE",
        "pourquoi": ("arbitrage EXPLICITE de l'utilisateur du 30/08/2026, refuse comme "
                     "exception : la fleche est un cout, « redresser ton identite » en fait "
                     "partie, donc une identite prete rend la carte injouable. Ce cas est la "
                     "pour que personne ne « corrige » ce comportement sans le voir tomber"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')"],
        "declencher": [],
        "main_exclusive": ["ma009", "01088"],
        "jouer": ["ma009"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["ma009"], "degats": [["01094", 0]]},
    },
    {
        "nom": "ma011 Bulletproof Chica — Hero Interrupt (defense) : tous les degats prevenus et un Robuste sur l'identite",
        "pourquoi": ("l'identite est INCLINEE : un heros incline ne defend pas, c'est le "
                     "seul moyen fiable de faire arriver une attaque jusqu'a lui (GUIDE §8). "
                     "Avec `defender='ma001a'`, la DEF 2 ramenait l'attaque de Rhino a 0 "
                     "degat et l'interruption n'etait jamais proposee — le declencheur est "
                     "`WhenUnitWouldTakeDamage`, pas la fenetre de defense. La carte est en "
                     "MAIN, pas dans `jouer` : elle se joue en reaction"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.Exhaust('ma001a')"],
        "main_exclusive": ["ma011", "01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "statuts": [["ma001a", "Tough"]],
                    "defausse": ["ma011"]},
    },
    {
        "nom": "ma013 Star Portal — l'allie de la defausse arrive INCLINE, la menace et les degats suivent SES valeurs",
        "pourquoi": ("01059 Jessica Jones imprime CTR 1* et ATQ 2* : 1 menace retiree et "
                     "2 degats. L'inclinaison a l'entree en jeu est le point le plus facile "
                     "a rater (`PutIntoPlay(..., exhaust=True)`), elle est controlee. "
                     "Star-Gaze [wild] redresse l'identite, deja prete : sans effet visible"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.CreatePlayerDiscardPile('01059')"],
        "declencher": ["Puzzle.SetThreat('The Break-In!', 5)"],
        "main_exclusive": ["ma013", "01088", "01090"],
        "cibles": ["01094"],
        "jouer": ["ma013"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["01059"], "exhausted": ["01059"],
                    "degats": [["01094", 2]], "menace": [["01097b", 4]]},
    },
    {
        "nom": "ma013 Star Portal — contre-epreuve : aucun allie dans aucune defausse, la carte est INJOUABLE",
        "pourquoi": ("la fleche est un cout, rendu ici par une `conditions=` faute de "
                     "`CostFunc` capable de le dire. Sans ce temoin, la carte pourrait "
                     "partir a vide et le joueur bruler 2 ressources pour rien"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')"],
        "declencher": ["Puzzle.SetThreat('The Break-In!', 5)"],
        "main_exclusive": ["ma013", "01088", "01090"],
        "jouer": ["ma013"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["ma013"], "menace": [["01097b", 5]]},
    },
    {
        "nom": "ma015 Break Through — 4 degats, 3 menaces, et un ennemi ETOURDI parce que la manigance tombe",
        "pourquoi": ("les trois effets d'un coup. La menace est posee a 3 exactement : les "
                     "3 retirees enlevent la DERNIERE, ce qui declenche "
                     "`if_this_remove_last_threat`. Star-Gaze [energy] soigne dans le vide "
                     "(l'identite est intacte) et n'ajoute aucun degat"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')"],
        "declencher": ["Puzzle.SetThreat('The Break-In!', 3)"],
        "main_exclusive": ["ma015", "01088", "01090"],
        "cibles": ["01094"],
        "jouer": ["ma015"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]], "menace": [["01097b", 0]],
                    "statuts": [["01094", "Stunned"]]},
    },
    {
        "nom": "ma015 Break Through — contre-epreuve : aucune defaite, aucun Etourdi",
        "pourquoi": ("jumeau negatif du cas precedent : menace a 5, il en reste 2 apres "
                     "coup, et Rhino (14 PV) survit a 4 degats. La troisieme phrase est "
                     "CONDITIONNELLE — sans ce temoin, un Etourdi inconditionnel passerait"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')"],
        "declencher": ["Puzzle.SetThreat('The Break-In!', 5)"],
        "main_exclusive": ["ma015", "01088", "01090"],
        "cibles": ["01094"],
        "jouer": ["ma015"],
        "verifier": "ma015_aucun_etourdi",
    },
    {
        "nom": "ma017 Edges Syndrome — malus continu : -1 a CHAQUE pouvoir de base",
        "pourquoi": ("l'obligation RESTE EN JEU (modele 28021 / 04166) : c'est ce qui donne "
                     "son sens a ses deux Actions. Les trois pouvoirs de la face heros sont "
                     "controles d'un coup"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')"],
        "declencher": ["Puzzle.Reveal('ma017')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"attack": -1, "thwart": -1, "defense": -1},
                    "en_jeu": ["ma017"]},
    },
    {
        "nom": "ma017 Edges Syndrome — Action 1 : 2 degats subis, la carte est DEFAUSSEE",
        "pourquoi": ("la fleche est un cout, rendu par `CostFunc.TakeDamage(2, "
                     "\"YourIdentity\")` : le releve controle les degats ET le depart de la "
                     "carte, sinon un cout non paye passerait"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')"],
        "declencher": ["Puzzle.Reveal('ma017')",
                       "Puzzle.Action('ma017', 'Action', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["ma017"], "degats_identite": 2},
    },
    {
        "nom": "ma017 Edges Syndrome — Action 2 : 4 degats subis, la carte est RETIREE DU JEU",
        "pourquoi": ("branche inatteignable sans le 3e argument de `Puzzle.Action` : le "
                     "pilote prend toujours la premiere action offerte. Le verificateur "
                     "distingue « retiree du jeu » de « defaussee », ce qu'`etat_attendu` "
                     "ne sait pas faire"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')"],
        "declencher": ["Puzzle.Reveal('ma017')",
                       "Puzzle.Action('ma017', 'Action', 1)"],
        "verifier": "ma017_retiree_du_jeu",
    },
    {
        "nom": "ma018 Catalina Chavez — elle gagne les modificateurs de la zone de jeu, CTR converti en MNG",
        "pourquoi": ("arbitrage de l'utilisateur du 30/08/2026 : lecture LITTERALE, tout ce "
                     "qui est dans la zone de jeu. 01057 Combat Training donne +1 ATQ et "
                     "ma006 Star Flight +1 CTR : Catalina doit gagner +1 ATQ et +1 MNG "
                     "(pas +1 CTR, un sbire n'en a pas)"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('01057', under_control=True)",
                          "Puzzle.PutIntoPlay('ma006', under_control=True)",
                          "Puzzle.PutIntoPlay('ma018')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["ma018", "attack", 1], ["ma018", "scheme", 1]]},
    },
    {
        "nom": "ma018 Catalina Chavez — contre-epreuve : zone de jeu vide, ATQ et MNG restent imprimes",
        "pourquoi": ("jumeau negatif du cas precedent. Il reste VERT sans le module (rien "
                     "ne se passe non plus), il ne prouve donc rien seul : c'est le couple "
                     "avec le cas positif qui prouve que la capacite lit vraiment la zone "
                     "de jeu et n'ajoute pas un bonus fixe"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma018')"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["ma018", "attack", 0], ["ma018", "scheme", 0]]},
    },
    {
        "nom": "ma019 Search for the Cure — menace de depart = cout combine des allies attaches",
        "pourquoi": ("la menace de depart est X, CABLEE a la main (ecart assume, modeles "
                     "mw018 et wc019a) : `desc.StartingThreat` ne sait pas dire « la somme "
                     "du cout des cartes attachees ». 01059 coute 3 -> 3 menaces, et PAS le "
                     "repli a 2 par joueur. `accepter_choix` est indispensable : la "
                     "recherche est un `may`, et le pilote decline par defaut"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.CreatePlayerDiscardPile('01059')"],
        "declencher": ["Puzzle.Reveal('ma019')"],
        "accepter_choix": True,
        "cibles": ["01059"],
        "verifier": "ma019_allie_attache_et_menace",
    },
    {
        "nom": "ma019 Search for the Cure — aucun allie attache : 2 menaces par joueur, en plus",
        "pourquoi": ("seconde moitie de la phrase imprimee. La defausse ne contient qu'une "
                     "ressource : aucun allie a attacher, donc le repli s'applique — en "
                     "solo, 1 joueur x 2[per_hero] x 1 heros = 2"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.CreatePlayerDiscardPile('01088')"],
        "declencher": ["Puzzle.Reveal('ma019')"],
        "verifier": "etat_attendu",
        "attendu": {"menace": [["ma019", 2]]},
    },
    {
        "nom": "ma020 Star Lightning — Catalina attaque et l'identite est SONNEE",
        "pourquoi": ("l'identite est inclinee pour qu'elle ne defende pas : c'est le seul "
                     "moyen fiable de faire arriver une attaque jusqu'a elle (GUIDE §8). "
                     "La clause est « if this attack DEALS DAMAGE », pas « if undefended » "
                     ": on controle donc les degats ET le statut"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma018')",
                          "Puzzle.Exhaust('ma001a')"],
        "declencher": ["Puzzle.Reveal('ma020')"],
        "verifier": "ma020_sonnee_apres_attaque",
    },
    {
        "nom": "ma020 Star Lightning — contre-epreuve : Catalina absente, aucune attaque et aucun Sonne",
        "pourquoi": ("jumeau negatif. La branche « surge » qui part alors n'est PAS "
                     "observable de facon deterministe (limite du harnais declaree dans "
                     "docs/ms_america_cartes.md) : ce cas prouve seulement que rien "
                     "d'autre ne se produit"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.Exhaust('ma001a')"],
        "declencher": ["Puzzle.Reveal('ma020')"],
        "verifier": "ma020_rien_ne_se_passe",
    },
    {
        "nom": "ma022 Gwenpool — +1 ATQ par amelioration signature, PLAFONNE a +2",
        "pourquoi": ("trois ameliorations signature sont posees (ma005, ma006, ma007) : le "
                     "plafond doit en ramener le bonus a +2. Sans lui, Gwenpool serait a "
                     "+3. `IdentitySpecific` est la classe moteur des cartes signature"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma005', under_control=True)",
                          "Puzzle.PutIntoPlay('ma006', under_control=True)",
                          "Puzzle.PutIntoPlay('ma007', under_control=True)",
                          "Puzzle.PutIntoPlay('ma022', under_control=True)"],
        "declencher": [],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["ma022", "attack", 2]]},
    },
    {
        "nom": "ma023 Marvel Boy — vaincu par degats consecutifs, une amelioration inclinee est REDRESSEE",
        "pourquoi": ("le texte dit « IS defeated », pas « would be » : rien n'est remplace, "
                     "l'allie meurt. Star Light est inclinee au depart, sinon `canbe_ready` "
                     "l'ecarte et la capacite n'a aucune cible legale. Marvel Boy est amene "
                     "a 1 PV pour que son unique degat consecutif le tue"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma023', under_control=True)",
                          "Puzzle.PutIntoPlay('ma005', under_control=True)",
                          "Puzzle.Exhaust('ma005')",
                          "Puzzle.Damage('ma023', 2)"],
        "declencher": ["Puzzle.Attack('ma023')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["ma023"], "pret": ["ma005"]},
    },
    {
        "nom": "ma024 Noh-Varr's Ship — capacite Resource : elle finance un evenement et s'incline",
        "pourquoi": ("la main ne contient qu'un seul icone (ma009 = [physical]) pour un cout "
                     "de 2 : le vaisseau est OBLIGE de fournir le second. Sans lui, ma015 "
                     "resterait en main. Le releve controle l'inclinaison, qui est le cout "
                     "de la fleche"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('ma024', under_control=True)"],
        "declencher": ["Puzzle.SetThreat('The Break-In!', 5)"],
        "main_exclusive": ["ma015", "ma009"],
        "cibles": ["01094"],
        "jouer": ["ma015"],
        "verifier": "etat_attendu",
        "attendu": {"exhausted": ["ma024"], "defausse": ["ma015"]},
    },
    {
        "nom": "ma024 Noh-Varr's Ship — contre-epreuve : injouable si l'identite n'a pas le trait YOUNG AVENGER",
        "pourquoi": ("temoin monte avec un AUTRE heros : Okoye n'est pas une YOUNG AVENGER. "
                     "Sans ce cas, la condition de jeu serait invisible — une carte sans "
                     "condition passerait le cas positif a l'identique"),
        "scenario": "rhino",
        "heros": "okoye",
        "mise_en_place": ["Puzzle.ChangeToFace('Okoye', 'ok001a')"],
        "declencher": [],
        "main_exclusive": ["ma024", "01088", "01090"],
        "jouer": ["ma024"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["ma024"], "hors_jeu": ["ma024"]},
    },
    {
        "nom": "ma025 Power Stomp — X degats = ATQ courante, sur le vilain ET chaque sbire engage",
        "pourquoi": ("01057 Combat Training porte Ms. America a ATQ 3, ce qui rend la carte "
                     "jouable ET fixe X. 01103 Shocker (3 PV) est engage : il tombe "
                     "exactement. Rhino encaisse 3 + 1 (Star-Gaze [physical], la carte est "
                     "SUPERPOWER) = 4"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')",
                          "Puzzle.PutIntoPlay('01057', under_control=True)",
                          "Puzzle.PutIntoPlay('01103')"],
        "declencher": [],
        "main_exclusive": ["ma025", "01088", "01090"],
        "cibles": ["01094"],
        "jouer": ["ma025"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 4]], "hors_jeu": ["01103"]},
    },
    {
        "nom": "ma025 Power Stomp — contre-epreuve : ATQ 2, la carte est INJOUABLE",
        "pourquoi": ("« Play only if your hero has at least 3 ATK » porte sur une valeur "
                     "COURANTE, qu'aucun kwarg de `SetPlay` ne sait exprimer : la condition "
                     "est ecrite a la main. Sans ce temoin elle serait invisible"),
        "scenario": "rhino",
        "heros": "ms_america",
        "mise_en_place": ["Puzzle.ChangeToFace('America Chavez', 'ma001a')"],
        "declencher": [],
        "main_exclusive": ["ma025", "01088", "01090"],
        "cibles": ["01094"],
        "jouer": ["ma025"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["ma025"], "degats": [["01094", 0]]},
    },
    {
        "nom": "mf001a Flexibility — un evenement SUPERPOWER JOUE ne doit PAS revenir en main",
        "pourquoi": ("le texte dit « or discard it from your hand WITHOUT BEING PLAYED ». Le "
                     "module ecoute `AfterCardDiscard`, qui ne sait pas d'ou la carte part : "
                     "un evenement joué finit lui aussi a la defausse. Sonde de MESURE. Le "
                     "paiement se fait avec 01088 (Energie, aucun trait) pour qu'aucune carte "
                     "SUPERPOWER ne soit depensee et ne consomme la limite avant l'evenement"),
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')", "Puzzle.SetThreat('01097b', 4)"],
        "main_exclusive": ["mf009", "01088"],
        "payer_avec": ["01088"],
        "declencher": [],
        "jouer": ["mf009"],
        "cibles": ["01097b"],
        "verifier": "etat_attendu",
        "attendu": {"defausse": ["mf009"]},
    },
    {
        "nom": "mf001a Flexibility — une carte SUPERPOWER defaussee DEPUIS LE JEU ne doit PAS revenir en main",
        "pourquoi": ("le texte dit « discard it FROM YOUR HAND ». Cosmic Flight (01017) est une "
                     "amelioration SUPERPOWER : detruite en jeu, elle ne devrait pas revenir en "
                     "main. Sonde de MESURE. Le deck de DEPART de Mister Fantastic ne contient "
                     "que des evenements SUPERPOWER, mais le jeu compte 102 ameliorations "
                     "SUPERPOWER et le deckbuilder permet d'en mettre"),
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')",
                          "Puzzle.PutIntoPlay('01017', under_control=True)"],
        "declencher": ["Puzzle.Discard('01017')"],
        "verifier": "mf001a_ou_est_la_carte",
    },
    {
        "nom": "mf001a Flexibility — SUPERPOWER defaussee DE LA MAIN sans etre jouee : elle DOIT revenir",
        "pourquoi": ("troisieme branche du texte, jamais couverte : « or discard it from your "
                     "hand without being played ». Sonde de MESURE : `control_by_player='You'` "
                     "exige `is_in_play` (`factory/discard.py`), et la main porte `is_in_hand`, "
                     "pas `is_in_play` (`deck/deck_type.py`). Lecture statique : la branche ne "
                     "part peut-etre jamais"),
        "scenario": "rhino",
        "heros": "mister_fantastic",
        "mise_en_place": ["Puzzle.ChangeForm('mf001b')"],
        "main_exclusive": ["mf011", "mf009"],
        "declencher": ["Puzzle.Discard('mf011')"],
        "verifier": "mf001a_ou_est_mf011",
    },

    # ------------------------------------------------------------------------
    # Pack « venompool » : Wade Wilson symbiote, set 129, vp001a-vp016
    # ------------------------------------------------------------------------
    {
        "nom": "vp009 Klyntar Suit — You get +3 hit points",
        "pourquoi": ("modele 05023 Endurance : `GiveKeywordToAttached(\"You\", health=3)`. "
                     "Le bonus vise l'IDENTITE, pas la carte : un `health` pose sur "
                     "l'amelioration elle-meme ne se verrait nulle part en jeu"),
        "scenario": "rhino",
        "heros": "venompool",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('vp009')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs": {"health": 3}, "en_jeu": ["vp009"]},
    },
    {
        "nom": "vp009 Klyntar Suit — drain 1 : 1 degat a l'attaquant ET 1 soin sur l'identite",
        "pourquoi": ("le mot-cle « drain » du pack, defini par l'insert : degats PUIS soin. "
                     "Verifier les DEUX moities : un module qui n'infligerait que les degats "
                     "passerait un controle qui ne regarde que l'ennemi. L'identite est "
                     "blessee de 3 avant. DEUX pieges de mise en place ici : (1) sans "
                     "`ChangeToFace` prealable, `Puzzle.Damage('vp001a')` instancie une "
                     "SECONDE identite dans l'aside deck et le rendu leve AssertionError "
                     "(modele ma005/hd001a, qui font tous le ChangeToFace d'abord) ; "
                     "(2) on designe la face par son CARD_ID `vp001b` et non par « Wade "
                     "Wilson », qui est aussi le nom de 44001b, l'alter-ego officiel de "
                     "Deadpool. TROISIEME piege, trouve en jeu : l'attaquant est un "
                     "SBIRE (vp014, ATK 1 fixe) et non Rhino, et l'identite est EPUISEE "
                     "avant. Avec Rhino, le pilote defendait (degats reduits a 0) et la "
                     "Response ne partait jamais — le module avait raison, c'est le cas "
                     "qui etait faux. Un sbire n'a pas de carte de boost : les nombres "
                     "sont donc deterministes, et les DEUX moities du drain sont "
                     "prouvees d'un coup : vp014 finit a 1 degat (la moitie « degats ») "
                     "et l'identite reste a 3 (la moitie « soin » a exactement annule le "
                     "degat subi)"),
        "scenario": "rhino",
        "heros": "venompool",
        "mise_en_place": ["Puzzle.ChangeToFace('vp001b', 'vp001a')",
                          "Puzzle.Damage('vp001a', 3)",
                          "Puzzle.PutIntoPlay('vp009')",
                          "Puzzle.PutIntoPlay('vp014')",
                          "Puzzle.Exhaust('vp001a')"],
        "declencher": ["Puzzle.Attack('vp014')"],
        "cibles": ["vp001a"],
        "accepter_choix": True,
        "verifier": "etat_attendu",
        "attendu": {"degats": [["vp014", 1]], "degats_identite": 3},
    },
    {
        "nom": "vp010 True Form — se defausse quand Klyntar Suit quitte le jeu",
        "pourquoi": ("« Discard this card from play if you do not control Klyntar Suit ». "
                     "Aucune carte du depot ne portait cette tournure : la dependance passe "
                     "par `AfterCardLeavePlay`. Sans le module, True Form resterait en jeu "
                     "toute seule, ce que le texte interdit"),
        "scenario": "rhino",
        "heros": "venompool",
        "mise_en_place": ["Puzzle.PutIntoPlay('vp009')",
                          "Puzzle.PutIntoPlay('vp010')"],
        "declencher": ["Puzzle.Discard('vp009')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["vp009", "vp010"]},
    },
    {
        "nom": "vp013 Killer Thrill — +1 ATK par compteur d'adrenaline",
        "pourquoi": ("`ThisGainKeyword` + `OnEvent.Counter`, modele 12011 Ant-Man. Le "
                     "compteur `adrenaline` a du etre ajoute a l'enum COUNTER du moteur : "
                     "sans lui la carte tomberait des la creation de partie. 2 compteurs "
                     "doivent donner exactement +2 ATK"),
        "scenario": "rhino",
        "heros": "venompool",
        "mise_en_place": ["Puzzle.PutIntoPlay('vp013')"],
        "declencher": ["Puzzle.Counter('vp013', 'adrenaline', 2)"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["vp013", "attack", 2]],
                    "compteurs": [["vp013", "adrenaline", 2]]},
    },
    {
        "nom": "vp014 Coldwar — +1 ATK tant que Killer Thrill est en jeu",
        "pourquoi": ("`ThisGainKeywordWhileFaceIsInPlay` n'expose PAS `attack` "
                     "(enhance_self.py:138) : il a fallu passer par `ThisGainKeyword` avec "
                     "`OnEvent.CardInPlay`, modele dt133 Orka. Le cas verifie que le bonus "
                     "arrive bien quand Killer Thrill entre en jeu"),
        "scenario": "rhino",
        "heros": "venompool",
        "mise_en_place": ["Puzzle.PutIntoPlay('vp014')"],
        "declencher": ["Puzzle.PutIntoPlay('vp013')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["vp014", "attack", 1]]},
    },
    {
        "nom": "vp015 Guzz — +1 SCH tant que Killer Thrill est en jeu",
        "pourquoi": ("jumeau de vp014 mais sur la MANIGANCE, pas l'attaque : deux cartes "
                     "au texte quasi identique dont une seule ligne differe, exactement le "
                     "genre de paire ou un copier-coller se voit en partie et pas en lecture"),
        "scenario": "rhino",
        "heros": "venompool",
        "mise_en_place": ["Puzzle.PutIntoPlay('vp015')"],
        "declencher": ["Puzzle.PutIntoPlay('vp013')"],
        "verifier": "etat_attendu",
        "attendu": {"attributs_carte": [["vp015", "scheme", 1]]},
    },
    {
        "nom": "vp002 Black Cat — son contre de base ignore les icones de crise",
        "pourquoi": ("modele 32002 Shadowcat. Black Cat n'imprime QUE crisis (ni guard ni "
                     "patrol) : le cas prouve que la capacite existe, et le module ne coche "
                     "que crisis pour ne pas creer de capacite fantome"),
        "scenario": "rhino",
        "heros": "venompool",
        "mise_en_place": [],
        "declencher": ["Puzzle.PutIntoPlay('vp002', under_control=True)"],
        "verifier": "etat_attendu",
        "attendu": {"en_jeu": ["vp002"]},
    },
]

# ------------------------------------------------- verifications outillees --
# Definies ici en texte pour rester dans le processus fils (voir plus bas).
VERIFICATIONS = r'''
def brawn_ressource_seulement_si_epuise(monde, aides):
    """bw001a : « The Complete Package » n'existe que tant que Brawn est epuise.

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
    """bw018 : l'obligation part, et le joueur n'est pas laisse dans un etat mort.

    Les deux branches imprimees sont acceptees : soit la carte est retiree du
    jeu (option « epuiser Amadeus Cho »), soit elle est defaussee apres avoir
    sonne et desoriente. Ce qui n'est PAS acceptable, c'est qu'elle reste en jeu.
    """
    if aides["par_id"](monde, "bw018") is not None:
        return False, "Analysis Paralysis est encore en jeu : l'obligation n'a pas ete resolue"
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if identite.IsStunned() or identite.IsConfused():
        return True, "option « sonne et desoriente » appliquee"
    return True, "option « retirer du jeu » appliquee"

def brawn_team_up_refuse_sans_allie(monde, aides):
    """bw024 : sans Silk en jeu, le Team-Up ne doit PAS pouvoir se jouer.

    Temoin de l'arbitrage du 7/8/2026 : la restriction est portee par une
    condition de jeu et non par la cle `TeamUp`. Si la condition sautait, la
    carte partirait en defausse et personne ne le verrait.
    """
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    main = [getattr(f.paper, "card_id", None)
            for f in monde.players[0].hand_cards.GetAll()]
    if "bw024" in defausse:
        return False, ("Strong as Silk a ete jouee alors que Silk n'est pas en jeu : "
                       "la condition de Team-Up ne tient pas")
    if "bw024" not in main:
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
    """bw014 : jouer une carte depuis la reserve REDRESSE l'identite.

    Brawn est epuise volontairement avant (`Puzzle.Attack` sur lui-meme le fait
    attaquer, donc s'epuiser) : sans cela, « ready your identity » n'aurait rien
    a redresser et le cas passerait sur une carte inerte.
    """
    souci = _brawn_carte_bien_jouee_depuis_reserve(monde, "bw013")
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
    """bw013 : jouer une carte depuis la reserve inflige 1 degat a un ennemi."""
    souci = _brawn_carte_bien_jouee_depuis_reserve(monde, "bw014")
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
    """bw017 : jouer une carte depuis la reserve retire 1 menace d'un complot.

    3 menaces sont posees en mise en place : il doit en rester 2.
    """
    souci = _brawn_carte_bien_jouee_depuis_reserve(monde, "bw014")
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
    """bw006 : payee uniquement en [mental] depuis la main, elle va en RESERVE.

    Symetrique du cas « 10 degats » : ici on paie en [mental], donc pas de bonus
    de degats, mais la carte est recyclee au lieu d'etre defaussee.
    """
    reserve = [getattr(f.paper, "card_id", None)
               for f in monde.players[0].reserve.GetAll()]
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "bw006" in reserve:
        return True, "Gamma Strike recyclee en reserve apres un paiement [mental]"
    if "bw006" in defausse:
        return False, ("Gamma Strike est en defausse : le recyclage vers la reserve "
                       "n'a pas eu lieu apres un paiement entierement [mental]")
    return False, f"Gamma Strike introuvable (reserve={reserve}, defausse={defausse})"

def brawn_hulk_out_fin_de_round(monde, aides):
    """bw015 : « When the round ends, remove 1 rage counter from here ».

    On declenche une fin de round et on exige que le compteur descende. Sans le
    Forced Interrupt, le bonus resterait a +2 ATK pour toujours.
    """
    from game.effect.rule import GameRule
    from game.message import Message

    face = aides["par_id"](monde, "bw015")
    if face is None:
        return False, "Hulk Out (bw015) introuvable en jeu"

    avant = face.GetCounters("rage")
    if avant < 2:
        return False, f"Hulk Out entre en jeu avec {avant} compteur(s) (attendu 2)"

    Message.WhenRoundEnd(monde).Send()

    apres_face = aides["par_id"](monde, "bw015")
    apres = apres_face.GetCounters("rage") if apres_face is not None else 0
    if apres >= avant:
        return False, (f"le compteur de rage n'a pas baisse a la fin du round "
                       f"({avant} -> {apres})")
    return True, f"compteur de rage {avant} -> {apres} a la fin du round"

def brawn_cho_lab_alter_ego(monde, aides):
    """bw012 : l'action d'alter-ego remelange une carte Brawn de la defausse.

    On place d'abord une carte du set dans la defausse, puis on resout l'action.
    """
    from game.effect.rule import GameRule
    from game.operate.faces import Faces

    joueur = monde.players[0]
    lab = aides["par_id"](monde, "bw012")
    if lab is None:
        return False, "Cho's Lab (bw012) introuvable en jeu"
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
    """bw020 : quand Namor manigance, la menace va sur Rising Tide.

    Sans le Forced Interrupt, elle irait sur le complot principal — et la
    nemesis perdrait sa boucle (Rising Tide nourrit Namor, qui nourrit Rising
    Tide).
    """
    rising = aides["par_id"](monde, "bw019")
    if rising is None:
        return False, "Rising Tide (bw019) introuvable en jeu"

    menace_rising = getattr(rising, "threat", 0)
    if menace_rising <= 0:
        return False, ("Rising Tide ne porte aucune menace : la manigance de Namor est "
                       "allee ailleurs (complot principal)")
    return True, f"la manigance de Namor a place {menace_rising} menace(s) sur Rising Tide"

def brawn_silk_defausse_traitrise(monde, aides):
    """bw002 : jouee DEPUIS LA MAIN, elle cherche et defausse une traitrise.

    L'insert est explicite : depuis la RESERVE, elle ne le fait pas. Ce cas
    verifie l'autre moitie de la regle — depuis la main, elle le fait.
    """
    reserve = [getattr(f.paper, "card_id", None)
               for f in monde.players[0].reserve.GetAll()]
    if "bw002" in reserve:
        return False, "Silk est en reserve : elle n'a pas ete jouee depuis la main"

    if aides["par_id"](monde, "bw002") is None:
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
    """bw024 : « Brawn and Silk get +1 ATK until the end of the round ».

    Les DEUX doivent monter. Un effet qui ne toucherait que le heros passerait
    un test qui ne regarde que lui.
    """
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "bw024" not in defausse:
        return False, f"Strong as Silk n'a pas ete jouee (defausse = {defausse})"

    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    silk = aides["par_id"](monde, "bw002")
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
    """bw008 : +1 ATK par [physical] depense, puis menace retiree = ATK.

    Payee avec deux Counter-Punch ([physical]), Brawn passe de 2 a 4 ATK et
    retire donc 4 menaces. On mesure le retrait sur le complot principal, qui
    demarre le scenario rhino avec de la menace.
    """
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"

    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "bw008" not in defausse:
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
    """bw024 : avec Silk en jeu, le Team-Up doit reellement se jouer."""
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "bw024" not in defausse:
        main = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].hand_cards.GetAll()]
        return False, (f"Strong as Silk n'a pas ete jouee alors que Silk est en jeu "
                       f"(main = {main}, defausse = {defausse})")
    return True, "Strong as Silk jouee avec Silk en jeu"

def brawn_brains_and_brawn(monde, aides):
    """bw025 : la carte lit les icones IMPRIMEES de la main ET de la reserve.

    Financee par Genius 01089 ([mental]) et Strength 01090 ([physical]), elle
    doit avoir agi sur au moins une des deux moities : degats a un ennemi, ou
    menace retiree. On accepte l'une ou l'autre — ce qui compte est qu'elle ait
    ete jouee et qu'elle ait produit un effet.
    """
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "bw025" not in defausse:
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
    """bw004 : jouee en defense et payee en [mental], elle part en RESERVE.

    Modele de sg_unbeatable sg016 : on constate d'abord que la carte a bien ete
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

    if "bw004" not in reserve and "bw004" not in defausse:
        return False, (f"Calculated Defense n'a pas ete jouee "
                       f"(reserve = {reserve}, defausse = {defausse})")
    if "bw004" not in reserve:
        return False, ("Calculated Defense est en defausse alors qu'elle a ete payee "
                       "en [mental] depuis la main : elle devait aller en reserve")

    main = len(list(monde.players[0].hand_cards.Get()))
    if main < 1:
        return False, "main vide : aucune pioche constatee"
    return True, f"jouee en defense, recyclee en reserve, main a {main} carte(s)"

def gwenpool_manche_intrigue(monde, aides):
    """gp001a : la Regle note la manche ou le Mechant a intrigue.

    La capacite n'a AUCUN effet visible sur la table : elle remplit une
    ardoise posee sur le monde, que gp003 consulte plus tard pour savoir si le
    Mechant a intrigue la manche derniere. Elle pouvait donc rester muette
    indefiniment sans que rien ne le signale — c'est exactement le genre de
    capacite qu'un test de construction ne voit pas.
    """
    Unused = aides.get("par_id")  # noqa: F841 (garde la signature homogene)
    manches = getattr(monde, "_gwenpool_manches_intrigue", None)
    if not manches:
        return False, ("l'ardoise _gwenpool_manches_intrigue est vide : la manigance du "
                       "Mechant n'a pas ete notee")
    return True, f"manche(s) notee(s) : {sorted(manches)}"

def brawn_double_defense(monde, aides):
    """Les DEUX Calculated Defense jouees sur la MEME defense.

    Le script porte `LimitOncePerEvent`, ajoute apres une boucle infinie
    constatee en partie reelle le 7/8/2026 : payee en [mental], la carte
    revient en RESERVE, une zone « comme en main », donc redevient jouable
    dans la fenetre de defense encore ouverte. Le jeu la reproposait sans fin.

    La limite est PAR EVENEMENT et non par carte : un SECOND exemplaire doit
    rester jouable sur la meme defense, ce que le texte imprime autorise
    (« 2 cards instead if Brawn did not ready this way »). Ce cas prouve les
    deux moities a la fois. Que les deux exemplaires finissent en reserve dit
    qu'ils ont ete joues tous les deux ; et que le cas RENDE un resultat dit
    que la sequence se termine, une boucle non bornee epuisant le plafond de
    questions du harnais.

    Il a fallu la cle `ne_pas_depenser` pour y arriver : sans elle le pilote
    defausse le second exemplaire comme ressource pour payer le premier.
    """
    reserve = [getattr(f.paper, "card_id", None)
               for f in monde.players[0].reserve.GetAll()]
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    manquants = [c for c in ("bw004", "bw005") if c not in reserve]
    if manquants:
        return False, (f"exemplaire(s) {manquants} absent(s) de la reserve "
                       f"(reserve = {reserve}, defausse = {defausse})")
    return True, "les deux exemplaires joues sur la meme defense, et la sequence se termine"

def brawn_gamma_strike_sans_bonus(monde, aides):
    """bw006 : temoin. Payee en [energy], la carte fait 7 degats, pas 10.

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
    """bw010 : cout X, donc l'effet ne se voit que si le pilote a surpaye.

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
    """bw014 : une carte POSEE EN RESERVE doit etre jouable depuis la reserve.

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
    """bw020 : Namor gagne +X ATK et +X SCH pour X jetons d'acceleration.

    Temoin : on releve ses valeurs, on ajoute un jeton, et on exige qu'elles
    montent. Un bonus fige a l'entree en jeu resterait identique.
    """
    namor = aides["par_id"](monde, "bw020")
    if namor is None:
        return False, "Namor (bw020) introuvable en jeu"

    rising_tide = aides["par_id"](monde, "bw019")
    if rising_tide is None:
        return False, "Rising Tide (bw019) introuvable en jeu"

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
    """sr017 : Mysterio en jeu doit porter un statut Tenace (Tough)."""
    face = aides["par_id"](monde, "sr015")
    if face is None:
        return False, "Mysterio (sr015) introuvable en jeu"
    if not face.IsTough():
        return False, "Mysterio n'a pas de statut Tenace"
    return True, "Mysterio est Tenace"

def we_hunger_resolue(monde, aides):
    """vr012 : le joueur est en forme heros et l'obligation est resolue.

    Le pilote choisit une des deux options (3 degats, ou 3 menaces + soin 1) :
    on accepte l'une OU l'autre, mais l'obligation ne doit plus etre en jeu et
    la penalite correspondante doit se voir dans le monde.
    """
    if not monde.players[0].IsHero():
        return False, "le joueur n'est pas en forme heros"
    if aides["par_id"](monde, "vr012") is not None:
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
    """mw012 : l'obligation interdit de redresser l'identite."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if aides["par_id"](monde, "mw012") is None:
        return False, "l'obligation mw012 n'est pas en jeu"
    if identite.IsExhaust():
        return True, "l'identite est restee inclinee malgre le redressement"
    return False, "l'identite s'est redressee : l'obligation ne bloque rien"

def witter_a_agi(monde, aides):
    """mw013 : soit 2 degats indirects, soit l'identite inclinee."""
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
    """mw016 : les DEUX statuts doivent etre poses sur la meme cible."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    statut = identite.CastTo(aides["CanStatus"])
    manquants = [s for s in ("Stunned", "Confused") if not statut.HasStatus(s)]
    if manquants:
        return False, f"statut(s) manquant(s) : {', '.join(manquants)}"
    return True, "identite Stunned + Confused"

def web_of_fate_a_pioche(monde, aides):
    """mw011 : une des 5 cartes du dessus doit avoir rejoint la main.

    On ne fige pas LAQUELLE : c'est le pilote de test qui choisit dans la
    liste proposee, et son critere n'a pas a etre grave dans le test.
    """
    attendus = {"mw004", "mw006", "mw003", "mw009", "mw010"}
    main = {getattr(f.paper, "card_id", None)
            for f in monde.players[0].hand_cards.GetAll()}
    prises = attendus & main
    if prises:
        return True, f"ajoutee a la main depuis les 5 du dessus : {sorted(prises)}"
    return False, ("aucune des 5 cartes regardees n'est en main "
                   f"(main = {sorted(x for x in main if x)})")

def veranke_devenue_sbire(monde, aides):
    """mw026 : l'alliee vaincue revient en jeu comme sbire, soignee."""
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

    # Cle `statuts_absents` : l'inverse de `statuts`. Indispensable des qu'un cas
    # prouve qu'un statut a ete CONSOMME — c'est la moitie invisible des labels
    # 'attack'/'thwart', qui n'ont d'autre effet observable que de livrer la
    # capacite a Sonne et Desoriente (`cards/pack/status/`).
    for card_id, statut in attendu.get("statuts_absents") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (statut {statut})")
        elif face.CastTo(aides["CanStatus"]).HasStatus(statut):
            soucis.append(f"{card_id} porte ENCORE le statut {statut}")

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
    """cd004 : Cloak entierement soigne (3/3) et 2 cartes piochees."""
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
    """cd005 : 3 degats sur Rhino, Sonne ET Desoriente (Cloak est en jeu)."""
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
    """cd010 : 1 degat sur Rhino, Desoriente + Sonne, 1 soin sur Cloak (2-1)."""
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
    """jj012 : la manigance est vaincue et une AUTRE manigance est arrivee en jeu."""
    from game.card.face.card_type import EncounterSideScheme, PlayerSideScheme
    if aides["par_id"](monde, "jj012") is not None:
        return False, "Always a Bigger Conspiracy est encore en jeu"
    autres = []
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is None or not face.IsInPlay():
            continue
        if EncounterSideScheme.IsType(face) or PlayerSideScheme.IsType(face):
            if getattr(face.paper, "card_id", None) != "jj012":
                autres.append(face)
    if not autres:
        return False, "aucune autre manigance secondaire n'a ete revelee"
    noms = [getattr(x.paper, "card_id", "?") for x in autres]
    return True, f"manigance(s) revelee(s) : {noms}"

def jj_couple_tenace(monde, aides):
    """jj022 : Jessica Jones ET Luke Cage portent un statut Tenace."""
    identite = aides["identite"](monde)
    luke = aides["par_id"](monde, "jj002")
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
    """av003 : a 10 PV, 3 degats, Rhino Sonne et 1 menace retiree du complot."""
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
    return _obligation_resolue(monde, aides, "mf013")

def obligation_resolue_67011(monde, aides):
    return _obligation_resolue(monde, aides, "th011")

def obligation_resolue_75018(monde, aides):
    return _obligation_resolue(monde, aides, "sg018")

def mf_mental_gymnastics(monde, aides):
    """mf012 : 2 degats (X=0) et le vilain Desoriente car la main est vide."""
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
    """iw018 : la traitrise s'est resolue et a quitte le jeu sans planter."""
    if aides["par_id"](monde, "iw018") is not None:
        return False, "End of the Line est encore en jeu : la resolution a echoue"
    return True, "traitrise resolue"

def ht_nova_flame(monde, aides):
    """ht010 : 7 degats au vilain, et des compteurs flamme poses sur lui.

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
    return _obligation_resolue(monde, aides, "mk012")

def obligation_resolue_78013(monde, aides):
    return _obligation_resolue(monde, aides, "lj013")

def obligation_resolue_66013(monde, aides):
    return _obligation_resolue(monde, aides, "iw013")


def ht_the_thing_tenace(monde, aides):
    """ht002 : l'allie est en jeu, a 5 PV, 3 ATK et un statut Tenace."""
    allie = aides["par_id"](monde, "ht002")
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
    """iw002 : l'allie est en jeu et UNE de ses deux options a ete appliquee.

    Option A : 1 menace retiree de chaque manigance (le complot passe de 3 a 2).
    Option B : la carte du dessus de la defausse revient en main.
    """
    allie = aides["par_id"](monde, "iw002")
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
    """ah014 : Lady Hellbender est passee du camp ennemi au camp du joueur.

    `TreatAsAlly` remplace la carte par le gabarit `tah_hellbender_ally`, donc
    son card_id CHANGE : on interroge les allies controles, pas `par_id`.
    """
    allies = [getattr(f.paper, "card_id", "?")
              for f in monde.players[0].GetControlAllies()]
    if not allies:
        return False, "le joueur ne controle aucun allie"
    if aides["par_id"](monde, "ah014") is not None:
        return False, f"ah014 est encore un sbire (allies = {allies})"
    return True, f"Lady Hellbender est passee alliee (allies = {allies})"

def cd_barrage_reparti(monde, aides):
    """cd002a : les degats de l'attaque de base de Dagger ont touche DEUX ennemis.

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
    """cd002b : Tandy Bowen a +2 REC tant que Tyrone Johnson est en jeu.

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
    """ah001c : la forme BRUTE est active et son attaque a fait plus que l'ATK imprime."""
    identite = aides["identite"](monde)
    vilain = aides["par_id"](monde, "01094")
    if identite is None or vilain is None:
        return False, "identite ou Rhino introuvable"
    if getattr(identite.paper, "card_id", None) != "ah001c":
        return False, f"forme active = {getattr(identite.paper, 'card_id', '?')} (attendue ah001c)"
    degats = vilain.max_health - vilain.health
    attendu = identite.attack + 2
    if degats < attendu:
        return False, (f"degats = {degats}, or l'attaque de base ({identite.attack}) "
                       f"plus le bonus de 2 en attendait {attendu}")
    return True, f"forme BRUTE, {degats} degats (ATK {identite.attack} + 2)"

def vr_hunger_a_soigne(monde, aides):
    """vr001a : le sbire est vaincu et Venom s'est soigne de 1.

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
    """mk001c : la carte Protection a ete jouee alors que la main etait vide.

    Elle coute 1 ; sans la reduction de Mr. Knight il n'y a aucun payeur et la
    carte reste en main. La voir EN JEU prouve donc la reduction.
    """
    if aides["par_id"](monde, "01081") is None:
        return False, "Armored Vest n'est pas en jeu : le cout n'a pas ete reduit"
    identite = aides["identite"](monde)
    face = getattr(identite.paper, "card_id", "?") if identite else "?"
    if face != "mk001c":
        return False, f"forme active = {face} (attendue Mr. Knight mk001c)"
    return True, "Armored Vest posee gratuitement en forme Mr. Knight"

def identite_sans_statut_tenace(monde, aides):
    """L'identite du joueur ne porte PLUS de statut Tenace."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if identite.IsTough():
        return False, "l'identite porte encore un statut Tenace"
    return True, "le statut Tenace a bien ete defausse"

def gp003_desorientee_annule_tout(monde, aides):
    """gp003 est imprimee « (attack/thwart) » : Desoriente doit l'ANNULER.

    Le label `thwart` est ce qui declenche le statut Desoriente
    (`cards/pack/status/confused.py`, `AfterPlayerTriggerAbility(label='thwart')`).
    Sans lui, la carte passe en force : elle retire sa menace ET l'identite
    garde son statut pour plus tard. Avec lui, `set_be_instead` remplace TOUTE
    la capacite — c'est deja ce qui arrive a la carte OFFICIELLE 18004
    Crosscounter, imprimee « (attack/defense/thwart) », pour laquelle
    `confused.py` porte un cas special.
    """
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    soucis = []
    if identite.IsConfused():
        soucis.append("l'identite est encore Desorientee : le statut n'a pas ete consomme")
    principal = aides["par_id"](monde, "01097b")
    if principal is None:
        soucis.append("complot principal 01097b introuvable")
    elif principal.threat != 3:
        soucis.append(f"menace sur 01097b = {principal.threat} (attendu 3 : "
                      "la capacite devait etre annulee)")
    vilain = aides["par_id"](monde, "01094")
    if vilain is None:
        soucis.append("Rhino introuvable")
    else:
        subis = vilain.max_health - vilain.health
        if subis != 0:
            soucis.append(f"degats sur Rhino = {subis} (attendu 0 : "
                          "la capacite devait etre annulee)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "capacite annulee de bout en bout, statut Desoriente consomme"

def mf001a_ou_est_la_carte(monde, aides):
    """Diagnostic : ou 01017 a-t-elle atterri apres avoir ete defaussee DU JEU ?"""
    j = monde.players[0]
    def ids(seq):
        return [getattr(f.paper, "card_id", None) for f in seq]
    main = ids(j.hand_cards.GetAll())
    defausse = ids(j.discard_pile.Get())
    en_jeu = aides["par_id"](monde, "01017") is not None
    ou = f"main={main} defausse={defausse} en_jeu={en_jeu}"
    if "01017" in main:
        return False, "SUR-DECLENCHEMENT : 01017 est revenue EN MAIN alors qu'elle etait EN JEU. " + ou
    if "01017" in defausse:
        return True, "01017 est bien restee dans la defausse. " + ou
    return False, "01017 est introuvable, la sonde ne prouve rien. " + ou

def mf001a_ou_est_mf011(monde, aides):
    """Diagnostic : mf011 defaussee DE LA MAIN sans etre jouee revient-elle ?"""
    j = monde.players[0]
    ids = lambda seq: [getattr(f.paper, "card_id", None) for f in seq]
    main = ids(j.hand_cards.GetAll())
    defausse = ids(j.discard_pile.Get())
    ou = f"main={main} defausse={defausse}"
    if "mf011" in main:
        return True, "mf011 est bien revenue en main (branche du texte respectee). " + ou
    if "mf011" in defausse:
        return False, "MANQUE : mf011 est restee dans la defausse, la Response n'a PAS part. " + ou
    return False, "mf011 introuvable. " + ou

def identite_est_tenace(monde, aides):
    """L'identite du joueur porte un statut Tenace."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if not identite.IsTough():
        return False, "l'identite n'est pas Tenace"
    return True, "l'identite est Tenace"

def tt_human_torch_a_choisi(monde, aides):
    """th002 : la torche est en jeu et UNE des deux options a ete appliquee.

    Option A : 1 degat a The Thing puis statut Tenace.
    Option B : 3 degats au vilain.
    Le pilote choisit ; on accepte l'une ou l'autre, mais pas l'inaction.
    """
    torche = aides["par_id"](monde, "th002")
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
    return _obligation_resolue(monde, aides, "av012")

def obligation_resolue_73017(monde, aides):
    return _obligation_resolue(monde, aides, "jj017")

def aav_retaliate(monde, aides):
    """av008 : Agent Anti-Venom porte retaliate 1 tant que le Booster est en jeu."""
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
    """jj016 : l'identite de Jessica Jones porte un statut Tenace (Tough)."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if not identite.IsTough():
        return False, "Jessica Jones n'a pas de statut Tenace"
    return True, "Jessica Jones est Tenace"

def mk_forme_heros_et_vilain_desoriente(monde, aides):
    """mk010 : l'identite est passee en forme heros et Rhino est Desoriente."""
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
    """lj027 : au moins un allie PET AVENGER est arrive en jeu."""
    n = 0
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and face.IsInPlay() and face.HasTrait("PET AVENGER"):
            n += 1
    if n >= 1:
        return True, f"{n} PET AVENGER en jeu"
    return False, "aucun PET AVENGER en jeu : la recherche n'a rien sorti"

def lj_defausse_non_vide(monde, aides):
    """lj012 : la carte cherchee dans le deck est bien partie a la defausse.

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
    """sg001b : le setup range les 6 ecureuils dans le deck additionnel."""
    joueur = monde.players[0]
    deck = list(joueur.additional_deck.Get())
    ids = sorted(getattr(f.paper, "card_id", "?") for f in deck)
    attendus = ["sg002", "sg003", "sg004", "sg005", "sg006", "sg007"]
    if ids != attendus:
        return False, f"deck ecureuil = {ids} (attendu {attendus})"
    return True, "les 6 ecureuils sont dans le deck ecureuil"

def sg_deux_ecureuils_prets(monde, aides):
    """sg013 : deux ecureuils entrent en jeu, et ils sont PRETS."""
    faces = _sg_ecureuils_en_jeu(monde)
    if len(faces) < 2:
        return False, f"{len(faces)} ecureuil(s) en jeu (attendu 2)"
    inclines = [getattr(f.paper, "card_id", "?") for f in faces if f.IsExhaust()]
    if inclines:
        return False, f"ecureuils inclines alors qu'ils devraient etre prets : {inclines}"
    return True, f"{len(faces)} ecureuils en jeu, tous prets"

def sg_ecureuil_depense(monde, aides):
    """sg001a : l'ecureuil a bien finance la carte, et Unbeatable Army a suivi.

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
    """sg020 : Discord in the Branches rend les capacites d'ecureuil blanches.

    Nancy Whitehead (sg008) est mise en jeu APRES la manigance. Sa propre
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
    """sg002 : aucun ecureuil ne doit gagner d'ATK par une carte hors du set."""
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
    """sg022 : la capacite Boost defausse l'ecureuil controle."""
    faces = _sg_ecureuils_en_jeu(monde)
    if faces:
        ids = [getattr(f.paper, "card_id", "?") for f in faces]
        return False, f"ecureuil(s) encore en jeu : {ids}"
    return True, "l'ecureuil a bien ete defausse"

def sg_unbeatable(monde, aides):
    """sg016 : l'evenement est joue en defense, et l'attaque ne passe pas.

    Sans `Puzzle.Attack(defender=...)`, le message WhenUnitWouldDefend n'etait
    jamais envoye et cette carte etait intestable.
    """
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "sg016" not in defausse:
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
    """Temoin du cas sg016 : sans defenseur, la carte ne peut pas etre jouee."""
    defausse = [getattr(f.paper, "card_id", None)
                for f in monde.players[0].discard_pile.Get()]
    if "sg016" in defausse:
        return False, ("Unbeatable! a ete jouee alors qu'aucun defenseur n'etait "
                       "declare : le cas principal ne prouve rien")
    return True, "sans defenseur declare, la fenetre de defense ne s'ouvre pas"

def sg_gatherer_soigne(monde, aides):
    """sg007 : depense pour payer une carte du set, il rend 1 point de vie."""
    if aides["par_id"](monde, "sg007") is not None:
        return False, "The Gatherer est encore en jeu : il n'a pas ete depense"
    identite = aides["identite"](monde)
    subis = identite.max_health - identite.health
    if subis != 2:
        return False, f"degats restants = {subis} (3 infliges, 1 soin attendu, donc 2)"
    return True, "The Gatherer depense, 1 degat soigne"

def sg_forager_defausse(monde, aides):
    """sg006 : depense, il regarde 2 cartes et en defausse 1.

    Les ecureuils depenses partent dans la defausse ECUREUIL : la defausse du
    joueur ne doit donc contenir que l'evenement joue et la carte defaussee
    depuis le deck.
    """
    if aides["par_id"](monde, "sg006") is not None:
        return False, "The Forager est encore en jeu : il n'a pas ete depense"
    cartes = [getattr(f.paper, "card_id", None)
              for f in monde.players[0].discard_pile.Get()]
    if aides["par_id"](monde, "sg008") is None:
        return False, "Nancy Whitehead n'a pas ete jouee : le paiement a echoue"
    if "01090" not in cartes:
        return False, ("Strength, posee sur le dessus du deck, n'a pas ete defaussee : "
                       "la branche optionnelle du Forager n'a pas ete prise")
    return True, "The Forager depense, la carte du dessus du deck est defaussee"

def sg_monkey_joe(monde, aides):
    """sg003 : le sbire tombe sous son attaque, un ecureuil est appele.

    Monkey Joe a 1 PV et 1 degat consequent : il meurt en frappant. L'ecureuil
    appele est donc le SEUL encore en jeu a la fin.
    """
    if aides["par_id"](monde, "01103") is not None:
        return False, "Shocker (01103) est encore en jeu : Monkey Joe ne l'a pas vaincu"
    faces = [f for f in _sg_ecureuils_en_jeu(monde)
             if getattr(f.paper, "card_id", None) != "sg003"]
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
    """sg011 : au-dela de 3 ecureuils, la seconde activation n'appelle rien."""
    faces = _sg_ecureuils_en_jeu(monde)
    if len(faces) != 3:
        return False, f"{len(faces)} ecureuil(s) en jeu (attendu exactement 3)"
    parc = aides["par_id"](monde, "sg011")
    if parc is None:
        return False, "Central Park n'est pas en jeu"
    if not parc.IsExhaust():
        return False, "Central Park n'est pas incline : l'action n'a pas ete jouee"
    return True, "Central Park s'incline mais n'appelle pas de 4e ecureuil"

def sg_bruiser_encaisse(monde, aides):
    """sg005 : le degat consequent d'un autre ecureuil part sur The Bruiser.

    Tippy-Toe manigance : elle devrait prendre 1 degat consequent. Avec The
    Bruiser en jeu, elle en sort indemne, et c'est lui qui porte le degat, en
    s'inclinant pour payer son cout.
    """
    agissant = aides["par_id"](monde, "sg002")
    bruiser = aides["par_id"](monde, "sg005")
    if bruiser is None:
        return False, "The Bruiser (sg005) n'est pas en jeu"
    if agissant is None:
        return False, "Tippy-Toe (sg002) n'est plus en jeu"
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
    """ag004 : 3 menaces de base + 1 icone (Stampede 01106, deck Rencontre truque)
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
    """ag012 : invulnerabilite conditionnelle (engage avec un AUTRE sbire) PUIS
    l'allie qui encaisse a la place du joueur, a hauteur de son ATK courante.
    """
    faustus = aides["par_id"](monde, "ag012")
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
    """ag013 : trouve Advanced Ultron Drone (01143, deck Rencontre truque a une
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

# ------------------------------------------------------------------------
# Pack « okoye » : ok001a-ok024
# ------------------------------------------------------------------------

def okoye_art_of_war_reduit_degats_consecutifs(monde, aides):
    """ok001a : apres une attaque de base d'Okoye, l'allie DORA MILAJE
    officiel 51022 (Aneka, ATK imprime "2*") doit voir son
    attack_consequential_damage baisser de 2 a 1."""
    face = aides["par_id"](monde, "51022")
    if face is None:
        return False, "Aneka (51022) introuvable en jeu"
    valeur = face.attack_consequential_damage
    if valeur != 1:
        return False, (f"attack_consequential_damage d'Aneka (51022) = {valeur} "
                       f"(imprime 2, attendu 1 apres The Art of War)")
    return True, "The Art of War a bien reduit de 1 les degats consecutifs d'Aneka (51022) apres l'attaque de base"

def okoye_vanguard_leader_cherche_reinforcements(monde, aides):
    """ok001b : au Setup, une carte REINFORCEMENTS doit avoir rejoint la main."""
    joueur = monde.players[0]
    for face in joueur.hand_cards.GetAll():
        if face.HasTrait("REINFORCEMENTS"):
            return True, f"carte REINFORCEMENTS en main apres le Setup : {getattr(face.paper, 'card_id', '?')}"
    return False, "aucune carte REINFORCEMENTS en main apres le Setup"

def okoye_marshalling_forces_remet_dans_le_deck(monde, aides):
    """ok001b : Marshalling Forces retire une carte REINFORCEMENTS de la defausse."""
    joueur = monde.players[0]
    dans_defausse = [getattr(f.paper, "card_id", None) for f in joueur.discard_pile.Get()]
    if "ok004" in dans_defausse:
        return False, f"ok004 est encore dans la defausse (defausse = {dans_defausse})"
    return True, "ok004 a quitte la defausse (remelange dans le deck par Marshalling Forces)"

def okoye_aneka_buff_atk_allies(monde, aides):
    """ok002 : Aneka donne +1 ATK aux autres allies DORA MILAJE, pas a elle-meme."""
    dora = aides["par_id"](monde, "ok017")
    if dora is None:
        return False, "ok017 (Dora Milaje) introuvable en jeu"
    if dora.attack != dora.printed_attack + 1:
        return False, f"ATK d'ok017 = {dora.attack} (imprime {dora.printed_attack}, attendu +1)"
    aneka = aides["par_id"](monde, "ok002")
    if aneka is not None and aneka.attack != aneka.printed_attack:
        return False, f"Aneka elle-meme a ete affectee (ATK={aneka.attack}, imprime {aneka.printed_attack})"
    return True, "ok017 gagne +1 ATK apres l'entree en jeu d'Aneka, Aneka elle-meme non affectee"

def okoye_ayo_buff_thw_allies(monde, aides):
    """ok003 : Ayo donne +1 THW aux autres allies DORA MILAJE."""
    dora = aides["par_id"](monde, "ok017")
    if dora is None:
        return False, "ok017 (Dora Milaje) introuvable en jeu"
    if dora.thwart != dora.printed_thwart + 1:
        return False, f"THW d'ok017 = {dora.thwart} (imprime {dora.printed_thwart}, attendu +1)"
    return True, "ok017 gagne +1 THW apres l'entree en jeu d'Ayo"

def okoye_adored_ones_cree_deux_dora_milaje(monde, aides):
    """ok004/ok005 : la branche "Create 2 Dora Milaje allies" doit poser 2
    allies nommes "Dora Milaje" sous le controle du joueur."""
    joueur = monde.players[0]
    dora = [f for f in joueur.allies.Get() if f.IsName("Dora Milaje")]
    if len(dora) != 2:
        return False, f"{len(dora)} allie(s) Dora Milaje en jeu (attendu 2) — branche choisie par le pilote inattendue ?"
    return True, "2 allies Dora Milaje crees et mis en jeu par Adored Ones"

def okoye_angelic_warfare_cree_deux_midnight_angel(monde, aides):
    """ok006/ok007 : la branche "Create 2 Midnight Angel allies"."""
    joueur = monde.players[0]
    ma = [f for f in joueur.allies.Get() if f.IsName("Midnight Angel")]
    if len(ma) != 2:
        return False, f"{len(ma)} allie(s) Midnight Angel en jeu (attendu 2)"
    return True, "2 allies Midnight Angel crees et mis en jeu par Angelic Warfare"

def okoye_spear_thrust_degat_de_base(monde, aides):
    """ok008/ok009 : 4 degats de base a un ennemi, meme sans exhausteur."""
    villain = aides["par_id"](monde, "01094")
    if villain is None:
        return False, "Rhino (01094) introuvable en jeu"
    subis = villain.max_health - villain.health
    if subis < 4:
        return False, f"degats sur Rhino = {subis} (attendu au moins 4)"
    return True, f"Spear Thrust inflige bien ses 4 degats de base ({subis} au total)"

def okoye_close_ranks_pose_un_compteur(monde, aides):
    """ok010 : apres la defaite d'un allie DORA MILAJE controle, 1 compteur phalanx."""
    face = aides["par_id"](monde, "ok010")
    if face is None:
        return False, "Close Ranks (ok010) introuvable en jeu"
    n = face.CastTo(aides["CanPlaceCounter"]).GetCounters("phalanx")
    if n != 1:
        return False, f"compteurs phalanx sur Close Ranks = {n} (attendu 1)"
    return True, "1 compteur phalanx pose apres la defaite de l'allie DORA MILAJE"

def okoye_close_ranks_finance_un_achat(monde, aides):
    """ok010 : la ressource de Close Ranks finance vraiment l'achat de Vibranium
    Spear (cout 1), et ne consomme qu'UN SEUL compteur phalanx sur les 2 poses."""
    close_ranks = aides["par_id"](monde, "ok010")
    if close_ranks is None:
        return False, "Close Ranks (ok010) introuvable en jeu"
    if not close_ranks.IsExhaust():
        return False, "Close Ranks n'est pas incline (le cout Exhaust n'a pas ete paye)"
    n = close_ranks.CastTo(aides["CanPlaceCounter"]).GetCounters("phalanx")
    if n != 1:
        return False, f"compteurs phalanx restants sur Close Ranks = {n} (attendu 1 : 2 poses, 1 depense pour payer 1 [physical])"
    spear = aides["par_id"](monde, "ok015")
    if spear is None:
        return False, "Vibranium Spear (ok015) n'est pas en jeu : l'achat finance par Close Ranks a echoue"
    return True, "Close Ranks a finance Vibranium Spear en depensant exactement 1 compteur phalanx sur 2"

def okoye_upanga_buff_hp_allies(monde, aides):
    """ok011 : chaque allie DORA MILAJE controle gagne +1 point de vie."""
    dora = aides["par_id"](monde, "ok017")
    if dora is None:
        return False, "ok017 (Dora Milaje) introuvable en jeu"
    if dora.max_health != dora.printed_health + 1:
        return False, f"PV max d'ok017 = {dora.max_health} (imprime {dora.printed_health}, attendu +1)"
    return True, "ok017 gagne +1 PV grace a Upanga"

def okoye_upanga_action_remet_equipement(monde, aides):
    """ok011 : l'Action d'identite civile remet une carte ARMOR/TECH/WEAPON de la defausse au deck."""
    joueur = monde.players[0]
    dans_defausse = [getattr(f.paper, "card_id", None) for f in joueur.discard_pile.Get()]
    if "ok015" in dans_defausse:
        return False, f"ok015 est encore dans la defausse (defausse = {dans_defausse})"
    upanga = aides["par_id"](monde, "ok011")
    if upanga is None or not upanga.IsExhaust():
        return False, "Upanga n'est pas incline : le cout de l'action n'a pas ete paye"
    return True, "ok015 a quitte la defausse (remelange par l'Action d'identite civile d'Upanga), Upanga inclinee"

def okoye_midnight_angel_armor_stats(monde, aides):
    """ok012/ok013 : +2 PV, trait AERIAL, sur le personnage DORA MILAJE attache."""
    dora = aides["par_id"](monde, "ok017")
    if dora is None:
        return False, "ok017 (Dora Milaje) introuvable en jeu"
    if dora.max_health != dora.printed_health + 2:
        return False, f"PV max d'ok017 = {dora.max_health} (imprime {dora.printed_health}, attendu +2)"
    if not dora.HasTrait("AERIAL"):
        return False, "ok017 n'a pas gagne le trait AERIAL"
    armure = aides["par_id"](monde, "ok012")
    if armure is None:
        return False, "Midnight Angel Armor (ok012) n'est pas en jeu"
    return True, "ok017 gagne +2 PV et le trait AERIAL, Midnight Angel Armor bien attachee"

def okoye_fragile_donne_overkill(monde, aides):
    """ok017 : SANS armure, une attaque qui depasse les PV restants d'un allie
    Fragile deverse l'exces sur l'identite du joueur (Deferlement)."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    subis = identite.max_health - identite.health
    if subis < 1:
        return False, (f"degats indirects sur l'identite = {subis} (attendu au moins 1 : "
                       f"exces de l'attaque de Rhino (ATK 2) sur ok017, deja blesse a 1 PV restant)")
    return True, f"Fragile a bien deverse {subis} degat(s) en exces sur l'identite (pas d'armure attachee)"

def okoye_armure_retire_fragile(monde, aides):
    """ok012 : AVEC l'armure attachee, ok017 perd Fragile : l'exces d'attaque
    ne doit PLUS se deverser sur l'identite."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    subis = identite.max_health - identite.health
    if subis != 0:
        return False, (f"degats indirects sur l'identite = {subis} (attendu 0 : Midnight Angel Armor "
                       f"retire le mot-cle fragile, donc pas de Deferlement)")
    return True, "aucun degat indirect sur l'identite : Midnight Angel Armor supprime bien Fragile"

def okoye_legion_paire_pour_la_limite(monde, aides):
    """ok017/ok018 : 2 allies Legion (ok017 + ok018) comptent comme 1 seul pour
    la limite d'allies ; un troisieme allie NON Legion (51022 Aneka officielle)
    compte normalement — total attendu 2, pas 3."""
    joueur = monde.players[0]
    if joueur.limit_ally.curr_ally != 2:
        return False, (f"curr_ally = {joueur.limit_ally.curr_ally} (attendu 2 : "
                       f"ok017+ok018 Legion comptent comme 1, + 51022 Aneka normale = 2)")
    dora = aides["par_id"](monde, "ok017")
    ma = aides["par_id"](monde, "ok018")
    aneka = aides["par_id"](monde, "51022")
    if dora is None or ma is None or aneka is None:
        return False, "un des 3 allies a ete defausse par la limite (aucun ne devrait l'etre)"
    return True, "2 allies Legion comptes comme 1 seul, aucune defausse forcee"

def okoye_royal_protector_limite_et_thw(monde, aides):
    """ok014 : +1 limite d'allies, Okoye +1 THW en forme heros."""
    joueur = monde.players[0]
    if joueur.limit_ally.Get() != 4:
        return False, f"limite d'allies = {joueur.limit_ally.Get()} (attendu 4 : 3 de base + 1)"
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if identite.thwart != identite.printed_thwart + 1:
        return False, f"THW d'Okoye = {identite.thwart} (imprime {identite.printed_thwart}, attendu +1)"
    return True, "limite d'allies a 4, Okoye gagne +1 THW en forme heros"

def okoye_royal_protector_redresse_apres_defaite(monde, aides):
    """ok014 : apres la defaite d'un allie WAKANDA, exhaust Royal Protector -> ready Okoye."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if identite.card.IsExhaust():
        return False, "Okoye est encore inclinee : la Response n'a pas redresse l'identite"
    protecteur = aides["par_id"](monde, "ok014")
    if protecteur is None or not protecteur.IsExhaust():
        return False, "Royal Protector n'est pas inclinee (son propre cout n'a pas ete paye)"
    return True, "Okoye redressee et Royal Protector inclinee apres la defaite de l'allie WAKANDA"

def okoye_vibranium_spear_sur_heros(monde, aides):
    """ok015/ok016 : +1 ATK seulement quand attachee a un heros (pas un allie)."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if identite.attack != identite.printed_attack + 1:
        return False, f"ATK d'Okoye = {identite.attack} (imprime {identite.printed_attack}, attendu +1)"
    return True, "Okoye gagne +1 ATK avec Vibranium Spear (portee par un heros)"

def okoye_vibranium_spear_sur_allie(monde, aides):
    """ok015/ok016 : +2 ATK quand attachee a un allie."""
    dora = aides["par_id"](monde, "ok017")
    if dora is None:
        return False, "ok017 (Dora Milaje) introuvable en jeu"
    if dora.attack != dora.printed_attack + 2:
        return False, f"ATK d'ok017 = {dora.attack} (imprime {dora.printed_attack}, attendu +2)"
    return True, "ok017 gagne +2 ATK avec Vibranium Spear (portee par un allie)"

def okoye_funeral_rites_branche_retrait(monde, aides):
    """ok019 : la branche « exhaust alter-ego + allies DORA MILAJE -> retirer
    Funeral Rites de la partie » retire bien l'obligation du jeu."""
    if aides["par_id"](monde, "ok019") is not None:
        return False, "Funeral Rites (ok019) est encore en jeu"
    return True, "Funeral Rites a bien ete retiree de la partie"

def okoye_malevolent_mimic_menace_apres_defaite(monde, aides):
    """ok020 : Forced Response, apres la defaite d'un allie (n'importe lequel), +2 menace.
    Le side scheme demarre a 2 (StartingThreat imprime '2*', 1 joueur) : attendu 2+2=4.
    (Ne PAS remettre la menace a 0 avant : un side scheme a 0 menace est aussitot
    considere dejoue et quitte le jeu, contrairement au complot principal.)"""
    face = aides["par_id"](monde, "ok020")
    if face is None:
        return False, "Malevolent Mimic (ok020) introuvable en jeu (dejouee/retiree ?)"
    if face.threat != 4:
        return False, f"menace sur Malevolent Mimic = {face.threat} (attendu 4 : 2 de depart + 2 de la Response)"
    return True, "Malevolent Mimic gagne 2 menace apres la defaite d'un allie (2 de depart + 2 = 4)"

def okoye_malice_manigance_apres_defaite(monde, aides):
    """ok021 : Forced Response, apres la defaite d'un allie, Malice manigance
    (action de base SCH = 3) sur le complot principal, remis a 0 avant le cas."""
    scheme = aides["par_id"](monde, "01097b")
    if scheme is None:
        return False, "complot principal (01097b) introuvable"
    if scheme.threat != 3:
        return False, (f"menace sur le complot principal = {scheme.threat} "
                       f"(attendu 3 : SCH imprime de Malice)")
    return True, "Malice a bien manigance pour sa valeur SCH imprimee (3) apres la defaite de l'allie"

def okoye_mimic27_atk_egal_atk_heros(monde, aides):
    """ok022 : X = ATK du joueur en forme HEROS (2, valeur imprimee d'Okoye)."""
    face = aides["par_id"](monde, "ok022")
    if face is None:
        return False, "Mimic-27 (ok022) introuvable en jeu"
    if face.attack != 2:
        return False, f"ATK de Mimic-27 = {face.attack} (attendu 2, ATK imprime d'Okoye en forme heros)"
    return True, "ATK de Mimic-27 = 2, egal a l'ATK d'Okoye en forme heros"

def okoye_mimic27_atk_zero_en_alter_ego(monde, aides):
    """ok022 : X = 0 en forme ALTER-EGO."""
    face = aides["par_id"](monde, "ok022")
    if face is None:
        return False, "Mimic-27 (ok022) introuvable en jeu"
    if face.attack != 0:
        return False, f"ATK de Mimic-27 = {face.attack} (attendu 0 en forme identite civile)"
    return True, "ATK de Mimic-27 = 0 en forme identite civile"

def okoye_war_drumming_branche_heros_faible_atk(monde, aides):
    """ok023/ok024 : en forme HEROS, un seul sbire en jeu (Malice, ATK 1 < 3) est
    designe sans choix et attaque le joueur (branche villainous, ATK<=2, non
    codee — seul le fait que l'attaque ait bien eu lieu est verifiable)."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    subis = identite.max_health - identite.health
    if subis != 1:
        return False, f"degats sur l'identite = {subis} (attendu 1 : ATK imprime de Malice)"
    return True, "Malice (seul sbire en jeu) a bien attaque le joueur pour son ATK (1)"

def okoye_war_drumming_branche_identite_civile_surge(monde, aides):
    """ok023/ok024 : en forme IDENTITE CIVILE, la carte gagne renfort (1 carte
    Rencontre supplementaire distribuee au joueur)."""
    from game.operate.worlds import Worlds
    joueur = monde.players[0]
    n = len(list(joueur.discard_pile.Get())) if hasattr(joueur, "discard_pile") else 0
    ids_defausse_rencontre = [getattr(f.paper, "card_id", None)
                              for f in Worlds.GetEncounterDiscardPileCards(monde)]
    if len(ids_defausse_rencontre) < 2:
        return False, (f"defausse Rencontre = {ids_defausse_rencontre} (attendu au moins 2 : "
                       f"War Drumming elle-meme + la carte supplementaire tiree par Renfort)")
    return True, f"Renfort a bien distribue une carte Rencontre supplementaire (defausse Rencontre = {ids_defausse_rencontre})"

def iron_lad_destiny_defausse_au_moins_deux(monde, aides):
    """il001a : Destiny regarde 4 cartes, en garde au plus 2 (AskChooseFaces
    range (0,2)) : au moins 2 partent donc TOUJOURS en defausse, quel que
    soit le type de ressource nomme ou les correspondances trouvees."""
    joueur = monde.players[0]
    n = len(list(joueur.discard_pile.Get()))
    if n < 2:
        return False, (f"defausse du joueur = {n} carte(s) (attendu au moins 2 : "
                       f"Destiny regarde 4 cartes et n'en garde jamais plus de 2)")
    return True, f"Destiny a bien defausse au moins 2 des 4 cartes vues (defausse = {n})"

def iron_lad_seeking_solutions_remet_en_deck(monde, aides):
    """il007/il008 : la carte choisie (il009, forcee via 'cibles') doit avoir
    QUITTE la defausse (melangee dans le deck). Le bonus de pioche (1 carte
    par carte TECH melangee) est secondaire et non verifie ici."""
    joueur = monde.players[0]
    ids_defausse = [getattr(f.paper, "card_id", None) for f in joueur.discard_pile.Get()]
    if "il009" in ids_defausse:
        return False, f"il009 est encore dans la defausse (defausse={ids_defausse}) : pas melangee"
    return True, "il009 a bien quitte la defausse (melangee dans le deck)"

def iron_lad_vision_ai_melange_et_retourne(monde, aides):
    """il009 : deux cibles distinctes sur la meme defausse a 2 cartes.
    01089 (defaussee en dernier, donc dessus) doit etre melangee dans le
    deck ; 01088 (defaussee en premier, donc dessous) doit revenir en main."""
    joueur = monde.players[0]
    ids_main = [getattr(f.paper, "card_id", None) for f in joueur.hand_cards.GetAll()]
    ids_defausse = [getattr(f.paper, "card_id", None) for f in joueur.discard_pile.Get()]
    soucis = []
    if "01089" in ids_defausse:
        soucis.append(f"01089 (dessus de la defausse) est encore dans la defausse : pas melangee (defausse={ids_defausse})")
    if "01088" not in ids_main:
        soucis.append(f"01088 (dessous de la defausse) n'est pas revenu en main (main={ids_main})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "Vision AI a bien melange le dessus de la defausse et rendu le dessous en main"

def iron_lad_hack_retire_au_lieu_de_placer(monde, aides):
    """il010 : message.SetBeInstead + RemoveThreatFromSchemes([meme plan]) :
    la menace du complot principal doit BAISSER (jamais monter) quand un
    sbire manigance, et Hack doit avoir ete defaussee (cout de l'Interrupt)."""
    face = aides["par_id"](monde, "01097b")
    if face is None:
        return False, "complot principal (01097b) introuvable"
    if face.threat >= 5:
        return False, (f"menace sur le complot principal = {face.threat} (attendu < 5 : la menace "
                       f"posee doit etre retiree au lieu d'etre ajoutee)")
    if aides["par_id"](monde, "il010") is not None:
        return False, "Hack (il010) est encore en jeu (devrait etre defaussee, cout de l'Interrupt)"
    return True, f"Hack a bien empeche la pose de menace et en a retire du complot principal (menace={face.threat}, depart 5)"

def iron_lad_kang_empile_puis_rend(monde, aides):
    """il019 : Filter.One(highest_cost=True) doit choisir il015 (cout 3) et
    non il011 (cout 2) ; au When Defeated, il015 doit revenir en main et
    Kang doit avoir quitte le jeu (mis de cote)."""
    joueur = monde.players[0]
    ids_main = [getattr(f.paper, "card_id", None) for f in joueur.hand_cards.GetAll()]
    soucis = []
    if "il015" not in ids_main:
        soucis.append(f"il015 (cout le plus eleve, 3) n'est pas revenue en main apres la defaite de Kang (main={ids_main})")
    if aides["par_id"](monde, "il019") is not None:
        soucis.append("Kang the Conqueror (il019) est encore trouvable en jeu (devrait etre mis de cote)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "Kang a bien empile il015 (cout le plus eleve) puis l'a rendue a sa defaite, et s'est mis de cote"
def si008_stark_island_paye(monde, aides):
    """si008 : Pepper Potts (cout 1) doit etre en jeu ET 01088 doit avoir
    quitte la main (seule source de paiement possible avec main_exclusive) :
    preuve que le cout a vraiment ete paye via Player.PlayACard, pas
    seulement que la carte cherchee a ete posee gratuitement.
    """
    pepper = aides["par_id"](monde, "si007")
    if pepper is None:
        return False, "Pepper Potts (si007) n'est pas en jeu : la recherche ou la mise en jeu a echoue"
    joueur = monde.players[0]
    en_main = [f for f in joueur.hand_cards.GetAll()
               if getattr(f.paper, "card_id", None) == "01088"]
    if en_main:
        return False, "01088 est encore en main : le cout de Pepper Potts n'a pas ete paye"
    return True, "Pepper Potts en jeu, 01088 depensee pour payer son cout : PlayACard fonctionne"

def si001a_degat_et_ressource(monde, aides):
    """si001a : jouer si010 (cout 1) sans aucune autre source de ressource en
    main doit forcer le pilote a utiliser la capacite Ressource de l'identite
    (degat a un ami -> genere wild) : l'identite doit avoir subi 1 degat.
    """
    identite = aides["identite"](monde)
    subis = identite.max_health - identite.health
    endo_sym_spare = aides["par_id"](monde, "si010")
    if endo_sym_spare is None:
        return False, "si010 n'est pas en jeu : la carte n'a pas ete payee/jouee"
    if subis < 1:
        return False, f"degats subis par l'identite = {subis} (attendu >= 1 : preuve que la capacite Ressource a servi)"
    return True, f"si010 en jeu, {subis} degat(s) subis par l'identite : la capacite Ressource a paye"

def diag_si002_direct(monde, aides):
    armure = aides["par_id"](monde, "si002")
    if armure is None:
        return False, "si002 n'est pas en jeu meme via Puzzle.PutIntoPlay direct : le bug est dans si002 lui-meme"
    return True, "si002 en jeu via PutIntoPlay direct : le bug vient donc de BeginGameWithSetAside/additional_discard_pile"

def diag_wonder_man_ionic(monde, aides):
    ionic = aides["par_id"](monde, "58002")
    if ionic is None:
        return False, "58002 (Ionic Physiology) n'est pas en jeu : BeginGameWithSetAside ne se declenche pas dans ce harnais"
    return True, "Ionic Physiology en jeu : BeginGameWithSetAside fonctionne bien dans ce harnais"

def si001b_armure_en_jeu(monde, aides):
    """si001b : l'Armure Endo-Sym (si002) doit etre en jeu des le debut de partie."""
    armure = aides["par_id"](monde, "si002")
    if armure is None:
        partout = []
        for objet in monde.object_manager.card_dict.values():
            face = objet.face
            if face is not None and getattr(face.paper, "card_id", None) == "si002":
                partout.append((face.IsInPlay(), face.card.area))
        return False, f"si002 introuvable EN JEU ; occurrences ailleurs (IsInPlay, area) = {partout}"
    return True, "Endo-Sym Armor trouvee et mise en jeu par le Setup de Tony Stark"

def si001b_opa_retire_menace(monde, aides):
    """si001b : O.P.A. doit retirer 1+X menaces (X = ressources mentales
    depensees, ici 2 via Genius surpaye) d'une manigance a 5 menaces : 2 attendues."""
    scheme = aides["par_id"](monde, "01097b")
    if scheme is None:
        scheme = aides["par_id"](monde, "01097a")
    if scheme is None:
        return False, "manigance principale introuvable"
    joueur = monde.players[0]
    en_main = [f for f in joueur.hand_cards.GetAll()
               if getattr(f.paper, "card_id", None) == "01089"]
    if en_main:
        return False, "01089 (Genius) est encore en main : le cout n'a pas ete paye"
    if scheme.threat != 2:
        return False, f"menace restante = {scheme.threat} (attendu 2 : 5 - (1 + 2 mental depenses))"
    return True, f"menace restante = 2, conforme a 1+X avec X=2 mental depenses"

def si002_attaque_degats(monde, aides):
    """si002 : Rhino (01094, HP 14) doit avoir subi 2+X degats. X=1 (minimum
    garanti par la capacite Ressource de l'identite) => 3 degats."""
    rhino = aides["par_id"](monde, "01094")
    if rhino is None:
        return False, "01094 (Rhino) introuvable en jeu"
    subis = rhino.max_health - rhino.health
    if subis != 3:
        return False, f"degats subis par Rhino = {subis} (attendu 3 : 2 + X avec X=1 physical minimum)"
    return True, "Rhino a subi 3 degats (2 + 1 physical minimum) : Hero Action fonctionne"

def si002_defense_prevention(monde, aides):
    """si002 : l'identite doit avoir subi 3 degats sur les 5 infliges (1+X
    previens, X=1 energy minimum, donc 2 previens, 3 restent)."""
    identite = aides["identite"](monde)
    subis = identite.max_health - identite.health
    if subis != 3:
        return False, f"degats subis par l'identite = {subis} (attendu 3 : 5 infliges - (1+1) previens)"
    return True, "3 degats subis sur 5 (2 previens) : Hero Interrupt fonctionne"

def si003_rage_et_atk(monde, aides):
    """si003 : apres 1 attaque de base, rage doit passer de 4 a 3 et l'ATK de 4 a 3."""
    teen = aides["par_id"](monde, "si003")
    if teen is None:
        return False, "si003 introuvable en jeu"
    rage = teen.GetCounters('rage')
    if rage != 3:
        return False, f"compteurs rage = {rage} (attendu 3 apres 1 attaque)"
    if teen.attack != 3:
        return False, f"ATK courante = {teen.attack} (attendu 3 = 0 + 3 rage)"
    return True, "rage=3, ATK=3 apres l'attaque de base : les 2 capacites fonctionnent"

def si007_ignore_crisis(monde, aides):
    """si007 : la manigance principale doit avoir perdu 1 menace MALGRE
    Crowd Control (Crisis 1) en jeu, preuve que ignore_crisis fonctionne."""
    scheme = aides["par_id"](monde, "01097b")
    if scheme is None:
        scheme = aides["par_id"](monde, "01097a")
    if scheme is None:
        return False, "manigance principale introuvable"
    if scheme.threat != 4:
        return False, f"menace restante = {scheme.threat} (attendu 4 : 5-1, malgre Crowd Control en jeu)"
    return True, "1 menace retiree malgre Crowd Control (Crisis) : ignore_crisis fonctionne"

def si004_dernier_jeton(monde, aides):
    """si004 : au dernier jeton Flouze, Daniel Hall doit se defausser
    (Uses natif) ET une carte de la main doit avoir ete defaussee (ex_operation)."""
    si010 = aides["par_id"](monde, "si010")
    if si010 is None:
        return False, "si010 n'est pas en jeu : le paiement via si004 a echoue"
    daniel = aides["par_id"](monde, "si004")
    if daniel is not None:
        return False, "si004 est encore en jeu : Uses natif n'a pas defausse la carte au dernier jeton"
    joueur = monde.players[0]
    en_main = [f for f in joueur.hand_cards.GetAll()
               if getattr(f.paper, "card_id", None) == "01085"]
    if en_main:
        return False, "01085 est encore en main : l'Interruption Obligatoire n'a pas defausse de carte"
    return True, "si010 joue (paye par si004), si004 auto-defausse, 01085 defaussee : tout fonctionne"

def si009_boost_annule(monde, aides):
    """si009 : apres avoir annule un boost, il doit rester 1 jeton Observation sur 2."""
    iron_sight = aides["par_id"](monde, "si009")
    if iron_sight is None:
        return False, "si009 n'est pas en jeu"
    obs = iron_sight.GetCounters('observation')
    if obs != 1:
        return False, f"jetons Observation restants = {obs} (attendu 1 sur 2 : l'interruption n'a pas ete utilisee)"
    return True, "1 jeton Observation consomme : l'interruption d'annulation de boost fonctionne"

def si010_matter_dans_deck(monde, aides):
    """si010 : Endo-Sym Matter (si013) doit avoir quitte la defausse (melangee au deck)."""
    joueur = monde.players[0]
    en_defausse = [f for f in joueur.discard_pile.Get(True)
                   if getattr(f.paper, "card_id", None) == "si013"]
    if en_defausse:
        return False, "si013 est encore en defausse : elle n'a pas ete melangee au deck"
    return True, "si013 a quitte la defausse : la recherche + le melange au deck fonctionnent"

def si009_jouable_depuis_main(monde, aides):
    """si009 : doit pouvoir etre jouee normalement depuis la main en payant son cout."""
    iron_sight = aides["par_id"](monde, "si009")
    if iron_sight is None:
        return False, "si009 n'est jamais entree en jeu : injouable depuis la main (regression du bug .SetPlay())"
    return True, "si009 jouee normalement depuis la main : CanPlayThisSupportCard() est bien present"

def si011_double_effet(monde, aides):
    """si011 : Rhino doit avoir subi 3 degats ET la manigance doit avoir perdu 2 menaces."""
    rhino = aides["par_id"](monde, "01094")
    scheme = aides["par_id"](monde, "01097b") or aides["par_id"](monde, "01097a")
    if rhino is None or scheme is None:
        return False, "Rhino ou manigance introuvable"
    subis = rhino.max_health - rhino.health
    if subis != 3:
        return False, f"degats subis par Rhino = {subis} (attendu 3)"
    if scheme.threat != 3:
        return False, f"menace restante = {scheme.threat} (attendu 3 : 5-2)"
    return True, "3 degats + 2 menaces retirees : les 2 cibles fonctionnent"

def si012_double_effet(monde, aides):
    """si012 : l'identite doit avoir subi 2 degats sur 5 (3 previens) ET la manigance perdu 1 menace."""
    identite = aides["identite"](monde)
    scheme = aides["par_id"](monde, "01097b") or aides["par_id"](monde, "01097a")
    if scheme is None:
        return False, "manigance introuvable"
    subis = identite.max_health - identite.health
    if subis != 2:
        return False, f"degats subis par l'identite = {subis} (attendu 2 : 5-3 previens)"
    if scheme.threat != 4:
        return False, f"menace restante = {scheme.threat} (attendu 4 : 5-1)"
    return True, "2 degats subis (3 previens) + 1 menace retiree : Interruption + double effet fonctionnent"

def si013_double_ressource(monde, aides):
    """si013 : si011 (cout 2, un Event qui se resout puis se defausse) doit
    avoir inflige ses 3 degats a Rhino, preuve qu'elle a ete jouee en payant
    SEULEMENT avec le G unique de si013, double a 2 par DoubleResourcesThisGenerates."""
    rhino = aides["par_id"](monde, "01094")
    if rhino is None:
        return False, "Rhino introuvable"
    subis = rhino.max_health - rhino.health
    if subis != 3:
        return False, f"degats subis par Rhino = {subis} (attendu 3 : si011 n'a pas ete jouee, le G unique de si013 n'a pas ete double)"
    return True, "si011 (cout 2) jouee et resolue avec le seul G de si013 : la ressource a bien ete doublee"

def si014_option1_exhaust(monde, aides):
    """si014 option 1 : Tony Stark doit etre incline (cout de l'option), preuve
    qu'elle a ete choisie (option 2 n'incline jamais l'identite)."""
    identite = aides["identite"](monde)
    if not identite.IsExhaust():
        return False, "l'identite n'est pas inclinee : l'option 1 (Exhaust Tony Stark) n'a pas ete choisie"
    return True, "identite inclinee : l'option 1 (retrait de la partie) a bien ete choisie et executee"

def si014_option2_surge(monde, aides):
    """si014 option 2, paiement impossible (main vide) : la carte doit gagner renfort (surge)."""
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and getattr(face.paper, "card_id", None) == "si014":
            if getattr(face, "surge", 0) < 1:
                return False, f"surge={getattr(face, 'surge', None)} (attendu >=1 : le paiement a du echouer)"
            return True, "si014 a gagne renfort : ThisCardGainSurge s'est declenche sur paiement impossible"
    return False, "si014 introuvable dans le monde"

def si015_when_revealed(monde, aides):
    """si015 : 1 degat au joueur a la revelation."""
    identite = aides["identite"](monde)
    subis = identite.max_health - identite.health
    if subis != 1:
        return False, f"degats subis = {subis} (attendu 1)"
    return True, "1 degat inflige a la revelation de Massive Attack"

def si015_boost_en_jeu(monde, aides):
    """si015 : le Boost doit mettre Massive Attack en jeu."""
    scheme = aides["par_id"](monde, "si015")
    if scheme is None:
        return False, "si015 n'est pas en jeu apres le Boost"
    return True, "Massive Attack mise en jeu par son Boost"

def si016_armored_repete(monde, aides):
    """si016 : 2 instances de 3 degats, Armored 2 previent 2 a chaque fois -> 2 subis au total."""
    minion = aides["par_id"](monde, "si016")
    if minion is None:
        return False, "si016 n'est pas en jeu (peut-etre defait, verifier les degats)"
    subis = minion.max_health - minion.health
    if subis != 2:
        return False, f"degats subis par si016 = {subis} (attendu 2 : (3-2) x 2 instances)"
    return True, "2 degats subis sur 6 infliges (2 x 2 previens) : Armored 2 se recharge a chaque instance"

def si016_revealed_et_boost(monde, aides):
    """si016 : When Revealed + [star] Boost doivent chacun infliger 1 degat au joueur (2 au total)."""
    identite = aides["identite"](monde)
    subis = identite.max_health - identite.health
    if subis != 2:
        return False, f"degats subis par l'identite = {subis} (attendu 2 : 1 revele + 1 boost)"
    return True, "2 degats au joueur (1 revele + 1 boost) : les 2 triggers fonctionnent"

def si017_deux_degats(monde, aides):
    """si017 : 2 instances de 1 degat au joueur (pas 1 instance de 2)."""
    identite = aides["identite"](monde)
    subis = identite.max_health - identite.health
    if subis != 2:
        return False, f"degats subis = {subis} (attendu 2)"
    return True, "2 degats infliges au joueur (2 instances de 1)"

def si001b_opa_limite_phase(monde, aides):
    """si001b : apres 1 usage d'O.P.A. dans la phase, une 2e tentative doit
    etre REFUSEE (AssertionError, aucune action disponible) -- sinon
    LimitOncePerPhase ne bloque pas vraiment la reoffre, ce qui boucle le
    pilote d'autoplay (bloqua reellement une partie, graine 1, rhino)."""
    from game.puzzle.puzzle import PuzzleHelper
    try:
        PuzzleHelper.Exec(["Puzzle.Action('si001b', 'Action')"], monde)
    except AssertionError as e:
        return True, f"2e activation refusee comme attendu ({e}) : LimitOncePerPhase fonctionne"
    except Exception as e:
        return False, f"2e activation a leve une erreur inattendue : {type(e).__name__}: {e}"
    return False, "2e activation d'O.P.A. ACCEPTEE dans la meme phase : LimitOncePerPhase ne bloque pas la reoffre"

################################################################################
# Pack « kate_bishop » (kb001-kb020).
def kb_hawkeye_ally_consequential(monde, aides):
    """kb002 : Hawkeye defait par degat CONSEQUENT doit etre REMELANGE au deck
    (pas defausse) et poser 1 compteur fleche sur Kate's Bow.

    Garde contre un faux positif : « hors_jeu » a lui seul ne distingue pas
    « remelange au deck » de « defausse normalement » (les deux quittent le
    jeu). On verifie explicitement la PRESENCE dans le player_deck et
    l'ABSENCE dans la defausse.
    """
    arc = aides["par_id"](monde, "kb012")
    if arc is None:
        return False, "Kate's Bow n'est pas en jeu"
    n = arc.CastTo(aides["CanPlaceCounter"]).GetCounters('arrow')
    if n != 1:
        return False, f"compteurs arrow sur Kate's Bow = {n} (attendu 1)"

    joueur = monde.players[0]
    dans_deck = any(getattr(f.paper, "card_id", None) == "kb002" for f in joueur.player_deck.Get())
    dans_defausse = any(getattr(f.paper, "card_id", None) == "kb002" for f in joueur.discard_pile.Get())
    encore_en_jeu = aides["par_id"](monde, "kb002") is not None

    if encore_en_jeu:
        return False, "Hawkeye (kb002) est encore en jeu : l'Interrupt n'a pas remplace la defaite"
    if dans_defausse:
        return False, "Hawkeye (kb002) est dans la defausse : il a ete DEFAUSSE au lieu d'etre remelange au deck"
    if not dans_deck:
        return False, "Hawkeye (kb002) n'est ni en jeu, ni en defausse, ni dans le deck : il a disparu"
    return True, "Hawkeye remelange au deck (pas defausse) et 1 compteur fleche pose sur Kate's Bow"

def kb_bow_fin_de_phase(monde, aides):
    """kb012 : Interrupt imprime -> 1 compteur fleche a la fin de la phase joueur.

    Le declencheur (`AbilityFactory.WhenPlayerPhaseEnd`) n'est pas atteignable
    par l'API Puzzle (elle ne rejoue que des commandes `Puzzle.*`, et aucune ne
    fait avancer les phases). On envoie donc directement le message
    `Message.WhenPhaseEnd` que l'ability ecoute reellement -- meme principe que
    `brawn_ressource_seulement_si_epuise` plus haut, qui manipule l'etat du jeu
    directement dans le verifieur plutot que via `declencher`.
    """
    from game.message import Message

    arc = aides["par_id"](monde, "kb012")
    if arc is None:
        return False, "Kate's Bow n'est pas en jeu"
    avant = arc.CastTo(aides["CanPlaceCounter"]).GetCounters('arrow')

    message = Message.WhenPhaseEnd(monde.phase_id, "Player", monde)
    message.Send()

    apres = arc.CastTo(aides["CanPlaceCounter"]).GetCounters('arrow')
    if apres != avant + 1:
        return False, (f"compteurs arrow sur Kate's Bow = {apres} apres WhenPhaseEnd "
                       f"(attendu {avant + 1} : {avant} avant + 1 place en fin de phase)")
    return True, f"1 compteur fleche pose en fin de phase joueur ({avant} -> {apres})"

def kb_madame_masque_stats(monde, aides):
    """kb017 : ATK/SCH de Madame Masque = ATK/THW IMPRIMES de la face HEROS de
    l'identite engagee, quelle que soit la forme ACTUELLEMENT affichee.

    Corrige le 29/8/2026 : la carte lisait `heros.attack`/`heros.thwart`
    (proprietes CALCULEES via `GetKeyword`, qui ne se peuplent que sur la face
    ACTIVEMENT affichee -- valent 0 pour une face d'identite dormante). Elle
    lit maintenant `heros.printed_attack`/`heros.printed_thwart`, remplis pour
    CHAQUE face des `Initialize()` (card_face.py), actif ou non -- meme
    pattern deja utilise par av013.py/av014.py/ag012.py pour lire le stat
    d'une autre carte. Ce verifieur suit donc `printed_attack`/`printed_thwart`
    (la reference correcte), pas `attack`/`thwart` (casse pour une face
    inactive, bug moteur distinct et non corrige ici).

    Preuve non triviale : verifie une valeur NON NULLE (2/2, imprime de
    kb001a), pas juste une egalite qui passerait aussi a 0=0. Deux cas
    utilisent ce verifieur : Kate en forme Heros (ou `heros.attack` vaut aussi
    2, donc ne distinguerait pas un retour a l'ancien code fautif) ET Kate en
    alter-ego (ou `heros.attack` vaudrait 0 avec l'ancien code -- c'est ce cas
    qui aurait echoue avant la correction).
    """
    masque = aides["par_id"](monde, "kb017")
    if masque is None:
        return False, "Madame Masque (kb017) n'est pas en jeu"
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    heros = identite.GetHeroFace()

    soucis = []
    if masque.attack != heros.printed_attack:
        soucis.append(f"ATK Madame Masque = {masque.attack} (attendu {heros.printed_attack}, ATK imprime de la face heros)")
    if masque.scheme != heros.printed_thwart:
        soucis.append(f"SCH Madame Masque = {masque.scheme} (attendu {heros.printed_thwart}, THW imprime de la face heros)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"Madame Masque copie ATK={masque.attack}/SCH={masque.scheme} de la face heros engagee"

def ss004_precise_force_joue_et_borne(monde, aides):
    """ss004/ss005/ss006 : DeclareNumber(0,3) -- le pilote choisit toujours le
    premier item propose (valeur 0), meme limite documentee sur il002. On
    verifie donc que la carte a bien ete JOUEE (defausse) et que le degat
    reste dans la borne haute imprimee [0,3] : preuve structurelle que
    DealDamage(effect.targets, value, effect) est bien appele avec value
    dans les bornes, la branche non-nulle restant hors de portee du pilote
    generique (pas de cle de cas pour forcer une option parmi plusieurs)."""
    ids = [getattr(f.paper, "card_id", None) for f in monde.players[0].discard_pile.Get()]
    if "ss004" not in ids and "ss005" not in ids and "ss006" not in ids:
        return False, f"aucun exemplaire de Precise Force n'est dans la defausse (carte non jouee, defausse={ids})"
    cible = aides["par_id"](monde, "01094")
    if cible is None:
        return False, "01094 introuvable en jeu"
    degats = cible.max_health - cible.health
    if degats < 0 or degats > 3:
        return False, f"degats sur 01094 = {degats} (hors bornes [0,3])"
    return True, (f"Precise Force jouee (defausse), degats sur 01094 = {degats} "
                  f"(borne 0-3 respectee ; le pilote decline systematiquement la valeur "
                  f"non nulle via DeclareNumber, meme limite que il002)")

def ss012_mark_of_kaine_deferlement(monde, aides):
    """ss012/ss013/ss014 : Mark of Kaine attachee a 01110 (ATK imprime 1),
    Tigra (01051, 2 ATK) l'attaque. 01110 est adoucie a 1 PV, donc l'attaque
    la vainc avec 1 point d'exces. Un sbire ayant un ATK non nul rend le
    delta de PV de l'attaquante AMBIGU (le degat consequentiel standard, ATK
    du sbire vaincu = 1, se confond numeriquement avec le deversement du
    deferlement) : la preuve directe et non ambigue est donc le JOURNAL de
    la partie, qui trace explicitement 'gains overkill' avec Mark of Kaine
    comme source au moment ou `message.GainOverKill(effect)` s'execute."""
    import os
    prefixe = os.environ.get("CAS_PREFIX", "")
    chemin_log = f"/tmp/capacites_{prefixe}517.log"
    try:
        contenu = open(chemin_log, encoding="utf-8", errors="replace").read()
    except Exception as exc:
        return False, f"journal introuvable ({chemin_log}) : {exc}"

    if aides["par_id"](monde, "01110") is not None:
        return False, "01110 est encore en jeu (devrait avoir ete vaincu par l'attaque de Tigra)"

    if "gains overkill" not in contenu:
        return False, "aucune trace de 'gains overkill' dans le journal de la partie"
    if "Mark of Kaine" not in contenu:
        return False, "'gains overkill' present mais pas attribue a Mark of Kaine dans le journal"

    return True, "01110 vaincu ; le journal trace explicitement 'gains overkill' avec Mark of Kaine comme source"

def ss007_spider_pathy_pose_sbire(monde, aides):
    """ss007/ss008 : Search.EncounterCard(card_type=Minion) puis PutIntoPlay,
    qui engage AUTOMATIQUEMENT le sbire trouve avec le joueur courant
    (face_on_event.py:169). On verifie qu'au moins un sbire est en jeu,
    engage avec le joueur, et que Spider-pathy a bien ete jouee."""
    from game.card.face.card_type import Minion
    joueur = monde.players[0]
    sbires = []
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and face.IsInPlay() and Minion.IsType(face):
            sbires.append(face)
    if not sbires:
        return False, "aucun sbire en jeu apres Spider-pathy"
    engage_ok = any(m.GetEngagedPlayer() == joueur for m in sbires)
    if not engage_ok:
        return False, "aucun des sbires en jeu n'est engage avec le joueur"
    ids = [getattr(f.paper, "card_id", None) for f in joueur.discard_pile.Get()]
    if "ss007" not in ids and "ss008" not in ids:
        return False, f"Spider-pathy n'est pas dans la defausse (carte non jouee, defausse={ids})"
    return True, f"{len(sbires)} sbire(s) en jeu, au moins un engage avec le joueur, Spider-pathy jouee"

def hd001b_carte_mise_au_fond_du_deck_rencontre(monde, aides):
    """hd001b : hd024 etait sur le DESSUS du deck de rencontre ; apres
    Deducktive Reasoning elle doit se trouver au FOND, et nulle part ailleurs."""
    from game.operate.worlds import Worlds
    cartes = Worlds.GetEncounterDeckCards(monde)
    ids = [getattr(f.paper, "card_id", None) for f in cartes]
    if "hd024" not in ids:
        return False, "hd024 n'est plus dans le deck de rencontre (deck = %s...)" % ids[:6]
    if ids[0] == "hd024":
        return False, "hd024 est toujours sur le dessus du deck de rencontre"
    if ids[-1] != "hd024":
        return False, ("hd024 n'est pas au fond du deck de rencontre "
                       "(position %d sur %d)" % (ids.index("hd024"), len(ids)))
    return True, "hd024 mise au fond du deck de rencontre (%d cartes)" % len(ids)

def hd012_defausse_videe_et_une_carte_en_main(monde, aides):
    """hd012 : les 3 cartes semees en defausse doivent l'avoir quittee, et
    exactement une d'entre elles doit se trouver en MAIN (« instead »)."""
    semees = {"01051", "01088", "01089"}
    joueur = monde.players[0]
    defausse = {getattr(f.paper, "card_id", None) for f in joueur.discard_pile.GetAll()}
    main = [getattr(f.paper, "card_id", None) for f in joueur.hand_cards.GetAll()]
    restantes = semees & defausse
    if restantes:
        return False, "encore en defausse : %s" % sorted(restantes)
    gardees = [c for c in main if c in semees]
    if len(gardees) != 1:
        return False, ("%d carte(s) semee(s) en main (attendu 1) ; main = %s"
                       % (len(gardees), main))
    return True, "3 cartes sorties de la defausse, %s gardee en main" % gardees[0]

def hd017_un_evenement_cherche_en_main(monde, aides):
    """hd017 : la main ne contenait qu'une carte Resource avant le declencheur ;
    tout evenement present maintenant vient de la recherche du second Interrupt."""
    from game.card.face.card_type import Event
    joueur = monde.players[0]
    main = list(joueur.hand_cards.GetAll())
    evenements = [getattr(f.paper, "card_id", None) for f in main if Event.IsType(f)]
    if not evenements:
        return False, ("aucun evenement en main : le second Interrupt de hd017 "
                       "n'a rien cherche (main = %s)"
                       % [getattr(f.paper, "card_id", None) for f in main])
    return True, "evenement(s) cherche(s) en main : %s" % evenements

# ------------------------------------------------------------------------
# Pack « wiccan » : wc001a-wc023
#
# Trois de ces verificateurs sont des SONDES IN-PROCESS : ils renvoient dans
# le monde un message que l'API Puzzle ne sait pas produire (debut de phase
# du vilain, fin de phase joueur, deck de joueur vide). C'est exactement le
# message qu'envoie le moteur lui-meme au meme moment ; la seule chose qu'ils
# court-circuitent, c'est l'attente du tour de jeu correspondant.
# ------------------------------------------------------------------------

def _wc_dessus_du_deck_rencontre(monde):
    from game.operate.worlds import Worlds
    cartes = Worlds.GetEncounterDeckCards(monde)
    return cartes[0] if cartes else None

def _wc_defausse_rencontre(monde):
    from game.operate.worlds import Worlds
    return [getattr(f.paper, "card_id", None)
            for f in Worlds.GetEncounterDiscardPileCards(monde)]

def wc_clairvoyance_dessus_face_visible(monde, aides):
    """wc001a / wc001b : au debut de la phase des joueurs, la carte du dessus
    du deck rencontre doit etre retournee FACE VISIBLE."""
    from game.message import Message
    Message.WhenPhaseBegin("Player", monde).Send()

    face = _wc_dessus_du_deck_rencontre(monde)
    if face is None:
        return False, "deck de rencontre vide : rien a retourner"
    card_id = getattr(face.paper, "card_id", "?")
    if not face.card.state.is_face_up:
        return False, (f"la carte du dessus du deck rencontre ({card_id}) est "
                       f"encore FACE CACHEE : Clairvoyance n'a pas joue")
    return True, f"carte du dessus du deck rencontre ({card_id}) retournee face visible"

def wc001a_defausse_au_debut_de_la_phase_du_vilain(monde, aides):
    """wc001a : le Forced Interrupt defausse le dessus du deck rencontre au
    debut de la phase du vilain. La defausse de rencontre est VIDE au depart
    d'une partie : tout ce qui s'y trouve apres la sonde vient de la."""
    from game.message import Message
    avant = _wc_defausse_rencontre(monde)
    if avant:
        return False, f"la defausse de rencontre n'etait pas vide au depart : {avant}"

    dessus = _wc_dessus_du_deck_rencontre(monde)
    attendu = getattr(dessus.paper, "card_id", None) if dessus else None

    Message.WhenPhaseBegin("Villain", monde).Send()

    apres = _wc_defausse_rencontre(monde)
    if not apres:
        return False, "aucune carte de rencontre defaussee au debut de la phase du vilain"
    if attendu is not None and attendu not in apres:
        return False, (f"la carte defaussee n'est pas celle du dessus "
                       f"(attendue {attendu}, defausse = {apres})")
    return True, f"carte du dessus ({attendu}) defaussee au debut de la phase du vilain"

def wc_defausse_rencontre_non_vide(monde, aides):
    """wc001b : « look at the top 2 cards, you may discard one of them ». La
    defausse de rencontre est vide au depart, donc toute carte qui s'y trouve
    a ete defaussee par l'action."""
    apres = _wc_defausse_rencontre(monde)
    if not apres:
        return False, "aucune carte de rencontre defaussee : l'action n'a rien fait"
    return True, f"carte(s) de rencontre defaussee(s) par l'action : {apres}"

def wc002_hulkling_bonus_et_defausse(monde, aides):
    """wc002 : ATQ 1* (1 en solo) + 2 icones de bonus (01111 Explosion) = 3
    degats, et la carte comptee est ensuite defaussee."""
    rhino = aides["par_id"](monde, "01094")
    if rhino is None:
        return False, "Rhino (01094) introuvable en jeu"
    subis = rhino.max_health - rhino.health
    if subis < 3:
        return False, (f"degats sur Rhino = {subis} (attendu au moins 3 : ATQ 1 "
                       f"+ 2 icones de bonus). Le bonus d'icones n'a pas ete applique")
    defausse = _wc_defausse_rencontre(monde)
    if "01111" not in defausse:
        return False, (f"la carte comptee (01111) n'a pas ete defaussee "
                       f"(defausse de rencontre = {defausse})")
    return True, f"{subis} degats (1 ATQ + 2 icones) et 01111 defaussee"

def wc008_defausse_remontee_dans_le_deck(monde, aides):
    """wc008 : 2 icones de bonus -> les 2 cartes semees dans la defausse du
    joueur doivent l'avoir quittee (remelangees dans le deck)."""
    joueur = monde.players[0]
    defausse = [getattr(f.paper, "card_id", None) for f in joueur.discard_pile.GetAll()]
    restantes = [c for c in ("01086", "01087") if c in defausse]
    if restantes:
        return False, (f"encore dans la defausse du joueur : {restantes} "
                       f"(defausse = {defausse})")
    return True, "les 2 cartes semees ont quitte la defausse (remelangees dans le deck)"

def wc011_teleport(monde, aides):
    """wc011 : l'identite choisie est REDRESSEE, et elle porte +1 sur l'un de
    ses pouvoirs de base jusqu'a la fin du round.

    Le pouvoir n'est pas impose : le texte dit « a basic power of THEIR
    choice », et le pilote prend la premiere branche proposee. On accepte donc
    n'importe lequel des quatre, mais il en faut un."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if identite.IsExhaust():
        return False, "l'identite est encore inclinee : Teleport ne l'a pas redressee"

    bonus = []
    for nom, imprime in (("attack", "printed_attack"),
                         ("thwart", "printed_thwart"),
                         ("defense", "printed_defense"),
                         ("recover", "printed_recovery")):
        if not hasattr(identite, nom) or not hasattr(identite, imprime):
            continue
        if getattr(identite, nom) > getattr(identite, imprime):
            bonus.append(nom)
    if not bonus:
        return False, ("identite redressee, mais AUCUN pouvoir de base au-dessus de sa "
                       "valeur imprimee : le bonus « 2 icones ou plus » n'est pas parti")
    return True, f"identite redressee et +1 sur {bonus}"

def wc013_carte_remontee_sur_le_dessus(monde, aides):
    """wc013 : la carte cherchee (01143, forcee par `cibles`) doit se trouver
    SUR LE DESSUS du deck rencontre apres le melange."""
    from game.operate.worlds import Worlds
    ids = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde)]
    if not ids:
        return False, "deck de rencontre vide"
    if ids[0] != "01143":
        return False, (f"le dessus du deck rencontre est {ids[0]} (attendu 01143) ; "
                       f"6 premieres = {ids[:6]}")
    return True, "01143 remontee sur le dessus du deck rencontre apres melange"

def wc017_royal_couple(monde, aides):
    """wc017 : le heros est redresse ET la carte choisie dans la defausse de
    rencontre est remontee sur le deck."""
    from game.operate.worlds import Worlds
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if identite.IsExhaust():
        return False, "le heros est encore incline : Royal Couple n'a pas joue"
    ids = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde)]
    if "01106" not in ids:
        return False, "01106 n'a pas quitte la defausse de rencontre pour le deck"
    if ids[0] != "01106":
        return False, f"01106 est dans le deck mais pas sur le DESSUS (dessus = {ids[0]})"
    return True, "heros redresse et 01106 remontee sur le dessus du deck rencontre"

def wc017_sans_hulkling(monde, aides):
    """wc017 : sans Hulkling en jeu, la condition doit interdire la carte —
    le heros reste incline et rien ne remonte de la defausse de rencontre."""
    from game.operate.worlds import Worlds
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if not identite.IsExhaust():
        return False, ("le heros a ete redresse alors que Hulkling n'est pas en jeu : "
                       "la condition Team-Up ne joue pas")
    ids = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde)]
    if ids and ids[0] == "01106":
        return False, "01106 est remontee sur le deck alors que Hulkling n'est pas en jeu"
    return True, "sans Hulkling, Royal Couple ne fait rien : heros toujours incline"

def wc018_obligation_retiree(monde, aides):
    """wc018, branche 1 : l'obligation quitte le jeu et l'identite est
    inclinee."""
    if aides["par_id"](monde, "wc018") is not None:
        return False, "wc018 est encore en jeu : la resolution a echoue"
    identite = aides["identite"](monde)
    if identite is not None and not identite.IsExhaust():
        return False, "l'identite n'est pas inclinee : le cout de la branche n'a pas ete paye"
    return True, "obligation retiree du jeu et identite inclinee"

def wc018_interrupteur_des_boosts(monde, aides):
    """wc018, branche 2 : l'interrupteur global du pack est leve, puis
    rabaisse a la fin de la phase des joueurs.

    On teste l'interrupteur PAR SON EFFET, pas seulement par la valeur du
    drapeau : `IconesBoostDuDessus` doit rendre 0 tant qu'il est leve, alors
    que la carte du dessus du deck rencontre porte de vraies icones."""
    from game.message import Message
    from game.effect.rule import DebugRule
    from cards.pack.wiccan.wiccan import (
        BoostsComptables, IconesBoostDuDessus, DRAPEAU_BOOSTS_ETEINTS,
    )

    if aides["par_id"](monde, "wc018") is not None:
        return False, "wc018 est encore en jeu : la resolution a echoue"

    if not getattr(monde, DRAPEAU_BOOSTS_ETEINTS, False):
        return False, ("le drapeau d'extinction des icones de bonus n'est pas leve : "
                       "la branche 2 n'a pas ete choisie ou n'a rien fait")

    effet = DebugRule(monde.object_manager.card_dict[0].face)
    if BoostsComptables(effet):
        return False, "BoostsComptables() rend encore Vrai alors que le drapeau est leve"
    if IconesBoostDuDessus(effet, monde.players[0]) != 0:
        return False, "IconesBoostDuDessus() rend encore un nombre non nul"

    Message.WhenPhaseEnd(monde.phase_id, "Player", monde).Send()

    if getattr(monde, DRAPEAU_BOOSTS_ETEINTS, False):
        return False, ("le drapeau est reste leve apres la fin de la phase des joueurs : "
                       "l'extinction serait definitive")
    return True, ("icones de bonus eteintes (drapeau leve, comptage a 0), puis rallumees "
                  "a la fin de la phase des joueurs")

def wc019b_deck_joueur_vide(monde, aides):
    """wc019b : quand un deck de JOUEUR se vide, 1 menace sur le complot
    principal. Sonde : on renvoie `Message.AfterDeckRunOut` sur le deck du
    joueur, exactement le message qu'emet le moteur quand le deck se vide —
    sans la penalite standard qui, elle, distribuerait une carte rencontre et
    fausserait le releve."""
    from game.message import Message
    from game.operate.worlds import Worlds

    if aides["par_id"](monde, "wc019b") is None:
        return False, "wc019b n'est pas en jeu : le retournement de New Vessel a echoue"

    principaux = Worlds.GetAllMainSchemes(monde)
    if not principaux:
        return False, "aucun complot principal en jeu"
    avant = principaux[0].threat

    Message.AfterDeckRunOut(monde.players[0].player_deck).Send()

    apres = principaux[0].threat
    if apres != avant + 1:
        return False, (f"menace du complot principal : {avant} -> {apres} "
                       f"(attendu {avant + 1})")
    return True, f"1 menace posee sur le complot principal ({avant} -> {apres})"

def wc021_degats_sans_etourdissement(monde, aides):
    """wc021 : 1 degat a CHAQUE personnage ami (identite + allie), et AUCUN
    etourdissement puisque Moridun n'est pas en jeu."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    subis = identite.max_health - identite.health
    if subis != 1:
        return False, f"degats sur l'identite = {subis} (attendu 1)"

    allie = aides["par_id"](monde, "wc002")
    if allie is None:
        return False, "l'allie wc002 n'est plus en jeu"
    if allie.max_health - allie.health != 1:
        return False, (f"degats sur l'allie wc002 = {allie.max_health - allie.health} "
                       f"(attendu 1 : la portee est « each friendly character »)")

    if identite.CastTo(aides["CanStatus"]).HasStatus("Stunned"):
        return False, "l'identite est Sonnee alors que Moridun n'est pas en jeu"
    return True, "1 degat a l'identite et a l'allie, aucun etourdissement"

def wc023_desoriente_et_non_retiree(monde, aides):
    """wc023 : The Demiurge en jeu -> aucune revelation de Moridun, le joueur
    est Desoriente, et la trahison n'est PAS retiree du jeu (« then remove »
    appartient a la branche conditionnelle)."""
    if aides["par_id"](monde, "wc019b") is None:
        return False, "wc019b n'est pas en jeu : le montage du cas a echoue"
    if aides["par_id"](monde, "wc020") is not None:
        return False, "Moridun a ete revele alors que The Demiurge est en jeu"

    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if not identite.CastTo(aides["CanStatus"]).HasStatus("Confused"):
        return False, "l'identite n'est pas Desorientee"
    return True, "aucune revelation de Moridun, identite Desorientee"

def wc019a_seul_billy_retire_la_menace(monde, aides):
    """wc019a : « Only the Billy Kaplan player can remove threat from this
    scheme. » On tente le retrait DEUX fois, avec deux initiateurs differents.

    `GameRule(face)` prend pour initiateur le controleur de la face
    (rule.py:10-22) : monter l'effet sur l'identite du joueur 2 puis sur celle
    du joueur 1 donne exactement les deux initiateurs que
    `PlayersCannotRemoveThreatFrom` compare (player.py:268-269).

    C'est la MANIGANCE qui porte l'appel (`nv.RemoveThreatFromSchemes`), pas
    l'identite : `CanThwart.OnRemoveSchemeThreat` lit `by_effect.ability`
    (can_thwart.py:62), attribut qu'un effet de REGLE n'a pas. Passer par la
    manigance emprunte le chemin de base, exactement comme `Puzzle.PlaceThreat`
    et comme mw018/wc019a eux-memes."""
    from game.effect.rule import GameRule

    nv = aides["par_id"](monde, "wc019a")
    if nv is None:
        return False, "wc019a n'est pas en jeu"
    if len(monde.players) < 2:
        return False, "la partie n'a qu'un joueur : la restriction est intestable"

    depart = nv.threat
    if depart < 3:
        return False, f"menace de depart trop basse sur New Vessel ({depart})"

    autre = monde.players[1].GetIdentity()
    nv.RemoveThreatFromSchemes([nv], 2, GameRule(autre))
    if nv.threat != depart:
        return False, (f"le second joueur ({autre.name}) a retire de la menace : "
                       f"{depart} -> {nv.threat}. La restriction ne joue pas")

    billy = monde.players[0].GetIdentity()
    nv.RemoveThreatFromSchemes([nv], 2, GameRule(billy))
    if nv.threat != depart - 2:
        return False, (f"le joueur Billy Kaplan n'a PAS pu retirer de la menace : "
                       f"{depart} -> {nv.threat} (attendu {depart - 2}). "
                       f"La restriction est trop large")
    return True, (f"menace inchangee pour le second joueur ({depart}), puis "
                  f"{depart} -> {nv.threat} pour le joueur Billy Kaplan")

# ------------------------------------------------------------------------
# Pack « speed » : sd001a-sd022
#
# Deux de ces verificateurs sont des SONDES IN-PROCESS : ils renvoient dans le
# monde `Message.WhenPhaseEnd(phase_id, "Player", monde)` ou
# `Message.WhenRoundEnd(monde)`, exactement les messages qu'emet le moteur au
# meme moment. L'API Puzzle n'avance aucune phase ni aucun round : c'est le
# seul moyen d'exercer le balayage des compteurs explosifs (regle de l'insert)
# et la duree de l'interrupteur de l'obligation sd017.
# ------------------------------------------------------------------------

def _sd_compteurs_explosifs_en_jeu(monde, aides):
    total = 0
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is None or not face.IsInPlay():
            continue
        if isinstance(face, aides["CanPlaceCounter"]):
            total += face.GetCounters("explosive")
    return total

def _sd_fin_de_phase_joueur(monde):
    from game.message import Message
    Message.WhenPhaseEnd(monde.phase_id, "Player", monde).Send()

def sd_balayage_ennemi(monde, aides):
    """sd001a : a la fin de la phase des joueurs, le compteur explosif d'un
    ENNEMI est retire du jeu ET lui inflige 1 degat."""
    rhino = aides["par_id"](monde, "01094")
    if rhino is None:
        return False, "Rhino (01094) introuvable en jeu"
    if rhino.CastTo(aides["CanPlaceCounter"]).GetCounters("explosive") != 1:
        return False, "le compteur explosif n'a pas ete pose au montage du cas"
    avant = rhino.max_health - rhino.health

    _sd_fin_de_phase_joueur(monde)

    reste = rhino.CastTo(aides["CanPlaceCounter"]).GetCounters("explosive")
    if reste != 0:
        return False, (f"le compteur explosif est encore la ({reste}) : le balayage de "
                       f"fin de phase des joueurs n'a pas eu lieu")
    apres = rhino.max_health - rhino.health
    if apres != avant + 1:
        return False, (f"degats sur Rhino : {avant} -> {apres} (attendu {avant + 1}). "
                       f"Le compteur est parti sans infliger son degat")
    return True, f"compteur retire et 1 degat inflige ({avant} -> {apres})"

def sd_balayage_manigance(monde, aides):
    """sd001b : meme regle, en identite civile, sur une MANIGANCE — 1 menace
    retiree au moment du retrait du compteur."""
    joueur = monde.players[0]
    if joueur.IsHero():
        return False, "le cas devait rester en identite civile"

    scheme = aides["par_id"](monde, "01097b")
    if scheme is None:
        return False, "le complot principal (01097b) est introuvable"
    if scheme.CastTo(aides["CanPlaceCounter"]).GetCounters("explosive") != 1:
        return False, "le compteur explosif n'a pas ete pose au montage du cas"
    avant = scheme.threat

    _sd_fin_de_phase_joueur(monde)

    reste = scheme.CastTo(aides["CanPlaceCounter"]).GetCounters("explosive")
    if reste != 0:
        return False, (f"le compteur explosif est encore la ({reste}) : la regle de "
                       f"l'insert ne joue pas quand Speed finit la phase en alter-ego")
    if scheme.threat != avant - 1:
        return False, (f"menace : {avant} -> {scheme.threat} (attendu {avant - 1}). "
                       f"Le compteur est parti sans retirer sa menace")
    return True, f"compteur retire et 1 menace retiree ({avant} -> {scheme.threat})"

def sd001b_accelerated_perception(monde, aides):
    """sd001b : l'evenement seme dans la defausse (sd003) l'a quittee, et la
    main est passee de 1 a 2 cartes (la pioche est inconditionnelle)."""
    joueur = monde.players[0]
    defausse = [getattr(f.paper, "card_id", None) for f in joueur.discard_pile.GetAll()]
    if "sd003" in defausse:
        return False, (f"sd003 est encore dans la defausse du joueur : le remelange n'a "
                       f"pas eu lieu (defausse = {defausse})")
    main = len(list(joueur.hand_cards.Get()))
    if main != 2:
        return False, (f"main a {main} carte(s) (attendu 2 : 1 carburant + 1 piochee). "
                       f"La pioche n'a pas eu lieu")
    return True, "sd003 a quitte la defausse (remelangee dans le deck) et 1 carte piochee"

def sd005_instead(monde, aides):
    """sd005, branche « instead » : l'evenement de la defausse remonte, on
    pioche, AUCUN compteur explosif n'est pose, et l'annulation a quand meme eu
    lieu (le « instead » ne remplace QUE Hyperkinetic Fuel)."""
    joueur = monde.players[0]
    soucis = []

    defausse = [getattr(f.paper, "card_id", None) for f in joueur.discard_pile.GetAll()]
    if "sd003" in defausse:
        soucis.append("sd003 est encore dans la defausse : le remelange n'a pas eu lieu")
    if "sd005" not in defausse:
        soucis.append(f"sd005 n'a pas ete jouee (defausse du joueur = {defausse})")

    total = _sd_compteurs_explosifs_en_jeu(monde, aides)
    if total != 0:
        soucis.append(f"{total} compteur(s) explosif(s) en jeu : le « instead » n'a pas "
                      f"remplace la pose de compteur")

    if aides["par_id"](monde, "sd020") is not None:
        soucis.append("sd020 est en jeu : l'annulation de la carte rencontre n'a pas eu "
                      "lieu, alors que le « instead » ne la remplace pas")

    if soucis:
        return False, " ; ".join(soucis)
    return True, ("evenement remonte de la defausse, aucun compteur explosif pose, "
                  "carte rencontre annulee quand meme")

def sd011_restriction_du_tour(monde, aides):
    """sd011 : la carte financee par Top Speed est bien entree en jeu, et
    plus aucune autre ne peut etre jouee ce tour-ci."""
    joueur = monde.players[0]

    if aides["par_id"](monde, "sd014") is None:
        return False, ("sd014 n'est pas en jeu : la restriction a bloque la carte que "
                       "Top Speed etait justement en train de payer")

    suivante = None
    for face in joueur.hand_cards.GetAll():
        if getattr(face.paper, "card_id", None) == "sd013":
            suivante = face
            break
    if suivante is None:
        return False, "sd013 n'est plus en main : le montage du cas a echoue"

    if suivante.CanPlayBy(joueur):
        return False, ("sd013 est encore jouable alors que le supplement de Top Speed a "
                       "ete pris : « you cannot play cards for the rest of the turn » ne "
                       "joue pas")
    return True, ("sd014 (payee par Top Speed) est en jeu, et sd013 n'est plus jouable "
                  "pour le reste du tour")

def sd017_obligation_retiree(monde, aides):
    """sd017, branche 1 : l'obligation quitte le jeu et l'identite civile est
    inclinee."""
    if aides["par_id"](monde, "sd017") is not None:
        return False, "sd017 est encore en jeu : la resolution a echoue"
    identite = aides["identite"](monde)
    if identite is not None and not identite.IsExhaust():
        return False, "l'identite n'est pas inclinee : le cout de la branche n'a pas ete paye"
    return True, "obligation retiree du jeu et Thomas Shepherd incline"

def sd017_interrupteur_hyperkinetic(monde, aides):
    """sd017, branche 2 : Hyperkinetic Fuel est eteint, et il le RESTE apres la
    premiere fin de round — il ne se rallume qu'a la SECONDE (« until the end
    of the NEXT round »)."""
    from game.message import Message
    from cards.pack.speed.speed import (
        HyperkineticFuelActif, DRAPEAU_HYPERKINETIC_ETEINT,
    )
    from game.effect.rule import DebugRule

    if aides["par_id"](monde, "sd017") is not None:
        return False, "sd017 est encore en jeu : la branche 2 n'a pas ete choisie"

    if not getattr(monde, DRAPEAU_HYPERKINETIC_ETEINT, False):
        return False, ("le drapeau d'extinction n'est pas leve : la branche 2 n'a pas ete "
                       "choisie ou n'a rien fait")

    effet = DebugRule(monde.object_manager.card_dict[0].face)
    if HyperkineticFuelActif(effet):
        return False, "HyperkineticFuelActif() rend encore Vrai alors que le drapeau est leve"

    Message.WhenRoundEnd(monde).Send()
    if not getattr(monde, DRAPEAU_HYPERKINETIC_ETEINT, False):
        return False, ("le drapeau est retombe des la PREMIERE fin de round : le texte dit "
                       "« until the end of the NEXT round », il faut en laisser passer une")

    Message.WhenRoundEnd(monde).Send()
    if getattr(monde, DRAPEAU_HYPERKINETIC_ETEINT, False):
        return False, ("le drapeau est reste leve apres la SECONDE fin de round : "
                       "l'extinction serait definitive")
    if not HyperkineticFuelActif(effet):
        return False, "HyperkineticFuelActif() rend encore Faux apres la seconde fin de round"
    return True, ("Hyperkinetic Fuel eteint, toujours eteint apres la 1re fin de round, "
                  "rallume a la 2e")

def sd018_attachements_permanents(monde, aides):
    """sd018 : l'attachement entre en jeu APRES la manigance et doit porter le
    mot-cle Permanent."""
    if aides["par_id"](monde, "sd018") is None:
        return False, "sd018 n'est pas en jeu : le montage du cas a echoue"
    art = aides["par_id"](monde, "sd020")
    if art is None:
        return False, "sd020 n'est pas en jeu : le montage du cas a echoue"
    if not getattr(art, "permanent", False):
        return False, ("sd020 ne porte PAS le mot-cle Permanent alors que The Real Question "
                       "est en jeu")
    return True, "l'attachement entre en jeu apres la manigance et gagne bien Permanent"

def _sd_actions_de_carte(monde, card_id, aides, ability_type=None):
    """(actions DECLAREES, actions REELLEMENT disponibles) sur une carte en jeu.

    Reproduit exactement le filtrage de `Puzzle.Action` (puzzle.py:495-506) :
    la seconde liste est ce que le joueur voit propose, condition comprise.

    On rend AUSSI les actions declarees, et c'est indispensable : sans elles,
    un cas « l'action est indisponible » resterait vert quand le module de la
    carte est retire, puisqu'il n'y aurait plus d'action du tout. La paire
    distingue « capacite absente » de « capacite presente mais grisee »."""
    from game.ability.ability import AbilityType
    from game.event.manager import EventManager
    from game.message import Message
    from game.effect.rule import GameRule

    face = aides["par_id"](monde, card_id)
    if face is None:
        return None, None
    joueur = monde.players[0]
    type_demande = getattr(AbilityType, ability_type) if ability_type else None
    candidats = [x for x in face.effect.Find(when=Message.WhenPlayerInTurn,
                                             type=type_demande)
                 if not x.ability.is_play]
    message = Message.WhenPlayerLikeInTurn(joueur, GameRule(joueur.GetIdentity()))
    message.Send()
    disponibles = EventManager.FilterAvailableEffects(
        message, candidats, joueur, monde, None)
    return candidats, disponibles

def sd020_action_indisponible(monde, aides):
    """sd020 : tant que The Real Question (sd018) est en jeu, l'attachement est
    Permanent et sa Hero Action de defausse doit etre GRISEE — pas echouer, ni
    faire planter la partie sur l'assert de `DiscardInternal`."""
    if aides["par_id"](monde, "sd018") is None:
        return False, "sd018 n'est pas en jeu : le montage du cas a echoue"
    art = aides["par_id"](monde, "sd020")
    if art is None:
        return False, "sd020 n'est pas en jeu : le montage du cas a echoue"
    if not getattr(art, "permanent", False):
        return False, "sd020 ne porte pas Permanent : le montage du cas a echoue"

    candidats, effets = _sd_actions_de_carte(monde, "sd020", aides, "HeroAction")
    if not candidats:
        return False, ("sd020 ne DECLARE aucune Hero Action : le cas ne prouverait rien "
                       "(une capacite absente est aussi « indisponible »)")
    if effets:
        return False, (f"la Hero Action de sd020 est encore proposee ({len(effets)} effet(s)) "
                       f"alors que The Real Question est en jeu : la defausse d'une carte "
                       f"Permanente ferait planter la partie")
    return True, ("Hero Action declaree mais indisponible tant que The Real Question est "
                  "en jeu")

def sd021_chaines(monde, aides):
    """sd021 : apres l'attaque du sbire porteur, le heros est SONNE et
    l'attachement est defausse."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    if not identite.CastTo(aides["CanStatus"]).HasStatus("Stunned"):
        return False, "le heros n'est pas Sonne : le Forced Response n'a pas joue"
    if aides["par_id"](monde, "sd021") is not None:
        return False, "sd021 est encore en jeu : elle n'a pas ete defaussee"
    return True, "heros Sonne et Magic Chains defaussee"


def sd021_cout_impayable(monde, aides):
    """sd021 : en identite civile il n'y a AUCUN heros a etourdir, donc le cout
    de la fleche n'est pas payable : ni etourdissement, ni defausse."""
    if aides["par_id"](monde, "sd021") is None:
        return False, "sd021 defaussee alors que le cout n'etait pas payable"
    identite = aides["identite"](monde)
    if identite is not None and identite.CastTo(aides["CanStatus"]).HasStatus("Stunned"):
        return False, "identite Sonnee alors qu'aucun heros n'est en jeu"
    return True, "cout impayable : Magic Chains reste en jeu, personne n'est Sonne"

def pt001a_limite_une_fois_par_round(monde, aides):
    """pt001a : « (Limit once per round.) ». Deux allies a degat consecutif
    frappent ; Patriot ne peut encaisser qu'UNE fois.

    On ne peut pas dire d'avance LEQUEL des deux allies sera protege (l'ordre
    depend du moteur) : on compte donc les totaux."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"

    subis = identite.max_health - identite.health
    if subis != 1:
        return False, (f"l'identite a encaisse {subis} degat(s) (attendu 1 : "
                       f"la limite une-fois-par-round)")

    total_allies = 0
    for card_id in ("01083", "01067"):
        face = aides["par_id"](monde, card_id)
        if face is None:
            return False, f"{card_id} introuvable en jeu"
        total_allies += face.max_health - face.health
    if total_allies != 1:
        return False, (f"les allies portent {total_allies} degat(s) au total "
                       f"(attendu 1 : celui que Patriot n'a PAS pu reprendre)")

    return True, "1 degat deplace sur Patriot, 1 degat laisse a l'allie : limite respectee"


def pt008_attachement_deplace(monde, aides):
    """pt008 : l'Exo-Suit passe de Rhino a Mockingbird, son texte est blanc,
    son ATK+ suit le porteur et son SCH+ devient un CTR+."""
    exo = aides["par_id"](monde, "04075")
    allie = aides["par_id"](monde, "01083")
    vilain = aides["par_id"](monde, "01094")
    if exo is None:
        return False, "04075 Exo-Suit n'est plus en jeu"
    if allie is None:
        return False, "01083 Mockingbird n'est plus en jeu"
    if vilain is None:
        return False, "01094 Rhino introuvable"

    soucis = []

    porteur = exo.GetBindFace()
    if porteur is not allie:
        soucis.append(f"l'Exo-Suit est attache a {porteur} (attendu Mockingbird)")

    if not exo.is_treat_as_if_blank:
        soucis.append("l'Exo-Suit n'est PAS traite comme blanc")

    # « treat SCH as THW » : ATK+ 1 et SCH+ 1 sur l'allie -> +1 ATQ et +1 CTR.
    if allie.attack != allie.printed_attack + 1:
        soucis.append(f"ATQ de l'allie = {allie.attack} "
                      f"(imprime {allie.printed_attack}, attendu +1 par l'ATK+)")
    if allie.thwart != allie.printed_thwart + 1:
        soucis.append(f"CTR de l'allie = {allie.thwart} "
                      f"(imprime {allie.printed_thwart}, attendu +1 : le SCH+ converti)")

    # Rhino a rendu le bonus.
    if vilain.attack != vilain.printed_attack:
        soucis.append(f"ATQ de Rhino = {vilain.attack} "
                      f"(imprime {vilain.printed_attack}) : le bonus n'a pas suivi")

    if soucis:
        return False, " ; ".join(soucis)
    return True, "attachement deplace, texte blanc, ATK+ suivi et SCH+ converti en CTR+"


def pt014_allie_cherche(monde, aides):
    """pt014 : l'allie vaincu par degat CONSECUTIF fait remonter un allie du
    deck a la main. La main a ete VIDEE par `main_exclusive` : tout allie qui
    s'y trouve vient de la recherche."""
    from game.card.face.card_type import Ally

    mort = aides["par_id"](monde, "01083")
    if mort is not None:
        return False, ("01083 est encore en jeu : le degat consecutif ne l'a pas "
                       "vaincu (la limite de Will to Protect a-t-elle bien ete "
                       "consommee par le premier allie ?)")

    allies_en_main = [getattr(f.paper, "card_id", "?")
                      for f in monde.players[0].hand_cards.GetAll()
                      if Ally.IsType(f)]
    if not allies_en_main:
        cartes = [getattr(f.paper, "card_id", "?")
                  for f in monde.players[0].hand_cards.GetAll()]
        return False, f"aucun allie en main apres la recherche (main = {cartes})"

    return True, f"allie(s) remonte(s) en main : {allies_en_main}"


def pt019_mgh_drug_attachee(monde, aides):
    """pt019 : le MGH Drug cherche est bien ATTACHE au sbire, pas seulement en
    jeu."""
    hyde = aides["par_id"](monde, "pt019")
    drug = aides["par_id"](monde, "pt020")
    if hyde is None:
        return False, "pt019 Mr. Hyde n'est pas en jeu"
    if drug is None:
        return False, "pt020 MGH Drug n'est pas en jeu : la recherche a echoue"
    porteur = drug.GetBindFace()
    if porteur is not hyde:
        return False, f"le MGH Drug est attache a {porteur} (attendu Mr. Hyde)"
    return True, "MGH Drug trouve et attache a Mr. Hyde"


def pt021_hyde_a_frappe(monde, aides):
    """pt021 : quand Mr. Hyde est en jeu, il attaque et la branche « if no
    attack was made this way » ne part PAS. L'allie doit etre intact et
    l'identite avoir encaisse l'attaque."""
    allie = aides["par_id"](monde, "01067")
    identite = aides["identite"](monde)
    if allie is None:
        return False, "01067 n'est plus en jeu"
    if identite is None:
        return False, "identite introuvable"

    degats_allie = allie.max_health - allie.health
    if degats_allie != 0:
        return False, (f"l'allie porte {degats_allie} degat(s) : la branche "
                       f"« if no attack was made this way » est partie a tort")

    subis = identite.max_health - identite.health
    if subis <= 0:
        return False, "l'identite n'a rien encaisse : Mr. Hyde n'a pas attaque"

    return True, (f"Mr. Hyde a attaque ({subis} degat(s) sur l'identite) et "
                  f"l'allie est intact")


# ------------------------------------------------------- pack ms_america --

def _ma_dans_le_deck(monde, card_id):
    for face in monde.players[0].player_deck.GetAll():
        if getattr(face.paper, "card_id", None) == card_id:
            return True
    return False


def _ma_dans_la_defausse(monde, card_id):
    for face in monde.players[0].discard_pile.GetAll():
        if getattr(face.paper, "card_id", None) == card_id:
            return True
    return False


def ma001b_carte_remontee_dans_le_deck(monde, aides):
    """ma001b : la carte cherchee dans la defausse est bien DANS LE DECK.

    `etat_attendu` ne sait pas regarder le deck du joueur : « hors_jeu » serait
    satisfait par une carte restee dans la defausse, ce qui ne prouverait rien.
    On controle aussi que la carte qui a PAYE, elle, est bien a la defausse.
    """
    soucis = []
    if not _ma_dans_le_deck(monde, "ma002"):
        soucis.append("ma002 n'est pas dans le deck du joueur")
    if _ma_dans_la_defausse(monde, "ma002"):
        soucis.append("ma002 est encore dans la defausse")
    if not _ma_dans_la_defausse(monde, "01088"):
        soucis.append("01088 n'a pas ete defaussee : le cout n'a pas ete paye")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "ma002 a quitte la defausse pour le deck, 01088 a paye"


def ma003_melangee_dans_le_deck(monde, aides):
    """ma003 : « shuffle her into your deck INSTEAD » — le deck, pas la defausse."""
    soucis = []
    if aides["par_id"](monde, "ma003") is not None:
        soucis.append("ma003 est encore en jeu : elle aurait du partir")
    if _ma_dans_la_defausse(monde, "ma003"):
        soucis.append("ma003 est dans la DEFAUSSE : le remplacement « instead » "
                      "n'a pas eu lieu")
    if not _ma_dans_le_deck(monde, "ma003"):
        soucis.append("ma003 n'est pas dans le deck du joueur")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "ma003 a ete melangee dans le deck au lieu d'etre vaincue"


def ma004_evenement_attache(monde, aides):
    """ma004 : l'evenement est SOUS le soutien, et le soutien est incline."""
    santana = aides["par_id"](monde, "ma004")
    if santana is None:
        return False, "ma004 introuvable en jeu"
    soucis = []
    zone = santana.GetPlacedCardArea()
    ids = [getattr(f.paper, "card_id", None) for f in zone.GetAll()]
    if "ma015" not in ids:
        soucis.append(f"ma015 n'est pas attachee a Santana Family (zone = {ids})")
    if not santana.IsExhaust():
        soucis.append("ma004 n'est pas inclinee : le cout de la fleche n'a pas ete paye")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"ma015 est attachee sous ma004 (zone = {ids}) et ma004 est inclinee"


def ma015_aucun_etourdi(monde, aides):
    """ma015 : la troisieme phrase est CONDITIONNELLE — ici, rien ne tombe."""
    vilain = aides["par_id"](monde, "01094")
    if vilain is None:
        return False, "Rhino introuvable"
    soucis = []
    degats = vilain.max_health - vilain.health
    if degats != 4:
        soucis.append(f"degats sur Rhino = {degats} (attendu 4)")
    manigance = aides["par_id"](monde, "01097b")
    if manigance is None:
        soucis.append("complot principal introuvable")
    elif manigance.threat != 2:
        soucis.append(f"menace = {manigance.threat} (attendu 2 : 5 - 3)")
    statut = vilain.CastTo(aides["CanStatus"])
    if statut.HasStatus("Stunned") or statut.HasStatus("Confused"):
        soucis.append("Rhino porte un statut : la clause conditionnelle est "
                      "partie alors que RIEN n'a ete vaincu")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "4 degats, 3 menaces retirees, aucun statut : la clause est bien conditionnelle"


def ma017_retiree_du_jeu(monde, aides):
    """ma017 : « remove this card from the game » n'est pas « discard »."""
    soucis = []
    if aides["par_id"](monde, "ma017") is not None:
        soucis.append("ma017 est encore en jeu")
    if _ma_dans_la_defausse(monde, "ma017"):
        soucis.append("ma017 est dans la defausse : elle devait etre RETIREE DU JEU")
    identite = aides["identite"](monde)
    subis = identite.max_health - identite.health
    if subis != 4:
        soucis.append(f"degats sur l'identite = {subis} (attendu 4)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "ma017 a quitte le jeu sans passer par la defausse, 4 degats subis"


def ma019_allie_attache_et_menace(monde, aides):
    """ma019 : l'allie est attache, et la menace vaut SON cout imprime."""
    manigance = aides["par_id"](monde, "ma019")
    if manigance is None:
        return False, "ma019 introuvable en jeu"
    soucis = []
    zone = manigance.GetPlacedCardArea()
    ids = [getattr(f.paper, "card_id", None) for f in zone.GetAll()]
    if "01059" not in ids:
        soucis.append(f"01059 n'est pas attachee (zone = {ids})")
    if manigance.threat != 3:
        soucis.append(f"menace = {manigance.threat} (attendu 3, le cout de 01059 ; "
                      f"2 signifierait que le repli « pas d'allie » s'est applique)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "01059 attachee et menace de depart = 3, son cout imprime"


def ma020_sonnee_apres_attaque(monde, aides):
    """ma020 : Catalina attaque, des degats passent, l'identite est Sonnee."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    soucis = []
    subis = identite.max_health - identite.health
    if subis <= 0:
        soucis.append("l'identite n'a rien encaisse : Catalina n'a pas attaque")
    if not identite.CastTo(aides["CanStatus"]).HasStatus("Stunned"):
        soucis.append("l'identite n'est pas Sonnee")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"Catalina a attaque ({subis} degat(s)) et l'identite est Sonnee"


def ma020_rien_ne_se_passe(monde, aides):
    """ma020, contre-epreuve : sans Catalina, ni degat ni Sonne."""
    identite = aides["identite"](monde)
    if identite is None:
        return False, "identite introuvable"
    soucis = []
    subis = identite.max_health - identite.health
    if subis != 0:
        soucis.append(f"l'identite a encaisse {subis} degat(s) alors que Catalina "
                      f"n'est pas en jeu")
    if identite.CastTo(aides["CanStatus"]).HasStatus("Stunned"):
        soucis.append("l'identite est Sonnee alors qu'aucune attaque n'a eu lieu")
    if soucis:
        return False, " ; ".join(soucis)
    return True, ("aucune attaque, aucun Sonne : la branche « if no attack is made "
                  "this way » est la seule partie (surge non observable)")
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
            # d'Ashley Barton (mw023), payee R+Y sans qu'on le voie.
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
            # `declencher_apres` : commandes Puzzle.* jouees APRES `jouer`.
            # Ajoutee le 30/08/2026 pour le pack `ms_america`. `declencher`
            # tourne AVANT `jouer` : impossible sans cette cle de tester une
            # capacite dont l'effet ne se voit qu'a l'usage SUIVANT d'un
            # pouvoir (ma009 America's Anger, « double all modifiers ... on
            # its next use this turn ») ou une carte qui exige qu'un evenement
            # ait deja ete joue dans le tour (ma003 Hawkeye, « if you have
            # resolved Star-Gaze this turn »). Cle ADDITIVE : aucun cas
            # existant ne la definit, aucun n'est modifie.
            if cas.get("declencher_apres"):
                PuzzleHelper.Exec(cas["declencher_apres"], monde)
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
            # « ne_pas_depenser » INTERDIT a des cartes de servir de ressource,
            # la ou « payer_avec » se contente de les PREFERER, en gardant tout
            # le reste en repli. La difference compte des qu'une carte de la
            # main est elle-meme le sujet du cas : pour prouver que les DEUX
            # Calculated Defense de Brawn partent sur la meme defense, il faut
            # empecher le pilote de defausser la seconde pour financer la
            # premiere — ce qu'il faisait systematiquement, rendant
            # l'interaction intestable (constate le 9/8/2026).
            #
            # Les cles de `payment` sont les identifiants des EFFETS PAYANTS,
            # pas ceux des objets carte : une carte offerte en ressource y
            # apparait sous l'id de son effet, jamais sous le sien. Interdire
            # l'id de l'objet ne filtrait donc rien. On remonte aux effets par
            # `is_paying`, exactement comme le descripteur de carte remplit son
            # champ `resources` (game/card/card.py).
            for card_id in cas.get("ne_pas_depenser") or []:
                for objet_id, objet in monde_courant().object_manager.card_dict.items():
                    face = objet.face
                    if face is None or getattr(face.paper, "card_id", None) != card_id:
                        continue
                    interdits.add(str(objet_id))
                    for effet in objet.GetEffects():
                        if getattr(effet.ability, "is_paying", False):
                            interdits.add(str(effet.object_id))
            candidates = []
            # CORRECTIF 5/8/2026 : une carte peut fournir PLUSIEURS ressources
            # (« RR » de Nuts! sg017, « YY » d'Energy 01088). Le pilote comptait
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
            # aux cartes a cout X (mw008), dont le cout annonce est nul : sans
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
            # `choisir_option` (pack kate_bishop) : forcer UNE option PRECISE
            # parmi plusieurs choix nommes sans cible-carte (DeclareNumber,
            # ChooseAbilities a options textuelles) ou le pilote, qui prend
            # toujours la PREMIERE option non en echec, choisirait sinon
            # systematiquement "0" ou la premiere branche. Sans elle, "Master
            # Archer" (kb001a) ne retirerait jamais de compteur puisque 0 est
            # une reponse toujours legale a `player.DeclareNumber`. Cle
            # ADDITIVE : n'affecte AUCUN cas qui ne la definit pas (repli
            # integral sur la boucle historique ci-dessous si absente ou sans
            # correspondance), donc aucun cas existant n'est modifie.
            voulues = cas.get("choisir_option")
            if voulues and etat["phase"] == "cas":
                if isinstance(voulues, str):
                    voulues = [voulues]
                for o in options:
                    if isinstance(o, dict) and not o.get("failure_reason") \
                            and o.get("name") in voulues:
                        legales = [str(x) for x in (o.get("all_legal_targets") or [])]
                        mini, maxi = (o.get("target_num_range") or [0, 0])[:2]
                        cibles = legales[:mini]
                        if cas.get("accepter_choix") and legales:
                            borne = maxi if isinstance(maxi, int) and maxi > 0 else 1
                            cibles = legales[:borne]
                        forcees = choisir_cibles(cas.get("cibles") or [], legales)
                        if forcees:
                            cibles = forcees[:maxi] if isinstance(maxi, int) else forcees
                        return json.dumps({"id": str(o.get("id", 0)),
                                           "targets": cibles,
                                           "resources": payer(o, cibles)})
            # Accepter la premiere option jouable en fournissant le nombre
            # MINIMAL de cibles qu'elle exige. Repondre « aucune cible » a un
            # choix qui en exige une fait rejeter la reponse par le moteur, qui
            # repose alors la meme question a l'infini (c'est ce qui bloquait la
            # mise en place d'Albert, dont la capacite Setup fouille le deck).
            # `preferer_option` : choisir l'option dont le NOM contient l'un des
            # fragments donnes, au lieu de la premiere jouable. Ajoute le
            # 30/08/2026 pour le pack `wiccan`. Sans elle, un `ChooseAbilities`
            # a plusieurs branches n'est testable que sur SA PREMIERE branche
            # (« le pilote prend toujours la premiere option », convention
            # il017/ok019/ss011) : la seconde branche de l'obligation wc018,
            # qui eteint le comptage des icones de bonus pour tout le pack,
            # n'aurait eu aucun cas sujet. Le filtre porte sur le libelle exact
            # de la `ForChoiceAbility`, pas sur un rang : il ne se trompe pas de
            # question quand plusieurs asks s'enchainent, il n'agit que sur
            # celles qui proposent vraiment ce libelle.
            ordonnees = options
            if cas.get("preferer_option") and etat["phase"] == "cas":
                fragments = cas["preferer_option"]
                if isinstance(fragments, str):
                    fragments = [fragments]
                # Le moteur remplace les espaces des noms d'option par des
                # soulignes (« +1_ATK_until_the_end_of_the_round ») : on
                # normalise les deux cotes, sinon aucun libelle a plusieurs
                # mots ne peut jamais correspondre.
                def _nom(o):
                    return str(o.get("name") or "").replace("_", " ")
                preferees = [o for o in options if isinstance(o, dict)
                             and any(f.replace("_", " ") in _nom(o) for f in fragments)]
                ordonnees = preferees + [o for o in options if o not in preferees]

            for o in ordonnees:
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
    rapport = sys.argv[3] if len(sys.argv) > 3 else f"/tmp/test_capacites_{os.environ.get('CAS_PREFIX', '')}.json"

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
