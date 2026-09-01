# Portage DOCTOR DOOM — set 139, préfixe `dd`, pack `doctor_doom`

**Source** : `A créer/Doctor Doom Hero Revised-20260829T085431Z-1-001.zip`
(24 fichiers). **Auteur : Grawlix Ipsum** (et non « jakxin », comme l'annonçait
`tools/prefixes_fanmade.json` — corrigé).
**Plan** : item n° 16, groupe B, difficulté annoncée 3/5.
**Aspect du deck de départ** : **Agression** (choix utilisateur du 01/09/2026).

---

## 1. Deux erreurs du plan, corrigées d'entrée

1. **« Alt Arts » n'est PAS le même kit de cartes.** Le plan annonçait
   « mêmes 15 noms, même total… un jeu d'illustrations alternatives ». En
   réalité, le zip « Doctor Doom Alt Arts » contient **16 cartes différentes** :
   des arts alternatifs de cartes OFFICIELLES (Spiritual Meditation, Summoning
   Spell, Zone of Silence, Sorcerer Supreme, et les ressources doubles Energy /
   Genius / Strength / endurance) plus quelques cartes custom (Castle Doom,
   Kristoff, Prot-Doombot, Ingenuity). **Aucun nom en commun avec le pack
   Revised.** Il ne sera donc PAS fusionné : à traiter à part, plus tard.
2. **L'auteur est Grawlix Ipsum**, crédité sur chaque carte.

## 2. Inventaire — 17 entrées

### Identités
| card_id | Carte | Imprimé |
|---|---|---|
| `dd001a` | * Doctor Doom (Hero) | CTR 3 / ATQ 1 / DEF 2, MNG 5, 11 PV. LATVERIA. MYSTIC. |
| `dd001b` | * Victor von Doom (AlterEgo) | REC 3, MNG 6, 11 PV. GENIUS. LATVERIA. |

### Signature (15 exemplaires, 10 card_id)
| card_id | Carte | n° | Type / coût / RES | Ex. |
|---|---|---|---|---|
| `dd002` | * Victorious (Zora Vukovic) | 1 | Ally 3, G, HERALD. LATVERIA. | 1 |
| `dd003` | Doombot | 2-3 | Ally 1, R, TECH. **Requirement ([mental])** | 2 |
| `dd004` | "This World Is Mine!" | 4-6 | Event 3, B, ATTACK. SPELL. | 3 |
| `dd005` | "Doom Prevails" | 7 | Event 3, B, SPELL. | 1 |
| `dd006` | "Pain Is For Lesser Men!" | 8-9 | Event 2, B, DEFENSE. SPELL. | 2 |
| `dd007` | Unparalleled Genius | 10-11 | Resource **BBB** | 2 |
| `dd008` | * Doomstadt | 12 | Support 1, R, LOCATION. LATVERIA. | 1 |
| `dd009` | * Doom's Time Platform | 13 | Upgrade 2, Y, TECH. | 1 |
| `dd010` | * Doom's Armor | 14 | Upgrade 3, Y, TECH. | 1 |
| `dd011` | * Doom's Mask | 15 | Upgrade 3, Y, TECH. | 1 |

### Obligations (2 — inhabituel) et némésis (4 cartes, 3 card_id)
| card_id | Carte | Note |
|---|---|---|
| `dd012` | Rescue Cynthia von Doom | Obligation. « Flip to alter-ego form. You may **not** change form. » |
| `dd013` | Incomparable Ego | Obligation. Icônes **acceleration + hazard**, plus une capacité `[star] Boost`. |
| `dd014` | Meddlesome Heroes! | SideScheme, menace 4, 3 boost, hazard. ⚠ image livrée **pivotée**. |
| `dd015` | * Mister Fantastic | Minion, SCH 2 / ATQ 2 / 4 PV, Guard. Patrol. |
| `dd016` | Richards! | Treachery ×2 |

**Doublons vérifiés au coin de ressource** (leçon Beast) : les 5 groupes de
même nom ont tous la **même** icône. Ce sont de vraies copies, contrairement à
Multi-Tasking du pack `bt`.

## 3. Le kit en une phrase : TOUT passe par le mental

L'identité gagne un compteur `power` (max 3) chaque fois qu'un événement SPELL
est payé avec du [mental], et les échange contre le mot-clé **villainous**.
Presque toutes les cartes ont un bonus « si tu l'as payée **uniquement** en
[mental] ». Doom's Mask produit du mental en double pour les sorts, et
Unparalleled Genius est une ressource à **trois** mentales.

Et le sbire némésis, Mister Fantastic, **éteint tout le moteur** : tant qu'il
est engagé, chaque [mental] généré devient [physical].

## 4. Les sept points durs

