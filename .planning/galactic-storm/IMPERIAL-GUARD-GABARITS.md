# Imperial Guard (Galactic Storm, lot GS-4) : gabarits PROCESSUS-CARTE, gs091-gs113

Genere par `.planning/galactic-storm/defs/generer_gabarits_gs4.py` a partir des MESURES (rapport `test_capacites` filtre `[ig]`, sortie de `substituer_pack.py`, autoplay). Etape 1 : entrees `defs/imperial_guard_cards.py` (inserees par `defs/inserer_gs4.py`) ; etape 4 : images portees par `defs/copier_images_gs4.py`.

Batterie `[ig]` : 62/62 cas verts.

### gs091 : Disciplined Training

- [x] Etape 2 : cartes de reference : toughness : GiveKeywordToInPlayWhenApplyThis(toughness=1), modeles ar011 et 40189 ; Setup : base desc (setup.md) ; Special : WhenResolveSpecialAbility (special.md, modele ab007) ; DiscardEachOther (worlds.py)
- [x] Etape 5 : texte-contre-code, mots-pieges : « EACH IMPERIAL GUARD minion » (pas les autres sbires), la carte Tenace ne vaut que pour les sbires qui ENTRENT apres elle ; « YOUR identity » = celle du joueur qui resout ; « each OTHER SETTING environment ».
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Aucun nombre imprime ; Setup 1 ; Special : 1 degat. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 5 cas sujets, 5 verts avec le module ; substitution : SUBST gs091 : rouges 3/5 ⚠ un cas reste vert sans module
      - VERT : [ig] gs091 « Each IMPERIAL GUARD minion gains toughness » : Astra entre en jeu avec une carte Tenace
      - VERT : [ig] gs091 toughness, TEMOIN : un sbire d'un AUTRE set (Shocker) n'a pas de carte Tenace
      - VERT : [ig] gs091 Special : « Deal 1 damage to your identity » (resolu par le verificateur)
      - VERT : [ig] gs091 When Revealed : revelee, elle defausse l'AUTRE environnement SETTING en jeu (Noble Bearing)
      - VERT : [ig] gs091 Setup : en jeu des la mise en place (aucun script) ; son « When Revealed » n'a PAS joue
      Note : Les cas « When Revealed » et « Setup » ne mesurent que la base desc / le When Revealed, verts sans module pour Setup (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : OUI : environnement en jeu dessine (ui-app/src/board/kree-sentry-plateau.test.ts, environment_area ; calibre : rouge sans la carte)

Carte terminee : OUI.

### gs092 : Loyal Devotion

- [x] Etape 2 : cartes de reference : teamwork : GiveKeywordToInPlayWhenApplyThis(teamwork="IMPERIAL GUARD"), modele bl012 (teamwork.md) ; Special : PlaceThreatOnSchemes("MainScheme", 1)
- [x] Etape 5 : texte-contre-code, mots-pieges : « gains teamwork (IMPERIAL GUARD) » : le sbire qui ENTRE s'active si UN AUTRE sbire IMPERIAL GUARD est deja en jeu ; « the MAIN scheme ».
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Setup 1 ; 1 menace. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 4 cas sujets, 4 verts avec le module ; substitution : SUBST gs092 : rouges 3/4 ⚠ un cas reste vert sans module
      - VERT : [ig] gs092 « teamwork (IMPERIAL GUARD) » : Titan entre en jeu alors qu'Astra y est deja -> il s'active (attaque le heros : 2 degats)
      - VERT : [ig] gs092 teamwork, TEMOIN : sans autre sbire IMPERIAL GUARD en jeu, Titan n'active rien
      - VERT : [ig] gs092 Special : « Place 1 threat on the main scheme » (1B : 2 -> 3)
      - VERT : [ig] gs092 When Revealed : revelee, elle defausse l'AUTRE environnement SETTING en jeu (Disciplined Training)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs093 : Noble Bearing

- [x] Etape 2 : cartes de reference : guard + trait : GiveKeywordToInPlayWhenApplyThis(guard=1, trait="ELITE"), modeles sk091 et bl012 ; Special : Worlds.DiscardEncounterCards(3)
- [x] Etape 5 : texte-contre-code, mots-pieges : « guard AND the ELITE trait » (les deux) ; « the TOP 3 cards of the ENCOUNTER deck » ; sbires deja en jeu : l'environnement est en jeu des la mise en place.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Setup 1 ; guard 1 ; 3 cartes. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 5 cas sujets, 5 verts avec le module ; substitution : SUBST gs093 : rouges 4/5 ⚠ un cas reste vert sans module
      - VERT : [ig] gs093 « gains guard and the ELITE trait » : Astra entre en jeu avec le trait ELITE
      - VERT : [ig] gs093 guard : Astra porte le mot-cle Guard (1)
      - VERT : [ig] gs093 guard et ELITE, TEMOIN : un sbire d'un autre set (Shocker) n'en a ni l'un ni l'autre
      - VERT : [ig] gs093 Special : « Discard the top 3 cards of the encounter deck » (3 Advance en defausse)
      - VERT : [ig] gs093 When Revealed : revelee, elle defausse l'AUTRE environnement SETTING en jeu
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs094 : Astra

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; IsClass("IdentitySpecific") (modele bt021), GetControlCards()
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « IDENTITY-SPECIFIC » = classe propre a l'identite (pas Basic) ; « you CONTROL » = en jeu, pas la main
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 4 (pastille orange), MNG 2, ATQ 1, 1 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs094 : rouges 3/3
      - VERT : [ig] gs094 « Discard an identity-specific card you control » : Aunt May (soutien propre a Spider-Man) est defaussee, pas de Special
      - VERT : [ig] gs094 « If you cannot » : seul un allie BASIC en jeu (Mockingbird) -> rien a defausser, Special
      - VERT : [ig] gs094 « you control » : une carte propre a l'identite qui n'est que dans la MAIN n'est pas defaussee (Special)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs095 : Earthquake

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; Faces.ExhaustAll
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « If you WERE ALREADY exhausted » : l'etat est lu AVANT ; « your IDENTITY » (alter ego compris)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 5 (pastille orange), MNG 1, ATQ 2, 2 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs095 : rouges 2/2
      - VERT : [ig] gs095 « Exhaust your identity » : l'identite est inclinee, pas de Special
      - VERT : [ig] gs095 « If you were already exhausted » : identite deja inclinee -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs096 : Electron

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; FacesCounter.GetPrintedResourcesCount (modele gs240) ; icone eclair identifiee par decoupe contre sk152 (energie)
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « [energy] RESOURCE from your HAND » = carte de la main portant l'icone ; wild non compte (question Q2)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 5 (pastille orange), MNG 1, ATQ 2, 2 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs096 : rouges 3/3
      - VERT : [ig] gs096 « Discard a [energy] resource from your hand » : Energy (YY) defaussee, pas de Special
      - VERT : [ig] gs096 « If you cannot » : main sans [energy] (Genius, mentale) -> Special
      - VERT : [ig] gs096 « [energy] resource » : une carte WILD (Spider-Woman) n'est pas une ressource [energy] imprimee -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs097 : Fang

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; GetControlCards(CardFinder(has_printed_res="G")) ; icone etoile = wild (decoupe contre ab007 / rg011 / tt006)
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « a card you CONTROL » = en jeu (question Q6) ; « PRINTED [wild] »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 5 (pastille orange), MNG 1, ATQ 2, 2 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs097 : rouges 2/2
      - VERT : [ig] gs097 « Discard a card you control with a printed [wild] resource » : Spider-Woman (RES G) en jeu est defaussee
      - VERT : [ig] gs097 « If you cannot » : seul un allie a ressource [physical] en jeu (Mockingbird) -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs098 : Gladiator

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; Defeated(None, effect) (modele gs118a) ; Victory 0 : base desc (victory.md, modele 60024)
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « NON-SCENARIO SPECIFIC » = pas Rick Jones (classe Encounter, question Q7) ; « If NO ally was defeated » ; Victory 0 = pile de victoire ; trait ELITE imprime
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 8 (pastille orange), MNG 1, ATQ 3, 3 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 4 cas sujets, 4 verts avec le module ; substitution : SUBST gs098 : rouges 2/4 ⚠ un cas reste vert sans module
      - VERT : [ig] gs098 « Defeat a non-scenario specific ally you control » : Mockingbird est vaincue, pas de Special
      - VERT : [ig] gs098 « non-scenario specific » : Rick Jones (allie du scenario) ne peut PAS etre choisi -> Special, Rick toujours en jeu
      - VERT : [ig] gs098 Victory 0 : Gladiator vaincu va dans la pile de victoire
      - VERT : [ig] gs098 trait ELITE imprime
      Note : Les cas Victory 0 et trait ELITE mesurent des bases desc : verts sans module (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs099 : Hobgoblin

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; Faces.ResolveAbility(.., AbilityType.WhenRevealed, ..) (modeles sm 27083, sk046)
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « ANOTHER » sbire IMPERIAL GUARD (pas lui-meme, pas un sbire d'un autre set) EN JEU ; « a » : le joueur choisit ; « If NO ability was resolved »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 4 (pastille orange), MNG 3, ATQ 1, 2 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs099 : rouges 3/3
      - VERT : [ig] gs099 « Resolve a When Revealed ability of another IMPERIAL GUARD minion in play » : copie celui de Titan (defausse une carte Ressource)
      - VERT : [ig] gs099 « If no ability was resolved this way » : aucun autre sbire IMPERIAL GUARD en jeu -> Special
      - VERT : [ig] gs099 « another » : un sbire d'un AUTRE set (Shocker) en jeu ne compte pas -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs100 : Hussar

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; GetControlUpgrade() (comprend les ameliorations des allies)
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « UPGRADE » = amelioration (pas un soutien) ; « you control » = en jeu
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 5 (pastille orange), MNG 1, ATQ 2, 2 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs100 : rouges 2/2
      - VERT : [ig] gs100 « Discard an upgrade you control » : Combat Training (amelioration) est defaussee
      - VERT : [ig] gs100 « If you cannot » : aucune amelioration (un soutien seulement) -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs101 : Magique

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; Faces.GiveStatus([mechant], "Tough") (modele gs135)
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « THE villain » ; « If you CANNOT » = deja une carte Tenace
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 4 (pastille orange), MNG 2, ATQ 2, 1 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs101 : rouges 2/2
      - VERT : [ig] gs101 « Give the villain a tough status card » : Kree Sentry recoit une carte Tenace
      - VERT : [ig] gs101 « If you cannot » : le mechant a deja une carte Tenace -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs102 : Manta

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; Faces.GiveStatus([identite], "Stunned") (modele sk151)
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « If you WERE ALREADY stunned » ; « YOU » = l'identite (alter ego compris)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 4 (pastille orange), MNG 2, ATQ 2, 2 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs102 : rouges 2/2
      - VERT : [ig] gs102 « You are stunned » : l'identite est etourdie, pas de Special
      - VERT : [ig] gs102 « If you were already stunned » : deja etourdie -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs103 : Mentor

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; Worlds.GetAllSideSchemes filtre PlayerSideScheme
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « PLAYER side scheme » (pas une manigance de rencontre) ; « from PLAY »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 4 (pastille orange), MNG 3, ATQ 1, 1 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs103 : rouges 2/2
      - VERT : [ig] gs103 « Discard a player side scheme from play » : Build Support (manigance annexe JOUEUR) est defaussee
      - VERT : [ig] gs103 « If you cannot » : une manigance annexe de RENCONTRE (Locking on Target) n'est pas une manigance JOUEUR -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs104 : Neutron

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; GetControlCardsByType(support=True)
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « SUPPORT » en jeu sous le controle du joueur (pas un allie)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 5 (pastille orange), MNG 1, ATQ 2, 2 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs104 : rouges 2/2
      - VERT : [ig] gs104 « Discard a support you control » : Aunt May est defaussee
      - VERT : [ig] gs104 « If you cannot » : aucun soutien (un allie seulement) -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs105 : Nightside

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; FacesCounter.GetPrintedResourcesCount ; icone « noeuds relies » = mental (decoupe contre sk148 / sk151)
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « [mental] RESOURCE from your HAND » ; wild non compte (question Q2)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 4 (pastille orange), MNG 2, ATQ 2, 1 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs105 : rouges 2/2
      - VERT : [ig] gs105 « Discard a [mental] resource from your hand » : Genius (BB) defausse, pas de Special
      - VERT : [ig] gs105 « If you cannot » : main sans [mental] (Energy) -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs106 : Oracle

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; Faces.GiveStatus([identite], "Confused")
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « If you WERE ALREADY confused »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 4 (pastille orange), MNG 3, ATQ 1, 1 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs106 : rouges 2/2
      - VERT : [ig] gs106 « You are confused » : l'identite est desorientee, pas de Special
      - VERT : [ig] gs106 « If you were already confused » : deja desorientee -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs107 : Pulsar

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; FacesCounter.GetPrintedResourcesCount ; icone poing = physique (decoupe contre sk148 / sk152)
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « [physical] RESOURCE from your HAND » ; wild non compte (question Q2)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 5 (pastille orange), MNG 1, ATQ 2, 1 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs107 : rouges 2/2
      - VERT : [ig] gs107 « Discard a [physical] resource from your hand » : Strength (RR) defaussee, pas de Special
      - VERT : [ig] gs107 « If you cannot » : main sans [physical] -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs108 : Smasher

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; CardFinder Event sur la main
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « EVENT » = type Evenement ; « from your HAND »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 5 (pastille orange), MNG 1, ATQ 2, 1 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs108 : rouges 1/2 ⚠ un cas reste vert sans module
      - VERT : [ig] gs108 « Discard an event from your hand » : l'evenement (01005) est defausse, pas de Special
      - VERT : [ig] gs108 « If you cannot » : main sans evenement -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs109 : Starbolt

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; Faces.RemoveCountersOn([carte], 1, 'all-purpose') (all-purpose-counter.md)
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « ALL-PURPOSE counter » = compteur defini par la carte (pas des degats) ; « a card YOU CONTROL »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 5 (pastille orange), MNG 2, ATQ 2, 1 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs109 : rouges 2/2
      - VERT : [ig] gs109 « Remove 1 all-purpose counter from a card you control » : Web-Shooter (3 jetons web) en perd un
      - VERT : [ig] gs109 « If you cannot » : aucune carte controlee avec un compteur -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs110 : Titan

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; type Ressource sur la main
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « RESOURCE CARD » = type Ressource, pas une icone
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 6 (pastille orange), MNG 0, ATQ 2, 1 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs110 : rouges 2/2
      - VERT : [ig] gs110 « Discard a resource card from your hand » : la carte Ressource (Energy) est defaussee, pas de Special
      - VERT : [ig] gs110 « resource card » : un evenement portant une icone de ressource n'est PAS une carte Ressource -> Special
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs111 : Warstar

- [x] Etape 2 : cartes de reference : « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele` (imperial_guard/__init__.py : WhenThisRevealed + ResolveSpecialAbility, modele baxter_stockman ResoudreLeSpecial) ; Worlds.DiscardEncounterCards(1) + Reveal (modele tx009)
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = aucune carte a defausser (le sbire n'a aucun autre effet) ; « YOU » = le joueur a qui il est revele ; le Special vise l'environnement SETTING EN JEU ; « IF that card is an IMPERIAL GUARD MINION » (une traitrise ne compte pas) ; « Otherwise »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 5 (pastille orange), MNG 1, ATQ 2, 2 icone(s) de boost. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs111 : rouges 3/3
      - VERT : [ig] gs111 « Discard the top card of the encounter deck. If that card is an IMPERIAL GUARD minion, reveal it » : Titan est revele
      - VERT : [ig] gs111 « Otherwise » : la carte du dessus n'est pas un sbire IMPERIAL GUARD (Advance) -> Special
      - VERT : [ig] gs111 « IMPERIAL GUARD MINION » : une traitrise IMPERIAL GUARD du dessus (Guard Assembles) -> Special, elle n'est pas revelee
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (le sbire entre en jeu, ses cartes defaussees quittent des zones standard)

Carte terminee : OUI.

### gs112 : Guard Assembles

- [x] Etape 2 : cartes de reference : boucle Worlds.DiscardEncounterCards(1) bornee + Reveal (modele baxter_stockman DefausserJusquAuSbire, tx009)
- [x] Etape 5 : texte-contre-code, mots-pieges : « until you discard an IMPERIAL GUARD MINION » (un sbire d'un autre set ou une traitrise ne l'arrete pas) ; « and reveal IT ».
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 1 icone de boost. Identique.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs112 : rouges 2/2
      - VERT : [ig] gs112 « Discard cards ... until you discard an IMPERIAL GUARD minion and reveal it » : deux Advance defaussees puis Titan revele
      - VERT : [ig] gs112 « IMPERIAL GUARD minion » : un sbire d'un AUTRE set (Shocker) ne l'arrete pas ; Titan, derriere, est revele
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs113 : Imperial Formation

- [x] Etape 2 : cartes de reference : Faces.ResolveAbility (sm 27083, sk046) ; Search.EncounterCard(include_discard_pile=True) + Reveal (fne 60185)
- [x] Etape 5 : texte-contre-code, mots-pieges : « EACH IMPERIAL GUARD minion IN PLAY » ; « If you cannot » = aucun en jeu ; recherche d'un SBIRE IMPERIAL GUARD dans le deck ET la defausse.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Aucune icone de boost. Identique.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs113 : rouges 3/3
      - VERT : [ig] gs113 « Resolve the When Revealed ability of each IMPERIAL GUARD minion in play » : Titan ET Smasher resolvent le leur
      - VERT : [ig] gs113 « If you cannot » : aucun sbire IMPERIAL GUARD en jeu -> cherche dans le deck rencontre et revele Titan
      - VERT : [ig] gs113 recherche : dans la DEFAUSSE rencontre aussi
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON

Carte terminee : OUI.

