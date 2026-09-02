# Portage du pack VILAIN GORR THE GOD BUTCHER — journal de validation

Set 136, préfixe `gb`, **26 card_id** pour 34 cartes physiques. Auteur
**BLUEHG**. Pack VILAIN (« Scenario Pack »), pas un héros : ni deck de
départ, ni obligation, ni set némésis. Porté le 02/09/2026.

`PROCESSUS-HEROS.md` ne couvre pas les packs vilain ; les étapes retenues
sont celles qui ont un sens ici (données, scripts, scénarios, sets
d'encartage, images), et chaque carte passe par `PROCESSUS-CARTE.md`.

---

## 0. Ce que le scénario demande au moteur

### Trois horloges à compteurs

| Compteur | Porteur | Rôle |
|---|---|---|
| `plan` | complot principal 1B | +1 à chaque phase du vilain tant qu'il est au stade 2 ou 3 ; à 3, le complot avance |
| `timer` | environnement Godbomb (face A) | défaite à 12 par joueur |
| `necro` | face B, All-Black Necroverse | paliers 3/6/9 par joueur qui renforcent les NECROVERSE, défaite à 12 |

Les trois noms ont été ajoutés au `Literal CardFace.COUNTER` : sans eux,
`IsCounter` refuse le nom et **la partie tombe à la pose du premier
compteur**. Même piège que `'style'` (kate_bishop) et `'disguise'` (beast).

### Un environnement RECTO-VERSO retourné en cours de partie

Une seule carte à deux faces, déclarée `"gb007a,gb007b"` dans le `set_aside`
du scénario. Le complot 3A la retourne si elle est déjà en jeu
(`RemoveCountersOn(All, 'timer')` puis `card.Flip`), et ne la sort de la
réserve que sinon. Modèle : Alert Level 50090a/b (pack `aos`).

⚠ Dans la réserve, la carte est rangée sur sa **face A** : la chercher par
`name="All-Black Necroverse"` ne trouve rien. On la cherche par `card_ids` et
on la retourne avec `flip_to_name`.

### Deux cartes à DOS DE CARTE JOUEUR

Le PDF de l'auteur l'exige noir sur blanc : Heroes' Labor (gb021) et Stalking
Berserker (gb022) ont un dos joueur et vivent dans les decks des joueurs. Le
moteur n'a **aucun champ** pour ça : le dos se déduit du PROPRIÉTAIRE
(`card.py:815-838`). Il faut donc créer la carte **dans** `player.player_deck`
(`CardFactory.GenerateCard('gb021', joueur.player_deck, monde)`), ce que font
les complots 2A et 3A. Modèle : Panicked Refugees 45178 (pack `aoa`).

Leur « After you draw X or discard it from the top of your deck, reveal it »
se code en deux fabriques : `AfterCardEnterHand` (le moteur n'a pas de
message « After you draw ») et `AfterCardDiscardInternal(from_where=
"PlayerDeckTop")`.

### Le trait NECROVERSE

Ajouté au `Literal TRAITS`. Purement déclaratif, comme tous les traits.

### Le modulaire « Necroverse » est un pack EXTERNE

Deicide 1A cite trois sets : « Gorr the God Butcher, **Necroverse**, and
Standard ». Premier montage : couper les 11 cartes au trait NECROVERSE pour
en faire le modulaire. **Faux.** L'utilisateur a fourni le 02/09 le dossier
Drive « Necroverse [1.5] », un set de **8 cartes** du même auteur, dont le
pied de carte dit « NECROVERSE (1/8) ». Les 34 cartes du zip Gorr portent
toutes « GORR THE GOD BUTCHER (x/34) » : elles forment **un seul set**.

Le Setup et le complot 3A cherchent donc le `set_name` « Necroverse » : ils
ne trouvent rien tant que ce set n'est pas porté, et fonctionneront sans
changer une ligne le jour où il le sera. C'est la raison pour laquelle le cas
du Setup (gb004a) reste vert sous substitution — voir §2.

### Le modulaire recommandé, « Intergalactic Hazards »

Introuvable au départ (ni officiel, ni dans nos packs, ni dans les zips
Galactic Storm / Skrull Menace). Le texte ne fait que le **recommander** :
n'importe quel modulaire convient. **Légions de Hel** retenue par défaut
(choix de l'utilisateur), le joueur pouvant en choisir un autre à l'écran de
préparation. L'utilisateur a depuis fourni le vrai set (6 cartes), à porter.

---

## 1. Étapes

| Étape | État | Preuve |
|---|---|---|
| `data/cards.json` | ✅ | pack `gorr`, 26 card_id |
| Scripts | ✅ | 22 modules dans `cards/pack/gorr/gorr_the_god_butcher/` ; `test_cards` **5047 ok / 0 err** |
| Scénarios | ✅ | `data/scenarios/gorr.json` (Gorr I + II) et `gorr_expert.json` (II + III), 3 stades, `set_aside` = environnement + Gestalt |
| Set d'encartage | ✅ | `data/encounter_sets/gorr.json`, 18 cartes |
| `data/sets_info.json` | ✅ | « 136. Custom (Gorr the God Butcher) », 2 scénarios |
| Images | ✅ | 26 jpg dans `assets/pics/` |
| Préfixe | ✅ | `tools/prefixes_fanmade.json`, entrée `gb` à 26 cartes |
| Validation carte par carte | ✅ | §2 : **30/30 cas verts**, **25/26 cartes rouges** par substitution |

---

## 2. Cartes, et ce que les tests ont trouvé

Les 22 modules portent chacun leur bloc « CARTES DE RÉFÉRENCE » et
« TEXTE CONTRE CODE » en en-tête. Ce journal ne répète que les arbitrages et
les pannes.

### Trois vrais défauts trouvés par les tests

1. **`"Retaliate": "1"` dans le `desc` de gb014** (Vicious Tendrils) faisait
   planter la **création de la carte** : `Retaliate` est un attribut d'UNITÉ,
   un `Attachment` ne l'enregistre pas (`KeyError`, `has_attribute.py:32`).
   Le texte dit « **Gorr gains** retaliate 1 » : c'est un bonus DONNÉ, par
   `GiveKeywordToAttached(retaliate=1)`. Trouvé par l'autoplay, qui plantait
   au montage de la partie.
2. **`message.GetToPlayer()` sur `WhenUnitWouldAttack`** (gb012, Mind-Hewn
   Blade) : cette méthode n'existe que sur les messages de révélation. Le
   joueur attaqué se lit `GetAgainstPlayer()`. L'`AttributeError` était
   avalée par `effect_invoke.py` : **la carte ne faisait rien, en silence**.
3. **`LimitOncePerPhasePerPlayer` rendait gb020 INERTE** (You Are My God).
   La condition `assert isinstance(message, TriggerNonePlayerMessage)`
   (`once_per.py:30`) ne tient pas sur `AfterUnitAttackEnd`, et l'assertion
   était avalée. La limite est donc écrite à la main sur le même registre du
   moteur (`world.stat.IsOncePerPhasePerPlayer`). ⚠ `LimitOncePerPhase`
   aurait été un second piège : elle est GLOBALE (panne documentée sur
   wd056b).

### Trois faux verts trouvés par la substitution

- **gb020** a dû être réécrit **trois fois** : l'obligation de Spider-Man
  pose déjà 1 dégât au setup, les cartes de boost font varier le reste,
  `degats_identite_min` **n'est pas une clé de `etat_attendu`** (elle
  n'existe que dans un vérificateur du pack `al`, donc elle était ignorée en
  silence et le cas ne vérifiait RIEN), et SONNER le vilain annule toute
  l'**activation**, donc le déclencheur n'est jamais émis. Le cas déclenche
  désormais lui-même une activation sans boost et compte les dégâts : 2 pour
  une attaque, 4 pour deux.
- **gb008** : vérifier « en réserve » ne suffisait pas, il fallait exiger
  « ET pas dans la défausse de rencontre ».
- **gb017** : le dégât indirect venait de l'activation de Gorr, pas de la
  carte ; le cas vérifie maintenant le **surge**.

### Trois cas restent verts sous substitution, assumés

- **gb004a** (Setup) : il met de côté un set modulaire **externe et pas
  encore porté**, et l'environnement comme le Gestalt sont déjà hors jeu par
  le `set_aside` du scénario. La carte n'a donc rien à faire de mesurable
  aujourd'hui. **Le cas deviendra démonstratif dès que le set Necroverse
  sera porté.**
- **gb004b** et **gb007b** : contre-cas d'ABSENCE d'effet (vilain au stade I,
  5 compteurs au lieu de 6), verts par construction.

### Arbitrages

- **Un seul set d'encartage** pour les 34 cartes (voir §0).
- **Répartition des stades** : `gorr.json` = Gorr I + II, `gorr_expert.json`
  = II + III, comme le dit Deicide 1A.
- **`Advance` explicite vers 3A** pour le vilain III : le texte l'impose, et
  le complot peut être encore en 1B.
- **Aucun `Advance` sur les faces A** : une face A sans `TargetThreat` est
  avancée toute seule par le moteur (`scheme_main.py:65-73`) ; en coder un
  ferait sauter un stade.
- **Le « if able » de Heroes' Labor** se lit sur le retour booléen de
  l'helper `PoserTimer` du pack, il ne se devine pas.
- **Blighted Chains** : « a hero's basic power » n'a pas de clé unique dans
  le moteur ; trois fabriques dédiées (attaque, contre, défense).

---

## 3. Autoplay ciblé

8 parties `spider_man` contre `gorr` (normal, équilibré), plus 8 parties
TÉMOIN contre `rhino`, le 02/09/2026 :

| Scénario | V | D | %V | rounds | incidents |
|---|---|---|---|---|---|
| gorr | 0 | 6 | 0 % | 9,1 | 2 bloquées |
| rhino (témoin) | 0 | 7 | 0 % | 5,6 | 1 bloquée |

- **Grep exhaustif des 8 journaux** (`NameError|AttributeError|TypeError|
  KeyError|AssertionError`) : **0 partout**.
- **Les 2 blocages ne viennent pas du pack** : même question fautive
  (`Hero_Action id=64`), même carte — **Tenacity 01093, une carte OFFICIELLE
  du Core Set** — et le témoin Rhino bloque exactement pareil. Défaut
  préexistant du pilote sur cette carte.
- **18 des 22 cartes vues en jeu réel.** Jamais vues : gb003 (vilain III,
  expert seulement), gb006 (stade 3, jamais atteint en 9 tours), gb008
  (Gestalt, il faut 3 Necro-Raven en jeu), gb022 (stade 3). Leurs preuves
  sont les cas du §2.
- Le 0 % de victoire est la norme du bot (le témoin fait pareil), et Gorr
  tient 9,1 tours contre 5,6 à Rhino : le scénario dure plus longtemps, ce
  qui est cohérent avec ses 13/16/19 PV par joueur.

---

## 4. Batteries

- `test_capacites` filtré `gb0` : **30/30**.
- Substitution : **25/26 cartes** rouges, 3 cas verts expliqués au §2.
- `test_cards` : **5047 ok / 0 err**.
- ⚠ Batterie complète du harnais : **à faire** (fichiers partagés touchés :
  `card_face.py` pour les compteurs et le trait, `tools/test_capacites.py`).

---

## 5. Ce que ces contrôles ne voient pas — reste à faire

- **Une vraie partie jouée à la main** : non faite.
- **Les deux sets modulaires** fournis par l'utilisateur le 02/09, à porter :
  **Intergalactic Hazards [2.5]** (6 cartes) et **Necroverse [1.5]**
  (8 cartes), tous deux de BLUEHG, zips à la racine du dépôt. Le second
  rendra démontrable le Setup de gb004a et rendra au scénario son escalade
  d'origine.
- **Le stade 3 en partie réelle** : l'autoplay ne l'atteint jamais, seuls
  les cas de test y vont (par le vilain III en expert).
