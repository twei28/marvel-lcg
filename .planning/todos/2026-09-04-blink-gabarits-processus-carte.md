# PROCESSUS-CARTE.md — les 21 gabarits du pack BLINK (set 156, `bk`)

Gate de `PROCESSUS-HEROS.md` : un gabarit rempli par carte. Rédigés le
04/09/2026. Auteur du pack : **Kajislav**, zip « Blink (Released) ».

**Preuves communes**, citées une fois :

- **Étape 7, cas** : `test_capacites.py … /tmp/rapport.json bk0` → **23/23**.
- **Batterie complète** (le moteur est touché) : **1242/1246**, les 4 rouges
  étant les 4 rouges antérieurs de `squirrel_girl`, mot pour mot identiques
  avant et après.
- **Étape 8, autoplay** : 16 parties (Rhino, Klaw), **0 erreur** au grep
  exhaustif. Témoin `yondu` sur les mêmes vilains : mêmes chiffres (0 %
  de victoire, 4.0 / 4.5 rounds contre 4.1 / 4.8), donc c'est la ligne de base
  du pilote et non le deck.
- **Decks** : `verifier_tous_les_decks` → **118/119**, le seul échec étant
  antérieur ; le passage de 117/118 à 118/119 est exactement l'ajout de blink.
- **Étape 7, substitution** : `substituer_pack.py .game-src 47300 bk0` →
  **21/21 cartes** tombent au rouge sans leur module.
- **Étape 1** : pack `blink` en queue de `cards.json`, set
  `156. Custom (Blink)`, préfixe `bk` déclaré, checksums recalculés,
  `verifier_prefixes` OK.
- **Étape 4, image** : `assets/pics/bk0*` pour les 21, découpées du zip.
- `test_cards` : **5217 ok / 0 erreur**.
- `verifier_appels_modules` : « tous les appels de blink existent » — mais
  seulement APRÈS avoir réparé l'outil (voir plus bas, c'est la trouvaille de
  la journée).
- `verifier_cartes_en_jeu` : « les 21 cartes portent ce que leur texte
  annonce ».

---

## CE QUE CE PACK A SORTI DU MOTEUR ET DES OUTILS

### 1. Le moteur ne calculait un coût par cible QUE pour Tony Stark

`effect_checker.py` portait ceci, en dur :

```python
if "09039" in [x.paper.card_id for x in effect.context.all_legal_targets]:
```

Hors de ce cas unique, le coût est calculé **une seule fois, avec
`target=None`, avant tout choix de cible** : `Message.WhenCalculateEffectCost`
arrive donc avec `for_targets == []`. Toute réduction conditionnée à la cible
est **silencieusement inerte**.

`bk009` Portal dit exactement cela : « When attached enemy or scheme **would
be a target of** an ATTACK or THWART event, reduce that event's resource cost
by 2. » Résultat observé : le portail s'accrochait bien à Rhino, puis
`Lose Footing` devenait injouable, et le journal ne disait rien de plus que
`WhenPlayerInTurn failed`, c'est-à-dire « coût impayable ».

Deux versions successives ont échoué avant de comprendre : elles lisaient
`check_effect.targets` puis `message.for_face`, deux champs **qui n'existent
pas** sur ce message. `getattr` rendait `None`, la condition était toujours
fausse, et rien ne se plaignait. C'est une mesure instrumentée (un `print`
dans la condition, relu dans le journal du harnais et non sur stdout) qui a
montré `targets= []`.

**Correctif** : deux listes explicites et commentées dans
`EffectChecker.CostDependsOnTarget`, l'une pour les cartes qui changent le
coût **en tant que cible** (`09039`), l'autre pour les améliorations qui le
changent **attachées à une cible** (`bk009`). La boucle par cible coûte un
calcul de coût par cible légale : on ne l'allume que pour les cartes qui en
ont besoin.

### 2. La gate `verifier_appels_modules` était VIDE pour 116 packs sur 122

L'outil ne lisait que `src/cards/pack/<pack>/*.py`. Or un pack de héros est
rangé en `pack/<pack>/<set>/` et `pack/<pack>/<set>_nemesis/` : le seul
fichier au premier niveau est un `__init__.py`. **Aucun module de carte
n'était lu.** L'outil répondait « OK : tous les appels existent » sans en
avoir examiné un seul, et il l'a fait pour night_thrasher, lady_sif,
armored_spidey, iron_man_model_42, yondu, doctor_druid… c'est-à-dire pour
tous les gabarits qui le citent comme preuve.

Seuls les six packs plats historiques (`core`, `dt`…) étaient réellement
couverts, d'où les deux prises que sa propre documentation revendique.

**Témoin de la réparation** : réintroduire `Faces.ShuffleAllToEncounterDeck`
(méthode inexistante, plantage réel sur `bk013`) laissait l'outil au vert
avant, le fait tomber après.

