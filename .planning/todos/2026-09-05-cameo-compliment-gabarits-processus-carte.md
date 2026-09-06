# PROCESSUS-CARTE.md — les 3 gabarits du pack CAMEO COMPLIMENT (set 162, `cc`)

Rédigés le 05/09/2026. Auteur du pack : **BlueRiver**, zip « Cameo compliment ».

⚠ **CE N'EST PAS UN PACK DE HÉROS.** Trois cartes d'ASPECT, une par aspect, sans
identité, sans obligation, sans set némésis, donc sans deck de départ.
`PROCESSUS-HEROS.md` ne s'applique pas : seul `PROCESSUS-CARTE.md`, trois fois.
Aucun aspect n'a eu à être arbitré non plus, il est **imprimé sur chaque carte**.

**Preuves communes**, citées une fois :

- **Étape 7, cas** : `test_capacites.py … cc00` → **6/6**, en passe parallèle
  **et** en passe séquentielle, verdicts identiques un à un.
- **Étape 7, substitution** : `substituer_pack.py … cc0` → **3/3 cartes, et
  2/2 cas rouges pour chacune**. Aucun cas ne reste vert sans son module, pas
  même les contre-cas : c'est le meilleur résultat possible, et il s'explique
  (les contre-cas ne mesurent pas une absence d'effet mais un effet
  **différent**, voir plus bas).
- **Étape 1** : pack `cameo_compliment` en queue de `cards.json`, set
  `162. Custom (Cameo Compliment)`, préfixe `cc` déclaré, `verifier_prefixes` OK.
- **Étape 4, image** : `assets/pics/cc00*.png` pour les 3, copiées du zip par
  `tools/importer_images_cameo_compliment.py`. ⚠ **Les sources sont des PNG**,
  seul pack livré ainsi : copiées telles quelles, le moteur servant les trois
  extensions (`mime_type.py:7-27`, `web_server.py:299-301`) et 600 images du
  dépôt étant déjà des PNG. Réencoder en JPG ferait perdre de la qualité pour
  rien.
- `test_cards` : **5304 ok / 0 erreur** (5301 avant le pack, soit **+3**).
- `verifier_desc_mots_cles cameo_compliment` : « les 3 cartes ont un desc
  conforme à leur texte ».
- `verifier_noms_modules` / `verifier_cartes_en_jeu` : OK sur les 3.
- `verifier_appels_modules` : OK — **et la gate a été CALIBRÉE** (§9) :
  `Faces.GiveStatusQuiNExistePas` injecté dans `cc001`, elle a rendu
  « cameo_compliment.cameo_compliment/cc001.py:38 … n'existe pas », puis le
  fichier a été remis et la gate repassée au vert.
- `audit_cartes` : 0 type d'argument, 0 texte-seul, 0 construction impossible,
  0 module en erreur, et **aucune** des 103 suspicions « marqueur sans
  capacité » ne concerne ce pack (le compte n'a pas bougé).
- `verifier_api_cartes` : **5940 fichiers, 3 en faute, toutes ANTÉRIEURES et
  hors de ce pack**.
- **Étape 10** : contrôle des signatures étrangères sur les **124 decks de
  départ** → **0 écart**. Deux decks témoins (`black_cat`, `spider_man`)
  remontent une partie après l'ajout des données.
- **Étape 8** : les 3 textes français dans `textes-fr-fanmade.ts`, **déployés**.
  Conventions du dépôt respectées et vérifiées au grep : « Mise en place » pour
  le mot-clé `Setup` (`ab001b`, `cd003`, `sr012`, `jj001b`, `mk001b`) et
  « Maximum 1 par deck » pour `MaxPerDeck` (`60031`, `bw024`, `lj027`).

---

## PAS DE GATE DE PORTÉE, ET AUCUNE NOUVEAUTÉ MOTEUR

Rien hors de `src/cards/pack/cameo_compliment/` n'a été modifié. Aucun mot-clé
nouveau (`Setup` et `MaxPerDeck` ont déjà leur fiche et sont des **bases
automatiques**, zéro script), aucun compteur nouveau, aucune fabrique nouvelle.

---

## CE QUE CES TROIS CARTES SONT

Le nom du zip dit tout : **le complément de `58031` Cameo**, carte OFFICIELLE de
l'aspect Meneur imprimée dans le pack `wonder_man`, pour les trois autres
aspects.

| Carte | Aspect | Cherche |
|---|---|---|
| `58031` **Cameo** (officielle) | Meneur | un **allié** spécifique à une identité |
| `cc001` **Lock It Down** | Justice | un **soutien** spécifique à une identité, trait **LOCATION** |
| `cc002` **New Suit?** | Protection | une **amélioration** spécifique à une identité, trait **ARMOR** |
| `cc003` **Ye Be Worthy** | Agressivité | une **amélioration** spécifique à une identité, trait **WEAPON**, et **NON PERMANENTE** |

Texte identique à un mot près (« from an identity » au lieu de « for an
identity »), même ordre, même montage. Tout le code vit donc dans **une seule
fonction partagée**, `CapaciteCameo`, dans le `__init__.py` du set : les trois
cartes ne peuvent pas diverger entre elles, et le seul paramètre qui change est
le filtre.

⚠ **Aucun coût, aucune icône de ressource** : les deux coins de la carte sont
vides, vérifié par **découpe d'image** des six coins côte à côte (leçon
Lockjaw). Le `desc` n'a donc ni `Cost` ni `RES`, exactement comme `58031`.

