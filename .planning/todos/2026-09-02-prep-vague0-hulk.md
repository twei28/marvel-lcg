# PRÉ-PORTAGE — Hulk (Rainy)

**Statut : dossier de préparation. AUCUN fichier du moteur n'a été touché.**
Zip : `Hulk-20260902T073908Z-1-001.zip`, 19 images, **14 cartes distinctes**
(+ 1 visuel de boîte). Difficulté : **2/5**.

## 1. Identité du pack

| Champ | Valeur proposée |
|---|---|
| Préfixe | `hk` (vérifié libre le 02/09) |
| Numéro de set | `148` |
| Libellé | `148. Custom (Hulk)` |
| `set_name` héros | ⚠ **`Hulk` est PRIS** par le héros officiel `10001a`. Voir §5 Q1. |
| `set_name` némésis | **sans objet**, le pack n'a pas de set némésis. Voir §5 Q2. |
| Dossier | `src/cards/pack/hulk_rainy/...` (nom à trancher avec le `set_name`) |

## 2. Inventaire, texte imprimé relevé sur les scans

Numérotation imprimée `HULK (n/15)` : 15 exemplaires, **11 cartes signature
distinctes**, plus 2 faces d'identité et 1 obligation.

| card_id | n/15 | Nom | Type | Coût | RES | Traits | Texte imprimé |
|---|---|---|---|---|---|---|---|
| `hk001a` | — | ★ Hulk | Hero | — | — | AVENGER. GAMMA. | THW 0 / ATK 2 / DEF 3 / HS 4 / PV 15. *Anger* — **Response**: After Hulk takes damage, deal 1 damage to an enemy. |
| `hk001b` | — | ★ Bruce Banner | AlterEgo | — | — | GENIUS. SCIENTIST. | REC 4 / HS 6 / PV 15. *Bring Out The Big Guy* — **Interrupt**: When an enemy would scheme, spend a 💪 resource → change to your hero form. That enemy attacks you instead. |
| `hk002` | 1 | ★ Black Widow | Ally | 3 | ⭐ | AVENGER. S.H.I.E.L.D. SPY. | THW 2★ / ATK 1★ / PV 3. ★ **Response**: After Black Widow thwarts, remove 1 threat from another scheme. **Hero Action**: Exhaust Black Widow → flip to your alter-ego form. |
| `hk003` | 2, 3 | Brilliant Mind | Event | 2 | 🧠 | THWART. | **Alter-Ego Action** *(thwart)*: Remove 3 threat from a scheme. If you paid for this card using only 🧠 resources, choose to either remove 2 additional threat from that scheme or confuse an enemy. |
| `hk004` | 4, 5 | Hulk Smash | Event | 3 | 💪 | ATTACK. SUPERPOWER. | **Hero Action**: Make the following attacks against the same target: • *(attack)*: Deal 3 damage. • *(attack)*: Deal 3 damage. • *(attack)*: Deal 3 damage. |
| `hk005` | 6, 7 | Interception | Event | 0 | 💪 | TACTIC. | **Hero Interrupt**: When a treachery is revealed, take 2 damage → cancel all of its effects and discard it. If you overpaid for this card with a ⚡ or 💪 resource, remove 2 threat from a scheme. |
| `hk006` | 8, 9 | Reckless Charge | Event | 1 | 💪 | ATTACK. SUPERPOWER. | **Hero Action** *(attack)*: Deal 1 damage to Hulk → deal 3 damage to an enemy. If you paid for this card using a 💪 resource, this attack gains overkill. |
| `hk007` | 10 | Natural Genius | Resource | — | 🧠🧠 | — | Spend this card only in alter-ego form. |
| `hk008` | 11 | Unnatural Strength | Resource | — | 💪💪 | — | Spend this card only in hero form. |
| `hk009` | 12 | The Other Guy | Support | 2 | 🧠 | GAMMA. PERSONA. | **Alter-Ego Response** *(thwart)*: After you change form, remove 1 threat from a scheme. (Limit once per phase.) **Hero Response** *(attack)*: After you change form, deal 1 damage to an enemy. (Limit once per phase.) |
| `hk010` | 13 | Intimidating Roar | Upgrade | 1 | 🧠 | SKILL. SUPERPOWER. | **Hero Response** *(thwart)*: After Hulk takes damage from an attack, exhaust Intimidating Roar → remove 1 threat from a scheme (2 threat instead if you took 3 or more damage). |
| `hk011` | 14 | Limitless Endurance | Upgrade | 3 | ⚡ | CONDITION. GAMMA. SUPERPOWER. | You get +3 hit points and Bruce Banner gets +1 REC. **Hero Action**: Exhaust Limitless Endurance → heal 1 damage from Hulk. |
| `hk012` | 15 | Limitless Strength | Upgrade | 3 | 💪 | CONDITION. GAMMA. SUPERPOWER. | Hulk gets +1 ATK. **Hero Resource**: Exhaust Limitless Strength → generate a 💪 resource. |
| `hk013` | — | Inner Conflict | Obligation | — | — | — | *Give to the Bruce Banner player.* Change form (flip your identity). Then: • If you are Bruce Banner, discard 1 random card from your hand. Discard this obligation. • If you are Hulk, exhaust your hero. Discard this obligation. |

