# Cas test_capacites des CARTES D'ASPECT du pack Elektra Natchios (MC63, 63015-63039), noms prefixes « [el_aspect] ».
# Un cas par capacite, sujet = le card_id dans le nom (substituer_pack.py filtre dessus). Gabarits PROCESSUS-CARTE :
# docs/packs/elektra_cartes.md. Plan et decisions : .planning/elektra-officiel/aspects-plan.md.
#
# Montage : vilain Rhino 01094 (14 PV, ATQ 2) contre Iron Fist (heros du pack iron_fist, alter ego Danny Rand au depart,
# `HEROS` le passe en forme heros : DEFENDER, MARTIAL ARTIST) ; `main_exclusive` dit avec QUOI on paie (01088 Energy = YY,
# 01089 Genius = BB, 01090 Strength = RR, 01055 The Power of Aggression = UNE ressource wild hors Aggression, 01079 The Power
# of Protection = UNE ressource wild hors Protection).
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('64001b', '64001a')"
CIVIL = "Puzzle.ChangeToFace('64001a', '64001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
VIDER_DEFAUSSE = "Puzzle.EmptyPlayerDiscardPile()"
DD_HEROS = "Puzzle.ChangeToFace('60001b', '60001a')"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[el_aspect] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "iron_fist"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "if_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ 63027 Dance with the Devil (reimpression : 60031 est un lien)
    _c("63027 Dance with the Devil : Team-Up (Daredevil et Elektra en jeu) : jouee sur Rhino, Action -> defaussee, 3 degats",
       "« Attach to an enemy. Hero Action (attack): Discard this card -> deal 3 damage to attached enemy » ; Daredevil (heros) + Elektra (allie 60007)",
       [DD_HEROS, *en_jeu("60007")], [], {"degats": [["01094", 3]], "hors_jeu": ["63027"]},
       heros="daredevil", main_exclusive=["63027", "01090"], jouer=["63027"], cibles=["01094"],
       declencher_apres=["Puzzle.Action('63027', 'HeroAction')"]),
    _c("63027 Dance with the Devil : CONTRE-CAS sans Elektra en jeu, la carte n'est pas jouable (Team-Up)",
       "le Team-Up exige les DEUX personnages nommes", [DD_HEROS], [], {"jouable": [["63027", False]]},
       heros="daredevil", main_exclusive=["63027", "01090"], verifier="if_jouable"),
]
