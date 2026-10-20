# Cas test_capacites du modulaire ACCUSER CORPS de Galactic Storm (gs156-gs160), lot GS-6 (20/10/2026).
# Format identique a tools/cas/hala_ultimatum.py ; filtre `[ac]`. Modulaire seul, scenario de test
# `gs_hala_ultimatum` (meme pack) pour disposer d'un mechant en jeu.
SC = "gs_hala_ultimatum"
HEROS = "Puzzle.ChangeForm('01001b')"
DECK_NEUTRE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', '01186', '01186', '01186')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[ac] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    _c("gs156 Forced Interrupt : un ennemi qui attaque le joueur porteur gagne +1 ATK pour cette attaque",
       "« When an enemy initiates an attack against the attached identity, that enemy gets +1 ATK for that "
       "attack » : WhenUnitWouldAttack + GainATKForThisAttack (modele OFFICIEL cw 56017 Savage Strike)",
       DECK_NEUTRE + ["Puzzle.Flip('gs138a')", HEROS, "Puzzle.PutIntoPlay('gs156')"],
       ["Puzzle.Attack('gs138b')"], {"degats_identite": 3}),
    _c("gs156 Forced Interrupt, TEMOIN : sans The Accused en jeu, la meme attaque n'inflige que l'ATQ de "
       "base (2)",
       "temoin : le bonus +1 vient bien de la carte",
       DECK_NEUTRE + ["Puzzle.Flip('gs138a')", HEROS], ["Puzzle.Attack('gs138b')"], {"degats_identite": 2}),
    _c("gs156 Forced Response : un ennemi ACCUSER CORPS est vaincu -> The Accused se defausse",
       "« After an ACCUSER CORPS enemy is defeated, discard this card »",
       ["Puzzle.PutIntoPlay('gs156')", "Puzzle.PutIntoPlay('gs159')"], ["Puzzle.Damage('gs159', 10)"],
       {"hors_jeu": ["gs156"]}),
    _c("gs156 Forced Response, TEMOIN : un ennemi SANS le trait ACCUSER CORPS vaincu -> The Accused reste",
       "temoin : seul le trait declenche la defausse",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs156')", "Puzzle.PutIntoPlay('01103')"],
       ["Puzzle.Damage('01103', 10)"], {"en_jeu": ["gs156"]}),
    _c("gs157 Hero Action : 2 degats sur l'identite et 1 carte de rencontre distribuee -> melangee dans le "
       "deck rencontre",
       "« Take 2 damage and deal yourself 1 facedown encounter card -> shuffle this card into the "
       "encounter deck »",
       ["Puzzle.PutIntoPlay('gs157')", HEROS], ["Puzzle.Action('gs157')"],
       {"hors_jeu": ["gs157"], "degats_identite": 2}, verifier="ac_etat"),
    _c("gs158 Forced Response : l'ennemi porteur attaque et blesse un personnage -> Unwavering se "
       "defausse",
       "« After attached enemy attacks and damages a character, discard this card »",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('01103')", "Puzzle.AttachReel('gs158', '01103')", HEROS],
       ["Puzzle.Attack('01103')"], {"hors_jeu": ["gs158"]}),
    _c("gs159 Kree Accuser : Toughness + Villainous (base native)",
       "desc.Toughness, desc.Villainous ; fiches mots-cles/toughness.md, villainous.md",
       ["Puzzle.PutIntoPlay('gs159')"], ["Puzzle.Damage('gs159', 1)"], {"degats": [["gs159", 0]]}),
    _c("gs160 When Revealed : un ennemi ACCUSER CORPS en jeu -> il s'active contre le joueur",
       "« Each ACCUSER CORPS enemy activates against you »",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs159')", HEROS], ["Puzzle.Reveal('gs160')"],
       {"degats_identite": 2}),
    _c("gs160 When Revealed : AUCUN ennemi ACCUSER CORPS en jeu -> cherche et revele un Kree Accuser",
       "« If no enemy activated this way, search the encounter deck and discard pile for a Kree Accuser "
       "and reveal it »",
       DECK_NEUTRE + ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('gs159', '01186')"],
       ["Puzzle.Reveal('gs160')"], {"en_jeu": ["gs159"]}),
]

VERIFICATIONS = r'''
def ac_etat(monde, aides):
    """etat_attendu + dans_deck_rencontre_n [[card_id, n]] (Universal Weapon qui se remelange)."""
    attendu = aides["cas"].get("attendu") or {}
    connues = set(CLES_ETAT_ATTENDU) | {"dans_deck_rencontre_n"}
    inconnues = sorted(set(attendu) - connues)
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de ac_etat : {inconnues}"
    ok, message = etat_attendu(monde, aides)
    soucis = [] if ok else [message]
    for card_id, n in attendu.get("dans_deck_rencontre_n") or []:
        from game.operate.worlds import Worlds
        reel = sum(1 for f in Worlds.GetEncounterDeckCards(monde) if getattr(f.paper, "card_id", None) == card_id)
        if reel != n:
            soucis.append(f"{card_id} dans le deck rencontre = {reel} (attendu {n})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "ok"
'''
