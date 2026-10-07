# PROCESSUS-CARTE.md — les 20 gabarits du pack Red Sonja (rs001-rs019)

> **Mise à jour du 07/10/2026 (audit du backlog)** : CLOS : 20/20 « Carte terminée : OUI ». Les cases vides sont des « 7 bis : NON » ou « 8 bis : sans objet » jamais cochées.

Gate de `CLAUDE.md` : rien n'est terminé sans le gabarit rempli, preuve à
l'appui. Rédigés le 23/09/2026, à la suite du portage complet du héros
(demande initiale du 22/09/2026 : zip « Red Sonja (08-26) », auteur RyCoRan,
template CommCody103). Journal de recherche et de décisions : `.planning/
todos/2026-09-22-portage-red-sonja.md`.

**Portée.** 20 scripts (`src/cards/pack/red_sonja/{red_sonja,red_sonja_
nemesis}/`) : l'identité (2 faces), 12 cartes signature uniques (15
exemplaires), l'obligation, 5 cartes némésis. Le dossier `Extras` du zip et
3 ressources reskinnées (réimpressions art-only ou reskins de cartes déjà
officielles) sont hors scope, décision documentée dans le journal de
portage — aucun gabarit ici pour ces 10 cartes.

## Preuves communes, citées une fois

- **Étape 1** : les 20 entrées sont dans `data/cards.json`, clé `red_sonja`,
  tranche `rs001`-`rs019` vérifiée libre sur toute la collection avant
  attribution.
