# PROCESSUS-CARTE.md : les 17 gabarits du pack BLADE (set 165, `bl`)

> **Mise à jour du 07/10/2026 (audit du backlog)** : CLOS : 17 gabarits « OUI ». L'unique case vide est la partie jouée à la main, sortie du backlog le 15/09.

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
07/09/2026 (soir). Auteur du pack : **Rainy**, zip « Blade » (dossier
`A créer`), 26 scans pour 17 card_id (15 cartes héros, 1 obligation, set
némésis de 8 cartes).

⚠ **Aucun aspect n'a été arbitré, et c'est voulu** (consigne du 06/09/2026) :
`player_deck` vide, le zip ne fournit aucune decklist.

**Un arbitrage utilisateur, posé AVANT d'écrire (étape 3)** :

| Question | Réponse du 07/09/2026 |
|---|---|
| « Attacks with piercing deal double damage » (tout le set némésis) contre les bonus de Blade's Sword et du Bandolier : dans quel ordre ? | **Bonus puis doublement** : Go for the Heart 4 + épée 1 = 5, doublé = 10 (et non 9). |

C'est aussi l'ordre naturel du moteur : les bonus passent par
`DealAdditionalDamage` (messages `WhenUnitWouldAttack` puis
`WhenUnitMakeKeyWordAttack`), le doublement par
`WhenRecalculateAttackDamage`, envoyé après (`can_attack.py:374`). Le cas
« bl003 + bl008 + bl013 » mesure **10**.

**Preuves communes**, citées une fois :

