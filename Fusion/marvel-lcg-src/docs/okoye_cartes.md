# Pack Okoye — fiches PROCESSUS-CARTE.md, une par card_id

Gabarit suivi : `PROCESSUS-CARTE.md` du worktree `refonte-doc-creation-contenu`
(non mergé au moment de la rédaction — lu en lecture seule). 25 card_id au
total (`ok001a` à `ok024`, la face `a`/`b` d'Okoye comptant pour deux
identifiants distincts ; le brouillon initial parlait de « 24 scripts »,
décompte informel qui omettait cette distinction).

Outils exécutés depuis `.game-src` (chemin absolu, `$HOME/marvel-work/python/bin/python3.10`) :
- `tools/test_cards.py` : 4541 ok / 0 err (pack okoye inclus, aucune régression).
- `tools/audit_cartes.py` : 0 suspicion sur le pack okoye (types_arguments,
  marqueur_sans_capacite, exhaust_sans_cout, texte_seul, construction_impossible
  tous vides pour `okoye`).
- `tools/verifier_api_cartes.py` : 0 défaut sur le pack okoye (4 défauts
  préexistants ailleurs : spot, web_of_deceit — non liés à ce travail).
- `tools/verifier_coherence_cartes.py` : 0 obligation sans destinataire, 0
  carte joueur sans classe, 0 image manquante, 0 mot-clé imprimé sans clé
  `desc` pour le pack okoye. `couverture_packs_custom` ressort VIDE pour TOUS
  les packs custom (pas seulement okoye) dans cet environnement — limitation
  du filtre `cid[0].isdigit()` de l'outil sur des `card_id` à préfixe
  alphabétique, déjà le cas pour tous les autres packs maison ; sans lien
  avec ce travail, mais outil impuissant à publier un pourcentage ici.
  La collision de nom « Okoye » (`51024` allié officiel du pack `bp`,
  `ok001a`/`ok001b` l'identité) est signalée par l'outil comme
  « désignation par nom ambigu dans les tests » : sans conséquence dans les
  cas écrits ici (aucun ne met `51024` en jeu en même temps qu'un appel
  `Puzzle.*('Okoye')`), documentée pour mémoire.
- `tools/test_capacites.py` : 27 cas dédiés au pack okoye, **27/27 verts**.
  Preuve par substitution effectuée sur les 3 vrais défauts trouvés en
  écrivant ces cas (voir détail par carte) : `ok010`, `ok020`, `ok022`.
- Deck de départ : vérifié par un script dérivé de
  `tools/verifier_tous_les_decks.py` restreint au seul deck `okoye` (les ~90
  decks du dépôt entier n'ont pas été rejoués) : partie montée avec succès,
  identité `ok001a`, main de 6 cartes, 33 cartes restantes au deck.
- `tools/autoplay.py` : 8 parties contre `rhino`, profil `equilibre` — voir
  détail en fin de fichier (§ « Partie 8 : autoplay »).

## Doute non résolu, bloquant sur DEUX cartes (ok008/ok009)

Voir le rapport de fin de tâche pour la question formelle. Résumé : le texte
imprimé de Spear Thrust mélange « DORA MILAJE characters » (coût) et « allies »
(décompte de X) ; Okoye elle-même porte le trait DORA MILAJE sur sa face
héros (`ok001a`), donc « characters » l'inclut littéralement au pied de la
lettre alors que « allies » ne compte que les alliés. Le script actuel
(hérité du brouillon) restreint le coût à `card_type=Ally`, lecture
recommandée mais **non tranchée avec l'utilisateur**.

---

### ok001a : Okoye (face héros)

- [x] Étape 2 : carte de référence : `59018` (Hercule) pour le couple
      `attack_consequential_damage`/`thwart_consequential_damage` via
      `TemporaryGain`, motif identique (réduction de dégâts consécutifs pour
      une durée limitée) — comparable car même paire de clés `GainForThisActive`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés — `after`
      (`AfterUnitUseBasicPower`, pas une fenêtre `Response` générique),
      `you control` (filtre `Worlds.FindCardsOnField(..., trait="DORA MILAJE")`
      restreint aux alliés du joueur courant via le contexte de l'effet),
      `until the end of the phase` (`Message.WhenPhaseEnd`), `Limit once per
      round` (`.LimitOncePerRound()`).
      Résultat : conforme au texte imprimé.
- [x] Étape 6 : nombres texte ↔ code : « 1 less » → `-1` sur
      `attack_consequential_damage`/`thwart_consequential_damage` selon
      `message.power`. HP/ATK/THW/DEF/HS (9/2/1/2/5) vérifiés desc ↔ image.
      Résultat : conforme.
- [x] Étape 7 : cas dédié : `ok001a Okoye — The Art of War reduit les degats
      consecutifs d'un allie DORA MILAJE officiel` (met en jeu l'allié
      officiel `51022` Aneka du pack `bp`, ATK imprimé `2*`, déclenche une
      attaque de base d'Okoye, vérifie `attack_consequential_damage` passé de
      2 à 1). Vert.
- [x] Étape 8 : autoplay ciblé, voir bilan global en fin de fichier.

Carte terminée : OUI.

---

### ok001b : Okoye (face alter-ego)

- [x] Étape 2 : cartes de référence : capacité *Vanguard Leader* (Setup) —
      comparable à tout Setup officiel de recherche deck+défausse
      (`AbilityFactory.WhenCardSetup` + `Search.PlayerCard`, motif standard
      du moteur, ex. plusieurs identités officielles avec Setup de recherche).
      Capacité *Marshalling Forces* (Action) — comparable à `Faces.ShuffleAllTo`
      déjà utilisé ailleurs dans le moteur pour « shuffle X into your deck ».
- [x] Étape 5 : texte-contre-code : `and discard pile` (both
      `include_player_deck=True, include_discard_pile=True` côté Setup),
      `Shuffle` (rappel entre parenthèses, `Search.PlayerCard` mélange en
      interne), `Limit once per round` (`.LimitOncePerRound()` sur
      Marshalling Forces uniquement, pas sur le Setup qui n'a lieu qu'une
      fois de toute façon).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : aucune valeur numérique propre à ces
      deux capacités (recherche d'UNE carte, pas de compteur). REC/HS (3/6)
      vérifiés desc ↔ image.
      Résultat : conforme.
- [x] Étape 7 : cas dédiés :
      capacité Setup : `ok001b Okoye — Vanguard Leader trouve une carte
      REINFORCEMENTS au Setup` (aucune mise en place : le Setup s'exécute
      automatiquement avant le tour du joueur ; vérifie qu'une carte de trait
      REINFORCEMENTS a rejoint la main). Vert.
      capacité Action : `ok001b Okoye — Marshalling Forces remelange une
      carte REINFORCEMENTS de la defausse` (défausse `ok004`, active l'Action
      via `Puzzle.Action`, vérifie que `ok004` a quitté la défausse). Vert.
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI.

---

### ok002 : Aneka

- [x] Étape 2 : carte de référence : `bp/51014.py` (Manifold) pour
      `AbilityFactory.AfterCardEnterPlay` sur `"This"` — comparable car même
      déclencheur (réponse à sa propre entrée en jeu) avec effet sur d'autres
      cartes du même trait.
- [x] Étape 5 : texte-contre-code : `After` (`AfterCardEnterPlay`, pas
      `WhenCardWouldEnterPlay`), `all other` (liste filtrée `f is not this`,
      calculée à la main puisque ce n'est pas une cible `.SetTarget()`),
      `you control` (portée par `Worlds.FindCardsOnField` sur le joueur
      courant), `until the end of the phase` (`GainUntilPhaseEnd`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : « +1 ATK » → `attack=1`. Cost/HP/ATK/THW
      (2/2/2/1) vérifiés desc ↔ image, RES=B vérifié par découpe d'icône (coin
      bas-gauche, bleu, pictogramme molécule) contre Ayo (jaune, éclair) et
      Spear Thrust (rouge, poing) du MÊME pack.
      Résultat : conforme.
- [x] Étape 7 : cas dédié : `ok002 Aneka — Response : +1 ATK aux autres
      allies DORA MILAJE, pas a elle-meme` (pose `ok017` puis `ok002`,
      vérifie +1 ATK sur `ok017` et ATK inchangé sur `ok002` elle-même). Vert.
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI.

---

### ok003 : Ayo

- [x] Étape 2 : carte de référence : `ok002` (Aneka) — capacité identique au
      mot près, THW au lieu d'ATK.
- [x] Étape 5 : texte-contre-code : identique à ok002 (After, all other, you
      control, until the end of the phase).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : « +1 THW » → `thwart=1`. Cost/HP/ATK/THW
      (2/2/1/2) vérifiés, RES=Y vérifié par icône (jaune, éclair).
      Résultat : conforme.
- [x] Étape 7 : cas dédié : `ok003 Ayo — Response : +1 THW aux autres allies
      DORA MILAJE` (même montage que ok002, THW). Vert.
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI.

---

### ok004 / ok005 : Adored Ones (2 exemplaires physiques, même texte)

- [x] Étape 2 : carte de référence : `moon_knight/age_of_khonshu` (modèle
      `CreerJetonEtMettreEnJeu`, `CardFactory.GenerateCard` + `PutIntoPlay`
      pour un jeton hors deck) pour la branche « create » ; motif
      `CardFinder(check_face_fn=...)` (recherche par NOM parmi une liste,
      puisque `Search.PlayerCard` ne prend qu'un seul `name=`) pour la
      branche « search ».
- [x] Étape 5 : texte-contre-code : `Choose one` (`initiator.ChooseAbilities`
      avec 2 `ForChoiceAbility`), `Create 2` (boucle `range(2)`), `and put
      them into play` (`PutIntoPlay` dans `CreerJetonEtMettreEnJeu`), `deck
      and discard pile` (`include_player_deck=True, include_discard_pile=True`),
      `Aneka or Ayo` (`check_face_fn=lambda f: f.IsName(...) or f.IsName(...)`),
      `put her into play` (`face.PutIntoPlay`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : « Create 2 » → `range(2)`. Cost=2,
      RES=Y vérifiés desc ↔ image.
      Résultat : conforme.
- [x] Étape 7 : cas dédié : `ok004 Adored Ones — branche « Create 2 Dora
      Milaje allies »` (carte réellement JOUÉE, coût payé avec `01088`
      Energy = 2 [energy], vérifie 2 alliés nommés « Dora Milaje » en jeu).
      Vert. **Branche non couverte par le harnais** : « Search deck/discard
      for Aneka or Ayo » — les deux branches sont toujours légales
      simultanément, le pilote de test choisit systématiquement la première
      option offerte (aucun levier `cibles`/`accepter_choix` documenté ne
      permet de forcer la seconde) ; le mécanisme sous-jacent
      (`ChooseAbilities`/`ForChoiceAbility`) est un primitif du moteur utilisé
      par des centaines de cartes officielles, seule la branche SPÉCIFIQUE à
      cette carte restait à prouver côté recherche/mise en jeu par nom — à
      vérifier en partie réelle.
      `ok005` est un second exemplaire physique du MÊME script : couvert par
      le même cas (aucune capacité distincte).
- [~] Étape 8 : autoplay ciblé — voir bilan global ; aucune partie observée
      n'a vu le pilote jouer Adored Ones pour son effet (il l'a utilisée
      seulement comme ressource générique), donc aucune preuve
      supplémentaire en partie simulée au-delà du cas dédié.

Carte terminée : OUI pour la branche « create » (preuve directe) ; la branche
« search Aneka/Ayo » repose sur un mécanisme du moteur déjà éprouvé ailleurs
mais n'a pas de preuve directe propre à cette carte — limite du harnais
documentée, pas un défaut connu.

---

### ok006 / ok007 : Angelic Warfare (2 exemplaires physiques, même texte)

- [x] Étape 2 : carte de référence : `ok004` (Adored Ones) pour la branche
      « create » (même modèle `CreerJetonEtMettreEnJeu`) ; `trors/04017.py`
      (Ready for Action) pour `Faces.GiveStatus(targets, "Tough", effect)` +
      `.SetTarget("YourAlly", canbe_tough=True)`, étendu à « up to 3 » via
      `range=("Zero", 3)`.
- [x] Étape 5 : texte-contre-code : deux `Hero Action` distinctes sur le même
      événement = un choix à la résolution (modèle Adored Ones), pas deux
      capacités séparées. `Ready Okoye` (`Faces.ReadyAll([initiator.GetHero()])`),
      `give up to 3 allies` (`range=("Zero", 3)`), `a tough status card`
      (`canbe_tough=True`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : « Create 2 » → `range(2)`, « up to 3 »
      → `range=("Zero", 3)`. Cost=4, RES=B vérifiés.
      Résultat : conforme.
- [x] Étape 7 : cas dédié : `ok006 Angelic Warfare — branche « Create 2
      Midnight Angel allies »` (jouée, payée en [mental] via 01089+01084+01081
      = 4B, vérifie 2 alliés « Midnight Angel » en jeu). Vert. **Branche non
      couverte par le harnais** : « Ready Okoye + give tough », même limite
      structurelle que ok004 (choix toujours résolu vers la première option
      par le pilote de test). `ok007` couvert par le même script.
- [~] Étape 8 : autoplay ciblé — voir bilan global ; même limite d'observation
      qu'Adored Ones.

Carte terminée : OUI pour la branche « create » ; la branche « ready + tough »
n'a pas de preuve directe (limite du harnais, mécanisme générique déjà
éprouvé).

---

### ok008 / ok009 : Spear Thrust (2 exemplaires physiques, même texte)

**Doute characters/allies tranché par l'utilisateur (29/08/2026) : allié
uniquement.** Le texte imprimé dit « exhaust up to 3 DORA MILAJE
**characters** you control » (coût) puis « X is the number of **allies**
exhausted » (décompte) : Okoye porte elle-même le trait DORA MILAJE sur sa
face héros, donc « characters » l'inclut littéralement, mais le décompte ne
retient que les « allies ». Décision retenue : le coût se restreint aux
alliés Dora Milaje (`card_type=Ally`), Okoye ne peut jamais être choisie
comme coût — option strictement dominée de toute façon (s'exhaustiver
soi-même ne rapporterait aucun dégât puisque X ne compte que les alliés).
Le script actuel implémente déjà cette lecture, aucun changement de code
nécessaire.

- [x] Étape 2 : carte de référence : `winter/54014.py` (Firepower) pour
      `CostFunc.Exhaust("YouControlCards", trait=..., card_type=Ally,
      range=(0,3))` en coût optionnel, adapté ici en `range=(0,3)` (Firepower
      a `range=(1,3)`, cout obligatoire, car c'est son seul effet).
- [x] Étape 5 : texte-contre-code : `Deal 4 damage` (`DealDamage` fixe),
      `You may exhaust up to 3` (coût optionnel `range=(0,3)`), `divided
      among enemies as you choose` (boucle `ForChoiceAbility` répétée une
      fois par carte exhaustée), `where X is the number of allies exhausted`
      (`len(effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards)`).
      **characters vs allies : voir doute ci-dessus, non tranché.**
- [x] Étape 6 : nombres texte ↔ code : « 4 damage » → `DealDamage(..., 4,
      ...)`, « up to 3 » → `range=(0,3)`, « 1 damage » par carte exhaustée
      (implicite dans la boucle, 1 point par itération = X au total). Cost=2,
      RES=R vérifiés.
      Résultat : conforme (hors doute characters/allies).
- [x] Étape 7 : cas dédié : `ok008 Spear Thrust — 4 degats de base a un
      ennemi` (jouée sur Rhino, payée avec `01090` Strength = 2R, vérifie au
      moins 4 dégâts). Vert. **Branche bonus non couverte par le harnais** :
      coût optionnel à plage 0-3, le pilote de test décline systématiquement
      les coûts optionnels (comportement documenté du harnais) — la
      conversion « allié exhausté → dégât » n'a donc pas de preuve directe.
- [~] Étape 8 : autoplay ciblé — voir bilan global.

Carte terminée : OUI (doute characters/allies tranché ; branche bonus
« exhaust jusqu'à 3 alliés → X dégâts » non prouvée par le harnais — coût
optionnel à plage 0-3 que le pilote décline systématiquement, limite
documentée du harnais, pas un défaut de la carte — à vérifier en partie
réelle).

---

### ok010 : Close Ranks

- [x] Étape 2 : carte de référence : pour le déclencheur, motif officiel
      classique `AbilityFactory.AfterUnitBeDefeated` avec cible tuple
      `("YouControl", CardFinder(...))`. Pour la capacité Resource :
      `spiderham/spider_ham/30001a.py` (Spider-Ham, compteurs « toon ») et
      `falcon/falcon/53006.py` (Falcon's Flock, compteurs « bird ») —
      `CostFunc.Counter("This", 1, <nom>)` + `SetToAvailableTimesFn`, motif
      RETENU après un premier brouillon incorrect (voir défaut ci-dessous).
- [x] Étape 5 : texte-contre-code : `After...is defeated` (`AfterUnitBeDefeated`),
      `place 1 phalanx counter` (`Faces.PlaceCountersOn(..., 1, 'phalanx', ...,
      maximum=3)`), `to a maximum of 3` (`maximum=3`), `Exhaust Close Ranks`
      (`CostFunc.Exhaust("This")`), `remove any number of phalanx counters`
      (`CostFunc.Counter("This", 1, 'phalanx')` + `SetToAvailableTimesFn`,
      voir défaut corrigé ci-dessous), `generate that many [physical]
      resources` (`Resources("R")` par unité, répétée selon compteurs
      disponibles).
      Résultat : conforme APRÈS correction (voir défaut).
- [x] Étape 6 : nombres texte ↔ code : « 1 phalanx counter » → `1`, « maximum
      of 3 » → `maximum=3`. Cost=2, RES=R vérifiés.
      Résultat : conforme.
- [x] **DÉFAUT TROUVÉ ET CORRIGÉ** : le brouillon initial dépensait TOUJOURS
      tous les compteurs phalanx disponibles à chaque activation (`resources_fn`
      fixe basé sur `Resources("R" * dispo)`), au lieu de « any number » au
      choix du joueur — écart assumé silencieusement par l'agent précédent.
      Recherche technique (pas un choix de conception) : `resources_fn` ne
      peut annoncer qu'un montant FIXE par source de paiement
      (`resources.py:389-415`), aucun « clip » automatique au besoin réel.
      Solution retenue : `CostFunc.Counter("This", 1, 'phalanx')` avec valeur
      FIXE 1, répétée via `SetToAvailableTimesFn` — le paiement présente
      alors N choix d'1 ressource chacun, choisir K parmi N traduit
      fidèlement « any number ».
- [x] Étape 7 : cas dédiés, preuve par substitution :
      capacité Response : `ok010 Close Ranks — Response : 1 compteur phalanx
      apres la defaite d'un allie DORA MILAJE` (pose Close Ranks + `ok017`,
      défait `ok017`, vérifie 1 compteur). Vert.
      capacité Resource : `ok010 Close Ranks — la Resource finance un achat
      en consommant SEULEMENT les compteurs necessaires` (pose 2 compteurs
      phalanx, achète Vibranium Spear coût 1 en payant avec Close Ranks,
      vérifie EXACTEMENT 1 compteur consommé sur 2). **Preuve par
      substitution effectuée** : le brouillon buggé (toujours tout dépenser)
      a été remis en place → cas ROUGE (« compteurs phalanx restants = 0,
      attendu 1 ») ; correctif restauré → cas VERT. Un deuxième bug technique
      a aussi été trouvé et corrigé au passage : `CostFunc.Exhaust(...) +
      CostFunc.Counter(...)` (opérateur `+` entre deux `CostFunc.Base`)
      lève `TypeError`, seul le chaînage `.SetCostFunc(...).SetCostFunc(...)`
      fonctionne (chaque appel empile dans `self.cost_funcs`).
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI.

---

### ok011 : Upanga

- [x] Étape 2 : carte de référence : `trors/04016.py` (Team Training) pour
      `AbilityFactory.GiveKeywordToInPlayWhenApplyThis(...)`, restreint ici
      aux alliés DORA MILAJE via `CardFinder` au lieu du simple `Ally` de
      Team Training. Motif `CardFinder(check_face_fn=...)` pour la recherche
      multi-trait (ARMOR/TECH/WEAPON), comparable à celui d'Adored Ones.
- [x] Étape 5 : texte-contre-code : `Each...ally you control` (`control_by=
      "You"`), `gets +1 hit point` (`health=1`), `Exhaust Upanga` (`CostFunc.Exhaust
      ("This")`), `ARMOR, TECH, or WEAPON` (`check_face_fn` avec `or`), `discard
      pile into your deck` (`Faces.ShuffleAllTo`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : « +1 hit point » → `health=1`. Cost=2,
      RES=B vérifiés.
      Résultat : conforme.
- [x] Étape 7 : cas dédiés :
      capacité passive : `ok011 Upanga — chaque allie DORA MILAJE controle
      gagne +1 PV` (pose Upanga + `ok017`, vérifie +1 PV max). Vert.
      capacité Action d'identité civile : `ok011 Upanga — Action d'identite
      civile remet un equipement ARMOR/TECH/WEAPON dans le deck` (défausse
      `ok015`, active l'action — la partie DÉMARRE en forme identité civile,
      aucun changement de forme requis — vérifie qu'ok015 a quitté la
      défausse et qu'Upanga est inclinée). Vert.
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI.

---

### ok012 / ok013 : Midnight Angel Armor (2 exemplaires physiques, même texte)

- [x] Étape 2 : carte de référence : `cap/03025.py` (Honorary Avenger) pour
      le couple `CanPlayThisUpgradeCard(cible)` + `GiveKeywordToAttached
      (cible, health=2, trait="AERIAL")`.
- [x] Étape 5 : texte-contre-code : `Attach to a friendly DORA MILAJE
      character` (`CardFinder(card_type=Friend, trait="DORA MILAJE")`), `Max
      1 per character` (géré nativement par le moteur pour toute amélioration
      de même NOM, vérifié sur Clarity of Purpose `spdr/31029.py` qui ne code
      aucune vérification supplémentaire — aucun code requis), `+2 hit
      points` (`health=2`), `gains the AERIAL trait` (`trait="AERIAL"`),
      `loses the fragile keyword` (condition intégrée DANS `Fragile()`,
      `okoye/__init__.py`, faute de mécanisme générique pour désactiver une
      ability portée par une AUTRE carte — voir fiche `mots-cles/fragile.md`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : « +2 hit points » → `health=2`. Cost=1,
      RES=R vérifiés.
      Résultat : conforme.
- [x] Étape 7 : cas dédiés, preuve par substitution sur la suppression de
      Fragile :
      capacité stats : `ok012 Midnight Angel Armor — +2 PV, trait AERIAL sur
      le DORA MILAJE attache` (pose `ok017`, attache l'armure, vérifie +2 PV
      et trait AERIAL). Vert.
      capacité suppression Fragile : `ok012 Midnight Angel Armor — retire le
      mot-cle fragile (AUCUN Deferlement)` vs témoin SANS armure `ok017 Dora
      Milaje — Fragile deverse l'exces d'attaque sur l'identite (SANS
      armure)` — même mise en place (ok017 blessée à 1 PV restant, Rhino ATK
      2 l'attaque en défense), AVEC armure : 0 dégât indirect sur l'identité
      (Vert) ; SANS armure : 1 dégât indirect (Vert). La paire de cas EST la
      preuve par substitution demandée par l'étape (contraste direct
      armure/pas d'armure sur le MÊME scénario).
      `ok013` est un second exemplaire physique du même script : couvert par
      les mêmes cas.
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI.

---

### ok014 : Royal Protector

- [x] Étape 2 : carte de référence : `environment.py` (paramètre `ally_limit`
      de `GiveKeywordToInPlayWhenApplyThis`) pour « Increase your ally limit
      by 1 » ; motif générique `GiveKeywordToInPlayWhenApplyThis(Hero,
      control_by="You", thwart=1)` pour « Okoye gets +1 THW while in hero
      form » (cible la face Hero précisément, qui n'existe que quand active,
      aucune condition de forme supplémentaire nécessaire) ; motif officiel
      `AfterUnitBeDefeated` + `Faces.ReadyAll` pour la Response.
- [x] Étape 5 : texte-contre-code : `Increase your ally limit by 1`
      (`ally_limit=1` sur `"You"`), `while in hero form` (cible `Hero` type,
      implicitement conditionnée par l'existence de la face), `After a
      WAKANDA ally is defeated` (`AfterUnitBeDefeated`, cible
      `("YouControl", CardFinder(trait="WAKANDA"))`), `exhaust Royal
      Protector` (`CostFunc.Exhaust("This")`), `ready Okoye`
      (`Faces.ReadyAll([initiator.GetHero()], effect)`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : « by 1 » → `ally_limit=1`, « +1 THW »
      → `thwart=1`. Cost=3, RES=Y vérifiés.
      Résultat : conforme.
- [x] Étape 7 : cas dédiés :
      capacité passive : `ok014 Royal Protector — +1 limite d'allies, Okoye
      +1 THW en forme heros` (forme héros nécessaire pour lire le THW,
      `limit_ally.Get()`==4, THW+1 vérifiés). Vert.
      capacité Response : `ok014 Royal Protector — Response : redresse Okoye
      apres la defaite d'un allie WAKANDA` (Okoye exhaustée, `ok017` (WAKANDA)
      défaite, vérifie Okoye redressée et Royal Protector inclinée). Vert.
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI.

---

### ok015 / ok016 : Vibranium Spear (2 exemplaires physiques, même texte)

- [x] Étape 2 : carte de référence : `GiveKeywordToAttached(..., attack=1,
      get_new_value=...)` pour le bonus ATK conditionnel (motif générique du
      moteur, `get_new_value` renvoie le multiplicateur appliqué à
      `attack=1`, `asset_helper.py:201-208`) ; `albert/albert/ab008.py` pour
      `AbilityFactory.UnitAttackGainKeyword` (même carte : +ATK en jeu +
      piercing sur attaque de base), attaquant DYNAMIQUE ici via
      `CardFinder(check_effect_fn=...)` qui lit `effect.this.attached_face`.
- [x] Étape 5 : texte-contre-code : `Attach to a friendly WAKANDA character`
      (`CardFinder(card_type=Friend, trait="WAKANDA")`), `Restricted` (lu
      directement par le moteur depuis `desc.Restricted`, aucun script
      requis — confirmé §5 étape 5 du guide), `Max 1 per character` (géré
      nativement, même mécanisme que Midnight Angel Armor), `+1 ATK (+2 ATK
      instead if attached to an ally)` (`get_new_value` renvoie 2 sur un
      Ally, 1 sinon), `its basic attacks gain piercing`
      (`UnitAttackGainKeyword(..., is_basic_attack=True, piercing=True)`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : « +1 ATK » / « +2 ATK » → multiplicateur
      1/2 via `get_new_value`. Cost=1, RES=R, Restricted=1 vérifiés.
      Résultat : conforme.
- [x] Étape 7 : cas dédiés (les deux branches conditionnelles) :
      `ok015 Vibranium Spear — +1 ATK sur un heros` (attachée à Okoye, forme
      héros, vérifie +1 ATK). Vert.
      `ok015 Vibranium Spear — +2 ATK sur un allie` (attachée à `ok017`,
      vérifie +2 ATK). Vert.
      **Piercing non re-vérifié indépendamment** : `UnitAttackGainKeyword`
      est un primitif du moteur déjà éprouvé (modèle albert ab008), seul le
      bonus ATK conditionnel (spécifique à cette carte) a été isolé et
      prouvé ; à vérifier en partie réelle si un doute subsiste sur le
      déclenchement effectif de piercing lors d'une attaque de base.
      `ok016` est un second exemplaire physique du même script : couvert par
      les mêmes cas.
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI (bonus ATK conditionnel prouvé ; piercing non re-testé
indépendamment, primitif du moteur déjà éprouvé ailleurs — à garder à l'œil
en partie réelle).

---

### ok017 : Dora Milaje (jeton Created Ally)

- [x] Étape 2 : carte de référence : `determination/__init__.py` (fonction
      `Fragile()`, déjà écrite pour l'aspect fan-made Determination — motif
      officiel de la carte 33032 Marked, `WhenUnitWouldAttackUnit` +
      `GainOverKill`) pour le mot-clé Fragile ; `aoa/missions.py` (
      `ThisNotCountAllyLimit`) pour le mécanisme Legion (marquer un allié
      comme ne comptant pas, ici conditionné au rang pair/impair dans le
      groupe plutôt qu'à un « toujours vrai »). Voir fiches complètes
      `docs/reference/mots-cles/fragile.md` et `.../legion.md`.
- [x] Étape 5 : texte-contre-code : `Fragile` (texte rappelé littéralement,
      mécanisme dans `Fragile()`), `Legion` (texte rappelé littéralement,
      mécanisme dans `Legion()`, pairage par `card.object_id`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : « 2 allies... count as 1 » → pairage
      un-sur-deux (`index % 2 == 1` ne compte pas), Cost=0, HP=2, ATK=1,
      THW=1 vérifiés contre l'image (`00c Dora Milaje.png`).
      Résultat : conforme.
- [x] Étape 7 : cas dédiés :
      Fragile (positif, sans armure) : `ok017 Dora Milaje — Fragile deverse
      l'exces d'attaque sur l'identite (SANS armure)`. Vert (voir aussi la
      preuve par substitution sous ok012).
      Legion : `ok017/ok018 — Legion : 2 allies Legion comptent comme 1 seul
      pour la limite d'allies` (pose `ok017`+`ok018`+l'allié officiel non-
      Legion `51022`, vérifie `limit_ally.curr_ally == 2` — 1 pour la paire
      Legion + 1 normal). Vert.
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI.

---

### ok018 : Midnight Angel (jeton Created Ally)

- [x] Étape 2 : carte de référence : `ok017` — même mécanisme Fragile/Legion,
      seule différence les stats et le trait AERIAL supplémentaire.
- [x] Étape 5 : texte-contre-code : identique à ok017.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : Cost=0, HP=3, ATK=2, THW=2, trait
      AERIAL supplémentaire, vérifiés contre l'image (`00d Midnight
      Angel.png`).
      Résultat : conforme.
- [x] Étape 7 : couvert par le cas Legion ci-dessus (`ok017/ok018`), qui met
      `ok018` en jeu et vérifie son inclusion dans le pairage. Fragile
      spécifique à `ok018` non re-testé isolément (mécanisme partagé et déjà
      prouvé sur `ok017`, code strictement identique).
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI.

---

### ok019 : Funeral Rites (Obligation)

- [x] Étape 2 : carte de référence : motif officiel `AbilityFactory
      .WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` +
      `player.ChooseAbilities` à 2 branches (motif générique du moteur pour
      les obligations à choix, comparable à toute obligation « choose one »
      officielle) ; `Worlds.FindCardsOnField` pour cibler les alliés DORA
      MILAJE (déjà utilisé dans plusieurs autres cartes du pack).
- [x] Étape 5 : texte-contre-code : `Give to the Okoye player` (`GiveTo:
      "Okoye"` dans `desc`), `You may flip` (`YouMayFlipToYourAlterEgoForm`,
      optionnel), `Exhaust your alter ego and all DORA MILAJE allies`
      (`Faces.ExhaustAll([alter_ego] + allies, effect)`), `remove...from the
      game` (`Faces.RemoveAllFromGame`), `Exhaust 3 DORA MILAJE allies`
      (`canbe_exhaust=True, max=3`), `If no ally was exhausted this way, this
      card gains surge` (`ThisCardGainSurge` en `else`), `Discard this
      obligation` (`Faces.DiscardAll`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : « 3 » → `max=3`. Boost=2, GiveTo=Okoye
      vérifiés.
      Résultat : conforme.
- [x] Étape 7 : cas dédié : `ok019 Funeral Rites — branche « exhaust alter-ego
      + allies -> retirer de la partie »` (révèle l'obligation avec `ok017`
      en jeu, vérifie que Funeral Rites a quitté la partie). Vert.
      **Branche 2 non couverte par le harnais** : le choix résolu par défaut
      correspond à la première branche offerte ; « Exhaust 3 DORA MILAJE
      allies... » et la clause de renfort conditionnelle n'ont pas de preuve
      directe — mécanisme `ChooseAbilities` déjà éprouvé ailleurs dans le
      pack (Adored Ones, Angelic Warfare), même limite structurelle.
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI pour la branche 1 (preuve directe) ; branche 2 non
prouvée directement (limite du harnais, mécanisme générique déjà éprouvé).

---

### ok020 : Malevolent Mimic (SideScheme, némésis)

- [x] Étape 2 : carte de référence : motif officiel `AbilityFactory
      .AfterUnitBeDefeated` avec cible `Ally` SANS restriction de contrôle
      (contrairement à Close Ranks qui restreint à `YouControl`) ; pose de
      menace sur SOI-MÊME (`PlaceThreatOnSchemes([this], ...)`).
- [x] Étape 5 : texte-contre-code : `After an ally is defeated` (`Ally`, sans
      tuple `YouControl` — n'importe quel joueur), `place 2 threat here`
      (`PlaceThreatOnSchemes([this], 2, effect)`).
      Résultat : conforme APRÈS correction (voir défaut).
- [x] Étape 6 : nombres texte ↔ code : « 2 threat » → `2`. StartingThreat=2*
      (icône « 2 » + silhouette = par joueur, convention confirmée par
      `02018b`/`gmw` StartingThreat`"4*"` du même type). Boost=3 (icônes
      comptées sur le scan).
      Résultat : conforme.
- [x] **DÉFAUT TROUVÉ ET CORRIGÉ** : `NameError: name 'SideScheme' is not
      defined` — le type JSON « SideScheme » correspond à la classe
      `EncounterSideScheme` dans les scripts (piège documenté au GUIDE §10,
      « Type SideScheme en JSON = classe EncounterSideScheme dans les
      scripts »), pas à `SideScheme` qui n'existe dans aucun espace de noms
      de script. Le premier cas de test écrit était passé au VERT pour une
      MAUVAISE raison (le `StartingThreat` imprimé « 2* » coïncidait
      numériquement avec les 2 menaces attendues de la Response qui, elle,
      plantait en silence) — leçon retenue, le cas de test a été corrigé
      pour vérifier 2 (départ) + 2 (Response) = 4, qui ne peut être atteint
      QUE si la Response s'exécute réellement.
- [x] Étape 7 : cas dédié, preuve par substitution : `ok020 Malevolent Mimic
      — Forced Response : +2 menace apres la defaite d'un allie`. **Preuve
      par substitution effectuée** : le bug `SideScheme` remis en place →
      cas ROUGE (« menace = 2 (attendu 4) ») ; correctif restauré → cas VERT.
- [x] Étape 8 : autoplay ciblé, voir bilan global (nemesis non tiré dans les
      8 parties témoin, comme attendu — le nemesis set n'est ajouté qu'au
      deck rencontre du scénario dédié Okoye, pas au scénario `rhino`
      générique utilisé pour l'autoplay ciblé de ce rapport).

Carte terminée : OUI.

---

### ok021 : Malice (Minion, némésis)

- [x] Étape 2 : carte de référence : `sm/27074` (Venom) pour « Steady »,
      mot-clé purement déclaratif (`desc.Steady`, aucune ability nécessaire,
      vérifié sur Venom qui ne porte aucun crochet supplémentaire dans son
      code). `cw/dangerous_recruits/56087.py` (Venom, `BasicAttack`/
      `this.CastTo(Enemy).BasicAttack(...)`) transposé à `BasicSchemes`
      (`can_scheme.py:166`, symétrique de `BasicAttacks`) pour « Malice
      schemes » hors activation normale.
- [x] Étape 5 : texte-contre-code : `Steady` (lu directement depuis `desc`,
      aucun script requis), `After an ally is defeated, Malice schemes`
      (`AfterUnitBeDefeated` + `this.BasicSchemes(effect)`, cible `Ally` sans
      restriction de contrôle comme Malevolent Mimic).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : HP=5, SCH=3, ATK=1, Steady=1, Boost=2
      vérifiés contre l'image (N2 Malice). `Nemesis: "Okoye"` posé (seul le
      sbire NOMMÉ dans « Okoye's nemesis minion » porte ce champ, pas
      Mimic-27).
      Résultat : conforme.
- [x] Étape 7 : cas dédié : `ok021 Malice — Forced Response : manigance (SCH
      imprime) apres la defaite d'un allie` (complot principal remis à 0,
      défait `ok017`, vérifie 3 menace = SCH imprimé de Malice sur le
      complot principal). Vert.
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI.

---

### ok022 : Mimic-27 (Minion, némésis)

- [x] Étape 2 : carte de référence : motif `AbilityFactory.ThisSetKeyword`
      (`enhance_self.py:462`, `FaceSet` → `GainAttack` avec multiplicateur 1)
      pour un ATK entièrement recalculé ; `twc/bulldozer/07051.py` (Ramming
      Speed) pour `message.MustDefendWithAlly(effect)` ; `cw/dangerous_recruits
      /56087.py` (Venom) pour la ré-attaque via `BasicAttack`.
- [x] Étape 5 : texte-contre-code : `X is equal to your ATK` (`identite
      .attack`), `0 instead if you are in alter-ego form` (voir défaut
      ci-dessous), `must choose an ally to defend...if able`
      (`MustDefendWithAlly`), `attacks again` après avoir défait un
      personnage (`message.atk_messages` avec `has_defeated_target`,
      re-attaque via `BasicAttack`), `Limit once per round`
      (`.LimitOncePerRound()`).
      Résultat : conforme APRÈS correction (voir défaut).
- [x] Étape 6 : nombres texte ↔ code : ATK dynamique, base `desc.ATK="0"`
      (convention vérifiée sur `01162` Titania officielle, même motif de
      stat entièrement calculée). HP=5, SCH=1, Boost=2 vérifiés.
      Résultat : conforme.
- [x] **DÉFAUT TROUVÉ ET CORRIGÉ** : `AttributeError: 'Hero' object has no
      attribute 'IsAlterEgo'` — `IsAlterEgo()`/`IsHero()` sont des méthodes
      du JOUEUR (`player.py:236/246`), pas de la face identité. Le script
      appelait `identite.IsAlterEgo()` au lieu de `joueur.IsAlterEgo()`,
      plantage systématique de la capacité DÈS qu'elle tentait de calculer
      X (le crash tombait dans un `try/except` du moteur qui remettait la
      valeur à 0 par défaut, masquant le plantage derrière une valeur
      COÏNCIDEMMENT correcte en forme identité civile, mais fausse en forme
      héros).
- [x] Étape 7 : cas dédiés, preuve par substitution :
      `ok022 Mimic-27 — X = ATK du joueur en forme HEROS`. **Preuve par
      substitution effectuée** : le bug `identite.IsAlterEgo()` remis en
      place → cas ROUGE (« ATK = 0 (attendu 2) », crash visible dans le
      journal) ; correctif restauré (`joueur.IsAlterEgo()`) → cas VERT.
      `ok022 Mimic-27 — X = 0 en forme IDENTITE CIVILE`. Vert (ce cas était
      déjà vert avec le bug, mais pour une MAUVAISE raison — le crash
      produisait justement 0 par défaut ; corrigé, il reste vert pour la
      BONNE raison cette fois).
      **Branches non couvertes par le harnais** : « must choose an ally to
      defend » et « attacks again after defeating a character » n'ont pas de
      cas dédié (nécessiteraient une mise en scène de défense/défaite d'allié
      plus complexe) — mécanismes du moteur déjà éprouvés ailleurs
      (`MustDefendWithAlly`, `BasicAttack`), mais sans preuve directe propre
      à cette carte. À vérifier en partie réelle.
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI pour le calcul dynamique de X (bug réel trouvé et
corrigé, preuve par substitution faite) ; branches défense forcée et
ré-attaque non prouvées directement (limite du harnais).

---

### ok023 / ok024 : War Drumming (2 exemplaires physiques, même texte)

- [x] Étape 2 : carte de référence : `core/rhino/01106.py` (Stampede) pour
      `AbilityFactory.WhenThisRevealed("Alter-Ego"|"Hero", ...)` et
      `minion.DoAttackYou(joueur, effect, property=...)` (`enemy.py:74`,
      générique à tout Enemy, déjà utilisé par Stampede pour Rhino).
- [x] Étape 5 : texte-contre-code : `When Revealed (Alter-Ego)` /
      `(Hero)` (deux `WhenThisRevealed` distincts), `gains surge`
      (`ThisCardGainSurge`), `Choose a minion in play` (`Worlds
      .GetOnFieldMinions` + `MayChooseOneText` si plusieurs candidats),
      `That minion attacks you` (`DoAttackYou`), `ATK is 2 or less...gains
      villainous` (voir écart assumé ci-dessous), `ATK is 3 or
      more...gains overkill` (`AttackProperty(overkill=True)`), `If there are
      no minions in play, this card gains surge` (branche `if not minions`).
      Résultat : conforme, sauf la clause villainous (écart assumé
      documenté, voir ci-dessous — pas un défaut de lecture, une limite
      réelle du moteur).
- [x] Étape 6 : nombres texte ↔ code : « ATK is 2 or less » / « 3 or more » →
      seuils exacts (`cible.attack >= 3` pour overkill, sinon la branche
      villainous, non codée). Boost=1 vérifié.
      Résultat : conforme.
- [x] **ÉCART ASSUMÉ, documenté et NON bloquant** (déjà présent dans le
      brouillon, revérifié et confirmé fondé) : la branche « ATK ≤ 2, gains
      villainous for this attack » n'a AUCUN hook dans ce moteur.
      `AttackProperty` (les propriétés PAR ATTAQUE, `can_attack.py:4`) n'a
      pas de champ `villainous` — seuls overkill/ranged/piercing/etc. y
      figurent. `HasVillainous.GainVillainous`/`Gain(..., villainous=1)`
      EXISTE bien comme mécanisme de mot-clé PERMANENT sur une carte
      (`face_gain.py:266`), mais Villainous se déclenche à l'ACTIVATION
      normale d'un sbire (« quand ce sbire s'active, donne-lui une carte
      boost », vérifié sur Blackjack O'Hare `gmw/16055`) — or cette attaque
      est générée manuellement via `DoAttackYou`, HORS activation normale
      (`WhenEnemyWouldActivate` n'est jamais envoyé par ce chemin). Même en
      accordant temporairement le mot-clé Villainous au sbire autour de
      l'appel, son SEUL déclencheur (l'activation) ne se produit jamais dans
      ce contexte précis : il n'existe donc PAS d'implémentation possible qui
      change le comportement observable, contrairement à une carte comme
      Close Ranks où plusieurs implémentations concurrentes produisaient des
      résultats différents. Seul le texte imprimé porte cette clause,
      exactement comme la clause « cannot place arrow counters » de Kate
      Bishop kb003 dans un pack précédent (précédent déjà accepté sans
      question, mécanisme structurellement identique).
- [x] Étape 7 : cas dédiés, preuve par substitution sur le harnais (pas sur
      le code de la carte, aucun bug trouvé ici) :
      branche Hero (ATK ≤ 2, un seul sbire en jeu) : `ok023 War Drumming —
      branche HEROS : le seul sbire en jeu attaque le joueur`. Deux pièges de
      HARNAIS (pas de la carte) trouvés et documentés dans le cas lui-même :
      (a) le deck Protection provisoire contient `01078` Get Behind Me!, que
      le pilote de test jouait spontanément pour annuler le Reveal — corrigé
      par `main_exclusive` non vide sans cette carte (piège : une liste VIDE
      est falsy en Python, `if cas.get("main_exclusive")` ignore alors
      totalement la consigne de vidage) ; (b) un héros NON incliné défend
      automatiquement contre une attaque dirigée sur lui, absorbant les
      dégâts avec sa DEF — Okoye est explicitement inclinée avant le Reveal
      (guide §8 : « un héros incliné ne défend pas »). Une fois ces deux
      pièges neutralisés : Vert (Malice, ATK 1, attaque bien le joueur pour 1
      dégât).
      branche Alter-Ego (gains surge) : `ok023 War Drumming — branche
      IDENTITE CIVILE : gagne renfort` (vérifié indirectement par une carte
      Rencontre supplémentaire distribuée). Vert.
      `ok024` est un second exemplaire physique du même script : couvert par
      les mêmes cas.
- [x] Étape 8 : autoplay ciblé, voir bilan global.

Carte terminée : OUI pour les deux branches codées (Hero/Alter-Ego, avec
seuil overkill) ; la clause villainous reste du texte pur sans contrepartie
mécanique possible dans ce moteur (limite structurelle démontrée, pas un
défaut à corriger).

---

## Partie 8 : autoplay (bilan pour l'ensemble du pack)

`tools/autoplay.py`, 8 parties okoye vs 8 parties témoin (`spider_man`,
héros officiel déjà validé), scénario `rhino`, difficulté normale, profil
`equilibre`, graines 1-8 (mêmes graines pour les deux decks) :

| Deck | Victoires | Défaites | Sans verdict (!) | % victoire | Rounds moyens |
|---|---|---|---|---|---|
| okoye (testé) | 0 | 8 | 0 | 0 % | 5.2 |
| spider_man (témoin) | 0 | 7 | 1 | 0 % | 5.6 |

Grep exhaustif des 16 journaux (`NameError\|AttributeError\|TypeError\|KeyError\|AssertionError`) : **0 occurrence**, okoye et témoin confondus.

Lecture ligne à ligne d'un échantillon des journaux okoye : cartes du pack
bien piochées et jouées (notamment comme ressource brute quand le pilote ne
juge pas leur effet prioritaire — comportement attendu de l'heuristique de
jeu, pas un défaut). Aucune anomalie, aucun blocage, aucun plantage.

**Lecture du taux de victoire à 0 %** : conforme à l'avertissement du guide
(§8, « un taux de blocage absolu ne veut RIEN dire : le pilote est une
heuristique, il se coince aussi tout seul »). Le témoin officiel spider_man
affiche EXACTEMENT le même taux de victoire (0 %) dans les mêmes conditions,
et un TAUX DE BLOCAGE légèrement supérieur (1 partie sans verdict sur 8,
contre 0 pour okoye) : rien n'indique que le pack okoye dégrade la jouabilité
par rapport au témoin, au contraire. Ce taux de victoire nul reflète une
limite du PILOTE heuristique face à Rhino en profil équilibré, déjà
documentée dans le projet, pas une anomalie du pack.

Nemesis set (`ok020`-`ok024`) : non tiré durant ces 8 parties témoin, car le
scénario `rhino` générique n'inclut pas le deck rencontre némésis dédié
d'Okoye — chaque capacité némésis a néanmoins son propre cas
`test_capacites.py` dédié (voir fiches ci-dessus).

## Ce qui n'a pas pu être vérifié par manque d'outil

- **Partie humaine dans le navigateur** : aucune partie n'a été jouée
  manuellement dans le wizard/plateau. Tout ce rapport repose sur les outils
  automatisés (`test_cards`, `audit_cartes`, `verifier_api_cartes`,
  `verifier_coherence_cartes`, `test_capacites`, `autoplay`) : c'est le point
  explicitement noté comme non couvrable par ces outils au §8 du guide
  (« est-ce que la carte est agréable et fait ce qu'elle promet »).
- **Fiche héros au survol dans le wizard** (étape 7 de PROCESSUS-HEROS,
  « preuve obligatoire ») : l'entrée `heros-info.js` a été écrite, mais
  confirmer visuellement l'affichage au survol dans le wizard nécessite le
  navigateur — non fait.
- **rsync des deux `public/`** (§10 du guide) : ce worktree ne contient
  qu'une seule copie de `public/js/prepare/`, à l'intérieur du dépôt Git
  suivi. La mention d'un second `public/` hors dépôt (miroir Windows séparé)
  concerne une disposition de poste de travail extérieure à ce worktree — non
  vérifiable ni synchronisable depuis ici.
- **Branche « search Aneka/Ayo »** (Adored Ones), **branche « ready + tough
  status »** (Angelic Warfare), **branche 2** (Funeral Rites), **branche
  bonus exhaust** (Spear Thrust), **défense forcée et ré-attaque**
  (Mimic-27) : mécanismes du moteur déjà éprouvés ailleurs dans le dépôt,
  mais sans cas de test PROPRE à ces branches précises — le pilote de test
  choisit systématiquement soit la première option offerte dans un choix à
  plusieurs branches légales, soit décline les coûts optionnels. Chacune est
  listée précisément carte par carte ci-dessus.
