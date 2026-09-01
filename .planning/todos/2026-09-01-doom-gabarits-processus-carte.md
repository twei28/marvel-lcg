# PROCESSUS-CARTE.md — les 17 gabarits du pack DOCTOR DOOM (set 139, `dd`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
01/09/2026. Auteur du pack : **Grawlix Ipsum**.

**Preuves communes**, citées une fois :

- **Étape 7, substitution** : `substituer_pack.py .game-src 65000 dd0` →
  **15/15 cartes**, aucun cas resté vert sans son module.
- **Étape 8, autoplay** : 8 parties contre Rhino. **Grep exhaustif : 0 erreur
  sur les 8 journaux.** 4,4 rounds tenus (Beast 6,1 ; Agatha 5,0 — Doom est le
  plus fragile des trois avec 11 PV). `Power_Syphon` relevé **13 fois** et
  `Overwhelming_Power` **1 fois** dans les journaux : la mécanique vedette et
  l'extension `villainous` partent en partie réelle.
- **Étape 4, image** : `assets/pics/dd0*.png` pour les 17.
- **Étape 1** : pack `doctor_doom` en queue de `cards.json`, checksums refaits.
- `test_capacites.py [dd0]` : **17/17**.

---

### dd001a : * Doctor Doom (Hero)

- [x] Étape 2 : `AfterPlayerPlayedCard` (play.py:275), dont le message porte
      `paid_resources` ; compteurs plafonnés : `PlaceCountersInternal(...,
      maximum=3)` ; `GainUntilRoundEnd` (ab003, 12016).
- [x] Étape 5 : mots-pièges : **« using A [mental] resource »** (au moins une)
      → `HasColor`, à ne pas confondre avec le « **only** » de dd004/dd005/dd006
      → `OnlyHasColor` ; **« to a maximum of 3 »** confié au moteur, pas
      vérifié à la main ; **« Ignore any boost effects »** non codé (écart §5).
      Résultat : conforme.
- [x] Étape 6 : CTR 3 / ATQ 1 / DEF 2, MNG 5, 11 PV ; 1 compteur, max 3 ;
      3 compteurs dépensés. Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas**, subst. **2/2**.
- [x] Étape 8 : **713 occurrences**, `Power_Syphon` ×13.

**Carte terminée : OUI**

---

### dd001b : * Victor von Doom (AlterEgo)

- [x] Étape 2 : aucune capacité déclenchée — les deux lignes sont des
      **règles de deckbuilding**, appliquées au deck de départ et non scriptées.
- [x] Étape 5 : **« no additional allies »** → le deck d'aspect n'en contient
      aucun ; **« up to 6 TECH and/or SPELL from other aspects »** → 3 utilisées
      sur 6. Les deux sont vérifiées par un contrôle écrit pour l'occasion, qui
      a d'ailleurs attrapé une faute (Kaluu, un allié Leadership, et deux
      cartes ni TECH ni SPELL). Résultat : conforme.
- [x] Étape 6 : REC 3, MNG 6, 11 PV ; plafond de 6 cartes hors aspect.
- [x] Étape 7 : **aucun cas requis** — rien à déclencher. La contrainte vit
      dans le deck, et c'est le contrôle de légalité qui en fait foi.
- [x] Étape 8 : **135 occurrences**.

**Carte terminée : OUI**

> ⚠ **Écart assumé** : ces deux règles ne sont **pas opposables** par le moteur.
> Un joueur qui construit son propre deck dans le deckbuilder peut les
> enfreindre : rien ne l'en empêchera. Elles sont respectées dans le deck de
> départ livré, et documentées dans son `aspect_note`.

---

### dd002 : * Victorious (Ally)

- [x] Étape 2 : 01083 Mockingbird (`AfterCardEnterPlay`) ; 04001b Clint Barton
      (`Search.PlayerCard` + `GainCard`).
- [x] Étape 5 : **`include_player_deck` obligatoire** (piège bt011) ;
      le filtre vise un **événement** SPELL, pas toute carte SPELL ;
      « Toughness » lu dans `desc`, aucun module. Résultat : conforme.
- [x] Étape 6 : coût 3 / 3 PV / ATQ 3* / CTR 1*. Résultat : conforme.
- [x] Étape 7 : 1 cas, subst. 1/1.
- [x] Étape 8 : **32 occurrences**.

**Carte terminée : OUI**

---

### dd003 : Doombot (Ally, ×2)

- [x] Étape 2 : **45031 * Colossus**, jumeau exact au nom près — même texte,
      même montage repris tel quel.
