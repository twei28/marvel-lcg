# Cas test_capacites de l'OBLIGATION et du SET NEMESIS d'IRON FIST (Hero Pack MC64EN : 64026 Lack of Chi, 64027 Davos,
# 64028 Crane Daughter x3, 64029 Steel Serpent), noms prefixes « [iron_fist_nem] ». Un cas par capacite, le card_id est
# dans le nom. Gabarits : docs/packs/iron_fist_cartes.md. Scripts : src/cards/pack/iron_fist/iron_fist_nemesis/.
#
# Montage : vilain Rhino 01094 (14 PV, ATQ 2) ; Iron Fist en HEROS (PV 10, DEF 2). Deck rencontre = des 01105 (0 boost).
# Le set nemesis (Davos, 3 Crane Daughter, Steel Serpent) est MIS DE COTE au depart : `Puzzle.Reveal('64027')` revele
# donc le Davos mis de cote et « find » y trouve les 3 Crane Daughter. SANS_NEMESIS vide cette zone pour les cas sans elles.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('64001b', '64001a')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
SANS_DEFENSE = {"passer_sur_option": "Defense"}
SANS_NEMESIS = "Puzzle.RemoveNemesisAside()"
DAVOS_REVELE = "Puzzle.Reveal('64027')"
DAVOS_ATTAQUE = "Puzzle.EnemyAttacks('64027', '64001a')"


def chi(face, n):
    return f"Puzzle.Counter('{face}', 'chi', {n})"


