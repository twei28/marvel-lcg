# PRÉ-PORTAGE — Lady Sif (Rainy)

**Statut : dossier de préparation. AUCUN fichier du moteur n'a été touché.**
Zip : `Lady Sif-20260902T073844Z-1-001.zip`, 23 images, **18 cartes distinctes**.
Difficulté : **2/5**. C'est le seul pack de la vague 0 **avec un set némésis
complet**, donc le seul qui respecte le gabarit de `PROCESSUS-HEROS.md`.

## 1. Identité du pack

| Champ | Valeur proposée |
|---|---|
| Préfixe | `ls` (vérifié libre le 02/09) |
| Numéro de set | `150` |
| Libellé | `150. Custom (Lady Sif)` |
| `set_name` héros | `Lady Sif` — **vérifié libre** (le `06002` officiel est un ALLIÉ, pas un set) |
| `set_name` némésis | `Lady Sif Nemesis` |
| Dossier | `src/cards/pack/lady_sif/lady_sif/` et `.../lady_sif_nemesis/` |

## 2. Inventaire, texte imprimé relevé sur les scans

`LADY SIF (n/15)` : 15 exemplaires, **12 cartes signature distinctes**, plus
2 faces d'identité, 1 obligation et 5 cartes némésis.

| card_id | n | Nom | Type | Coût | RES | Traits | Texte imprimé |
|---|---|---|---|---|---|---|---|
| `ls001a` | — | ★ Lady Sif | Hero | — | — | ASGARD. SOLDIER. | THW 1 / ATK 2 / DEF 2 / HS 5 / PV 13. *Valiant Warrior* — **Response** *(thwart)*: After Lady Sif uses a basic power, remove 1 threat from a scheme. |
| `ls001b` | — | ★ Lady Sif | AlterEgo | — | — | ASGARD. SOLDIER. | REC 4 / HS 6 / PV 13. *Shieldmaiden* — **Action**: Ready a friendly ASGARD character. (Limit once per round.) |
| `ls002` | 1 | ★ Thor (Odinson) | Ally | 3 | ⭐ | ASGARD. AVENGER. | THW 1 / ATK 2★ / PV 3. ★ **Response**: After Thor attacks, choose a player. Deal 1 damage to each minion engaged with that player. |
| `ls003` | 2, 3 | Impale | Event | 3 | 💪 | ATTACK. SKILL. | **Hero Action** *(attack)*: Deal 6 damage to an enemy. Choose for this attack to gain either overkill or piercing. |
| `ls004` | 4, 5, 6 | Lead The Charge | Event | 1 | 💪 | ATTACK. TACTIC. | **Hero Action** *(attack)*: Lady Sif makes a basic attack without exhausting. Choose another friendly character. That character gets +1 ATK until the end of the round. |
| `ls005` | 7 | To Arms! | Event | 0 | ⚡ | TACTIC. | **Alter-Ego Action**: Change to hero form. You may spend 1 resource to ready your hero. **Hero Action**: Search your deck and discard pile for a WEAPON upgrade and add it to your hand. Shuffle your deck. |
| `ls006` | 8, 9, 10 | Valiant Defense | Event | 1 | ⚡ | DEFENSE. TACTIC. | **Hero Interrupt** *(defense)*: When an enemy attacks, make a basic defense without exhausting your hero. You get +1 DEF for this attack (+2 DEF instead if you paid for this card using a ⚡ resource). |
| `ls007` | 11 | ★ Sif's Chambers | Support | 1 | 🧠 | ASGARD. LOCATION. | **Alter-Ego Action**: Exhaust Sif's Chambers → heal 1 damage from Lady Sif. Heal 1 damage from Thor or Odinson. Choose a Lady Sif card in your discard pile and shuffle it into your deck. |
| `ls008` | 12 | ★ Sif's Steed | Support | 3 | ⚡ | ASGARD. CREATURE. | **Hero Response**: After Lady Sif exhausts, exhaust Sif's Steed → ready Lady Sif. **Hero Action**: Exhaust Sif's Steed → ready Lady Sif. |
| `ls009` | 13 | ★ Sif's Crest | Upgrade | 3 | 🧠 | ARMOR. ASGARD. | You get +2 hit points. **Hero Interrupt**: When Lady Sif uses a basic power, draw 1 card. (Limit once per phase.) |
| `ls010` | 14 | ★ Sif's Spear | Upgrade | 1 | 💪 | ASGARD. WEAPON. | Restricted. Lady Sif gets +1 DEF while in hero form and gains retaliate 1. |
| `ls011` | 15 | ★ Sif's Sword | Upgrade | 2 | 💪 | ASGARD. WEAPON. | Restricted. Lady Sif gets +1 ATK while in hero form. While in hero form, Lady Sif's basic attacks gain piercing. |
| `ls012` | — | Unrequited Love | Obligation | — | — | — | *Give to the Lady Sif player.* You may flip to alter-ego form. Stun Lady Sif. Stun or confuse Thor. If you cannot, confuse Lady Sif. Discard this obligation. |
| `ls013` | N 1/5 | Captivating Wiles | SideScheme | — | 3🧑 | — | *The Enchantress is manipulating us to do her dirty work for her!* **Forced Interrupt**: When the player phase begins, exhaust the first player's identity and place 2 threat on the main scheme. ★ **Boost**: Place 2 threat on the main scheme. |
| `ls014` | N 2/5 | ★ Enchantress | Minion | — | — | ASGARD. ELITE. | SCH 3 / ATK 2 / PV 5. **Forced Interrupt**: When Enchantress is attacked, declare the engaged hero the defender (without exhausting). If you cannot, cancel that attack and place 2 threat on the main scheme instead. (Limit once per phase.) |
| `ls015` | N 3/5 | ★ Skurge | Minion | — | — | ASGARD. | SCH 1 / ATK 3★ / PV 5. Teamwork (ASGARD). Toughness. ★ **Forced Interrupt**: When Skurge attacks you, he attacks the character you control with the fewest remaining hit points. This attack gains overkill and piercing. ★ **Boost**: Defeat an ally you control. |
| `ls016` | N 4/5 | Hypnotic Suggestion | Attachment | — | — | TEMPTATION. | Attach to your identity. **Forced Action**: Exhaust this card → draw 1 card, then play that card (paying its costs). If you cannot, place 2 threat on the main scheme. **Alter-Ego Action**: Exhaust this card and spend a 🧠 resource → discard this card. |
| `ls017` | N 5/5 | Love Concoction | Attachment | — | — | ITEM. TEMPTATION. | Attach to your identity. **Forced Action**: Exhaust this card and give the villain a facedown boost card → ready your identity. **Alter-Ego Action**: Exhaust this card and give the villain a facedown boost card → discard this card. ★ **Boost**: Reveal this card. |

