# Baxter Stockman v3 (TMNT Villains / Modulars, Inkwire, `tx`) : gabarits PROCESSUS-CARTE

Preuves du 16/10/2026. Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_baxter.py` (prefixes `[baxter]` et `[dazed]`).
Scans : `.planning/tmnt/pics-baxter/`. Questions en attente : `.planning/tmnt/baxter-questions.md`.

Resume des preuves transversales (voir `baxter-phase-a.md`) : substitution `tools/substituer_pack.py .game-src <port> tx`, `verifier_appels_modules.py` (calibre : un appel inexistant le fait tomber), autoplay solo et 2 joueurs, normal et expert.

---

### tx001 : * Baxter Stockman (I), Villain

- [x] Etape 2 : carte(s) de reference : FI debut de phase / « each player resolves the Special » : `tx011` Mad Lab (meme declencheur) et `60199` Tombstone (`WhenVillainPhaseBegin`) ; Special : `ab007` / zeus `ResoudreLeSpecialDe` ; Toughness : `01076` (natif).
- [x] Etape 5 : texte-contre-code : mots-pieges : each player (tous, premier joueur d'abord) ; resolves (le joueur resout, « engaged with YOU ») ; When the villain phase BEGINS (debut, pas fin) ; Toughness natif. Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 13*, ATK 0, SCH 1, Stage I, Toughness 1, traits AERIAL FLY GENIUS : identiques au scan (cas `nombres imprimes`). Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacite 1 (Toughness, natif) : cas `tx001 Baxter Stockman I : PV 13...` (carte Tough a l'entree) ; capacite 2 (FI) : cas `tx001 Forced Interrupt ...` x7 (compteur, carte face cachee, non-SWARM, 2 joueurs x3), temoin `sans debut de phase`.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx001 `) : ROUGES 5/9 ; restent verts sans module (assumes) : base native / absence `tx001 Baxter Stockman I : PV 13 par joueur (solo 13), Toughness (carte Tough a l`; base native / absence `tx001 Baxter Stockman I : PV 13 par joueur (2 joueurs : 26)`; temoin `tx001 TEMOIN `; cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee).
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---

### tx002 : * Baxter Stockman (II), Villain

- [x] Etape 2 : carte(s) de reference : When Revealed + recherche pioche/defausse : `sk142` Paibok II (`Search.EncounterCard(include_discard_pile=True)` + `Reveal`) ; FI : `tx001`.
- [x] Etape 5 : texte-contre-code : mots-pieges : encounter deck AND discard pile (cas defausse seule) ; the Baxter Blaster attachment (card_id tx005) ; reveal it (revelee, pas posee) ; (Shuffle.) = comportement natif. Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 16*, ATK 1, SCH 2, Stage II, Toughness 1. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacite 1 (When Revealed) : cas `tx002 When Revealed` x3 (deck, defausse, aucun Blaster) + `EXPERT : Baxter II en jeu des la mise en place` ; capacite 2 (FI) : cas `tx002 Forced Interrupt`.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx002 `) : ROUGES 4/6 ; restent verts sans module (assumes) : base native / absence `tx002 When Revealed : aucun Blaster nulle part : rien ne plante, rien n'est reve`; cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---

### tx003 : * Baxter Stockman (III), Villain

- [x] Etape 2 : carte(s) de reference : chaque sbire gagne guard : `sk091` (`GiveKeywordToInPlayWhenApplyThis(CardFinder2(trait, Minion), guard=1)`) ; carte face cachee a chaque joueur : `56138` (`Utility.DealEachPlayerEncounterCard`) ; FI : `tx001`.
- [x] Etape 5 : texte-contre-code : mots-pieges : EACH SWARM minion (tous, y compris de Donatello) ; gains GUARD (mot-cle chiffre) ; Deal EACH player 1 facedown encounter card. Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 19*, ATK 2, SCH 2, Stage III, Toughness 1. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacite 1 (guard) : cas `tx003 : Each SWARM minion gains guard` + temoin stade II ; capacite 2 (When Revealed) : cas solo / 2 joueurs / temoin ; capacite 3 (FI) : cas `tx003 Forced Interrupt`.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx003 `) : ROUGES 4/7 ; restent verts sans module (assumes) : temoin `tx003 TEMOIN `; temoin `tx003 TEMOIN `; cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---

### tx004a : Baxter's Laboratory 1A, MainScheme

- [x] Etape 2 : carte(s) de reference : `hs004a` Rats and More Rats (`Find.FindAndPutIntoPlay` par joueur) ; `sp001a` (`WhenCardSetup`).
- [x] Etape 5 : texte-contre-code : mots-pieges : A Plague minion engaged with EACH player (un par joueur) ; Content = regle (scenario JSON). Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Stage 1A. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacite 1 (Setup) : cas `tx004a Setup (solo)` et `(2 joueurs)`.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx004a `) : ROUGES 2/3 ; restent verts sans module (assumes) : cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---

