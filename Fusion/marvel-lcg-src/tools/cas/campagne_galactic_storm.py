# Cas test_capacites des cartes de campagne de Galactic Storm (gs224-gs236), lot "campagne".
# Noms prefixes `[gsc]` (filtre : `[gsc]`). Gabarit :
# .planning/galactic-storm/CAMPAGNE-ALLIEES-GABARITS.md.
#
# Scenario generique "rhino" (comme binary.py/majestrix.py) : ces alliees ne dependent d'aucun
# scenario particulier. SANS_BOOST neutralise la pioche de boost du mechant (01105 est une carte de
# rencontre inoffensive, meme recette que binary.py) pour rendre les degats de Rhino deterministes
# (ATQ 2, 14 PV).

SC = "rhino"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + list(mise)
    cas = {"nom": "[gsc] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ gs224 Rick Jones
    # Cause trouvee (21/10/2026, TRACE_OPTIONS + journal) : SANS le module, Rhino attaque bien
    # l'identite d'abord, puis le moteur pose normalement « Defense » (regle de base du jeu : tout
    # allie en jeu peut defendre a la place du joueur) — le pilote de test accepte TOUJOURS la
    # premiere option offerte, donc Rick Jones finit quand meme par encaisser, MEME SANS son
    # ability : meme etat final que la redirection, mesurer le resultat net ne suffit pas.
    # ⚠ « questions_absentes": ["Defense"] » etait TROP strict : une fois la cible redirigee sur
    # Rick Jones par `ReplaceTarget`, une question de defense LEGITIME part quand meme (« qui
    # defend RICK JONES ? », reponse normale du jeu, pas un defaut). Ce qui distingue vraiment les
    # deux scenarios : le PROMPT de la toute premiere question d'attaque nomme Peter Parker (SANS
    # le module) ou Rick Jones (AVEC) comme cible — jamais les deux.
    _c("gs224 Rick Jones : Forced Interrupt redirige l'attaque du mechant sur lui AVANT toute resolution "
       "(l'identite n'est jamais la cible annoncee de l'attaque)",
       "« When the villain attacks you, it attacks Rick Jones instead » : ReplaceTarget avant resolution",
       en_jeu("gs224") + ["Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0, "hors_jeu": ["gs224"]}, questions_absentes=["Peter Parker] est attaqué"]),
    # ============================================================ gs226 Lauri-Ell
    # `Puzzle.GiveFacedownBoost` ajoutee le 21/10/2026 (meme famille que
    # `fne/kingpin/60165`) pour monter une pile de boost HORS activation :
    # l'ancien cas (pile vide) ne mesurait que « l'attaque se deroule
    # normalement », vrai avec ou sans le module.
    # ⚠ « hors_jeu » (via `par_id`/`IsInPlay`) ne convient PAS ici : une carte
    # posee FACE CACHEE dans `components.boostable.GetDeck()` est deja
    # `IsInPlay() == False` (face cachee) des l'instant ou elle y est posee,
    # AVANT meme toute attaque — `hors_jeu` restait donc vrai avec ou sans le
    # module (meme piege que gs224, trouve le 21/10/2026). Verifier custom :
    # mesure directement la TAILLE de la pile de boost de la cible apres
    # l'attaque (doit etre vide seulement si la Reponse l'a vraiment videe).
    _c("gs226 Lauri-Ell : apres avoir attaque et blesse un ennemi, sa pile de boost (hors activation) est defaussee",
       "« Response: After Lauri-Ell attacks and damages an enemy, discard each boost card on that enemy »",
       en_jeu("gs226") + ["Puzzle.PutIntoPlay('01101')", "Puzzle.GiveFacedownBoost('01101', '01105')"],
       ["Puzzle.Attack('gs226')"],
       {}, verifier="gsc_gs226_pile_boost_videe"),
    # ============================================================ gs225 Gladiator
    _c("gs225 Gladiator : apres l'avoir joue depuis la main, un sbire est vaincu",
       "« After you play Gladiator from your hand, defeat a minion »",
       ["Puzzle.PutIntoPlay('01101')"], [],
       {"en_jeu": ["gs225"], "hors_jeu": ["01101"]},
       main_exclusive=["gs225", "01088", "01088", "01088", "01088"], payer_avec=["01088", "01088", "01088", "01088"],
       jouer=["gs225"], cibles=["01101"]),
    # ============================================================ gs227 Binary
    _c("gs227 Binary : ATK = X (icones [energy] en main, 2 cartes energie -> ATK 2)",
       "« X is the number of [energy] resource in your hand »",
       en_jeu("gs227"), [],
       {"attributs_carte": [["gs227", "attack", 2]]},
       main_exclusive=["01088", "01088"]),
    _c("gs227 Binary : sans [energy] en main, ATK retombe a 0",
       "contre-cas : aucune icone [energy] -> X = 0",
       en_jeu("gs227"), [],
       {"attributs_carte": [["gs227", "attack", 0]]},
       main_exclusive=["01090", "01090"]),
    # ============================================================ gs228 Captain Marvel
    _c("gs228 Captain Marvel : Resource (la defausser genere YY) paie un allie cout 2 sans autre ressource",
       "« Resource: Discard Captain Marvel -> generate [energy][energy] resources »",
       en_jeu("gs228"), [],
       {"en_jeu": ["01067"], "hors_jeu": ["gs228"]},
       main_exclusive=["01067"], jouer=["01067"]),
    # ============================================================ gs229 Crystal
    _c("gs229 Crystal : When Defeated, payer 3 -> elle revient en jeu sous controle",
       "« When Defeated: Spend 3 resources of any type -> put Crystal into play under your control »",
       en_jeu("gs229"), ["Puzzle.Damage('gs229', 4)"],
       {"en_jeu": ["gs229"]},
       main_exclusive=["01088", "01088", "01088"], accepter_choix=True),
    # ============================================================ gs230 Doctor Pym
    _c("gs230 Doctor Pym : Alter-Ego Action, s'epuiser donne +1 a chaque pouvoir de base jusqu'a la fin du round "
       "(bonus mesure APRES passage en forme Heros : « your identity », pas seulement l'alter ego)",
       "« Exhaust Doctor Pym -> your identity gets +1 to each of its basic powers until the end of the round »",
       en_jeu("gs230"), ["Puzzle.Action('gs230', 'AlterEgoAction')", "Puzzle.ChangeForm('01001b')"],
       {"attributs": {"attack": 1, "thwart": 1, "defense": 1}, "exhausted": ["gs230"]}),
    # ============================================================ gs231 Goliath
    _c("gs231 Goliath : apres un pouvoir de base, defausse 1 ; carte [physical] -> 1 degat a chaque ennemi",
       "« discard the top card of your deck. If a [physical] resource was discarded this way, deal 1 damage to each enemy »",
       en_jeu("gs231") + ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01090')"], ["Puzzle.Attack('gs231')"],
       {"degats": [["01094", 3]]}),
    _c("gs231 Goliath : si la carte defaussee n'est pas [physical], aucun degat de la Reponse (seule l'attaque frappe, 2)",
       "contre-cas : Energy (Y) ne declenche pas le degat supplementaire",
       en_jeu("gs231") + ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088')"], ["Puzzle.Attack('gs231')"],
       {"degats": [["01094", 2]]}),
    # ============================================================ gs232 Her
    _c("gs232 Her : apres son entree en jeu, une amelioration inclinee est redressee",
       "« After Her enters play, ready an upgrade you control »",
       ["Puzzle.PutIntoPlay('01018')", "Puzzle.Exhaust('01018')"],
       ["Puzzle.PutIntoPlay('gs232', under_control=True)"],
       {"pret": ["01018"]}, accepter_choix=True),
    # ============================================================ gs233 Living Lightning
    _c("gs233 Living Lightning : en quittant le jeu, defausse 2, 1 carte [energy] -> 1 carte redressee",
       "« discard the top 2 cards of your deck. For each printed [energy] resource discarded this way, ready a card you control »",
       en_jeu("gs233") + ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01088', '01090')",
                          "Puzzle.PutIntoPlay('01018')", "Puzzle.Exhaust('01018')"],
       ["Puzzle.Discard('gs233')"],
       {"pret": ["01018"]}, accepter_choix=True),
    # ============================================================ gs234 Sersi
    _c("gs234 Sersi : Action, remplace Sonne par Desoriente sur un sbire",
       "« Action: Exhaust Sersi, deal 1 damage to her, and spend a [mental] resource -> choose a status "
       "card in play. Replace that status card with a different status card »",
       en_jeu("gs234") + ["Puzzle.PutIntoPlay('01101')", "Puzzle.Stun('01101')"],
       ["Puzzle.Action('gs234', 'Action')"],
       {"statuts": [["01101", "Confused"]], "statuts_absents": [["01101", "Stunned"]],
        "exhausted": ["gs234"], "degats": [["gs234", 1]]},
       main_exclusive=["01089"], accepter_choix=True, choisir_option=["Confused"]),
    # ============================================================ gs235 Spider-Woman
    _c("gs235 Spider-Woman : defaussee de son deck, etourdit jusqu'a 2 ennemis",
       "« Response: After Spider-Woman is discarded from the top of your deck, stun up to 2 enemies »",
       ["Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01103')",
        "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('gs235')"],
       ["Puzzle.Discard('gs235')"],
       {"statuts": [["01101", "Stunned"], ["01103", "Stunned"]]},
       accepter_choix=True, cibles=["01101", "01103"]),
    # ============================================================ gs236 Thor
    _c("gs236 Thor : apres l'avoir joue depuis la main, 1 degat par [energy] paye a chaque sbire engage",
       "« deal 1 damage to each minion engaged with you for each [energy] resource you used to pay for him »",
       ["Puzzle.PutIntoPlay('01184')"],
       [],
       {"degats": [["01184", 2]]},
       main_exclusive=["gs236", "01088", "01089"],
       payer_avec=["01088", "01089"], jouer=["gs236"]),
]

VERIFICATIONS = r'''
def gsc_gs226_pile_boost_videe(monde, aides):
    cible = aides["par_id"](monde, "01101")
    if cible is None:
        return False, "01101 n'est plus en jeu"
    if cible.max_health - cible.health != 2:
        return False, f"degats sur 01101 = {cible.max_health - cible.health} (attendu 2)"
    attaquante = aides["par_id"](monde, "gs226")
    if attaquante is None:
        return False, "gs226 n'est plus en jeu"
    taille = cible.components.boostable.GetDeck().GetSize()
    if taille != 0:
        return False, f"pile de boost hors activation de 01101 non videe ({taille} carte(s) restante(s))"
    return True, "pile de boost hors activation videe"
'''
