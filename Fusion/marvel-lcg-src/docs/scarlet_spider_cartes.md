# Pack Scarlet Spider — fiches PROCESSUS-CARTE.md, une par card_id

Gabarit suivi : `PROCESSUS-HEROS.md` / `PROCESSUS-CARTE.md`. 23 card_id au
total (`ss001a` à `ss022`, la face `a`/`b` de Scarlet Spider comptant pour
deux identifiants distincts). Source : pack fan-made CptScorp (« Marvel
Champions Custom Project »), zip `Scarlet Spider` — 23 cartes physiques
scannées (2 faces héros + 15 signature + 1 obligation + 5 némésis).
Personnage : Kaine Parker, clone de Peter Parker devenu Scarlet Spider.

Étapes 1-6 de PROCESSUS-HEROS (cards.json, deck de départ, nemesis json,
sets_info.json, prefixe déclaré, trait CLONE ajouté au moteur) faites lors
d'une session antérieure. Cette session a repris à l'étape 2 de
PROCESSUS-HEROS (scripts) et a couvert le reste (images, biographie, texte
FR, validation carte par carte, autoplay, gate finale).

## Deux points tranchés par Claude le 29/08/2026

1. **Aspect du deck de départ** : aucune decklist d'aspect fournie par
   l'auteur (comme pour Okoye et Iron Lad). **Aggression** choisi (kit
   signature dominé par le dégât cible unique physique — Precise Force,
   Unrestrained, Stings of Kaine, tous RES physique — et la synergie
   overkill/piercing — Mark of Kaine, Stings of Kaine, Spider Stealth
   Suit). Voir `metadata.aspect_note` de `deck/starter/scarlet_spider.json`.
2. **`desc.Class` manquant sur les 15 cartes signature** (ss002-ss016) :
   trouvé par `verifier_coherence_cartes.py` en tout début de cette
   session (« cartes joueur sans classe d'aspect : 15 »). Ce n'était pas un
   choix mais un oubli de la session précédente qui a écrit les données —
   corrigé en ajoutant `"Class": "Hero"` à chaque `desc` (modèle exact :
   toutes les cartes signature d'Okoye et d'Iron Lad portent ce champ),
   checksum de `data/cards.json` recalculé.

## Outils exécutés depuis `.game-src`

- `tools/test_cards.py` : **4588 ok / 0 err** (pack `scarlet_spider` inclus,
  aucune régression sur les autres packs — référence avant ce pack :
  4565 ok pour iron_lad).
- `tools/verifier_prefixes.py` : OK, aucun doublon, préfixe `ss` déjà
  déclaré dans `tools/prefixes_fanmade.json` (fait en session antérieure).
- `tools/verifier_coherence_cartes.py` : 0 obligation sans destinataire,
  **0 carte joueur sans classe** (15 corrigées, voir plus haut), 0 image
  manquante pour le pack `scarlet_spider`. Les autres lignes du rapport
  (collisions de noms « Scarlet Spider » avec 3 alliés officiels d'autres
  packs — spiderham/30020, silk/52013, madame_web/mw022 — et « Kaine
  Parker » sans collision) sont des collisions **de noms**, jamais de
  `card_id` : le moteur distingue toujours les cartes par `card_id`, donc
  aucune collision technique. Une conséquence réelle de cette ambiguïté DE
  NOM a été rencontrée et contournée : voir le bug n°2 ci-dessous.
- Deck de départ (`tools/verifier_tous_les_decks.py`, restreint via
  `DECK_NOM=scarlet_spider`) : partie montée avec succès, identité
  `ss001a`, main 5, deck restant 31-34 selon le tirage.
- Script de contrôle « jamais une carte signature d'un autre héros dans un
  deck » (PROCESSUS-HEROS §10) : **0 résultat**, sur les 90 decks de
  départ du dépôt, `scarlet_spider` inclus.
- `tools/test_capacites.py` : **21 cas dédiés au pack `scarlet_spider`,
  21/21 verts** (indices 566-586). Répartition : un cas par capacité
  distincte des cartes non dupliquées, et un cas partagé pour chaque lot
  de cartes physiquement dupliquées (Grim Resolve x2, Precise Force x3,
  Spider-pathy x2, Unrestrained x2, Mark of Kaine x3), exactement le même
  principe qu'Iron Lad (Ion Blast x3, Seeking Solutions x2...), plus un
  cas de non-régression dédié au bug moteur du 30/08/2026 (voir bug n°3).
  **Trois vrais bugs trouvés et corrigés** en écrivant ces cas (preuve par
  substitution rouge/vert directe), détail ci-dessous — dont deux dans le
  moteur partagé, pas dans les scripts du pack.
- `tools/autoplay.py` : **8 parties contre `rhino`, profil `equilibre`,
  0 partie bloquée, 0 traceback** (grep exhaustif
  `NameError|AttributeError|TypeError|KeyError|AssertionError` sur les 8
  journaux : 0 partout ; grep élargi `traceback|exception` : 0 partout
  aussi). 0/8 victoires, 4,2 rounds tenus en moyenne, 8/8 parties terminées
  par « The Main Scheme was Completed » (aucune élimination de joueur).
  Toutes les capacités du pack ont été observées en jeu réel dans le
  journal détaillé d'au moins une des 8 parties (recherche des 23
  card_id) : `ss001a` à `ss022` tous présents. **Témoin `okoye`** (héros
  déjà audité à 100%, même scénario/profil) : 0/8 victoires, 0 bloquée,
  4,1 rounds tenus en moyenne, 6/8 terminées par complot achevé et 2/8 par
  élimination des joueurs — taux de blocage et de survie comparables,
  aucun écart anormal.

> ⚠ **Indices décalés de +56 depuis la fusion dans `master` (30/08/2026).**
> Les numéros de cas cités DANS LE CORPS de cette fiche sont ceux de la
> branche `worktree-okoye`, avant l'arrivée des packs `dazzler`,
> `wolverine_x23`, `superior_iron_man` et `kate_bishop` qui les précèdent
> désormais dans `CAS`. Pour retrouver un cas, ajouter 56 à l'indice écrit.

