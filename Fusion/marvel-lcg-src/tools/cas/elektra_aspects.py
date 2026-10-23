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

    # ============================================================ 63015 Shang-Chi
    _c("63015 Shang-Chi : valeurs imprimees PV 3, ATQ 2, CTR 2, traits HERO FOR HIRE et MARTIAL ARTIST, 10 compteurs ring a l'entree",
       "nombres texte <-> code (scan 15) ; « enters play with 10 ring counters »",
       [*en_jeu("63015")], [],
       {"attrs": [["63015", "max_health", 3], ["63015", "attack", 2], ["63015", "thwart", 2]],
        "traits_de": [["63015", "HERO FOR HIRE"], ["63015", "MARTIAL ARTIST"]], "compteurs": [["63015", "ring", 10]]},
       main_exclusive=["01090"]),
    _c("63015 Shang-Chi : Action -> retire 1 ring et inflige 1 degat a Rhino (pas une attaque)",
       "« Action: Remove 1 ring counter from here -> deal 1 damage to an enemy »",
       [*en_jeu("63015")], [], {"degats": [["01094", 1]], "compteurs": [["63015", "ring", 9]]},
       main_exclusive=["01090"], declencher_apres=["Puzzle.Action('63015', 'Action')"], cibles=["01094"]),
    _c("63015 Shang-Chi : limite DEUX fois par round -> 2 degats, 8 compteurs",
       "« (Limit twice per round) » : deux capacites identiques, chacune une fois par round",
       [*en_jeu("63015")], [], {"degats": [["01094", 2]], "compteurs": [["63015", "ring", 8]]},
       main_exclusive=["01090"], declencher_apres=["Puzzle.Action('63015', 'Action')", "Puzzle.Action('63015', 'Action')"],
       cibles=["01094", "01094"]),
    _c("63015 Shang-Chi : TEMOIN d'epuisement, la 3e utilisation dans le round est refusee (toujours 2 degats, 8 compteurs)",
       "la limite est reelle : la 3e Action ne fait rien",
       [*en_jeu("63015")], [], {"degats": [["01094", 2]], "compteurs": [["63015", "ring", 8]]},
       main_exclusive=["01090"],
       declencher_apres=["Puzzle.Action('63015', 'Action')", "Puzzle.Action('63015', 'Action')"],
       cibles=["01094", "01094", "01094"], declencher_tolerant=["Puzzle.Action('63015', 'Action')"]),
    # ============================================================ 63016 Black Cat
    _c("63016 Black Cat : valeurs imprimees PV 3, ATQ 1, CTR 1, Villainous, traits HERO FOR HIRE et MARTIAL ARTIST",
       "nombres texte <-> code (scan 16)",
       [*en_jeu("63016")], [],
       {"attrs": [["63016", "max_health", 3], ["63016", "attack", 1], ["63016", "thwart", 1]],
        "traits_de": [["63016", "HERO FOR HIRE"], ["63016", "MARTIAL ARTIST"]]}, main_exclusive=["01090"]),
    _c("63016 Black Cat : Villainous, son attaque recoit une carte boost (Exhaustion, 2) : 1 + 2 = 3 degats a Rhino, 1 consecutif",
       "« Villainous. (When this character uses a basic power, give it a boost card.) »",
       [*en_jeu("63016"), "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01191')"],
       ["Puzzle.Attack('63016')"], {"degats": [["01094", 3], ["63016", 1]]}, avec_boost=True, main_exclusive=["01090"]),
    _c("63016 Black Cat : TEMOIN un allie SANS Villainous (Vision) attaque (ATQ 2) sans carte boost : 2 degats",
       "la carte boost vient bien du mot-cle", [*en_jeu("01068"), "Puzzle.EmptyEncounterDeck()",
        "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01191')"],
       ["Puzzle.Attack('01068')"], {"degats": [["01094", 2]]}, avec_boost=True, main_exclusive=["01090"]),
    # ============================================================ 63021 Shuriken
    _c("63021 Shuriken : valeurs imprimees, 3 compteurs shuriken, cout 2*",
       "Uses (3 shuriken counters)", [HEROS, *en_jeu("63021")], [], {"en_jeu": ["63021"], "compteurs": [["63021", "shuriken", 3]]},
       main_exclusive=["01090"]),
    _c("63021 Shuriken : Hero Action -> retire 1 shuriken, 1 degat a Rhino (pas une attaque)",
       "« Remove 1 shuriken counter from here -> deal 1 damage to an enemy »",
       [HEROS, *en_jeu("63021")], [], {"degats": [["01094", 1]], "compteurs": [["63021", "shuriken", 2]]},
       main_exclusive=["01090"], declencher_apres=["Puzzle.Action('63021', 'HeroAction')"], cibles=["01094"]),
    _c("63021 Shuriken : trois utilisations -> 3 degats ; le dernier compteur retire, la carte est defaussee (regle des Uses)",
       "3 compteurs = 3 usages ; plus de compteur -> defaussee (RR : Uses)",
       [HEROS, *en_jeu("63021")], [], {"degats": [["01094", 3]], "hors_jeu": ["63021"]},
       main_exclusive=["01090"],
       declencher_apres=["Puzzle.Action('63021', 'HeroAction')", "Puzzle.Action('63021', 'HeroAction')", "Puzzle.Action('63021', 'HeroAction')"],
       cibles=["01094", "01094", "01094"]),
    _c("63021 Shuriken : Discount 1 (Martial Artist) : Iron Fist heros la paie 1 ressource (cout 2*)",
       "« [star] Discount 1 (Martial Artist) »", [HEROS], [], {"en_jeu": ["63021"]},
       main_exclusive=["63021", "01079"], jouer=["63021"]),
    _c("63021 Shuriken : CONTRE-CAS Danny Rand (sans le trait) : une ressource ne suffit pas",
       "la remise exige le trait", [], [], {"en_main": ["63021"]}, main_exclusive=["63021", "01079"], jouer=["63021"]),
    # ============================================================ 63022 Stone
    _c("63022 Stone : valeurs imprimees PV 3, ATQ 2, CTR 1, trait MARTIAL ARTIST",
       "nombres texte <-> code (scan 22)", [*en_jeu("63022")], [],
       {"attrs": [["63022", "max_health", 3], ["63022", "attack", 2], ["63022", "thwart", 1]], "traits_de": [["63022", "MARTIAL ARTIST"]]},
       main_exclusive=["01090"]),
    _c("63022 Stone : bat EXACTEMENT Tiger Shark (6 PV, ATQ 2) -> se soigne de 2 (2 degats portes -> 0, puis 2 consecutifs : 2)",
       "« After Stone exactly defeats an enemy, heal 2 damage from Stone »",
       [*en_jeu("63022"), "Puzzle.PutIntoPlay('01131', under_control=False)", "Puzzle.Damage('01131', 4)", "Puzzle.Damage('63022', 2)"], ["Puzzle.Attack('63022', '01131')"],
       {"degats": [["63022", 2]], "hors_jeu": ["01131"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("63022 Stone : CONTRE-CAS victoire AVEC exces (Tiger Shark a 1 PV) : pas de soin, il garde son degat consecutif",
       "« EXACTLY defeats » : un exces ne declenche rien",
       [*en_jeu("63022"), "Puzzle.PutIntoPlay('01131', under_control=False)", "Puzzle.Damage('01131', 5)"], ["Puzzle.Attack('63022', '01131')"],
       {"degats": [["63022", 2]], "hors_jeu": ["01131"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("63022 Stone : CONTRE-CAS il n'acheve pas Rhino : pas de soin (consecutif 2 reste)",
       "pas de victoire, pas de Response", [*en_jeu("63022")], ["Puzzle.Attack('63022')"],
       {"degats": [["01094", 2], ["63022", 2]]}, main_exclusive=["01090"]),
    _c("63022 Stone : annexe 01107 (menace 2... deja reduite a 1) dejouee EXACTEMENT par Stone (2 degats - 2 soin + 1 consecutif = 1)",
       "« or side scheme » : second declencheur, excedent de menace nul",
       [*en_jeu("63022"), "Puzzle.PutIntoPlay('01107', under_control=False)", "Puzzle.SetThreat('01107', 1)", "Puzzle.Damage('63022', 2)"],
       ["Puzzle.Thwart('63022')"], {"degats": [["63022", 1]]}, main_exclusive=["01090"], cibles=["01107"], accepter_choix=True),
    # ============================================================ 63038 Moondragon
    _c("63038 Moondragon : valeurs imprimees PV 5, ATQ 1, CTR 1, traits DEFENDER et MARTIAL ARTIST",
       "nombres texte <-> code (scan 38)", [*en_jeu("63038")], [],
       {"attrs": [["63038", "max_health", 5], ["63038", "attack", 1], ["63038", "thwart", 1]],
        "traits_de": [["63038", "DEFENDER"], ["63038", "MARTIAL ARTIST"]]}, main_exclusive=["01090"]),
    _c("63038 Moondragon : attaque (le pilote choisit X = 1, premier item de DeclareNumber) -> ATQ 1 + 1 = 2 degats a Rhino, consecutif 1 + 1 = 2",
       "« +X to that power and +X consequential damage » ; limite connue du harnais : X = 1 seulement, la borne 3 est dans DeclareNumber(1, 3)",
       [*en_jeu("63038")], ["Puzzle.Attack('63038')"], {"degats": [["01094", 2], ["63038", 2]]}, main_exclusive=["01090"]),
    _c("63038 Moondragon : contre une annexe (X = 1) -> CTR 1 + 1 = 2 menace retiree, consecutif 2 ; l'ATQ ne bouge pas",
       "« +X to THAT power » : le CTR quand il contre", [*en_jeu("63038"), "Puzzle.PutIntoPlay('01107', under_control=False)"],
       ["Puzzle.Thwart('63038')"], {"degats": [["63038", 2]]}, main_exclusive=["01090"], cibles=["01107"]),
    # ============================================================ 63023 Hunting Shadows
    _c("63023 Hunting Shadows : cherche la carte la plus profonde des 8 (01191), melange, la remet AU DESSUS",
       "« Search the top 8 ... set it aside. Shuffle ... put the set-aside card on top »",
       [HEROS, "Puzzle.EmptyEncounterDeck()",
        "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105', '01191', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"],
       [], {"dessus": "01191", "taille_deck": 17}, avec_boost=True, main_exclusive=["63023"], jouer=["63023"], cibles=["01191"],
       verifier="sc_dessus_rencontre"),
    # ============================================================ 63039 Moon Knight
    _c("63039 Moon Knight : valeurs imprimees PV 5, ATQ 2, CTR 2, traits DEFENDER et MARTIAL ARTIST",
       "nombres texte <-> code (scan 39)", [*en_jeu("63039")], [],
       {"attrs": [["63039", "max_health", 5], ["63039", "attack", 2], ["63039", "thwart", 2]],
        "traits_de": [["63039", "DEFENDER"], ["63039", "MARTIAL ARTIST"]]}, main_exclusive=["01090"]),
    _c("63039 Moon Knight : defend en depensant une ressource [energy] -> Rhino (ATQ 2) ne fait AUCUN degat",
       "« [energy] - Prevent 2 damage from this attack »", [*en_jeu("63039")], ["Puzzle.Defend('63039', '01094')"],
       {"degats": [["63039", 0]]}, main_exclusive=["01088"], payer_avec=["01088"], payer_jusqu_a=2, accepter_choix=True),
    _c("63039 Moon Knight : defend en depensant une ressource [physical] -> 2 degats a Rhino",
       "« [physical] - Deal 2 damage to the attacker »", [*en_jeu("63039")], ["Puzzle.Defend('63039', '01094')"],
       {"degats": [["01094", 2]]}, main_exclusive=["01090"], payer_avec=["01090"], payer_jusqu_a=2, accepter_choix=True),
    _c("63039 Moon Knight : defend sans depenser de ressource -> ATQ 2 pris normalement (2 degats)",
       "« up to 3 »: zero ressource, aucun effet", [*en_jeu("63039")], ["Puzzle.Defend('63039', '01094')"],
       {"degats": [["63039", 2], ["01094", 0]]}, main_exclusive=["01088"], payer_avec=[], payer_jusqu_a=0, accepter_choix=True),
    _c("63039 Moon Knight : [mental] (Genius BB) -> la carte boost de Rhino est DEFAUSSEE avant d'etre retournee : ATQ 2 seul = 2 degats, pas 2 + 3",
       "« [mental] - Discard 1 boost card from the attacker » ; Hydra Mercenary (boost 1) devrait ajouter 1 : TEMOIN ci-dessous",
       [*en_jeu("63039"), "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01191')"],
       ["Puzzle.Defend('63039', '01094')"], {"degats": [["63039", 2]]}, avec_boost=True, main_exclusive=["01089"], payer_avec=["01089"], payer_jusqu_a=2, accepter_choix=True),
    _c("63039 Moon Knight : TEMOIN sans depense, la carte boost (Exhaustion, 2) est retournee : 2 + 2 = 4 degats",
       "valeur de reference du cas precedent",
       [*en_jeu("63039"), "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01191')"],
       ["Puzzle.Defend('63039', '01094')"], {"degats": [["63039", 4]]}, avec_boost=True, main_exclusive=["01089"], payer_avec=[], payer_jusqu_a=0, accepter_choix=True),
    _c("63039 Moon Knight : trois types depenses (une ressource [energy], une [mental], une [physical]) -> prevention 2 ET 2 degats a Rhino",
       "chaque icone est un effet independant ; « up to 3 resources »",
       [*en_jeu("63039")], ["Puzzle.Defend('63039', '01094')"], {"degats": [["63039", 0], ["01094", 2]]},
       main_exclusive=["63017", "63016", "63015"], payer_avec=["63017", "63016", "63015"], payer_jusqu_a=3, payer_tout=True, accepter_choix=True),

    # ============================================================ 63035 Backstab (Linked Double-Cross)
    _c("63035 Backstab : revelee -> 4 degats au vilain (Rhino) et surge",
       "« When Revealed: Deal 4 damage to the villain. This card gains surge. » : la carte suivante (Hydra Mercenary 01101) est revelee",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"], ["Puzzle.Reveal('63035')"],
       {"degats": [["01094", 4]], "en_jeu": ["01101"], "carte_du_surge": "01101"}, avec_boost=True, main_exclusive=["01090"]),
    _c("63035 Backstab : Boost pendant l'ATTAQUE de Rhino (un ennemi active) -> 2 degats a Rhino",
       "« [star] Boost: If an enemy is activating, deal 2 damage to it »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '63035')"],
       ["Puzzle.Attack('01094')"], {"degats": [["01094", 2]]}, avec_boost=True, main_exclusive=["01090"]),
    _c("63035 Backstab : Boost pendant une MANIGANCE de Rhino : c'est AUSSI un ennemi qui active -> 2 degats a Rhino, pas d'icones en plus (menace 1)",
       "« If an ENEMY is activating » : l'activation d'un complot compte (une manigance est l'activation de l'ennemi)",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '63035')"],
       ["Puzzle.Scheme('01094')"], {"degats": [["01094", 2]], "menace": [["01097b", 1]]}, avec_boost=True, main_exclusive=["01090"]),
    _c("63035 Backstab : Boost sans ennemi qui active (attaque d'un allie VILLAINOUS, Black Cat) -> la carte gagne 2 icones : ATQ 1 + 2 = 3 degats a Rhino, aucun degat de la carte",
       "« Otherwise, this card gains [boost][boost] » ; Black Cat (63016, Villainous) recoit une carte boost quand elle attaque : aucun ennemi n'active",
       [*en_jeu("63016"), "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '63035')"],
       ["Puzzle.Attack('63016')"], {"degats": [["01094", 3], ["63016", 1]]}, avec_boost=True, main_exclusive=["01090"]),
    # ============================================================ 63036 Misdirect
    _c("63036 Misdirect : revelee -> soigne 4 degats de l'identite (5 -> 1) et surge",
       "« When Revealed: Heal 4 damage from an identity. This card gains surge. » : la carte suivante (Hydra Mercenary 01101) est revelee",
       ["Puzzle.Damage('64001b', 5)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
       ["Puzzle.Reveal('63036')"], {"degats_identite": 1, "en_jeu": ["01101"], "carte_du_surge": "01101"}, avec_boost=True, main_exclusive=["01090"], accepter_choix=True),
    _c("63036 Misdirect : le soin ne depasse pas les degats portes (2 -> 0)",
       "4 points MAXIMUM, pas de degats negatifs", ["Puzzle.Damage('64001b', 2)"], ["Puzzle.Reveal('63036')"],
       {"degats_identite": 0}, main_exclusive=["01090"], accepter_choix=True),
    _c("63036 Misdirect : Boost -> Rhino est sonne",
       "« [star] Boost: Stun an enemy »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '63036')"],
       ["Puzzle.Attack('01094')"], {"statuts": [["01094", "Stunned"]]}, avec_boost=True, main_exclusive=["01090"], accepter_choix=True),
    # ============================================================ 63037 Sabotage
    _c("63037 Sabotage : revelee -> 3 menace retiree du complot principal (5 -> 2) et surge",
       "« When Revealed: Remove 3 threat from the main scheme. This card gains surge. » : la carte suivante (Hydra Mercenary 01101) est revelee",
       ["Puzzle.SetThreat('01097b', 5)", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01101')"],
       ["Puzzle.Reveal('63037')"], {"menace": [["01097b", 2]], "en_jeu": ["01101"], "carte_du_surge": "01101"}, avec_boost=True, main_exclusive=["01090"]),
    _c("63037 Sabotage : revelee, menace 2 seulement -> retire 2 (pas de menace negative)",
       "« Remove 3 threat » : au plus ce qui est present", ["Puzzle.SetThreat('01097b', 2)"], ["Puzzle.Reveal('63037')"],
       {"menace": [["01097b", 0]]}, main_exclusive=["01090"]),
    _c("63037 Sabotage : Boost -> Rhino est desoriente",
       "« [star] Boost: Confuse an enemy »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '63037')"],
       ["Puzzle.Attack('01094')"], {"statuts": [["01094", "Confused"]]}, avec_boost=True, main_exclusive=["01090"], accepter_choix=True),
    # ============================================================ 63034 Double-Cross
    _c("63034 Double-Cross : valeurs imprimees : cout 0, menace de depart 2 par joueur (1 joueur : 2), Victory 0, unique",
       "nombres texte <-> code (scan 34)", ["Puzzle.PutIntoPlay('63034', under_control=True)"], [],
       {"menace": [["63034", 2]]}, main_exclusive=["01090"]),
    _c("63034 Double-Cross : dejouee -> Backstab, Misdirect et Sabotage melanges dans les 10 premieres cartes du deck (13 cartes), plus rien de mis de cote",
       "« When Defeated: ... shuffle the set-aside Backstab, Misdirect, and Sabotage treachery cards into the top 10 cards of the encounter deck »",
       ["Puzzle.PutIntoPlay('63034', under_control=True)", "Puzzle.PutIntoPlay('63022', under_control=True)", "Puzzle.SetThreat('63034', 1)",
        "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(" + ", ".join(["'01105'"] * 15) + ")"],
       ["Puzzle.Thwart('63022')"], {"dans_top": 13, "taille": 18}, avec_boost=True, main_exclusive=["01090"], cibles=["63034"],
       verifier="el_melange_haut"),
    _c("63034 Double-Cross : deck de rencontre de 4 cartes seulement -> tout le deck est melange avec elles (7 cartes)",
       "« (or the whole deck if there are fewer than 10 cards) »",
       ["Puzzle.PutIntoPlay('63034', under_control=True)", "Puzzle.PutIntoPlay('63022', under_control=True)", "Puzzle.SetThreat('63034', 1)",
        "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105')"],
       ["Puzzle.Thwart('63022')"], {"dans_top": 7, "taille": 7}, avec_boost=True, main_exclusive=["01090"], cibles=["63034"],
       verifier="el_melange_haut"),
    _c("63034 Double-Cross : CONTRE-CAS une copie est DEJA dans la pile de victoire -> rien n'est melange (les 3 restent de cote)",
       "« If there is not ALREADY a copy of Double-Cross in the victory display »",
       ["Puzzle.PutIntoPlay('63034', under_control=True)", "Puzzle.PutIntoPlay('63022', under_control=True)", "Puzzle.SetThreat('63034', 1)",
        "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(" + ", ".join(["'01105'"] * 15) + ")",
        "Puzzle.MoveTo('63034', 'VictoryDisplay')", "Puzzle.PutIntoPlay('63034', under_control=True)"],
       ["Puzzle.Thwart('63022')"], {"dans_top": 0, "taille": 15}, avec_boost=True, main_exclusive=["01090"], cibles=["63034"],
       verifier="el_melange_haut"),
]


VERIFICATIONS = r'''
def el_melange_haut(monde, aides):
    """`attendu` : dans_top (combien de Backstab/Misdirect/Sabotage sont dans les `dans_top` premieres cartes du deck de rencontre ;
    0 = aucune), taille (taille du deck). Les trois sont toujours soit TOUTES dans le deck soit TOUTES de cote."""
    from game.operate.worlds import Worlds
    attendu = aides["cas"]["attendu"]
    deck = [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde) if f is not None]
    trois = ("63035", "63036", "63037")
    soucis = []
    if len(deck) != attendu["taille"]:
        soucis.append(f"deck de rencontre = {len(deck)} carte(s) (attendu {attendu['taille']})")
    n = attendu["dans_top"]
    if n:
        haut = deck[:n]
        for c in trois:
            if c not in haut:
                soucis.append(f"{c} absente des {n} premieres cartes ({haut})")
    else:
        for c in trois:
            if c in deck:
                soucis.append(f"{c} est dans le deck alors qu'elle devait rester de cote")
    cote = [getattr(f.paper, "card_id", None) for f in monde.aside_deck.Get(True) if f is not None]
    for c in trois:
        if n and c in cote:
            soucis.append(f"{c} est encore de cote")
        if not n and c not in cote:
            soucis.append(f"{c} n'est plus de cote")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"deck {len(deck)}, les trois cartes {'dans les ' + str(n) + ' premieres' if n else 'de cote'}"
'''
