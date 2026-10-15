# Cas test_capacites du bloc SKRULL PANTHEON (sk170-183) et du set modulaire DARD'VAN SECT (sk184-188).
# Format identique a tools/test_capacites.py ; noms prefixes `[pantheon]` (filtre : `[pantheon]`).
#
# Conventions de ce fichier :
#  - le heros de test (Spider-Man, 01001) demarre en ALTER EGO ; `Puzzle.ChangeForm('01001b')` le met en forme HEROS.
#  - le mechant est UNE carte double face : `sk170a` = face Kly'bn, `sk170b` = face Sl'gur't (idem 171, 172).
#    ⚠ Une fois la carte retournee, `Puzzle.*('sk170a')` ne la retrouve plus (face cachee) : viser la face VISIBLE.
#  - `NEUTRE` vide le deck rencontre (cartes melangees a la mise en place) ; chaque mesure part d'un plateau connu.
#  - ¤ Retourner le mechant dans une mise en place : `Puzzle.Reveal('sk182')` (Prayer to Sl'gur't : Sl'gur't n'est pas
#    en jeu, donc « flip the villain ») ; la face d'arrivee pose son jeton de foi (+1).
SC = "sk_skrull_pantheon"
SCE = "sk_skrull_pantheon_expert"
NEUTRE = "Puzzle.EmptyEncounterDeck()"
HEROS = "Puzzle.ChangeForm('01001b')"
VERS_SLGURT = "Puzzle.Reveal('sk182')"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[pantheon] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "pantheon_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ===================================================================== mise en place
    _c("sk170a Setup normal : Kly'bn I face visible, 1 jeton de foi, complot 1B, environnement mis de cote",
       "stade I (face Kly'bn) en jeu ; « When Revealed » : 1 jeton de foi ; sk175 (Skrull Pantheon) hors jeu, dans la zone mise de cote",
       [], [], {"mechant_id": "sk170a", "foi": 1, "en_jeu": ["sk170a", "sk173b"], "hors_jeu": ["sk170b", "sk171a", "sk175a", "sk175b"],
                "menace": [["sk173b", 6]], "aside": ["sk175a"]}),
    _c("sk171a Setup EXPERT : Kly'bn II en jeu (stade II), 1 jeton de foi",
       "mode expert : villain sk171, sk172 ; le stade I est retire",
       [], [], {"mechant_id": "sk171a", "foi": 1, "en_jeu": ["sk171a", "sk173b"], "hors_jeu": ["sk170a", "sk172a"]}, scenario=SCE),
    _c("sk173a Setup : les ensembles obligatoires sont dans le deck rencontre (Dard'van Sect, Skrull Pantheon, Standard)",
       "Contents : Skrull Pantheon, Dard'van Sect, Standard + un ensemble modulaire (Skrull Society)",
       [], [], {"dans_deck_rencontre": ["sk176", "sk177", "sk178", "sk179", "sk180", "sk181", "sk182", "sk183",
                                         "sk184", "sk185", "sk186", "sk187", "sk188", "01186", "sk107"]}),
]


SECTION_A = [
    # ===================================================================== stades du mechant (une carte, deux faces)
    _c("sk170a Changement de stade : Kly'bn I vaincu -> Kly'bn II du MEME cote (face Kly'bn), jeton de foi conserve + 1",
       "`Scenario.AdvanceVillainStage` : le stade suivant prend la face de meme nom que le stade vaincu ; foi 1 (mise en place) + 1 (When Revealed de II)",
       [NEUTRE], ["Puzzle.Damage('sk170a', 99)"], {"mechant_id": "sk171a", "foi": 2, "pv_max": [["sk171a", 18]], "degats": [["sk171a", 0]]}),
    _c("sk170b Changement de stade : Sl'gur't I vaincu -> Sl'gur't II du MEME cote (face Sl'gur't)",
       "insert p.14 : « the next stage of the villain deck enters play on the same side as the just defeated stage » ; foi 1 + 1 (flip) + 1 (II)",
       [NEUTRE, VERS_SLGURT], ["Puzzle.Damage('sk170b', 99)"], {"mechant_id": "sk171b", "foi": 3, "pv_max": [["sk171b", 18]], "degats": [["sk171b", 0]]}),
    _c("sk174b PV partages : 4 degats subis face Kly'bn restent sur la face Sl'gur't apres le retournement",
       "meme carte : le compteur de degats est celui de la carte ; PV max identiques des deux cotes (15)",
       [NEUTRE, "Puzzle.Damage('sk170a', 4)"], ["Puzzle.AdvanceMainScheme(1)"], {"mechant_id": "sk170b", "degats": [["sk170b", 4]], "pv_max": [["sk170b", 15]]}),
    _c("sk171b En vaincre un suffit : Sl'gur't II vaincu (face visible) = victoire, sans avoir touche a Kly'bn",
       "insert p.14 : « if you defeat one, you don't need to defeat the other to win the game » ; stade II = dernier stade en mode normal",
       [NEUTRE, "Puzzle.AdvanceVillain()", VERS_SLGURT], ["Puzzle.Damage('sk171b', 99)"], {"victoire": True}),
    _c("sk171a Dernier stade vaincu (face Kly'bn) : victoire des joueurs",
       "mode normal : le paquet mechant ne contient que I et II",
       [NEUTRE, "Puzzle.AdvanceVillain()"], ["Puzzle.Damage('sk171a', 99)"], {"victoire": True}),
    _c("sk171a TEMOIN : stade II blesse mais pas vaincu : pas de victoire",
       "ligne de base du precedent",
       [NEUTRE, "Puzzle.AdvanceVillain()"], ["Puzzle.Damage('sk171a', 5)"], {"victoire": False, "mechant_id": "sk171a", "degats": [["sk171a", 5]]}),
    _c("sk172a Expert : stade II vaincu -> stade III (face Kly'bn), carte d'etat Robuste donnee a la revelation",
       "mode expert : villain sk171, sk172 ; « When Revealed: place 1 faith counter on Kly'bn and give him a tough status card »",
       [NEUTRE], ["Puzzle.Damage('sk171a', 99)"], {"mechant_id": "sk172a", "foi": 2, "statuts_mechant": ["Tough"], "pv_max": [["sk172a", 20]]}, scenario=SCE),
    _c("sk172b Expert : stade II vaincu face Sl'gur't -> stade III face Sl'gur't, Robuste donnee (« give HER a tough status card »)",
       "meme texte cote Sl'gur't ; foi 1 + 1 (flip) + 1 (III)",
       [NEUTRE, VERS_SLGURT], ["Puzzle.Damage('sk171b', 99)"], {"mechant_id": "sk172b", "foi": 3, "statuts_mechant": ["Tough"], "pv_max": [["sk172b", 20]]}, scenario=SCE),
    _c("sk172a Expert : dernier stade (III) vaincu = victoire",
       "paquet expert : II puis III",
       [NEUTRE, "Puzzle.AdvanceVillain()"], ["Puzzle.Damage('sk172a', 99)", "Puzzle.Damage('sk172a', 99)"], {"victoire": True}, scenario=SCE),
    _c("sk170a PV par stade et par joueur : 15 / 18 / 20 (deux joueurs : 30 au stade I)",
       "« HIT POINTS 15 per player » imprime ; deux joueurs = 30",
       [NEUTRE], [], {"pv_max": [["sk170a", 30]]}, heros2="hawkeye"),
]

