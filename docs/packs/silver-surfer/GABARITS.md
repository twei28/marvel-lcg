# Silver Surfer (DesignHacker, MC4 SEALED) : gabarits PROCESSUS-CARTE, 16 card_id

Pack `silver_surfer`, préfixe `sv`, set 211. Source : zip « SILVER SURFER (MC4 SEALED) » déposé le 24/10/2026.
Cas : `Fusion/marvel-lcg-src/tools/cas/silver_surfer.py` (filtre `[sv]`, **63 cas verts sur 63**). Plateau :
`ui-app/src/board/silver-surfer-plateau.test.ts` (6 cas). Preuve par substitution : `tools/substituer_pack.py <game> <port> sv`
= **16/16 cartes avec au moins un cas rouge sans leur module** (les cas qui restent verts sont des contre-cas d'ABSENCE d'effet
ou des valeurs imprimées, à assumer ici).

## Arbitrages utilisateur du 24/10/2026 (questions posées une à une, scan à l'appui)

1. **The World Eater (sv013)** n'imprime ni ATK ni SCH : il **ne s'active pas du tout** (`EnemyCannotActivate`, `desc` ATK/SCH = 0 pour le moteur).
2. **The Silver Surfboard (sv003), coût de l'Interruption en alter-ego** : « Silver Surfer » est la face héros, absente en alter-ego → le coût
   n'est PAS payable, la planche part sans piocher (lecture littérale).
3. **Rage of Retribution (sv005)** n'imprime pas « Attach to » : elle se pose **seulement sur l'identité** (cible par défaut du moteur,
   `CanPlayThisUpgradeCard`), cas `sv005 ... se pose sur l'IDENTITE`.
4. **Dawn Greenwood (sv002)** : les deux icônes sous ATK/THW sont des **dégâts consécutifs** ; avec 1 PV elle tombe à chaque action, et son
   Interruption la renvoie en main contre 2 dégâts à l'identité (conforme au texte).
5. Pas de decklist d'aspect fournie : `player_deck` reste vide (PROCESSUS-HEROS étape 3, consigne du 06/09/2026).

## Gates du héros

- [x] Étapes 1 à 8 de PROCESSUS-HEROS : cartes (`cards.json`), scripts, deck de départ, `sets_info.json`, images (`assets/pics`, non versionnées),
      biographie (`heros-info.js`, clé `sv001a`), textes FR (`textes-fr-fanmade.ts` + généré).