## Bugs réels trouvés et corrigés (preuve par substitution)

1. **ss002 à ss016 (15 cartes signature)** — `desc.Class` absent de
   `data/cards.json`, détecté par `verifier_coherence_cartes.py` avant
   même d'écrire un seul script. Corrigé en ajoutant
   `"Class": "Hero"` à chaque `desc` (modèle Okoye/Iron Lad), checksum
   recalculé via `tools/recalculer_checksums.py`.
2. **ss022 (Forced Contract)** — `player.GetHero()` lève une
   `AssertionError` (`hero=[(01,ss001b) Kaine Parker]`,
   `player_get.py:203-208`) dès que la traîtrise est révélée alors que le
   joueur est en forme d'identité civile — ce qui est le cas normal à
   l'instant précis de mise en place testé (`test_capacites`), et
   probablement fréquent en partie réelle aussi (une traîtrise se révèle
   sans égard à la forme du joueur). Rouge : `AssertionError` observée au
   premier essai de `ss022 — When Revealed`. Vert : remplacé par une
   lecture directe parmi `player.GetAllIdentityFace()` (les deux faces,
   quelle que soit celle active) filtrée par `Hero.IsType`, puis
   `printed_attack` (la valeur `.attack` effective d'une face INACTIVE
   rend 0 — constaté en jeu réel avant le second correctif) plutôt que
   `.attack`.
3. **Bug moteur réel, DEUX défauts imbriqués, CORRIGÉS le 30/08/2026** —
   interaction « Simultaneous Overkill » : quand l'identité Scarlet Spider
   (Response « This », printée sur ss001a) inflige elle-même un excès de
   dégâts overkill à un sbire marqué par Mark of Kaine (ss012/013/014), le
   moteur appelle `can_health.py:245-261`
   (`first_player.ChooseOrder([sbire, overkill_target], prompt=
   "Simultaneous Overkill")`, où `overkill_target` = le VILLAIN via
   `Worlds.FindVillain`, `can_attack.py:353`) pour choisir l'ordre de
   résolution de deux unités simultanément affectées. **Ce n'est PAS un
   défaut des scripts `ss001a`/`ss012` eux-mêmes** — les deux ability sont
   structurellement identiques à leurs modèles officiels
   (`AfterUnitAttackAndDefeatUnit`, `33032` Marked) et se construisent/
   passent `audit_cartes` sans souci.
   - **Défaut A** (`engine/controller/controller.py:306-309`, fonction
     `ChoiceOne`) : `target_range` (figé au moment où le choix est RENDU
     au joueur/pilote) ne correspondait plus au nombre de cibles
     réellement validées par `all_legal_targets` au moment de VALIDER la
     réponse — écart observé dans les deux sens selon le scénario exact.
     Avant correctif : `AssertionError` répétée **en boucle infinie** (le
     moteur reposait la même question sans jamais avancer — un vrai
     blocage de partie, pas un simple crash). Rouge : reproduit à volonté,
     3 tentatives, même trace à chaque fois (`select_effect.targets=
     [[Goblin]] target_range=(2, 2)`). Vert : le second garde-fou (qui
     plantait aussi sur une réponse **partielle mais non vide**, en plus
     du cas vraiment vide déjà couvert par le garde-fou juste au-dessus)
     retiré — comparer `all_legal_targets` à cet endroit n'est pas fiable,
     c'est justement cette valeur qui change entretemps. Précédent direct
     dans ce même fichier : l'exemption déjà existante pour
     `select_rule.startswith('VillainAnd')`, qui traite déjà le vilain
     mêlé à d'autres cibles comme un cas spécial connu.
   - **Défaut B** (`game/player/model/player_ask.py:169-172`, méthode
     `ChooseOrder`) : une fois le défaut A corrigé, la partie continue
     mais `effect` peut revenir vide côté ability sans que `faces` (les
     unités à ordonner) le soit — l'ancien `assert len(faces) == 0`
     plantait alors net. Rouge : `AssertionError` directe à ce point après
     correctif du défaut A. Vert : repli sur l'ordre d'origine de `faces`
     quand `effect` est vide mais `faces` ne l'est pas (moins bon que
     l'ordre choisi par le joueur, mais correct — aucune des unités à
     traiter n'est perdue).
   - **Preuve par substitution du correctif** (pas du module `ss012`,
     déjà prouvé indépendamment au cas précédent) : les deux correctifs
     retirés → `AssertionError`/boucle infinie reproductible à volonté ;
     correctifs en place → la partie continue normalement, Rhino subit
     bien 1+2=3 dégâts d'excès (preuve que l'interruption de Mark of Kaine
     a réellement augmenté le montant, pas seulement qu'elle a été
     offerte). Cas dédié : `ss012 Mark of Kaine — Hero Interrupt : +2 à
     l'excès quand Scarlet Spider vainc elle-même le sbire marqué
     (régression moteur ChooseOrder/ChoiceOne)`, vert.
   - Non-régression : `tools/test_cards.py` 4588 ok / 0 err après
     correctif (inchangé) ; 8 cas ciblés sur la zone dégâts/exces/mort
     simultanée (dont `ab002` Elsie-Dee, `ok017` Dora Milaje Fragile,
     `55041` The Mangog) relancés individuellement, tous verts — aucune
     régression détectée sur les deux fichiers moteur touchés.
   - **Reste à vérifier en partie réelle** (comme pour tout le reste du
     pack) : une vraie partie humaine dans le navigateur, qu'un agent ne
     peut pas jouer — mais le risque de blocage identifié n'existe plus
     dans le harnais qui reproduit fidèlement le moteur.

Aucun de ces points n'était visible par `test_cards.py` (construction
seule) : le premier (Class manquante) par `verifier_coherence_cartes.py`,
les autres par `test_capacites.py` (la carte étant vraiment JOUÉE) —
confirmation directe de la leçon du guide (§8).