> Les 18 cartes ont été lues sur les scans, une par une, le 02/09/2026.
> Icônes de ressource lues à vue : à vérifier contre une carte du même pack.

## 3. Étape 2 du PROCESSUS-CARTE, pré-remplie

| Capacité | Carte de référence | Pourquoi |
|---|---|---|
| `ls006` « +2 DEF **si tu as payé avec une ressource ⚡** » | **`01013` Photonic Blast** (`effect.GetPaidResources().HasColor("Y")`) et `01060` For Justice! | ⚠ **Ce n'est PAS une brique neuve** : 306 cartes officielles portent cette tournure, la fabrique `play.py` l'expose nativement. |
| `ls001a` « After Lady Sif uses a basic power » | `Texas Twister`, mais surtout la famille officielle « After you use a basic power » | Déclencheur standard. |
| `ls001b`, `ls008` « ready a friendly character » | famille officielle Leadership | — |
| `ls002` « deal 1 damage to each minion engaged with that player » | `04006` / `ho004` (recette §6, cible littérale) | — |
| `ls004` « makes a basic attack **without exhausting** » | famille officielle (Relentless Assault, Sif's Steed inverse) | — |
| `ls005` « search deck **and discard pile** for a WEAPON » | `bt`, `si001b` (recherche dans le deck) | La fouille de la DÉFAUSSE en plus est la nuance à vérifier. |
| `ls010` « Restricted » | **base automatique**, lue dans `desc` : **aucun module à écrire** (PROCESSUS-CARTE étape 5) | Piège classique : ne pas la recoder. |
| `ls010` « retaliate 1 » | fiche `mots-cles/retaliate.md` **déjà écrite** | — |
| `ls015` « Toughness » | **base automatique**, lue dans `desc` | Idem, ne pas recoder. |
| `ls015` « Teamwork (ASGARD) » | **`32159` à `32163`** (Acolytes) et **`38029` à `38031`** (Reavers) : **31 cartes officielles** portent ce mot-clé | ⚠ Le mot-clé existe dans le moteur (fabriques `environment`), mais **aucune fiche** dans `docs/reference/mots-cles/`. Voir §5 Q1. |
| `ls014` « declare the engaged hero the defender » | à chercher, aucun modèle identifié le 02/09 | Point d'attention n°1 du pack. |
| `ls016` « draw 1 card, then play that card (paying its costs) » | à chercher : famille « jouer une carte de force » | Point d'attention n°2. Le « If you cannot » doit être testé comme cas réellement atteignable (piège `wd028`). |
| `ls017` « give the villain a facedown boost card » | famille boost (`ag`, `wc` comptent les icônes) ; ici on en AJOUTE une | — |

## 4. Collisions de noms, vérifiées dans `data/cards.json`

| Nom | Collision | Conséquence |
|---|---|---|
| **Lady Sif** | `06002` Ally set **Thor**, `desc.Class = "Hero"` + `21190` Ally (campagne MTS) | L'allié officiel Lady Sif est une signature de Thor. Le héros `ls001a` porte le même nom : `collision_note` obligatoire, et le contrôle de PROCESSUS-HEROS étape 10 doit être relancé. |
| **Thor** | `06001a` Hero, `13011`/`25013`/`59020` Ally, `ra001a` Hero (Jane Foster), `mk020` Minion | 6 homonymes. L'allié `ls002` est une carte distincte de `13011`. |
| **Enchantress** | `21177` Minion, `25029` Minion (Valkyrie Nemesis), `55001-03` Villain | Le sbire `ls014` est une 5ᵉ Enchantress. |
| **Skurge** | `21144` Minion (Hela) | Deuxième Skurge. |
| **Hypnotic Suggestion** | `ag014` Treachery (Agent 13 Nemesis) | Homonyme d'un pack MAISON, pas officiel. |
| **Love Concoction** | `55014` Attachment (Enchantress) | Même personnage source, deux cartes différentes. |
| `set_name` **Lady Sif** | **libre** | Rien à trancher, contrairement à Hulk et Iron Man. |

Libres : Impale, Lead The Charge, To Arms!, Valiant Defense, Sif's Chambers,
Sif's Steed, Sif's Crest, Sif's Spear, Sif's Sword, Captivating Wiles,
Unrequited Love.

## 5. ⚠ Questions à poser AVANT d'écrire le premier script

**Q1 — Le mot-clé `teamwork` n'a pas de fiche.**
Vérifié le 02/09 : 31 cartes officielles le portent, le moteur le connaît
(`src/game/ability/factory/environment*.py`), mais
`docs/reference/mots-cles/` ne l'a pas. La règle du CLAUDE.md est explicite :
fiche absente → la créer AVANT d'écrire une ligne de code.
- A) *(recommandé)* Créer `mots-cles/teamwork.md` sur le gabarit du README, en
  relevant le mécanisme réel dans `environment.py` et en citant `32159` comme
  carte témoin. Le faire une fois sert aussi à Blade (vague 4).
