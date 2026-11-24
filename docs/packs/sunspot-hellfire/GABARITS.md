# Sunspot (Dipsome, campagne Hellfire Hunt) : gabarits PROCESSUS-CARTE, 17 card_id

Pack `sunspot_hellfire`, préfixe `so`, set 231 (« Custom (Hellfire Hunt - Sunspot) »). Source : zip « Hellfire Hunt Campaign », dossier
`Hero/Sunspot/` (23 images : 17 cartes distinctes, dont 6 en double ; **aucun texte fourni**, tout est lu sur les scans ; auteur Dipsome, MC Custom
Content). **La campagne Hellfire Hunt elle-même (cartes de campagne, scénarios, modules, règles) n'est PAS portée** : seul le héros l'est.
Le héros est un STOCK de compteurs `solar` posé sur l'identité : l'alter ego (Setup 5, Energy Absorption) le remplit, le héros le dépense
(montage de Spider-Woman, Kajislav `sw`). Deck `deck/starter/sunspot_hellfire.json` : 15 cartes, `player_deck` VIDE (aucune decklist fournie, décision du
06/09/2026). Nom de pack et de set distincts du Sunspot officiel (allié `40016`, pack next_evol), qu'on ne touche pas.

Cas : `Fusion/marvel-lcg-src/tools/cas/sunspot_hellfire.py` (filtre `[so]`, 54 cas). Plateau : `ui-app/src/board/sunspot-plateau.test.ts` (5 cas verts d'emblée).

## ⚠ DOUTES EN ATTENTE DE L'UTILISATEUR (choix provisoire codé, cartes « NON (provisoire) »)

1. **so001a** Solar Rechanneling : « If you removed at least half of the counters, ready Sunspot » : la moitié du stock **avant** le retrait (retenu :
   5 compteurs → il faut en retirer 3) ou la moitié de ce qu'il en RESTE ? Et X peut-il valoir 0 (retenu : oui, rien ne se passe) ?
2. **so001b** Energy Absorption : « up to 3 cards » : au moins une carte défaussée (retenu) ou zéro autorisé ? « Resource icon » = les icônes IMPRIMÉES de
   toutes couleurs, wild compris (retenu : oui).
3. **so002** Cannonball : « the next card you play this phase » : la prochaine carte jouée, de n'importe quel type (retenu), une seule fois.
4. **so004** Blessings of the Sun : le compteur est posé AVANT le calcul (« for each solar counter on Sunspot » compte le compteur qu'on vient de poser :
   retenu) ou le calcul se fait AVANT la pose ?
5. **so005** Radiant Disruption : la seconde manigance (« another scheme », avec AERIAL) est-elle obligatoire ? (retenu : facultative, le moteur propose
   « Cancel »).
6. **so007** Solar Flare : « each minion engaged with you » : les dégâts frappent la cible choisie ET chaque sbire engagé avec vous, sans compter deux
   fois la cible (retenu). X = 0 désoriente quand même (retenu).
7. **so008** Solar Surge : les paliers se lisent au moment du PAIEMENT, sur le stock du joueur qui paie (retenu) ; « triple instead » remplace le double.
8. **so011** Solar Soar : « Hero Response: At the end of your turn » : seulement sous forme de héros (retenu).
9. **so012** M-Pox Sickness : « the first card you play each round » : toute carte jouée (événement, soutien, amélioration, allié), y compris sous forme
   d'alter ego (retenu) ; les ressources posées ne comptent pas.
10. **so013** Superhuman Mutants Murdering : (a) texte récursif tel qu'imprimé (la seconde activation redéclencherait la Response à l'infini) : retenu =
    UNE activation supplémentaire par activation d'origine, sans rebond ; (b) « it » = Donald Pierce (retenu), pas la manigance ; (c) menace de départ 6
    FIXE (aucune icône par héros imprimée) ; (d) icône [hazard] lue contre `01180` Legions of Hydra (même glyphe).
11. **so015** Cybernetic Assault : le texte ne dit pas si Pierce, tout juste mis en jeu, attaque aussi. Retenu : en jeu → il attaque ; absent → mis en jeu
    engagé avec vous (son Quickstrike le fait alors attaquer en forme de héros), pas d'attaque forcée en plus.
