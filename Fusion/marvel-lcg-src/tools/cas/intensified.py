# Cas test_capacites de la carte d'etat maison « Intensified » (TMNT, Inkwire, capture
# .planning/tmnt/intensified-capture.webp) et de l'environnement te201 Intense Combatants
# qui la pose : prefixes « [intensified] » et « [te201] ».
# Fiches : docs/reference/mots-cles/intensified.md, intensify.md.
#
# Texte : « The next time this character would discard a status card, discard this status
# card instead. This card cannot be given to a character that has no status cards. »
#
# Lecture codee : l'EFFET de la carte d'etat d'origine a lieu (Sonne annule l'attaque,
# Coriace previent les degats...), seule sa DEFAUSSE est remplacee : elle reste, Intensified
# part. Une defausse de plusieurs cartes d'un coup : chaque Intensified en remplace UNE.
#
# Montage (calque de cloaked.py) : Spider-Man (01001a ATQ 2 / CTR 1) en forme heros contre
# Rhino 01094 (ATQ 2 / MNG 1, PV 14). Le deck rencontre ne contient que 01105 « I'm Tough »
# (0 icone de boost). Heros incline + main videe quand Rhino frappe : le pilote ne defend pas.
#
# Verificateur `intensified_etat` : `nb` = [[card_id, statut, n]] (nombre EXACT de cartes de
# ce statut), le reste delegue a etat_attendu.