SECTION_B = [
    # ===================================================================== « Alternation of Gods » : le retournement
    _c("sk174b Retournement (« Flip the villain » de 2B) : les attachements du mechant sont defausses",
       "insert p.14 : « all attachment cards ... are discarded » ; Electricity Projection (sk148) posee sur Kly'bn, puis le stade 2B (When Revealed : flip the villain) retourne le mechant",
       [NEUTRE, "Puzzle.AttachReel('sk148', 'sk170a')"], ["Puzzle.AdvanceMainScheme(1)"], {"mechant_id": "sk170b", "attaches_mechant": [], "hors_jeu": ["sk148"]}),
    _c("sk174b TEMOIN : sans retournement l'attachement reste sur le mechant",
       "ligne de base du precedent",
       [NEUTRE, "Puzzle.AttachReel('sk148', 'sk170a')"], [], {"mechant_id": "sk170a", "attaches_mechant": ["sk148"]}),
    _c("sk174b Retournement : les cartes d'etat (Sonne, Desoriente, Robuste) sont defaussees",
       "insert p.14 : « status cards ... are discarded »",
       [NEUTRE, "Puzzle.Stun('sk170a')", "Puzzle.Confuse('sk170a')", "Puzzle.Tough('sk170a')"], ["Puzzle.AdvanceMainScheme(1)"], {"mechant_id": "sk170b", "statuts_mechant": []}),
    _c("sk174b TEMOIN : sans retournement les trois cartes d'etat restent",
       "ligne de base du precedent",
       [NEUTRE, "Puzzle.Stun('sk170a')", "Puzzle.Confuse('sk170a')", "Puzzle.Tough('sk170a')"], [], {"statuts_mechant": ["Confused", "Stunned", "Tough"]}),
    _c("sk174b Retournement : les cartes de boost face cachee du mechant sont defaussees",
       "insert p.14 : « boost cards ... are discarded » ; sk186 (Dard'van Sect) donne 1 carte de boost face cachee au mechant",
       [NEUTRE, "Puzzle.CreateEncounterDeck('sk107', 'sk107')", "Puzzle.Reveal('sk186')"], ["Puzzle.AdvanceMainScheme(1)"], {"mechant_id": "sk170b", "boosts_mechant": 0}),
    _c("sk174b TEMOIN : sans retournement la carte de boost reste au mechant",
       "ligne de base du precedent",
       [NEUTRE, "Puzzle.CreateEncounterDeck('sk107', 'sk107')", "Puzzle.Reveal('sk186')"], [], {"mechant_id": "sk170a", "boosts_mechant": 1}),
    _c("sk174b Retournement : les jetons de foi et les degats SURVIVENT, et la face d'arrivee pose son jeton (When Revealed)",
       "insert p.14 : « except for the faith counters and damage » ; foi 1 + 2 posees + 1 (When Revealed de Sl'gur't) = 4",
       [NEUTRE, "Puzzle.Counter('sk170a', 'faith', 2)", "Puzzle.Damage('sk170a', 6)"], ["Puzzle.AdvanceMainScheme(1)"],
       {"mechant_id": "sk170b", "foi": 4, "degats": [["sk170b", 6]]}),
    _c("sk170b Retournement vers Kly'bn (aller-retour) : la face Kly'bn resout SON When Revealed",
       "deux retournements : foi 1 + 1 + 1 = 3, face Kly'bn de nouveau visible",
       [NEUTRE, VERS_SLGURT], ["Puzzle.Reveal('sk181')"], {"mechant_id": "sk170a", "foi": 3}),
    _c("sk172a Retournement au stade III : Robuste defaussee puis REDONNEE par le When Revealed de la face d'arrivee",
       "expert, stade III : Sonne pose avant le retournement disparait ; Robuste revient (« give her a tough status card »)",
       [NEUTRE, "Puzzle.AdvanceVillain()", "Puzzle.Stun('sk172a')"], [VERS_SLGURT], {"mechant_id": "sk172b", "statuts_mechant": ["Tough"], "foi": 3}, scenario=SCE),
]

SECTION_C = [
    # ===================================================================== Reponse forcee : foi -> cartes distribuees
    _c("sk170a Reponse forcee Kly'bn : 1 jeton de foi = 1 carte du dessus defaussee, distribuee si ce n'est PAS une traitrise",
       "apres l'etape 1 : Hydra Mercenary (sbire) defausse du dessus, distribue au joueur, revele a l'etape 4 : il entre en jeu engage",
       [NEUTRE, HEROS, "Puzzle.CreateEncounterDeck('sk107','sk107','sk107','sk107','01101')"], ["Puzzle.RunVillainPhase()"],
       {"en_jeu": ["01101"], "foi": 1}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk170a Reponse forcee Kly'bn : une TRAITRISE defaussee n'est PAS distribuee (Exhaustion reste en defausse, le heros reste pret)",
       "foi 2 : Hydra Mercenary (dessus) + Exhaustion (dessous) sont defaussees ; seul le sbire est distribue",
       [NEUTRE, HEROS, "Puzzle.Counter('sk170a', 'faith', 1)", "Puzzle.CreateEncounterDeck('sk107','sk107','sk107','sk107','01191','01101')"], ["Puzzle.RunVillainPhase()"],
       {"en_jeu": ["01101"], "defausse_rencontre": ["01191"], "pret": ["01001a"], "foi": 2}, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk170a Reponse forcee : « in player order » : 3 sbires, 2 joueurs -> le premier joueur en recoit 2, le second 1",
       "foi 3 : trois Hydra Mercenary defausses, distribues un a un en commencant par le premier joueur",
       [NEUTRE, HEROS, "Puzzle.Counter('sk170a', 'faith', 2)", "Puzzle.CreateEncounterDeck('sk107','sk107','sk107','sk107','sk107','sk107','01101','01101','01101')"],
       ["Puzzle.RunVillainPhase()"], {"engages": [[0, 3], [1, 2]]}, main_exclusive=["01088"], heros2="hawkeye", passer_sur_option="Defense"),
    _c("sk170b Reponse forcee Sl'gur't : seules les TRAITRISES defaussees sont distribuees (Exhaustion distribuee, heros incline ; le sbire reste en defausse)",
       "foi 2 (1 + retournement) : Exhaustion (dessus) et Hydra Mercenary defausses ; la traitrise est distribuee et revelee, le sbire n'entre pas en jeu",
       [NEUTRE, VERS_SLGURT, HEROS, "Puzzle.CreateEncounterDeck('sk107','sk107','sk107','sk107','01101','01191')"], ["Puzzle.RunVillainPhase()"],
       {"hors_jeu": ["01101"], "defausse_rencontre": ["01101"], "exhausted": ["01001a"], "foi": 2}, main_exclusive=["01088"], passer_sur_option="Defense"),
]