### tx004b : Baxter's Laboratory 1B, MainScheme

- [x] Etape 2 : carte(s) de reference : `ab007` / `zeus` (`WhenResolveSpecialAbility`) ; `gmw/16034` (all-purpose counter) ; `ar012` (`DealEncounterCards`).
- [x] Etape 5 : texte-contre-code : mots-pieges : engaged with YOU ; each SWARM minion ; If there are NO SWARM minions ; deal YOURSELF ; all-purpose = type de la carte porteuse (FAQ). Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : StartingThreat 1*, TargetThreat 11*, EscalationThreat 1*, Stage 1B. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacite 1 (Special Replicate) : cas `tx004b Replicate` x6 + `tx001 Forced Interrupt` ; capacite 2 (perdre si achevee) : cas `tx004b « If this scheme is completed »` + temoin.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx004b `) : ROUGES 6/11 ; restent verts sans module (assumes) : base native / absence `tx004b menace : depart 1 par joueur, cible 11 par joueur (solo : 1 / 11)`; base native / absence `tx004b menace : depart 1 par joueur, cible 11 par joueur (2 joueurs : 2 / 22)`; base native / absence `tx004b « If this scheme is completed, the players lose the game » : menace a la `; temoin `tx004b TEMOIN `; cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---

### tx005 : * Baxter Blaster, Attachment

- [x] Etape 2 : carte(s) de reference : `01118` Sonic Converter ; `aa018` (deux couts alternatifs) ; `04132` Luger (`WhenThisBoostAttachTo`).
- [x] Etape 5 : texte-contre-code : mots-pieges : Baxter Stockman = le VILAIN (pas td015) ; attacks AND damages ; daze THEM ; Exhaust your HERO / spend 2 resources of ANY type ; Hero Action. Resultat : conforme (ATQ ★ : TODO-QUESTION Q1).
- [x] Etape 6 : nombres texte <-> code : Boost 0 (etoile seule), traits TECH WEAPON. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacites : Attach (cas homonyme td015), Forced Response (3 cas dont temoin et coup prevenu), Hero Action exhaust (1), Hero Action 2 ressources (1), offre de l'action par forme (2), Boost (1).
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx005 `) : ROUGES 7/11 ; restent verts sans module (assumes) : temoin `tx005 TEMOIN `; base native / absence `tx005 « attacks AND damages » : un coup entierement prevenu (Tough) n'hebete pas`; base native / absence `tx005 ATQ « ★ » : AUCUN bonus d'ATQ (TODO-QUESTION Q1) : Baxter II garde son ATQ`; cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI, sous reserve de la question Q1 (l'etoile de la case ATQ n'a aucune valeur imprimee ; lecture provisoire : aucun bonus, marquee TODO-QUESTION dans `tx005.py`, cas dedie).

---

### tx006 : Swarm Superiority, Attachment (x2)

- [x] Etape 2 : carte(s) de reference : `sk177` (`AttachToFaceWhenPutIntoPlay(..., if_cannot_gain_surge=True)`) ; `GiveKeywordToAttached(trait, guard)` ; `gmw/16034`.
- [x] Etape 5 : texte-contre-code : mots-pieges : a SWARM minion (trait) ; If you CANNOT (surge) ; gains AERIAL AND guard ; 2 counters on ATTACHED minion. Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Boost 1, CONDITION. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacites : Attach + 2 compteurs + AERIAL/guard (1), temoin (1), defausse (1), surge sans SWARM (1), surge avec non-SWARM (1).
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx006 `) : ROUGES 4/6 ; restent verts sans module (assumes) : temoin `tx006 TEMOIN `; cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---

### tx007 : Plague of M.O.U.S.E.R.S., Minion (x4)

- [x] Etape 2 : carte(s) de reference : `td016` Plague of M.O.U.S.E.R.s (meme texte, `CapacitesEssaim`), fiche swarm.md.
- [x] Etape 5 : texte-contre-code : mots-pieges : SCH, ATK AND hit points ; that MANY ; INSTEAD. Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Boost 1, MOUSERS SWARM, PV/ATQ/MNG dynamiques (0 dans desc). Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacites : compteurs a l'entree + stats, degats remplaces (1 degat, mort), croissance par le Special.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx007 `) : ROUGES 4/5 ; restent verts sans module (assumes) : cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---

