# She-Hulk « Why Not » (Merlin) : gabarits PROCESSUS-CARTE, 12 card_id

Pack `she_hulk_why_not`, préfixe `wn`, set 217. Source : zip « She-Hulk Release EN » déposé le 25/10/2026 (le zip FR
« Miss Hulk » est la She-Hulk OFFICIELLE du core, déjà en jeu : rien à créer). Variante de la She-Hulk officielle :
l'auteur a retouché au scotch 9 cartes du core ; deck `deck/starter/she_hulk_why_not.json` (`variante_de: "she_hulk"`,
`variante_nom: "Why Not (Merlin)"` ; le deck de base porte `variante_nom: "Officielle"`).

Cas : `Fusion/marvel-lcg-src/tools/cas/she_hulk_why_not.py` (filtre `[wn]`, **24 cas verts sur 24**, aucune exception
avalée avec `MCLCG_TRACE_CRASH`). Plateau : `ui-app/src/board/she-hulk-why-not-plateau.test.ts` (3 cas). Preuve par
substitution : `tools/substituer_pack.py .game-src 31000 wn0` = **12/12 cartes avec au moins un cas rouge sans leur module**
(les cas qui restent verts sont listés carte par carte ci-dessous).

## Arbitrages utilisateur du 25/10/2026 (questions posées une à une)

1. Ce zip devient une **variante fan-made** de la She-Hulk officielle (pas un nouveau héros, pas seulement les Team-Up).
2. **wn001a**, « for each ⛑ icon in play » + note « Did you look at my obligation? » : l'icône est l'**Accélération** ;
   on compte les icônes imprimées en jeu ET les pions Accélération (Legal Work 01160 en pose un).
3. **wn008**, note « If you have no one to stun, you cannot discard it » : si l'attaque a **vaincu** l'ennemi attaqué,
   la carte **reste** en jeu ; sinon elle se défausse et sonne, comme 01028.

