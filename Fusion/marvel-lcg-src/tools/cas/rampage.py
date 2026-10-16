# Cas test_capacites du mot-cle MAISON « Rampage X » (aspects TMNT, Inkwire) et de la recette
# « reskin d'une carte joueur par ability_link » (socle des packs tmnt_aspect_*, 16/10/2026).
# Filtre : `[rampage]` (mot-cle + ua015 Demolish) et `[reskin]` (ua006 Bo-Wing, ua009 Clobber).
# Fiche : docs/reference/mots-cles/rampage.md ; recette : docs/reference/RECETTES-MOTEUR.md.
#
# Conventions :
#  - Spider-Man (01001) demarre en ALTER EGO ; HEROS le met en forme heros (10 PV) ;
#  - `main_exclusive` : la main ne contient QUE la carte jouee et de quoi payer
#    (01090 Strength = RR, 01088 Energy = YY : 4 ressources pour un cout de 3) ;
#  - le deck du joueur est VIDE puis reconstruit avec des 01089 Genius, absents de la main :
#    chaque Genius en defausse vient donc de Rampage ;
#  - Rhino 01094 (14 PV) est la cible de mesure, 01101 Hydra Mercenary (3 PV) le sbire ;
#  - tr008 Shell Cycle (pack raphael) est le soutien NYC de reference.
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
DECK6 = "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089', '01089')"
PAIE3 = ["ua015", "01090", "01088"]
# ⚠ `Puzzle.Tough('01101')` viserait une copie du DECK RENCONTRE (FindOrCreateFace y cherche avant la
# table) : on passe la face rendue par PutIntoPlay.
SBIRE_TENACE = "Puzzle.Tough(Puzzle.PutIntoPlay('01101'))"