def pose(*ids):
    return ["Puzzle.PutIntoPlay('%s')" % i for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[iron_fist_nem] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "iron_fist"), "mise_en_place": SANS_BOOST + [HEROS] + list(mise),
           "declencher": declencher, "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ===================================================================== 64026 Lack of Chi
    _c("64026 Lack of Chi : revelee avec 3 chi sur Iron Fist -> les 3 chi passent sur l'obligation",
       "When Revealed : Move all chi counters from your identity to this card",
       [chi("64001a", 3)], ["Puzzle.Reveal('64026')"],
       {"compteurs": [["64026", "chi", 3]], "compteurs_identite": [["chi", 0]]}),
    _c("64026 Lack of Chi : en jeu avec 1 chi, un chi pose sur Iron Fist est detourne ici (2 ici, 0 sur Iron Fist)",
       "Forced Interrupt : place it here instead",
       [chi("64001a", 1), "Puzzle.Reveal('64026')"], [chi("64001a", 1)],
       {"compteurs": [["64026", "chi", 2]], "compteurs_identite": [["chi", 0]]}),
    _c("64026 Lack of Chi : 3 chi ici, le 4e detourne -> l'obligation est defaussee",
       "If there are at least 4 chi counters here, discard this card",
       [chi("64001a", 3), "Puzzle.Reveal('64026')"], [chi("64001a", 1)],
       {"hors_jeu": ["64026"], "compteurs_identite": [["chi", 0]]}),
    _c("64026 Lack of Chi : revelee avec 4 chi -> elle RESTE (le seuil ne se lit qu'apres un chi detourne)",
       "la phrase « at least 4 » appartient a l'Interruption forcee, pas au When Revealed",
       [chi("64001a", 4)], ["Puzzle.Reveal('64026')"],
       {"compteurs": [["64026", "chi", 4]], "compteurs_identite": [["chi", 0]]}),
    _c("64026 TEMOIN : sans l'obligation, un chi pose sur Iron Fist y reste",
       "temoin des cas precedents", [], [chi("64001a", 1)], {"compteurs_identite": [["chi", 1]]}),
    _c("64026 Lack of Chi : apres sa defausse, Iron Fist reprend ses chi normalement",
       "l'obligation defaussee ne detourne plus rien",
       [chi("64001a", 3), "Puzzle.Reveal('64026')"], [chi("64001a", 1), chi("64001a", 2)],
       {"hors_jeu": ["64026"], "compteurs_identite": [["chi", 2]]}),

    # ===================================================================== 64027 Davos
    _c("64027 Davos : revele -> les 3 Crane Daughter mises de cote sont glissees sous lui",
       "When Revealed : Find and tuck the 3 Crane Daughter minions under here",
       [], [DAVOS_REVELE], {"en_jeu": ["64027"], "taille_pose_sous": [["64027", 3]]}),
    _c("64027 Davos : find fouille aussi le deck et la defausse de rencontre (2 dans le deck, 1 en defausse -> 3 dessous)",
       "Rules Reference 1.8 p.19 FIND : toute zone ou la carte peut se trouver",
       [SANS_NEMESIS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '64028', '01105', '64028', '01105')",
        "Puzzle.CreateEncounterDiscardPile('64028')"], [DAVOS_REVELE],
       {"en_jeu": ["64027"], "taille_pose_sous": [["64027", 3]]}),
    _c("64027 Davos : find prend aussi une Crane Daughter EN JEU (elle quitte le jeu, glissee dessous)",
       "Rules Reference 1.8 p.19 FIND : la zone de jeu est fouillee",
       [SANS_NEMESIS] + pose("64028"), [DAVOS_REVELE],
       {"en_jeu": ["64027"], "hors_jeu": ["64028"], "taille_pose_sous": [["64027", 1]]}),
    _c("64027 Davos : 3 Crane Daughter dessous, 4 degats -> aucun degat, une Crane Daughter melangee dans le deck",
       "Forced Interrupt : shuffle a tucked Crane Daughter into the encounter deck instead",
       [DAVOS_REVELE], ["Puzzle.Damage('64027', 4)"],
       {"en_jeu": ["64027"], "degats": [["64027", 0]], "taille_pose_sous": [["64027", 2]], "dans_deck_rencontre": ["64028"]}),
    _c("64027 Davos : Iron Fist l'attaque (ATQ 2) -> 0 degat, 2 Crane Daughter restent dessous",
       "any amount of damage, attaque comprise",
       [DAVOS_REVELE], ["Puzzle.Attack('64001a')"],
       {"degats": [["64027", 0]], "taille_pose_sous": [["64027", 2]]}, cibles=["64027"]),
    _c("64027 TEMOIN : sans Crane Daughter dessous, Davos prend les degats (2)",
       "rien a melanger : pas de remplacement",
       [SANS_NEMESIS] + pose("64027"), ["Puzzle.Damage('64027', 2)"], {"degats": [["64027", 2]]}),

    # ===================================================================== 64028 Crane Daughter
    _c("64028 Crane Daughter : vaincue -> melangee dans le deck de rencontre",
       "When Defeated : Shuffle Crane Daughter into the encounter deck",
       [SANS_NEMESIS] + pose("64028"), ["Puzzle.Damage('64028', 99)"], {"hors_jeu": ["64028"], "dans_deck_rencontre": ["64028"]}),
    _c("64028 Crane Daughter : retournee en boost avec Davos en jeu -> glissee sous Davos apres l'activation",
       "[star] Boost : After this activation, tuck this card under Davos",
       [SANS_NEMESIS] + pose("64027"), ["Puzzle.Boost('64028')"], {"taille_pose_sous": [["64027", 1]]}, **SANS_DEFENSE),
    _c("64028 Crane Daughter : retournee en boost SANS Davos -> defaussee comme une carte de boost ordinaire",
       "pas de Davos en jeu : rien a faire",
       [SANS_NEMESIS], ["Puzzle.Boost('64028')"], {"hors_jeu": ["64028"], "defausse_rencontre": ["64028"]}, **SANS_DEFENSE),
    _c("64028 Crane Daughter : Vulnerable imprime -> sonnee, elle est defaussee",
       "mot-cle natif lu dans data/cards.json",
       [SANS_NEMESIS] + pose("64028"), ["Puzzle.Stun('64028')"], {"hors_jeu": ["64028"]}),

    # ===================================================================== 64029 Steel Serpent
    _c("64029 Steel Serpent : Davos (3 Crane Daughter dessous) attaque -> une est defaussee, ATQ 2+3 = 5 degats",
       "Forced Interrupt : discard a tucked Crane Daughter → +3 ATK for this attack",
       [DAVOS_REVELE] + pose("64029"), [DAVOS_ATTAQUE],
       {"degats_identite": 5, "taille_pose_sous": [["64027", 2]], "defausse_rencontre": ["64028"]}, **SANS_DEFENSE),
    _c("64029 TEMOIN : sans Steel Serpent, Davos attaque a 2 et garde ses 3 Crane Daughter",
       "temoin du cas precedent",
       [DAVOS_REVELE], [DAVOS_ATTAQUE], {"degats_identite": 2, "taille_pose_sous": [["64027", 3]]}, **SANS_DEFENSE),
    _c("64029 Steel Serpent : aucune Crane Daughter (ni dessous ni en jeu) -> pas de +3 (2 degats)",
       "cout avant la fleche : impayable, pas de bonus",
       [SANS_NEMESIS] + pose("64027", "64029"), [DAVOS_ATTAQUE], {"degats_identite": 2}, **SANS_DEFENSE),
    _c("64029 Steel Serpent : aucune dessous, une Crane Daughter EN JEU -> elle est vaincue (melangee), 5 degats",
       "defeat a Crane Daughter in play → +3 ATK",
       [SANS_NEMESIS] + pose("64027", "64028", "64029"), [DAVOS_ATTAQUE],
       {"degats_identite": 5, "hors_jeu": ["64028"], "dans_deck_rencontre": ["64028"]}, **SANS_DEFENSE),
    _c("64029 Steel Serpent : Crane Daughter dessous ET en jeu, le joueur choisit de vaincre celle en jeu -> les 2 dessous restent",
       "discard ... OR defeat : le joueur attaque choisit",
       [SANS_NEMESIS] + pose("64027") + ["Puzzle.PlaceUnder('64028', '64027')", "Puzzle.PlaceUnder('64028', '64027')"] + pose("64028", "64029"),
       [DAVOS_ATTAQUE], {"degats_identite": 5, "taille_pose_sous": [["64027", 2]], "dans_deck_rencontre": ["64028"]},
       choisir_option="Defeat_a_Crane_Daughter_in_play", **SANS_DEFENSE),
    _c("64029 Steel Serpent : le +3 ne vaut que pour CETTE attaque (Davos revient a ATQ 2)",
       "for this attack",
       [DAVOS_REVELE] + pose("64029"), [DAVOS_ATTAQUE],
       {"attributs_carte": [["64027", "attack", 0]]}, **SANS_DEFENSE),
    _c("64029 Steel Serpent : un AUTRE sbire attaque -> rien (2 Hydra Mercenary ATQ... temoin par les Crane Daughter intactes)",
       "When DAVOS attacks",
       [DAVOS_REVELE] + pose("01101", "64029"), ["Puzzle.EnemyAttacks('01101', '64001a')"],
       {"taille_pose_sous": [["64027", 3]]}, **SANS_DEFENSE),
    _c("64029 Steel Serpent : icone Acceleration imprimee",
       "icone lue dans data/cards.json", pose("64029"), [], {"en_jeu": ["64029"], "icones": [["Acceleration", 1]]}),
]
