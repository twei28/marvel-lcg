# Portage du pack VENOMPOOL — journal de validation

Set 129, préfixe `vp`, 17 `card_id`. Auteur **CptScorp**, *Marvel Champions
Custom Project*, Cycle 2. Zip source : `A créer/Venompool (Council
Released)-20260813T091211Z-1-001.zip`.

Ce document tient le gabarit `PROCESSUS-CARTE.md` pour chaque carte du pack,
comme l'exige la « Gate finale » de `PROCESSUS-HEROS.md`.

---

## 0. Ce que le pack apporte au projet, au-delà du héros

### `drain X` a enfin une définition imprimée

L'insert du pack (« Venompool Insert.png ») définit le mot-clé maison resté
sans définition depuis `agent_anti_venom` :

> « When an ability instructs you to drain X from an enemy, deal X damage to
> that enemy, then heal X damage from your identity. »

C'est **mot pour mot** la lecture arbitrée à l'aveugle avec l'utilisateur le
4/8/2026. `docs/reference/mots-cles/drain-x.md` est mis à jour : la
convention n'est plus une supposition, et la question systématique qu'exigeait
la fiche avant tout nouvel appel à `Drain()` n'a plus lieu d'être.

### L'icône du side scheme, identifiée par comparaison d'image

`vp012` Shocking Entrance porte une icône « + sur une forme ». Plutôt que de
la nommer à vue (leçon Lockjaw, `PROCESSUS-CARTE.md` étape 3), elle a été
découpée du scan puis superposée aux icônes officielles :

| Carte | Icône | Forme |
|---|---|---|
| 01107 Breakin' & Takin' | **hazard** | « + » sur une **carte inclinée** |
| 01109 Bomb Scare | acceleration | « + » sur une **maison soulignée** |
| **vp012 Shocking Entrance** | **hazard** ✔ | « + » sur une carte inclinée |

`desc.Hazard = "1"`, pas `Acceleration`.

### Quatre homonymes préexistants

| Nom | Carte déjà présente | Conséquence |
|---|---|---|
| **Wade Wilson** | `44001b`, alter-ego officiel de Deadpool | `desc.GiveTo` de `vp011` se résout **par nom** (`Worlds.FindPlayerByName`). L'insert du pack interdit lui-même de jouer Deadpool et Venompool ensemble. |
| **Venompool** | `dt105`, allié de l'aspect fan-made Determination | Un allié à son propre nom est **exclu** du deck. Les modules ne résolvent jamais « Venompool » par son nom, toujours par le joueur (`GetVenompool`). |
| **Black Cat** | `01002` (allié signature de Spider-Man), `wd045` (sbire Electro) | Classe `Hero` : jamais mélangeable. |
| **Thwip!** / **Foresight** | `sr003` (Spider-Man Rainy), `mw009` (Madame Web) | Événements signature d'autres héros, classe `Hero`. |

Tout est consigné dans `metadata.collision_note` de `deck/starter/venompool.json`.

---

## 1. Étapes de `PROCESSUS-HEROS.md`

| Étape | État | Preuve |
|---|---|---|
| 1. Cartes dans `data/cards.json` | ✅ | 17 `card_id`, diff de **305 lignes ajoutées / 0 supprimée** |
| 2. Scripts | ✅ | 17 modules, `test_cards` 4895 → **4912 ok / 0 err** |
| 3. Deck de départ | ✅ | `deck/starter/venompool.json`, 15 signature + 25 aspect/basiques |
| 4. `data/nemesis/…` | ⬜ | facultatif (UI), non fourni |
| 5. `data/sets_info.json` | ✅ | set « 129. Custom (Venompool) » |
| 6. Images | ✅ | 17 `.jpg` en 975 px extraits des scans du zip |
| 7. Biographie | ✅ | `vp001a` dans `heros-info.js`, `node --check` propre |
| 8. Textes français | ✅ | 17 entrées, `tsc --noEmit` propre |
| 9. Validation carte par carte | 🟡 | en cours, §2 ci-dessous |
| 10. Points transverses | ✅ | 0 carte signature étrangère dans un `player_deck` |

**Aspect** : contrairement à `ms_america` et `patriot`, l'auteur fournit sa
decklist complète (planche « Venompool Starter Deck ») — aspect **Protection**,
aucun choix à faire.

---

## 2. Arbitrages posés à l'utilisateur

| Carte | Question | Réponse (31/08/2026) |
|---|---|---|
| `vp016` Psyche Warp | « the ally with the highest printed ATK » : quels alliés ? | **Tes alliés seulement.** En multi, la carte ne peut pas défausser l'allié d'un coéquipier. |

Points **non** soumis à question, et pourquoi :

- **`vp007` « attacks » vs `vp010` « makes a basic attack »** : le contraste est
  imprimé dans le même pack, il est donc voulu. `is_basic_attack=None` sur
  l'un, `True` sur l'autre.
- **`vp001a` « Limit 1 [per_hero] per phase »** : sur une carte d'identité,
  l'icône joueur ne peut désigner que le porteur — personne d'autre ne
  déclenche la Response d'une identité qui n'est pas la sienne.
- **`vp006` « Each enemy may only be targeted once »** : rendu par l'absence de
  `repeat_rules`, là où `vp003` (« divided as you choose ») en a besoin. Choix
  technique, pas arbitrage de règles.
- **`vp011` « You MUST flip »** : `48026` et `16053`, les deux obligations
  modèles, disent « you MAY flip ». Le changement de forme est ici **forcé**,
  le helper `YouMayFlipToYourAlterEgoForm` n'est donc pas utilisé.

---

## 3. Gabarit par carte

*(rempli au fil des validations — voir §4 pour l'état des preuves)*

---

## 4. Ce qui reste à prouver

- cas `test_capacites` pour chaque capacité, avec preuve par substitution ;
- `tools/autoplay.py`, 8 parties minimum contre un héros témoin ;
- une partie complète jouée à la main dans le navigateur.
