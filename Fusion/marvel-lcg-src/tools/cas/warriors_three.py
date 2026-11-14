# Cas test_capacites du heros THE WARRIORS THREE (Phenexian et Mysteltainn, prefixe `wt`) : noms prefixes « [wt] » puis le
# card_id (substituer_pack.py filtre dessus).
#
# Rappels de montage :
#  - le deck `warriors_three` demarre en ALTER EGO (wt001b), avec wt002 (titre) et les TROIS soutiens PERSONA wt003-wt005 deja EN JEU
#    (Setup) ; `Puzzle.ChangeToFace('wt001b', 'wt001a')` passe en HEROS FANDRAL sans rien declencher (wt001c Hogun, wt001d Volstagg) ;
#    `Puzzle.ChangeForm('wt001c')` fait un VRAI changement de forme (messages envoyes : la synchronisation des etats part) ;
#  - ⚠ la synchronisation des etats pret/epuise lit `wt_actif` sur wt002 : un `ChangeToFace` silencieux ne la met pas a jour,
#    donc les cas qui MESURENT les etats partent d'un alter ego et passent par `ChangeForm`.
#  - Rhino 01094 est le vilain, 01097b son complot principal (menace 0), 01101 Hydra Mercenary un sbire ;
#  - ressources : 01088 Energy = YY, 01089 Genius = BB, 01090 Strength = RR ; ⚠ `main_exclusive` DEFAUSSE la main de depart.
SC = "rhino"
F = "Puzzle.ChangeToFace('wt001b', 'wt001a')"
H = "Puzzle.ChangeToFace('wt001b', 'wt001c')"
V = "Puzzle.ChangeToFace('wt001b', 'wt001d')"
VILAIN = "01094"
COMPLOT = "01097b"
SBIRE = "01101"
SANS_BOOST = ["Puzzle.EmptyEncounterDeck()",
              "Puzzle.CreateEncounterDeck('01098', '01098', '01098', '01098', '01098', '01098', '01098', '01098')"]