FORME_HEROS = "Puzzle.ChangeForm('01001b')"
INCLINE = "Puzzle.Exhaust('01001a')"
RIEN_A_BOOSTER = "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"
TE201 = "Puzzle.PutIntoPlay('te201')"
R = "01094"
H = "01001a"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": "spider_man",
           "mise_en_place": [FORME_HEROS] + mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "intensified_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ------------------------------------------------------------------ pose
    _c("[intensified] ne peut PAS etre donnee a un personnage sans carte d'etat",
       "« This card cannot be given to a character that has no status cards » : Rhino nu, rien n'est pose",
       [], [f"Puzzle.Intensify('{R}')"], {"nb": [[R, "Intensified", 0]]}),
    _c("[intensified] donnee a un personnage qui porte deja une carte d'etat",
       "Rhino Sonne : la pose reussit, la carte est reconnue (HasStatus Intensified)",
       [f"Puzzle.Stun('{R}')"], [f"Puzzle.Intensify('{R}')"],
       {"nb": [[R, "Intensified", 1], [R, "Stunned", 1]], "statuts": [[R, "Intensified"]]}),
    _c("[intensified] aucun plafond : deux Intensified s'empilent",
       "aucun plafond imprime (contrairement a Sonne / Hebete / Camoufle) : 2 poses = 2 cartes",
       [f"Puzzle.Stun('{R}')"], [f"Puzzle.Intensify('{R}', 2)"], {"nb": [[R, "Intensified", 2]]}),

    # ------------------------------------------------------------------ Sonne
    _c("[intensified] Sonne : l'attaque est QUAND MEME annulee, Sonne reste, Intensified part",
       "Rhino Sonne + Intensified attaque : 0 degat ; la defausse de Sonne est remplacee",
       [INCLINE, RIEN_A_BOOSTER, f"Puzzle.Stun('{R}')", f"Puzzle.Intensify('{R}')"],
       [f"Puzzle.Attack('{R}')"],
       {"degats_identite": 0, "nb": [[R, "Stunned", 1], [R, "Intensified", 0]]}, main_exclusive=["01088"]),
    _c("[intensified] TEMOIN : Sonne seul, l'attaque est annulee et Sonne part",
       "contre-cas du precedent : sans Intensified, la carte Sonne est defaussee",
       [INCLINE, RIEN_A_BOOSTER, f"Puzzle.Stun('{R}')"],
       [f"Puzzle.Attack('{R}')"],
       {"degats_identite": 0, "nb": [[R, "Stunned", 0]]}, main_exclusive=["01088"]),
    _c("[intensified] Sonne + Intensified : DEUX attaques annulees, puis plus rien",
       "Intensified double la duree : 1re attaque (Intensified part), 2e attaque (Sonne part), 0 degat au total",
       [INCLINE, RIEN_A_BOOSTER, f"Puzzle.Stun('{R}')", f"Puzzle.Intensify('{R}')"],
       [f"Puzzle.Attack('{R}')", f"Puzzle.Attack('{R}')"],
       {"degats_identite": 0, "nb": [[R, "Stunned", 0], [R, "Intensified", 0]]}, main_exclusive=["01088"]),
    _c("[intensified] deux Intensified + Sonne : une attaque n'en consomme qu'UNE",
       "« the next time » : chaque Intensified remplace une defausse ; il en reste une, Sonne reste",
       [INCLINE, RIEN_A_BOOSTER, f"Puzzle.Stun('{R}')", f"Puzzle.Intensify('{R}', 2)"],
       [f"Puzzle.Attack('{R}')"],
       {"degats_identite": 0, "nb": [[R, "Stunned", 1], [R, "Intensified", 1]]}, main_exclusive=["01088"]),

    # ------------------------------------------------------------------ Desoriente
    _c("[intensified] Desoriente : la manigance est QUAND MEME annulee, Desoriente reste",
       "Rhino Desoriente + Intensified manigance : 0 menace ; Intensified part a la place",
       [RIEN_A_BOOSTER, f"Puzzle.Confuse('{R}')", f"Puzzle.Intensify('{R}')"],
       [f"Puzzle.Scheme('{R}')"],
       {"menace": [["01097b", 0]], "nb": [[R, "Confused", 1], [R, "Intensified", 0]]}, main_exclusive=["01088"]),
    _c("[intensified] TEMOIN : Desoriente seul, la manigance est annulee et Desoriente part",
       "contre-cas du precedent",
       [RIEN_A_BOOSTER, f"Puzzle.Confuse('{R}')"],
       [f"Puzzle.Scheme('{R}')"],
       {"menace": [["01097b", 0]], "nb": [[R, "Confused", 0]]}, main_exclusive=["01088"]),

    # ------------------------------------------------------------------ Coriace
    _c("[intensified] Coriace : les degats sont QUAND MEME prevenus, Coriace reste",
       "3 degats sur Rhino Coriace + Intensified : 0 subi, Intensified part a la place de Coriace",
       [f"Puzzle.Tough('{R}')", f"Puzzle.Intensify('{R}')"],
       [f"Puzzle.Damage('{R}', 3)"],
       {"degats": [[R, 0]], "nb": [[R, "Tough", 1], [R, "Intensified", 0]]}),
    _c("[intensified] TEMOIN : Coriace seule, degats prevenus et Coriace part",
       "contre-cas du precedent",
       [f"Puzzle.Tough('{R}')"],
       [f"Puzzle.Damage('{R}', 3)"],
       {"degats": [[R, 0]], "nb": [[R, "Tough", 0]]}),

    # ------------------------------------------------------------------ Expose (defausse groupee)
    _c("[intensified] deux Exposes : +2 degats QUAND MEME, un Expose reste (Intensified en remplace UN)",
       "« discard ALL Exposed » defausse deux cartes ; l'Intensified remplace la defausse d'une seule : 2 + 2 = 4 degats, 1 Expose reste",
       [f"Puzzle.AddStatus('{R}', 'Exposed', 2)", f"Puzzle.Intensify('{R}')"],
       [f"Puzzle.Attack('{H}')"],
       {"degats": [[R, 4]], "nb": [[R, "Exposed", 1], [R, "Intensified", 0]]},
       main_exclusive=["01088"], cibles=[R]),
    _c("[intensified] TEMOIN : deux Exposes seuls, +2 degats et les deux partent",
       "contre-cas du precedent",
       [f"Puzzle.AddStatus('{R}', 'Exposed', 2)"],
       [f"Puzzle.Attack('{H}')"],
       {"degats": [[R, 4]], "nb": [[R, "Exposed", 0]]},
       main_exclusive=["01088"], cibles=[R]),

    # ------------------------------------------------------------------ Camoufle / Hebete
    _c("[intensified] Camoufle : +2 ATQ QUAND MEME, Camoufle reste",
       "attaque de base du heros Camoufle + Intensified : 4 degats ; Intensified part a la place",
       [f"Puzzle.Cloak('{H}')", f"Puzzle.Intensify('{H}')"],
       [f"Puzzle.Attack('{H}')"],
       {"degats": [[R, 4]], "nb": [[H, "Cloaked", 1], [H, "Intensified", 0]]},
       main_exclusive=["01088"], cibles=[R]),
    _c("[intensified] Hebete : -2 ATQ QUAND MEME, Hebete reste",
       "attaque de base du heros Hebete + Intensified : 0 degat ; Intensified part a la place",
       [f"Puzzle.Daze('{H}')", f"Puzzle.Intensify('{H}')"],
       [f"Puzzle.Attack('{H}')"],
       {"degats": [[R, 0]], "nb": [[H, "Dazed", 1], [H, "Intensified", 0]]},
       main_exclusive=["01088"], cibles=[R]),

    # ------------------------------------------------------------------ vidage
    {
        "nom": "[intensified] « defaussez chaque carte d'etat » : TOUT part, Intensified comprise, rien n'est remplace",
        "pourquoi": "DiscardEachStatus est un vidage : sans la garde `vidage`, Intensified remplacerait la 1re defausse et Sonne resterait",
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": [FORME_HEROS, f"Puzzle.Stun('{R}')", f"Puzzle.Intensify('{R}')"],
        "declencher": [],
        "verifier": "intensified_vider",
        "attendu": {},
    },

    # ------------------------------------------------------------------ te201 Intense Combatants
    _c("[te201] Forced Interrupt : un SECOND Sonne devient une Intensified",
       "« if that character already has 1 copy of that status card on them, intensify them instead »",
       [TE201, f"Puzzle.Stun('{R}')"], [f"Puzzle.AddStatus('{R}', 'Stunned')"],
       {"en_jeu": ["te201"], "nb": [[R, "Stunned", 1], [R, "Intensified", 1]]}),
    _c("[te201] TEMOIN : sans te201, le second Sonne est simplement refuse",
       "contre-cas : prouve que l'Intensified du cas precedent vient de te201",
       [f"Puzzle.Stun('{R}')"], [f"Puzzle.AddStatus('{R}', 'Stunned')"],
       {"nb": [[R, "Stunned", 1], [R, "Intensified", 0]]}),
    _c("[te201] premier Sonne : aucun exemplaire avant, la pose est normale",
       "« already has 1 copy » : sans exemplaire prealable, te201 ne fait rien",
       [TE201], [f"Puzzle.AddStatus('{R}', 'Stunned')"],
       {"nb": [[R, "Stunned", 1], [R, "Intensified", 0]]}),
    _c("[te201] un second Expose (empilable) devient lui aussi une Intensified",
       "texte litteral : « 1 copy of THAT status card », quel que soit le plafond du statut",
       [TE201, f"Puzzle.AddStatus('{R}', 'Exposed')"], [f"Puzzle.AddStatus('{R}', 'Exposed')"],
       {"nb": [[R, "Exposed", 1], [R, "Intensified", 1]]}),
    _c("[te201] TEMOIN : sans te201, deux Exposes s'empilent",
       "contre-cas du precedent",
       [f"Puzzle.AddStatus('{R}', 'Exposed')"], [f"Puzzle.AddStatus('{R}', 'Exposed')"],
       {"nb": [[R, "Exposed", 2], [R, "Intensified", 0]]}),
    _c("[te201] une seconde Intensified n'est pas « intensifiee » (pas de boucle), elle s'empile",
       "Intensified exclue de la fenetre de te201 : 2 poses d'Intensified = 2 cartes",
       [TE201, f"Puzzle.Stun('{R}')"], [f"Puzzle.Intensify('{R}', 2)"],
       {"nb": [[R, "Stunned", 1], [R, "Intensified", 2]]}),
    _c("[te201] vaut pour TOUT personnage : seconde Coriace sur le heros -> Intensified",
       "« a character » : ami comme ennemi",
       [TE201, f"Puzzle.Tough('{H}')"], [f"Puzzle.AddStatus('{H}', 'Tough')"],
       {"nb": [[H, "Tough", 1], [H, "Intensified", 1]]}),
    _c("[te201] chaine complete : Sonne x2 -> Intensified, puis DEUX attaques de Rhino annulees",
       "te201 pose l'Intensified, qui garde Sonne une attaque de plus : 0 degat, plus aucun etat",
       [TE201, INCLINE, RIEN_A_BOOSTER, f"Puzzle.Stun('{R}')", f"Puzzle.AddStatus('{R}', 'Stunned')"],
       [f"Puzzle.Attack('{R}')", f"Puzzle.Attack('{R}')"],
       {"degats_identite": 0, "nb": [[R, "Stunned", 0], [R, "Intensified", 0]]}, main_exclusive=["01088"]),
]