---

## CE QUE LES GATES ONT TROUVÉ

### 1. « Search your collection » n'est PAS un écart à assumer

Le plan de portage donnait ce pack à **4/5**, « brique 4 seule : chercher dans
tout le catalogue une carte d'une identité absente, **avec l'écran qui va
avec** ». Or le moteur sait déjà le faire, et de **deux** façons :

- `Search.Collection` (`search.py:371`) interroge `CardsDB.GetPapers`, fait
  choisir par `AskChoosePaper` et **fabrique** la carte dans la défausse ;
- `58031` Cameo n'utilise pas cette primitive : elle parcourt `CardsDB.papers`
  elle-même, appelle `CardFactory.GenerateCard` **sur chaque candidat** dans
  `world.area_removed`, puis `AskChooseFace`.

**On a recopié le chemin de `58031`, et pour une raison précise** :
`AskChoosePaper` rend un `card_id` sans jamais montrer les cartes, alors que
`AskChooseFace` montre les faces fabriquées. Sur **70 candidats** pour `cc001`,
la différence n'est pas cosmétique — c'est exactement « l'écran qui va avec »
que le plan redoutait, et il existe déjà.

⚠ Le journal de `wd029` Multiverse Recruit assume au contraire un **écart** sur
ce même texte, faute d'avoir vu l'un ou l'autre de ces deux chemins. **L'écart y
est évitable**, et c'est consigné ici pour qu'on y revienne : ce n'est pas le
chantier de ce pack.

### 2. `58031` est imprécise sur « identity-specific », et on ne l'a pas recopiée

La carte officielle ne teste que `paper.set_name in candidate_sets`, c'est-à-dire
« imprimée dans le pack d'un héros ». Or un pack de héros contient **aussi** des
cartes d'aspect et des cartes basiques, que n'importe quel deck peut inclure :
elles ne sont **pas** spécifiques à une identité.

La règle du jeu est claire : « identity-specific » désigne la restriction de
construction de deck, qui vaut `Class: "Hero"` dans les données. **On ajoute donc
ce test** — c'est le **seul écart délibéré** du pack avec sa carte modèle.

Mesure sur le catalogue du 05/09/2026 :

| Filtre | écarte |
|---|---|
| LOCATION supports | **4** : `lj030` * Central Park (Basic, lockjaw), `as019` * The Daily Bugle (Protection), `as022` * Spider-Verse (Basic, armored_spidey), `bk015` * Earth-295 (Basic, blink) |
| ARMOR upgrades | **0** — les deux lectures coïncident |
| WEAPON upgrades | **0** — les deux lectures coïncident |

⚠ L'imprécision de `58031` est donc **réelle mais sans conséquence chez elle** :
aucun allié du dépôt n'est dans ce cas. Consignée plutôt que recopiée.

### 3. Le mot-clé `Setup` n'était prouvé par aucun cas, et une sonde a comblé le trou

Les six cas envoient `Message.WhenGameWouldBegin` **à la main** (voir plus bas) :
ils prouvent la capacité, mais **pas** que le moteur met réellement la carte en
jeu à la mise en place. `desc.Setup = "1"` est une base automatique, et « ne
jamais prétendre qu'un test passe sans l'avoir exécuté » vaut aussi pour les
bases.

Une **sonde d'autoplay** a donc été montée : un deck jetable (Spider-Man,
trois cartes d'aspect remplacées par `cc001`, `cc002`, `cc003`), passé à
`autoplay --deck <chemin>`, **3 parties**. Le journal montre les trois cartes,
à chaque partie :

```
[cc001 Lock It Down] is entering play ([The Break-In!])   <- pendant la mise en place
[cc001 Lock It Down] activates
[Alpha Flight Station]] are being shuffled into <deck du joueur>
[cc001 Lock It Down]] retirée(s)
```