12. **so016** Political Persecution : « place 2 threats to that scheme » = 2 menaces SUR cette manigance (retenu), sinon sur la manigance principale.

## Gates du héros

- [x] PROCESSUS-HEROS étapes 1 à 8 : cartes (`cards.json`, pack `sunspot_hellfire`), scripts (`src/cards/pack/sunspot_hellfire/`), deck de départ, `sets_info.json`
      (« 231. Custom (Hellfire Hunt - Sunspot) »), préfixe `so`, images (`assets/pics/so*.jpg`, 615×882, non versionnées ; `so013` en paysage 882×615),
      textes FR (`ui-app/src/board/textes-fr-fanmade.ts` + copie publique régénérée), nom FR du compteur (`compteurs-fr.ts` : `solar` → « solaire »),
      biographie (`public/js/prepare/heros-info.js`, `so001a` ; **survol dans l'assistant NON vérifié**).
- [x] Légalité des decks (§10) : 0 signature étrangère dans un `player_deck` (vide).
- [x] Valeurs imprimées relues contre `cards.json` : 0 écart (stats lues sur les scans).
- [ ] Une partie complète jouée par un humain : NON FAITE.

Modifications du MOTEUR (toutes `# CORRECTIF`, 26/10/2026) : `src/game/card/face/card_face.py` (compteur `'solar'` ajouté à `COUNTER`), `src/game/card/factory.py`
(`so006` dans la liste blanche des événements à deux capacités de jeu). Aucune autre.

> **IMAGES so001a / so001b ÉCHANGÉES le 26/10/2026.** Dans le moteur `so001a` est la face HÉROS (`type: Hero`, comme `01001a` Spider-Man et `sw001a`
> Spider-Woman, dont l'image montre bien le héros) et `so001b` l'alter ego. Mais le zip de l'auteur numérote ses faces dans l'autre sens (« 32A » = Roberto,
> « 32B » = Sunspot) et les deux scans avaient été rangés tels quels : `assets/pics/so001a.jpg` affichait Roberto sur la face héros, et inversement. Les deux fichiers
> sont échangés (`so001a.jpg` = Sunspot, `so001b.jpg` = Roberto). Aucun script, `cards.json` ni deck touché ; `assets/pics/` n'est pas versionné (sauvegarde des
> deux anciens fichiers hors dépôt). À regarder en partie : la carte héros doit montrer Sunspot, l'alter ego Roberto Da Costa.

### so001a : * Sunspot (face HÉROS) — X-FORCE. PV 10, THW 0, ATK 0, DEF 0, main 5.

Solar Rechanneling — Interrupt : when you use one of Sunspot's basic powers, remove X solar counters → +X to that power for this use ; at least half → ready Sunspot.
Forced Response : at the end of each phase, if no solar counters, exhaust Sunspot and flip him into alter-ego form.

- [x] Étape 2 : cartes de référence : `14002` Scarlet Witch et `27047` Dum Dum Dugan (`WhenUnitUseBasicPower` + `message.GainValue`) ; `sw006`/`sw007` (X choisi,
      valeur RENDUE) ; `14001a` Quicksilver (`ReadyAll`) ; `01025` Split Personality (`ChangeToOtherIdentityForm`).
- [x] Étape 5 : mots-pièges : « at least HALF of the counters » (avant le retrait : doute 1), « At the end of EACH phase » (joueurs ET méchant), « When you USE a
      basic power » (ATK, THW, DEF : trois cas), « Forced » (obligatoire). Résultat : conforme.
- [x] Étape 6 : nombres : PV 10, ATK/THW/DEF 0, main 5. Résultat : conforme (cas « valeurs imprimées »).
- [x] Étape 7 : cas : ATK (X=5 → 5 dégâts), témoin stock vide, THW (menace 6 → 1), DEF (Rhino ne fait aucun dégât), témoin DEF (2 dégâts), redressement
      (≥ moitié), reflux en alter ego (fin de phase des joueurs), témoin (reste héros), reflux après la phase du méchant. Substitution : rouges 6/10 (vertes sans
      module : valeurs imprimées et les trois témoins d'absence, assumés).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (compteurs `solar` sur l'identité) : `sunspot-plateau.test.ts` (compteur dessiné avec sa valeur). Pas de
      correctif à voir rouge (pack neuf).

Carte terminée : NON (provisoire) : aucune partie humaine ; doute 1.

### so001b : * Roberto Da Costa (face ALTER EGO) — MUTANT. PV 10, REC 3, main 6.

Setup : place 5 solar counters here. Energy Absorption — Action : discard up to 3 cards ; for each resource icon discarded, place 1 solar counter here.

- [x] Étape 2 : `sw001b` Julia Carpenter (Setup d'identité `WhenCardSetup` + Action qui remplit le stock) ; `01023` Legal Practice (`CostFunc.Discard` à plage, cartes
      défaussées lues sur le coût) ; `FacesCounter.GetPrintedResources(...).val` pour compter les icônes.
- [x] Étape 5 : mots-pièges : « up to 3 » (au moins 1 : doute 2), « each resource ICON » (icônes imprimées, wild compris), « here » (l'identité). Conforme.
- [x] Étape 6 : nombres : PV 10, REC 3, main 6, 5 compteurs au Setup, 3 cartes max. Conforme.
- [x] Étape 7 : cas : Setup (5), Energy absorbée avec 2 cartes (5 + 4 = 9), 1 carte (7), 3 cartes (11), valeurs imprimées. Substitution : rouges 4/5 (valeurs imprimées).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros.
- [x] Étape 8 bis : OUI (compteurs sur l'identité) : cas plateau `sunspot-plateau.test.ts`.

Carte terminée : NON (provisoire) : aucune partie humaine ; doute 2.

### so002 : * Cannonball (Sam Guthrie), allié — X-FORCE. Coût 3, PV 3, ATK 2 (2★), THW 2 (2★).

Response : after Cannonball attacks, reduce the cost of the next card you play this phase by 1.

- [x] Étape 2 : `05008` Nakia Bahadir (`Worlds.UpdateNextCardPlayCost(.., -1, in_this="Phase")`) ; `01028` (`AfterUnitAttackEnd`) ; `sz002` Cannonball (stats « 2** »).
- [x] Étape 5 : mots-pièges : « the NEXT card ... THIS PHASE » (une carte, la phase en cours), « After Cannonball attacks » (ses propres attaques). Conforme.
- [x] Étape 6 : nombres : coût 3, PV 3, ATK 2**, THW 2**, réduction 1. Conforme.
- [x] Étape 7 : cas : après son attaque (2 dégâts), Blazing Strike (coût 2) payée par UNE ressource (2 + 6 = 8 dégâts) ; témoin sans attaque (0 dégât) ; valeurs
      imprimées. Substitution : rouges 1/3 (valeurs imprimées et témoin d'absence).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan. [x] Étape 8 bis : NON (aucun attachement, compteur ni changement de zone propre).

Carte terminée : NON (provisoire) : aucune partie humaine ; doute 3.

### so003 : Blazing Strike (événement, coût 2, [physical], ×2) — ATTACK.

Hero Action (attack) : remove 1 solar counter from Sunspot → deal 6 damage to an enemy. If Sunspot has AERIAL, stun that enemy.

- [x] Étape 2 : `01021` Gamma Slam (événement d'attaque) ; `sw007` (compteur de l'identité = COÛT) ; `05031` (`GiveStatus`).
- [x] Étape 5 : mots-pièges : « If Sunspot has the AERIAL trait » (trait de Solar Soar), « stun THAT enemy » (la cible). Conforme.
- [x] Étape 6 : nombres : coût 2, 6 dégâts, 1 compteur. Conforme.
- [x] Étape 7 : cas : 6 dégâts et 1 compteur (5 → 4) ; avec AERIAL, ennemi Sonné ; témoin sans AERIAL ; stock vide, carte non jouable. Substitution : rouges 3/4 (stock vide :
      0 dégât attendu, vert sans module, assumé).
- [x] Étape 7 bis : NON. [x] Étape 8 : voir le bilan. [x] Étape 8 bis : NON.

Carte terminée : NON (provisoire) : aucune partie humaine ; aucun doute propre.

### so004 : Blessings of the Sun (événement, coût 0, [mental], ×2) — DEFENSE.

Hero Interrupt (defense) : when you defend against an attack, place 1 solar counter on Sunspot → for each solar counter on Sunspot, +1 DEF for that attack.

- [x] Étape 2 : `14014` Never Back Down (`WhenUnitDefendAgainstAttack(HeroInterrupt, "You", .., is_basic_defense=True)` + `message.GainDEFForThisAttack`).
- [x] Étape 5 : mots-pièges : « place 1 counter → for each solar counter » (le compteur posé compte : doute 4). Conforme.
- [x] Étape 6 : nombres : coût 0, 1 compteur posé. Conforme.
- [x] Étape 7 : cas : stock 1 puis Rechanneling (Tiger Shark ATK 3 : 0 dégât) ; stock 0 (+1 DEF puis +1 : 1 dégât) ; témoin sans l'événement (3 dégâts). ⚠ Le pilote
      accepte AUSSI l'interruption du héros (`passer_sur_option` ne la décline pas) : les cas mesurent la COMBINAISON. Substitution : rouges 2/3 (témoin d'absence).
- [x] Étape 7 bis : NON. [x] Étape 8 : voir le bilan. [x] Étape 8 bis : NON (pas de zone nouvelle).

Carte terminée : NON (provisoire) : aucune partie humaine ; doute 4.

### so005 : Radiant Disruption (événement, coût 1, [mental], ×2) — THWART.

Hero Action (thwart) : remove X solar counters from Sunspot. Remove X threat from a scheme. If Sunspot has AERIAL, remove X threat from another scheme.

- [x] Étape 2 : `sw006` Psi-Web Trap (X retiré = X contré) ; `48009` Scout Ahead (« another scheme » : `MayChooseOneAbility` + `exclude`).
- [x] Étape 5 : mots-pièges : « another » (exclure la première), AERIAL, **« may » ABSENT** : la seconde manigance est OBLIGATOIRE (RR « May » ; corrigé le 26/10/2026 : plus d'option « Cancel », `ChooseAbilities` forcé, le joueur choisit seulement LAQUELLE ; sans autre manigance, rien n'est forcé).
- [x] Étape 6 : nombres : coût 1. Conforme.
- [x] Étape 7 : cas : X = 5 (menace 6 → 1, stock 0) ; avec AERIAL, X aussi sur une autre manigance (`so013` : 6 → 1) ; **OBLIGATOIRE : le pilote cherche « Cancel » (`preferer_option`), il n'existe plus, la 2e manigance perd quand même ses menaces** (vu ROUGE avant : `so013` restait à 6) ; CONTRE-CAS AERIAL sans autre manigance (rien ne plante, une seule retirée). Substitution : rouges 4/4.
- [x] Étape 7 bis : NON. [x] Étape 8 : voir le bilan. [x] Étape 8 bis : NON.

**Doute 5 TRANCHÉ le 26/10/2026** (RR « May » : seul « may » donne une option) : obligatoire. Corrigé.
Carte terminée : NON (provisoire) : aucune partie humaine.

### so006 : Soak Up the Sun (événement, coût 2, [energy], ×2) — SUPERPOWER.

Alter-Ego Action : place 5 solar counters on your identity card. Hero Action : if you have AERIAL, place 3 solar counters on Sunspot.

- [x] Étape 2 : `hp003` Gigantification, `bm005` (deux capacités de jeu → liste blanche `factory.py`, **`so006` ajouté**) ; `sw001b`.
- [x] Étape 5 : mots-pièges : « If you have the AERIAL trait » (la Hero Action reste jouable sans le trait). Conforme.
- [x] Étape 6 : nombres : 5 et 3 compteurs, coût 2. Conforme.
- [x] Étape 7 : cas : alter ego (+5), héros avec AERIAL (+3), héros sans AERIAL (rien). Substitution : rouges 2/3 (témoin).
- [x] Étape 7 bis : NON. [x] Étape 8 : voir le bilan (le deck monte une partie : liste blanche vérifiée par `verifier_tous_les_decks`). [x] Étape 8 bis : NON.

Carte terminée : NON (provisoire) : aucune partie humaine ; aucun doute propre.

### so007 : Solar Flare (événement, coût 3, [physical]) — ATTACK. SUPERPOWER.

Hero Action (attack) : confuse an enemy. Remove any number of solar counters → deal 2 damage to that enemy and each minion engaged with you for each counter removed.

- [x] Étape 2 : `05031` Concussive Blow (Confused puis dégâts) ; `06006`/`14032` (« each minion engaged with you ») ; `sw007` (X retiré).
- [x] Étape 5 : mots-pièges : « each minion engaged with YOU » (`joueur.GetEngagedMinions()`), « EACH counter removed » (2 × X). Conforme (doute 6).
- [x] Étape 6 : nombres : coût 3, 2 dégâts par compteur. Conforme.
- [x] Étape 7 : cas : X = 5 → 10 dégâts à Rhino ET au sbire engagé, Rhino désorienté, stock 0 ; stock vide : désorienté, 0 dégât. Substitution : rouges 2/2.
- [x] Étape 7 bis : NON. [x] Étape 8 : voir le bilan. [x] Étape 8 bis : NON.

Carte terminée : NON (provisoire) : aucune partie humaine ; doute 6.

### so008 : Solar Surge (ressource, [energy], ×2).

Resource : double the resources this card generates if Sunspot has more than 2 solar counters (triple if more than 4).

- [x] Étape 2 : `01055` The Power of Aggression (`CheckThisCanDropPay(fn)`).
- [x] Étape 5 : mots-pièges : « MORE than 2 » (3 ou plus), « triple INSTEAD » (jamais ×6), joueur qui paie. Conforme (doute 7).
- [x] Étape 6 : nombres : 2 et 4 (seuils), ×2 et ×3. Conforme.
- [x] Étape 7 : cas : stock 5 → ×3 (paie un cout 3 avec UNE carte) ; stock 3 → ×2 (cout 2) ; stock 2 → rien. Substitution : rouges 2/3 (témoin).
- [x] Étape 7 bis : NON. [x] Étape 8 : voir le bilan. [x] Étape 8 bis : NON.

Carte terminée : NON (provisoire) : aucune partie humaine ; doute 7.

### so009 : * Da Costa International (soutien, coût 1, [mental]) — LOCATION. Unique.

Alter-Ego Response : after you resolve your « Energy Absorption » ability, place 1 solar counter on your identity.

- [x] Étape 2 : `21037` Mystic Senses (`AfterPlayerResolveAbility(.., ability_name=..)`).
- [x] Étape 5 : mots-pièges : « YOUR Energy Absorption » (la capacité nommée de Roberto), Response d'ALTER EGO. Conforme.
- [x] Étape 6 : nombres : coût 1, 1 compteur. Conforme.
- [x] Étape 7 : cas : avec le soutien 5 + 2 + 1 = 8 ; témoin sans le soutien 7. Substitution : rouges 1/2 (témoin).
- [x] Étape 7 bis : NON. [x] Étape 8 : voir le bilan. [x] Étape 8 bis : NON.

Carte terminée : NON (provisoire) : aucune partie humaine ; aucun doute propre.

### so010 : * Radiant Avenger (amélioration TITLE, coût 2, [physical]). Unique.

Sunspot gains AVENGER. Hero Action : exhaust this card and remove 1 solar counter → +1 ATK until the end of the round. Action : exhaust this card → place 1 solar counter on Sunspot.

- [x] Étape 2 : `01017` Cosmic Flight (`GiveKeywordToAttached(.., trait=..)`) ; `14022` Adrenaline Rush (`GainUntilPhaseEnd` → `GainUntilRoundEnd`).
- [x] Étape 5 : mots-pièges : « Exhaust AND remove » (deux coûts), « until the end of the ROUND ». Conforme.
- [x] Étape 6 : nombres : coût 2, +1 ATK, 1 compteur. Conforme.
- [x] Étape 7 : cas : trait AVENGER ; Hero Action (ATK 1, stock 4, carte inclinée) ; Action (stock 6, carte inclinée). Substitution : rouges 3/3.
- [x] Étape 7 bis : limite imprimée ? NON. [x] Étape 8 : voir le bilan. [x] Étape 8 bis : OUI (amélioration attachée) : `sunspot-plateau.test.ts`.

Carte terminée : NON (provisoire) : aucune partie humaine ; aucun doute propre.

### so011 : Solar Soar (amélioration, coût 3, [physical]) — SUPERPOWER.

Sunspot gains AERIAL. Hero Response : at the end of your turn, place 1 solar counter on Sunspot.

- [x] Étape 2 : `01017` (trait) ; `AfterPlayerTurnEnd(HeroResponse, "You", op)` ; `Puzzle.EndPlayerTurn()` du banc.
- [x] Étape 5 : mots-pièges : « at the end of YOUR turn » (le tour du joueur), Response facultative. Conforme (doute 8).
- [x] Étape 6 : nombres : coût 3, 1 compteur. Conforme.
- [x] Étape 7 : cas : trait AERIAL ; fin de tour : +1 (5 → 6). Substitution : rouges 2/2.
- [x] Étape 7 bis : NON. [x] Étape 8 : voir le bilan. [x] Étape 8 bis : OUI (amélioration attachée) : `sunspot-plateau.test.ts`.

Carte terminée : NON (provisoire) : aucune partie humaine ; doute 8.

### so012 : M-Pox Sickness (obligation, boost 2) — à donner au joueur Roberto Da Costa.

Increase the resource cost of the first card you play each round by 1. Alter-Ego Action : remove 3 solar counters from your identity → remove M-Pox Sickness from the game.

- [x] Étape 2 : `27132` Friends and Family (`IncreaseResourceCostToPlay`) ; `51031` (`CardFace`) ; `21026` Loss of Control (`PlayerActionToRemoveThisFromGame`).
- [x] Étape 5 : mots-pièges : « the FIRST card ... each ROUND » (`this_round_played_cards` vide), « remove from the GAME » (pas défausse). Conforme (doute 9).
- [x] Étape 6 : nombres : +1, 3 compteurs, boost 2. Conforme.
- [x] Étape 7 : cas : première carte à +1 (coût 3, RR insuffisant) ; payée par RR + YY (passe) ; témoin sans l'obligation ; Action (hors jeu, stock 5 → 2). Substitution : rouges 2/4
      (RR+YY passe avec ou sans l'obligation : il fixe le surcoût à exactement 1 ; et le témoin).
- [x] Étape 7 bis : limite imprimée ? NON (« each round » est une condition de coût, pas une limite d'usage). [x] Étape 8 : voir le bilan. [x] Étape 8 bis : NON.

Carte terminée : NON (provisoire) : aucune partie humaine ; doute 9. ⚠ Le cas « stock 2, Action non jouable » n'a pas pu être écrit : une Action non offerte lève une
`AssertionError` de mise en place du banc ; le coût (3 compteurs) est couvert par le cas nominal.

### so013 : Superhuman Mutants Murdering (manigance annexe de l'ennemi juré) — menace de départ 6, boost 3, [hazard].

Forced Response : after Donald Pierce activates against you, it activates against you again.

- [x] Étape 2 : `11051` Ancient Grudge (`DoActivate`) ; `04078`/`15025` (`AfterEnemyActivatesAgainstYou`).
- [x] Étape 5 : mots-pièges : « it » (Pierce), « against YOU », « again » (une fois, sans rebond : doute 10). ⚠ La garde anti-rebond se fait par `activate_message.by_effect` (une
      garde « en cours » ne tient pas, voir RECETTES §37).
- [x] Étape 6 : nombres : menace 6 (fixe), boost 3, icône [hazard] (lue contre `01180`). Conforme.
- [x] Étape 7 : cas : menace 6 ; l'invariant « autant d'activations supplémentaires que de Responses ignorées, au moins une » (+ ≥ 6 dégâts) ; témoin sans la manigance (3 dégâts).
      ⚠ Le banc enchaîne plusieurs activations de Pierce (9 dégâts mesurés) : on ne mesure donc PAS un total exact. Substitution : rouges 1/3 (valeurs imprimées et témoin).
- [x] Étape 7 bis : NON. [x] Étape 8 : voir le bilan. [x] Étape 8 bis : OUI (manigance annexe dessinée) : `sunspot-plateau.test.ts`.

Carte terminée : NON (provisoire) : aucune partie humaine ; doute 10. Le Boost (3 icônes) n'a aucun effet imprimé.

### so014 : * Donald Pierce (sbire de l'ennemi juré) — CYBORG. ELITE. HELLFIRE. PV 6, ATK 3, SCH 1, boost 3. Toughness. Quickstrike. Villainous.

- [x] Étape 2 : mots-clés natifs lus dans `desc` (`01167` Vulture : Quickstrike ; `11041` : Toughness, Villainous) : **aucun module** (rien d'imprimé hors mots-clés).
- [x] Étape 5 : mots-clés : fiches `mots-cles/toughness.md`, `quickstrike.md`, `villainous.md` ouvertes. Conforme.
- [x] Étape 6 : nombres : PV 6, ATK 3, SCH 1, boost 3. Conforme (cas « valeurs imprimées »).
- [x] Étape 7 : cas : valeurs imprimées et traits. Substitution : sans objet (aucun module).
- [x] Étape 7 bis : NON. [x] Étape 8 : voir le bilan (Pierce attaque dans les cas `so013` et `so015`). [x] Étape 8 bis : OUI (sbire dessiné) : `sunspot-plateau.test.ts`.

Carte terminée : NON (provisoire) : aucune partie humaine. Quickstrike à l'engagement n'a pas de cas dédié.

### so015 : Cybernetic Assault (traîtrise de l'ennemi juré, boost 1, ×2).

When Revealed : Donald Pierce attacks you. If he is not in play, search the encounter deck and discard pile for him and put him into play engaged with you.

- [x] Étape 2 : `01164` Titania's Fury (`FindCardOnField` + `DoAttackYou`) ; `11051` Ancient Grudge (`Search.EncounterCard(.., include_discard_pile=True)` + `PutIntoPlay`).
- [x] Étape 5 : mots-pièges : « If he is NOT in play » (doute 11 : attaque après mise en jeu ?). Conforme à la lecture retenue.
- [x] Étape 6 : nombres : boost 1. Conforme.
- [x] Étape 7 : cas : Pierce en jeu → 3 dégâts ; absent (dans le deck rencontre) → en jeu. Substitution : rouges 2/2.
- [x] Étape 7 bis : NON. [x] Étape 8 : voir le bilan. [x] Étape 8 bis : NON.

Carte terminée : NON (provisoire) : aucune partie humaine ; doute 11.

### so016 : Political Persecution (traîtrise de l'ennemi juré, TACTIC, boost 1).

When Revealed : if the Superhuman Mutants Murdering scheme is in play, place 2 threats to that scheme. If it is not in play, place 2 threats to the main scheme.

- [x] Étape 2 : `01178` Kree Manipulator (`Worlds.FindMainScheme` + `PlaceThreatOnSchemes`).
- [x] Étape 5 : mots-pièges : « IF NOT in play » (sinon la principale, jamais les deux). ⚠ `card_type=SideScheme` n'existe pas (NameError avalé) : `Scheme2`. Conforme (doute 12).
- [x] Étape 6 : nombres : 2 menaces, boost 1. Conforme.
- [x] Étape 7 : cas : annexe absente → 2 sur la principale ; annexe en jeu → 6 + 2 = 8 sur elle, 0 sur la principale. Substitution : rouges 2/2.
- [x] Étape 7 bis : NON. [x] Étape 8 : voir le bilan. [x] Étape 8 bis : NON.

Carte terminée : NON (provisoire) : aucune partie humaine ; doute 12.

## Bilan du héros (chiffres)

- **Cas `test_capacites`** (`[so]`) : **54 sur 54 verts** (dont 5 cas de valeurs imprimées et 11 témoins d'absence). Plateau : 5 cas verts (`sunspot-plateau.test.ts`).
- **Preuve par substitution** (`tools/substituer_pack.py`, pack sauvegardé avant dans `/tmp/sauvegarde_pack_so`, empreinte `79288677…` identique avant et après, `diff -r` vide) :
  les 16 cartes à script ont au moins un cas qui rougit sans leur module. Vertes sans module, assumées : valeurs imprimées (so001a, so001b, so002, so013, so014), témoins d'absence
  (so001a ×3, so002, so003 « stock vide », so004, so006, so008, so009, so012 ×2, so013). `so014` n'a aucun module (mots-clés natifs).
- **Autoplay ciblé** : 8 parties de `sunspot_hellfire` contre Rhino (normal, équilibré) : 0 victoire, 0 blocage, **0 exception** (grep `NameError|AttributeError|TypeError|KeyError|
  AssertionError` : 0 dans les 8 journaux), 3,5 rounds en moyenne (6 manigances complétées, 2 défaites). Témoin `spider_man` : 8 parties, 0 victoire, 0 blocage, 0 exception, 6,9 rounds.
  Aucune victoire des deux côtés : le deck de joueur est vide (le harnais le complète de ressources inertes). Sunspot perd plus vite (3,5 contre 6,9 rounds) : sa main de départ
  est faite de cartes qui coûtent des compteurs et son alter ego passe son temps à se recharger. Journaux lus : les 15 titres du deck apparaissent, ainsi qu'Energy Absorption (16 fois)
  et Solar Rechanneling (4 fois).
- **Decks** : `verifier_tous_les_decks` complet : **175 sur 175 montent une partie** (`sunspot_hellfire` : « identité so001b, main 6, deck 9 », liste blanche `so006` incluse).
- **Statique** : `test_cards` : 7 744 modules sans erreur ; `verifier_appels_modules` OK et **calibré** (un appel inventé exprès, `Faces.MethodeInventeeSunspot`, est bien refusé ; fichier
  retiré) ; `verifier_cibles` OK ; `verifier_prefixes` OK ; `verifier_traductions_fr` OK ; tests de vocabulaire FR (statuts, événements, compteurs), textes FR et `tsc` verts.

## À vérifier en partie réelle (aucun outil du projet ne le voit)

- Une partie complète avec Sunspot choisi dans la liste Fan-made, y compris le basculement forcé en alter ego quand le stock tombe à zéro.
- La saisie du nombre X (Solar Rechanneling, Radiant Disruption, Solar Flare) à l'écran : liste de nombres du stock au maximum.
- Solar Rechanneling pendant une DÉFENSE jouée avec Blessings of the Sun : l'ordre des deux fenêtres (le banc mesure la combinaison).
- L'icône [hazard] de Superhuman Mutants Murdering et les 17 images à l'écran (`so013` en paysage) ; la biographie au survol dans l'assistant.
- Les icônes de ressource : lues à l'œil et comparées à des cartes officielles de couleur connue (rouge = physique, bleu = mental, jaune = énergie), sans découpe pixel par pixel.
- Quickstrike de Donald Pierce à l'engagement, et la Response « Forced » de so013 en partie réelle (le banc enchaîne des activations supplémentaires).
- Le Boost des trois cartes de némésis (3, 3 et 1 icônes) : aucun effet imprimé.

## Autoplay du 26/10/2026 (corrections de verdicts : so005, images so001a/b)

`tools/autoplay.py .game-src-so --deck sunspot_hellfire --vilains klaw --profils equilibre --parties 8` : 8 parties en 126 s, 0 victoire / 8 défaites, **0 traceback** sur les 8
journaux ; Radiant Disruption est jouée dans les parties (3 activations lues). Témoin `she_hulk` (même vilain) : 8 parties, 0 victoire, 1 bloquée. Deck `sunspot_hellfire` seul : OK
« identité so001b, main 6, deck 9 ». Les images `so001a` / `so001b` sont échangées (voir l'encadré avant le gabarit so001a).