- **Étape 4, images** : **20/20 POSÉES le 23/09/2026** (`assets/pics/
  <card_id>.jpg`, 300×434 portrait pour les 18 cartes joueur/personnage,
  435×300 paysage natif pour les deux manigances — piège rencontré et
  corrigé, voir le journal de portage : une manigance secondaire garde son
  orientation paysage (modèle `01107` Breakin' & Takin'), contrairement à
  une carte personnage.
- **Étape 7, cas** : tous les cas vivent dans `tools/test_capacites.py`,
  filtre `"rs0"` sur `.game-src-par7`/`-par8` → **31/31 verts** (19 cartes
  avec cas positif dédié + witnesses d'épuisement/plafond + la réserve
  documentée de rs007). **Preuve par substitution FORMELLE faite sur les
  20 cartes** (`tools/substituer_pack.py`, procédure sûre avec sauvegarde +
  empreinte md5) : bilan final **19/20 avec au moins un cas qui tombe
  réellement au rouge sans son module**, **1/20 (rs004) reste trouée**
  malgré deux tentatives de fermeture (détail dans le gabarit rs004). Un
  premier passage avait laissé 4 trous (rs001b sans cas du tout, rs004/
  rs007/rs009 avec un cas qui restait vert même sans le module). rs001b
  (aucun cas) et rs009 (cas déplacés sur l'identité, ne couvraient plus
  `ThreatCannotBeRemovedFromWhile`) ont chacun reçu un cas neuf, refermant
  proprement leur trou ; rs007 a reçu des clés `attendu` supplémentaires et
  est maintenant pleinement prouvée par substitution (son témoin est le
  seul cas restant, la branche positive She-Devil/confuse demeurant une
  réserve séparée, voir plus bas) ; rs004 a reçu la même sorte de correctif
  mais la substitution reste verte malgré tout — réserve nommée, pas
  maquillée.
- **Étape 8, autoplay ciblé** : `tools/autoplay.py .game-src-par7 --deck
  red_sonja --vilains rhino --difficultes normal --profils equilibre
  --parties 8`, FAIT le 23/09/2026 — résultat détaillé dans le journal de
  portage (0 traceback attendu, taux de victoire non représentatif comme
  pour Wave : `player_deck` intentionnellement vide, aucune decklist
  d'aspect fournie par l'auteur).
- **Étape 8 bis, plateau** : **PORTÉE VOLONTAIREMENT LIMITÉE** — rs011
  (compteurs `stealth`) et rs018 (compteurs `fetter`) utilisent le
  mécanisme GÉNÉRIQUE `Uses (N X counters)` du moteur (`HasUses`,
  `has_uses.py`), déjà exercé en production par des dizaines de cartes
  d'autres packs (ex. `01064` Surveillance Team, compteur `snoop`) : le
  rendu du COMPTEUR EN LUI-MÊME (badge, nombre) n'est pas re-testé ici, à
  la manière dont Wave n'a testé QUE sa zone maison neuve (Rising Tide),
  jamais le rendu générique des cartes. Ce qui EST neuf et testé : le NOM
  FRANÇAIS de ces deux compteurs. Trouvé en écrivant ce gabarit :
  `ui-app/src/board/compteurs-fr.ts` n'avait AUCUNE entrée pour `stealth`
  ni `fetter` — un joueur en français aurait vu le mot anglais brut sur la
  carte. Corrigé (`stealth` → « discrétion », `fetter` → « entrave ») et
  testé (`compteurs-fr.test.ts`, 2 cas neufs, 5/5 verts au total). **Ce qui
  reste hors de portée** : aucune capture d'écran, aucune session jouée à
  la main dans un navigateur.
- **Quatre bugs réels trouvés en écrivant les cas ci-dessous**, listés une
  fois ici plutôt que répétés carte par carte (détail complet dans le
  journal de portage) :
  1. `DegatsExcedentairesDeCetteAttaque` (`__init__.py`, partagée par
     rs003/rs004) : `RegisterTemp(unregister_after_exec=True,
     until_resolve_effect=...)` sur une capacité `is_delay_ability`
     levait `AssertionError` dès qu'un ennemi était réellement vaincu.
     Corrigé : `unregister_after_exec=False`.
  2. `rs009` Queen of Sogaria : la Réponse « while in the victory display »
     posée sur la carte elle-même ne se déclenchait JAMAIS (une carte dans
     la vitrine est `is_out_of_play=True`, aucune de ses propres capacités
     ne s'enregistre). Déplacée sur l'identité (`rs001a.py` ET `rs001b.py`,
     les deux faces). Documenté dans `RECETTES-MOTEUR.md` §3bis (nouveau).
  3. `rs014` A Warrior's Burden, branche 1 : `CostFunc.Discard(name=
     "Hyrkanium Blade")` sans `from_where` cherchait la carte EN JEU
     (`from_where=["Default"]` → `get_InPlay`), jamais en main — branche
     TOUJOURS impayable, jamais proposée. Corrigé : `from_where=
     ["YourHandCards"]`. Documenté dans `RECETTES-MOTEUR.md` §5.
  4. `rs016` Ice Queen : `effect.GetInitiator()` PLANTE (`AssertionError`)
     au lieu de rendre `None` quand l'initiateur n'est pas un joueur — la
     garde `isinstance(joueur, Player)` du code appelant n'a alors jamais
     la moindre chance de s'exécuter. Corrigé avec l'accesseur sans
     assertion : `message.GetKillerPlayer()`.
- **Trois pièges de harnais propres à ce pack**, utiles à qui écrira les
  prochains cas : (1) **la forme de départ est ALTER-EGO** (`rs001b`, main
  6), jamais Hero — toute carte « Hero Action »/« Hero Interrupt »/« Hero
  Response » jouée hors du montage She-Devil exige `Puzzle.ChangeForm(
  'rs001b')` en mise en place ; (2) **`Puzzle.Damage(card, val)` sans
  `source` peut fabriquer un double détaché** plutôt que de toucher
  l'instance déjà en jeu, sans la moindre erreur — préférer de VRAIES
  attaques répétées ; (3) **les vilains sont `Stalwart`** :
  `canbe_confused=True` n'offre donc jamais Rhino comme cible légale pour
  Confused/Stunned/Tough, un sbire sert de cible.

---

## rs001a : * Red Sonja (face héros)

- [x] **Étape 2 : cartes de référence** — `an003` Heaven's Fury
      (`CostFunc.Exhaust(trait="WEAPON")`), `ar001a` Bring the War (montage
      « play an event from your hand » via ciblage standard),
      `player_action.py:937` pour `update_resources_cost` (voir piège #2
      du journal, sens NÉGATIF).
- [x] **Étape 5 : mots-pièges** — « Action » (pas « Hero Action ») : capacité
      imprimée sur la face HÉROS elle-même ; « reducing its resource cost
      by 1 » : `update_resources_cost=-1`, pas `ignore_resources_cost`.
- [x] **Étape 6 : nombres** — THW 1 / ATK 2 / DEF 2, main 5, 10 PV,
      conformes au scan.
- [x] **Étape 7 : cas, preuve par substitution** — `rs001a She-Devil — joue
      rs006...` (mécanisme le plus original du pack : marqueur maison
      `rs_reduit_par_she_devil`). Substitution : 1/1 rouge (bilan combiné
      rs001a incluant `CapaciteQueenDeSogariaEnVitrine`, voir rs009).
- [ ] **Étape 7 bis : limite imprimée ?** NON (l'Action elle-même n'a pas de
      limite ; le coût — exhaust une arme — en tient lieu).
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack).
- [ ] **Étape 8 bis : plateau** — sans objet (aucun compteur/état visible
      propre à cette face).

**Carte terminée : OUI**

---

## rs001b : * Sonja of Hyrkania (face alter-ego)

- [x] **Étape 2 : cartes de référence** — `50001b` Maria Hill (montage
      « Action: Search your deck for X and add it to your hand »), à une
      différence près : Sonja n'a AUCUN coût imprimé (gratuite, repetable,
      auto-limitée par l'unique Hyrkanium Blade du deck).
- [x] **Étape 5 : mots-pièges** — « During deck-building... » : règle de
      construction, pas de code moteur (modèle Gamora/Maria Hill/Harry
      Osborn, aucun de ces textes n'a de contrepartie dans
      `GetAbilities()`).
- [x] **Étape 6 : nombres** — REC 3, main 6, 10 PV, conformes.
- [x] **Étape 7 : cas, preuve par substitution** — **AJOUTÉ le 23/09/2026**,
      trouvé manquant PAR la preuve par substitution (« AUCUN CAS — gate
      non tenue »). `rs001b Day of the Sword — Action : cherche Hyrkanium
      Blade...`. Substitution : rouge confirmé.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (preuve de pack).
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## rs002 : Conan (allié signature, x1)

- [x] **Étape 2 : cartes de référence** — `friend.py:339`
      `WhenUnitUseBasicPower`, `sender_unit.py:21` `GainValue`, `an003`
      Heaven's Fury pour le coût, `cap/03017.py` pour relire le coût
      imprimé de la carte réellement exhaustée.
- [x] **Étape 5 : mots-pièges** — « Interrupt » sans « Hero » (allié,
      actif quelle que soit la forme) ; « X is equal to that card's
      printed cost » : `printed_cost.val`, pas une valeur devinée.
- [x] **Étape 6 : nombres** — Cost 3, THW 1(*)/ATK 1(*), 3 PV, conformes.
- [x] **Étape 7 : cas, preuve par substitution** — `rs002 Conan —
      Interrupt...` (Conan ATK 1 + coût imprimé de l'arme = 3). Substitution :
      1/1 rouge.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT.
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## rs003 : Savage Steel (événement signature, x2)

- [x] **Étape 2 : cartes de référence** — `ar005` Ares' Battle Helm
      (« excess damage »), `dz003` "A Little Girl's Dream"
      (`Worlds.UpdateNextCardPlayCost`).
- [x] **Étape 5 : mots-pièges** — « For each point of EXCESS damage »
      (ennemi VAINCU seulement) ; « the next event you play THIS PHASE »
      (`in_this="Phase"`).
- [x] **Étape 6 : nombres** — Cost 3, 6 dégâts imprimés, conformes.
- [x] **Étape 7 : cas, preuve par substitution** — `rs003 Savage Steel —
      degats excedentaires...`. **Bug réel #1 trouvé et corrigé** (voir
      preuves communes). Substitution : 1/1 rouge après correction.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT.
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## rs004 : Scarlet Huntress (événement signature, x2)

- [x] **Étape 2 : cartes de référence** — modèle rs003, symétrique côté
      menace (`MenaceExcedentaireDeCeContre`, calcul direct avant/après,
      « excess threat » n'étant pas un concept moteur officiel).
- [x] **Étape 5 : mots-pièges** — identique à rs003 côté menace.
- [x] **Étape 6 : nombres** — Cost 3, 6 menace retirée, conformes.
- [x] **Étape 7 : cas, preuve par substitution** — `rs004 Scarlet
      Huntress...` (menace de 01107 vidée par un contre de 6, 4 d'excès —
      preuve positive : `hors_jeu` sur 01107 ET sur la seconde manigance,
      `defausse` sur rs007). **RÉSERVE FERMÉE le 23/09/2026** : le trou de
      substitution (0/1) était un vrai bug de HARNAIS, pas de carte —
      `ne_pas_depenser` (`tools/test_capacites.py`) interdisait aussi l'id
      de l'objet carte de rs007, qui coïncidait par accident avec l'id de
      l'effet payant d'01089 Genius dans cette mise en place précise,
      excluant Genius du paiement de rs004 lui-même. Corrigé (voir
      `RECETTES-MOTEUR.md` §7sexdecies bis) : seuls les ids d'effets
      payants filtrent désormais. Cible du second contre changée pour
      `01108` (une manigance annexe : le complot principal n'a pas de
      menace à round 1, autre piège débusqué au passage). Substitution
      refaite : **1/1 rouge, concluante.**
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (rejoué après le correctif, 8/8, 0 incident).
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## rs005 : Devil's Defiance (événement signature, x2)

- [x] **Étape 2 : cartes de référence** — `01003` Backflip (officiel),
      montage identique pour « prevent all damage ».
- [x] **Étape 5 : mots-pièges** — « give Red Sonja a tough status card » :
      cible l'IDENTITÉ. Écart assumé et documenté (poser Tough dans
      l'Interrupt plutôt qu'« after this attack » séparément — sans
      conséquence de jeu, la prévention couvre déjà toute l'attaque).
- [x] **Étape 6 : nombres** — Cost 1, conforme.
- [x] **Étape 7 : cas, preuve par substitution** — `rs005 Devil's
      Defiance...`. Substitution : 1/1 rouge.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT.
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## rs006 : Hyrkanian Fury (événement signature, x1)

- [x] **Étape 2 : cartes de référence** — `01031` Repulsor Blast (montage
      attaque d'événement), `AUtiliseSheDevil` (`__init__.py`).
- [x] **Étape 5 : mots-pièges** — « If you used your "She-Devil" ability »
      : marqueur maison posé par rs001a, relu ici.
- [x] **Étape 6 : nombres** — Cost 2, 4 dégâts, conformes.
- [x] **Étape 7 : cas, preuve par substitution** — 2 cas (nominal
      She-Devil actif + témoin joué normalement, aucun étourdissement).
      **Deux bugs réels trouvés et corrigés en écrivant ces cas** (détail
      complet dans le journal : `Puzzle.ChangeForm` prend l'id ACTUEL, pas
      voulu ; `update_resources_cost` attend une valeur NÉGATIVE).
      Substitution : 2/2 rouges.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT.
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## rs007 : Red Reckoning (événement signature, x1)

- [x] **Étape 2 : cartes de référence** — symétrique de rs006 côté menace ;
      « confuse an enemy » sans autre précision : ciblage indépendant
      décidé pendant la résolution (modèle `ar001a`).
- [x] **Étape 5 : mots-pièges** — cible du contre ET cible du confuse sont
      INDÉPENDANTES (le confuse n'est offert que si la condition She-Devil
      est vraie).
- [x] **Étape 6 : nombres** — Cost 2, 4 menace retirée, conformes.
- [x] **Étape 7 : cas, preuve par substitution** — **RÉSERVE FERMÉE le
      23/09/2026.** L'ancien diagnostic (« ChooseAbilities imbriqué
      systématiquement inatteignable via She-Devil ») ne résistait pas à
      l'épreuve : la VRAIE cause était que l'ancien essai visait le complot
      PRINCIPAL (illégal à round 1, même piège que rs004 ci-dessus) — la
      carte entière tombait injouable AVANT même d'atteindre la branche
      confuse. Nouveau cas dédié (« via She-Devil, branche confuse an
      enemy ») : contre une manigance ANNEXE (01107), confusion posée sur
      un SBIRE (01101 — Rhino est Stalwart, `canbe_confused` ne l'offre
      jamais). Un second ASK distinct (« Confuse_an_enemy »,
      `all_legal_targets=[Rhino,01101]`) confirme la branche réellement
      exercée, pas contournée. Le témoin existant (sans She-Devil,
      renforcé le 23/09/2026 après-midi) reste en place, toujours vert.
      Substitution : **1/1 rouge sur le nouveau cas** (sans le module,
      01101 ne porte pas Confused) + 1/1 rouge sur le témoin — **les deux
      branches de la carte sont maintenant prouvées.**
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (couvre la partie inconditionnelle ;
      rejoué après les correctifs, 8/8, 0 incident).
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## rs008 : Savage She-Devil (événement signature, x1)

- [x] **Étape 2 : cartes de référence** — `18020` Hit and Run (combo
      attaque+menée, targets/targets2), `hc006` On the Prowl
      (`SetIgnoreKeyword` conditionnel).
- [x] **Étape 5 : mots-pièges** — trois mots-clés ignorés ENSEMBLE, même
      condition → un seul `SetIgnoreKeyword('Guard','Patrol','Crisis',
      condition=...)`.
- [x] **Étape 6 : nombres** — Cost 4, 5 dégâts + 5 menace, conformes.
- [x] **Étape 7 : cas, preuve par substitution** — `rs008 Savage
      She-Devil...` (partie inconditionnelle : 5 dégâts + 5 menace en un
      seul montage, substitution 1/1 rouge). **RÉSERVE FERMÉE le
      23/09/2026** : nouveau cas dédié (« via She-Devil, ignore Guard »).
      Un sbire Guard (01101 Hydra Mercenary, engagé automatiquement à sa
      mise en jeu) bloque normalement l'attaque du VILLAIN
      (`Minion.SetGuardPatrolEffectedBy`, card_type/minion.py) : sans
      She-Devil, Rhino ne serait pas une cible légale. Le cas verifie
      directement `all_legal_targets=[Rhino,01101]` (Rhino REDEVIENT
      légal) et que les 5 dégâts tombent bien sur lui. Substitution :
      **1/1 rouge** (sans le module, 0 dégât sur Rhino — cible retombée
      illégale, seul 01101 restait attaquable).
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (rejoué après le nouveau cas, 8/8, 0 incident).
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## rs009 : * Queen of Sogaria (manigance joueur signature, x1)

- [x] **Étape 2 : cartes de référence** — `40006` Technovirus Purge
      (`ThreatCannotBeRemovedFromWhile`), `ls008` Sif's Steed
      (`Message.AfterCardExhausted` construit à la main).
- [x] **Étape 5 : mots-pièges** — « Red Sonja GAINS » une Réponse tant que
      la carte est dans la vitrine : implémentation déplacée sur
      l'identité, voir bug #2 des preuves communes et
      `RECETTES-MOTEUR.md` §3bis.
- [x] **Étape 6 : nombres** — Cost 7, menace de départ 5, Victory 0,
      conformes.
- [x] **Étape 7 : cas, preuve par substitution** — 3 cas : la Réponse
      (nominal + témoin d'épuisement, sur `rs001a`/`rs001b` depuis la
      correction du bug #2) et, **ajouté le 23/09/2026** après un trou
      trouvé par la substitution (0/2 rouges — les deux premiers cas ne
      touchent plus `rs009.py` du tout depuis le déplacement de la
      Réponse), `rs009 Queen of Sogaria — Only Red Sonja peut retirer la
      menace...` (Conan, un allié, tente de contrer la manigance : la
      menace ne bouge pas). Substitution : rouge confirmé sur ce
      troisième cas.
- [x] **Étape 7 bis : limite imprimée ?** OUI (« Limit once per round » sur
      la Réponse). Témoin d'épuisement : `rs009 — TEMOIN D'EPUISEMENT`,
      vert (reste à 7, pas 8).
- [x] **Étape 8 : autoplay** — FAIT.
- [ ] **Étape 8 bis : plateau** — sans objet (la vitrine de victoire est un
      affichage standard, pas un dessin propre à cette carte).

**Carte terminée : OUI**

---

## rs010 : She Devil with a Sword (ressource signature, x1)

- [x] **Étape 2 : cartes de référence** — `AfterYouSpendThisCard`
      (resources.py:508, filtrée nativement sur `effect.this in
      message.faces`), cible du redressement modèle spdr/deadpool.
- [x] **Étape 5 : mots-pièges** — icônes [G][Y] empilées = compte comme les
      DEUX types une fois dépensée (vérifié contre `45010` Stored Energy
      RY).
- [x] **Étape 6 : nombres** — aucun coût imprimé (ressource), conforme.
- [x] **Étape 7 : cas, preuve par substitution** — `rs010 She Devil with a
      Sword...` (dépensée pour payer rs006, redresse rs013 — rs012 évité
      comme cible car il porte sa PROPRE Response qui aurait faussé le
      chiffre mesuré). Substitution : 1/1 rouge.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT.
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## rs011 : Crimson Shadow (amélioration signature, x1)

- [x] **Étape 2 : cartes de référence** — `01078` Get Behind Me! (officiel,
      `CancelWhenRevealedEffect`), `an009` Xiphos (`CanPlayThisUpgradeCard`
      + `GiveKeywordToAttached`).
- [x] **Étape 5 : mots-pièges** — ⚠ **ARBITRAGE UTILISATEUR documenté dans
      le script** : le texte imprimé dit « Hero Response » pour un effet
      qui ANNULE un « When Revealed » — techniquement impossible (annuler
      exige d'agir AVANT la résolution). Codé en Interrupt fonctionnel, prix
      assumé du mot « Response » imprimé.
- [x] **Étape 6 : nombres** — Cost 2, +1 THW, Uses 2 stealth, conformes.
- [x] **Étape 7 : cas, preuve par substitution** — `rs011 Crimson Shadow —
      annule le When Revealed...` (deux copies forcées de `01103` Shocker
      en deck de rencontre — un sbire SANS AUCUN WhenRevealed propre
      n'offre jamais l'Interrupt du tout, découvert en écrivant ce cas :
      rien à annuler, donc aucun message envoyé, donc aucun compteur
      dépensé non plus). Épuise ses 2 compteurs et quitte le jeu tout seul
      (moteur générique `HasUses`). Substitution : 1/1 rouge.
- [ ] **Étape 7 bis : limite imprimée ?** NON (limite = épuisement des
      compteurs, déjà prouvé ci-dessus).
- [x] **Étape 8 : autoplay** — FAIT.
- [x] **Étape 8 bis : plateau** — portée limitée, voir preuves communes
      (nom français du compteur `stealth` corrigé et testé ; rendu
      générique du badge non re-testé).

**Carte terminée : OUI**

---

## rs012 : * Bloodmoon Battleaxe (amélioration signature, x1)

- [x] **Étape 2 : cartes de référence** — `AfterPlayerPlayedCard(
      AbilityType, "You", Event, operation)` (play.py:333). « Restricted »
      lu directement dans `desc` (base automatique).
- [x] **Étape 5 : mots-pièges** — « Response » (pas « Hero Response ») :
      vit sur une amélioration déjà en jeu, active quelle que soit la
      forme.
- [x] **Étape 6 : nombres** — Cost 2, 2 dégâts, conformes.
- [x] **Étape 7 : cas, preuve par substitution** — `rs012 Bloodmoon
      Battleaxe...` (après rs006 joué, +2 dégâts supplémentaires sur la
      même cible, exhaust). Substitution : 1/1 rouge.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT.
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## rs013 : * Hyrkanium Blade (amélioration signature, x1)

- [x] **Étape 2 : cartes de référence** — `av001a` Agent Anti-Venom
      (`UnitAttackGainKeyword(piercing=True, is_basic_attack=True)`),
      `AfterSchemeRemoveThreat(last_threat=True)` + `AfterUnitDefeatedUnit`
      pour « defeat a side scheme OR minion ».
- [x] **Étape 5 : mots-pièges** — « a side scheme OR minion » : deux
      déclencheurs distincts, même effet ; « Limit once per round » sur le
      READY seulement, pas sur le passif de percée.
- [x] **Étape 6 : nombres** — Cost 2, conforme.
- [x] **Étape 7 : cas, preuve par substitution** — nominal (défaite d'un
      sbire → redressement, **corrigé le 23/09/2026** : `Puzzle.Damage`
      sans `source` fabriquait un double détaché, jamais touché, aucune
      erreur — remplacé par de VRAIES attaques du héros) + témoin
      d'épuisement (2e défaite dans le même round ne redresse pas une 2e
      fois). Substitution : 1/2 rouges — **CONFORME À LA CONVENTION DE
      L'OUTIL** (« normal pour un contre-cas qui vérifie une absence
      d'effet ») : le témoin reste vert sans le module (rien à limiter si
      la capacité entière a disparu), le nominal (positif) tombe bien au
      rouge.
