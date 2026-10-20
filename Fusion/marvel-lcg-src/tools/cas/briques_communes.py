# Cas test_capacites des TROIS BRIQUES MOTEUR communes aux campagnes Punisher
# MC×DC 2026 et Galactic Storm (decision de l'utilisateur du 20/10/2026) :
# prefixe « [briques] ». Recette : docs/reference/RECETTES-MOTEUR.md §15.
#
#   [briques][attaque]   un ennemi attaque un autre ennemi ou un allie
#                        (`Enemy.AttackCharacter`, commande `Puzzle.EnemyAttacks`)
#   [briques][immunite]  « ne peut pas etre affecte par les cartes joueur »
#                        (`PlayerCardImmunity`, fabrique
#                        `AbilityFactory.CannotBeAffectedByPlayerCards`)
#   [briques][mechants]  plusieurs mechants en jeu, un seul « le mechant »
#                        (`Worlds.Villains`, `Villains.Rule`)
#
# Montage commun : scenario Rhino (01094, ATQ 2, PV 14 en solo), Spider-Man.
# Le deck rencontre ne contient que 01105 « I'm Tough » (0 icone de boost) pour
# que les attaques de Rhino ne recoivent AUCUN bonus de boost, sauf dans le cas
# qui mesure justement le « vous » d'un Boost (01121 Weapons Runner).
#
# Sbires utilises (rhino) : 01103 Shocker (PV 3, ATQ 2), 01110 Hydra Bomber
# (PV 2), 01101 Hydra Mercenary (PV 3, Guard). Allie : 01011 Spider-Woman (PV 2).

FORME_HEROS = "Puzzle.ChangeForm('01001b')"
RIEN_A_BOOSTER = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]

