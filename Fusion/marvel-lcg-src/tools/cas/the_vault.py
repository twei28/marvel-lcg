# Cas test_capacites du scenario custom THE VAULT (Kajislav, prefixe `vt`) : noms prefixes « [vt] » puis le card_id (substituer_pack.py
# filtre dessus). 1er fichier : le SOCLE (mise en place, complot principal, environnement, Inspection, fin de partie, activation).
#
# Rappels de montage :
#  - scenario `the_vault` (standard : vilains I) ou `the_vault_expert` (II) = la VRAIE mise en place (vt017a) ; le vilain revele et les 4
#    vilains glisses sous le Vault sont TIRES AU HASARD : ces cas ne mesurent que des quantites independantes de l'identite ;
#  - scenario `rhino` = position DETERMINISTE montee a la main : on retire le Rhino, on pose vt017b + vt018, la regle des vilains
#    (`Puzzle.SetVillainRule('LowestActivationOrder', 'PlayerChooses', True)`), le deck de vilains (`BuildVillainDeck`) et ce qu'on veut
#    sous le Vault (`PlaceUnder`) ;
#  - heros `spider_man` (01001a/b) ; la partie commence en ALTER-EGO ; `HEROS` passe en forme heros ;
#  - `SANS_BOOST` remplace le deck de rencontre par des cartes sans icone boost (sinon le boost d'une attaque change les degats) ;
#  - 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ; 01005 est une SIGNATURE de Spider-Man.
SC = "the_vault"
SCX = "the_vault_expert"
HEROS = "Puzzle.ChangeToFace('01001b', '01001a')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
DECK_BASIQUE = "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089', '01089')"

# Position deterministe : le Vault et le complot 1B en jeu, la regle des vilains posee, aucun vilain (on les ajoute).
SOCLE = [
    "Puzzle.RemoveVillain('01094')",
    "Puzzle.Remove('01097b')",            # le complot du Rhino : « the main scheme » doit etre vt017b, le SEUL complot principal
    "Puzzle.PutIntoPlay('vt017b')",
    "Puzzle.SetThreat('vt017b', 0)",      # PutIntoPlay lui laisse sa menace de depart (1) : on mesure des DIFFERENCES
    "Puzzle.PutIntoPlay('vt018')",
    "Puzzle.SetVillainRule('LowestActivationOrder', 'PlayerChooses', True)",
]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def mechants_en_jeu(*ids):
    """Met de VRAIS vilains en jeu (zone des vilains) : le deck de vilains les revele un a un (`PutIntoPlay` ne les y met pas)."""
    out = []
    for i in ids:
        out += [f"Puzzle.BuildVillainDeck('{i}')", "Puzzle.RevealNextVillain()"]
    return out


def sous_le_vault(*ids):
    return [f"Puzzle.PlaceUnder('{i}', 'vt018')" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    scenario = cle.pop("scenario", "rhino")
    if scenario == "rhino" and not cle.pop("sans_socle", False):
        mise = SOCLE + list(mise)
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[vt] " + nom, "pourquoi": pourquoi, "scenario": scenario,
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "vt_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ vt017a : mise en place REELLE
    _c("vt017a Setup (standard) : The Vault en jeu, 4 vilains SOUS le Vault, 1 vilain revele (1B), 3 dans le deck de vilains, Inspection de cote",
       "« Create the Villain deck. Put The Vault environment into play. Then, place the top 4 villain cards ... beneath it facedown. Set the Inspection "
       "of the Vault obligation aside » + 1B « Reveal the top card of the villain deck »",
       [], [],
       {"vault_en_jeu": True, "sous_vault_mechants": 4, "tous": 1, "deck_de_mechants": 3, "inspection_en_jeu": False, "fin": None},
       scenario=SC, sans_socle=True, avec_boost=True),
    # ============================================================ vt017b : 1B, accomplie -> a la place
    _c("vt017b When Revealed : le dessus du deck de vilains est REVELE (1 en jeu, 1 reste au deck)",
       "« When Revealed: Reveal the top card of the villain deck »",
       ["Puzzle.BuildVillainDeck('vt001', 'vt003')"], ["Puzzle.Reveal('vt017b')"],
       {"tous": 1, "deck_de_mechants": 1}),
    _c("vt017b Interruption forcee (VRAIE mise en place) : menace accomplie -> la menace tombe a 1[per_hero], 1 vilain sous le Vault est REVELE, l'Inspection est donnee",
       "« When this scheme would be completed, instead do each of the following: 1. Remove all but 1 threat 2. Reveal 1 random villain beneath The Vault 3. Reveal Inspection »",
       [], ["Puzzle.SetThreat('vt017b', 6)"],
       {"menace": [["vt017b", 1]], "sous_vault_mechants": 3, "tous": 2, "inspection_en_jeu": True, "fin": None},
       scenario=SC, sans_socle=True, avec_boost=True),

    # ============================================================ vt018 The Vault : sbires uniques, fin de partie
    _c("vt018 un SBIRE UNIQUE vaincu (Shocker) est glisse sous le Vault",
       "« After a unique minion (✦) is defeated, place it beneath The Vault facedown »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003") + ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Damage('01103', 3)"],
       {"sous_vault": ["vt003", "01103"], "sous_vault_sbires": 1, "defausse_rencontre": []}),
    _c("vt018 contre-cas : un sbire NON unique vaincu (Hydra Mercenary) n'est PAS glisse sous le Vault",
       "« unique minion » seulement",
       mechants_en_jeu("vt001") + sous_le_vault("vt003") + ["Puzzle.PutIntoPlay('01101')"], ["Puzzle.Damage('01101', 3)"],
       {"sous_vault": ["vt003"], "sous_vault_sbires": 0}),
    _c("vt018 aucun vilain sous le Vault apres qu'un sbire unique y est glisse : les joueurs PERDENT",
       "« If no villain is beneath The Vault, the players lose the game »",
       mechants_en_jeu("vt001") + ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Damage('01103', 3)"],
       {"fin": "perdu"}),
    _c("vt018 dernier vilain vaincu, deck de vilains vide, 1 vilain sous le Vault : les joueurs GAGNENT",
       "« If all the villains are either beneath The Vault or defeated, the players win the game »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003"), ["Puzzle.Damage('vt001', 99)"],
       {"fin": "gagne", "tous": 0}),
    _c("vt018 dernier vilain vaincu et AUCUN vilain sous le Vault : victoire ET defaite vraies ensemble -> VICTOIRE (arbitrage du 25/10/2026)",
       "les deux conditions du Vault a la fois : la victoire passe en premier",
       mechants_en_jeu("vt001"), ["Puzzle.Damage('vt001', 99)"],
       {"fin": "gagne"}),
    _c("vt018 vilain vaincu alors que le deck de vilains n'est PAS vide : le suivant est revele (livret p.1), pas de fin de partie",
       "« After the last villain leaves play, reveal the top card of the villain deck »",
       mechants_en_jeu("vt001") + sous_le_vault("vt005") + ["Puzzle.BuildVillainDeck('vt003')"], ["Puzzle.Damage('vt001', 99)"],
       {"tous": 1, "en_jeu": ["vt003"], "deck_de_mechants": 0, "hors_jeu": ["vt001"], "fin": None}),
    _c("vt018 un vilain vaincu n'emporte RIEN a la suite : ses degats, attachements et jetons disparaissent avec lui",
       "livret p.1 : « all tokens, status cards, and attachments on the just-defeated villain are discarded instead of carrying over »",
       mechants_en_jeu("vt001", "vt003") + sous_le_vault("vt005"), ["Puzzle.Damage('vt001', 99)"],
       {"tous": 1, "hors_jeu": ["vt001"], "en_jeu": ["vt003"], "fin": None}),

    # ============================================================ vt019 Inspection of the Vault
    _c("vt019 Alter-Ego Action : epuise l'identite, depense une ressource mentale -> l'Inspection est MISE DE COTE (hors jeu, pas defaussee)",
       "« Exhaust your identity and spend a [mental] resource -> set this card aside, out of play »",
       mechants_en_jeu("vt001") + sous_le_vault("vt003") + ["Puzzle.PutIntoPlay('vt019', under_control=True)"],
       ["Puzzle.Action('vt019', 'AlterEgoAction')"],
       {"inspection_en_jeu": False, "mis_de_cote": ["vt019"], "defausse": [], "exhausted": ["01001b"]},
       main_exclusive=["01089"]),
]


