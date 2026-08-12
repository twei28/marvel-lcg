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
