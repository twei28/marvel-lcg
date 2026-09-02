# PRÉ-PORTAGE — Viv Vision (Rainy)

**Statut : dossier de préparation. AUCUN fichier du moteur n'a été touché.**
Préparé le 02/09/2026 pendant qu'une autre session travaillait sur le dépôt.
Zip : `Viv Vision-20260902T074028Z-1-001.zip`, 21 images, **12 cartes distinctes**.
Difficulté : **2/5**. C'est le plus petit pack du deuxième arrivage.

## 1. Identité du pack

| Champ | Valeur proposée |
|---|---|
| Préfixe | `vv` (vérifié libre dans `tools/prefixes_fanmade.json` le 02/09) |
| Numéro de set | `147` (premier libre après `146. Custom (Necroverse)`) |
| Libellé | `147. Custom (Viv Vision)` |
| `set_name` héros | `Viv Vision` (vérifié libre) |
| `set_name` némésis | **sans objet, voir §5** |
| Dossier | `src/cards/pack/viv_vision/viv_vision/` |

## 2. Inventaire, texte imprimé relevé sur les scans

Numérotation imprimée : `VIV VISION (n/15)`. 15 exemplaires, **9 cartes
signature distinctes** (les doublons sont des copies), plus 2 faces d'identité
et 1 obligation.

| card_id | n/15 | Nom | Type | Coût | RES | Traits | Texte imprimé |
|---|---|---|---|---|---|---|---|
| `vv001a` | — | ★ Viv Vision | Hero | — | — | ANDROID. CHAMPION. | THW 1 / ATK 1 / DEF 1 / HS 5 / PV 10. *Density Manipulation* — **Action**: Spend a ⚡ resource → you get +2 to a chosen basic power until the end of the round. (Limit once per round.) |
| `vv001b` | — | ★ Viv Vision | AlterEgo | — | — | ANDROID. | REC 3 / HS 6 / PV 10. *Recharge* — **Action**: Choose a card with a printed ⚡ resource in your discard pile and place it on top of your deck. (Limit once per round.) |
| `vv002` | 1 | Hologram Projection | Event | 2 | 🧠 | SUPERPOWER. | Requirement (⚡🧠). **Hero Interrupt**: When an enemy would activate, cancel that activation and confuse that enemy. |
| `vv003` | 2, 3 | Just a Phase | Event | 1 | 🧠 | SUPERPOWER. THWART. | **Hero Interrupt**: When your hero makes a basic thwart, they get +3 THW and ignore the patrol keyword and the crisis icon for that thwart. This thwart gains breakthrough. |
| `vv004` | 4, 5 | Phase Up | Event | 1 | ⚡ | DEFENSE. SUPERPOWER. | Requirement (⚡). **Interrupt** *(defense)*: When you would take any amount of damage, prevent all of that damage. You gain stalwart until the end of the round. |
| `vv005` | 6, 7, 8, 9 | Solar Beam | Event | 2 | ⚡ | ATTACK. SUPERPOWER. THWART. | Requirement (⚡). **Hero Action** *(attack)*: Deal 5 damage to an enemy. This attack gains ranged. **Hero Action** *(thwart)*: Remove 4 threat from a scheme. |
| `vv006` | 10, 11 | Superdense Strike | Event | 2 | 💪 | ATTACK. SUPERPOWER. | **Hero Interrupt**: When your hero makes a basic attack against an enemy, she gets +4 ATK for that attack and that attack gains piercing. Give your hero a tough status card. |
| `vv007` | 12 | ★ Sparky the Dog | Support | 1 | ⭐ | ANDROID. GOOD BOY. | **Hero Interrupt**: When a minion initiates an attack, exhaust Sparky the Dog → deal 2 damage to that minion. **Alter-Ego Action**: Exhaust Sparky the Dog → heal 1 damage from your identity. |
| `vv008` | 13 | Computer Mind | Upgrade | 1 | 🧠 | CONDITION. SUPERPOWER. | **Response**: After you play a card that has the requirement keyword, exhaust Computer Mind → draw 1 card for each required resource on that card. |
| `vv009` | 14 | Insubstantial Flight | Upgrade | 2 | ⚡ | SUPERPOWER. | Requirement (⚡). You gain the AERIAL trait. **Hero Response**: After your hero exhausts, exhaust Insubstantial Flight → ready your hero. |
| `vv010` | 15 | ★ Viv's Solar Gem | Upgrade | 2 | ⚡ | ITEM. | **Resource**: Exhaust Viv's Solar Gem → generate a ⚡ resource. **Response**: After the villain phase ends, ready Viv's Solar Gem. |
| `vv011` | — | Grounded | Obligation | — | — | — | *Give to the Viv Vision player.* Flip to alter-ego form. You cannot change form. **Alter-Ego Action**: Exhaust your alter-ego → remove Grounded from the game. |

