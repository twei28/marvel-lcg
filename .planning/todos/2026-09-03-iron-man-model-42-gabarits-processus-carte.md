# PROCESSUS-CARTE.md — les 15 gabarits du pack IRON MAN (MODEL 42) (set 151, `im`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
03/09/2026. Auteur du pack : **Rainy**.

**Preuves communes**, citées une fois :

- **Étape 7, substitution** : `substituer_pack.py .game-src 56000 im0` →
  **15/15 cartes prouvées**, et tous les cas tombent au rouge quand le module
  de leur carte disparaît. Passe **relancée après le correctif du coût** sur
  `im007`, `im008` et `im013` : la première passe ne prouvait plus les modules
  tels qu'ils sont livrés.
- **Étape 8, autoplay** : **32 parties** (Rhino et Klaw, normal et expert,
  profil équilibré, 8 graines). **Grep exhaustif : 0 erreur**, et **0 partie
  bloquée** après deux correctifs (voir §Bilan). ⚠ **0 victoire sur 32**, contre
  3 pour Lady Sif et 5 pour Hulk : 19 défaites sur la manigance principale,
  13 éliminations, 3,8 rounds tenus en moyenne. **Ce n'est pas un pack cassé** —
  le relevé des journaux montre le réacteur qui tourne : **144 compteurs posés**
  par `im001a` Reactor Cores, 18 par `im006` Tony's Workshop, dépensés par
  `im008` (12), `im007` (11) et les autres. C'est un héros dur : 10 PV, le plus
  fragile des trois, et une menée qui part en carburant. À revoir côté **deck
  d'aspect**, pas côté modules. Les 14 cartes du deck apparaissent dans les
  journaux (`im001a` 3229 occurrences, `im006` 374, `im008` 307) ; `im012`
  Hulkbuster est à 0, ce qui est correct : c'est la variante, elle n'est pas
  dans le deck livré.
- **Témoins** : le même autoplay relancé sur `lady_sif` et `hulk_rainy` après le
  correctif du pilote rend **exactement** leurs chiffres antérieurs (3/32 et
  5/32, 0 incident) : le correctif est un non-événement là où rien ne bloquait.
- **Étape 4, image** : `assets/pics/im0*.jpg` pour les 15, découpées du zip
  `Iron Man (Model 42)-20260902T073854Z-1-001.zip` (19 fichiers, 15 cartes
  distinctes : Repulsor Barrage ×2, Tactical Overview ×2, Take Flight ×3).
- **Étape 1** : pack `iron_man_model_42` en queue de `cards.json`, set
  `151. Custom (Iron Man Model 42)` dans `sets_info.json`, préfixe `im` mis à
  jour, checksums recalculés, `verifier_prefixes` OK.
- `test_capacites.py [im0]` : **22/22 cas verts**.
- `test_cards` : **5116 ok / 0 erreur** (5101 avant le pack, +15).
- `verifier_appels_modules` : « tous les appels de iron_man_model_42
  existent » ; `verifier_cartes_en_jeu` : « les 15 cartes de iron_man_model_42 portent
  ce que leur texte annonce ».
- **Étape 10 de PROCESSUS-HEROS** : contrôle relancé sur les **114 decks de
  départ** → **0 écart**, alors que le héros porte le nom du héros officiel
  `01029a`.
- **Les 15 scans ont été relus un par un** avant la première ligne de code, et
  les douze icônes de ressource croisées à l'intérieur du pack (leçon
  Lockjaw) : quatre énergie, deux physique, deux mental, une wild pour
  `im005`.

**Le compteur `reactor` est un mot-clé maison de fait**, et il a fallu
l'ajouter à l'énum `COUNTER` du moteur
(`src/game/card/face/card_face.py`) : sans lui, `IsCounter` refuse le nom et
**toute carte qui en pose tombe à la création de la partie**, pas en jeu.
Même geste que `flame` (human_torch), `illusion` (spider_man_rainy) ou
`adrenaline` (venompool) avant lui.

**Cinq décisions de l'utilisateur**, prises le 03/09/2026 avant la première
ligne de code :

1. `set_name` = **`Iron Man (Model 42)`** — « Iron Man » est pris par
   `01029a`, « Superior Iron Man » par le pack `si`.
2. Set némésis : **emprunté à l'Iron Man officiel** (`01171`, `01172`,
   `01173` ×2, `01174`), le zip n'en fournissant aucun.
