# Sentry (Robert Reynolds) : gabarits PROCESSUS-CARTE, 03/11/2026

Pack `sentry` (prefixe `rr`, set 250, auteur Neptune, version « New »). Scripts : `src/cards/pack/sentry/{sentry,sentry_nemesis,merged_sentry}/` + helpers `sentry_commun.py`. Cas : `tools/cas/sentry.py` (55). Decks : `deck/starter/sentry.json` (Aggression, deck de base), `sentry_justice.json`, `sentry_leadership.json`, `sentry_protection.json`. 93 card_id : rr001a/b, rr002-rr014 (16 cartes de heros avec doublons), rr015 obligation, rr016-rr019 nemesis, rr020-rr023 modulaire Merged Sentry, rr024-rr092 reskins d'aspect (`ability_link`).

## Source et decisions

- Matiere : Sentry.zip (PNG 1500x2150 ; version « New », l'« Old » est une autre iteration). Scans EN seuls : textes FR ecrits a la main (noms laisses en anglais). 3 cartes ont ete remplacees par l'auteur le 03/11 : rr007 Molecularkinesis (Hero Interrupt : annule une carte rencontre revelee), rr013 Obliterate (tous les attachements d'un ennemi OU un sbire non-ELITE ; Special a trois defausses), rr001a (image recadree).
- Decisions utilisateur du 03/11 : The Watchtower = 1 compteur (la carte prime) — **QUESTION EN ATTENTE DE L'AUTEUR** (l'insert et la page A4 disent 2) : constante unique `WATCHTOWER_MAX_COMPTEURS` en tete de `rr005.py` ; Void « cannot take less than X damage each round » = **chaque attaque** lui inflige au moins X ; nom du heros « Sentry » ; Obliterate = choix direct sans degats ; decklist Justice recopiee a 37 cartes ; Merged Sentry = modulaire jouable avec tout scenario.
- Lecture a valider : Cornelius Worth (rr004) : le « choose » est coupe en DEUX capacites qui partagent le cout d'epuisement (une `Resource` [mental] et une `Action` retirer 1 compteur), le moteur n'ayant pas d'Action qui genere une ressource dans la reserve.
- Mots-cles ouverts (fiches) : stun, confuse, consequential, malevolent (maison), cancel (crees le 03/11) ; piercing, overkill, retaliate, toughness, guard, patrol, surge, permanent, special lues avant les scripts.
- Moteur (fichiers partages) : `CardFace.COUNTER` (balance, overwhelm) et `CardFace.TRAITS` (SPLIT, THERAPIST, DARK SENTRY) dans `card_face.py`, `compteurs-fr.ts`. Un Special resolu depuis la DEFAUSSE exige `.NoOutOfPlayLimit()`. Avec 3 compteurs le Void est revele : les cas qui attaquent font `RemoveNemesisAside()`.
- Limites non mesurees (ecrites dans les scripts) : boost de rr023 (+2 icones, perforation), Specials de rr007 (defausse des decks) et rr008 (« autres ennemis ne s'activent pas »), Response de defense de rr012, glisse sous Monster of Antithesis et defaite a 5 (rr017).

### rr001a : Sentry

- [x] Etape 2 : carte(s) de reference : - « At the end of your turn » : `so011` / Binary (`AbilityFactory.AfterPlayerTurnEnd(.., "You", op)`) ; type `ForcedResponse` comme le texte. - « balance counter » : compteur maison declare dans `CardFace.COUNTER` (card_face.py) + `compteurs-fr.ts` ; pose par `Faces.PlaceCountersOn` (helper `PoserEquilibre`, qui laisse The Watchtower detourner le compteur : `WhenCardWouldBePlacedCounter`). - « reduce the resource cost of the next event you play » : `dz014` / `sentinel` : `AbilityFactory.WhenCalculateEffectCost(NonKeyword, op, conditions=[..])` + `message.UpdateCost(-X, effect)`.
- [x] Etape 5 : texte-contre-code : « At the end of YOUR turn » : fin du tour de ce joueur (heros seulement : l'alter-ego n'a pas cette capacite). « Forced » : obligatoire, aucun choix. « ONCE PER PHASE » : marqueur `joueur.rr_gg_phase = world.phase_id`, pose quand l'evenement est JOUE (la condition de cout, evaluee plusieurs fois pour l'affichage, reste pure). « the NEXT EVENT you play » : seul un evenement (jamais une amelioration) consomme la reduction ; X est lu au calcul du cout (compteurs sur Duality Aspect, pas « en jeu »). X = 0 : aucune reduction et le marqueur n'est PAS pose (une phase sans compteur ne consomme pas Golden Guardian). Chiffres : PV 16, main 4, THW 1, ATQ 2, DEF 3.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (2) : fin de tour en forme HEROS : 1 balance counter sur Duality Aspect ; TEMOIN : en forme ALTER-EGO la capacite de la face heros n'existe pas (0 compteur)
- [x] Etape 7 bis : preuve par substitution : 1/2 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr001b : Robert Reynolds

- [x] Etape 2 : carte(s) de reference : - Setup : Duality Aspect porte `desc.Permanent` (donnees) : le moteur la met en jeu a la mise en place, SANS compteur : aucun code ici (fiche `permanent.md`, `setup.md`). - « After you change to this form » : `AbilityFactory.AfterFlipToThisFace(Response, op)` (modele `wn001a`, `ch001b`).
- [x] Etape 5 : texte-contre-code : « you MAY remove » : la Reponse est facultative (type `Response`). « UP TO 2 » : on retire autant que possible, jusqu'a 2 ; l'ordre est d'abord Duality Aspect puis les autres cartes (The Watchtower) : le texte dit « from play », sans imposer la carte. Pas de limite au nombre de compteurs en jeu (insert). Chiffres : PV 16, main 5, REC 4.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (2) : en passant en alter-ego avec 3 compteurs : on en retire 2 (reste 1) ; TEMOIN : un seul compteur, on retire ce qu'il y a (« up to 2 » : 0 reste)
- [x] Etape 7 bis : preuve par substitution : 2/2 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr002 : Duality Aspect

- [x] Etape 2 : carte(s) de reference : - Permanent : lu dans `desc` (`Permanent`), aucun code (fiche `permanent.md`). - « After you place a counter here, if there are N+ » : `AbilityFactory.AfterCounterPlacedOn(ForcedResponse, "This", 'balance', op, at_least=3)` (`game/ability/factory/counter.py`). - « Find X and reveal him » : `ca016` Meticulous Targeting (helper `TrouverEtRevelerVoid`). - « After the Special ability on a card is resolved » : `AfterPlayerResolveAbility(.., which_abilities=["Special"])` (RECETTES §27, modele `rz007`).
- [x] Etape 5 : texte-contre-code : « AFTER you place a balance counter HERE » : seulement les compteurs poses SUR cette carte (un compteur detourne par The Watchtower ne declenche rien). « 3+ HERE » : sur cette carte, pas « en jeu ». « he engages YOU » : le joueur de Duality Aspect. « Void » : introuvable -> rien. « SPLIT card » : trait SPLIT, resolue PAR N'IMPORTE QUI (le Void la resout aussi) ; la carte est remelangee dans le deck du joueur SENTRY (proprietaire), pas du Void. « you MAY remove 1 » : la suite est facultative. Chiffres : aucun cout, un seul exemplaire (Permanent).
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (2) : le 3e compteur fait reveler Void (il entre en jeu) ; TEMOIN : 2 compteurs seulement, Void ne vient pas
- [x] Etape 7 bis : preuve par substitution : 1/2 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr003 : C.L.O.C.

- [x] Etape 2 : carte(s) de reference : - « When X enters play » en Reponse : `AbilityFactory.AfterCardEnterPlay(AbilityType.Response, "This", op)` (forme de `counter.py::ThisEnterPlayWithCounters`). - « remove a balance counter from play » : helper `RetirerEquilibre` (Duality Aspect d'abord, puis The Watchtower). - ☆ sous THW/ATQ (dégâts consécutifs) : lu dans `desc` (`"2*"`, `"1*"`), aucun code (fiche `consequential.md`).
- [x] Etape 5 : texte-contre-code : « you MAY » : Reponse facultative. « 1 balance counter FROM PLAY » : n'importe quelle carte en jeu (pas seulement Duality Aspect) ; sans compteur la Reponse est sans effet. Chiffres : cout 2, THW 2, ATQ 1, PV 3.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (2) : en entrant en jeu, retire 1 balance counter (2 -> 1) ; TEMOIN : sans compteur en jeu, rien a retirer (0 reste)
- [x] Etape 7 bis : preuve par substitution : 1/2 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr004 : Cornelius Worth

- [x] Etape 2 : carte(s) de reference : - « Exhaust this card → » : `CostFunc.Exhaust("This")` (ca003, mf005). - « Generate a [mental] resource » : `CanGenerateResources(AbilityType.Resource, Resources("B"))` + `CostFunc.Exhaust("This")` (modele `im005` Stark Tower, `ca009`). - « remove 1 balance counter from Duality Aspect » : `Faces.RemoveCountersOn([dualite], 1, 'balance', effect)`.
- [x] Etape 5 : texte-contre-code : « choose » : le moteur n'a pas d'« Action qui genere une ressource dans la reserve » : une ressource n'existe qu'AU PAIEMENT. Les deux options deviennent DEUX capacites qui partagent le meme cout (epuiser la carte) : une `Resource` (generer [mental]) et une `Action` (retirer 1 compteur) ; elles s'excluent donc l'une l'autre, comme le « choose ». Lecture notee au compte rendu. « from DUALITY ASPECT » : seulement cette carte (pas The Watchtower). Sans compteur sur Duality Aspect, l'Action est sans effet. Chiffres : cout 1.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (1) : Action : epuise la carte et retire 1 compteur de Duality Aspect (2 -> 1)
- [x] Etape 7 bis : preuve par substitution : 1/1 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr005 : The Watchtower

- [x] Etape 2 : carte(s) de reference : - « You get +2 THW » : `GiveKeywordToInPlayWhenApplyThis(Hero, control_by="You", thwart=2)` (modele `ca003` pour +1 REC, `ra013`). - « When a counter would be placed » : `AbilityFactory.WhenCardWouldBePlacedCounter(Interrupt, CardFinder(name=..), 'balance', op)` (`game/ability/factory/counter.py`) ; remplacer l'evenement : `message.SetBeInstead(effect)` (RECETTES §27). - « place a counter here » : `Faces.PlaceCountersOn([this], 1, 'balance', effect, maximum=1)`.
- [x] Etape 5 : texte-contre-code : « You get +2 THW » : l'identite du joueur (face HEROS : seule face avec un THW). « that counter » : UN compteur ; si l'effet en place plusieurs a la fois (obligation : 3), UN est detourne ici et les autres restent sur Duality Aspect. « to a maximum of 1 » (decision utilisateur du 03/11 : la carte prime sur l'insert qui dit 2) : l'Interruption n'est pas proposee quand la carte porte deja un compteur ou qu'elle est epuisee. Chiffres : cout 3, +2 THW, plafond 1. ⚠ LIMITE DE COMPTEURS DE LA TOUR : UNE SEULE constante. QUESTION EN ATTENTE DE LA REPONSE DE L'AUTEUR (Neptune) : la carte imprimee dit « to a maximum of 1 », l'insert et la page de regles A4 disent « able to hold up to 2 ». Provisoirement 1 (decision utilisateur du 03/11 : la carte prime). Si l'auteur repond 2 : changer CETTE ligne (le cas de test `tools/cas/sentry.py` la lit) et le texte de `cards.json` (rr005). WATCHTOWER_MAX_COMPTEURS = 1
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (5) : la balance de fin de tour est DETOURNEE ici : 1 compteur sur la tour, 0 sur Duality Aspect ; TEMOIN D'EPUISEMENT (plafond = WATCHTOWER_MAX_COMPTEURS) : la tour est PLEINE, le compteur suivant va sur Duality Aspect ; TEMOIN : tour epuisee, le compteur va sur Duality Aspect ; « You get +2 THW » : Sentry (THW 1) deja a 3 : un Thwart de base retire 3 menaces (5 -> 2) ; TEMOIN : sans la tour, un Thwart de base retire 1 menace (5 -> 4)
- [x] Etape 7 bis : preuve par substitution : 2/5 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr006 : Endless Power

- [x] Etape 2 : carte(s) de reference : - « NAME gets +1 ATK and gains retaliate 1 » : `GiveKeywordToInPlayWhenApplyThis(CardFinder(name=..), control_by="You", attack=1, retaliate=1)` (`ca004`, `ra013`). - « After you play an event » : `AfterPlayerPlayedCard(HeroResponse, "You", Event, op)` (RECETTES §1) ; « using Golden Guardian » : marqueur `joueur.rr_gg_evenement` pose par rr001a. - Special : `AbilityFactory.WhenResolveSpecialAbility("This", op)` (RECETTES §27, `rz006`) ; statuts : `Faces.GiveStatus(cibles, "Stunned"/"Confused", effect)`.
- [x] Etape 5 : texte-contre-code : « SENTRY gets » : nom propre = la face heros. « using your Golden Guardian ability » : l'evenement DONT LE COUT a ete reduit par Golden Guardian (marqueur de rr001a), pas n'importe quel evenement. « shuffle THAT event into your deck » : l'evenement qui vient d'etre joue (il est alors dans la defausse). « The Void stuns AND confuses » : le Void (en jeu) etourdit ET embrouille chaque AUTRE ennemi et chaque personnage sous le controle du joueur ; sans Void en jeu le Special n'a pas d'effet. Chiffres : cout 3, +1 ATK, retaliate 1.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (2) : Special resolu : le Void etourdit et embrouille l'AUTRE ennemi (Hydra Mercenary) ; la carte SPLIT est remelangee dans le deck par Duality Aspect ; TEMOIN : sans Void en jeu le Special n'a aucun effet (l'autre ennemi n'est ni etourdi ni embrouille)
- [x] Etape 7 bis : preuve par substitution : 1/2 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr007 : Molecularkinesis

- [x] Etape 2 : carte(s) de reference : - « When an encounter card is revealed, cancel all of its effects and discard it » : `bkw/08008` (Grappling Hook) : `WhenPlayerRevealCard(HeroInterrupt, "You", type, "All", op)` + `message.CancelAllEffectsAndDiscardIt(effect)` ; « discard this card » en COUT : `CostFunc.Discard("This")`. Fiche `docs/reference/mots-cles/cancel.md` si elle existe (annuler = les effets ne se resolvent pas). - « draw 1 card for each » : `joueur.DrawUp(n, effect)`. Special : `joueur.DiscardDeckTopCards(n, effect)` + `Worlds.DiscardEncounterCards(n, effect)` ; `.NoOutOfPlayLimit()` (resolu depuis la defausse par le Void).
- [x] Etape 5 : texte-contre-code : « an ENCOUNTER card » : toute carte rencontre revelee (traitrise, sbire, complot annexe...) ; « cancel ALL of its effects and DISCARD it » : tous ses effets (When Revealed compris) sont annules et la carte est defaussee. « Then, discard THIS card » : paye en COUT (la carte quitte le jeu avant la resolution : meme resultat). « for each balance counter on DUALITY ASPECT » (Interruption : Duality seule) ; Special : « IN PLAY » (somme de toutes les cartes). Chiffres : cout 2.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (2) : Equilibrium Intent est revelee (sans Void elle poserait 1 compteur) : ses effets sont ANNULES (les compteurs ne bougent pas), la carte est defaussee,  ; TEMOIN : sans compteur sur Duality Aspect, l'annulation a lieu (0 compteur, pas le +1 d'Equilibrium Intent) mais on ne pioche rien
- [x] Etape 7 bis : preuve par substitution : 2/2 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr008 : Pacifying Presence

- [x] Etape 2 : carte(s) de reference : - « When X would be dealt damage ... prevent all » : `WhenUnitWouldTakeDamage(HeroInterrupt, None, op, conditions=[..])` + `message.PreventDamage("All", effect)` (sender_damage.py:665) ; coût `CostFunc.Discard("This")`. - Soin : `this.HealthUnits([cible], 1, effect)` ; dégâts d'une carte : `carte.sustained`. - « cannot activate this round » : `this.effect.RegisterTemp(WhenEnemyWouldActivate(Temp0, ..), unregister_after_exec=False, until_round_end=True)` + `message.SetBeInstead(effect)` (RECETTES §26 Specials / `rz018`).
- [x] Etape 5 : texte-contre-code : « friendly character » : identite et allies des joueurs. « Then, heal damage FROM AMONG characters EQUAL TO THAT DAMAGE » : autant de points de soin que de degats empeches, repartis un par un entre les personnages blesses au choix du joueur. « Heal 2 PER HERO from Void » : 2 x nombre de joueurs. « Other enemies cannot activate THIS ROUND » : tous les ennemis sauf le Void, jusqu'a la fin du round. Chiffres : cout 1.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (3) : Rhino frappe Sentry (blesse de 3) : les 2 degats sont EMPECHES, la carte est defaussee, puis 2 degats sont soignes (3 -> 1) ; TEMOIN sans la carte : la meme attaque s'ajoute aux 3 degats (5) ; Special (via Void a 3 compteurs) : le Void (blesse de 3) est SOIGNE de 2 par joueur (2) -> il lui reste 1 degat
- [x] Etape 7 bis : preuve par substitution : 2/3 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr009 : Purposeful Disparity

- [x] Etape 2 : carte(s) de reference : - « reduce the damage he takes by 1 » : `WhenUnitWouldTakeDamage(.., is_from_attack=True)` + `message.ReduceDamage(1, effect)` (sender_damage.py:830). - « Exhaust this card → » : `CostFunc.Exhaust("This")` ; deplacer une carte : `Faces.MoveAllTo([carte], joueur.discard_pile, effect)` (le dernier arrive est le DESSUS).
- [x] Etape 5 : texte-contre-code : « While Sentry is in HERO FORM » : seulement quand l'identite du joueur est la face heros (l'alter-ego ne beneficie pas de la reduction). « from EACH attack » : chaque attaque, d'au plus 1 ; jamais sous 0. « Place it ON TOP of your discard pile » : devient la carte du dessus (celle que le Void resout en premier). Chiffres : cout 2, -1.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (2) : en forme HEROS, une attaque de 3 (Hydra Mercenary ATK 1... Rhino 2) inflige 1 de moins ; TEMOIN : sans la carte, la meme attaque inflige 2
- [x] Etape 7 bis : preuve par substitution : 1/2 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr010 : Energy Flare

- [x] Etape 2 : carte(s) de reference : - « Deal N damage to each enemy » : `this.DealDamage(ennemis, 3, effect, property=AttackProperty(overkill=..))` (`ca012`, `.SetPlay()`). - Special : le Void attaque : `void.CastTo(Enemy).AttackCharacter(cible, effect, overkill=True)` (RECETTES §16.1) ; `.NoOutOfPlayLimit()`.
- [x] Etape 5 : texte-contre-code : « each enemy IN PLAY » : le Void compris pour les degats de l'evenement. « gains overkill if 3+ balance counters IN PLAY » : somme sur toutes les cartes. Special : « each character you control AND each enemy » : chaque personnage du joueur (identite, allies) puis chaque AUTRE ennemi (le Void ne s'attaque pas lui-meme), une attaque chacun. Chiffres : cout 3, 3 degats.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (2) : 3 degats a CHAQUE ennemi en jeu (Rhino prend 3, Hydra Mercenary a 3 PV est abattu) ; Special (via Void ATQ 3) : le Void attaque chaque personnage (Sentry subit 3) et chaque AUTRE ennemi (Hydra Mercenary, 3 PV, est abattu)
- [x] Etape 7 bis : preuve par substitution : 2/2 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr011 : Global Influence