CAS += SECTION_A + SECTION_B + SECTION_C

SECTION_D = [
    # ===================================================================== complot principal : stade 1 (deux sorties)
    _c("sk173b Derniere menace retiree : environnement DESTROYED en jeu, complot directement en 2B (sans 2A), mechant retourne",
       "Interruption forcee : `WhenLastThreatRemoveFromThisScheme` ; « Advance to stage 2B » saute le When Revealed de 2A (Strengthen the Faith reste dans le deck) ; 2B retourne le mechant",
       [NEUTRE, "Puzzle.CreateEncounterDeck('sk107', 'sk180')"], ["Puzzle.PlaceThreat('sk173b', -6)"],
       {"en_jeu": ["sk174b", "sk175b"], "hors_jeu": ["sk173b", "sk175a", "sk180", "sk174a"], "aside": [], "mechant_id": "sk170b", "foi": 2,
        "menace": [["sk174b", 0]]}),
    _c("sk173b Derniere menace retiree par un CONTRE reel (heros en forme heros, THW 1) : meme resultat",
       "le chemin des contres (`RemoveThreatInternal`) envoie aussi AfterCardRemovedToken",
       [NEUTRE, HEROS, "Puzzle.SetThreat('sk173b', 1)"], ["Puzzle.Thwart('01001a')"],
       {"en_jeu": ["sk174b", "sk175b"], "aside": [], "mechant_id": "sk170b"}),
    _c("sk173b TEMOIN : il reste de la menace -> rien ne se passe (environnement toujours de cote)",
       "ligne de base : 6 - 5 = 1",
       [NEUTRE], ["Puzzle.PlaceThreat('sk173b', -5)"],
       {"en_jeu": ["sk173b"], "hors_jeu": ["sk175a", "sk175b", "sk174b"], "aside": ["sk175a"], "mechant_id": "sk170a", "menace": [["sk173b", 1]]}),
    _c("sk173b When Completed : seuil atteint (9) -> environnement STRONGHOLD, stade 2A resolu (Strengthen the Faith revele +2 menace), puis 2B retourne le mechant",
       "« Advance to stage 2A » : chemin normal du moteur ; 2A fouille le deck et la defausse ; menace de Strengthen : 2[per_hero] + 2[per_hero] = 4 ; 2B : « Flip the villain »",
       [NEUTRE, "Puzzle.CreateEncounterDeck('sk107', 'sk180')"], ["Puzzle.PlaceThreat('sk173b', 3)"],
       {"en_jeu": ["sk174b", "sk175a", "sk180"], "hors_jeu": ["sk173b", "sk175b"], "aside": [], "menace": [["sk180", 4]], "mechant_id": "sk170b"}),
    _c("sk173b TEMOIN : 8 menaces ne suffisent pas (seuil 9[per_hero])",
       "6 + 2 = 8 < 9",
       [NEUTRE], ["Puzzle.PlaceThreat('sk173b', 2)"],
       {"en_jeu": ["sk173b"], "hors_jeu": ["sk175a", "sk175b"], "aside": ["sk175a"], "menace": [["sk173b", 8]]}),
    _c("sk174a Revelation : Strengthen the Faith est cherchee aussi dans la DEFAUSSE rencontre",
       "« Search the encounter deck and discard pile » ; copie dans la defausse",
       [NEUTRE, "Puzzle.CreateEncounterDiscardPile('sk180')"], ["Puzzle.PlaceThreat('sk173b', 3)"],
       {"en_jeu": ["sk180"], "menace": [["sk180", 4]]}),
    _c("sk174a Revelation, TEMOIN : aucune Strengthen the Faith nulle part -> rien n'est revele, le stade 2B s'installe quand meme",
       "la fouille ne trouve rien (pas d'erreur)",
       [NEUTRE], ["Puzzle.PlaceThreat('sk173b', 3)"], {"en_jeu": ["sk174b", "sk175a"], "hors_jeu": ["sk180"]}),
    _c("sk174a Revelation : deux joueurs -> menace de Strengthen = 2*2 + 2*2 = 8",
       "« 2[per_hero] additional threat » : par joueur, en plus de la menace de depart (2 par joueur)",
       [NEUTRE, "Puzzle.CreateEncounterDeck('sk107', 'sk180')"], ["Puzzle.PlaceThreat('sk173b', 6)"],
       {"en_jeu": ["sk180"], "menace": [["sk180", 8]]}, heros2="hawkeye"),
    _c("sk174b Revelation : le mechant sur la face Sl'gur't est retourne vers Kly'bn",
       "« Flip the villain » : le retournement est symetrique ; foi 1 + 1 (Sl'gur') + 1 (Kly'bn)",
       [NEUTRE, VERS_SLGURT], ["Puzzle.AdvanceMainScheme(1)"], {"en_jeu": ["sk174b"], "mechant_id": "sk170a", "foi": 3}),
    _c("sk174b 2B accompli : les joueurs perdent la partie",
       "texte en gras imprime (base automatique du moteur) ; seuil 12[per_hero], depart 0",
       [NEUTRE, "Puzzle.AdvanceMainScheme(1)"], ["Puzzle.PlaceThreat('sk174b', 12)"], {"defaite": True}),
    _c("sk174b TEMOIN : 11 menaces ne perdent pas la partie",
       "ligne de base",
       [NEUTRE, "Puzzle.AdvanceMainScheme(1)"], ["Puzzle.PlaceThreat('sk174b', 11)"], {"defaite": False, "menace": [["sk174b", 11]]}),
]

