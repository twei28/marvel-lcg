# Cas test_capacites des 9 PISTES (LEAD, pu039-pu047) du scenario 1 « The Big Apple » (pack MC×DC 2026), PU-6/PU-7. Prefixe `[pist]`.
# Ville REELLE (9 lieux en jeu, un par rangee) ; la piste est posee dans l'aire du joueur ; le paquet LEADS est cree avec UNE seule carte (le dessus).
# Verificateur `pist_etat` : cle `victoire` = les pistes dans la pile de victoire ; le reste va a `etat_attendu`.
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
GRILLE_REELLE = [["pu030", "pu031", "pu032"], ["pu033", "pu034", "pu035"], ["pu036", "pu037", "pu038"]]
G = repr(GRILLE_REELLE)
# case de chaque lieu : pu030 (0,0) pu031 (0,1) pu032 (0,2) pu033 (1,0) pu034 (1,1) pu035 (1,2) pu036 (2,0) pu037 (2,1) pu038 (2,2)
CASE = {"pu030": (0, 0), "pu031": (0, 1), "pu032": (0, 2), "pu033": (1, 0), "pu034": (1, 1), "pu035": (1, 2), "pu036": (2, 0), "pu037": (2, 1), "pu038": (2, 2)}


def ville(lieu, communs=("pu005", "pu006")):
    return [*["Puzzle.PutIntoPlay('%s')" % x for x in communs],
            "Puzzle.InstallerVille(%s, %s, en_jeu=True)" % (G, repr(CASE[lieu])),
            *["Puzzle.MoveCardToGameArea('%s', 1)" % x for x in communs]]


def _p(nom, pourquoi, lieu, piste, avant, declencher, attendu, suivante="pu040", deck=None, **cle):
    # Ce qui touche la piste ou la zone commune (compteurs, menace, zone) vient APRES la ville et la piste ; le reste (sbires, degats) avant.
    apres = [x for x in avant if x.startswith(("Puzzle.PlaceCounters", "Puzzle.MoveCardToGameArea", "Puzzle.SetThreat"))]
    avant = [x for x in avant if x not in apres]
    cas = {"nom": "[pist] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": "spider_man",
           "mise_en_place": [*(RIEN if deck is None else ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join(repr(x) for x in deck)]), FORME_HEROS, *avant, *ville(lieu), "Puzzle.PutIntoPlay('%s', under_control=True)" % piste,
                             "Puzzle.CreateLeadsDeck('%s')" % suivante, *apres],
           "declencher": declencher, "verifier": "pist_etat", "attendu": attendu, "main_exclusive": ["01088"]}
    cas.update(cle)
    return cas


def _fin(piste, compteur, seuil, **plus):
    """attendu d'une piste TERMINEE : plus de compteur ici, en victoire, la suivante revelee, 1 carte piochee (main 1 + 1)."""
    d = {"victoire": [piste], "en_jeu": ["pu040"], "taille_main": 2}
    d.update(plus)
    return d