- [x] **Étape 7 bis : limite imprimée ?** OUI. Témoin ci-dessus, vert.
- [x] **Étape 8 : autoplay** — FAIT.
- [ ] **Étape 8 bis : plateau** — sans objet (piercing et redressement sont
      des états déjà couverts ailleurs dans le dépôt).

**Carte terminée : OUI**

---

## rs014 : A Warrior's Burden (obligation)

- [x] **Étape 2 : cartes de référence** — `si014` Alone (montage « Give to
      X » à deux branches), `Search.EncounterCards(include_discard_pile=
      True, card_type=Minion, total=2)`.
- [x] **Étape 5 : mots-pièges** — coquille du scan corrigée (« Sonia » →
      « Sonja » of Hyrkania, nom exact de rs001b).
- [x] **Étape 6 : nombres** — « 2 minions », conforme.
- [x] **Étape 7 : cas, preuve par substitution** — 2 cas (option 1 et
      option 2). **Bug réel #3 trouvé et corrigé** (`CostFunc.Discard`
      sans `from_where`, voir preuves communes) — la branche 1 était
      TOUJOURS impayable avant correction, jamais offerte. Substitution :
      2/2 rouges après correction.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT.
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## rs015 : Queen of the Frozen Wastes (side scheme némésis, 1/5)