def _c(tag, nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": f"[{tag}] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ Rampage 3 sur ua015 Demolish
    _c("rampage", "ua015 Demolish : Rampage 3 paye (3 degats a l'identite, 3 cartes du deck defaussees) puis 8 degats a Rhino",
       "« As an additional cost, take 3 damage and discard 3 cards from the top of your deck » + « Deal 8 damage to an "
       "enemy » : deck de 6 Genius -> 3 restent ; l'evenement est joue (defausse) et l'effet resolu (8 degats)",
       [HEROS, SANS_DECK, DECK6], [],
       {"degats_identite": 3, "taille_deck_joueur": 3, "degats": [["01094", 8]], "defausse": ["ua015", "01089"]},
       main_exclusive=PAIE3, jouer=["ua015"], cibles=["01094"]),
    _c("rampage", "ua015 Demolish : deck de 2 cartes (< X) : la carte reste jouable, le cout est PAYE, 8 degats",
       "arbitrage du 25/09/2026 repris par Rampage (fiche rampage.md, lecture 1) : on defausse ce qui reste, le deck se "
       "remelange, rien de plus n'est defausse ; le cout est paye, l'effet a lieu",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01089')"], [],
       {"degats_identite": 3, "degats": [["01094", 8]], "defausse": ["ua015"]},
       main_exclusive=PAIE3, jouer=["ua015"], cibles=["01094"]),
    _c("rampage", "ua015 Demolish : deck VIDE : cout impayable, AUCUN degat pris, Rhino intact",
       "« if they cannot pay for all of the costs at once, they do not pay any » : la defausse est verifiee AVANT les degats",
       [HEROS, SANS_DECK], [],
       {"degats_identite": 0, "degats": [["01094", 0]], "en_main": ["ua015"]},
       main_exclusive=PAIE3, jouer=["ua015"], cibles=["01094"]),
    _c("rampage", "ua015 Demolish : identite Tenace : degats du cout empeches = cout NON paye, ni defausse ni 8 degats",
       "Rules Reference « Cost » : « If taking damage is a cost, that cost is not considered paid unless all of that "
       "damage was taken » ; la defausse (2e partie du cout) n'a pas lieu",
       [HEROS, SANS_DECK, DECK6, "Puzzle.Tough('01001a')"], [],
       {"degats_identite": 0, "taille_deck_joueur": 6, "degats": [["01094", 0]]},
       main_exclusive=PAIE3, jouer=["ua015"], cibles=["01094"]),
    _c("rampage", "ua015 Demolish : soutien NYC controle -> percant ET deferlement (sbire Tenace a 3 PV tue, 5 de trop sur Rhino)",
       "« If you control a NYC support, this attack gains overkill and piercing » : piercing defausse le Tenace du sbire, "
       "overkill reporte 8 - 3 = 5 degats sur le vilain",
       [HEROS, SANS_DECK, DECK6, "Puzzle.PutIntoPlay('tr008', under_control=True)", SBIRE_TENACE], [],
       {"hors_jeu": ["01101"], "degats": [["01094", 5]], "degats_identite": 3},
       main_exclusive=PAIE3, jouer=["ua015"], cibles=["01101"]),
    _c("rampage", "ua015 Demolish : SANS soutien NYC, ni percant ni deferlement (le Tenace du sbire absorbe tout)",
       "contre-cas de la condition : meme montage sans tr008 ; le sbire survit (Tenace consomme), Rhino intact",
       [HEROS, SANS_DECK, DECK6, SBIRE_TENACE], [],
       {"en_jeu": ["01101"], "degats": [["01094", 0], ["01101", 0]], "degats_identite": 3},
       main_exclusive=PAIE3, jouer=["ua015"], cibles=["01101"]),

    # ============================================================ reskin par ability_link
    _c("reskin", "ua009 Clobber (reskin de 18012) : 3 degats et retour en main (premiere carte du round)",
       "IDENTIQUE a 18012 : `ability_link` branche le script de l'officielle sur la carte TMNT ; la capacite vit sur ua009",
       [HEROS], [],
       {"degats": [["01094", 3]], "en_main": ["ua009"]},
       main_exclusive=["ua009", "01090"], jouer=["ua009"], cibles=["01094"]),
    _c("reskin", "ua009 Clobber : TEMOIN 18012 (officielle), meme montage, meme resultat",
       "le reskin doit se comporter EXACTEMENT comme l'original : meme chiffre, meme zone d'arrivee",
       [HEROS], [],
       {"degats": [["01094", 3]], "en_main": ["18012"]},
       main_exclusive=["18012", "01090"], jouer=["18012"], cibles=["01094"]),
    _c("reskin", "ua009 Clobber : rejouee dans le meme round, ce n'est plus la premiere carte -> defausse (6 degats)",
       "deuxieme branche du texte : « If this is the first card you have played this round » est FAUX au second jeu",
       [HEROS], [],
       {"degats": [["01094", 6]], "defausse": ["ua009"], "absent_main": ["ua009"]},
       main_exclusive=["ua009", "01090", "01090"], jouer=["ua009", "ua009"], cibles=["01094"]),
    _c("reskin", "ua006 Bo-Wing (reskin de 53035) : porte SES traits (NINJA TURTLE VIGILANTE), pas ceux de Winter Soldier",
       "Paper.Load lit `traits` sur l'entree du reskin ; `ability_link` ne copie QUE les capacites",
       [HEROS, "Puzzle.PutIntoPlay('ua006', under_control=True)"], [],
       {"carte": "ua006", "presents": ["NINJA", "TURTLE", "VIGILANTE"], "absents": ["SOLDIER", "S.H.I.E.L.D"],
        "nom": "Bo-Wing", "unique": True},
       verifier="reskin_identite"),
    _c("reskin", "ua006 Bo-Wing : unicite par SON titre : Winter Soldier 53035 en jeu n'empeche pas de jouer Bo-Wing",
       "`CanCoexistWith` compare les titres : « Bo-Wing » != « Winter Soldier » (question ouverte Q-R1 sur le bandeau "
       "« Winter Soldier » imprime sous le titre : ce cas fige la lecture actuelle)",
       [HEROS, "Puzzle.PutIntoPlay('53035', under_control=True)"], [],
       {"en_jeu": ["53035", "ua006"]},
       main_exclusive=["ua006", "01090", "01088"], jouer=["ua006"]),
    _c("reskin", "ua006 Bo-Wing : un 2e Bo-Wing en main n'est PAS jouable quand le 1er est en jeu (unique)",
       "« * Bo-Wing » est unique : sa propre copie le bloque",
       [HEROS, "Puzzle.Gain('ua006')", "Puzzle.PutIntoPlay('ua006', under_control=True)"], [],
       {"carte": "ua006", "jouable": False, "en_jeu": 1},
       main=["01088", "01089", "01088"], verifier="max_par_joueur_jouable"),
    _c("reskin", "ua006 Bo-Wing : TEMOIN, sans copie en jeu le Bo-Wing en main est jouable",
       "contre-cas du precedent : c'est bien la copie en jeu qui bloque, pas une autre raison",
       [HEROS, "Puzzle.Gain('ua006')"], [],
       {"carte": "ua006", "jouable": True, "en_jeu": 0},
       main=["01088", "01089", "01088"], verifier="max_par_joueur_jouable"),
    _c("reskin", "ua006 Bo-Wing : la Reponse de 53035 part sur Bo-Wing (attaque et tue un sbire -> 2 menaces retirees)",
       "« After Bo-Wing attacks and defeats an enemy, remove 2 threat from a scheme » : sbire a 1 PV restant, ATK 2",
       [HEROS, "Puzzle.PutIntoPlay('ua006', under_control=True)", "Puzzle.Damage(Puzzle.PutIntoPlay('01101'), 2)"],
       ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Attack('ua006')"],
       {"hors_jeu": ["01101"], "menace": [["01097b", 3]]},
       main_exclusive=["01088"], cibles=["01101", "01097b"], accepter_choix=True),
    _c("reskin", "ua006 Bo-Wing : TEMOIN 53035 Winter Soldier, meme montage, meme resultat (2 menaces retirees)",
       "le reskin doit rendre le MEME chiffre que l'original",
       [HEROS, "Puzzle.PutIntoPlay('53035', under_control=True)", "Puzzle.Damage(Puzzle.PutIntoPlay('01101'), 2)"],
       ["Puzzle.SetThreat('01097b', 5)", "Puzzle.Attack('53035')"],
       {"hors_jeu": ["01101"], "menace": [["01097b", 3]]},
       main_exclusive=["01088"], cibles=["01101", "01097b"], accepter_choix=True),
]


VERIFICATIONS = r'''
def reskin_identite(monde, aides):
    """Traits, nom et unicite d'un reskin EN JEU : `attendu` = carte, presents, absents, nom, unique."""
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} n'est pas en jeu"
    soucis = []
    for t in attendu.get("presents", []):
        if not face.HasTrait(t):
            soucis.append(f"trait {t} absent")
    for t in attendu.get("absents", []):
        if face.HasTrait(t):
            soucis.append(f"trait {t} PRESENT (herite de l'original ?)")
    if "nom" in attendu and face.name != attendu["nom"]:
        soucis.append(f"nom {face.name!r} (attendu {attendu['nom']!r})")
    if "unique" in attendu and bool(face.IsUnique()) != attendu["unique"]:
        soucis.append(f"unique={face.IsUnique()} (attendu {attendu['unique']})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{attendu['carte']} : {face.name}, traits propres, unique={face.IsUnique()}"
'''