- [x] `tools/verifier_tous_les_decks.py` : **154/154 decks montent une partie** (8 échecs « ip/port » d'une passe lancée en double, rejoués un à un : OK).
- [x] `tools/test_cards.py` : 7306 modules OK, 0 erreur ; `verifier_prefixes.py` OK ; `verifier_traductions_fr.py` OK.
- [x] Autoplay : 16 parties (rhino/klaw × équilibré/agressif × 4 graines), **0 traceback** (`grep NameError|AttributeError|TypeError|KeyError|AssertionError` = 0 sur les 16 journaux).
      Les parties durent 2 rounds (témoin Yondu : 4 à 5) : le pilote fait attaquer Dawn Greenwood en boucle, qui s'inflige 1 dégât consécutif et
      coûte 2 dégâts d'identité à chaque retour en main (comportement voulu de la carte, mal joué par le pilote).
- [ ] **Une partie complète jouée par un humain avec le héros : NON FAITE.** Aucun outil du projet ne la remplace (agrément, lisibilité des
      choix, feeling de Silver Up / Cosmic Strength). À faire avant de déclarer le héros terminé.

Cartes en attente de cette seule gate : toutes. Le reste du gabarit ci-dessous est rempli carte par carte.


### sv001a : * Silver Surfer (face HEROS) — AERIAL. COSMIC. ADVENTURER. PV 14, THW 1, ATK 3, DEF 2, main 5.

```
* Silver Surfer (face HEROS) — AERIAL. COSMIC. ADVENTURER. PV 14, THW 1, ATK 3, DEF 2, main 5.
Compunction — Forced Response: After Silver Surfer makes a basic attack, change your form.

Cartes de reference :
 - `tg001a` * Throg : meme fabrique `AfterUnitUseBasicPower(type, "This", op, powers=[...])`
   (« After Throg uses a basic power »), ici restreinte a l'ATTAQUE.
 - `lj008` / helpers de Lockjaw : `identite.ChangeToOtherIdentityForm(effect)` pour « change your form ».

⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
 - « Forced Response » : obligatoire, pas de choix ; resout APRES l'attaque.
 - « makes a BASIC attack » : seul le pouvoir de base ATK compte, pas l'attaque d'un evenement.
 - « change YOUR form » : l'identite du joueur (ici la face heros qui devient Norrin Radd).
 - Le texte « Forced Response » est imprime sur la face HEROS : rien a conditionner en alter-ego.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - sv001a Compunction : apres son attaque de base, la forme change (Hero -> AlterEgo)
      - sv001a Silver Surfer : valeurs imprimees PV 14, AERIAL COSMIC ADVENTURER
      Preuve par substitution : **rouges 1/2** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la carte ne fait que chiffrer, retourner la forme ou déplacer des cartes déjà visibles). Résultat : sans objet.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv001b : * Norrin Radd (face ALTER-EGO) — COSMIC. ADVENTURER. PV 14, REC 4, main 6.

```
* Norrin Radd (face ALTER-EGO) — COSMIC. ADVENTURER. PV 14, REC 4, main 6.
Toomie! — Action: Exhaust Norrin Radd -> search your deck and discard pile for The Silver Surfboard
  upgrade and add it to your hand. Shuffle your deck.

Cartes de reference :
 - `yd001b` * Yondu Udonta (Whistlin') : « Exhaust Yondu Udonta -> ... add it to your hand », meme cout
   `CostFunc.Exhaust("YourIdentity")` et meme fouille `Search.SearchForCards`.
 - `an001b` * Aldrif Odinsdottir, `ok001b` * Okoye : fouille du deck + ajout en main, melange par defaut.

⚠ Mots-pieges :
 - « deck AND discard pile » seulement (PAS la main ni le « hors jeu » du mot-cle `summon`) :
   ce n'est pas un `summon`, le texte ne le dit pas.
 - « add it to your HAND » : en main, pas en jeu.
 - « Shuffle your deck » : comportement par defaut de `Search` (rien a coder).
 - « Exhaust Norrin Radd -> » : la fleche en fait un COUT ; l'alter-ego deja incline ne peut plus chercher.
 - Aucune limite imprimee.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - sv001b Toomie! : cherche The Silver Surfboard dans le DECK et l'ajoute a la main (aucune autre carte prise)
      - sv001b Toomie! : cherche aussi dans la DEFAUSSE (contre-cas : planche seulement defaussee)
      - sv001b Toomie! : alter-ego deja inclinee -> pas de recherche (le cout n'est pas payable)
      - sv001b Toomie! : absente en forme HEROS (aucune recherche)
      - sv001b Norrin Radd : valeurs imprimees PV 14, COSMIC ADVENTURER
      Preuve par substitution : **rouges 2/5** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la carte ne fait que chiffrer, retourner la forme ou déplacer des cartes déjà visibles). Résultat : sans objet.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv002 : * Dawn Greenwood — Allie, cout 0, PV 1, ATK 1*, THW 1*, ressource [mental]. ADVENTURER.

```
* Dawn Greenwood — Allie, cout 0, PV 1, ATK 1*, THW 1*, ressource [mental]. ADVENTURER.
Interrupt: When Dawn Greenwood is defeated, deal 2 damage to your identity -> return Dawn Greenwood to your hand.

Cartes de reference :
 - `05002` * Red Dagger (msm) : « Interrupt: When Red Dagger is defeated, <cout> -> ... return to hand »,
   meme fabrique `WhenUnitBeDefeated(Interrupt, "This", op)` et `Faces.ReturnToHand([this], initiator, effect)`.
 - `01027` Focused Rage : cout en degats a l'identite (`CostFunc.TakeDamage`).

⚠ Mots-pieges :
 - « deal 2 damage to YOUR IDENTITY » : les deux formes (heros ET alter-ego), `"YourIdentity"`.
 - la fleche en fait un COUT : si l'identite ne peut pas payer, Dawn est simplement vaincue.
 - « return Dawn Greenwood to your hand » : elle QUITTE le jeu au lieu d'etre defaussee (Interruption).
 - le [star] des icones ATK/THW de l'allie est une icone de degats consecutifs (`1*`), pas un texte.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - sv002 Dawn Greenwood : vaincue, elle retourne en main contre 2 degats a l'identite
      - sv002 Dawn Greenwood : valeurs imprimees PV 1, cout 0, ADVENTURER
      Preuve par substitution : **rouges 1/2** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la carte ne fait que chiffrer, retourner la forme ou déplacer des cartes déjà visibles). Résultat : sans objet.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv003 : * The Silver Surfboard — Upgrade, cout 0, ressource [wild]. AERIAL. COSMIC. VEHICLE.

```
* The Silver Surfboard — Upgrade, cout 0, ressource [wild]. AERIAL. COSMIC. VEHICLE.
Hero Action: Exhaust The Silver Surfboard -> ready Silver Surfer.
Interrupt: When you discard The Silver Surfboard, deal 1 damage to Silver Surfer -> draw a card.

Cartes de reference :
 - `tg001a` * Throg : « ready Throg » = `Faces.ReadyAll(effect.targets)` avec `.SetTarget("YourHero")`.
 - `01027` Focused Rage : « take 1 damage -> draw 1 card », meme cout `CostFunc.TakeDamage` puis `DrawUp(1)`.
 - `intensified.py` / `WhenCardWouldDiscard` : fenetre « When X would be discarded ».

⚠ Mots-pieges :
 - « Silver Surfer » = la face HEROS : en alter-ego (Norrin Radd) il n'y a personne a blesser ni a redresser,
   le cout de l'Interruption n'est alors pas payable (lecture litterale).
 - « When YOU discard » : l'amelioration est en jeu ; une Interruption n'existe que depuis le jeu.
 - « deal 1 damage to Silver Surfer -> » : AVANT la fleche, donc un COUT.
 - Pas de limite imprimee.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - sv003 The Silver Surfboard : Hero Action, incline la planche et redresse Silver Surfer
      - sv003 The Silver Surfboard : defaussee, 1 degat a Silver Surfer et on pioche 1 carte
      - sv003 The Silver Surfboard : defaussee en ALTER-EGO, le cout n'est pas payable (aucune pioche)
      - sv003 The Silver Surfboard : absente en ALTER-EGO (Hero Action inutilisable)
      - sv003 The Silver Surfboard : jouee depuis la main avec un allie en jeu, elle se pose sur l'IDENTITE
      Preuve par substitution : **rouges 2/5** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : cas plateau `ui-app/src/board/silver-surfer-plateau.test.ts` (vert ; aucun correctif de plateau nécessaire, rendu générique). Résultat : OK.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv004 : Energy Manipulation — Amelioration, cout 0, ressource [energy]. COSMIC. SUPERPOWER.

```
Energy Manipulation — Amelioration, cout 0, ressource [energy]. COSMIC. SUPERPOWER.
Action: Spend X [energy] resources -> put X energy counters here.
Hero Action: Discard Energy Manipulation -> draw 1 card (to a maximum of 5) for each energy counter here.

Cartes de reference :
 - `01018` Energy Channel (core) : MEME schema, « Spend X [energy] resources -> put X energy counters here »
   avec `SetCost(Cost("Y"))` (cout variable) + `Faces.PlaceCountersOn(... 'energy')`, puis Hero Action
   `CostFunc.Discard("This")` qui lit `this.GetCounters('energy')` apres la defausse.
 - `06006` Lightning Strike : lecture du paiement variable.

⚠ Mots-pieges :
 - « Action » nue (civile ET heroique) pour poser les compteurs ; « Hero Action » pour piocher.
 - « (to a maximum of 5) » : plafond sur le NOMBRE de cartes piochees, pas sur les compteurs.
 - le compteur `energy` existe deja dans l'enum COUNTER.
 - « Discard Energy Manipulation -> » : la defausse est un COUT, la carte part meme si 0 compteur.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - sv004 Energy Manipulation : Action, depenser Energy (YY) pose 2 compteurs energy
      - sv004 Energy Manipulation : Hero Action, defausse et pioche 1 carte par compteur (3 compteurs -> 3 cartes)
      - sv004 Energy Manipulation : plafond de 5 cartes (7 compteurs -> 5 cartes)
      - sv004 Energy Manipulation : sans compteur, Hero Action = defausse sans pioche
      - sv004 Energy Manipulation : Hero Action absente en ALTER-EGO
      Preuve par substitution : **rouges 4/5** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : cas plateau `ui-app/src/board/silver-surfer-plateau.test.ts` (vert ; aucun correctif de plateau nécessaire, rendu générique). Résultat : OK.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv005 : Rage of Retribution — Amelioration, cout 2, ressource [physical]. CONDITION.

```
Rage of Retribution — Amelioration, cout 2, ressource [physical]. CONDITION.
Silver Surfer gains retaliate 1.
Interrupt: When Silver Surfer would change form, discard Rage of Retribution -> ready Silver Surfer instead.

Cartes de reference :
 - `ar001b` / `45030b` : `WhenUnitWouldChangeForm(Interrupt, "You", op)` (fenetre « would change form »).
 - `aa010`, `ag012` : `message.SetBeInstead(effect)` pour « ... instead ».
 - `14001a` / `tg001a` : `.SetTarget("YourHero")` + `Faces.ReadyAll(effect.targets)`.
 - `RECETTES-MOTEUR` §3 : `*GiveKeywordToInPlayWhenApplyThis("YourHero", retaliate=1)` (« Your hero gains »,
   forme heros seulement, PAS `"You"`).

⚠ Mots-pieges :
 - « Silver Surfer gains retaliate 1 » : un NOM PROPRE, donc la face HEROS seulement (pas Norrin Radd).
 - « would change form » : on part de la face HEROS (from_form=Hero).
 - « discard Rage of Retribution -> » : la defausse est un COUT ; sans elle, rien n'est remplace.
 - « ready Silver Surfer INSTEAD » : le changement de forme n'a PAS lieu, il est remplace par le redressement.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - sv005 Rage of Retribution : Silver Surfer a riposte 1 (Rhino qui l'attaque prend 1 degat)
      - sv005 Rage of Retribution : en ALTER-EGO, pas de riposte (Norrin Radd n'est pas Silver Surfer)
      - sv005 Rage of Retribution : au changement de forme, defaussee pour redresser Silver Surfer a la place
      - sv005 Rage of Retribution : jouee depuis la main avec un allie en jeu, elle se pose sur l'IDENTITE (decision utilisateur du 24/10/2026)
      Preuve par substitution : **rouges 2/4** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la carte ne fait que chiffrer, retourner la forme ou déplacer des cartes déjà visibles). Résultat : sans objet.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv006 : Cosmic Speed — Evenement, cout 3, ressource [energy]. COSMIC. THWART.

```
Cosmic Speed — Evenement, cout 3, ressource [energy]. COSMIC. THWART.
Hero Action (thwart): Choose one:
 • Remove 4 threat from a scheme.
 • Discard The Silver Surfboard -> remove up to 3 threat from each scheme in play.

Cartes de reference :
 - `08013` Stealth Strike (bkw) / `14004` Double Time (qsv) : UN SEUL module `Play` qui fait le choix
   lui-meme par `joueur.ChooseAbilities(effect, ForChoiceAbility(...).SetTarget(...))`. Choisir ainsi evite
   la liste blanche des evenements a DEUX capacites de jeu (`game/card/factory.py`, lecon ls005).
 - `13003` Giant Help (wsp) : `SetLabel('thwart')`.
 - `RemoveThreatFromSchemes("EachScheme", n, effect)` (card_face.py) pour « each scheme in play ».

⚠ Mots-pieges :
 - « up to 3 threat from EACH scheme in play » : toutes les manigances (principale et annexes), 3 maximum
   chacune ; ce n'est PAS un choix de cible.
 - « Discard The Silver Surfboard -> » : la defausse est un COUT, la 2e option n'existe que si la planche
   est EN JEU chez le joueur ; elle passe par `Faces.DiscardAll`, donc l'Interruption de sv003 se propose.
 - « (thwart) » : l'evenement compte comme une action de contre (statut Desoriente).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - sv006 Cosmic Speed : option 1, retire 4 menaces a une manigance (6 -> 2)
      - sv006 Cosmic Speed : option 2, defausse la planche et retire jusqu'a 3 menaces de CHAQUE manigance
      - sv006 Cosmic Speed : sans planche en jeu, seule l'option 1 existe (menace 6 -> 2, aucune autre perte)
      Preuve par substitution : **rouges 3/3** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la carte ne fait que chiffrer, retourner la forme ou déplacer des cartes déjà visibles). Résultat : sans objet.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv007 : Cosmic Strength — Evenement, cout 3, ressource [energy]. COSMIC. SUPERPOWER.

```
Cosmic Strength — Evenement, cout 3, ressource [energy]. COSMIC. SUPERPOWER.
Hero Interrupt: When you make a basic attack, choose one:
 • You get +7 ATK for that attack.
 • Discard The Silver Surfboard -> You get +9 ATK for that attack and it gains overkill.

Cartes de reference :
 - `10003` Hulk Smash (hlk) : `WhenUnitMakeAttack(HeroInterrupt, "You", op, is_basic_attack=True).SetPlay()`,
   `message.GainATKForThisAttack(n, effect)` et `message.GainOverKill(effect)`.
 - `08013` / `14004` : le « choose one » dans UN module, par `ChooseAbilities` (pas de liste blanche).

⚠ Mots-pieges :
 - « basic attack » : `is_basic_attack=True` ; l'attaque d'un evenement ne declenche pas la carte.
 - « +7 » et « +9 » : l'option 2 REMPLACE l'option 1 (+9 et non +16), elle ne s'y ajoute pas.
 - « Discard The Silver Surfboard -> » : la defausse est un COUT, l'option n'existe que si la planche est en jeu.
 - « it gains overkill » : l'attaque, uniquement dans l'option 2.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - sv007 Cosmic Strength : option 1, +7 ATQ pour l'attaque de base (3 + 7 = 10 degats a Rhino)
      - sv007 Cosmic Strength : option 2, defausse la planche -> +9 ATQ (3 + 9 = 12 degats a Rhino)
      - sv007 Cosmic Strength : option 2 contre un sbire de 3 PV, l'exces (overkill) passe au mechant
      - sv007 Cosmic Strength : option 1 contre un sbire, pas d'overkill (le vilain ne prend rien)
      Preuve par substitution : **rouges 3/4** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la carte ne fait que chiffrer, retourner la forme ou déplacer des cartes déjà visibles). Résultat : sans objet.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv008 : Cosmic Energy — Evenement, cout X, ressource [energy]. ATTACK. COSMIC. THWART.

