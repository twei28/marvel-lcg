# Majestrix's Verdict (Galactic Storm, lot GS-5) : gabarits PROCESSUS-CARTE, gs114-gs137

Genere par `.planning/galactic-storm/defs/generer_gabarits_majestrix.py` a partir des MESURES (rapport
`test_capacites` filtre `[mv]`, sortie de `substituer_pack.py ... gs`, autoplay). Etape 1 : entrees
`defs/majestrix_cards.py` (inserees par `defs/inserer_majestrix.py`) ; etape 4 : images portees par
`defs/copier_images_majestrix.py` (27 card_id, une image par numero imprime).

Batterie `[mv]` : 75/75 cas verts.

### gs114 : Deathbird (I)

- [x] Etape 2 : cartes de reference : Forced interrupt : 50089b Extract Captives (ReplaceTarget sur WhenUnitWouldAttack, un ennemi attaque un allie : moteur natif) ; +1 ATK : GainATKForThisAttack (sender_damage.py).
- [x] Etape 5 : texte-contre-code, mots-pieges : « initiates an attack AGAINST YOU » (identite visee, pas un allie deja vise), « if YOU control », « THAT ally » (choix du joueur s'il en a plusieurs), « instead » (cible REMPLACEE, pas ajoutee) ; etoile en exposant de l'ATQ = renvoi au texte.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 16[per_hero] -> HP "16*" ; MNG 2 ; ATQ 2 ; +1 ATK -> bonus_atq=1. Identiques desc / script / scan.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs114 : rouges 1/3 ⚠ un cas reste vert sans module
      - VERT : [mv] gs114 Forced interrupt : Deathbird attaque Ch'od (STARJAMMER controle) au lieu du heros, avec +1 ATQ (3 degats)
      - VERT : [mv] gs114 Forced interrupt, TEMOIN : aucun STARJAMMER en jeu -> Deathbird attaque le heros (2 degats)
      - VERT : [mv] gs114 Forced interrupt, TEMOIN : un allie NON STARJAMMER (Black Widow) ne detourne pas l'attaque
      Note : Les deux TEMOINS (sans STARJAMMER, allie non STARJAMMER) verifient une absence de detournement : verts sans module (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON (aucune carte deplacee, aucun compteur)

Carte terminee : OUI.

### gs115 : Deathbird (II)

- [x] Etape 2 : cartes de reference : cannot be defeated : 50129a Citizen V / 35029 (UnitCannotBeDefeatedWhile) + relance ecrite a part (piege de change_on_event, RECETTES §16) ; Forced interrupt : comme gs114.
- [x] Etape 5 : texte-contre-code, mots-pieges : « players do not control Lilandra AND the Shi'ar Throne SUPPORT » (les deux, sous controle de joueurs ; la face manigance ne compte pas) ; memes mots-pieges que gs114.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 19[per_hero] -> "19*" ; MNG 2 ; ATQ 3 ; +1 ATK. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 4 cas sujets, 4 verts avec le module ; substitution : SUBST gs115 : rouges 2/4 ⚠ un cas reste vert sans module
      - VERT : [mv] gs115 Forced interrupt : Deathbird II detournee sur Ch'od avec +1 ATQ (ATQ 3 + 1 = 4 degats)
      - VERT : [mv] gs115 cannot be defeated : sans Lilandra ni le soutien Shi'ar Throne, Deathbird II a 0 PV reste en jeu
      - VERT : [mv] gs115 cannot be defeated, TEMOIN : Lilandra ET le soutien Shi'ar Throne controles -> Deathbird II vaincue (victoire)
      - VERT : [mv] gs115 cannot be defeated : Deathbird II a 0 PV tombe des que Lilandra et le Trone passent sous controle
      Note : Verts sans module : le TEMOIN (Lilandra + Trone -> victoire) et le cas « tombe des que ... » (sans module, Deathbird meurt tout de suite : meme etat final). Ce dernier a ete vu ROUGE AVEC le module avant le correctif de la relance (« victoire = False », passe du 20/10/2026) : il mesure bien la relance.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs116 : Deathbird (III)

- [x] Etape 2 : cartes de reference : comme gs115 ; « 1 additional boost card for that activation » : sk100 Emperor's Throne (GiveAdditionalBoostCardForThisActivation).
- [x] Etape 5 : texte-contre-code, mots-pieges : PAS de +1 ATK sur ce stade (texte different, verifie sur le scan) ; la carte de boost ne vaut que si l'attaque est detournee.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 21[per_hero] -> "21*" ; MNG 2 ; ATQ 3 ; boost_sup=1. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs116 : rouges 2/3 ⚠ un cas reste vert sans module
      - VERT : [mv] gs116 Forced interrupt (expert) : Deathbird III detournee sur Ch'od SANS +1 ATQ, avec 1 carte de boost en plus (2 recues)
      - VERT : [mv] gs116 Forced interrupt, TEMOIN : sans STARJAMMER, Deathbird III attaque le heros avec UNE carte de boost
      - VERT : [mv] gs116 cannot be defeated (expert) : Deathbird III a 0 PV reste en jeu sans Lilandra ni le Trone
      Note : Le TEMOIN sans STARJAMMER (une seule carte de boost) reste vert sans module (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs117a : Earn the People's Favor (1A)

- [x] Etape 2 : cartes de reference : Setup d'une face 1A : 50087a Batroc (WhenCardSetup, SetupCards.PutIntoPlay / SetAsideCards) ; tuck face visible : PlaceCardHere(.., True, ..) (livret p.4).
- [x] Etape 5 : texte-contre-code, mots-pieges : « EACH STARJAMMER ally » (les six, Lilandra comprise) ; « Set the Shi'ar Throne side scheme ASIDE » (pas en jeu) ; « Contents » porte par le JSON du scenario.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Aucun nombre sur la face A ; Contents : 2 stades de mechant (expert : II et III), 1 modulaire -> data/scenarios/gs_majestrix_verdict*.json.
      Resultat : conforme.
- [x] Etape 7 : 1 cas sujets, 1 verts avec le module ; substitution : SUBST gs117a : rouges 1/1
      - VERT : [mv] gs117a Setup : la prison entre en jeu, les SIX STARJAMMER glisses dessous face visible, le Trone mis de cote
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : OUI : cas plateau ui-app/src/board/glisse-sous-manigance.test.ts (allies glisses face VISIBLE sous la prison) ; aucun correctif plateau necessaire (mecanisme generique de mere-de-la-nuit) ; calibrage : la meme table avec les allies FACE CACHEE fait tomber le 3e cas (vu rouge le 20/10/2026).

Carte terminee : OUI.

### gs117b : Earn the People's Favor (1B)

- [x] Etape 2 : cartes de reference : When Revealed : WhenThisRevealed + PlaceThreatOnSchemes (50134) ; « After resolving step one of the villain phase » : 04096b Hunting Down Heroes (AfterResolveVillainPhaseStep).
- [x] Etape 5 : texte-contre-code, mots-pieges : « 2 threat FOR EACH PLAYER in alter-ego form » (0 si tous en heros, contre-cas) ; la menace va sur la PRISON ; etoile de l'escalade = renvoi au texte.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Seuil 3[per_hero] -> "3*" ; escalade +1[per_hero] -> "1*" ; depart 0 ; 1[per_hero] -> "1*" ; 2 par joueur -> 2*n. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs117b : rouges 3/3
      - VERT : [mv] gs117b When Revealed : 1[per_hero] menace sur la prison (6 de depart + 1 = 7, un joueur)
      - VERT : [mv] gs117b Forced Response apres l'etape 1 : joueur en ALTER EGO -> +2 sur la prison (7 -> 9)
      - VERT : [mv] gs117b Forced Response apres l'etape 1, TEMOIN : joueur en HEROS -> rien (7)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs118a : Majestrix's Verdict (2A)

- [x] Etape 2 : cartes de reference : « players as a group choose » : convention Filter.One (premier joueur) ; remove from the game : Faces.RemoveAllFromGame ; « Advance to stage 2B » automatique (face A sans seuil, comme sk145a) ; in expert mode : Worlds.IsExpert (50087a).
- [x] Etape 5 : texte-contre-code, mots-pieges : « Otherwise » = seulement si AUCUN glisse (FAQ 1.2) ; « (2 ... instead in expert mode) » ; « in play » ; Lilandra executee = defaite (insert).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 1 (2 en expert) glisse(s) ; 1 en jeu. Identiques au scan.
      Resultat : conforme.
- [x] Etape 7 : 5 cas sujets, 5 verts avec le module ; substitution : SUBST gs118a : rouges 5/5
      - VERT : [mv] gs118a When Revealed : le STARJAMMER glisse choisi (Ch'od) est retire de la partie, puis 2B (prison +1)
      - VERT : [mv] gs118a When Revealed (expert) : DEUX STARJAMMER glisses retires de la partie
      - VERT : [mv] gs118a FAQ (expert) : un SEUL glisse -> lui seul est retire, aucun allie en jeu n'est touche
      - VERT : [mv] gs118a Otherwise : plus aucun glisse -> un STARJAMMER EN JEU (Corsair) est retire de la partie
      - VERT : [mv] gs118a Lilandra glissee executee -> les joueurs perdent
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : OUI (carte retiree de la partie, zone non dessinee) : rien a dessiner ; la prison se redessine avec un glisse de moins (meme cas plateau que gs117a).

Carte terminee : OUI.

### gs118b : Majestrix's Verdict (2B)

- [x] Etape 2 : cartes de reference : WhenMainSchemeStageWouldBeCompleted + SetBeInstead : sk145b (meme auteur) ; flip d'une manigance en jeu = revelation (OnAfterFlip) ; helpers 1B.
- [x] Etape 5 : texte-contre-code, mots-pieges : « INSTEAD » (jamais accompli) ; « flip this card AND REVEAL IT » (2A rejoue son execution) ; stade 2B qui recommence a 0 (point tranche par necessite, voir questions).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Seuil 5[per_hero] -> "5*" ; escalade +2[per_hero] -> "2*" ; depart 0 ; 1[per_hero] ; 2 par joueur. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs118b : rouges 3/3
      - VERT : [mv] gs118b Forced Interrupt : 2B serait accomplie -> retournee et revelee (2A execute un 2e STARJAMMER), retour en 2B a 0
      - VERT : [mv] gs118b When Revealed : 1[per_hero] menace sur la prison (7 -> 8)
      - VERT : [mv] gs118b Forced Response apres l'etape 1 : alter ego -> +2 sur la prison (8 -> 10)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON (meme carte retournee deux fois, le plateau dessine la face courante)

Carte terminee : OUI.

### gs119 : Imprisoned on Chandilar

- [x] Etape 2 : cartes de reference : Assault / Permanent : bases desc (assault.md, permanent.md) ; tuck apres depart : 50081 Abduct Superhumans ; liberation : 50088b Locate Missing Person.
- [x] Etape 5 : texte-contre-code, mots-pieges : « a STARJAMMER ALLY leaves play » ; retire de la partie = pas recapture ; « place 6 threat » meme sans allie (question Q3) ; « players as a group » ; tuck FACE VISIBLE.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Depart 6 ; « place 6 threat ». Identiques.
      Resultat : conforme.
- [x] Etape 7 : 5 cas sujets, 5 verts avec le module ; substitution : SUBST gs119 : rouges 2/5 ⚠ un cas reste vert sans module
      - VERT : [mv] gs119 Forced Interrupt : la derniere menace part -> l'allie choisi (Corsair) entre en jeu sous controle, 6 menaces reviennent
      - VERT : [mv] gs119 Forced Response : un STARJAMMER vaincu (Corsair) est glisse a nouveau sous la prison
      - VERT : [mv] gs119 Forced Response, TEMOIN : un allie NON STARJAMMER vaincu n'est pas glisse
      - VERT : [mv] gs119 Assault : le contre de base de Spider-Man (CTR 1, ATQ 2) retire 2 menaces de la prison
      - VERT : [mv] gs119 Permanent : une defausse par une regle d'un autre set laisse la prison en jeu
      Note : Verts sans module (assume) : Assault et Permanent (bases desc) et le temoin « allie NON STARJAMMER non glisse » (absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : OUI : glissement face visible sous la prison, cas plateau glisse-sous-manigance.test.ts (voir gs117a).

Carte terminee : OUI.

### gs120a : Shi'ar Throne (manigance annexe)

- [x] Etape 2 : cartes de reference : 32172a Enemy of My Enemy (flip puis PutIntoPlay de la face B) ; retournement differe a AfterSchemeBeDefeated (piege mesure, RECETTES §16).
- [x] Etape 5 : texte-contre-code, mots-pieges : « the DEFEATING player » (message.defeating_player, repli premier joueur) ; face B = SOUTIEN.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Depart 3[per_hero] -> "3*" ; Hazard 1. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 1 cas sujets, 1 verts avec le module ; substitution : SUBST gs120a : rouges 1/1
      - VERT : [mv] gs120a When Defeated : le joueur qui la vainc retourne le Trone et en prend le controle (soutien gs120b)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : OUI : la carte change de zone (manigances -> soutiens du joueur) ; zones existantes, pas de cas plateau propre (support standard).

Carte terminee : OUI.

### gs120b : Shi'ar Throne (soutien)

- [x] Etape 2 : cartes de reference : 16142 Milano / sk062 Baxter Building (CanGenerateResources + Exhaust + AnyPlayerCanDoThis) ; AfterCardLeavePlay(ForcedResponse).
- [x] Etape 5 : texte-contre-code, mots-pieges : « Shi'ar Throne OR Lilandra » (deux declencheurs, deux cas) ; « for ANY player » ; ressource [mental] verifiee par decoupe (sk003, sk148).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 1 ressource B. Identique.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs120b : rouges 3/3
      - VERT : [mv] gs120b Forced Response : Lilandra quitte le jeu -> le soutien se retourne et la manigance est revelee (3 menaces)
      - VERT : [mv] gs120b Forced Response : le soutien Shi'ar Throne quitte le jeu (defausse) -> retourne et revele (3 menaces)
      - VERT : [mv] gs120b Resource : incliner le Trone paie Aunt May (cout 1) sans autre ressource
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : OUI : retour de la zone soutien a la zone manigances (zones standard).

Carte terminee : OUI.

### gs121 : Lilandra

- [x] Etape 2 : cartes de reference : 50091 Rescued Captive (ThisNotCountAllyLimit) ; 01083 (AfterCardEnterPlay) + SetupCards.Reveal(only_set_aside) ; 50089b (SetGameOver).
- [x] Etape 5 : texte-contre-code, mots-pieges : « set aside » (rien si le Trone est deja en jeu) ; « REMOVED from the game » ≠ vaincue (contre-cas).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 4 ; CTR 1 ; ATQ 2 + 1 degat consecutif -> "2*" ; pas de cout. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 4 cas sujets, 4 verts avec le module ; substitution : SUBST gs121 : rouges 3/4 ⚠ un cas reste vert sans module
      - VERT : [mv] gs121 Forced Response : Lilandra entre en jeu -> le Trone mis de cote est revele (3[per_hero] menaces, Hazard)
      - VERT : [mv] gs121 Does not count against your ally limit : 3 allies + Lilandra, Lilandra hors du compte
      - VERT : [mv] gs121 « If Lilandra is removed from the game, the players lose the game » : Lilandra en jeu retiree de la partie
      - VERT : [mv] gs121 defaite, TEMOIN : Lilandra VAINCUE n'est pas retiree de la partie (glissee sous la prison, pas de defaite)
      Note : Le contre-cas « Lilandra VAINCUE : pas de defaite » reste vert sans module (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : OUI : sort de prison / y retourne (cas plateau de la prison).

Carte terminee : OUI.

### gs122 : Ch'od

- [x] Etape 2 : cartes de reference : Retaliate : base desc (retaliate.md).
- [x] Etape 5 : texte-contre-code, mots-pieges : Riposte 2 (pas 1).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Cout 3, PV 6, CTR 1*, ATQ 3** (2 consecutifs), RES B, Riposte 2. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 1 cas sujets, 1 verts avec le module ; substitution : SUBST gs122 : rouges 0/1 ⚠ un cas reste vert sans module
      - VERT : [mv] gs122 Retaliate 2 : Deathbird detournee sur Ch'od subit 2 degats de riposte
      Note : Aucune capacite scriptee (module vide) : le cas « Retaliate 2 » mesure la base desc et reste vert sans module (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs123 : Corsair

- [x] Etape 2 : cartes de reference : UnitAttackGainKeyword("This", ranged=True) (RECETTES §3, 27078).
- [x] Etape 5 : texte-contre-code, mots-pieges : « attacks » = toutes ses attaques.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Cout 3, PV 4, CTR 2*, ATQ 2*, RES Y. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 1 cas sujets, 1 verts avec le module ; substitution : SUBST gs123 : rouges 1/1
      - VERT : [mv] gs123 Corsair : ses attaques gagnent Distance -> pas de riposte du Jailor (1 seul degat, consecutif)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs124 : Hepzibah

- [x] Etape 2 : cartes de reference : UnitAttackGainKeyword("This", piercing=True).
- [x] Etape 5 : texte-contre-code, mots-pieges : « attacks » = toutes.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Cout 3, PV 3, CTR 2*, ATQ 3*, RES R. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 1 cas sujets, 1 verts avec le module ; substitution : SUBST gs124 : rouges 1/1
      - VERT : [mv] gs124 Hepzibah : ses attaques gagnent Percant -> le Tenace de Deathbird saute, 3 degats passent
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs125 : Korvus

- [x] Etape 2 : cartes de reference : UnitAttackGainKeyword("This", overkill=True).
- [x] Etape 5 : texte-contre-code, mots-pieges : « attacks » = toutes ; deux etoiles sous l'ATQ.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Cout 3, PV 5, CTR 1*, ATQ 3**, RES Y. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 1 cas sujets, 1 verts avec le module ; substitution : SUBST gs125 : rouges 1/1
      - VERT : [mv] gs125 Korvus : ses attaques gagnent Debordement -> 2 degats en exces sur Deathbird (Jailor a 1 PV)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs126 : Raza

- [x] Etape 2 : cartes de reference : Toughness : base desc (toughness.md).
- [x] Etape 5 : texte-contre-code, mots-pieges : Tenace a l'entree en jeu (piege du Reset, RECETTES §16).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Cout 3, PV 3, CTR 2*, ATQ 2*, RES B, Toughness 1. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 1 cas sujets, 1 verts avec le module ; substitution : SUBST gs126 : rouges 0/1 ⚠ un cas reste vert sans module
      - VERT : [mv] gs126 Raza : Toughness -> il entre en jeu avec une carte d'etat Tenace
      Note : Aucune capacite scriptee (module vide) : cas de la base desc, vert sans module (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : OUI (carte d'etat Tenace dessinee, mecanisme standard)

Carte terminee : OUI.

### gs127 : Royal Cape of the Shi'ar

- [x] Etape 2 : cartes de reference : 07035 Distracting Taunts (AttachToFaceWhenPutIntoPlay, health, Response AfterUnitAttackUnit + SetCost) ; sk148 (retaliate).
- [x] Etape 5 : texte-contre-code, mots-pieges : « Attached CHARACTER » (vaut pour Lilandra) ; « After LILANDRA attacks DEATHBIRD » ; cout [energy].
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : +2 PV, Riposte 1, 2 icones de boost. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 4 cas sujets, 4 verts avec le module ; substitution : SUBST gs127 : rouges 4/4
      - VERT : [mv] gs127 Royal Cape : attachee a Deathbird, +2 PV (18) et Riposte 1
      - VERT : [mv] gs127 Royal Cape Response : Lilandra attaque Deathbird, [energy] paye -> la Cape passe sur Lilandra (PV max 6)
      - VERT : [mv] gs127 Royal Cape Response, TEMOIN : sans [energy] en main, la Cape reste sur Deathbird
      - VERT : [mv] gs127 Royal Cape revelee depuis le deck rencontre : elle s'attache a Deathbird
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : OUI : l'attachement change de porteur (Deathbird -> Lilandra), zones standard.

Carte terminee : OUI.

### gs128 : Shi'ar Crest

- [x] Etape 2 : cartes de reference : badge SCH+/THW+ : has_modify.py ; steady : GiveKeywordToAttached ; Boost : 52037 Growing Strong.
- [x] Etape 5 : texte-contre-code, mots-pieges : « the ACTIVATING enemy » ; badge « +1 SCH/THW » (+1 MNG sur Deathbird, +1 CTR sur Lilandra).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : +1 MNG / +1 CTR, 1 icone de boost. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs128 : rouges 3/3
      - VERT : [mv] gs128 Shi'ar Crest : attachee a Deathbird, +1 MNG et Solide (steady)
      - VERT : [mv] gs128 Shi'ar Crest Response : [mental] paye -> la Crete passe sur Lilandra (+1 CTR, Solide)
      - VERT : [mv] gs128 Shi'ar Crest Boost : l'ennemi qui s'active (Deathbird) recoit une carte d'etat Tenace
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : OUI : changement de porteur (zones standard).

Carte terminee : OUI.

### gs129 : Shi'ar Javelin

- [x] Etape 2 : cartes de reference : badge ATK+ ; 27147 Arm Cannon (UnitAttackGainKeyword("Attached..")) ; Boost : 50160 Supersonic.
- [x] Etape 5 : texte-contre-code, mots-pieges : « IF this activation is an attack » ; « attached CHARACTER ».
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : +1 ATQ, 1 icone de boost, 2 exemplaires. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs129 : rouges 3/3
      - VERT : [mv] gs129 Shi'ar Javelin : attache a Deathbird, +1 ATQ ; ses attaques gagnent Percant (le Tenace du heros saute, 3 degats)
      - VERT : [mv] gs129 Shi'ar Javelin Response : [physical] paye -> le Javelot passe sur Lilandra (+1 ATQ)
      - VERT : [mv] gs129 Shi'ar Javelin Boost : l'attaque gagne Percant -> le Tenace du heros saute (ATQ 2 + 1 icone = 3 degats)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : OUI : changement de porteur (zones standard).

Carte terminee : OUI.

### gs130 : Araki

- [x] Etape 2 : cartes de reference : Patrol / Vulnerable : bases desc ; When Defeated : sk155 ; « each scheme » : littéral EachScheme.
- [x] Etape 5 : texte-contre-code, mots-pieges : « EACH SCHEME » (principale + annexes) ; Vulnerable = defausse, pas « vaincu ».
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : MNG 3, ATQ 1, PV 4, 0 icone de boost ; 2 et 1 menaces. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 5 cas sujets, 5 verts avec le module ; substitution : SUBST gs130 : rouges 2/5 ⚠ un cas reste vert sans module
      - VERT : [mv] gs130 Araki When Defeated : 2 menaces sur CHAQUE manigance (principale 0 -> 2, prison 7 -> 9)
      - VERT : [mv] gs130 Araki Boost : 1 menace sur chaque manigance (prison 7 -> 8, principale 0 -> 1)
      - VERT : [mv] gs130 Araki Vulnerable : sonne, il est defausse (pas vaincu : aucune menace posee)
      - VERT : [mv] gs130 Araki Patrol : engage, le contre du heros ne peut pas viser la principale (2 restent, la prison prend 2)
      - VERT : [mv] gs130 Araki Patrol, TEMOIN : sans Araki, le meme contre vise la principale (2 -> 1)
      Note : Verts sans module (assume) : Vulnerable et les deux cas Patrol (bases desc : cas sujet et temoin).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs131 : Jailor of Chandilar

- [x] Etape 2 : cartes de reference : When Defeated : sk155 + RemoveThreatFromSchemes ; Boost : WhenCardBecomeBoost.
- [x] Etape 5 : texte-contre-code, mots-pieges : menace sur la PRISON.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : MNG 1, ATQ 2, PV 6, Riposte 1, 1 icone, 4 exemplaires ; 2 / 1 menaces. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs131 : rouges 2/3 ⚠ un cas reste vert sans module
      - VERT : [mv] gs131 Jailor When Defeated : 2 menaces retirees de la prison (7 -> 5)
      - VERT : [mv] gs131 Jailor Boost : 1 menace sur la prison (7 -> 8)
      - VERT : [mv] gs131 Jailor Retaliate 1 : le heros qui l'attaque subit 1 degat
      Note : Retaliate : base desc, cas vert sans module (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs132 : Private Audience

- [x] Etape 2 : cartes de reference : 49039 Selene (UnitCannotAttackTarget) ; 55061 Puppet Master (UnitCannotThwartTarget).
- [x] Etape 5 : texte-contre-code, mots-pieges : « ALLIES » (pas les heros) ; « the VILLAIN » ; « the MAIN scheme ».
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Depart 3[per_hero], Acceleration 1, aucune icone de boost. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 5 cas sujets, 5 verts avec le module ; substitution : SUBST gs132 : rouges 2/5 ⚠ un cas reste vert sans module
      - VERT : [mv] gs132 Private Audience : revelee avec 3[per_hero] menaces et l'icone Acceleration
      - VERT : [mv] gs132 Private Audience : un allie (Ch'od) ne peut pas attaquer le mechant (0 degat)
      - VERT : [mv] gs132 Private Audience, TEMOIN : sans elle, Ch'od frappe le mechant (3 degats)
      - VERT : [mv] gs132 Private Audience : un allie (Ch'od) ne peut pas contrer la manigance principale (2 menaces restent)
      - VERT : [mv] gs132 Private Audience, TEMOIN : sans elle, Ch'od contre la manigance principale (2 -> 1)
      Note : Les cas temoins (sans elle) et le cas « revelee avec 3 menaces » restent verts sans module (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs133 : Tapping the M'kraan Force

- [x] Etape 2 : cartes de reference : Hinder/Amplify/Hazard : bases desc ; When Defeated : sk100 ; HealthUnits.
- [x] Etape 5 : texte-contre-code, mots-pieges : « EACH STARJAMMER ally IN PLAY ».
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Depart 2, Hinder 2[per_hero], Amplify 1, Hazard 1, 3 icones ; soin 1. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs133 : rouges 1/2 ⚠ un cas reste vert sans module
      - VERT : [mv] gs133 Tapping the M'kraan Force : revelee avec 2 + Hinder 2[per_hero] = 4 menaces, Amplify et Hazard
      - VERT : [mv] gs133 Tapping When Defeated : 1 degat soigne sur chaque STARJAMMER en jeu (Ch'od 3 -> 2)
      Note : Le cas « revelee avec 4 menaces et les icones » mesure les bases desc : vert sans module (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs134 : Tortured Prisoners

- [x] Etape 2 : cartes de reference : Crisis : base desc ; sk156 (When Revealed, menace additionnelle).
- [x] Etape 5 : texte-contre-code, mots-pieges : « TUCKED » (pas en jeu) ; « additional ».
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Depart 1[per_hero], Crisis 1, 2 icones ; +1 par glisse. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs134 : rouges 2/2
      - VERT : [mv] gs134 Tortured Prisoners : 1[per_hero] + 1 par STARJAMMER glisse (6) = 7 menaces, icone Crisis
      - VERT : [mv] gs134 Tortured Prisoners : un seul STARJAMMER libere -> 1 + 5 = 6 menaces
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs135 : Birthright to the Throne

- [x] Etape 2 : cartes de reference : 16114 Single-Minded Fury (DoAttackYou du controleur, meme en alter ego) ; 50096 (DoSchemes) ; Tenace : 52037.
- [x] Etape 5 : texte-contre-code, mots-pieges : « the player WHO CONTROLS IT » ; « SUPPORT » ; detournement par Deathbird possible.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 1 icone de boost, 2 exemplaires. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs135 : rouges 3/3
      - VERT : [mv] gs135 Birthright : pas de soutien Shi'ar Throne -> Deathbird manigance (principale 0 -> 2)
      - VERT : [mv] gs135 Birthright : le soutien Shi'ar Throne en jeu -> Deathbird attaque son controleur EN ALTER EGO (detournee sur Lilandra, 3 degats)
      - VERT : [mv] gs135 Birthright Boost : Deathbird recoit une carte d'etat Tenace
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs136 : Exemplar Punishment

- [x] Etape 2 : cartes de reference : 04096b (ChooseAbilities a deux branches) ; ra028 (TakeIndirectDamage).
- [x] Etape 5 : texte-contre-code, mots-pieges : « FOR EACH » (un choix par glisse) ; « place 2 threat on IT » (question Q2).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 1 indirect / 1 menace / 2 menaces, 1 icone, 2 exemplaires. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs136 : rouges 3/3
      - VERT : [mv] gs136 Exemplar Punishment : 2 glisses (4 liberes), « 1 menace sur la principale » choisi 2 fois (0 -> 2)
      - VERT : [mv] gs136 Exemplar Punishment : 6 glisses, « 1 degat indirect » choisi 6 fois (6 degats, principale a 0)
      - VERT : [mv] gs136 Exemplar Punishment : aucun glisse -> 2 menaces sur la prison (7 -> 9)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs137 : Sister's Deception

- [x] Etape 2 : cartes de reference : 22031 Old Rivals (BasicAttack d'un allie contre l'identite).
- [x] Etape 5 : texte-contre-code, mots-pieges : « attacks YOU » (le joueur qui revele) ; « WITHOUT exhausting » (cas : pret) ; « WITH consequential damage » (cas : 1 degat).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : ATQ de Lilandra 2, 1 consecutif ; 3 menaces ; 2 icones, 2 exemplaires. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs137 : rouges 2/2
      - VERT : [mv] gs137 Sister's Deception : Lilandra en jeu attaque le joueur (2 degats), sans s'incliner, 1 degat consecutif
      - VERT : [mv] gs137 Sister's Deception : Lilandra pas en jeu -> 3 menaces sur la prison (7 -> 10)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man, profil equilibre) : 8 parties gs_majestrix_verdict normal + 8 expert, temoin sk_paibok (meme auteur, meme deck) 8 normal + 8 expert. Majestrix : 16/16 parties avec verdict, 0 bloquee (temoin Paibok : 2 bloquees sur 16), 0 victoire (le bot ne libere presque jamais de STARJAMMER : Assault, pas d'attaque des geoliers), 12 joueurs elimines, 4 « Players Lost » = execution de Lilandra, la derniere glissee (journal lu : Raza, Korvus, Hepzibah, Corsair, Ch'od puis Lilandra retires de la partie, un par passage en 2A/2B, comme le veut la regle). grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 16 journaux : 0 partout. Partie normale 6 lue : liberation de la prison (2 fois), boucle 2B -> 2A -> 2B observee (« retournee », execution, 2B revelee a 0).
- [x] Etape 8 bis : NON

Carte terminee : OUI.