> Les 14 cartes ont été lues sur les scans, une par une, le 02/09/2026. Les
> icônes de ressource sont lues à vue : **à vérifier contre une carte du même
> pack** avant l'étape 1 (leçon Lockjaw).

## 3. Étape 2 du PROCESSUS-CARTE, pré-remplie

⚠ **Découverte du 02/09 qui change le coût du pack** : la « provenance du
paiement » n'est PAS une brique neuve. Elle est native.
`effect.GetPaidResources().HasColor("Y")` (modèle `01013` Photonic Blast,
`src/cards/pack/core/captain_marvel/01013.py`), et la fabrique `play.py:292`
expose déjà `message.paid_resources.HasColor(...)`. **306 cartes officielles**
portent ce genre de phrase.

| Capacité | Carte de référence | Pourquoi |
|---|---|---|
| `hk003` « paid for this card using **only** 🧠 » | **`10004` Sub-Orbital Leap** et **`10006` Unstoppable Force** (Hulk officiel), `src/cards/pack/hlk/hulk/` | Même tournure exacte « using only [physical] resources ». Il suffit de changer la couleur. |
| `hk006` « paid for this card using a 💪 » | **`01053` Relentless Assault** | « If you paid for this card using a [physical] resource, this attack gains... » : même phrase, même effet (mot-clé sur l'attaque). |
| `hk005` « **overpaid** with a ⚡ or 💪 » | **`58005` Starstruck** (Wonder Man), `src/cards/pack/wonder_man/wonder_man/58005.py` | « If you overpaid for this card with a [energy] resource, stun that enemy. » Seule différence : deux couleurs acceptées au lieu d'une. |
| `hk005` « cancel all of its effects and discard it » (traîtrise) | `an005` Single Out (Angela) | Annulation d'un « When Revealed » déjà écrite dans un pack maison. |
| `hk004` trois attaques successives sur la même cible | `04006` / `ho004` (recette §6 « AoE ») + `Puzzle.Attack` | Le point délicat est « against the SAME target » : la cible est choisie une fois, pas trois. |
| `hk001a` « After Hulk takes damage, deal 1 damage » | famille Response-après-dégâts (`rg`, `an001a` Frenzy) | — |
| `hk001b` Interruption qui remplace un complot par une attaque | ~~à chercher : aucun modèle identifié~~ → **`52019` Ready for a Fight** (pack `silk`), trouvé au grep le 02/09 par la session de portage | ⚠ **CORRECTION** : le modèle existe, et c'est un jumeau MOT POUR MOT. `52019` imprime « **Interrupt**: When an enemy would scheme, discard Ready for a Fight → change to hero form. That enemy attacks you instead. » Seul le coût diffère (défausser l'amélioration ici, dépenser une ressource physique sur `hk001b`). Montage déjà écrit : `WhenUnitWouldScheme(Interrupt, Enemy, op).SetTarget("YourIdentity")`, puis `ChangeToForm(Hero, effect)`, `message.SetBeInstead(effect)` et `message.trigger.CastTo(Enemy).DoAttackYou(initiator, effect)`. **Le pack n'a donc aucune inconnue**, et la Q4 du §5 est sans objet. |
| `hk007`, `hk008` ressource jouable seulement dans une forme | `.SetPlay(hero_form_only=True)` (recette §5, modèles `01009`, `ho012`) | Vérifier qu'il existe l'équivalent alter-ego. |
| `hk009` Response après changement de forme, une par forme | `dz`/`she_hulk` (trait PERSONA déjà utilisé) | — |