```
Cosmic Energy — Evenement, cout X, ressource [energy]. ATTACK. COSMIC. THWART.
Hero Action (attack): Remove X threat divided among schemes as you choose and deal X damage to an enemy,
  where X is the number of [energy] resources you paid for Cosmic Energy's cost.

Cartes de reference :
 - `14006` Speed Cyclone : cout X (`desc.Cost = "X"`).
 - `06006` Lightning Strike / `52018` Energy Shield : X lu dans le paiement (`GetPaidResources().GetColor("Y")`,
   qui convertit les [wild] en energie).
 - `13003` Giant Help (wsp) : menace « divided among schemes as you choose ».

⚠ Mots-pieges :
 - X = ressources ENERGIE PAYEES (un [wild] paye en vaut une), pas le cout total paye : payer avec du mental
   ne compte pas.
 - « divided among schemes as you choose » : X menaces au total, retirees une par une ou groupees, sur les
   manigances de son choix ; on s'arrete quand il n'y a plus de menace.
 - les DEUX effets (menace ET degats) ont lieu, sans condition l'un de l'autre.
 - (attack) : evenement d'attaque (statut Etourdi), le texte du pack porte aussi les traits ATTACK et THWART.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - sv008 Cosmic Energy : X = 2 [energy] (Energy YY) -> 2 menaces retirees et 2 degats, et PAS de changement de forme
      - sv008 Cosmic Energy : paye en MENTAL (Genius BB), X = 0 -> rien ne se passe
      - sv008 Cosmic Energy : paiement mixte Energy YY + Genius BB, X = 2 seulement
      - sv008 Cosmic Energy : menace repartie entre manigances (X = 2 : principale 1 -> 0 puis annexe 3 -> 2)
      Preuve par substitution : **rouges 3/4** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la carte ne fait que chiffrer, retourner la forme ou déplacer des cartes déjà visibles). Résultat : sans objet.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv009 : Silver Up — Evenement, cout 2, ressource [energy]. COSMIC. SUPERPOWER.

```
Silver Up — Evenement, cout 2, ressource [energy]. COSMIC. SUPERPOWER.
When you play this card, you may discard The Silver Surfboard, then choose two instead.
Alter-Ego Action: Flip to Silver Surfer, then choose one: draw 2 cards, deal 4 damage to an enemy, or ready
  Silver Surfer.