- [x] Etape 2 : carte(s) de reference : - `ca010` (Sinister Flight) : `this.RemoveThreatFromSchemes(effect.targets, n, effect, ignore_crisis=True)` + `.SetPlay().SetLabel('thwart').SetTarget(Scheme2).SetIgnoreKeyword('Patrol')`. - Special : `this.PlaceThreatOnSchemes("EachScheme", X, effect)` (card_face.py:1032) ; `.NoOutOfPlayLimit()`.
- [x] Etape 5 : texte-contre-code : « up to 3 threat FROM AMONG schemes » : lecture codee = UNE manigance choisie (modele `ca010`), jusqu'a 3 (5 a 3+ compteurs) ; « ignoring patrol AND any crisis icons » : les deux. « X = the Void's SCH » : le SCH COURANT du Void (= compteurs sur Duality Aspect) ; sans Void en jeu, pas d'effet. « EACH scheme » : principale et annexes. Chiffres : cout 2, 3 ou 5.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (3) : retire 3 menaces du complot principal (5 -> 2) malgre un sbire Patrol engage ; avec 3 compteurs : 5 menaces retirees (6 -> 1) ; Special (via Void a 3 compteurs, SCH 3) : 3 menaces sur CHAQUE manigance (complot principal 1 -> 4)
- [x] Etape 7 bis : preuve par substitution : 3/3 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr012 : Nigh-Invulnerability