3. Aspect du deck de départ : **Agressivité**.
4. `im012` Hulkbuster Armor : **les deux cartes créées**, `im011` Save The Day
   dans le deck livré.
5. « Spend X **printed** [energy] resources » : **lecture littérale**.

**Le pack en une phrase** : un compteur, et dix cartes qui le lisent. Quatre
en posent, huit en dépensent, et le héros n'a que 10 PV — le réacteur est à la
fois la ressource offensive et la réserve de survie.

---

### im001a : * Iron Man (Hero)

- [x] Étape 2 : **`29038` Haywire** pour le sélecteur
      `SetTarget(has_printed_res="Y", from_where=["YourHandCards"])` ;
      **`01174` Electromagnetic Backlash** et `23013` * Captain Marvel pour
      `FacesCounter.GetPrintedResourcesCount(faces, "Y")`. Les deux chemins
      servent : le sélecteur dit QUELLES cartes sont dépensées, le compteur dit
      COMBIEN de ressources elles valent.
- [x] Étape 5 : mots-pièges : **« printed »** exclut les ressources GÉNÉRÉES,
      donc `im005` Stark Tower ne peut pas charger le réacteur (arbitrage
      utilisateur) ; **« place X counters HERE »** : sur l'identité ; le type
      imprimé est `Action` **nu**, pas `Hero Action` ; aucune limite imprimée.
      Résultat : conforme.
- [x] Étape 6 : CTR 2 / ATQ 2 / DEF 2, MNG 5, **10 PV**. Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas**.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Défaut corrigé avant le premier test : X compte les RESSOURCES, pas les
> cartes.** La première écriture posait `len(cartes)` compteurs. Or
> « X printed [energy] **resources** » compte les ICÔNES : `01088` Energy
> porte `RES = "YY"` et vaut donc **2 compteurs à elle seule**. Compter les
> cartes aurait sous-payé le joueur **en silence** sur toutes les cartes à
> double icône, et aucun outil ne l'aurait vu. C'est le cas de test, écrit
> exprès sur `01088`, qui rend la chose vérifiable.

**Carte terminée : OUI**

---

### im001b : * Tony Stark (AlterEgo)

- [x] Étape 2 : `an001b` * Aldrif Odinsdottir et `ok001b` * Okoye pour le
      Setup (`WhenCardSetup` + `Search.PlayerCard` + `GainCard`) ; `10025`
      Inner Demons pour `DiscardHandCards` ; **`16024` Deft Focus** via
      `aa009` pour `Worlds.UpdateNextCardPlayCost`.
- [x] Étape 5 : mots-pièges : **« Discard 1 card → »** est un COÛT, on lit son
      retour ; **« a TECH UPGRADE »** : le trait ET le type ; **« search your
      DECK »** seulement, pas la défausse — contrairement à `ls005` du pack
      précédent ; **« the next UPGRADE played »** : le type, pas un trait ;
      « once per ROUND ». Résultat : conforme.
- [x] Étape 6 : REC 3, MNG 6, 10 PV ; réduction de 1. Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas**. Celui de l'Action est sujet par
      construction : la main ne contient QUE `im010` (coût 1), donc aucune
      ressource pour la payer. Si elle entre en jeu, c'est que son coût est
      tombé à 0.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Écart assumé, et il est dans le moteur.** La carte dit « this **ROUND** »
> mais `UpdateNextCardPlayCost` n'accepte que `in_this="Phase"` ou `"Turn"`
> (`worlds.py:815`) : il n'y a pas de portée « Round ». On prend `"Phase"`, la
> plus large. La différence ne se verrait que si une amélioration était jouée
> pendant la phase du vilain.

**Carte terminée : OUI**

---

### im002 : Repulsor Barrage (Event, ×2)

- [x] Étape 2 : `01053` Relentless Assault pour l'événement d'attaque à
      `AttackProperty` ; **`27071` Sand Storm** pour la répartition libre
      (`player.AssignDamage`) ; `50134` / `ho010` pour le « you may » payé.
- [x] Étape 5 : mots-pièges : **« You MAY remove »** — facultatif ET coût,
      donc les 3 dégâts supplémentaires ne tombent que si le compteur est
      réellement parti ; **« to THAT enemy »** : la même cible ; **« If Iron
      Man has AERIAL »** : lu à la résolution, pas au paiement ; **« you may
      divide »** : la répartition est facultative, `AssignDamage` couvre les
      deux. Résultat : conforme.