def en_jeu(*ids):
    return [f"Puzzle.PutIntoPlay('{i}', under_control=True)" for i in ids]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    mise = SANS_BOOST + ["Puzzle.EmptyHand()"] + list(mise)
    cas = {"nom": "[wt] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "warriors_three"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "wt_etat"), "attendu": attendu}
    cas.setdefault("regles", ["v16_all", "v18_all"])
    cas.update(cle)
    return cas


CAS = [
    # ============================================================ wt001 : identite (quatre faces) et mise en place
    _c("wt001b Setup : la carte-titre wt002 et les trois soutiens PERSONA sont en jeu des le depart",
       "« Permanent. Setup. » : wt002-wt005 mis en jeu par desc.Setup depuis le hero_deck", [], [],
       {"en_jeu": ["wt002", "wt003", "wt004", "wt005"], "pv_max": [["wt001b", 12]]}, main_exclusive=["01090"]),
    _c("wt001a Fandral : PV 12, ASGARD ; ATQ 1 (1 degat a Rhino)",
       "nombres texte <-> code (scan) : HAND SIZE 4 / HIT POINTS 12, THW 2 ATK 1 DEF 1",
       [F], ["Puzzle.Attack('wt001a')"],
       {"pv_max": [["wt001a", 12]], "traits": ["ASGARD"], "degats": [[VILAIN, 1]]},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("wt001a Fandral : CTR 2 (2 menaces retirees)",
       "nombres texte <-> code (scan) : THW 2", [F, f"Puzzle.SetThreat('{COMPLOT}', 5)"], ["Puzzle.Thwart('wt001a')"],
       {"menace": [[COMPLOT, 3]]}, main_exclusive=["01090"], cibles=[COMPLOT], accepter_choix=True),
    _c("wt001c Hogun : CTR 1 (1 menace retiree)",
       "nombres texte <-> code (scan) : THW 1 ATK 1 DEF 2", [H, f"Puzzle.SetThreat('{COMPLOT}', 5)"], ["Puzzle.Thwart('wt001c')"],
       {"menace": [[COMPLOT, 4]]}, main_exclusive=["01090"], cibles=[COMPLOT], accepter_choix=True),
    _c("wt001d Volstagg : ATQ 2 (2 degats a Rhino)",
       "nombres texte <-> code (scan) : THW 1 ATK 2 DEF 1", [V], ["Puzzle.Attack('wt001d')"],
       {"degats": [[VILAIN, 2]]}, main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),

    # ============================================================ Hero Resource (identite et soutiens)
    _c("wt001a Hero Resource : Fandral (identite) + le soutien de Hogun paient Artful Bladework, +2 car paye avec Fandral",
       "« If you paid for this card with Fandral » : 4 + 2 degats", [F], [],
       {"degats": [[VILAIN, 6]], "exhausted": ["wt001a", "wt004"]},
       main_exclusive=["wt012"], payer_avec=["wt001a", "wt004"], jouer=["wt012"], cibles=[VILAIN, VILAIN], accepter_choix=True),
    _c("wt001c Hero Resource : CONTRE-CAS, Hogun (identite) + le soutien de Volstagg paient : 4 degats seulement",
       "pas de Fandral dans le paiement", [H], [],
       {"degats": [[VILAIN, 4]], "exhausted": ["wt001c", "wt005"]},
       main_exclusive=["wt012"], payer_avec=["wt001c", "wt005"], jouer=["wt012"], cibles=[VILAIN, VILAIN], accepter_choix=True),
    _c("wt003 Soutien de Fandral inactif : Hero Resource, paye Artful Bladework (+2) et s'incline",
       "« Exhaust Fandral → generate a resource » depuis son soutien (Volstagg est le heros actif ; Hogun, inactif, paie aussi)", [V], [],
       {"degats": [[VILAIN, 6]], "exhausted": ["wt003", "wt004"]},
       main_exclusive=["wt012"], payer_avec=["wt003", "wt004"], jouer=["wt012"], cibles=[VILAIN, VILAIN], accepter_choix=True),

    _c("wt004 Soutien de Hogun inactif : Hero Resource (mental), paye Artful Bladework avec le soutien de Volstagg, et s'incline",
       "« Exhaust Hogun → generate a [mental] resource » depuis son soutien (Fandral est le heros actif)", [F], [],
       {"degats": [[VILAIN, 4]], "exhausted": ["wt004", "wt005"]},
       main_exclusive=["wt012"], payer_avec=["wt004", "wt005"], jouer=["wt012"], cibles=[VILAIN, VILAIN], accepter_choix=True),
    _c("wt005 Soutien de Volstagg inactif : Hero Resource (physique), paye Mighty Endurance -> une carte Tough a un ami",
       "« If you used Volstagg to pay for this card » : le soutien de Volstagg paie, le heros actif (Fandral) recoit la Tough", [F], [],
       {"exhausted": ["wt005"], "statuts": [["wt001a", "Tough"]]},
       main_exclusive=["wt011"], payer_avec=["wt005"], jouer=["wt011"], accepter_choix=True),
    _c("wt001d Hero Resource : Volstagg (identite) paie Mighty Endurance -> une carte Tough a un ami (lui-meme)",
       "« Exhaust Volstagg → generate a [physical] resource » depuis la face HEROS", [V], [],
       {"exhausted": ["wt001d"], "statuts": [["wt001d", "Tough"]]},
       main_exclusive=["wt011"], payer_avec=["wt001d"], jouer=["wt011"], accepter_choix=True),
    _c("wt012 Artful Bladework : paye avec Fandral (identite), 4 + 2 = 6 degats",
       "« Deal 4 damage to an enemy. Then, if you paid for this card with Fandral, deal 2 damage to an enemy »", [F], [],
       {"degats": [[VILAIN, 6]]}, main_exclusive=["wt012"], payer_avec=["wt001a", "wt004"], jouer=["wt012"], cibles=[VILAIN, VILAIN], accepter_choix=True),
    _c("wt012 Artful Bladework : CONTRE-CAS, paye sans Fandral, 4 degats seulement",
       "pas de Fandral dans le paiement", [H], [],
       {"degats": [[VILAIN, 4]]}, main_exclusive=["wt012"], payer_avec=["wt001c", "wt005"], jouer=["wt012"], cibles=[VILAIN, VILAIN], accepter_choix=True),
    _c("wt001a Change To : depuis une face HEROS, la seule option libre est l'alter ego (index 0)",
       "CORRECTIF player_setup.py : « You can only change active hero when a card allows you to do so »", [F],
       ["Puzzle.Action('wt001a', 'PlayTurnOption', 0)"], {"wt_identite": "wt001b"}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt001a Change To : CONTRE-CAS, une face HEROS n'offre PAS de changement libre vers un autre heros (aucune seconde option)",
       "pas de « Change To Hogun » depuis Fandral", [F],
       [], {"wt_identite": "wt001a"}, main_exclusive=["01090"], declencher_tolerant=["Puzzle.Action('wt001a', 'PlayTurnOption', 1)"]),
    _c("wt001b Change To : depuis l'alter ego, les trois heros sont offerts (index 2 existe)",
       "« When you flip this card, flip one of your inactive heroes » : le joueur choisit son heros par « Change To »", [],
       ["Puzzle.Action('wt001b', 'PlayTurnOption', 2)"], {"wt_identite_autre_que": "wt001b"}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ changement de heros actif (wt002, wt015) et etats
    _c("wt002 Hero Action : change le heros actif (Fandral -> un autre), la carte-titre s'incline",
       "« Exhaust this card → change your active hero »", [F], ["Puzzle.Action('wt002', 'HeroAction', 0)"],
       {"exhausted": ["wt002"], "wt_identite_autre_que": "wt001a"}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt015 Leap into Action : change le heros actif (Fandral -> un autre)",
       "« Hero Action: Change your active hero »", [F], [],
       {"wt_identite_autre_que": "wt001a"}, main_exclusive=["wt015"], jouer=["wt015"], accepter_choix=True),
    _c("wt002 Etats : Fandral epuise, la carte-titre change le heros actif (-> Hogun) : Hogun est PRET, le soutien de Fandral est epuise",
       "« Heroes ... remain ready or exhausted when they flip » : chaque heros garde SON etat (ordre alphabetique : Hogun d'abord)",
       [F], ["Puzzle.Exhaust('wt001a')", "Puzzle.Action('wt002', 'HeroAction', 0)"],
       {"pret": ["wt001c"], "exhausted": ["wt003", "wt002"], "wt_identite": "wt001c"}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt002 Etats : retour a Fandral (carte-titre redressee) -> Fandral est de nouveau EPUISE, le soutien de Hogun est pret",
       "l'etat de Fandral est retrouve, pas celui de Hogun",
       [F], ["Puzzle.Exhaust('wt001a')", "Puzzle.Action('wt002', 'HeroAction', 0)", "Puzzle.Ready('wt002')", "Puzzle.Action('wt002', 'HeroAction', 0)"],
       {"exhausted": ["wt001a", "wt002"], "pret": ["wt004"], "wt_identite": "wt001a"}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt002 Etats : Fandral epuise puis alter ego -> l'alter ego reprend l'etat de la carte-titre (pret), le soutien de Fandral est epuise",
       "la carte « The Warriors Three » se retourne en gardant son etat", [F],
       ["Puzzle.Exhaust('wt001a')", "Puzzle.ChangeForm('wt001a')"],
       {"pret": ["wt001b"], "exhausted": ["wt003"], "wt_identite": "wt001b"}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt002 Etats : depuis l'alter ego, le passage a un heros lit l'etat de SON soutien (Volstagg, epuise, devient actif epuise)",
       "l'alter ego vers Volstagg (ChangeForm choisit la derniere face heros)", ["Puzzle.Exhaust('wt005')"],
       ["Puzzle.ChangeForm('wt001b')"], {"exhausted": ["wt001d"], "wt_identite": "wt001d"}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ cartes du deck de heros
    _c("wt006 Hildegarde : Response, tous les WARRIORS THREE gagnent +1 ATQ et +1 CTR jusqu'a la fin de la phase",
       "valeurs imprimees : cout 3, PV 3 ; +1 ATQ / +1 CTR sur l'identite", [F], [],
       {"attributs": {"attack": 1, "thwart": 1}, "en_jeu": ["wt006"]},
       main_exclusive=["wt006", "01088", "01090"], jouer=["wt006"], accepter_choix=True),
    _c("wt007 Brandrheid Undrsigr : Volstagg gagne +1 ATQ (3 degats) ",
       "« Volstagg gets +1 ATK » : ATQ 2 + 1", [V] + ["Puzzle.Attach('wt007', 'wt001d')"], ["Puzzle.Attack('wt001d')"],
       {"degats": [[VILAIN, 3]]}, main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("wt007 Brandrheid Undrsigr : CONTRE-CAS, Fandral n'a pas le bonus (1 degat)",
       "le bonus est celui de Volstagg", [F] + ["Puzzle.Attach('wt007', 'wt001a')"], ["Puzzle.Attack('wt001a')"],
       {"degats": [[VILAIN, 1]]}, main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("wt007 Brandrheid Undrsigr : Hero Response, apres que Volstagg devient actif, soigne 1 degat de l'identite",
       "« After Volstagg becomes the active hero, heal 1 damage from him »", ["Puzzle.Damage('wt001b', 3)", "Puzzle.Attach('wt007', 'wt001b')"],
       ["Puzzle.ChangeForm('wt001b')"], {"degats_identite": 2, "wt_identite": "wt001d"}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt008 Fimbuldraugr : Fandral gagne +1 CTR (3 menaces retirees)",
       "« Fandral gets +1 THW » : CTR 2 + 1", [F, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.Attach('wt008', 'wt001a')"],
       ["Puzzle.Thwart('wt001a')"], {"menace": [[COMPLOT, 2]]}, main_exclusive=["01090"], cibles=[COMPLOT], accepter_choix=True),
    _c("wt008 Fimbuldraugr : Hero Response, apres que Fandral devient actif, retire 1 menace d'une manigance",
       "« After Fandral becomes the active hero, remove 1 threat from a scheme »", [H, f"Puzzle.SetThreat('{COMPLOT}', 4)", "Puzzle.Attach('wt008', 'wt001c')"],
       ["Puzzle.Action('wt002', 'HeroAction', 0)"], {"menace": [[COMPLOT, 3]], "wt_identite": "wt001a"}, main_exclusive=["01090"], cibles=[COMPLOT], accepter_choix=True),
    _c("wt009 Hridgandr : Hogun gagne +1 ATQ (2 degats)", "« Hogun gets +1 ATK, +1 THW »",
       [H, "Puzzle.Attach('wt009', 'wt001c')"], ["Puzzle.Attack('wt001c')"], {"degats": [[VILAIN, 2]]},
       main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("wt009 Hridgandr : Hero Response, apres que Hogun devient actif, 1 degat a un ennemi",
       "« After Hogun becomes the active hero, deal 1 damage to an enemy »", [F, "Puzzle.Attach('wt009', 'wt001a')"],
       ["Puzzle.Action('wt002', 'HeroAction', 0)"], {"degats": [[VILAIN, 1]], "wt_identite": "wt001c"}, main_exclusive=["01090"], cibles=[VILAIN], accepter_choix=True),
    _c("wt010 Hildegund and Kin : apres le passage en alter ego, soigne 2 degats d'un personnage ami",
       "« After you flip to alter-ego, heal 2 damage from a friendly character »", [F, "Puzzle.Damage('wt001a', 3)"] + en_jeu("wt010"),
       ["Puzzle.ChangeForm('wt001b')"], {"degats_identite": 1}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt011 Mighty Endurance : paye avec Volstagg, un personnage ami recoit une carte Tough",
       "« If you used Volstagg to pay for this card, give a friendly character a tough status card »", [F], [],
       {"statuts": [["wt001a", "Tough"]]}, main_exclusive=["wt011"], payer_avec=["wt005"], jouer=["wt011"], accepter_choix=True),
    _c("wt011 Mighty Endurance : CONTRE-CAS, payee autrement, c'est Volstagg (son soutien) qui reçoit la Tough",
       "« Otherwise, give Volstagg a tough status card »", [F], [],
       {"statuts_absents": [["wt001a", "Tough"]]}, main_exclusive=["wt011", "01090"], payer_avec=["01090"], jouer=["wt011"], accepter_choix=True),
    _c("wt013 Hold the Line : la menace posee sur un complot est empechee",
       "« prevent that threat »", [F], ["Puzzle.Scheme('01094')"],
       {"menace": [[COMPLOT, 0]]}, main_exclusive=["wt013", "01090"], jouer=["wt013"], payer_avec=["01090"], accepter_choix=True),
    _c("wt014 Rally! : redresse les soutiens PERSONA (pas celui du heros actif)",
       "« Ready all PERSONA supports you control »", [F, "Puzzle.Exhaust('wt003')", "Puzzle.Exhaust('wt004')", "Puzzle.Exhaust('wt005')"], [],
       {"pret": ["wt004", "wt005"], "exhausted": ["wt003"]}, main_exclusive=["wt014"], jouer=["wt014"], accepter_choix=True),
    _c("wt022 Revelry in Asgard : +2 taille de main jusqu'a la fin du round",
       "« Alter-Ego Action: You get +2 hand size until the end of the round » (Team-Up Odinson)", ["Puzzle.PutIntoPlay('ra002', under_control=True)"],
       [], {"attributs": {"hand_size": 2}}, main_exclusive=["wt022"], jouer=["wt022"], accepter_choix=True),

    # ============================================================ arbitrages du 26/10/2026 (RR v1.8 + notice de l'auteur)
    # Q1 (notice, face B) : « Status cards on your inactive heroes will remain on them, but wont be relevant until they become the
    # active hero » ; ceux de la carte The Warriors Three « are treated as if they were on your active hero ». Le moteur les garde
    # sur l'IDENTITE : un heros passe inactif les emporte DONC avec lui (stash sur son soutien, `wt_stash`).
    _c("wt002 Etats (Q1) : Fandral Sonne, changement de heros (-> Hogun) : Hogun n'est PAS Sonne, le soutien de Fandral garde l'etat",
       "« Status cards on your inactive heroes will remain on them »", [F, "Puzzle.Stun('wt001a')"],
       ["Puzzle.Action('wt002', 'HeroAction', 0)"],
       {"wt_identite": "wt001c", "statuts_absents": [["wt001c", "Stunned"]], "wt_stash": [["wt003", "Stunned"]]},
       main_exclusive=["01090"], accepter_choix=True),
    _c("wt002 Etats (Q1) : retour a Fandral, il est de nouveau Sonne et son soutien n'a plus rien",
       "l'etat de Fandral est retrouve en redevenant actif",
       [F, "Puzzle.Stun('wt001a')"],
       ["Puzzle.Action('wt002', 'HeroAction', 0)", "Puzzle.Ready('wt002')", "Puzzle.Action('wt002', 'HeroAction', 0)"],
       {"wt_identite": "wt001a", "statuts": [["wt001a", "Stunned"]], "wt_stash_vide": ["wt003", "wt004", "wt005"]},
       main_exclusive=["01090"], accepter_choix=True),
    _c("wt002 Etats (Q1) : un etat pose sur l'ALTER EGO (la carte The Warriors Three) suit le heros actif : Volstagg reste Sonne",
       "« status cards ... on The Warriors Three card remain on the card when it flips, but they are treated as if they were on your active hero »",
       ["Puzzle.Stun('wt001b')"], ["Puzzle.ChangeForm('wt001b')"],
       {"wt_identite": "wt001d", "statuts": [["wt001d", "Stunned"]], "wt_stash_vide": ["wt003", "wt004", "wt005"]},
       main_exclusive=["01090"], accepter_choix=True),
    _c("wt002 Etats (Q1) : Fandral Tough puis alter ego : l'alter ego n'a pas la Tough de Fandral, son soutien la garde",
       "l'etat appartient a Fandral, pas a l'alter ego", [F, "Puzzle.Tough('wt001a')"], ["Puzzle.ChangeForm('wt001a')"],
       {"wt_identite": "wt001b", "statuts_absents": [["wt001b", "Tough"]], "wt_stash": [["wt003", "Tough"]]},
       main_exclusive=["01090"], accepter_choix=True),
    # Q2 : « Otherwise, give Volstagg a tough status card » : Volstagg INACTIF la recoit sur son soutien (elle l'attend).
    _c("wt011 Mighty Endurance (Q2) : payee autrement, Volstagg INACTIF recoit la Tough sur son soutien, pas Fandral",
       "notice : les etats des heros inactifs restent sur eux", [F], [],
       {"statuts_absents": [["wt001a", "Tough"]], "wt_stash": [["wt005", "Tough"]]},
       main_exclusive=["wt011", "01090"], payer_avec=["01090"], jouer=["wt011"], accepter_choix=True),
    _c("wt011 Mighty Endurance (Q2) : la Tough attendue sur le soutien de Volstagg le suit quand il devient actif",
       "Volstagg actif apres coup : la Tough est sur lui", [F], [],
       {"wt_identite": "wt001d", "statuts": [["wt001d", "Tough"]], "wt_stash_vide": ["wt005"]},
       main_exclusive=["wt011", "01090"], payer_avec=["01090"], jouer=["wt011"], declencher_apres=["Puzzle.ChangeForm('wt001a')", "Puzzle.ChangeToFace('wt001b', 'wt001d')"],
       accepter_choix=True),
    # Q3 : le soutien du heros actif n'est PAS un soutien (notice, face A).
    _c("wt021 Fated Clash (Q3) : avec Fandral actif, ce sont les soutiens de Hogun et de Volstagg qui s'inclinent, pas celui de Fandral",
       "« Exhaust two PERSONA supports you control » : le soutien du heros actif n'est pas un soutien", [F] + en_jeu("wt017"), ["Puzzle.Reveal('wt021')"],
       {"pret": ["wt003"], "exhausted": ["wt004", "wt005"]}, main_exclusive=["01090"], accepter_choix=True),
    # Q6 : « ignore all crisis icons in play » : TOUTES les cartes joueur, pas seulement celles dont Fandral est la source.
    _c("wt008 Fimbuldraugr (Q6) : Fandral actif, un ALLIE (Vision) deja en jeu retire de la menace du complot malgre une icone Crise",
       "RR « Crisis Icon » : ignorer l'icone = les cartes joueur peuvent retirer de la menace du complot principal",
       [F, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.PutIntoPlay('01125')", "Puzzle.Attach('wt008', 'wt001a')"] + en_jeu("01068"),
       ["Puzzle.Thwart('01068')"], {"menace": [[COMPLOT, 4]]}, main_exclusive=["01090"], cibles=[COMPLOT], accepter_choix=True),
    _c("wt008 Fimbuldraugr (Q6) : CONTRE-CAS, Hogun actif (Fandral inactif) : la Crise bloque l'allie, la menace reste a 5",
       "« while he is your active hero »",
       [H, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.PutIntoPlay('01125')", "Puzzle.Attach('wt008', 'wt001c')"] + en_jeu("01068"),
       [], {"menace": [[COMPLOT, 5]]}, main_exclusive=["01090"], declencher_tolerant=["Puzzle.Thwart('01068')"], cibles=[COMPLOT], accepter_choix=True),
    # Q15 : « this turn » = le TOUR du joueur, pas le round.
    _c("wt022 Revelry in Asgard (Q15) : un sbire vaincu CE tour -> +3 taille de main",
       "« If a minion was defeated this turn, you get +3 hand size instead »",
       ["Puzzle.PutIntoPlay('ra002', under_control=True)", "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage('01101', 5)"],
       [], {"attributs": {"hand_size": 3}}, main_exclusive=["wt022"], jouer=["wt022"], accepter_choix=True),
    _c("wt022 Revelry in Asgard (Q15) : CONTRE-CAS, un sbire vaincu au tour PRECEDENT (meme round) ne compte pas -> +2",
       "« this turn » : le tour du joueur, pas le round",
       ["Puzzle.PutIntoPlay('ra002', under_control=True)", "Puzzle.PutIntoPlay('01101')", "Puzzle.Damage('01101', 5)",
        "Puzzle.EndPlayerTurn()", "Puzzle.BeginPlayerTurn()"],
       [], {"attributs": {"hand_size": 2}}, main_exclusive=["wt022"], jouer=["wt022"], accepter_choix=True),

    # ============================================================ nemesis
    _c("wt017 Fenris : ne peut pas prendre de degats",
       "« Fenris can not take damage or be defeated »", [F] + en_jeu("wt017"), ["Puzzle.Damage('wt017', 5)"],
       {"degats": [["wt017", 0]], "en_jeu": ["wt017"]}, main_exclusive=["01090"]),
    _c("wt017 Fenris : manigance -> 1 menace sur Countdown to Ragnarok",
       "« When Fenris schemes, place 1 threat on Countdown to Ragnarok »", [F] + en_jeu("wt017", "wt018"), ["Puzzle.Scheme('wt017')"],
       {"menace": [["wt018", 1]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt018 Countdown to Ragnarok : a 5 menaces, les joueurs perdent",
       "« if there is at least 5 threat here, the players lose the game » (cinq manigances de Fenris ; le SetThreat de mise en place est empeche : seul Fenris place de la menace ici)",
       [F] + en_jeu("wt017", "wt018"), ["Puzzle.Scheme('wt017')"] * 5, {"wt_perdu": True}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt018 Countdown to Ragnarok : CONTRE-CAS, a 3 menaces la partie continue",
       "seuil de 5", [F] + en_jeu("wt017", "wt018"), ["Puzzle.Scheme('wt017')"] * 3,
       {"wt_perdu": False, "menace": [["wt018", 3]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt018 Countdown to Ragnarok : la menace ne vient que de Fenris (celle posee par la regle de debogage est empechee)",
       "« Threat can only be placed on this scheme by Fenris »", [F] + en_jeu("wt017", "wt018") + ["Puzzle.SetThreat('wt018', 4)"], [],
       {"menace": [["wt018", 0]]}, main_exclusive=["01090"]),
    _c("wt016 A Questing We Shall Go! : revelee, elle cherche le sbire le plus bas du deck rencontre, le revele et s'y attache",
       "« Search the encounter deck for the bottommost minion. Reveal it, then attach this card to it »",
       [F, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01098', '01101')"], ["Puzzle.Reveal('wt016')"],
       {"en_jeu": ["01101"], "pv_max": [["01101", 8]], "traits_de": [["01101", "ELITE"]], "hotes": [["wt016", "01101"]]}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt016 A Questing We Shall Go! (Q9) : le sbire vaincu, la carte attachee part avec lui (defaussee, plus en jeu)",
       "RR Attachment : une carte attachee quitte le jeu avec son hote ; elle n'a plus de bonus a donner",
       [F, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01098', '01101')"], ["Puzzle.Reveal('wt016')", "Puzzle.Damage('01101', 10)"],
       {"hors_jeu": ["01101", "wt016"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt016 A Questing We Shall Go! (Q9) : CONTRE-CAS, aucun sbire dans le deck rencontre : rien a attacher, la carte prend surge (un vilain de plus est revele)",
       "« If you can't, this card gains surge »",
       [F, "Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01098', '01098', '01098')"], ["Puzzle.Reveal('wt016')"],
       {"hors_jeu": ["01101"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt019 Gleipnir : Boost, la carte est revelee (pas d'exception quand le vilain la retourne en renfort)",
       "« [star] Boost: Reveal this card » : donnee face cachee en boost a Rhino, qui attaque",
       [F, "Puzzle.GiveFacedownBoost('01094', 'wt019')"], ["Puzzle.Attack('01094')"],
       {"en_jeu": ["wt019"]}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt019 Gleipnir : Hero Action, 3 ressources + defausse → defausse Fenris",
       "« Spend 3 resources and discard Gleipnir → discard Fenris »", [F] + en_jeu("wt017", "wt019"),
       ["Puzzle.Action('wt019', 'HeroAction', 0)"], {"defausse_rencontre": ["wt017"]},
       main_exclusive=["01088", "01089", "01090"], accepter_choix=True),
    _c("wt020 Skadihr : vaincue, elle devient un allie WARRIORS THREE",
       "« put her under your control as a WARRIORS THREE ally »", [F] + en_jeu("wt020"), ["Puzzle.Damage('wt020', 9)"],
       {"wt_allie_nom": "Skadihr"}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt020 Skadihr : « Quickstrike », des qu'elle s'engage avec le heros elle attaque (ATQ 2 - DEF 1 de Fandral = 1 degat)",
       "« Quickstrike. » : mot-clef lu dans desc (la cle manquait, relevee le 26/10/2026 par verifier_coherence_cartes) ; mise en jeu SOUS CONTROLE = engagee avec le heros ; ATQ 2",
       [F] + en_jeu("wt020"), [],
       {"degats_identite": 1}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt020 Skadihr : TEMOIN, en ALTER EGO elle s'engage sans attaquer (Quickstrike ne vise qu'un heros) -> 0 degat",
       "Quickstrike n'attaque que si le joueur est en forme heros (fiche mots-cles/quickstrike.md)",
       [] + en_jeu("wt020"), [], {"degats_identite": 0}, main_exclusive=["01090"], accepter_choix=True),
    _c("wt021 Fated Clash : revelee, deux soutiens PERSONA s'inclinent (ou Fenris manigance)",
       "« Choose one: Exhaust two PERSONA supports you control / Fenris schemes »", [F] + en_jeu("wt017"), ["Puzzle.Reveal('wt021')"],
       {"wt_persona_epuises_min": 1}, main_exclusive=["01090"], accepter_choix=True),

    # ============================================================ mesures MULTIJOUEUR du 26/10/2026 (consigne : « ce qui n'a pas ete mesure »)
    # Fimbuldraugr : « ignore all crisis icons in play » = TOUTE source de Crise, y compris l'allie d'un AUTRE joueur (2 joueurs).
    _c("wt008 Fimbuldraugr (2 joueurs) : Fandral actif, l'ALLIE DE L'AUTRE JOUEUR (Vision, siege 1) retire de la menace malgre une icone Crise",
       "RR « Crisis Icon » : l'icone ignoree ne bloque aucune carte joueur, quel que soit son controleur",
       [F, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.PutIntoPlay('01125')", "Puzzle.Attach('wt008', 'wt001a')",
        "Puzzle.PutIntoPlay('01068', under_control=True, player=1)"],
       ["Puzzle.Thwart('01068')"], {"menace": [[COMPLOT, 4]]}, main_exclusive=["01090"], cibles=[COMPLOT], accepter_choix=True,
       heros2="spider_man"),
    _c("wt008 Fimbuldraugr (2 joueurs) : CONTRE-CAS, Hogun actif (Fandral inactif) : la Crise bloque l'allie de l'AUTRE joueur, la menace reste a 5",
       "« while he is your active hero » : Fimbuldraugr n'agit que pour Fandral actif",
       [H, f"Puzzle.SetThreat('{COMPLOT}', 5)", "Puzzle.PutIntoPlay('01125')", "Puzzle.Attach('wt008', 'wt001c')",
        "Puzzle.PutIntoPlay('01068', under_control=True, player=1)"],
       [], {"menace": [[COMPLOT, 5]]}, main_exclusive=["01090"], declencher_tolerant=["Puzzle.Thwart('01068')"], cibles=[COMPLOT],
       accepter_choix=True, heros2="spider_man"),
    # Revelry : « this turn » = le tour du JOUEUR qui joue la carte ; un sbire vaincu pendant le tour d'un AUTRE joueur ne compte pas.
    _c("wt022 Revelry in Asgard (2 joueurs) : un sbire vaincu pendant le tour de l'AUTRE joueur ne compte pas -> +2",
       "RR « Turn » : le tour de l'autre joueur est fini ; l'indicateur est remis a faux au debut de CHAQUE tour (AnyPlayer)",
       ["Puzzle.PutIntoPlay('ra002', under_control=True)", "Puzzle.PutIntoPlay('01101')", "Puzzle.BeginPlayerTurn(1)",
        "Puzzle.Damage('01101', 5)", "Puzzle.EndPlayerTurn(1)", "Puzzle.BeginPlayerTurn()"],
       [], {"attributs": {"hand_size": 2}}, main_exclusive=["wt022"], jouer=["wt022"], accepter_choix=True, heros2="spider_man"),
    _c("wt022 Revelry in Asgard (2 joueurs) : TEMOIN, un sbire vaincu pendant MON tour (apres le tour de l'autre joueur) -> +3",
       "« If a minion was defeated this turn » : le tour du joueur qui joue la carte",
       ["Puzzle.PutIntoPlay('ra002', under_control=True)", "Puzzle.PutIntoPlay('01101')", "Puzzle.BeginPlayerTurn(1)",
        "Puzzle.EndPlayerTurn(1)", "Puzzle.BeginPlayerTurn()", "Puzzle.Damage('01101', 5)"],
       [], {"attributs": {"hand_size": 3}}, main_exclusive=["wt022"], jouer=["wt022"], accepter_choix=True, heros2="spider_man"),
]


VERIFICATIONS = r'''
def wt_etat(monde, aides):
    """Cles propres : `wt_identite` (card_id de la face de l'identite), `wt_identite_autre_que` (une face HEROS DIFFERENTE),
    `wt_perdu` (la partie est perdue ou non), `wt_allie_nom` (un allie du joueur porte ce nom),
    `wt_persona_epuises_min` (au moins n soutiens PERSONA epuises) ; le reste va a etat_attendu."""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    identite = aides["identite"](monde)
    face_id = getattr(identite.paper, "card_id", None)
    if "wt_identite" in attendu and face_id != attendu["wt_identite"]:
        soucis.append(f"identite {face_id} (attendu {attendu['wt_identite']})")
    if "wt_identite_autre_que" in attendu:
        if face_id == attendu["wt_identite_autre_que"] or face_id not in ("wt001a", "wt001c", "wt001d"):
            soucis.append(f"identite {face_id} (attendu une AUTRE face heros que {attendu['wt_identite_autre_que']})")
    if "wt_perdu" in attendu:
        perdu = bool(getattr(monde, "is_game_over", False))
        if perdu != attendu["wt_perdu"]:
            soucis.append(f"partie perdue = {perdu} (attendu {attendu['wt_perdu']})")
    if "wt_allie_nom" in attendu:
        joueur = monde.players[0]
        noms = [getattr(f, "name", "") for f in joueur.allies.Get()]
        if not any(attendu["wt_allie_nom"] in n for n in noms):
            soucis.append(f"aucun allie nomme {attendu['wt_allie_nom']} (allies = {noms})")
    if "wt_persona_epuises_min" in attendu:
        joueur = monde.players[0]
        n = 0
        for objet in monde.object_manager.card_dict.values():
            face = getattr(objet, "face", None) or objet
            if getattr(getattr(face, "paper", None), "card_id", None) in ("wt003", "wt004", "wt005", "wt010") and face.IsInPlay() and not face.card.IsReady():
                n += 1
        if n < attendu["wt_persona_epuises_min"]:
            soucis.append(f"{n} soutien(s) PERSONA epuise(s) (attendu au moins {attendu['wt_persona_epuises_min']})")
    # `wt_stash` : [[soutien, statut]] : la carte d'etat attend sur le SOUTIEN du heros inactif ; `wt_stash_vide` : [soutien] sans aucune.
    for card_id, statut in attendu.get("wt_stash") or []:
        face = aides["par_id"](monde, card_id)
        noms = [str(getattr(f, 'name', '') or f.printed_name) for f in face.components.status.deck.GetAll()] if face is not None else []
        if not any(statut in n for n in noms):
            soucis.append(f"{card_id} ne garde pas l'etat {statut} (etats = {noms})")
    for card_id in attendu.get("wt_stash_vide") or []:
        face = aides["par_id"](monde, card_id)
        n = face.components.status.deck.GetSize() if face is not None else 0
        if n:
            soucis.append(f"{card_id} garde {n} carte(s) d'etat (attendu aucune)")
    propres = ("wt_identite", "wt_identite_autre_que", "wt_perdu", "wt_allie_nom", "wt_persona_epuises_min", "wt_stash", "wt_stash_vide")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(cas); copie["cas"]["attendu"] = reste
    ok, message = etat_attendu(monde, copie)
    if not ok:
        soucis.append(message)
    if soucis:
        return False, " ; ".join(soucis)
    return True, message
'''
