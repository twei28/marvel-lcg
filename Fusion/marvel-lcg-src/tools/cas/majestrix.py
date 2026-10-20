# Cas test_capacites du scenario 2 MAJESTRIX'S VERDICT de Galactic Storm (gs114-gs137), lot GS-5 (20/10/2026).
# Format identique a tools/test_capacites.py ; noms prefixes `[mv]` puis le card_id (filtre : `[mv]`, ou
# `[mv] gs131 ` pour une carte).
#
# Conventions de ce fichier :
#  - le heros de test (Spider-Man, 01001, ATQ 2 / CTR 1 / DEF 3) demarre en ALTER EGO ; `HEROS` le met en heros.
#  - la mise en place REELLE du scenario tourne a chaque cas : Imprisoned on Chandilar (gs119) en jeu avec
#    6 + 1[per_hero] menaces (1B), les six STARJAMMER glisses dessous, le Trone (gs120a) mis de cote.
#  - `LIBERER` : la derniere menace quitte la prison par le CHEMIN REEL (`SetThreat` -> RemoveThreatFromSchemes),
#    l'Interruption forcee de gs119 met en jeu l'allie designe par `cibles` (card_id).
#  - `DECK_NEUTRE` : le deck rencontre ne contient que des Advance (01186), traitrise SANS icone de boost ni
#    capacite Boost : une activation de Deathbird ne recoit alors aucun bonus de boost (mesures exactes).
#  - la main de depart de Spider-Man contient Great Responsibility (01061), qui transforme une pose de menace en
#    degats : les cas qui mesurent une pose de menace pendant une ACTIVATION fixent la main (`main_exclusive`).
SC = "gs_majestrix_verdict"
SCE = "gs_majestrix_verdict_expert"
HEROS = "Puzzle.ChangeForm('01001b')"
LIBERER = "Puzzle.SetThreat('gs119', 0)"
DECK_NEUTRE = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01186', '01186', '01186', '01186')"]
SANS_DEFENSE = {"passer_sur_option": "Defense"}
TOUS = ["gs121", "gs122", "gs123", "gs124", "gs125", "gs126"]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[mv] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "mv_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================== gs117a / gs117b : mise en place
    _c("gs117a Setup : la prison entre en jeu, les SIX STARJAMMER glisses dessous face visible, le Trone mis de cote",
       "« Put the Imprisoned on Chandilar side scheme into play and tuck each STARJAMMER ally under it. Set the Shi'ar "
       "Throne side scheme aside » (WhenCardSetup, modele 50087a)",
       [], [], {"en_jeu": ["gs119"], "glisses": TOUS, "glisses_visibles": True, "mis_de_cote_scenario": ["gs120a"],
                "hors_jeu": ["gs120a", "gs120b"]}),
    _c("gs117b When Revealed : 1[per_hero] menace sur la prison (6 de depart + 1 = 7, un joueur)",
       "« Place 1[per_hero] threat on Imprisoned on Chandilar » (1B revelee a la mise en place)",
       [], [], {"menace": [["gs119", 7], ["gs117b", 0]]}),
    _c("gs117b Forced Response apres l'etape 1 : joueur en ALTER EGO -> +2 sur la prison (7 -> 9)",
       "« After resolving step one of the villain phase, place 2 threat on Imprisoned for each player in alter-ego "
       "form » (AfterResolveVillainPhaseStep, modele 04096b) ; le verificateur envoie la fin de l'etape 1",
       [], [], {"menace": [["gs119", 9]]}, verifier="mv_etape_un"),
    _c("gs117b Forced Response apres l'etape 1, TEMOIN : joueur en HEROS -> rien (7)",
       "« for each player in ALTER-EGO form » : 0 joueur en alter ego, 0 menace",
       [HEROS], [], {"menace": [["gs119", 7]]}, verifier="mv_etape_un"),
    # ============================================================== gs119 Imprisoned on Chandilar
    _c("gs119 Forced Interrupt : la derniere menace part -> l'allie choisi (Corsair) entre en jeu sous controle, 6 menaces reviennent",
       "« When the last threat is removed from here, choose a STARJAMMER ally tucked under here, put that ally into play "
       "under any player's control and place 6 threat here » (modele 50088b)",
       [], [LIBERER], {"sous_controle": ["gs123"], "menace": [["gs119", 6]],
                       "glisses": ["gs121", "gs122", "gs124", "gs125", "gs126"]}, cibles=["gs123"]),
    _c("gs119 Forced Response : un STARJAMMER vaincu (Corsair) est glisse a nouveau sous la prison",
       "« After a STARJAMMER ally leaves play, tuck it under here » (modele 50081, face visible)",
       [LIBERER], ["Puzzle.Damage('gs123', 9)"], {"glisses": ["gs121", "gs122", "gs123", "gs124", "gs125", "gs126"],
                                                  "glisses_visibles": True, "hors_jeu": ["gs123"]}, cibles=["gs123"]),
    _c("gs119 Forced Response, TEMOIN : un allie NON STARJAMMER vaincu n'est pas glisse",
       "« a STARJAMMER ally » : Black Widow (01075, sans le trait) part en defausse, la prison garde ses 6 glisses",
       ["Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Damage('01075', 9)"],
       {"glisses": TOUS, "hors_jeu": ["01075"]}),
    _c("gs119 Assault : le contre de base de Spider-Man (CTR 1, ATQ 2) retire 2 menaces de la prison",
       "base automatique `desc.Assault` (fiche assault.md) : « basic thwart ... uses its ATK instead of its THW »",
       [HEROS], ["Puzzle.Thwart('01001a')"], {"menace": [["gs119", 5]]}, cibles=["gs119"]),
    _c("gs119 Permanent : une defausse par une regle d'un autre set laisse la prison en jeu",
       "base automatique `desc.Permanent` (fiche permanent.md : seul un effet du meme set la fait quitter le jeu)",
       [], ["Puzzle.Discard('gs119')"], {"en_jeu": ["gs119"], "glisses": TOUS}),
    # ============================================================== gs121 Lilandra
    _c("gs121 Forced Response : Lilandra entre en jeu -> le Trone mis de cote est revele (3[per_hero] menaces, Hazard)",
       "« After Lilandra enters play, reveal the set aside Shi'ar Throne side scheme »",
       [], [LIBERER], {"sous_controle": ["gs121"], "en_jeu": ["gs120a"], "menace": [["gs120a", 3]],
                       "icones": [["Hazard", 1]]}, cibles=["gs121"]),
    _c("gs121 Does not count against your ally limit : 3 allies + Lilandra, Lilandra hors du compte",
       "« Does not count against your ally limit » (ThisNotCountAllyLimit, modele 50091) : limite 3, Lilandra en plus",
       [LIBERER, "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.PutIntoPlay('01076', under_control=True)",
        "Puzzle.PutIntoPlay('01083', under_control=True)"], [],
       {"sous_controle": ["gs121", "01075", "01076", "01083"], "allies_comptes": 3}, cibles=["gs121"]),
    _c("gs121 « If Lilandra is removed from the game, the players lose the game » : Lilandra en jeu retiree de la partie",
       "`AfterCardLeavePlay('This')` vers la zone des cartes retirees -> defaite",
       [LIBERER], ["Puzzle.Remove('gs121')"], {"defaite": True}, cibles=["gs121"]),
    _c("gs121 defaite, TEMOIN : Lilandra VAINCUE n'est pas retiree de la partie (glissee sous la prison, pas de defaite)",
       "« REMOVED from the game » ≠ vaincue",
       [LIBERER], ["Puzzle.Damage('gs121', 9)"], {"defaite": False, "glisses": TOUS}, cibles=["gs121"]),
    # ============================================================== gs114 / gs115 / gs116 Deathbird
    _c("gs114 Forced interrupt : Deathbird attaque Ch'od (STARJAMMER controle) au lieu du heros, avec +1 ATQ (3 degats)",
       "« she attacks that ally instead with +1 ATK » (ReplaceTarget, modele 50089b) ; deck neutre (0 icone de boost)",
       [LIBERER, HEROS] + DECK_NEUTRE, ["Puzzle.Attack('gs114')"],
       {"degats": [["gs122", 3]], "degats_identite": 0}, cibles=["gs122"], **SANS_DEFENSE),
    _c("gs114 Forced interrupt, TEMOIN : aucun STARJAMMER en jeu -> Deathbird attaque le heros (2 degats)",
       "ligne de base : ATQ 2, deck neutre",
       [HEROS] + DECK_NEUTRE, ["Puzzle.Attack('gs114')"], {"degats_identite": 2}, **SANS_DEFENSE),
    _c("gs114 Forced interrupt, TEMOIN : un allie NON STARJAMMER (Black Widow) ne detourne pas l'attaque",
       "« if you control a STARJAMMER ally »",
       [HEROS, "Puzzle.PutIntoPlay('01075', under_control=True)"] + DECK_NEUTRE, ["Puzzle.Attack('gs114')"],
       {"degats_identite": 2, "degats": [["01075", 0]]}, **SANS_DEFENSE),
    _c("gs122 Retaliate 2 : Deathbird detournee sur Ch'od subit 2 degats de riposte",
       "base automatique `desc.Retaliate` 2",
       [LIBERER, HEROS] + DECK_NEUTRE, ["Puzzle.Attack('gs114')"],
       {"degats": [["gs114", 2], ["gs122", 3]]}, cibles=["gs122"], **SANS_DEFENSE),
    _c("gs115 Forced interrupt : Deathbird II detournee sur Ch'od avec +1 ATQ (ATQ 3 + 1 = 4 degats)",
       "meme texte que gs114, ATQ 3",
       [LIBERER, HEROS, "Puzzle.AdvanceVillain()"] + DECK_NEUTRE, ["Puzzle.Attack('gs115')"],
       {"degats": [["gs122", 4]], "degats_identite": 0, "mechant_id": "gs115"}, cibles=["gs122"], **SANS_DEFENSE),
    _c("gs115 cannot be defeated : sans Lilandra ni le soutien Shi'ar Throne, Deathbird II a 0 PV reste en jeu",
       "« Deathbird cannot be defeated, if players do not control Lilandra and the Shi'ar Throne support » (modele 50129a)",
       ["Puzzle.AdvanceVillain()"], ["Puzzle.Damage('gs115', 99)"], {"mechant_id": "gs115", "victoire": False}),
    _c("gs115 cannot be defeated, TEMOIN : Lilandra ET le soutien Shi'ar Throne controles -> Deathbird II vaincue (victoire)",
       "les deux conditions remplies : la defaite ordinaire s'applique (dernier stade du mode standard)",
       [LIBERER, "Puzzle.SetThreat('gs120a', 0)", "Puzzle.AdvanceVillain()"], ["Puzzle.Damage('gs115', 99)"],
       {"victoire": True}, cibles=["gs121"]),
    _c("gs115 cannot be defeated : Deathbird II a 0 PV tombe des que Lilandra et le Trone passent sous controle",
       "`change_on_event` : la condition change APRES les degats, la defaite est relancee",
       ["Puzzle.AdvanceVillain()", "Puzzle.Damage('gs115', 99)"], [LIBERER, "Puzzle.SetThreat('gs120a', 0)"],
       {"victoire": True}, cibles=["gs121"]),
    _c("gs116 Forced interrupt (expert) : Deathbird III detournee sur Ch'od SANS +1 ATQ, avec 1 carte de boost en plus (2 recues)",
       "« she attacks that ally instead. Give her 1 additional boost card for that activation »",
       [LIBERER, HEROS, "Puzzle.AdvanceVillain()"] + DECK_NEUTRE, ["Puzzle.Attack('gs116')"],
       {"degats": [["gs122", 3]], "boosts_sur": [["gs116", 2]], "mechant_id": "gs116"},
       cibles=["gs122"], scenario=SCE, **SANS_DEFENSE),
    _c("gs116 Forced interrupt, TEMOIN : sans STARJAMMER, Deathbird III attaque le heros avec UNE carte de boost",
       "ligne de base du precedent",
       [HEROS, "Puzzle.AdvanceVillain()"] + DECK_NEUTRE, ["Puzzle.Attack('gs116')"],
       {"degats_identite": 3, "boosts_sur": [["gs116", 1]]}, scenario=SCE, **SANS_DEFENSE),
    _c("gs116 cannot be defeated (expert) : Deathbird III a 0 PV reste en jeu sans Lilandra ni le Trone",
       "meme texte que gs115",
       ["Puzzle.AdvanceVillain()"], ["Puzzle.Damage('gs116', 99)"], {"mechant_id": "gs116", "victoire": False},
       scenario=SCE),
    # ============================================================== gs118a / gs118b Majestrix's Verdict
    _c("gs118a When Revealed : le STARJAMMER glisse choisi (Ch'od) est retire de la partie, puis 2B (prison +1)",
       "« choose 1 STARJAMMER ally tucked under Imprisoned on Chandilar and remove it from the game. Advance to stage 2B »",
       [], ["Puzzle.AdvanceMainScheme(1)"],
       {"retires": ["gs122"], "glisses": ["gs121", "gs123", "gs124", "gs125", "gs126"], "principale": "gs118b",
        "menace": [["gs119", 8]], "defaite": False}, cibles=["gs122"]),
    _c("gs118a When Revealed (expert) : DEUX STARJAMMER glisses retires de la partie",
       "« (2 STARJAMMER allies instead in expert mode) »",
       [], ["Puzzle.AdvanceMainScheme(1)"],
       {"retires": ["gs122", "gs123"], "glisses": ["gs121", "gs124", "gs125", "gs126"], "principale": "gs118b"},
       cibles=["gs122", "gs123"], scenario=SCE),
    _c("gs118a FAQ (expert) : un SEUL glisse -> lui seul est retire, aucun allie en jeu n'est touche",
       "FAQ du livret 1.2 : « Otherwise » ne joue que si AUCUN STARJAMMER n'est glisse. Montage (limite de 3 allies, "
       "Lilandra hors compte) : 1er passage en 2A retire Ch'od et Corsair ; Lilandra, Hepzibah, Korvus liberes ; "
       "2B accomplie -> 2A ne trouve que Raza glisse",
       ["Puzzle.AdvanceMainScheme(1)"] + [LIBERER] * 3, ["Puzzle.SetThreat('gs118b', 5)"],
       {"retires": ["gs122", "gs123", "gs126"], "nb_retires": 3, "nb_glisses": 0,
        "sous_controle": ["gs121", "gs124", "gs125"], "defaite": False},
       cibles=["gs122", "gs123", "gs121", "gs124", "gs125", "gs126"], scenario=SCE),
    _c("gs118a Otherwise : plus aucun glisse -> un STARJAMMER EN JEU (Corsair) est retire de la partie",
       "« Otherwise, the players as a group choose 1 STARJAMMER ally in play and remove it from the game ». Montage : "
       "2A retire Ch'od, 4 liberes (Corsair, Lilandra, Hepzibah, Korvus), 2B accomplie -> Raza (glisse) retire, "
       "2B accomplie une 2e fois -> plus aucun glisse, Corsair (en jeu) retire",
       ["Puzzle.AdvanceMainScheme(1)"] + [LIBERER] * 4 + ["Puzzle.SetThreat('gs118b', 5)"],
       ["Puzzle.SetThreat('gs118b', 5)"],
       {"retires": ["gs122", "gs126", "gs123"], "nb_retires": 3, "nb_glisses": 0, "defaite": False,
        "sous_controle": ["gs121", "gs124", "gs125"]},
       cibles=["gs122", "gs123", "gs121", "gs124", "gs125", "gs126"]),
    _c("gs118a Lilandra glissee executee -> les joueurs perdent",
       "« If Lilandra is removed from the game, the players lose the game » (insert, gs121) via `RetirerDeLaPartie`",
       [], ["Puzzle.AdvanceMainScheme(1)"], {"retires": ["gs121"], "defaite": True}, cibles=["gs121"]),
    _c("gs118b Forced Interrupt : 2B serait accomplie -> retournee et revelee (2A execute un 2e STARJAMMER), retour en 2B a 0",
       "« When this stage would be completed, flip this card and reveal it instead » (modele sk145b) : pas de defaite",
       ["Puzzle.AdvanceMainScheme(1)"], ["Puzzle.SetThreat('gs118b', 5)"],
       {"principale": "gs118b", "menace": [["gs118b", 0]], "nb_retires": 2, "nb_glisses": 4, "defaite": False},
       cibles=["gs122", "gs123"]),
    _c("gs118b When Revealed : 1[per_hero] menace sur la prison (7 -> 8)",
       "« Place 1[per_hero] threat on Imprisoned on Chandilar »",
       [], ["Puzzle.AdvanceMainScheme(1)"], {"principale": "gs118b", "menace": [["gs119", 8]]}, cibles=["gs122"]),
    _c("gs118b Forced Response apres l'etape 1 : alter ego -> +2 sur la prison (8 -> 10)",
       "meme capacite que 1B",
       ["Puzzle.AdvanceMainScheme(1)"], [], {"principale": "gs118b", "menace": [["gs119", 10]]},
       cibles=["gs122"], verifier="mv_etape_un"),
    # ============================================================== gs120a / gs120b Shi'ar Throne
    _c("gs120a When Defeated : le joueur qui la vainc retourne le Trone et en prend le controle (soutien gs120b)",
       "« The defeating player flips this card and takes control of it » (modele 32172a)",
       [LIBERER], ["Puzzle.SetThreat('gs120a', 0)"], {"sous_controle": ["gs120b"], "hors_jeu": ["gs120a"]},
       cibles=["gs121"]),
    _c("gs120b Forced Response : Lilandra quitte le jeu -> le soutien se retourne et la manigance est revelee (3 menaces)",
       "« After Shi'ar Throne or LILANDRA leaves play, flip this card and reveal it »",
       [LIBERER, "Puzzle.SetThreat('gs120a', 0)"], ["Puzzle.Damage('gs121', 9)"],
       {"en_jeu": ["gs120a"], "hors_jeu": ["gs120b", "gs121"], "menace": [["gs120a", 3]]}, cibles=["gs121"]),
    _c("gs120b Forced Response : le soutien Shi'ar Throne quitte le jeu (defausse) -> retourne et revele (3 menaces)",
       "« After SHI'AR THRONE or Lilandra leaves play, flip this card and reveal it »",
       [LIBERER, "Puzzle.SetThreat('gs120a', 0)"], ["Puzzle.Discard('gs120b')"],
       {"en_jeu": ["gs120a", "gs121"], "hors_jeu": ["gs120b"], "menace": [["gs120a", 3]]}, cibles=["gs121"]),
    _c("gs120b Resource : incliner le Trone paie Aunt May (cout 1) sans autre ressource",
       "« Resource: Exhaust Shi'ar Throne → generate a [mental] resource for any player » (modele 16142) ; en HEROS : "
       "Peter Parker (alter ego) a sa propre ressource [mental] et payait a la place du Trone",
       [LIBERER, "Puzzle.SetThreat('gs120a', 0)", HEROS], [], {"en_jeu": ["01006"], "exhausted": ["gs120b"]},
       cibles=["gs121"], main_exclusive=["01006"], jouer=["01006"]),
    # ============================================================== gs123 / gs124 / gs125 / gs126 Starjammers
    _c("gs123 Corsair : ses attaques gagnent Distance -> pas de riposte du Jailor (1 seul degat, consecutif)",
       "« Corsair's attacks gain ranged » ; Jailor of Chandilar a Riposte 1",
       [LIBERER] + DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs131')"], ["Puzzle.Attack('gs123')"],
       {"degats": [["gs123", 1], ["gs131", 2]]}, cibles=["gs123", "gs131"]),
    _c("gs124 Hepzibah : ses attaques gagnent Percant -> le Tenace de Deathbird saute, 3 degats passent",
       "« Hepzibah's attacks gain piercing »",
       [LIBERER, "Puzzle.Tough('gs114')"], ["Puzzle.Attack('gs124')"],
       {"degats": [["gs114", 3]], "statuts_absents": [["gs114", "Tough"]]}, cibles=["gs124", "gs114"]),
    _c("gs125 Korvus : ses attaques gagnent Debordement -> 2 degats en exces sur Deathbird (Jailor a 1 PV)",
       "« Korvus's attacks gain overkill »",
       [LIBERER] + DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs131')", "Puzzle.Damage('gs131', 5)"], ["Puzzle.Attack('gs125')"],
       {"degats": [["gs114", 2]], "hors_jeu": ["gs131"]}, cibles=["gs125", "gs131"]),
    _c("gs126 Raza : Toughness -> il entre en jeu avec une carte d'etat Tenace",
       "base automatique `desc.Toughness`",
       [LIBERER], [], {"statuts": [["gs126", "Tough"]]}, cibles=["gs126"]),
    # ============================================================== gs127 / gs128 / gs129 attachements
    _c("gs127 Royal Cape : attachee a Deathbird, +2 PV (18) et Riposte 1",
       "« Attach to Deathbird. Attached character gets +2 hit points and gains retaliate 1 »",
       ["Puzzle.PutIntoPlay('gs127')"], [],
       {"accroche_a": [["gs127", "gs114"]], "pv_max": [["gs114", 18]], "attributs_carte": [["gs114", "retaliate", 1]]}),
    _c("gs127 Royal Cape Response : Lilandra attaque Deathbird, [energy] paye -> la Cape passe sur Lilandra (PV max 6)",
       "« After Lilandra attacks Deathbird, spend a [energy] resource → attach this card to Lilandra »",
       [LIBERER, "Puzzle.PutIntoPlay('gs127')"], ["Puzzle.Attack('gs121')"],
       {"accroche_a": [["gs127", "gs121"]], "pv_max": [["gs121", 6], ["gs114", 16]]},
       cibles=["gs121", "gs114"], main_exclusive=["01088"]),
    _c("gs127 Royal Cape Response, TEMOIN : sans [energy] en main, la Cape reste sur Deathbird",
       "le cout « spend a [energy] resource » doit etre paye",
       [LIBERER, "Puzzle.PutIntoPlay('gs127')"], ["Puzzle.Attack('gs121')"],
       {"accroche_a": [["gs127", "gs114"]]}, cibles=["gs121", "gs114"], main_exclusive=["01090"]),
    _c("gs128 Shi'ar Crest : attachee a Deathbird, +1 MNG et Solide (steady)",
       "badge +1 SCH/THW (`desc.SCH+`) ; « Attached character gains steady »",
       ["Puzzle.PutIntoPlay('gs128')"], [],
       {"accroche_a": [["gs128", "gs114"]], "attributs_carte": [["gs114", "scheme", 1], ["gs114", "steady", 1]]}),
    _c("gs128 Shi'ar Crest Response : [mental] paye -> la Crete passe sur Lilandra (+1 CTR, Solide)",
       "« spend a [mental] resource → attach this card to Lilandra » ; badge +1 THW pour Lilandra",
       [LIBERER, "Puzzle.PutIntoPlay('gs128')"], ["Puzzle.Attack('gs121')"],
       {"accroche_a": [["gs128", "gs121"]], "attributs_carte": [["gs121", "thwart", 1], ["gs121", "steady", 1],
                                                                ["gs114", "scheme", 0]]},
       cibles=["gs121", "gs114"], main_exclusive=["01089"]),
    _c("gs128 Shi'ar Crest Boost : l'ennemi qui s'active (Deathbird) recoit une carte d'etat Tenace",
       "« Give the activating enemy a tough status card » (modele 52037)",
       [], ["Puzzle.Boost('gs128')"], {"statuts": [["gs114", "Tough"]]}),
    _c("gs129 Shi'ar Javelin : attache a Deathbird, +1 ATQ ; ses attaques gagnent Percant (le Tenace du heros saute, 3 degats)",
       "badge +1 ATK (`desc.ATK+`) ; « Attached character's attacks gain piercing and overkill » (modele 27147)",
       [HEROS, "Puzzle.PutIntoPlay('gs129')", "Puzzle.Tough('01001a')"] + DECK_NEUTRE, ["Puzzle.Attack('gs114')"],
       {"accroche_a": [["gs129", "gs114"]], "attributs_carte": [["gs114", "attack", 1]], "degats_identite": 3,
        "statuts_absents": [["01001a", "Tough"]]}, **SANS_DEFENSE),
    _c("gs129 Shi'ar Javelin Response : [physical] paye -> le Javelot passe sur Lilandra (+1 ATQ)",
       "« spend a [physical] resource → attach this card to Lilandra »",
       [LIBERER, "Puzzle.PutIntoPlay('gs129')"], ["Puzzle.Attack('gs121')"],
       {"accroche_a": [["gs129", "gs121"]], "attributs_carte": [["gs121", "attack", 1], ["gs114", "attack", 0]]},
       cibles=["gs121", "gs114"], main_exclusive=["01090"]),
    _c("gs129 Shi'ar Javelin Boost : l'attaque gagne Percant -> le Tenace du heros saute (ATQ 2 + 1 icone = 3 degats)",
       "« If this activation is an attack, it gains piercing and overkill » (modele 50160)",
       [HEROS, "Puzzle.Tough('01001a')"], ["Puzzle.Boost('gs129')"],
       {"degats_identite": 3, "statuts_absents": [["01001a", "Tough"]]}, **SANS_DEFENSE),
    # ============================================================== gs130 Araki / gs131 Jailor
    _c("gs130 Araki When Defeated : 2 menaces sur CHAQUE manigance (principale 0 -> 2, prison 7 -> 9)",
       "« Place 2 threat on each scheme in play »",
       ["Puzzle.PutIntoPlay('gs130')"], ["Puzzle.Damage('gs130', 9)"],
       {"menace": [["gs117b", 2], ["gs119", 9]], "hors_jeu": ["gs130"]}),
    _c("gs130 Araki Boost : 1 menace sur chaque manigance (prison 7 -> 8, principale 0 -> 1)",
       "« Place 1 threat on each scheme in play » ; heros : Deathbird ATTAQUE (une manigance a 2+1 acheverait 1B)",
       [HEROS], ["Puzzle.Boost('gs130')"], {"menace": [["gs119", 8], ["gs117b", 1]]}, main_exclusive=["01088"],
       **SANS_DEFENSE),
    _c("gs130 Araki Vulnerable : sonne, il est defausse (pas vaincu : aucune menace posee)",
       "base automatique `desc.Vulnerable`",
       ["Puzzle.PutIntoPlay('gs130')"], ["Puzzle.Stun('gs130')"],
       {"hors_jeu": ["gs130"], "menace": [["gs119", 7], ["gs117b", 0]]}),
    _c("gs127 Royal Cape revelee depuis le deck rencontre : elle s'attache a Deathbird",
       "« Attach to Deathbird » par le chemin reel de revelation (`AttachToFaceWhenPutIntoPlay`)",
       [], ["Puzzle.Reveal('gs127')"], {"accroche_a": [["gs127", "gs114"]]}),
    _c("gs131 Jailor When Defeated : 2 menaces retirees de la prison (7 -> 5)",
       "« Remove 2 threat from Imprisoned on Chandilar »",
       DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs131')"], ["Puzzle.Damage('gs131', 9)"],
       {"menace": [["gs119", 5]], "hors_jeu": ["gs131"]}),
    _c("gs131 Jailor Boost : 1 menace sur la prison (7 -> 8)",
       "« Place 1 threat on Imprisoned on Chandilar »",
       [HEROS], ["Puzzle.Boost('gs131')"], {"menace": [["gs119", 8], ["gs117b", 0]]}, main_exclusive=["01088"],
       **SANS_DEFENSE),
    _c("gs131 Jailor Retaliate 1 : le heros qui l'attaque subit 1 degat",
       "base automatique `desc.Retaliate`",
       [HEROS] + DECK_NEUTRE + ["Puzzle.PutIntoPlay('gs131')"], ["Puzzle.Attack('01001a')"], {"degats_identite": 1},
       cibles=["gs131"]),
    # ============================================================== gs132 / gs133 / gs134 manigances annexes
    _c("gs132 Private Audience : revelee avec 3[per_hero] menaces et l'icone Acceleration",
       "`desc.StartingThreat 3*`, `desc.Acceleration`",
       [], ["Puzzle.Reveal('gs132')"], {"menace": [["gs132", 3]], "icones": [["Acceleration", 1]]}),
    _c("gs132 Private Audience : un allie (Ch'od) ne peut pas attaquer le mechant (0 degat)",
       "« Allies cannot attack the villain » (modele 49039 Selene)",
       [LIBERER, "Puzzle.Reveal('gs132')"], ["Puzzle.Attack('gs122')"], {"degats": [["gs114", 0]]},
       cibles=["gs122", "gs114"]),
    _c("gs132 Private Audience, TEMOIN : sans elle, Ch'od frappe le mechant (3 degats)",
       "ligne de base du precedent",
       [LIBERER], ["Puzzle.Attack('gs122')"], {"degats": [["gs114", 3]]}, cibles=["gs122", "gs114"]),
    _c("gs132 Private Audience : un allie (Ch'od) ne peut pas contrer la manigance principale (2 menaces restent)",
       "« Allies cannot ... thwart the main scheme » (modele 55061 Puppet Master)",
       [LIBERER, "Puzzle.Reveal('gs132')", "Puzzle.SetThreat('gs117b', 2)"], ["Puzzle.Thwart('gs122')"],
       {"menace": [["gs117b", 2]]}, cibles=["gs122", "gs117b"]),
    _c("gs132 Private Audience, TEMOIN : sans elle, Ch'od contre la manigance principale (2 -> 1)",
       "ligne de base du precedent",
       [LIBERER, "Puzzle.SetThreat('gs117b', 2)"], ["Puzzle.Thwart('gs122')"],
       {"menace": [["gs117b", 1]]}, cibles=["gs122", "gs117b"]),
    _c("gs133 Tapping the M'kraan Force : revelee avec 2 + Hinder 2[per_hero] = 4 menaces, Amplify et Hazard",
       "`desc.StartingThreat 2`, `Hinder 2*`, `Amplify`, `Hazard`",
       [], ["Puzzle.Reveal('gs133')"], {"menace": [["gs133", 4]], "icones": [["Amplify", 1], ["Hazard", 1]]}),
    _c("gs133 Tapping When Defeated : 1 degat soigne sur chaque STARJAMMER en jeu (Ch'od 3 -> 2)",
       "« Heal 1 damage from each STARJAMMER ally in play »",
       [LIBERER, "Puzzle.Damage('gs122', 3)", "Puzzle.Reveal('gs133')"], ["Puzzle.SetThreat('gs133', 0)"],
       {"degats": [["gs122", 2]], "hors_jeu": ["gs133"]}, cibles=["gs122"]),
    _c("gs134 Tortured Prisoners : 1[per_hero] + 1 par STARJAMMER glisse (6) = 7 menaces, icone Crisis",
       "« Place 1 additional threat here for each STARJAMMER ally tucked under Imprisoned on Chandilar »",
       [], ["Puzzle.Reveal('gs134')"], {"menace": [["gs134", 7]], "icones": [["Crisis", 1]]}),
    _c("gs134 Tortured Prisoners : un seul STARJAMMER libere -> 1 + 5 = 6 menaces",
       "le compte suit les glisses, pas les six de depart",
       [LIBERER], ["Puzzle.Reveal('gs134')"], {"menace": [["gs134", 6]]}, cibles=["gs122"]),
    # ============================================================== gs135 / gs136 / gs137 traitrises
    _c("gs135 Birthright : pas de soutien Shi'ar Throne -> Deathbird manigance (principale 0 -> 2)",
       "« Otherwise, Deathbird schemes » ; deck neutre",
       DECK_NEUTRE, ["Puzzle.Reveal('gs135')"], {"menace": [["gs117b", 2]]}),
    _c("gs135 Birthright : le soutien Shi'ar Throne en jeu -> Deathbird attaque son controleur EN ALTER EGO (detournee sur Lilandra, 3 degats)",
       "« Deathbird attacks the player who controls it (even if that player is in alter ego form) » (modele 16114) ; "
       "l'Interruption forcee de Deathbird detourne l'attaque sur Lilandra (STARJAMMER) avec +1 ATQ",
       [LIBERER, "Puzzle.SetThreat('gs120a', 0)"] + DECK_NEUTRE, ["Puzzle.Reveal('gs135')"],
       {"degats": [["gs121", 3]], "menace": [["gs117b", 0]], "forme": "AlterEgo"}, cibles=["gs121"]),
    _c("gs135 Birthright Boost : Deathbird recoit une carte d'etat Tenace",
       "« Give Deathbird a tough status card »",
       [], ["Puzzle.Boost('gs135')"], {"statuts": [["gs114", "Tough"]]}),
    _c("gs136 Exemplar Punishment : 2 glisses (4 liberes), « 1 menace sur la principale » choisi 2 fois (0 -> 2)",
       "« For each STARJAMMER ally tucked ... choose to either take 1 indirect damage or place 1 threat on the main "
       "scheme » ; 4 liberes pour rester sous le seuil de 1B (3)",
       [LIBERER] * 4, ["Puzzle.Reveal('gs136')"], {"menace": [["gs117b", 2]], "degats_identite": 0, "nb_glisses": 2},
       choisir_option=["Place_1_threat_on_the_main_scheme"], cibles=["gs121", "gs122", "gs123", "gs124"]),
    _c("gs136 Exemplar Punishment : 6 glisses, « 1 degat indirect » choisi 6 fois (6 degats, principale a 0)",
       "l'autre branche du choix",
       [], ["Puzzle.Reveal('gs136')"], {"menace": [["gs117b", 0]], "degats_identite": 6},
       choisir_option=["Take_1_indirect_damage"]),
    _c("gs136 Exemplar Punishment : aucun glisse -> 2 menaces sur la prison (7 -> 9)",
       "« If there is no ally tucked under Imprisoned on Chandilar, place 2 threat on it » (lecture retenue : la prison, Q2)",
       ["Puzzle.AdvanceMainScheme(1)"] + [LIBERER] * 4 + ["Puzzle.SetThreat('gs118b', 5)"], ["Puzzle.Reveal('gs136')"],
       {"nb_glisses": 0, "menace": [["gs119", 9], ["gs118b", 0]]},
       cibles=["gs122", "gs123", "gs121", "gs124", "gs125", "gs126"]),
    _c("gs137 Sister's Deception : Lilandra en jeu attaque le joueur (2 degats), sans s'incliner, 1 degat consecutif",
       "« she attacks you (resolve her ATK against you without exhausting her, but with taking consequential damage) » "
       "(modele 22031 Old Rivals)",
       [LIBERER], ["Puzzle.Reveal('gs137')"],
       {"degats_identite": 2, "degats": [["gs121", 1]], "pret": ["gs121"], "menace": [["gs119", 6]]}, cibles=["gs121"]),
    _c("gs137 Sister's Deception : Lilandra pas en jeu -> 3 menaces sur la prison (7 -> 10)",
       "« Otherwise, place 3 threat on Imprisoned on Chandilar »",
       [], ["Puzzle.Reveal('gs137')"], {"menace": [["gs119", 10]], "degats_identite": 0}),
]