- [x] Étape 6 : coût 2, ressource énergie ; 3 + 3 dégâts. Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas** (branche compteur, 6 dégâts).
- [x] Étape 8 : voir preuve commune.

> ⚠ **Écart assumé** : `AssignDamage` (`player_action.py:93`) n'accepte pas de
> `property`, donc la branche AERIAL **ne porte pas le mot-clé `ranged`**. La
> branche normale, si. La différence ne se voit que face à une Riposte.

**Carte terminée : OUI**

---

### im003 : Tactical Overview (Event, ×2)

- [x] Étape 2 : la jumelle exacte de `im002`, côté menée. `hk003` / `an004`
      pour `RemoveThreatFromSchemes`.
- [x] Étape 5 : mots-pièges : les mêmes que `im002`, plus **« from THAT
      scheme »**. Résultat : conforme.
- [x] Étape 6 : coût 2, ressource mentale ; 3 + 3 menaces. Résultat :
      conforme.
- [x] Étape 7 : 1 capacité, **1 cas**. ⚠ La principale est chargée à **6** et
      non à 8 : son seuil est de 7 par joueur, et la poser à 8 **terminait la
      partie** avant que le cas ne joue — la carte n'était jamais jouée et le
      cas échouait sans aucun rapport avec la carte.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Il n'existe AUCUN `AssignThreat`**, contrairement aux dégâts.
> `RemoveThreatFromSchemesTotal` (`card_face.py:734`) ne fait pas ce que son
> nom laisse croire : il retire **1** menace à chacune des N premières
> manigances, ce qui n'est pas « répartir N menaces librement ». La
> répartition libre est donc rendue en posant la question **une fois par
> point** retiré. En solo c'est identique ; à plusieurs manigances, c'est la
> lettre du texte.

**Carte terminée : OUI**

---

### im004 : Take Flight (Event, ×3)

- [x] Étape 2 : `ho011` / `vv009` pour `Faces.ReadyAll` ; `38007` Energy
      Transfer pour `GainUntilRoundEnd(effect, trait=...)`.
- [x] Étape 5 : mots-pièges : **l'ORDRE DE LECTURE est le piège de la carte** —
      « If Iron Man **ALREADY** has AERIAL » se lit AVANT que la carte ne donne
      le trait, sinon la condition est toujours vraie et la carte pose un
      compteur à chaque fois ; « until the end of the ROUND » ; les deux
      premiers effets sont inconditionnels. Résultat : conforme.
- [x] Étape 6 : coût 1, ressource énergie ; 1 compteur conditionnel.
      Résultat : conforme.
- [x] Étape 7 : 1 capacité, **2 cas** — le contre-cas sans AERIAL (aucun
      compteur) et le cas nominal avec `im010` en jeu. C'est la paire qui
      prouve l'ordre de lecture.
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### im005 : * Stark Tower (Support)

- [x] Étape 2 : `an007` Asgard's Assassin et `ma005` * Star Light —
      `CanGenerateResources(AbilityType.Resource, Resources("G"))` +
      `CostFunc.Exhaust("This")`.
- [x] Étape 5 : mots-pièges : **« Resource » NU**, pas « Hero Resource » — la
      ressource se génère dans les DEUX formes, et le cas est monté en forme
      civile pour le prouver. Résultat : conforme.
- [x] Étape 6 : coût 3, ressource wild. Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas**, sur le montage de preuve de `vv010` :
      la main est réduite à la seule carte à payer, le soutien est donc
      l'unique source possible.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Écart assumé — « for ANY PLAYER ».** Le moteur n'expose aucun paramètre
> pour offrir une ressource générée à un AUTRE joueur : la signature de
> `CanGenerateResources` (`resources.py:277`) propose `for_card`,
> `for_ability`, `from_hand`, `for_player_whose_identity_has_trait`, mais rien
> qui désigne un destinataire. La ressource va au joueur qui paie. En solo les
> deux lectures sont identiques.

> ⚠ **Conséquence de l'arbitrage sur `im001a`** : cette carte GÉNÈRE un wild,
> elle ne porte donc pas d'icône énergie imprimée au sens de Reactor Cores.
> **Stark Tower ne peut pas charger le réacteur.** C'est voulu : sans cette
> lecture, un seul Stark Tower le rechargerait indéfiniment.

