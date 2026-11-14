# Kree Sentry (Galactic Storm, lot GS-4) : gabarits PROCESSUS-CARTE, gs076-gs090

Genere par `.planning/galactic-storm/defs/generer_gabarits_gs4.py` a partir des MESURES (rapport `test_capacites` filtre `[ks]`, sortie de `substituer_pack.py`, autoplay). Etape 1 : entrees `defs/kree_sentry_cards.py` (inserees par `defs/inserer_gs4.py`) ; etape 4 : images portees par `defs/copier_images_gs4.py` (une image par numero imprime).

Batterie `[ks]` : 90/90 cas verts.

### gs076 : Kree Sentry (I)

- [x] Etape 2 : cartes de reference : AfterUnitAttackAndDamageUnit (01118 Sonic Converter) ; AttacherUnePoigne (AttachTo2, modele sunfire) ; PlaceThreatOnSchemes("MainScheme") (01121)
- [x] Etape 5 : texte-contre-code, mots-pieges : « attacks AND DAMAGES » (aucun degat = rien) ; « THAT character » ; « If you cannot » (aucune copie de cote OU personnage vaincu) ; etoile de l'ATQ = renvoi au texte.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 16[per_hero] -> "16*" ; MNG 2 ; ATQ 1 ; 1 menace. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 5 cas sujets, 5 verts avec le module ; substitution : SUBST gs076 : rouges 4/5 ⚠ un cas reste vert sans module
      - VERT : [ks] gs076 Forced Response : Kree Sentry attaque un allie (Black Widow) et le blesse -> une Poigne s'attache a lui
      - VERT : [ks] gs076 Forced Response : AUCUNE Poigne de cote -> 1 menace sur la principale (2 -> 3)
      - VERT : [ks] gs076 Forced Response, TEMOIN : l'attaque ne fait AUCUN degat (allie Tenace) -> rien ne se declenche
      - VERT : [ks] gs076 Forced Response : l'allie est VAINCU par l'attaque -> la Poigne ne peut pas s'y attacher : 1 menace sur la principale
      - VERT : [ks] gs076 Forced Response : Kree Sentry attaque un SBIRE (Shocker) et le blesse -> Poigne sur le sbire
      Note : Les cas temoins (carte Tenace, aucun degat) verifient une absence : verts sans module (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : OUI : Poigne attachee a un allie / un sbire / une identite dessinee (ui-app/src/board/kree-sentry-plateau.test.ts ; calibre le 20/10/2026 : la meme table sans la Poigne de Rick fait tomber 3 cas sur 7)

Carte terminee : OUI.

### gs077 : Kree Sentry (II)

- [x] Etape 2 : cartes de reference : comme gs076 ; When Revealed : WhenThisRevealed + AttacherUnePoigne
- [x] Etape 5 : texte-contre-code, mots-pieges : « a set aside copy » ; meme Reponse avec 2 menaces ; ATQ 2.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 18[per_hero] -> "18*" ; MNG 2 ; ATQ 2 ; 2 menaces. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs077 : rouges 3/3
      - VERT : [ks] gs077 When Revealed : Kree Sentry (II) arrive -> la Poigne de cote s'attache a Rick Jones (deux sur lui)
      - VERT : [ks] gs077 Forced Response : AUCUNE Poigne de cote -> 2 menaces sur la principale (2 -> 4)
      - VERT : [ks] gs077 Forced Response : une Poigne de cote -> s'attache a l'allie blesse (ATQ 2 : 2 degats)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : OUI : voir gs076

Carte terminee : OUI.

### gs078 : Kree Sentry (III)

- [x] Etape 2 : cartes de reference : comme gs076 ; « EACH set aside copy » : boucle d'attache jusqu'a epuisement
- [x] Etape 5 : texte-contre-code, mots-pieges : « EACH » (toutes les copies de cote) ; 3 menaces ; ATQ 3 ; pas de citation.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 21[per_hero] -> "21*" ; MNG 2 ; ATQ 3 ; 3 menaces. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs078 : rouges 2/2
      - VERT : [ks] gs078 When Revealed (expert) : Kree Sentry (III) -> CHAQUE Poigne de cote s'attache a Rick Jones (deux copies mises de cote)
      - VERT : [ks] gs078 Forced Response (expert) : AUCUNE Poigne de cote -> 3 menaces sur la principale (2 -> 5)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : OUI : voir gs076

Carte terminee : OUI.

### gs079a : Sentry Awakens (1A)

- [x] Etape 2 : cartes de reference : WhenCardSetup (gs117a, 50087a) ; SetupCards.PutIntoPlay(.., under_control=True) ; AttacherUnePoigne
- [x] Etape 5 : texte-contre-code, mots-pieges : Rick EN JEU avant l'attache ; les deux Poignes commencent de cote (donnees du scenario) ; « Contents » porte par le JSON.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Aucun nombre sur la face A. Contents : 2 stades (expert : II et III) + 1 modulaire.
      Resultat : conforme.
- [x] Etape 7 : 2 cas sujets, 2 verts avec le module ; substitution : SUBST gs079a : rouges 2/2
      - VERT : [ks] gs079a Setup : Rick Jones en jeu sous le controle du premier joueur, UNE Poigne sur lui, l'autre mise de cote
      - VERT : [ks] gs079a Setup (expert) : Kree Sentry (II) revele a la mise en place, Rick Jones porte alors LES DEUX Poignes
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : OUI : Rick Jones et sa Poigne dessines (kree-sentry-plateau.test.ts ; calibre : table sans la Poigne de Rick -> 3 cas rouges)

Carte terminee : OUI.

### gs079b : Sentry Awakens (1B)

- [x] Etape 2 : cartes de reference : AfterResolveVillainPhaseStep (gs117b, 04096b) ; DealDamage (54035) ; bases StartingThreat / EscalationThreat / TargetThreat
- [x] Etape 5 : texte-contre-code, mots-pieges : « EACH character » (identites, allies, sbires) ; « for each copy attached to IT » ; une seule instance de degats (question Q3).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Depart 2[per_hero] -> "2*" ; escalade +1[per_hero] -> "1*" ; objectif 7[per_hero] -> "7*". Identiques.
      Resultat : conforme.
- [x] Etape 7 : 6 cas sujets, 6 verts avec le module ; substitution : SUBST gs079b : rouges 4/6 ⚠ un cas reste vert sans module
      - VERT : [ks] gs079b valeurs : menace de depart 2[per_hero] (un joueur : 2), aucune menace sur le complot du deck
      - VERT : [ks] gs079b Forced Response apres l'etape 1 : Rick Jones porte UNE Poigne -> 1 degat sur lui
      - VERT : [ks] gs079b Forced Response : DEUX Poignes sur Rick Jones -> 2 degats (une seule instance)
      - VERT : [ks] gs079b Forced Response : une Poigne sur le HEROS (identite) -> 1 degat sur l'identite ; Rick sans Poigne n'en subit pas
      - VERT : [ks] gs079b Forced Response : une Poigne sur un SBIRE (Shocker) -> 1 degat sur lui
      - VERT : [ks] gs079b Forced Response, TEMOIN : un allie SANS Poigne (Black Widow) n'est pas blesse
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs080a : Self-Destruct Sequence (2A)

- [x] Etape 2 : cartes de reference : WhenThisRevealed (gs118a) ; Search.EncounterCard + Reveal (60185) ; PlaceThreatOnSchemes "2*" ; PlaceAccelerationToken (50082)
- [x] Etape 5 : texte-contre-code, mots-pieges : « IF the side scheme is IN PLAY » ; « Otherwise, search the encounter deck AND discard pile » ; menace ET jeton sur la MEME carte.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 2[per_hero] menaces, 1 jeton d'acceleration. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs080a : rouges 3/3
      - VERT : [ks] gs080a When Revealed : Outpost Collapse Protocol EN JEU -> 2[per_hero] menaces et 1 jeton d'acceleration sur elle
      - VERT : [ks] gs080a When Revealed : Outpost Collapse Protocol dans le DECK RENCONTRE -> cherchee et revelee (Hinder 2 : 1 + 2 = 3)
      - VERT : [ks] gs080a When Revealed : Outpost Collapse Protocol dans la DEFAUSSE rencontre -> cherchee et revelee
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON (compteur d'acceleration dessine par le plateau existant, `k_acceleration_token`)

Carte terminee : OUI.

### gs080b : Self-Destruct Sequence (2B)

- [x] Etape 2 : cartes de reference : meme Reponse forcee que gs079b ; « If this stage is completed, the players lose » : regle du dernier stade (gs199b)
- [x] Etape 5 : texte-contre-code, mots-pieges : la phrase en gras n'est pas une capacite a coder ; « completes » imprime : coquille (question Q1).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Depart 1[per_hero] -> "1*" ; escalade +1[per_hero] ; objectif 10[per_hero] -> "10*". Identiques.
      Resultat : conforme.
- [x] Etape 7 : 4 cas sujets, 4 verts avec le module ; substitution : SUBST gs080b : rouges 1/4 ⚠ un cas reste vert sans module
      - VERT : [ks] gs080b valeurs : menace de depart 1[per_hero] sur le stade 2 (un joueur : 1)
      - VERT : [ks] gs080b Forced Response apres l'etape 1 : une Poigne sur Rick Jones -> 1 degat (stade 2)
      - VERT : [ks] gs080b : stade 2 accompli (menace 10[per_hero]) -> les joueurs perdent
      - VERT : [ks] gs080b : stade 2 non accompli (9 sur 10) -> pas de defaite
      Note : Le cas « 10 sur 10 -> defaite » mesure la regle du dernier stade : vert sans module (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs081 : Rick Jones

- [x] Etape 2 : cartes de reference : ThisNotCountAllyLimit (50091) ; WhenUnitWouldAttack + ReplaceTarget (50089b) + property.not_against_player (briques communes) ; AfterCardLeavePlay (gs121)
- [x] Etape 5 : texte-contre-code, mots-pieges : « attacks YOU » = le joueur que Rick sert ; « INSTEAD » ; « leaves play » = tout depart ; livret p.4 : « attacks you » ne part pas.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 5 (pastille orange), CTR 1, ATQ 2 avec deux etoiles = 2 degats consecutifs ("2**"), aucun cout. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 9 cas sujets, 9 verts avec le module ; substitution : SUBST gs081 : rouges 7/9 ⚠ un cas reste vert sans module
      - VERT : [ks] gs081 Forced Interrupt : Kree Sentry attaque le HEROS -> il attaque Rick Jones a la place (1 degat sur Rick, 0 sur le heros)
      - VERT : [ks] gs081 Forced Interrupt, TEMOIN : l'attaque contre un AUTRE joueur n'est pas detournee
      - VERT : [ks] gs081 Forced Interrupt : le detournement ne compte pas comme une attaque « contre vous » (Experimental Weapons ne part pas)
      - VERT : [ks] gs081 Forced Response (Experimental Weapons), TEMOIN : sans detournement, la meme carte fait defausser une carte
      - VERT : [ks] gs081 « If Rick Jones leaves play, the players lose the game » : Rick vaincu -> defaite
      - VERT : [ks] gs081 « If Rick Jones leaves play... » : Rick DEFAUSSE par un effet -> defaite
      - VERT : [ks] gs081 « If Rick Jones leaves play... », TEMOIN : un autre allie qui part ne fait pas perdre
      - VERT : [ks] gs081 « does not count against your ally limit » : trois allies + Rick Jones, 3 comptes dans la limite
      - VERT : [ks] gs081 Rick Jones attaque Kree Sentry (seule cible permise par sa Poigne) : ATQ 2 sur Kree Sentry, 2 degats consecutifs sur lui
      Note : Verts sans module (assume) : les temoins (autre joueur, autre allie) et les mesures de base (ATQ 2**, controle).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : OUI : Rick Jones dessine (allies) avec sa Poigne (kree-sentry-plateau.test.ts ; calibre : table sans la Poigne de Rick -> 3 cas rouges)

Carte terminee : OUI.

### gs082 : Sentry's Grasp

- [x] Etape 2 : cartes de reference : 54035 Encased in Ice (consider_as Minion, IfCardHasOrMoreCounters) ; UnitCannotThwartTarget (03028) ; EnemyCannotActivate (49007) ; WhenCardWouldLeavePlay + SetBeInstead (37034) ; refuse_target_fn (squirrel_girl)
- [x] Etape 5 : texte-contre-code, mots-pieges : « can ONLY attack Kree Sentry OR THIS card » ; « as if it were a MINION » = attaques seulement (livret p.9) ; « set it aside INSTEAD » ; seuil 3 (5 avec Death Grip) ; sur un sbire : aucune activation.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Seuil 3 degats ; aucun cout ; 2 exemplaires. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 15 cas sujets, 15 verts avec le module ; substitution : SUBST gs082 : rouges 7/15 ⚠ un cas reste vert sans module
      - VERT : [ks] gs082 « cannot thwart » : le heros porteur d'une Poigne ne contre pas (menace du complot inchangee)
      - VERT : [ks] gs082 « cannot thwart », TEMOIN : sans Poigne sur lui, le meme heros retire 1 menace (2 -> 1)
      - VERT : [ks] gs082 « can only attack Kree Sentry or this card » : le heros porteur attaque Kree Sentry (2 degats)
      - VERT : [ks] gs082 « can only attack Kree Sentry or this card » : un SBIRE (Shocker) n'est PAS une cible legale pour le porteur
      - VERT : [ks] gs082 « can only attack Kree Sentry or this card » : le porteur peut attaquer SA Poigne (2 degats sur elle)
      - VERT : [ks] gs082 « Any player can attack this card as if it were a minion » : un heros SANS Poigne attaque la Poigne de Rick (2 degats)
      - VERT : [ks] gs082 « If there is 3 or more damage here, set Sentry's Grasp aside » : 2 degats -> reste attachee
      - VERT : [ks] gs082 « ...3 or more damage here, set aside » : 3 degats -> remise de cote (plus attachee a Rick)
      - VERT : [ks] gs082 « Forced Interrupt: When this card would leave play, set it aside instead » : l'hote (Black Widow) est vaincu -> Poigne de cote
      - VERT : [ks] gs082 « ...set it aside instead » : la Poigne DEFAUSSEE par un effet est mise de cote (jamais en defausse)
      - VERT : [ks] gs082 degats effaces : une Poigne mise de cote revient SANS degat
      - VERT : [ks] gs082 sur un SBIRE : Shocker porteur ne peut pas s'activer (ni attaquer ni manigancer) ; le temoin attaque
      - VERT : [ks] gs082 sur un SBIRE, TEMOIN : sans Poigne, Shocker attaque le heros (2 degats)
      - VERT : [ks] gs082 « as if it were a minion » = pour les ATTAQUES seulement : la reponse de Valkyrie (« deal 2 damage to a minion ») ne vise pas la Poigne
      - VERT : [ks] gs082 « as if it were a minion », TEMOIN : la meme reponse de Valkyrie frappe un VRAI sbire (Shocker, 2 degats)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : OUI : Poigne attachee a un allie, un sbire, une identite et ses compteurs de degats dessines (kree-sentry-plateau.test.ts ; calibre : table sans la Poigne de Rick -> 3 cas rouges)

Carte terminee : OUI.

### gs083 : Optic Blast Cannon

- [x] Etape 2 : cartes de reference : UnitAttackGainKeyword (27147, gs129) ; PlayerActionToDiscardThis + Cost("RR") (01118) ; Boost : would_atk_message (50160) ; badge ATK+ (gs129)
- [x] Etape 5 : texte-contre-code, mots-pieges : « IF this activation is an attack » ; icones de ressource = deux poings = [physical][physical] (decoupe contre sk148 / sk152) ; piercing ET ranged.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : +1 ATQ, 1 icone de boost, Cost RR. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 9 cas sujets, 9 verts avec le module ; substitution : SUBST gs083 : rouges 6/9 ⚠ un cas reste vert sans module
      - VERT : [ks] gs083 Optic Blast Cannon : attache a Kree Sentry, +1 ATQ
      - VERT : [ks] gs083 « Kree Sentry's attacks gain piercing and ranged » : l'attaque (detournee sur Rick Tenace) defausse sa carte Tenace et fait 2 degats (1 + 1)
      - VERT : [ks] gs083 piercing, TEMOIN : sans Optic Blast Cannon, la carte Tenace de Rick absorbe l'attaque (0 degat)
      - VERT : [ks] gs083 ranged : l'attaque de Kree Sentry contre le Jailor (Riposte 1) ne subit pas de riposte
      - VERT : [ks] gs083 ranged, TEMOIN : sans l'arme, le Jailor riposte (1 degat sur Kree Sentry)
      - VERT : [ks] gs083 Hero Action : depenser [physical][physical] -> defausser Optic Blast Cannon
      - VERT : [ks] gs083 Hero Action, TEMOIN : sans [physical][physical] (deux [energy]) la carte reste attachee
      - VERT : [ks] gs083 Boost : l'activation recoit Optic Blast Cannon en boost -> l'attaque gagne piercing (Tenace de Rick defaussee), ATQ 1 + 1 icone = 2 degats
      - VERT : [ks] gs083 Boost : activation de MANIGANCE (alter ego) -> aucun effet de boost (menace 2 + SCH 2 + 1 icone)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : OUI : attache a Kree Sentry (plateau)

Carte terminee : OUI.

### gs084 : Repulsor Blast Unit

- [x] Etape 2 : cartes de reference : UnitAttackGainKeyword ; WhenCardWouldLeavePlay sur la Poigne (modele gs082) ; Boost (50160)
- [x] Etape 5 : texte-contre-code, mots-pieges : « 5 or more damage on IT » ; « overkill AND ranged » ; le boost ne donne que overkill.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : +1 ATQ, 1 icone de boost, 2 exemplaires, seuil 5. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 9 cas sujets, 9 verts avec le module ; substitution : SUBST gs084 : rouges 5/9 ⚠ un cas reste vert sans module
      - VERT : [ks] gs084 Repulsor Blast Unit : attache a Kree Sentry, +1 ATQ
      - VERT : [ks] gs084 « attacks gain overkill » : Kree Sentry (ATQ 2) abat Shocker a 1 PV, l'exces (1) va au mechant lui-meme
      - VERT : [ks] gs084 overkill, TEMOIN : sans l'unite, aucun exces ne retourne a Kree Sentry (ATQ 1, Shocker a 1 PV)
      - VERT : [ks] gs084 ranged : l'attaque de Kree Sentry contre le Jailor ne subit pas de riposte
      - VERT : [ks] gs084 Forced Interrupt : une Poigne a 5 degats (Death Grip en jeu) va etre mise de cote -> Repulsor Blast Unit defaussee
      - VERT : [ks] gs084 Forced Interrupt, TEMOIN : une Poigne mise de cote a 3 degats seulement -> Repulsor reste attachee
      - VERT : [ks] gs084 Forced Interrupt : 5 degats poses d'un coup SANS Death Grip (seuil 3) -> la Poigne part de cote avec 5 degats, Repulsor defaussee
      - VERT : [ks] gs084 Forced Interrupt, TEMOIN : 4 degats d'un coup (seuil 3) -> la Poigne part de cote mais Repulsor reste
      - VERT : [ks] gs084 Boost : l'attaque de l'activation gagne overkill (ATQ 1 + 1 icone, Shocker a 1 PV : 1 d'exces)
      Note : Les temoins (3 ou 4 degats, sans l'unite) verifient une absence : verts sans module (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : OUI : attache a Kree Sentry (plateau)

Carte terminee : OUI.

### gs085 : Death Grip

- [x] Etape 2 : cartes de reference : marquage gs_seuil_poigne a l'entree en jeu (modele squirrel_girl refuse_target_fn) lu par SeuilDeLaPoigne ; AfterCardLeavePlay
- [x] Etape 5 : texte-contre-code, mots-pieges : « INSTEAD of 3 » ; « 5 or MORE » ; Poigne a 3 ou 4 degats quand Death Grip s'en va (question Q4).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Menace de depart 3[per_hero] -> "3*" ; seuil 5 ; 1 icone de boost. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 5 cas sujets, 5 verts avec le module ; substitution : SUBST gs085 : rouges 2/5 ⚠ un cas reste vert sans module
      - VERT : [ks] gs085 valeurs : menace de depart 3[per_hero] (un joueur : 3), aucun Hinder
      - VERT : [ks] gs085 « set aside when there is 5 or more damage instead of 3 » : 3 degats -> la Poigne RESTE attachee
      - VERT : [ks] gs085 : 4 degats -> toujours attachee
      - VERT : [ks] gs085 : 5 degats -> mise de cote
      - VERT : [ks] gs085 : Death Grip s'en va avec une Poigne a 4 degats -> « 3 or more damage here » : elle tombe de cote aussitot
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs086 : Locking on Target

- [x] Etape 2 : cartes de reference : Hinder : base desc (hinder.md, 16066) ; Amplify : base desc (amplify.md, sk252)
- [x] Etape 5 : texte-contre-code, mots-pieges : icone « avion + croix » = Amplify (decoupe contre sk252 et gs133) ; Hinder 1[per_hero] ; aucun texte de regle.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Menace 3, Hinder 1[per_hero], Amplify 1, 2 icones de boost, 2 exemplaires. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 4 cas sujets, 4 verts avec le module ; substitution : SUBST gs086 : carte SANS module : substitution des DONNEES (Hinder et Amplify retires du desc dans cards.json, restaure par git) : rouges 3/4 (le temoin sans la carte reste vert, assume)
      - VERT : [ks] gs086 Hinder 1[per_hero] : revelee, 3 + 1 = 4 menaces (un joueur)
      - VERT : [ks] gs086 Amplify : l'icone « avion + croix » (identique a sk252) est comptee par le moteur
      - VERT : [ks] gs086 Amplify : l'activation de Kree Sentry (alter ego) qui retourne un boost a 1 icone en recoit une de plus (2 + SCH 2 + 1 + 1 = 6)
      - VERT : [ks] gs086 Amplify, TEMOIN : sans Locking on Target, la meme activation donne 2 + 2 + 1 = 5
      Note : AUCUN module (carte a mots-cles seuls) : la substitution porte sur les DONNEES (Hinder et Amplify retires du desc, cards.json restaure par git) ; le temoin « sans Locking on Target » reste vert (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs087 : Outpost Collapse Protocol

- [x] Etape 2 : cartes de reference : Hinder : base desc ; AfterResolveVillainPhaseStep (gs117b) ; DealDamage (54035)
- [x] Etape 5 : texte-contre-code, mots-pieges : « the FIRST player » ; « each character THEY CONTROL » (identite, allies, Rick Jones ; pas les sbires).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Menace 1, Hinder 2[per_hero], 2 icones de boost. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 4 cas sujets, 4 verts avec le module ; substitution : SUBST gs087 : rouges 2/4 ⚠ un cas reste vert sans module
      - VERT : [ks] gs087 Hinder 2[per_hero] : revelee, 1 + 2 = 3 menaces (un joueur)
      - VERT : [ks] gs087 Forced Response apres l'etape 1 : le premier joueur inflige 1 degat a chaque personnage qu'il controle (identite + Rick Jones)
      - VERT : [ks] gs087 Forced Response, TEMOIN : un sbire (Shocker) n'est pas un personnage que le joueur controle
      - VERT : [ks] gs087 Forced Response : seul le PREMIER joueur subit (deux joueurs : le second heros est intact)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs088 : "Gotcha!"

- [x] Etape 2 : cartes de reference : ThisCardGainSurge (40189) ; AttacherUnePoigne ; WhenCardBecomeBoost (an013)
- [x] Etape 5 : texte-contre-code, mots-pieges : « If you CANNOT » = plus de copie de cote ; l'etoile rouge seule du coin n'est pas une icone de boost.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Aucune icone de boost (etoile seule), 2 exemplaires. Identique.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs088 : rouges 3/3
      - VERT : [ks] gs088 When Revealed : la Poigne de cote s'attache a Rick Jones (2 sur lui)
      - VERT : [ks] gs088 When Revealed : AUCUNE Poigne de cote -> la carte gagne surge (la carte semee au dessus du deck est revelee)
      - VERT : [ks] gs088 Boost : l'activation retourne « Gotcha! » en boost -> la Poigne de cote s'attache a Rick Jones
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs089 : Caught in Its Sights

- [x] Etape 2 : cartes de reference : joueur.AskSpendResources(Cost("2")) (28024, bl015) ; Enemy.AttackCharacter (briques communes) ; PeutDepenserDeuxRessources (garde-fou de paiement partiel)
- [x] Etape 5 : texte-contre-code, mots-pieges : « YOU may spend » ; « 2 resources OF ANY TYPE » ; paiement partiel refuse ; l'attaque vise Rick Jones directement (les joueurs defendent).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Depense 2, 1 icone de boost, 2 exemplaires. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 3 cas sujets, 3 verts avec le module ; substitution : SUBST gs089 : rouges 2/3 ⚠ un cas reste vert sans module
      - VERT : [ks] gs089 When Revealed : le joueur depense 2 ressources -> Kree Sentry n'attaque pas Rick Jones
      - VERT : [ks] gs089 When Revealed : AUCUNE ressource a depenser -> Kree Sentry attaque Rick Jones (1 degat, une Poigne de plus)
      - VERT : [ks] gs089 attaque sur Rick Jones : le heros peut DEFENDRE (DEF 3 contre ATQ 1 : 0 degat, heros incline)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON

Carte terminee : OUI.

### gs090 : Intruder Elimination

- [x] Etape 2 : cartes de reference : DoAttackYou (16114, gs135) ; Enemy.AttackCharacter (briques communes) ; ThisCardGainSurge (40189)
- [x] Etape 5 : texte-contre-code, mots-pieges : « CHOOSE a non-KREE character » (question Q5) ; « (even if alter-ego) » ; surge seulement si un ENNEMI est attaque ; FAQ p.22.
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 2 icones de boost, 2 exemplaires. Identiques.
      Resultat : conforme.
- [x] Etape 7 : 4 cas sujets, 4 verts avec le module ; substitution : SUBST gs090 : rouges 4/4
      - VERT : [ks] gs090 When Revealed : cible = un SBIRE (Shocker) -> Kree Sentry l'attaque (1 degat) et la carte gagne surge
      - VERT : [ks] gs090 When Revealed : cible = l'identite du PREMIER joueur -> Kree Sentry attaque Rick Jones (FAQ p.22), pas de surge
      - VERT : [ks] gs090 When Revealed : cible = un ALLIE (Black Widow) -> Kree Sentry l'attaque, pas de surge
      - VERT : [ks] gs090 « non-KREE » : Kree Sentry n'est PAS une cible proposee
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible 20/10/2026 (tools/autoplay.py, deck spider_man) : 16 parties gs_kree_sentry profil equilibre (8 normal + 8 expert, graines 1-8) + 32 parties prudent/agressif (graines 20-27), temoin sk_paibok (meme auteur, meme deck) 16 parties equilibre. Kree Sentry : 48 parties, 0 victoire (le pilote attaque avec Rick Jones, dont les 2 degats consecutifs le tuent : « Players Lost » au round 1 ou 2, journal lu ligne a ligne sur la partie 1 : Rick Jones, Poigne attachee, degats de 1B, attaque detournee sur Rick, Poigne de l'attaque), 2 parties bloquees (graine 25 prudent, normal et expert) sur Hero_Action 01093 Tenacity « WhenPlayerInTurn failed », MEME blocage que le temoin Paibok (graines 2 et 7) : defaut preexistant, hors lot. grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback sur les 48 journaux Kree Sentry et les 16 du temoin : 0 partout. Cartes revelees vues dans les journaux : Sentry Awakens 1B (16 parties), Kree Sentry I et II, Self-Destruct Sequence 2A/2B, Outpost Collapse Protocol, Intruder Elimination, Repulsor Blast Unit, Guard Assembles (3), Warstar, Neutron, Mentor, Hobgoblin, Astra.
- [x] Etape 8 bis : NON

Carte terminee : OUI.

