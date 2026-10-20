
---

## 4. Les cartes du héros : `data/cards.json`

Les règles générales du format d'une carte (clés de premier niveau, toutes les clés `desc`, balises du texte
imprimé, listes blanches de traits et de compteurs) sont dans le manuel de campagne fourni en **annexe L**
(`annexes/L-manuel-campagne-cartes-et-scripts.md`) et rappelées au **chapitre 12**. Ce chapitre ne dit que ce qui
est **propre à un héros**. Toutes les valeurs ont été **mesurées le 20/10/2026 sur le fichier réel**.

### 4.1 Forme de ta livraison

Tu ne livres **jamais** `data/cards.json` entier. Tu livres un fragment qui ne contient que **ton** pack, cartes
triées par `card_id`, indentation de 4 espaces, `ensure_ascii=False` :

```json
{
  "<pack>": [
    { "card_id": "xx001a", "type": "Hero", ... },
    { "card_id": "xx001b", "type": "AlterEgo", ... }
  ]
}
```

La **clé du pack** est un nom court en minuscules et soulignés (`lockjaw`, `iron_fist`) ; c'est aussi le nom du
dossier `src/cards/pack/<pack>/` et la valeur de `name` dans l'entrée de `sets_info`. Le `checksum` n'est pas
ton affaire.

### 4.2 Les cartes d'un pack de héros, dans l'ordre où on les numérote

Mesuré : Iron Fist compte 13 cartes, Harry Osborn 18, Lockjaw 31, Ant-Man 35 (avec ses cartes d'aspect). La
numérotation suit **l'ordre imprimé de la boîte** (numéro de collection) :

| Rang | Cartes | `type` | `set_name` | Exemple (Lockjaw) |
|---|---|---|---|---|
| 1 | l'identité : face héros `…001a`, face alter ego `…001b`, (formes de plus `…001c`…) | `Hero`, `AlterEgo` | le nom du héros | `lj001a`, `lj001b` |
| 2 | les **cartes signature** : une carte = un `card_id`, plusieurs exemplaires = le même id répété dans le deck | `Ally` `Event` `Upgrade` `Support` `Resource` | le nom du héros | `lj002`–`lj012` (11 titres, 15 exemplaires) |
| 3 | l'**obligation** (1) | `Obligation` | le nom du héros | `lj013` |
| 4 | les **cartes némésis** (en général 5 exemplaires) | `Minion` `SideScheme` `Attachment` `Treachery` | **`"<Héros> Nemesis"`** | `lj014`–`lj017` |
| 5 | les **cartes d'aspect** que la boîte ou l'auteur fournit (facultatif) | `Ally` `Event` `Upgrade`… | le nom du héros (classe = l'aspect) | `lj018`–`lj030` |

* **Héros officiel** : ids à cinq chiffres, `<n° de pack><n° de carte>` (`12001a` Ant-Man, `64001a` Iron Fist) ;
  le numéro de carte est le **numéro de collection imprimé** (1A/1B, 2 à 12…). Les cartes d'aspect de la boîte ont
  un `set_name` vide (`""`) et une classe d'aspect (`Leadership`, `Basic`…).
* **Héros fan-made** : **deux lettres de préfixe**, trois chiffres, suffixe de face (`lj001a`). Le préfixe est
  choisi **avant la première carte** et déclaré dans `tools/prefixes_fanmade.json` (§4.4).
* **Numérotation continue, sans trou.** Le plus grand identifiant du pack se déclare dans `sets_info` (`max_id`).

### 4.3 Les deux faces de l'identité

Une identité est une **paire** : face `a` = **héros** (type `Hero`), face `b` = **alter ego** (type `AlterEgo`).
**Le jeu commence toujours sur la face `b`** (alter ego) ; le joueur passe en héros en retournant la carte.

| Face | `type` | `desc` obligatoire | Notes |
|---|---|---|---|
| héros `…a` | `Hero` | `HP` `ATK` `THW` `DEF` `HS` | `ATK` (attaque), `THW` (contre-manigance), `DEF` (défense), `HS` (taille de main) |
| alter ego `…b` | `AlterEgo` | `HP` `REC` `HS` | `REC` (récupération) ; **pas** de `ATK` `THW` `DEF` |

* Le **nom** commence par `"* "` (carte unique) sur **les deux faces** : `"* Lockjaw"`, `"* Scott Lang"`.
* Les **traits** diffèrent d'une face à l'autre (`["INHUMAN", "PET AVENGER"]` côté héros, `["INHUMAN", "GOOD BOY"]`
  côté alter ego).
* Les deux faces ont **le même `set_name`** (le nom du héros) et, pour un héros maison, la **même clé `custom`**.
* Les capacités imprimées sur la face (`Setup`, `Response`, `Action`…) vont dans le `text` ; les statistiques de
  base **ne sont pas** des capacités : elles sont automatiques.
* **Formes de plus** : une face `c` (Ant-Man Géant : `12001c`, type `Hero`, ses propres `HP ATK THW DEF HS`), `d`,
  `e` (Conan, Moon Knight). Elles se déclarent dans `hero` du deck de départ (§5.2). Une forme de plus est de type
  `Hero` ou `AlterEgo` selon ce qu'elle est.
* **Taille d'image** : voir §7.2.

{{CARTE:lj001a}}

{{CARTE:lj001b}}

Un héros officiel avec **trois formes** (Ant-Man) — notez que la forme Géant a des stats inverses (ATK 3, THW 1,
DEF 3, HS 4) :

{{CARTE:12001c}}

### 4.4 Les cartes signature

* `desc.Class` = **`"Hero"`**. C'est ce qui en fait la carte *de ce héros* : le deck-builder s'en sert pour les
  proposer, et le contrôle « jamais la signature d'un autre héros » (règle 11) s'appuie dessus.
* `set_name` = **le nom du héros**, exactement comme sur la face héros (« Lockjaw »).
* `desc` classique d'une carte joueur : `Cost`, `RES` (lettres `R` physique, `B` mentale, `Y` énergie, `G` joker),
  `HP`/`ATK`/`THW` pour un allié (`"ATK": "4*"` = dégâts consécutifs), `MaxPerDeck` si imprimé.
* **15 exemplaires** au total dans `hero_deck` pour 145 des 152 héros du jeu (§5.2).
* Les **icônes de ressource** se comparent à une carte connue du même pack (règle 8) : jamais « à vue ».
* Un **trait nouveau** (`TELEPORT`, `GOOD BOY`) n'empêche rien (la liste `TRAITS` du moteur n'est qu'un typage), mais
  se signale dans `BESOINS-MOTEUR.md` pour que Claude l'ajoute. Un **compteur nouveau** (`desc.Uses`, par
  exemple `"3,chi"`) **fait échouer la construction de la carte** s'il n'est pas dans l'enum `COUNTER` du
  moteur : voir `reference/compteurs.json`, et signale-le **avant** tout.

{{CARTE:lj003}}

{{CARTE:lj010}}

### 4.5 L'obligation

* `type` = `Obligation`, `set_name` = le nom du héros.
* **`desc.GiveTo` = le nom de l'ALTER EGO** (sans l'étoile) : `"Lockjaw"`. C'est ce qui l'adresse au bon joueur.
  Contrôle du vérificateur : `GiveTo` doit être le nom de la face `b` (148 decks sur 152 ont **une** obligation ;
  deux seulement ont un `GiveTo` qui diffère du nom de l'alter ego, tous deux pour des noms de personnage à
  tiroirs : Iron Lad, SP//dr).
* `desc.Boost` : le nombre d'icônes de boost (l'obligation est aussi une carte de rencontre).
* Le texte commence par `<b><i>Give to the <Héros> player.</i></b>`.

