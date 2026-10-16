# Donatello (td) : gabarits PROCESSUS-CARTE, 16/10/2026

Preuves communes à toutes les cartes :
- Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_donatello.py` (101 cas, tous verts :
  `tools/test_capacites.py .game-src <port> rapport "[donatello]"`).
- Substitution : `tools/substituer_pack.py .game-src <port> td` puis `td016` / `td017` (rejoués
  après ajout des cas essaim). Chaque module remplacé par un stub tombe au rouge sur au moins un cas
  sujet ; les cas qui restent verts sans module sont des TEMOINS D'ABSENCE (« sans X, rien ne se
  passe »), des mesures de données natives (`desc` : Restricted, Toughness, Quickstrike, icônes) ou
  des cas portés par une autre carte dont le nom cite l'id.
  Bilan rouges/cas : td001a 2/3, td001b 4/6, td002 2/8, td003 2/3, td004 2/3, td005 4/5, td006 4/5,
  td008 4/5, td009 4/6, td010 4/6, td011 1/4, td012 6/12, td013 7/9, td014 3/6, td015 4/8,
  td016 7/10, td017 3/4.
- Autoplay : `tools/autoplay.py .game-src --deck donatello --vilains rhino --parties 8` : 8 parties,
  0 traceback (grep NameError|AttributeError|TypeError|KeyError|AssertionError|Traceback = 0 sur les
  8 logs) ; témoin `spider_man` : 8 parties, 0 traceback. Les deux à 0 % de victoire : le deck
  Donatello n'a PAS de moitié d'aspect (consigne du 06/09/2026), taux non comparable. Metalhead,
  la Carapace et td016 sont apparus dans les journaux de Donatello. Lecture ligne à ligne : journaux
  survolés, pas lus en entier.
- `verifier_tous_les_decks` pour le deck `donatello` : OK (« identite td001b, main 6, deck 9 »), PAS
  la passe des 107 decks.
- Scans relus un à un le 16/10/2026 (texte, nombres, icônes de ressource). Icônes de ressource
  VÉRIFIÉES PAR DÉCOUPE contre des cartes officielles (coin inférieur gauche de 01004 mental, 01006
  énergie, 01003 physique, 01011 wild) : td002/td005/td009/td011 énergie (Y), td003/td004/td006
  mental (B), td008/td010/td012 physique (R), td007 mental + wild (BG) : tout conforme à `desc.RES`.
- Étape 8 bis (plateau, ce que la carte DESSINE) : `ui-app/src/board/tmnt-donatello-plateau.test.ts`
  (28 cas verts). Preuve de sensibilité (16/10/2026) : `zones.ts` `sousArbre` ramené à un seul étage
  (`...[]`) et `card-model.ts` `compteursAffiches` sans `push` => 11 cas ROUGES (carte glissée sous la
  Carapace absente/non cliquable, compteurs swarm absents), lignes restaurées (`git checkout`), cas
  reverts verts. Le cliquable (jouer/dépenser/défausser la carte glissée) est vérifié par
  `useInteraction`. Ce que le test NE prouve PAS : un rendu pixel à l'écran (jamais regardé en vrai).
Questions « une icône / un mot » : aucune ouverte (décisions de `decisions-phase-b.md` appliquées).

### td001a : * Donatello (face héros)
- [x] Étape 2 : réf. `wd056b` (coût BB), `03001a` (Action d'identité + limite), `mf011` (pioche).
- [x] Étape 5 : mots-pièges : « Action » nu, « spend [mental][mental] » = coût `BB`, « limit once per round ». OK.
- [x] Étape 6 : PV 11, ATQ 1, CTR 2, DEF 2, main 5 = scan = `cards.json`.
- [x] Étape 7 : cas « depense BB : pioche 2 », rouge sans module ; « le cout BB est obligatoire » (témoin vert).
- [x] Étape 7 bis : limite OUI. Témoin `td001a Kashikoi — TEMOIN D'EPUISEMENT` : 2e activation refusée, main = 4 (5 si inerte). Rouge sans module.
- [x] Étape 8 : voir communs. [x] Étape 8 bis : NON (pioche seulement).
Carte terminée : OUI.