## 4. Collisions de noms, vérifiées dans `data/cards.json`

| Nom | Collision | Conséquence |
|---|---|---|
| **Hulk** | `10001a` Hero (set Hulk), `01050` Ally, `th014` Minion, `62020` Ally | Le nom de la carte peut être identique ; c'est le `set_name` qui doit différer. |
| **Bruce Banner** | `10001b` AlterEgo (set Hulk) | Idem. |
| **Hulk Smash** | `10003` Event, set **Hulk**, `desc.Class = "Hero"` | Signature du Hulk officiel. `collision_note` obligatoire, et le contrôle de PROCESSUS-HEROS étape 10 doit être relancé. |
| **Limitless Strength** | `10007` Resource, set **Hulk**, `desc.Class = "Hero"` | Idem. |
| **Black Widow** | `01075` Ally, `08001a` Hero, `50064-66` Villain, `50148` Minion | 6 homonymes. L'allié `hk002` a des stats différentes de `01075` : deux cartes distinctes qui portent le même nom. |
| `set_name` **Hulk** et **Hulk Nemesis** | PRIS tous les deux | Voir Q1. |

Libres : Brilliant Mind, Interception, Reckless Charge, Natural Genius,
Unnatural Strength, The Other Guy, Intimidating Roar, Limitless Endurance.
« Inner Conflict » : **vérifié libre** le 02/09.

## 5. ⚠ Questions à poser AVANT d'écrire le premier script

**Q1 — Le `set_name`, puisque « Hulk » est déjà pris.**
`IsDeckBuildingClass` compare les `set_name` littéralement (leçon `wolverine_x23`).
- A) *(recommandé)* `Hulk (Rainy)`, sur le modèle de `Thor (Jane Foster)` qui
  existe déjà dans le dépôt (`ra001a`).
- B) `Savage Hulk`, `Immortal Hulk` ou un autre nom de version.
- C) Autre (précise).

**Q2 — Le pack n'a AUCUNE carte némésis** (1 obligation, rien d'autre).
Vérifié : sur les 111 decks de départ du dépôt, aucun n'a de `nemesis_set` vide.
- A) *(recommandé)* Livrer sans set némésis, fidèle au matériel.
- B) Emprunter le set némésis du Hulk officiel.
- C) Autre (précise).

**Q3 — L'aspect du deck de départ** (aucune decklist fournie).
- A) *(recommandé)* **Agressivité** : `hk004` Hulk Smash, `hk006` Reckless
  Charge, `hk012` Limitless Strength et l'`Anger` de l'identité paient tous
  sur les dégâts, et c'est l'aspect du Hulk officiel.
- B) **Protection** : `hk011` Limitless Endurance et les 15 PV vont dans ce sens.
- C) Autre (précise).

**~~Q4 — `hk001b` « That enemy attacks you instead »~~ — SANS OBJET.**
La question prévoyait « chercher d'abord au grep ; si rien, demander ». Le grep
a été fait le 02/09 et il a rendu **`52019` Ready for a Fight**, jumeau mot pour
mot déjà scripté (voir §3). Il n'y a donc rien à arbitrer : on transpose, en
remplaçant le coût de défausse par la dépense d'une ressource physique.

## 6. Ce que ce dossier ne fait PAS

Identique au §6 du dossier Viv Vision : aucune écriture dans `data/cards.json`,
`data/sets_info.json`, `tools/prefixes_fanmade.json`, aucun script, aucun test,
aucune image, aucune bio, aucun texte FR. Étapes 5 à 8 du PROCESSUS-CARTE
entièrement dues.