SECTION_E = [
    # ===================================================================== environnement Skrull Pantheon
    _c("sk175a Stronghold : Action de heros OFFERTE avec 2 ressources de meme type (Energy YY) ; retire 1 jeton de foi",
       "chemin reel : stade 1 accompli -> environnement face Stronghold ; foi 1 + 1 (2B retourne) = 2 -> 1",
       [NEUTRE, "Puzzle.PlaceThreat('sk173b', 3)", HEROS], ["Puzzle.Action('sk175a', 'HeroAction')"],
       {"foi": 1, "taille_main": 0, "en_jeu": ["sk175a"]}, main_exclusive=["01088"], payer_avec=["01088"], payer_tout=True),
    _c("sk175a Stronghold : deux ressources de types DIFFERENTS (1 mental + 1 energie) ne PAIENT PAS le cout : aucun jeton retire, main intacte",
       "« 2 resources of the SAME type » : la face Destroyed accepte, pas Stronghold ; (l'Action est quand meme proposee : le moteur ne teste la couleur qu'au paiement, comme 40090 / 55035)",
       [NEUTRE, "Puzzle.PlaceThreat('sk173b', 3)", HEROS], ["Puzzle.Action('sk175a', 'HeroAction')"], {"foi": 2, "taille_main": 2}, main_exclusive=["01005", "01012"], payer_avec=["01005", "01012"], payer_tout=True),
    _c("sk175a Stronghold, TEMOIN : meme main, la carte Energy (YY) rend l'Action offerte",
       "ligne de base",
       [NEUTRE, "Puzzle.PlaceThreat('sk173b', 3)", HEROS], [], {"action_offerte": [["sk175a", 1]]}, main_exclusive=["01088"]),
    _c("sk175b Destroyed : Action OFFERTE avec deux ressources de types DIFFERENTS ; retire 1 jeton de foi",
       "« 2 resources of ANY type » : mental (Swinging Web Kick) + energie (Crisis Interdiction) ; foi 2 -> 1",
       [NEUTRE, "Puzzle.PlaceThreat('sk173b', -6)", HEROS], ["Puzzle.Action('sk175b', 'HeroAction')"],
       {"foi": 1, "taille_main": 0, "en_jeu": ["sk175b"]}, main_exclusive=["01005", "01012"], payer_avec=["01005", "01012"], payer_tout=True),
    _c("sk175b Destroyed : Action NON offerte sans aucun jeton de foi",
       "garde « il reste de la foi » (sinon le cout serait paye pour rien)",
       [NEUTRE, "Puzzle.PlaceThreat('sk173b', -6)", HEROS, "Puzzle.Counter('sk170b', 'faith', -2)"], [], {"action_offerte": [["sk175b", 0]], "foi": 0}, main_exclusive=["01088"]),
    _c("sk175a Stronghold : Action NON offerte sans aucun jeton de foi",
       "meme garde cote Stronghold",
       [NEUTRE, "Puzzle.PlaceThreat('sk173b', 3)", HEROS, "Puzzle.Counter('sk170b', 'faith', -2)"], [], {"action_offerte": [["sk175a", 0]], "foi": 0}, main_exclusive=["01088"]),
    _c("sk175a Stade 1 : tant que le complot n'a pas avance, l'environnement reste hors jeu (les jetons ne peuvent pas etre retires)",
       "insert p.14 : « faith counters cannot be removed from the villain until the main scheme advances to the second stage »",
       [NEUTRE, HEROS], [], {"hors_jeu": ["sk175a", "sk175b"], "aside": ["sk175a"], "foi": 1}),
]

SBIRES_176 = ["Puzzle.PutIntoPlay('sk107')", "Puzzle.PutIntoPlay('01101')"]   # Scientist (MNG 3, ATQ 0) et Hydra Mercenary (MNG 0, ATQ 1)