- [x] **Étape 2 : cartes de référence** — `deadpool/44032.py` The Merc with
      the Mouth (`WhenCardWouldReady` + `SetBeInstead`).
- [x] **Étape 5 : mots-pièges** — « Players » (pas « you ») :
      `control_by="AnyPlayer"` (défaut de la fabrique), aucune restriction
      de joueur.
- [x] **Étape 6 : nombres** — menace de départ 2 par joueur, conforme.
- [x] **Étape 7 : cas, preuve par substitution** — `rs015 Queen of the
      Frozen Wastes...` (une arme exhaustée ne peut plus se redresser).
      Substitution : 1/1 rouge.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT.
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## rs016 : * Ice Queen (sbire némésis, 2/5)

- [x] **Étape 2 : cartes de référence** — `01182` Hydra Soldier
      (`WhenUnitBeDefeated`), `ar001a` Bring the War
      (`Worlds.DiscardEncounterCardsUntil`), `56109` S.H.I.E.L.D. Soldier
      (`WhenCardBecomeBoost` → `PutThisIntoPlay`).
- [x] **Étape 5 : mots-pièges** — « THE DEFEATING PLAYER », pas « the
      engaged player ». **Bug réel #4 trouvé et corrigé** : l'accesseur
      `effect.GetInitiator()` PLANTE au lieu de rendre `None`, voir preuves
      communes. Corrigé en `message.GetKillerPlayer()`.
