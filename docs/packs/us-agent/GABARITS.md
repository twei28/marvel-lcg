# U.S. Agent (DesignHacker, « SEALED ») : gabarits PROCESSUS-CARTE, 17 card_id

Pack `us_agent`, préfixe `us` (`ua` est pris par TMNT Aspect Aggression), set 218. Source : zip « U.S. AGENT (SEALED) » déposé le 25/10/2026
(15 cartes héros dont 3 Bouncing Bulwark, 2 Deflection, 2 Reckless, 2 Roundhouse ; obligation ; 5 cartes némésis dont 2 Seeing Red ;
« US Agent Starter Deck.png » = decklist de l'auteur). Les impressions multiples d'un même titre sont UN seul card_id (texte identique,
vérifié visuellement et numériquement). Aucune des 17 cartes n'existait dans le jeu (les « U.S. Agent » 04014 / 56075 / sw014 sont des alliés, non touchés).

## Arbitrages du 26/10/2026 (RR 1.8 + scans)
Les questions en attente de ce fichier ont été tranchées par le Rules Reference et les scans (détail : `VERDICTS-REGLES-2026-10-26.md`, liste : `docs/rapports/2026-10-26-arbitrages-heros-fanmade.md`). Seules deux cartes changent : **us004** (coût en dégâts : tout ou rien) et **us010** (la rafale re-propose la Réponse). Les autres questions sont « A confirmé » : le code était déjà conforme.

## Consignes de l'utilisateur appliquées
Doute de carte : option recommandée codée, carte marquée « NON (provisoire) » avec la question exacte (ci-dessous). Aucune question posée en cours de route.

## Gates du héros
- [x] Étapes 1 à 8 de PROCESSUS-HEROS : cartes (`cards.json`, pack `us_agent`), scripts (`src/cards/pack/us_agent/`), deck de départ
      (`deck/starter/us_agent.json`, **player_deck = la decklist FOURNIE par l'auteur, 25 cartes officielles**), `sets_info.json`
      (« 218. Custom (U.S. Agent) »), préfixe `us`, images (`assets/pics/us001a.jpg`…`us016.jpg`, petit côté 615, non versionnées),
      biographie (`heros-info.js`, `us001a`), textes FR (`textes-fr-fanmade.ts` + copie générée `public/js/traduction/textes-fr-fanmade.js`).
- [x] Règle de deck « Master of None » : `metadata.deckbuilding` (aspects libres, `types_interdits: [Ally]`, `classes_interdites: [Basic]`).
      **Seule modification de code partagé : `public/js/deckbuilder/regles.js` (fonction `classesInterdites` + une branche dans `validerDeck`)**, test `tools/tests-lanceur/regles-us-agent.test.mjs`.
- [x] Homonymes de la decklist tranchés par le titre officiel d'origine : Determination 21052 (pas 61022), One Way or Another 22015 (pas uj024), Go All Out 29017 (pas ul009), What Doesn't Kill Me 27016 (pas up042).
- [x] Légalité des decks (PROCESSUS-HEROS §10) : 0 signature étrangère dans `player_deck` (25 cartes d'aspect, aucune classe Hero).
- [x] `tools/test_cards.py` : 0 erreur ; `verifier_prefixes.py` OK ; `verifier_appels_modules.py us_agent` OK et **calibré** (§9 : un appel inventé dans us005 a été vu, puis retiré).
- [x] Cas : `tools/cas/us_agent.py` (filtre `[us]`) : **100/100 verts**, aucune exception avalée (`MCLCG_TRACE_CRASH`) ; les `<E> ... failed` des journaux sont les cartes volontairement injouables des cas témoins.
- [x] Plateau : `ui-app/src/board/us-agent-plateau.test.ts` (8 cas, verts d'emblée : rendu générique ; seule la suppression de la carte de la table les rougit).
- [ ] RESTE : voir « Résultats des gates lourdes » ci-dessous, et **une partie complète jouée par un humain : NON FAITE** (aucun outil ne la remplace).
- [ ] Biographie : preuve « au survol du héros dans le wizard » **non faite en navigateur** (module chargé en node, clé `us001a` = `heroCardId`).


## Résultats des gates lourdes (25/10/2026)
- **Substitution** (`tools/substituer_pack.py`, carte par carte car la passe globale sortait « rapport illisible » sous verrou partagé) : chaque carte a au moins un cas ROUGE sans son module ; les cas qui restent verts sont des valeurs imprimées ou des témoins d'absence (détail par carte ci-dessous). Pack intact après coup (`diff -rq` identique à la sauvegarde).
- **Deck** : `DECK_NOM=us_agent verifier_tous_les_decks.py` : « identite us001a, main 6, deck 34 » (OK). Passe complète des 158+ decks : NON refaite (aucun fichier moteur Python touché par ce pack ; seuls `data/*.json` partagés et `regles.js`).
- **Autoplay** : 8 parties `us_agent` (rhino/klaw x équilibré/agressif x 2) contre 8 du témoin `captain_america` : 0 NameError / AttributeError / TypeError / KeyError / AssertionError sur les 8 journaux. Une partie `us_agent` (klaw, équilibré, graine 2) est étiquetée « bloquee » par l'outil : son journal se termine par « Secret Rendezvous est accomplie » (défaite normale de la manigance), pas par une boucle ; le témoin n'a aucune partie bloquée. Victoires : us_agent 1/8, témoin 0/8 (le pilote, pas les cartes). Cartes vues au journal : Bolster (8), Walker's Chopper, Machine Gun, Nuke (attaque), Seeing Red + Spear of Odin (mélangées au deck, Seeing Red défaussée), Battle of the Patriots, Forced Leave, Deflection, Roundhouse, Bouncing Bulwark, Reckless, Convincer, Solid Gear, Shield ; la capacité d'Obstinance (« Spend a [mental] resource ») apparaît au journal d'actes (« Hero_Interrupt », « Spend_a_[mental]_resource »).
- **Restent à vérifier en partie réelle** : une partie complète avec le héros (aucun outil ne la remplace) ; l'affichage de la biographie au survol dans le wizard ; le rendu des deux branches nommées d'Obstinance (« Spend a [mental] resource » / « Spend a [physical] resource ») dans l'interface ; le choix de l'amélioration défaussée par Spear of Odin (AskChooseFace) ; les 10 questions de règle ci-dessous.
- **Modification du moteur / des outils partagés** : AUCUNE en Python. Seule modification de code partagé : `Fusion/marvel-lcg-src/public/js/deckbuilder/regles.js` (clé `classes_interdites`).


### us001a : * U.S. Agent (face HÉROS) — AVENGER. SOLDIER. PV 11, THW 2, ATK 2, DEF 2, main 6.

*Bolster* — **Response** : After you defend, ready an upgrade you control.

- [x] Étape 2 : cartes de référence : `mf006` (AfterUnitDefendEnd), `31022`/`gs232` (ready an upgrade you control : `SetTarget(Upgrade, canbe_ready=True, from_where=["YouControlCards"])`), `01019a` (Response sur face héros).
- [x] Étape 5 : mots-pièges : « After you DEFEND » (pas d'exigence de dégâts) ; « AN upgrade you control » = cible obligatoire, INCLINÉE ; Response nue (optionnelle). Conforme.
- [x] Étape 6 : nombres : PV 11, THW 2, ATK 2, DEF 2, main 6 (cas valeurs imprimées). Conforme.
- [x] Étape 7 : 3 cas sujets. Substitution : **rouges 1/3** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : NON.

**Carte terminée : NON (provisoire)** : partie réelle jouée par un humain (gate du héros), aucune question de règle en suspens.

### us001b : * John Walker (face ALTER EGO) — SOLDIER. PV 11, REC 3, main 6.

*Master of None* — deckbuilding : tous les aspects, ni alliés ni cartes Basic. **Action** : Exhaust John Walker → search your deck and discard pile for the U.S. Agent's Shield upgrade and add it to your hand.

- [x] Étape 2 : cartes de référence : `06001b` Odinson (`Search.PlayerCard(..., include_discard_pile=True)` + `GainCard`) ; règle de deck : `metadata.deckbuilding` (`aspects`, `types_interdits`, clé neuve `classes_interdites`).
- [x] Étape 5 : mots-pièges : « Master of None » = règle d'ÉDITEUR (pas de script) ; « Action » nue = forme alter ego seulement ; l'inclinaison est un COÛT payé même si rien n'est trouvé. Conforme.
- [x] Étape 6 : nombres : PV 11, REC 3, main 6. Conforme. Règle de deck : 6 tests node (aspects libres, Basic et alliés refusés, 2 témoins qui mordent ; mutation vue rouge).
- [x] Étape 7 : 4 cas sujets. Substitution : **rouges 3/4** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : NON.

**Carte terminée : NON (provisoire)** : partie réelle jouée par un humain (gate du héros), aucune question de règle en suspens.

### us002 : Bouncing Bulwark — Event, coût 0, [physical], ATTACK. TACTIC. (x3)

**Hero Action** *(attack)* : Discard U.S. Agent's Shield → deal 4 damage to an enemy. Then, if this attack deals 2 or more excess damage, put U.S. Agent's Shield into play from your discard pile.

- [x] Étape 2 : cartes de référence : `13013` Into the Fray / `28013` No Quarter (`DealDamage(..., if_this_attack_deal_excess_damage=fn)`), `54023`/`bk008` (`PutIntoPlay` depuis la défausse).
- [x] Étape 5 : mots-pièges : « Discard ... → » COÛT (bouclier EN JEU) ; « 2 OR MORE excess » (`>= 2`) ; « put INTO PLAY from discard » (revient en jeu, équipé au héros). Conforme.
- [x] Étape 6 : nombres : 4 dégâts, seuil d'excès 2, coût 0. Conforme (cas excès 0 / 1 / 2 / 3).
- [x] Étape 7 : 5 cas sujets. Substitution : **rouges 4/5** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : OUI (carte d'état / attachement / compteur / bouclier revenu en jeu) : cas plateau `us-agent-plateau.test.ts`, vert d'emblée.

**Carte terminée : NON (provisoire)** : question en suspens : *Le coût « Discard U.S. Agent's Shield → » : d'où se défausse le bouclier ?*
  - A. Seulement EN JEU (recommandé) : la carte est injouable sans bouclier en jeu, comme codé
  - B. Aussi depuis la MAIN : on peut payer en défaussant le bouclier tenu en main (la carte devient jouable sans bouclier en jeu)

### us003 : Deflection — Event, coût 1, [physical], TACTIC. (x2)

**Hero Response** : After an enemy deals 2 or more damage to you, if U.S. Agent's Shield is in play, stun up to 2 minions.

- [x] Étape 2 : cartes de référence : `sh007` Trading Blows (`AfterUnitTookDamage(HeroResponse, "You", op, who_dealt_damage=Enemy).SetPlay()`).
- [x] Étape 5 : mots-pièges : « 2 OR MORE » (`took_damage >= 2`, dégâts réellement subis) ; « an ENEMY » (pas de dégâts directs) ; « UP TO 2 minions » (cibles 0..2, sbires seulement). Conforme.
- [x] Étape 6 : nombres : 2 dégâts, 2 sbires, coût 1. Conforme.
- [x] Étape 7 : 6 cas sujets. Substitution : **rouges 2/6** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : OUI (carte d'état / attachement / compteur / bouclier revenu en jeu) : cas plateau `us-agent-plateau.test.ts`, vert d'emblée.

**Carte terminée : NON (provisoire)** : question en suspens : *« if U.S. Agent's Shield is in play » : condition d'offre ou clause de l'effet ?*
  - A. Condition d'OFFRE (recommandé, codé) : sans bouclier en jeu la Réponse n'est pas proposée (impossible de gaspiller la carte)
  - B. Clause de l'EFFET : la carte est proposée et jouable, mais ne fait rien sans bouclier

### us004 : Reckless — Event, coût 0, [mental], ATTACK. TACTIC. THWART. (x2)

**Hero Action** *(attack/thwart)* : Take X damage → remove X threat from a scheme and deal X damage to an enemy (to a maximum of 4.)

- [x] Étape 2 : cartes de référence : `tm006` Majime (même carte, max 3), `dt028` Pay It Forward.
- [x] Étape 5 : mots-pièges : « X » choisi 0..4 ; « AND » : une manigance ET un ennemi, effets indépendants ; libellé (attack/thwart). Conforme. **Arbitrage du 26/10/2026 (RR Cost)** : « If taking damage is a cost, that cost is not considered paid unless all of that damage was taken » → une prévention, même partielle, annule l'effet en entier (plus de « X réel » à la Majime).
- [x] Étape 6 : nombres : Max 4, coût 0, traits ATTACK TACTIC THWART (lus en main). Conforme.
- [x] Étape 7 : 6 cas sujets (nouveau : « X = 3 mais 1 dégât PRÉVENU (Jessica's Jacket jj010) → coût non payé, aucun effet », vu ROUGE avec l'ancien code : menace 2 / Rhino 2 au lieu de 4 / 0). Substitution : **rouges 4/6** (restent verts sans module : X = 0 et les libellés en main, absence / données).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : NON.

**Carte terminée : NON (provisoire)** : partie réelle jouée par un humain non faite. Question de règle TRANCHÉE (RR Cost, 26/10/2026) : le coût « Take X damage » est payé seulement si TOUS les X dégâts sont subis (`took_damage >= X`) ; sinon l'effet n'a pas lieu. Les cartes cousines `tm006` Majime et `dt028` Pay It Forward gardent la lecture « X réel » : hors périmètre, à reprendre si la même règle s'y applique.

### us005 : Roundhouse — Event, coût 1, [physical], ATTACK. (x2)

**Hero Action** *(attack)* : Deal 2 damage to an enemy. If you paid for this card using a Protection (green) or Justice (yellow) card, confuse that enemy.

- [x] Étape 2 : cartes de référence : `jennika/tj004` (`effect.context.paid_this_res_effects`).
- [x] Étape 5 : mots-pièges : « paid using a Protection or Justice CARD » : la CLASSE de la carte payeuse, pas la couleur ; « that enemy » = la cible des dégâts. Conforme sous réserve de la question.
- [x] Étape 6 : nombres : 2 dégâts, coût 1. Conforme (7 classes payeuses testées).
- [x] Étape 7 : 9 cas sujets. Substitution : **rouges 9/9** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : OUI (carte d'état / attachement / compteur / bouclier revenu en jeu) : cas plateau `us-agent-plateau.test.ts`, vert d'emblée.

**Carte terminée : NON (provisoire)** : question en suspens : *« If you paid for this card using a Protection or Justice card » : combien de cartes payeuses ?*
  - A. AU MOINS UNE carte Protection/Justice parmi celles dépensées (recommandé, codé)
  - B. TOUTES les cartes dépensées doivent être Protection/Justice

### us006 : * Walker's Chopper — Support unique, coût 3, [physical], VEHICLE.

**Alter-Ego Response** : After you exhaust John Walker to recover or search for U.S. Agent's Shield, exhaust Walker's Chopper → change to hero form, then ready U.S. Agent.

- [x] Étape 2 : cartes de référence : `AfterUnitUseBasicPower(.., powers=["REC"])` (friend.py) pour la récupération de BASE ; `AfterCardResolveAbility` (resolve.py) pour l'Action de us001b ; `01025` (`ChangeToOtherIdentityForm`).
- [x] Étape 5 : mots-pièges : « exhaust John Walker TO recover » : récupération de base seulement (piège `AfterUnitMakeRecovery`, qui ignore son drapeau) ; « THEN ready » : on redresse la face héros après le changement. Conforme.
- [x] Étape 6 : nombres : Coût 3, une inclinaison du soutien. Conforme.
- [x] Étape 7 : 5 cas sujets. Substitution : **rouges 2/5** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : OUI (carte d'état / attachement / compteur / bouclier revenu en jeu) : cas plateau `us-agent-plateau.test.ts`, vert d'emblée.

**Carte terminée : NON (provisoire)** : partie réelle jouée par un humain (gate du héros), aucune question de règle en suspens.

### us007 : * Convincer — Upgrade unique, coût 2, [energy], TECH. WEAPON.

Restricted. U.S. Agent gets +1 ATK. Uses (3 charge counters.) **Hero Response** : After you damage a minion with base hit points of 5 or less, exhaust Convincer and remove 1 charge counter from here → stun that minion.

- [x] Étape 2 : cartes de référence : `mf006` (+1 stat), `sh016` Jo (`AfterYouDealDamage` + `CostFunc.Counter`), `ch015`.
- [x] Étape 5 : mots-pièges : « BASE hit points » = PV imprimés (`printed_health`) ; « a MINION » (pas le vilain) ; coût double (incliner ET 1 compteur) ; Uses/Restricted natifs. Conforme.
- [x] Étape 6 : nombres : +1 ATK, 3 compteurs, seuil 5. Conforme (4 PV oui, 8 PV non, dernier compteur → sortie de jeu).
- [x] Étape 7 : 5 cas sujets. Substitution : **rouges 5/5** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : OUI (carte d'état / attachement / compteur / bouclier revenu en jeu) : cas plateau `us-agent-plateau.test.ts`, vert d'emblée.

**Carte terminée : NON (provisoire)** : partie réelle jouée par un humain (gate du héros), aucune question de règle en suspens.

### us008 : Obstinance — Upgrade, coût 1, [mental], CONDITION.

**Hero Interrupt** : When you exhaust to use a basic power but before resolving its effects, exhaust Obstinance and spend 1 [mental] or [physical] resource → ready U.S. Agent.

- [x] Étape 2 : cartes de référence : `ch017` Martial Mastery (`WhenUnitUseBasicPower(HeroInterrupt, Hero, op, powers=[..])`), RECETTES §5 (deux coûts alternatifs = deux capacités).
- [x] Étape 5 : mots-pièges : « basic power » : ATQ, CTR ET DEF ; « [mental] OR [physical] » : deux capacités (icônes lues dans le texte et vérifiées contre Reckless RES=B) ; « exhaust Obstinance AND spend ». Conforme.
- [x] Étape 6 : nombres : 1 ressource. Conforme (Genius, Strength, Hellcat [wild], thwart, défense, 3 témoins).
- [x] Étape 7 : 9 cas sujets. Substitution : **rouges 5/9** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : NON.

**Carte terminée : NON (provisoire)** : partie réelle jouée par un humain (gate du héros), aucune question de règle en suspens.

### us009 : * Solid Gear — Upgrade unique, coût 2, [physical], ARMOR.

**Hero Interrupt** : When an enemy initiates an attack, exhaust Solid Gear → reduce the resource cost of the next Protection (green) card you play this phase by 2.

- [x] Étape 2 : cartes de référence : `19018` Subdue (`WhenUnitWouldAttack`), `01092`/`ch007` (`Worlds.UpdateNextCardPlayCost(.., in_this="Phase")`).
- [x] Étape 5 : mots-pièges : « the NEXT » (une seule carte) ; « Protection card » = classe, tous types ; « this PHASE » ; « by 2 » (-2, plancher 0). Conforme.
- [x] Étape 6 : nombres : Réduction 2, coût 2. Conforme.
- [x] Étape 7 : 5 cas sujets. Substitution : **rouges 2/5** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : NON.

**Carte terminée : NON (provisoire)** : partie réelle jouée par un humain (gate du héros), aucune question de règle en suspens.

### us010 : * U.S. Agent's Machine Gun — Upgrade unique, coût 2, [physical], WEAPON.

Restricted. U.S. Agent gets +1 ATK. Uses (3 ammo counters.) **Hero Response** : After you damage an enemy, remove 1 ammo counter from here → deal 2 damage to each minion engaged with you.

- [x] Étape 2 : cartes de référence : `sh016` Jo, `43014` Rictor / `dt015` (`SetTarget("YourEngagedMinions", range="All")`).
- [x] Étape 5 : mots-pièges : « an ENEMY » (vilain ou sbire) ; « each minion engaged WITH YOU » (pas le vilain) ; coût = 1 compteur (pas d'inclinaison) ; **la garde `pas_sa_propre_rafale` est RETIRÉE (arbitrage du 26/10/2026, RR Response : « once per occurrence »)** : les dégâts de la rafale sont une nouvelle occurrence de « you damage an enemy », la Réponse (facultative) est re-proposée tant qu'il reste des compteurs. Conforme.
- [x] Étape 6 : nombres : +1 ATK, 3 compteurs, 2 dégâts. Conforme.
- [x] Étape 7 : 6 cas sujets (nouveau : « M.O.D.O.K. 8 PV : 3 rafales = 6 dégâts, carte défaussée », vu ROUGE avec la garde : 2 dégâts, carte encore en jeu ; les deux cas à sbire ont été corrigés : Weapons Runner 2 PV meurt de la 1re rafale donc aucune re-proposition, Shocker meurt à la 2e). Substitution : **rouges 6/6**.
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : OUI (carte d'état / attachement / compteur / bouclier revenu en jeu) : cas plateau `us-agent-plateau.test.ts`, vert d'emblée.

**Carte terminée : NON (provisoire)** : partie réelle jouée par un humain non faite. Question de règle TRANCHÉE (26/10/2026) : la rafale re-propose la Réponse. Le pilote du harnais ACCEPTE toujours : un seul coup peut vider les 3 compteurs (autoplay graine 305 : 3 rafales sur Nuke puis carte défaussée, la boucle se termine). Un humain, lui, peut refuser à chaque proposition : à vérifier en partie que la proposition est bien faite à chaque fois et qu'« Annuler » la coupe.

### us011 : * U.S. Agent's Shield — Upgrade unique, coût 1, [physical], ITEM. WEAPON.

Restricted. **Hero Interrupt** : When you are attacked by an enemy, exhaust U.S. Agent's Shield → deal 2 damage to the attacker or prevent 1 damage from this attack.

- [x] Étape 2 : cartes de référence : `05012` Nova (`WhenUnitInitiatesAttackAgainst`), `45040` Magic Barrier (`message.PreventDamage`).
- [x] Étape 5 : mots-pièges : « OR » : une seule des deux branches ; « When YOU are attacked » : pas une attaque contre un allié ; Restricted natif. Conforme.
- [x] Étape 6 : nombres : 2 dégâts / 1 prévenu. Conforme (deux branches, bouclier incliné, attaque d'un allié, 3 Restricted).
- [x] Étape 7 : 5 cas sujets. Substitution : **rouges 2/5** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : NON.

**Carte terminée : NON (provisoire)** : partie réelle jouée par un humain (gate du héros), aucune question de règle en suspens.

### us012 : Forced Leave — Obligation (set U.S. Agent), Boost 1, « Give to the John Walker player ».

Flip to alter-ego form. Choose: • Exhaust John Walker and discard U.S. Agent's Shield → remove this obligation from the game. • Discard 1 card from your hand at random → discard this obligation.

- [x] Étape 2 : cartes de référence : `th011` Annual Shedding (même auteur, bascule SANS « may »), `ch018` Family Ties (deux sorties).
- [x] Étape 5 : mots-pièges : bascule obligatoire ; branche 1 : COÛT (John Walker PRÊT + bouclier en jeu) et sortie « REMOVE from the game » ; branche 2 : défausse AU HASARD et sortie « DISCARD ». Conforme sous réserve.
- [x] Étape 6 : nombres : Boost 1, 1 carte. Conforme.
- [x] Étape 7 : 5 cas sujets. Substitution : **rouges 5/5** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : NON.

**Carte terminée : NON (provisoire)** : question en suspens : *« Exhaust John Walker and discard U.S. Agent's Shield → » : d'où se défausse le bouclier ?*
  - A. Seulement EN JEU (recommandé, codé) : branche non offerte sans bouclier en jeu
  - B. Aussi depuis la MAIN : la branche est offerte avec un bouclier en main

### us013 : * Nuke — Sbire némésis unique (1/5), CYBORG. SOLDIER. SCH 1, ATK 2, PV 5, Boost 1.

**Forced Interrupt** : When Nuke makes an attack against you, discard the top card from your deck. If an Aggression (red) card, or a card with a printed [physical] resource was discarded this way, that attack deals 1 additional damage.

- [x] Étape 2 : cartes de référence : `45129` Velociraptor / `09028` Baron Mordo (`WhenUnitAttackYou` + `DiscardDeckTopCard`), `10026` Abomination (`GetPrintedResources(..).r`).
- [x] Étape 5 : mots-pièges : « Aggression card OR printed [physical] » : un OU sur UNE carte, +1 au plus ; Interruption : joue AVANT la défense ; « against YOU ». Conforme sous réserve.
- [x] Étape 6 : nombres : PV 5, SCH 1, ATK 2, +1 dégât. Conforme.
- [x] Étape 7 : 8 cas sujets. Substitution : **rouges 7/8** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : NON.

**Carte terminée : NON (provisoire)** : question en suspens : *« a card with a printed [physical] resource » : une ressource [wild] imprimée compte-t-elle ?*
  - A. NON (recommandé, codé) : seule l'icône [physical] rouge compte (même lecture qu'Abomination 10026)
  - B. OUI : le [wild] compte aussi (+1 dégât de plus souvent)

### us014 : Battle of the Patriots — Manigance annexe némésis (2/5), menace 4, Acceleration, Boost 2.

Aggression (red), Basic (gray), and Leadership (blue) cards cost 1 additional resource.

- [x] Étape 2 : cartes de référence : `ar010` / `sk280` (`IncreaseResourceCostToPlay`), `01109` Bomb Scare (Acceleration natif).
- [x] Étape 5 : mots-pièges : « cost 1 ADDITIONAL » : +1 au coût de jeu ; trois classes seulement (Protection, Justice, Hero intactes) ; effet continu. Icône du centre = ACCÉLÉRATION (comparée à 01109 ; fiche hazard.md : pointe + barre = Acceleration). Conforme sous réserve.
- [x] Étape 6 : nombres : Menace 4, +1, Boost 2. Conforme.
- [x] Étape 7 : 10 cas sujets. Substitution : **rouges 3/10** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : OUI (carte d'état / attachement / compteur / bouclier revenu en jeu) : cas plateau `us-agent-plateau.test.ts`, vert d'emblée.

**Carte terminée : NON (provisoire)** : question en suspens : *« cards cost 1 additional resource » : pour quels joueurs ?*
  - A. TOUS les joueurs (recommandé, codé) : le texte ne dit pas « you play »
  - B. Seulement le joueur qui affronte la manigance (en multijoueur, les autres ne paient pas plus)

### us015 : Seeing Red — Traîtrise némésis (3/5, 4/5), Boost 1. (x2)

Discard the top 2 cards from your deck. If a card with a printed [physical] resource was discarded this way, take 2 indirect damage.

- [x] Étape 2 : cartes de référence : `ch021` (`WhenThisRevealed`, `DealIndirectDamage`), `10026` (`GetPrintedResources(..).r`).
- [x] Étape 5 : mots-pièges : texte sans « When Revealed » imprimé = effet à la révélation ; « IF a card » : 2 dégâts au total ; « INDIRECT ». Conforme sous réserve.
- [x] Étape 6 : nombres : 2 cartes, 2 dégâts. Conforme.
- [x] Étape 7 : 5 cas sujets. Substitution : **rouges 5/5** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : NON.

**Carte terminée : NON (provisoire)** : question en suspens : *« printed [physical] resource » : une ressource [wild] imprimée compte-t-elle ?*
  - A. NON (recommandé, codé) : seule l'icône [physical] rouge compte
  - B. OUI : le [wild] compte aussi (2 dégâts indirects plus souvent)

### us016 : Spear of Odin — Attachement némésis (5/5), Boost 3.

Attach to the enemy with the most remaining hit points. **Forced Interrupt** : When attached enemy deals damage to your hero, discard an upgrade you control, then discard Spear of Odin.

- [x] Étape 2 : cartes de référence : `04117` / `24039` (`AttachToFaceWhenPutIntoPlay(.., most_remaining_hp=True)`, ici type Enemy), `32178` (`WhenUnitWouldTakeDamage(.., who_deal_damage=...)`).
- [x] Étape 5 : mots-pièges : « enemy » (vilain OU sbire) ; « REMAINING » hit points ; « then discard Spear » même sans amélioration ; « your HERO ». Conforme sous réserve.
- [x] Étape 6 : nombres : Boost 3. Conforme.
- [x] Étape 7 : 6 cas sujets. Substitution : **rouges 5/6** (les cas qui restent verts sans module sont des valeurs imprimées ou des témoins d'absence).
- [x] Étape 7 bis : limite imprimée ? **NON**.
- [x] Étape 8 : autoplay : voir « Résultats des gates lourdes » (journal lu : lignes citées si la carte a été jouée).
- [x] Étape 8 bis : OUI (carte d'état / attachement / compteur / bouclier revenu en jeu) : cas plateau `us-agent-plateau.test.ts`, vert d'emblée.

**Carte terminée : NON (provisoire)** : question en suspens : *« deals damage to your hero » : les dégâts subis par l'ALTER EGO comptent-ils ?*
  - A. NON (recommandé, codé) : seulement quand le joueur est en forme héros
  - B. OUI : l'identité sous n'importe quelle forme (la lance se défausse aussi en alter ego)
