# Cas test_capacites de Hawkeye MC×DC 2026 (PU-11, identite alternative pu283a heros / pu283b alter-ego, p283-p284). Prefixe `[hawk]`.
# Deck = celui du Hawkeye OFFICIEL (Arc 04002, Carquois 04003, fleches 04005-04009). Le heros demarre en alter-ego : `Puzzle.ChangeForm('pu283b')` le passe en forme HEROS,
# un second `ChangeForm('pu283a')` le ramene en alter-ego (declenche la Reponse). Temoins officiels : `heros: "hawkeye"` (04001a/b).
HEROS = "hawkeye_mcdc_2026"
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
EN_HEROS = "Puzzle.ChangeForm('pu283b')"
VIDER = ["Puzzle.EmptyPlayerDiscardPile()"]   # la main de depart est defaussee AVANT `declencher` : on vide puis on pose la defausse voulue


def _h(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[hawk] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": HEROS, "mise_en_place": [*RIEN, *mise],
           "declencher": declencher, "verifier": "etat_attendu", "attendu": attendu, "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


CAS = [
    # ------------------------------------------------------------------------------------------------------ pu283a : attaques de base a distance
    _h("pu283a : l'attaque de base de Hawkeye ignore la Riposte (ranged) : Whiplash (Retaliate 1) n'inflige rien", "« Hawkeye's basic attacks gain ranged » : ranged = ignore retaliate",
       [EN_HEROS, "Puzzle.PutIntoPlay('01172')"], ["Puzzle.Attack('pu283a')"], {"degats": [["01172", 1]], "degats_identite": 0}, cibles=["01172"]),
    _h("pu283a, TEMOIN : le Hawkeye OFFICIEL (pas de ranged) prend la Riposte de Whiplash", "la portee vient de pu283a",
       ["Puzzle.ChangeForm('04001b')", "Puzzle.PutIntoPlay('01172')"], ["Puzzle.Attack('04001a')"], {"degats": [["01172", 2]], "degats_identite": 1},
       heros="hawkeye", cibles=["01172"]),
    # ------------------------------------------------------------------------------------------------------ pu283a : Quick Draw
    _h("pu283a Quick Draw : Hawkeye rend l'Arc pret SANS s'incliner", "« Ready Hawkeye's Bow » : pas de cout d'inclinaison (le 04001a officiel s'incline)",
       [EN_HEROS, "Puzzle.PutIntoPlay('04002')", "Puzzle.Exhaust('04002')"], ["Puzzle.Action('pu283a', 'Action')"], {"pret": ["04002", "pu283a"]}),
    _h("pu283a Quick Draw, TEMOIN D'EPUISEMENT : une 2e fois dans la MEME phase ne rend pas l'Arc", "« Limit once per phase » : l'Arc reste incline au second essai",
       [EN_HEROS, "Puzzle.PutIntoPlay('04002')", "Puzzle.Exhaust('04002')"],
       ["Puzzle.Action('pu283a', 'Action')", "Puzzle.Exhaust('04002')"], {"exhausted": ["04002"]}, declencher_tolerant=["Puzzle.Action('pu283a', 'Action')"]),
    # ------------------------------------------------------------------------------------------------------ pu283b : Response
    _h("pu283b Response : en revenant a l'alter-ego, 2 cartes ARROW de la defausse sont melangees dans le deck",
       "« After you change to this form, shuffle 2 ARROW cards from your discard pile into your deck » : 2 sur 3 (choix du joueur)",
       [EN_HEROS], [*VIDER, "Puzzle.CreatePlayerDiscardPile('04005', '04006', '04007')", "Puzzle.ChangeForm('pu283a')"],
       {"defausse_joueur": 1, "defausse": ["04007"]}, cibles=["04005", "04006"]),
    _h("pu283b Response : une SEULE carte ARROW en defausse -> elle est melangee (autant que possible), la non-ARROW reste",
       "RR : un effet se resout autant qu'il le peut ; « ARROW cards » = le trait",
       [EN_HEROS], [*VIDER, "Puzzle.CreatePlayerDiscardPile('04005', '04010')", "Puzzle.ChangeForm('pu283a')"],
       {"defausse_joueur": 1, "defausse": ["04010"]}, cibles=["04005"]),
    _h("pu283b Response, TEMOIN : en passant a la forme HEROS (pas « this form »), rien n'est melange", "« change TO THIS FORM » seulement",
       [], [*VIDER, "Puzzle.CreatePlayerDiscardPile('04005', '04006')", EN_HEROS], {"defausse_joueur": 2}),
    # ------------------------------------------------------------------------------------------------------ pu283b : Action
    _h("pu283b Action : 1 ressource -> l'Arc (cherche dans le deck) entre en jeu", "« find either Hawkeye's Bow or Hawkeye's Quiver and put it into play »",
       [], ["Puzzle.Action('pu283b', 'Action')"], {"en_jeu": ["04002"], "hors_jeu": ["04003"]}, choisir_option="Put_Hawkeye's_Bow_into_play"),
    _h("pu283b Action : au choix, le Carquois entre en jeu (et pas l'Arc)", "« either ... or » : un seul des deux",
       [], ["Puzzle.Action('pu283b', 'Action')"], {"en_jeu": ["04003"], "hors_jeu": ["04002"]}, choisir_option="Put_Hawkeye's_Quiver_into_play"),
    _h("pu283b Action : l'Arc est cherche aussi dans la DEFAUSSE (deck vide)", "« find » = deck et defausse, comme le Weapon of Choice officiel",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDiscardPile('04002')"], ["Puzzle.Action('pu283b', 'Action')"], {"en_jeu": ["04002"]},
       choisir_option="Put_Hawkeye's_Bow_into_play"),
    _h("pu283b Action : l'Arc est deja en jeu -> seul le Carquois est propose et entre en jeu", "cartes uniques : on n'offre que ce qui n'est pas deja la",
       ["Puzzle.PutIntoPlay('04002')"], ["Puzzle.Action('pu283b', 'Action')"], {"en_jeu": ["04002", "04003"]}),
    _h("pu283b Action, TEMOIN D'EPUISEMENT : une 2e fois dans la MEME phase n'apporte rien", "« Limit once per phase » : le Carquois n'entre pas apres l'Arc",
       [], ["Puzzle.Action('pu283b', 'Action')"], {"en_jeu": ["04002"], "hors_jeu": ["04003"]}, main_exclusive=["01088", "01088"],
       choisir_option="Put_Hawkeye's_Bow_into_play", declencher_tolerant=["Puzzle.Action('pu283b', 'Action')"]),
]
