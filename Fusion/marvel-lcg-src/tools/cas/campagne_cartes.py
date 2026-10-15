# Cas test_capacites du bloc CAMPAGNE_CARTES (sk263-sk289b, cartes de campagne de Skrull Menace).
# Format identique a tools/test_capacites.py ; noms prefixes `[campagne_cartes]` (filtre : `[campagne_cartes]`).
#
# Conventions de ce fichier :
#  - le heros de test (Spider-Man, 01001) demarre en ALTER EGO ; `Puzzle.ChangeForm('01001b')` le met en forme
#    HEROS ;
#  - un sbire pose par `Puzzle.PutIntoPlay` s'ENGAGE toujours avec le joueur (RECETTES §1) ;
#  - 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR : cartes de main sans effet qui servent a
#    fixer la main (`main_exclusive`) ou a payer une couleur (`payer_avec`) ;
#  - sbires de test : 01101 Hydra Mercenary (3 PV, non Skrull), 01103 Shocker (3 PV, ATQ 2, MNG 1), 01102 Sandman
#    (ELITE) ; Skrull : sk184 Dard'van Fanatic (4 PV, MNG 2, non Elite), sk155 General Kalamari (ELITE SKRULL) ;
#  - SUPERPOWER de Spider-Man (core) : 01004, 01005, 01013, 01021, 01022 (Ground Stomp : « 1 degat a chaque
#    ennemi », sans cible), 01031.
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
VIDE = "Puzzle.EmptyEncounterDeck()"
RHINO = "01094"
INERTE = ["01088"]     # une main inerte (YY)


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[campagne_cartes] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ===================================================================== sk263 Crusader
    _c("sk263 Crusader : 1 degat au mechant et au sbire engage ; un sbire acheve = 1 carte piochee",
       "Response apres l'entree en jeu ; `SetTarget('VillainAndEngagedSamePlayerMinion')` ; Hydra Mercenary (3 PV) "
       "a 2 degats est achevee, Rhino reste debout : une seule carte piochee",
       [VIDE, "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage('01101', 2)"],
       ["Puzzle.PutIntoPlay('sk263', under_control=True)"],
       {"degats": [[RHINO, 1]], "hors_jeu": ["01101"], "taille_main": 2, "en_jeu": ["sk263"]},
       main_exclusive=INERTE),
    _c("sk263 Crusader : DEUX sbires achieves = 2 cartes piochees (un compte par ennemi vaincu)",
       "« draw 1 card for each enemy defeated this way » : deux sbires a 1 PV restant tombent, 2 cartes",
       [VIDE, "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage('01101', 2)", "Puzzle.PutIntoPlay('01103')",
        "Puzzle.Damage('01103', 2)"],
       ["Puzzle.PutIntoPlay('sk263', under_control=True)"],
       {"degats": [[RHINO, 1]], "hors_jeu": ["01101", "01103"], "taille_main": 3},
       main_exclusive=INERTE),
    _c("sk263 Crusader, TEMOIN : aucun ennemi achieve = aucune carte piochee",
       "ligne de base : Hydra Mercenary (3 PV) intacte prend 1 degat et survit ; la main reste a 1 carte",
       [VIDE, "Puzzle.PutIntoPlay('01101')"],
       ["Puzzle.PutIntoPlay('sk263', under_control=True)"],
       {"degats": [[RHINO, 1], ["01101", 1]], "taille_main": 1},
       main_exclusive=INERTE),
    # ===================================================================== sk264 Jazinda
    _c("sk264 Jazinda : inclinee, le heros gagne +1 CTR (forme heros)",
       "`GiveKeywordToInPlayWhenApplyThis(Hero, control_by='You', thwart=1)` tant que Jazinda est inclinee",
       [HEROS, "Puzzle.PutIntoPlay('sk264', under_control=True)"], ["Puzzle.Exhaust('sk264')"],
       {"attributs": {"thwart": 1}, "exhausted": ["sk264"]}, main_exclusive=INERTE),
    _c("sk264 Jazinda, TEMOIN : redressee, aucun bonus de CTR",
       "ligne de base : le bonus tombe quand Jazinda se redresse",
       [HEROS, "Puzzle.PutIntoPlay('sk264', under_control=True)", "Puzzle.Exhaust('sk264')"],
       ["Puzzle.Ready('sk264')"],
       {"attributs": {"thwart": 0}, "pret": ["sk264"]}, main_exclusive=INERTE),
    _c("sk264 Jazinda : elle ne compte PAS contre la limite d'allies (3 allies + Jazinda, tous restent en jeu)",
       "`ThisNotCountAllyLimit` : la limite est de 3 ; avec Jazinda un 4e allie ne declenche aucune defausse",
       [HEROS, "Puzzle.PutIntoPlay('sk038', under_control=True)", "Puzzle.PutIntoPlay('sk049', under_control=True)",
        "Puzzle.PutIntoPlay('sk056', under_control=True)"],
       ["Puzzle.PutIntoPlay('sk264', under_control=True)"],
       {"en_jeu": ["sk038", "sk049", "sk056", "sk264"], "allies_comptes": 3, "allies_en_jeu": 4},
       main_exclusive=INERTE, verifier="cc_allies"),
    _c("sk264 Jazinda, TEMOIN : 4 allies SANS Jazinda -> la limite de 3 s'applique (un seul est compte en trop)",
       "contre-cas : le 4e allie ordinaire depasse la limite, `curr_ally` = 4 > 3 (le moteur demande alors une defausse)",
       [HEROS, "Puzzle.PutIntoPlay('sk038', under_control=True)", "Puzzle.PutIntoPlay('sk049', under_control=True)",
        "Puzzle.PutIntoPlay('sk056', under_control=True)"],
       ["Puzzle.PutIntoPlay('sk057', under_control=True)"],
       {"allies_comptes_max": 3, "allies_en_jeu": 3},
       main_exclusive=INERTE, verifier="cc_allies"),
    _c("sk264 Jazinda : le bonus de CTR ne profite PAS au heros d'un AUTRE joueur",
       "« YOUR hero » : controle_par 'You' ; deux joueurs, Jazinda sous le controle du joueur 1 (Spider-Man)",
       [HEROS, "Puzzle.ChangeToFace('sk037b', 'sk037a')", "Puzzle.PutIntoPlay('sk264', under_control=True)",
        "Puzzle.Exhaust('sk264')"],
       [], {"thwart_joueur2": 0, "thwart_joueur1": 1}, main_exclusive=INERTE, heros2="lyja",
       verifier="cc_jazinda_deux_joueurs"),
    # ===================================================================== sk265 Paibok (allie)
    _c("sk265 Paibok : entre en jeu avec une carte Robuste (Toughness lu dans le desc)",
       "fiche toughness.md : aucun script ; le statut est pose a l'entree en jeu",
       [], ["Puzzle.PutIntoPlay('sk265', under_control=True)"],
       {"statuts": [["sk265", "Tough"]]}, main_exclusive=INERTE),
    _c("sk265 Paibok : apres la defausse d'une traitrise, il prend 1 degat et l'attache face cachee ; +1 THW / +1 ATQ",
       "Response `AfterCardDiscard(FinderTraitrise)` + cout `TakeDamage(1)` + `PlaceCardHere(face cachee)` + `ThisGainKeyword` ; "
       "le Robuste d'entree est retire d'abord pour que les degats se voient",
       ["Puzzle.PutIntoPlay('sk265', under_control=True)", "Puzzle.Tough('sk265')"],
       ["Puzzle.Discard('01186')"],
       {"pose_sous": [["sk265", "01186"]], "degats": [["sk265", 1]],
        "attributs_carte": [["sk265", "thwart", 1], ["sk265", "attack", 1]]}, main_exclusive=INERTE),
    _c("sk265 Paibok, TEMOIN : une carte qui n'est PAS une traitrise (sbire) defaussee : rien n'est attache",
       "« a treachery card » : un sbire n'est pas une traitrise ; aucun degat",
       ["Puzzle.PutIntoPlay('sk265', under_control=True)", "Puzzle.Tough('sk265')"],
       ["Puzzle.Discard('01101')"],
       {"taille_pose_sous": [["sk265", 0]], "degats": [["sk265", 0]],
        "attributs_carte": [["sk265", "thwart", 0], ["sk265", "attack", 0]]}, main_exclusive=INERTE),
    _c("sk265 Paibok : un evenement de Lyja portant le trait TREACHERY compte aussi (decision du 15/10/2026)",
       "`EstTraitrise` : type Treachery OU trait TREACHERY ; sk039 Faking Death",
       ["Puzzle.PutIntoPlay('sk265', under_control=True)", "Puzzle.Tough('sk265')"],
       ["Puzzle.Discard('sk039')"],
       {"pose_sous": [["sk265", "sk039"]], "degats": [["sk265", 1]]}, main_exclusive=INERTE),
    _c("sk265 Paibok : « to a maximum of 2 » : la troisieme traitrise defaussee n'est PAS attachee",
       "la Reponse n'est offerte que tant que la pile compte moins de 2 cartes ; 2 attachees, 2 degats",
       ["Puzzle.PutIntoPlay('sk265', under_control=True)", "Puzzle.Tough('sk265')"],
       ["Puzzle.Discard('01186')", "Puzzle.Discard('01111')", "Puzzle.Discard('01112')"],
       {"taille_pose_sous": [["sk265", 2]], "degats": [["sk265", 2]],
        "attributs_carte": [["sk265", "thwart", 2], ["sk265", "attack", 2]]}, main_exclusive=INERTE),
    _c("sk265 Paibok : tant qu'il est Robuste, le cout « take 1 damage » ne peut pas etre paye (rien n'est attache)",
       "regle : un cout de degats n'est paye que si TOUS les degats sont subis ; le Robuste d'entree les prevoit",
       ["Puzzle.PutIntoPlay('sk265', under_control=True)"],
       ["Puzzle.Discard('01186')"],
       {"taille_pose_sous": [["sk265", 0]], "degats": [["sk265", 0]]},
       main_exclusive=INERTE),
    # ===================================================================== sk266 Skymax
    _c("sk266 Skymax : les allies de la defausse retournent dans le deck, pas les autres cartes",
       "Response apres l'entree en jeu : `ShuffleAllTo(allies de la defausse, deck)`",
       ["Puzzle.CreatePlayerDeck('01088')", "Puzzle.CreatePlayerDiscardPile('sk038', 'sk049', '01089')"],
       ["Puzzle.PutIntoPlay('sk266', under_control=True)"],
       {"dans_deck_joueur": ["sk038", "sk049"], "defausse": ["01089"], "en_jeu": ["sk266"]}, main_exclusive=["01090"]),
    _c("sk266 Skymax, TEMOIN : un allie EN JEU n'est pas touche",
       "« from your discard pile » : l'allie en jeu reste en jeu",
       ["Puzzle.CreatePlayerDeck('01088')", "Puzzle.PutIntoPlay('sk038', under_control=True)"],
       ["Puzzle.PutIntoPlay('sk266', under_control=True)"],
       {"en_jeu": ["sk038", "sk266"]}, main_exclusive=["01090"]),
    # ===================================================================== sk267 Super-Skrull (allie)
    _c("sk267 Super-Skrull : un SUPERPOWER defausse est attache face cachee ; +1 THW / +1 ATQ",
       "Response `AfterCardDiscard(trait SUPERPOWER)` + `PlaceCardHere` + `ThisGainKeyword` (noms distincts) ; "
       "01022 Ground Stomp porte SUPERPOWER",
       [], ["Puzzle.PutIntoPlay('sk267', under_control=True)", "Puzzle.Discard('01022')"],
       {"pose_sous": [["sk267", "01022"]], "attributs_carte": [["sk267", "thwart", 1], ["sk267", "attack", 1]]},
       main_exclusive=INERTE),
    _c("sk267 Super-Skrull : DEUX pouvoirs DIFFERENTS = +2 / +2",
       "« for each DIFFERENT SUPERPOWER card » : 01022 et 01031",
       [], ["Puzzle.PutIntoPlay('sk267', under_control=True)", "Puzzle.Discard('01022')", "Puzzle.Discard('01031')"],
       {"taille_pose_sous": [["sk267", 2]], "attributs_carte": [["sk267", "thwart", 2], ["sk267", "attack", 2]]},
       main_exclusive=INERTE),
    _c("sk267 Super-Skrull : deux COPIES du meme pouvoir = +1 / +1 seulement (noms distincts)",
       "deux exemplaires de 01022 sont attaches (2 cartes) mais comptent UNE fois",
       [],
       ["Puzzle.PutIntoPlay('sk267', under_control=True)", "Puzzle.Discard('01022')", "Puzzle.Discard(Puzzle.CreateCard('01022'))"],
       {"taille_pose_sous": [["sk267", 2]], "attributs_carte": [["sk267", "thwart", 1], ["sk267", "attack", 1]]},
       main_exclusive=INERTE),
    _c("sk267 Super-Skrull : « to a maximum of 4 » : le cinquieme SUPERPOWER n'est PAS attache",
       "cinq pouvoirs distincts defausses : 01004, 01005, 01013, 01021, 01022 ; quatre attaches",
       [],
       ["Puzzle.PutIntoPlay('sk267', under_control=True)", "Puzzle.Discard('01004')", "Puzzle.Discard('01005')", "Puzzle.Discard('01013')", "Puzzle.Discard('01021')",
        "Puzzle.Discard('01022')"],
       {"taille_pose_sous": [["sk267", 4]], "attributs_carte": [["sk267", "thwart", 4], ["sk267", "attack", 4]]},
       main_exclusive=INERTE),
    _c("sk267 Super-Skrull, TEMOIN : une carte sans le trait SUPERPOWER defaussee : rien n'est attache",
       "01085 Emergency (THWART, pas SUPERPOWER)",
       [], ["Puzzle.PutIntoPlay('sk267', under_control=True)", "Puzzle.Discard('01085')"],
       {"taille_pose_sous": [["sk267", 0]], "attributs_carte": [["sk267", "thwart", 0], ["sk267", "attack", 0]]},
       main_exclusive=INERTE),
    # ===================================================================== sk268 Chilly McHotpants
    _c("sk268 Chilly McHotpants : entre en jeu comme un SBIRE engage avec le joueur (MNG 2, ATQ 2, 5 PV)",
       "`TreatAsMinion` : la face allie est remplacee par le gabarit sbire ; nom repris de la carte",
       [VIDE], ["Puzzle.PutIntoPlay('sk268', under_control=True)"],
       {"nom": "Chilly McHotpants", "scheme": 2, "attack": 2, "pv": 5, "engage": True},
       main_exclusive=INERTE, verifier="cc_war_skrull"),
    _c("sk268 Chilly McHotpants : ne compte PAS contre la limite d'allies (3 allies en jeu, tous restent)",
       "`ThisNotCountAllyLimit` : la carte entre sous sa face d'allie puis devient un sbire ; aucun allie n'est defausse",
       [HEROS, VIDE, "Puzzle.PutIntoPlay('sk038', under_control=True)", "Puzzle.PutIntoPlay('sk049', under_control=True)",
        "Puzzle.PutIntoPlay('sk056', under_control=True)"],
       ["Puzzle.PutIntoPlay('sk268', under_control=True)"],
       {"en_jeu": ["sk038", "sk049", "sk056"], "allies_comptes": 3, "allies_en_jeu": 3},
       main_exclusive=INERTE, verifier="cc_allies"),
    _c("sk268 Chilly McHotpants : apres avoir attaque, 1 carte piochee (degats subis, pas de 2e carte)",
       "Response `AfterUnitAttackYou` : le joueur en alter ego n'a pas de DEF, il encaisse 2 : une seule carte",
       [VIDE, "Puzzle.PutIntoPlay('sk268', under_control=True)"],
       ["Puzzle.Attack('skrull_war_minion')"],
       {"taille_main": 2, "degats_identite": 2}, main_exclusive=INERTE),
    _c("sk268 Chilly McHotpants : si le joueur ne subit AUCUN degat, 2 cartes piochees",
       "la carte Robuste de l'identite absorbe l'attaque : `damaged_targets` ne contient pas l'identite",
       [VIDE, "Puzzle.PutIntoPlay('sk268', under_control=True)", "Puzzle.Tough('01001b')"],
       ["Puzzle.Attack('skrull_war_minion')"],
       {"taille_main": 3, "degats_identite": 0}, main_exclusive=INERTE),
    _c("sk268 Chilly McHotpants vaincu : la carte revient dans la defausse du joueur, sous sa forme d'allie",
       "`TreatAsMinion` : quand le sbire quitte le jeu l'allie revient (`SwapCardFace`) dans la defausse du proprietaire",
       [VIDE, "Puzzle.PutIntoPlay('sk268', under_control=True)"],
       ["Puzzle.Damage('skrull_war_minion', 10)"],
       {"defausse": ["sk268"]}, main_exclusive=INERTE),
    # ===================================================================== sk269 Xavin
    _c("sk269 Xavin : defausse du deck jusqu'a un evenement a « Hero Action » et la resout (01022 : 1 degat a chaque ennemi)",
       "Interruption a l'entree en jeu ; `DiscardDeckUntil(Event, with_texts=['Hero Action'])` ; la ressource 01088 "
       "est defaussee d'abord, l'evenement ensuite ; `ResolveAbility` ; Rhino prend 1 degat",
       ["Puzzle.CreatePlayerDeck('01022', '01088')"],
       ["Puzzle.PutIntoPlay('sk269', under_control=True)"],
       {"defausse": ["01088", "01022"], "degats": [[RHINO, 1]], "en_jeu": ["sk269"]},
       main_exclusive=["01090"], accepter_choix=True),
    _c("sk269 Xavin, TEMOIN : un evenement SANS « Hero Action » (01086 First Aid, Action) est defausse mais pas pris pour cible",
       "le filtre `with_texts` saute 01086 et continue : 01022 est resolu (1 degat a Rhino), 01086 reste en defausse",
       ["Puzzle.CreatePlayerDeck('01022', '01086')"],
       ["Puzzle.PutIntoPlay('sk269', under_control=True)"],
       {"defausse": ["01086", "01022"], "degats": [[RHINO, 1]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("sk269 Xavin : deck epuise sans evenement a « Hero Action » : rien n'est resolu, rien ne reste en resolution",
       "`DiscardDeckUntil` rend None : aucun ennemi ne subit de degats",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01086')"],
       ["Puzzle.PutIntoPlay('sk269', under_control=True)"],
       {"degats": [[RHINO, 0]], "en_jeu": ["sk269"], "aucune_en_resolution": True}, main_exclusive=["01090"],
       accepter_choix=True),
    # ===================================================================== sk270 Buddy Training Program
    _c("sk270 Buddy Training Program : cout X = stade du mechant : stade 1 = 1 ressource",
       "`IncreaseResourceCostToPlay('This', stade)` sur un desc Cost 0 ; Rhino I (stade 1)",
       [], [], {"carte": "sk270", "cout": 1}, main=["sk270"], verifier="cc_cout"),
    _c("sk270 Buddy Training Program : au stade 2 (Rhino II) le cout est 2",
       "`printed_stage` du mechant relu a chaque calcul de cout",
       ["Puzzle.AdvanceVillain()"], [], {"carte": "sk270", "cout": 2}, main=["sk270"], verifier="cc_cout"),
    _c("sk270 Buddy Training Program : au stade 2, une carte a 2 icones (01088 YY) paie et la carte se joue",
       "temoin du precedent : le cout vaut bien 2",
       ["Puzzle.AdvanceVillain()"], [], {"en_jeu": ["sk270"], "menace": [["sk270", 2]]}, main_exclusive=["01088"],
       jouer=["sk270"]),
    _c("sk270 Buddy Training Program : vaincue, donne une carte Robuste au heros (jusqu'a X = 1 personnage amical)",
       "When Defeated : `GiveStatus(Tough)` sur la cible choisie parmi les personnages amicaux (Friend, range 0..X) ; "
       "Victory 0 : la carte part en pile de victoire",
       [HEROS, "Puzzle.PutIntoPlay('sk270', under_control=True)", "Puzzle.SetThreat('sk270', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"statuts": [["01001a", "Tough"]], "hors_jeu": ["sk270"]},
       main_exclusive=INERTE, cibles=["01001a"], accepter_choix=True),
    _c("sk270 Buddy Training Program : jusqu'a X = 2 personnages au stade 2 (heros ET allie recoivent chacun une carte Robuste)",
       "range (0, X) relu a la defaite : stade 2 -> deux cibles ; l'allie sk038 et le heros",
       ["Puzzle.AdvanceVillain()", HEROS, "Puzzle.PutIntoPlay('sk038', under_control=True)",
        "Puzzle.PutIntoPlay('sk270', under_control=True)", "Puzzle.SetThreat('sk270', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"statuts": [["01001a", "Tough"], ["sk038", "Tough"]], "hors_jeu": ["sk270"]},
       main_exclusive=INERTE, cibles=["sk270", "01001a", "sk038"], accepter_choix=True),
    # ===================================================================== sk271 Cloning Faux Pas
    _c("sk271 Cloning Faux Pas : porte 1 icone ACCELERATION en jeu (desc, aucun script)",
       "decision utilisateur du 15/10/2026 : l'icone du coeur de la boite de texte est Acceleration",
       ["Puzzle.PutIntoPlay('sk271', under_control=True)"], [],
       {"icones": [["Acceleration", 1]], "menace": [["sk271", 3]]}, main_exclusive=INERTE),
    _c("sk271 Cloning Faux Pas : vaincue, 3 degats a CHAQUE sbire SKRULL engage ; un sbire non Skrull est epargne",
       "When Defeated : `DeclareNumber(0, 3)` (choisi par `choisir_option`) puis `DealDamage` a chaque sbire SKRULL engage avec le vainqueur",
       [HEROS, VIDE, "Puzzle.PutIntoPlay('sk184')", "Puzzle.PutIntoPlay('sk155')", "Puzzle.PutIntoPlay('01101')",
        "Puzzle.PutIntoPlay('sk271', under_control=True)", "Puzzle.SetThreat('sk271', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"degats": [["sk184", 3], ["sk155", 3], ["01101", 0]], "hors_jeu": ["sk271"]},
       main_exclusive=INERTE, cibles=["sk271"], accepter_choix=True, choisir_option=["3"]),
    _c("sk271 Cloning Faux Pas, TEMOIN : montant 0 declare : aucun degat",
       "« up to 3 » : le joueur peut declarer 0 ; le pilote prend la premiere option (0)",
       [HEROS, VIDE, "Puzzle.PutIntoPlay('sk184')", "Puzzle.PutIntoPlay('sk271', under_control=True)",
        "Puzzle.SetThreat('sk271', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"degats": [["sk184", 0]], "hors_jeu": ["sk271"]}, main_exclusive=INERTE, cibles=["sk271"],
       accepter_choix=True),
    # ===================================================================== sk272 Fickle Alliance
    _c("sk272 Fickle Alliance : vaincue, un sbire non Elite du deck rencontre devient un allie (MNG imprime -> CTR, traits gardes)",
       "When Defeated : `Search.EncounterCard(non_trait ELITE)` + `Faces.TreatAsAlly(gabarit skrull_fickle_ally)` ; 01103 Shocker (MNG 1, ATQ 2, CRIMINAL)",
       [HEROS, VIDE, "Puzzle.CreateEncounterDeck('01102', '01103')", "Puzzle.PutIntoPlay('sk272', under_control=True)",
        "Puzzle.SetThreat('sk272', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"nom": "Shocker", "thwart": 1, "attack": 2, "trait": "CRIMINAL", "csq_atk": 1, "csq_thw": 1, "hors_jeu": ["sk272"]},
       main_exclusive=INERTE, cibles=["sk272"], accepter_choix=True, verifier="cc_fickle"),
    _c("sk272 Fickle Alliance : un sbire ELITE du deck rencontre n'est PAS cherchable (seul Sandman reste : rien n'est mis en jeu)",
       "« non-ELITE minion » : 01102 Sandman est ELITE ; aucun allie n'apparait",
       [HEROS, VIDE, "Puzzle.CreateEncounterDeck('01102')", "Puzzle.PutIntoPlay('sk272', under_control=True)",
        "Puzzle.SetThreat('sk272', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"aucun_allie_fickle": True, "hors_jeu": ["sk272"]},
       main_exclusive=INERTE, cibles=["sk272"], accepter_choix=True, verifier="cc_fickle"),
    _c("sk272 Fickle Alliance : l'allie prend 1 degat consequent apres avoir attaque",
       "gabarit ATK 0* : une etoile = 1 degat consequent ; l'allie (Shocker, 3 PV) attaque Rhino : 2 degats a Rhino, 1 a l'allie",
       [HEROS, VIDE, "Puzzle.CreateEncounterDeck('01102', '01103')", "Puzzle.PutIntoPlay('sk272', under_control=True)",
        "Puzzle.SetThreat('sk272', 1)", "Puzzle.Thwart('01001a')"],
       ["Puzzle.Attack('skrull_fickle_ally')"],
       {"degats": [["skrull_fickle_ally", 1], [RHINO, 2]]}, main_exclusive=INERTE, cibles=["sk272", RHINO],
       accepter_choix=True),
    _c("sk272 Fickle Alliance : l'allie issu du sbire, vaincu, retourne en DEFAUSSE DE RENCONTRE (sa carte est une carte rencontre)",
       "`Card.CheckIfCanDiscard` rend la face de sbire ; le proprietaire est le camp rencontre, pas le joueur",
       [HEROS, VIDE, "Puzzle.CreateEncounterDeck('01102', '01103')", "Puzzle.PutIntoPlay('sk272', under_control=True)",
        "Puzzle.SetThreat('sk272', 1)", "Puzzle.Thwart('01001a')"],
       ["Puzzle.Damage('skrull_fickle_ally', 10)"],
       {"defausse_rencontre": ["01103"]}, main_exclusive=INERTE, cibles=["sk272"], accepter_choix=True),
    # ===================================================================== sk273 Newbie Training
    _c("sk273 Newbie Training : vaincue, defait un sbire SKRULL non Elite et pioche 1 carte ; l'Elite SKRULL est epargne",
       "When Defeated : `SetTarget(Minion, trait SKRULL, non_trait ELITE)` + `Faces.DefeatUnits` + `DrawUp(1)` ; "
       "sk184 (non Elite) tombe, sk155 (ELITE) reste",
       [HEROS, VIDE, "Puzzle.PutIntoPlay('sk184')", "Puzzle.PutIntoPlay('sk155')", "Puzzle.PutIntoPlay('sk273', under_control=True)",
        "Puzzle.SetThreat('sk273', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"hors_jeu": ["sk184", "sk273"], "en_jeu": ["sk155"], "taille_main": 2},
       main_exclusive=INERTE, cibles=["sk273"], accepter_choix=True),
    _c("sk273 Newbie Training, TEMOIN : aucun sbire SKRULL non Elite : rien n'est defait, aucune carte piochee",
       "sk155 est ELITE, 01101 n'est pas SKRULL : aucune cible legale, la recompense n'est pas offerte",
       [HEROS, VIDE, "Puzzle.PutIntoPlay('sk155')", "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('sk273', under_control=True)",
        "Puzzle.SetThreat('sk273', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"en_jeu": ["sk155", "01101"], "hors_jeu": ["sk273"], "taille_main": 1},
       main_exclusive=INERTE, cibles=["sk273"], accepter_choix=True),
    # ===================================================================== sk274 Searching for Powers
    _c("sk274 Searching for Powers : vaincue, cherche un SUPERPOWER dans le deck et le JOUE sans payer (01022 Ground Stomp : 1 degat a chaque ennemi)",
       "When Defeated : `Search.PlayerCard(trait SUPERPOWER)` -> main -> `PlayCardsLikeInTurn(ignore_resources_cost=True)` ; la main n'a que 1 carte inerte",
       [HEROS, "Puzzle.CreatePlayerDeck('01022')", "Puzzle.PutIntoPlay('sk274', under_control=True)", "Puzzle.SetThreat('sk274', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"degats": [[RHINO, 1]], "defausse": ["01022"], "hors_jeu": ["sk274"]}, main_exclusive=INERTE, cibles=["sk274", "01022"],
       accepter_choix=True),
    _c("sk274 Searching for Powers : l'amelioration SUPERPOWER trouvee dans la DEFAUSSE (sk044 Lazerfist, cout 3) est jouee gratuitement",
       "deck ET defausse sont fouilles ; l'amelioration s'attache a l'identite sans payer ses 3 ressources",
       [HEROS, "Puzzle.CreatePlayerDeck('01088')", "Puzzle.CreatePlayerDiscardPile('sk044')",
        "Puzzle.PutIntoPlay('sk274', under_control=True)", "Puzzle.SetThreat('sk274', 1)"],
       ["Puzzle.Thwart('01001a')"],
       {"attaches": [["01001a", "sk044"]], "hors_jeu": ["sk274"]}, main_exclusive=INERTE, cibles=["sk274", "sk044"],
       accepter_choix=True),
    # ===================================================================== sk275 Skrull Military Training
    _c("sk275 Skrull Military Training : le CTR du heros ne retire AUCUNE menace (3 de depart)",
       "« unless it is being thwarted by a SKRULL ally » : le heros (pas un allie) ne peut pas",
       [HEROS, "Puzzle.PutIntoPlay('sk275', under_control=True)"],
       ["Puzzle.Thwart('01001a')"], {"menace": [["sk275", 3]]}, main_exclusive=INERTE, cibles=["sk275"]),
    _c("sk275 Skrull Military Training : un allie NON Skrull (sk038 Human Torch) ne retire aucune menace",
       "`ThreatCannotBeRemovedFromWhile` : seul un allie SKRULL passe",
       [HEROS, "Puzzle.PutIntoPlay('sk038', under_control=True)", "Puzzle.PutIntoPlay('sk275', under_control=True)"],
       ["Puzzle.Thwart('sk038')"], {"menace": [["sk275", 3]]}, main_exclusive=INERTE, cibles=["sk275"]),
    _c("sk275 Skrull Military Training : un SOUTIEN (sk278 Cadre K) ne peut pas retirer la menace non plus",
       "l'Action de Cadre K retire de la menace sans etre un contre d'allie : bloquee",
       [HEROS, "Puzzle.PutIntoPlay('sk278', under_control=True)", "Puzzle.PutIntoPlay('sk275', under_control=True)"],
       ["Puzzle.Action('sk278')"], {"menace": [["sk275", 3]]}, main_exclusive=INERTE, cibles=["sk275"]),
    _c("sk275 Skrull Military Training : un allie SKRULL (sk264 Jazinda, CTR 3) retire la menace, vainc le complot : pile de victoire",
       "contre d'un allie SKRULL : autorise ; menace 3 -> 0 ; Victory 0 : la carte va en vitrine",
       [HEROS, "Puzzle.PutIntoPlay('sk264', under_control=True)", "Puzzle.PutIntoPlay('sk275', under_control=True)"],
       ["Puzzle.Thwart('sk264')"], {"hors_jeu": ["sk275"], "en_victoire": ["sk275"]}, main_exclusive=INERTE,
       cibles=["sk275"], verifier="cc_victoire"),
    _c("sk275 Skrull Military Training : en pile de victoire, le heros du proprietaire gagne +1 CTR, +1 ATQ, +1 DEF",
       "`GiveKeywordToInPlayWhenApplyThis(Hero, works_in_the_victory_display=True, ...)` ; apres la defaite par deux allies "
       "SKRULL sans bonus propre (sk266 Skymax CTR 2 + sk267 Super-Skrull CTR 2 : 4 >= 3)",
       [HEROS, "Puzzle.PutIntoPlay('sk266', under_control=True)", "Puzzle.PutIntoPlay('sk267', under_control=True)",
        "Puzzle.PutIntoPlay('sk275', under_control=True)"],
       ["Puzzle.Thwart('sk266')", "Puzzle.Thwart('sk267')"], {"attributs": {"thwart": 1, "attack": 1, "defense": 1}},
       main_exclusive=INERTE, cibles=["sk275"]),
    _c("sk275 Skrull Military Training, TEMOIN : tant que la carte est EN JEU (pas en vitrine), aucun bonus",
       "« while this card is in the victory display »",
       [HEROS, "Puzzle.PutIntoPlay('sk275', under_control=True)"],
       [], {"attributs": {"thwart": 0, "attack": 0, "defense": 0}}, main_exclusive=INERTE),
    _c("sk275 Skrull Military Training : le bonus va au heros du PROPRIETAIRE seulement, pas a celui de l'autre joueur",
       "deux joueurs : Spider-Man (proprietaire) +1 aux trois pouvoirs, Lyja rien",
       [HEROS, "Puzzle.ChangeToFace('sk037b', 'sk037a')", "Puzzle.PutIntoPlay('sk266', under_control=True)",
        "Puzzle.PutIntoPlay('sk267', under_control=True)", "Puzzle.PutIntoPlay('sk275', under_control=True)"],
       ["Puzzle.Thwart('sk266')", "Puzzle.Thwart('sk267')"],
       {"p1": {"thwart": 1, "attack": 1, "defense": 1}, "p2": {"thwart": 0, "attack": 0, "defense": 0}},
       main_exclusive=INERTE, cibles=["sk275"], heros2="lyja", verifier="cc_deux_joueurs_bonus"),
    # ===================================================================== sk276 Stealing For Good
    _c("sk276 Stealing For Good : vaincue, ajoute une amelioration du deck a la main et retire sa valeur de menace (01065, cout 2)",
       "When Defeated : `Search.PlayerCard(card_type=Upgrade)` + `GainCard` + `RemoveThreatFromSchemes(cible, printed_cost)` ; "
       "Bomb Scare (menace 5) perd 2",
       [HEROS, "Puzzle.CreatePlayerDeck('01065')", "Puzzle.PutIntoPlay('01109')",
        "Puzzle.PutIntoPlay('sk276', under_control=True)", "Puzzle.SetThreat('sk276', 1)"],
       ["Puzzle.SetThreat('01109', 5)", "Puzzle.Thwart('01001a')"],
       {"en_main": ["01065"], "menace": [["01109", 3]], "hors_jeu": ["sk276"]}, main_exclusive=INERTE,
       cibles=["sk276", "01109"], accepter_choix=True),
    _c("sk276 Stealing For Good : une amelioration de cout 1 (01007 Spider-Tracer) retire 1 menace seulement",
       "la valeur est le cout IMPRIME de l'amelioration trouvee",
       [HEROS, "Puzzle.CreatePlayerDeck('01007')", "Puzzle.PutIntoPlay('01109')",
        "Puzzle.PutIntoPlay('sk276', under_control=True)", "Puzzle.SetThreat('sk276', 1)"],
       ["Puzzle.SetThreat('01109', 5)", "Puzzle.Thwart('01001a')"],
       {"en_main": ["01007"], "menace": [["01109", 4]], "hors_jeu": ["sk276"]}, main_exclusive=INERTE,
       cibles=["sk276", "01109"], accepter_choix=True),
    # ===================================================================== sk289a / sk289b Cooperation Progress Reminder
    _c("sk289a / sk289b Cooperation Progress Reminder : les deux faces (type Insert) se creent sans erreur, rien n'est scripte",
       "carte sans capacite : le moteur sait fabriquer une face `Insert` (comme rule_a / rule_b) ; la regle (victory display) est du ressort du bloc campagne",
       ["Puzzle.CreateCard('sk289a')", "Puzzle.CreateCard('sk289b')"], [], {}, main_exclusive=INERTE),
    # ===================================================================== sk277 Antalya
    _c("sk277 Antalya : Action -> soigne 1 degat de l'identite et s'incline",
       "`WhenInYourPlayTurn(Action)` + `CostFunc.Exhaust` + `HealthUnits` ; l'identite (alter ego) a 3 degats : il en reste 2",
       ["Puzzle.PutIntoPlay('sk277', under_control=True)", "Puzzle.Damage('01001b', 3)"],
       ["Puzzle.Action('sk277')"], {"degats_identite": 2, "exhausted": ["sk277"]}, main_exclusive=INERTE,
       cibles=["01001b"]),
    _c("sk277 Antalya : peut soigner un ALLIE (personnage amical de n'importe quel type)",
       "`SetTarget(Friend, canbe_heal=True)` : sk038 Human Torch (3 PV) a 2 degats ; il n'en reste qu'1",
       ["Puzzle.PutIntoPlay('sk277', under_control=True)", "Puzzle.PutIntoPlay('sk038', under_control=True)",
        "Puzzle.Damage('sk038', 2)"],
       ["Puzzle.Action('sk277')"], {"degats": [["sk038", 1]], "exhausted": ["sk277"]}, main_exclusive=INERTE,
       cibles=["sk038"]),
    _c("sk277 Antalya, TEMOIN : incline, elle n'offre plus son Action (les degats restent)",
       "cout « Exhaust Antalya » : impayable une fois inclinee",
       ["Puzzle.PutIntoPlay('sk277', under_control=True)", "Puzzle.Damage('01001b', 3)", "Puzzle.Exhaust('sk277')"],
       [], {"degats_identite": 3, "exhausted": ["sk277"]}, main_exclusive=INERTE,
       declencher_tolerant=["Puzzle.Action('sk277')"]),
    # ===================================================================== sk278 Cadre K
    _c("sk278 Cadre K : Action -> retire 1 menace d'une manigance (Bomb Scare 4 -> 3) et s'incline",
       "`WhenInYourPlayTurn(Action)` + `RemoveThreatFromSchemes([cible], 1)` ; `SetTarget(Scheme2)`",
       ["Puzzle.PutIntoPlay('sk278', under_control=True)", "Puzzle.PutIntoPlay('01109')"],
       ["Puzzle.SetThreat('01109', 4)", "Puzzle.Action('sk278')"],
       {"menace": [["01109", 3]], "exhausted": ["sk278"]}, main_exclusive=INERTE, cibles=["01109"]),
    _c("sk278 Cadre K, TEMOIN : incline, aucune menace retiree",
       "meme position, Cadre K deja inclinee : la menace reste a 4",
       ["Puzzle.PutIntoPlay('sk278', under_control=True)", "Puzzle.PutIntoPlay('01109')", "Puzzle.Exhaust('sk278')"],
       ["Puzzle.SetThreat('01109', 4)"],
       {"menace": [["01109", 4]]}, main_exclusive=INERTE, declencher_tolerant=["Puzzle.Action('sk278')"]),
    # ===================================================================== sk279 Pool-O-Vision
    _c("sk279 Pool-O-Vision : apres la defaite d'un sbire SKRULL, pioche 1 carte par icone en jeu (Acceleration + Crise = 2)",
       "`Worlds.GetIconsNum([Crisis, Acceleration, Amplify, Hazard])` : Bomb Scare (Acceleration 1) + Crowd Control (Crise 1) = 2",
       [HEROS, "Puzzle.PutIntoPlay('sk279', under_control=True)", "Puzzle.PutIntoPlay('sk184')",
        "Puzzle.PutIntoPlay('01109')", "Puzzle.PutIntoPlay('01108')"],
       ["Puzzle.Damage('sk184', 10)"],
       {"taille_main": 3, "hors_jeu": ["sk184"], "exhausted": ["sk279"], "icones": [["Acceleration", 1], ["Crisis", 1]]},
       main_exclusive=INERTE),
    _c("sk279 Pool-O-Vision : quatre icones differentes (Crise, Acceleration, Amplification, Alea) : plafond de 3 cartes",
       "« to a maximum of 3 » : 01108 Crise, 01109 Acceleration, 16054 Amplify, sk067 Hazard = 4 icones, 3 cartes",
       [HEROS, "Puzzle.PutIntoPlay('sk279', under_control=True)", "Puzzle.PutIntoPlay('sk184')",
        "Puzzle.PutIntoPlay('01109')", "Puzzle.PutIntoPlay('01108')", "Puzzle.PutIntoPlay('16054')",
        "Puzzle.PutIntoPlay('sk067')"],
       ["Puzzle.Damage('sk184', 10)"],
       {"taille_main": 4, "hors_jeu": ["sk184"], "exhausted": ["sk279"],
        "icones": [["Acceleration", 1], ["Crisis", 1], ["Amplify", 1], ["Hazard", 1]]},
       main_exclusive=INERTE),
    _c("sk279 Pool-O-Vision, TEMOIN : sans aucune icone en jeu, aucune carte piochee (mais le soutien s'incline)",
       "0 icone : `n` = 0, rien n'est pioche",
       [HEROS, "Puzzle.PutIntoPlay('sk279', under_control=True)", "Puzzle.PutIntoPlay('sk184')"],
       ["Puzzle.Damage('sk184', 10)"],
       {"taille_main": 1, "hors_jeu": ["sk184"]}, main_exclusive=INERTE),
    _c("sk279 Pool-O-Vision, TEMOIN : la defaite d'un sbire NON Skrull (Hydra Mercenary) ne declenche rien",
       "« a SKRULL minion » : 01101 n'a pas le trait ; la main reste a 1 carte, le soutien reste pret",
       [HEROS, VIDE, "Puzzle.PutIntoPlay('sk279', under_control=True)", "Puzzle.PutIntoPlay('01101')",
        "Puzzle.PutIntoPlay('01109')"],
       ["Puzzle.Damage('01101', 10)"],
       {"taille_main": 1, "hors_jeu": ["01101"], "pret": ["sk279"]}, main_exclusive=INERTE),
    _c("sk279 Pool-O-Vision, TEMOIN : « Hero Response » : en alter ego (forme hors heros) rien n'est pioche",
       "la Reponse de heros n'est offerte qu'en forme heros",
       ["Puzzle.PutIntoPlay('sk279', under_control=True)", "Puzzle.PutIntoPlay('sk184')", "Puzzle.PutIntoPlay('01109')"],
       ["Puzzle.Damage('sk184', 10)"],
       {"taille_main": 1, "hors_jeu": ["sk184"], "pret": ["sk279"]}, main_exclusive=INERTE),
    # ===================================================================== sk280 Princess Anelle
    _c("sk280 Princess Anelle : cout X = joueurs + ennemis SKRULL en jeu : solo, aucun ennemi SKRULL = 1",
       "`IncreaseResourceCostToPlay('This', ...)` ; Rhino (BRUTE, CRIMINAL) n'est pas SKRULL",
       [], [], {"carte": "sk280", "cout": 1}, main=["sk280"], verifier="cc_cout"),
    _c("sk280 Princess Anelle : deux ennemis SKRULL en jeu (sbire Dard'van et General Kalamari) = 1 + 2 = 3",
       "les SBIRES SKRULL comptent, Elite ou non",
       ["Puzzle.PutIntoPlay('sk184')", "Puzzle.PutIntoPlay('sk155')"], [], {"carte": "sk280", "cout": 3}, main=["sk280"],
       verifier="cc_cout"),
    _c("sk280 Princess Anelle : le MECHANT SKRULL compte aussi (scenario Paibok) = 1 + 1 = 2",
       "`EnnemisSkrull` : sbires ET mechant porteurs du trait ; Paibok (sk141) est SKRULL",
       [], [], {"carte": "sk280", "cout": 2}, main=["sk280"], scenario="sk_paibok", verifier="cc_cout"),
    _c("sk280 Princess Anelle : un sbire non Skrull (Hydra Mercenary) ne compte pas = 1",
       "seul le trait SKRULL compte",
       ["Puzzle.PutIntoPlay('01101')"], [], {"carte": "sk280", "cout": 1}, main=["sk280"], verifier="cc_cout"),
    _c("sk280 Princess Anelle : deux joueurs, aucun ennemi SKRULL = 2",
       "« the total number of PLAYERS » : 2 joueurs",
       [], [], {"carte": "sk280", "cout": 2}, main=["sk280"], heros2="lyja", verifier="cc_cout"),
    _c("sk280 Princess Anelle : ALLIANCE (2 joueurs) : un cout de 4 qu'un joueur seul ne peut pas payer l'est a deux",
       "cout 2 (joueurs) + 2 ennemis SKRULL = 4 ; la main du joueur 1 (une carte) + l'alter ego ne couvrent que 2 ; le joueur 2 aide a payer",
       ["Puzzle.PutIntoPlay('sk184')", "Puzzle.PutIntoPlay('sk155')"], [], {"en_jeu": ["sk280"]}, main_exclusive=["01086"],
       jouer=["sk280"], heros2="lyja"),
    _c("sk280 Princess Anelle : apres la phase des joueurs, elle quitte la PARTIE (pas la defausse) et la phase du mechant est sautee",
       "Response `AfterPhaseEnd('Player')` + cout `RemoveFromGame` ; `monde.skip_villain_phases` passe a 1 (lu par la boucle de round)",
       ["Puzzle.PutIntoPlay('sk280', under_control=True)"], ["Puzzle.EndPlayerPhase()"],
       {"hors_jeu": ["sk280"], "phases_sautees": 1, "defausse_vide_de": ["sk280"]}, main_exclusive=INERTE, verifier="cc_anelle"),
    _c("sk280 Princess Anelle, TEMOIN : sans Anelle, la phase du mechant n'est pas sautee",
       "ligne de base : `skip_villain_phases` reste a 0",
       [], ["Puzzle.EndPlayerPhase()"], {"phases_sautees": 0}, main_exclusive=INERTE, verifier="cc_anelle"),
    # ===================================================================== sk281 Skrull Battleship
    _c("sk281 Skrull Battleship : jouable si on controle un allie SKRULL (Jazinda en jeu)",
       "`CanPlayThisSupportCard(conditions=[...])` : cout 2 paye par 01088 (YY)",
       ["Puzzle.PutIntoPlay('sk264', under_control=True)"], [], {"en_jeu": ["sk281"]}, main_exclusive=["01088"],
       jouer=["sk281"]),
    _c("sk281 Skrull Battleship, TEMOIN : sans allie SKRULL (Human Torch, non Skrull), la carte reste en main",
       "« Play only if you control a SKRULL ally » : un allie non Skrull ne suffit pas",
       ["Puzzle.PutIntoPlay('sk038', under_control=True)"], [], {"hors_jeu": ["sk281"], "en_main": ["sk281"]},
       main_exclusive=["01088"], jouer=["sk281"]),
    _c("sk281 Skrull Battleship : Ressource de heros -> une ressource [wild] qui paie le cout manquant d'une carte (Jazinda, cout 3)",
       "hand 01089 (BB) + Battleship (wild) = 3 ; sans Battleship : 2 seulement, Jazinda reste en main (cas suivant) ; forme heros (pas de ressource d'alter ego)",
       [HEROS, "Puzzle.PutIntoPlay('sk281', under_control=True)", "Puzzle.PutIntoPlay('sk278', under_control=True)"],
       [], {"en_jeu": ["sk264"], "exhausted": ["sk281"]}, main_exclusive=["01089"], jouer=["sk264"]),
    _c("sk281 Skrull Battleship, TEMOIN : sans le Battleship, 2 ressources ne paient pas Jazinda (cout 3) : elle reste en main",
       "ligne de base du precedent",
       [HEROS], [], {"hors_jeu": ["sk264"], "en_main": ["sk264"]}, main_exclusive=["01089"], jouer=["sk264"]),
    # ===================================================================== sk282 Skrull Kill Krew
    _c("sk282 Skrull Kill Krew : Action de heros -> 1 degat a un sbire SKRULL, s'incline (sbire non vaincu)",
       "`WhenInYourPlayTurn(HeroAction)` + `Exhaust` ; sk184 (4 PV) prend 1 degat",
       [HEROS, VIDE, "Puzzle.PutIntoPlay('sk282', under_control=True)", "Puzzle.PutIntoPlay('sk184')"],
       ["Puzzle.Action('sk282')"], {"degats": [["sk184", 1]], "exhausted": ["sk282"]}, main_exclusive=INERTE),
    _c("sk282 Skrull Kill Krew : si le sbire est VAINCU par ce coup, le soutien se redresse",
       "`if_this_attack_defeats` + `Faces.ReadyAll` : sk184 a 3 degats (1 PV restant) ; le soutien reste pret",
       [HEROS, VIDE, "Puzzle.PutIntoPlay('sk282', under_control=True)", "Puzzle.PutIntoPlay('sk184')",
        "Puzzle.Damage('sk184', 3)"],
       ["Puzzle.Action('sk282')"], {"hors_jeu": ["sk184"], "pret": ["sk282"]}, main_exclusive=INERTE),
    _c("sk282 Skrull Kill Krew, TEMOIN : sans sbire SKRULL (Hydra Mercenary seul), aucune action offerte",
       "`SetTarget(Minion, trait SKRULL)` : 01101 n'est pas une cible legale ; il reste intact, le soutien pret",
       [HEROS, VIDE, "Puzzle.PutIntoPlay('sk282', under_control=True)", "Puzzle.PutIntoPlay('01101')"],
       [], {"degats": [["01101", 0]], "pret": ["sk282"]}, main_exclusive=INERTE,
       declencher_tolerant=["Puzzle.Action('sk282')"]),
    _c("sk282 Skrull Kill Krew, TEMOIN : « Hero Action » : en alter ego, rien ne se passe",
       "Action de heros refusee hors forme heros",
       [VIDE, "Puzzle.PutIntoPlay('sk282', under_control=True)", "Puzzle.PutIntoPlay('sk184')"],
       [], {"degats": [["sk184", 0]], "pret": ["sk282"]}, main_exclusive=INERTE,
       declencher_tolerant=["Puzzle.Action('sk282')"]),
    # ===================================================================== sk283 3-D Man's Goggles
    _c("sk283 3-D Man's Goggles : s'attache a un allie NON Skrull (Human Torch), jamais a un Skrull",
       "`CanPlayThisUpgradeCard(CardFinder(Ally, non_trait SKRULL))` ; Jazinda (SKRULL) et Human Torch en jeu : seule Human Torch est cible",
       ["Puzzle.PutIntoPlay('sk264', under_control=True)", "Puzzle.PutIntoPlay('sk038', under_control=True)"],
       [], {"accroche_a": [["sk283", "sk038"]]}, main_exclusive=["01089"], jouer=["sk283"]),
    _c("sk283 3-D Man's Goggles, TEMOIN : avec SEULEMENT un allie Skrull (Jazinda), la carte n'est pas jouable (reste en main)",
       "aucune cible legale",
       ["Puzzle.PutIntoPlay('sk264', under_control=True)"], [], {"hors_jeu": ["sk283"], "en_main": ["sk283"]},
       main_exclusive=["01089"], jouer=["sk283"]),
    _c("sk283 3-D Man's Goggles : l'allie qui attaque un ennemi SKRULL ne prend AUCUN degat consequent (Human Torch ATQ 2*)",
       "Interruption `WhenUnitWouldAttack` + `DoesNotTakeConsequentialDamage` ; sk184 prend 2, Human Torch 0",
       [VIDE, "Puzzle.PutIntoPlay('sk038', under_control=True)", "Puzzle.PutIntoPlay('sk184')"],
       [], {"degats": [["sk184", 2], ["sk038", 0]]}, main_exclusive=["01089"], jouer=["sk283"],
       declencher_apres=["Puzzle.Attack('sk038')"], cibles=["sk184"]),
    _c("sk283 3-D Man's Goggles, TEMOIN : contre un ennemi NON Skrull (Hydra Mercenary), l'allie prend son degat consequent",
       "l'Interruption ne vise que les ennemis SKRULL",
       [VIDE, "Puzzle.PutIntoPlay('sk038', under_control=True)", "Puzzle.PutIntoPlay('01101')"],
       [], {"degats": [["01101", 2], ["sk038", 1]]}, main_exclusive=["01089"], jouer=["sk283"],
       declencher_apres=["Puzzle.Attack('sk038')"], cibles=["01101"]),
    _c("sk283 3-D Man's Goggles, TEMOIN : sans les lunettes, la meme attaque contre un Skrull coute 1 degat a l'allie",
       "ligne de base du premier cas d'Interruption",
       [VIDE, "Puzzle.PutIntoPlay('sk038', under_control=True)", "Puzzle.PutIntoPlay('sk184')"],
       ["Puzzle.Attack('sk038')"], {"degats": [["sk184", 2], ["sk038", 1]]}, main_exclusive=INERTE, cibles=["sk184"]),
    # ===================================================================== sk284 Inhibitor Mask
    _c("sk284 Inhibitor Mask : s'attache a un ennemi SKRULL ; son texte imprime est ignore (Skrull Commander ne donne plus +1 ATQ)",
       "`CanPlayThisUpgradeCard(Enemy, SKRULL)` + `GiveKeywordToAttached(treat_as_blank)` ; sk113 « each other SKRULL minion gets +1 ATK » : sk184 ne gagne rien",
       [VIDE, "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk184')"],
       [], {"accroche_a": [["sk284", "sk113"]], "attributs_carte": [["sk184", "attack", 0]]}, main_exclusive=["01088"],
       jouer=["sk284"], cibles=["sk113"]),
    _c("sk284 Inhibitor Mask, TEMOIN : sans le masque, Skrull Commander donne bien +1 ATQ a sk184",
       "ligne de base du precedent",
       [VIDE, "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk184')"],
       [], {"attributs_carte": [["sk184", "attack", 1]]}, main_exclusive=INERTE),
    _c("sk284 Inhibitor Mask, TEMOIN : avec SEULEMENT des ennemis non Skrull (Rhino), la carte n'est pas jouable",
       "« Attach to a SKRULL enemy » : aucune cible legale",
       [VIDE], [], {"hors_jeu": ["sk284"], "en_main": ["sk284"]}, main_exclusive=["01088"], jouer=["sk284"]),
    _c("sk284 Inhibitor Mask : TEMPORARY : defaussee a la fin du round, le texte redevient actif",
       "`ProcessTemporary` (fin de round) defausse l'amelioration, meme attachee a un ennemi",
       [VIDE, "Puzzle.PutIntoPlay('sk113')", "Puzzle.PutIntoPlay('sk184')"],
       [], {"hors_jeu": ["sk284"], "attributs_carte": [["sk184", "attack", 1]]}, main_exclusive=["01088"],
       jouer=["sk284"], cibles=["sk113"], verifier="cc_apres_fin_de_round"),
    # ===================================================================== sk285 Ultimate Nullifier
    _c("sk285 Ultimate Nullifier : l'ennemi porteur ne peut PAS s'activer (l'attaque de sk184 est annulee)",
       "`EnemyCannotActivate(NonKeyword, 'AttachedEnemy')` ; sans le Nullifier sk184 infligerait 2 degats",
       [VIDE, "Puzzle.PutIntoPlay('sk184')"],
       [], {"degats_identite": 0, "accroche_a": [["sk285", "sk184"]]}, main_exclusive=["01088"], jouer=["sk285"],
       declencher_apres=["Puzzle.Attack('sk184')"]),
    _c("sk285 Ultimate Nullifier, TEMOIN : sans lui, l'attaque de sk184 inflige 2 degats a l'alter ego",
       "ligne de base du precedent",
       [VIDE, "Puzzle.PutIntoPlay('sk184')"], ["Puzzle.Attack('sk184')"], {"degats_identite": 2}, main_exclusive=INERTE),
    _c("sk285 Ultimate Nullifier : sur le MECHANT (Paibok SKRULL), il porte 1 icone Hazard (solo = 1 par joueur)",
       "`ThisGainKeyword(hazard=1)` : `Worlds.GetPlayerNumIcon` icones tant qu'il est attache a un mechant ; scenario Paibok",
       [], [], {"icones": [["Hazard", 1]], "accroche_a": [["sk285", "sk141"]]}, main_exclusive=["01088"],
       jouer=["sk285"], scenario="sk_paibok", cibles=["sk141"]),
    _c("sk285 Ultimate Nullifier : a DEUX joueurs il porte 2 icones Hazard sur le mechant",
       "« 1[per_hero] hazard icon » : une icone par joueur",
       [], [], {"icones": [["Hazard", 2]], "accroche_a": [["sk285", "sk141"]]}, main_exclusive=["01088"],
       jouer=["sk285"], scenario="sk_paibok", cibles=["sk141"], heros2="lyja"),
    _c("sk285 Ultimate Nullifier, TEMOIN : sur un SBIRE (sk184), aucune icone Hazard",
       "« while attached to the VILLAIN » : le sbire ne declenche pas l'icone",
       [VIDE, "Puzzle.PutIntoPlay('sk184')"],
       [], {"icones": [["Hazard", 0]], "accroche_a": [["sk285", "sk184"]]}, main_exclusive=["01088"], jouer=["sk285"]),
    _c("sk285 Ultimate Nullifier : TEMPORARY : defaussee a la fin du round",
       "`ProcessTemporary` : l'icone et l'interdiction d'activer disparaissent avec elle",
       [VIDE, "Puzzle.PutIntoPlay('sk184')"],
       [], {"hors_jeu": ["sk285"]}, main_exclusive=["01088"], jouer=["sk285"], verifier="cc_apres_fin_de_round"),
    # ===================================================================== sk286 Reverting Device
    _c("sk286 Reverting Device : sous le controle du joueur, chaque sbire SKRULL engage avec lui perd 1 MNG (sk184 : 2 -> 1)",
       "`GiveKeywordToInPlayWhenApplyThis(Minion SKRULL, scheme=-1, get_new_value=engage avec moi)` ; jouee pour de vrai (cout 0)",
       [VIDE, "Puzzle.PutIntoPlay('sk184')"],
       [], {"attributs_carte": [["sk184", "scheme", -1]], "attaches": [["01001b", "sk286"]]}, main_exclusive=INERTE,
       jouer=["sk286"]),
    _c("sk286 Reverting Device, TEMOIN : un sbire NON Skrull engage (Shocker, MNG 1) n'est pas touche",
       "le trait SKRULL est exige",
       [VIDE, "Puzzle.PutIntoPlay('01103')"],
       [], {"attributs_carte": [["01103", "scheme", 0]]}, main_exclusive=INERTE, jouer=["sk286"]),
    _c("sk286 Reverting Device, TEMOIN : sans la carte, sk184 garde son MNG imprime",
       "ligne de base",
       [VIDE, "Puzzle.PutIntoPlay('sk184')"], [], {"attributs_carte": [["sk184", "scheme", 0]]}, main_exclusive=INERTE),
    _c("sk286 Reverting Device : un sbire SKRULL engage avec l'AUTRE joueur n'est pas touche",
       "« engaged with YOU » : deux joueurs, sk184 est engage avec le joueur 2",
       [VIDE, "Puzzle.PutIntoPlay('sk184')", "Puzzle.Engage('sk184', 1)"],
       [], {"attributs_carte": [["sk184", "scheme", 0]]}, main_exclusive=INERTE, jouer=["sk286"], heros2="lyja"),
    _c("sk286 Reverting Device : le bonus se recalcule quand un sbire SKRULL s'engage APRES la pose de la carte",
       "`AfterMinionEngagePlayer` relance le calcul : sk184 entre en jeu apres l'amelioration",
       [VIDE, "Puzzle.PutIntoPlay('sk286', under_control=True)"], ["Puzzle.PutIntoPlay('sk184')"],
       {"attributs_carte": [["sk184", "scheme", -1]]}, main_exclusive=INERTE),
    # ===================================================================== sk287 Skrull Shapeshifter
    _c("sk287 Skrull Shapeshifter : l'identite (alter ego) gagne le trait SKRULL",
       "`GiveKeywordToAttached('You', trait='SKRULL')` ; jouee pour de vrai (cout 1)",
       [], [], {"traits": ["SKRULL"]}, main_exclusive=["01088"], jouer=["sk287"]),
    _c("sk287 Skrull Shapeshifter : le trait vaut AUSSI en forme heros (contre-cas de l'autre forme)",
       "RECETTES §3 : « You » = les deux faces de l'identite",
       [HEROS], [], {"traits": ["SKRULL"]}, main_exclusive=["01088"], jouer=["sk287"]),
    _c("sk287 Skrull Shapeshifter, TEMOIN : sans la carte, l'identite n'est pas SKRULL",
       "ligne de base", [], [], {"traits_absents": ["SKRULL"]}, main_exclusive=INERTE),
    _c("sk287 Skrull Shapeshifter : quand le joueur serait vaincu, ses PV passent a 1 a la place, puis la carte est defaussee",
       "Interruption `WhenUnitWouldBeDefeated('You')` + `SetBeInstead` + `SetHealth(1)` + `DiscardAll` : alter ego a 10 PV, 99 degats",
       ["Puzzle.PutIntoPlay('sk287', under_control=True)"], ["Puzzle.Damage('01001b', 99)"],
       {"degats_identite": 9, "hors_jeu": ["sk287"], "defausse": ["sk287"]}, main_exclusive=INERTE),
    # ===================================================================== sk288 Sy-Torak Gem
    _c("sk288 Sy-Torak Gem : +3 points de vie (alter ego : 13 PV max)",
       "`GiveKeywordToAttached('You', health=3)` ; jouee pour de vrai (cout 2, 01088)",
       [], [], {"attributs": {"health": 3}}, main_exclusive=["01088"], jouer=["sk288"]),
    _c("sk288 Sy-Torak Gem : le heros gagne +1 ATQ en forme heros",
       "`GiveKeywordToAttached(Hero, attack=1)`",
       [HEROS], [], {"attributs": {"attack": 1, "health": 3}}, main_exclusive=["01088"], jouer=["sk288"]),
    _c("sk288 Sy-Torak Gem, TEMOIN : sans la carte, aucun bonus",
       "ligne de base (heros)", [HEROS], [], {"attributs": {"attack": 0, "health": 0}}, main_exclusive=INERTE),
    _c("sk288 Sy-Torak Gem : deck epuise, une ressource [energy] est depensee et la gemme reste en jeu",
       "Interruption forcee `AfterDeckRunOut` ; `ForChoiceAbilityWithCost(Cost('Y'))` payee par 01088 (YY) de la main",
       ["Puzzle.PutIntoPlay('sk288', under_control=True)", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090')"],
       ["Puzzle.Draw(1)"], {"en_jeu": ["sk288"], "defausse": ["01088"]}, main_exclusive=["01088"]),
    _c("sk288 Sy-Torak Gem : la gemme defaussee en pleine pioche fait perdre ses +3 PV : l'identite (11 degats sur 13) tombe, sans planter",
       "autoplay du 15/10/2026 : `Eliminate` levait `AssertionError` quand le joueur etait deja elimine PENDANT la pioche ; "
       "correctif `player_action.py` (garde `not player.is_eliminated`)",
       ["Puzzle.PutIntoPlay('sk288', under_control=True)", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090')",
        "Puzzle.Damage('01001b', 11)"],
       ["Puzzle.Draw(3)"], {"defaite": True}, main_exclusive=["01089"], verifier="cc_defaite"),
    _c("sk288 Sy-Torak Gem : deck epuise SANS ressource [energy] payable : la gemme est defaussee",
       "`Otherwise` : la branche payante n'est pas offerte (main = 01089 BB) ; la gemme part en defausse",
       ["Puzzle.PutIntoPlay('sk288', under_control=True)", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090')"],
       ["Puzzle.Draw(1)"], {"hors_jeu": ["sk288"], "defausse": ["sk288"]}, main_exclusive=["01089"]),
]

# Verifications outillees de ce bloc (executees dans le processus fils, comme VERIFICATIONS de test_capacites).
VERIFICATIONS = r'''
def cc_allies(monde, aides):
    """Limite d'allies : `allies_comptes` = nombre exact compte contre la limite, `allies_comptes_max` = plafond."""
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    soucis = []
    for card_id in attendu.get("en_jeu") or []:
        if aides["par_id"](monde, card_id) is None:
            soucis.append(f"{card_id} n'est pas en jeu")
    n = joueur.limit_ally.curr_ally
    en_jeu = len(joueur.GetControlAllies())
    if "allies_en_jeu" in attendu and en_jeu != attendu["allies_en_jeu"]:
        soucis.append(f"allies en jeu = {en_jeu} (attendu {attendu['allies_en_jeu']})")
    if "allies_comptes" in attendu and n != attendu["allies_comptes"]:
        soucis.append(f"allies comptes contre la limite = {n} (attendu {attendu['allies_comptes']})")
    if "allies_comptes_max" in attendu and n > attendu["allies_comptes_max"]:
        soucis.append(f"allies comptes contre la limite = {n} (plafond {attendu['allies_comptes_max']})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{n} allie(s) compte(s) contre la limite"


def cc_jazinda_deux_joueurs(monde, aides):
    """Deux joueurs : Jazinda (joueur 1) donne +1 CTR a SON heros seulement."""
    attendu = aides["cas"]["attendu"]
    soucis = []
    for rang, cle in ((0, "thwart_joueur1"), (1, "thwart_joueur2")):
        identite = monde.players[rang].GetIdentity()
        if not hasattr(identite, "thwart"):
            soucis.append(f"joueur {rang + 1} : l'identite n'a pas de CTR")
            continue
        ecart = identite.thwart - identite.printed_thwart
        if ecart != attendu[cle]:
            soucis.append(f"joueur {rang + 1} : ecart de CTR = {ecart} (attendu {attendu[cle]})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "bonus de CTR chez le joueur 1 seulement"


def cc_war_skrull(monde, aides):
    """sk268 : la carte est un SBIRE engage avec le joueur, nom/MNG/ATQ/PV repris de l'allie."""
    from game.card.face.card_type import Minion
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    sbires = [m for m in joueur.engaged_minions.Get() if m.printed_name == attendu["nom"]]
    if not sbires:
        return False, f"aucun sbire « {attendu['nom']} » engage (engages = {[m.printed_name for m in joueur.engaged_minions.Get()]})"
    m = sbires[0]
    soucis = []
    if not Minion.IsType(m):
        soucis.append("la face n'est pas un sbire")
    if m.scheme != attendu["scheme"]:
        soucis.append(f"MNG = {m.scheme} (attendu {attendu['scheme']})")
    if m.attack != attendu["attack"]:
        soucis.append(f"ATQ = {m.attack} (attendu {attendu['attack']})")
    if m.max_health != attendu["pv"]:
        soucis.append(f"PV max = {m.max_health} (attendu {attendu['pv']})")
    if not m.HasTrait("SKRULL"):
        soucis.append("le sbire n'a pas le trait SKRULL")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "Chilly McHotpants est un sbire SKRULL engage (MNG 2, ATQ 2, 5 PV)"


def cc_cout(monde, aides):
    """Cout de ressources CALCULE par le moteur pour jouer la carte de la main (`WhenCalculateEffectCost`)."""
    from game.message import Message
    attendu = aides["cas"]["attendu"]
    joueur = monde.players[0]
    cartes = [f for f in joueur.hand_cards.GetAll() if getattr(f.paper, "card_id", None) == attendu["carte"]]
    if not cartes:
        return False, f"{attendu['carte']} n'est pas en main"
    effets = cartes[0].effect.Find(func_name="Play")
    if not effets:
        return False, "aucun effet de jeu"
    calcul = Message.WhenCalculateEffectCost(joueur, effets[0], [])
    calcul.Send()
    valeur = calcul.cost.val
    if valeur != attendu["cout"]:
        return False, f"cout calcule = {valeur} (attendu {attendu['cout']})"
    return True, f"cout calcule = {valeur}"


def cc_anelle(monde, aides):
    """sk280 : `skip_villain_phases` (lu par la boucle de round) et la carte n'est pas en defausse."""
    ok, message = etat_attendu(monde, aides)
    attendu = aides["cas"]["attendu"]
    soucis = [] if ok else [message]
    if monde.skip_villain_phases != attendu["phases_sautees"]:
        soucis.append(f"phases du mechant a sauter = {monde.skip_villain_phases} (attendu {attendu['phases_sautees']})")
    defausse = [getattr(f.paper, "card_id", None) for f in monde.players[0].discard_pile.GetAll()]
    for carte in attendu.get("defausse_vide_de") or []:
        if carte in defausse:
            soucis.append(f"{carte} est en DEFAUSSE (elle devait quitter la partie) : {defausse}")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"phases du mechant a sauter = {monde.skip_villain_phases} ; defausse = {defausse}"


def cc_apres_fin_de_round(monde, aides):
    """Joue la fin de round du moteur (`ProcessTemporary` : defausse les cartes TEMPORARY) puis `etat_attendu`."""
    from game.effect.rule import GameRule
    monde.ProcessTemporary(GameRule(monde.players[0].GetIdentity()))
    return etat_attendu(monde, aides)


def cc_defaite(monde, aides):
    """La partie est perdue (identite vaincue) : `monde.is_game_over` et le joueur est elimine."""
    if not monde.is_game_over:
        return False, "la partie n'est pas terminee"
    if not monde.players[0].is_eliminated and not monde.const_players[0].is_eliminated:
        return False, "le joueur n'est pas elimine"
    return True, "joueur elimine, partie terminee"


def cc_victoire(monde, aides):
    """`en_victoire` : card_ids qui doivent etre dans la pile de victoire ; le reste via etat_attendu."""
    ok, message = etat_attendu(monde, aides)
    attendu = aides["cas"]["attendu"]
    vitrine = [getattr(f.paper, "card_id", None) for f in monde.victory_display.GetAll()]
    manquants = [c for c in attendu.get("en_victoire") or [] if c not in vitrine]
    if manquants:
        return False, f"absent(s) de la pile de victoire : {manquants} (vitrine = {vitrine})"
    return ok, message if not ok else f"{message} ; pile de victoire = {vitrine}"


def cc_deux_joueurs_bonus(monde, aides):
    """Bonus de stats (`thwart`, `attack`, `defense`) de l'identite de chaque joueur : `p1` et `p2`."""
    attendu = aides["cas"]["attendu"]
    soucis = []
    for rang, cle in ((0, "p1"), (1, "p2")):
        identite = monde.players[rang].GetIdentity()
        for nom, ecart in attendu[cle].items():
            courant = getattr(identite, nom)
            base = getattr(identite, {"thwart": "printed_thwart", "attack": "printed_attack",
                                       "defense": "printed_defense"}[nom])
            if courant != base + ecart:
                soucis.append(f"joueur {rang + 1} : {nom} = {courant} (imprime {base}, attendu {base + ecart})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "bonus conformes pour les deux joueurs"


def cc_fickle(monde, aides):
    """sk272 : le sbire est devenu un ALLIE sous le controle du joueur 1 (gabarit `skrull_fickle_ally`)."""
    from game.card.face.card_type import Ally
    ok, message = etat_attendu(monde, aides)
    attendu = aides["cas"]["attendu"]
    allie = aides["par_id"](monde, "skrull_fickle_ally")
    if attendu.get("aucun_allie_fickle"):
        if allie is not None:
            return False, "un allie est apparu alors qu'aucun sbire non Elite n'etait cherchable"
        return ok, message if not ok else "aucun allie cree (le deck ne contenait que l'Elite)"
    if allie is None:
        return False, "aucun allie issu de Fickle Alliance en jeu"
    soucis = [] if ok else [message]
    if not Ally.IsType(allie):
        soucis.append("la face n'est pas un allie")
    if allie.printed_name != attendu["nom"]:
        soucis.append(f"nom = {allie.printed_name} (attendu {attendu['nom']})")
    if allie.thwart != attendu["thwart"]:
        soucis.append(f"CTR = {allie.thwart} (attendu {attendu['thwart']} : le MNG imprime)")
    if allie.attack != attendu["attack"]:
        soucis.append(f"ATQ = {allie.attack} (attendu {attendu['attack']})")
    if not allie.HasTrait(attendu["trait"]):
        soucis.append(f"trait {attendu['trait']} perdu (traits = {allie.traits})")
    if allie.attack_consequential_damage != attendu["csq_atk"]:
        soucis.append(f"degats consequents a l'attaque = {allie.attack_consequential_damage}")
    if allie.thwart_consequential_damage != attendu["csq_thw"]:
        soucis.append(f"degats consequents au contre = {allie.thwart_consequential_damage}")
    if allie.GetControlBy() != monde.players[0]:
        soucis.append("l'allie n'est pas sous le controle du joueur 1")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{allie.printed_name} est un allie (CTR {allie.thwart}, ATQ {allie.attack}, traits {allie.traits})"
'''
