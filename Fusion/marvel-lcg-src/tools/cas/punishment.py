# Cas test_capacites du set PUNISHMENT (scenario 3 « One Last Kill », pack MC×DC 2026), PU-4. Prefixe `[pun]`.
# Montage : scenario `one_last_kill_jigsaw` (Punisher I + Jigsaw I cible, standard), Spider-Man en HEROS. La mise en place REELLE tourne :
# Punisher (pu086a) avec Target Lock FOCUSED (pu091a) et M1911s (pu095) attaches, Jigsaw (pu056a) avec In the Crosshairs, 5B (pu090b),
# complot 1B (pu088b). Les sbires de test (core) : 01103 Shocker (PV 3), 01110 Hydra Bomber (PV 2).
SC = "one_last_kill_jigsaw"
SCE = "one_last_kill_jigsaw_expert"
HEROS = "Puzzle.ChangeForm('01001b')"
ALTER_EGO = "Puzzle.ChangeForm('01001a')"
SANS_DEFENSE = {"passer_sur_option": "Defense"}


def _u(nom, pourquoi, mise, declencher, attendu, **cle):
    deck = cle.pop("deck", None)
    cas = {"nom": "[pun] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC), "heros": "spider_man",
           "mise_en_place": [*(["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join(repr(x) for x in deck)] if deck else []), HEROS, *mise],
           "declencher": declencher, "verifier": cle.pop("verifier", "pun_etat"), "attendu": attendu,
           "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


D4 = ["01105"] * 4
CAS = [
    # ---------------------------------------------------------------- mise en place
    _u("pu088a/pu090a Setup : Punisher, Jigsaw sous-fifre, Target Lock FOCUSED et M1911s sur Punisher, In the Crosshairs sur Jigsaw, 5B retournee",
       "« Find Target Lock and attach to Punisher, FOCUSED side up. Find Justice or Punishment? and reveal its setup side » ; 5A revele Jigsaw (I), In the Crosshairs",
       [], [], {"en_jeu": ["pu086a", "pu056a", "pu091a", "pu092", "pu088b", "pu090b", "pu095"],
                "accroche_a": [["pu091a", "pu086a"], ["pu095", "pu086a"], ["pu092", "pu056a"]]}),
    _u("pu090a/pu092 : les PV de Jigsaw = 14 (le NOMBRE imprime, pas par joueur) + 5 par joueur = 19 ; trait TARGETED",
       "« Set their hit points to the numeral » puis « +5[per hero] hit points, gains the TARGETED trait »",
       [], [], {"pv_max": [["pu056a", 19]], "traits_de": [["pu056a", "TARGETED"]]}),
    _u("pu092 : Jigsaw (stade courant) vaincu -> les joueurs perdent",
       "« If attached character's current stage is defeated, the players lose the game »",
       [], ["Puzzle.Damage('pu056a', 99)"], {"defaite": True}),
    _u("pu092 TEMOIN : Punisher blesse mais vivant -> pas de defaite", "contre-cas",
       [], ["Puzzle.Damage('pu086a', 3)"], {"defaite": False}),
    # ---------------------------------------------------------------- Target Lock FOCUSED
    _u("pu091a : Punisher va s'activer -> il attaque l'ennemi aux PV les plus bas (Shocker, 3 PV) a la place du heros",
       "« When Punisher would activate, he attacks the enemy with the fewest remaining hit points instead » (ATQ 1 + M1911s 1 = 2)",
       ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Attack('pu086a')"], {"degats": [["01103", 2]], "degats_identite": 0}, deck=D4, **SANS_DEFENSE),
    _u("pu091a : sans sbire, l'ennemi aux PV les plus bas est Jigsaw (19 PV) : il le blesse (2)",
       "Jigsaw est un ennemi", [], ["Puzzle.Attack('pu086a')"], {"degats": [["pu056a", 2]], "degats_identite": 0}, deck=D4, **SANS_DEFENSE),
    _u("pu091a : l'attaque blesse un ennemi -> menace sur le complot egale aux icones de boost de la carte du dessus de la defausse (Shocker : 1)",
       "« place threat on the main scheme equal to the number of boost icons on the top card of the encounter discard pile »",
       ["Puzzle.PutIntoPlay('01110')"], ["Puzzle.Attack('pu086a')"], {"menace": [["pu088b", 2]]}, deck=["01105", "01103"], **SANS_DEFENSE),
    _u("pu091a : Rachel (pu098) n'est jamais attaquee par Punisher -> il attaque Jigsaw",
       "« Punisher cannot attack this minion »",
       ["Puzzle.PutIntoPlay('pu098')"], ["Puzzle.Attack('pu086a')"], {"degats": [["pu098", 0], ["pu056a", 2]]}, deck=D4, **SANS_DEFENSE),
    # ---------------------------------------------------------------- Reponse de heros / Target Lock DISTRACTED
    _u("pu086a Hero Response : apres avoir attaque Punisher, 2 ressources -> Target Lock DISTRACTED et une arme non permanente defaussee (M1911s)",
       "« flip Target Lock to its DISTRACTED side and discard one non-permanent attachment from Punisher »",
       [], ["Puzzle.Attack('01001a')"], {"en_jeu": ["pu091b"], "hors_jeu": ["pu095"]},
       cibles=["pu086a"], main_exclusive=["01089", "01090"], payer_avec=["01089", "01090"], payer_tout=True),
    _u("pu091b : fin de manche -> Target Lock revient FOCUSED",
       "« At the end of the round, flip this card »",
       [ "Puzzle.ChangeToFace('pu091a', 'pu091b')" ], ["Puzzle.SendRoundEnd()"], {"en_jeu": ["pu091a"]}),
    # ---------------------------------------------------------------- manigances principales
    _u("pu088b : apres l'etape 1 de la phase du vilain, Jigsaw (le vilain cible) s'active contre le premier joueur (ATQ 1 : 1 degat) ; Punisher (phase du vilain) est renvoye par Target Lock sur Jigsaw (2 degats)",
       "« After resolving step one of the villain phase, the TARGETED villain activates against the first player »",
       [], ["Puzzle.RunVillainPhase()"], {"degats_identite": 1, "degats": [["pu056a", 2]]}, deck=D4, **SANS_DEFENSE),
    _u("pu089a : revele -> Assault Rifle (pu093) trouve et revele, Target Lock passe DISTRACTED",
       "« Find and reveal Punisher's Assault Rifle. Flip Target Lock to its DISTRACTED side »",
       [], ["Puzzle.Reveal('pu089a,pu089b')"], {"en_jeu": ["pu093", "pu091b"]}, deck=["pu093", "01105"]),
    # ---------------------------------------------------------------- armes
    _u("pu093 Assault Rifle : revele -> defausse les autres ARMAMENT (M1911s), s'attache a Punisher avec 2 compteurs ammo",
       "« Discard each other ARMAMENT card in play » ; « Uses (2[per hero] ammo counters) »",
       [], ["Puzzle.Reveal('pu093')"], {"hors_jeu": ["pu095"], "accroche_a": [["pu093", "pu086a"]], "compteurs": [["pu093", "ammo", 2]]}),
    _u("pu095 M1911s : apres l'attaque de Punisher, 1 compteur ammo retire (2 -> 1)",
       "« After Punisher attacks, remove 1 ammo counter from here »",
       [], ["Puzzle.Attack('pu086a')"], {"compteurs": [["pu095", "ammo", 1]]}, deck=D4, **SANS_DEFENSE),
    _u("pu094 RPG : revele -> M1911s defaussee ; l'attaque (ATQ 1 + 2) inflige des degats INDIRECTS et epuise le personnage blesse (le heros)",
       "« Punisher's attacks deal indirect damage. Exhaust any character damaged by his attack »",
       ["Puzzle.Reveal('pu094')"], ["Puzzle.EnemyAttacks('pu086a', '01001a')"], {"hors_jeu": ["pu095"], "exhausted": ["01001a"], "degats_identite": 3, "compteurs": [["pu094", "ammo", 1]]},
       deck=D4, **{"passer_sur_option": "Defense"}),
    _u("pu094 RPG contre un ENNEMI (Target Lock) : degats normaux (ATQ 1 + 2), Jigsaw epuise, 1 compteur retire",
       "indirect seulement contre un joueur", ["Puzzle.Reveal('pu094')"], ["Puzzle.Attack('pu086a')"],
       {"degats": [["pu056a", 3]], "exhausted": ["pu056a"], "compteurs": [["pu094", "ammo", 1]]}, deck=D4, **{"passer_sur_option": "Defense"}),
    # ---------------------------------------------------------------- Mexican Standoff
    _u("pu096 Mexican Standoff : le heros attaque Punisher -> Punisher puis Jigsaw s'activent contre lui sans boost, la carte est defaussee",
       "« he activates. Then, the TARGETED villain activates against you. Do not give either character a boost card »",
       ["Puzzle.Reveal('pu096')"], ["Puzzle.Attack('01001a')"], {"hors_jeu": ["pu096"], "degats_identite": 1}, deck=D4, cibles=["pu086a"]),
    # ---------------------------------------------------------------- sbires
    _u("pu097 Microchip : va s'activer -> a la place Punisher recoit une carte de boost face cachee",
       "« When Microchip would activate, give Punisher a facedown boost card instead »",
       ["Puzzle.PutIntoPlay('pu097')"], ["Puzzle.Attack('pu097')"], {"degats_identite": 0, "boosts_punisher": 1}, deck=D4, verifier="pun_etat"),
    _u("pu097 Microchip vaincu : revele l'arme du dessus de la defausse (Assault Rifle)",
       "« Reveal the top WEAPON attachment in the encounter discard pile »",
       ["Puzzle.CreateEncounterDiscardPile('pu093')", "Puzzle.PutIntoPlay('pu097')"], ["Puzzle.Damage('pu097', 3)"], {"en_jeu": ["pu093"]}),
    _u("pu098 Rachel : va manigancer (alter ego) -> elle attaque Jigsaw a la place (ATQ 2)",
       "« When Rachel Cole-Alves would scheme, she attacks the TARGETED villain instead »",
       [ALTER_EGO, "Puzzle.PutIntoPlay('pu098')"], ["Puzzle.Scheme('pu098')"], {"degats": [["pu056a", 2]], "menace": [["pu088b", 1]]}, deck=D4),
    # ---------------------------------------------------------------- Judge, Jury... Execution!
    _u("pu099 vaincu : le sbire aux PV les plus bas (Bomber, 2 PV) est defausse et Jigsaw prend 2 degats",
       "« deal damage to the TARGETED villain equal to that minion's remaining hit points »",
       ["Puzzle.PutIntoPlay('pu099')", "Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')"],
       ["Puzzle.SetThreat('pu099', 1)", "Puzzle.Thwart('01001a')"], {"hors_jeu": ["01110"], "degats": [["pu056a", 2]], "en_jeu": ["01103"]}, cibles=["pu099"]),
    _u("pu099 vaincu, aucun sbire : Punisher recoit une carte de boost face cachee",
       "« Otherwise, give Punisher a facedown boost card »",
       ["Puzzle.PutIntoPlay('pu099')"], ["Puzzle.SetThreat('pu099', 1)", "Puzzle.Thwart('01001a')"], {"boosts_punisher": 1}, cibles=["pu099"]),
    # ---------------------------------------------------------------- traitrises
    _u("pu100 Back Against the Wall (alter ego) : 1 degat (ATQ de Jigsaw) sur Punisher, que sa carte Tenace absorbe (elle saute)",
       "« Deal damage to Punisher equal to the TARGETED villain's ATK »", [ALTER_EGO], ["Puzzle.Reveal('pu100')"], {"statuts_absents": [["pu086a", "Tough"]]}, deck=D4),
    _u("pu100 Back Against the Wall (heros) : Target Lock passe DISTRACTED et Punisher s'active (ATQ 1 + 1 M1911s + 1 DISTRACTED = 3)",
       "« Flip Target Lock to its DISTRACTED side. Punisher activates »", [], ["Puzzle.Reveal('pu100')"], {"en_jeu": ["pu091b"], "degats_identite": 3}, deck=D4, **SANS_DEFENSE),
    _u("pu102 Bullet Spray : 1 degat au heros, 1 a Jigsaw et 1 a chaque sbire engage (Shocker)",
       "« Deal 1 damage to each character you control. Deal 1 damage to the TARGETED villain and each minion engaged with you »",
       ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Reveal('pu102')"], {"degats_identite": 1, "degats": [["pu056a", 1], ["01103", 1]]}, deck=D4),
    _u("pu104 Flash-Bang : le heros, Jigsaw et le sbire engage sont etourdis",
       "« Stun each character you control. Stun the TARGETED villain and each minion engaged with you »",
       ["Puzzle.PutIntoPlay('01103')"], ["Puzzle.Reveal('pu104')"],
       {"statuts": [["01001a", "Stunned"], ["pu056a", "Stunned"], ["01103", "Stunned"]]}, deck=D4),
    _u("pu105 Say Good Night (alter ego) : Jigsaw prend des degats egaux a l'ATQ de Punisher (1 + 1 M1911s = 2)",
       "« Deal damage to the TARGETED villain equal to Punisher's ATK »", [ALTER_EGO], ["Puzzle.Reveal('pu105')"], {"degats": [["pu056a", 2]]}, deck=D4),
    _u("pu105 Say Good Night (heros) : le heros prend l'ATQ de Punisher (2) s'il ne l'evite pas",
       "« Take damage equal to Punisher's ATK »", [], ["Puzzle.Reveal('pu105')"], {"degats_identite": 2}, deck=D4),
    # ---------------------------------------------------------------- fin de partie
    _u("pu090b : le dernier stade de Punisher vaincu -> les joueurs gagnent (stade II standard apres le I)",
       "« If Punisher's final stage is defeated, the players win the game »",
       [], ["Puzzle.Damage('pu086a', 99)", "Puzzle.Damage('pu086a', 99)", "Puzzle.Damage('pu087a', 99)", "Puzzle.Damage('pu087a', 99)"], {"victoire": True}, deck=D4),
    _u("pu090b TEMOIN : le stade I vaincu ne gagne pas ; le stade II apparait avec Target Lock",
       "stades intermediaires", [], ["Puzzle.Damage('pu086a', 99)", "Puzzle.Damage('pu086a', 99)"], {"en_jeu": ["pu087a", "pu091a"], "victoire": False, "defaite": False}, deck=D4),
    # ---------------------------------------------------------------- variantes du scenario
    _u("expert : Punisher II (pu086b), Jigsaw II (pu056b) cible avec 16 + 5 = 21 PV",
       "« Reveal the UNDERLING villain (I for standard, II for expert mode) »", [], [],
       {"en_jeu": ["pu086b", "pu056b", "pu091a", "pu092"], "pv_max": [["pu056b", 21]], "traits_de": [["pu056b", "TARGETED"]]}, scenario=SCE),
    _u("Hobgoblin sous-fifre : Hobgoblin I (pu071a) cible avec 15 + 5 = 20 PV",
       "scenario one_last_kill_hobgoblin", [], [],
       {"en_jeu": ["pu086a", "pu071a", "pu092"], "pv_max": [["pu071a", 20]]}, scenario="one_last_kill_hobgoblin"),
]

VERIFICATIONS = r'''
def pun_etat(monde, aides):
    """etat_attendu + `defaite` (les joueurs ont perdu) ; accepte aussi `victoire`."""
    attendu = aides["cas"].get("attendu") or {}
    inconnues = sorted(set(attendu) - set(CLES_ETAT_ATTENDU) - {"defaite", "victoire", "boosts_punisher"})
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de pun_etat : {inconnues}"
    reste = {k: v for k, v in attendu.items() if k not in ("defaite", "victoire", "boosts_punisher")}
    aides["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, aides)
    aides["cas"]["attendu"] = attendu
    soucis = [] if ok else [message]
    if "boosts_punisher" in attendu:
        v = aides["par_id"](monde, "pu086a")
        n = v.components.boostable.GetDeck().GetSize()
        if n != attendu["boosts_punisher"]:
            soucis.append(f"cartes de boost face cachee de Punisher = {n} (attendu {attendu['boosts_punisher']})")
    perdu = bool(monde.is_game_over) and not monde.game_over.players_won
    gagne = bool(monde.is_game_over) and bool(monde.game_over.players_won)
    if "defaite" in attendu and perdu != attendu["defaite"]:
        soucis.append(f"defaite = {perdu} (attendu {attendu['defaite']})")
    if "victoire" in attendu and gagne != attendu["victoire"]:
        soucis.append(f"victoire = {gagne} (attendu {attendu['victoire']})")
    return (False, " ; ".join(soucis)) if soucis else (True, "etat Punishment conforme")
'''