Choix techniques (non discutés, GUIDE §9) : cartes inchangées reprises du core (01020 Hellcat, 01024 One-Two Punch x3,
obligation 01160, némésis 01161-01164) ; `player_deck` = celui du deck officiel `she_hulk.json` (re-skin d'un héros
officiel qui garde son deck, précédent `wolverine_x23` ; l'auteur ne fournit pas de decklist) ; les trois Team-Up Basic
(wn009-wn011) ne sont pas dans le deck de départ, on les ajoute au deckbuilder (Max 1 par deck) ; pas de biographie
(identité alternative d'un héros existant, PROCESSUS-HEROS étape 7).

## Gates du héros

- [x] Étapes 1 à 8 de PROCESSUS-HEROS : cartes (`cards.json`, pack `she_hulk_why_not`), scripts
      (`src/cards/pack/she_hulk_why_not/`), deck de départ, `sets_info.json` (« 217. Custom (She-Hulk Why Not) »),
      préfixe (`tools/prefixes_fanmade.json`), images (`assets/pics/wn*.jpg`, 615×882, non versionnées), textes FR
      (`ui-app/src/board/textes-fr-fanmade.ts`, gates `textes-fr-fanmade.test.ts` et `vocabulaire-*.test.ts` vertes).
      Biographie : sans objet (variante).
- [x] Légalité des decks (PROCESSUS-HEROS §10) : 0 signature étrangère dans un `player_deck`.
- [x] `verifier_tous_les_decks` : `she_hulk_why_not` « identite wn001a, main 6, deck 34 », `she_hulk` (touché) idem ;
      passe complète du 25/10/2026 : **158/158 decks montent une partie**.
- [x] `tools/test_cards.py` : 7467 modules OK, 0 erreur. `verifier_prefixes.py` OK. `verifier_traductions_fr.py` OK.
      `verifier_appels_modules.py she_hulk_why_not` OK, **calibré** (§9) : un appel inventé dans wn003 a été vu
      (« this.DealDamageInexistant n'existe pas »), puis retiré.
- [x] Autoplay : 8 parties (rhino/klaw × équilibré/agressif × 2), témoin She-Hulk officielle sur les mêmes 8 graines.
      0 traceback sur les 16 journaux, 0 blocage des deux côtés, durées équivalentes (3,5 à 4,5 rounds ; 0 victoire
      des deux côtés : le pilote, pas la carte). Journal lu : wn003 (2 dégâts à Klaw ET à Titania), wn004 (menace
      retirée, sans libellé thwart), wn001b (« 1 ⚠ empêché »), wn007 (21 activations), wn008 posée.
- [ ] **Une partie complète jouée par un humain avec la variante : NON FAITE.** Aucun outil ne la remplace.

Cartes en attente de cette seule gate : toutes. Les cartes non jouées par le pilote en autoplay (wn002, wn005 en jeu,
wn006, Team-Up wn009-wn011 absents du deck) ne sont couvertes que par leurs cas de capacité.

### wn001a : * She-Hulk (face HÉROS) — AVENGER. GAMMA. PV 15, THW 1, ATK 3, DEF 2, main 4.

« Do You Even Lift? » — **Response** : After you change to this form, deal 1 damage to an enemy for each [acceleration] icon in play.

- [x] Étape 2 : cartes de référence : `01019a` (même déclencheur `AfterUnitChangeForm(Response, "You", to_this_form=True)`) ;
      `44017` Barely a Scratch (`Worlds.GetIconsNum(effect, ["Acceleration"])`) ; `bw020` Namor (somme des `acceleration_token`).
- [x] Étape 5 : mots-pièges : « Response » (facultative, après) ; « to this form » (pas en passant en alter ego) ; « AN enemy »
      (une cible) ; « each icon in play » (imprimées + pions, arbitrage 2 ; zéro → pas de capacité proposée). Conforme.
- [x] Étape 6 : nombres : 1 dégât par icône ; PV 15, ATK 3, THW 1, DEF 2, main 4 (`desc` + cas « valeurs imprimées »). Conforme.
- [x] Étape 7 : cas : 2 pions → 2 ; Bomb Scare (icône imprimée) → 1 ; icône + 2 pions → 3 ; contre-cas 0 icône → 0 ; valeurs
      imprimées. Substitution : **rouges 3/5** (verts sans module : le contre-cas d'absence et les valeurs imprimées, assumés).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay, journal lu ligne à ligne (rhino équilibré 1 et agressif 1) : Legal Work 01160 pose 1 pion Accélération
      sur The Break-In!, Bomb Scare 01109 (1 icône imprimée) est en jeu ; au passage en héros, « She-Hulk s'active, cible Rhino » et
      inflige **2** dégâts = 1 pion + 1 icône. Les autres passages en héros, sans icône en jeu, ne proposent rien. Aucun incident.
- [x] Étape 8 bis : change ce qu'on voit ? NON (dégâts seulement).

Carte terminée : **NON (provisoire)** : seule manque la partie réelle jouée par un humain (gate du héros).

### wn001b : * Jennifer Walters (face ALTER EGO) — ATTORNEY. GAMMA. PV 15, REC 5, main 6.

« I Object! » — **Interrupt** : When threat would be placed on a scheme, prevent 1 of that threat. (Limit once per **phase**.)

- [x] Étape 2 : référence `01019b` (même fabrique `WhenThreatWouldBePlacedOn`, `PreventThreat(1)`), limite `.LimitOncePerPhase()`.
- [x] Étape 5 : « Interrupt » (avant la pose) ; « a scheme » (toute manigance) ; « once per PHASE » (l'auteur a remplacé « round »). Conforme.
- [x] Étape 6 : 1 menace prévenue ; PV 15, REC 5, main 6 (cas « valeurs imprimées »). Conforme.
- [x] Étape 7 : cas « Rhino manigance (1) → prévenue ». Substitution : **rouges 2/3** (vert sans module : valeurs imprimées).
      ⚠ Première version des cas fausse (piège noté en RECETTES §26) : la mise en place `SetThreat` en alter ego consommait déjà la
      limite ; corrigé en posant la menace en forme héros.
- [x] Étape 7 bis : limite imprimée OUI. Témoin d'épuisement : deux manigances de Rhino dans la même phase, menace 1 + 0 + 1 = **2**.
- [x] Étape 8 : autoplay : « 1 ⚠ empêché(s) d'être placé(s) sur Breakin' & Takin' ». Aucun incident.
- [x] Étape 8 bis : NON.

Carte terminée : **NON (provisoire)** : partie réelle (gate du héros).

### wn002 : Gamma Slam — Event, coût 3, [mental], ATTACK. SUPERPOWER. GAMMA.

**Hero Action** *(attack)* : Deal X damage to an enemy (to a maximum of 15). X is the amount of damage you have sustained.

- [x] Étape 2 : référence `01021` (texte identique ; retouches = coût 4 → 3, trait GAMMA ajouté, dans `cards.json`).
- [x] Étape 5 : « attack » (libellé `attack`) ; « maximum of 15 » (`min(15, ...)`) ; « you have sustained » (`sustained` de l'identité). Conforme.
- [x] Étape 6 : coût 3 (le cas paie avec exactement 3 ressources : 01090 + 01020 ; à 4, injouable) ; plafond 15. Conforme.
- [x] Étape 7 : cas « 5 dégâts subis → 5 à Rhino, payée avec 3 ressources ». Substitution : **rouges 1/1**.
- [x] Étape 7 bis : NON. Étape 8 : non jouée par le pilote (couverte par son cas). Étape 8 bis : NON.

Carte terminée : **NON (provisoire)** : partie réelle.

### wn003 : Ground Stomp — Event, coût 2, [mental], GAMMA. SUPERPOWER. (x2)

**Hero Action** : Deal **2** damage to each enemy.

- [x] Étape 2 : référence `01022` (`SetTarget(Enemy, range="All")`), valeur 1 → 2.
- [x] Étape 5 : « each enemy » (méchant ET sbires, `range="All"`). Conforme.
- [x] Étape 6 : 2 dégâts, coût 2. Conforme.
- [x] Étape 7 : cas « 2 dégâts à Rhino ET au sbire ». Substitution : **rouges 1/1**.
- [x] Étape 7 bis : NON. Étape 8 : autoplay, 2 dégâts à Klaw et à Titania (journal). Étape 8 bis : NON.

Carte terminée : **NON (provisoire)** : partie réelle.

### wn004 : Legal Practice — Event, coût 0, [physical], SKILL. (x2)

**Alter-Ego Action** : Choose and discard up to 5 cards from your hand → remove **2** threat from a scheme for each card discarded this way.

- [x] Étape 2 : référence `01023` (`CostFunc.Discard("YourHandCards", range=(1, 5))`), ×1 → ×2 ; l'auteur a BARRÉ « Thwart » et « (thwart) ».
- [x] Étape 5 : « up to 5 » ; « for each card » (2 × défaussées) ; plus de trait THWART ni de libellé thwart. Conforme.
- [x] Étape 6 : 5 cartes max, 2 menaces par carte, coût 0. Conforme.
- [x] Étape 7 : cas « 2 cartes défaussées → 4 menaces retirées (6 → 2) » ; cas des traits lus en main (SKILL seul).
      Substitution : **rouges 1/2** (vert sans module : les traits, qui sont des données).
- [x] Étape 7 bis : NON. Étape 8 : autoplay, menace retirée de The Break-In! (journal). Étape 8 bis : NON.

Carte terminée : **NON (provisoire)** : partie réelle.

### wn005 : Split Personality — Event, coût 3, [energy].

**Action** : Change your form. Then, draw up to your printed hand size. **Ready your identity.**

- [x] Étape 2 : référence `01025` + `Faces.ReadyAll([identité])` APRÈS la pioche (ordre du texte).
- [x] Étape 5 : « your identity » = la NOUVELLE forme après le changement ; « printed hand size » (celle de la nouvelle forme). Conforme.
- [x] Étape 6 : coût 3 (payé avec 3 ressources exactes). Conforme.
- [x] Étape 7 : cas « héros incliné → alter ego PRÊT, main 6 ». Substitution : **rouges 1/1**.
- [x] Étape 7 bis : NON. Étape 8 : défaussée pour payer en autoplay, pas jouée (couverte par son cas). Étape 8 bis : NON
      (changement de forme et inclinaison déjà dessinés par le rendu générique).

Carte terminée : **NON (provisoire)** : partie réelle.

### wn006 : Superhuman Law Division — Support, coût 1, [physical], LOCATION.

**Alter-Ego Action** : Exhaust Superhuman Law Division and spend a [mental] resource → remove **3** threat from a scheme.

- [x] Étape 2 : référence `01026` (coût `Exhaust("This")` + `Cost("B")`), 2 → 3 ; « (thwart) » barré : aucun libellé (déjà le cas en 01026).
- [x] Étape 5 : « and spend » (les deux parties du coût) ; « a scheme ». Conforme.
- [x] Étape 6 : 3 menaces, coût 1, [mental]. Conforme.
- [x] Étape 7 : cas « inclinée + [mental] → 5 → 2 ». Substitution : **rouges 1/1**.
- [x] Étape 7 bis : NON. Étape 8 : non jouée par le pilote. Étape 8 bis : NON.

Carte terminée : **NON (provisoire)** : partie réelle.

### wn007 : Focused Rage — Upgrade, coût 2, [energy], SKILL. (x2)

**Hero Action** : Exhaust Focused Rage and take 1 damage → draw 1 card.

- [x] Étape 2 : référence `01027` (texte identique ; retouche = coût 3 → 2, dans `cards.json`).
- [x] Étape 5 : « and take 1 damage » (seconde partie du coût, `TakeDamage(1, "Initiator")`). Conforme.
- [x] Étape 6 : coût 2 (payé avec une seule carte double) ; 1 dégât ; 1 carte. Conforme.
- [x] Étape 7 : cas « inclinée + 1 dégât → 1 carte » ; cas « coût 2 ». Substitution : **rouges 1/2** (vert sans module : le coût, donnée).
- [x] Étape 7 bis : NON. Étape 8 : 21 activations en autoplay, sans erreur. Étape 8 bis : NON.

Carte terminée : **NON (provisoire)** : partie réelle.

### wn008 : Superhuman Strength — Upgrade, coût 2, [mental], GAMMA. SUPERPOWER. (x2)

She-Hulk gets +2 ATK. **Forced Response** : After She-Hulk attacks, discard Superhuman Strength → stun the attacked enemy.
*(If there is no one to stun, you cannot discard this card.)*

- [x] Étape 2 : référence `01028` (`GiveKeywordToAttached(attack=2)`, `AfterUnitAttackEnd` + `Discard("This")` + `SetTarget("Targets", canbe_stunned=True)`).
- [x] Étape 5 : « Forced » (obligatoire) ; « the attacked enemy » ; note de l'auteur (arbitrage 3) : condition `ennemi_attaque_en_jeu`.
      ⚠ Mesuré par MUTATION : sans cette condition, le cas « ennemi vaincu → la carte reste » reste VERT : 01028 ne paie déjà pas le
      coût quand la cible a disparu. La condition est donc redondante, gardée pour dire l'arbitrage dans le code.
- [x] Étape 6 : +2 ATK (3 + 2 = 5 dégâts mesurés), coût 2. Conforme.
- [x] Étape 7 : cas « Rhino : 5 dégâts, sonné, carte défaussée » ; cas « sbire vaincu : carte restée ». Substitution : **rouges 1/2**
      (vert sans module : « la carte reste », absence d'effet).
- [x] Étape 7 bis : NON. Étape 8 : posée en autoplay, appliquée à She-Hulk (journal). Étape 8 bis : OUI (amélioration posée,
      Sonné sur l'ennemi) : `she-hulk-why-not-plateau.test.ts`, vert d'emblée, aucun correctif (rendu générique).

Carte terminée : **NON (provisoire)** : partie réelle.

### wn009 : Hey you! — Event Basic, coût 0, [wild], TACTIC. Team-Up (Deadpool and She-Hulk). Max 1 per deck.

**Action** : Stun and confuse an enemy. Remove Hey you! from the game.

- [x] Étape 2 : fiche `mots-cles/teamup.md` ; `47022` Unlikely Duo (`SetTarget("TeamUp")` + `SetTarget2(Enemy)`) ; `16175` Power Unleashed (`RemoveAllFromGame`).
- [x] Étape 5 : « Stun AND confuse » (deux statuts, même ennemi) ; « Remove from the game » (zone retirée, pas défausse). Conforme.
      ⚠ Bug trouvé par le cas : relire `effect.targets2` levait une assertion avalée (Sonné posé, Désorienté jamais) ; corrigé, noté
      dans la fiche teamup et en RECETTES §26.
- [x] Étape 6 : coût 0, Max 1 par deck (`desc.MaxPerDeck`). Conforme.
- [x] Étape 7 : cas « avec Deadpool (allié 40024) : Sonné + Désorienté, retirée » ; témoin « sans Deadpool : reste en main ».
      Substitution : **rouges 1/2** (vert sans module : le témoin d'injouabilité, porté par `desc.TeamUp`).
- [x] Étape 7 bis : NON. Étape 8 : absente du deck de départ (Basic à ajouter), non jouée en autoplay. Étape 8 bis : OUI (deux
      statuts) : cas plateau vert d'emblée.

Carte terminée : **NON (provisoire)** : partie réelle (et autoplay sans occasion de la jouer).

### wn010 : Gamma Power — Event Basic, coût 0, [wild], GAMMA. TACTIC. Team-Up (Hulk and She-Hulk). Max 1 per deck.

**Action** : Place a total of 2 stun status cards on up to 2 enemies. Remove Gamma Power from the game.

- [x] Étape 2 : comme wn009 ; `27182b` (`SetTarget(Enemy, range=(1, 2))`).
- [x] Étape 5 : « a TOTAL of 2 » sur « up to 2 » : deux ennemis → un Sonné chacun ; un seul ennemi → les deux cartes vont sur lui
      (le moteur n'en garde qu'une sauf Steady : règle du jeu, pas un arbitrage). Conforme.
- [x] Étape 6 : 2 cartes, 2 ennemis max, coût 0. Conforme.
- [x] Étape 7 : cas « Hulk (allié 01050) + 2 ennemis → Sonné chacun, retirée » ; témoin « sans Hulk ». Substitution : **rouges 1/2**.
- [x] Étape 7 bis : NON. Étape 8 : non jouée (absente du deck). Étape 8 bis : OUI : cas plateau vert d'emblée.

Carte terminée : **NON (provisoire)** : partie réelle.

### wn011 : A Spider on the Wall — Event Basic, coût 0, [wild], TACTIC. Team-Up (She-Hulk and Spider-Man). Max 1 per deck.

**Action** : Ready She-Hulk and draw 3 cards. Remove A Spider on the Wall from the game.

- [x] Étape 2 : comme wn009 ; `hc020` Green Hell (`Faces.ReadyAll` sur les personnages du Team-Up) ; `ub019` (`IsName` parmi les cibles).
- [x] Étape 5 : « Ready **She-Hulk** » (seulement elle, pas Spider-Man) ; « draw 3 » (le joueur qui joue). Conforme.
- [x] Étape 6 : 3 cartes, coût 0. Conforme.
- [x] Étape 7 : cas « Spider-Man (allié 13019) : She-Hulk redressée, main 1 → 4, retirée » ; témoin « sans Spider-Man ».
      Substitution : **rouges 1/2**.
- [x] Étape 7 bis : NON. Étape 8 : non jouée (absente du deck). Étape 8 bis : NON (zone retirée non dessinée).

Carte terminée : **NON (provisoire)** : partie réelle.

## À vérifier en partie réelle (aucun outil ne le remplace)

- Toute la variante, jouée par un humain dans le navigateur : choix de « Why Not (Merlin) » dans la fenêtre du héros, agrément.
- wn001a avec une vraie Legal Work (01160) qui a posé un pion Accélération : le nombre de dégâts proposé.
- Les trois Team-Up ajoutés depuis le deckbuilder (Max 1 par deck), joués avec un vrai allié ou une vraie identité Deadpool /
  Hulk / Spider-Man en multijoueur : les cibles TeamUp ne doivent rien demander (correctif du 12/10/2026), seul l'ennemi l'est.