- B) Coder sans fiche.
- C) Autre (précise).

**Q2 — `ls014` Enchantress, « declare the engaged hero the defender ».**
La carte force le héros à défendre une attaque **que le joueur porte**, sans
l'épuiser, et bascule sur une annulation d'attaque « If you cannot ».
- A) *(recommandé)* Chercher un modèle au grep avant de coder, puis poser la
  question du cas exact où « you cannot » est atteignable (piège `wd028` : un
  « If you cannot » qui teste un cas impossible est une carte à moitié morte).
- B) Coder les deux branches au jugé.
- C) Autre (précise).

**Q3 — L'aspect du deck de départ** (aucune decklist fournie).
- A) *(recommandé)* **Leadership** : `ls002` Thor, `ls001b` Shieldmaiden,
  `ls004` Lead The Charge et `ls007` Sif's Chambers tournent tous autour des
  alliés et du prêt de personnages ASGARD.
- B) **Agressivité** : `ls003` Impale et `ls011` Sif's Sword tapent fort.
- C) **Protection** : `ls006` Valiant Defense et `ls010` Sif's Spear.
- D) Autre (précise).

**Q4 — `ls007` Sif's Chambers : « Heal 1 damage from Thor or Odinson ».**
« Odinson » n'est le nom d'aucune carte du pack. C'est le sous-titre de `ls002`
(★ Thor — Odinson). Le texte semble donc viser une seule et même carte.
- A) *(recommandé)* Lire « Thor ou Odinson » comme « la carte alliée Thor de ce
  pack, quel que soit le nom sous lequel elle est référencée », et soigner le
  `collision_note` pour que la cible ne soit pas un autre Thor du jeu.
- B) Traiter « Odinson » comme un allié absent du zip et le réclamer à l'auteur.
- C) Autre (précise).

## 6. Ce que ce dossier ne fait PAS

Identique aux autres dossiers de la vague 0.
