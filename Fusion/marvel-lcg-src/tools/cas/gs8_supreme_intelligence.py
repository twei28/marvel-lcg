# Cas test_capacites du lot GS-8 de Galactic Storm (Kajislav) : scenario 5 Supreme Intelligence
# (gs195-gs208) et sets modulaires Starforce (gs209-gs217), Seeds of Corruption (gs218-gs221),
# Nega-Bomb (gs222a/b, gs223). Prefixe des cas : [gs8] ; filtre : `[gs8]` (ou `gsNNN ` pour une carte).
#
# Conventions :
#  - heros de test : Spider-Man (01001), demarre en alter ego (01001b) ; HEROS le passe en forme heros ;
#  - scenario `gs_supreme_intelligence` : a la mise en place (graine du harnais), 1A met de cote les sbires
#    STARFORCE et en met UN en jeu ; `SANS_STARFORCE_EN_JEU` le retire pour partir d'une table connue ;
#  - `NEUTRE` remplace le deck rencontre par des cartes sans icone de boost (Kree Infantry n'en est pas :
#    1 icone) : 01105 (Rhino, Advance) n'a aucune icone ;
#  - scenario d'essai `gs_essai_modulaires_gs8` : Rhino avec Seeds of Corruption, Nega-Bomb et Starforce en
#    modulaires (les sbires Starforce y sont de simples sbires du deck rencontre).

