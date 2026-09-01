# PROCESSUS-CARTE.md — les 25 gabarits du pack BEAST (set 134, `bt`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli, preuve à l'appui, pour
**chaque** carte du pack. Rédigés le 01/09/2026, après la batterie complète.

**Preuves communes à toutes les cartes**, citées une fois ici plutôt que
répétées 25 fois :

- **Étape 7, substitution** : `tools/substituer_pack.py .game-src 34000 bt0` →
  **23/23 cartes**, aucun cas resté vert sans son module.
- **Étape 8, autoplay** : `tools/autoplay.py --deck beast --vilains rhino
  --parties 8`, témoin `agatha_harkness` dans la même fournée. **Grep exhaustif
  des 8 journaux : 0 `NameError`/`AttributeError`/`TypeError`/`KeyError`/
  `AssertionError`/`Traceback`.** Beast tient 6,1 rounds contre 5,0 au témoin,
  0 victoire de part et d'autre (comportement connu de ce pilote contre Rhino).
- **Batterie complète** : 884/889, les 5 rouges préexistants, 0 régression.
- **Étape 4, image** : `assets/pics/<card_id>.png` déposée pour les 25.
- **Étape 1** : entrée dans `data/cards.json`, pack `beast` en queue de
  fichier, `custom: "Arnaud"`, checksums recalculés.

Le nombre d'occurrences en autoplay est donné par carte : il dit si la carte a
été **vue en jeu réel**, pas seulement en test unitaire.

---

### bt001a : * Beast (Hero)

