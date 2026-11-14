# Cas test_capacites du SET NEMESIS d'ELEKTRA (Hero Pack MC63, set « Elektra Nemesis », 63029-63033), noms prefixes
# « [elektra_nem] ». Un cas par capacite, le card_id est dans le nom. Gabarits : docs/packs/elektra_heros.md.
# Scripts : src/cards/pack/elektra/elektra_nemesis/. L'obligation 63028 n'est PAS montee (pas de scan officiel, 14/11/2026).
#
# Montage : vilain Rhino 01094 (14 PV, ATQ 2) ; Elektra en HEROS. Le deck rencontre est remplace par des 01105 (0 icone de boost).
# ⚠ `attributs_carte` attend un ECART par rapport a l'imprime, pas une valeur absolue.
# USAGI up041 : allie 3 PV, Retaliate 2 (temoin de ranged, comme tools/cas/capos.py).
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('63001b', '63001a')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
USAGI = "up041"
SANS_DEFENSE = {"passer_sur_option": "Defense"}
# Le set nemesis est MIS DE COTE en debut de partie : sans ce retrait, le harnais retrouve l'exemplaire mis de cote d'Aka
# au lieu de celui qu'il vient de poser (meme precaution que tools/cas/carnage.py).
SANS_NEMESIS = "Puzzle.RemoveNemesisAside()"


