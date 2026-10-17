# TMNT Shinobi Kuji-Kiri (`sj001`-`sj020`) : gabarits PROCESSUS-CARTE (17/10/2026)

Pack `tmnt_shinobi_kuji_kiri` (set 203, « TMNT Shinobi Kuji-Kiri », Inkwire, `desc.Class = "Kuji-Kiri"`). Scans : `Kuji-Kiri/K1..K20`
(`zip-shinobi`). Numérotation figée : `tools/tmnt_shinobi_numerotation.tsv`. Cas : `tools/cas/tmnt_shinobi_kuji_kiri.py` (filtre `[sj]`,
118 cas) ; plateau : `ui-app/src/board/tmnt-shinobi-kuji-kiri-plateau.test.ts` (6 tests). Questions : `shinobi-kuji-kiri-questions.md`.
Classement contre les officielles : **NOUVELLE** pour les 20 (aucune n'est un art alternatif : `sj002` reproduit le TEXTE de `core/01074`
Inspired mais change nom, classe, trait SPELL ; `sj006` = `phoenix/34009` Mind Control à 3 dégâts consécutifs ; `sj013` = `scw/15003` Chaos
Magic + retrait du jeu ; `sj015` = `drs/09035` Vapors of Valtorr ; `sj010`/`sj007` suivent `falcon/53010` Battlefield Awareness ; ce sont
des cartes exclusives, pas des reskins).

Icônes de ressource (jamais à vue, comparées aux coins de `tj002`/`tj005` RES=B, `tj004` RES=R, `tj003` RES=Y, étoile = [wild] comme `tj009`) :
nœuds bleus = B, poing rouge = R, éclair jaune = Y, étoile verte = G. Étoile « ✦ » devant le titre = unique (nom `* ...` dans `cards.json`).
Icône « Y » du texte de `sj007`/`sj010` = l'icône de BOOST (comparée au coin de `01099` Charge) ; l'étoile = l'étoile de boost
(`FacesCounter.CountTotalBoostStarAndBoost`).

**Preuve par substitution** (script jetable, module remplacé par `GetAbilities -> []`, cas relancés, ports 28300-28399) : le nombre de cas
ROUGES sans module est donné carte par carte ; les cas qui restent VERTS sans module sont des témoins d'ABSENCE (« injouable en alter ego »,
« non proposée », « sans la carte, valeur imprimée »), des données (unicité `✦`, `MaxPerDeck`) ou des cas du moteur : assumé, listé.
**Étape 8 (autoplay ciblé)** : voir le bloc commun en fin de fichier.

