# Portage du pack AGATHA HARKNESS — journal de validation

Set 132, préfixe `aa`, 22 `card_id` (aa001a/b + aa002-aa021). Auteur
**Ripper3** (« MC Custom Content By: Ripper3 »). Zip source : `A créer/Agatha
Harkness-20260829T085949Z-1-001.zip` + la carte « Agatha All Along » fournie
par l'utilisateur (lien Discord, 31/08/2026) — c'était le blocage annoncé
dans le plan.

Gabarit `PROCESSUS-CARTE.md` par carte, comme l'exige la Gate finale de
`PROCESSUS-HEROS.md`. Item n°9 du plan fan-made (groupe A, 2/5), premier
portage mené avec `RECETTES-MOTEUR.md` et `substituer_pack.py`.

---

## 0. Ce que le pack apporte, au-delà du héros

### La carte manquante, et une version à trancher

Le zip ne contenait pas « Agatha All Along ». L'utilisateur l'a fournie ;
elle existe en **deux versions** : 13 menaces (planche du zip) et 10 (Discord
de l'auteur), textes identiques par ailleurs. Arbitrage utilisateur du
31/08/2026 : **13 retenues** — c'est un vrai choix d'équilibrage, la carte se
vide en encaissant des attaques.

### `Puzzle.Thwart` ajouté au harnais

Aucun déclencheur « After <allié> thwarts » n'était joignable par les tests :
`Puzzle.Attack` avait sa branche amie, pas le contre. Miroir exact ajouté
(`MakeBasicPowerLikeInTurn([face], ..., ["THW"])`), utilisé par le cas aa019
Wiccan. Bénéficie à tout le projet.

### Trait COSMIC ENTITY ajouté à l'énum

Comme EARTH-6160 la veille : `TRAITS` dans `card_face.py`.

### Le flux d'élimination, documenté par l'exemple

`Ghost Form` (aa001b) a coûté trois passages. Ce que le portage a établi, et
qui vaut pour toute future carte « après élimination » :
- `player.Eliminate()` (player.py:113) **défausse main, deck, défausse,
  soutiens, alliés** et retire le joueur de `world.players` **AVANT**
  d'envoyer `WhenPlayerEliminated` ; le message **ne porte pas** le joueur ;
- l'identité survit (exclue par `non_card_type=Identity`) mais **ses
  écouteurs ne sont plus servis** : l'ability doit être **ancrée ailleurs**
  (ici la manigance principale, via `RegisterTemp` posé au Setup) ;
- un `RegisterTemp` doit être de type **`Temp0`** : un `ForcedResponse`
  enregistré ainsi n'est jamais traité (silencieux) ;
- la réserve du joueur est vide dans le harnais (`Puzzle.CreatePlayerAdditionalDeck`
  est le chemin du vrai serveur, `server_new_game.py:93`) : le module cherche
  d'abord `player.set_aside_deck`, puis `world.aside_deck` en repli.

### Homonymes, en pagaille (7 familles)

Consignés dans `metadata.collision_note` du deck et en tête du `__init__` du
pack : **Agatha Harkness** (15007 est un SOUTIEN signature du pack officiel
Scarlet Witch), **Scarlet Witch** (héros 15001a, alliés 14002 et 58014),
**Wiccan** (héros fan-made wc001a, alliés 15011/56030, sbire 57061),
**Pixie** (36017, alliée Leadership officielle de la MÊME classe), **Death**
(vilain officiel 45084a/b), **Death's Embrace** (clin d'œil assumé à 15026
Magical Suspension, némésis officielle de Wanda, texte quasi identique).

---

## 1. Étapes de `PROCESSUS-HEROS.md`