SECTION_F = [
    # ===================================================================== sk176 / sk177 : Blessed by
    _c("sk176 Blessed by Kly'bn : s'attache au sbire de plus FAIBLE MNG (Hydra Mercenary 0, pas Skrull Scientist 3) et lui donne +X MNG (X = 1 jeton de foi)",
       "`AttachToFaceWhenPutIntoPlay(Minion, lowest_sch=True)` ; `GiveKeywordToAttached(scheme=1, get_new_value=foi)`",
       [NEUTRE] + SBIRES_176, ["Puzzle.Reveal('sk176')"],
       {"accroche_a": [["sk176", "01101"]], "attributs_carte": [["01101", "scheme", 1], ["sk107", "scheme", 0]]}),
    _c("sk176 Blessed by Kly'bn : le bonus SUIT les jetons de foi (1 -> 3 -> 2)",
       "X = nombre de jetons de foi SUR LE MECHANT : se recalcule a chaque pose / retrait",
       [NEUTRE] + SBIRES_176 + ["Puzzle.Reveal('sk176')", "Puzzle.Counter('sk170a', 'faith', 2)"], ["Puzzle.Counter('sk170a', 'faith', -1)"],
       {"accroche_a": [["sk176", "01101"]], "attributs_carte": [["01101", "scheme", 2]], "foi": 2}),
    _c("sk176 Blessed by Kly'bn : aucun sbire en jeu -> la carte gagne Renfort (revele la carte suivante)",
       "« If you cannot, this card gains surge » ; le sbire seme au dessus du deck est revele par le Renfort",
       [NEUTRE, "Puzzle.CreateEncounterDeck('sk107', '01101')"], ["Puzzle.Reveal('sk176')"],
       {"hors_jeu": ["sk176"], "en_jeu": ["01101"], "carte_du_surge": "01101"}),
    _c("sk176 Boost (manigance) : +2 icones de boost : la manigance du mechant place 2 + 1 + 2 = 5 menaces (deux joueurs)",
       "★ Boost : « If this activation is a SCHEME, this card gets +2 boost icons » ; menace de depart 12 (6 par joueur)",
       [NEUTRE], ["Puzzle.Boost('sk176')"], {"menace": [["sk173b", 17]]}, heros2="hawkeye"),
    _c("sk176 Boost, TEMOIN : pendant une ATTAQUE les 2 icones ne s'ajoutent pas (1 + 1 = 2 degats au heros)",
       "meme carte comme boost d'une attaque : ATQ 1 + 1 icone",
       [NEUTRE, HEROS], ["Puzzle.Boost('sk176')"], {"degats_identite": 2}, passer_sur_option="Defense"),
    _c("sk177 Blessed by Sl'gur't : s'attache au sbire de plus FAIBLE ATQ (Skrull Scientist 0, pas Hydra Mercenary 1) et lui donne +X ATQ",
       "`AttachToFaceWhenPutIntoPlay(Minion, lowest_atk=True)` ; `GiveKeywordToAttached(attack=1, get_new_value=foi)`",
       [NEUTRE] + SBIRES_176, ["Puzzle.Reveal('sk177')"],
       {"accroche_a": [["sk177", "sk107"]], "attributs_carte": [["sk107", "attack", 1], ["01101", "attack", 0]]}),
    _c("sk177 Blessed by Sl'gur't : le bonus SUIT les jetons de foi (1 -> 3)",
       "recalcul a chaque pose de jeton",
       [NEUTRE] + SBIRES_176 + ["Puzzle.Reveal('sk177')"], ["Puzzle.Counter('sk170a', 'faith', 2)"],
       {"accroche_a": [["sk177", "sk107"]], "attributs_carte": [["sk107", "attack", 3]]}),
    _c("sk177 Blessed by Sl'gur't : aucun sbire en jeu -> Renfort",
       "« If you cannot, this card gains surge »",
       [NEUTRE, "Puzzle.CreateEncounterDeck('sk107', '01101')"], ["Puzzle.Reveal('sk177')"],
       {"hors_jeu": ["sk177"], "en_jeu": ["01101"], "carte_du_surge": "01101"}),
    _c("sk177 Boost (attaque) : +2 icones : l'attaque du mechant inflige 1 + 1 + 2 = 4 degats",
       "★ Boost : « If this activation is an ATTACK, this card gets +2 boost icons »",
       [NEUTRE, HEROS], ["Puzzle.Boost('sk177')"], {"degats_identite": 4}, passer_sur_option="Defense"),
    _c("sk177 Boost, TEMOIN : pendant une MANIGANCE les 2 icones ne s'ajoutent pas (2 + 1 = 3 menaces, deux joueurs)",
       "meme carte comme boost d'une manigance",
       [NEUTRE], ["Puzzle.Boost('sk177')"], {"menace": [["sk173b", 15]]}, heros2="hawkeye"),
    # ===================================================================== sk178 Nogor
    _c("sk178 Nogor : +1 MNG, +1 ATQ et +1 PV par jeton de foi sur le mechant (1 jeton)",
       "`ThisGainKeyword(foi, scheme=1, attack=1, health=1)` ; imprime 1 / 1 / 4",
       [NEUTRE, "Puzzle.PutIntoPlay('sk178')"], [],
       {"attributs_carte": [["sk178", "scheme", 1], ["sk178", "attack", 1], ["sk178", "health", 1]]}),
    _c("sk178 Nogor : les bonus suivent les jetons (1 -> 4) et un Nogor blesse ne guerit pas",
       "3 jetons de plus : +4 partout ; 2 degats subis restent",
       [NEUTRE, "Puzzle.PutIntoPlay('sk178')", "Puzzle.Damage('sk178', 2)"], ["Puzzle.Counter('sk170a', 'faith', 3)"],
       {"attributs_carte": [["sk178", "scheme", 4], ["sk178", "attack", 4], ["sk178", "health", 4]], "degats": [["sk178", 2]]}),
    _c("sk178 Nogor revele : retourne le mechant (When Revealed)",
       "« Flip the villain »",
       [NEUTRE], ["Puzzle.Reveal('sk178')"], {"en_jeu": ["sk178"], "mechant_id": "sk170b", "foi": 2}),
    _c("sk178 Nogor en Boost : retourne le mechant (face visible d'arrivee = Sl'gur't)",
       "★ Boost : « Flip the villain » pendant l'attaque du mechant ; foi 1 + 1",
       [NEUTRE, HEROS], ["Puzzle.Boost('sk178')"], {"mechant_id": "sk170b", "foi": 2}, passer_sur_option="Defense"),
    # ===================================================================== sk179 Shapeless Wastes
    _c("sk179 Shapeless Wastes : Hinder 2[per_hero] + menace fixe 2 = 4 menaces (un joueur)",
       "Hinder natif (desc) : 2 par joueur, sur la carte elle-meme ; depart 2 fixe",
       [NEUTRE], ["Puzzle.Reveal('sk179')"], {"menace": [["sk179", 4]]}),
    _c("sk179 Shapeless Wastes : deux joueurs -> 2 + 2*2 = 6 menaces",
       "Hinder par joueur",
       [NEUTRE], ["Puzzle.Reveal('sk179')"], {"menace": [["sk179", 6]]}, heros2="hawkeye"),
    _c("sk179 Reponse forcee : un sbire SKRULL vaincu -> le mechant est retourne",
       "« if that character has the SKRULL trait, flip the villain » (Skrull Spy sk108)",
       [NEUTRE, "Puzzle.PutIntoPlay('sk179')", "Puzzle.PutIntoPlay('sk108')"], ["Puzzle.Damage('sk108', 9)"],
       {"mechant_id": "sk170b", "hors_jeu": ["sk108"], "foi": 2}),
    _c("sk179 Reponse forcee : un sbire NON-Skrull vaincu -> 1 jeton de foi (pas de retournement)",
       "« Otherwise, place 1 faith counter on the villain » (Hydra Mercenary)",
       [NEUTRE, "Puzzle.PutIntoPlay('sk179')", "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Damage('01101', 9)"],
       {"mechant_id": "sk170a", "foi": 2, "hors_jeu": ["01101"]}),
    _c("sk179 Reponse forcee : un ALLIE non-Skrull vaincu -> 1 jeton de foi",
       "« an ally OR a minion » : Black Cat (allie)",
       [NEUTRE, "Puzzle.PutIntoPlay('sk179')", "Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Damage('01002', 9)"],
       {"mechant_id": "sk170a", "foi": 2, "hors_jeu": ["01002"]}),
    _c("sk179 Reponse forcee, TEMOIN : sans la carte en jeu, un sbire vaincu ne pose aucun jeton",
       "ligne de base",
       [NEUTRE, "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Damage('01101', 9)"], {"foi": 1, "hors_jeu": ["01101"]}),
    # ===================================================================== sk180 Strengthen the Faith
    _c("sk180 Strengthen the Faith : menace 2[per_hero] a la revelation (un joueur : 2 ; deux joueurs : 4)",
       "StartingThreat 2*",
       [NEUTRE], ["Puzzle.Reveal('sk180')"], {"menace": [["sk180", 4]]}, heros2="hawkeye"),
    _c("sk180 Reponse forcee : un sbire SKRULL entre en jeu -> 1 jeton de foi",
       "« After a SKRULL minion enters play, place 1 faith counter on the villain » (Skrull Spy)",
       [NEUTRE, "Puzzle.PutIntoPlay('sk180')"], ["Puzzle.PutIntoPlay('sk108')"], {"foi": 2, "en_jeu": ["sk108"]}),
    _c("sk180 Reponse forcee, TEMOIN : un sbire NON-Skrull entre en jeu -> rien",
       "Hydra Mercenary : pas de trait SKRULL",
       [NEUTRE, "Puzzle.PutIntoPlay('sk180')"], ["Puzzle.PutIntoPlay('01101')"], {"foi": 1, "en_jeu": ["01101"]}),
    _c("sk180 Reponse forcee, TEMOIN : un ALLIE ne declenche pas (« SKRULL minion »)",
       "type sbire exige : Black Cat (allie, sans le trait de toute facon) -> rien",
       [NEUTRE, "Puzzle.PutIntoPlay('sk180')"], ["Puzzle.PutIntoPlay('01002', under_control=True)"], {"foi": 1}),
    _c("sk180 Boost : place 1 jeton de foi (pendant l'attaque du mechant)",
       "★ Boost",
       [NEUTRE, HEROS], ["Puzzle.Boost('sk180')"], {"foi": 2}, passer_sur_option="Defense"),
    # ===================================================================== sk181 / sk182 Prayer
    _c("sk181 Prayer to Kly'bn : Kly'bn en jeu -> il s'active contre le joueur (heros : ATQ 1 + 0 = 1 degat)",
       "« If Kly'bn is in play, he activates against you » ; deck de boost : Advance (aucune icone)",
       [NEUTRE, HEROS, "Puzzle.CreateEncounterDeck('01186')"], ["Puzzle.Reveal('sk181')"], {"mechant_id": "sk170a", "degats_identite": 1, "foi": 1}, passer_sur_option="Defense"),
    _c("sk181 Prayer to Kly'bn : Kly'bn PAS en jeu (face Sl'gur't visible) -> le mechant est retourne vers Kly'bn",
       "« Otherwise, flip the villain »",
       [NEUTRE, VERS_SLGURT], ["Puzzle.Reveal('sk181')"], {"mechant_id": "sk170a", "foi": 3}),
    _c("sk181 Boost : Kly'bn pas en jeu -> retourne le mechant (face visible Sl'gur't, attaque du mechant)",
       "★ Boost : « If Kly'bn is not in play, flip the villain »",
       [NEUTRE, HEROS, VERS_SLGURT], ["Puzzle.Boost('sk181')"], {"mechant_id": "sk170a", "foi": 3}, passer_sur_option="Defense"),
    _c("sk181 Boost, TEMOIN : Kly'bn EN jeu -> pas de retournement",
       "condition inversee",
       [NEUTRE, HEROS], ["Puzzle.Boost('sk181')"], {"mechant_id": "sk170a", "foi": 1}, passer_sur_option="Defense"),
    _c("sk182 Prayer to Sl'gur't : Sl'gur't en jeu -> elle s'active contre le joueur (heros : ATQ 2 = 2 degats)",
       "« If Sl'gur't is in play, she activates against you »",
       [NEUTRE, VERS_SLGURT, HEROS, "Puzzle.CreateEncounterDeck('01186')"], ["Puzzle.Reveal('sk182')"], {"mechant_id": "sk170b", "degats_identite": 2, "foi": 2}, passer_sur_option="Defense"),
    _c("sk182 Prayer to Sl'gur't : Sl'gur't PAS en jeu (face Kly'bn visible) -> le mechant est retourne vers Sl'gur't",
       "« Otherwise, flip the villain »",
       [NEUTRE], ["Puzzle.Reveal('sk182')"], {"mechant_id": "sk170b", "foi": 2}),
    _c("sk182 Boost : Sl'gur't pas en jeu -> retourne le mechant (face visible Kly'bn)",
       "★ Boost",
       [NEUTRE, HEROS], ["Puzzle.Boost('sk182')"], {"mechant_id": "sk170b", "foi": 2}, passer_sur_option="Defense"),
    _c("sk182 Boost, TEMOIN : Sl'gur't EN jeu -> pas de retournement",
       "condition inversee",
       [NEUTRE, HEROS, VERS_SLGURT], ["Puzzle.Boost('sk182')"], {"mechant_id": "sk170b", "foi": 2}, passer_sur_option="Defense"),
    # ===================================================================== sk183 Talisman
    _c("sk183 Talisman of the Skrulls : Nogor est cherche dans le DECK et revele (il retourne le mechant), pas de Renfort",
       "« Search the encounter deck and discard pile for Nogor and reveal him » ; carte de remplissage au-dessus : elle reste dans le deck",
       [NEUTRE, "Puzzle.CreateEncounterDeck('sk178', '01101')"], ["Puzzle.Reveal('sk183')"],
       {"en_jeu": ["sk178"], "mechant_id": "sk170b", "dans_deck_rencontre": ["01101"]}),
    _c("sk183 Talisman : Nogor est cherche aussi dans la DEFAUSSE rencontre",
       "« deck AND discard pile »",
       [NEUTRE, "Puzzle.CreateEncounterDeck('01101')", "Puzzle.CreateEncounterDiscardPile('sk178')"], ["Puzzle.Reveal('sk183')"],
       {"en_jeu": ["sk178"], "mechant_id": "sk170b"}),
    _c("sk183 Talisman : Nogor introuvable -> la carte gagne Renfort (le sbire au-dessus du deck est revele)",
       "« If Nogor did not enter play this way, this card gains surge »",
       [NEUTRE, "Puzzle.CreateEncounterDeck('01101')"], ["Puzzle.Reveal('sk183')"],
       {"en_jeu": ["01101"], "hors_jeu": ["sk178"], "carte_du_surge": "01101", "mechant_id": "sk170a"}),
    _c("sk183 Talisman : Nogor deja EN JEU -> il n'entre pas en jeu : Renfort",
       "un seul exemplaire : introuvable dans le deck",
       [NEUTRE, "Puzzle.PutIntoPlay('sk178')", "Puzzle.CreateEncounterDeck('01101')"], ["Puzzle.Reveal('sk183')"],
       {"en_jeu": ["sk178", "01101"], "carte_du_surge": "01101"}),
]