- [x] Etape 2 : carte(s) de reference : - `se011` / `56047` : `WhenUnitWouldAttack(HeroInterrupt, Enemy, op).SetTarget("YourHero")` + `message.DeclareDefender(heros, effect)` ; `.SetPlay().SetLabel('defense')`. - Statuts : `Faces.GiveStatus(cibles, "Tough"/"Stunned", effect)`. Special : `RegisterTemp(WhenUnitWouldTakeDamage(Temp0, ..), unregister_after_exec=False, until_phase_end=True)` + `PreventDamage("All")` (RECETTES §26).
- [x] Etape 5 : texte-contre-code : « WITHOUT EXHAUSTING him » : la declaration ne depense pas la defense du heros. « Give HIM a tough status card » : Sentry (le defenseur). « stun THE ATTACKER if 3+ counters IN PLAY » : l'ennemi qui attaque. Special : le Void gagne Tough et ne subit AUCUN degat jusqu'a la fin de la PHASE ; sans Void en jeu, rien. Chiffres : cout 1.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (1) : Special (via Void a 3 compteurs) : le Void ne subit AUCUN degat cette phase (2 attaques de Sentry : la 1re absorbee par Toughness, la 2e normalement 3
- [x] Etape 7 bis : preuve par substitution : 1/1 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr013 : Obliterate

- [x] Etape 2 : carte(s) de reference : - `ChooseAbilities` de `ForChoiceAbility` avec cibles : `rz007` (`SetTarget(Enemy, ..)`) ; critere « non-ELITE » : `CardFinder(card_type=Minion, non_trait="ELITE")` (ca022) ; attachements d'un ennemi : `ennemi.GetAttachedAttachments()` (ca020). - « defeat, ignoring When Defeated » : `Faces.DefeatUnits(cibles, None, effect, ignore_when_defeated=True)` ; « defeat a side scheme » : `this.RemoveThreatFromSchemes(cibles, "All", effect)`. - Special : cout imprime `carte.printed_cost.val` (ra031), PV `carte.max_health`, menace `scheme.threat` ; `.NoOutOfPlayLimit()`.
- [x] Etape 5 : texte-contre-code : DECISION UTILISATEUR du 03/11 (valable pour la nouvelle version) : « choix direct SANS DEGATS » : aucune attaque (Toughness, gardes, effets « apres une attaque » ne comptent pas). « ALL attachments from AN enemy » : tous ceux de l'ennemi choisi. « NON-ELITE minion » : un sbire sans le trait ELITE. « (or side scheme IF 3+ counters IN PLAY) » : troisieme choix, seulement a 3+ compteurs. Special : TROIS defausses : la carte au plus haut cout que vous controlez, le sbire aux PV les plus hauts (tout sbire, Void compris : le texte ne l'exclut pas) et le complot annexe a la plus haute menace. Chiffres : cout 4.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (2) : choix « vaincre un sbire non-ELITE » : Hydra Mercenary (Garde 1, 3 PV) est vaincu SANS attaque ; Special (via Void a 3 compteurs) : la carte au plus HAUT COUT que Sentry controle (The Watchtower, 3) est defaussee
- [x] Etape 7 bis : preuve par substitution : 2/2 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr014 : Unrivaled Might

