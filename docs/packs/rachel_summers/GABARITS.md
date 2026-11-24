# Rachel Summers / Marvel Girl (Dipsome, campagne Hellfire Hunt) : gabarits PROCESSUS-CARTE, 26/10/2026

Pack `rachel_summers` (préfixe `rm`, set 232, auteur Dipsome). Scripts : `src/cards/pack/rachel_summers/{marvel_girl,marvel_girl_nemesis}/`
(15 modules ; `rm015` Ahab n'en a pas : Ténacité et Vilenie viennent de sa fiche). Cas : `tools/cas/rachel_summers.py` (**59 cas `[rm]`,
59/59 verts**) ; plateau : `ui-app/src/board/rachel-summers-plateau.test.ts` (6 cas verts) ; deck `deck/starter/rachel_summers.json`
(`player_deck` vide : le dossier du zip n'imprime aucune decklist) ; recettes `RECETTES-MOTEUR.md` §36 ; fiche `mots-cles/tour-supplementaire.md`.
Image : `assets/pics/rm001a.jpg` à `rm016.jpg` (17 fichiers, hors git).

**Aucune carte n'est « terminée »** : il manque la partie réelle jouée par un humain, et des questions de règle restent en suspens
(consigne utilisateur du 25/10/2026 : les doutes sont gardés pour la fin ; le choix provisoire est celui qui est codé).

**Deux ajouts MOTEUR** (marqués `# CORRECTIF`, derrière un drapeau de joueur, sans effet sur les autres héros) :
- le tour supplémentaire de `rm007` : `World.PlayerPhase` (`world.py`) + `PlayerPhase.FinDeTourSupplementaire` (`player_phase.py`), drapeau
  `RM_TOUR_SUPPLEMENTAIRE` ; **preuve par mutation** : la boucle désactivée, aucune ligne « Additional turn » dans 3 parties sur 3 (8 sur 8 avec) ;
- « end this turn » de `rm013` : `EventManager` (`event/manager.py`), drapeau `RM_FIN_DE_TOUR` ; **preuve par mutation** : le test conditionnel retiré,
  le cas « la boucle d'actions du tour LIT le drapeau » tombe au rouge (« drapeau toujours à 1 ») ;
- trait `HOUNDS` (`card_face.py`), drapeaux (`player_flag.py`), `Puzzle.BeginPlayerTurn` et `Puzzle.FinDeTourSupplementaire` (`puzzle.py`, harnais).

Lecture de la substitution (`substituer_pack.py`, `rouges N/M`) : **16/16 modules** ont au moins un cas qui tombe au rouge sans eux, pack identique
avant/après. Les cas qui restent verts sans module sont des **valeurs imprimées**, des **contre-cas d'absence** ou des **témoins** (listés carte par carte).
Autoplay : 8 parties Rachel contre Rhino (1 victoire ; 5 « tous éliminés », 1 « Hound Program : les joueurs perdent », 1 « manigance accomplie »,
4,8 rounds), 0 erreur, 0 exception ; témoin `spider_man` 8 parties (0 victoire, 6,9 rounds), 0 erreur ; les 17 identifiants du pack
apparaissent dans les journaux ; « Additional turn » dans les 8 journaux. Deck : `DECK_NOM=rachel_summers` monte une partie (« identité rm001a, main 5, deck 10 »).

---

### rm001a : Marvel Girl (face héros)
- [x] Étape 2 : « After your turn begins » `22001a` Nebula / `03019` Quinjet (`AfterPlayerTurnBegin`) ; mélanger la main dans le deck `14007` (`Faces.ShuffleAllTo`) ;
      réduire le coût de la prochaine carte `05008` Nakia (`Worlds.UpdateNextCardPlayCost`, ici `in_this="Turn"`).
- [x] Étape 5 : mots-pièges : « shuffle your hand into your deck → draw a **new hand** » (coût puis effet, codé en une opération : on pioche jusqu'à la taille de main,
      `DrawUp("Max")`) ; « **this turn** » (le coût réduit ne vaut que pour la prochaine carte du tour) ; le nom « Chronoskimming » est LU par rm010.
- [x] Étape 6 : PV 10, ATQ 1, MEN 3, DÉF 2, taille de main 4 (scan) = `desc` = cas de valeurs imprimées. Vert.
- [x] Étape 7 : cas : valeurs ; remélange (7 cartes → 4 en main, 3 au deck) ; réduction du coût (main 4 → 2 contre 4 → 1 sans la Réponse) ; contre-cas alter ego (la
      Réponse est sur la face héros). Substitution : rouges 2/5 (verts : valeurs imprimées, 2 contre-cas).
- [x] Étape 7 bis : limite imprimée NON. Étape 8 : autoplay ci-dessus, la Réponse part à chaque début de tour héros. Étape 8 bis : NON.
Carte terminée : NON (provisoire) : partie réelle ; question 1.

### rm001b : Rachel Summers (face alter ego)
- [x] Étape 2 : `48001b` Kurt Wagner (`Search.PlayerCard` + `Faces.AddToHand`, Action).
- [x] Étape 5/6 : PV 10, REC 4, taille de main 5 ; MUTANT, PSIONIC. Résultat : vert.
- [x] Étape 7 : cas : valeurs ; Action (cherche Temporal Reversal, s'incline, le deck passe de 3 à 2) ; contre-cas sans copie (main vide, coût payé).
      Substitution : rouges 2/3 (vert : valeurs imprimées).
- [x] Étape 7 bis : NON. Étape 8 : autoplay. Étape 8 bis : NON.
Carte terminée : NON (provisoire) : partie réelle.

### rm002 : Captain Britain (Betsy Braddock)
- [x] Étape 2 : `22001a` (Réponse « après le début de votre tour »), `03003` (`GainUntilPhaseEnd`).
- [x] Étape 5/6 : coût 2, PV 3, ATQ 1*, MEN 1* ; « +1 ATK and +1 THW until the end of the phase ». Vert.
- [x] Étape 7 : cas : valeurs ; +1/+1 après `BeginPlayerTurn` ; contre-cas sans début de tour. Substitution : rouges 1/3 (verts : valeurs, contre-cas).
- [x] Étape 7 bis NON ; étape 8 autoplay ; étape 8 bis NON (alliée ordinaire).
Carte terminée : NON (provisoire) : partie réelle.

### rm003 : Askani's Prophecies
- [x] Étape 2 : `01025` Split Personality, `27032` Double Life (`ChangeToOtherForm`, `Faces.ReadyAll`), `16040` (`HealthUnits`).
- [x] Étape 5 : trois phrases EN ORDRE (redresser, soigner 1, changer de forme) ; l'identité se relit AVANT le changement. Vert.
- [x] Étape 6 : coût 2 (wild). Étape 7 : cas : 3 dégâts + incliné → 2 dégâts, prêt, face héros ; contre-cas face héros (injouable). Substitution : rouges 1/2 (vert : contre-cas).
- [x] Étape 7 bis NON ; étape 8 autoplay ; étape 8 bis NON.
Carte terminée : NON (provisoire) : partie réelle.

### rm004 : Black Hole
- [x] Étape 2 : `04036` Pheromones (`Faces.GiveStatus` « Stunned » et « Confused »), `18020` (`SetTarget` / `SetTarget2`), `us010` (sbires engagés).
- [x] Étape 5 : « a minion AND a villain » (deux ciblages) ; dégâts au méchant et à CHAQUE sbire engagé AVEC VOUS (liste sans doublon). Vert.
- [x] Étape 6 : coût 3 (mental). Étape 7 : cas : sbire + méchant sonnés, désorientés, 1 dégât chacun ; cas sans sbire (le méchant seul). Substitution : rouges 2/2.
- [x] Étape 7 bis NON ; étape 8 autoplay ; étape 8 bis NON.
Carte terminée : NON (provisoire) : partie réelle ; question 2.

### rm005 : Psionic Blasts (x2)
- [x] Étape 2 : `18020` Hit and Run (deux cibles, `SetLabel('attack', 'thwart')`), `16005` (`if_this_attack_defeats`), `RemoveThreatFromSchemes(.., if_this_remove_last_threat=)`.
- [x] Étape 5 : « to THE enemy » (imprimé) codé « un ennemi » ; DEUX pioches distinctes (ennemi vaincu, dernière menace). Vert.
- [x] Étape 6 : coût 2 (énergie), 3 dégâts, 3 menaces. Étape 7 : quatre cas (aucune pioche ; ennemi vaincu ; dernière menace ; les deux = 2 pioches). Substitution : rouges 4/4.
- [x] Étape 7 bis NON ; étape 8 autoplay ; étape 8 bis NON.
Carte terminée : NON (provisoire) : partie réelle ; question 3.

### rm006 : Telekinetic Counterblast (x2)
- [x] Étape 2 : `al014` Lurking (`heros.BasicAttack([cible], effect, property=AttackProperty(additional_value=N))`), `36012` (`AfterUnitAttackYou`).
- [x] Étape 5 : « that enemy » = l'attaquant ; « without exhausting » ; +3 ATQ pour CETTE attaque. Vert.
- [x] Étape 6 : coût 1 (physique). Étape 7 : cas : héros incliné pour ne pas défendre, Rhino attaque, 1 + 3 = 4 dégâts. Substitution : rouges 1/1.
- [x] Étape 7 bis NON ; étape 8 autoplay ; étape 8 bis NON.
Carte terminée : NON (provisoire) : partie réelle ; question 4.

### rm007 : Temporal Reversal (x2)
- [x] Étape 2 : `27032` Double Life (`.MaxOnePerRound()`) ; AUCUNE carte ne donne un tour de plus : MOTEUR (fiche `tour-supplementaire.md`).
- [x] Étape 5 : « after THIS one » (tour de plus juste après, avant le joueur suivant) ; les trois étapes se font à la fin du tour qui a joué la carte, dans l'ordre ;
      « Max 1 per round ». Vert.
- [x] Étape 6 : coût 0 (mental). Étape 7 : cas : le drapeau part (1) et la carte va à la défausse ; témoin d'épuisement ; les trois étapes (main 2 → 4, tout redressé ; main 6 → 4).
      Substitution : rouges 2/4 (verts : les deux cas des étapes de fin de tour, qui mesurent le MOTEUR et non le module).
- [x] Étape 7 bis : OUI, « Max 1 per round » : deux copies en main, une seule jouée (1 tour de plus + 0) ; drapeau lu : 1.
      **26/10/2026, multijoueur (RR « Max » : « across all copies of a card (by title) for all players »)** : le verdict de relecture annonçait un changement de code. MESURÉ :
      aucun n'est nécessaire. `LimitOncePerRound` compte l'objet `Ability`, partagé par toutes les copies de la carte, quel que soit le joueur : le joueur 1 joue
      sa Temporal Reversal, la limite du round est CONSOMMÉE pour la copie que le joueur 2 tient en main (cas `rm007 ... vaut pour TOUS les joueurs`, clé de vérification
      `rm_limite_round` qui lit `world.stat.IsOncePerRound` sur la capacité de la copie du joueur 2). Mesure calibrée par un TÉMOIN (sans première résolution, la limite est LIBRE).
      Ces deux cas sont VERTS d'emblée : ils ne sont donc pas passés par le rouge (le comportement était déjà conforme) ; la mesure, elle, a été vue prendre les deux valeurs.
- [x] Étape 8 : autoplay : « Additional turn » dans 8/8 parties ; journal lu (fin de tour, pioche, redressement, tour de plus, Chronoskimming repart). Mutation : 0/3 sans la boucle.
- [x] Étape 8 bis NON.
Carte terminée : NON (provisoire) : partie réelle. (Question 5 tranchée le 26/10/2026 : A confirmé ; « Max » multijoueur déjà conforme, voir ci-dessus.)

### rm008 : Askani (amélioration, titre)
- [x] Étape 2 : `14007` (`Faces.ShuffleAllTo`), `35006` / `03008` (`WhenUnitWouldBeDefeated` + `SetBeInstead` + `SetHealth(1)`).
- [x] Étape 5 : « the TOP three » = les trois dernières entrées de la défausse ; « When YOU would be defeated » (l'identité, toute cause). Vert.
- [x] Étape 6 : coût 3 (énergie). Étape 7 : cas : Action (le fond de la défausse reste, trois cartes au deck) ; Interruption mortelle (PV 1, Askani défaussée) ;
      contre-cas non mortel. Substitution : rouges 2/3 (vert : contre-cas).
- [x] Étape 7 bis NON ; étape 8 autoplay ; étape 8 bis NON.
Carte terminée : NON (provisoire) : partie réelle ; question 6.

### rm009 : Psionic Shield
- [x] Étape 2 : `01028` (`GiveKeywordToAttached(CardFinder(name=..))`), `09020` Unflappable (`AfterUnitDefendAgainstAttack(.., take_no_damage=True)`).
- [x] Étape 5 : « and take no damage » ; « that enemy » = l'attaquant. Vert.
- [x] Étape 6 : coût 2 (énergie), +2 DÉF. Étape 7 : cas : +2 DÉF ; défense sans dégât → Rhino désorienté, bouclier incliné ; contre-cas héros incliné. Substitution : rouges 2/3 (vert : contre-cas).
- [x] Étape 7 bis NON ; étape 8 autoplay ; étape 8 bis NON.
Carte terminée : NON (provisoire) : partie réelle.

### rm010 : Temporal Retrieval (x2)
- [x] Étape 2 : `27003` Parental Guidance (`PlaceCardHere(.., False, effect)`), `us006` (`AfterCardResolveAbility(.., ability_name=)`), `AfterPlayerPlayedCard`.
- [x] Étape 5 : « to a maximum of 3 » ; « Chronoskimming » (nom de rm001a) ; « discard this card → put each card attached... » : on reprend les cartes AVANT de défausser. Vert.
- [x] Étape 6 : coût 1 (énergie). Étape 7 : cas : attacher ; Action offerte à 2 / plus offerte à 3 ; Réponse après Chronoskimming ; Réponse après une carte TEMPORAL ; contre-cas non TEMPORAL.
      Substitution : rouges 4/6 (verts : témoin « à 3, plus offerte » et contre-cas, absences).
- [x] Étape 7 bis : OUI, « maximum of 3 » : témoin d'épuisement (2 attachées → offerte, 3 → non).
- [x] Étape 8 : autoplay. Étape 8 bis : OUI (cartes attachées sous une amélioration attachée à l'identité) : cas plateau `rachel-summers-plateau.test.ts`
      (vert d'emblée : le correctif générique `zones.ts` du 09/09/2026 était déjà en place, pas de « vu rouge » possible).
Carte terminée : NON (provisoire) : partie réelle ; question 7.

### rm011 : Telekinetic Axe
- [x] Étape 2 : `10003` Hulk Smash (`WhenUnitMakeAttack(HeroInterrupt, "You", .., is_basic_attack=True)` + `GainOverKill`), `27187a` (`SetTarget("Attacked")`).
- [x] Étape 5 : Restreint (`desc`) ; « overkill ET stun » ; pas de filtre `canbe_stunned`. Vert.
- [x] Étape 6 : coût 3 (physique), +1 ATQ. Étape 7 : cas : +1 ATQ ; overkill (1 PV restant, 1 dégât au méchant) ; étourdi ; contre-cas hache inclinée. Substitution : rouges 3/4 (vert : contre-cas).
- [x] Étape 7 bis NON ; étape 8 autoplay ; étape 8 bis NON.
Carte terminée : NON (provisoire) : partie réelle ; question 8.

### rm012 : Telekinetic Sword
- [x] Étape 2 : `01039` (`GiveKeywordToAttached("You", health=N)`), `uw010` (`UnitAttackGainKeyword("You", piercing=True)`).
- [x] Étape 5 : « Marvel Girl ATTACKS gain piercing » = toutes ses attaques ; « after you attack ». Vert.
- [x] Étape 6 : coût 3 (physique), +3 PV. Étape 7 : cas : +3 PV ; perçant (le sbire robuste prend 1 dégât) ; contre-cas sans épée ; pioche + inclinée. Substitution : rouges 3/4 (vert : contre-cas).
- [x] Étape 7 bis NON ; étape 8 autoplay ; étape 8 bis NON.
Carte terminée : NON (provisoire) : partie réelle ; question 9.

### rm013 : Memory From The Future (obligation)
- [x] Étape 2 : `sf010` Shame / `st005b` (`GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1)`), `PlayerActionToDiscardThis(.., ex_operation=)` ; « end this turn » : MOTEUR.
- [x] Étape 5 : `effect.GetInitiator()` d'une Action de joueur est le JOUEUR ; « discard this obligation » (défausse rencontre). Vert.
- [x] Étape 6 : boost 2. Étape 7 : cas : −1 taille de main ; Action (défaussée, Rachel inclinée, drapeau posé) ; la boucle d'actions LIT le drapeau ; contre-cas face héros. Substitution : rouges 3/4 (vert : contre-cas).
      Mutation moteur : boucle désactivée → rouge.
- [x] Étape 7 bis NON ; étape 8 autoplay (apparue dans les journaux : 32 lignes) ; étape 8 bis NON.
Carte terminée : NON (provisoire) : partie réelle ; question 10.

### rm014 : Hound Program (manigance annexe, nemesis)
- [x] Étape 2 : `Worlds.SetGameOver(False, effect)` (`27102b`), `this.PlaceThreatOnSchemes([this], n, effect)`, `AfterPlayerTurnBegin`, `Permanent` (`40105a`).
- [x] Étape 5 : « Hero Response » imprimé sur une carte de rencontre : codé en Réponse FORCÉE (sinon jamais déclenchée) ; seulement au tour de Marvel Girl en forme héros ; « at least 5 ». Vert.
- [x] Étape 6 : menace de départ 1, boost 3. Étape 7 : cas : valeurs ; +1 (1 → 2) ; contre-cas alter ego ; témoin 4 → 5 (les joueurs perdent) ; témoin 3 → 4 (la partie continue).
      Substitution : rouges 3/5 (verts : valeurs, contre-cas).
- [x] Étape 7 bis NON. Étape 8 : autoplay : 43 lignes ; une partie sur huit perdue sur « Hound Program ». Étape 8 bis : OUI (menace sur la manigance) : cas plateau.
Carte terminée : NON (provisoire) : partie réelle ; question 11.

### rm015 : Ahab (sbire nemesis) : AUCUN MODULE
- [x] Étape 2 : Ténacité et Vilenie lues dans `desc` (`toughness.md`, `villainous.md`). Étape 5/6 : PV 5, ATQ 3, SCH 2, boost 2 ; ELITE, CYBORG, HOUNDS.
- [x] Étape 7 : un cas de valeurs imprimées (PV, ATQ, SCH, Vilenie, traits, carte d'état Tenace à l'entrée en jeu) : vert. Pas de substitution possible (aucun script).
- [x] Étape 8 : autoplay : 86 lignes. Étape 8 bis NON.
Carte terminée : NON (provisoire) : partie réelle.

### rm016 : Hound Clothes (x3)
- [x] Étape 2 : `32150` Wrapped in Metal, `16123` (attachement à l'identité, `GiveKeywordToAttached("Character", ..)`), `01163` (`if_cannot_gain_surge`), `27154` (boost : `GetToPlayer().DiscardRandomHandCards`).
- [x] Étape 5 : « Max 1 per **identity** » (`desc.MaxPerUnit`) ; « −1 hand size » pour l'identité porteuse ; la Hero Action exige la forme héros. Vert.
- [x] Étape 6 : boost 1 + ★. Étape 7 : cas : attachée, −1 taille de main ; seconde copie non attachée ; Hero Action (défaussée, identité inclinée, taille de main rétablie) ; contre-cas alter ego ; ★ Boost (2 → 1 carte).
      Substitution : rouges 5/5.
- [x] Étape 7 bis NON. Étape 8 : autoplay (16 lignes). Étape 8 bis : OUI (attachement à l'identité) : cas plateau.
Carte terminée : NON (provisoire) : partie réelle ; question 12.

---

## Questions en attente (option A = celle qui est codée)

> **26/10/2026 : TOUTES TRANCHÉES** (règles + scans, `VERDICTS-REGLES-2026-10-26.md`) : option A confirmée partout. Point 11 (rm014 Hound Program, « Hero Response »)
> : DÉCISION UTILISATEUR du 26/10/2026 : Réponse forcée, en forme héros (déjà codée). Point 5 : « Max 1 per round » multijoueur déjà conforme (mesuré).
> Le texte ci-dessous est conservé pour mémoire.
1. **rm001a Chronoskimming** : la Réponse est-elle offerte quand la main est VIDE (A : oui, on pioche alors une main entière) ou seulement avec au moins une carte à remélanger (B) ?
   « Draw a new hand » : A jusqu'à la taille de main ; B autant de cartes que celles remélangées.
2. **rm004 Black Hole** : sans sbire en jeu, la carte est jouable et agit sur le méchant seul (A : choix du moteur) ou injouable (B : « a minion and a villain » exige les deux) ?
3. **rm005 Psionic Blasts** : « Deal 3 damage to THE enemy » (imprimé) : A un ennemi au choix ; B le même ennemi que celui d'une autre étape (sans objet ici : il n'y a qu'une cible). Lecture codée A.
4. **rm006 Telekinetic Counterblast** : le héros peut-il contre-attaquer INCLINÉ (A : oui, « without exhausting » : le moteur n'exige pas qu'il soit prêt) ou seulement prêt (B) ?
5. **rm007 Temporal Reversal** : les trois étapes se font à la fin du tour qui joue la carte (A) ou à la fin du tour supplémentaire (B) ? « Max 1 per round » : par joueur (A) ou
   pour toute la table (B) ? Les capacités « après le début de votre tour » repartent au tour de plus (A).
6. **rm008 Askani** : moins de trois cartes en défausse : on les remélange toutes (A) ; l'Interruption vaut sous les deux formes (A) ou seulement en forme héros (B).
7. **rm010 Temporal Retrieval** : si la carte quitte le jeu autrement (défausse par un effet), les cartes attachées vont à la défausse du propriétaire (A : comportement du moteur, non codé) ou
   reviennent en main (B) ? Sa propre mise en jeu (elle a le trait TEMPORAL) offre sa Réponse (A, inoffensive : rien d'attaché) ou non (B).
8. **rm011 Telekinetic Axe** : « stun the attacked enemy » alors qu'il est déjà sonné : l'Interruption reste offerte (A : pas de filtre, le overkill est conservé) ou non (B).
9. **rm012 Telekinetic Sword** : « Marvel Girl attacks gain piercing » : toutes les attaques (A) ou seulement les attaques de base (B).
10. **rm013 Memory From The Future** : « end this turn » termine le tour immédiatement, les autres actions du tour sont perdues (A) ; autre lecture : ne s'applique qu'à la fin de l'action en cours (B).
11. **rm014 Hound Program** : « Hero Response » imprimé : codé FORCÉ (A) ou facultatif (B : le joueur ne le déclencherait jamais) ; au 5e jeton la défaite est immédiate (A).
12. **rm016 Hound Clothes** : « −1 hand size » vaut sous les deux formes de l'identité (A) ; la seconde copie gagne Renfort (A).
13. **Icônes de ressource** (en bas à gauche de chaque carte) lues à l'œil et comparées à des cartes officielles, sans découpe pixel par pixel : rm002 et rm003 = wild, rm004 et rm007 = mental,
    rm005, rm008, rm009 et rm010 = énergie, rm006, rm011 et rm012 = physique. À confirmer sur écran.

## À vérifier en partie réelle
- une partie complète avec Marvel Girl choisie dans la liste Fan-made ;
- Temporal Reversal : le tour supplémentaire à l'écran (onglet du joueur, pioche, redressement, retour de Chronoskimming) ;
- Memory From The Future : le tour se termine bien à l'écran ;
- les 17 images à l'écran (Hound Program est en paysage), la biographie au survol dans l'assistant ;
- Temporal Retrieval : cartes attachées face cachée lisibles par leur propriétaire ;
- les icônes de ressource (question 13) et le boost de Hound Clothes.