### sj001 : Foresight (Événement SPELL, 1, B)
- [x] Étape 2 : `agent_13/ag004` Infiltrate (`LookAtDeck("EncounterDeck", 1)` + `MayChooseOneAbility`), `aos/50023` ; révéler le dessus : `Worlds.RevealEncounterDeckTopCard`.
- [x] Étape 5 : « You MAY reveal » (facultatif, `Cancel`) ; « reveal that card TO draw 3 » (révélation d'abord, pioche ensuite) ; Hero Action. Homonymes `mw009`, `vp008` : textes et types différents (confirmé sur scan).
- [x] Étape 6 : coût 1, pioche 3 : conforme (`desc` et script).
- [x] Étape 7 : 4 cas (révélée : Shocker en jeu, 1 dégât, main 3 ; déclinée ; c'est bien le dessus ; alter ego injouable). Rouges sans module : 3/4 ; vert : alter ego (absence).
- [x] Étape 7 bis : limite imprimée ? NON.  - [x] Étape 8 bis : NON (une carte révélée est déjà dessinée par le moteur).
Carte terminée : **OUI**.

### sj002 : Imbued Weapons (Amélioration SPELL, 1, R)
- [x] Étape 2 : `core/01074` Inspired (texte identique ; `CanPlayThisUpgradeCard(Ally)` + `GiveKeywordToAttached(Ally, thwart=1, attack=1)`).
- [x] Étape 5 : « an ally » (tout allié) ; +1 THW ET +1 ATK ; « Max 1 per ally » = `desc.MaxPerUnit "1"`. Étape 6 : 1, +1, +1 conformes.
- [x] Étape 7 : 5 cas (+1/+1 mesurés, témoin sans carte, pas de PV/DEF en plus, Max 1 per ally refusé / témoin accepté). Rouges sans module : 2/5 ; verts : témoin et « pas de PV » (absences), témoin positif Max.
- [x] Étape 7 bis : limite imprimée OUI (« Max 1 per ally ») : témoin d'épuisement = 2e copie injouable sur l'allié déjà équipé (cas rouge sans module).
- [x] Étape 8 bis : OUI (attachée à un allié) : `tmnt-shinobi-kuji-kiri-plateau.test.ts`, vert d'emblée (correctif générique d'attachement déjà en place), témoin négatif.
Carte terminée : **OUI**.

### sj003 : Yang (Événement ATTACK SPELL, 2, R)
- [x] Étape 2 : `jennika/tj004` Decisive Strike (dégâts directs, label attack), `donatello/td005` (`ChooseAbilities`).
- [x] Étape 5 : « Deal 2 damage » direct (ATQ du héros non ajoutée, cas dédié) ; « Choose » : UNE option après les dégâts ; « Stun AN enemy » (autre ennemi possible) ; « a FRIENDLY character ». Étape 6 : 2 conforme.
- [x] Étape 7 : 5 cas. Rouges sans module : 4/5 ; vert : alter ego (absence).  - [x] 7 bis : NON.  - [x] 8 bis : NON (statut : badge déjà couvert).
Carte terminée : **OUI**.

### sj004 : Yin (Événement SPELL, 2, Y)
- [x] Étape 2 : `cloak_dagger/cd004`, `lockjaw/lj024` (soin sur un personnage ami), `donatello/td005` (choix, Cloak), `ShinobiCloak`. Fiches `cloak.md`, `cloaked.md`.
- [x] Étape 5 : soin de 2 plafonné ; « Choose » : UNE option ; « Cloak A friendly character » (un seul, allié possible) ; « Confuse AN enemy ». Étape 6 : 2 conforme.
- [x] Étape 7 : 5 cas. Rouges sans module : 4/5 ; vert : alter ego.  - [x] 7 bis : NON.  - [x] 8 bis : NON (badge Camouflé déjà couvert).
Carte terminée : **OUI**.

### sj005 : Tai Chi (Ressource, générée [wild], G)
- [x] Étape 2 : `aos/maria_hill/50007`, `angel/42008` (`AfterYouSpendThisCard(..., to_pay_card=)`), `mut_gen/32018` (`MaxPerDeck "2"`).
- [x] Étape 5 : « ON A SPELL CARD » (tout type SPELL) ; « draw 1 » ; « Max 2 per deck » (donnée). Étape 6 : 2, 1 conformes.
- [x] Étape 7 : 4 cas (événement SPELL, amélioration SPELL, non-SPELL, SPELL payée autrement). Rouges sans module : 2/4 ; verts : non-SPELL et « autre ressource » (absences).
- [x] Étape 7 bis : « Max 2 per deck » : limite de CONSTRUCTION (donnée `MaxPerDeck`, lue par le deck-builder), pas de témoin de partie.  - [x] 8 bis : NON.
Carte terminée : **OUI**.

### sj006 : Enthrall (Amélioration CONDITION SPELL, 3, B)
- [x] Étape 2 : `phoenix/34009` Mind Control (même texte à 1 dégât consécutif près), `rogue/38011`, `bp/51036`. EXTENSION DE DONNÉES : gabarit `enthrall_controlled_ally` (`ATK "0***"`, `THW "0***"`, CONTROLLED).
- [x] Étape 5 : « non-ELITE » ; « THW equal to its printed SCH » ; « 3 consequential damage after it thwarts OR attacks » (deux cas) ; « blank textbox » (cas + témoin). Étape 6 : 3 (dégâts), coût 3 conformes.
- [x] Étape 7 : 8 cas (allié contrôlé THW 1/ATQ 2/PV 3/3 conséq. ; texte vide + témoin ; attaque : 2 dégâts puis allié vaincu ; contre : 1 menace puis allié vaincu ; ELITE refusé / témoin ; quitte le jeu : redevient sbire). Rouges sans module : 5/8 ; verts : témoin blank, témoin positif, retour en sbire.
- [x] Étape 7 bis : NON.  - [x] Étape 8 bis : OUI (allié contrôlé + Enthrall) : plateau, vert d'emblée, dit clairement.
Carte terminée : **OUI**.

### sj007 : ✦ Ring of Protection (Amélioration SPELL, 1, R)
- [x] Étape 2 : `drs/09007` (`WhenPlayerRevealCard` + `CancelAllEffectsAndDiscardIt`), `falcon/53010` (icônes [star] et [boost]), `scw/15008` (coût `Discard("This")`). Fiche `boost.md`.
- [x] Étape 5 : « a treachery is revealed » SANS « from the encounter deck » (toute révélation, `from_encounter` laissé à None) ; « discard THIS card → » (coût) ; « cancel ALL effects and discard it » ; icônes de la traîtrise annulée, deck du joueur. Étape 6 : 1 conforme.
- [x] Étape 7 : 7 cas (1 icône, 2 icônes, ÉTOILE seule, 0 icône ; témoin sans Ring ; sbire non annulé ; alter ego). Rouges sans module : 4/7 ; verts : témoin, sbire non annulé, alter ego.
- [x] Étape 7 bis : NON (unique ✦ : donnée).  - [x] 8 bis : NON.  Non prouvé : révélation par un AUTRE joueur (« AnyPlayer »).
Carte terminée : **OUI**.

### sj008 : ✦ Toshokan Arcana (Soutien LOCATION, 3, Y)
- [x] Étape 2 : `ant/12015` Call for Aid (`DiscardDeckUntil` + `GainCard`), `CostFunc.Exhaust("This")`.
- [x] Étape 5 : « Action » (les deux formes, cas alter ego) ; « until you discard a SPELL » (première SPELL, tout type, cartes sautées défaussées) ; ajoutée à la main. Étape 6 : 3 conforme.
- [x] Étape 7 : 7 cas (jusqu'à la SPELL ; première seulement ; amélioration SPELL ; alter ego ; épuisement ; positif ; deck sans SPELL). Rouges sans module : 7/7.
- [x] Étape 7 bis : OUI (inclinaison) : témoin d'épuisement 0 action après usage.  - [x] 8 bis : NON.  Note : un deck qui se vide pendant la défausse suit la règle du deck vide (le deck est remélangé).
Carte terminée : **OUI**.

### sj009 : ✦ Armageddon (Complot annexe JOUEUR, 0, B, Victory 0, menace 5 par héros)
- [x] Étape 2 : `jj/61020` Run Them to Ground (`DealEncounterCards(1)` à chaque joueur), `next_evol/40006` (`works_in_the_victory_display=True`), `drs/09026` (cible `Hero`), `deadpool/44024`. Fiche `victory.md`.
- [x] Étape 5 : « EACH player » ; « After it ENTERS PLAY » (Réponse obligatoire) ; « While in the victory display » (pas tant qu'en jeu) ; « EACH identity » (les deux joueurs) ; « IN HERO FORM ». Étape 6 : 0, 1 carte, +1, menace « 5* » = 5 par héros (5 solo, 10 à deux) conformes.
- [x] Étape 7 : 7 cas (solo ; deux joueurs ; en jeu : +0 ; victoire : deux héros +1 ; alter ego +0 ; témoin sans carte ; vaincue → pile de victoire). Rouges sans module : 5/7 ; verts : les deux témoins « +0 ».
- [x] Étape 7 bis : NON.  - [x] 8 bis : NON (la pile de victoire et la menace par héros sont déjà dessinées).  Note : `Puzzle.MoveTo(.., 'VictoryDisplay')` n'enregistre PAS l'effet de la pile (carte jamais jouée) : les cas passent par jouer puis vaincre.
Carte terminée : **OUI**.

### sj010 : Flash Ward (Événement DEFENSE SPELL, 1, R)
- [x] Étape 2 : `falcon/53010` (coût `DiscardDeckTopCards("EncounterDeck", N)` + `CountTotalBoostStarAndBoost`), `nova/28003`, `determination/dt046` (`WhenUnitWouldTakeDamage` sur `Friend`, label defense).
- [x] Étape 5 : « would take damage » (tout dégât) ; « FRIENDLY character » (héros ou allié) ; « discard the top 2 ... → » (coût) ; « 1 per icon IN EACH of the discarded card's boost areas » (total des deux). Étape 6 : 2 cartes, 1 par icône conformes.
- [x] Étape 7 : 6 cas (1+1 ; étoile ; plafonné par les dégâts ; 0 icône : coût payé, rien empêché ; allié protégé ; témoin ennemi). Rouges sans module : 5/6 ; vert : témoin ennemi.
- [x] Étape 7 bis : NON.  - [x] 8 bis : NON.  Non prouvé : deck de rencontre de moins de 2 cartes (comportement moteur préexistant, voir questions).
Carte terminée : **OUI**.

### sj011 : Unravel (Événement ATTACK SPELL THWART, 2, Y)
- [x] Étape 2 : `gam/18020` Hit and Run (`SetTarget(Enemy)` + `SetTarget2(Scheme2)`, labels attack/thwart) ; coûts `DiscardDeckTopCards("YourDeck", 3)` + `("EncounterDeck", 3)`.
- [x] Étape 5 : les DEUX défausses sont le coût ; deux cibles distinctes (ennemi, manigance, y compris annexe). Étape 6 : 3, 3, 3, 3 conformes.
- [x] Étape 7 : 3 cas (principal : decks 5→2 et 6→3, 3 dégâts, menace 5→2 ; sbire vaincu + manigance annexe ; alter ego). Rouges sans module : 2/3.  - [x] 7 bis : NON.  - [x] 8 bis : NON.
Carte terminée : **OUI**.

### sj012 : ✦ A Thin Place (Soutien LOCATION MYSTIC, 0, B)
- [x] Étape 2 : `thor/06017` Hall of Heroes (Alter-Ego Action : inclinaison + 3 compteurs → piocher), `skrull_menace/sk009` (`AfterPlayerPlayedCard(from_hand=True)`), `jennika/tj011` ; `CarteShinobi("Kuji-Kiri")`. Fiche `shinobi.md`.
- [x] Étape 5 : « Alter-Ego Action » ; cout = incliner ET 3 compteurs ; « draw 2 AND heal 2 » ; « Kuji-Kiri card FROM YOUR HAND » (classe, pas trait) ; coût : incliner ; « here ». Étape 6 : 3, 2, 2, 1 conformes.
- [x] Étape 7 : 9 cas (Réponse ; non Kuji-Kiri ; épuisement ; Réponse en alter ego ; action : 0 compteur / main 2 / dégâts 3→1 ; 2 compteurs refusé ; positif ; forme héros refusée ; déjà incliné refusé). Rouges sans module : 5/9 ; verts : absences/ témoin.
- [x] 7 bis : OUI (inclinaison) : 2e carte Kuji-Kiri du round : toujours 1 compteur.  - [x] 8 bis : OUI (compteurs mystiques) : plateau lu (3 « mystique »), témoin sans compteur.
Carte terminée : **OUI**.

### sj013 : ✦ Kirby's Pencil (Amélioration ARTIFACT, 0, B)
- [x] Étape 2 : `scw/15003` Chaos Magic (`PlayCardsLikeInTurn(ignore_resources_cost=True, after_play=...)`), `mut_gen/32179` (`Faces.RemoveAllFromGame`).
- [x] Étape 5 : « FROM YOUR HAND » ; « ignoring its resource cost » ; « PRINTED resource cost » (cas 1, 3, 0) ; « THEN remove THIS card from the game » (zone des cartes retirées, jamais la défausse). Étape 6 : 0 conforme.
- [x] Étape 7 : 6 cas (coût 1, coût 3, coût 0 ; témoin sans Crayon ; alter ego : pas d'action ; plus de 2e usage). Rouges sans module : 4/6 ; verts : témoin sans Crayon, alter ego.
- [x] 7 bis : NON ; usage unique (cas).  - [x] 8 bis : NON (la carte quitte la partie).
Carte terminée : **OUI**.

### sj014 : ✦ Kuji-Kaijū (Amélioration SPELL TITLE, 1, Y)
- [x] Étape 2 : `cap/03031` Enraged (`attack_consequential_damage=1`), `cyclops/33035` Honorary X-Men (trait gagné), `ant/12018` (`health=2`), sélecteur `"YourAlly"`.
- [x] Étape 5 : « an ally YOU CONTROL » (allié d'un autre joueur refusé) ; FERAL ET GIANT ; +2 PV ET +2 ATQ, pas de THW ; « +1 consequential after it ATTACKS » seulement (pas après un contre ; 0+1 = 1 pour un allié sans icône, comme `03031`). Étape 6 : 2, 2, 1 conformes.
- [x] Étape 7 : 9 cas. Rouges sans module : 4/9 ; verts : témoins sans la carte, « contre » (absence de bonus), unicité (donnée), témoin positif.
- [x] 7 bis : NON (unicité ✦ : donnée).  - [x] 8 bis : OUI (attachée à un allié) : plateau vert d'emblée.
Carte terminée : **OUI**.

### sj015 : Morphic Charm (Événement SPELL, 0, B)
- [x] Étape 2 : `drs/invocation/09035` Vapors of Valtorr (même phrase). EXTENSION MOTEUR : `Player.DeclareStatusCard` (`player_ask.py`) + 4 paramètres optionnels (`exposed`, `cloaked`, `dazed`, `intensified`, défaut False : 09035, 15004, 50020 inchangés). Fiches `cloaked.md`, `dazed.md`, `intensified.md`, `exposed.md`.
- [x] Étape 5 : « a minion OR ALLY with a status card » ; « THAT status card » (genre désigné) ; « DIFFERENT » (jamais le même genre : Exposed et Coriace testés) ; plafonds respectés ; « → draw 1 » après le remplacement. Étape 6 : 0, 1 conformes.
- [x] Étape 7 : 8 cas. Rouges sans module : 6/8 ; verts : héros non cible (absence), alter ego.
- [x] 7 bis : NON.  - [x] 8 bis : NON (badge d'état déjà couvert).  Non prouvé : remplacement sur un personnage portant Intensified (la défausse est alors redirigée par Intensified, règle de la carte d'état).
Carte terminée : **OUI**.

### sj016 : QNA Restoration (Événement SPELL, 1, R)
- [x] Étape 2 : `gmw/the_market/16176` (`SetTarget("Players")`, `MayChooseOneAbility` sur sa défausse), `sm/ghost_spider/27008` (`ShuffleAllTo`), `HealthUnits`.
- [x] Étape 5 : « THAT player's identity » ; « THAT player MAY ... THEIR discard pile » mélangée dans SON deck. Étape 6 : 2, 1 conformes.
- [x] Étape 7 : 5 cas (soin 4→2 + mélange ; Cancel ; soin plafonné ; AUTRE joueur : son identité, sa défausse, son deck, joueur 1 intact ; alter ego). Rouges sans module : 4/5.
- [x] 7 bis : NON.  - [x] 8 bis : NON.
Carte terminée : **OUI**.

### sj017 : ✦ Yi (Allié MYSTIC NINJA TURTLE, 3, G, PV 3, ATK 1*, THW 1*)
- [x] Étape 2 : `aos/50023` Melinda May (`AfterUnitUseBasicPower`), `leonardo/tl002` Splinter / `gmw/16033` (cible défausse → dessus du deck). Stats « 1* » : une icône conséquentielle chacune, comme tous les alliés TMNT de l'auteur ; le [star] du texte est l'icône étoile (aucun code).
- [x] Étape 5 : « uses A BASIC POWER » (ATQ ou CTR testés) ; seulement Yi ; « SPELL OR TECH » (`traits=[...]`) ; « TOP of your deck » sans mélange. Étape 6 : 3, 3, 1*, 1* conformes.
- [x] Étape 7 : 5 cas. Rouges sans module : 3/5 ; verts : aucune cible, autre allié (absences).  - [x] 7 bis : NON.  - [x] 8 bis : NON (carte posée sur le deck : pile déjà dessinée).
Carte terminée : **OUI**.

### sj018 : ✦ Wu Jen Tessen (Amélioration MYSTIC WEAPON, 2, Y, Restricted)
- [x] Étape 2 : `skrull_menace/sk009` (`from_hand=True`), `jennika/tj006` (`ReadyAll`), `up003`. Fiche `restricted.md` (`desc.Restricted "1"`, base automatique).
- [x] Étape 5 : « Hero Response » ; « KUJI-KIRI card FROM YOUR HAND » (Dual comprises, Tessen elle-même : sa propre entrée en jeu déclenche sa Réponse, cas dédié) ; coût : s'incliner ; « ready YOUR HERO ». Étape 6 : 2, Restricted 1 conformes.
- [x] Étape 7 : 5 cas. Rouges sans module : 3/5 ; verts : non Kuji-Kiri, alter ego.
- [x] 7 bis : OUI (inclinaison) : 2e carte Kuji-Kiri : héros re-épuisé reste épuisé (cas rouge sans module).  - [x] 8 bis : NON.
Carte terminée : **OUI**.

### sj019 : Static Shock (Événement ATTACK SPELL, 1*, Y)
- [x] Étape 2 : `tmnt_aspect_aggression/ua015` Demolish (`CostFunc.Rampage(X)`), `rainy/ra005` Lightning Strike (`Worlds.FindCardsOnField(card_type=Enemy, engaged_with=...)`). Fiche `rampage.md`.
- [x] Étape 5 : Rampage 1 en coût (dégât empêché = non joué, cas Coriace) ; « 3 damage to AN enemy » puis « 1 to EACH enemy ENGAGED WITH YOU » (sbires engagés avec vous ; sbire d'un autre joueur épargné ; sbire vaincu n'en reçoit pas plus). Le vilain n'est pas « engagé » au sens du moteur (précédents `ra005`, `dt036`). Étape 6 : 1, 1, 3, 1 conformes.
- [x] Étape 7 : 5 cas. Rouges sans module : 3/5 ; verts : Rampage impayable (le coût est du moteur), alter ego.
- [x] 7 bis : NON.  - [x] 8 bis : NON.
Carte terminée : **OUI**.

### sj020 : Æthreal Shift (Événement DEFENSE SPELL THWART, 3, R) : LECTURE PROVISOIRE
- [x] Étape 2 : `tmnt_aspect_protection/up004` Autodefenestration (`WhenUnitWouldTakeDamage(..., is_from_attack=True)` + `PreventDamage("All")`), `determination/dt046` (menace retirée par choix de manigance).
- [ ] Étape 5 : scan « Hero ACTION » devant « When your hero would take damage » : coquille probable (Q-K1). Implémenté : Hero INTERRUPT. Le reste (« from an attack », « all of that damage », « threat equal to the damage prevented this way ») est conforme.
- [x] Étape 6 : 3 (coût) conforme.
- [x] Étape 7 : 5 cas (2 dégâts empêchés + 2 menaces ; témoin sans carte ; menace plafonnée ; dégâts directs ne déclenchent pas ; manigance annexe choisie). Rouges sans module : 3/5 ; verts : témoin et dégâts directs.
- [x] 7 bis : NON.  - [x] 8 bis : NON.
Carte terminée : **NON** : attend Q-K1 (Hero Action ou Hero Interrupt). Comportement prouvé pour la lecture Interruption.

## Étape 8 commune (autoplay ciblé)
Deck de test `/tmp/.../scratchpad/w/deck_kuji.json` : Spider-Man + Voie Onmyōdō (`se002`) + les 20 cartes Kuji-Kiri (sauf Tai Chi en excès), 8 parties contre Rhino
(`tools/autoplay.py`, port 28310, profil équilibre). Résultat : voir le rapport final (cartes jouées au journal : Reveal that card to draw 3 cards, Cloak a friendly character,
Shuffle a card from your discard pile, Look at the top 2 cards...).

Résultat Étape 8 (17/10/2026) : 8 parties `tools/autoplay.py` contre Rhino (normal, profil équilibre, port 28310), deck Spider-Man + Voie Onmyōdō + Kuji-Kiri :
0 victoire, 7 défaites, 1 minuteur ; le témoin `spider_man` (4 parties) fait 0 victoire aussi. Grep des tracebacks (NameError, AttributeError, TypeError, KeyError,
AssertionError) sur les 5 journaux conservés : 0. Actes vus au journal : Reveal that card to draw 3 cards, Cloak a friendly character, Stun an enemy, Shuffle a card from
your discard pile into your deck, Remove threat ... equal to the damage prevented (sj020), p_confused (sj015), Look at the top 2 cards (Insight). Les journaux des 3 autres
parties n'ont pas été conservés (non relus ligne à ligne) ; le taux de victoire ne dit rien sur les cartes.