**Ce que la gate réparée a immédiatement trouvé, et que rien d'autre n'avait
vu** :

- `bk018` Timebroker : `this.PlaceThreatOn` n'existe pas. Il maniganciat sans
  poser la moindre menace, et **son cas était vert** parce qu'il mesurait les
  deux autres tiers de la carte. Le cas a été complété.
- `spider_man_rainy/sr014` For My Next Trick… : `this.GetThreat()` n'existe
  pas, la menace se lit par la propriété `this.threat`. L'Interruption forcée
  ne partait **jamais**. Carte antérieure à ce pack, corrigée au passage.

Balayage des 122 packs après correction : **plus aucun appel inexistant**.

### 3. Trois API inventées dans le pack, trois symptômes différents

| Appel écrit | Réalité | Ce que ça donnait |
|---|---|---|
| `this.PlaceThreatOn(...)` (bk018, bk019) | `PlaceThreatOnSchemes` | menace jamais posée |
| `Faces.ShuffleAllToEncounterDeck(...)` (bk013) | `Faces.ShuffleAllTo(..., "EncounterDeck", ...)` | Morph restait en jeu |
| `Search.PlayerCard(...)[0]` (bk008) | rend **une face ou None**, pas une liste | `'Upgrade' object is not subscriptable` |

Aucune des trois n'est vue par `test_cards` : ce sont des accès d'attribut à
l'exécution, dans un corps de fonction qui ne s'exécute qu'en partie.

### 4. Deux cas de test faux sur des modules justes

- **bk002 Sabretooth** : `main_exclusive` lui donnait la carte **en même temps
  que le portail**, donc **avant** sa mise en jeu. « if there is a PORTAL
  upgrade in play » était légitimement faux. L'ordre du cas était la moitié du
  test.
- **bk007 Crystal Palace** : l'obligation `bk017` semblait le déclencheur
  idéal puisqu'elle défausse les portails. Mais elle commence par « You may
  flip to alter-ego form », et `bk001b` **remélange alors tous les portails
  dans le deck** : il n'en reste aucun à défausser, la carte gagne Renfort, et
  le cas mesurait cette cascade. `Puzzle.Discard('bk009')` ne convenait pas non
  plus : il prend un exemplaire **quelconque**, et le journal montrait la copie
  21 partir du deck pendant que la copie 20 restait sur Rhino. Le déclencheur
  retenu est le texte même du portail.

### 5. L'autoplay a sorti une carte qui pouvait faire tomber le moteur

`bk003` Assault Redirection dit « When **a character** would take any amount
of damage from an attack, prevent all of that damage » — plus large que le
« you » des événements de défense officiels (`ma011`, `01003` Backflip). Pris
à la lettre sans borner l'attaquant, « a character » inclut le **vilain** : le
pilote a joué la carte pour annuler les dégâts que Blink infligeait
elle-même à Klaw avec Hit and Run. Le journal disait « Blink défend contre
Blink », puis le moteur tombait sur
`assert being_atk_message.defense_messages == []` (`can_attack.py:427`) : une
défense restait ouverte au milieu d'une attaque.

1 partie sur 16, et **aucun cas de test ne l'aurait trouvée** : c'est
exactement ce que l'étape 8 existe pour attraper.

Correctif : `who_deal_damage=Enemy`, ce que le libellé `(defense)` annonce
déjà. `Unit2` reste volontairement large — alliés et personnages des autres
joueurs sont bien couverts, ce que « a character » demande et ce que « you »
exclurait. Un **contre-témoin calibré** a été ajouté : sans le correctif il
tombe au rouge (`bk003 n'est pas en main`), avec il passe.

### 6. `from_where="PlayerArea"` ne voit pas les portails

Ce filtre teste `from_area.play_area != None`, c'est-à-dire la zone du
**joueur**. Un portail s'accroche à un **ennemi** ou à une **manigance** : il
vit dans la zone d'améliorations de sa cible. Aucun portail ne remplissait la
condition, la Réponse de `bk007` ne partait jamais. « discarded FROM PLAY » se
rend donc directement : `from_area.flags.is_in_play`.

---

## ÉCART ASSUMÉ

- **`bk016` Tallus** : « Shuffle your deck » n'est pas codé. La permission de
  jouer la carte du dessus est accordée par `YouMayPlayCardLikeInHand(...,
  from_where="YourDeckTop")` et vit jusqu'à la fin de la phase ; mélanger dans
  la foulée ferait disparaître la carte que le joueur vient de regarder, avant
  même qu'il ait pu la jouer. Conséquence réelle : la carte du dessus reste
  connue et jouable jusqu'à la fin de la phase. Écart en faveur du joueur,
  signalé dans le module.

---

## QUESTION OUVERTE CHEZ L'AUTEUR