VERIFICATIONS = r'''
def vt_etat(monde, aides):
    """Cles propres : `vault_en_jeu` (bool), `sous_vault_mechants` / `sous_vault_sbires` (nombres), `sous_vault` (liste de card_id, ordre libre),
    `tous` (nombre de vilains en jeu), `deck_de_mechants`, `inspection_en_jeu` (bool), `fin` (None | "gagne" | "perdu"),
    `degats_joueurs` ([degats du joueur 1, du joueur 2...]), `le_mechant` (card_id de « the villain ») ; le reste va a etat_attendu."""
    from game.effect.rule import GameRule
    from game.operate.worlds import Worlds
    from game.operate.villains import Villains
    from game.card.face.base import Villain
    from game.card.face.card_type import Minion, Obligation
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    cid = lambda f: getattr(getattr(f, "paper", None), "card_id", None)
    effet = GameRule(Worlds.GetAllMainSchemes(monde)[0])
    vault = aides["par_id"](monde, "vt018")
    dessous = list(vault.GetPlacedCardArea().GetAll()) if vault is not None else []
    mesures = {
        "vault_en_jeu": vault is not None,
        "sous_vault_mechants": sum(1 for f in dessous if Villain.IsType(f)),
        "sous_vault_sbires": sum(1 for f in dessous if Minion.IsType(f)),
        "sous_vault": sorted(cid(f) for f in dessous),
        "tous": len(Villains.All(effet)),
        "deck_de_mechants": Villains.VillainDeckSize(effet),
        "inspection_en_jeu": bool(Worlds.FindCardsOnField(effet, name="Inspection of the Vault", card_type=Obligation)),
        "fin": (None if not monde.is_game_over else ("gagne" if monde.game_over.players_won else "perdu")),
        # degats subis par l'identite de chaque joueur (ordre des sieges) ; `le_mechant` : « the villain » d'une carte de rencontre.
        "degats_joueurs": [p.GetIdentity().max_health - p.GetIdentity().health for p in monde.const_seat_order_players],
        "le_mechant": cid(Worlds.FindVillain(effet)),
    }
    # `hazard_de` : [[card_id, n]] -> nombre d'icones Hazard de la carte en jeu.
    for card_id, n in attendu.get("hazard_de") or []:
        f = aides["par_id"](monde, card_id)
        mesures_h = getattr(f, "hazard", None) if f is not None else None
        if mesures_h != n:
            soucis_h = f"hazard de {card_id} = {mesures_h} (attendu {n})"
            return False, soucis_h
    soucis = []
    propres = set(mesures) | {"hazard_de"}
    for cle in propres:
        if cle in attendu and cle in mesures:
            voulu = sorted(attendu[cle]) if cle == "sous_vault" else attendu[cle]
            if mesures[cle] != voulu:
                soucis.append(f"{cle} = {mesures[cle]} (attendu {voulu})")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    if reste:
        copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
        ok, message = etat_attendu(monde, copie)
        if not ok:
            soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"The Vault : {mesures}"
'''
