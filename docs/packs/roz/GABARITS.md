# Roz (jakxin) : gabarits PROCESSUS-CARTE, 21 card_id

Pack `roz`, préfixe `rz`, set 220 (« 220. Custom (Roz) »). Source : zip « Roz Solomon » déposé le 25/10/2026 (31 PNG, auteur
jakxin). Héros neuf : Rosalind « Roz » Solomon, agent du S.H.I.E.L.D. au service du Wakanda ; ennemi juré Dario Agger (Roxxon).
Deck de départ `deck/starter/roz.json` : 15 cartes de héros + obligation + némésis ; **l'auteur fournit sa decklist imprimée**
(`Roz Decklist.png`), `player_deck` la recopie (25 cartes : aspect Leadership + Basic, noms résolus en `card_id` officiels, voir
`metadata.note`). Une `Roz Solomon` existe déjà (`ra003`, allié du pack rainy) : jamais touchée, jamais cherchée par nom.

Cas : `Fusion/marvel-lcg-src/tools/cas/roz.py` (filtre `[rz]`, **69 cas verts sur 69**). Plateau : `ui-app/src/board/roz-plateau.test.ts`
(5 cas). Preuve par substitution : `tools/substituer_pack.py .game-src-rz2 32000 rz0` = **18/18 modules avec au moins un cas rouge sans leur module** (les cas qui restent verts sont, carte par carte, des valeurs imprimées, des contre-cas d'absence et des témoins : assumés) ; empreinte du dossier du pack identique avant/après (aucun stub resté).

## Décision de méthode (consigne utilisateur du 25/10/2026)

Pas de question carte par carte pendant la construction : chaque doute a reçu l'option RECOMMANDÉE, codée, et la carte est marquée
**« Carte terminée : NON (provisoire) »** avec la question précise. Toutes les questions en attente sont regroupées en fin de
document (§ « Questions en attente »).

## Ce que ce pack a dû ajouter au moteur (CORRECTIFs commentés)

- `CardFace.TRAITS` : `"ROXXON"` (Dario Agger). `CardFace.COUNTER` : `'agent'` (+ libellé `compteurs-fr.ts`).
- `PlayerStat.this_turn_resolved_specials` + `EffectInvoker._ResolveSelfInternal` (`effect_invoke.py`) : décompte des capacités
  « Special » réellement résolues ce tour (`rz002`, `rz003`).
- `Puzzle.ResolveSpecial` (`puzzle.py`, `puzzle_.py`) : commande de banc de test.
- **26/10/2026** : `WorldStat.turn_serial` (`world_stat.py`, un numéro qui change à chaque début ET fin de tour de joueur) pour « limit once per TURN » (rz003) ;
  `Puzzle.NewPlayerTurn` (`puzzle.py`, `puzzle_.py`) : clôt le tour courant et en ouvre un autre (banc de test). Additifs.
- Aucun autre fichier du moteur touché. Fichiers partagés de données : `cards.json`, `sets_info.json`, `prefixes_fanmade.json`
  (`rz`), `textes-fr-fanmade.ts` (21 textes), `heros-info.js` (`rz001a`), `RECETTES-MOTEUR.md` §27, `mots-cles/special.md`.

## Gates du héros

- [x] Étapes 1 à 8 de PROCESSUS-HEROS : cartes (`cards.json`, pack `roz`), scripts (`src/cards/pack/roz/`), deck de départ,
      `sets_info.json`, préfixe, images (`assets/pics/rz*.jpg`, 615×882, la manigance annexe `rz018` en paysage 882×615, non
      versionnées), biographie (`heros-info.js`, `rz001a`), textes FR (gates `textes-fr-fanmade.test.ts`, `vocabulaire-statuts.test.ts`,
      `compteurs-fr.test.ts` vertes).
- [x] Légalité des decks (PROCESSUS-HEROS §10) : 0 signature étrangère dans le `player_deck`.
- [x] `verifier_tous_les_decks` : `roz` « identité rz001a, main 7, deck 33 » (main 7 = le Setup d'`rz001b` a ajouté une amélioration) ;
      passe complète du 25/10/2026 : **162/163**, le seul échec est `wasp_hank_pym` (pack d'un autre agent en cours, `hp003`,
      untracked), sans lien avec ce pack.
- [x] `tools/test_cards.py` : **7539 modules OK, 0 erreur** (874 sans `GetAbilities`). `verifier_prefixes.py` OK.
      `verifier_traductions_fr.py` OK. `verifier_appels_modules.py roz` OK, **calibré** (§9) : un appel inventé (`this.DealDamageInexistant`, module temporaire `rz999`, supprimé) a bien été refusé.
- [x] Autoplay : 8 parties de Roz (rhino/klaw × équilibré/agressif × 2), témoin She-Hulk officielle sur les mêmes 8 graines.
      0 exception sur les 16 journaux ; 0 victoire des deux côtés (le pilote, pas les cartes) ; Roz 3,5 à 7,5 rounds, She-Hulk 4 à 4,5.
      Journaux lus : les Specials de Stealth Tech, Agent of Wakanda, Ayo et Aneka (via Dora Milaje) se résolvent ; Weighed Down
      inflige 1 dégât par Special puis 5 en alter ego ; Legal Council s'active et annule un Special.
- [ ] **Une partie complète jouée par un humain avec Roz : NON FAITE.** Aucun outil ne la remplace.


**26/10/2026, après les correctifs d'arbitrage** (rz002, rz003, rz006) : autoplay relancé, 8 parties Roz contre Rhino (0 victoire, 8 défaites, 6,2 rounds), 0 exception (grep sur les 8 journaux : 0), 0 blocage ;
témoin `she_hulk` 8 parties (0 victoire, 1 partie bloquée par le pilote, 0 exception). Deck `roz` : OK. Substitution (rz002 6/8, rz003 4/6, rz006 4/6) : pack identique avant/après (md5 `55e8c000…`).

## Gabarits carte par carte

### rz001a : * Roz (face HÉROS) — S.H.I.E.L.D. SPY WAKANDA. PV 9, THW 2, ATK 1, DEF 1, main 5

> <i>Driven</i> — Response : After you use a basic power, resolve the "Special" ability on another WAKANDA card you control.
> Special : Ready another friendly character (limit once per round).

- [x] Étape 2 : cartes de référence : Driven : `51001a` Black Panther (`AfterUnitUseBasicPower` + `ResolveSpecialAbility`) ; Special : `51010` (`WhenResolveSpecialAbility`), `01024` (`Faces.ReadyAll` + `canbe_ready`).
- [x] Étape 5 : mots-pièges vérifiés : « ANOTHER WAKANDA card » (`exclude="This"`, seules les cartes à Special) ; « After you use a BASIC power » ; « ANOTHER friendly character » (héros ou allié, jamais Roz) ; « once per ROUND ». Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : PV 9, THW 2, ATK 1, DEF 1, main 5 (`desc` + cas « valeurs imprimées »). Résultat : conforme.
- [x] Étape 7 : 6 cas : rz001a Roz : valeurs imprimees PV 9, ATK 1, THW 2, DEF 1, main 5, S.H.I.E.L.D. SPY WAKANDA | rz001a Driven : apres un contre de base, le Special d'une AUTRE carte WAKANDA (Wakandan Jumpsuit) re | rz001a Driven : CONTRE-CAS aucune autre carte WAKANDA a Special en jeu -> seul le contre de base ret | rz001a Special : redresse un AUTRE personnage ami (Mockingbird epuisee) | rz001a Special : CONTRE-CAS Roz epuisee, aucun autre personnage -> elle ne se redresse pas elle-meme | rz001a Special : TEMOIN D'EPUISEMENT, deux resolutions dans le meme round -> un seul allie redresse. Substitution : **rouges 3/6** (restent verts sans le module : rz001a Roz : valeurs imprimees PV 9, ATK 1, THW 2, DEF 1, main 5, S.H.I.E.L.D. SPY WAKANDA ; rz001a Driven : CONTRE-CAS aucune autre carte WAKANDA a Special en jeu -> seul le contre d ; rz001a Special : CONTRE-CAS Roz epuisee, aucun autre personnage -> elle ne se redresse pas)
- [x] Étape 7 bis : limite imprimée ? OUI (« limit once per round » du Special) : cas « TÉMOIN d'épuisement » : 2 résolutions, 1 seul allié redressé.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Driven vu en autoplay (journal) : Roz résout Stealth Tech, Agent of Wakanda, Ayo (via Dora Milaje).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON (rien de nouveau à dessiner).

Carte terminée : **NON (provisoire)** : seule manque la partie réelle jouée par un humain (gate du héros).

### rz001b : * Rosalind Solomon (face ALTER EGO) — S.H.I.E.L.D. SPY WAKANDA. PV 9, REC 3★, main 6

> Setup : Find a WAKANDA upgrade and add it to your hand.
> ★ <i>Agent E-23</i> — Response : After you make a basic recovery, search your deck for a S.H.I.E.L.D. or WAKANDA card and add it to your hand.

- [x] Étape 2 : cartes de référence : Setup : `01040b` T'Challa (`WhenCardSetup` + `Search.PlayerCard` + `GainCard`) ; Response : `45015` Sidekick (`AfterUnitMakeRecovery(is_basic_recovery=True)`), `bl002` (`finder=CardFinder(traits=[...])` = OU).
- [x] Étape 5 : mots-pièges vérifiés : « FIND » = deck ET défausse (convention du projet, `br009`/`Worthy`), « search your DECK » = deck seul ; « BASIC recovery » ; « S.H.I.E.L.D. OR WAKANDA » (OU). Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : PV 9, REC 3, main 6 ; la main de départ passe à 7 (6 + 1 amélioration trouvée). Résultat : conforme.
- [x] Étape 7 : 5 cas : rz001b Rosalind Solomon : valeurs imprimees PV 9, REC 3, main 6, S.H.I.E.L.D. SPY WAKANDA | rz001b Setup : une amelioration WAKANDA du deck est ajoutee a la main de depart (6 + 1 = 7 cartes) | rz001b Agent E-23 : apres une recuperation de base, une carte S.H.I.E.L.D. du deck (Mockingbird) pas | rz001b Agent E-23 : une carte WAKANDA (Okoye) convient aussi | rz001b Agent E-23 : CONTRE-CAS une guerison par une carte (pas une recuperation DE BASE) ne cherche . Substitution : **rouges 3/5** (restent verts sans le module : rz001b Rosalind Solomon : valeurs imprimees PV 9, REC 3, main 6, S.H.I.E.L.D. SPY WAKANDA ; rz001b Agent E-23 : CONTRE-CAS une guerison par une carte (pas une recuperation DE BASE) n)
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Setup vu en autoplay : « Roz gagne Wakandan Jumpsuit » au Setup.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminée : **NON (provisoire)** : partie réelle jouée par un humain manquante ; arbitrage en attente : Q1 : « Find » = deck + défausse (recommandé) ou deck seul ?

### rz002 : * Thor (Jane Foster) — ALLIÉ, coût 3, [wild], 3 PV, THW 2★, ATK 2★. ASGARD

> Reduce the cost of this card by 1 for each "Special" ability resolved this turn.
> Each Thor ally gains "Response: After this card uses a basic power, resolve the "Special" on a WAKANDA card you control."

- [x] Étape 2 : cartes de référence : coût : `wd157` (`ReduceCostToPlayThis(fn)`) ; octroi : `alopex/ta009`, `leonardo/tl011` (`GiveKeywordToInPlayWhenApplyThis(..., given_abilities=[...])`) ; Response : `51001a`.
- [x] Étape 5 : mots-pièges vérifiés : « EACH Thor ally gains » (y compris cette carte et Odinson) ; « each Special ABILITY resolved THIS TURN » (capacités RÉSOLUES, cout payé) ; « After THIS CARD uses a basic power ». Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : coût 3, 3 PV, THW 2, ATK 2 ; réduction : -1 par Special. Résultat : conforme.
- [x] Étape 7 : 5 cas : rz002 Thor (Jane Foster) : valeurs imprimees cout 3, 3 PV, ATK 2, THW 2, ASGARD | rz002 Thor (Jane Foster) : un Special resolu ce tour -> cout 3 - 1 = 2, payee avec Strength (RR) | rz002 Thor (Jane Foster) : TEMOIN aucun Special ce tour -> cout 3, injouable avec 2 ressources | rz002 Thor (Jane Foster) : DEUX Specials ce tour -> cout 3 - 2 = 1, payee avec UNE ressource (Emerge | rz002 Reponse donnee : apres que Thor (Jane Foster) utilise un pouvoir de base, le Special d'une car. Substitution : **rouges 3/5** (restent verts sans le module : rz002 Thor (Jane Foster) : valeurs imprimees cout 3, 3 PV, ATK 2, THW 2, ASGARD ; rz002 Thor (Jane Foster) : TEMOIN aucun Special ce tour -> cout 3, injouable avec 2 ressou)
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Thor présent dans 114 lignes de journal d'autoplay (jouée, réduction de coût).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI (allié dessiné) : plateau vert d'emblée.

- [x] **26/10/2026, Q2 (RR : « Each Thor ally » ne dit pas « you control »)** : l'octroi vise tout allié nommé Thor EN JEU, de n'importe quel joueur (`control_by="You"` retiré).
      **DÉFAUT ANTÉRIEUR TROUVÉ EN CHEMIN, même en solo** : chaque Thor ne recevait que SA PROPRE Réponse, jamais celle de l'autre Thor. Deux causes, vues au journal
      (`try_apply` jamais appelé pour l'autre carte, puis `CheckWhichCard` faux) : (1) l'évènement de rafraîchissement par défaut (`EnterPlayWhen`, « when ») part AVANT
      que l'autre Thor soit en jeu : `change_on_event=OnEvent.EnterPlayAfter(...)` ; (2) un `CardFinder(name="Thor")` est une capacité RÉFÉRENTIELLE (`Referential.Check`,
      `v16_referential_ability`) : un nom cité par une carte ne désigne pas une AUTRE carte du même nom : `FinderThor()` (helper du set, `check_face_fn` sur le nom) ne passe pas
      par ce contrôle. Cas `rz_nb_reponses` (nombre de Réponses enregistrées sur la carte) : 3 cas (autre joueur, même joueur, ordre inverse) VUS ROUGES (1 Réponse au lieu de 2)
      avant le correctif, verts après. Substitution relancée : **rouges 6/8** (verts : valeurs imprimées, témoin « aucun Special »).
Carte terminée : **NON (provisoire)** : partie réelle jouée par un humain manquante. (Q2 tranchée le 26/10/2026 : tout allié Thor, y compris les Thor officiels et ceux des autres joueurs.)

### rz003 : * Thor (Odinson) — ALLIÉ, coût 4, [wild], 4 PV, THW 1★, ATK 3★. ASGARD

> Reduce the cost to play this card by 2 if you resolved a "Special" ability this turn.
> Each Thor ally gains "Response: After you resolve a "Special" ability on a card you control, deal 1 damage to an enemy (limit once per turn)."

- [x] Étape 2 : cartes de référence : coût conditionnel : `bl002` ; octroi : `ta009`/`tl011` ; « After you resolve a Special » : `storm/36007` ; « once per turn » rendu « par round » (arbitrage `hc002`).
- [x] Étape 5 : mots-pièges vérifiés : « BY 2 IF you resolved a Special THIS turn » (2 d'un coup, pas par Special) ; « on a card YOU CONTROL » ; « deal 1 damage to AN enemy » ; « once per TURN » (rendu par round). Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : coût 4, 4 PV, THW 1, ATK 3 ; réduction 2. Résultat : conforme.
- [x] Étape 7 : 5 cas : rz003 Thor (Odinson) : valeurs imprimees cout 4, 4 PV, ATK 3, THW 1, ASGARD | rz003 Thor (Odinson) : un Special resolu ce tour -> cout 4 - 2 = 2, payee avec Strength (RR) | rz003 Thor (Odinson) : TEMOIN aucun Special ce tour -> cout 4, injouable avec 2 ressources | rz003 Reponse donnee : apres un Special resolu, 1 degat a un ennemi (Thor Odinson en jeu) | rz003 Reponse donnee : TEMOIN D'EPUISEMENT, deux Specials dans le meme round -> 1 seul degat (limite. Substitution : **rouges 3/5** (restent verts sans le module : rz003 Thor (Odinson) : valeurs imprimees cout 4, 4 PV, ATK 3, THW 1, ASGARD ; rz003 Thor (Odinson) : TEMOIN aucun Special ce tour -> cout 4, injouable avec 2 ressources)
- [x] Étape 7 bis : limite imprimée ? OUI (« limit once per turn ») : cas TÉMOIN d'épuisement : Stealth Tech résout 2 Specials, 1 seul dégât.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Thor : voir rz002.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI (allié dessiné) : plateau vert d'emblée.

- [x] **26/10/2026, Q2 (suite) (RR « Limit » : « limit once per turn » ≠ « per round »)** : la limite est par TOUR de joueur. `WorldStat.turn_serial` (change à chaque début ET fin de tour) est noté
      SUR l'allié Thor qui reçoit la Réponse (`rz003_tour`), au moment où elle se résout : chaque Thor a SA limite (avant, l'objet `Ability` partagé donnait UNE limite pour tous les Thor, par
      round). Même octroi à tout Thor que rz002 (voir ci-dessus). Cas : « un AUTRE tour du même round » (premier Special, `Puzzle.NewPlayerTurn`, second Special : 2 dégâts) VU ROUGE
      (« dégâts = 1, attendu 2 ») avant, vert après ; témoin d'épuisement « deux Specials dans le même TOUR -> 1 seul dégât » (rz006 en deux résolutions) vert avant et après (assumé : c'est le témoin
      de la limite). Substitution relancée : **rouges 4/6** (verts : valeurs imprimées, témoin « aucun Special »).
Carte terminée : **NON (provisoire)** : partie réelle jouée par un humain manquante. (Q2 (suite) tranchée le 26/10/2026 : une fois par TOUR.)

### rz004 : Vibranium Gun — AMÉLIORATION, coût 2, [mental], Restricted. TECH. WEAPON. WAKANDA

> Restricted.
> Roz's basic attacks gain ranged.
> Special (attack) : Deal 2 damage to an enemy. This attack gains piercing.

- [x] Étape 2 : cartes de référence : Special (attack) : `51011` Panther Claws (`AttackProperty(piercing=...)`) ; ranged sur attaques de base : `22004` (`UnitAttackGainKeyword(..., is_basic_attack=True)`) ; Restricted : `desc.Restricted`, base automatique.
- [x] Étape 5 : mots-pièges vérifiés : « BASIC attacks » (pas les attaques d'événement) ; « THIS attack gains piercing » (le Special seul) ; le Special est une ATTAQUE et n'est PAS ranged (la riposte s'applique). Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : coût 2 ; 2 dégâts du Special ; Restricted 1. Résultat : conforme.
- [x] Étape 7 : 6 cas : rz004 Vibranium Gun : Special (attaque) -> 2 degats a un ennemi | rz004 Vibranium Gun : Special -> perce la carte Tenace de l'ennemi (piercing) | rz004 Vibranium Gun : attaque de BASE a distance -> pas de riposte de M.O.D.O.K. ; seule la riposte  | rz004 Vibranium Gun : TEMOIN le Special (attaque) n'est PAS a distance : il contre-attaque... M.O.D. | rz004 Vibranium Gun : TEMOIN sans le pistolet, la riposte de M.O.D.O.K. frappe Roz (2 degats) apres  | rz004 Vibranium Gun : valeurs imprimees TECH WEAPON WAKANDA, Restricted 1. Substitution : **rouges 4/6** (restent verts sans le module : rz004 Vibranium Gun : TEMOIN sans le pistolet, la riposte de M.O.D.O.K. frappe Roz (2 dega ; rz004 Vibranium Gun : valeurs imprimees TECH WEAPON WAKANDA, Restricted 1)
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Journal lu : « Roz gagne (ranged) de Vibranium Gun », « ignore Retaliate sur M.O.D.O.K. » ; Special : « va attaquer (+2), avec (Perçant) ».
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminée : **NON (provisoire)** : seule manque la partie réelle jouée par un humain (gate du héros).

### rz005 : Wakandan Jumpsuit — AMÉLIORATION, coût 3, [energy]. ARMOR. TECH. WAKANDA

> You get +3 hit points.
> Special (thwart) : Remove 2 threat from a scheme.

- [x] Étape 2 : cartes de référence : `01039`/`bw013` (`GiveKeywordToAttached("You", health=N)`) ; Special (thwart) : `51010` Kimoyo Beads.
- [x] Étape 5 : mots-pièges vérifiés : « YOU get +3 hit points » (identité, pas seulement la face héros) ; « a scheme » (principale ou annexe). Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : +3 PV ; 2 menaces. Résultat : conforme.
- [x] Étape 7 : 3 cas : rz005 Wakandan Jumpsuit : « You get +3 hit points » | rz005 Wakandan Jumpsuit : Special (contre) -> 2 menaces retirees | rz005 Wakandan Jumpsuit : valeurs imprimees ARMOR TECH WAKANDA. Substitution : **rouges 2/3** (restent verts sans le module : rz005 Wakandan Jumpsuit : valeurs imprimees ARMOR TECH WAKANDA)
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Jumpsuit résolue 35 fois dans les journaux.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminée : **NON (provisoire)** : seule manque la partie réelle jouée par un humain (gate du héros).

### rz006 : Wakandan Stealth Tech — AMÉLIORATION, coût 2, [mental]. TECH. WAKANDA

> Roz gets +1 DEF.
> Special : Draw 1 card (limit once per round).
> Special : Reduce the cost of the next card you play this turn by 1 (limit once per round).

- [x] Étape 2 : cartes de référence : pioche : `01025` ; coût de la prochaine carte : `nt008`, `im001b` (`Worlds.UpdateNextCardPlayCost(joueur, -1, effect, in_this="Turn")`) ; choix entre deux effets : `51025` (`ChooseAbilities` + `ForChoiceAbility`).
- [x] Étape 5 : mots-pièges vérifiés : DEUX Specials imprimés : **DÉCISION UTILISATEUR du 26/10/2026 : « resolve the Special » n'en résout qu'UN SEUL, au choix du joueur** (« the Special », singulier ; chacun garde sa limite). Rendu : UNE capacité `Special` pour le moteur (donc UNE résolution comptée pour rz002 / rz003), qui fait choisir entre les deux effets ; seul un effet dont la limite du round est LIBRE est proposé ; limite = marqueur de round posé sur la carte à l'effet (pas `LimitOncePerRound()`, qui se consommerait même quand l'AUTRE effet est choisi) ; « the NEXT card you play THIS TURN » ; « Roz gets +1 DEF » (face héros). Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : +1 DEF ; pioche 1 ; -1 de coût. Résultat : conforme.
- [x] Étape 7 : 5 cas : rz006 Wakandan Stealth Tech : « Roz gets +1 DEF » | rz006 Wakandan Stealth Tech : Special -> pioche 1 carte | rz006 Wakandan Stealth Tech : TEMOIN D'EPUISEMENT, deux resolutions dans le round -> UNE seule pioch | rz006 Wakandan Stealth Tech : Special -> la PROCHAINE carte jouee ce tour coute 1 de moins (Haymaker | rz006 Wakandan Stealth Tech : TEMOIN sans Special, Haymaker coute 2 -> injouable avec UNE ressource. Substitution : **rouges 4/5** (restent verts sans le module : rz006 Wakandan Stealth Tech : TEMOIN sans Special, Haymaker coute 2 -> injouable avec UNE )
      **26/10/2026** : +1 cas « UNE résolution = UN seul Special (la réduction n'est PAS appliquée quand on pioche) » : VU ROUGE sur l'ancien code (« 01087 n'est plus en main : la carte a été jouée
      alors qu'elle ne devait pas l'être »), vert après. Piège de mesure : la carte piochée fournit une ressource et aurait payé le second point de Haymaker ; le deck est donc vidé et recréé
      avec UNE carte de rencontre (01098, sans ressource). Les cas « réduction » et « témoin d'épuisement » utilisent maintenant DEUX résolutions (pioche puis réduction). Substitution : **rouges 4/6**
      (verts : le cas « UN seul Special », qui mesure une ABSENCE d'effet et reste vert quand le module disparaît ; et le témoin sans Special).
- [x] Étape 7 bis : limite imprimée ? OUI (deux « limit once per round ») : cas TÉMOIN d'épuisement : 2 résolutions, 1 seule pioche.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Stealth Tech : 136 lignes de journal (Special résolu, pioche).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminée : **NON (provisoire)** : partie réelle jouée par un humain manquante. (Q3 tranchée par l'utilisateur le 26/10/2026 : UN seul Special, au choix.)

### rz007 : Agent of Wakanda — AMÉLIORATION, coût 2, [physical]. TITLE. WAKANDA

> Roz gets +1 THW.
> Response : After you resolve a "Special" ability on another card, place 1 agent counter here.
> Special : Exhaust Agent of Wakanda and remove 6 agent counters → stun or confuse an enemy.

- [x] Étape 2 : cartes de référence : `storm/36007` (`AfterPlayerResolveAbility(..., which_abilities=["Special"])`) ; compteurs : `ch015` (`CostFunc.Counter`), `ch019` (`PlaceCountersOn`) ; stun/confuse : `nebu/22005` (`ChooseAbilities`).
- [x] Étape 5 : mots-pièges vérifiés : « on ANOTHER card » (`message.trigger is not effect.this`) ; « exhaust AND remove 6 » : deux coûts obligatoires ; compteur `agent` déclaré (`COUNTER`, `compteurs-fr.ts`) ; « stun OR confuse ». Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : +1 THW ; 6 compteurs (relu sur le zoom du scan). Résultat : conforme.
- [x] Étape 7 : 5 cas : rz007 Agent of Wakanda : « Roz gets +1 THW » | rz007 Agent of Wakanda : Response -> un Special resolu sur une AUTRE carte (Jumpsuit) place 1 compte | rz007 Agent of Wakanda : TEMOIN son propre Special ne place PAS de compteur (« another card ») | rz007 Agent of Wakanda : Special -> ou DESORIENTE un ennemi (6 compteurs, carte inclinee) | rz007 Agent of Wakanda : CONTRE-CAS avec 5 compteurs seulement -> le Special n'a pas lieu. Substitution : **rouges 4/5** (restent verts sans le module : rz007 Agent of Wakanda : CONTRE-CAS avec 5 compteurs seulement -> le Special n'a pas lieu)
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Agent of Wakanda : 200 lignes, compteur placé à chaque Special d'une autre carte.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI (compteurs sur l'amélioration) : `roz-plateau.test.ts` vert d'emblée (4 puis 6 compteurs dessinés).

Carte terminée : **NON (provisoire)** : seule manque la partie réelle jouée par un humain (gate du héros).

### rz008 : * A.T.M.C.P. — SOUTIEN unique, coût 1, [physical]. VEHICLE. WAKANDA

> You gain the AERIAL trait.
> Special : Exhaust A.T.M.C.P. → choose 1 : • Ready your identity. • Change form.

- [x] Étape 2 : cartes de référence : `bw013` (`GiveKeywordToInPlayWhenApplyThis("You", ...)` pour un SOUTIEN) ; `45016` (`ChooseAbilities`) ; `01025` (`ChangeToOtherIdentityForm`).
- [x] Étape 5 : mots-pièges vérifiés : « you gain the AERIAL trait » (continu) ; « choose 1 » ; « Ready your IDENTITY ». Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : coût 1. Résultat : conforme.
- [x] Étape 7 : 3 cas : rz008 A.T.M.C.P. : « You gain the AERIAL trait » | rz008 A.T.M.C.P. : Special, 1re branche -> Roz epuisee est redressee, le vehicule s'incline | rz008 A.T.M.C.P. : Special, 2e branche -> change de forme (Roz passe en alter ego). Substitution : **rouges 3/3**
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : A.T.M.C.P. dans 31 lignes de journal.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI (soutien dessiné) : plateau vert.

Carte terminée : **NON (provisoire)** : seule manque la partie réelle jouée par un humain (gate du héros).

### rz009 : Trained Shots — ÉVÉNEMENT, coût 2, [energy] (x2). SKILL

> Hero Action : Deal 2 damage to an enemy. Resolve the "Special" ability on a WAKANDA upgrade. Resolve the "Special" ability on a WAKANDA upgrade.

- [x] Étape 2 : cartes de référence : `01022` (Hero Action d'événement) ; `51025` Heart of the Panther (`ChooseAbilities` + `ResolveSpecialAbility`).
- [x] Étape 5 : mots-pièges vérifiés : DEUX résolutions séparées (la même amélioration peut servir deux fois) ; « WAKANDA UPGRADE » (type Upgrade) ; pas de « (attack) » imprimé. Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : 2 dégâts ; 2 résolutions. Résultat : conforme.
- [x] Étape 7 : 2 cas : rz009 Trained Shots : 2 degats a un ennemi, puis DEUX fois le Special d'une amelioration WAKANDA (Ju | rz009 Trained Shots : sans amelioration WAKANDA, seuls les 2 degats partent. Substitution : **rouges 2/2**
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Trained Shots : 44 lignes de journal.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminée : **NON (provisoire)** : partie réelle jouée par un humain manquante ; arbitrage en attente : Q4 : « Resolve ... Resolve ... » : la même amélioration peut être choisie deux fois (recommandé) ou deux améliorations différentes ?

### rz010 : Negotiator — ÉVÉNEMENT, coût 2, [mental] (x2). SKILL

> Hero Action : Remove 2 threat from a scheme. Resolve the "Special" ability on a WAKANDA upgrade. Resolve the "Special" ability on a WAKANDA upgrade.

- [x] Étape 2 : cartes de référence : `01023` (`RemoveThreatFromSchemes`) ; `rz009` (même helper).
- [x] Étape 5 : mots-pièges vérifiés : pas de « (thwart) » imprimé ; deux résolutions indépendantes. Nom : la carte imprime « Negotiator », la decklist « Negotiations » (nom de la carte retenu). Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : 2 menaces ; 2 résolutions. Résultat : conforme.
- [x] Étape 7 : 1 cas : rz010 Negotiator : retire 2 menaces, puis DEUX fois le Special d'une amelioration WAKANDA (Jumpsuit). Substitution : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Negotiator : 40 lignes de journal.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminée : **NON (provisoire)** : partie réelle jouée par un humain manquante ; arbitrage en attente : Q4 (suite).

### rz011 : Nimble — ÉVÉNEMENT, coût 1, [energy] (x2). DEFENSE. SKILL

> Hero Interrupt (defense) : When you would take any amount of damage, prevent 3 of that damage. Resolve the "Special" ability of a WAKANDA card you control.

- [x] Étape 2 : cartes de référence : `05005` Wiggle Room / `14015` Side Step (`WhenUnitWouldTakeDamage` + `PreventDamage(3)`) ; Special : `51025`.
- [x] Étape 5 : mots-pièges vérifiés : « prevent 3 of THAT damage » ; « Special of a WAKANDA card YOU CONTROL » (tout type de carte à Special). Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : prévenir 3 ; coût 1. Résultat : conforme.
- [x] Étape 7 : 3 cas : rz011 Nimble : 4 degats de Rhino (ATK 2 + boost 2) -> 3 sont prevenus, 1 passe | rz011 Nimble : TEMOIN sans Nimble, Rhino frappe pour 4 | rz011 Nimble : resout ensuite le Special d'une carte WAKANDA (Stealth Tech : pioche 1). Substitution : **rouges 2/3** (restent verts sans le module : rz011 Nimble : TEMOIN sans Nimble, Rhino frappe pour 4)
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Nimble : 54 lignes de journal.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminée : **NON (provisoire)** : seule manque la partie réelle jouée par un humain (gate du héros).

### rz012 : Hand-to-Hand — ÉVÉNEMENT, coût 0, [physical] (x2). SKILL

> Response : After a minion or side scheme enters play, resolve the "Special" ability on 1 WAKANDA card you control.

- [x] Étape 2 : cartes de référence : `01024` (Response d'événement) ; `27189a` (`AfterCardEnterPlay(..., CardFinder(card_type=Minion|SchemeSide2))`).
- [x] Étape 5 : mots-pièges vérifiés : « Response » sans « Hero » ; « minion OR SIDE scheme » (jamais le complot principal) ; « 1 WAKANDA card ». Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : coût 0. Résultat : conforme.
- [x] Étape 7 : 2 cas : rz012 Hand-to-Hand : un sbire entre en jeu -> Response, Special d'une carte WAKANDA (Jumpsuit : -2 m | rz012 Hand-to-Hand : une manigance annexe entre en jeu -> le meme Special. Substitution : **rouges 2/2**
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Hand-to-Hand : 32 lignes de journal.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminée : **NON (provisoire)** : seule manque la partie réelle jouée par un humain (gate du héros).

### rz013 : Energy / rz014 Genius / rz015 Strength — RESSOURCES Basic (reskins), Max 1 par deck

> Max 1 per deck. (RES YY / BB / RR)

- [x] Étape 2 : cartes de référence : `01088`-`01090` officiels (mêmes valeurs) ; décision Hellcat `hc023-hc026` : reskins de l'auteur gardés en doublons, pas en art alternatif.
- [x] Étape 5 : mots-pièges vérifiés : valeurs imprimées identiques aux officielles (`RES`, `MaxPerDeck`, `Class`). Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : RES YY / BB / RR. Résultat : conforme.
- [x] Étape 7 : 1 cas : rz013 Energy : ressource [energy][energy], Max 1 par deck (reskin de 01088). Substitution : sans objet (aucun script : carte à données seules, valeurs imprimées vérifiées par le cas).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Aucun script (carte à données seules) ; les ressources sont dépensées en autoplay.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminée : **NON (provisoire)** : partie réelle jouée par un humain manquante ; arbitrage en attente : Q5 : reskins rz013-rz015 gardés comme cartes à part (précédent Hellcat) ou convertis en arts alternatifs de 01088-01090 ?
- [x] **26/10/2026, arbitrage reskins** (RR « A copy of a card is defined by title » + GUIDE §12 bis) : ces trois ressources ne changent que l'image de `01088` / `01089` / `01090` : ART ALTERNATIF des ressources doubles. Traitement, comme Gwenpool / Beast / Binary : collection `roz` dans `COLLECTIONS` (`ui-app/src/board/variantes.ts`) ET dans `COLLECTIONS_RESSOURCES` (`public/js/prepare/app.js`, proposée par défaut au héros « Roz » : `collectionDuHeros`). Les cartes restent dans `cards.json` (précédent TMNT / Gwenpool).
      « Max 1 per deck » par TITRE : `validerDeck` (`public/js/deckbuilder/regles.js`, `cleCopie` = titre|sous-titre) compte déjà `01088` + le reskin comme un même titre ; **aucun correctif nécessaire**, preuve : `tools/tests-lanceur/regles-ressources-doubles-par-titre.test.mjs` (4 verts : chaque reskin du dépôt + son officielle = « Trop d’exemplaires de « Energy » : 2/1 », deux mêmes reskins idem, un seul légal, trois titres différents sans gêne). Le moteur n'applique pas MaxPerDeck (seul le constructeur le juge).
      Collection : `ui-app/src/board/resources-art-packs-fanmade-2026-10.test.ts` (45 verts : ordre Energy/Genius/Strength, wizard aligné, images présentes ; ROUGE vu avant le câblage : 18 échecs sur 27, puis rouge à nouveau en retirant l'entrée du wizard).
      Carte terminée : NON (provisoire) : partie réelle humaine (voir la collection « Roz » dans la modale du héros et les trois ressources à l'écran).

### rz016 : Weighed Down — OBLIGATION (« Give to the Rosalind Solomon player »), boost 2

> Forced Response : After you resolve the "Special" ability on a card you control, take 1 damage.
> Alter-Ego Action : Take 1 damage for each card you control with a "Special" ability (to a maximum of 5 damage). If you take: • 2 or fewer damage → discard this card. • 3 or more damage → remove this card from the game.

- [x] Étape 2 : cartes de référence : `11018` Weakened (Forced Response persistante) ; `storm/36007` ; `PlayerActionToDiscardThis`, `01160` (`RemoveAllFromGame`) ; `DealDamage` rend le total infligé.
- [x] Étape 5 : mots-pièges vérifiés : « AFTER you resolve ... ON A CARD YOU CONTROL » ; « for each CARD you control WITH a Special » (cartes qui IMPRIMENT un Special, plafond 5) ; « If you TAKE » (dégâts réellement subis) ; « 2 OR FEWER » défausse (rencontre) / « 3 OR MORE » retirée. Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : 1 dégât par Special ; plafond 5 ; seuil 2 / 3. Résultat : conforme.
- [x] Étape 7 : 4 cas : rz016 Weighed Down : Forced Response, apres un Special resolu sur une carte controlee -> 1 degat a l | rz016 Weighed Down : Alter-Ego Action avec 2 cartes a Special (Jumpsuit, Stealth Tech) -> 2 degats,  | rz016 Weighed Down : Alter-Ego Action avec 3 cartes a Special -> 3 degats, RETIREE de la partie | rz016 Weighed Down : plafond de 5 degats (6 cartes a Special). Substitution : **rouges 4/4**
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Weighed Down : 68 lignes de journal : 1 dégât à chaque Special, 5 dégâts en alter ego.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminée : **NON (provisoire)** : partie réelle jouée par un humain manquante ; arbitrage en attente : Q6 : « each card you control with a Special » compte le héros Roz elle-même et les alliés officiels à Special (Okoye, Aneka, Ayo) : recommandé OUI (toute carte contrôlée qui imprime un Special). Confirmer ?

### rz017 : * Dario Agger — SBIRE NÉMÉSIS, PV 3, ATK 1, SCH 3, boost 2. ROXXON

> Forced Interrupt : When a player would attack Dario Agger, that player must discard an upgrade or support from their hand or play area. If no card is discarded this way, Dario Agger cannot be defeated by this attack.

- [x] Étape 2 : cartes de référence : `WhenUnitWouldBeAttacked` (`do_attack.py`) ; « cannot be defeated » : `aa016`/`16080b` (`UnitCannotBeDefeatedWhile`) en TEMPORAIRE `until_event_end=message` (`04004`, `tg006`) ; choix de carte : `14015` (`AskChooseFace`).
- [x] Étape 5 : mots-pièges vérifiés : « THAT player » = le contrôleur de l'attaquant (héros ou allié) ; « upgrade OR support FROM hand OR play area » ; « IF NO CARD IS DISCARDED » ; protection limitée à CETTE attaque. Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : PV 3, ATK 1, SCH 3, boost 2 ; trait ROXXON ajouté. Résultat : conforme.
- [x] Étape 7 : 5 cas : rz017 Dario Agger : valeurs imprimees PV 3, ATK 1, SCH 3, ROXXON | rz017 Dario Agger : attaque avec une amelioration en main -> elle est defaussee ET Dario (2 degats d | rz017 Dario Agger : aucune amelioration ni soutien a defausser -> il ne peut pas etre vaincu par cet | rz017 Dario Agger : TEMOIN la meme attaque contre un sbire ordinaire (3 PV, 2 degats) le vainc | rz017 Dario Agger : un SOUTIEN en jeu peut etre defausse a la place d'une amelioration. Substitution : **rouges 3/5** (restent verts sans le module : rz017 Dario Agger : valeurs imprimees PV 3, ATK 1, SCH 3, ROXXON ; rz017 Dario Agger : TEMOIN la meme attaque contre un sbire ordinaire (3 PV, 2 degats) le v)
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Dario Agger : 54 lignes de journal.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI (sbire engagé portant ses attachements) : plateau vert.

Carte terminée : **NON (provisoire)** : partie réelle jouée par un humain manquante ; arbitrage en attente : Q7 : sans carte à défausser, Dario reste en jeu à 0 PV (lecture littérale, recommandé) ou ses dégâts sont plafonnés pour qu'il garde 1 PV ?

### rz018 : Legal Council — MANIGANCE ANNEXE némésis, menace 2 par joueur, boost 2, 1 icône Accélération

> Forced Interrupt : When you would exhaust or use a "Special" ability on an upgrade you control, spend 1 resource of any type or cancel its effects.

- [x] Étape 2 : cartes de référence : `WhenCardWouldResolveAbility` (`33008`) ; annulation : `message.SetBeInstead(effect)` ; paiement : `Cost("1")` (`rainy/90115`), `27176` (`ForChoiceAbilityWithCost`).
- [x] Étape 5 : mots-pièges vérifiés : « EXHAUST OR USE a Special » : deux déclencheurs, UN prix ; « of ANY type » = `Cost("1")` (pas `Cost("G")`, icône wild) ; « upgrade YOU control » (le joueur est le contrôleur de l'amélioration). Icône d'Accélération identifiée contre `01109`. Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : menace 2 par joueur (`StartingThreat "2*"`), boost 2, `Acceleration 1`. Résultat : conforme.
- [x] Étape 7 : 4 cas : rz018 Legal Council : valeurs imprimees menace 2 par joueur, 1 icone Acceleration, boost 2 | rz018 Legal Council : le Special de Jumpsuit est ANNULE (on refuse de payer) -> la menace ne bouge p | rz018 Legal Council : on PAIE 1 ressource (Strength) -> le Special de Jumpsuit part et la main est v | rz018 Legal Council : TEMOIN sans la manigance, aucun choix : le Special de Jumpsuit part et la main. Substitution : **rouges 2/4** (restent verts sans le module : rz018 Legal Council : valeurs imprimees menace 2 par joueur, 1 icone Acceleration, boost 2 ; rz018 Legal Council : TEMOIN sans la manigance, aucun choix : le Special de Jumpsuit part )
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Legal Council : 37 lignes de journal : choix payer / annuler proposé, un Special annulé.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI (manigance annexe paysage) : plateau vert.

Carte terminée : **NON (provisoire)** : partie réelle jouée par un humain manquante ; arbitrage en attente : Q8 : le moteur n'a aucun message « would exhaust ». Lecture provisoire : toute capacité d'une de vos améliorations qui est un Special OU dont le coût incline la carte déclenche le choix payer 1 ressource / annuler. L'inclinaison est déjà payée si on annule. Acceptable ?

### rz019 : * Minotaur — ATTACHEMENT némésis, boost 2. CREATURE. SCH -2 / ATK +3★

> Attach to Dario Agger. If you cannot, this card gains incite 1 and surge.
> Dario Agger gets +3 hit points and gains retaliate 1.
> ★ Dario Agger attacks gain overkill.

- [x] Étape 2 : cartes de référence : `01163` Genetically Enhanced, `jj021` (`ThisGainIncite`), `22030` ; `ho016`/`50107b` (`UnitAttackGainKeyword(overkill=True)`).
- [x] Étape 5 : mots-pièges vérifiés : « Attach to Dario Agger » (nommé) ; « If you cannot, gains incite 1 AND surge » (seulement sans Dario) ; +3 PV ET Riposte 1 ; SCH -2 / ATK +3 : bonus imprimés de l'attache ; ★ toujours active. Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : +3 PV, Riposte 1, ATK +3, SCH -2 ; incite 1. Résultat : conforme.
- [x] Étape 7 : 1 cas : rz019 Minotaur : attache a Dario Agger -> +3 PV, Riposte 1, ATK +3, SCH -2. Substitution : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Minotaur : 3 lignes de journal (rare).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI (attachement sur un sbire) : plateau vert.

Carte terminée : **NON (provisoire)** : seule manque la partie réelle jouée par un humain (gate du héros).

### rz020 : Lawyers — ATTACHEMENT némésis (x2). PERSONA. SCH +1

> Attach to Dario Agger. Otherwise, attach to the villain.
> Attached character gains villainous. If the attached character is the villain, it gets an additional boost card when it schemes.
> Action : Spend 2 resources of any type → discard this card.

- [x] Étape 2 : cartes de référence : `nebu/22030` (`if_cannot_attach_to=Villain`) ; `hc010` (`villainous=1`) ; `sk125` (`GiveAdditionalBoostCardForThisActivation`, ici `WhenUnitWouldScheme`) ; `Cost("2")`.
- [x] Étape 5 : mots-pièges vérifiés : « attached CHARACTER gains villainous » (Dario OU le vilain) ; « additional boost card WHEN IT SCHEMES » (seulement le vilain, seulement quand il manigance) ; « 2 resources OF ANY TYPE » = `Cost("2")`. Résultat : conforme (texte lu sur le scan à l'écran).
- [x] Étape 6 : nombres texte ↔ code : SCH +1 ; villainous 1 ; 2 ressources. Résultat : conforme.
- [x] Étape 7 : 3 cas : rz020 Lawyers : Action, 2 ressources de n'importe quel type (Strength = 2) -> la carte est defaussee | rz020 Lawyers : TEMOIN une seule ressource (Emergency = 1) ne suffit pas -> la carte reste attachee | rz020 Lawyers : attache a Dario Agger -> villainous, SCH +1. Substitution : **rouges 3/3**
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay (8 parties, témoin She-Hulk) : Lawyers : 15 lignes de journal.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI (attachement sur un sbire) : plateau vert.

Carte terminée : **NON (provisoire)** : seule manque la partie réelle jouée par un humain (gate du héros).


## Questions en attente (à poser à l'utilisateur, une par carte, option recommandée en premier)

> **26/10/2026 : TOUTES TRANCHÉES** (règles + scans, `VERDICTS-REGLES-2026-10-26.md`) : Q1, Q4 à Q9 : option A confirmée ; **Q2** : appliquée (tout allié Thor, de tout joueur ; « once per TURN ») ;
> **Q3** : DÉCISION UTILISATEUR : UN seul Special, au choix (rz006). Le texte ci-dessous est conservé pour mémoire.

- Q1 : « Find » = deck + défausse (recommandé) ou deck seul ?
- Q2 : « each Thor ally » = tout allié nommé Thor que vous contrôlez, y compris les Thor officiels (recommandé), ou seulement ceux de ce pack ?
- Q2 (suite) : « once per turn » est rendu par « une fois par round » (identique en solo). Acceptable ?
- Q3 : deux Specials non nommés sur une carte : « resolve the Special ability on a card » les résout TOUS LES DEUX (recommandé) ou le joueur n'en choisit qu'un ?
- Q4 : « Resolve ... Resolve ... » : la même amélioration peut être choisie deux fois (recommandé) ou deux améliorations différentes ?
- Q4 (suite).
- Q5 : reskins rz013-rz015 gardés comme cartes à part (précédent Hellcat) ou convertis en arts alternatifs de 01088-01090 ?
- Q6 : « each card you control with a Special » compte le héros Roz elle-même et les alliés officiels à Special (Okoye, Aneka, Ayo) : recommandé OUI (toute carte contrôlée qui imprime un Special). Confirmer ?
- Q7 : sans carte à défausser, Dario reste en jeu à 0 PV (lecture littérale, recommandé) ou ses dégâts sont plafonnés pour qu'il garde 1 PV ?
- Q8 : le moteur n'a aucun message « would exhaust ». Lecture provisoire : toute capacité d'une de vos améliorations qui est un Special OU dont le coût incline la carte déclenche le choix payer 1 ressource / annuler. L'inclinaison est déjà payée si on annule. Acceptable ?
- Q9 : « The Power in All of Us » existe en deux impressions (`13024` Wasp, `46023` Iceman, même texte, `ability_link`) : la decklist ne dit pas laquelle ; `13024` retenue.

## À vérifier en partie réelle (aucun outil ne le remplace)

- Une partie complète avec Roz choisie dans la liste Fan-made (tuile, biographie au survol, image des 21 cartes).
- Les deux Thor : réduction de coût visible dans la main, Réponse donnée à CHAQUE allié Thor (y compris un Thor officiel).
- Le choix « dépenser 1 ressource / annuler » de Legal Council (rz018) : lisibilité de la fenêtre de paiement.
- Weighed Down : la défausse d'une obligation se range dans la défausse rencontre ; un Special résolu en forme alter ego.
- L'icône Accélération de Legal Council (comparée à Bomb Scare) et les 21 images : rendu des scans à l'écran.