def pose(*ids):
    return ["Puzzle.PutIntoPlay('%s')" % i for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[elektra_nem] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "elektra"), "mise_en_place": SANS_BOOST + [HEROS] + list(mise),
           "declencher": declencher, "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ===================================================================== 63029 Aka
    _c("63029 Aka : vaincu -> il est melange dans le paquet de rencontre (pas la defausse)",
       "When Defeated : la carte retourne dans le paquet de rencontre",
       [SANS_NEMESIS] + pose("63029"), ["Puzzle.Damage('63029', 99)"], {"hors_jeu": ["63029"], "dans_deck_rencontre": ["63029"]}),
    _c("63029 Aka : retourne comme carte de boost -> il est distribue face cachee au joueur Elektra",
       "[star] Boost : la carte elle-meme est distribuee au joueur Elektra Natchios",
       [SANS_NEMESIS], ["Puzzle.Boost('63029')"], {"distribuees": 1}, verifier="ares_cartes_rencontre_distribuees", **SANS_DEFENSE),
    _c("63029 Aka : Quickstrike imprime (desc) et profil 4 PV / ATQ 2 / MAN 2",
       "mot-cle natif lu dans data/cards.json",
       [SANS_NEMESIS] + pose("63029"), [], {"en_jeu": ["63029"], "attributs_carte": [["63029", "attack", 0], ["63029", "scheme", 0]]}),

    # ===================================================================== 63030 The Fist Fits in the Hand
    _c("63030 The Fist Fits in the Hand : Hand Archer (ATQ 1, MAN 1) passe a ATQ 2 / MAN 2",
       "chaque sbire HAND gagne +1 MAN et +1 ATQ tant que la manigance est en jeu",
       pose("63033", "63030"), [], {"attributs_carte": [["63033", "attack", 1], ["63033", "scheme", 1]]}),
    _c("63030 TEMOIN : sans la manigance, Hand Archer reste a ATQ 1 / MAN 1",
       "temoin du cas precedent",
       pose("63033"), [], {"attributs_carte": [["63033", "attack", 0], ["63033", "scheme", 0]]}),
    _c("63030 The Fist Fits in the Hand : un sbire SANS le trait HAND (01101) ne gagne rien",
       "le bonus ne vise que le trait HAND",
       pose("01101", "63030"), [], {"attributs_carte": [["01101", "attack", 0], ["01101", "scheme", 0]]}),
    _c("63030 The Fist Fits in the Hand : icone Hazard imprimee",
       "icone lue dans data/cards.json", pose("63030"), [], {"en_jeu": ["63030"], "icones": [["Hazard", 1]]}),

    # ===================================================================== 63031 Hand Katana
    _c("63031 Hand Katana : Aka (4 PV) et Hand Archer (3 PV) en jeu -> s'attache a Aka, qui passe a ATQ 4",
       "attache au sbire HAND aux PV de base les plus eleves ; +2 ATQ",
       [SANS_NEMESIS] + pose("63033", "63029", "63031"), [], {"accroche_a": [["63031", "63029"]], "attributs_carte": [["63029", "attack", 2], ["63033", "attack", 0]]}),
    _c("63031 Hand Katana : aucun sbire HAND -> s'attache au mechant (Rhino ATQ 2 -> 4)",
       "sinon, attache au mechant",
       pose("63031"), [], {"accroche_a": [["63031", "01094"]], "attributs_carte": [["01094", "attack", 2]]}),
    _c("63031 Hand Katana : Hero Action, 2 ressources depensees -> la carte est defaussee",
       "Hero Action : depenser 2 ressources de n'importe quel type -> defausser cette carte",
       pose("63031"), [], {"hors_jeu": ["63031"], "attributs_carte": [["01094", "attack", 0]]},
       main_exclusive=["01090"], declencher_apres=["Puzzle.Action('63031', 'HeroAction')"]),

    # ===================================================================== 63032 Hand Blademaster
    _c("63032 Hand Blademaster : seul sbire HAND -> ATQ 1 / MAN 1",
       "pas d'AUTRE sbire HAND : aucun bonus (lui-meme ne compte pas)",
       pose("63032"), [], {"attributs_carte": [["63032", "attack", 0], ["63032", "scheme", 0]]}),
    _c("63032 Hand Blademaster : un autre sbire HAND (Hand Archer) en jeu -> ATQ 2 / MAN 2",
       "+1 MAN et +1 ATQ s'il y a un autre sbire HAND en jeu",
       pose("63032", "63033"), [], {"attributs_carte": [["63032", "attack", 1], ["63032", "scheme", 1]]}),
    _c("63032 Hand Blademaster : l'autre sbire HAND quitte le jeu -> retour a ATQ 1 / MAN 1",
       "le bonus suit la presence de l'autre sbire",
       pose("63032", "63033"), ["Puzzle.Damage('63033', 99)"], {"attributs_carte": [["63032", "attack", 0], ["63032", "scheme", 0]]}),
    _c("63032 Hand Blademaster : vaincu -> melange dans le paquet de rencontre",
       "When Defeated", pose("63032"), ["Puzzle.Damage('63032', 99)"], {"hors_jeu": ["63032"], "dans_deck_rencontre": ["63032"]}),

    # ===================================================================== 63033 Hand Archer
    _c("63033 Hand Archer : attaque RANGED sur Usagi (Retaliate 2) -> l'archer ne subit aucune riposte",
       "ses attaques gagnent ranged : la riposte est ignoree",
       pose("63033") + ["Puzzle.PutIntoPlay('%s', under_control=True)" % USAGI],
       ["Puzzle.EnemyAttacks('63033', '%s')" % USAGI], {"degats": [["63033", 0]]}, **SANS_DEFENSE),
    _c("63032 TEMOIN de ranged : Hand Blademaster attaque Usagi (Retaliate 2) -> il subit 2 de riposte",
       "temoin : sans ranged la riposte s'applique",
       pose("63032") + ["Puzzle.PutIntoPlay('%s', under_control=True)" % USAGI],
       ["Puzzle.EnemyAttacks('63032', '%s')" % USAGI], {"degats": [["63032", 2]]}, **SANS_DEFENSE),
    _c("63033 Hand Archer : vaincu -> melange dans le paquet de rencontre",
       "When Defeated", pose("63033"), ["Puzzle.Damage('63033', 99)"], {"hors_jeu": ["63033"], "dans_deck_rencontre": ["63033"]}),
    _c("63029 Aka EN JEU : une autre carte de boost est retournee (Elektra defend son attaque Quickstrike) -> Aka reste en jeu",
       "le [star] Boost ne vaut que lorsque Aka EST la carte de boost retournee ; rouge sans la condition `message.trigger == effect.this`",
       [SANS_NEMESIS] + pose("63029"), [], {"en_jeu": ["63029"]}, verifier="ares_cartes_rencontre_distribuees"),
]