soit **9 mises en place, 9 activations, 9 mélanges, 9 retraits du jeu**, plus
« Discard_2_cards: 3 » au round 0 de chaque partie. Le deck de sonde n'est pas
livré, c'est un fichier de brouillon.

⚠ Une des trois parties est **bloquée**, sur `01093` **Tenacity** — une carte
BASIQUE officielle du deck Spider-Man, sans rapport avec ce pack (le témoin
`spider_man` bloquait déjà 1 partie sur 8 la veille). Écrit ici pour ne pas
laisser croire que la sonde était propre à 3/3.

---

## POURQUOI UNE VÉRIFICATION DÉDIÉE, ET PAS `etat_attendu`

Deux raisons, toutes deux mesurées :

1. **La fenêtre est hors de portée du harnais.** Ces cartes sont branchées sur
   `AfterGameSetup`, donc sur `Message.WhenGameWouldBegin`, envoyé **une seule
   fois** par `world.py:611` à la toute fin de la mise en place — c'est-à-dire
   **avant** que le harnais ne prenne la main. Aucune commande `Puzzle.*` ne le
   renvoie. La vérification l'envoie à la main, exactement comme
   `throg_chomped_fin_de_round` le fait pour `WhenRoundEnd`.
2. **`etat_attendu` ne pourrait pas mesurer la bonne chose.** Un
   `hors_jeu: [cc001]` passerait au vert même si la carte n'avait **rien
   cherché du tout** : « remove this card from the game » est la **dernière**
   phrase. Les chiffres qui comptent sont ailleurs, et la vérification dédiée
   les prend tous les quatre :
   - la carte quitte le jeu ;
   - le deck du joueur gagne **exactement une** carte ;
   - cette carte a le bon **type**, le bon **trait**, `Class: "Hero"`, un
     `set_name` **absent de la partie**, et pour `cc003` **pas de `Permanent`** ;
   - la main perd **exactement deux** cartes.

---

## LES CONTRE-CAS, ET POURQUOI ILS TOMBENT AU ROUGE EUX AUSSI

Les trois contre-cas rejouent le même cas **avec l'identité qui possède la carte
que le pilote choisirait sinon**. Le pilote prend toujours la première option
légale, donc le résultat est déterministe et l'écart se lit en clair :

| Carte | héros du cas nominal → carte trouvée | héros du contre-cas → carte trouvée |
|---|---|---|
| `cc001` | `spider_man` → `01015` * Alpha Flight Station (**Captain Marvel**) | `captain_marvel` → `01026` * Superhuman Law Division (She-Hulk) |
| `cc002` | `spider_man` → `01016` * Captain Marvel's Helmet (**Captain Marvel**) | `captain_marvel` → `01036` Mark V Armor (Iron Man) |
| `cc003` | `spider_man` → `01046` Energy Daggers (**Black Panther**) | `black_panther` → `04002` Hawkeye's Bow (Hawkeye) |

C'est pour cela qu'ils tombent au rouge sous substitution, contrairement aux
contre-cas d'absence des trois packs précédents : ils ne mesurent pas un
**zéro**, ils mesurent un **résultat différent**. Sans module, aucune carte
n'est mélangée du tout et la vérification le dit.

---

## MOTS-CLÉS RENCONTRÉS

| Mot-clé | Cartes | État |
|---|---|---|
| `Setup` | les 3 | fiche existante — **base automatique**, `desc.Setup = "1"`, le moteur met la carte en jeu seul. AUCUN SCRIPT. Prouvé en partie réelle par la sonde du §3 |
| `MaxPerDeck` | les 3 | base automatique, `desc.MaxPerDeck = "1"`. AUCUN SCRIPT |

**Aucune fiche n'a eu à être créée.** ⚠ `LOCATION`, `ARMOR` et `WEAPON` sont des
**TRAITS**, pas des mots-clés : ils vivent dans `traits`, et ce sont les traits
des cartes CHERCHÉES, pas de celles-ci — les trois cartes du pack n'ont
elles-mêmes **aucun trait**.

---

## HOMONYMES ET NOMS

Vérifié sur les 5917 cartes du catalogue : **« Lock It Down », « New Suit? » et
« Ye Be Worthy » n'ont AUCUN homonyme**, et aucune des trois ne cherche quoi que
ce soit par son nom. C'est le premier pack de la journée sans un seul piège
d'homonymie.

⚠ Le fichier du zip s'appelle « New Suit\_.png », avec un **souligné** là où la
carte imprime un **point d'interrogation** : le système de fichiers Windows ne
l'accepte pas. Le `name` de la carte garde son « ? ».

---

## ÉCARTS ASSUMÉS

- **`Class: "Hero"` ajouté à « identity-specific »** : écart délibéré avec
  `58031`, détaillé au §2. Il rend le filtre **plus** fidèle au texte imprimé,
  pas moins.