- [x] Étape 5 : **`Requirement ([mental])`** = mot-clé OFFICIEL, base
      automatique `desc.Requirement` (has_cost.py:24), aucun module — fiche
      créée : `mots-cles/requirement.md` ; **« without exhausting it »** → ne
      pas appeler `ExhaustAll` après `DeclareDefender`, qui n'incline pas ;
      **CTR « — »** → la clé `THW` est **omise**. Résultat : conforme.
- [x] Étape 6 : coût 1 / 2 PV / ATQ 2*. Résultat : conforme.
- [x] Étape 7 : 1 cas, subst. 1/1. ⚠ **Deux défauts trouvés ici** : `"THW": "-"`
      levait `ValueError` dès la mise en place ; et il manquait
      `CanPlayThisAllyCard()`, sans quoi **l'allié n'était pas jouable du
      tout** — la trace montrait le pilote n'ayant que « Defense » en option.
- [x] Étape 8 : **245 occurrences**.

**Carte terminée : OUI**

---

### dd004 : "This World Is Mine!" (Event, ×3)

- [x] Étape 2 : 01053 Relentless Assault.
- [x] Étape 5 : **overkill/piercing vivent dans `AttackProperty`**, pas
      `DamageProperty` ; c'est le **héros** qui porte l'attaque, pas
      l'événement ; **« only »** → `OnlyHasColor`. Résultat : conforme.
- [x] Étape 6 : coût 3 ; 8 dégâts. Résultat : conforme.
- [x] Étape 7 : 1 cas, subst. 1/1.
- [x] Étape 8 : **42 occurrences**.

**Carte terminée : OUI**

---

### dd005 : "Doom Prevails" (Event)

- [x] Étape 2 : 15004 Hex Bolt (`CountTotalBoostIcons`) ; `GetTops(3)`.
- [x] Étape 5 : **« LOOK AT »** — les cartes restent sur le deck, on ne
      défausse pas (différence avec ho014) ; **« among »** = répartition ;
      X peut valoir 0. Résultat : conforme.
- [x] Étape 6 : coût 3 ; 3 cartes regardées ; X dégâts, X menaces.
- [x] Étape 7 : 1 cas, subst. 1/1. Le sommet du deck est fixé par
      `CreateEncounterDeck`, sinon X dépend du mélange.
- [x] Étape 8 : **5 occurrences**.

**Carte terminée : OUI**

---

### dd006 : "Pain Is For Lesser Men!" (Event, ×2)

- [x] Étape 2 : 01003 Backflip / 03005 Shield Block ; 05015 pour les statuts.
- [x] Étape 5 : **« stun AND confuse »** = les deux ; **« the enemy »** =
      l'attaquant de cette attaque. Résultat : conforme.
- [x] Étape 6 : coût 2. Résultat : conforme.
- [x] Étape 7 : 1 cas, subst. 1/1. ⚠ L'attaquant du cas est **Sandman
      (ATQ 3)** : la DEF 2 de Doom absorbait entièrement les 2 de Rhino, si
      bien que « when you WOULD take any amount of damage » n'était jamais
      atteint. Ni retirer le défenseur ni incliner Doom n'y changeaient rien.
- [x] Étape 8 : **40 occurrences**.

**Carte terminée : OUI**

---

### dd007 : Unparalleled Genius (Resource, ×2)

- [x] Étape 2 : **aucune capacité, aucun script**. Ressource à trois mentales,
      comme 01014 Energy Absorption (`YYY`).
- [x] Étape 5 : aucun texte de règles. Icônes lues au coin : **BBB**.
- [x] Étape 6 : 3 icônes. Résultat : conforme.
- [x] Étape 7 : **aucun cas requis** (aucune capacité). N'apparaît donc pas au
      bilan de substitution (15 cartes scriptées sur 17 entrées).
- [x] Étape 8 : **17 occurrences**, donc réellement dépensée.

**Carte terminée : OUI**

---

### dd008 : * Doomstadt (Support)

- [x] Étape 2 : aa002 * Scarlet Witch — `YouMayPlayCardLikeInHand(...,
      from_where="ThisPlacedCard")` + `TuckCardUnderHere`.
- [x] Étape 5 : **plafond de 3** vérifié en condition de l'action ;
      `GetPlacedCardArea().GetSize()` pour compter (et non un `GetPlacedCards()`
      inexistant) ; les événements restent **visibles** (aa002 les met face
      cachée). Résultat : conforme.
- [x] Étape 6 : coût 1 ; max 3. Résultat : conforme.
- [x] Étape 7 : 1 cas, subst. 1/1.
- [x] Étape 8 : **23 occurrences**.

