# Cas test_capacites du heros custom BINARY (Galactic Storm, Kajislav, prefixe `gs`, lot GS-1) :
# noms prefixes « [binary] » puis le card_id (substituer_pack.py filtre dessus). Gabarits PROCESSUS-CARTE :
# docs/packs/galactic-storm/BINARY-GABARITS.md. Questions : .planning/todos/2026-10-20-gs1-questions.md.
#
# Rappels de montage :
#  - Binary demarre en ALTER EGO (gs001b Carol Danvers) ; `Puzzle.ChangeToFace('gs001b', 'gs001a')` la passe
#    en forme HEROS ;
#  - le deck de depart a un `player_deck` COMPLET (liste de l'auteur) : `main_exclusive` fixe la main, et
#    les icones (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR, 43034 Combat Specialist = G)
#    font varier « the number of [energy] resources in your hand » ;
#  - Rhino 01094 (14 PV, ATQ 2) est le vilain, 01097b son complot principal, 01101 Hydra Mercenary (Garde,
#    3 PV) un sbire, 01172 Whiplash (Riposte 1) un sbire a riposte ;
#  - « after your turn ends » et « after the player phase begins » ne sont pas joignables par l'API Puzzle :
#    les verificateurs `bn_fin_de_tour` / `bn_debut_phase` envoient le message du moteur puis mesurent.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('gs001b', 'gs001a')"
CIVIL = "Puzzle.ChangeToFace('gs001a', 'gs001b')"
SANS_DECK = "Puzzle.EmptyPlayerDeck()"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
VIDER_DEFAUSSE = "Puzzle.EmptyPlayerDiscardPile()"
COMPLOT = "01097b"


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[binary] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "binary"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "bn_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ gs001a Binary : ATQ X
    _c("gs001a Binary : ATQ X = icones [energy] en main (Energy YY + Solar Flare Y = 3)",
       "« X is the number of [energy] resources in your hand » : des ICONES, Energy (YY) en vaut 2",
       [HEROS], [], {"attrs": [["gs001a", "attack", 3]]}, main_exclusive=["01088", "gs005"]),
    _c("gs001a Binary : ATQ X plafonnee a 5 (6 icones [energy] en main)",
       "« (to a maximum of 5) » : Energy YY + Energy Torrent YY + Pursued Y + Solar Flare Y = 6 -> 5",
       [HEROS], [], {"attrs": [["gs001a", "attack", 5]]}, main_exclusive=["01088", "gs006", "gs004", "gs005"]),
    _c("gs001a Binary : ATQ X ignore le physique, le mental et le wild (Strength RR, Genius BB, Combat Specialist G -> 0)",
       "lecture Q3 : seules les icones [energy] comptent, le wild n'en est pas une tant qu'il reste en main",
       [HEROS], [], {"attrs": [["gs001a", "attack", 0]]}, main_exclusive=["01090", "01089", "43034"]),
    _c("gs001a Binary : ATQ X suit la main (on gagne une Energy en cours de tour : 0 -> 2)",
       "rafraichi sur `OnEvent.HandCards` : la statistique bouge quand la main bouge",
       [HEROS], ["Puzzle.Gain('01088')"], {"attrs": [["gs001a", "attack", 2]]}, main_exclusive=["01090"]),
    _c("gs001a Binary : valeurs imprimees PV 12, CTR 2, DEF 2, main 5, AERIAL STARJAMMER",
       "nombres texte <-> code (scan 1A) : HAND SIZE 5 / HIT POINTS 12, THW 2, ATK X, DEF 2",
       [HEROS], [], {"attrs": [["gs001a", "max_health", 12], ["gs001a", "thwart", 2], ["gs001a", "defense", 2],
                               ["gs001a", "hand_size", 5]], "traits": ["AERIAL", "STARJAMMER"]},
       main_exclusive=["01090"]),
    # ============================================================ gs001a Binary : Burnout
    _c("gs001a Burnout : apres le tour, les cartes [energy] de la main partent, les autres restent",
       "« Forced Response: After your turn ends, discard each [energy] resource from your hand »",
       [HEROS], [VIDER_DEFAUSSE], {"main_ids": ["01090"], "defausse_avec": ["01088", "gs005"]},
       main_exclusive=["01088", "01090", "gs005"], verifier="bn_fin_de_tour"),
    _c("gs001a Burnout : absent en ALTER EGO (Carol Danvers garde ses cartes [energy])",
       "contre-cas dans l'AUTRE forme : Burnout est imprime sur la face heros",
       [], [VIDER_DEFAUSSE], {"main_ids": ["01088", "01090", "gs005"]},
       main_exclusive=["01088", "01090", "gs005"], verifier="bn_fin_de_tour"),
    _c("gs001a Burnout + Energy Conversion : toute carte a ressource devient [energy] et part",
       "lecture litterale : sous Energy Conversion, Strength (RR) est traitee [energy] en main",
       [HEROS, *en_jeu("gs010")], [VIDER_DEFAUSSE], {"main_ids": [], "defausse_avec": ["01088", "01090"]},
       main_exclusive=["01088", "01090"], verifier="bn_fin_de_tour"),
    # ============================================================ gs001b Carol Danvers
    _c("gs001b Exploring Space : Action, piocher 1 carte (main 1 -> 2)",
       "« Exploring Space — Action: Draw 1 card »",
       [], ["Puzzle.Action('gs001b', 'Action')"], {"taille_main": 2}, main_exclusive=["01090"]),
    _c("gs001b Exploring Space : limite 1 par round (TEMOIN D'EPUISEMENT) : deux tentatives, 1 seule pioche",
       "« (Limit once per round.) » : la 2e Action est refusee, main 2 et non 3",
       [], ["Puzzle.Action('gs001b', 'Action')"], {"taille_main": 2}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('gs001b', 'Action')"]),
    _c("gs001b Exploring Space : absente en forme HEROS (aucune pioche)",
       "contre-cas : l'Action est imprimee sur la face Carol Danvers",
       [HEROS], [], {"taille_main": 1}, main_exclusive=["01090"],
       declencher_tolerant=["Puzzle.Action('gs001a', 'Action')"]),
    _c("gs001b Carol Danvers : valeurs imprimees PV 12, REC 4, main 5, ASTRONAUT",
       "nombres texte <-> code (scan 1B)",
       [], [], {"attrs": [["gs001b", "max_health", 12], ["gs001b", "recover", 4], ["gs001b", "hand_size", 5]],
                "traits": ["ASTRONAUT"]}, main_exclusive=["01090"]),
    # ============================================================ gs002 Cosmic Influx
    _c("gs002 Cosmic Influx : pioche 3 (Energy, Genius, Strength) et subit 4 degats (BB + RR)",
       "« Draw 3 cards. Take 1 damage for each non-[energy] resource drawn » : icones, Energy YY ne blesse pas",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01089', '01088')"], [],
       {"main_ids": ["01088", "01089", "01090"], "degats_identite": 4},
       main_exclusive=["gs002", "43034"], jouer=["gs002"]),
    _c("gs002 Cosmic Influx + Energy Conversion : aucun degat (FAQ du livret 1.2 p.22)",
       "« the cards are drawn first and ... being treated as energy resources they cause none »",
       [HEROS, *en_jeu("gs010"), SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01089', '01088')"], [],
       {"main_ids": ["01088", "01089", "01090"], "degats_identite": 0},
       main_exclusive=["gs002", "43034"], jouer=["gs002"]),
    _c("gs002 Cosmic Influx : Max 1 par round (TEMOIN D'EPUISEMENT) : la 2e copie reste en main (main 5 et non 6)",
       "« Max 1 per round » : 4 cartes, une jouee + une depensee + 3 piochees = 5 ; sans la limite, la 2e partirait (6)",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01088', '01088', '01088', '01088', '01088', '01088')"], [],
       {"en_main": ["gs002"], "taille_main": 5, "degats_identite": 0},
       main_exclusive=["gs002", "gs002", "43034", "43034"], jouer=["gs002", "gs002"]),
    # ============================================================ gs003 Fuel the Fire
    _c("gs003 Fuel the Fire : 2 [energy] en main, attaque de Rhino (2) : 2 evites et 2 soignes (3 -> 1 degat)",
       "« for each [energy] resource in your hand prevent 1 of that damage and heal 1 damage from Binary »",
       [HEROS, "Puzzle.Damage('gs001a', 3)", "Puzzle.Exhaust('gs001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 1, "defausse_avec": ["gs003"]}, main_exclusive=["gs003", "01088"]),
    _c("gs003 Fuel the Fire : 1 seule [energy] : 1 evite, 1 soigne (3 -> 3 degats)",
       "le compte suit la main : Pursued by the Flame (Y) seule",
       [HEROS, "Puzzle.Damage('gs001a', 3)", "Puzzle.Exhaust('gs001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 3, "defausse_avec": ["gs003"]}, main_exclusive=["gs003", "gs004"]),
    _c("gs003 Fuel the Fire : sans [energy] en main, elle n'est pas jouee (Rhino frappe 2 : 3 -> 5)",
       "condition « rien a changer » : la carte reste en main",
       [HEROS, "Puzzle.Damage('gs001a', 3)", "Puzzle.Exhaust('gs001a')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 5, "en_main": ["gs003"]}, main_exclusive=["gs003", "01090"]),
    # ============================================================ gs004 Pursued by the Flame
    _c("gs004 Pursued by the Flame : retire 2 menaces et redresse Binary (Energy YY restee en main)",
       "« Remove 2 threat from a scheme. If you have at least [energy][energy] resources in your hand, ready Binary »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.Exhaust('gs001a')"], [],
       {"menace": [[COMPLOT, 3]], "pret": ["gs001a"]},
       main_exclusive=["gs004", "01089", "01088"], payer_avec=["01089"], jouer=["gs004"]),
    _c("gs004 Pursued by the Flame : 1 seule [energy] en main : menace retiree, Binary reste inclinee",
       "seuil « at least [energy][energy] » non atteint (Solar Flare Y seule)",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.Exhaust('gs001a')"], [],
       {"menace": [[COMPLOT, 3]], "exhausted": ["gs001a"]},
       main_exclusive=["gs004", "01089", "gs005"], payer_avec=["01089"], jouer=["gs004"]),
    # ============================================================ gs005 Solar Flare
    _c("gs005 Solar Flare : 2 [energy] restees en main : 4 + 2 = 6 degats a Rhino",
       "« Deal 4 damage ... If you have at least [energy][energy] ..., deal 2 additional damage »",
       [HEROS], [], {"degats": [["01094", 6]]},
       main_exclusive=["gs005", "01089", "01088"], payer_avec=["01089"], jouer=["gs005"], cibles=["01094"]),
    _c("gs005 Solar Flare : 1 seule [energy] : 4 degats seulement",
       "seuil non atteint (Pursued by the Flame Y seule)",
       [HEROS], [], {"degats": [["01094", 4]]},
       main_exclusive=["gs005", "01089", "gs004"], payer_avec=["01089"], jouer=["gs005"], cibles=["01094"]),
    # ============================================================ gs006 Energy Torrent
    _c("gs006 Energy Torrent : depensee pour payer, elle est remelangee dans le deck (pas en defausse)",
       "« Response: After you spend this card, shuffle it into your deck »",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 3)"], [VIDER_DEFAUSSE], {"dans_deck_joueur": ["gs006"], "defausse_sans": ["gs006"]},
       main_exclusive=["gs004", "gs006"], payer_avec=["gs006"], jouer=["gs004"]),
    _c("gs006 Energy Torrent : defaussee par Burnout (pas depensee) : elle reste en defausse",
       "« after you SPEND » : une defausse n'est pas une depense",
       [HEROS], [VIDER_DEFAUSSE], {"defausse_avec": ["gs006"]},
       main_exclusive=["gs006"], verifier="bn_fin_de_tour"),
    # ============================================================ gs007 Prophet-Singer
    _c("gs007 Prophet-Singer : regarde le dessus (Genius) et l'echange avec la carte de la main (Energy)",
       "« look at the top card of your deck and swap it with a card in your hand »",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01089')", *en_jeu("gs007")],
       ["Puzzle.Action('gs007', 'Action')"],
       {"main_ids": ["01089"], "dessus_deck": "01088", "exhausted": ["gs007"]}, main_exclusive=["01088"]),
    _c("gs007 Prophet-Singer : valeurs imprimees (soutien unique, cout 0, AERIAL CREATURE)",
       "nombres texte <-> code (scan 7) ; « Action » nue : utilisable en alter ego (cas ci-dessus)",
       [*en_jeu("gs007")], [], {"traits_de": [["gs007", "AERIAL"], ["gs007", "CREATURE"]]},
       main_exclusive=["01088"]),
    # ============================================================ gs008 White Hole
    _c("gs008 White Hole : defausse Genius et Combat Specialist (wild), ajoute l'Energy a la main",
       "« discard ... until you discard a card with a printed [energy] resource. Add that card to your hand »",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01090', '01088', '43034', '01089')", *en_jeu("gs008")],
       [VIDER_DEFAUSSE, "Puzzle.Action('gs008', 'HeroAction')"],
       {"en_main": ["01088"], "defausse_avec": ["01089", "43034"], "dans_deck_joueur": ["01090"]},
       main_exclusive=["01084"]),
    _c("gs008 White Hole : l'Energy est la DERNIERE carte du deck, elle arrive quand meme en main",
       "piege `Deck.DiscardUntil` (rend None en vidant le deck) : contourne dans gs008",
       [HEROS, SANS_DECK, "Puzzle.CreatePlayerDeck('01088', '01090')", *en_jeu("gs008")],
       [VIDER_DEFAUSSE, "Puzzle.Action('gs008', 'HeroAction')"],
       {"en_main": ["01088"]}, main_exclusive=["01089"]),
    _c("gs008 White Hole : Energy Conversion ne touche PAS le deck (Strength reste [physical] et part)",
       "« in YOUR HAND » : la conversion ne vise que la main",
       [HEROS, *en_jeu("gs010"), SANS_DECK, "Puzzle.CreatePlayerDeck('01089', '01088', '01090')", *en_jeu("gs008")],
       [VIDER_DEFAUSSE, "Puzzle.Action('gs008', 'HeroAction')"],
       {"en_main": ["01088"], "defausse_avec": ["01090"], "dans_deck_joueur": ["01089"]},
       main_exclusive=["01084"]),
    _c("gs008 White Hole : absente en ALTER EGO (Hero Action)",
       "contre-cas dans l'autre forme : rien n'est defausse, le soutien reste pret",
       [SANS_DECK, "Puzzle.CreatePlayerDeck('01088', '01090')", *en_jeu("gs008")], [VIDER_DEFAUSSE],
       {"pret": ["gs008"], "dans_deck_joueur": ["01088", "01090"]}, main_exclusive=["01089"],
       declencher_tolerant=["Puzzle.Action('gs008', 'HeroAction')"]),
    # ============================================================ gs009 Body in Flames
    _c("gs009 Body in Flames : 2 [energy] en main -> riposte 1",
       "palier « 1 or 2 - Binary gains retaliate 1 »",
       [HEROS, *en_jeu("gs009")], [], {"attrs": [["gs001a", "retaliate", 1]]}, main_exclusive=["01088"]),
    _c("gs009 Body in Flames : 3 [energy] -> riposte 2",
       "palier « 3 or 4 - retaliate 2 »",
       [HEROS, *en_jeu("gs009")], [], {"attrs": [["gs001a", "retaliate", 2]]}, main_exclusive=["01088", "gs005"]),
    _c("gs009 Body in Flames : 6 [energy] -> riposte 3",
       "palier « 5 or more - retaliate 3 »",
       [HEROS, *en_jeu("gs009")], [], {"attrs": [["gs001a", "retaliate", 3]]},
       main_exclusive=["01088", "gs006", "gs004", "gs005"]),
    _c("gs009 Body in Flames : aucune [energy] -> pas de riposte",
       "0 n'est sur aucun palier",
       [HEROS, *en_jeu("gs009")], [], {"attrs": [["gs001a", "retaliate", 0]]}, main_exclusive=["01090"]),
    _c("gs009 Body in Flames : en ALTER EGO, Carol Danvers ne riposte pas (« BINARY gains »)",
       "contre-cas dans l'autre forme (RECETTES §3, NOM de la face heros)",
       [*en_jeu("gs009")], [], {"attrs": [["gs001b", "retaliate", 0]]}, main_exclusive=["01088", "gs005"]),
    # ============================================================ gs010 Energy Conversion
    _c("gs010 Energy Conversion : Strength (RR) en main compte 2 [energy] pour l'ATQ X",
       "« Treat the printed resources of each card in your hand as if they were [energy] resources »",
       [HEROS, *en_jeu("gs010")], [], {"attrs": [["gs001a", "attack", 2]]}, main_exclusive=["01090"]),
    _c("gs010 Energy Conversion : Temporary, defaussee a la fin du round",
       "« Temporary » (desc, base automatique) : ProcessTemporary de fin de round",
       [HEROS, *en_jeu("gs010")], [], {"hors_jeu": ["gs010"]}, main_exclusive=["01090"],
       verifier="bn_fin_de_round"),
    _c("gs010 Energy Conversion : partie a la fin du round, l'ATQ X redescend (Strength : 2 -> 0)",
       "la statistique est recalculee quand la conversion quitte le jeu",
       [HEROS, *en_jeu("gs010")], [], {"attrs": [["gs001a", "attack", 0]]}, main_exclusive=["01090"],
       verifier="bn_fin_de_round"),
    # ============================================================ gs011 Light, Radiation, Heat
    _c("gs011 Light, Radiation, Heat : 1 [energy] -> attaque de base a distance, Whiplash ne riposte pas",
       "« 1 - Your basic attacks gain ranged » (Riposte ignoree : 0 degat sur Binary)",
       [HEROS, *en_jeu("gs011"), "Puzzle.PutIntoPlay('01172')"], ["Puzzle.Attack('gs001a')"],
       {"degats_identite": 0, "degats": [["01172", 1]]}, main_exclusive=["gs005"], cibles=["01172"]),
    _c("gs011 Light, Radiation, Heat : TEMOIN sans la carte, Whiplash riposte (1 degat sur Binary)",
       "meme position sans Light, Radiation, Heat",
       [HEROS, "Puzzle.PutIntoPlay('01172')"], ["Puzzle.Attack('gs001a')"],
       {"degats_identite": 1, "degats": [["01172", 1]]}, main_exclusive=["gs005"], cibles=["01172"]),
    _c("gs011 Light, Radiation, Heat : 2 [energy] -> perforante, la carte Tenace de Rhino saute et il subit 2",
       "« 2 - Your basic attacks also gain piercing »",
       [HEROS, *en_jeu("gs011"), "Puzzle.Tough('01094')"], ["Puzzle.Attack('gs001a')"],
       {"degats": [["01094", 2]], "statuts_absents": [["01094", "Tough"]]}, main_exclusive=["01088"],
       cibles=["01094"]),
    _c("gs011 Light, Radiation, Heat : 1 seule [energy] -> pas perforante, la carte Tenace absorbe",
       "paliers cumulatifs : sous 2, pas de perforant",
       [HEROS, *en_jeu("gs011"), "Puzzle.Tough('01094')"], ["Puzzle.Attack('gs001a')"],
       {"degats": [["01094", 0]]}, main_exclusive=["gs005"], cibles=["01094"]),
    _c("gs011 Light, Radiation, Heat : 3 [energy] -> deferlement, l'exces sur le sbire (1 PV) passe a Rhino (2)",
       "« 3 - Your basic attacks also gain overkill »",
       [HEROS, *en_jeu("gs011"), "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage(Puzzle.FindFaceInPlay('01101'), 2)"],
       ["Puzzle.Attack('gs001a')"], {"degats": [["01094", 2]], "hors_jeu": ["01101"]},
       main_exclusive=["01088", "gs005"], cibles=["01101"]),
    _c("gs011 Light, Radiation, Heat : 2 [energy] -> pas de deferlement, Rhino intact",
       "sous 3, pas de deferlement",
       [HEROS, *en_jeu("gs011"), "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage(Puzzle.FindFaceInPlay('01101'), 2)"],
       ["Puzzle.Attack('gs001a')"], {"degats": [["01094", 0]], "hors_jeu": ["01101"]},
       main_exclusive=["01088"], cibles=["01101"]),
    # ============================================================ gs031 Forgotten Life
    _c("gs031 Forgotten Life : en forme heros, taille de main 5 -> 4",
       "« While in hero form, your hand size is reduced by 1 »",
       [HEROS, "Puzzle.Reveal('gs031')"], [], {"attrs": [["gs001a", "hand_size", 4]], "en_jeu": ["gs031"]},
       main_exclusive=["01090"]),
    _c("gs031 Forgotten Life : en ALTER EGO, Carol Danvers garde sa main de 5",
       "contre-cas : « WHILE IN HERO FORM »",
       ["Puzzle.Reveal('gs031')"], [], {"attrs": [["gs001b", "hand_size", 5]], "en_jeu": ["gs031"]},
       main_exclusive=["01090"]),
    _c("gs031 Forgotten Life : Action d'alter ego, incliner Carol et defausser une carte signature -> retiree du jeu",
       "« Exhaust Carol Danvers and discard an identity-specific card from your hand → remove Forgotten Life »",
       ["Puzzle.Reveal('gs031')"], [VIDER_DEFAUSSE, "Puzzle.Action('gs031', 'AlterEgoAction')"],
       {"hors_jeu": ["gs031"], "exhausted": ["gs001b"], "defausse_avec": ["gs005"], "retiree": ["gs031"]},
       main_exclusive=["gs005", "01090"]),
    _c("gs031 Forgotten Life : sans carte signature en main, l'Action n'est pas payable",
       "contre-cas du second cout : Strength (basique) ne paie pas",
       ["Puzzle.Reveal('gs031')"], ["Puzzle.EmptyPlayerDiscardPile()"],
       {"en_jeu": ["gs031"], "pret": ["gs001b"], "main_ids": ["01090"]},
       main_exclusive=["01090"], declencher_tolerant=["Puzzle.Action('gs031', 'AlterEgoAction')"]),
    # ============================================================ gs032 Rogue
    _c("gs032 Rogue : debut de phase des joueurs, Touched (deck rencontre) s'attache a Binary, qui s'incline",
       "« find Touched and attach it to a character other than Rogue. If it is a friendly character, exhaust »",
       [HEROS, "Puzzle.PutIntoPlay('gs032')", "Puzzle.CreateEncounterDeck('gs237')"], [],
       {"porteur_touched": "gs001a", "exhausted": ["gs001a"]}, verifier="bn_debut_phase", cibles=["gs001a"],
       main_exclusive=["01090"]),
    _c("gs032 Rogue : Touched donnee a RHINO (ennemi) : Rhino n'est pas incline",
       "« IF it is a friendly character » : un ennemi n'est pas incline",
       [HEROS, "Puzzle.PutIntoPlay('gs032')", "Puzzle.CreateEncounterDeck('gs237')"], [],
       {"porteur_touched": "01094", "pret": ["01094", "gs001a"]}, verifier="bn_debut_phase", cibles=["01094"],
       main_exclusive=["01090"]),
    _c("gs032 Rogue : Touched deja attachee a Rhino se DEPLACE sur Binary au debut de phase",
       "« find Touched » : y compris en jeu ; elle quitte son porteur",
       [HEROS, "Puzzle.PutIntoPlay('gs032')", "Puzzle.AttachReel('gs237', '01094')"], [],
       {"porteur_touched": "gs001a"}, verifier="bn_debut_phase", cibles=["gs001a"], main_exclusive=["01090"]),
    _c("gs032 Rogue : vaincue, Touched (attachee a Rhino) est defaussee",
       "« When Defeated: Discard Touched »",
       [HEROS, "Puzzle.PutIntoPlay('gs032')", "Puzzle.AttachReel('gs237', '01094')"],
       ["Puzzle.Damage(Puzzle.FindFaceInPlay('gs032'), 5)"],
       {"hors_jeu": ["gs032", "gs237"], "defausse_rencontre": ["gs237"]}, main_exclusive=["01090"]),
    _c("gs032 Rogue : valeurs imprimees MNG 2, ATQ 2, PV 5, BROTHERHOOD OF MUTANTS ELITE",
       "nombres texte <-> code (scan 32)",
       [HEROS, "Puzzle.PutIntoPlay('gs032')"], [],
       {"attrs": [["gs032", "scheme", 2], ["gs032", "attack", 2], ["gs032", "max_health", 5]],
        "traits_de": [["gs032", "BROTHERHOOD OF MUTANTS"], ["gs032", "ELITE"]]}, main_exclusive=["01090"]),
    # ============================================================ gs237 Touched
    _c("gs237 Touched : revelee avec Rogue en jeu, elle s'attache au personnage choisi (Hope Summers)",
       "« If Rogue is in play, attach to a character other than Rogue »",
       [HEROS, "Puzzle.PutIntoPlay('gs032')", *en_jeu("40204")], ["Puzzle.Reveal('gs237')"],
       {"porteur_touched": "40204"}, cibles=["40204"], main_exclusive=["01090"]),
    _c("gs237 Touched : revelee SANS Rogue en jeu, elle gagne Renfort (1 carte distribuee)",
       "« Otherwise, this card gains surge »",
       [HEROS], ["Puzzle.Reveal('gs237')"], {"porteur_touched": None}, surge_hors_phase=1,
       main_exclusive=["01090"]),
    _c("gs237 Touched sur un SBIRE : Rogue gagne riposte 2",
       "« Minion, Rogue gains retaliate 2 »",
       [HEROS, "Puzzle.PutIntoPlay('gs032')", "Puzzle.PutIntoPlay('01101')"],
       ["Puzzle.AttachReel('gs237', Puzzle.FindFaceInPlay('01101'))"],
       {"attrs": [["gs032", "retaliate", 2], ["gs032", "attack", 2], ["gs032", "villainous", 0]]},
       main_exclusive=["01090"]),
    _c("gs237 Touched sur le VILAIN : Binary (ATQ 3) frappe Rogue, elle ne subit que 1",
       "« Villain, reduce the damage Rogue takes from each attack by 2 »",
       [HEROS, "Puzzle.PutIntoPlay('gs032')", "Puzzle.AttachReel('gs237', '01094')"], ["Puzzle.Attack('gs001a')"],
       {"degats": [["gs032", 1]], "attrs": [["gs032", "retaliate", 0]]},
       main_exclusive=["01088", "gs005"], cibles=["gs032"]),
    _c("gs237 Touched sur un ALLIE : Rogue +2 ATQ (2 -> 4)",
       "« Ally, Rogue gets +2 ATK »",
       [HEROS, "Puzzle.PutIntoPlay('gs032')", *en_jeu("40204")], ["Puzzle.AttachReel('gs237', '40204')"],
       {"attrs": [["gs032", "attack", 4], ["gs032", "retaliate", 0]]}, main_exclusive=["01090"]),
    _c("gs237 Touched sur l'IDENTITE : Rogue gagne Vilenie",
       "« Identity, Rogue gains villainous »",
       [HEROS, "Puzzle.PutIntoPlay('gs032')"], ["Puzzle.AttachReel('gs237', 'gs001a')"],
       {"attrs": [["gs032", "villainous", 1], ["gs032", "attack", 2]]}, main_exclusive=["01090"]),
    # ============================================================ gs239 Goin' Rogue
    _c("gs239 Goin' Rogue : Touched sur un personnage AMICAL (Binary) : Rogue +1 MNG",
       "« While Touched is attached to a friendly character, Rogue gets +1 SCH »",
       [HEROS, "Puzzle.PutIntoPlay('gs032')", "Puzzle.PutIntoPlay('gs239')"],
       ["Puzzle.AttachReel('gs237', 'gs001a')"],
       {"attrs": [["gs032", "scheme", 3], ["gs032", "attack", 2]]}, main_exclusive=["01090"]),
    _c("gs239 Goin' Rogue : Touched sur un ENNEMI (Rhino) : Rogue +1 ATQ",
       "« While Touched is attached to an enemy character, Rogue gets +1 ATK »",
       [HEROS, "Puzzle.PutIntoPlay('gs032')", "Puzzle.PutIntoPlay('gs239')"],
       ["Puzzle.AttachReel('gs237', '01094')"],
       {"attrs": [["gs032", "scheme", 2], ["gs032", "attack", 3]]}, main_exclusive=["01090"]),
    _c("gs239 Goin' Rogue : valeurs imprimees, menace de depart 2 (1 joueur), icone Hazard",
       "« 2 [par joueur] » et l'icone Hazard (desc, base automatique)",
       [HEROS, "Puzzle.PutIntoPlay('gs239')"], [],
       {"menace": [["gs239", 2]], "icones": [["Hazard", 1]]}, main_exclusive=["01090"]),
    # ============================================================ gs240 Energy Transfer
    _c("gs240 Energy Transfer : l'Energy de la main est defaussee, pas de degat",
       "« Discard each [energy] resource from your hand. If no card was discarded this way, take 3 damage »",
       [HEROS], [VIDER_DEFAUSSE, "Puzzle.Reveal('gs240')"],
       {"main_ids": ["01090"], "defausse_avec": ["01088"], "degats_identite": 0},
       main_exclusive=["01088", "01090"]),
    _c("gs240 Energy Transfer : aucune [energy] en main -> 3 degats, rien defausse",
       "branche « If no card was discarded this way »",
       [HEROS], [VIDER_DEFAUSSE, "Puzzle.Reveal('gs240')"],
       {"main_ids": ["01090"], "degats_identite": 3}, main_exclusive=["01090"]),
    _c("gs240 Energy Transfer + Energy Conversion : Strength comptee [energy], defaussee, pas de degat",
       "« [energy] resource from your HAND » : lue apres la conversion",
       [HEROS, *en_jeu("gs010")], [VIDER_DEFAUSSE, "Puzzle.Reveal('gs240')"],
       {"main_ids": [], "defausse_avec": ["01090"], "degats_identite": 0}, main_exclusive=["01090"]),
]

VERIFICATIONS = r'''
CLES_BINARY = {'main_ids', 'attrs', 'defausse_avec', 'defausse_sans', 'dessus_deck', 'porteur_touched', 'retiree'}


def bn_etat(monde, aides):
    """etat_attendu + cles propres : main_ids (ensemble exact de la main), attrs [[card_id, attribut, valeur]],
    defausse_avec / defausse_sans (card_id presents / absents de la defausse du joueur), dessus_deck (card_id
    du dessus du deck), porteur_touched (card_id du personnage qui porte Touched gs237, ou None),
    retiree (card_id dans la zone des cartes retirees du jeu)."""
    cas = aides["cas"]
    attendu = dict(cas.get("attendu") or {})
    propres = {k: attendu.pop(k) for k in list(attendu) if k in CLES_BINARY}
    j = monde.players[0]
    soucis = []
    if "main_ids" in propres:
        vu = sorted(getattr(f.paper, "card_id", "?") for f in j.hand_cards.GetAll())
        if vu != sorted(propres["main_ids"]):
            soucis.append(f"main = {vu} (attendu {sorted(propres['main_ids'])})")
    pile = [getattr(f.paper, "card_id", "?") for f in j.discard_pile.Get()]
    for cid in propres.get("defausse_avec") or []:
        if cid not in pile:
            soucis.append(f"{cid} absent de la defausse (defausse = {pile})")
    for cid in propres.get("defausse_sans") or []:
        if cid in pile:
            soucis.append(f"{cid} present dans la defausse (defausse = {pile})")
    if "dessus_deck" in propres:
        dessus = j.player_deck.Get(True)
        vu = getattr(dessus[0].paper, "card_id", None) if dessus else None
        if vu != propres["dessus_deck"]:
            soucis.append(f"dessus du deck = {vu} (attendu {propres['dessus_deck']})")
    if "porteur_touched" in propres:
        porteur = None
        for objet in monde.object_manager.card_dict.values():
            face = objet.face
            if face is not None and face.IsInPlay() and getattr(face.paper, "card_id", None) == "gs237":
                hote = getattr(face, "bind_face", None)
                porteur = getattr(getattr(hote, "paper", None), "card_id", None)
        if porteur != propres["porteur_touched"]:
            soucis.append(f"Touched portee par {porteur} (attendu {propres['porteur_touched']})")
    for cid in propres.get("retiree") or []:
        retirees = [getattr(f.paper, "card_id", None) for f in monde.area_removed.GetAll()]
        if cid not in retirees:
            soucis.append(f"{cid} n'est pas retiree du jeu (retirees = {retirees})")
    for cid, attr, voulu in propres.get("attrs") or []:
        face = aides["par_id"](monde, cid)
        if face is None:
            soucis.append(f"{cid} introuvable en jeu (attrs)")
        elif getattr(face, attr) != voulu:
            soucis.append(f"{cid}.{attr} = {getattr(face, attr)} (attendu {voulu})")
    sauvegarde = cas["attendu"]
    cas["attendu"] = attendu
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = sauvegarde
    if not ok:
        soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, msg


def bn_fin_de_tour(monde, aides):
    """Envoie « apres la fin du tour du joueur » (`AfterPlayerTurnEnd`, modele gorr_berserker_fin_de_tour)."""
    from game.message import Message
    joueur = monde.players[0]
    fin = Message.WhenPlayerTurnEnd(joueur, 1)
    Message.AfterPlayerTurnEnd(joueur, fin).Send()
    return bn_etat(monde, aides)


def bn_debut_phase(monde, aides):
    """Ouvre la phase des joueurs comme `phase_begin` (world.py) : WhenPhaseBegin puis AfterPhaseBegin."""
    from game.message import Message
    debut = Message.WhenPhaseBegin("Player", monde)
    debut.Send()
    Message.AfterPhaseBegin(debut).Send()
    return bn_etat(monde, aides)


def bn_fin_de_round(monde, aides):
    """Joue la defausse de fin de round du moteur (`ProcessTemporary`) puis bn_etat."""
    from game.effect.rule import GameRule
    monde.ProcessTemporary(GameRule(monde.const_players[0].GetIdentity()))
    return bn_etat(monde, aides)
'''
