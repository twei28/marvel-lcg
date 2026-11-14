# Hepzibah (Starjammers, Phenexian et Mysteltainn) : gabarits PROCESSUS-CARTE, 26/10/2026

Pack `hepzibah` (préfixe `hz`, set 225). Scripts : `src/cards/pack/hepzibah/{hepzibah,hepzibah_nemesis}/`. Cas : `tools/cas/hepzibah.py`
(52 cas `[hz]`) ; plateau : `ui-app/src/board/hepzibah-plateau.test.ts` ; règle de deck : `tools/tests-lanceur/regles-hepzibah.test.mjs` (5 tests) ;
deck de départ `deck/starter/hepzibah.json` (aucune decklist imprimée : `player_deck` vide) ; recettes `RECETTES-MOTEUR.md` §31 ; fiches
`mots-cles/special.md`, `indirect-damage.md` (nouvelle), `all-purpose-counter.md`, `uses.md`, `quickstrike.md`.

**Aucune carte n'est « terminée »** : il manque la partie réelle jouée par un humain (voir la fin), et plusieurs cartes portent une question de
règle en suspens (choix provisoire codé, consigne utilisateur du 25/10/2026 : les questions sont gardées pour la fin).

Lecture de la substitution (`substituer_pack.py hz0`) : **16/16 modules** ont au moins un cas qui tombe au ROUGE quand le module est remplacé par un
stub ; pack identique avant/après (md5 `e3b1d5a0…`). Les cas qui restent verts sans module sont, carte par carte : des **valeurs imprimées**, des
**contre-cas d'absence d'effet** ou des **témoins** (assumés ci-dessous, jamais maquillés).
Autoplay : 8 parties Hepzibah contre Rhino (0 victoire, 0 blocage : deck de joueur vide, 5 « manigance accomplie », 3 « tous éliminés »), témoin `spider_man` 8 parties (0 victoire, 0 blocage), 0 exception dans les 16 journaux ; les 15 modules du set apparaissent dans les journaux (Special résolu 22 fois).
Passe des decks : 167/167 decks du jeu montent une partie (passe complète, fichiers partagés touchés), dont `hepzibah` (« identité hz001a, main 6, deck 9 »).

---
### hz001a : Hepzibah (face héros)

- [x] Étape 2 : cartes de référence : `zeus/ze002` Hera (choisir une carte EN MAIN qui IMPRIME un Special, `APrintedSpecial`/`ResoudreLeSpecialDe`) ; `56033` Hulk Shape (`AfterPlayerPlayedCard(.., Event, ..)`).
- [x] Étape 5 : mots-pièges : « after you play an **event** » (pas toute carte) ; « a card in your hand » (le joueur choisit, y compris une carte non événement qui imprime un Special) ; filtre « au moins une candidate » dans `conditions`.
- [x] Étape 6 : nombres texte ↔ code : PV 10, ATQ 2, CTR 1, DÉF 2, TM 5 (scan) = cas de valeurs imprimées (ATQ : 2 dégâts à Rhino ; CTR : 1 menace). Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : Special de Feral Rage résolu après Keen Senses (+1 ATQ) ; contre-cas sans Special en main. Substitution : rouges 1/4 (verts : 2 valeurs imprimées, le contre-cas).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI/NON : NON (la carte n'ajoute rien à l'écran)
Carte terminée : NON (provisoire) : partie réelle humaine ; Q1 : le Special est-il choisi par le joueur même s'il n'y a qu'une candidate ?


### hz001b : Hepzibah (face alter ego)

- [x] Étape 2 : cartes de référence : `01019a` (`AfterUnitChangeForm(.., to_this_form=True)`), `40044` (`Faces.MoveAllTo`), `Faces.MoveAllToDeck(.., "Bottom", ..)`. Règle de deck : `maria_hill.json` (`hors_aspect`).
- [x] Étape 5 : mots-pièges : « **2** events » (s'il n'y en a qu'un, on place celui-la) ; « on the **bottom** of your deck » ; « Weapons Officer » = règle de DECKBUILDER (quota de 3 cartes [[WEAPON]] d'autres aspects, pas un effet de jeu).
- [x] Étape 6 : nombres texte ↔ code : PV 10, REC 3, TM 6 (scan) : cas de valeurs imprimées (PV + trait OUTLAW). Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : 2 événements -> sous le deck (deck 2 -> 4) ; 1 événement -> seul celui-là ; contre-cas sans événement ; règle de deck : 5 tests node, calibrée en retirant `metadata.deckbuilding` (le deck de 3 armes passe de légal à refusé). Substitution : rouges 2/4 (verts : valeurs imprimées, contre-cas).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
Carte terminée : NON (provisoire) : partie réelle humaine ; Q2 : l'ordre des deux événements sous le deck (le joueur choisit, le 1er choisi est placé en premier).