---

### ss001a : Scarlet Spider (face héros)

- [x] Étape 2 : carte de référence : `aoa/genosha/45136.py` (Genoshan
      Mech) et `mut_gen/zero_tolerance/32104.py` (Operation Zero
      Tolerance) pour `AfterUnitAttackAndDefeatUnit('This', Minion,
      has_excess_damage=True)` + `message.target` encore déplaçable à ce
      stade ; `spdr/iron_spiders_sinister_six/31036.py` (Spot) pour
      `Faces.ShuffleAllTo([this], "EncounterDeck", effect)` ;
      `falcon/53035.py` (Winter Soldier) pour le retrait de menace via
      `.SetTarget(Scheme2)`.
- [x] Étape 5 : mots-pièges vérifiés — `After you deal excess damage`
      (`has_excess_damage=True`, pas juste « defeat »), `shuffle it back
      into the encounter deck` (le sbire lui-même, pas une carte
      quelconque), `Max 3 threat per minion` (`min(message.excess_damage,
      3)`, pas un plafond global). Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : HP 11, ATK 2, THW 1, DEF 3, HS 5
      (desc et carte identiques) ; « Max 3 » → `min(exces, 3)`. Résultat :
      conforme.
- [x] Étape 7 : cas `ss001a Scarlet Spider — Extreme Interrogation` :
      Hydra Bomber (01110, officielle) adoucie à 1 PV, Haymaker (01087,
      3 dégâts) joué contre elle → excès 1, sbire remélangé dans le deck
      de rencontre, menace du complot 5→4. Vert du premier coup (après
      correctif du `Puzzle.ChangeForm` — voir note technique en fin de
      fichier).
- [x] Étape 8 : `ss001a` présent dans les 8/8 parties de l'autoplay,
      « Extreme Interrogation » observable dans le journal détaillé
      (partie 1 notamment, Bella Donna vaincue par Scarlet Spider avec
      déferlement).

Carte terminée : OUI

### ss001b : Kaine Parker (face alter-ego)

- [x] Étape 2 : carte de référence : `okoye/okoye/ok001b.py` (Vanguard
      Leader), même couple `Search.PlayerCard(include_discard_pile=True,
      name=...)` + `initiator.GainCard(face, effect)` ; coût « discard 1
      card from your hand » : modèle `CostFunc.Discard("YourHandCards")`
      (`aoa/45014.py`).
- [x] Étape 5 : mots-pièges : `1 copy of Spider-pathy` (recherche par
      `name`, pas par `card_id` précis — les deux exemplaires ss007/ss008
      sont équivalents), `Limit once per round` (`.LimitOncePerRound()`).
      Résultat : conforme.
- [x] Étape 6 : nombres : 1 carte défaussée, 1 carte cherchée. Résultat :
      conforme.
- [x] Étape 7 : cas `ss001b Kaine Parker — Spider Link` : Spider-pathy
      placée dans la défausse en mise en place, l'action l'y trouve et
      l'ajoute en main. Vert du premier coup.
- [x] Étape 8 : `ss001b` (Spider Link) exercé dans 7/8 parties de
      l'autoplay, 0 traceback.

Carte terminée : OUI

### ss002, ss003 : Grim Resolve (2 exemplaires physiques)