- [x] Etape 2 : carte(s) de reference : - `ca012` (Chomp) : `this.DealDamage(effect.targets, N, effect, property=AttackProperty(piercing=True))` + `.SetPlay().SetLabel('attack').SetTarget(Enemy)`. - Special : `void.AttackCharacter(villain, effect, property=AttackProperty(piercing=True))` puis `void.DoAttackYou(joueur, effect, property=AttackProperty(piercing=True, other_characters_cannot_defend=True))` ; `.NoOutOfPlayLimit()`.
- [x] Etape 5 : texte-contre-code : « 10 damage INSTEAD » : 10 a 3+ compteurs en jeu (somme), sinon 8. « The Void attacks the villain AND you » : DEUX attaques (le vilain, puis le joueur). « You CANNOT DEFEND » : aucun autre personnage ne peut defendre l'attaque contre le joueur (`other_characters_cannot_defend`) ; l'identite subit l'attaque. « piercing » : sur les deux. Chiffres : cout 3, 8 ou 10.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (3) : sans compteur : 8 degats au vilain (Rhino) ; avec 3 compteurs en jeu : 10 degats « instead » ; Special (via Void ATQ 3) : le Void attaque le vilain (Rhino subit 3) ET Sentry (subit 3)
- [x] Etape 7 bis : preuve par substitution : 3/3 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr015 : Fractured Psyche