SECTION_G = [
    # ===================================================================== DARD'VAN SECT
    _c("sk184 Dard'van Fanatic : 1 degat a chaque personnage qu'on controle (choix 1)",
       "« Choose to either deal 1 damage to each character you control or place 1 threat on each scheme in play » ; Hawkeye en second joueur : seul le revelateur est touche",
       [NEUTRE, HEROS], ["Puzzle.Reveal('sk184')"],
       {"degats_identite": 1, "menace": [["sk173b", 6]]}, choisir_option="Deal_1_damage_to_each_character_you_control"),
    _c("sk184 Dard'van Fanatic : 1 menace sur chaque complot en jeu (choix 2), complot principal compris",
       "« each scheme in play » : complot principal et complots annexes (Shapeless Wastes en jeu)",
       [NEUTRE, "Puzzle.PutIntoPlay('sk179')"], ["Puzzle.Reveal('sk184')"],
       {"degats_identite": 0, "menace": [["sk173b", 7], ["sk179", 5]]}, choisir_option="Place_1_threat_on_each_scheme_in_play"),
    _c("sk184 Dard'van Fanatic : le choix des degats touche aussi les allies que le joueur controle",
       "« each character you control » : identite et Black Cat",
       [NEUTRE, HEROS, "Puzzle.PutIntoPlay('01002', under_control=True)"], ["Puzzle.Reveal('sk184')"],
       {"degats_identite": 1, "degats": [["01002", 1]]}, choisir_option="Deal_1_damage_to_each_character_you_control"),
    _c("sk185 Dard'van Priest : « When Revealed » : il comploter (menace sur le complot principal)",
       "le Priest (MNG 2) manigance contre le joueur revelateur : 6 + 2 = 8 menaces (pas de boost : deck vide, Priest 2 icones de boost seulement quand il est carte de boost)",
       [NEUTRE, "Puzzle.CreateEncounterDeck('01186')"], ["Puzzle.Reveal('sk185')"], {"menace_min": [["sk173b", 8]], "en_jeu": ["sk185"]}),
    _c("sk185 Dard'van Priest : Interruption forcee : il N'ATTAQUE PAS, il resout le When Revealed d'une carte en jeu (Fanatic : 1 degat au heros)",
       "« When Dard'van Priest would attack, instead choose a card in play with a When Revealed ability and resolve that ability » ; choix force : le Fanatic ; l'ATQ du Priest (0) n'inflige rien : les 1 degats viennent du Fanatic",
       [NEUTRE, HEROS, "Puzzle.PutIntoPlay('sk185')", "Puzzle.PutIntoPlay('sk184')"], ["Puzzle.Attack('sk185')"],
       {"degats_identite": 1}, cibles=["sk184"]),
    _c("sk185 Dard'van Priest : le choix peut viser le MECHANT : +1 jeton de foi",
       "« resolve that ability » : le When Revealed de Kly'bn pose un jeton",
       [NEUTRE, HEROS, "Puzzle.PutIntoPlay('sk185')"], ["Puzzle.Attack('sk185')"],
       {"foi": 2, "degats_identite": 0}, cibles=["sk170a"]),
    _c("sk185 Dard'van Priest, TEMOIN : sans l'Interruption, une attaque ordinaire n'a aucun effet de revelation (foi inchangee)",
       "ligne de base : les deux autres cas tombent au rouge sans le module",
       [NEUTRE, HEROS, "Puzzle.PutIntoPlay('sk185')"], [], {"foi": 1}),
    _c("sk186 Dard'van Sect : le mechant recoit 1 carte de boost face cachee ; menace 2[per_hero] ; icone Hazard",
       "« Give the villain 1 facedown boost card » ; Hazard natif",
       [NEUTRE, "Puzzle.CreateEncounterDeck('sk107', 'sk107')"], ["Puzzle.Reveal('sk186')"],
       {"boosts_mechant": 1, "menace": [["sk186", 2]], "icones": [["Hazard", 1]]}),
    _c("sk187 Collective Prayers : defausse 1 carte par personnage en jeu (identite + mechant = 2) et revele celles du set Dard'van Sect",
       "« Discard the top card of the encounter deck for each character in play. Reveal each card discarded this way that belongs to the Dard'van Sect encounter set » ; deux cartes : Dard'van Fanatic (set) et Hydra Mercenary (autre set)",
       [NEUTRE, "Puzzle.CreateEncounterDeck('sk107', '01101', 'sk184')"], ["Puzzle.Reveal('sk187')"],
       {"en_jeu": ["sk184"], "hors_jeu": ["01101"], "defausse_rencontre": ["01101"]}),
    _c("sk187 Collective Prayers : le nombre de cartes suit le nombre de personnages (identite + allie + mechant = 3)",
       "Black Cat en jeu : 3 cartes defaussees (deux Hydra Mercenary et le Fanatic en 3e position : revele)",
       [NEUTRE, "Puzzle.PutIntoPlay('01002', under_control=True)", "Puzzle.CreateEncounterDeck('sk107', 'sk184', '01101', '01101')"], ["Puzzle.Reveal('sk187')"],
       {"en_jeu": ["sk184"], "dans_deck_rencontre": ["sk107"]}),
    _c("sk188 Sectarian Practices : resout le When Revealed d'une carte en jeu (choix force : le mechant, +1 jeton de foi), pas de Renfort",
       "« Choose a card in play with a When Revealed ability and resolve that ability »",
       [NEUTRE, "Puzzle.CreateEncounterDeck('01101')"], ["Puzzle.Reveal('sk188')"], {"foi": 2, "hors_jeu": ["01101"]}, cibles=["sk170a"]),
    _c("sk188 Sectarian Practices : le When Revealed du complot 2B (« flip the villain ») peut etre choisi",
       "complot principal en 2B en jeu : choix force",
       [NEUTRE, "Puzzle.AdvanceMainScheme(1)", "Puzzle.CreateEncounterDeck('01101')"], ["Puzzle.Reveal('sk188')"], {"mechant_id": "sk170a", "hors_jeu": ["01101"]}, cibles=["sk174b"]),
]