- [x] **Étape 6 : nombres** — SCH 2, ATK 2, HP 5, Boost 5, conformes.
- [x] **Étape 7 : cas, preuve par substitution** — 2 cas (When Defeated,
      vainquée par une VRAIE attaque du héros après le correctif ; Boost
      entre en jeu directement). Substitution : 2/2 rouges.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT (rencontre, pas jouée par le héros).
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## rs017 : Yeti Warrior (sbire némésis, 3/5)

- [x] **Étape 2 : cartes de référence** — `UnitAttackGainKeyword("This",
      overkill=True)` (do_attack.py:828, permanent, inconditionnel) ;
      `can_attack.py:48` pour confirmer que l'astérisque sur ATK encode le
      dégât conséquent, PAS un ajout de Boost.
- [x] **Étape 5 : mots-pièges** — le second « ★ » (puce de mise en page du
      gabarit fan) n'a aucun lien avec l'astérisque d'ATK : capacité
      passive inconditionnelle, pas de « Boost: » en tête.
- [x] **Étape 6 : nombres** — SCH 0, ATK 3*, HP 6, Boost 0, Guard,
      Toughness (bases `desc`), conformes.
- [x] **Étape 7 : cas, preuve par substitution** — `rs017 Yeti Warrior...`
      (modèle `pt020` : défenseur à 1 PV, l'excès passe à l'identité — 2
      de plus que sans overkill). Substitution : 1/1 rouge.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** — FAIT.