**Carte terminée : OUI**

---

### dd009 : * Doom's Time Platform (Upgrade)

- [x] Étape 2 : aa014 (`ChooseAbilities`) ; an001a (`ReadyAll`) ;
      `ShuffleAllTo`.
- [x] Étape 5 : **« event OR upgrade »** = les deux types ; la seconde branche
      n'est proposée que si la défausse en contient. Résultat : conforme.
- [x] Étape 6 : coût 2 ; 1 carte remélangée. Résultat : conforme.
- [x] Étape 7 : 1 cas (première branche — le pilote prend toujours la
      première), subst. 1/1.
- [x] Étape 8 : **13 occurrences**.

**Carte terminée : OUI**

---

### dd010 : * Doom's Armor (Upgrade)

- [x] Étape 2 : an008/ho011 (`GiveKeywordToAttached`) ; 19005 pour le
      déclencheur d'attaque de base ; `AttackProperty.additional_boost_card`.
- [x] Étape 5 : **« +3 hit points »** = maximum, pas un soin ; **« If Doctor
      Doom HAS villainous »** est une **condition**, pas un coût — vérifiée
      avant de proposer l'inclinaison. Résultat : conforme.
- [x] Étape 6 : coût 3 ; +3 PV ; 1 carte de boost. Résultat : conforme.
- [x] Étape 7 : 1 cas (bonus continu), subst. 1/1.
- [x] Étape 8 : **9 occurrences**.

**Carte terminée : OUI**

> ⚠ **Écart connu** : n'accroche que l'**attaque** de base. Les trois pouvoirs
> sont concernés par `villainous`, mais seuls l'attaque (can_attack.py:220) et
> la manigance (can_scheme.py:92) distribuent des cartes de boost ; la défense
> n'a aucun chemin. À compléter quand Elektra arrivera.

---

### dd011 : * Doom's Mask (Upgrade)

- [x] Étape 2 : an007 (`resources_fn` évaluée au paiement) ; ab007 ;
      `GiveKeywordToAttached(steady=1)`.
- [x] Étape 5 : **piège ho009** — `res` est figé avant le `PayCost` dans le
      couple Can+Do de 31001a, d'où `resources_fn` ; la carte payée se lit dans
      `message.paying_for_card` ; **une seule `CanGenerateResources` par carte**
      (assert). Résultat : conforme.
- [x] Étape 6 : coût 3 ; 1 mental, 2 pour un SPELL. Résultat : conforme.
- [x] Étape 7 : 2 capacités, **2 cas** (ressource doublée, et steady),
      subst. **2/2**.
- [x] Étape 8 : **38 occurrences**.

**Carte terminée : OUI**

---

### dd012 : Rescue Cynthia von Doom (Obligation)

- [x] Étape 2 : aa014 / bt019 (squelette) ; iw015
      (`PlayersCannotChangeForms`).
- [x] Étape 5 : **« FLIP », pas « you MAY flip »** → changement **forcé**, on
      n'utilise pas `YouMayFlipToYourAlterEgoForm` (lecture vp011) ; **« You may
      not change form »** → blocage continu ; les deux branches sont des
      **actions durables**, pas les puces d'un choix unique — différence de fond
      avec aa014/bt019. Résultat : conforme.
- [x] Étape 6 : Boost 2 ; 1 carte TECH défaussée. Résultat : conforme.
- [x] Étape 7 : 1 cas, subst. 1/1.
- [x] Étape 8 : **28 occurrences**.

**Carte terminée : OUI**

---

### dd013 : Incomparable Ego (Obligation)

- [x] Étape 2 : 44032 « The Merc with the Mouth » (même couple « exhaust each
      ally » + « cannot ready ») ; an013/ho015 pour `[star] Boost`.
- [x] Étape 5 : **`CardCannotReady` rend une LISTE** d'abilities (d'où le `*`) ;
      **acceleration et hazard** sont des bases automatiques, identifiées par
      comparaison d'image et non à vue (leçon Lockjaw) ; **« discard a [mental] »**
      = une carte portant l'icône, d'où `has_printed_res="B"` et non
      `card_type=Resource`. Résultat : conforme.
- [x] Étape 6 : Boost 1, Acceleration 1, Hazard 1. Résultat : conforme.
- [x] Étape 7 : 1 cas, subst. 1/1.
- [x] Étape 8 : **46 occurrences**.

**Carte terminée : OUI**

---

### dd014 : Meddlesome Heroes! (SideScheme némésis)