**Carte terminée : OUI**

---

### im006 : * Tony's Workshop (Support)

- [x] Étape 2 : `aa003` * Ebony pour le squelette ; `38007` / `hk011` pour
      `HealthUnits` ; `im001a` du même pack pour `Faces.PlaceCountersOn`.
- [x] Étape 5 : mots-pièges : **« heal ... from Tony Stark » et « place ... on
      him »** visent la MÊME carte, l'identité — on passe par `GetIdentity()`
      et non par un `CardFinder(name="Tony Stark")`, l'alter-ego officiel
      `01029b` portant exactement ce nom ; `Alter-Ego Action`, donc rien en
      forme de héros. Résultat : conforme.
- [x] Étape 6 : coût 1, ressource physique ; 1 soin, 1 compteur. Résultat :
      conforme.
- [x] Étape 7 : 1 capacité, **1 cas**, monté en forme civile — c'est la seule
      source de réacteur accessible hors forme de héros, et le compteur va
      donc sur `im001b`.
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### im007 : Energy Shield (Upgrade)

- [x] Étape 2 : `03009` / `ls010` pour `GiveKeywordToAttached(Hero,
      defense=1)` ; **`si016` * Tony Stark A.I.** (mot-clé maison « Armored 2 »)
      et `01098` Armored Rhino Suit pour `PreventDamage`. ⚠ Coïncidence utile :
      `si016` est un sbire némésis dont le `desc.Nemesis` vaut « Tony Stark ».
- [x] Étape 5 : mots-pièges : **« IRON MAN gets +1 DEF »** cite un nom PROPRE,
      la face héros seule (piège an002) ; **« any amount of damage »** : toute
      instance, pas seulement une attaque ; **« remove 1 counter → »** est un
      COÛT, d'où le retour de `RetirerUnReacteur` ; **« prevent UP TO 2 »**.
      Résultat : conforme.
- [x] Étape 6 : coût 2, ressource énergie ; +1 DEF, 2 dégâts prévenus.
      Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas**. ⚠ **Le héros est incliné à la mise en
      place** du second : au premier passage il se déclarait défenseur, sa
      DEF 2+1=3 absorbait les 2 dégâts de Rhino, et la prévention n'avait plus
      rien à prévenir — le cas passait au vert pour la mauvaise raison,
      compteur intact.
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### im008 : * Mark IVa Repulsors (Upgrade)

- [x] Étape 2 : **`41019` Directed Force** pour `DealAdditionalDamage(2)` ;
      `WhenUnitWouldAttack(..., is_basic_attack=True)`, qui porte à la fois
      `DealAdditionalDamage` et `GainRanged`.
- [x] Étape 5 : mots-pièges : **« makes a BASIC attack »** —
      `is_basic_attack=True` est indispensable, sans lui `im002` en
      profiterait ; **« remove 1 counter → »** : coût ; **« THAT attack »** :
      celle en cours. Résultat : conforme.
- [x] Étape 6 : coût 1, ressource énergie ; +2 dégâts. Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas** (ATQ 2 + 2 = 4).
- [x] Étape 8 : voir preuve commune.

> ⚠ **Pourquoi `WhenUnitWouldAttack` et non `WhenUnitUseBasicPower`.** Les deux
> fenêtres existent et `32177` Swagger emploie la seconde — mais Swagger
> modifie la DEF, une valeur du POUVOIR, alors qu'ici il faut modifier
> l'ATTAQUE elle-même. `DealAdditionalDamage` et `GainRanged` ne vivent que
> sur `WhenUnitWouldAttack`.

**Carte terminée : OUI**

---

### im009 : * Repulsor Core One (Upgrade)

- [x] Étape 2 : `ho011` * Goblin Glider / `ls008` Sif's Steed pour l'action
      payée par `CostFunc.Exhaust("This")` ; `ho009` pour le coût arbitraire
      `CostFunc.Custom(None, fn)`.
- [x] Étape 5 : mots-pièges : le coût de la seconde action a **DEUX parties** —
      retirer un compteur ET incliner la carte (piège `wd005`) ; le retrait
      passe par `CostFunc.Custom`, dont le False bloque le paiement, donc sans
      compteur l'action n'est pas proposée ; **« place ... on Iron Man »** :
      l'identité, pas l'amélioration. Résultat : conforme.