| Étape | État | Preuve |
|---|---|---|
| 1. `data/cards.json` | ✅ | pack `agatha_harkness`, 22 card_id ; JSON identique hors nouveau pack ; checksums recalculés |
| 2. Scripts | ✅ | 17 modules (aa016 et aa015 portent des bases automatiques + 1 capacité ; aucun module pour les cartes purement `desc`) ; `test_cards` **4967 ok / 0 err** |
| 3. Deck de départ | ✅ | `deck/starter/agatha_harkness.json`, aspect LEADERSHIP choisi par l'utilisateur (indice fort : l'auteur fournit 2 cartes Leadership) ; monte en partie (« identite aa001a, main 7, deck 33 ») ; `set_aside` = aa013 |
| 4. `data/nemesis/agatha_harkness_nemesis.json` | ✅ | 5 entrées (aa018 en double) |
| 5. `data/sets_info.json` | ✅ | « 132. Custom (Agatha Harkness) », max_id aa021 |
| 6. Images | ✅ | 22 jpg dans `assets/pics/` (Agatha All Along en version 13 menaces) |
| 7. Biographie | ✅ | entrée `aa001a` dans `heros-info.js` (survol à confirmer, cf. §5) |
| 8. Texte français | ✅ | 22 entrées dans `textes-fr-fanmade.ts` (déploiement ui-app à faire, §5) |
| 9. Validation carte par carte | ✅ | §2 : **32/32 cas verts**, 20/22 cartes rouges par substitution (3 exceptions expliquées) |
| 10. Signature d'un autre héros | ✅ | contrôle du guide : 0 anomalie sur les 108 decks |

## 2. Gabarits par carte

Preuve : `BILAN : 32/32 cas passes` (`/tmp/rapport-aa12.json`) ;
substitutions par `tools/substituer_pack.py`.

Toutes les cartes ci-dessous ont leur **carte de référence (étape 2)**, leur
**bloc texte-contre-code (5)**, leurs **nombres (6)**, leur **cas sujet (7)**
et l'**autoplay (8)** du §3. Détail des points non triviaux :

### aa001a * Agatha Harkness (héros) — Carte terminée : OUI
Références iw001a/27078 (`AfterUnitTookDamage`, `is_from_attack=True`),
an011 (`DiscardDeckTopCards`), 01034 (`ReturnToHand`). Mots-pièges : « from
an ATTACK » (les dégâts directs ne déclenchent rien), « an EQUAL number »
(`took_damage`, pas les dégâts annoncés), « discarded THIS WAY ». Cas :
2 (dont la levée du verrou SPELL par aa011), rouges 1/1.

### aa001b * Agatha Harkness (alter-ego) — Carte terminée : OUI
Setup an001b + le montage d'élimination décrit au §0. Cas : 2 (Setup,
Ghost Form en partie à 2 joueurs — en solo l'élimination termine la partie).

### aa002 * Scarlet Witch — Carte terminée : OUI
Jumelle de dz014 Lightbringr. Vérificateur sur mesure
(`aa002_sort_attache`) : `etat_attendu` ne sait pas lire la zone de cartes
posées d'un allié. Rouge 1/1.

### aa003 Ebony / aa012 Regained Youth / aa010 Mirror Image — Carte terminée : OUI
Bonus continus (an008/ho005) + une capacité chacune. aa012 : le déclencheur
est `AfterDeckReset` (21068) ; le cas vide un deck de 33 cartes par
`Puzzle.Draw(40)` — `CreatePlayerDeck` AJOUTE sans vider. aa010 : `SetBeInstead`
(56069) conditionné aux dégâts létaux. Rouges 2/2 chacune.

### aa004 Wake Thy Power / aa005 Witchcraft / aa006 Soul Harvest — Carte terminée : OUI
Branches par couleur (01050 Hulk) et par icônes de boost (15004 Hex Bolt).
Mots-pièges : « for each resource ICON » (une carte à double icône compte
deux fois), « to THAT enemy », « stun or confuse AN enemy » (cible libre).
Rouges 1/1, 2/2, 1/1.

### aa007 Occult Knowledge — Carte terminée : OUI
Texte MOT POUR MOT de 40060 Digging Deep. Le cas prouve la synergie : aa006
la défausse, elle remonte, et son double icône GB déclenche les DEUX branches
de Soul Harvest. Rouge 1/1.

### aa008 * Agatha All Along — Carte terminée : OUI
Manigance-joueur Victory 0 avec bonus AU TABLEAU DES VICTOIRES
(`works_in_the_victory_display=True`, 40006 Technovirus Purge). Trois cas :
pose à 13, Response qui vide, et le passage au tableau qui donne +1 partout
et +3 PV. **Le premier reste vert sous substitution** : c'est un cas de
DONNÉES (desc), assumé.

### aa009 The Witches' Road — Carte terminée : OUI
`AfterUnitChangeForm(to_form=Hero)` filtré MYSTIC + `UpdateNextCardPlayCost`
(16024 Deft Focus). Preuve par le paiement : aa005 (coût 2) payée avec une
seule ressource. Rouge 1/1.

