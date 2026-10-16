# Venus (TMNT Heroes v3, Inkwire) : gabarits PROCESSUS-CARTE

Preuves du 16/10/2026. Pack `venus` (prefixe `tv`, set 183 PROVISOIRE), 20 card_id :
`tv001a`, `tv001b`, `tv002`-`tv014`, `tv015` (obligation), `tv016`-`tv019` (set nemesis).
Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_venus.py` (prefixe `[venus]`, **82 cas, tous verts** :
`test_capacites.py .game-src <port> <rapport> "[venus]"`, PARALLELES=4). Substitution :
`tools/substituer_pack.py .game-src 44000 tv` (base de ports <= 48000 : 60 ports par carte), **18/18**
cartes avec module rouges sans leur module (`tv008` Evanescence et `tv016` Lab n'ont AUCUN module : base
`desc`/ressource, assumes ci-dessous). Les cas restes verts sous substitution sont des TEMOINS D'ABSENCE
(refus par cout impayable, forme alter-ego, « jamais un sbire »), des valeurs imprimees (`desc`) ou
des icones natives (Boost, Hazard) : assumes carte par carte.

Autres gates : `tools/test_cards.py` (6433 ok, 0 erreur), `tools/verifier_appels_modules.py venus` OK
(calibre : `Faces.MethodeInexistanteVenus` dans un module jetable le fait tomber), `verifier_api_cartes.py`
(aucun probleme dans `venus`), `DECK_NOM=venus tools/verifier_tous_les_decks.py` : `identite tv001a, main 6,
deck 8` (temoin raphael : OK), legalite des decks (aucune carte signature etrangere). Autoplay :
`tools/autoplay.py --deck venus`, **24 parties** (rhino + klaw, normal ; 8 equilibre + 16 prudent), 0
traceback, 0 incident ; temoin `raphael` (8 parties rhino + klaw, equilibre) : 0 victoire sur 8 pour les deux
(aucune moitie d'aspect : les decks homebrew a `player_deck` vide perdent en 4 a 6 rounds, Venus 5,2 rounds
contre rhino, Raphael 6,5).
Plateau (etape 8 bis) : `ui-app/src/board/tmnt-venus-plateau.test.ts`, 24 cas verts
(`cd ui-app && npx vitest run src/board/tmnt-venus-plateau.test.ts`), tsc vert. Sensibilite prouvee en
CASSANT puis restaurant : (A) l'entree `dredge` de `compteurs-fr.ts` -> 1 rouge (`compteurs-fr.test.ts`) ;
(B) `attachees` de `zones.ts` (l. 343) -> 9 rouges sur 24 (ameliorations, statuts Tough / Stunned / Confused) ;
(C) `posees(notre?.dealt_encounter_cards)` de `zones.ts` (l. 872) -> 1 rouge (carte de boost donnee face
cachee). Aucun vrai trou d'affichage trouve.

Icones de ressource verifiees par decoupe contre `01020` (G : etoile verte sur fond vert), `01021` (B),
`01023` (R), `01025` (Y) : les 13 cartes de deck (`tv002`-`tv014`) portent la MEME etoile verte = wild
(`RES = G`, `tv008` : trois icones = `GGG`). L'icone « ✶ resource » du texte (`tv005`, `tv011`) est le glyphe
wild du texte officiel (`01008` Web-Shooter : « generate a ✶ resource »). L'icone centrale de `tv015` et de
`tv016` (carte inclinee + croix) est celle de `01107` Breakin' & Takin' : **Hazard 1** (question Q2).

Decisions de l'utilisateur appliquees (cas analogues) : « Raphael » en forme civile = l'IDENTITE
(`tv011` Dragon Scale se paie aussi en forme Bonnie ; compteurs sur l'identite) ; fidelite 100 % (X libre,
zero compris, sur `tv003`) ; `player_deck` VIDE ; aucune paire jumelle declaree (candidates `tv011` Dragon Scale
/ `tv014` Turtle Shell, scans 12 et 15 : illustration probablement continue, A CONFIRMER).
Questions en attente : `.planning/tmnt/venus-questions.md` (Q1 plafond 6 de `tv001a`, Q2 icone Hazard de
l'obligation, Q3 ressources wild comptees par `tv005`). Aucune partie humaine dans le navigateur n'a ete jouee.

### tv001a : * Venus (face héros)

- [x] Étape 2 : carte(s) de référence : `tr001a`/`tr009` (compteur sur l'identité, `maximum=`), `ra001a` (`LimitOncePerRound`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « for EACH ELEMENT upgrade YOU control » (trait, pas nom), « to a MAXIMUM of 6 » (TODO-QUESTION Q1 : plafond du stock), « Limit once per round ».
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : PV 10, ATQ 1, CTR 2, DEF 2, main 4 (cas `valeurs imprimees`), plafond 6.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 5 cas rouges sans module (3 ELEMENT -> 3 ; armure non comptée tv009 vert témoin ; zéro ELEMENT ; plafond 6 ; limite) ; verts assumés : Action absente en alter-ego, valeurs.
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? OUI. Témoin d'épuisement : `limite 1 par round` (3 compteurs, un 4e ELEMENT entre en jeu, 2e Action refusée : 3 et non 7).
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), grep tracebacks : 0, lecture du journal : la carte est jouée / résolue dans les journaux (lignes « s’active » relevées).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « 3 / 6 compteurs de dragage visibles », « forme alter-ego », « compteurs retirés », « pas sur l'amélioration ». Rouge en cassant `compteurs-fr` (A).

Carte terminée : OUI

### tv001b : * Bonnie (face alter-ego)

- [x] Étape 2 : carte(s) de référence : `tm001b` (Setup `WhenCardSetup`), `br009`/`mots-cles/seek.md` (`DiscardDeckUntil`), `ra001b` (Action de soin, `Friend`, `LimitOncePerRound`), `tr013` (coût en compteurs).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « Setup » = mise en place du personnage ; « until you discard AN ELEMENT UPGRADE » ; « Remove 1 dredge counter from BONNIE -> » = coût ; « FRIENDLY character » (pas un sbire) ; « Limit once per round ». Piège moteur : deck épuisé, la défausse est remélangée (`DefausserJusquA`).
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : PV 10, REC 4, main 6 ; soin 2 ; 1 compteur.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 6 cas rouges sans module sur 10 (+ Setup sans ELEMENT durci : témoin 01075 en défausse, rouge confirmé à la main) ; verts assumés : Action sans compteur, jamais un sbire, valeurs.
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? OUI. Témoin d'épuisement : `limite 1 par round` (2 compteurs, 4 dégâts : après la 1re Action 2 dégâts et 1 compteur restent, 2e refusée).
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), grep tracebacks : 0, lecture du journal : la carte est jouée / résolue dans les journaux (lignes « s’active » relevées).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « Setup : l'amélioration ELEMENT est attachée à l'identité, traversée en défausse ». Rouge en cassant `attachees` (B).

Carte terminée : OUI

### tv002 : * Bludgeon

- [x] Étape 2 : carte(s) de référence : `tl002` Splinter (`AfterCardEnterPlay`, `SetTarget(from_where=["YourDiscardPile"])`, `Faces.MoveAllToDeck(..., "Top")`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « 1 card from YOUR discard pile » (libre, pas seulement spécifique), « on TOP », Réponse (pas Hero Response).
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : coût 3, PV 3, ATQ 2*, CTR 2* (conséquent 1 chacun), x1.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 2 cas rouges (carte remontée au sommet ; choix libre y compris une carte Hero) ; vert assumé : statistiques `desc`.
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), grep tracebacks : 0, lecture du journal : la carte est jouée / résolue dans les journaux (lignes « s’active » relevées).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « Bludgeon » : allié dessiné, pile du deck = carte du dessus dos visible (2 cartes), défausse sans la carte remontée.

Carte terminée : OUI

### tv003 : Arc Nova

- [x] Étape 2 : carte(s) de référence : `kb001a`/`16006` (X par `DeclareNumber`), `tg003` (`AskChooseFaces`), `td006` (dégâts d'événement d'attaque).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « X » libre zéro compris (retrait fait à la main, `CostFunc.Counter` refuse 0), « 4 damage to X ENEMIES » (ennemis distincts, vilain ET sbires ; moins d'ennemis que X : compteurs perdus), « Venus » = identité, label `attack`.
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : coût 2, 4 dégâts, X compteurs ; scan « 2/16 » = coquille de l'auteur.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 4 cas rouges (X=2 deux ennemis dont un vaincu ; X=1 ; X=3 pour 1 ennemi ; …) ; verts assumés : X=0 (absence), sans compteur, injouable en alter-ego.
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), grep tracebacks : 0, lecture du journal : la carte est jouée / résolue dans les journaux (lignes « s’active » relevées).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Compteurs retirés dessinés (cas « compteurs retirés »).

Carte terminée : OUI

### tv004 : Brain Burn

- [x] Étape 2 : carte(s) de référence : `tg003`/`42006` (thwart d'événement), `tr004` (statuts), `01165` Eviction Notice (`MayChooseOneAbility` + coût), helper `ProposerRetraitDragage`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « You MAY remove 2 dredge counters ... to confuse AND stun AN enemy » (facultatif, option « Cancel », les DEUX statuts sur UN ennemi, ciblé parmi ceux qui peuvent en recevoir), 2 menaces d'abord.
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : coût 1, 2 menaces, 2 compteurs, x2.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 3 cas rouges sur 3 (retrait seul via Cancel ; choix accepté : menace 5 -> 3, Confused + Stunned ; un seul compteur : branche non offerte).
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), grep tracebacks : 0, lecture du journal : la carte est jouée / résolue dans les journaux (lignes « s’active » relevées).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « Sonné ET Désorienté : les deux cartes de statut sur le vilain ». Rouge en cassant `attachees` (B).

Carte terminée : OUI

### tv005 : Eldritch Lance

- [x] Étape 2 : carte(s) de référence : `td006` (Overkill par `AttackProperty`), `tr006` (`GetPaidResources`), `mots-cles/overkill.md`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « [WILD] resource used to PAY » = `GetPaidResources().g` (TODO-QUESTION Q3 : surplus compté), « gains OVERKILL » (excès au vilain), label `attack`.
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : coût 4, 5 dégâts, 1 carte par wild.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 3 cas rouges (sans wild : 0 carte ; Evanescence + Energy : 3 cartes ; overkill : Hydra 3 PV -> 2 sur Rhino) ; vert assumé : injouable en alter-ego.
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), grep tracebacks : 0, lecture du journal : la carte est jouée / résolue dans les journaux (lignes « s’active » relevées).
      Résultat : OK.
- [x] Étape 8 bis : NON : ne fait que chiffrer (dégâts, pioche).

Carte terminée : OUI

### tv006 : Quantanucleic Acid

- [x] Étape 2 : carte(s) de référence : `19001a`/`tg010` (`GiveStatus("Tough")`), `ProposerRetraitDragage`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « Give VENUS a tough status card » (identité en forme héros), « You MAY remove 2 ... to draw 2 cards » (facultatif, coût), pas de label.
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : coût 1, 2 compteurs, 2 cartes.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 3 cas rouges sur 3 (Tough + refus ; accepté : 2 cartes piochées, compteurs 2 -> 0 ; 1 compteur : pas de pioche).
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), grep tracebacks : 0, lecture du journal : la carte est jouée / résolue dans les journaux (lignes « s’active » relevées).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « Venus porte une carte d'état Tenace » (statut attaché à l'identité).

Carte terminée : OUI

### tv007 : Resistance

- [x] Étape 2 : carte(s) de référence : `bl006` Vampiric Reflexes (même 1re phrase : `WhenUnitWouldTakeDamage(HeroInterrupt, "You", is_from_attack=True)` + `PreventDamage("All")`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « from an ATTACK » (traîtrise non prévenue), « prevent ALL damage », « You MAY remove 2 ... draw 3 », Hero Interrupt (forme héros seulement).
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : coût 2, 2 compteurs, 3 cartes, x2.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 2 cas rouges (prévention totale ; accepté : 3 cartes) ; verts assumés : témoin sans carte, dégâts hors attaque, injouable en alter-ego.
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), grep tracebacks : 0, lecture du journal : la carte est jouée / résolue dans les journaux (lignes « s’active » relevées).
      Résultat : OK.
- [x] Étape 8 bis : NON : prévention et pioche, rien de nouveau à dessiner.

Carte terminée : OUI

### tv008 : Evanescence

- [x] Étape 2 : carte de référence : `td007` Inspired Brilliance (ressource sans texte, aucun module).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : aucune capacité imprimée (citation seule) ; icônes `GGG` vérifiées par découpe (3 étoiles vertes).
      Résultat : OK.
- [x] Étape 6 : nombres : RES `GGG`, aucun coût.
      Résultat : OK.
- [x] Étape 7 : cas : `tv008 Evanescence : trois jokers paient SEULS Bludgeon (coût 3)` (vert avec le module absent par construction : aucun module, base `desc`, assumé) ; mesure aussi `tv005` (3 jokers = 3 cartes).
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), tracebacks : 0, lecture du journal : payée en cours de partie (lignes « gagne la ressource GGG »).
      Résultat : OK.
- [x] Étape 8 bis : NON : ressource, rien à dessiner.

Carte terminée : OUI

### tv009 : * Arcane Emitting Diode

- [x] Étape 2 : carte(s) de référence : `tr011` (amélioration d'attaque qui s'incline, `heros.DealDamage`), `27183b` (`CostFunc.DiscardDeckTopCards`), `td011` (`CanPlayThisUpgradeCard`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « Exhaust this card AND discard the top 2 cards » : deux coûts ; « AN enemy » (sbire légal) ; label `attack` ; deck vide : coût impayable.
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : coût 2, 2 dégâts, 2 cartes défaussées.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 3 cas rouges (cout + 2 dégâts, sbire cible, inclinée = pas de 2e usage) ; verts assumés : deck vide, absente en alter-ego.
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (l'inclinaison borne l'usage).
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), tracebacks : 0, lecture du journal : la carte est jouée et activée (lignes « s’active », coûts de compteurs relevés).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « les améliorations ELEMENT utilisées sont dessinées inclinées » (attachées à l'identité, `tv014` : Venus redressée).

Carte terminée : OUI

### tv010 : * Cosmic Requiem

- [x] Étape 2 : carte(s) de référence : `br009` (`DiscardDeckUntil(card_type=Event)` + `AddToHand`), `tr013` (coût compteurs).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « until you discard AN EVENT » (un allié ne s'arrête pas), deux coûts, aucun événement : deck remélangé, rien en main.
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : coût 2, 2 compteurs.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 3 cas rouges (trouvé en main ; allié traversé ; aucun événement) ; vert assumé : un seul compteur.
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (l'inclinaison borne l'usage).
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), tracebacks : 0, lecture du journal : la carte est jouée et activée (lignes « s’active », coûts de compteurs relevés).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « les améliorations ELEMENT utilisées sont dessinées inclinées » (attachées à l'identité, `tv014` : Venus redressée).

Carte terminée : OUI

### tv011 : * Dragon Scale

- [x] Étape 2 : carte(s) de référence : `tr001a` (ressource à coût de compteur), `ab007`/`ma005` (`CanGenerateResources`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « Resource: » SANS Hero (aussi en Bonnie) ; « generate a [WILD] » = `Resources("G")` ; `conditions=[a_un_compteur]` obligatoire (défaut trouvé : sans elle la ressource est offerte sans compteur et la carte est annulée).
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : coût 2, 1 compteur.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 2 cas rouges (paie Brain Burn en forme héros ; paie First Aid en forme Bonnie) ; vert assumé : sans compteur, la carte reste en main.
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (l'inclinaison borne l'usage).
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), tracebacks : 0, lecture du journal : la carte est jouée et activée (lignes « s’active », coûts de compteurs relevés).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « les améliorations ELEMENT utilisées sont dessinées inclinées » (attachées à l'identité, `tv014` : Venus redressée).

Carte terminée : OUI

### tv012 : * Dream Weaver

- [x] Étape 2 : carte(s) de référence : `tv010` (même montage), `br009`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « an ALLY OR UPGRADE » (événement traversé, allié ou amélioration arrête), deux coûts.
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : coût 2, 2 compteurs.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 2 cas rouges (allié en main ; amélioration, événement traversé) ; vert assumé : un seul compteur.
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (l'inclinaison borne l'usage).
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), tracebacks : 0, lecture du journal : la carte est jouée et activée (lignes « s’active », coûts de compteurs relevés).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « les améliorations ELEMENT utilisées sont dessinées inclinées » (attachées à l'identité, `tv014` : Venus redressée).

Carte terminée : OUI

### tv013 : * Reanimator Engine

- [x] Étape 2 : carte(s) de référence : `tl002` (cible en défausse), `Faces.ShuffleAllTo`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « UP TO 2 » (`range=(0, 2)`), « shuffle them into your deck », deux coûts.
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : coût 2, 2 compteurs, 2 cartes.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 2 cas rouges (2 cartes ; 1 seule) ; vert assumé : un seul compteur.
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (l'inclinaison borne l'usage).
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), tracebacks : 0, lecture du journal : la carte est jouée et activée (lignes « s’active », coûts de compteurs relevés).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « les améliorations ELEMENT utilisées sont dessinées inclinées » (attachées à l'identité, `tv014` : Venus redressée).

Carte terminée : OUI

### tv014 : * Turtle Shell

- [x] Étape 2 : carte(s) de référence : `td011` (`Faces.ReadyAll([heros])`), `tv009` (coût `DiscardDeckTopCards`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « ready VENUS » = le héros ; deux coûts ; deck vide : coût impayable.
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : coût 2, 2 cartes défaussées.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 1 cas rouge nominal (Venus inclinée redressée, deck 3 -> 1) ; vert assumé : deck vide refusée (voir la remarque : un seul cas nominal).
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (l'inclinaison borne l'usage).
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), tracebacks : 0, lecture du journal : la carte est jouée et activée (lignes « s’active », coûts de compteurs relevés).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « les améliorations ELEMENT utilisées sont dessinées inclinées » (attachées à l'identité, `tv014` : Venus redressée).

Carte terminée : OUI

### tv015 : Faulty Creation (obligation)

- [x] Étape 2 : carte(s) de référence : `01165` Eviction Notice (`WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm`), `tm013` (`PlayerActionToRemoveThisFromGame`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « You MAY flip » (facultatif, option Cancel), « Exhaust BONNIE -> » (Alter-Ego Action, un seul coût), « remove FROM THE GAME », icône Hazard imprimée (Q2).
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : Boost 2 (deux icônes rouges), Hazard 1, GiveTo Bonnie.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 2 cas rouges sur 7 (flip accepté ; Action retire l'obligation) ; verts assumés : refus, déjà en alter-ego, Action absente en forme héros, Hazard et Boost (natifs `desc`).
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), grep tracebacks : 0, lecture du journal : la carte est jouée / résolue dans les journaux (lignes « s’active » relevées).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « Faulty Creation : l'obligation est dessinée, Bonnie en civil ; une fois retirée plus dessinée ».

Carte terminée : OUI

### tv016 : Jasper Barlow's Lab (complot annexe)

- [x] Étape 2 : carte de référence : `16066` Blockade (`Hinder 2*`, aucun script), `14025` (Incite), `01107` (Hazard).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : Hinder `2*` = PAR JOUEUR, Incite 2 sur la PRINCIPALE, icône Hazard (découpe), menace de départ 0 ; aucun script (fiches `hinder.md`, `incite.md`, `hazard.md`).
      Résultat : OK.
- [x] Étape 6 : nombres : StartingThreat 0, Hinder 2*, Incite 2, Boost 2, Hazard 1.
      Résultat : OK.
- [x] Étape 7 : cas : `Hinder 2[par joueur] (menace 2) et Incite 2 (principale 3 -> 5)` ; `à DEUX joueurs, Hinder = 4` ; `Boost 2 : 4 dégâts`. AUCUN module : verts sans module par construction (base `desc`, assumé).
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 24 parties, tracebacks : 0, lecture du journal : le complot est révélé (24 lignes d'activité).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « la manigance annexe porte 2 jetons de menace ».

Carte terminée : OUI

### tv017 : * Jasper Barlow

- [x] Étape 2 : carte(s) de référence : `tl015` Karai (`WhenThisRevealed` + boost « deal this card to the first player »), `tr017` (`message.GetToPlayer()`), `19001a` (`GiveStatus`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « each minion engaged WITH YOU » (pas l'autre joueur ; Jasper lui-même est engagé à la révélation), Tough, boost étoile seul (0 icône), `desc.Nemesis = Venus`.
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : PV 2, MNG 2, ATQ 0.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 3 cas rouges sur 4 (Tough sur Hydra et sur lui-même ; autre joueur épargné ; boost donné face cachée, 2 dégâts) ; vert assumé : valeurs `desc`.
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), grep tracebacks : 0, lecture du journal : la carte est jouée / résolue dans les journaux (lignes « s’active » relevées).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « Tenace sur les sbires engagés » et « boost : carte distribuée dos seul ». Rouge en cassant `dealt_encounter_cards` (C).

Carte terminée : OUI

### tv018 : * Groundchuck-Dirtbag

- [x] Étape 2 : carte(s) de référence : `01101` Hydra Mercenary (Guard), `01076` Luke Cage (Toughness), `tl015` (boost).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : Guard et Toughness lus par le moteur (fiches `guard.md`, `toughness.md`), boost étoile seul, pas de `(nemesis minion)` imprimé donc pas de `desc.Nemesis`.
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : PV 4, MNG 1, ATQ 3, Guard 1, Toughness 1.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 1 cas rouge (boost donné face cachée) ; vert assumé : valeurs, Guard et Toughness natifs (`IsGuard`, `IsToughness`, Tough à l'entrée).
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), grep tracebacks : 0, lecture du journal : vue en jeu dans les journaux du lot de 16 parties « prudent » : mélangée au deck rencontre et retournée comme carte de boost de Klaw (journaux lus ; non vue dans les 8 premières parties).
      Résultat : OK.
- [x] Étape 8 bis : OUI par le boost : cas plateau « carte distribuée dos seul » (rouge avec (C)).

Carte terminée : OUI

### tv019 : Salvaged Scales

- [x] Étape 2 : carte(s) de référence : `50134`/`ho015` (`PlaceThreatOnSchemes("MainScheme", ...)`), `tv017` (sbires engagés avec le joueur de la révélation).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « 2 threat on the MAIN scheme », « If Jasper Barlow IS IN PLAY » (présence, nom sans l'étoile), « the villain AND each minion engaged WITH YOU ».
      Résultat : OK.
- [x] Étape 6 : nombres texte ↔ code : Boost 2, 2 menaces ; x2.
      Résultat : OK.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : 3 cas rouges sur 4 (sans Jasper : menace seule ; avec Jasper : Tough sur vilain, Hydra et Jasper ; Jasper mais sbire d'un autre joueur) ; vert assumé : Boost 2 (natif).
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 24 parties, témoin raphael (8), grep tracebacks : 0, lecture du journal : vue en jeu dans les journaux « prudent » (révélée plusieurs fois, 2 menaces posées sur la principale, aucun Tough car Jasper absent : conforme au texte).
      Résultat : OK.
- [x] Étape 8 bis : OUI. Cas plateau « Tenace sur le vilain et sur chaque sbire engagé ».

Carte terminée : OUI

