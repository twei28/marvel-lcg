# Cas test_capacites du heros RAPHAEL (TMNT Heroes v3, Inkwire, prefixe `tr`).
# Format identique a tools/test_capacites.py ; noms prefixes `[raphael]` (filtre : `[raphael]`),
# un `card_id` sujet dans chaque nom (substituer_pack.py filtre dessus).
#
# Decisions de l'utilisateur appliquees (.planning/tmnt/decisions-phase-b.md) :
#  - « Raphael » en forme CIVILE : les effets visent l'IDENTITE (soin, degats, rage) ;
#  - rage plafonnee a 3 SEULEMENT la ou c'est imprime (Yaban Hito, Seething Rage, Sai) ;
#  - encart des Sai : chaque usage = action d'attaque + 1 rage (max 3) ;
#  - Out of Control : « vous » = l'identite seulement ; Disarm : attachements de RENCONTRE seulement.
#
# Conventions :
#  - le heros demarre en ALTER EGO (tr001b, Raph) ; HEROS le met en forme heros (tr001a, Raphael) ;
#  - `main_exclusive` vide la main : chaque cas sait avec QUOI il paie
#    (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR, tr007 Seething Rage = R) ;
#  - Rhino 01094 est le vilain, 01101 Hydra Mercenary (3 PV) le sbire de mesure.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('tr001b', 'tr001a')"
CIVIL = "Puzzle.ChangeToFace('tr001a', 'tr001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
# Deck rencontre vide par defaut : les attaques de Rhino n'ont alors AUCUN boost (mesure du degat exact).
# (« I'm Tough » 01105 : aucune icone ni effet de boost ; un deck VIDE ferait avorter l'attaque de Rhino, 0 degat.)
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[raphael] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "raphael"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ===================================================================== tr001a Raphael (face heros)
    _c("tr001a Raphael : un compteur de rage se depense comme une ressource [physical] (paye Shell Cycle, cout 1)",
       "« Each rage counter on Raphael can be spent as if it were a [physical] resource » : main vide sauf la carte jouee, "
       "1 compteur de rage = SEULE source de paiement ; le compteur doit tomber de 1 a 0",
       [HEROS, "Puzzle.Counter('tr001a', 'rage', 1)"], [],
       {"en_jeu": ["tr008"], "compteurs_identite": [["rage", 0]]},
       main_exclusive=["tr008"], jouer=["tr008"]),
    _c("tr001a Raphael : 2 compteurs de rage paient le Requirement [physical][physical] de Headbutt",
       "la rage est une ressource PHYSIQUE : une carte a Requirement RR est jouable avec 2 rage seulement en main",
       [HEROS, "Puzzle.Counter('tr001a', 'rage', 2)"], [],
       {"defausse": ["tr004"], "compteurs_identite": [["rage", 0]], "degats": [["01094", 4]]},
       main_exclusive=["tr004"], jouer=["tr004"], cibles=["01094"]),
    _c("tr001a Yaban Hito : une attaque qui blesse Raphael pose 1 rage (Rhino ATK 2 -> 2 degats, 1 rage)",
       "« After Raphael takes any amount of damage from an attack, place 1 rage counter on him (max 3) » ; `is_from_attack=True`",
       [HEROS], ["Puzzle.Attack('01094')"],
       {"degats_identite": 2, "compteurs_identite": [["rage", 1]]}, main_exclusive=["01090"]),
    _c("tr001a Yaban Hito : plafond de 3 (4 attaques de Rhino : 8 degats, rage 3 et non 4)",
       "TEMOIN D'EPUISEMENT du plafond imprime « to a maximum of 3 » : on mesure un CHIFFRE au 4e declenchement",
       [HEROS], ["Puzzle.Attack('01094')", "Puzzle.Attack('01094')", "Puzzle.Attack('01094')", "Puzzle.Attack('01094')"],
       {"degats_identite": 8, "compteurs_identite": [["rage", 3]]}, main_exclusive=["01090"]),
    _c("tr001a Yaban Hito : des degats qui ne viennent PAS d'une attaque ne posent rien (Puzzle.Damage 2)",
       "contre-cas « from an attack » : les degats de Casey, des Sai, du poison... ne declenchent pas Yaban Hito",
       [HEROS], ["Puzzle.Damage('tr001a', 2)"],
       {"degats_identite": 2, "compteurs_identite": [["rage", 0]]}, main_exclusive=["01090"]),
    _c("tr001a Yaban Hito : 0 degat (statut Tough) = pas de rage",
       "« takes ANY AMOUNT of damage » : `AfterUnitTookDamage` ne part qu'apres des degats effectifs",
       [HEROS, "Puzzle.Tough('tr001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 0, "compteurs_identite": [["rage", 0]]}, main_exclusive=["01090"]),
    _c("tr001a Yaban Hito : absente en ALTER-EGO (Raph attaque par Rhino : aucune rage)",
       "contre-cas dans l'AUTRE forme : la Reponse est imprimee sur la face heros seulement",
       [], ["Puzzle.Attack('01094')"],
       {"degats_identite": 2, "compteurs_identite": [["rage", 0]]}, main_exclusive=["01090"]),
    # ===================================================================== tr001b Raph (face alter-ego)
    _c("tr001b Raph : defausse 1 carte (cout) puis met en jeu 2 Sai du DECK, inclinees",
       "« Action: Discard 1 card from your hand -> search your deck and discard pile for up to 2 [[SAI]] upgrades and put them "
       "into play, exhausted » ; `up to 2` : le pilote prend le minimum, donc `cibles` force les deux",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('tr011', 'tr012', '01090', '01090')"], ["Puzzle.Action('tr001b', 'Action')"],
       {"en_jeu": ["tr011", "tr012"], "exhausted": ["tr011", "tr012"], "defausse": ["01089"],
        "taille_deck_joueur": 2},
       main_exclusive=["01089"], cibles=["tr011", "tr012"]),
    _c("tr001b Raph : une seule Sai trouvable (l'autre n'existe nulle part) -> une seule en jeu",
       "« up to 2 » : avec une seule Sai dans le deck, la recherche en ramene une",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('tr011', '01090', '01090')"], ["Puzzle.Action('tr001b', 'Action')"],
       {"en_jeu": ["tr011"], "hors_jeu": ["tr012"], "exhausted": ["tr011"], "defausse": ["01089"]},
       main_exclusive=["01089"], cibles=["tr011"]),
    _c("tr001b Raph : la recherche couvre aussi la DEFAUSSE (Sai dans la defausse, pas dans le deck)",
       "« search your deck AND DISCARD PILE »",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090')", "Puzzle.CreatePlayerDiscardPile('tr012')"],
       ["Puzzle.Action('tr001b', 'Action')"],
       {"en_jeu": ["tr012"], "exhausted": ["tr012"], "defausse": ["01089"]},
       main_exclusive=["01089"], cibles=["tr012"]),
    _c("tr001b Raph : l'Action est ABSENTE en forme heros (aucune Sai mise en jeu)",
       "contre-cas dans l'autre forme : `Action` (pas `Hero Action`) est imprimee sur la face alter-ego",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('tr011', '01090')"], [],
       {"hors_jeu": ["tr011"], "taille_deck_joueur": 2},
       main_exclusive=["01089"], declencher_tolerant=["Puzzle.Action('tr001b', 'Action')"]),
    # ===================================================================== tr002 Casey Jones
    _c("tr002 Casey Jones (forme HEROS) : 1 degat a Raphael ET a chaque sbire engage avec soi, +1 rage",
       "« After Casey Jones enters play, deal 1 damage to Raphael and each minion engaged with you. Place 1 rage counter on Raphael »",
       [HEROS, "Puzzle.PutIntoPlay('01101')"], [],
       {"en_jeu": ["tr002"], "degats_identite": 1, "degats": [["01101", 1]], "compteurs_identite": [["rage", 1]]},
       main_exclusive=["tr002", "01088", "01089"], jouer=["tr002"]),
    _c("tr002 Casey Jones (forme CIVILE) : l'IDENTITE (Raph) prend 1 degat, le sbire aussi, et la rage se pose sur l'identite",
       "decision du 15/10/2026 : « Raphael » = l'identite, meme en alter-ego (le code d'origine ne faisait rien en civil)",
       ["Puzzle.PutIntoPlay('01101')"], [],
       {"en_jeu": ["tr002"], "forme": "AlterEgo", "degats_identite": 1, "degats": [["01101", 1]],
        "compteurs_identite": [["rage", 1]]},
       main_exclusive=["tr002", "01088", "01089"], jouer=["tr002"]),
    _c("tr002 Casey Jones : la rage de Casey n'a AUCUN plafond (3 rage -> 4)",
       "decision du 15/10/2026 : `PLAFOND_PARTOUT = False`, aucun « to a maximum of 3 » imprime sur Casey Jones",
       [HEROS, "Puzzle.Counter('tr001a', 'rage', 3)"], [],
       {"en_jeu": ["tr002"], "compteurs_identite": [["rage", 4]], "degats_identite": 1},
       main_exclusive=["tr002", "01088", "01089"], jouer=["tr002"], ne_pas_depenser=["tr001a"]),
    _c("tr002 Casey Jones : ses degats ne sont PAS une attaque (pas de Yaban Hito) : exactement 1 rage, pas 2",
       "les 1 degats de Casey sur Raphael n'ont pas `is_from_attack` : 1 rage de Casey, 0 de Yaban Hito",
       [HEROS], [],
       {"compteurs_identite": [["rage", 1]], "degats_identite": 1},
       main_exclusive=["tr002", "01088", "01089"], jouer=["tr002"]),
    _c("tr002 Casey Jones : un sbire engage avec un AUTRE joueur ne prend rien (2 joueurs)",
       "« each minion engaged WITH YOU » : piege `each` / `with you`, mesure en partie a deux joueurs",
       [HEROS, "Puzzle.PutIntoPlay('01101')", "Puzzle.Engage('01101', 1)"], [],
       {"en_jeu": ["tr002"], "degats": [["01101", 0]], "degats_identite": 1},
       heros2="spider_man", main_exclusive=["tr002", "01088", "01089"], jouer=["tr002"]),
    _c("tr002 Casey Jones : ATQ 2* = 1 degat consecutif (Casey attaque Rhino : Rhino -2, Casey -1)",
       "l'etoile creuse sous la valeur d'ATQ = degat consecutif imprime ; PV 2 : Casey survit avec 1 degat",
       [HEROS, "Puzzle.PutIntoPlay('tr002', under_control=True)"], ["Puzzle.Attack('tr002')"],
       {"degats": [["01094", 2], ["tr002", 1]]}, cibles=["01094"]),
    # ===================================================================== tr003 Disarm
    _c("tr003 Disarm : Requirement [physical] : REFUSEE avec Energy (YY) seule, la carte reste en main, menace inchangee",
       "mot-cle Requirement (base automatique `desc.Requirement = R`, fiche requirement.md) : cout 2 dont au moins 1 physique ; "
       "temoin positif = le cas suivant (meme position avec Strength RR)",
       [HEROS, "Puzzle.SetThreat('01097b', 6)"], [],
       {"en_main": ["tr003"], "menace": [["01097b", 6]]}, main_exclusive=["tr003", "01088"], jouer=["tr003"], cibles=["01097b"]),
    _c("tr003 Disarm : retire 4 menaces d'un complot (6 -> 2), aucune Sai : rien d'autre ne part",
       "« Remove 4 threat from a scheme » ; sans Sai, l'option « defausser une Sai » n'est pas offerte : l'attachement d'un ennemi reste",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.PutIntoPlay('01100')"], [],
       {"menace": [["01097b", 2]], "defausse": ["tr003"], "en_jeu": ["01100"]},
       main_exclusive=["tr003", "01090"], jouer=["tr003"], cibles=["01097b"]),
    _c("tr003 Disarm : ACCEPTER = la Sai ET l'attachement a « Hero Action » d'un ennemi sont defausses",
       "« You may discard a [[SAI]] upgrade you control to discard an attachment with the text Hero Action or Hero Response from an enemy » ; "
       "01100 Enhanced Ivory Horn (attachement de RENCONTRE, Hero Action) attache a Rhino",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.PutIntoPlay('01100')", "Puzzle.PutIntoPlay('tr011', under_control=True)"], [],
       {"menace": [["01097b", 2]], "hors_jeu": ["tr011", "01100"], "defausse": ["tr003"]},
       main_exclusive=["tr003", "01090"], jouer=["tr003"], cibles=["01097b", "tr011"]),
    _c("tr003 Disarm : REFUSER = rien n'est defausse (les 4 menaces partent quand meme)",
       "le « may » se refuse : ni la Sai ni l'attachement ne bougent",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.PutIntoPlay('01100')", "Puzzle.PutIntoPlay('tr011', under_control=True)"], [],
       {"menace": [["01097b", 2]], "en_jeu": ["tr011", "01100"], "defausse": ["tr003"]},
       main_exclusive=["tr003", "01090"], jouer=["tr003"], cibles=["01097b"], choisir_option=["Cancel"]),
    _c("tr003 Disarm : une AMELIORATION joueur posee sur un ennemi n'est PAS un « attachment » (Gekido sur Rhino reste, la Sai aussi)",
       "decision du 15/10/2026 : attachements de RENCONTRE seulement (type Attachment). Gekido porte le texte « Hero Action » mais est une Upgrade",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.PutIntoPlay('tr010')", "Puzzle.Attach('tr010', '01094')",
        "Puzzle.PutIntoPlay('tr011', under_control=True)"], [],
       {"menace": [["01097b", 2]], "en_jeu": ["tr011", "tr010"], "defausse": ["tr003"]},
       main_exclusive=["tr003", "01090"], jouer=["tr003"], cibles=["01097b", "tr011"]),
    _c("tr003 Disarm : un attachement SANS « Hero Action/Response » n'est pas eligible (Armored Rhino Suit reste)",
       "le filtre lit le TEXTE imprime : 01098 n'en porte pas",
       [HEROS, "Puzzle.SetThreat('01097b', 6)", "Puzzle.PutIntoPlay('01098')", "Puzzle.PutIntoPlay('tr011', under_control=True)"], [],
       {"menace": [["01097b", 2]], "en_jeu": ["tr011", "01098"], "defausse": ["tr003"]},
       main_exclusive=["tr003", "01090"], jouer=["tr003"], cibles=["01097b", "tr011"]),
    # ===================================================================== tr004 Headbutt
    _c("tr004 Headbutt : Requirement [physical][physical] : REFUSEE avec 1 seule [physical] (Seething Rage R + Energy YY)",
       "Requirement RR sur une carte a cout 2 : 3 ressources dont une SEULE physique ne suffisent pas ; temoin positif = les cas suivants (Strength RR)",
       [HEROS], [],
       {"en_main": ["tr004"], "degats": [["01094", 0]]}, main_exclusive=["tr004", "tr007", "01088"], jouer=["tr004"], cibles=["01094"]),
    _c("tr004 Headbutt : 4 degats a l'ennemi et il est ETOURDI (1re branche)",
       "« Deal 4 damage to an enemy. Stun or confuse that enemy » : le pilote prend la 1re branche (stun)",
       [HEROS], [],
       {"degats": [["01094", 4]], "statuts": [["01094", "Stunned"]], "statuts_absents": [["01094", "Confused"]], "defausse": ["tr004"]},
       main_exclusive=["tr004", "01090"], jouer=["tr004"], cibles=["01094"]),
    _c("tr004 Headbutt : 4 degats et il est DESORIENTE (2e branche, `preferer_option`)",
       "l'autre branche du « stun or confuse » : Confused et non Stunned",
       [HEROS], [],
       {"degats": [["01094", 4]], "statuts": [["01094", "Confused"]], "statuts_absents": [["01094", "Stunned"]], "defausse": ["tr004"]},
       main_exclusive=["tr004", "01090"], jouer=["tr004"], cibles=["01094"], preferer_option=["confuse"]),
    _c("tr004 Headbutt : l'ennemi vaincu par les 4 degats (sbire 3 PV) : aucun statut, aucun plantage",
       "« that enemy » est hors jeu : les options sont sans effet, la carte finit en defausse",
       [HEROS, "Puzzle.PutIntoPlay('01101')"], [],
       {"hors_jeu": ["01101"], "defausse": ["tr004"], "aucune_en_resolution": True},
       main_exclusive=["tr004", "01090"], jouer=["tr004"], cibles=["01101"]),
    # ===================================================================== tr005 Savage Assault
    _c("tr005 Savage Assault : Requirement [physical][physical][physical] : REFUSEE avec 2 [physical] + 2 [energy]",
       "Requirement RRR sur une carte a cout 4 : 4 ressources dont 2 physiques seulement ne suffisent pas ; temoin positif = les cas suivants "
       "(Strength + 2 Seething Rage = 4 [physical])",
       [HEROS], [],
       {"en_main": ["tr005"], "degats": [["01094", 0]]}, main_exclusive=["tr005", "01090", "01088"], jouer=["tr005"], cibles=["01094"]),
    _c("tr005 Savage Assault : 10 degats TOUS sur un seul ennemi (Rhino)",
       "« 10 damage divided among enemies as you choose » : 10 selections sur la meme cible (`repeat_rules=Health`)",
       [HEROS], [],
       {"degats": [["01094", 10]], "defausse": ["tr005"]},
       main_exclusive=["tr005", "01090", "tr007", "tr007"], jouer=["tr005"], cibles=["01094"] * 10),
    _c("tr005 Savage Assault : 10 degats REPARTIS (7 sur Rhino + 3 sur le sbire, qui meurt) : total mesure a 10, pas 10 chacun",
       "piege `each` : le total est 10, pas 10 par ennemi",
       [HEROS, "Puzzle.PutIntoPlay('01101')"], [],
       {"degats": [["01094", 7]], "hors_jeu": ["01101"], "defausse": ["tr005"]},
       main_exclusive=["tr005", "01090", "tr007", "tr007"], jouer=["tr005"], cibles=["01094"] * 7 + ["01101"] * 3),
    # ===================================================================== tr006 Unbridled Fury
    _c("tr006 Unbridled Fury : +2 ATQ a Raphael ET pioche 1 si payee avec une ressource [physical] (Strength)",
       "« +2 ATK until the end of the round. If you paid using a [physical] resource, draw 1 card » : ATQ 3 -> 5, main : 0 + 1 pioche",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090')"], [],
       {"attributs": {"attack": 2}, "taille_main": 1, "defausse": ["tr006"]},
       main_exclusive=["tr006", "01090"], jouer=["tr006"], payer_avec=["01090"]),
    _c("tr006 Unbridled Fury : payee en [energy] : +2 ATQ mais PAS de pioche",
       "contre-cas du « if you paid using a [physical] resource »",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090')"], [],
       {"attributs": {"attack": 2}, "taille_main": 0, "defausse": ["tr006"]},
       main_exclusive=["tr006", "01088"], jouer=["tr006"], payer_avec=["01088"]),
    _c("tr006 Unbridled Fury : payee avec un COMPTEUR DE RAGE (ressource [physical]) : pioche 1",
       "la rage depensee « comme une ressource [physical] » compte comme une ressource physique payee",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090')", "Puzzle.Counter('tr001a', 'rage', 1)"], [],
       {"attributs": {"attack": 2}, "taille_main": 1, "compteurs_identite": [["rage", 0]]},
       main_exclusive=["tr006"], jouer=["tr006"]),
    _c("tr006 Unbridled Fury : Max 1 per phase : TEMOIN D'EPUISEMENT, le 2e exemplaire n'est plus jouable et l'ATQ reste a +2",
       "limite imprimee « Max 1 per phase » : apres une 1re Fury, la 2nde (autre exemplaire) est refusee ; ATQ +2 (et non +4)",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090')"], [],
       {"attributs": {"attack": 2}, "jouable": [["tr006", False]]},
       main_exclusive=["tr006", "tr006", "01090", "01090"], jouer=["tr006"], verifier="raphael_etat"),
    _c("tr006 Unbridled Fury : a la FIN DU ROUND l'ATQ redevient 3 (dure jusqu'a la fin du round, pas plus)",
       "« until the end of the round » : `GainUntilRoundEnd`, mesure avant et apres la fin de round",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090')"], [],
       {"attributs": {"attack": 0}, "fin_de_round": True},
       main_exclusive=["tr006", "01090"], jouer=["tr006"], verifier="raphael_etat"),
    # ===================================================================== tr007 Seething Rage
    _c("tr007 Seething Rage (forme HEROS) : depensee, soigne 2 a Raphael et pose 1 rage",
       "« After you spend this card, heal 2 damage from Raphael and place 1 rage counter on him (max 3) » ; Shell Cycle (cout 1) payee par tr007",
       [HEROS, "Puzzle.Damage('tr001a', 3)"], [],
       {"degats_identite": 1, "compteurs_identite": [["rage", 1]], "en_jeu": ["tr008"]},
       main_exclusive=["tr008", "tr007"], jouer=["tr008"], payer_avec=["tr007"]),
    _c("tr007 Seething Rage (forme CIVILE) : l'IDENTITE (Raph) est soignee de 2 et recoit la rage",
       "decision du 15/10/2026 : « Raphael » = l'identite, meme en alter-ego (le code d'origine ne faisait rien en civil)",
       ["Puzzle.Damage('tr001b', 3)"], [],
       {"forme": "AlterEgo", "degats_identite": 1, "compteurs_identite": [["rage", 1]], "en_jeu": ["tr008"]},
       main_exclusive=["tr008", "tr007"], jouer=["tr008"], payer_avec=["tr007"]),
    _c("tr007 Seething Rage : plafond de 3 imprime (rage 3 -> reste 3), soin 2 quand meme",
       "TEMOIN D'EPUISEMENT du « to a maximum of 3 » : chiffre mesure, la rage ne passe pas a 4",
       [HEROS, "Puzzle.Damage('tr001a', 3)", "Puzzle.Counter('tr001a', 'rage', 3)"], [],
       {"degats_identite": 1, "compteurs_identite": [["rage", 3]]},
       main_exclusive=["tr008", "tr007"], jouer=["tr008"], payer_avec=["tr007"], ne_pas_depenser=["tr001a"]),
    _c("tr007 Seething Rage : sans degat a soigner, la rage est posee quand meme (0 degat, rage 1)",
       "le soin de 2 sur une identite intacte ne bloque pas la rage",
       [HEROS], [],
       {"degats_identite": 0, "compteurs_identite": [["rage", 1]]},
       main_exclusive=["tr008", "tr007"], jouer=["tr008"], payer_avec=["tr007"]),
    # ===================================================================== tr008 Shell Cycle
    _c("tr008 Shell Cycle : incline + 2 ressources payees en [physical][physical] -> redresse le heros ET +1 THW",
       "« Exhaust Shell Cycle and spend 2 resources of any type -> ready your hero. If you paid using [physical][physical], +1 THW until the end of the round » ; "
       "Strength = RR",
       [HEROS, "Puzzle.PutIntoPlay('tr008', under_control=True)", "Puzzle.Exhaust('tr001a')"],
       ["Puzzle.Action('tr008', 'HeroAction')"],
       {"pret": ["tr001a"], "exhausted": ["tr008"], "attributs": {"thwart": 1}},
       main_exclusive=["01090"], payer_avec=["01090"], ne_pas_depenser=["tr001a"]),
    _c("tr008 Shell Cycle : payee en [energy][energy] -> le heros se redresse mais PAS de +1 THW",
       "contre-cas de la couleur payee",
       [HEROS, "Puzzle.PutIntoPlay('tr008', under_control=True)", "Puzzle.Exhaust('tr001a')"],
       ["Puzzle.Action('tr008', 'HeroAction')"],
       {"pret": ["tr001a"], "exhausted": ["tr008"], "attributs": {"thwart": 0}},
       main_exclusive=["01088"], payer_avec=["01088"], ne_pas_depenser=["tr001a"]),
    _c("tr008 Shell Cycle : 1 seule [physical] parmi les 2 ressources (rage 1 + Energy) -> pas de +1 THW",
       "« using [physical][physical] » = DEUX physiques : une seule ne suffit pas",
       [HEROS, "Puzzle.PutIntoPlay('tr008', under_control=True)", "Puzzle.Exhaust('tr001a')", "Puzzle.Counter('tr001a', 'rage', 1)"],
       ["Puzzle.Action('tr008', 'HeroAction')"],
       {"pret": ["tr001a"], "exhausted": ["tr008"], "attributs": {"thwart": 0}},
       main_exclusive=["01088"], payer_avec=["01088"]),
    _c("tr008 Shell Cycle : 2 COMPTEURS DE RAGE comptent comme [physical][physical] -> +1 THW",
       "les compteurs de rage depenses comme ressource physique comptent dans le paiement de l'ABILITE",
       [HEROS, "Puzzle.PutIntoPlay('tr008', under_control=True)", "Puzzle.Exhaust('tr001a')", "Puzzle.Counter('tr001a', 'rage', 2)"],
       ["Puzzle.Action('tr008', 'HeroAction')"],
       {"pret": ["tr001a"], "exhausted": ["tr008"], "attributs": {"thwart": 1}, "compteurs_identite": [["rage", 0]]},
       main_exclusive=["01089"]),
    # ===================================================================== tr009 Raph's Punching Bag
    _c("tr009 Punching Bag : Raph gets +2 REC en forme ALTER-EGO",
       "« Raph gets +2 REC » : le bonus vise l'alter-ego (REC 4 -> 6)",
       ["Puzzle.PutIntoPlay('tr009', under_control=True)"], [],
       {"forme": "AlterEgo", "attributs": {"recover": 2}}, main_exclusive=["01090"]),
    _c("tr009 Punching Bag : le bonus de REC ne FUIT PAS sur la forme heros (contre-cas dans l'autre forme)",
       "RECETTES §3 (defaut `an002` Sera) : un bonus d'identite exige un contre-cas dans l'autre forme ; REC du heros inchange",
       [HEROS, "Puzzle.PutIntoPlay('tr009', under_control=True)"], [],
       {"forme": "Hero", "pas_de_rec": True}, main_exclusive=["01090"], verifier="raphael_etat"),
    _c("tr009 Punching Bag : retire TOUTES les rages (3) et pioche 3 ; le Sac s'incline",
       "« remove all rage counters from your identity -> draw 1 card for each removed » : le nombre RETIRE (3), pas un chiffre fixe",
       ["Puzzle.PutIntoPlay('tr009', under_control=True)", "Puzzle.Counter('tr001b', 'rage', 3)", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01090', '01090', '01090', '01090')"],
       ["Puzzle.Action('tr009', 'AlterEgoAction')"],
       {"compteurs_identite": [["rage", 0]], "taille_main": 4, "exhausted": ["tr009"]}, main_exclusive=["01089"]),
    _c("tr009 Punching Bag : 1 rage retiree -> 1 pioche (pas 3)",
       "la pioche suit le nombre REELLEMENT retire",
       ["Puzzle.PutIntoPlay('tr009', under_control=True)", "Puzzle.Counter('tr001b', 'rage', 1)", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01090', '01090', '01090', '01090')"],
       ["Puzzle.Action('tr009', 'AlterEgoAction')"],
       {"compteurs_identite": [["rage", 0]], "taille_main": 2, "exhausted": ["tr009"]}, main_exclusive=["01089"]),
    _c("tr009 Punching Bag : les compteurs gagnes en forme HEROS PERSISTENT apres le retournement et se retirent en civil",
       "les compteurs vivent sur la CARTE d'identite, partagee par les deux faces : 2 rage posees en Raphael, retirees par le Sac en Raph",
       [HEROS, "Puzzle.Counter('tr001a', 'rage', 2)", CIVIL, "Puzzle.PutIntoPlay('tr009', under_control=True)", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01090', '01090', '01090', '01090')"],
       ["Puzzle.Action('tr009', 'AlterEgoAction')"],
       {"forme": "AlterEgo", "compteurs_identite": [["rage", 0]], "taille_main": 3}, main_exclusive=["01089"]),
    _c("tr009 Punching Bag : sans compteur de rage, l'Action n'est pas offerte (le Sac reste pret, aucune pioche)",
       "`RemoveEachCounter` n'offre l'Action qu'avec au moins un compteur",
       ["Puzzle.PutIntoPlay('tr009', under_control=True)", SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090')"], [],
       {"pret": ["tr009"], "taille_main": 1}, main_exclusive=["01089"],
       declencher_tolerant=["Puzzle.Action('tr009', 'AlterEgoAction')"]),
    # ===================================================================== tr010 Gekido
    _c("tr010 Gekido : incline et pose 1 rage sur Raphael (1re branche)",
       "« Exhaust Gekido -> choose: place 1 rage / heal 1 »",
       [HEROS, "Puzzle.PutIntoPlay('tr010', under_control=True)"], ["Puzzle.Action('tr010', 'HeroAction')"],
       {"exhausted": ["tr010"], "compteurs_identite": [["rage", 1]]}, main_exclusive=["01090"]),
    _c("tr010 Gekido : la rage de Gekido n'a AUCUN plafond (3 -> 4)",
       "decision du 15/10/2026 : pas de « to a maximum of 3 » imprime sur Gekido",
       [HEROS, "Puzzle.PutIntoPlay('tr010', under_control=True)", "Puzzle.Counter('tr001a', 'rage', 3)"], ["Puzzle.Action('tr010', 'HeroAction')"],
       {"exhausted": ["tr010"], "compteurs_identite": [["rage", 4]]}, main_exclusive=["01090"]),
    _c("tr010 Gekido : 2e branche, soigne 1 degat de Raphael (3 degats -> 2), pas de rage",
       "l'autre branche du « choose » (`preferer_option`)",
       [HEROS, "Puzzle.PutIntoPlay('tr010', under_control=True)", "Puzzle.Damage('tr001a', 3)"], ["Puzzle.Action('tr010', 'HeroAction')"],
       {"exhausted": ["tr010"], "degats_identite": 2, "compteurs_identite": [["rage", 0]]}, main_exclusive=["01090"],
       preferer_option=["heal"]),
    _c("tr010 Gekido : soin sans degat = rien (aucun plantage), Gekido s'incline",
       "« heal 1 damage » sur une identite intacte",
       [HEROS, "Puzzle.PutIntoPlay('tr010', under_control=True)"], ["Puzzle.Action('tr010', 'HeroAction')"],
       {"exhausted": ["tr010"], "degats_identite": 0, "compteurs_identite": [["rage", 0]]}, main_exclusive=["01090"],
       preferer_option=["heal"]),
    _c("tr010 Gekido : l'Action est ABSENTE en forme civile (Hero Action) : Gekido reste pret, aucune rage",
       "contre-cas dans l'autre forme",
       ["Puzzle.PutIntoPlay('tr010', under_control=True)"], [],
       {"forme": "AlterEgo", "pret": ["tr010"], "compteurs_identite": [["rage", 0]]}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('tr010', 'HeroAction')"]),
    # ===================================================================== tr011 Raphael's Sai
    _c("tr011 Raphael's Sai : Action d'attaque = incline, 1 degat a l'identite, 1 degat a l'ennemi, 1 rage",
       "« Hero Action (attack): Exhaust this card and take 1 damage -> deal 1 damage to an enemy » + encart (1 rage, max 3, decision du 15/10/2026) ; "
       "Yaban Hito ne part pas (degats de cout, pas une attaque) : 1 rage et non 2",
       [HEROS, "Puzzle.PutIntoPlay('tr011', under_control=True)"], ["Puzzle.Action('tr011', 'HeroAction')"],
       {"exhausted": ["tr011"], "degats": [["01094", 1]], "degats_identite": 1, "compteurs_identite": [["rage", 1]]},
       main_exclusive=["01090"], cibles=["01094"]),
    _c("tr011 Raphael's Sai : la rage de la Sai est plafonnee a 3 (3 -> 3)",
       "TEMOIN D'EPUISEMENT du plafond imprime sur l'encart : chiffre mesure",
       [HEROS, "Puzzle.PutIntoPlay('tr011', under_control=True)", "Puzzle.Counter('tr001a', 'rage', 3)"], ["Puzzle.Action('tr011', 'HeroAction')"],
       {"exhausted": ["tr011"], "degats": [["01094", 1]], "degats_identite": 1, "compteurs_identite": [["rage", 3]]},
       main_exclusive=["01090"], cibles=["01094"]),
    _c("tr011 Raphael's Sai : l'Action est ABSENTE en forme civile (Hero Action) : aucun degat, Sai prete",
       "contre-cas dans l'autre forme",
       ["Puzzle.PutIntoPlay('tr011', under_control=True)"], [],
       {"forme": "AlterEgo", "pret": ["tr011"], "degats": [["01094", 0]], "degats_identite": 0}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('tr011', 'HeroAction')"], cibles=["01094"]),
    _c("tr011 Raphael's Sai : l'Action est une ATTAQUE (label attack) : un heros ETOURDI la consomme, aucun degat a Rhino",
       "`SetLabel('attack')` livre l'action au statut Stunned : le statut tombe et l'attaque est annulee",
       [HEROS, "Puzzle.PutIntoPlay('tr011', under_control=True)", "Puzzle.Stun('tr001a')"], ["Puzzle.Action('tr011', 'HeroAction')"],
       {"exhausted": ["tr011"], "degats": [["01094", 0]], "statuts_absents": [["tr001a", "Stunned"]]},
       main_exclusive=["01090"], cibles=["01094"]),
    _c("tr011 Raphael's Sai : Restricted (base moteur) : un 3e objet Restricted n'est PAS gardable, 2 restent en jeu",
       "mot-cle Restricted (fiche restricted.md, aucun script) : 2 cartes Restricted au plus ; tr011, tr012 puis Hawkeye's Bow (04002)",
       [HEROS], [],
       {"restreintes": 2}, main_exclusive=["tr011", "tr012", "04002", "01090", "01090", "01090"],
       jouer=["tr011", "tr012", "04002"], verifier="raphael_etat"),
    # ===================================================================== tr012 Raphael's Other Sai
    _c("tr012 Other Sai : apres que Raphael vainc un SBIRE (attaque de base), exhaust -> pioche 1",
       "« Hero Response: After Raphael defeats an enemy, exhaust this card -> draw 1 card » : sbire 3 PV, ATQ 3",
       [HEROS, "Puzzle.PutIntoPlay('tr012', under_control=True)", "Puzzle.PutIntoPlay('01101')",
        SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090')"], ["Puzzle.Attack('tr001a')"],
       {"hors_jeu": ["01101"], "exhausted": ["tr012"], "taille_main": 2}, main_exclusive=["01089"], cibles=["01101"]),
    _c("tr012 Other Sai : la Reponse ne part PAS si la Sai est deja inclinee",
       "« exhaust this card » est un cout : une Sai inclinee ne repond pas",
       [HEROS, "Puzzle.PutIntoPlay('tr012', under_control=True, exhaust=True)", "Puzzle.PutIntoPlay('01101')",
        SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090')"], ["Puzzle.Attack('tr001a')"],
       {"hors_jeu": ["01101"], "exhausted": ["tr012"], "taille_main": 1}, main_exclusive=["01089"], cibles=["01101"]),
    _c("tr012 Other Sai : une victoire d'un ALLIE ne declenche pas la Reponse (Jessica Jones tue le sbire)",
       "« After RAPHAEL defeats » : pas un allie",
       [HEROS, "Puzzle.PutIntoPlay('tr012', under_control=True)", "Puzzle.PutIntoPlay('01059', under_control=True)",
        "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage('01101', 1)",
        SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090')"], ["Puzzle.Attack('01059')"],
       {"hors_jeu": ["01101"], "pret": ["tr012"], "taille_main": 1}, main_exclusive=["01089"], cibles=["01101"]),
    _c("tr012 Other Sai : la Reponse part aussi pour un ennemi vaincu HORS attaque de base (Headbutt, evenement)",
       "pas de `is_from_attack` : tout ennemi vaincu par Raphael, ici par les 4 degats de Headbutt",
       [HEROS, "Puzzle.PutIntoPlay('tr012', under_control=True)", "Puzzle.PutIntoPlay('01101')",
        SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090')"], [],
       {"hors_jeu": ["01101"], "exhausted": ["tr012"], "taille_main": 1, "defausse": ["tr004"]},
       main_exclusive=["tr004", "01090"], jouer=["tr004"], cibles=["01101"]),
    _c("tr012 Other Sai : DEUX Sai en jeu = deux Reponses pour un meme ennemi vaincu (2 pioches), les deux s'inclinent",
       "encart : « une Sai OU les deux » ; chaque Sai porte la Reponse (tr011 la recoit par tr012)",
       [HEROS, "Puzzle.PutIntoPlay('tr012', under_control=True)", "Puzzle.PutIntoPlay('tr011', under_control=True)",
        "Puzzle.PutIntoPlay('01101')", SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01090', '01090')"],
       ["Puzzle.Attack('tr001a')"],
       {"hors_jeu": ["01101"], "exhausted": ["tr012", "tr011"], "taille_main": 3}, main_exclusive=["01089"], cibles=["01101"]),
    _c("tr012 Other Sai : la capacite d'attaque n'existe sur tr012 que si tr011 est en jeu (Other Sai seule : rien)",
       "contre-cas du « gains » : sans Raphael's Sai en jeu, l'Action d'attaque n'est pas donnee",
       [HEROS, "Puzzle.PutIntoPlay('tr012', under_control=True)"], [],
       {"pret": ["tr012"], "degats": [["01094", 0]], "degats_identite": 0}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('tr012', 'HeroAction')"], cibles=["01094"]),
    _c("tr012 Other Sai : AVEC tr011 en jeu, tr012 offre aussi l'attaque (1 degat a Rhino, 1 a l'identite, 1 rage)",
       "« Each SAI upgrade you control gains » : la Sai qui porte la Reponse recoit l'Action d'attaque de l'autre",
       [HEROS, "Puzzle.PutIntoPlay('tr011', under_control=True)", "Puzzle.PutIntoPlay('tr012', under_control=True)"],
       ["Puzzle.Action('tr012', 'HeroAction')"],
       {"exhausted": ["tr012"], "pret": ["tr011"], "degats": [["01094", 1]], "degats_identite": 1, "compteurs_identite": [["rage", 1]]},
       main_exclusive=["01090"], cibles=["01094"]),
    _c("tr012 Other Sai : un ennemi vaincu PAR UNE SAI (le sbire a 1 PV tombe sous l'Action de tr011) -> tr012 pioche",
       "les degats de la Sai sont infliges par le HEROS : Raphael est l'auteur de la victoire",
       [HEROS, "Puzzle.PutIntoPlay('tr011', under_control=True)", "Puzzle.PutIntoPlay('tr012', under_control=True)",
        "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage('01101', 2)", SANS_DECK,
        "Puzzle.CreatePlayerDeck('01090', '01090')"],
       ["Puzzle.Action('tr011', 'HeroAction')"],
       {"hors_jeu": ["01101"], "exhausted": ["tr011", "tr012"], "taille_main": 2, "compteurs_identite": [["rage", 1]]},
       main_exclusive=["01089"], cibles=["01101"]),
    # ===================================================================== tr013 Out of Control
    _c("tr013 Out of Control (recue en forme CIVILE) : retourne en forme HEROS et incline l'identite",
       "« Flip to hero form and exhaust your identity » : l'obligation est recue par Raph (GiveTo Raph)",
       [], ["Puzzle.Reveal('tr013')"],
       {"forme": "Hero", "exhausted": ["tr001a"], "en_jeu": ["tr013"]}, main_exclusive=["01090"]),
    _c("tr013 Out of Control (recue en forme HEROS) : reste heros, identite inclinee",
       "« flip to hero form » sans effet quand on l'est deja ; l'identite s'incline",
       [HEROS], ["Puzzle.Reveal('tr013')"],
       {"forme": "Hero", "exhausted": ["tr001a"], "en_jeu": ["tr013"]}, main_exclusive=["01090"]),
    _c("tr013 Out of Control : « GiveTo Raph » vise le BON joueur (2 joueurs : Raphael en 2e siege)",
       "le joueur qui n'est pas Raph n'est ni retourne ni incline",
       [], ["Puzzle.Reveal('tr013')"],
       {"forme_joueur": [[1, "Hero"], [0, "AlterEgo"]], "identite_inclinee_joueur": [[1, True], [0, False]]},
       heros="spider_man", heros2="raphael", main_exclusive=["01090"], verifier="raphael_etat"),
    _c("tr013 Out of Control : ne peut PAS changer de forme (retour en civil refuse, reste Raphael)",
       "« You cannot change forms » : `PlayersCannotChangeForms` sur le joueur rattache",
       [], ["Puzzle.Reveal('tr013')", "Puzzle.Ready('tr001a')"],
       {"forme": "Hero", "en_jeu": ["tr013"]}, main_exclusive=["01090"],
       declencher_apres=["Puzzle.ChangeForm('tr001a')"]),
    _c("tr013 Out of Control : l'IDENTITE ne peut pas CONTRER (Raphael pret, menace 3 inchangee)",
       "« You cannot thwart » : identite seulement",
       ["Puzzle.SetThreat('01097b', 3)"], ["Puzzle.Reveal('tr013')", "Puzzle.Ready('tr001a')"],
       {"menace": [["01097b", 3]]}, main_exclusive=["01090"],
       declencher_apres=["Puzzle.Thwart('tr001a')"]),
    _c("tr013 Out of Control : un ALLIE peut contrer (Jessica Jones THW 1* : menace 3 -> 2)",
       "decision du 15/10/2026 : « vous » = l'identite seulement, les allies contrent",
       ["Puzzle.SetThreat('01097b', 3)", "Puzzle.PutIntoPlay('01059', under_control=True)"],
       ["Puzzle.Reveal('tr013')", "Puzzle.Ready('tr001a')"],
       {"menace": [["01097b", 2]]}, main_exclusive=["01090"],
       declencher_apres=["Puzzle.Thwart('01059')"]),
    _c("tr013 Out of Control : l'IDENTITE ne peut pas DEFENDRE (Rhino ATQ 2 passe en entier : 2 degats)",
       "« You cannot defend » : sans l'interdit Raphael (DEF 2) encaisserait 0",
       [], ["Puzzle.Reveal('tr013')", "Puzzle.Ready('tr001a')"],
       {"degats_identite": 2}, main_exclusive=["01090"],
       declencher_apres=["Puzzle.Defend('tr001a', '01094')"]),
    _c("tr013 Out of Control : temoin SANS l'obligation, Raphael DEFEND (DEF 2 contre ATQ 2 : 0 degat)",
       "le contre-cas qui rend le cas precedent significatif",
       [HEROS], [],
       {"degats_identite": 0}, main_exclusive=["01090"],
       declencher_apres=["Puzzle.Defend('tr001a', '01094')"]),
    _c("tr013 Out of Control : un ALLIE peut DEFENDRE (Jessica Jones prend le coup, l'identite 0 degat)",
       "decision du 15/10/2026 : les allies defendent",
       ["Puzzle.PutIntoPlay('01059', under_control=True)"], ["Puzzle.Reveal('tr013')", "Puzzle.Ready('tr001a')"],
       {"degats_identite": 0, "degats": [["01059", 2]]}, main_exclusive=["01090"],
       declencher_apres=["Puzzle.Defend('01059', '01094')"]),
    _c("tr013 Out of Control : Hero Action = retire 2 rage, retourne en civil ET defausse l'obligation",
       "« Remove 2 rage counters from Raphael -> flip to alter-ego form and discard Out of Control » : la carte elle-meme peut retourner l'identite",
       [], ["Puzzle.Reveal('tr013')", "Puzzle.Counter('tr001a', 'rage', 2)", "Puzzle.Action('tr013', 'HeroAction')"],
       {"forme": "AlterEgo", "hors_jeu": ["tr013"], "compteurs_identite": [["rage", 0]]}, main_exclusive=["01090"]),
    _c("tr013 Out of Control : avec 1 seule rage la sortie n'est PAS offerte (reste Raphael, obligation en jeu, rage 1)",
       "cout `Remove 2 rage` : sans 2 compteurs l'Action n'existe pas",
       [], ["Puzzle.Reveal('tr013')", "Puzzle.Counter('tr001a', 'rage', 1)"],
       {"forme": "Hero", "en_jeu": ["tr013"], "compteurs_identite": [["rage", 1]]}, main_exclusive=["01090"],
       declencher_apres=[], declencher_tolerant=["Puzzle.Action('tr013', 'HeroAction')"]),
]
VERIFICATIONS = r'''
CLES_RAPHAEL = {"jouable", "restreintes", "fin_de_round", "forme_joueur", "identite_inclinee_joueur",
                "timer", "taille_deck_rencontre", "cartes_distribuees", "sonde", "pas_de_rec"}

def _raphael_fin_de_round(monde):
    from game.message import Message
    from game.effect.rule import GameRule
    m = Message.WhenRoundEnd(monde)
    m.Send()
    monde.buff_manager.OnRoundEnd()
    monde.ProcessTemporary(GameRule(monde.const_players[0].GetIdentity()))
    Message.AfterRoundEnd(m).Send()

def raphael_etat(monde, aides):
    """etat_attendu (cles communes) + cles propres a Raphael :
    jouable [[card_id_en_main, bool]], restreintes n, fin_de_round (envoie une fin de round AVANT de mesurer),
    forme_joueur [[siege, Hero|AlterEgo]], identite_inclinee_joueur [[siege, bool]], timer [[card_id, n]],
    taille_deck_rencontre n, cartes_distribuees n."""
    attendu = aides["cas"].get("attendu") or {}
    inconnues = sorted(set(attendu) - set(CLES_ETAT_ATTENDU) - CLES_RAPHAEL)
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de raphael_etat : {inconnues}"
    soucis = []
    joueur = monde.players[0]
    if attendu.get("fin_de_round"):
        _raphael_fin_de_round(monde)
    for card_id, voulu in attendu.get("jouable") or []:
        face = None
        for f in joueur.hand_cards.GetAll():
            if getattr(f.paper, "card_id", None) == card_id:
                face = f
                break
        if face is None:
            soucis.append(f"{card_id} n'est pas en main (jouable)")
            continue
        reel = bool(face.CanPlayBy(joueur))
        if reel != voulu:
            soucis.append(f"{card_id} jouable = {reel} (attendu {voulu})")
    if "restreintes" in attendu:
        restreintes = [getattr(f.paper, "card_id", None) for f in joueur.GetControlUpgrade()
                       if (getattr(f.paper, "desc", None) or {}).get("Restricted")]
        if len(restreintes) != attendu["restreintes"]:
            soucis.append(f"cartes Restricted en jeu = {restreintes} (attendu {attendu['restreintes']})")
    for siege, forme in attendu.get("forme_joueur") or []:
        j = monde.const_players[siege]
        reelle = "Hero" if j.IsHero() else "AlterEgo"
        if reelle != forme:
            soucis.append(f"forme du siege {siege} = {reelle} (attendu {forme})")
    for siege, voulu in attendu.get("identite_inclinee_joueur") or []:
        j = monde.const_players[siege]
        reel = bool(j.GetIdentity().IsExhaust())
        if reel != voulu:
            soucis.append(f"identite du siege {siege} inclinee = {reel} (attendu {voulu})")
    for card_id, n in attendu.get("timer") or []:
        face = aides["par_id"](monde, card_id)
        if face is None:
            soucis.append(f"{card_id} introuvable en jeu (timer)")
        elif face.GetCounters("timer") != n:
            soucis.append(f"{card_id}.timer = {face.GetCounters('timer')} (attendu {n})")
    if "taille_deck_rencontre" in attendu:
        from game.operate.worlds import Worlds
        n = len(Worlds.GetEncounterDeckCards(monde))
        if n != attendu["taille_deck_rencontre"]:
            soucis.append(f"deck rencontre = {n} carte(s) (attendu {attendu['taille_deck_rencontre']})")
    if "cartes_distribuees" in attendu:
        n = sum(len(list(j.dealt_encounter_cards.GetAll())) for j in monde.players)
        if n != attendu["cartes_distribuees"]:
            soucis.append(f"cartes rencontre distribuees face cachee = {n} (attendu {attendu['cartes_distribuees']})")
    if attendu.get("pas_de_rec"):
        # La face HEROS n'imprime aucune REC : le bonus du Sac (alter-ego) ne doit lui en donner aucune.
        rec = getattr(monde.players[0].GetIdentity(), "recover", None)
        if rec not in (None, 0):
            soucis.append(f"la forme heros a une REC de {rec} (le bonus du Sac a fui)")
    if attendu.get("sonde"):
        return False, "SONDE " + repr(sonde_raphael(monde))
    reste = {k: v for k, v in attendu.items() if k not in CLES_RAPHAEL}
    copie = dict(aides)
    copie["cas"] = dict(aides["cas"], attendu=reste, verifier="raphael_etat")
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    return (not soucis), ("etat conforme" if not soucis else " ; ".join(soucis))

def sonde_raphael(monde):
    from game.operate.worlds import Worlds
    j = monde.players[0]
    return {"deck_rencontre": [getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde)],
            "aside_nemesis": [getattr(f.paper, "card_id", None) for f in j.set_aside_nemesis_sets.Get(True)],
            "main": [getattr(f.paper, "card_id", None) for f in j.hand_cards.GetAll()]}
'''