Cartes de reference :
 - `ls005` To Arms! (lady_sif) : Action d'alter-ego « Change to hero form » puis effet, un seul module.
 - `14004` Double Time (qsv) : `ChooseAbilities` pour le choix ; `choose_x_different_options=2` pour « choose
   two » (deux options DIFFERENTES).
 - `lj*` (Lockjaw) : `identite.ChangeToOtherIdentityForm(effect)` pour « flip ».

⚠ Mots-pieges :
 - la defausse de la planche est FACULTATIVE (« you may ») et vient AVANT le choix ; elle fait passer le choix
   de UNE a DEUX options (differentes). Sans planche en jeu, on ne la propose pas.
 - « Flip to Silver Surfer, THEN choose » : le retournement precede le choix, donc « ready Silver Surfer »
   redresse la face heros qui vient d'arriver.
 - la planche est defaussee en forme ALTER-EGO : l'Interruption de sv003 (1 degat a Silver Surfer) n'est pas
   payable ici (lecture litterale, le Surfer n'est pas en jeu), donc pas de pioche.
 - Une seule capacite de jeu (Alter-Ego Action), pas de liste blanche.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - sv009 Silver Up : retourne en Silver Surfer puis pioche 2 cartes (option 1)
      - sv009 Silver Up : retourne puis inflige 4 degats a un ennemi (option 2)
      - sv009 Silver Up : retourne puis redresse Silver Surfer (option 3) : l'identite etait inclinee
      - sv009 Silver Up : avec la planche defaussee, DEUX options (pioche 2 ET 4 degats)
      - sv009 Silver Up : sans defausser la planche, UNE seule option (la planche reste en jeu)
      Preuve par substitution : **rouges 5/5** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la carte ne fait que chiffrer, retourner la forme ou déplacer des cartes déjà visibles). Résultat : sans objet.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv010 : The Power Cosmic — Ressource [energy][energy].