> Les 12 cartes ont été lues sur les scans, une par une, le 02/09/2026.
> Les icônes de ressource de la colonne RES ont été lues à vue : **à vérifier
> contre une carte du même pack avant l'étape 1** (leçon Lockjaw, PROCESSUS-CARTE
> étape 3). Toute valeur chiffrée repasse par l'étape 6 de toute façon.

## 3. Étape 2 du PROCESSUS-CARTE, pré-remplie

Vérifié dans `data/cards.json` et `src/cards/pack/` le 02/09/2026.

| Capacité | Carte de référence | Pourquoi |
|---|---|---|
| `vv001a` « Spend a ⚡ → +2 à un pouvoir de base choisi jusqu'à la fin du round » | **`01068` ★ Vision (allié du Core Set)**, `src/cards/pack/core/01068.py` | Texte quasi identique : « Spend a [energy] resource → choose THW or ATK. Until the end of the phase, Vision gets +2 to the chosen power. » Deux écarts à coder : *round* et non *phase*, et le choix porte sur les TROIS pouvoirs de base, pas deux. **Ne PAS partir du héros officiel `26001a`** : sa capacité est la forme de masse recto-verso, sans rapport. |
| `vv001b` « prendre une carte à ressource ⚡ imprimée dans la défausse et la mettre sur le deck » | à chercher : famille « récupérer depuis la défausse » (`al007`, `aa009` utilisent `discard_pile`) | Le filtre porte sur la RESSOURCE IMPRIMÉE de la carte : recette §4 de `RECETTES-MOTEUR.md`, `FacesCounter.GetPrintedResources([face])` (modèles `21006`, `ho009`). |
| `vv004`, `vv005` « Requirement (⚡) » | fiche `mots-cles/requirement.md` **déjà écrite** | Ne pas recoder le mot-clé. |
| `vv004` « prevent all of that damage » + stalwart | famille prévention (`im`/`si` : Energy Shield, Endo-Sym) | — |
| `vv005` « This attack gains ranged » | fiche `mots-cles/ranged.md` **déjà écrite** (écrite au portage Gorr) | — |
| `vv003` « ignore the patrol keyword and the crisis icon » | fiches `patrol.md` et `crisis.md` **déjà écrites** | — |

## 4. Collisions de noms, vérifiées dans `data/cards.json`

| Nom | Collision | Conséquence |
|---|---|---|
| **Solar Beam** | `26008` Event, `set_name` **Vision**, `desc.Class = "Hero"` + `57051` Treachery | Carte signature d'un AUTRE héros. Le `collision_note` du deck doit le dire, et le contrôle « jamais une signature d'un autre héros dans un deck » de PROCESSUS-HEROS étape 10 doit être relancé. |
| **Superdense Strike** | `26009` Event, `set_name` **Vision**, `desc.Class = "Hero"` + `57052` Treachery | Idem. |
| **Grounded** | `47023` Obligation (Jubilee), `wd041` Environment (Electro) | Deux homonymes, aucun risque fonctionnel, à noter. |
| `set_name` **Vision** | PRIS par le héros officiel | Sans objet ici : on prend `Viv Vision`, vérifié libre. |