SI = "gs_supreme_intelligence"
SIX = "gs_supreme_intelligence_expert"
ESSAI = "gs_essai_modulaires_gs8"
HEROS = "Puzzle.ChangeForm('01001b')"
NEUTRE = ["Puzzle.EmptyEncounterDeck()",
          "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
# Le sbire STARFORCE mis en jeu par la mise en place (graine : le premier trouve) : retire de la partie.
SANS_STARFORCE_EN_JEU = "Puzzle.RemoveMinionsInPlay()"
SANS_TANK = "Puzzle.Remove('gs200')"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[gs8] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SI),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": list(mise), "declencher": list(declencher),
           "verifier": cle.pop("verifier", "gs8_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ===================================================================== mise en place
    _c("gs198a Setup : chaque STARFORCE mis de cote, UN en jeu engage avec le premier joueur, Holding Tank sur le mechant",
       "1A : « Set each STARFORCE minion aside and put 1 of them at random into play engaged with the first player. "
       "Attach Holding Tank to the villain. » 10 sbires STARFORCE (8 Starforce + 2 Supremor, lecture Q1) : 9 de cote, 1 "
       "en jeu ; Holding Tank attache a gs195 avec 7 pions integrity (1 joueur). Sans le module : 0 de cote, pas de Tank",
       [], [],
       {"starforce_mis_de_cote": 9, "starforce_en_jeu": 1, "accroche_a": [["gs200", "gs195"]],
        "compteurs": [["gs200", "integrity", 7]], "en_jeu": ["gs195", "gs198b"]}),
    _c("gs198a Setup EXPERT : stade II (gs196) au depart, meme mise en place, Tenace (Toughness)",
       "Insert : (II) et (III) en expert ; gs196 porte Toughness (carte Tenace a l'entree en jeu)",
       [], [],
       {"starforce_mis_de_cote": 9, "starforce_en_jeu": 1, "accroche_a": [["gs200", "gs196"]],
        "statuts": [["gs196", "Tough"]], "pv_max": [["gs196", 14]], "hors_jeu": ["gs195"]},
       scenario=SIX),
    _c("gs198a Setup a DEUX joueurs : Holding Tank porte 14 pions (7 par joueur), mechant 26 PV",
       "Uses (7[per_hero]) et HIT POINTS 13[per_hero]",
       [], [],
       {"compteurs": [["gs200", "integrity", 14]], "pv_max": [["gs195", 26]]},
       heros2="hawkeye"),
    # ===================================================================== mechants
    _c("gs195 Supreme Intelligence I : un sbire KREE non ELITE vaincu -> soin de 1, AUCUNE carte de boost",
       "Kree Infantry (KREE, pas ELITE) vaincu : le mechant (3 degats) en garde 2, aucune carte de boost recue",
       [SANS_STARFORCE_EN_JEU, SANS_TANK, "Puzzle.Damage('gs195', 3)", "Puzzle.PutIntoPlay('gs202')", *NEUTRE],
       ["Puzzle.Damage('gs202', 5)"],
       {"degats": [["gs195", 2]], "boost_du_mechant": 0, "hors_jeu": ["gs202"]}),
    _c("gs195 Supreme Intelligence I : un sbire KREE ELITE (Starforce) vaincu -> soin de 1 ET une carte de boost face cachee",
       "Ronan the Accuser (ELITE KREE) vaincu : 3 degats -> 2, une carte de boost donnee au mechant",
       [SANS_STARFORCE_EN_JEU, SANS_TANK, "Puzzle.Damage('gs195', 3)", "Puzzle.PutIntoPlay('gs214')", *NEUTRE],
       ["Puzzle.Damage('gs214', 8)"],
       {"degats": [["gs195", 2]], "boost_du_mechant": 1, "vitrine": ["gs214"]}),
    _c("gs195 Supreme Intelligence I : Kree Infantry ELITE par Genetic Augmentation vaincue -> carte de boost (trait gagne)",
       "« If that minion has the ELITE trait » : le trait GAGNE compte (Genetic Augmentation attachee) ; 7 PV (5+2)",
       [SANS_STARFORCE_EN_JEU, SANS_TANK, "Puzzle.Damage('gs195', 3)", "Puzzle.PutIntoPlay('gs202')", "Puzzle.Reveal('gs201')",
        *NEUTRE],
       ["Puzzle.Damage('gs202', 7)"],
       {"degats": [["gs195", 2]], "boost_du_mechant": 1, "hors_jeu": ["gs202", "gs201"]}),
    _c("gs195 Supreme Intelligence I : un sbire NON KREE vaincu -> rien (contre-cas)",
       "« After a KREE minion is defeated » : Hydra Mercenary 01101 (pas KREE) vaincu : aucun soin",
       [SANS_STARFORCE_EN_JEU, SANS_TANK, "Puzzle.Damage('gs195', 3)", "Puzzle.PutIntoPlay('01101')", *NEUTRE],
       ["Puzzle.Damage('01101', 3)"],
       {"degats": [["gs195", 3]], "boost_du_mechant": 0}),
    _c("gs196 Supreme Intelligence II : sbire ELITE vaincu -> soin de 1 et carte de boost",
       "Meme Reponse forcee que gs195 (expert, stade II)",
       [SANS_STARFORCE_EN_JEU, SANS_TANK, "Puzzle.Damage('gs196', 1)", "Puzzle.Damage('gs196', 3)", "Puzzle.PutIntoPlay('gs214')", *NEUTRE],
       ["Puzzle.Damage('gs214', 8)"],
       {"degats": [["gs196", 2]], "boost_du_mechant": 1},
       scenario=SIX),
    _c("gs196 Supreme Intelligence II : sbire KREE non ELITE vaincu -> soin de 1, pas de boost",
       "Kree Infantry vaincu au stade II",
       [SANS_STARFORCE_EN_JEU, SANS_TANK, "Puzzle.Damage('gs196', 1)", "Puzzle.Damage('gs196', 3)", "Puzzle.PutIntoPlay('gs202')", *NEUTRE],
       ["Puzzle.Damage('gs202', 5)"],
       {"degats": [["gs196", 2]], "boost_du_mechant": 0},
       scenario=SIX),
    _c("gs197 Supreme Intelligence III : un sbire KREE NON ELITE vaincu -> soin de 1 ET carte de boost (aucune condition)",
       "« heal 1 damage from the villain and give it a facedown boost card » : Kree Infantry suffit au stade III",
       [SANS_STARFORCE_EN_JEU, SANS_TANK, "Puzzle.AdvanceVillain()", "Puzzle.Damage('gs197', 1)", "Puzzle.Damage('gs197', 3)", "Puzzle.PutIntoPlay('gs202')",
        *NEUTRE],
       ["Puzzle.Damage('gs202', 5)"],
       {"degats": [["gs197", 2]], "boost_du_mechant": 1, "pv_max": [["gs197", 15]]},
       scenario=SIX),
    # ===================================================================== complots principaux
    _c("gs198b Protectors 1B : complete -> toute la menace part, un STARFORCE mis de cote entre en jeu (9 -> 8), pas d'avance",
       "Forced Interrupt : menace 5 + escalade 2 = 7 >= 6 a l'etape 1 : au lieu d'etre complete, 0 menace et un sbire de "
       "plus ; 8 de cote > 5 : on reste en 1B",
       [SANS_STARFORCE_EN_JEU, "Puzzle.SetThreat('gs198b', 5)", HEROS, *NEUTRE],
       ["Puzzle.RunVillainPhase()"],
       {"menace": [["gs198b", 0]], "starforce_mis_de_cote": 8, "starforce_en_jeu": 1, "en_jeu": ["gs198b"]},
       main_exclusive=["01088"]),
    _c("gs198b Protectors 1B : 6 STARFORCE de cote -> la completion en met un en jeu, il en reste 5 : avance en 2A -> 2B",
       "« Then, if there are 5 or less set aside STARFORCE minions, advance to stage 2A » ; 2A remelange les 5 restants "
       "dans le deck rencontre (0 de cote) ; le complot en jeu est 2B (1 menace par joueur)",
       [SANS_STARFORCE_EN_JEU, "Puzzle.Remove('gs204')", "Puzzle.Remove('gs204')", "Puzzle.Remove('gs213')", "Puzzle.SetThreat('gs198b', 5)", *NEUTRE],
       ["Puzzle.RunVillainPhase()"],
       {"starforce_mis_de_cote": 0, "complot": "gs199b"},
       main_exclusive=["01088"]),
    _c("gs198b Protectors 1B : l'objectif de menace ne peut pas etre modifie (une modification de +3 est ignoree)",
       "« The target threat value of this scheme cannot be changed » : `Gain(target_threat=3)` sur 1B laisse l'objectif a 6",
       [SANS_STARFORCE_EN_JEU], [],
       {"objectif_apres_gain": [3, 6]}),
    _c("gs199a The Endless Mind 2A : revele -> chaque STARFORCE mis de cote est melange dans le deck rencontre",
       "When Revealed : 9 sbires de cote -> 0, tous dans le deck rencontre",
       [SANS_STARFORCE_EN_JEU, *NEUTRE], ["Puzzle.AdvanceMainScheme()"],
       {"starforce_mis_de_cote": 0, "starforce_dans_deck": 9, "complot": "gs199b"}),
    _c("gs199b The Endless Mind 2B : 11 menaces par joueur = defaite des joueurs",
       "« If this stage is completed, the players lose the game » (coquille « completes » corrigee) : la menace atteint "
       "l'objectif a la phase du mechant -> partie perdue",
       [SANS_STARFORCE_EN_JEU, *NEUTRE, "Puzzle.AdvanceMainScheme()", "Puzzle.SetThreat('gs199b', 10)"],
       ["Puzzle.RunVillainPhase()"],
       {"partie_perdue": True},
       main_exclusive=["01088"], declencher_tolerant=["Puzzle.RunVillainPhase()"]),
    # ===================================================================== Holding Tank
    _c("gs200 Holding Tank : l'attaque du heros (2) sur le mechant est reduite de 2 -> 0 degat, aucun pion retire",
       "« Reduce the amount of damage the villain takes from each attack by 2 » ; « After an enemy takes ANY amount of "
       "damage » : 0 degat = pas de pion retire (7 restent)",
       [SANS_STARFORCE_EN_JEU, HEROS, *NEUTRE], ["Puzzle.Attack('01001a')"],
       {"degats": [["gs195", 0]], "compteurs": [["gs200", "integrity", 7]]},
       cibles=["gs195"], main_exclusive=["01088"]),
    _c("gs200 Holding Tank : des degats HORS attaque (3) ne sont pas reduits, et retirent 1 pion",
       "« from each ATTACK » : 3 degats d'effet passent en entier ; un ennemi a subi des degats -> 6 pions",
       [SANS_STARFORCE_EN_JEU, *NEUTRE], ["Puzzle.Damage('gs195', 3)"],
       {"degats": [["gs195", 3]], "compteurs": [["gs200", "integrity", 6]]}),
    _c("gs200 Holding Tank : un SBIRE qui subit des degats retire aussi 1 pion",
       "« After an ENEMY takes any amount of damage » : Kree Infantry prend 1 degat -> 6 pions",
       [SANS_STARFORCE_EN_JEU, "Puzzle.PutIntoPlay('gs202')", *NEUTRE], ["Puzzle.Damage('gs202', 1)"],
       {"compteurs": [["gs200", "integrity", 6]], "degats": [["gs202", 1]]}),
    _c("gs200 Holding Tank : le dernier pion retire -> la carte quitte le jeu, l'attaque suivante n'est plus reduite",
       "Uses : au dernier pion la carte part (base native) ; 1 pion restant, 1 degat d'effet -> Tank parti ; attaque de "
       "Spider-Man (2) ensuite : 2 degats en plus (3 au total)",
       [SANS_STARFORCE_EN_JEU, HEROS, "Puzzle.Counter('gs200', 'integrity', -6)", *NEUTRE],
       ["Puzzle.Damage('gs195', 1)", "Puzzle.Attack('01001a')"],
       {"degats": [["gs195", 3]], "hors_jeu": ["gs200"]},
       cibles=["gs195"], main_exclusive=["01088"]),
    # ===================================================================== rencontres du scenario
    _c("gs201 Genetic Augmentation : s'attache au sbire KREE aux PV restants les plus eleves : +2 PV et trait ELITE, +1 ATK",
       "Kree Infantry (5 PV) et Ren-Varr endommage (5-3 = 2 restants) : Infantry recoit l'attachement -> 7 PV, ELITE, ATK 3",
       [SANS_STARFORCE_EN_JEU, "Puzzle.PutIntoPlay('gs202')", "Puzzle.PutIntoPlay('gs203')", "Puzzle.Damage('gs203', 3)",
        *NEUTRE],
       ["Puzzle.Reveal('gs201')"],
       {"accroche_a": [["gs201", "gs202"]], "pv_max": [["gs202", 7]], "traits_de": [["gs202", "ELITE"]],
        "attributs_carte": [["gs202", "attack", 1]]}),
    _c("gs201 Genetic Augmentation : aucun sbire KREE en jeu -> Renfort (la carte suivante du deck est revelee)",
       "« Otherwise, this card gains surge » : deck = Kree Infantry au-dessus : elle est revelee par le Renfort",
       [SANS_STARFORCE_EN_JEU, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', 'gs202')"],
       ["Puzzle.Reveal('gs201')"],
       {"en_jeu": ["gs202"], "carte_du_surge": "gs202"},
       declencher_tolerant=["Puzzle.Reveal('gs201')"]),
    _c("gs202 Kree Infantry : vaincu -> 2 menaces sur le complot principal",
       "When Defeated : menace de 1B 0 -> 2",
       [SANS_STARFORCE_EN_JEU, "Puzzle.PutIntoPlay('gs202')", *NEUTRE], ["Puzzle.Damage('gs202', 5)"],
       {"menace": [["gs198b", 2]], "hors_jeu": ["gs202"]}),
    _c("gs202 Kree Infantry : Garde et Patrouille portees (bases desc)",
       "Guard. Patrol. : icones lues sur la carte en jeu",
       [SANS_STARFORCE_EN_JEU, "Puzzle.PutIntoPlay('gs202')", *NEUTRE], [],
       {"mots_cles": [["gs202", "guard", 1], ["gs202", "patrol", 1]]}),
    _c("gs203 Ren-Varr : vaincu -> le mechant recoit une carte Tenace",
       "When Defeated : gs195 sans Tenace -> Tenace",
       [SANS_STARFORCE_EN_JEU, "Puzzle.PutIntoPlay('gs203')", *NEUTRE], ["Puzzle.Damage('gs203', 5)"],
       {"statuts": [["gs195", "Tough"]], "hors_jeu": ["gs203"]}),
    _c("gs203 Ren-Varr : Vulnerable -> etourdi il est DEFAUSSE (pas vaincu) : pas de carte Tenace",
       "Vulnerable (livret p.3) : defausse, « not considered defeated » : son When Defeated ne part pas",
       [SANS_STARFORCE_EN_JEU, "Puzzle.PutIntoPlay('gs203')", *NEUTRE], ["Puzzle.Stun(Puzzle.FindFaceInPlay('gs203'))"],
       {"statuts_absents": [["gs195", "Tough"]], "hors_jeu": ["gs203"]}),
    _c("gs204 Supremor : +1 PV par sbire KREE dans la pile de victoire (2 Starforce -> 5 PV)",
       "★ Supremor gets +1 hit point for each KREE minion in the victory display : 3 + 2",
       [SANS_STARFORCE_EN_JEU, "Puzzle.MoveTo('gs209', 'VictoryDisplay')", "Puzzle.MoveTo('gs210', 'VictoryDisplay')",
        "Puzzle.PutIntoPlay('gs204')", *NEUTRE], [],
       {"pv_max": [["gs204", 5]]}),
    _c("gs204 Supremor : un sbire KREE ARRIVE en vitrine apres son entree en jeu -> +1 PV (suivi continu)",
       "Supremor en jeu (3 PV), Kree Infantry vaincu (Victory ? non : il va en defausse) puis Ronan vaincu -> vitrine : 4 PV",
       [SANS_STARFORCE_EN_JEU, "Puzzle.PutIntoPlay('gs204')", "Puzzle.PutIntoPlay('gs214')", *NEUTRE],
       ["Puzzle.Damage('gs214', 8)"],
       {"pv_max": [["gs204", 4]], "vitrine": ["gs214"]}),
    _c("gs205 Loyalty to Supremor : chaque sbire gagne Garde (meme non KREE)",
       "« Each minion gains guard » : Hydra Mercenary 01101 a deja Garde ; Ren-Varr (sans Garde imprimee) l'obtient",
       [SANS_STARFORCE_EN_JEU, "Puzzle.PutIntoPlay('gs203')", *NEUTRE], ["Puzzle.Reveal('gs205')"],
       {"mots_cles": [["gs203", "guard", 1]], "en_jeu": ["gs205"]}),
    _c("gs206 Selective Breeding : revele -> chaque sbire KREE de la defausse rencontre est melange dans le deck",
       "Defausse : 2 Kree Infantry + 1 Hydra Mercenary (pas KREE) -> les 2 Infantry rejoignent le deck, le Mercenary reste",
       [SANS_STARFORCE_EN_JEU, *NEUTRE, "Puzzle.CreateEncounterDiscardPile('gs202', 'gs202', '01101')"],
       ["Puzzle.Reveal('gs206')"],
       {"dans_deck_rencontre": ["gs202"], "defausse_rencontre_ids": ["01101"], "absents_defausse_rencontre": ["gs202"]}),
    _c("gs207 Supremor Seed : dejoue -> le joueur peut placer un sbire KREE de la vitrine dans la defausse rencontre",
       "When Defeated : Ronan en vitrine -> defausse rencontre",
       [SANS_STARFORCE_EN_JEU, *NEUTRE, "Puzzle.MoveTo('gs214', 'VictoryDisplay')", "Puzzle.PutIntoPlay('gs207')", "Puzzle.SetThreat('gs207', 1)", HEROS],
       ["Puzzle.Thwart('01001a')"],
       {"hors_vitrine": ["gs214"], "defausse_rencontre_ids": ["gs214"], "hors_jeu": ["gs207"]},
       cibles=["gs207"], main_exclusive=["01088"], choisir_option=["Place Ronan the Accuser in the encounter discard pile"]),
    _c("gs207 Supremor Seed : refus (« may ») -> le sbire reste dans la pile de victoire",
       "contre-cas « MAY » : option Cancel",
       [SANS_STARFORCE_EN_JEU, *NEUTRE, "Puzzle.MoveTo('gs214', 'VictoryDisplay')", "Puzzle.PutIntoPlay('gs207')", "Puzzle.SetThreat('gs207', 1)", HEROS],
       ["Puzzle.Thwart('01001a')"],
       {"vitrine": ["gs214"], "hors_jeu": ["gs207"]},
       cibles=["gs207"], main_exclusive=["01088"], choisir_option=["Cancel"]),
    _c("gs208 Summon Reinforcements : au moins 1 STARFORCE de cote -> le mechant manigance (2 menaces sur 1B)",
       "SCH 2, deck neutre (aucun boost) : menace de 1B 0 -> 2",
       [SANS_STARFORCE_EN_JEU, *NEUTRE], ["Puzzle.Reveal('gs208')"],
       {"menace": [["gs198b", 2]]}),
    _c("gs208 Summon Reinforcements : aucun STARFORCE de cote -> on defausse jusqu'a un sbire et on le revele",
       "Otherwise : 10 STARFORCE retires ; deck : 01105, 01105 puis Kree Infantry -> Infantry revelee (en jeu), 1B a 0",
       [SANS_STARFORCE_EN_JEU, *["Puzzle.Remove('%s')" % i for i in ("gs204", "gs204", "gs210", "gs211", "gs212", "gs213", "gs214", "gs215", "gs216")],
        "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('gs202', '01105', '01105')"],
       ["Puzzle.Reveal('gs208')"],
       {"en_jeu": ["gs202"], "menace": [["gs198b", 0]], "starforce_mis_de_cote": 0}),
    _c("gs198b TEMOIN : sur 2B (sans la phrase), la meme modification de +3 passe (11 -> 14)",
       "Contre-cas du verrou : l'ajout moteur ne touche que le complot qui imprime « cannot be changed »",
       [SANS_STARFORCE_EN_JEU, *NEUTRE, "Puzzle.AdvanceMainScheme()"], [],
       {"complot": "gs199b", "objectif_apres_gain": [3, 14]}),
    # ===================================================================== Starforce (scenario d'essai Rhino)
    _c("gs209 Cadmi-M : en pile de victoire -> le mechant gagne Riposte 1 ; Cadmi-M porte Riposte 1 en jeu",
       "« While Cadmi-M is in the victory display, the villain gains retaliate 1 » ; Rhino imprime 0",
       ["Puzzle.PutIntoPlay(\'gs209\')", "Puzzle.Damage(\'gs209\', 8)", "Puzzle.PutIntoPlay('gs212')"], [],
       {"mots_cles": [["01094", "retaliate", 1], ["gs212", "retaliate", 1]]},
       scenario=ESSAI),
    _c("gs209 Cadmi-M TEMOIN : hors de la pile de victoire (en jeu) -> le mechant n'a pas Riposte",
       "Contre-cas « WHILE in the victory display » : Cadmi-M en jeu ne donne rien au mechant",
       ["Puzzle.PutIntoPlay('gs209')"], [],
       {"mots_cles": [["01094", "retaliate", 0], ["gs209", "retaliate", 1]]},
       scenario=ESSAI),
    _c("gs212 Korath : en pile de victoire avec Cadmi-M -> Riposte 2 (les bonus s'additionnent)",
       "Deux sources « gains retaliate 1 »",
       ["Puzzle.PutIntoPlay(\'gs209\')", "Puzzle.Damage(\'gs209\', 8)", "Puzzle.PutIntoPlay(\'gs212\')", "Puzzle.Damage(\'gs212\', 8)"], [],
       {"mots_cles": [["01094", "retaliate", 2]]},
       scenario=ESSAI),
    _c("gs210 Doctor Minerva : en pile de victoire -> le mechant gagne +1 SCH",
       "« the villain gets +1 SCH »",
       ["Puzzle.PutIntoPlay(\'gs210\')", "Puzzle.Damage(\'gs210\', 8)"], [],
       {"attributs_carte": [["01094", "scheme", 1], ["01094", "attack", 0]]},
       scenario=ESSAI),
    _c("gs211 Inndig-O : en pile de victoire -> le mechant gagne +1 ATK",
       "« the villain gets +1 ATK »",
       ["Puzzle.PutIntoPlay(\'gs211\')", "Puzzle.Damage(\'gs211\', 8)"], [],
       {"attributs_carte": [["01094", "attack", 1], ["01094", "scheme", 0]]},
       scenario=ESSAI),
    _c("gs214 Ronan : en pile de victoire avec Inndig-O -> +2 ATK",
       "Deux sources « gets +1 ATK »",
       ["Puzzle.PutIntoPlay(\'gs211\')", "Puzzle.Damage(\'gs211\', 8)", "Puzzle.PutIntoPlay(\'gs214\')", "Puzzle.Damage(\'gs214\', 8)"], [],
       {"attributs_carte": [["01094", "attack", 2]]},
       scenario=ESSAI),
    _c("gs214 Ronan TEMOIN : retire de la pile de victoire par Supremor Seed (gs207) -> le bonus tombe",
       "Ronan vaincu (vitrine, +1 ATK) puis Supremor Seed dejoue : Ronan va dans la defausse rencontre, Rhino revient a ATK 2",
       [*NEUTRE, "Puzzle.PutIntoPlay(\'gs214\')", "Puzzle.Damage(\'gs214\', 8)", "Puzzle.PutIntoPlay('gs207')",
        "Puzzle.SetThreat('gs207', 1)", HEROS], ["Puzzle.Thwart('01001a')"],
       {"attributs_carte": [["01094", "attack", 0]], "hors_vitrine": ["gs214"], "defausse_rencontre_ids": ["gs214"]},
       scenario=ESSAI, cibles=["gs207"], main_exclusive=["01088"],
       choisir_option=["Place Ronan the Accuser in the encounter discard pile"]),
    _c("gs213 Protector : en pile de victoire -> le mechant gagne Solide (steady) ; Protector est Solide",
       "« the villain gains steady »",
       ["Puzzle.PutIntoPlay(\'gs213\')", "Puzzle.Damage(\'gs213\', 8)", "Puzzle.PutIntoPlay('gs211')"], [],
       {"mots_cles": [["01094", "steady", 1]]},
       scenario=ESSAI),
    _c("gs213 Protector : en jeu, Solide imprime (desc) : un Sonne ne l'etourdit pas encore",
       "Steady (base desc) : 1 carte Sonne posee, le sbire reste actif (il en faut 2)",
       ["Puzzle.PutIntoPlay('gs213')", "Puzzle.Stun(Puzzle.FindFaceInPlay('gs213'))"], [],
       {"mots_cles": [["gs213", "steady", 1]]},
       scenario=ESSAI),
    _c("gs215 Shatterax : ses attaques gagnent Percant -> la carte Tenace du heros est defaussee, 1 degat",
       "★ Shatterax's attacks gain piercing : Spider-Man Tenace, attaque de 1 : Tenace defaussee AVANT les degats",
       ["Puzzle.PutIntoPlay('gs215')", "Puzzle.Tough('01001b')", *NEUTRE], ["Puzzle.Attack('gs215')"],
       {"degats_identite": 1, "statuts_absents": [["01001b", "Tough"]]},
       scenario=ESSAI, main_exclusive=["01088"]),
    _c("gs215 Shatterax : en pile de victoire -> les attaques du MECHANT gagnent Percant",
       "Rhino (ATK 2) attaque Peter Parker (alter ego : pas de defense) Tenace : Tenace defaussee, 2 degats",
       ["Puzzle.PutIntoPlay(\'gs215\')", "Puzzle.Damage(\'gs215\', 8)", "Puzzle.Tough('01001b')", *NEUTRE], ["Puzzle.Attack('01094')"],
       {"degats_identite": 2, "statuts_absents": [["01001b", "Tough"]]},
       scenario=ESSAI, main_exclusive=["01088"]),
    _c("gs215 Shatterax TEMOIN : Shatterax en jeu (pas en vitrine) -> l'attaque de Rhino est absorbee par la Tenace",
       "Contre-cas : sans Percant, la Tenace absorbe tout",
       ["Puzzle.PutIntoPlay('gs215')", "Puzzle.Tough('01001b')", *NEUTRE], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0},
       scenario=ESSAI, main_exclusive=["01088"]),
    _c("gs216 Ultimus : en pile de victoire -> l'attaque du MECHANT gagne Debordement (allie defenseur, l'exces au heros)",
       "Rhino ATK 2 + Inndig-O en vitrine (+1) = 3 contre Black Cat 01002 (2 PV) : 1 degat d'exces sur Spider-Man",
       [HEROS, "Puzzle.PutIntoPlay(\'gs216\')", "Puzzle.Damage(\'gs216\', 8)", "Puzzle.PutIntoPlay(\'gs211\')", "Puzzle.Damage(\'gs211\', 8)",
        "Puzzle.PutIntoPlay('01002', under_control=True)", *NEUTRE], ["Puzzle.Attack('01094', '01002')"],
       {"degats_identite": 1},
       scenario=ESSAI, main_exclusive=["01088"]),
    _c("gs216 Ultimus TEMOIN : sans Ultimus en vitrine, l'exces sur l'allie est perdu",
       "Meme montage sans Ultimus : 0 degat sur Spider-Man",
       [HEROS, "Puzzle.PutIntoPlay(\'gs211\')", "Puzzle.Damage(\'gs211\', 8)", "Puzzle.PutIntoPlay('01002', under_control=True)", *NEUTRE],
       ["Puzzle.Attack('01094', '01002')"],
       {"degats_identite": 0},
       scenario=ESSAI, main_exclusive=["01088"]),
    _c("gs216 Ultimus : ses propres attaques gagnent Debordement (ATK 2 avec Genetic Augmentation contre Black Cat blessee)",
       "★ Ultimus's attacks gain overkill : Ultimus +1 ATK (gs201, seul sbire KREE) = 2 contre Black Cat a 1 PV restant : 1 au heros",
       [HEROS, "Puzzle.PutIntoPlay('gs216')", "Puzzle.Reveal('gs201')", "Puzzle.PutIntoPlay('01002', under_control=True)",
        "Puzzle.Damage('01002', 1)", *NEUTRE], ["Puzzle.Attack('gs216', '01002')"],
       {"degats_identite": 1, "accroche_a": [["gs201", "gs216"]]},
       scenario=ESSAI, main_exclusive=["01088"]),
    _c("gs217 Starformation : un sbire STARFORCE en jeu -> il recoit une carte Tenace et une carte de boost face cachee",
       "« Give each STARFORCE minion a tough status card and a facedown boost card » : Ronan en jeu",
       ["Puzzle.PutIntoPlay('gs214')", *NEUTRE], ["Puzzle.Reveal('gs217')"],
       {"statuts": [["gs214", "Tough"]], "statuts_absents": [["01094", "Tough"]], "boosts_sur": [["gs214", 1]]},
       scenario=ESSAI),
    _c("gs217 Starformation : aucun STARFORCE en jeu -> le MECHANT recoit la Tenace et la carte de boost",
       "« Otherwise, give the villain a tough status card and a facedown boost card »",
       [*NEUTRE], ["Puzzle.Reveal('gs217')"],
       {"statuts": [["01094", "Tough"]], "boost_du_mechant": 1},
       scenario=ESSAI),
    # ===================================================================== Seeds of Corruption (essai Rhino)
    _c("gs218 Manipulated Memories : attachee a l'identite ; un evenement paye SANS ressource mentale ne se joue pas",
       "« Each event card in your hand gains requirement ([mental]) » : Haymaker (2) avec Strength (RR) seulement : reste en main",
       [HEROS, *NEUTRE, "Puzzle.Reveal('gs218')"], [],
       {"en_main": ["01087"], "degats": [["01094", 0]], "accroche_a": [["gs218", "01001a"]]},
       scenario=ESSAI, main_exclusive=["01087", "01090"], jouer=["01087"], cibles=["01094"]),
    _c("gs218 Manipulated Memories TEMOIN : sans l'attachement, Haymaker se paie avec Strength (3 degats)",
       "Contre-cas : le meme paiement passe",
       [HEROS, *NEUTRE], [],
       {"degats": [["01094", 3]]},
       scenario=ESSAI, main_exclusive=["01087", "01090"], jouer=["01087"], cibles=["01094"]),
    _c("gs218 Manipulated Memories : payer AVEC une ressource mentale (Genius BB) -> Haymaker se joue (3 degats)",
       "Requirement = contrainte de couleur incluse dans le cout (2 dont 1 mentale), pas un cout en plus",
       [HEROS, *NEUTRE, "Puzzle.Reveal('gs218')"], [],
       {"degats": [["01094", 3]]},
       scenario=ESSAI, main_exclusive=["01087", "01089"], jouer=["01087"], cibles=["01094"]),
    _c("gs218 Manipulated Memories : un ALLIE n'est pas touche (Hulk 01050 paye avec Strength entre en jeu)",
       "« each EVENT card » : contre-cas sur un allie",
       [HEROS, *NEUTRE, "Puzzle.Reveal('gs218')"], [],
       {"en_jeu": ["01050"]},
       scenario=ESSAI, main_exclusive=["01050", "01090"], jouer=["01050"]),
    _c("gs218 Manipulated Memories : Action de heros (2 ressources du meme type) -> defaussee",
       "« Hero Action: Spend 2 resources of the same type → discard this card »",
       [HEROS, *NEUTRE, "Puzzle.Reveal('gs218')"], ["Puzzle.Action('gs218', 'HeroAction')"],
       {"hors_jeu": ["gs218"]},
       scenario=ESSAI, main_exclusive=["01090"]),
    _c("gs218 Manipulated Memories ★ Boost : activation = MANIGANCE (alter ego) -> le joueur est Desoriente",
       "« If this activation is a scheme, you are confused »",
       [*NEUTRE], ["Puzzle.Boost('gs218')"],
       {"statuts": [["01001b", "Confused"]], "statuts_absents": [["01001b", "Stunned"]]},
       scenario=ESSAI, main_exclusive=["01088"]),
    _c("gs218 Manipulated Memories ★ Boost : activation = ATTAQUE (heros) -> le joueur est Sonne",
       "« Otherwise, you are stunned »",
       [HEROS, *NEUTRE], ["Puzzle.Boost('gs218')"],
       {"statuts": [["01001a", "Stunned"]], "statuts_absents": [["01001a", "Confused"]]},
       scenario=ESSAI, main_exclusive=["01088"]),
    _c("gs219 Psychic Shackles : une carte a ressource mentale imprimee ne se joue pas (Maria Hill 01067)",
       "« Players cannot play cards with a printed [mental] resource » ; Hinder 1 : 3 + 1 = 4 menaces",
       [*NEUTRE, "Puzzle.Reveal('gs219')"], [],
       {"en_main": ["01067"], "menace": [["gs219", 4]]},
       scenario=ESSAI, main_exclusive=["01067", "01090"], jouer=["01067"]),
    _c("gs219 Psychic Shackles TEMOIN : une carte SANS icone mentale se joue (Hulk 01050, icone energie)",
       "Contre-cas : seules les icones mentales imprimees sont bloquees",
       [*NEUTRE, "Puzzle.Reveal('gs219')"], [],
       {"en_jeu": ["01050"]},
       scenario=ESSAI, main_exclusive=["01050", "01090"], jouer=["01050"]),
    _c("gs219 Psychic Shackles TEMOIN 2 : sans le complot, Maria Hill se joue",
       "Contre-cas du blocage",
       [*NEUTRE], [],
       {"en_jeu": ["01067"]},
       scenario=ESSAI, main_exclusive=["01067", "01090"], jouer=["01067"]),
    _c("gs220 Mental Torture : la carte defaussee au hasard porte une ressource mentale -> identite Sonnee",
       "Main = Genius (BB) seul : defausse, Spider-Man Sonne",
       [*NEUTRE], ["Puzzle.Reveal('gs220')"],
       {"statuts": [["01001b", "Stunned"]], "taille_main": 0},
       scenario=ESSAI, main_exclusive=["01089"]),
    _c("gs220 Mental Torture TEMOIN : la carte defaussee n'a pas d'icone mentale -> pas Sonne",
       "Main = Strength (RR) seul : defausse, aucun statut",
       [*NEUTRE], ["Puzzle.Reveal('gs220')"],
       {"statuts_absents": [["01001b", "Stunned"]], "taille_main": 0},
       scenario=ESSAI, main_exclusive=["01090"]),
    _c("gs221 Whisper in the Mind : l'obligation du joueur (Eviction Notice) est trouvee dans le deck rencontre et revelee",
       "« Find a copy of your obligation and reveal it » : 01165 quitte le deck rencontre, pas de Renfort",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01165')"], ["Puzzle.Reveal('gs221')"],
       {"absent_deck_rencontre": ["01165"]},
       scenario=ESSAI, declencher_tolerant=["Puzzle.Reveal('gs221')"]),
    _c("gs221 Whisper in the Mind : obligation introuvable -> Renfort",
       "« If your obligation was not revealed this way, this card gains surge » : deck sans 01165, le dessus est revele",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', 'gs202')", "Puzzle.Remove('01165')"],
       ["Puzzle.Reveal('gs221')"],
       {"carte_du_surge": "gs202", "en_jeu": ["gs202"]},
       scenario=ESSAI, declencher_tolerant=["Puzzle.Reveal('gs221')"]),
    _c("gs221 Whisper in the Mind ★ Boost : l'obligation dans la pile de victoire est melangee dans le deck rencontre",
       "« If your obligation is in the victory display ... shuffle it into the encounter deck »",
       [*NEUTRE, "Puzzle.MoveTo('01165', 'VictoryDisplay')"], ["Puzzle.Boost('gs221')"],
       {"hors_vitrine": ["01165"], "dans_deck_rencontre": ["01165"]},
       scenario=ESSAI, main_exclusive=["01088"]),
    _c("gs221 Whisper in the Mind ★ Boost : l'obligation RETIREE du jeu revient aussi dans le deck rencontre",
       "« ... or if it was removed from the game »",
       [*NEUTRE, "Puzzle.MoveTo('01165', 'RemovedArea')"], ["Puzzle.Boost('gs221')"],
       {"dans_deck_rencontre": ["01165"]},
       scenario=ESSAI, main_exclusive=["01088"]),
    # ===================================================================== Nega-Bomb (essai Rhino)
    _c("gs222a Nega-Bomb : Setup -> en jeu des la mise en place, 8 menaces (1 joueur), 4 pions time",
       "Setup (base desc) + « Enters play with 4 time counters on it » ; StartingThreat 8[per_hero]",
       [], [],
       {"en_jeu": ["gs222a"], "menace": [["gs222a", 8]], "compteurs": [["gs222a", "time", 4]]},
       scenario=ESSAI),
    _c("gs222a Nega-Bomb : apres l'etape 1 de la phase du mechant, un pion time part (4 -> 3)",
       "Forced Response : un seul pion retire par phase, la carte reste recto",
       [*NEUTRE], ["Puzzle.RunVillainPhase()"],
       {"compteurs": [["gs222a", "time", 3]], "en_jeu": ["gs222a"]},
       scenario=ESSAI, main_exclusive=["01088"]),
    _c("gs222a/gs222b Nega-Bomb : dernier pion -> retournee, Detonation : X = ceil(7 / 3) = 3 a chaque ami et sbire, Tenace ignoree",
       "Spider-Man (Tenace), Black Cat et Hydra Mercenary : 3 cibles, 7 menaces -> 3 degats chacun ; Detonation retiree du jeu",
       ["Puzzle.Counter('gs222a', 'time', -3)", "Puzzle.SetThreat('gs222a', 7)", "Puzzle.PutIntoPlay('01002', under_control=True)",
        "Puzzle.PutIntoPlay('01101')", "Puzzle.Tough('01001b')", *NEUTRE], ["Puzzle.RunVillainPhase()"],
       {"degats_identite": 3, "hors_jeu": ["01002", "01101", "gs222a"], "retires_du_jeu": ["gs222b"]},
       scenario=ESSAI, main_exclusive=["01088"]),
    _c("gs223 Green Interference : retire 1 compteur polyvalent de CHAQUE carte en jeu (Nega-Bomb 4 -> 3, sbire 2 -> 1)",
       "« Remove 1 all-purpose counter from each card in play » ; pas de Renfort (des compteurs ont ete retires)",
       [*NEUTRE, "Puzzle.PutIntoPlay('01101')", "Puzzle.Counter('01101', 'counter', 2)"], ["Puzzle.Reveal('gs223')"],
       {"compteurs": [["gs222a", "time", 3], ["01101", "counter", 1]]},
       scenario=ESSAI),
    _c("gs223 Green Interference : aucun compteur en jeu -> Renfort",
       "« If no counter was removed this way, this card gains surge » : Nega-Bomb retiree, le dessus du deck est revele",
       ["Puzzle.Remove('gs222a')", "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', 'gs202')"],
       ["Puzzle.Reveal('gs223')"],
       {"carte_du_surge": "gs202"},
       scenario=ESSAI, declencher_tolerant=["Puzzle.Reveal('gs223')"]),
    _c("gs223 Green Interference ★ Boost : retire 1 compteur d'UNE carte en jeu (Nega-Bomb 4 -> 3)",
       "« Remove 1 all-purpose counter from a card in play » ; une seule carte a compteurs : pas de choix",
       [*NEUTRE], ["Puzzle.Boost('gs223')"],
       {"compteurs": [["gs222a", "time", 3]]},
       scenario=ESSAI, main_exclusive=["01088"]),
]