### hz002 : Corsair (allié, Christopher Summers)

- [x] Étape 2 : cartes de référence : `50002` Nick Fury (`AfterUnitUseBasicPower(.., "This", ..)`), `zeus/ze002` pour le Special en main.
- [x] Étape 5 : mots-pièges : « **Hero** Response » : sous-type dédié (`AbilityType.HeroResponse`), donc seulement en forme héros ; « uses a basic power » (attaque ET menée) ; ATQ 2*, CTR 2*.
- [x] Étape 6 : nombres texte ↔ code : Coût 3, PV 3 (scan) ; ATQ 2 (2 dégâts à Rhino dans le cas). Icône de ressource : joker (étoile verte), lue à l'œil. Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : Attaque d'allié -> +1 ATQ (Feral Rage) ; Special de Feline Grace (héros incliné -> redressé) ; CONTRE-CAS alter ego (la Hero Response n'est pas offerte). Substitution : rouges 2/4 (verts : valeurs imprimées, contre-cas alter ego).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
Carte terminée : NON (provisoire) : partie réelle humaine ; Q3 : défendre compte-t-il comme « utiliser un pouvoir de base » ? (non codé : attaque et menée seulement).


### hz003 : Targeting Goggles

- [x] Étape 2 : cartes de référence : `ok001b` (`Search.PlayerCard` + `GainCard`), `40044` (`MoveAllTo(.., player_deck)` = sur le dessus), `14022` (Hero Action d'amélioration).
- [x] Étape 5 : mots-pièges : « search your deck for an **event** » ; « **Then** place 1 card from your hand on **top** » (la carte peut être celle qu'on vient de chercher).
- [x] Étape 6 : nombres texte ↔ code : Coût 1, ressource mentale (bleue, lue à l'œil), traits ITEM TECH. Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : main vide : l'événement cherché revient sur le dessus (main 0, deck inchangé) ; main à 1 carte : taille de main inchangée ; **« Then » (26/10/2026) : aucun événement dans le deck → RIEN n'est remis sur le dessus (main 1 et deck 3 inchangés)**, vu ROUGE avant le correctif (deck 4, main 0), vert après. Substitution : rouges 3/3.
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
**Q4 TRANCHÉE le 26/10/2026 (RR « Then » : si le texte avant « then » ne se résout pas entièrement, celui d'après n'est pas tenté)** : sans événement trouvé, on ne remet rien. `hz003.py` corrigé (`if not face: return`).
Carte terminée : NON (provisoire) : partie réelle humaine non faite.


### hz004 : Hepzibah's Spacesuit

- [x] Étape 2 : cartes de référence : `48005` Prehensile Tail (même paire `GiveKeywordToAttached(.., control_additional_restricted=..)` + `CanGenerateResources(.., for_card=Event)`), `20001a` Venom.
- [x] Étape 5 : mots-pièges : « 1 **additional** upgrade that has restricted » (donc 3 au total) ; « Hero Resource » (= `AbilityType.HeroResource`, héros seulement) ; « [wild] for an **event** » seulement.
- [x] Étape 6 : nombres texte ↔ code : Coût 2, ressource énergie (jaune, lue à l'œil), traits ARMOR TECH. Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : paie Keen Senses seule ; CONTRE-CAS : ne paie pas une amélioration ; 3 Restricted légaux avec elle ; CONTRE-CAS sans elle, une des trois sort du jeu. Substitution : rouges 2/4 (verts : les deux contre-cas).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
Carte terminée : NON (provisoire) : partie réelle humaine ; aucune


### hz005 : Energy Blaster

- [x] Étape 2 : cartes de référence : `us007` (`desc.Uses = "3,charge"` + `CostFunc.Counter`), `16005` Root Stomp (`DealDamage(.., if_this_attack_defeats=..)`).
- [x] Étape 5 : mots-pièges : « **Hero Action** » ; « Exhaust **and** remove 1 charge counter » (deux coûts) ; « If this **action** defeats that enemy » ; Restricted et Uses = bases automatiques (pas de script).
- [x] Étape 6 : nombres texte ↔ code : Coût 1, énergie, Restricted 1, Uses 3 charge ; 1 dégât ; compteurs 3 -> 2. Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : 1 dégât + compteur ; Special de Feral Rage si l'ennemi est vaincu ; CONTRE-CAS non vaincu ; TÉMOIN D'ÉPUISEMENT (dernier compteur -> carte défaussée, l'action a quand même lieu). **Q5 MESURÉE le 26/10/2026** : deux cas sur le MÉCHANT, Rhino à 1 PV : l'action le vainc (étape vaincue, RR « Villain Defeat ») → le Special part, +1 ATQ ; Rhino à 2 PV : pas vaincu → ATQ imprimée. Verts d'emblée (le moteur compte bien l'étape vaincue) ; sous module vidé tout rougit. Substitution : rouges 6/6 (les 4 cas d'avant + les 2 du méchant).
- [x] Étape 7 bis : limite imprimée ? OUI : « Uses (3) » est un compteur, pas une limite par tour : témoin = le dernier compteur retiré -> la carte quitte le jeu (`hors_jeu` + `defausse`).
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
Carte terminée : NON (provisoire) : partie réelle humaine non faite.


### hz006 : Heavy Machine Gun

- [x] Étape 2 : cartes de référence : `01022` Ground Stomp (`SetTarget(Enemy, range="All")`), `us007` (`Uses`).
- [x] Étape 5 : mots-pièges : « **each** enemy » (méchant ET sbires) ; Exhaust + 1 compteur de munitions ; Uses 2.
- [x] Étape 6 : nombres texte ↔ code : Coût 2, physique (rouge, lue à l'œil), Restricted 1, Uses 2 ammo ; 1 dégât à chacun. Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : Rhino + Hydra Mercenary (1 dégât chacun, compteur 2 -> 1) ; TÉMOIN D'ÉPUISEMENT (dernier compteur -> défaussée). Substitution : rouges 2/3 (le 3e cas du filtre est celui des trois Restricted de hz004, qui nomme `hz006` : vert sans module, `Restricted` vient de `desc`).
- [x] Étape 7 bis : limite imprimée ? OUI : témoin du dernier compteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
Carte terminée : NON (provisoire) : partie réelle humaine ; aucune


### hz007 : Feral Rage (x3)

- [x] Étape 2 : cartes de référence : `10002` Crushing Blow (`DealDamage(.., hero.attack, ..)`), `14022` (`GainUntilPhaseEnd(effect, attack=1)`), `ze003` (Special nommé, `.NoOutOfPlayLimit()`).
- [x] Étape 5 : mots-pièges : « damage **equal to your ATK** » (ATQ courante, bonus compris) ; Special : « +1 ATK **until the end of the player phase** » (`GainUntilPhaseEnd(.., end_phase="Player")` depuis le 26/10/2026 : résolu en phase du méchant, le bonus tient jusqu'à la fin de la phase des joueurs SUIVANTE).
- [x] Étape 6 : nombres texte ↔ code : Coût 1, physique, traits ATTACK SKILL ; 2 dégâts (ATQ 2). Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : attaque (2 dégâts à Rhino) ; Special résolu depuis la main via Keen Senses (+1 ATQ) ; **Special résolu en PHASE DU MÉCHANT (`Puzzle.BeginVillainPhase`, `ResolveSpecial`, `EndVillainPhase`) : le +1 ATQ TIENT après la phase du méchant** (vu ROUGE avant le correctif : ATQ 2 au lieu de 3), et **TÉMOIN : il tombe à la fin de la phase des joueurs suivante** (la durée mord). Substitution : rouges 3/4 (le témoin d'expiration reste vert sans module).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
**Q6 TRANCHÉE le 26/10/2026 (RR « Lasting Effects »)** : la durée imprimée est « la fin de la phase des joueurs », même si le Special se résout pendant la phase du méchant. Corrigé.
Carte terminée : NON (provisoire) : partie réelle humaine non faite.


### hz008 : Keen Senses (x3)

- [x] Étape 2 : cartes de référence : `01023` Legal Practice (`RemoveThreatFromSchemes`, `SetTarget(Scheme2)`), `01024` (`Faces.ReadyAll`), `ze003`.
- [x] Étape 5 : mots-pièges : « **last** threat » (avant > 0 et après == 0) ; « ready Hepzibah » ; Special : 1 menace d'une manigance au choix.
- [x] Étape 6 : nombres texte ↔ code : Coût 1, mentale (bleue), traits SKILL THWART ; 2 menaces (5 -> 3). Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : 5 -> 3 (héros incliné reste incliné) ; menace 2 -> 0 : Hepzibah se redresse ; Special depuis la main (via Feral Rage) : 5 -> 4. Substitution : rouges 3/3.
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
Carte terminée : NON (provisoire) : partie réelle humaine ; Q7 : Keen Senses sur une manigance annexe qui tombe à 0 compte aussi comme « last threat » (codé oui).


### hz009 : Feline Grace (x2)

- [x] Étape 2 : cartes de référence : `kb003` Evasive Shot (`WhenUnitWouldTakeDamage(HeroInterrupt, "You", .., is_from_attack=True)` + `PreventDamage(4)`), `ze003`.
- [x] Étape 5 : mots-pièges : « prevent **4** » ; « **Hero** Interrupt (defense) » ; Special « Ready Hepzibah » **(Limit once per phase)**.
- [x] Étape 6 : nombres texte ↔ code : Coût 0, énergie, traits DEFENSE SKILL ; Rhino : 0 dégât avec la carte. Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : Rhino attaque, héros INCLINÉ (sinon il défend lui-même : le premier jet du cas était vide) : 0 dégât avec la carte, >= 1 sans (CONTRE-CAS) ; Special : héros incliné -> redressé ; TÉMOIN D'ÉPUISEMENT (limite par phase : le 2e Special de la phase ne redresse pas, héros ré-incliné entre les deux). Substitution : rouges 3/4 (vert : le contre-cas sans la carte).
- [x] Étape 7 bis : limite imprimée ? OUI : témoin d'épuisement `hz009 ... (Limit once per phase)`, deux résolutions dans la même phase, état mesuré au second (héros resté incliné).
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
Carte terminée : NON (provisoire) : partie réelle humaine ; Q8 : la limite « une fois par phase » est-elle PAR CARTE (codé : marqueur sur la copie) ou partagée entre les deux copies ?


### hz010 : Armed to the Teeth (x2)

- [x] Étape 2 : cartes de référence : `45051` Basic Spell (`ChooseAbilities` + `ForChoiceAbility`, une seule capacité de jeu), `ok001b` (`Search.PlayerCard`, deck ET défausse), `50011` (`PlaceCountersOn(.., 'all-purpose', ..)`).
- [x] Étape 5 : mots-pièges : « Choose one » (deux branches) ; « deck **and discard** » ; Special : « all-purpose counter on a WEAPON you control » (devient un compteur du type que la carte porte : `charge` sur Energy Blaster).
- [x] Étape 6 : nombres texte ↔ code : Coût 0, physique, trait CONDITION. Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : branche 1 (armes redressées), branche 2 (arme cherchée dans le deck -> main), Special (compteur : charge 4 / polyvalent 4) ; TÉMOIN : sans le Special le total reste 3. Substitution : rouges 3/4 (vert : le témoin).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
Carte terminée : NON (provisoire) : partie réelle humaine ; Q9 : sur une arme sans compteur nommé, le compteur polyvalent devient le compteur générique sans effet (codé tel quel ; alternative : offrir la cible seulement si l'arme a un compteur nommé).


### hz011 : Vendetta (obligation)

- [x] Étape 2 : cartes de référence : `hs092` (`PlayersCannotChangeForms`), `ma017` (`PlayerActionToRemoveThisFromGame`), `tc001a` (`CostFunc.Discard("YouControlCards", ..)`), `Minion.EngagePlayer`.
- [x] Étape 5 : mots-pièges : « **while** a minion is engaged with you » ; « **Forced** Interrupt: **When** a minion enters play » (Interruption, avant l'entrée) ; « engage it **and** flip to hero form » ; Action : coût = défausser un allié, effet = retirer cette carte de la partie.
- [x] Étape 6 : nombres texte ↔ code : Boost 2, « Give to the Hepzibah player ». Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : Forced Interrupt (alter ego : le sbire est engagé et Hepzibah passe en forme héros) ; blocage du passage en alter ego avec un sbire engagé ; CONTRE-CAS sans sbire (le passage est possible) ; Action (allié défaussé, obligation retirée). Substitution : rouges 3/4 (vert : le contre-cas).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
Carte terminée : NON (provisoire) : partie réelle humaine ; Q10 : « engage it » : avec le porteur de l'obligation (codé), même si le sbire s'engagerait avec un autre joueur en multijoueur.


### hz012 : Minister T'Cahr

- [x] Étape 2 : cartes de référence : `15025` Luminous (`AfterEnemyActivatesAgainstYou`), `15027` (`Search.EncounterCard(.., include_discard_pile=True)`), `ag013` (`face.Reveal(joueur, effect)`).
- [x] Étape 5 : mots-pièges : « **after T'Cahr activates against you** » ; « search the encounter deck **and discard pile** » ; « [[SHI'AR]] **card** » (tout type) ; « and reveal it ».
- [x] Étape 6 : nombres texte ↔ code : PV 5, ATQ 1*, SCH 2*, boost 2, SHI'AR ; sbire némésis d'Hepzibah (`Nemesis: Hepzibah`). Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : activation : Shi'ar Infantry révélée (+ l'autre copie mise en jeu : 2 en jeu) ; CONTRE-CAS sans carte SHI'AR ; valeurs imprimées. Substitution : rouges 1/3 (verts : contre-cas, valeurs imprimées).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI/NON : NON
Carte terminée : NON (provisoire) : partie réelle humaine ; Q11 : les étoiles de ATQ 1* et SCH 2* sont lues comme 1 et 2 (aucun texte ne les modifie).


### hz013 : Kill Order (manigance annexe)

- [x] Étape 2 : cartes de référence : `39047` The Mojo Files (`GiveKeywordToInPlayWhenApplyThis(Minion, quickstrike=1)`), `32079` The Brotherhood.
- [x] Étape 5 : mots-pièges : « **Each** minion gains quickstrike » ; menace 3 PAR HÉROS (`3*`) ; icône Acceleration (pointe + barre, `acceleration.md`).
- [x] Étape 6 : nombres texte ↔ code : Boost 3, menace de départ 3 par héros (silhouette), 1 icône Acceleration. Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : menace 3 (solo) ; sbire révélé sous Kill Order : il s'engage et frappe aussitôt (héros incliné, sans défense) ; CONTRE-CAS sans Kill Order (aucun dégât, héros incliné). Substitution : rouges 1/3 (verts : la menace imprimée, le contre-cas).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
Carte terminée : NON (provisoire) : partie réelle humaine ; Q12 : lecture de l'icône centrale (Acceleration) et de la menace par héros, faites sur le scan.


### hz014 : The Vengeful Wing

- [x] Étape 2 : cartes de référence : `16137` Starshark (`UnitAttackGainKeyword("This", indirect_damage=True)`).
- [x] Étape 5 : mots-pièges : « [star] attacks deal **indirect** damage » (permanent, étoile en tête) ; ELITE SHI'AR VEHICLE ; ATQ 3*, SCH 2*.
- [x] Étape 6 : nombres texte ↔ code : PV 6, boost 3. Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : héros ET allié inclinés : le moteur demande « Assign 3 damage » (jamais en attaque directe) : 2 à l'allié, 1 à Hepzibah ; valeurs imprimées. Substitution : rouges 1/2 (vert : valeurs imprimées).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
Carte terminée : NON (provisoire) : partie réelle humaine ; Q13 : la défense s'applique avant la répartition indirecte (comportement du moteur, `indirect-damage.md`).


### hz015 : Shi'ar Infantry (x2)

- [x] Étape 2 : cartes de référence : `15027` Chaos Manipulation (`Search.EncounterCard(.., name=..)` + `PutIntoPlay`), `16137` (`WhenCardBecomeBoost("This", ..)`).
- [x] Étape 5 : mots-pièges : « **another** copy » ; « put it into play (it is **not revealed**) » ; Boost « [star] seul » (aucune icône : `Boost` 0).
- [x] Étape 6 : nombres texte ↔ code : PV 2, ATQ 2, SCH 1, SHI'AR SOLDIER. Résultat : vert.
- [x] Étape 7 : cas `[hz]` par capacité, preuve par substitution : When Revealed : 2 copies en jeu (deck à 2 copies) ; Boost : carte donnée face cachée à Rhino, qui attaque : la carte entre en jeu ; valeurs imprimées. Substitution : rouges 2/3 (vert : valeurs imprimées).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir l'en-tête (8 parties Hepzibah + 8 du témoin, 0 exception) ; journaux lus.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON
Carte terminée : NON (provisoire) : partie réelle humaine ; Q14 : en Boost, la carte est mise en jeu engagée avec le joueur attaqué (codé), pas avec le premier joueur.

### hz016, hz017, hz018 : Energy, Genius, Strength (reskins de ressources, sans module)

- [x] Aucune capacité : « Max 1 per deck. » (Basic, `RES` YY / BB / RR, `MaxPerDeck` 1). Cartes à part (précédent Hellcat et Corsair `cr017-cr019`).
Carte terminée : NON (provisoire) : Q15 : cartes à part (codé) ou arts alternatifs des ressources officielles ?
- [x] **26/10/2026, arbitrage reskins** (RR « A copy of a card is defined by title » + GUIDE §12 bis) : ces trois ressources ne changent que l'image de `01088` / `01089` / `01090` : ART ALTERNATIF des ressources doubles. Traitement, comme Gwenpool / Beast / Binary : collection `hepzibah` dans `COLLECTIONS` (`ui-app/src/board/variantes.ts`) ET dans `COLLECTIONS_RESSOURCES` (`public/js/prepare/app.js`, proposée par défaut au héros « Hepzibah » : `collectionDuHeros`). Les cartes restent dans `cards.json` (précédent TMNT / Gwenpool).
      « Max 1 per deck » par TITRE : `validerDeck` (`public/js/deckbuilder/regles.js`, `cleCopie` = titre|sous-titre) compte déjà `01088` + le reskin comme un même titre ; **aucun correctif nécessaire**, preuve : `tools/tests-lanceur/regles-ressources-doubles-par-titre.test.mjs` (4 verts : chaque reskin du dépôt + son officielle = « Trop d’exemplaires de « Energy » : 2/1 », deux mêmes reskins idem, un seul légal, trois titres différents sans gêne). Le moteur n'applique pas MaxPerDeck (seul le constructeur le juge).
      Collection : `ui-app/src/board/resources-art-packs-fanmade-2026-10.test.ts` (45 verts : ordre Energy/Genius/Strength, wizard aligné, images présentes ; ROUGE vu avant le câblage : 18 échecs sur 27, puis rouge à nouveau en retirant l'entrée du wizard).
      Carte terminée : NON (provisoire) : partie réelle humaine (voir la collection « Hepzibah » dans la modale du héros et les trois ressources à l'écran).

---

## Ce qui reste « à vérifier en partie réelle » (aucun outil du projet ne le remplace)

- Une partie complète avec Hepzibah choisie dans la liste Fan-made (deck de départ sans decklist d'auteur : le joueur choisit ses cartes d'aspect).
- Le choix de la carte à Special (fenêtre « Resolve the "Special" ability ») après un événement : le harnais prend la première candidate.
- Armed to the Teeth : la fenêtre « Choose one » à deux branches.
- Vendetta : le passage forcé en forme héros quand un sbire entre en jeu (l'écran doit montrer la bascule).
- The Vengeful Wing : la fenêtre « Assign N damage » (répartition indirecte).
- Les icônes de ressource, lues à l'œil et comparées à des cartes officielles de même glyphe (pas de découpe pixel par pixel).
- Les 18 images à l'écran (Kill Order est en paysage).
- Le survol de la biographie dans l'assistant (`heros-info.js`, `hz001a` : le module se charge, la clé est la bonne).

## Autoplay du 26/10/2026 (corrections de verdicts : hz003, hz005, hz007)

`tools/autoplay.py .game-src-hz --deck hepzibah --vilains klaw --profils equilibre --parties 8` : 8 parties, 0 victoire / 8 défaites (4,1 rounds), 0 bloquée, **0 traceback**
sur les 8 journaux ; Targeting Goggles s'active (54 lignes, dont une activation lue), Feral Rage est jouée (attaque, 2 dégâts). Témoin `she_hulk` (même vilain) : 8 parties, 0 victoire,
1 bloquée. Deck `hepzibah` seul : OK « identité hz001a, main 6, deck 9 ». Le Special résolu en phase du méchant n'est pas atteint par le pilote : prouvé par les cas
`Puzzle.BeginVillainPhase` / `ResolveSpecial` / `EndVillainPhase`.