- [x] Étape 6 : coût 2, ressource énergie. Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas**. Les deux actions sont `HeroAction`,
      donc le `type` ne les distingue pas : c'est `index` qui les sépare.
- [x] Étape 8 : voir preuve commune.

> **La carte pivot du pack** : elle convertit dans les deux sens, une
> activation en compteur ou un compteur en activation. Les deux actions
> partagent le même coût d'inclinaison, donc une seule part par round.

**Carte terminée : OUI**

---

### im010 : Rocket Boots (Upgrade)

- [x] Étape 2 : `vv009` / `ho011` pour `GiveKeywordToAttached(...,
      trait="AERIAL")` ; **`32177` Swagger** pour
      `WhenUnitUseBasicPower(HeroInterrupt, ...)` + `message.GainValue(1,
      effect)`.
- [x] Étape 5 : mots-pièges : **« IRON MAN gains »** : nom propre, face héros
      seule ; **« ONE OF Iron Man's basic powers »** : les trois, donc AUCUNE
      condition sur `message.power`, contrairement à Swagger qui filtre sur
      'DEF' ; **« +1 to THAT power »** : au pouvoir employé, jamais un
      `GainUntilRoundEnd` qui durerait tout le round. Résultat : conforme.
- [x] Étape 6 : coût 1, ressource physique ; +1. Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas**. `GainValue` redirige tout seul vers le
      bon sous-message (`sender_unit.py:21`) : c'est ce qui rend « that power »
      sans avoir à savoir lequel.
- [x] Étape 8 : voir preuve commune.

> **La carte qui débloque le pack.** Elle donne AERIAL en permanence, ce qui
> rend `im002` et `im003` répartissables, fait de `im004` une source de
> compteur à 1 [energy], et active `42029` Bombs Away côté aspect. C'est la
> pièce que `im001b` va chercher au Setup, puisqu'elle est TECH.

**Carte terminée : OUI**

---

### im011 : Save The Day (Upgrade)

- [x] Étape 2 : **`dz013` Velvet Sky** et `09007` Protective Ward pour
      `CancelAllEffectsAndDiscardIt` ; `08018` Spycraft pour
      `CostFunc.Discard("This")` ; `hk005` Interception du pack `hulk_rainy`
      pour le même texte au coût près.
- [x] Étape 5 : mots-pièges : **« cancel ALL of its effects »** → niveau
      « All », et pas le `CancelWhenRevealedEffect`, qui laisse passer les
      mots-clés (Surge compris) ; le coût a **DEUX parties** ; **« When a
      treachery is revealed »** sans « you » → `"AnyPlayer"`, et sans « from
      the encounter deck » → pas de `from_encounter`. Résultat : conforme.
- [x] Étape 6 : coût 1, ressource énergie. Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas** (`01105` « I'm Tough » annulée, Rhino ne
      reçoit aucune carte Tenace).
- [x] Étape 8 : voir preuve commune.

**Carte terminée : OUI**

---

### im012 : * Hulkbuster Armor (Upgrade, variante de `im011`)

- [x] Étape 2 : `05023` / `hk011` pour `GiveKeywordToAttached` ; `ls011` Sif's
      Sword pour `UnitAttackGainKeyword(..., is_basic_attack=True)` ; `si016` /
      `01098` pour `PreventDamage`, ici en version « All » ; `32177` Swagger
      pour `Faces.RemoveAllFromGame`.
- [x] Étape 5 : mots-pièges : **« -1 hand size » est un MALUS réel** — la main
      passe de 5 à 4, ce qui est cher pour un héros qui convertit sa main en
      compteurs ; **« his BASIC attacks »** → `is_basic_attack=True` ;
      **`Interrupt` NU, pas `Hero Interrupt`** : la prévention marche dans les
      DEUX formes, contrairement à `im007` ; **« from the GAME »**, pas une
      défausse. Résultat : conforme.
- [x] Étape 6 : coût 2, ressource physique ; -1 main, +1 ATQ, +1 DEF.
      Résultat : conforme.
- [x] Étape 7 : 3 capacités, **2 cas** (les bonus continus d'un coup, puis la
      prévention totale). Le Déferlement sur les attaques de base n'a pas de cas
      dédié : écart assumé, voir §Reste à faire. ⚠ Le héros est incliné à la
      mise en place du second cas, même raison que `im007`.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Carte ALTERNATIVE.** L'auteur la donne comme « alternative replacement
