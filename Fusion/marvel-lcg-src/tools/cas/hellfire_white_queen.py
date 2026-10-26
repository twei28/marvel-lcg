# Cas test_capacites du scenario 1 « WHITE QUEEN » de la campagne Hellfire Hunt (Dipsome), prefixe `hf` : noms prefixes « [hf] » puis le card_id.
#
# Rappels de montage :
#  - `spider_man` demarre en ALTER-EGO : `Puzzle.ChangeForm('01001a')` le passe en HEROS (le vilain ATTAQUE un heros, MANIGANCE contre un alter ego) ;
#  - le vilain et le complot sont ceux du scenario : White Queen A1 (hf101a) et Infiltrating the Mansion (hf104b, menace 0, cible 2 par heros) ;
#  - `Puzzle.BeginVillainPhase()` fait activer le vilain : il recoit UNE carte de boost avant son attaque ou son complot. Pour mesurer ce qui se passe
#    APRES, le deck de rencontre est refait : [carte de boost inoffensive 01105, carte voulue, ...] ;
#  - 01105 = « Bomb Scare » (aucune capacite de boost), utilisee comme remplissage par les autres packs.
SC = "hellfire_white_queen"
SCX = "hellfire_white_queen_expert"
HEROS = "Puzzle.ChangeForm('01001a')"   # spider_man demarre en ALTER-EGO
REMPLI = "'01105'"


def deck(*cartes, remplissage=6):
    """Deck de rencontre de test, les cartes voulues listees DU DESSUS vers le dessous, puis du remplissage inoffensif.
    ⚠ `Puzzle.CreateEncounterDeck(a, b, c)` pose `a` en DERNIER : la derniere carte creee est le DESSUS du deck (mesure le 26/10/2026) ;
    on inverse donc la liste."""
    ids = list(cartes) + ["01105"] * remplissage
    return ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join("'%s'" % c for c in reversed(ids))]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[hf] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": ["Puzzle.EmptyHand()"] + list(mise), "declencher": declencher,
           "verifier": cle.pop("verifier", "hf_etat"), "attendu": attendu}
    cas.update(cle)
    # La main de depart (4 cartes de Spider-Man) fausse les mesures (le pilote joue « Great Responsibility » en remplacement d'une pose de menace) :
    # une seule ressource inoffensive, sauf demande contraire.
    cas.setdefault("main_exclusive", ["01090"])
    return cas


