# Cas test_capacites : « Discard this card and remove it from the campaign log » (Tactical Scanner 04155-04158, Hydra Campaign).
# Noms « [campagne_retraits] ». Le cout `CostFunc.RemoveFromCampaignLog` ne faisait RIEN avant le 14/11/2026 : le carnet gardait la
# carte et le mode campagne la remettait au scenario suivant. Il efface maintenant la cle du carnet du joueur qui la porte, dans le
# monde, et la note dans `Campaign Log Keys Removed` (lue par le descripteur : `campagne_retraits`).
# Verts avec le correctif, rouges sans (cles absentes / valeur inchangee).
SC = "thanos"
HEROS = "Puzzle.ChangeForm('01001b')"


def _c(nom, pourquoi, carte, carnet, attendu, **cle):
    cas = {"nom": "[campagne_retraits] " + nom, "pourquoi": pourquoi, "scenario": SC, "heros": "spider_man",
           # 04155 (« ready your hero and heal 5 ») n'offre son action que si le heros est incline ET blesse.
           "mise_en_place": [HEROS, f"Puzzle.PutIntoPlay('{carte}')", "Puzzle.Damage('01001b', 3)", "Puzzle.Exhaust('01001b')"],
           "main_exclusive": ["01092"],
           "declencher": [f"Puzzle.Action('{carte}', 'HeroAction')"], "verifier": "campagne_retraits_monde",
           "carnet": carnet, "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    _c(f"{carte} {nom} : la Hero Action retire la carte du carnet (« Player 1 Tech Upgrade » vide)",
       "« remove it from the campaign log » : sans cela la carte revient au scenario suivant",
       carte, {"Player 1 Tech Upgrade": carte},
       {"cles": {"Player 1 Tech Upgrade": "", "Campaign Log Keys Removed": "Player 1 Tech Upgrade"}, "retraits": ["Player 1 Tech Upgrade"]},
       accepter_choix=True)
    for carte, nom in (("04155", "Tactical Scanner (soin)"), ("04156", "Tactical Scanner (pioche)"),
                       ("04157", "Tactical Scanner (allie)"), ("04158", "Tactical Scanner (degats)"))
] + [
    _c("04156 Tactical Scanner : une AUTRE cle du carnet (Basic Upgrade) n'est pas touchee",
       "seule la cle qui porte CETTE carte est retiree",
       "04156", {"Player 1 Tech Upgrade": "04156", "Player 1 Basic Upgrade": "04160a"},
       {"cles": {"Player 1 Tech Upgrade": "", "Player 1 Basic Upgrade": "04160a"}, "retraits": ["Player 1 Tech Upgrade"]}),
    _c("04156 Tactical Scanner : le carnet porte une AUTRE carte (04155) pour ce joueur -> rien n'est retire",
       "la cle n'est retiree que si elle porte la carte utilisee",
       "04156", {"Player 1 Tech Upgrade": "04155"},
       {"cles": {"Player 1 Tech Upgrade": "04155"}, "retraits": []}),
    _c("04156 Tactical Scanner : partie sans carnet -> aucune erreur, rien de retire",
       "une partie hors campagne (pas de cle) joue la carte comme avant",
       "04156", {},
       {"cles": {}, "retraits": []}),
]

VERIFICATIONS = r'''
def campagne_retraits_monde(monde, aides):
    """Le carnet DU MONDE apres la Hero Action : cles lues dans `monde.store` (`attendu["cles"]`), liste que le descripteur
    transmet au panneau de fin de scenario (`attendu["retraits"]`)."""
    attendu = aides["cas"].get("attendu") or {}
    store = monde.store
    soucis = []
    for cle, valeur in (attendu.get("cles") or {}).items():
        lu = store.GetStr(cle) if store.HasKey(cle) else ""
        if lu != valeur:
            soucis.append(f"{cle} = {lu!r} (attendu {valeur!r})")
    retraits = [x for x in (store.GetStr("Campaign Log Keys Removed") if store.HasKey("Campaign Log Keys Removed") else "").split(";") if x]
    if retraits != (attendu.get("retraits") or []):
        soucis.append(f"retraits = {retraits} (attendu {attendu.get('retraits')})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"carnet du monde ok : retraits={retraits}"
'''