- [x] Étape 2 : carte de référence : `47009` Grande Finale (officielle)
      pour `effect.GetPaidResources().GetResourceIconTypes()` ; modèle du
      choix parmi 4 libellés : `determination/dt070.py` (Munitions Cache,
      `initiator.AskChooseOneText`) ; « until the end of the round » :
      `brawn/bw015.py` (Hulk Out, `TemporaryGain(..., Message.
      WhenRoundEnd, ...)`) ; « ready your identity » : `il015.py` (Iron
      Lad's Suit, `Faces.ReadyAll([identite], effect)`).
- [x] Étape 5 : mots-pièges : `Choose a basic power` (choix parmi
      ATK/THW/DEF/REC, pas un pouvoir fixe), `for each different resource`
      (`GetResourceIconTypes`, nombre de TYPES distincts, pas la valeur
      totale payée), `ready your identity` (l'identité, pas la carte
      Grim Resolve elle-même). Résultat : conforme.
- [x] Étape 6 : nombres : +1 par ressource différente (vérifié avec 1
      seul type de ressource payé → +1 exactement). Résultat : conforme.
- [x] Étape 7 : cas `ss002 Grim Resolve` (partagé pour les 2 exemplaires,
      contenu identique) : payé avec Energy (01088, un seul type Y),
      ATK choisi (1er item de la liste) → +1 ATK constaté, identité
      redressée. Vert du premier coup.
- [x] Étape 8 : `ss002`/`ss003` exercés dans 4/8 parties de l'autoplay,
      0 traceback.

Carte terminée : OUI (les 2 exemplaires)

### ss004, ss005, ss006 : Precise Force (3 exemplaires physiques)

- [x] Étape 2 : carte de référence : `determination/dt005.py` (Blast
      Radius) et `iron_lad/il002.py` (Stature) pour
      `initiator.DeclareNumber(0, 3)` + `this.DealDamage(effect.targets,
      value, effect)`.
- [x] Étape 5 : mots-pièges : `up to 3` (`DeclareNumber(0, 3)`, le joueur
      peut infliger 0), `an enemy` (`.SetTarget(Enemy)`, cible unique).
      Résultat : conforme.
- [x] Étape 6 : nombres : borne haute 3. Résultat : conforme.
- [x] Étape 7 : cas `ss004 Precise Force` (partagé pour les 3 exemplaires,
      contenu identique) : **limite du harnais documentée** — le pilote
      générique de `test_capacites` choisit TOUJOURS le premier item
      offert par `AskChooseOneText`/`DeclareNumber`, c'est-à-dire la
      valeur 0 : aucune clé de cas n'existe pour forcer une valeur précise
      parmi plusieurs options offertes séparément (à la différence de
      `cibles`, qui ne force que le CHOIX DE CIBLE au sein d'une seule
      option). Même limite déjà documentée sur `il002` (« pilote décline
      le bonus »). Le cas vérifie donc : la carte est bien jouée
      (retrouvée en défausse) et les dégâts constatés restent dans la
      borne imprimée [0, 3] — preuve structurelle que `DealDamage` est
      bien appelé avec la valeur déclarée, la branche non-nulle restant
      hors de portée du pilote générique. Vert du premier coup.
- [x] Étape 8 : `ss004`/`ss005`/`ss006` exercés (au moins un exemplaire
      joué) dans 4/8 parties de l'autoplay, 0 traceback.

Carte terminée : OUI (les 3 exemplaires ; la valeur exacte « jusqu'à 3 »
n'est prouvée en direct que par la borne, pas par une valeur non-nulle
forcée — limite du harnais, pas du script)

### ss007, ss008 : Spider-pathy (2 exemplaires physiques)

- [x] Étape 2 : carte de référence : `Search.EncounterCard(include_
      discard_pile=False, card_type=Minion)` (recherche le premier sbire
      rencontré en descendant le deck de rencontre) ; `core/
      legions_of_hydra/01180.py` pour `face.PutIntoPlay(player, effect)`,
      qui engage AUTOMATIQUEMENT un Minion avec le joueur
      (`face_on_event.py:169`, commentaire « Will auto engage if this is
      a Minion »).
- [x] Étape 5 : mots-pièges : `the topmost minion` (recherche, pas un nom
      précis), `engaged with you` (auto-engagement natif du moteur, pas
      de code supplémentaire nécessaire), `Draw 1 card`. Résultat :
      conforme.
- [x] Étape 6 : nombres : 1 carte piochée. Résultat : conforme.
- [x] Étape 7 : cas `ss007 Spider-pathy` (partagé pour les 2 exemplaires,
      contenu identique) : après la carte jouée, au moins un sbire est
      trouvé en jeu ET engagé avec le joueur (preuve robuste, ne dépend
      pas d'un `card_id` précis puisque le sbire trouvé dépend du tirage
      du deck de rencontre). Vert du premier coup.
- [x] Étape 8 : `ss007`/`ss008` exercés dans 4/8 parties de l'autoplay,
      0 traceback (dont un sbire mis en jeu observé dans le journal).

Carte terminée : OUI (les 2 exemplaires)

### ss009, ss010 : Unrestrained (2 exemplaires physiques)

- [x] Étape 2 : carte de référence : `wsp/13013.py` (Into the Fray),
      `DealDamage(..., 7, effect, if_this_attack_deal_excess_damage=
      action)` ; `core/spider_man/32008.py` (Steel Fist) pour
      `Faces.GiveStatus(targets, "Stunned"/"Confused", effect)`.
- [x] Étape 5 : mots-pièges : `Deal 7 damage` (montant fixe, pas de
      DeclareNumber), `If the villain takes overkill damage` (condition
      sur `Villain.IsType(cible)`, pas sur n'importe quel ennemi), `stun
      AND confuse` (les deux statuts, pas un choix). Résultat : conforme.
- [x] Étape 6 : nombres : 7 dégâts fixes. Résultat : conforme.
- [x] Étape 7 : cas `ss009 Unrestrained` (partagé pour les 2 exemplaires,
      contenu identique) : 7 dégâts garantis constatés sur Rhino (14 PV,
      ne meurt pas, donc sans excès dans ce cas précis) — preuve du degat
      de base uniquement. **La branche stun/confuse (si le vilain
      subit un excès overkill) n'a pas de cas dédié** : la construire
      exigerait de vaincre le vilain de la partie en cours (fin de
      partie), ce qui rendrait le reste du cas invérifiable ; le code
      (`if_this_attack_deal_excess_damage` + `Villain.IsType`) suit
      exactement le modèle `wsp/13013.py`, déjà éprouvé ailleurs dans le
      dépôt. Vert du premier coup pour la branche testée.
- [x] Étape 8 : `ss009`/`ss010` exercés dans 5/8 parties de l'autoplay,
      0 traceback.

Carte terminée : OUI (les 2 exemplaires ; branche stun/confuse non
couverte par un cas dédié — construction analogue à un modèle déjà
éprouvé, mais pas exercée en direct, faute de scénario permettant de
vaincre le vilain sans clore la partie)

### ss011 : Four Seasons' Room

- [x] Étape 2 : carte de référence : `core/02035.py` (Intimidation) pour
      `player.ChooseAbilities` à 2 branches ; `game/operate/faces.py:447`
      (`Faces.GiveFacedownBoostCards`) pour la carte boost donnée au
      vilain.
- [x] Étape 5 : mots-pièges : `Exhaust Four Seasons' Room` (coût
      `CostFunc.Exhaust("This")`), `draw 1 card` vs `2 instead` (deux
      branches distinctes, pas un bonus cumulatif). Résultat : conforme.
- [x] Étape 6 : nombres : 1 carte piochée (branche par défaut) ou 2
      (branche boost). Résultat : conforme.
- [x] Étape 7 : cas `ss011 Four Seasons' Room` : branche par défaut
      (première option, même convention que `il017`/`ok019` pour un choix
      libre à 2 branches — le pilote générique prend toujours la
      première) : Four Seasons' Room inclinée, main passée de 6 à 7
      cartes. Vert (après correctif de la taille de main attendue : 6,
      pas 5 — la forme de départ est l'identité civile, HS=6, pas la face
      héros HS=5). **La branche « donner une carte boost, piocher 2 » n'a
      pas de cas dédié**, même limite que pour toute carte « Choose : A
      ou B » libre dans ce dépôt (voir `il017`/`ok019`).
- [x] Étape 8 : `ss011` exercé dans 5/8 parties de l'autoplay,
      0 traceback.

Carte terminée : OUI (branche par défaut prouvée ; branche boost non
couverte par un cas dédié, même limite que toutes les obligations/actions
« Choose » à 2 branches libres déjà présentes dans le dépôt)

### ss012, ss013, ss014 : Mark of Kaine (3 exemplaires physiques)

- [x] Étape 2 : carte de référence : `33032` Marked (officielle) pour
      `AbilityFactory.WhenUnitWouldAttackUnit(None, "AttachedMinion",
      marked)` + `message.GainOverKill(effect)` ; `gmw/16045.py` (Follow
      Through) pour `AbilityFactory.WhenUnitAttackDealExcessDamage
      (HeroInterrupt, "You", ...)` + `message.IncreaseDamage(2, effect)`.
- [x] Étape 5 : mots-pièges : `Attach to a minion` (`CanPlayThisUpgradeCard
      (Minion)`), `Attacks against this minion` (n'importe quel
      attaquant, `attacker=None`, pas seulement Scarlet Spider), `When
      Scarlet Spider deals excess damage` (restreint à `"You"`, PAS
      « any attacker »), `to this minion` (`Condition.CheckWhichCard
      ("AttachedMinion", message.target, effect)`, restreint au sbire
      attaché et à aucun autre). Résultat : conforme.
- [x] Étape 6 : nombres : +2 sur l'excès. Résultat : conforme (construction
      seule — voir ci-dessous pour la limite de la preuve en direct).
