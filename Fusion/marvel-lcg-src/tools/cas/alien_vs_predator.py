# Cas test_capacites du scenario custom ALIEN VS. PREDATOR (RyCoRan, prefixe `ap`) : noms prefixes « [ap] » puis le card_id
# (substituer_pack.py filtre dessus). 1er fichier : le SOCLE (mise en place, deux mechants, compteur actif, faces Defeated, complots).
#
# Rappels de montage :
#  - scenario `alien_vs_predator` (standard : ap001a/ap002a) ou `alien_vs_predator_expert` (ap003a/ap004a) = la VRAIE mise en place
#    (ap005a) : Reine puis Warlord en jeu, Skulls for the Taking et Expanding Hive en jeu (2 menaces chacune en solo), 16 Alien Scout
#    glisses sous la Reine, compteur actif sur la Reine, complot 1B (ap005b) a 0 menace ;
#  - heros `spider_man` (01001a/b) ; la partie commence en ALTER-EGO ; `HEROS` passe en forme heros ;
#  - `SANS_BOOST` remplace le deck de rencontre par des cartes sans icone boost (01098 Armored Rhino Suit : sans Rhino en jeu, elle ne fait
#    rien ; surtout PAS 01105 « I'm Tough », qui gagne surge des que le mechant est Tenace et boucle sans fin avec la regle v18) : une attaque ou une manigance n'est pas
#    modifiee par un boost tire au hasard ;
#  - en forme heros, Spider-Sense (01001a) fait piocher a chaque attaque du mechant : ne JAMAIS vider le deck du joueur dans un cas
#    d'attaque (la pioche dans un deck vide bloque l'attaque, dommages jamais infliges) ;
#  - le pilote DEFEND chaque attaque par defaut (degats annules) : `passer_sur_option="Defense"` pour laisser le heros encaisser ;
#  - la main de depart de Spider-Man contient Great Responsibility (01061) : le pilote la joue des que de la menace va au complot
#    principal (menace remplacee par des degats) ; `Puzzle.EmptyHand()` dans les cas qui mesurent cette menace ;
#  - 01088 Energy = Y, 01089 Genius = B, 01090 Strength = R.
SC = "alien_vs_predator"
SCX = "alien_vs_predator_expert"
HEROS = "Puzzle.ChangeForm('01001a')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]
SANS_DECK = "Puzzle.EmptyPlayerDeck()"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[ap] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "ap_etat"), "attendu": attendu}
    # Les REGLES D'UNE VRAIE PARTIE (25/10/2026) : le lanceur (public/js/prepare/launcher.js) pose `v16_all` et `v18_all` sur toute partie
    # neuve. Sans elles le harnais jouait l'ANCIEN surge (revelation immediate), que le jeu n'utilise plus : avec le deck de remplissage
    # 01105 (« I'm Tough » gagne surge si le mechant est deja Tenace) les surges s'enchainaient, vidaient le deck et le moteur repiochait
    # une carte encore en cours de revelation (AssertionError avalee, `face_on_event.py` Reveal). Avec v18, un surge DISTRIBUE face cachee
    # (et 01105 bouclerait sans fin : d'ou le remplissage 01098).
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ ap005a : mise en place REELLE
    _c("ap005a Setup (standard) : Reine et Warlord en jeu, Skulls et Expanding Hive en jeu, 16 Alien Scout sous la Reine, compteur actif sur la Reine",
       "« Put Skulls for the Taking and Expanding Hive into play. Place the Xenomorph deck next to Alien Queen and place the active counter on her »",
       [], [],
       {"mechants": ["ap001a", "ap002a"], "actif": "ap001a", "sous_reine": 16, "en_jeu": ["ap009", "ap010"],
        "menace": [["ap009", 2], ["ap010", 2], ["ap005b", 0]], "complot": "ap005b", "fin": None},
       avec_boost=True),
    _c("ap005a Setup (expert) : les faces B (ap003a, ap004a) sont en jeu, compteur actif sur la Reine",
       "« Alien Queen (A) and Predator Warlord (A) (B instead in expert mode) »",
       [], [],
       {"mechants": ["ap003a", "ap004a"], "actif": "ap003a", "sous_reine": 16, "fin": None},
       scenario=SCX, avec_boost=True),

    # ============================================================ ap001a / ap002a : la menace va sur LEUR manigance
    _c("ap001a la Reine manigance : sa menace (2) va sur Expanding Hive, pas sur le complot ; le compteur passe au Warlord (1B)",
       "« When Alien Queen schemes, place that threat on her side scheme instead » + 1B « After a villain activates, move the active counter »",
       [], ["Puzzle.Scheme('ap001a')"],
       {"menace": [["ap009", 4], ["ap010", 2], ["ap005b", 0]], "actif": "ap002a"}),
    _c("ap002a le Warlord manigance : sa menace (1) va sur Skulls for the Taking ; le compteur revient a la Reine",
       "« When Predator Warlord schemes, place that threat on his side scheme instead »",
       ["Puzzle.SetActiveVillain('ap002a')"], ["Puzzle.Scheme('ap002a')"],
       {"menace": [["ap010", 3], ["ap009", 2], ["ap005b", 0]], "actif": "ap001a"}),
    _c("ap001a « if able » : Expanding Hive absente -> la menace de la Reine va sur le complot principal",
       "« place that threat on her side scheme instead of the main scheme, IF ABLE »",
       ["Puzzle.Remove('ap009')"], ["Puzzle.Scheme('ap001a')"],
       {"menace": [["ap005b", 2]]}),
    _c("ap001a la Reine attaque et blesse le heros : un Alien Scout passe de sous la Reine au deck du joueur",
       "« After Alien Queen attacks and damages a character you control, shuffle a Xenomorph card into your deck »",
       [HEROS], ["Puzzle.Attack('ap001a')"],
       {"sous_reine": 15, "scouts_deck_joueur": 1, "degats_identite": 1}, passer_sur_option="Defense"),
    _c("ap001a contre-cas : la Reine attaque mais ne blesse pas (le heros defend) -> aucun Alien Scout melange",
       "« attacks AND DAMAGES »",
       [HEROS, "Puzzle.Tough('01001a')"], ["Puzzle.Attack('ap001a')"],
       {"sous_reine": 16, "scouts_deck_joueur": 0}),
    _c("ap002a le Warlord attaque : le joueur choisit +1 ATK (option 2) -> 3 degats au heros",
       "« either place 2 threat on the main scheme or he gets +1 ATK for this attack »",
       [HEROS, "Puzzle.SetActiveVillain('ap002a')"], ["Puzzle.Attack('ap002a')"],
       {"degats_identite": 3, "menace": [["ap005b", 0]]},
       choisir_option="Predator_Warlord_gets_+1_ATK_for_this_attack", passer_sur_option="Defense"),
    _c("ap002a le Warlord attaque : option 1 -> 2 menaces sur le complot principal, attaque a 2",
       "« either place 2 threat on the main scheme or ... »",
       [HEROS, "Puzzle.EmptyHand()", "Puzzle.SetActiveVillain('ap002a')"], ["Puzzle.Attack('ap002a')"],
       {"degats_identite": 2, "menace": [["ap005b", 2], ["ap010", 2]]},
       choisir_option="Place_2_threat_on_the_main_scheme", passer_sur_option="Defense"),

    _c("ap003a (expert) la Reine B manigance : sa menace (2) va sur Expanding Hive",
       "ap003a : meme texte que ap001a (« place that threat on her side scheme instead »)",
       [], ["Puzzle.Scheme('ap003a')"],
       {"menace": [["ap009", 4], ["ap005b", 0]], "actif": "ap004a"}, scenario=SCX),
    _c("ap003a (expert) la Reine B attaque et blesse le heros : un Alien Scout melange dans le deck du joueur",
       "ap003a « After Alien Queen attacks and damages a character you control, shuffle a Xenomorph card into your deck »",
       [HEROS], ["Puzzle.Attack('ap003a')"],
       {"sous_reine": 15, "scouts_deck_joueur": 1, "degats_identite": 2}, scenario=SCX, passer_sur_option="Defense"),
    _c("ap004a (expert) le Warlord B manigance : sa menace (1) va sur Skulls for the Taking",
       "ap004a : meme texte que ap002a",
       ["Puzzle.SetActiveVillain('ap004a')"], ["Puzzle.Scheme('ap004a')"],
       {"menace": [["ap010", 3], ["ap005b", 0]], "actif": "ap003a"}, scenario=SCX),
    _c("ap004a (expert) le Warlord B attaque, option +1 ATK : 4 degats (ATK 3 + 1)",
       "ap004a « either place 2 threat on the main scheme or he gets +1 ATK for this attack »",
       [HEROS, "Puzzle.SetActiveVillain('ap004a')"], ["Puzzle.Attack('ap004a')"],
       {"degats_identite": 4}, scenario=SCX,
       choisir_option="Predator_Warlord_gets_+1_ATK_for_this_attack", passer_sur_option="Defense"),

    # ============================================================ ap005b : le compteur actif
    _c("ap005b la Reine SONNEE au moment d'attaquer : pas d'attaque, mais le compteur passe au Warlord (arbitrage du 25/10/2026)",
       "« After a villain activates, move the active counter » : la carte Sonne remplace l'activation, l'alternance ne se casse pas",
       [HEROS, "Puzzle.Stun('ap001a')"], ["Puzzle.Attack('ap001a')"],
       {"degats_identite": 0, "actif": "ap002a", "statuts_absents": [["ap001a", "Stunned"]]}),
    _c("ap005b etape 1 : aucune menace sur les DEUX manigances des mechants -> 2 degats a chaque mechant",
       "« if there is no threat on each villain's side scheme, deal 2 damage to each villain »",
       ["Puzzle.SetThreat('ap009', 0)", "Puzzle.SetThreat('ap010', 0)"], ["Puzzle.RunVillainPhase()"],
       {"degats": [["ap001a", 2], ["ap002a", 2]]}),
    _c("ap005b etape 1 contre-cas : une menace reste sur Skulls -> aucun degat aux mechants",
       "« no threat on EACH villain's side scheme »",
       ["Puzzle.SetThreat('ap009', 0)", "Puzzle.SetThreat('ap010', 1)"], ["Puzzle.RunVillainPhase()"],
       {"degats": [["ap001a", 0], ["ap002a", 0]]}),
    _c("ap005b insert : les deux mechants a 2 PV, manigances vides -> ils tombent ensemble et les joueurs GAGNENT",
       "insert « Ultimate Hunt 1B » : « they are both reduced to zero health and the players win the game »",
       ["Puzzle.SetThreat('ap009', 0)", "Puzzle.SetThreat('ap010', 0)", "Puzzle.SetHealth('ap001a', 2)", "Puzzle.SetHealth('ap002a', 2)"],
       ["Puzzle.RunVillainPhase()"],
       {"fin": "gagne"}),

    # ============================================================ ap001a/ap001b : la Reine vaincue se retourne
    _c("ap001b face Defeated de la Reine (ap001a vaincue, Warlord en jeu) : Warlord soigne de 4, Tenace, stade 3A puis 3B, manigances permanentes et la Reine retirees",
       "« When Defeated: Flip this card » + ap001b « Heal 4[per_hero] damage from Predator Warlord and give him a tough status card. Advance to stage 3A. "
       "Remove each permanent side scheme and this card from the game »",
       ["Puzzle.Damage('ap002a', 6)"], ["Puzzle.Damage('ap001a', 99)"],
       {"mechants": ["ap002a"], "degats": [["ap002a", 2]], "statuts": [["ap002a", "Tough"]], "complot": "ap007b",
        "hors_jeu": ["ap009", "ap010"], "actif": "ap002a", "fin": None}),
    _c("ap002b face Defeated du Warlord (ap002a vaincu, Reine en jeu) : Reine soignee de 4, Tenace, stade 4B",
       "ap002b « Heal 4[per_hero] damage from Alien Queen ... Advance to stage 4A »",
       ["Puzzle.Damage('ap001a', 5)"], ["Puzzle.Damage('ap002a', 99)"],
       {"mechants": ["ap001a"], "degats": [["ap001a", 1]], "statuts": [["ap001a", "Tough"]], "complot": "ap008b",
        "hors_jeu": ["ap009", "ap010"], "actif": "ap001a", "fin": None}),
    _c("ap003b (expert) la Reine B vaincue : le Warlord B est soigne de 6",
       "ap003b « Heal 6[per_hero] damage from Predator Warlord »",
       ["Puzzle.Damage('ap004a', 8)"], ["Puzzle.Damage('ap003a', 99)"],
       {"mechants": ["ap004a"], "degats": [["ap004a", 2]], "complot": "ap007b"},
       scenario=SCX),
    _c("ap004b (expert) le Warlord B vaincu : la Reine B est soignee de 6",
       "ap004b « Heal 6[per_hero] damage from Alien Queen »",
       ["Puzzle.Damage('ap003a', 8)"], ["Puzzle.Damage('ap004a', 99)"],
       {"mechants": ["ap003a"], "degats": [["ap003a", 2]], "complot": "ap008b"},
       scenario=SCX),
    _c("ap001a second mechant vaincu (Reine seule restante) -> les joueurs GAGNENT, sans face Defeated (arbitrage 2 du 25/10/2026)",
       "« When Defeated: Flip this card » ne se joue pas pour le dernier mechant (1er degat : la Tenace donnee par ap002b)",
       ["Puzzle.Damage('ap002a', 99)"], ["Puzzle.Damage('ap001a', 1)", "Puzzle.Damage('ap001a', 99)"],
       {"fin": "gagne"}),
]