### tx008 : Radical Ingenuity, Treachery (x3)

- [x] Etape 2 : carte(s) de reference : `08013` / `16155` (`ChooseAbilities`) ; Special : `tx004b`.
- [x] Etape 5 : texte-contre-code : mots-pieges : Choose (une puce) ; Resolve the Special par le joueur qui revele ; Place 2 threat on the main scheme. Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Boost 2. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacites : option 1 (+ sans SWARM), option 2.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx008 `) : ROUGES 3/4 ; restent verts sans module (assumes) : cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---

### tx009 : Rapid Replication, Treachery (x3)

- [x] Etape 2 : carte(s) de reference : `sk145b` `RevelerPouvoirDuDeck` (`DiscardEncounterCardsUntil` + `Reveal`).
- [x] Etape 5 : texte-contre-code : mots-pieges : until a MINION is discarded ; Reveal THAT minion ; THEN Special (meme sans sbire). Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Boost 2. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacites : cas nominal, sbire en bas du deck, sbire en defausse (remelange), aucun sbire.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx009 `) : ROUGES 4/5 ; restent verts sans module (assumes) : cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---

### tx010 : Robotics Facility, SideScheme (x3)

- [x] Etape 2 : carte(s) de reference : bases automatiques : `01108` (Crisis), `01109` (Acceleration), `16066` (Hinder).
- [x] Etape 5 : texte-contre-code : mots-pieges : 4 SANS icone de joueur ; Hinder 1 PAR JOUEUR s'ajoute ; icones Acceleration + Crisis verifiees par decoupe (IoU 0,86 / 0,93). Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : StartingThreat 4, Hinder 1*, Boost 1, Acceleration 1, Crisis 1. Resultat : conforme.
- [x] Etape 7 : cas par capacite : module vide (bases automatiques) : cas menace solo/2 joueurs, icones portees, Crisis bloque le contre + temoin. La substitution laisse tout vert : le module est deja vide, la preuve est le cas `icones` et le temoin Crisis.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx010 `) : module VIDE par construction (Hinder, Acceleration, Crisis, Boost sont des bases `desc`) : la substitution ne change rien (0/6 rouges), la preuve est dans les cas `icones`, `Crisis` + temoin et les menaces de depart ; ROUGES 0/6 ; restent verts sans module (assumes) : base native / absence `tx010 Robotics Facility : 4 menaces de depart FIXES + Hinder 1 par joueur (solo `; base native / absence `tx010 Robotics Facility (2 joueurs) : 4 fixes + Hinder 2 = 6`; base native / absence `tx010 icones : Acceleration et Crisis portees (desc), lues en jeu`; base native / absence `tx010 Crisis : le complot principal ne peut plus etre contre (menace 5 reste 5)`; temoin `tx010 TEMOIN `; cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---

### tx011 : Mad Lab, SideScheme (x2)

- [x] Etape 2 : carte(s) de reference : `tx001` (declencheur) ; `Worlds.GetFirstPlayer`.
- [x] Etape 5 : texte-contre-code : mots-pieges : the FIRST player (un seul) ; MUST. Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : StartingThreat 2*, Boost 1. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacite 1 (FI) : cas 2 joueurs (3 et 4) + temoin (3 et 3).
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx011 `) : ROUGES 1/5 ; restent verts sans module (assumes) : base native / absence `tx011 Mad Lab : 2 menaces par joueur (solo 2, 2 joueurs 4)`; base native / absence `tx011 Mad Lab (2 joueurs) : 4 menaces`; temoin `tx011 TEMOIN `; cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---

