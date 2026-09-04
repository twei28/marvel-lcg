# PROCESSUS-CARTE.md — les 15 gabarits du pack DOCTOR DRUID (set 155, `dr`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
04/09/2026. Auteur du pack : **Kajislav**, zip « Doctor Druid (Released) ».

**Preuves communes**, citées une fois :

- **Étape 7, cas** : `test_capacites.py … /tmp/rapport.json dr0` → **21/21**.
- **Étape 7, substitution** : `substituer_pack.py .game-src 60000 dr0` →
  **15/15 cartes** tombent au rouge sans leur module.
- **Étape 1** : pack `doctor_druid` en queue de `cards.json`, set
  `155. Custom (Doctor Druid)`, préfixe `dr` déclaré, checksums recalculés,
  `verifier_prefixes` OK.
- **Étape 4, image** : `assets/pics/dr0*` pour les 15, découpées du zip
  (23 scans hors Extras, 15 cartes distinctes).
- `test_cards` : **5196 ok / 0 erreur**.
- `verifier_appels_modules` : « tous les appels de doctor_druid existent ».
- `verifier_cartes_en_jeu` : « les 15 cartes portent ce que leur texte
  annonce ».
- `verifier_tous_les_decks` : **117/118**, `doctor_druid` au vert (le seul
  échec restant, `sp_dr`, est antérieur).
- **Batterie complète** : **1220/1224**, les 4 rouges étant antérieurs et
  vérifiés identiques avant/après l'ajout du compteur `hate` à l'énum.
- **Étape 10** : contrôle sur les **118 decks de départ** → **0 écart**.
- **Deck de départ** : conforme à la decklist de l'auteur (Extras 47),
  **12 Meneur + 13 Basic**. Aucun arbitrage d'aspect.

⚠ **LE PRÉFIXE EST `dr`, PAS `dd`** : `dd` appartient déjà à `doctor_doom`
(set 139). Le registre des préfixes l'a refusé avant la première ligne de code,
ce qui est exactement sa raison d'être.

---

## LA MÉCANIQUE DU PACK, ET POURQUOI ELLE A DEMANDÉ QUATRE MONTAGES

Sept des huit cartes signature portent « **While this card is in your hand**,
... ». Le héros les rejoue ensuite depuis la défausse, et le set némésis vide
précisément la main. Tout le pack tient sur cette tension.

**Trois montages ont échoué avant le bon :**

1. `CanWorkOnlyInHand()` seul → le bonus s'appliquait **toujours**, même la
   carte partie à la défausse. Ce drapeau est lu par `CheckNotOutOfPlay`
   (`effect_checker.py:241`), qui gouverne la **résolution** d'une capacité,
   pas la collecte des modificateurs continus.
2. `+ condition=` → aucun changement.
3. `+ change_on_event=OnEvent.HandCards(...)` → aucun changement.

**La raison de fond** : aucune carte du dépôt n'avait jamais fait porter un
modificateur **continu** par une carte **située en main**. `21032` Pip the
Troll, que le moteur cite nommément dans son contrôle de zone, emploie bien
`CanWorkOnlyInHand()` — mais sur une capacité **déclenchée**.

**Le montage retenu** est celui de `sm/personal_nightmare/27154` (Evil
Doppelgänger), seule carte du jeu à lire une main : la carte qui **porte** le
bonus est **en jeu** et compte ce que la main contient. C'est donc `dr001a`,
le héros, qui porte les sept bonus, via `ThisGainKeyword` +
`change_on_event=OnEvent.HandCards`.

⚠ **CONSÉQUENCE ASSUMÉE POUR LA SUBSTITUTION** : la moitié « en main » de six
cartes ne vit plus dans leur module. Chacune garde donc un cas **qui lui
appartient en propre** — c'est la raison d'être du cas « ressource » de
`dr004`, écrit exprès après que la substitution l'eut laissée à 0/1.

---

## CE QUE LES GATES ONT TROUVÉ, ET QUE RIEN D'AUTRE N'AURAIT DIT

### 1. Moxie faisait passer au vert une mécanique qui ne marchait pas

Le deck contient `12016` Moxie, que le pilote joue systématiquement en Réponse
au changement de forme : **+1 ATQ, +1 CTR, +1 DEF jusqu'à la fin du round**.
Le +1 que je prenais pour l'effet de mes cartes venait d'elle. **Trois cas
« en main » passaient donc par accident**, alors que le mécanisme était
totalement inopérant.

Ce sont les **contre-témoins « une fois JOUÉE »** qui l'ont révélé : ils
mesuraient l'extinction du bonus, et l'extinction n'arrivait jamais. Sans eux,
le pack partait avec sept cartes dont le bonus ne s'éteint pas, c'est-à-dire
un héros deux fois trop fort, sans qu'aucun test ne s'en plaigne.

La ligne de base Moxie est désormais inscrite dans les cinq cas concernés.

### 2. Le héros et son alter-ego n'avaient AUCUN cas

Sorti par la substitution (« AUCUN CAS — gate non tenue »), et par elle seule :
tous les autres cas passaient. Les deux cartes les plus jouées du pack
n'étaient pas testées. Comblé.

### 3. L'étoile de Nekra ne veut pas dire « par joueur »

Les 41 sbires à étoile du dépôt sont des sbires de **scénario**, dont les PV se
multiplient par le nombre de joueurs. Nekra est une **némésis** : son étoile
signale seulement que son texte modifie ses valeurs. Encodée `3*`, elle aurait
eu 9 PV à trois joueurs. `cards.json` porte donc 3 et 1, et le bonus vit dans
le module.

### 4. `get_new_value` sans `change_on_event` est figé