Les 8 autres noms du pack sont libres.

## 5. ⚠ Questions à poser AVANT d'écrire le premier script

À poser une par une, en multichoix, option recommandée en premier (règle du
PROCESSUS-CARTE étape 3). Elles sont rédigées ici pour ne pas être oubliées ;
c'est la session qui porte qui les pose.

**Q1 — Le mot-clé `breakthrough` (carte `vv003` Just a Phase).**
Vérifié le 02/09 : **0 occurrence** dans les 5 635 cartes de `data/cards.json`,
rien dans `src/`, aucune fiche dans `docs/reference/mots-cles/`. Le pack ne le
définit nulle part (12 cartes, aucun insert de règles fourni).
- A) *(recommandé)* Le coder comme l'`overkill` de la menace : la menace retirée
  en excès d'une manigance se reporte sur une autre manigance. C'est la lecture
  naturelle par symétrie avec `overkill`, et elle colle au reste de la carte
  (qui ignore déjà `patrol` et `crisis`).
- B) Le coder comme « la menée touche toutes les manigances », plus fort.
- C) Écrire à l'auteur (Rainy) avant de coder, et laisser la carte de côté.
- D) Autre (précise).

**Q2 — Le pack n'a AUCUNE carte némésis.**
15 cartes signature + 1 obligation, et rien d'autre. Vérifié : sur les **111
decks de départ** du dépôt, **aucun** n'a de `nemesis_set` vide. L'obligation
`vv011` ne convoque personne, donc elle fonctionne seule, mais le pack sort du
gabarit de PROCESSUS-HEROS étape 1.
- A) *(recommandé)* Livrer sans set némésis, `nemesis_set: []`, et le dire dans
  la note du préfixe. C'est fidèle au matériel fourni.
- B) Emprunter le set némésis du Vision officiel.
- C) Écrire à l'auteur.
- D) Autre (précise).

**Q3 — L'aspect du deck de départ.**
Aucune decklist n'est fournie par l'auteur.
- A) *(recommandé)* **Protection** : `vv004` Phase Up prévient tous les dégâts et
  donne stalwart, `vv009` Insubstantial Flight et `vv010` Solar Gem vont dans le
  même sens, et c'est l'aspect du Vision officiel.
- B) **Justice** : `vv003` et `vv005` sont deux grosses cartes de menée.
- C) **Agressivité**.
- D) Autre (précise).

**Q4 — Le dossier « Vivian alt cards ».**
Le zip contient une seconde version de `0.1`, `0.2` et `Grounded`. À l'œil ce
sont des ARTS ALTERNATIFS, pas des règles différentes, mais ça n'a pas été
comparé texte contre texte.
- A) *(recommandé)* Comparer les deux jeux texte contre texte. Si le texte est
  identique, déclarer la variante dans `metadata.hero_alts` du deck (mécanisme de
  `GUIDE-CREATION-CONTENU.md` §5.3), **jamais** un second deck de départ.
- B) Ignorer les cartes alternatives.
- C) Autre (précise).

## 6. Ce que ce dossier ne fait PAS

- Aucune entrée dans `data/cards.json`, `data/sets_info.json`,
  `tools/prefixes_fanmade.json` : ce sont les trois fichiers partagés qui
  s'écrasent entre sessions (§4 du plan `2026-08-29-plan-heros-vilains-fanmade`).
- Aucun script, aucun test, aucune image déposée dans `assets/pics/`.
- Aucune biographie dans `heros-info.js`, aucun texte FR dans
  `textes-fr-fanmade.ts`.
- Les étapes 5 à 8 du PROCESSUS-CARTE (texte-contre-code, nombres, tests par
  capacité avec preuve par substitution, autoplay) restent entièrement dues.