CAS += SECTION_D + SECTION_E + SECTION_F + SECTION_G










SECTION_H = [
    # ===================================================================== Reponse forcee aux autres stades (memes modules, une face chacun)
    _c("sk171a Reponse forcee Kly'bn II (expert) : 1 jeton de foi = 1 carte du dessus defaussee et distribuee (sbire)",
       "meme texte aux trois stades ; expert : le stade II est en jeu des la mise en place",
       [NEUTRE, HEROS, "Puzzle.CreateEncounterDeck('sk107','sk107','sk107','sk107','01101')"], ["Puzzle.RunVillainPhase()"],
       {"en_jeu": ["01101"], "foi": 1, "mechant_id": "sk171a"}, scenario=SCE, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk171b Reponse forcee Sl'gur't II (expert) : seule la traitrise est distribuee (Exhaustion : heros incline), le sbire reste en defausse",
       "stade II face Sl'gur't (apres retournement) : foi 2",
       [NEUTRE, VERS_SLGURT, HEROS, "Puzzle.CreateEncounterDeck('sk107','sk107','sk107','sk107','01101','01191')"], ["Puzzle.RunVillainPhase()"],
       {"hors_jeu": ["01101"], "defausse_rencontre": ["01101"], "exhausted": ["01001a"], "foi": 2, "mechant_id": "sk171b"}, scenario=SCE, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk172a Reponse forcee Kly'bn III (expert) : le sbire defausse est distribue ; la carte d'etat Robuste est en place",
       "stade III face Kly'bn : foi 2 (1 + 1), Robuste donnee a la revelation",
       [NEUTRE, "Puzzle.AdvanceVillain()", HEROS, "Puzzle.CreateEncounterDeck('sk107','sk107','sk107','sk107','sk107','01101')"], ["Puzzle.RunVillainPhase()"],
       {"en_jeu": ["01101"], "foi": 2, "statuts_mechant": ["Tough"], "mechant_id": "sk172a"}, scenario=SCE, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk172b Reponse forcee Sl'gur't III (expert) : 3 jetons de foi = 3 cartes defaussees, seule la traitrise est distribuee",
       "stade III face Sl'gur't : foi 3 (1 + 1 + 1) ; Exhaustion (distribuee, heros incline), deux Hydra Mercenary restent en defausse",
       [NEUTRE, "Puzzle.AdvanceVillain()", VERS_SLGURT, HEROS, "Puzzle.CreateEncounterDeck('sk107','sk107','sk107','sk107','01101','01101','01191')"], ["Puzzle.RunVillainPhase()"],
       {"hors_jeu": ["01101"], "defausse_rencontre": ["01101"], "exhausted": ["01001a"], "foi": 3, "mechant_id": "sk172b"}, scenario=SCE, main_exclusive=["01088"], passer_sur_option="Defense"),
    _c("sk188 Sectarian Practices (autre scenario, Rhino) : aucune carte en jeu avec un When Revealed -> Renfort (la carte suivante est revelee)",
       "« If you cannot, this card gains surge » ; set Dard'van Sect utilisable hors Skrull Pantheon (insert p.14)",
       [NEUTRE, "Puzzle.CreateEncounterDeck('sk107', '01101')"], ["Puzzle.Reveal('sk188')"],
       {"en_jeu": ["01101"], "carte_du_surge": "01101"}, scenario="rhino", verifier="etat_attendu"),
]
CAS += SECTION_H

# ##FIN_DES_CAS##