CAS = [
    # =================================================================== BRIQUE 1
    {
        "nom": "[briques][attaque] Rhino attaque un SBIRE (Shocker) : 2 degats sur Shocker, aucun sur le heros, aucune defense proposee",
        "pourquoi": ("Enemy.AttackCharacter vers un ennemi : la cible encaisse l'ATQ de base ; le heros, pret et en forme "
                     "heros, n'est pas sollicite pour defendre (seul le controleur d'une cible defend ; un ennemi n'a "
                     "pas de controleur joueur), donc il reste PRET"),
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('01103')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('01094', '01103')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01103", 2]], "degats_identite": 0, "pret": ["01001a"]},
    },
    {
        "nom": "[briques][attaque] Rhino attaque un sbire avec overkill (+2 ATQ) : Hydra Bomber abattu, l'exces (2) va au mechant (RR 1.8 p.31)",
        "pourquoi": ("ATQ 2 + 2 = 4 sur un sbire a 2 PV : 2 d'exces ; « If a minion is defeated by an attack with the "
                     "overkill keyword, deal any damage beyond its hit points to the villain » — ici Rhino lui-meme, "
                     "comme Kree Sentry dans Galactic Storm p.9"),
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('01110')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('01094', '01110', overkill=True, additional_attack=2)"],
        "questions_absentes": ["Simultaneous Overkill"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01110"], "degats": [["01094", 2]]},
    },
    {
        "nom": "[briques][attaque] overkill_to : l'exces sur un sbire abattu va a la carte designee (Shocker), pas au mechant (Punisher p185)",
        "pourquoi": ("« His overkill damage on minions is dealt to the TARGETED villain » : la cible de l'exces est "
                     "un parametre ; ici Shocker la recoit (2), Rhino n'en recoit aucun"),
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('01094', '01110', overkill=True, additional_attack=2, overkill_to='01103')"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01110"], "degats": [["01103", 2], ["01094", 0]]},
    },
    {
        "nom": "[briques][attaque] players_may_defend : le heros DEFEND l'attaque visant Shocker et devient la cible (Punisher p180)",
        "pourquoi": ("« Players may defend any attack, even ones targeting enemies » : le pilote accepte la defense "
                     "proposee ; DEF 3 contre ATQ 2 = 0 degat, Shocker intact, le heros est incline par sa defense"),
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('01103')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('01094', '01103', players_may_defend=True)"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01103", 0]], "degats_identite": 0, "exhausted": ["01001a"]},
    },
    {
        "nom": "[briques][attaque] Rhino attaque DIRECTEMENT un allie (Spider-Woman) avec overkill : allie abattu, l'exces (1) va a l'identite",
        "pourquoi": ("RR 1.8 p.10 « Attacks Against Allies » : les degats non defendus vont a l'allie ; overkill : "
                     "« any excess damage ... is dealt to the identity of the player who controlled the defeated ally ». "
                     "Alter ego : personne ne peut defendre a sa place (un alter ego ne defend pas)"),
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('01011', under_control=True)"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('01094', '01011', overkill=True, additional_attack=1)"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["01011"], "degats_identite": 1},
    },
    {
        "nom": "[briques][attaque] Boost « engaged with YOU » pendant une attaque contre un sbire : Weapons Runner s'engage avec le joueur DESIGNE (2e joueur), pas le joueur courant",
        "pourquoi": ("Galactic Storm p.9 : « Any boost abilities that refer to “you” apply to the player who revealed "
                     "the card that caused Kree Sentry to attack the minion ». Partie a DEUX : le « vous » est le "
                     "joueur 1 (indice), alors que le moteur, sans `boost_player`, retombe sur le joueur courant (0)"),
        "scenario": "rhino", "heros": "spider_man", "heros2": "spider_man",
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01121')",
                          "Puzzle.PutIntoPlay('01103')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('01094', '01103', joueur=1)"],
        "verifier": "fne_engage_joueur",
        "attendu": {"carte": "01121", "joueur": 1},
    },
    {
        "nom": "[briques][attaque] TEMOIN : meme Boost, « vous » = joueur 0 quand c'est lui que la carte designe",
        "pourquoi": "contre-cas du precedent : la mesure suit bien le parametre, pas la place du joueur",
        "scenario": "rhino", "heros": "spider_man", "heros2": "spider_man",
        "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01121')",
                          "Puzzle.PutIntoPlay('01103')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('01094', '01103', joueur=0)"],
        "verifier": "fne_engage_joueur",
        "attendu": {"carte": "01121", "joueur": 0},
    },

    # =================================================================== BRIQUE 2
    {
        "nom": "[briques][immunite] attaque de base du heros : Rhino protege n'est pas une cible, l'attaque va a Shocker",
        "pourquoi": ("Galactic Storm p.14 : « That includes attacking the villain with either heroes or allies » ; "
                     "Rhino est ecarte des cibles legales, le pilote frappe la seule cible restante (Shocker, 2 degats)"),
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01103')", "Puzzle.ProtectFromPlayerCards('01094')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 0], ["01103", 2]]},
    },
    {
        "nom": "[briques][immunite] TEMOIN : sans protection, le meme heros peut viser Rhino (2 degats)",
        "pourquoi": "contre-cas : prouve que Rhino est une cible legale ordinaire dans ce montage",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01103')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["01094"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]]},
    },
    {
        "nom": "[briques][immunite] carte a cible UNIQUE (Swinging Web Kick, 8 degats a un ennemi) : injouable quand seul Rhino protege est en jeu",
        "pourquoi": ("« If a card or ability has only one target and that target is the villain, that card cannot be "
                     "played » : la carte reste en main, Rhino intact"),
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.ProtectFromPlayerCards('01094')"],
        "main_exclusive": ["01005", "01090", "01088"],
        "declencher": [],
        "jouer": ["01005"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["01005"], "degats": [["01094", 0]]},
    },
    {
        "nom": "[briques][immunite] TEMOIN : Swinging Web Kick sans protection : 8 degats sur Rhino, carte jouee",
        "pourquoi": "contre-cas : la carte est jouable dans ce montage (paiement, forme heros)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS],
        "main_exclusive": ["01005", "01090", "01088"],
        "declencher": [],
        "jouer": ["01005"],
        "verifier": "etat_attendu",
        "attendu": {"absent_main": ["01005"], "degats": [["01094", 8]]},
    },
    {
        "nom": "[briques][immunite] amelioration a attacher (Webbed Up) : injouable sur Rhino protege, seule cible",
        "pourquoi": "« attaching upgrades or other player cards to the villain » : Webbed Up reste en main",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.ProtectFromPlayerCards('01094')"],
        "main_exclusive": ["01009", "01090", "01088"],
        "declencher": [],
        "jouer": ["01009"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["01009"], "taille_attaches": [["01094", 0]]},
    },
    {
        "nom": "[briques][immunite] exces d'un overkill du HEROS (Ares) sur un sbire abattu : rien sur Rhino protege",
        "pourquoi": ("« dealing damage to the villain through overkill when a minion is defeated with excess "
                     "damage » : meme montage que « Overkill [regle] — sbire vaincu » (4 d'exces sur Rhino), Rhino "
                     "protege n'en recoit aucun"),
        "scenario": "rhino", "heros": "ares",
        "mise_en_place": ["Puzzle.ChangeToFace('ar001b', 'ar001a')",
                          "Puzzle.PutIntoPlay('39043')",
                          "Puzzle.PutIntoPlay('ar008', under_control=True)",
                          "Puzzle.ProtectFromPlayerCards('01094')"],
        "main_exclusive": ["01090"],
        "declencher": ["Puzzle.Attack('ar001a')"],
        "cibles": ["39043"],
        "verifier": "etat_attendu",
        "attendu": {"hors_jeu": ["39043"], "degats": [["01094", 0]]},
    },
    {
        "nom": "[briques][immunite] effets directs d'une carte joueur (degats de zone, etat, Robuste, compteur, bonus) : aucun ne touche Rhino protege",
        "pourquoi": ("le verificateur applique a Rhino, au nom du heros (effet de carte joueur, sans ciblage), "
                     "2 degats, Sonne, la defausse de son Robuste, 1 compteur, +1 ATQ ; puis 2 degats au nom de "
                     "Shocker (carte rencontre), qui DOIVENT passer"),
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01103')", "Puzzle.Tough('01094')",
                          "Puzzle.ProtectFromPlayerCards('01094')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "briques_effets_directs",
        "attendu": {"protege": True},
    },
    {
        "nom": "[briques][immunite] TEMOIN : memes effets directs sans protection : tous touchent Rhino",
        "pourquoi": "contre-cas : chacune des cinq mesures bouge quand Rhino n'est pas protege",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.PutIntoPlay('01103')", "Puzzle.Tough('01094')"],
        "main_exclusive": ["01088"],
        "declencher": [],
        "verifier": "briques_effets_directs",
        "attendu": {"protege": False},
    },
    {
        "nom": "[briques][immunite] porteur d'un attachement (AttachedCharacter, In the Crosshairs) : Shocker protege, Rhino reste ciblable",
        "pourquoi": ("Punisher p183 « Attached character ... cannot be affected by player cards » : Charge (01099, "
                     "attachement rencontre) attachee a Shocker sert de source ; l'attaque du heros ne peut viser que "
                     "Rhino (2 degats), Shocker intact"),
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('01103')",
                          "Puzzle.ProtectFromPlayerCards('01099', attached_to='01103')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        # Le pilote VEUT Shocker : il ne lui est pas offert, l'attaque retombe sur Rhino.
        "cibles": ["01103"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01103", 0], ["01094", 2]]},
    },
    {
        "nom": "[briques][immunite] l'attachement source QUITTE le jeu : la protection tombe, Shocker redevient ciblable",
        "pourquoi": "la protection ne vaut que tant que sa source est en jeu ; Charge defaussee, le heros peut viser Shocker",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.PutIntoPlay('01103')",
                          "Puzzle.ProtectFromPlayerCards('01099', attached_to='01103')",
                          "Puzzle.Discard('01099')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01001a')"],
        "cibles": ["01103"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01103", 2]]},
    },
    {
        "nom": "[briques][immunite] condition de trait (HIDDEN) : protection active tant que le trait est present (BRUTE sur Rhino)",
        "pourquoi": "while_fn relu a chaque question : Rhino a BRUTE, il est protege (Swinging Web Kick injouable)",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.ProtectFromPlayerCards('01094', trait='BRUTE')"],
        "main_exclusive": ["01005", "01090", "01088"],
        "declencher": [],
        "jouer": ["01005"],
        "verifier": "etat_attendu",
        "attendu": {"en_main": ["01005"], "degats": [["01094", 0]]},
    },
    {
        "nom": "[briques][immunite] condition de trait absente (ELITE, que Rhino n'a pas) : pas de protection, 8 degats",
        "pourquoi": "le pendant : apres un retournement sur la face DISCOVERED (sans HIDDEN), la carte joueur passe",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, "Puzzle.ProtectFromPlayerCards('01094', trait='ELITE')"],
        "main_exclusive": ["01005", "01090", "01088"],
        "declencher": [],
        "jouer": ["01005"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 8]]},
    },
    {
        "nom": "[briques][immunite] un ENNEMI peut toujours attaquer le mechant protege (Rachel Cole-Alves, p195) : Shocker inflige 2 a Rhino",
        "pourquoi": "l'immunite ne vise que les cartes JOUEUR : une attaque d'ennemi (brique 1) passe",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, "Puzzle.PutIntoPlay('01103')", "Puzzle.ProtectFromPlayerCards('01094')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.EnemyAttacks('01103', '01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats": [["01094", 2]]},
    },
    {
        "nom": "[briques][immunite] le heros DEFEND encore l'attaque du mechant protege (la defense vise l'attaquant sans l'affecter)",
        "pourquoi": "Rhino protege attaque, le pilote defend avec le heros (DEF 3 contre ATQ 2) : 0 degat, heros incline",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [*RIEN_A_BOOSTER, FORME_HEROS, "Puzzle.ProtectFromPlayerCards('01094')"],
        "main_exclusive": ["01088"],
        "declencher": ["Puzzle.Attack('01094')"],
        "verifier": "etat_attendu",
        "attendu": {"degats_identite": 0, "exhausted": ["01001a"]},
    },
]

