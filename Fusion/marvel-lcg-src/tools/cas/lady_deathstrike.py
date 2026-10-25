# Cas test_capacites du scenario custom LADY DEATHSTRIKE (Mysteltainn, prefixe `ld`) : noms prefixes « [ld] » puis le card_id
# (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - scenario `lady_deathstrike` (standard : stades I et II) ou `lady_deathstrike_expert` (II et III) ; heros `spider_man` (01001a/b) ;
#  - le Setup de ld004a attache UNE copie de Bleeding Out (ld005) a l'identite de chaque joueur avec 3 compteurs `bleed` ;
#  - `player_deck` du heros est complete par le harnais (ressources inertes 01088-01090) ; `main_exclusive` fixe la main ;
#  - la partie commence en ALTER-EGO ; `HEROS` passe en forme heros ;
#  - `SANS_BOOST` remplace le deck de rencontre par des cartes sans icone boost (sinon le boost de l'attaque change les degats) ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ; 01005 Swinging Web Kick, 01006... sont des cartes SIGNATURE
#    de Spider-Man (classe Hero = « identity-specific »).
SC = "lady_deathstrike"
SCX = "lady_deathstrike_expert"
HEROS = "Puzzle.ChangeToFace('01001b', '01001a')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
VIDER_DEFAUSSE = "Puzzle.EmptyPlayerDiscardPile()"
BO = "ld005"
VILAIN = "ld001"
COMPLOT = "ld004b"
# Un deck de 6 cartes de ressources (aucune carte d'identite) et un deck dont les 4 premieres sont des signatures Spider-Man.
DECK_BASIQUE = "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089', '01089')"
DECK_HEROS = "Puzzle.CreatePlayerDeck('01089', '01089', '01005', '01005', '01005', '01005')"   # le DERNIER est le dessus


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[ld] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "ld_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    _c("ld004a Setup : chaque joueur a SA copie de Bleeding Out attachee a l'identite avec 3 compteurs bleed",
       "« Attach a copy of Bleeding Out to each player ... Place 3 bleed counters on each copy »",
       [], [], {"compteurs": [[BO, "bleed", 3]], "accroche_a": [[BO, "01001b"]]}, main_exclusive=["01090"], avec_boost=True),
]


VERIFICATIONS = r'''
def ld_etat(monde, aides):
    """Cles propres : `stat` ([[card_id, "attack"|"thwart"|"defense", n]]), `jetons_complot` (nb de jetons d'acceleration sur ld004b),
    `menace_cible` (menace cible imprimee de ld004b) ; le reste va a `etat_attendu`."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    for card_id, nom, valeur in attendu.get("stat") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (stat)")
        elif getattr(face, nom, None) != valeur:
            soucis.append(f"{nom} de {card_id} = {getattr(face, nom, None)} (attendu {valeur})")
    propres = ("stat",)
    cas["attendu"] = {k: v for k, v in attendu.items() if k not in propres}
    try:
        if cas["attendu"]:
            ok, msg = etat_attendu(monde, aides)
            if not ok:
                soucis.append(msg)
    finally:
        cas["attendu"] = attendu
    return (False, " ; ".join(soucis)) if soucis else (True, "Lady Deathstrike conforme")
'''