### tx012 : Flight of Flyborgs, Minion (x3)

- [x] Etape 2 : carte(s) de reference : `td017` + `tx007` (`CapacitesEssaim(4)`).
- [x] Etape 5 : texte-contre-code : mots-pieges : idem tx007 ; trait FLYBORG singulier (Q4). Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Boost 2, AERIAL FLYBORG SWARM. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacites : 4 compteurs + stats + traits, 3 degats, 9 degats.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx012 `) : ROUGES 2/4 ; restent verts sans module (assumes) : base native / absence `tx012 : 9 degats sur 4 compteurs : vaincu par le moteur`; cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI, sous reserve de la question Q4 (trait FLYBORG singulier imprime, td014 ne la trouvera pas).

---

### tx013 : * Superfly, Minion

- [x] Etape 2 : carte(s) de reference : `27067` Sand Clone / `td016` (SCH et ATQ suivent un compteur).
- [x] Etape 5 : texte-contre-code : mots-pieges : seuls SCH et ATQ suivent (PV imprimes 5, pas de « remove counters instead ») ; compteur Ooze. Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 5, Boost 3. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacites : entree 2 ooze, Special +1, 2 degats reels, 5 degats.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx013 `) : ROUGES 3/5 ; restent verts sans module (assumes) : base native / absence `tx013 : 5 degats vainquent Superfly (PV 5)`; cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI, sous reserve de la question Q4 (trait FLYBORG singulier imprime).

---

### tx014 : Buzz Off, Treachery (x2)

- [x] Etape 2 : carte(s) de reference : `tx008` (Choose) ; `wd111` (degats a l'identite).
- [x] Etape 5 : texte-contre-code : mots-pieges : Choose ; TAKE 2 damage = l'identite. Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Boost 1. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacites : option menace, option degats.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx014 `) : ROUGES 2/3 ; restent verts sans module (assumes) : cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---

### tx015 : Roadkill Rodneys, Minion (x3)

- [x] Etape 2 : carte(s) de reference : `ThisGainKeyword` (tx013) ; `dz020` Klaw (`AfterUnitAttackAndDamageUnit`) ; `Faces.RemoveCountersOn`.
- [x] Etape 5 : texte-contre-code : mots-pieges : +1 ATK FOR EACH cable ; attacks AND damages ; daze THAT character ; EACH cable counter. Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 3, ATK 1, SCH 1, Boost 2, Quickstrike 1. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacites : entree 1 cable (ATQ 2), Special (ATQ 3), Reponse forcee (Dazed + cables retires), temoin coup prevenu.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx015 `) : ROUGES 4/5 ; restent verts sans module (assumes) : cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---

### tx016 : Wrapped Up, Treachery (x2)

- [x] Etape 2 : carte(s) de reference : `td005` (friendly characters) ; RECETTES §2 (retour de GiveStatus) ; `ThisCardGainSurge`.
- [x] Etape 5 : texte-contre-code : mots-pieges : a FRIENDLY character ; If you CANNOT (surge). Resultat : conforme (Q2).
- [x] Etape 6 : nombres texte <-> code : Boost 1. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacites : un personnage hebete, avec allie, surge si tout est deja hebete, temoin sans surge.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx016 `) : ROUGES 4/5 ; restent verts sans module (assumes) : cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI, sous reserve de la question Q2 (qui choisit le personnage hebete ; lecture provisoire : le joueur qui revele, parmi tous les personnages amis).

---

### tx017 : Auto Defense Bots, Minion (x4)