{{CARTE:lj013}}

### 4.6 Le set némésis

* `set_name` = **`"<Héros> Nemesis"`** pour **toutes** les cartes du set.
* En général **5 cartes** (145 decks sur 152) : un **sbire némésis** (`Minion`, souvent `ELITE`), un **complot
  annexe** (`SideScheme`, image **paysage**), des sbires ou attachements/traîtrises de renfort. Les quantités se
  déclarent dans `nemesis_set` du deck de départ (id répété = exemplaires multiples).
* **Le sbire némésis porte `desc.Nemesis`** (`"Lockjaw"` : le nom du héros ; sur 158 sbires marqués des sets némésis du jeu, exemplaires comptés, 109 portent exactement
  le nom de la face héros, les autres un autre nom — celui du deck, de l'alter ego : en cas de doute, question). C'est ce marqueur qui dit au moteur
  « celui-ci est *le* sbire némésis » (cartes du type « mettez en jeu le sbire némésis de ce joueur »). Sans lui,
  le jeu retombe sur une comparaison de noms de sets, fragile : correctif du 04/10/2026 sur Hercules.
* Un héros dont l'éditeur n'a **pas publié** l'obligation ni le set némésis (Iron Fist au 20/10/2026) a
  `obligations: []` et `nemesis_set: []` : tu le dis dans `QUESTIONS.md` — jamais une obligation inventée.

{{CARTE:lj014}}

{{CARTE:lj015}}

### 4.7 Les cartes d'aspect du pack (si elles existent)

Quand l'auteur ou la boîte fournit des cartes d'aspect (Lockjaw : `lj018`–`lj030`, classes `Aggression`,
`Protection`…), elles sont des **cartes joueur ordinaires** : `Class` = l'aspect, `set_name` = le nom du héros
(fan-made) ou `""` (boîte officielle). **Elles ne sont dans aucun `hero_deck`.** Elles n'entrent dans un deck que
par le `player_deck` **fourni par l'auteur** ou par le deck-builder.

### 4.8 Identifiants, préfixes (héros fan-made)

Le préfixe est **choisi avant la première carte** : propose **deux préfixes libres** à l'utilisateur (question à
choix multiple) et attends sa réponse. Préfixes **déjà pris** (lus dans le registre au moment de la construction ;
aussi dans `reference/prefixes-pris.json`) :

{{PREFIXES:}}

L'entrée à livrer dans `tools/prefixes.<pack>.fragment.json` (modèle : celle de Lockjaw) :

{{PREFIXE:lj}}

### 4.9 Checklist de relecture des cartes d'un héros (à faire avant de livrer)

* [ ] chaque face d'identité a son `type` (`Hero` / `AlterEgo`), son `set_name`, son `*` dans le nom et sa clé `custom` ;
* [ ] face héros : `HP ATK THW DEF HS` ; alter ego : `HP REC HS` (des chaînes) ;
* [ ] toutes les cartes signature ont `Class: "Hero"` et le `set_name` du héros ;
* [ ] l'obligation a `GiveTo` = nom de l'alter ego, et un `Boost` ;
* [ ] les cartes némésis ont `set_name` = `"<Héros> Nemesis"`, le sbire némésis a `desc.Nemesis` ;
* [ ] aucun trou de numérotation ; `max_id` = le plus grand id ;
* [ ] les ressources (`RES`) ont été comparées, pas lues à vue ; chaque doute est une question ;
* [ ] les textes sont ceux de l'image, mot pour mot, balises comprises (`<b>`, `<i>`, `[[TRAIT]]`, `[mental]`, `[star]`…) ;
* [ ] tous les traits et compteurs nouveaux sont dans `BESOINS-MOTEUR.md` ;
* [ ] `verifier-livraison-heros.py` ne donne aucune ERREUR.