```
The Power Cosmic — Ressource [energy][energy].
Response: After you spend this card to play a [[COSMIC]] event, deal 2 damage to an enemy.

Cartes de reference :
 - `42008` Avian Anatomy (angel) : `AfterYouSpendThisCard(Response, op, to_pay_card=CardFinder2("AERIAL", Event))`,
   meme texte « After you spend this card to pay for a <trait> event ».
 - `sh001` : meme fabrique, Hero Response sur un evenement (sans `SetPlay`).

⚠ Mots-pieges :
 - « Response » nue (pas « Hero Response ») : se joue sous toute identite.
 - « to play a COSMIC EVENT » : trait COSMIC ET type Event ; une amelioration ou un soutien COSMIC ne declenche pas.
 - « an enemy » : un ennemi quelconque (sbire ou mechant), choisi par le joueur.
 - La ressource vaut YY : le deck compte 2 exemplaires.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - sv010 The Power Cosmic : depensee pour un evenement COSMIC (Cosmic Speed), 2 degats a un ennemi
      - sv010 The Power Cosmic : depensee pour un evenement NON cosmique (Haymaker), pas de degats en plus
      Preuve par substitution : **rouges 1/2** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la carte ne fait que chiffrer, retourner la forme ou déplacer des cartes déjà visibles). Résultat : sans objet.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv011 : Silver Down — Obligation (set « Silver Surfer »), Boost 1, « Give to the Norrin Radd player ».

```
Silver Down — Obligation (set « Silver Surfer »), Boost 1, « Give to the Norrin Radd player ».
You may flip to alter-ego form. Choose:
 • Exhaust Norrin Radd -> remove Silver Down from the game.
 • Summon Dawn Greenwood and remove her from the game -> remove Silver Down from the game.