- [x] Étape 2 : jj013 (`WhenSchemeBeDefeated`) ; aa014 (`ChooseAbilities`) ;
      kb019 (`TakeIndirectDamage`).
- [x] Étape 5 : **`WhenSchemeBeDefeated` et non `AfterSchemeBeDefeated`** —
      seule la première teste `is_when_defeated` ; **« OR »** = choix du joueur ;
      hazard automatique. Résultat : conforme.
- [x] Étape 6 : menace 4 ; 4 dégâts ou 4 menaces ; Boost 3.
- [x] Étape 7 : 1 cas, subst. 1/1. ⚠ **Deux corrections** : `GetInitiator()`
      levait `AssertionError: initiator=Rhino` (l'initiateur d'une carte de
      rencontre est le vilain) → `message.defeating_player` ; et le pilote
      jouait `dd006` pour **prévenir** les 4 dégâts, d'où un `main_exclusive`.
- [x] Étape 8 : **0 occurrence** — carte némésis, elle n'entre qu'après une
      obligation, ce qui n'arrive pas en 4,4 rounds. Preuve par son cas.
      L'image, livrée en portrait, a été **pivotée** (convention 01107).

**Carte terminée : OUI**

---

### dd015 : * Mister Fantastic (Minion némésis)

- [x] Étape 2 : **ah001a « Hypermind »** — même `Ability` brute sur
      `Message.CheckEffectGeneratedResources` + `SetResources` ;
      `EngagePlayer` (minion.py:128).
- [x] Étape 5 : **« each time you GENERATE »** — seule la production change de
      couleur, les icônes **imprimées** ne sont pas touchées ; **« engaged with
      you »** = ce joueur seulement ; Guard/Patrol/Boost automatiques.
      Résultat : conforme.
- [x] Étape 6 : 4 PV / SCH 2 / ATQ 2 / Boost 2. Résultat : conforme.
- [x] Étape 7 : 1 cas, subst. 1/1. ⚠ **Le premier cas ne prouvait rien** : il
      vérifiait la seule présence de la carte, vraie même sans le module, et
      restait **vert sous substitution (0/1)**. Il vérifie maintenant l'absence
      de compteur *power* après paiement via Doom's Mask.
- [x] Étape 8 : **0 occurrence** (carte némésis, voir dd014).

**Carte terminée : OUI**

---

### dd016 : Richards! (Treachery némésis, ×2)

- [x] Étape 2 : 21106 Proxima's Power / 11051 Ancient Grudge (`DoActivate`) ;
      bt023 (`Search.EncounterCards`).
- [x] Étape 5 : **« did NOT activate this way »** est un **repli**, pas un
      ajout — coder les deux ferait entrer un second sbire ; la recherche vise
      le **card_id** `dd015` et jamais le nom, « Mister Fantastic » désignant
      aussi le héros officiel mf001a et l'allié iw002. Résultat : conforme.
- [x] Étape 6 : Boost 3. Résultat : conforme.
- [x] Étape 7 : 1 cas, subst. 1/1. ⚠ **`include_set_aside=True` indispensable** :
      au début de partie les cartes némésis ne sont pas dans le deck rencontre,
      elles attendent dans `set_aside_nemesis_sets`. Sans ce drapeau la carte
      ne faisait rien — le journal listait dd012 et dd013 dans le deck, mais
      pas dd015.
- [x] Étape 8 : **0 occurrence** (carte némésis, voir dd014).

**Carte terminée : OUI**

---

## Bilan de la gate

| | Nombre |
|---|---|
| Cartes **terminées : OUI** | **17 / 17** |
| Cartes **terminées : NON** | **0** |

`test_capacites.py [dd0]` : **17/17**. Substitution : **15/15 cartes**
scriptées, aucun cas vert. Les deux cartes sans script (`dd007` ressource,
`dd001b` règles de deckbuilding) n'ont aucune capacité à prouver.

**Reste pour la gate de `PROCESSUS-HEROS.md` : une partie jouée à la main**,
avec le survol de la biographie dans le wizard et le déploiement `ui-app`.

**Deux écarts assumés, à ne pas oublier :**

1. Les **règles de deckbuilding** de `dd001b` ne sont pas opposables par le
   moteur : respectées dans le deck livré, contournables dans le deckbuilder.
2. `dd010` n'accroche que l'**attaque** de base ; la **défense** n'a aucun
   chemin de distribution de cartes de boost dans le moteur, et `dd001a`
   « Ignore any boost effects » n'a donc pas d'objet aujourd'hui. À reprendre
   avec Elektra.
