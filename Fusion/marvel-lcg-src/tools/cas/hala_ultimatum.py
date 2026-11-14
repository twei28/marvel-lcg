# Cas test_capacites du scenario 3 HALA ULTIMATUM de Galactic Storm (gs138-gs155), lot GS-6 (20/10/2026).
# Format identique a tools/cas/kree_sentry.py ; noms prefixes `[hu]` (filtre : `[hu]`, ou `[hu] gs144 ` pour
# une carte).
#
# Conventions de ce fichier :
#  - le heros de test (Spider-Man, 01001) demarre en ALTER EGO ; `HEROS` le met en heros.
#  - la mise en place REELLE du scenario tourne a chaque cas (scenario=SC) : Hala (gs143) en jeu, Kree
#    Leader (I) (gs138a, HIDDEN) en jeu.
#  - priorite donnee a la mecanique HIDDEN (les deux moities, le flip, l'avancee de stade qui garde le
#    cote DISCOVERED) : c'est le coeur neuf du lot. Les autres cartes (attachements, sbires, manigances
#    annexes, traitrises) ont un cas de construction/texte chacune, sans aller jusqu'a la preuve par
#    substitution systematique faute de temps (consigne dans le rapport de fin de lot).
SC = "gs_hala_ultimatum"
HEROS = "Puzzle.ChangeForm('01001b')"
DECK_NEUTRE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', '01186', '01186', '01186')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[hu] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "hu_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================== HIDDEN, moitie attaque (NEUF)
    _c("gs138a HIDDEN, moitie attaque : le mechant attaque le heros -> aucun degat, 1 carte de rencontre "
       "face cachee distribuee",
       "« whenever a player would be attacked by the villain, that player is dealt a facedown encounter "
       "card » : Message.WhenUnitWouldAttack + SetBeInstead (modele AbilityFactoryEnemy.EnemyCannotActivate) "
       "+ Player.DealEncounterCards (modele ar012 Ares)",
       DECK_NEUTRE + [HEROS], ["Puzzle.Attack('gs138a')"],
       {"degats_identite": 0, "cartes_distribuees": 1}),
    _c("gs138a HIDDEN, moitie attaque, TEMOIN (sans HEROS en forme heros, meme attaque) : toujours aucun "
       "degat, une carte distribuee",
       "la redirection ne depend pas de la forme du joueur vise",
       DECK_NEUTRE, ["Puzzle.Attack('gs138a')"],
       {"degats_identite": 0, "cartes_distribuees": 1}),
    # ============================================================== HIDDEN, moitie immunite (wiring)
    # NOTE : la moitie immunite (CannotBeAffectedByPlayerCards) est deja testee en general par
    # briques_communes.py (14 cas, filtre [briques][immunite]) ; ce cablage (while_fn=HasTrait('HIDDEN'))
    # n'a PAS de cas dedie ici — `Puzzle.Stun`/`Puzzle.Tough` passent par `DebugRule`, qui CONTOURNE la
    # protection par construction (c'est voulu : le harnais doit pouvoir forcer un etat pour construire un
    # scenario de test), donc inadapte a la preuve. A verifier en partie reelle avec une vraie carte joueur
    # ciblant le mechant HIDDEN (voir questions du lot).
    _c("gs138a HIDDEN, attachements indiscutables : un Grand-High Pursuer attache ne peut pas etre "
       "defausse tant que le mechant est HIDDEN",
       "« Attachments attached to the villain cannot be discarded » : WhenCardWouldDiscard + SetBeInstead "
       "(modele skrull_menace/paibok RegleDesPouvoirs)",
       ["Puzzle.PutIntoPlay('gs144')"], ["Puzzle.Discard('gs144')"], {"en_jeu": ["gs144"], "attaches": [["gs138a", "gs144"]]}),
    _c("gs138a HIDDEN, attachements indiscutables, TEMOIN : une fois DISCOVERED (Tanalth), le meme "
       "attachement SE DEFAUSSE normalement",
       "la protection est imprimee seulement sur la face HIDDEN : elle tombe au retournement",
       ["Puzzle.PutIntoPlay('gs144')", "Puzzle.Flip('gs138a')"], ["Puzzle.Discard('gs144')"],
       {"hors_jeu": ["gs144"]}),
    # ============================================================== Flip HIDDEN -> DISCOVERED (gs142a)
    _c("gs142a When Revealed : flip le mechant vers DISCOVERED, met Hala de cote, chaque joueur pioche 1 "
       "carte — attachements et degats du stade HIDDEN sont CONSERVES (meme carte)",
       "« Flip the villain to its DISCOVERED side and set the Hala environment aside. Each player draws 1 "
       "card » : villain.card.Flip(effect) (modele gob/risky_business 02006a, sk189a Veranke) ; "
       "Faces.SetAside (Hala) ; Players.ForEachPlayer + DrawUp",
       ["Puzzle.PutIntoPlay('gs144')", "Puzzle.Damage('gs138a', 3)"], ["Puzzle.AdvanceMainScheme(1)"],
       {"en_jeu": ["gs138b"], "hors_jeu": ["gs138a", "gs143"], "attaches": [["gs138b", "gs144"]],
        "degats": [["gs138b", 3]]}),
    # ============================================================== Avancee de stade (native) garde le cote
    _c("Avancee native de stade : une fois DISCOVERED (Tanalth I), le stade suivant (II) entre DEJA sur "
       "Tanalth, pas sur Kree Leader",
       "`Scenario.AdvanceVillainStage` choisit la face du stade suivant portant le MEME NOM que la face "
       "vaincue (« the next stage enters play on the same side as the just-defeated stage »), natif, "
       "aucun code a ecrire pour cette regle — condition : les deux faces de chaque stade portent le MEME "
       "nom (« Kree Leader » / « Tanalth ») sur les trois stades",
       ["Puzzle.Flip('gs138a')"], ["Puzzle.AdvanceVillain()"],
       {"en_jeu": ["gs139b"], "hors_jeu": ["gs138a", "gs138b", "gs139a"]}),
    _c("Avancee native de stade, TEMOIN : SANS flip prealable (toujours HIDDEN), le stade suivant entre "
       "sur Kree Leader (II), pas sur Tanalth",
       "temoin : la regle « meme cote » fonctionne dans les deux sens",
       [], ["Puzzle.AdvanceVillain()"],
       {"en_jeu": ["gs139a"], "hors_jeu": ["gs138a", "gs139b"]}),
    # ============================================================== Tanalth (DISCOVERED), reponse forcee
    _c("gs138b Forced Response : Tanalth attaque et vainc un allie -> elle recoit un tenace",
       "« After Tanalth attacks and defeats a character, give her a tough status card »",
       ["Puzzle.Flip('gs138a')", "Puzzle.PutIntoPlay('01075', under_control=True)"],
       ["Puzzle.EnemyAttacks('gs138b', '01075')"],
       {"statuts": [["gs138b", "Tough"]], "hors_jeu": ["01075"]}),
    _c("gs138b Forced Response : Tanalth a DEJA un tenace, elle en vainc un second -> carte de boost face "
       "cachee en plus (pas un second tenace)",
       "« If she already has a tough status card, give her a facedown boost card »",
       ["Puzzle.Flip('gs138a')", "Puzzle.AddTough('gs138b', 1)", "Puzzle.PutIntoPlay('01075', under_control=True)"],
       ["Puzzle.EnemyAttacks('gs138b', '01075')"],
       {}, verifier="hu_boost_du_vilain"),
    # ============================================================== gs140b (stade III) : Steady + recherche
    _c("gs140b When Revealed (stade III) : cherche Grand-High Pursuer et l'attache a Tanalth",
       "« Search the encounter deck and discard pile for Grand-High Pursuer and attach it to Tanalth »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('gs144', '01186')", "Puzzle.Remove('gs138a')",
        "Puzzle.Remove('gs139a')"],
       ["Puzzle.Reveal('gs140b')"], {"attaches": [["gs140b", "gs144"]]}),
    # ============================================================== gs141b : repli et avancee vers 2A
    # CORRECTIF (20/10/2026, apres reconstruction de .game) : le rapport precedent accusait une « limite
    # outillage » sur les compteurs poses pendant la mise en place -- FAUX : `Puzzle.PlaceCounters` AJOUTE
    # des compteurs (il ne les POSE jamais a une valeur absolue), et la mise en place reelle de gs141a a
    # DEJA place 4 jetons hideout (2 + 2[per_hero], un joueur) avant que ce cas ne s'execute. Le cas
    # `Puzzle.PlaceCounters('gs143', 'hideout', 1)` portait donc Hala a 4+1=5, jamais a 1 : le dernier jeton
    # retire par le sbire vaincu ne tombait jamais a 0, et « avancer » n'etait jamais appelee -- confirme
    # par sonde (`check_is_last_counter` voyait `left_counter=4`, jamais 0). `Puzzle.Counter(..., -3)`
    # RETIRE 3 jetons (modele `Faces.RemoveCountersOn`), ramenant Hala a 1 avant le declencheur.
    _c("gs141b Forced Interrupt : un sbire vaincu retire 1 jeton de repli de Hala",
       "« When a minion is defeated, remove 1 hideout counter from Hala »",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Damage('01103', 3)"],
       {"compteurs": [["gs143", "hideout", 3]]}),
    _c("gs141b Forced Response : le DERNIER jeton de repli retire -> avance a 2A",
       "« After the last hideout counter is removed from Hala, advance to stage 2A »",
       DECK_NEUTRE + ["Puzzle.Counter('gs143', 'hideout', -3)", "Puzzle.PutIntoPlay('01103')"],
       # `principale` attend gs142b, pas gs142a : comme 1A -> 1B, la face « 2A » (gs142a) n'a pas de
       # seuil de menace imprime (`desc.Stage` seul) -- elle s'auto-avance VERS gs142b, SA PROPRE capacite
       # (le flip du mechant, Hala mise de cote, pioche) deja resolue entre-temps (confirme par sonde :
       # gs138b en jeu, gs143 hors jeu, apres l'enchainement complet).
       ["Puzzle.Damage('01103', 3)"], {"principale": "gs142b", "en_jeu": ["gs138b"], "hors_jeu": ["gs143"]}),
    # ============================================================== gs143 Hala : jetons et action
    _c("gs143 entree en jeu : 2 + 2[per_hero] jetons de repli (un joueur : 4)",
       "« Enters play with 2 hideout counters, plus 2[per_hero] additional hideout counters »",
       [], [], {"compteurs": [["gs143", "hideout", 4]]}),
    _c("gs143 Scour the Planet : cherche un sbire KREE et le revele, puis pioche 1 carte",
       "« Action: Search the encounter deck and discard pile for a KREE minion and reveal it -> draw 1 "
       "card »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('gs149', '01186')", HEROS],
       # CORRECTIF (20/10/2026) : la mise en place reelle de ce scenario fait piocher 6 cartes (pas 5), le
       # pioche de l'Action porte donc la main a 7, pas 6 (hypothese de depart erronee signalee dans le
       # rapport de fin de lot -- confirme par le journal : « Spider-Man pioche 6 carte(s) » a la mise en
       # place, puis « Spider-Man pioche 1 carte(s) » pour l'Action).
       ["Puzzle.Action('gs143')"], {"en_jeu": ["gs149"], "taille_main": 7}),
    # ============================================================== Attachements du mechant
    _c("gs144 Hero Action : depenser [energy][mental][physical] defausse la carte",
       "« Spend [energy][mental][physical] resources -> discard this card »",
       # CORRECTIF (20/10/2026) : tant que le mechant est HIDDEN (gs138a), la protection « Attachments
       # attached to the villain cannot be discarded » (testee a part sur gs138a) bloque AUSSI cette
       # defausse volontaire -- confirme par le journal (« WhenCardWouldDiscard est remplace par Kree
       # Leader »). Il faut flip le mechant vers DISCOVERED (Tanalth, gs138b) avant de pouvoir prouver le
       # Hero Action lui-meme.
       ["Puzzle.Flip('gs138a')", "Puzzle.PutIntoPlay('gs144')", HEROS, "Puzzle.CreateHandCards('gs006', 'gs003', 'gs008')"],
       ["Puzzle.Action('gs144')"], {"hors_jeu": ["gs144"]}),
    _c("gs146 Kree Resilience : le mechant peut porter DEUX tenaces (cap de base 1 + 1 supplementaire)",
       "« Attached villain can have 1 additional tough status card » : `RetenirTenaceSupplementaire(1)` "
       "etend le plafond de `can_status.py` (`tough_max`) pour l'HOTE attache",
       ["Puzzle.PutIntoPlay('gs146')"], ["Puzzle.AddTough('gs138a', 1)", "Puzzle.AddTough('gs138a', 1)"],
       {"statuts": [["gs138a", "Tough"]], "attaches": [["gs138a", "gs146"]]}),
    _c("gs146 Kree Resilience, TEMOIN : SANS la carte, le second tenace EXCEDENTAIRE est automatiquement "
       "defausse (plafond de base 1)",
       "temoin : le plafond de 1 est bien celui du moteur sans la carte",
       [], ["Puzzle.AddTough('gs138a', 1)", "Puzzle.AddTough('gs138a', 1)"],
       {"statuts": [["gs138a", "Tough"]]}),
    # ============================================================== Sbires
    _c("gs147 Kree Assassin : Retaliate 1 (base native) — le heros attaque Kree Assassin, qui lui rend 1 "
       "degat consequentiel",
       "desc.Retaliate, fiche mots-cles/retaliate.md : « after this character is attacked, deal 1 damage "
       "to the attacking character »",
       # CORRECTIF (20/10/2026, apres reconstruction de .game) : la recherche de mise en place de gs141a
       # (« each player searches the encounter deck for a KREE minion and reveals it ») engage DEJA un
       # Kree Soldier (gs149) avec le heros AVANT que ce cas ne s'execute -- sans le retirer, l'attaque de
       # base ciblait gs149 au lieu de gs147 (0 degat mesure, Kree Assassin jamais touche).
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs147')", HEROS, "Puzzle.Remove('gs149')"], ["Puzzle.Attack('01001a')"],
       {"degats_identite": 1}),
    _c("gs148 Kree Pursuer When Defeated : le mechant a un tenace -> Kree Pursuer rejoint le deck rencontre",
       "« When Defeated: If the villain has a tough status card, shuffle Kree Pursuer into the encounter "
       "deck »",
       DECK_NEUTRE + ["Puzzle.AddTough('gs138a', 1)", "Puzzle.PutIntoPlay('gs148')", HEROS],
       ["Puzzle.Damage('gs148', 10)"], {"hors_jeu": ["gs148"], "dans_deck_rencontre_n": [["gs148", 1]]}),
    # ============================================================== Manigances annexes (gs150-gs152)
    _c("gs150 When Defeated : pas de jeton de repli (0 restant) -> le vainqueur peut defausser un "
       "attachement « Hero Action » d'un ennemi",
       "« If you cannot, the defeating player may discard an attachment with the text \"Hero Action\" from "
       "an enemy »",
       # CORRECTIF (20/10/2026, apres reconstruction de .game) : `Puzzle.PlaceCounters` AJOUTE des
       # compteurs (il n'en pose jamais a 0 pile) -- `Puzzle.Counter(..., -N)` les RETIRE, modele
       # `Faces.RemoveCountersOn`. Et `Puzzle.SetThreat('gs150', 0)` vainc la manigance DIRECTEMENT en mise
       # en place, sans joueur vainqueur (`has_defeating_player=True` ne voit personne) : gs144 ne se
       # defaussait donc jamais. Menace mise a 1 (= le THW de base de Spider-Man) pour que ce soit bien le
       # `Puzzle.Thwart` du declencheur qui l'acheve, avec un vainqueur reel ; `cibles` force ce contre ET
       # non contre la manigance principale (egalement valide).
       DECK_NEUTRE + ["Puzzle.Counter('gs143', 'hideout', -99)", "Puzzle.PutIntoPlay('gs150')",
                      "Puzzle.PutIntoPlay('gs144')", HEROS, "Puzzle.SetThreat('gs150', 1)"],
       ["Puzzle.Thwart('01001a')"], {"hors_jeu": ["gs144"]}, cibles=["gs150"]),
    # ============================================================== Traitrises
    _c("gs153 When Revealed : le mechant n'a pas de tenace -> il en recoit un",
       "« Give the villain a tough status card »",
       DECK_NEUTRE, ["Puzzle.Reveal('gs153')"], {"statuts": [["gs138a", "Tough"]]}),
    _c("gs153 When Revealed : le mechant a DEJA un tenace -> defausse jusqu'a un attachement ou un sbire, "
       "revele",
       "« If the villain already has a tough status card, discard cards from the encounter deck until you "
       "discard an attachment or a minion and reveal it »",
       # CORRECTIF (20/10/2026) : `Puzzle.CreateEncounterDeck` empile chaque carte au-dessus de la
       # precedente -- la DERNIERE citee finit DESSUS (confirme par journal : avec ('01186', 'gs149'),
       # gs149 etait defaussee EN PREMIER, jamais 01186). Ordre inverse pour que 01186 (ni attachement ni
       # sbire) soit bien la premiere carte defaussee, et gs149 (sbire) celle qui arrete la defausse ; deux
       # cartes de bourrage SOUS les deux (le deck epuise en cours de resolution est remelange avec la
       # defausse -- constate au journal -- ce qui effacait 01186 de la defausse avant la verification).
       DECK_NEUTRE + ["Puzzle.AddTough('gs138a', 1)", "Puzzle.EmptyEncounterDeck()",
                      "Puzzle.CreateEncounterDeck('01186', '01186', 'gs149', '01186')"],
       ["Puzzle.Reveal('gs153')"], {"defausse_rencontre_n": [["01186", 1]], "en_jeu": ["gs149"]}),
    # gs154 Boost (« +2 boost icons si l'ennemi qui s'active a un tenace ») : construction verifiee
    # (test_cards, verifier_appels_modules), PAS de preuve par cas faute de temps — a verifier en partie
    # reelle (voir rapport de fin de lot).
    _c("gs155 When Revealed : le mechant a deja un tenace -> il s'active contre le joueur qui revele",
       "« If the villain already has a tough status card, the villain activates against you »",
       DECK_NEUTRE + ["Puzzle.AddTough('gs138a', 1)", HEROS], ["Puzzle.Reveal('gs155')"],
       {"cartes_distribuees": 1}),
]

