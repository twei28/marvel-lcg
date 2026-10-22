# (Bastion et non Nimrod : Nimrod ne peut pas prendre plus de 3 degats par phase ; Toughness = deux coups.)
# Cas test_capacites des 4 DEFIS MC×DC 2026 (PU-11, 22/10/2026) : pu279 Rise of the Machines, pu280 Secret Agent, pu281 It's a Trap!, pu282 Angry Birds. Prefixe `[defi]`.
# Cle `defis` du harnais : la carte `Challenge` mise en jeu comme le lanceur le fait (`scene.campaign.SetChallenge`). Chaque regle a son TEMOIN sans defi (meme
# montage, cle `defis` absente) : la regle seule fait la difference. Verificateur : `defi_etat`.
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]


def _d(nom, pourquoi, scenario, defi, mise, declencher, attendu, **cle):
    cas = {"nom": "[defi] " + nom, "pourquoi": pourquoi, "scenario": scenario, "heros": "spider_man",
           "mise_en_place": [*RIEN, FORME_HEROS, *mise], "declencher": declencher, "verifier": "defi_etat", "attendu": attendu,
           "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    if defi:
        cas["defis"] = [defi]
    cas.update(cle)
    return cas


M279 = "rise_of_the_machines"
M280 = "secret_agent"
M281 = "its_a_trap"
M282 = "angry_birds"
HAYMAKER = dict(main_exclusive=["01087", "01089"], jouer=["01087"], cibles=["01130"])   # Haymaker : cout 2, ressource imprimee ENERGIE, 3 degats

CAS = [
    _d("pu280 : la carte Challenge est en jeu", "SetChallenge met la carte en jeu", M280, "pu280", [], [], {"en_jeu": ["pu280"]}),
    # ------------------------------------------------------------------------------------------------------------ pu279
    _d("pu279 : Haymaker (energie imprimee, 3 degats) inflige 4 a Whirlwind", "« Cards with a printed [energy] deal 1 additional damage » : 3 + 1", M279, "pu279",
       ["Puzzle.PutIntoPlay('01130')"], [], {"degats": [["01130", 4]], "defausse": ["01087"]}, **HAYMAKER),
    _d("pu279, TEMOIN : meme Haymaker sans le defi -> 3 degats", "la regle seule ajoute le degat", "vision_pvp", None,
       ["Puzzle.PutIntoPlay('01130')"], [], {"degats": [["01130", 3]], "defausse": ["01087"]}, **HAYMAKER),
    _d("pu279, TEMOIN : l'attaque de base du heros (pas une carte a energie imprimee) reste a 2 degats", "l'identite n'est pas une carte a ressource imprimee", M279, "pu279",
       ["Puzzle.PutIntoPlay('01130')"], ["Puzzle.Attack('01001a')"], {"degats": [["01130", 2]]}, cibles=["01130"]),
    _d("pu279 : Bastion (Future Past, Victory 1) vaincu NE va PAS en pile de victoire", "« All Future Past cards lose victory 1 »", M279, "pu279",
       ["Puzzle.PutIntoPlay('32167')"], ["Puzzle.Damage('32167', 99)", "Puzzle.Damage('32167', 99)"], {"victoire_sans": ["32167"], "hors_jeu": ["32167"]}),
    _d("pu279, TEMOIN : sans le defi, Bastion vaincu va en pile de victoire", "la perte de Victory vient du defi", "vision_pvp", None,
       ["Puzzle.PutIntoPlay('32167')"], ["Puzzle.Damage('32167', 99)", "Puzzle.Damage('32167', 99)"], {"victoire_contient": ["32167"]}),
    _d("pu279 : quand le stade du vilain avance, le complot avance a 2A", "« When the villain stage advances, advance the main scheme to 2A »", M279, "pu279",
       [], ["Puzzle.AdvanceVillain()"], {"complots_stade": 2}),
    _d("pu279, TEMOIN : sans le defi, le complot reste au stade 1", "TEMOIN", "vision_pvp", None, [], ["Puzzle.AdvanceVillain()"], {"complots_stade": 1}),
    # ------------------------------------------------------------------------------------------------------------ pu280
    _d("pu280 : Captain America gagne le trait HYDRA", "« Captain America gains the HYDRA trait »", M280, "pu280", [], [], {"traits_de": [["56137", "HYDRA"]]}),
    _d("pu280, TEMOIN : sans le defi, pas de trait HYDRA", "TEMOIN", "captain_america", None, [], [], {"sans_trait": [["56137", "HYDRA"]]}),
    _d("pu280 : un sbire HYDRA (Hydra Mercenary) gagne Rapide", "« All HYDRA minions gain quickstrike »", M280, "pu280",
       ["Puzzle.PutIntoPlay('01101')"], [], {"mots_cles": [["01101", "Quickstrike", 1]]}),
    _d("pu280, TEMOIN : un sbire NON HYDRA (Shocker) n'a pas Rapide", "TEMOIN de portee", M280, "pu280",
       ["Puzzle.PutIntoPlay('01103')"], [], {"mots_cles": [["01103", "Quickstrike", 0]]}),
    _d("pu280, TEMOIN : sans le defi, Hydra Mercenary n'a pas Rapide", "TEMOIN", "captain_america", None, ["Puzzle.PutIntoPlay('01101')"], [], {"mots_cles": [["01101", "Quickstrike", 0]]}),
    _d("pu280 : quand le stade du vilain avance, le complot avance a 2A", "« advance the main scheme to 2A »", M280, "pu280", [], ["Puzzle.AdvanceVillain()"], {"complots_stade": 2}),
    # ------------------------------------------------------------------------------------------------------------ pu281
    _d("pu281 : une annexe de rencontre (Breakin' & Takin') gagne incite 1, crise et acceleration", "« All encounter side schemes gain incite 1, [crisis] and [acceleration] »",
       M281, "pu281", ["Puzzle.PutIntoPlay('01107')"], [], {"mots_cles": [["01107", "Incite", 1], ["01107", "Crisis", 1], ["01107", "Acceleration", 1]]}),
    _d("pu281, TEMOIN : sans le defi, aucune des trois icones", "TEMOIN", "en_sabah_nur", None, ["Puzzle.PutIntoPlay('01107')"], [],
       {"mots_cles": [["01107", "Incite", 0], ["01107", "Crisis", 0], ["01107", "Acceleration", 0]]}),
    _d("pu281 : le vilain gagne Stable (steady)", "« The villain gains steady »", M281, "pu281", [], [], {"mots_cles": [["45184a", "Steady", 1]]}),
    _d("pu281, TEMOIN : sans le defi, le vilain n'est pas stable", "TEMOIN", "en_sabah_nur", None, [], [], {"mots_cles": [["45184a", "Steady", 0]]}),
    _d("pu281 : quand le stade du vilain avance, le complot avance a 2A", "« advance the main scheme to 2A »", M281, "pu281", [], ["Puzzle.AdvanceVillain()"], {"complots_stade": 2}),
    # ------------------------------------------------------------------------------------------------------------ pu282
    {"nom": "[defi] pu282 : un Blue Bird (Storm) a son amelioration AERIAL (Eyes in the Sky, ajoutee au deck) en jeu et 2 cartes de moins en main de depart",
     "pourquoi": "« Blue birds begin the game with their AERIAL upgrade in play, but -2 hand size for their opening hand »", "scenario": M282, "heros": "storm",
     "defis": ["pu282"], "deck_ajoute": ["42030"], "mise_en_place": [], "declencher": [], "verifier": "defi_etat", "main_exclusive": None,
     "attendu": {"en_jeu": ["42030"], "taille_main": 4, "attributs": {"hand_size": 0}}},
    {"nom": "[defi] pu282, TEMOIN : un Red Bird (Falcon) n'a rien en jeu et sa main de depart est complete", "pourquoi": "les Red Birds n'ont ni l'AERIAL ni le malus",
     "scenario": M282, "heros": "falcon", "defis": ["pu282"], "deck_ajoute": ["42030"], "mise_en_place": [], "declencher": [], "verifier": "defi_etat",
     "main_exclusive": None, "attendu": {"hors_jeu": ["42030"], "taille_main": 6}},
    {"nom": "[defi] pu282, TEMOIN : sans le defi, Storm n'a pas l'AERIAL en jeu et une main complete", "pourquoi": "TEMOIN",
     "scenario": "the_tower_defense", "heros": "storm", "deck_ajoute": ["42030"], "mise_en_place": [], "declencher": [], "verifier": "defi_etat",
     "main_exclusive": None, "attendu": {"hors_jeu": ["42030"], "taille_main": 6}},
    _d("pu282 : l'action de l'allie (Black Widow) : elle est defaussee, 1 degat a Avengers Tower et 4 au vilain actif",
       "« Action: Discard this ally -> deal 1 damage to Avenger's Tower and 4 damage to the villain »", M282, "pu282",
       ["Puzzle.PutIntoPlay('21100a')", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Action('01075', 'Action')"],
       {"defausse": ["01075"], "degats": [["21095", 4]], "compteurs_n": [["21100a", "damage", 2]]}),   # la Tour a DEJA 1 compteur de degats avant l'action (voir le temoin) : 1 + 1
    _d("pu282, TEMOIN : sans l'action, Avengers Tower n'a que son compteur de depart et le vilain actif aucun degat", "base de mesure du cas precedent", M282, "pu282",
       ["Puzzle.PutIntoPlay('21100a')", "Puzzle.PutIntoPlay('01075', under_control=True)"], [], {"compteurs_n": [["21100a", "damage", 1]], "degats": [["21095", 0]]}),
]

VERIFICATIONS = r'''
def defi_etat(monde, aides):
    from game.operate.worlds import Worlds
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    victoire = sorted(str(getattr(f.paper, "card_id", "")) for f in monde.victory_display.Get(True))
    for i in attendu.get("victoire_contient") or []:
        if i not in victoire:
            soucis.append(f"{i} absente de la pile de victoire {victoire}")
    for i in attendu.get("victoire_sans") or []:
        if i in victoire:
            soucis.append(f"{i} presente dans la pile de victoire")
    if "complots_stade" in attendu:
        stades = [str(f.paper.desc.get("Stage", "")) if hasattr(f.paper, "desc") else "?" for f in Worlds.GetAllMainSchemes(monde)]
        ids = [str(f.paper.card_id) for f in Worlds.GetAllMainSchemes(monde)]
        chiffres = {s[:1] for s in stades}
        if chiffres != {str(attendu["complots_stade"])}:
            soucis.append(f"complots en jeu {ids} stades {stades} (attendu stade {attendu['complots_stade']})")
    for i, cle, valeur in attendu.get("mots_cles") or []:
        face = aides["par_id"](monde, i)
        if face is None:
            soucis.append(f"{i} introuvable en jeu")
        elif face.GetKeyword(cle) != valeur:
            soucis.append(f"{i} {cle} = {face.GetKeyword(cle)} (attendu {valeur})")
    for i, trait in attendu.get("sans_trait") or []:
        face = aides["par_id"](monde, i)
        if face is None:
            soucis.append(f"{i} introuvable en jeu")
        elif face.HasTrait(trait):
            soucis.append(f"{i} a le trait {trait} (ne devrait pas)")
    for i, nom, n in attendu.get("compteurs_n") or []:
        face = aides["par_id"](monde, i)
        if face is None:
            soucis.append(f"{i} introuvable en jeu")
        elif face.GetCounters(nom) != n:
            soucis.append(f"{i} a {face.GetCounters(nom)} compteur(s) {nom} (attendu {n})")
    propres = {"compteurs_n", "victoire_contient", "victoire_sans", "complots_stade", "mots_cles", "sans_trait"}
    reste = {k: v for k, v in attendu.items() if k not in propres}
    if reste:
        cas["attendu"] = reste
        try:
            ok, msg = etat_attendu(monde, aides)
        finally:
            cas["attendu"] = attendu
        if not ok:
            soucis.append(msg)
    return (False, " ; ".join(soucis)) if soucis else (True, "defi conforme")
'''