Cartes de reference :
 - `yd013` Banished (yondu) et `lj013` Canine Urges (lockjaw) : MEME squelette — `WhenThisObligationGiveToYou`,
   `YouMayFlipToYourAlterEgoForm`, puis `joueur.ChooseAbilities` avec `condition=` sur chaque branche.
 - `Convoquer` du set (mot-cle maison `summon`, fiche summon.md).

⚠ Mots-pieges :
 - AUCUNE branche ne DEFAUSSE l'obligation : les deux la RETIRENT DE LA PARTIE (piege hc013 : une obligation
   reste en jeu tant qu'on ne la deplace pas).
 - « Exhaust Norrin Radd » : l'alter-ego, donc seulement apres le retournement et si elle est prete ;
   la fleche en fait un COUT.
 - « Summon Dawn Greenwood AND REMOVE HER FROM THE GAME -> » : le tout est le COUT de la 2e branche ; elle
   n'est offerte que si Dawn existe hors jeu (deck, defausse, main...). Dawn est RETIREE de la partie : plus
   jamais disponible.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - sv011 Silver Down : option 1, epuiser Norrin Radd -> l'obligation est RETIREE DE LA PARTIE
      - sv011 Silver Down : option 2, convoque Dawn Greenwood (deck) et la retire de la partie, puis l'obligation aussi
      - sv011 Silver Down : Dawn dans la DEFAUSSE aussi (convocation hors deck)
      - sv011 Silver Down : Norrin Radd deja epuisee -> seule la convocation est possible (Dawn retiree)
      - sv011 Silver Down : sans Dawn hors jeu, seule l'option 1 est possible (alter-ego epuisee, Dawn intacte)
      Preuve par substitution : **rouges 5/5** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la carte ne fait que chiffrer, retourner la forme ou déplacer des cartes déjà visibles). Résultat : sans objet.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv012 : * Galactus (sbire nemesis de Silver Surfer) — PV 3, SCH 2, ATK 2, Villainous. COSMIC. ELITE.