> for Save The Day » et les deux portent le numéro imprimé **14/15** : ce n'est
> pas un cumul, c'est un choix de deckbuilding. Décision de l'utilisateur : les
> DEUX cartes existent, et c'est `im011` qui part dans le deck livré.

**Carte terminée : OUI**

---

### im013 : Tactical Interface (Upgrade)

- [x] Étape 2 : **`32177` Swagger** pour la fenêtre et `message.GainValue` ;
      **`61023` Grapnel Launcher** et `42006` Natural Flight pour l'exemption
      de Patrouille.
- [x] Étape 5 : mots-pièges : **« makes a BASIC thwart »** — le filtre sur
      `message.power == 'THW'` est indispensable, sinon la carte se
      déclencherait aussi sur l'attaque et la défense ; **« remove 1 counter
      → »** : coût ; Patrouille protège le complot PRINCIPAL, sans l'exemption
      la carte promettrait quelque chose qu'elle ne ferait pas (leçon `gp005`).
      Résultat : conforme.
- [x] Étape 6 : coût 1, ressource mentale ; +2 menaces. Résultat : conforme.
- [x] Étape 7 : 1 capacité, **1 cas** (CTR 2 + 2 = 4).
- [x] Étape 8 : voir preuve commune.

> ⚠ **Pourquoi pas `.SetIgnoreKeyword('Patrol')` sur cette abilité.** C'est ce
> que fait `61023` — mais `61023` EFFECTUE elle-même la menée, donc son propre
> effet porte l'exemption. Ici la menée est celle du JOUEUR, faite par un autre
> effet : notre `SetIgnoreKeyword` ne serait jamais consulté.
> `effect.IsIgnoreKeyword` (`effect.py:493`) offre l'autre chemin, un message
> `CheckIfEffectIsIgnoreKeyWord` auquel répond
> `UnitIgnoreKeywordIcons(..., while_use_basic_thw=True)` (`play.py:443`), ici
> enregistré **en temporaire** puisque l'exemption est conditionnée au
> compteur payé.

**Carte terminée : OUI**

---

### im014 : Technical Issues (Obligation)

- [x] Étape 2 : **`an010` Banished from Asgard**, jumeau de STRUCTURE et pas
      seulement d'esprit : même `YouMayFlipToYourAlterEgoForm`, même
      `ChooseAbilities` à deux branches, même `GainSurge` conditionné à un
      effet qui n'a rien fait, même `Otherwise` en repli.
- [x] Étape 5 : mots-pièges : **« You MAY flip »** et non « must » ; la
      première branche exige **DEUX cartes inclinables**, Tony Stark ET Tony's
      Workshop (piège `wd005`) ; **« remove ... from the GAME »** pour la
      branche indolore contre une DÉFAUSSE pour l'autre ; **« If NO reactor
      counters were removed THIS WAY »** : le surge tombe seulement si le
      compteur était à ZÉRO, donc on lit le nombre RÉELLEMENT retiré.
      Résultat : conforme.
- [x] Étape 6 : 1 icône de boost, `GiveTo` = « Tony Stark », 2 compteurs.
      Résultat : conforme.
- [x] Étape 7 : 1 capacité, **2 cas** — la branche indolore avec l'atelier en
      jeu, et le contre-cas sans atelier ni compteur.
- [x] Étape 8 : voir preuve commune.

> ⚠ **Le défaut le plus cher du pack, et c'est exactement celui de `ls014` la
> veille.** `Player.GetPlayArea()` **n'existe pas**. La première écriture
> l'appelait pour trouver Tony's Workshop, et le moteur a **avalé
> l'AttributeError** : l'obligation ne faisait plus RIEN — ni bascule, ni
> inclinaison, ni défausse — et rien ne l'écrivait nulle part. Ni `test_cards`,
> ni `verifier_appels_modules` (qui vérifie que le NOM existe, pas sur quel
> type), ni `verifier_cartes_en_jeu` ne le voient. **Seuls les deux cas de test
> l'ont sorti.** Le bon accesseur est `joueur.supports.Get()`
> (`player.py:75`).
> Au passage : `condition` de `ForChoiceAbility` attend un **booléen**, pas un
> callable (`for_choice.py:43`).

