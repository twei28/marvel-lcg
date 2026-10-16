# Cas test_capacites du heros JENNIKA (TMNT Heroes v3, Inkwire, prefixe `tj`).
# Format identique a tools/test_capacites.py ; noms prefixes `[jennika]` (filtre : `[jennika]`),
# un `card_id` sujet dans chaque nom (substituer_pack.py filtre dessus).
#
# Decisions de l'utilisateur appliquees (.planning/tmnt/decisions-phase-b.md) :
#  - « Cloak X » = poser la carte d'etat Cloaked sur X (Moonlighting, Phantasm, Street Phantoms) ;
#  - vrai octroi d'aptitude pour les armes jumelles (Tekko-Kagi, comme Katana / Nunchuck) ;
#  - inserts de regles : aucune carte creee (le dos « Sosaiken Cardback » n'est pas une carte jouable).
# Lectures provisoires (TODO-QUESTION) : .planning/tmnt/jennika-questions.md.
#
# Conventions :
#  - Jennika demarre en ALTER EGO (tj001b, Jenny) ; HEROS la met en forme heros (tj001a) ;
#  - la VRAIE mise en place tourne : la Voie tj011 (mise de cote) est en jeu des le depart ; sa Reponse
#    (« After you play a Shinobi card ... draw 1 card ») peut donc piocher dans un cas qui joue une carte
#    Shinobi : les cas qui comptent la main l'excluent explicitement ;
#  - `main_exclusive` vide la main (APRES `mise_en_place`) : chaque cas sait avec QUOI il paie
#    (01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR) ;
#  - ordre du pilote : mise_en_place, main_exclusive, declencher, jouer, declencher_apres ;
#  - Rhino 01094 est le vilain (complot principal 01097b), 01101 Hydra Mercenary (3 PV) le sbire de mesure.
SC = "rhino"
HEROS = "Puzzle.ChangeToFace('tj001b', 'tj001a')"
CIVIL = "Puzzle.ChangeToFace('tj001a', 'tj001b')"
COMPLOT = "01097b"
# Deck rencontre bourre de « I'm Tough » (01105, sans icone ni effet de boost) : les attaques de Rhino n'ont
# AUCUN boost, la mesure des degats est exacte.
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01105', '01105', '01105', '01105', '01105', '01105', '01105', '01105')"]
BONUS_SENPAI = {"attack": 1, "thwart": 1, "defense": 1}
AUCUN_BONUS = {"attack": 0, "thwart": 0, "defense": 0}


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    if not cle.pop("avec_boost", False):
        mise = SANS_BOOST + list(mise)
    cas = {"nom": "[jennika] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "jennika"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ===================================================================== tj001a Ninja Senpai
    _c("tj001a Ninja Senpai : jouer une carte NINJUTSU (Moonlighting) donne +1 CTR / ATQ / DEF a Jennika",
       "« When you play a Shinobi card, Jennika gets +1 THW, +1 ATK and +1 DEF until the end of the round » : "
       "Moonlighting (Hero Action, classe Ninjutsu, cout 0) jouee en forme heros ; l'Interrupt part avant la resolution",
       [HEROS], [], {"attributs": BONUS_SENPAI, "defausse": ["tj005"], "statuts": [["tj001a", "Cloaked"]]},
       main_exclusive=["tj005"], jouer=["tj005"]),
    _c("tj001a Ninja Senpai : jouer une carte TAIJUTSU (Decisive Strike) donne le meme bonus",
       "Decisive Strike (classe Taijutsu, cout 2, payee par Energy YY) : +1/+1/+1 ; ses 3 degats frappent Rhino",
       [HEROS], [], {"attributs": BONUS_SENPAI, "defausse": ["tj004"], "degats": [["01094", 3]]},
       main_exclusive=["tj004", "01088"], payer_avec=["01088"], jouer=["tj004"], cibles=["01094"]),
    _c("tj001a Ninja Senpai : jouer une carte KUJI-KIRI (Apparition) donne le meme bonus",
       "Apparition (classe Kuji-Kiri, cout 2, payee par Energy YY) : +1/+1/+1 ; menace 5 -> 3 sur le principal",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"attributs": BONUS_SENPAI, "defausse": ["tj003"], "menace": [[COMPLOT, 3]]},
       main_exclusive=["tj003", "01088"], payer_avec=["01088"], jouer=["tj003"], cibles=[COMPLOT, "01094"]),
    _c("tj001a Ninja Senpai : jouer une carte BUSHIDO (Fearless Resolve, une amelioration) donne le meme bonus",
       "Fearless Resolve (classe Bushido, cout 1, payee par Strength RR) : le declencheur couvre aussi les ameliorations",
       [HEROS], [], {"attributs": BONUS_SENPAI, "en_jeu": ["tj006"]},
       main_exclusive=["tj006", "01090"], payer_avec=["01090"], jouer=["tj006"]),
    _c("tj001a Ninja Senpai : TEMOIN D'EPUISEMENT, deux NINJUTSU dans le meme round -> un seul bonus (+1, pas +2)",
       "« Limit once per round for each Shinobi » : Moonlighting x2 (meme classe) ; la 2e jouee ne redonne rien : "
       "ATQ +1 et non +2 (les deux ont bien ete jouees : plus aucune Moonlighting en main)",
       [HEROS], [], {"attributs": BONUS_SENPAI, "defausse": ["tj005"], "absent_main": ["tj005"]},
       main_exclusive=["tj005", "tj005"], jouer=["tj005", "tj005"]),
    _c("tj001a Ninja Senpai : deux Shinobi DIFFERENTS (Ninjutsu puis Bushido) -> le bonus s'ajoute (+2)",
       "la limite est PAR classe : Moonlighting (Ninjutsu) puis Fearless Resolve (Bushido) donnent chacune +1 : +2/+2/+2",
       [HEROS], [], {"attributs": {"attack": 2, "thwart": 2, "defense": 2}, "en_jeu": ["tj006"], "defausse": ["tj005"]},
       main_exclusive=["tj005", "tj006", "01090"], payer_avec=["01090"], jouer=["tj005", "tj006"]),
    _c("tj001a Ninja Senpai : TEMOIN, Composure (aucune classe Shinobi) ne declenche RIEN",
       "Composure ne porte pas de classe Shinobi : jouee en forme heros, aucun bonus (+0/+0/+0) ; la carte choisie "
       "dans la defausse est bien revenue en main",
       [HEROS, "Puzzle.CreatePlayerDiscardPile('01090')"], [],
       {"attributs": AUCUN_BONUS, "defausse": ["tj002"], "en_main": ["01090"]},
       main_exclusive=["tj002", "01088"], payer_avec=["01088"], jouer=["tj002"], cibles=["01090"]),
    _c("tj001a Ninja Senpai : « Jennika gets » ne vaut qu'en forme HEROS (carte jouee en alter ego, puis passage en heros : +0)",
       "en alter ego la face heros n'est pas en jeu : Fearless Resolve jouee en forme Jenny ne donne rien, et le "
       "passage en forme heros ensuite n'ajoute aucun bonus retroactif",
       [], [], {"attributs": AUCUN_BONUS, "en_jeu": ["tj006"]},
       main_exclusive=["tj006", "01090"], payer_avec=["01090"], jouer=["tj006"],
       declencher_apres=[HEROS]),
    _c("tj001a Ninja Senpai : le bonus dure jusqu'a la FIN DU ROUND puis disparait",
       "Moonlighting jouee (+1/+1/+1) ; apres l'envoi de la fin de round (WhenRoundEnd + buff_manager), +0/+0/+0",
       [HEROS], [], {"attributs": AUCUN_BONUS, "defausse": ["tj005"]},
       main_exclusive=["tj005"], jouer=["tj005"], verifier="jennika_apres_fin_de_round"),
    _c("tj001a Ninja Senpai : la limite est PAR Shinobi (4 capacites, une seule verrouillee apres une Ninjutsu) et se RENOUVELLE a la fin du round",
       "Moonlighting (Ninjutsu) jouee : sur les 4 capacites de Ninja Senpai (une par classe), exactement UNE est verrouillee pour le round ; "
       "apres la fin du round (WhenRoundEnd + buff_manager), aucune ne l'est plus",
       [HEROS], [], {"defausse": ["tj005"]},
       main_exclusive=["tj005"], jouer=["tj005"], verifier="jennika_limite_renouvelee"),
    _c("tj001a Jennika / tj001b Jenny : statistiques imprimees (ATQ 1, CTR 1, DEF 2, PV 12, main 4 / REC 3, PV 12, main 5)",
       "valeurs du scan, lues sur la face en jeu : forme heros puis forme alter ego",
       [HEROS], [], {"valeurs": {"tj001a": {"attack": 1, "thwart": 1, "defense": 2, "max_health": 12, "hand_size": 4}}},
       verifier="jennika_desc"),
    _c("tj001b Jenny : statistiques imprimees de l'alter ego (REC 3, PV 12, main 5)",
       "valeurs du scan", [], [], {"valeurs": {"tj001b": {"recover": 3, "max_health": 12, "hand_size": 5}}},
       verifier="jennika_desc"),

    # ===================================================================== tj001b Jenny
    _c("tj001b Jenny Setup : la VRAIE mise en place met la Voie tj011 en jeu (mise de cote, hors du deck et de la main)",
       "« Setup: Put the Sosaiken Path into play under your control » : BeginGameWithSetAside fabrique tj011, le Setup la "
       "met en jeu ; la main de depart n'est pas amputee (5 = taille de main de Jenny)",
       [], [], {"en_jeu": ["tj011"], "taille_main": 5, "forme": "AlterEgo"}, verifier="jennika_voie"),
    _c("tj001b Jenny Setup : la Voie est sous le CONTROLE du joueur, en un SEUL exemplaire (aucun doublon dans le deck)",
       "« under your control » : le joueur la controle ; mise en place normale, tj011 n'existe qu'une fois dans la partie",
       [], [], {"en_jeu": ["tj011"], "exemplaires": {"tj011": 1}}, verifier="jennika_voie"),
    _c("tj001b Jenny Action : defausse 1 carte, met en jeu 2 Tekko-Kagi (deck + defausse), inclinees",
       "« Discard 1 card from your hand -> search deck and discard pile for up to 2 TEKKO-KAGI upgrades, put them into play "
       "exhausted » : tj009 dans le deck, tj010 dans la defausse, main = 01088",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', 'tj009', '01074')",
        "Puzzle.CreatePlayerDiscardPile('tj010')"], ["Puzzle.Action('tj001b', 'Action', 0)"],
       {"en_jeu": ["tj009", "tj010"], "exhausted": ["tj009", "tj010"], "defausse": ["01088"], "taille_deck_joueur": 2},
       main_exclusive=["01088"], accepter_choix=True),
    _c("tj001b Jenny Action : « up to 2 » : UNE seule Tekko-Kagi disponible (deck), une seule mise en jeu",
       "jusqu'a 2 : une seule trouvee, l'autre absente ; le cout (defausse) est paye quand meme",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', 'tj009', '01074')"],
       ["Puzzle.Action('tj001b', 'Action', 0)"],
       {"en_jeu": ["tj009"], "hors_jeu": ["tj010"], "exhausted": ["tj009"], "defausse": ["01088"]},
       main_exclusive=["01088"], accepter_choix=True),
    _c("tj001b Jenny Action : aucune Tekko-Kagi a trouver : rien en jeu, mais la carte est bien defaussee",
       "0 Tekko-Kagi dans le deck et la defausse : la recherche ne ramene rien",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', '01074')"],
       ["Puzzle.Action('tj001b', 'Action', 0)"],
       {"hors_jeu": ["tj009", "tj010"], "defausse": ["01088"], "taille_deck_joueur": 2},
       main_exclusive=["01088"], accepter_choix=True),
    _c("tj001b Jenny Action : seules des TEKKO-KAGI sont cherchees (une amelioration ordinaire du deck reste dans le deck)",
       "« TEKKO-KAGI upgrades » : trait ET type ; Fearless Resolve (amelioration sans le trait) n'est jamais mise en jeu",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('tj006', 'tj009', 'tj006')"],
       ["Puzzle.Action('tj001b', 'Action', 0)"],
       {"en_jeu": ["tj009"], "hors_jeu": ["tj006"], "taille_deck_joueur": 2},
       main_exclusive=["01088"], accepter_choix=True),
    _c("tj001b Jenny Action : TEMOIN, main vide : l'Action n'est pas proposee (le cout de defausse est impayable)",
       "« Discard 1 card from your hand -> » : sans carte en main, aucune action disponible",
       ["Puzzle.EmptyHand()", "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01073', 'tj009', '01074')"],
       [], {"carte": "tj001b", "type": "Action", "nombre": 0}, verifier="jennika_actions_disponibles"),

    # ===================================================================== tj002 Composure
    _c("tj002 Composure : une carte CHOISIE de la defausse revient en main (forme alter ego), les autres restent",
       "« Action: Choose a card in your discard pile -> add that card to your hand » : defausse = 01090 + 01089, on "
       "designe 01089 ; payee par Energy YY (cout 1) ; « Action » (sans Hero) : jouable en alter ego",
       ["Puzzle.CreatePlayerDiscardPile('01090', '01089')"], [],
       {"en_main": ["01089"], "defausse": ["tj002", "01090"], "forme": "AlterEgo"},
       main_exclusive=["tj002", "01088"], payer_avec=["01088"], jouer=["tj002"], cibles=["01089"]),
    _c("tj002 Composure : meme effet en forme HEROS",
       "« Action » civil OU heros : en forme heros aussi, la carte choisie (01090) revient en main",
       [HEROS, "Puzzle.CreatePlayerDiscardPile('01090', '01089')"], [],
       {"en_main": ["01090"], "defausse": ["tj002", "01089"], "forme": "Hero"},
       main_exclusive=["tj002", "01088"], payer_avec=["01088"], jouer=["tj002"], cibles=["01090"]),
    _c("tj002 Composure : tout TYPE de carte se reprend (un evenement de la defausse, ici Moonlighting)",
       "« a card » sans restriction : un evenement ; Composure elle-meme n'est pas encore en defausse pendant le choix",
       ["Puzzle.CreatePlayerDiscardPile('tj005')"], [],
       {"en_main": ["tj005"], "defausse": ["tj002"]},
       main_exclusive=["tj002", "01088"], payer_avec=["01088"], jouer=["tj002"], cibles=["tj005"]),

    # ===================================================================== tj003 Apparition
    _c("tj003 Apparition : retire 2 menaces du complot PRINCIPAL ET desoriente un ennemi (Rhino)",
       "« Remove 2 threat from a scheme and confuse an enemy » : principal 5 -> 3, Rhino desoriente ; Apparition payee "
       "par Energy YY (cout 2)",
       [f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"menace": [[COMPLOT, 3]], "statuts": [["01094", "Confused"]], "defausse": ["tj003"]},
       main_exclusive=["tj003", "01088"], payer_avec=["01088"], jouer=["tj003"], cibles=[COMPLOT, "01094"]),
    _c("tj003 Apparition : « a scheme » est AU CHOIX : une manigance ANNEXE (01107) et un SBIRE (01101)",
       "annexe 4 -> 2 (le principal garde ses 5) ; le sbire 01101 est desoriente (pas Rhino)",
       ["Puzzle.PutIntoPlay('01107')", "Puzzle.SetThreat('01107', 4)", f"Puzzle.SetThreat('{COMPLOT}', 5)",
        "Puzzle.PutIntoPlay('01101')"], [],
       {"menace": [["01107", 2], [COMPLOT, 5]], "statuts": [["01101", "Confused"]],
        "statuts_absents": [["01094", "Confused"]]},
       main_exclusive=["tj003", "01088"], payer_avec=["01088"], jouer=["tj003"], cibles=["01107", "01101"]),
    _c("tj003 Apparition : CRISE active -> le principal n'est pas une cible de contre, la menace de l'annexe Crise baisse",
       "« (thwart) » : une Crise (01108) interdit de retirer de la menace du principal ; seule 01108 est legale : "
       "3 -> 1, le principal garde ses 5 ; Rhino est desoriente quand meme",
       ["Puzzle.PutIntoPlay('01108')", "Puzzle.SetThreat('01108', 3)", f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"menace": [["01108", 1], [COMPLOT, 5]], "statuts": [["01094", "Confused"]]},
       main_exclusive=["tj003", "01088"], payer_avec=["01088"], jouer=["tj003"], cibles=[COMPLOT, "01094"]),
    _c("tj003 Apparition : TEMOIN de la Crise : sans annexe Crise le principal est bien une cible (5 -> 3)",
       "meme montage sans 01108 : le contre vise le principal",
       [f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"menace": [[COMPLOT, 3]]},
       main_exclusive=["tj003", "01088"], payer_avec=["01088"], jouer=["tj003"], cibles=[COMPLOT, "01094"]),
    _c("tj003 Apparition : la menace restante est plafonnee a 0 (principal a 1 -> 0, pas de menace negative)",
       "« remove 2 threat » sur 1 menace : retire ce qui existe",
       [f"Puzzle.SetThreat('{COMPLOT}', 1)"], [],
       {"menace": [[COMPLOT, 0]], "statuts": [["01094", "Confused"]]},
       main_exclusive=["tj003", "01088"], payer_avec=["01088"], jouer=["tj003"], cibles=[COMPLOT, "01094"]),
    _c("tj003 Apparition : jouable en forme HEROS aussi (Action, pas Hero Action), meme effet",
       "« Action (thwart) » : forme heros, principal 5 -> 3 et Rhino desoriente",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 5)"], [],
       {"menace": [[COMPLOT, 3]], "statuts": [["01094", "Confused"]], "forme": "Hero"},
       main_exclusive=["tj003", "01088"], payer_avec=["01088"], jouer=["tj003"], cibles=[COMPLOT, "01094"]),

    # ===================================================================== tj004 Decisive Strike
    _c("tj004 Decisive Strike : 3 degats a Rhino, payee SANS evenement ATTACK (Strength RR) : pas d'etourdissement",
       "« Deal 3 damage to an enemy. If you paid with an ATTACK event, stun that enemy » : payee par une carte RESSOURCE "
       "(Strength) : 3 degats, Rhino non etourdi",
       [HEROS], [], {"degats": [["01094", 3]], "statuts_absents": [["01094", "Stunned"]], "defausse": ["tj004"]},
       main_exclusive=["tj004", "01090"], payer_avec=["01090"], jouer=["tj004"], cibles=["01094"]),
    _c("tj004 Decisive Strike : payee avec un evenement ATTACK (Haymaker 01087 + Energy) : Rhino est ETOURDI",
       "Haymaker (evenement, trait ATTACK) defausse pour sa ressource avec une carte Energy : Rhino prend 3 et est etourdi",
       [HEROS], [], {"degats": [["01094", 3]], "statuts": [["01094", "Stunned"]], "defausse": ["tj004", "01087"]},
       main_exclusive=["tj004", "01087", "01088"], payer_avec=["01087", "01088"], jouer=["tj004"], cibles=["01094"]),
    _c("tj004 Decisive Strike : payee avec un evenement NON-ATTACK (Backflip 01003, DEFENSE/SKILL) : pas d'etourdissement",
       "« with an ATTACK event » : un evenement d'un autre trait ne compte pas ; Backflip (R) + Energy (YY) paient le cout 2",
       [HEROS], [], {"degats": [["01094", 3]], "statuts_absents": [["01094", "Stunned"]], "defausse": ["tj004", "01003"]},
       main_exclusive=["tj004", "01003", "01088"], payer_avec=["01003", "01088"], jouer=["tj004"], cibles=["01094"]),
    _c("tj004 Decisive Strike : une AUTRE Decisive Strike (ATTACK) peut payer : etourdissement du sbire (3 degats le vainquent)",
       "la 2e copie est un evenement ATTACK : on la remplace par Repulsor Blast 01031 (ATTACK) ; sbire Hydra Mercenary 01101 "
       "(3 PV) : 3 degats = vaincu, plus d'etourdissement a poser (un ennemi vaincu n'est pas etourdi) ; Rhino reste net",
       [HEROS, "Puzzle.PutIntoPlay('01101')"], [],
       {"hors_jeu": ["01101"], "statuts_absents": [["01094", "Stunned"]], "defausse": ["tj004", "01031"]},
       main_exclusive=["tj004", "01031", "01088"], payer_avec=["01031", "01088"], jouer=["tj004"], cibles=["01101"]),
    _c("tj004 Decisive Strike : Hydra Mercenary (3 PV) bien frappe par Decisive Strike puis etourdi quand il survit (Toughness absente)",
       "cible Rhino (14 PV) : survit, etourdi s'il y a un ATTACK ; ici Repulsor Blast paie -> Stunned",
       [HEROS], [],
       {"degats": [["01094", 3]], "statuts": [["01094", "Stunned"]], "defausse": ["tj004", "01031"]},
       main_exclusive=["tj004", "01031", "01088"], payer_avec=["01031", "01088"], jouer=["tj004"], cibles=["01094"]),

    # ===================================================================== tj005 Moonlighting
    _c("tj005 Moonlighting : Cloak Jennika = carte d'etat Cloaked sur le HEROS (pas sur le vilain)",
       "« Hero Action: Cloak Jennika » : Cloaked sur tj001a, aucun sur Rhino ; cout 0",
       [HEROS], [], {"statuts": [["tj001a", "Cloaked"]], "statuts_absents": [["01094", "Cloaked"]], "defausse": ["tj005"]},
       main_exclusive=["tj005"], jouer=["tj005"]),
    _c("tj005 Moonlighting : la carte Cloaked sert vraiment : la prochaine ATTAQUE de Jennika a +2 (1 + 2 = 3 degats)",
       "Cloaked (cloaked.md) : +2 au prochain pouvoir de base ; Moonlighting jouee, puis attaque de base de Jennika "
       "(ATQ 1, +1 de Ninja Senpai, +2 de Cloaked) : 4 degats sur Rhino, et Cloaked est partie",
       [HEROS], [],
       {"degats": [["01094", 4]], "statuts_absents": [["tj001a", "Cloaked"]]},
       main_exclusive=["tj005"], jouer=["tj005"], declencher_apres=["Puzzle.Attack('tj001a')"]),
    _c("tj005 Moonlighting : deux Moonlighting = UN seul Cloaked (plafond d'une carte par personnage, encart Shredder, cloaked.md)",
       "deux exemplaires joues : le second ne pose rien (Jennika porte deja son Cloaked), l'attaque vaut ATQ 1 + 1 Senpai + 2 = 4 "
       "et le Cloaked part",
       [HEROS], [], {"degats": [["01094", 4]], "statuts_absents": [["tj001a", "Cloaked"]]},
       main_exclusive=["tj005", "tj005"], jouer=["tj005", "tj005"], declencher_apres=["Puzzle.Attack('tj001a')"]),

    # ===================================================================== tj006 Fearless Resolve
    _c("tj006 Fearless Resolve : entre en jeu avec 2 compteurs de samourai (Uses)",
       "« Uses (2 samurai counters) » : base native `desc.Uses = 2,samurai` ; le compteur est declare dans CardFace.COUNTER",
       [HEROS], [], {"compteurs": [["tj006", "samurai", 2]], "en_jeu": ["tj006"]},
       main_exclusive=["tj006", "01090"], payer_avec=["01090"], jouer=["tj006"]),
    _c("tj006 Fearless Resolve : Hero Action = incline, retire les 2 compteurs -> Jennika est REDRESSEE (la carte part ensuite)",
       "Jennika inclinee ; l'action coute l'inclinaison de la carte ET 2 compteurs : Jennika prete, tj006 defaussee (dernier "
       "compteur retire)",
       [HEROS, "Puzzle.PutIntoPlay('tj006', under_control=True)", "Puzzle.Exhaust('tj001a')"],
       ["Puzzle.Action('tj006', 'HeroAction', 0)"],
       {"pret": ["tj001a"], "hors_jeu": ["tj006"], "defausse": ["tj006"]}),
    _c("tj006 Fearless Resolve : TEMOIN, en forme d'ALTER EGO la Hero Action n'est pas proposee",
       "« Hero Action » : forme heros seulement",
       ["Puzzle.PutIntoPlay('tj006', under_control=True)"], [],
       {"carte": "tj006", "type": "HeroAction", "nombre": 0}, verifier="jennika_actions_disponibles"),
    _c("tj006 Fearless Resolve : TEMOIN, la carte DEJA inclinee n'offre pas l'action (cout d'inclinaison impayable)",
       "« Exhaust Fearless Resolve and ... » : une carte inclinee ne peut pas s'incliner",
       [HEROS, "Puzzle.PutIntoPlay('tj006', under_control=True, exhaust=True)"], [],
       {"carte": "tj006", "type": "HeroAction", "nombre": 0}, verifier="jennika_actions_disponibles"),
    _c("tj006 Fearless Resolve : TEMOIN, un seul compteur restant : l'action n'est pas proposee (il faut en retirer 2)",
       "« remove 2 samurai counters » : cout de deux compteurs ; avec 1 seul, impayable",
       [HEROS, "Puzzle.PutIntoPlay('tj006', under_control=True)", "Puzzle.Counter('tj006', 'samurai', -1)"], [],
       {"carte": "tj006", "type": "HeroAction", "nombre": 0}, verifier="jennika_actions_disponibles"),
    _c("tj006 Fearless Resolve : « ready JENNIKA » : le heros se redresse, un ALLIE incline reste incline",
       "l'effet vise Jennika uniquement : l'allie Hellcat (01020, inclinee) n'est pas redresse",
       [HEROS, "Puzzle.PutIntoPlay('tj006', under_control=True)", "Puzzle.PutIntoPlay('01020', under_control=True)",
        "Puzzle.Exhaust('tj001a')", "Puzzle.Exhaust('01020')"],
       ["Puzzle.Action('tj006', 'HeroAction', 0)"],
       {"pret": ["tj001a"], "exhausted": ["01020"]}),

    # ===================================================================== tj007 Jenny's Crib
    _c("tj007 Jenny's Crib : Action d'alter ego = incline la Crib + defausse 1 carte -> pioche 1 et REDRESSE l'identite",
       "Jenny inclinee, main = 01088 : apres l'action, 01088 en defausse, la carte du dessus du deck (01073) en main, Jenny "
       "prete, la Crib inclinee",
       ["Puzzle.PutIntoPlay('tj007', under_control=True)", "Puzzle.EmptyPlayerDeck()",
        "Puzzle.CreatePlayerDeck('01074', '01073')", "Puzzle.Exhaust('tj001b')"],
       ["Puzzle.Action('tj007', 'AlterEgoAction', 0)"],
       {"pret": ["tj001b"], "exhausted": ["tj007"], "defausse": ["01088"], "en_main": ["01073"], "taille_deck_joueur": 1},
       main_exclusive=["01088"], accepter_choix=True),
    _c("tj007 Jenny's Crib : TEMOIN, en forme HEROS l'Action d'alter ego n'est pas proposee",
       "« Alter-Ego Action »", [HEROS, "Puzzle.PutIntoPlay('tj007', under_control=True)"], [],
       {"carte": "tj007", "type": "AlterEgoAction", "nombre": 0}, verifier="jennika_actions_disponibles",
       main_exclusive=["01088"]),
    _c("tj007 Jenny's Crib : TEMOIN, main vide : l'action n'est pas proposee (cout de defausse impayable)",
       "« discard 1 card from your hand » : sans carte, impayable",
       ["Puzzle.PutIntoPlay('tj007', under_control=True)", "Puzzle.EmptyHand()"], [],
       {"carte": "tj007", "type": "AlterEgoAction", "nombre": 0}, verifier="jennika_actions_disponibles"),
    _c("tj007 Jenny's Crib : TEMOIN, Crib deja inclinee : l'action n'est pas proposee",
       "« Exhaust Jenny's Crib and ... »",
       ["Puzzle.PutIntoPlay('tj007', under_control=True, exhaust=True)"], [],
       {"carte": "tj007", "type": "AlterEgoAction", "nombre": 0}, verifier="jennika_actions_disponibles",
       main_exclusive=["01088"]),

    # ===================================================================== tj008 Jennika's Bow
    _c("tj008 Jennika's Bow : Hero Action, branche DEGATS : 1 degat a Rhino, l'arc s'incline",
       "« Exhaust the Bow -> deal 1 damage to an enemy OR remove 1 threat from a scheme » : on choisit les degats",
       [HEROS, "Puzzle.PutIntoPlay('tj008', under_control=True)", f"Puzzle.SetThreat('{COMPLOT}', 3)"],
       ["Puzzle.Action('tj008', 'HeroAction', 0)"],
       {"degats": [["01094", 1]], "menace": [[COMPLOT, 3]], "exhausted": ["tj008"]},
       choisir_option=["Deal_1_damage_to_an_enemy"], cibles=["01094"]),
    _c("tj008 Jennika's Bow : Hero Action, branche MENACE : 1 menace retiree du principal, aucun degat",
       "meme action, on choisit de retirer 1 menace : 3 -> 2, Rhino intact",
       [HEROS, "Puzzle.PutIntoPlay('tj008', under_control=True)", f"Puzzle.SetThreat('{COMPLOT}', 3)"],
       ["Puzzle.Action('tj008', 'HeroAction', 0)"],
       {"degats": [["01094", 0]], "menace": [[COMPLOT, 2]], "exhausted": ["tj008"]},
       choisir_option=["Remove_1_threat_from_a_scheme"], cibles=[COMPLOT]),
    _c("tj008 Jennika's Bow : TEMOIN, forme ALTER EGO : la Hero Action n'est pas proposee",
       "« Hero Action »", ["Puzzle.PutIntoPlay('tj008', under_control=True)"], [],
       {"carte": "tj008", "type": "HeroAction", "nombre": 0}, verifier="jennika_actions_disponibles"),
    _c("tj008 Jennika's Bow : Hero Response : apres un evenement ATTACK (Decisive Strike), l'arc inclinee est REDRESSE",
       "arc inclinee ; Decisive Strike (ATTACK) jouee, payee par Strength : l'arc est prete a la fin",
       [HEROS, "Puzzle.PutIntoPlay('tj008', under_control=True, exhaust=True)"], [],
       {"pret": ["tj008"], "defausse": ["tj004"]},
       main_exclusive=["tj004", "01090"], payer_avec=["01090"], jouer=["tj004"], cibles=["01094"]),
    _c("tj008 Jennika's Bow : Hero Response : apres un evenement THWART (Apparition), l'arc inclinee est REDRESSE",
       "Apparition (trait THWART) jouee : l'arc est prete a la fin",
       [HEROS, "Puzzle.PutIntoPlay('tj008', under_control=True, exhaust=True)", f"Puzzle.SetThreat('{COMPLOT}', 4)"], [],
       {"pret": ["tj008"], "defausse": ["tj003"]},
       main_exclusive=["tj003", "01088"], payer_avec=["01088"], jouer=["tj003"], cibles=[COMPLOT, "01094"]),
    _c("tj008 Jennika's Bow : TEMOIN, un evenement ni ATTACK ni THWART (Composure, SKILL) ne redresse PAS l'arc",
       "« an ATTACK or THWART event » : Composure n'a aucun des deux traits : l'arc reste inclinee",
       [HEROS, "Puzzle.PutIntoPlay('tj008', under_control=True, exhaust=True)", "Puzzle.CreatePlayerDiscardPile('01090')"], [],
       {"exhausted": ["tj008"], "defausse": ["tj002"]},
       main_exclusive=["tj002", "01088"], payer_avec=["01088"], jouer=["tj002"], cibles=["01090"]),
    _c("tj008 Jennika's Bow : TEMOIN, une carte qui n'est PAS un evenement (Fearless Resolve, amelioration) ne la redresse pas",
       "« event » : type Event seulement",
       [HEROS, "Puzzle.PutIntoPlay('tj008', under_control=True, exhaust=True)"], [],
       {"exhausted": ["tj008"], "en_jeu": ["tj006"]},
       main_exclusive=["tj006", "01090"], payer_avec=["01090"], jouer=["tj006"]),
    _c("tj008 Jennika's Bow : Restricted est lu dans le desc (base automatique, aucun script)",
       "desc.Restricted = 1 sur tj008 (fiche restricted.md) et sur AUCUNE autre amelioration du pack",
       [], [], {"restricted": {"tj008": True, "tj009": False, "tj010": False, "tj006": False}},
       verifier="jennika_desc"),

    # ===================================================================== tj009 Tekko-Kagi
    _c("tj009 Tekko-Kagi : l'octroi donne la ressource wild AUX DEUX Tekko-Kagi (tj009 + tj010 paient Decisive Strike cout 2)",
       "« Each TEKKO-KAGI upgrade you control gains Hero Resource ... for a Shinobi card » (vrai octroi) : deux Tekko-Kagi, "
       "Decisive Strike (Taijutsu, cout 2) payee uniquement par elles (main vide hors la carte jouee)",
       [HEROS, "Puzzle.PutIntoPlay('tj009', under_control=True)", "Puzzle.PutIntoPlay('tj010', under_control=True)"], [],
       {"defausse": ["tj004"], "exhausted": ["tj009", "tj010"]},
       main_exclusive=["tj004"], payer_avec=["tj009", "tj010"], jouer=["tj004"], cibles=["01094"]),
    _c("tj009 Tekko-Kagi : UNE seule Tekko-Kagi en jeu (tj009) : sa ressource wild paie Fearless Resolve (Bushido, cout 1)",
       "tj009 porte l'aptitude qu'elle octroie a elle-meme : seule en jeu, elle fonctionne",
       [HEROS, "Puzzle.PutIntoPlay('tj009', under_control=True)"], [],
       {"en_jeu": ["tj006"], "exhausted": ["tj009"]},
       main_exclusive=["tj006"], payer_avec=["tj009"], jouer=["tj006"]),
    _c("tj009 Tekko-Kagi : « for a SHINOBI card » : la ressource ne paie PAS Composure (aucune classe Shinobi)",
       "Composure (cout 1) ne peut pas etre payee par la Tekko-Kagi : elle reste en main, l'arme reste prete",
       [HEROS, "Puzzle.PutIntoPlay('tj009', under_control=True)", "Puzzle.CreatePlayerDiscardPile('01090')"], [],
       {"en_main": ["tj002"], "pret": ["tj009"]},
       main_exclusive=["tj002"], payer_avec=["tj009"], jouer=["tj002"], cibles=["01090"]),
    _c("tj009 Tekko-Kagi : la ressource ne paie pas non plus une carte d'ASPECT (01063 Justice)",
       "carte non Shinobi : refusee",
       [HEROS, "Puzzle.PutIntoPlay('tj009', under_control=True)"], [],
       {"en_main": ["01063"], "pret": ["tj009"]},
       main_exclusive=["01063"], payer_avec=["tj009"], jouer=["01063"]),
    _c("tj009 Tekko-Kagi : Hero Resource INUTILISABLE en alter ego (Fearless Resolve reste en main)",
       "« Hero Resource » : forme heros seulement",
       ["Puzzle.PutIntoPlay('tj009', under_control=True)"], [],
       {"en_main": ["tj006"], "pret": ["tj009"]},
       main_exclusive=["tj006"], payer_avec=["tj009"], jouer=["tj006"]),
    _c("tj009 Tekko-Kagi : l'octroi cesse quand tj009 quitte le jeu : tj010 reste en jeu SANS ressource",
       "« gains » : l'aptitude n'existe que tant que la donneuse est en jeu ; apres defausse de tj009, tj010 : 0 ressource octroyee",
       [HEROS, "Puzzle.PutIntoPlay('tj009', under_control=True)", "Puzzle.PutIntoPlay('tj010', under_control=True)"],
       ["Puzzle.Discard('tj009')"], {"tj010": {"ressource": 0}, "tj009": None},
       verifier="jennika_octrois"),
    _c("tj009 Tekko-Kagi : TEMOIN POSITIF, deux Tekko-Kagi en jeu : chacune porte exactement UNE ressource octroyee",
       "effets distincts par porteur",
       [HEROS, "Puzzle.PutIntoPlay('tj009', under_control=True)", "Puzzle.PutIntoPlay('tj010', under_control=True)"], [],
       {"tj009": {"ressource": 1, "interruption": 1}, "tj010": {"ressource": 1, "interruption": 1},
        "effets_distincts": True},
       verifier="jennika_octrois"),
    _c("tj009 Tekko-Kagi : « you control » : la Tekko-Kagi d'un AUTRE joueur ne recoit pas la ressource",
       "2 joueurs : tj009 chez le joueur 1, tj010 chez le joueur 2 : `control_by=\"You\"` : la ressource de tj009 ne va qu'aux Tekko-Kagi "
       "du joueur 1 (tj010 : 0 ressource) et l'interruption de tj010 ne va qu'a celles du joueur 2 (tj009 : 0 interruption, tj010 : 1)",
       [HEROS, "Puzzle.PutIntoPlay('tj009', under_control=True)",
        "Puzzle.PutIntoPlay('tj010', under_control=True, player=1)"], [],
       {"tj009": {"ressource": 1, "interruption": 0}, "tj010": {"ressource": 0, "interruption": 1}},
       verifier="jennika_octrois",
       heros2="spider_man"),

    # ===================================================================== tj010 Other Tekko-Kagi
    _c("tj010 Other Tekko-Kagi : Hero Interrupt a l'attaque de base : incline + defausse 1 carte -> +2 ATQ ET PERCANT (Rhino Tenace)",
       "ATQ 1 + 2 = 3 degats ; l'attaque gagne Perçant : Rhino Tenace PREND les 3 degats et perd son statut (sans Perçant, "
       "Tenace absorberait tout) ; la Tekko-Kagi est inclinee, 01088 defaussee",
       [HEROS, "Puzzle.PutIntoPlay('tj010', under_control=True)", "Puzzle.Tough('01094')"], ["Puzzle.Attack('tj001a')"],
       {"degats": [["01094", 3]], "statuts_absents": [["01094", "Tough"]], "exhausted": ["tj010"], "defausse": ["01088"]},
       main_exclusive=["01088"], accepter_choix=True),
    _c("tj010 Other Tekko-Kagi : TEMOIN, SANS l'arme : la meme attaque (Rhino Tenace) ne fait AUCUN degat et ne retire que Tenace",
       "ligne de base : ATQ 1 contre Tenace -> 0 degat, statut retire",
       [HEROS, "Puzzle.Tough('01094')"], ["Puzzle.Attack('tj001a')"],
       {"degats": [["01094", 0]], "statuts_absents": [["01094", "Tough"]]}, main_exclusive=["01088"]),
    _c("tj010 Other Tekko-Kagi : l'octroi touche aussi tj009 (« each TEKKO-KAGI upgrade you control gains ») : tj009 porte l'interruption",
       "tj010 en jeu donne l'Hero Interrupt a tj009 : elle seule s'incline et s'applique (tj010 absente de la liste des armes pretes)",
       [HEROS, "Puzzle.PutIntoPlay('tj009', under_control=True)", "Puzzle.PutIntoPlay('tj010', under_control=True)",
        "Puzzle.Exhaust('tj010')"],
       ["Puzzle.Attack('tj001a')"],
       {"degats": [["01094", 3]], "exhausted": ["tj009", "tj010"]}, main_exclusive=["01088"], accepter_choix=True),
    _c("tj010 Other Tekko-Kagi : TEMOIN, main vide : le cout de defausse est impayable, pas d'interruption (1 degat)",
       "« discard 1 card from your hand » : sans carte, l'arme ne s'incline pas et l'attaque reste a ATQ 1",
       [HEROS, "Puzzle.PutIntoPlay('tj010', under_control=True)", "Puzzle.EmptyHand()"], ["Puzzle.Attack('tj001a')"],
       {"degats": [["01094", 1]], "pret": ["tj010"]}),
    _c("tj010 Other Tekko-Kagi : TEMOIN, arme deja inclinee : pas d'interruption (1 degat)",
       "« exhaust this card » : une arme inclinee ne peut pas servir",
       [HEROS, "Puzzle.PutIntoPlay('tj010', under_control=True, exhaust=True)"], ["Puzzle.Attack('tj001a')"],
       {"degats": [["01094", 1]], "exhausted": ["tj010"], "defausse": []}, main_exclusive=["01088"]),
    _c("tj010 Other Tekko-Kagi : « basic attack » : une attaque d'EVENEMENT (Haymaker, 3 degats) ne declenche PAS l'interruption",
       "Haymaker (Hero Action (attack), pas une attaque de base) : 3 degats exactement, l'arme reste prete",
       [HEROS, "Puzzle.PutIntoPlay('tj010', under_control=True)"], [],
       {"degats": [["01094", 3]], "pret": ["tj010"], "defausse": ["01087"]},
       main_exclusive=["01087", "01088", "01089"], payer_avec=["01088"], jouer=["01087"], cibles=["01094"]),
    # ===================================================================== tj011 Sosaiken (la Voie)
    _c("tj011 Sosaiken : Reponse apres une carte NINJUTSU (Moonlighting) : incline la Voie -> pioche 1 carte",
       "deck = 01073 (dessus) ; Moonlighting jouee, main vide : la Voie s'incline, 01073 arrive en main",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01074', '01073')"], [],
       {"exhausted": ["tj011"], "en_main": ["01073"], "taille_deck_joueur": 1},
       main_exclusive=["tj005"], jouer=["tj005"], accepter_choix=True),
    _c("tj011 Sosaiken : Reponse apres une carte BUSHIDO (amelioration) : pioche 1 aussi (« a Shinobi card », pas seulement les evenements)",
       "Fearless Resolve jouee (Strength RR) : la Voie s'incline et pioche 01073",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01074', '01073')"], [],
       {"exhausted": ["tj011"], "en_main": ["01073"]},
       main_exclusive=["tj006", "01090"], payer_avec=["01090"], jouer=["tj006"], accepter_choix=True),
    _c("tj011 Sosaiken : Reponse en forme ALTER EGO aussi (« Response », sans Hero) : Fearless Resolve jouee en alter ego pioche",
       "Support : la Reponse tient dans les deux formes",
       ["Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01074', '01073')"], [],
       {"exhausted": ["tj011"], "en_main": ["01073"], "forme": "AlterEgo"},
       main_exclusive=["tj006", "01090"], payer_avec=["01090"], jouer=["tj006"], accepter_choix=True),
    _c("tj011 Sosaiken : TEMOIN, une carte NON Shinobi (Composure) ne declenche pas la Reponse (aucune pioche)",
       "deck = 01073 : Composure jouee, la Voie reste prete, 01073 reste dans le deck",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01074', '01073')",
        "Puzzle.CreatePlayerDiscardPile('01090')"], [],
       {"pret": ["tj011"], "taille_deck_joueur": 2, "en_main": ["01090"]},
       main_exclusive=["tj002", "01088"], payer_avec=["01088"], jouer=["tj002"], cibles=["01090"]),
    _c("tj011 Sosaiken : TEMOIN D'EPUISEMENT, la Voie deja inclinee : 2e carte Shinobi, aucune 2e pioche",
       "Moonlighting x2 (Ninjutsu) puis... la limite de Senpai n'est pas la Voie ; la Voie s'incline a la 1re et ne repioche pas "
       "a la 2e : une seule pioche (le deck passe de 3 a 2)",
       [HEROS, "Puzzle.EmptyPlayerDeck()", "Puzzle.CreatePlayerDeck('01074', '01073', '01075')"], [],
       {"exhausted": ["tj011"], "taille_deck_joueur": 2},
       main_exclusive=["tj005", "tj005"], jouer=["tj005", "tj005"], accepter_choix=True),
    _c("tj011 Sosaiken : TYPE PATH (la Voie) : la face en jeu est un Path, PAS un Support, rangee dans l'aire de soutien",
       "type imprime PATH (decision du 16/10/2026) : `Path.IsType` vrai, `Support.IsType` faux, un effet qui vise « Support » "
       "(Worlds.GetOnFieldSupports, GetControlCardsByType(support=True)) ne la voit pas, mais elle reste une carte en jeu du joueur",
       [], [], {}, verifier="jennika_voie_type"),
    _c("tj011 Sosaiken : PERMANENT protege la Voie : un effet d'un AUTRE set (Rhino) ne peut pas la retirer du jeu",
       "« Permanent » (permanent.md) : une GameRule portee par Rhino 01094 tente RemoveAllFromGame sur la Voie ; "
       "elle reste en jeu, dans l'aire de soutien",
       [], [], {}, verifier="jennika_voie_permanente"),
    _c("tj011 Sosaiken : PERMANENT : le moteur la tient pour Permanent (desc), classe Hero, type Path, sans cout",
       "« Permanent » est une base automatique (permanent.md) : aucun script ; on lit l'indicateur du moteur sur la face en jeu",
       [], [], {"permanent": {"tj011": True}}, verifier="jennika_desc"),

    # ===================================================================== tj012 Personality Adjustment
    _c("tj012 Personality Adjustment : donnee a Jenny (alter ego), branche 1 : incline Jenny -> l'obligation est RETIREE DU JEU",
       "« You may flip... Choose: Exhaust Jenny -> remove from the game » : forme alter ego, on choisit l'option 1 : "
       "Jenny inclinee, obligation retiree de la PARTIE (pas defaussee)",
       [f"Puzzle.SetThreat('{COMPLOT}', 1)"], ["Puzzle.Reveal('tj012')"],
       {"carte": "tj012", "exhausted": ["tj001b"], "menace": [[COMPLOT, 1]], "forme": "AlterEgo"},
       verifier="jennika_retiree_du_jeu", preferer_option=["Exhaust_Jenny"]),
    _c("tj012 Personality Adjustment : branche 2 : 3 menaces sur le complot principal, l'obligation est DEFAUSSEE",
       "meme obligation, option 2 : principal 1 -> 4, Jenny reste prete, tj012 hors jeu (defaussee)",
       [f"Puzzle.SetThreat('{COMPLOT}', 1)"], ["Puzzle.Reveal('tj012')"],
       {"menace": [[COMPLOT, 4]], "pret": ["tj001b"], "hors_jeu": ["tj012"]},
       preferer_option=["Place_3_threat"]),
    _c("tj012 Personality Adjustment : donnee a Jennika en forme HEROS, bascule REFUSEE : l'option 1 (Exhaust Jenny) n'existe PAS, 3 menaces obligatoires",
       "« You MAY flip » refuse (Cancel) : Jennika reste en forme heros ; « Exhaust JENNY » exige l'alter ego, seule la 2e branche est "
       "legale : principal 1 -> 4, obligation defaussee, forme heros conservee",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 1)"], ["Puzzle.Reveal('tj012')"],
       {"menace": [[COMPLOT, 4]], "hors_jeu": ["tj012"], "forme": "Hero"},
       choisir_option=["Cancel"], preferer_option=["Exhaust_Jenny"]),
    _c("tj012 Personality Adjustment : « You MAY flip to alter-ego form » : accepte, Jennika passe en alter ego puis peut s'incliner (branche 1)",
       "en forme heros, on accepte de basculer : Jenny (alter ego) incline, l'obligation retiree du jeu",
       [HEROS, f"Puzzle.SetThreat('{COMPLOT}', 1)"], ["Puzzle.Reveal('tj012')"],
       {"carte": "tj012", "exhausted": ["tj001b"], "menace": [[COMPLOT, 1]], "forme": "AlterEgo"},
       verifier="jennika_retiree_du_jeu", preferer_option=["Change", "Flip", "Exhaust_Jenny"], accepter_choix=True),
    _c("tj012 Personality Adjustment : Jenny DEJA inclinee : branche 1 impossible (cout), 3 menaces",
       "le cout d'inclinaison est impayable : seule la branche 2 est legale",
       [f"Puzzle.SetThreat('{COMPLOT}', 1)", "Puzzle.Exhaust('tj001b')"], ["Puzzle.Reveal('tj012')"],
       {"menace": [[COMPLOT, 4]], "hors_jeu": ["tj012"]}, preferer_option=["Exhaust_Jenny"]),

    # ===================================================================== tj013 Dun Import Exports
    _c("tj013 Dun Import Exports : menace de depart 2 + Entrave 1 PAR JOUEUR : 3 menaces en solo a l'entree en jeu",
       "« Hinder 1[per_hero] » : desc.Hinder = 1* (1 menace par joueur posee a l'entree en jeu) en plus de la menace de depart 2 "
       "(desc.StartingThreat = 2, non par joueur) : 2 + 1 = 3",
       [], ["Puzzle.PutIntoPlay('tj013')"], {"menace": [["tj013", 3]]}),
    _c("tj013 Dun Import Exports : Entrave 1 PAR JOUEUR : 2 + 2 = 4 menaces a deux joueurs (la menace de depart ne depend pas du nombre de joueurs)",
       "2 joueurs -> Entrave 2 + menace de depart 2 = 4",
       [], ["Puzzle.PutIntoPlay('tj013')"], {"menace": [["tj013", 4]]}, heros2="spider_man"),
    _c("tj013 Dun Import Exports : Incite 2 : revelee, 2 menaces s'ajoutent au complot PRINCIPAL",
       "« Incite 2 » : Reveal pose 2 menaces sur le principal (1 -> 3) ; la carte porte sa menace de depart (2) + son Entrave (1)",
       [f"Puzzle.SetThreat('{COMPLOT}', 1)"], ["Puzzle.Reveal('tj013')"],
       {"menace": [[COMPLOT, 3], ["tj013", 3]]}),
    _c("tj013 Dun Import Exports : icone Hazard 1 portee (une carte rencontre de plus a la phase du mechant)",
       "desc.Hazard = 1 lu par le moteur : une icone Hazard en jeu (verifiee par decoupe contre le glyphe de la police, fiche hazard.md)",
       [], ["Puzzle.PutIntoPlay('tj013')"], {"icones": [["Hazard", 1]]}),
    _c("tj013 Dun Import Exports : 2 icones de boost lues par le moteur",
       "desc.Boost = 2 (deux fleches rouges sur le scan)",
       [], ["Puzzle.PutIntoPlay('tj013')"], {"icones_boost": [["tj013", 2]]}),

    # ===================================================================== tj014 Phantasm
    _c("tj014 Phantasm : When Defeated -> Cloaked sur CHAQUE sbire PHANTOMS en jeu (Street Phantoms)",
       "Phantasm et un Street Phantoms en jeu ; Phantasm vaincu (PV 1, Tenace : un 1er coup retire Tenace, le 2e le vainc) -> le Street Phantoms "
       "porte Cloaked ; Rhino non",
       ["Puzzle.PutIntoPlay('tj014')", "Puzzle.PutIntoPlay('tj015')"], ["Puzzle.Damage('tj014', 9)", "Puzzle.Damage('tj014', 9)"],
       {"statuts": [["tj015", "Cloaked"]], "statuts_absents": [["01094", "Cloaked"]], "hors_jeu": ["tj014"]}),
    _c("tj014 Phantasm : « each PHANTOMS minion » : deux Street Phantoms -> deux Cloaked ; un sbire NON PHANTOMS (Hydra Mercenary) n'en recoit pas",
       "le trait PHANTOMS filtre : 01101 reste sans carte",
       ["Puzzle.PutIntoPlay('tj014')", "Puzzle.PutIntoPlay('tj015')", "Puzzle.PutIntoPlay('01101')"],
       ["Puzzle.Damage('tj014', 9)", "Puzzle.Damage('tj014', 9)"],
       {"statuts": [["tj015", "Cloaked"]], "statuts_absents": [["01101", "Cloaked"]]}),
    _c("tj014 Phantasm : TEMOIN, sans le When Defeated (Phantasm seul en jeu) aucune erreur et le vilain n'est pas Cloaked",
       "Phantasm vaincu seul : rien d'autre a camoufler, aucune exception",
       ["Puzzle.PutIntoPlay('tj014')"], ["Puzzle.Damage('tj014', 9)", "Puzzle.Damage('tj014', 9)"],
       {"hors_jeu": ["tj014"], "statuts_absents": [["01094", "Cloaked"]]}),
    _c("tj014 Phantasm : Retaliate 1 : le heros qui l'attaque subit 1 degat (base automatique)",
       "desc.Retaliate = 1 ; Jennika (forme heros) attaque Phantasm (Tenace) : 1 degat en retour",
       [HEROS, "Puzzle.PutIntoPlay('tj014')"], ["Puzzle.Attack('tj001a', 'tj014')"],
       {"degats_identite": 1}),
    _c("tj014 Phantasm : Tenace (Toughness 1) : la carte entre en jeu avec une carte d'etat Tenace",
       "base automatique (desc.Toughness = 1)", ["Puzzle.PutIntoPlay('tj014')"], [],
       {"statuts": [["tj014", "Tough"]], "degats": [["tj014", 0]]}),
    _c("tj014 Phantasm : Tenace absorbe un 1er coup de 9 (le statut part, aucun degat)",
       "Toughness : le 1er coup retire Tenace sans degat",
       ["Puzzle.PutIntoPlay('tj014')"], ["Puzzle.Damage('tj014', 9)"],
       {"statuts_absents": [["tj014", "Tough"]], "degats": [["tj014", 0]]}),
    _c("tj014 Phantasm : Boost 3 : l'attaque de Rhino (ATQ 2) + 3 icones = 5 degats a Jenny",
       "desc.Boost = 3 (trois fleches rouges)",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('tj014')"], ["Puzzle.Attack('01094')"],
       {"degats_identite": 5}, avec_boost=True),
    _c("tj014 Phantasm : MNG 2 / ATQ 2 / PV 1 imprimes (lus par le moteur)",
       "valeurs du scan : MNG 2, ATQ 2, PV 1",
       ["Puzzle.PutIntoPlay('tj014')"], [],
       {"valeurs": {"tj014": {"scheme": 2, "attack": 2, "max_health": 1}}}, verifier="jennika_desc"),
    # ===================================================================== tj015 Street Phantoms
    _c("tj015 Street Phantoms : When Revealed -> Cloaked sur la carte ELLE-MEME (pas le vilain)",
       "« Cloak Street Phantoms »", [], ["Puzzle.Reveal('tj015')"],
       {"statuts": [["tj015", "Cloaked"]], "statuts_absents": [["01094", "Cloaked"]]}),
    _c("tj015 Street Phantoms : Tenace (Toughness 1) a l'entree en jeu ; MNG 1 / ATQ 1 / PV 1 imprimes",
       "base automatique ; valeurs du scan", ["Puzzle.PutIntoPlay('tj015')"], [],
       {"statuts": [["tj015", "Tough"]], "valeurs": {"tj015": {"scheme": 1, "attack": 1, "max_health": 1}}},
       verifier="jennika_desc"),
    _c("tj015 Street Phantoms : Boost 2 : l'attaque de Rhino (ATQ 2) + 2 icones = 4 degats a Jenny",
       "desc.Boost = 2", ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('tj015')"],
       ["Puzzle.Attack('01094')"], {"degats_identite": 4}, avec_boost=True),
]