### td001b : * Donnie (face alter ego)
- [x] Étape 2 : réf. `vp001b` (recherche deck + défausse), `face_on_event.py` `PutIntoPlay(exhaust=True)`, `CostFunc.Discard`.
- [x] Étape 5 : « Bo OR Shell » = UNE seule carte (cas deck : td012 reste dans le deck), « exhausted », « (Shuffle) », coût devant la flèche.
- [x] Étape 6 : PV 11, REC 3, main 6.
- [x] Étape 7 : 5 cas (td011, td012, défausse, aucune cible, témoin main vide), rouge sans module sur les 4 positifs.
- [x] Étape 7 bis : limite NON.
- [x] Étape 8 : voir communs.
- [x] Étape 8 bis : OUI (l'amélioration arrive attachée et inclinée) ; `tmnt-donatello-plateau.test.ts` « td001b Donnie », rouge sans correctif (mutation `sousArbre`).
Carte terminée : OUI.

### td002 : * Metalhead
- [x] Étape 2 : réf. `dd003` Doombot (Interrupt + `PlayCardsLikeInTurn`), `td012`.
- [x] Étape 5 : « from your hand OR Donatello's Shell » PROUVÉ des deux côtés ; « When DONATELLO defends » = forme héros (témoin alter ego) ; unique (témoin copie en jeu : CORRECTION moteur de carte, ajout `FieldHasNotThisUniqueType`) ; « without paying his resource cost » (Energy reste en main).
- [x] Étape 6 : coût 2, PV 1, ATQ 2*, CTR 2* (une étoile = 1 dégât consécutif, mesuré), Toughness.
- [x] Étape 7 : cas main + cas Carapace, rouges sans module ; ATQ/CTR consécutifs mesurés (verts sans module : valeurs natives).
- [x] Étape 7 bis : NON. [x] Étape 8 : voir communs. [x] Étape 8 bis : NON.
Carte terminée : OUI.

### td003 : Bō Tobu (macron, un seul card_id)
- [x] Étape 2 : réf. `si012`, `br004`. [x] Étape 5 : « would take damage FROM AN ATTACK » (témoin dégâts directs), « prevent 3 OF THAT damage » (attaque de 2), « a scheme ». 
- [x] Étape 6 : coût 1, RES B. [x] Étape 7 : attaque de 4 (1 dégât, menace 5 -> 2), attaque de 2, témoin ; rouge sans module.
- [x] Étape 7 bis : NON. [x] Étape 8 : voir communs. [x] Étape 8 bis : NON.
Carte terminée : OUI.

### td004 : Chūdan-Ura-Uke
- [x] Étape 2 : réf. `br004`. [x] Étape 5 : « 3 damage to the attacking enemy » (ah016 survit à 3, Shocker tombe), « from an attack » (témoin). Cas « attaquant mort entre temps » NON montable : le moteur annule déjà les dégâts d'une source hors jeu avant l'interruption.
- [x] Étape 6 : coût 1, RES B. [x] Étape 7 : 2 cas + témoin, rouge sans module. [x] 7 bis NON. [x] Étape 8 communs. [x] 8 bis NON.
Carte terminée : OUI.

### td005 : Improvised Tactics
- [x] Étape 2 : réf. `55023` (choose two), coût `Exhaust` TECH. [x] Étape 5 : « choose two, jamais la même » (témoin Piocher x1), « Stun OR confuse » (2 branches), coût devant la flèche (sans TECH : injouable).
- [x] Étape 6 : coût 2, RES Y. [x] Étape 7 : 4 cas, rouges sans module.
- [ ] Option « Cloak two friendly characters » : travail de l'AUTRE agent (carte d'état Cloaked), ligne et branche non touchées ici, ses cas sont les siens (non relus ici) ; aucun de mes cas ne la choisit.
Étape 8 bis : la carte Cloaked est dessinée sur l'identité et sur un allié (`tmnt-donatello-plateau.test.ts`), mais la branche moteur reste à l'autre agent.
La branche Cloak est prouvee par `tools/cas/cloaked_cartes.py` (cas « td005 Improvised Tactics : deux amis Cloaked », 17/17 le 16/10/2026, rouge avec l'ancien td005).
Carte terminée : OUI (hors partie réelle).

### td006 : Singularity
- [x] Étape 2 : réf. `16036`, `04009`, `bw024`. [x] Étape 5 : « play only if you control » (injouable sans Gantelet), « 10 damage », overkill / piercing / ranged chacun MUTÉ séparément (flag à False -> cas rouge : overkill, piercing, ranged).
- [x] Étape 6 : coût 4, RES B. [x] Étape 7 : 5 cas, rouges sans module. [x] 7 bis NON. [x] Étape 8 communs. [x] 8 bis NON.
Carte terminée : OUI.

### td007 : Inspired Brilliance
- Aucun texte, aucun script. [x] Étape 6 : RES BG = scan (découpe). [x] Étape 7 : 3 cas (paie un coût de 2 seule, ne paie pas un coût de 4, icônes B+G lues). Pas de module donc pas de substitution (rien à retirer).
- [x] Étape 8 : voir communs (dans le deck de départ). [x] 8 bis NON.
Carte terminée : OUI (carte de données pure).

### td008 : * Donnie's Lab
- [x] Étape 2 : réf. `01034`, `22034`. [x] Étape 5 : ANDROID, ITEM OU TECH (3 cas, un par trait), « in your discard pile », témoin Energy jamais ramenée, « Alter-Ego Action » (témoin forme héros).
- [x] Étape 6 : coût 1, RES R. [x] Étape 7 : rouges sans module. [x] 7 bis NON. [x] Étape 8 communs. [x] 8 bis NON (carte en main).
Carte terminée : OUI.

### td009 : * Anti-Gravity Gauntlet
- [x] Étape 2 : réf. `ho006`, `ho011`. [x] Étape 5 : « Donatello gets +1 ATK » (face héros), « ATTACK event » (témoin non-ATTACK), « +3 de CET événement » (attaque de base suivante sans bonus), coût exhaust ET défausse (main vide : pas de +3).
- [x] Étape 6 : coût 2, RES Y, +1, +3. [x] Étape 7 : 6 cas, rouges sans module sur +1 ATQ et +3. [x] 7 bis NON. [x] Étape 8 communs. [x] 8 bis NON.
Carte terminée : OUI.

### td010 : * Truevision Goggles
- [x] Étape 2 : réf. `tg009`. [x] Étape 5 : « basic thwart » (témoins attaque de base et contre d'événement), « +1 THW for that thwart », « You MAY discard a status card » (option Cancel offerte, statut reste), UNE carte à la fois, +1 offert sans ennemi à statut.
- [x] Étape 6 : coût 1, RES R. [x] Étape 7 : rouges sans module. [x] 7 bis NON. [x] Étape 8 communs. [x] 8 bis NON.
Carte terminée : OUI.

### td011 : * Donatello's Bō
- [x] Étape 2 : réf. `ho011`, `03009`. [x] Étape 5 : « ready Donatello », « Restricted » (3 cartes restreintes : une défaussée ; donnée native `desc`, vert sans module), Hero Action (témoin alter ego).
- [x] Étape 6 : coût 2, RES Y, Restricted 1. [x] Étape 7 : l'action rouge sans module. [x] 7 bis NON. [x] Étape 8 communs. [x] 8 bis NON.
Carte terminée : OUI.

### td012 : * Donatello's Shell
- [x] Étape 2 : réf. `60030`, `dd008`, Echo `60037a`. [x] Étape 5 : « play, spend, OR discard » EN ENTIER (décision 15/10, fidélité 100 %) : jouer, dépenser, défausser chacun prouvé ; « Max 1 » (témoin d'épuisement : Carapace redressée entre deux actions) ; Hero Action (témoin alter ego).
- [x] Étape 6 : coût 2, RES R. [x] Étape 7 : 12 cas (tuck, plafond, alter ego, dépenser + témoin, jouer, défausser td001b + témoin, défausser td009 +3 + témoin), 6 rouges sans module.
- [x] Étape 7 bis : plafond « Max 1 » : cas `TEMOIN « Max 1 tucked card »`, 2e carte non glissée, Carapace prête, 1 carte dessous.
- [x] Étape 8 : voir communs. [x] Étape 8 bis : OUI (carte glissée) ; 13 cas `td012` (dessinée, rang juste derrière la Carapace, `peeking`, dos pour un autre siège, jouer/dépenser/défausser cliquables), 8 rouges sous mutation `sousArbre`.
MOTEUR PARTAGÉ MODIFIÉ (voir rapport) ; regressions relancées : Echo, Brawn, ho009, sf010, wd0, sf0.
Carte terminée : OUI.

### td013 : Broken Shell (obligation)
- [x] Étape 2 : réf. `ho013`, `sf010`, `sf015`. [x] Étape 5 : bascule ET -5 PV (11 -> 6), plancher 1 (4 PV -> 1), déjà alter ego, « cannot change to hero form » (témoin), deux Actions (BB / défausser la Carapace EN JEU), « remove from the game » (zone retirée, ni défaussée), repassage en héros après retrait.
- [x] Étape 6 : Boost 2. [x] Étape 7 : 9 cas, 7 rouges sans module. [x] 7 bis NON. [x] Étape 8 : deck de départ monté (`verifier_tous_les_decks`). [x] 8 bis : OUI (changement de forme) ; `tmnt-donatello-plateau.test.ts` « td013 » : forme d'identité, obligation dessinée, Carapace défaussée, retrait du jeu en zone `annexes` (témoins d'état, pas de rouge dédié : le changement de face n'a pas de code de rendu propre).
Carte terminée : OUI.

### td014 : Extermination!
- [x] Étape 2 : réf. `27068`, `01128`, `01109`. [x] Étape 5 : « deck AND discard pile » (3 cas : deck, FLYBORGS, défausse), UN seul sbire, « engaged with the FIRST player » (vérifié sur le premier joueur ; le cas « vaincue par le 2e joueur » n'est pas montable avec le harnais), traits pluriels (décision), rien si aucun sbire.
- [x] Étape 6 : menace 2 par joueur (2 puis 4), Acceleration 1, Boost 2. [x] Étape 7 : rouges sans module sur les 3 recherches. [x] 7 bis NON. [x] Étape 8 communs. [x] 8 bis NON.
Carte terminée : OUI (réserve : « premier joueur » vs « joueur qui déjoue » non distingués en jeu).

### td015 : * Baxter Stockman
- [x] Étape 2 : réf. `04117`, `jj019`, `01167`. [x] Étape 5 : « any MOUSERS OR FLYBORGS in play » (deux cas + témoin + dynamique), Quickstrike (natif : n'agit qu'en forme héros, mesuré), « schemes instead ».
- [x] Étape 6 : PV 3, SCH 2, ATQ 0, Boost 2. [x] Étape 7 : 8 cas, 4 rouges sans module. [x] 7 bis NON. [x] Étape 8 communs. [x] 8 bis NON.
Carte terminée : OUI.

### td016 : Plague of M.O.U.S.E.R.s
- [x] Étape 2 : réf. `16036`, `27067`, `gorr/gb009`, `sk178`. [x] Étape 5 : SCH, ATQ ET PV = compteurs, DYNAMIQUES (`desc.HP = 0`, `ThisGainKeyword(health=1)`), aucune défaite écrite dans le module, « that many instead » (3 dégâts sur 2 compteurs, 1 puis 1), vaincu par `LimitHealth`, défausse de rencontre.
- [x] Étape 6 : boost 1, 2 compteurs. [x] Étape 7 : 10 cas, 7 rouges sans module (les 3 verts : mort identique avec PV 0 sans module).
- [x] Étape 8 : voir communs. [x] 8 bis : OUI (compteurs) ; `tmnt-donatello-plateau.test.ts` « td016 / td017 essaims » : `compteurs.swarm` dessiné (2, 4, 1), rouge sans `push` de `compteursAffiches`.
Limites mesurées : dégâts remplacés -> aucun excédent Overkill ; mort sans tueur (pas de « after you defeat »).
Limite 8 bis : la valeur ATQ/PV/SCH dynamique affichée sur la carte n'est pas affirmée (seul le compteur l'est).
Carte terminée : OUI.

### td017 : Flight of Flyborgs
- Jumeau de td016 (4 compteurs, boost 3) : 4 cas, 3 rouges sans module. Mêmes limites, même 8 bis (compteur à 4 dessiné).
Carte terminée : OUI.