CAS = [
    # ===================================================================== le scenario se monte
    _c("hf104a mise en place : White Queen (PSIONIC) en jeu, PV 12, complot 1B a 0 menace",
       "le scenario `hellfire_white_queen` se charge : vilain hf101a, complot hf104b, cartes imprimees (nombres texte <-> code)",
       deck("01105"), [],
       {"en_jeu": ["hf101a", "hf104b"], "vie": [["hf101a", 12]], "attaque": [["hf101a", 1]],
        "trait_de": [["hf101a", "PSIONIC", True], ["hf101a", "DIAMOND", False], ["hf101a", "HELLFIRE", True]],
        "menace_de": [["hf104b", 0]]}),

    # ===================================================================== forme A : hf101a / hf102a / hf103a
    _c("hf101a Reponse forcee : apres l'attaque, defausse le dessus ; une carte ILLUSION est revelee ; White Queen se retourne (PV et degats conserves)",
       "« After White Queen attacks you, discard the top card of the encounter deck. If that card has the ILLUSION trait, reveal it. Flip White Queen » : "
       "le heros est en forme HEROS (le vilain attaque) ; la 1re carte est la carte de boost de l'attaque, la 2e (Illusory Sentinel, ILLUSION) est defaussee puis revelee",
       [HEROS, "Puzzle.Damage('hf101a', 5)"] + deck("01105", "hf112"), ["Puzzle.Attack('hf101a')"],
       {"en_jeu": ["hf101b", "hf112"], "absents": ["hf101a"], "degats_de": [["hf101b", 5]], "vie": [["hf101b", 12]],
        "trait_de": [["hf101b", "DIAMOND", True], ["hf101b", "PSIONIC", False]]}),
    _c("hf101a Reponse forcee : CONTRE-CAS, la carte defaussee n'a pas le trait ILLUSION -> rien n'est revele mais White Queen se retourne quand meme",
       "la parenthese imprimee « (whether that card had the ILLUSION trait or not) » : le retournement est inconditionnel",
       [HEROS] + deck("01105", "01105"), ["Puzzle.Attack('hf101a')"],
       {"en_jeu": ["hf101b"], "absents": ["hf101a", "hf112"]}),
    # ===================================================================== forme B : hf101b / hf102b / hf103b
    _c("hf101b Reponse forcee : apres son complot (le heros est en ALTER-EGO), White Queen se retourne sur sa forme PSIONIC",
       "« After White Queen schemes, flip this card » : contre un alter-ego le vilain MANIGANCE ; degats conserves au retour sur la forme A",
       ["Puzzle.Flip('hf101a')", "Puzzle.Damage('hf101b', 3)"] + deck("01105"), ["Puzzle.Scheme('hf101b')"],
       {"en_jeu": ["hf101a"], "absents": ["hf101b"], "degats_de": [["hf101a", 3]]}),
    _c("hf101b Interruption forcee : l'attaque du heros (2) est reduite du nombre d'icones de boost defaussees (Psionic Active : 3) -> 0 degat",
       "« Reduce damage from that attack by the number of boost icons discarded this way » : hf120 porte 3 icones",
       [HEROS, "Puzzle.Flip('hf101a')"] + deck("hf120"), ["Puzzle.Attack('01001a')"],
       {"en_jeu": ["hf101b"], "degats_de": [["hf101b", 0]]}, cibles=["hf101b"], accepter_choix=True),
    _c("hf101b Interruption forcee : TEMOIN, la carte defaussee n'a aucune icone -> les 2 degats passent",
       "meme montage avec Bomb Scare (aucune icone de boost) : 2 degats",
       [HEROS, "Puzzle.Flip('hf101a')"] + deck("01105"), ["Puzzle.Attack('01001a')"],
       {"en_jeu": ["hf101b"], "degats_de": [["hf101b", 2]]}, cibles=["hf101b"], accepter_choix=True),
    # ===================================================================== le stade suivant est revele dans la MEME forme (livret p. 8)
    _c("hf101a stade vaincu en forme PSIONIC : le stade 2 est revele en forme PSIONIC (hf102a), PV remis au stade 15",
       "« Revealing her in the same form as the one she defeated » : la face qui partage le plus de traits avec la forme vaincue",
       deck("01105"), ["Puzzle.Damage('hf101a', 12)"],
       {"en_jeu": ["hf102a"], "absents": ["hf101a", "hf101b", "hf102b"], "vie": [["hf102a", 15]], "degats_de": [["hf102a", 0]]}),
    _c("hf101b stade vaincu en forme DIAMOND : le stade 2 est revele en forme DIAMOND (hf102b)",
       "meme regle, forme B : la face B du stade 2 est la face visible",
       ["Puzzle.Flip('hf101a')"] + deck("01105"), ["Puzzle.Damage('hf101b', 12)"],
       {"en_jeu": ["hf102b"], "absents": ["hf101a", "hf101b", "hf102a"], "vie": [["hf102b", 15]], "degats_de": [["hf102b", 0]]}),
    _c("hf102b stade 2 forme DIAMOND : Steady et Retaliate 1 imprimes (desc)",
       "nombres texte <-> code : ATK 3, SCH 1, PV 15, Steady, Retaliate 1",
       ["Puzzle.Flip('hf101a')", "Puzzle.Damage('hf101b', 12)"] + deck("01105"), [],
       {"en_jeu": ["hf102b"], "attaque": [["hf102b", 3]], "vie": [["hf102b", 15]], "steady": ["hf102b"]}),

    # ===================================================================== stade 3 (mode expert) : Incite 1 a chaque retour en PSIONIC
    _c("hf103a Incite 1 : White Queen B3 -> A3 apres son complot : +1 menace sur le complot : 1 du complot + 1 d'incitation = 2 = le seuil du stade 1, qui est donc COMPLETE",
       "livret p. 8 : « incite 1 ... place threat on the main scheme when she flips back to the PSIONIC form everytime » ; le temoin ci-dessous reste a 1 (stade non complete)",
       ["Puzzle.Damage('hf102a', 15)", "Puzzle.Flip('hf103a')"] + deck("01105"), ["Puzzle.Scheme('hf103b')"],
       {"en_jeu": ["hf105b"], "absents": ["hf104b"]}, scenario=SCX),
    _c("hf103a Incite 1 : TEMOIN, stade 2 (B2 -> A2 apres son complot) : pas d'incitation, 1 seule menace",
       "contre-cas : seul le stade 3 porte Incite",
       ["Puzzle.Flip('hf102a')"] + deck("01105"), ["Puzzle.Scheme('hf102b')"],
       {"en_jeu": ["hf102a"], "menace_de": [["hf104b", 1]]}, scenario=SCX),
    # ===================================================================== complots principaux
    _c("hf104b When Completed : la menace atteint le seuil -> White Queen se retourne (DIAMOND), 1 jeton d'acceleration, le moteur avance au stade 2",
       "« When Completed : Flip White Queen and place 1 acceleration token here » ; le jeton passe au stade suivant (AdvanceMainScheme) ; hf105a cherche Crystalline Adaptation",
       deck("hf107", "01105"), ["Puzzle.PlaceThreat('hf104b', 2)"],
       {"en_jeu": ["hf101b", "hf105b", "hf107"], "absents": ["hf104b", "hf101a"], "attache": [["hf107", "hf101b"]], "acceleration": [["hf105b", 1]]}),
    _c("hf104b Reponse forcee : le round finit sans que le seuil soit atteint -> le complot avance au stade 2 (White Queen ne se retourne PAS)",
       "« After the round ends, advance to stage 2A » : le stade 1 dure au plus un round",
       deck("hf107", "01105"), ["Puzzle.SendAfterRoundEnd()"],
       {"en_jeu": ["hf101a", "hf105b", "hf107"], "absents": ["hf104b"], "attache": [["hf107", "hf101a"]], "acceleration": [["hf105b", 0]]}),
    _c("hf105b When Completed : White Queen se retourne, puis le stade 3 : Mutant Supremacy est cherche et revelee (hf106a)",
       "« When Completed : Flip White Queen » + 3A « When Revealed : search ... for the Mutant Supremacy side scheme and reveal it »",
       deck("hf124", "hf107", "01105"), ["Puzzle.PlaceThreat('hf104b', 2)", "Puzzle.PlaceThreat('hf105b', 9)"],
       {"en_jeu": ["hf106b", "hf124", "hf101a"], "absents": ["hf105b", "hf101b"]}),
    _c("hf106b stade 3 complete : « the players lose the game »",
       "« If this stage is completed, the players lose the game » : texte imprime lu par le moteur",
       deck("hf124", "hf107", "01105"), ["Puzzle.PlaceThreat('hf104b', 2)", "Puzzle.PlaceThreat('hf105b', 9)", "Puzzle.PlaceThreat('hf106b', 5)"],
       {"gagnee": False, "partie_finie": True}),

    # ===================================================================== hf107 Crystalline Adaptation
    _c("hf107 revelee : s'attache a White Queen, +1 ATQ (valeur imprimee ATK+ 1)",
       "« Attach to White Queen » ; le bonus +1 ATK / +1 SCH vient de `desc` (has_modify)",
       deck("hf107", "01105"), ["Puzzle.Reveal('hf107')"],
       {"en_jeu": ["hf107"], "attache": [["hf107", "hf101a"]], "attaque": [["hf101a", 2]]}),
    _c("hf107 Max 1 par ennemi : un SECOND exemplaire ne s'attache pas et gagne surge (la carte suivante, Illusory Sentinel, est revelee)",
       "« Max 1 per enemy. Attach to White Queen. Otherwise, this card gains surge. »",
       ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', 'hf112', 'hf107', 'hf107')", "Puzzle.Reveal('hf107')"],
       ["Puzzle.Reveal('hf107')"],
       {"nb_en_jeu": [["hf107", 1]], "en_jeu": ["hf112"], "attache": [["hf107", "hf101a"]]}),
    _c("hf107 Interruption forcee : White Queen PSIONIC est attaquee -> elle se retourne (DIAMOND) et la carte est defaussee",
       "« When White Queen is attacked, if she is in PSIONIC form, flip her and discard this card »",
       [HEROS] + deck("hf107", "01105"), ["Puzzle.Reveal('hf107')", "Puzzle.Attack('01001a')"],
       {"en_jeu": ["hf101b"], "absents": ["hf101a", "hf107"]}, cibles=["hf101a"], accepter_choix=True),
    _c("hf107 Interruption forcee : TEMOIN, White Queen DIAMOND attaquee -> rien (la carte reste attachee)",
       "la condition « if she is in PSIONIC form » : une forme DIAMOND ne se retourne pas",
       [HEROS, "Puzzle.Flip('hf101a')"] + deck("hf107", "01105"), ["Puzzle.Reveal('hf107')", "Puzzle.Attack('01001a')"],
       {"en_jeu": ["hf101b", "hf107"], "attache": [["hf107", "hf101b"]]}, cibles=["hf101b"], accepter_choix=True),
    _c("hf107 Boost : White Queen DIAMOND active (attaque) avec Crystalline en boost -> elle se retourne et 2 menaces sur le complot (stade 2 : 2 -> 4)",
       "« After this activation, if White Queen is in DIAMOND form, flip her and place 2 threat on the main scheme » ; le complot est avance au stade 2 (cible 9) pour ne pas etre complete",
       [HEROS, "Puzzle.PlaceThreat('hf104b', 2)"] + deck("hf107", "01105"), ["Puzzle.Attack('hf101b')"],
       {"en_jeu": ["hf101a"], "absents": ["hf101b"], "menace_de": [["hf105b", 4]]}),
    _c("hf107 Boost : TEMOIN, meme activation avec une carte sans effet -> pas de retournement, menace inchangee (2)",
       "contre-cas : la meme attaque avec Bomb Scare en boost",
       [HEROS, "Puzzle.PlaceThreat('hf104b', 2)"] + deck("01105", "01105"), ["Puzzle.Attack('hf101b')"],
       {"en_jeu": ["hf101b"], "menace_de": [["hf105b", 2]]}),
    # ===================================================================== hf110 Psionic Feedback
    _c("hf110 revelee : s'attache a White Queen, +1 ATQ et +1 SCH",
       "« Attach to White Queen » ; ATK+ 1 / SCH+ 1 imprimes",
       deck("hf110", "01105"), ["Puzzle.Reveal('hf110')"],
       {"en_jeu": ["hf110"], "attache": [["hf110", "hf101a"]], "attaque": [["hf101a", 2]]}),
    _c("hf110 Reponse forcee : apres que White Queen se retourne, elle recoit 1 carte de boost face cachee",
       "« After White Queen flips, give her 1 facedown boost card »",
       deck("hf110", "01105", "01105"), ["Puzzle.Reveal('hf110')", "Puzzle.Flip('hf101a')"],
       {"en_jeu": ["hf101b", "hf110"], "boosts_de": [["hf101b", 1]]}),
    _c("hf110 Action de heros : depenser [mental][physical] -> la carte est defaussee",
       "« Hero Action : Spend [mental][physical] resources -> discard this card » : 01089 Genius ([mental]) et 01090 Strength ([physical]) en main",
       [HEROS] + deck("hf110", "01105"), ["Puzzle.Reveal('hf110')", "Puzzle.Action('hf110', 'HeroAction')"],
       {"absents": ["hf110"], "en_jeu": ["hf101a"]}, main_exclusive=["01089", "01090"], payer_avec=["01089", "01090"], payer_tout=True, accepter_choix=True),
    _c("hf110 Boost : « Reveal this card » : la carte de boost est revelee et s'attache a White Queen",
       "« [star] Boost : Reveal this card » (modele 04084)",
       [HEROS] + deck("hf110", "01105"), ["Puzzle.Attack('hf101a')"],
       {"en_jeu": ["hf110"], "attache": [["hf110", "hf101b"]]}),
    # ===================================================================== hf111 Psionic Maelstrom
    _c("hf111 revelee en forme PSIONIC : 2 compteurs illusion (1 de Uses + 1 en plus)",
       "« Uses (1 illusion counter). When Revealed : if White Queen is in PSIONIC form, place 1 additional illusion counter here »",
       deck("hf111", "01105"), ["Puzzle.Reveal('hf111')"],
       {"en_jeu": ["hf111"], "attache": [["hf111", "hf101a"]], "compteurs_sur": [["hf111", "illusion", 2]]}),
    _c("hf111 revelee en forme DIAMOND : 1 seul compteur illusion",
       "contre-cas : pas de compteur en plus",
       ["Puzzle.Flip('hf101a')"] + deck("hf111", "01105"), ["Puzzle.Reveal('hf111')"],
       {"en_jeu": ["hf111"], "attache": [["hf111", "hf101b"]], "compteurs_sur": [["hf111", "illusion", 1]]}),
    _c("hf111 Reponse forcee : apres l'attaque de White Queen, X degats indirects (X = 2 cartes ILLUSION en jeu : Maelstrom + Phantom Warrior) et -1 compteur",
       "« take X indirect damage, where X is equal to the number of ILLUSION cards in play. Remove 1 illusion counter from here » ; le heros DEFEND l'attaque (0 degat) : les 2 degats sont les degats indirects",
       [HEROS, "Puzzle.PutIntoPlay('hf114')"] + deck("01105", "01105"), ["Puzzle.Reveal('hf111')", "Puzzle.Attack('hf101a')"],
       {"degats_identite": 2, "compteurs_sur": [["hf111", "illusion", 1]]}),
    _c("hf111 Reponse forcee : TEMOIN, un seul ILLUSION en jeu (Maelstrom seul) -> 1 degat indirect",
       "contre-cas du nombre X", [HEROS] + deck("01105", "01105"), ["Puzzle.Reveal('hf111')", "Puzzle.Attack('hf101a')"],
       {"degats_identite": 1, "compteurs_sur": [["hf111", "illusion", 1]]}),
    _c("hf111 Uses : le dernier compteur retire fait quitter la carte (forme DIAMOND : 1 compteur -> 0)",
       "mot-cle Uses natif : la carte est defaussee quand le dernier pion est retire",
       [HEROS, "Puzzle.Flip('hf101a')"] + deck("01105", "01105"), ["Puzzle.Reveal('hf111')", "Puzzle.Attack('hf101b')"],
       {"absents": ["hf111"]}),
    # ===================================================================== hf112 Illusory Sentinel
    _c("hf112 revele : valeurs imprimees (PV 3, ATK 2, SCH 1), Steady, Quickstrike : il attaque des qu'il est engage (2 degats)",
       "nombres texte <-> code (scan) ; Quickstrike lu dans `desc` : « After this minion engages your HERO, it attacks » : heros en forme heros mais incline (il ne peut pas defendre)",
       [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf112", "01105"), ["Puzzle.Reveal('hf112')"],
       {"en_jeu": ["hf112"], "vie": [["hf112", 3]], "attaque": [["hf112", 2]], "steady": ["hf112"], "degats_identite": 2}),
    _c("hf112 Boost : l'activation du vilain est une attaque -> +2 icones de boost (3 en tout : 1 imprimee + 2) : 1 + 3 = 4 degats",
       "« [star] Boost : If this activation is an attack, this card gets +2 boost icons for this activation »",
       deck("hf112", "01105"), ["Puzzle.Attack('hf101a')"],
       {"degats_identite": 4}),
    _c("hf112 Boost : TEMOIN, meme attaque avec Bomb Scare en boost : 1 degat",
       "contre-cas de la ligne du dessus",
       deck("01105", "01105"), ["Puzzle.Attack('hf101a')"],
       {"degats_identite": 1}),
    # ===================================================================== hf114-hf117 Phantom Warrior
    _c("hf114 Phantom Warrior en boost : entre en jeu engage avec le joueur ; Guard + Steady + Toughness imprimes",
       "« [star] Boost : Put Phantom Warrior into play engaged with you » (modele 01121)",
       [HEROS] + deck("hf114", "01105"), ["Puzzle.Attack('hf101a')"],
       {"en_jeu": ["hf114"], "vie": [["hf114", 2]], "steady": ["hf114"]}),
    _c("hf115 Phantom Warrior (illustration 2) : meme effet",
       "les quatre illustrations portent le meme texte",
       [HEROS] + deck("hf115", "01105"), ["Puzzle.Attack('hf101a')"], {"en_jeu": ["hf115"]}),
    _c("hf116 Phantom Warrior (illustration 3) : meme effet",
       "idem", [HEROS] + deck("hf116", "01105"), ["Puzzle.Attack('hf101a')"], {"en_jeu": ["hf116"]}),
    _c("hf117 Phantom Warrior (illustration 4) : meme effet",
       "idem", [HEROS] + deck("hf117", "01105"), ["Puzzle.Attack('hf101a')"], {"en_jeu": ["hf117"]}),

    # ===================================================================== hf118 Fractured Loyalties
    _c("hf118 : l'allie PRET (Mockingbird, ATK 1) attaque le joueur, s'incline et prend les degats consequents",
       "« Choose an ally you control. It makes a basic attack against you (with exhausting and taking the consequential damage) » : le heros (incline) ne defend pas",
       [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('01083', under_control=True)"] + deck("hf118", "01105"), ["Puzzle.Reveal('hf118')"],
       {"exhausted": ["01083"], "degats_identite": 1}),
    _c("hf118 : sans allie, la carte gagne surge (la carte suivante, Illusory Sentinel, est revelee)",
       "« If no attack was made this way, this card gains surge »",
       deck("hf118", "hf112", "01105"), ["Puzzle.Reveal('hf118')"],
       {"en_jeu": ["hf112"]}),
    _c("hf118 : TEMOIN, un allie deja INCLINE ne peut pas attaquer : surge",
       "l'attaque exige d'incliner l'allie",
       ["Puzzle.PutIntoPlay('01083', under_control=True, exhaust=True)"] + deck("hf118", "hf112", "01105"), ["Puzzle.Reveal('hf118')"],
       {"en_jeu": ["hf112"], "degats_identite": 0}),
    # ===================================================================== hf120 Psionic Active
    _c("hf120 forme DIAMOND, heros en forme HEROS : White Queen attaque (ATK 2 de la forme B)",
       "« If White Queen is in DIAMOND form, she attacks you » : le heros incline ne defend pas",
       [HEROS, "Puzzle.Exhaust('01001a')", "Puzzle.Flip('hf101a')"] + deck("hf120", "01105"), ["Puzzle.Reveal('hf120')"],
       {"degats_identite": 2}),
    _c("hf120 forme DIAMOND, heros en ALTER-EGO : le joueur PEUT incliner son identite et prendre 1 degat pour annuler l'attaque",
       "« you may choose to exhaust your identity and take 1 damage to cancel this attack » : option acceptee",
       ["Puzzle.Flip('hf101a')"] + deck("hf120", "01105"), ["Puzzle.Reveal('hf120')"],
       {"degats_identite": 1, "exhausted": ["01001b"]}, accepter_choix=True),
    _c("hf120 forme DIAMOND, ALTER-EGO : option refusee -> l'attaque a lieu (2 degats)",
       "contre-cas : sans accepter, l'attaque n'est pas annulee",
       ["Puzzle.Flip('hf101a')"] + deck("hf120", "01105"), ["Puzzle.Reveal('hf120')"],
       {"degats_identite": 2}, choisir_option="Cancel"),
    _c("hf120 forme PSIONIC : White Queen MANIGANCE (SCH 2 : le stade 1 est complete, le complot avance)",
       "« If White Queen is in PSIONIC form, she schemes » : 2 menaces = le seuil du stade 1",
       deck("hf120", "01105"), ["Puzzle.Reveal('hf120')"],
       {"absents": ["hf104b"], "en_jeu": ["hf105b"]}),
    # ===================================================================== hf122 Psionic Fortification
    _c("hf122 forme DIAMOND : soigne 1 degat de White Queen et lui donne une carte Tenace",
       "« If White Queen is in DIAMOND form, heal 1 damage from her and give her a tough status card »",
       ["Puzzle.Flip('hf101a')", "Puzzle.Damage('hf101b', 5)"] + deck("hf122", "01105"), ["Puzzle.Reveal('hf122')"],
       {"degats_de": [["hf101b", 4]], "statuts": [["hf101b", "Tough"]]}),
    _c("hf122 forme PSIONIC : soigne 3 degats et retire ses cartes Sonne et Desoriente",
       "« If she is in PSIONIC form, heal 3 damage from her and remove each stunned and confused status card from her »",
       ["Puzzle.Damage('hf101a', 5)", "Puzzle.Stun('hf101a')", "Puzzle.Confuse('hf101a')"] + deck("hf122", "01105"), ["Puzzle.Reveal('hf122')"],
       {"degats_de": [["hf101a", 2]], "statuts_absents": [["hf101a", "Stunned"], ["hf101a", "Confused"]]}),
    _c("hf122 Boost : « Give White Queen a tough status card »",
       "boost de l'activation du vilain",
       [HEROS] + deck("hf122", "01105"), ["Puzzle.Attack('hf101a')"],
       {"statuts": [["hf101b", "Tough"]]}),
    # ===================================================================== hf124 Mutant Supremacy
    _c("hf124 revelee : menace de depart 2 (2 par heros, 1 heros)",
       "valeur imprimee : « 2 [per hero] »",
       deck("hf124", "01105"), ["Puzzle.Reveal('hf124')"],
       {"en_jeu": ["hf124"], "menace_de": [["hf124", 2]]}),
    _c("hf124 Reponse forcee : apres que White Queen attaque ET blesse un personnage, il est Sonne",
       "« After White Queen attacks and damages a character, stun that character » : le heros incline ne defend pas, l'attaque (ATK 1) le blesse",
       [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf124", "01105", "01105"), ["Puzzle.Reveal('hf124')", "Puzzle.Attack('hf101a')"],
       {"statuts": [["01001a", "Stunned"]]}),
    _c("hf124 Reponse forcee : TEMOIN, l'attaque est defendue (0 degat) -> pas de Sonne",
       "« attacks and damages » : sans degat, rien",
       [HEROS] + deck("hf124", "01105", "01105"), ["Puzzle.Reveal('hf124')", "Puzzle.Attack('hf101a')"],
       {"statuts_absents": [["01001a", "Stunned"]]}),
    _c("hf124 Reponse forcee : apres que White Queen manigance contre le joueur, il est Desoriente",
       "« After White Queen schemes against you, you are confused » : alter-ego, White Queen forme A",
       deck("hf124", "01105", "01105"), ["Puzzle.Reveal('hf124')", "Puzzle.Scheme('hf101a')"],
       {"statuts": [["01001b", "Confused"]]}),
    _c("hf124 Boost : White Queen DIAMOND -> le joueur est Sonne",
       "« If White Queen is in DIAMOND form, you are stunned »",
       ["Puzzle.Flip('hf101a')"] + deck("hf124", "01105"), ["Puzzle.Attack('hf101b')"],
       {"statuts": [["01001b", "Stunned"]]}),
    _c("hf124 Boost : TEMOIN, White Queen PSIONIC -> pas Sonne",
       "contre-cas de la forme",
       deck("hf124", "01105"), ["Puzzle.Scheme('hf101a')"],
       {"statuts_absents": [["01001b", "Stunned"]]}),
    # ===================================================================== hf125 Telepathic Interrogation
    _c("hf125 revelee sans carte ILLUSION en jeu : menace 2",
       "« Place 2 additional threat here for each ILLUSION card in play » : aucune -> menace de depart seule (2)",
       deck("hf125", "01105"), ["Puzzle.Reveal('hf125')"],
       {"en_jeu": ["hf125"], "menace_de": [["hf125", 2]]}),
    _c("hf125 revelee avec UN Phantom Warrior (ILLUSION) en jeu : menace 2 + 2 = 4",
       "2 menaces en plus par carte ILLUSION",
       ["Puzzle.PutIntoPlay('hf114')"] + deck("hf125", "01105"), ["Puzzle.Reveal('hf125')"],
       {"menace_de": [["hf125", 4]]}),
    _c("hf125 Boost : White Queen PSIONIC -> le joueur est Desoriente",
       "« If the White Queen is in PSIONIC form, you are confused »",
       deck("hf125", "01105"), ["Puzzle.Scheme('hf101a')"],
       {"statuts": [["01001b", "Confused"]]}),
    _c("hf125 Boost : TEMOIN, White Queen DIAMOND -> pas Desoriente",
       "contre-cas de la forme",
       ["Puzzle.Flip('hf101a')"] + deck("hf125", "01105"), ["Puzzle.Scheme('hf101b')"],
       {"statuts_absents": [["01001b", "Confused"]]}),

    # ===================================================================== hf104a Setup : retirer les sbires White Queen
    _c("hf104a Setup : les deux sbires « White Queen » du module Perfection ne sont PAS dans le deck de rencontre au depart",
       "« Setup : Remove each minion named White Queen from the game » (montage natif du scenario, sans `deck()`)",
       [], [], {"en_jeu": ["hf101a"], "dans_deck_rencontre": ["hf303"], "hors_deck_rencontre": ["hf301", "hf302"]}),
    # ===================================================================== MODULE PERFECTION
    _c("hf301 White Queen (sbire DIAMOND) : n'entre JAMAIS en jeu : le joueur recoit une carte de rencontre face cachee et la carte est defaussee",
       "« Forced Interrupt : When a White Queen minion attempts to enter play, give the engaged player a facedown encounter card and discard this card »",
       deck("hf301", "01105", "01105"), ["Puzzle.Reveal('hf301')"],
       {"absents": ["hf301"], "distribuees": 1, "defausse_rencontre": ["hf301"]}),
    _c("hf302 White Queen (sbire PSIONIC) : revele la plus haute carte ILLUSION de la defausse (Astral Trap), puis n'entre pas en jeu",
       "« When Revealed : Reveal the topmost ILLUSION attachment in the encounter discard pile » + l'Interruption forcee d'entree en jeu",
       deck("hf302", "01105", "01105") + ["Puzzle.EmptyEncounterDiscardPile()", "Puzzle.MoveTo('hf303', 'EncounterDiscardPile')"], ["Puzzle.Reveal('hf302')"],
       {"en_jeu": ["hf303"], "absents": ["hf302"], "distribuees": 1}),
    _c("hf303 Astral Trap revelee (alter-ego) : s'attache a l'identite, 2 compteurs illusion car White Queen est PSIONIC",
       "« Attach to your identity. Uses (1 illusion counter). When Revealed : if the villain or a minion engaged with you has the PSIONIC trait, place 1 additional illusion counter »",
       deck("hf303", "01105"), ["Puzzle.Reveal('hf303')"],
       {"en_jeu": ["hf303"], "attache": [["hf303", "01001b"]], "compteurs_sur": [["hf303", "illusion", 2]]}),
    _c("hf303 Astral Trap : TEMOIN, White Queen DIAMOND (aucun PSIONIC) -> 1 seul compteur",
       "la condition PSIONIC", ["Puzzle.Flip('hf101a')"] + deck("hf303", "01105"), ["Puzzle.Reveal('hf303')"],
       {"compteurs_sur": [["hf303", "illusion", 1]]}),
    _c("hf303 Astral Trap : « Attached character cannot be healed » : 3 degats, 2 soins -> toujours 3 degats",
       "le soin de l'identite porteuse est REMPLACE par rien",
       ["Puzzle.Damage('01001b', 3)"] + deck("hf303", "01105"), ["Puzzle.Reveal('hf303')", "Puzzle.Heal('01001b', 2)"],
       {"degats_identite": 3}),
    _c("hf303 Astral Trap : TEMOIN, sans la carte le meme soin de 2 ramene a 1 degat",
       "contre-cas", ["Puzzle.Damage('01001b', 3)"] + deck("01105"), ["Puzzle.Heal('01001b', 2)"],
       {"degats_identite": 1}),
    _c("hf303 Astral Trap : Action d'alter-ego, incliner un personnage -> retire 1 compteur illusion (2 -> 1)",
       "« Alter-Ego Action : Exhaust a character you control -> remove 1 illusion counter from here »",
       deck("hf303", "01105"), ["Puzzle.Reveal('hf303')", "Puzzle.Action('hf303', 'AlterEgoAction')"],
       {"compteurs_sur": [["hf303", "illusion", 1]], "exhausted": ["01001b"]}, accepter_choix=True),
    _c("hf304 Illusory Defender revelee : s'attache a l'identite, 2 compteurs illusion (PSIONIC)",
       "memes regles d'attache et de compteurs que hf303",
       [HEROS] + deck("hf304", "01105"), ["Puzzle.Reveal('hf304')"],
       {"attache": [["hf304", "01001a"]], "compteurs_sur": [["hf304", "illusion", 2]]}),
    _c("hf304 Illusory Defender : « Attacks against you cannot be defended by allies » : Mockingbird ne PEUT PAS defendre contre White Queen",
       "`UnitCannotDefend` ; mesure par `IsCanDefense` (`Puzzle.Attack(..., defender)` DECLARE le defenseur sans consulter la regle)",
       [HEROS, "Puzzle.PutIntoPlay('01083', under_control=True)"] + deck("hf304", "01105"), ["Puzzle.Reveal('hf304')"],
       {"peut_defendre": [["01083", "hf101a", False]]}),
    _c("hf304 Illusory Defender : TEMOIN, sans la carte Mockingbird PEUT defendre",
       "contre-cas", [HEROS, "Puzzle.PutIntoPlay('01083', under_control=True)"] + deck("01105"), [],
       {"peut_defendre": [["01083", "hf101a", True]]}),
    _c("hf304 Illusory Defender : Reponse forcee apres l'attaque du vilain -> 1 compteur retire (2 -> 1)",
       "« After the villain attacks you, remove 1 illusion counter from here »",
       [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf304", "01105", "01105"), ["Puzzle.Reveal('hf304')", "Puzzle.Attack('hf101a')"],
       {"compteurs_sur": [["hf304", "illusion", 1]]}),
    _c("hf305 Psychic Mirage : « You cannot change form » : le heros reste en alter-ego",
       "`PlayersCannotChangeForms`", deck("hf305", "01105"), ["Puzzle.Reveal('hf305')", "Puzzle.ChangeForm('01001a')"],
       {"forme": "AlterEgo"}),
    _c("hf305 Psychic Mirage : TEMOIN, sans la carte le meme changement de forme passe (heros)",
       "contre-cas", deck("01105"), ["Puzzle.ChangeForm('01001a')"], {"forme": "Hero"}),
    _c("hf305 Psychic Mirage : « You cannot ready your identity » : incline puis `Ready` -> reste incline",
       "`CardCannotReady`", deck("hf305", "01105"), ["Puzzle.Reveal('hf305')", "Puzzle.Exhaust('01001b')", "Puzzle.Ready('01001b')"],
       {"exhausted": ["01001b"]}),
    _c("hf305 Psychic Mirage : Action, defausser une carte specifique a l'identite -> retire 1 compteur (2 -> 1)",
       "« Action : Discard an identity-specific card from your hand -> remove 1 illusion counter » : 01003 Backflip est une carte de Spider-Man",
       deck("hf305", "01105"), ["Puzzle.Reveal('hf305')", "Puzzle.Action('hf305', 'Action')"],
       {"compteurs_sur": [["hf305", "illusion", 1]], "defausse": ["01003"]}, main_exclusive=["01003"], accepter_choix=True),
    _c("hf306 Psionic Projection : une attaque de base du heros coute 1 ressource [mental] en plus ; Reponse forcee : -1 compteur apres l'attaque",
       "`AdditionalCostToAttack(Hero, Spend B)` ; « After your hero makes a basic attack or a basic thwart, remove 1 illusion counter »",
       [HEROS] + deck("hf306", "01105"), ["Puzzle.Reveal('hf306')", "Puzzle.Attack('01001a')"],
       {"compteurs_sur": [["hf306", "illusion", 1]], "defausse": ["01089"]}, main_exclusive=["01089"], payer_avec=["01089"], cibles=["hf101a"], accepter_choix=True),
    _c("hf307 Illusion Unraveled : quand un attachement ILLUSION est defausse, il est donne au vilain en boost face cachee et hf307 est defaussee",
       "« When an ILLUSION attachment is discarded, give that card to the villain as a facedown boost card. Discard this card. »",
       deck("hf307", "hf303", "01105", "01105"), ["Puzzle.Reveal('hf307')", "Puzzle.Reveal('hf303')", "Puzzle.Discard('hf303')"],
       {"absents": ["hf307", "hf303"], "boosts_de": [["hf101a", 1]]}),
    _c("hf308 Illusion Loop : +1 compteur sur chaque attachement ILLUSION qui en a (Astral Trap 2 -> 3) ; le vilain manigance",
       "« For each ILLUSION attachment in play, if it has any illusion counters on it, place 1 illusion counter on it. The villain schemes. »",
       deck("hf303", "hf308", "01105", "01105"), ["Puzzle.Reveal('hf303')", "Puzzle.Reveal('hf308')"],
       {"compteurs_sur": [["hf303", "illusion", 3]]}),
    _c("hf308 Illusion Loop Boost : un attachement ILLUSION sur l'identite -> le joueur est Desoriente",
       "« If there is at least one ILLUSION attachment attached to your identity, you are confused »",
       deck("hf303", "01105"), ["Puzzle.Reveal('hf303')"] + [], {}),
    # ===================================================================== MODULE HELLFIRE CONCLAVE
    _c("hf311 Black Bishop : apres avoir attaque ET blesse un personnage, il le Desoriente",
       "« [star] Forced Response : After Black Bishop attacks and damages a character, confuse that character »",
       deck("hf311", "01105"), ["Puzzle.Reveal('hf311')", "Puzzle.Attack('hf311')"],
       {"statuts": [["01001b", "Confused"]], "degats_identite": 1}),
    _c("hf311 Black Bishop Boost : « You are confused »",
       "boost de l'activation du vilain", deck("hf311", "01105"), ["Puzzle.Scheme('hf101a')"],
       {"statuts": [["01001b", "Confused"]]}),
    _c("hf312 White Bishop : Quickstrike + Hellfire Hunt (+1 ATK) -> apres avoir engage le heros incline il attaque (1) et le rend Sonne",
       "« [star] Forced Response : After White Bishop attacks and damages a character, stun that character » ; sans Hellfire Hunt son ATQ est 0 : aucun degat, donc aucun Sonne",
       [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf318", "hf312", "01105", "01105"), ["Puzzle.Reveal('hf318')"],
       {"en_jeu": ["hf312"], "attaque": [["hf312", 1]], "statuts": [["01001a", "Stunned"]]}),
    _c("hf312 White Bishop Boost : « You are stunned »",
       "boost de l'activation du vilain", deck("hf312", "01105"), ["Puzzle.Scheme('hf101a')"],
       {"statuts": [["01001b", "Stunned"]]}),
    _c("hf313 Hellfire Pawn (x4) : en boost, entre en jeu engage ; Guard, Patrol, Surge imprimes (PV 3, ATK 2)",
       "« [star] Boost : Put Hellfire Pawn into play engaged with you » (modele 01121)",
       [HEROS] + deck("hf313", "01105"), ["Puzzle.Attack('hf101a')"],
       {"en_jeu": ["hf313"], "vie": [["hf313", 3]], "attaque": [["hf313", 2]]}),
    _c("hf317 The Hellfire Conclave revelee : 9 menaces, dont 1 deplacee sur le complot principal par sbire ELITE HELLFIRE en jeu (Black Bishop)",
       "« When Revealed : Move 1 threat from here to the main scheme for each ELITE, HELLFIRE minion in play »",
       ["Puzzle.PutIntoPlay('hf311')"] + deck("hf317", "01105"), ["Puzzle.Reveal('hf317')"],
       {"menace_de": [["hf317", 8], ["hf104b", 1]]}),
    _c("hf317 The Hellfire Conclave : « Each HELLFIRE minion gains incite 1 » : un sbire HELLFIRE (Black Bishop) revele ensuite pose 1 menace sur le complot",
       "mot-cle Incite accorde aux sbires HELLFIRE tant que la carte est en jeu",
       deck("hf317", "hf311", "01105", "01105"), ["Puzzle.Reveal('hf317')", "Puzzle.Reveal('hf311')"],
       {"menace_de": [["hf104b", 1]]}),
    _c("hf317 The Hellfire Conclave : « Each player engaged with a HELLFIRE minion cannot thwart this scheme » : la contrarie echoue (9 menaces)",
       "`UnitCannotThwartTarget(\"EngagedIdentity\")`",
       [HEROS, "Puzzle.PutIntoPlay('hf313')", "Puzzle.Engage('hf313')"] + deck("hf317", "01105"), ["Puzzle.Reveal('hf317')", "Puzzle.Thwart('01001a')"],
       {"menace_de": [["hf317", 9]]}, cibles=["hf317"], accepter_choix=True),
    _c("hf318 Hellfire Hunt : « Each HELLFIRE minion gets +1 ATK » (Hellfire Pawn : 2 -> 3) ; chaque joueur cherche et met en jeu un sbire HELLFIRE engage",
       "`GiveKeywordToInPlayWhenApplyThis(CardFinder2(HELLFIRE, Minion), attack=1)` + recherche",
       deck("hf318", "hf313", "01105", "01105"), ["Puzzle.Reveal('hf318')"],
       {"en_jeu": ["hf313"], "attaque": [["hf313", 3]]}),
    # ===================================================================== MODULE PSIONIC DELUSION
    _c("hf321 Echoes of Enmity : revele le sbire ENNEMI du joueur (Vulture) et s'y attache",
       "« Search the encounter deck, discard pile, and set-aside area for your nemesis minion, then reveal that minion. Attach Echoes of Enmity to it. (Shuffle.) » : le sbire nemesis de Spider-Man est le Vautour (01167)",
       deck("hf321", "01105"), ["Puzzle.Reveal('hf321')"],
       {"en_jeu": ["hf321", "01167"], "attache": [["hf321", "01167"]]}),
    _c("hf321 Echoes of Enmity Boost : « Exhaust your identity »",
       "boost de l'activation du vilain", deck("hf321", "01105"), ["Puzzle.Scheme('hf101a')"],
       {"exhausted": ["01001b"]}),
    _c("hf322 Incite Fear : « You cannot resolve triggered abilities in your identity's printed text box » : l'Interruption Spider-Sense (pioche 1) ne part plus",
       "`PlayersCannotTriggerAbility(\"You\", \"TriggeredAbility\", on_which_card=\"YourIdentity\")` ; la main de depart (1 carte) reste a 1",
       [HEROS, "Puzzle.Exhaust('01001a')"] + deck("hf322", "01105", "01105"), ["Puzzle.Reveal('hf322')", "Puzzle.Attack('hf101a')"],
       {"en_jeu": ["hf322"], "taille_main": 1}),
    _c("hf322 Incite Fear : TEMOIN, sans la carte Spider-Sense pioche 1 (main 2)",
       "contre-cas", [HEROS, "Puzzle.Exhaust('01001a')"] + deck("01105", "01105"), ["Puzzle.Attack('hf101a')"],
       {"taille_main": 2}),
    _c("hf322 Incite Fear : Action, defausser 2 cartes au hasard de la main -> defausse cette carte",
       "« Action : Discard 2 cards at random from your hand -> discard this card »",
       deck("hf322", "01105"), ["Puzzle.Reveal('hf322')", "Puzzle.Action('hf322', 'Action')"],
       {"absents": ["hf322"], "taille_main": 0}, main_exclusive=["01090", "01089"], accepter_choix=True),
    _c("hf324 Mind Manipulation : s'attache a l'allie de plus petit COUT (Black Cat 2 plutot que Mockingbird 3), qui devient un sbire",
       "« Attach to the ally you control with the lowest cost » ; l'allie traite comme un sbire a la face generique `minion` (pic_id = l'allie d'origine)",
       ["Puzzle.PutIntoPlay('01083', under_control=True)", "Puzzle.PutIntoPlay('01002', under_control=True)"] + deck("hf324", "01105"), ["Puzzle.Reveal('hf324')"],
       {"en_jeu": ["hf324"], "hote_pic": [["hf324", "01002"]]}),
    _c("hf324 Mind Manipulation : sans allie, la carte gagne surge (la carte suivante, Illusory Sentinel, est revelee)",
       "« If you cannot, this card gains surge »", deck("hf324", "hf112", "01105"), ["Puzzle.Reveal('hf324')"],
       {"en_jeu": ["hf112"]}),
    _c("hf325 Veil of Mind's Mirage : revele le side scheme nemesis (Highway Robbery) et s'attache a l'identite ; fin de phase : 1 degat a l'identite",
       "« Find your nemesis side scheme, then reveal it ... Forced Response : After the player phase ends, if your nemesis side scheme is in play, deal 1 damage to your identity »",
       deck("hf325", "01105"), ["Puzzle.Reveal('hf325')"],
       {"en_jeu": ["hf325", "01166"], "attache": [["hf325", "01001b"]]}),
]

VERIFICATIONS = r'''
def hf_etat(monde, aides):
    """Extensions de `etat_attendu` (meme famille que bb_etat) : compteurs_sur [[id, nom, n]], menace_de [[id, n]], attaque [[id, n]], vie [[id, pv_max]],
    degats_de [[id, n]], statuts_sur [[id, 'stunned'|'tough'|'confused', n]], absents [ids hors jeu], trait_de [[id, TRAIT, bool]],
    attache [[carte, hote]], boosts_de [[id, n]] (cartes de boost face cachee sur la carte), le reste va a etat_attendu."""
    attendu = aides["cas"].get("attendu") or {}
    # FILET (26/10/2026) : le moteur AVALE les exceptions des scripts de cartes (PROCESSUS-CARTE etape 7, point 6) ; un cas ne doit donc JAMAIS passer
    # au vert si le journal contient une trace d'exception.
    try:
        import os as _os
        _journal = open(f"/tmp/capacites_{_os.environ.get('CAS_PREFIX', '')}{aides['index']}.log", encoding="utf-8", errors="replace").read()
        _trace = [l for l in _journal.splitlines() if "Traceback" in l]
    except Exception:
        _trace = []
    propres = ("compteurs_sur", "menace_de", "attaque", "vie", "degats_de", "statuts_sur", "absents", "trait_de", "attache", "boosts_de", "steady", "acceleration", "gagnee", "partie_finie", "nb_en_jeu", "distribuees", "hors_deck_rencontre", "peut_defendre", "hote_pic")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    copie = dict(aides); copie["cas"] = dict(aides["cas"]); copie["cas"]["attendu"] = reste
    ok, msg = etat_attendu(monde, copie)
    soucis = [] if ok else [msg]
    if _trace:
        soucis.append("le journal contient une exception avalee par le moteur (Traceback)")
    par_id = aides["par_id"]
    def face(cid):
        f = par_id(monde, cid)
        if f is None:
            soucis.append(f"{cid} n'est pas en jeu")
        return f
    for cid, hote in attendu.get("attache", []):
        f = face(cid)
        if f is not None:
            b = f.bind_face
            got = getattr(getattr(b, "paper", None), "card_id", None) if b else None
            if got != hote:
                soucis.append(f"{cid} attache a {got} (attendu {hote})")
    for cid, nom, n in attendu.get("compteurs_sur", []):
        f = face(cid)
        if f is not None and f.GetCounters(nom) != n:
            soucis.append(f"{cid} compteurs {nom} = {f.GetCounters(nom)} (attendu {n})")
    for cid, n in attendu.get("menace_de", []):
        f = face(cid)
        if f is not None and f.threat != n:
            soucis.append(f"{cid} menace = {f.threat} (attendu {n})")
    for cid, n in attendu.get("attaque", []):
        f = face(cid)
        if f is not None and f.attack != n:
            soucis.append(f"{cid} ATK = {f.attack} (attendu {n})")
    for cid, n in attendu.get("vie", []):
        f = face(cid)
        if f is not None and f.max_health != n:
            soucis.append(f"{cid} PV max = {f.max_health} (attendu {n})")
    for cid, n in attendu.get("degats_de", []):
        f = face(cid)
        if f is not None and (f.max_health - f.health) != n:
            soucis.append(f"{cid} degats = {f.max_health - f.health} (attendu {n})")
    for cid, st, n in attendu.get("statuts_sur", []):
        f = face(cid)
        if f is not None and getattr(f, st) != n:
            soucis.append(f"{cid} statut {st} = {getattr(f, st)} (attendu {n})")
    for cid in attendu.get("absents", []):
        if par_id(monde, cid) is not None:
            soucis.append(f"{cid} est encore en jeu")
    for cid, tr, b in attendu.get("trait_de", []):
        f = face(cid)
        if f is not None and bool(f.HasTrait(tr)) != b:
            soucis.append(f"{cid} trait {tr} = {f.HasTrait(tr)} (attendu {b})")
    for cid, n in attendu.get("boosts_de", []):
        f = face(cid)
        if f is not None:
            vus = f.components.boostable.GetDeck().GetSize()
            if vus != n:
                soucis.append(f"{cid} cartes de boost = {vus} (attendu {n})")
    for cid, n in attendu.get("acceleration", []):
        f = face(cid)
        if f is not None and f.acceleration_token != n:
            soucis.append(f"{cid} jetons d'acceleration = {f.acceleration_token} (attendu {n})")
    if "partie_finie" in attendu and bool(getattr(monde, "is_game_over", False)) != attendu["partie_finie"]:
        soucis.append(f"partie finie = {getattr(monde, 'is_game_over', False)} (attendu {attendu['partie_finie']})")
    if "gagnee" in attendu:
        fini = bool(getattr(monde, "is_game_over", False))
        gagne = fini and bool(monde.game_over.players_won)
        if gagne != attendu["gagnee"]:
            soucis.append(f"partie gagnee = {gagne} (attendu {attendu['gagnee']})")
    for cid, voulu in attendu.get("nb_en_jeu", []):
        total = 0
        for objet in monde.object_manager.card_dict.values():
            f = getattr(objet, "face", None) or objet
            if getattr(getattr(f, "paper", None), "card_id", None) == cid and f.IsInPlay():
                total += 1
        if total != voulu:
            soucis.append(f"{total} exemplaire(s) de {cid} en jeu (attendu {voulu})")
    if "distribuees" in attendu:
        n = len(list(monde.players[0].dealt_encounter_cards.Get(True)))
        if n != attendu["distribuees"]:
            soucis.append(f"cartes rencontre distribuees = {n} (attendu {attendu['distribuees']})")
    if attendu.get("hors_deck_rencontre"):
        from game.operate.worlds import Worlds
        ids = {getattr(f.paper, "card_id", None) for f in Worlds.GetEncounterDeckCards(monde)}
        for cid in attendu["hors_deck_rencontre"]:
            if cid in ids:
                soucis.append(f"{cid} est dans le deck de rencontre (il devait en etre retire)")
    for ally, attaquant, voulu in attendu.get("peut_defendre", []):
        f, a = face(ally), face(attaquant)
        if f is not None and a is not None and bool(f.IsCanDefense(a)) != voulu:
            soucis.append(f"{ally} peut defendre contre {attaquant} = {f.IsCanDefense(a)} (attendu {voulu})")
    for cid, pic in attendu.get("hote_pic", []):
        f = face(cid)
        if f is not None:
            hote = f.bind_face
            vu = getattr(hote, "pic_id", None) if hote else None
            if vu != pic:
                soucis.append(f"{cid} est attache a une carte d'image {vu} (attendu {pic})")
    for cid in attendu.get("steady", []):
        f = face(cid)
        if f is not None and not f.IsSteady():
            soucis.append(f"{cid} n'est pas Steady")
    if soucis:
        return False, " ; ".join(soucis)
    return True, "etat conforme"
'''