CAS = [
    # ------------------------------------------------------------------ pu039 Bar Fight at Josie's (Hell's Kitchen, 3 bouncer)
    _p("pu039 piste : un SBIRE est vaincu a Hell's Kitchen -> 1 compteur bouncer", "Response ; « a minion »", "pu030", "pu039",
       ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Damage('01103', 3)"], {"compteurs": [["pu039", "bouncer", 1]], "victoire": []}),
    _p("pu039 piste : un ALLIE que je controle est vaincu a Hell's Kitchen -> 1 compteur bouncer", "Response ; « or ally you control »", "pu030", "pu039",
       ["Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Damage('01075', 2)"], {"compteurs": [["pu039", "bouncer", 1]]}),
    _p("pu039 piste, TEMOIN : meme sbire vaincu a Theater District (MEME rangee, pas au lieu) -> aucun compteur", "« While in Hell's Kitchen »", "pu031", "pu039",
       ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Damage('01103', 3)"], {"compteurs": [["pu039", "bouncer", 0]]}),
    _p("pu039 piste, FIN : 2 compteurs + 1 sbire vaincu = 3 -> en victoire, piste suivante (pu040) revelee, 1 carte piochee", "seuil 3 : « add this card to the victory display, reveal the top LEAD card, and draw 1 card »",
       "pu030", "pu039", ["Puzzle.PutIntoPlay('01103')", "Puzzle.PlaceCounters('pu039', 'bouncer', 2)"], ["Puzzle.Damage('01103', 3)"], _fin("pu039", "bouncer", 3)),
    _p("pu039 piste, TEMOIN de seuil : 1 compteur + 1 sbire vaincu = 2 -> pas terminee", "le seuil mord (3)", "pu030", "pu039",
       ["Puzzle.PutIntoPlay('01103')", "Puzzle.PlaceCounters('pu039', 'bouncer', 1)"], ["Puzzle.Damage('01103', 3)"],
       {"compteurs": [["pu039", "bouncer", 2]], "victoire": [], "taille_main": 1}),
    # ------------------------------------------------------------------ pu040 Art Heals the Soul (Theater District, 3 culture)
    _p("pu040 piste : l'identite est soignee a Theater District -> 1 compteur culture", "Response ; « you heal a friendly character »", "pu031", "pu040",
       ["Puzzle.Damage('01001a', 4)"], ["Puzzle.Heal('01001a', 2)"], {"compteurs": [["pu040", "culture", 1]], "victoire": []}, suivante="pu041"),
    _p("pu040 piste, TEMOIN : soin a Hell's Kitchen (meme rangee) -> aucun compteur", "« While in The Theater District »", "pu030", "pu040",
       ["Puzzle.Damage('01001a', 4)"], ["Puzzle.Heal('01001a', 2)"], {"compteurs": [["pu040", "culture", 0]]}, suivante="pu041"),
    _p("pu040 piste, FIN : 2 compteurs + 1 soin = 3 -> victoire, suivante (pu041) revelee, 1 carte", "seuil 3", "pu031", "pu040",
       ["Puzzle.Damage('01001a', 4)", "Puzzle.PlaceCounters('pu040', 'culture', 2)"], ["Puzzle.Heal('01001a', 2)"],
       {"victoire": ["pu040"], "en_jeu": ["pu041"], "taille_main": 2}, suivante="pu041"),
    # ------------------------------------------------------------------ pu041 A Walk in the Park (Upper East Side)
    _p("pu041 piste : une manigance annexe est vaincue a Upper East Side -> piste terminee tout de suite (victoire, suivante, 1 carte)",
       "Response ; pas de compteur", "pu032", "pu041",
       ["Puzzle.PutIntoPlay('01107')", "Puzzle.MoveCardToGameArea('01107', 1)", "Puzzle.SetThreat('01107', 1)"], ["Puzzle.Thwart('01001a')"],
       {"victoire": ["pu041"], "en_jeu": ["pu040"], "taille_main": 2}),
    _p("pu041 piste, TEMOIN : un ALLIE vainc la manigance annexe a Upper East Side -> pas terminee (« you » = l'identite, decision du 23/10/2026)",
       "Response ; « after you defeat a side scheme » : l'identite seulement", "pu032", "pu041",
       ["Puzzle.PutIntoPlay('01107')", "Puzzle.MoveCardToGameArea('01107', 1)", "Puzzle.SetThreat('01107', 1)", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01075')"],
       {"victoire": [], "taille_main": 1, "hors_jeu": ["01107"]}),
    _p("pu041 piste, TEMOIN : meme manigance vaincue a Hell's Kitchen -> pas terminee", "« While in Upper East Side »", "pu030", "pu041",
       ["Puzzle.PutIntoPlay('01107')", "Puzzle.MoveCardToGameArea('01107', 1)", "Puzzle.SetThreat('01107', 1)"], ["Puzzle.Thwart('01001a')"],
       {"victoire": [], "taille_main": 1}),
    # ------------------------------------------------------------------ pu042 Village of the Damned (West Village, 4 curse)
    _p("pu042 piste : une carte de rencontre est revelee a West Village -> 1 compteur curse", "Response ; « after you reveal an encounter card »",
       "pu033", "pu042", [], ["Puzzle.Reveal('01105')"], {"compteurs": [["pu042", "curse", 1]], "victoire": []}),
    _p("pu042 piste, TEMOIN : revelation a Midtown (meme rangee) -> aucun compteur", "« While in West Village »", "pu034", "pu042",
       [], ["Puzzle.Reveal('01105')"], {"compteurs": [["pu042", "curse", 0]]}),
    _p("pu042 piste, SEUIL 4 : 3 compteurs + 1 revelation = 4 -> victoire", "seuil 4 (pas 3)", "pu033", "pu042",
       ["Puzzle.PlaceCounters('pu042', 'curse', 3)"], ["Puzzle.Reveal('01105')"], {"victoire": ["pu042"], "en_jeu": ["pu040"], "taille_main": 2}),
    _p("pu042 piste, TEMOIN de seuil : 2 compteurs + 1 revelation = 3 -> PAS terminee (le seuil est 4)", "le seuil 4 mord", "pu033", "pu042",
       ["Puzzle.PlaceCounters('pu042', 'curse', 2)"], ["Puzzle.Reveal('01105')"], {"compteurs": [["pu042", "curse", 3]], "victoire": [], "taille_main": 1}),
    # ------------------------------------------------------------------ pu043 Midtown Memories (Midtown, 3 cartes glissees)
    _p("pu043 piste : une manigance est contree a Midtown -> le joueur glisse une des 2 cartes du dessus du deck rencontre sous la piste",
       "Response ; « look at the top two cards ... Tuck one of them here »", "pu034", "pu043",
       ["Puzzle.PutIntoPlay('01107')", "Puzzle.MoveCardToGameArea('01107', 1)", "Puzzle.SetThreat('01107', 3)"], ["Puzzle.Thwart('01001a')"],
       {"taille_pose_sous": [["pu043", 1]], "victoire": []}, deck=("01105", "01101", "01103")),
    _p("pu043 piste, TEMOIN : meme contre a Soho... (meme rangee ? non : Hell's Kitchen) -> rien de glisse", "« While in Midtown »", "pu033", "pu043",
       ["Puzzle.PutIntoPlay('01107')", "Puzzle.MoveCardToGameArea('01107', 1)", "Puzzle.SetThreat('01107', 3)"], ["Puzzle.Thwart('01001a')"],
       {"taille_pose_sous": [["pu043", 0]]}, deck=("01105", "01101", "01103")),
    # ------------------------------------------------------------------ pu044 Kings of Yancy Street (Lower East Side, 8 degats)
    _p("pu044 piste : le joueur attaque le vilain a Lower East Side (ATQ 2) -> les 2 degats vont sur la piste, le vilain n'en subit AUCUN",
       "Interrupt ; « place that attack's damage here instead »", "pu035", "pu044", ["Puzzle.PutIntoPlay('pu055a')", "Puzzle.MoveCardToGameArea('pu055a', 3)"],
       ["Puzzle.Attack('01001a')"], {"jetons": [["pu044", "damage", 2]], "degats": [["pu055a", 0]], "victoire": []}, cibles=["pu055a"]),
    _p("pu044 piste, TEMOIN : meme attaque a Midtown (meme rangee) -> le vilain subit 2 degats, la piste n'a rien", "« While in Lower East Side »",
       "pu034", "pu044", ["Puzzle.PutIntoPlay('pu055a')", "Puzzle.MoveCardToGameArea('pu055a', 3)"], ["Puzzle.Attack('01001a')"],
       {"jetons": [["pu044", "damage", 0]], "degats": [["pu055a", 2]]}, cibles=["pu055a"]),
    _p("pu044 piste, FIN : 6 degats + 2 = 8 -> victoire, suivante revelee, 1 carte", "seuil 8 degats", "pu035", "pu044",
       ["Puzzle.PutIntoPlay('pu055a')", "Puzzle.MoveCardToGameArea('pu055a', 3)", "Puzzle.Token('pu044', 'damage', 6)"], ["Puzzle.Attack('01001a')"],
       {"victoire": ["pu044"], "en_jeu": ["pu040"], "taille_main": 2, "degats": [["pu055a", 0]]}, cibles=["pu055a"]),
    # ------------------------------------------------------------------ pu045 "Where's My Rent!?" (Soho, 3 rent)
    _p("pu045 piste : un evenement (Haymaker, 3 en Soho) est joue a Soho -> 1 compteur rent", "Response ; « after you play an event »", "pu036", "pu045",
       ["Puzzle.PutIntoPlay('01130')"], [], {"compteurs": [["pu045", "rent", 1]], "victoire": []},
       main_exclusive=["01087", "01089", "01088"], jouer=["01087"], cibles=["01130"]),
    _p("pu045 piste, TEMOIN : meme evenement joue a Financial District (meme rangee) -> aucun compteur", "« While in Soho »", "pu037", "pu045",
       ["Puzzle.PutIntoPlay('01130')"], [], {"compteurs": [["pu045", "rent", 0]]},
       main_exclusive=["01087", "01089", "01088"], jouer=["01087"], cibles=["01130"]),
    # ------------------------------------------------------------------ pu046 Play the Market (Financial District, 3 stock)
    _p("pu046 piste : un allie defend a Financial District -> 1 compteur stock", "Response ; « after you defend an attack »", "pu037", "pu046",
       ["Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('01075', under_control=True)"],
       ["Puzzle.EnemyAttacks('01103', '01001a', defender='01001a')"], {"compteurs": [["pu046", "stock", 1]], "victoire": []}),
    _p("pu046 piste, TEMOIN : meme defense a Soho (meme rangee) -> aucun compteur", "« While in the Financial District »", "pu036", "pu046",
       ["Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('01075', under_control=True)"],
       ["Puzzle.EnemyAttacks('01103', '01001a', defender='01001a')"], {"compteurs": [["pu046", "stock", 0]]}),
    # ------------------------------------------------------------------ pu047 Forget It... It's Chinatown (Chinatown, 2 takeout)
    _p("pu047 piste : le joueur vainc un sbire a Chinatown -> 1 compteur takeout", "Response ; « after you defeat a minion »", "pu038", "pu047",
       ["Puzzle.PutIntoPlay('01103')", "Puzzle.Damage('01103', 2)"], ["Puzzle.Attack('01001a')"], {"compteurs": [["pu047", "takeout", 1]], "victoire": [], "hors_jeu": ["01103"]}, cibles=["01103"]),
    _p("pu047 piste, FIN : 1 compteur + 1 sbire vaincu = 2 -> victoire (seuil 2, pas 3)", "seuil 2", "pu038", "pu047",
       ["Puzzle.PutIntoPlay('01103')", "Puzzle.Damage('01103', 2)", "Puzzle.PlaceCounters('pu047', 'takeout', 1)"], ["Puzzle.Attack('01001a')"],
       {"victoire": ["pu047"], "en_jeu": ["pu040"], "taille_main": 2}, cibles=["01103"]),
    _p("pu047 piste, TEMOIN : un ALLIE vainc le sbire a Chinatown -> aucun compteur (« you » = l'identite, decision du 23/10/2026)", "« after you defeat a minion » : l'identite seulement", "pu038", "pu047",
       ["Puzzle.PutIntoPlay('01103')", "Puzzle.Damage('01103', 2)", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Attack('01075')"],
       {"compteurs": [["pu047", "takeout", 0]], "victoire": [], "hors_jeu": ["01103"]}, cibles=["01103"]),
    _p("pu047 piste, TEMOIN : meme sbire vaincu a Soho (meme rangee) -> aucun compteur", "« While in Chinatown »", "pu036", "pu047",
       ["Puzzle.PutIntoPlay('01103')", "Puzzle.Damage('01103', 2)"], ["Puzzle.Attack('01001a')"], {"compteurs": [["pu047", "takeout", 0]]}, cibles=["01103"]),
    _p("pu043 piste, FIN : 2 cartes deja glissees + 1 = 3 -> victoire, suivante revelee, 1 carte", "seuil 3 cartes glissees", "pu034", "pu043",
       ["Puzzle.PutIntoPlay('01107')", "Puzzle.MoveCardToGameArea('01107', 1)", "Puzzle.SetThreat('01107', 3)"],
       ["Puzzle.PlaceUnder('01105', 'pu043')", "Puzzle.PlaceUnder('01101', 'pu043')", "Puzzle.Thwart('01001a')"],
       {"victoire": ["pu043"], "en_jeu": ["pu040"], "taille_main": 2}, deck=("01105", "01101", "01103")),
    _p("pu045 piste, FIN : 2 compteurs + 1 evenement = 3 -> victoire", "seuil 3", "pu036", "pu045",
       ["Puzzle.PutIntoPlay('01130')", "Puzzle.PlaceCounters('pu045', 'rent', 2)"], [], {"victoire": ["pu045"], "en_jeu": ["pu040"]},
       main_exclusive=["01087", "01089", "01088"], jouer=["01087"], cibles=["01130"]),
    _p("pu046 piste, FIN : 2 compteurs + 1 defense = 3 -> victoire, suivante, 1 carte", "seuil 3", "pu037", "pu046",
       ["Puzzle.PutIntoPlay('01103')", "Puzzle.PlaceCounters('pu046', 'stock', 2)"],
       ["Puzzle.EnemyAttacks('01103', '01001a', defender='01001a')"], {"victoire": ["pu046"], "en_jeu": ["pu040"], "taille_main": 2}),
]

VERIFICATIONS = r'''
def pist_etat(monde, aides):
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    if "victoire" in attendu:
        ids = sorted(getattr(f.paper, "card_id", None) for f in monde.victory_display.Get(True) if str(getattr(f.paper, "card_id", "")).startswith("pu0"))
        if ids != sorted(attendu["victoire"]):
            soucis.append(f"pile de victoire = {ids} (attendu {sorted(attendu['victoire'])})")
    reste = {k: v for k, v in attendu.items() if k != "victoire"}
    if reste:
        cas["attendu"] = reste
        try:
            ok, msg = etat_attendu(monde, aides)
        finally:
            cas["attendu"] = attendu
        if not ok:
            soucis.append(msg)
    return (False, " ; ".join(soucis)) if soucis else (True, "piste conforme")
'''
