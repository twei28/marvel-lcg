# Cas test_capacites des cartes OFFICIELLES 27018 Across the Spider-Verse et 39049 Cultist (prefixe de nom « [at] ») : « avis suite non
# resolue » du 26/10/2026 (meme principe que Safe House #30, voir docs/reference/RECETTES-MOTEUR.md « Player.NotifyNoResult »).
#  - RR « Then » : si la partie avant « Then » ne se resout pas, la suite non plus ; le joueur doit en etre AVERTI (ligne de journal + bulle
#    `choix_uniques[].texte`) ;
#  - 27018 : « search your discard pile for a Web-Warrior ally and put it into play, THEN choose a player… » : sans allie WEB-WARRIOR en
#    defausse, aucun joueur n'est choisi. Heros Ghost-Spider (27001, WEB-WARRIOR) : son identite paie le « Exhaust a Web-Warrior card » ;
#  - 39049 : « search the encounter deck and discard pile for The Kraken (39050) and put it into play engaged with you. Then, discard Cultist » :
#    sans Kraken, Cultist reste en jeu.
HEROS_27 = "Puzzle.ChangeToFace('27001b', '27001a')"
FILLER = "01098"


def _a27018(nom, pourquoi, mise, attendu, **cle):
    cas = {"nom": "[at] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": "ghost_spider",
           "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098')",
                             HEROS_27, "Puzzle.EmptyPlayerDiscardPile()"] + mise,
           "declencher": [], "verifier": "at_etat", "attendu": attendu,
           "main_exclusive": ["27018", "01090", "01090"], "payer_avec": ["01090", "01090"], "jouer": ["27018"], "accepter_choix": True}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


def _cultist(nom, pourquoi, deck, attendu, **cle):
    cas = {"nom": "[at] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": "spider_man",
           "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(" + ", ".join(f"'{i}'" for i in deck) + ")",
                             "Puzzle.EmptyEncounterDiscardPile()", "Puzzle.PutIntoPlay('39049')"],
           "declencher": ["Puzzle.Activate('39049')"], "verifier": "at_etat", "attendu": attendu, "main_exclusive": ["01090"],
           "accepter_choix": True}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    _a27018("27018 Across the Spider-Verse : AUCUN allie WEB-WARRIOR en defausse -> le joueur est AVERTI (RR « Then »)",
            "« search your discard pile for a Web-Warrior ally … then choose a player » : rien a mettre en jeu, aucun joueur n'est choisi ; decision "
            "de l'utilisateur du 26/10/2026 : le jeu le dit",
            [], {"at_avis": "No Web-Warrior ally in your discard pile: no player is chosen.", "at_hors_jeu": ["27010"]}),
    _a27018("27018 Across the Spider-Verse : TEMOIN, Silk (WEB-WARRIOR) en defausse -> elle entre en jeu, AUCUN avis",
            "contre-cas : l'avis n'existe que lorsque la recherche ne trouve rien",
            ["Puzzle.CreatePlayerDiscardPile('27010')"], {"at_pas_d_avis": True, "at_en_jeu": ["27010"]}),
    _cultist("39049 Cultist : pas de Kraken dans le deck ni la defausse -> Cultist RESTE en jeu et le joueur est AVERTI (RR « Then »)",
             "« search … for The Kraken and put it into play engaged with you. Then, discard Cultist » : sans Kraken, la defausse ne se resout pas",
             [FILLER] * 4,
             {"at_avis": "The Kraken was not found: Cultist is not discarded.", "at_en_jeu": ["39049"], "at_hors_jeu": ["39050"]}),
    _cultist("39049 Cultist : TEMOIN, The Kraken dans le deck -> Kraken en jeu, Cultist defausse, AUCUN avis",
             "contre-cas : l'avis n'existe que lorsque la recherche ne trouve rien",
             [FILLER, FILLER, "39050", FILLER],
             {"at_pas_d_avis": True, "at_en_jeu": ["39050"], "at_hors_jeu": ["39049"]}),
]


VERIFICATIONS = r'''
def at_etat(monde, aides):
    """Cles propres : `at_avis` (texte de l'avis publie), `at_pas_d_avis`, `at_en_jeu` / `at_hors_jeu` (card_id en jeu ou non) ;
    le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    avis = [c.get("texte") for c in getattr(monde.stat, "choix_uniques", []) if c.get("texte")]
    if attendu.get("at_avis") and attendu["at_avis"] not in avis:
        soucis.append(f"l'avis « {attendu['at_avis']} » n'a pas ete publie (avis : {avis})")
    if attendu.get("at_pas_d_avis") and avis:
        soucis.append(f"un avis a ete publie alors que la recherche aboutissait : {avis}")
    for card_id in attendu.get("at_en_jeu") or []:
        if aides["par_id"](monde, card_id) is None:
            soucis.append(f"{card_id} n'est pas en jeu")
    for card_id in attendu.get("at_hors_jeu") or []:
        if aides["par_id"](monde, card_id) is not None:
            soucis.append(f"{card_id} est en jeu alors qu'il ne devrait pas l'etre")
    propres = ("at_avis", "at_pas_d_avis", "at_en_jeu", "at_hors_jeu")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