```
* Galactus (sbire nemesis de Silver Surfer) — PV 3, SCH 2, ATK 2, Villainous. COSMIC. ELITE.
Villainous.
When Revealed: Reveal The World Eater and put it into play engaged with you.
When Defeated: Remove Galactus from the game.

Cartes de reference :
 - `04130` The Sleeper (trors) : « When Revealed » + « When Defeated: Remove X from the game »
   (`WhenThisRevealed(None, op)`, `WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", op)`,
   `Faces.RemoveAllFromGame`).
 - `yd015` Sav'rkk (yondu_nemesis) : « reveal / summon X » depuis le deck de rencontre (`Search.SearchForCards`).
 - `Villainous` : lu directement dans `desc` (fiche mots-cles/villainous.md), rien a coder.

⚠ Mots-pieges :
 - « engaged WITH YOU » : engage le joueur a qui Galactus est revele (`message.GetToPlayer()`).
 - The World Eater fait partie du set nemesis, donc du deck de rencontre : on le cherche dans le deck et la
   defausse ; s'il est deja en jeu (Galactus est unique), il n'y a rien a reveler.
 - « Remove Galactus from the game » : jamais defausse, il ne reviendra plus.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - sv012 Galactus : revele, il met The World Eater en jeu (cherche dans le deck de rencontre)
      - sv012 Galactus : vaincu, il est RETIRE DE LA PARTIE (pas defausse), sans World Eater
      - sv012 Galactus : valeurs imprimees PV 3, ATK 2, SCH 2, COSMIC ELITE
      Preuve par substitution : **rouges 2/3** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : cas plateau `ui-app/src/board/silver-surfer-plateau.test.ts` (vert ; aucun correctif de plateau nécessaire, rendu générique). Résultat : OK.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv013 : * The World Eater (sbire nemesis de Silver Surfer) — PV 5, AUCUNE valeur d'ATK ni de SCH imprimee. COSMIC. ELITE.

```
* The World Eater (sbire nemesis de Silver Surfer) — PV 5, AUCUNE valeur d'ATK ni de SCH imprimee. COSMIC. ELITE.
Galactus cannot take damage and his attacks gain overkill.
When Defeated: Remove The World Eater from the game.

Cartes de reference :
 - `01136` Ultron / `01181` Madame Hydra : « X cannot take damage while Y » ; ici l'immunite est posee sur
   une AUTRE carte (Galactus) par `*AbilityFactory.UnitCannotTakeDamage(finder)` (damage.py, correctif du
   30/08/2026 : rend une LISTE, deballage `*`).
 - `yd016` Sword-Gun-Arm : `UnitAttackGainKeyword(..., overkill=True)` pour « attacks gain overkill ».
 - `04130` The Sleeper : « When Defeated: Remove X from the game ».
 - `51038` (bp) : `EnemyCannotActivate` pour un sbire qui ne s'active pas.

⚠ Mots-pieges :
 - ARBITRAGE UTILISATEUR (24/10/2026, question posee avec le scan) : aucune valeur d'ATK/SCH imprimee -> le
   sbire NE S'ACTIVE PAS DU TOUT (ni attaque, ni manigance, pas de carte boost). `desc` porte ATK 0 / SCH 0
   pour le moteur, l'activation est interdite par `EnemyCannotActivate`.
 - « Galactus » = la carte nommee, quel que soit le porteur ; l'effet dure tant que The World Eater est EN JEU.
 - « his attacks gain overkill » : toutes les attaques de Galactus, pas seulement les attaques de base.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (6 cas sujets) :
      - sv013 The World Eater : Galactus ne subit aucun degat tant qu'il est en jeu
      - sv013 The World Eater : vaincu, il est RETIRE DE LA PARTIE (5 PV, 6 degats)
      - sv013 The World Eater : les attaques de Galactus ont overkill (exces sur l'allie vers l'identite)
      - sv013 The World Eater : sans lui, Galactus n'a pas overkill (l'exces est perdu)
      - sv013 The World Eater : sans World Eater, Galactus subit les degats (3 PV, 3 degats -> retire)
      - sv013 The World Eater : ne s'active pas (aucune attaque, aucune carte boost retournee)
      Preuve par substitution : **rouges 3/6** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : cas plateau `ui-app/src/board/silver-surfer-plateau.test.ts` (vert ; aucun correctif de plateau nécessaire, rendu générique). Résultat : OK.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv014 : The Life Stealer — Manigance annexe, menace de depart 2, Boost 2.

```
The Life Stealer — Manigance annexe, menace de depart 2, Boost 2.
All friendly characters get -1 ATK.
When Revealed: Place 1 additional threat here for each friendly character in play.