VERIFICATIONS = r'''
def jennika_actions_disponibles(monde, aides):
    """Nombre d'actions REELLEMENT disponibles sur `carte` (type `type`), comme Puzzle.Action les numerote."""
    from game.ability.ability import AbilityType
    from game.event.manager import EventManager
    from game.message import Message
    from game.effect.rule import GameRule
    attendu = aides["cas"]["attendu"]
    face = aides["par_id"](monde, attendu["carte"])
    if face is None:
        return False, f"{attendu['carte']} introuvable en jeu"
    joueur = monde.GetCurrentPlayer()
    type_capacite = getattr(AbilityType, attendu["type"]) if attendu.get("type") else None
    candidats = [x for x in face.effect.Find(when=Message.WhenPlayerInTurn, type=type_capacite)
                 if not x.ability.is_play]
    message = Message.WhenPlayerLikeInTurn(joueur, GameRule(joueur.GetIdentity()))
    message.Send()
    dispo = EventManager.FilterAvailableEffects(message, candidats, joueur, monde, None)
    n = len(dispo)
    if n != attendu["nombre"]:
        return False, f"{attendu['carte']} offre {n} action(s) {attendu.get('type')} (attendu {attendu['nombre']})"
    return True, f"{attendu['carte']} : {n} action(s) {attendu.get('type')} disponible(s), comme attendu"


def jennika_apres_fin_de_round(monde, aides):
    """Mesure les attributs puis envoie la fin de round (WhenRoundEnd + buff_manager.OnRoundEnd, comme
    world.end_round) et delegue a etat_attendu : `attendu` decrit l'etat APRES la fin de round."""
    from game.message import Message
    identite = aides["identite"](monde)
    avant = (identite.attack, identite.thwart, identite.defense)
    if avant != (identite.printed_attack + 1, identite.printed_thwart + 1, identite.printed_defense + 1):
        return False, f"avant la fin de round le bonus +1/+1/+1 devrait etre la : {avant}"
    Message.WhenRoundEnd(monde).Send()
    monde.stat.OnRoundEnd()
    monde.buff_manager.OnRoundEnd()
    ok, msg = etat_attendu(monde, aides)
    return ok, f"bonus avant la fin du round {avant} ; apres : {msg}"


def jennika_limite_renouvelee(monde, aides):
    """Ninja Senpai = 4 capacites (une par classe Shinobi), chacune `LimitOncePerRound`. Apres UNE carte Ninjutsu : exactement une
    est verrouillee ; apres la fin du round (WhenRoundEnd + buff_manager.OnRoundEnd), aucune."""
    from game.message import Message
    heros = aides["par_id"](monde, "tj001a")
    if heros is None:
        return False, "tj001a introuvable en jeu"
    capacites = [e.ability for e in heros.effect.GetAll() if getattr(e.ability.when, "__name__", "") == "WhenPlayerPlayCard"]
    if len(capacites) != 4:
        return False, f"Ninja Senpai devrait porter 4 capacites (une par classe), trouvees : {len(capacites)}"
    verrouillees = [a for a in capacites if not monde.stat.IsOncePerRound(a)]
    if len(verrouillees) != 1:
        return False, f"apres une carte Ninjutsu, {len(verrouillees)} capacite(s) verrouillee(s) (attendu 1)"
    Message.WhenRoundEnd(monde).Send()
    monde.stat.OnRoundEnd()
    monde.buff_manager.OnRoundEnd()
    restantes = [a for a in capacites if not monde.stat.IsOncePerRound(a)]
    if restantes:
        return False, f"apres la fin du round, {len(restantes)} capacite(s) encore verrouillee(s)"
    ok, msg = etat_attendu(monde, aides)
    return ok, f"1 capacite verrouillee puis 0 apres la fin du round ; {msg}"


def jennika_voie(monde, aides):
    """Etat apres la VRAIE mise en place : la Voie tj011 en jeu, sous le controle du joueur, en un seul exemplaire."""
    attendu = aides["cas"]["attendu"]
    soucis = []
    voie = aides["par_id"](monde, "tj011")
    if voie is None:
        soucis.append("tj011 n'est pas en jeu")
    else:
        joueur = monde.players[0]
        if voie.GetControlBy() is not joueur:
            soucis.append(f"tj011 n'est pas sous le controle du joueur ({voie.GetControlBy()})")
    total = 0
    for objet in monde.object_manager.card_dict.values():
        face = objet.face
        if face is not None and getattr(face.paper, "card_id", None) == "tj011":
            total += 1
    if total != 1:
        soucis.append(f"tj011 existe en {total} exemplaire(s) (attendu 1)")
    if "taille_main" in attendu:
        n = len(monde.players[0].hand_cards.GetAll())
        if n != attendu["taille_main"]:
            soucis.append(f"main = {n} carte(s) (attendu {attendu['taille_main']})")
    ok, msg = etat_attendu(monde, {**aides, "cas": {**aides["cas"], "attendu": {k: v for k, v in attendu.items() if k not in ("exemplaires", "taille_main")}}})
    if not ok:
        soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"Voie en jeu, controlee, 1 exemplaire ; {msg}"


def jennika_voie_type(monde, aides):
    """La Voie tj011 est un PATH, pas un Support ; aire de soutien ; invisible aux selecteurs « Support »."""
    from game.card.face.card_type import Support
    from game.operate.worlds import Worlds
    soucis = []
    voie = aides["par_id"](monde, "tj011")
    if voie is None:
        return False, "tj011 n'est pas en jeu"
    joueur = monde.players[0]
    if type(voie).__name__ != "Path" or voie.type_name != "Path":
        soucis.append(f"type = {type(voie).__name__}/{voie.type_name} (attendu Path)")
    if Support.IsType(voie):
        soucis.append("Support.IsType(tj011) est vrai")
    if voie.card.area is not joueur.supports:
        soucis.append(f"zone = {voie.card.area} (attendu l'aire de soutien)")
    if voie in Worlds.GetOnFieldSupports(voie.card.game_area):
        soucis.append("Worlds.GetOnFieldSupports voit la Voie")
    if voie in joueur.GetControlCardsByType(support=True):
        soucis.append("GetControlCardsByType(support=True) voit la Voie")
    if voie not in joueur.GetOnFieldCards():
        soucis.append("GetOnFieldCards ne voit pas la Voie (elle doit rester une carte en jeu)")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "Path en aire de soutien, ni Support ni vue des selecteurs Support"


def jennika_voie_permanente(monde, aides):
    """Permanent : une regle portee par une carte d'un AUTRE set ne retire pas la Voie du jeu (RemoveAllFromGame passe par
    OnWhenCardLeavePlay de HasPermanent)."""
    from game.effect.rule import GameRule
    from game.operate.faces import Faces
    voie = aides["par_id"](monde, "tj011")
    rhino = aides["par_id"](monde, "01094")
    if voie is None or rhino is None:
        return False, f"voie={voie} rhino={rhino}"
    if not voie.permanent:
        return False, "la Voie n'est pas Permanent"
    Faces.RemoveAllFromGame([voie], GameRule(rhino))
    if not voie.IsInPlay():
        return False, "la Voie a ete retiree du jeu par un effet d'un autre set (Permanent n'a pas protege)"
    if voie.card.area is not monde.players[0].supports:
        return False, f"la Voie a change de zone : {voie.card.area}"
    return True, "la Voie reste en jeu, dans l'aire de soutien, malgre RemoveAllFromGame d'un autre set"


def _jennika_nb_effets(face, nom_fonction):
    return [e for e in face.effect.GetAll() if nom_fonction in e.ability.func_names]


def jennika_octrois(monde, aides):
    """`attendu` : {card_id: {"ressource": n, "interruption": n} ou None = hors jeu}, `effets_distincts` : les effets de ressource
    ne sont pas partages entre porteurs. Compte les CanGenerateResources (octroi de tj009) et les WhenUnitMakeAttack
    (octroi de tj010) portes par chaque Tekko-Kagi."""
    attendu = aides["cas"]["attendu"]
    soucis = []
    effets = []
    for cid, voulu in attendu.items():
        if cid == "effets_distincts":
            continue
        face = aides["par_id"](monde, cid)
        if voulu is None:
            if face is not None:
                soucis.append(f"{cid} est encore en jeu")
            continue
        if face is None:
            soucis.append(f"{cid} introuvable en jeu")
            continue
        res = _jennika_nb_effets(face, "CanGenerateResources")
        itr = [e for e in face.effect.GetAll() if getattr(e.ability.when, "__name__", "") == "WhenUnitWouldAttack"]
        effets += [id(e) for e in res]
        if "ressource" in voulu and len(res) != voulu["ressource"]:
            soucis.append(f"{cid} porte {len(res)} ressource(s) octroyee(s) (attendu {voulu['ressource']})")
        if "interruption" in voulu and len(itr) != voulu["interruption"]:
            soucis.append(f"{cid} porte {len(itr)} interruption(s) octroyee(s) (attendu {voulu['interruption']})")
    if attendu.get("effets_distincts") and len(set(effets)) != len(effets):
        soucis.append("des effets de ressource sont partages entre porteurs")
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"octrois conformes : {attendu}"


def jennika_desc(monde, aides):
    """`attendu.restricted` : {card_id: bool} lu dans le desc de la carte ; `attendu.permanent` : {card_id: bool} lu
    sur la face EN JEU (indicateur du moteur)."""
    from cards.database import CardsDB
    attendu = aides["cas"]["attendu"]
    soucis = []
    for cid, voulu in (attendu.get("restricted") or {}).items():
        papier = CardsDB.papers[cid]
        reel = papier.desc.get("Restricted") == "1"
        if reel != voulu:
            soucis.append(f"{cid} Restricted={reel} (attendu {voulu})")
    for cid, voulu in (attendu.get("permanent") or {}).items():
        face = aides["par_id"](monde, cid)
        if face is None:
            soucis.append(f"{cid} introuvable en jeu")
            continue
        if bool(face.permanent) != voulu:
            soucis.append(f"{cid} permanent={face.permanent} (attendu {voulu})")
    for cid, attributs in (attendu.get("valeurs") or {}).items():
        face = aides["par_id"](monde, cid)
        if face is None:
            soucis.append(f"{cid} introuvable en jeu")
            continue
        for nom, voulu in attributs.items():
            reel = getattr(face, nom, None)
            if reel != voulu:
                soucis.append(f"{cid}.{nom} = {reel} (attendu {voulu})")
    # Les autres cles (statuts, ...) restent celles d'etat_attendu : une cle ignoree en silence ne prouverait rien.
    reste = {k: v for k, v in attendu.items() if k not in ("restricted", "permanent", "valeurs")}
    if reste:
        ok, msg = etat_attendu(monde, {**aides, "cas": {**aides["cas"], "attendu": reste}})
        if not ok:
            soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, "desc conforme"


def jennika_retiree_du_jeu(monde, aides):
    """`attendu.carte` doit etre dans la zone `area_removed` (retiree DE LA PARTIE, pas defaussee) ; delegue le reste a etat_attendu."""
    attendu = aides["cas"]["attendu"]
    cid = attendu["carte"]
    retirees = [getattr(f.paper, "card_id", None) for f in monde.area_removed.GetAll()]
    defausse = [getattr(f.paper, "card_id", None) for f in monde.players[0].discard_pile.GetAll()]
    soucis = []
    if cid not in retirees:
        soucis.append(f"{cid} n'est pas retiree du jeu (retirees = {retirees}, defausse = {defausse})")
    if aides["par_id"](monde, cid) is not None:
        soucis.append(f"{cid} est encore en jeu")
    ok, msg = etat_attendu(monde, {**aides, "cas": {**aides["cas"], "attendu": {k: v for k, v in attendu.items() if k != "carte"}}})
    if not ok:
        soucis.append(msg)
    if soucis:
        return False, " ; ".join(soucis)
    return True, f"{cid} retiree du jeu ; {msg}"
'''