- [x] Etape 2 : carte(s) de reference : `ss021` / `lj015` (`WhenUnitWouldBeDefeated` + `SetBeInstead`) ; `sk287` (soin).
- [x] Etape 5 : texte-contre-code : mots-pieges : would be DEFEATED ; heal ALL ; remove 1 shield ; INSTEAD. Resultat : conforme (Q3).
- [x] Etape 6 : nombres texte <-> code : HP 1, ATK 1, SCH 0, Boost 1, Guard 1, Patrol 1. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacites : entree 1 shield, survie, defaite sans shield, deux boucliers (Special).
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx017 `) : ROUGES 3/5 ; restent verts sans module (assumes) : base native / absence `tx017 : sans bouclier, le coup suivant le vainc (le texte n'a plus rien a retire`; cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI, sous reserve de la question Q3 (plus aucun compteur shield ; lecture provisoire : vaincu normalement).

---

### tx018 : Intruder Alert!, Attachment (x3)

- [x] Etape 2 : carte(s) de reference : `ma017` (`CostFunc.TakeDamage`) ; `aa018` ; `wd111` ; `04092` (`RevealThisCard`).
- [x] Etape 5 : texte-contre-code : mots-pieges : Take 2 damage ; exhaust your IDENTITY ; Action (deux formes) ; Crisis. Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Boost 1 + etoile, Crisis 1. Resultat : conforme.
- [x] Etape 7 : cas par capacite : capacites : attache, Crisis, action degats, action inclinaison (alter-ego et heros), Boost.
      Preuve par substitution (module remplace par un stub, cas filtres sur `tx018 `) : ROUGES 6/7 ; restent verts sans module (assumes) : cas `nombres imprimes` (desc, sans module par construction)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : voir le bilan global (`baxter-phase-a.md`) : 32 parties jouees (solo et 2 joueurs, normal et expert, 8 chacune), 0 traceback, 0 NameError/AttributeError/TypeError/KeyError/AssertionError ; 1 partie `bloquee` (Tenacity 01093, defaut du pilote deja documente, sans rapport avec le scenario)
- [x] Etape 8 bis : voir `ui-app/src/board/tmnt-baxter-plateau.test.ts` (cartes qui attachent, compteurs, statut) ; cartes qui ne font que chiffrer ou distribuer : sans cas plateau.

Carte terminee : OUI

---
### dazed : carte d'état Dazed (Hébété), 6e état du moteur

- [x] Étape 2 : carte(s) de référence : `cloaked.py` (même forme : trois déclencheurs, un seul consommateur, `AbilityType.Status`),
      `tough.py` (priorité), `exposed.md` (recette d'une carte d'état maison, 11 points de contact), fiche `dazed.md`.
- [x] Étape 5 : texte-contre-code (scan `Dazed (1).png` + encart `Dazed Rules Insert.png`) : « uses a basic power OR activates » (pouvoir de
      base du héros/allié = `WhenUnitUseBasicPower`, ennemi = `WhenEnemyActivateAgainstYou`) ; « decrease that value by 2 » (minimum 0) ;
      « would take ANY AMOUNT of damage » (au moins 1) ; « increase by 2 » ; « then discard » ; un seul Dazed par personnage ; Steady / Stalwart
      sans effet ; Tough d'abord ; Cloaked et Dazed simultanés. Résultat : conforme.
- [x] Étape 6 : nombres : -2 / +2 / 1 carte maximum. Résultat : conforme.
- [x] Étape 7 : 23 cas `[dazed]` : -2 ATQ, -2 CTR (min 0), -2 ATQ d'ennemi, -2 MNG d'ennemi, +2 aux dégâts, un seul effet (deux ordres), un seul
      Dazed (par `Faces.GiveStatus`), Tough d'abord (deux ordres de pose), zéro dégât réel, Cloaked + Dazed simultanés (dégâts, attaque),
      Cloaked seul inchangé, défense (-2 DEF, pas de +2 sur l'excès) + témoins. Substitution du module `dazed.py` par un stub : 10 cas nominaux
      rouges sur 21 (verts : les témoins, la pose, la limite « un seul » de `can_status.py`) ; mutations : sans la priorité de Tough le cas
      « Dazed posé avant Tough » est rouge ; `cloaked.py` ramené à l'origine : le cas de simultanéité sur les dégâts est rouge. Résultat : prouvé.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : Blaster, Rodneys et Wrapped Up posent Dazed dans les 32 parties (0 traceback).
- [x] Étape 8 bis : la carte change ce qu'on VOIT (statut) : `tmnt-baxter-plateau.test.ts` (4 cas : identité, allié, ennemi, avec Cloaked),
      `effets-statuts.test.ts`, `mobile/etats.test.ts` ; vus ROUGES sans le correctif (`compter()` donnait `NaN`, `etatDe` retombait sur
      « D / Dazed »).

Carte terminée : OUI (non prouvé : Dazed + attaque perforante, Dazed sur allié à dégâts consécutifs, voir `baxter-phase-a.md`).