| # | Point | État |
|---|---|---|
| 1 | **Requirement ([mental])** (`dd003`) | ✅ **RÉSOLU** : mot-clé OFFICIEL, base automatique `desc.Requirement` (has_cost.py:24), 8 cartes officielles l'emploient. Aucun script. Fiche créée : `docs/reference/mots-cles/requirement.md`. |
| 2 | Deux règles de **deckbuilding** sur `dd001b` | « Aucun allié supplémentaire » **et** « jusqu'à 6 TECH/SPELL hors aspect ». Le plan n'annonçait que la seconde. Sans précédent connu. |
| 3 | Le héros **gagne villainous** | Mot-clé de vilain appliqué au joueur, plus « ignore les effets de boost ». |
| 4 | **Doomstadt** : sorts glissés dessous, jouables de là (max 3) | Proche d'aa002 Scarlet Witch (événement attaché, jouable). |
| 5 | **Mister Fantastic** : [mental] → [physical] | Substitution de couleur à la génération. |
| 6 | **Doom's Mask** : 1 mental, ou 2 pour un SPELL | Piège `ho009` connu : la couleur est figée AVANT le paiement. |
| 7 | **"Doom Prevails"** : lit 3 cartes du deck rencontre | Compte leurs icônes de boost (★ et ▼) ; `CountTotalBoostIcons` existe. |

## 5. Collision de noms

**Mister Fantastic** : héros officiel `mf001a` et allié `iw002` (Invisible
Woman). Notre `dd015` est un **sbire némésis** homonyme. À documenter dans le
`collision_note` du deck de départ, et à ne pas confondre au moment des tests.

## 6. Journal des étapes

| Étape `PROCESSUS-HEROS` | État | Preuve |
|---|---|---|
| Inventaire du zip | ✅ | 17 entrées, aucune carte manquante. Le zip « Alt Arts » écarté : 16 cartes sans rapport (§1). |
| `cards.json` + `sets_info.json` | ✅ | set 139, `dd001a`…`dd016`, checksums refaits. |
| Images | ✅ | 17 `.png` dans `assets/pics/`. `dd014`, livrée en portrait, pivotée (convention 01107). |
| Modules | ✅ | 15 modules dans `src/cards/pack/doctor_doom/doctor_doom/`. `dd007` (ressource) et `dd001b` (règles de deckbuilding) n'en ont pas. |
| Textes FR | ✅ | 17 entrées dans `textes-fr-fanmade.ts`. |
| Biographie | ✅ | `heros-info.js`, `dd001a`, FR + EN. |
| Deck de départ | ✅ | `deck/starter/doctor_doom.json`, **Agression**, 15 signature + 25 aspect. |
| Deck némésis | ✅ | `data/nemesis/doctor_doom_nemesis.json`. |
| Cas de test | ✅ | **17/17** (`test_capacites.py [dd0]`). |
| Substitution | ✅ | **15/15 cartes** — aucun cas ne reste vert sans son module. |
| Autoplay | ✅ | 8 parties, **0 erreur**, 4,4 rounds. `Power_Syphon` ×13, `Overwhelming_Power` ×1. |
| Légalité du deck | ✅ | `verifier_tous_les_decks.py DECK_NOM=doctor_doom`. A attrapé 3 fautes (Kaluu allié Leadership, 2 cartes ni TECH ni SPELL). |
| Gabarits `PROCESSUS-CARTE` | ✅ | `.planning/todos/2026-09-01-doom-gabarits-processus-carte.md`, 17/17 « OUI ». |
| Batterie complète | ✅ | Due : 4 fichiers moteur partagés modifiés (§4). Verdict au §7. |
| **Partie jouée à la main** | ⬜ | **Seul point restant de la gate.** |

## 7. Extension du moteur — ce qu'il faut retenir

Quatre fichiers **partagés** touchés, ce qui déclenche la batterie complète
(règle §6bis du GUIDE) :

1. `identity.py` — `Hero` hérite désormais de `HasVillainous`. Inerte par
   défaut (`printed_villainous` vaut 0), mais **confirmé comme la bonne place**
   par l'annonce FFG « Killer Instinct » du 13/08/2026 : Elektra sera le
   premier héros OFFICIEL à porter le mot-clé. À garder tel quel.
2. `can_boost.py` — garde `if num <= 0: return`. **Indispensable** : sans lui,
   tout héros non villainous plantait à chaque attaque de base, `CastTo(Minion
   | Villain)` levant un assert. Le défaut ne venait pas de Doom, il était
   latent et la ligne 1 l'a réveillé.
3. `face_action.py` — paramètre `villainous` ajouté à `TemporaryGain` et
   `GainUntilRoundEnd`, que `Gain` acceptait déjà. Même oubli que `retaliate`
   le 4/8/2026.
4. `puzzle.py` — `Puzzle.PlaceCounters`, sans quoi aucune capacité qui
   **dépense** des compteurs n'est testable isolément.

**Reste pour Elektra** : la **défense** n'a aucun chemin de distribution de
cartes de boost (l'attaque l'a en `can_attack.py:220`, la manigance en
`can_scheme.py:92`). Doom n'en a pas eu besoin, `dd010` n'accrochant que
l'attaque de base.