- [x] Étape 2 : référence : `AfterUnitDefendAgainstAttack(..., take_no_damage=True)`
      (do_attack.py:288 — le drapeau existait, aucune carte officielle ne
      l'employait) ; fouille deck+défausse : `04001b` * Clint Barton.
- [x] Étape 5 : mots-pièges : **`any card`** (aucun filtre passé à
      `Search.PlayerCard`, un `card_type` par réflexe aurait restreint la
      carte) ; **`when defending`** (`who_defense="You"` : encaisser 0 hors
      défense ne déclenche rien) ; `your deck or discard pile` (les deux zones).
      Résultat : conforme.
- [x] Étape 6 : THW 1 / ATK 2 / DEF 3 / MNG 5 / 13 PV, 0 dégât. Identiques
      scan ↔ `desc` ↔ script. Résultat : conforme.
- [x] Étape 7 : 1 capacité, 1 cas — « bt001a Thick Skinned », rouge sans
      module / vert avec (subst. 1/1). Résultat : vert.
- [x] Étape 8 : **1175 occurrences**, et le journal donne `"Thick_Skinned": 2`
      sur 11 rounds, `"Thick_Skinned": 4` sur 4 autres. La capacité vedette
      part vraiment, plusieurs fois par round.

**Carte terminée : OUI**

---

### bt001b : * Dr Hank McCoy (AlterEgo)

- [x] Étape 2 : pool hors-deck : `36001b` * Ororo Munroe
      (`BeginGameWithSetAside`) ; changement de forme : `01019a` * She-Hulk
      (`AfterUnitChangeForm(to_this_form=True)`) ; tirage :
      `Rand.RandomChoice` ; mélange : `Faces.ShuffleAllTo`.
- [x] Étape 5 : mots-pièges : **`1 random`** (c'est le hasard qui choisit, pas
      le joueur — passer par `AskChooseFace` comme Ororo trahirait la carte) ;
      **`into your deck`** (pas la main) ; `all cards you mulligan` (on
      remélange `message.discarded_faces`, PAS la pile de défausse, qu'un autre
      effet de mise en place pourrait avoir garnie). Résultat : conforme.
- [x] Étape 6 : REC 4 / MNG 6 / 13 PV ; 1 carte Discovery ; pool de 5.
      Résultat : conforme.
- [x] Étape 7 : **3 capacités, 3 couvertes** — « bt001b Scientific Discovery »,
      « bt001b pool Discovery » et « **bt001b Setup — les cartes écartées au
      mulligan reviennent dans le deck** ». Subst. **3/3**, toutes rouges sans
      module ; celle du mulligan tombe sur
      `defausse du joueur = 6 carte(s) (attendu 0)`.
- [x] Étape 8 : **167 occurrences**, 15 `Change_Form` relevés dans les
      journaux.

**Carte terminée : OUI**

> **Comment le trou a été fermé (01/09/2026).** La capacité `Setup` était
> intestable : le pilote du harnais répondait toujours « je ne défausse rien »
> au mulligan, `premiere_option_jouable` fournissant le nombre MINIMAL de
> cibles, soit zéro. L'option porte le nom exact « Resolve Mulligans »
> (identifié par `TRACE_OPTIONS`). Une clé **`mulligan: "all" | [card_id, …]`**
> a été ajoutée au pilote : `"all"` écarte toute la main, seul réglage
> déterministe puisque la main de départ dépend du mélange. La clé est
> **additive** — sans elle, `option_mulligan()` rend `None` et la boucle
> historique reprend la main — donc aucun cas existant ne change.
> Le cas vérifie `defausse_joueur: 0` **et** `taille_main: 6` : le second
> prouve que la repioche a lieu AVANT le remélange, sans quoi le joueur
> pourrait retomber sur ce qu'il vient d'écarter.

---

### bt002 : * Wonder Man (Ally)

- [x] Étape 2 : `44013` Dogpool, « When Defeated: Deal 1 damage to an enemy » —
      même `WhenUnitBeDefeated(WhenDefeated, "This").SetTarget(Enemy)`.
- [x] Étape 5 : mot-piège : **`When Defeated`** = l'allié TOMBE, à ne pas
      confondre avec `AfterUnitDefeatedUnit` (l'allié a vaincu quelqu'un).
      Résultat : conforme.
- [x] Étape 6 : coût 3 / 4 PV / ATK 1* / THW 1* / 2 dégâts. Résultat : conforme.
- [x] Étape 7 : 1 capacité, 1 cas — « bt002 Wonder Man », subst. 1/1.
- [x] Étape 8 : **304 occurrences**.

**Carte terminée : OUI**

---

### bt003 : * Phoenix (Ally)

- [x] Étape 2 : bt002 du même pack (texte identique au mot près), et par lui
      `44013` Dogpool.
- [x] Étape 5 : identique à bt002 ; seuls les traits changent
      (PSIONIC. X-MEN au lieu d'AVENGER). Résultat : conforme.
- [x] Étape 6 : coût 3 / 4 PV / ATK 1* / THW 1* / 2 dégâts. Résultat : conforme.
- [x] Étape 7 : 1 capacité, 1 cas — « bt003 Phoenix », subst. 1/1.
- [x] Étape 8 : **0 occurrence, et c'est attendu** : Phoenix n'est pas dans
      `deck/starter/beast.json` (qui monte Wonder Man) mais dans la variante
      `deck/custom/beast_phoenix.json`, que l'autoplay ne joue pas. Le cas de
      test la couvre, et son module est le même que bt002, vu 304 fois.

**Carte terminée : OUI**

---

### bt004 : Experimental Warfare (Event)

- [x] Étape 2 : `03033` Expert Defense (« Hero Interrupt (defense) … +3 DEF for
      that attack ») ; effet différé : `RunAt.AfterEnemyActivationEnd` ;
      lecture « 0 dégât » : bt001a du même pack.
- [x] Étape 5 : mots-pièges : **`all upgrade cards in play`** (portée non
      qualifiée → **arbitrage utilisateur : les tiennes seulement**) ;
      **`for each exhausted upgrade`** (on compte la liste RENDUE par
      `Faces.ExhaustAll`, pas celle qu'on lui passe) ; **`the attacking
      character`** (`message.attacker`, pas un ennemi au choix) ;
      **`dealt "0" damage`** (0 encaissé, pas « attaque annulée »).
      Résultat : conforme.
- [x] Étape 6 : coût 1 ; +1 DEF par amélioration ; 3 dégâts. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt004 Experimental Warfare », subst. 1/1. **Le cas a
      trouvé deux vrais bugs** : `CanBeExhaust` inexistant (`AttributeError` en
      pleine défense) puis une capacité `RegisterTemp`/`Temp0` qui ne se
      déclenchait jamais.
- [x] Étape 8 : **28 occurrences**.

**Carte terminée : OUI**

---

### bt005 : Fighting With Friends (Event, ×2)

- [x] Étape 2 : `01013` Photonic Blast (`GetPaidResources().HasColor`) ;
      `01069` Get Ready (redresser un allié) ; an001a Frenzy (redresser
      l'identité).
- [x] Étape 5 : mots-pièges : **`a [mental] resource`** → `HasColor`, PAS
      `OnlyHasColor` (le texte ne dit pas « only », contrairement à 20003) ;
      **`Hero Response` sans déclencheur** → arbitrage utilisateur : codée en
      Hero Action, seule lecture qui rende la carte jouable.
      Résultat : conforme.
- [x] Étape 6 : coût 1 ; 1 héros + 1 allié. Résultat : conforme.
- [x] Étape 7 : 2 capacités (redressement, branche mentale), **2 cas** — le
      nominal et le contre-cas « sans mental, seul le héros se redresse ».
      Subst. **2/2**, les deux rouges sans module.
- [x] Étape 8 : **50 occurrences**.

**Carte terminée : OUI**

---

### bt006 : In The Heat Of Battle (Event)

- [x] Étape 2 : `04049` Clear the Area (« Remove 2 threat… If this removes the
      last threat on that scheme ») ; pool Discovery : bt001b du même pack.
- [x] Étape 5 : mots-pièges : **`shuffle … into your hand`** (contradiction →
      arbitrage utilisateur : le verbe l'emporte, la carte part dans le DECK) ;
      **`removed all threat`** (testé sur la manigance CIBLÉE, `effect.targets`,
      pas une quelconque) ; **`Action` et non `Hero Action`** (jouable dans les
      deux formes). Résultat : conforme.
- [x] Étape 6 : coût 2 ; 4 menaces ; 1 carte Discovery. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt006 In The Heat Of Battle », subst. 1/1. Le cas
      couvre **les deux moitiés** : `01107` (2 menaces) est vidée par les 4 de
      l'événement, ce qui déclenche le bonus Discovery.
- [x] Étape 8 : **28 occurrences**.

**Carte terminée : OUI**

---

### bt007a : Multi-Tasking ([mental])

- [x] Étape 2 : `01022` Ground Stomp (dégâts à tous les ennemis) ; littéral
      `"EachScheme"` de `RemoveThreatFromSchemes` ; compteur
      `stat.this_turn_played_cards` (player_stat.py:7).
- [x] Étape 5 : mots-pièges : **`all enemy characters`** et **`all schemes`**
      (deux effets de zone : `SetTarget` ne portant qu'un type, on passe par
      `Worlds.FindCardsOnField` + le littéral) ; **`repeat this hero action`**
      (boucle infinie si relu naïvement → arbitrage utilisateur : **une seule**
      répétition) ; **`first card you played this turn`** (on compte les AUTRES
      cartes, `is not this`, ce qui reste juste que la carte soit déjà
      enregistrée ou non). Résultat : conforme.
- [x] Étape 6 : coût 1 ; 1 dégât ; 1 menace ; 1 répétition. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt007a Multi-Tasking », qui vérifie **2 dégâts** au
      vilain (donc la double résolution), subst. 1/1.
- [x] Étape 8 : **37 occurrences**.

**Carte terminée : OUI**

---

### bt007b : Multi-Tasking ([physical])

- [x] Étape 2 : copie stricte de bt007a. Deux card_id pour une même carte aux
      ressources différentes : précédent `01043a/b/c/d` Wakanda Forever!.
- [x] Étape 5 : **icône de ressource lue au coin, pas au nom du fichier**
      (leçon Lockjaw) : 6/15 est mentale, 7/15 physique. C'est ce contrôle qui
      a évité de les traiter comme deux copies. Résultat : conforme.
- [x] Étape 6 : identiques à bt007a, `RES` seule diffère. Résultat : conforme.
- [x] Étape 7 : 1 cas dédié — « bt007b Multi-Tasking », qui prouve que le
      second card_id est bien câblé. Subst. 1/1.
- [x] Étape 8 : **69 occurrences**.

**Carte terminée : OUI**

---

### bt008 : Primal Rage (Event, ×2)

- [x] Étape 2 : `19005` Knife Leap (« Hero Interrupt: When you make a basic
      attack, you get +5 ATK ») ; coût de défausse : `45014` Advanced Suit.
- [x] Étape 5 : mots-pièges : **`discard a card` avant la flèche** = le COÛT,
      pas l'effet (le coder en effet donnerait les +5 gratis) ; **`basic
      attack`** → `is_basic_attack=True`, distinction imprimée par 01024.
      Résultat : conforme.
- [x] Étape 6 : coût 0 ; +5 ATK ; 1 carte défaussée. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt008 Primal Rage » (ATK 2+5 = 7 dégâts minimum),
      subst. 1/1.
- [x] Étape 8 : **42 occurrences**.

**Carte terminée : OUI**

---

### bt009 : Alien Materials (Resource, ×2)

- [x] Étape 2 : **aucune capacité, donc aucun script.** Ressource double :
      `01088` Energy (`YY`), `01044` Vibranium (`GG`).
- [x] Étape 5 : la carte n'a **aucun texte de règles** (seulement une citation).
      Le seul point à vérifier était l'icône : **deux ressources**, énergie +
      mental, lues au coin par comparaison (leçon Lockjaw) → `RES: "YB"`.
      Résultat : conforme.
- [x] Étape 6 : aucun nombre imprimé hors le `2/15`. Résultat : conforme.
- [x] Étape 7 : **aucun cas requis** — l'étape 7 demande un cas par capacité, et
      cette carte n'en a aucune. Elle n'apparaît donc pas au bilan de
      substitution (23 cartes scriptées sur 25 entrées).
- [x] Étape 8 : **32 occurrences** en autoplay, donc réellement piochée et
      dépensée en partie.

**Carte terminée : OUI**

---

### bt010 : Beast's Lab (Support)

- [x] Étape 2 : `01034` * Stark Tower (inclinaison + choix d'un joueur par
      `SetTarget` rendant des identités + `Players.ForEachTargets`) ; fouille :
      `04001b`, `04141`.
- [x] Étape 5 : mots-pièges : **`that player searches their deck`** (c'est le
      joueur CHOISI qui fouille SES zones — passer `initiator` viserait le
      mauvais deck en multi) ; **`an upgrade`** sans trait (contrairement à
      Stark Tower qui exige TECH) ; le « (Shuffle.) » est implicite.
      Résultat : conforme.
- [x] Étape 6 : coût 4 ; 1 amélioration. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt010 Beast's Lab », subst. 1/1.
- [x] Étape 8 : **24 occurrences**.

**Carte terminée : OUI**

---

### bt011 : Hank's Kimono (Support)

- [x] Étape 2 : `04001b` * Clint Barton (fouille de la défausse) ; `aa003`
      * Ebony (Alter-Ego Action + `CostFunc.Exhaust("This")`) ;
      `Faces.MoveAllToDeck(..., "Top", ...)`.
- [x] Étape 5 : mots-pièges : **`a resource card`** = le TYPE de carte
      Resource, pas « une carte portant une icône » (sinon la phrase n'aurait
      aucun sens) ; **`on the top of your deck`** (pas dans la main) ; pas de
      « shuffle », donc pas de mélange. Résultat : conforme.
- [x] Étape 6 : coût 1 ; 1 carte. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt011 Hank's Kimono », subst. 1/1. ⚠ **Ce cas était
      un FAUX VERT** : le module plantait à chaque usage
      (`include_player_deck` manquant, argument sans valeur par défaut) et la
      ressource remontait quand même dans le deck par le remélange de la
      défausse. Durci depuis avec `defausse_joueur: 0`.
- [x] Étape 8 : **66 occurrences**. **C'est l'autoplay qui a trouvé le bug**,
      dans 4 parties sur 8 ; après correction, grep à 0.

**Carte terminée : OUI**

---

### bt012 : Civilian Disguise (Support)

- [x] Étape 2 : `01008` Web-Shooter (`desc.Uses` au format `"3,disguise"`) ;
      `23016` Command Team (compteur dépensé en coût) ;
      `AfterUnitDefendAgainstAttack` sans `take_no_damage`.
- [x] Étape 5 : mots-pièges : **`remove 1 counter` avant la flèche** = le COÛT ;
      **`After defending`** (il faut avoir été le défenseur déclaré) ; le texte
      ne dit pas ce qui arrive à 0 compteur → **arbitrage utilisateur : elle se
      défausse**, via `Uses`. Résultat : conforme.
- [x] Étape 6 : coût 1 ; **3** compteurs ; 1 carte piochée. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt012 Civilian Disguise » (compteurs 3 → 2),
      subst. 1/1.
- [x] Étape 8 : **73 occurrences**.

**Carte terminée : OUI**

---

### bt013 : Hunter Gear (Upgrade)

- [x] Étape 2 : `an008`/`ho011` (`GiveKeywordToAttached("You", defense=1)`) ;
      `ab007` (génération de ressource) ; `mf009` (condition sur la main).
- [x] Étape 5 : mots-pièges : **`cards marked with a [physical] resource`** →
      `HasColorPrinted`, PAS `HasColor`, qui convertirait le [wild] et
      bloquerait la carte à tort ; **`Action` qui génère une ressource** → le
      moteur n'accepte que Resource/HeroResource/AlterEgoResource, codée en
      Resource (signalé à l'auteur). Résultat : conforme.
- [x] Étape 6 : coût 2 ; +1 DEF ; 1 ressource. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt013 Hunter Gear » (DEF 3 → 4), subst. 1/1.
- [x] Étape 8 : **27 occurrences**.

**Carte terminée : OUI**

---

### bt014 : * Peter Parker (Ally, Discovery)

- [x] Étape 2 : `ab007` * Donald Pierce — même
      `CanGenerateResources(Resource, Resources("G")) +
      CostFunc.Exhaust("This")`.
- [x] Étape 5 : mots-pièges : **`Action`** → Resource (contrainte moteur,
      signalée à l'auteur) ; **une seule `CanGenerateResources` par carte**
      (assert) ; **ATK 0 sans étoile, THW 2 AVEC étoile**, lu au coin.
      Résultat : conforme.
- [x] Étape 6 : coût 2 / 3 PV / THW 2* / ATK 0. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt014 Peter Parker », subst. 1/1. ⚠ Le premier
      montage du cas échouait parce que **bt005 redressait l'allié qui venait
      de payer** (chaîne aval) : la carte payée est désormais `22034`.
- [x] Étape 8 : **1 occurrence** — faible mais réelle : carte hors-deck, elle
      doit d'abord rejoindre le deck puis être piochée.

**Carte terminée : OUI**

---

### bt015 : Space Hand Grenade (Upgrade, Discovery)

- [x] Étape 2 : `01185` Biomechanical Upgrades (amélioration attachée à un
      sbire + `ForcedInterrupt` sur `"AttachedMinion"`) ; `20003`
      (`CancelThisAttack`).
- [x] Étape 5 : mots-pièges : **`that minion`** = le porteur, pas un sbire au
      choix ; **`attach to minion`** sans contrainte (contrairement à 01185 qui
      impose les plus gros PV). Résultat : conforme.
- [x] Étape 6 : coût 1 ; 4 dégâts. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt015 Space Hand Grenade », subst. 1/1. Le cas prouve
      l'annulation (0 dégât encaissé) **et** la mort du sbire.
- [x] Étape 8 : **7 occurrences**.

**Carte terminée : OUI**

---

### bt016 : Ambush (Event, Discovery)

- [x] Étape 2 : `20003` Grasping Tendrils
      (`WhenUnitInitiatesAttackAgainst` + `CancelThisAttack`).
- [x] Étape 5 : mots-pièges : **`Forced Interrupt`** sur un événement de main
      (inhabituel → arbitrage utilisateur : **on suit le mot imprimé**) ;
      **`an support card in play`** (portée non qualifiée → les tiens) ;
      **`exhaust` avant la flèche** = le COÛT. Résultat : conforme.
- [x] Étape 6 : coût 0 ; 1 soutien incliné. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt016 Ambush », subst. 1/1. ⚠ A imposé d'ajouter
      `ForcedInterrupt` à `check_sub_type` (ability.py) : sans quoi **le deck
      ne montait pas du tout**.
- [x] Étape 8 : **1 occurrence** (carte hors-deck, comme bt014).

**Carte terminée : OUI**

---

### bt017 : Automated Life-Support (Upgrade, Discovery)

- [x] Étape 2 : `01185` (même charpente : `WhenUnitWouldBeDefeated` +
      `SetBeInstead` + soin) ; `05015`/`01083` pour `GiveStatus("Tough")`.
- [x] Étape 5 : mots-pièges : **`would be defeated`** → `SetBeInstead`
      indispensable, sans quoi l'allié meurt malgré le soin ; **`Max 1 per
      ally`** = base automatique `desc.MaxPerUnit`, aucun module.
      Résultat : conforme.
- [x] Étape 6 : coût 2 ; 1 soin ; 1 statut. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt017 Automated Life-Support » (l'allié survit et
      porte Tough), subst. 1/1.
- [x] Étape 8 : **5 occurrences**.

**Carte terminée : OUI**

---

### bt018 : Mecha-Beast (Upgrade, Discovery)

- [x] Étape 2 : `an008`/`ho011` —
      `GiveKeywordToAttached("You", thwart=1, health=2)`.
- [x] Étape 5 : mots-pièges : **`+2 hitpoints`** = le MAXIMUM de PV monte, ce
      n'est pas un soin ; **`+1 THW`** est bien le CTR, pas le SCH (le héros
      n'a pas de SCH). Résultat : conforme.
- [x] Étape 6 : coût 3 ; +1 THW ; +2 PV. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt018 Mecha-Beast » (CTR 1→2, PV 13→15), subst. 1/1.
- [x] Étape 8 : **0 occurrence, et c'est explicable** : carte Discovery à
      coût 3, elle doit rejoindre le deck par un passage en alter-ego, puis
      être piochée et payée — improbable en 6 rounds. **C'est la seule carte du
      pack jamais vue en autoplay.** Sa preuve reste son cas de test, rouge
      sous substitution.

**Carte terminée : OUI**

---

### bt019 : Unfinished Projects (Obligation)

- [x] Étape 2 : `aa014` Chaotic Forces — même structure exacte
      (`WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` +
      `ChooseAbilities` à deux puces, la 1re retirant de la partie, la 2nde
      défaussant).
- [x] Étape 5 : mots-pièges : **`Mutation Degeneration`** (carte inexistante →
      arbitrage utilisateur : l'obligation elle-même) ; **`remove from the
      game` vs `discard`** (asymétrie voulue des deux puces) ; **`upgrade/
      support cards in play`** (les deux types, et seulement ce que tu
      contrôles). Résultat : conforme.
- [x] Étape 6 : Boost 2 ; 2 cartes ; 2 dégâts. Résultat : conforme.
- [x] Étape 7 : 2 puces, **2 cas** (branche à 2 cartes, et contre-cas sans
      carte à payer). Subst. **2/2**. ⚠ Ces cas ont révélé que **le module
      n'était jamais chargé** : `set_name: "Beast"` mais fichier rangé dans
      `beast_nemesis/`. L'obligation entrait en jeu et ne faisait rien, en
      silence.
- [x] Étape 8 : **55 occurrences**, et le journal montre la branche
      `Discard_2_upgrade/support_cards_in_play_→_remove_this_obligation_from_the_game`
      réellement jouée.

**Carte terminée : OUI**

---

### bt020 : Lizard-Fied Mutants (Minion nemesis, ×2)

- [x] Étape 2 : **aucun script.** `Guard`, `Patrol`, `Boost` et `Nemesis` sont
      des bases automatiques lues dans `desc` (fiches
      `docs/reference/mots-cles/guard.md` et `patrol.md`, toutes deux
      explicites : « aucun script requis »).
- [x] Étape 5 : mots-pièges : `Guard. Patrol.` — vérifié qu'aucune capacité
      fantôme n'est codée pour eux ; trait **LIZARD** ajouté à l'énum `TRAITS`.
      Résultat : conforme.
- [x] Étape 6 : 4 PV / SCH 1 / ATK 2 / Boost 2 ; `Guard: 1`, `Patrol: 1`.
      Résultat : conforme.
- [x] Étape 7 : **aucun cas requis** — la carte n'a aucune capacité scriptée.
      Ses mots-clés sont couverts par le moteur lui-même.
- [x] Étape 8 : **198 occurrences**, donc bien mis en jeu et engagé.

**Carte terminée : OUI**

---

### bt021 : Dark Transformation (Treachery nemesis)

- [x] Étape 2 : `an011` Hel's Retribution (`WhenThisRevealed` +
      `message.GetToPlayer()`) ; `42025` (`DiscardDeckTopCards`) ; `50062`
      (dégâts à l'identité) ; `11020` Depowered (« hero-specific »).
- [x] Étape 5 : mots-pièges : **`for every hero-specific card`** (1 dégât PAR
      carte, pas 1 si au moins une) ; **`from your deck`** (le joueur, pas le
      deck rencontre) ; **`hero-specific`** = classe `IdentitySpecific`, PAS
      `desc.Class == "Hero"`. Résultat : conforme.
- [x] Étape 6 : Boost 1 ; **5** cartes ; 1 dégât par carte. Résultat : conforme.
- [x] Étape 7 : 1 cas — « bt021 Dark Transformation » (3 signatures posées → 3
      dégâts), subst. 1/1.
- [x] Étape 8 : **12 occurrences**.

**Carte terminée : OUI**

---

### bt022 : * Dark Beast (Minion nemesis)

- [x] Étape 2 : `an011`/bt021 (`WhenThisRevealed`) ; `05015`/`01083`
      (`GiveStatus`).
- [x] Étape 5 : mots-pièges : **`All allies`** (portée non qualifiée →
      arbitrage utilisateur : tous les alliés en jeu) ; **`Stalwart`** = base
      automatique, aucun module (le script ne porte que le When Revealed) ;
      `canbe_confused=True` (un allié protégé n'est pas une cible légale).
      Résultat : conforme.
- [x] Étape 6 : 6 PV / SCH 4 / ATK 1 / Boost 3 / `Stalwart: 1`.
      Résultat : conforme.
- [x] Étape 7 : 1 capacité scriptée, 1 cas — « bt022 Dark Beast » (deux alliés
      désorientés), subst. 1/1.
- [x] Étape 8 : **103 occurrences**.

**Carte terminée : OUI**

---

### bt023 : Mutant Science Program (SideScheme nemesis)

- [x] Étape 2 : `an011` (`WhenThisRevealed` + `GetToPlayer`) ;
      `aos/campaign.py` (`PlaceCountersInternal`) ; `AfterPlayerDrewCards`
      (factory/player.py:372) ; `Search.EncounterCards` ; `aa014`
      (`PutIntoPlay`).
- [x] Étape 5 : mots-pièges : **`for every ally in YOUR discard pile`** (la
      défausse du joueur visé, pas de tous) ; **asymétrie voulue** — 1 compteur
      par allié, mais **2[per_hero]** s'il n'y en a aucun (l'icône per_hero est
      sur le second nombre seulement, vérifiée sur l'image après rotation) ;
      **`remove … and discard … and find …`** (les trois parties, aucune
      optionnelle) ; **`the Lizard-Fied Minion`** (nom inexistant → arbitrage :
      bt020). Résultat : conforme.
- [x] Étape 6 : menace `5*` ; Boost 2 ; 1 compteur/allié ; 2[per_hero] sinon ;
      1 compteur retiré. Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas** (branche « aucun allié » → 2 compteurs,
      et branche « 3 alliés » → 3 compteurs). Subst. **2/2**.
- [x] Étape 8 : **49 occurrences**.

**Carte terminée : OUI**

---

## Bilan de la gate

| | Nombre |
|---|---|
| Cartes **terminées : OUI** | **25 / 25** |
| Cartes **terminées : NON** | **0** |

Les **28 cas** du pack passent (`test_capacites.py [bt0]` : 28/28), et la
substitution est complète : **23/23 cartes scriptées**, aucun cas resté vert
sans son module. Les deux cartes sans script (`bt009` ressource double,
`bt020` Guard/Patrol) n'ont aucune capacité à prouver, et sont vues en jeu
32 et 198 fois.

**Il ne reste donc, pour la gate finale de `PROCESSUS-HEROS.md`, qu'un seul
point : une partie complète jouée à la main.** Avec, au passage, les deux
vérifications que seul le navigateur permet :

- le **survol de la biographie** dans le wizard (preuve obligatoire de
  l'étape 7 de `PROCESSUS-HEROS.md`) ;
- le **déploiement `ui-app`** des textes FR.

Et, hors périmètre de la gate mais à confirmer au même moment : le retrait de
Squirrel Girl des héros proposés (masquage fait côté `catalog.js`, jamais vu
dans le navigateur).