VERIFICATIONS = r'''
def briques_effets_directs(monde, aides):
    """Applique a Rhino, au nom du HEROS (GameRule(identite) : `this` est une
    carte joueur, aucun ciblage), cinq effets directs ; puis 2 degats au nom de
    Shocker (carte rencontre). `attendu.protege` : True = aucun des cinq ne doit
    toucher Rhino, False = tous le touchent. Les degats rencontre passent dans
    les deux cas."""
    from game.effect.rule import GameRule
    from game.operate.faces import Faces
    attendu = aides["cas"].get("attendu") or {}
    protege = attendu["protege"]
    rhino = aides["par_id"](monde, "01094")
    shocker = aides["par_id"](monde, "01103")
    heros = aides["identite"](monde)
    if rhino is None or shocker is None or heros is None:
        return False, "montage incomplet (Rhino, Shocker ou heros introuvable)"
    rhino = rhino.CastTo(aides["CanStatus"])
    effet_joueur = GameRule(heros)
    if not rhino.IsTough():
        return False, "montage : Rhino devait porter un Robuste"
    blesse = lambda f: f.max_health - f.health
    pv0, atq0, cpt0 = blesse(rhino), rhino.attack, rhino.GetCounters("all-purpose")
    # Robuste d'abord : sinon il absorberait les degats qui suivent.
    rhino.DiscardTough(effet_joueur, rule="All")
    rhino.TakeDamage(heros, 2, effet_joueur)
    Faces.GiveStatus([rhino], "Stunned", effet_joueur)
    Faces.PlaceCountersOn([rhino], 1, "all-purpose", effet_joueur)
    rhino.GainUntilRoundEnd(effet_joueur, attack=1)
    mesures = {
        "degats": blesse(rhino) - pv0,
        "sonne": int(rhino.IsStunned()),
        "robuste_defausse": int(not rhino.IsTough()),
        "compteur": rhino.GetCounters("all-purpose") - cpt0,
        "bonus_atq": rhino.attack - atq0,
    }
    voulu = {"degats": 2, "sonne": 1, "robuste_defausse": 1, "compteur": 1, "bonus_atq": 1}
    if protege:
        voulu = {k: 0 for k in voulu}
    ecarts = [f"{k}={mesures[k]} (attendu {voulu[k]})" for k in voulu if mesures[k] != voulu[k]]
    # Cote RENCONTRE, tout passe : la defausse du Robuste (encore la si Rhino
    # est protege) puis 2 degats.
    rhino.DiscardTough(GameRule(shocker), rule="All")
    if rhino.IsTough():
        ecarts.append("une carte RENCONTRE n'a pas pu defausser le Robuste de Rhino")
    pv1 = blesse(rhino)
    rhino.TakeDamage(shocker, 2, GameRule(shocker))
    if blesse(rhino) - pv1 != 2:
        ecarts.append(f"degats de la carte RENCONTRE = {blesse(rhino) - pv1} (attendu 2, l'immunite ne vise que les cartes joueur)")
    if ecarts:
        return False, " ; ".join(ecarts)
    return True, f"mesures {mesures}, degats rencontre 2"
'''