- **Le dédoublonnage par nom est repris tel quel de `58031`** : deux packs
  peuvent imprimer la même carte (`35002` et `wx002` sont tous deux
  « * Wolverine's Claws »). La joueuse n'a pas à choisir entre deux exemplaires
  identiques. Conséquence : si deux cartes **différentes** portaient un jour le
  même nom et le même trait, une seule serait offerte. Aucune n'est dans ce cas
  aujourd'hui.
- **`cc002` n'a PAS de clause « non-permanent »**, contrairement à `cc003`, et
  ce n'est pas un oubli de l'auteur : c'est imprimé. Une armure permanente reste
  une cible légitime. La vérification de `cc002` ne teste donc pas la
  permanence — elle mesure ce que la carte dit, pas ce qu'on trouverait
  cohérent.

---

## CE QUE CES BLOCS NE PEUVENT PAS VOIR

⚠ **Aucune partie n'a été jouée par un humain dans le navigateur.**

⚠ **Aucune de ces trois cartes n'est dans un deck de départ livré**, et il ne
faut pas en mettre : ce sont des cartes d'aspect que la joueuse ajoute à son
deck, exactement comme `58031`. Elles n'apparaîtront donc **jamais** dans un
autoplay des 124 decks. La seule couverture « en partie réelle » est la sonde du
§3, montée exprès et jetée après.

⚠ **La liste des candidats est un instantané du catalogue.** 70 soutiens
LOCATION, 48 améliorations ARMOR, 52 améliorations WEAPON non permanentes au
05/09/2026. Chaque pack de héros ajouté en fait grossir une ou plusieurs — c'est
voulu, et c'est ce qui rend ces cartes intéressantes, mais cela veut aussi dire
qu'aucun cas ne peut fixer *quelle* carte sera trouvée à long terme. Les cas
fixent le **type**, le **trait**, la **classe**, la **provenance** et la
**permanence** : ce que la carte promet, pas ce que le catalogue contient
aujourd'hui.

---

## Gabarits, carte par carte

### cc001 : Lock It Down (aspect Justice)
- [x] Étape 2 : `58031` Cameo, carte officielle, modèle intégral. Montage
      partagé dans `CapaciteCameo`.
- [x] Étape 5 : « an identity-specific **LOCATION support** » → type `Support`
      ET trait LOCATION ET `Class: "Hero"` (voir §2). « from an identity **not
      in this game** » → on retire les sets des identités présentes, **toutes
      faces confondues** (`GetAllIdentityFace`) : une identité à trois faces ne
      doit pas passer entre les mailles. « Setup » / « Max 1 per deck » → bases
      automatiques.
- [x] Étape 6 : aucun coût, aucune icône de ressource, vérifiés par découpe
      d'image. `MaxPerDeck: "1"`, `Setup: "1"`, `Class: "Justice"`.
- [x] Étape 7 : 2 cas, **rouges 2/2**.
- [x] Étape 7 bis : limite imprimée **OUI**, « Max 1 per deck » — mais c'est une
      règle de **construction de deck**, pas une limite de déclenchement : elle
      n'a pas de témoin d'épuisement possible, et le moteur l'applique seul
      depuis `desc.MaxPerDeck`. La carte se retire du jeu après son unique
      usage, ce que les deux cas mesurent.

**Carte terminée : OUI**

### cc002 : New Suit? (aspect Protection) — **OUI**
(2 cas, rouges 2/2 ; filtre `Upgrade` + ARMOR + `Class: "Hero"`. ⚠ Sur ce trait,
le test `Class: "Hero"` n'écarte **aucune** carte du catalogue : les deux
lectures coïncident, il est gardé pour que les trois cartes du set répondent à
la même définition. ⚠ **Pas** de clause « non-permanent », et c'est imprimé.)

### cc003 : Ye Be Worthy (aspect Agressivité) — **OUI**
(2 cas, rouges 2/2 ; filtre `Upgrade` + WEAPON + `Class: "Hero"` + **pas de
`Permanent`**. ⚠ La clause « non-permanent » est la **seule** qui distingue
cette carte de ses deux sœurs, et la vérification l'exige explicitement. Mesure
sur le catalogue : elle écarte **six** améliorations WEAPON — `35002` et `wx002`
* Wolverine's Claws, `41002a` Psi-Knife, `41002b` Psi-Katana, `43002` * X-23's
Claws, `nt003b` * Battle Board. Toutes sont des armes de signature qui ne
peuvent **pas** quitter le jeu : sans le test, une carte permanente mélangée
dans le deck passerait inaperçue, elle a le bon type et le bon trait.)

**3 cartes terminées sur 3.**