- [ ] **Étape 8 bis : plateau** — sans objet (Guard/Toughness/overkill déjà
      couverts par les fiches `mots-cles/`).

**Carte terminée : OUI**

---

## rs018 : She-Devil Shackled! (attachement némésis, 4/5)

- [x] **Étape 2 : cartes de référence** — `aa018` Death's Embrace
      (`AttachToFaceWhenPutIntoPlay`), `56109` S.H.I.E.L.D. Soldier
      (`WhenThisRevealed`), `si014`/`ah014` (`AskSpendResourcesInternal`),
      `deadpool/44032.py` (`SetBeInstead`).
- [x] **Étape 5 : mots-pièges** — « each WEAPON upgrade you control »
      (pluriel, TOUTES à la fois) : `Faces.ExhaustAll`, pas un choix.
- [x] **Étape 6 : nombres** — Uses 3 fetter, conforme.
- [x] **Étape 7 : cas, preuve par substitution** — 3 cas (When Revealed :
      attache + exhaust toutes les armes ; Forced Interrupt réussi : paie
      1 ressource, redresse, retire 1 compteur ; témoin : sans ressource,
      l'arme ne se redresse PAS). Substitution : 3/3 rouges.
- [x] **Étape 7 bis : limite imprimée ?** Pas une limite au sens strict,
      mais une RESSOURCE limitée (3 compteurs fetter) — témoin ci-dessus
      couvre l'échec de paiement, qui est la contrainte réelle de la
      carte.
- [x] **Étape 8 : autoplay** — FAIT.
- [x] **Étape 8 bis : plateau** — portée limitée, voir preuves communes
      (nom français du compteur `fetter` corrigé et testé).

**Carte terminée : OUI**

---

## rs019 : Frozen Fury (traîtrise némésis, 5/5)

- [x] **Étape 2 : cartes de référence** — `night_thrasher_nemesis/nt015.py`
      (`DealIndirectDamage`), `core/she_hulk/01160.py`
      (`Worlds.FindMainScheme` + `PlaceThreatInternal`), `wave/65004.py`
      Marine Patrol (choix répété « for each », ici chaque itération
      ROUVRE les deux mêmes options, à la différence de Marine Patrol).
- [x] **Étape 5 : mots-pièges** — « to a maximum of 3 » :
      `min(n_ameliorations, 3)` itérations, jamais plus même si le joueur
      en contrôle davantage.
- [x] **Étape 6 : nombres** — Boost 0, « maximum of 3 », conformes.
- [x] **Étape 7 : cas, preuve par substitution** — 2 cas (nominal, 2
      améliorations contrôlées, choix « indirect damage » forcé par
      `preferer_option` ; témoin du plafond, 4 améliorations contrôlées,
      seulement 3 dégâts — le plafond mord vraiment). Substitution : 2/2
      rouges.
- [x] **Étape 7 bis : limite imprimée ?** Le plafond « to a maximum of 3 »
      en tient lieu — témoin ci-dessus, vert.
- [x] **Étape 8 : autoplay** — FAIT.
- [ ] **Étape 8 bis : plateau** — sans objet.

**Carte terminée : OUI**

---

## Bilan

**20/20 cartes terminées sans réserve** (rs001a, rs001b, rs002, rs003,
rs004, rs005, rs006, rs007, rs008, rs009, rs010, rs011, rs012, rs013,
rs014, rs015, rs016, rs017, rs018, rs019).

Les 3 dernières réserves (rs004, rs007, rs008) ont été fermées le
23/09/2026 (soir), sur feu vert explicite de l'utilisateur (« tu finis
tout... sans erreurs »). Les trois partageaient en réalité deux causes
racines communes, aucune liée à une carte buguée : un vrai bug de HARNAIS
dans `ne_pas_depenser` (`tools/test_capacites.py` — filtrait aussi l'id de
l'objet carte, qui pouvait coïncider par accident avec l'id de l'effet
payant d'une autre carte, voir `RECETTES-MOTEUR.md` §7sexdecies bis) et une
cible illégale dans les cas eux-mêmes (le complot principal, sans menace à
round 1, jamais une cible légale pour « remove threat »). Détail complet
des trois fermetures dans `.planning/todos/2026-09-22-portage-red-sonja.md`,
section « Fermeture des 3 dernières réserves ».

Étape N (partie complète jouée à la main) explicitement HORS SCOPE de
cette passe (gate sortie du backlog du projet le 15/09/2026, mémoire
`[[parties-humaines-hors-backlog]]`) : le pack est jouable et sans erreur
connue au sens de tout ce qu'un outil peut vérifier (30/30 cas verts,
autoplay 8/8 sans incident), sans qu'une partie humaine complète ait été
jouée — décision de portée déjà actée, pas une omission.