VERIFICATIONS = r'''
def _mv_prison(monde):
    for objet in monde.object_manager.card_dict.values():
        f = objet.face
        if f is not None and f.IsInPlay() and getattr(f.paper, "card_id", None) == "gs119":
            return f
    return None


def _mv_glisses(monde):
    prison = _mv_prison(monde)
    if prison is None:
        return None, []
    return prison, list(prison.GetPlacedCardArea().GetAll())


def mv_sonde(monde, aides):
    """SONDE de mise au point (jamais dans la batterie finale) : decrit l'etat, rend toujours False."""
    lignes = []
    for objet in monde.object_manager.card_dict.values():
        f = objet.face
        if f is None:
            continue
        cid = getattr(f.paper, "card_id", "")
        if not cid.startswith("gs"):
            continue
        lignes.append(f"{cid}:{type(f).__name__}:{getattr(f.card.area, 'deck_type', '?')}"
                      f":jeu={f.IsInPlay()}:up={f.IsFaceUp()}:menace={getattr(f, 'threat', None)}"
                      f":pv={getattr(f, 'health', None)}"
                      f":incl={f.IsExhaust() if f.IsInPlay() and hasattr(f, 'IsExhaust') else '-'}")
    lignes.append(f"fin={monde.is_game_over}")
    return False, " | ".join(sorted(lignes))


def mv_etat(monde, aides):
    """etat_attendu (cles communes) + les cles propres au scenario Majestrix's Verdict :
    glisses (liste exacte des card_id glisses sous la prison), glisses_visibles, sous_controle (en jeu sous le
    controle d'un joueur), retires (zone des cartes retirees de la partie), defaite, victoire, mechant_id,
    principale (card_id de la manigance principale en jeu), allies_comptes, boosts_recus."""
    attendu = aides["cas"].get("attendu") or {}
    connues = set(CLES_ETAT_ATTENDU) | {"glisses", "glisses_visibles", "sous_controle", "retires", "defaite",
                                        "victoire", "mechant_id", "principale", "allies_comptes", "nb_glisses",
                                        "nb_retires"}
    inconnues = sorted(set(attendu) - connues)
    if inconnues:
        return False, f"cle(s) attendu INCONNUE(S) de mv_etat : {inconnues}"
    ok, message = etat_attendu(monde, aides)
    soucis = [] if ok else [message]
    prison, glisses = _mv_glisses(monde)
    ids = sorted(getattr(f.paper, "card_id", "?") for f in glisses)
    if "glisses" in attendu and ids != sorted(attendu["glisses"]):
        soucis.append(f"glisses sous la prison = {ids} (attendu {sorted(attendu['glisses'])}, prison en jeu = {prison is not None})")
    if attendu.get("glisses_visibles") and any(not f.IsFaceUp() for f in glisses):
        soucis.append("une carte glissee est FACE CACHEE (le livret p.4 la veut face visible)")
    for card_id in attendu.get("sous_controle") or []:
        face = aides["par_id"](monde, card_id)
        controle = face.GetControlBy() if face is not None else None
        if face is None or controle is None or not controle.IsPlayer():
            soucis.append(f"{card_id} n'est pas en jeu sous le controle d'un joueur")
    if "nb_glisses" in attendu and len(ids) != attendu["nb_glisses"]:
        soucis.append(f"glisses sous la prison = {ids} (attendu {attendu['nb_glisses']})")
    retirees = [getattr(f.paper, "card_id", None) for f in monde.area_removed.GetAll()]
    starjammers_retires = [c for c in retirees if c in ("gs121", "gs122", "gs123", "gs124", "gs125", "gs126")]
    if "nb_retires" in attendu and len(starjammers_retires) != attendu["nb_retires"]:
        soucis.append(f"STARJAMMER retires de la partie = {starjammers_retires} (attendu {attendu['nb_retires']})")
    for card_id in attendu.get("retires") or []:
        if card_id not in retirees:
            soucis.append(f"{card_id} n'est pas retire de la partie (retirees = {retirees})")
    if "defaite" in attendu:
        perdu = bool(monde.is_game_over) and not monde.game_over.players_won
        if perdu != attendu["defaite"]:
            soucis.append(f"defaite = {perdu} (attendu {attendu['defaite']}, partie terminee = {monde.is_game_over})")
    if "victoire" in attendu:
        gagne = bool(monde.is_game_over) and bool(monde.game_over.players_won)
        if gagne != attendu["victoire"]:
            soucis.append(f"victoire = {gagne} (attendu {attendu['victoire']}, partie terminee = {monde.is_game_over})")
    if "mechant_id" in attendu:
        from game.operate.worlds import Worlds
        vilains = [getattr(v.paper, "card_id", None) for v in Worlds.GetAllVillains(monde)]
        if attendu["mechant_id"] not in vilains:
            soucis.append(f"mechant en jeu = {vilains} (attendu {attendu['mechant_id']})")
    if "principale" in attendu:
        from game.operate.worlds import Worlds
        mains = [getattr(m.paper, "card_id", None) for m in Worlds.GetAllMainSchemes(monde)]
        if attendu["principale"] not in mains:
            soucis.append(f"manigance principale = {mains} (attendu {attendu['principale']})")
    if "allies_comptes" in attendu:
        from game.message import Message
        joueur = monde.players[0]
        n = 0
        for allie in joueur.GetControlAllies():
            m = Message.CheckIfAllyCountLimit(allie)
            m.Send()
            if not m.not_count:
                n += 1
        if n != attendu["allies_comptes"]:
            soucis.append(f"allies comptes dans la limite = {n} (attendu {attendu['allies_comptes']})")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "ok"


def mv_etape_un(monde, aides):
    """Envoie la fin de l'ETAPE 1 de la phase du mechant (`AfterResolveVillainPhaseStep(1)`, world.py:758),
    exactement comme `process_villain_phase_step`, puis mesure par mv_etat."""
    from game.message import Message
    debut = Message.WhenVillainPhaseStepStart(1, monde)
    debut.Send()
    Message.AfterResolveVillainPhaseStep(1, debut).Send()
    return mv_etat(monde, aides)
'''