VERIFICATIONS = r'''
def intensified_etat(monde, aides):
    """etat_attendu + `nb` : [[card_id, statut, n]], nombre EXACT de cartes d'etat de ce nom."""
    attendu = aides["cas"].get("attendu") or {}
    inconnues = sorted(set(attendu) - set(CLES_ETAT_ATTENDU) - {"nb"})
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de intensified_etat : {inconnues}"
    reste = {k: v for k, v in attendu.items() if k != "nb"}
    copie = dict(aides); copie["cas"] = dict(aides["cas"]); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    soucis = [] if ok else [message]
    for card_id, statut, n in attendu.get("nb") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu ({statut})")
            continue
        reel = getattr(face.CastTo(aides["CanStatus"]), statut.lower())
        if reel != n:
            soucis.append(f"{card_id} porte {reel} carte(s) {statut} (attendu {n})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"


def intensified_vider(monde, aides):
    """Rhino porte Sonne + Intensified ; DiscardEachStatus doit TOUT emporter."""
    from game.effect.rule import GameRule
    rhino = aides["par_id"](monde, "01094")
    if rhino is None:
        return False, "Rhino introuvable"
    rhino = rhino.CastTo(aides["CanStatus"])
    if rhino.stunned != 1 or rhino.intensified != 1:
        return False, f"montage : Sonne={rhino.stunned} Intensified={rhino.intensified} (attendu 1 / 1)"
    rhino.DiscardEachStatus(GameRule(rhino))
    if rhino.GetStatusSize() != 0:
        return False, (f"il reste {rhino.GetStatusSize()} carte(s) d'etat apres « defaussez chaque carte "
                       f"d'etat » (Sonne={rhino.stunned}, Intensified={rhino.intensified})")
    return True, "toutes les cartes d'etat parties"
'''
