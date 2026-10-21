# Cas test_capacites du set CAPOS (pack MC×DC 2026 « La ville ne dort jamais », scenario 1 « The Big Apple »), PU-7. Prefixe `[capo]`.
# Montage : scenario `rhino` (Rhino reste le vilain actif), le CAPO est mis en jeu a cote (`Puzzle.PutIntoPlay`), Spider-Man en HEROS.
# Le deck rencontre est REMPLACE par des 01105 (« I'm Tough », 0 icone de boost) : la DERNIERE carte donnee est le DESSUS.
# Le CAPO attaque directement le heros (`Puzzle.EnemyAttacks`, brique commune), sans defense. Le complot principal du montage est 01097b.
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DEFENSE = {"passer_sur_option": "Defense"}
MENACE0 = "Puzzle.SetThreat('01097b', 0)"
BW = "01075"       # Black Widow : allie, 2 PV
USAGI = "up041"    # Usagi Yojimbo : allie, 3 PV, Retaliate 2, Toughness


def _k(nom, pourquoi, capo, attendu, mise=(), deck=("01105", "01105", "01105"), declencher=None, cible="01001a", defense=True, **cle):
    cas = {"nom": "[capo] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": "spider_man",
           "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join(repr(x) for x in deck),
                             HEROS, "Puzzle.PutIntoPlay('%s')" % capo, *mise],
           "declencher": declencher or ["Puzzle.EnemyAttacks('%s', '%s')" % (capo, cible)],
           "verifier": "etat_attendu", "attendu": attendu, "main_exclusive": ["01088"]}
    if defense:
        cas.update(SANS_DEFENSE)
    cas.update(cle)
    return cas


def _minions(n):
    return ["Puzzle.PutIntoPlay('%s')" % x for x in ("01101", "01110", "01120")[:n]]