VERIFICATIONS = r'''
def hu_etat(monde, aides):
    """etat_attendu (cles communes) + cles propres a Hala Ultimatum : mechant_id, principale,
    cartes_distribuees n, dans_deck_rencontre_n [[card_id, n]], defausse_rencontre_n [[card_id, n]]."""
    attendu = aides["cas"].get("attendu") or {}
    connues = set(CLES_ETAT_ATTENDU) | {"mechant_id", "principale", "cartes_distribuees",
                                        "dans_deck_rencontre_n", "defausse_rencontre_n"}
    inconnues = sorted(set(attendu) - connues)
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de hu_etat : {inconnues}"
    ok, message = etat_attendu(monde, aides)
    soucis = [] if ok else [message]
    if "mechant_id" in attendu:
        from game.operate.worlds import Worlds
        vilains = [getattr(v.paper, "card_id", None) for v in Worlds.GetAllVillains(monde)]
        if attendu["mechant_id"] not in vilains:
            soucis.append(f"mechant en jeu = {vilains} (attendu {attendu['mechant_id']})")
    if "principale" in attendu:
        from game.operate.worlds import Worlds
        mains = [getattr(m.paper, "card_id", None) for m in Worlds.GetAllMainSchemes(monde)]
        if attendu["principale"] not in mains:
            soucis.append(f"manigance principale = {mains} (attendu {attendu['principale']})")
    if "cartes_distribuees" in attendu:
        joueur = monde.players[0]
        n = len(joueur.dealt_encounter_cards.Get(True))
        if n != attendu["cartes_distribuees"]:
            soucis.append(f"cartes de rencontre distribuees au joueur 0 = {n} (attendu {attendu['cartes_distribuees']})")
    for card_id, n in attendu.get("dans_deck_rencontre_n") or []:
        from game.operate.worlds import Worlds
        reel = sum(1 for f in Worlds.GetEncounterDeckCards(monde) if getattr(f.paper, "card_id", None) == card_id)
        if reel != n:
            soucis.append(f"{card_id} dans le deck rencontre = {reel} (attendu {n})")
    for card_id, n in attendu.get("defausse_rencontre_n") or []:
        from game.operate.worlds import Worlds
        reel = sum(1 for f in Worlds.GetEncounterDiscardPileCards(monde) if getattr(f.paper, "card_id", None) == card_id)
        if reel != n:
            soucis.append(f"{card_id} dans la defausse rencontre = {reel} (attendu {n})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "ok"


def hu_boost_du_vilain(monde, aides):
    """gs138b : apres un second personnage vaincu alors qu'elle a deja un tenace, verifie que la pile de
    boost de Tanalth a grossi d'une carte face cachee (elle garde UN SEUL tenace, pas deux)."""
    vilain = aides["par_id"](monde, "gs138b")
    if vilain is None:
        return False, "gs138b introuvable en jeu"
    tenaces = vilain.GetCounters("tough") if hasattr(vilain, "GetCounters") else None
    pile = vilain.components.boostable.GetDeck().Get(True)
    if not pile:
        return False, "aucune carte de boost face cachee sur Tanalth"
    return True, f"boosts={len(pile)} tenaces={tenaces}"


def hu_sonde(monde, aides):
    """SONDE de mise au point (jamais dans la batterie finale) : decrit l'etat, rend toujours False."""
    lignes = []
    for objet in monde.object_manager.card_dict.values():
        f = objet.face
        if f is None:
            continue
        cid = getattr(f.paper, "card_id", "")
        if not cid.startswith("gs") and not (cid.startswith("010") and f.IsInPlay()):
            continue
        lignes.append(f"{cid}:{type(f).__name__}:jeu={f.IsInPlay()}:menace={getattr(f, 'threat', None)}"
                      f":pv={getattr(f, 'health', None)}")
    lignes.append(f"fin={monde.is_game_over}")
    return False, " | ".join(sorted(lignes))
'''