**`bk015` Earth-295** : « ready a unique (★) ally, support or upgrade in
play ». Earth-295 **est elle-même une carte unique**, et rien dans le texte ne
dit « another ». Elle peut donc se cibler elle-même : on l'incline en coût, on
dépense 1 ressource, on la redresse, et on recommence indéfiniment sans que
rien ne se passe. Un humain ne le ferait jamais, mais le pilote d'autoplay
tourne en boucle dessus — c'est **la seule partie bloquée sur 16**, et le
témoin `yondu` n'en a aucune.

La carte est portée **telle qu'imprimée** : la question est posée à l'auteur
plutôt que corrigée d'office. Les trois questions en attente portent sur Doctor Druid
(Druidic Ritual sans événement valide en défausse, portée multijoueur de
Psychiatric Care, absence de condition de retrait sur Harness Violent
Emotions).

---

## Gabarits, carte par carte

Les blocs « étape 2 » et « étape 5 » sont en tête de chaque module.

### bk001a : * Blink (face héros)
- [x] Étape 2 : `05018` Lockjaw, `ma011` (modèle du cas), `09039` (coût/cible).
- [x] Étape 5 : « from PLAY to your HAND » est une **reprise**, pas une
      défausse. Limite une fois par round, qui mord réellement depuis le
      correctif moteur du 03/09/2026.
- [x] Étape 6 : PV 9, ATQ 2, CTR 2, DEF 2, main 5.
- [x] Étape 7 : 1 cas, rouge 1/1.

**Carte terminée : OUI**

### bk001b : * Clarice Ferguson (face alter-ego)
- [x] Étape 5 : « EACH … from play » et « heal 1 for each upgrade **shuffled
      this way** » : le soin se compte sur ce qui a réellement été remélangé.
      Contraste imprimé avec bk001a, qui n'en prend qu'un.
- [x] Étape 6 : PV 9, REC 3, main 6.
- [x] Étape 7 : 1 cas, rouge 1/1.

**Carte terminée : OUI**

### bk002 : * Sabretooth — **OUI** (1 cas, rouge 1/1 ; `CanWorkOnlyInHand()` sur un déclencheur, modèle `21032` Pip the Troll. ⚠ l'ordre du cas fait le test)
### bk003 : Assault Redirection — **OUI** (1 cas, rouge 1/1 ; modèle `ma011`, identité inclinée)
### bk004 : Everywhere at Once — **OUI** (1 cas, rouge 1/1 ; ne frappe QUE les porteurs de portail)
### bk005 : Lose Footing — **OUI** (1 cas, rouge 1/1 ; 4 + 2 par portail sur LA cible, et témoin du timing de défausse de bk009)
### bk006 : Multiple 'Porting — **OUI** (1 cas, rouge 1/1 ; jumeau CTR de bk005)
### bk007 : * Crystal Palace — **OUI** (1 cas, rouge 1/1 ; `from_area.flags.is_in_play`, modèles `ma004` et `27007` pour la zone posée)
### bk008 : * Blink's Quiver — **OUI** (1 cas, rouge 1/1 ; la 2ᵉ Hero Action a reçu une condition, sans quoi le moteur offrait une action morte qui passait devant la fouille)
### bk009 : Portal — **OUI** (2 cas, rouges 1/2 ; la carte qui a fait sortir le trou du moteur. Le second cas est un contre-témoin : sans portail, `Lose Footing` est injouable)
### bk010 : * Nocturne — **OUI** (1 cas, rouge 1/1 ; compte TOUTES les améliorations, pas seulement les portails)
### bk011 : Little Surprise — **OUI** (1 cas, rouge 1/1)
### bk012 : * Mimic — **OUI** (1 cas, rouge 1/1 ; ATQ **imprimée**, et `0**` comme Power Man `21012`)
### bk013 : * Morph — **OUI** (1 cas, rouge 1/1 ; `ShuffleAllTo(..., "EncounterDeck", ...)`, deck de RENCONTRE et non le vôtre)
### bk014 : Proper Funeral — **OUI** (1 cas, rouge 1/1 ; « remove from the game », pas « discard »)
### bk015 : * Earth-295 — **OUI** (1 cas, rouge 1/1 ; carte UNIQUE)
### bk016 : * Tallus — **OUI** (1 cas, rouge 1/1 ; écart « Shuffle your deck » assumé plus haut)
### bk017 : Stranger in This Reality — **OUI** (1 cas, rouge 1/1. ⚠ bandeau BLINK : module dans `blink/`, piège `bt019` vu AVANT d'écrire, cinquième occurrence)
### bk018 : * Timebroker — **OUI** (1 cas, rouge 1/1 ; les TROIS tiers du texte dans un seul cas depuis la correction du `PlaceThreatOn`)
### bk019 : Damaged Reality — **OUI** (1 cas, rouge 1/1 ; même faute `PlaceThreatOn`, trouvée par le cas celle-là)
### bk020 : Timebreakers — **OUI** (1 cas, rouge 1/1 ; convoque ET révèle)

**21 cartes terminées sur 21.**
