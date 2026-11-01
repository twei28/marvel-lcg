# The Hunger Core (Marvel Zombies, fan-made) : gabarits PROCESSUS-CARTE, 27/10/2026

Scénario `the_hunger_core` (préfixe `hg`, auteur Penasquequeman, porté depuis TTS), **78 cartes** : hg001 à hg076, plus les faces hg004a/hg004b et hg005a/hg005b.
Scripts : `src/cards/pack/the_hunger_core/` : `the_hunger_core/` (hg001-hg006, hg046-hg055), `horde_deck_metazombies/` (hg007-hg015), neuf `zombie_<nom>_signature/` (hg016-hg045), `hungry_horde/` (hg056-hg058), `fallen_heroes/` (hg059-hg071), `survivor_deck/` (hg072-hg076). Code partagé : `commun.py` (Horde deck, decks signature, infection, Metazombies) et `the_hunger_core/__init__.py` (`CapacitesDuCoeur`).
Données : `data/cards_custom.json` (entrées hg), `data/scenarios/the_hunger_core(_expert).json`, `data/encounter_sets/the_hunger_core_*.json`. Fiches mots-clés maison : `mots-cles/shielded-by-the-horde.md`, `just-a-core-x.md`, `rupture-x.md`, `horde-metazombies.md`, `infection.md`.
Cas : `tools/cas/the_hunger_core.py`, **233 cas `[hg]`** (89 pour hg001-hg027, 99 pour hg028-hg076, 31 ajoutés le 27/10/2026 : règles du livret, hg003, hg015, hg034, hg052-hg055, hg066 ; puis 14 pour la limite d'Infection et la récupération). Les vérificateurs dédiés sont `hg_setup_etat`, `hg_distribuees_et_pas_de_degats`, `hg_manigance_etat`, `hg_peut_defendre_etat`, `hg008_deck_signature_etat`, `hg014_etat`, `hg_etat_plus` (cartes retirées du jeu, taille d'un deck signature, Metazombie à moitié de ses PV, nombre de cartes Tenace) `hg_infection_etat` (joueurs éliminés par siège, partie perdue, Infection/dégâts par siège, sbire engagé avec un siège, bout droit de la rangée) et `hg_jeton_etat` (porteur du jeton actif, rang dans la rangée, défausse du Horde deck, fond d'un deck signature, Metazombies indemnes).

**Aucune carte n'est « terminée »** : il manque partout la partie réelle jouée par un humain, la preuve par substitution n'est pas tracée (voir plus bas) et 46 cartes attendent un cas plateau qui n'existe pas.

## Chiffres globaux

- **test_capacites** : **233/233 cas `[hg]` verts** (relancé le 27/10/2026 après la limite d'Infection, point 6 ; auparavant 219/219, puis 188/188).
- **Autoplay relancé le 27/10/2026 après la limite d'Infection** : 8 parties `spider_man` contre `the_hunger_core` (standard, profil équilibré) : 0 plantage, 0 traceback, 0 victoire (5 « Players Lost », 3 « All players were eliminated »), 5,4 rondes en moyenne. Journaux non lus ligne à ligne : on ne sait pas si une mort par Infection s'y est produite (en solo, 7 compteurs en ~5 rondes est rare).
- **Autoplay relancé le 27/10/2026 après les corrections** : 8 parties `spider_man` contre `the_hunger_core` (standard, profil équilibré) : 0 plantage, 0 victoire (6 « Players Lost », 2 « All players were eliminated »), 5,5 rondes en moyenne. Journaux lus pour les nouvelles règles : le jeton passe d'UN cran par fin de phase méchant (hg011 -> hg013 -> hg012...), les Metazombies attaquent (1 à 13 attaques par partie), les morsures posent 1 Infection (0 à 6 par partie), deux Trapped Survivor révélés depuis le deck de rencontre (parties 4 et 6). Les lignes ci-dessous sur l'autoplay décrivent la fournée d'AVANT ces corrections.
- **Substitution** (Étape 7.3) : **aucune passe `substituer_pack.py` n'est tracée pour ce pack**, ni dans les commits (`c447e40d` à `33c497ee`) ni dans les scripts. Les seules traces de module retiré puis remis sont dans les en-têtes de `hg004b` (confirmé) et de `hg005b`, dont le cas d'accomplissement reste VERT sans module (filet générique du moteur sur le dernier stade, assumé dans le script). Beaucoup de cas s'appellent « TÉMOIN (preuve par substitution) », mais ce sont des **contre-cas montés sans la carte**, pas des passes avec le module retiré. Sur chaque fiche, l'Étape 7 est donc **partielle**.
- **Autoplay** : 8 parties, deck `spider_man` contre le vilain `the_hunger_core`. Toutes se sont terminées normalement : aucun blocage, aucun traceback, 0 victoire sur 8 (difficulté du scénario, pas un bug). Ce rapport ne mentionne **aucun héros témoin** dans la même fournée, les journaux **n'ont pas été lus ligne à ligne carte par carte**, et le mode (standard ou expert) n'est pas précisé. Les commits antérieurs indiquent aussi 8 parties sans plantage pour hg014-hg017 et pour hg018-hg027 ; dans ce dernier lot, un blocage relevait d'une limite connue du pilote sur `01093` Tenacity.
- **Angles morts structurels de cet autoplay** (cartes qui ne peuvent PAS apparaître dans ces 8 parties) :
  - Spider-Man est le héros choisi, donc `hg004a` exclut `hg010` Zombie Spider-Man du Horde deck : **hg010, hg027, hg028 et hg029 ne sont jamais en partie** en solo (à deux, hg010 peut désormais entrer si Spider-Man meurt d'Infection, point 6).
  - ~~hg051-hg055 jamais en jeu~~ : **RÉSOLU le 27/10/2026** (voir « Corrections du 27/10/2026 » ci-dessous) : les 5 Trapped Survivor sont désormais mélangés au deck de rencontre, comme le veut le livret. Les alliés hg072-hg076 n'arrivent en main que si un joueur vainc leur manigance (rare en autoplay).
  - **hg003** (Cœur stade III) n'entre en jeu qu'en mode expert (II -> III). En standard, le Cœur passe de I à II.
- **Plateau (Étape 8 bis)** : **aucun cas plateau pour ce pack**. `grep -ril hunger ui-app/src/board/` ne renvoie que `textes-fr-fanmade.ts`, et seulement pour des cartes Venom sans rapport (« We Hunger », « Feed the Hunger »). Aucun `*.test.ts` ne cite un card_id `hg`. Les 46 cartes qui changent ce qu'on VOIT sont marquées « absent » ci-dessous.
- **Mise à l'échelle par héros** : les valeurs « N* » écrites dans un script (Rupture 1*, Hunger Pulse 1*/2*, Trapped Survivor 2*, Fallen God 4*, Patched Armor +2*, Valeria 3*) ne sont éprouvées **qu'en solo** (N* = N). Les cas à deux joueurs existent seulement pour hg016, hg017, hg028 et hg044.

## Corrections du 27/10/2026 et observations hors carte

Source : le livret PDF du scénario (9 pages, images seulement, relu page par page le 27/10/2026 ; copie de travail dans le scratchpad de la session de portage). Rien n'a été inventé : chaque correctif cite sa page.

1. **Jeton actif et Metazombie vaincu : bug fonctionnel CONFIRMÉ et corrigé.** `PasserLeJeton`, `JetonApresDefaite` et `QuandMetazombieVaincu` n'étaient appelés nulle part (grep), et aucun autre mécanisme ne les remplaçait. Conséquences mesurées : (a) `hg004a` posait le jeton sur le Cœur et il n'en bougeait plus ; comme le Cœur n'attaque jamais (Just a Core), **aucun Metazombie ne s'activait en phase méchant** ; (b) un Metazombie vaincu passait par `Villain.OnBeDefeated` -> `AdvanceVillainStage`, qui le **retirait de la partie** (aucun stade suivant de même nom) au lieu de le mettre dans la défausse du Horde deck : il ne pouvait jamais revenir. Correctif : `commun.ReglesDuScenario()` (type `AbilityType.Scenario`, modèle Sinister Six `27100a`), ajoutée à `CapacitesDuCoeur` (le Cœur est le seul à rester en jeu du Setup à la victoire) : fin de phase méchant -> `PasserLeJeton` (p. 4) ; `WhenUnitBeDefeated` d'un Metazombie VILLAIN -> `QuandMetazombieVaincu` (p. 3 + FAQ p. 8 : attachements de signature au FOND de son deck signature, jeton au suivant s'il était actif, carte dans la défausse du Horde deck, ce qui court-circuite l'« avance » de stade). `MettreUnMetazombieEnJeu` passe le jeton au Metazombie qui entre quand il était sur le Cœur (p. 4 « When a Metazombie enters play again, the token moves to it ») : c'est aussi ce qui le pose sur le premier de la rangée à la mise en place (p. 7, étape 7). `JetonApresDefaite` corrigé au passage : il prenait le PREMIER restant au lieu du SUIVANT À DROITE du vaincu. **Piège mesuré en autoplay** (puis corrigé et couvert par 2 cas « vraie partie ») : une capacité `AbilityType.Scenario` reste active HORS JEU, donc hg002 (stade II, encore dans le deck des stades en standard) appliquait chaque règle une seconde fois (jeton avancé de deux crans, 2 Infections par morsure ; 3 fois en expert avec hg003). Chaque règle porte désormais la condition « ce stade du Cœur est en jeu » (substitution : sans elle, les 2 cas passent au rouge). Cas : 12 cas `[hg] regle jeton` / `regle Metazombie vaincu` (dont un témoin sans le Cœur) ; substitution faite le 27/10/2026 : `ReglesDuScenario` retirée -> les 8 cas sujets de rotation et de défaite alors présents passent au rouge, le témoin reste vert ; crochet d'entrée de `MettreUnMetazombieEnJeu` retiré -> les 2 cas « jeton sur le premier de la rangée / sur celui qui rentre » passent au rouge.
2. **Règle « Infection » : elle EXISTE dans le livret (p. 5) et n'était codée nulle part : corrigé.** « When an attack from a Zombie or Metazombie enemy deals damage to your hero, place 1 Infection counter » + « If an ally defends, or if your DEF or a tough status card prevents all the damage, there is no Infection ». Codée une seule fois dans `ReglesDuScenario` : `AfterUnitAttackAndDamageUnit(Scenario, ennemi ZOMBIE|METAZOMBIE, Hero, ...)` (`target_took_damage=True`). Cas : Metazombie (1), sbire Zombie hg056 (1), Tenace qui absorbe (0), Rhino non zombie (0), témoin sans le Cœur (0), vraie partie (exactement 1) ; substitution : les 2 cas sujets « rhino » passent au rouge. **TOUJOURS NON CODÉ** (même page du livret, hors du périmètre de cette correction) : la LIMITE (7, 6 en expert) qui vainc le héros et met sa version zombie en jeu (p. 5 et FAQ p. 8 « My hero dies from Infection in a solo game: you lose ») et le choix de la récupération de base (soigner REC OU retirer 3 Infection, p. 5). ~~Aujourd'hui les compteurs Infection s'accumulent sans aucune conséquence~~ : **limite et récupération CODÉES le 27/10/2026**, voir point 6.
3. **Trapped Survivor (hg051-hg055) : la règle existait, la donnée était fausse : corrigé.** Livret p. 7, étape 6 : « The Hunger Core set (13 cards, with the remaining Trapped Survivors) » (8 cartes hg046-hg050 + 5 survivants = 13, compte confirmé p. 9). Ils étaient dans `set_aside` des deux fichiers `data/scenarios/the_hunger_core(_expert).json` : déplacés dans `encounters`. Les alliés hg072-hg076 restent mis de côté (« Survivor deck »). `RetirerZombiesEtSurvivorsHomonymes` cherche désormais le Trapped Survivor d'un héros homonyme (Wolverine, Blade) aussi dans le deck de rencontre (le cas `hg004a Setup (wolverine)` reste vert). Cas : « hg051-hg055 mise en place » (les 5 dans le deck de rencontre, les 5 alliés mis de côté).
4. *(Observation, non tranchée, inchangée.)* **Portée du mot « Metazombie »** : `commun.Metazombies()`, `hg001` (bouclier et Rupture), `hg049` (« exposed ») et `hg064` ne comptent que les 9 **Villain** du Horde deck. `hg073` Chewie et `hg075` Blade s'appuient au contraire sur les 13 Fallen Heroes, des **Minion** qui portent le trait METAZOMBIE. Les deux lectures sont documentées et cohérentes carte par carte, mais un Fallen Hero en jeu ne protège pas le Cœur et sa défaite ne déclenche pas Rupture. Ce point est à faire valider une fois, globalement.
5. ~~Commentaires périmés~~ : **NETTOYÉS le 27/10/2026** (code inchangé) : `hg013` (Devour hg009, Web hg010, Absorption hg011), `hg031`/`hg033` (le triple hg033 est voulu), `hg042` (manigance annexe, plus « TRAITRISE »), `hg043` (l'attache EST codée), `hg048` (`SetHealth`, plus `DealDamage`), `hg062`/`hg063` (plus de contournement `ThisGainKeyword` décrit comme actif), `hg051`-`hg055` (contexte « mises de côté, jamais en jeu » remplacé par la règle du livret ; en-têtes de hg052-hg055 qui citaient « Franklin Richards » à la place de leur propre allié), `hg026`, `hg029`, `hg038`, `hg023`, `hg064` (« hg046 pas encore écrite »). Restent historiques, et datés comme tels, les en-têtes CORRECTIF eux-mêmes.
6. **Infection : LIMITE et RÉCUPÉRATION, codées le 27/10/2026** (fiche `mots-cles/infection.md`, créée ce jour). Livret relu mot à mot (p. 5, p. 6 glossaire « Zombie version », p. 7 étape 3, p. 8 Expert / Défaite / FAQ) :
   - p. 5 « The limit is **7** in Standard and **6** in Expert. Changing form does not remove Infection. » ; « When you reach the limit, **your hero is defeated** and its zombie version enters play: if it is a Metazombie, at the right end of the row (unless there are already 3); if it is a *Fallen Heroes* minion, engaged with the next player; if your hero has no zombie version, put a Metazombie from the Horde deck into play. » ; FAQ p. 8 « My hero dies from Infection in a solo game. You lose: there are no heroes left. The zombie version only enters play if players remain, and its hit points use the starting number of players. »
   - p. 5 « **Basic recovery:** choose between healing your REC in damage, as usual, or **removing 3 Infection counters**. You cannot do both. » Le choix se présente donc **à chaque récupération de base** (pouvoir d'alter-ego), pas à une étape de fin de round.
   - **Contenu : rien ne manque.** Les 9 versions Metazombie (hg007-hg015) et les 13 sbires Fallen Heroes (hg059-hg071) existent ; `hg004a` met déjà de côté celle du héros choisi.
   - Code (`commun.py`, branché dans `ReglesDuScenario`, condition `coeur_en_jeu`) : `AfterCounterPlacedOn(Scenario, identité, 'infection', at_least=LimiteInfection)` (7, ou 6 si `Worlds.IsExpert`) -> `MortParInfection` : joueur suivant calculé AVANT la défaite, `Faces.DefeatUnits([identité], Cœur)` (modèle `sl072b` Creeping Corruption ; `Identity.OnBeDefeated` élimine le joueur, en solo la partie est perdue), puis, s'il reste des joueurs, `MettreLaVersionZombieEnJeu` : Metazombie -> `_EntrerDansLaRangee` (factorisé hors de `MettreUnMetazombieEnJeu`, même gestion du jeton, refusé à 3) ; Fallen Heroes -> `PutIntoPlay(joueur suivant)` (engagé avec lui) ; aucune version -> `MettreUnMetazombieEnJeu`. Les PV « par joueur » lisent nativement `started_player_num`. Récupération : `WhenUnitMakeRecovery(Scenario, alter-ego)`, offerte seulement si l'identité porte au moins 1 Infection -> `ChoixDeRecuperation` (`ChooseAbilities` : soigner, ou `SetBeInstead` + retrait de min(3, stock) compteurs ; modèle `35030` Death Factor).
   - Cas (14, préfixe `[hg] regle Infection LIMITE` / `RECUPERATION`, vérificateur `hg_infection_etat`) : standard 6 -> 7 par morsure (vaincu, partie perdue) ; témoin standard 5 -> 6 (survit) ; expert (`rhino_expert`) 5 -> 6 (vaincu) ; témoin expert 4 -> 5 ; témoin sans le Cœur 6 -> 7 (rien) ; à deux en vraie mise en place : Spider-Man -> hg010 au bout droit de la rangée (3 Metazombies), Hawkeye -> hg060 engagé avec le joueur suivant, Black Panther (aucune version) -> un Metazombie du Horde deck, témoin du plafond (déjà 3 : hg010 n'entre pas), témoin 5 -> 6 ; récupération : branche soin (5 dégâts -> 2, Infection 4 intacte), branche Infection (4 -> 1, 0 soin), branche Infection avec 2 compteurs (-> 0), témoin sans le Cœur (aucun choix, soin normal).
   - **Substitution tracée le 27/10/2026** : (a) capacité de limite retirée -> les 6 cas sujets de la limite passent au rouge, les 5 témoins restent verts ; (b) capacité de récupération retirée -> les 2 cas « branche Infection » au rouge ; (c) `MettreLaVersionZombieEnJeu` neutralisé -> les 3 cas d'entrée (hg010, hg060, Horde deck) au rouge ; (d) limite expert forcée à 7 -> le cas expert au rouge.
   - **À CONFIRMER** (lectures choisies, sans effet observable connu dans ce pack) :
     - (i) la branche « retirer 3 Infection » REMPLACE la récupération (`SetBeInstead`) : les réponses « après une récupération » (`AfterUnitRecovery`, `AfterUnitUseBasicPower` REC, ex. `tg007` Foreverglade, `45015` Sidekick) ne partent PAS dans cette branche. Autre lecture possible : c'est toujours une « basic recovery » qui soigne 0, et ces réponses partiraient.
     - (ii) « enters play » est lu comme une MISE EN JEU, pas une révélation : le When Revealed d'un Fallen Hero (ex. hg060 « Deal 2 damage to each ally you control ») ne se déclenche pas quand il entre comme version zombie.
     - (iii) Version Metazombie refusée parce que la rangée est pleine : elle reste mise de côté et ne revient plus (le livret ne prévoit rien d'autre ; pas de repli « Metazombie du Horde deck », réservé au héros SANS version zombie).
     - (iv) « the next player » = le joueur suivant dans l'ordre du tour au moment de la mort (`Worlds.GetNextPlayer`, calculé avant l'élimination). La défaite est attribuée au Cœur (`killer`), ce qui ne change rien tant qu'aucune carte ne lit « l'ennemi qui a vaincu le héros ».

---

## Le Cœur, la manigance principale et l'environnement (set « The Hunger Core », hg001-hg006)

### hg001 : The Hunger Core (I) — Heartbeat (méchant, stade 1)

- [x] Étape 2 : références : Shielded by the Horde = `AbilityFactory.CannotBeAffectedByPlayerCards(while_fn=...)`, modèle Kree Leader `gs138a` ; Just a Core X = `WhenUnitWouldAttack` + `SetBeInstead` + `DealEncounterCards` (moitié « attaque » de `gs138a`) ; Rupture X = `WhenUnitBeDefeated` filtré `CardFinder(traits=["METAZOMBIE"], card_type=Villain)`. Code mutualisé dans `CapacitesDuCoeur` (`the_hunger_core/__init__.py`), qui porte aussi depuis le 27/10/2026 les règles du livret sans carte (`commun.ReglesDuScenario` : jeton, Metazombie vaincu, Infection, voir « Corrections du 27/10/2026 »). Fiches : shielded-by-the-horde, just-a-core-x, rupture-x, horde-metazombies.
- [x] Étape 5 : mots-pièges : « against a player in hero form » = `joueur.IsHero()` (en alter-ego, la manigance native s'applique, rien à coder) ; « instead of attacking » = `SetBeInstead` ; les dégâts de Rupture ignorent le bouclier (ils sont infligés par le Cœur lui-même). Rien à confirmer.
- [x] Étape 6 : nombres : PV `12*`, SCH 1 (`desc`) ; Just a Core 1 = `just_a_core=1` ; Rupture 1[per_hero] = `rupture_x * NombreDeJoueurs`. Conformes.
- [ ] Étape 7 (partielle) : 6 cas : bouclier (attaque refusée, retombe sur Rhino) ; exposé (2 dégâts) ; témoin sans bouclier ; Rupture (1 dégât malgré un autre Metazombie qui blinde le Cœur) ; Just a Core (1 carte face cachée, 0 dégât) ; alter-ego (manigance normale). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête (le Cœur est en jeu dès le Setup des 8 parties).
- [x] Étape 8 bis : NON (les cartes de rencontre face cachée distribuées par Just a Core sont une mécanique native, déjà dessinée).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg002 : The Hunger Core (II) — Hunger (méchant, stade 2)

- [x] Étape 2 : références : `CapacitesDuCoeur` (comme hg001) ; When Revealed = `AbilityFactory.WhenThisRevealed` + `commun.PoserInfection` sur chaque joueur. Le Reveal part via `AdvanceVillainStage(..., call_reveal=True)` (Deeper Inside) ou au départ en expert.
- [x] Étape 5 : mots-pièges : « Each player » = boucle sur `Worlds.GetPlayers`. Texte du Cœur identique à hg001, Just a Core 1.
- [x] Étape 6 : nombres : PV `15*`, SCH 2, Just a Core 1, Rupture 1*, 1 compteur Infection. Conformes.
- [ ] Étape 7 (partielle) : When Revealed : 1 cas (chaque joueur pose 1 Infection, solo). Capacités du Cœur : couvertes par les cas hg001 (même fonction) et vues en jeu via le cas hg004b (le Cœur avance en hg002). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (pose un compteur Infection, un nouveau compteur `'infection'` ajouté à `CardFace.COUNTER` le 27/10, dont l'affichage n'a jamais été vérifié) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg003 : The Hunger Core (III) — Hive (méchant, stade 3)

- [x] Étape 2 : références : comme hg002 ; Steady natif (`desc.Steady`, fiche steady.md).
- [x] Étape 5 : mots-pièges : Just a Core PASSE À 2 (`just_a_core=2`) ; Steady sans code.
- [x] Étape 6 : nombres : PV `18*`, SCH 3, Steady 1, Just a Core 2, Rupture 1*, 1 Infection. Conformes.
- [ ] Étape 7 (partielle) : 2 cas ajoutés le 27/10/2026 : When Revealed (1 Infection) ; Just a Core 2 (2 cartes face cachée, 0 dégât, vérificateur `hg014_etat`). Non couvert : Steady (natif) et Deeper Inside II -> III en expert. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay : n'apparaît qu'en mode expert ; non attestée dans la fournée rapportée (mode non précisé).
- [ ] Étape 8 bis : OUI (compteur Infection) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; Étape 7 partielle (chemin expert) ; Étape 8 bis absente ; jamais vue en autoplay.

### hg004a : The Devourer's Skin (manigance principale 1, face A : Setup)

- [x] Étape 2 : références : Contents et villain I/II = champs du fichier scénario (modèle ap005a) ; set aside = champ `set_aside` ; `Villains.SetRule(the_villain="Active")` (fiche mechants-multiples, modèle ap005a) ; `commun.RetirerZombiesEtSurvivorsHomonymes`, `ConstruireLeHordeDeck` et `MettreUnMetazombieEnJeu` ×2 (fiche horde-metazombies).
- [x] Étape 5 : mots-pièges : « Fallen Heroes (without the zombie versions set aside) » : ils sont déjà mélangés par le Setup générique et doivent être RETIRÉS explicitement (`SetupCards.SetAsideCards`) ; correspondance des homonymes par NOM (Wolverine et Blade sont aussi des héros jouables) ; « remove that ally and its Trapped Survivor from the game » = retirés du jeu, pas seulement mis de côté.
- [x] Étape 6 : nombres : 2 Metazombies en jeu ; Horde deck 9 (8 si un héros homonyme est choisi). Conformes.
- [ ] Étape 7 (partielle) : 5 cas sur le vrai scénario : ms_marvel (Cœur hg001, 2 Metazombies, Horde 9) ; iron_man (hg008 absent, Horde 8) ; wolverine (hg076 et hg055 retirés du jeu, hg055 désormais cherché aussi dans le deck de rencontre) ; **27/10** jeton posé sur le PREMIER Metazombie de la rangée (p. 7, étape 7 ; il restait sur le Cœur) ; les 5 Trapped Survivor dans le deck de rencontre. Non couvert : retrait d'un Fallen Hero homonyme (ex. un héros Hawkeye -> hg060 mis de côté). Substitution : faite pour le jeton (rouge sans le crochet d'entrée).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête (Setup des 8 parties).
- [ ] Étape 8 bis : OUI (mise de côté, retrait du jeu, Horde deck qui est une zone propre au scénario, 2 Metazombies en jeu) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg004b : The Devourer's Skin (manigance principale 1, face B)

- [x] Étape 2 : références : Deeper Inside = `WhenUnitWouldBeDefeated` + `SetBeInstead`, puis `AdvanceMainScheme` (modèle Klaw 01116b/01117b) et `coeur.Advance(to_villain=ProchainStadeDuCoeur)` ; défaite si accomplie = `WhenMainSchemeStageWouldBeCompleted` + `SetGameOver(False)` (modèle AvP `ap005b`).
- [x] Étape 5 : mots-pièges : « instead » annule la défaite du Cœur, donc l'avancée de stade du méchant est rejouée À LA MAIN ; Rupture peut vaincre le Cœur même blindé (FAQ p. 8) ; hg005a sans menace s'auto-avance en hg005b (mesuré).
- [x] Étape 6 : nombres : départ `1*`, escalade `1*`, seuil `9*`. Conformes.
- [ ] Étape 7 (partielle) : 2 cas : Deeper Inside (manigance en hg005b, méchant hg002, partie non finie) ; accompli à 9 -> perdu. Non couvert : le passage II -> III en expert. Substitution : confirmée pour ce module d'après son en-tête (aucun chiffre rouges/total tracé).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (le Cœur est remplacé par une carte GÉNÉRÉE pour son stade suivant et la manigance change de face) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; Étape 8 bis absente ; chemin expert non testé.

### hg005a : The Innards (manigance principale 2, face A)

- [x] Étape 2 : références : texte d'ambiance seul, `GetAbilities() -> []`.
- [x] Étape 5 : mots-pièges : aucun texte de règle ; aucune menace imprimée, donc auto-avance native vers hg005b (`MainScheme.OnAfterCardRevealedEnd`).
- [x] Étape 6 : nombres : Stage 2 seulement.
- [x] Étape 7 : aucune capacité : pas de cas propre (le passage hg005a -> hg005b est mesuré par les cas hg004b/hg005b).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON.
Carte terminée : NON (provisoire) : partie réelle humaine.

### hg005b : The Innards (manigance principale 2, face B)

- [x] Étape 2 : références : `SetupCards.PutIntoPlay(name="Inside Galactus", card_type=Environment)` (modèle ap005a) + `MettreUnMetazombieEnJeu` ×2 ; défaite si accomplie = même capacité que hg004b.
- [x] Étape 5 : mots-pièges : « (max. 3 in play) » porté par `MettreUnMetazombieEnJeu` (`MAX_METAZOMBIES_EN_JEU`).
- [x] Étape 6 : nombres : départ `1*`, escalade `1*`, seuil `11*`, 2 Metazombies, plafond 3. Conformes.
- [ ] Étape 7 (partielle) : 2 cas : révélée (Inside Galactus en jeu, 3 Metazombies, le plafond refuse le 4e) ; accompli à 11 -> perdu. **Substitution mesurée** d'après le script : le cas « accompli » reste VERT sans module (filet générique de fin de partie sur le dernier stade, assumé, pas maquillé).
- [x] Étape 7 bis : limite imprimée ? OUI (max. 3 en jeu) : témoin fait (2 en jeu + 2 demandés = 3, le 4e est refusé).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (environnement et Metazombies mis en jeu depuis le Horde deck) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; Étape 8 bis absente.

### hg006 : Inside Galactus (environnement)

- [x] Étape 2 : références : +1 ATK = `GiveKeywordToInPlayWhenApplyThis(CardFinder(check_face_fn=_est_le_mechant_actif), attack=1)`, modèle sk096 Tarnax VII ; Digestive Juices = `WhenVillainPhaseEnd` + `TakeIndirectDamage`, modèle cr016.
- [x] Étape 5 : mots-pièges : « The villain » = celui qui porte le jeton actif (Cœur compris), pas tous les Metazombies ; `change_on_event=OnEvent.Counter(..., 'active')` est indispensable (sans lui, le bonus restait sur l'ancien porteur, mesuré) ; « each player ».
- [x] Étape 6 : nombres : +1 ATK, 2 dégâts indirects. Conformes.
- [ ] Étape 7 (partielle) : 3 cas : +1 ATK sur le méchant actif ; le bonus suit le jeton ; 2 dégâts indirects en fin de phase méchant. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête (en jeu une fois hg005b révélée).
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée. (Le jeton actif, dont dépend « the villain », tourne enfin depuis le 27/10/2026 : correction 1.)

---

## Le Horde deck : les 9 Metazombies (hg007-hg015)

Préambule commun. Ce sont des `Villain` au trait METAZOMBIE (« a villain for all purposes »). Leurs scripts vivent dans `horde_deck_metazombies/` : un fichier mal placé se charge en `GetAbilities() -> []` sans aucune erreur, le piège est documenté dans hg007. Les noms en gras (« Shield », « Storm », « Web », « Absorption », « Ambush », « Hex », « Portal to Limbo », « Devour », « Upgrades ») sont des **noms d'ambiance**, pas des mots-clés, selon l'arbitrage utilisateur du 27/10/2026. Partout, « ACTIVATES » couvre l'attaque ET la manigance (`AfterEnemyActivatesAgainstYou`, jamais `AfterUnitAttackUnit` seul).

### hg007 : Zombie Captain America

- [x] Étape 2 : références : Leader of the Horde = `GiveKeywordToInPlayWhenApplyThis(CardFinder(traits=["METAZOMBIE"], card_type=Villain), attack=1, not_include_this=True)`, modèle sk099 ; Shield = `WhenUnitWouldTakeDamage(ForcedInterrupt)` + `ReduceDamage`, modèle ag002, avec `.LimitOncePerPhase()` (modèles ar007 et sm010).
- [x] Étape 5 : mots-pièges : « each OTHER Metazombie » (pas lui-même, pas le Cœur) ; « would take damage » sans restriction à l'attaque ; réduction sans minimum imprimé ; « the first time each phase ».
- [x] Étape 6 : nombres : SCH 1, ATK 2, PV `12*`, +1 ATK, réduction 2. Conformes.
- [ ] Étape 7 (partielle) : 3 cas : un autre Metazombie gagne +1 et pas lui ; premier dégât réduit de 2 ; témoin d'épuisement. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (« the first time each phase ») : témoin fait, second dégât dans la même phase non réduit (3 + 5 = 8, pas 3 + 3).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg008 : Zombie Iron Man

- [x] Étape 2 : références : entrée en jeu = `Ability(ForcedResponse, Message.AfterCardPutIntoPlay, ...)` construite à la main (aucune fabrique, modèle asset.py:153) + `commun.DefausserJusquaUneAmeliorationDuDeckSignature` (adapté de 04115 Zola's Mutate) ; Upgrades = `ThisGainKeyword(len(GetAttachedAttachments()), attack=1, change_on_event=OnEvent.AttachedMove(Attachment))`, modèle 04114.
- [x] Étape 5 : mots-pièges : « his signature deck », pas le deck de rencontre ; `AfterCardEnterPlay` n'écoute PAS `PutIntoPlay` (piège mesuré, traces via `MCLCG_TRACE_CRASH`) ; une carte rangée dans le deck signature a déjà `bind_face == metazombie`, d'où un passage par `area_processing` avant `AttachTo2` (piège moteur documenté dans `commun.py`) ; « for each attachment ON HIM » = toutes ses améliorations.
- [x] Étape 6 : nombres : SCH 2, ATK 1, PV `11*`, +1 ATK par amélioration. Deck signature de 5 cartes (livret « 5 for Zombie Iron Man »). Conformes.
- [ ] Étape 7 (partielle) : 3 cas : une amélioration attachée à l'entrée (+1) ; témoin d'échelle (2 attachements, +2) ; les 4 cartes non attachées restent dans le deck signature. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (attache une carte tirée d'un deck privé et remélange ce deck) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg009 : Zombie Hulk

- [x] Étape 2 : références : Overkill permanent par la voie dynamique `WhenUnitWouldAttackUnit(ForcedInterrupt)` + `GainOverKill`, modèle 40074b Harpoon (fiche overkill) ; Devour = `AfterUnitDefeatedUnit(ForcedResponse, "This", Ally)` + `HealHealth`.
- [x] Étape 5 : mots-pièges : Overkill sur toute attaque (Identity|Ally) ; Devour seulement sur un ALLIÉ vaincu ; « maximum hit points » = `max_health` de l'allié ; c'est LUI qui est soigné.
- [x] Étape 6 : nombres : SCH 0, ATK 4, PV `15*`. Conformes.
- [ ] Étape 7 (partielle) : 2 cas : Black Cat (2 PV) défend, l'excès passe et Hulk est soigné ; témoin (Hulk allié qui survit : ni excès ni soin). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg010 : Zombie Spider-Man

- [x] Étape 2 : références : `AfterUnitAttackAndDamageUnit(ForcedResponse, "This", Hero, target_in_play=True)` + `GiveStatus("Stunned")`, modèle 60166 Kingpin's Cane.
- [x] Étape 5 : mots-pièges : « a HERO » (un allié défenseur ne déclenche rien) ; « deals damage » sans « attacks » : ce sont ses seuls dégâts possibles, lecture équivalente.
- [x] Étape 6 : nombres : SCH 2, ATK 2, PV `9*`. Conformes.
- [ ] Étape 7 (partielle) : 2 cas : héros blessé puis étourdi ; contre-cas allié défenseur (rien). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay : **jamais en partie** (héros spider_man, donc exclu du Horde deck).
- [ ] Étape 8 bis : OUI (statut Étourdi posé par script) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente ; jamais vue en autoplay.

### hg011 : Zombie Captain Marvel

- [x] Étape 2 : références : Absorption = `AfterUnitAttackUnit(ForcedResponse, Hero|Ally, "This")` + `PlaceCountersOn(..., 'energy', maximum=5)` (modèles 55044 et ap304) ; +1 ATK par compteur = `ThisGainKeyword(... GetCounters('energy'), change_on_event=OnEvent.Counter)`, modèle 19001a Drax ; retrait après son attaque = `RemoveCountersOn`.
- [x] Étape 5 : mots-pièges : « after SHE is attacked » sans condition de dégâts ; « after she ATTACKS » = l'autre côté du message ; « (max. 5) » géré par `maximum=5` ; pas de minimum au retrait. Piège de harnais : `"cibles": ["hg011"]` est requis même s'il n'y a qu'un seul ennemi.
- [x] Étape 6 : nombres : SCH 1, ATK 1, PV `10*`, +1 compteur, plafond 5, -1 compteur. Conformes.
- [ ] Étape 7 (partielle) : 4 cas : attaquée (1 compteur, +1 ATK) ; plafond ; retrait après son attaque (3 -> 2) ; témoin à vide (attaque à 0 compteur sans planter). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (max. 5) : témoin d'épuisement du plafond fait (déjà 4 compteurs, deux attaques, reste à 5).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (compteurs energy) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg012 : Zombie Thor

- [x] Étape 2 : références : `AfterEnemyActivatesAgainstYou(ForcedResponse, "This")` (modèles nt013 et 27158) + `GetAgainstPlayer().GetControlAllies()` + `DealDamage(..., 1)`, modèle 24044 Boomerang.
- [x] Étape 5 : mots-pièges : « ACTIVATES » (manigance comprise) ; « each ally THAT PLAYER controls » ; dégâts directs ; l'identité n'est pas touchée (le modèle 18746, qui la touche, est écarté).
- [x] Étape 6 : nombres : SCH 1, ATK 3, PV `13*`, 1 dégât. Conformes.
- [ ] Étape 7 (partielle) : 3 cas : attaque (l'allié subit 1) ; manigance en alter-ego (l'allié subit 1 quand même) ; sans allié (aucun plantage). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg013 : Zombie Black Widow

- [x] Étape 2 : références : `UnitCannotDefend(Ally, "This", cannot_trigger_defense_ability=True)`, croisement de ap305 et de ip034/gs190 ; Stalwart natif.
- [x] Étape 5 : mots-pièges : « ALLIES » seulement ; « ZOMBIE BLACK WIDOW's attacks » seulement ; « Ambush » = ambiance (arbitrage utilisateur).
- [x] Étape 6 : nombres : SCH 1, ATK 1, PV `9*`, Stalwart 1. Conformes.
- [ ] Étape 7 (partielle) : 3 cas (vérificateur `hg_peut_defendre_etat`, qui lit `IsCanDefense`) : l'alliée ne peut pas défendre contre elle ; contre-cas avec un autre ennemi ; ligne de base sans hg013. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg014 : Zombie Doctor Strange

- [x] Étape 2 : références : `AfterEnemyActivatesAgainstYou(ForcedResponse, "This")` (comme hg012) + `joueur.DealEncounterCards(1)`, modèle sk065.
- [x] Étape 5 : mots-pièges : « activates » ; « against YOU » = `GetAgainstPlayer()` ; pas de « instead » (contrairement à Just a Core, l'attaque se résout ET la carte est distribuée) ; « Hex » = ambiance.
- [x] Étape 6 : nombres : SCH 2, ATK 1, PV `10*`, 1 carte. Conformes.
- [ ] Étape 7 (partielle) : 3 cas (`hg014_etat`) : attaque (dégâts ET 1 carte) ; manigance (1 carte) ; contre-cas avec l'activation d'un autre Metazombie (0 carte). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (carte de rencontre distribuée face cachée, native).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg015 : Zombie Magik

- [x] Étape 2 : références : `AfterEnemyActivatesAgainstYou` ; garde « pas engagé » = `engaged_minions.GetSize() == 0` (modèle Kingpin 60159b) ; fouille = `Worlds.DiscardEncounterCardsUntil(card_type=Minion)` + `PutIntoPlay` (modèle 32109 Master Mold) ; remélange = `ShuffleAllTo(..., "EncounterDeck")` (modèle 60161b) ; Metazombie de repli = `MettreUnMetazombieEnJeu`.
- [x] Étape 5 : mots-pièges : la garde « not engaged » couvre TOUTE la capacité ; « put IT » = le sbire trouvé ; « Then shuffle » APRÈS la mise en jeu et sans condition ; « If NO minion is discarded » = résultat de la fouille ; « fewer than 3 » relu au moment de la résolution.
- [x] Étape 6 : nombres : SCH 1, ATK 2, PV `10*`, plafond 3 (`MAX_METAZOMBIES_EN_JEU`). Conformes.
- [ ] Étape 7 (partielle) : 6 cas : sbire trouvé, engagé, défausse remélangée ; manigance en alter-ego ; contre-cas « déjà engagé » (rien) ; **27/10** branche « aucun sbire -> un Metazombie entre » (vrai scénario, Horde deck construit : 1 -> 2 Metazombies) et son témoin sans activation (reste 1) ; **27/10** plafond : déjà 3 Metazombies -> aucun 4e. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (« fewer than 3 Metazombies ») : témoin fait le 27/10/2026 (3 en jeu, Portal to Limbo sans sbire -> toujours 3).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (sbire sorti du deck de rencontre et mis en jeu, Metazombie sorti du Horde deck) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

---

## Decks signature : Zombie Captain America (hg016-hg018)

### hg016 : Thrown Shield

- [x] Étape 2 : références : 24035 Mister Hyde (texte identique à la valeur près) : `DealDamage(GetOnFieldHeroes + GetOnFieldAllies, 2)`.
- [x] Étape 5 : mots-pièges : « each HERO » (un alter-ego n'encaisse pas, d'où le rejet de `GetOnFieldFriendlyCharacters`) ; « each ally IN PLAY », tous joueurs confondus ; trait ATTACK = saveur.
- [x] Étape 6 : nombres : 2 dégâts. Conformes.
- [ ] Étape 7 (partielle) : 4 cas : forme héros + allié (2 chacun) ; alter-ego (rien sur l'identité) ; deux joueurs ; aucun allié. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg017 : Avengers, Feast!

- [x] Étape 2 : références : `commun.Metazombies` + `Players.ForEachPlayer` + `DoActivate(..., do_not_give_boost=True)`, modèles sl039b, gb020 et 56187.
- [x] Étape 5 : mots-pièges : « EACH Metazombie » (pas le Cœur, et sans regarder le jeton) ; « activates » ; « against each player » ; « Do not deal boost cards ». À CONFIRMER : l'ordre (Metazombie par Metazombie, puis joueur par joueur) n'a aucun effet observable connu.
- [x] Étape 6 : nombres : aucun.
- [ ] Étape 7 (partielle) : 7 cas : aucun Metazombie ; un seul (1 dégât) ; deux (5 cumulés) ; manigance en alter-ego ; deux joueurs ; « pas de boost » (deck de Charge 01099) ; témoin avec activation directe AVEC boost. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg018 : Dented Vibranium Shield

- [x] Étape 2 : références : ts006 Bladed Armor (presque mot pour mot) : `AttachToFaceWhenPutIntoPlay(CardFinder(card_ids=["hg007"]))`, `GiveKeywordToAttached(retaliate=2)`, `PlayerActionToDiscardThis(HeroAction).SetCost(Cost("2"))`.
- [x] Étape 5 : mots-pièges : Retaliate est DONNÉ par l'amélioration (pas dans `desc`) ; « Spend 2 resources » = `Cost("2")` (« of any type » par défaut) ; Hero Action.
- [x] Étape 6 : nombres : Retaliate 2, coût 2. Conformes.
- [ ] Étape 7 (partielle) : 5 cas : attachée avec Retaliate 2 ; témoin sans bouclier ; riposte en jeu (2 dégâts) ; posée sans hôte (défaussée) ; Hero Action. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (s'attache à un Metazombie) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

---

## Decks signature : Zombie Iron Man (hg019-hg023)

Préambule commun (hg019-hg022). Ces améliorations ne sortent du deck signature QUE par `commun.DefausserJusquaUneAmeliorationDuDeckSignature` (entrée en jeu de hg008, ou hg023) : c'est ce canal qui fait l'attache, d'où l'absence de `AttachToFaceWhenPutIntoPlay` sur hg019, hg021 et hg022. hg020 en pose une, sans effet sur ce canal. Le patron « Hero Action: Spend N resources -> discard this card » donne `PlayerActionToDiscardThis(HeroAction).SetCost(Cost("N"))`. **À CONFIRMER** (hg019, hg020, hg021) : un « Spend N resources » nu est lu « of any type ». Les cas utilisent `IRON_MAN_NU` : l'amélioration TIRÉE AU HASARD à l'entrée de hg008 est retirée, puis le cas attache celle qu'il veut tester.

### hg019 : Necrotic Repulsors

- [x] Étape 2 : références : `UnitAttackGainKeyword(CardFinder(name="Zombie Iron Man"), piercing=True)` (modèle 27078, sur une amélioration tierce) ; coût générique `Cost("2")` (modèle sq017).
- [x] Étape 5 : mots-pièges : « His » = Zombie Iron Man ; toutes ses attaques ; Hero Action ; « any type » à confirmer (préambule).
- [x] Étape 6 : nombres : coût 2.
- [ ] Étape 7 (partielle) : 3 cas : Piercing (Tenace défaussée) ; témoin sans l'amélioration ; Hero Action. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (attachée à hg008) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg020 : Patched Armor

- [x] Étape 2 : références : 01119 Solid-Sound Body (triplet attache + bonus + défausse) ; `GiveKeywordToAttached(health="2*")` (modèles 21136a et 21137a).
- [x] Étape 5 : mots-pièges : « +2* » est une chaîne par héros (pas `2`) ; coût générique ; Hero Action.
- [x] Étape 6 : nombres : +2* PV, coût 3. Conformes.
- [ ] Étape 7 (partielle) : 2 cas : +2 PV (solo, l'échelle par héros n'est pas éprouvée) ; Hero Action (bonus perdu). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (attachée à hg008) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente ; échelle 2* non testée à plusieurs.

### hg021 : Rotten Thrusters

- [x] Étape 2 : références : `GiveKeywordToAttached(Villain, scheme=1)` (modèle 27149) ; `UnitCannotBeAttacked("AttachedVillain", conditions=[Ally.IsType(message.attacker)])` (modèles 27152, rl014 et 58030) ; `Cost("2")`.
- [x] Étape 5 : mots-pièges : « by ALLIES » seulement (le héros attaque normalement) ; +1 SCH pour lui seul ; « any type » à confirmer.
- [x] Étape 6 : nombres : +1 SCH, coût 2.
- [ ] Étape 7 (partielle) : 4 cas : +1 SCH ; Black Cat ne peut pas l'attaquer ; témoin sans l'amélioration ; Hero Action. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (attachée à hg008) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg022 : Necrotic Unibeam

- [x] Étape 2 : références : `UnitAttackGainKeyword("AttachedVillain", overkill=True)` (modèle 27147 Arm Cannon) ; `AfterUnitAttackUnit(ForcedResponse, "AttachedVillain", "You")` + `GetControlAllies` (modèles 24044 et hg012) ; `Cost("BBB")` (modèle sl063).
- [x] Étape 5 : mots-pièges : « His ATTACKS » (pas les activations) ; « the attacked player » ; alliés de ce joueur seulement ; [mental]×3. **À CONFIRMER** : ForcedResponse plutôt que ForcedInterrupt (aucune différence observable connue).
- [x] Étape 6 : nombres : 1 dégât, coût BBB. Conformes.
- [ ] Étape 7 (partielle) : 6 cas : Overkill ; témoin sans l'amélioration ; dégâts aux alliés ; témoin ; Hero Action payée avec 2 Genius ; Hero Action REFUSÉE avec un seul Genius. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (attachée à hg008) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg023 : Hunger Protocol

- [x] Étape 2 : références : `DefausserJusquaUneAmeliorationDuDeckSignature` (partagé avec hg008) ; `DoActivate(joueur)` contre « you » ; Surge = `ThisCardGainSurge` (modèle rl015).
- [x] Étape 5 : mots-pièges : « 2 OR MORE attachments » (`>= 2`) ; « Otherwise » exclusif ; « If you cannot » ne porte que sur la branche d'attache ; Iron Man absent : Surge (garde défensive).
- [x] Étape 6 : nombres : seuil 2. Conforme.
- [ ] Étape 7 (partielle) : 3 cas : 2 améliorations -> il active ; 1 seule -> attache (pas d'activation) ; Iron Man absent -> Surge. Non couvert : un deck signature SANS amélioration (Surge par la branche d'attache). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (seuil « 2 or more ») : témoin fait des deux côtés du seuil (2 -> activation, 1 -> attache).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (branche d'attache depuis le deck signature) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

---

## Decks signature : Zombie Hulk (hg024-hg026)

### hg024 : Hulk Hungry!

- [x] Étape 2 : références : 50076 Attacrobatics (`IsAlterEgo` -> `ChangeToForm(Hero)` -> `FindVillain`) ; `DoActivate` (modèle hg017).
- [x] Étape 5 : mots-pièges : changement de forme seulement « if alter-ego » ; « activates » (en pratique une attaque, puisque la forme est déjà héros) ; « you » = `GetToPlayer`. À CONFIRMER : Zombie Hulk absent, garde défensive (rien).
- [x] Étape 6 : nombres : aucun.
- [ ] Étape 7 (partielle) : 3 cas : alter-ego -> héros + 4 dégâts ; déjà héros -> 4 dégâts ; Hulk absent -> changement de forme seul. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (le changement de forme est natif et déjà dessiné).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg025 : Smash

- [x] Étape 2 : références : `ChooseAbilities` + `ForChoiceAbility` (01173, 40125) ; `GetControlCardsByType` (50119) + `Faces.DiscardAll` ; héros = `GetAllIdentityFace` filtré sur Hero (ss022, 60012).
- [x] Étape 5 : mots-pièges : choix toujours offert, même vide ; « that type » = le type choisi seulement ; « If you control none » se lit sur le type choisi ; « your HERO » quelle que soit la forme ; « Smash » = titre d'ambiance.
- [x] Étape 6 : nombres : 3 dégâts. Conforme.
- [ ] Étape 7 (partielle) : 4 cas : Support ×2 défaussés ; contre-cas « that type » ; Upgrade ×2 ; Upgrade sans upgrade (3 dégâts). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (défausse standard et dégâts).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg026 : Endless Rage

- [x] Étape 2 : références : ld007 Reaver Commander (`AttachToFaceWhenPutIntoPlay` + `GiveKeywordToAttached(steady=1)`), ici avec `attack=1` dans le même appel ; `Cost("3")` (modèle sf014).
- [x] Étape 5 : mots-pièges : Steady et +1 ATK dans le même appel ; pas « (any player) » ; si l'attache échoue, filet natif (défausse générique plutôt qu'au fond du deck signature : écart théorique noté).
- [x] Étape 6 : nombres : +1 ATK, coût 3.
- [ ] Étape 7 (partielle) : 3 cas : attachée (Steady, 4 -> 5) ; témoin sans Hulk (hors jeu) ; Hero Action. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (attachée à hg009) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

---

## Decks signature : Zombie Spider-Man (hg027-hg029)

Préambule : ces trois cartes ne peuvent pas apparaître dans l'autoplay rapporté (héros Spider-Man, donc hg010 et son deck signature sont exclus).

### hg027 : Rotten Web

- [x] Étape 2 : références : 09030 Counterspell (`AttachToFaceWhenPutIntoPlay("YourHero")`) ; 16123 (`GiveKeywordToAttached(thwart=-1, attack=-1)`) ; 16125 The Poison (`Cost("3", different_type=True).AnyPlayerCanDoThis()`).
- [x] Étape 5 : mots-pièges : « your HERO » ; pas de malus DEF ; « (any player) » ; « of DIFFERENT types ».
- [x] Étape 6 : nombres : -1 ATK, -1 THW, coût 3 types différents.
- [ ] Étape 7 (partielle) : 2 cas : malus ATK/THW (DEF inchangée) ; Hero Action avec Energy, Genius et Strength. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay : **jamais en partie** (voir le préambule).
- [ ] Étape 8 bis : OUI (s'attache au héros du joueur) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente ; jamais vue en autoplay.

### hg028 : Dead Spider-Sense

- [x] Étape 2 : références : `Worlds.FindCardOnField(name="Zombie Spider-Man")` (modèle 22031) ; `hand_cards.GetSize()` (27156) ; `DoActivate`.
- [x] Étape 5 : mots-pièges : « the player with the MOST cards » (maximum strict) ; « If tied » : le joueur qui révèle, qu'il soit ou non parmi les ex aequo ; « activates ». À CONFIRMER : lecture du départage (aucun équivalent dans le dépôt).
- [x] Étape 6 : nombres : aucun.
- [ ] Étape 7 (partielle) : 4 cas : solo (2 dégâts et étourdi via Web) ; Spider-Man absent ; deux joueurs, le plus grand (Hawkeye) est visé ; égalité, le joueur qui révèle est visé. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay : **jamais en partie**.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; jamais vue en autoplay.

### hg029 : Rooftop to Rooftop (manigance annexe)

- [x] Étape 2 : références : wd049 (`GiveKeywordToInPlayWhenApplyThis(CardFinder(name=...), scheme=1)`) ; « cannot be attacked by allies » = même filtre que hg021, cible nommée (modèle tg012).
- [x] Étape 5 : mots-pièges : « While this scheme is in play » ne se code pas ; « by ALLIES » ; +1 SCH seulement.
- [x] Étape 6 : nombres : départ `2*` (natif), +1 SCH.
- [ ] Étape 7 (partielle) : 3 cas : +1 SCH ; Black Cat bloquée ; le héros attaque normalement. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay : **jamais en partie**.
- [x] Étape 8 bis : NON (manigance annexe ordinaire).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; jamais vue en autoplay.

---

## Decks signature : Zombie Captain Marvel (hg030-hg033)

Préambule. `DECKS_SIGNATURE["Zombie Captain Marvel"] = [hg030, hg031, hg032, hg033, hg033, hg033]` **n'est pas un bug** : le livret dit « 6 for Zombie Captain Marvel » et `data/encounter_sets/the_hunger_core_sig_zombie_captain_marvel.json` liste trois hg033. Les notes contraires du corps de hg031 et hg033 ont été corrigées le 27/10/2026. Ces cartes sortent par la voie générique (`RevelerLeDessusDuDeckSignature` -> `Reveal`).

### hg030 : Rotten Binary

- [x] Étape 2 : références : hg016 (texte identique, valeur 1) et 24035.
- [x] Étape 5 : mots-pièges : « each HERO » (pas l'alter-ego) ; tous les alliés ; trait COSMIC = saveur.
- [x] Étape 6 : nombres : 1 dégât.
- [ ] Étape 7 (partielle) : 2 cas : héros + allié ; alter-ego (seul l'allié encaisse). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg031 : Photon Fist

- [x] Étape 2 : références : `AttachToFaceWhenPutIntoPlay(CardFinder(name="Zombie Captain Marvel", card_type=Villain))` (comme hg018 et hg026 : voie de révélation générique, pas le canal Iron Man) ; `UnitAttackGainKeyword(overkill=True)` (comme hg019 et hg022) ; `Cost("2")`.
- [x] Étape 5 : mots-pièges : « Her » = Zombie Captain Marvel ; toutes ses attaques ; pas « (any player) ».
- [x] Étape 6 : nombres : coût 2.
- [ ] Étape 7 (partielle) : 4 cas : révélée puis attachée ; Overkill (1 dégât d'excès) ; témoin sans l'amélioration ; Hero Action. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (attachée à hg011) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg032 : Discharge

- [x] Étape 2 : références : identification par nom (modèle hg023) ; `PlaceCountersOn(maximum=5)` (hg011) ; `RemoveCountersOn("All")`, dont la valeur rendue = « the removed counters » ; `GiveStatus("Stunned")` (sk128) ; dégâts indirects à chaque joueur (11028).
- [x] Étape 5 : mots-pièges : « fewer than 5 » (`< 5`) ; « Then remove all » sans condition ; « she is stunned » ; « each player » ; INDIRECT. À CONFIRMER : Captain Marvel absente, rien (garde défensive).
- [x] Étape 6 : nombres : +1 si < 5, plafond 5. Conformes.
- [ ] Étape 7 (partielle) : 3 cas : 2 -> 3, tout est retiré, étourdie, 3 dégâts indirects ; déjà à 5 (pas d'ajout, 5 dégâts) ; absente. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (« fewer than 5 ») : témoin fait (déjà à 5, aucun ajout, 5 retirés -> 5 dégâts indirects, pas 6).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (compteurs energy retirés, statut Étourdi) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg033 : Energy Hunger (×3 dans le deck signature)

- [x] Étape 2 : références : hg011 (`PlaceCountersOn(..., 'energy', maximum=5)`), cible par nom (modèle hg023).
- [x] Étape 5 : mots-pièges : la cible est NOMMÉE (pas « the active Metazombie ») ; « (max. 5) » = plafond du total ; garde défensive si elle est absente.
- [x] Étape 6 : nombres : +2 compteurs, plafond 5. Conformes. Trois exemplaires (livret + encounter_set).
- [ ] Étape 7 (partielle) : 2 cas : +2 compteurs (+2 ATK) ; plafond (4 -> 5). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (max. 5) : témoin fait (déjà à 4 -> 5, pas 6).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (compteurs energy) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

---

## Decks signature : Zombie Thor (hg034-hg036)

### hg034 : Bloodied Mjolnir

- [x] Étape 2 : références : hg026 (attache + `GiveKeywordToAttached(attack=1)`) ; 21103 Proxima's Spear (`UnitAttackGainKeyword(overkill=True, piercing=True)`) ; Storm +1 = SECONDE `AfterEnemyActivatesAgainstYou(ForcedResponse, cible)` greffée sur le même message que hg012 ; `Cost("3")`.
- [x] Étape 5 : mots-pièges : « His attacks » (Overkill et Piercing) contre Storm (qui couvre l'activation) ; « each ally » = la portée de Storm (alliés du joueur visé) ; « additional » = 1 + 1. **À CONFIRMER** : deux incréments de 1 au lieu d'un seul de 2 (sans effet tant qu'aucune carte ne compte les déclenchements).
- [x] Étape 6 : nombres : +1 ATK, +1 dégât Storm, coût 3.
- [ ] Étape 7 (partielle) : 6 cas : révélée puis attachée (+1 ATK) ; Storm +1 (l'allié subit 2) ; Piercing ; Hero Action ; **27/10** Overkill (Thor ATK 4 abat Black Cat 2 PV qui défend -> 2 dégâts d'excès à l'identité) et son témoin sans Mjolnir (ATK 3, 0 excès). **27/10** : défaite de Thor -> Mjolnir au FOND de son deck signature (cas `regle Metazombie vaincu`). Substitution : non tracée (le témoin sans la carte est un contre-cas).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (attachée à hg012) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Overkill sans cas ; Étape 8 bis absente.

### hg035 : Rotten Lightning

- [x] Étape 2 : références : 01154 Concussive Blast (`GetOnFieldFriendlyCharacters` + `DealDamage`), wc021.
- [x] Étape 5 : mots-pièges : « friendly CHARACTER » = identité dans les deux formes + alliés, tous joueurs.
- [x] Étape 6 : nombres : 2 dégâts.
- [ ] Étape 7 (partielle) : 2 cas : héros + allié (2 chacun) ; alter-ego touché aussi. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg036 : Fallen God of Thunder

- [x] Étape 2 : références : 01104 Rhino « Hard to Keep Down » (`HealthUnits`, garde « rien soigné ») ; `FindVillain(name="Zombie Thor")` ; `DoActivate`.
- [x] Étape 5 : mots-pièges : « If he had no damage » = total soigné nul ; « against you » ; pas de Surge. **À CONFIRMER** : « 4* » écrit dans le texte libre est lu comme « par joueur » (`HealthUnits` accepte "4*").
- [x] Étape 6 : nombres : soin `4*`.
- [ ] Étape 7 (partielle) : 2 cas : blessé à 5, soigné de 4, pas d'activation ; indemne, il active. Substitution : non tracée. Échelle 4* testée en solo seulement.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

---

## Decks signature : Zombie Black Widow (hg037-hg039)

### hg037 : Widow's Bite

- [x] Étape 2 : références : 01106 Stampede (deux `WhenThisRevealed("Alter-Ego"/"Hero")`) ; 04120 Mind Ray (`GiveStatus([GetHero()], "Stunned")`) ; `PoserInfection`.
- [x] Étape 5 : mots-pièges : deux branches selon la forme ; Surge en alter-ego seulement ; « your HERO » ; le joueur qui révèle (pas chaque joueur) ; ordre imprimé respecté.
- [x] Étape 6 : nombres : 1 Infection dans chaque branche.
- [ ] Étape 7 (partielle) : 2 cas : alter-ego (1 Infection + Surge, 01126 révélé) ; héros (étourdi + 1 Infection, pas de Surge). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (compteur Infection, statut Étourdi) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg038 : Infiltrator (manigance annexe)

- [x] Étape 2 : références : hg029 (sans la clause « allies ») ; wd049 et 22029 Self-Preservation (`GiveKeywordToInPlayWhenApplyThis(CardFinder(name=...))`).
- [x] Étape 5 : mots-pièges : +1 SCH seulement ; Hazard natif (icône seule) ; « While in play » ne se code pas.
- [x] Étape 6 : nombres : départ `2*`, Hazard 1 (natifs), +1 SCH.
- [ ] Étape 7 (partielle) : 1 cas (+1 SCH). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (manigance annexe ordinaire).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg039 : Sleeper Agent

- [x] Étape 2 : références : hg024 (texte identique au nom près), 50076.
- [x] Étape 5 : mots-pièges : comme hg024. À CONFIRMER : Black Widow absente, garde défensive.
- [x] Étape 6 : nombres : aucun.
- [ ] Étape 7 (partielle) : 2 cas : alter-ego -> héros, attaquée (1 dégât) ; absente (changement de forme seul). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (changement de forme natif).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

---

## Decks signature : Zombie Doctor Strange (hg040-hg042)

### hg040 : Rotten Eye of Agamotto

- [x] Étape 2 : références : hg026 (attache par nom) ; hg007 (`WhenUnitWouldTakeDamage(ForcedInterrupt, "AttachedVillain")` + `ReduceDamage`) ; `Cost("BB")` (hg022).
- [x] Étape 5 : mots-pièges : « EACH time » (pas de limite, contrairement à hg007) ; toute source de dégâts ; pas de minimum.
- [x] Étape 6 : nombres : réduction 1, coût BB.
- [ ] Étape 7 (partielle) : 3 cas : 3 -> 2 ; « each time » (2 + 2 = 4, contre-preuve d'une limite fantôme) ; Hero Action. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON (le cas « each time » vérifie qu'aucune limite ne mord).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (attachée à hg014) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg041 : Crimson Bands of Cyttorak

- [x] Étape 2 : références : hg027 (`"YourHero"`) ; 32150 Wrapped in Metal (`UnitCannotAttackTarget("AttachedIdentity", cannot_attack=True, cannot_trigger_attack_ability=True)` ; coût composé `SetCost` + `SetCostFunc(CostFunc.Exhaust)`).
- [x] Étape 5 : mots-pièges : « cannot attack » seulement (pas thwart, defend ou recover) ; coût « 2 of different types AND exhaust » ; pas « (any player) ».
- [x] Étape 6 : nombres : coût 2 de types différents + inclinaison.
- [ ] Étape 7 (partielle) : 2 cas : ne peut plus attaquer (Rhino reste à 0) ; Hero Action (défaussée, héros incliné). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (s'attache au héros) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg042 : Hunger Hex (manigance annexe)

- [x] Étape 2 : références : 51041 Playing for Keeps (`GiveKeywordToInPlayWhenApplyThis(Identity, hand_size=...)`), sk090.
- [x] Étape 5 : mots-pièges : « EACH player's » = toutes les identités ; « reduced by 2 » = `-2`. (En-tête du script corrigé le 27/10/2026 : « MANIGANCE ANNEXE », plus « TRAITRISE ».)
- [x] Étape 6 : nombres : départ `3*` (natif), -2 en taille de main.
- [ ] Étape 7 (partielle) : 1 cas (taille de main -2). Non couvert : retour à la normale quand la manigance quitte le jeu. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

---

## Decks signature : Zombie Magik (hg043-hg045)

### hg043 : Soulsword

- [x] Étape 2 : références : `AttachToFaceWhenPutIntoPlay(CardFinder(name="Zombie Magik", card_type=Villain))` (comme hg031 et hg034) ; `GiveKeywordToAttached(attack=1)` (01074) ; `UnitAttackGainKeyword(piercing=True)` (hg019) ; `Cost("3")`.
- [x] Étape 5 : mots-pièges : **CORRIGÉ le 27/10** : l'attache manquait (la lecture « attachée par le canal Iron Man » était fausse : Magik n'a pas ce canal) ; « Her » ; « any type » à confirmer.
- [x] Étape 6 : nombres : +1 ATK, coût 3.
- [ ] Étape 7 (partielle) : 3 cas (avec `Puzzle.Reveal`) : attachée (+1 ATK) ; Piercing ; Hero Action. Le rouge d'AVANT le correctif est attesté par le rapport de fusion (bug trouvé par ces cas) ; substitution du module : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (attachée à hg015) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg044 : Teleportation Disc

- [x] Étape 2 : références : hg017 (boucle `ForEachPlayer` + `do_not_give_boost=True`) ; identification par nom (hg023).
- [x] Étape 5 : mots-pièges : un seul Metazombie NOMMÉ ; « against each player » ; « activates » ; sans boost. À CONFIRMER : ordre des joueurs (rien d'observable).
- [x] Étape 6 : nombres : aucun.
- [ ] Étape 7 (partielle) : 2 cas : solo sans boost (2 dégâts nus) ; deux joueurs (2 sur chaque identité). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg045 : Demons of Limbo

- [x] Étape 2 : références : 40111 Tag Team (sbire de la défausse mis en jeu et engagé) ; wd059 (tri sur `printed_health`) ; sk241 et sl036 (défausse de rencontre filtrée sur Minion). Surge natif (`desc.Surge`).
- [x] Étape 5 : mots-pièges : « MINION » (pas un ennemi quelconque) ; « most hit points » = PV IMPRIMÉS (`.health` vaut 0 hors jeu) ; « engaged with you ». À CONFIRMER : égalité (le dernier de la défausse est pris).
- [x] Étape 6 : nombres : Surge 1 (natif).
- [ ] Étape 7 (partielle) : 1 cas (01101 à 3 PV entre en jeu, 01110 à 2 PV reste). Non couvert : défausse sans sbire, égalité. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (un sbire passe de la défausse de rencontre au jeu) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

---

## Set partagé « The Hunger Core » : traîtrises et manigances annexes (hg046-hg050)

### hg046 : Metazombie Power!

- [x] Étape 2 : références : `LeMetazombieActif` + `RevelerLeDessusDuDeckSignature` (fiche horde-metazombies, qui la cite comme carte exemple) ; Surge = `ThisCardGainSurge` (sk244).
- [x] Étape 5 : mots-pièges : « THE ACTIVE Metazombie » (le jeton tranche) ; « no Metazombies in play » testé AVANT `LeMetazombieActif` (qui retombe sur le Cœur). À CONFIRMER : le titre est lu comme ambiance ; deck signature vide = rien.
- [x] Étape 6 : nombres : Boost 2 (natif), Surge 1.
- [ ] Étape 7 (partielle) : 2 cas : Spider-Man seul (son deck signature passe de 3 à 2) ; aucun Metazombie -> Surge. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête (3 exemplaires dans le deck de rencontre). Dépend du jeton actif, qui tourne depuis le 27/10/2026 (correction 1).
- [ ] Étape 8 bis : OUI (révèle une carte d'un deck privé, qui peut s'attacher ou entrer en jeu) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg047 : Rise of the Horde!

- [x] Étape 2 : références : `NbMetazombiesEnJeu` + `MettreUnMetazombieEnJeu` (anticipés par hg015) ; Surge (hg023).
- [x] Étape 5 : mots-pièges : « fewer than 3 » relu à la résolution ; « Otherwise » exclusif. À CONFIRMER : troisième état théorique (moins de 3 en jeu mais Horde deck et défausse vides) : pas de Surge.
- [x] Étape 6 : nombres : Boost 3, plafond 3. Conformes.
- [ ] Étape 7 (partielle) : 2 cas (vrai scénario) : 2 Metazombies -> 3 ; déjà 3 -> Surge. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (« fewer than 3 ») : témoin fait (déjà 3, pas de 4e, Surge).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (Metazombie du Horde deck mis en jeu) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg048 : Half-Eaten

- [x] Étape 2 : références : hg047 (même structure) ; « with damage » = `SetHealth(max_health - degats)`, état posé et non infligé (modèles 03008 et 62014) ; arrondi par défaut (modèle 03026).
- [x] Étape 5 : mots-pièges : **CORRIGÉ le 27/10** : `DealDamage` passait par le bouclier de hg007 et par Tenace, d'où `SetHealth`. « ITS hit points » = `max_health`. **À CONFIRMER** : arrondi vers le bas (PV impairs : 9*, 11*, 13*, 15*).
- [x] Étape 6 : nombres : Boost 2, `// 2`, plafond 3.
- [ ] Étape 7 (partielle) : 2 cas (vrai scénario) : 3e Metazombie à la moitié de ses PV (`metazombie_demi_pv`) ; déjà 3 -> Surge. Le rouge d'avant le correctif est attesté par le rapport de fusion ; substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (« fewer than 3 ») : témoin fait (déjà 3 -> Surge).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (Metazombie du Horde deck mis en jeu blessé) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg049 : Hunger Pulse

- [x] Étape 2 : références : 27157 Deepest Fears (`PlaceThreatOnSchemes("MainScheme", ...)` avec un littéral "1*"/"2*") ; Boost étoile = `WhenCardBecomeBoost("This")` (an013) + `PoserInfection`.
- [x] Étape 5 : mots-pièges : « the main scheme » (pas les annexes) ; icône de boost et effet étoile sont deux choses distinctes. **À CONFIRMER** : « exposed » = aucun Metazombie en jeu (symétrique de Shielded by the Horde).
- [x] Étape 6 : nombres : Boost 1, `1*`/`2*` menace, 1 Infection.
- [ ] Étape 7 (partielle) : 3 cas : exposé (2) ; blindé (1) ; boost (1 Infection). Substitution : non tracée. Échelle par héros testée en solo seulement.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (compteur Infection par le boost) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg050 : The Hive Calls (manigance annexe)

- [x] Étape 2 : références : 01156 Usurp The Throne et 16054 Vendetta (manigances annexes officielles à `text=""` sans script).
- [x] Étape 5 : mots-pièges : aucun texte. **À CONFIRMER** (décision acceptée) : texte peut-être perdu au portage TTS (le scan est un placeholder gris). Script vide.
- [x] Étape 6 : nombres : départ `4*`, Acceleration 1, Boost 1 (tous natifs).
- [ ] Étape 7 (partielle) : 1 cas (révélée, menace de départ, aucun plantage). Substitution : sans objet (module vide).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON.
Carte terminée : NON (provisoire) : partie réelle humaine ; texte imprimé à confirmer.

---

## Trapped Survivor (hg051-hg055, manigances annexes)

Préambule commun (Étapes 2, 5 et 6, identiques pour les 5 fichiers : seule la constante `ALLIE_CARD_ID` change, `diff` vérifié).
- **Étape 2** : Hinder natif (`desc.Hinder`, fiche hinder.md, modèle 16066) ; Forced Response = `AfterResolveVillainPhaseStep(ForcedResponse, 1)` (modèle 07001b Breakout) + `PlaceCountersOn(..., 'counter')` (pu143) + `PlaceThreatOnSchemes([this], "2*")` ; seuil = `GetCounters('counter') >= 3` puis `RemoveAllFromGame([this, allié])` + `PoserInfection` sur chaque joueur ; When Defeated = `WhenSchemeBeDefeated(WhenDefeated, "This")` (ap305, 04122) + `MoveAllToProcessingArea` + `AddToHand(joueur qui a vaincu)`.
- **Étape 5** : « place 1 counter » sans `*`, « 2[per_hero] threat HERE » ; « At 3 counters » se lit sur `'counter'` (pas Infection) ; « remove THIS CARD AND <allié> » ensemble ; l'Infection n'est posée qu'au seuil ; « the player WHO DEFEATED IT » (`defeating_player`, repli sur le premier joueur, à confirmer) ; « Survivor deck » = la zone de côté (aucun Deck2), l'allié est cherché par card_id. ~~Qui met ces manigances en jeu ?~~ **RÉSOLU le 27/10/2026** : livret p. 7, étape 6, elles sont mélangées au deck de rencontre (correction 3).
- **Étape 6** : départ 4 (fixe), Hinder `2*`, 1 compteur par phase, `2*` menace, seuil 3, 1 Infection par joueur. Conformes à `cards_custom.json`.
- **Autoplay** : depuis le 27/10/2026 elles sont dans le deck de rencontre, donc révélables en autoplay (voir l'en-tête pour la fournée relancée).
- **8 bis** : toutes changent ce qu'on voit (compteur, retrait du jeu, allié de la zone de côté vers la main).

### hg051 : Trapped Survivor: Franklin Richards

- [x] Étape 2 : références : voir le préambule. Allié lié : hg072.
- [x] Étape 5 : mots-pièges : voir le préambule.
- [x] Étape 6 : nombres : voir le préambule.
- [ ] Étape 7 (partielle) : 4 cas : Forced Response (1 compteur + 2 menaces) ; 3 compteurs (manigance et Franklin retirés du jeu, 1 Infection) ; témoin du seuil (1 -> 2, reste en jeu, 0 Infection) ; When Defeated (hg072 en main). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (« At 3 counters ») : témoin fait (2 compteurs : rien ; 3 : retrait).
- [ ] Étape 8 : autoplay : révélable depuis le 27/10/2026 (deck de rencontre) ; voir l'en-tête.
- [ ] Étape 8 bis : OUI : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg052 : Trapped Survivor: Chewie

- [x] Étape 2 : références : voir le préambule. Allié lié : hg073.
- [x] Étape 5 : mots-pièges : voir le préambule.
- [x] Étape 6 : nombres : voir le préambule.
- [ ] Étape 7 (partielle) : 2 cas : When Defeated (hg073 en main) ; **27/10** 3 compteurs (2 -> 3 à l'étape 1 : la manigance ET hg073 retirés du jeu, 1 Infection), propre à CE fichier. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (« At 3 counters ») : le seuil est atteint par CE fichier (2 -> 3) ; le témoin « en dessous du seuil » est celui de hg051 (même code, `diff` vérifié).
- [ ] Étape 8 : autoplay : révélable depuis le 27/10/2026 (deck de rencontre) ; voir l'en-tête.
- [ ] Étape 8 bis : OUI : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg053 : Trapped Survivor: Valeria Richards

- [x] Étape 2 : références : voir le préambule. Allié lié : hg074.
- [x] Étape 5 : mots-pièges : voir le préambule.
- [x] Étape 6 : nombres : voir le préambule.
- [ ] Étape 7 (partielle) : 2 cas : When Defeated (hg074 en main) ; **27/10** 3 compteurs (2 -> 3 à l'étape 1 : la manigance ET hg074 retirés du jeu, 1 Infection), propre à CE fichier. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (« At 3 counters ») : le seuil est atteint par CE fichier (2 -> 3) ; le témoin « en dessous du seuil » est celui de hg051 (même code, `diff` vérifié).
- [ ] Étape 8 : autoplay : révélable depuis le 27/10/2026 (deck de rencontre) ; voir l'en-tête.
- [ ] Étape 8 bis : OUI : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg054 : Trapped Survivor: Blade

- [x] Étape 2 : références : voir le préambule. Allié lié : hg075. Retirée du jeu au Setup si un héros nommé Blade est choisi (code commun, non testé pour Blade).
- [x] Étape 5 : mots-pièges : voir le préambule.
- [x] Étape 6 : nombres : voir le préambule.
- [ ] Étape 7 (partielle) : 2 cas : When Defeated (hg075 en main) ; **27/10** 3 compteurs (2 -> 3 à l'étape 1 : la manigance ET hg075 retirés du jeu, 1 Infection), propre à CE fichier. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (« At 3 counters ») : le seuil est atteint par CE fichier (2 -> 3) ; le témoin « en dessous du seuil » est celui de hg051 (même code, `diff` vérifié).
- [ ] Étape 8 : autoplay : révélable depuis le 27/10/2026 (deck de rencontre) ; voir l'en-tête.
- [ ] Étape 8 bis : OUI : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg055 : Trapped Survivor: Wolverine

- [x] Étape 2 : références : voir le préambule. Allié lié : hg076. Retirée du jeu au Setup avec hg076 si Wolverine est choisi (cas hg004a wolverine).
- [x] Étape 5 : mots-pièges : voir le préambule.
- [x] Étape 6 : nombres : voir le préambule.
- [ ] Étape 7 (partielle) : 2 cas : When Defeated (hg076 en main) ; **27/10** 3 compteurs (2 -> 3 à l'étape 1 : la manigance ET hg076 retirés du jeu, 1 Infection), propre à CE fichier. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (« At 3 counters ») : le seuil est atteint par CE fichier (2 -> 3) ; le témoin « en dessous du seuil » est celui de hg051 (même code, `diff` vérifié).
- [ ] Étape 8 : autoplay : révélable depuis le 27/10/2026 (deck de rencontre) ; voir l'en-tête.
- [ ] Étape 8 bis : OUI : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

---

## Hungry Horde (hg056-hg058, module)

### hg056 : Hungry Zombie (sbire)

- [x] Étape 2 : références : 01101 Hydra Mercenary (Guard seul, aucun script). Trait ZOMBIE (pas METAZOMBIE).
- [x] Étape 5 : mots-pièges : aucun. À CONFIRMER (décision acceptée) : fichier présent mais vide, plutôt que pas de fichier du tout.
- [x] Étape 6 : nombres : SCH 0, ATK 1, PV 3, Guard 1, Boost 1 (natifs).
- [ ] Étape 7 (partielle) : 1 cas (Guard natif : bloque l'attaque contre Rhino). Substitution : sans objet (module vide).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON.
Carte terminée : NON (provisoire) : partie réelle humaine.

### hg057 : Bloated Zombie (sbire)

- [x] Étape 2 : références : 40168a Stryfe (`AfterUnitBeDefeated(..., "This")`) + `.NoOutOfPlayLimit()` (xenomorph_deck d'AvP) ; boucle `PoserInfection` (hg002).
- [x] Étape 5 : mots-pièges : **CORRIGÉ le 27/10** : sans `.NoOutOfPlayLimit()`, la réponse ne partait JAMAIS pour sa propre défaite (piège gs229) ; « each player » ; Forced RESPONSE (après) ; toute cause de défaite.
- [x] Étape 6 : nombres : PV 5, Guard 1, Boost 2 (natifs), 1 Infection par joueur.
- [ ] Étape 7 (partielle) : 1 cas (vaincu -> 1 Infection). Le rouge d'avant le correctif est attesté (cas `[hg] hg057` rouge, infection = 0) ; substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (compteur Infection) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg058 : Bite

- [x] Étape 2 : références : hg037 (`GetToPlayer`) ; « has damage on it » = `sustained > 0` (rl002, 32070).
- [x] Étape 5 : mots-pièges : **CORRIGÉ le 27/10** : `GetHero()` fait `assert False` en alter-ego, d'où la lecture de `GetIdentity().sustained` (les dégâts vivent sur la carte d'identité). **À CONFIRMER** : la parenthèse REMPLACE la valeur (2 au lieu de 1), elle ne s'additionne pas.
- [x] Étape 6 : nombres : Boost 2, 1 ou 2 Infection.
- [ ] Étape 7 (partielle) : 4 cas : héros indemne (1) ; blessé (2, pas 3) ; alter-ego (1, aucun plantage) ; alter-ego blessé (2). Le rouge d'avant le correctif est attesté ; substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (compteur Infection) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

---

## Fallen Heroes (hg059-hg071, module : sbires au trait METAZOMBIE)

Préambule. Ce sont des **Minion** qui portent le trait METAZOMBIE, mais `commun.Metazombies()` ne les compte pas (observation 4). Guard est natif sur les 13. Le Fallen Hero homonyme d'un héros choisi est mis de côté au Setup (`hg004a`, code commun ; seul le retrait d'un Metazombie Horde est testé). « Charge » (hg068) et « Super Speed » (hg071) sont des noms d'ambiance sans effet caché (lecture retenue).

### hg059 : Zombie Luke Cage

- [x] Étape 2 : références : 01101 (Guard), 01076 Luke Cage (Toughness) : natifs, script vide.
- [x] Étape 5 : mots-pièges : aucun texte en plus des deux mots-clés.
- [x] Étape 6 : nombres : SCH 1, ATK 2, PV 6, Guard 1, Toughness 1, Boost 2 (natifs).
- [ ] Étape 7 (partielle) : 1 cas (entre en jeu Tenace). Guard non testé sur cette carte (natif, couvert ailleurs). Substitution : sans objet.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (statut Tenace posé nativement par Toughness, rendu commun à toutes les cartes Toughness).
Carte terminée : NON (provisoire) : partie réelle humaine.

### hg060 : Zombie Hawkeye

- [x] Étape 2 : références : 01103 Shocker (When Revealed) × 24044 Boomerang (`GetToPlayer().GetControlAllies()`).
- [x] Étape 5 : mots-pièges : « each ally YOU control » = le joueur qui révèle ; dégâts directs ; liste vide sans danger.
- [x] Étape 6 : nombres : PV 5, Guard 1, Boost 1, 2 dégâts.
- [ ] Étape 7 (partielle) : 1 cas (2 dégâts à chaque allié). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg061 : Zombie Giant-Man

- [x] Étape 2 : références : hg009 (Overkill permanent par la voie dynamique `WhenUnitWouldAttackUnit` + `GainOverKill`).
- [x] Étape 5 : mots-pièges : Overkill n'est jamais une clé `desc` ; toute attaque (Identity|Ally).
- [x] Étape 6 : nombres : ATK 3, PV 8, Guard 1, Boost 3.
- [ ] Étape 7 (partielle) : 2 cas : Black Cat abattue, 1 dégât d'excès ; témoin hg060 sans Overkill. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg062 : Zombie Wasp

- [x] Étape 2 : références : 01167 Vulture (Quickstrike natif), 01040a (Retaliate natif). Script vide.
- [x] Étape 5 : mots-pièges : **CORRIGÉ le 27/10** : `"Quickstrike": "1"` ajouté au `desc` de `cards_custom.json` et contournement `ThisGainKeyword` retiré (corps du script mis à jour le 27/10/2026).
- [x] Étape 6 : nombres : ATK 1, PV 4, Guard 1, Quickstrike 1, Retaliate 2.
- [ ] Étape 7 (partielle) : 2 cas : Quickstrike (révélée, elle attaque aussitôt) ; Retaliate 2. Substitution : sans objet (module vide, la preuve porte sur la donnée).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON.
Carte terminée : NON (provisoire) : partie réelle humaine.

### hg063 : Zombie Nova Prime

- [x] Étape 2 : références : comme hg062 ; Villainous natif (11041).
- [x] Étape 5 : mots-pièges : **CORRIGÉ le 27/10** (comme hg062) ; Villainous tire un boost aussi lors de l'attaque Quickstrike.
- [x] Étape 6 : nombres : ATK 2, PV 6, Guard 1, Quickstrike 1, Villainous 1, Boost 2.
- [ ] Étape 7 (partielle) : 1 cas (Quickstrike : 2 dégâts, boost Villainous sans icône). Substitution : sans objet.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON.
Carte terminée : NON (provisoire) : partie réelle humaine.

### hg064 : Zombie Mister Fantastic

- [x] Étape 2 : références : tk026 (« fewest remaining hit points », `.health`, le joueur choisit en cas d'égalité) ; `RevelerLeDessusDuDeckSignature`.
- [x] Étape 5 : mots-pièges : PV RESTANTS ; égalité = choix du joueur qui révèle. **À CONFIRMER** : « Metazombie » = les 9 Villain seulement (pas les Fallen Heroes, qui n'ont pas de deck signature).
- [x] Étape 6 : nombres : SCH 2, PV 6, Guard 1, Boost 2.
- [ ] Étape 7 (partielle) : 1 cas (Captain Marvel la plus blessée : son deck signature est révélé). Non couvert : égalité, aucun Metazombie. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (révèle une carte d'un deck privé) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg065 : Zombie Invisible Woman

- [x] Étape 2 : références : `WhenUnitWouldTakeDamage(NonKeyword, is_from_attack=True, who_deal_damage=Ally)` + `PreventDamage("All")` (aucun texte officiel identique) ; tk022 (`GiveStatus("Confused")`).
- [x] Étape 5 : mots-pièges : « by ATTACKS from ALLIES » seulement ; « your identity AND each ally you control ».
- [x] Étape 6 : nombres : PV 4, Guard 1, Boost 2.
- [ ] Étape 7 (partielle) : 3 cas : identité + allié désorientés ; Black Cat 0 dégât ; le héros blesse normalement. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (statuts Désorienté posés par script sur plusieurs cartes) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg066 : Zombie Thing

- [x] Étape 2 : références : 62001a et 32001a (`ThisCanHaveAdditionalTough(1)`) ; up016 Herman (boucle `GiveStatus("Tough")`).
- [x] Étape 5 : mots-pièges : « tough status cards » n'est pas le mot-clé Toughness (aucun `desc.Toughness`) ; plafond permanent. À CONFIRMER : deux appels distincts (aucun modèle à « 2 » fixe).
- [x] Étape 6 : nombres : PV 7, Boost 3, 2 cartes Tenace, plafond 2 (= base 1 + 1).
- [ ] Étape 7 (partielle) : 3 cas : 2 Tenaces (`tenaces`) ; elles absorbent deux coups, le 3e passe ; **27/10** une 3e Tenace (`Puzzle.AddTough`) est refusée, il en reste 2. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (« can have 2 at the same time ») : témoin d'épuisement fait le 27/10/2026 (3e tentative refusée).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (DEUX cartes Tenace sur une même carte : affichage jamais vérifié) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg067 : Zombie Human Torch

- [x] Étape 2 : références : hg010 (`AfterUnitAttackAndDamageUnit`) ; hg012 (`GetControlAllies` + 1 dégât) ; `GetToPlayer` = le joueur attaqué (do_attack.py:391).
- [x] Étape 5 : mots-pièges : « deals damage WITH AN ATTACK » (pas de déclenchement à 0 dégât) ; « the attacked player » même si un allié a défendu.
- [x] Étape 6 : nombres : PV 5, Guard 1, Villainous 1, Boost 2, 1 dégât.
- [ ] Étape 7 (partielle) : 2 cas : blesse -> 1 dégât à chaque allié ; témoin avec attaque absorbée par Tenace (rien). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg068 : Zombie Rhino

- [x] Étape 2 : références : 04027 Crossfire (`UnitAttackGainKeyword("This", piercing=True)`).
- [x] Étape 5 : mots-pièges : Piercing n'est pas une clé `desc`. **À CONFIRMER** : « Charge. » = nom d'ambiance, sans effet caché (la traîtrise officielle 01099 Charge n'a rien à voir).
- [x] Étape 6 : nombres : ATK 3, PV 7, Guard 1, Boost 3.
- [ ] Étape 7 (partielle) : 1 cas (Piercing : Tenace défaussée, 3 dégâts). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

### hg069 : Zombie Colossus

- [x] Étape 2 : références : cd017 Inner Demon (« Guard. Toughness. », aucun script officiel).
- [x] Étape 5 : mots-pièges : aucun.
- [x] Étape 6 : nombres : ATK 3, PV 7, Guard 1, Toughness 1, Boost 3.
- [ ] Étape 7 (partielle) : 1 cas (entre en jeu Tenace). Substitution : sans objet.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (Tenace native, comme hg059).
Carte terminée : NON (provisoire) : partie réelle humaine.

### hg070 : Zombie Falcon

- [x] Étape 2 : références : 49039 Selene et gs132 (`UnitCannotAttackTarget(Ally, cannot_attack="This")`) ; 01191 Exhaustion (`ExhaustAll`) ; `GiveStatus("Stunned")`.
- [x] Étape 5 : mots-pièges : « by ALLIES » ; « it is stunned » = la même identité ; les deux effets s'appliquent dans l'ordre. À CONFIRMER : « ; » lu comme une suite obligatoire.
- [x] Étape 6 : nombres : ATK 1, PV 4, Guard 1, Villainous 1, Boost 1.
- [ ] Étape 7 (partielle) : 2 cas : identité inclinée ET étourdie ; Black Cat ne la blesse pas. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [ ] Étape 8 bis : OUI (statut Étourdi + inclinaison posés par script) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 bis absente.

### hg071 : Zombie Quicksilver

- [x] Étape 2 : références : sk249 Cloning Program (`AfterEnemyActivationEnd` + `DoActivate`, garde anti-boucle) ; 41028 Psionic Illusion (`ChangeTarget`) + 45065 (`AskChooseFace` par le joueur attaqué).
- [x] Étape 5 : mots-pièges : « activates twice » = +1 activation, jamais une boucle ; « that player's choice » = le joueur ATTAQUÉ ; « while ... controls an ally » relu à chaque attaque. **À CONFIRMER** : « Super Speed » = ambiance ; les deux clauses sont indépendantes.
- [x] Étape 6 : nombres : ATK 2, PV 3, Guard 1, « twice » = 1 activation de plus.
- [ ] Étape 7 (partielle) : 2 cas : deux activations sans allié (2 + 2 = 4) ; avec un allié (4 dégâts sur Hulk, 0 sur l'identité). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? OUI (« twice », une borne sur le nombre d'activations) : témoin fait (exactement 4 dégâts, pas 6 ni une boucle).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (redirection de cible, elle chiffre seulement).
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée.

---

## Survivor deck (hg072-hg076, alliés)

Préambule. Les cinq alliés sont **mis de côté** au Setup et n'arrivent en main que par le When Defeated de leur Trapped Survivor (hg051-hg055), qui est dans le deck de rencontre depuis le 27/10/2026 (correction 3). Ils sont **retirés du jeu** si un héros homonyme est choisi (hg004a). Le « * » de leurs ATK et THW est l'étoile de **dégâts conséquents** (parseurs `can_attack.py` et `can_thwart.py`), pas « par héros ». Leur statut 8 bis vient de ce passage zone de côté -> main (ou retrait du jeu), quel que soit leur texte. L'autoplay ne les voit que si le pilote vainc une manigance Trapped Survivor.

### hg072 : Franklin Richards

- [x] Étape 2 : références : 09002 Wong (`WhenInYourPlayTurn(Action).SetCostFunc(CostFunc.Exhaust("This"))` + `ChooseAbilities`) ; `RemoveCountersOn(..., 'infection')` sur l'IDENTITÉ du héros ciblé (symétrique de `PoserInfection`) ; lj024 (`HealthUnits`), cible `Friend`.
- [x] Étape 5 : mots-pièges : « choose one » ; « from A HERO » (n'importe quel héros, compteur retiré de son identité) ; « a FRIENDLY CHARACTER » = `Friend` (héros OU allié).
- [x] Étape 6 : nombres : coût 0, THW `1*` (1 dégât conséquent), PV 2, wild ; 2 Infection, 2 soins.
- [ ] Étape 7 (partielle) : 2 cas : option 1 (3 -> 1 Infection) ; option 2 (héros blessé de 3 -> 1). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay : **jamais en jeu**.
- [ ] Étape 8 bis : OUI (retire des compteurs Infection ; passe de la zone de côté à la main) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 et 8 bis absentes.

### hg073 : Chewie

- [x] Étape 2 : références : 61009 4K Digital Camcorder (`SetTarget(Minion)` + `DiscardAll`) ; lj024 (dégâts à soi) ; `CardFinder(traits=[...])` en OU.
- [x] Étape 5 : mots-pièges : **DÉCISION du 27/10** : lecture STRICTE `card_type=Minion` (les Fallen Heroes sont des Minion METAZOMBIE ; la lecture large aurait défaussé gratuitement un Metazombie VILAIN de 9 à 15 PV). « Chewie takes 1 damage » est dans l'EFFET, pas dans le coût.
- [x] Étape 6 : nombres : coût 0, ATK `1*`, PV 2, wild, 1 dégât à soi.
- [ ] Étape 7 (partielle) : 3 cas : sbire ZOMBIE hg056 défaussé ; sbire METAZOMBIE hg059 défaussé ; contre-cas vilain hg013 non ciblable. Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay : **jamais en jeu**.
- [ ] Étape 8 bis : OUI (zone de côté -> main ; un sbire passe du jeu à la défausse) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 et 8 bis absentes.

### hg074 : Valeria Richards

- [x] Étape 2 : références : hg072 (charpente) ; nt012 (branches sans cible) ; 40002 Bodyslide (`ChangeToOtherIdentityForm`) ; `LeCoeur` + `DealDamage`.
- [x] Étape 5 : mots-pièges : « Change form » = l'identité du joueur, pas Valeria ; « The Hunger Core » = cible fixe. **À CONFIRMER** : « 3* » en prose = par héros (`3 * NombreDeJoueurs`), différent du THW `3*` (étoile conséquente).
- [x] Étape 6 : nombres : coût 0, THW `3*`, PV 2, wild ; 3* dégâts.
- [ ] Étape 7 (partielle) : 3 cas : changement de forme ; 3 dégâts au Cœur exposé ; 0 contre un Cœur blindé. Substitution : non tracée. Échelle par héros testée en solo seulement.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay : **jamais en jeu**.
- [ ] Étape 8 bis : OUI (zone de côté -> main) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 et 8 bis absentes.

### hg075 : Blade

- [x] Étape 2 : références : 42025 Harpoon (`UnitGetATKWhileAttacking`) ; 32091 Cannonball (`AfterUnitAttackAndDefeatUnit`) + `DoesNotTakeConsequentialDamage` (58020, 17020).
- [x] Étape 5 : mots-pièges : « ENEMY » (Minion ET Villain, sans ambiguïté, contrairement à Chewie) ; « WHILE attacks » ; « IF HE DEFEATS IT » ; négation totale. « Undead Hunter » = ambiance.
- [x] Étape 6 : nombres : coût 0, THW `1*`, ATK `2*`, PV 3, wild ; +2 ATK.
- [ ] Étape 7 (partielle) : 2 cas : contre hg056 (2 + 2 = 4, vaincu, aucun dégât conséquent) ; témoin contre un sbire ordinaire (2 dégâts, 1 dégât conséquent). Non couvert : une attaque à +2 qui ne vainc pas (le dégât conséquent doit tomber). Substitution : non tracée.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay : **jamais en jeu**.
- [ ] Étape 8 bis : OUI (zone de côté -> main) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; substitution non tracée ; Étape 8 et 8 bis absentes.

### hg076 : Wolverine

- [x] Étape 2 : références : alliés officiels sans texte (01013, 03010). Script vide.
- [x] Étape 5 : mots-pièges : aucun texte ; ne pas inventer de capacité fantôme.
- [x] Étape 6 : nombres : coût 0, THW `1*`, ATK `3*`, PV 3, wild (natifs).
- [ ] Étape 7 (partielle) : 1 cas (posé en jeu, aucun plantage). Substitution : sans objet.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay : **jamais en jeu**.
- [ ] Étape 8 bis : OUI (zone de côté -> main, ou retiré du jeu au Setup avec hg055 : cas hg004a wolverine) : cas plateau **absent**.
Carte terminée : NON (provisoire) : partie réelle humaine ; Étape 8 et 8 bis absentes.

---

## Points « À CONFIRMER » conservés (lecture retenue codée, aucun blocage)

Repris des en-têtes de scripts, sans arbitrage nouveau dans ce document :
- hg017, hg044 : ordre de résolution des activations multiples.
- hg019, hg020, hg021, hg043 : « Spend N resources » nu = « of any type ».
- hg022 : ForcedResponse plutôt que ForcedInterrupt pour les dégâts aux alliés.
- hg024, hg032, hg033, hg039 : Metazombie nommé absent, aucun effet.
- hg028 : départage de « most cards in hand ».
- hg034 : Storm +1 en seconde réponse.
- hg036 : « 4* » en texte libre = par joueur.
- hg045 : égalité de PV imprimés.
- hg046 : le titre est d'ambiance.
- hg047, hg048 : troisième état (Horde deck et défausse vides).
- hg048 : arrondi vers le bas.
- hg049 : « exposed » = aucun Metazombie en jeu.
- hg050 : texte peut-être perdu.
- hg051-hg055 : `defeating_player` absent. (Entrée en jeu : résolue le 27/10/2026, deck de rencontre.)
- Horde deck : le `Deck2` remélange sa défausse DÈS qu'il se vide (`BindDiscardPile`), pas au moment où un Metazombie doit entrer (« If the Horde deck is empty, shuffle its discard pile », p. 3) : un Metazombie vaincu entre ces deux instants reste dans la défausse au lieu d'être remélangé. Écart mesuré le 27/10/2026 (cas « REVIENNENT »), jugé mineur, non corrigé.
- hg056 : fichier vide plutôt qu'absent.
- hg058 : la parenthèse REMPLACE la valeur.
- hg064 : portée de « Metazombie ».
- hg066 : deux `GiveStatus`.
- hg068, hg071 : « Charge » et « Super Speed » sont des noms d'ambiance.
- hg070 : « ; » lu comme une suite.
- hg074 : « 3* » = par héros.

## À vérifier en partie réelle (aucun outil du projet ne le voit)

- Une partie complète, avec un héros qui n'élimine PAS Zombie Spider-Man (pour voir hg010 et hg027-hg029), en standard ET en expert (hg003).
- La rotation du jeton actif à l'écran (le compteur `active` change de carte à chaque fin de phase méchant ; codée et testée le 27/10/2026, jamais regardée sur le plateau).
- Les compteurs Infection à l'écran (nouveau compteur, désormais posés à chaque morsure). **Leur conséquence de règle (limite 7/6 -> héros vaincu, version zombie en jeu ; récupération « soigner OU retirer 3 ») n'est PAS codée** : point ouvert prioritaire, livret p. 5.
- Une révélation de Trapped Survivor en vraie partie (deck de rencontre depuis le 27/10/2026), puis sa défaite (allié en main).
- Le dessin des améliorations posées sur un Metazombie (hg008, hg018-hg022, hg026, hg031, hg034, hg040, hg043), des deux Tenaces de hg066 et des decks signature (zones privées attachées à la carte du Metazombie) : aucun cas plateau.