VERIFICATIONS = r'''
def ap_etat(monde, aides):
    """Cles propres : `mechants` (card_id des mechants vivants en jeu, ordre libre), `actif` (card_id du mechant actif), `complot`
    (card_id du complot principal en jeu), `sous_reine` (Alien Scout glisses sous la Reine), `scouts_deck_joueur` (Alien Scout dans le
    deck du joueur 1), `scouts_distribues` (Alien Scout distribues face cachee au joueur 1), `distribuees`
    (toutes les cartes de rencontre face cachee du joueur 1), `scouts_defausse_joueur` (dans sa defausse),
    `boosts_de` ([[card_id, n]] cartes boost face cachee sur un ennemi), `garde` (la garde « do not move » encore posee), `retires` / `pas_retires` (card_id
    dans / hors de la zone « retire de la partie »), `engage_avec` ([[card_id, rang du joueur a partir de 0]]),
    `peut_defendre` ([[defenseur, attaquant, bool]] : `IsCanDefense`, la question que le moteur pose avant d'offrir la defense), `fin`
    (None | "gagne" | "perdu"), `menace_complot` ; le reste va a etat_attendu."""
    from game.effect.rule import GameRule
    from game.operate.worlds import Worlds
    from game.operate.villains import Villains
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    cid = lambda f: getattr(getattr(f, "paper", None), "card_id", None)
    joueur_1 = lambda m: m.const_seat_order_players[0]
    scouts = ("ap101", "ap102", "ap103", "ap104")
    complots = [c for c in Worlds.GetAllMainSchemes(monde) if c.IsInPlay()]
    effet = GameRule(joueur_1(monde).GetIdentity())
    vivants = [v for v in Worlds.GetVillains(effet) if not v.HasTrait("DEFEATED")]
    actif = None
    for v in vivants:
        if v.IsActive():
            actif = v
    reine = next((v for v in vivants if v.IsName("Alien Queen")), None)
    joueur = monde.const_seat_order_players[0]
    distribuees = list(joueur.dealt_encounter_cards.GetAll()) if hasattr(joueur, "dealt_encounter_cards") else []
    mesures = {
        "mechants": sorted(cid(v) for v in vivants),
        "actif": cid(actif),
        "complot": cid(complots[0]) if complots else None,
        "sous_reine": sum(1 for f in reine.GetPlacedCardArea().GetAll() if cid(f) in scouts) if reine is not None else 0,
        "scouts_deck_joueur": sum(1 for f in joueur.player_deck.GetAll() if cid(f) in scouts),
        "scouts_distribues": sum(1 for f in distribuees if cid(f) in scouts),
        "distribuees": len(distribuees),
        "scouts_defausse_joueur": sum(1 for f in joueur.discard_pile.GetAll() if cid(f) in scouts),
        "garde": bool(getattr(monde, "_ap_garder_compteur", False)),
        "fin": (None if not monde.is_game_over else ("gagne" if monde.game_over.players_won else "perdu")),
        "menace_complot": complots[0].threat if complots else None,
    }
    soucis = []
    retires = [cid(f) for f in monde.area_removed.GetAll()]
    for card_id in attendu.get("retires") or []:
        if card_id not in retires:
            soucis.append(f"{card_id} n'est pas retire de la partie (retires = {retires})")
    for card_id in attendu.get("pas_retires") or []:
        if card_id in retires:
            soucis.append(f"{card_id} est retire de la partie")
    defausse_rencontre = [cid(f) for f in Worlds.GetEncounterDiscardPileCards(monde)]
    for card_id in attendu.get("pas_en_defausse_rencontre") or []:
        if card_id in defausse_rencontre:
            soucis.append(f"{card_id} est dans la defausse de rencontre")
    for defenseur, attaquant, voulu in attendu.get("peut_defendre") or []:
        d, a = aides["par_id"](monde, defenseur), aides["par_id"](monde, attaquant)
        peut = d.IsCanDefense(a) if d is not None and a is not None else None
        if peut != voulu:
            soucis.append(f"{defenseur} peut defendre contre {attaquant} = {peut} (attendu {voulu})")
    for card_id, rang in attendu.get("engage_avec") or []:
        f = aides["par_id"](monde, card_id)
        j = getattr(f, "engaged_player", None) if f is not None else None
        voulu = monde.const_seat_order_players[rang]
        if j is not voulu:
            soucis.append(f"{card_id} engage avec {j} (attendu le joueur {rang + 1})")
    for card_id, n in attendu.get("boosts_de") or []:
        f = aides["par_id"](monde, card_id)
        taille = f.components.boostable.GetDeck().GetSize() if f is not None else None
        if taille != n:
            soucis.append(f"boosts de {card_id} = {taille} (attendu {n})")
    propres = set(mesures) | {"boosts_de", "retires", "pas_retires", "engage_avec", "pas_en_defausse_rencontre", "peut_defendre"}
    for cle in propres:
        if cle in attendu and cle in mesures:
            voulu = sorted(attendu[cle]) if cle == "mechants" else attendu[cle]
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
    return True, f"AvP : {mesures}"
'''