- **Étape 1** : pack `blade` en queue de `cards.json` (18 entrées, deux faces
  d'identité), set `165. Custom (Blade)` dans `sets_info.json`, préfixe `bl`
  déclaré, `verifier_prefixes` OK, checksums recalculés.
- **Étape 3 (héros)** : `deck/starter/blade.json`, 15 exemplaires signature
  (9 card_id), obligation `bl011`, set némésis `bl012`-`bl017` (**8 cartes** :
  Vampire x2, Embraced x2), `player_deck` vide.
- **Étape 4, images** : `assets/pics/bl0*.jpg` pour les 17, copiées par
  `tools/importer_images_blade.py` (⚠ `0.2 Blade.jpg` = HÉROS, `0.1 Eric
  Brooks.jpg` = ALTER-EGO, vérifié sur le libellé imprimé).
- **Icônes de ressource** : vérifiées par la couleur du coin contre les
  références `sf002` (Y), `sf006` (B), `sf008` (R), `ar007` (G) : Gear Up **G**,
  Go for the Heart **R**, On the Hunt **B**, Vampire Bite **R**, Vampiric
  Reflexes **Y**, Bandolier **R**, Blade's Sword **R**, Daywalker **Y**,
  Predatory Instincts **B**.
- **Mots-clés** : fiches lues avant d'écrire : `uses`, `teamwork`, `traitor`,
  `surge`, `piercing`, `retaliate`, `restricted`, `seek`. Aucune fiche créée :
  rien de nouveau. Robustesse et Étourdi sont des STATUTS, pas des mots-clés
  (README des fiches).
- **Compteurs** : `'blood'` et `'thirst'` **AJOUTÉS à l'énumération `COUNTER`**
  (`card_face.py:194`, commentaire CORRECTIF daté) ; `'stake'` existait
  (Mojo `39048`). Sans eux, `HasUses` refuse la carte à la construction
  (fiche uses.md).
- `test_cards` : **5353 ok / 0 erreur** (5335 avant, soit **+18**).
- `verifier_desc_mots_cles blade` / `verifier_noms_modules` /
  `verifier_appels_modules blade` / `verifier_cartes_en_jeu blade` : **OK**.
- **Étape 7, cas** : 51 cas `bl0` : table et bilan en fin de fichier.
- **Étape 7 (héros)** : biographie `bl001a` dans `heros-info.js`
  (`node --check` OK), fiche VUE au survol dans l'onglet FAN-MADE de
  l'assistant local (capture du 07/09, 22:36 : bio, Eric Brooks, Londres /
  New York, Vengeurs / Nightstalkers / MI-13, Dracula / Deacon Frost /
  Morbius, The Tomb of Dracula #10 (1973)).
- **Étape 8 (héros)** : 17 textes français dans `textes-fr-fanmade.ts`
  (`tsc --noEmit` OK).
- **Étape 10** : signatures étrangères : **0 sur 127 decks**.

---

## PORTÉE : UN FICHIER MOTEUR PARTAGÉ TOUCHÉ, DE FAÇON ADDITIVE

`src/game/card/face/card_face.py` : deux noms de compteur ajoutés à l'énum
`COUNTER` (`'blood'`, `'thirst'`), même geste que les CORRECTIF précédents
(`flame`, `flare`, `unworthy`...). Purement additif : aucun nom existant ne
change, aucune carte livrée ne lit ces noms.

Rien d'autre hors de `src/cards/pack/blade/`. Aucune fabrique nouvelle,
aucun trait nouveau (VAMPIRE, ITEM, WEAPON, TACTIC, ATTACK, THWART, DEFENSE,
SUPERPOWER, TITLE, CONDITION, ELITE, AVENGER existent).

---

## LA MÉCANIQUE : LE SANG ET LE PERÇANT

| Carte | Ce qu'elle fait |
|---|---|
| `bl001b` Serum Injection | pose 2 pions de sang sur l'identité |
| `bl005` Vampire Bite | en pose 1 (ou soigne, ou les deux si l'ennemi tombe) |
| `bl001a` Blood Rush | en dépense 1 pour redresser Blade (1 par phase) |
| `bl009` Daywalker | même redressement, contre 2 dégâts, même limite |
| `bl011` The Thirst | en mange 1 par tour, sinon 2 dégâts |
| `bl003`, `bl007`, `bl015`, `bl009` | donnent le perçant |
| `bl008` Blade's Sword | +1 aux attaques perçantes |
| tout le set némésis | « attacks with piercing deal double damage » |

Deux cartes du set némésis sont des **copies du set Horror de Mojo** :
Vampire (`39051`) et Bandolier of Stakes (`39048`). Leurs modules sont les
modèles exacts de `bl014` et `bl015` ; Dracula est un Vampire à 12 PV.

---

## CE QUE LES GATES ONT TROUVÉ

Sept cas rouges à la première passe, **trois défauts de code corrigés**,
un défaut de vérificateur, deux cas mal montés, un cas impossible :

### 1. `GiveKeywordToAttached` et une carte dont la face est ÉCHANGÉE : `KeyError: 'VAMPIRE'`

Turned (`bl017`) convertit l'allié en sbire par `TreatAttachedCardAsMinion`
(échange de face, modèle 27171). Un `GiveKeywordToAttached(Minion,
trait="VAMPIRE", health=3)` sur la même carte appliquait puis RETIRAIT ses
bonus sur les DEUX faces (journal : « Tigra (allié) appliquent Turned »,
puis « Tigra (sbire) appliquent Turned », puis « n'appliquent plus » sur
l'allié) et retirait un trait jamais posé sur cette face :
`trait.py:81`, `self.traits_internal[trait].remove(face)` → KeyError, effet
avorté, allié rétabli. Correctif : le trait va dans `process` (comme le
`CopyTrait` de Manipulated Mind), les +3 PV par `GainHealthAndMaxHealth`
sur la face sbire APRÈS l'attache (un `printed_health` posé dans `process`
était écrasé à l'entrée en jeu : 3 PV max au lieu de 6, mesuré).

### 2. Une carte de RENCONTRE en jeu n'a pas de contrôleur joueur

The Thirst (`bl011`) « activait » sans rien faire : `JoueurDeCetteCarte`
(contrôleur ou propriétaire de la carte) rendait None pour une obligation
en jeu. Le joueur se lit sur le MESSAGE (`message.to_player`). À garder
pour toute obligation ou attachement de rencontre à effet joueur.

### 3. Un trait ACCORDÉ disparaît avant le « After ... defeated »

Blood Hunt (`bl012`) : `AfterUnitBeDefeated(Response,
CardFinder(card_type=Minion, trait="VAMPIRE"))` ne partait jamais. Le
journal montre « Hydra Soldier n'appliquent plus Blood Hunt » AVANT la
Response : le sbire vaincu a quitté le jeu, le trait accordé est parti, le
filtre ne matche plus. Correctif : `Minion` sans filtre (écriture exacte de
`27174a` Public Outcry, carte officielle), justifié : tant que Blood Hunt
est en jeu, TOUT sbire est VAMPIRE (premier paragraphe).

### 4. Le vérificateur cherchait la face convertie par `card_id`

Après conversion, la face porte le paper du gabarit « Traitor Minion »
(`aav_traitor_minion`), plus celui de l'allié : `par_id("01051")` ne trouve
rien. Le vérificateur `blade_traitre` cherche par NOM (`par_nom`), et la
cible de l'attaque suivante se nomme `aav_traitor_minion`.

### 5. Aucune commande Puzzle ne COMMENCE un tour de joueur

Pour The Thirst, le vérificateur `blade_debut_de_tour` envoie lui-même
`Message.WhenPlayerTurnBegin(joueur)` (ce que fait `player_phase.py:54`),
puis délègue à `etat_attendu`. Trois cas verts.

### 6. ⚠ Le harnais ne sait pas VIDER la main (cas impossible, retiré)

`main_exclusive: []` est falsy et laisse la main de départ ;
`Puzzle.Discard('01090')` CRÉE une nouvelle Strength et la défausse (la
Strength gagnée reste en main) ; et le pilote DÉPENSE dès qu'il a une carte,
`accepter_choix` ou non. La branche « Otherwise, discard this card » du
Bandolier de rencontre (`bl015`) est donc sans témoin outillé. Elle est la
copie mot pour mot de `39048`.

### 7. `Puzzle.Discard` crée la carte qu'on lui nomme

Corollaire du point 6, à connaître : `FindOrCreateFace` par nom, pas la
carte en main. Consigné ici pour le prochain qui voudra « défausser la
main ».

---

## ⚠ Ce que ces blocs ne peuvent pas voir

- `bl015` : la branche « Otherwise, discard » (point 6).
- `bl006` : la riposte gagnée pendant l'interruption vaut-elle pour la MÊME
  attaque ? Le cas mesure « au moins 1 » sur deux attaques de Rhino.
- `bl012` : x4 sur un sbire Embraced sous Blood Hunt (deux textes de
  doublement cumulés, lecture littérale assumée, non mesurée).
- `bl017` : l'ATQ +1 de l'attachement sur le traître (le vérificateur
  affiche « ATQ 3 » pour Tigra 2 + 1, sans l'exiger).
- `bl002` : un contre-cas « deck sans carte éligible » n'est pas montable
  (recherche moteur qui offre tout quand rien ne matche, observation ares).
- Une vraie partie humaine dans le navigateur : **pas faite**.

---

## Les gabarits, carte par carte

### bl001a : * Blade (héros)

- [x] Étape 2 : `ls001a` Valiant Warrior (`AfterUnitUseBasicPower(Response,
      "You")`, une seule question), `61033a` (pion en COÛT,
      `CostFunc.Counter("This", 1, ...)`), `23001a` (pions sur l'identité).
- [x] Étape 5 : « a basic power » (les trois), « remove 1 blood counter FROM
      HIM » (coût sur l'identité), « ready Blade », « Limit once per PHASE »
      partagée avec Daywalker (`BloodRushPasEncoreResolue`).
      Résultat : conforme.
- [x] Étape 6 : 12 PV / 2 ATQ / 2 CTR / 2 DEF / main 5 ; 1 pion.
- [x] Étape 7 : « 1 pion : Blade se redresse, pion 0, Rhino 2 »,
      « CONTRE-CAS sans pion : Blade reste incliné », « les pions posés en
      civil survivent au changement de forme (2 sur bl001a après le flip) ».
- [x] Étape 7 bis : limite OUI. Témoin : « deux attaques, 2 pions : un seul
      redressement, Blade incliné, 1 pion restant, Rhino 4 ».
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### bl001b : * Eric Brooks (alter-ego)

- [x] Étape 2 : `an001b`/`ok001b` (`WhenCardSetup("This")`, résolu à
      l'étape 16 de la mise en place, après le deck rencontre), `01190`
      Shadow of the Past (`set_aside_nemesis_sets` + `Faces.ShuffleAllTo`),
      `39048` (`Cost(...)`), `23001a` (pions).
- [x] Étape 5 : « other than DRACULA » (nom sans étoile, sans homonyme),
      « Spend a [physical] resource » (`Cost("R")`), « Action » sur la face
      civile, « Limit once per round ».
      Résultat : conforme.
- [x] Étape 6 : 12 PV / REC 4 / main 6 ; 2 pions.
- [x] Étape 7 : « Serum Injection : Strength payée, 2 pions », « Slayer :
      sept cartes némésis dans le deck rencontre, Dracula seul de côté »
      (vérificateur `blade_nemesis_melange`).
- [x] Étape 7 bis : limite OUI. Témoin : « second appel refusé, 2 pions et
      non 4, une carte reste en main ».
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### bl002 : Gear Up

- [x] Étape 2 : `ReduceCostToPlayThis(1, conditions=[...])`
      (resources.py:586), `an001b`/`ar003` (`Search.PlayerCard` deck +
      défausse, `finder=CardFinder(traits=[...])`, `GainCard`).
- [x] Étape 5 : « Action » (les deux formes), « if you are in ALTER-EGO
      form » (condition sur la réduction), « ATTACK, ITEM, TACTIC, OR
      WEAPON CARD » (OU, pas seulement des améliorations).
      Résultat : conforme.
- [x] Étape 6 : coût 1, -1.
- [x] Étape 7 : « héros, coût 1 : Energy paie, le Bandolier sort du deck »,
      « ALTER-EGO, coût 0 : jouée seule en main », « CONTRE-CAS héros seule
      en main : injouable ».
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### bl003 : Go for the Heart

- [x] Étape 2 : `01053`/`ar002` (`DealDamage(..., property=AttackProperty(
      piercing=True))`), `al023` (`GiveStatus("Stunned")`), `ar003` (option
      facultative, `ChooseAbilities(forced=False)` + `canbe_exhaust`).
- [x] Étape 5 : « This attack gains piercing » (à la source), « You MAY
      exhaust a WEAPON upgrade » (facultatif, offert seulement si arme
      prête et ennemi vivant), « stun THAT enemy ».
      Résultat : conforme.
- [x] Étape 6 : coût 2, 4 dégâts.
- [x] Étape 7 : « 4 perçants : le Tenace de Whirlwind ne bloque rien »,
      « + épée : Rhino étourdi, épée inclinée, 5 », « CONTRE-CAS sans arme :
      pas d'étourdissement, 4 », « Vampire (6 PV) tombe à 4 x 2 »,
      « ARBITRAGE : (4 + 1) x 2 = 10 sur Dracula ».
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### bl004 : On the Hunt

- [x] Étape 2 : `ar001a` Bring the War (LE modèle : `CostFunc.SearchForCard(
      Minion, "PutIntoPlayEngagedYou", include_encounter_deck=True)`,
      `searched_faces`, condition « le deck a un sbire »), `ls001a`
      (manigance en cible de l'abilité).
- [x] Étape 5 : « Search the ENCOUNTER DECK » (deck seul), « → » (le sbire est
      le COÛT), « If THAT minion has the VAMPIRE trait » (lu après l'entrée en
      jeu), « draw 1 card ».
      Résultat : conforme.
- [x] Étape 6 : coût 0, 3 menaces, 1 carte.
- [x] Étape 7 : « Hydra Bomber convoqué, 3 menaces retirées (5 → 2), main
      0 », « Vampire convoqué : main 1 ».
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI (réserve : condition « deck sans sbire » sans témoin,
comme ar001a).

### bl005 : Vampire Bite

- [x] Étape 2 : `bl003`/`01053` (attaque du héros), `av008`
      (`HealthUnits`), `23001a` (`PlaceCountersOn`), `08013`/`ar001a` (deux
      branches).
- [x] Étape 5 : « Choose to either ... or ... » (deux `ForChoiceAbility`), « do
      BOTH instead if this attack DEFEATS that enemy » (état lu après les
      dégâts, sans question), « your Vampire Bite attacks gain piercing »
      (Daywalker) lu ICI : `piercing=ControleDaywalker(...)`.
      Résultat : conforme.
- [x] Étape 6 : coût 1, 2 dégâts, 2 soins, 1 pion.
- [x] Étape 7 : « heal 2 : 3 blessures → 1 », « blood : 1 pion, aucun soin »,
      « Hydra Bomber tombe : soin ET pion », « + Daywalker : perçant, Tenace
      de Rhino sans effet (2) », « CONTRE-CAS sans Daywalker : Tenace absorbe
      (0) ».
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### bl006 : Vampiric Reflexes

- [x] Étape 2 : `03005` EM Shield / `br004` (`WhenUnitWouldTakeDamage(
      HeroInterrupt, "You", is_from_attack=True)` + `PreventDamage("All")` +
      `SetLabel('defense')`), `12016` Moxie (`GainUntilRoundEnd(...,
      retaliate=1)`).
- [x] Étape 5 : « from an ATTACK » (`is_from_attack=True`), « prevent ALL »,
      « You MAY exhaust a WEAPON upgrade » (facultatif), « retaliate 1 until
      the END OF THE ROUND » (sur le héros).
      Résultat : conforme.
- [x] Étape 6 : coût 0, riposte 1.
- [x] Étape 7 : « Rhino attaque, tout est prévenu, carte jouée », « + épée :
      épée inclinée, Rhino saigne (≥ 1 sur deux attaques) ».
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI (réserve : la riposte sur la même attaque n'est pas
isolée).

### bl007 : Bandolier of Stakes (amélioration)

- [x] Étape 2 : `39048` Bandolier of Stakes (Mojo) : même pion, même
      `CostFunc.Counter("This", 1, 'stake')`, Uses lu dans `desc` ;
      `DealAdditionalDamage` (sender_damage.py:128) au lieu de
      `GainATKForThisAttack` qui assert une attaque de base.
- [x] Étape 5 : « When A HERO attacks » (tout héros, toute attaque, pas de
      `is_basic_attack` : écart voulu avec 39048), « 1 additional damage and
      gains piercing », « Uses (3 stake counters) » (desc, sortie native).
      Résultat : conforme.
- [x] Étape 6 : coût 1, 3 pions, +1.
- [x] Étape 7 : « attaque de base : 3 → 2 pions, 3 dégâts perçants sur Rhino
      Tenace », « Uses : le dernier pieu fait sortir la carte », « attaque
      d'ÉVÉNEMENT : Go for the Heart 4 + 1 ».
- [x] Étape 7 bis : les pions bornent l'usage (Uses).
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### bl008 : * Blade's Sword

- [x] Étape 2 : `WhenUnitMakeKeyWordAttack(..., has_keyword="Piercing")`
      (do_attack.py:105), message envoyé APRÈS `WhenUnitWouldAttack`
      (can_attack.py:358) ; `DealAdditionalDamage` (sender_damage.py:33).
- [x] Étape 5 : « When BLADE makes an attack WITH PIERCING » (`"You"`,
      mot-clé lu après les interruptions qui le donnent), « increase by 1 »
      (avant le doublement), « Restricted » (desc).
      Résultat : conforme.
- [x] Étape 6 : coût 1, +1.
- [x] Étape 7 : « CONTRE-CAS attaque de base sans perçant : 2 », « + Bandolier :
      2 + 1 + 1 = 4 » (l'ordre des messages), et « (4 + 1) x 2 = 10 » (bl003).
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### bl009 : Daywalker

- [x] Étape 2 : `aa008` (`GiveKeywordToInPlayWhenApplyThis(..., health=3)`),
      `bl001a` (même déclencheur, même nom, même limite),
      `CostFunc.TakeDamage(2, "YourIdentity")`.
- [x] Étape 5 : « +3 hit points », « your Vampire Bite attacks gain piercing »
      (codé dans bl005), « When you would trigger Blood Rush, take 2 damage →
      resolve without paying its cost » (écrit comme une SECONDE Response
      au même moment, coût 2 dégâts, limite partagée : effet identique, le
      moteur n'a pas de message « would trigger an ability »).
      Résultat : conforme, écart d'écriture documenté.
- [x] Étape 6 : coût 2, +3 PV, 2 dégâts.
- [x] Étape 7 : « sans pion : 2 dégâts, Blade se redresse », « limite
      PARTAGÉE : après Daywalker, Blood Rush refusé dans la même phase (le
      pion arrivé entre les deux reste) », « +3 PV » (`attributs`).
- [x] Étape 7 bis : limite OUI (partagée), témoin ci-dessus.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### bl010 : Predatory Instincts

- [x] Étape 2 : `aa008` (`defense=1`), `ar007` (`AfterCardEnterPlay(
      HeroResponse, Enemy)`), `an001b` (`Search.PlayerCard(name=...,
      include_discard_pile=True)`).
- [x] Étape 5 : « Blade gets +1 DEF », « After an ENEMY enters play » (sbire
      ou vilain), « exhaust → », « a copy of VAMPIRE BITE » (nom, sans
      homonyme), « deck AND discard pile ».
      Résultat : conforme.
- [x] Étape 6 : coût 2, +1.
- [x] Étape 7 : « +1 DEF » (`attributs`), « Hydra Bomber entre en jeu : la
      carte s'incline, Vampire Bite en main ».
- [x] Étape 7 bis : aucune limite (inclinaison).
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### bl011 : The Thirst (obligation)

- [x] Étape 2 : `WhenPlayerTurnBegin(ForcedInterrupt, "You")`
      (turn_phase.py:23), fiche uses.md (`desc.Uses = "3,thirst"`, sortie
      native), `ar010` (obligation qui reste en jeu), `ar006` (`DealDamage`
      à l'identité).
- [x] Étape 5 : « When YOUR turn begins », « remove 1 blood counter ... TO
      remove 1 thirst counter » (le sang est la condition), « If you cannot,
      take 2 damage », « Uses (3 thirst counters) », « Give to the Eric Brooks
      player » (`GiveTo`).
      Résultat : conforme, un défaut corrigé (joueur lu sur le message,
      trouvaille 2).
- [x] Étape 6 : 3 pions, 1 + 1, 2 dégâts, 2 boost.
- [x] Étape 7 : « 1 pion de sang : sang 0, soif 2, 0 dégât », « sans sang :
      2 dégâts, soif 3 », « Uses : dernier pion de soif → l'obligation part »
      (vérificateur `blade_debut_de_tour`).
- [x] Étape 7 bis : aucune limite (Uses borne la durée).
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### bl012 : Blood Hunt

- [x] Étape 2 : `ar011`/`40101` (`GiveKeywordToInPlayWhenApplyThis(
      CardFinder(card_type=Minion), trait=, health=, teamwork=)`), `39051`
      (doublement), `27174a` Public Outcry (`AfterUnitBeDefeated(Response,
      Minion)` sur une carte de rencontre), `39043` (`RemoveThreatFromSchemes`).
- [x] Étape 5 : « Non-VAMPIRE minions gain the VAMPIRE trait » puis « VAMPIRE
      minions get +3 hit points and gain teamwork » (donc TOUS les sbires :
      un seul appel sans filtre), le texte de doublement donné aux seuls
      sbires sans VAMPIRE IMPRIMÉ (`paper.traits`, sinon x4 sur Vampire et
      Dracula), « Response: After a VAMPIRE minion is defeated » (`Minion`
      sans filtre : trouvaille 3), « 4 » menaces par joueur (`"4*"`).
      Résultat : conforme, un défaut corrigé.
- [x] Étape 6 : menace 4*, 2 boost, +3, 2 menaces.
- [x] Étape 7 : « Whirlwind VAMPIRE, 9 PV, prend 8 perçants et survit »,
      « Response : Hydra Soldier (7 PV) tombe à 8, 4 → 2 menaces », « un
      Vampire IMPRIMÉ n'est pas doublé deux fois : 8 sur 9 PV », « teamwork :
      le second sbire active contre Blade ».
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI (réserve : x4 sur un sbire Embraced, non mesuré).

### bl013 : * Dracula

- [x] Étape 2 : `39051` Vampire (Mojo) : `CapacitesDeVampire()` du set
      (`UpdateAttacksDealDamage(... "Double")` +
      `AfterUnitAttackAndDamageUnit(ForcedResponse, "This")` +
      `HealHealth(sustained)` sinon `GiveStatus("Tough")`).
- [x] Étape 5 : « If you CANNOT » heal = rien à soigner (même lecture que « If
      no damage was healed » du Vampire), « Elite » (trait), « (Blade's
      nemesis minion) », laissé de côté par le Setup d'Eric Brooks.
      Résultat : conforme.
- [x] Étape 6 : 12 PV / SCH 3 / ATQ 3, 3 boost.
- [x] Étape 7 : « blessé (5), il frappe Blade (3) et soigne tout », « rien à
      soigner : Tenace », « 4 perçants → 8 », « (4 + 1) x 2 = 10 » (bl003).
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### bl014 : Vampire

- [x] Étape 2 : `39051` : COPIE EXACTE (nom, chiffres, texte).
- [x] Étape 5 : homonyme 39051 (aucune recherche par ce nom au pack),
      « If no damage was healed this way ».
      Résultat : conforme.
- [x] Étape 6 : 6 PV / SCH 2 / ATQ 2, 2 boost.
- [x] Étape 7 : « blessé (3), il frappe Blade (2) et soigne tout », « tombe à
      4 x 2 = 8 » (bl003), « sous Blood Hunt : 8 sur 9 PV, pas x4 » (bl012),
      « convoqué par On the Hunt : pioche » (bl004).
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### bl015 : Bandolier of Stakes (attachement)

- [x] Étape 2 : `39048` (Mojo) : COPIE EXACTE (`AskSpendResources(Cost("1"))`,
      `AttachTo2(identité)`, `WhenUnitMakeAttack(HeroInterrupt, "YourHero",
      is_basic_attack=True)` + `CostFunc.Counter`, `GainATKForThisAttack`).
- [x] Étape 5 : « YOUR hero makes a BASIC attack » (≠ bl007), « You MAY spend 1
      resource of any type » (`Cost("1")`), « Otherwise, discard », « Surge »
      et « Uses » en `desc`, sans icône de boost (comme 39048).
      Résultat : conforme.
- [x] Étape 6 : 3 pions, +1 ATQ, 1 ressource.
- [x] Étape 7 : « révélé, Strength dépensée : accroché à Blade, puis un pieu
      donne +1 ATQ et perçant (3 sur Rhino Tenace, 2 pions) ». ⚠ Pas de cas
      « refus » (trouvaille 6).
- [x] Étape 7 bis : Uses.
- [x] Étape 8 : bloc final.

Carte terminée : OUI (réserve : branche « Otherwise, discard » sans témoin).

### bl016 : Embraced

- [x] Étape 2 : `an008`/`dd010` (`GiveKeywordToAttached(Minion, trait=,
      health=<callable>)`, asset.py:13), `39051` (doublement,
      `"AttachedMinion"`), `ransacked_armory` / `01190` (`Search.EncounterCard`
      + `face.Reveal(joueur, effect, if_entered_play=...)` + `AttachTo2`),
      fiche seek.md.
- [x] Étape 5 : « +X hit points where X = their PRINTED hit points »
      (`printed_health` de l'hôte), « Seek a NON-VAMPIRE minion from the
      encounter deck » (`non_trait`, deck seul), « reveal it AND attach »,
      rien à étreindre → défaussé.
      Résultat : conforme.
- [x] Étape 6 : 2 boost, +X.
- [x] Étape 7 : « Whirlwind sort du deck, entre en jeu, porte Embraced, trait
      VAMPIRE », « 6 + 6 PV : 8 perçants, il survit ».
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

### bl017 : Turned

- [x] Étape 2 : `27171` Manipulated Mind (`TreatAttachedCardAsMinion(Ally,
      <gabarit>, process)`, `Filter.One`, `ThisCardGainSurge`), fiche
      traitor.md (gabarit « Traitor Minion », SCH 1 par `process`),
      `Filter.One(..., fewest_remaining_hp=True)`, `desc.ATK+` (sf014).
- [x] Étape 5 : « gains traitor » (sbire engagé avec son propriétaire, 1 SCH),
      « the VAMPIRE trait » et « +3 hit points » posés dans la conversion
      (trouvaille 1), « the ally with the FEWEST remaining hit points »,
      « If you cannot, this card gains surge », « Heal all damage from that
      ally » (avant la conversion, même résultat).
      Résultat : conforme, un défaut corrigé.
- [x] Étape 6 : 1 boost, +1 ATQ, +3 PV.
- [x] Étape 7 : « Tigra (3 PV, blessée 2) choisie devant Jessica Jones :
      sbire VAMPIRE engagé, 6/6 PV, ATQ 3 » (vérificateur `blade_traitre`),
      « le traître prend double : Go for the Heart (8) l'achève, Turned
      part », « aucun allié : surge, défaussée ».
- [x] Étape 7 bis : aucune limite.
- [x] Étape 8 : bloc final.

Carte terminée : OUI.

---

## Étape 8 : autoplay ciblé et passes de contrôle

### Cas, passe parallèle puis séquentielle (07/09/2026, 22:20 et 22:33)

`test_capacites.py … bl0` : **51/51** en parallèle (`PARALLELES=4`) après les
quatre correctifs (première passe 45/52, puis 48, 51 ; un cas impossible
retiré). Séquentiel : **50/51**, l'unique écart étant « bl017 Turned, aucun
allié » dont le processus est mort AVANT la partie (`AssertionError:
port=42050` déjà pris, engine.py:103), pas la carte : rejoué seul en
séquentiel, **3/3** sur `bl017`.

### Substitution (`substituer_pack.py … 31000 bl0`, sources rétablies, md5 identique : 2633f508…)

| Carte | Rouges sans module | Verts restants (attendus) |
|---|---|---|
| bl001a | 2/5 | contre-cas « sans pion », « pions après flip » (ne lit pas le module), « limite partagée » (Daywalker suffit) |
| bl001b | 4/4 | |
| bl002 | 3/3 | |
| bl003 | 6/6 | |
| bl004 | 2/2 | |
| bl005 | 5/5 | |
| bl006 | 2/2 | |
| bl007 | 4/4 | |
| bl008 | 3/5 | contre-cas « sans perçant », « riposte » (l'épée n'y sert que d'arme) |
| bl009 | 3/4 | « Vampire Bite perçant » (lit la présence de la carte, pas son module) |
| bl010 | 2/2 | |
| bl011 | 3/3 | |
| bl012 | 4/4 | |
| bl013 | 4/4 | |
| bl014 | 2/3 | « On the Hunt pioche » (trait imprimé) |
| bl015 | 1/1 | |
| bl016 | 2/2 | |
| bl017 | 2/3 | « aucun allié » (un attachement sans hôte part de toute façon) |

**18/18** modules (deux faces d'identité) avec au moins un cas au rouge sans
leur module.

### Decks

`DECK_NOM=blade verifier_tous_les_decks` : `{"ok": true, "message":
"identite bl001b, main 6, deck 9"}`. Témoin `ares` : `identite ar001a, main
5, deck 10`. Signatures étrangères : **0 sur 127 decks**.

### Autoplay (`autoplay.py --deck blade --vilains rhino --profils equilibre --parties 8`)

| Parties | Bloquées | Tracebacks | V / D | Rounds moy. |
|---|---|---|---|---|
| 8 | **0** | **0** | 0 / 8 (5 éliminés, 3 manigances) | 3,8 |

Cartes jouées par le pilote : Vampiric Reflexes 18, Vampire Bite 14, Go for
the Heart 14, On the Hunt 8, Daywalker 4, Sword 2, Bandolier 2, Predatory
Instincts 1. Quatre « `WhenPlayerInTurn failed` » sur Predatory Instincts :
le pilote tente de la jouer sans pouvoir payer (même famille que Tenacity,
commentaires du pilote), pas un défaut de carte. Le 0 % est celui du profil
`equilibre` sur Rhino (Ares et le témoin officiel font 0 % aussi) ; un deck
de 15 cartes sans aspect se vide tous les trois rounds.

### Gate finale de PROCESSUS-HEROS

- [x] Étapes 1 à 8 complètes
- [x] 17 gabarits « Carte terminée : OUI » : bl001a, bl001b, bl002, bl003,
      bl004, bl005, bl006, bl007, bl008, bl009, bl010, bl011, bl012, bl013,
      bl014, bl015, bl016, bl017
- [x] `verifier_tous_les_decks` relancé, deck `blade` au vert
- [ ] Une partie complète jouée avec le héros : **pas faite** (à jouer par
      l'utilisateur)
