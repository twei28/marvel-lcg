# TMNT Shinobi, les 20 Ninjutsu (`sa001`-`sa020`) : gabarits PROCESSUS-CARTE (17/10/2026)

Pack `tmnt_shinobi_ninjutsu` (set « TMNT Shinobi Ninjutsu », `desc.Class = "Ninjutsu"`, Inkwire). Scans : `Ninjutsu/N1..N20` du zip (relus un par un, texte et
icônes). Classement contre les officielles : **NOUVELLE** pour les 20 (aucun texte identique à une officielle : pas d'art alternatif à convertir). Homonyme
confirmé sur le scan : `sa008` Smoke Bombs ≠ `27139` Smoke Bombs (Goblin Gear : ATTACHEMENT du vilain à « bomb counters », aucun rapport). Aucune coquille de
crédit (les 20 impriment « TMNT Shinobi By: Inkwire »). Icônes de ressource vérifiées contre des scans du même éditeur (`tj005`/`tj004`/`tj009` : B/R/Y ;
`ub017`/`ub031` : étoile verte = G ; `up007` : étoile des dégâts consécutifs = « 1* »), jamais à vue.
Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_shinobi_ninjutsu.py` (filtre `[sa] saNNN`, **149 cas**), cas plateau : `ui-app/src/board/tmnt-shinobi-ninjutsu-plateau.test.ts`
(13 tests). Questions : `.planning/tmnt/shinobi-ninjutsu-questions.md` (Q-N1, Q-N2, Q-N3). Fiches ajoutées : `shadow-counter.md`, `smoke-counter.md` ; `cloak.md` complétée.

**Preuve par substitution** (script jetable du 17/10/2026 : module remplacé par `GetAbilities -> []`, cas `[sa] saNNN` relancés, module restauré) : rouges / verts sans module,
par carte : sa001 3/3, sa002 3/3, sa003 6/1, sa004 2/2, sa005 3/2, sa006 5/0, sa007 8/4, sa008 4/4, sa009 7/2, sa010 5/5, sa011 5/2, sa012 2/2, sa013 3/5, sa014 4/5, sa015 5/3,
sa016 6/0, sa017 4/2, sa018 5/4, sa019 3/3, sa020 1/3. Les cas qui restent VERTS sans module sont des témoins d'ABSENCE (carte non jouable faute de condition, action
non proposée, effet non déclenché pour une autre carte / un autre joueur / une autre forme) ou portent sur des bases NATIVES du moteur (`Uses`, `MaxPerUnit`, `Restricted`,
« Max 1 TRAINING per ally », « Max 1 per deck »), assumés : voir carte par carte. Mutation supplémentaire : `sa001` sans `AttackProperty(piercing=True)` -> le cas du
sbire Coriace redevient ROUGE. Gates : `verifier_appels_modules.py` sur le pack = OK, calibré (un appel inexistant ajouté à `sa015` est trouvé, puis retiré) ;
`verifier_prefixes.py` vert ; `test_cards.py` : 6725 ok / 0 err (les 20 cartes construisent).

Étape 8 (autoplay ciblé) : **NON faite sur les 20 cartes** (consigne : pas de batterie ; aucun deck de test ne contient encore de carte Shinobi portée, le deck-builder des
Paths n'est pas branché sur un deck d'autoplay). Étape 8 bis : voir chaque carte ; cas plateau commun en fin de document.

Éléments communs : « Play only if your hero is cloaked » = `JouableSiHerosCamoufle` (identité en forme HÉROS portant une carte Cloaked) ; coûts « discard a cloaked status card
from ... » = `CoutDefausserCloaked` (`CostFunc.Custom(CardFinder(has_status="Cloaked", ...), DiscardCloaked)`, modèle `sk049`) ; « Cloak a character you control → » = `CoutCamoufler`.
Règles Cloaked du livret p.8 prouvées en jeu : un seul Cloaked par personnage, Solide/Steady n'y change rien (« Can I put 2 Cloaked on a steady character ? No » : une seule carte
posée même déjà présente), Coriace avant Cloaked, +2 DEF de la défense puis la carte part avant l'excédent (`sa002`), les dégâts consécutifs résolvent après le +2 ATQ (`sa017`).

### sa001 : Assassinate (Événement 2, Ninjutsu, ATTACK) : Hero Action (Q-N1)
- [x] Étape 2 : `04044` Piercing Strike (`hero.DealDamage(..., AttackProperty(piercing=True))`, `.SetPlay().SetLabel('attack')`) ; `JouableSiVousControlez` (condition de jeu en tête) ; `08003` (Action nue, plus utilisée : Q-N1 → Hero Action).
- [x] Étape 5 : « YOUR HERO is cloaked » (forme héros) ; « Hero Action » (le scan imprime « Action » : coquille, l'utilisateur a répondu Hero Action, Q-N1) ; « 7 damage to a MINION » ; « gains piercing ». Résultat : texte = code.
- [x] Étape 6 : 7 dégâts, coût 2 (desc et script). Conforme.
- [x] Étape 7 : 6 cas (sbire vaincu ; sbire Coriace vaincu grâce au piercing ; héros non camouflé / alter-ego camouflé / sans sbire : injouable ; témoin jouable). Rouges sans module 3/6 ; verts = 3 injouables.
- [x] Étape 7 bis : limite imprimée ? NON. [ ] Étape 8 : non faite. [x] Étape 8 bis : NON (dégâts).
- [x] Réponse Q-N1 (réponse du 17/10/2026, `shinobi-reponses.md`) : script en `AbilityType.HeroAction`, `cards.json` et FR « Hero Action » / « Action de héros » ; +1 cas (type de capacité = HeroAction, vérificateur `sn_type_capacite_main`) : 7 cas, substitution (ancien script) : 6/7 donc le nouveau cas rougit.

Carte terminée : **OUI**.

### sa002 : Shroud and Protect (Événement 1, DEFENSE) : terminée
- [x] Étape 2 : `14014` Never Back Down (même déclencheur, `IfYouTakeNoDamage`), `09015` (redresser le héros), `up023` (Cloak).
- [x] Étape 5 : « +1 DEF for THAT attack » ; « If you take NO damage » ; « cloak AND ready your hero » ; Hero Interrupt ; « When YOU defend ». Résultat : conforme.
- [x] Étape 6 : +1, coût 1. Conforme.
- [x] Étape 7 : 6 cas (ATQ 4 contre DEF 4 : 0 dégât, camouflé ET redressé ; témoin sans la carte : 1 dégât ; ATQ 5 : 1 dégât, ni Cloaked ni redressement ; héros déjà camouflé : +2 DEF puis une seule carte ;
  alter-ego et allié défenseur : non jouée). Rouges sans module 3/6.
- [x] Étape 7 bis : NON. [ ] Étape 8 : non faite. [x] Étape 8 bis : statut posé (badge déjà couvert, `tmnt-shinobi-ninjutsu-plateau.test.ts` « Cloaked »).
Carte terminée : **OUI**.

### sa003 : Reconnaissance (Événement 1, TACTIC) : terminée
- [x] Étape 2 : `27043` Global Logistics (regarder N cartes d'un deck joueur ou rencontre, `PlaceOnTopAndOrBottomInAnyOrder`, `SetTarget(from_where=[PlayersDeckTop, EncounterDeckTop])`) ; `sk049` (coût Custom).
- [x] Étape 5 : coût « Cloak a character you control → » (payé avant, personnage sans Cloaked) ; « a PLAYER deck OR encounter deck » (un seul) ; « those cards » (toutes remises). Résultat : conforme.
- [x] Étape 6 : 3 cartes, coût 1. Conforme.
- [x] Étape 7 : 7 cas (deck rencontre : héros camouflé, 3 vues, dessus/dessous mesurés ; deck du joueur ; deck d'un AUTRE joueur ; alter-ego camouflé ; héros déjà camouflé : coût payé par l'allié ; injouable si tous camouflés ; jouable sinon). Rouges sans module 6/7.
  ⚠ Harnais : le pilote ne sait pas ordonner deux cartes de MÊME card_id (« Place on bottom » échoue) : les decks de test ont des identifiants distincts.
- [x] Étape 7 bis : NON. [ ] Étape 8 : non faite. [x] Étape 8 bis : statut posé (badge couvert).
Carte terminée : **OUI**.

### sa004 : Scale the Wall (Événement 0) : terminée
- [x] Étape 2 : `vz014` Scared of the Dark (« Max 1 per round » = `LimitOncePerRound`) ; `JouableSiVousControlez` ; `DrawUp`.
- [x] Étape 5 : « YOUR HERO is cloaked » (sans dépense de la carte) ; « Max 1 PER ROUND » ; « Draw 2 ». Résultat : conforme.
- [x] Étape 6 : pioche 2, coût 0. Conforme.
- [x] Étape 7 : 4 cas (héros camouflé : +2 cartes, Cloaked conservé ; héros non camouflé / alter-ego : injouable ; **témoin d'épuisement** ci-dessous). Rouges sans module 2/4.
- [x] Étape 7 bis : limite imprimée OUI (« Max 1 per round ») : deux copies en main, la 1re jouée (main = 1 copie + 2 piochées = 3), la 2e : jouable = False au second déclenchement du même round.
- [ ] Étape 8 : non faite. [x] Étape 8 bis : NON.
Carte terminée : **OUI**.

### sa005 : Run the Rooftops (Événement 0, NYC THWART) : terminée
- [x] Étape 2 : `10019` To the Rescue! (même effet) ; `JouableSiVousControlez`.
- [x] Étape 5 : « YOUR HERO is cloaked » ; « 2 threat from A scheme » (principal, annexe ou autre). Résultat : conforme.
- [x] Étape 6 : 2 menaces, coût 0. Conforme.
- [x] Étape 7 : 5 cas (principal 5 -> 3 ; complot annexe de 2 menaces vaincu ; 4 -> 2 exactement ; non camouflé / alter-ego : injouable). Rouges sans module 3/5.
- [x] Étape 7 bis : NON. [ ] Étape 8 : non faite. [x] Étape 8 bis : NON (menace chiffrée).
Carte terminée : **OUI**.

### sa006 : Cut-and-Run (Événement 2, ATTACK TACTIC) : terminée
- [x] Étape 2 : `35018` Precision Strike (dégâts puis `IsDefeated()`), `up023` (Cloak).
- [x] Étape 5 : « 4 damage to AN ENEMY » ; « If this attack DEFEATS an enemy » (vaincu par ces dégâts) ; « cloak YOUR HERO ». Résultat : conforme.
- [x] Étape 6 : 4 dégâts, coût 2. Conforme.
- [x] Étape 7 : 5 cas (sbire de 3 PV vaincu : camouflé ; sbire de 4 PV pile : camouflé ; vilain non vaincu : 4 dégâts, pas de Cloaked ; sbire Coriace : survit, pas de Cloaked ; héros déjà camouflé : une seule carte). Rouges sans module 5/5.
- [x] Étape 7 bis : NON. [ ] Étape 8 : non faite. [x] Étape 8 bis : statut posé (badge couvert).
Carte terminée : **OUI**.

### sa007 : ✦ Hamato Clan (Soutien unique 2, TEAM) : terminée
- [x] Étape 2 : `27023` (« After an ally leaves play » = `AfterCardLeavePlay(Response, Ally, ...)`) ; `tj006` (deux coûts chaînés Exhaust + Counter) ; fiche `shadow-counter.md`.
- [x] Étape 5 : « an ally YOU CONTROL » ; « leaves play » (défaite, défausse...) ; « place 1 shadow counter HERE » ; « Exhaust AND remove 1 shadow counter » ; « cloak AN ALLY you control ». Résultat : conforme.
- [x] Étape 6 : 1 compteur, coût 2. Conforme.
- [x] Étape 7 : 12 cas (défausse, défaite, 2 alliés : 2 compteurs ; témoins : allié d'un autre joueur, sbire ; Action : 1 compteur retiré, allié camouflé ; sans compteur / sans allié : non proposée ; alter-ego : proposée). Rouges sans module 8/12 ; verts : 4 absences.
- [x] Étape 7 bis : limite imprimée ? NON (l'inclinaison fait la limite) : témoin d'épuisement : 2 compteurs, un usage, puis 0 action disponible.
- [ ] Étape 8 : non faite. [x] Étape 8 bis : OUI (compteur `shadow`) : cas plateau (compteur dessiné, libellé « ombre », vu ROUGE sans la ligne `compteurs-fr.ts`).
Carte terminée : **OUI**.

### sa008 : Smoke Bombs (Amélioration 1, ITEM) : terminée
- [x] Étape 2 : `tj006` (Uses + Exhaust + Counter) ; `up023` (`CanPlayThisUpgradeCard()`) ; `td005`/`SetTarget(Friend)`. Fiche `smoke-counter.md`.
- [x] Étape 5 : « Uses (2 smoke counters) » (natif) ; « Max 1 per player » (`MaxPerUnit`) ; deux coûts ; « a FRIENDLY character » (héros ou allié, jamais un ennemi). Résultat : conforme. Homonyme `27139` confirmé distinct.
- [x] Étape 6 : 2 compteurs, 1 compteur retiré, coût 1, MaxPerUnit 1. Conforme.
- [x] Étape 7 : 8 cas (2 compteurs à l'entrée ; Max 1 : 2e copie injouable (chiffre jouable=False) / témoin jouable ; Action : héros camouflé, compteur 2 -> 1, inclinée ; allié camouflé ; deux usages : la carte part (Uses) ; épuisement ; alter-ego : non proposée). Rouges sans module 4/8 ; verts : Uses et Max natifs, témoins.
- [x] Étape 7 bis : limite imprimée OUI (« Max 1 per player ») : témoin ci-dessus ; usage limité par Uses (2) : cas « deux usages » ; épuisement : 0 action après usage.
- [ ] Étape 8 : non faite. [x] Étape 8 bis : OUI (compteur `smoke`, statut) : cas plateau.
Carte terminée : **OUI**.

### sa009 : ✦ Twilight Sentry (Amélioration unique 1, TITLE TRAINING) : ordre du moteur conservé (Q-N3)
- [x] Étape 2 : `ua004` (attache + « Max 1 TRAINING per ally » natif) ; `dt088` (Forced Response à la pose pour poser un statut) ; `19032`/`27087b` (« instead » = `SetBeInstead`).
- [x] Étape 5 : « an ally YOU CONTROL » ; « and cloak THEM » (à la pose) ; « Max 1 TRAINING upgrade per ally » ; « Interrupt » (pas Hero) ; « WOULD take ANY amount » ; « discard a cloaked status card INSTEAD ». Résultat : conforme ; Q-N3 résolue (ordre du moteur conservé).
- [x] Étape 6 : coût 1. Conforme.
- [x] Étape 7 : 9 cas (pose : allié camouflé et amélioration attachée ; aucun allié / allié d'un autre joueur : injouable ; allié contrôlé : jouable ; allié déjà entraîné : injouable ; comportement retenu Q-N3 : le statut résout avant l'Interruption ; témoins). Rouges sans module 7/9.
  Q-N3 (réponse du 17/10/2026, `shinobi-reponses.md`) : ordre du moteur conservé, aucune extension : la carte ne sert qu'à camoufler l'allié à la pose ; l'Interruption n'est en pratique jamais proposée (statut Cloaked avant Interruption). Le cas « comportement retenu » le prouve.
- [x] Étape 7 bis : NON. [ ] Étape 8 : non faite. [x] Étape 8 bis : OUI (amélioration sur un allié, statut) : cas plateau.
Carte terminée : **OUI**. Non prouvé : l'Interruption elle-même (jamais proposée, par choix de l'utilisateur).

### sa010 : Opportunist (Amélioration 2, SKILL) : terminée
- [x] Étape 2 : `sk049` (coût sur un personnage + `DiscardTough`), `tj006` (Exhaust), `10019` (retrait de menace).
- [x] Étape 5 : « from a character YOU CONTROL » ; deux coûts ; « 3 threat from A scheme » ; Max 1 per player. Résultat : conforme.
- [x] Étape 6 : 3 menaces, coût 2, MaxPerUnit 1. Conforme.
- [x] Étape 7 : 10 cas (carte du héros ; carte d'un allié ; complot annexe vaincu ; sans Cloaked / Cloaked d'un autre joueur / alter-ego : non proposée ; Max 1 ; positif). Rouges sans module 5/10 ; verts : absences et Max natif.
- [x] Étape 7 bis : OUI (Max 1 per player, témoin) ; épuisement : un usage puis 0 action malgré un Cloaked restant.
- [ ] Étape 8 : non faite. [x] Étape 8 bis : NON (menace, statut déjà couvert).
Carte terminée : **OUI**.

### sa011 : Stealth Proficiency (Événement 0) : terminée
- [x] Étape 2 : `sk049`/`CoutDefausserCloaked` ; `09015` (redresser le héros) ; `su009` (`AfterUnitUseBasicPower`) ; `up023`.
- [x] Étape 5 : deux capacités sur un événement ; « discard a cloaked status card FROM YOUR HERO » (coût) ; « After YOU use ONE OF YOUR basic powers » (ATQ, CTR, DEF). Résultat : conforme.
- [x] Étape 6 : coût 0. Conforme.
- [x] Étape 7 : 7 cas (Action : héros incliné redressé, Cloaked défaussé ; héros non camouflé : non jouable ; Réponse après ATQ, CTR, DEF ; allié : pas « you » ; héros déjà camouflé : +2 consommé puis une seule carte). Rouges sans module 5/7.
- [x] Étape 7 bis : NON. [ ] Étape 8 : non faite. [x] Étape 8 bis : statut (badge couvert).
Carte terminée : **OUI**. Non prouvé : la Réponse en alter-ego (aucun pouvoir de base d'alter-ego atteignable par l'API).

### sa012 : Black Ops (Amélioration 1) : Hero Response (Q-N2)
- [x] Étape 2 : `se008` Onigari (« After you defeat a minion OR side scheme », deux capacités), `13017`/`up023` (coût `Discard("This")`), `09015`.
- [x] Étape 5 : « Hero Action: After ... » est contradictoire (Q-N2) ; « After YOUR HERO defeats » ; « minion or side scheme ». Résultat : Hero Response, confirmée par l'utilisateur (Q-N2, 17/10/2026).
- [x] Étape 6 : coût 1. Conforme.
- [x] Étape 7 : 4 cas (sbire vaincu : redressé, carte défaussée ; complot annexe vaincu ; sbire non vaincu ; allié qui vainc). Rouges sans module 2/4.
- [x] Étape 7 bis : NON. [ ] Étape 8 : non faite. [x] Étape 8 bis : NON.
Carte terminée : **OUI**. Q-N2 (réponse du 17/10/2026, `shinobi-reponses.md`) : Hero Response confirmée.

### sa013 : Up in Smoke (Événement 0, TACTIC) : terminée
- [x] Étape 2 : `vz015` (redresser, `canbe_ready`), `19032` Regroup (`Faces.ReturnToHand(.., "Owner")`), `27087b` (`WhenCardWouldDiscard` + `SetBeInstead`).
- [x] Étape 5 : deux capacités ; « a NINJA ally » ; « WOULD be discarded FROM PLAY » ; « return it to its OWNER'S hand INSTEAD ». Résultat : conforme.
- [x] Étape 6 : coût 0. Conforme.
- [x] Étape 7 : 8 cas (redresser un NINJA ; allié non NINJA : non ; allié vaincu -> main ; défaussé par un effet -> main ; témoin sans la carte : défausse ; sbire ; allié défaussé de la main ; alter-ego). Rouges sans module 3/8.
- [x] Étape 7 bis : NON. [ ] Étape 8 : non faite. [x] Étape 8 bis : changement de zone (allié -> main) : zones de base couvertes par `zones.ts`.
Carte terminée : **OUI**. Non prouvé : « owner's hand » quand le contrôleur n'est pas le propriétaire (aucun cas à deux joueurs).

### sa014 : ✦ Hidden Passage (Soutien unique 1, LOCATION NYC SEWERS) : terminée
- [x] Étape 2 : `ub058` (Alter-Ego Action + Exhaust), `13033`/`56043` (« After you change form » : `AfterUnitChangeForm`), `CoutDefausserCloaked("identity")`.
- [x] Étape 5 : « from your IDENTITY » (les deux formes) ; deux coûts ; Hero Response « After you change form » (précédent officiel `13033`, `21022` : part après le passage en forme héros). Résultat : conforme.
- [x] Étape 6 : pioche 1, coût 1. Conforme.
- [x] Étape 7 : 9 cas (Action alter-ego ; non camouflée / forme héros : non proposée ; épuisement ; positif ; Réponse après passage en héros ; passage en alter-ego : non ; déjà inclinée : non ; déjà camouflée : une seule). Rouges sans module 4/9.
- [x] Étape 7 bis : NON (inclinaison) : témoin d'épuisement : 0 action après usage. [ ] Étape 8 : non faite. [x] Étape 8 bis : statut (badge couvert).
Carte terminée : **OUI**.

### sa015 : ✦ Kusari-Kagi (Amélioration unique 1, NINJA WEAPON) : terminée
- [x] Étape 2 : `17007` Element Gun (Restricted + Hero Action + Exhaust), `sk049`/`CoutDefausserCloaked("hero")`, `DrawUp`.
- [x] Étape 5 : « Restricted » (natif) ; deux coûts, Cloaked de VOTRE HÉROS ; « 1 damage to AN ENEMY AND draw 1 ». Résultat : conforme.
- [x] Étape 6 : 1 dégât, 1 carte, coût 1, Restricted 1. Conforme.
- [x] Étape 7 : 8 cas (sbire : 1 dégât + 1 carte ; sbire vaincu : carte piochée quand même ; vilain ; Cloaked sur un allié / héros sans Cloaked / alter-ego : non proposée ; épuisement ; positif). Rouges sans module 5/8.
- [x] Étape 7 bis : NON (inclinaison) : témoin d'épuisement : 0 action. [ ] Étape 8 : non faite. [x] Étape 8 bis : NON.
Carte terminée : **OUI**. Non prouvé : la limite « Restricted » (2 cartes Restricted) : base native, aucun cas dans ce pack.

### sa016 : Shadow Summon (Événement 1, TACTIC) : terminée
- [x] Étape 2 : `22009` Combat Ready (`DiscardDeckUntil` + `PutIntoPlay`), `ul035` (fin de phase : `RunAt.TheEndOfThePhase` + `GainCard`).
- [x] Étape 5 : « Discard ... UNTIL you discard a NINJA ALLY and put it INTO PLAY » ; « STILL IN PLAY at the END OF THE PHASE, add it to YOUR HAND ». Résultat : conforme.
- [x] Étape 6 : coût 1. Conforme.
- [x] Étape 7 : 6 cas (jusqu'à l'allié NINJA ; fin de phase : en main ; allié parti avant : reste en défausse ; allié non NINJA défaussé sans être joué ; aucun NINJA : rien en jeu ; alter-ego). Rouges sans module 6/6.
  ⚠ Moteur : sans allié NINJA, la défausse est remélangée au deck (`DiscardUntil`, commun à `22009`) : seul « rien n'entre en jeu » est mesuré.
- [x] Étape 7 bis : NON. [ ] Étape 8 : non faite. [x] Étape 8 bis : changement de zone (deck -> défausse -> jeu -> main) : zones de base.
Carte terminée : **OUI**.

### sa017 : ✦ Moja (Allié unique 3, NINJA TURTLE ; THW 1*, ATQ 1*, PV 3) : terminée
- [x] Étape 2 : `up024`/`ud004` (« After X enters play, cloak X »), `ud003` (`AfterAllyTakeConsequentialDamage`), `se005` (`Select.From("YourHandCards", finder=CarteShinobi(...))` dans `CostFunc.Discard`).
- [x] Étape 5 : deux Réponses ; « takes consequential damage » (réellement subis) ; « discard a NINJUTSU card FROM YOUR HAND → » (Dual et signature Ninjutsu comptent) ; « cloak Moja ». Résultat : conforme.
- [x] Étape 6 : coût 3, PV 3, ATQ 1*, CTR 1*. Conforme.
- [x] Étape 7 : 6 cas (entrée en jeu : camouflée ; 3 PV : 2 dégâts ; dégâts consécutifs (1 par étoile) : défausse tj005 (Ninjutsu) et camouflée ; Taijutsu seule : non proposée ; déjà camouflée : +2 ATQ puis dégât consécutif plein puis nouvelle carte (livret p.8) ; Coriace : rien subi). Rouges sans module 4/6.
- [x] Étape 7 bis : NON. [ ] Étape 8 : non faite. [x] Étape 8 bis : statut (badge couvert).
Carte terminée : **OUI**.

### sa018 : Smokescreen (Amélioration 1, PREPARATION) : terminée
- [x] Étape 2 : `up023` (PREPARATION, `ReduceCostToPlayThis`, `Discard("This")`), `up004`/`Cloaked` (`PreventDamage(min(2, will_take_damage))`).
- [x] Étape 5 : « if your IDENTITY is cloaked » ; « an ENEMY attack » ; « a FRIENDLY character » ; « prevent 2 OF THAT damage » ; « discard THIS card → » (coût) ; Hero Interrupt. Résultat : conforme.
- [x] Étape 6 : 2 dégâts évités, réduction 1, coût 1. Conforme.
- [x] Étape 7 : 9 cas (réduction : coût 0 identité camouflée héros / alter-ego (⚠ Peter paie seul sa ressource : interdit au cas) ; non camouflée : cout 1 ; ATQ 4 -> 2 dégâts, témoin 4 ; ATQ 2 : 0 ; allié protégé ; dégâts directs : non ; alter-ego : non). Rouges sans module 5/9.
- [x] Étape 7 bis : NON. [ ] Étape 8 : non faite. [x] Étape 8 bis : NON.
Carte terminée : **OUI**.

### sa019 : Gaslight (Événement 1, THWART) : terminée
- [x] Étape 2 : `CoutDefausserCloaked("hero")` (`sk049`) ; `ud004` (choix `ChooseAbilities` de deux `ForChoiceAbility`) ; `10019`, `08003` (Confused).
- [x] Étape 5 : coût « from YOUR HERO » ; « choose: » (une seule branche) ; « 3 threat from A scheme » ; « Confuse AN enemy ». Résultat : conforme.
- [x] Étape 6 : 3 menaces, coût 1. Conforme.
- [x] Étape 7 : 6 cas (branche menace 5 -> 2 ; branche Désorienté, menace inchangée ; héros non camouflé / allié seul camouflé / alter-ego : injouable ; positif). Rouges sans module 3/6.
- [x] Étape 7 bis : NON. [ ] Étape 8 : non faite. [x] Étape 8 bis : statut (badge couvert).
Carte terminée : **OUI**.

### sa020 : From the Shadows (Ressource [wild], Max 1 per deck) : terminée
- [x] Étape 2 : `21046` Audacity (`AfterYouSpendThisCard(HeroResponse, ...)`, filtre `to_pay_card`), `CarteShinobi("Ninjutsu")`.
- [x] Étape 5 : « After you spend THIS card » ; « TO PLAY a Ninjutsu card » ; « cloak YOUR HERO » ; « Max 1 per deck » (`MaxPerDeck`, règle du deck-builder). Résultat : conforme.
- [x] Étape 6 : RES G, MaxPerDeck 1. Conforme.
- [x] Étape 7 : 4 cas (payer Cut-and-Run avec elle : camouflé ; carte non Ninjutsu : non ; carte payée sans elle : non ; alter-ego : non). Rouges sans module 1/4 ; verts : 3 témoins.
- [x] Étape 7 bis : NON (« Max 1 per deck » : règle de construction, non jouée en partie). [ ] Étape 8 : non faite. [x] Étape 8 bis : NON.
Carte terminée : **OUI**. Non prouvé : « Max 1 per deck » dans le deck-builder (aucun test de construction pour cette carte).

### Étape 8 bis commune : `ui-app/src/board/tmnt-shinobi-ninjutsu-plateau.test.ts` (13 tests)
Statut Cloaked dessiné sur héros / allié ; compteurs `shadow` (sa007) et `smoke` (sa008) dessinés + libellés français ; Twilight Sentry portée par l'ALLIÉ avec sa carte Cloaked ; témoins négatifs. Vu ROUGE sans le correctif :
les deux libellés français (`compteurs-fr.ts` rétabli à l'état d'avant : 2 tests échouent). Le reste est vert d'emblée (rendu générique déjà en place), dit clairement.
