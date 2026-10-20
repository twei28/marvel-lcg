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
]