- [x] Étape 7 : **deux capacités distinctes, preuve inégale** :
      - Capacité 1 (déferlement accordé) : cas `ss012 Mark of Kaine —
        attaques contre le sbire marque gagnent deferlement` : Hydra
        Bomber (01110, ATK 1) adoucie à 1 PV, marquée, puis attaquée par
        Tigra (01051, alliée officielle, PAS l'identité — voir note ci-
        dessous). **Rouge** (retrait du module `WhenUnitWouldAttackUnit`)
        : aucune trace de « gains overkill » dans le journal. **Vert**
        (module remis) : le journal trace explicitement
        `[Tigra] gains overkill ([Mark of Kaine])` au moment exact où
        `message.GainOverKill(effect)` s'exécute — preuve directe et non
        ambiguë (le delta de PV de l'attaquante seul aurait été ambigu :
        le dégât conséquentiel standard du sbire vaincu, ATK 1, se
        confond numériquement avec un déversement d'exces de 1, constaté
        empiriquement en écrivant ce cas).
      - Capacité 2 (+2 à l'excès) : **prouvée en direct** (30/08/2026,
        après correctif du bug moteur « Simultaneous Overkill » documenté
        plus haut). Cas `ss012 Mark of Kaine — Hero Interrupt : +2 à
        l'excès quand Scarlet Spider vainc elle-même le sbire marqué
        (régression moteur ChooseOrder/ChoiceOne)` : 39043 Goblin (HP
        imprimé 1) attaqué directement par l'identité `ss001a`
        (`attacker="This"`, condition `who_deal="You"` de la capacité 2
        bien exercée cette fois). **Rouge** (les deux correctifs moteur
        retirés) : `AssertionError` reproductible à volonté, boucle
        infinie. **Vert** (correctifs en place) : le journal trace
        `Dégâts en excès +2 ([Mark of Kaine])`, puis Rhino subit 3 dégâts
        (1 exces de base + 2 de la capacité) — `degats_min` vérifie ce
        montant explicitement, pas seulement que l'interruption a été
        offerte.
- [x] Étape 8 : `ss012`/`ss013`/`ss014` exercés dans 6/8 parties de
      l'autoplay, 0 traceback — dont au moins une pose observée dans le
      journal détaillé sans planter.