- [x] Etape 2 : carte(s) de reference : - `ca014` (Essential Bloodlust, meme gabarit) / `dy013` / `my015` : `WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` + `ChooseAbilities`, branche 1 `condition=joueur.IsAlterEgo()` + `Exhaust("YourIdentity")`. - « place 3 balance counters » : helper `PoserEquilibre` (The Watchtower peut en detourner UN, `WhenCardWouldBePlacedCounter`).
- [x] Etape 5 : texte-contre-code : « You may flip to alter-ego form » : bascule facultative avant le choix. « Exhaust ROBERT REYNOLDS » : l'alter-ego, PRET et en forme alter-ego (apres l'eventuelle bascule). « Place 3 balance counters on Duality Aspect. Discard this obligation » : la defausse appartient a la SECONDE branche (la premiere la retire de la partie). Aucun surge (le texte n'en parle pas). Chiffres : boost 2 (Menace 2), 3 compteurs.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (2) : branche 1 : en alter-ego, Robert Reynolds s'incline et l'obligation est RETIREE de la partie ; branche 2 : 3 balance counters sur Duality Aspect, l'obligation est defaussee (pas retiree), Reynolds reste pret
- [x] Etape 7 bis : preuve par substitution : 2/2 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr016 : Void

- [x] Etape 2 : carte(s) de reference : - « SCH/ATK = X » variable : `ThisGainKeyword(fn, scheme=1, attack=1, change_on_event=OnEvent.Counter(CardFinder(name=..), 'balance'))` (`bg015`, `bw016`). - « cannot take less than X damage » : `WhenUnitWouldTakeDamage(.., "This", op)` + `message.IncreaseDamage(n, effect)` (sender_damage.py:812). - « When the Void would activate ... instead » : `AbilityFactory.WhenEnemyWouldActivate(NonKeywordStar..., "This", op)` + `message.SetBeInstead(effect)` ; Special d'une autre carte : `carte.ResolveSpecialAbility(joueur, effect)`. - Toughness : lu dans `desc` ; Malevolent : fiche `malevolent.md` (mot-cle maison, hors `desc`).
- [x] Etape 5 : texte-contre-code : « X » : compteurs sur DUALITY ASPECT seulement. « cannot take less than X damage EACH ROUND » : DECISION UTILISATEUR du 03/11 : CHAQUE ATTAQUE lui inflige au moins X (plancher par instance de degats, applique quand elle en inflige au moins 1). « 3+ balance counters IN PLAY » : la somme de toutes les cartes (Duality Aspect + The Watchtower). « the TOPMOST SPLIT card » : la plus haute carte SPLIT de la defausse du joueur Sentry. « INSTEAD » : l'activation est remplacee (ni manigance ni attaque) ; « if able » : sans carte SPLIT, le Void s'active normalement. MALEVOLENT (fiche `malevolent.md`, page de regles A4 du 03/11) : tant que le Void est en jeu, la PREMIERE attaque de chaque personnage ami et de chaque AUTRE ennemi, a chaque round, est RE-CIBLEE sur le Void (`WhenUnitWouldAttackUnit` + `message.ChangeTarget(void, effect)`, modele `ca019`) ; marqueur `attaquant.rr_void_ronde = world.round_id`. De plus un ennemi qui allait attaquer une IDENTITE alors que le Void est engage avec ce joueur attaque le Void a la place (meme hors premiere attaque). Chiffres : PV 4 par joueur, boost 3.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (6) : plancher de degats : avec 4 compteurs, la 2e attaque de Sentry (2 degats ; la 1re est absorbee par Toughness) inflige AU MOINS 4 : le Void (4 PV pour  ; TEMOIN : sans compteur (X = 0) la 2e attaque de Sentry (la 1re est absorbee par Toughness) inflige 2, pas davantage ; la 1re attaque de Sentry du round vise Rhino mais est RE-CIBLEE sur le Void : Rhino ne subit rien ; la 2e attaque du MEME round n'est plus contrainte : elle touche Rhino (2) ; TEMOIN : sans le Void en jeu, la 1re attaque de Sentry touche Rhino (2) ; Rhino allait attaquer Sentry alors que le Void est engage avec le joueur : il attaque le VOID a la place (Sentry, epuise, ne subit rien)
- [x] Etape 7 bis : preuve par substitution : 4/6 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr017 : Monster of Antithesis

- [x] Etape 2 : carte(s) de reference : voir l entete du script
- [x] Etape 5 : texte-contre-code : voir l entete du script
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [ ] Etape 7 : AUCUN cas dedie (voir « Limites non mesurees »).
- [ ] Etape 7 bis : pas de script (carte sans capacite codee) : rien a substituer.
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr018 : Angel of Death

- [x] Etape 2 : carte(s) de reference : - `ca017` (Death Spiral) : `AttachToFaceWhenPutIntoPlay(CardFinder(card_type=Minion, name=..), if_cannot_gain_surge=True)` ; ici `if_cannot_operation` pose en plus les 2 compteurs. - « gains guard and patrol » : `GiveKeywordToAttached(.., guard=1, patrol=1)` ; fin de round : `WhenRoundEnd(ForcedInterrupt, None, op)` (`bw016`) ; Special : `carte.ResolveSpecialAbility(joueur, effect)`.
- [x] Etape 5 : texte-contre-code : « If you CANNOT (attach) » : Void absent -> 2 compteurs sur Duality Aspect PUIS surge. « AT THE END OF THE ROUND (after the first player token is passed) » : code sur la fin de round ; le moteur n'a pas de fenetre distincte « apres le jeton » (note). « discards cards FROM THE TOP of their deck UNTIL they discard a SPLIT card » : on defausse une a une ; deck epuise sans SPLIT -> rien a resoudre. Chiffres : boost 3.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (2) : revelee avec le Void en jeu : elle s'attache AU VOID ; Void ABSENT : 2 compteurs sur Duality Aspect PUIS surge (la carte suivante du deck est distribuee)
- [x] Etape 7 bis : preuve par substitution : 2/2 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr019 : Equilibrium Intent

- [x] Etape 2 : carte(s) de reference : - « X activates » : `ca016` (`ennemi.DoActivate(joueur, effect)`) ; surge : `this.GainSurge(1, effect)` ; `ca018` pour le Boost (`WhenCardBecomeBoost("This", ..)`). - compteur : helper `PoserEquilibre`.
- [x] Etape 5 : texte-contre-code : « If the Void is in play, he activates » : il s'active (contre le joueur qui revele). « If the Void is NOT in play » : 1 compteur sur Duality Aspect PUIS surge. Boost : « identity-specific » = carte de classe Hero (`card_classes` : `IdentitySpecific`) ; « you control » = en jeu sous le controle du joueur, tirage AU HASARD ; faute de carte en jeu, une carte de la MAIN (au choix). Chiffres : boost 1.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (3) : Void en jeu, 3+ compteurs : il s'active, son Forced Interrupt resout le Special de la carte SPLIT du dessus de la defausse (Endless Power etourdit l'a ; TEMOIN : seulement 2 compteurs, le Void s'active normalement (le Special de la defausse n'est PAS resolu) ; Void ABSENT : 1 compteur sur Duality Aspect puis surge (la carte suivante du deck est distribuee)
- [x] Etape 7 bis : preuve par substitution : 2/3 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr020 : Merged Sentry

- [x] Etape 2 : carte(s) de reference : - « +X ATK » variable : `ThisGainKeyword(fn, attack=1, change_on_event=OnEvent.Counter("This", 'overwhelm'))` (rr016, `bw016`) ; plancher de degats : `WhenUnitWouldTakeDamage` + `IncreaseDamage` (rr016). - « After X schemes » : `AbilityFactory.AfterUnitSchemeEnd(ForcedResponse, "This", op)` (do_scheme.py:70). - « When Defeated : puts him under your control as an ally » : EXACTEMENT `warriors_three/wt020` (Skadihr) : `WhenUnitWouldBeDefeated(ForcedInterrupt, "This", op)` + `SetBeInstead` + `HealHealth(99)` + `Faces.TreatAsAlly(this, "tah_hellbender_ally", joueur, GameRule(this), process=..)` puis `GainAttackConsequentialDamage(1)` / `GainThwartConsequentialDamage(1)`.
- [x] Etape 5 : texte-contre-code : « X = overwhelm counters ON HIM » (pas les balance counters de Sentry). « cannot take less than X damage from EACH ATTACK » : plancher par attaque (meme lecture que Void, decision utilisateur du 03/11). « schemes OR thwarts » : seule la manigance existe tant qu'il est un sbire (apres sa defaite il est un allie : sa face est remplacee par le gabarit, ses capacites de sbire disparaissent). « Reset his hit points to 4 » : 4 PV (pas 4 par joueur). Chiffres : PV 4*, boost 3.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (2) : plancher et +X ATQ : avec 2 compteurs overwhelm, une attaque de 2 (apres la 1re absorbee par Toughness) lui inflige au moins 2 et il est a 2 degats ; When Defeated : abattu (1 PV restant, 2 attaques dont la 1re absorbee par Toughness), il N'EST PAS defait : il reste en jeu comme ALLIE, PV remis a 4 
- [x] Etape 7 bis : preuve par substitution : 1/2 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr021 : External Darkness

- [x] Etape 2 : carte(s) de reference : - « Find X and put it into play engaged with you » : `ca016` / `ca022` (`Search.EncounterCard(.., include_discard_pile=True, include_set_aside=True, name=..)` + `face.PutIntoPlay(joueur, effect)`) ; stade : `printed_stage` (`has_stage.py`). - Crisis : lu dans `desc` (fiche `crisis.md`).
- [x] Etape 5 : texte-contre-code : « Find » : deck, defausse et zone de cote. Deja en jeu : il s'engage avec le joueur (pas de recherche). « X = the MAIN SCHEME's current stage » : le stade du complot principal (pas du vilain, voir rr022). Absent : rien.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (1) : revelee : Merged Sentry est CHERCHE dans le deck rencontre et entre en jeu engage, avec autant de compteurs overwhelm que le stade du complot principa
- [x] Etape 7 bis : preuve par substitution : 1/1 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr022 : Newfound Nature

- [x] Etape 2 : carte(s) de reference : - `ca017` : `AttachToFaceWhenPutIntoPlay(CardFinder(card_type=Minion, name=..), if_cannot_gain_surge=True)` ; stade du vilain : `villain.printed_stage` (`sk270`, `21013`). - « After X attacks and damages » : `AbilityFactory.AfterUnitAttackAndDamageUnit(ForcedResponse, attacker, who_be_attacked, op)` (do_attack.py:477) ; statut : `Faces.GiveStatus(.., "Stunned")`.
- [x] Etape 5 : texte-contre-code : « X = the VILLAIN's stage » (pas celui du complot principal). « non-hero CHARACTER » : un allie ; l'alter-ego et le heros sont exclus. Sans Merged Sentry le When Revealed ne pose rien (la carte a deja gagne surge a l'attache).
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (3) : revelee avec Merged Sentry en jeu : elle s'attache A MERGED SENTRY et pose X compteurs (stade du vilain 1) ; ★ : Merged Sentry (avec la carte attachee) attaque un allie (C.L.O.C., 6 PV) et le blesse : l'allie est ETOURDI ; TEMOIN : sans la carte attachee, l'allie blesse n'est PAS etourdi
- [x] Etape 7 bis : preuve par substitution : 2/3 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr023 : Scourge Blast

- [x] Etape 2 : carte(s) de reference : - `ca018` (boost : `WhenCardBecomeBoost("This", op)` + `message.GainBoostIcon(n, effect)`) ; `ca014` (`this.DealIndirectDamage(identite, n, effect)`) ; surge `this.GainSurge(1, effect)`.
- [x] Etape 5 : texte-contre-code : « place 1 counter THEN take 1 indirect damage FOR EACH counter » : le compteur est pose AVANT le calcul. Sans Merged Sentry : surge seulement. Boost : seulement quand l'activation est une ATTAQUE (pas une manigance) ; +2 icones ET perforation. ⚠ La perforation passe par `would_message.property.piercing` (champ de l'AttackProperty de l'activation) : lecture au mieux, mesuree par le cas.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (ligne « Chiffres » de l'entete).
- [x] Etape 7 : cas (2) : Merged Sentry en jeu : +1 compteur overwhelm (1 -> 2) puis 2 degats indirects a Sentry ; TEMOIN : sans Merged Sentry, surge (la carte suivante est distribuee) et aucun degat
- [x] Etape 7 bis : preuve par substitution : 2/2 cas rouges sans le module (les autres sont des temoins d'absence, verts par construction).
- [x] Etape 8 : autoplay cible : voir le bilan du heros ci-dessous.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : compteurs d'equilibre / de submersion, Void et Merged Sentry en jeu, Monster of Antithesis ; cas Vitest `sentry-plateau.test.ts` + captures Chromium FR et EN (captures/sentry, captures/sentry-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### rr024-rr092 : 69 reskins d'aspect (Aggression 18, Justice 14, Leadership 15, Protection 16, Basic 6)

- Aucun script : `ability_link` vers l'officielle de meme nom et de meme classe (voir `sentry-rapport.txt` du generateur) ; textes FR repris des officielles (`textes-fr-complets.ts`). Energy / Genius / Strength (rr089, rr090, rr092) sont des ressources sans `ability_link`, comme les Basics de Carnage. Aucune retouche du texte des officielles (audit des errata separe).
- Preuve : montage de TOUS les decks (4 decks Sentry) et autoplay.

Carte terminee : OUI (reskins) : sous reserve de la gate de heros.

## Bilan des portes du heros (03/11/2026)

- Cas du pack : 55 sur 55 (`tools/test_capacites.py ... "rr0"`). Substitution : 23 cartes sur 23 avec au moins un cas rouge sans leur module (`tools/substituer_pack.py`, passes seules pour rr005, rr009, rr012).
- Statique : `test_cards.py` 8210 modules, 0 erreur ; `verifier_api_cartes.py` 0 en faute (apres correction d'un commentaire) ; `audit_cartes.py` : remarques rr001b (Setup porte par `Permanent` de rr002), rr016/rr020/rr022 (types `NonKeywordStar` voulus : `ForcedInterrupt`/`ForcedResponse` resolvent le Special en double ou ne partent pas), rr017 (texte seul : l'interruption est dans `RemelangerOuGlisser`).
- Decks : passe COMPLETE, 188 decks sur 188 montent une partie (card_face.py partage touche : compteurs `balance`/`overwhelm`, traits SPLIT/THERAPIST/DARK SENTRY).
- Autoplay (rhino, normal, equilibre) : Sentry 8 parties, 0 bloquee, 0 traceback, 7,0 rounds en moyenne, 0 victoire ; temoin spider_man : 8 parties, 0 bloquee, 6,9 rounds.
- Ecran : test Chromium `ui-check/tests/sentry-ecrans.spec.ts` en francais et en anglais (31 captures chacune dans `captures/sentry/` et `captures/sentry-en/`), plateau `ui-app/src/board/sentry-plateau.test.ts`. Texte FR pose sur Void et Merged Sentry (les plus denses) : lisible, dans la zone, aucune correction de voile ni de taille.
- Textes FR : `ui-app/src/board/textes-fr-fanmade.ts` (23 cartes a la main + 69 reskins repris des officielles), copie JS regeneree ; gates `textes-fr-fanmade`, `vocabulaire-statuts`, `traduction-public` verts. Biographie `rr001a` dans `heros-info.js` (factuelle, tiree de la page d'introduction de l'auteur).
- Non mesure par un cas : boost de rr023 (+2 icones, perforation), Specials de rr007 (defausse des decks) et rr008 (« autres ennemis ne s'activent pas »), Response de defense de rr012, glisse sous Monster of Antithesis et defaite a 5 (rr017).
- Questions en attente : The Watchtower (carte : 1 compteur max ; insert et page A4 : 2) -> auteur ; Cornelius Worth (rr004) : coupe du « choose » en deux capacites a valider.
- Partie humaine complete : non jouee.