### aa011 Runic Magician — Carte terminée : OUI
Ressource ciblée (54002) via `check_effect_fn` (seul crochet OU du
CardFinder). Son Hero Interrupt vit dans aa001a (helper du `__init__`) :
**le cas correspondant reste donc vert si on stubbe aa011**, par conception,
annoncé dans les deux fichiers.

### aa013 Ghost Agatha — Carte terminée : OUI
Tri du dessus en trois sorts (51016). Rouge 1/1.

### aa014 Chaotic Forces — Carte terminée : OUI
Squelette an010 ; première puce conditionnée à la présence de aa008 au
tableau des victoires ; indirect via kb019. Rouge 1/1.

### aa015 Burned at the Stake / aa016 * Death — Carte terminée : OUI
aa015 donne Robuste à aa016 par `card_ids` (jamais par nom : « Death » est
aussi un vilain officiel) : c'est le verrou du set, Death étant Vulnerable.
**ÉCART ASSUMÉ** : les deux cas d'aa016 restent verts sous substitution car
`desc.HP = "INF"` suffit déjà à la rendre invincible ; le module
`UnitCannotBeDefeatedWhile` (16080b Collector) double la garantie par
fidélité au texte imprimé « [star] Death cannot be defeated ».

### aa017 Funeral — Carte terminée : OUI
Deuxième obligation du pack, DANS le set némésis (cas rare). Rouge 1/1.

### aa018 Death's Embrace — Carte terminée : OUI
Quasi-jumelle de 15026. Le premier cas a dû être **rendu discriminant** :
jouer une carte à coût 0 restait vert sous substitution. Critère final :
aa005 (coût 2) face à 2 icônes — avec le module le paiement ÉCHOUE, donc la
**ressource reste en main** et le vilain est intact. Deux pièges de harnais
notés dans le cas : `cibles` force aussi la cible d'ATTACHE (la carte
n'entrait jamais en jeu), et l'attachement exige `under_control=True`.
Rouges 2/2.

### aa019 Wiccan / aa020 Pixie / aa021 Coven of Chaos — Carte terminée : OUI
Cartes d'aspect bonus. aa019 est le premier usage de `Puzzle.Thwart`.
aa021 : « under its OWNER's control » (piège inverse de « you control »).
Rouges 1/1 chacune.

## 3. Autoplay ciblé (étape 8)

8 parties contre Rhino (normal, équilibré), le 31/08/2026 :

| Deck | V | D | %V | rounds | incidents |
|---|---|---|---|---|---|
| agatha_harkness | 0 | 8 | 0 % | 5,0 | 0 |

- **Grep exhaustif des 8 journaux** : **0 traceback**.
- **Lecture des journaux** : `Power_Absorption` apparaît dans les parties
  (la capacité vedette part vraiment), 13 des 14 cartes jouables sont vues
  en jeu. **aa013 Ghost Agatha n'apparaît jamais** : en solo l'élimination
  termine la partie — c'est le comportement attendu, sa preuve est le cas de
  test à deux joueurs.
- Comparaison : Harry Osborn et Venompool font 0 % eux aussi contre Rhino
  avec ce pilote ; les rounds tenus (5,0) sont dans la même fourchette.

## 4. Batteries finales

- `test_capacites` filtré `aa0` : **32/32**.
- Substitutions : **20/22 cartes** rouges, 3 cas verts expliqués ci-dessus.
- `test_cards` : **4967 ok / 0 err**.
- Deck monté en partie + contrôle des signatures étrangères : 0 anomalie.
- Batterie complète des 862 cas (fichiers PARTAGÉS touchés : `card_face.py`,
  `puzzle.py`, le harnais) : lancée seule, résultat à consigner.

## 5. Ce que ces contrôles ne peuvent pas voir — reste à faire

- **Une vraie partie jouée à la main** (gate finale) : non faite.
- **Survol de la biographie dans le wizard** et **déploiement ui-app**
  (`deployer.sh`) : non refaits depuis l'ajout d'Agatha.
- **Ghost Agatha en multijoueur réel** : prouvée par un cas à deux joueurs,
  jamais vue en partie complète.
- **Le contrôle « premier joueur » d'aa013** : le texte le dit, le module
  laisse le contrôleur courant agir (écart documenté dans le module).