**Carte terminée : OUI**

---

## Bilan

**15 cartes, 15 « Carte terminée : OUI ».**

### La leçon se répète, et elle est maintenant chiffrée

Trois packs d'affilée, le même défaut : **le moteur avale les exceptions des
modules de cartes, et la carte ne fait rien sans que rien ne le signale.**

| Pack | Carte | Appel fautif | Trouvé par |
|---|---|---|---|
| `lady_sif` | `ls014` | `Player.GetHero()` hors forme héros (assert) | cas de test |
| `lady_sif` | `ls014` | `CancelThisAttack` absent de `WhenUnitBeingAttack` | cas de test |
| `iron_man_model_42` | `im014` | `Player.GetPlayArea()` n'existe pas | cas de test |

Aucun n'était visible en lecture, aucun outil statique ne les voit. La règle
qui s'en dégage, à appliquer avant d'écrire une ligne : **vérifier qu'une
méthode existe SUR LE TYPE qu'on appelle**, pas seulement qu'un nom du même
genre existe quelque part dans le moteur.

### Le harnais ment aussi quand on lit son verdict trop vite

Trois cas passaient ou échouaient pour la mauvaise raison :

- `im007` et `im012` : le héros se déclarait **défenseur**, sa DEF absorbait
  les dégâts, et la prévention n'avait plus rien à prévenir. **Incliner le
  héros à la mise en place** est ce qui a rendu les cas sujets.
- `im003` : charger la principale à **8** alors que son seuil est de **7 par
  joueur** terminait la partie avant que le cas ne joue. La carte n'était
  jamais jouée, et l'échec ne disait rien d'elle.

### Les deux blocages, et pourquoi le premier correctif n'a pas suffi

Les 22 cas étaient verts, `test_cards` sans erreur, et le pack bloquait une
partie sur 32. **Deux causes, l'une dans le pack, l'autre dans le pilote.**

**1. Le coût était dans le CORPS et non dans le COÛT.** `im007`, `im008` et
`im013` écrivaient `if RetirerUnReacteur(...): <effet>`. Réacteur vide, la
capacité **résout quand même et ne fait rien** : le moteur la repropose à
l'identique, le pilote la reprend, la partie tourne en rond. C'est le défaut du
blocage Underling du 20/08. Dans le coût (`CoutDuReacteur`), le `False` empêche
le paiement et l'option n'est même pas offerte. `im009` et `im011` le faisaient
déjà correctement.

**2. Les deux empreintes du pilote ignoraient les compteurs.**
`tools/autoplay.py` compare deux signatures du monde : celle du garde-fou
anti-répétition (`empreinte`) et celle du désistement (`progres`). Ni l'une ni
l'autre ne lisait les compteurs. Or `im007` dépense un compteur pour
**prévenir** des dégâts : les PV ne baissent pas, justement parce que la
prévention a marché, et aucun des neuf termes ne bouge. La capacité passait
pour inerte alors que le journal montre noir sur blanc le compteur retiré et
les 2 dégâts prévenus.

⚠ **Et la première passe n'a corrigé qu'une des deux empreintes.** Le blocage
ne s'est pas résorbé : il s'est **déplacé** d'un garde-fou à l'autre, avec un
message différent. Les compteurs passent désormais par un **helper partagé**,
`compteurs_du_joueur`, précisément pour que les deux signatures ne puissent
plus diverger. C'est la troisième fois de la journée que ce fichier trébuche
sur la même chose : deux lectures du monde qui ne regardent pas le même monde.

**Mesure : 1 partie bloquée → 0**, et les deux témoins (`lady_sif`,
`hulk_rainy`) rendent leurs chiffres antérieurs au chiffre près.

### Reste à faire (écarts assumés, aucun bloquant)

- **Une capacité sans cas dédié** : le Déferlement sur les attaques de base de
  `im012`. Montage recopié à l'identique de `ls011`, vérifié au chargement.
- **`AssignDamage` ne porte pas `ranged`** : la branche AERIAL de `im002`
  perd le mot-clé. Visible seulement face à une Riposte.
- **`im005` « for any player »** : le moteur n'a pas de paramètre pour offrir
  une ressource générée à un autre joueur. Sans effet en solo.
- **`im001b` « this round »** rendu par `"Phase"`, faute de portée « Round »
  dans `UpdateNextCardPlayCost`.