Carte terminée : OUI (les 3 exemplaires ; les deux capacités — déferlement
accordé et +2 à l'excès — prouvées avec substitution rouge/vert directe)

### ss015 : Spider Stealth Suit

- [x] Étape 2 : carte de référence : `okoye/ok016.py` (Royal Protector)
      pour `AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You",
      health=1)` (upgrade sans texte « Attach to... », porté directement
      par l'identité) ; `game/ability/factory/damage.py`
      (`WhenDamageWouldBeDealtTo` + `by_play_card=("YouControl",
      CardFinder(...))`) pour l'augmentation de dégâts d'un événement
      ATTACK joué ; `game/card/face/base/scheme.py:140-143`
      (`Scheme2.RemoveThreatInternal`, qui RELIT `remove_message.value`
      après `.Send()`) pour justifier la mutation directe de ce champ
      dans le second Hero Interrupt.
- [x] Étape 5 : mots-pièges : `+1 hit point` (fixe, pas conditionnel),
      `an [[ATTACK]] or [[THWART]] event` (filtré par trait, pas par nom
      de carte précis), `the damage dealt OR the threat removed` (deux
      branches indépendantes, jamais les deux en même temps sur un même
      événement). Résultat : conforme.
- [x] Étape 6 : nombres : +1 PV, +1 dégât, +1 menace retirée. Résultat :
      conforme.
- [x] Étape 7 : **deux capacités**, preuve inégale :
      - +1 PV fixe : cas `ss015 Spider Stealth Suit — +1 point de vie
        fixe` : identité posée en jeu avec la carte, PV max +1 constaté.
        Vert du premier coup.
      - +1 dégât sur événement ATTACK : cas `ss015 Spider Stealth Suit —
        Hero Interrupt` : Unrestrained (ss009, 7 dégâts fixes, sans
        DeclareNumber donc pleinement déterministe) joué contre Rhino →
        8 dégâts constatés (7+1). Vert du premier coup.
      - +1 menace retirée sur événement THWART : **NON prouvée en
        direct**, faute de temps pour construire un scénario propre (le
        seul candidat trouvé, Chase Them Down 01052, exige lui-même
        « votre héros attaque et vainc un ennemi » comme déclencheur,
        ajoutant une couche de mise en place non résolue dans le temps
        disponible). Le mécanisme lui-même est vérifié par lecture de
        code : `Scheme2.RemoveThreatInternal` relit bien
        `remove_message.value` après résolution des interruptions, donc
        la mutation directe de ce champ (contrairement à `IncreaseDamage`,
        aucune méthode dédiée n'existe sur ce message) a un effet réel,
        pas seulement documentaire.
- [x] Étape 8 : `ss015` exercé dans 5/8 parties de l'autoplay,
      0 traceback.

Carte terminée : OUI (+1 PV et +1 dégât sur ATTACK prouvés en direct ;
+1 menace retirée sur THWART **à vérifier en partie réelle**, aucun outil
du dépôt n'a permis de le déclencher proprement dans le temps disponible)

### ss016 : Stings of Kaine

- [x] Étape 2 : carte de référence : `okoye/ok016.py` (Royal Protector)
      pour le +1 ATK fixe ; `cw/tigra/56005.py` (Sharp Claws) pour
      `AbilityFactory.WhenUnitMakeAttack(HeroInterrupt, "You", ...)
      .SetCostFunc(CostFunc.Exhaust("This"))` ; `drax/19005.py` (Knife
      Leap) pour le couple `message.GainPiercing(effect)` +
      `message.GainOverKill(effect)` sur le même message.
- [x] Étape 5 : mots-pièges : `Scarlet Spider gets +1 ATK` (fixe),
      `When you attack` (`is_basic_attack=None`, couvre l'attaque de base
      ET les événements ATTACK, pas seulement l'un des deux — vérifié via
      Haymaker, un événement), `exhaust Stings of Kaine` (coût), `gains
      piercing AND overkill` (les deux mots-clés, pas un choix).
      Résultat : conforme.
- [x] Étape 6 : nombres : +1 ATK. Résultat : conforme.
- [x] Étape 7 : deux cas :
      - +1 ATK fixe : cas `ss016 Stings of Kaine — +1 ATK fixe` : carte
        posée, ATK effective +1 constatée. Vert du premier coup.
      - Interruption piercing+overkill : cas `ss016 Stings of Kaine —
        Hero Interrupt` : Scarlet Spider attaque Hydra Mercenary (01101,
        3 PV, choisi pour égaler EXACTEMENT l'ATK effective 2+1=3 et
        éviter tout excès — qui, combiné au déferlement accordé ici,
        aurait reproduit le plantage « Simultaneous Overkill » déjà
        rencontré sur `ss012`) → Stings of Kaine inclinée, preuve que
        l'interruption a bien été offerte et payée. Vert.
- [x] Étape 8 : `ss016` exercé dans 5/8 parties de l'autoplay,
      0 traceback.

Carte terminée : OUI

### ss017 : Murderer's Guilt

- [x] Étape 2 : carte de référence : `okoye/ok019.py` (Funeral Rites),
      même structure `AbilityFactory.WhenThisObligationGiveToYou` +
      `YouMayFlipToYourAlterEgoForm` + `player.ChooseAbilities` à 2
      branches.
- [x] Étape 5 : mots-pièges : `Give to the Kaine Parker player`
      (`desc.GiveTo`), `Exhaust Kaine Parker and take 2 damage` (deux
      opérations distinctes dans la même branche), `1 damage for each
      event in your hand` (`Event.IsType`, filtre par TYPE de carte, pas
      par trait), `If less than 3 damage was taken this way` (compare au
      nombre RÉEL de dégâts subis, pas un seuil fixe indépendant de la
      main). Résultat : conforme.
- [x] Étape 6 : nombres : 2 dégâts (branche 1), seuil de 3 (branche 2).
      Résultat : conforme.
- [x] Étape 7 : cas `ss017 Murderer's Guilt` : branche par défaut
      (première option, même convention que `il017`/`ok019`) — Murderer's
      Guilt bien retirée de la partie. Vert du premier coup. **Branche 2
      (dégâts par événement en main) non couverte par un cas dédié**,
      même limite que toute obligation « Choose » libre à 2 branches déjà
      documentée sur `il017`/`ss011`.
- [x] Étape 8 : révélée en mise en place de plusieurs parties de
      l'autoplay (obligation du héros, présente dans 7/8 parties), aucune
      n'a planté.

Carte terminée : OUI (branche par défaut prouvée ; branche « dégâts par
événement » non couverte par un cas dédié, même limite que toute carte
« Choose » à 2 branches libres déjà présente dans le dépôt)

### ss018 : Assassins Guild

- [x] Étape 2 : carte de référence : `core/ultron/01136.py` (Ultron III,
      « Each [[Drone]] minion gets +1 ATK and +1 hit point »), modèle
      exact de `AbilityFactory.GiveKeywordToInPlayWhenApplyThis
      (CardFinder2("ASSASSIN", Enemy), attack=1)`.
- [x] Étape 5 : mots-pièges : `Each [[ASSASSIN]] enemy` (`Enemy` couvre
      sbires ET vilain, pas seulement les sbires), `+1 ATK` (fixe, en
      continu tant que la carte est en jeu). Résultat : conforme.
- [x] Étape 6 : nombres : +1 ATK. Résultat : conforme.
- [x] Étape 7 : cas `ss018 Assassins Guild` : révélée, Harvester (ss020,
      ATK imprimé 2) mis en jeu → ATK effective 3 constatée. Vert du
      premier coup.
- [x] Étape 8 : `ss018` exercée dans 1/8 partie de l'autoplay (obligation
      du set nemesis, révélée dans le tirage), 0 traceback.

Carte terminée : OUI

### ss019 : Bella Donna

- [x] Étape 2 : carte de référence : `mots-cles/plotting.md` +
      `okoye/okoye_nemesis/ok021.py` (Malice) pour
      `AbilityFactory.AfterMinionEngagePlayer("This", "You", ...)` +
      `this.CastTo(Minion).BasicSchemes(effect)` (Plotting) ;
      `core/ultron/01143.py` (Advanced Ultron Drone) pour
      `AbilityFactory.WhenUnitBeDefeated(ForcedInterrupt, "This", ...)`,
      la carte étant encore manipulable à ce point ; `core/
      spider_man_nemesis/01095.py` (Rhino) pour `Search.EncounterCard(...)`
      + `face.Reveal(None, effect)`. ELITE : trait purement déclaratif,
      aucun code (précédent `ok021`, déjà porteur du même trait sans rien
      coder).
- [x] Étape 5 : mots-pièges : `After this minion engages your identity`
      (`AfterMinionEngagePlayer`, pas une attaque), `it schemes`
      (`BasicSchemes`, action SCH de base sans cible explicite),
      `another [[ASSASSIN]] minion` (recherche par trait, la carte
      elle-même n'étant plus en jeu au moment de la recherche puisqu'elle
      vient d'être vaincue), `reveal it` (`Reveal`, pas `PutIntoPlay`).
      Résultat : conforme.
- [x] Étape 6 : nombres : HP 4, SCH 3, ATK 1 (desc conforme). Résultat :
      conforme.
- [x] Étape 7 : deux cas :
      - Plotting : cas `ss019 Bella Donna — Plotting` : menace du complot
        mise à 0, Bella Donna mise en jeu (engagement automatique) →
        3 menaces posées (= SCH imprimé). Vert du premier coup.
      - Forced Interrupt à la défaite : cas `ss019 Bella Donna — Forced
        Interrupt` : deck de rencontre truqué avec Harvester (ss020,
        ASSASSIN), Bella Donna mise en jeu puis tuée (99 dégâts) → Bella
        Donna hors jeu, Harvester en jeu (revelé puis entré en jeu selon
        le pipeline standard de révélation d'un sbire). Vert du premier
        coup.
- [x] Étape 8 : `ss019` exercée dans 1/8 partie de l'autoplay (sbire
      nemesis, tirage), Plotting observé dans le journal détaillé
      (menace posée à l'engagement), 0 traceback.

Carte terminée : OUI

### ss020 : Harvester

- [x] Étape 2 : carte de référence : `core/04027.py` (Crossfire,
      officielle, Quickstrike + « attacks gain piercing » continu) pour
      `AbilityFactory.UnitAttackGainKeyword("This", piercing=True)` ;
      `core/klaw/01118.py` (Sonic Converter) pour
      `AbilityFactory.AfterUnitAttackAndDamageUnit(ForcedResponse,
      "This", "Character", ...)` + `message.attacked`. Quickstrike : mot-
      clé purement déclaratif (`desc.Quickstrike`), aucun code.
- [x] Étape 5 : mots-pièges : `Harvester's attacks gain piercing` (en
      continu, `"This"`, pas seulement sa prochaine attaque), `attacks
      AND damages a character` (`AfterUnitAttackAndDamageUnit`, pas
      `attacks` seul — dégât STRICTEMENT positif requis), `deal 1 damage
      to that character` (`message.attacked`, LE MÊME personnage que
      celui blessé, pas un autre). Résultat : conforme.
- [x] Étape 6 : nombres : HP 5, SCH 2, ATK 2 (desc conforme) ; +1 dégât
      supplémentaire. Résultat : conforme.
- [x] Étape 7 : cas combiné `ss020 Harvester` (les deux capacités
      s'exercent nécessairement ensemble dans un même combat, et se
      distinguent numériquement) : identité rendue Tenace, Harvester
      l'attaque (ATK 2) → 3 dégâts constatés sur l'identité au total
      (2 grâce au perçant qui ignore la Tenace, normalement 0 sans lui,
      +1 de la Réponse Obligatoire, normalement 2 sans elle) : les 3
      valeurs possibles (0, 2, 3) sont mutuellement exclusives et
      identifient sans ambiguïté quelle capacité est active. Vert du
      premier coup pour la combinaison des deux capacités actives (2+1=3).
- [x] Étape 8 : `ss020` exercé dans 1/8 partie de l'autoplay (sbire du
      set nemesis, tirage), 0 traceback.

Carte terminée : OUI

### ss021 : Undead Hand Ninja

- [x] Étape 2 : carte de référence : `lockjaw/lj015.py` (Annihilus,
      fan-made, modèle EXACT) pour `AbilityFactory.WhenUnitWouldBeDefeated
      (ForcedInterrupt, "This", ...)` + `message.SetBeInstead(effect)` +
      `Faces.ShuffleAllTo([this], "EncounterDeck", effect)` ; helper
      `RevealThisCard` (modèle `mut_gen/colossus_nemesis/32029.py`,
      Slammed) pour le Boost « Reveal this card ». Incite 1 : mot-clé
      purement déclaratif (`desc.Incite`), aucun code.
- [x] Étape 5 : mots-pièges : `When this minion would be defeated`
      (`WhenUnitWouldBeDefeated`, AVANT la défaite, pas après),
      `shuffle it back into the encounter deck INSTEAD`
      (`SetBeInstead(effect)`, la défaite n'a jamais lieu). Résultat :
      conforme.
- [x] Étape 6 : nombres : Incite 1 (desc conforme). Résultat : conforme.
- [x] Étape 7 : cas `ss021 Undead Hand Ninja — Forced Interrupt` : mis en
      jeu, 99 dégâts infligés → hors jeu (le nom du sbire) ET présent
      dans le deck de rencontre (remélangé, pas défaussé). Vert du
      premier coup. **Boost « Reveal this card » non couvert par un cas
      dédié** : action purement d'affichage (`RevealThisCard`, déjà
      utilisé par 3+ cartes officielles), aucun effet secondaire distinct
      à observer dans l'état du monde.
- [x] Étape 8 : `ss021` révélable en jeu réel (set nemesis), non observée
      spontanément dans les 8 parties (aléa du tirage).

Carte terminée : OUI (Forced Interrupt prouvé en direct ; Boost non testé
en direct, mécanisme purement déclaratif déjà éprouvé sur 3+ cartes
officielles du dépôt)

### ss022 : Forced Contract

- [x] Étape 2 : carte de référence : `th015` Friendly Fire (fan-made,
      DesignHacker) pour `max(x.attack for x in ...)` ; `core/01154.py`
      (Concussive Blast, officielle) pour le Boost `player.
      GetControlCharacters()` + `DealDamage(units, 1, effect)`. Surge :
      mot-clé purement déclaratif (`desc.Surge`), aucun code.
- [x] Étape 5 : mots-pièges : `The ally with highest ATK` (`player.
      allies.Get()`, PAS tous les personnages amis — Concussive Blast
      sert de modèle pour le Boost seulement, pas pour le « When
      Revealed », qui vise spécifiquement un allié), `equal to Scarlet
      Spider's ATK` (la face Héros précisément, corrigée pour lire
      `printed_attack` — voir bug n°2 plus haut), `If there is no ally in
      play` (branche de repli distincte, pas un cas particulier de la
      première formule), `Each friendly character` (Boost seul —
      identité ET alliés, `GetControlCharacters()`). Résultat : conforme
      (après le correctif du bug n°2).
- [x] Étape 6 : nombres : dégâts = ATK imprimée de Scarlet Spider (2) ;
      2 dégâts si aucun allié ; 1 dégât par personnage ami (Boost).
      Résultat : conforme.
- [x] Étape 7 : deux cas :
      - When Revealed : cas `ss022 Forced Contract — When Revealed` :
        **rouge** (`AssertionError` sur `player.GetHero()`, voir bug n°2),
        **vert** après le correctif (`GetAllIdentityFace` + `Hero.IsType`
        + `printed_attack`) — Tigra (01051, seule alliée en jeu) subit 2
        dégâts (= ATK imprimée de Scarlet Spider). Preuve par
        substitution directe (le bug lui-même EST la preuve rouge,
        rencontré en écrivant le cas).
      - Boost : cas `ss022 Forced Contract — Boost` : Tigra et l'identité
        subissent chacune 1 dégât. Vert du premier coup.
- [x] Étape 8 : `ss022` exercée dans 1/8 partie de l'autoplay
      (trahison du set nemesis, tirage), 0 traceback — confirmant
      indirectement que le correctif du bug n°2 tient en dehors du
      harnais de test aussi.

Carte terminée : OUI

---

## Note technique : `Puzzle.ChangeForm('Scarlet Spider')` ne fonctionne pas

Rencontré en écrivant le tout premier cas (`ss001a`) : `Puzzle.ChangeForm
('Scarlet Spider')` ne change JAMAIS réellement la forme du joueur — aucun
traceback, aucun message d'erreur, juste un silence total (aucune capacité
« Hero Action » n'était jamais jouable ensuite). Cause : le NOM « Scarlet
Spider » est **ambigu** dans la base de 5140 cartes — trois alliés
officiels portent ce même nom (`spiderham/30020`, `silk/52013`,
`madame_web/mw022`). `Puzzle.FindOrCreateFace('Scarlet Spider')` ne
retrouve pas la face héros DÉJÀ en jeu (elle n'est pas "in play" tant que
l'autre face de l'identité est active) et retombe sur `CardFactory.
GenerateCard`, qui résout le nom vers UN DE CES TROIS ALLIÉS au hasard de
l'ordre interne — `Identity.IsType()` est alors faux, et `ChangeForm` ne
fait rien. Passer le `card_id` (`'ss001a'`) au lieu du nom ne suffit PAS
non plus (même échec, y compris un crash direct de `CardFactory.
GenerateCard` sur une carte Identity dupliquée). **Solution retenue** :
`Puzzle.ChangeToFace('Kaine Parker', 'ss001a')` — `ChangeToFace` cherche la
face ACTIVE par nom (« Kaine Parker », sans collision) et bascule
explicitement vers la face de DESTINATION par `card_id`, sans jamais
passer par la recherche ambiguë. Appliqué à tous les cas de ce pack qui
changent de forme.

## Ce que ces blocs ne peuvent pas voir

Aucune partie n'a été jouée par un humain dans le navigateur : la
validation s'arrête à `test_cards`, `verifier_*`, `test_capacites`
(21 cas verts) et `autoplay` (8 parties, 0 traceback, comparable au
témoin `okoye`). Un agent ne peut pas jouer une vraie partie dans
l'interface web — ce point de la gate finale de `PROCESSUS-HEROS.md`
reste **explicitement NON fait**, à réaliser par un humain.

Un point précis à vérifier en priorité lors de cette partie réelle :

1. **`ss015` (Spider Stealth Suit)**, moitié « menace retirée » de
   l'interruption : jouer un événement THWART avec Spider Stealth Suit en
   jeu et vérifier que la menace retirée est bien augmentée de 1 (le
   mécanisme de code repose sur une mutation directe d'un champ non
   documenté comme mutable, `WhenSchemeWouldRemoveThreat.value` — vérifié
   par lecture de code seulement, jamais exercé en direct).

Le point précédemment listé ici — `ss012` (Mark of Kaine) + `ss001a`,
« Scarlet Spider vainc elle-même avec excès un sbire marqué » — était un
vrai bug **moteur** (pas propre à Scarlet Spider), qui bloquait la partie
en boucle infinie. **Corrigé le 30/08/2026** dans deux fichiers moteur
partagés (`engine/controller/controller.py`, `game/player/model/
player_ask.py`), voir le détail au bug n°3 en tête de ce document. Le
scénario exact est maintenant un cas vert de `test_capacites.py`, et
8 autres cas ciblés sur des mécanismes proches (dégâts en excès, mort
simultanée) ont été relancés sans régression. Le risque de blocage
identifié n'existe donc plus dans le harnais qui reproduit fidèlement le
moteur — la vérification navigateur reste utile en confirmation générale,
mais n'est plus la priorité qu'elle était.