VERIFICATIONS = r'''
def pantheon_dump(monde, aides):
    """SONDE de mise au point (jamais dans la batterie finale) : decrit l'etat."""
    from game.operate.worlds import Worlds
    lignes = []
    for objet in monde.object_manager.card_dict.values():
        f = objet.face
        if f is not None and f.IsInPlay() and not getattr(f.paper, "card_id", "").startswith("sk"):
            lignes.append(f"[{f.paper.card_id} {f.name}]")
        if f is not None and f.IsInPlay() and getattr(f.paper, "card_id", "").startswith("sk"):
            extra = ""
            if f.paper.card_id.startswith(("sk170", "sk171", "sk172")):
                st = [x.name for x in f.card.components.status.GetDeck().Get()]
                bo = [x.paper.card_id for x in f.card.components.boostable.GetDeck().Get()]
                at = [x.paper.card_id for x in f.GetAttachedAttachments()]
                extra = f" degats={f.max_health - f.health} statuts={st} boosts={bo} attaches={at}"
            lignes.append(f"{f.paper.card_id}[{f.name}] foi={f.GetCounters('faith')} menace={getattr(f, 'threat', None)}{extra}")
    from game.ability.ability import AbilityType
    cand = []
    for objet in monde.object_manager.card_dict.values():
        f = objet.face
        if f is not None and f.IsInPlay() and f.effect.Find(type=AbilityType.WhenRevealed):
            cand.append(f"{f.paper.card_id}:{len(f.effect.Find(type=AbilityType.WhenRevealed))}")
    lignes.append("avec_WhenRevealed=" + str(cand))
    lignes.append("aside=" + str([getattr(f.paper, "card_id", "?") for f in monde.aside_deck.Get(True)]))
    lignes.append("deck_rencontre=" + str([getattr(f.paper, "card_id", "?") for f in Worlds.GetEncounterDeckCards(monde)]))
    lignes.append("defausse_rencontre=" + str([getattr(f.paper, "card_id", "?") for f in Worlds.GetEncounterDiscardPileCards(monde)]))
    return False, " | ".join(lignes)


def _pantheon_mechant(monde):
    from game.operate.worlds import Worlds
    vilains = Worlds.GetAllVillains(monde)
    return vilains[0] if vilains else None


def pantheon_etat(monde, aides):
    """etat_attendu (cles communes) + les cles propres au scenario :
    dump, mechant_id, foi, statuts_mechant, boosts_mechant, attaches_mechant, victoire, defaite,
    aside [ids], taille_deck_rencontre, nb_en_jeu [[card_id, n]], action_offerte [[card_id, n]]."""
    attendu = aides["cas"].get("attendu") or {}
    if attendu.get("dump"):
        return pantheon_dump(monde, aides)
    propres = {"mechant_id", "foi", "statuts_mechant", "boosts_mechant", "attaches_mechant", "victoire", "defaite",
               "aside", "taille_deck_rencontre", "nb_en_jeu", "action_offerte", "engages"}
    inconnues = sorted(set(attendu) - set(CLES_ETAT_ATTENDU) - propres)
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de pantheon_etat : {inconnues}"
    from game.operate.worlds import Worlds
    ok, message = etat_attendu(monde, aides)
    soucis = [] if ok else [message]
    v = _pantheon_mechant(monde)
    if v is None and not (attendu.get("victoire") or attendu.get("defaite")):
        return False, "aucun mechant en jeu"
    if "mechant_id" in attendu and (v is None or v.paper.card_id != attendu["mechant_id"]):
        soucis.append(f"mechant = {None if v is None else v.paper.card_id} (attendu {attendu['mechant_id']})")
    if "foi" in attendu and v is not None and v.GetCounters("faith") != attendu["foi"]:
        soucis.append(f"jetons de foi = {v.GetCounters('faith')} (attendu {attendu['foi']})")
    if "statuts_mechant" in attendu and v is not None:
        noms = sorted(x.name for x in v.card.components.status.GetDeck().Get())
        if noms != sorted(attendu["statuts_mechant"]):
            soucis.append(f"statuts du mechant = {noms} (attendu {sorted(attendu['statuts_mechant'])})")
    if "boosts_mechant" in attendu and v is not None:
        n = v.card.components.boostable.GetDeck().GetSize()
        if n != attendu["boosts_mechant"]:
            soucis.append(f"cartes de boost du mechant = {n} (attendu {attendu['boosts_mechant']})")
    if "attaches_mechant" in attendu and v is not None:
        ids = sorted(a.paper.card_id for a in v.GetAttachedAttachments())
        if ids != sorted(attendu["attaches_mechant"]):
            soucis.append(f"attachements du mechant = {ids} (attendu {sorted(attendu['attaches_mechant'])})")
    if "victoire" in attendu:
        gagne = bool(monde.is_game_over) and bool(monde.game_over.players_won)
        if gagne != attendu["victoire"]:
            soucis.append(f"victoire = {gagne} (attendu {attendu['victoire']})")
    if "defaite" in attendu:
        perdu = bool(monde.is_game_over) and not monde.game_over.players_won
        if perdu != attendu["defaite"]:
            soucis.append(f"defaite = {perdu} (attendu {attendu['defaite']})")
    if "aside" in attendu:
        ids = sorted(getattr(f.paper, "card_id", "?") for f in monde.aside_deck.Get(True))
        if ids != sorted(attendu["aside"]):
            soucis.append(f"zone mise de cote = {ids} (attendu {sorted(attendu['aside'])})")
    if "taille_deck_rencontre" in attendu:
        n = len(Worlds.GetEncounterDeckCards(monde))
        if n != attendu["taille_deck_rencontre"]:
            soucis.append(f"taille du deck rencontre = {n} (attendu {attendu['taille_deck_rencontre']})")
    for indice, n in attendu.get("engages") or []:
        reel = monde.const_players[indice].engaged_minions.GetSize()
        if reel != n:
            soucis.append(f"sbires engages avec le joueur {indice} = {reel} (attendu {n})")
    for card_id, n in attendu.get("nb_en_jeu") or []:
        compte = sum(1 for o in monde.object_manager.card_dict.values()
                     if o.face is not None and o.face.IsInPlay() and getattr(o.face.paper, "card_id", None) == card_id)
        if compte != n:
            soucis.append(f"{card_id} en jeu x{compte} (attendu {n})")
    for card_id, n in attendu.get("action_offerte") or []:
        from game.ability.ability import AbilityType
        from game.event.manager import EventManager
        from game.message import Message
        from game.effect.rule import GameRule
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (action_offerte)")
            continue
        joueur = monde.GetCurrentPlayer()
        candidats = [x for x in face.effect.Find(when=Message.WhenPlayerInTurn, type=AbilityType.HeroAction)
                     if not x.ability.is_play]
        msg = Message.WhenPlayerLikeInTurn(joueur, GameRule(joueur.GetIdentity()))
        msg.Send()
        offertes = EventManager.FilterAvailableEffects(msg, candidats, joueur, monde, None)
        if len(offertes) != n:
            soucis.append(f"{card_id} offre {len(offertes)} Action(s) de heros (attendu {n})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat Pantheon conforme"
'''