CAS = [
    # ------------------------------------------------------------------------------------------------ pu048 Count Nefaria
    _k("pu048a Nefaria : attaque OVERKILL sur Black Widow (1 PV restant) -> l'exces (1) va au heros",
       "« ★ Count Nefaria's attacks gain overkill » : ATQ 2 sur 1 PV, exces 1 sur l'identite",
       "pu048a", {"degats_identite": 1, "hors_jeu": [BW]},
       mise=["Puzzle.PutIntoPlay('%s', under_control=True)" % BW, "Puzzle.Damage('%s', 1)" % BW], cible=BW),
    _k("pu055a TEMOIN d'overkill : Diamondback (sans overkill, meme ATQ 2) abat Black Widow -> aucun exces sur le heros",
       "temoin : sans le mot-cle, l'exces est perdu", "pu055a", {"degats_identite": 0, "hors_jeu": [BW]},
       mise=["Puzzle.PutIntoPlay('%s', under_control=True)" % BW, "Puzzle.Damage('%s', 1)" % BW], cible=BW),
    _k("pu048a Nefaria : attaque RANGED sur Usagi (Retaliate 2) -> Nefaria ne subit aucune riposte",
       "« ★ Count Nefaria's attacks gain ... ranged » : ranged ignore la riposte",
       "pu048a", {"degats": [["pu048a", 0]]},
       mise=["Puzzle.PutIntoPlay('%s', under_control=True)" % USAGI], cible=USAGI),
    _k("pu055a TEMOIN de ranged : Diamondback attaque Usagi (Retaliate 2) -> il subit 2 de riposte",
       "temoin : sans ranged, la riposte s'applique", "pu055a", {"degats": [["pu055a", 2]]},
       mise=["Puzzle.PutIntoPlay('%s', under_control=True)" % USAGI], cible=USAGI),
    _k("pu048b Nefaria (expert) : ATQ 3 overkill sur Black Widow (1 PV restant) -> exces 2 sur le heros",
       "face B : ATQ 3★, meme texte", "pu048b", {"degats_identite": 2, "hors_jeu": [BW]},
       mise=["Puzzle.PutIntoPlay('%s', under_control=True)" % BW, "Puzzle.Damage('%s', 1)" % BW], cible=BW),
    # ------------------------------------------------------------------------------------------------ pu049 Crime-Master
    _k("pu049a Crime-Master : aucun sbire engage -> ATQ 1 : 1 degat", "« +1 ATK for each minion engaged with you » : base", "pu049a",
       {"degats_identite": 1}),
    _k("pu049a Crime-Master : 2 sbires engages -> ATQ 1+2 = 3 degats", "+1 par sbire", "pu049a", {"degats_identite": 3}, mise=_minions(2)),
    _k("pu049a Crime-Master : 3 sbires engages -> PLAFOND +2 : 3 degats (pas 4)", "« to a maximum of +2 ATK »", "pu049a",
       {"degats_identite": 3}, mise=_minions(3)),
    _k("pu049b Crime-Master (expert) : 1 sbire engage -> ATQ 2+1 = 3 degats", "face B : ATQ 2★", "pu049b", {"degats_identite": 3}, mise=_minions(1)),
    # ------------------------------------------------------------------------------------------------ pu050 Ringmaster
    _k("pu050a Ringmaster : choix « depenser une ressource mentale » (main = Genius BB) -> la carte est defaussee, le heros n'est PAS confus",
       "Forced Response apres l'attaque ; branche 1 = Spend [mental]", "pu050a",
       {"defausse": ["01089"], "statuts_absents": [["01001a", "Confused"]], "degats_identite": 1},
       main_exclusive=["01089"], payer_avec=["01089"]),
    _k("pu050a Ringmaster : choix « confondre un personnage que vous controlez » -> l'identite est Confuse, la main intacte",
       "branche 2", "pu050a", {"statuts": [["01001a", "Confused"]], "en_main": ["01089"], "degats_identite": 1},
       main_exclusive=["01089"], preferer_option="Confuse"),
    _k("pu050a Ringmaster : AUCUNE ressource mentale en main (Energy YY) -> la branche payante n'est pas offerte, le heros est confus",
       "la branche payante est offerte seulement si payable (PeutCouvrirLeCout)", "pu050a",
       {"statuts": [["01001a", "Confused"]], "en_main": ["01088"], "degats_identite": 1}, mise=["Puzzle.CreatePlayerDeck(%s)" % ", ".join(["'01088'"] * 10)]),
    _k("pu050b Ringmaster (expert) : ATQ 1, SCH 3 : meme choix (confus)", "face B", "pu050b",
       {"statuts": [["01001a", "Confused"]], "degats_identite": 1}, mise=["Puzzle.CreatePlayerDeck(%s)" % ", ".join(["'01088'"] * 10)]),
    # ------------------------------------------------------------------------------------------------ pu051 Lady Yulan
    _k("pu051a Lady Yulan : choix « soigner 2 degats d'elle » (5 -> 3)", "Forced Response ; branche 1", "pu051a",
       {"degats": [["pu051a", 3]], "degats_identite": 2, "taille_deck_joueur": 32}, mise=["Puzzle.Damage('pu051a', 5)"]),
    _k("pu051a Lady Yulan : choix « defausser les 6 premieres cartes de votre deck » -> deck 32 -> 26 ; elle n'est pas soignee",
       "branche 2", "pu051a", {"degats": [["pu051a", 5]], "degats_identite": 2, "taille_deck_joueur": 26}, mise=["Puzzle.Damage('pu051a', 5)"],
       preferer_option="Discard the top 6"),
    _k("pu051b Lady Yulan (expert) : soigne 3 (6 -> 3)", "face B : 3", "pu051b",
       {"degats": [["pu051b", 3]], "degats_identite": 3}, mise=["Puzzle.Damage('pu051b', 6)"]),
    # ------------------------------------------------------------------------------------------------ pu052 Mister Negative
    _k("pu052a Mister Negative : choix « 1 carte de boost de plus » -> DEUX cartes du deck rencontre defaussees (Shocker, 2 icones de boost : 1+2 = 3 degats)",
       "Forced Interrupt ; branche 1", "pu052a", {"defausse_rencontre": ["01105", "01103"], "degats_identite": 3},
       deck=("01103", "01105")),
    _k("pu052a Mister Negative : choix « etourdir apres l'attaque » -> UNE seule carte defaussee, l'identite est Etourdie apres",
       "branche 2 ; le heros n'est etourdi QU'APRES l'attaque", "pu052a",
       {"defausse_rencontre": ["01105"], "dans_deck_rencontre": ["01103"], "statuts": [["01001a", "Stunned"]], "degats_identite": 1},
       deck=("01103", "01105"), preferer_option="stun"),
    _k("pu052b Mister Negative (expert) : branche 1 -> 2 cartes defaussees ET overkill (Black Widow 1 PV : ATQ 2 + 2 icones du boost de plus = 4, exces 3 sur le heros)",
       "face B : « This attack gains overkill »", "pu052b", {"defausse_rencontre": ["01105", "01103"], "degats_identite": 3, "hors_jeu": [BW]}, deck=("01103", "01105"),
       mise=["Puzzle.PutIntoPlay('%s', under_control=True)" % BW, "Puzzle.Damage('%s', 1)" % BW], cible=BW),
    _k("pu052a TEMOIN : face A, meme montage -> PAS d'overkill (exces perdu)", "la face A ne donne pas overkill", "pu052a",
       {"degats_identite": 0, "hors_jeu": [BW]},
       mise=["Puzzle.PutIntoPlay('%s', under_control=True)" % BW, "Puzzle.Damage('%s', 1)" % BW], cible=BW),
    # ------------------------------------------------------------------------------------------------ pu053 The Rose
    _k("pu053a The Rose : choix « 2 menaces sur le complot principal » -> menace 2, degats 1", "Forced Interrupt ; branche 1", "pu053a",
       {"menace": [["01097b", 2]], "degats_identite": 1}, mise=[MENACE0]),
    _k("pu053a The Rose : choix « +2 ATQ pour cette attaque » -> 3 degats, aucune menace", "branche 2", "pu053a",
       {"menace": [["01097b", 0]], "degats_identite": 3}, mise=[MENACE0], preferer_option="gets +2 ATK"),
    _k("pu053b The Rose (expert) : ATQ 2, +2 = 4 degats", "face B", "pu053b", {"degats_identite": 4}, mise=[MENACE0], preferer_option="gets +2 ATK"),
    # ------------------------------------------------------------------------------------------------ pu054 Nightshade
    _k("pu054a Nightshade : aucun allie -> 1 degat (l'attaque) seulement", "« 1 indirect damage for each ally you control » : base", "pu054a",
       {"degats_identite": 1}),
    _k("pu054a Nightshade : 1 allie (Black Widow) -> 1 attaque + 1 indirect = 2 degats repartis", "+1 indirect par allie", "pu054a",
       {"degats_identite": 2}, mise=["Puzzle.PutIntoPlay('%s', under_control=True)" % BW]),
    _k("pu054a Nightshade : 2 allies -> 1 attaque + 2 indirects = 3 degats", "un indirect par allie", "pu054a", {"degats_identite": 3},
       mise=["Puzzle.PutIntoPlay('%s', under_control=True)" % BW, "Puzzle.PutIntoPlay('%s', under_control=True)" % USAGI]),
    _k("pu054b Nightshade (expert) : ATQ 2 + 1 allie = 3 degats", "face B", "pu054b", {"degats_identite": 3},
       mise=["Puzzle.PutIntoPlay('%s', under_control=True)" % BW]),
    # ------------------------------------------------------------------------------------------------ pu055 Diamondback
    _k("pu055a Diamondback : subit 3 degats d'une attaque (Nefaria expert ATQ 3) -> UNE carte de boost face cachee", "Forced Response ; seuil 3",
       "pu055a", {"boosts_sur": [["pu055a", 1]]}, mise=["Puzzle.PutIntoPlay('pu048b')"],
       declencher=["Puzzle.EnemyAttacks('pu048b', 'pu055a')"], defense=False),
    _k("pu055a Diamondback : subit 2 degats seulement (Nefaria standard ATQ 2) -> AUCUNE carte de boost", "le seuil mord : 2 < 3", "pu055a",
       {"boosts_sur": [["pu055a", 0]]}, mise=["Puzzle.PutIntoPlay('pu048a')"], declencher=["Puzzle.EnemyAttacks('pu048a', 'pu055a')"], defense=False),
    _k("pu055b Diamondback (expert) : 3 degats -> UNE carte de boost face cachee", "face B", "pu055b", {"boosts_sur": [["pu055b", 1]]},
       mise=["Puzzle.PutIntoPlay('pu048b')"], declencher=["Puzzle.EnemyAttacks('pu048b', 'pu055b')"], defense=False),
]
