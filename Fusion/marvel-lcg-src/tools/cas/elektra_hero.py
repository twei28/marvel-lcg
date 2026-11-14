# Cas test_capacites du HEROS officiel ELEKTRA (Hero Pack MC63, set « Elektra », 63001a-63014 + paquet Ninja 63002-63004),
# noms prefixes « [elektra] ». Un cas par capacite, le card_id est dans le nom. Gabarits : docs/packs/elektra_heros.md.
# Plan et decisions : .planning/elektra-heros/PLAN.md. Scripts : src/cards/pack/elektra/elektra/ et elektra_ninja/.
#
# ⚠ POINT DE DEPART : `Puzzle.ChangeToFace('63001b', '63001a')` (HEROS) declenche l'Interruption Ninja Training, comme en partie :
# apres le montage le paquet Ninja compte 5 cartes et le paquet de rencontre en contient 1 de la famille Ninja. Les cas qui
# partent de HEROS comptent donc a partir de 5 / 1.
#
# Montage : vilain Rhino 01094 (14 PV, ATQ 2) ; Elektra Natchios (63001b) / Elektra (63001a). `main_exclusive` dit avec
# QUOI on paie (01090 = Strength RR, 01088 Energy = YY, 01089 Genius = BB).
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('63001b', '63001a')"
CIVIL = "Puzzle.ChangeToFace('63001a', '63001b')"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
DOOM = "Puzzle.ChangeToFace('dd001b', 'dd001a')"
IFIST = "Puzzle.ChangeToFace('64001b', '64001a')"
NINJA6 = ["63002", "63002", "63003", "63003", "63004", "63004"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[elektra] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "elektra"), "mise_en_place": SANS_BOOST + list(mise),
           "declencher": declencher, "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ===================================================================== 63001b Elektra Natchios
    _c("63001b Elektra Natchios : la partie commence avec le paquet NINJA (6 cartes : 2 x 63002, 2 x 63003, 2 x 63004)",
       "« begins the game with a NINJA deck » : BeginGameWithSetAside + paquet annexe melange",
       [], [], {"deck_annexe_taille": 6, "deck_annexe": NINJA6}),
    _c("63001b Ninja Training : passage en forme heros -> la carte du dessus du paquet NINJA est melangee dans le paquet de rencontre",
       "« Interrupt: When you change to hero form, shuffle the top card of the NINJA deck into the encounter deck » : "
       "paquet Ninja 6 -> 5, une carte Ninja de plus dans le paquet de rencontre",
       [], ["Puzzle.ChangeForm('63001b')"], {"deck_annexe_taille": 5, "forme": "Hero", "rencontre_compte": [[["63002", "63003", "63004"], 1]]}),

    # ===================================================================== 63007 Killer Blow
    _c("63007 Killer Blow : 5 degats a Rhino (14 PV), pas vaincu -> aucune carte Ninja melangee",
       "« Deal up to 5 damage » : le joueur choisit 5 ; « if this attack defeats that enemy » ne part pas",
       [HEROS, "Puzzle.PutIntoPlay('63007')"], [], {"degats": [["01094", 5]], "rencontre_compte": [[["63002", "63003", "63004"], 1]],
        "deck_annexe_taille": 5}, jouer=["63007"], main_exclusive=["01090"], choisir_option="5", cibles=["01094"]),
    _c("63007 Killer Blow : 5 degats a un sbire (3 PV) -> vaincu, une carte Ninja du dessus est melangee dans le paquet de rencontre",
       "« If this attack defeats that enemy, shuffle the top card of the NINJA deck into the encounter deck »",
       [HEROS, "Puzzle.PutIntoPlay('01101')"], [], {"hors_jeu": ["01101"], "deck_annexe_taille": 4,
        "rencontre_compte": [[["63002", "63003", "63004"], 2]]}, jouer=["63007"], main_exclusive=["01090"], choisir_option="5", cibles=["01101"]),
    _c("63007 Killer Blow : le joueur choisit 2 (\"up to 5\") sur un sbire a 3 PV -> 2 degats, pas vaincu, pas de melange",
       "« UP TO 5 » : un nombre inferieur est legal ; 2 < 3 PV, l'ennemi survit",
       [HEROS, "Puzzle.PutIntoPlay('01101')"], [], {"degats": [["01101", 2]], "deck_annexe_taille": 5,
        "rencontre_compte": [[["63002", "63003", "63004"], 1]]}, jouer=["63007"], main_exclusive=["01090"], choisir_option="2", cibles=["01101"]),
    # ===================================================================== 63008 Move Unseen
    _c("63008 Move Unseen : retire 4 menaces du complot principal (6 -> 2) et melange une carte Ninja dans le paquet de rencontre",
       "« Remove up to 4 threat from a scheme. Shuffle the top card of the NINJA deck into the encounter deck »",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.PutIntoPlay('63008')"], [], {"menace": [["01097b", 2]], "deck_annexe_taille": 4,
        "rencontre_compte": [[["63002", "63003", "63004"], 2]]}, jouer=["63008"], main_exclusive=["01090"], choisir_option="4"),
    _c("63008 Move Unseen : le joueur choisit 0 (\"up to 4\") -> menace intacte, mais la carte Ninja est quand meme melangee",
       "le melange est une phrase separee, sans condition : il part meme si 0 menace est retiree",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.PutIntoPlay('63008')"], [], {"menace": [["01097b", 6]], "deck_annexe_taille": 4,
        "rencontre_compte": [[["63002", "63003", "63004"], 2]]}, jouer=["63008"], main_exclusive=["01090"], choisir_option="0"),
    # ===================================================================== 63009 Sai Strike
    _c("63009 Sai Strike : 3 degats a Rhino, aucun Elektra's Sai en jeu -> aucune carte Ninja melangee",
       "« For each Elektra's Sai you control » : zero Sai, zero melange",
       [HEROS, "Puzzle.PutIntoPlay('63009')"], [], {"degats": [["01094", 3]], "deck_annexe_taille": 5,
        "rencontre_compte": [[["63002", "63003", "63004"], 1]]}, jouer=["63009"], main_exclusive=["01090"], cibles=["01094"]),
    _c("63009 Sai Strike : deux Elektra's Sai sous son controle -> deux cartes Ninja melangees (une par Sai)",
       "« For each Elektra's Sai you control, shuffle the top card of the NINJA deck into the encounter deck »",
       [HEROS, "Puzzle.CreatePlayerDeck('63012')", "Puzzle.PutIntoPlay('63012', under_control=True)",
        "Puzzle.CreatePlayerDeck('63012')", "Puzzle.PutIntoPlay('63012', under_control=True)", "Puzzle.PutIntoPlay('63009')"], [], {"degats": [["01094", 3]], "deck_annexe_taille": 3,
        "rencontre_compte": [[["63002", "63003", "63004"], 3]]}, jouer=["63009"], main_exclusive=["01090"], cibles=["01094"]),
    # ===================================================================== 63012 Elektra's Sai
    _c("63012 Elektra's Sai : Hero Action, epuise la carte, 1 degat a Rhino",
       "« Exhaust Elektra's Sai -> deal 1 damage to an enemy »",
       [HEROS, "Puzzle.PutIntoPlay('63012', under_control=True)"], ["Puzzle.Action('63012', 'HeroAction', 0)"],
       {"degats": [["01094", 1]], "exhausted": ["63012"]}, cibles=["01094"]),
    _c("63012 Elektra's Sai : le prochain evenement ATTACK de la phase coute 1 de moins (Sai Strike jouee sans payer)",
       "« reduce the cost of the next ACROBATIC or ATTACK event you play this phase by 1 » : Sai Strike (cout 1), seule carte en main, "
       "se joue gratuitement apres l'Action du Sai (1 + 3 = 4 degats)",
       [HEROS, "Puzzle.PutIntoPlay('63012', under_control=True)"], ["Puzzle.Action('63012', 'HeroAction', 0)"],
       {"degats": [["01094", 4]]}, jouer=["63009"], main_exclusive=[], cibles=["01094"]),

    # ===================================================================== 63010 Resurrection Altar
    _c("63010 Resurrection Altar : Elektra serait vaincue (8 degats + attaque de Tiger Shark, ATQ 3 contre sa DEF boostee) -> l'Autel quitte le jeu, PV remis a 9 (0 degat)",
       "« Interrupt: When you would be defeated, remove this card from the game -> set your hit point dial to 9 instead »",
       [HEROS, "Puzzle.PutIntoPlay('63010', under_control=True)", "Puzzle.Damage('63001a', 8)", "Puzzle.PutIntoPlay('01131')"], ["Puzzle.Attack('01131')"],
       {"hors_jeu": ["63010"], "degats_identite": 0, "forme": "Hero"}, accepter_choix=True, main_exclusive=["01090"]),
    _c("63010 Resurrection Altar : sans l'Autel, la meme attaque vainc Elektra (temoin : 63010 absent, PV a 0 restant)",
       "contre-cas : sans la carte rien ne remet les PV a 9 ; la partie est perdue",
       [HEROS, "Puzzle.Damage('63001a', 8)", "Puzzle.PutIntoPlay('01131')"], ["Puzzle.Attack('01131')"],
       {"degats_identite_min": 9}, accepter_choix=True, main_exclusive=["01090"]),
    # ===================================================================== 63013 History with the Hand
    _c("63013 History with the Hand : Elektra en forme heros joue la carte (cout 0) -> elle est en jeu",
       "« Prerequisite (hero form) » satisfait", [HEROS, "Puzzle.PutIntoPlay('63013')"], [],
       {"en_jeu": ["63013"]}, jouer=["63013"], main_exclusive=["01090"]),
    _c("63013 History with the Hand : Forced Response -> Elektra change de forme (heros -> alter-ego), la carte est defaussee",
       "« Forced Response: After you change form, discard this card »",
       [HEROS, "Puzzle.PutIntoPlay('63013', under_control=True)"], ["Puzzle.ChangeForm('63001a')"],
       {"hors_jeu": ["63013"], "forme": "AlterEgo"}),

    _c("63013 History with the Hand : Prerequisite (hero form) : en ALTER-EGO la carte ne se joue pas (reste en main)",
       "contre-cas : en forme alter-ego la condition de jeu n'est pas remplie",
       [], [], {"en_main": ["63013"]}, jouer=["63013"], main_exclusive=["63013"]),
    _c("63013 History with the Hand : +1 taille de main : on pioche jusqu'a la taille de main, la main se refait a 6 au lieu de 5",
       "« You get +1 hand size » : la pioche de fin de round remplit jusqu'a la taille de main",
       [HEROS, "Puzzle.PutIntoPlay('63013', under_control=True)", "Puzzle.EmptyHand()"], ["Puzzle.DrawUpToHandSize()"],
       {"taille_main": 6}),
    _c("63013 History with the Hand : temoin sans la carte : on pioche jusqu'a la taille de main, la main se refait a 5",
       "meme montage sans History with the Hand : taille de main 5",
       [HEROS, "Puzzle.EmptyHand()"], ["Puzzle.DrawUpToHandSize()"], {"taille_main": 5}),

    # ===================================================================== 63005 Daredevil
    _c("63005 Daredevil : apres son attaque de base, une carte de la defausse de rencontre (01105) est replacee sur le dessus du paquet de rencontre",
       "« Response: After Daredevil uses a basic power, place a card from the encounter discard pile on top of the encounter deck »",
       [HEROS, "Puzzle.PutIntoPlay('63005', under_control=True)", "Puzzle.CreateEncounterDiscardPile('01101')"], ["Puzzle.Attack('63005')"],
       {"dans_deck_rencontre": ["01101"], "defausse_rencontre": []}, accepter_choix=True, cibles=["01094"]),
    _c("63005 Daredevil : apres son deploiement de menace de base (Thwart), la meme Response part",
       "« a basic power » : attaque OU deploiement de base",
       [HEROS, "Puzzle.PutIntoPlay('63005', under_control=True)", "Puzzle.SetThreat('01097b', 6)", "Puzzle.CreateEncounterDiscardPile('01101')"],
       ["Puzzle.Thwart('63005')"], {"dans_deck_rencontre": ["01101"], "defausse_rencontre": []}, accepter_choix=True),
    _c("63005 Daredevil : defausse de rencontre VIDE -> rien ne se passe, aucune erreur",
       "« a card from the encounter discard pile » : aucune carte a choisir",
       [HEROS, "Puzzle.PutIntoPlay('63005', under_control=True)", "Puzzle.EmptyEncounterDiscardPile()"], ["Puzzle.Attack('63005')"],
       {"defausse_rencontre": []}, accepter_choix=True, cibles=["01094"]),

    # ===================================================================== 63011 White Tiger
    _c("63011 White Tiger : passage en forme heros -> DEUX cartes Ninja melangees (Ninja Training + White Tiger), paquet Ninja 6 -> 4",
       "« After you change to hero form, shuffle the top card of the NINJA deck into the encounter deck » en plus de l'Interruption de 63001b",
       ["Puzzle.PutIntoPlay('63011', under_control=True)"], ["Puzzle.ChangeForm('63001b')"],
       {"deck_annexe_taille": 4, "forme": "Hero", "rencontre_compte": [[["63002", "63003", "63004"], 2]]}),
    _c("63011 White Tiger : paquet Ninja VIDE -> « Otherwise » : Elektra recoit 1 carte boost face cachee",
       "decision utilisateur du 13/11/2026 : « sinon » = paquet Ninja vide",
       ["Puzzle.EmptyAdditionalDeck()", "Puzzle.PutIntoPlay('63011', under_control=True)"], ["Puzzle.ChangeForm('63001b')"],
       {"forme": "Hero", "deck_annexe_taille": 0, "boosts_sur": [["63001a", 1]]}),
    _c("63011 White Tiger : passage en ALTER-EGO -> rien (la Response vise la forme heros)",
       "contre-cas : « change TO HERO form »", [HEROS, "Puzzle.PutIntoPlay('63011', under_control=True)"], ["Puzzle.ChangeForm('63001a')"],
       {"forme": "AlterEgo", "deck_annexe_taille": 5, "rencontre_compte": [[["63002", "63003", "63004"], 1]]}),
    # ===================================================================== 63006 Acrobatic Prowess
    _c("63006 Acrobatic Prowess : Elektra incline est redressee et recoit 1 carte boost face cachee",
       "« Ready Elektra and give her 1 facedown boost card »",
       [HEROS, "Puzzle.Exhaust('63001a')", "Puzzle.PutIntoPlay('63006')"], [],
       {"pret": ["63001a"], "boosts_sur": [["63001a", 1]]}, jouer=["63006"], main_exclusive=["01090"]),

    # ===================================================================== 63001a Elektra : Villainous + Killer Instinct ; 63002-63004 Ninja
    _c("63001a Elektra : Villainous : une attaque de base recoit UNE carte de boost (Shocker 2 icones) ; avec Killer Instinct (+1 icone) : ATQ 1 + 3 = 4 degats",
       "« ★ Villainous (When this character uses a basic power, give it a boost card) » ; « Killer Instinct ... that card gains [boost] »",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01103')"], ["Puzzle.Attack('63001a')"],
       {"boosts_sur": [["63001a", 1]], "degats": [["01094", 4]]}, cibles=["01094"]),
    _c("63001a Killer Instinct : une carte de boost SANS icone (01105) gagne 1 icone : ATQ 1 + 1 = 2 degats",
       "« Interrupt: When a boost card given to Elektra is turned faceup ... that card gains [boost] » : sans l'Interruption l'attaque ferait 1",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105')"], ["Puzzle.Attack('63001a')"],
       {"boosts_sur": [["63001a", 1]], "degats": [["01094", 2]]}, cibles=["01094"]),
    _c("63001a Killer Instinct sur une carte Ninja Strike (63003) en boost : le Boost est annule (ATQ 1 + 1 icone = 2), la carte est defaussee, pas dans le paquet Ninja",
       "« cancel its Boost ability. Then, that card gains [boost] » : l'Interruption est prise d'office par le pilote",
       [HEROS, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '63003')"], ["Puzzle.Attack('63001a')"],
       {"degats": [["01094", 2]], "deck_annexe_taille": 5, "defausse_rencontre": ["63003"]}, cibles=["01094"]),
    # --- Effets Boost des cartes Ninja, mesures SANS Killer Instinct : sur Doctor Doom (heros sans l'Interruption), pile de boost chargee a la main
    _c("63003 Ninja Strike (boost d'une attaque de BASE) : +3 a l'attaque (ATQ 1 + 3 = 4) et la carte rejoint le paquet Ninja du joueur",
       "« ★ Boost: If Elektra is using a basic power, she gets +3 to that power for this use and you shuffle this card into the NINJA deck »",
       [DOOM, "Puzzle.GiveFacedownBoost('dd001a', '63003')"], ["Puzzle.Attack('dd001a')"],
       {"degats": [["01094", 4]], "deck_annexe_taille": 1}, heros="doctor_doom", cibles=["01094"]),
    _c("63002 Ninja Stars (boost d'une attaque de BASE) : le heros pioche 2 cartes et la carte rejoint le paquet Ninja",
       "« If Elektra is using a basic power, draw 2 cards and shuffle this card into the NINJA deck »",
       [DOOM, "Puzzle.EmptyHand()", "Puzzle.GiveFacedownBoost('dd001a', '63002')"], ["Puzzle.Attack('dd001a')"],
       {"taille_main": 2, "deck_annexe_taille": 1}, heros="doctor_doom", cibles=["01094"]),
    _c("63004 Ninja Vanish (boost d'une attaque de BASE) : le heros recoit une carte Tough et la carte rejoint le paquet Ninja",
       "« give her a tough status card and shuffle this card into the NINJA deck »",
       [DOOM, "Puzzle.GiveFacedownBoost('dd001a', '63004')"], ["Puzzle.Attack('dd001a')"],
       {"statuts": [["dd001a", "Tough"]], "deck_annexe_taille": 1}, heros="doctor_doom", cibles=["01094"]),
    _c("63003 Ninja Strike sur un DEPLOIEMENT de base (extension moteur) : THW 1 + 3 = 4 menaces retirees (6 -> 2), la carte rejoint le paquet Ninja",
       "le boost d'un heros se resout aussi sur Thwart (Iron Fist : heros sans l'Interruption d'Elektra, THW 1)",
       [IFIST, "Puzzle.SetThreat('01097b', 6)", "Puzzle.GiveFacedownBoost('64001a', '63003')"], ["Puzzle.Thwart('64001a')"],
       {"menace": [["01097b", 2]], "deck_annexe_taille": 1}, heros="iron_fist"),
    _c("63003 Ninja Strike sur une DEFENSE de base (extension moteur) : DEF 2 + 3 = 5 contre l'ATQ 2 de Rhino : 0 degat, la carte rejoint le paquet Ninja",
       "le boost d'un heros se resout aussi sur Defense ; le temoin sans la carte est le cas suivant (2 degats moins la DEF 2 = 0, donc on mesure le paquet)",
       [IFIST, "Puzzle.GiveFacedownBoost('64001a', '63003')"], ["Puzzle.Defend('64001a', '01094')"],
       {"deck_annexe_taille": 1, "degats_identite": 0}, heros="iron_fist", main_exclusive=["01090"]),
    _c("63003 Ninja Strike boost d'un ENNEMI : Rhino active avec la carte -> « Otherwise », elle va dans la pile de boost du heros (elle y attend sa prochaine action)",
       "le pouvoir en cours est celui de Rhino, pas d'Elektra : « Otherwise, give this card to Elektra as a facedown boost card » ; Iron Fist (sans Villainous) "
       "la recoit (1 carte) APRES sa propre defense (le boost de Rhino se resout apres la defense) : la carte attend dans la pile, le paquet Ninja reste vide",
       [IFIST, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '63003')"], ["Puzzle.Boost('63003')"],
       {"boosts_sur": [["64001a", 1]], "deck_annexe_taille": 0}, heros="iron_fist", main_exclusive=["01090"]),
    # ===================================================================== 63014 Stealth Mastery (portee par Iron Fist : ATQ 2, heros sans Villainous ni Killer Instinct)
    _c("63014 Stealth Mastery : « When you attack » : augmente de 3 -> ATQ 2 + 3 = 5 degats, la carte part sur le dessus du paquet",
       "« choose to either increase or reduce the damage that attack deals by 3. Put Stealth Mastery on top of your deck »",
       [IFIST, "Puzzle.PutIntoPlay('63014', under_control=True)"], ["Puzzle.Attack('64001a')"],
       {"degats": [["01094", 5]], "hors_jeu": ["63014"], "dans_deck_joueur": ["63014"]}, heros="iron_fist", cibles=["01094"], choisir_option="Increase_the_damage_by_3"),
    _c("63014 Stealth Mastery : « When you attack » : reduit de 3 -> ATQ 2 - 3 = 0 degat (pas de degats negatifs)",
       "la reduction s'arrete a 0", [IFIST, "Puzzle.PutIntoPlay('63014', under_control=True)"], ["Puzzle.Attack('64001a')"],
       {"degats": [["01094", 0]], "dans_deck_joueur": ["63014"]}, heros="iron_fist", cibles=["01094"], choisir_option="Reduce_the_damage_by_3"),
    _c("63014 Stealth Mastery : « or are attacked » : Rhino (ATQ 2) attaque Iron Fist non defendu, augmente de 3 -> 5 degats sur l'identite",
       "l'attaque d'un ENNEMI contre l'identite declenche aussi",
       [IFIST, "Puzzle.PutIntoPlay('63014', under_control=True)"], ["Puzzle.PutIntoPlay('01131')", "Puzzle.Attack('01131')"],
       {"degats_identite": 4, "dans_deck_joueur": ["63014"]}, heros="iron_fist", choisir_option="Increase_the_damage_by_3", main_exclusive=["01090"]),
    _c("63014 Stealth Mastery : « are attacked » : reduit de 3 -> Rhino (ATQ 2) ne fait aucun degat",
       "reduire de 3 une attaque de 2", [IFIST, "Puzzle.PutIntoPlay('63014', under_control=True)", "Puzzle.PutIntoPlay('01131')"], ["Puzzle.Attack('01131')"],
       {"degats_identite": 0, "dans_deck_joueur": ["63014"]}, heros="iron_fist", choisir_option="Reduce_the_damage_by_3", main_exclusive=["01090"]),
    _c("63014 Stealth Mastery : aucune attaque -> rien (la carte reste en jeu)",
       "contre-cas : sans attaque, l'Interruption ne part pas", [IFIST, "Puzzle.PutIntoPlay('63014', under_control=True)"], [],
       {"en_jeu": ["63014"]}, heros="iron_fist"),
]