La valeur se calcule une fois et ne bouge plus : Nekra serait restée à son ATQ
imprimée quel que soit le nombre de pions. ⚠ Le paramètre s'appelle
`change_on_event` sur `GiveKeywordToInPlayWhenApplyThis` et
`ex_change_on_event` sur `GiveKeywordToAttached`.

### 5. Deux API inventées, trouvées par `test_cards` et non par le vérificateur

`CostFunc.GiveStatus` (inexistant → `CostFunc.Custom`) et un argument
positionnel manquant sur `WhenEnemyActivateAgainstYou`. Le vérificateur
statique disait « tous les appels existent » : les deux outils ne se
remplacent pas.

### 6. `Identity`/`Hero` + `control_by="You"`, jamais le littéral `"You"`

Le littéral passe la construction sans erreur mais n'accroche pas l'identité.
Idiome du dépôt : `an002` (taille de main), `aa003` (REC).

---

## ÉCARTS ASSUMÉS

- **`dr001a` Druidic Ritual** : le texte dit « play », le moteur n'a **aucune**
  opération « joue cette carte ». L'idiome est `YouMayPlayCardLikeInHand`
  (modèle `05018` Lockjaw), qui rend la carte **jouable**. Le joueur paie bien
  le coût de l'événement, mais peut renoncer, ce que la carte imprimée ne
  prévoit pas.
- **`dr001b` Psychiatric Care** : X est lu sur la REC **imprimée**. Lire la
  courante ferait boucler la carte sur elle-même (2 donne +2, donc 4, qui
  redonnerait +4…). Le montage est un bonus permanent plutôt qu'une
  interruption : l'effet observable est le même, la REC ne servant qu'à
  récupérer.
- **`dr008` Mystical Protection** : le mot-clé Inébranlable accordé « à chaque
  personnage que vous contrôlez » n'est pas mesurable par `attributs_carte`
  (`stalwart` absent de la table `IMPRIME` du harnais). Le cas mesure l'autre
  moitié de la carte, l'annulation d'une carte de rencontre.

---

## TROIS ÉCARTS DE NOMS — question posée à l'auteur

Les noms de **fichiers**, la **decklist** et les **cartes** divergent. Le scan
fait foi dans les trois cas :

| Fichier | Decklist | Carte (retenu) |
|---|---|---|
| turning astral | Turning Astral | **Astral Travel** |
| studies of druidry | Practice of Druidry | **Practice of Druidry** |
| overcome by emotions | Emotionally Overwhelmed | **Emotionally Overwhelmed** |

Deux entrées de la decklist ne différaient que par l'orthographe :
**Side-by-Side** (`45016`) et **Strength In Numbers** (`03017`).

---

## Gabarits, carte par carte

Les blocs « étape 2 » et « étape 5 » sont en tête de chaque module.

### dr001a : * Doctor Druid (face héros)
- [x] Étape 2 : `05018` Lockjaw (jouer depuis la défausse), `aoa/45043` et
      `01027` (`CostFunc.TakeDamage`), `27154` (lire une main).
- [x] Étape 5 : « Take 1 damage » = COÛT ; « topmost » = dernière défaussée ;
      « Action **ou** Hero Action » exclut `dr008`, qui est une Interruption.
- [x] Étape 6 : PV 9, ATQ 1, CTR 1, DEF 2, main 5. Limite une fois par round.
- [x] Étape 7 : 1 cas, rouge 1/1. Porte aussi les 7 bonus « en main ».

**Carte terminée : OUI**

### dr001b : * Anthony Druid (face alter-ego)
- [x] Étape 2 : `aa003`, `al011` (`recover=` via la fabrique de bonus).
- [x] Étape 5 : « a friendly **character** » inclut les alliés ; X figé sur
      l'imprimé.
- [x] Étape 6 : PV 9, REC 2, main 6.
- [x] Étape 7 : 1 cas, rouge 1/1.

**Carte terminée : OUI**

### dr002 : * Doctor Strange — **OUI** (2 cas, rouges 1/2 ; le vert est la moitié portée par le héros. ⚠ homonyme du héros officiel `09001a`)
### dr003 : * Ancient One — **OUI** (1 cas, rouge 1/1 ; `LookAtDeck` + tri sur `IsDeckBuildingClass`)
### dr004 : Fellow Druid — **OUI** (2 cas, rouges 1/2 ; le cas « ressource » lui appartient en propre)
### dr005 : Astral Travel — **OUI** (2 cas, rouges 1/2)
### dr006 : Awaken Nature — **OUI** (2 cas, rouges 1/2 ; « each enemy / each scheme », aucune cible à choisir)
### dr007 : Elemental Control — **OUI** (2 cas, rouges 1/2 ; la paire « en main / jouée » qui a tout révélé)
### dr008 : Mystical Protection — **OUI** (1 cas, rouge 1/1 ; seule carte du set non rejouable par le héros)
### dr009 : Practice of Druidry — **OUI** (2 cas, rouges 1/2 ; +1 aux **quatre** pouvoirs de base)
### dr010 : Ancient Order of Druids — **OUI** (1 cas, rouge 1/1. ⚠ bandeau « DOCTOR DRUID » : module dans `doctor_druid/`, piège `bt019` payé une 4ᵉ fois)
### dr011 : * Nekra — **OUI** (1 cas, rouge 1/1 ; compteur maison `hate`, plafond 5 codé côté helper)
### dr012 : Harness Violent Emotions — **OUI** (1 cas, rouge 1/1 ; « card » et non « event »)
### dr013 : Emotionally Overwhelmed — **OUI** (1 cas, rouge 1/1 ; modèle `15026`)
### dr014 : Resurrection of Nekra — **OUI** (1 cas, rouge 1/1 ; « activates », pas « attacks »)

**15 cartes terminées sur 15.**