VERIFICATIONS = r'''
def _gs8_ids(faces):
    return [getattr(f.paper, "card_id", None) for f in faces]

def _gs8_mis_de_cote_starforce(monde):
    return [f for f in monde.aside_deck.Get(True) if f.HasTrait("STARFORCE")]

_GS8_PROPRES = {"starforce_mis_de_cote", "starforce_en_jeu", "starforce_dans_deck", "boost_du_mechant", "vitrine",
                "hors_vitrine", "complot", "objectif", "partie_perdue", "mots_cles", "defausse_rencontre_ids",
                "absents_defausse_rencontre", "retires_du_jeu", "engages", "objectif_apres_gain", "absent_deck_rencontre"}

def gs8_etat(monde, aides):
    """Etat du lot GS-8, puis delegation a etat_attendu pour les cles communes.
    starforce_mis_de_cote / starforce_en_jeu / starforce_dans_deck : nombres de sbires STARFORCE ; boost_du_mechant :
    cartes de boost du mechant ; vitrine / hors_vitrine : ids dans (hors de) la pile de victoire ; complot : id du complot
    principal en jeu ; objectif : objectif de menace du complot principal ; partie_perdue ; mots_cles : [[id, attribut,
    valeur]] (guard, patrol, retaliate, steady...) ; defausse_rencontre_ids / absents_defausse_rencontre ; retires_du_jeu."""
    from game.operate.worlds import Worlds
    attendu = aides["cas"].get("attendu") or {}
    soucis = []
    if "starforce_mis_de_cote" in attendu:
        n = len(_gs8_mis_de_cote_starforce(monde))
        if n != attendu["starforce_mis_de_cote"]:
            soucis.append(f"{n} sbire(s) STARFORCE mis de cote {_gs8_ids(_gs8_mis_de_cote_starforce(monde))} (attendu {attendu['starforce_mis_de_cote']})")
    if "starforce_en_jeu" in attendu:
        en_jeu = [f for f in Worlds.GetOnFieldCards(monde.players[0].GetIdentity().card.game_area) if f.IsInPlay() and f.HasTrait("STARFORCE")]
        if len(en_jeu) != attendu["starforce_en_jeu"]:
            soucis.append(f"{len(en_jeu)} sbire(s) STARFORCE en jeu {_gs8_ids(en_jeu)} (attendu {attendu['starforce_en_jeu']})")
    if "starforce_dans_deck" in attendu:
        deck = [f for f in Worlds.GetEncounterDeckCards(monde) if f.HasTrait("STARFORCE")]
        if len(deck) != attendu["starforce_dans_deck"]:
            soucis.append(f"{len(deck)} sbire(s) STARFORCE dans le deck rencontre (attendu {attendu['starforce_dans_deck']})")
    if "boost_du_mechant" in attendu:
        mechant = Worlds.GetAllVillains(monde)[0]
        pile = [getattr(f.paper, "card_id", "?") for f in mechant.components.boostable.GetDeck().Get(True)]
        if len(pile) != attendu["boost_du_mechant"]:
            soucis.append(f"pile de boost du mechant = {pile} (attendu {attendu['boost_du_mechant']} carte(s))")
    vitrine = _gs8_ids(monde.victory_display.GetAll())
    for i in attendu.get("vitrine") or []:
        if i not in vitrine:
            soucis.append(f"{i} absent de la pile de victoire {vitrine}")
    for i in attendu.get("hors_vitrine") or []:
        if i in vitrine:
            soucis.append(f"{i} encore dans la pile de victoire {vitrine}")
    if "objectif_apres_gain" in attendu:
        # La modification est appliquee ICI (le harnais n'execute que des appels Puzzle.*) : Gain(target_threat=+N)
        # est le SEUL chemin du moteur qui modifie un objectif (face_gain.py -> GainTargetThreatValue).
        from game.effect.rule import GameRule
        gain, voulu = attendu["objectif_apres_gain"]
        complot = Worlds.GetAllMainSchemes(monde)[0]
        complot.Gain(GameRule(complot), 1, target_threat=gain)
        if complot.target_threat != voulu:
            soucis.append(f"objectif apres un gain de {gain} = {complot.target_threat} (attendu {voulu})")
    if "complot" in attendu or "objectif" in attendu:
        complot = Worlds.GetAllMainSchemes(monde)[0]
        cid = getattr(getattr(complot, "paper", None), "card_id", None)
        if "complot" in attendu and cid != attendu["complot"]:
            soucis.append(f"complot principal en jeu = {cid} (attendu {attendu['complot']})")
        if "objectif" in attendu and getattr(complot, "target_threat", None) != attendu["objectif"]:
            soucis.append(f"objectif de {cid} = {getattr(complot, 'target_threat', None)} (attendu {attendu['objectif']})")
    if "partie_perdue" in attendu:
        go = monde.game_over
        fin = go.reason
        gagne = getattr(go, "players_won", None)
        perdu = fin is not None and gagne is False
        if perdu != attendu["partie_perdue"]:
            soucis.append(f"partie perdue = {perdu} (is_game_over={fin}, is_win={gagne})")
    for card_id, attribut, valeur in attendu.get("mots_cles") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (mots_cles)")
            continue
        n = getattr(face, attribut, None)
        if n != valeur:
            soucis.append(f"{card_id}.{attribut} = {n} (attendu {valeur})")
    defausse = _gs8_ids(Worlds.GetEncounterDiscardPileCards(monde))
    for i in attendu.get("defausse_rencontre_ids") or []:
        if i not in defausse:
            soucis.append(f"{i} absent de la defausse rencontre {defausse}")
    for i in attendu.get("absents_defausse_rencontre") or []:
        if i in defausse:
            soucis.append(f"{i} encore dans la defausse rencontre {defausse}")
    deck = _gs8_ids(Worlds.GetEncounterDeckCards(monde))
    for i in attendu.get("absent_deck_rencontre") or []:
        if i in deck:
            soucis.append(f"{i} encore dans le deck rencontre")
    retires = _gs8_ids(monde.area_removed.GetAll())
    for i in attendu.get("retires_du_jeu") or []:
        if i not in retires:
            soucis.append(f"{i} n'est pas retire du jeu {retires}")
    for card_id, rang in attendu.get("engages") or []:
        face = aides["par_id"](monde, card_id)
        if face is None or getattr(face, "engaged_player", None) is not monde.players[rang]:
            soucis.append(f"{card_id} n'est pas engage avec le joueur {rang}")
    reste = {k: v for k, v in attendu.items() if k not in _GS8_PROPRES}
    if reste:
        inconnues = sorted(set(reste) - CLES_ETAT_ATTENDU)
        if inconnues:
            return False, f"cle(s) inconnue(s) : {inconnues}"
        sauve = aides["cas"]["attendu"]
        aides["cas"]["attendu"] = reste
        try:
            ok, msg = etat_attendu(monde, aides)
        finally:
            aides["cas"]["attendu"] = sauve
        if not ok:
            soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"etat conforme (vitrine {vitrine})"
'''