Cartes de reference :
 - `ho015` / `RECETTES-MOTEUR` §3 : bonus continu sur d'autres cartes par `*GiveKeywordToInPlayWhenApplyThis(
   finder, attack=N)` (rend une LISTE).
 - `50134` / `wd` : `WhenThisRevealed(None, op)` + `this.PlaceThreatOnSchemes([this], n, effect)`.

⚠ Mots-pieges :
 - « friendly characters » = les IDENTITES (heros ou alter-ego) et les ALLIES de tous les joueurs (classe
   `Friend`), jamais les ennemis.
 - « ADDITIONAL threat » : s'ajoute aux 2 menaces imprimees (`StartingThreat`).
 - « for each friendly character IN PLAY » : compte a la REVELATION ; il ne se met pas a jour ensuite.
 - « -1 ATK » : continu tant que la manigance est en jeu.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - sv014 The Life Stealer : revelee avec le heros seul, 2 + 1 = 3 menaces
      - sv014 The Life Stealer : avec Dawn Greenwood en jeu, 2 + 2 = 4 menaces
      - sv014 The Life Stealer : les personnages amis ont -1 ATQ (Silver Surfer : 3 -> 2 degats a Rhino)
      Preuve par substitution : **rouges 3/3** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la carte ne fait que chiffrer, retourner la forme ou déplacer des cartes déjà visibles). Résultat : sans objet.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.

### sv015 : Cosmic Power — Attachement de rencontre, Boost 1, ATK+ 0 [star].

```
Cosmic Power — Attachement de rencontre, Boost 1, ATK+ 0 [star]. 
Attach to Galactus. If you cannot, attach to the villain.
[star] Attached enemy's attacks gain overkill.
Hero Action: Take 3 damage -> remove Cosmic Power from the game.

Cartes de reference :
 - `yd016` Sword-Gun-Arm (yondu_nemesis) : « Attach to X. If you cannot, ... » et
   `UnitAttackGainKeyword("AttachedEnemy", overkill=True)`.
 - `AbilityFactory.AttachToFaceWhenPutIntoPlay(finder, if_cannot_attach_to=Villain)` (attachment.py ; modeles 22030, 53039, ar013 : « EnemyLeader » vise le chef de l'EQUIPE ADVERSE du mode competitif, pas le vilain).
 - `01027` Focused Rage : cout `CostFunc.TakeDamage(n, "YourIdentity")`.
 - `4xxxx` Provoked/Hero Action sur attachement ennemi : `WhenInYourPlayTurn(HeroAction, op)`.

⚠ Mots-pieges :
 - « If you cannot, attach to the VILLAIN » : Galactus absent (pas encore revele, ou deja retire) -> le mechant.
 - « Attached enemy's attacks » : TOUTES les attaques du porteur (Galactus ou le mechant).
 - « Take 3 damage -> » : COUT, subi par l'identite du joueur qui agit ; l'attachement est ensuite RETIRE DE
   LA PARTIE (pas defausse).
 - Le [star] devant « Attached enemy's attacks » est la convention d'impression de l'ATK+ `0*`.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par les cas de valeurs imprimées (PV, coûts, stats) et `desc` de `cards.json`. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - sv015 Cosmic Power : s'attache a Galactus quand il est en jeu
      - sv015 Cosmic Power : sans Galactus, s'attache au vilain
      - sv015 Cosmic Power : les attaques du porteur gagnent overkill (Rhino contre Dawn : 1 d'exces + 2 de cout de Dawn = 3 a l'identite)
      - sv015 Cosmic Power : sans Cosmic Power, l'attaque de Rhino contre Dawn n'a pas d'overkill
      - sv015 Cosmic Power : Hero Action, subir 3 degats retire la carte de la partie
      Preuve par substitution : **rouges 4/5** sans le module (les cas verts restants sont des contre-cas d'absence ou de valeurs imprimées). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties, témoin Yondu, grep tracebacks : 0. Journal lu pour sv002 (boucle Dawn, voir ci-dessus) ; les autres cartes sont peu jouées par le pilote (parties de 2 rounds). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : cas plateau `ui-app/src/board/silver-surfer-plateau.test.ts` (vert ; aucun correctif de plateau nécessaire, rendu générique). Résultat : OK.

Carte terminée : **NON (provisoire)** : tout est vert sauf la partie réelle jouée par un humain (gate du héros), voir plus haut.
